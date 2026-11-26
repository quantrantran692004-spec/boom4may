# Graph Report - bom4may  (2026-11-26)

## Corpus Check
- 134 files · ~167,055 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 1, .bat 1, .pyw 1)

## Summary
- 2185 nodes · 7619 edges · 96 communities (81 shown, 15 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 1095 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c105773a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ToolError
- build_common_steps
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
- account_flow.py
- AttemptDeadline
- marketplace_flow.py
- _read_nodes
- MENU_ROUTING.md
- Q3Q4FlowTests
- _type_field
- resume_common_index
- Nghiên cứu và tích hợp Swarmote
- q7_state_machine.py
- _yellow_form_button
- amazon_is_foreground
- ._refresh_devices
- RegistrationState
- PROJECT_INDEX.md
- RandomPrefixTests
- core.py
- vision.py
- setup.py
- _visible
- time
- VisionFieldTests
- build_create_address_steps
- main
- cli.py
- Bàn giao trạng thái dự án — 13/11/2026
- q7_random_prefix.py
- FakeControl
- .get
- ui_backend.py
- cloud_adb
- ProxyConfig
- swarmote_desktop.py
- .remaining
- b1–b11 Reliability and Latency Implementation Plan
- .test_tail_stop_after_swipe_resumes_remaining_view_before_back
- Danh mục ảnh nằm trong dự án
- _recognize
- Amazon Android Tool — Giai đoạn A/B
- ProfileRegistry
- _CombinedStop
- Giao diện vận hành
- run
- Amazon trên Swarmote
- home_menu.py
- build_reload_payment_steps
- Bộ cài chia sẻ Windows x64
- CountryRecoveryTests
- PhoneReader
- VERIFICATION.md
- AppSettings
- build_post_auth_steps
- run_batch
- CloudPhone
- PROJECT_HANDOFF.md
- create_profile
- BatchDraft
- test_swarmote_navigation.py
- screen
- ._build_main
- RunJob
- Window
- Giai đoạn 2 — bản thử State Machine riêng q7
- SafetyTests
- random_prefix.py
- .test_b1_b2_wait_two_seconds_after_tap_before_view_scroll
- _choose_tail_target
- OTP_DESIGN.md
- ensure_manager_ready
- Bàn giao dừng theo yêu cầu người dùng — 13/11/2026
- otp_token
- 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng
- GRAPH_AUDIT.md
- Value

## God Nodes (most connected - your core abstractions)
1. `ToolError` - 356 edges
2. `CloudPhone` - 234 edges
3. `AttemptDeadline` - 201 edges
4. `RunJob` - 164 edges
5. `RegistrationState` - 163 edges
6. `build_common_steps()` - 115 edges
7. `Window` - 98 edges
8. `PostMenuStep` - 94 edges
9. `Q1FlowTests` - 92 edges
10. `PostMenuSession` - 81 edges

## Surprising Connections (you probably didn't know these)
- `Bổ sung đọc ảnh OCR và chạm trực tiếp dự phòng cho b26 khi uiautomator dump WebView lỗi — 19/11/2026` --references--> `_read_hierarchy()`  [INFERRED]
  PROJECT_HANDOFF.md → amazon_android/account_flow.py
- `b6 US +1 còn mở sau bốn cú chạm — 14/11/2026` --references--> `_wait_screen()`  [INFERRED]
  PROJECT_HANDOFF.md → amazon_android/account_flow.py
- `q6 b1–b3a riêng, b4–b11 chung — 14/11/2026` --references--> `_ensure_menu()`  [INFERRED]
  PROJECT_HANDOFF.md → amazon_android/account_flow.py
- `Điều tra q1/q2 mượt, q3+ lỗi thất thường khi chạy song song — 14/11/2026` --references--> `_ensure_menu()`  [INFERRED]
  PROJECT_HANDOFF.md → amazon_android/account_flow.py
- `q5 b1–b3 riêng, b4–b11 chung — 14/11/2026` --references--> `build_common_steps()`  [INFERRED]
  PROJECT_HANDOFF.md → amazon_android/account_flow.py

## Import Cycles
- None detected.

## Communities (96 total, 15 thin omitted)

### Community 0 - "ToolError"
Cohesion: 0.14
Nodes (17): ToolError, _field_for_label(), fill_identifier(), fill_signup_form(), _nodes(), open_entry(), status(), _tap() (+9 more)

### Community 1 - "build_common_steps"
Cohesion: 0.05
Nodes (7): build_common_steps(), _ScreenWaitExpired, node(), Q1FlowTests, read(), provider_read(), read()

### Community 2 - "otp.py"
Cohesion: 0.10
Nodes (9): browser_launch_options(), extract_otp(), _NoRedirect, read_otp(), _read_otp_in_browser(), validate_otp_url(), wait_for_new_otp(), OtpTests (+1 more)

### Community 3 - "BulkInputTests"
Cohesion: 0.10
Nodes (5): parse_column(), parse_records(), validate_card(), _card_parts(), BulkInputTests

### Community 4 - "desktop.py"
Cohesion: 0.15
Nodes (8): create_shortcut(), relaunch_command(), runtime(), set_process_identity(), set_tk_icon(), set_window_identity(), Sửa shortcut ghim mở nhầm IDLE — 13/11/2026, WindowsIdentityTests

### Community 5 - "show_apps"
Cohesion: 0.09
Nodes (27): open_amazon(), foreground(), package_path(), ready_for_home_menu(), _check_stop(), collapse_apps_panel(), install_amazon(), collect() (+19 more)

### Community 6 - "RunnerTests"
Cohesion: 0.11
Nodes (7): RunnerTests, create(), resume(), create(), failed_start(), resume(), create()

### Community 7 - "PostMenuStep"
Cohesion: 0.12
Nodes (8): PostMenuSession, PostMenuStep, Một quy luật để sửa mã về sau — 20/11/2026, PostMenuTests, reconcile(), first(), SharedStepRecoveryTests, action()

### Community 8 - ".test_only_confirmed_target_names_are_selected_for_one_start_command"
Cohesion: 0.08
Nodes (14): ProfileStartNotSubmitted, _select_profile_rows(), _selected_profile_names(), start_profile(), start_profiles_together(), _wait_for_selected(), Hàng đợi 4 máy với giới hạn 2 Running — 14/11/2026, delayed_start() (+6 more)

### Community 9 - "build_create_address_detail_steps"
Cohesion: 0.12
Nodes (7): build_create_address_detail_steps(), AddressDetailTests, read(), adb(), tap(), read(), item()

### Community 10 - "003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật"
Cohesion: 0.07
Nodes (25): 002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ, Kiểm tra bắt buộc, Phạm vi, Rủi ro và bảo trì, Điều kiện dừng, 003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật, Các bước, Kiểm tra bắt buộc (+17 more)

### Community 11 - "Danh mục từng bước đã biết — 13/11/2026"
Cohesion: 0.06
Nodes (35): Bản thử q7 State Machine — 14/11/2026, Chung b10 — Chuyển WhatsApp sang SMS, Chung b11 — Lấy và gõ OTP SMS, Chung b11a — Chạm ô OTP trên màn SMS, Chung b11b — Xác minh đăng nhập hoặc bấm Create của luồng tạo, Chung b4 — Sign In từ menu, Chung b4a — Chạm ô SĐT, Chung b5 — Gõ số điện thoại (+27 more)

### Community 12 - "build_random_steps"
Cohesion: 0.13
Nodes (3): build_random_steps(), B1–b3 xem menu ngẫu nhiên cho 12 máy — 14/11/2026, adb()

### Community 16 - "Ảnh hướng dẫn q1/q2 và menu chung lưu cục bộ"
Cohesion: 0.07
Nodes (28): B16–b22 chung — Đổi marketplace sang United States (18/11/2026), B32–b39 — Reload Balance, thêm thẻ và địa chỉ thanh toán (21/11/2026), B6 — Hai ảnh đính kèm mới ngày 13/11/2026, Menu chung ảnh 01 — Danh sách chữ, Menu chung ảnh 02 — App Store bên phải sau khi Amazon mở, q1 b6 — US +1 hiện nhưng chạm không đóng hộp, 14/11/2026, q1 ảnh 01 — Menu và ba thẻ, q1 ảnh 02 — Sign In cuối menu (+20 more)

### Community 17 - "account_flow.py"
Cohesion: 0.15
Nodes (5): menu_layout(), _national_phone(), _parse_ui_nodes(), route_list_menu(), cloud_screenshot()

### Community 18 - "AttemptDeadline"
Cohesion: 0.05
Nodes (30): AttemptDeadline, ExtendedRecoveryTests, fail(), read(), read(), MarketplaceFlowTests, read(), adb() (+22 more)

### Community 19 - "marketplace_flow.py"
Cohesion: 0.17
Nodes (28): _account_tab(), build_marketplace_steps(), run(), account_target(), back_and_read_text(), foreground_ready(), recover_country_list(), _country_card() (+20 more)

### Community 20 - "_read_nodes"
Cohesion: 0.12
Nodes (29): _at_or_after(), sign_in(), _country_nodes(), _CountryReadStop, _ensure_menu(), _find_scrolling(), home_visible(), _read_nodes() (+21 more)

### Community 21 - "MENU_ROUTING.md"
Cohesion: 0.23
Nodes (7): Bằng chứng và phạm vi, Kiểm chứng, Quy tắc chạy, Điều hướng hai dạng menu ba gạch, Luồng q1 từ menu ba gạch tới nhập OTP, Thử trên q1 đã có, Luồng q2 từ menu ba gạch

### Community 22 - "Q3Q4FlowTests"
Cohesion: 0.23
Nodes (3): build_q3_steps(), build_q4_steps(), Q3Q4FlowTests

### Community 23 - "_type_field"
Cohesion: 0.17
Nodes (5): enter_otp(), _type_field(), _UiReadIncomplete, FlowRecoveryTests, form()

### Community 24 - "resume_common_index"
Cohesion: 0.14
Nodes (6): resume_common_index(), current(), Dự phòng dùng chung khi chạy song song — 14/11/2026, ResumeRegistrationStateTests, factory(), factory()

### Community 25 - "Nghiên cứu và tích hợp Swarmote"
Cohesion: 0.40
Nodes (4): Hành vi có bằng chứng, Kiểm thử còn lại, Nghiên cứu và tích hợp Swarmote, Phần đã áp dụng

### Community 26 - "q7_state_machine.py"
Cohesion: 0.08
Nodes (16): ActionValidator, _already_reached_result(), build_q7_pilot_steps(), _past_known_step(), RecoveryHandler, ResultVerifier, StateDeadline, StateDetector (+8 more)

### Community 27 - "_yellow_form_button"
Cohesion: 0.50
Nodes (3): _ActionNotResolved, _visual_form_button(), _yellow_form_button()

### Community 28 - "amazon_is_foreground"
Cohesion: 0.13
Nodes (8): amazon_is_foreground(), cloud_serials(), probe(), require_online(), scan(), CloudBridgeTests, adb(), Ẩn cửa sổ cmd khi gọi ADB — 2026-11-13

### Community 30 - "RegistrationState"
Cohesion: 0.13
Nodes (6): RegistrationState, build_tail_steps(), open_menu(), view(), visit_seconds(), RandomPrefixTests

### Community 31 - "PROJECT_INDEX.md"
Cohesion: 0.19
Nodes (6): Quy trình Swarmote hiện tại, Bản đồ repository, q3 — b1–b3 và nối luồng chung, q4 — Giỏ hàng, Pets, Home and DIY, q5 — ba thẻ riêng và b4–b11 chung, q6 — Trang chủ, Giỏ hàng, menu và một thẻ

### Community 32 - "RandomPrefixTests"
Cohesion: 0.12
Nodes (4): RandomPrefixTests, adb(), adb(), adb()

### Community 33 - "core.py"
Cohesion: 0.27
Nodes (19): adb(), available_memory_mb(), check_play(), configure_avd(), connected_devices(), Device, device_avd_name(), device_resources() (+11 more)

### Community 34 - "vision.py"
Cohesion: 0.12
Nodes (10): _bounds(), _canonical_text(), _compact(), _field_contents(), _field_is_blank(), _join_wrapped_categories(), _normalize(), ocr_nodes() (+2 more)

### Community 35 - "setup.py"
Cohesion: 0.23
Nodes (12): app_data_dir(), avd_names(), create_avd(), doctor(), executable(), installed_image(), run(), sdk_root() (+4 more)

### Community 36 - "_visible"
Cohesion: 0.19
Nodes (27): _bounds(), _button(), _text(), _visible(), _action(), _address_form(), _addresses(), _bounded_native() (+19 more)

### Community 37 - "time"
Cohesion: 0.16
Nodes (12): main(), check_runtime(), main(), verify(), _app_installed(), _app_paths(), _check_external_apps(), _install_python_dependencies() (+4 more)

### Community 38 - "VisionFieldTests"
Cohesion: 0.24
Nodes (3): _input_box(), detection(), VisionFieldTests

### Community 39 - "build_create_address_steps"
Cohesion: 0.24
Nodes (4): build_create_address_steps(), CreateAddressFlowTests, read(), node()

### Community 40 - "main"
Cohesion: 0.18
Nodes (9): main(), main(), Đợt tăng tốc và tự phục hồi b4–b11 ngày 13/11/2026, File dự án mà Graphify không phân tích trực tiếp, .gitignore, Launch Swarmote Tool.pyw, pyproject.toml, Ảnh PNG trong dự án (+1 more)

### Community 41 - "cli.py"
Cohesion: 0.27
Nodes (6): main(), parser(), report(), get_device(), print_json(), Store

### Community 42 - "Bàn giao trạng thái dự án — 13/11/2026"
Cohesion: 0.13
Nodes (13): B6 danh sách quốc gia vẫn mở sau khi chọn — 13/11/2026, Bàn giao trạng thái dự án — 13/11/2026, Bản chính boom4may và bản dự phòng — 14/11/2026, Bộ cài offline chia sẻ — 14/11/2026, Cài đặt máy mới, Dừng riêng máy đang chọn — 14/11/2026, q3/q4 đã nối b1–b3 và thử đồng thời bốn luồng — 13/11/2026, q5 b1–b3 riêng, b4–b11 chung — 14/11/2026 (+5 more)

### Community 43 - "q7_random_prefix.py"
Cohesion: 0.12
Nodes (18): _read_hierarchy(), scroll_view(), wait_until(), RecoverableStepError, build_random_steps(), browse(), action(), run_browse() (+10 more)

### Community 44 - "FakeControl"
Cohesion: 0.13
Nodes (5): ParallelInstallTests, PhoneWindow, FakeControl, InstallTests, descendants()

### Community 45 - ".get"
Cohesion: 0.15
Nodes (5): ProfileCreateNotSubmitted, ProfileManagerWindowError, unavailable(), failed(), automatic()

### Community 46 - "ui_backend.py"
Cohesion: 0.07
Nodes (16): swarmote_adb_path(), swarmote_tunnel_owner(), arrange_on_open(), _row_if_fits(), _sort_key(), _tiles(), _connect(), country_reverse_points() (+8 more)

### Community 47 - "cloud_adb"
Cohesion: 0.18
Nodes (18): _keyboard_visible(), _resume_address_payment_index(), cloud_adb(), reported_installer(), _scroll(), _account_content(), run(), action() (+10 more)

### Community 48 - "ProxyConfig"
Cohesion: 0.14
Nodes (12): BatchItem, parse_proxy_line(), prepare_five(), BulkRecord, lines(), parse_bulk_payload(), _proxy_rows(), _table_cells() (+4 more)

### Community 49 - "swarmote_desktop.py"
Cohesion: 0.12
Nodes (21): _activate_manager(), _create_profile_form(), _descendants(), inspect(), _invoke(), _main_window(), _one(), _open_profiles() (+13 more)

### Community 50 - ".remaining"
Cohesion: 0.22
Nodes (10): _country_full_row(), _read_login_sms_visual(), _read_nodes_once(), _read_visual_nodes(), _scroll_up(), read_menu(), return_to_menu(), visit() (+2 more)

### Community 51 - "b1–b11 Reliability and Latency Implementation Plan"
Cohesion: 0.18
Nodes (10): b1–b11 Reliability and Latency Implementation Plan, Completion Criteria, File Map, Global Constraints, Review Focus, Task 1: Measure current step latency and classify existing failures, Task 2: Define safe retry, reconcile, pause, and stop behavior, Task 3: Reduce redundant UI reads and unnecessary waits (+2 more)

### Community 52 - ".test_tail_stop_after_swipe_resumes_remaining_view_before_back"
Cohesion: 0.14
Nodes (3): browse(), tap(), tap()

### Community 53 - "Danh mục ảnh nằm trong dự án"
Cohesion: 0.22
Nodes (9): amazon_android/assets/obsidian_prism.png, amazon_android/assets/swarmote_tool_square.png và swarmote_tool.ico, assets/ui_history/machine7_input_before.png, assets/ui_history/reset_check.png, assets/ui_history/ui-12.png, assets/ui_history/ui_palette_preview.png, assets/ui_history/ui-preview.png, assets/ui_history/ui-screenshot.png (+1 more)

### Community 54 - "_recognize"
Cohesion: 0.21
Nodes (6): _engine(), _recognize(), check(), ParallelOcrTests, engine(), read()

### Community 55 - "Amazon Android Tool — Giai đoạn A/B"
Cohesion: 0.29
Nodes (7): Amazon Android Tool — Giai đoạn A/B, Cài trên máy Windows mới, Dán nhiều proxy, Sử dụng, Trạng thái nghiệm thu, Yêu cầu, Điện thoại đám mây Swarmote

### Community 56 - "ProfileRegistry"
Cohesion: 0.18
Nodes (9): ProfileRegistry, ProfileLookupError, ProfileNotFound, Thiết kế yêu cầu, absent(), ProfileRegistryTests, lookup(), broken() (+1 more)

### Community 58 - "Giao diện vận hành"
Cohesion: 0.40
Nodes (4): Bố cục, Giao diện vận hành, Hướng thị giác, Quy tắc

### Community 59 - "run"
Cohesion: 0.18
Nodes (4): run(), run(), run(), run()

### Community 60 - "Amazon trên Swarmote"
Cohesion: 0.33
Nodes (5): Amazon trên Swarmote, Người dùng và công việc, Nền tảng, Điều chưa xác minh, Định hướng ngôn ngữ nếu xây dựng lại — 23/11/2026

### Community 61 - "home_menu.py"
Cohesion: 0.05
Nodes (36): _confirm_menu_fallback(), _menu_evidence(), MenuReadUnavailable, _nodes(), budget(), open_home_menu(), _tap(), Lỗi chạy song song q3 Terminal trùng / q1 chưa thấy menu — 14/11/2026 (+28 more)

### Community 62 - "build_reload_payment_steps"
Cohesion: 0.13
Nodes (9): build_reload_payment_steps(), node(), ReloadPaymentTests, adb(), wait(), read(), read(), read() (+1 more)

### Community 63 - "Bộ cài chia sẻ Windows x64"
Cohesion: 0.50
Nodes (3): Bộ cài chia sẻ Windows x64, Dựng lại, Nguồn thành phần

### Community 64 - "CountryRecoveryTests"
Cohesion: 0.22
Nodes (5): _same_country_position(), CountryRecoveryTests, read(), wait(), node()

### Community 65 - "PhoneReader"
Cohesion: 0.26
Nodes (6): phone_reader(), PhoneReader, ReaderResponseError, fake_worker(), IsolationTests, duplicate()

### Community 66 - "VERIFICATION.md"
Cohesion: 0.17
Nodes (10): Kết luận và tích hợp, Kết quả thực tế, So sánh bộ đọc trên q1 — 13/11/2026, Thành phần thiết bị, b1–b3 bắt buộc có ba cú bấm — 14/11/2026, b1–b3 ngẫu nhiên cho 12 máy — 14/11/2026, b1–b3 ngẫu nhiên trên 12 máy, không dùng OCR — 14/11/2026, b6 cuộn tới đáy rồi vuốt ngược — 14/11/2026 (+2 more)

### Community 67 - "AppSettings"
Cohesion: 0.17
Nodes (9): _new_prefix(), save(), default_path(), AppSettings, load_settings(), save_settings(), settings_path(), Tăng số lần thử đọc cây Android và bổ sung phương án dự phòng cho b23–b31 — 19/11/2026 (+1 more)

### Community 68 - "build_post_auth_steps"
Cohesion: 0.18
Nodes (10): Hướng dẫn khi tiếp tục dự án, build_account_preview_step(), build_post_auth_steps(), Nhận diện giao diện lúc chạy, Nhập liệu và lỗi, Quy tắc tự động hóa sau menu ba gạch, Trạng thái hiện tại của dự án, Từng máy độc lập (+2 more)

### Community 69 - "run_batch"
Cohesion: 0.08
Nodes (19): emit(), _phone_preparation_lock(), _prepare_phone(), _prepare_phone_locked(), progress(), stop_here(), retry_preparation(), run_batch() (+11 more)

### Community 70 - "CloudPhone"
Cohesion: 0.08
Nodes (13): verify_menu_open(), CloudPhone, prop(), reconcile(), route(), _serve(), type_characters(), build_q5_steps() (+5 more)

### Community 71 - "PROJECT_HANDOFF.md"
Cohesion: 0.12
Nodes (16): b1–b3 ngẫu nhiên cho q1–q12 — 14/11/2026, B4–b11 chạy đồng thời và OCR — 14/11/2026, b6 US +1 còn mở sau bốn cú chạm — 14/11/2026, Bản thử State Machine q7 và b1–b3 mở mục con — 14/11/2026, Bỏ thời hạn tổng sau menu — 14/11/2026, Bổ sung đọc ảnh OCR và chạm trực tiếp dự phòng cho b26 khi uiautomator dump WebView lỗi — 19/11/2026, Cơ chế chụp ảnh OCR quét chữ ấn luôn cho toàn bộ b26–b31 — 19/11/2026, Dán bảng Amazon có ghi chú thẻ live và URL OTP escaped — 14/11/2026 (+8 more)

### Community 72 - "create_profile"
Cohesion: 0.24
Nodes (3): create_profile(), Mục tiêu và bằng chứng, CreationWindowVisibilityTests

### Community 74 - "test_swarmote_navigation.py"
Cohesion: 0.16
Nodes (6): control(), ProfilesNavigationTests, descendants(), invoke(), descendants(), descendants()

### Community 75 - "screen"
Cohesion: 0.13
Nodes (31): confirmed_login_otp_nodes(), continue_number(), country(), finish_auto(), finish_create(), finish_login(), focus_otp(), focus_phone() (+23 more)

### Community 76 - "._build_main"
Cohesion: 0.22
Nodes (3): _crystal_art(), _edge_light(), Ô Amazon riêng Máy 1–12 dễ thấy hơn — 14/11/2026

### Community 77 - "RunJob"
Cohesion: 0.11
Nodes (10): _automatic_resume_slots(), AccountData, RunJob, DesktopResumeTests, apartment_type(), PreparationThreadsTests, run(), install() (+2 more)

### Community 78 - "Window"
Cohesion: 0.18
Nodes (3): Window, Các bước, PreparationProgressTests

### Community 79 - "Giai đoạn 2 — bản thử State Machine riêng q7"
Cohesion: 0.40
Nodes (5): Cách thử bản pilot cũ (không áp dụng cho factory hiện hành), Giai đoạn 2 — bản thử State Machine riêng q7, Giới hạn, Phạm vi và quan hệ với luồng cũ, Sơ đồ

### Community 81 - "random_prefix.py"
Cohesion: 0.07
Nodes (18): _first_point(), action(), browse_view(), finish_view(), sign_in(), _first_point(), _menu(), _prefix_nodes() (+10 more)

### Community 83 - "_choose_tail_target"
Cohesion: 0.25
Nodes (4): _choose_tail_target(), _TailChoicesExhausted, choose(), choose()

### Community 84 - "OTP_DESIGN.md"
Cohesion: 0.50
Nodes (3): Nối vào bước tạo tài khoản sau khi xác minh màn hình Amazon, Thiết kế OTP cho từng Profile, Đã chuẩn bị

### Community 85 - "ensure_manager_ready"
Cohesion: 0.32
Nodes (3): ensure_manager_ready(), _swarmote_exe(), ManagerStartupTests

### Community 87 - "Bàn giao dừng theo yêu cầu người dùng — 13/11/2026"
Cohesion: 0.25
Nodes (7): Bàn giao dừng theo yêu cầu người dùng — 13/11/2026, Bằng chứng trực tiếp đã có, Bối cảnh đã hoàn tất trước lỗi hiện tại, Cách tiếp tục, Kiểm chứng gần nhất, Lỗi chính chưa xử lý xong, Yêu cầu mới nhất

### Community 89 - "001 — Tách dữ liệu từng mẻ và đối chiếu số hàng"
Cohesion: 0.29
Nodes (7): 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Rủi ro và bảo trì, Thiết kế yêu cầu, Điều kiện dừng

### Community 92 - "GRAPH_AUDIT.md"
Cohesion: 0.50
Nodes (3): Cách kiểm tra sau mỗi sửa đổi, Giới hạn đã xác nhận, Kiểm tra độ phủ Graphify — cập nhật 26/11/2026

## Knowledge Gaps
- **1 isolated node(s):** `amazon-android-tool`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 538 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **15 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ToolError` connect `ToolError` to `build_common_steps`, `otp.py`, `BulkInputTests`, `show_apps`, `RunnerTests`, `PostMenuStep`, `.test_only_confirmed_target_names_are_selected_for_one_start_command`, `build_create_address_detail_steps`, `build_random_steps`, `StopResetTests`, `unittest`, `account_flow.py`, `AttemptDeadline`, `marketplace_flow.py`, `_read_nodes`, `_type_field`, `resume_common_index`, `q7_state_machine.py`, `_yellow_form_button`, `amazon_is_foreground`, `._refresh_devices`, `RegistrationState`, `RandomPrefixTests`, `core.py`, `vision.py`, `setup.py`, `_visible`, `build_create_address_steps`, `cli.py`, `q7_random_prefix.py`, `.get`, `ui_backend.py`, `cloud_adb`, `ProxyConfig`, `swarmote_desktop.py`, `.remaining`, `_recognize`, `ProfileRegistry`, `home_menu.py`, `build_reload_payment_steps`, `CountryRecoveryTests`, `PhoneReader`, `AppSettings`, `build_post_auth_steps`, `run_batch`, `CloudPhone`, `create_profile`, `BatchDraft`, `test_swarmote_navigation.py`, `screen`, `RunJob`, `Window`, `random_prefix.py`, `_choose_tail_target`, `ensure_manager_ready`, `otp_token`, `batch_state.py`?**
  _High betweenness centrality (0.405) - this node is a cross-community bridge._
- **Are the 58 inferred relationships involving `ToolError` (e.g. with `_read_nodes_once()` and `_resume_address_payment_index()`) actually correct?**
  _`ToolError` has 58 INFERRED edges - model-reasoned connections that need verification._
- **What connects `amazon-android-tool` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `ToolError` be split into smaller, more focused modules?**
  _Cohesion score 0.14022988505747128 - nodes in this community are weakly interconnected._
- **Why does `CloudPhone` connect `CloudPhone` to `ToolError`, `build_common_steps`, `show_apps`, `PostMenuStep`, `build_create_address_detail_steps`, `build_random_steps`, `unittest`, `account_flow.py`, `AttemptDeadline`, `_read_nodes`, `Q3Q4FlowTests`, `_type_field`, `resume_common_index`, `q7_state_machine.py`, `_yellow_form_button`, `amazon_is_foreground`, `._refresh_devices`, `RegistrationState`, `RandomPrefixTests`, `build_create_address_steps`, `cli.py`, `q7_random_prefix.py`, `ui_backend.py`, `cloud_adb`, `swarmote_desktop.py`, `.remaining`, `.test_tail_stop_after_swipe_resumes_remaining_view_before_back`, `home_menu.py`, `build_reload_payment_steps`, `CountryRecoveryTests`, `PhoneReader`, `build_post_auth_steps`, `run_batch`, `screen`, `RunJob`, `Window`, `random_prefix.py`, `.test_manual_otp_repair_continues_with_confirmation_and_tail_for_both_modes`?**
  _High betweenness centrality (0.110) - this node is a cross-community bridge._
- **Are the 88 inferred relationships involving `CloudPhone` (e.g. with `build_common_steps()` and `_country_full_row()`) actually correct?**
  _`CloudPhone` has 88 INFERRED edges - model-reasoned connections that need verification._
- **Should `build_common_steps` be split into smaller, more focused modules?**
  _Cohesion score 0.04981684981684982 - nodes in this community are weakly interconnected._