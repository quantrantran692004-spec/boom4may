import threading
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from amazon_android import account_flow as flow
from amazon_android.cloud import CloudPhone
from amazon_android.core import ToolError
from amazon_android.post_menu import AttemptDeadline
from amazon_android.runner import RunJob


def node(text, bounds):
    return {"text": text, "bounds": bounds}


class CountryRecoveryTests(unittest.TestCase):
    def setUp(self):
        self.phone = CloudPhone("127.0.0.1:5001")
        self.deadline = AttemptDeadline(180)
        self.stop = threading.Event()

    def test_country_ocr_swipe_stays_inside_visible_list_not_background_form(self):
        nodes = [node("Sign in or create account", "[0,0][1440,3120]"),
                 node("Country/region code", "[45,100][260,140]"),
                 node("Vanuatu +678", "[55,220][245,250]"),
                 node("Vietnam +84", "[55,300][240,330]"),
                 node("Zimbabwe +263", "[55,380][245,410]")]
        with patch.object(flow, "cloud_adb") as adb:
            flow._scroll_up(self.phone, nodes, self.deadline, country_list=True, reverse=True)
        args = adb.call_args.args
        x1, y1, x2, y2 = map(int, args[4:8])
        self.assertEqual(x1, x2)
        self.assertTrue(55 <= x1 <= 245)
        self.assertTrue(220 < y1 < y2 < 410)
        self.assertGreaterEqual(y2 - y1, 100)

    def test_country_popup_stays_open_after_tap_then_retries_current_us_row(self):
        us = node("United States +1", "[55,280][245,315]")
        country = [node("Country/region code", "[45,100][260,140]"), us,
                   node("Uruguay +598", "[55,320][245,355]")]
        form = [node("Enter mobile number or email", "[20,50][300,75]"),
                node("Continue", "[20,150][300,190]"), node("US +1", "[20,100][80,130]")]
        taps = []

        def read(*_, **_kwargs):
            return form if len(taps) >= 2 else country

        def wait(_phone, expected, *_args, **_kwargs):
            current = read()
            if flow.screen(current) not in expected:
                raise ToolError("Popup COUNTRY still open")
            return current

        action = next(step.action for step in flow.build_common_steps(self.phone, lambda _: None)
                      if step.name.startswith("b6"))
        with patch.object(flow, "_read_nodes", side_effect=read), \
             patch.object(flow, "_wait_screen", side_effect=wait), \
             patch.object(flow, "_tap", side_effect=lambda *args: taps.append(args[1])), \
             patch.object(flow, "cloud_adb", return_value=SimpleNamespace(stdout='Physical size: 300x600')), \
             patch.object(self.stop, "wait", return_value=False):
            action(RunJob(0, "batch", None), self.deadline, self.stop)
        self.assertEqual(len(taps), 2)
        self.assertIs(taps[0], us)
        self.assertEqual(flow._bounds(taps[1])[0:3:2], (149, 151))

    def test_country_uses_full_row_center_if_tapping_text_does_not_close_popup(self):
        us = node('United States +1', '[15,280][100,315]')
        country = [node('Country/region code', '[20,10][240,40]'), us,
                   node('Uruguay +598', '[15,320][100,355]')]
        form = [node('Sign in or create account', '[0,0][300,50]'),
                node('Enter mobile number or email', '[10,60][250,90]'),
                node('Continue', '[10,160][250,190]'),
                node('US +1', '[10,100][80,130]')]
        tapped = []
        def read(*_, **_kwargs):
            return form if len(tapped) >= 2 else country
        action = next(step.action for step in flow.build_common_steps(self.phone, lambda _: None)
                      if step.name.startswith('b6'))
        with patch.object(flow, '_read_nodes', side_effect=read), \
             patch.object(flow, '_tap', side_effect=lambda _phone, target, _deadline: tapped.append(target)), \
             patch.object(flow, 'cloud_adb', return_value=SimpleNamespace(stdout='Physical size: 300x600')), \
             patch.object(self.stop, 'wait', return_value=False):
            action(RunJob(0, 'batch', None), self.deadline, self.stop)
        self.assertEqual(len(tapped), 2)
        self.assertEqual(tapped[0], us)
        self.assertEqual(flow._bounds(tapped[1])[0:3:2], (149, 151))

    def test_country_scrolls_to_end_before_reversing_to_us(self):
        us = node('United States +1', '[15,280][100,315]')
        first = [node('Afghanistan +93', '[15,280][100,315]')]
        bottom = [node('Zimbabwe +263', '[15,280][100,315]')]
        with patch.object(flow, '_read_nodes', side_effect=[first, bottom, bottom, [us]]), \
             patch.object(flow, '_scroll_up') as scroll, \
             patch.object(self.stop, 'wait', return_value=False):
            self.assertEqual(flow._find_scrolling(self.phone, 'United States +1',
                                                  self.deadline, self.stop, country_list=True), us)
        self.assertEqual([(call.kwargs['fling'], call.kwargs['reverse'])
                          for call in scroll.call_args_list],
                         [(True, False), (False, True), (False, True)])

    def test_small_ocr_bounds_jitter_is_not_treated_as_list_still_flinging(self):
        original = node("United States +1", "[55,280][245,315]")
        jittered = node("United States +1", "[56,281][244,316]")
        self.assertTrue(flow._same_country_position(original, jittered))
        moved = node("United States +1", "[55,380][245,415]")
        self.assertFalse(flow._same_country_position(original, moved))

    def test_unresponsive_country_popup_has_bounded_selection_retries(self):
        us = node("United States +1", "[55,280][245,315]")
        country = [node("Country/region code", "[45,100][260,140]"), us]
        action = next(step.action for step in flow.build_common_steps(self.phone, lambda _: None)
                      if step.name.startswith("b6"))
        with patch.object(flow, "_read_nodes", return_value=country), \
             patch.object(flow, "_wait_screen", return_value=country), \
             patch.object(flow, "_tap") as tap, \
             patch.object(flow, "cloud_adb", return_value=SimpleNamespace(stdout='Physical size: 300x600')), \
             patch.object(self.stop, "wait", return_value=False):
            with self.assertRaisesRegex(ToolError, "bốn lần"):
                action(RunJob(0, "batch", None), self.deadline, self.stop)
        self.assertEqual(tap.call_count, 8)


if __name__ == "__main__":
    unittest.main()
