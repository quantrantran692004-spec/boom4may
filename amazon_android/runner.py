"""Pipeline Profile creation with phone preparation and a Running-phone limit."""
from __future__ import annotations

import threading
import time

# Import on the caller thread; initialize each UIA worker explicitly as MTA.
import pythoncom
from collections import deque
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from typing import Callable, Mapping

from .cloud import CloudPhone, open_amazon
from .core import ToolError
from .home_menu import open_home_menu
from .profile_registry import ProfileRegistry
from .swarmote_desktop import (
    ProfileCreateNotSubmitted, ProfileManagerWindowError, ProfileNotFound,
    ProxyTestFailed, ProfileStartNotSubmitted,
    ProxyConfig, create_profile, install_amazon, ensure_manager_ready,
    open_adb_shell, profile_status, show_apps, collapse_apps_panel,
    start_profile, visible_profile_names,
)


@dataclass(frozen=True)
class AccountData:
    phone: str
    full_name: str
    password: str = field(repr=False)
    otp_url: str = field(repr=False)
    card: str = field(default="", repr=False)
    browser_otp: str = field(default="", repr=False)


@dataclass(frozen=True)
class RunJob:
    index: int
    batch_id: str
    proxy: ProxyConfig | None
    proxy_fallbacks: tuple[ProxyConfig, ...] = ()
    account: AccountData | None = field(default=None, repr=False)


Progress = Callable[[int, str, str, str | None], None]
MenuReady = Callable[[int, str, str, str], None]


def _start_and_confirm(name, device_id, stop):
    """A lost Start response is not proof the request failed. Never resend it."""
    if stop.is_set():
        raise ToolError('Đã dừng trước khi mở máy')
    try:
        return start_profile(name, wait=False)
    except Exception as original:
        for attempt in range(3):
            if stop.is_set():
                raise ToolError('Đã dừng khi xác nhận Start') from original
            try:
                state = profile_status(name)
            except ToolError:
                state = {}
            if state.get('device_id') not in (None, device_id):
                raise ToolError(f'{name}: Device ID đã đổi; không nhận kết quả Start') from original
            if state.get('device_id') == device_id and state.get('state') in {'Running', 'Starting'}:
                return state
            if attempt < 2:
                stop.wait(0.5)
        raise original


