import threading
import time
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from amazon_android.cloud import CloudPhone
from amazon_android.create_address_flow import build_create_address_steps
from amazon_android.desktop import POST_MENU_STEP_FACTORIES
from amazon_android.post_menu import AttemptDeadline, RegistrationState
from amazon_android.random_prefix import build_post_auth_steps


def node(label, y=100):
    return {'text': label, 'bounds': f'[20,{y}][380,{y+40}]'}


class CreateAddressFlowTests(unittest.TestCase):
    def setUp(self):
        self.phone = CloudPhone('127.0.0.1:5001')
        self.stop = threading.Event()
        self.state = RegistrationState(flow_mode='create',
                                       marketplace_completed=set(range(16, 23)))
        self.deadline = AttemptDeadline(190)

    def test_all_twelve_factories_append_only_to_create(self):
        for index, factory in POST_MENU_STEP_FACTORIES.items():
            phone = CloudPhone(f'127.0.0.1:{5001+index}')
            for mode in ('create', 'login'):
                with self.subTest(slot=index+1, mode=mode):
                    state = RegistrationState(flow_mode=mode)
                    names = [s.name for s in factory(
                        phone, lambda _: None, registration=state)]
                    suffix = names[-16:] if mode == 'create' else names[-3:]
                    self.assertEqual([n.split()[0] for n in suffix],
                                     [f'b{i}' for i in range(23, 35)] +
                                     ['b36', 'b37', 'b38', 'b39'] if mode == 'create'
                                     else ['b20', 'b21', 'b22'])

    def test_login_followup_options_append_only_the_selected_steps(self):
        for index, factory in POST_MENU_STEP_FACTORIES.items():
            phone = CloudPhone(f'127.0.0.1:{5001+index}')
            for choice, expected in (
                    ('address_and_card', [*range(23, 35), 36, 37, 38, 39]),
                    ('card_only', [32, 33, 34, 36, 37, 38, 39])):
                with self.subTest(slot=index+1, choice=choice):
                    state = RegistrationState(flow_mode='login', login_followup=choice)
                    names = [step.name for step in factory(
                        phone, lambda _: None, registration=state)]
                    self.assertEqual([name.split()[0] for name in names[-len(expected):]],
                                     [f'b{number}' for number in expected])

    def test_b23_waits_three_seconds_then_taps_only_visible_account_word(self):
        action = build_create_address_steps(self.phone, self.state)[0].action
        target = dict(node('Account', 145), vision='true')
        with patch('amazon_android.create_address_flow._read_text_region',
                   return_value=[node('Orders'), target]) as text_read, \
             patch('amazon_android.create_address_flow._tap_for_transition') as tap, \
             patch.object(self.stop, 'wait', return_value=False) as wait:
            action(None, self.deadline, self.stop)
        self.assertAlmostEqual(wait.call_args_list[0].args[0], 3, delta=.2)
        text_read.assert_called_once()
        tap.assert_called_once()
        self.assertIs(tap.call_args.args[1], target)
        self.assertIn(23, self.state.create_address_completed)

    def test_b23_stop_continue_keeps_remaining_wait_without_completing_step(self):
        action = build_create_address_steps(self.phone, self.state)[0].action
        with patch.object(self.stop, 'wait', return_value=True):
            with self.assertRaisesRegex(Exception, 'Đã dừng'):
                action(None, self.deadline, self.stop)
        ready_at = self.state.create_address_wait_until[23]
        self.assertNotIn(23, self.state.create_address_completed)
        with patch('amazon_android.create_address_flow._read_text_region',
                   return_value=[dict(node('Account', 145), vision='true')]), \
             patch('amazon_android.create_address_flow._tap_for_transition') as tap, \
             patch.object(self.stop, 'wait', return_value=False) as wait:
            action(None, self.deadline, self.stop)
        self.assertAlmostEqual(wait.call_args_list[0].args[0],
                               max(0, ready_at-time.monotonic()), delta=.2)
        tap.assert_called_once()
        self.assertIn(23, self.state.create_address_completed)

    def test_b24_skips_scroll_when_addresses_visible(self):
        self.state.create_address_completed.add(23)
        action = build_create_address_steps(self.phone, self.state)[1].action
        with patch('amazon_android.create_address_flow._read_text_region',
                   return_value=[node('Your Addresses', 450)]), \
             patch('amazon_android.create_address_flow.cloud_adb') as adb, \
             patch.object(self.stop, 'wait', return_value=False):
            action(None, self.deadline, self.stop)
        adb.assert_not_called()
        self.assertIn(24, self.state.create_address_completed)

    def test_b25_taps_visible_address_text_without_native_read(self):
        self.state.create_address_completed.update({23, 24})
        action = build_create_address_steps(self.phone, self.state)[2].action
        target = dict(node('Your Addresses', 450), vision='true')
        with patch('amazon_android.create_address_flow._read_text_region',
                   return_value=[target]) as text_read, \
             patch('amazon_android.create_address_flow._tap_for_transition') as tap, \
             patch.object(self.stop, 'wait', return_value=False):
            action(None, self.deadline, self.stop)
        text_read.assert_called_once()
        tap.assert_called_once()
        self.assertIn(25, self.state.create_address_completed)

    def test_b24_scrolls_until_addresses_appear(self):
        self.state.create_address_completed.add(23)
        action = build_create_address_steps(self.phone, self.state)[1].action
        screens = [[node('Orders'), node('Account settings', 700)],
                   [node('Your Addresses', 480)]]
        with patch('amazon_android.create_address_flow._read_text_region', side_effect=screens), \
             patch('amazon_android.create_address_flow.cloud_adb',
                   return_value=SimpleNamespace(stdout='Physical size: 420x910')) as adb, \
             patch.object(self.stop, 'wait', return_value=False):
            action(None, self.deadline, self.stop)
        self.assertEqual(sum(call.args[1:4] == ('shell', 'input', 'swipe')
                             for call in adb.call_args_list), 1)
        self.assertIn(24, self.state.create_address_completed)

    def test_b24_empty_frame_scrolls_then_reads_target(self):
        self.state.create_address_completed.add(23)
        action = build_create_address_steps(self.phone, self.state)[1].action
        with patch('amazon_android.create_address_flow._read_text_region',
                   side_effect=[[], [node('Your Addresses', 480)]]) as read, \
             patch('amazon_android.create_address_flow.cloud_adb',
                   return_value=SimpleNamespace(stdout='Physical size: 420x910')) as adb, \
             patch.object(self.stop, 'wait', return_value=False):
            action(None, self.deadline, self.stop)
        self.assertEqual(read.call_count, 2)
        self.assertEqual(sum(call.args[1:4] == ('shell', 'input', 'swipe')
                             for call in adb.call_args_list), 1)
        self.assertIn(24, self.state.create_address_completed)

    def test_b24_first_account_frame_scrolls_when_focus_probe_is_transient(self):
        self.state.create_address_completed.add(23)
        action = build_create_address_steps(self.phone, self.state)[1].action
        first = [dict(node('Your Orders'), package='com.amazon.mShop.android.shopping'),
                 dict(node('Account Tab', 830), package='com.amazon.mShop.android.shopping',
                      **{'content-desc': 'Your Account Tab, 2 of 4'})]
        found = [dict(node('Your Addresses', 480),
                      package='com.amazon.mShop.android.shopping')]
        with patch('amazon_android.create_address_flow._read_text_region',
                   side_effect=[first, found]), \
             patch('amazon_android.create_address_flow._tap_for_transition') as tap, \
             patch('amazon_android.create_address_flow.cloud_adb',
                   return_value=SimpleNamespace(stdout='Physical size: 420x910')) as adb, \
             patch.object(self.stop, 'wait', return_value=False):
            action(None, self.deadline, self.stop)
        tap.assert_not_called()
        self.assertEqual(sum(c.args[1:4] == ('shell', 'input', 'swipe')
                             for c in adb.call_args_list), 1)
        self.assertIn(24, self.state.create_address_completed)

    def test_b24_scrolls_then_backs_out_of_inserted_ad_and_finds_text(self):
        self.state.create_address_completed.add(23)
        action = build_create_address_steps(self.phone, self.state)[1].action
        stage = ['ad']; actions = []
        def read(*_args):
            return {'ad': [node('Special offer')],
                    'ad_scrolled': [node('Shop now')],
                    'account': [node('Orders')],
                    'addresses': [node('Your Addresses', 480)]}[stage[0]]
        def adb(_phone, *args, **_kwargs):
            if args[1:3] == ('input', 'swipe'):
                actions.append('swipe')
                stage[0] = 'ad_scrolled' if stage[0] == 'ad' else 'addresses'
            elif args[1:3] == ('input', 'keyevent'):
                actions.append('back'); stage[0] = 'account'
            return SimpleNamespace(stdout='Physical size: 420x910')
        with patch('amazon_android.create_address_flow._read_text_region',
                   side_effect=read), \
             patch('amazon_android.create_address_flow.cloud_adb',
                   side_effect=adb), \
             patch.object(self.stop, 'wait', return_value=False):
            action(None, self.deadline, self.stop)
        self.assertEqual(actions, ['swipe', 'back', 'swipe'])
        self.assertIn(24, self.state.create_address_completed)


if __name__ == '__main__':
    unittest.main()
