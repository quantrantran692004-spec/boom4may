"""Swarmote V3 presentation tokens and static Lucide assets for Tk.

The SVG originals and their 4x PNG masks ship with the app. Runtime rendering
uses Pillow (already a dependency), so no SVG engine or network is required.
"""
from functools import lru_cache
from pathlib import Path
import tkinter as tk

import customtkinter as ctk
from PIL import Image

BG = "#F5F9FA"
HEADER = "#DAEFF1"
HEADER_BORDER = "#BBDCE0"
HEADER_WAVES = ("#CFEEED", "#BFE7E9", "#B0E1E4")
LOGO_BG = "#087C86"
HEADER_CONTROL = "#E8F3F4"
HEADER_TEXT = "#344950"
SETTINGS_ICON = "#42636A"
FOOTER = "#CFE9EB"
FOOTER_BORDER = "#B8DDE1"
FOOTER_TEXT = "#153D50"
FOOTER_ERROR = "#AF3042"
FOOTER_DISABLED_BG = "#DFEAF0"
FOOTER_DISABLED_TEXT = "#6C8091"
FOOTER_DISABLED_BORDER = "#B8CEDA"
BATCH_STOP_BG = "#DA323E"
BATCH_STOP_HOVER = "#BD2136"
SURFACE = "#FEFEFE"
INPUT = "#FFFFFF"
WHITE = "#FFFFFF"
INK = "#082D3B"
BODY = "#183747"
MUTED = "#3F6074"
PLACEHOLDER = "#5E7182"
BLUE = "#006F7B"
BLUE_HOVER = "#005C67"
PALE = "#F1F6FE"
BORDER = "#D6E5EB"
FIELD_BORDER = "#B9CFDD"
FOCUS = "#006F7B"
SECONDARY = "#FFFFFF"
SECONDARY_HOVER = "#EAF1F6"
SECONDARY_BORDER = "#9FB6C7"
UTILITY_TEXT = "#294F61"
IMPORT_BG = "#FFFFFF"
IMPORT_HOVER = "#E9F5F6"
IMPORT_TEXT = "#07556B"
IMPORT_BORDER = "#B2D0DB"
PROCESSING = "#0055DE"
PROGRESS_TEXT = "#1C3D63"
CONTINUE_FACE = "#F8FAFF"
CONTINUE_BORDER = "#8BAFFF"
CONTINUE_TEXT = "#0055DE"
CONTINUE_FACE_HOVER = "#E8EFFF"
GREEN = "#087126"
RED = "#C32236"
ROW_ALT = "#FFFFFF"
ROW_HOVER = "#F0F5FC"
ROW_BORDER = "#C7DDE6"
ROW_SELECTED_BORDER = "#075CFF"
ROW_INACTIVE = "#F3F6F9"
TABLE_HEADER = "#F8FAFC"
TABLE_HEADER_TEXT = "#475F73"
DISABLED_BG = "#EAF0F5"
DISABLED_TEXT = "#718296"
CONTINUE_BG = "#0455D3"
CONTINUE_HOVER = "#0449B7"
PRIMARY_PRESSED = "#033C97"
STOP_BG = "#FFF6F7"
STOP_HOVER = "#FCE7EB"
STOP_BORDER = "#D98B98"
SCROLLBAR = "#C1CCD2"
SCROLLBAR_HOVER = "#9DADB6"
ICON_DEFAULT = "#355667"
FONT_FAMILY = "Segoe UI"
FONT_SEMIBOLD = "Segoe UI Semibold"  # same Windows family, native 600 face

ICON_SECTION = 20
ICON_BUTTON = 16
ICON_STATUS = 16
ICON_TABLE = 14
ICON_GAP = 6

STATES = {
    "success": (GREEN, "#EAF6EF", "circle-check"),
    "processing": (PROCESSING, PALE, "loader-circle"),
    "waiting": ("#B45300", "#FFF4DF", "clock"),
    "error": (RED, STOP_BG, "circle-alert"),
    "stopped": (RED, STOP_BG, "square"),
    "inactive": (MUTED, DISABLED_BG, "clock"),
}


