"""Real install/Apps/Terminal flow; only OS and Android boundaries are faked."""
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from types import SimpleNamespace
from unittest.mock import patch

from amazon_android.swarmote_desktop import install_amazon
from test_swarmote_install import FakeControl


class PhoneWindow:
    def __init__(self, number):
        self.number = self.handle = number
        self.page = 'launcher'
        self.search = ''
        self.install_count = 0
        self.shell_on = False

    def controls(self):
        apps, terminal = FakeControl('Apps', 'Text'), FakeControl('Terminal', 'Text')
        apps.parent = lambda: FakeControl('', 'Group', invoke=lambda: setattr(self, 'page', 'apps'))
        terminal.parent = lambda: FakeControl('', 'Group', invoke=lambda: setattr(self, 'page', 'terminal'))
        result = [apps, terminal]
        if self.page == 'apps':
            edit = FakeControl('Enter content', 'Edit')
            edit.iface_value = SimpleNamespace(SetValue=lambda v: setattr(self, 'search', v))
            result += [FakeControl('App Store', 'TabItem'), edit]
            if self.search == 'z':
                result += [FakeControl('Amazon Shopping', 'Text', (100, 100, 200, 120)),
                           FakeControl('Install', 'Button', (220, 105, 270, 140),
                                       invoke=lambda: setattr(self, 'install_count', self.install_count+1))]
        elif self.page == 'terminal':
            tab = FakeControl('ADB Shell', 'TabItem')
            tab.iface_selection_item = SimpleNamespace(Select=lambda: setattr(self, 'shell_on', True))
            result.append(tab)
            if self.shell_on:
                result += [FakeControl('SHELL: On', 'Text'),
                           FakeControl(f'localhost:{5000 + self.number}', 'Text')]
        return result


class ParallelInstallTests(unittest.TestCase):
    def test_twelve_installs_keep_store_actions_and_adb_ports_on_their_own_phone(self):
        phones = {f'q{i}': PhoneWindow(i) for i in range(1, 13)}
        barrier = threading.Barrier(12, timeout=5)
        started, verified, messages = set(), set(), {name: [] for name in phones}
        lock = threading.Lock()

        def lookup(name, device_id, **kwargs):
            self.assertEqual(device_id, f'ACN{phones[name].number}')
            with lock:
                first = name not in started
                started.add(name)
            if first:
                barrier.wait()
            return phones[name]

        def package(phone, _package):
            number = int(phone.serial.rsplit(':', 1)[1]) - 5000
            target = phones[f'q{number}']
            self.assertEqual(target.install_count, 1)
            self.assertTrue(target.shell_on)
            with lock:
                verified.add(number)
            return '/data/app/amazon.apk'

        with patch('amazon_android.swarmote_desktop._phone_window', side_effect=lookup), \
             patch('amazon_android.swarmote_desktop._descendants', side_effect=lambda w: w.controls()), \
             patch('amazon_android.cloud.require_online'), \
             patch('amazon_android.cloud.package_path', side_effect=package):
            with ThreadPoolExecutor(max_workers=12) as pool:
                futures = {name: pool.submit(install_amazon, name, device_id=f'ACN{w.number}',
                           stop=threading.Event(), progress=messages[name].append) for name, w in phones.items()}
                results = {name: future.result(timeout=10) for name, future in futures.items()}
        self.assertEqual(verified, set(range(1, 13)))
        for name, result in results.items():
            self.assertEqual(result['profile_name'], name)
            self.assertTrue(result['amazon_package_installed'])
            self.assertTrue(any('Apps' in m for m in messages[name]))
            self.assertTrue(any('Android' in m for m in messages[name]))
            self.assertEqual(phones[name].page, 'apps')


if __name__ == '__main__':
    unittest.main()
