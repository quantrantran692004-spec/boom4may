"""Exercise real worker COM apartments without touching a desktop or phone."""
import ctypes
import queue
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from types import SimpleNamespace
from unittest.mock import patch

from amazon_android.desktop import Window
from amazon_android.runner import RunJob, _prepare_phone


def apartment_type():
    apartment, qualifier = ctypes.c_int(), ctypes.c_int()
    result = ctypes.OleDLL('ole32').CoGetApartmentType(
        ctypes.byref(apartment), ctypes.byref(qualifier))
    if result != 0:
        raise RuntimeError(f'CoGetApartmentType failed: {result}')
    return apartment.value


class PreparationThreadsTests(unittest.TestCase):
    def test_app_store_panel_closes_after_amazon_opens_before_menu(self):
        from worker_helpers import on_worker
        actions = []
        registry = SimpleNamespace(get=lambda *a: {'stage': 'APP_INSTALLED'},
                                   mark=lambda *a, **k: None)
        with patch('amazon_android.runner.open_adb_shell',
                   return_value={'serial': '127.0.0.1:5001'}), \
             patch('amazon_android.runner.show_apps'), \
             patch('amazon_android.runner.open_amazon',
                   side_effect=lambda _phone: actions.append('amazon')), \
             patch('amazon_android.runner.collapse_apps_panel',
                   side_effect=lambda *_a, **_k: actions.append('collapse')), \
             patch('amazon_android.runner.open_home_menu',
                   side_effect=lambda *_a, **_k: actions.append('menu') or
                   {'stage': 'HOME_MENU_OPEN'}):
            result = on_worker(_prepare_phone, RunJob(0, 'test', None), 'q1',
                               'ACN1', registry, lambda *_e: None, threading.Event())
        self.assertEqual(result, 'done')
        self.assertEqual(actions, ['amazon', 'collapse', 'menu'])

    def test_com_initialization_failure_marks_the_row_instead_of_leaving_running(self):
        from worker_helpers import on_worker
        registry = SimpleNamespace(mark=lambda *a, **kw: None)
        events = []
        with patch('pythoncom.CoInitializeEx', side_effect=RuntimeError('COM unavailable')):
            result = on_worker(_prepare_phone, RunJob(0, 'test', None), 'q1', 'ACN1',
                               registry, lambda *e: events.append(e), threading.Event())
        self.assertEqual(result, 'error')
        self.assertEqual(events[-1][2:], ('error', 'q1'))

    def test_twelve_phone_workers_use_mta_and_preserve_progress_row(self):
        barrier = threading.Barrier(12, timeout=5)
        observed, events = {}, []
        stop = threading.Event()

        def install(name, device_id=None, stop=None, progress=None):
            observed[name] = (apartment_type(), device_id)
            barrier.wait()
            if progress:
                progress('Đang mở Apps')

        registry = SimpleNamespace(get=lambda *a: {'stage': 'STARTED'}, mark=lambda *a, **k: None)
        with patch('amazon_android.runner.install_amazon', side_effect=install), \
             patch('amazon_android.runner.open_adb_shell', side_effect=lambda name, device_id, **kw:
                   {'serial': f'127.0.0.1:{5000 + int(name[1:])}'}), \
             patch('amazon_android.runner.show_apps'), \
             patch('amazon_android.runner.open_amazon'), \
             patch('amazon_android.runner.collapse_apps_panel'), \
             patch('amazon_android.runner.open_home_menu', return_value={'stage': 'HOME_MENU_OPEN'}):
            with ThreadPoolExecutor(max_workers=12) as pool:
                futures = [pool.submit(_prepare_phone, RunJob(i, 'test', None),
                    f'q{i+1}', f'ACN{i+1}', registry, lambda *e: events.append(e), stop)
                    for i in range(12)]
                self.assertEqual([f.result(timeout=10) for f in futures], ['done'] * 12)
        self.assertEqual(observed, {f'q{i}': (1, f'ACN{i}') for i in range(1, 13)})
        progress_rows = {(e[0], e[3]) for e in events if 'Đang mở Apps' in e[1]}
        self.assertEqual(progress_rows, {(i, f'q{i+1}') for i in range(12)})

    def test_coordinator_uses_same_mta_model_as_phone_workers(self):
        observed = []
        context = {'registry': None, 'events': queue.Queue(), 'stop': threading.Event(),
                   'serials': {}, 'opened': {}, 'group': 12, 'hide': False}

        def run(*a, **kw):
            observed.append(apartment_type())
            return {'menu_open': 0, 'error': 0, 'stopped': 0}

        with patch('amazon_android.desktop.run_batch', side_effect=run):
            with ThreadPoolExecutor(max_workers=1) as pool:
                pool.submit(Window._run, Window.__new__(Window), [], context).result(timeout=5)
        self.assertEqual(observed, [1])


if __name__ == '__main__':
    unittest.main()