def state_style(state):
    if state in {"done", "post_done"}:
        return STATES["success"]
    if state in {"error", "uncertain", "post_paused"}:
        return STATES["error"]
    if state in {"stopped", "post_stopped", "stop_requested"}:
        return STATES["stopped"]
    if state in {"queued", "retry_queued", "resume_queued"}:
        return STATES["waiting"]
    if state in {"running", "created", "started", "installed", "post_running"}:
        return STATES["processing"]
    return STATES["inactive"]


def status_title(state):
    """Short presentation label; the original message is always kept separately."""
    return {
        "done": "Đã tới menu", "post_done": "Hoàn tất", "error": "Cần kiểm tra",
        "uncertain": "Chưa xác định", "post_paused": "Cần kiểm tra",
        "stopped": "Đã dừng", "post_stopped": "Đã dừng", "stop_requested": "Đang dừng",
        "queued": "Đang chờ", "retry_queued": "Chờ tiếp tục", "resume_queued": "Đang nối lại",
        "running": "Đang chuẩn bị", "created": "Đã tạo Profile", "started": "Đã mở máy",
        "installed": "Đã cài Amazon", "post_running": "Đang xử lý",
        "menu_only": "Đã tới menu", "idle": "Chưa chạy",
    }.get(state, "Trạng thái máy")


def ui_font(size=16, weight="normal"):
    if weight == "semibold":
        return ctk.CTkFont(FONT_SEMIBOLD, size, weight="normal")
    return ctk.CTkFont(FONT_FAMILY, size, weight=weight)


def startup_geometry(screen_width, screen_height, scale):
    """Open close to full screen while leaving room for native window chrome."""
    width = max(400, min(1840, screen_width - 32))
    height = max(300, min(960, screen_height - 104))
    x = max(0, round((screen_width - width) / 2))
    y = max(12, round((screen_height - height) / 2 - 40))
    return round(width / scale), round(height / scale), x, y


@lru_cache(maxsize=256)
def icon(name, color=ICON_DEFAULT, size=ICON_BUTTON, gap=0):
    path = Path(__file__).with_name("assets") / "icons" / f"{name}.png"
    with Image.open(path) as source:
        tinted = Image.new("RGBA", source.size, color)
        tinted.putalpha(source.getchannel("A"))
    if gap:
        padded = Image.new("RGBA", (round(tinted.width * (size + gap) / size), tinted.height))
        padded.paste(tinted, (0, 0))
        tinted = padded
    return ctk.CTkImage(light_image=tinted, dark_image=tinted, size=(size + gap, size))


LABEL_ICONS = {
    "Số máy": "smartphone", "Dán dữ liệu": "clipboard-list",
    "Proxy": "globe", "Thông tin Amazon": "user-round",
    "Số điện thoại": "phone", "Mật khẩu Amazon": "key-round",
    "Thẻ của số điện thoại này": "credit-card",
    "URL OTP của số điện thoại này": "link", "Mã OTP": "shield-check",
}


