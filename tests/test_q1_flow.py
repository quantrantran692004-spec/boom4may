import threading
import unittest
from types import SimpleNamespace
from subprocess import TimeoutExpired
from unittest.mock import patch

from PIL import Image, ImageDraw

from amazon_android.cloud import CloudPhone
from amazon_android.core import AMAZON_PACKAGE, ToolError
from amazon_android.post_menu import AttemptDeadline, PostMenuSession, RecoverableStepError
from amazon_android.account_flow import (
    _ScreenWaitExpired, _button, _find_scrolling, _national_phone, _parse_ui_nodes, _read_nodes, _scroll_up, _unique,
    build_common_steps, menu_layout, resume_common_index,
    route_list_menu, screen, _yellow_form_button,
)
from amazon_android.q1_flow import build_q1_steps
from amazon_android.q2_flow import build_q2_steps
from amazon_android.runner import AccountData, RunJob


def node(text, *, bounds="[10,10][200,50]", kind="android.widget.TextView"):
    return {"text": text, "bounds": bounds, "class": kind}


class Q1FlowTests(unittest.TestCase):
    def test_b9_retries_continue_after_dismissing_visible_keyboard(self):
        field = node(self.job.account.full_name, kind="android.widget.EditText",
                     bounds="[30,210][350,250]")
        form = [node("Create account"), node("First and last name"), field]
        action = node("Continue", bounds="[35,470][345,520]")
        duplicate = node("Continue", bounds="[35,530][345,580]")
        b9 = next(step.action for step in build_common_steps(self.phone, lambda _: None)
                  if step.name.startswith("b9"))
        with patch("amazon_android.account_flow._read_nodes",
                   side_effect=[form + [action, duplicate], form + [action]]), \
             patch("amazon_android.account_flow._check_summary") as check, \
             patch("amazon_android.account_flow._wait_screen"), \
             patch("amazon_android.account_flow.cloud_adb",
                   return_value=SimpleNamespace(stdout="mInputShown=true")) as adb, \
             patch("amazon_android.account_flow._tap") as tap:
            b9(self.job, self.deadline, self.stop)
        self.assertEqual(adb.call_args.args[1:], ("shell", "input", "keyevent", "KEYCODE_BACK"))
        self.assertEqual(check.call_count, 2)
        self.assertEqual(tap.call_count, 1)
        self.assertIs(tap.call_args.args[1], action)

    def test_b8_recognizes_create_form_with_incomplete_accessibility_labels(self):
        controls = [node("Mobile number"), node("Continue"),
                    node("", kind="android.widget.EditText")]
        for landmark in (node("First and last name:"),
                         dict(node("Amazon"), **{"content-desc": "Create an account"})):
            with self.subTest(landmark=landmark):
                self.assertEqual(screen(controls + [landmark]), "CREATE_FORM")
        self.assertNotEqual(screen(controls), "CREATE_FORM")
        self.assertNotEqual(screen(controls + [node("First and last name"),
                          node("", kind="android.widget.EditText")]), "CREATE_FORM")

    def test_b8_resumes_on_create_form_without_tapping_again(self):
        form = [node("First and last name:"), node("Mobile number"), node("Continue"),
                node("", kind="android.widget.EditText")]
        b8 = next(step.action for step in build_common_steps(self.phone, lambda _: None)
                  if step.name.startswith("b8"))
        with patch("amazon_android.account_flow._read_nodes", return_value=form), \
             patch("amazon_android.account_flow._tap") as tap:
            b8(self.job, self.deadline, self.stop)
        tap.assert_not_called()

    def setUp(self):
        self.phone = CloudPhone("127.0.0.1:5001")
        self.job = RunJob(0, "batch", None, account=AccountData(
            "12025550123", "Example User", "Example456!",
            "https://apifc.net/smsrecord?token=q1"))
        self.deadline = AttemptDeadline(180)
        self.stop = threading.Event()

    def test_classifies_supported_screens_and_stops_on_unknown(self):
        cases = [
            (["Shop by category."], "MENU"),
            (["Sign In", "Customer Service"], "MENU"),
            (["Sign in or create account", "Enter mobile number or email"],
             "IDENTIFIER"),
            (["Country/region code", "United States +1"], "COUNTRY"),
            (["Looks like you are new to Amazon", "Proceed to create an account"],
             "NEW_ACCOUNT"),
            (["Create account", "First and last name"], "CREATE_FORM"),
            (["Verify with WhatsApp", "Send code by SMS"], "WHATSAPP"),
            (["Verify mobile number", "Enter security code"], "SMS"),
            (["Something unexpected"], "UNKNOWN"),
        ]
        for labels, expected in cases:
            with self.subTest(expected=expected):
                self.assertEqual(screen([node(label) for label in labels]), expected)

    def test_list_menu_uses_live_text_structure_for_all_connected_machines(self):
        listed = [node(label) for label in (
            "Shop by Category", "Books", "Electronics", "Home services",
            "See all", "Customer Service", "Sign In")]
        cards = [node(label) for label in (
            "Shop by category", "Gifting", "Pets", "Fashion and Beauty")]
        self.assertEqual(menu_layout(listed), "LIST")
        self.assertEqual(menu_layout(cards), "CARDS")
        for factory in (build_q1_steps, build_q2_steps):
            steps = factory(self.phone, lambda _code: None)
            session = PostMenuSession("batch", 0, "q1")
            with patch("amazon_android.account_flow._read_nodes",
                       return_value=listed), \
                 patch("amazon_android.account_flow.visit_home") as home:
                target = route_list_menu(self.phone, steps, 0, session,
                                         self.deadline, self.stop)
            self.assertEqual(steps[target].name, "b4 Sign In")
            self.assertEqual(session.menu_route, "LIST")
            home.assert_called_once()
            with patch("amazon_android.account_flow._read_nodes",
                       return_value=cards), \
                 patch("amazon_android.account_flow.visit_home") as home:
                self.assertIsNone(route_list_menu(
                    self.phone, steps, 0, session, self.deadline, self.stop))
            self.assertEqual(session.menu_route, "")
            home.assert_not_called()

    def test_list_route_recovers_if_home_was_already_opened(self):
        steps = build_q2_steps(self.phone, lambda _code: None)
        session = PostMenuSession("batch", 1, "q2")
        session.menu_route = "LIST"
        home_nodes = [node("Sign in for the best experience")]
        with patch("amazon_android.account_flow._read_nodes",
                   return_value=home_nodes), \
             patch("amazon_android.account_flow.visit_home") as home:
            target = route_list_menu(self.phone, steps, 0, session,
                                     self.deadline, self.stop)
        self.assertEqual(steps[target].name, "b4 Sign In")
        home.assert_called_once()

    def test_shared_b4_returns_from_home_to_list_menu_sign_in(self):
        field = node("", kind="android.widget.EditText")
        focused_field = dict(field, focused="true")
        home = [node("Sign in for the best experience")]
        listed = [node(label) for label in (
            "Shop by Category", "Books", "Electronics", "Customer Service",
            "Sign In")]
        identifier = [node("Sign in or create account"),
                      node("Enter mobile number or email"), field]
        focused_identifier = identifier[:-1] + [focused_field]
        sign_in, focus = build_common_steps(self.phone, lambda _code: None)[:2]
        with patch("amazon_android.account_flow._read_nodes",
                   side_effect=[home, focused_identifier]), \
             patch("amazon_android.account_flow._ensure_menu",
                   return_value=listed) as ensure, \
             patch("amazon_android.account_flow._find_scrolling",
                   return_value=listed[-1]), \
             patch("amazon_android.account_flow._wait_screen",
                   return_value=identifier), \
             patch("amazon_android.account_flow._tap") as tap:
            sign_in.action(self.job, self.deadline, self.stop)
            tap.assert_called_once()
            focus.action(self.job, self.deadline, self.stop)
        ensure.assert_called_once()
        self.assertEqual(tap.call_count, 2)
        self.assertIs(tap.call_args_list[0].args[1], listed[-1])
        self.assertIs(tap.call_args_list[1].args[1], field)

    def test_b4_prefers_clickable_sign_in_when_tree_repeats_label(self):
        label = node("Sign In", bounds="[20,220][130,250]")
        row = node("Sign In", bounds="[20,530][340,580]",
                   kind="android.widget.Button")
        row["clickable"] = "true"
        menu = [node("Shop by Category"), node("Customer Service",
                                               bounds="[20,470][340,510]"),
                label, row]
        with patch("amazon_android.account_flow._read_nodes", return_value=menu):
            selected = _find_scrolling(self.phone, "Sign In", self.deadline,
                                       self.stop, menu_action=True)
        self.assertIs(selected, row)

    def test_b4_uses_customer_service_landmark_for_two_text_labels(self):
        other = node("Sign In", bounds="[20,220][130,250]")
        menu_row = node("Sign In", bounds="[20,530][340,580]")
        menu = [node("Shop by Category"), node("Customer Service",
                                               bounds="[20,470][340,510]"),
                other, menu_row]
        with patch("amazon_android.account_flow._read_nodes", return_value=menu):
            selected = _find_scrolling(self.phone, "Sign In", self.deadline,
                                       self.stop, menu_action=True)
        self.assertIs(selected, menu_row)

    def test_b4_stops_if_two_sign_in_rows_remain_below_landmark(self):
        menu = [node("Shop by Category"),
                node("Customer Service", bounds="[20,470][340,510]"),
                node("Sign In", bounds="[20,530][340,580]"),
                node("Sign In", bounds="[20,590][340,640]")]
        with patch("amazon_android.account_flow._read_nodes", return_value=menu):
            with self.assertRaises(ToolError):
                _find_scrolling(self.phone, "Sign In", self.deadline,
                                self.stop, menu_action=True)

    def test_ambiguous_button_stops_instead_of_guessing(self):
        with self.assertRaises(ToolError):
            _unique([node("Continue", bounds="[0,0][100,40]"),
                     node("Continue", bounds="[0,50][100,90]")], "Continue")

    def test_accessibility_description_can_identify_a_button(self):
        button = {"text": "", "content-desc": "Send code by SMS",
                  "bounds": "[0,0][100,40]"}
        self.assertIs(_unique([button], "Send code by SMS"), button)

    def test_visible_continue_is_chosen_over_hidden_duplicate(self):
        hidden = node("Continue", bounds="[0,0][0,0]")
        button = node("Continue", bounds="[20,470][350,520]",
                      kind="android.widget.Button")
        button["clickable"] = "true"
        field = node("", bounds="[30,210][350,250]",
                     kind="android.widget.EditText")
        self.assertIs(_button([hidden, button], "Continue", below=field), button)

    def test_name_continue_combines_nested_webview_controls(self):
        row = node("Continue", bounds="[20,470][350,520]")
        label = node("Continue", bounds="[140,480][230,510]")
        row["clickable"] = label["clickable"] = "true"
        field = node("Name", bounds="[30,210][350,250]")
        self.assertIs(_button([label, row], "Continue", below=field), row)

    def test_b9_selects_full_width_continue_among_separate_matches(self):
        field = node("Name", bounds="[30,210][350,250]")
        action = dict(node("Continue", bounds="[35,470][345,520]"), clickable="true")
        duplicate = dict(node("Continue", bounds="[120,525][240,555]"), clickable="true")
        self.assertIs(_button([duplicate, action], "Continue", below=field), action)
        another_action = dict(action, bounds="[35,530][345,580]")
        with self.assertRaises(ToolError):
            _button([action, another_action], "Continue", below=field)

    def test_b9_waits_for_name_readback_before_tapping_continue(self):
        action = node("Continue", bounds="[35,470][345,520]")
        heading = [node("Create account"), node("First and last name"), action]
        field = dict(node("", kind="android.widget.EditText",
                          bounds="[30,210][350,250]"), focused="false")
        focused_field = dict(field, focused="true")
        value = self.job.account.full_name
        snapshots = [heading + [field], heading + [focused_field],
                     heading + [dict(focused_field, text=value[:-1])],
                     heading + [dict(focused_field, text=value)]]
        b9 = next(step.action for step in build_common_steps(self.phone, lambda _: None)
                  if step.name.startswith("b9"))
        with patch("amazon_android.account_flow._read_nodes", side_effect=snapshots), \
             patch("amazon_android.account_flow._check_summary"), \
             patch("amazon_android.account_flow._wait_screen"), \
             patch("amazon_android.account_flow._tap") as tap, \
             patch("amazon_android.account_flow.type_characters") as typed:
            b9(self.job, self.deadline, self.stop)
        typed.assert_called_once()
        self.assertEqual([call.args[1] for call in tap.call_args_list], [field, action])

    def test_b9_resolves_two_xml_labels_to_one_clickable_parent(self):
        xml = f'''<hierarchy>
          <node package="{AMAZON_PACKAGE}" clickable="true" bounds="[35,470][345,520]">
            <node package="{AMAZON_PACKAGE}" text="Continue" bounds="[120,478][240,500]" />
            <node package="{AMAZON_PACKAGE}" content-desc="Continue" bounds="[116,483][244,510]" />
          </node>
        </hierarchy>'''
        nodes = _parse_ui_nodes(xml)
        field = node("Name", bounds="[30,210][350,250]")
        self.assertIs(_button(nodes, "Continue", below=field), nodes[0])

    def test_country_scrolls_past_hidden_us_entry(self):
        hidden = node("United States +1", bounds="[0,0][0,0]")
        visible = node("United States +1", bounds="[50,320][320,360]")
        with patch("amazon_android.account_flow._read_nodes",
                   side_effect=[[hidden, node("Ukraine +380")], [visible]]), \
             patch("amazon_android.account_flow._scroll_up") as scroll:
            result = _find_scrolling(self.phone, "United States +1",
                                     self.deadline, self.stop)
        self.assertIs(result, visible)
        scroll.assert_called_once()

    def test_b6_open_country_list_scrolls_before_tapping_us(self):
        country = [node("Country/region code")]
        hidden = node("United States +1", bounds="[0,0][0,0]")
        visible = node("United States +1", bounds="[50,320][320,360]")
        confirmed = [node("Sign in or create account"),
                     node("Enter mobile number or email"), node("US +1")]
        action = next(step.action for step in build_common_steps(
            self.phone, lambda _code: None) if step.name.startswith("b6"))
        with patch("amazon_android.account_flow._read_nodes",
                   side_effect=[country + [hidden], country + [visible],
                                country + [visible], confirmed]), \
             patch("amazon_android.account_flow._scroll_up") as scroll, \
             patch("amazon_android.account_flow._tap") as tap, \
             patch("amazon_android.account_flow._wait_screen",
                   return_value=confirmed):
            action(self.job, self.deadline, self.stop)
        scroll.assert_called_once()
        self.assertIs(tap.call_args.args[1], visible)

    def test_b6_checks_stable_us_row_and_recovers_from_sg_selection(self):
        heading = [node("Country/region code")]
        form = [node("Sign in or create account"), node("Enter mobile number or email")]
        moving = node("United States +1", bounds="[50,300][320,340]")
        settled = node("United States +1", bounds="[50,320][320,360]")
        sg = node("SG +65")
        end = heading + [node("Zimbabwe +263")]
        action = next(step.action for step in build_common_steps(self.phone, lambda _: None)
                      if step.name.startswith("b6"))
        with patch("amazon_android.account_flow._read_nodes", side_effect=[
                heading + [moving], heading + [settled], heading + [settled],
                form + [sg], heading + [settled], heading + [settled],
                form + [node("US +1")]]), \
             patch("amazon_android.account_flow._wait_screen", side_effect=[
                 end]), \
             patch("amazon_android.account_flow._scroll_up") as scroll, \
             patch("amazon_android.account_flow._tap") as tap, \
             patch.object(self.stop, "wait", return_value=False):
            action(self.job, self.deadline, self.stop)
        self.assertEqual([call.args[1] for call in tap.call_args_list], [settled, sg, settled])
        self.assertFalse(scroll.call_args.kwargs["fling"])
        self.assertTrue(scroll.call_args.kwargs["reverse"])

    def test_reads_current_ui_again_after_adb_timeout(self):
        error = ToolError("ADB timeout")
        error.__cause__ = TimeoutExpired("adb", 6)
        current = [node("United States +1")]
        with patch("amazon_android.account_flow._read_nodes_once",
                   side_effect=[error, current]) as read:
            self.assertEqual(_read_nodes(self.phone, self.deadline, self.stop), current)
        self.assertEqual(read.call_count, 2)

    def test_b6_long_swipe_stays_inside_country_list(self):
        region = node("", bounds="[40,120][340,720]")
        region["scrollable"] = "true"
        with patch("amazon_android.account_flow.cloud_adb") as adb:
            _scroll_up(self.phone, [region], self.deadline, country_list=True, fling=True)
        _, _, _, _, x1, y1, x2, y2, duration = adb.call_args.args
        self.assertEqual(x1, x2)
        self.assertTrue(40 < int(x1) < 340)
        self.assertTrue(120 < int(y2) < int(y1) < 720)
        self.assertGreater(int(y1) - int(y2), 400)
        self.assertLessEqual(int(duration), 70)

    def test_b6_scrolls_back_if_fling_passes_us(self):
        target = node("United States +1")
        with patch("amazon_android.account_flow._read_nodes",
                   side_effect=[[node("Afghanistan +93")], [node("Japan +81")],
                                [node("Zimbabwe +263")], [node("Zimbabwe +263")],
                                [target]]), \
             patch("amazon_android.account_flow._scroll_up") as scroll, \
             patch.object(self.stop, "wait", return_value=False):
            self.assertIs(_find_scrolling(self.phone, "United States +1",
                                          self.deadline, self.stop,
                                          country_list=True), target)
        self.assertTrue(scroll.call_args_list[0].kwargs["fling"])
        self.assertTrue(scroll.call_args_list[1].kwargs["fling"])
        self.assertTrue(scroll.call_args_list[3].kwargs["reverse"])
        self.assertTrue(scroll.call_args_list[3].kwargs["gentle_reverse"])

    def test_b6_reverses_when_forward_swipe_no_longer_moves_list(self):
        last = [node("Yemen +967")]  # No known bottom landmark: detect unchanged rows.
        target = node("United States +1")
        with patch("amazon_android.account_flow._read_nodes",
                   side_effect=[[node("United Kingdom +44")], last, last, last, [target]]), \
             patch("amazon_android.account_flow._scroll_up") as scroll, \
             patch.object(self.stop, "wait", return_value=False):
            self.assertIs(_find_scrolling(self.phone, "United States +1",
                                          self.deadline, self.stop,
                                          country_list=True), target)
        self.assertFalse(scroll.call_args_list[0].kwargs["reverse"])
        self.assertEqual([call.kwargs["reverse"] for call in scroll.call_args_list[1:]],
                         [False, True, True])

    def test_b6_reaches_bottom_before_reversing_past_wallis(self):
        near_bottom = [node("United Kingdom +44"), node("Wallis and Futuna +681")]
        bottom = [node("Zimbabwe +263"), node("Åland Islands +358")]
        target = node("United States +1")
        with patch("amazon_android.account_flow._read_nodes",
                   side_effect=[[node("Afghanistan +93")], near_bottom,
                                bottom, bottom, [target]]), \
             patch("amazon_android.account_flow._scroll_up") as scroll, \
             patch.object(self.stop, "wait", return_value=False):
            result = _find_scrolling(self.phone, "United States +1", self.deadline,
                                     self.stop, country_list=True)
        self.assertIs(result, target)
        self.assertEqual([(call.kwargs["fling"], call.kwargs["reverse"])
                          for call in scroll.call_args_list],
                         [(True, False), (True, False), (False, True),
                          (False, True)])

    def test_b6_vietnam_at_bottom_gets_short_reverse_after_fling(self):
        target = node("United States +1")
        with patch("amazon_android.account_flow._read_nodes",
                   side_effect=[[node("Afghanistan +93")], [node("Vietnam +84")],
                                [node("Vietnam +84")], [target]]), \
             patch("amazon_android.account_flow._scroll_up") as scroll, \
             patch.object(self.stop, "wait", return_value=False):
            self.assertIs(_find_scrolling(self.phone, "United States +1",
                                          self.deadline, self.stop,
                                          country_list=True), target)
        self.assertEqual([(call.kwargs["fling"], call.kwargs["reverse"],
                           call.kwargs["gentle_reverse"])
                          for call in scroll.call_args_list],
                         [(True, False, False), (False, True, True),
                          (False, True, True)])
        self.assertTrue(scroll.call_args_list[-1].kwargs["force_adb"])

    def test_b6_resumed_at_vietnam_reverses_without_another_downward_fling(self):
        target = node("United States +1")
        for label in ("Vietnam", "Viet Nam", "Việt Nam"):
            with self.subTest(label=label), \
                 patch("amazon_android.account_flow._read_nodes",
                       side_effect=[[node(label)], [target]]), \
                 patch("amazon_android.account_flow._scroll_up") as scroll, \
                 patch.object(self.stop, "wait", return_value=False):
                self.assertIs(_find_scrolling(self.phone, "United States +1",
                                              self.deadline, self.stop,
                                              country_list=True), target)
                scroll.assert_called_once()
                self.assertTrue(scroll.call_args.kwargs["reverse"])
                self.assertTrue(scroll.call_args.kwargs["gentle_reverse"])
                self.assertFalse(scroll.call_args.kwargs["fling"])

    def test_b6_continues_short_reverse_when_first_swipe_misses_us(self):
        target = node("United States +1")
        vietnam = [node("Vietnam +84")]
        bottom = [node("Zimbabwe +263")]
        with patch("amazon_android.account_flow._read_nodes",
                   side_effect=[[node("Afghanistan +93")], vietnam, vietnam,
                                vietnam, bottom, bottom, [target]]), \
             patch("amazon_android.account_flow._scroll_up") as scroll, \
             patch.object(self.stop, "wait", return_value=False):
            self.assertIs(_find_scrolling(self.phone, "United States +1",
                                          self.deadline, self.stop,
                                          country_list=True), target)
        self.assertEqual([call.kwargs["gentle_reverse"]
                          for call in scroll.call_args_list],
                         [False, True, True, True, True, True])
        self.assertTrue(scroll.call_args_list[-1].kwargs["reverse"])
        self.assertFalse(scroll.call_args_list[-1].kwargs["fling"])
        self.assertEqual([call.kwargs["force_adb"] for call in scroll.call_args_list],
                         [False, True, True, True, True, True])

    def test_b6_gentle_reverse_adb_stays_inside_country_list(self):
        region = node("", bounds="[40,120][340,720]")
        region["scrollable"] = "true"
        vietnam = node("Vietnam +84", bounds="[50,650][300,690]")
        with patch("amazon_android.isolated_reader.current", return_value=None), \
             patch("amazon_android.account_flow.ui_backend.country_scroll",
                   return_value=False), \
             patch("amazon_android.account_flow.cloud_adb") as adb:
            _scroll_up(self.phone, [region, vietnam], self.deadline,
                       country_list=True, reverse=True, gentle_reverse=True)
        _, _, _, _, x1, y1, x2, y2, duration = adb.call_args.args
        self.assertEqual(x1, x2)
        self.assertTrue(40 < int(x1) < 340)
        self.assertTrue(120 < int(y1) < int(y2) < 720)
        self.assertLess(int(y2) - int(y1), 200)
        self.assertEqual(duration, "650")

    def test_b6a_reverse_adb_distance_is_three_times_b6b(self):
        region = dict(node("", bounds="[40,120][340,720]"), scrollable="true")
        vietnam = node("Vietnam +84", bounds="[50,650][300,690]")
        with patch("amazon_android.isolated_reader.current", return_value=None), \
             patch("amazon_android.account_flow.ui_backend.country_scroll", return_value=False), \
             patch("amazon_android.account_flow.cloud_adb") as adb:
            _scroll_up(self.phone, [region, vietnam], self.deadline,
                       country_list=True, reverse=True, gentle_reverse=True,
                       force_adb=True)
            b6b = adb.call_args.args
            _scroll_up(self.phone, [region, vietnam], self.deadline,
                       country_list=True, reverse=True, gentle_reverse=True,
                       force_adb=True, first_reverse_triple=True)
            b6a = adb.call_args.args
        self.assertEqual(int(b6a[7]) - int(b6a[5]),
                         3 * (int(b6b[7]) - int(b6b[5])))
        self.assertEqual(b6a[8], b6b[8])

    def test_b6_screenshot_bottom_swipes_once_then_selects_us_in_both_modes(self):
        from amazon_android.post_menu import RegistrationState
        region = dict(node('', bounds='[53,165][360,785]'), scrollable='true')
        rows = ['Uruguay +598', 'Uzbekistan +998', 'Vanuatu +678', 'Vatican City +39',
                'Venezuela +58', 'Vietnam +84', 'Wallis & Futuna +681',
                'Western Sahara +212', 'Yemen +967', 'Zambia +260',
                'Zimbabwe +263', 'Åland Islands +358']
        bottom = [node('Country/region code', bounds='[80,120][290,150]'), region] + [
            node(text, bounds=f'[80,{185+50*i}][310,{215+50*i}]')
            for i,text in enumerate(rows)]
        us = node('United States +1', bounds='[80,175][290,210]')
        found = [bottom[0], us, node('Uruguay +598', bounds='[80,225][310,260]')]
        confirmed = [node('Sign in or create account'), node('Enter mobile number or email'),
                     node('US +1')]
        for mode in ('create','login'):
            state = RegistrationState(flow_mode=mode)
            action = next(s.action for s in build_common_steps(self.phone, lambda _: None,
                                                               registration=state)
                          if s.name.startswith('b6'))
            reads = iter([bottom, found, found, confirmed]); events = []
            def read(*_a, **_k):
                events.append('read'); return next(reads)
            def adb(phone, *args, **_kwargs):
                self.assertEqual(phone, self.phone)
                self.assertEqual(args[:3], ('shell','input','swipe'))
                self.assertEqual(args[-1], '650')
                self.assertTrue(165 < int(args[4]) < int(args[6]) < 785)
                self.assertEqual(int(args[6])-int(args[4]), 150)
                events.append('reverse')
            with self.subTest(mode=mode), \
                 patch('amazon_android.account_flow._read_nodes', side_effect=read), \
                 patch('amazon_android.account_flow.cloud_adb', side_effect=adb), \
                 patch('amazon_android.account_flow.ui_backend.country_scroll',
                       side_effect=AssertionError('No second native read before reverse')), \
                 patch('amazon_android.account_flow._tap') as tap, \
                 patch.object(self.stop, 'wait', return_value=False):
                action(self.job, self.deadline, self.stop)
            self.assertEqual(events, ['read','reverse','read','read','read'])
            tap.assert_called_once_with(self.phone, us, self.deadline)
            self.assertFalse(state.country_reverse_started)

    def test_b6_stop_resume_keeps_reverse_direction_without_flinging_down_again(self):
        from amazon_android.post_menu import RegistrationState
        state = RegistrationState(); other = RegistrationState()
        target = node('United States +1')
        def paused(_seconds):
            self.stop.set(); return True
        with patch('amazon_android.account_flow._read_nodes', return_value=[node('Åland Islands +358')]), \
             patch('amazon_android.account_flow._scroll_up') as scroll, \
             patch.object(self.stop, 'wait', side_effect=paused):
            with self.assertRaisesRegex(ToolError,'Đã dừng'):
                _find_scrolling(self.phone,'United States +1',self.deadline,self.stop,
                                country_list=True,country_state=state)
        self.assertTrue(state.country_reverse_started)
        self.assertFalse(other.country_reverse_started)
        self.stop.clear()
        with patch('amazon_android.account_flow._read_nodes', side_effect=[
                    [node('United Kingdom +44'),node('Uruguay +598')],[target]]), \
             patch('amazon_android.account_flow._scroll_up') as scroll, \
             patch.object(self.stop,'wait',return_value=False):
            self.assertIs(_find_scrolling(self.phone,'United States +1',self.deadline,self.stop,
                                         country_list=True,country_state=state),target)
        scroll.assert_called_once()
        self.assertEqual((scroll.call_args.kwargs['fling'],scroll.call_args.kwargs['reverse'],
                          scroll.call_args.kwargs['force_adb']), (False,True,True))

    def test_b6b_second_gentle_pull_then_reads_us(self):
        from amazon_android.post_menu import RegistrationState
        state = RegistrationState(country_reverse_started=True,
                                  country_reverse_swipes=1)
        first = [node('Uruguay +598'), node('Vietnam +84')]
        us = node('United States +1')
        with patch('amazon_android.account_flow._read_nodes', return_value=[us]), \
             patch('amazon_android.account_flow._scroll_up') as scroll, \
             patch.object(self.stop, 'wait', return_value=False):
            found = _find_scrolling(self.phone, 'United States +1', self.deadline,
                                    self.stop, country_list=True, nodes=first,
                                    country_state=state)
        self.assertIs(found, us)
        scroll.assert_called_once()
        self.assertTrue(scroll.call_args.kwargs['gentle_reverse'])
        self.assertEqual(state.country_reverse_swipes, 2)

    def test_b6_bottom_nudges_before_selecting_us_at_top_edge(self):
        from amazon_android.post_menu import RegistrationState
        state = RegistrationState()
        us = node('United States +1', bounds='[80,166][290,190]')
        bottom = [node('Country/region code', bounds='[80,120][290,165]'), us,
                  node('Vietnam +84', bounds='[80,600][290,640]')]
        revealed = [node('Country/region code', bounds='[80,120][290,165]'),
                    node('United States +1', bounds='[80,210][290,245]')]
        with patch('amazon_android.account_flow._read_nodes', return_value=revealed), \
             patch('amazon_android.account_flow._scroll_up') as scroll, \
             patch.object(self.stop, 'wait', return_value=False):
            result = _find_scrolling(self.phone, 'United States +1', self.deadline,
                                     self.stop, country_list=True, nodes=bottom,
                                     country_state=state)
        self.assertEqual(result, revealed[1])
        scroll.assert_called_once()
        self.assertEqual((scroll.call_args.kwargs['fling'],
                          scroll.call_args.kwargs['reverse'],
                          scroll.call_args.kwargs['gentle_reverse']), (False, True, True))
        self.assertTrue(state.country_reverse_started)

    def test_b6_unreadable_country_pauses_after_three_reads_without_blind_swipes(self):
        from amazon_android.account_flow import _UiReadIncomplete
        from amazon_android.post_menu import PostMenuStep
        action = next(s.action for s in build_common_steps(self.phone, lambda _: None)
                      if s.name.startswith('b6'))
        session = PostMenuSession(self.job.batch_id,self.job.index,'q1')
        with patch('amazon_android.account_flow._read_nodes_once',
                   side_effect=_UiReadIncomplete('UI unavailable')) as read, \
             patch('amazon_android.account_flow._scroll_up') as scroll, \
             patch.object(self.stop,'wait',return_value=False):
            session.run(self.job,(PostMenuStep('b6 chọn US +1',action),),lambda *_:None,self.stop)
        self.assertEqual(session.state,'PAUSED')
        self.assertEqual(read.call_count,3)
        self.assertIn('ba lần',session.last_error)
        scroll.assert_not_called()

    def test_b6_unchanged_after_native_reverse_uses_adb_on_fresh_read(self):
        region = node("", bounds="[40,120][340,720]")
        region["scrollable"] = "true"
        vietnam = node("Vietnam +84", bounds="[50,650][300,690]")
        with patch("amazon_android.isolated_reader.current", return_value=None), \
             patch("amazon_android.account_flow.ui_backend.country_scroll") as native, \
             patch("amazon_android.account_flow.cloud_adb") as adb:
            _scroll_up(self.phone, [region, vietnam], self.deadline,
                       country_list=True, reverse=True, gentle_reverse=True,
                       force_adb=True)
        native.assert_not_called()
        self.assertEqual(adb.call_args.args[1:4], ("shell", "input", "swipe"))

    def test_phone_uses_input_digits_then_checks_us_national_number(self):
        self.assertEqual(_national_phone(self.job), "2025550123")

    def test_only_first_three_steps_are_q1_specific(self):
        q1 = build_q1_steps(self.phone, lambda code: None)
        common = build_common_steps(self.phone, lambda code: None)
        self.assertEqual([step.name for step in q1[:3]],
                         ["b1 Gifting", "b2 Pets", "b3 Fashion and Beauty"])
        self.assertEqual([step.name for step in q1[3:]],
                         [step.name for step in common])
        self.assertEqual(common[0].name, "b4 Sign In")

    def test_b4a_focuses_phone_field_on_existing_identifier_screen(self):
        field = node("", kind="android.widget.EditText")
        focused = dict(field, focused="true")
        identifier = [node("Sign in or create account"),
                      node("Continue"), field,
                      node("", kind="android.widget.EditText", bounds="[0,0][0,0]")]
        focus = build_common_steps(self.phone, lambda code: None)[1].action
        with patch("amazon_android.account_flow._read_nodes",
                   side_effect=[identifier, identifier[:-2] + [focused, identifier[-1]]]), \
             patch("amazon_android.account_flow._tap") as tap:
            focus(self.job, self.deadline, self.stop)
        self.assertIs(tap.call_args.args[1], field)

    def test_b5_retries_focus_before_typing_phone_number(self):
        field = dict(node("", kind="android.widget.EditText"), focused="false")
        focused = dict(field, focused="true")
        filled = dict(focused, text=self.job.account.phone)
        heading = [node("Sign in or create account"), node("Continue")]
        steps = build_common_steps(self.phone, lambda _code: None)
        actions = []
        with patch("amazon_android.account_flow._read_nodes", side_effect=[
                heading + [field], heading + [field], heading + [field],
                heading + [field], heading + [focused],
                heading + [filled]]), \
             patch("amazon_android.account_flow._tap",
                   side_effect=lambda *_: actions.append("tap")), \
             patch("amazon_android.account_flow.type_characters",
                   side_effect=lambda *_: actions.append("type")):
            steps[2].action(self.job, self.deadline, self.stop)
        self.assertEqual(actions, ["tap", "tap", "type"])

    def test_paused_q1_and_q2_rewind_from_b10_to_shared_b4(self):
        identifier = [node("Sign in or create account"),
                      node("Enter mobile number or email")]
        with patch("amazon_android.account_flow._read_nodes",
                   return_value=identifier):
            for factory in (build_q1_steps, build_q2_steps):
                steps = factory(self.phone, lambda code: None)
                current = next(i for i, step in enumerate(steps)
                               if step.name.startswith("b10"))
                target = resume_common_index(self.phone, steps, current,
                                             self.deadline, self.stop)
                self.assertEqual(steps[target].name, "b4 Sign In")

    def test_common_sms_steps_keep_each_machine_url_and_state(self):
        second = RunJob(1, "batch", None, account=AccountData(
            "12025550124", "Second User", "Example456!",
            "https://apifc.net/smsrecord?token=q2"))
        first_send = next(step.action for step in build_common_steps(
            self.phone, lambda code: None) if step.name.startswith("b10"))
        second_send = next(step.action for step in build_common_steps(
            CloudPhone("127.0.0.1:5002"), lambda code: None)
            if step.name.startswith("b10"))
        whatsapp = [node("Verify with WhatsApp"), node("Send code by SMS")]
        sms = [node("Verify mobile number"), node("Enter security code")]
        with patch("amazon_android.account_flow._read_nodes", return_value=whatsapp), \
             patch("amazon_android.account_flow._check_summary"), \
             patch("amazon_android.account_flow._tap") as tap, \
             patch("amazon_android.account_flow._wait_screen", return_value=sms):
            first_send(self.job, self.deadline, self.stop)
            second_send(second, self.deadline, self.stop)
        self.assertEqual(tap.call_count, 2)

    def test_b10_taps_sms_and_confirms_sms_screen_before_any_url_read(self):
        statuses = []
        action = next(step.action for step in build_common_steps(
            self.phone, lambda _code: None, statuses.append)
            if step.name.startswith("b10"))
        whatsapp = [node("Verify with WhatsApp"), node("Send code by SMS")]
        sms = [node("Verify mobile number"), node("Enter security code")]
        order = []
        with patch("amazon_android.account_flow._read_nodes",
                   return_value=whatsapp), \
             patch("amazon_android.account_flow._check_summary"), \
             patch("amazon_android.account_flow._tap",
                   side_effect=lambda *_: order.append("tap SMS")), \
             patch("amazon_android.account_flow._wait_screen",
                   side_effect=lambda *_args, **_kwargs:
                       (order.append("SMS screen") or sms)), \
             patch("amazon_android.account_flow.wait_for_new_otp") as read:
            action(self.job, self.deadline, self.stop)
        self.assertEqual(order, ["tap SMS", "SMS screen"])
        self.assertEqual(statuses, ["Đang chờ mã"])
        read.assert_not_called()

    def test_shared_steps_accept_direct_jump_from_b5_to_sms_without_earlier_taps(self):
        from amazon_android.post_menu import RegistrationState
        state = RegistrationState()
        sms = [node("Verify mobile number"), node("Enter security code"),
               node(self.job.account.phone)]
        steps = build_common_steps(self.phone, lambda _: None, registration=state)
        with patch("amazon_android.account_flow._read_nodes", return_value=sms), \
             patch("amazon_android.account_flow._tap") as tap:
            for step in steps[:8]:
                step.action(self.job, self.deadline, self.stop)
        tap.assert_not_called()
        self.assertIsNotNone(state.sms_requested_at)
        self.assertEqual(state.sms_tap_attempts, 0)

    def test_direct_sms_jump_with_another_phone_stops_before_otp(self):
        sms = [node("Verify mobile number"), node("Enter security code"),
               node("12025559999")]
        action = next(step.action for step in build_common_steps(self.phone, lambda _: None)
                      if step.name.startswith("b10"))
        with patch("amazon_android.account_flow._read_nodes", return_value=sms), \
             patch("amazon_android.account_flow._tap") as tap:
            with self.assertRaisesRegex(ToolError, "không khớp"):
                action(self.job, self.deadline, self.stop)
        tap.assert_not_called()

    def test_direct_sms_jump_accepts_phone_in_accessibility_description(self):
        sms = [node("Verify mobile number"), node("Enter security code"),
               {"content-desc": f"US +1 {self.job.account.phone}",
                "bounds": "[10,80][200,110]"}]
        action = next(step.action for step in build_common_steps(self.phone, lambda _: None)
                      if step.name.startswith("b10"))
        with patch("amazon_android.account_flow._read_nodes", return_value=sms), \
             patch("amazon_android.account_flow._tap") as tap:
            action(self.job, self.deadline, self.stop)
        tap.assert_not_called()

    def test_b7_accepts_direct_jump_to_whatsapp_after_continue(self):
        identifier = [node("Sign in or create account"),
                      node("Enter mobile number or email"), node("Continue"),
                      node("US +1"), node(self.job.account.phone)]
        whatsapp = [node("Verify with WhatsApp"), node("Send code by SMS"),
                    node(self.job.account.phone)]
        action = next(step.action for step in build_common_steps(self.phone, lambda _: None)
                      if step.name.startswith("b7"))
        with patch("amazon_android.account_flow._read_nodes",
                   side_effect=[identifier, whatsapp]), \
             patch("amazon_android.account_flow._tap_for_transition") as tap:
            action(self.job, self.deadline, self.stop)
        tap.assert_called_once()

    def test_b6_stops_scrolling_when_android_jumps_to_sms(self):
        sms = [node("Verify mobile number"), node("Enter security code"),
               node(self.job.account.phone)]
        with patch("amazon_android.account_flow._read_nodes", side_effect=[
                [node("Vietnam +84")], sms]), \
             patch("amazon_android.account_flow._scroll_up") as scroll:
            with self.assertRaises(RecoverableStepError):
                _find_scrolling(self.phone, "United States +1", self.deadline,
                                self.stop, country_list=True)
        scroll.assert_called_once()

    def test_b6_accepts_sms_while_country_picker_is_opening(self):
        identifier = [node("Sign in or create account"),
                      node("Enter mobile number or email"), node("Continue"),
                      node("SG +65"), node(self.job.account.phone)]
        sms = [node("Verify mobile number"), node("Enter security code"),
               node(self.job.account.phone)]
        action = next(step.action for step in build_common_steps(self.phone, lambda _: None)
                      if step.name.startswith("b6"))
        with patch("amazon_android.account_flow._read_nodes",
                   side_effect=[identifier, sms]), \
             patch("amazon_android.account_flow._tap_for_transition") as tap:
            action(self.job, self.deadline, self.stop)
        tap.assert_called_once()

    def test_b10_retries_once_only_after_same_phone_stays_on_whatsapp(self):
        from amazon_android.post_menu import RegistrationState
        state = RegistrationState()
        whatsapp = [node("Verify with WhatsApp"), node("Send code by SMS"),
                    node(self.job.account.phone)]
        sms = [node("Verify mobile number"), node("Enter security code"),
               node(self.job.account.phone)]
        action = next(step.action for step in build_common_steps(
            self.phone, lambda _: None, registration=state)
            if step.name.startswith("b10"))
        with patch("amazon_android.account_flow._read_nodes",
                   side_effect=[whatsapp, whatsapp]), \
             patch("amazon_android.account_flow._tap") as tap, \
             patch("amazon_android.account_flow._wait_screen",
                   side_effect=[_ScreenWaitExpired("still WhatsApp"), sms]):
            action(self.job, self.deadline, self.stop)
        self.assertEqual(tap.call_count, 2)
        self.assertEqual(state.sms_tap_attempts, 2)

    def test_b10_never_taps_a_third_time_after_two_uncertain_attempts(self):
        from amazon_android.post_menu import RegistrationState
        state = RegistrationState()
        whatsapp = [node("Verify with WhatsApp"), node("Send code by SMS"),
                    node(self.job.account.phone)]
        action = next(step.action for step in build_common_steps(
            self.phone, lambda _: None, registration=state)
            if step.name.startswith("b10"))
        with patch("amazon_android.account_flow._read_nodes", return_value=whatsapp), \
             patch("amazon_android.account_flow._tap") as tap, \
             patch("amazon_android.account_flow._wait_screen",
                   side_effect=_ScreenWaitExpired("still WhatsApp")):
            with self.assertRaisesRegex(ToolError, "hai lần"):
                action(self.job, self.deadline, self.stop)
            with self.assertRaisesRegex(ToolError, "hai lần"):
                action(self.job, self.deadline, self.stop)
        self.assertEqual(tap.call_count, 2)
        self.assertEqual(state.sms_tap_attempts, 2)

    def test_sms_is_not_sent_twice_after_uncertain_transition(self):
        steps = build_q1_steps(self.phone, lambda code: None)
        send_sms = next(step.action for step in steps if step.name.startswith("b10"))
        whatsapp = [node("Verify with WhatsApp"), node("Send code by SMS")]
        with patch("amazon_android.account_flow._read_nodes", return_value=whatsapp), \
             patch("amazon_android.account_flow._check_summary"), \
             patch("amazon_android.account_flow._tap") as tap, \
             patch("amazon_android.account_flow._wait_screen",
                   side_effect=ToolError("slow screen")):
            with self.assertRaises(ToolError):
                send_sms(self.job, self.deadline, self.stop)
            with self.assertRaisesRegex(ToolError, "slow screen"):
                send_sms(self.job, self.deadline, self.stop)
        tap.assert_called_once()

    def test_b10_stalled_whatsapp_pauses_only_affected_phone(self):
        whatsapp = [node("Verify with WhatsApp"), node("Send code by SMS")]
        sms = [node("Verify mobile number"), node("Enter security code")]
        first = PostMenuSession("batch", 0, "q1")
        second = PostMenuSession("batch", 1, "q2")
        first_step = next(step for step in build_common_steps(
            self.phone, lambda _: None, registration=first.registration)
            if step.name.startswith("b10"))
        second_phone = CloudPhone("127.0.0.1:5002")
        second_step = next(step for step in build_common_steps(
            second_phone, lambda _: None, registration=second.registration)
            if step.name.startswith("b10"))
        second_job = RunJob(1, "batch", None, account=AccountData(
            "12025550124", "Second User", "Example456!",
            "https://apifc.net/smsrecord?token=q2"))
        events = []
        def read(phone, *_args):
            return whatsapp if phone.serial == self.phone.serial else sms
        with patch("amazon_android.account_flow._read_nodes", side_effect=read), \
             patch("amazon_android.account_flow._check_summary"), \
             patch("amazon_android.account_flow._tap") as tap, \
             patch("amazon_android.account_flow._wait_screen",
                   side_effect=ToolError("Chưa thấy màn nhập mã SMS")):
            first.run(self.job, (first_step,), lambda *event: events.append(event), self.stop)
            second.run(second_job, (second_step,), lambda *event: events.append(event), self.stop)
            self.assertEqual((first.state, first.next_step), ("PAUSED", 0))
            self.assertEqual((second.state, second.next_step), ("DONE", 1))
            first.run(self.job, (first_step,), lambda *event: events.append(event), self.stop)
        tap.assert_called_once()
        self.assertEqual((first.state, first.next_step), ("PAUSED", 0))
        self.assertTrue(any("Chưa thấy màn nhập mã SMS" in event[1] for event in events))
        self.assertIsNotNone(first.registration.sms_requested_at)
        self.assertIsNotNone(second.registration.sms_requested_at)

    def test_wait_screen_stops_after_bounded_sms_observation(self):
        from amazon_android.account_flow import _wait_screen
        whatsapp = [node("Verify with WhatsApp"), node("Send code by SMS")]
        with patch("amazon_android.account_flow._read_nodes", return_value=whatsapp), \
             patch("amazon_android.account_flow.cloud_adb") as adb:
            with self.assertRaisesRegex(ToolError, "kiểm tra máy này"):
                _wait_screen(self.phone, {"SMS"}, AttemptDeadline(None), self.stop,
                             max_wait=0, timeout_message="Chưa thấy SMS; kiểm tra máy này")
        adb.assert_not_called()

    def test_sms_tap_timeout_checks_next_screen_without_resending(self):
        error = ToolError("ADB timeout")
        error.__cause__ = TimeoutExpired("adb", 6)
        whatsapp = [node("Verify with WhatsApp"), node("Send code by SMS"),
                    node(self.job.account.phone)]
        sms = [node("Verify mobile number"), node("Enter security code"),
               node(self.job.account.phone)]
        send_sms = next(step.action for step in build_common_steps(self.phone, lambda _: None)
                        if step.name.startswith("b10"))
        with patch("amazon_android.account_flow._read_nodes",
                   side_effect=[whatsapp, sms]), \
             patch("amazon_android.account_flow._tap", side_effect=error) as tap:
            send_sms(self.job, self.deadline, self.stop)
        tap.assert_called_once()

    def test_incomplete_ui_dump_is_read_again_before_using_controls(self):
        incomplete = SimpleNamespace(returncode=0, stdout="<hierarchy>")
        valid = SimpleNamespace(returncode=0, stdout=
            f'<hierarchy><node package="{AMAZON_PACKAGE}" text="Continue" /></hierarchy>')
        with patch("amazon_android.account_flow.cloud_adb", side_effect=[
                incomplete, incomplete, valid, valid]) as adb, \
             patch("amazon_android.account_flow._read_visual_nodes", return_value=[]):
            result = _read_nodes(self.phone, self.deadline, self.stop)
        self.assertEqual(result[0]["text"], "Continue")
        self.assertEqual(adb.call_count, 4)

    def test_sms_screen_after_manual_send_continues_without_second_tap(self):
        statuses = []
        send_sms = next(step.action for step in build_common_steps(
            self.phone, lambda code: None, statuses.append)
            if step.name.startswith("b10"))
        sms = [node("Verify mobile number"), node("Enter security code"),
               node(self.job.account.phone)]
        with patch("amazon_android.account_flow._read_nodes", return_value=sms), \
             patch("amazon_android.account_flow._tap") as tap:
            send_sms(self.job, self.deadline, self.stop)
        tap.assert_not_called()
        self.assertEqual(statuses, ["Đang chờ mã"])

    def test_create_button_is_after_otp_deadline(self):
        steps = build_q1_steps(self.phone, lambda code: None)
        self.assertTrue(all(step.within_attempt for step in steps[:-1]))
        self.assertFalse(steps[-1].within_attempt)

    def test_sms_code_comes_from_q1_url_and_not_whatsapp(self):
        received = []
        statuses = []
        steps = build_q1_steps(self.phone, received.append, statuses.append)
        send_sms = next(step.action for step in steps if step.name.startswith("b10"))
        enter_otp = next(step.action for step in steps if step.name == "b11 nhập OTP")
        whatsapp = [node("Verify with WhatsApp"), node("Send code by SMS")]
        sms = [node("Verify mobile number"), node("Enter security code"),
               node("Create your Amazon account"), node(self.job.account.phone)]
        with patch("amazon_android.account_flow._read_nodes",
                   side_effect=[whatsapp, sms]), \
             patch("amazon_android.account_flow.time.monotonic",
                   return_value=self.deadline.started + 1), \
             patch("amazon_android.account_flow._check_summary"), \
             patch("amazon_android.account_flow._tap"), \
             patch("amazon_android.account_flow._wait_screen", return_value=sms):
            send_sms(self.job, self.deadline, self.stop)
        with patch("amazon_android.account_flow._read_nodes", return_value=sms), \
             patch("amazon_android.account_flow.time.monotonic",
                   return_value=self.deadline.started + 2), \
             patch("amazon_android.account_flow._field", return_value={"text": ""}), \
             patch("amazon_android.account_flow.wait_for_new_otp",
                   return_value="222222") as wait, \
             patch("amazon_android.account_flow._type_field") as typed:
            enter_otp(self.job, self.deadline, self.stop)
        self.assertEqual(wait.call_args.kwargs["not_before"], self.deadline.started + 5)
        self.assertEqual(received, ["222222"])
        self.assertEqual(statuses, ["Đang chờ mã", "Đã nhập mã"])
        self.assertEqual(wait.call_args.args[:2],
                         (self.job.account.otp_url, None))
        self.assertEqual(typed.call_args.args[2], "222222")

    def test_b11_taps_otp_field_even_when_provider_read_fails(self):
        field = node("", kind="android.widget.EditText", bounds="[30,210][350,250]")
        sms = [node("Verify mobile number"), node("Enter security code"),
               node(self.job.account.phone), field]
        focused_sms = sms[:-1] + [dict(field, focused="true")]
        steps = {step.name: step.action for step in build_common_steps(self.phone, lambda _: None)}
        actions = []

        def provider_read(*_args, **_kwargs):
            actions.append("read")
            raise ToolError("Provider unavailable")

        with patch("amazon_android.account_flow._read_nodes",
                   side_effect=[sms, sms, focused_sms, focused_sms]), \
             patch("amazon_android.account_flow._tap",
                   side_effect=lambda _phone, target, _deadline: actions.append(target)), \
             patch("amazon_android.account_flow.wait_for_new_otp", side_effect=provider_read), \
             patch("amazon_android.account_flow.type_characters") as typed:
            steps["b10 Send code by SMS"](self.job, self.deadline, self.stop)
            steps["b11a chạm ô OTP"](self.job, self.deadline, self.stop)
            with self.assertRaisesRegex(ToolError, "Provider unavailable"):
                steps["b11 nhập OTP"](self.job, self.deadline, self.stop)
        self.assertEqual(actions, [field, "read"])
        typed.assert_not_called()

    def test_b11_restores_otp_focus_after_browser_returns(self):
        field = dict(node("", kind="android.widget.EditText", bounds="[30,210][350,250]"),
                     focused="false")
        focused = dict(field, focused="true")
        filled = dict(focused, text="222222")
        heading = [node("Verify mobile number"), node("Enter security code"),
                   node(self.job.account.phone)]
        steps = {step.name: step.action for step in build_common_steps(self.phone, lambda _: None)}
        actions = []
        with patch("amazon_android.account_flow._read_nodes", side_effect=[
                heading + [field], heading + [focused], heading + [field],
                heading + [field], heading + [focused], heading + [filled]]), \
             patch("amazon_android.account_flow._tap", side_effect=lambda *_: actions.append("tap")), \
             patch("amazon_android.account_flow.wait_for_new_otp", return_value="222222"), \
             patch("amazon_android.account_flow.type_characters",
                   side_effect=lambda _phone, value, *_: actions.append(value)):
            steps["b10 Send code by SMS"](self.job, self.deadline, self.stop)
            steps["b11 nhập OTP"](self.job, self.deadline, self.stop)
        self.assertEqual(actions, ["tap", "222222"])

    def test_create_is_not_pressed_twice_after_screen_changes(self):
        create = build_q1_steps(self.phone, lambda code: None)[-1].action
        sms = [node("Verify mobile number"), node("Enter security code"),
               node("Create your Amazon account"), node(self.job.account.phone)]
        next_screen = [node("Next page")]
        with patch("amazon_android.account_flow._read_nodes",
                   side_effect=[sms, next_screen, next_screen]), \
             patch("amazon_android.account_flow._field",
                   return_value=node("222222", bounds="[10,1][200,9]")), \
             patch("amazon_android.account_flow._tap") as tap:
            create(self.job, AttemptDeadline(30), self.stop)
            create(self.job, AttemptDeadline(30), self.stop)
        tap.assert_called_once()

    def test_after_sms_waits_through_slow_sms_blank_and_loading(self):
        from amazon_android.account_flow import _wait_after_sms
        elapsed = [0]
        screens = iter([[node("Verify mobile number"), node("Enter security code")],
                        [], [node("Amazon")], [node("Shop by category")]])
        def read(*_args):
            elapsed[0] += 8
            return next(screens)
        with patch("amazon_android.account_flow.time.monotonic", side_effect=lambda: elapsed[0]), \
             patch("amazon_android.account_flow._read_nodes", side_effect=read) as reader, \
             patch.object(AttemptDeadline, "allowance", side_effect=lambda seconds: seconds), \
             patch.object(self.stop, "wait", return_value=False), \
             patch("amazon_android.account_flow._tap") as tap:
            self.assertTrue(_wait_after_sms(self.phone, self.deadline, self.stop))
        self.assertEqual(reader.call_count, 4)
        self.assertEqual(elapsed[0], 32)
        tap.assert_not_called()

    def test_after_sms_still_accepts_stop_while_waiting(self):
        from amazon_android.account_flow import _wait_after_sms
        with patch("amazon_android.account_flow._read_nodes", return_value=[]), \
             patch.object(self.stop, "wait", return_value=True):
            with self.assertRaisesRegex(ToolError, "Đã dừng"):
                _wait_after_sms(self.phone, self.deadline, self.stop)

    def test_after_sms_timeout_is_45_seconds_without_repeating_confirmation(self):
        from amazon_android.account_flow import _wait_after_sms
        elapsed = [0]
        def read(*_args):
            elapsed[0] += 15
            return [node("Verify mobile number"), node("Enter security code")]
        with patch("amazon_android.account_flow.time.monotonic", side_effect=lambda: elapsed[0]), \
             patch("amazon_android.account_flow._read_nodes", side_effect=read) as reader, \
             patch.object(AttemptDeadline, "allowance", side_effect=lambda seconds: seconds), \
             patch.object(self.stop, "wait", return_value=False), \
             patch("amazon_android.account_flow._tap") as tap:
            self.assertFalse(_wait_after_sms(self.phone, self.deadline, self.stop))
        self.assertEqual(elapsed[0], 45)
        self.assertEqual(reader.call_count, 3)
        tap.assert_not_called()

    def test_login_jump_verifies_sms_without_pressing_create(self):
        from amazon_android.post_menu import RegistrationState
        state = RegistrationState()
        steps = build_common_steps(self.phone, lambda _: None, registration=state)
        send_sms = next(step.action for step in steps if step.name.startswith("b10"))
        finish = steps[-1].action
        otp = node("222222", kind="android.widget.EditText",
                   bounds="[25,100][335,140]")
        verify = node("Verify mobile number", bounds="[25,155][335,195]")
        sms = [node("Verify mobile number"), node("Enter security code"),
               node(self.job.account.phone), otp, verify]
        menu = [node("Shop by category")]
        with patch("amazon_android.account_flow._read_nodes",
                   side_effect=[sms, sms, menu]), \
             patch("amazon_android.account_flow._tap") as tap, \
             patch("amazon_android.account_flow._visual_form_button") as visual:
            send_sms(self.job, self.deadline, self.stop)
            finish(self.job, self.deadline, self.stop)
        self.assertTrue(state.login_jump_seen)
        self.assertTrue(state.login_verify_pressed)
        self.assertFalse(state.create_pressed)
        tap.assert_called_once_with(self.phone, verify, self.deadline)
        visual.assert_not_called()

    def test_login_otp_uses_visual_readback_then_verify_without_retyping(self):
        from amazon_android.post_menu import RegistrationState
        state = RegistrationState(login_jump_seen=True, sms_requested_at=1.0)
        statuses = []
        codes = []
        steps = build_common_steps(self.phone, codes.append, statuses.append,
                                   registration=state)
        enter = next(step.action for step in steps if step.name == "b11 nhập OTP")
        finish = steps[-1].action
        blank = [node("Verify mobile number"), node("Enter security code"),
                 node(self.job.account.phone),
                 node("", kind="android.widget.EditText",
                      bounds="[25,100][335,140]")]
        visual = blank[:-1] + [node("222222", kind="android.widget.EditText",
                                    bounds="[25,100][335,140]"),
                               node("Verify mobile number", bounds="[25,155][335,195]")]
        menu = [node("Shop by category")]
        tapped = False

        def read(*_args):
            return menu if tapped else blank

        def type_then_lose_readback(*_args, **kwargs):
            kwargs["before_input"]()
            raise ToolError("Chưa xác nhận được nội dung ô 'Enter security code'")

        def tap(*_args):
            nonlocal tapped
            tapped = True

        with patch("amazon_android.account_flow._read_nodes", side_effect=read), \
             patch("amazon_android.account_flow._read_login_sms_visual",
                   return_value=visual) as visual_read, \
             patch("amazon_android.account_flow.wait_for_new_otp",
                   return_value="222222"), \
             patch("amazon_android.account_flow._type_field",
                   side_effect=type_then_lose_readback) as typed, \
             patch("amazon_android.account_flow._tap", side_effect=tap) as pressed:
            enter(self.job, self.deadline, self.stop)
            finish(self.job, self.deadline, self.stop)
        typed.assert_called_once()
        self.assertEqual(visual_read.call_count, 2)
        pressed.assert_called_once()
        self.assertIs(pressed.call_args.args[1], visual[-1])
        self.assertTrue(state.login_otp_input_attempted)
        self.assertTrue(state.login_verify_pressed)
        self.assertFalse(state.create_pressed)
        self.assertEqual(codes, ["222222"])
        self.assertEqual(statuses, ["Đã nhập mã"])

    def test_login_otp_resume_does_not_type_again_when_readback_is_unclear(self):
        from amazon_android.post_menu import RegistrationState
        state = RegistrationState(login_jump_seen=True, login_otp_input_attempted=True,
                                  sms_requested_at=1.0, code="222222")
        enter = next(step.action for step in build_common_steps(
            self.phone, lambda _: None, registration=state)
            if step.name == "b11 nhập OTP")
        blank = [node("Verify mobile number"), node("Enter security code"),
                 node(self.job.account.phone),
                 node("", kind="android.widget.EditText",
                      bounds="[25,100][335,140]")]
        with patch("amazon_android.account_flow._read_nodes", return_value=blank), \
             patch("amazon_android.account_flow._read_login_sms_visual",
                   return_value=blank), \
             patch("amazon_android.account_flow._type_field") as typed, \
             patch("amazon_android.account_flow.wait_for_new_otp") as provider:
            with self.assertRaisesRegex(ToolError, "không gõ lặp"):
                enter(self.job, self.deadline, self.stop)
        typed.assert_not_called()
        provider.assert_not_called()

    def test_create_otp_never_uses_login_visual_readback(self):
        from amazon_android.post_menu import RegistrationState
        state = RegistrationState(create_flow_seen=True, sms_requested_at=1.0)
        enter = next(step.action for step in build_common_steps(
            self.phone, lambda _: None, registration=state)
            if step.name == "b11 nhập OTP")
        blank = [node("Verify mobile number"), node("Enter security code"),
                 node(self.job.account.phone),
                 node("", kind="android.widget.EditText",
                      bounds="[25,100][335,140]")]
        with patch("amazon_android.account_flow._read_nodes", return_value=blank), \
             patch("amazon_android.account_flow.wait_for_new_otp",
                   return_value="222222"), \
             patch("amazon_android.account_flow._type_field") as typed, \
             patch("amazon_android.account_flow._read_login_sms_visual") as visual_read:
            enter(self.job, self.deadline, self.stop)
        typed.assert_called_once()
        self.assertNotIn("before_input", typed.call_args.kwargs)
        visual_read.assert_not_called()
        self.assertFalse(state.login_otp_input_attempted)

    def test_login_jump_without_visible_verify_does_not_guess_create(self):
        from amazon_android.post_menu import RegistrationState
        state = RegistrationState(login_jump_seen=True, code="222222")
        finish = build_common_steps(self.phone, lambda _: None,
                                    registration=state)[-1].action
        sms = [node("Verify mobile number"), node("Enter security code"),
               node(self.job.account.phone),
               node("222222", kind="android.widget.EditText",
                    bounds="[25,100][335,140]")]
        with patch("amazon_android.account_flow._read_nodes", return_value=sms), \
             patch("amazon_android.account_flow._tap") as tap, \
             patch("amazon_android.account_flow._visual_form_button",
                   side_effect=ToolError("Chưa xác định được nút Verify mobile number")) as visual:
            with self.assertRaisesRegex(ToolError, "Verify mobile number"):
                finish(self.job, self.deadline, self.stop)
        self.assertFalse(state.login_verify_pressed)
        tap.assert_not_called()
        visual.assert_called_once_with(self.phone, sms, "Verify mobile number",
                                       sms[-1], self.deadline, min_coverage=0.5)

    def test_login_uses_one_yellow_button_when_webview_omits_its_label(self):
        from amazon_android.post_menu import RegistrationState
        state = RegistrationState(login_jump_seen=True, code="222222")
        finish = build_common_steps(self.phone, lambda _: None,
                                    registration=state)[-1].action
        otp = node("222222", kind="android.widget.EditText",
                   bounds="[25,100][335,140]")
        sms = [node("Verify mobile number"), node("Enter security code"),
               node(self.job.account.phone), otp]
        yellow = node("", bounds="[25,155][335,195]")
        with patch("amazon_android.account_flow._read_nodes",
                   side_effect=[sms, [node("Shop by category")]]), \
             patch("amazon_android.account_flow._visual_form_button",
                   return_value=yellow) as visual, \
             patch("amazon_android.account_flow._tap") as tap:
            finish(self.job, self.deadline, self.stop)
        visual.assert_called_once_with(self.phone, sms, "Verify mobile number",
                                       otp, self.deadline, min_coverage=0.5)
        tap.assert_called_once_with(self.phone, yellow, self.deadline)
        self.assertTrue(state.login_verify_pressed)
        self.assertFalse(state.create_pressed)

    def test_login_continue_retries_visible_verify_once_after_uncertain_tap(self):
        from amazon_android.post_menu import RegistrationState
        state = RegistrationState(login_jump_seen=True, code="222222")
        finish = build_common_steps(self.phone, lambda _: None,
                                    registration=state)[-1].action
        otp = node("222222", kind="android.widget.EditText",
                   bounds="[25,100][335,140]")
        verify = node("Verify mobile number", bounds="[25,155][335,195]")
        sms = [node("Verify mobile number"), node("Enter security code"),
               node(self.job.account.phone), otp, verify]
        menu = [node("Shop by category")]
        taps = []

        def read(*_args):
            return menu if len(taps) == 2 else sms

        with patch("amazon_android.account_flow._read_nodes", side_effect=read), \
             patch("amazon_android.account_flow._tap",
                   side_effect=lambda *_args: taps.append(verify)), \
             patch.object(AttemptDeadline, "allowance", side_effect=[0, 10]):
            with self.assertRaisesRegex(ToolError, "màn SMS chưa đổi"):
                finish(self.job, self.deadline, self.stop)
            self.assertEqual(state.login_verify_attempts, 1)
            finish(self.job, self.deadline, self.stop)
        self.assertEqual(taps, [verify, verify])
        self.assertEqual(state.login_verify_attempts, 2)
        self.assertFalse(state.create_pressed)

    def test_login_continue_stops_after_two_verify_attempts(self):
        from amazon_android.post_menu import RegistrationState
        state = RegistrationState(login_jump_seen=True, code="222222",
                                  login_verify_pressed=True,
                                  login_verify_attempts=2)
        finish = build_common_steps(self.phone, lambda _: None,
                                    registration=state)[-1].action
        sms = [node("Verify mobile number"), node("Enter security code"),
               node(self.job.account.phone),
               node("222222", kind="android.widget.EditText",
                    bounds="[25,100][335,140]"),
               node("Verify mobile number", bounds="[25,155][335,195]")]
        with patch("amazon_android.account_flow._read_nodes", return_value=sms), \
             patch("amazon_android.account_flow._tap") as tap:
            with self.assertRaisesRegex(ToolError, "hai lần"):
                finish(self.job, self.deadline, self.stop)
        tap.assert_not_called()
        self.assertFalse(state.create_pressed)

    def test_explicit_modes_bind_distinct_final_actions_and_recover_create_marker(self):
        from amazon_android.post_menu import RegistrationState
        create_state = RegistrationState(flow_mode="create", create_flow_seen=True)
        login_state = RegistrationState(flow_mode="login")
        create_steps = build_common_steps(self.phone, lambda _: None,
                                          registration=create_state)
        login_steps = build_common_steps(self.phone, lambda _: None,
                                         registration=login_state)
        self.assertEqual(create_steps[-1].action.__name__, "finish_create")
        self.assertEqual(login_steps[-1].action.__name__, "finish_login")
        sms = [node("Verify mobile number"), node("Enter security code"),
               node("Create your Amazon account"), node(self.job.account.phone)]
        with patch("amazon_android.account_flow._read_nodes", return_value=sms), \
             patch("amazon_android.account_flow._tap") as tap:
            login_steps[5].action(self.job, self.deadline, self.stop)
            self.assertTrue(login_state.login_jump_seen)
            create_state.create_flow_seen = False
            create_steps[7].action(self.job, self.deadline, self.stop)
            self.assertTrue(create_state.create_flow_seen)
            self.assertFalse(create_state.login_jump_seen)
        tap.assert_not_called()

    def test_create_b10_sends_sms_from_matching_whatsapp_without_old_marker(self):
        from amazon_android.post_menu import RegistrationState
        state = RegistrationState(flow_mode="create")
        send_sms = next(step.action for step in build_common_steps(
            self.phone, lambda _: None, registration=state)
            if step.name.startswith("b10"))
        whatsapp = [node("Verify with WhatsApp"), node("Send code by SMS"),
                    node(self.job.account.phone)]
        sms = [node("Verify mobile number"), node("Enter security code"),
               node("Create your Amazon account"), node(self.job.account.phone)]
        with patch("amazon_android.account_flow._read_nodes", return_value=whatsapp), \
             patch("amazon_android.account_flow._wait_screen", return_value=sms), \
             patch("amazon_android.account_flow._tap_for_transition") as tap:
            send_sms(self.job, self.deadline, self.stop)
        tap.assert_called_once()
        self.assertFalse(state.login_jump_seen)
        self.assertEqual(state.sms_tap_attempts, 1)

    def test_existing_auto_session_keeps_visible_create_fallback(self):
        from amazon_android.post_menu import RegistrationState
        state = RegistrationState(login_jump_seen=True, code="222222")
        finish = build_common_steps(self.phone, lambda _: None,
                                    registration=state)[-1].action
        create = node("Create your Amazon account",
                      bounds="[25,155][335,195]")
        sms = [node("Verify mobile number"), node("Enter security code"),
               node(self.job.account.phone),
               node("222222", kind="android.widget.EditText",
                    bounds="[25,100][335,140]"), create]
        with patch("amazon_android.account_flow._read_nodes",
                   side_effect=[sms, sms, [node("Next page")]]), \
             patch("amazon_android.account_flow._tap") as tap:
            finish(self.job, self.deadline, self.stop)
        tap.assert_called_once_with(self.phone, create, self.deadline)
        self.assertTrue(state.create_pressed)
        self.assertFalse(state.login_verify_pressed)

    def test_create_flow_keeps_create_action_even_after_sms(self):
        from amazon_android.post_menu import RegistrationState
        state = RegistrationState(create_flow_seen=True)
        steps = build_common_steps(self.phone, lambda _: None, registration=state)
        send_sms = next(step.action for step in steps if step.name.startswith("b10"))
        finish = steps[-1].action
        otp = node("222222", kind="android.widget.EditText",
                   bounds="[25,100][335,140]")
        sms = [node("Verify mobile number"), node("Enter security code"),
               node(self.job.account.phone), otp]
        create = node("Create your Amazon account", bounds="[25,155][335,195]")
        with patch("amazon_android.account_flow._read_nodes",
                   side_effect=[sms, sms, [node("Next page")]]), \
             patch("amazon_android.account_flow._tap") as tap, \
             patch("amazon_android.account_flow._visual_form_button",
                   return_value=create) as visual:
            send_sms(self.job, self.deadline, self.stop)
            finish(self.job, self.deadline, self.stop)
        self.assertFalse(state.login_jump_seen)
        self.assertFalse(state.login_verify_pressed)
        self.assertTrue(state.create_pressed)
        tap.assert_called_once_with(self.phone, create, self.deadline)
        visual.assert_called_once()

    def test_visual_fallback_accepts_one_yellow_form_button_and_rejects_two(self):
        field = node("", bounds="[25,100][335,140]")
        with Image.new("RGB", (360, 640), "white") as image:
            draw = ImageDraw.Draw(image)
            draw.rounded_rectangle((25, 330, 334, 369), radius=18, fill="#ffd814")
            draw.text((150, 345), "Continue", fill="black")
            result = _yellow_form_button(image, field)
            self.assertEqual(result["bounds"], "[25,330][335,370]")
            draw.rounded_rectangle((25, 240, 334, 279), radius=18, fill="#ffd814")
            with self.assertRaisesRegex(ToolError, "nút vàng"):
                _yellow_form_button(image, field)
            self.assertEqual(_yellow_form_button(image, field, labels=((140, 342, 220, 358),)),
                             result)

    def test_login_yellow_button_survives_text_splitting_the_color_band(self):
        field = node("", bounds="[24,230][360,279]")
        with Image.new("RGB", (386, 481), "white") as image:
            draw = ImageDraw.Draw(image)
            draw.rounded_rectangle((28,290,357,332), radius=20, fill="#ffd814")
            draw.rectangle((120,309,250,316), fill="black")
            with self.assertRaises(ToolError):
                _yellow_form_button(image, field)
            self.assertEqual(_yellow_form_button(image, field, min_coverage=0.5)["bounds"],
                             "[24,290][360,333]")

    def test_create_uses_visual_fallback_only_for_matching_phone_and_taps_once(self):
        create = build_common_steps(self.phone, lambda _: None)[-1].action
        otp = node("222222", kind="android.widget.EditText", bounds="[25,100][335,140]")
        sms = [node("Verify mobile number"), node("Enter security code"),
               node(self.job.account.phone), otp]
        wrong_phone = sms[:2] + [otp]
        button = node("", bounds="[25,155][335,195]")
        next_screen = [node("Next page")]
        with patch("amazon_android.account_flow._read_nodes",
                   side_effect=[wrong_phone, sms, next_screen, next_screen]), \
             patch("amazon_android.account_flow._visual_form_button", return_value=button) as visual, \
             patch("amazon_android.account_flow._tap") as tap:
            with self.assertRaisesRegex(ToolError, "SĐT"):
                create(self.job, self.deadline, self.stop)
            visual.assert_not_called()
            create(self.job, self.deadline, self.stop)
            create(self.job, self.deadline, self.stop)
        visual.assert_called_once_with(self.phone, sms, "Create your Amazon account", otp,
                                      self.deadline)
        tap.assert_called_once_with(self.phone, button, self.deadline)


if __name__ == "__main__":
    unittest.main()
