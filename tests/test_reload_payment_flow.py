import threading
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from amazon_android.cloud import CloudPhone
from amazon_android.core import ToolError
from amazon_android.post_menu import AttemptDeadline, RegistrationState
from amazon_android.reload_payment_flow import build_reload_payment_steps
from amazon_android.runner import AccountData, RunJob


def node(text, y):
    return {'text': text, 'bounds': f'[20,{y}][380,{y+30}]'}


class ReloadPaymentTests(unittest.TestCase):
    def setUp(self):
        from amazon_android import reload_payment_flow as flow
        self.phone = CloudPhone('127.0.0.1:5001')
        self.state = RegistrationState(flow_mode='create',
                                       create_address_completed=set(range(23, 32)))
        self.stop = threading.Event()
        self.deadline = AttemptDeadline(190)
        account = AccountData('12025550123', 'Example Person', 'ExamplePass1!',
                              'https://example.test/otp', '4111111111111111|12|2030')
        self.job = RunJob(0, 'batch', None, account=account)
        target_reader = patch.object(
            flow, '_read_text_region',
            side_effect=lambda phone, deadline, stop, crop, **_kwargs:
                flow._read(phone, deadline, stop, visual=True))
        target_reader.start()
        self.addCleanup(target_reader.stop)

    def test_b32_to_b39_uses_visible_labels_and_one_scroll_per_requested_step(self):
        from amazon_android import reload_payment_flow as flow
        stage = ['account']; swipes = []; taps = []; entered = []
        screens = {
            'account': [node('Your Orders', 100), node('Orders', 140),
                        node('Account', 180)],
            'account_bottom': [node('Gift Card Balance: $0.00', 440),
                               node('Reload Balance', 510)],
            'product': [node('Amazon Gift Card Balance Reload', 200)],
            'product_bottom': [node('Low Balance Auto-Reload', 150),
                               node('Buy Now', 740)],
            'payment': [node('Add a payment method', 360),
                        node('Add a credit or debit card', 400),
                        node('Set up now', 500)],
            'card': [node('Card number', 100), node('Card number', 140),
                     node('Expiration date', 190), node('MM / YY', 230),
                     node('Name on card', 285),
                     node('First and last name', 330),
                     node('Add and continue', 425)],
            'billing': [node('Use this address', 170)],
            'after_billing': [],
        }
        def adb(_phone, *args, **_kwargs):
            if args[1:3] == ('wm', 'size'):
                return SimpleNamespace(stdout='Physical size: 420x910')
            if args[1:3] == ('input', 'swipe'):
                swipes.append(stage[0])
                stage[0] = 'account_bottom' if stage[0] == 'account' else 'product_bottom'
            if args[1:3] == ('input', 'text'):
                entered.append(args[3])
            return SimpleNamespace(stdout='')
        def tap(_phone, target, _deadline):
            label = target.get('text', '')
            taps.append(label)
            stage[0] = {'Reload Balance': 'product', 'Buy Now': 'payment',
                        'Add a credit or debit card': 'card',
                        'Add and continue': 'billing',
                        'Use this address': 'after_billing'}.get(label, stage[0])
        with patch.object(flow, '_read', side_effect=lambda *_a, **_k: screens[stage[0]]), \
             patch.object(flow, '_foreground'), \
             patch.object(flow, 'cloud_adb', side_effect=adb), \
             patch.object(flow, '_tap', side_effect=tap), \
             patch.object(self.stop, 'wait', return_value=False):
            for step in build_reload_payment_steps(self.phone, self.state):
                step.action(self.job, self.deadline, self.stop)
        self.assertEqual(swipes, ['account', 'product'])
        self.assertEqual(''.join(entered).replace('%s', ' '),
                         '411111111111111112/30Example Person')
        self.assertIn('Add and continue', taps)
        self.assertIn('Use this address', taps)
        self.assertNotIn('Set up now', taps)
        self.assertEqual(self.state.reload_completed, {32, 33, 34, 36, 37, 38, 39})

    def test_b38_missing_card_stops_before_input(self):
        from amazon_android import reload_payment_flow as flow
        self.state.reload_completed.update({32, 33, 34, 36, 37})
        job = RunJob(0, 'batch', None,
                     account=AccountData('12025550123', 'Example Person',
                                         'ExamplePass1!', 'https://example.test/otp'))
        with patch.object(flow, 'cloud_adb') as adb:
            with self.assertRaisesRegex(ToolError, 'chưa có thẻ'):
                build_reload_payment_steps(self.phone, self.state)[-2].action(
                    job, self.deadline, self.stop)
        adb.assert_not_called()

    def test_b38_locates_all_three_fields_in_one_cropped_read_before_input(self):
        from amazon_android import reload_payment_flow as flow
        self.state.reload_completed.update({32, 33, 34, 36, 37})
        form = [node('Card number', 100), node('Card number', 140),
                node('Expiration date', 190), node('MM / YY', 230),
                node('Name on card', 285), node('First and last name', 330)]
        button = node('Add and continue', 425)
        sent = []
        def read(_phone, _deadline, _stop, crop, **kwargs):
            if crop == (.05, .58):
                self.assertTrue(kwargs['direct_visual'])
                self.assertFalse(sent)
                return form
            return [button]
        def adb(_phone, *args, **_kwargs):
            if args[:3] == ('shell', 'input', 'text'):
                sent.append(args[3])
            return SimpleNamespace(stdout='')
        with patch.object(flow, '_read_text_region', side_effect=read) as region, \
             patch.object(flow, '_foreground'), patch.object(flow, '_tap'), \
             patch.object(flow, 'cloud_adb', side_effect=adb):
            build_reload_payment_steps(self.phone, self.state)[-2].action(
                self.job, self.deadline, self.stop)
        self.assertEqual(region.call_count, 2)  # Form once, then button.
        self.assertEqual(len(sent), 35)
        self.assertEqual(self.state.reload_card_fields_sent, {0, 1, 2})

    def test_b38_hides_keyboard_and_taps_button_in_actual_image_region(self):
        from amazon_android import reload_payment_flow as flow
        from amazon_android import account_flow
        self.state.reload_completed.update({32, 33, 34, 36, 37})
        self.state.reload_card_fields_sent.update({0, 1, 2})
        target = node('Add and continue', 377)
        actions = []
        def adb(_phone, *args, **_kwargs):
            actions.append(args)
            return SimpleNamespace(stdout='')
        with patch.object(account_flow, '_keyboard_visible', return_value=True), \
             patch.object(flow, '_read_text_region', return_value=[target]) as read, \
             patch.object(flow, '_foreground'), \
             patch.object(flow, 'cloud_adb', side_effect=adb), \
             patch.object(flow, '_tap', side_effect=lambda *_: actions.append(('tap',))):
            build_reload_payment_steps(self.phone, self.state)[-2].action(
                self.job, self.deadline, self.stop)
        self.assertEqual(actions, [('shell', 'input', 'keyevent', 'KEYCODE_BACK'),
                                   ('tap',)])
        self.assertEqual(read.call_args.args[3], (.30, .80))

    def test_b38_button_crop_matches_saved_form_image(self):
        from amazon_android.reload_payment_flow import _find
        from amazon_android.vision import ocr_nodes
        screenshot = (Path(__file__).resolve().parents[1] / 'flow_images' /
                      'shared' / 'reload_payment' /
                      '06_b38_add_and_continue.png').read_bytes()
        nodes = ocr_nodes(screenshot, crop=(.30, .80), text_only=True)
        self.assertIsNotNone(_find(nodes, 'add and continue'))

    def test_b38_types_in_paced_groups_after_one_field_tap(self):
        from amazon_android import reload_payment_flow as flow
        entered = []
        target = node('Name on card', 300)
        with patch.object(flow, '_foreground'), \
             patch.object(flow, '_tap') as tap, \
             patch.object(self.stop, 'wait', return_value=False) as wait, \
             patch.object(flow, 'cloud_adb', side_effect=lambda _phone, *args, **_kw:
                          entered.append(args[3]) or SimpleNamespace(stdout='')):
            flow._input(self.phone, target, 'Example Person', self.deadline, self.stop)
        tap.assert_called_once()
        self.assertEqual(entered, list('Example') + ['%s'] + list('Person'))
        self.assertEqual([call.args[0] for call in wait.call_args_list], [.4] * 13)

    def test_b32_scrolls_immediately_after_person_tap_without_account_scan(self):
        from amazon_android import reload_payment_flow as flow
        with patch.object(flow, '_read',
                          side_effect=AssertionError('account scan')), \
             patch.object(flow, '_swipe') as swipe:
            build_reload_payment_steps(self.phone, self.state)[0].action(
                self.job, self.deadline, self.stop)
        swipe.assert_called_once()

    def test_reload_tap_is_followed_by_scroll_before_product_read(self):
        from amazon_android import reload_payment_flow as flow
        self.state.reload_completed.add(32)
        actions = []
        def read(*_args, **_kwargs):
            actions.append('read')
            return [node('Reload Balance', 510)] if 'tap' not in actions else [node('Buy Now', 740)]
        with patch.object(flow, '_read', side_effect=read), \
             patch.object(flow, '_foreground'), \
             patch.object(flow, '_tap', side_effect=lambda *_: actions.append('tap')), \
             patch.object(flow, '_swipe', side_effect=lambda *_a, **_k: actions.append('swipe')):
            steps = build_reload_payment_steps(self.phone, self.state)
            steps[1].action(self.job, self.deadline, self.stop)
            steps[2].action(self.job, self.deadline, self.stop)
        self.assertEqual(actions, ['read', 'tap', 'swipe'])

    def test_b33_scrolls_until_reload_balance_appears_then_taps(self):
        from amazon_android import reload_payment_flow as flow
        self.state.reload_completed.add(32)
        target = node('Reload Balance', 510)
        visible = [False]
        with patch.object(flow, '_read_text_region',
                          side_effect=lambda *_: [target] if visible[0] else []), \
             patch.object(flow, '_swipe',
                          side_effect=lambda *_a, **_k:
                              visible.__setitem__(0, True)) as swipe, \
             patch.object(flow, '_foreground'), \
             patch.object(flow, '_tap') as tap:
            build_reload_payment_steps(self.phone, self.state)[1].action(
                self.job, self.deadline, self.stop)
        swipe.assert_called_once()
        tap.assert_called_once_with(self.phone, target, unittest.mock.ANY)

    def test_b34_scrolls_as_soon_as_product_appears(self):
        from amazon_android import reload_payment_flow as flow
        self.state.reload_completed.update({32, 33})
        swipes = []
        def read(*_args, **_kwargs):
            return ([node('Buy Now', 740)] if swipes else
                    [node('Amazon Gift Card Balance Reload', 200)])
        with patch.object(flow, '_read', side_effect=read), \
             patch.object(flow, '_swipe', side_effect=lambda *_a, **_k: swipes.append(1)), \
             patch.object(self.stop, 'wait', return_value=False) as wait:
            build_reload_payment_steps(self.phone, self.state)[2].action(
                self.job, self.deadline, self.stop)
        self.assertEqual(len(swipes), 1)
        wait.assert_not_called()

    def test_b34_scrolls_before_reading_even_when_buy_now_is_visible(self):
        from amazon_android import reload_payment_flow as flow
        self.state.reload_completed.update({32, 33})
        with patch.object(flow, '_read',
                          side_effect=AssertionError('read before swipe')), \
             patch.object(flow, '_swipe') as swipe:
            build_reload_payment_steps(self.phone, self.state)[2].action(
                self.job, self.deadline, self.stop)
        swipe.assert_called_once()

    def test_missing_visual_label_uses_native_without_waiting(self):
        from amazon_android import reload_payment_flow as flow
        modes = []
        def read(*_args, visual=False, **_kwargs):
            modes.append(visual)
            return [node('Gift Card Balance', 440)] if visual else [node('Reload Balance', 510)]
        with patch.object(flow, '_read', side_effect=read), \
             patch.object(self.stop, 'wait', return_value=False) as wait:
            _, target = flow._read_until(self.phone, self.deadline, self.stop,
                                         'reload balance')
        self.assertEqual(target['text'], 'Reload Balance')
        self.assertEqual(modes, [True, True, False])
        wait.assert_not_called()

    def test_b34_does_not_need_product_title_to_start_short_scroll(self):
        from amazon_android import reload_payment_flow as flow
        self.state.reload_completed.update({32, 33})
        swipes = []
        with patch.object(flow, '_read', side_effect=lambda *_a, **_k:
                          [node('Buy Now', 740)] if swipes else
                          [node('Unrecognized loading page', 40)]), \
             patch.object(flow, '_swipe', side_effect=lambda *_a, **kw: swipes.append(kw)), \
             patch.object(self.stop, 'wait', return_value=False):
            build_reload_payment_steps(self.phone, self.state)[2].action(
                self.job, self.deadline, self.stop)
        self.assertEqual(swipes, [{'short': True}])

    def test_b36_taps_first_visible_buy_now_without_second_scan(self):
        from amazon_android import reload_payment_flow as flow
        self.state.reload_completed.update({32, 33, 34})
        target = node('Buy Now', 740)
        with patch.object(flow, '_read_text_region', return_value=[target]) as read, \
             patch.object(flow, '_read', side_effect=AssertionError('full scan')), \
             patch.object(flow, '_swipe') as swipe, \
             patch.object(flow, '_foreground'), \
             patch.object(flow, '_tap') as tap:
            build_reload_payment_steps(self.phone, self.state)[3].action(
                self.job, self.deadline, self.stop)
        read.assert_called_once()
        tap.assert_called_once_with(self.phone, target, unittest.mock.ANY)
        swipe.assert_not_called()

    def test_b36_scrolls_again_only_when_buy_now_is_absent(self):
        from amazon_android import reload_payment_flow as flow
        self.state.reload_completed.update({32, 33, 34})
        target = node('Buy Now', 740)
        visible = [False]
        with patch.object(flow, '_read_text_region',
                          side_effect=lambda *_: [target] if visible[0] else []), \
             patch.object(flow, '_swipe',
                          side_effect=lambda *_a, **_k:
                              visible.__setitem__(0, True)) as swipe, \
             patch.object(flow, '_foreground'), \
             patch.object(flow, '_tap') as tap:
            build_reload_payment_steps(self.phone, self.state)[3].action(
                self.job, self.deadline, self.stop)
        swipe.assert_called_once()
        tap.assert_called_once()

    def test_b37_visible_card_text_is_found_in_cropped_user_image(self):
        from amazon_android.reload_payment_flow import _find
        from amazon_android.vision import ocr_nodes
        screenshot = (Path(__file__).resolve().parents[1] / 'flow_images' /
                      'shared' / 'reload_payment' /
                      '09_b37_visible_card_option.png').read_bytes()
        nodes = ocr_nodes(screenshot, crop=(.20, .65), text_only=True)
        target = _find(nodes, 'add a credit or debit card')
        self.assertIsNotNone(target)
        self.assertEqual(target['text'], 'Add a credit or debit card')
        self.assertTrue(300 < int(target['bounds'].split(',')[1].split(']')[0]) < 420)

    def test_b37_taps_target_region_text_without_full_screen_read(self):
        from amazon_android import reload_payment_flow as flow
        self.state.reload_completed.update({32, 33, 34, 36})
        target = node('Add a credit or debit card', 370)
        with patch.object(flow, '_read_text_region', return_value=[target]) as region, \
             patch.object(flow, '_read', side_effect=AssertionError('full-screen read')), \
             patch.object(flow, '_foreground'), \
             patch.object(flow, '_tap') as tap:
            build_reload_payment_steps(self.phone, self.state)[4].action(
                self.job, self.deadline, self.stop)
        region.assert_called_once()
        tap.assert_called_once_with(self.phone, target, unittest.mock.ANY)
        self.assertIn(37, self.state.reload_completed)

    def test_b38_taps_add_and_continue_from_button_region_after_fields_sent(self):
        from amazon_android import reload_payment_flow as flow
        from amazon_android import account_flow
        self.state.reload_completed.update({32, 33, 34, 36, 37})
        self.state.reload_card_fields_sent.update({0, 1, 2})
        target = node('Add and continue', 380)
        with patch.object(flow, '_read_text_region', return_value=[target]) as region, \
             patch.object(flow, '_read', side_effect=AssertionError('full scan')), \
             patch.object(account_flow, '_keyboard_visible', return_value=False), \
             patch.object(flow, '_foreground'), \
             patch.object(flow, '_tap') as tap:
            build_reload_payment_steps(self.phone, self.state)[-2].action(
                self.job, self.deadline, self.stop)
        self.assertEqual(region.call_args.args[3], (.30, .80))
        tap.assert_called_once_with(self.phone, target, unittest.mock.ANY)
        self.assertIn(38, self.state.reload_completed)

    def test_b39_taps_use_this_address_without_billing_page_checks(self):
        from amazon_android import reload_payment_flow as flow
        self.state.reload_completed.update({32, 33, 34, 36, 37, 38})
        target = node('Use this address', 170)
        with patch.object(flow, '_read_text_region', return_value=[target]) as region, \
             patch.object(flow, '_read', side_effect=AssertionError('page scan')), \
             patch.object(flow, '_foreground') as foreground, \
             patch.object(flow, '_tap') as tap:
            build_reload_payment_steps(self.phone, self.state)[-1].action(
                self.job, self.deadline, self.stop)
        self.assertEqual(region.call_args.args[3], (.05, .50))
        tap.assert_called_once_with(self.phone, target, unittest.mock.ANY)
        foreground.assert_not_called()
        self.assertIn(39, self.state.reload_completed)


if __name__ == '__main__':
    unittest.main()
