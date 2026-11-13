import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import patch
from amazon_android import account_flow as flow
from amazon_android.cloud import CloudPhone
from amazon_android.post_menu import AttemptDeadline
from amazon_android import runner
from amazon_android.core import AMAZON_PACKAGE, ToolError


class ExtendedRecoveryTests(unittest.TestCase):
    def test_stop_during_menu_read_does_not_send_navigation(self):
        from amazon_android import home_menu as menu
        stop = threading.Event()
        def read(*args, **kwargs):
            stop.set()
            return [{'content-desc': 'Browse menu Tab', 'bounds': '[0,0][50,50]'}]
        with patch.object(menu, '_nodes', side_effect=read), patch.object(menu, '_tap') as tap:
            with self.assertRaisesRegex(ToolError, 'Đã dừng'):
                menu.open_home_menu(CloudPhone('127.0.0.1:5001'), stop=stop)
        tap.assert_not_called()

    def test_read_recovery_keeps_deadline_and_does_not_retry_wrong_account(self):
        phone = CloudPhone('127.0.0.1:5001')
        clock = [0.0]
        def fail(*args):
            clock[0] += 1
            raise flow._UiReadIncomplete('temporary')
        with patch.object(flow.time, 'monotonic', side_effect=lambda: clock[0]), \
             patch.object(flow, '_read_nodes_once', side_effect=fail):
            with self.assertRaisesRegex(ToolError, 'Hết thời gian'):
                flow._read_nodes(phone, AttemptDeadline(2, started=0), threading.Event())
        with patch.object(flow, '_read_nodes_once', side_effect=ToolError('SĐT không khớp')) as read:
            with self.assertRaisesRegex(ToolError, 'không khớp'):
                flow._read_nodes(phone, AttemptDeadline(10), threading.Event())
        self.assertEqual(read.call_count, 1)

    def test_app_store_wait_recovers_stale_control_tree(self):
        from amazon_android import swarmote_desktop as sw
        from types import SimpleNamespace
        control = SimpleNamespace(element_info=SimpleNamespace(name='App Store', control_type='TabItem'))
        with patch.object(sw, '_descendants', side_effect=[RuntimeError('stale provider'), [control]]), \
             patch.object(sw.time, 'sleep'):
            sw._wait_for(object(), 'App Store', 'TabItem', seconds=2)

    def test_menu_read_failure_is_retried_without_new_tap(self):
        from amazon_android import home_menu as menu
        with patch.object(menu, '_nodes', side_effect=[menu.MenuReadUnavailable('temporary'),
                         [{'package': AMAZON_PACKAGE, 'text': 'Shop by category'}]]), patch.object(menu, '_tap') as tap:
            self.assertEqual(menu.open_home_menu(CloudPhone('127.0.0.1:5001'), timeout=3)['stage'],
                             'HOME_MENU_OPEN')
        tap.assert_not_called()

    def test_start_timeout_observes_delivered_start_without_sending_again(self):
        with patch.object(runner, 'start_profile', side_effect=ToolError('response lost')) as start, \
             patch.object(runner, 'profile_status', return_value={'state': 'Running', 'device_id': 'ACN1'}):
            result = runner._start_and_confirm('q1', 'ACN1', threading.Event())
        self.assertEqual(result['state'], 'Running')
        start.assert_called_once()

    def test_start_recovery_does_not_accept_another_device(self):
        stop = threading.Event()
        with patch.object(runner, 'start_profile', side_effect=ToolError('response lost')), \
             patch.object(runner, 'profile_status', return_value={'state': 'Running', 'device_id': 'OTHER'}):
            with self.assertRaises(ToolError):
                runner._start_and_confirm('q1', 'ACN1', stop)

    def test_twelve_phones_recover_four_read_failures_without_manual_continue(self):
        counts = {}
        def read(phone, deadline, stop):
            counts[phone.serial] = counts.get(phone.serial, 0) + 1
            if counts[phone.serial] <= 4:
                raise flow._UiReadIncomplete('temporary')
            return [{'serial': phone.serial}]
        phones = [CloudPhone(f'127.0.0.1:{5001+i}') for i in range(12)]
        with patch.object(flow, '_read_nodes_once', side_effect=read):
            with ThreadPoolExecutor(max_workers=12) as pool:
                results = list(pool.map(lambda p: flow._read_nodes(p, AttemptDeadline(15), threading.Event()), phones))
        self.assertEqual(results, [[{'serial': p.serial}] for p in phones])

    def test_transition_keeps_observing_after_short_wait_without_tapping(self):
        reads = [0]
        def read(*args):
            reads[0] += 1
            return []
        def classify(_nodes):
            return 'SMS' if reads[0] >= 5 else 'UNKNOWN'
        with patch.object(flow, '_read_nodes', side_effect=read), \
             patch.object(flow, 'screen', side_effect=classify), \
             patch('amazon_android.account_flow.threading.Event.wait', return_value=False), \
             patch.object(flow, 'cloud_adb') as adb:
            flow._wait_screen(CloudPhone('127.0.0.1:5001'), {'SMS'},
                              AttemptDeadline(None), threading.Event(), seconds=2)
        self.assertEqual(reads[0], 5)
        adb.assert_not_called()
