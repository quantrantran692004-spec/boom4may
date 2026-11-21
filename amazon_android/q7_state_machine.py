"""Isolated q7 pilot: verify Android state around the existing shared steps.

This module does not create accounts or choose new business actions. It wraps
the existing b4–b11 actions and refuses an unobserved transition.
"""
from __future__ import annotations

import re
import threading
import time
from dataclasses import dataclass, field

from .account_flow import (FINAL_SMS_STEP, POST_SMS_WAIT_SECONDS, OTP_FIELD, PHONE_FIELD, _check_summary, _field, _has, home_visible,
                           _read_nodes, _visible, screen)
from .cloud import CloudPhone, cloud_adb
from .core import AMAZON_PACKAGE, ToolError
from .post_menu import (AttemptDeadline, PostMenuStep, RecoverableStepError,
                        RegistrationState)
from .q7_random_prefix import _menu, _size, build_random_steps
from .random_prefix import build_post_auth_steps, _tail_candidates
from .runner import RunJob


class StateMachineStop(ToolError):
    """An unsafe or unknown state must pause q7, never replay its action."""

    terminal = True

    def __init__(self, message: str, *, kind: str = "unverified") -> None:
        super().__init__(message)
        self.kind = kind


class StateMachineTimeout(StateMachineStop):
    def __init__(self, message: str) -> None:
        super().__init__(message, kind="timeout")


class UnknownStateHandler:
    @staticmethod
    def stop(observed: str = "UNKNOWN") -> None:
        raise StateMachineStop(
            f"q7: màn hình {observed} không xác định hoặc không được hướng dẫn; "
            "cần kiểm tra trực tiếp", kind="unknown_screen")


@dataclass(frozen=True)
class StateSpec:
    name: str
    before: frozenset[str]
    after: frozenset[str]
    seconds: int
    retry_action: int = 0


LATER = frozenset({"NEW_ACCOUNT", "CREATE_FORM", "WHATSAPP", "SMS"})
STAGE = {"MENU": 0, "IDENTIFIER": 1, "COUNTRY": 1,
         "NEW_ACCOUNT": 2, "CREATE_FORM": 3, "WHATSAPP": 4, "SMS": 5}
JUMP_TARGET = {"b4 Sign In": 1, "b4a chạm ô SĐT": 1,
               "b5 nhập SĐT": 1, "b6 chọn US +1": 1,
               "b7 Continue": 2, "b8 Proceed to create an account": 3,
               "b9 nhập tên": 4, "b10 Send code by SMS": 5}


def _past_known_step(spec: StateSpec, observed: str) -> bool:
    """Accept only a recognized later registration screen for this step."""
    return (spec.name in JUMP_TARGET and observed in LATER and
            STAGE[observed] > JUMP_TARGET[spec.name])


def _already_reached_result(spec: StateSpec, observed: str) -> bool:
    return (_past_known_step(spec, observed) or
            (observed in spec.after and observed not in spec.before))


def _browse_ready_after_sms(nodes: list[dict[str, str]]) -> bool:
    kind = screen(nodes)
    if kind == "MENU":
        return True
    if kind != "UNKNOWN":
        return False
    browse = {node.get("bounds", "") for node in nodes
              if _visible(node) and node.get("bounds") and
              node.get("content-desc", "").casefold().startswith("browse menu tab")}
    return (len(browse) == 1 or home_visible(nodes) or
            bool(_tail_candidates(nodes, RegistrationState())))


SPECS = (
    StateSpec("b4 Sign In", frozenset({"MENU", "IDENTIFIER"}),
              frozenset({"IDENTIFIER"}), 45, 1),
    StateSpec("b4a chạm ô SĐT", frozenset({"IDENTIFIER"}),
              frozenset({"IDENTIFIER"}), 45, 1),
    StateSpec("b5 nhập SĐT", frozenset({"IDENTIFIER"}),
              frozenset({"IDENTIFIER"}), 60, 1),
    StateSpec("b6 chọn US +1", frozenset({"IDENTIFIER", "COUNTRY"}),
              frozenset({"IDENTIFIER"}), 120, 1),
    StateSpec("b7 Continue", frozenset({"IDENTIFIER"}),
              frozenset({"NEW_ACCOUNT", "CREATE_FORM"}), 60),
    StateSpec("b8 Proceed to create an account", frozenset({"NEW_ACCOUNT", "CREATE_FORM"}),
              frozenset({"CREATE_FORM"}), 60),
    StateSpec("b9 nhập tên", frozenset({"CREATE_FORM"}),
              frozenset({"WHATSAPP", "SMS"}), 60),
    StateSpec("b10 Send code by SMS", frozenset({"WHATSAPP", "SMS"}),
              frozenset({"SMS"}), 60),
    StateSpec("b11a chạm ô OTP", frozenset({"SMS"}),
              frozenset({"SMS"}), 45, 1),
    StateSpec("b11 nhập OTP", frozenset({"SMS"}),
              frozenset({"SMS"}), 300),
    StateSpec(FINAL_SMS_STEP, frozenset({"SMS"}),
              frozenset(), 90),
)