def _prepare_phone(job: RunJob, name: str, device_id: str,
                   registry: ProfileRegistry, emit: Progress,
                   stop: threading.Event,
                   menu_ready: MenuReady | None = None,
                   stop_after_step: threading.Event | None = None) -> str:
    """Operate only the phone window; the coordinator owns the Profiles window."""
    import pythoncom

    initialized = False
    try:
        pythoncom.CoInitializeEx(pythoncom.COINIT_MULTITHREADED)
        initialized = True
        def progress(message):
            emit(job.index, f"{message} · {name}", "running", name)

        def stop_here(message: str, stage: str | None = None) -> bool:
            if not stop.is_set() and stop_after_step is not None and stop_after_step.is_set():
                registry.mark(job.batch_id, job.index, "STOPPED", stage=stage)
                emit(job.index, f"Đã dừng riêng {name} · {message}", "stopped", name)
                return True
            return False

        if stop_here("chưa chuẩn bị máy"):
            return "stopped"
        if stop.is_set():
            registry.mark(job.batch_id, job.index, "STOPPED")
            emit(job.index, f"Đã dừng chuẩn bị {name}", "stopped", name)
            return "stopped"
        item = registry.get(job.batch_id, job.index)
        if item is None:
            raise ToolError("Không còn metadata của Profile")
        if item["stage"] != "APP_INSTALLED":
            emit(job.index, f"Đang tìm z và cài Amazon · {name}", "running", name)
            install_amazon(name, device_id=device_id, stop=stop, progress=progress)
            registry.mark(job.batch_id, job.index, "READY", stage="APP_INSTALLED")
        emit(job.index, f"Amazon đã cài trên {name}", "installed", name)
        if stop_here("sau khi cài Amazon"):
            return "stopped"
        if stop.is_set():
            registry.mark(job.batch_id, job.index, "STOPPED")
            emit(job.index, f"Đã dừng sau khi cài Amazon · {name}", "stopped", name)
            return "stopped"
        emit(job.index, f"Đang mở menu Amazon · {name}", "running", name)
        shell = open_adb_shell(name, device_id, stop=stop, progress=progress)
        if stop_here("sau khi nối ADB"):
            return "stopped"
        if stop.is_set():
            raise ToolError("Đã dừng chuẩn bị máy")
        show_apps(name, device_id, stop=stop, progress=progress)
        if stop_here("sau khi mở danh sách ứng dụng"):
            return "stopped"
        if stop.is_set():
            raise ToolError("Đã dừng chuẩn bị máy")
        phone = CloudPhone(shell["serial"])
        open_amazon(phone)
        if stop_here("sau khi mở Amazon"):
            return "stopped"
        if stop.is_set():
            raise ToolError("Đã dừng chuẩn bị máy")
        collapse_apps_panel(name, device_id, stop=stop)
        if stop_here("sau khi thu gọn ứng dụng"):
            return "stopped"
        menu = open_home_menu(phone, stop=stop)
        if stop.is_set():
            raise ToolError("Đã dừng chuẩn bị máy")
        if menu["stage"] != "HOME_MENU_OPEN":
            raise ToolError("Amazon chưa xác nhận menu ba gạch")
        if menu_ready is not None:
            menu_ready(job.index, name, device_id, phone.serial)
        if stop_here("sau khi mở menu ba gạch", stage="MENU_OPEN"):
            return "stopped"
        registry.mark(job.batch_id, job.index, "DONE", stage="MENU_OPEN")
        message = (f"Đã mở menu ba gạch · {name}" if job.account is not None
                   else f"Đã mở menu ba gạch · {name}; chưa có dữ liệu Amazon")
        emit(job.index, message, "done", name)
        return "done"
    except Exception as exc:
        if not stop.is_set() and stop_after_step is not None and stop_after_step.is_set():
            registry.mark(job.batch_id, job.index, "STOPPED")
            emit(job.index, f"Đã dừng riêng {name} tại bước đang lỗi", "stopped", name)
            return "stopped"
        if stop.is_set():
            registry.mark(job.batch_id, job.index, "STOPPED")
            emit(job.index, f"Đã dừng chuẩn bị {name}", "stopped", name)
            return "stopped"
        registry.mark(job.batch_id, job.index, "ERROR",
                      error=str(exc) if isinstance(exc, ToolError) else type(exc).__name__)
        emit(job.index, f"Dừng tại {name}: {exc}", "error", name)
        return "error"
    finally:
        if initialized:
            pythoncom.CoUninitialize()


