"""Shared Android UI recognition and Amazon registration steps b4–b11.

Every action reads the live Android hierarchy. Unknown or ambiguous screens
raise ToolError so the phone stays where it is for a manual fix.
"""
from __future__ import annotations

import math
import random
import re
import threading
import time
import xml.etree.ElementTree as ET
from io import BytesIO
from subprocess import TimeoutExpired
from typing import Callable

from PIL import Image

from .cloud import CloudPhone, cloud_adb, cloud_screenshot
from .core import AMAZON_PACKAGE, ToolError
from .otp import wait_for_new_otp
from .post_menu import (AttemptDeadline, PostMenuSession, PostMenuStep,
                        RegistrationState, RecoverableStepError, type_characters)
from .registration import BOUNDS, _field_for_label
from .runner import RunJob
from . import ui_backend


UI_PATH = "/sdcard/amazon_tool_post_menu.xml"
SIZE = re.compile(r"(?:Physical|Override) size:\s*(\d+)x(\d+)")
PHONE_FIELD = "Enter mobile number or email"
NAME_FIELD = "First and last name"
OTP_FIELD = "Enter security code"


def _text(node: dict[str, str]) -> str:
    value = node.get("text", "").strip() or node.get("content-desc", "")
    return " ".join(value.split()).casefold().rstrip(".")


def _has(nodes: list[dict[str, str]], label: str) -> bool:
    target = label.casefold().rstrip(".:")
    return any(" ".join(node.get(attribute, "").split()).casefold().rstrip(".:") == target
               for node in nodes for attribute in ("text", "content-desc"))


def screen(nodes: list[dict[str, str]]) -> str:
    """Classify only screenshot-supported screens; unknown means stop."""
    if _has(nodes, "Verify mobile number") and _has(nodes, "Enter security code"):
        return "SMS"
    if _has(nodes, "Verify with WhatsApp") and _has(nodes, "Send code by SMS"):
        return "WHATSAPP"
    create_heading = any(_has(nodes, title) for title in
                         ("Create account", "Create an account", "Create your Amazon account"))
    name_label = _has(nodes, NAME_FIELD)
    if (create_heading and name_label) or (
            (create_heading or name_label) and
            _has(nodes, "Mobile number") and _has(nodes, "Continue") and
            len(_visible_edit_fields(nodes)) == 1):
        return "CREATE_FORM"
    if _has(nodes, "Looks like you are new to Amazon") and _has(
            nodes, "Proceed to create an account"):
        return "NEW_ACCOUNT"

    country_rows = {node.get("bounds", "") for node in nodes
                    if _visible(node) and re.fullmatch(
                        r"[a-z][a-z .()'-]*\s+\+\d{1,4}", _text(node))}
    if _has(nodes, "Country/region code") and len(country_rows) >= 2:
        return "COUNTRY"

    # The country selector label can remain in the identifier form hierarchy,
    # and WebView dumps sometimes omit the heading or EditText node. Recognize
    # the live phone form from its label/button or unique input/button pair
    # before treating the country label as an open picker.
    identifier_heading = _has(nodes, "Sign in or create account")
    phone_label = _has(nodes, PHONE_FIELD)
    has_continue = _has(nodes, "Continue")
    edit_count = len(_visible_edit_fields(nodes))
    if ((identifier_heading and phone_label) or
            (phone_label and has_continue) or
            (identifier_heading and has_continue and edit_count == 1) or
            (has_continue and edit_count == 1 and
             not _has(nodes, "Country/region code"))):
        return "IDENTIFIER"
    if _has(nodes, "Country/region code"):
        return "COUNTRY"
    if (_has(nodes, "Shop by category") or
            (_has(nodes, "Sign In") and _has(nodes, "Customer Service"))):
        return "MENU"
    return "UNKNOWN"


def menu_layout(nodes: list[dict[str, str]]) -> str:
    """Classify a live Browse menu by its accessible content, not an image."""
    if screen(nodes) != "MENU":
        return "OTHER"
    labels = {_text(node) for node in nodes}
    cards = {"gifting", "pets", "fashion and beauty", "your stuff",
             "sports & outdoors", "books and reading", "office & professional"}
    list_items = {"books", "electronics", "home services", "see all",
                  "today's deals", "try prime"}
    if cards & labels:
        return "CARDS"
    if ({"sign in", "customer service"} <= labels and
            len(list_items & labels) >= 2):
        return "LIST"
    return "UNKNOWN"


def home_visible(nodes: list[dict[str, str]]) -> bool:
    if screen(nodes) == "MENU":
        return False
    return (_has(nodes, "Sign in for the best experience") or
            any(node.get("content-desc", "").startswith("Home Tab")
                and node.get("selected") == "true" for node in nodes))


class _UiReadIncomplete(RecoverableStepError):
    pass


def _read_nodes(phone: CloudPhone, deadline: AttemptDeadline,
                stop: threading.Event) -> list[dict[str, str]]:
    attempt = 0
    while True:
        if stop.is_set():
            raise ToolError("Đã dừng máy này")
        deadline.remaining()
        try:
            return _read_nodes_once(phone, deadline, stop)
        except ToolError as exc:
            if (not isinstance(exc, _UiReadIncomplete) and
                    not isinstance(exc.__cause__, TimeoutExpired)):
                raise
        attempt += 1
        if attempt == 1 or attempt % 5 == 0:
            deadline.recovering(f"Đọc màn hình chưa xong · đang tự phục hồi lần {attempt}")
        stop.wait(deadline.allowance(min(1, 0.1 * attempt)))


