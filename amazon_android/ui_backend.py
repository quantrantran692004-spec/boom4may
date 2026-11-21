"""Fast, per-serial UiAutomator2 reads through Swarmote's existing ADB server.

Only u2.jar is deployed on first connection. No input IME is installed and no
account data is logged. A failed reader cools down before the ADB fallback.
"""
from __future__ import annotations

import os
import re
import socket
import threading
import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field

from .cloud import CloudPhone, swarmote_adb_path, swarmote_tunnel_owner
from .core import AMAZON_PACKAGE, ToolError


@dataclass
class _Session:
    device: object | None = None
    retry_at: float = 0
    lock: threading.RLock = field(default_factory=threading.RLock)


_sessions: dict[str, _Session] = {}
_guard = threading.Lock()


def _session(phone: CloudPhone) -> _Session:
    with _guard:
        return _sessions.setdefault(phone.serial, _Session())


def ready(phone: CloudPhone) -> bool:
    item = _session(phone)
    return item.device is not None and time.monotonic() >= item.retry_at


def _connect(phone: CloudPhone):
    if not swarmote_tunnel_owner(int(phone.serial.rsplit(":", 1)[1])):
        raise ToolError("Tunnel không thuộc Swarmote")
    # Do not let adbutils select its bundled ADB or a device automatically.
    with socket.create_connection(("127.0.0.1", 5037), timeout=2):
        pass
    os.environ["ADBUTILS_ADB_PATH"] = str(swarmote_adb_path())
    import adbutils
    import uiautomator2

    client = adbutils.AdbClient(host="127.0.0.1", port=5037, socket_timeout=5)
    if phone.serial not in {device.serial for device in client.device_list()}:
        raise ToolError("Chưa thấy đúng serial Swarmote")
    return uiautomator2.connect(client.device(serial=phone.serial))


def _failed(item: _Session) -> None:
    if item.device is not None:
        try:
            item.device.stop_uiautomator(wait=False)
        except Exception:
            pass
    item.device = None
    item.retry_at = time.monotonic() + 30


def read_tree(phone: CloudPhone) -> str | None:
    item = _session(phone)
    with item.lock:
        if time.monotonic() < item.retry_at:
            return None
        try:
            if item.device is None:
                item.device = _connect(phone)
            # Request all window roots explicitly; default active-root results
            # can omit WebView descendants during initial attachment.
            xml = item.device.dump_hierarchy(max_depth=150, root_in_active=False)
            root = ET.fromstring(xml)
            if next(root.iter("node"), None) is None:
                raise ToolError("UiAutomator2 chưa có cây giao diện")
            return xml
        except Exception:
            _failed(item)
            return None


def country_reverse_points(top: int, bottom: int, centers: list[int],
                           *, gentle: bool = False,
                           distance_multiplier: int = 1) -> tuple[int, int]:
    """Move back four rows normally, or at most one row for a gentle b6 swipe."""
    height = bottom - top
    ordered = sorted(set(center for center in centers if top <= center <= bottom))
    gaps = [b - a for a, b in zip(ordered, ordered[1:]) if b > a]
    if gaps:
        row_height = sorted(gaps)[len(gaps) // 2]
        distance = min(int(height * 0.70), max(int(height * 0.28), 4 * row_height))
    else:
        distance = int(height * 0.40)
    if gentle:
        distance = max(1, min(int(height * 0.10), row_height if gaps else int(height * 0.08)))
        distance *= distance_multiplier
    start = top + max(1, (height - distance) // 2)
    return start, start + distance


def country_scroll(phone: CloudPhone, *, fling: bool, reverse: bool,
                   gentle: bool = False) -> bool:
    """Return True once a gesture was attempted; never repeat uncertain input."""
    if not ready(phone):
        return False
    item = _session(phone)
    with item.lock:
        xml = read_tree(phone)
        if xml is None:
            return False
        nodes = [node for node in ET.fromstring(xml).iter("node")
                 if node.get("package") == AMAZON_PACKAGE]
        # This path is only for the live native country container, not menus
        # or a WebView with no scrollable element. The existing fallback handles
        # screenshots when Android does not expose the container.
        heading = any((node.get("text", "") or node.get("content-desc", ""))
                      .strip().casefold().rstrip(":") == "country/region code" for node in nodes)
        if not heading:
            return False
        containers = [node for node in nodes if node.get("scrollable") == "true"]
        if len(containers) != 1:
            return False
        bounds = re.fullmatch(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]", containers[0].get("bounds", ""))
        if not bounds:
            return False
        left, top, right, bottom = map(int, bounds.groups())
        if right <= left or bottom <= top:
            return False
        try:
            control = item.device(packageName=AMAZON_PACKAGE, scrollable=True)
            if control.count != 1:
                return False
        except Exception:
            _failed(item)
            return False
        try:
            if fling:
                control.fling.toEnd(max_swipes=3)
            else:
                x = (left + right) // 2
                if reverse:
                    centers = []
                    for node in nodes:
                        value = (node.get("text", "") or node.get("content-desc", "")).strip()
                        match = re.fullmatch(r"[a-zA-ZÅå][a-zA-ZÅå .()'-]*\s*\+\d{1,4}", value)
                        box = re.fullmatch(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]", node.get("bounds", ""))
                        if match and box:
                            _, y1, _, y2 = map(int, box.groups())
                            centers.append((y1 + y2) // 2)
                    y1, y2 = country_reverse_points(top, bottom, centers,
                                                    gentle=gentle)
                else:
                    y1 = top + int((bottom - top) * 0.60)
                    y2 = top + int((bottom - top) * 0.40)
                item.device.swipe(x, y1, x, y2,
                                  duration=0.65 if reverse and gentle else 0.28)
        except Exception:
            # A network error may follow a delivered gesture. Caller must read
            # again, not emit an ADB swipe as a second attempt in this call.
            _failed(item)
        return True