class Button(ctk.CTkButton):
    """Button skin; command, state and geometry remain owned by the caller."""
    def __init__(self, master, *, role="secondary", icon_name=None,
                 accessible_name=None, **kwargs):
        self.skin_role = role
        self.icon_name = icon_name
        self.accessible_name = accessible_name or kwargs.get("text", "")
        self._skin_ready = False
        super().__init__(master, **kwargs)
        self._font.configure(weight="normal")
        if role in {"import", "run", "batch-stop"}:
            self._font.configure(family=FONT_SEMIBOLD, size=15)
        self._skin_ready = True
        self._skin()
        if role in {"primary", "run"}:
            self.bind("<ButtonPress-1>", self._press, add="+")
            self.bind("<ButtonRelease-1>", lambda _: self._skin(), add="+")
        if accessible_name:
            self._canvas.configure(takefocus=1)
            self._canvas.bind("<Return>", lambda _: self.invoke(), add="+")
            self._canvas.bind("<space>", lambda _: self.invoke(), add="+")
            self._tooltip = Tooltip(self, accessible_name)
            # Tk canvas controls do not have an aria-label; expose the native
            # window name as well as the keyboard focus and visible tooltip.
            if self.winfo_toplevel().tk.call("tk", "windowingsystem") == "win32":
                import ctypes
                ctypes.windll.user32.SetWindowTextW(self._canvas.winfo_id(), accessible_name)

    def configure(self, require_redraw=False, **kwargs):
        if getattr(self, "_skin_ready", False):
            for key in ("fg_color", "hover_color", "text_color", "text_color_disabled",
                        "border_color", "image"):
                kwargs.pop(key, None)
        super().configure(require_redraw=require_redraw, **kwargs)
        if getattr(self, "_skin_ready", False):
            self._skin()

    def _skin(self):
        disabled = self.cget("state") == "disabled"
        key = (disabled, self.skin_role, self.icon_name)
        if getattr(self, "_skin_key", None) == key:
            return
        self._skin_key = key
        if disabled:
            face, hover, text, border = DISABLED_BG, DISABLED_BG, DISABLED_TEXT, BORDER
            if self.skin_role in {"run", "batch-stop", "footer-secondary"}:
                face, hover, text, border = (FOOTER_DISABLED_BG, FOOTER_DISABLED_BG,
                                             FOOTER_DISABLED_TEXT, FOOTER_DISABLED_BORDER)
        elif self.skin_role in {"primary", "run"}:
            face, hover, text, border = CONTINUE_BG, CONTINUE_HOVER, WHITE, CONTINUE_BG
        elif self.skin_role == "batch-stop":
            face, hover, text, border = BATCH_STOP_BG, BATCH_STOP_HOVER, WHITE, BATCH_STOP_BG
        elif self.skin_role == "footer-secondary":
            face, hover, text, border = SURFACE, SECONDARY_HOVER, INK, BORDER
        elif self.skin_role in {"stop", "danger"}:
            face, hover, text, border = STOP_BG, STOP_HOVER, RED, STOP_BORDER
        elif self.skin_role == "settings":
            face, hover, text, border = SURFACE, SECONDARY_HOVER, SETTINGS_ICON, HEADER_BORDER
        elif self.skin_role == "import":
            face, hover, text, border = IMPORT_BG, IMPORT_HOVER, IMPORT_TEXT, IMPORT_BORDER
        elif self.skin_role == "continue":
            face, hover, text, border = CONTINUE_FACE, CONTINUE_FACE_HOVER, CONTINUE_TEXT, CONTINUE_BORDER
        else:
            face, hover, text, border = SECONDARY, SECONDARY_HOVER, UTILITY_TEXT, SECONDARY_BORDER
        options = dict(fg_color=face, hover_color=hover, text_color=text,
                       text_color_disabled=text if disabled else DISABLED_TEXT, border_color=border)
        if self.icon_name:
            options.update(image=icon(self.icon_name, text), compound="left",
                           border_spacing=ICON_GAP)
        super().configure(**options)

    def _press(self, _event):
        if self.cget("state") != "disabled":
            self._skin_key = None
            super().configure(fg_color=PRIMARY_PRESSED, hover_color=PRIMARY_PRESSED)


class Entry(ctk.CTkEntry):
    def __init__(self, master, **kwargs):
        kwargs["font"] = ui_font(16)
        kwargs.update(fg_color=INPUT, text_color=BODY,
                      placeholder_text_color=PLACEHOLDER, border_color=FIELD_BORDER)
        super().__init__(master, **kwargs)
        self.bind("<FocusIn>", lambda _: self.configure(border_color=FOCUS), add="+")
        self.bind("<FocusOut>", lambda _: self.configure(border_color=FIELD_BORDER), add="+")


