import json
import tempfile
import threading
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

from amazon_android.cloud import CloudPhone
from amazon_android.core import ToolError
from amazon_android.create_address_detail_flow import build_create_address_detail_steps
from amazon_android.post_menu import AttemptDeadline, RegistrationState


def item(text, y, **extra):
    return {'text': text, 'bounds': f'[20,{y}][380,{y+40}]', **extra}


class AddressDetailTests(unittest.TestCase):
    def setUp(self):
        from amazon_android import create_address_detail_flow as flow
        self.phone = CloudPhone('127.0.0.1:5001')
        self.state = RegistrationState(flow_mode='create',
                                       create_address_completed={23, 24, 25})
        self.stop = threading.Event()
        self.deadline = AttemptDeadline(190)
        text_reader = patch.object(
            flow, '_read_text_region',
            side_effect=lambda phone, deadline, stop, crop, **_kwargs:
                flow._read(phone, deadline, stop, visual=True))
        text_reader.start()
        self.addCleanup(text_reader.stop)

    def test_prefix_history_prevents_reuse_after_new_call(self):
        from amazon_android import create_address_detail_flow as flow
        with tempfile.TemporaryDirectory() as directory, \
             patch.object(flow, '_prefix_file', Path(directory) / 'prefixes.json'), \
             patch.object(flow.secrets, 'choice', side_effect=lambda choices: choices[0]):
            self.assertEqual(flow._new_prefix(), '100')
            self.assertEqual(flow._new_prefix(), '101')
            self.assertEqual(json.loads(flow._prefix_file.read_text()), ['100', '101'])

    def test_b28_uses_saved_proxy_digits_instead_of_random_fallback(self):
        from amazon_android import create_address_detail_flow as flow
        self.state.create_address_completed.update({26, 27})
        self.state.create_address_proxy_prefix = '3654'
        stage = ['form']
        street = item('Street address or P.O. Box', 270,
                      **{'class': 'android.widget.EditText'})
        base = [item('Country/Region', 150), item('Street address', 240)]
        screens = {'form': base + [street],
                   'suggestions': base + [item('3654', 270),
                                          item('3654 Main St, City, AL 36547', 330)],
                   'populated': base + [item('3654 Main St', 270),
                                        item('ZIP Code', 390), item('36547', 440),
                                        item('City', 490)]}
        typed = []
        def adb(_phone, *args, **_kwargs):
            if args[:3] == ('shell', 'input', 'text'):
                typed.append(args[3]); stage[0] = 'suggestions'
            return SimpleNamespace(stdout='')
        def tap(_phone, target, _deadline):
            if stage[0] == 'suggestions':
                stage[0] = 'populated'
        with patch.object(flow, '_read_hierarchy', side_effect=AssertionError('native read')) as native, \
             patch.object(flow, '_read', side_effect=lambda *_a, **_k: screens[stage[0]]), \
             patch.object(flow, '_foreground'), \
             patch.object(flow, '_new_prefix', side_effect=AssertionError('random fallback')), \
             patch.object(flow, '_tap_for_transition', side_effect=tap), \
             patch.object(flow, '_tap'), \
             patch.object(flow, 'cloud_adb', side_effect=adb), \
             patch.object(self.stop, 'wait', return_value=False):
            build_create_address_detail_steps(self.phone, self.state)[2].action(
                None, self.deadline, self.stop)
        self.assertEqual(typed, list('3654'))
        self.assertIn(28, self.state.create_address_completed)
        native.assert_not_called()

    def test_b28_never_selects_unit_field_when_street_field_missing(self):
        from amazon_android import create_address_detail_flow as flow
        native = [item('Country/Region', 120), item('Street address', 220),
                  item('Unit or suite number', 310),
                  item('', 335, **{'class': 'android.widget.EditText'})]
        self.assertIsNone(flow._street_field(native))
        visual = [item('Street address', 220),
                  item('Street address or P.O. Box', 260, vision='true')]
        self.assertEqual(flow._street_field(visual)['text'], 'Street address or P.O. Box')

    def test_b28_rejects_street_resource_id_on_unit_row(self):
        from amazon_android import create_address_detail_flow as flow
        nodes = [item('Street address', 150), item('Unit or suite number', 240),
                 item('', 270, **{'class': 'android.widget.EditText',
                                  'resource-id': 'streetAddress'})]
        self.assertIsNone(flow._street_field(nodes))

    def test_b28_ocr_accepts_address_line_one_above_unit(self):
        from amazon_android import create_address_detail_flow as flow
        nodes = [item('Address line 1', 130, vision='true'),
                 item('Enter street address', 180, vision='true'),
                 item('Unit or suite number', 240, vision='true')]
        field = flow._street_field(nodes)
        self.assertEqual(field['text'], 'Enter street address')
        self.assertEqual(flow._street_tap_target(nodes, field)['bounds'],
                         '[199,199][201,201]')

    def test_b28_types_before_reading_delayed_suggestions(self):
        from amazon_android import create_address_detail_flow as flow
        self.state.create_address_completed.update({26, 27})
        self.state.create_address_proxy_prefix = '0218'
        suggestions = [item('0218 Main St', 300, vision='true')]
        events = []
        visual_reads = [[], suggestions]
        def adb(_phone, *args, **_kwargs):
            if args[:3] == ('shell', 'input', 'text'):
                events.append(('type', args[3]))
            return SimpleNamespace(stdout='')
        def read(*_args, **_kwargs):
            events.append(('read', None))
            return visual_reads.pop(0)
        with patch.object(flow, '_read_hierarchy', side_effect=AssertionError('native read')) as native, \
             patch.object(flow, '_read_text_region', side_effect=read), \
             patch.object(flow, '_foreground'), patch.object(flow, '_tap') as tap, \
             patch.object(flow, 'cloud_adb', side_effect=adb), \
             patch.object(self.stop, 'wait', return_value=False):
            build_create_address_detail_steps(self.phone, self.state)[2].action(
                None, self.deadline, self.stop)
        tap.assert_called_once()
        self.assertEqual(events[:4], [('type', digit) for digit in '0218'])
        self.assertEqual([kind for kind, _ in events], ['type'] * 4 + ['read', 'read'])
        native.assert_not_called()

    def test_b28_selects_cropped_suggestion_without_native_dump(self):
        from amazon_android import create_address_detail_flow as flow
        self.state.create_address_completed.update({26, 27})
        self.state.create_address_proxy_prefix = '545'
        form = [item('Street address', 220, vision='true'),
                item('Street address or P.O. Box', 260, vision='true')]
        suggestion = [item('545', 270, vision='true'),
                      item('545 Lake Washington Blvd E', 330, vision='true')]
        sent = []
        def adb(_phone, *args, **_kwargs):
            if args[:3] == ('shell', 'input', 'text'):
                sent.append(args[3])
            return SimpleNamespace(stdout='')
        with patch.object(flow, '_read', return_value=form), \
             patch.object(flow, '_read_text_region',
                          side_effect=lambda *_a, **_k: suggestion if sent else []), \
             patch.object(flow, '_read_hierarchy', side_effect=AssertionError('native dump')) as native, \
             patch.object(flow, '_foreground'), patch.object(flow, '_tap') as tap, \
             patch.object(flow, 'cloud_adb', side_effect=adb):
            build_create_address_detail_steps(self.phone, self.state)[2].action(
                None, self.deadline, self.stop)
        self.assertEqual(sent, list('545'))
        self.assertIn(28, self.state.create_address_completed)
        self.assertEqual(tap.call_count, 1)
        native.assert_not_called()

    def test_b27_uses_ocr_when_native_returns_partial_form(self):
        from amazon_android import create_address_detail_flow as flow
        self.state.create_address_completed.add(26)
        native = [item('Add a new address', 20), item('United States', 100)]
        visual = [item('Country/Region', 60), item('Street address', 150),
                  item('Street address or P.O. Box', 180, vision='true'),
                  item('Unit or suite number', 240)]
        with patch.object(flow, '_read_hierarchy', return_value=native), \
             patch.object(flow, '_read', return_value=visual) as ocr, \
             patch.object(flow, '_tap_for_transition') as tap:
            build_create_address_detail_steps(self.phone, self.state)[1].action(
                None, self.deadline, self.stop)
        self.assertIn(27, self.state.create_address_completed)
        self.assertTrue(ocr.called)
        tap.assert_not_called()

    def test_b27_accepts_visible_street_without_other_form_labels(self):
        from amazon_android import create_address_detail_flow as flow
        self.state.create_address_completed.add(26)
        visual = [item('Street address', 220, vision='true'),
                  item('Street address or P.O. Box', 260, vision='true')]
        with patch.object(flow, '_read_text_region', return_value=visual), \
             patch.object(flow, '_read_hierarchy') as native, \
             patch.object(flow, '_tap_for_transition') as tap:
            build_create_address_detail_steps(self.phone, self.state)[1].action(
                None, self.deadline, self.stop)
        self.assertIn(27, self.state.create_address_completed)
        native.assert_not_called()
        tap.assert_not_called()

    def test_b27_blue_manual_link_advances_directly_to_b28(self):
        from amazon_android import create_address_detail_flow as flow
        self.state.create_address_completed.add(26)
        link = item('Enter an address manually', 320, vision='true')
        with patch.object(flow, '_read_text_region', return_value=[link]) as read, \
             patch.object(flow, '_read_hierarchy', side_effect=AssertionError('native read')) as native, \
             patch.object(flow, '_foreground'), \
             patch.object(flow, '_tap_for_transition') as tap:
            build_create_address_detail_steps(self.phone, self.state)[1].action(
                None, self.deadline, self.stop)
        read.assert_called_once()
        tap.assert_called_once()
        native.assert_not_called()
        self.assertIn(27, self.state.create_address_completed)

    def test_b28_uncertain_input_is_not_sent_again_on_resume(self):
        from amazon_android import create_address_detail_flow as flow
        self.state.create_address_completed.update({26, 27})
        self.state.create_address_proxy_prefix = '545'
        suggestion = [item('545 Main St', 300, vision='true')]
        with patch.object(flow, 'cloud_adb', side_effect=ToolError('ADB timeout')) as adb, \
             patch.object(flow, '_read_text_region') as read:
            with self.assertRaisesRegex(ToolError, 'chưa rõ số đã được nhập'):
                build_create_address_detail_steps(self.phone, self.state)[2].action(
                    None, self.deadline, self.stop)
        adb.assert_called_once()
        read.assert_not_called()
        self.assertTrue(self.state.create_address_prefix_sent)
        with patch.object(flow, 'cloud_adb') as resumed_adb, \
             patch.object(flow, '_read_text_region', return_value=suggestion), \
             patch.object(flow, '_foreground'), patch.object(flow, '_tap') as tap:
            build_create_address_detail_steps(self.phone, self.state)[2].action(
                None, self.deadline, self.stop)
        resumed_adb.assert_not_called()
        tap.assert_called_once()
        self.assertIn(28, self.state.create_address_completed)

    def test_native_fallback_does_not_restart_phone_ocr_reader(self):
        from amazon_android import create_address_detail_flow as flow
        reader = SimpleNamespace(call=Mock(return_value=[]))
        with patch('amazon_android.isolated_reader.current', return_value=reader), \
             patch.object(flow, '_read_hierarchy', return_value=[]) as direct:
            flow._bounded_native(self.phone, AttemptDeadline(30), self.stop)
        reader.call.assert_not_called()
        direct.assert_called_once()

    def test_b28_rejects_edit_box_that_overlaps_unit_row(self):
        from amazon_android import create_address_detail_flow as flow
        nodes = [item('Street address', 220), item('Unit or suite number', 310),
                 {'text': '', 'bounds': '[20,270][380,340]',
                  'class': 'android.widget.EditText', 'focused': 'true'}]
        self.assertFalse(flow._street_focused(nodes))

    def test_b26_to_b31_read_native_text_and_confirm_each_transition(self):
        from amazon_android import create_address_detail_flow as flow
        stage = ['addresses']
        taps = []
        street = item('Street address or P.O. Box', 270,
                      **{'class': 'android.widget.EditText'})
        screens = {
            'addresses': [item('Your Addresses', 90), item('Add a new address', 150)],
            'search': [item('Search for an address', 130),
                       item('Enter an address manually', 320)],
            'form': [item('Country/Region', 150), item('Street address', 240), street],
            'suggestions': [item('Country/Region', 150), item('Street address', 240),
                            item('545', 270, **{'class': 'android.widget.EditText'}),
                            item('545 N 78th St, Seattle, WA 98103', 330)],
            'populated': [item('Country/Region', 150), item('Street address', 240),
                          item('545 N 78th St', 270), item('ZIP Code', 390),
                          item('98103', 440), item('City', 490),
                          item('Make this my default address', 650, checked='true'),
                          item('Add address', 760)],
            'saved': [item('Address saved', 40), item('Your Addresses', 100),
                      item('Add a new address', 150), item('Personal Addresses', 260),
                      item('', 830, **{'content-desc': 'Your Account Tab, 2 of 4'})],
            'account': [item('Your Orders', 190), item('Orders', 130),
                        item('Account', 130)],
        }
        def tap(_phone, target, _deadline):
            taps.append(target.get('text') or target.get('content-desc'))
            if stage[0] == 'form':
                return
            if stage[0] == 'populated' and not target.get('text'):
                return  # b29 taps the square beside the label.
            stage[0] = {'addresses': 'search', 'search': 'form',
                        'suggestions': 'populated', 'populated': 'saved',
                        'saved': 'account'}[stage[0]]
        def adb(_phone, *args, **_kwargs):
            if args[:3] == ('shell', 'input', 'text'):
                stage[0] = 'suggestions'
            return SimpleNamespace(stdout='Physical size: 420x910')
        with patch.object(flow, '_read_hierarchy', side_effect=lambda *_: screens[stage[0]]) as read, \
             patch.object(flow, '_read', side_effect=lambda *_a, **_k: screens[stage[0]]), \
             patch.object(flow, '_default_visual_label', return_value={
                 'text': 'Make this my default address',
                 'bounds': '[51,650][300,690]', 'vision': 'true'}), \
             patch.object(flow, '_street_focused', return_value=True), \
             patch.object(flow, '_foreground'), \
             patch.object(flow, '_new_prefix', return_value='545'), \
             patch.object(flow, '_tap_for_transition', side_effect=tap), \
             patch.object(flow, '_tap', side_effect=tap), \
             patch.object(flow, 'cloud_adb', side_effect=adb), \
             patch.object(self.stop, 'wait', return_value=False):
            for step in build_create_address_detail_steps(self.phone, self.state):
                step.action(None, self.deadline, self.stop)
        self.assertEqual(self.state.create_address_completed, set(range(23, 32)))
        self.assertEqual(taps, ['Add a new address', 'Enter an address manually',
                                '545 N 78th St, Seattle, WA 98103',
                                None,
                                'Add address', 'Your Account Tab, 2 of 4'])
        self.assertEqual(self.state.create_address_submit_attempts, 1)

    def test_b26_reads_webview_image_before_native_dump(self):
        from amazon_android import create_address_detail_flow as flow
        order = []
        def visual(*_args, **_kwargs):
            order.append('visual')
            raise AssertionError('first backend')
        with patch.object(flow, '_read', side_effect=visual), \
             patch.object(flow, '_read_hierarchy', side_effect=lambda *_a:
                          (order.append('native') or [])), \
             self.assertRaisesRegex(AssertionError, 'first backend'):
            build_create_address_detail_steps(self.phone, self.state)[0].action(None, self.deadline, self.stop)
        self.assertEqual(order, ['visual'])

    def test_b28_taps_visible_suggestion_without_waiting_for_zip_fill(self):
        from amazon_android import create_address_detail_flow as flow
        self.state.create_address_completed.update({26, 27})
        self.state.create_address_prefix = '545'
        self.state.create_address_prefix_sent = True
        self.state.create_address_prefix_sent_at = flow.time.monotonic()
        visual = [item('Street address', 240),
                  {'text': '545', 'bounds': '[25,278][64,301]', 'vision': 'true'},
                  {'text': '545 Lake Washington Blvd E',
                   'bounds': '[22,317][245,339]', 'vision': 'true'},
                  {'text': 'Seattle, WA 98112',
                   'bounds': '[23,339][169,359]', 'vision': 'true'}]
        with patch.object(flow, '_read_text_region', return_value=visual) as read, \
             patch.object(flow, '_read_hierarchy',
                          side_effect=AssertionError('native reread')), \
             patch.object(flow, '_foreground'), \
             patch.object(flow, '_tap') as tap:
            build_create_address_detail_steps(self.phone, self.state)[2].action(
                None, self.deadline, self.stop)
        read.assert_called_once()
        tap.assert_called_once()
        self.assertEqual(tap.call_args.args[1]['text'], '545 Lake Washington Blvd E')
        self.assertIn(28, self.state.create_address_completed)

    def test_b29_taps_checkbox_once_without_status_scan(self):
        from amazon_android import create_address_detail_flow as flow
        self.state.create_address_completed.update({26, 27, 28})
        label = {'text': 'Make this my default address',
                 'bounds': '[51,489][298,512]', 'vision': 'true'}
        with patch.object(flow, '_read', return_value=[label]) as read, \
             patch.object(flow, '_foreground'), \
             patch.object(flow, '_tap') as tap:
            build_create_address_detail_steps(self.phone, self.state)[3].action(
                None, self.deadline, self.stop)
        read.assert_called_once()
        tap.assert_called_once()
        self.assertEqual(tap.call_args.args[1]['bounds'], '[31,499][33,501]')
        self.assertIn(29, self.state.create_address_completed)

    def test_b29_scrolls_to_label_then_taps_square(self):
        from amazon_android import create_address_detail_flow as flow
        self.state.create_address_completed.update({26, 27, 28})
        label = {'text': 'Make this my default address',
                 'bounds': '[51,489][298,512]', 'vision': 'true'}
        with patch.object(flow, '_read', side_effect=[[item('Phone number', 200)], [label]]) as read, \
             patch.object(flow, '_scroll') as scroll, \
             patch.object(flow, '_foreground'), \
             patch.object(flow, '_tap') as tap:
            build_create_address_detail_steps(self.phone, self.state)[3].action(
                None, self.deadline, self.stop)
        self.assertEqual(read.call_count, 2)
        scroll.assert_called_once()
        tap.assert_called_once()
        self.assertIn(29, self.state.create_address_completed)

    def test_b29_tap_failure_keeps_b30_blocked(self):
        from amazon_android import create_address_detail_flow as flow
        self.state.create_address_completed.update({26, 27, 28})
        label = {'text': 'Make this my default address',
                 'bounds': '[51,489][298,512]', 'vision': 'true'}
        steps = build_create_address_detail_steps(self.phone, self.state)
        with patch.object(flow, '_read', return_value=[label]), \
             patch.object(flow, '_foreground'), \
             patch.object(flow, '_tap', side_effect=ToolError('tap failed')):
            with self.assertRaisesRegex(ToolError, 'tap failed'):
                steps[3].action(None, self.deadline, self.stop)
        with self.assertRaisesRegex(ToolError, 'Chưa hoàn tất b29'):
            steps[4].action(None, self.deadline, self.stop)
        self.assertNotIn(29, self.state.create_address_completed)

    def test_default_visual_label_tolerates_one_ocr_letter_error(self):
        from amazon_android import create_address_detail_flow as flow
        nodes = [{'text': 'Make this my defauIt address',
                  'bounds': '[51,489][298,512]', 'vision': 'true'},
                 {'text': 'Delivery instructions',
                  'bounds': '[51,550][298,580]', 'vision': 'true'}]
        self.assertEqual(flow._default_visual_label(nodes), nodes[0])

    def test_b30_taps_visible_add_address_from_ocr_without_scrolling(self):
        from amazon_android import create_address_detail_flow as flow
        self.state.create_address_completed.update({26, 27, 28, 29})
        native = [item('ZIP Code', 80), item('City', 130)]
        visual = [item('Add address', 680, vision='true')]
        saved = [item('Address saved', 80)]
        tapped = []
        with patch.object(flow, '_read_hierarchy',
                          side_effect=lambda *_: saved if tapped else native), \
             patch.object(flow, '_read', side_effect=lambda *_a, **_k:
                          saved if tapped else visual), \
             patch.object(flow, '_foreground'), \
             patch.object(flow, '_scroll') as scroll, \
             patch.object(flow, '_tap_for_transition',
                          side_effect=lambda _p, target, _d: tapped.append(target)), \
             patch.object(self.stop, 'wait', return_value=False):
            build_create_address_detail_steps(self.phone, self.state)[4].action(
                None, self.deadline, self.stop)
        self.assertEqual(tapped[0]['text'], 'Add address')
        self.assertIn(30, self.state.create_address_completed)
        scroll.assert_not_called()

    def test_b30_scrolls_then_taps_add_address_without_form_check(self):
        from amazon_android import create_address_detail_flow as flow
        self.state.create_address_completed.update({26, 27, 28, 29})
        visible = [item('Add address', 680, vision='true')]
        saved = [item('Address saved', 80)]
        stage = ['above_button']
        tapped = []
        def read(*_args, **_kwargs):
            if tapped:
                return saved
            return visible if stage[0] == 'at_button' else [item('Phone number', 500)]
        with patch.object(flow, '_read', side_effect=read), \
             patch.object(flow, '_foreground'), \
             patch.object(flow, '_scroll', side_effect=lambda *_:
                          stage.__setitem__(0, 'at_button')) as scroll, \
             patch.object(flow, '_tap_for_transition',
                          side_effect=lambda _p, target, _d: tapped.append(target)), \
             patch.object(self.stop, 'wait', return_value=False):
            build_create_address_detail_steps(self.phone, self.state)[4].action(
                None, self.deadline, self.stop)
        scroll.assert_called_once()
        self.assertEqual(tapped[0]['text'], 'Add address')
        self.assertIn(30, self.state.create_address_completed)

    def test_b31_uses_device_tab_position_when_saved_page_hides_icon_label(self):
        from amazon_android import create_address_detail_flow as flow
        self.state.create_address_completed.update(range(26, 31))
        self.state.create_address_saved_at = 0
        stage = ['saved']
        saved = [item('Your Addresses', 90), item('Add a new address', 150)]
        account = [item('Your Orders', 190), item('Orders', 130), item('Account', 130)]
        with patch.object(flow, '_read_hierarchy', side_effect=lambda *_:
                          saved if stage[0] == 'saved' else account), \
             patch.object(flow, '_read', side_effect=lambda *_a, **_k:
                          saved if stage[0] == 'saved' else account), \
             patch.object(flow, '_foreground'), \
             patch.object(flow, '_account_tab', return_value=item('', 830)) as locate, \
             patch.object(flow, '_tap',
                          side_effect=lambda *_: stage.__setitem__(0, 'account')) as click, \
             patch.object(self.stop, 'wait', return_value=False):
            build_create_address_detail_steps(self.phone, self.state)[5].action(
                None, self.deadline, self.stop)
        locate.assert_called_once()
        click.assert_called_once()
        self.assertIn(31, self.state.create_address_completed)

    def test_b31_finishes_after_person_tap_without_account_scan(self):
        from amazon_android import create_address_detail_flow as flow
        self.state.create_address_completed.update(range(26, 31))
        self.state.create_address_saved_at = 0
        saved = [item('Your Addresses', 90), item('Add a new address', 150)]
        with patch.object(flow, '_read_hierarchy', return_value=saved) as read, \
             patch.object(flow, '_read',
                          side_effect=AssertionError('post-tap scan')), \
             patch.object(flow, '_foreground'), \
             patch.object(flow, '_account_tab', return_value=item('', 830)), \
             patch.object(flow, '_tap') as tap, \
             patch.object(self.stop, 'wait', return_value=False):
            build_create_address_detail_steps(self.phone, self.state)[5].action(
                None, self.deadline, self.stop)
        read.assert_called_once()
        tap.assert_called_once()
        self.assertIn(31, self.state.create_address_completed)
        self.assertIsNotNone(self.state.create_address_person_tapped_at)


if __name__ == '__main__':
    unittest.main()