def _read_nodes_once(phone: CloudPhone, deadline: AttemptDeadline,
                     stop: threading.Event) -> list[dict[str, str]]:
    from .isolated_reader import current
    reader = current(phone.serial)
    if reader is not None:
        try:
            return reader.call('read', min(35, deadline.remaining()), stop)
        except ToolError as exc:
            raise _UiReadIncomplete(str(exc)) from exc
    # Remember only the successful reading method, never a stale screen/frame.
    # Reprobe accessibility every 20 seconds and when visual reading fails.
    if (deadline.visual_until.get(phone.serial, 0) > time.monotonic() and
            not ui_backend.ready(phone)):
        try:
            visual = _read_visual_nodes(phone, deadline, stop)
            if screen(visual) != "UNKNOWN":
                return visual
        except _UiReadIncomplete:
            pass
        deadline.visual_until.pop(phone.serial, None)
    nodes = []
    read_error = None
    try:
        nodes = _read_hierarchy(phone, deadline, stop)
    except ToolError as exc:
        if not isinstance(exc, _UiReadIncomplete) and not isinstance(exc.__cause__, TimeoutExpired):
            raise
        read_error = exc
    kind = screen(nodes)
    if kind != "UNKNOWN" and (kind not in {"IDENTIFIER", "CREATE_FORM", "SMS"}
                              or _visible_edit_fields(nodes)):
        return nodes
    try:
        visual = _read_visual_nodes(phone, deadline, stop)
    except _UiReadIncomplete:
        if read_error is not None:
            raise read_error
        if nodes:
            return nodes
        raise
    if screen(visual) != "UNKNOWN":
        deadline.visual_until[phone.serial] = time.monotonic() + 20
        return visual
    if read_error is not None:
        raise read_error
    return nodes


def _read_hierarchy(phone: CloudPhone, deadline: AttemptDeadline,
                    stop: threading.Event) -> list[dict[str, str]]:
    if stop.is_set():
        raise ToolError("Đã dừng máy này")
    deadline.remaining()
    fast_xml = (ui_backend.read_tree(phone) if ui_backend.ready(phone) or
                deadline.remaining() >= 35 else None)
    if fast_xml is not None:
        deadline.remaining()
        nodes = _parse_ui_nodes(fast_xml)
        if not nodes:
            raise ToolError("Amazon không ở màn hình trước; giữ nguyên máy này")
        return nodes
    timeout = max(1, math.ceil(min(6, deadline.remaining())))
    dumped = cloud_adb(phone, "shell", "uiautomator", "dump", UI_PATH,
                       timeout=timeout, check=False)
    if dumped.returncode:
        raise _UiReadIncomplete("Không đọc được cây giao diện Amazon")
    result = cloud_adb(phone, "shell", "cat", UI_PATH,
                       timeout=max(1, math.ceil(min(6, deadline.remaining()))), check=False)
    if result.returncode:
        raise _UiReadIncomplete("Không lấy được cây giao diện Amazon từ ADB")
    try:
        nodes = _parse_ui_nodes(result.stdout)
    except ET.ParseError as exc:
        raise _UiReadIncomplete("Cây giao diện Amazon chưa hợp lệ") from exc
    if not nodes:
        raise ToolError("Amazon không ở màn hình trước; giữ nguyên máy này")
    return nodes


def _read_visual_nodes(phone: CloudPhone, deadline: AttemptDeadline,
                       stop: threading.Event) -> list[dict[str, str]]:
    if stop.is_set():
        raise ToolError("Đã dừng máy này")
    try:
        # OCR mode must also verify the foreground app; a similar browser form
        # or a system dialog is not evidence that Amazon is ready for a tap.
        focus = cloud_adb(phone, "shell", "dumpsys", "window", "windows",
                          timeout=max(1, math.ceil(min(4, deadline.remaining()))),
                          check=False)
        if not any("mCurrentFocus=" in line and AMAZON_PACKAGE in line
                   for line in focus.stdout.splitlines()):
            raise _UiReadIncomplete("Chưa xác nhận Amazon đang ở phía trước")
        screenshot = cloud_screenshot(
            phone, timeout=max(1, math.ceil(min(6, deadline.remaining()))))
        from .vision import ocr_nodes

        return ocr_nodes(screenshot, stop=stop, remaining=deadline.remaining)
    except ImportError as exc:
        raise ToolError("Amazon cần OCR để đọc WebView; cài dependencies dự án rồi mở lại tool") from exc
    except _UiReadIncomplete:
        raise
    except ToolError as exc:
        raise _UiReadIncomplete("Lần đọc ảnh Amazon chưa thành công; đang thử lại") from exc
    except Exception as exc:
        raise _UiReadIncomplete("Chữ trên ảnh Amazon chưa đọc được; đang thử lại") from exc


def _parse_ui_nodes(xml: str) -> list[dict[str, str]]:
    root = ET.fromstring(xml)
    parents = {child: parent for parent in root.iter() for child in parent}
    amazon_nodes = [node for node in root.iter("node")
                    if node.get("package") == AMAZON_PACKAGE]
    ids = {node: str(index) for index, node in enumerate(amazon_nodes)}
    return [dict(node.attrib, ui_id=ids[node],
                 ui_parent=ids.get(parents.get(node), "")) for node in amazon_nodes]


def verify_menu_open(phone: CloudPhone, profile_name: str = "q1") -> None:
    """Read-only guard for attaching an already-running phone."""
    nodes = _read_nodes(phone, AttemptDeadline(10), threading.Event())
    if screen(nodes) != "MENU":
        raise ToolError(f"{profile_name} chưa ở menu ba gạch; mở đúng menu rồi thử lại")


def _bounds(node: dict[str, str]) -> tuple[int, int, int, int]:
    found = BOUNDS.fullmatch(node.get("bounds", ""))
    if not found:
        raise ToolError("Phần tử Amazon chưa có vùng bấm hợp lệ")
    x1, y1, x2, y2 = map(int, found.groups())
    if x2 <= x1 or y2 <= y1:
        raise ToolError("Vùng bấm Amazon không hợp lệ")
    return x1, y1, x2, y2


