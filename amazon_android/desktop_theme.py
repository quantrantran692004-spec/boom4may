"""Swarmote V3 presentation tokens and static Lucide assets for Tk.

The SVG originals and their 4x PNG masks ship with the app. Runtime rendering
uses Pillow (already a dependency), so no SVG engine or network is required.
"""
from functools import lru_cache
from pathlib import Path
import tkinter as tk

import customtkinter as ctk
from PIL import Image, ImageTk
from .desktop_art import rounded_surface, button_face, banner, phone_art, brand_art

BG = "#E9F3FC"
HEADER = "#DFEFF9"
HEADER_BORDER = "#B8DCEB"
HEADER_CONTROL = "#ECF8FF"
HEADER_TEXT = "#073B54"
SETTINGS_ICON = "#005370"
FOOTER = "#F3F9FD"
SURFACE = "#F5FAFE"
INPUT = "#F5F8FD"
WHITE = "#FFFFFF"
INK = "#07132F"
BODY = "#173F57"
MUTED = "#496486"
PLACEHOLDER = "#506A8B"  # supplied #687983 is only 4.12:1 on INPUT
BLUE = "#0754FB"
BLUE_HOVER = "#0044D7"
PALE = "#E7F6FF"
BORDER = "#D2E4F1"
FIELD_BORDER = "#B2CBE1"
FOCUS = "#0754FB"
SECONDARY = "#F5FAFE"
SECONDARY_HOVER = "#E4F5FF"
SECONDARY_BORDER = "#B8DDEB"
GREEN = "#12831E"
RED = "#CA1934"
ROW_ALT = "#F3F9FD"
ROW_HOVER = "#EDF8FF"
TABLE_HEADER = "#EFF6FC"
TABLE_HEADER_TEXT = "#496486"
DISABLED_BG = "#E5EEF5"
DISABLED_TEXT = "#8296A9"
CONTINUE_BG = "#0875F5"
CONTINUE_HOVER = "#005CE8"
PRIMARY_PRESSED = "#0044C7"
STOP_BG = "#FFF0F5"
STOP_HOVER = "#FADCE7"
STOP_BORDER = "#FFA5BC"
SCROLLBAR = "#C0D9E8"
SCROLLBAR_HOVER = "#80B9D2"
ICON_DEFAULT = "#006075"
FONT_FAMILY = "Segoe UI"
FONT_SEMIBOLD = "Segoe UI Semibold"  # same Windows family, native 600 face

ICON_SECTION = 24
ICON_BUTTON = 20
ICON_STATUS = 22
ICON_TABLE = 20
ICON_GAP = 6

