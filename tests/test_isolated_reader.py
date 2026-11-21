import os
import threading
import time
import unittest
from concurrent.futures import ThreadPoolExecutor
from amazon_android.isolated_reader import PhoneReader
from amazon_android.core import ToolError
from unittest.mock import patch


def fake_worker(connection, serial):
    try:
        while True:
            request, operation, budget, options = connection.recv()
            if operation == 'stall':
                time.sleep(30)
            elif operation == 'crash':
                return
            else:
                connection.send((request, serial, True, (serial, os.getpid())))
    except EOFError:
        pass


def production_worker_with_fake_android(connection, serial):
    from amazon_android.isolated_reader import _serve
    with patch('amazon_android.account_flow._read_nodes_once',
               side_effect=lambda phone, deadline, stop: [{'serial': phone.serial}]), \
         patch('amazon_android.account_flow._read_visual_nodes',
               side_effect=lambda phone, deadline, stop: [{'visual_serial': phone.serial}]), \
         patch('amazon_android.marketplace_flow._read_navigation_nodes',
               side_effect=lambda phone, deadline, stop: [{'navigation_serial': phone.serial}]), \
         patch('amazon_android.ui_backend.country_scroll', return_value=True):
        _serve(connection, serial)


class IsolationTests(unittest.TestCase):
    def test_production_server_routes_read_and_scroll_to_bound_phone(self):
        reader = PhoneReader('127.0.0.1:5003', target=production_worker_with_fake_android)
        try:
            self.assertEqual(reader.call('read', 15, threading.Event()), [{'serial': reader.serial}])
            self.assertEqual(reader.call('visual', 15, threading.Event()),
                             [{'visual_serial': reader.serial}])
            self.assertEqual(reader.call('navigation', 15, threading.Event()),
                             [{'navigation_serial': reader.serial}])
            self.assertTrue(reader.call('scroll', 5, threading.Event(), fling=True, reverse=False))
        finally:
            reader.close()

    def test_two_threads_cannot_claim_same_device(self):
        from amazon_android.isolated_reader import phone_reader
        def duplicate():
            with phone_reader('127.0.0.1:5001'):
                pass
        with phone_reader('127.0.0.1:5001'):
            with ThreadPoolExecutor(max_workers=1) as pool:
                with self.assertRaises(ToolError):
                    pool.submit(duplicate).result()

    def test_flow_uses_own_reader_and_rejects_a_different_serial(self):
        from amazon_android.isolated_reader import phone_reader
        from amazon_android.account_flow import _read_nodes_once
        from amazon_android.cloud import CloudPhone
        from amazon_android.post_menu import AttemptDeadline
        stop = threading.Event()
        with phone_reader('127.0.0.1:5001', stop) as reader:
            with patch.object(reader, 'call', return_value=[{'text': 'own screen'}]) as call:
                result = _read_nodes_once(CloudPhone(reader.serial), AttemptDeadline(180), stop)
                self.assertEqual(result, [{'text': 'own screen'}])
                self.assertEqual(call.call_args.args[0], 'read')
                with self.assertRaises(ToolError):
                    _read_nodes_once(CloudPhone('127.0.0.1:5002'), AttemptDeadline(180), stop)

    def test_twelve_processes_have_distinct_pids_and_fixed_serials(self):
        readers = [PhoneReader(f'127.0.0.1:{5001+i}', target=fake_worker) for i in range(12)]
        try:
            with ThreadPoolExecutor(max_workers=12) as pool:
                results = list(pool.map(lambda r: r.call('read', 20, threading.Event()), readers))
            self.assertEqual([r[0] for r in results], [r.serial for r in readers])
            self.assertEqual(len({r[1] for r in results}), 12)
            self.assertNotIn(os.getpid(), {r[1] for r in results})
        finally:
            for reader in readers:
                reader.close()

    def test_stalled_reader_is_stopped_without_blocking_another(self):
        bad = PhoneReader('127.0.0.1:5001', target=fake_worker)
        good = PhoneReader('127.0.0.1:5002', target=fake_worker)
        try:
            with self.assertRaises(ToolError):
                bad.call('stall', 0.4, threading.Event())
            self.assertIsNone(bad.process)
            result = good.call('read', 10, threading.Event())
            self.assertEqual(result[0], good.serial)
        finally:
            bad.close(); good.close()

    def test_cancel_before_request_does_not_start_process(self):
        reader = PhoneReader('127.0.0.1:5001', target=fake_worker)
        stop = threading.Event(); stop.set()
        with self.assertRaises(ToolError):
            reader.call('read', 5, stop)
        self.assertIsNone(reader.process)
