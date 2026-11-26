import threading
import time
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from amazon_android.cloud import CloudPhone
from amazon_android.core import ToolError
from amazon_android.account_flow import _wait_screen
from amazon_android.post_menu import AttemptDeadline, PostMenuSession, PostMenuStep, RegistrationState
from amazon_android.q7_state_machine import (
    ActionValidator, RecoveryHandler, ResultVerifier, SPECS, StateDeadline, StateDetector,
    StateMachineStop, StateMachineTimeout, TransitionManager,
    build_q7_pilot_steps,
)
from amazon_android.post_menu import RecoverableStepError
from amazon_android.runner import AccountData, RunJob


class Q7StateMachineTests(unittest.TestCase):
    def setUp(self):
        self.phone = CloudPhone("127.0.0.1:5007")
        self.job = RunJob(6, "batch", None, account=AccountData(
            "12025550107", "Example User", "ExampleOnly",
            "https://example.test/otp"))
        self.stop = threading.Event()

    def identifier(self, value=""):
        return [
            {"text": "Enter mobile number or email", "bounds": "[0,10][200,40]"},
            {"text": "Continue", "bounds": "[0,180][200,220]"},
            {"text": value, "class": "android.widget.EditText",
             "bounds": "[0,50][200,100]", "focused": "true"},
        ]

    def test_state_specs_cover_existing_common_steps_without_changing_actions(self):
        steps = build_q7_pilot_steps(self.phone, lambda _: None)
        post_auth = next(i for i, step in enumerate(steps)
                         if step.name.startswith('b12 '))
        self.assertEqual([step.name for step in steps[3:post_auth]],
                         [spec.name for spec in SPECS])
        self.assertEqual([step.name.split(" ", 1)[0] for step in steps[post_auth:]],
                         [f'b{i}' for i in range(12, 17)] + ['b16a'] +
                         [f'b{i}' for i in range(17, 23)])
        self.assertEqual([step.name for step in steps[:3]],
                         ["b1 ngẫu nhiên", "b2 ngẫu nhiên", "b3 ngẫu nhiên"])

    def test_detector_recovers_one_loading_frame_then_identifies_form(self):
        with patch("amazon_android.q7_state_machine._read_nodes",
                   side_effect=[[], self.identifier()]):
            kind, _ = StateDetector(self.phone).observe(
                StateDeadline(3), self.stop)
        self.assertEqual(kind, "IDENTIFIER")

    def test_unknown_and_wrong_machine_stop_before_action(self):
        with patch("amazon_android.q7_state_machine._read_nodes", return_value=[]):
            with self.assertRaises(StateMachineStop):
                StateDetector(self.phone).observe(StateDeadline(3), self.stop,
                                                  unknown_wait=0)
        other = RunJob(0, "batch", None, account=self.job.account)
        with self.assertRaises(StateMachineStop):
            ActionValidator.check(SPECS[2], "IDENTIFIER", self.identifier(), other)

    def test_disconnected_adb_is_distinct_from_unknown_screen(self):
        from types import SimpleNamespace
        with patch("amazon_android.q7_state_machine._read_nodes",
                   side_effect=ToolError("read failed")), \
             patch("amazon_android.q7_state_machine.cloud_adb",
                   return_value=SimpleNamespace(returncode=1, stdout="offline")):
            with self.assertRaises(StateMachineStop) as raised:
                StateDetector(self.phone).observe(StateDeadline(3), self.stop)
        self.assertEqual(raised.exception.kind, "connection_lost")
        with patch("amazon_android.q7_state_machine.cloud_adb",
                   return_value=SimpleNamespace(returncode=1, stdout="offline")):
            self.assertEqual(RecoveryHandler.classify_action_error(
                self.phone, ToolError("tap failed")), "connection_lost")

    def test_q7_wait_stops_on_wrong_known_screen(self):
        country = [
            {"text": "Country/region code", "bounds": "[0,0][100,30]"},
            {"text": "United States +1", "bounds": "[0,40][100,80]"},
            {"text": "United Kingdom +44", "bounds": "[0,90][100,130]"},
        ]
        with patch("amazon_android.account_flow._read_nodes", return_value=country):
            with self.assertRaisesRegex(ToolError, "COUNTRY"):
                _wait_screen(self.phone, {"SMS"}, StateDeadline(3), self.stop)

    def test_q7_wait_keeps_observing_a_valid_previous_screen(self):
        later = [
            {"text": "Looks like you are new to Amazon"},
            {"text": "Proceed to create an account"},
        ]
        deadline = StateDeadline(3, pending_screens=frozenset({"IDENTIFIER"}))
        with patch("amazon_android.account_flow._read_nodes",
                   side_effect=[self.identifier(), later]):
            observed = _wait_screen(self.phone, {"NEW_ACCOUNT"}, deadline,
                                    self.stop)
        self.assertEqual(observed, later)

    def test_transition_requires_expected_result_and_matching_phone(self):
        self.assertFalse(TransitionManager.allows(SPECS[4], "IDENTIFIER"))
        self.assertTrue(TransitionManager.allows(SPECS[4], "NEW_ACCOUNT"))
        detector = StateDetector(self.phone)
        verifier = ResultVerifier(detector)
        with patch("amazon_android.q7_state_machine._read_nodes",
                   return_value=self.identifier("999")):
            with self.assertRaisesRegex(StateMachineStop, "SĐT"):
                verifier.verify(SPECS[2], self.job, StateDeadline(3), self.stop)
        wrong_account = [
            {"text": "Looks like you are new to Amazon"},
            {"text": "Proceed to create an account"},
            {"text": "Mobile number 2025550199"},
        ]
        with self.assertRaisesRegex(ToolError, "SĐT"):
            ActionValidator.check(SPECS[5], "NEW_ACCOUNT", wrong_account,
                                  self.job)

    def test_expired_state_and_unrecognized_create_result_pause(self):
        with self.assertRaises(StateMachineTimeout):
            StateDeadline(1, started=time.monotonic() - 2).remaining()
        with patch("amazon_android.q7_state_machine._read_nodes",
                   return_value=self.identifier()):
            with self.assertRaisesRegex(StateMachineStop, "chưa có dấu hiệu"):
                ResultVerifier(StateDetector(self.phone)).verify(
                    SPECS[-1], self.job, StateDeadline(3), self.stop)

    def test_create_result_can_enter_documented_browse_menu_without_claiming_success(self):
        menu = [{"text": "Shop by category", "bounds": "[10,10][200,40]"}]
        with patch("amazon_android.q7_state_machine._read_nodes", return_value=menu):
            ResultVerifier(StateDetector(self.phone)).verify(
                SPECS[-1], self.job, StateDeadline(3), self.stop)

    def test_final_sms_result_can_land_on_home_before_b12_opens_browse(self):
        home = [{"text": "Today's picks", "bounds": "[10,10][200,40]"},
                {"content-desc": "Browse menu Tab, 4 of 4",
                 "bounds": "[300,700][390,740]"},
                {"content-desc": "Home Tab, 1 of 4",
                 "bounds": "[10,700][80,740]"}]
        with patch("amazon_android.q7_state_machine._read_nodes",
                   return_value=home), \
             patch("amazon_android.q7_state_machine.cloud_adb") as adb:
            ResultVerifier(StateDetector(self.phone)).verify(
                SPECS[-1], self.job, StateDeadline(3), self.stop)
        adb.assert_not_called()

    def test_login_otp_visual_confirmation_survives_blank_native_readback(self):
        sms = [{"text": "Verify mobile number", "bounds": "[10,10][200,40]"},
               {"text": "Enter security code", "bounds": "[10,50][200,80]"},
               {"text": self.job.account.phone, "bounds": "[10,90][200,120]"},
               {"text": "", "class": "android.widget.EditText",
                "bounds": "[10,130][200,170]"}]
        state = RegistrationState(login_jump_seen=True, login_otp_confirmed=True,
                                  code="222222")
        with patch("amazon_android.q7_state_machine._read_nodes", return_value=sms):
            ResultVerifier(StateDetector(self.phone)).verify(
                SPECS[-2], self.job, StateDeadline(3), self.stop,
                registration=state)
            with self.assertRaisesRegex(StateMachineStop, "sáu số OTP"):
                ResultVerifier(StateDetector(self.phone)).verify(
                    SPECS[-2], self.job, StateDeadline(3), self.stop,
                    registration=RegistrationState(create_flow_seen=True))

    def test_final_sms_accepts_home_or_browse_menu(self):
        pages = ([{"content-desc": "Home Tab, 1 of 4", "selected": "true",
                   "bounds": "[10,700][80,740]"}],
                 [{"text": "Shop by category", "bounds": "[20,100][330,160]"}])
        for page in pages:
            with self.subTest(page=page), patch(
                    "amazon_android.q7_state_machine._read_nodes", return_value=page):
                ResultVerifier(StateDetector(self.phone)).verify(
                    SPECS[-1], self.job, StateDeadline(3), self.stop)

    def test_q7_resume_after_create_can_continue_from_visible_menu_without_retap(self):
        destinations = (
            [{"text": "Shop by category", "bounds": "[10,10][200,40]"}],
            [{"text": "Today's picks", "bounds": "[10,10][200,40]"},
             {"content-desc": "Browse menu Tab, 4 of 4",
              "bounds": "[300,700][390,740]"}],
        )
        for marker in ("create_pressed", "login_verify_pressed"):
            for destination in destinations:
                with self.subTest(marker=marker, destination=destination[0]["text"]):
                    self._assert_q7_resume_without_repeating_sms(marker, destination)

    def _assert_q7_resume_without_repeating_sms(self, marker, destination):
        state = RegistrationState(**{marker: True})
        actions = [Mock() for _ in SPECS]
        original = tuple(PostMenuStep(f"b{i} ngẫu nhiên", Mock())
                         for i in (1, 2, 3))
        original += tuple(PostMenuStep(spec.name, action)
                          for spec, action in zip(SPECS, actions))
        with patch("amazon_android.q7_state_machine.build_random_steps",
                   return_value=original):
            steps = build_q7_pilot_steps(self.phone, lambda _: None,
                                         registration=state)
        create_step = steps[3 + len(SPECS) - 1]
        with patch("amazon_android.q7_state_machine._read_nodes",
                   return_value=destination):
            create_step.action(self.job, AttemptDeadline(None), self.stop)
        actions[-1].assert_not_called()

    def test_q7_wrapper_runs_action_then_verifies_value(self):
        actions = [Mock() for _ in range(len(SPECS))]
        originals = tuple(PostMenuStep(f"b{i} ngẫu nhiên", Mock()) for i in (1, 2, 3))
        originals += tuple(PostMenuStep(spec.name, action)
                           for spec, action in zip(SPECS, actions))
        with patch("amazon_android.q7_state_machine.build_random_steps",
                   return_value=originals):
            steps = build_q7_pilot_steps(self.phone, lambda _: None)
        with patch("amazon_android.q7_state_machine._read_nodes",
                   side_effect=[self.identifier(),
                                self.identifier(self.job.account.phone)]):
            steps[5].action(self.job, AttemptDeadline(None), self.stop)
        actions[2].assert_called_once()

    def test_q7_skips_known_direct_sms_jump_without_replaying_earlier_actions(self):
        actions = [Mock() for _ in SPECS]
        originals = tuple(PostMenuStep(f"b{i} ngẫu nhiên", Mock()) for i in (1, 2, 3))
        originals += tuple(PostMenuStep(spec.name, action)
                           for spec, action in zip(SPECS, actions))
        with patch("amazon_android.q7_state_machine.build_random_steps",
                   return_value=originals):
            steps = build_q7_pilot_steps(self.phone, lambda _: None)
        sms = [{"text": "Verify mobile number"},
               {"text": "Enter security code"},
               {"text": self.job.account.phone}]
        with patch("amazon_android.q7_state_machine._read_nodes", return_value=sms):
            for index in range(3 + 2, 3 + 7):
                steps[index].action(self.job, AttemptDeadline(None), self.stop)
        for action in actions[2:7]:
            action.assert_not_called()

    def test_q7_remembers_create_form_when_earlier_step_is_skipped(self):
        from amazon_android.post_menu import RegistrationState
        state = RegistrationState()
        actions = [Mock() for _ in SPECS]
        originals = tuple(PostMenuStep(f"b{i} ngẫu nhiên", Mock())
                          for i in (1, 2, 3))
        originals += tuple(PostMenuStep(spec.name, action)
                           for spec, action in zip(SPECS, actions))
        with patch("amazon_android.q7_state_machine.build_random_steps",
                   return_value=originals):
            steps = build_q7_pilot_steps(self.phone, lambda _: None,
                                         registration=state)
        form = [{"text": "Create account"}, {"text": "First and last name"},
                {"text": self.job.account.phone}]
        with patch("amazon_android.q7_state_machine._read_nodes", return_value=form):
            steps[3 + 4].action(self.job, AttemptDeadline(None), self.stop)
        self.assertTrue(state.create_flow_seen)
        self.assertFalse(state.login_jump_seen)
        actions[4].assert_not_called()

    def test_q7_b4_does_not_open_menu_when_already_on_whatsapp(self):
        actions = [Mock() for _ in SPECS]
        originals = tuple(PostMenuStep(f"b{i} ngẫu nhiên", Mock()) for i in (1, 2, 3))
        originals += tuple(PostMenuStep(spec.name, action)
                           for spec, action in zip(SPECS, actions))
        with patch("amazon_android.q7_state_machine.build_random_steps",
                   return_value=originals):
            steps = build_q7_pilot_steps(self.phone, lambda _: None)
        whatsapp = [{"text": "Verify with WhatsApp"},
                    {"text": "Send code by SMS"},
                    {"text": self.job.account.phone}]
        with patch("amazon_android.q7_state_machine.cloud_adb",
                   return_value=SimpleNamespace(stdout="mCurrentFocus=com.amazon.mShop.android.shopping")), \
             patch("amazon_android.q7_state_machine._read_nodes", return_value=whatsapp), \
             patch("amazon_android.q7_state_machine._menu") as menu:
            steps[3].action(self.job, AttemptDeadline(None), self.stop)
        menu.assert_not_called()
        actions[0].assert_not_called()

    def test_q7_b7_accepts_sms_result_after_one_continue(self):
        actions = [Mock() for _ in SPECS]
        originals = tuple(PostMenuStep(f"b{i} ngẫu nhiên", Mock()) for i in (1, 2, 3))
        originals += tuple(PostMenuStep(spec.name, action)
                           for spec, action in zip(SPECS, actions))
        with patch("amazon_android.q7_state_machine.build_random_steps",
                   return_value=originals):
            steps = build_q7_pilot_steps(self.phone, lambda _: None)
        sms = [{"text": "Verify mobile number"},
               {"text": "Enter security code"},
               {"text": self.job.account.phone}]
        with patch("amazon_android.q7_state_machine._read_nodes",
                   side_effect=[self.identifier(), sms]):
            steps[7].action(self.job, AttemptDeadline(None), self.stop)
        actions[4].assert_called_once()

    def test_q7_does_not_repeat_continue_when_result_is_already_visible(self):
        actions = [Mock() for _ in SPECS]
        originals = tuple(PostMenuStep(f"b{i} ngẫu nhiên", Mock()) for i in (1, 2, 3))
        originals += tuple(PostMenuStep(spec.name, action)
                           for spec, action in zip(SPECS, actions))
        with patch("amazon_android.q7_state_machine.build_random_steps",
                   return_value=originals):
            steps = build_q7_pilot_steps(self.phone, lambda _: None)
        new = [{"text": "Looks like you are new to Amazon"},
               {"text": "Proceed to create an account"},
               {"text": self.job.account.phone}]
        whatsapp = [{"text": "Verify with WhatsApp"},
                    {"text": "Send code by SMS"},
                    {"text": self.job.account.phone}]
        with patch("amazon_android.q7_state_machine._read_nodes", return_value=new):
            steps[7].action(self.job, AttemptDeadline(None), self.stop)
        with patch("amazon_android.q7_state_machine._read_nodes", return_value=whatsapp):
            steps[9].action(self.job, AttemptDeadline(None), self.stop)
        actions[4].assert_not_called()
        actions[6].assert_not_called()

    def test_focus_recovery_is_bounded_and_duplicate_locator_stops(self):
        actions = [Mock() for _ in SPECS]
        originals = tuple(PostMenuStep(f"b{i} ngẫu nhiên", Mock()) for i in (1, 2, 3))
        originals += tuple(PostMenuStep(spec.name, action)
                           for spec, action in zip(SPECS, actions))
        with patch("amazon_android.q7_state_machine.build_random_steps",
                   return_value=originals):
            steps = build_q7_pilot_steps(self.phone, lambda _: None)
        actions[1].side_effect = [RecoverableStepError("focus chưa có"), None]
        with patch("amazon_android.q7_state_machine._read_nodes",
                   return_value=self.identifier()):
            steps[4].action(self.job, AttemptDeadline(None), self.stop)
        self.assertEqual(actions[1].call_count, 2)
        actions[4].side_effect = RecoverableStepError("nhiều nút Continue")
        with patch("amazon_android.q7_state_machine._read_nodes",
                   return_value=self.identifier()):
            with self.assertRaises(StateMachineStop) as raised:
                steps[7].action(self.job, AttemptDeadline(None), self.stop)
        self.assertEqual(raised.exception.kind, "locator_or_focus")
        actions[4].assert_called_once()

    def test_slow_transition_is_observed_without_replaying_continue(self):
        actions = [Mock() for _ in SPECS]
        originals = tuple(PostMenuStep(f"b{i} ngẫu nhiên", Mock()) for i in (1, 2, 3))
        originals += tuple(PostMenuStep(spec.name, action)
                           for spec, action in zip(SPECS, actions))
        with patch("amazon_android.q7_state_machine.build_random_steps",
                   return_value=originals):
            steps = build_q7_pilot_steps(self.phone, lambda _: None)
        new_account = [
            {"text": "Looks like you are new to Amazon"},
            {"text": "Proceed to create an account"},
            {"text": "Mobile number 2025550107"},
        ]
        with patch("amazon_android.q7_state_machine._read_nodes",
                   side_effect=[self.identifier(), self.identifier(), new_account]):
            steps[7].action(self.job, AttemptDeadline(None), self.stop)
        actions[4].assert_called_once()

    def test_b4_requires_amazon_foreground_before_returning_to_menu(self):
        steps = build_q7_pilot_steps(self.phone, lambda _: None)
        with patch("amazon_android.q7_state_machine.cloud_adb",
                   return_value=SimpleNamespace(stdout="mCurrentFocus=system.dialog")), \
             patch("amazon_android.q7_state_machine._menu") as menu:
            with self.assertRaisesRegex(StateMachineStop, "Amazon ở phía trước"):
                steps[3].action(self.job, AttemptDeadline(None), self.stop)
        menu.assert_not_called()

    def test_terminal_state_error_pauses_only_q7(self):
        q7 = PostMenuSession("batch", 6, "q7")
        attempts = []
        def fail(*_):
            attempts.append(1)
            raise StateMachineStop("unknown")
        q7.run(self.job, (PostMenuStep("b5 nhập SĐT", fail),),
               lambda *_: None, self.stop)
        self.assertEqual((q7.state, q7.next_step, len(attempts)),
                         ("PAUSED", 0, 1))

    def test_selected_q7_stop_does_not_stop_another_worker(self):
        q7 = PostMenuSession("batch", 6, "q7")
        q8 = PostMenuSession("batch", 7, "q8")
        selected_stop = threading.Event()
        calls = []
        def first(job, *_):
            calls.append((job.index, "first"))
            if job.index == 6:
                selected_stop.set()
        def second(job, *_):
            calls.append((job.index, "second"))
        steps = (PostMenuStep("b1", first), PostMenuStep("b2", second))
        q7.run(self.job, steps, lambda *_: None, self.stop,
               stop_after_step=selected_stop)
        q8.run(RunJob(7, "batch", None), steps, lambda *_: None,
               threading.Event())
        self.assertEqual((q7.state, q7.next_step), ("PAUSED", 1))
        self.assertEqual((q8.state, q8.next_step), ("DONE", 2))
        self.assertEqual(calls, [(6, "first"), (7, "first"), (7, "second")])


if __name__ == "__main__":
    unittest.main()
