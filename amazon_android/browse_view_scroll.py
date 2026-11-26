"""Moderate browsing swipe shared by random category visits."""
from __future__ import annotations

import math
import time

from .core import ToolError


def wait_until(when, deadline, stop):
    """Keep the browse pause interruptible and preserve its original end time."""
    remaining = max(0, when - time.monotonic())
    if stop.is_set() or (remaining and stop.wait(deadline.allowance(remaining))):
        raise ToolError('Đã dừng máy này')


def scroll_view(phone, width, height, deadline, stop, number, adb):
    """One upward finger swipe to reveal products farther down the page."""
    if stop.is_set():
        raise ToolError('Đã dừng máy này')
    deadline.recovering(f'b{number}: lướt xem trang một lượt')
    x = width // 2
    adb(phone, 'shell', 'input', 'swipe', str(x), str(round(height * .68)),
        str(x), str(round(height * .43)), '450',
        timeout=max(1, math.ceil(min(5, deadline.remaining()))))
