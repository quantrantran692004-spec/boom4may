"""Per-phone workflow control after Amazon's Browse menu is open.

The Amazon screen steps are intentionally supplied later. Every step must
inspect the current UI before acting so a manual fix can be resumed safely.
"""
from __future__ import annotations

import math
import re
import shlex
import threading
import time
from dataclasses import dataclass, field
from typing import Callable

from .cloud import CloudPhone, cloud_adb
from .core import ToolError
from .runner import RunJob


class RecoverableStepError(ToolError):
    """Observation/locator failure eligible for a checked, same-step retry."""


@dataclass(frozen=True)
class AttemptDeadline:
    seconds: int | None
    started: float = field(default_factory=time.monotonic)
    visual_until: dict[str, float] = field(default_factory=dict, compare=False, repr=False)
    notice: Callable[[str], None] | None = field(default=None, compare=False, repr=False)

    def recovering(self, message: str) -> None:
        if self.notice is not None:
            self.notice(message)

    def remaining(self) -> float:
        if self.seconds is None:
            return float('inf')
        return max(0.001, self.started + self.seconds - time.monotonic())

    def allowance(self, requested: float) -> float:
        """Give a wait only the time still available in this attempt."""
        if requested <= 0:
            raise ValueError("Requested wait must be positive")
        return min(requested, self.remaining())


StepAction = Callable[[RunJob, AttemptDeadline, threading.Event], None]
Progress = Callable[[int, str, str, str], None]


@dataclass(frozen=True)
class PostMenuStep:
    name: str
    action: StepAction
    within_attempt: bool = True


Reconcile = Callable[[int, RunJob, AttemptDeadline, threading.Event],
                     tuple[int, tuple[PostMenuStep, ...]] | None]
Route = Callable[[int, RunJob, AttemptDeadline, threading.Event], int | None]


@dataclass
class RegistrationState:
    """Keep dispatch markers when a phone's steps are rebound or rewound."""
    sms_requested_at: float | None = None
    code: str = field(default="", repr=False)
    create_pressed: bool = False
    prefix_choices: dict[int, str] = field(default_factory=dict, repr=False)


