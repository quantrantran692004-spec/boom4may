from worker_helpers import on_worker
import queue
import sys
import threading
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from amazon_android.cloud import CloudPhone
from amazon_android.desktop import Window
from amazon_android.post_menu import PostMenuSession, PostMenuStep, RegistrationState
from amazon_android.q1_flow import build_q1_steps
from amazon_android.q2_flow import build_q2_steps
from amazon_android.runner import AccountData, RunJob


class ResumeRegistrationStateTests(unittest.TestCase):
    def setUp(self):
        self.job = RunJob(0, "batch", None, account=AccountData(
            "12025550123", "Example User", "Example456!",
            "https://apifc.net/smsrecord?token=q1"))
        self.window = Window.__new__(Window)
        self.window.cancel = threading.Event()
        self.window.events = queue.Queue()
        self.window.otp_events = queue.Queue()
        self.window.otp_status_events = queue.Queue()
        self.window.jobs = {0: self.job}
        self.window.phone_serials = {0: "127.0.0.1:5001"}
        self.window.post_menu_sessions = {}
        self.window.post_menu_steps = {}
        self.window.post_menu_workers = {}
        self.window.post_menu_stops = {}
        self.window.phone_stop_after_step = {}
        self.window.menu_opened_at = {}
        self.window.values = [{"profile_name": SimpleNamespace(get=lambda: "q1")}]

    def test_sessions_keep_independent_registration_markers_and_hide_code_in_repr(self):
        first = PostMenuSession("batch", 0, "q1")
        second = PostMenuSession("batch", 1, "q2")
        first.registration.code = "999999"
        first.registration.create_pressed = True
        self.assertIsNot(first.registration, second.registration)
        self.assertEqual(second.registration.code, "")
        self.assertFalse(second.registration.create_pressed)
        self.assertNotIn("999999", repr(first.registration))
        self.assertNotIn("999999", repr(first))

    def test_both_factories_forward_the_supplied_state_to_common_steps(self):
        registration = RegistrationState(123.0, "999999", True)
        phone = CloudPhone("127.0.0.1:5001")
        otp, status = Mock(), Mock()
        for module, factory in (("q1_flow", build_q1_steps),
                                ("q2_flow", build_q2_steps)):
            with self.subTest(module=module), patch(
                    f"amazon_android.{module}.build_common_steps",
                    return_value=()) as common:
                factory(phone, otp, status, registration)
                common.assert_called_once_with(phone, otp, status, registration)

    def test_first_start_creates_state_before_building_steps(self):
        seen = []
        steps = (PostMenuStep("b4", Mock()),)

        def factory(phone, otp, status, registration):
            self.assertIs(self.window.post_menu_sessions[0].registration, registration)
            seen.append((phone.serial, registration))
            return steps

        self.window.post_menu_step_factories = {0: factory}
        with patch("amazon_android.desktop.threading.Thread") as worker:
            self.window._start_post_menu(0)
        session = self.window.post_menu_sessions[0]
        self.assertEqual(session.bound_serial, "127.0.0.1:5001")
        self.assertEqual(seen, [(session.bound_serial, session.registration)])
        self.assertIs(worker.call_args.kwargs["args"][2], steps)
        worker.return_value.start.assert_called_once()

    def test_unguided_q5_reports_missing_prefix_instead_of_silently_returning(self):
        self.window.post_menu_step_factories = {}
        self.window._start_post_menu(4)
        slot, message, state, name = self.window.events.get_nowait()
        self.assertEqual((slot, state, name), (4, 'menu_only', 'q5'))
        self.assertIn('b1–b3', message)
        self.assertEqual(self.window.post_menu_workers, {})

    def test_start_rebinds_changed_serial_without_losing_sent_markers(self):
        session = PostMenuSession("batch", 0, "q1", state="PAUSED",
                                  bound_serial="127.0.0.1:5000")
        session.registration.sms_requested_at = 123.0
        session.registration.code = "999999"
        session.registration.create_pressed = True
        self.window.post_menu_sessions[0] = session
        self.window.post_menu_steps[0] = (PostMenuStep("old", Mock()),)
        replacement = (PostMenuStep("new", Mock()),)
        factory = Mock(return_value=replacement)
        self.window.post_menu_step_factories = {0: factory}
        with patch("amazon_android.desktop.threading.Thread") as worker:
            self.window._start_post_menu(0)
        self.assertEqual(factory.call_args.args[0].serial, "127.0.0.1:5001")
        self.assertIs(factory.call_args.args[3], session.registration)
        self.assertIs(worker.call_args.kwargs["args"][2], replacement)
        self.assertEqual((session.registration.sms_requested_at,
                          session.registration.code, session.registration.create_pressed),
                         (123.0, "999999", True))

    def _run_reconcile(self, *, changed_serial, target):
        session = PostMenuSession("batch", 0, "q1", next_step=1,
                                  state="PAUSED", bound_serial="127.0.0.1:5001")
        registration = session.registration
        registration.sms_requested_at = 123.0
        registration.code = "999999"
        registration.create_pressed = True
        if changed_serial:
            self.window.phone_serials[0] = "127.0.0.1:5002"
        calls = []
        old = tuple(PostMenuStep(str(i), Mock(side_effect=AssertionError("stale steps")))
                    for i in range(2))

        def factory(phone, otp, status, state):
            self.assertIs(state, registration)
            return tuple(PostMenuStep(str(i), lambda *_, n=i:
                                       calls.append((n, phone.serial, state)))
                         for i in range(2))

        self.window.post_menu_step_factories = {0: factory}
        self.window.post_menu_steps[0] = old
        with patch(
                "amazon_android.desktop.route_list_menu", return_value=None), patch(
                "amazon_android.desktop.resume_common_index", return_value=target):
            on_worker(self.window._run_post_menu, session, self.job, old, threading.Event())
        self.assertEqual([entry[0] for entry in calls], list(range(target, 2)))
        self.assertTrue(all(entry[1] == self.window.phone_serials[0] for entry in calls))
        self.assertTrue(all(entry[2] is registration for entry in calls))
        self.assertEqual((registration.sms_requested_at, registration.code,
                          registration.create_pressed), (123.0, "999999", True))
        self.assertEqual(session.bound_serial, self.window.phone_serials[0])
        self.assertEqual(session.state, "DONE")

    def test_resume_rebinds_changed_serial_even_when_screen_keeps_same_step(self):
        self._run_reconcile(changed_serial=True, target=1)

    def test_resume_rewind_keeps_sms_and_create_markers(self):
        self._run_reconcile(changed_serial=False, target=0)


if __name__ == "__main__":
    unittest.main()
