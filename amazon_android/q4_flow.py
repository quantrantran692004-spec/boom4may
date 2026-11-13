"""q4's Cart, Pets and Home and DIY visits, followed by shared b4–b11."""
from .account_flow import build_common_steps
from .cloud import CloudPhone
from .post_menu import PostMenuStep, RegistrationState
from .profile_navigation import cart_action, category_action


def build_q4_steps(phone: CloudPhone, on_otp, on_status=lambda _: None,
                   registration: RegistrationState | None = None) -> tuple[PostMenuStep, ...]:
    return (PostMenuStep("b1 Giỏ hàng", cart_action(phone)),
            PostMenuStep("b2 Pets", category_action(phone, "Pets")),
            PostMenuStep("b3 Home and DIY", category_action(phone, "Home and DIY")),
            ) + build_common_steps(phone, on_otp, on_status, registration)
