# Graph Report - bom4may  (2026-11-28)

## Corpus Check
- 144 files · ~188,323 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 2, .bat 1, .pyw 1)

## Summary
- 2465 nodes · 8652 edges · 94 communities (79 shown, 15 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 1249 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `9e69540e`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- reload_payment_flow.py
- Q1FlowTests
- otp.py
- BulkInputTests
- ProxyConfig
- open_adb_shell
- RunnerTests
- PostMenuStep
- .test_only_confirmed_target_names_are_selected_for_one_start_command
- build_create_address_detail_steps
- 003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật
- Danh mục từng bước đã biết — 13/11/2026
- unittest
- StopResetTests
- account_flow.py
- amazon-android-tool
- Ảnh hướng dẫn q1/q2 và menu chung lưu cục bộ
- ._open_settings
- AttemptDeadline
- CloudPhone
- phone_window_layout.py
- MENU_ROUTING.md
- Q3Q4FlowTests
- _type_field
- phone_window_layout.py
- Nghiên cứu và tích hợp Swarmote
- ._run
- change_us_flow.py
- core.py
- subprocess
- PROJECT_INDEX.md
- RandomPrefixTests
- core.py
- vision.py
- desktop.py
- _visible
- time
- retry_preparation
- build_create_address_steps
- main
- cli.py
- _read_nodes
- FakeControl
- desktop_theme.py
- ToolError
- ._refresh_devices
- Swarmote V3 — đối chiếu ảnh mẫu 27/11/2026
- cli.py
- bulk_input.py
- b1–b11 Reliability and Latency Implementation Plan
- desktop.py
- Danh mục ảnh nằm trong dự án
- _yellow_form_button
- Amazon Android Tool — Giai đoạn A/B
- StatusCell
- cli.py
- ._continue_profile
- _restore_prefix_menu
- Amazon trên Swarmote
- home_menu.py
- build_reload_payment_steps
- Bộ cài chia sẻ Windows x64
- CountryRecoveryTests
- PhoneReader
- VERIFICATION.md
- BatchDraft
- .test_single_row_paste_and_clear_touch_only_selected_failed_machine
- create_profile
- Proxy dự phòng trong RAM Implementation Plan
- PROJECT_HANDOFF.md
- windows_identity.py
- CloudPhone
- ProfilesNavigationTests
- build_q1_steps
- status_title
- .test_creation_session_runs_b11_confirmation_through_b15_on_all_twelve_slots
- _TailChoicesExhausted
- CountryRecoveryTests
- screen
- swarmote_desktop.py
- batch.py
- isolated_reader.py
- OTP_DESIGN.md
- ensure_manager_ready
- _scroll_up
- RegistrationState
- ToolError
- _proxy_postal_prefix
- ._run_preparation_retry
- GRAPH_AUDIT.md
- cloud_adb
- OTP_DESIGN.md

## God Nodes (most connected - your core abstractions)
1. `ToolError` - 372 edges
2. `CloudPhone` - 238 edges
3. `AttemptDeadline` - 227 edges
4. `RunJob` - 181 edges
5. `RegistrationState` - 166 edges
6. `Window` - 123 edges
7. `build_common_steps()` - 115 edges
8. `PostMenuStep` - 100 edges
9. `PostMenuSession` - 93 edges
10. `Q1FlowTests` - 92 edges

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

## Communities (94 total, 15 thin omitted)

### Community 0 - "reload_payment_flow.py"
Cohesion: 0.30
Nodes (10): _read_text_region(), _add_button(), step(), _card_parts(), _field_target(), _find(), _input(), _read_until() (+2 more)

### Community 1 - "Q1FlowTests"
Cohesion: 0.06
Nodes (4): build_common_steps(), node(), Q1FlowTests, provider_read()

### Community 2 - "otp.py"
Cohesion: 0.10
Nodes (9): browser_launch_options(), extract_otp(), _NoRedirect, read_otp(), _read_otp_in_browser(), validate_otp_url(), wait_for_new_otp(), OtpTests (+1 more)

### Community 4 - "ProxyConfig"
Cohesion: 0.17
Nodes (7): proxy_key(), ProxyReserve, ProxyConfig, proxy(), ProxyReserveTests, create(), create()

### Community 5 - "open_adb_shell"
Cohesion: 0.08
Nodes (31): ready_for_home_menu(), _check_stop(), collapse_apps_panel(), install_amazon(), collect(), open_adb_shell(), _pause(), _phone_window() (+23 more)

### Community 6 - "RunnerTests"
Cohesion: 0.05
Nodes (19): ProfileRegistry, absent(), ProfileRegistryTests, lookup(), broken(), RunnerTests, create(), resume() (+11 more)

### Community 7 - "PostMenuStep"
Cohesion: 0.06
Nodes (22): reconcile(), route(), PostMenuSession, at_create_b13(), pause_if_requested(), PostMenuStep, Công tắc dừng trước b13 của luồng Tạo, Công việc (+14 more)

### Community 8 - ".test_only_confirmed_target_names_are_selected_for_one_start_command"
Cohesion: 0.11
Nodes (6): BatchStartTests, checkbox(), toggle(), descendants(), FakeBox, FakeButton

### Community 9 - "build_create_address_detail_steps"
Cohesion: 0.12
Nodes (7): build_create_address_detail_steps(), AddressDetailTests, read(), adb(), tap(), read(), item()

### Community 10 - "003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật"
Cohesion: 0.06
Nodes (27): 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Rủi ro và bảo trì, Thiết kế yêu cầu, Điều kiện dừng, 003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật (+19 more)

### Community 11 - "Danh mục từng bước đã biết — 13/11/2026"
Cohesion: 0.06
Nodes (36): Bản thử q7 State Machine — 14/11/2026, Chung b10 — Chuyển WhatsApp sang SMS, Chung b11 — Lấy và gõ OTP SMS, Chung b11a — Chạm ô OTP trên màn SMS, Chung b11b — Xác minh đăng nhập hoặc bấm Create của luồng tạo, Chung b12–b15 — Mở ba gạch rồi ba lượt điều hướng ngẫu nhiên, Chung b4 — Sign In từ menu, Chung b4a — Chạm ô SĐT (+28 more)

### Community 14 - "account_flow.py"
Cohesion: 0.16
Nodes (3): _ActionNotResolved, _visual_form_button(), cloud_screenshot()

### Community 16 - "Ảnh hướng dẫn q1/q2 và menu chung lưu cục bộ"
Cohesion: 0.07
Nodes (28): B16–b22 chung — Đổi marketplace sang United States (18/11/2026), B32–b39 — Reload Balance, thêm thẻ và địa chỉ thanh toán (21/11/2026), B6 — Hai ảnh đính kèm mới ngày 13/11/2026, Menu chung ảnh 01 — Danh sách chữ, Menu chung ảnh 02 — App Store bên phải sau khi Amazon mở, q1 b6 — US +1 hiện nhưng chạm không đóng hộp, 14/11/2026, q1 ảnh 01 — Menu và ba thẻ, q1 ảnh 02 — Sign In cuối menu (+20 more)

### Community 17 - "._open_settings"
Cohesion: 0.20
Nodes (5): Settings hiện chậm — 14/11/2026, __init__(), descendants(), __init__(), __init__()

### Community 18 - "AttemptDeadline"
Cohesion: 0.05
Nodes (25): AttemptDeadline, ChangeUsFlowTests, node(), MarketplaceFlowTests, read(), adb(), read(), tap() (+17 more)

### Community 19 - "CloudPhone"
Cohesion: 0.09
Nodes (17): amazon_is_foreground(), cloud_serials(), CloudPhone, open_amazon(), foreground(), package_path(), probe(), prop() (+9 more)

### Community 20 - "phone_window_layout.py"
Cohesion: 0.14
Nodes (5): arrange_on_open(), _row_if_fits(), _sort_key(), _tiles(), PhoneWindowLayoutTests

### Community 21 - "MENU_ROUTING.md"
Cohesion: 0.50
Nodes (4): Bằng chứng và phạm vi, Kiểm chứng, Quy tắc chạy, Điều hướng hai dạng menu ba gạch

### Community 22 - "Q3Q4FlowTests"
Cohesion: 0.21
Nodes (3): build_q3_steps(), build_q4_steps(), Q3Q4FlowTests

### Community 23 - "_type_field"
Cohesion: 0.13
Nodes (47): confirmed_login_otp_nodes(), continue_number(), enter_otp(), finish_auto(), finish_create(), finish_login(), focus_otp(), focus_phone() (+39 more)

### Community 24 - "phone_window_layout.py"
Cohesion: 0.08
Nodes (17): ActionValidator, _already_reached_result(), build_q7_pilot_steps(), run(), _past_known_step(), RecoveryHandler, ResultVerifier, StateDeadline (+9 more)

### Community 25 - "Nghiên cứu và tích hợp Swarmote"
Cohesion: 0.40
Nodes (4): Hành vi có bằng chứng, Kiểm thử còn lại, Nghiên cứu và tích hợp Swarmote, Phần đã áp dụng

### Community 26 - "._run"
Cohesion: 0.17
Nodes (25): b2(), _account_tab(), build_marketplace_steps(), run(), account_target(), back_and_read_text(), foreground_ready(), recover_country_list() (+17 more)

### Community 27 - "change_us_flow.py"
Cohesion: 0.17
Nodes (13): _account_icon_from_image(), _after_back(), _browse(), b16(), b17(), _google_sheet(), _observe(), _passkey_page() (+5 more)

### Community 28 - "core.py"
Cohesion: 0.17
Nodes (16): app_data_dir(), available_memory_mb(), avd_names(), configure_avd(), create_avd(), doctor(), emulator_serials(), executable() (+8 more)

### Community 30 - "subprocess"
Cohesion: 0.18
Nodes (12): main(), check_runtime(), main(), verify(), _app_installed(), _app_paths(), _check_external_apps(), _install_python_dependencies() (+4 more)

### Community 31 - "PROJECT_INDEX.md"
Cohesion: 0.15
Nodes (9): Quy trình Swarmote hiện tại, Bản đồ repository, Luồng q1 từ menu ba gạch tới nhập OTP, Thử trên q1 đã có, Luồng q2 từ menu ba gạch, q3 — b1–b3 và nối luồng chung, q4 — Giỏ hàng, Pets, Home and DIY, q5 — ba thẻ riêng và b4–b11 chung (+1 more)

### Community 32 - "RandomPrefixTests"
Cohesion: 0.11
Nodes (4): RandomPrefixTests, adb(), adb(), adb()

### Community 33 - "core.py"
Cohesion: 0.14
Nodes (10): swarmote_adb_path(), _connect(), country_reverse_points(), country_scroll(), _failed(), read_tree(), ready(), _session() (+2 more)

### Community 34 - "vision.py"
Cohesion: 0.14
Nodes (14): _read_login_sms_visual(), _read_nodes_once(), _read_visual_nodes(), _UiReadIncomplete, _visible_edit_fields(), current(), phone_reader(), PhoneReader (+6 more)

### Community 36 - "_visible"
Cohesion: 0.13
Nodes (34): _bounds(), _resume_address_payment_index(), _text(), _visible(), _menu_visible(), _action(), _address_form(), _addresses() (+26 more)

### Community 37 - "time"
Cohesion: 0.20
Nodes (11): _field_for_label(), fill_identifier(), fill_signup_form(), _nodes(), open_entry(), status(), _tap(), _type_into() (+3 more)

### Community 38 - "retry_preparation"
Cohesion: 0.20
Nodes (4): _type_field(), Phục hồi khi ô nhập chưa nhận focus ở b4–b11 — 14/11/2026, FlowRecoveryTests, form()

### Community 39 - "build_create_address_steps"
Cohesion: 0.24
Nodes (4): build_create_address_steps(), CreateAddressFlowTests, read(), node()

### Community 40 - "main"
Cohesion: 0.16
Nodes (9): main(), main(), Đợt tăng tốc và tự phục hồi b4–b11 ngày 13/11/2026, File dự án mà Graphify không phân tích trực tiếp, .gitignore, Launch Swarmote Tool.pyw, pyproject.toml, Ảnh PNG trong dự án (+1 more)

### Community 42 - "_read_nodes"
Cohesion: 0.17
Nodes (25): _at_or_after(), sign_in(), _country_nodes(), _CountryReadStop, _ensure_menu(), _find_scrolling(), home_visible(), _read_nodes() (+17 more)

### Community 44 - "FakeControl"
Cohesion: 0.13
Nodes (5): ParallelInstallTests, PhoneWindow, FakeControl, InstallTests, descendants()

### Community 45 - "desktop_theme.py"
Cohesion: 0.17
Nodes (7): Button, Entry, FooterNote, HeaderWave, icon(), ui_font(), section_heading()

### Community 46 - "ToolError"
Cohesion: 0.11
Nodes (3): Window, Các bước, PreparationProgressTests

### Community 48 - "Swarmote V3 — đối chiếu ảnh mẫu 27/11/2026"
Cohesion: 0.17
Nodes (11): Bố cục, Bố cục được áp dụng, Chữ và tiến độ, Giao diện vận hành, Hướng thị giác, Kiểm chứng và phạm vi, Kích thước và cuộn, Phân tích màu ảnh mẫu (+3 more)

### Community 49 - "cli.py"
Cohesion: 0.22
Nodes (5): _same_country_position(), CountryRecoveryTests, read(), wait(), node()

### Community 50 - "bulk_input.py"
Cohesion: 0.11
Nodes (9): BulkRecord, lines(), _markdown_cell_text(), parse_bulk_payload(), parse_column(), _proxy_rows(), _table_cells(), _url_from_cell() (+1 more)

### Community 51 - "b1–b11 Reliability and Latency Implementation Plan"
Cohesion: 0.18
Nodes (10): b1–b11 Reliability and Latency Implementation Plan, Completion Criteria, File Map, Global Constraints, Review Focus, Task 1: Measure current step latency and classify existing failures, Task 2: Define safe retry, reconcile, pause, and stop behavior, Task 3: Reduce redundant UI reads and unnecessary waits (+2 more)

### Community 52 - "desktop.py"
Cohesion: 0.07
Nodes (19): _bounds(), _canonical_text(), _compact(), _engine(), _field_contents(), _field_is_blank(), _input_box(), _join_wrapped_categories() (+11 more)

### Community 53 - "Danh mục ảnh nằm trong dự án"
Cohesion: 0.18
Nodes (11): amazon_android/assets/icons/, amazon_android/assets/obsidian_prism.png, amazon_android/assets/swarmote_tool_square.png và swarmote_tool.ico, assets/ui_history/machine7_input_before.png, assets/ui_history/reset_check.png, assets/ui_history/ui-12.png, assets/ui_history/ui_palette_preview.png, assets/ui_history/ui-preview.png (+3 more)

### Community 55 - "Amazon Android Tool — Giai đoạn A/B"
Cohesion: 0.29
Nodes (7): Amazon Android Tool — Giai đoạn A/B, Cài trên máy Windows mới, Dán nhiều proxy, Sử dụng, Trạng thái nghiệm thu, Yêu cầu, Điện thoại đám mây Swarmote

### Community 56 - "StatusCell"
Cohesion: 0.18
Nodes (9): _new_prefix(), save(), default_path(), AppSettings, load_settings(), save_settings(), settings_path(), Tăng số lần thử đọc cây Android và bổ sung phương án dự phòng cho b23–b31 — 19/11/2026 (+1 more)

### Community 57 - "cli.py"
Cohesion: 0.15
Nodes (22): main(), parser(), report(), adb(), check_play(), connected_devices(), Device, device_avd_name() (+14 more)

### Community 59 - "_restore_prefix_menu"
Cohesion: 0.18
Nodes (5): _prefix_nodes(), _PrefixRecoveryStop, _restore_prefix_menu(), 14 ảnh menu chung b1–b3 ngẫu nhiên — 14/11/2026, B1–B3 hiện hành — Ba lượt ngẫu nhiên q1–q12

### Community 60 - "Amazon trên Swarmote"
Cohesion: 0.33
Nodes (5): Amazon trên Swarmote, Người dùng và công việc, Nền tảng, Điều chưa xác minh, Định hướng ngôn ngữ nếu xây dựng lại — 23/11/2026

### Community 61 - "home_menu.py"
Cohesion: 0.08
Nodes (25): b6 Country US +1 — 14/11/2026, B6 cuộn quốc gia và chọn lại — 13/11/2026, Biên bản kiểm tra thực tế — 2026-11-12, Cài và đo UiAutomator2 theo phê duyệt mới — 13/11/2026, Dừng riêng một máy — 14/11/2026, Focus ô nhập b4–b11 — 14/11/2026, Ghim taskbar — 13/11/2026, Giao diện sáng, dễ đọc — 2026-11-13 (+17 more)

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
Cohesion: 0.22
Nodes (9): Hướng dẫn khi tiếp tục dự án, build_post_auth_steps(), Nhận diện giao diện lúc chạy, Nhập liệu và lỗi, Quy tắc tự động hóa sau menu ba gạch, Trạng thái hiện tại của dự án, Từng máy độc lập, Chung b16–b22 — Tài khoản và marketplace United States (+1 more)

### Community 66 - "VERIFICATION.md"
Cohesion: 0.17
Nodes (10): Kết luận và tích hợp, Kết quả thực tế, So sánh bộ đọc trên q1 — 13/11/2026, Thành phần thiết bị, b1–b3 bắt buộc có ba cú bấm — 14/11/2026, b1–b3 ngẫu nhiên cho 12 máy — 14/11/2026, b1–b3 ngẫu nhiên trên 12 máy, không dùng OCR — 14/11/2026, b6 cuộn tới đáy rồi vuốt ngược — 14/11/2026 (+2 more)

### Community 67 - "BatchDraft"
Cohesion: 0.16
Nodes (3): BatchDraft, BatchDraftTests, Value

### Community 68 - ".test_single_row_paste_and_clear_touch_only_selected_failed_machine"
Cohesion: 0.10
Nodes (19): _phone_preparation_lock(), _prepare_phone(), _prepare_phone_locked(), progress(), stop_here(), run_batch(), fill_slots(), manually_selected() (+11 more)

### Community 69 - "create_profile"
Cohesion: 0.12
Nodes (10): create_profile(), 002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ, Các bước, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Rủi ro và bảo trì, Thiết kế yêu cầu (+2 more)

### Community 70 - "Proxy dự phòng trong RAM Implementation Plan"
Cohesion: 0.29
Nodes (6): Global Constraints, Proxy dự phòng trong RAM Implementation Plan, Review Focus, Task 1: Pool và dán dự phòng, Task 2: Cấp phát và vòng đời mẻ, Task 3: Bố cục hẹp và xác minh

### Community 71 - "PROJECT_HANDOFF.md"
Cohesion: 0.13
Nodes (14): b1–b3 ngẫu nhiên cho q1–q12 — 14/11/2026, B4–b11 chạy đồng thời và OCR — 14/11/2026, b6 US +1 còn mở sau bốn cú chạm — 14/11/2026, Bản thử State Machine q7 và b1–b3 mở mục con — 14/11/2026, Bỏ thời hạn tổng sau menu — 14/11/2026, Bổ sung đọc ảnh OCR và chạm trực tiếp dự phòng cho b26 khi uiautomator dump WebView lỗi — 19/11/2026, Cơ chế chụp ảnh OCR quét chữ ấn luôn cho toàn bộ b26–b31 — 19/11/2026, Không bỏ qua b1–b3 ngẫu nhiên; 14 ảnh menu mới — 14/11/2026 (+6 more)

### Community 72 - "windows_identity.py"
Cohesion: 0.16
Nodes (8): create_shortcut(), relaunch_command(), runtime(), set_process_identity(), set_tk_icon(), set_window_identity(), Sửa shortcut ghim mở nhầm IDLE — 13/11/2026, WindowsIdentityTests

### Community 74 - "ProfilesNavigationTests"
Cohesion: 0.13
Nodes (8): control(), ProfilesNavigationTests, descendants(), descendants(), invoke(), descendants(), descendants(), descendants()

### Community 75 - "build_q1_steps"
Cohesion: 0.14
Nodes (7): build_q1_steps(), category(), build_q5_steps(), Cách xử lý ảnh tiếp theo, Phần riêng từng máy, Tiến độ hướng dẫn bằng ảnh — cập nhật 13/11/2026, Q6FlowTests

### Community 77 - ".test_creation_session_runs_b11_confirmation_through_b15_on_all_twelve_slots"
Cohesion: 0.29
Nodes (3): browse(), tap(), tap()

### Community 79 - "CountryRecoveryTests"
Cohesion: 0.10
Nodes (5): startup_geometry(), StatusCell, TableText, Tooltip, DesktopLayoutTests

### Community 80 - "screen"
Cohesion: 0.12
Nodes (16): country(), name(), phone_number(), proceed(), skip_creation_for_login(), menu_layout(), _registration_nodes(), route_list_menu() (+8 more)

### Community 81 - "swarmote_desktop.py"
Cohesion: 0.09
Nodes (29): _activate_manager(), _create_profile_form(), _descendants(), inspect(), _invoke(), _main_window(), _one(), _open_profiles() (+21 more)

### Community 82 - "batch.py"
Cohesion: 0.40
Nodes (4): BatchItem, parse_proxy_line(), prepare_five(), BatchSafetyTests

### Community 83 - "isolated_reader.py"
Cohesion: 0.07
Nodes (13): AccountData, retry_preparation(), RunJob, P03 — Mở form New Profile, DesktopResumeTests, apartment_type(), PreparationThreadsTests, run() (+5 more)

### Community 84 - "OTP_DESIGN.md"
Cohesion: 0.12
Nodes (15): B6 danh sách quốc gia vẫn mở sau khi chọn — 13/11/2026, Bàn giao trạng thái dự án — 13/11/2026, Bản chính boom4may và bản dự phòng — 14/11/2026, Bộ cài offline chia sẻ — 14/11/2026, Cài đặt máy mới, Dán bảng Amazon có ghi chú thẻ live và URL OTP escaped — 14/11/2026, Dừng riêng máy đang chọn — 14/11/2026, q3/q4 đã nối b1–b3 và thử đồng thời bốn luồng — 13/11/2026 (+7 more)

### Community 85 - "ensure_manager_ready"
Cohesion: 0.40
Nodes (5): Cách thử bản pilot cũ (không áp dụng cho factory hiện hành), Giai đoạn 2 — bản thử State Machine riêng q7, Giới hạn, Phạm vi và quan hệ với luồng cũ, Sơ đồ

### Community 86 - "_scroll_up"
Cohesion: 0.36
Nodes (9): _scroll_up(), open_menu(), read_menu(), return_to_menu(), view(), visit(), action(), visit_seconds() (+1 more)

### Community 87 - "RegistrationState"
Cohesion: 0.05
Nodes (17): resume_common_index(), RegistrationState, build_random_steps(), finish_view(), build_tail_steps(), _choose_tail_target(), B1–b3 xem menu ngẫu nhiên cho 12 máy — 14/11/2026, Dự phòng dùng chung khi chạy song song — 14/11/2026 (+9 more)

### Community 88 - "ToolError"
Cohesion: 0.07
Nodes (19): ToolError, _confirm_menu_fallback(), _menu_evidence(), MenuReadUnavailable, budget(), open_home_menu(), _tap(), _start_and_confirm() (+11 more)

### Community 89 - "_proxy_postal_prefix"
Cohesion: 0.48
Nodes (3): _proxy_postal_prefix(), controls(), ProxyPostalPrefixTests

### Community 92 - "GRAPH_AUDIT.md"
Cohesion: 0.50
Nodes (3): Cách kiểm tra sau mỗi sửa đổi, Giới hạn đã xác nhận, Kiểm tra độ phủ Graphify — cập nhật 26/11/2026

### Community 96 - "cloud_adb"
Cohesion: 0.09
Nodes (27): _country_full_row(), _keyboard_visible(), _parse_ui_nodes(), _read_hierarchy(), scroll_view(), wait_until(), cloud_adb(), RecoverableStepError (+19 more)

### Community 100 - "OTP_DESIGN.md"
Cohesion: 0.50
Nodes (3): Nối vào bước tạo tài khoản sau khi xác minh màn hình Amazon, Thiết kế OTP cho từng Profile, Đã chuẩn bị

## Knowledge Gaps
- **1 isolated node(s):** `amazon-android-tool`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 597 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **15 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ToolError` connect `ToolError` to `reload_payment_flow.py`, `Q1FlowTests`, `otp.py`, `BulkInputTests`, `ProxyConfig`, `open_adb_shell`, `RunnerTests`, `PostMenuStep`, `.test_only_confirmed_target_names_are_selected_for_one_start_command`, `build_create_address_detail_steps`, `unittest`, `StopResetTests`, `account_flow.py`, `AttemptDeadline`, `CloudPhone`, `_type_field`, `phone_window_layout.py`, `._run`, `change_us_flow.py`, `core.py`, `RandomPrefixTests`, `core.py`, `vision.py`, `desktop.py`, `_visible`, `time`, `retry_preparation`, `build_create_address_steps`, `cli.py`, `_read_nodes`, `ToolError`, `._refresh_devices`, `cli.py`, `bulk_input.py`, `desktop.py`, `StatusCell`, `cli.py`, `._continue_profile`, `_restore_prefix_menu`, `build_reload_payment_steps`, `BatchDraft`, `.test_single_row_paste_and_clear_touch_only_selected_failed_machine`, `create_profile`, `ProfilesNavigationTests`, `_TailChoicesExhausted`, `screen`, `swarmote_desktop.py`, `batch.py`, `isolated_reader.py`, `OTP_DESIGN.md`, `_scroll_up`, `RegistrationState`, `cloud_adb`?**
  _High betweenness centrality (0.364) - this node is a cross-community bridge._
- **Are the 63 inferred relationships involving `ToolError` (e.g. with `_read_nodes_once()` and `_resume_address_payment_index()`) actually correct?**
  _`ToolError` has 63 INFERRED edges - model-reasoned connections that need verification._
- **What connects `amazon-android-tool` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Q1FlowTests` be split into smaller, more focused modules?**
  _Cohesion score 0.06140350877192982 - nodes in this community are weakly interconnected._
- **Why does `CloudPhone` connect `CloudPhone` to `Q1FlowTests`, `open_adb_shell`, `PostMenuStep`, `build_create_address_detail_steps`, `unittest`, `account_flow.py`, `AttemptDeadline`, `Q3Q4FlowTests`, `_type_field`, `phone_window_layout.py`, `change_us_flow.py`, `RandomPrefixTests`, `core.py`, `vision.py`, `desktop.py`, `time`, `retry_preparation`, `build_create_address_steps`, `cli.py`, `_read_nodes`, `.remaining`, `ToolError`, `cli.py`, `cli.py`, `._continue_profile`, `build_reload_payment_steps`, `PhoneReader`, `.test_single_row_paste_and_clear_touch_only_selected_failed_machine`, `build_q1_steps`, `.test_creation_session_runs_b11_confirmation_through_b15_on_all_twelve_slots`, `screen`, `swarmote_desktop.py`, `isolated_reader.py`, `_scroll_up`, `RegistrationState`, `ToolError`, `cloud_adb`?**
  _High betweenness centrality (0.117) - this node is a cross-community bridge._
- **Are the 89 inferred relationships involving `CloudPhone` (e.g. with `build_common_steps()` and `_country_full_row()`) actually correct?**
  _`CloudPhone` has 89 INFERRED edges - model-reasoned connections that need verification._
- **Should `otp.py` be split into smaller, more focused modules?**
  _Cohesion score 0.10080645161290322 - nodes in this community are weakly interconnected._