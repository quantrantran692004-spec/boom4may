# Graph Report - bom4may  (2026-11-28)

## Corpus Check
- 143 files · ~187,008 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 2, .bat 1, .pyw 1)

## Summary
- 2453 nodes · 8612 edges · 93 communities (78 shown, 15 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 1238 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5aa35f2e`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- reload_payment_flow.py
- Q1FlowTests
- otp.py
- BulkInputTests
- ProxyConfig
- swarmote_desktop.py
- RunnerTests
- PostMenuStep
- .test_only_confirmed_target_names_are_selected_for_one_start_command
- build_create_address_detail_steps
- 003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật
- Danh mục từng bước đã biết — 13/11/2026
- ProfileRegistry
- StopResetTests
- amazon-android-tool
- Ảnh hướng dẫn q1/q2 và menu chung lưu cục bộ
- desktop_theme.py
- AttemptDeadline
- CloudPhone
- phone_window_layout.py
- MENU_ROUTING.md
- Q3Q4FlowTests
- _type_field
- phone_window_layout.py
- Nghiên cứu và tích hợp Swarmote
- ._run
- _after_back
- .test_both_modes_and_all_slots_share_one_continuation_extension_point
- RegistrationState
- PROJECT_INDEX.md
- RandomPrefixTests
- core.py
- vision.py
- ._refresh_devices
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
- account_flow.py
- Amazon Android Tool — Giai đoạn A/B
- StatusCell
- core.py
- .test_transition_keeps_observing_after_short_wait_without_tapping
- _prefix_nodes
- Amazon trên Swarmote
- home_menu.py
- build_reload_payment_steps
- Bộ cài chia sẻ Windows x64
- CountryRecoveryTests
- PhoneReader
- VERIFICATION.md
- AccountData
- .test_single_row_paste_and_clear_touch_only_selected_failed_machine
- Bàn giao dừng theo yêu cầu người dùng — 13/11/2026
- Proxy dự phòng trong RAM Implementation Plan
- PROJECT_HANDOFF.md
- Q2FlowTests
- CloudPhone
- ProfilesNavigationTests
- sys
- status_title
- subprocess
- BatchDraft
- CountryRecoveryTests
- test_q1_flow.py
- _create_profile_form
- Luồng q1 từ menu ba gạch tới nhập OTP
- isolated_reader.py
- OTP_DESIGN.md
- ensure_manager_ready
- Q5_FLOW.md
- File dự án mà Graphify không phân tích trực tiếp
- home_menu.py
- _proxy_postal_prefix
- GRAPH_AUDIT.md
- cloud_adb
- OTP_DESIGN.md

## God Nodes (most connected - your core abstractions)
1. `ToolError` - 372 edges
2. `CloudPhone` - 238 edges
3. `AttemptDeadline` - 227 edges
4. `RunJob` - 177 edges
5. `RegistrationState` - 166 edges
6. `Window` - 122 edges
7. `build_common_steps()` - 115 edges
8. `PostMenuStep` - 94 edges
9. `Q1FlowTests` - 92 edges
10. `PostMenuSession` - 88 edges

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

## Communities (93 total, 15 thin omitted)

### Community 0 - "reload_payment_flow.py"
Cohesion: 0.28
Nodes (11): _keyboard_visible(), _read_text_region(), _add_button(), step(), _card_parts(), _field_target(), _find(), _input() (+3 more)

### Community 1 - "Q1FlowTests"
Cohesion: 0.07
Nodes (4): build_common_steps(), node(), Q1FlowTests, provider_read()

### Community 2 - "otp.py"
Cohesion: 0.10
Nodes (9): browser_launch_options(), extract_otp(), _NoRedirect, read_otp(), _read_otp_in_browser(), validate_otp_url(), wait_for_new_otp(), OtpTests (+1 more)

### Community 3 - "BulkInputTests"
Cohesion: 0.05
Nodes (8): BatchDraft, BulkRecord, parse_bulk_payload(), parse_column(), parse_records(), BatchDraftTests, BulkInputTests, Value

### Community 4 - "ProxyConfig"
Cohesion: 0.17
Nodes (7): proxy_key(), ProxyReserve, ProxyConfig, proxy(), ProxyReserveTests, create(), create()

### Community 5 - "swarmote_desktop.py"
Cohesion: 0.08
Nodes (39): package_path(), _check_stop(), collapse_apps_panel(), _descendants(), ensure_manager_ready(), inspect(), install_amazon(), _main_window() (+31 more)

### Community 6 - "RunnerTests"
Cohesion: 0.07
Nodes (14): RunnerTests, create(), resume(), create(), failed_start(), resume(), run(), run() (+6 more)

### Community 7 - "PostMenuStep"
Cohesion: 0.07
Nodes (17): reconcile(), route(), PostMenuSession, PostMenuStep, PostMenuTests, first_step(), reconcile(), first() (+9 more)

### Community 8 - ".test_only_confirmed_target_names_are_selected_for_one_start_command"
Cohesion: 0.06
Nodes (18): verify_menu_open(), ToolError, _start_and_confirm(), create_profile(), check_stop(), ProfileStartNotSubmitted, Mục tiêu và bằng chứng, Tự phục hồi lỗi tạm thời trong mẻ nhiều máy — 14/11/2026 (+10 more)

### Community 9 - "build_create_address_detail_steps"
Cohesion: 0.12
Nodes (7): build_create_address_detail_steps(), AddressDetailTests, read(), adb(), tap(), read(), item()

### Community 10 - "003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật"
Cohesion: 0.06
Nodes (27): emit(), 002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ, Các bước, Kiểm tra bắt buộc, Phạm vi, Rủi ro và bảo trì, Điều kiện dừng, 003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật (+19 more)

### Community 11 - "Danh mục từng bước đã biết — 13/11/2026"
Cohesion: 0.06
Nodes (35): Bản thử q7 State Machine — 14/11/2026, Chung b10 — Chuyển WhatsApp sang SMS, Chung b11 — Lấy và gõ OTP SMS, Chung b11a — Chạm ô OTP trên màn SMS, Chung b11b — Xác minh đăng nhập hoặc bấm Create của luồng tạo, Chung b4 — Sign In từ menu, Chung b4a — Chạm ô SĐT, Chung b5 — Gõ số điện thoại (+27 more)

### Community 12 - "ProfileRegistry"
Cohesion: 0.19
Nodes (5): ProfileRegistry, absent(), ProfileRegistryTests, lookup(), broken()

### Community 16 - "Ảnh hướng dẫn q1/q2 và menu chung lưu cục bộ"
Cohesion: 0.07
Nodes (28): B16–b22 chung — Đổi marketplace sang United States (18/11/2026), B32–b39 — Reload Balance, thêm thẻ và địa chỉ thanh toán (21/11/2026), B6 — Hai ảnh đính kèm mới ngày 13/11/2026, Menu chung ảnh 01 — Danh sách chữ, Menu chung ảnh 02 — App Store bên phải sau khi Amazon mở, q1 b6 — US +1 hiện nhưng chạm không đóng hộp, 14/11/2026, q1 ảnh 01 — Menu và ba thẻ, q1 ảnh 02 — Sign In cuối menu (+20 more)

### Community 17 - "desktop_theme.py"
Cohesion: 0.12
Nodes (8): FooterNote, HeaderWave, startup_geometry(), state_style(), status_title(), DesktopLayoutTests, __init__(), __init__()

### Community 18 - "AttemptDeadline"
Cohesion: 0.05
Nodes (24): AttemptDeadline, ChangeUsFlowTests, node(), MarketplaceFlowTests, read(), adb(), read(), tap() (+16 more)

### Community 19 - "CloudPhone"
Cohesion: 0.08
Nodes (15): cloud_serials(), CloudPhone, open_amazon(), foreground(), probe(), prop(), reported_installer(), scan() (+7 more)

### Community 20 - "phone_window_layout.py"
Cohesion: 0.14
Nodes (5): arrange_on_open(), _row_if_fits(), _sort_key(), _tiles(), PhoneWindowLayoutTests

### Community 21 - "MENU_ROUTING.md"
Cohesion: 0.50
Nodes (4): Bằng chứng và phạm vi, Kiểm chứng, Quy tắc chạy, Điều hướng hai dạng menu ba gạch

### Community 22 - "Q3Q4FlowTests"
Cohesion: 0.23
Nodes (3): build_q3_steps(), build_q4_steps(), Q3Q4FlowTests

### Community 23 - "_type_field"
Cohesion: 0.12
Nodes (51): confirmed_login_otp_nodes(), continue_number(), country(), finish_auto(), finish_create(), finish_login(), focus_otp(), focus_phone() (+43 more)

### Community 24 - "phone_window_layout.py"
Cohesion: 0.10
Nodes (17): ActionValidator, _already_reached_result(), _browse_ready_after_sms(), build_q7_pilot_steps(), run(), _past_known_step(), RecoveryHandler, ResultVerifier (+9 more)

### Community 25 - "Nghiên cứu và tích hợp Swarmote"
Cohesion: 0.40
Nodes (4): Hành vi có bằng chứng, Kiểm thử còn lại, Nghiên cứu và tích hợp Swarmote, Phần đã áp dụng

### Community 26 - "._run"
Cohesion: 0.12
Nodes (32): _account_icon_from_image(), _browse(), b5(), _observe(), _person(), _post_done_person(), _account_tab(), build_marketplace_steps() (+24 more)

### Community 27 - "_after_back"
Cohesion: 0.36
Nodes (7): _after_back(), b16(), b17(), _google_sheet(), _passkey_page(), _raw_nodes(), _wait_raw()

### Community 30 - "RegistrationState"
Cohesion: 0.09
Nodes (8): resume_common_index(), build_random_steps(), finish_view(), b1–b3 ngẫu nhiên cho q1–q12 — 14/11/2026, adb(), adb(), adb(), adb()

### Community 31 - "PROJECT_INDEX.md"
Cohesion: 0.21
Nodes (5): Quy trình Swarmote hiện tại, Luồng q2 từ menu ba gạch, q3 — b1–b3 và nối luồng chung, q4 — Giỏ hàng, Pets, Home and DIY, q6 — Trang chủ, Giỏ hàng, menu và một thẻ

### Community 32 - "RandomPrefixTests"
Cohesion: 0.11
Nodes (4): RandomPrefixTests, adb(), adb(), adb()

### Community 33 - "core.py"
Cohesion: 0.13
Nodes (11): swarmote_adb_path(), swarmote_tunnel_owner(), _connect(), country_reverse_points(), country_scroll(), _failed(), read_tree(), ready() (+3 more)

### Community 34 - "vision.py"
Cohesion: 0.17
Nodes (9): _new_prefix(), phone_reader(), PhoneReader, ReaderResponseError, Tăng số lần thử đọc cây Android và bổ sung phương án dự phòng cho b23–b31 — 19/11/2026, fake_worker(), IsolationTests, duplicate() (+1 more)

### Community 36 - "_visible"
Cohesion: 0.12
Nodes (34): _bounds(), _resume_address_payment_index(), _same_country_position(), _scroll_up(), _text(), _visible(), _menu_visible(), _action() (+26 more)

### Community 37 - "time"
Cohesion: 0.19
Nodes (12): require_online(), _field_for_label(), fill_identifier(), fill_signup_form(), _nodes(), open_entry(), status(), _tap() (+4 more)

### Community 38 - "retry_preparation"
Cohesion: 0.16
Nodes (5): enter_otp(), _type_field(), Phục hồi khi ô nhập chưa nhận focus ở b4–b11 — 14/11/2026, FlowRecoveryTests, form()

### Community 39 - "build_create_address_steps"
Cohesion: 0.24
Nodes (4): build_create_address_steps(), CreateAddressFlowTests, read(), node()

### Community 40 - "main"
Cohesion: 0.16
Nodes (9): main(), main(), Đợt tăng tốc và tự phục hồi b4–b11 ngày 13/11/2026, File dự án mà Graphify không phân tích trực tiếp, .gitignore, Launch Swarmote Tool.pyw, pyproject.toml, Ảnh PNG trong dự án (+1 more)

### Community 42 - "_read_nodes"
Cohesion: 0.12
Nodes (26): _at_or_after(), sign_in(), _country_nodes(), _CountryReadStop, _ensure_menu(), _find_scrolling(), home_visible(), _read_nodes() (+18 more)

### Community 44 - "FakeControl"
Cohesion: 0.13
Nodes (5): ParallelInstallTests, PhoneWindow, FakeControl, InstallTests, descendants()

### Community 45 - "desktop_theme.py"
Cohesion: 0.19
Nodes (6): Button, Entry, icon(), ui_font(), section_heading(), Settings hiện chậm — 14/11/2026

### Community 46 - "ToolError"
Cohesion: 0.10
Nodes (4): Window, otp_token(), Các bước, PreparationProgressTests

### Community 47 - "._refresh_devices"
Cohesion: 0.12
Nodes (3): Dán bảng Amazon có ghi chú thẻ live và URL OTP escaped — 14/11/2026, Phạm vi q1–q12 sau phản hồi người dùng — 14/11/2026, Trạng thái kiểm chứng và giới hạn

### Community 48 - "Swarmote V3 — đối chiếu ảnh mẫu 27/11/2026"
Cohesion: 0.17
Nodes (11): Bố cục, Bố cục được áp dụng, Chữ và tiến độ, Giao diện vận hành, Hướng thị giác, Kiểm chứng và phạm vi, Kích thước và cuộn, Phân tích màu ảnh mẫu (+3 more)

### Community 49 - "cli.py"
Cohesion: 0.27
Nodes (4): CountryRecoveryTests, read(), wait(), node()

### Community 50 - "bulk_input.py"
Cohesion: 0.15
Nodes (8): lines(), _markdown_cell_text(), _proxy_rows(), _table_cells(), _url_from_cell(), validate_card(), _unfiltered_single_page(), Đã có trong graph

### Community 51 - "b1–b11 Reliability and Latency Implementation Plan"
Cohesion: 0.18
Nodes (10): b1–b11 Reliability and Latency Implementation Plan, Completion Criteria, File Map, Global Constraints, Review Focus, Task 1: Measure current step latency and classify existing failures, Task 2: Define safe retry, reconcile, pause, and stop behavior, Task 3: Reduce redundant UI reads and unnecessary waits (+2 more)

### Community 52 - "desktop.py"
Cohesion: 0.07
Nodes (19): _bounds(), _canonical_text(), _compact(), _engine(), _field_contents(), _field_is_blank(), _input_box(), _join_wrapped_categories() (+11 more)

### Community 53 - "Danh mục ảnh nằm trong dự án"
Cohesion: 0.18
Nodes (11): amazon_android/assets/icons/, amazon_android/assets/obsidian_prism.png, amazon_android/assets/swarmote_tool_square.png và swarmote_tool.ico, assets/ui_history/machine7_input_before.png, assets/ui_history/reset_check.png, assets/ui_history/ui-12.png, assets/ui_history/ui_palette_preview.png, assets/ui_history/ui-preview.png (+3 more)

### Community 54 - "account_flow.py"
Cohesion: 0.16
Nodes (14): _ActionNotResolved, _read_hierarchy(), _read_login_sms_visual(), _read_nodes_once(), _read_visual_nodes(), _UiReadIncomplete, _visible_edit_fields(), _visual_form_button() (+6 more)

### Community 55 - "Amazon Android Tool — Giai đoạn A/B"
Cohesion: 0.29
Nodes (7): Amazon Android Tool — Giai đoạn A/B, Cài trên máy Windows mới, Dán nhiều proxy, Sử dụng, Trạng thái nghiệm thu, Yêu cầu, Điện thoại đám mây Swarmote

### Community 56 - "StatusCell"
Cohesion: 0.18
Nodes (7): save(), default_path(), AppSettings, load_settings(), save_settings(), settings_path(), SettingsTests

### Community 57 - "core.py"
Cohesion: 0.05
Nodes (61): BatchItem, parse_proxy_line(), prepare_five(), main(), parser(), report(), adb(), app_data_dir() (+53 more)

### Community 58 - ".test_transition_keeps_observing_after_short_wait_without_tapping"
Cohesion: 0.22
Nodes (3): read(), read(), menu()

### Community 59 - "_prefix_nodes"
Cohesion: 0.25
Nodes (7): _prefix_nodes(), Cách xử lý ảnh tiếp theo, Phần riêng từng máy, Tiến độ hướng dẫn bằng ảnh — cập nhật 13/11/2026, 14 ảnh menu chung b1–b3 ngẫu nhiên — 14/11/2026, B1–b3 xem menu ngẫu nhiên cho 12 máy — 14/11/2026, B1–B3 hiện hành — Ba lượt ngẫu nhiên q1–q12

### Community 60 - "Amazon trên Swarmote"
Cohesion: 0.33
Nodes (5): Amazon trên Swarmote, Người dùng và công việc, Nền tảng, Điều chưa xác minh, Định hướng ngôn ngữ nếu xây dựng lại — 23/11/2026

### Community 61 - "home_menu.py"
Cohesion: 0.08
Nodes (24): b6 Country US +1 — 14/11/2026, B6 cuộn quốc gia và chọn lại — 13/11/2026, Biên bản kiểm tra thực tế — 2026-11-12, Cài và đo UiAutomator2 theo phê duyệt mới — 13/11/2026, Dừng riêng một máy — 14/11/2026, Focus ô nhập b4–b11 — 14/11/2026, Ghim taskbar — 13/11/2026, Giao diện sáng, dễ đọc — 2026-11-13 (+16 more)

### Community 62 - "build_reload_payment_steps"
Cohesion: 0.13
Nodes (9): build_reload_payment_steps(), node(), ReloadPaymentTests, adb(), wait(), read(), read(), read() (+1 more)

### Community 63 - "Bộ cài chia sẻ Windows x64"
Cohesion: 0.50
Nodes (3): Bộ cài chia sẻ Windows x64, Dựng lại, Nguồn thành phần

### Community 64 - "CountryRecoveryTests"
Cohesion: 0.11
Nodes (3): animations_enabled(), SmoothScrollableFrame, DesktopScrollTests

### Community 65 - "PhoneReader"
Cohesion: 0.18
Nodes (11): Hướng dẫn khi tiếp tục dự án, build_post_auth_steps(), Nhận diện giao diện lúc chạy, Nhập liệu và lỗi, Quy tắc tự động hóa sau menu ba gạch, Trạng thái hiện tại của dự án, Từng máy độc lập, Bản đồ repository (+3 more)

### Community 66 - "VERIFICATION.md"
Cohesion: 0.13
Nodes (13): Kết luận và tích hợp, Kết quả thực tế, So sánh bộ đọc trên q1 — 13/11/2026, Thành phần thiết bị, b1–b3 bắt buộc có ba cú bấm — 14/11/2026, b1–b3 ngẫu nhiên cho 12 máy — 14/11/2026, b1–b3 ngẫu nhiên trên 12 máy, không dùng OCR — 14/11/2026, b6 cuộn tới đáy rồi vuốt ngược — 14/11/2026 (+5 more)

### Community 67 - "AccountData"
Cohesion: 0.29
Nodes (7): 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Rủi ro và bảo trì, Thiết kế yêu cầu, Điều kiện dừng

### Community 68 - ".test_single_row_paste_and_clear_touch_only_selected_failed_machine"
Cohesion: 0.16
Nodes (13): _phone_preparation_lock(), _prepare_phone(), _prepare_phone_locked(), progress(), stop_here(), run_batch(), fill_slots(), manually_selected() (+5 more)

### Community 69 - "Bàn giao dừng theo yêu cầu người dùng — 13/11/2026"
Cohesion: 0.29
Nodes (6): Bàn giao dừng theo yêu cầu người dùng — 13/11/2026, Bối cảnh đã hoàn tất trước lỗi hiện tại, Cách tiếp tục, Kiểm chứng gần nhất, Lỗi chính chưa xử lý xong, Yêu cầu mới nhất

### Community 70 - "Proxy dự phòng trong RAM Implementation Plan"
Cohesion: 0.29
Nodes (6): Global Constraints, Proxy dự phòng trong RAM Implementation Plan, Review Focus, Task 1: Pool và dán dự phòng, Task 2: Cấp phát và vòng đời mẻ, Task 3: Bố cục hẹp và xác minh

### Community 71 - "PROJECT_HANDOFF.md"
Cohesion: 0.11
Nodes (17): visit(), B4–b11 chạy đồng thời và OCR — 14/11/2026, b6 US +1 còn mở sau bốn cú chạm — 14/11/2026, Bản thử State Machine q7 và b1–b3 mở mục con — 14/11/2026, Bỏ thời hạn tổng sau menu — 14/11/2026, Bổ sung đọc ảnh OCR và chạm trực tiếp dự phòng cho b26 khi uiautomator dump WebView lỗi — 19/11/2026, Cơ chế chụp ảnh OCR quét chữ ấn luôn cho toàn bộ b26–b31 — 19/11/2026, File chính đã sửa (+9 more)

### Community 74 - "ProfilesNavigationTests"
Cohesion: 0.13
Nodes (8): control(), ProfilesNavigationTests, descendants(), descendants(), invoke(), descendants(), descendants(), descendants()

### Community 78 - "BatchDraft"
Cohesion: 0.25
Nodes (4): _choose_tail_target(), _TailChoicesExhausted, choose(), choose()

### Community 79 - "CountryRecoveryTests"
Cohesion: 0.13
Nodes (3): StatusCell, TableText, Tooltip

### Community 80 - "test_q1_flow.py"
Cohesion: 0.10
Nodes (7): menu_layout(), _parse_ui_nodes(), route_list_menu(), _ScreenWaitExpired, build_q1_steps(), category(), Q6FlowTests

### Community 81 - "_create_profile_form"
Cohesion: 0.11
Nodes (14): _activate_manager(), _create_profile_form(), _invoke(), ProfileCountryUnknown, ProfileCreateNotSubmitted, ProfileManagerWindowError, ProfileNotFound, _proxy_test_country() (+6 more)

### Community 83 - "isolated_reader.py"
Cohesion: 0.08
Nodes (11): AccountData, retry_preparation(), RunJob, P03 — Mở form New Profile, DesktopResumeTests, apartment_type(), PreparationThreadsTests, run() (+3 more)

### Community 84 - "OTP_DESIGN.md"
Cohesion: 0.11
Nodes (17): set_tk_icon(), B6 danh sách quốc gia vẫn mở sau khi chọn — 13/11/2026, Bàn giao trạng thái dự án — 13/11/2026, Bản chính boom4may và bản dự phòng — 14/11/2026, Bộ cài offline chia sẻ — 14/11/2026, Cài đặt máy mới, Dừng riêng máy đang chọn — 14/11/2026, Dự phòng dùng chung khi chạy song song — 14/11/2026 (+9 more)

### Community 85 - "ensure_manager_ready"
Cohesion: 0.40
Nodes (5): Cách thử bản pilot cũ (không áp dụng cho factory hiện hành), Giai đoạn 2 — bản thử State Machine riêng q7, Giới hạn, Phạm vi và quan hệ với luồng cũ, Sơ đồ

### Community 87 - "File dự án mà Graphify không phân tích trực tiếp"
Cohesion: 0.10
Nodes (4): RegistrationState, build_tail_steps(), Q5FlowTests, RandomPrefixTests

### Community 88 - "home_menu.py"
Cohesion: 0.10
Nodes (13): _confirm_menu_fallback(), _menu_evidence(), MenuReadUnavailable, _nodes(), budget(), open_home_menu(), ready_for_home_menu(), _tap() (+5 more)

### Community 89 - "_proxy_postal_prefix"
Cohesion: 0.48
Nodes (3): _proxy_postal_prefix(), controls(), ProxyPostalPrefixTests

### Community 92 - "GRAPH_AUDIT.md"
Cohesion: 0.50
Nodes (3): Cách kiểm tra sau mỗi sửa đổi, Giới hạn đã xác nhận, Kiểm tra độ phủ Graphify — cập nhật 26/11/2026

### Community 96 - "cloud_adb"
Cohesion: 0.07
Nodes (38): _country_full_row(), _tap(), scroll_view(), wait_until(), b2(), amazon_is_foreground(), cloud_adb(), RecoverableStepError (+30 more)

### Community 100 - "OTP_DESIGN.md"
Cohesion: 0.50
Nodes (3): Nối vào bước tạo tài khoản sau khi xác minh màn hình Amazon, Thiết kế OTP cho từng Profile, Đã chuẩn bị

## Knowledge Gaps
- **1 isolated node(s):** `amazon-android-tool`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 596 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **15 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ToolError` connect `.test_only_confirmed_target_names_are_selected_for_one_start_command` to `reload_payment_flow.py`, `Q1FlowTests`, `otp.py`, `BulkInputTests`, `ProxyConfig`, `swarmote_desktop.py`, `RunnerTests`, `PostMenuStep`, `build_create_address_detail_steps`, `ProfileRegistry`, `StopResetTests`, `unittest`, `AttemptDeadline`, `CloudPhone`, `_type_field`, `phone_window_layout.py`, `._run`, `_after_back`, `RegistrationState`, `RandomPrefixTests`, `core.py`, `vision.py`, `_visible`, `time`, `retry_preparation`, `build_create_address_steps`, `_read_nodes`, `ToolError`, `._refresh_devices`, `cli.py`, `bulk_input.py`, `desktop.py`, `account_flow.py`, `StatusCell`, `core.py`, `_prefix_nodes`, `build_reload_payment_steps`, `.test_single_row_paste_and_clear_touch_only_selected_failed_machine`, `PROJECT_HANDOFF.md`, `ProfilesNavigationTests`, `BatchDraft`, `test_q1_flow.py`, `_create_profile_form`, `isolated_reader.py`, `File dự án mà Graphify không phân tích trực tiếp`, `home_menu.py`, `cloud_adb`?**
  _High betweenness centrality (0.356) - this node is a cross-community bridge._
- **Are the 63 inferred relationships involving `ToolError` (e.g. with `_read_nodes_once()` and `_resume_address_payment_index()`) actually correct?**
  _`ToolError` has 63 INFERRED edges - model-reasoned connections that need verification._
- **What connects `amazon-android-tool` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Q1FlowTests` be split into smaller, more focused modules?**
  _Cohesion score 0.07023705004389816 - nodes in this community are weakly interconnected._
- **Why does `Window` connect `ToolError` to `otp.py`, `BulkInputTests`, `ProxyConfig`, `PostMenuStep`, `.test_only_confirmed_target_names_are_selected_for_one_start_command`, `003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật`, `ProfileRegistry`, `StopResetTests`, `unittest`, `desktop_theme.py`, `CloudPhone`, `Q3Q4FlowTests`, `RandomPrefixTests`, `._refresh_devices`, `main`, `desktop_theme.py`, `._refresh_devices`, `StatusCell`, `CountryRecoveryTests`, `AccountData`, `Proxy dự phòng trong RAM Implementation Plan`, `CloudPhone`, `CountryRecoveryTests`, `isolated_reader.py`, `OTP_DESIGN.md`, `File dự án mà Graphify không phân tích trực tiếp`?**
  _High betweenness centrality (0.124) - this node is a cross-community bridge._
- **Are the 89 inferred relationships involving `CloudPhone` (e.g. with `build_common_steps()` and `_country_full_row()`) actually correct?**
  _`CloudPhone` has 89 INFERRED edges - model-reasoned connections that need verification._
- **Should `otp.py` be split into smaller, more focused modules?**
  _Cohesion score 0.09848484848484848 - nodes in this community are weakly interconnected._