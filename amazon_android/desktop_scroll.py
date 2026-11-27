"""Interruptible pixel scrolling for the desktop panels, without worker threads."""
import math
import sys
import time
import tkinter as tk

import customtkinter as ctk


def animations_enabled():
    """Honor Windows' client-area animation preference without changing it."""
    if sys.platform == "win32":
        import ctypes
        enabled = ctypes.c_int(1)
        if ctypes.windll.user32.SystemParametersInfoW(0x1042, 0, ctypes.byref(enabled), 0):
            return bool(enabled.value)
    return True


class SmoothScrollableFrame(ctk.CTkScrollableFrame):
    FRAME_MS = 16
    RESPONSE_SECONDS = .045
    WHEEL_PIXELS = 48

    def __init__(self, master, **kwargs):
        self._global_bindings = []
        self._scroll_after = None
        self._scroll_target = None
        self._wheel_fraction = 0
        self._scroll_last = 0
        self._animate_scroll = animations_enabled()
        super().__init__(master, **kwargs)
        self._scrollbar.configure(command=self._direct_scroll)
        self.bind_all("<ButtonPress-1>", self._stop_on_click, add="+")

    def bind_all(self, sequence=None, func=None, add=None):
        identifier = super().bind_all(sequence, func, add)
        if identifier:
            self._global_bindings.append((sequence, identifier))
        return identifier

    def _extent(self):
        canvas = self._parent_canvas
        bounds = canvas.bbox("all")
        total = max(1, bounds[3] - bounds[1]) if bounds else 1
        first, last = canvas.yview()
        return total, first * total, max(0, total * (1 - (last - first)))

    def _mouse_wheel_all(self, event):
        if not self.check_if_master_is_canvas(event.widget):
            return
        if self._shift_pressed or self._orientation != "vertical":
            self._cancel_scroll()
            return super()._mouse_wheel_all(event)
        # Preserve fractional touchpad deltas instead of rounding them to zero.
        delta = float(getattr(event, "delta", 0))
        if not delta:
            return
        if sys.platform == "win32":
            delta /= 120
        elif sys.platform != "darwin":
            delta = math.copysign(1, delta)
        self._queue_scroll(-delta * self.WHEEL_PIXELS * self._get_widget_scaling())

    def _queue_scroll(self, pixels):
        total, current, maximum = self._extent()
        if maximum <= 0:
            self._cancel_scroll()
            return
        target = self._scroll_target
        # A reversal starts at the visible position, without draining old input.
        if target is None:
            target = current + self._wheel_fraction
        elif (target - current) * pixels < 0:
            target = current
        self._wheel_fraction = 0
        ahead = min(self._parent_canvas.winfo_height() * .8,
                    320 * self._get_widget_scaling())
        target = max(current - ahead, min(current + ahead, target + pixels))
        self._scroll_target = max(0, min(maximum, target))
        if not self._animate_scroll:
            self._parent_canvas.yview_moveto(self._scroll_target / total)
            remainder = self._scroll_target - self._extent()[1]
            self._cancel_scroll()
            self._wheel_fraction = remainder
        elif self._scroll_after is None:
            self._scroll_last = time.monotonic() - self.FRAME_MS / 1000
            self._scroll_step()

    def _scroll_step(self):
        self._scroll_after = None
        if self._scroll_target is None or not self.winfo_exists():
            return
        total, current, maximum = self._extent()
        target = max(0, min(maximum, self._scroll_target))
        now = time.monotonic()
        elapsed = min(.05, max(.001, now - self._scroll_last))
        self._scroll_last = now
        remaining = target - current
        if abs(remaining) <= 2:
            self._parent_canvas.yview_moveto(target / total)
            self._wheel_fraction = target - self._extent()[1]
            self._scroll_target = None
            return
        position = current + remaining * (1 - math.exp(-elapsed / self.RESPONSE_SECONDS))
        self._parent_canvas.yview_moveto(position / total)
        self._scroll_after = self.after(self.FRAME_MS, self._scroll_step)

    def _cancel_scroll(self):
        if self._scroll_after is not None:
            self.after_cancel(self._scroll_after)
        self._scroll_after = None
        self._scroll_target = None
        self._wheel_fraction = 0

    def _stop_on_click(self, event):
        if self.check_if_master_is_canvas(event.widget):
            self._cancel_scroll()

    def _direct_scroll(self, *args):
        self._cancel_scroll()
        self._parent_canvas.yview(*args)

    def destroy(self):
        self._cancel_scroll()
        root = self._root()
        for sequence, identifier in self._global_bindings:
            try:
                # Python 3.11 has no selective unbind_all. Remove only this
                # frame's Tcl binding, preserving the other scrolling panels.
                script = str(self.tk.call("bind", "all", sequence))
                kept = [line for line in script.splitlines()
                        if f"[{identifier} " not in line]
                self.tk.call("bind", "all", sequence, "\n".join(kept))
                root.deletecommand(identifier)
            except tk.TclError:
                pass  # The root may already be tearing down its bindings.
        self._global_bindings.clear()
        super().destroy()
