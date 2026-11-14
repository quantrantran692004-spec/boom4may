"""UI Automation for Swarmote's Profile form.

Controls use UIA patterns without physical mouse or keyboard input. The
management window is activated for Chromium buttons that ignore background
Invoke; no session cookies or private Swarmote endpoints are read.
"""
from __future__ import annotations

import re
import time
from dataclasses import dataclass
from pathlib import Path
from os import environ

import psutil

from .core import ToolError


class ProfileNotFound(ToolError):
    """The exact Profile name is absent from a trustworthy Profiles view."""


class ProfileLookupError(ToolError):
    """The Profiles view cannot identify one exact row."""


class ProfileCreateNotSubmitted(ToolError):
    """Validation or UI failed before the Create request was sent."""


class ProfileStartNotSubmitted(ToolError):
    """The Start button was never invoked; retrying cannot duplicate a Start."""


class ProxyTestFailed(ProfileCreateNotSubmitted):
    """Swarmote rejected the proxy before submitting Profile creation."""


class ProfileManagerWindowError(ToolError):
    """The Swarmote management window cannot be identified safely."""


@dataclass(frozen=True)
class ProxyConfig:
    kind: str
    host: str
    port: int
    username: str = ""
    password: str = ""

    def __post_init__(self) -> None:
        if self.kind not in {"socks5", "http", "https"}:
            raise ToolError("Loại proxy phải là socks5, http hoặc https")
        if not self.host or re.search(r"[\s/@:]", self.host):
            raise ToolError("Host proxy không hợp lệ")
        if not 1 <= self.port <= 65535:
            raise ToolError("Port proxy phải trong khoảng 1–65535")


def _swarmote_exe() -> Path:
    default = Path(environ.get("LOCALAPPDATA", str(Path.home()))) / "Programs" / "Swarmote" / "Swarmote.exe"
    running = set()
    for process in psutil.process_iter(["name", "exe"]):
        try:
            if (process.info.get("name") or "").casefold() == "swarmote.exe" and process.info.get("exe"):
                running.add(Path(process.info["exe"]))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    if len(running) == 1:
        return running.pop()
    if len(running) > 1:
        raise ToolError("Có nhiều bản Swarmote đang chạy; hãy giữ một bản trước khi chạy mẻ")
    candidates = [default]
    for key in ("ProgramFiles", "ProgramFiles(x86)"):
        if environ.get(key):
            candidates.append(Path(environ[key]) / "Swarmote" / "Swarmote.exe")
    return next((p for p in candidates if p.is_file()), default)


