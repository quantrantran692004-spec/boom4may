"""Three best-effort, live-menu taps before the shared registration steps."""
from __future__ import annotations

import secrets
import threading
import time

from .account_flow import (_at_or_after, _ensure_menu, _read_nodes, _tap_for_transition,
                           _text, _visible, build_common_steps)
from .cloud import CloudPhone
from .core import ToolError
from .post_menu import AttemptDeadline, PostMenuStep, RegistrationState
from .runner import RunJob


KNOWN_MENU_ACTIONS = {
    "gifting", "pets", "fashion and beauty", "groceries and drinks",
    "home and diy", "books and reading", "toys, kids and baby",
    "office & professional", "sports & outdoors", "devices and electronics",
    "books", "electronics", "home services", "your stuff",
}
EXCLUDED = {
    "shop by category", "sign in", "customer service", "see all",
    "browse menu tab", "continue", "create account", "your account",
}


class _PrefixDeadline(AttemptDeadline):
    """Keep optional browsing taps from waiting forever on a broken UI read."""

    def remaining(self) -> float:
        if self.seconds is None:
            return super().remaining()
        left = self.started + self.seconds - time.monotonic()
        if left <= 0:
            raise ToolError("Đã hết thời gian đọc menu ngẫu nhiên")
        return left


def _menu_targets(nodes: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    """Use live, visible menu controls; never choose registration controls."""
    targets: dict[str, dict[str, str]] = {}
    for node in nodes:
        if not _visible(node):
            continue
        label = _text(node)
        if (not label or label in EXCLUDED or
                any(term in label for term in (
                    "sign in", "sign out", "create", "continue", "account",
                    "password", "payment", "security code", "otp",
                    "browse menu", "customer service"))):
            continue
        nav = label.startswith(("home tab", "cart tab"))
        if not (nav or label in KNOWN_MENU_ACTIONS):
            continue
        # The Android tree can repeat one label on its card and its text.
        if label not in targets or (node.get("clickable") == "true" and
                                    targets[label].get("clickable") != "true"):
            targets[label] = node
    return targets


def build_random_steps(phone: CloudPhone, on_otp,
                       on_status=lambda _status: None,
                       registration: RegistrationState | None = None,
                       ) -> tuple[PostMenuStep, ...]:
    """Draw each prefix tap from the current menu, once per phone and batch."""
    state = registration if registration is not None else RegistrationState()

    def random_tap(number: int):
        def action(job: RunJob, deadline: AttemptDeadline,
                   stop: threading.Event) -> None:
            if stop.is_set():
                raise ToolError("Đã dừng máy này")
            prefix_deadline = _PrefixDeadline(15, visual_until=deadline.visual_until,
                                              notice=deadline.notice)
            try:
                nodes = _read_nodes(phone, prefix_deadline, stop)
                if _at_or_after(nodes, "IDENTIFIER"):
                    return
                nodes = _ensure_menu(phone, prefix_deadline, stop)
            except ToolError:
                if stop.is_set():
                    raise
                deadline.recovering(f"b{number}: chưa về được menu, chuyển tiếp để b4 tự kiểm tra")
                return
            targets = _menu_targets(nodes)
            if not targets:
                deadline.recovering(f"b{number}: menu chưa có mục bấm rõ, chuyển tiếp")
                return
            chosen = state.prefix_choices.get(number)
            if chosen not in targets:
                unused = [label for label in targets if label not in state.prefix_choices.values()]
                chosen = secrets.choice(unused or list(targets))
                state.prefix_choices[number] = chosen
            deadline.recovering(f"b{number}: đã chọn ngẫu nhiên {chosen}")
            _tap_for_transition(phone, targets[chosen], deadline)
            if stop.wait(deadline.allowance(0.3)):
                raise ToolError("Đã dừng máy này")
        return action

    return tuple(PostMenuStep(f"b{number} ngẫu nhiên", random_tap(number))
                 for number in (1, 2, 3)) + build_common_steps(
                     phone, on_otp, on_status, state)