@dataclass(frozen=True)
class StateDeadline(AttemptDeadline):
    pending_screens: frozenset[str] = field(default_factory=frozenset)
    strict_expected = True

    def remaining(self) -> float:
        left = self.started + self.seconds - time.monotonic()
        if left <= 0:
            raise StateMachineTimeout("q7: hết thời gian chờ trạng thái; giữ nguyên bước")
        return left


class StateDetector:
    def __init__(self, phone: CloudPhone):
        self.phone = phone

    def observe(self, deadline: StateDeadline, stop: threading.Event,
                *, unknown_wait: float = 8) -> tuple[str, list[dict[str, str]]]:
        until = time.monotonic() + unknown_wait
        while True:
            if stop.is_set():
                raise StateMachineStop("q7: đã dừng", kind="user_stop")
            try:
                nodes = _read_nodes(self.phone, deadline, stop)
            except ToolError as exc:
                if stop.is_set():
                    raise StateMachineStop("q7: đã dừng", kind="user_stop") from exc
                try:
                    connection = cloud_adb(self.phone, "get-state", timeout=4,
                                           check=False)
                except ToolError as probe_error:
                    raise StateMachineStop(
                        "q7: mất kết nối ADB khi đọc màn hình",
                        kind="connection_lost") from probe_error
                if connection.returncode or connection.stdout.strip() != "device":
                    raise StateMachineStop(
                        "q7: mất kết nối ADB khi đọc màn hình",
                        kind="connection_lost") from exc
                if isinstance(exc, StateMachineTimeout):
                    raise
                raise StateMachineStop(
                    "q7: ADB còn kết nối nhưng XML/OCR chưa đọc được màn hình",
                    kind="observation_failed") from exc
            kind = screen(nodes)
            if kind != "UNKNOWN":
                return kind, nodes
            if time.monotonic() >= until:
                UnknownStateHandler.stop()
            stop.wait(min(0.25, deadline.remaining()))


class ActionValidator:
    @staticmethod
    def check(spec: StateSpec, observed: str, nodes: list[dict[str, str]],
              job: RunJob) -> None:
        if job.index != 6:
            raise StateMachineStop("State Machine thử nghiệm chỉ dành cho q7",
                                   kind="wrong_worker")
        if observed not in spec.before:
            raise StateMachineStop(
                f"q7 {spec.name}: màn {observed} không cho phép hành động này",
                kind="unexpected_screen")
        if observed in LATER:
            _check_summary(nodes, job)


class TransitionManager:
    @staticmethod
    def allows(spec: StateSpec, observed: str) -> bool:
        return observed in spec.after or _past_known_step(spec, observed)


class ResultVerifier:
    def __init__(self, detector: StateDetector):
        self.detector = detector

    def verify(self, spec: StateSpec, job: RunJob, deadline: StateDeadline,
               stop: threading.Event, *,
               registration: RegistrationState | None = None) -> None:
        try:
            self._verify(spec, job, deadline, stop, registration=registration)
        except StateMachineTimeout as exc:
            raise StateMachineStop(
                f"q7 {spec.name}: đã xử lý nhưng chưa xác minh được kết quả; "
                "giữ nguyên bước, không bấm lặp", kind="unverified_action") from exc

    def _verify(self, spec: StateSpec, job: RunJob, deadline: StateDeadline,
                stop: threading.Event, *,
                registration: RegistrationState | None = None) -> None:
        # Both SMS branches can land on Home. A visible Browse tab lets b12
        # open the menu; it does not prove account creation or sign-in.
        if not spec.after:
            until = time.monotonic() + min(POST_SMS_WAIT_SECONDS, deadline.remaining())
            while True:
                if stop.is_set():
                    raise StateMachineStop("q7: đã dừng", kind="user_stop")
                nodes = _read_nodes(self.detector.phone, deadline, stop)
                observed = screen(nodes)
                if _browse_ready_after_sms(nodes):
                    return  # b12 will tap Browse and verify its menu.
                if observed not in {"UNKNOWN", "SMS"} or time.monotonic() >= until:
                    raise StateMachineStop(
                        f"q7: sau xác minh SMS thấy {observed} nhưng chưa có "
                        "dấu hiệu menu Browse", kind="result_unknown")
                stop.wait(min(0.25, deadline.remaining()))
        while True:
            observed, nodes = self.detector.observe(deadline, stop)
            if TransitionManager.allows(spec, observed):
                if observed in LATER:
                    _check_summary(nodes, job)
                if spec.name == "b5 nhập SĐT" and observed == "IDENTIFIER":
                    if job.account is None or _field(nodes, PHONE_FIELD).get("text") != job.account.phone:
                        raise StateMachineStop("q7: chưa xác nhận đúng SĐT sau b5",
                                               kind="result_mismatch")
                if spec.name == "b6 chọn US +1" and observed == "IDENTIFIER":
                    if not _has(nodes, "US +1"):
                        raise StateMachineStop("q7: chưa xác nhận US +1 sau b6",
                                               kind="result_mismatch")
                if spec.name == "b11 nhập OTP":
                    observed_code = _field(nodes, OTP_FIELD).get("text", "")
                    visual_login_confirmed = bool(
                        registration and registration.login_jump_seen and
                        not registration.create_flow_seen and
                        registration.login_otp_confirmed and registration.code)
                    if ((visual_login_confirmed and
                         re.fullmatch(r"[0-9]{6}", observed_code) and
                         observed_code != registration.code) or
                            (not visual_login_confirmed and
                             not re.fullmatch(r"[0-9]{6}", observed_code))):
                        raise StateMachineStop("q7: chưa xác nhận đủ sáu số OTP",
                                               kind="result_mismatch")
                return
            if observed not in spec.before:
                UnknownStateHandler.stop(observed)
            # A known but earlier screen can be a slow transition. Observe it
            # again without resending the action until this state's deadline.
            stop.wait(min(0.25, deadline.remaining()))