class FooterNote(ctk.CTkLabel):
    """Routine progress stays quiet; errors retain their meaningful color."""
    def configure(self, require_redraw=False, **kwargs):
        if "text_color" in kwargs:
            kwargs["text_color"] = FOOTER_ERROR if kwargs["text_color"] == RED else FOOTER_TEXT
        super().configure(require_redraw=require_redraw, **kwargs)


class TableText(tk.Label):
    """Small native table label with the same DPI scaling as CTk fields."""
    def __init__(self, master, **kwargs):
        self._cell_font = kwargs.pop("font")
        self._wrap = kwargs.pop("wraplength", 0)
        self._padding = kwargs.pop("padx", 6), kwargs.pop("pady", 4)
        scale = ctk.ScalingTracker.get_widget_scaling(master)
        super().__init__(master, font=self._cell_font.create_scaled_tuple(scale),
                         wraplength=round(self._wrap * scale),
                         padx=round(self._padding[0] * scale),
                         pady=round(self._padding[1] * scale), **kwargs)
        ctk.ScalingTracker.add_widget(self._scale, self)
        self.bind("<Destroy>", self._dispose, add="+")

    def _scale(self, scale, _window_scale):
        self.configure(font=self._cell_font.create_scaled_tuple(scale),
                       wraplength=round(self._wrap * scale),
                       padx=round(self._padding[0] * scale),
                       pady=round(self._padding[1] * scale))

    def set_wrap(self, width):
        if self._wrap != width:
            self._wrap = width
            self.configure(wraplength=round(width * ctk.ScalingTracker.get_widget_scaling(self)))

    def set_font(self, size, weight="normal"):
        self._cell_font = ui_font(size, weight)
        self.configure(font=self._cell_font.create_scaled_tuple(
            ctk.ScalingTracker.get_widget_scaling(self)))

    def _dispose(self, event):
        if event.widget is self:
            ctk.ScalingTracker.remove_widget(self._scale, self)


class HeaderWave(ctk.CTkFrame):
    """Static, resize-only vector decoration behind the header controls."""
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=HEADER, corner_radius=0, **kwargs)
        self.wave = tk.Canvas(self, bg=HEADER, highlightthickness=0, borderwidth=0)
        self.wave.place(relx=0, rely=0, relwidth=1, relheight=1)
        self._wave_shapes = [self.wave.create_polygon(0, 0, 0, 0, fill=color,
                             outline="", smooth=True, splinesteps=24)
                             for color in HEADER_WAVES]
        self.wave.bind("<Configure>", self._draw_wave)

    def _draw_wave(self, event):
        width, height = event.width, event.height
        for shape, start in zip(self._wave_shapes, (0.64, 0.77, 0.88)):
            self.wave.coords(shape,
                width * start, height, width * (start + .06), height * .7,
                width * (start + .10), 0, width, 0,
                width * 1.1, height * .5, width, height)


