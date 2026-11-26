import threading
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

from amazon_android.core import ToolError
from amazon_android.swarmote_desktop import _phone_window, _wait_for, open_adb_shell, show_apps


class SwarmoteWaitTests(unittest.TestCase):
    def test_phone_lookup_does_not_visit_unrelated_uia_providers(self):
        desktop = Mock()
        desktop.windows.side_effect = AssertionError('Must not enumerate desktop UIA')
        expected = object()
        desktop.window.return_value.wrapper_object.return_value = expected
        titles = {1: 'Other app', 2: 'q1 - ACN1', 3: 'q2 - ACN2'}
        def enumerate_windows(callback, extra):
            for handle in titles:
                callback(handle, extra)
        with patch('pywinauto.Desktop', return_value=desktop), \
             patch('win32gui.EnumWindows', side_effect=enumerate_windows), \
             patch('win32gui.GetWindowText', side_effect=titles.__getitem__), \
             patch('win32process.GetWindowThreadProcessId', return_value=(1, 123)), \
             patch('amazon_android.swarmote_desktop._swarmote_exe', return_value=Path('Swarmote.exe')), \
             patch('amazon_android.swarmote_desktop.psutil.Process', return_value=SimpleNamespace(exe=lambda: 'Swarmote.exe')), \
             patch('amazon_android.phone_window_layout.arrange_on_open') as arrange:
            self.assertIs(_phone_window('q2', 'ACN2'), expected)
        desktop.window.assert_called_once_with(handle=3)
        arrange.assert_called_once_with(3, 'swarmote.exe')

    def test_phone_lookup_continues_if_window_layout_fails(self):
        desktop = Mock()
        expected = object()
        desktop.window.return_value.wrapper_object.return_value = expected
        with patch('pywinauto.Desktop', return_value=desktop), \
             patch('win32gui.EnumWindows', side_effect=lambda callback, extra: callback(3, extra)), \
             patch('win32gui.GetWindowText', return_value='q2 - ACN2'), \
             patch('win32process.GetWindowThreadProcessId', return_value=(1, 123)), \
             patch('amazon_android.swarmote_desktop._swarmote_exe', return_value=Path('Swarmote.exe')), \
             patch('amazon_android.swarmote_desktop.psutil.Process', return_value=SimpleNamespace(exe=lambda: 'Swarmote.exe')), \
             patch('amazon_android.phone_window_layout.arrange_on_open',
                   side_effect=OSError('Windows refused to move the viewer')):
            self.assertIs(_phone_window('q2', 'ACN2'), expected)

    def test_stop_before_apps_or_terminal_lookup_does_not_touch_ui(self):
        stop = threading.Event(); stop.set()
        with patch('amazon_android.swarmote_desktop._phone_window') as lookup:
            for operation in [show_apps, open_adb_shell]:
                with self.subTest(operation=operation.__name__):
                    with self.assertRaisesRegex(ToolError, 'Đã dừng'):
                        operation('q1', 'ACN1', stop=stop)
        lookup.assert_not_called()

    def test_stop_after_apps_invoke_is_not_swallowed_by_retry(self):
        stop = threading.Event()
        group = SimpleNamespace(invoke=stop.set)
        apps = SimpleNamespace(element_info=SimpleNamespace(name='Apps', control_type='Text'),
                               is_visible=lambda: True, parent=lambda: group)
        messages = []
        with patch('amazon_android.swarmote_desktop._phone_window', return_value=object()), \
             patch('amazon_android.swarmote_desktop._descendants', return_value=[apps]):
            with self.assertRaisesRegex(ToolError, 'Đã dừng'):
                show_apps('q1', 'ACN1', stop=stop, progress=messages.append)
        self.assertTrue(any('Apps' in m for m in messages))

    def test_wait_ignores_hidden_store_and_reports_elapsed_progress(self):
        elapsed = [0.0]
        hidden = SimpleNamespace(element_info=SimpleNamespace(name='App Store', control_type='TabItem'),
                                 is_visible=lambda: False)
        messages = []
        with patch('amazon_android.swarmote_desktop.time.monotonic', side_effect=lambda: elapsed[0]), \
             patch('amazon_android.swarmote_desktop.time.sleep', side_effect=lambda s: elapsed.__setitem__(0, elapsed[0]+s)), \
             patch('amazon_android.swarmote_desktop._descendants', return_value=[hidden]):
            with self.assertRaisesRegex(ToolError, 'App Store'):
                _wait_for(object(), 'App Store', 'TabItem', seconds=4, progress=messages.append, visible=True)
        self.assertGreaterEqual(len(messages), 2)


if __name__ == '__main__':
    unittest.main()
