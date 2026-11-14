from contextlib import nullcontext
import queue
import threading
import unittest
from unittest.mock import patch

from amazon_android import random_prefix
from amazon_android.cloud import CloudPhone
from amazon_android.desktop import POST_MENU_STEP_FACTORIES, Window
from amazon_android.post_menu import AttemptDeadline, PostMenuSession, RegistrationState
from amazon_android.core import ToolError
from amazon_android.runner import RunJob


def node(label, top):
    return {"text": label, "bounds": f"[20,{top}][300,{top + 40}]"}


MENU = [node("Shop by category", 20), node("Gifting", 100),
        node("Pets", 160), node("Fashion and Beauty", 220),
        node("Sign In", 300), dict(node("Settings", 360), clickable="true")]


class RandomPrefixTests(unittest.TestCase):
    def setUp(self):
        self.phone = CloudPhone("127.0.0.1:5001")
        self.deadline = AttemptDeadline(None)
        self.stop = threading.Event()
        self.job = RunJob(0, "batch", None)

    def test_all_twelve_slots_use_three_random_steps_and_shared_b4(self):
        self.assertEqual(set(POST_MENU_STEP_FACTORIES), set(range(12)))
        for factory in POST_MENU_STEP_FACTORIES.values():
            steps = factory(self.phone, lambda _: None, registration=RegistrationState())
            self.assertEqual([step.name for step in steps[:4]],
                             ["b1 ngẫu nhiên", "b2 ngẫu nhiên", "b3 ngẫu nhiên",
                              "b4 Sign In"])

    def test_three_taps_use_distinct_live_menu_targets(self):
        state = RegistrationState()
        steps = random_prefix.build_random_steps(self.phone, lambda _: None,
                                                  registration=state)
        tapped = []
        with patch.object(random_prefix, "_read_nodes", return_value=MENU), \
             patch.object(random_prefix, "_ensure_menu", return_value=MENU), \
             patch.object(random_prefix, "_tap_for_transition",
                   side_effect=lambda _phone, target, _deadline: tapped.append(target["text"])), \
             patch.object(random_prefix.secrets, "choice", side_effect=lambda items: items[-1]), \
             patch.object(self.stop, "wait", return_value=False):
            for step in steps[:3]:
                step.action(self.job, self.deadline, self.stop)
        self.assertEqual(len(set(tapped)), 3)
        self.assertEqual(set(tapped), {"Gifting", "Pets", "Fashion and Beauty"})
        self.assertNotIn("sign in", state.prefix_choices.values())

    def test_resume_keeps_choice_and_new_batch_draws_again(self):
        state = RegistrationState()
        step = random_prefix.build_random_steps(self.phone, lambda _: None,
                                                registration=state)[0]
        with patch.object(random_prefix, "_read_nodes", return_value=MENU), \
             patch.object(random_prefix, "_ensure_menu", return_value=MENU), \
             patch.object(random_prefix, "_tap_for_transition") as tap, \
             patch.object(random_prefix.secrets, "choice", side_effect=lambda items: items[0]) as draw, \
             patch.object(self.stop, "wait", return_value=False):
            step.action(self.job, self.deadline, self.stop)
            rebuilt = random_prefix.build_random_steps(self.phone, lambda _: None,
                                                       registration=state)[0]
            rebuilt.action(self.job, self.deadline, self.stop)
            self.assertEqual(draw.call_count, 1)
            self.assertEqual(tap.call_count, 2)
            self.assertEqual(tap.call_args_list[0].args[1], tap.call_args_list[1].args[1])
        self.assertEqual(state.prefix_choices[1], "gifting")

        other = RegistrationState()
        with patch.object(random_prefix, "_read_nodes", return_value=MENU), \
             patch.object(random_prefix, "_ensure_menu", return_value=MENU), \
             patch.object(random_prefix, "_tap_for_transition"), \
             patch.object(random_prefix.secrets, "choice", side_effect=lambda items: items[-1]), \
             patch.object(self.stop, "wait", return_value=False):
            random_prefix.build_random_steps(self.phone, lambda _: None,
                                             registration=other)[0].action(
                                                 self.job, self.deadline, self.stop)
        self.assertEqual(other.prefix_choices[1], "fashion and beauty")
        self.assertEqual(state.prefix_choices[1], "gifting")

    def test_missing_target_does_not_pause_prefix(self):
        steps = random_prefix.build_random_steps(self.phone, lambda _: None)
        with patch.object(random_prefix, "_read_nodes", return_value=MENU), \
             patch.object(random_prefix, "_ensure_menu",
                   return_value=[node("Shop by category", 20)]), \
             patch.object(random_prefix, "_tap_for_transition") as tap:
            steps[0].action(self.job, self.deadline, self.stop)
        tap.assert_not_called()

    def test_menu_recovery_failure_does_not_pause_prefix(self):
        step = random_prefix.build_random_steps(self.phone, lambda _: None)[0]
        with patch.object(random_prefix, "_read_nodes", return_value=MENU), \
             patch.object(random_prefix, "_ensure_menu", side_effect=ToolError("slow menu")), \
             patch.object(random_prefix, "_tap_for_transition") as tap:
            step.action(self.job, self.deadline, self.stop)
        tap.assert_not_called()

    def test_unavailable_read_has_bounded_prefix_budget(self):
        step = random_prefix.build_random_steps(self.phone, lambda _: None)[0]
        with patch.object(random_prefix, "_read_nodes", side_effect=ToolError("ADB read failed")) as read, \
             patch.object(random_prefix, "_tap_for_transition") as tap:
            step.action(self.job, self.deadline, self.stop)
        self.assertEqual(read.call_args.args[1].seconds, 15)
        tap.assert_not_called()

    def test_active_random_route_does_not_skip_list_menu_prefix(self):
        window = Window.__new__(Window)
        session = PostMenuSession("batch", 0, "q1")
        steps = random_prefix.build_random_steps(self.phone, lambda _: None)
        context = {"serials": {0: self.phone.serial}, "steps": {0: steps},
                   "factories": {0: random_prefix.build_random_steps},
                   "events": queue.Queue(), "otp": queue.Queue(),
                   "otp_status": queue.Queue()}
        with patch("amazon_android.isolated_reader.phone_reader",
                   return_value=nullcontext()), \
             patch.object(session, "run") as run, \
             patch("amazon_android.desktop.route_list_menu") as old_route:
            window._run_post_menu(session, self.job, steps, self.stop, context)
            self.assertIsNone(run.call_args.kwargs["route"](
                0, self.job, self.deadline, self.stop))
            old_route.assert_not_called()


if __name__ == "__main__":
    unittest.main()
