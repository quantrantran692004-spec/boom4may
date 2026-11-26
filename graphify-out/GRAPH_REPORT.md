# Graph Report - bom4may  (2026-11-26)

## Corpus Check
- 134 files · ~166,346 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 1, .bat 1, .pyw 1)

## Summary
- 2182 nodes · 7600 edges · 92 communities (74 shown, 18 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 1091 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b0a5c82b`
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
- desktop.py
- amazon-android-tool
- Ảnh hướng dẫn q1/q2 và menu chung lưu cục bộ
- home_menu.py
- AttemptDeadline
- marketplace_flow.py
- _find_scrolling
- Điều hướng hai dạng menu ba gạch
- Q3Q4FlowTests
- _type_field
- phone_window_layout.py
- Nghiên cứu và tích hợp Swarmote
- q7_state_machine.py
- ExtendedRecoveryTests
- amazon_is_foreground
- RegistrationState
- PROJECT_INDEX.md
- RandomPrefixTests
- core.py
- vision.py
- setup.py
- _visible
- time
- retry_preparation
- build_create_address_steps
- main
- cli.py
- Bàn giao trạng thái dự án — 13/11/2026
- q7_random_prefix.py
- FakeControl
- _scroll_up
- ui_backend.py
- cloud_adb
- bulk_input.py
- swarmote_desktop.py
- account_flow.py
- b1–b11 Reliability and Latency Implementation Plan
- .test_tail_stop_after_swipe_resumes_remaining_view_before_back
- Danh mục ảnh nằm trong dự án
- build_q1_steps
- Amazon Android Tool — Giai đoạn A/B
- _proxy_postal_prefix
- _CombinedStop
- Giao diện vận hành
- ._start_post_menu
- Amazon trên Swarmote
- home_menu.py
- build_reload_payment_steps
- Bộ cài chia sẻ Windows x64
- CountryRecoveryTests
- PhoneReader
- VERIFICATION.md
- run_batch
- PLAN.md
- PROJECT_HANDOFF.md
- ProxyConfig
- BatchDraft
- test_swarmote_navigation.py
- screen
- ._build_main
- Q2FlowTests
- Window
- Giai đoạn 2 — bản thử State Machine riêng q7
- SafetyTests
- _tail_menu
- Luồng q1 từ menu ba gạch tới nhập OTP
- RunJob
- OTP_DESIGN.md
- ensure_manager_ready
- Q5_FLOW.md
- otp_token
- ._apply_bulk_text
- GRAPH_AUDIT.md

## God Nodes (most connected - your core abstractions)
1. `ToolError` - 354 edges
2. `CloudPhone` - 234 edges
3. `AttemptDeadline` - 202 edges
4. `RunJob` - 164 edges
5. `RegistrationState` - 162 edges
6. `build_common_steps()` - 115 edges
7. `Window` - 98 edges
8. `PostMenuStep` - 93 edges
9. `Q1FlowTests` - 92 edges
10. `PostMenuSession` - 81 edges

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

## Communities (92 total, 18 thin omitted)

### Community 0 - "ToolError"
Cohesion: 0.11
Nodes (20): _CountryReadStop, require_online(), ToolError, reconcile(), _TailChoicesExhausted, _field_for_label(), fill_identifier(), fill_signup_form() (+12 more)

### Community 1 - "build_common_steps"
Cohesion: 0.05
Nodes (6): build_common_steps(), node(), Q1FlowTests, read(), provider_read(), read()

### Community 2 - "otp.py"
Cohesion: 0.10
Nodes (9): browser_launch_options(), extract_otp(), _NoRedirect, read_otp(), _read_otp_in_browser(), validate_otp_url(), wait_for_new_otp(), OtpTests (+1 more)

### Community 4 - "desktop.py"
Cohesion: 0.22
Nodes (6): create_shortcut(), relaunch_command(), runtime(), set_process_identity(), set_window_identity(), WindowsIdentityTests

### Community 5 - "show_apps"
Cohesion: 0.08
Nodes (32): ready_for_home_menu(), progress(), _check_stop(), collapse_apps_panel(), _descendants(), install_amazon(), check_stop(), open_adb_shell() (+24 more)

### Community 6 - "RunnerTests"
Cohesion: 0.06
Nodes (18): ProfileRegistry, ProfileNotFound, absent(), ProfileRegistryTests, lookup(), broken(), RunnerTests, create() (+10 more)

### Community 7 - "PostMenuStep"
Cohesion: 0.08
Nodes (13): PostMenuSession, PostMenuStep, PostMenuTests, reconcile(), first(), ResumeRegistrationStateTests, factory(), factory() (+5 more)

### Community 8 - ".test_only_confirmed_target_names_are_selected_for_one_start_command"
Cohesion: 0.09
Nodes (12): ProfileStartNotSubmitted, _select_profile_rows(), _selected_profile_names(), start_profile(), start_profiles_together(), _wait_for_selected(), BatchStartTests, checkbox() (+4 more)

### Community 9 - "build_create_address_detail_steps"
Cohesion: 0.12
Nodes (7): build_create_address_detail_steps(), AddressDetailTests, read(), adb(), tap(), read(), item()

### Community 10 - "003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật"
Cohesion: 0.10
Nodes (15): 003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật, Các bước, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Quy trình đích, Rủi ro và bảo trì, Điều kiện dừng (+7 more)

### Community 11 - "Danh mục từng bước đã biết — 13/11/2026"
Cohesion: 0.06
Nodes (36): B1–B3 hiện hành — Ba lượt ngẫu nhiên q1–q12, Bản thử q7 State Machine — 14/11/2026, Chung b10 — Chuyển WhatsApp sang SMS, Chung b11 — Lấy và gõ OTP SMS, Chung b11a — Chạm ô OTP trên màn SMS, Chung b11b — Xác minh đăng nhập hoặc bấm Create của luồng tạo, Chung b4 — Sign In từ menu, Chung b4a — Chạm ô SĐT (+28 more)

### Community 12 - "build_random_steps"
Cohesion: 0.08
Nodes (7): resume_common_index(), build_random_steps(), finish_view(), B1–b3 xem menu ngẫu nhiên cho 12 máy — 14/11/2026, Dự phòng dùng chung khi chạy song song — 14/11/2026, adb(), wait()

### Community 14 - "desktop.py"
Cohesion: 0.06
Nodes (15): _automatic_resume_slots(), save(), default_path(), AccountData, AppSettings, load_settings(), save_settings(), settings_path() (+7 more)

### Community 16 - "Ảnh hướng dẫn q1/q2 và menu chung lưu cục bộ"
Cohesion: 0.07
Nodes (29): 14 ảnh menu chung b1–b3 ngẫu nhiên — 14/11/2026, B16–b22 chung — Đổi marketplace sang United States (18/11/2026), B32–b39 — Reload Balance, thêm thẻ và địa chỉ thanh toán (21/11/2026), B6 — Hai ảnh đính kèm mới ngày 13/11/2026, Menu chung ảnh 01 — Danh sách chữ, Menu chung ảnh 02 — App Store bên phải sau khi Amazon mở, q1 b6 — US +1 hiện nhưng chạm không đóng hộp, 14/11/2026, q1 ảnh 01 — Menu và ba thẻ (+21 more)

### Community 17 - "home_menu.py"
Cohesion: 0.14
Nodes (9): _confirm_menu_fallback(), _menu_evidence(), MenuReadUnavailable, _nodes(), budget(), open_home_menu(), _tap(), HomeMenuTests (+1 more)

### Community 18 - "AttemptDeadline"
Cohesion: 0.07
Nodes (23): AttemptDeadline, MarketplaceFlowTests, read(), adb(), read(), tap(), read(), read() (+15 more)

### Community 19 - "marketplace_flow.py"
Cohesion: 0.21
Nodes (23): _account_tab(), run(), account_target(), back_and_read_text(), foreground_ready(), recover_country_list(), _country_card(), _destination() (+15 more)

### Community 20 - "_find_scrolling"
Cohesion: 0.14
Nodes (21): _at_or_after(), country(), sign_in(), _country_nodes(), _ensure_menu(), _find_scrolling(), _tap_for_transition(), _unique() (+13 more)

### Community 21 - "Điều hướng hai dạng menu ba gạch"
Cohesion: 0.50
Nodes (4): Bằng chứng và phạm vi, Kiểm chứng, Quy tắc chạy, Điều hướng hai dạng menu ba gạch

### Community 22 - "Q3Q4FlowTests"
Cohesion: 0.21
Nodes (3): build_q3_steps(), build_q4_steps(), Q3Q4FlowTests

### Community 23 - "_type_field"
Cohesion: 0.15
Nodes (10): confirmed_login_otp_nodes(), enter_otp(), focus_otp(), focus_phone(), read_sms_form(), _field(), _tap_input(), _type_field() (+2 more)

### Community 24 - "phone_window_layout.py"
Cohesion: 0.13
Nodes (5): arrange_on_open(), _row_if_fits(), _sort_key(), _tiles(), PhoneWindowLayoutTests

### Community 25 - "Nghiên cứu và tích hợp Swarmote"
Cohesion: 0.40
Nodes (4): Hành vi có bằng chứng, Kiểm thử còn lại, Nghiên cứu và tích hợp Swarmote, Phần đã áp dụng

### Community 26 - "q7_state_machine.py"
Cohesion: 0.09
Nodes (17): ActionValidator, _already_reached_result(), _browse_ready_after_sms(), build_q7_pilot_steps(), run(), _past_known_step(), RecoveryHandler, ResultVerifier (+9 more)

### Community 27 - "ExtendedRecoveryTests"
Cohesion: 0.15
Nodes (6): _start_and_confirm(), ExtendedRecoveryTests, fail(), read(), read(), menu()

### Community 28 - "amazon_is_foreground"
Cohesion: 0.09
Nodes (10): verify_menu_open(), cloud_serials(), CloudPhone, route(), CloudBridgeTests, adb(), step(), Q6FlowTests (+2 more)

### Community 30 - "RegistrationState"
Cohesion: 0.11
Nodes (3): RegistrationState, build_tail_steps(), RandomPrefixTests

### Community 31 - "PROJECT_INDEX.md"
Cohesion: 0.21
Nodes (6): Hướng dẫn khi tiếp tục dự án, Bản đồ repository, Luồng q2 từ menu ba gạch, q3 — b1–b3 và nối luồng chung, q4 — Giỏ hàng, Pets, Home and DIY, q6 — Trang chủ, Giỏ hàng, menu và một thẻ

### Community 32 - "RandomPrefixTests"
Cohesion: 0.11
Nodes (4): RandomPrefixTests, adb(), adb(), adb()

### Community 33 - "core.py"
Cohesion: 0.28
Nodes (19): adb(), available_memory_mb(), check_play(), configure_avd(), connected_devices(), Device, device_avd_name(), device_resources() (+11 more)

### Community 34 - "vision.py"
Cohesion: 0.07
Nodes (19): _bounds(), _canonical_text(), _compact(), _engine(), _field_contents(), _field_is_blank(), _input_box(), _join_wrapped_categories() (+11 more)

### Community 35 - "setup.py"
Cohesion: 0.17
Nodes (13): app_data_dir(), avd_names(), create_avd(), doctor(), executable(), installed_image(), run(), sdk_root() (+5 more)

### Community 36 - "_visible"
Cohesion: 0.13
Nodes (32): _bounds(), _resume_address_payment_index(), _text(), _visible(), _action(), _address_form(), _addresses(), _bounded_native() (+24 more)

### Community 37 - "time"
Cohesion: 0.20
Nodes (12): check_runtime(), main(), verify(), _app_installed(), _app_paths(), _check_external_apps(), _install_python_dependencies(), main() (+4 more)

### Community 38 - "retry_preparation"
Cohesion: 0.18
Nodes (4): emit(), retry_preparation(), Mã hiện có, P03 — Mở form New Profile

### Community 39 - "build_create_address_steps"
Cohesion: 0.24
Nodes (4): build_create_address_steps(), CreateAddressFlowTests, read(), node()

### Community 40 - "main"
Cohesion: 0.15
Nodes (9): main(), main(), Đợt tăng tốc và tự phục hồi b4–b11 ngày 13/11/2026, File dự án mà Graphify không phân tích trực tiếp, .gitignore, Launch Swarmote Tool.pyw, pyproject.toml, Ảnh PNG trong dự án (+1 more)

### Community 41 - "cli.py"
Cohesion: 0.18
Nodes (13): BatchItem, parse_proxy_line(), prepare_five(), main(), parser(), report(), open_amazon(), foreground() (+5 more)

### Community 42 - "Bàn giao trạng thái dự án — 13/11/2026"
Cohesion: 0.11
Nodes (16): set_tk_icon(), B6 danh sách quốc gia vẫn mở sau khi chọn — 13/11/2026, Bàn giao trạng thái dự án — 13/11/2026, Bản chính boom4may và bản dự phòng — 14/11/2026, Bộ cài offline chia sẻ — 14/11/2026, Cài đặt máy mới, Dừng riêng máy đang chọn — 14/11/2026, Hàng đợi 4 máy với giới hạn 2 Running — 14/11/2026 (+8 more)

### Community 43 - "q7_random_prefix.py"
Cohesion: 0.10
Nodes (22): scroll_view(), wait_until(), RecoverableStepError, build_random_steps(), browse(), action(), run_browse(), finish_view() (+14 more)

### Community 44 - "FakeControl"
Cohesion: 0.13
Nodes (5): ParallelInstallTests, PhoneWindow, FakeControl, InstallTests, descendants()

### Community 45 - "_scroll_up"
Cohesion: 0.36
Nodes (9): _scroll_up(), open_menu(), read_menu(), return_to_menu(), view(), visit(), action(), visit_seconds() (+1 more)

### Community 46 - "ui_backend.py"
Cohesion: 0.13
Nodes (11): swarmote_adb_path(), swarmote_tunnel_owner(), _connect(), country_reverse_points(), country_scroll(), _failed(), read_tree(), ready() (+3 more)

### Community 47 - "cloud_adb"
Cohesion: 0.17
Nodes (19): _keyboard_visible(), _tap(), cloud_adb(), package_path(), probe(), prop(), reported_installer(), _scroll() (+11 more)

### Community 48 - "bulk_input.py"
Cohesion: 0.08
Nodes (11): BulkRecord, lines(), parse_bulk_payload(), parse_column(), _proxy_rows(), _table_cells(), _url_from_cell(), validate_card() (+3 more)

### Community 49 - "swarmote_desktop.py"
Cohesion: 0.17
Nodes (14): _activate_manager(), _create_profile_form(), _invoke(), _one(), _profile_checkbox(), _profile_form_open(), ProfileCreateNotSubmitted, ProxyTestFailed (+6 more)

### Community 50 - "account_flow.py"
Cohesion: 0.12
Nodes (20): _ActionNotResolved, _button(), _country_full_row(), _form_action(), _parse_ui_nodes(), _read_hierarchy(), _read_login_sms_visual(), _read_nodes_once() (+12 more)

### Community 51 - "b1–b11 Reliability and Latency Implementation Plan"
Cohesion: 0.18
Nodes (10): b1–b11 Reliability and Latency Implementation Plan, Completion Criteria, File Map, Global Constraints, Review Focus, Task 1: Measure current step latency and classify existing failures, Task 2: Define safe retry, reconcile, pause, and stop behavior, Task 3: Reduce redundant UI reads and unnecessary waits (+2 more)

### Community 52 - ".test_tail_stop_after_swipe_resumes_remaining_view_before_back"
Cohesion: 0.18
Nodes (3): browse(), tap(), tap()

### Community 53 - "Danh mục ảnh nằm trong dự án"
Cohesion: 0.22
Nodes (9): amazon_android/assets/obsidian_prism.png, amazon_android/assets/swarmote_tool_square.png và swarmote_tool.ico, assets/ui_history/machine7_input_before.png, assets/ui_history/reset_check.png, assets/ui_history/ui-12.png, assets/ui_history/ui_palette_preview.png, assets/ui_history/ui-preview.png, assets/ui_history/ui-screenshot.png (+1 more)

### Community 54 - "build_q1_steps"
Cohesion: 0.25
Nodes (5): build_q1_steps(), category(), Cách xử lý ảnh tiếp theo, Phần riêng từng máy, Tiến độ hướng dẫn bằng ảnh — cập nhật 13/11/2026

### Community 55 - "Amazon Android Tool — Giai đoạn A/B"
Cohesion: 0.29
Nodes (7): Amazon Android Tool — Giai đoạn A/B, Cài trên máy Windows mới, Dán nhiều proxy, Sử dụng, Trạng thái nghiệm thu, Yêu cầu, Điện thoại đám mây Swarmote

### Community 56 - "_proxy_postal_prefix"
Cohesion: 0.48
Nodes (3): _proxy_postal_prefix(), controls(), ProxyPostalPrefixTests

### Community 58 - "Giao diện vận hành"
Cohesion: 0.40
Nodes (4): Bố cục, Giao diện vận hành, Hướng thị giác, Quy tắc

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
Cohesion: 0.27
Nodes (4): CountryRecoveryTests, read(), wait(), node()

### Community 65 - "PhoneReader"
Cohesion: 0.24
Nodes (7): phone_reader(), PhoneReader, ReaderResponseError, fake_worker(), IsolationTests, duplicate(), production_worker_with_fake_android()

### Community 66 - "VERIFICATION.md"
Cohesion: 0.17
Nodes (10): Kết luận và tích hợp, Kết quả thực tế, So sánh bộ đọc trên q1 — 13/11/2026, Thành phần thiết bị, b1–b3 bắt buộc có ba cú bấm — 14/11/2026, b1–b3 ngẫu nhiên cho 12 máy — 14/11/2026, b1–b3 ngẫu nhiên trên 12 máy, không dùng OCR — 14/11/2026, b6 cuộn tới đáy rồi vuốt ngược — 14/11/2026 (+2 more)

### Community 69 - "run_batch"
Cohesion: 0.09
Nodes (23): _phone_preparation_lock(), _prepare_phone(), _prepare_phone_locked(), stop_here(), run_batch(), fill_slots(), manually_selected(), refresh_slots() (+15 more)

### Community 71 - "PROJECT_HANDOFF.md"
Cohesion: 0.11
Nodes (17): b1–b3 ngẫu nhiên cho q1–q12 — 14/11/2026, B4–b11 chạy đồng thời và OCR — 14/11/2026, b6 US +1 còn mở sau bốn cú chạm — 14/11/2026, Bản thử State Machine q7 và b1–b3 mở mục con — 14/11/2026, Bỏ thời hạn tổng sau menu — 14/11/2026, Bổ sung đọc ảnh OCR và chạm trực tiếp dự phòng cho b26 khi uiautomator dump WebView lỗi — 19/11/2026, Cơ chế chụp ảnh OCR quét chữ ấn luôn cho toàn bộ b26–b31 — 19/11/2026, Dán nhiều proxy cách nhau bằng dấu cách — 14/11/2026 (+9 more)

### Community 72 - "ProxyConfig"
Cohesion: 0.16
Nodes (8): create_profile(), ProxyConfig, Giới hạn và lựa chọn cần xác minh, Kế hoạch sửa luồng mẻ Swarmote, Kết luận đã xác minh, Quy trình đích, Thứ tự thực hiện, CreationWindowVisibilityTests

### Community 74 - "test_swarmote_navigation.py"
Cohesion: 0.13
Nodes (8): _open_profiles(), visible_profile_names(), control(), ProfilesNavigationTests, descendants(), invoke(), descendants(), descendants()

### Community 75 - "screen"
Cohesion: 0.11
Nodes (27): continue_number(), finish_auto(), finish_create(), finish_login(), name(), phone_number(), proceed(), send_sms() (+19 more)

### Community 76 - "._build_main"
Cohesion: 0.23
Nodes (3): _crystal_art(), _edge_light(), Ô Amazon riêng Máy 1–12 dễ thấy hơn — 14/11/2026

### Community 79 - "Giai đoạn 2 — bản thử State Machine riêng q7"
Cohesion: 0.40
Nodes (5): Cách thử bản pilot cũ (không áp dụng cho factory hiện hành), Giai đoạn 2 — bản thử State Machine riêng q7, Giới hạn, Phạm vi và quan hệ với luồng cũ, Sơ đồ

### Community 81 - "_tail_menu"
Cohesion: 0.11
Nodes (16): amazon_is_foreground(), build_marketplace_steps(), build_post_auth_steps(), _tail_candidates(), _tail_input_action(), _tail_menu(), _tail_safe_page_choices(), Phần dùng chung đã được hướng dẫn (+8 more)

### Community 83 - "RunJob"
Cohesion: 0.10
Nodes (9): UnknownStateHandler, _choose_tail_target(), RunJob, Một quy luật để sửa mã về sau — 20/11/2026, Q5FlowTests, continuation(), choose(), choose() (+1 more)

### Community 84 - "OTP_DESIGN.md"
Cohesion: 0.50
Nodes (3): Nối vào bước tạo tài khoản sau khi xác minh màn hình Amazon, Thiết kế OTP cho từng Profile, Đã chuẩn bị

### Community 85 - "ensure_manager_ready"
Cohesion: 0.17
Nodes (8): ensure_manager_ready(), inspect(), _main_window(), collect(), ProfileManagerWindowError, _swarmote_exe(), ManagerStartupTests, unavailable()

### Community 89 - "._apply_bulk_text"
Cohesion: 0.15
Nodes (8): 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng, Các bước, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Rủi ro và bảo trì, Thiết kế yêu cầu, Điều kiện dừng

### Community 92 - "GRAPH_AUDIT.md"
Cohesion: 0.50
Nodes (3): Cách kiểm tra sau mỗi sửa đổi, Giới hạn đã xác nhận, Kiểm tra độ phủ Graphify — cập nhật 26/11/2026

## Knowledge Gaps
- **1 isolated node(s):** `amazon-android-tool`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 537 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **18 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ToolError` connect `ToolError` to `build_common_steps`, `otp.py`, `BulkInputTests`, `show_apps`, `RunnerTests`, `PostMenuStep`, `.test_only_confirmed_target_names_are_selected_for_one_start_command`, `build_create_address_detail_steps`, `build_random_steps`, `StopResetTests`, `desktop.py`, `home_menu.py`, `AttemptDeadline`, `marketplace_flow.py`, `_find_scrolling`, `_type_field`, `q7_state_machine.py`, `ExtendedRecoveryTests`, `amazon_is_foreground`, `._refresh_devices`, `RegistrationState`, `RandomPrefixTests`, `core.py`, `vision.py`, `setup.py`, `_visible`, `retry_preparation`, `build_create_address_steps`, `cli.py`, `q7_random_prefix.py`, `_scroll_up`, `ui_backend.py`, `cloud_adb`, `bulk_input.py`, `swarmote_desktop.py`, `account_flow.py`, `build_reload_payment_steps`, `CountryRecoveryTests`, `PhoneReader`, `run_batch`, `ProxyConfig`, `BatchDraft`, `test_swarmote_navigation.py`, `screen`, `Window`, `_tail_menu`, `RunJob`, `ensure_manager_ready`, `otp_token`, `._apply_bulk_text`?**
  _High betweenness centrality (0.383) - this node is a cross-community bridge._
- **Are the 58 inferred relationships involving `ToolError` (e.g. with `_read_nodes_once()` and `_resume_address_payment_index()`) actually correct?**
  _`ToolError` has 58 INFERRED edges - model-reasoned connections that need verification._
- **What connects `amazon-android-tool` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `ToolError` be split into smaller, more focused modules?**
  _Cohesion score 0.11428571428571428 - nodes in this community are weakly interconnected._
- **Why does `CloudPhone` connect `amazon_is_foreground` to `ToolError`, `build_common_steps`, `show_apps`, `PostMenuStep`, `build_create_address_detail_steps`, `build_random_steps`, `desktop.py`, `home_menu.py`, `AttemptDeadline`, `_find_scrolling`, `Q3Q4FlowTests`, `_type_field`, `q7_state_machine.py`, `ExtendedRecoveryTests`, `RegistrationState`, `RandomPrefixTests`, `_visible`, `build_create_address_steps`, `cli.py`, `q7_random_prefix.py`, `_scroll_up`, `ui_backend.py`, `cloud_adb`, `swarmote_desktop.py`, `account_flow.py`, `.test_tail_stop_after_swipe_resumes_remaining_view_before_back`, `build_q1_steps`, `._start_post_menu`, `build_reload_payment_steps`, `CountryRecoveryTests`, `PhoneReader`, `run_batch`, `screen`, `Q2FlowTests`, `Window`, `_tail_menu`, `RunJob`, `.test_manual_otp_repair_continues_with_confirmation_and_tail_for_both_modes`?**
  _High betweenness centrality (0.112) - this node is a cross-community bridge._
- **Are the 88 inferred relationships involving `CloudPhone` (e.g. with `build_common_steps()` and `_country_full_row()`) actually correct?**
  _`CloudPhone` has 88 INFERRED edges - model-reasoned connections that need verification._
- **Should `build_common_steps` be split into smaller, more focused modules?**
  _Cohesion score 0.05292702485966319 - nodes in this community are weakly interconnected._