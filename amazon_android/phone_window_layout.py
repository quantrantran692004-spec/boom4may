"""Best-effort layout of visible Swarmote phone viewer windows.

Only Win32 window geometry changes. The phone, ADB and UIA workflows do not
depend on this module succeeding.
"""
from __future__ import annotations

import re
import threading
from math import ceil
from statistics import median

import psutil


_lock = threading.Lock()
_arranged: set[tuple[int, str, int]] = set()
_PHONE_TITLE = re.compile(r"(.+) - (ACN\d+)")


def _sort_key(item):
    profile = item[1].rsplit(" - ", 1)[0]
    numbered = re.fullmatch(r"q(\d+)", profile, re.IGNORECASE)
    return (0, int(numbered.group(1)), item[1]) if numbered else (1, profile.casefold(), item[1])


def _tiles(work: tuple[int, int, int, int], count: int,
           base: tuple[int, int]) -> list[tuple[int, int, int, int]]:
    """Fit portrait viewers in reading order without overlapping work area."""
    if count <= 0:
        return []
    left, top, right, bottom = work
    margin, gap = 8, 8
    width = max(1, right - left - margin * 2)
    height = max(1, bottom - top - margin * 2)
    columns = max(range(1, count + 1), key=lambda n: (
        min((width - gap * (n - 1)) / (n * base[0]),
            (height - gap * (ceil(count / n) - 1)) /
            (ceil(count / n) * base[1])), -n))
    rows = ceil(count / columns)
    cell_width = max(1, (width - gap * (columns - 1)) // columns)
    cell_height = max(1, (height - gap * (rows - 1)) // rows)
    scale = min(1, cell_width / base[0], cell_height / base[1])
    tile_width = max(1, int(base[0] * scale))
    tile_height = max(1, int(base[1] * scale))
    return [(left + margin + (index % columns) * (cell_width + gap),
             top + margin + (index // columns) * (cell_height + gap),
             tile_width, tile_height) for index in range(count)]


def _row_if_fits(work: tuple[int, int, int, int],
                 sizes: list[tuple[int, int]]) -> list[tuple[int, int, int, int]] | None:
    """Keep each viewer's size when one row already fits the monitor."""
    left, top, right, bottom = work
    margin, gap = 8, 8
    total_width = sum(width for width, _ in sizes) + gap * max(0, len(sizes) - 1)
    if (total_width > right - left - margin * 2 or
            any(height > bottom - top - margin * 2 for _, height in sizes)):
        return None
    x = left + margin
    result = []
    for width, height in sizes:
        result.append((x, top + margin, width, height))
        x += width + gap
    return result


def arrange_on_open(handle: int, expected_exe: str) -> None:
    """Arrange once per new viewer, keeping windows on their current monitor."""
    import win32api
    import win32con
    import win32gui
    import win32process

    with _lock:
        viewers = []

        def collect(candidate, _extra):
            title = win32gui.GetWindowText(candidate)
            if (not _PHONE_TITLE.fullmatch(title) or
                    not win32gui.IsWindowVisible(candidate) or
                    win32gui.IsIconic(candidate)):
                return
            try:
                _, pid = win32process.GetWindowThreadProcessId(candidate)
                if psutil.Process(pid).exe().casefold() != expected_exe.casefold():
                    return
                monitor = win32api.MonitorFromWindow(candidate,
                                                     win32con.MONITOR_DEFAULTTONEAREST)
                work = tuple(win32api.GetMonitorInfo(monitor)["Work"])
                rect = win32gui.GetWindowRect(candidate)
            except (psutil.NoSuchProcess, psutil.AccessDenied, OSError):
                return
            viewers.append((candidate, title, pid, monitor, work,
                            rect[2] - rect[0], rect[3] - rect[1]))

        win32gui.EnumWindows(collect, None)
        current = next((item for item in viewers if item[0] == handle), None)
        if current is None:
            return
        group = sorted((item for item in viewers if item[3] == current[3]), key=_sort_key)
        identities = {(item[0], item[1], item[2]) for item in group}
        _arranged.intersection_update({(item[0], item[1], item[2]) for item in viewers})
        if (current[0], current[1], current[2]) in _arranged:
            return  # A user may have moved this window since the first layout.
        portrait = [(item[5], item[6]) for item in group if item[6] > item[5] * 1.3]
        sizes = portrait or [(item[5], item[6]) for item in group]
        base = (max(1, int(median(size[0] for size in sizes))),
                max(1, int(median(size[1] for size in sizes))))
        positions = (_row_if_fits(current[4], [(item[5], item[6]) for item in group])
                     or _tiles(current[4], len(group), base))
        flags = (win32con.SWP_NOACTIVATE | win32con.SWP_NOZORDER |
                 win32con.SWP_NOOWNERZORDER | win32con.SWP_ASYNCWINDOWPOS)
        for item, (x, y, width, height) in zip(group, positions):
            win32gui.SetWindowPos(item[0], 0, x, y, width, height, flags)
        _arranged.update(identities)
