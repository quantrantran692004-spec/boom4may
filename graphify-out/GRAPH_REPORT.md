# Graph Report - bom4may  (2026-11-27)

## Corpus Check
- 139 files · ~174,821 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 2, .bat 1, .pyw 1)

## Summary
- 2268 nodes · 7843 edges · 92 communities (79 shown, 13 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 1129 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `46678318`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ToolError
- Q1FlowTests
- otp.py
- BulkInputTests
- desktop.py
- show_apps
- RunnerTests
- PostMenuStep
- .test_only_confirmed_target_names_are_selected_for_one_start_command
- build_create_address_detail_steps
- 003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật
- Danh mục từng bước đã biết — 13/11/2026
- build_random_steps
- StopResetTests
- amazon-android-tool
- Ảnh hướng dẫn q1/q2 và menu chung lưu cục bộ
- ToolError
- AttemptDeadline
- marketplace_flow.py
- _find_scrolling
- MENU_ROUTING.md
- Q3Q4FlowTests
- _type_field
- phone_window_layout.py
- Nghiên cứu và tích hợp Swarmote
- profile_status
- amazon_is_foreground
- Window
- RegistrationState
- PROJECT_INDEX.md
- RandomPrefixTests
- core.py
- vision.py
- subprocess
- _visible
- time
- retry_preparation
- build_create_address_steps
- account_flow.py
- cli.py
- Bàn giao trạng thái dự án — 13/11/2026
- cloud_adb
- FakeControl
- Button
- screen
- cloud_adb
- bulk_input.py
- cli.py
- account_flow.py
- b1–b11 Reliability and Latency Implementation Plan
- desktop.py
- Danh mục ảnh nằm trong dự án
- build_q1_steps
- Amazon Android Tool — Giai đoạn A/B
- test_desktop_layout.py
- _CombinedStop
- Giao diện vận hành
- build_common_steps
- Amazon trên Swarmote
- home_menu.py
- build_reload_payment_steps
- Bộ cài chia sẻ Windows x64
- CountryRecoveryTests
- PhoneReader
- VERIFICATION.md
- AccountData
- .test_single_row_paste_and_clear_touch_only_selected_failed_machine
- _visible
- cloud.py
- PROJECT_HANDOFF.md
- build_post_auth_steps
- BatchDraft
- test_swarmote_navigation.py
- _button
- random_prefix.py
- Q2FlowTests
- BatchDraft
- CountryRecoveryTests
- build_q1_steps
- 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng
- Bàn giao dừng theo yêu cầu người dùng — 13/11/2026
- _prefix_nodes
- OTP_DESIGN.md
- ensure_manager_ready
- .test_b11_taps_otp_field_even_when_provider_read_fails
- Q5_FLOW.md
- _scroll_up
- ._refresh_table
- GRAPH_AUDIT.md
- PreparationProgressTests

## God Nodes (most connected - your core abstractions)
1. `ToolError` - 354 edges
2. `CloudPhone` - 234 edges
3. `AttemptDeadline` - 202 edges
4. `RunJob` - 170 edges
5. `RegistrationState` - 162 edges
6. `build_common_steps()` - 115 edges
7. `Window` - 109 edges
8. `PostMenuStep` - 93 edges
9. `Q1FlowTests` - 92 edges
10. `PostMenuSession` - 85 edges

## Surprising Connections (you probably didn't know these)
- `Cách xử lý ảnh tiếp theo` --references--> `screen()`  [INFERRED]
  FLOW_PROGRESS.md → amazon_android/account_flow.py
- `Bổ sung đọc ảnh OCR và chạm trực tiếp dự phòng cho b26 khi uiautomator dump WebView lỗi — 19/11/2026` --references--> `_read_hierarchy()`  [INFERRED]
  PROJECT_HANDOFF.md → amazon_android/account_flow.py
- `b6 US +1 còn mở sau bốn cú chạm — 14/11/2026` --references--> `_wait_screen()`  [INFERRED]
  PROJECT_HANDOFF.md → amazon_android/account_flow.py
- `q6 b1–b3a riêng, b4–b11 chung — 14/11/2026` --references--> `_ensure_menu()`  [INFERRED]
  PROJECT_HANDOFF.md → amazon_android/account_flow.py
- `Điều tra q1/q2 mượt, q3+ lỗi thất thường khi chạy song song — 14/11/2026` --references--> `_ensure_menu()`  [INFERRED]
  PROJECT_HANDOFF.md → amazon_android/account_flow.py

## Import Cycles
- None detected.

## Communities (92 total, 13 thin omitted)

### Community 0 - "ToolError"
Cohesion: 0.22
Nodes (11): ToolError, _field_for_label(), fill_identifier(), fill_signup_form(), _nodes(), open_entry(), _tap(), _type_into() (+3 more)

### Community 2 - "otp.py"
Cohesion: 0.10
Nodes (8): browser_launch_options(), extract_otp(), _NoRedirect, read_otp(), _read_otp_in_browser(), wait_for_new_otp(), OtpTests, PackagedBrowserTests

### Community 3 - "BulkInputTests"
Cohesion: 0.06
Nodes (12): BulkRecord, lines(), parse_bulk_payload(), parse_column(), parse_records(), _proxy_rows(), _table_cells(), _url_from_cell() (+4 more)

### Community 4 - "desktop.py"
Cohesion: 0.17
Nodes (8): create_shortcut(), relaunch_command(), runtime(), set_process_identity(), set_tk_icon(), set_window_identity(), Sửa shortcut ghim mở nhầm IDLE — 13/11/2026, WindowsIdentityTests

### Community 5 - "show_apps"
Cohesion: 0.09
Nodes (30): ready_for_home_menu(), _check_stop(), collapse_apps_panel(), _descendants(), inspect(), install_amazon(), check_stop(), _one() (+22 more)

### Community 6 - "RunnerTests"
Cohesion: 0.05
Nodes (20): ProfileRegistry, ProfileLookupError, ProfileNotFound, Thiết kế yêu cầu, absent(), ProfileRegistryTests, lookup(), broken() (+12 more)

### Community 7 - "PostMenuStep"
Cohesion: 0.07
Nodes (18): reconcile(), route(), PostMenuSession, PostMenuStep, PostMenuTests, first_step(), reconcile(), step() (+10 more)

### Community 8 - ".test_only_confirmed_target_names_are_selected_for_one_start_command"
Cohesion: 0.08
Nodes (14): ProfileStartNotSubmitted, _select_profile_rows(), _selected_profile_names(), start_profile(), start_profiles_together(), _wait_for_selected(), Hàng đợi 4 máy với giới hạn 2 Running — 14/11/2026, delayed_start() (+6 more)

### Community 9 - "build_create_address_detail_steps"
Cohesion: 0.13
Nodes (7): build_create_address_detail_steps(), AddressDetailTests, read(), adb(), tap(), read(), item()

### Community 10 - "003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật"
Cohesion: 0.07
Nodes (25): 002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ, Kiểm tra bắt buộc, Phạm vi, Rủi ro và bảo trì, Điều kiện dừng, 003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật, Các bước, Kiểm tra bắt buộc (+17 more)

### Community 11 - "Danh mục từng bước đã biết — 13/11/2026"
Cohesion: 0.06
Nodes (36): Bản thử q7 State Machine — 14/11/2026, Chung b10 — Chuyển WhatsApp sang SMS, Chung b11 — Lấy và gõ OTP SMS, Chung b11a — Chạm ô OTP trên màn SMS, Chung b11b — Xác minh đăng nhập hoặc bấm Create của luồng tạo, Chung b12–b15 — Mở ba gạch rồi ba lượt điều hướng ngẫu nhiên, Chung b4 — Sign In từ menu, Chung b4a — Chạm ô SĐT (+28 more)

### Community 12 - "build_random_steps"
Cohesion: 0.05
Nodes (12): build_random_steps(), browse(), finish_view(), B1–b3 xem menu ngẫu nhiên cho 12 máy — 14/11/2026, Một quy luật để sửa mã về sau — 20/11/2026, adb(), adb(), tap() (+4 more)

### Community 13 - "StopResetTests"
Cohesion: 0.07
Nodes (6): retry_preparation(), RunJob, P03 — Mở form New Profile, Q6FlowTests, StopResetTests, install()

### Community 16 - "Ảnh hướng dẫn q1/q2 và menu chung lưu cục bộ"
Cohesion: 0.07
Nodes (28): B16–b22 chung — Đổi marketplace sang United States (18/11/2026), B32–b39 — Reload Balance, thêm thẻ và địa chỉ thanh toán (21/11/2026), B6 — Hai ảnh đính kèm mới ngày 13/11/2026, Menu chung ảnh 01 — Danh sách chữ, Menu chung ảnh 02 — App Store bên phải sau khi Amazon mở, q1 b6 — US +1 hiện nhưng chạm không đóng hộp, 14/11/2026, q1 ảnh 01 — Menu và ba thẻ, q1 ảnh 02 — Sign In cuối menu (+20 more)

### Community 17 - "ToolError"
Cohesion: 0.10
Nodes (14): CloudPhone, _confirm_menu_fallback(), _menu_evidence(), MenuReadUnavailable, _nodes(), budget(), open_home_menu(), _tap() (+6 more)

### Community 18 - "AttemptDeadline"
Cohesion: 0.06
Nodes (27): AttemptDeadline, ExtendedRecoveryTests, fail(), read(), read(), MarketplaceFlowTests, read(), adb() (+19 more)

### Community 19 - "marketplace_flow.py"
Cohesion: 0.21
Nodes (22): _account_tab(), run(), account_target(), back_and_read_text(), foreground_ready(), recover_country_list(), _destination(), _is_account_tab() (+14 more)

### Community 20 - "_find_scrolling"
Cohesion: 0.23
Nodes (19): _at_or_after(), country(), sign_in(), _ensure_menu(), _find_scrolling(), menu_layout(), _read_nodes(), _tap_for_transition() (+11 more)

### Community 21 - "MENU_ROUTING.md"
Cohesion: 0.23
Nodes (7): Bằng chứng và phạm vi, Kiểm chứng, Quy tắc chạy, Điều hướng hai dạng menu ba gạch, Luồng q1 từ menu ba gạch tới nhập OTP, Thử trên q1 đã có, Luồng q2 từ menu ba gạch

### Community 22 - "Q3Q4FlowTests"
Cohesion: 0.18
Nodes (3): build_q3_steps(), build_q4_steps(), Q3Q4FlowTests

### Community 23 - "_type_field"
Cohesion: 0.23
Nodes (22): adb(), available_memory_mb(), avd_names(), check_play(), configure_avd(), connected_devices(), create_avd(), Device (+14 more)

### Community 24 - "phone_window_layout.py"
Cohesion: 0.08
Nodes (14): _already_reached_result(), build_q7_pilot_steps(), _past_known_step(), ResultVerifier, StateDeadline, StateDetector, StateMachineStop, StateMachineTimeout (+6 more)

### Community 25 - "Nghiên cứu và tích hợp Swarmote"
Cohesion: 0.40
Nodes (4): Hành vi có bằng chứng, Kiểm thử còn lại, Nghiên cứu và tích hợp Swarmote, Phần đã áp dụng

### Community 26 - "profile_status"
Cohesion: 0.17
Nodes (7): visible_lookup(), _start_and_confirm(), _profile_row_status(), profile_status(), Các bước, Tự phục hồi lỗi tạm thời trong mẻ nhiều máy — 14/11/2026, Tự phục hồi lỗi tạm thời trong mẻ nhiều máy — 14/11/2026

### Community 28 - "amazon_is_foreground"
Cohesion: 0.16
Nodes (3): amazon_is_foreground(), CloudBridgeTests, adb()

### Community 29 - "Window"
Cohesion: 0.09
Nodes (5): state_style(), Window, emit(), Các bước, Trạng thái kiểm chứng và giới hạn

### Community 30 - "RegistrationState"
Cohesion: 0.08
Nodes (9): RegistrationState, build_tail_steps(), open_menu(), view(), visit_seconds(), _choose_tail_target(), RandomPrefixTests, choose() (+1 more)

### Community 31 - "PROJECT_INDEX.md"
Cohesion: 0.19
Nodes (6): Quy trình Swarmote hiện tại, Bản đồ repository, q3 — b1–b3 và nối luồng chung, q4 — Giỏ hàng, Pets, Home and DIY, q5 — ba thẻ riêng và b4–b11 chung, q6 — Trang chủ, Giỏ hàng, menu và một thẻ

### Community 32 - "RandomPrefixTests"
Cohesion: 0.11
Nodes (4): RandomPrefixTests, adb(), adb(), adb()

### Community 33 - "core.py"
Cohesion: 0.10
Nodes (13): wait_until(), swarmote_adb_path(), swarmote_tunnel_owner(), ReaderResponseError, _connect(), country_reverse_points(), country_scroll(), _failed() (+5 more)

### Community 34 - "vision.py"
Cohesion: 0.07
Nodes (19): _bounds(), _canonical_text(), _compact(), _engine(), _field_contents(), _field_is_blank(), _input_box(), _join_wrapped_categories() (+11 more)

### Community 35 - "subprocess"
Cohesion: 0.18
Nodes (11): Cài đặt máy mới, _app_installed(), _app_paths(), _check_external_apps(), _install_python_dependencies(), _installed_project_metadata_matches(), main(), _offer_downloads() (+3 more)

### Community 36 - "_visible"
Cohesion: 0.15
Nodes (17): _action(), _address_form(), _addresses(), _bounded_native(), run(), _default_box_target(), _default_visual_label(), _find() (+9 more)

### Community 37 - "time"
Cohesion: 0.16
Nodes (13): app_data_dir(), doctor(), executable(), installed_image(), sdk_root(), confirm(), download_commandline_tools(), official_commandline_archive() (+5 more)

### Community 38 - "retry_preparation"
Cohesion: 0.16
Nodes (6): _keyboard_visible(), _tap_input(), _type_field(), Phục hồi khi ô nhập chưa nhận focus ở b4–b11 — 14/11/2026, FlowRecoveryTests, form()

### Community 39 - "build_create_address_steps"
Cohesion: 0.24
Nodes (4): build_create_address_steps(), CreateAddressFlowTests, read(), node()

### Community 40 - "account_flow.py"
Cohesion: 0.11
Nodes (18): _ActionNotResolved, _country_nodes(), _CountryReadStop, _form_action(), _read_login_sms_visual(), _read_nodes_once(), _read_visual_nodes(), resume_common_index() (+10 more)

### Community 41 - "cli.py"
Cohesion: 0.17
Nodes (8): BatchItem, parse_proxy_line(), prepare_five(), create_profile(), ProxyConfig, Mục tiêu và bằng chứng, BatchSafetyTests, CreationWindowVisibilityTests

### Community 42 - "Bàn giao trạng thái dự án — 13/11/2026"
Cohesion: 0.12
Nodes (14): B6 danh sách quốc gia vẫn mở sau khi chọn — 13/11/2026, Bàn giao trạng thái dự án — 13/11/2026, Bản chính boom4may và bản dự phòng — 14/11/2026, Bộ cài offline chia sẻ — 14/11/2026, Dừng riêng máy đang chọn — 14/11/2026, Mã hiện có, q3/q4 đã nối b1–b3 và thử đồng thời bốn luồng — 13/11/2026, q5 b1–b3 riêng, b4–b11 chung — 14/11/2026 (+6 more)

### Community 43 - "cloud_adb"
Cohesion: 0.12
Nodes (21): _country_full_row(), _parse_ui_nodes(), _read_hierarchy(), scroll_view(), cloud_adb(), RecoverableStepError, build_random_steps(), browse() (+13 more)

### Community 44 - "FakeControl"
Cohesion: 0.13
Nodes (5): ParallelInstallTests, PhoneWindow, FakeControl, InstallTests, descendants()

### Community 45 - "Button"
Cohesion: 0.13
Nodes (7): Button, Entry, FooterNote, icon(), TableText, Tooltip, ui_font()

### Community 46 - "screen"
Cohesion: 0.18
Nodes (13): focus_phone(), home_visible(), route_list_menu(), screen(), _ScreenWaitExpired, _tap(), _unique(), visit_home() (+5 more)

### Community 47 - "cloud_adb"
Cohesion: 0.35
Nodes (10): _foreground(), _add_button(), step(), _card_parts(), _field_target(), _find(), _input(), _read_until() (+2 more)

### Community 48 - "bulk_input.py"
Cohesion: 0.13
Nodes (5): arrange_on_open(), _row_if_fits(), _sort_key(), _tiles(), PhoneWindowLayoutTests

### Community 49 - "cli.py"
Cohesion: 0.20
Nodes (10): main(), parser(), report(), open_amazon(), foreground(), get_device(), print_json(), Store (+2 more)

### Community 51 - "b1–b11 Reliability and Latency Implementation Plan"
Cohesion: 0.18
Nodes (10): b1–b11 Reliability and Latency Implementation Plan, Completion Criteria, File Map, Global Constraints, Review Focus, Task 1: Measure current step latency and classify existing failures, Task 2: Define safe retry, reconcile, pause, and stop behavior, Task 3: Reduce redundant UI reads and unnecessary waits (+2 more)

### Community 52 - "desktop.py"
Cohesion: 0.15
Nodes (8): _automatic_resume_slots(), save(), default_path(), AppSettings, load_settings(), save_settings(), settings_path(), SettingsTests

### Community 53 - "Danh mục ảnh nằm trong dự án"
Cohesion: 0.18
Nodes (11): amazon_android/assets/icons/, amazon_android/assets/obsidian_prism.png, amazon_android/assets/swarmote_tool_square.png và swarmote_tool.ico, assets/ui_history/machine7_input_before.png, assets/ui_history/reset_check.png, assets/ui_history/ui-12.png, assets/ui_history/ui_palette_preview.png, assets/ui_history/ui-preview.png (+3 more)

### Community 55 - "Amazon Android Tool — Giai đoạn A/B"
Cohesion: 0.29
Nodes (7): Amazon Android Tool — Giai đoạn A/B, Cài trên máy Windows mới, Dán nhiều proxy, Sử dụng, Trạng thái nghiệm thu, Yêu cầu, Điện thoại đám mây Swarmote

### Community 56 - "test_desktop_layout.py"
Cohesion: 0.12
Nodes (6): startup_geometry(), status_title(), StatusCell, DesktopLayoutTests, __init__(), __init__()

### Community 58 - "Giao diện vận hành"
Cohesion: 0.33
Nodes (5): Bố cục, Giao diện vận hành, Hướng thị giác, Quy tắc, Swarmote V3 — nghiệm thu 27/11/2026

### Community 60 - "Amazon trên Swarmote"
Cohesion: 0.33
Nodes (5): Amazon trên Swarmote, Người dùng và công việc, Nền tảng, Điều chưa xác minh, Định hướng ngôn ngữ nếu xây dựng lại — 23/11/2026

### Community 61 - "home_menu.py"
Cohesion: 0.07
Nodes (27): b6 Country US +1 — 14/11/2026, B6 cuộn quốc gia và chọn lại — 13/11/2026, Biên bản kiểm tra thực tế — 2026-11-12, Cài và đo UiAutomator2 theo phê duyệt mới — 13/11/2026, Cập nhật luồng mẻ trước đó — 2026-11-13, Dừng riêng một máy — 14/11/2026, Focus ô nhập b4–b11 — 14/11/2026, Ghim taskbar — 13/11/2026 (+19 more)

### Community 62 - "build_reload_payment_steps"
Cohesion: 0.13
Nodes (9): build_reload_payment_steps(), node(), ReloadPaymentTests, adb(), wait(), read(), read(), read() (+1 more)

### Community 63 - "Bộ cài chia sẻ Windows x64"
Cohesion: 0.50
Nodes (3): Bộ cài chia sẻ Windows x64, Dựng lại, Nguồn thành phần

### Community 64 - "CountryRecoveryTests"
Cohesion: 0.12
Nodes (3): animations_enabled(), SmoothScrollableFrame, DesktopScrollTests

### Community 65 - "PhoneReader"
Cohesion: 0.27
Nodes (7): phone_reader(), PhoneReader, _serve(), fake_worker(), IsolationTests, duplicate(), production_worker_with_fake_android()

### Community 66 - "VERIFICATION.md"
Cohesion: 0.17
Nodes (10): Kết luận và tích hợp, Kết quả thực tế, So sánh bộ đọc trên q1 — 13/11/2026, Thành phần thiết bị, b1–b3 bắt buộc có ba cú bấm — 14/11/2026, b1–b3 ngẫu nhiên cho 12 máy — 14/11/2026, b1–b3 ngẫu nhiên trên 12 máy, không dùng OCR — 14/11/2026, b6 cuộn tới đáy rồi vuốt ngược — 14/11/2026 (+2 more)

### Community 67 - "AccountData"
Cohesion: 0.13
Nodes (4): AccountData, DesktopResumeTests, Q2FlowTests, on_worker()

### Community 68 - ".test_single_row_paste_and_clear_touch_only_selected_failed_machine"
Cohesion: 0.13
Nodes (16): _phone_preparation_lock(), _prepare_phone(), _prepare_phone_locked(), progress(), stop_here(), run_batch(), fill_slots(), manually_selected() (+8 more)

### Community 69 - "_visible"
Cohesion: 0.21
Nodes (19): _bounds(), _resume_address_payment_index(), _text(), _visible(), _street_field(), _street_focused(), _street_label(), _street_saved_field() (+11 more)

### Community 70 - "cloud.py"
Cohesion: 0.21
Nodes (9): cloud_serials(), package_path(), probe(), prop(), reported_installer(), require_online(), scan(), build_q5_steps() (+1 more)

### Community 71 - "PROJECT_HANDOFF.md"
Cohesion: 0.12
Nodes (16): b1–b3 ngẫu nhiên cho q1–q12 — 14/11/2026, B4–b11 chạy đồng thời và OCR — 14/11/2026, b6 US +1 còn mở sau bốn cú chạm — 14/11/2026, Bản thử State Machine q7 và b1–b3 mở mục con — 14/11/2026, Bỏ thời hạn tổng sau menu — 14/11/2026, Bổ sung đọc ảnh OCR và chạm trực tiếp dự phòng cho b26 khi uiautomator dump WebView lỗi — 19/11/2026, Cơ chế chụp ảnh OCR quét chữ ấn luôn cho toàn bộ b26–b31 — 19/11/2026, Dán bảng Amazon có ghi chú thẻ live và URL OTP escaped — 14/11/2026 (+8 more)

### Community 72 - "build_post_auth_steps"
Cohesion: 0.14
Nodes (14): Hướng dẫn khi tiếp tục dự án, build_marketplace_steps(), build_post_auth_steps(), _tail_candidates(), _tail_input_action(), _tail_safe_page_choices(), Phần dùng chung đã được hướng dẫn, Nhận diện giao diện lúc chạy (+6 more)

### Community 74 - "test_swarmote_navigation.py"
Cohesion: 0.10
Nodes (14): _activate_manager(), _create_profile_form(), _invoke(), _open_profiles(), _profile_form_open(), _unfiltered_single_page(), visible_profile_names(), Đã có trong graph (+6 more)

### Community 75 - "_button"
Cohesion: 0.14
Nodes (22): confirmed_login_otp_nodes(), continue_number(), enter_otp(), finish_auto(), finish_create(), finish_login(), focus_otp(), name() (+14 more)

### Community 76 - "random_prefix.py"
Cohesion: 0.14
Nodes (7): _first_point(), PrefixDeadline, Q7PrefixTimeout, _tap_child(), _first_point(), _PrefixRecoveryStop, _TailChoicesExhausted

### Community 77 - "Q2FlowTests"
Cohesion: 0.16
Nodes (9): main(), main(), Đợt tăng tốc và tự phục hồi b4–b11 ngày 13/11/2026, File dự án mà Graphify không phân tích trực tiếp, .gitignore, Launch Swarmote Tool.pyw, pyproject.toml, Ảnh PNG trong dự án (+1 more)

### Community 79 - "CountryRecoveryTests"
Cohesion: 0.27
Nodes (4): CountryRecoveryTests, read(), wait(), node()

### Community 81 - "001 — Tách dữ liệu từng mẻ và đối chiếu số hàng"
Cohesion: 0.29
Nodes (7): 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Rủi ro và bảo trì, Thiết kế yêu cầu, Điều kiện dừng

### Community 82 - "Bàn giao dừng theo yêu cầu người dùng — 13/11/2026"
Cohesion: 0.25
Nodes (7): Bàn giao dừng theo yêu cầu người dùng — 13/11/2026, Bối cảnh đã hoàn tất trước lỗi hiện tại, Cách tiếp tục, Kiểm chứng gần nhất, Lỗi chính chưa xử lý xong, Phần sửa Stop/Reset đã viết nhưng chưa thử GUI thật, Yêu cầu mới nhất

### Community 83 - "_prefix_nodes"
Cohesion: 0.29
Nodes (6): _prefix_nodes(), Cách xử lý ảnh tiếp theo, Phần riêng từng máy, Tiến độ hướng dẫn bằng ảnh — cập nhật 13/11/2026, 14 ảnh menu chung b1–b3 ngẫu nhiên — 14/11/2026, B1–B3 hiện hành — Ba lượt ngẫu nhiên q1–q12

### Community 84 - "OTP_DESIGN.md"
Cohesion: 0.50
Nodes (3): Nối vào bước tạo tài khoản sau khi xác minh màn hình Amazon, Thiết kế OTP cho từng Profile, Đã chuẩn bị

### Community 85 - "ensure_manager_ready"
Cohesion: 0.14
Nodes (10): ensure_manager_ready(), _main_window(), collect(), ProfileCreateNotSubmitted, ProfileManagerWindowError, ProxyTestFailed, ManagerStartupTests, unavailable() (+2 more)

### Community 87 - "Q5_FLOW.md"
Cohesion: 0.40
Nodes (5): Cách thử bản pilot cũ (không áp dụng cho factory hiện hành), Giai đoạn 2 — bản thử State Machine riêng q7, Giới hạn, Phạm vi và quan hệ với luồng cũ, Sơ đồ

### Community 88 - "_scroll_up"
Cohesion: 0.53
Nodes (6): _scroll_up(), read_menu(), return_to_menu(), visit(), action(), Tự động chuyển bước sau 60 giây nếu không thấy menu Browse ở b13–b15 — 19/11/2026

### Community 91 - "._refresh_table"
Cohesion: 0.48
Nodes (3): _proxy_postal_prefix(), controls(), ProxyPostalPrefixTests

### Community 92 - "GRAPH_AUDIT.md"
Cohesion: 0.50
Nodes (3): Cách kiểm tra sau mỗi sửa đổi, Giới hạn đã xác nhận, Kiểm tra độ phủ Graphify — cập nhật 26/11/2026

## Knowledge Gaps
- **1 isolated node(s):** `amazon-android-tool`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 558 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **13 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ToolError` connect `ToolError` to `Q1FlowTests`, `otp.py`, `BulkInputTests`, `show_apps`, `RunnerTests`, `PostMenuStep`, `.test_only_confirmed_target_names_are_selected_for_one_start_command`, `build_create_address_detail_steps`, `build_random_steps`, `StopResetTests`, `desktop.py`, `ToolError`, `AttemptDeadline`, `marketplace_flow.py`, `_find_scrolling`, `_type_field`, `phone_window_layout.py`, `profile_status`, `amazon_is_foreground`, `Window`, `RegistrationState`, `RandomPrefixTests`, `core.py`, `vision.py`, `_visible`, `time`, `retry_preparation`, `build_create_address_steps`, `account_flow.py`, `cli.py`, `cloud_adb`, `screen`, `cloud_adb`, `cli.py`, `desktop.py`, `build_q1_steps`, `build_common_steps`, `build_reload_payment_steps`, `PhoneReader`, `AccountData`, `.test_single_row_paste_and_clear_touch_only_selected_failed_machine`, `_visible`, `cloud.py`, `build_post_auth_steps`, `BatchDraft`, `test_swarmote_navigation.py`, `_button`, `random_prefix.py`, `BatchDraft`, `CountryRecoveryTests`, `build_q1_steps`, `_prefix_nodes`, `ensure_manager_ready`, `.test_b11_taps_otp_field_even_when_provider_read_fails`, `_scroll_up`?**
  _High betweenness centrality (0.327) - this node is a cross-community bridge._
- **Are the 58 inferred relationships involving `ToolError` (e.g. with `_read_nodes_once()` and `_resume_address_payment_index()`) actually correct?**
  _`ToolError` has 58 INFERRED edges - model-reasoned connections that need verification._
- **What connects `amazon-android-tool` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Q1FlowTests` be split into smaller, more focused modules?**
  _Cohesion score 0.08350951374207188 - nodes in this community are weakly interconnected._
- **Why does `CloudPhone` connect `ToolError` to `ToolError`, `Q1FlowTests`, `show_apps`, `PostMenuStep`, `build_create_address_detail_steps`, `build_random_steps`, `StopResetTests`, `desktop.py`, `AttemptDeadline`, `_find_scrolling`, `Q3Q4FlowTests`, `phone_window_layout.py`, `profile_status`, `.test_manual_otp_repair_continues_with_confirmation_and_tail_for_both_modes`, `amazon_is_foreground`, `Window`, `RegistrationState`, `RandomPrefixTests`, `core.py`, `retry_preparation`, `build_create_address_steps`, `account_flow.py`, `cloud_adb`, `screen`, `cli.py`, `desktop.py`, `build_q1_steps`, `build_common_steps`, `build_reload_payment_steps`, `PhoneReader`, `AccountData`, `.test_single_row_paste_and_clear_touch_only_selected_failed_machine`, `cloud.py`, `build_post_auth_steps`, `BatchDraft`, `_button`, `random_prefix.py`, `CountryRecoveryTests`, `build_q1_steps`, `_scroll_up`?**
  _High betweenness centrality (0.111) - this node is a cross-community bridge._
- **Are the 88 inferred relationships involving `CloudPhone` (e.g. with `build_common_steps()` and `_country_full_row()`) actually correct?**
  _`CloudPhone` has 88 INFERRED edges - model-reasoned connections that need verification._
- **Should `otp.py` be split into smaller, more focused modules?**
  _Cohesion score 0.1010752688172043 - nodes in this community are weakly interconnected._