def _tap(phone: CloudPhone, node: dict[str, str], deadline: AttemptDeadline) -> None:
    x1, y1, x2, y2 = _bounds(node)
    cloud_adb(phone, "shell", "input", "tap", str((x1 + x2) // 2),
              str((y1 + y2) // 2),
              timeout=max(1, math.ceil(min(6, deadline.remaining()))))


def _tap_for_transition(phone: CloudPhone, node: dict[str, str],
                        deadline: AttemptDeadline) -> None:
    """Transport errors are uncertain delivery; the caller must observe next UI."""
    _bounds(node)  # Invalid targets must never be treated as dispatched taps.
    try:
        _tap(phone, node, deadline)
    except ToolError:
        deadline.recovering("ADB chưa xác nhận cú chạm · đang đọc lại màn hình")


def _unique(nodes: list[dict[str, str]], label: str,
            *, starts: bool = False) -> dict[str, str]:
    target = label.casefold()
    matches = [node for node in nodes if
               (_text(node).startswith(target) if starts else _text(node) == target)]
    # UI hierarchies sometimes repeat one visible label at identical bounds.
    distinct = {node.get("bounds", ""): node for node in matches}
    if len(distinct) != 1 or "" in distinct:
        raise ToolError(f"Không xác định được duy nhất '{label}' trên máy này")
    return next(iter(distinct.values()))


def _visible(node: dict[str, str]) -> bool:
    if node.get("visible-to-user") == "false" or node.get("enabled") == "false":
        return False
    try:
        _bounds(node)
    except ToolError:
        return False
    return True


class _ActionNotResolved(RecoverableStepError):
    pass


def _button(nodes: list[dict[str, str]], label: str,
            *, below: dict[str, str] | None = None) -> dict[str, str]:
    """Select the visible action control, not a hidden duplicate label."""
    matches = [node for node in nodes if _has([node], label)
               and _visible(node)]
    by_id = {node["ui_id"]: node for node in nodes if "ui_id" in node}
    actions = []
    for match in matches:
        action = match
        parent = by_id.get(match.get("ui_parent", ""))
        while (match.get("class") != "android.widget.Button" and parent is not None
               and _visible(parent) and parent.get("scrollable") != "true"):
            if parent.get("clickable") == "true":
                if (_text(parent) in {"", label.casefold()} and
                        parent.get("class") != "android.widget.EditText"):
                    action = parent
                break
            parent = by_id.get(parent.get("ui_parent", ""))
        actions.append(action)
    matches = actions
    if below is not None:
        bottom = _bounds(below)[3]
        matches = [node for node in matches if _bounds(node)[1] >= bottom]
    for preferred in (
            [node for node in matches if node.get("clickable") == "true"
             and node.get("class") == "android.widget.Button"],
            [node for node in matches if node.get("clickable") == "true"],
            matches):
        distinct = {node["bounds"]: node for node in preferred}
        if len(distinct) == 1:
            return next(iter(distinct.values()))
        if len(distinct) > 1:
            if below is not None:
                # A WebView may expose the button and its nested label separately.
                for outer in distinct.values():
                    left, top, right, bottom = _bounds(outer)
                    if all(left <= x1 < x2 <= right and top <= y1 < y2 <= bottom
                           for x1, y1, x2, y2 in map(_bounds, distinct.values())):
                        return outer
                # The form's full-width action aligns with the name input.
                field_left, _, field_right, _ = _bounds(below)
                min_overlap = (field_right - field_left) * 0.8
                aligned = []
                for candidate in distinct.values():
                    left, _, right, _ = _bounds(candidate)
                    if min(right, field_right) - max(left, field_left) >= min_overlap:
                        aligned.append(candidate)
                if len(aligned) == 1:
                    return aligned[0]
            break
    raise _ActionNotResolved(f"Không xác định được duy nhất nút '{label}' trên máy này")


def _yellow_form_button(image: Image.Image, field: dict[str, str], *,
                        labels: tuple[tuple[int, int, int, int], ...] = ()) -> dict[str, str]:
    """Find one wide yellow action aligned below the verified input field."""
    left, top, right, bottom = _bounds(field)
    width = right - left
    height = bottom - top
    if not (0 <= left < right <= image.width and 0 <= top < bottom < image.height):
        raise _ActionNotResolved("Vùng ô nhập không khớp ảnh màn hình Android")
    pixels = image.convert("RGB").load()
    rows = []
    for y in range(bottom, min(image.height, bottom + 8 * height)):
        yellow = 0
        for x in range(left, right, 3):
            r, g, b = pixels[x, y]
            if r >= 230 and 160 <= g <= 239 and r > g and b <= 95:
                yellow += 3
        if yellow >= width * 0.75:
            rows.append(y)
    bands = []
    for y in rows:
        if not bands or y - bands[-1][-1] > 3:
            bands.append([])
        bands[-1].append(y)
    matches = [band for band in bands if height * 0.4 <= len(band) <= height * 1.8]
    if len(matches) > 1:
        matches = [band for band in matches if any(
            left <= (x1 + x2) // 2 < right and band[0] <= (y1 + y2) // 2 <= band[-1]
            for x1, y1, x2, y2 in labels)]
    if len(matches) != 1:
        raise _ActionNotResolved("Chưa xác định được một nút vàng dưới ô nhập từ ảnh Android")
    band = matches[0]
    return {"bounds": f"[{left},{band[0]}][{right},{band[-1] + 1}]"}


def _visual_form_button(phone: CloudPhone, nodes: list[dict[str, str]], label: str,
                        field: dict[str, str],
                        deadline: AttemptDeadline) -> dict[str, str]:
    labels = tuple(_bounds(node) for node in nodes if _visible(node) and _has([node], label))
    timeout = max(1, math.ceil(min(6, deadline.remaining())))
    try:
        screenshot = cloud_screenshot(phone, timeout=timeout)
        with Image.open(BytesIO(screenshot)) as image:
            return _yellow_form_button(image, field, labels=labels)
    except _ActionNotResolved:
        raise
    except ToolError as exc:
        raise _ActionNotResolved(str(exc)) from exc
    except OSError:
        raise _ActionNotResolved("Không đọc được ảnh màn hình Android") from None


def _form_action(phone: CloudPhone, nodes: list[dict[str, str]], label: str,
                 field: dict[str, str], deadline: AttemptDeadline) -> dict[str, str]:
    try:
        return _button(nodes, label, below=field)
    except _ActionNotResolved:
        return _visual_form_button(phone, nodes, label, field, deadline)


def _wait_screen(phone: CloudPhone, expected: set[str],
                 deadline: AttemptDeadline, stop: threading.Event,
                 *, seconds: float = 20) -> list[dict[str, str]]:
    next_notice = time.monotonic() + seconds
    last_screen = "UNKNOWN"
    last_read_failed = False
    while True:
        if stop.is_set():
            raise ToolError("Đã dừng máy này")
        try:
            nodes = _read_nodes(phone, deadline, stop)
        except ToolError as exc:
            if not isinstance(exc, _UiReadIncomplete) and not isinstance(exc.__cause__, TimeoutExpired):
                raise
            last_read_failed = True
        else:
            last_read_failed = False
            last_screen = screen(nodes)
            if last_screen in expected:
                return nodes
        if time.monotonic() >= next_notice:
            deadline.recovering(f"Màn đang chuyển chậm ({last_screen}) · tiếp tục đọc, không bấm lặp")
            next_notice = time.monotonic() + max(3, seconds)
        stop.wait(0.2)


def _registration_nodes(phone: CloudPhone, deadline: AttemptDeadline,
                        stop: threading.Event) -> list[dict[str, str]]:
    """Let a transient blank/loading frame settle before rejecting a form."""
    nodes = _read_nodes(phone, deadline, stop)
    if screen(nodes) != "UNKNOWN":
        return nodes
    deadline.recovering("Form đang tải hoặc chưa rõ chữ · đang đọc lại")
    return _wait_screen(phone, {"IDENTIFIER", "COUNTRY", "NEW_ACCOUNT", "CREATE_FORM",
                                "WHATSAPP", "SMS"}, deadline, stop, seconds=6)


def visit_home(phone: CloudPhone, deadline: AttemptDeadline,
               stop: threading.Event, *, view_seconds: float | None = None) -> None:
    """Open Home by its accessible tab and view it for 2–5 seconds."""
    nodes = _read_nodes(phone, deadline, stop)
    if not home_visible(nodes):
        if screen(nodes) != "MENU":
            raise ToolError("Amazon chưa ở menu để mở Trang chủ")
        home = _unique([node for node in nodes if _visible(node)],
                       "Home Tab", starts=True)
        _tap(phone, home, deadline)
        until = time.monotonic() + deadline.allowance(6)
        while time.monotonic() < until:
            if home_visible(_read_nodes(phone, deadline, stop)):
                break
            stop.wait(min(0.15, max(0, until - time.monotonic())))
        else:
            raise ToolError("Amazon chưa xác nhận Trang chủ sau khi bấm biểu tượng nhà")
    stop.wait(deadline.allowance(view_seconds if view_seconds is not None
                                 else random.choice((2, 3, 4, 5))))
    deadline.remaining()


def route_list_menu(phone: CloudPhone, steps: tuple[PostMenuStep, ...],
                    current: int, session: PostMenuSession,
                    deadline: AttemptDeadline,
                    stop: threading.Event) -> int | None:
    """On a list menu, visit Home once and continue at shared b4."""
    if session.index == 5:
        # q6 has its own Home → Cart → menu/card prefix even on the list menu.
        return None
    matches = [index for index, step in enumerate(steps)
               if step.name == "b4 Sign In"]
    if len(matches) != 1 or current >= matches[0]:
        return None
    nodes = _read_nodes(phone, deadline, stop)
    layout = menu_layout(nodes)
    if layout == "LIST":
        session.menu_route = "LIST"
    elif layout == "CARDS":
        session.menu_route = ""
    if session.menu_route != "LIST" or screen(nodes) in {
            "IDENTIFIER", "NEW_ACCOUNT", "CREATE_FORM", "WHATSAPP", "SMS"}:
        return None
    visit_home(phone, deadline, stop)
    return matches[0]


def _scroll_up(phone: CloudPhone, nodes: list[dict[str, str]],
               deadline: AttemptDeadline, *, country_list: bool = False,
               fling: bool = False, reverse: bool = False) -> None:
    start, end, duration = (0.72, 0.32, "300")
    if country_list:
        deadline.remaining()
        from .isolated_reader import current
        reader = current(phone.serial)
        if reader is not None:
            try:
                attempted = reader.call('scroll', min(15, deadline.remaining()),
                                        reader.stop, fling=fling, reverse=reverse)
            except ToolError:
                # Delivery may be uncertain. Read again before another gesture;
                # never issue an ADB swipe as a second input for this request.
                deadline.recovering('Đang đọc lại sau thao tác cuộn chưa xác nhận')
                return
        else:
            attempted = ui_backend.country_scroll(phone, fling=fling, reverse=reverse)
        if attempted:
            return
        if fling:
            start, end, duration = (0.96, 0.04, "65")
        elif reverse:
            start, end, duration = (0.40, 0.59, "280")
        else:
            start, end, duration = (0.60, 0.40, "280")
        scroll_regions = {_bounds(node) for node in nodes
                          if node.get("scrollable") == "true" and _visible(node)}
        if not scroll_regions:
            # OCR supplies text boxes, not an Android scroll container. Use
            # the currently visible country rows inside the modal, excluding
            # the identifier form visible behind it.
            headings = [_bounds(node) for node in nodes if _visible(node)
                        and _has([node], "Country/region code")]
            header_bottom = max((box[3] for box in headings), default=0)
            rows = [_bounds(node) for node in nodes if _visible(node)
                    and _bounds(node)[1] >= header_bottom
                    and re.fullmatch(r"[a-z][a-z .()'-]*\s*\+\d{1,4}", _text(node))]
            if len(rows) >= 2:
                scroll_regions.add((min(box[0] for box in rows), min(box[1] for box in rows),
                                    max(box[2] for box in rows), max(box[3] for box in rows)))
        if len(scroll_regions) == 1:
            left, top, right, bottom = scroll_regions.pop()
            x = (left + right) // 2
            height = bottom - top
            cloud_adb(phone, "shell", "input", "swipe", str(x),
                      str(top + int(height * start)), str(x),
                      str(top + int(height * end)), duration,
                      timeout=max(1, math.ceil(min(6, deadline.remaining()))))
            return
    dimensions = []
    for node in nodes:
        try:
            _, _, x2, y2 = _bounds(node)
            dimensions.append((x2, y2))
        except ToolError:
            pass
    if dimensions:
        width = max(item[0] for item in dimensions)
        height = max(item[1] for item in dimensions)
    else:
        output = cloud_adb(phone, "shell", "wm", "size", timeout=3).stdout
        found = SIZE.search(output)
        if not found:
            raise ToolError("Không xác định được kích thước màn hình máy này")
        width, height = map(int, found.groups())
    if fling:
        start, end = 0.90, 0.14
    cloud_adb(phone, "shell", "input", "swipe", str(width // 2),
              str(int(height * start)), str(width // 2),
              str(int(height * end)), duration,
              timeout=max(1, math.ceil(min(6, deadline.remaining()))))


def _find_scrolling(phone: CloudPhone, label: str,
                    deadline: AttemptDeadline, stop: threading.Event,
                    *, starts: bool = False,
                    menu_action: bool = False,
                    country_list: bool = False,
                    nodes: list[dict[str, str]] | None = None) -> dict[str, str]:
    previous = None
    reverse = False
    attempt = 0
    while attempt < (40 if country_list else 30):
        if stop.is_set():
            raise ToolError("Đã dừng máy này")
        deadline.remaining()
        if nodes is None:
            nodes = _read_nodes(phone, deadline, stop)
        target = label.casefold()
        matches = [node for node in nodes if _visible(node) and
                   (_text(node).startswith(target) if starts else _text(node) == target)]
        if matches:
            if menu_action:
                try:
                    return _button(nodes, label)
                except ToolError:
                    # The menu can expose both its row and a duplicate label.
                    # Customer Service sits immediately before Sign In in both
                    # observed layouts; use that live landmark if it is unique.
                    anchors = [node for node in nodes if _visible(node)
                               and _text(node) == "customer service"]
                    if len({node["bounds"] for node in anchors}) == 1:
                        return _button(nodes, label, below=anchors[0])
                    raise
            return _unique(matches, label, starts=starts)
        visible = tuple(_text(node) for node in nodes if _visible(node) and _text(node))
        stalled = visible == previous
        if stalled and not country_list:
            break
        fling = False
        if country_list:
            country_labels = [value.rsplit("+", 1)[0].strip() for value in visible
                              if re.fullmatch(r"[a-z][a-z .()'-]*\s*\+\d{1,4}", value)]
            end_marker = any(value.startswith(("wallis", "western sahara", "zimbabwe"))
                             for value in country_labels)
            if not reverse:
                # First quickly reach the end; reverse immediately when the
                # final alphabetical rows appear, without waiting for stasis.
                fling = not end_marker
                reverse = end_marker
            elif stalled:
                # A short reverse swipe can miss/advance slowly; keep nudging.
                reverse = True
        previous = visible
        _scroll_up(phone, nodes, deadline, country_list=country_list,
                   fling=fling, reverse=reverse)
        pause = 0.1 if country_list else 0.12
        stop.wait(deadline.allowance(pause))
        nodes = None
        attempt += 1
    raise ToolError(f"Không tìm thấy '{label}' sau khi cuộn máy này")


def _same_country_position(first: dict[str, str], second: dict[str, str]) -> bool:
    """Ignore minor OCR box jitter while rejecting a row still moving."""
    ax1, ay1, ax2, ay2 = _bounds(first)
    bx1, by1, bx2, by2 = _bounds(second)
    height = min(ay2 - ay1, by2 - by1)
    overlap = min(ax2, bx2) - max(ax1, bx1)
    return (abs((ay1 + ay2) - (by1 + by2)) / 2 <= max(3, height * 0.20)
            and overlap >= min(ax2 - ax1, bx2 - bx1) * 0.75)


def _country_full_row(phone: CloudPhone, row: dict[str, str],
                      deadline: AttemptDeadline) -> dict[str, str]:
    """Tap the middle of the visible country row if its text box missed."""
    output = cloud_adb(phone, "shell", "wm", "size",
                       timeout=max(1, math.ceil(min(4, deadline.remaining()))))
    sizes = SIZE.findall(output.stdout)
    if not sizes:
        raise RecoverableStepError("Không xác định được chiều rộng màn hình để chọn hàng US +1")
    width = int(sizes[-1][0])  # Override size, when present, matches tap coordinates.
    _, top, _, bottom = _bounds(row)
    center = width // 2
    return {"bounds": f"[{center - 1},{top}][{center + 1},{bottom}]"}


def _ensure_menu(phone: CloudPhone, deadline: AttemptDeadline,
                 stop: threading.Event) -> list[dict[str, str]]:
    nodes = _read_nodes(phone, deadline, stop)
    if screen(nodes) == "MENU":
        return nodes
    browse = [node for node in nodes if node.get("content-desc", "").startswith(
        "Browse menu Tab")]
    if len(browse) == 1:
        _tap(phone, browse[0], deadline)
    elif not browse:
        # A category card may have opened a page. Return once, then recheck.
        cloud_adb(phone, "shell", "input", "keyevent", "4",
                  timeout=max(1, math.ceil(min(6, deadline.remaining()))))
    else:
        raise ToolError("Có nhiều nút Browse menu; dừng máy này để kiểm tra")
    return _wait_screen(phone, {"MENU"}, deadline, stop, seconds=6)


def _visible_edit_fields(nodes: list[dict[str, str]]) -> list[dict[str, str]]:
    return [node for node in nodes
            if node.get("class") == "android.widget.EditText" and _visible(node)]


def _field(nodes: list[dict[str, str]], label: str) -> dict[str, str]:
    visible_nodes = [node for node in nodes if _visible(node)]
    try:
        return _field_for_label(visible_nodes, (label,))
    except ToolError:
        fields = _visible_edit_fields(visible_nodes)
        if len(fields) == 1:
            return fields[0]
    raise ToolError(f"Không xác định được ô '{label}' của máy này")


def _keyboard_visible(phone: CloudPhone, deadline: AttemptDeadline) -> bool:
    timeout = max(1, math.ceil(min(4, deadline.remaining())))
    result = cloud_adb(phone, "shell", "dumpsys", "input_method",
                       timeout=timeout, check=False)
    return bool(re.search(r"\bmInputShown=true\b", result.stdout))


def _tap_input(phone: CloudPhone, field: dict[str, str],
               deadline: AttemptDeadline, stop: threading.Event) -> None:
    """Tap a field and confirm focus even when it came from screenshot OCR."""
    attempts = 3 if field.get("vision") == "true" else 1
    for attempt in range(attempts):
        if stop.is_set():
            raise ToolError("Đã dừng máy này")
        if attempt:
            deadline.recovering(f"Ô nhập chưa nhận focus · tìm lại vị trí và chạm lần {attempt + 1}/3")
            label = {"phone": PHONE_FIELD, "name": NAME_FIELD, "otp": OTP_FIELD}.get(
                field.get("vision-field-kind", ""))
            nodes = _read_nodes(phone, deadline, stop)
            expected = {PHONE_FIELD: "IDENTIFIER", NAME_FIELD: "CREATE_FORM", OTP_FIELD: "SMS"}
            if label is None or screen(nodes) != expected[label]:
                raise ToolError("Màn nhập đã thay đổi; chưa chạm lại ô")
            field = _field(nodes, label)
        _tap_for_transition(phone, field, deadline)
        if field.get("vision") != "true" or _keyboard_visible(phone, deadline):
            return
        if attempt + 1 < attempts:
            stop.wait(deadline.allowance(0.2))
    raise ToolError("Đã thử chạm lại ô nhập nhưng bàn phím chưa mở; kiểm tra ô trên máy rồi bấm Tiếp tục")


def _type_field(phone: CloudPhone, label: str, value: str,
                deadline: AttemptDeadline, stop: threading.Event, *,
                nodes: list[dict[str, str]] | None = None) -> list[dict[str, str]]:
    if nodes is None:
        nodes = _read_nodes(phone, deadline, stop)
    for recovery in range(3):
        if recovery:
            deadline.recovering(f"Đã đọc lại ô nhập · gõ tiếp phần còn thiếu, lần {recovery + 1}/3")
        # A control can be temporarily absent while the WebView reflows.
        for read_attempt in range(3):
            try:
                field = _field(nodes, label)
                break
            except ToolError:
                if read_attempt == 2:
                    raise
                deadline.recovering("Ô nhập đang thay đổi · đọc lại trước khi gõ")
                stop.wait(deadline.allowance(0.15))
                nodes = _read_nodes(phone, deadline, stop)
        current = field.get("text", "")
        if current == value:
            return nodes
        if current and field.get("vision") == "true":
            # An OCR prefix may be an incomplete reading of a full value.
            # Reobserve it before deciding, and never append based on OCR alone.
            for _ in range(2):
                stop.wait(deadline.allowance(0.15))
                nodes = _read_nodes(phone, deadline, stop)
                field = _field(nodes, label)
                current = field.get("text", "")
                if current == value:
                    return nodes
                if field.get("vision") != "true":
                    break
            if field.get("vision") == "true":
                raise ToolError(f"OCR chưa xác nhận đầy đủ ô '{label}'; giữ nguyên nội dung để tránh gõ lặp")
        if current and not value.startswith(current):
            raise ToolError(f"Ô '{label}' khác dữ liệu của máy này; sửa trực tiếp rồi Tiếp tục")
        if field.get("vision") == "true":
            _tap_input(phone, field, deadline, stop)
        elif field.get("focused") != "true":
            _tap_for_transition(phone, field, deadline)
        # Name, phone and OTP all require the same native focus checks.
        if field.get("focused") == "false" and field.get("vision") != "true":
            nodes = _read_nodes(phone, deadline, stop)
            field = _field(nodes, label)
            if field.get("focused") == "false":
                _tap_for_transition(phone, field, deadline)
                nodes = _read_nodes(phone, deadline, stop)
                field = _field(nodes, label)
            if field.get("focused") == "false":
                raise ToolError(f"Ô '{label}' chưa nhận focus sau khi thử lại")
            current = field.get("text", "")
            if current == value:
                return nodes
            if current and not value.startswith(current):
                raise ToolError(f"Ô '{label}' khác dữ liệu của máy này; chưa gõ thêm")
        if current:
            # A tap in an existing prefix may put the caret in its middle.
            cloud_adb(phone, "shell", "input", "keyevent", "KEYCODE_MOVE_END",
                       timeout=max(1, math.ceil(min(4, deadline.remaining()))))
        input_error = None
        try:
            type_characters(phone, value[len(current):], deadline, stop)
        except ToolError as exc:
            if stop.is_set():
                raise
            input_error = exc
        # An uncertain ADB result must be resolved by fresh field readback,
        # never by resending the entire value. Wait for IME updates first.
        observed = []
        for attempt in range(3):
            if attempt and stop.wait(deadline.allowance(0.15)):
                raise ToolError("Đã dừng máy này")
            nodes = _read_nodes(phone, deadline, stop)
            try:
                field = _field(nodes, label)
            except ToolError:
                continue
            actual = field.get("text", "")
            if actual == value:
                return nodes
            observed.append(actual)
        # OCR can omit characters, so it must not authorize appending a
        # supposedly missing suffix. Native readback must be stable twice.
        if (len(observed) < 2 or field.get("vision") == "true" or observed[-1] != observed[-2] or
                not value.startswith(observed[-1])):
            if input_error is not None:
                raise input_error
            break
    raise ToolError(f"Chưa xác nhận được nội dung ô '{label}'")


def _at_or_after(nodes: list[dict[str, str]], kind: str) -> bool:
    order = {"MENU": 0, "IDENTIFIER": 1, "NEW_ACCOUNT": 2,
             "CREATE_FORM": 3, "WHATSAPP": 4, "SMS": 5}
    return screen(nodes) in order and order[screen(nodes)] >= order[kind]


def _national_phone(job: RunJob) -> str:
    if job.account is None:
        raise ToolError("Máy này chưa có thông tin Amazon")
    digits = re.sub(r"\D", "", job.account.phone)
    if len(digits) == 11 and digits.startswith("1"):
        return digits[1:]
    if len(digits) == 10:
        return digits
    raise ToolError("SĐT máy này cần 10 số US hoặc 1 + 10 số")


def _check_summary(nodes: list[dict[str, str]], job: RunJob) -> None:
    digits_on_screen = "".join(re.findall(r"\d", " ".join(
        node.get("text", "") for node in nodes)))
    if _national_phone(job) not in digits_on_screen:
        raise ToolError("SĐT trên Amazon không khớp hàng của máy này")


def resume_common_index(phone: CloudPhone, steps: tuple[PostMenuStep, ...],
                        current: int, deadline: AttemptDeadline,
                        stop: threading.Event) -> int:
    """Rewind a paused phone to its observed shared screen, never skip ahead."""
    if current >= len(steps) - 1:  # A prior Create tap must never be repeated.
        return current
    target_name = {
        "MENU": "b4 Sign In",
        "IDENTIFIER": "b4 Sign In",
        "COUNTRY": "b6 chọn US +1",
        "NEW_ACCOUNT": "b8 Proceed to create an account",
        "CREATE_FORM": "b9 nhập tên",
        "WHATSAPP": "b10 Send code by SMS",
        "SMS": "b10 Send code by SMS",
    }.get(screen(_read_nodes(phone, deadline, stop)))
    if target_name is None:
        return current
    matches = [index for index, step in enumerate(steps)
               if step.name == target_name]
    return min(current, matches[0]) if len(matches) == 1 else current


def build_common_steps(phone: CloudPhone,
                       on_otp: Callable[[str], None],
                       on_status: Callable[[str], None] = lambda _status: None,
                       registration: RegistrationState | None = None,
                       ) -> tuple[PostMenuStep, ...]:
    """Build b4–b11 once for any machine, with OTP state local to this phone."""
    state = registration if registration is not None else RegistrationState()

    def sign_in(job: RunJob, deadline: AttemptDeadline,
                stop: threading.Event) -> None:
        nodes = _read_nodes(phone, deadline, stop)
        if screen(nodes) == "IDENTIFIER":
            return
        if _at_or_after(nodes, "NEW_ACCOUNT"):
            return
        _ensure_menu(phone, deadline, stop)
        _tap_for_transition(phone, _find_scrolling(phone, "Sign In", deadline, stop,
                                                   menu_action=True), deadline)

    def focus_phone(job: RunJob, deadline: AttemptDeadline,
                    stop: threading.Event) -> None:
        nodes = _wait_screen(phone, {"IDENTIFIER", "NEW_ACCOUNT", "CREATE_FORM",
                                    "WHATSAPP", "SMS", "COUNTRY"}, deadline, stop)
        if screen(nodes) == "IDENTIFIER":
            _tap_input(phone, _field(nodes, PHONE_FIELD), deadline, stop)

    def phone_number(job: RunJob, deadline: AttemptDeadline,
                     stop: threading.Event) -> None:
        nodes = _registration_nodes(phone, deadline, stop)
        if _at_or_after(nodes, "NEW_ACCOUNT"):
            return
        if screen(nodes) != "IDENTIFIER" or job.account is None:
            raise ToolError("Máy này chưa ở form nhập số điện thoại")
        _national_phone(job)
        _type_field(phone, PHONE_FIELD, job.account.phone,
                    deadline, stop, nodes=nodes)

    def country(job: RunJob, deadline: AttemptDeadline,
                stop: threading.Event) -> None:
        nodes = _registration_nodes(phone, deadline, stop)
        unclosed_taps = 0
        while not stop.is_set():
            deadline.remaining()
            kind = screen(nodes)
            if _at_or_after(nodes, "NEW_ACCOUNT"):
                return
            if kind == "IDENTIFIER":
                unclosed_taps = 0
                candidates = [node for node in nodes if _visible(node) and re.fullmatch(
                    r"[a-z]{2}\s*\+\d+", _text(node))]
                if len(candidates) != 1:
                    raise ToolError("Không xác định được ô chọn mã quốc gia")
                if _has(candidates, "US +1"):
                    return
                _tap_for_transition(phone, candidates[0], deadline)
                nodes = _wait_screen(phone, {"COUNTRY"}, deadline, stop)
            elif kind != "COUNTRY":
                raise ToolError("Máy này chưa ở danh sách mã quốc gia")

            target = _find_scrolling(phone, "United States +1", deadline, stop,
                                     country_list=True, nodes=nodes)
            if stop.wait(deadline.allowance(0.15)):
                break
            nodes = _read_nodes(phone, deadline, stop)
            current = [node for node in nodes if _visible(node) and
                       _text(node) == "united states +1"]
            current = list({node["bounds"]: node for node in current}.values())
            if (screen(nodes) != "COUNTRY" or len(current) != 1 or
                    not _same_country_position(target, current[0])):
                continue  # Momentum can move a row between reading and tapping.
            _tap_for_transition(phone, current[0], deadline)
            if stop.wait(deadline.allowance(0.8)):
                break
            nodes = _read_nodes(phone, deadline, stop)
            if screen(nodes) == "COUNTRY":
                visible_us = [node for node in nodes if _visible(node) and
                              _text(node) == "united states +1"]
                visible_us = list({node["bounds"]: node for node in visible_us}.values())
                if len(visible_us) == 1 and _same_country_position(current[0], visible_us[0]):
                    deadline.recovering("Hộp quốc gia còn mở · thử bấm giữa hàng US +1")
                    _tap_for_transition(phone, _country_full_row(phone, visible_us[0], deadline),
                                        deadline)
                    if stop.wait(deadline.allowance(0.8)):
                        break
                    nodes = _read_nodes(phone, deadline, stop)
            if screen(nodes) == "COUNTRY":
                unclosed_taps += 1
                if unclosed_taps >= 4:
                    raise ToolError("Đã thử vùng chữ và giữa hàng US +1 bốn lần nhưng danh sách chưa đóng; kiểm tra máy này")
                deadline.recovering("Danh sách chưa đóng · đọc lại hàng US +1 rồi chọn lại")
            # If Android landed on another country, reopen and look again.
        raise ToolError("Đã dừng máy này")

    def continue_number(job: RunJob, deadline: AttemptDeadline,
                        stop: threading.Event) -> None:
        nodes = _registration_nodes(phone, deadline, stop)
        if _at_or_after(nodes, "NEW_ACCOUNT"):
            return
        if screen(nodes) != "IDENTIFIER" or not _has(nodes, "US +1"):
            raise ToolError("Máy này chưa xác nhận số điện thoại US +1")
        _check_summary(nodes, job)
        _tap_for_transition(phone, _button(nodes, "Continue"), deadline)
        _wait_screen(phone, {"NEW_ACCOUNT", "CREATE_FORM"}, deadline, stop)

    def proceed(job: RunJob, deadline: AttemptDeadline,
                stop: threading.Event) -> None:
        nodes = _registration_nodes(phone, deadline, stop)
        if _at_or_after(nodes, "CREATE_FORM"):
            return
        if screen(nodes) != "NEW_ACCOUNT":
            raise ToolError("Máy này chưa ở màn tạo tài khoản mới")
        _check_summary(nodes, job)
        _tap_for_transition(phone, _button(nodes, "Proceed to create an account"), deadline)
        _wait_screen(phone, {"CREATE_FORM", "WHATSAPP", "SMS"}, deadline, stop)

    def name(job: RunJob, deadline: AttemptDeadline,
             stop: threading.Event) -> None:
        nodes = _registration_nodes(phone, deadline, stop)
        if _at_or_after(nodes, "WHATSAPP"):
            return
        if screen(nodes) != "CREATE_FORM" or job.account is None:
            raise ToolError("Máy này chưa ở form nhập tên")
        _check_summary(nodes, job)
        nodes = _type_field(phone, NAME_FIELD, job.account.full_name,
                            deadline, stop, nodes=nodes)
        if screen(nodes) != "CREATE_FORM":
            raise ToolError("Amazon không còn ở form nhập tên")
        try:
            button = _form_action(phone, nodes, "Continue", _field(nodes, NAME_FIELD), deadline)
        except _ActionNotResolved:
            timeout = max(1, math.ceil(min(6, deadline.remaining())))
            ime = cloud_adb(phone, "shell", "dumpsys", "input_method", timeout=timeout)
            if re.search(r"\bmInputShown=true\b", ime.stdout):
                cloud_adb(phone, "shell", "input", "keyevent", "KEYCODE_BACK", timeout=timeout)
                nodes = _read_nodes(phone, deadline, stop)
                if screen(nodes) != "CREATE_FORM":
                    raise ToolError("Amazon đã rời form nhập tên sau khi đóng bàn phím")
                _check_summary(nodes, job)
            else:
                raise
            field = _field(nodes, NAME_FIELD)
            if field.get("text", "") != job.account.full_name:
                raise ToolError("Chưa xác nhận được tên trên form")
            button = _form_action(phone, nodes, "Continue", field, deadline)
        _tap_for_transition(phone, button, deadline)
        _wait_screen(phone, {"WHATSAPP", "SMS"}, deadline, stop)

    def send_sms(job: RunJob, deadline: AttemptDeadline,
                 stop: threading.Event) -> None:
        nodes = _registration_nodes(phone, deadline, stop)
        if screen(nodes) == "SMS":
            if state.sms_requested_at is None:
                state.sms_requested_at = time.monotonic()
            on_status("Đang chờ mã")
            return
        if state.sms_requested_at is not None:
            try:
                _wait_screen(phone, {"SMS"}, deadline, stop)
            except ToolError as exc:
                raise ToolError("Đã bấm gửi SMS nhưng chưa xác nhận màn nhập mã; kiểm tra máy này") from exc
            on_status("Đang chờ mã")
            return
        if screen(nodes) != "WHATSAPP" or job.account is None:
            raise ToolError("Máy này chưa ở màn chọn gửi mã bằng SMS")
        _check_summary(nodes, job)
        button = _button(nodes, "Send code by SMS")
        _bounds(button)
        # Record dispatch intent before ADB; transport errors can arrive after
        # Android received the tap. Only observing SMS confirms the result.
        state.sms_requested_at = time.monotonic()
        try:
            _tap_for_transition(phone, button, deadline)
        except ToolError:
            pass
        on_status("Đang chờ mã")
        _wait_screen(phone, {"SMS"}, deadline, stop)

    def read_sms_form(job: RunJob, deadline: AttemptDeadline,
                      stop: threading.Event) -> list[dict[str, str]]:
        nodes = _registration_nodes(phone, deadline, stop)
        if screen(nodes) != "SMS" or job.account is None:
            raise ToolError("Máy này chưa ở màn nhập mã SMS")
        _check_summary(nodes, job)
        return nodes

    def focus_otp(job: RunJob, deadline: AttemptDeadline,
                  stop: threading.Event) -> None:
        field = _field(read_sms_form(job, deadline, stop), OTP_FIELD)
        if not re.fullmatch(r"[0-9]{6}", field.get("text", "")):
            _tap_input(phone, field, deadline, stop)

    def enter_otp(job: RunJob, deadline: AttemptDeadline,
                  stop: threading.Event) -> None:
        nodes = read_sms_form(job, deadline, stop)
        current = _field(nodes, OTP_FIELD).get("text", "")
        if re.fullmatch(r"[0-9]{6}", current):
            state.code = current
            on_otp(current)
            on_status("Đã nhập mã")
            return
        if state.sms_requested_at is None:
            raise ToolError("Chưa xác nhận được lần gửi SMS; sửa mã trên máy rồi Tiếp tục")
        while True:
            try:
                code = state.code or job.account.browser_otp or wait_for_new_otp(
                    job.account.otp_url, None,
                    timeout=deadline.allowance(30), stop=stop,
                    not_before=state.sms_requested_at + 4)
                break
            except ToolError as exc:
                if "Hết thời gian chờ lượt đọc OTP" not in str(exc):
                    on_status("Không đọc được mã SMS")
                    raise
                on_status("Chưa lấy được mã · tự mở lại trình duyệt")
        _type_field(phone, OTP_FIELD, code, deadline, stop,
                    nodes=read_sms_form(job, deadline, stop))
        state.code = code
        on_otp(code)
        on_status("Đã nhập mã")

    def create_account(job: RunJob, deadline: AttemptDeadline,
                       stop: threading.Event) -> None:
        nodes = (_read_nodes(phone, deadline, stop) if state.create_pressed else
                 _registration_nodes(phone, deadline, stop))
        if screen(nodes) != "SMS" and state.create_pressed:
            return
        if screen(nodes) != "SMS":
            raise ToolError("Máy này không còn ở màn SMS; kiểm tra trước khi tạo tài khoản")
        value = _field(nodes, OTP_FIELD).get("text", "")
        if not re.fullmatch(r"[0-9]{6}", value):
            raise ToolError("Máy này chưa nhập đủ OTP để tạo tài khoản")
        if state.code and value != state.code:
            raise ToolError("Mã đang hiện khác mã đã xác nhận trên máy này")
        if not state.create_pressed:
            _check_summary(nodes, job)
            field = _field(nodes, OTP_FIELD)
            button = _form_action(phone, nodes, "Create your Amazon account", field, deadline)
            _bounds(button)
            state.create_pressed = True
            try:
                _tap_for_transition(phone, button, deadline)
            except ToolError:
                pass
        until = time.monotonic() + deadline.allowance(10)
        while time.monotonic() < until:
            if screen(_read_nodes(phone, deadline, stop)) != "SMS":
                return  # A later screenshot is needed to classify the result.
            stop.wait(0.25)
        raise ToolError("Đã bấm Create nhưng Amazon vẫn ở màn OTP; kiểm tra máy này")

    return (
        PostMenuStep("b4 Sign In", sign_in),
        PostMenuStep("b4a chạm ô SĐT", focus_phone),
        PostMenuStep("b5 nhập SĐT", phone_number),
        PostMenuStep("b6 chọn US +1", country),
        PostMenuStep("b7 Continue", continue_number),
        PostMenuStep("b8 Proceed to create an account", proceed),
        PostMenuStep("b9 nhập tên", name),
        PostMenuStep("b10 Send code by SMS", send_sms),
        PostMenuStep("b11a chạm ô OTP", focus_otp),
        PostMenuStep("b11 nhập OTP", enter_otp),
        PostMenuStep("b11 bấm Create your Amazon account", create_account,
                     within_attempt=False),
    )
