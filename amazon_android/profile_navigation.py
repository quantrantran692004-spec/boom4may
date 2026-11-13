"""Live navigation primitives for the newly documented q3/q4 prefix steps."""
from __future__ import annotations

import threading
import time

from .account_flow import (_at_or_after, _ensure_menu, _find_scrolling, _has,
                           _read_nodes, _tap_for_transition, _unique, _visible)
from .cloud import CloudPhone
from .core import ToolError
from .post_menu import AttemptDeadline
from .runner import RunJob


def category_action(phone: CloudPhone, label: str):
    def action(job: RunJob, deadline: AttemptDeadline, stop: threading.Event) -> None:
        nodes = _read_nodes(phone, deadline, stop)
        if _at_or_after(nodes, "IDENTIFIER"):
            return
        _ensure_menu(phone, deadline, stop)
        _tap_for_transition(phone, _find_scrolling(phone, label, deadline, stop), deadline)
        if stop.wait(deadline.allowance(0.4)):
            raise ToolError("Đã dừng máy này")
    return action


def cart_visible(nodes: list[dict[str, str]]) -> bool:
    return (any(node.get("content-desc", "").casefold().startswith("cart tab")
                and node.get("selected") == "true" for node in nodes)
            or _has(nodes, "Your Amazon Cart is empty")
            or (_has(nodes, "Your Amazon Cart is") and _has(nodes, "empty"))
            or (_has(nodes, "Cart") and _has(nodes, "Continue shopping")))


def cart_action(phone: CloudPhone):
    def action(job: RunJob, deadline: AttemptDeadline, stop: threading.Event) -> None:
        nodes = _read_nodes(phone, deadline, stop)
        if _at_or_after(nodes, "IDENTIFIER") or cart_visible(nodes):
            return
        # Locate the actual navigation tab, never the cart graphic in a page.
        for attempt in range(3):
            tabs = [node for node in nodes if _visible(node) and
                    node.get("content-desc", "").casefold().startswith("cart tab")]
            if tabs:
                target = _unique(tabs, "Cart Tab", starts=True)
                break
            if attempt == 2:
                raise ToolError("q4 chưa xác định được tab giỏ hàng trong giao diện Android")
            if stop.wait(deadline.allowance(0.15)):
                raise ToolError("Đã dừng máy này")
            nodes = _read_nodes(phone, deadline, stop)
        _tap_for_transition(phone, target, deadline)
        until = time.monotonic() + deadline.allowance(8)
        while time.monotonic() < until:
            if stop.is_set():
                raise ToolError("Đã dừng máy này")
            nodes = _read_nodes(phone, deadline, stop)
            if cart_visible(nodes) or _at_or_after(nodes, "IDENTIFIER"):
                return
            stop.wait(deadline.allowance(0.15))
        raise ToolError("q4 chưa xác nhận được màn giỏ hàng sau khi chạm tab")
    return action
