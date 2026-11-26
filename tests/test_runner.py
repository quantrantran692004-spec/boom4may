import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest.mock import patch

from amazon_android.core import ToolError
from amazon_android.profile_registry import ProfileRegistry
from amazon_android.runner import AccountData, RunJob, run_batch
from amazon_android.swarmote_desktop import (ProfileCreateNotSubmitted,
    ProfileManagerWindowError, ProfileNotFound, ProfileStartNotSubmitted,
    ProxyConfig)


class RunnerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.registry = ProfileRegistry(Path(self.temp.name) / "profiles.json")
        proxy = ProxyConfig("socks5", "proxy.example", 1001, "user", "secret")
        self.jobs = [RunJob(i, "batch", proxy) for i in range(3)]
        self.existing = set()
        self.running = set()
        self.calls = []
        self.stop = threading.Event()

    def status(self, name):
        if name not in self.existing:
            raise ProfileNotFound(name)
        return {"profile_name": name,
                "state": "Running" if name in self.running else "Offline",
                "device_id": f"ACN{name}"}

    def create(self, name, _proxy):
        self.calls.append(f"create:{name}")
        self.existing.add(name)

    def start(self, name, *, wait=True):
        self.calls.append(f"start:{name}")
        self.running.add(name)
        return {"state": "Running" if wait else "Starting",
                "device_id": f"ACN{name}"}

    def install(self, name, device_id=None, stop=None, progress=None):
        self.calls.append(f"install:{name}")
        return {"amazon_package_installed": True}

    def group_start(self, names):
        self.calls.append("group:" + ",".join(names))
        return {name: {"state": "Running"} for name in names}

    def execute(self, jobs=None, start_group_size=1, auto_close=True,
                hide_profile_creation=False, menu_ready=None, stop_after_step=None,
                proxy_prefix_ready=None, create_result=None,
                trace_preparation=False, manual_slots=None, manual_override=False,
                automatic_start_slots=None):
        events = []
        def shell(name, device_id, **kwargs):
            if trace_preparation:
                self.calls.append('shell')
            return {"serial": f"127.0.0.1:{5000 + int(name[1:])}",
                    "device_id": device_id}

        def menu(phone, **kwargs):
            if trace_preparation:
                self.calls.append('menu')
            if auto_close:
                self.running.discard(f"q{int(phone.serial.rsplit(':', 1)[1]) - 5000}")
            return {"stage": "HOME_MENU_OPEN"}

        def create(name, proxy, **kwargs):
            if hide_profile_creation:
                self.assertEqual(kwargs, {"hide_window": True})
            else:
                self.assertEqual(kwargs, {})
            self.create(name, proxy)
            return create_result(name) if create_result else None

        with patch("amazon_android.runner.profile_status", self.status), \
             patch("amazon_android.runner.visible_profile_names",
                   side_effect=lambda: set(self.existing)), \
             patch("amazon_android.runner.create_profile", side_effect=create), \
             patch("amazon_android.runner.start_profile", self.start), \
             patch("amazon_android.runner.install_amazon", self.install), \
             patch("amazon_android.runner.open_adb_shell", side_effect=shell), \
             patch("amazon_android.runner.show_apps",
                   side_effect=lambda *_a, **_k: self.calls.append('apps')
                   if trace_preparation else None), \
             patch("amazon_android.runner.open_amazon",
                   side_effect=lambda *_a, **_k: self.calls.append('open')
                   if trace_preparation else None), \
             patch("amazon_android.runner.collapse_apps_panel",
                   side_effect=lambda *_a, **_k: self.calls.append('collapse')
                   if trace_preparation else None), \
             patch("amazon_android.runner.open_home_menu", side_effect=menu):
            result = run_batch(jobs or self.jobs, self.registry,
                               lambda *event: events.append(event), self.stop,
                               start_group_size=start_group_size,
                               hide_profile_creation=hide_profile_creation,
                               menu_ready=menu_ready,
                               proxy_prefix_ready=proxy_prefix_ready,
                               stop_after_step=stop_after_step,
                               manual_slots=manual_slots,
                               manual_override=manual_override,
                               automatic_start_slots=automatic_start_slots)
        return result, events

    def test_two_running_slots_start_next_phone_when_one_closes(self):
        result, events = self.execute(start_group_size=2)
        self.assertEqual(result['menu_open'], 3)
        self.assertEqual(result['created'], 3)
        self.assertEqual(result['stopped'], 0)
        self.assertEqual([call for call in self.calls if call.startswith('start:')],
                         ['start:q1', 'start:q2', 'start:q3'])
        self.assertEqual(self.registry.get('batch', 2)['state'], 'DONE')

    def test_manual_continue_starts_third_after_automatic_two_are_used(self):
        self.execute(self.jobs[:2], start_group_size=2)
        result, _ = self.execute(
            self.jobs[2:], start_group_size=2,
            automatic_start_slots=frozenset({0, 1}),
            manual_slots={('batch', 2)}, manual_override=True)
        self.assertEqual(result['menu_open'], 1)
        self.assertEqual(self.calls.count('start:q3'), 1)

    def test_fresh_install_uses_existing_tunnel_and_reaches_menu_before_panel_cleanup(self):
        def install(name, device_id=None, **_kwargs):
            self.calls.append(f'install:{name}')
            return {'amazon_package_installed': True,
                    'serial': '127.0.0.1:5001', 'device_id': device_id}
        with patch.object(self, 'install', side_effect=install):
            result, _ = self.execute(self.jobs[:1], trace_preparation=True)
        self.assertEqual(result['menu_open'], 1)
        self.assertEqual(self.calls[-4:], ['install:q1', 'open', 'menu', 'collapse'])

    def test_opens_first_phone_before_creating_second_profile(self):
        result, _ = self.execute()
        self.assertEqual(result["menu_open"], 3)
        self.assertLess(self.calls.index("start:q1"), self.calls.index("create:q2"))

    def test_passed_proxy_postal_prefix_is_kept_per_machine_without_blocking_missing_value(self):
        captured = {}
        result, _ = self.execute(self.jobs[:3],
            proxy_prefix_ready=lambda slot, prefix: captured.__setitem__(slot, prefix),
            create_result=lambda name: {'address_search_prefix':
                                         {'q1': '3654', 'q2': None, 'q3': '9021'}[name]})
        self.assertEqual(result['menu_open'], 3)
        self.assertEqual(captured, {0: '3654', 2: '9021'})

    def test_twelve_jobs_create_start_install_and_reach_their_own_menu(self):
        jobs = [RunJob(i, 'batch', self.jobs[0].proxy) for i in range(12)]
        ready = []
        result, events = self.execute(jobs, start_group_size=12,
                                      menu_ready=lambda *args: ready.append(args))
        self.assertEqual(result['menu_open'], 12)
        self.assertEqual(result['error'], 0)
        self.assertEqual(sorted((r[0], r[1], r[3]) for r in ready),
                         [(i, f'q{i+1}', f'127.0.0.1:{5001+i}') for i in range(12)])
        for i in range(1, 13):
            for action in ('create', 'start', 'install'):
                self.assertEqual(self.calls.count(f'{action}:q{i}'), 1)

    def test_menu_callback_carries_the_correct_phone_serial(self):
        ready = []
        result, _ = self.execute(self.jobs[:2],
                                 menu_ready=lambda *item: ready.append(item))
        self.assertEqual(result["menu_open"], 2)
        self.assertEqual(sorted(ready), [
            (0, "q1", "ACNq1", "127.0.0.1:5001"),
            (1, "q2", "ACNq2", "127.0.0.1:5002"),
        ])

    def test_existing_q2_menu_reconnects_its_serial_before_done(self):
        item = self.registry.reserve("batch", 1, self.status)
        self.existing.add("q2")
        self.running.add("q2")
        self.registry.mark("batch", 1, "DONE", device_id="ACNq2",
                           stage="MENU_OPEN")
        account_job = RunJob(1, "batch", self.jobs[1].proxy,
                             account=AccountData(
                                 "12025550124", "Second User", "Example456!",
                                 "https://apifc.net/smsrecord?token=q2"))
        ready = []
        result, events = self.execute([account_job], auto_close=False,
                                      menu_ready=lambda *args: ready.append(args))
        self.assertEqual(result["menu_open"], 1)
        self.assertEqual(ready, [(1, "q2", "ACNq2", "127.0.0.1:5002")])
        self.assertEqual(events[-1][2], "done")
        self.assertNotIn("install:q2", self.calls)

    def test_existing_q2_menu_offline_does_not_claim_automation_started(self):
        self.registry.reserve("batch", 1, self.status)
        self.existing.add("q2")
        self.registry.mark("batch", 1, "DONE", device_id="ACNq2",
                           stage="MENU_OPEN")
        ready = []
        result, events = self.execute([self.jobs[1]],
                                      menu_ready=lambda *args: ready.append(args))
        self.assertEqual(result["stopped"], 1)
        self.assertEqual(ready, [])
        self.assertEqual(events[-1][2], "stopped")

    def test_hidden_creation_setting_only_changes_create_call(self):
        result, _ = self.execute(self.jobs[:1], hide_profile_creation=True)
        self.assertEqual(result["created"], 1)
        self.assertEqual(result["menu_open"], 1)
        self.assertIn("start:q1", self.calls)

    def test_fresh_fixed_name_is_checked_before_create(self):
        original_status = self.status
        checked = []

        def status(name):
            if name not in self.existing:
                checked.append(name)
            return original_status(name)

        with patch.object(self, "status", side_effect=status):
            result, _ = self.execute(self.jobs[:1])
        self.assertEqual(result["created"], 1)
        self.assertEqual(result["menu_open"], 1)
        self.assertEqual(checked, ["q1"])

    def test_manager_window_error_stops_batch_before_reserving_more_names(self):
        def unavailable(_name, _proxy):
            try:
                raise ProfileManagerWindowError("two manager windows")
            except ProfileManagerWindowError as exc:
                raise ProfileCreateNotSubmitted(str(exc)) from exc

        with patch.object(self, "create", side_effect=unavailable):
            result, _ = self.execute()
        self.assertEqual(result["error"], 1)
        self.assertEqual(result["stopped"], 2)
        self.assertIsNone(self.registry.get("batch", 1))
        self.assertIsNone(self.registry.get("batch", 2))

    def test_transient_manager_focus_error_retries_same_profile_before_next(self):
        attempts = []
        original = self.create
        def create(name, proxy):
            attempts.append(name)
            if name == 'q1' and attempts.count(name) < 3:
                raise ProfileCreateNotSubmitted(
                    'Không đưa được cửa sổ quản lý Swarmote lên trước để bấm New Profile')
            original(name, proxy)
        with patch.object(self, 'create', side_effect=create), \
             patch.object(self.stop, 'wait', return_value=False):
            result, events = self.execute(self.jobs[:2], start_group_size=2)
        self.assertEqual(attempts, ['q1', 'q1', 'q1', 'q2'])
        self.assertEqual(result['error'], 0)
        self.assertEqual(result['menu_open'], 2)
        self.assertTrue(any('tranh cửa sổ' in event[1] for event in events))

    def test_creates_second_profile_while_first_phone_is_installing(self):
        second_created = threading.Event()
        first_install_started = threading.Event()
        original_create = self.create
        original_install = self.install

        def create(name, proxy):
            if name == "q2":
                self.assertTrue(first_install_started.wait(3),
                                "q2 creation did not overlap q1 installation")
            original_create(name, proxy)
            if name == "q2":
                second_created.set()

        def install(name, device_id=None, stop=None, progress=None):
            if name == "q1":
                first_install_started.set()
                self.assertTrue(second_created.wait(3), "q2 creation waited for q1 install")
            return original_install(name, device_id=device_id)

        with patch.object(self, "create", side_effect=create), \
             patch.object(self, "install", side_effect=install):
            result, _ = self.execute(self.jobs[:2], start_group_size=2)
        self.assertTrue(first_install_started.is_set())
        self.assertEqual(result["menu_open"], 2)

    def test_next_phone_waits_until_user_closes_a_running_phone(self):
        third_created = threading.Event()
        original_create = self.create
        result = {}

        def create(name, proxy):
            original_create(name, proxy)
            if name == "q3":
                third_created.set()

        def run():
            with patch.object(self, "create", side_effect=create):
                result["summary"], result["events"] = self.execute(
                    start_group_size=2, auto_close=False)

        thread = threading.Thread(target=run, daemon=True)
        thread.start()
        self.assertTrue(third_created.wait(3))
        self.assertNotIn("start:q3", self.calls)
        self.running.discard("q1")  # User closes a phone in Swarmote.
        thread.join(6)
        self.assertFalse(thread.is_alive())
        self.assertIn("start:q3", self.calls)
        self.assertEqual(result["summary"]["menu_open"], 3)

    def test_stop_releases_waiting_batch_without_starting_next_phone(self):
        third_created = threading.Event()
        original_create = self.create
        result = {}

        def create(name, proxy):
            original_create(name, proxy)
            if name == "q3":
                third_created.set()

        def run():
            with patch.object(self, "create", side_effect=create):
                result["summary"], _ = self.execute(start_group_size=2, auto_close=False)

        thread = threading.Thread(target=run, daemon=True)
        thread.start()
        self.assertTrue(third_created.wait(3))
        self.stop.set()
        thread.join(6)
        self.assertFalse(thread.is_alive())
        self.assertNotIn("start:q3", self.calls)
        self.assertEqual(self.registry.get("batch", 2)["state"], "STOPPED")

    def test_selected_phone_stop_does_not_block_other_profiles(self):
        selected_stop = threading.Event()
        selected_stop.set()
        summary, events = self.execute(start_group_size=2,
                                       stop_after_step={1: selected_stop})
        self.assertEqual(summary["menu_open"], 2)
        self.assertEqual(summary["stopped"], 1)
        self.assertNotIn("create:q2", self.calls)
        self.assertIn("start:q3", self.calls)
        self.assertTrue(any(event[0] == 1 and event[2] == "stopped"
                            for event in events))

    def test_stop_waiting_phone_starts_next_phone_when_slot_opens(self):
        created_q3 = threading.Event()
        selected_stop = threading.Event()
        original_create = self.create
        result = {}

        def create(name, proxy):
            original_create(name, proxy)
            if name == "q3":
                created_q3.set()

        def run():
            with patch.object(self, "create", side_effect=create):
                result["summary"], result["events"] = self.execute(
                    start_group_size=1, auto_close=False,
                    stop_after_step={1: selected_stop})

        thread = threading.Thread(target=run, daemon=True)
        thread.start()
        self.assertTrue(created_q3.wait(3))
        selected_stop.set()
        self.running.discard("q1")
        thread.join(6)
        self.assertFalse(thread.is_alive())
        self.assertNotIn("start:q2", self.calls)
        self.assertIn("start:q3", self.calls)
        self.assertEqual(self.registry.get("batch", 1)["state"], "STOPPED")
        self.assertEqual(result["summary"]["stopped"], 1)

    def test_continue_respects_running_phones_from_same_batch(self):
        first, _ = self.execute(self.jobs[:2], start_group_size=2, auto_close=False)
        self.assertEqual(first["menu_open"], 2)
        item = self.registry.reserve("batch", 2, self.status)
        self.create(item["name"], self.jobs[2].proxy)
        self.registry.mark("batch", 2, "READY", device_id="ACNq3",
                           stage="PROFILE_CONFIRMED")
        result = {}

        def resume():
            result["summary"], _ = self.execute(self.jobs[2:], start_group_size=2,
                                                auto_close=False)

        thread = threading.Thread(target=resume, daemon=True)
        thread.start()
        time.sleep(0.3)
        self.assertNotIn("start:q3", self.calls)
        self.running.discard("q1")
        thread.join(6)
        self.assertFalse(thread.is_alive())
        self.assertIn("start:q3", self.calls)
        self.assertEqual(result["summary"]["menu_open"], 1)

    def test_manual_running_phone_does_not_use_an_automatic_slot(self):
        for index in (0, 1, 2):
            item = self.registry.reserve('batch', index, self.status)
            self.create(item['name'], self.jobs[index].proxy)
            self.registry.mark('batch', index, 'READY', device_id=f'ACN{item["name"]}',
                               stage='PROFILE_CONFIRMED')
        self.running.update({'q1', 'q2'})
        result, _ = self.execute(self.jobs[2:], start_group_size=2,
                                 auto_close=False, manual_slots={('batch', 1)})
        self.assertEqual(result['menu_open'], 1)
        self.assertIn('start:q3', self.calls)
        self.assertEqual(self.running, {'q1', 'q2', 'q3'})

    def test_manual_override_starts_when_two_automatic_phones_are_running(self):
        for index in (0, 1, 2):
            item = self.registry.reserve('batch', index, self.status)
            self.create(item['name'], self.jobs[index].proxy)
            self.registry.mark('batch', index, 'READY', device_id=f'ACN{item["name"]}',
                               stage='PROFILE_CONFIRMED')
        self.running.update({'q1', 'q2'})
        result, _ = self.execute(self.jobs[2:], start_group_size=2,
                                 auto_close=False, manual_slots={('batch', 2)},
                                 manual_override=True)
        self.assertEqual(result['menu_open'], 1)
        self.assertIn('start:q3', self.calls)

    def test_queued_phone_claimed_by_continue_is_not_started_by_automatic_runner(self):
        for index in (0, 1, 2):
            item = self.registry.reserve('batch', index, self.status)
            self.create(item['name'], self.jobs[index].proxy)
            self.registry.mark('batch', index, 'READY', device_id=f'ACN{item["name"]}',
                               stage='PROFILE_CONFIRMED')
        self.running.update({'q1', 'q2'})
        manual_slots = set()
        result = {}
        def automatic():
            result['summary'], _ = self.execute(self.jobs[2:], start_group_size=2,
                                                 auto_close=False,
                                                 manual_slots=manual_slots)
        thread = threading.Thread(target=automatic, daemon=True)
        thread.start()
        time.sleep(.2)
        manual_slots.add(('batch', 2))
        thread.join(5)
        self.assertFalse(thread.is_alive())
        self.assertNotIn('start:q3', self.calls)
        self.assertEqual(result['summary']['stopped'], 0)
        self.assertEqual(self.registry.get('batch', 2)['state'], 'READY')

    def test_full_resume_counts_running_profiles_before_starting_waiter(self):
        for index in range(3):
            item = self.registry.reserve("batch", index, self.status)
            self.existing.add(item["name"])
            self.registry.mark("batch", index,
                               "DONE" if index < 2 else "READY",
                               device_id=f"ACN{item['name']}",
                               stage="MENU_OPEN" if index < 2 else "PROFILE_CONFIRMED")
        self.running.update({"q1", "q2"})
        result = {}

        def resume():
            result["summary"], _ = self.execute(start_group_size=2, auto_close=False)

        thread = threading.Thread(target=resume, daemon=True)
        thread.start()
        time.sleep(0.3)
        self.assertNotIn("start:q3", self.calls)
        self.running.discard("q1")
        thread.join(6)
        self.assertFalse(thread.is_alive())
        self.assertIn("start:q3", self.calls)

    def test_settings_limit_starts_only_confirmed_profiles(self):
        result, _ = self.execute(start_group_size=12)
        self.assertEqual(result["menu_open"], 3)
        self.assertEqual({call for call in self.calls if call.startswith("start:")},
                         {"start:q1", "start:q2", "start:q3"})

    def test_limit_two_eventually_starts_all_when_closed(self):
        result, _ = self.execute(start_group_size=2)
        self.assertEqual(result["menu_open"], 3)
        self.assertIn("start:q1", self.calls)
        self.assertIn("start:q2", self.calls)
        self.assertIn("start:q3", self.calls)

    def test_limit_two_waits_for_shutdown_then_starts_both_queued_phones(self):
        jobs = [RunJob(i, "batch", self.jobs[0].proxy) for i in range(4)]
        result = {}

        def run():
            result["summary"], _ = self.execute(jobs, start_group_size=2,
                                                auto_close=False)

        worker = threading.Thread(target=run, daemon=True)
        worker.start()
        until = time.monotonic() + 5
        while time.monotonic() < until and "create:q4" not in self.calls:
            time.sleep(0.02)
        self.assertIn("create:q4", self.calls)
        self.assertNotIn("start:q3", self.calls)
        self.assertNotIn("start:q4", self.calls)
        self.running.difference_update({"q1", "q2"})
        worker.join(7)
        self.assertFalse(worker.is_alive())
        self.assertEqual(result["summary"]["menu_open"], 4)
        self.assertIn("start:q3", self.calls)
        self.assertIn("start:q4", self.calls)

    def test_start_button_not_ready_retries_without_continue(self):
        jobs = [RunJob(i, "batch", self.jobs[0].proxy) for i in range(4)]
        ordinary_start = self.start
        attempts = 0

        def delayed_start(name, *, wait=True):
            nonlocal attempts
            if name == "q3":
                attempts += 1
                if attempts == 1:
                    raise ProfileStartNotSubmitted("nút Start chưa sẵn sàng")
            return ordinary_start(name, wait=wait)

        with patch.object(self, "start", side_effect=delayed_start):
            result, events = self.execute(jobs, start_group_size=2)
        self.assertEqual(result["menu_open"], 4)
        self.assertEqual(result["error"], 0)
        self.assertEqual(attempts, 2)
        self.assertEqual(self.calls.count("start:q4"), 1)
        self.assertTrue(any(index == 2 and state == "queued" and
                            "tự thử lại" in message
                            for index, message, state, _ in events))

    def test_failed_start_still_creates_remaining_profiles(self):
        def failed_start(name, *, wait=True):
            self.calls.append("start:" + name)
            raise ToolError("selection failed")

        with patch.object(self, "start", side_effect=failed_start):
            result, events = self.execute(start_group_size=2)
        self.assertEqual(result["error"], 1)
        self.assertEqual(result["stopped"], 2)
        self.assertIn("create:q3", self.calls)
        self.assertNotIn("start:q2", self.calls)
        self.assertTrue(any(e[0] == 2 and e[2] == "stopped" for e in events))

    def test_failed_create_does_not_retry_and_other_rows_continue(self):
        normal_create = self.create
        def create(name, proxy):
            if name == "q2":
                self.calls.append("create:q2")
                raise ToolError("uncertain")
            normal_create(name, proxy)
        with patch.object(self, "create", side_effect=create):
            result, events = self.execute()
        self.assertEqual(result["menu_open"], 2)
        self.assertEqual(result["error"], 1)
        self.assertEqual(self.registry.get("batch", 1)["state"], "UNCERTAIN")
        self.assertNotIn("start:q2", self.calls)
        self.assertTrue(any(e[0] == 1 and e[2] == "uncertain" for e in events))

    def test_continue_after_install_skips_second_install(self):
        normal_install = self.install
        def install_then_stop(name, device_id=None, stop=None, progress=None):
            normal_install(name, device_id=device_id)
            self.stop.set()
        with patch.object(self, "install", side_effect=install_then_stop):
            result, _ = self.execute(self.jobs[:1])
        self.assertEqual(result["stopped"], 1)
        self.assertEqual(self.registry.get("batch", 0)["stage"], "APP_INSTALLED")
        self.stop.clear()
        result, _ = self.execute(self.jobs[:1])
        self.assertEqual(result["menu_open"], 1)
        self.assertEqual(self.calls.count("create:q1"), 1)
        self.assertEqual(self.calls.count("install:q1"), 1)

    def test_proxy_test_failure_is_known_not_submitted(self):
        def failed(_name, _proxy):
            raise ProfileCreateNotSubmitted("Test Failed")
        with patch.object(self, "create", side_effect=failed):
            result, events = self.execute(self.jobs[:1])
        item = self.registry.get("batch", 0)
        self.assertEqual((item["state"], item["stage"]), ("ERROR", "RESERVED"))
        self.assertEqual(item["last_error"], "Test Failed")
        self.assertEqual(result["error"], 1)
        self.assertTrue(any(e[2] == "error" for e in events))


if __name__ == "__main__":
    unittest.main()
