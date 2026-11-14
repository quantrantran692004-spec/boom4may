"""Three loose, per-phone browse gestures before the existing registration flow."""
from __future__ import annotations

import re
import hashlib
import random
import secrets
import threading

from .account_flow import build_common_steps
from .cloud import CloudPhone, cloud_adb
from .core import ToolError
from .post_menu import (AttemptDeadline, PostMenuStep, RecoverableStepError,
                        RegistrationState)
from .runner import RunJob


SIZE = re.compile(r"(?:Physical|Override) size:\s*(\d+)x(\d+)")
COLUMNS = (0.16, 0.50, 0.84)
ROWS = (0.20, 0.42, 0.62, 0.79)
POINTS = tuple((x, y) for y in ROWS for x in COLUMNS)


def _first_point(job: RunJob) -> tuple[float, float]:
    """A new batch shuffles 12 positions, giving every phone a unique b1."""
    seed = int.from_bytes(hashlib.sha256(job.batch_id.encode("utf-8")).digest())
    positions = list(POINTS)
    random.Random(seed).shuffle(positions)
    return positions[job.index]


def _size(phone: CloudPhone, deadline: AttemptDeadline) -> tuple[int, int]:
    output = cloud_adb(phone, "shell", "wm", "size",
                       timeout=max(1, int(min(5, deadline.remaining()))))
    sizes = SIZE.findall(output.stdout)
    if not sizes:
        raise RecoverableStepError("Chưa đọc được kích thước màn hình máy này")
    width, height = map(int, sizes[-1])
    if width < 100 or height < 200:
        raise RecoverableStepError("Kích thước màn hình máy này chưa hợp lệ")
    return width, height


def _menu(phone: CloudPhone, width: int, height: int,
          deadline: AttemptDeadline) -> None:
    # One tap at the live device's bottom Browse tab; b4 still verifies UI.
    try:
        cloud_adb(phone, "shell", "input", "tap", str(round(width * 0.86)),
                  str(round(height * 0.93)),
                  timeout=max(1, int(min(5, deadline.remaining()))))
    except ToolError:
        pass  # A browse tap can be delivered despite an ADB response error.


def build_random_steps(phone: CloudPhone, on_otp,
                       on_status=lambda _status: None,
                       registration: RegistrationState | None = None,
                       ) -> tuple[PostMenuStep, ...]:
    """Try up to four random category positions per step without OCR."""
    state = registration if registration is not None else RegistrationState()

    def browse(number: int):
        def action(job: RunJob, deadline: AttemptDeadline,
                   stop: threading.Event) -> None:
            if stop.is_set():
                raise ToolError("Đã dừng máy này")
            width, height = _size(phone, deadline)
            candidates = list(POINTS)
            used = set(state.prefix_choices.values())
            for attempt in range(4):
                if stop.is_set():
                    raise ToolError("Đã dừng máy này")
                if number > 1 or attempt:
                    _menu(phone, width, height, deadline)
                if attempt >= 2:
                    # Reveal another row if the first two taps were not sent.
                    try:
                        cloud_adb(phone, "shell", "input", "swipe",
                                  str(width // 2), str(round(height * 0.73)),
                                  str(width // 2), str(round(height * 0.35)), "280",
                                  timeout=max(1, int(min(5, deadline.remaining()))))
                    except ToolError:
                        pass
                available = [point for point in candidates if point not in used]
                preferred = (_first_point(job) if number == 1 and attempt == 0
                             else None)
                point = (preferred if preferred in available else
                         secrets.choice(available or candidates))
                candidates.remove(point)
                x, y = point
                try:
                    cloud_adb(phone, "shell", "input", "tap",
                              str(round(width * x)), str(round(height * y)),
                              timeout=max(1, int(min(5, deadline.remaining()))))
                except ToolError:
                    deadline.recovering(f"b{number}: cú bấm chưa xác nhận, thử vị trí khác")
                    continue
                state.prefix_choices[number] = point
                state.prefix_completed.add(number)
                deadline.recovering(f"b{number}: đã bấm vị trí danh mục ngẫu nhiên")
                if stop.wait(1):
                    raise ToolError("Đã dừng máy này")
                return
            raise RecoverableStepError(
                f"b{number}: chưa gửi được cú bấm; đang tự thử lại đúng máy")
        return action

    common = build_common_steps(phone, on_otp, on_status, state)

    def sign_in(job: RunJob, deadline: AttemptDeadline,
                stop: threading.Event) -> None:
        if not {1, 2, 3} <= state.prefix_completed:
            raise RecoverableStepError("Chưa đủ ba lượt bấm ngẫu nhiên")
        width, height = _size(phone, deadline)
        _menu(phone, width, height, deadline)
        common[0].action(job, deadline, stop)

    return (tuple(PostMenuStep(f"b{number} ngẫu nhiên", browse(number))
                  for number in (1, 2, 3)) +
            (PostMenuStep(common[0].name, sign_in,
                          within_attempt=common[0].within_attempt),) + common[1:])
