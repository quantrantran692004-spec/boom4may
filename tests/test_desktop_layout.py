"""Check the compact desktop layout on a scaled Windows display."""
import sys
import unittest
from unittest.mock import patch

import customtkinter as ctk

from amazon_android import desktop


@unittest.skipUnless(sys.platform == "win32", "Tk window layout requires Windows")
class DesktopLayoutTests(unittest.TestCase):
    def test_table_has_all_twelve_slots_and_locked_batch_starts_at_table(self):
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
            window.draft.locked = True
            window._refresh_devices()
            self.assertFalse(window.bulk_card.winfo_manager())
            self.assertFalse(window.proxy_line.winfo_manager())
            self.assertTrue(window.preview_table.winfo_manager())
            window.draft.locked = False
            window._refresh_devices()
            self.assertTrue(window.bulk_card.winfo_manager())
            self.assertTrue(window.proxy_line.winfo_manager())
        finally:
            window.root.withdraw()
            window.root.destroy()


if __name__ == "__main__":
    unittest.main()
