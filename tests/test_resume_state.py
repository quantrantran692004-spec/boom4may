from worker_helpers import on_worker
from contextlib import nullcontext
import queue
import sys
import threading
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from amazon_android.cloud import CloudPhone
from amazon_android.desktop import Window
from amazon_android.post_menu import AttemptDeadline, PostMenuSession, PostMenuStep, RegistrationState
from amazon_android.q1_flow import build_q1_steps
from amazon_android.q2_flow import build_q2_steps
from amazon_android.runner import AccountData, RunJob
from amazon_android.settings import AppSettings
from amazon_android.random_prefix import build_random_steps
from amazon_android.account_flow import resume_common_index


class ResumeRegistrationStateTests(unittest.TestCase):
    def setUp(self):
        marketplace = patch('amazon_android.random_prefix.build_marketplace_steps', return_value=())
        marketplace.start()
        self.addCleanup(marketplace.stop)
        addresses = patch('amazon_android.random_prefix.build_create_address_steps', return_value=())
        addresses.start()
        self.addCleanup(addresses.stop)
        address_detail = patch('amazon_android.random_prefix.build_create_address_detail_steps',
                               return_value=())
        address_detail.start()
        self.addCleanup(address_detail.stop)
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
        self.window.post_menu_resume_after_stop = set()
        self.window.menu_opened_at = {}
        self.window.values = [{"profile_name": SimpleNamespace(get=lambda: "q1")}]
        self.window.settings = AppSettings(account_flow_mode="login")

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
        self.assertEqual(session.registration.flow_mode, "login")
        self.assertEqual(seen, [(session.bound_serial, session.registration)])
        self.assertIs(worker.call_args.kwargs["args"][2], steps)
        worker.return_value.start.assert_called_once()

    def test_queued_resume_clears_phone_stop_only_when_worker_restarts(self):
        session = PostMenuSession("batch", 0, "q1", state="PAUSED")
        self.window.post_menu_sessions[0] = session
        self.window.post_menu_step_factories = {0: Mock(return_value=(PostMenuStep("b4", Mock()),))}
        event = threading.Event(); event.set()
        self.window.phone_stop_after_step[0] = event
        self.window.post_menu_resume_after_stop.add(0)
        with patch("amazon_android.desktop.threading.Thread") as worker:
            self.window._start_post_menu(0)
        self.assertFalse(event.is_set())
        self.assertEqual(self.window.post_menu_resume_after_stop, set())
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
        session.registration.tail_choices[12] = "pets"
        session.registration.tail_attempted.add("pets")
        session.registration.tail_completed.add(12)
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
        self.assertEqual(session.registration.tail_choices, {12: "pets"})
        self.assertEqual(session.registration.tail_attempted, {"pets"})
        self.assertEqual(session.registration.tail_completed, {12})

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

    def test_manual_otp_repair_continues_with_confirmation_and_tail_for_both_modes(self):
        for mode in ('create', 'login'):
            with self.subTest(mode=mode):
                state = RegistrationState(flow_mode=mode, create_flow_seen=mode == 'create',
                    prefix_completed={1, 2, 3}, code='111111', sms_requested_at=123.0,
                    reload_completed={32, 33, 34, 36, 37, 38, 39} if mode == 'create' else set())
                steps = build_random_steps(CloudPhone('127.0.0.1:5001'), lambda _: None,
                                            registration=state)
                session = PostMenuSession('batch', 0, 'q1', state='PAUSED',
                    bound_serial='127.0.0.1:5001', registration=state,
                    next_step=next(i for i, step in enumerate(steps) if step.name.startswith('b5 ')))
                button = {'text': 'Create your Amazon account' if mode == 'create' else 'Verify mobile number',
                          'bounds': '[20,180][330,230]', 'class': 'android.widget.Button'}
                sms = [{'text': 'Verify mobile number', 'bounds': '[10,10][330,40]'},
                       {'text': 'Enter security code', 'bounds': '[20,50][330,80]'},
                       {'text': self.job.account.phone, 'bounds': '[20,85][330,115]'},
                       {'text': '222222', 'bounds': '[20,120][330,170]',
                        'class': 'android.widget.EditText'}, button]
                browse = {'content-desc': 'Browse menu Tab, 4 of 4', 'bounds': '[300,700][390,740]'}
                home = [browse]
                menu = [{'text': 'Shop by category', 'bounds': '[10,10][330,40]'}] + [
                    {'text': label, 'bounds': f'[20,{100+i*60}][330,{150+i*60}]'}
                    for i, label in enumerate(('Cats', 'Dogs', 'Pets'))]
                pressed = []; menu_open = [False]
                def read(*_args, **_kwargs):
                    return sms if not pressed else menu if menu_open[0] else home
                def confirm(_phone, target, *_args):
                    self.assertIs(target, button)
                    pressed.append(mode)
                def navigate(_phone, target, *_args):
                    menu_open[0] = target is browse
                def back(_phone, *args, **_kwargs):
                    if args[-1] == 'KEYCODE_BACK':
                        menu_open[0] = True
                self.window.post_menu_sessions[0] = session
                self.window.post_menu_step_factories = {0: build_random_steps}
                self.window.post_menu_steps[0] = steps
                with patch('amazon_android.isolated_reader.phone_reader', return_value=nullcontext()), \
                     patch('amazon_android.account_flow._read_nodes', side_effect=read), \
                     patch('amazon_android.account_flow._tap', side_effect=confirm), \
                     patch('amazon_android.account_flow._type_field') as type_field, \
                     patch('amazon_android.random_prefix._read_nodes', side_effect=read), \
                     patch('amazon_android.random_prefix.amazon_is_foreground', return_value=True), \
                     patch('amazon_android.random_prefix._scroll_up'), \
                     patch('amazon_android.random_prefix.cloud_adb', side_effect=back), \
                     patch('amazon_android.random_prefix._tap', side_effect=navigate), \
                     patch('amazon_android.post_menu._CombinedStop.wait', return_value=False):
                    on_worker(self.window._run_post_menu, session, self.job, steps, threading.Event())
                self.assertEqual(session.state, 'DONE', session.last_error)
                self.assertEqual(pressed, [mode])
                self.assertEqual(state.code, '222222')
                self.assertEqual(state.tail_completed, {12, 13, 14, 15})
                type_field.assert_not_called()

    def test_manual_sms_completion_on_home_resumes_b12_without_confirming_again(self):
        state = RegistrationState(flow_mode='create', create_flow_seen=True,
                                  sms_requested_at=123.0, code='222222')
        phone = CloudPhone('127.0.0.1:5001')
        steps = build_random_steps(phone, lambda _: None, registration=state)
        current = next(i for i, step in enumerate(steps) if step.name == 'b11 nhập OTP')
        home = [{'content-desc': 'Browse menu Tab, 4 of 4', 'bounds': '[300,700][390,740]'}]
        with patch('amazon_android.account_flow._read_nodes', return_value=home):
            target = resume_common_index(phone, steps, current,
                AttemptDeadline(None),
                threading.Event(), state, self.job)
        self.assertTrue(steps[target].name.startswith('b12 '))
        self.assertTrue(state.manual_sms_completed)
        self.assertFalse(state.create_pressed)
        with patch('amazon_android.random_prefix._read_nodes', return_value=[
                {'text': 'Shop by category', 'bounds': '[10,10][330,40]'}]), \
             patch('amazon_android.random_prefix.amazon_is_foreground', return_value=True):
            steps[target].action(self.job, AttemptDeadline(None),
                Mock(is_set=Mock(return_value=False), wait=Mock(return_value=False)))
        self.assertEqual(state.tail_completed, {12})

    def test_create_resume_at_sms_restores_missing_create_marker(self):
        state = RegistrationState(flow_mode='create', prefix_completed={1, 2, 3})
        phone = CloudPhone('127.0.0.1:5001')
        steps = build_random_steps(phone, lambda _: None, registration=state)
        current = next(i for i, step in enumerate(steps) if step.name.startswith('b10 '))
        sms = [{'text': label, 'bounds': f'[20,{i*45}][330,{i*45+40}]'}
               for i, label in enumerate(('Verify mobile number', 'Enter security code',
                                          self.job.account.phone,
                                          'Create your Amazon account'))]
        with patch('amazon_android.account_flow._read_nodes', return_value=sms):
            target = resume_common_index(phone, steps, current,
                AttemptDeadline(None), threading.Event(), state, self.job)
        self.assertEqual(steps[target].name, 'b10 Send code by SMS')
        self.assertTrue(state.create_flow_seen)
        self.assertFalse(state.login_jump_seen)

    def test_manual_resume_rejects_different_phone_row_before_advancing(self):
        from amazon_android.core import ToolError
        from amazon_android.post_menu import AttemptDeadline
        state = RegistrationState(flow_mode='login', code='111111')
        phone = CloudPhone('127.0.0.1:5001')
        steps = build_random_steps(phone, lambda _: None, registration=state)
        current = next(i for i, step in enumerate(steps) if step.name.startswith('b5 '))
        sms = [{'text': 'Verify mobile number'}, {'text': 'Enter security code'},
               {'text': '12025550999'}]
        with patch('amazon_android.account_flow._read_nodes', return_value=sms):
            with self.assertRaisesRegex(ToolError, 'SĐT'):
                resume_common_index(phone, steps, current, AttemptDeadline(None),
                                    threading.Event(), state, self.job)
        self.assertEqual(state.code, '111111')

    def test_forward_resume_does_not_skip_random_prefix_views(self):
        session = PostMenuSession('batch', 0, 'q1', next_step=0, state='PAUSED')
        called = []
        steps = tuple(PostMenuStep(f'b{i} ngẫu nhiên', lambda *_: called.append('tap'))
                      for i in (1, 2, 3)) + (PostMenuStep('b4 Sign In', lambda *_: None),)
        session.run(self.job, steps, lambda *_: None, threading.Event(),
                    reconcile=lambda *_: (3, steps))
        self.assertEqual(session.state, 'PAUSED')
        self.assertEqual(session.next_step, 0)
        self.assertEqual(called, [])

    def test_paused_b37_resumes_same_step_without_registration_read(self):
        phone = CloudPhone('127.0.0.1:5001')
        state = RegistrationState(flow_mode='create',
                                  reload_completed={32, 33, 34, 36})
        called = []
        steps = (PostMenuStep('b11b hoàn tất xác minh SMS', lambda *_: None),
                 PostMenuStep('b37 thêm phương thức thanh toán',
                              lambda *_: called.append('b37')))
        session = PostMenuSession('batch', 0, 'q1', next_step=1,
                                  state='PAUSED', registration=state)
        with patch('amazon_android.account_flow._read_nodes',
                   side_effect=AssertionError('registration reread')):
            session.run(self.job, steps, lambda *_: None, threading.Event(),
                        reconcile=lambda current, job, deadline, stop:
                            (resume_common_index(phone, steps, current, deadline,
                                                 stop, state, job), steps))
        self.assertEqual(called, ['b37'])
        self.assertEqual(session.state, 'DONE')
        self.assertEqual(state.reload_completed, {32, 33, 34, 36})

    def test_manually_selected_us_resumes_continue_instead_of_old_country_error(self):
        state = RegistrationState(flow_mode='create')
        phone = CloudPhone('127.0.0.1:5001')
        steps = build_random_steps(phone, lambda _: None, registration=state)
        current = next(i for i, step in enumerate(steps) if step.name.startswith('b6 '))
        form = [{'text': 'Sign in or create account'},
                {'text': 'Enter mobile number or email'}, {'text': 'Continue'}, {'text': 'US +1'},
                {'text': self.job.account.phone, 'class': 'android.widget.EditText',
                 'bounds': '[20,100][330,160]'}]
        with patch('amazon_android.account_flow._read_nodes', return_value=form):
            target = resume_common_index(phone, steps, current, AttemptDeadline(None),
                                        threading.Event(), state, self.job)
        self.assertEqual(steps[target].name, 'b7 Continue')


if __name__ == "__main__":
    unittest.main()
