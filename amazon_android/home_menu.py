"""Deterministic Amazon navigation through the home browse menu."""
from __future__ import annotations

import re
import time
import math
import threading
from subprocess import TimeoutExpired
import xml.etree.ElementTree as ET

from .cloud import CloudPhone, cloud_adb, open_amazon
from .core import AMAZON_PACKAGE, ToolError
from .swarmote_desktop import install_amazon, open_adb_shell, show_apps, start_profile


BOUNDS = re.compile(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]")


class MenuReadUnavailable(ToolError):
    """A failed observation; retry it without replaying navigation actions."""


def _menu_evidence(nodes):
    labels = {node.get('text', '').strip().rstrip('.').casefold() for node in nodes
              if node.get('package') == AMAZON_PACKAGE}
    return ('shop by category' in labels or len(labels & {
        'gifting', 'pets', 'fashion and beauty', 'groceries and drinks',
        'home and diy', 'books and reading', 'health and personal care',
        'devices and electronics', 'toys, kids and baby'}) >= 3 or
        {'sign in', 'customer service', 'books', 'electronics'} <= labels)


def _confirm_menu_fallback(phone, seconds, stop):
    """Use the shared native/visual Android reader when menu XML omits labels."""
    from .account_flow import _read_nodes
    from .post_menu import AttemptDeadline
    try:
        return _menu_evidence(_read_nodes(phone, AttemptDeadline(max(1, min(12, seconds))),
                                          stop if stop is not None else threading.Event()))
    except ToolError:
        if stop is not None and stop.is_set():
            raise
        return False


def _nodes(phone: CloudPhone, *, stop=None, until=None) -> list[dict[str, str]]:
    def budget():
        if stop is not None and stop.is_set():
            raise ToolError('Đã dừng chuẩn bị máy')
        if until is not None and time.monotonic() >= until:
            raise MenuReadUnavailable('Hết thời gian đọc menu')
        return max(1, math.ceil(min(15, until - time.monotonic()))) if until is not None else 15

    def pause():
        if stop is None:
            time.sleep(0.3)
        else:
            stop.wait(0.3)
    path = "/sdcard/amazon_tool_menu.xml"
    last_error = "Android chưa trả cây giao diện hợp lệ"
    for attempt in range(3):
        try:
            dumped = cloud_adb(phone, "shell", "uiautomator", "dump", path,
                               timeout=budget(), check=False)
            # Some Windows ADB invocations report an interrupted exit code after
            # Android has already written the dump. Accept only an explicit
            # success message for that case, then validate the XML itself.
            if dumped.returncode and f"dumped to: {path}" not in dumped.stdout:
                last_error = f"ADB dump trả mã {dumped.returncode}"
                if attempt < 2:
                    pause()
                continue
            result = cloud_adb(phone, "shell", "cat", path, timeout=budget(), check=False)
            nodes = [node.attrib for node in ET.fromstring(result.stdout).iter("node")]
            if not any(node.get("package") == AMAZON_PACKAGE for node in nodes):
                last_error = "Màn hình trước chưa phải Amazon Shopping"
                if attempt < 2:
                    time.sleep(0.3)
                continue
            return nodes
        except (ToolError, ET.ParseError) as exc:
            if stop is not None and stop.is_set():
                raise ToolError('Đã dừng chuẩn bị máy') from exc
            last_error = str(exc) if isinstance(exc, ToolError) else "XML chưa hợp lệ"
        if attempt < 2:
            pause()
    raise MenuReadUnavailable(f"Không đọc được giao diện Amazon sau 3 lần: {last_error}")


def _tap(phone: CloudPhone, node: dict[str, str]) -> None:
    match = BOUNDS.fullmatch(node.get("bounds", ""))
    if not match:
        raise ToolError("Không xác định được vị trí nút Amazon")
    x1, y1, x2, y2 = map(int, match.groups())
    cloud_adb(phone, "shell", "input", "tap",
              str((x1 + x2) // 2), str((y1 + y2) // 2))


def open_home_menu(phone: CloudPhone, timeout: int = 45, *, stop=None) -> dict:
    """Reach Amazon's Browse menu, with no account data entered."""
    deadline = time.monotonic() + timeout
    backed_out = False
    skip_back_sent = False
    tapped_menu = False
    menu_taps = 0
    unselected_reads = 0
    next_fallback = 0.0
    while time.monotonic() < deadline:
        if stop is not None and stop.is_set():
            raise ToolError('Đã dừng chuẩn bị máy')
        try:
            nodes = _nodes(phone, stop=stop, until=deadline)
        except MenuReadUnavailable:
            time.sleep(min(0.3, max(0, deadline - time.monotonic())))
            continue
        if stop is not None and stop.is_set():
            raise ToolError('Đã dừng chuẩn bị máy')
        labels = {node.get("text", "") for node in nodes}
        if ("Authentication required" in labels or
                "Verify mobile number" in labels or
                "Enter security code" in labels):
            raise ToolError("Amazon đang ở bước xác minh tài khoản; giữ nguyên màn hình để bạn tiếp tục")
        if _menu_evidence(nodes):
            return {"stage": "HOME_MENU_OPEN", "account_input_sent": False}
        menu = [node for node in nodes
                if node.get("content-desc", "").startswith("Browse menu Tab")]
        if (len(menu) == 1 and menu[0].get('selected') == 'true' and
                time.monotonic() >= next_fallback):
            if _confirm_menu_fallback(phone, deadline - time.monotonic(), stop):
                return {"stage": "HOME_MENU_OPEN", "account_input_sent": False}
            next_fallback = time.monotonic() + 5
        if len(menu) == 1 and tapped_menu:
            if menu[0].get("selected") == "false":
                unselected_reads += 1
            else:
                unselected_reads = 0
        if len(menu) == 1 and menu_taps < 3 and (
                not tapped_menu or unselected_reads >= 2):
            try:
                _tap(phone, menu[0])
            except ToolError as exc:
                if not isinstance(exc.__cause__, TimeoutExpired):
                    raise
                # ADB may time out after Android received this navigation tap.
                # Observe the next screen before deciding whether to retry.
                pass
            tapped_menu = True
            menu_taps += 1
            unselected_reads = 0
        elif "Skip sign in" in labels and not skip_back_sent:
            # Leave the first-run sign-in screen with Android Back, without
            # touching the Skip control or changing subsequent menu routing.
            cloud_adb(phone, "shell", "input", "keyevent", "4")
            skip_back_sent = True
        elif "Sign in or create account" in labels and not backed_out:
            cloud_adb(phone, "shell", "input", "keyevent", "4")
            backed_out = True
        if stop is None:
            time.sleep(1)
        else:
            stop.wait(1)
    raise ToolError("Amazon chưa hiện menu ba gạch; đã dừng tại màn hiện tại")


def ready_for_home_menu(name: str) -> dict:
    """Start, install and open Amazon, then stop at the home Browse menu."""
    profile = start_profile(name)
    installed = install_amazon(name)
    shell = open_adb_shell(name)
    show_apps(name, shell["device_id"])
    phone = CloudPhone(shell["serial"])
    open_amazon(phone)
    menu = open_home_menu(phone)
    return {"profile": profile, "amazon_package_installed":
            installed["amazon_package_installed"], **menu}
