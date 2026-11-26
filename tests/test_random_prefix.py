from contextlib import nullcontext
import queue
import threading
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from amazon_android import random_prefix
from amazon_android.cloud import CloudPhone
from amazon_android.account_flow import build_common_steps, resume_common_index
from amazon_android.core import ToolError
from amazon_android.desktop import POST_MENU_STEP_FACTORIES, Window
from amazon_android.post_menu import (AttemptDeadline, PostMenuSession, PostMenuStep,
                                      RecoverableStepError, RegistrationState)
from amazon_android.runner import AccountData, RunJob
from amazon_android.settings import AppSettings


class RandomPrefixTests(unittest.TestCase):
    def setUp(self):
        random_prefix._tail_sequences.clear()
        self.native_prefix_nodes = random_prefix._prefix_nodes
        reader = patch.object(random_prefix, "_prefix_nodes", return_value=[])
        reader.start()
        self.addCleanup(reader.stop)
        foreground = patch.object(random_prefix, 'amazon_is_foreground', return_value=True)
        foreground.start()
        self.addCleanup(foreground.stop)
        marketplace = patch.object(random_prefix, 'build_marketplace_steps', return_value=())
        marketplace.start()
        self.addCleanup(marketplace.stop)
        browse_adb = patch('amazon_android.account_flow.cloud_adb',
                           return_value=SimpleNamespace(stdout='Physical size: 420x840'))
        browse_adb.start()
        self.addCleanup(browse_adb.stop)
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
            self.assertEqual([step.name.split(" ", 1)[0] for step in steps[-4:]],
                             ["b12", "b13", "b14", "b15"])

    def test_both_modes_and_all_slots_share_one_continuation_extension_point(self):
        original = random_prefix.build_post_auth_steps
        for mode in ('create', 'login'):
            for index, factory in POST_MENU_STEP_FACTORIES.items():
                with self.subTest(mode=mode, slot=index + 1):
                    state = RegistrationState(flow_mode=mode)
                    phone = CloudPhone(f'127.0.0.1:{5001+index}')
                    calls = []
                    def continuation(active_phone, active_state):
                        self.assertIs(active_phone, phone)
                        self.assertIs(active_state, state)
                        def probe(*_args):
                            calls.append((active_phone.serial, active_state.flow_mode))
                        return original(active_phone, active_state) + (
                            PostMenuStep('b16 test extension only', probe),)
                    with patch.object(random_prefix, 'build_post_auth_steps',
                                      side_effect=continuation), \
                         patch('amazon_android.q7_state_machine.build_post_auth_steps',
                               side_effect=continuation):
                        steps = factory(phone, lambda _: None, registration=state)
                    self.assertEqual([s.name.split(' ', 1)[0] for s in steps
                                      if s.name.split(' ', 1)[0] in
                                      {'b12', 'b13', 'b14', 'b15'}],
                                     ['b12', 'b13', 'b14', 'b15'])
                    self.assertEqual(sum(s.name.startswith('b16 ') for s in steps), 1)
                    steps[-1].action(RunJob(index, 'extension-test', None), self.deadline, self.stop)
                    self.assertEqual(calls, [(phone.serial, mode)])

    def test_q8_to_q12_menu_event_binds_random_prefix_and_common_steps(self):
        window = Window.__new__(Window)
        window.settings = AppSettings()
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
        window.phone_serials = {i: f"127.0.0.1:{5001 + i}" for i in range(7, 12)}
        window.values = [{"profile_name": SimpleNamespace(get=lambda i=i: f"q{i + 1}")}
                         for i in range(12)]
        window.jobs = {i: RunJob(i, "batch", None, account=AccountData(
            f"12025550{i:03d}", f"Example {i}", "Example456!",
            f"https://apifc.net/smsrecord?token=example{i}"))
            for i in range(7, 12)}
        with patch("amazon_android.desktop.threading.Thread", side_effect=lambda **_: Mock()), \
             patch("amazon_android.random_prefix.build_common_steps",
                   wraps=build_common_steps) as common:
            for index in range(7, 12):
                window._start_post_menu(index)
        self.assertEqual(common.call_count, 5)
        self.assertEqual(set(window.post_menu_sessions), set(range(7, 12)))
        for call, index in zip(common.call_args_list, range(7, 12)):
            session = window.post_menu_sessions[index]
            steps = window.post_menu_steps[index]
            self.assertIs(POST_MENU_STEP_FACTORIES[index], random_prefix.build_random_steps)
            self.assertEqual(call.args[0].serial, window.phone_serials[index])
            self.assertIs(call.args[3], session.registration)
            self.assertEqual(session.registration.flow_mode, "create")
            self.assertEqual(session.bound_serial, window.phone_serials[index])
            self.assertEqual([step.name for step in steps[:4]],
                             ["b1 ngẫu nhiên", "b2 ngẫu nhiên", "b3 ngẫu nhiên",
                              "b4 Sign In"])
            tail = next(i for i, step in enumerate(steps)
                        if step.name.startswith('b12 '))
            self.assertEqual([step.name for step in steps[3:tail]],
                             [step.name for step in build_common_steps(
                                 CloudPhone(window.phone_serials[index]), lambda _: None)])
        self.assertEqual(len({id(session.registration)
                              for session in window.post_menu_sessions.values()}), 5)

    def test_tail_opens_menu_then_uses_three_distinct_targets_on_twelve_phones(self):
        menu = [{"text": "Shop by category", "bounds": "[10,10][200,40]"}]
        menu += [{"text": label, "bounds": f"[20,{60 + i * 50}][200,{100 + i * 50}]"}
                 for i, label in enumerate(sorted(random_prefix.MENU_CARD_LABELS))]
        menu.append({"text": "Dogs", "bounds": "[210,100][350,140]"})
        menu.append({"content-desc": "Cart Tab, 3 of 4, 0 items",
                     "bounds": "[220,700][280,740]"})
        menu.append({"content-desc": "Home Tab, 1 of 4",
                     "bounds": "[10,700][70,740]"})
        stop = Mock(is_set=Mock(return_value=False), wait=Mock(return_value=False))
        states = []
        with patch.object(random_prefix, "_read_nodes", return_value=menu), \
             patch.object(random_prefix, "_tap") as tap, \
             patch.object(random_prefix.secrets, "choice",
                          side_effect=lambda items: items[0]) as choose:
            for index in range(12):
                state = RegistrationState(create_pressed=index % 2 == 0,
                                          login_verify_pressed=index % 2 == 1)
                states.append(state)
                phone = CloudPhone(f"127.0.0.1:{5001 + index}")
                job = RunJob(index, "batch", None)
                for step in random_prefix.build_tail_steps(phone, state):
                    step.action(job, AttemptDeadline(None), stop)
                self.assertEqual(state.tail_completed, {12, 13, 14, 15})
                self.assertEqual(len(set(state.tail_choices.values())), 3)
            self.assertEqual(tap.call_count, 36)
            self.assertEqual(len({tuple(state.tail_choices.values()) for state in states}), 12)
            for number in (13, 14, 15):
                self.assertEqual(len({state.tail_choices[number] for state in states}), 12)
            self.assertNotIn("cart", choose.call_args_list[0].args[0])
            self.assertIn("dogs", choose.call_args_list[0].args[0])
            self.assertNotIn("dogs", {state.tail_choices[13] for state in states})
            self.assertNotIn("home tab, 1 of 4", choose.call_args_list[0].args[0])
            for index in range(12):
                serials = {call.args[0].serial
                           for call in tap.call_args_list[index * 3:(index + 1) * 3]}
                self.assertEqual(serials, {f"127.0.0.1:{5001 + index}"})
        self.assertEqual(len({id(state.tail_choices) for state in states}), 12)

    def test_creation_session_runs_b11_confirmation_through_b15_on_all_twelve_slots(self):
        all_choices = []
        for index, factory in POST_MENU_STEP_FACTORIES.items():
            with self.subTest(slot=index + 1):
                state = RegistrationState(flow_mode="create", create_flow_seen=True,
                                          code="222222", prefix_completed={1, 2, 3})
                phone = CloudPhone(f"127.0.0.1:{5001 + index}")
                job = RunJob(index, "creation-through-tail", None, account=AccountData(
                    "12025550123", "Example User", "Example456!",
                    "https://example.com/otp"))
                steps = factory(phone, lambda _: None, registration=state)
                session = PostMenuSession(job.batch_id, index, f"q{index + 1}",
                    next_step=next(i for i, step in enumerate(steps)
                                   if step.name.startswith("b11b ")),
                    registration=state)
                sms = [{"text": "Verify mobile number", "bounds": "[10,10][330,40]"},
                       {"text": "Enter security code", "bounds": "[20,50][330,80]"},
                       {"text": job.account.phone, "bounds": "[20,85][330,115]"},
                       {"text": "222222", "class": "android.widget.EditText",
                        "bounds": "[20,120][330,170]"},
                       {"text": "Create your Amazon account", "class": "android.widget.Button",
                        "bounds": "[20,180][330,230]"}]
                browse = {"content-desc": "Browse menu Tab, 4 of 4",
                          "bounds": "[300,700][390,740]"}
                home = [{"text": "Today's picks", "bounds": "[20,80][330,120]"}, browse]
                menu = [{"text": "Shop by category", "bounds": "[10,10][330,40]"}] + [
                    {"text": label, "bounds": f"[20,{60 + i*35}][330,{90 + i*35}]"}
                    for i, label in enumerate(sorted(random_prefix.MENU_CARD_LABELS))]
                dispatched = []
                menu_open = [False]
                def read(*_args, **_kwargs):
                    if "create" not in dispatched:
                        return sms
                    return menu if menu_open[0] else home
                def tap(_phone, target, *_args):
                    self.assertEqual(_phone.serial, phone.serial)
                    if target is sms[-1]:
                        dispatched.append("create")
                    elif target is browse:
                        dispatched.append("browse")
                        menu_open[0] = True
                    else:
                        dispatched.append("random")
                        menu_open[0] = False
                stop = Mock(is_set=Mock(return_value=False), wait=Mock(return_value=False))
                events = []
                def adb(_phone, *args, **_kwargs):
                    if args[-1] == 'KEYCODE_BACK':
                        menu_open[0] = True
                with patch("amazon_android.account_flow._read_nodes", side_effect=read), \
                     patch("amazon_android.account_flow._tap", side_effect=tap), \
                     patch("amazon_android.q7_state_machine._read_nodes", side_effect=read), \
                     patch.object(random_prefix, "_read_nodes", side_effect=read), \
                     patch.object(random_prefix, 'amazon_is_foreground', return_value=True), \
                     patch.object(random_prefix, '_scroll_up'), \
                     patch.object(random_prefix, 'cloud_adb', side_effect=adb), \
                     patch.object(random_prefix, "_tap", side_effect=tap):
                    tail_end = next(i for i, step in enumerate(steps)
                                    if step.name.startswith('b15 ')) + 1
                    session.run(job, steps[:tail_end],
                                lambda *event: events.append(event), stop)
                self.assertEqual((session.state, session.next_step), ("DONE", tail_end))
                self.assertEqual(state.tail_completed, {12, 13, 14, 15})
                self.assertEqual(dispatched.count("create"), 1)
                self.assertEqual(dispatched.count("browse"), 1)
                self.assertEqual(dispatched.count("random"), 3)
                self.assertFalse(state.login_verify_pressed)
                self.assertEqual(events[-1][2], "post_done")
                all_choices.append(tuple(state.tail_choices.values()))
        self.assertEqual(len(set(all_choices)), 12)

    def test_tail_rereads_slow_menu_and_never_taps_home(self):
        state = RegistrationState(create_pressed=True)
        menu = [{"text": "Shop by category", "bounds": "[10,10][200,40]"},
                {"text": "Pets", "bounds": "[20,60][200,100]"}]
        stop = Mock(is_set=Mock(return_value=False), wait=Mock(return_value=False))
        with patch.object(random_prefix, "_read_nodes", side_effect=[[], [], menu]) as read, \
             patch.object(random_prefix, "_tap") as tap, \
             patch.object(random_prefix.secrets, "choice", side_effect=lambda items: items[0]):
            random_prefix.build_tail_steps(self.phone, state)[0].action(
                self.job, self.deadline, stop)
        self.assertEqual(read.call_count, 3)
        self.assertEqual(tap.call_count, 0)
        self.assertEqual(state.tail_choices, {})
        self.assertEqual(state.tail_completed, {12})

    def test_tail_waits_two_seconds_for_menu_then_one_second_per_visit(self):
        state = RegistrationState(create_pressed=True)
        menu = [{"text": "Shop by category", "bounds": "[10,10][330,40]"}] + [
            {"text": label, "bounds": f"[20,{100+i*60}][330,{150+i*60}]"}
            for i, label in enumerate(("Cats", "Dogs", "Pets"))]
        stop = Mock(is_set=Mock(return_value=False), wait=Mock(return_value=False))
        with patch.object(random_prefix, "_read_nodes", return_value=menu), \
             patch.object(random_prefix, "_tap"), \
             patch.object(random_prefix.secrets, "randbelow", side_effect=[0, 1, 2]), \
             patch.object(random_prefix.secrets, "choice", side_effect=lambda items: items[0]):
            for step in random_prefix.build_tail_steps(self.phone, state):
                step.action(self.job, self.deadline, stop)
        waits = [call.args[0] for call in stop.wait.call_args_list]
        for actual, expected in zip(waits, [2, 0.5, 1.0, 0.5, 1.0, 0.5, 1.0], strict=True):
            self.assertAlmostEqual(actual, expected, delta=0.1)
        self.assertEqual(state.tail_completed, {12, 13, 14, 15})
        self.assertEqual(state.tail_view_until, {})

    def test_create_tail_views_each_random_visit_for_sixteen_seconds(self):
        state = RegistrationState(flow_mode='create', create_pressed=True)
        menu = [{'text': 'Shop by category', 'bounds': '[10,10][330,40]'}] + [
            {'text': label, 'bounds': f'[20,{100+i*60}][330,{150+i*60}]'}
            for i, label in enumerate(('Cats', 'Dogs', 'Pets'))]
        stop = Mock(is_set=Mock(return_value=False), wait=Mock(return_value=False))
        with patch.object(random_prefix, '_read_nodes', return_value=menu), \
             patch.object(random_prefix, '_tap'), \
             patch.object(random_prefix.secrets, 'choice', side_effect=lambda items: items[0]):
            for step in random_prefix.build_tail_steps(self.phone, state):
                step.action(self.job, self.deadline, stop)
        waits = [call.args[0] for call in stop.wait.call_args_list]
        for actual, expected in zip(waits, [2, 8, 16, 8, 16, 8, 16], strict=True):
            self.assertAlmostEqual(actual, expected, delta=0.1)
        self.assertEqual(state.tail_completed, {12, 13, 14, 15})

    def test_tail_resume_finishes_view_without_reopening_menu_or_repeating_tap(self):
        menu = [{"text": "Shop by category", "bounds": "[10,10][330,40]"},
                {"text": "Pets", "bounds": "[20,100][330,160]"}]
        for number, expected_remaining in ((12, 1), (13, 0.75)):
            with self.subTest(step=number):
                state = RegistrationState(login_verify_pressed=True)
                stop = Mock(is_set=Mock(return_value=False),
                            wait=Mock(side_effect=[True, False] if number == 12
                                      else [True, False, False]))
                clock = [100]
                with patch.object(random_prefix, "_read_nodes", return_value=menu) as read, \
                     patch.object(random_prefix, "_tap") as tap, \
                     patch.object(random_prefix.secrets, "randbelow", return_value=2), \
                     patch.object(random_prefix.time, "monotonic", side_effect=lambda: clock[0]):
                    step = random_prefix.build_tail_steps(self.phone, state)[number - 12]
                    with self.assertRaisesRegex(ToolError, "Đã dừng"):
                        step.action(self.job, self.deadline, stop)
                    self.assertNotIn(number, state.tail_completed)
                    self.assertIn(number, state.tail_view_until)
                    clock[0] = 100.25 if number == 13 else 101
                    rebound = random_prefix.build_tail_steps(self.phone, state)[number - 12]
                    rebound.action(self.job, self.deadline, stop)
                self.assertEqual(stop.wait.call_args.args[0], expected_remaining)
                self.assertIn(number, state.tail_completed)
                self.assertEqual(state.tail_view_until, {})
                self.assertEqual(read.call_count, 1 if number == 12 else 2)
                self.assertEqual(tap.call_count, int(number == 13))

    def test_tail_returns_from_a_category_page_through_browse_tab(self):
        state = RegistrationState(create_pressed=True)
        page = [{"text": "Category page", "bounds": "[10,10][200,40]"},
                {"content-desc": "Browse menu Tab, 4 of 4",
                 "bounds": "[300,700][390,740]"},
                {"content-desc": "Home Tab, 1 of 4",
                 "bounds": "[10,700][80,740]"}]
        menu = [{"text": "Shop by category", "bounds": "[10,10][200,40]"},
                {"text": "Gifting", "bounds": "[20,60][200,100]"}]
        stop = Mock(is_set=Mock(return_value=False), wait=Mock(return_value=False))
        with patch.object(random_prefix, "_read_nodes", side_effect=[page, menu]), \
             patch.object(random_prefix, "_tap") as tap, \
             patch.object(random_prefix.secrets, "choice", side_effect=lambda items: items[0]):
            random_prefix.build_tail_steps(self.phone, state)[0].action(
                self.job, self.deadline, stop)
        self.assertEqual(tap.call_count, 1)
        self.assertIs(tap.call_args_list[0].args[1], page[1])

    def test_tail_opens_browse_from_home_after_either_sms_branch(self):
        home = [{"text": "Today's picks", "bounds": "[10,10][200,40]"},
                {"content-desc": "Browse menu Tab, 4 of 4",
                 "bounds": "[300,700][390,740]"},
                {"content-desc": "Home Tab, 1 of 4",
                 "bounds": "[10,700][80,740]"}]
        menu = [{"text": "Shop by category", "bounds": "[10,10][200,40]"},
                {"text": "Pets", "bounds": "[20,60][200,100]"}]
        stop = Mock(is_set=Mock(return_value=False), wait=Mock(return_value=False))
        for marker in ("create_pressed", "login_verify_pressed"):
            with self.subTest(marker=marker):
                state = RegistrationState(**{marker: True})
                with patch.object(random_prefix, "_read_nodes",
                           side_effect=[home, menu]), \
                     patch.object(random_prefix, "_tap") as tap, \
                     patch.object(random_prefix.secrets, "choice",
                           side_effect=lambda items: items[0]):
                    random_prefix.build_tail_steps(self.phone, state)[0].action(
                        self.job, self.deadline, stop)
                self.assertEqual(state.tail_completed, {12})
                self.assertEqual(state.tail_choices, {})
                self.assertEqual(tap.call_count, 1)
                self.assertIs(tap.call_args_list[0].args[1], home[1])

    def test_tail_never_repeats_uncertain_target_on_continue(self):
        state = RegistrationState(create_pressed=True)
        menu = [{"text": "Shop by category", "bounds": "[10,10][200,40]"},
                {"text": "Gifting", "bounds": "[20,60][200,100]"},
                {"text": "Pets", "bounds": "[220,60][400,100]"}]
        stop = Mock(is_set=Mock(return_value=False), wait=Mock(return_value=False))
        action = random_prefix.build_tail_steps(self.phone, state)[1].action
        with patch.object(random_prefix, "_read_nodes", return_value=menu), \
             patch.object(random_prefix, "_tap", side_effect=[ToolError("ADB"), None]) as tap, \
             patch.object(random_prefix.secrets, "choice", side_effect=lambda items: items[0]):
            with self.assertRaises(ToolError):
                action(self.job, self.deadline, stop)
            action(self.job, self.deadline, stop)
            action(self.job, self.deadline, stop)
        self.assertEqual(tap.call_count, 2)
        self.assertEqual(state.tail_attempted, {"gifting", "pets"})
        self.assertEqual(state.tail_choices[13], "pets")

    def test_tail_stops_on_sms_and_resume_never_rewinds_to_create(self):
        state = RegistrationState(create_pressed=True)
        steps = random_prefix.build_random_steps(self.phone, lambda _: None,
                                                 registration=state)
        tail_index = next(i for i, step in enumerate(steps)
                          if step.name.startswith("b12 "))
        with patch.object(random_prefix, "_read_nodes", return_value=[
                {"text": "Verify mobile number", "bounds": "[10,10][200,40]"},
                {"text": "Enter security code", "bounds": "[10,50][200,80]"}]), \
             patch.object(random_prefix, "_tap") as tap:
            with self.assertRaisesRegex(ToolError, "form đăng ký"):
                steps[tail_index].action(self.job, self.deadline, self.stop)
        tap.assert_not_called()
        with patch("amazon_android.account_flow._read_nodes",
                   side_effect=AssertionError("must not re-read before Create")):
            self.assertEqual(resume_common_index(self.phone, steps, tail_index,
                                                 self.deadline, self.stop), tail_index)

    def test_b12_waits_through_stale_sms_and_loading_before_menu(self):
        sms = [{"text": "Verify mobile number"}, {"text": "Enter security code"}]
        menu = [{"text": "Shop by category", "bounds": "[10,10][200,40]"}]
        state = RegistrationState(login_verify_pressed=True)
        stop = Mock(is_set=Mock(return_value=False), wait=Mock(return_value=False))
        with patch.object(random_prefix, "_read_nodes", side_effect=[sms, [], menu]), \
             patch.object(random_prefix, "_tap") as tap:
            random_prefix.build_tail_steps(self.phone, state)[0].action(
                self.job, self.deadline, stop)
        tap.assert_not_called()
        self.assertEqual(state.tail_completed, {12})
        self.assertTrue(all(call.args[0] >= 2 for call in stop.wait.call_args_list))

    def test_tail_ignores_live_navigation_absent_from_browse_menu(self):
        state = RegistrationState(login_verify_pressed=True)
        card = {"text": "Explore local finds", "clickable": "true",
                "class": "android.widget.Button", "bounds": "[20,100][330,160]"}
        page = [{"text": "Shop by category", "bounds": "[10,10][200,40]"},
                card, {"text": "Home", "clickable": "true",
                       "bounds": "[10,700][80,740]"},
                {"text": "Buy now", "clickable": "true",
                 "bounds": "[20,400][330,460]"}]
        self.assertNotIn('explore local finds', random_prefix._tail_candidates(page, state))

    def test_tail_accepts_both_browse_menu_layouts(self):
        state = RegistrationState(login_verify_pressed=True)
        list_menu = [{'text': 'Shop by Category', 'bounds': '[30,100][250,130]'}] + [
            {'text': label, 'bounds': f'[70,{150+i*45}][300,{180+i*45}]'}
            for i, label in enumerate(('Books', 'Electronics', 'Home services',
                                       'See all', "Today's Deals", 'Try Prime'))]
        choices = random_prefix._tail_candidates(list_menu, state)
        self.assertEqual(set(choices), random_prefix.TAIL_LIST_LABELS)
        self.assertEqual(random_prefix.screen(list_menu), 'MENU')

    def test_b14_exhausted_menu_stays_at_step_without_tap(self):
        state = RegistrationState(login_verify_pressed=True,
                                  tail_choices={13: 'books'},
                                  tail_attempted={'books'},
                                  tail_completed={12, 13})
        menu = [{'text': 'Shop by Category', 'bounds': '[30,100][250,130]'}]
        with patch.object(random_prefix, '_read_nodes', return_value=menu), \
             patch.object(random_prefix, '_scroll_up') as scroll, \
             patch.object(random_prefix, '_tap') as tap, \
             patch.object(self.stop, 'wait', return_value=False):
            with self.assertRaisesRegex(ToolError, 'b14: chưa thấy mục mới'):
                random_prefix.build_tail_steps(self.phone, state)[2].action(
                    self.job, self.deadline, self.stop)
        self.assertNotIn(14, state.tail_completed)
        self.assertNotIn(14, state.tail_choices)
        self.assertEqual(scroll.call_count, 2)
        tap.assert_not_called()

    def test_b13_reads_list_menu_image_when_native_has_only_heading(self):
        state = RegistrationState(login_verify_pressed=True)
        native = [{'text': 'Shop by Category', 'bounds': '[30,100][250,130]'}]
        visual = native + [{'text': 'Books', 'bounds': '[55,150][120,180]'},
                           {'text': 'Electronics', 'bounds': '[55,200][180,230]'}]
        with patch.object(random_prefix, '_read_nodes', return_value=native), \
             patch.object(random_prefix, '_read_visual_nodes', return_value=visual), \
             patch.object(random_prefix, '_tap') as tap, \
             patch.object(random_prefix, '_scroll_up') as scroll, \
             patch.object(self.stop, 'wait', return_value=False):
            random_prefix.build_tail_steps(self.phone, state)[1].action(
                self.job, self.deadline, self.stop)
        self.assertIn(13, state.tail_completed)
        self.assertIn(state.tail_choices[13], {'books', 'electronics'})
        tap.assert_called_once()
        scroll.assert_called_once_with(self.phone, [], self.deadline, browsing=True)

    def test_tail_excludes_search_parents_camera_icons_and_permission_actions(self):
        def item(text='', **attrs):
            return dict({'text':text,'bounds':'[20,100][330,160]',
                         'clickable':'true','class':'android.view.ViewGroup'},**attrs)
        controls = [item('Search Amazon.sg'), item('Search'), item('Search by image'), item('Scan it'),
                    item('Allow access'),item('Not now'),
                    item('', **{'content-desc':'Camera button'}),
                    item('', **{'content-desc':'Lens AI'}),
                    item('Enter keywords', **{'resource-id':'app:id/search_box'}),
                    item('Photo', **{'resource-id':'app:id/camera_icon'})]
        valid = [item('Explore local finds'),item('Dogs'),
                 item('', **{'content-desc':'Cart Tab, 3 of 4'})]
        self.assertEqual(set(random_prefix._tail_candidates(controls+valid,RegistrationState())),
                         {'dogs'})

    def test_tail_escapes_search_keyboard_even_if_menu_cards_remain_in_hierarchy(self):
        browse = {'content-desc':'Browse menu Tab, 4 of 4','bounds':'[300,700][390,740]'}
        menu = [{'text':'Shop by category','bounds':'[10,10][330,40]'},browse]
        search = menu + [{'text':'Search Amazon.sg','class':'android.widget.EditText',
                          'focused':'true','bounds':'[40,50][350,95]'}]
        search_no_keyboard = [{'text':'Search with photo','bounds':'[20,100][220,140]'}]
        page = [browse]
        events = []
        def adb(phone,*args,**_kwargs):
            self.assertIs(phone,self.phone)
            self.assertEqual(args,('shell','input','keyevent','KEYCODE_BACK'))
            events.append('back')
        def tap(_phone,target,*_args):
            self.assertIs(target,browse); events.append('browse')
        with patch.object(random_prefix,'_read_nodes',side_effect=[search,search_no_keyboard,page,menu]), \
             patch.object(random_prefix,'cloud_adb',side_effect=adb), \
             patch.object(random_prefix,'_tap',side_effect=tap), \
             patch.object(self.stop,'wait',return_value=False):
            self.assertIs(random_prefix._tail_menu(self.phone,self.deadline,self.stop),menu)
        self.assertEqual(events,['back','back','browse'])

    def test_tail_declines_camera_access_then_exits_lens_and_reopens_browse(self):
        decline = {'text':'Not now','bounds':'[20,810][200,850]'}
        lens_permission = [{'text':'Allow camera access to scan products','bounds':'[20,620][380,660]'},
                           decline,{'text':'Allow access','bounds':'[215,810][390,850]'}]
        lens = [{'text':'Scan a barcode to reorder or read reviews','bounds':'[60,200][330,240]'}]
        browse = {'content-desc':'Browse menu Tab, 4 of 4','bounds':'[300,700][390,740]'}
        menu = [{'text':'Shop by category','bounds':'[10,10][330,40]'}]
        events = []
        with patch.object(random_prefix,'_read_nodes',side_effect=[lens_permission,lens,[browse],menu]), \
             patch.object(random_prefix,'_tap',side_effect=lambda _p,n,*_:events.append(
                 'decline' if n is decline else 'browse')), \
             patch.object(random_prefix,'cloud_adb',side_effect=lambda _p,*a,**_k:events.append(a[-1])), \
             patch.object(self.stop,'wait',return_value=False):
            self.assertIs(random_prefix._tail_menu(self.phone,self.deadline,self.stop),menu)
        self.assertEqual(events,['decline','KEYCODE_BACK','browse'])

    def test_tail_read_failure_is_bounded_and_never_sends_camera_or_menu_input(self):
        from amazon_android.account_flow import _UiReadIncomplete
        with patch('amazon_android.account_flow._read_nodes_once',side_effect=_UiReadIncomplete('bad UI')) as read, \
             patch.object(random_prefix,'cloud_adb') as adb, \
             patch.object(self.stop,'wait',return_value=False):
            with self.assertRaises(_UiReadIncomplete):
                random_prefix._tail_menu(self.phone,self.deadline,self.stop)
        self.assertEqual(read.call_count,3)
        adb.assert_not_called()

    def test_tail_back_timeout_reads_result_before_sending_any_second_input(self):
        search = [{'text':'Search with photo','bounds':'[20,100][330,150]'}]
        menu = [{'text':'Shop by category','bounds':'[10,10][330,40]'}]
        with patch.object(random_prefix,'_read_nodes',side_effect=[search,menu]) as read, \
             patch.object(random_prefix,'cloud_adb',side_effect=ToolError('ADB response timeout')) as adb, \
             patch.object(random_prefix,'_tap') as tap, \
             patch.object(self.stop,'wait',return_value=False):
            self.assertIs(random_prefix._tail_menu(self.phone,self.deadline,self.stop),menu)
        self.assertEqual(read.call_count,2)
        adb.assert_called_once()
        tap.assert_not_called()

    def test_b15_timeout_clears_wait_clock_so_continue_can_retry(self):
        state = RegistrationState(login_verify_pressed=True,
                                  tail_menu_wait_started={15: 100.0},
                                  tail_choices={13: 'dogs', 14: 'cats'},
                                  tail_completed={12, 13, 14})
        step = random_prefix.build_tail_steps(self.phone, state)[3]
        menu = [{'text': 'Shop by category', 'bounds': '[10,10][330,40]'},
                {'text': 'Pets', 'clickable': 'true',
                 'bounds': '[20,100][330,160]'}]
        with patch.object(random_prefix.time, 'monotonic', return_value=161.0), \
             patch.object(random_prefix, '_tail_menu') as read, \
             patch.object(random_prefix, '_read_nodes', return_value=menu), \
             patch.object(random_prefix, '_tap') as tap, \
             patch.object(self.stop, 'wait', return_value=False):
            with self.assertRaisesRegex(ToolError, 'sau 60 giây'):
                step.action(self.job, self.deadline, self.stop)
            self.assertNotIn(15, state.tail_menu_wait_started)
            read.assert_not_called()
            read.return_value = menu
            step.action(self.job, self.deadline, self.stop)
        tap.assert_called_once()
        self.assertIn(15, state.tail_completed)

    def test_b15_does_not_use_account_navigation_when_browse_layout_changes(self):
        state = RegistrationState(login_verify_pressed=True,
                                  tail_choices={13: 'dogs', 14: 'cats'},
                                  tail_completed={12, 13, 14})
        page = [{'text': 'Your Orders', 'bounds': '[20,150][300,190]'},
                {'text': 'Orders', 'bounds': '[10,110][95,145]'},
                {'text': 'Account', 'bounds': '[190,110][280,145]'},
                {'text': 'Buy Again', 'clickable': 'true',
                 'bounds': '[100,110][185,145]'}]
        self.assertEqual(random_prefix._tail_candidates(page, state), {})

    def test_tail_does_not_click_background_menu_when_a_popup_has_focus(self):
        menu = [{'text':'Shop by category','bounds':'[10,10][330,40]'}]
        with patch.object(random_prefix,'_read_nodes',return_value=menu), \
             patch.object(random_prefix,'amazon_is_foreground',side_effect=[False,True]), \
             patch.object(random_prefix,'cloud_adb') as adb, \
             patch.object(random_prefix,'_tap') as tap, \
             patch.object(self.stop,'wait',return_value=False):
            self.assertIs(random_prefix._tail_menu(self.phone,self.deadline,self.stop),menu)
        adb.assert_called_once_with(self.phone,'shell','input','keyevent','KEYCODE_BACK',timeout=4)
        tap.assert_not_called()

    def test_new_batch_avoids_each_phones_previous_step_without_losing_cross_phone_uniqueness(self):
        menu = [{'text':'Shop by category','bounds':'[10,10][330,40]'}] + [
            {'text':label,'clickable':'true','class':'android.widget.Button',
             'bounds':f'[20,{100+i*40}][330,{130+i*40}]'}
            for i,label in enumerate(sorted(random_prefix.TAIL_MENU_LABELS))]
        batches = []
        with patch.object(random_prefix,'_read_nodes',return_value=menu), \
             patch.object(random_prefix,'_tap'), \
             patch.object(random_prefix.secrets,'choice',side_effect=lambda items:items[0]), \
             patch.object(self.stop,'wait',return_value=False):
            for batch in ('old-random-batch','new-random-batch'):
                states = []
                for i in range(12):
                    state = RegistrationState(login_verify_pressed=True)
                    phone = CloudPhone(f'127.0.0.1:{5001+i}')
                    for step in random_prefix.build_tail_steps(phone,state):
                        step.action(RunJob(i,batch,None),self.deadline,self.stop)
                    states.append(state)
                    self.assertEqual(state.tail_completed,{12,13,14,15})
                    self.assertEqual(len(set(state.tail_choices.values())),3)
                batches.append(states)
                for step in (13,14,15):
                    self.assertEqual(len({s.tail_choices[step] for s in states}),12)
        for old,new in zip(*batches):
            for step in (13,14,15):
                self.assertNotEqual(old.tail_choices[step],new.tail_choices[step])

    def test_twelve_concurrent_final_choices_cannot_duplicate_sequences(self):
        from concurrent.futures import ThreadPoolExecutor
        barrier = threading.Barrier(12)
        def choose(index):
            state = RegistrationState(tail_choices={13: "pets", 14: "dogs"})
            barrier.wait(timeout=5)
            return random_prefix._choose_tail_target(
                RunJob(index, "concurrent-tail", None), 15,
                [f"navigation {i}" for i in range(12)], state)
        with ThreadPoolExecutor(max_workers=12) as pool:
            choices = list(pool.map(choose, range(12)))
        self.assertEqual(len(set(choices)), 12)

    def test_each_random_step_reserves_different_labels_for_twelve_concurrent_phones(self):
        from concurrent.futures import ThreadPoolExecutor
        for number in (13, 14, 15):
            barrier = threading.Barrier(12)
            states = [RegistrationState(tail_choices={n: f'previous {n} phone {i}'
                      for n in (13, 14, 15) if n < number}) for i in range(12)]
            def choose(index):
                barrier.wait(timeout=5)
                return random_prefix._choose_tail_target(
                    RunJob(index, f'parallel-step-{number}', None), number,
                    [f'live card {i}' for i in range(12)], states[index])
            with ThreadPoolExecutor(max_workers=12) as pool:
                choices = list(pool.map(choose, range(12)))
            self.assertEqual(len(set(choices)), 12)

    def test_used_step_target_scrolls_to_new_item_instead_of_matching_other_phone(self):
        random_prefix._choose_tail_target(RunJob(0, 'batch', None), 13,
                                          ['pets'], RegistrationState())
        state = RegistrationState(create_pressed=True)
        menu = [{'text': 'Shop by category', 'bounds': '[10,10][330,40]'},
                {'text': 'Pets', 'bounds': '[20,100][330,160]'}]
        fresh = menu + [{'text': 'Cats', 'bounds': '[20,180][330,240]'}]
        with patch.object(random_prefix, '_read_nodes', side_effect=[menu, fresh, fresh, fresh]), \
             patch.object(random_prefix, '_scroll_up') as scroll, \
             patch.object(random_prefix, '_tap') as tap, \
             patch.object(self.stop, 'wait', return_value=False):
            random_prefix.build_tail_steps(self.phone, state)[1].action(
                RunJob(1, 'batch', None), self.deadline, self.stop)
        self.assertEqual(scroll.call_count, 2)  # Reveal another choice, then browse it.
        self.assertTrue(scroll.call_args.kwargs['browsing'])
        tap.assert_called_once_with(self.phone, fresh[-1], self.deadline)
        self.assertEqual(state.tail_choices, {13: 'cats'})

    def test_no_distinct_live_target_uses_other_phone_choice_after_two_searches(self):
        random_prefix._choose_tail_target(RunJob(0, 'batch', None), 13,
                                          ['pets'], RegistrationState())
        state = RegistrationState(create_pressed=True)
        menu = [{'text': 'Shop by category', 'bounds': '[10,10][330,40]'},
                {'text': 'Pets', 'bounds': '[20,100][330,160]'}]
        with patch.object(random_prefix, '_read_nodes', return_value=menu), \
             patch.object(random_prefix, '_scroll_up') as scroll, \
             patch.object(random_prefix, '_tap') as tap, \
             patch.object(self.stop, 'wait', return_value=False):
            random_prefix.build_tail_steps(self.phone, state)[1].action(
                RunJob(1, 'batch', None), self.deadline, self.stop)
        self.assertEqual(scroll.call_count, 3)  # Two searches and the visit swipe.
        self.assertTrue(scroll.call_args.kwargs['browsing'])
        tap.assert_called_once()
        self.assertEqual(state.tail_choices, {13: 'pets'})

    def test_rebinding_and_new_batch_keep_step_reservations_scoped_correctly(self):
        restored = RegistrationState(tail_choices={13: 'pets', 14: 'cats'},
                                     tail_attempted={'pets', 'cats'})
        random_prefix._choose_tail_target(RunJob(0, 'old', None), 15,
                                          ['dogs'], restored)
        other = RegistrationState()
        self.assertEqual(random_prefix._choose_tail_target(
            RunJob(1, 'old', None), 13, ['pets', 'gifting'], other), 'gifting')
        self.assertEqual(random_prefix._choose_tail_target(
            RunJob(1, 'new', None), 13, ['pets'], other), 'pets')

    def test_b12_uses_live_dimensions_when_signed_in_home_hides_browse_label(self):
        state = RegistrationState(login_verify_pressed=True)
        home = [{"content-desc": "Home Tab, 1 of 4", "selected": "true",
                 "bounds": "[10,700][80,740]"}]
        menu = [{"text": "Shop by category", "bounds": "[10,10][200,40]"}]
        stop = Mock(is_set=Mock(return_value=False), wait=Mock(return_value=False))
        with patch.object(random_prefix, "_read_nodes", side_effect=[home, menu]), \
             patch.object(random_prefix, "cloud_adb", return_value=SimpleNamespace(
                 stdout=f"mCurrentFocus=Window{{ {random_prefix.AMAZON_PACKAGE} }}")), \
             patch.object(random_prefix, "_size", return_value=(420, 840)), \
             patch.object(random_prefix, "_menu") as open_menu:
            random_prefix.build_tail_steps(self.phone, state)[0].action(
                self.job, self.deadline, stop)
        open_menu.assert_called_once_with(self.phone, 420, 840, self.deadline)
        self.assertEqual(state.tail_completed, {12})

    def test_login_tail_resume_rechecks_sms_verify_before_b12(self):
        state = RegistrationState(login_jump_seen=True, login_verify_pressed=True,
                                  login_verify_attempts=1)
        steps = random_prefix.build_random_steps(self.phone, lambda _: None,
                                                 registration=state)
        final_index = next(i for i, step in enumerate(steps)
                           if step.name.startswith("b11b "))
        sms = [{"text": "Verify mobile number"},
               {"text": "Enter security code"}]
        with patch("amazon_android.account_flow._read_nodes", return_value=sms):
            self.assertEqual(resume_common_index(self.phone, steps, final_index + 1,
                                                 self.deadline, self.stop, state),
                             final_index)
        self.assertEqual(state.login_verify_attempts, 1)

    def test_login_b12_resume_checks_phone_row_before_retrying_verify(self):
        state = RegistrationState(flow_mode='login', login_jump_seen=True,
                                  login_verify_pressed=True,
                                  login_verify_attempts=1)
        steps = random_prefix.build_random_steps(self.phone, lambda _: None,
                                                 registration=state)
        b11 = next(i for i, step in enumerate(steps)
                   if step.name.startswith('b11b '))
        job = RunJob(0, 'batch', None,
                     account=AccountData('12025550123', 'Example Person',
                                         'ExamplePass1!', 'https://example.test/otp'))
        sms = [{'text': 'Verify mobile number'},
               {'text': 'Enter security code'},
               {'text': '2025550123'}]
        with patch('amazon_android.account_flow._read_nodes', return_value=sms):
            self.assertEqual(resume_common_index(self.phone, steps, b11 + 1,
                                                 self.deadline, self.stop,
                                                 state, job), b11)
        sms[-1]['text'] = '2025550999'
        with patch('amazon_android.account_flow._read_nodes', return_value=sms):
            with self.assertRaisesRegex(ToolError, 'SĐT'):
                resume_common_index(self.phone, steps, b11 + 1,
                                    self.deadline, self.stop, state, job)

    def test_login_resume_after_b12_keeps_saved_step_without_sms_scan(self):
        state = RegistrationState(flow_mode='login', login_jump_seen=True,
                                  login_verify_pressed=True,
                                  tail_completed={12})
        steps = random_prefix.build_random_steps(self.phone, lambda _: None,
                                                 registration=state)
        b13 = next(i for i, step in enumerate(steps)
                   if step.name.startswith('b13 '))
        with patch('amazon_android.account_flow._read_nodes',
                   side_effect=AssertionError('should not scan SMS')):
            self.assertEqual(resume_common_index(self.phone, steps, b13,
                                                 self.deadline, self.stop,
                                                 state), b13)

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

    def test_child_pages_still_view_all_three_steps_before_b4(self):
        state = RegistrationState()
        menu = [{"text": "Shop by category", "bounds": "[10,10][200,40]"}] + [
            {"text": label, "bounds": f"[20,{100+i*70}][330,{150+i*70}]"}
            for i, label in enumerate(("Cats", "Dogs", "Pets"))]
        page = [{"text": "Child page", "bounds": "[20,100][330,150]"}]
        called = []
        with patch.object(random_prefix, "build_common_steps", return_value=(
                PostMenuStep("b4 Sign In", lambda *_: called.append("b4")),)):
            steps = random_prefix.build_random_steps(self.phone, lambda _: None,
                                                       registration=state)
        with patch.object(random_prefix, "_prefix_nodes",
                          side_effect=[menu, page, menu, page, menu, menu]), \
             patch.object(random_prefix, "cloud_adb", return_value=SimpleNamespace(
                 stdout="Physical size: 420x840")) as adb, \
             patch.object(random_prefix.secrets, "choice", side_effect=lambda items: items[0]), \
             patch.object(random_prefix.secrets, "randbelow", return_value=2), \
             patch.object(self.stop, "wait", return_value=False) as wait:
            for i, step in enumerate(steps[:3]):
                step.action(self.job, self.deadline, self.stop)
                if i < 2:
                    with self.assertRaises(RecoverableStepError):
                        steps[3].action(self.job, self.deadline, self.stop)
            self.assertEqual(called, [])
            steps[3].action(self.job, self.deadline, self.stop)
        self.assertEqual(state.prefix_completed, {1, 2, 3})
        self.assertEqual(state.prefix_attempted, {"cats", "dogs", "pets"})
        self.assertEqual(sum(call.args == (5,) for call in wait.call_args_list), 3)
        self.assertEqual(called, ["b4"])
        taps = [call.args for call in adb.call_args_list
                if call.args[1:4] == ("shell", "input", "tap")]
        self.assertEqual(len(taps), 6)  # Three child visits, menu before b2/b3/b4.

    def test_prefix_read_failure_is_one_bounded_request_without_ocr_retry_loop(self):
        reader = Mock()
        reader.call.side_effect = ToolError('native hierarchy stalled')
        with patch('amazon_android.isolated_reader.current', return_value=reader), \
             patch.object(random_prefix, '_read_nodes', side_effect=AssertionError('OCR retry')), \
             patch.object(random_prefix, '_read_nodes_once') as direct:
            self.assertEqual(self.native_prefix_nodes(self.phone, self.deadline, self.stop), [])
        reader.call.assert_called_once_with('read', 6, self.stop)
        direct.assert_not_called()

    def test_prefix_keeps_the_single_read_ui_and_ocr_fallback_for_live_child_targets(self):
        menu = [{'text': 'Shop by category'}, {'text': 'Dogs'}]
        with patch('amazon_android.isolated_reader.current', return_value=None), \
             patch.object(random_prefix, '_read_nodes', side_effect=AssertionError('retry loop')), \
             patch.object(random_prefix, '_read_nodes_once', return_value=menu) as read:
            self.assertIs(self.native_prefix_nodes(self.phone, self.deadline, self.stop), menu)
        read.assert_called_once()
        self.assertEqual(read.call_args.args[1].seconds, 6)

    def test_prefix_read_cannot_swallow_another_phones_reader_or_stop(self):
        with patch('amazon_android.isolated_reader.current',
                   side_effect=ToolError('Serial không khớp')):
            with self.assertRaisesRegex(ToolError, 'Serial'):
                self.native_prefix_nodes(self.phone, self.deadline, self.stop)
        self.stop.set()
        with patch('amazon_android.isolated_reader.current') as current:
            with self.assertRaisesRegex(ToolError, 'Đã dừng'):
                self.native_prefix_nodes(self.phone, self.deadline, self.stop)
        current.assert_not_called()

    def test_prefix_returns_from_foreign_app_without_using_its_stale_browse_control(self):
        foreign = [{'content-desc': 'Browse menu Tab', 'bounds': '[1,1][20,20]'}]
        menu = [{'text': 'Shop by category', 'bounds': '[10,10][330,40]'}]
        with patch.object(random_prefix, 'amazon_is_foreground', side_effect=[False, True]), \
             patch.object(random_prefix, '_prefix_nodes', return_value=menu) as read, \
             patch.object(random_prefix, '_tap') as tap, \
             patch.object(random_prefix, '_menu') as browse, \
             patch.object(random_prefix, 'cloud_adb') as adb, \
             patch.object(self.stop, 'wait', return_value=False):
            result = random_prefix._restore_prefix_menu(
                self.phone, 420, 840, self.deadline, self.stop, foreign)
        self.assertIs(result, menu)
        adb.assert_called_once_with(self.phone, 'shell', 'input', 'keyevent',
                                    'KEYCODE_BACK', timeout=4)
        browse.assert_called_once_with(self.phone, 420, 840, self.deadline)
        read.assert_called_once()
        tap.assert_not_called()

    def test_prefix_uses_one_back_fallback_when_browse_does_not_change_child_page(self):
        page = [{'text': 'Unfamiliar child page', 'bounds': '[20,100][330,160]'}]
        menu = [{'text': 'Shop by category', 'bounds': '[10,10][330,40]'}]
        with patch.object(random_prefix, '_prefix_nodes', side_effect=[page, menu]) as read, \
             patch.object(random_prefix, '_menu') as browse, \
             patch.object(random_prefix, 'cloud_adb') as adb, \
             patch.object(self.stop, 'wait', return_value=False):
            result = random_prefix._restore_prefix_menu(
                self.phone, 420, 840, self.deadline, self.stop, page)
        self.assertIs(result, menu)
        self.assertEqual(read.call_count, 2)
        self.assertEqual(browse.call_count, 2)
        adb.assert_called_once_with(self.phone, 'shell', 'input', 'keyevent',
                                    'KEYCODE_BACK', timeout=4)

    def test_unrecoverable_external_page_pauses_only_this_phone_without_retry_loop(self):
        state = RegistrationState(prefix_completed={1}, prefix_choices={1: (0.16, 0.20)})
        steps = random_prefix.build_random_steps(self.phone, lambda _: None, registration=state)
        session = PostMenuSession('batch', 0, 'q1', next_step=1, registration=state)
        events = []
        with patch.object(random_prefix, 'amazon_is_foreground', return_value=False) as focus, \
             patch.object(random_prefix, '_size', return_value=(420, 840)), \
             patch.object(random_prefix, 'cloud_adb') as adb, \
             patch.object(random_prefix, '_menu') as browse, \
             patch.object(self.stop, 'wait', return_value=False):
            session.run(self.job, steps, lambda *args: events.append(args), self.stop)
        self.assertEqual((session.state, session.next_step), ('PAUSED', 1))
        self.assertEqual(state.prefix_completed, {1})
        self.assertEqual(focus.call_count, 2)
        self.assertEqual(adb.call_count, 1)
        browse.assert_not_called()
        self.assertEqual(events[-1][2], 'post_paused')
        other_state = RegistrationState()
        other = CloudPhone('127.0.0.1:5002')
        with patch.object(random_prefix, '_size', return_value=(420, 840)), \
             patch.object(random_prefix, 'cloud_adb') as adb, \
             patch.object(self.stop, 'wait', return_value=False):
            random_prefix.build_random_steps(other, lambda _: None, registration=other_state)[0].action(
                RunJob(1, 'batch', None), self.deadline, self.stop)
        self.assertEqual(other_state.prefix_completed, {1})
        self.assertEqual(state.prefix_completed, {1})
        self.assertTrue(all(call.args[0] is other for call in adb.call_args_list))

    def test_prefix_recovery_preserves_auth_form_and_stop_without_tapping(self):
        sms = [{'text': 'Verify mobile number'}, {'text': 'Enter security code'}]
        with patch.object(random_prefix, 'cloud_adb') as adb, \
             patch.object(random_prefix, '_menu') as browse:
            with self.assertRaises(random_prefix._PrefixRecoveryStop):
                random_prefix._restore_prefix_menu(
                    self.phone, 420, 840, self.deadline, self.stop, sms)
            self.stop.set()
            with self.assertRaisesRegex(ToolError, 'Đã dừng'):
                random_prefix._restore_prefix_menu(
                    self.phone, 420, 840, self.deadline, self.stop, [])
        adb.assert_not_called()
        browse.assert_not_called()

    def test_tail_reopens_menu_and_ignores_product_card_on_child_page(self):
        state = RegistrationState(login_verify_pressed=True)
        menu = [{"text": "Shop by category", "bounds": "[10,10][200,40]"},
                {"text": "Dogs", "bounds": "[20,100][330,160]"},
                {"text": "Cats", "bounds": "[20,180][330,240]"}]
        browse = {"content-desc": "Browse menu Tab, 4 of 4", "bounds": "[300,700][390,740]"}
        page = [{"text": "Product card", "clickable": "true",
                 "bounds": "[20,100][330,200]"}, browse]
        steps = random_prefix.build_tail_steps(self.phone, state)
        with patch.object(random_prefix, "_read_nodes", side_effect=[menu, page, menu, menu, menu]), \
             patch.object(random_prefix, "_tap") as tap, \
             patch.object(random_prefix, '_scroll_up'), \
             patch.object(random_prefix, 'cloud_adb'), \
             patch.object(random_prefix.secrets, "choice", side_effect=lambda items: items[0]), \
             patch.object(self.stop, "wait", return_value=False):
            steps[1].action(self.job, self.deadline, self.stop)
            steps[2].action(self.job, self.deadline, self.stop)
        self.assertEqual(state.tail_choices, {13: "cats", 14: "dogs"})
        self.assertEqual(tap.call_count, 2)
        self.assertIs(tap.call_args_list[1].args[1], menu[1])

    def test_tail_child_page_scrolls_then_backs_before_next_menu_choice(self):
        state = RegistrationState(login_verify_pressed=True)
        menu = [{'text': 'Shop by category', 'bounds': '[10,10][330,40]'},
                {'text': 'Cats', 'bounds': '[20,100][330,160]'},
                {'text': 'Dogs', 'bounds': '[20,180][330,240]'}]
        page = [{'text': 'Product card', 'clickable': 'true',
                 'bounds': '[20,100][330,200]'}]
        stage = ['menu']; actions = []
        def tap(_phone, target, _deadline):
            actions.append(target['text']); stage[0] = 'page'
        def adb(_phone, *args, **_kwargs):
            self.assertEqual(args, ('shell', 'input', 'keyevent', 'KEYCODE_BACK'))
            actions.append('back'); stage[0] = 'menu'
        with patch.object(random_prefix, '_read_nodes',
                          side_effect=lambda *_a, **_k: menu if stage[0] == 'menu' else page), \
             patch.object(random_prefix, '_tap', side_effect=tap), \
             patch.object(random_prefix, '_scroll_up',
                          side_effect=lambda *_a, **_k: actions.append('scroll')), \
             patch.object(random_prefix, 'cloud_adb', side_effect=adb), \
             patch.object(random_prefix.secrets, 'choice', side_effect=lambda items: items[0]), \
             patch.object(self.stop, 'wait', return_value=False):
            steps = random_prefix.build_tail_steps(self.phone, state)
            steps[1].action(self.job, self.deadline, self.stop)
            self.assertEqual(actions, ['Cats', 'scroll', 'back'])
            self.assertIn(13, state.tail_completed)
            steps[2].action(self.job, self.deadline, self.stop)
        self.assertEqual(actions, ['Cats', 'scroll', 'back', 'Dogs', 'scroll', 'back'])
        self.assertEqual(state.tail_choices, {13: 'cats', 14: 'dogs'})

    def test_tail_child_read_failure_still_scrolls_and_backs(self):
        state = RegistrationState(login_verify_pressed=True, tail_viewed={13},
                                  tail_choices={13: 'cats'})
        menu = [{'text': 'Shop by category', 'bounds': '[10,10][330,40]'}]
        actions = []
        with patch.object(random_prefix, '_read_nodes',
                          side_effect=[ToolError('slow page'), menu]), \
             patch.object(random_prefix, '_scroll_up',
                          side_effect=lambda *_a, **_k: actions.append('scroll')), \
             patch.object(random_prefix, 'cloud_adb',
                          side_effect=lambda *_a, **_k: actions.append('back')), \
             patch.object(self.stop, 'wait', return_value=False):
            random_prefix.build_tail_steps(self.phone, state)[1].action(
                self.job, self.deadline, self.stop)
        self.assertEqual(actions, ['scroll', 'back'])
        self.assertIn(13, state.tail_completed)

    def test_tail_resume_after_page_scroll_does_not_tap_or_scroll_again(self):
        state = RegistrationState(login_verify_pressed=True,
                                  tail_choices={13: 'cats'}, tail_attempted={'cats'},
                                  tail_viewed={13}, tail_page_scrolled={13})
        page = [{'text': 'Child page', 'bounds': '[20,100][330,160]'}]
        menu = [{'text': 'Shop by category', 'bounds': '[10,10][330,40]'}]
        stage = ['page']
        with patch.object(random_prefix, '_read_nodes',
                          side_effect=lambda *_a, **_k: page if stage[0] == 'page' else menu), \
             patch.object(random_prefix, '_scroll_up') as scroll, \
             patch.object(random_prefix, '_tap') as tap, \
             patch.object(random_prefix, 'cloud_adb',
                          side_effect=lambda *_a, **_k: stage.__setitem__(0, 'menu')) as adb:
            random_prefix.build_tail_steps(self.phone, state)[1].action(
                self.job, self.deadline, self.stop)
        self.assertIn(13, state.tail_completed)
        scroll.assert_not_called()
        tap.assert_not_called()
        adb.assert_called_once()

    def test_prefix_opens_menu_then_views_each_random_tap_for_three_to_five_seconds(self):
        state = RegistrationState()
        steps = random_prefix.build_random_steps(self.phone, lambda _: None,
                                                  registration=state)
        def adb(_phone, *args, **_kwargs):
            return SimpleNamespace(stdout="Physical size: 420x840")
        with patch.object(random_prefix, "cloud_adb", side_effect=adb), \
             patch.object(random_prefix.secrets, "randbelow", return_value=2), \
             patch.object(self.stop, "wait", return_value=False) as waited:
            steps[0].action(self.job, self.deadline, self.stop)
            steps[1].action(self.job, self.deadline, self.stop)
        delays = [call.args[0] for call in waited.call_args_list]
        self.assertEqual(delays, [2.0, 5, 0.6, 2.0, 5])
        self.assertEqual(state.prefix_completed, {1, 2})

    def test_prefix_waits_after_tap_then_scrolls_forward_once(self):
        clock = [100.0]
        actions = []
        state = RegistrationState()

        def adb(_phone, *args, **_kwargs):
            if args[:3] in {('shell', 'input', 'tap'), ('shell', 'input', 'swipe')}:
                actions.append((args[2], args))
            return SimpleNamespace(stdout='Physical size: 420x840')

        def wait(seconds):
            actions.append(('wait', seconds))
            clock[0] += seconds
            return False

        with patch.object(random_prefix.time, 'monotonic', side_effect=lambda: clock[0]), \
             patch.object(random_prefix, 'cloud_adb', side_effect=adb), \
             patch.object(random_prefix.secrets, 'randbelow', return_value=0), \
             patch.object(self.stop, 'wait', side_effect=wait):
            random_prefix.build_random_steps(self.phone, lambda _: None,
                                             registration=state)[0].action(
                                                 self.job, self.deadline, self.stop)
        self.assertEqual([action[0] for action in actions],
                         ['tap', 'wait', 'swipe', 'wait'])
        self.assertEqual([action[1] for action in actions if action[0] == 'wait'],
                         [2.0, 1.0])
        swipe = next(action[1] for action in actions if action[0] == 'swipe')
        self.assertGreater(int(swipe[4]), int(swipe[6]))
        self.assertEqual(state.prefix_completed, {1})

    def test_tail_waits_after_tap_then_scrolls_forward_once(self):
        menu = [{'text': 'Shop by category', 'bounds': '[10,10][330,40]'},
                {'text': 'Pets', 'bounds': '[20,100][330,160]'}]
        for mode, duration in (('create', 16.0), ('login', 1.0)):
            with self.subTest(mode=mode):
                clock = [100.0]
                actions = []
                state = RegistrationState(flow_mode=mode,
                                          create_pressed=mode == 'create',
                                          login_verify_pressed=mode == 'login')

                def wait(seconds):
                    actions.append(('wait', seconds))
                    clock[0] += seconds
                    return False

                def adb(_phone, *args, **_kwargs):
                    if args[:3] == ('shell', 'input', 'swipe'):
                        actions.append(('swipe', args))
                    return SimpleNamespace(stdout='Physical size: 420x840')

                with patch.object(random_prefix.time, 'monotonic', side_effect=lambda: clock[0]), \
                     patch.object(random_prefix, '_read_nodes', return_value=menu), \
                     patch.object(random_prefix, '_tap',
                                  side_effect=lambda *_args: actions.append(('tap', None))), \
                     patch('amazon_android.account_flow.cloud_adb', side_effect=adb), \
                     patch.object(self.stop, 'wait', side_effect=wait):
                    random_prefix.build_tail_steps(self.phone, state)[1].action(
                        self.job, self.deadline, self.stop)
                self.assertEqual([action[0] for action in actions],
                                 ['tap', 'wait', 'swipe', 'wait'])
                self.assertEqual([action[1] for action in actions if action[0] == 'wait'],
                                 [duration / 2, duration / 2])
                swipe = next(action[1] for action in actions if action[0] == 'swipe')
                self.assertGreater(int(swipe[4]), int(swipe[6]))
                self.assertEqual(state.tail_completed, {13})

    def test_tail_stop_after_swipe_resumes_remaining_view_before_back(self):
        clock = [100.0]
        stage = ['menu']
        actions = []
        state = RegistrationState(flow_mode='create', create_pressed=True)
        menu = [{'text': 'Shop by category', 'bounds': '[10,10][330,40]'},
                {'text': 'Pets', 'bounds': '[20,100][330,160]'}]
        page = [{'text': 'Pet products', 'bounds': '[20,100][330,160]'}]
        waits = [False, True, False]

        def wait(seconds):
            actions.append(('wait', seconds))
            stopped = waits.pop(0)
            if not stopped:
                clock[0] += seconds
            return stopped

        def adb(_phone, *args, **_kwargs):
            if args[:3] == ('shell', 'input', 'keyevent'):
                actions.append(('back', None))
                stage[0] = 'menu'
            return SimpleNamespace(stdout='Physical size: 420x840')

        def tap(*_args):
            actions.append(('tap', None))
            stage[0] = 'page'

        with patch.object(random_prefix.time, 'monotonic', side_effect=lambda: clock[0]), \
             patch.object(random_prefix, '_read_nodes',
                          side_effect=lambda *_a, **_k: menu if stage[0] == 'menu' else page), \
             patch.object(random_prefix, '_tap', side_effect=tap), \
             patch.object(random_prefix, '_scroll_up',
                          side_effect=lambda *_a, **_k: actions.append(('swipe', None))), \
             patch.object(random_prefix, 'cloud_adb', side_effect=adb), \
             patch.object(self.stop, 'wait', side_effect=wait):
            step = random_prefix.build_tail_steps(self.phone, state)[1]
            with self.assertRaisesRegex(ToolError, 'Đã dừng'):
                step.action(self.job, self.deadline, self.stop)
            self.assertEqual(state.tail_page_scrolled, {13})
            self.assertNotIn(13, state.tail_completed)
            step.action(self.job, self.deadline, self.stop)
        self.assertEqual([action[0] for action in actions],
                         ['tap', 'wait', 'swipe', 'wait', 'wait', 'back'])
        self.assertEqual(clock[0], 116.0)
        self.assertEqual(state.tail_completed, {13})

    def test_stop_during_prefix_view_resumes_same_tap_without_repeating(self):
        state = RegistrationState()
        action = random_prefix.build_random_steps(self.phone, lambda _: None,
                                                   registration=state)[0].action
        commands = []
        def adb(_phone, *args, **_kwargs):
            commands.append(args)
            return SimpleNamespace(stdout="Physical size: 420x840")
        with patch.object(random_prefix, "cloud_adb", side_effect=adb), \
             patch.object(random_prefix.secrets, "randbelow", return_value=0), \
             patch.object(self.stop, "wait", side_effect=[True, False, False]) as waited:
            with self.assertRaisesRegex(ToolError, "Đã dừng"):
                action(self.job, self.deadline, self.stop)
            self.assertEqual(state.prefix_completed, set())
            self.assertIn(1, state.prefix_view_until)
            action(self.job, self.deadline, self.stop)
            action(self.job, self.deadline, self.stop)
        self.assertEqual(state.prefix_completed, {1})
        self.assertEqual(state.prefix_view_until, {})
        self.assertEqual(len([command for command in commands
                              if command[:3] == ("shell", "input", "tap")]), 1)
        self.assertEqual(len([command for command in commands
                              if command[:3] == ("shell", "input", "swipe")]), 1)
        self.assertEqual(state.prefix_view_scrolled, {1})
        self.assertEqual(next(command for command in commands
                              if command[:3] == ("shell", "input", "swipe"))[-1], '450')
        self.assertEqual(waited.call_count, 3)

    def test_b1_b2_wait_two_seconds_after_tap_before_view_scroll(self):
        state = RegistrationState()
        steps = random_prefix.build_random_steps(self.phone, lambda _: None,
                                                  registration=state)
        clock = [100.0]
        actions = []

        def adb(_phone, *args, **_kwargs):
            if args[:3] in {('shell', 'input', 'tap'), ('shell', 'input', 'swipe')}:
                actions.append((args[2], clock[0]))
            return SimpleNamespace(stdout='Physical size: 420x840')

        def wait(seconds):
            clock[0] += seconds
            return False

        with patch.object(random_prefix.time, 'monotonic', side_effect=lambda: clock[0]), \
             patch.object(random_prefix, 'cloud_adb', side_effect=adb), \
             patch.object(random_prefix, '_restore_prefix_menu', return_value=[]), \
             patch.object(random_prefix.secrets, 'choice', side_effect=lambda items: items[0]), \
             patch.object(random_prefix.secrets, 'randbelow', return_value=0), \
             patch.object(self.stop, 'wait', side_effect=wait):
            steps[0].action(self.job, self.deadline, self.stop)
            steps[1].action(self.job, self.deadline, self.stop)

        taps = [at for kind, at in actions if kind == 'tap']
        swipes = [at for kind, at in actions if kind == 'swipe']
        self.assertEqual(len(taps), 2)
        self.assertEqual(len(swipes), 2)
        self.assertEqual([swipe - tap for tap, swipe in zip(taps, swipes)], [2.0, 2.0])

    def test_b3_views_without_any_scroll(self):
        state = RegistrationState(prefix_completed={1, 2})
        step = random_prefix.build_random_steps(self.phone, lambda _: None,
                                                 registration=state)[2]
        commands = []

        def adb(_phone, *args, **_kwargs):
            commands.append(args)
            return SimpleNamespace(stdout='Physical size: 420x840')

        with patch.object(random_prefix, 'cloud_adb', side_effect=adb), \
             patch.object(random_prefix, '_restore_prefix_menu', return_value=[]), \
             patch.object(random_prefix.secrets, 'randbelow', return_value=0), \
             patch.object(self.stop, 'wait', return_value=False):
            step.action(self.job, self.deadline, self.stop)
        self.assertIn(3, state.prefix_completed)
        self.assertNotIn(3, state.prefix_scroll_at)
        self.assertNotIn(3, state.prefix_view_scrolled)
        self.assertFalse(any(command[:3] == ('shell', 'input', 'swipe')
                             for command in commands))

    def test_b3_retry_after_failed_taps_does_not_scroll(self):
        state = RegistrationState(prefix_completed={1, 2})
        step = random_prefix.build_random_steps(self.phone, lambda _: None,
                                                 registration=state)[2]
        commands = []

        def adb(_phone, *args, **_kwargs):
            commands.append(args)
            if args[:3] == ('shell', 'input', 'tap') and sum(
                    cmd[:3] == ('shell', 'input', 'tap') for cmd in commands) <= 3:
                raise ToolError('tap failed')
            return SimpleNamespace(stdout='Physical size: 420x840')

        with patch.object(random_prefix, 'cloud_adb', side_effect=adb), \
             patch.object(random_prefix, '_restore_prefix_menu', return_value=[]), \
             patch.object(random_prefix.secrets, 'choice', side_effect=lambda items: items[0]), \
             patch.object(random_prefix.secrets, 'randbelow', return_value=0), \
             patch.object(self.stop, 'wait', return_value=False):
            step.action(self.job, self.deadline, self.stop)
        self.assertIn(3, state.prefix_completed)
        self.assertFalse(any(command[:3] == ('shell', 'input', 'swipe')
                             for command in commands))

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
