"""Three loose, per-phone browse gestures before the existing registration flow."""
from __future__ import annotations

import re
import hashlib
import random
import secrets
import threading
import time

from .account_flow import (_bounds, _read_hierarchy, _text, _visible,
                           build_common_steps, screen)
from .cloud import CloudPhone, cloud_adb
from .core import ToolError
from .browse_view_scroll import scroll_view, wait_until
from .post_menu import (AttemptDeadline, PostMenuStep, RecoverableStepError,
                        RegistrationState)
from .runner import RunJob


SIZE = re.compile(r"(?:Physical|Override) size:\s*(\d+)x(\d+)")
COLUMNS = (0.16, 0.50, 0.84)
ROWS = (0.20, 0.42, 0.62, 0.79)
POINTS = tuple((x, y) for y in ROWS for x in COLUMNS)
EXTRA_VIEW_SECONDS = 30
PREFIX_TIMEOUT_SECONDS = 90


class Q7PrefixTimeout(ToolError):
    terminal = True


class PrefixDeadline(AttemptDeadline):
    def remaining(self) -> float:
        left = self.started + self.seconds - time.monotonic()
        if left <= 0:
            raise Q7PrefixTimeout("q7: hết 90 giây tìm mục con; giữ nguyên bước")
        return left
CHILD_LABELS = frozenset({
    "gift cards", "today's deals", "bank promotions", "clearance store",
    "promotions", "vouchers", "international store", "weekly new arrivals",
    "grocery", "health & personal care", "pets supplies", "dogs", "cats",
    "birds", "fish", "small animals", "fashion", "apparel", "shoes",
    "watches", "jewellery", "beauty", "luxury beauty", "home & kitchen",
    "lawn & garden", "arts, crafts & sewing", "diy, tools & automotive",
    "electronics", "mobile & accessories", "computers", "tablets", "tv",
    "music", "musical instruments", "video games", "dvd", "gaming store",
    "books", "steam store", "toys & games", "baby", "baby clothes",
    "girls' clothes", "boys' clothes",
})


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


def _tap_child(phone: CloudPhone, deadline: AttemptDeadline,
               stop: threading.Event) -> bool:
    """Tap a visible submenu row from the current Android hierarchy."""
    for read_attempt in range(3):
        if stop.is_set():
            raise ToolError("Đã dừng máy này")
        try:
            nodes = _read_hierarchy(phone, deadline, stop)
        except ToolError:
            nodes = []
        if screen(nodes) == "MENU":
            children = list({node["bounds"]: node for node in nodes
                             if _visible(node) and _text(node) in CHILD_LABELS}.values())
            if children:
                child = secrets.choice(children)
                x1, y1, x2, y2 = _bounds(child)
                cloud_adb(phone, "shell", "input", "tap", str((x1 + x2) // 2),
                          str((y1 + y2) // 2),
                          timeout=max(1, int(min(5, deadline.remaining()))))
                return True
        if read_attempt < 2 and stop.wait(deadline.allowance(0.4)):
            raise ToolError("Đã dừng máy này")
    return False


def build_random_steps(phone: CloudPhone, on_otp,
                       on_status=lambda _status: None,
                       registration: RegistrationState | None = None,
                       ) -> tuple[PostMenuStep, ...]:
    """Browse a random category and a visible child, adding 30 seconds total."""
    state = registration if registration is not None else RegistrationState()

    def browse(number: int):
        def action(job: RunJob, outer: AttemptDeadline,
                   stop: threading.Event) -> None:
            if stop.is_set():
                raise ToolError("Đã dừng máy này")
            if number in state.prefix_completed:
                return
            started = state.q7_prefix_started_at.setdefault(number, time.monotonic())
            deadline = PrefixDeadline(PREFIX_TIMEOUT_SECONDS, started=started,
                                      notice=outer.notice)
            try:
                run_browse(job, deadline, stop)
            except Q7PrefixTimeout:
                state.q7_prefix_started_at.pop(number, None)
                raise
            else:
                state.q7_prefix_started_at.pop(number, None)
        def run_browse(job: RunJob, deadline: PrefixDeadline,
                       stop: threading.Event) -> None:
            width, height = _size(phone, deadline)
            def finish_view(point):
                state.prefix_choices[number] = point
                until = state.q7_prefix_view_until.setdefault(
                    number, time.monotonic() + 1 + EXTRA_VIEW_SECONDS / 3)
                if number not in state.prefix_view_scrolled:
                    wait_until(until - (1 + EXTRA_VIEW_SECONDS / 3) / 2,
                               deadline, stop)
                    scroll_view(phone, width, height, deadline, stop,
                                number, cloud_adb)
                    state.prefix_view_scrolled.add(number)
                wait_until(until, deadline, stop)
                state.q7_prefix_view_until.pop(number, None)
                state.prefix_completed.add(number)

            if number in state.q7_prefix_view_until:
                finish_view(state.prefix_choices[number])
                return
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
                if stop.wait(0.5):
                    raise ToolError("Đã dừng máy này")
                try:
                    after_card = _read_hierarchy(phone, deadline, stop)
                except ToolError:
                    after_card = []
                if after_card and screen(after_card) != "MENU":
                    finish_view(point)
                    return
                try:
                    opened_child = _tap_child(phone, deadline, stop)
                except Q7PrefixTimeout:
                    raise
                except ToolError:
                    opened_child = False
                if not opened_child:
                    deadline.recovering(f"b{number}: chưa thấy mục con, thử thẻ khác")
                    continue
                deadline.recovering(f"b{number}: đã mở một mục con ngẫu nhiên")
                deadline.remaining()
                finish_view(point)
                return
            raise RecoverableStepError(
                f"b{number}: chưa mở được mục con; đang tự thử lại đúng máy")
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
