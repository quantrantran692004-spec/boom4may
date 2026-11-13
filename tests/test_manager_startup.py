import threading
import unittest
from unittest.mock import Mock, patch
from amazon_android import swarmote_desktop as sw


class ManagerStartupTests(unittest.TestCase):
    def test_launches_once_then_waits_for_profiles(self):
        exe = Mock(); exe.is_file.return_value = True
        window = object()
        with patch.object(sw, '_main_window', side_effect=[sw.ProfileManagerWindowError('missing'), window]), \
             patch.object(sw, '_swarmote_exe', return_value=exe), \
             patch.object(sw.psutil, 'process_iter', return_value=[]), \
             patch.object(sw, '_open_profiles') as profiles, \
             patch('subprocess.Popen') as launch, patch.object(sw.time, 'sleep'):
            sw.ensure_manager_ready()
        launch.assert_called_once()
        profiles.assert_called_once_with(window)

    def test_existing_manager_is_reused_without_launch(self):
        with patch.object(sw, '_main_window', return_value=object()), \
             patch.object(sw, '_open_profiles'), patch('subprocess.Popen') as launch:
            sw.ensure_manager_ready()
        launch.assert_not_called()

    def test_stopped_batch_does_not_launch_app(self):
        stop = threading.Event(); stop.set()
        with patch('subprocess.Popen') as launch:
            with self.assertRaisesRegex(sw.ToolError, 'Đã dừng'):
                sw.ensure_manager_ready(stop=stop)
        launch.assert_not_called()