class RecoveryHandler:
    @staticmethod
    def may_retry(spec: StateSpec, error: Exception, attempts: int) -> bool:
        return (attempts <= spec.retry_action and
                isinstance(error, RecoverableStepError))

    @staticmethod
    def classify_action_error(phone: CloudPhone, error: ToolError) -> str:
        if isinstance(error, RecoverableStepError):
            return "locator_or_focus"
        try:
            connection = cloud_adb(phone, "get-state", timeout=4, check=False)
        except ToolError:
            return "connection_lost"
        if connection.returncode or connection.stdout.strip() != "device":
            return "connection_lost"
        return "action_unverified"


def build_q7_pilot_steps(phone: CloudPhone, on_otp, on_status=lambda _status: None,
                         registration: RegistrationState | None = None,
                         ) -> tuple[PostMenuStep, ...]:
    """Keep q7's random prefix and wrap only its shared registration states."""
    state = registration if registration is not None else RegistrationState()
    original = build_random_steps(phone, on_otp, on_status, state)
    common = original[3:]
    if tuple(step.name for step in common) != tuple(spec.name for spec in SPECS):
        raise ValueError("q7 pilot no longer matches shared step inventory")
    detector = StateDetector(phone)
    verifier = ResultVerifier(detector)
    wrapped = []
    for step, spec in zip(common, SPECS):
        def run(job: RunJob, outer: AttemptDeadline, stop: threading.Event,
                *, action=step.action, rule=spec) -> None:
            deadline = StateDeadline(rule.seconds, notice=outer.notice,
                                     pending_screens=rule.before)
            try:
                attempts = 0
                while True:
                    if (rule.name == FINAL_SMS_STEP and
                            (state.create_pressed or state.login_verify_pressed)):
                        preview = _read_nodes(phone, deadline, stop)
                        if _browse_ready_after_sms(preview):
                            return  # Resume after a delivered Create/Verify tap.
                    # A random child can open another page. Returning to the
                    # known Browse tab is the only pre-b4 recovery action.
                    if rule.name == "b4 Sign In":
                        focus = cloud_adb(phone, "shell", "dumpsys", "window", "windows",
                                          timeout=max(1, int(min(4, deadline.remaining()))),
                                          check=False)
                        if not any("mCurrentFocus=" in line and AMAZON_PACKAGE in line
                                   for line in focus.stdout.splitlines()):
                            raise StateMachineStop(
                                "q7: chưa xác nhận Amazon ở phía trước để về menu")
                        try:
                            preview = _read_nodes(phone, deadline, stop)
                        except ToolError:
                            preview = []
                        if screen(preview) in LATER | {"IDENTIFIER"}:
                            observed, _nodes = screen(preview), preview
                        else:
                            width, height = _size(phone, deadline)
                            _menu(phone, width, height, deadline)
                            observed, _nodes = detector.observe(deadline, stop)
                    else:
                        observed, _nodes = detector.observe(deadline, stop)
                    if observed in {"NEW_ACCOUNT", "CREATE_FORM"}:
                        state.create_flow_seen = True
                    if _already_reached_result(rule, observed):
                        if job.index != 6:
                            raise StateMachineStop("State Machine thử nghiệm chỉ dành cho q7",
                                                   kind="wrong_worker")
                        _check_summary(_nodes, job)
                        return
                    ActionValidator.check(rule, observed, _nodes, job)
                    try:
                        action(job, deadline, stop)
                        break
                    except Exception as exc:
                        attempts += 1
                        if not RecoveryHandler.may_retry(rule, exc, attempts):
                            raise
                        stop.wait(min(0.5, deadline.remaining()))
                verifier.verify(rule, job, deadline, stop, registration=state)
            except StateMachineStop:
                raise
            except ToolError as exc:
                raise StateMachineStop(f"q7 {rule.name}: {exc}",
                                       kind=RecoveryHandler.classify_action_error(
                                           phone, exc)) from exc
            except Exception as exc:
                raise StateMachineStop(
                    f"q7 {rule.name}: lỗi xử lý {type(exc).__name__}; "
                    "giữ nguyên bước để kiểm tra", kind="unexpected_error") from exc
        wrapped.append(PostMenuStep(step.name, run, within_attempt=step.within_attempt))
    return original[:3] + tuple(wrapped) + build_post_auth_steps(phone, state)
