"""q3's category visits, followed by shared b4–b11."""
from .account_flow import build_common_steps
from .cloud import CloudPhone
from .post_menu import PostMenuStep, RegistrationState
from .profile_navigation import category_action


def build_q3_steps(phone: CloudPhone, on_otp, on_status=lambda _: None,
                   registration: RegistrationState | None = None) -> tuple[PostMenuStep, ...]:
    return tuple(PostMenuStep(f"b{index} {label}", category_action(phone, label))
                 for index, label in enumerate(("Groceries and Drinks", "Home and DIY",
                                                 "Books and Reading"), 1)) + build_common_steps(
                     phone, on_otp, on_status, registration)