class MachineCell(tk.Frame):
    """Phone identity and Profile caption, with native labels that follow DPI."""
    def __init__(self, master, **kwargs):
        background = kwargs.get("bg", SURFACE)
        super().__init__(master, bg=background, borderwidth=0)
        self.full_text = ""
        self._identity_width = 155
        self.pack_propagate(False)
        self.phone = tk.Label(self, bg=WHITE, borderwidth=0,
                              highlightthickness=1, highlightbackground=BORDER)
        self.phone.pack(side="left")
        self.divider = tk.Frame(self, bg=BORDER, width=1)
        self.divider.pack(side="right", fill="y", pady=6)
        self.copy = tk.Frame(self, bg=background, borderwidth=0)
        self.copy.pack(side="left", fill="x", expand=True)
        self.primary = TableText(self.copy, text="", bg=background, fg=INK,
                                 font=ui_font(17, "semibold"), wraplength=88,
                                 anchor="w", justify="left", padx=0, pady=0)
        self.caption = TableText(self.copy, text="", bg=background, fg=MUTED,
                                 font=ui_font(14), wraplength=88,
                                 anchor="w", justify="left", padx=0, pady=1)
        self.primary.pack(fill="x")
        self.caption.pack(fill="x")
        self._update_icon(ctk.ScalingTracker.get_widget_scaling(self), 1)
        ctk.ScalingTracker.add_widget(self._update_icon, self)
        self.bind("<Destroy>", self._dispose_icon, add="+")

    def configure(self, cnf=None, **kwargs):
        if not hasattr(self, "primary"):
            return super().configure(cnf, **kwargs)
        if "text" in kwargs:
            self.full_text = kwargs.pop("text")
            title, _, profile = self.full_text.partition("\n")
            self.primary.configure(text=title)
            self.caption.configure(text=f"Profile · {profile}" if profile else "Chưa dùng")
        if "fg" in kwargs:
            self.primary.configure(fg=kwargs.pop("fg"))
        if "bg" in kwargs:
            for child in (self.copy, self.primary, self.caption):
                child.configure(bg=kwargs["bg"])
        return super().configure(cnf, **kwargs)

    def cget(self, key):
        return self.full_text if key == "text" else super().cget(key)

    def set_wrap(self, width):
        self._identity_width = width
        self.configure(width=round(width * ctk.ScalingTracker.get_widget_scaling(self)))
        for label in (self.primary, self.caption):
            label.set_wrap(max(70, width - 56))

    def _update_icon(self, scale, _window_scale):
        self.configure(width=round(self._identity_width * scale), height=round(50 * scale))
        self._phone_image = icon("smartphone", INK, 24)
        self.phone.configure(image=self._phone_image.create_scaled_photo_image(scale, "light"),
                             width=round(38 * scale), height=round(46 * scale))
        self.phone.pack_configure(padx=(0, round(12 * scale)))

    def _dispose_icon(self, event):
        if event.widget is self:
            ctk.ScalingTracker.remove_widget(self._update_icon, self)

    def bind(self, sequence=None, func=None, add=None):
        result = super().bind(sequence, func, add)
        if hasattr(self, "primary"):
            for child in (self.phone, self.divider, self.copy, self.primary, self.caption):
                child.bind(sequence, func, add)
        return result


