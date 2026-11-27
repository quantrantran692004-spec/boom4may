"""Independent Reg US flow, held at b1 until its actions are specified."""
from __future__ import annotations

from .core import ToolError
from .post_menu import PostMenuStep


class RegUsAwaitingInstruction(ToolError):
    terminal = True


def _await_b1(job, deadline, stop) -> None:
    """Pause without touching the phone or advancing beyond b1."""
    raise RegUsAwaitingInstruction(
        "Reg US chưa có hướng dẫn b1; giữ nguyên màn để người dùng chỉ bước tiếp theo")


def build_reg_us_steps(phone, on_otp, on_otp_status=None, registration=None) -> tuple[PostMenuStep, ...]:
    """Bind a separate post-menu flow without reusing Amazon's b1 onward."""
    return (PostMenuStep("b1 Reg US", _await_b1),)
