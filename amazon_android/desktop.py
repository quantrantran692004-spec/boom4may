"""Self-service Swarmote desk. Input values stay in memory for this session."""
from __future__ import annotations

import queue
import threading
import time
import tkinter as tk
import webbrowser
from dataclasses import replace
from tkinter import messagebox, simpledialog

import customtkinter as ctk
from .desktop_scroll import SmoothScrollableFrame

from .bulk_input import MAX_PROFILES, parse_bulk_payload, parse_column, parse_records, validate_card
from .batch_state import BatchDraft
from .core import ToolError
from .otp import extract_otp, otp_token, validate_otp_url
from .post_menu import PostMenuSession, PostMenuStep
from .account_flow import (
    resume_common_index, route_list_menu, verify_menu_open,
)
from .random_prefix import build_random_steps
from .windows_identity import set_process_identity, set_tk_icon, set_window_identity
from .cloud import CloudPhone
from .profile_registry import ProfileRegistry
from .registration import PHONE
from .runner import AccountData, RunJob, run_batch, retry_preparation
from .settings import CHANGE_US_FROM_START, AppSettings, load_settings, save_settings
from .change_us_flow import build_change_us_steps
from .swarmote_desktop import (
    ProxyConfig, open_adb_shell, profile_status,
)


from .desktop_theme import (
    BG, HEADER, FOOTER, SURFACE, INPUT, WHITE, INK, BODY, MUTED, PLACEHOLDER,
    BLUE, BLUE_HOVER, PALE, BORDER, FIELD_BORDER, SECONDARY, SECONDARY_HOVER,
    GREEN, RED, ROW_ALT, ROW_HOVER, TABLE_HEADER, TABLE_HEADER_TEXT,
    DISABLED_BG, DISABLED_TEXT, CONTINUE_BG, CONTINUE_HOVER, STOP_BG, STOP_HOVER,
    SCROLLBAR, SCROLLBAR_HOVER, ICON_SECTION, ICON_TABLE, ICON_STATUS,
    LABEL_ICONS, Button, Entry, icon, state_style, status_title, ui_font,
    HEADER_BORDER, HEADER_CONTROL, HEADER_TEXT, HEADER_WAVES, ICON_DEFAULT,
    TableText, StatusCell, MachineCell, HeaderWave, FooterNote,
    startup_geometry,
    ROW_BORDER, ROW_SELECTED_BORDER, ROW_INACTIVE,
    PROCESSING, PROGRESS_TEXT,
    FOOTER_BORDER, FOOTER_TEXT, LOGO_BG, UTILITY_TEXT,
)

BULK = (
    ("proxy", "Proxy", "host:port:user:password", "Proxy dư tự dùng thay proxy lỗi"),
    ("account", "Thông tin Amazon", "SĐT | Mật khẩu | Tên | URL OTP (thẻ tùy chọn)", "Dán 1 lần: tối đa 12 hàng"),
)

FIELD_KEYS = (
    "host", "port", "username", "proxy_password",
    "full_name", "phone", "amazon_password", "profile_name", "card", "otp_url",
)
REPAIR_KEYS = tuple(key for key in FIELD_KEYS if key != "profile_name")

POST_MENU_STEP_FACTORIES = {index: build_random_steps for index in range(12)}


def _automatic_resume_slots(items: list[dict], start_group_size: int = 12) -> list[int]:
    """Resume queued work after a restart; errors require an explicit Continue."""
    return [item["slot"] for item in items
            if item.get("state") in {"READY", "RUNNING"}
            and item.get("stage") != "MENU_OPEN"]