class StatusCell(tk.Frame):
    """Two visual levels, retaining the full status for tooltip and selection."""
    def __init__(self, master, **kwargs):
        background = kwargs.get("bg", SURFACE)
        super().__init__(master, bg=background, borderwidth=0)
        self.full_text = ""
        self._description_indent = 22
        self._state_symbol, self._state_color = "clock", MUTED
        self.heading = tk.Frame(self, bg=background, borderwidth=0)
        self.state_icon = tk.Label(self.heading, bg=background, borderwidth=0, padx=0, pady=0)
        self.state_icon.pack(side="left", padx=(6, 0))
        self.primary = TableText(self.heading, text="", bg=background, fg=BODY,
                                 font=ui_font(16, "semibold"), wraplength=150, anchor="w",
                                 justify="left", padx=6, pady=2)
        self.description = TableText(self, text="", bg=background, fg=MUTED,
                                     font=ui_font(14), wraplength=150, anchor="w",
                                     justify="left", padx=6, pady=1)
        self.primary.pack(side="left", fill="x", expand=True)
        self.heading.pack(fill="x")
        self.description.pack(fill="x", padx=(22, 0))
        self._update_icon(ctk.ScalingTracker.get_widget_scaling(self), 1)
        ctk.ScalingTracker.add_widget(self._update_icon, self)
        self.bind("<Destroy>", self._dispose_icon, add="+")
        self._tooltip = Tooltip(self, lambda: self.full_text)

    def configure(self, cnf=None, **kwargs):
        if not hasattr(self, "primary"):
            return super().configure(cnf, **kwargs)
        text = kwargs.pop("text", None)
        title = kwargs.pop("title", None)
        color = kwargs.pop("fg", None)
        symbol = kwargs.pop("symbol", None)
        if text is not None:
            self.full_text = text
            message, _, otp = text.partition("\nOTP: ")
            compact = " ".join(message.split())
            if compact == title:
                compact = ""
            if len(compact) > 48:
                compact = compact[:47].rstrip() + "…"
            if otp and otp != "Chưa yêu cầu mã":
                compact = f"{compact}\nOTP: {otp}".strip()
            self.description.configure(text=compact)
            if compact:
                self.description.pack(fill="x", padx=(self._description_indent, 0))
            else:
                self.description.pack_forget()
        if title is not None:
            self.primary.configure(text=title)
        if color is not None:
            self.primary.configure(fg=color)
            processing = color == PROCESSING
            if getattr(self, "_description_processing", None) != processing:
                self._description_processing = processing
                self.description.set_font(15 if processing else 14,
                                          "semibold" if processing else "normal")
                self.description.configure(fg=PROGRESS_TEXT if processing else MUTED)
        if color is not None or symbol is not None:
            changed = (color or self._state_color, symbol or self._state_symbol)
            if changed != (self._state_color, self._state_symbol):
                self._state_color, self._state_symbol = changed
                self._update_icon(ctk.ScalingTracker.get_widget_scaling(self), 1)
        if "bg" in kwargs:
            self.heading.configure(bg=kwargs["bg"])
            self.state_icon.configure(bg=kwargs["bg"])
            self.primary.configure(bg=kwargs["bg"])
            self.description.configure(bg=kwargs["bg"])
        return super().configure(cnf, **kwargs)

    def cget(self, key):
        return self.full_text if key == "text" else super().cget(key)

    def set_wrap(self, width):
        self.primary.set_wrap(max(100, width - 24))
        self.description.set_wrap(max(100, width - 24))

    def _update_icon(self, scale, _window_scale):
        self._icon_image = icon(self._state_symbol, self._state_color, ICON_STATUS)
        self.state_icon.configure(image=self._icon_image.create_scaled_photo_image(scale, "light"))
        self.state_icon.pack_configure(padx=(round(6 * scale), 0))
        self._description_indent = round(22 * scale)
        if self.description.winfo_manager():
            self.description.pack_configure(padx=(self._description_indent, 0))

    def _dispose_icon(self, event):
        if event.widget is self:
            ctk.ScalingTracker.remove_widget(self._update_icon, self)

    def bind(self, sequence=None, func=None, add=None):
        result = super().bind(sequence, func, add)
        if hasattr(self, "primary"):
            for child in (self.heading, self.state_icon, self.primary, self.description):
                child.bind(sequence, func, add)
        return result


class Tooltip:
    def __init__(self, widget, text):
        self.widget, self.text, self.window = widget, text, None
        widget.bind("<Enter>", self.show, add="+")
        widget.bind("<Leave>", self.hide, add="+")
        if hasattr(widget, "_canvas"):
            widget._canvas.bind("<FocusIn>", self.show, add="+")
            widget._canvas.bind("<FocusOut>", self.hide, add="+")
        widget.bind("<Destroy>", self.hide, add="+")

    def show(self, _event=None):
        if self.window is not None:
            return
        self.window = tk.Toplevel(self.widget)
        self.window.overrideredirect(True)
        self.window.geometry(f"+{self.widget.winfo_rootx()}+{self.widget.winfo_rooty() + self.widget.winfo_height() + 6}")
        value = self.text() if callable(self.text) else self.text
        if not value:
            self.hide()
            return
        tk.Label(self.window, text=value, bg=SURFACE, fg=BODY,
                 font=(FONT_FAMILY, 10), wraplength=440, justify="left",
                 padx=8, pady=4, borderwidth=1, relief="solid").pack()

    def hide(self, _event=None):
        if self.window is not None:
            self.window.destroy()
            self.window = None