def ensure_manager_ready(*, stop=None, progress=None, seconds=60):
    """Launch an installed manager once, then wait for its Profiles page."""
    import subprocess

    deadline = time.monotonic() + seconds
    launch_checked = False
    report = _progress_reporter(progress, "Đang tìm/mở Swarmote và chờ trang Profiles")
    last_error = "chưa thấy cửa sổ"
    while time.monotonic() < deadline:
        _check_stop(stop)
        report()
        try:
            window = _main_window()
        except ProfileManagerWindowError as exc:
            last_error = str(exc)
            if not launch_checked:
                exe = _swarmote_exe()
                running = False
                for process in psutil.process_iter(["exe"]):
                    try:
                        if (process.info.get("exe") or "").casefold() == str(exe).casefold():
                            running = True
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
                launch_checked = True
                if not running:
                    if not exe.is_file():
                        raise ToolError("Chưa tìm thấy Swarmote đã cài. Cài Swarmote hoặc mở bản đã cài rồi chạy mẻ lại")
                    _check_stop(stop)
                    subprocess.Popen([str(exe)], cwd=str(exe.parent),
                                     creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            try:
                _open_profiles(window)
                return window
            except ToolError as exc:
                last_error = str(exc)
                # A manager exists: never launch a second instance for login/loading.
                launch_checked = True
        _pause(0.5, stop)
    _check_stop(stop)
    raise ToolError(f"Swarmote chưa sẵn sàng sau {seconds:g}s: {last_error}. "
                    "Nếu đang ở màn đăng nhập, hãy đăng nhập và mở Profiles rồi chạy lại")


def _main_window():
    try:
        from pywinauto import Desktop
        import win32gui
        import win32process
    except ImportError as exc:
        raise ToolError("Thiếu pywinauto; cài dự án bằng python -m pip install -e .") from exc
    expected = str(_swarmote_exe()).casefold()
    handles = []

    def collect(handle, _extra):
        if not win32gui.GetWindowText(handle).casefold().startswith("swarmote"):
            return
        try:
            _, pid = win32process.GetWindowThreadProcessId(handle)
            if psutil.Process(pid).exe().casefold() == expected:
                handles.append(handle)
        except (psutil.NoSuchProcess, psutil.AccessDenied, OSError):
            return

    win32gui.EnumWindows(collect, None)
    if len(handles) > 1:
        profiles = [handle for handle in handles
                    if win32gui.IsWindowVisible(handle)
                    and win32gui.GetWindowText(handle).casefold().endswith("profiles")]
        if len(profiles) == 1:
            handles = profiles
    if len(handles) != 1:
        raise ProfileManagerWindowError(
            f"Cần đúng một cửa sổ quản lý Swarmote; tìm thấy {len(handles)}")
    return Desktop(backend="uia").window(handle=handles[0]).wrapper_object()


def _descendants(control) -> list:
    """Wrap only valid UIA elements; Swarmote sometimes exposes type-less nodes."""
    from pywinauto.controls.uiawrapper import UIAWrapper

    result = []
    for info in control.element_info.descendants():
        if not info.control_type:
            continue
        try:
            result.append(UIAWrapper(info))
        except (KeyError, ValueError):
            continue
    return result


def _one(window, name: str, control_type: str):
    matches = [item for item in _descendants(window)
               if item.element_info.name == name and item.element_info.control_type == control_type]
    if len(matches) != 1:
        raise ToolError(f"Giao diện Swarmote thay đổi: cần một {control_type} '{name}', thấy {len(matches)}")
    return matches[0]


def _invoke(window, name: str, control_type: str = "Button") -> None:
    item = _one(window, name, control_type)
    try:
        item.invoke()
    except Exception as exc:
        raise ToolError(f"Không thể kích hoạt '{name}' bằng UI Automation; đã dừng để không chiếm chuột") from exc


def _select_radio(window, name: str) -> None:
    item = _one(window, name, "RadioButton")
    try:
        item.iface_selection_item.Select()
    except Exception as exc:
        raise ToolError(f"Không chọn được '{name}' qua UI Automation") from exc


def _set_value(window, name: str, control_type: str, value: str) -> None:
    item = _one(window, name, control_type)
    try:
        # ValuePattern avoids mouse/focus and pywinauto's text-bearing action log.
        item.iface_value.SetValue(value)
    except Exception as exc:
        raise ToolError(f"Không điền được trường '{name}' qua UI Automation") from exc


def _check_stop(stop) -> None:
    if stop is not None and stop.is_set():
        raise ToolError("Đã dừng thao tác Swarmote")


def _pause(seconds: float, stop) -> None:
    if stop is None:
        time.sleep(seconds)
    elif stop.wait(seconds):
        _check_stop(stop)


def _progress_reporter(progress, message: str):
    """Report a wait immediately and every three seconds, without account data."""
    started = time.monotonic()
    next_update = started

    def report():
        nonlocal next_update
        now = time.monotonic()
        if progress is not None and now >= next_update:
            progress(f"{message} · {now - started:.0f}s")
            next_update = now + 3
    return report


def _wait_for(window, name: str, control_type: str | None, seconds: float = 8,
              stop=None, progress=None, visible: bool = False) -> None:
    until = time.monotonic() + seconds
    report = _progress_reporter(progress, f"Đang chờ {name}")
    last_error = ""
    while time.monotonic() < until:
        _check_stop(stop)
        report()
        try:
            if any(item.element_info.name == name and (control_type is None or item.element_info.control_type == control_type)
                   and (not visible or item.is_visible())
                   for item in _descendants(window)):
                return
        except Exception as exc:
            _check_stop(stop)
            last_error = f"; lỗi đọc UI gần nhất: {type(exc).__name__}"
        _pause(0.25, stop)
    _check_stop(stop)
    raise ToolError(f"Swarmote không hiện '{name}' sau {seconds:g} giây{last_error}")


def _activate_manager(window) -> None:
    """Expose Chromium controls before invoking buttons that ignore background UIA."""
    import win32con
    import win32gui

    try:
        if not win32gui.IsWindowVisible(window.handle):
            win32gui.ShowWindow(window.handle, win32con.SW_SHOWNA)
        if win32gui.IsIconic(window.handle):
            win32gui.ShowWindow(window.handle, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(window.handle)
    except Exception as exc:
        raise ToolError("Không đưa được cửa sổ quản lý Swarmote lên trước để bấm New Profile") from exc


def _profile_form_open(window) -> bool:
    controls = {(x.element_info.name, x.element_info.control_type)
                for x in _descendants(window)}
    return {("Create", "Button"), ("Single Create", "RadioButton"),
            ("Profile Name", "Edit"), ("ip/Host", "Edit")} <= controls


def _unfiltered_single_page(window, controls: list) -> bool:
    """All Profiles are visible when the unfiltered table has no next page."""
    searches = [x for x in controls if x.element_info.name == "Profile Name"
                and x.element_info.control_type == "Edit"]
    next_buttons = [x for x in controls if x.element_info.name == "Go to next page"
                    and x.element_info.control_type == "Button"]
    previous_buttons = [x for x in controls if x.element_info.name == "Go to previous page"
                        and x.element_info.control_type == "Button"]
    has_total = any(re.fullmatch(r"Total \d+", x.element_info.name)
                    for x in controls)
    return (len(searches) == len(next_buttons) == len(previous_buttons) == 1
            and has_total and not searches[0].iface_value.CurrentValue
            and not next_buttons[0].is_enabled()
            and not previous_buttons[0].is_enabled())


def _open_profiles(window) -> None:
    """Use the visible Profiles page even when its sidebar is collapsed."""
    controls = _descendants(window)
    if any(x.element_info.name == "New Profile" and x.element_info.control_type == "Button"
           for x in controls):
        return
    # Swarmote's compact sidebar does not expose a named Profiles MenuItem.
    # The document title still identifies the page while its content loads.
    if any(x.element_info.control_type == "Document" and
           x.element_info.name.casefold().endswith("profiles") for x in controls):
        _wait_for(window, "New Profile", "Button", seconds=10)
        return
    menu_items = [x for x in controls if x.element_info.name == "Profiles" and
                  x.element_info.control_type == "MenuItem"]
    if len(menu_items) == 1:
        try:
            menu_items[0].invoke()
        except Exception as exc:
            raise ToolError("Không mở được trang Profiles qua UI Automation") from exc
        _wait_for(window, "New Profile", "Button")
        return
    raise ToolError("Không xác định được trang Profiles. Hãy mở danh sách Profiles trong Swarmote rồi thử lại")


def visible_profile_names() -> set[str]:
    """Read the current Profiles table without typing in its search field."""
    window = _main_window()
    _open_profiles(window)
    return {x.element_info.name for x in _descendants(window)
            if x.element_info.control_type == "DataItem"
            and re.fullmatch(r"q\d+", x.element_info.name)}


def inspect() -> dict:
    """Read-only status without proxy or account values."""
    window = _main_window()
    controls = {(item.element_info.name, item.element_info.control_type)
                for item in _descendants(window)}
    return {
        "window_found": True,
        "profile_form_open": ("Create", "Button") in controls and ("Profile Name", "Edit") in controls,
        "proxy_form_available": ("ip/Host", "Edit") in controls and ("Port", "Spinner") in controls,
        "mouse_or_focus_used": False,
    }


def create_profile(name: str, proxy: ProxyConfig, *, hide_window: bool = False) -> dict:
    """Create one Swarmote Profile using its Custom proxy form.

    This never starts the phone. It stops if semantic UIA controls disappear.
    """
    if not hide_window:
        return _create_profile_form(name, proxy)
    import win32con
    import win32gui

    try:
        window = _main_window()
    except ToolError as exc:
        raise ProfileCreateNotSubmitted(str(exc)) from exc
    was_visible = bool(win32gui.IsWindowVisible(window.handle))
    try:
        if was_visible:
            win32gui.ShowWindow(window.handle, win32con.SW_HIDE)
        if win32gui.IsWindowVisible(window.handle):
            raise ProfileCreateNotSubmitted("Không ẩn được cửa sổ quản lý Swarmote")
        return _create_profile_form(name, proxy, window)
    finally:
        if win32gui.IsWindow(window.handle):
            win32gui.ShowWindow(window.handle, win32con.SW_SHOWNA)


def _create_profile_form(name: str, proxy: ProxyConfig, window=None) -> dict:
    # The optional hidden mode can keep the form hidden between Chromium button
    # invocations. Each button still needs a brief visible foreground activation.
    hidden_requested = False
    if window is not None and getattr(window, "handle", None) is not None:
        import win32gui
        hidden_requested = not win32gui.IsWindowVisible(window.handle)

    def restore_hidden() -> None:
        if hidden_requested:
            import win32con
            import win32gui
            win32gui.ShowWindow(window.handle, win32con.SW_HIDE)

    try:
        if not name.strip() or len(name.strip()) > 80:
            raise ToolError("Tên Profile phải dài 1–80 ký tự")
        if proxy.kind != "socks5":
            raise ToolError("Bản giao diện đã xác minh mặc định socks5; chưa xác minh chọn HTTP/HTTPS không chiếm chuột")
        window = window or _main_window()
        if any(x.element_info.name == name.strip() and x.element_info.control_type == "DataItem"
               for x in _descendants(window)):
            raise ToolError("Profile cùng tên đã tồn tại trong danh sách Swarmote; không tạo lại")
        if not _profile_form_open(window):
            _open_profiles(window)
            _activate_manager(window)
            _invoke(window, "New Profile")
            try:
                _wait_for(window, "Create", "Button")
            except ToolError as exc:
                raise ToolError("Đã bấm New Profile nhưng form tạo chưa mở; chưa điền tên hoặc proxy") from exc
            if not _profile_form_open(window):
                raise ToolError("New Profile chưa mở đúng form tạo; chưa điền tên hoặc proxy")
            restore_hidden()
        _select_radio(window, "Single Create")
        _select_radio(window, "Custom")
        _set_value(window, "Profile Name", "Edit", name.strip())
        _set_value(window, "ip/Host", "Edit", proxy.host)
        _set_value(window, "Port", "Spinner", str(proxy.port))
        if proxy.username:
            _set_value(window, "Account", "Edit", proxy.username)
        if proxy.password:
            _set_value(window, "Password", "Edit", proxy.password)
        # Swarmote must validate the outgoing proxy before a cloud phone is made.
        _activate_manager(window)
        _invoke(window, "Test Proxy")
        restore_hidden()
        until_tested = time.monotonic() + 35
        while time.monotonic() < until_tested:
            labels = {x.element_info.name for x in _descendants(window)}
            if "Test Passed" in labels:
                break
            if "Test Failed" in labels:
                raise ProxyTestFailed("Swarmote báo proxy không đạt bài kiểm tra; chưa tạo Profile")
            time.sleep(0.3)
        else:
            raise ToolError("Swarmote chưa xác nhận Test Passed; chưa tạo Profile")
    except ProxyTestFailed:
        raise
    except ToolError as exc:
        raise ProfileCreateNotSubmitted(str(exc)) from exc
    _activate_manager(window)
    _invoke(window, "Create")
    restore_hidden()
    try:
        _wait_for(window, name.strip(), "DataItem", seconds=60)
    except ToolError as exc:
        raise ToolError("Đã gửi yêu cầu tạo Profile nhưng chưa xác định kết quả; kiểm tra danh sách trước khi thử lại") from exc
    return {"profile_name": name.strip(), "created": True, "proxy_configured": True,
            "phone_started": False}


def profile_status(name: str) -> dict:
    """Read one exact Profile, including rows hidden by Swarmote pagination."""
    window = _main_window()
    _open_profiles(window)
    controls = _descendants(window)
    rows = [x.parent() for x in controls
            if x.element_info.name == name and x.element_info.control_type == "DataItem"]
    if not rows:
        if _unfiltered_single_page(window, controls):
            raise ProfileNotFound(f"Không thấy Profile tên '{name}'")
        search = _one(window, "Profile Name", "Edit")
        previous = search.iface_value.CurrentValue
        try:
            _set_value(window, "Profile Name", "Edit", name)
            deadline = time.monotonic() + 6
            searched_at = time.monotonic()
            while time.monotonic() < deadline:
                controls = _descendants(window)
                rows = [x.parent() for x in controls
                        if x.element_info.name == name and x.element_info.control_type == "DataItem"]
                if rows:
                    break
                no_results = any(x.element_info.name == "Total 0" for x in controls)
                if no_results and time.monotonic() - searched_at >= 1.0:
                    raise ProfileNotFound(f"Không thấy Profile tên '{name}'")
                time.sleep(0.2)
            if not rows:
                raise ProfileLookupError(f"Không xác minh được Profile '{name}' qua bộ lọc Swarmote")
            result = _profile_row_status(name, rows)
        finally:
            _set_value(window, "Profile Name", "Edit", previous)
        return result
    return _profile_row_status(name, rows)


def _profile_row_status(name: str, rows: list) -> dict:
    if len(rows) != 1:
        raise ProfileLookupError(f"Có {len(rows)} Profile tên '{name}'; cần kiểm tra thủ công")
    cells = [x.element_info.name for x in rows[0].children()
             if x.element_info.control_type == "DataItem"]
    return {"profile_name": name, "state": next((x for x in cells if x in {"Offline", "Running"}), "Unknown"),
            "device_id": next((x for x in cells if x.startswith("ACN")), None)}


def start_profile(name: str, *, wait: bool = True) -> dict:
    """Send Start with UIA; optionally return before the phone finishes booting."""
    try:
        current = profile_status(name)
        settle_until = time.monotonic() + 15
        while current["state"] not in {"Running", "Offline"} and time.monotonic() < settle_until:
            time.sleep(0.5)
            current = profile_status(name)
        if current["state"] == "Running":
            return current
        if current["state"] != "Offline":
            raise ToolError("Profile chưa ở trạng thái Offline, dừng trước khi gửi Start")
        window = _main_window()
        search = _one(window, "Profile Name", "Edit")
        previous_filter = search.iface_value.CurrentValue
        filtered = not any(x.element_info.name == name and x.element_info.control_type == "DataItem"
                           for x in _descendants(window))
    except ToolError as exc:
        raise ProfileStartNotSubmitted(str(exc)) from exc
    invoked = False
    try:
        if filtered:
            _set_value(window, "Profile Name", "Edit", name)
            _wait_for(window, name, "DataItem", seconds=10)
        _select_profile_rows(window, [name])
        # The toolbar changes from disabled "Start" to enabled "Start(1)"
        # asynchronously after selecting one row.
        until_enabled = time.monotonic() + 8
        while time.monotonic() < until_enabled:
            starts = [x for x in _descendants(window)
                      if x.element_info.name in {"Start", "Start(1)"}
                      and x.element_info.control_type == "Button" and x.is_enabled()]
            if len(starts) == 1:
                if _selected_profile_names(window) != {name}:
                    raise ToolError("Swarmote đã đổi lựa chọn Profile trước khi Start; chưa gửi Start")
                invoked = True
                starts[0].invoke()
                break
            time.sleep(0.25)
        else:
            raise ToolError("Swarmote chưa bật nút Start cho Profile đã chọn")
    except ToolError as exc:
        if not invoked:
            raise ProfileStartNotSubmitted(str(exc)) from exc
        raise
    finally:
        if invoked:
            try:
                _select_profile_rows(window, [], seconds=3)
            except ToolError:
                pass  # Next Start still requires an exact Start(1) selection.
        if filtered:
            try:
                _set_value(window, "Profile Name", "Edit", previous_filter)
            except ToolError as exc:
                if not invoked:
                    raise ProfileStartNotSubmitted(str(exc)) from exc
                raise
    if not wait:
        return {**current, "state": "Starting"}
    until = time.monotonic() + 90
    while time.monotonic() < until:
        state = profile_status(name)
        if state["state"] == "Running":
            return state
        time.sleep(1)
    raise ToolError("Đã gửi Start nhưng chưa xác định trạng thái; kiểm tra Profile trước khi thử lại")


def start_profiles_together(names: list[str], timeout: int = 120) -> dict[str, dict]:
    """Select exact Offline Profiles and send one Start(N) UIA command."""
    if not names or len(names) != len(set(names)):
        raise ToolError("Danh sách Profile mở đồng thời phải khác nhau và không trống")
    initial = {name: profile_status(name) for name in names}
    offline = [name for name, item in initial.items() if item["state"] == "Offline"]
    unknown = [name for name, item in initial.items()
               if item["state"] not in {"Offline", "Running"}]
    if unknown:
        raise ToolError(f"Trạng thái chưa rõ của {', '.join(unknown)}; chưa gửi Start")
    if not offline:
        return initial

    window = _main_window()
    _select_profile_rows(window, offline)

    expected = f"Start({len(offline)})"
    until_enabled = time.monotonic() + 8
    while time.monotonic() < until_enabled:
        buttons = [x for x in _descendants(window)
                   if x.element_info.name == expected
                   and x.element_info.control_type == "Button" and x.is_enabled()]
        if len(buttons) == 1:
            if _selected_profile_names(window) != set(offline):
                raise ToolError("Swarmote đã đổi lựa chọn Profile trước khi Start; chưa gửi Start")
            buttons[0].invoke()
            break
        time.sleep(0.25)
    else:
        raise ToolError(f"Swarmote chưa bật nút {expected}; chưa gửi Start")

    deadline = time.monotonic() + timeout
    latest = dict(initial)
    while time.monotonic() < deadline:
        for name in offline:
            try:
                latest[name] = profile_status(name)
            except ToolError:
                latest[name] = {"profile_name": name, "state": "Unknown", "device_id": None}
        if all(latest[name]["state"] == "Running" for name in offline):
            return latest
        time.sleep(1)
    return latest


def _profile_checkbox(window, name: str):
    row = _one(window, name, "DataItem").parent()
    boxes = [x for x in _descendants(row) if x.element_info.control_type == "CheckBox"]
    if len(boxes) != 1:
        raise ToolError(f"{name}: không xác định được checkbox duy nhất")
    return boxes[0]


def _selected_profile_names(window) -> set[str]:
    """Read checked rows, excluding the table header's select-all checkbox."""
    selected = set()
    for item in _descendants(window):
        if item.element_info.control_type != "CheckBox" or item.get_toggle_state() != 1:
            continue
        ancestor = item.parent()
        while ancestor and ancestor.element_info.control_type != "Table":
            if ancestor.element_info.control_type == "DataItem":
                cells = [x.element_info.name for x in ancestor.children()
                         if x.element_info.control_type == "DataItem"]
                if len(cells) >= 3 and cells[1].isdigit() and cells[2]:
                    selected.add(cells[2])
                    break
            ancestor = ancestor.parent()
    return selected


def _select_profile_rows(window, names: list[str], seconds: float = 8) -> None:
    """Select rows sequentially; Swarmote re-renders after each toggle."""
    target = set(names)
    for name in names:
        _profile_checkbox(window, name)
    current = _selected_profile_names(window)
    for name in current - target:
        _profile_checkbox(window, name).iface_toggle.Toggle()
        _wait_for_selected(window, current - {name}, seconds)
        current.remove(name)
    for name in names:
        if name in current:
            continue
        _profile_checkbox(window, name).iface_toggle.Toggle()
        _wait_for_selected(window, current | {name}, seconds)
        current.add(name)


def _wait_for_selected(window, expected: set[str], seconds: float) -> None:
    until = time.monotonic() + seconds
    last = set()
    while time.monotonic() < until:
        last = _selected_profile_names(window)
        if last == expected:
            return
        time.sleep(0.2)
    raise ToolError(f"Swarmote chọn {', '.join(sorted(last)) or '0'}; cần {', '.join(sorted(expected)) or '0'}; chưa gửi Start")


def open_adb_shell(name: str, device_id: str | None = None, *, stop=None, progress=None) -> dict:
    """Open the phone's ADB tunnel through background UIA patterns."""
    _check_stop(stop)
    if device_id is None:
        status = profile_status(name)
        if status["state"] != "Running" or not status["device_id"]:
            raise ToolError("Profile cần ở trạng thái Running và có Device ID")
        device_id = status["device_id"]
    window = _phone_window(name, device_id, seconds=35, stop=stop, progress=progress)
    _check_stop(stop)
    report = _progress_reporter(progress, "Đang mở Terminal / ADB Shell")
    report()
    controls = _descendants(window)
    if not any(x.element_info.name == "ADB Shell" and x.element_info.control_type == "TabItem"
               and x.is_visible() for x in controls):
        until_terminal = time.monotonic() + 30
        groups = []
        while time.monotonic() < until_terminal:
            _check_stop(stop)
            report()
            controls = _descendants(window)
            groups = []
            seen = set()
            for label in controls:
                if (label.element_info.name != "Terminal" or
                        label.element_info.control_type != "Text" or
                        not label.is_visible()):
                    continue
                group = label.parent()
                if group.element_info.control_type != "Group":
                    continue
                runtime_id = getattr(group.element_info, "runtime_id", None)
                key = tuple(runtime_id) if runtime_id else id(group)
                if key not in seen:
                    groups.append(group)
                    seen.add(key)
            if groups:
                break
            _pause(0.25, stop)
        if not groups:
            raise ToolError("Không tìm thấy nút Terminal trong cửa sổ Profile")
        opened = False
        for group in groups:
            _check_stop(stop)
            try:
                group.invoke()
            except Exception:
                _check_stop(stop)
                # The Invoke may have landed; inspect before another candidate.
                pass
            try:
                _wait_for(window, "ADB Shell", "TabItem", seconds=3,
                          stop=stop, progress=progress, visible=True)
            except ToolError:
                _check_stop(stop)
            opened = any(x.element_info.name == "ADB Shell" and
                         x.element_info.control_type == "TabItem" and x.is_visible()
                         for x in _descendants(window))
            if opened:
                break
            if progress is not None:
                progress("Terminal chưa mở ADB Shell · thử nút dự phòng trên cùng máy")
        if not opened:
            raise ToolError(f"{name}: đã thử {len(groups)} nút Terminal nhưng ADB Shell chưa hiện")
    _check_stop(stop)
    tab = _one(window, "ADB Shell", "TabItem")
    try:
        tab.iface_selection_item.Select()
    except Exception as exc:
        raise ToolError("Không thể mở ADB Shell bằng UIA Selection") from exc
    _wait_for(window, "SHELL: On", "Text", seconds=20, stop=stop, progress=progress, visible=True)
    _check_stop(stop)
    ports = {int(match.group(1)) for x in _descendants(window)
             if x.element_info.control_type == "Text"
             if (match := re.fullmatch(r"localhost:(\d{1,5})", x.element_info.name))}
    if len(ports) != 1:
        raise ToolError("ADB Shell hoạt động nhưng không xác định được cổng tunnel duy nhất")
    return {"profile_name": name, "device_id": device_id,
            "adb_shell_open": True, "serial": f"127.0.0.1:{ports.pop()}",
            "window_handle": window.handle,
            "mouse_or_focus_used": False}


def _phone_window(name: str, device_id: str, *, seconds: float = 20,
                  handle: int | None = None, stop=None, progress=None):
    """Resolve exact title and process before constructing one UIA wrapper."""
    from pywinauto import Desktop
    import win32gui
    import win32process

    expected_title = f"{name} - {device_id}"
    expected_exe = str(_swarmote_exe()).casefold()
    until = time.monotonic() + seconds
    report = _progress_reporter(progress, f"Đang tìm cửa sổ {name}")
    while time.monotonic() < until:
        _check_stop(stop)
        report()
        matches = []

        def collect(candidate, _extra):
            try:
                if win32gui.GetWindowText(candidate) != expected_title:
                    return
                if handle is not None and candidate != handle:
                    return
                _, pid = win32process.GetWindowThreadProcessId(candidate)
                if psutil.Process(pid).exe().casefold() == expected_exe:
                    matches.append(candidate)
            except (psutil.NoSuchProcess, psutil.AccessDenied, OSError):
                return

        # Win32 metadata first: never ask every other app's UIA provider to
        # respond for each phone, and never trust a reused HWND over identity.
        win32gui.EnumWindows(collect, None)
        _check_stop(stop)
        if len(matches) == 1:
            return Desktop(backend="uia").window(handle=matches[0]).wrapper_object()
        if len(matches) > 1:
            raise ToolError(f"Có nhiều cửa sổ điện thoại khớp {name}; đã dừng")
        _pause(0.25, stop)
    raise ToolError(f"Không thấy cửa sổ điện thoại {name} sau {seconds:g} giây; kiểm tra máy còn mở trong Swarmote")


def show_apps(name: str, device_id: str | None = None, *, stop=None, progress=None):
    """Keep the Swarmote phone on its Apps tab after using the ADB tunnel."""
    _check_stop(stop)
    if not device_id:
        status = profile_status(name)
        device_id = status["device_id"]
    if not device_id:
        raise ToolError(f"{name}: chưa có Device ID để mở Apps")
    window = _phone_window(name, device_id, seconds=60, stop=stop, progress=progress)
    until = time.monotonic() + 120
    last_seen = "chưa có nút Apps"
    report = _progress_reporter(progress, "Đang mở Apps / App Store")
    while time.monotonic() < until:
        _check_stop(stop)
        report()
        controls = _descendants(window)
        if any(x.element_info.name == "App Store" and x.element_info.control_type == "TabItem"
               and x.is_visible() for x in controls):
            return window
        all_labels = [x for x in controls if x.element_info.name == "Apps"
                      and x.element_info.control_type == "Text"]
        visible_labels = [x for x in all_labels if x.is_visible()]
        labels = visible_labels
        if len(labels) == 1:
            try:
                _check_stop(stop)
                labels[0].parent().invoke()
                _wait_for(window, "App Store", "TabItem", seconds=10,
                          stop=stop, progress=progress, visible=True)
                return window
            except Exception as exc:
                _check_stop(stop)
                last_seen = f"Apps có trong UIA nhưng chưa mở được: {type(exc).__name__}"
                if progress is not None:
                    progress(last_seen)
        else:
            last_seen = f"UIA thấy {len(all_labels)} nhãn Apps"
        _pause(0.25, stop)
    raise ToolError(f"{name}: Apps chưa sẵn sàng sau 120 giây ({last_seen})")


def collapse_apps_panel(name: str, device_id: str, *, stop=None) -> bool:
    """Close the App Store side panel once after Amazon opens; leave a closed panel alone."""
    _check_stop(stop)
    window = _phone_window(name, device_id, seconds=10, stop=stop)
    controls = _descendants(window)
    if not any(item.element_info.name == "App Store" and
               item.element_info.control_type == "TabItem" and item.is_visible()
               for item in controls):
        return False
    apps = [item for item in controls if item.element_info.name == "Apps" and
            item.element_info.control_type == "Text" and item.is_visible()]
    if len(apps) != 1:
        raise ToolError(f"{name}: không xác định được duy nhất nút Apps để thu panel")
    _check_stop(stop)
    try:
        apps[0].parent().invoke()
    except Exception as exc:
        raise ToolError(f"{name}: chưa thu được panel Apps") from exc
    until = time.monotonic() + 3
    while time.monotonic() < until:
        _check_stop(stop)
        if not any(item.element_info.name == "App Store" and
                   item.element_info.control_type == "TabItem" and item.is_visible()
                   for item in _descendants(window)):
            return True
        _pause(0.2, stop)
    raise ToolError(f"{name}: đã bấm Apps nhưng panel App Store vẫn hiện")


def install_amazon(name: str, timeout: int = 180,
                   device_id: str | None = None, stop=None, progress=None) -> dict:
    """Open Apps immediately, search z, install Amazon, then verify over ADB."""
    from .cloud import CloudPhone, package_path, require_online
    from .core import AMAZON_PACKAGE

    def check_stop():
        if stop is not None and stop.is_set():
            raise ToolError("Đã dừng cài Amazon")

    check_stop()

    if device_id is None:
        status = profile_status(name)
        if status["state"] != "Running" or not status["device_id"]:
            raise ToolError("Profile cần Running và có Device ID trước khi cài Amazon")
        device_id = status["device_id"]
    window = show_apps(name, device_id, stop=stop, progress=progress)
    check_stop()
    wait_options = {"stop": stop, "progress": progress, "visible": True}
    _wait_for(window, "Enter content", "Edit", seconds=20, **wait_options)
    check_stop()
    if progress is not None:
        progress("Đang tìm Amazon Shopping trong App Store")
    _set_value(window, "Enter content", "Edit", "z")
    _wait_for(window, "Amazon Shopping", "Text", seconds=60, **wait_options)
    check_stop()
    items = _descendants(window)
    amazon = [x for x in items if x.element_info.name == "Amazon Shopping"
              and x.element_info.control_type == "Text" and x.is_visible()]
    if len(amazon) != 1:
        raise ToolError(f"Cần đúng một thẻ Amazon Shopping; thấy {len(amazon)}")
    bounds = amazon[0].rectangle()
    installs = [x for x in items if x.element_info.name in {"Install", "Installed", "Installing", "Downloading"}
                and x.element_info.control_type == "Button"
                and x.is_visible()
                and x.rectangle().left >= bounds.right
                and abs((x.rectangle().top + x.rectangle().bottom) -
                        (bounds.top + bounds.bottom)) < 85]
    installs.sort(key=lambda x: x.rectangle().left - bounds.right)
    if not installs or (len(installs) > 1 and
                        installs[0].rectangle().left == installs[1].rectangle().left):
        raise ToolError("Không xác định được nút cài đặt cùng thẻ Amazon")
    already_installed = installs[0].element_info.name == "Installed"
    if installs[0].element_info.name == "Install":
        if progress is not None:
            progress("Đang bấm Install Amazon Shopping")
        check_stop()
        try:
            installs[0].invoke()
        except Exception as exc:
            raise ToolError("Nút Install không hỗ trợ UIA Invoke; đã dừng để không chiếm chuột") from exc
    check_stop()
    shell = open_adb_shell(name, device_id, stop=stop, progress=progress)
    check_stop()
    show_apps(name, shell["device_id"], stop=stop, progress=progress)
    phone = CloudPhone(shell["serial"])
    require_online(phone)
    until = time.monotonic() + timeout
    report = _progress_reporter(progress, "Đang chờ Android xác nhận cài Amazon")
    while time.monotonic() < until:
        check_stop()
        report()
        if package_path(phone, AMAZON_PACKAGE):
            return {"profile_name": name, "amazon_package_installed": True,
                    "already_installed": already_installed, "source_verified": False}
        if stop is None:
            time.sleep(2)
        else:
            stop.wait(2)
    raise ToolError("Đã mở Amazon trong App Store nhưng Android chưa xác nhận cài đặt; kiểm tra máy trước khi thử lại")


def ready_for_registration(name: str) -> dict:
    """Start an existing Profile, install/open Amazon, reach the entry form."""
    from .cloud import CloudPhone, open_amazon
    from .registration import open_entry, status as registration_status

    profile = start_profile(name)
    installed = install_amazon(name)
    shell = open_adb_shell(name)
    phone = CloudPhone(shell["serial"])
    try:
        registration = registration_status(phone)
    except ToolError:
        registration = {"registration_entry": False}
    if not registration["registration_entry"]:
        open_amazon(phone)
        registration = open_entry(phone)
    return {"profile": profile, "amazon_package_installed": installed["amazon_package_installed"],
            "registration_entry": registration["registration_entry"],
            "identifier_field_found": registration["identifier_field_found"],
            "continue_pressed": False}
