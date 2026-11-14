from worker_helpers import on_worker
import queue
import threading
import unittest
from unittest.mock import patch

from amazon_android import profile_navigation as nav
from amazon_android.q1_flow import build_q1_steps
from amazon_android.q2_flow import build_q2_steps
from amazon_android.q3_flow import build_q3_steps
from amazon_android.q4_flow import build_q4_steps
from amazon_android.desktop import Window, POST_MENU_STEP_FACTORIES
from amazon_android.random_prefix import build_random_steps
from amazon_android.q7_state_machine import build_q7_pilot_steps
from amazon_android.account_flow import build_common_steps
from amazon_android.cloud import CloudPhone
from amazon_android.post_menu import AttemptDeadline, PostMenuSession, RegistrationState
from amazon_android.runner import AccountData, RunJob


MENU = [{"text": "Shop by category", "bounds": "[0,40][300,80]"}]


class Q3Q4FlowTests(unittest.TestCase):
    def setUp(self):
        self.phone = CloudPhone('127.0.0.1:5003')
        self.job = RunJob(2, 'batch', None)
        self.stop = threading.Event()
        self.deadline = AttemptDeadline(180)

    def test_q3_order_and_q4_order_both_reuse_all_common_steps(self):
        common = [step.name for step in build_common_steps(self.phone, lambda _: None)]
        for factory, prefix in ((build_q3_steps, ['b1 Groceries and Drinks', 'b2 Home and DIY', 'b3 Books and Reading']),
                                (build_q4_steps, ['b1 Giỏ hàng', 'b2 Pets', 'b3 Home and DIY'])):
            steps = factory(self.phone, lambda _: None)
            self.assertEqual([s.name for s in steps[:3]], prefix)
            self.assertEqual([s.name for s in steps[3:]], common)
        self.assertEqual(set(POST_MENU_STEP_FACTORIES), set(range(12)))
        self.assertIs(POST_MENU_STEP_FACTORIES[6], build_q7_pilot_steps)
        self.assertTrue(all(factory is build_random_steps
                            for index, factory in POST_MENU_STEP_FACTORIES.items()
                            if index != 6))

    def test_common_b4_to_b11_can_bind_twelve_distinct_serials_and_states(self):
        states = [RegistrationState() for _ in range(12)]
        phones = [CloudPhone(f'127.0.0.1:{5001 + slot}') for slot in range(12)]
        steps = [build_common_steps(phone, lambda _: None, registration=state)
                 for phone, state in zip(phones, states)]
        self.assertTrue(all([step.name for step in group] ==
                            [step.name for step in steps[0]] for group in steps))
        self.assertEqual(len({phone.serial for phone in phones}), 12)
        states[0].create_pressed = True
        self.assertTrue(all(not state.create_pressed for state in states[1:]))

    def test_q1_to_q4_use_identical_shared_action_implementations(self):
        factories = (build_q1_steps, build_q2_steps, build_q3_steps, build_q4_steps)
        groups = [factory(CloudPhone(f'127.0.0.1:{5001 + slot}'), lambda _: None)
                  for slot, factory in enumerate(factories)]
        baseline = [(step.name, step.action.__code__) for step in groups[0][3:]]
        self.assertEqual(baseline[0][0], 'b4 Sign In')
        for group in groups[1:]:
            self.assertEqual([(step.name, step.action.__code__) for step in group[3:]],
                             baseline)

    def test_q3_category_steps_find_live_labels_in_user_order(self):
        target = {"text": "category", "bounds": "[20,100][200,150]"}
        steps = build_q3_steps(self.phone, lambda _: None)
        with patch.object(nav, '_read_nodes', return_value=MENU), \
             patch.object(nav, '_ensure_menu'), \
             patch.object(nav, '_find_scrolling', return_value=target) as find, \
             patch.object(nav, '_tap_for_transition') as tap, \
             patch.object(self.stop, 'wait', return_value=False):
            for step in steps[:3]:
                step.action(self.job, self.deadline, self.stop)
        self.assertEqual([c.args[1] for c in find.call_args_list],
                         ['Groceries and Drinks', 'Home and DIY', 'Books and Reading'])
        self.assertEqual(tap.call_count, 3)

    def test_q4_cart_taps_accessibility_tab_and_confirms_cart_before_returning(self):
        tab = {"content-desc": "Cart Tab, 3 of 4, 0 items", "bounds": "[180,650][240,700]"}
        cart = [{"text": "Your Amazon Cart is empty"}]
        action = build_q4_steps(self.phone, lambda _: None)[0].action
        with patch.object(nav, '_read_nodes', side_effect=[MENU + [tab], cart]), \
             patch.object(nav, '_tap_for_transition') as tap:
            action(self.job, self.deadline, self.stop)
        tap.assert_called_once_with(self.phone, tab, self.deadline)

    def test_q4_already_on_cart_does_not_click_twice(self):
        action = build_q4_steps(self.phone, lambda _: None)[0].action
        with patch.object(nav, '_read_nodes', return_value=[{'text':'Your Amazon Cart is empty'}]), \
             patch.object(nav, '_tap_for_transition') as tap:
            action(self.job, self.deadline, self.stop)
        tap.assert_not_called()

    def test_q4_pets_and_home_diy_return_to_menu_before_finding_card(self):
        steps = build_q4_steps(self.phone, lambda _: None)
        calls = []
        with patch.object(nav, '_read_nodes', return_value=[{'text':'Your Amazon Cart is empty'}]), \
             patch.object(nav, '_ensure_menu', side_effect=lambda *_: calls.append('menu')), \
             patch.object(nav, '_find_scrolling', side_effect=lambda _p, label, *_: (calls.append(label) or {'bounds':'[10,10][100,50]'})), \
             patch.object(nav, '_tap_for_transition'), patch.object(self.stop, 'wait', return_value=False):
            for step in steps[1:3]:
                step.action(self.job, self.deadline, self.stop)
        self.assertEqual(calls, ['menu','Pets','menu','Home and DIY'])

    def test_q3_q4_attach_verify_their_own_profile_and_serial(self):
        for slot in (2, 3):
            w = Window.__new__(Window); w.attach_events = queue.Queue()
            name = f'q{slot+1}'; serial = f'127.0.0.1:{5001+slot}'
            with patch('amazon_android.desktop.profile_status', return_value={'state':'Running','device_id':name+'-device'}) as status, \
                 patch('amazon_android.desktop.open_adb_shell', return_value={'serial':serial}), \
                 patch('amazon_android.desktop.verify_menu_open') as check:
                on_worker(w._probe_existing_profile, slot, None)
            status.assert_called_once_with(name)
            self.assertEqual(check.call_args.args, (CloudPhone(serial), name))
            self.assertEqual(w.attach_events.get_nowait(), ('ready', None, serial))

    def test_four_real_common_flows_wait_for_otp_concurrently_without_crossing_data(self):
        barrier = threading.Barrier(4, timeout=5)
        results = {}; typed = {}; sessions = []; threads = []
        accounts = {}; snapshots = {}; url_codes = {}
        factories = (build_q1_steps, build_q2_steps, build_q3_steps, build_q4_steps)
        for i in range(4):
            serial = f'127.0.0.1:{5001+i}'
            accounts[serial] = AccountData(f'1202555012{i}',f'Example {i}','Example456!',f'https://apifc.net/smsrecord?token=fixture{i}')
            snapshots[serial] = [{'text':'Verify mobile number'},{'text':'Enter security code'},
                {'text':accounts[serial].phone}, {'text':'','class':'android.widget.EditText','bounds':'[10,100][300,140]'}]
            url_codes[accounts[serial].otp_url] = str(111111*(i+1))

        def read_otp(url, *_args, **_kwargs):
            barrier.wait()
            return url_codes[url]

        def type_field(phone, _label, value, *_args, **_kwargs):
            typed[phone.serial] = value

        with patch('amazon_android.account_flow._read_nodes', side_effect=lambda phone,*_:snapshots[phone.serial]), \
             patch('amazon_android.account_flow.wait_for_new_otp', side_effect=read_otp), \
             patch('amazon_android.account_flow._type_field', side_effect=type_field):
            for i,factory in enumerate(factories):
                phone = CloudPhone(f'127.0.0.1:{5001+i}')
                session = PostMenuSession('batch',i,f'q{i+1}'); sessions.append(session)
                steps = factory(phone, lambda code,slot=i:results.__setitem__(slot,code), registration=session.registration)
                selected = tuple(s for s in steps if s.name in {'b10 Send code by SMS','b11 nhập OTP'})
                thread = threading.Thread(target=session.run, args=(RunJob(i,'batch',None,account=accounts[phone.serial]), selected,lambda *_:None,threading.Event()))
                threads.append(thread); thread.start()
            for thread in threads:
                thread.join(timeout=8)
        self.assertTrue(all(not t.is_alive() for t in threads))
        self.assertEqual([s.state for s in sessions], ['DONE']*4)
        self.assertEqual(len({id(s.registration) for s in sessions}), 4)
        for i in range(4):
            self.assertEqual(results[i], str(111111*(i+1)))
            self.assertEqual(typed[f'127.0.0.1:{5001+i}'],results[i])


if __name__ == '__main__':
    unittest.main()
