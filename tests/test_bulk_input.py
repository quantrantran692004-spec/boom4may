import unittest
import threading
from unittest.mock import Mock, patch

from amazon_android.bulk_input import parse_bulk_payload, parse_column, parse_records, validate_card
from amazon_android.batch_state import BatchDraft
from amazon_android.core import ToolError
from amazon_android.desktop import GREEN, Window
from amazon_android.post_menu import PostMenuSession
from amazon_android.runner import AccountData, RunJob
from amazon_android.swarmote_desktop import ProxyConfig


class Value:
    def __init__(self, value=""):
        self.value = value

    def get(self):
        return self.value

    def set(self, value):
        self.value = value


class BulkInputTests(unittest.TestCase):
    def locked_window(self):
        window = Window.__new__(Window)
        window.draft = BatchDraft(proxy_count=2, account_count=2, locked=True)
        window.selected = 1
        window.status = [("Máy 1 đã có Profile", "created"),
                         ("Máy 2 tạo Profile lỗi", "error")]
        window.registry = Mock()
        window.registry.get.return_value = {"stage": "RESERVED", "state": "ERROR",
                                            "device_id": None}
        window.phone_serials = {}
        window.post_menu_sessions = {}
        window.preparation_retry_workers = {}
        window._pending_retries = set()
        window._edited_locked_rows = set()
        window.running = True
        window.jobs = {}
        window.values = []
        for index in range(2):
            proxy = ProxyConfig("socks5", f"old{index}.example", 1000 + index,
                                "user", "password")
            account = AccountData(f"1202555012{index}", f"Example {index}",
                                  "ExamplePass1!",
                                  f"https://apifc.net/smsrecord?token=machine{index}")
            window.jobs[index] = RunJob(index, window.draft.batch_id, proxy,
                                        (), account)
            window.values.append({
                "host": Value(proxy.host), "port": Value(str(proxy.port)),
                "username": Value(proxy.username),
                "proxy_password": Value(proxy.password),
                "phone": Value(account.phone),
                "amazon_password": Value(account.password),
                "full_name": Value(account.full_name),
                "card": Value(""), "otp_url": Value(account.otp_url),
                "profile_name": Value(f"q{index + 1}"),
            })
        window.proxy_line = Mock()
        window.run_note = Mock()
        window._refresh_devices = Mock()
        window._previous_work_busy = Mock(return_value=False)
        window._start_profile_creation_retry = Mock()
        return window

    def test_locked_failed_machine_paste_only_changes_selected_proxy(self):
        window = self.locked_window()
        window._pending_retries.add(1)
        window.status[1] = ("Chờ tạo lại", "retry_queued")
        window._accept_proxy_text("new.example:2002:newuser:newpass")
        self.assertEqual(window.values[0]["host"].get(), "old0.example")
        self.assertEqual(window.values[1]["host"].get(), "new.example")
        self.assertEqual(window.jobs[1].proxy.host, "old1.example")
        self.assertEqual(window._pending_retries, set())
        self.assertEqual(window.status[1][1], "error")
        self.assertEqual(window._edited_locked_rows, {1})

    def test_continue_uses_repaired_proxy_and_account_for_only_failed_machine(self):
        window = self.locked_window()
        original_first = window.jobs[0]
        window._accept_proxy_text("new.example:2002:newuser:newpass")
        window.values[1]["full_name"].set("Repaired Person")
        window.values[1]["phone"].set("12025550999")
        window.values[1]["otp_url"].set(
            "https://apifc.net/smsrecord?token=repaired")
        window._continue_profile(1)
        self.assertIs(window.jobs[0], original_first)
        self.assertEqual(window.jobs[1].proxy.host, "new.example")
        self.assertEqual(window.jobs[1].account.phone, "12025550999")
        self.assertEqual(window.jobs[1].account.full_name, "Repaired Person")
        self.assertEqual(window._edited_locked_rows, set())
        self.assertEqual(window._pending_retries, set())
        window._start_profile_creation_retry.assert_called_once_with(1)

    def test_immediate_retry_receives_repaired_machine_job(self):
        window = self.locked_window()
        window._accept_proxy_text("new.example:2002:newuser:newpass")
        window._continue_profile(1)
        window.cancel = threading.Event()
        window.phone_stop_after_step = {}
        window.events = Mock()
        window.run_group_size = 2
        window.run_hide_profile_creation = True
        window.proxy_postal_prefixes = {}
        window.menu_opened_at = {}
        with patch("amazon_android.desktop.threading.Thread") as thread:
            Window._start_profile_creation_retry(window, 1)
        sent_jobs = thread.call_args.kwargs["args"][0]
        self.assertEqual(len(sent_jobs), 1)
        self.assertEqual(sent_jobs[0].proxy.host, "new.example")
        self.assertEqual(sent_jobs[0].index, 1)

    def test_locked_failed_machine_rejects_multi_proxy_paste(self):
        window = self.locked_window()
        window._accept_proxy_text("one.example:1001:u:p two.example:1002:u:q")
        self.assertEqual(window.values[1]["host"].get(), "old1.example")
        self.assertEqual(window._edited_locked_rows, set())

    def test_only_failed_uncreated_profile_has_editable_detail_fields(self):
        window = self.locked_window()
        window.bulk_boxes = {"proxy": Mock(), "account": Mock()}
        window.detail_entries = {"host": Mock(), "full_name": Mock(),
                                 "profile_name": Mock()}
        window.count_menu = Mock()
        window.proxy_paste_heading = Mock()
        window.proxy_paste_hint = Mock()
        window.single_account_line = Mock()
        window.apply_single_account_button = Mock()
        window.clear_selected_button = Mock()
        window._set_editing(False)
        window.detail_entries["host"].configure.assert_called_with(state="normal")
        window.detail_entries["full_name"].configure.assert_called_with(state="normal")
        window.bulk_boxes["proxy"].configure.assert_called_with(state="disabled")
        window.selected = 0
        window._set_editing(False)
        window.detail_entries["host"].configure.assert_called_with(state="disabled")
        window.proxy_line.configure.assert_called_with(state="disabled")
        window.selected = 1
        window.status[1] = ("Create chưa chắc chắn", "uncertain")
        window._set_editing(False)
        window.detail_entries["host"].configure.assert_called_with(state="disabled")
        window.status[1] = ("Amazon đã dừng", "post_paused")
        window.post_menu_sessions[1] = PostMenuSession(window.draft.batch_id, 1,
                                                       "q2", state="PAUSED")
        window._set_editing(False)
        window.detail_entries["host"].configure.assert_called_with(state="disabled")
        window.detail_entries["full_name"].configure.assert_called_with(state="normal")
        window.single_account_line.configure.assert_called_with(state="normal")

    def test_paused_machine_can_fix_amazon_without_changing_created_proxy(self):
        window = self.locked_window()
        window.status[1] = ("Amazon đã dừng", "post_paused")
        window.post_menu_sessions[1] = PostMenuSession(window.draft.batch_id, 1,
                                                       "q2", state="PAUSED")
        window.post_menu_workers = {}
        window.phone_stop_after_step = {}
        window.cancel = threading.Event()
        window._start_post_menu = Mock()
        old_proxy = window.jobs[1].proxy
        old_first = window.jobs[0]
        window.values[1]["phone"].set("12025550999")
        window._edited_locked_rows.add(1)
        window._continue_profile(1)
        self.assertEqual(window.jobs[1].account.phone, "12025550999")
        self.assertIs(window.jobs[1].proxy, old_proxy)
        self.assertIs(window.jobs[0], old_first)
        window._start_post_menu.assert_called_once_with(1)

    def test_created_profile_error_allows_amazon_but_not_proxy_replacement(self):
        window = self.locked_window()
        window.registry.get.return_value = {
            "stage": "PROFILE_CONFIRMED", "state": "ERROR",
            "device_id": "device-two"}
        self.assertFalse(window._can_edit_locked_row(1))
        self.assertTrue(window._can_edit_account_row(1))
        window._accept_proxy_text("new.example:2002:newuser:newpass")
        self.assertEqual(window.values[1]["host"].get(), "old1.example")
        self.assertEqual(window._edited_locked_rows, set())

    def test_editing_queued_machine_cancels_old_retry_before_new_continue(self):
        window = self.locked_window()
        window._pending_retries.add(1)
        window.status[1] = ("Chờ tạo lại", "retry_queued")
        window._schedule_refresh = Mock()
        window._on_row_value_changed(1, "full_name")
        self.assertEqual(window._pending_retries, set())
        self.assertEqual(window._edited_locked_rows, {1})
        self.assertEqual(window.status[1][1], "error")

    def test_focusing_proxy_field_cancels_queued_retry_before_paste(self):
        window = self.locked_window()
        window._pending_retries.add(1)
        window.status[1] = ("Chờ tạo lại", "retry_queued")
        window._begin_locked_repair()
        self.assertEqual(window._pending_retries, set())
        self.assertEqual(window._edited_locked_rows, {1})

    def test_invalid_repair_keeps_old_job_and_does_not_queue_retry(self):
        window = self.locked_window()
        old_job = window.jobs[1]
        window.values[1]["port"].set("invalid")
        window._edited_locked_rows.add(1)
        window._continue_profile(1)
        self.assertIs(window.jobs[1], old_job)
        self.assertEqual(window._pending_retries, set())
        self.assertEqual(window.status[1][1], "error")

    def test_locked_account_field_allows_one_value_paste_only(self):
        window = self.locked_window()
        window.root = Mock()
        window.root.clipboard_get.return_value = "One Name"
        self.assertIsNone(window._paste_detail_column("name"))
        window.root.clipboard_get.return_value = "One Name\nOther Name"
        self.assertEqual(window._paste_detail_column("name"), "break")

    def test_proxy_rows_map_in_order(self):
        found = parse_column("proxy", "one.example:1001:u:p\ntwo.example:1002:u:q\n")
        self.assertEqual([(x.host, x.port) for x in found],
                         [("one.example", 1001), ("two.example", 1002)])

    def test_space_separated_proxy_paste_maps_four_entries_in_order(self):
        found = parse_column(
            "proxy", "one.example:1001:u1:p1 two.example:1002:u2:p2 "
            "three.example:1003:u3:p3 four.example:1004:u4:p4")
        self.assertEqual([(item.host, item.port, item.username) for item in found], [
            ("one.example", 1001, "u1"), ("two.example", 1002, "u2"),
            ("three.example", 1003, "u3"), ("four.example", 1004, "u4")])

    def test_single_proxy_password_with_spaces_keeps_existing_parsing(self):
        found = parse_column("proxy", "one.example:1001:u:pass with spaces")
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].password, "pass with spaces")

    def test_space_separated_proxy_limit_is_enforced(self):
        pasted = " ".join(f"host{i}.example:1001:u:p" for i in range(101))
        with self.assertRaisesRegex(ToolError, "giới hạn"):
            parse_column("proxy", pasted)

    def test_single_proxy_field_distributes_space_separated_paste(self):
        window = Window.__new__(Window)
        window.draft = BatchDraft()
        window.selected = 2
        window.proxy_fallbacks = []
        window.values = [{key: Mock() for key in
                          ("host", "port", "username", "proxy_password")}
                         for _ in range(12)]
        window.count = Mock()
        window.proxy_line = Mock()
        window.run_note = Mock()
        window._refresh_devices = Mock()
        window._accept_proxy_text(
            "one.example:1001:u1:p1 two.example:1002:u2:p2 "
            "three.example:1003:u3:p3 four.example:1004:u4:p4")
        self.assertEqual(window.draft.proxy_count, 4)
        window.count.set.assert_called_with("4")
        for index, host in enumerate(("one.example", "two.example",
                                      "three.example", "four.example")):
            window.values[index]["host"].set.assert_called_with(host)

    def test_selected_machine_binds_its_own_amazon_fields(self):
        window = Window.__new__(Window)
        window.count = Mock()
        window.count.get.return_value = "12"
        window.draft = BatchDraft()
        window.draft.locked = True
        keys = ("full_name", "phone", "amazon_password", "card", "otp_url")
        window.values = [{key: object() for key in keys} for _ in range(12)]
        window.detail_entries = {key: Mock() for key in keys}
        window.detail_title = Mock()
        window.account_detail_heading = Mock()
        window.single_account_heading = Mock()
        window.detail_status = Mock()
        window.single_account_line = Mock()
        window.apply_single_account_button = Mock()
        window.clear_selected_button = Mock()
        window.status = [("Chưa chạy", "idle") for _ in range(12)]
        window._refresh_otp_detail = Mock()
        window._refresh_devices = Mock()
        window._select(6)
        for key in keys:
            window.detail_entries[key].configure.assert_called_with(
                textvariable=window.values[6][key])
        window.account_detail_heading.configure.assert_called_with(
            text="Thông tin Amazon riêng · Máy 7")
        window.single_account_heading.configure.assert_called_with(
            text="Dán hàng Amazon · Máy 7")

    def test_internal_blank_line_rejected_to_preserve_alignment(self):
        with self.assertRaises(ToolError):
            parse_column("name", "First\n\nThird")

    def test_password_whitespace_is_not_silently_changed(self):
        self.assertEqual(parse_column("password", "  value  \n"), ["  value  "])

    def test_short_passwords_pass_paste_and_machine_validation_unchanged(self):
        window = Window.__new__(Window)
        window.registry, window.registry_error = object(), ""
        window.draft = BatchDraft(proxy_count=1, account_count=1)
        window.jobs, window.count = {}, Value("1")
        values = {"host": "proxy.example", "port": "1001", "username": "user",
                  "proxy_password": "secret", "phone": "12025550123",
                  "full_name": "First", "amazon_password": "a", "card": "",
                  "otp_url": "https://apifc.net/smsrecord?token=synthetic-short"}
        window.values = [{key: Value(value) for key, value in values.items()}]
        for size in range(1, 9):
            password = "a" * size
            with self.subTest(size=size):
                window.values[0]["amazon_password"].set(password)
                basic = f"{values['phone']},{password},First"
                self.assertEqual(parse_records(basic)[0].password, password)
                _, accounts = parse_bulk_payload(basic + "," + values["otp_url"])
                self.assertEqual([row.password for row in accounts], [password])
                self.assertEqual(window._input_issue(), "")
                self.assertEqual(window._account_for_profile(0).password, password)
        for password in ("", "a b", "a\tb", "mật-khẩu"):
            with self.subTest(invalid=password):
                window.values[0]["amazon_password"].set(password)
                with self.assertRaises(ToolError):
                    parse_records(f"{values['phone']},{password},First,{values['otp_url']}",
                                  account_table=True)
                self.assertNotEqual(window._input_issue(), "")
                with self.assertRaises(ToolError):
                    window._account_for_profile(0)

    def test_markdown_table_imports_multiple_records_and_optional_proxy(self):
        rows = parse_records(
            "| Job 1 | +84901234567 | Pass1234 | Name One | one.example:1001:u:p |\n"
            "| --- | ---: | --- | --- | --- |\n"
            "| Job 2 | +84901234568 | Pass5678 | Name Two | two.example:1002:u:q |"
        )
        self.assertEqual([item.profile_name for item in rows], ["Job 1", "Job 2"])
        self.assertEqual(rows[1].full_name, "Name Two")
        self.assertEqual(rows[1].proxy.host, "two.example")

    def test_table_with_four_columns_keeps_proxy_optional(self):
        rows = parse_records("Job 1\t+84901234567\tPass1234\tName One")
        self.assertIsNone(rows[0].proxy)

    def test_three_column_markdown_table_assigns_q_profiles(self):
        rows = parse_records(
            "| 17624680931 | Example456! | Wilhelmina |\n"
            "| ----------: | --------- | ---------- |\n"
            "| 17624680932 | Example789! | Cordelia |"
        )
        self.assertEqual([item.profile_name for item in rows], ["q1", "q2"])
        self.assertEqual([item.phone for item in rows], ["17624680931", "17624680932"])
        self.assertEqual(rows[1].full_name, "Cordelia")

    def test_table_rejects_ambiguous_column_count(self):
        with self.assertRaises(ToolError):
            parse_records("17624680931,Example456!")

    def test_desktop_table_requires_exactly_three_columns(self):
        with self.assertRaises(ToolError):
            parse_records("Job 1,17624680931,Example456!,Name One",
                          three_columns_only=True)

    def test_desktop_otp_table_keeps_each_url_with_its_phone(self):
        rows = parse_records(
            "| SĐT | Mật khẩu | Tên | URL OTP |\n"
            "| --- | --- | --- | --- |\n"
            "| 17624680931 | Example456! | First | https://apifc.net/smsrecord?token=one |\n"
            "| 17624680932 | Example789! | Second | https://apifc.net/smsrecord?token=two |",
            account_table=True,
        )
        self.assertEqual([(row.profile_name, row.phone, row.otp_url) for row in rows], [
            ("q1", "17624680931", "https://apifc.net/smsrecord?token=one"),
            ("q2", "17624680932", "https://apifc.net/smsrecord?token=two"),
        ])
        self.assertNotIn("token=one", repr(rows[0]))

    def test_desktop_otp_table_requires_url_and_rejects_shared_token(self):
        with self.assertRaisesRegex(ToolError, "4 cột"):
            parse_records("17624680931,Example456!,First", account_table=True)
        with self.assertRaisesRegex(ToolError, "URL OTP"):
            parse_records("17624680931,Example456!,First,", account_table=True)
        with self.assertRaisesRegex(ToolError, "trùng"):
            parse_records(
                "17624680931,Example456!,First,https://apifc.net/smsrecord?token=same\n"
                "17624680932,Example789!,Second,https://apifc.net/smsrecord?token=same",
                account_table=True,
            )

    def test_expanded_markdown_table_maps_twelve_cards_and_otp_links_by_row(self):
        rows = []
        for index in range(12):
            url = f"https://apifc.net/smsrecord?token=synthetic{index:02d}"
            card = f"400000000000{index:04d}\\|12\\|2030"
            cells = [f"1202555{index:04d}", "Example456!", f"Name {index + 1}",
                     "", "", "", "", "", "", card, f"[{url}]({url})"]
            rows.append("| " + " | ".join(cells) + " |")
        separator = "| " + " | ".join(["---:"] + ["-"] * 10) + " |"
        rows.insert(1, separator)
        found = parse_records("\n".join(rows), account_table=True)
        self.assertEqual(len(found), 12)
        self.assertEqual([item.profile_name for item in found],
                         [f"q{index}" for index in range(1, 13)])
        for index, item in enumerate(found):
            self.assertEqual(item.phone, f"1202555{index:04d}")
            self.assertEqual(item.card, f"400000000000{index:04d}|12|2030")
            self.assertEqual(item.otp_url,
                             f"https://apifc.net/smsrecord?token=synthetic{index:02d}")
            self.assertNotIn(item.card, repr(item))

    def test_bulk_paste_keeps_bold_first_data_row_above_separator(self):
        lines = []
        expected = []
        for index in range(3):
            phone, password, name = f"1202555012{index}", f"Example{index}Pass!", f"Person {index}"
            card = f"400000000000000{index}|12|2030"
            url = f"https://apifc.net/smsrecord?token=synthetic-bold-{index}"
            cells = [phone, password, name, "", "", "", "", "check later", "",
                     card.replace("|", r"\|"), f"[{url}]({url})"]
            if index == 0:
                cells = [f"**{cell}**" if cell else "" for cell in cells]
                cells[-1] = f"[**{url}**]({url})"
            lines.append("| " + " | ".join(cells) + " |")
            expected.append((f"q{index + 1}", phone, password, name, card, url))
        lines.insert(1, "| " + " | ".join(["---:"] + ["-"] * 10) + " |")
        pasted = "\n".join(lines)
        proxies, accounts = parse_bulk_payload(pasted)
        self.assertEqual(proxies, [])
        self.assertEqual(len(accounts), 3)
        for records in (accounts, parse_records(pasted, account_table=True)):
            self.assertEqual([(row.profile_name, row.phone, row.password, row.full_name,
                               row.card, row.otp_url) for row in records], expected)
        window = Window.__new__(Window)
        window.draft = BatchDraft()
        window.values = [{key: Value() for key in
                          ("phone", "amazon_password", "full_name", "card", "otp_url")}
                         for _ in range(12)]
        window.count = Mock()
        window.bulk_boxes = {kind: Mock() for kind in ("proxy", "account")}
        window.bulk_feedback = {kind: Mock() for kind in ("proxy", "account")}
        for callback in ("_refresh_devices", "_refresh_otp_detail", "_maybe_show_preview"):
            setattr(window, callback, Mock())
        window.run_note = Mock()
        window._apply_bulk_text("account", pasted)
        self.assertEqual(window.draft.account_count, 3)
        window.count.set.assert_called_with("3")
        self.assertEqual([tuple(row[key].get() for key in
                               ("phone", "amazon_password", "full_name", "card", "otp_url"))
                          for row in window.values[:3]],
                         [record[1:] for record in expected])

    def test_markdown_bold_headers_and_whole_link_keep_first_account(self):
        url = "https://apifc.net/smsrecord?token=synthetic-bold-link"
        for marker in ("**", "__"):
            with self.subTest(marker=marker):
                rows = parse_records(
                    f"| {marker}SĐT{marker} | Mật khẩu | Tên | URL OTP |\n"
                    "| --- | --- | --- | --- |\n"
                    f"| {marker}12025550123{marker} | {marker}Example456!{marker} | "
                    f"{marker}First{marker} | {marker}[{url}]({url}){marker} |",
                    account_table=True)
                self.assertEqual(len(rows), 1)
                self.assertEqual((rows[0].phone, rows[0].password, rows[0].full_name, rows[0].otp_url),
                                 ("12025550123", "Example456!", "First", url))

    def test_tab_and_csv_passwords_keep_literal_bold_markers(self):
        url = "https://apifc.net/smsrecord?token=synthetic-literal"
        for separator in ("\t", ","):
            with self.subTest(separator=separator):
                rows = parse_records(separator.join(
                    ("12025550123", "**Example456!**", "First", url)), account_table=True)
                self.assertEqual(rows[0].password, "**Example456!**")

    def test_bold_markdown_link_label_still_rejects_mismatched_target(self):
        label = "https://apifc.net/smsrecord?token=synthetic-label"
        target = "https://apifc.net/smsrecord?token=synthetic-target"
        with self.assertRaisesRegex(ToolError, "URL OTP"):
            parse_records(
                f"| 12025550123 | Example456! | First | [**{label}**]({target}) |",
                account_table=True)

    def test_card_column_can_use_raw_pipes_and_rejects_extra_url(self):
        url = "https://apifc.net/smsrecord?token=synthetic"
        five_columns = parse_records(
            f"| 12025550123 | Example456! | Name | 4000000000000001\\|12\\|2030 | {url} |",
            account_table=True,
        )
        self.assertEqual(five_columns[0].card, "4000000000000001|12|2030")
        found = parse_records(
            f"| 12025550123 | Example456! | Name | 4000000000000001|12|2030 | {url} |",
            account_table=True,
        )
        self.assertEqual(found[0].card, "4000000000000001|12|2030")
        with self.assertRaisesRegex(ToolError, "đúng 1 URL OTP"):
            parse_records(
                f"| 12025550123 | Example456! | Name | {url} | {url} |",
                account_table=True,
            )

    def test_tab_rows_accept_live_card_note_and_escaped_otp_url(self):
        rows = []
        for index in range(3):
            phone = f"12025550{index:03d}"
            card = f"400000000000{index:04d}|12|2030|live=>√【example.test】"
            url = f"https\\://apifc.net/smsrecord?token=synthetic{index}\\"
            rows.append(f"{phone}\tExample456!\tName {index}\t\t\t\t"
                        f"\t\t\t{card}\t{url}")
        parsed = parse_records("\n".join(rows), account_table=True)
        self.assertEqual([item.phone for item in parsed],
                         [f"12025550{index:03d}" for index in range(3)])
        self.assertEqual([item.card for item in parsed],
                         [f"400000000000{index:04d}|12|2030" for index in range(3)])
        self.assertEqual([item.otp_url for item in parsed],
                         [f"https://apifc.net/smsrecord?token=synthetic{index}"
                          for index in range(3)])
        self.assertNotIn("example.test", repr(parsed[0]))

    def test_card_annotation_is_limited_to_supported_live_format(self):
        self.assertEqual(
            validate_card("4000000000000001|12|2030|live=>√【example.test】"),
            "4000000000000001|12|2030")
        with self.assertRaises(ToolError):
            validate_card("4000000000000001|12|2030|other")

    def test_account_paste_discards_bad_card_and_extra_export_columns(self):
        url = "https://apifc.net/smsrecord?token=synthetic"
        rows = parse_records(
            f"12025550123\tExample456!\tFirst\t4000000000000001|13|2030\tignored\t"
            f"https://other.test/wrong\t{url}",
            account_table=True)
        self.assertEqual((rows[0].phone, rows[0].card, rows[0].otp_url),
                         ("12025550123", "", url))

    def test_either_paste_box_extracts_valid_proxy_and_account_rows(self):
        url = "https://apifc.net/smsrecord?token=synthetic"
        mixed = ("note to discard\n"
                 "proxy.example:1001:user:secret\n"
                 f"12025550123\tExample456!\tFirst\tbad card\t{url}\n"
                 "broken.example:bad:user:secret\n")
        proxies, accounts = parse_bulk_payload(mixed)
        self.assertEqual([(item.host, item.port) for item in proxies],
                         [("proxy.example", 1001)])
        self.assertEqual([(item.profile_name, item.card, item.otp_url)
                          for item in accounts], [("q1", "", url)])

        window = Window.__new__(Window)
        window.draft = BatchDraft()
        window.values = [{key: Mock() for key in
                          ("host", "port", "username", "proxy_password", "phone",
                           "amazon_password", "full_name", "card", "otp_url")}
                         for _ in range(12)]
        window.count = Mock()
        window.bulk_boxes = {kind: Mock() for kind in ("proxy", "account")}
        window.bulk_feedback = {kind: Mock() for kind in ("proxy", "account")}
        window.run_note = Mock()
        window.proxy_fallbacks = []
        window._refresh_devices = Mock()
        window._refresh_otp_detail = Mock()
        window._maybe_show_preview = Mock()
        window._apply_bulk_text("proxy", mixed)
        self.assertEqual((window.draft.proxy_count, window.draft.account_count), (1, 1))
        window.values[0]["phone"].set.assert_called_with("12025550123")
        window.values[0]["host"].set.assert_called_with("proxy.example")
        window._apply_bulk_text("account", "other.example:1002:user:secret")
        window.values[0]["host"].set.assert_called_with("other.example")
        self.assertEqual(window.draft.account_count, 1)
        window.bulk_feedback["account"].configure.assert_called_with(
            text="Đã chuyển vào Proxy", text_color=GREEN)

    def test_bulk_payload_skips_bad_rows_without_shifting_valid_phone_url_pairs(self):
        first = "https://apifc.net/smsrecord?token=first"
        second = "https://apifc.net/smsrecord?token=second"
        pasted = (f"12025550123\tExample456!\tFirst\t{first}\n"
                  "12025550124\tExample456!\tBroken\thttps://other.test/wrong\n"
                  f"12025550125\tExample456!\tSecond\t{second}\n"
                  f"12025550126\tExample456!\tDuplicate\t{first}")
        proxies, accounts = parse_bulk_payload(pasted)
        self.assertEqual(proxies, [])
        self.assertEqual([(row.profile_name, row.phone, row.otp_url) for row in accounts], [
            ("q1", "12025550123", first),
            ("q2", "12025550125", second),
        ])

    def test_bulk_account_rows_accept_missing_cards_and_mixed_rows(self):
        url1 = "https://apifc.net/smsrecord?token=synthetic-one"
        url2 = "https://apifc.net/smsrecord?token=synthetic-two"
        rows = parse_records(
            f"12025550123\tExample456!\tFirst\t{url1}\n"
            f"12025550124\tExample789!\tSecond\t\t\t"
            f"4000000000000001|12|2030\t{url2}",
            account_table=True,
        )
        self.assertEqual([row.card for row in rows], ["", "4000000000000001|12|2030"])
        self.assertEqual([row.otp_url for row in rows], [url1, url2])

    def test_desktop_validation_does_not_require_card_after_bulk_paste(self):
        from types import SimpleNamespace
        window = Window.__new__(Window)
        window.registry = object()
        window.registry_error = ""
        window.draft = BatchDraft(proxy_count=1, account_count=1)
        window.jobs = {}
        window.count = SimpleNamespace(get=lambda: "1")
        values = {
            "host": "proxy.example", "port": "1001", "username": "user",
            "proxy_password": "secret", "phone": "12025550123",
            "amazon_password": "Example456!", "full_name": "First",
            "card": "", "otp_url": "https://apifc.net/smsrecord?token=synthetic",
        }
        window.values = [{key: SimpleNamespace(get=lambda value=value: value)
                          for key, value in values.items()}]
        self.assertEqual(window._input_issue(), "")

    def test_batch_cannot_start_with_proxy_rows_but_no_amazon_rows(self):
        from types import SimpleNamespace
        window = Window.__new__(Window)
        window.registry = object()
        window.registry_error = ""
        window.draft = BatchDraft(proxy_count=2, account_count=0)
        window.jobs = {}
        window.count = SimpleNamespace(get=lambda: "2")
        self.assertIn("Chưa có hàng Amazon", window._input_issue())


if __name__ == "__main__":
    unittest.main()