@dataclass
class PostMenuSession:
    batch_id: str
    index: int
    profile_name: str
    menu_opened_at: float | None = None
    next_step: int = 0
    attempts: int = 0
    state: str = "READY"
    menu_route: str = ""
    last_error: str = ""
    registration: RegistrationState = field(default_factory=RegistrationState,
                                             repr=False)
    bound_serial: str = ""
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    def run(self, job: RunJob, steps: tuple[PostMenuStep, ...],
            emit: Progress, stop: threading.Event,
            reconcile: Reconcile | None = None,
            route: Route | None = None,
            stop_after_step: threading.Event | None = None) -> None:
        """Run this phone only; errors pause at the same step for manual repair."""
        if not steps:
            raise ValueError("Post-menu steps have not been supplied")
        if (job.batch_id, job.index) != (self.batch_id, self.index):
            raise ValueError("Job does not belong to this phone session")
        with self._lock:
            if self.state not in {"READY", "PAUSED"}:
                return
            was_paused = self.state == "PAUSED"
            self.attempts += 1
            deadline = AttemptDeadline(
                None,
                notice=lambda message: emit(self.index, message, "post_running", self.profile_name))
            self.state = "RUNNING"
            self.last_error = ""
        emit(self.index,
             f"{self.profile_name} · đang xử lý liên tục từ bước hiện tại",
             "post_running", self.profile_name)

        def pause_if_requested() -> bool:
            if stop_after_step is None or not stop_after_step.is_set() or stop.is_set():
                return False
            with self._lock:
                self.state = "PAUSED"
                self.last_error = ""
            next_name = steps[self.next_step].name if self.next_step < len(steps) else "bước tiếp theo"
            emit(self.index, f"Đã dừng riêng {self.profile_name} · tiếp từ {next_name} khi bấm Tiếp tục",
                 "post_stopped", self.profile_name)
            return True

        if pause_if_requested():
            return
        if route is not None:
            try:
                target = route(self.next_step, job, deadline, stop)
                if target is not None:
                    if target < self.next_step or target >= len(steps):
                        raise ValueError("Invalid menu route")
                    if target > self.next_step:
                        with self._lock:
                            self.next_step = target
                        emit(self.index,
                             f"Menu dạng danh sách · đã xem Trang chủ, tiếp từ {steps[target].name}",
                             "post_running", self.profile_name)
            except Exception as exc:
                if pause_if_requested():
                    return
                reason = str(exc) if isinstance(exc, ToolError) else type(exc).__name__
                step_name = steps[self.next_step].name
                with self._lock:
                    self.state = "PAUSED"
                    self.last_error = f"{step_name}: {reason}"
                emit(self.index,
                     f"Dừng tại {step_name}: {reason} · sửa trên máy rồi bấm Tiếp tục",
                     "post_paused", self.profile_name)
                return
        if was_paused and reconcile is not None:
            if pause_if_requested():
                return
            try:
                resumed = reconcile(self.next_step, job, deadline, stop)
                if resumed is not None:
                    target, replacement = resumed
                    if target < 0 or target > self.next_step or len(replacement) != len(steps):
                        raise ValueError("Invalid resume step")
                    with self._lock:
                        self.next_step = target
                    steps = replacement
                    emit(self.index, f"Đọc lại màn hiện tại · tiếp từ {steps[target].name}",
                         "post_running", self.profile_name)
            except Exception as exc:
                if pause_if_requested():
                    return
                reason = str(exc) if isinstance(exc, ToolError) else type(exc).__name__
                step_name = steps[self.next_step].name
                with self._lock:
                    self.state = "PAUSED"
                    self.last_error = f"{step_name}: {reason}"
                emit(self.index,
                     f"Dừng tại {step_name}: {reason} · sửa trên máy rồi bấm Tiếp tục",
                     "post_paused", self.profile_name)
                return
        while self.next_step < len(steps):
            if pause_if_requested():
                return
            step = steps[self.next_step]
            recoveries = 0
            try:
                while True:
                    if stop.is_set():
                        raise ToolError("Đã dừng tự động hóa")
                    if step.within_attempt:
                        deadline.remaining()
                    action_deadline = deadline
                    try:
                        step.action(job, action_deadline, stop)
                        if step.within_attempt:
                            deadline.remaining()
                        break
                    except RecoverableStepError:
                        if pause_if_requested():
                            return
                        # b1–b9 actions re-read Android before acting and check
                        # the resulting state. SMS/OTP/Create are not replayed here.
                        retryable = bool(re.fullmatch(r'b[1-9][a-z]?', step.name.split(' ', 1)[0]))
                        if not retryable or stop.is_set():
                            raise
                        recoveries += 1
                        if recoveries == 1 or recoveries % 20 == 0:
                            emit(self.index,
                                 f"{step.name} · đang đợi màn hình rồi tự đọc lại ({recoveries})",
                                 "post_running", self.profile_name)
                        message = (f"{step.name} · màn hình chưa sẵn sàng, "
                                   f"đang đợi rồi tự đọc lại ({recoveries})")
                        if recoveries == 1 or recoveries % 20 == 0:
                            deadline.recovering(message)
                        stop.wait(min(2.0, 0.25 * recoveries))
            except Exception as exc:
                if pause_if_requested():
                    return
                reason = str(exc) if isinstance(exc, ToolError) else type(exc).__name__
                retryable = bool(re.fullmatch(r'b[1-9][a-z]?', step.name.split(' ', 1)[0]))
                if retryable and not stop.is_set():
                    recoveries += 1
                    if recoveries == 1 or recoveries % 20 == 0:
                        message = (f"{step.name} · lần xử lý chưa thành công ({reason}); "
                                   f"đang đợi rồi tự kiểm tra lại ({recoveries})")
                        emit(self.index, message, "post_running", self.profile_name)
                    stop.wait(min(2.0, 0.25 * recoveries))
                    continue
                with self._lock:
                    self.state = "PAUSED"
                    self.last_error = f"{step.name}: {reason}"
                emit(self.index,
                     f"Dừng tại {step.name}: {reason} · sửa trên máy rồi bấm Tiếp tục",
                     "post_paused", self.profile_name)
                return
            with self._lock:
                self.next_step += 1
            emit(self.index, f"Đã xong {step.name} · {self.profile_name}",
                 "post_running", self.profile_name)
        with self._lock:
            self.state = "DONE"
        emit(self.index, f"Đã xong các bước đã hướng dẫn · {self.profile_name}",
             "post_done", self.profile_name)


def type_characters(phone: CloudPhone, value: str, deadline: AttemptDeadline,
                    stop: threading.Event) -> None:
    """Send one Android text key event per character; never use clipboard/paste."""
    if any(ord(char) < 32 or ord(char) > 126 for char in value):
        raise ToolError("Trường có ký tự Android chưa gõ được; sửa trực tiếp trên máy")
    for position, char in enumerate(value, 1):
        if stop.is_set():
            raise ToolError("Đã dừng khi đang gõ")
        remaining = deadline.remaining()
        token = "%s" if char == " " else char
        command = f"input text {shlex.quote(token)}\n"
        result = cloud_adb(phone, "shell", input_text=command,
                           timeout=max(1, math.ceil(min(remaining, 10))),
                           check=False)
        if result.returncode:
            raise ToolError(f"Android không gõ được ký tự thứ {position}")