class Window:
    def __init__(self) -> None:
        set_process_identity()
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        icon.cache_clear()
        self.root = ctk.CTk(fg_color=BG)
        self.root.title("Swarmote · Amazon workspace")
        set_tk_icon(self.root)
        scale = self.root._get_window_scaling()
        available_width = self.root.winfo_screenwidth() / scale
        available_height = self.root.winfo_screenheight() / scale
        initial_width, initial_height, initial_x, initial_y = startup_geometry(
            self.root.winfo_screenwidth(), self.root.winfo_screenheight(), scale)
        self.root.minsize(
            min(1100, max(760, initial_width - 40)),
            min(600, max(380, initial_height - 30)),
        )
        self.root.geometry(f"{initial_width}x{initial_height}+{initial_x}+{initial_y}")
        self.root.update_idletasks()
        set_window_identity(self.root.winfo_id())

        self.count = tk.StringVar(value="1")
        try:
            self.settings = load_settings()
            self.settings_error = ""
        except ToolError as exc:
            self.settings = AppSettings()
            self.settings_error = str(exc)
        self.draft = BatchDraft()
        self.jobs: dict[int, RunJob] = {}
        self.post_menu_step_factories = dict(POST_MENU_STEP_FACTORIES)
        self.post_menu_steps: dict[int, tuple[PostMenuStep, ...]] = {}
        self.post_menu_sessions: dict[int, PostMenuSession] = {}
        self.post_menu_stops: dict[int, threading.Event] = {}
        self.phone_stop_after_step: dict[int, threading.Event] = {}
        self.post_menu_resume_after_stop: set[int] = set()
        self.manual_slots: set[tuple[str, int]] = set()
        self.post_menu_workers: dict[int, threading.Thread] = {}
        self.menu_opened_at: dict[int, float] = {}
        self.phone_serials: dict[int, str] = {}
        self.proxy_postal_prefixes: dict[int, str] = {}
        self.attach_in_progress = False
        self.attaching_index = 0
        self.attach_events: queue.Queue[tuple[str, AccountData | None, str | None]] = queue.Queue()
        self.proxy_fallbacks = []
        try:
            self.registry = ProfileRegistry(persistent=False)
            self.registry_error = ""
        except ToolError as exc:
            self.registry = None
            self.registry_error = str(exc)
        self.restored_batch = None  # Every launch starts a fresh 1–12 workspace.
        self.selected = 0
        self.running = False
        self.batch_worker = None
        self.attach_worker = None
        self._draining_workers = []
        self._pending_retries: set[int] = set()
        self._edited_locked_rows: set[int] = set()
        self.preparation_retry_workers: dict[int, threading.Thread] = {}
        self.cancel = threading.Event()
        self.events: queue.Queue[tuple[int, str, str, str | None]] = queue.Queue()
        self.otp_events: queue.Queue[tuple[str, int, str]] = queue.Queue()
        self.otp_status_events: queue.Queue[tuple[str, int, str]] = queue.Queue()
        self.values = [
            {key: tk.StringVar(value="") for key in FIELD_KEYS}
            for _ in range(MAX_PROFILES)
        ]
        predicted = (self.registry.preview_names(MAX_PROFILES) if self.registry else
                     [f"q{i}" for i in range(1, MAX_PROFILES + 1)])
        for index, row in enumerate(self.values):
            row["profile_name"].set(predicted[index])
        self.status = [("Chưa chạy", "idle") for _ in range(MAX_PROFILES)]
        self.otp_status = ["Chưa yêu cầu mã" for _ in range(MAX_PROFILES)]
        self.otp_codes = ["" for _ in range(MAX_PROFILES)]
        if self.restored_batch:
            batch_id, items = self.restored_batch
            self.count.set(str(len(items)))
            self.draft.batch_id = batch_id
            self.draft.proxy_count = len(items)
            self.draft.locked = True
            for item in items:
                index = item["slot"]
                self.jobs[index] = RunJob(index, batch_id, None)
                self.values[index]["profile_name"].set(item["name"])
                if item["stage"] == "MENU_OPEN":
                    self.status[index] = (f"{item['name']} đã tới menu", "done")
                elif item["state"] == "ERROR":
                    self.status[index] = (
                        f"Dừng tại {item['name']}: {item.get('last_error') or 'cần kiểm tra lại'}",
                        "error",
                    )
                elif item["state"] == "STOPPED":
                    self.status[index] = (f"{item['name']} đã dừng", "stopped")
                else:
                    self.status[index] = (
                        f"{item['name']} đã tạo · đang chờ tiếp tục", "queued",
                    )
        self.row_buttons: list[ctk.CTkButton] = []
        self.row_stop_buttons: list[ctk.CTkButton] = []
        self.bulk_boxes: dict[str, ctk.CTkEntry] = {}
        self.bulk_feedback: dict[str, ctk.CTkLabel] = {}
        self.detail_entries: dict[str, ctk.CTkEntry] = {}
        self.table_rows: list[dict[str, tk.Label]] = []
        self._display_options: dict[object, dict[str, object]] = {}
        self._editing_display_state: tuple[str, str, int | None] | None = None
        self._refresh_after_id: str | None = None

        self._build()
        if self.restored_batch:
            self._set_editing(False)
        for index, row in enumerate(self.values):
            for key, value in row.items():
                value.trace_add("write", lambda *_, i=index, k=key:
                                self._on_row_value_changed(i, k))
        self._refresh_devices()
        self._select(0)
        if self.registry_error:
            self.run_note.configure(text=self.registry_error, text_color=RED)
        elif self.settings_error:
            self.run_note.configure(text=self.settings_error, text_color=RED)
        elif self.restored_batch:
            self.run_note.configure(text="Đã khôi phục mẻ đang chờ từ Swarmote",
                                    text_color=BLUE)
        self.root.after(150, self._poll)
        if self.restored_batch:
            self.root.after(450, self._resume_restored)

    def _label(self, parent, text: str, size: int = 13, *,
               color: str = MUTED, weight: str = "normal", **kwargs):
        name = LABEL_ICONS.get(text)
        # The existing half-width password label has no spare icon space at
        # the minimum window size; preserve its text and field geometry.
        if text == "Mật khẩu Amazon":
            name = None
        if name and "image" not in kwargs:
            kwargs.update(image=icon(name, ICON_DEFAULT, ICON_TABLE if text.isupper() else
                                     ICON_SECTION if size >= 18 else ICON_STATUS, gap=6),
                          compound="left", padx=0)
        if text != "Swarmote" and size < 18:
            weight = "normal"
        if text != "Swarmote" and (size >= 18 or text.startswith(
                ("Dán hàng Amazon", "Thông tin Amazon riêng", "Dán 1–12 proxy"))):
            weight = "semibold"
        return ctk.CTkLabel(
            parent, text=text, text_color=color,
            font=ui_font(size, weight),
            **kwargs,
        )

    def _configure_display(self, widget, **options) -> None:
        """Avoid redrawing unchanged CustomTkinter canvases during status updates."""
        cache = getattr(self, "_display_options", None)
        if cache is None:
            cache = self._display_options = {}
        previous = cache.setdefault(widget, {})
        changed = {key: value for key, value in options.items()
                   if key not in previous or previous[key] != value}
        if changed:
            widget.configure(**changed)
            previous.update(changed)

    def _build(self) -> None:
        header = HeaderWave(self.root, height=64, border_width=0)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Frame(header, bg=HEADER_BORDER, height=1).place(
            relx=0, rely=1, relwidth=1, anchor="sw")
        self._label(header, "", 20, image=icon("layers-2", WHITE, 24),
                    fg_color=LOGO_BG, corner_radius=8, width=40, height=40).pack(
                        side="left", padx=(18, 0))
        self._label(header, "Swarmote", 22,
                    color=INK, weight="bold").pack(side="left", padx=(12, 26))
        ctk.CTkFrame(header, width=1, height=26, fg_color=HEADER_BORDER).pack(
            side="left", padx=(0, 26))
        self._label(header, "Số máy", 14,
                    color=INK, weight="bold").pack(side="left")
        self.count_menu = ctk.CTkOptionMenu(
            header, values=[str(i) for i in range(1, MAX_PROFILES + 1)],
            variable=self.count, command=lambda _: self._refresh_devices(),
            width=70, height=34, corner_radius=8,
            fg_color=SURFACE, button_color=SURFACE,
            button_hover_color=SECONDARY_HOVER, text_color=HEADER_TEXT,
            dropdown_fg_color=SURFACE, dropdown_text_color=BODY,
            text_color_disabled=DISABLED_TEXT,
            font=ctk.CTkFont("Segoe UI", 14, weight="bold"),
        )
        self.count_menu.pack(side="left", padx=10)
        self.settings_button = Button(
            header, text="", width=40, height=38,
            icon_name="settings", role="settings", accessible_name="Cài đặt",
            bg_color=HEADER_WAVES[-1],
            corner_radius=8, fg_color=SECONDARY, hover_color=SECONDARY_HOVER,
            border_width=1, border_color=BORDER, text_color=INK,
            font=ctk.CTkFont("Segoe UI Symbol", 20),
            command=self._open_settings,
        )
        self.settings_button.pack(side="right", padx=18)

        shell = ctk.CTkFrame(self.root, fg_color="transparent")
        shell.pack(fill="both", expand=True, padx=12, pady=12)
        shell.grid_columnconfigure(0, weight=1)
        shell.grid_rowconfigure(0, weight=1)
        work_area = ctk.CTkFrame(shell, fg_color="transparent")
        work_area.grid(row=0, column=0, sticky="nsew")
        work_area.grid_columnconfigure(0, weight=7, minsize=600)
        work_area.grid_columnconfigure(1, weight=4, minsize=350)
        work_area.grid_rowconfigure(0, weight=1)
        self.main = SmoothScrollableFrame(work_area, fg_color="transparent",
                                            corner_radius=0, scrollbar_button_color=SCROLLBAR,
                                            scrollbar_button_hover_color=SCROLLBAR_HOVER)
        self.main.grid(row=0, column=0, sticky="nsew")
        self.main.grid_columnconfigure(0, weight=1)
        self.detail_panel = SmoothScrollableFrame(
            work_area, fg_color="transparent", corner_radius=0,
            scrollbar_button_color=SCROLLBAR, scrollbar_button_hover_color=SCROLLBAR_HOVER,
        )
        self.detail_panel.grid(row=0, column=1, sticky="nsew", padx=(12, 0))
        self.detail_panel.grid_columnconfigure(0, weight=1)
        for panel in (self.main, self.detail_panel):
            panel._scrollbar.configure(width=16, border_spacing=4,
                                       corner_radius=8, fg_color=BG)
        self._build_main()
        self._build_actions(work_area)
        self.main._parent_canvas.bind("<Configure>", self._fit_table_columns, add="+")
        self.detail_panel._parent_canvas.bind("<Configure>", self._fit_detail_text, add="+")

    def _build_main(self) -> None:
        bulk_card = ctk.CTkFrame(self.main, fg_color=SURFACE, corner_radius=14,
                                 border_width=1, border_color=BORDER)
        self.bulk_card = bulk_card
        bulk_card.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        bulk_card.grid_columnconfigure(1, weight=1)
        self._label(bulk_card, "Dán dữ liệu", 20,
                    color=INK, weight="bold").grid(
                        row=0, column=0, columnspan=2, sticky="w",
                        padx=20, pady=(14, 6))
        for index, (kind, title, placeholder, hint) in enumerate(BULK):
            self._bulk_row(bulk_card, kind, title, placeholder, hint,
                           index + 1)
        self.validation_label = self._label(bulk_card, "Cần dán proxy để chạy", 15)
        self.validation_label.grid(row=3, column=0, columnspan=4,
                                   sticky="w", padx=20, pady=(4, 12))

        self._build_preview_table()

        detail_card = ctk.CTkFrame(self.detail_panel, fg_color=SURFACE, corner_radius=14,
                                   border_width=1, border_color=BORDER)
        detail_card.grid(row=0, column=0, sticky="ew", pady=(2, 0))
        detail_card.grid_columnconfigure((0, 1), weight=1, uniform="detail")
        title_row = ctk.CTkFrame(detail_card, fg_color="transparent")
        title_row.grid(row=0, column=0, columnspan=2, sticky="ew",
                       padx=22, pady=(20, 6))
        self.detail_title = self._label(title_row, "Máy 1", 20,
                                        color=INK, weight="bold",
                                        image=icon("smartphone", UTILITY_TEXT, 22, gap=8),
                                        compound="left")
        self.detail_title.pack(side="left")
        self.detail_profile_label = self._label(title_row, "q1", 14,
            color=BLUE, weight="semibold", fg_color=HEADER_CONTROL, corner_radius=6,
            width=44, height=28)
        self.detail_profile_label.pack(side="right")
        self.progress_row = progress_row = ctk.CTkFrame(detail_card, fg_color="transparent", corner_radius=0)
        progress_row.grid(row=1, column=0, columnspan=2, sticky="ew",
                          padx=20, pady=(0, 12))
        self.status_marker = self._label(progress_row, "", 18, color=BLUE,
                                          image=icon("clock", MUTED, ICON_STATUS))
        self.status_marker.pack(side="left", anchor="n", padx=(0, 8), pady=(4, 0))
        progress_text = ctk.CTkFrame(progress_row, fg_color="transparent")
        progress_text.pack(side="left", fill="x", expand=True)
        self.detail_status = self._label(
            progress_text, "Chưa chạy", 16, color=INK,
            wraplength=305, justify="left", anchor="w")
        self.detail_status.configure(font=ui_font(16, "semibold"))
        self.detail_status.pack(fill="x")
        self.detail_description = self._label(
            progress_text, "", 14, color=MUTED,
            wraplength=305, justify="left", anchor="w")
        self.detail_description.pack(fill="x", pady=(2, 0))
        self._progress_detail_font = ui_font(17, "semibold")
        self._secondary_detail_font = ui_font(15)

        def section_heading(text, row, symbol, size=16):
            section = ctk.CTkFrame(detail_card, fg_color="transparent")
            section.grid(row=row, column=0, columnspan=2, sticky="ew", padx=20)
            ctk.CTkFrame(section, fg_color=BORDER, height=1, corner_radius=0).pack(
                fill="x", pady=(0, 8))
            label = self._label(section, text, size, color=INK,
                image=icon(symbol, UTILITY_TEXT, ICON_STATUS, gap=8), compound="left")
            label.configure(font=ui_font(size, "semibold"))
            label.pack(fill="x", pady=(0, 2))
            return label

        self.account_detail_heading = section_heading(
            "Thông tin Amazon riêng · Máy 1", 9, "user-round", 17)
        self.proxy_paste_heading = section_heading(
            "Dán 1–12 proxy để tự điền", 3, "globe")
        self.proxy_line = Entry(
            detail_card, placeholder_text="host:port:user:password",
            height=36, corner_radius=8, border_color=FIELD_BORDER,
            fg_color=INPUT, text_color=INK, placeholder_text_color=PLACEHOLDER,
            font=ctk.CTkFont("Segoe UI", 17),
        )
        self.proxy_line.grid(row=4, column=0, columnspan=2,
                             sticky="ew", padx=20, pady=(5, 6))
        self.proxy_line.bind("<Control-v>", self._paste_single_proxy, add="+")
        self.proxy_line.bind("<Return>", lambda _: self._split_single_proxy())
        self.proxy_line.bind("<FocusIn>", lambda _: self._begin_locked_repair(), add="+")
        self.proxy_paste_hint = self._label(
            detail_card,
            "Nhiều proxy cách nhau bằng dấu cách hoặc xuống dòng: tự chia Máy 1–12.",
            14, wraplength=305, justify="left")
        self.proxy_paste_hint.grid(row=5, column=0, columnspan=2, sticky="w",
                                   padx=20, pady=(0, 10))

        fields = [
            ("Tên Amazon", "full_name", 10, 0, False),
            ("Số điện thoại", "phone", 10, 1, False),
            ("Mật khẩu Amazon", "amazon_password", 11, 0, True),
            ("Thẻ của số điện thoại này", "card", 12, 0, True),
            ("URL OTP của số điện thoại này", "otp_url", 13, 0, False),
            ("Host", "host", 14, 0, False),
            ("Port", "port", 14, 1, False),
            ("User proxy", "username", 15, 0, False),
            ("Pass proxy", "proxy_password", 15, 1, True),
            ("Tên Profile (dự kiến, tự cấp)", "profile_name", 16, 0, False),
        ]
        for label, key, row, col, _secret in fields:
            cell = ctk.CTkFrame(detail_card, fg_color="transparent")
            cell.grid(row=row, column=col,
                       columnspan=2 if key in {"amazon_password", "card", "otp_url", "profile_name"} else 1, sticky="ew",
                       padx=(20, 20) if key in {"amazon_password", "card", "otp_url", "profile_name"} else
                           (20 if col == 0 else 8, 20 if col == 1 else 8),
                      pady=(0, 10))
            self._label(cell, label, 16, color=INK,
                        weight="bold").pack(anchor="w", pady=(0, 5))
            entry = Entry(
                cell, width=115, height=36, corner_radius=8, border_color=FIELD_BORDER,
                fg_color=INPUT, text_color=INK, placeholder_text_color=PLACEHOLDER,
                font=ctk.CTkFont("Segoe UI", 17),
                show="•" if _secret else "",
            )
            entry.pack(fill="x")
            if key == "profile_name":
                entry.configure(state="disabled")
            else:
                entry.bind("<FocusIn>", lambda _: self._begin_locked_repair(), add="+")
            self.detail_entries[key] = entry
        self.detail_entries["host"].bind("<Control-v>", self._paste_host, add="+")
        for key, kind in (
            ("full_name", "name"),
            ("phone", "phone"),
            ("amazon_password", "password"),
        ):
            self.detail_entries[key].bind(
                "<Control-v>",
                lambda _event, column=kind: self._paste_detail_column(column),
                add="+",
            )
        otp_row = ctk.CTkFrame(detail_card, fg_color="transparent")
        self.otp_detail_row = otp_row
        otp_row.grid(row=2, column=0, columnspan=2, sticky="ew",
                     padx=20, pady=(0, 12))
        otp_row.grid_remove()
        self.otp_detail_status = self._label(
            otp_row, "Mã OTP", 16, color=INK, weight="bold")
        self.otp_detail_status.pack(side="left")
        self.otp_detail_code = self._label(
            otp_row, "", 17, color=INK, weight="bold")
        self.otp_detail_code.pack(side="left", padx=(10, 0))
        self.otp_copy_button = Button(
            otp_row, text="Sao chép", icon_name="copy", width=90, height=36,
            corner_radius=8, fg_color=SECONDARY, hover_color=SECONDARY_HOVER,
            text_color=INK, text_color_disabled=DISABLED_TEXT,
            border_color=FIELD_BORDER, border_width=1,
            font=ctk.CTkFont("Segoe UI", 15, weight="bold"),
            state="disabled", command=self._copy_otp,
        )
        self.otp_copy_button.pack(side="right")
        self.attach_profile_button = Button(
            detail_card, text="Thử q1 từ menu ba gạch", icon_name="smartphone", height=40,
            corner_radius=8, fg_color=SECONDARY, hover_color=SECONDARY_HOVER,
            text_color=INK, text_color_disabled=DISABLED_TEXT,
            border_color=FIELD_BORDER, border_width=1,
            font=ctk.CTkFont("Segoe UI", 16, weight="bold"),
            command=self._attach_from_menu,
        )
        self.attach_profile_button.grid(row=17, column=0, columnspan=2,
                                   sticky="ew", padx=20, pady=(0, 17))
        self.single_account_heading = section_heading(
            "Dán hàng Amazon · Máy 1", 6, "clipboard-paste")
        self.single_account_line = Entry(
            detail_card, placeholder_text="SĐT | MK | Tên | Thẻ | URL OTP",
            height=36, corner_radius=8, border_color=FIELD_BORDER,
            fg_color=INPUT, text_color=INK, placeholder_text_color=PLACEHOLDER,
            font=ctk.CTkFont("Segoe UI", 17), show="•")
        self.single_account_line.grid(row=7, column=0, columnspan=2,
                                      sticky="ew", padx=20, pady=(5, 8))
        self.single_account_line.bind("<Return>", lambda _: self._apply_single_account_line())
        self.apply_single_account_button = Button(
            detail_card, text="Điền dữ liệu", icon_name="arrow-down-to-line", width=115, height=34,
            fg_color=SECONDARY, hover_color=SECONDARY_HOVER,
            text_color=INK, text_color_disabled=MUTED,
            border_color=FIELD_BORDER, border_width=1,
            font=ctk.CTkFont("Segoe UI", 16, weight="bold"),
            command=self._apply_single_account_line)
        self.apply_single_account_button.grid(row=8, column=0, sticky="ew",
                                              padx=(20, 8), pady=(0, 10))
        self.clear_selected_button = Button(
            detail_card, text="Xóa dữ liệu", role="danger", icon_name="trash-2", width=115, height=34,
            fg_color=SECONDARY, hover_color=SECONDARY_HOVER,
            text_color=INK, text_color_disabled=DISABLED_TEXT,
            font=ctk.CTkFont("Segoe UI", 16, weight="bold"),
            command=self._clear_selected_data)
        self.clear_selected_button.grid(row=8, column=1, sticky="ew",
                                        padx=(8, 20), pady=(0, 10))

    def _build_actions(self, parent) -> None:
        action = ctk.CTkFrame(parent, fg_color=FOOTER, corner_radius=10,
                              border_width=1, border_color=FOOTER_BORDER)
        action.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(8, 0))
        action.grid_columnconfigure((0, 1, 2), weight=1, uniform="batch_actions")
        action.grid_columnconfigure(4, weight=1)
        self.run_button = Button(
            action, text="Chạy 1 máy", role="run", icon_name="play", width=150, height=48,
            corner_radius=10, fg_color=CONTINUE_BG, hover_color=CONTINUE_HOVER,
            border_width=1, border_color=FIELD_BORDER,
            text_color=INK, text_color_disabled=DISABLED_TEXT,
            font=ctk.CTkFont("Segoe UI", 16, weight="bold"),
            command=self._start,
        )
        self.run_button.grid(row=0, column=0, sticky="ew", padx=(16, 8), pady=12)
        self.stop_button = Button(
            action, text="Dừng cả mẻ", role="batch-stop", icon_name="square", width=140, height=48,
            corner_radius=9, fg_color=SECONDARY, hover_color=SECONDARY_HOVER,
            text_color=INK, text_color_disabled=DISABLED_TEXT,
            border_color=FIELD_BORDER, border_width=1,
            font=ctk.CTkFont("Segoe UI", 16, weight="bold"),
            state="disabled",
            command=self._request_stop,
        )
        self.stop_button.grid(row=0, column=1, sticky="ew", padx=8, pady=12)
        self.reset_button = Button(
            action, text="Mẻ mới", role="footer-secondary", icon_name="refresh-cw", width=130, height=48,
            corner_radius=9, fg_color=SECONDARY, hover_color=SECONDARY_HOVER,
            text_color=INK, text_color_disabled=DISABLED_TEXT,
            border_color=FIELD_BORDER, border_width=1,
            font=ctk.CTkFont("Segoe UI", 16, weight="bold"),
            command=self._reset,
        )
        self.reset_button.grid(row=0, column=2, sticky="ew", padx=8, pady=12)
        ctk.CTkFrame(action, width=1, height=34, fg_color=HEADER_BORDER).grid(
            row=0, column=3, padx=16)
        activity = ctk.CTkFrame(action, fg_color="transparent")
        activity.grid(row=0, column=4, sticky="e", padx=(0, 18), pady=10)
        self.activity_marker = self._label(activity, "●", 18, color=MUTED, width=18)
        self.activity_marker.pack(side="left", padx=(0, 8))
        self.run_note = FooterNote(activity, text="Sẵn sàng nhập liệu",
                                   text_color=FOOTER_TEXT, font=ui_font(14),
                                   wraplength=220, justify="right")
        self.run_note.pack(side="left")

    def _show_preview_table(self) -> None:
        self.main._cancel_scroll()
        self.root.update_idletasks()
        canvas = self.main._parent_canvas
        bounds = canvas.bbox("all")
        if bounds:
            canvas.yview_moveto(
                min(1.0, self.preview_table.winfo_y() /
                    max(1, bounds[3] - bounds[1]))
            )

    def _copy_otp(self) -> None:
        code = self.otp_codes[self.selected]
        if code:
            self.root.clipboard_clear()
            self.root.clipboard_append(code)

    def show_otp(self, batch_id: str, index: int, code: str) -> bool:
        """UI-thread hook; discard a late OTP from a batch already reset."""
        if batch_id != self.draft.batch_id:
            return False
        if not 0 <= index < MAX_PROFILES or not (len(code) == 6 and code.isascii() and code.isdigit()):
            raise ValueError("OTP must be six ASCII digits for an existing machine")
        self.otp_codes[index] = code
        self.otp_status[index] = "Đã lấy mã"
        if self.selected == index:
            self._refresh_otp_detail()
        self._refresh_table()
        return True

    def show_otp_status(self, batch_id: str, index: int, status: str) -> bool:
        if batch_id != self.draft.batch_id:
            return False
        self.otp_status[index] = status
        if self.selected == index:
            self._refresh_otp_detail()
        self._refresh_table()
        return True

    def _refresh_otp_detail(self) -> None:
        code = self.otp_codes[self.selected]
        self.otp_detail_code.configure(text=code)
        self.otp_copy_button.configure(state="normal" if code else "disabled")
        if code:
            self.otp_detail_row.grid()
        else:
            self.otp_detail_row.grid_remove()

    def _refresh_selected_progress(self) -> None:
        message, state = self.status[self.selected]
        color, background, symbol = state_style(state)
        self._configure_display(self.detail_status, text=status_title(state), text_color=color)
        if hasattr(self, "detail_profile_label"):
            self._configure_display(self.detail_profile_label,
                text=self.values[self.selected]["profile_name"].get())
        if hasattr(self, "detail_description"):
            self._configure_display(self.detail_description,
                                    text="" if message.strip() == status_title(state) else message,
                                    text_color=PROGRESS_TEXT if color == PROCESSING else BODY,
                                    font=self._progress_detail_font if color == PROCESSING
                                         else self._secondary_detail_font)
            if message.strip() == status_title(state):
                self.detail_description.pack_forget()
            elif not self.detail_description.winfo_manager():
                self.detail_description.pack(fill="x", pady=(2, 0))
        if hasattr(self, "status_marker"):
            self._configure_display(self.status_marker, image=icon(symbol, color, ICON_STATUS))
            self._configure_display(self.progress_row, fg_color="transparent")

    def _maybe_show_preview(self) -> None:
        keys = ("host", "port", "full_name", "phone", "amazon_password", "otp_url")
        if all(all(self.values[i][key].get() for key in keys)
               for i in range(int(self.count.get()))):
            self.root.after(80, self._show_preview_table)

    def _build_preview_table(self) -> None:
        self.table_bands = []
        self.table_actions = []
        self._table_fonts = []
        self._table_hover = None
        table = ctk.CTkFrame(self.main, fg_color=SURFACE, corner_radius=10,
                             border_width=1, border_color=BORDER)
        self.preview_table = table
        table.grid(row=1, column=0, sticky="ew")
        table.grid_columnconfigure(1, weight=1)
        self.table_title = self._label(table, "Danh sách điện thoại", 20,
                                       color=INK, weight="bold",
                                       image=icon("list", ICON_DEFAULT, 18, gap=6),
                                       compound="left")
        self.table_title.grid(row=0, column=0, columnspan=2,
                              sticky="w", padx=20, pady=(14, 12))
        self.table_count = self._label(table, "01 / 12", 17,
            color=UTILITY_TEXT, fg_color=HEADER_CONTROL, corner_radius=8,
            width=78, height=30)
        self.table_count.configure(font=ui_font(17, "semibold"))
        self.table_count.grid(row=0, column=2, sticky="e", padx=20, pady=(14, 12))
        keys = ("machine", "status")
        self.table_stripes = []
        for index in range(MAX_PROFILES):
            band = ctk.CTkFrame(table, fg_color=ROW_ALT, border_color=ROW_BORDER,
                                 border_width=1, corner_radius=8, width=0, height=0)
            band.grid(row=index + 1, column=0, columnspan=3, sticky="nsew",
                      padx=16, pady=4)
            self.table_bands.append(band)
            stripe = ctk.CTkFrame(band, fg_color=ROW_SELECTED_BORDER,
                                  corner_radius=2, width=4)
            stripe.place(relx=0, rely=.12, relheight=.76, x=1)
            self.table_stripes.append(stripe)
            band.bind("<Button-1>", lambda _event, i=index: self._select(i))
            band.bind("<Enter>", lambda _event, i=index: self._hover_table_row(i))
            band.bind("<Leave>", lambda _event: self._hover_table_row(None))
            cells = {}
            for col, key in enumerate(keys):
                # Native labels avoid four extra rounded Canvas redraws per row
                # whenever Windows resizes the main workspace.
                if key == "status":
                    label = StatusCell(table, bg=SURFACE)
                else:
                    label = MachineCell(table, bg=SURFACE)
                label.grid(row=index + 1, column=col, sticky="ew",
                           padx=(30 if col == 0 else 12, 6), pady=12)
                label.bind("<Button-1>", lambda _event, i=index: self._select(i))
                label.bind("<Enter>", lambda _event, i=index: self._hover_table_row(i))
                label.bind("<Leave>", lambda _event: self._hover_table_row(None))
                cells[key] = label
            self.table_rows.append(cells)
            actions = ctk.CTkFrame(table, fg_color="transparent")
            self.table_actions.append(actions)
            actions.grid(row=index + 1, column=2, sticky="e", padx=(8, 26), pady=12)
            button = Button(
                actions, text="Tiếp tục", role="continue", icon_name="play", width=96, height=38, corner_radius=8,
                fg_color=SECONDARY, hover_color=SECONDARY_HOVER,
                text_color=INK, text_color_disabled=DISABLED_TEXT,
                border_width=1, border_color=FIELD_BORDER,
                font=ctk.CTkFont("Segoe UI", 16, weight="bold"),
                command=lambda i=index: self._continue_profile(i),
            )
            button.pack(side="left", padx=(0, 8))
            self.row_buttons.append(button)
            stop_button = Button(
                actions, text="Dừng", role="stop", icon_name="square", width=82, height=38, corner_radius=8,
                fg_color=SECONDARY, hover_color=SECONDARY_HOVER,
                text_color=INK, text_color_disabled=DISABLED_TEXT,
                border_width=1, border_color=FIELD_BORDER,
                font=ctk.CTkFont("Segoe UI", 16, weight="bold"),
                state="disabled", command=lambda i=index: self._request_stop_phone(i),
            )
            stop_button.pack(side="left")
            self.row_stop_buttons.append(stop_button)
        ctk.CTkFrame(table, fg_color="transparent", height=5).grid(
            row=MAX_PROFILES + 1, column=0, columnspan=3, pady=(0, 10))

    def _hover_table_row(self, index) -> None:
        self._table_hover = index
        self._refresh_table()

    def _fit_table_columns(self, _event=None) -> None:
        width = self.main._parent_canvas.winfo_width() / self.main._get_widget_scaling()
        compact = width < 650
        identity_wrap = 135 if compact else min(210, round(width * .28))
        status_wrap = max(130, min(420, width - identity_wrap - 305))
        layout = (compact, round(status_wrap))
        if getattr(self, "_dense_table", None) == layout:
            return
        self._dense_table = layout
        wraps = {"machine": identity_wrap, "status": status_wrap}
        for cells in self.table_rows:
            for key, cell in cells.items():
                cell.set_wrap(wraps[key])

    def _fit_detail_text(self, _event=None) -> None:
        width = max(200, self.detail_panel._parent_canvas.winfo_width() /
                    self.detail_panel._get_widget_scaling() - 40)
        if getattr(self, "_detail_wrap", None) == width:
            return
        self._detail_wrap = width
        self.proxy_paste_hint.configure(wraplength=width, justify="left", anchor="w")
        for widget in (self.proxy_paste_heading, self.account_detail_heading,
                       self.single_account_heading):
            widget.configure(wraplength=max(160, width - 28), justify="left", anchor="w")
        for widget in (self.detail_status, self.detail_description):
            widget.configure(wraplength=max(160, width - 28))

    def _bulk_row(self, parent, kind: str, title: str,
                  placeholder: str, _hint: str, row: int) -> None:
        self._label(parent, title, 16, color=INK,
                    weight="bold").grid(row=row, column=0, sticky="w",
                                        padx=(20, 10), pady=7)
        entry = Entry(
            parent, placeholder_text=(
                f"Ctrl+V 1–100 proxy · {placeholder}" if kind == "proxy" else
                f"Ctrl+V 1–12 dòng · {placeholder}"),
            height=42, corner_radius=8, border_color=FIELD_BORDER,
            fg_color=INPUT, text_color=INK, placeholder_text_color=PLACEHOLDER,
            font=ctk.CTkFont("Segoe UI", 16),
        )
        entry.grid(row=row, column=1, sticky="ew", padx=(0, 8), pady=5)
        entry.bind("<Control-v>",
                   lambda _event, k=kind: self._paste_bulk_entry(k), add="+")
        entry.bind("<Return>", lambda _event, k=kind: self._apply_bulk(k))
        self.bulk_boxes[kind] = entry
        Button(
            parent, text="Dán clipboard", role="import", icon_name="clipboard-paste", width=116, height=42,
            corner_radius=8, fg_color=SECONDARY, hover_color=SECONDARY_HOVER,
            text_color=INK, border_width=1, border_color=FIELD_BORDER,
            font=ctk.CTkFont("Segoe UI", 16, weight="bold"),
            command=lambda k=kind: self._paste_from_clipboard(k),
        ).grid(row=row, column=2, padx=(0, 8), pady=5)
        feedback = self._label(parent, "Chưa dán", 14)
        feedback.grid(row=row, column=3, sticky="w", padx=(0, 16), pady=3)
        self.bulk_feedback[kind] = feedback

    def _paste_bulk_entry(self, kind: str) -> str | None:
        try:
            copied = self.root.clipboard_get()
        except tk.TclError:
            return None
        self._apply_bulk_text(kind, copied)
        return "break"

    def _paste_from_clipboard(self, kind: str) -> None:
        try:
            copied = self.root.clipboard_get()
        except tk.TclError:
            messagebox.showerror("Clipboard trống", "Không có văn bản để dán.")
            return
        self._apply_bulk_text(kind, copied)

    def _apply_account_text(self, copied: str) -> None:
        self._apply_account_records(parse_records(copied, account_table=True))

    def _apply_single_account_line(self) -> None:
        index = self.selected
        if self.draft.locked and not self._can_edit_account_row(index):
            self.run_note.configure(text="Dừng riêng máy này trước khi sửa hàng Amazon",
                                    text_color=RED)
            return
        raw = self.single_account_line.get().strip()
        if not raw or "\n" in raw or "\r" in raw:
            self.run_note.configure(text="Chỉ dán một hàng Amazon của máy đang chọn", text_color=RED)
            return
        try:
            table_row = (raw if "\t" in raw or raw.count("|") < 3 or
                         (raw.startswith("|") and raw.endswith("|")) else f"|{raw}|")
            record = parse_records(table_row, account_table=True)[0]
            token = otp_token(record.otp_url)
            if any(other.index != index and other.account is not None and
                   otp_token(other.account.otp_url) == token
                   for other in self.jobs.values()):
                raise ToolError("URL OTP trùng máy khác")
        except (ToolError, ValueError) as exc:
            self.run_note.configure(text=f"Máy {index + 1}: {exc}", text_color=RED)
            return
        if self.draft.locked:
            self._mark_locked_row_dirty(index)
        else:
            self.draft.account_count = max(self.draft.account_count, index + 1)
            self.count.set(str(max(int(self.count.get()), index + 1)))
        row = self.values[index]
        for key, value in (("phone", record.phone), ("amazon_password", record.password),
                           ("full_name", record.full_name), ("card", record.card),
                           ("otp_url", record.otp_url)):
            row[key].set(value)
        self.otp_codes[index] = ""
        self.otp_status[index] = "Chưa yêu cầu mã"
        self.single_account_line.delete(0, "end")
        self.run_note.configure(text=f"Đã điền hàng Amazon vào Máy {index + 1}", text_color=GREEN)
        self._refresh_devices()

    def _clear_selected_data(self) -> None:
        index = self.selected
        proxy_editable = self._can_edit_locked_row(index) if self.draft.locked else True
        account_editable = self._can_edit_account_row(index) if self.draft.locked else True
        if not proxy_editable and not account_editable:
            self.run_note.configure(text="Dừng riêng máy này trước khi xóa dữ liệu",
                                    text_color=RED)
            return
        if self.draft.locked:
            self._mark_locked_row_dirty(index)
        keys = REPAIR_KEYS if proxy_editable else (
            "phone", "amazon_password", "full_name", "card", "otp_url")
        for key in keys:
            self.values[index][key].set("")
        self.otp_codes[index] = ""
        self.otp_status[index] = "Chưa yêu cầu mã"
        if proxy_editable:
            self.proxy_line.delete(0, "end")
        self.single_account_line.delete(0, "end")
        self.run_note.configure(text=f"Đã xóa {'dữ liệu' if proxy_editable else 'Amazon'} Máy {index + 1}; nhập lại rồi bấm Tiếp tục",
                                text_color=BLUE)
        self._refresh_devices()

    def _apply_account_records(self, records) -> None:
        self.draft.replace("account", len(records))
        for target in self.values:
            for key in ("phone", "amazon_password", "full_name", "card", "otp_url"):
                target[key].set("")
        self.otp_status = ["Chưa yêu cầu mã" for _ in range(MAX_PROFILES)]
        self.otp_codes = ["" for _ in range(MAX_PROFILES)]
        for index, record in enumerate(records):
            target = self.values[index]
            target["phone"].set(record.phone)
            target["amazon_password"].set(record.password)
            target["full_name"].set(record.full_name)
            target["card"].set(record.card)
            target["otp_url"].set(record.otp_url)
        self.count.set(str(self.draft.count))
        self._refresh_devices()
        self.bulk_feedback["account"].configure(
            text=f"✓ {len(records)} máy", text_color=GREEN)
        if all(record.proxy for record in records):
            self.bulk_feedback["proxy"].configure(
                text=f"✓ {len(records)} máy", text_color=GREEN)
        self.run_note.configure(
            text=f"Đã gán {len(records)} hàng vào mẻ; chưa nhập vào Amazon", text_color=GREEN)
        self.bulk_boxes["account"].delete(0, "end")
        self._refresh_otp_detail()
        self._maybe_show_preview()

    def _apply_bulk(self, kind: str) -> None:
        self._apply_bulk_text(kind, self.bulk_boxes[kind].get())

    def _apply_bulk_text(self, kind: str, content: str) -> None:
        try:
            if self.draft.locked:
                raise ToolError("Mẻ đã chạy; bấm Mẻ mới để nhập dữ liệu khác")
            proxies, accounts = parse_bulk_payload(content)
        except (ToolError, ValueError) as exc:
            self.bulk_feedback[kind].configure(text=str(exc), text_color=RED)
            self.run_note.configure(text=str(exc), text_color=RED)
            return
        if proxies:
            self.draft.replace("proxy", len(proxies))
            for target in self.values:
                for key in ("host", "port", "username", "proxy_password"):
                    target[key].set("")
            for index, value in enumerate(proxies[:MAX_PROFILES]):
                target = self.values[index]
                target["host"].set(value.host)
                target["port"].set(str(value.port))
                target["username"].set(value.username)
                target["proxy_password"].set(value.password)
            self.proxy_fallbacks = proxies[MAX_PROFILES:]
            self.bulk_feedback["proxy"].configure(
                text=f"✓ {min(len(proxies), MAX_PROFILES)} máy · {len(self.proxy_fallbacks)} dự phòng",
                text_color=GREEN)
        if accounts:
            self._apply_account_records(accounts)
        if kind == "proxy" and not proxies:
            self.bulk_feedback["proxy"].configure(
                text="Đã chuyển vào Thông tin Amazon", text_color=GREEN)
        elif kind == "account" and not accounts:
            self.bulk_feedback["account"].configure(
                text="Đã chuyển vào Proxy", text_color=GREEN)
        self.count.set(str(self.draft.count))
        self._refresh_devices()
        self.run_note.configure(
            text=f"Đã nhận {len(proxies)} proxy, {len(accounts)} hàng Amazon hợp lệ",
            text_color=GREEN)
        self.bulk_boxes[kind].delete(0, "end")
        self._maybe_show_preview()

    def _paste_single_proxy(self, _event) -> str | None:
        try:
            copied = self.root.clipboard_get()
        except tk.TclError:
            self.root.after(80, self._split_single_proxy)
            return None
        self._accept_proxy_text(copied)
        return "break"

    def _paste_host(self, _event) -> str | None:
        try:
            copied = self.root.clipboard_get()
        except tk.TclError:
            self.root.after(80, self._split_host_if_full)
            return None
        if copied.count(":") >= 3:
            self._accept_proxy_text(copied)
            return "break"
        return None

    def _paste_detail_column(self, kind: str) -> str | None:
        try:
            copied = self.root.clipboard_get()
        except tk.TclError:
            return None
        if self.draft.locked:
            if "\n" in copied or "\r" in copied:
                self.run_note.configure(
                    text=f"Mẻ đã chạy; chỉ dán một giá trị vào Máy {self.selected + 1}",
                    text_color=RED)
                return "break"
            return None  # Let the entry paste one value into the selected row.
        if "\n" not in copied and "\r" not in copied:
            return None
        try:
            parsed = parse_column(kind, copied)
        except (ToolError, ValueError) as exc:
            self.run_note.configure(text=str(exc), text_color=RED)
            return "break"
        key = {"name": "full_name", "phone": "phone",
               "password": "amazon_password"}[kind]
        for index, value in enumerate(parsed):
            self.values[index][key].set(value)
        self.count.set(str(max(int(self.count.get()), len(parsed))))
        self.run_note.configure(
            text=f"Đã tự điền {len(parsed)} {kind} vào Máy 1–{len(parsed)}",
            text_color=GREEN,
        )
        self._refresh_devices()
        return "break"

    def _split_host_if_full(self) -> None:
        if self.detail_entries["host"].get().count(":") >= 3:
            self.proxy_line.delete(0, "end")
            self.proxy_line.insert(0, self.detail_entries["host"].get())
            self._split_single_proxy()

    def _split_single_proxy(self) -> None:
        raw = self.proxy_line.get()
        if not raw.strip():
            return
        self._accept_proxy_text(raw)

    def _accept_proxy_text(self, raw: str) -> None:
        try:
            if self.draft.locked:
                if not self._can_edit_locked_row(self.selected):
                    raise ToolError("Máy này đã có Profile hoặc đang chạy; không thể đổi proxy ở bước này")
                parsed = parse_column("proxy", raw)
                if len(parsed) != 1:
                    raise ToolError(f"Mẻ đã chạy; chỉ dán 1 proxy cho Máy {self.selected + 1}")
                self._mark_locked_row_dirty(self.selected)
                proxy = parsed[0]
                row = self.values[self.selected]
                for key, value in (
                    ("host", proxy.host), ("port", str(proxy.port)),
                    ("username", proxy.username),
                    ("proxy_password", proxy.password),
                ):
                    row[key].set(value)
                self.proxy_line.delete(0, "end")
                self.run_note.configure(
                    text=f"Đã sửa proxy Máy {self.selected + 1}; bấm Tiếp tục để tạo lại Profile",
                    text_color=GREEN)
                self._refresh_devices()
                return
            parsed = parse_column("proxy", raw)
            if len(parsed) > 1:
                self.draft.replace("proxy", len(parsed))
                self.proxy_fallbacks = parsed[MAX_PROFILES:]
            else:
                self.draft.replace("proxy", max(self.draft.proxy_count, self.selected + 1))
        except (ToolError, ValueError) as exc:
            self.run_note.configure(text=str(exc), text_color=RED)
            return
        if len(parsed) > 1:
            for target in self.values:
                for key in ("host", "port", "username", "proxy_password"):
                    target[key].set("")
        for index, proxy in enumerate(parsed[:MAX_PROFILES]):
            row = self.values[self.selected if len(parsed) == 1 else index]
            for key, value in (
                ("host", proxy.host), ("port", str(proxy.port)),
                ("username", proxy.username), ("proxy_password", proxy.password),
            ):
                row[key].set(value)
        self.count.set(str(self.draft.count))
        self.proxy_line.delete(0, "end")
        result = (f"Đã tự điền {len(parsed)} proxy vào Máy 1–{len(parsed)}"
                  if len(parsed) > 1 else
                  f"Đã điền proxy vào Máy {self.selected + 1}")
        self.run_note.configure(text=result, text_color=GREEN)
        self._refresh_devices()

    def _schedule_refresh(self) -> None:
        if self._refresh_after_id is None:
            self._refresh_after_id = self.root.after(40, self._delayed_refresh)

    def _on_row_value_changed(self, index: int, key: str) -> None:
        can_edit = (self._can_edit_locked_row(index) if key in
                    {"host", "port", "username", "proxy_password"} else
                    self._can_edit_account_row(index))
        if self.draft.locked and key in REPAIR_KEYS and index == self.selected and can_edit:
            self._mark_locked_row_dirty(index)
            if key == "otp_url":
                self.otp_codes[index] = ""
                self.otp_status[index] = "Chưa yêu cầu mã"
        self._schedule_refresh()

    def _mark_locked_row_dirty(self, index: int) -> None:
        self._edited_locked_rows.add(index)
        if index in self._pending_retries:
            self._pending_retries.discard(index)
            self.status[index] = (
                f"Máy {index + 1} đã sửa dữ liệu · bấm Tiếp tục để áp dụng",
                "error")
            self.run_note.configure(
                text=f"Đã hủy lượt tạo lại đang chờ của Máy {index + 1}; bấm Tiếp tục sau khi sửa xong",
                text_color=BLUE)

    def _begin_locked_repair(self) -> None:
        if (self.draft.locked and self.selected in self._pending_retries and
                (self._can_edit_locked_row(self.selected) or
                 self._can_edit_account_row(self.selected))):
            self._mark_locked_row_dirty(self.selected)
            self._refresh_devices()

    def _delayed_refresh(self) -> None:
        self._refresh_after_id = None
        self._refresh_devices()

    def _refresh_devices(self) -> None:
        if self._refresh_after_id is not None:
            self.root.after_cancel(self._refresh_after_id)
            self._refresh_after_id = None
        if not self.table_rows:
            return
        active = int(self.count.get())
        post_busy = any(session.state == "RUNNING"
                        for session in self.post_menu_sessions.values()) or any(
                            worker.is_alive() for worker in
                            getattr(self, "preparation_retry_workers", {}).values())
        has_post_menu = bool(self.post_menu_sessions)
        partial_jobs = self.draft.locked and any(
            index not in self.jobs for index in range(active))
        issue = self._input_issue()
        if self.registry_error:
            validation = self.registry_error
        elif self.draft.locked:
            validation = (f"Mẻ đang chạy · tối đa {self.run_group_size} máy Running tự động · "
                          f"{active} Profile" if self.running else
                          f"Mẻ đã khóa · {active} máy · bấm Mẻ mới để nhập mẻ tiếp theo")
        elif issue:
            validation = issue
        else:
            validation = f"✓ {active} máy đã phân bổ đúng · thông tin Amazon chưa nhập vào app"
        self.validation_label.configure(
            text=validation,
            text_color=(RED if self.registry_error else MUTED if not self.draft.locked and
                        not self.draft.proxy_count and not self.draft.account_count else
                        RED if issue else GREEN if not self.draft.locked else MUTED),
        )
        self.run_button.configure(
            text=f"Chạy {active} máy",
            state="disabled" if self.running or self.attach_in_progress or post_busy or has_post_menu or partial_jobs or issue or self._previous_work_busy() else "normal",
            fg_color=SECONDARY if self.running or self.attach_in_progress or post_busy or has_post_menu or partial_jobs or issue else CONTINUE_BG,
            text_color=INK,
        )
        self.stop_button.configure(state="normal" if self.running or post_busy else "disabled")
        if hasattr(self, "activity_marker"):
            self._configure_display(self.activity_marker,
                text_color=GREEN if self.running or post_busy else MUTED)
        self._configure_display(self.table_title, text="Danh sách điện thoại")
        if hasattr(self, "table_count"):
            self._configure_display(self.table_count, text=f"{active:02} / 12")
        self._refresh_selected_progress()
        self.reset_button.configure(state="disabled" if (self.running or post_busy or
                                    self.attach_in_progress) and not self.cancel.is_set() else "normal")
        can_attach = (self.selected in self.post_menu_step_factories
                      and self.selected not in self.jobs and not self.running
                      and not self.attach_in_progress and not self._previous_work_busy())
        self.attach_profile_button.configure(
            text=f"Thử q{self.selected + 1} từ menu ba gạch",
            state="normal" if can_attach else "disabled")
        if self.selected >= active:
            self.selected = active - 1
            self._select(self.selected)
        for i in range(MAX_PROFILES):
            state = self.status[i][1]
            may_continue = self._may_continue(i, state, bool(issue))
            item = (self.registry.get(self.jobs[i].batch_id, i)
                    if i in self.jobs and self.registry is not None else None)
            needs_creation = (i in self.jobs and state in
                              {"error", "stopped", "retry_queued"} and
                              ((item is None and self.jobs[i].proxy is not None) or
                               (item is not None and item.get("stage") == "RESERVED" and
                                item.get("state") in {"READY", "ERROR", "STOPPED"} and
                                not item.get("device_id"))))
            self._configure_display(self.row_buttons[i],
                text="Tạo Profile" if needs_creation else "Tiếp tục",
                state="normal" if i < active and may_continue else "disabled",
                fg_color=CONTINUE_BG if i < active and may_continue else SECONDARY,
                hover_color=CONTINUE_HOVER if i < active and may_continue else SECONDARY_HOVER)
            can_stop = i < active and self._can_stop_phone(i)
            self._configure_display(self.row_stop_buttons[i],
                state="normal" if can_stop else "disabled",
                fg_color=STOP_BG if can_stop else SECONDARY,
                hover_color=STOP_HOVER if can_stop else SECONDARY_HOVER)
        self._refresh_table()
        self._set_editing(not self.draft.locked)

    def _input_issue(self) -> str:
        if self.registry is None:
            return self.registry_error
        if self.draft.locked and self.jobs:
            return ""
        mode = getattr(self, "settings", AppSettings()).account_flow_mode
        active = int(self.count.get())
        if self.draft.proxy_count and self.draft.proxy_count < active:
            return f"Cần ít nhất {active} proxy; hiện có {self.draft.proxy_count}"
        if mode != CHANGE_US_FROM_START and self.draft.account_count == 0:
            return "Chưa có hàng Amazon nào; dán đủ thông tin cho mọi máy trước khi Chạy mẻ"
        if mode != CHANGE_US_FROM_START and self.draft.account_count != active:
            return f"Thông tin Amazon có {self.draft.account_count} hàng, cần {active}"
        for index in range(active):
            row = self.values[index]
            if not all(row[key].get().strip() for key in
                       ("host", "port", "username", "proxy_password")):
                return f"Máy {index + 1}: proxy chưa đủ"
            try:
                ProxyConfig("socks5", row["host"].get().strip(),
                            int(row["port"].get()), row["username"].get(),
                            row["proxy_password"].get())
            except (ToolError, ValueError) as exc:
                return f"Máy {index + 1}: {exc}"
        if mode == CHANGE_US_FROM_START:
            return ""
        required_account_keys = ("phone", "amazon_password", "full_name", "otp_url")
        account_rows = [any(self.values[i][key].get() for key in
                            (*required_account_keys, "card"))
                        for i in range(active)]
        if not all(
            all(self.values[i][key].get() for key in required_account_keys)
            for i in range(active)
        ):
            return "Thông tin Amazon chưa đủ cho mọi máy trong mẻ"
        if all(account_rows):
            tokens = []
            for index in range(active):
                row = self.values[index]
                if not PHONE.fullmatch(row["phone"].get().strip()):
                    return f"Máy {index + 1}: số điện thoại sai định dạng"
                password = row["amazon_password"].get()
                if not password or any(ord(c) < 33 or ord(c) > 126 for c in password):
                    return f"Máy {index + 1}: mật khẩu không được trống, chỉ nhận ASCII không dấu cách"
                if len(row["full_name"].get()) > 100:
                    return f"Máy {index + 1}: tên Amazon quá dài"
                if row["card"].get():
                    try:
                        validate_card(row["card"].get())
                    except ToolError as exc:
                        return f"Máy {index + 1}: {exc}"
                try:
                    tokens.append(otp_token(row["otp_url"].get()))
                except ToolError as exc:
                    return f"Máy {index + 1}: {exc}"
            if len(tokens) != len(set(tokens)):
                return "URL OTP bị trùng giữa các máy"
        return ""

    def _refresh_table(self) -> None:
        active = int(self.count.get())
        for index, cells in enumerate(self.table_rows):
            values = self.values[index]
            run_status = self.status[index][0]
            otp_state = self.otp_status[index]
            status_text = f"{run_status}\nOTP: {otp_state}"
            items = {
                "machine": (f"Máy {index + 1:02}\n{values['profile_name'].get()}"
                            if index < active else f"Máy {index + 1:02}"),
                "status": status_text if index < active else "—",
            }
            row_color = (PALE if index == self.selected else
                         ROW_HOVER if index == getattr(self, "_table_hover", None) else
                         ROW_ALT if index < active else ROW_INACTIVE)
            if hasattr(self, "table_bands"):
                self._configure_display(self.table_bands[index], fg_color=row_color,
                    border_color=ROW_SELECTED_BORDER if index == self.selected else ROW_BORDER,
                    border_width=2 if index == self.selected else 1)
                self._configure_display(self.table_actions[index], fg_color=row_color)
                if hasattr(self, "table_stripes"):
                    self._configure_display(self.table_stripes[index],
                        fg_color=ROW_SELECTED_BORDER if index == self.selected else ROW_BORDER)
            color, _background, symbol = state_style(self.status[index][1])
            for key, cell in cells.items():
                if isinstance(cell, StatusCell):
                    self._configure_display(cell, text=items[key],
                        title=status_title(self.status[index][1]) if index < active else "—",
                        bg=row_color, fg=color if index < active else MUTED,
                        symbol=symbol if index < active else "clock")
                    continue
                self._configure_display(
                    cell,
                    text=(items[key] if key in {"account", "status"} else
                          items[key][:46] + ("…" if len(items[key]) > 46 else "")),
                    bg=row_color,
                    fg=(color if key == "status" and index < active else
                        BODY if index < active else MUTED),
                )

    def _select(self, index: int) -> None:
        if index >= int(self.count.get()):
            return
        self.selected = index
        self.single_account_line.delete(0, "end")
        if not self.draft.locked:
            self.proxy_line.delete(0, "end")
        for key, entry in self.detail_entries.items():
            entry.configure(textvariable=self.values[index][key])
        self.detail_title.configure(text=f"Máy {index + 1:02}")
        self.account_detail_heading.configure(
            text=f"Thông tin Amazon riêng · Máy {index + 1}")
        self.single_account_heading.configure(text=f"Dán hàng Amazon · Máy {index + 1}")
        self._refresh_selected_progress()
        self.apply_single_account_button.configure(text="Điền dữ liệu")
        self.clear_selected_button.configure(text="Xóa dữ liệu")
        self._refresh_otp_detail()
        self._refresh_devices()

    def _reset(self) -> None:
        busy = self.running or self.attach_in_progress or any(session.state == "RUNNING"
                               for session in self.post_menu_sessions.values()) or any(
                                   worker.is_alive() for worker in
                                   getattr(self, "preparation_retry_workers", {}).values())
        if busy and not self.cancel.is_set():
            return
        workers = [getattr(self, "batch_worker", None), getattr(self, "attach_worker", None),
                   *self.post_menu_workers.values(),
                   *getattr(self, "preparation_retry_workers", {}).values()]
        self._draining_workers = [worker for worker in
            [*getattr(self, "_draining_workers", []), *workers]
            if worker is not None and worker.is_alive()]
        self.running = False
        self.attach_in_progress = False
        self.batch_worker = self.attach_worker = None
        self.cancel = threading.Event()
        self._pending_retries = set()
        self._edited_locked_rows = set()
        self.preparation_retry_workers = {}
        # Old workers retain their old queues/dictionaries. Late results must
        # never enter a new draft or attach a serial to the new machine rows.
        self.events = queue.Queue()
        self.attach_events = queue.Queue()
        self.otp_events = queue.Queue()
        self.otp_status_events = queue.Queue()
        if self.registry is not None:
            self.registry = ProfileRegistry(persistent=False)
        self._set_editing(True)
        self.draft = self.draft.new()
        self.jobs = {}
        self.post_menu_sessions = {}
        self.post_menu_stops = {}
        self.phone_stop_after_step = {}
        self.post_menu_resume_after_stop = set()
        self.manual_slots = set()
        self.post_menu_workers = {}
        self.post_menu_steps = {}
        self.menu_opened_at = {}
        self.phone_serials = {}
        self.proxy_postal_prefixes = {}
        self.proxy_fallbacks.clear()
        for row in self.values:
            for value in row.values():
                value.set("")
        predicted = (self.registry.preview_names(MAX_PROFILES) if self.registry else
                     [f"q{i}" for i in range(1, MAX_PROFILES + 1)])
        for index, row in enumerate(self.values):
            row["profile_name"].set(predicted[index])
        for box in self.bulk_boxes.values():
            box.delete(0, "end")
        for kind, _, _, _hint in BULK:
            self.bulk_feedback[kind].configure(text="Chưa dán", text_color=MUTED)
        self.status = [("Chưa chạy", "idle") for _ in range(MAX_PROFILES)]
        self.otp_status = ["Chưa yêu cầu mã" for _ in range(MAX_PROFILES)]
        self.otp_codes = ["" for _ in range(MAX_PROFILES)]
        self.count.set("1")
        self._select(0)
        self.run_note.configure(text=("Có thể nhập mẻ mới · đang chờ tác vụ cũ dừng hẳn"
                                     if self._previous_work_busy() else "Sẵn sàng nhập liệu"), text_color=MUTED)

    def _previous_work_busy(self) -> bool:
        return any(worker.is_alive() for worker in getattr(self, "_draining_workers", []))

    def _may_continue(self, index: int, state: str, issue: bool) -> bool:
        if self._previous_work_busy() or self.attach_in_progress:
            return False
        session = self.post_menu_sessions.get(index)
        if session is not None:
            if index in self.post_menu_resume_after_stop:
                return False
            event = self.phone_stop_after_step.get(index)
            return (session.state == "PAUSED" or
                    (session.state == "RUNNING" and not self.cancel.is_set() and
                     event is not None and event.is_set()))
        if self.draft.locked:
            worker = getattr(self, "preparation_retry_workers", {}).get(index)
            if worker is not None and worker.is_alive():
                event = self.phone_stop_after_step.get(index)
                return event is not None and event.is_set()
            return index in self.jobs and state != "menu_only" and (
                not self.running or state in {"error", "uncertain", "stopped",
                                              "retry_queued", "queued",
                                              "post_paused", "post_stopped"})
        return not self.running and not issue

    def _can_edit_locked_row(self, index: int) -> bool:
        if not self.draft.locked or index not in self.jobs:
            return False
        if self.status[index][1] not in {"error", "stopped", "retry_queued"}:
            return False
        if index in self.phone_serials or index in self.post_menu_sessions:
            return False
        worker = getattr(self, "preparation_retry_workers", {}).get(index)
        if worker is not None and worker.is_alive():
            return False
        if self.registry is None:
            return False
        item = self.registry.get(self.jobs[index].batch_id, index)
        if item is None:
            return self.jobs[index].proxy is not None
        return (item.get("stage") == "RESERVED" and
                item.get("state") in {"READY", "ERROR", "STOPPED"} and
                not item.get("device_id"))

    def _can_edit_account_row(self, index: int) -> bool:
        if not self.draft.locked or index not in self.jobs:
            return False
        if self.status[index][1] not in {"error", "uncertain", "stopped",
                                         "retry_queued", "post_paused", "post_stopped"}:
            return False
        session = self.post_menu_sessions.get(index)
        if session is not None and session.state == "RUNNING":
            return False
        for workers in (getattr(self, "preparation_retry_workers", {}),
                        getattr(self, "post_menu_workers", {})):
            worker = workers.get(index)
            if worker is not None and worker.is_alive():
                return False
        return True

    def _set_editing(self, enabled: bool) -> None:
        state = "normal" if enabled else "disabled"
        proxy_editable = enabled or self._can_edit_locked_row(self.selected)
        account_editable = enabled or self._can_edit_account_row(self.selected)
        proxy_state = "normal" if proxy_editable else "disabled"
        account_state = "normal" if account_editable else "disabled"
        display_state = (state, proxy_state, account_state, self.selected)
        if getattr(self, "_editing_display_state", None) == display_state:
            return
        self._editing_display_state = display_state
        for box in self.bulk_boxes.values():
            box.configure(state=state)
        for key, entry in self.detail_entries.items():
            if key != "profile_name":
                entry.configure(state=(proxy_state if key in
                    {"host", "port", "username", "proxy_password"} else account_state))
        self.proxy_line.configure(state=proxy_state)
        self.single_account_line.configure(state=account_state)
        self.apply_single_account_button.configure(state=account_state)
        self.clear_selected_button.configure(
            state="normal" if proxy_editable or account_editable else "disabled",
            text="Xóa Amazon" if account_editable and not proxy_editable
                 else "Xóa dữ liệu")
        self.count_menu.configure(state=state)
        if hasattr(self, "proxy_paste_heading"):
            self.proxy_paste_heading.configure(
                text=(f"Dán 1 proxy cho Máy {self.selected + 1}" if proxy_editable and not enabled else
                      "Dán 1–12 proxy để tự điền" if enabled else
                      "Proxy của Profile đã tạo"))
            self.proxy_paste_hint.configure(
                text=("Chỉ sửa máy này; nhập xong bấm Tiếp tục để tạo lại Profile."
                      if proxy_editable and not enabled else
                      "Nhiều proxy cách nhau bằng dấu cách hoặc xuống dòng: tự chia Máy 1–12."
                      if enabled else
                      "Proxy đã gắn vào Profile; có thể sửa thông tin Amazon ở dưới khi máy dừng/lỗi."))

    def _open_settings(self) -> None:
        current = getattr(self, "settings_window", None)
        if current is not None and current.winfo_exists():
            current.lift()
            return
        dialog = ctk.CTkToplevel(self.root, fg_color=BG)
        self.settings_window = dialog
        dialog.title("Settings · Swarmote")
        scale = self.root._get_window_scaling()
        dialog_width = min(520, int(self.root.winfo_screenwidth() / scale - 60))
        dialog_height = min(650, int(self.root.winfo_screenheight() / scale - 90))
        dialog.geometry(f"{dialog_width}x{dialog_height}+100+20")
        dialog.resizable(False, False)
        # Map the window before building its controls so the click gets
        # immediate visual feedback even on a busy Tk event loop.
        dialog.lift()
        dialog.update_idletasks()
        card = SmoothScrollableFrame(dialog, fg_color=SURFACE, corner_radius=10,
                            border_width=1, border_color=BORDER,
                            scrollbar_button_color=SCROLLBAR,
                            scrollbar_button_hover_color=SCROLLBAR_HOVER)
        card.pack(fill="both", expand=True, padx=16, pady=16)
        self._label(card, "Mở máy sau khi tạo Profile", 19,
                    color=INK, weight="normal").pack(anchor="w", padx=22, pady=(20, 8))
        self._label(card, "Số máy Running đồng thời (1–12)", 13,
                    color=INK).pack(anchor="w", padx=22)
        group_size = tk.StringVar(value=str(self.settings.start_group_size))
        ctk.CTkOptionMenu(
            card, values=[str(i) for i in range(1, MAX_PROFILES + 1)],
            variable=group_size, width=112, height=38, corner_radius=9,
            fg_color=PALE, button_color=PALE, text_color=BLUE,
            dropdown_fg_color=SURFACE, dropdown_text_color=BODY,
            text_color_disabled=DISABLED_TEXT,
            font=ctk.CTkFont("Segoe UI", 13, weight="normal"),
        ).pack(anchor="w", padx=22, pady=(10, 14))
        self._label(
            card,
            "Tạo Profile tiếp tục khi máy khác đang cài Amazon.\n"
            "Máy tiếp theo tự mở khi một máy Running chuyển sang Offline.",
            12, justify="left",
        ).pack(anchor="w", padx=22)
        hide_creation = tk.BooleanVar(value=self.settings.hide_profile_creation)
        ctk.CTkSwitch(
            card, text="Ẩn cửa sổ Swarmote khi tạo Profile",
            variable=hide_creation, onvalue=True, offvalue=False,
            text_color=BODY, fg_color=BORDER,
            progress_color=BLUE, button_color=WHITE,
            font=ctk.CTkFont("Segoe UI", 13, weight="normal"),
        ).pack(anchor="w", padx=22, pady=(14, 3))
        self._label(card, "Các điện thoại Running vẫn hiện bình thường.",
                    12, color=MUTED).pack(anchor="w", padx=22)
        login_mode = tk.BooleanVar(value=self.settings.account_flow_mode == "login")
        change_us_mode = tk.BooleanVar(
            value=self.settings.account_flow_mode == CHANGE_US_FROM_START)
        address_card = tk.BooleanVar(value=self.settings.login_followup == "address_and_card")
        card_only = tk.BooleanVar(value=self.settings.login_followup == "card_only")

        def select_login() -> None:
            if login_mode.get():
                change_us_mode.set(False)
            else:
                address_card.set(False)
                card_only.set(False)

        ctk.CTkSwitch(
            card, text="Đăng nhập Amazon",
            variable=login_mode, onvalue=True, offvalue=False,
            command=select_login,
            text_color=BODY, fg_color=BORDER,
            progress_color=BLUE, button_color=WHITE,
            font=ctk.CTkFont("Segoe UI", 13, weight="normal"),
        ).pack(anchor="w", padx=22, pady=(18, 3))

        def select_followup(selected, other):
            if selected.get():
                other.set(False)
                login_mode.set(True)
                change_us_mode.set(False)

        ctk.CTkSwitch(
            card, text="Đăng nhập · thêm địa chỉ rồi thẻ",
            variable=address_card, onvalue=True, offvalue=False,
            command=lambda: select_followup(address_card, card_only),
            text_color=BODY, fg_color=BORDER,
            progress_color=BLUE, button_color=WHITE,
            font=ctk.CTkFont("Segoe UI", 13, weight="normal"),
        ).pack(anchor="w", padx=22, pady=(14, 3))
        ctk.CTkSwitch(
            card, text="Đăng nhập · chỉ thêm thẻ",
            variable=card_only, onvalue=True, offvalue=False,
            command=lambda: select_followup(card_only, address_card),
            text_color=BODY, fg_color=BORDER,
            progress_color=BLUE, button_color=WHITE,
            font=ctk.CTkFont("Segoe UI", 13, weight="normal"),
        ).pack(anchor="w", padx=22, pady=(10, 3))

        def select_change_us() -> None:
            if change_us_mode.get():
                login_mode.set(False)
                address_card.set(False)
                card_only.set(False)

        ctk.CTkSwitch(
            card, text="Đổi US từ đầu · b1–b17",
            variable=change_us_mode, onvalue=True, offvalue=False,
            command=select_change_us,
            text_color=BODY, fg_color=BORDER,
            progress_color=BLUE, button_color=WHITE,
            font=ctk.CTkFont("Segoe UI", 13, weight="normal"),
        ).pack(anchor="w", padx=22, pady=(14, 3))
        self._label(card, "Tắt cả Đăng nhập và Đổi US: Tạo tài khoản.",
                    12, color=MUTED).pack(anchor="w", padx=22)
        self._label(card, "Áp dụng cho các máy bắt đầu luồng Amazon sau khi lưu.",
                    12, color=MUTED).pack(anchor="w", padx=22)

        def save() -> None:
            if self.running:
                messagebox.showerror("Mẻ đang chạy", "Đổi Settings sau khi mẻ kết thúc")
                return
            try:
                followup = ("address_and_card" if address_card.get() else
                            "card_only" if card_only.get() else "none")
                flow_mode = (CHANGE_US_FROM_START if change_us_mode.get() else
                             "login" if login_mode.get() else "create")
                updated = AppSettings(int(group_size.get()), hide_creation.get(),
                                      flow_mode, followup)
                save_settings(updated)
            except (ToolError, OSError, ValueError) as exc:
                messagebox.showerror("Không lưu được Settings", str(exc))
                return
            self.settings = updated
            dialog.destroy()
            mode_label = ("Đổi US từ đầu · b1–b17" if updated.account_flow_mode == CHANGE_US_FROM_START
                          else "Đăng nhập + địa chỉ + thẻ" if updated.login_followup == "address_and_card"
                          else "Đăng nhập + thẻ" if updated.login_followup == "card_only"
                          else "Đăng nhập" if updated.account_flow_mode == "login"
                          else "Tạo tài khoản")
            self.run_note.configure(
                text=f"Đã lưu: tối đa {updated.start_group_size} máy Running tự động · {mode_label}",
                text_color=GREEN,
            )

        Button(card, text="Lưu Settings", role="primary", icon_name="settings", width=136, height=38,
                      corner_radius=9, fg_color=BLUE, hover_color=BLUE_HOVER,
                      text_color=WHITE,
                      font=ctk.CTkFont("Segoe UI", 13, weight="normal"),
                      command=save).pack(anchor="e", padx=22, pady=(8, 18))

    def _sync_edited_locked_row(self, index: int) -> None:
        if index not in self._edited_locked_rows:
            return
        proxy_editable = self._can_edit_locked_row(index)
        account_editable = self._can_edit_account_row(index)
        if not proxy_editable and not account_editable:
            raise ToolError(f"Máy {index + 1} đang chạy; dừng riêng máy trước khi áp dụng dữ liệu sửa")
        row = self.values[index]
        previous = self.jobs[index]
        proxy = previous.proxy
        if proxy_editable:
            try:
                proxy = ProxyConfig("socks5", row["host"].get().strip(),
                                    int(row["port"].get()), row["username"].get(),
                                    row["proxy_password"].get())
            except (ToolError, ValueError) as exc:
                raise ToolError(f"Máy {index + 1}: proxy chưa hợp lệ") from exc
        account = previous.account
        if account_editable:
            account = (self._account_for_profile(index)
                       if previous.account is not None or
                       any(row[key].get() for key in
                           ("phone", "amazon_password", "full_name", "card", "otp_url"))
                       else None)
        if account is not None:
            token = otp_token(account.otp_url)
            if any(other.index != index and other.account is not None and
                   otp_token(other.account.otp_url) == token
                   for other in self.jobs.values()):
                raise ToolError(f"Máy {index + 1}: URL OTP trùng máy khác")
        self.jobs[index] = replace(
            previous, proxy=proxy,
            proxy_fallbacks=(() if proxy_editable and proxy != previous.proxy
                             else previous.proxy_fallbacks),
            account=account)
        self._edited_locked_rows.discard(index)

    def _continue_profile(self, index: int) -> None:
        if self._previous_work_busy():
            self.run_note.configure(text="Đang chờ tác vụ mẻ cũ dừng hẳn", text_color=MUTED)
            return
        if index in getattr(self, "_edited_locked_rows", set()):
            try:
                self._sync_edited_locked_row(index)
            except ToolError as exc:
                self.run_note.configure(text=str(exc), text_color=RED)
                self.status[index] = (str(exc), "error")
                self._refresh_devices()
                return
        session = self.post_menu_sessions.get(index)
        def select_manual() -> None:
            job = self.jobs.get(index)
            if job is not None and hasattr(job, 'batch_id'):
                if not hasattr(self, 'manual_slots'):
                    self.manual_slots = set()
                self.manual_slots.add((job.batch_id, index))
        if session is not None:
            event = self.phone_stop_after_step.get(index)
            if (session.state == "RUNNING" and event is not None and
                    event.is_set() and not self.cancel.is_set()):
                select_manual()
                self.post_menu_resume_after_stop.add(index)
                self.status[index] = (
                    f"Máy {index + 1} sẽ tiếp tục ngay sau khi dừng an toàn",
                    "resume_queued")
                self._refresh_devices()
                return
            if session.state == "PAUSED":
                if (session.last_error.startswith(("b11 nhập OTP:",
                                                   "b14 lấy và nhập OTP:")) and
                        "Không đọc được OTP bằng trình duyệt" in session.last_error):
                    if not self._read_browser_otp(index):
                        return
                self.phone_stop_after_step.setdefault(index, threading.Event()).clear()
                select_manual()
                self._start_post_menu(index)
            return
        if index in self.phone_serials and index in self.jobs:
            select_manual()
            self._start_post_menu(index)
            return
        item = (self.registry.get(self.jobs[index].batch_id, index)
                if index in self.jobs and self.registry is not None else None)
        job = self.jobs.get(index)
        if ((item is None and job is not None and getattr(job, "proxy", None) is not None) or
                (item is not None and item.get("stage") == "RESERVED" and
                 item.get("state") in {"READY", "ERROR", "STOPPED"} and
                 not item.get("device_id"))):
            if self.running and self.status[index][1] not in {
                    "error", "stopped", "retry_queued"}:
                self.run_note.configure(
                    text=f"Máy {index + 1} vẫn trong hàng tạo Profile; dừng riêng máy trước khi tạo thủ công",
                    text_color=MUTED)
                return
            select_manual()
            self._start_profile_creation_retry(index)
            return
        if item is not None and item.get("device_id"):
            select_manual()
            self._start_preparation_retry(index)
            return
        if (item is not None and item.get("stage") in
                {"PROFILE_CONFIRMED", "STARTED", "APP_INSTALLED", "MENU_OPEN"}
                and item.get("state") != "UNCERTAIN"):
            select_manual()
            self._start_preparation_retry(index)
            return
        if job is not None:
            self.status[index] = (
                "Chưa xác định được kết quả tạo Profile; cần kiểm tra đúng Profile trước khi Tiếp tục",
                "uncertain")
            self._refresh_devices()
            return
        select_manual()
        self._launch([index], manual_override=True)

    def _start_preparation_retry(self, index: int) -> None:
        if self.cancel.is_set():
            return
        if index in getattr(self, "_edited_locked_rows", set()):
            try:
                self._sync_edited_locked_row(index)
            except ToolError as exc:
                self.status[index] = (str(exc), "error")
                self._refresh_devices()
                return
        workers = getattr(self, "preparation_retry_workers", None)
        if workers is None:
            self.preparation_retry_workers = workers = {}
        worker = workers.get(index)
        if worker is not None and worker.is_alive():
            event = self.phone_stop_after_step.get(index)
            if event is not None and event.is_set() and not self.cancel.is_set():
                self.root.after(100, lambda: self._start_preparation_retry(index))
            return
        job = self.jobs.get(index)
        if job is None or self.registry is None:
            self.status[index] = ("Chưa có dữ liệu Profile của máy này để nối lại", "error")
            self._refresh_devices()
            return
        self.phone_stop_after_step.setdefault(index, threading.Event()).clear()
        self._pending_retries.discard(index)
        self.status[index] = (f"Máy {index + 1} đang tiếp tục ngay", "running")
        context = {"registry": self.registry, "events": self.events, "stop": self.cancel,
                   "serials": self.phone_serials, "opened": self.menu_opened_at,
                   "phone_stop": self.phone_stop_after_step[index]}
        worker = threading.Thread(target=self._run_preparation_retry,
                                  args=(job, context), daemon=True)
        workers[index] = worker
        self._refresh_devices()
        worker.start()

    def _start_profile_creation_retry(self, index: int) -> None:
        """Create one failed Profile now, sharing the manager lock with the batch."""
        worker = self.preparation_retry_workers.get(index)
        if worker is not None and worker.is_alive():
            return
        job = self.jobs[index]
        self.phone_stop_after_step.setdefault(index, threading.Event()).clear()
        self.status[index] = (f"Máy {index + 1} đang tạo lại Profile", "running")
        context = {"registry": self.registry, "events": self.events,
                   "stop": self.cancel, "serials": self.phone_serials,
                   "proxy_prefixes": self.proxy_postal_prefixes,
                   "opened": self.menu_opened_at, "group": self.run_group_size,
                   "hide": self.run_hide_profile_creation,
                   "phone_stops": {index: self.phone_stop_after_step[index]},
                   "final_index": -2, "manual_slots": self.manual_slots,
                   "manual_override": True}
        worker = threading.Thread(target=self._run, args=([job], context), daemon=True)
        self.preparation_retry_workers[index] = worker
        self._refresh_devices()
        worker.start()

    def _run_preparation_retry(self, job, context):
        import pythoncom
        pythoncom.CoInitializeEx(pythoncom.COINIT_MULTITHREADED)
        try:
            def emit(index, message, state, name):
                if state == "done":
                    context["opened"].setdefault(index, time.monotonic())
                context["events"].put((index, message, state, name))
            retry_preparation(job, context["registry"], emit, context["stop"],
                menu_ready=lambda index, _name, _device, serial:
                    context["serials"].__setitem__(index, serial),
                stop_after_step=context["phone_stop"], start_if_offline=True)
        except Exception as exc:
            stopped = context["stop"].is_set() or context["phone_stop"].is_set()
            reason = str(exc) if isinstance(exc, ToolError) else type(exc).__name__
            context["events"].put((job.index,
                "Đã dừng nối lại máy" if stopped else f"Không nối lại được máy: {reason}",
                "stopped" if stopped else "error", None))
        finally:
            pythoncom.CoUninitialize()

    def _read_browser_otp(self, index: int) -> bool:
        job = self.jobs[index]
        if job.account is None:
            return False
        choice = messagebox.askyesnocancel(
            f"Máy {index + 1} · OTP SMS",
            "Tool chưa đọc được URL OTP tự động.\n\n"
            "Yes: mở URL của máy này và dán phản hồi SMS vào tool.\n"
            "No: tiếp tục trên Amazon hoặc thử đọc URL lại.\n"
            "Cancel: giữ máy ở bước hiện tại.", parent=self.root)
        if choice is not True:
            return choice is False
        try:
            if not webbrowser.open(validate_otp_url(job.account.otp_url)):
                raise ToolError("Không mở được trình duyệt mặc định")
            response = simpledialog.askstring(
                f"Máy {index + 1} · Dán phản hồi OTP",
                "Tải lại trang OTP rồi dán nội dung SMS Amazon hoặc mã 6 số.",
                show="*", parent=self.root)
            if response is None:
                return False
            response = response.strip()
            code = (response if len(response) == 6 and response.isascii() and
                    response.isdigit() else extract_otp(response))
            if not code or not code.isascii():
                raise ToolError("Chưa thấy mã SMS Amazon hợp lệ")
        except ToolError as exc:
            messagebox.showerror("Không đọc được mã SMS", str(exc), parent=self.root)
            return False
        except (OSError, webbrowser.Error):
            messagebox.showerror("Không đọc được mã SMS", "Không mở được trình duyệt",
                                 parent=self.root)
            return False
        self.jobs[index] = replace(job, account=replace(job.account, browser_otp=code))
        return True

    def _request_stop(self) -> None:
        self.cancel.set()
        getattr(self, "_pending_retries", set()).clear()
        self.post_menu_resume_after_stop.clear()
        for event in self.post_menu_stops.values():
            event.set()
        self.run_note.configure(text="Đã yêu cầu dừng · có thể bấm Làm lại để nhập mẻ mới", text_color=MUTED)
        self._refresh_devices()

    def _request_stop_selected(self) -> None:
        self._request_stop_phone(self.selected)

    def _can_stop_phone(self, index: int) -> bool:
        session = self.post_menu_sessions.get(index)
        state = self.status[index][1]
        event = self.phone_stop_after_step.get(index)
        return (index in self.jobs and not self.cancel.is_set() and
                not (event is not None and event.is_set()) and
                ((session is None and state == "menu_only") or
                 (self.running and state == "retry_queued" and
                  index in self._pending_retries) or
                 (self.running and session is None and
                  state in {"idle", "running", "created", "started", "installed", "queued"}) or
                 (session is None and getattr(self, "preparation_retry_workers", {}).get(index)
                  is not None and self.preparation_retry_workers[index].is_alive()) or
                 (session is not None and session.state == "RUNNING")))

    def _request_stop_phone(self, index: int) -> None:
        if not self._can_stop_phone(index):
            return
        queued_retry = self.status[index][1] == "retry_queued"
        event = self.phone_stop_after_step.setdefault(index, threading.Event())
        event.set()
        self._pending_retries.discard(index)
        if self.status[index][1] == "menu_only" and index not in self.post_menu_sessions:
            self.status[index] = (f"Máy {index + 1} đã dừng riêng tại menu", "stopped")
            self.run_note.configure(text=f"Đã dừng riêng Máy {index + 1} tại menu", text_color=MUTED)
            self._refresh_devices()
            return
        self.status[index] = (f"Máy {index + 1} đã hủy lượt Tiếp tục", "stopped") if queued_retry else (
            f"Máy {index + 1} đang dừng ở điểm an toàn", "stop_requested")
        self.run_note.configure(text=f"Đã yêu cầu dừng riêng Máy {index + 1}", text_color=MUTED)
        self._refresh_devices()

    def _account_for_profile(self, index: int) -> AccountData:
        row = self.values[index]
        label = f"Máy q{index + 1}"
        phone = row["phone"].get().strip()
        name = row["full_name"].get().strip()
        password = row["amazon_password"].get()
        if not PHONE.fullmatch(phone):
            raise ToolError(f"{label}: SĐT chưa hợp lệ")
        if not name or len(name) > 100:
            raise ToolError(f"{label}: tên Amazon chưa hợp lệ")
        if not password or any(ord(c) < 33 or ord(c) > 126 for c in password):
            raise ToolError(f"{label}: mật khẩu không được trống, chỉ nhận ASCII không dấu cách")
        url = validate_otp_url(row["otp_url"].get())
        card = validate_card(row["card"].get()) if row["card"].get() else ""
        return AccountData(phone, name, password, url, card)

    def _attach_from_menu(self) -> None:
        index = self.selected
        if (self.running or self.attach_in_progress or self._previous_work_busy() or
                index not in self.post_menu_step_factories or index in self.jobs):
            return
        try:
            account = self._account_for_profile(index)
        except ToolError as exc:
            messagebox.showerror(f"Dữ liệu q{index + 1}", str(exc))
            return
        self.attach_in_progress = True
        self.attaching_index = index
        self._set_editing(False)
        self.attach_profile_button.configure(state="disabled")
        self._refresh_devices()
        self.run_note.configure(text=f"Đang kiểm tra q{index + 1} và menu ba gạch...", text_color=BLUE)
        self.attach_worker = threading.Thread(target=self._probe_existing_profile,
                         args=(index, account, self.attach_events), daemon=True)
        self.attach_worker.start()

    def _probe_existing_profile(self, index: int, account: AccountData,
                                output=None) -> None:
        import pythoncom

        name = f"q{index + 1}"
        output = self.attach_events if output is None else output
        pythoncom.CoInitializeEx(pythoncom.COINIT_MULTITHREADED)
        try:
            profile = profile_status(name)
            if profile["state"] != "Running" or not profile.get("device_id"):
                raise ToolError(f"{name} đang Offline; Start {name} và mở menu ba gạch trước khi thử")
            shell = open_adb_shell(name, profile["device_id"])
            phone = CloudPhone(shell["serial"])
            verify_menu_open(phone, name)
            output.put(("ready", account, phone.serial))
        except Exception as exc:
            reason = str(exc) if isinstance(exc, ToolError) else type(exc).__name__
            output.put(("error", None, reason))
        finally:
            pythoncom.CoUninitialize()

    def _start_post_menu(self, index: int) -> None:
        """Start this phone's post-menu steps after its Amazon menu opens."""
        existing_session = self.post_menu_sessions.get(index)
        mode = (existing_session.registration.flow_mode
                if existing_session is not None and
                existing_session.registration.flow_mode != "auto"
                else getattr(self, "settings", AppSettings()).account_flow_mode)
        change_us_mode = mode == CHANGE_US_FROM_START
        factory = self.post_menu_step_factories.get(index)
        if factory is None and not change_us_mode:
            name = f"q{index + 1}"
            self.events.put((index,
                             f"{name} đã tới menu; chưa có hướng dẫn b1–b3 riêng nên chưa thể nối luồng chung b4–b11",
                             "menu_only", name))
            return
        if self.cancel.is_set() and index not in self.post_menu_sessions:
            self.events.put((index, f"q{index + 1} đã tới menu; mẻ đang dừng",
                             "stopped", f"q{index + 1}"))
            return
        job = self.jobs.get(index)
        serial = self.phone_serials.get(index)
        if job is None or (job.account is None and not change_us_mode):
            self.events.put((index,
                             f"q{index + 1} đã tới menu nhưng chưa có hàng Amazon trong mẻ",
                             "menu_only", f"q{index + 1}"))
            return
        if serial is None:
            self.events.put((index,
                             f"q{index + 1} đã tới menu nhưng chưa nối ADB; bấm Tiếp tục để nối lại",
                             "post_paused", f"q{index + 1}"))
            return
        session = self.post_menu_sessions.setdefault(
            index, PostMenuSession(job.batch_id, index,
                                   self.values[index]["profile_name"].get(),
                                   self.menu_opened_at.get(index)))
        prefix = getattr(self, 'proxy_postal_prefixes', {}).get(index)
        if prefix and session.registration.create_address_prefix is None:
            session.registration.create_address_proxy_prefix = prefix
        if session.state == "READY" and session.attempts == 0:
            session.registration.flow_mode = mode
            session.registration.login_followup = self.settings.login_followup
        if session.state not in {"READY", "PAUSED"}:
            return
        worker = self.post_menu_workers.get(index)
        if worker is not None and worker.is_alive():
            self.root.after(100, lambda slot=index: self._start_post_menu(slot))
            return
        steps = self.post_menu_steps.get(index)
        if steps is None or session.bound_serial != serial:
            steps = (build_change_us_steps(
                CloudPhone(serial), session.registration,
                lambda code, batch_id=job.batch_id, slot=index, output=self.otp_events:
                    output.put((batch_id, slot, code)),
                lambda status, batch_id=job.batch_id, slot=index, output=self.otp_status_events:
                    output.put((batch_id, slot, status)))
                     if change_us_mode else factory(
                CloudPhone(serial),
                lambda code, batch_id=job.batch_id, slot=index, output=self.otp_events:
                    output.put((batch_id, slot, code)),
                lambda status, batch_id=job.batch_id, slot=index, output=self.otp_status_events:
                    output.put((batch_id, slot, status)),
                session.registration,
            ))
            self.post_menu_steps[index] = steps
            session.bound_serial = serial
        stop = threading.Event()
        self.post_menu_stops[index] = stop
        after_step = self.phone_stop_after_step.setdefault(index, threading.Event())
        if index in self.post_menu_resume_after_stop:
            after_step.clear()
            self.post_menu_resume_after_stop.discard(index)
        worker = threading.Thread(target=self._run_post_menu,
                                  args=(session, job, steps, stop), daemon=True,
                                  kwargs={"context": {"serials": self.phone_serials,
                                      "steps": self.post_menu_steps, "factories": self.post_menu_step_factories,
                                      "events": self.events, "otp": self.otp_events,
                                      "otp_status": self.otp_status_events,
                                      "after_step": after_step}})
        self.post_menu_workers[index] = worker
        worker.start()

    def _run_post_menu(self, session: PostMenuSession, job: RunJob,
                       steps: tuple[PostMenuStep, ...],
                       stop: threading.Event, context=None) -> None:
        import pythoncom

        pythoncom.CoInitializeEx(pythoncom.COINIT_MULTITHREADED)
        context = context if context is not None else {
            "serials": self.phone_serials, "steps": self.post_menu_steps,
            "factories": self.post_menu_step_factories, "events": self.events,
            "otp": self.otp_events, "otp_status": self.otp_status_events,
            "after_step": self.phone_stop_after_step.setdefault(job.index, threading.Event())}
        try:
            def route(current, active_job, deadline, active_stop):
                if session.registration.flow_mode == CHANGE_US_FROM_START:
                    return None
                if context["factories"].get(active_job.index) is build_random_steps:
                    return None  # The random prefix also runs on list menus.
                phone = CloudPhone(context["serials"][active_job.index])
                return route_list_menu(phone, steps, current, session,
                                       deadline, active_stop)

            def reconcile(current, active_job, deadline, active_stop):
                nonlocal steps
                phone = CloudPhone(context["serials"][active_job.index])
                target = resume_common_index(phone, steps, current,
                                             deadline, active_stop,
                                             session.registration, active_job)
                if target == current and session.bound_serial == phone.serial:
                    return None
                factory = context["factories"][job.index]
                replacement = factory(
                    phone,
                    lambda code, batch_id=active_job.batch_id, slot=job.index:
                        context["otp"].put((batch_id, slot, code)),
                    lambda status, batch_id=active_job.batch_id, slot=job.index:
                        context["otp_status"].put((batch_id, slot, status)),
                    session.registration,
                )
                context["steps"][job.index] = replacement
                session.bound_serial = phone.serial
                steps = replacement
                return target, replacement

            from .isolated_reader import phone_reader
            with phone_reader(context["serials"][job.index], stop):
                session.run(job, steps,
                            lambda index, message, state, name:
                                context["events"].put((index, message, state, name)),
                            stop, reconcile=(None if session.registration.flow_mode == CHANGE_US_FROM_START
                                             else reconcile), route=route,
                            stop_after_step=context.get("after_step"))
        finally:
            pythoncom.CoUninitialize()

    def _start(self) -> None:
        self._launch(list(range(int(self.count.get()))))

    def _resume_restored(self) -> None:
        if self.restored_batch:
            slots = _automatic_resume_slots(self.restored_batch[1],
                                            self.settings.start_group_size)
            if slots:
                self._launch(slots)

    def _launch(self, indices: list[int], *, manual_override: bool = False) -> None:
        if self.running or self.attach_in_progress or self._previous_work_busy():
            return
        if self.registry is None:
            messagebox.showerror("Danh sách Profile", self.registry_error)
            return
        try:
            if not self.jobs:
                issue = self._input_issue()
                if issue:
                    raise ToolError(issue)
                for index in range(int(self.count.get())):
                    values = {key: item.get() for key, item in self.values[index].items()}
                    proxy = ProxyConfig("socks5", values["host"].strip(),
                                        int(values["port"]), values["username"],
                                        values["proxy_password"])
                    fallbacks = tuple(self.proxy_fallbacks) if index == 0 else ()
                    account = (AccountData(
                        values["phone"].strip(), values["full_name"].strip(),
                        values["amazon_password"], values["otp_url"].strip(),
                        values["card"].strip(),
                    ) if values["phone"] else None)
                    self.jobs[index] = RunJob(index, self.draft.batch_id, proxy,
                                              fallbacks, account)
                self.draft.locked = True
                self._set_editing(False)
            if any(index not in self.jobs for index in indices):
                raise ToolError("Máy này chưa được nối vào mẻ đang thử q1")
            for index in indices:
                if index in self._edited_locked_rows:
                    self._sync_edited_locked_row(index)
            jobs = [self.jobs[index] for index in indices]
        except (ToolError, ValueError) as exc:
            messagebox.showerror("Dữ liệu chưa hợp lệ", str(exc))
            return
        self.running = True
        self.run_group_size = self.settings.start_group_size
        self.run_hide_profile_creation = self.settings.hide_profile_creation
        self.cancel.clear()
        for index in indices:
            self.phone_stop_after_step.setdefault(index, threading.Event()).clear()
        self.run_button.configure(state="disabled")
        self.settings_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.reset_button.configure(state="disabled")
        self._refresh_devices()
        self.run_note.configure(text="Đang tạo Profile và mở máy song song...", text_color=BLUE)
        context = {"registry": self.registry, "events": self.events,
                   "stop": self.cancel, "serials": self.phone_serials,
                   "proxy_prefixes": self.proxy_postal_prefixes,
                   "opened": self.menu_opened_at, "group": self.run_group_size,
                   "hide": self.run_hide_profile_creation,
                   "phone_stops": self.phone_stop_after_step,
                   "manual_slots": self.manual_slots,
                   "manual_override": manual_override,
                   "automatic_start_slots": None}
        self.batch_worker = threading.Thread(target=self._run, args=(jobs, context), daemon=True)
        self.batch_worker.start()

    def _run(self, jobs: list[RunJob], context=None) -> None:
        context = context if context is not None else {
            "registry": self.registry, "events": self.events, "stop": self.cancel,
            "serials": self.phone_serials, "opened": self.menu_opened_at,
            "proxy_prefixes": getattr(self, 'proxy_postal_prefixes', {}),
            "group": self.run_group_size, "hide": self.run_hide_profile_creation,
            "phone_stops": self.phone_stop_after_step,
            "manual_slots": getattr(self, 'manual_slots', set()),
            "automatic_start_slots": None}
        initialized = False
        message = "Mẻ đã kết thúc"
        final_state = "finished"
        try:
            import pythoncom
            pythoncom.CoInitializeEx(pythoncom.COINIT_MULTITHREADED)
            initialized = True
            def emit(index: int, update: str, state: str, name: str | None) -> None:
                if state == "done":
                    context["opened"].setdefault(index, time.monotonic())
                context["events"].put((index, update, state, name))

            summary = run_batch(
                jobs, context["registry"],
                emit,
                context["stop"],
                start_group_size=context["group"],
                hide_profile_creation=context["hide"],
                menu_ready=lambda index, _name, _device_id, serial:
                    context["serials"].__setitem__(index, serial),
                proxy_prefix_ready=lambda index, prefix:
                    context.setdefault("proxy_prefixes", {}).__setitem__(index, prefix),
                stop_after_step=context.get("phone_stops"),
                manual_slots=context.get("manual_slots"),
                manual_override=context.get("manual_override", False),
                automatic_start_slots=context.get("automatic_start_slots"),
            )
            message = (f"Mẻ kết thúc: {summary['menu_open']} tới menu · "
                       f"{summary['error']} lỗi · {summary['stopped']} dừng"
                       " · bấm trạng thái để xem lỗi" if summary["error"] else
                       f"Mẻ kết thúc: {summary['menu_open']} tới menu · 0 lỗi · "
                       f"{summary['stopped']} dừng")
            final_state = "error" if summary["error"] else "finished"
        except Exception as exc:
            message = f"Mẻ dừng do lỗi: {exc}"
            final_state = "error"
        finally:
            if initialized:
                pythoncom.CoUninitialize()
            context["events"].put((context.get("final_index", -1), message, final_state, None))

    def _poll(self) -> None:
        try:
            while True:
                state, account, detail = self.attach_events.get_nowait()
                self.attach_in_progress = False
                index = self.attaching_index
                if self.cancel.is_set():
                    self.run_note.configure(text="Đã dừng gắn máy · có thể Làm lại hoặc thử gắn lại", text_color=MUTED)
                    self._refresh_devices()
                    continue
                if state == "ready" and account is not None and detail is not None:
                    self.cancel.clear()
                    self.jobs[index] = RunJob(index, self.draft.batch_id, None,
                                          account=account)
                    self.draft.locked = True
                    self._set_editing(False)
                    self.phone_serials[index] = detail
                    self.menu_opened_at[index] = time.monotonic()
                    self.status[index] = (f"q{index + 1} đã ở menu ba gạch", "done")
                    self._refresh_devices()
                    self._start_post_menu(index)
                else:
                    if not self.draft.locked:
                        self._set_editing(True)
                    self.run_note.configure(text=detail or f"Không gắn được q{index + 1}",
                                            text_color=RED)
                    self._refresh_devices()
        except queue.Empty:
            pass
        try:
            while True:
                index, message, state, name = self.events.get_nowait()
                if index == -2:
                    self.run_note.configure(text=message,
                                            text_color=RED if state == "error" else MUTED)
                    self._refresh_devices()
                    continue
                if index == -1:
                    self.running = False
                    self.run_button.configure(state="normal")
                    self.settings_button.configure(state="normal")
                    self.stop_button.configure(state="disabled")
                    self.reset_button.configure(state="normal")
                    self._refresh_devices()
                    self.run_note.configure(
                        text=message,
                        text_color=RED if state == "error" else MUTED,
                    )
                    pending = sorted(getattr(self, "_pending_retries", set()))
                    if pending:
                        self._pending_retries.clear()
                        self._launch(pending, manual_override=True)
                else:
                    if name:
                        self.values[index]["profile_name"].set(name)
                    session = self.post_menu_sessions.get(index)
                    stop_request = self.phone_stop_after_step.get(index)
                    if state == "menu_only" and stop_request is not None and stop_request.is_set():
                        continue  # A late menu event must not undo this phone's stop.
                    if state in {"post_stopped", "post_paused", "post_done"} and \
                            session is not None and \
                            session.state == "RUNNING" and \
                            (stop_request is None or not stop_request.is_set()):
                        continue  # An older terminal event arrived after this phone resumed.
                    if (state == "post_stopped" and
                            index in self.post_menu_resume_after_stop and
                            not self.cancel.is_set()):
                        self.status[index] = (
                            f"Máy {index + 1} đang nối lại từ điểm dừng",
                            "resume_queued")
                        self._schedule_refresh()
                        self._start_post_menu(index)
                        continue
                    if state in {"post_paused", "post_done"}:
                        self.post_menu_resume_after_stop.discard(index)
                    if state == "post_running" and stop_request is not None and \
                            stop_request.is_set():
                        message = (f"Máy {index + 1} sẽ tiếp tục sau khi dừng an toàn"
                                   if index in self.post_menu_resume_after_stop else
                                   f"Máy {index + 1} đang dừng ở điểm an toàn")
                        state = ("resume_queued" if index in self.post_menu_resume_after_stop
                                 else "stop_requested")
                    self.status[index] = (message, state)
                    if self.selected == index:
                        self._refresh_selected_progress()
                    self._schedule_refresh()
                    if state == "done":
                        self._start_post_menu(index)
        except queue.Empty:
            pass
        try:
            while True:
                batch_id, index, code = self.otp_events.get_nowait()
                self.show_otp(batch_id, index, code)
        except queue.Empty:
            pass
        try:
            while True:
                batch_id, index, status = self.otp_status_events.get_nowait()
                self.show_otp_status(batch_id, index, status)
        except queue.Empty:
            pass
        if getattr(self, "_draining_workers", []) and not self._previous_work_busy():
            self._draining_workers = []
            self.run_note.configure(text="Tác vụ cũ đã dừng · sẵn sàng chạy mẻ mới", text_color=MUTED)
            self._refresh_devices()
        self.root.after(150, self._poll)

    def run(self) -> None:
        self.root.mainloop()


def main() -> None:
    Window().run()


if __name__ == "__main__":
    main()