def run_batch(jobs: list[RunJob], registry: ProfileRegistry,
              emit: Progress, stop: threading.Event, *,
              start_group_size: int = 1,
              hide_profile_creation: bool = False,
              menu_ready: MenuReady | None = None,
              stop_after_step: Mapping[int, threading.Event] | None = None) -> dict[str, int]:
    """Create serially, prepare phones concurrently, and fill freed Running slots."""
    if not 1 <= start_group_size <= 12:
        raise ToolError("Giới hạn máy Running phải từ 1 đến 12")
    summary = {"created": 0, "menu_open": 0, "error": 0, "stopped": 0}
    waiting: deque[tuple[RunJob, str, str]] = deque()
    active: dict[str, dict] = {}  # Starting phones reserve a slot until Running.
    futures = []
    future_by_name = {}
    start_blocked = False
    creation_blocked = False
    slot_warning_sent = False
    start_retry_since: dict[str, float] = {}
    try:
        visible_names = visible_profile_names()
    except ToolError:
        def startup_progress(message):
            for job in jobs:
                emit(job.index, message, "running", None)
        ensure_manager_ready(stop=stop, progress=startup_progress)
        visible_names = visible_profile_names()
    proxy_fallbacks = deque(next((job.proxy_fallbacks for job in jobs
                                  if job.proxy_fallbacks), ()))

    def requested(job: RunJob) -> bool:
        event = stop_after_step.get(job.index) if stop_after_step is not None else None
        return event is not None and event.is_set()

    def stop_job(job: RunJob, name: str | None, detail: str) -> None:
        if registry.get(job.batch_id, job.index) is not None:
            registry.mark(job.batch_id, job.index, "STOPPED")
        emit(job.index, f"Đã dừng riêng q{job.index + 1} · {detail}", "stopped", name)
        summary["stopped"] += 1

    def visible_lookup(name: str) -> dict:
        if name in visible_names:
            return {"profile_name": name}
        return profile_status(name)

    for batch_id in {job.batch_id for job in jobs}:
        for item in registry.items_for_batch(batch_id):
            if not item.get("device_id"):
                continue
            try:
                state = profile_status(item["name"])
            except ProfileNotFound:
                continue
            if state.get("device_id") != item["device_id"]:
                raise ToolError(f"{item['name']}: Device ID đã đổi; không thể kiểm tra giới hạn máy")
            if state["state"] == "Running":
                active[item["name"]] = {"device_id": item["device_id"],
                                        "seen_running": True}

    with ThreadPoolExecutor(max_workers=12, thread_name_prefix="swarmote-phone") as pool:
        def refresh_slots() -> None:
            nonlocal slot_warning_sent
            status_unknown = False
            for name in list(active):
                try:
                    state = profile_status(name)
                except ToolError:
                    status_unknown = True
                    continue  # Unknown is not proof that a paid phone has closed.
                if state.get("device_id") != active[name]["device_id"]:
                    continue
                if state["state"] == "Running":
                    active[name]["seen_running"] = True
                elif state["state"] == "Offline":
                    finished = future_by_name.get(name)
                    if active[name]["seen_running"] or (finished and finished.done()):
                        del active[name]
            if waiting and status_unknown and not slot_warning_sent:
                job, name, _device_id = waiting[0]
                emit(job.index, f"{name} đang đợi; mở trang Profiles để tool thấy máy đã tắt",
                     "queued", name)
                slot_warning_sent = True
            elif not status_unknown:
                slot_warning_sent = False

        def fill_slots() -> None:
            nonlocal start_blocked
            if waiting:
                remaining = deque()
                for job, name, device_id in waiting:
                    if requested(job):
                        stop_job(job, name, "chưa mở máy")
                    else:
                        remaining.append((job, name, device_id))
                waiting.clear()
                waiting.extend(remaining)
            if start_blocked or stop.is_set():
                return
            refresh_slots()
            while waiting and len(active) < start_group_size and not stop.is_set():
                job, name, device_id = waiting[0]
                if requested(job):
                    waiting.popleft()
                    stop_job(job, name, "chưa mở máy")
                    continue
                emit(job.index, f"Đang mở máy {name}", "running", name)
                try:
                    started = _start_and_confirm(name, device_id, stop)
                    if (started["state"] not in {"Starting", "Running"} or
                            started.get("device_id") != device_id):
                        raise ToolError(f"{name}: Start chưa xác nhận đúng Device ID")
                except ProfileStartNotSubmitted as exc:
                    if requested(job):
                        waiting.popleft()
                        stop_job(job, name, "trước khi mở máy")
                        continue
                    first = start_retry_since.setdefault(name, time.monotonic())
                    if time.monotonic() - first < 60 and not stop.is_set():
                        emit(job.index,
                             f"{name} đang đợi nút Start sẵn sàng; tool tự thử lại",
                             "queued", name)
                        return
                    waiting.popleft()
                    registry.mark(job.batch_id, job.index, "ERROR", error=str(exc))
                    emit(job.index, f"Không mở được {name} sau khi đợi Start: {exc}",
                         "error", name)
                    summary["error"] += 1
                    start_blocked = True
                    return
                except Exception as exc:
                    if requested(job):
                        waiting.popleft()
                        stop_job(job, name, "khi xác nhận mở máy")
                        continue
                    waiting.popleft()
                    registry.mark(job.batch_id, job.index, "ERROR",
                                  error=str(exc) if isinstance(exc, ToolError) else type(exc).__name__)
                    emit(job.index, f"Không xác nhận được Start {name}: {exc}", "error", name)
                    summary["error"] += 1
                    start_blocked = True
                    return
                waiting.popleft()
                start_retry_since.pop(name, None)
                active[name] = {"device_id": device_id,
                                "seen_running": started["state"] == "Running"}
                if requested(job):
                    stop_job(job, name, "sau khi mở máy")
                    continue
                item = registry.get(job.batch_id, job.index)
                if item and item["stage"] != "APP_INSTALLED":
                    registry.mark(job.batch_id, job.index, "READY", stage="STARTED")
                emit(job.index, f"Đã gửi Start · {name} đang mở", "started", name)
                future = pool.submit(_prepare_phone, job, name, device_id,
                                     registry, emit, stop, menu_ready,
                                     stop_after_step.get(job.index) if stop_after_step else None)
                futures.append(future)
                future_by_name[name] = future

        for position, job in enumerate(jobs):
            if stop.is_set():
                for remaining in jobs[position:]:
                    emit(remaining.index, "Đã dừng trước khi tạo Profile", "stopped", None)
                summary["stopped"] += len(jobs) - position
                break
            if requested(job):
                stop_job(job, None, "trước khi tạo Profile")
                continue
            item = None
            try:
                item = registry.reserve(job.batch_id, job.index, visible_lookup)
                name = item["name"]
                emit(job.index, f"Đang kiểm tra {name}", "running", name)
                if item["state"] == "UNCERTAIN":
                    raise ToolError(f"{name}: kết quả tạo chưa chắc chắn; cần kiểm tra thủ công")
                if item["stage"] == "RESERVED":
                    if job.proxy is None:
                        raise ToolError(f"{name}: cần proxy để tạo Profile chưa có")
                    if name in visible_names:
                        raise ToolError(f"{name} đã hiện trong Swarmote; chưa xác minh proxy của mẻ này")
                    proxy = job.proxy
                    while True:
                        registry.mark(job.batch_id, job.index, "RUNNING", stage="CREATING")
                        emit(job.index, f"Đang Test proxy và tạo {name}", "running", name)
                        try:
                            if hide_profile_creation:
                                create_profile(name, proxy, hide_window=True)
                            else:
                                create_profile(name, proxy)
                            found = profile_status(name)
                            break
                        except ProxyTestFailed as exc:
                            registry.mark(job.batch_id, job.index, "ERROR", stage="RESERVED",
                                          error=str(exc))
                            if requested(job):
                                raise
                            if not proxy_fallbacks:
                                raise
                            proxy = proxy_fallbacks.popleft()
                            emit(job.index,
                                 f"Proxy không đạt; thử proxy dự phòng còn {len(proxy_fallbacks)} · {name}",
                                 "running", name)
                        except ProfileCreateNotSubmitted as exc:
                            registry.mark(job.batch_id, job.index, "ERROR", stage="RESERVED",
                                          error=str(exc))
                            if isinstance(exc.__cause__, ProfileManagerWindowError):
                                creation_blocked = True
                            raise
                        except Exception as exc:
                            registry.mark(job.batch_id, job.index, "UNCERTAIN",
                                          error=str(exc) if isinstance(exc, ToolError) else type(exc).__name__)
                            raise
                    registry.mark(job.batch_id, job.index, "READY",
                                  device_id=found.get("device_id"), stage="PROFILE_CONFIRMED")
                    visible_names.add(name)
                    summary["created"] += 1
                else:
                    found = profile_status(name)
                    if item["stage"] == "CREATING":
                        raise ToolError(f"{name} đã tồn tại nhưng chưa xác minh proxy của mẻ này")
                    if item.get("device_id") and found.get("device_id") != item["device_id"]:
                        raise ToolError(f"{name}: Device ID đã đổi; dừng để tránh dùng nhầm máy")
                device_id = found.get("device_id")
                if not device_id or found["state"] not in {"Offline", "Running"}:
                    raise ToolError(f"{name}: chưa xác nhận Device ID hoặc trạng thái Profile")
                if requested(job):
                    stop_job(job, name, "sau khi xác nhận Profile")
                    continue
                if item["stage"] == "MENU_OPEN":
                    if found["state"] != "Running":
                        emit(job.index,
                             f"{name} đã tới menu nhưng đang Offline; Start máy rồi bấm Tiếp tục",
                             "stopped", name)
                        summary["stopped"] += 1
                        continue
                    active[name] = {"device_id": device_id, "seen_running": True}
                    if menu_ready is not None and job.account is not None:
                        shell = open_adb_shell(name, device_id, stop=stop,
                            progress=lambda message, slot=job.index, profile=name:
                                emit(slot, f"{message} · {profile}", "running", profile))
                        if requested(job):
                            stop_job(job, name, "sau khi nối lại ADB")
                            continue
                        menu_ready(job.index, name, device_id, shell["serial"])
                    message = (f"Đã mở menu ba gạch · {name}" if job.account is not None
                               else f"Đã mở menu ba gạch · {name}; chưa có dữ liệu Amazon")
                    emit(job.index, message, "done", name)
                    summary["menu_open"] += 1
                    continue
                emit(job.index, f"Đã xác nhận Profile {name}", "created", name)
                if found["state"] == "Running":
                    active[name] = {"device_id": device_id, "seen_running": True}
                    future = pool.submit(_prepare_phone, job, name, device_id,
                                         registry, emit, stop, menu_ready,
                                         stop_after_step.get(job.index) if stop_after_step else None)
                    futures.append(future)
                    future_by_name[name] = future
                else:
                    waiting.append((job, name, device_id))
                    fill_slots()
                    if any(queued[1] == name for queued in waiting):
                        emit(job.index, f"{name} đã tạo · chờ chỗ máy Running trống", "queued", name)
            except Exception as exc:
                current = registry.get(job.batch_id, job.index) if item else None
                if requested(job) and (current is None or current["state"] != "UNCERTAIN"):
                    stop_job(job, item["name"] if item else None,
                             "sau bước tạo Profile")
                    continue
                event_state = "error"
                if item:
                    if current and current["state"] != "UNCERTAIN":
                        registry.mark(job.batch_id, job.index, "ERROR",
                                      error=str(exc) if isinstance(exc, ToolError) else type(exc).__name__)
                    elif current and current["state"] == "UNCERTAIN":
                        event_state = "uncertain"
                summary["error"] += 1
                emit(job.index, f"Dừng ở bước tạo: {exc}", event_state,
                     item["name"] if item else None)
                if creation_blocked:
                    for remaining in jobs[position + 1:]:
                        emit(remaining.index,
                             "Chưa tạo: cửa sổ quản lý Swarmote chưa xác định được",
                             "stopped", None)
                    summary["stopped"] += len(jobs) - position - 1
                    break

        while waiting and not stop.is_set() and not start_blocked:
            fill_slots()
            if waiting:
                stop.wait(2)

        if waiting:
            reason = ("Đã dừng trước khi mở máy" if stop.is_set() else
                      "Đã dừng vì một máy Start lỗi")
            for job, name, _device_id in waiting:
                registry.mark(job.batch_id, job.index, "STOPPED")
                emit(job.index, f"{reason} · {name}", "stopped", name)
                summary["stopped"] += 1

        for future in as_completed(futures):
            outcome = future.result()
            summary["menu_open" if outcome == "done" else outcome] += 1
    return summary
