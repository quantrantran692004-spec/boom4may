from contextlib import nullcontext
import queue
import threading
import time
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from amazon_android import q7_random_prefix as random_prefix
from amazon_android.cloud import CloudPhone
from amazon_android.core import ToolError
from amazon_android.desktop import POST_MENU_STEP_FACTORIES, Window
from amazon_android.q7_state_machine import build_q7_pilot_steps
from amazon_android.post_menu import (AttemptDeadline, PostMenuSession, PostMenuStep,
                                      RecoverableStepError, RegistrationState)
from amazon_android.runner import RunJob


class RandomPrefixTests(unittest.TestCase):
    def setUp(self):
        reader = patch.object(random_prefix, "_read_hierarchy", return_value=[])
        reader.start()
        self.addCleanup(reader.stop)
        self.phone = CloudPhone("127.0.0.1:5001")
        self.job = RunJob(0, "batch", None)
        self.deadline = AttemptDeadline(None)
        self.stop = threading.Event()

    def test_twelve_slots_have_three_prefix_steps_before_b4(self):
        self.assertEqual(set(POST_MENU_STEP_FACTORIES), set(range(12)))
        self.assertIs(POST_MENU_STEP_FACTORIES[6], build_q7_pilot_steps)
        for factory in POST_MENU_STEP_FACTORIES.values():
            steps = factory(self.phone, lambda _: None)
            self.assertEqual([step.name for step in steps[:4]],
                             ["b1 ngẫu nhiên", "b2 ngẫu nhiên", "b3 ngẫu nhiên",
                              "b4 Sign In"])

    def test_all_twelve_phones_have_distinct_prefix_sequences_per_batch(self):
        for batch_id in ("first-batch", "next-batch"):
            first = [random_prefix._first_point(RunJob(index, batch_id, None))
                     for index in range(12)]
            self.assertEqual(len(set(first)), 12)
            self.assertEqual(set(first), set(random_prefix.POINTS))
        self.assertNotEqual(
            [random_prefix._first_point(RunJob(index, "first-batch", None))
             for index in range(12)],
            [random_prefix._first_point(RunJob(index, "next-batch", None))
             for index in range(12)])

    def test_three_steps_use_independent_random_positions_and_open_children(self):
        state = RegistrationState()
        steps = random_prefix.build_random_steps(self.phone, lambda _: None,
                                                  registration=state)
        commands = []
        def adb(_phone, *args, **_kwargs):
            commands.append(args)
            return SimpleNamespace(stdout="Physical size: 420x840")
        with patch.object(random_prefix, "cloud_adb", side_effect=adb), \
             patch.object(random_prefix, "_tap_child", return_value=True) as child, \
             patch.object(random_prefix.secrets, "choice", side_effect=lambda items: items[0]), \
             patch.object(self.stop, "wait", return_value=False) as wait:
            for step in steps[:3]:
                step.action(self.job, self.deadline, self.stop)
        taps = [command for command in commands if command[:3] == ("shell", "input", "tap")]
        category = [command for command in taps if int(command[-1]) < 740]
        self.assertEqual(len(category), 3)
        self.assertEqual(len(set(command[3:] for command in category)), 3)
        self.assertEqual(state.prefix_completed, {1, 2, 3})
        self.assertEqual(child.call_count, 3)
        self.assertEqual(sum(call.args == (11,) for call in wait.call_args_list), 3)

    def test_child_tap_uses_visible_submenu_bounds(self):
        nodes = [
            {"text": "Shop by category", "bounds": "[1,1][200,40]"},
            {"text": "Pets", "bounds": "[1,50][130,150]"},
            {"text": "Gifting", "bounds": "[140,50][270,150]"},
            {"text": "Books and Reading", "bounds": "[280,50][400,150]"},
            {"text": "Dogs", "bounds": "[20,170][390,220]"},
            {"text": "Sign In", "bounds": "[1,650][400,700]"},
        ]
        with patch.object(random_prefix, "_read_hierarchy", return_value=nodes), \
             patch.object(random_prefix, "cloud_adb") as adb:
            self.assertTrue(random_prefix._tap_child(self.phone, self.deadline, self.stop))
        self.assertEqual(adb.call_args.args[1:5], ("shell", "input", "tap", "205"))
        self.assertEqual(adb.call_args.args[5], "195")

    def test_opened_page_is_viewed_for_each_of_three_steps_before_b4(self):
        state = RegistrationState()
        steps = random_prefix.build_random_steps(self.phone, lambda _: None,
                                                  registration=state)
        page = [{"text": "Category page", "bounds": "[20,100][330,150]"}]
        with patch.object(random_prefix, "_read_hierarchy", return_value=page), \
             patch.object(random_prefix, "cloud_adb", return_value=SimpleNamespace(
                 stdout="Physical size: 420x840")), \
             patch.object(random_prefix, "_tap_child") as child, \
             patch.object(self.stop, "wait", return_value=False) as wait:
            for number, step in enumerate(steps[:3], 1):
                step.action(self.job, self.deadline, self.stop)
                self.assertEqual(len(state.prefix_completed), number)
                if number < 3:
                    with self.assertRaises(RecoverableStepError):
                        steps[3].action(self.job, self.deadline, self.stop)
        child.assert_not_called()
        self.assertEqual(sum(call.args == (11,) for call in wait.call_args_list), 3)
        self.assertEqual(state.prefix_completed, {1, 2, 3})

    def test_child_waits_for_expanded_menu_and_never_taps_sign_in(self):
        loading = [{"text": "Shop by category", "bounds": "[1,1][200,40]"}]
        menu = loading + [
            {"text": "Pets", "bounds": "[1,50][130,150]"},
            {"text": "Gifting", "bounds": "[140,50][270,150]"},
            {"text": "Books and Reading", "bounds": "[280,50][400,150]"},
            {"text": "Cats", "bounds": "[20,170][390,220]"},
            {"text": "Sign In", "bounds": "[1,650][400,700]"},
        ]
        with patch.object(random_prefix, "_read_hierarchy",
                          side_effect=[loading, menu]), \
             patch.object(random_prefix, "cloud_adb") as adb:
            self.assertTrue(random_prefix._tap_child(self.phone, self.deadline, self.stop))
        self.assertEqual(adb.call_args.args[5], "195")

    def test_failed_tap_tries_other_positions_and_scrolls(self):
        commands = []
        def adb(_phone, *args, **_kwargs):
            commands.append(args)
            if args[:3] == ("shell", "input", "tap") and len(
                    [cmd for cmd in commands if cmd[:3] == ("shell", "input", "tap")]) <= 3:
                raise ToolError("tap failed")
            return SimpleNamespace(stdout="Physical size: 420x840")
        step = random_prefix.build_random_steps(self.phone, lambda _: None)[0]
        with patch.object(random_prefix, "cloud_adb", side_effect=adb), \
             patch.object(random_prefix, "_tap_child", return_value=True), \
             patch.object(random_prefix.secrets, "choice", side_effect=lambda items: items[0]), \
             patch.object(self.stop, "wait", return_value=False):
            step.action(self.job, self.deadline, self.stop)
        self.assertTrue(any(cmd[:3] == ("shell", "input", "swipe") for cmd in commands))

    def test_no_successful_tap_keeps_b1_and_blocks_b4(self):
        state = RegistrationState()
        steps = random_prefix.build_random_steps(self.phone, lambda _: None,
                                                  registration=state)
        def adb(_phone, *args, **_kwargs):
            if args[:3] == ("shell", "input", "tap"):
                raise ToolError("tap failed")
            return SimpleNamespace(stdout="Physical size: 420x840")
        with patch.object(random_prefix, "cloud_adb", side_effect=adb), \
             patch.object(random_prefix, "_tap_child", return_value=True), \
             patch.object(random_prefix.secrets, "choice", side_effect=lambda items: items[0]):
            with self.assertRaises(RecoverableStepError):
                steps[0].action(self.job, self.deadline, self.stop)
        self.assertEqual(state.prefix_completed, set())
        with self.assertRaises(RecoverableStepError):
            steps[3].action(self.job, self.deadline, self.stop)

    def test_q7_prefix_timeout_pauses_without_marking_step_complete(self):
        state = RegistrationState(q7_prefix_started_at={1: time.monotonic() - 91})
        steps = random_prefix.build_random_steps(self.phone, lambda _: None,
                                                  registration=state)
        with self.assertRaises(random_prefix.Q7PrefixTimeout):
            steps[0].action(self.job, self.deadline, self.stop)
        self.assertEqual(state.prefix_completed, set())
        self.assertNotIn(1, state.q7_prefix_started_at)

    def test_b4_returns_to_menu_and_uses_existing_action(self):
        state = RegistrationState(prefix_completed={1, 2, 3})
        called = []
        with patch.object(random_prefix, "build_common_steps",
                          return_value=(PostMenuStep("b4 Sign In",
                                                     lambda *_: called.append("b4")),)):
            steps = random_prefix.build_random_steps(self.phone, lambda _: None,
                                                      registration=state)
        commands = []
        def adb(_phone, *args, **_kwargs):
            commands.append(args)
            return SimpleNamespace(stdout="Physical size: 420x840")
        with patch.object(random_prefix, "cloud_adb", side_effect=adb):
            steps[3].action(self.job, self.deadline, self.stop)
        self.assertEqual(called, ["b4"])
        self.assertTrue(any(cmd[:3] == ("shell", "input", "tap") for cmd in commands))

    def test_random_route_does_not_skip_prefix(self):
        window = Window.__new__(Window)
        session = PostMenuSession("batch", 0, "q1")
        steps = random_prefix.build_random_steps(self.phone, lambda _: None)
        context = {"serials": {0: self.phone.serial}, "steps": {0: steps},
                   "factories": {0: build_q7_pilot_steps},
                   "events": queue.Queue(), "otp": queue.Queue(),
                   "otp_status": queue.Queue()}
        with patch("amazon_android.isolated_reader.phone_reader",
                   return_value=nullcontext()), \
             patch.object(session, "run") as run:
            window._run_post_menu(session, self.job, steps, self.stop, context)
            self.assertIsNone(run.call_args.kwargs["route"](
                0, self.job, self.deadline, self.stop))


if __name__ == "__main__":
    unittest.main()
