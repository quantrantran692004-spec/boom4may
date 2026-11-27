# Graph Report - boom4may  (2026-11-27)

## Corpus Check
- 136 files · ~172,995 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 2, .bat 1, .pyw 1)

## Summary
- 2234 nodes · 7766 edges · 86 communities (74 shown, 12 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 1125 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `1710754c`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- registration.py
- build_common_steps
- otp.py
- BulkInputTests
- windows_identity.py
- swarmote_desktop.py
- RunnerTests
- PostMenuStep
- ToolError
- AddressDetailTests
- 003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật
- Danh mục từng bước đã biết — 13/11/2026
- RegistrationState
- StopResetTests
- amazon-android-tool
- Ảnh hướng dẫn q1/q2 và menu chung lưu cục bộ
- open_home_menu
- MarketplaceFlowTests
- marketplace_flow.py
- screen
- Điều hướng hai dạng menu ba gạch
- CloudPhone
- core.py
- q7_state_machine.py
- Nghiên cứu và tích hợp Swarmote
- q7_state_machine.py
- amazon_is_foreground
- Window
- RegistrationState
- PROJECT_INDEX.md
- build_random_steps
- ui_backend.py
- vision.py
- subprocess
- _visible
- setup.py
- _type_field
- build_create_address_steps
- ._refresh_devices
- cli.py
- Bàn giao trạng thái dự án — 13/11/2026
- q7_random_prefix.py
- FakeControl
- Button
- build_post_auth_steps
- cloud_adb
- phone_window_layout.py
- cli.py
- SafetyTests
- b1–b11 Reliability and Latency Implementation Plan
- VisionFieldTests
- Danh mục ảnh nằm trong dự án
- StatusCell
- Amazon Android Tool — Giai đoạn A/B
- .test_creation_session_runs_b11_confirmation_through_b15_on_all_twelve_slots
- _CombinedStop
- Giao diện vận hành
- _recognize
- Amazon trên Swarmote
- CloudPhone
- build_reload_payment_steps
- Bộ cài chia sẻ Windows x64
- CountryRecoveryTests
- test_isolated_reader.py
- VERIFICATION.md
- BatchDraft
- _prepare_phone
- .test_b1_b2_wait_two_seconds_after_tap_before_view_scroll
- .test_table_has_all_twelve_slots_and_locked_controls_remain_visible
- PROJECT_HANDOFF.md
- _tail_menu
- validate_card
- swarmote_desktop.py
- account_flow.py
- _choose_tail_target
- _tail_candidates
- PLAN.md
- Luồng q1 từ menu ba gạch tới nhập OTP
- Q5_FLOW.md
- RunJob
- OTP_DESIGN.md
- ensure_manager_ready
- Giai đoạn 2 — bản thử State Machine riêng q7
- GRAPH_AUDIT.md

## God Nodes (most connected - your core abstractions)
1. `ToolError` - 354 edges
2. `CloudPhone` - 234 edges
3. `AttemptDeadline` - 202 edges
4. `RunJob` - 170 edges
5. `RegistrationState` - 162 edges
6. `build_common_steps()` - 115 edges
7. `Window` - 108 edges
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

## Communities (86 total, 12 thin omitted)

### Community 0 - "registration.py"
Cohesion: 0.20
Nodes (13): require_online(), ToolError, _field_for_label(), fill_identifier(), fill_signup_form(), _nodes(), open_entry(), _tap() (+5 more)

### Community 1 - "build_common_steps"
Cohesion: 0.05
Nodes (6): build_common_steps(), node(), Q1FlowTests, read(), provider_read(), read()

### Community 2 - "otp.py"
Cohesion: 0.10
Nodes (9): browser_launch_options(), extract_otp(), _NoRedirect, read_otp(), _read_otp_in_browser(), validate_otp_url(), wait_for_new_otp(), OtpTests (+1 more)

### Community 3 - "BulkInputTests"
Cohesion: 0.06
Nodes (11): BulkRecord, lines(), parse_bulk_payload(), parse_column(), parse_records(), _proxy_rows(), _table_cells(), _url_from_cell() (+3 more)

### Community 4 - "windows_identity.py"
Cohesion: 0.17
Nodes (8): create_shortcut(), relaunch_command(), runtime(), set_process_identity(), set_tk_icon(), set_window_identity(), Sửa shortcut ghim mở nhầm IDLE — 13/11/2026, WindowsIdentityTests

### Community 5 - "swarmote_desktop.py"
Cohesion: 0.08
Nodes (31): ready_for_home_menu(), _check_stop(), collapse_apps_panel(), install_amazon(), collect(), open_adb_shell(), _pause(), _phone_window() (+23 more)

### Community 6 - "RunnerTests"
Cohesion: 0.05
Nodes (22): ProfileRegistry, ProfileLookupError, ProfileNotFound, Thiết kế yêu cầu, absent(), ProfileRegistryTests, lookup(), broken() (+14 more)

### Community 7 - "PostMenuStep"
Cohesion: 0.07
Nodes (16): PostMenuSession, PostMenuStep, Một quy luật để sửa mã về sau — 20/11/2026, PostMenuTests, first_step(), reconcile(), first(), fail() (+8 more)

### Community 8 - "ToolError"
Cohesion: 0.10
Nodes (8): ProfileStartNotSubmitted, start_profile(), BatchStartTests, checkbox(), toggle(), descendants(), FakeBox, FakeButton

### Community 9 - "AddressDetailTests"
Cohesion: 0.12
Nodes (8): build_create_address_detail_steps(), _street_field(), AddressDetailTests, read(), adb(), tap(), read(), item()

### Community 10 - "003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật"
Cohesion: 0.05
Nodes (32): 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Rủi ro và bảo trì, Thiết kế yêu cầu, Điều kiện dừng, 002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ (+24 more)

### Community 11 - "Danh mục từng bước đã biết — 13/11/2026"
Cohesion: 0.06
Nodes (36): B1–B3 hiện hành — Ba lượt ngẫu nhiên q1–q12, Bản thử q7 State Machine — 14/11/2026, Chung b10 — Chuyển WhatsApp sang SMS, Chung b11 — Lấy và gõ OTP SMS, Chung b11a — Chạm ô OTP trên màn SMS, Chung b11b — Xác minh đăng nhập hoặc bấm Create của luồng tạo, Chung b4 — Sign In từ menu, Chung b4a — Chạm ô SĐT (+28 more)

### Community 12 - "RegistrationState"
Cohesion: 0.09
Nodes (9): RegistrationState, build_random_steps(), finish_view(), B1–b3 xem menu ngẫu nhiên cho 12 máy — 14/11/2026, Q5FlowTests, adb(), adb(), adb() (+1 more)

### Community 13 - "StopResetTests"
Cohesion: 0.07
Nodes (3): retry_preparation(), P03 — Mở form New Profile, StopResetTests

### Community 16 - "Ảnh hướng dẫn q1/q2 và menu chung lưu cục bộ"
Cohesion: 0.07
Nodes (29): 14 ảnh menu chung b1–b3 ngẫu nhiên — 14/11/2026, B16–b22 chung — Đổi marketplace sang United States (18/11/2026), B32–b39 — Reload Balance, thêm thẻ và địa chỉ thanh toán (21/11/2026), B6 — Hai ảnh đính kèm mới ngày 13/11/2026, Menu chung ảnh 01 — Danh sách chữ, Menu chung ảnh 02 — App Store bên phải sau khi Amazon mở, q1 b6 — US +1 hiện nhưng chạm không đóng hộp, 14/11/2026, q1 ảnh 01 — Menu và ba thẻ (+21 more)

### Community 17 - "open_home_menu"
Cohesion: 0.07
Nodes (14): _confirm_menu_fallback(), _menu_evidence(), MenuReadUnavailable, _nodes(), budget(), open_home_menu(), _tap(), _start_and_confirm() (+6 more)

### Community 18 - "MarketplaceFlowTests"
Cohesion: 0.07
Nodes (23): AttemptDeadline, MarketplaceFlowTests, read(), adb(), read(), tap(), read(), read() (+15 more)

### Community 19 - "marketplace_flow.py"
Cohesion: 0.16
Nodes (28): _read_hierarchy(), _account_tab(), build_marketplace_steps(), run(), account_target(), back_and_read_text(), foreground_ready(), recover_country_list() (+20 more)

### Community 20 - "screen"
Cohesion: 0.10
Nodes (33): _at_or_after(), sign_in(), _ensure_menu(), _find_scrolling(), home_visible(), menu_layout(), _read_nodes(), route_list_menu() (+25 more)

### Community 21 - "Điều hướng hai dạng menu ba gạch"
Cohesion: 0.50
Nodes (4): Bằng chứng và phạm vi, Kiểm chứng, Quy tắc chạy, Điều hướng hai dạng menu ba gạch

### Community 22 - "CloudPhone"
Cohesion: 0.08
Nodes (12): verify_menu_open(), CloudPhone, reconcile(), category_action(), build_q3_steps(), build_q4_steps(), build_q5_steps(), MenuReturnTests (+4 more)

### Community 23 - "core.py"
Cohesion: 0.20
Nodes (27): adb(), app_data_dir(), available_memory_mb(), avd_names(), check_play(), configure_avd(), connected_devices(), create_avd() (+19 more)

### Community 24 - "q7_state_machine.py"
Cohesion: 0.14
Nodes (12): ActionValidator, _already_reached_result(), _browse_ready_after_sms(), run(), _past_known_step(), RecoveryHandler, StateMachineStop, StateMachineTimeout (+4 more)

### Community 25 - "Nghiên cứu và tích hợp Swarmote"
Cohesion: 0.40
Nodes (4): Hành vi có bằng chứng, Kiểm thử còn lại, Nghiên cứu và tích hợp Swarmote, Phần đã áp dụng

### Community 26 - "q7_state_machine.py"
Cohesion: 0.16
Nodes (5): build_q7_pilot_steps(), ResultVerifier, StateDeadline, StateDetector, Q7StateMachineTests

### Community 28 - "amazon_is_foreground"
Cohesion: 0.16
Nodes (3): amazon_is_foreground(), CloudBridgeTests, adb()

### Community 29 - "Window"
Cohesion: 0.11
Nodes (5): main(), Window, emit(), Các bước, PreparationProgressTests

### Community 30 - "RegistrationState"
Cohesion: 0.10
Nodes (5): build_tail_steps(), open_menu(), view(), visit_seconds(), RandomPrefixTests

### Community 31 - "PROJECT_INDEX.md"
Cohesion: 0.23
Nodes (5): Bản đồ repository, Luồng q2 từ menu ba gạch, q3 — b1–b3 và nối luồng chung, q4 — Giỏ hàng, Pets, Home and DIY, q6 — Trang chủ, Giỏ hàng, menu và một thẻ

### Community 32 - "build_random_steps"
Cohesion: 0.11
Nodes (4): RandomPrefixTests, adb(), adb(), adb()

### Community 33 - "ui_backend.py"
Cohesion: 0.13
Nodes (11): swarmote_adb_path(), swarmote_tunnel_owner(), _connect(), country_reverse_points(), country_scroll(), _failed(), read_tree(), ready() (+3 more)

### Community 34 - "vision.py"
Cohesion: 0.12
Nodes (10): _bounds(), _canonical_text(), _compact(), _field_contents(), _field_is_blank(), _join_wrapped_categories(), _normalize(), ocr_nodes() (+2 more)

### Community 35 - "subprocess"
Cohesion: 0.10
Nodes (19): save(), default_path(), AppSettings, load_settings(), save_settings(), settings_path(), main(), check_runtime() (+11 more)

### Community 36 - "_visible"
Cohesion: 0.11
Nodes (32): _resume_address_payment_index(), _text(), _visible(), _action(), _address_form(), _addresses(), _bounded_native(), run() (+24 more)

### Community 37 - "setup.py"
Cohesion: 0.46
Nodes (4): confirm(), download_commandline_tools(), official_commandline_archive(), setup_sdk()

### Community 38 - "_type_field"
Cohesion: 0.18
Nodes (4): enter_otp(), _type_field(), FlowRecoveryTests, form()

### Community 39 - "build_create_address_steps"
Cohesion: 0.24
Nodes (4): build_create_address_steps(), CreateAddressFlowTests, read(), node()

### Community 41 - "cli.py"
Cohesion: 0.17
Nodes (8): BatchItem, parse_proxy_line(), prepare_five(), create_profile(), ProxyConfig, Mục tiêu và bằng chứng, BatchSafetyTests, CreationWindowVisibilityTests

### Community 42 - "Bàn giao trạng thái dự án — 13/11/2026"
Cohesion: 0.08
Nodes (24): main(), B6 danh sách quốc gia vẫn mở sau khi chọn — 13/11/2026, Bàn giao trạng thái dự án — 13/11/2026, Bản chính boom4may và bản dự phòng — 14/11/2026, Bộ cài offline chia sẻ — 14/11/2026, Cài đặt máy mới, Dừng riêng máy đang chọn — 14/11/2026, Dự phòng dùng chung khi chạy song song — 14/11/2026 (+16 more)

### Community 43 - "q7_random_prefix.py"
Cohesion: 0.10
Nodes (26): scroll_view(), wait_until(), cloud_adb(), foreground(), reported_installer(), RecoverableStepError, build_random_steps(), browse() (+18 more)

### Community 44 - "FakeControl"
Cohesion: 0.13
Nodes (5): ParallelInstallTests, PhoneWindow, FakeControl, InstallTests, descendants()

### Community 45 - "Button"
Cohesion: 0.14
Nodes (7): Button, Entry, FooterNote, icon(), state_style(), status_title(), ui_font()

### Community 46 - "build_post_auth_steps"
Cohesion: 0.22
Nodes (9): Hướng dẫn khi tiếp tục dự án, build_post_auth_steps(), Nhận diện giao diện lúc chạy, Nhập liệu và lỗi, Quy tắc tự động hóa sau menu ba gạch, Trạng thái hiện tại của dự án, Từng máy độc lập, Chung b16–b22 — Tài khoản và marketplace United States (+1 more)

### Community 47 - "cloud_adb"
Cohesion: 0.26
Nodes (12): _keyboard_visible(), _foreground(), type_characters(), _add_button(), step(), _card_parts(), _field_target(), _find() (+4 more)

### Community 48 - "phone_window_layout.py"
Cohesion: 0.14
Nodes (5): arrange_on_open(), _row_if_fits(), _sort_key(), _tiles(), PhoneWindowLayoutTests

### Community 49 - "cli.py"
Cohesion: 0.17
Nodes (12): main(), parser(), report(), cloud_serials(), scan(), get_device(), print_json(), Store (+4 more)

### Community 51 - "b1–b11 Reliability and Latency Implementation Plan"
Cohesion: 0.18
Nodes (10): b1–b11 Reliability and Latency Implementation Plan, Completion Criteria, File Map, Global Constraints, Review Focus, Task 1: Measure current step latency and classify existing failures, Task 2: Define safe retry, reconcile, pause, and stop behavior, Task 3: Reduce redundant UI reads and unnecessary waits (+2 more)

### Community 52 - "VisionFieldTests"
Cohesion: 0.24
Nodes (3): _input_box(), detection(), VisionFieldTests

### Community 53 - "Danh mục ảnh nằm trong dự án"
Cohesion: 0.18
Nodes (11): amazon_android/assets/icons/, amazon_android/assets/obsidian_prism.png, amazon_android/assets/swarmote_tool_square.png và swarmote_tool.ico, assets/ui_history/machine7_input_before.png, assets/ui_history/reset_check.png, assets/ui_history/ui-12.png, assets/ui_history/ui_palette_preview.png, assets/ui_history/ui-preview.png (+3 more)

### Community 54 - "StatusCell"
Cohesion: 0.13
Nodes (3): StatusCell, TableText, Tooltip

### Community 55 - "Amazon Android Tool — Giai đoạn A/B"
Cohesion: 0.29
Nodes (7): Amazon Android Tool — Giai đoạn A/B, Cài trên máy Windows mới, Dán nhiều proxy, Sử dụng, Trạng thái nghiệm thu, Yêu cầu, Điện thoại đám mây Swarmote

### Community 56 - ".test_creation_session_runs_b11_confirmation_through_b15_on_all_twelve_slots"
Cohesion: 0.14
Nodes (3): browse(), tap(), tap()

### Community 58 - "Giao diện vận hành"
Cohesion: 0.33
Nodes (5): Bố cục, Giao diện vận hành, Hướng thị giác, Quy tắc, Swarmote V3 — nghiệm thu 27/11/2026

### Community 59 - "_recognize"
Cohesion: 0.21
Nodes (6): _engine(), _recognize(), check(), ParallelOcrTests, engine(), read()

### Community 60 - "Amazon trên Swarmote"
Cohesion: 0.33
Nodes (5): Amazon trên Swarmote, Người dùng và công việc, Nền tảng, Điều chưa xác minh, Định hướng ngôn ngữ nếu xây dựng lại — 23/11/2026

### Community 61 - "CloudPhone"
Cohesion: 0.08
Nodes (26): b6 Country US +1 — 14/11/2026, B6 cuộn quốc gia và chọn lại — 13/11/2026, Biên bản kiểm tra thực tế — 2026-11-12, Cài và đo UiAutomator2 theo phê duyệt mới — 13/11/2026, Cập nhật luồng mẻ trước đó — 2026-11-13, Dừng riêng một máy — 14/11/2026, Focus ô nhập b4–b11 — 14/11/2026, Ghim taskbar — 13/11/2026 (+18 more)

### Community 62 - "build_reload_payment_steps"
Cohesion: 0.13
Nodes (9): build_reload_payment_steps(), node(), ReloadPaymentTests, adb(), wait(), read(), read(), read() (+1 more)

### Community 63 - "Bộ cài chia sẻ Windows x64"
Cohesion: 0.50
Nodes (3): Bộ cài chia sẻ Windows x64, Dựng lại, Nguồn thành phần

### Community 64 - "CountryRecoveryTests"
Cohesion: 0.17
Nodes (9): _same_country_position(), _scroll_up(), read_menu(), return_to_menu(), action(), CountryRecoveryTests, read(), wait() (+1 more)

### Community 65 - "test_isolated_reader.py"
Cohesion: 0.15
Nodes (14): _read_login_sms_visual(), _read_nodes_once(), _read_visual_nodes(), current(), phone_reader(), PhoneReader, ReaderResponseError, _serve() (+6 more)

### Community 66 - "VERIFICATION.md"
Cohesion: 0.17
Nodes (10): Kết luận và tích hợp, Kết quả thực tế, So sánh bộ đọc trên q1 — 13/11/2026, Thành phần thiết bị, b1–b3 bắt buộc có ba cú bấm — 14/11/2026, b1–b3 ngẫu nhiên cho 12 máy — 14/11/2026, b1–b3 ngẫu nhiên trên 12 máy, không dùng OCR — 14/11/2026, b6 cuộn tới đáy rồi vuốt ngược — 14/11/2026 (+2 more)

### Community 68 - "_prepare_phone"
Cohesion: 0.13
Nodes (17): open_amazon(), package_path(), probe(), prop(), _phone_preparation_lock(), _prepare_phone(), _prepare_phone_locked(), progress() (+9 more)

### Community 70 - ".test_table_has_all_twelve_slots_and_locked_controls_remain_visible"
Cohesion: 0.40
Nodes (3): DesktopLayoutTests, __init__(), __init__()

### Community 71 - "PROJECT_HANDOFF.md"
Cohesion: 0.10
Nodes (19): visit(), b1–b3 ngẫu nhiên cho q1–q12 — 14/11/2026, B4–b11 chạy đồng thời và OCR — 14/11/2026, b6 US +1 còn mở sau bốn cú chạm — 14/11/2026, Bản thử State Machine q7 và b1–b3 mở mục con — 14/11/2026, Bỏ thời hạn tổng sau menu — 14/11/2026, Bổ sung đọc ảnh OCR và chạm trực tiếp dự phòng cho b26 khi uiautomator dump WebView lỗi — 19/11/2026, Cơ chế chụp ảnh OCR quét chữ ấn luôn cho toàn bộ b26–b31 — 19/11/2026 (+11 more)

### Community 72 - "_tail_menu"
Cohesion: 0.18
Nodes (5): _UiReadIncomplete, _tail_menu(), Chung b12–b15 — Mở ba gạch rồi ba lượt điều hướng ngẫu nhiên, fail(), read()

### Community 73 - "validate_card"
Cohesion: 0.12
Nodes (4): validate_card(), _automatic_resume_slots(), otp_token(), Trạng thái kiểm chứng và giới hạn

### Community 74 - "swarmote_desktop.py"
Cohesion: 0.07
Nodes (32): _activate_manager(), _create_profile_form(), _descendants(), _invoke(), _main_window(), _one(), _open_profiles(), _profile_checkbox() (+24 more)

### Community 75 - "account_flow.py"
Cohesion: 0.09
Nodes (39): _ActionNotResolved, _bounds(), confirmed_login_otp_nodes(), continue_number(), country(), finish_auto(), finish_create(), finish_login() (+31 more)

### Community 76 - "_choose_tail_target"
Cohesion: 0.25
Nodes (4): _choose_tail_target(), _TailChoicesExhausted, choose(), choose()

### Community 83 - "RunJob"
Cohesion: 0.12
Nodes (9): AccountData, RunJob, DesktopResumeTests, apartment_type(), PreparationThreadsTests, run(), install(), install() (+1 more)

### Community 84 - "OTP_DESIGN.md"
Cohesion: 0.50
Nodes (3): Nối vào bước tạo tài khoản sau khi xác minh màn hình Amazon, Thiết kế OTP cho từng Profile, Đã chuẩn bị

### Community 85 - "ensure_manager_ready"
Cohesion: 0.28
Nodes (4): ensure_manager_ready(), ProfileManagerWindowError, ManagerStartupTests, unavailable()

### Community 87 - "Giai đoạn 2 — bản thử State Machine riêng q7"
Cohesion: 0.40
Nodes (5): Cách thử bản pilot cũ (không áp dụng cho factory hiện hành), Giai đoạn 2 — bản thử State Machine riêng q7, Giới hạn, Phạm vi và quan hệ với luồng cũ, Sơ đồ

### Community 92 - "GRAPH_AUDIT.md"
Cohesion: 0.50
Nodes (3): Cách kiểm tra sau mỗi sửa đổi, Giới hạn đã xác nhận, Kiểm tra độ phủ Graphify — cập nhật 26/11/2026

## Knowledge Gaps
- **1 isolated node(s):** `amazon-android-tool`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 553 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ToolError` connect `registration.py` to `build_common_steps`, `otp.py`, `BulkInputTests`, `swarmote_desktop.py`, `RunnerTests`, `PostMenuStep`, `ToolError`, `AddressDetailTests`, `RegistrationState`, `StopResetTests`, `cloud.py`, `open_home_menu`, `MarketplaceFlowTests`, `marketplace_flow.py`, `screen`, `CloudPhone`, `core.py`, `q7_state_machine.py`, `q7_state_machine.py`, `amazon_is_foreground`, `Window`, `RegistrationState`, `build_random_steps`, `ui_backend.py`, `vision.py`, `subprocess`, `_visible`, `setup.py`, `_type_field`, `build_create_address_steps`, `cli.py`, `q7_random_prefix.py`, `Button`, `cloud_adb`, `cli.py`, `_recognize`, `build_reload_payment_steps`, `CountryRecoveryTests`, `test_isolated_reader.py`, `BatchDraft`, `_prepare_phone`, `PROJECT_HANDOFF.md`, `_tail_menu`, `validate_card`, `swarmote_desktop.py`, `account_flow.py`, `_choose_tail_target`, `RunJob`, `ensure_manager_ready`?**
  _High betweenness centrality (0.362) - this node is a cross-community bridge._
- **Are the 58 inferred relationships involving `ToolError` (e.g. with `_read_nodes_once()` and `_resume_address_payment_index()`) actually correct?**
  _`ToolError` has 58 INFERRED edges - model-reasoned connections that need verification._
- **What connects `amazon-android-tool` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `build_common_steps` be split into smaller, more focused modules?**
  _Cohesion score 0.0522466039707419 - nodes in this community are weakly interconnected._
- **Why does `RunJob` connect `RunJob` to `build_common_steps`, `BulkInputTests`, `swarmote_desktop.py`, `RunnerTests`, `PostMenuStep`, `RegistrationState`, `StopResetTests`, `cloud.py`, `MarketplaceFlowTests`, `screen`, `CloudPhone`, `q7_state_machine.py`, `q7_state_machine.py`, `Window`, `RegistrationState`, `build_random_steps`, `subprocess`, `_type_field`, `._refresh_devices`, `cli.py`, `q7_random_prefix.py`, `Button`, `build_post_auth_steps`, `.test_creation_session_runs_b11_confirmation_through_b15_on_all_twelve_slots`, `build_reload_payment_steps`, `CountryRecoveryTests`, `_prepare_phone`, `validate_card`, `account_flow.py`, `_choose_tail_target`, `OTP_DESIGN.md`?**
  _High betweenness centrality (0.104) - this node is a cross-community bridge._
- **Are the 88 inferred relationships involving `CloudPhone` (e.g. with `build_common_steps()` and `_country_full_row()`) actually correct?**
  _`CloudPhone` has 88 INFERRED edges - model-reasoned connections that need verification._
- **Should `otp.py` be split into smaller, more focused modules?**
  _Cohesion score 0.09848484848484848 - nodes in this community are weakly interconnected._