"""Check the compact desktop layout on a scaled Windows display."""
import sys
import unittest
from unittest.mock import patch

import customtkinter as ctk

from amazon_android import desktop
from amazon_android.desktop_theme import StatusCell, state_style, status_title, startup_geometry
from amazon_android.desktop_theme import ROW_SELECTED_BORDER, PROCESSING, PROGRESS_TEXT


@unittest.skipUnless(sys.platform == "win32", "Tk window layout requires Windows")
class DesktopLayoutTests(unittest.TestCase):
    def test_settings_dialog_saves_create_b13_switch(self):
        class HiddenRoot(ctk.CTk):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.withdraw()

        class HiddenDialog(ctk.CTkToplevel):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.withdraw()

        def descendants(widget):
            for child in widget.winfo_children():
                yield child
                yield from descendants(child)

        with patch.object(desktop.ctk, "CTk", HiddenRoot), \
             patch.object(desktop.ctk, "CTkToplevel", HiddenDialog), \
             patch.object(desktop, "save_settings") as saved:
            window = desktop.Window()
            try:
                window._open_settings()
                controls = list(descendants(window.settings_window))
                switches = [item for item in controls if isinstance(item, ctk.CTkSwitch)
                            and item.cget("text") == "Tạo tài khoản · dừng trước b13"]
                self.assertEqual(len(switches), 1)
                switches[0].toggle()
                buttons = [item for item in controls if isinstance(item, ctk.CTkButton)
                           and item.cget("text") == "Lưu Settings"]
                self.assertEqual(len(buttons), 1)
                buttons[0].invoke()
                self.assertTrue(window.settings.pause_before_b13)
                saved.assert_called_once_with(window.settings)
            finally:
                window.root.withdraw()
                for callback in window.root.tk.call("after", "info"):
                    window.root.after_cancel(callback)
                window.root.destroy()

    def test_startup_size_matches_reference_and_stays_inside_smaller_screen(self):
        for scale in (1, 1.25, 1.5):
            width, height, x, y = startup_geometry(1920, 1080, scale)
            self.assertAlmostEqual(width * scale, 1840, delta=1)
            self.assertAlmostEqual(height * scale, 960, delta=1)
            self.assertGreaterEqual(x, 0)
            self.assertGreaterEqual(y, 0)
            width, height, x, y = startup_geometry(1366, 768, scale)
            self.assertLessEqual(width * scale + x, 1366)
            self.assertLessEqual(height * scale + y + 60, 768)

    def test_long_status_keeps_full_message_and_scales_without_horizontal_overflow(self):
        class HiddenRoot(ctk.CTk):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.withdraw()

        with patch.object(desktop.ctk, "CTk", HiddenRoot):
            window = desktop.Window()
        root = window.root
        base_scale = root._get_window_scaling()
        try:
            window.count.set("12")
            message = "b22 mở tab hình người: màn hình chưa xác nhận; kiểm tra kết nối rồi bấm Tiếp tục."
            for i in range(12):
                window.values[i]["full_name"].set(f"Example User {i + 1}")
                window.values[i]["host"].set("proxy.example")
                window.values[i]["port"].set("3010")
                window.status[i] = (message, "post_paused")
            root.deiconify()
            for scale in (1, 1.25, 1.5):
                ctk.set_widget_scaling(scale / base_scale)
                ctk.set_window_scaling(scale / base_scale)
                root.minsize(900, 450)
                root.geometry(f"{int(1460 / scale)}x{int(751 / scale)}+5000+5000")
                window.status[11] = (message, "post_paused")
                window._select(11)
                root.update()
                cell = window.table_rows[11]["status"]
                self.assertNotIn("proxy", window.table_rows[11])
                self.assertNotIn("account", window.table_rows[11])
                self.assertTrue(window.proxy_line.winfo_manager())
                self.assertTrue(window.detail_entries["host"].winfo_manager())
                self.assertIsInstance(cell, StatusCell)
                self.assertIn(message, cell.cget("text"))
                self.assertEqual(status_title("post_paused"), cell.primary.cget("text"))
                self.assertEqual(message, window.detail_description.cget("text"))
                self.assertEqual(state_style("post_paused")[0], cell.primary.cget("fg"))
                self.assertLessEqual(window.preview_table.winfo_reqwidth(),
                                     window.main._parent_canvas.winfo_width())
                self.assertLessEqual(window.detail_panel.winfo_children()[0].winfo_reqwidth(),
                                     window.detail_panel._parent_canvas.winfo_width())
                self.assertEqual(window.table_bands[11].cget("fg_color"), cell.cget("bg"))
                band = window.table_bands[11]
                previous = window.table_bands[10]
                self.assertGreater(band.winfo_y(), previous.winfo_y() + previous.winfo_height())
                self.assertEqual(ROW_SELECTED_BORDER, band.cget("border_color"))
                continue_button, stop_button = window.row_buttons[11], window.row_stop_buttons[11]
                self.assertEqual(continue_button.winfo_y(), stop_button.winfo_y())
                self.assertGreater(stop_button.winfo_x(),
                                   continue_button.winfo_x() + continue_button.winfo_width())
                window.status[11] = ("b11 nhập OTP: đang đọc mã riêng của máy", "post_running")
                window._refresh_devices()
                self.assertEqual(PROCESSING, cell.primary.cget("fg"))
                self.assertEqual(PROGRESS_TEXT, cell.description.cget("fg"))
                self.assertEqual(window.status[11][0], window.detail_description.cget("text"))
        finally:
            root.withdraw()
            for callback in root.tk.call("after", "info"):
                root.after_cancel(callback)
            root.destroy()
            ctk.set_widget_scaling(1)
            ctk.set_window_scaling(1)

    def test_table_has_all_twelve_slots_and_locked_controls_remain_visible(self):
        class HiddenRoot(ctk.CTk):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.withdraw()

        with patch.object(desktop.ctk, "CTk", HiddenRoot):
            window = desktop.Window()
        try:
            root = window.root
            scale = root._get_window_scaling()
            width = min(1380, int(root.winfo_screenwidth() / scale - 60))
            height = min(800, int(root.winfo_screenheight() / scale - 90))
            root.geometry(f"{min(1100, width - 40)}x{min(600, height - 30)}+5000+5000")
            root.deiconify()
            root.update()

            self.assertEqual(12, sum(bool(row["machine"].winfo_manager())
                                     for row in window.table_rows))
            window.count.set("12")
            window._refresh_devices()
            window._select(11)
            self.assertEqual(11, window.selected)
            self.assertEqual("Máy 12", window.detail_title.cget("text"))
            card = window.detail_panel.winfo_children()[0]
            self.assertLessEqual(card.winfo_reqwidth(),
                                 window.detail_panel._parent_canvas.winfo_width())
            self.assertLessEqual(window.preview_table.winfo_reqwidth(),
                                 window.main._parent_canvas.winfo_width())
            window.draft.locked = True
            window._refresh_devices()
            self.assertTrue(window.bulk_card.winfo_manager())
            self.assertTrue(window.proxy_line.winfo_manager())
            self.assertTrue(window.single_account_line.winfo_manager())
            self.assertLess(window.proxy_line.winfo_rooty(),
                            window.detail_entries["full_name"].winfo_rooty())
            self.assertLess(window.single_account_line.winfo_rooty(),
                            window.detail_entries["full_name"].winfo_rooty())
            self.assertEqual("disabled", window.apply_single_account_button.cget("state"))
            self.assertTrue(window.preview_table.winfo_manager())
            window.draft.locked = False
            window._refresh_devices()
            self.assertTrue(window.bulk_card.winfo_manager())
            self.assertTrue(window.proxy_line.winfo_manager())
        finally:
            window.root.withdraw()
            for callback in window.root.tk.call("after", "info"):
                window.root.after_cancel(callback)
            window.root.destroy()


if __name__ == "__main__":
    unittest.main()
