import io
import threading
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from PIL import Image

from amazon_android.change_us_flow import (_ICON, _account_icon_from_image,
                                            _after_back,
                                            _google_sheet, _passkey_page,
                                            _post_done_person, _StepBlocked,
                                            build_change_us_steps)
from amazon_android.cloud import CloudPhone
from amazon_android.core import ToolError
from amazon_android.post_menu import AttemptDeadline, RegistrationState
from amazon_android.runner import AccountData, RunJob


def node(text, bounds='[10,10][80,35]', **fields):
    return {'text': text, 'bounds': bounds, 'visible-to-user': 'true',
            'enabled': 'true', **fields}


class ChangeUsFlowTests(unittest.TestCase):
    def setUp(self):
        self.phone = CloudPhone('127.0.0.1:5001')
        self.state = RegistrationState()
        self.steps = build_change_us_steps(self.phone, self.state)
        self.stop = threading.Event()
        self.outer = AttemptDeadline(None)
        self.job = RunJob(0, 'batch', None, account=AccountData(
            '2025550123', 'Example User', 'ExamplePass!',
            'https://apifc.net/smsrecord?token=example'))

    def test_names_stop_at_b17_and_b1_waits_four_seconds_after_menu(self):
        self.assertEqual(len(self.steps), 17)
        self.assertTrue(self.steps[-1].name.startswith('b17 '))
        browse = node('', '[5,170][45,195]', **{
            'content-desc': 'Browse menu Tab', 'selected': 'true'})
        with patch('amazon_android.change_us_flow._observe', return_value=(
                browse, [browse])), \
             patch('amazon_android.change_us_flow._pause') as pause, \
             patch('amazon_android.change_us_flow._tap_for_transition') as tap:
            self.steps[0].action(None, self.outer, self.stop)
        tap.assert_not_called()
        self.assertEqual(pause.call_count, 1)
        self.assertGreater(pause.call_args.args[1], 3.5)
        self.assertIsNotNone(self.state.early_us_menu_until)

    def test_b2_requires_person_label_or_live_icon(self):
        person = node('', '[55,170][80,195]', **{'content-desc': 'Your Account Tab'})
        with patch('amazon_android.change_us_flow._observe', return_value=(
                person, [person])), \
             patch('amazon_android.change_us_flow._foreground'), \
             patch('amazon_android.change_us_flow._tap_for_transition') as tap:
            self.steps[1].action(None, self.outer, self.stop)
        self.assertEqual(tap.call_args.args[1], person)

    def test_b2_adb_focus_error_pauses_this_step(self):
        person = node('', '[55,170][80,195]', **{'content-desc': 'Your Account Tab'})
        with patch('amazon_android.change_us_flow._observe', return_value=(
                person, [person])), \
             patch('amazon_android.change_us_flow._foreground',
                   side_effect=ToolError('Amazon chưa ở phía trước')):
            with self.assertRaises(_StepBlocked):
                self.steps[1].action(None, self.outer, self.stop)

    def test_person_icon_template_matches_only_live_bottom_bar(self):
        icon = Image.open(_ICON).convert('RGB')
        frame = Image.new('RGB', (300, 500), 'white')
        frame.paste(icon, (95, 438))
        image = io.BytesIO()
        frame.save(image, format='PNG')
        with patch('amazon_android.change_us_flow.cloud_screenshot',
                   return_value=image.getvalue()):
            target = _account_icon_from_image(self.phone, AttemptDeadline(10))
        self.assertIsNotNone(target)
        blank = Image.new('RGB', (300, 500), 'white')
        image = io.BytesIO()
        blank.save(image, format='PNG')
        with patch('amazon_android.change_us_flow.cloud_screenshot',
                   return_value=image.getvalue()):
            self.assertIsNone(_account_icon_from_image(self.phone, AttemptDeadline(10)))
        evidence = Path(__file__).resolve().parent.parent / 'flow_images' / 'shared' / 'marketplace_us'
        for name in ('01_b16_account_tab.png', '07_b22_account_after_done.png'):
            with self.subTest(name=name), patch(
                    'amazon_android.change_us_flow.cloud_screenshot',
                    return_value=(evidence / name).read_bytes()):
                self.assertIsNotNone(_account_icon_from_image(
                    self.phone, AttemptDeadline(10)))

    def test_b7_sends_done_once_then_person_without_wait_after_it_appears(self):
        self.state.early_us_selected_sent = True
        done = node('Done')
        person = node('', '[55,170][80,195]', **{'content-desc': 'Your Account Tab'})
        with patch('amazon_android.change_us_flow._wait_target', side_effect=[
                (done, [done], AttemptDeadline(10)),
                (person, [person], AttemptDeadline(10))]) as find, \
             patch('amazon_android.change_us_flow._foreground'), \
             patch('amazon_android.change_us_flow._tap_for_transition') as tap:
            self.steps[6].action(None, self.outer, self.stop)
        self.assertTrue(self.state.early_us_done_sent)
        self.assertEqual([call.args[1] for call in tap.call_args_list], [done, person])
        self.assertEqual(find.call_args.kwargs['interval'], .15)
        self.assertTrue(find.call_args.kwargs['visual_only'])

    def test_b7_does_not_tap_person_still_visible_on_country_settings(self):
        person = node('', '[55,170][80,195]', **{'content-desc': 'Your Account Tab'})
        settings = [person, node('Country/Region and Language'),
                    node('Country/Region: United States'), node('Done')]
        self.assertIsNone(_post_done_person(self.phone, settings, AttemptDeadline(10)))
        self.assertEqual(_post_done_person(self.phone, [person], AttemptDeadline(10)),
                         person)

    def test_b5_never_scrolls_a_screen_without_country_list_evidence(self):
        with patch('amazon_android.change_us_flow._observe', return_value=(None, [])), \
             patch('amazon_android.change_us_flow._scroll_country') as scroll, \
             patch('amazon_android.change_us_flow._pause'), \
             patch('amazon_android.change_us_flow.time.monotonic',
                   side_effect=[0, 0, 76]):
            with self.assertRaises(_StepBlocked):
                self.steps[4].action(None, self.outer, self.stop)
        scroll.assert_not_called()

    def test_b6_observes_selected_country_and_does_not_tap_again_on_resume(self):
        us = node('United States')
        with patch('amazon_android.change_us_flow._wait_target', side_effect=[
                (us, [us], AttemptDeadline(10)),
                (True, [], AttemptDeadline(10))]) as find, \
             patch('amazon_android.change_us_flow._foreground'), \
             patch('amazon_android.change_us_flow._tap_for_transition') as tap:
            self.steps[5].action(None, self.outer, self.stop)
        self.assertTrue(self.state.early_us_selected_sent)
        self.assertEqual(find.call_count, 2)
        tap.assert_called_once()
        with patch('amazon_android.change_us_flow._wait_target', return_value=(
                True, [], AttemptDeadline(10))) as find, \
             patch('amazon_android.change_us_flow._tap_for_transition') as tap:
            self.steps[5].action(None, self.outer, self.stop)
        find.assert_called_once()
        tap.assert_not_called()

    def test_b6_accepts_us_already_selected_manually(self):
        with patch('amazon_android.change_us_flow._wait_target', side_effect=[
                (True, [], AttemptDeadline(10)),
                (True, [], AttemptDeadline(10))]), \
             patch('amazon_android.change_us_flow._tap_for_transition') as tap:
            self.steps[5].action(None, self.outer, self.stop)
        self.assertTrue(self.state.early_us_selected_sent)
        tap.assert_not_called()

    def test_b7_resume_does_not_send_done_again(self):
        self.state.early_us_done_sent = True
        person = node('', '[55,170][80,195]', **{'content-desc': 'Your Account Tab'})
        with patch('amazon_android.change_us_flow._wait_target', return_value=(
                person, [person], AttemptDeadline(10))) as find, \
             patch('amazon_android.change_us_flow._foreground'), \
             patch('amazon_android.change_us_flow._tap_for_transition') as tap:
            self.steps[6].action(None, self.outer, self.stop)
        find.assert_called_once()
        tap.assert_called_once()
        self.assertEqual(tap.call_args.args[1], person)

    def test_b8_waits_six_seconds_then_uses_create_account_below_sign_in(self):
        self.state.early_us_person_tapped_at = __import__('time').monotonic()
        create = node('Create account')
        with patch('amazon_android.change_us_flow._pause') as pause, \
             patch('amazon_android.change_us_flow._wait_target', return_value=(
                 create, [create], AttemptDeadline(10))) as find, \
             patch('amazon_android.change_us_flow._foreground'), \
             patch('amazon_android.change_us_flow._tap_for_transition') as tap:
            self.steps[7].action(self.job, self.outer, self.stop)
        self.assertGreater(pause.call_args.args[1], 5.5)
        self.assertIn('Create account', find.call_args.args[4])
        self.assertEqual(tap.call_args.args[1], create)

    def test_b9_pauses_without_this_machines_account_row(self):
        with self.assertRaises(_StepBlocked):
            self.steps[8].action(RunJob(0, 'batch', None), self.outer, self.stop)

    def test_b9_types_only_its_own_phone_row(self):
        field = node('', **{'class': 'android.widget.EditText'})
        with patch('amazon_android.change_us_flow._wait_target', return_value=(
                field, [field], AttemptDeadline(10))), \
             patch('amazon_android.change_us_flow._tap_input') as focus, \
             patch('amazon_android.change_us_flow._type_field') as typed:
            self.steps[8].action(self.job, self.outer, self.stop)
        focus.assert_called_once()
        self.assertEqual(typed.call_args.args[2], self.job.account.phone)

    def test_b14_fetches_otp_from_this_row_and_b15_never_repeats_create(self):
        field = node('', **{'class': 'android.widget.EditText'})
        create = node('Create your Amazon account')
        self.state.early_us_sms_requested_at = 1.0
        with patch('amazon_android.change_us_flow._wait_target', return_value=(
                field, [field], AttemptDeadline(10))), \
             patch('amazon_android.change_us_flow._check_summary'), \
             patch('amazon_android.change_us_flow._field', return_value=field), \
             patch('amazon_android.change_us_flow._tap_input'), \
             patch('amazon_android.change_us_flow.wait_for_new_otp',
                   return_value='123456') as fetch, \
             patch('amazon_android.change_us_flow._type_field') as typed:
            self.steps[13].action(self.job, self.outer, self.stop)
        self.assertEqual(fetch.call_args.args[0], self.job.account.otp_url)
        self.assertEqual(typed.call_args.args[2], '123456')
        self.assertEqual(self.state.code, '123456')

        otp = node('123456', **{'class': 'android.widget.EditText'})
        with patch('amazon_android.change_us_flow._wait_target', return_value=(
                create, [create], AttemptDeadline(10))) as find, \
             patch('amazon_android.change_us_flow._field', return_value=otp), \
             patch('amazon_android.change_us_flow._check_summary'), \
             patch('amazon_android.change_us_flow._foreground'), \
             patch('amazon_android.change_us_flow._tap_for_transition') as tap, \
             patch('amazon_android.change_us_flow._wait_raw', return_value=(
                 True, [], AttemptDeadline(10))):
            self.steps[14].action(self.job, self.outer, self.stop)
            self.steps[14].action(self.job, self.outer, self.stop)
        self.assertTrue(self.state.early_us_create_sent)
        find.assert_called_once()
        tap.assert_called_once()

    def test_b16_backs_out_of_google_sheet_and_b17_taps_passkey(self):
        sheet = [node('Account created'), node('Create a passkey'),
                 node('Accede a tu Cuenta de Google para crear llaves de acceso'),
                 node('Cancelar'), node('Acceder')]
        ready = [node('Account created'), node('Create a passkey')]
        self.assertTrue(_google_sheet(sheet))
        self.assertTrue(_passkey_page(sheet))
        self.assertFalse(_google_sheet(ready))
        with patch('amazon_android.change_us_flow._wait_raw', return_value=(
                'sheet', sheet, AttemptDeadline(10))), \
             patch('amazon_android.change_us_flow._after_back',
                   return_value='ready'), \
             patch('amazon_android.change_us_flow.cloud_adb') as adb:
            self.steps[15].action(self.job, self.outer, self.stop)
        self.assertEqual(adb.call_args.args[2:], ('input', 'keyevent', 'KEYCODE_BACK'))
        passkey = node('Create a passkey')
        with patch('amazon_android.change_us_flow._wait_raw', return_value=(
                passkey, ready, AttemptDeadline(10))), \
             patch('amazon_android.change_us_flow._foreground'), \
             patch('amazon_android.change_us_flow._tap_for_transition') as tap:
            self.steps[16].action(self.job, self.outer, self.stop)
        self.assertTrue(self.state.early_us_passkey_sent)
        self.assertEqual(tap.call_args.args[1], passkey)

    def test_b16_second_back_when_english_google_sheet_remains(self):
        spanish = [node('Account created'), node('Create a passkey'),
                   node('Accede a tu Cuenta de Google para crear llaves de acceso'),
                   node('Cancelar')]
        english = [node('Account created'), node('Create a passkey'),
                   node('Sign in to your Google Account to create passkeys'),
                   node('Cancel'), node('Sign in')]
        self.assertTrue(_google_sheet(english))
        with patch('amazon_android.change_us_flow._wait_raw', return_value=(
                'sheet', spanish, AttemptDeadline(30))), \
             patch('amazon_android.change_us_flow._after_back',
                   side_effect=['sheet', 'ready']) as observe, \
             patch('amazon_android.change_us_flow.cloud_adb') as adb:
            self.steps[15].action(self.job, self.outer, self.stop)
        self.assertEqual(observe.call_count, 2)
        self.assertEqual(adb.call_count, 2)
        self.assertEqual(self.state.early_us_back_attempts, 2)

    def test_after_back_rechecks_persistent_english_sheet(self):
        english = [node('Account created'), node('Create a passkey'),
                   node('Sign in to your Google Account to create passkeys'),
                   node('Cancel'), node('Sign in')]
        clock = iter(range(100))
        with patch('amazon_android.change_us_flow._raw_nodes',
                   return_value=english) as read, \
             patch('amazon_android.change_us_flow._pause'), \
             patch('amazon_android.change_us_flow.time.monotonic',
                   side_effect=lambda: next(clock)):
            self.assertEqual(_after_back(self.phone, self.outer, self.stop),
                             'sheet')
        self.assertGreaterEqual(read.call_count, 2)


if __name__ == '__main__':
    unittest.main()
