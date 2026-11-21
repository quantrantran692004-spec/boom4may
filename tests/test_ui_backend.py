import unittest
from unittest.mock import Mock, patch

from amazon_android import ui_backend as ui, account_flow as flow
from amazon_android.cloud import CloudPhone
from amazon_android.core import AMAZON_PACKAGE
from amazon_android.post_menu import AttemptDeadline
import threading


MENU = f'<hierarchy><node package="{AMAZON_PACKAGE}" text="Shop by category" /></hierarchy>'
COUNTRY = f'''<hierarchy><node package="{AMAZON_PACKAGE}" text="Country/region code" />
<node package="{AMAZON_PACKAGE}" scrollable="true" bounds="[40,100][320,650]" /></hierarchy>'''


class UiBackendTests(unittest.TestCase):
    def setUp(self):
        self.phone = CloudPhone('127.0.0.1:5001')
        ui._sessions.clear()

    def tearDown(self):
        ui._sessions.clear()

    def test_reads_reuse_per_phone_client_and_request_full_hierarchy(self):
        first = Mock(); first.dump_hierarchy.return_value = MENU
        second = Mock(); second.dump_hierarchy.return_value = MENU
        other = CloudPhone('127.0.0.1:5002')
        with patch.object(ui, '_connect', side_effect=[first, second]) as connect:
            self.assertEqual(ui.read_tree(self.phone), MENU)
            self.assertEqual(ui.read_tree(self.phone), MENU)
            self.assertEqual(ui.read_tree(other), MENU)
        self.assertEqual(connect.call_count, 2)
        first.dump_hierarchy.assert_called_with(max_depth=150, root_in_active=False)

    def test_failed_reader_stops_own_service_and_cools_down_before_retry(self):
        device = Mock(); device.dump_hierarchy.side_effect = RuntimeError('network')
        with patch.object(ui, '_connect', return_value=device) as connect:
            self.assertIsNone(ui.read_tree(self.phone))
            self.assertIsNone(ui.read_tree(self.phone))
        connect.assert_called_once()
        device.stop_uiautomator.assert_called_once_with(wait=False)
        self.assertFalse(ui.ready(self.phone))

    def test_unknown_or_missing_package_does_not_trigger_device_auto_selection(self):
        with patch.object(ui, 'swarmote_tunnel_owner', return_value=False), \
             patch('socket.create_connection') as socket:
            self.assertIsNone(ui.read_tree(self.phone))
        socket.assert_not_called()

    def test_fast_hierarchy_does_not_also_run_cli_dump_or_ocr(self):
        with patch.object(ui, 'read_tree', return_value=MENU), \
             patch.object(flow, 'cloud_adb') as adb, \
             patch.object(flow, '_read_visual_nodes') as ocr:
            nodes = flow._read_nodes(self.phone, AttemptDeadline(180), threading.Event())
        self.assertEqual(flow.screen(nodes), 'MENU')
        adb.assert_not_called(); ocr.assert_not_called()

    def _ready_device(self):
        device = Mock()
        device.dump_hierarchy.return_value = COUNTRY
        device.return_value.count = 1
        ui._session(self.phone).device = device
        return device

    def test_native_country_fling_uses_bounded_scroll_to_end(self):
        device = self._ready_device()
        self.assertTrue(ui.country_scroll(self.phone, fling=True, reverse=False))
        device.return_value.fling.toEnd.assert_called_once_with(max_swipes=3)

    def test_reverse_small_swipe_uses_current_native_container(self):
        device = self._ready_device()
        self.assertTrue(ui.country_scroll(self.phone, fling=False, reverse=True))
        args = device.swipe.call_args.args
        self.assertEqual(args[0], args[2])
        self.assertTrue(100 < args[1] < args[3] < 650)
        self.assertGreater(args[3] - args[1], 150)

    def test_reverse_distance_tracks_four_visible_country_rows(self):
        start, end = ui.country_reverse_points(100, 650,
                                                [125 + 50 * i for i in range(10)])
        self.assertEqual(end - start, 200)
        self.assertTrue(100 < start < end < 650)

    def test_gentle_reverse_is_shorter_and_moves_from_top_to_bottom(self):
        centers = [125 + 50 * i for i in range(10)]
        regular = ui.country_reverse_points(100, 650, centers)
        gentle = ui.country_reverse_points(100, 650, centers, gentle=True)
        self.assertEqual(gentle[1] - gentle[0], 50)  # At most one visible row.
        triple = ui.country_reverse_points(100, 650, centers, gentle=True,
                                           distance_multiplier=3)
        self.assertEqual(triple[1] - triple[0], 3 * (gentle[1] - gentle[0]))
        device = self._ready_device()
        self.assertTrue(ui.country_scroll(self.phone, fling=False, reverse=True,
                                          gentle=True))
        _, y1, _, y2 = device.swipe.call_args.args
        self.assertTrue(100 < y1 < y2 < 650)
        self.assertLess(y2 - y1, regular[1] - regular[0])
        self.assertEqual(device.swipe.call_args.kwargs["duration"], 0.65)

    def test_uncertain_native_swipe_is_not_repeated_by_adb_fallback(self):
        device = self._ready_device()
        device.swipe.side_effect = RuntimeError('delivery uncertain')
        with patch.object(flow, 'cloud_adb') as adb:
            flow._scroll_up(self.phone, [], AttemptDeadline(180), country_list=True, reverse=True)
        adb.assert_not_called()
        device.swipe.assert_called_once()

    def test_missing_native_container_uses_existing_fallback_without_gesture(self):
        device = self._ready_device(); device.dump_hierarchy.return_value = MENU
        self.assertFalse(ui.country_scroll(self.phone, fling=True, reverse=False))
        device.swipe.assert_not_called()
        device.return_value.fling.toEnd.assert_not_called()

    def test_empty_warmup_hierarchy_falls_back_instead_of_claiming_wrong_app(self):
        device = Mock(); device.dump_hierarchy.return_value = '<hierarchy />'
        with patch.object(ui, '_connect', return_value=device):
            self.assertIsNone(ui.read_tree(self.phone))
        device.stop_uiautomator.assert_called_once_with(wait=False)


if __name__ == '__main__':
    unittest.main()
