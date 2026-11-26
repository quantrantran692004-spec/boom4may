import sys
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from amazon_android import phone_window_layout as layout


class PhoneWindowLayoutTests(unittest.TestCase):
    def setUp(self):
        layout._arranged.clear()

    def test_tiles_fit_work_area_without_overlap(self):
        for count in (1, 3, 4, 6, 12):
            with self.subTest(count=count):
                rects = layout._tiles((0, 0, 1536, 816), count, (382, 767))
                self.assertEqual(len(rects), count)
                for x, y, width, height in rects:
                    self.assertGreater(width, 0)
                    self.assertGreater(height, 0)
                    self.assertGreaterEqual(x, 0)
                    self.assertGreaterEqual(y, 0)
                    self.assertLessEqual(x + width, 1536)
                    self.assertLessEqual(y + height, 816)
                for first, a in enumerate(rects):
                    for b in rects[first + 1:]:
                        self.assertTrue(a[0] + a[2] <= b[0] or b[0] + b[2] <= a[0]
                                        or a[1] + a[3] <= b[1] or b[1] + b[3] <= a[1])

    def test_existing_window_sizes_are_kept_when_one_row_fits(self):
        self.assertEqual(layout._row_if_fits(
            (0, 0, 1536, 816), [(382, 767), (988, 754)]),
            [(8, 8, 382, 767), (398, 8, 988, 754)])
        self.assertIsNone(layout._row_if_fits(
            (0, 0, 1536, 816), [(382, 767)] * 4 + [(988, 754)]))

    def test_new_viewer_arranges_matching_windows_once_without_focus(self):
        titles = {3: 'q3 - ACN3', 4: 'q4 - ACN4', 5: 'q5 - ACN5',
                  6: 'q6 - ACN6', 9: 'Swarmote Profiles', 10: 'q9 - ACN9',
                  11: 'q11 - ACN11', 12: 'q12 - ACN12'}
        rects = {handle: (0, 0, 382, 767) for handle in titles}
        rects[6] = (0, 0, 988, 754)  # An expanded Apps panel must not dominate sizing.
        moved = []

        def enumerate_windows(callback, extra):
            for handle in titles:
                callback(handle, extra)

        def set_position(handle, _after, x, y, width, height, flags):
            moved.append((handle, x, y, width, height, flags))
            rects[handle] = (x, y, x + width, y + height)

        gui = SimpleNamespace(EnumWindows=enumerate_windows,
                              GetWindowText=titles.__getitem__,
                              IsWindowVisible=lambda _handle: True,
                              IsIconic=lambda handle: handle == 12,
                              GetWindowRect=rects.__getitem__,
                              SetWindowPos=set_position)
        api = SimpleNamespace(MonitorFromWindow=lambda handle, _flag: 2 if handle == 11 else 1,
                              GetMonitorInfo=lambda _monitor: {'Work': (0, 0, 1536, 816)})
        con = SimpleNamespace(MONITOR_DEFAULTTONEAREST=1, SWP_NOACTIVATE=1,
                              SWP_NOZORDER=2, SWP_NOOWNERZORDER=4,
                              SWP_ASYNCWINDOWPOS=8)
        process = SimpleNamespace(GetWindowThreadProcessId=lambda handle: (0, handle))
        modules = {'win32api': api, 'win32con': con, 'win32gui': gui,
                   'win32process': process}
        with patch.dict(sys.modules, modules), \
             patch.object(layout.psutil, 'Process',
                          side_effect=lambda pid: SimpleNamespace(
                              exe=lambda: 'Other.exe' if pid == 10 else 'Swarmote.exe')):
            layout.arrange_on_open(5, 'swarmote.exe')
            self.assertEqual([item[0] for item in moved], [3, 4, 5, 6])
            self.assertTrue(all(item[-1] == 15 for item in moved))
            self.assertTrue(all(item[2] == 8 for item in moved))
            self.assertTrue(all(item[4] <= 800 for item in moved))
            layout.arrange_on_open(5, 'swarmote.exe')
            self.assertEqual(len(moved), 4)
            titles[7] = 'q7 - ACN7'
            rects[7] = (0, 0, 382, 767)
            layout.arrange_on_open(7, 'swarmote.exe')
            self.assertEqual([item[0] for item in moved[4:]], [3, 4, 5, 6, 7])


if __name__ == '__main__':
    unittest.main()
