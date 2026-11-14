"""q5's three category taps, followed by the shared b4–b11 flow."""
from __future__ import annotations

from .account_flow import build_common_steps
from .cloud import CloudPhone
from .post_menu import PostMenuStep, RegistrationState
from .profile_navigation import category_action


def build_q5_steps(phone: CloudPhone, on_otp, on_status=lambda _: None,
                   registration: RegistrationState | None = None) -> tuple[PostMenuStep, ...]:
    """Tap each category; return to the menu only if a tap opened another page."""
    return tuple(PostMenuStep(f"b{index} {label}", category_action(phone, label))
                 for index, label in enumerate(("Toys, Kids and Baby",
                                                "Office & Professional",
                                                "Sports & Outdoors"), 1)) + build_common_steps(
                                                    phone, on_otp, on_status, registration)
