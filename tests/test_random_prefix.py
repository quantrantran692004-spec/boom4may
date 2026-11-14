from contextlib import nullcontext
import queue
import threading
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from amazon_android import random_prefix
from amazon_android.cloud import CloudPhone
from amazon_android.core import ToolError
from amazon_android.desktop import POST_MENU_STEP_FACTORIES, Window
from amazon_android.post_menu import (AttemptDeadline, PostMenuSession, PostMenuStep,
                                      RecoverableStepError, RegistrationState)
from amazon_android.runner import RunJob


class RandomPrefixTests(unittest.TestCase):
    def setUp(self):
        self.phone = CloudPhone("127.0.0.1:5001")
        self.job = RunJob(0, "batch", None)
        self.deadline = AttemptDeadline(None)
        self.stop = threading.Event()

    def test_twelve_slots_have_three_prefix_steps_before_b4(self):
        self.assertEqual(set(POST_MENU_STEP_FACTORIES), set(range(12)))
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

    def test_three_steps_use_independent_random_positions_without_ocr(self):
        state = RegistrationState()
        steps = random_prefix.build_random_steps(self.phone, lambda _: None,
                                                  registration=state)
        commands = []
        def adb(_phone, *args, **_kwargs):
            commands.append(args)
            return SimpleNamespace(stdout="Physical size: 420x840")
        with patch.object(random_prefix, "cloud_adb", side_effect=adb), \
             patch.object(random_prefix.secrets, "choice", side_effect=lambda items: items[0]), \
             patch.object(self.stop, "wait", return_value=False):
            for step in steps[:3]:
                step.action(self.job, self.deadline, self.stop)
        taps = [command for command in commands if command[:3] == ("shell", "input", "tap")]
        category = [command for command in taps if int(command[-1]) < 740]
        self.assertEqual(len(category), 3)
        self.assertEqual(len(set(command[3:] for command in category)), 3)
        self.assertEqual(state.prefix_completed, {1, 2, 3})

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
             patch.object(random_prefix.secrets, "choice", side_effect=lambda items: items[0]):
            with self.assertRaises(RecoverableStepError):
                steps[0].action(self.job, self.deadline, self.stop)
        self.assertEqual(state.prefix_completed, set())
        with self.assertRaises(RecoverableStepError):
            steps[3].action(self.job, self.deadline, self.stop)

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
                   "factories": {0: random_prefix.build_random_steps},
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
