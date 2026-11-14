"""q6 Home, Cart, menu and Electronics card before shared b4–b11."""
from __future__ import annotations

import threading

from .account_flow import (_at_or_after, _ensure_menu, _find_scrolling,
                           _read_nodes, _tap_for_transition, build_common_steps,
                           menu_layout, visit_home)
from .cloud import CloudPhone
from .post_menu import AttemptDeadline, PostMenuStep, RegistrationState
from .profile_navigation import cart_action
from .runner import RunJob


def build_q6_steps(phone: CloudPhone, on_otp, on_status=lambda _: None,
                   registration: RegistrationState | None = None) -> tuple[PostMenuStep, ...]:
    """Keep b3a within q6's third step so shared b4 stays at index three."""
    def home(job: RunJob, deadline: AttemptDeadline, stop: threading.Event) -> None:
        if _at_or_after(_read_nodes(phone, deadline, stop), "IDENTIFIER"):
            return
        visit_home(phone, deadline, stop, view_seconds=2)

    cart = cart_action(phone)

    def view_cart(job: RunJob, deadline: AttemptDeadline,
                  stop: threading.Event) -> None:
        if _at_or_after(_read_nodes(phone, deadline, stop), "IDENTIFIER"):
            return
        cart(job, deadline, stop)
        stop.wait(deadline.allowance(2))

    def menu_and_card(job: RunJob, deadline: AttemptDeadline,
                      stop: threading.Event) -> None:
        if _at_or_after(_read_nodes(phone, deadline, stop), "IDENTIFIER"):
            return
        nodes = _ensure_menu(phone, deadline, stop)
        label = ("Electronics" if menu_layout(nodes) == "LIST"
                 else "Devices and Electronics")
        _tap_for_transition(phone, _find_scrolling(phone, label, deadline, stop), deadline)
        stop.wait(0.4)

    return (PostMenuStep("b1 Trang chủ 2 giây", home),
            PostMenuStep("b2 Giỏ hàng 2 giây", view_cart),
            PostMenuStep("b3 Menu · b3a Electronics", menu_and_card),
            ) + build_common_steps(phone, on_otp, on_status, registration)