STATES = {
    "success": (GREEN, "#E8F3EC", "circle-check"),
    "processing": (BLUE, PALE, "loader-circle"),
    "waiting": ("#EF7600", "#FFF2E6", "clock"),
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
    width = max(400, min(1616, screen_width - 32))
    height = max(300, min(928, screen_height - 104))
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


@lru_cache(maxsize=256)
def _tinted_icon(name, rgb, size):
    path = Path(__file__).with_name("assets") / "icons" / f"{name}.png"
    with Image.open(path) as source:
        tinted = Image.new("RGBA", source.size, rgb)
        tinted.putalpha(source.getchannel("A"))
        return tinted.resize((size, size), Image.Resampling.LANCZOS)


class Button(ctk.CTkButton):
    """Button skin; command, state and geometry remain owned by the caller."""
    def __init__(self, master, *, role="secondary", icon_name=None,
                 accessible_name=None, **kwargs):
        self.skin_role = role
        self.icon_name = icon_name
        self.accessible_name = accessible_name or kwargs.get("text", "")
        self._skin_ready = False
        super().__init__(master, **kwargs)
        self._font.configure(weight="bold" if role in {"primary", "batch-stop"} else "normal")
        self._skin_ready = True
        self._skin()
        self._canvas.configure(takefocus=1)
        self._canvas.bind("<Return>", lambda _: self.invoke(), add="+")
        self._canvas.bind("<space>", lambda _: self.invoke(), add="+")
        self._canvas.bind("<FocusIn>", lambda _: self._paint_glass(), add="+")
        self._canvas.bind("<FocusOut>", lambda _: self._paint_glass(), add="+")
        if role == "primary":
            self.bind("<ButtonPress-1>", self._press, add="+")
            self.bind("<ButtonRelease-1>", lambda _: self._skin(), add="+")
        if accessible_name:
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
            self._paint_glass()

    def _skin(self):
        disabled = self.cget("state") == "disabled"
        key = (disabled, self.skin_role, self.icon_name)
        if getattr(self, "_skin_key", None) == key:
            return
        self._skin_key = key
        if disabled:
            face, hover, text, border = DISABLED_BG, DISABLED_BG, DISABLED_TEXT, BORDER
        elif self.skin_role == "primary":
            face, hover, text, border = CONTINUE_BG, CONTINUE_HOVER, WHITE, CONTINUE_BG
        elif self.skin_role == "batch-stop":
            face, hover, text, border = RED, STOP_HOVER, WHITE, STOP_BORDER
        elif self.skin_role == "clipboard":
            face, hover, text, border = "#007C91", "#006678", WHITE, "#99E6E9"
        elif self.skin_role in {"stop", "danger"}:
            face, hover, text, border = STOP_BG, STOP_HOVER, RED, STOP_BORDER
        elif self.skin_role == "settings":
            face, hover, text, border = HEADER_CONTROL, SECONDARY_HOVER, SETTINGS_ICON, HEADER_BORDER
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

    def _draw(self, no_color_updates=False):
        super()._draw(no_color_updates)
        if hasattr(self, "skin_role"):
            self._paint_glass()

    def _create_grid(self):
        super()._create_grid()
        # Render text on the same Canvas as the gradient to avoid opaque label boxes.
        for label in (getattr(self, "_text_label", None), getattr(self, "_image_label", None)):
            if label is not None:
                label.grid_remove()

    def _paint_glass(self):
        import tkinter.font as tkfont
        scale = self._get_widget_scaling()
        w, h = max(8, round(self._current_width * scale)), max(8, round(self._current_height * scale))
        disabled = self._state == "disabled"
        hover = getattr(self, "_glass_hover", False)
        text = self._textvariable.get() if self._textvariable is not None else self._text
        focus = self._canvas.focus_get() is self._canvas
        backing_id = id(getattr(self.master, "_art_pil", None))
        key = (w, h, self.skin_role, self.icon_name, disabled, hover, text, focus,
               str(self._font), str(self._text_color),
               str(self._text_color_disabled), backing_id)
        if getattr(self, "_glass_key", None) == key:
            return
        self._glass_key = key
        image = button_face(w, h, self.skin_role, disabled, hover)
        if hasattr(self.master, "_art_pil"):
            x,y=self.winfo_x(),self.winfo_y()
            backing=self.master._art_pil.crop((x,y,x+w,y+h))
            backing.alpha_composite(image)
            image=backing
        self._glass_photo = ImageTk.PhotoImage(image, master=self)
        self._canvas.itemconfigure("inner_parts", state="hidden")
        self._canvas.itemconfigure("border_parts", state="hidden")
        self._canvas.delete("glass")
        self._canvas.create_image(0, 0, image=self._glass_photo, anchor="nw", tags="glass")
        text_color = self._text_color_disabled if disabled else self._text_color
        text_color = self._apply_appearance_mode(text_color)
        font = self._apply_font_scaling(self._font)
        size = round((21 if self.skin_role in {"primary", "batch-stop"} else 18) * scale)
        gap = round(8 * scale) if text and self.icon_name else 0
        text_width = tkfont.Font(font=font).measure(text or "")
        left = (w - text_width - (size + gap if self.icon_name else 0)) / 2
        if self.icon_name:
            rgb = tuple(value // 257 for value in self.winfo_rgb(text_color))
            tinted = _tinted_icon(self.icon_name, rgb, size)
            self._glass_icon = ImageTk.PhotoImage(tinted, master=self)
            self._canvas.create_image(left, (h-4)/2, image=self._glass_icon, anchor="w", tags="glass")
        self._canvas.create_text(left + (size + gap if self.icon_name else 0), (h-4)/2,
                                 text=text, font=font, fill=text_color, anchor="w", tags="glass")
        for label in (self._text_label, self._image_label):
            if label is not None:
                label.grid_remove()
        self._canvas.tag_raise("glass")
        if focus:
            self._canvas.create_rectangle(5, 5, w-6, h-9, outline=BLUE, width=2, tags="glass")

    def _on_enter(self, event=None):
        super()._on_enter(event)
        self._glass_hover = True
        self._paint_glass()

    def _on_leave(self, event=None):
        super()._on_leave(event)
        self._glass_hover = False
        self._paint_glass()


class ArtFrame(ctk.CTkFrame):
    """A raster-painted frame; its children and callbacks remain native widgets."""
    def __init__(self, master, *, art_role="panel", **kwargs):
        self.art_role = art_role
        super().__init__(master, **kwargs)

    def configure(self, require_redraw=False, **kwargs):
        if "bg" in kwargs:
            kwargs["fg_color"] = kwargs.pop("bg")
        super().configure(require_redraw=require_redraw, **kwargs)

    def cget(self, key):
        return super().cget("fg_color" if key == "bg" else key)

    def _draw(self, no_color_updates=False):
        super()._draw(no_color_updates)
        if not hasattr(self, "art_role"):
            return
        scale = self._get_widget_scaling()
        w, h = max(8, round(self._current_width*scale)), max(8, round(self._current_height*scale))
        key = (w, h, self.art_role, str(self._fg_color))
        if getattr(self, "_art_key", None) == key:
            return
        self._art_key = key
        art = (banner(w, h, self.art_role == "footer") if self.art_role in {"header", "footer"}
               else rounded_surface(w, h, self.art_role, self._fg_color == PALE,
                                    self._apply_appearance_mode(self._fg_color)))
        self._art_pil=art
        self._art_photo = ImageTk.PhotoImage(art, master=self)
        self._canvas.delete("glass-surface")
        self._canvas.create_image(0, 0, image=self._art_photo, anchor="nw", tags="glass-surface")


@lru_cache(maxsize=12)
def artwork(name, size):
    art = brand_art() if name == "brand" else phone_art(int(name.rsplit("-", 1)[-1]))
    return ctk.CTkImage(light_image=art, dark_image=art, size=size)


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
        if "text_color" in kwargs and kwargs["text_color"] != RED:
            kwargs["text_color"] = WHITE
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

    def _dispose(self, event):
        if event.widget is self:
            ctk.ScalingTracker.remove_widget(self._scale, self)


class StatusCell(tk.Frame):
    """Two visual levels, retaining the full status for tooltip and selection."""
    def __init__(self, master, **kwargs):
        background = kwargs.get("bg", SURFACE)
        super().__init__(master, bg=background, borderwidth=0)
        self.full_text = ""
        self.primary = TableText(self, text="", bg=background, fg=BODY,
                                 font=ui_font(15, "semibold"), wraplength=150, anchor="w",
                                 justify="left", padx=6, pady=2)
        self.description = TableText(self, text="", bg=background, fg=MUTED,
                                     font=ui_font(14), wraplength=150, anchor="w",
                                     justify="left", padx=6, pady=1)
        self.primary.pack(fill="x")
        self.description.pack(fill="x")
        self._tooltip = Tooltip(self, lambda: self.full_text)

    def configure(self, cnf=None, **kwargs):
        if not hasattr(self, "primary"):
            return super().configure(cnf, **kwargs)
        text = kwargs.pop("text", None)
        title = kwargs.pop("title", None)
        color = kwargs.pop("fg", None)
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
                self.description.pack(fill="x")
            else:
                self.description.pack_forget()
        if title is not None:
            self.primary.configure(text=title)
        if color is not None:
            self.primary.configure(fg=color)
        if "bg" in kwargs:
            self.primary.configure(bg=kwargs["bg"])
            self.description.configure(bg=kwargs["bg"])
        return super().configure(cnf, **kwargs)

    def cget(self, key):
        return self.full_text if key == "text" else super().cget(key)

    def set_wrap(self, width):
        self.primary.set_wrap(width)
        self.description.set_wrap(width)

    def bind(self, sequence=None, func=None, add=None):
        result = super().bind(sequence, func, add)
        if hasattr(self, "primary"):
            for child in (self.primary, self.description):
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
