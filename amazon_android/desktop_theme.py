"""Swarmote V2 presentation tokens and static Lucide assets for Tk.

The SVG originals and their 4x PNG masks ship with the app. Runtime rendering
uses Pillow (already a dependency), so no SVG engine or network is required.
"""
from functools import lru_cache
from pathlib import Path
import tkinter as tk

import customtkinter as ctk
from PIL import Image

BG = "#E8EEEE"
HEADER = "#BCE4E4"
FOOTER = "#F0F5F5"
SURFACE = "#F8FAFA"
INPUT = "#F0F4F4"
WHITE = "#FFFFFF"
INK = "#192D31"
BODY = "#293D42"
MUTED = "#58686D"
# Two foregrounds are slightly darker than the supplied table to meet its
# >=4.5:1 text requirement on the supplied backgrounds (originals: 4.44/4.39).
PLACEHOLDER = "#637277"
BLUE = "#006D77"
BLUE_HOVER = "#006D77"
PALE = "#E3F1F1"
BORDER = "#D3DFDF"
FIELD_BORDER = "#C9D6D7"
FOCUS = "#006D77"
SECONDARY = "#E1F0F0"
SECONDARY_HOVER = "#D3E9E9"
SECONDARY_BORDER = "#C9DDDE"
GREEN = "#277353"
RED = "#B34545"
ROW_ALT = "#F1F5F5"
ROW_HOVER = "#EDF5F5"
TABLE_HEADER = "#E7EFEF"
TABLE_HEADER_TEXT = "#40575B"
DISABLED_BG = "#E4EAEA"
DISABLED_TEXT = "#768387"
CONTINUE_BG = "#F3D36C"
CONTINUE_HOVER = "#EAC65A"
PRIMARY_PRESSED = "#DEB94E"
STOP_BG = "#F5E7E7"
STOP_HOVER = "#F5E7E7"
SCROLLBAR = "#A5B8BB"
SCROLLBAR_HOVER = "#879FA3"

ICON_SECTION = 20
ICON_BUTTON = 16
ICON_STATUS = 16
ICON_TABLE = 14
ICON_GAP = 6

STATES = {
    "success": (GREEN, "#E4F1E9", "circle-check"),
    "processing": (BLUE, "#E1F0F0", "loader-circle"),
    "waiting": ("#88651B", "#F5EDD9", "clock"),
    "error": (RED, "#F5E7E7", "circle-alert"),
    "stopped": (RED, "#F5E7E7", "square"),
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


@lru_cache(maxsize=256)
def icon(name, color=MUTED, size=ICON_BUTTON, gap=0):
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
    "MÁY": "smartphone", "PROXY": "globe", "AMAZON": "user-round",
    "TRẠNG THÁI": "activity", "THAO TÁC": "sliders-horizontal",
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
        self._skin_ready = True
        self._skin()
        if role == "primary":
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
        elif self.skin_role == "primary":
            face, hover, text, border = CONTINUE_BG, CONTINUE_HOVER, INK, CONTINUE_BG
        elif self.skin_role == "stop":
            face, hover, text, border = STOP_BG, STOP_HOVER, RED, STOP_BG
        else:
            face, hover, text, border = SECONDARY, SECONDARY_HOVER, BLUE, SECONDARY_BORDER
        options = dict(fg_color=face, hover_color=hover, text_color=text,
                       text_color_disabled=DISABLED_TEXT, border_color=border)
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
        kwargs.update(fg_color=INPUT, text_color=BODY,
                      placeholder_text_color=PLACEHOLDER, border_color=FIELD_BORDER)
        super().__init__(master, **kwargs)
        self.bind("<FocusIn>", lambda _: self.configure(border_color=FOCUS), add="+")
        self.bind("<FocusOut>", lambda _: self.configure(border_color=FIELD_BORDER), add="+")


class Tooltip:
    def __init__(self, widget, text):
        self.widget, self.text, self.window = widget, text, None
        widget.bind("<Enter>", self.show, add="+")
        widget.bind("<Leave>", self.hide, add="+")
        widget._canvas.bind("<FocusIn>", self.show, add="+")
        widget._canvas.bind("<FocusOut>", self.hide, add="+")
        widget.bind("<Destroy>", self.hide, add="+")

    def show(self, _event=None):
        if self.window is not None:
            return
        self.window = tk.Toplevel(self.widget)
        self.window.overrideredirect(True)
        self.window.geometry(f"+{self.widget.winfo_rootx()}+{self.widget.winfo_rooty() + self.widget.winfo_height() + 6}")
        tk.Label(self.window, text=self.text, bg=SURFACE, fg=BODY,
                 padx=8, pady=4, borderwidth=1, relief="solid").pack()

    def hide(self, _event=None):
        if self.window is not None:
            self.window.destroy()
            self.window = None
