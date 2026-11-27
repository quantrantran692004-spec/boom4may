import queue
import threading
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from amazon_android.desktop import POST_MENU_STEP_FACTORIES, Window
from amazon_android.post_menu import PostMenuSession
from amazon_android.reg_us_flow import build_reg_us_steps
from amazon_android.runner import AccountData, RunJob
from amazon_android.settings import AppSettings


class RegUsFlowTests(unittest.TestCase):
    def test_reg_us_stops_at_b1_without_phone_action(self):
        steps = build_reg_us_steps(None, None)
        self.assertEqual([step.name for step in steps], ["b1 Reg US"])
        session = PostMenuSession("batch", 0, "q1")
        events = []
        session.run(RunJob(0, "batch", None), steps,
                    lambda *event: events.append(event), threading.Event())
        self.assertEqual(session.state, "PAUSED")
        self.assertEqual(session.next_step, 0)
        self.assertIn("chưa có hướng dẫn b1", session.last_error)
        self.assertEqual(events[-1][2], "post_paused")

    def test_reg_us_uses_separate_factory_after_shared_preparation(self):
        window = Window.__new__(Window)
        window.settings = AppSettings(account_flow_mode="reg_us")
        window.post_menu_step_factories = dict(POST_MENU_STEP_FACTORIES)
        window.cancel = threading.Event()
        window.events = queue.Queue()
        window.otp_events = queue.Queue()
        window.otp_status_events = queue.Queue()
        window.post_menu_sessions = {}
        window.post_menu_steps = {}
        window.post_menu_stops = {}
        window.post_menu_workers = {}
        window.phone_stop_after_step = {}
        window.post_menu_resume_after_stop = set()
        window.menu_opened_at = {}
        window.phone_serials = {0: "127.0.0.1:5001"}
        window.values = [{"profile_name": SimpleNamespace(get=lambda: "q1")}]
        window.jobs = {0: RunJob(0, "batch", None, account=AccountData(
            "12025550123", "Example", "Example456!", "https://example.test/otp"))}
        with patch("amazon_android.desktop.threading.Thread", return_value=Mock()):
            window._start_post_menu(0)
        self.assertEqual(window.post_menu_sessions[0].registration.flow_mode, "reg_us")
        self.assertEqual([step.name for step in window.post_menu_steps[0]], ["b1 Reg US"])
