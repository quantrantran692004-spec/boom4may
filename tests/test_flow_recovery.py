import threading
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from amazon_android import account_flow as flow
from amazon_android.cloud import CloudPhone
from amazon_android.core import ToolError
from amazon_android.post_menu import AttemptDeadline, RegistrationState
from amazon_android.runner import AccountData, RunJob


def form(value="", focused="true"):
    return [
        {"text": "Create account", "bounds": "[10,10][200,40]"},
        {"text": flow.NAME_FIELD, "class": "android.widget.TextView",
         "bounds": "[10,50][200,80]"},
        {"text": value, "class": "android.widget.EditText",
         "bounds": "[10,90][300,130]", "focused": focused},
    ]


class FlowRecoveryTests(unittest.TestCase):
    def setUp(self):
        self.phone = CloudPhone("127.0.0.1:5001")
        self.deadline = AttemptDeadline(180)
        self.stop = threading.Event()

    def test_ocr_recovers_failed_dump_then_skips_next_hierarchy_read(self):
        with patch.object(flow, "_read_hierarchy", side_effect=flow._UiReadIncomplete("dump")) as hierarchy, \
             patch.object(flow, "_read_visual_nodes", return_value=form()):
            self.assertEqual(flow.screen(flow._read_nodes(self.phone, self.deadline, self.stop)), "CREATE_FORM")
            self.assertEqual(flow.screen(flow._read_nodes(self.phone, self.deadline, self.stop)), "CREATE_FORM")
        self.assertEqual(hierarchy.call_count, 1)

    def test_read_recovers_two_transient_failures_but_stop_is_immediate(self):
        with patch.object(flow, "_read_nodes_once", side_effect=[
                flow._UiReadIncomplete("xml"), flow._UiReadIncomplete("capture"), form()]) as read:
            self.assertEqual(flow.screen(flow._read_nodes(self.phone, self.deadline, self.stop)), "CREATE_FORM")
        self.assertEqual(read.call_count, 3)
        self.stop.set()
        with patch.object(flow, "_read_nodes_once") as read:
            with self.assertRaises(ToolError):
                flow._read_nodes(self.phone, self.deadline, self.stop)
        read.assert_not_called()

    def test_partial_delivery_is_read_back_and_only_missing_suffix_is_typed(self):
        with patch.object(flow, "_read_nodes", side_effect=[form("Example"), form("Example"),
                         form("Example"), form("Example User")]), \
             patch.object(flow, "type_characters", side_effect=[ToolError("uncertain input"), None]) as typed, \
             patch.object(flow, "_tap"), patch.object(flow, "cloud_adb"):
            result = flow._type_field(self.phone, flow.NAME_FIELD, "Example User",
                                      self.deadline, self.stop, nodes=form())
        self.assertEqual([call.args[1] for call in typed.call_args_list], ["Example User", " User"])
        self.assertEqual(result[-1]["text"], "Example User")

    def test_native_name_focus_is_checked_before_typing(self):
        with patch.object(flow, "_read_nodes", side_effect=[form("", "false"), form(), form("Example User")]), \
             patch.object(flow, "_tap") as tap, patch.object(flow, "type_characters"):
            flow._type_field(self.phone, flow.NAME_FIELD, "Example User", self.deadline,
                             self.stop, nodes=form("", "false"))
        self.assertEqual(tap.call_count, 2)

    def test_conflicting_input_is_never_overwritten_or_retried(self):
        with patch.object(flow, "type_characters") as typed:
            with self.assertRaises(ToolError):
                flow._type_field(self.phone, flow.NAME_FIELD, "Example User", self.deadline,
                                 self.stop, nodes=form("Other person"))
        typed.assert_not_called()

    def test_keyboard_request_alone_does_not_confirm_keyboard_visible(self):
        with patch.object(flow, "cloud_adb", return_value=SimpleNamespace(stdout="mShowRequested=true mInputShown=false")):
            self.assertFalse(flow._keyboard_visible(self.phone, self.deadline))

    def test_ocr_focus_retry_refreshes_moved_field_bounds(self):
        original = dict(form()[-1], vision="true", **{"vision-field-kind": "name"})
        moved = dict(original, bounds="[20,100][310,140]")
        with patch.object(flow, "_keyboard_visible", side_effect=[False, True]), \
             patch.object(flow, "_read_nodes", return_value=form()[:-1] + [moved]), \
             patch.object(flow, "_tap") as tap:
            flow._tap_input(self.phone, original, self.deadline, self.stop)
        self.assertEqual([call.args[1]["bounds"] for call in tap.call_args_list],
                         [original["bounds"], moved["bounds"]])

    def test_sms_dispatch_error_is_resolved_by_reading_without_resending(self):
        state = RegistrationState()
        job = RunJob(0, "batch", None, account=AccountData("12025550123", "Example User", "", ""))
        whatsapp = [{"text": text, "bounds": "[10,10][200,50]"}
                    for text in ("Verify with WhatsApp", "Send code by SMS")]
        sms = [{"text": text} for text in ("Verify mobile number", flow.OTP_FIELD)]
        action = next(step.action for step in flow.build_common_steps(
            self.phone, lambda _: None, registration=state) if step.name.startswith("b10"))
        with patch.object(flow, "_read_nodes", side_effect=[whatsapp, sms]), \
             patch.object(flow, "_check_summary"), \
             patch.object(flow, "_wait_screen", return_value=sms), \
             patch.object(flow, "_tap", side_effect=ToolError("delivery uncertain")) as tap:
            action(job, self.deadline, self.stop)
            action(job, self.deadline, self.stop)
        self.assertIsNotNone(state.sms_requested_at)
        tap.assert_called_once()

    def test_create_dispatch_marker_survives_error_and_factory_rebuild(self):
        state = RegistrationState()
        job = RunJob(0, "batch", None, account=AccountData("12025550123", "Example User", "", ""))
        sms = [{"text": text, "bounds": "[10,150][300,190]"}
               for text in ("Verify mobile number", flow.OTP_FIELD, "Create your Amazon account")]
        entered = {"text": "123456", "bounds": "[10,90][300,130]"}
        first = flow.build_common_steps(self.phone, lambda _: None, registration=state)[-1].action
        with patch.object(flow, "_read_nodes", side_effect=[sms, [{"text": "next screen"}],
                                                          [{"text": "next screen"}]]), \
             patch.object(flow, "_field", return_value=entered), \
             patch.object(flow, "_check_summary"), \
             patch.object(flow, "_tap", side_effect=ToolError("delivery uncertain")) as tap:
            first(job, self.deadline, self.stop)
            rebuilt = flow.build_common_steps(self.phone, lambda _: None, registration=state)[-1].action
            rebuilt(job, self.deadline, self.stop)
        self.assertTrue(state.create_pressed)
        tap.assert_called_once()

    def test_temporary_missing_field_is_read_again_before_typing(self):
        with patch.object(flow, "_read_nodes", side_effect=[form(), form("Example User")]), \
             patch.object(flow, "type_characters") as typed:
            flow._type_field(self.phone, flow.NAME_FIELD, "Example User", self.deadline,
                             self.stop, nodes=form()[:-1])
        typed.assert_called_once()

    def test_transition_transport_error_is_observed_without_repeating_tap(self):
        target = {"bounds": "[10,10][300,50]"}
        notices = []
        deadline = AttemptDeadline(180, notice=notices.append)
        with patch.object(flow, "_tap", side_effect=ToolError("connection reset after delivery")) as tap:
            flow._tap_for_transition(self.phone, target, deadline)
        tap.assert_called_once()
        self.assertEqual(len(notices), 1)
        with patch.object(flow, "_tap") as tap:
            with self.assertRaises(ToolError):
                flow._tap_for_transition(self.phone, {"bounds": "invalid"}, deadline)
        tap.assert_not_called()

    def test_ocr_cannot_authorize_retyping_a_missing_suffix(self):
        initial = form()
        initial[-1].update({"vision": "true", "vision-field-kind": "name"})
        partial = form("Example")
        partial[-1].update({"vision": "true", "vision-field-kind": "name"})
        with patch.object(flow, "_tap_input"), \
             patch.object(flow, "_read_nodes", return_value=partial), \
             patch.object(flow, "type_characters") as typed:
            with self.assertRaises(ToolError):
                flow._type_field(self.phone, flow.NAME_FIELD, "Example User", self.deadline,
                                 self.stop, nodes=initial)
        typed.assert_called_once()

    def test_webview_read_mode_is_isolated_by_phone_and_expires(self):
        self.deadline.visual_until[self.phone.serial] = float("inf")
        other = CloudPhone("127.0.0.1:5002")
        with patch.object(flow, "_read_hierarchy", return_value=form()) as hierarchy, \
             patch.object(flow, "_read_visual_nodes", return_value=form()) as visual:
            flow._read_nodes(self.phone, self.deadline, self.stop)
            hierarchy.assert_not_called()
            flow._read_nodes(other, self.deadline, self.stop)
            self.assertEqual(hierarchy.call_count, 1)
            self.deadline.visual_until[self.phone.serial] = 0
            flow._read_nodes(self.phone, self.deadline, self.stop)
        self.assertEqual(hierarchy.call_count, 2)
        visual.assert_called_once()

    def test_incomplete_ocr_value_on_resume_never_authorizes_appending(self):
        partial = form("Example")
        partial[-1].update({"vision": "true", "vision-field-kind": "name"})
        with patch.object(flow, "_read_nodes", return_value=partial), \
             patch.object(flow, "_tap_input"), patch.object(flow, "cloud_adb"), \
             patch.object(flow, "type_characters") as typed:
            with self.assertRaises(ToolError):
                flow._type_field(self.phone, flow.NAME_FIELD, "Example User", self.deadline,
                                 self.stop, nodes=partial)
        typed.assert_not_called()

    def test_initial_loading_frame_is_read_again_before_rejecting_form(self):
        with patch.object(flow, "_read_nodes", side_effect=[
                [{"text": "loading"}], [{"text": "loading"}], form()]) as read:
            self.assertEqual(flow.screen(flow._registration_nodes(
                self.phone, self.deadline, self.stop)), "CREATE_FORM")
        self.assertEqual(read.call_count, 3)


if __name__ == "__main__":
    unittest.main()
