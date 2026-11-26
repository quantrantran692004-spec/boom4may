from worker_helpers import on_worker
import unittest
import queue
import threading
from unittest.mock import Mock, patch

from amazon_android.desktop import Window, _automatic_resume_slots
from amazon_android.runner import AccountData, RunJob
from amazon_android.settings import AppSettings


class DesktopResumeTests(unittest.TestCase):
    def test_403_browser_recovery_uses_only_paused_machine_url(self):
        window = Window.__new__(Window)
        window.root = None
        accounts = [AccountData("12025550123", "Example User", "Example456!",
                                f"https://apifc.net/smsrecord?token=q{i + 1}")
                    for i in range(2)]
        window.jobs = {i: RunJob(i, "batch", None, account=account)
                       for i, account in enumerate(accounts)}
        with patch("amazon_android.desktop.messagebox.askyesnocancel", return_value=True), \
             patch("amazon_android.desktop.webbrowser.open", return_value=True) as opened, \
             patch("amazon_android.desktop.simpledialog.askstring", return_value=
                   "yes|Amazon: 123456 is your sign-in code."):
            self.assertTrue(window._read_browser_otp(1))
        opened.assert_called_once_with(accounts[1].otp_url)
        self.assertEqual(window.jobs[1].account.browser_otp, "123456")
        self.assertEqual(window.jobs[0].account.browser_otp, "")

    def test_restarts_only_ready_work_not_old_errors_or_completed_machines(self):
        items = [
            {"slot": 0, "state": "ERROR", "stage": "APP_INSTALLED"},
            {"slot": 1, "state": "DONE", "stage": "MENU_OPEN"},
            {"slot": 2, "state": "READY", "stage": "PROFILE_CONFIRMED"},
            {"slot": 3, "state": "STOPPED", "stage": "APP_INSTALLED"},
        ]
        self.assertEqual(_automatic_resume_slots(items), [2])
        self.assertEqual(_automatic_resume_slots(items, start_group_size=2), [2])

    def test_launch_keeps_queue_open_and_manual_override(self):
        window = Window.__new__(Window)
        window.running = False
        window.attach_in_progress = False
        window._previous_work_busy = Mock(return_value=False)
        window.registry = Mock()
        window.settings = AppSettings(start_group_size=2)
        window.jobs = {index: RunJob(index, 'batch', None) for index in range(3)}
        window._edited_locked_rows = set()
        window.phone_stop_after_step = {}
        window.cancel = threading.Event()
        window.run_button = Mock()
        window.settings_button = Mock()
        window.stop_button = Mock()
        window.reset_button = Mock()
        window._refresh_devices = Mock()
        window.run_note = Mock()
        window.events = queue.Queue()
        window.phone_serials = {}
        window.proxy_postal_prefixes = {}
        window.menu_opened_at = {}
        window.manual_slots = set()
        with patch('amazon_android.desktop.threading.Thread') as worker:
            window._launch([0, 1, 2])
            automatic = worker.call_args.kwargs['args'][1]
            self.assertIsNone(automatic['automatic_start_slots'])
            self.assertFalse(automatic['manual_override'])
            window.running = False
            window._launch([2], manual_override=True)
            manual = worker.call_args.kwargs['args'][1]
            self.assertTrue(manual['manual_override'])

    def test_attach_existing_q1_only_after_running_menu_check(self):
        window = Window.__new__(Window)
        window.attach_events = queue.Queue()
        account = AccountData("12025550123", "Example User", "Example456!",
                              "https://apifc.net/smsrecord?token=q1")
        with patch("amazon_android.desktop.profile_status", return_value={
                "state": "Running", "device_id": "device-q1"}) as status, \
             patch("amazon_android.desktop.open_adb_shell", return_value={
                 "serial": "127.0.0.1:5001"}) as shell, \
             patch("amazon_android.desktop.verify_menu_open") as menu:
            on_worker(window._probe_existing_profile, 0, account)
        self.assertEqual(window.attach_events.get_nowait(),
                         ("ready", account, "127.0.0.1:5001"))
        status.assert_called_once_with("q1")
        shell.assert_called_once_with("q1", "device-q1")
        self.assertEqual(menu.call_args.args[0].serial, "127.0.0.1:5001")

    def test_attach_existing_q1_stops_if_offline(self):
        window = Window.__new__(Window)
        window.attach_events = queue.Queue()
        account = AccountData("12025550123", "Example User", "Example456!",
                              "https://apifc.net/smsrecord?token=q1")
        with patch("amazon_android.desktop.profile_status", return_value={
                "state": "Offline", "device_id": "device-q1"}), \
             patch("amazon_android.desktop.open_adb_shell") as shell, \
             patch("amazon_android.desktop.verify_menu_open") as menu:
            on_worker(window._probe_existing_profile, 0, account)
        state, _, reason = window.attach_events.get_nowait()
        self.assertEqual(state, "error")
        self.assertIn("Offline", reason)
        shell.assert_not_called()
        menu.assert_not_called()

    def test_attach_q2_uses_q2_profile_and_its_own_serial(self):
        window = Window.__new__(Window)
        window.attach_events = queue.Queue()
        account = AccountData("12025550124", "Second User", "Example456!",
                              "https://apifc.net/smsrecord?token=q2")
        with patch("amazon_android.desktop.profile_status", return_value={
                "state": "Running", "device_id": "device-q2"}) as status, \
             patch("amazon_android.desktop.open_adb_shell", return_value={
                 "serial": "127.0.0.1:5002"}) as shell, \
             patch("amazon_android.desktop.verify_menu_open") as menu:
            on_worker(window._probe_existing_profile, 1, account)
        self.assertEqual(window.attach_events.get_nowait(),
                         ("ready", account, "127.0.0.1:5002"))
        status.assert_called_once_with("q2")
        shell.assert_called_once_with("q2", "device-q2")
        self.assertEqual(menu.call_args.args[1], "q2")

    def test_q2_menu_without_serial_reports_why_it_cannot_start(self):
        window = Window.__new__(Window)
        window.post_menu_step_factories = {1: lambda *_: ()}
        window.post_menu_sessions = {}
        window.cancel = threading.Event()
        window.events = queue.Queue()
        window.jobs = {1: RunJob(1, "batch", None, account=AccountData(
            "12025550124", "Second User", "Example456!",
            "https://apifc.net/smsrecord?token=q2"))}
        window.phone_serials = {}
        window._start_post_menu(1)
        index, message, state, name = window.events.get_nowait()
        self.assertEqual((index, state, name), (1, "post_paused", "q2"))
        self.assertIn("chưa nối ADB", message)

    def test_q2_menu_without_amazon_row_reports_missing_data(self):
        window = Window.__new__(Window)
        window.post_menu_step_factories = {1: lambda *_: ()}
        window.post_menu_sessions = {}
        window.cancel = threading.Event()
        window.events = queue.Queue()
        window.jobs = {1: RunJob(1, "batch", None)}
        window.phone_serials = {1: "127.0.0.1:5002"}
        window._start_post_menu(1)
        _, message, state, _ = window.events.get_nowait()
        self.assertEqual(state, "menu_only")
        self.assertIn("chưa có hàng Amazon", message)


if __name__ == "__main__":
    unittest.main()
