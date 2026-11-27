"""Exercise real Tk wheel routing, fractional input and interruption."""
import sys
import tkinter as tk
import unittest
from unittest.mock import patch

import customtkinter as ctk

from amazon_android.desktop_scroll import SmoothScrollableFrame


@unittest.skipUnless(sys.platform == "win32", "Windows wheel deltas")
class DesktopScrollTests(unittest.TestCase):
    def setUp(self):
        self.root = ctk.CTk()
        self.root.withdraw()
        self.root.geometry("640x400+5000+5000")
        self.errors = []
        self.root.report_callback_exception = lambda *error: self.errors.append(error)
        self.panels = []
        self.labels = []
        with patch("amazon_android.desktop_scroll.animations_enabled", return_value=True):
            for _ in range(2):
                panel = SmoothScrollableFrame(self.root, width=280, height=360)
                panel.pack(side="left", fill="both", expand=True)
                for i in range(60):
                    label = tk.Label(panel, text=f"Row {i}", pady=8)
                    label.pack(fill="x")
                self.panels.append(panel)
                self.labels.append(label)
        self.root.deiconify()
        self.root.update()

    def pump(self, milliseconds=400):
        self.root.after(milliseconds, self.root.quit)
        self.root.mainloop()

    def tearDown(self):
        self.root.withdraw()
        for callback in self.root.tk.call("after", "info"):
            self.root.after_cancel(callback)
        self.root.destroy()
        self.assertFalse(self.errors)

    def test_wheel_over_child_moves_only_its_panel_and_settles_without_idle_timer(self):
        first, second = self.panels
        second_before = second._parent_canvas.yview()
        self.labels[0].event_generate("<MouseWheel>", delta=-120)
        _, start, _ = first._extent()
        distance = first.WHEEL_PIXELS * first._get_widget_scaling()
        self.assertGreater(start, 0)
        self.assertLess(start, distance)
        self.pump()
        self.assertAlmostEqual(first._extent()[1], distance, delta=2)
        self.assertEqual(second._parent_canvas.yview(), second_before)
        self.assertIsNone(first._scroll_after)
        self.assertIsNone(first._scroll_target)

    def test_small_touchpad_deltas_accumulate_and_reversal_retargets_visible_position(self):
        panel = self.panels[0]
        for _ in range(120):
            self.labels[0].event_generate("<MouseWheel>", delta=-1)
        self.pump()
        self.assertAlmostEqual(panel._extent()[1],
                               panel.WHEEL_PIXELS * panel._get_widget_scaling(), delta=2)
        panel._queue_scroll(100)
        current = panel._extent()[1]
        panel._queue_scroll(-30)
        self.assertLess(panel._scroll_target, current)
        self.pump()
        self.assertLess(panel._extent()[1], current)

    def test_drag_interrupts_and_edges_or_reduced_motion_leave_no_scheduled_work(self):
        panel = self.panels[0]
        panel._queue_scroll(200)
        self.assertIsNotNone(panel._scroll_after)
        panel._direct_scroll("moveto", .4)
        position = panel._parent_canvas.yview()
        self.assertIsNone(panel._scroll_after)
        self.pump(100)
        self.assertEqual(panel._parent_canvas.yview(), position)
        panel._direct_scroll("moveto", 1)
        panel._queue_scroll(200)
        self.pump(100)
        self.assertAlmostEqual(panel._parent_canvas.yview()[1], 1)
        self.assertIsNone(panel._scroll_after)
        panel._animate_scroll = False
        current = panel._extent()[1]
        panel._queue_scroll(-30)
        self.assertAlmostEqual(panel._extent()[1], current - 30, delta=2)
        self.assertIsNone(panel._scroll_after)

    def test_destroying_one_panel_removes_its_callbacks_and_preserves_other_panel(self):
        first, second = self.panels
        first._queue_scroll(200)
        bindings = list(first._global_bindings)
        first._parent_frame.destroy()
        self.pump(100)
        for sequence, identifier in bindings:
            self.assertNotIn(identifier, str(self.root.bind_all(sequence)))
        self.labels[1].event_generate("<MouseWheel>", delta=-120)
        self.pump()
        self.assertGreater(second._extent()[1], 0)
        self.assertIsNone(second._scroll_after)


if __name__ == "__main__":
    unittest.main()
