# Graph Report - boom4may  (2026-11-27)

## Corpus Check
- 135 files · ~168,489 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 1, .bat 1, .pyw 1)

## Summary
- 2190 nodes · 7631 edges · 97 communities (75 shown, 22 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 1095 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `745484c6`
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
- adb
- StopResetTests
- cloud.py
- amazon-android-tool
- Ảnh hướng dẫn q1/q2 và menu chung lưu cục bộ
- open_home_menu
- MarketplaceFlowTests
- marketplace_flow.py
- _read_nodes
- MENU_ROUTING.md
- Q3Q4FlowTests
- core.py
- _find_scrolling
- Nghiên cứu và tích hợp Swarmote
- q7_state_machine.py
- CloudPhone
- amazon_is_foreground
- Window
- RegistrationState
- PROJECT_INDEX.md
- build_random_steps
- ui_backend.py
- vision.py
- settings.py
- _visible
- subprocess
- ._run
- build_create_address_steps
- main
- cli.py
- Bàn giao trạng thái dự án — 13/11/2026
- q7_state_machine.py
- FakeControl
- _nodes
- setup_windows.py
- cloud_adb
- Value
- swarmote_desktop.py
- SafetyTests
- b1–b11 Reliability and Latency Implementation Plan
- cli.py
- Danh mục ảnh nằm trong dự án
- _tail_candidates
- Amazon Android Tool — Giai đoạn A/B
- profile_status
- _CombinedStop
- Giao diện vận hành
- _choose_tail_target
- Amazon trên Swarmote
- CloudPhone
- build_reload_payment_steps
- Bộ cài chia sẻ Windows x64
- CountryRecoveryTests
- test_isolated_reader.py
- VERIFICATION.md
- BatchDraft
- _prepare_phone
- _tap_child
- .test_b10_stalled_whatsapp_pauses_only_affected_phone
- PROJECT_HANDOFF.md
- _restore_prefix_menu
- ._continue_profile
- ProfilesNavigationTests
- ToolError
- retry_preparation
- Bàn giao dừng theo yêu cầu người dùng — 13/11/2026
- _ScreenWaitExpired
- _yellow_form_button
- _scroll_up
- action
- _start_and_confirm
- RunJob
- OTP_DESIGN.md
- ensure_manager_ready
- _tail_menu
- build_random_steps
- 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng
- SharedFallbackTests
- .test_selected_stop_finishes_install_before_stopping_that_phone
- GRAPH_AUDIT.md
- .test_b11_taps_otp_field_even_when_provider_read_fails
- PreparationProgressTests

## God Nodes (most connected - your core abstractions)
1. `ToolError` - 354 edges
2. `CloudPhone` - 234 edges
3. `AttemptDeadline` - 202 edges
4. `RunJob` - 170 edges
5. `RegistrationState` - 162 edges
6. `build_common_steps()` - 115 edges
7. `Window` - 98 edges
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

## Communities (97 total, 22 thin omitted)

### Community 0 - "registration.py"
Cohesion: 0.20
Nodes (12): require_online(), _field_for_label(), fill_identifier(), fill_signup_form(), _nodes(), open_entry(), status(), _tap() (+4 more)

### Community 1 - "build_common_steps"
Cohesion: 0.09
Nodes (3): build_common_steps(), node(), Q1FlowTests

### Community 2 - "otp.py"
Cohesion: 0.09
Nodes (9): browser_launch_options(), extract_otp(), _NoRedirect, read_otp(), _read_otp_in_browser(), validate_otp_url(), wait_for_new_otp(), OtpTests (+1 more)

### Community 3 - "BulkInputTests"
Cohesion: 0.10
Nodes (3): parse_column(), parse_records(), BulkInputTests

### Community 4 - "windows_identity.py"
Cohesion: 0.18
Nodes (8): create_shortcut(), relaunch_command(), runtime(), set_process_identity(), set_tk_icon(), set_window_identity(), Sửa shortcut ghim mở nhầm IDLE — 13/11/2026, WindowsIdentityTests

### Community 5 - "swarmote_desktop.py"
Cohesion: 0.10
Nodes (23): ready_for_home_menu(), _check_stop(), collapse_apps_panel(), install_amazon(), check_stop(), open_adb_shell(), _pause(), _phone_window() (+15 more)

### Community 6 - "RunnerTests"
Cohesion: 0.06
Nodes (14): ProfileRegistry, absent(), ProfileRegistryTests, RunnerTests, create(), resume(), create(), failed_start() (+6 more)

### Community 7 - "PostMenuStep"
Cohesion: 0.08
Nodes (17): route(), current(), PostMenuSession, PostMenuStep, Không bỏ qua b1–b3 ngẫu nhiên; 14 ảnh menu mới — 14/11/2026, PostMenuTests, reconcile(), step() (+9 more)

### Community 8 - "ToolError"
Cohesion: 0.11
Nodes (6): BatchStartTests, checkbox(), toggle(), descendants(), FakeBox, FakeButton

### Community 9 - "AddressDetailTests"
Cohesion: 0.13
Nodes (7): build_create_address_detail_steps(), AddressDetailTests, read(), adb(), tap(), read(), item()

### Community 10 - "003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật"
Cohesion: 0.08
Nodes (20): 003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật, Các bước, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Quy trình đích, Rủi ro và bảo trì, Điều kiện dừng (+12 more)

### Community 11 - "Danh mục từng bước đã biết — 13/11/2026"
Cohesion: 0.06
Nodes (35): Bản thử q7 State Machine — 14/11/2026, Chung b10 — Chuyển WhatsApp sang SMS, Chung b11 — Lấy và gõ OTP SMS, Chung b11a — Chạm ô OTP trên màn SMS, Chung b11b — Xác minh đăng nhập hoặc bấm Create của luồng tạo, Chung b4 — Sign In từ menu, Chung b4a — Chạm ô SĐT, Chung b5 — Gõ số điện thoại (+27 more)

### Community 12 - "adb"
Cohesion: 0.07
Nodes (7): adb(), adb(), tap(), adb(), wait(), adb(), tap()

### Community 16 - "Ảnh hướng dẫn q1/q2 và menu chung lưu cục bộ"
Cohesion: 0.07
Nodes (28): B16–b22 chung — Đổi marketplace sang United States (18/11/2026), B32–b39 — Reload Balance, thêm thẻ và địa chỉ thanh toán (21/11/2026), B6 — Hai ảnh đính kèm mới ngày 13/11/2026, Menu chung ảnh 01 — Danh sách chữ, Menu chung ảnh 02 — App Store bên phải sau khi Amazon mở, q1 b6 — US +1 hiện nhưng chạm không đóng hộp, 14/11/2026, q1 ảnh 01 — Menu và ba thẻ, q1 ảnh 02 — Sign In cuối menu (+20 more)

### Community 17 - "open_home_menu"
Cohesion: 0.18
Nodes (8): _confirm_menu_fallback(), _menu_evidence(), open_home_menu(), _tap(), Lỗi chạy song song q3 Terminal trùng / q1 chưa thấy menu — 14/11/2026, ParallelNavigationRegressionTests, Cập nhật luồng mẻ trước đó — 2026-11-13, q14 mở Amazon lần đầu — 2026-11-13

### Community 18 - "MarketplaceFlowTests"
Cohesion: 0.06
Nodes (22): MarketplaceFlowTests, read(), adb(), read(), tap(), read(), read(), pause() (+14 more)

### Community 19 - "marketplace_flow.py"
Cohesion: 0.19
Nodes (24): _account_tab(), run(), account_target(), back_and_read_text(), foreground_ready(), recover_country_list(), _destination(), _en_button() (+16 more)

### Community 20 - "_read_nodes"
Cohesion: 0.11
Nodes (28): _at_or_after(), sign_in(), _ensure_menu(), home_visible(), menu_layout(), _read_nodes(), route_list_menu(), _tap() (+20 more)

### Community 21 - "MENU_ROUTING.md"
Cohesion: 0.23
Nodes (7): Bằng chứng và phạm vi, Kiểm chứng, Quy tắc chạy, Điều hướng hai dạng menu ba gạch, Luồng q1 từ menu ba gạch tới nhập OTP, Thử trên q1 đã có, Luồng q2 từ menu ba gạch

### Community 22 - "Q3Q4FlowTests"
Cohesion: 0.21
Nodes (3): build_q3_steps(), build_q4_steps(), Q3Q4FlowTests

### Community 23 - "core.py"
Cohesion: 0.24
Nodes (19): adb(), available_memory_mb(), check_play(), configure_avd(), connected_devices(), Device, device_avd_name(), device_resources() (+11 more)

### Community 25 - "Nghiên cứu và tích hợp Swarmote"
Cohesion: 0.40
Nodes (4): Hành vi có bằng chứng, Kiểm thử còn lại, Nghiên cứu và tích hợp Swarmote, Phần đã áp dụng

### Community 26 - "q7_state_machine.py"
Cohesion: 0.09
Nodes (12): _already_reached_result(), build_q7_pilot_steps(), run(), _past_known_step(), ResultVerifier, StateDeadline, StateDetector, StateMachineStop (+4 more)

### Community 27 - "CloudPhone"
Cohesion: 0.09
Nodes (19): _read_nodes_once(), resume_common_index(), CloudPhone, probe(), prop(), reported_installer(), reconcile(), phone_reader() (+11 more)

### Community 28 - "amazon_is_foreground"
Cohesion: 0.14
Nodes (5): amazon_is_foreground(), cloud_serials(), CloudBridgeTests, adb(), Ẩn cửa sổ cmd khi gọi ADB — 2026-11-13

### Community 29 - "Window"
Cohesion: 0.09
Nodes (5): Window, Các bước, Trạng thái kiểm chứng và giới hạn, DesktopLayoutTests, __init__()

### Community 30 - "RegistrationState"
Cohesion: 0.13
Nodes (3): RegistrationState, build_tail_steps(), RandomPrefixTests

### Community 31 - "PROJECT_INDEX.md"
Cohesion: 0.15
Nodes (9): Hướng dẫn khi tiếp tục dự án, Cách xử lý ảnh tiếp theo, Tiến độ hướng dẫn bằng ảnh — cập nhật 13/11/2026, Quy trình Swarmote hiện tại, Bản đồ repository, q3 — b1–b3 và nối luồng chung, q4 — Giỏ hàng, Pets, Home and DIY, q5 — ba thẻ riêng và b4–b11 chung (+1 more)

### Community 32 - "build_random_steps"
Cohesion: 0.12
Nodes (4): RandomPrefixTests, adb(), adb(), adb()

### Community 33 - "ui_backend.py"
Cohesion: 0.08
Nodes (14): swarmote_tunnel_owner(), arrange_on_open(), _row_if_fits(), _sort_key(), _tiles(), country_reverse_points(), country_scroll(), _failed() (+6 more)

### Community 34 - "vision.py"
Cohesion: 0.07
Nodes (19): _bounds(), _canonical_text(), _compact(), _engine(), _field_contents(), _field_is_blank(), _input_box(), _join_wrapped_categories() (+11 more)

### Community 35 - "settings.py"
Cohesion: 0.17
Nodes (8): save(), default_path(), AppSettings, load_settings(), save_settings(), settings_path(), ProfileManagerWindowError, SettingsTests

### Community 36 - "_visible"
Cohesion: 0.17
Nodes (28): _bounds(), _button(), _text(), _visible(), _action(), _address_form(), _addresses(), _bounded_native() (+20 more)

### Community 37 - "subprocess"
Cohesion: 0.13
Nodes (16): app_data_dir(), avd_names(), create_avd(), doctor(), executable(), installed_image(), run(), sdk_root() (+8 more)

### Community 38 - "._run"
Cohesion: 0.15
Nodes (10): _profile_row_status(), ProfileLookupError, 002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ, Các bước, Kiểm tra bắt buộc, Phạm vi, Rủi ro và bảo trì, Thiết kế yêu cầu (+2 more)

### Community 39 - "build_create_address_steps"
Cohesion: 0.24
Nodes (4): build_create_address_steps(), CreateAddressFlowTests, read(), node()

### Community 40 - "main"
Cohesion: 0.16
Nodes (9): main(), main(), Đợt tăng tốc và tự phục hồi b4–b11 ngày 13/11/2026, File dự án mà Graphify không phân tích trực tiếp, .gitignore, Launch Swarmote Tool.pyw, pyproject.toml, Ảnh PNG trong dự án (+1 more)

### Community 41 - "cli.py"
Cohesion: 0.09
Nodes (19): BatchItem, parse_proxy_line(), prepare_five(), BulkRecord, lines(), parse_bulk_payload(), _proxy_rows(), _url_from_cell() (+11 more)

### Community 42 - "Bàn giao trạng thái dự án — 13/11/2026"
Cohesion: 0.11
Nodes (16): B6 danh sách quốc gia vẫn mở sau khi chọn — 13/11/2026, Bàn giao trạng thái dự án — 13/11/2026, Bản chính boom4may và bản dự phòng — 14/11/2026, Bộ cài offline chia sẻ — 14/11/2026, Cài đặt máy mới, Dừng riêng máy đang chọn — 14/11/2026, Dự phòng dùng chung khi chạy song song — 14/11/2026, Mã hiện có (+8 more)

### Community 43 - "q7_state_machine.py"
Cohesion: 0.13
Nodes (20): _parse_ui_nodes(), _read_hierarchy(), _UiReadIncomplete, RecoverableStepError, build_random_steps(), browse(), action(), run_browse() (+12 more)

### Community 44 - "FakeControl"
Cohesion: 0.13
Nodes (5): ParallelInstallTests, PhoneWindow, FakeControl, InstallTests, descendants()

### Community 45 - "_nodes"
Cohesion: 0.18
Nodes (5): MenuReadUnavailable, _nodes(), budget(), HomeMenuTests, menu()

### Community 46 - "setup_windows.py"
Cohesion: 0.28
Nodes (9): _app_installed(), _app_paths(), _check_external_apps(), _install_python_dependencies(), main(), _offer_downloads(), _ready_file_matches(), _runtime_imports_work() (+1 more)

### Community 47 - "cloud_adb"
Cohesion: 0.15
Nodes (21): _keyboard_visible(), _resume_address_payment_index(), cloud_adb(), foreground(), _scroll(), _account_content(), run(), _foreground() (+13 more)

### Community 49 - "swarmote_desktop.py"
Cohesion: 0.10
Nodes (27): package_path(), _activate_manager(), _create_profile_form(), _descendants(), inspect(), _invoke(), _main_window(), collect() (+19 more)

### Community 51 - "b1–b11 Reliability and Latency Implementation Plan"
Cohesion: 0.18
Nodes (10): b1–b11 Reliability and Latency Implementation Plan, Completion Criteria, File Map, Global Constraints, Review Focus, Task 1: Measure current step latency and classify existing failures, Task 2: Define safe retry, reconcile, pause, and stop behavior, Task 3: Reduce redundant UI reads and unnecessary waits (+2 more)

### Community 52 - "cli.py"
Cohesion: 0.18
Nodes (10): _table_cells(), main(), parser(), report(), open_amazon(), scan(), get_device(), print_json() (+2 more)

### Community 53 - "Danh mục ảnh nằm trong dự án"
Cohesion: 0.22
Nodes (9): amazon_android/assets/obsidian_prism.png, amazon_android/assets/swarmote_tool_square.png và swarmote_tool.ico, assets/ui_history/machine7_input_before.png, assets/ui_history/reset_check.png, assets/ui_history/ui-12.png, assets/ui_history/ui_palette_preview.png, assets/ui_history/ui-preview.png, assets/ui_history/ui-screenshot.png (+1 more)

### Community 54 - "_tail_candidates"
Cohesion: 0.20
Nodes (3): _browse_ready_after_sms(), _tail_candidates(), _tail_safe_page_choices()

### Community 55 - "Amazon Android Tool — Giai đoạn A/B"
Cohesion: 0.29
Nodes (7): Amazon Android Tool — Giai đoạn A/B, Cài trên máy Windows mới, Dán nhiều proxy, Sử dụng, Trạng thái nghiệm thu, Yêu cầu, Điện thoại đám mây Swarmote

### Community 56 - "profile_status"
Cohesion: 0.48
Nodes (3): _proxy_postal_prefix(), controls(), ProxyPostalPrefixTests

### Community 58 - "Giao diện vận hành"
Cohesion: 0.40
Nodes (4): Bố cục, Giao diện vận hành, Hướng thị giác, Quy tắc

### Community 59 - "_choose_tail_target"
Cohesion: 0.25
Nodes (4): _choose_tail_target(), _TailChoicesExhausted, choose(), choose()

### Community 60 - "Amazon trên Swarmote"
Cohesion: 0.33
Nodes (5): Amazon trên Swarmote, Người dùng và công việc, Nền tảng, Điều chưa xác minh, Định hướng ngôn ngữ nếu xây dựng lại — 23/11/2026

### Community 61 - "CloudPhone"
Cohesion: 0.08
Nodes (25): b6 Country US +1 — 14/11/2026, B6 cuộn quốc gia và chọn lại — 13/11/2026, Biên bản kiểm tra thực tế — 2026-11-12, Cài và đo UiAutomator2 theo phê duyệt mới — 13/11/2026, Dừng riêng một máy — 14/11/2026, Focus ô nhập b4–b11 — 14/11/2026, Ghim taskbar — 13/11/2026, Giao diện sáng, dễ đọc — 2026-11-13 (+17 more)

### Community 62 - "build_reload_payment_steps"
Cohesion: 0.08
Nodes (13): enter_otp(), _type_field(), build_reload_payment_steps(), FlowRecoveryTests, form(), node(), ReloadPaymentTests, adb() (+5 more)

### Community 63 - "Bộ cài chia sẻ Windows x64"
Cohesion: 0.50
Nodes (3): Bộ cài chia sẻ Windows x64, Dựng lại, Nguồn thành phần

### Community 64 - "CountryRecoveryTests"
Cohesion: 0.24
Nodes (5): _same_country_position(), CountryRecoveryTests, read(), wait(), node()

### Community 65 - "test_isolated_reader.py"
Cohesion: 0.27
Nodes (5): PhoneReader, ReaderResponseError, fake_worker(), IsolationTests, duplicate()

### Community 66 - "VERIFICATION.md"
Cohesion: 0.15
Nodes (11): Kết luận và tích hợp, Kết quả thực tế, So sánh bộ đọc trên q1 — 13/11/2026, Thành phần thiết bị, b1–b3 bắt buộc có ba cú bấm — 14/11/2026, b1–b3 ngẫu nhiên cho 12 máy — 14/11/2026, b1–b3 ngẫu nhiên trên 12 máy, không dùng OCR — 14/11/2026, b6 cuộn tới đáy rồi vuốt ngược — 14/11/2026 (+3 more)

### Community 68 - "_prepare_phone"
Cohesion: 0.10
Nodes (19): _prepare_phone(), _prepare_phone_locked(), progress(), stop_here(), run_batch(), fill_slots(), manually_selected(), refresh_slots() (+11 more)

### Community 69 - "_tap_child"
Cohesion: 0.25
Nodes (3): _new_prefix(), _tap_child(), Tăng số lần thử đọc cây Android và bổ sung phương án dự phòng cho b23–b31 — 19/11/2026

### Community 71 - "PROJECT_HANDOFF.md"
Cohesion: 0.12
Nodes (15): b1–b3 ngẫu nhiên cho q1–q12 — 14/11/2026, B4–b11 chạy đồng thời và OCR — 14/11/2026, b6 US +1 còn mở sau bốn cú chạm — 14/11/2026, Bản thử State Machine q7 và b1–b3 mở mục con — 14/11/2026, Bỏ thời hạn tổng sau menu — 14/11/2026, Bổ sung đọc ảnh OCR và chạm trực tiếp dự phòng cho b26 khi uiautomator dump WebView lỗi — 19/11/2026, Cơ chế chụp ảnh OCR quét chữ ấn luôn cho toàn bộ b26–b31 — 19/11/2026, Dán bảng Amazon có ghi chú thẻ live và URL OTP escaped — 14/11/2026 (+7 more)

### Community 72 - "_restore_prefix_menu"
Cohesion: 0.12
Nodes (10): browse(), action(), sign_in(), _first_point(), _prefix_nodes(), _PrefixRecoveryStop, _restore_prefix_menu(), 14 ảnh menu chung b1–b3 ngẫu nhiên — 14/11/2026 (+2 more)

### Community 74 - "ProfilesNavigationTests"
Cohesion: 0.12
Nodes (10): ProfileCreateNotSubmitted, unavailable(), failed(), create(), control(), ProfilesNavigationTests, descendants(), invoke() (+2 more)

### Community 75 - "ToolError"
Cohesion: 0.11
Nodes (36): _ActionNotResolved, confirmed_login_otp_nodes(), continue_number(), country(), finish_auto(), finish_create(), finish_login(), focus_otp() (+28 more)

### Community 76 - "retry_preparation"
Cohesion: 0.15
Nodes (4): emit(), _phone_preparation_lock(), retry_preparation(), P03 — Mở form New Profile

### Community 77 - "Bàn giao dừng theo yêu cầu người dùng — 13/11/2026"
Cohesion: 0.25
Nodes (7): Bàn giao dừng theo yêu cầu người dùng — 13/11/2026, Bằng chứng trực tiếp đã có, Bối cảnh đã hoàn tất trước lỗi hiện tại, Cách tiếp tục, Kiểm chứng gần nhất, Lỗi chính chưa xử lý xong, Yêu cầu mới nhất

### Community 81 - "action"
Cohesion: 0.39
Nodes (8): open_menu(), read_menu(), return_to_menu(), view(), visit(), action(), visit_seconds(), Tự động chuyển bước sau 60 giây nếu không thấy menu Browse ở b13–b15 — 19/11/2026

### Community 83 - "RunJob"
Cohesion: 0.14
Nodes (5): _automatic_resume_slots(), AccountData, RunJob, DesktopResumeTests, Q2FlowTests

### Community 84 - "OTP_DESIGN.md"
Cohesion: 0.50
Nodes (3): Nối vào bước tạo tài khoản sau khi xác minh màn hình Amazon, Thiết kế OTP cho từng Profile, Đã chuẩn bị

### Community 86 - "_tail_menu"
Cohesion: 0.12
Nodes (10): build_marketplace_steps(), build_post_auth_steps(), _tail_menu(), Nhận diện giao diện lúc chạy, Nhập liệu và lỗi, Quy tắc tự động hóa sau menu ba gạch, Trạng thái hiện tại của dự án, Từng máy độc lập (+2 more)

### Community 87 - "build_random_steps"
Cohesion: 0.11
Nodes (12): scroll_view(), wait_until(), finish_view(), build_random_steps(), browse_view(), finish_view(), Một quy luật để sửa mã về sau — 20/11/2026, Cách thử bản pilot cũ (không áp dụng cho factory hiện hành) (+4 more)

### Community 89 - "001 — Tách dữ liệu từng mẻ và đối chiếu số hàng"
Cohesion: 0.29
Nodes (7): 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Rủi ro và bảo trì, Thiết kế yêu cầu, Điều kiện dừng

### Community 92 - "GRAPH_AUDIT.md"
Cohesion: 0.67
Nodes (3): Cách kiểm tra sau mỗi sửa đổi, Giới hạn đã xác nhận, Kiểm tra độ phủ Graphify — cập nhật 26/11/2026

## Knowledge Gaps
- **1 isolated node(s):** `amazon-android-tool`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 536 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **22 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ToolError` connect `cli.py` to `registration.py`, `build_common_steps`, `otp.py`, `BulkInputTests`, `swarmote_desktop.py`, `RunnerTests`, `PostMenuStep`, `ToolError`, `AddressDetailTests`, `adb`, `StopResetTests`, `cloud.py`, `open_home_menu`, `MarketplaceFlowTests`, `marketplace_flow.py`, `_read_nodes`, `core.py`, `_find_scrolling`, `q7_state_machine.py`, `CloudPhone`, `amazon_is_foreground`, `Window`, `RegistrationState`, `build_random_steps`, `ui_backend.py`, `vision.py`, `settings.py`, `_visible`, `subprocess`, `._run`, `build_create_address_steps`, `q7_state_machine.py`, `_nodes`, `cloud_adb`, `swarmote_desktop.py`, `cli.py`, `_choose_tail_target`, `build_reload_payment_steps`, `CountryRecoveryTests`, `test_isolated_reader.py`, `BatchDraft`, `_prepare_phone`, `_tap_child`, `.test_b10_stalled_whatsapp_pauses_only_affected_phone`, `_restore_prefix_menu`, `._continue_profile`, `ProfilesNavigationTests`, `ToolError`, `retry_preparation`, `_ScreenWaitExpired`, `_scroll_up`, `action`, `_start_and_confirm`, `RunJob`, `ensure_manager_ready`, `_tail_menu`, `build_random_steps`, `.test_selected_stop_finishes_install_before_stopping_that_phone`, `.test_b11_taps_otp_field_even_when_provider_read_fails`?**
  _High betweenness centrality (0.380) - this node is a cross-community bridge._
- **Are the 58 inferred relationships involving `ToolError` (e.g. with `_read_nodes_once()` and `_resume_address_payment_index()`) actually correct?**
  _`ToolError` has 58 INFERRED edges - model-reasoned connections that need verification._
- **What connects `amazon-android-tool` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `build_common_steps` be split into smaller, more focused modules?**
  _Cohesion score 0.0880503144654088 - nodes in this community are weakly interconnected._
- **Why does `CloudPhone` connect `CloudPhone` to `registration.py`, `build_common_steps`, `swarmote_desktop.py`, `PostMenuStep`, `AddressDetailTests`, `adb`, `cloud.py`, `open_home_menu`, `MarketplaceFlowTests`, `_read_nodes`, `Q3Q4FlowTests`, `_find_scrolling`, `q7_state_machine.py`, `amazon_is_foreground`, `Window`, `RegistrationState`, `build_random_steps`, `ui_backend.py`, `subprocess`, `build_create_address_steps`, `cli.py`, `q7_state_machine.py`, `_nodes`, `cloud_adb`, `swarmote_desktop.py`, `cli.py`, `build_reload_payment_steps`, `CountryRecoveryTests`, `test_isolated_reader.py`, `_prepare_phone`, `_tap_child`, `.test_b10_stalled_whatsapp_pauses_only_affected_phone`, `ToolError`, `_scroll_up`, `RunJob`, `_tail_menu`, `build_random_steps`, `.test_manual_otp_repair_continues_with_confirmation_and_tail_for_both_modes`, `SharedFallbackTests`?**
  _High betweenness centrality (0.113) - this node is a cross-community bridge._
- **Are the 88 inferred relationships involving `CloudPhone` (e.g. with `build_common_steps()` and `_country_full_row()`) actually correct?**
  _`CloudPhone` has 88 INFERRED edges - model-reasoned connections that need verification._
- **Should `otp.py` be split into smaller, more focused modules?**
  _Cohesion score 0.09411764705882353 - nodes in this community are weakly interconnected._