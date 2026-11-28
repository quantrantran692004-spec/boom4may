import unittest
import sys
from types import SimpleNamespace
from unittest.mock import patch

from amazon_android.core import ToolError
from amazon_android.swarmote_desktop import (
    ProfileCreateNotSubmitted, ProfileNotFound, ProxyConfig, ProxyTestFailed,
    _activate_manager, _create_profile_form, _open_profiles, profile_status, visible_profile_names,
)


def control(name, kind):
    return SimpleNamespace(element_info=SimpleNamespace(name=name, control_type=kind))


class ProfilesNavigationTests(unittest.TestCase):
    def test_transient_foreground_denial_retries_same_manager(self):
        handle = 42
        calls = []
        def foreground(target):
            calls.append(target)
            if len(calls) == 1:
                raise RuntimeError('Windows denied focus once')
        gui = SimpleNamespace(IsWindowVisible=lambda _: True, IsIconic=lambda _: False,
                              SetForegroundWindow=foreground,
                              GetForegroundWindow=lambda: handle if len(calls) > 1 else 0)
        window = SimpleNamespace(handle=handle, set_focus=lambda: self.fail('fallback not needed'))
        with patch.dict(sys.modules, {'win32gui': gui, 'win32con': SimpleNamespace()}), \
             patch('amazon_android.swarmote_desktop.time.sleep') as sleep:
            _activate_manager(window)
        self.assertEqual(calls, [handle, handle])
        sleep.assert_called_once_with(0.25)

    def test_visible_names_reads_table_without_typing_into_search(self):
        rows = [control("q5", "DataItem"), control("q6", "DataItem"),
                control("Profile 3", "DataItem")]
        with patch("amazon_android.swarmote_desktop._main_window", return_value=object()), \
             patch("amazon_android.swarmote_desktop._open_profiles"), \
             patch("amazon_android.swarmote_desktop._descendants", return_value=rows), \
             patch("amazon_android.swarmote_desktop._set_value") as set_value:
            self.assertEqual(visible_profile_names(), {"q5", "q6"})
        set_value.assert_not_called()

    def test_status_finds_profile_hidden_on_another_page_and_restores_filter(self):
        window = object()
        row = object()
        current = {"filter": ""}
        search = SimpleNamespace(iface_value=SimpleNamespace(CurrentValue=""))
        q2 = SimpleNamespace(element_info=SimpleNamespace(name="q2", control_type="DataItem"),
                             parent=lambda: row)

        def descendants(_w):
            return [q2] if current["filter"] == "q2" else []

        def set_value(_w, _name, _kind, value):
            current["filter"] = value

        with patch("amazon_android.swarmote_desktop._main_window", return_value=window), \
             patch("amazon_android.swarmote_desktop._open_profiles"), \
             patch("amazon_android.swarmote_desktop._descendants", side_effect=descendants), \
             patch("amazon_android.swarmote_desktop._one", return_value=search), \
             patch("amazon_android.swarmote_desktop._set_value", side_effect=set_value), \
             patch("amazon_android.swarmote_desktop._profile_row_status",
                   return_value={"profile_name": "q2", "state": "Running"}):
            status = profile_status("q2")
        self.assertEqual(status["state"], "Running")
        self.assertEqual(current["filter"], "")

    def test_single_page_absence_does_not_type_into_profile_search(self):
        window = object()
        search = control("Profile Name", "Edit")
        search.iface_value = SimpleNamespace(CurrentValue="")
        previous = control("Go to previous page", "Button")
        following = control("Go to next page", "Button")
        previous.is_enabled = following.is_enabled = lambda: False
        controls = [search, previous, following, control("Total 4", "Text"),
                    control("Existing Profile", "DataItem")]
        with patch("amazon_android.swarmote_desktop._main_window", return_value=window), \
             patch("amazon_android.swarmote_desktop._open_profiles"), \
             patch("amazon_android.swarmote_desktop._descendants", return_value=controls), \
             patch("amazon_android.swarmote_desktop._set_value") as set_value:
            with self.assertRaises(ProfileNotFound):
                profile_status("q4")
        set_value.assert_not_called()

    def test_creation_opens_new_profile_before_filling_name(self):
        window = object()
        form = {"open": False}
        calls = []

        def descendants(_window):
            if not form["open"]:
                return [control("New Profile", "Button")]
            return [control("Create", "Button"), control("Single Create", "RadioButton"),
                    control("Profile Name", "Edit"), control("ip/Host", "Edit"),
                    control("Test Passed", "Text"), control("Country", "Text"),
                    control("United States (US)", "Text")]

        def invoke(_window, name):
            calls.append(name)
            if name == "New Profile":
                form["open"] = True

        with patch("amazon_android.swarmote_desktop._main_window", return_value=window), \
             patch("amazon_android.swarmote_desktop._descendants", side_effect=descendants), \
             patch("amazon_android.swarmote_desktop._open_profiles"), \
             patch("amazon_android.swarmote_desktop._activate_manager"), \
             patch("amazon_android.swarmote_desktop._invoke", side_effect=invoke), \
             patch("amazon_android.swarmote_desktop._wait_for"), \
             patch("amazon_android.swarmote_desktop._select_radio"), \
             patch("amazon_android.swarmote_desktop._set_value") as set_value:
            result = _create_profile_form("q4", ProxyConfig("socks5", "proxy.example", 1001))
        self.assertTrue(result["created"])
        self.assertEqual(calls, ["New Profile", "Test Proxy", "Create"])
        set_value.assert_any_call(window, "Profile Name", "Edit", "q4")

    def test_retry_closes_form_with_old_proxy_result(self):
        window = object()
        state = {"form": True, "result": "Test Failed"}
        calls = []
        def descendants(_window):
            if not state["form"]:
                return [control("New Profile", "Button")]
            return [control("Create", "Button"), control("Single Create", "RadioButton"),
                    control("Profile Name", "Edit"), control("ip/Host", "Edit"),
                    control(state["result"], "Text"), control("Country", "Text"),
                    control("United States (US)", "Text")]
        def invoke(_window, name):
            calls.append(name)
            if name == "Cancel":
                state["form"] = False
            elif name == "New Profile":
                state["form"] = True
                state["result"] = ""
            elif name == "Test Proxy":
                state["result"] = "Test Passed"
        with patch("amazon_android.swarmote_desktop._main_window", return_value=window), \
             patch("amazon_android.swarmote_desktop._descendants", side_effect=descendants), \
             patch("amazon_android.swarmote_desktop._open_profiles"), \
             patch("amazon_android.swarmote_desktop._activate_manager"), \
             patch("amazon_android.swarmote_desktop._invoke", side_effect=invoke), \
             patch("amazon_android.swarmote_desktop._wait_for"), \
             patch("amazon_android.swarmote_desktop._select_radio"), \
             patch("amazon_android.swarmote_desktop._set_value"):
            result = _create_profile_form("q4", ProxyConfig("socks5", "proxy.example", 1001))
        self.assertTrue(result["created"])
        self.assertEqual(calls, ["Cancel", "New Profile", "Test Proxy", "Create"])

    def test_passed_proxy_outside_us_or_without_country_never_creates(self):
        for country in ("Canada (CA)", None):
            with self.subTest(country=country):
                calls = []
                window = object()
                form_open = False

                def descendants(_window):
                    if not form_open:
                        return [control("New Profile", "Button")]
                    result = [control("Create", "Button"), control("Single Create", "RadioButton"),
                              control("Profile Name", "Edit"), control("ip/Host", "Edit"),
                              control("Test Passed", "Text")]
                    if country is not None:
                        result.extend([control("Country", "Text"), control(country, "Text")])
                    return result

                def invoke(_window, name):
                    nonlocal form_open
                    calls.append(name)
                    if name == "New Profile":
                        form_open = True

                with patch("amazon_android.swarmote_desktop._main_window", return_value=window), \
                     patch("amazon_android.swarmote_desktop._descendants", side_effect=descendants), \
                     patch("amazon_android.swarmote_desktop._open_profiles"), \
                     patch("amazon_android.swarmote_desktop._activate_manager"), \
                     patch("amazon_android.swarmote_desktop._invoke", side_effect=invoke), \
                     patch("amazon_android.swarmote_desktop._wait_for"), \
                     patch("amazon_android.swarmote_desktop._select_radio"), \
                     patch("amazon_android.swarmote_desktop._set_value"):
                    with self.assertRaises(ProxyTestFailed):
                        _create_profile_form("q4", ProxyConfig("socks5", "proxy.example", 1001))
                self.assertEqual(calls, ["New Profile", "Test Proxy"])

    def test_country_may_appear_after_test_passed(self):
        calls = []
        state = {"form": False, "tested": False, "reads": 0}

        def descendants(_window):
            if not state["form"]:
                return [control("New Profile", "Button")]
            result = [control("Create", "Button"), control("Single Create", "RadioButton"),
                      control("Profile Name", "Edit"), control("ip/Host", "Edit")]
            if state["tested"]:
                result.append(control("Test Passed", "Text"))
                state["reads"] += 1
                if state["reads"] > 1:
                    result.extend([control("Country", "Text"),
                                   control("United States (US)", "Text")])
            return result

        def invoke(_window, name):
            calls.append(name)
            if name == "New Profile":
                state["form"] = True
            elif name == "Test Proxy":
                state["tested"] = True

        with patch("amazon_android.swarmote_desktop._main_window", return_value=object()), \
             patch("amazon_android.swarmote_desktop._descendants", side_effect=descendants), \
             patch("amazon_android.swarmote_desktop._open_profiles"), \
             patch("amazon_android.swarmote_desktop._activate_manager"), \
             patch("amazon_android.swarmote_desktop._invoke", side_effect=invoke), \
             patch("amazon_android.swarmote_desktop._wait_for"), \
             patch("amazon_android.swarmote_desktop._select_radio"), \
             patch("amazon_android.swarmote_desktop._set_value"):
            result = _create_profile_form("q4", ProxyConfig("socks5", "proxy.example", 1001))
        self.assertTrue(result["created"])
        self.assertEqual(calls, ["New Profile", "Test Proxy", "Create"])
        self.assertGreaterEqual(state["reads"], 2)

    def test_new_profile_noop_stops_before_typing_in_search(self):
        window = object()
        with patch("amazon_android.swarmote_desktop._main_window", return_value=window), \
             patch("amazon_android.swarmote_desktop._descendants",
                   return_value=[control("New Profile", "Button")]), \
             patch("amazon_android.swarmote_desktop._open_profiles"), \
             patch("amazon_android.swarmote_desktop._activate_manager"), \
             patch("amazon_android.swarmote_desktop._invoke"), \
             patch("amazon_android.swarmote_desktop._wait_for"), \
             patch("amazon_android.swarmote_desktop._set_value") as set_value:
            with self.assertRaisesRegex(ProfileCreateNotSubmitted, "chưa mở đúng form"):
                _create_profile_form("q4", ProxyConfig("socks5", "proxy.example", 1001))
        set_value.assert_not_called()

    def test_compact_sidebar_uses_visible_new_profile_button(self):
        window = object()
        controls = [control("", "MenuItem"), control("New Profile", "Button")]
        with patch("amazon_android.swarmote_desktop._descendants", return_value=controls), \
             patch("amazon_android.swarmote_desktop._wait_for") as wait:
            _open_profiles(window)
        wait.assert_not_called()

    def test_waits_for_profiles_page_to_finish_loading(self):
        window = object()
        controls = [control("swarmote · admin · common · profiles", "Document")]
        with patch("amazon_android.swarmote_desktop._descendants", return_value=controls), \
             patch("amazon_android.swarmote_desktop._wait_for") as wait:
            _open_profiles(window)
        wait.assert_called_once_with(window, "New Profile", "Button", seconds=10)

    def test_unknown_page_reports_actionable_error(self):
        with patch("amazon_android.swarmote_desktop._descendants", return_value=[]):
            with self.assertRaisesRegex(ToolError, "mở danh sách Profiles"):
                _open_profiles(object())


if __name__ == "__main__":
    unittest.main()
