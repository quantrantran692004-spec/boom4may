# Graph Report - boom4may  (2026-11-26)

## Corpus Check
- 134 files · ~163,816 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 1, .bat 1, .pyw 1)

## Summary
- 2160 nodes · 7528 edges · 88 communities (74 shown, 14 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 1074 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `6b0e2c5a`
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
- build_random_steps
- StopResetTests
- cli.py
- amazon-android-tool
- Ảnh hướng dẫn q1/q2 và menu chung lưu cục bộ
- MarketplaceFlowTests
- marketplace_flow.py
- _read_nodes
- MENU_ROUTING.md
- Q3Q4FlowTests
- _type_field
- ExtendedRecoveryTests
- Nghiên cứu và tích hợp Swarmote
- q7_state_machine.py
- account_flow.py
- amazon_is_foreground
- Window
- RegistrationState
- PROJECT_INDEX.md
- build_random_steps
- core.py
- vision.py
- build_q1_steps
- _visible
- time
- phone_window_layout.py
- build_create_address_steps
- main
- SafetyTests
- Bàn giao trạng thái dự án — 13/11/2026
- random_prefix.py
- FakeControl
- Bàn giao dừng theo yêu cầu người dùng — 13/11/2026
- ui_backend.py
- ToolError
- ProxyConfig
- swarmote_desktop.py
- ProfileManagerWindowError
- b1–b11 Reliability and Latency Implementation Plan
- .test_creation_session_runs_b11_confirmation_through_b15_on_all_twelve_slots
- Danh mục ảnh nằm trong dự án
- setup.py
- Amazon Android Tool — Giai đoạn A/B
- profile_status
- _CombinedStop
- Giao diện vận hành
- .remaining
- Amazon trên Swarmote
- CloudPhone
- build_reload_payment_steps
- Bộ cài chia sẻ Windows x64
- CountryRecoveryTests
- test_isolated_reader.py
- VERIFICATION.md
- AppSettings
- Biên bản kiểm tra thực tế — 2026-11-12
- run_batch
- q5_flow.py
- PROJECT_HANDOFF.md
- _find_scrolling
- BatchDraft
- ProfilesNavigationTests
- screen
- .__init__
- AccountData
- 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng
- Giai đoạn 2 — bản thử State Machine riêng q7
- .test_b10_stalled_whatsapp_pauses_only_affected_phone
- build_post_auth_steps
- _choose_tail_target
- GRAPH_AUDIT.md
- OTP_DESIGN.md
- .test_tail_waits_after_tap_then_scrolls_forward_once
- PreparationProgressTests

## God Nodes (most connected - your core abstractions)
1. `ToolError` - 352 edges
2. `CloudPhone` - 234 edges
3. `AttemptDeadline` - 198 edges
4. `RunJob` - 164 edges
5. `RegistrationState` - 158 edges
6. `build_common_steps()` - 115 edges
7. `Window` - 97 edges
8. `PostMenuStep` - 93 edges
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
- `Phạm vi q1–q12 sau phản hồi người dùng — 14/11/2026` --references--> `build_common_steps()`  [INFERRED]
  PROJECT_HANDOFF.md → amazon_android/account_flow.py

## Import Cycles
- None detected.

## Communities (88 total, 14 thin omitted)

### Community 0 - "registration.py"
Cohesion: 0.19
Nodes (12): require_online(), _field_for_label(), fill_identifier(), fill_signup_form(), _nodes(), open_entry(), status(), _tap() (+4 more)

### Community 1 - "build_common_steps"
Cohesion: 0.09
Nodes (4): build_common_steps(), node(), Q1FlowTests, provider_read()

### Community 2 - "otp.py"
Cohesion: 0.10
Nodes (8): browser_launch_options(), extract_otp(), _NoRedirect, read_otp(), _read_otp_in_browser(), wait_for_new_otp(), OtpTests, PackagedBrowserTests

### Community 3 - "BulkInputTests"
Cohesion: 0.06
Nodes (14): BulkRecord, lines(), parse_bulk_payload(), parse_column(), parse_records(), _proxy_rows(), _table_cells(), _url_from_cell() (+6 more)

### Community 4 - "windows_identity.py"
Cohesion: 0.27
Nodes (6): create_shortcut(), relaunch_command(), runtime(), set_process_identity(), set_window_identity(), WindowsIdentityTests

### Community 5 - "swarmote_desktop.py"
Cohesion: 0.11
Nodes (22): ready_for_home_menu(), _check_stop(), collapse_apps_panel(), install_amazon(), check_stop(), open_adb_shell(), _pause(), _phone_window() (+14 more)

### Community 6 - "RunnerTests"
Cohesion: 0.06
Nodes (18): ProfileRegistry, absent(), ProfileRegistryTests, lookup(), broken(), RunnerTests, create(), resume() (+10 more)

### Community 7 - "PostMenuStep"
Cohesion: 0.08
Nodes (15): PostMenuSession, PostMenuStep, Một quy luật để sửa mã về sau — 20/11/2026, PostMenuTests, first_step(), reconcile(), first(), ResumeRegistrationStateTests (+7 more)

### Community 8 - "ToolError"
Cohesion: 0.08
Nodes (16): _main_window(), collect(), ProfileStartNotSubmitted, _select_profile_rows(), _selected_profile_names(), start_profile(), start_profiles_together(), _wait_for_selected() (+8 more)

### Community 9 - "AddressDetailTests"
Cohesion: 0.10
Nodes (9): build_create_address_detail_steps(), _new_prefix(), Tăng số lần thử đọc cây Android và bổ sung phương án dự phòng cho b23–b31 — 19/11/2026, AddressDetailTests, read(), adb(), tap(), read() (+1 more)

### Community 10 - "003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật"
Cohesion: 0.06
Nodes (26): 002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Rủi ro và bảo trì, Điều kiện dừng, 003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật, Các bước (+18 more)

### Community 11 - "Danh mục từng bước đã biết — 13/11/2026"
Cohesion: 0.05
Nodes (37): B1–B3 hiện hành — Ba lượt ngẫu nhiên q1–q12, Bản thử q7 State Machine — 14/11/2026, Chung b10 — Chuyển WhatsApp sang SMS, Chung b11 — Lấy và gõ OTP SMS, Chung b11a — Chạm ô OTP trên màn SMS, Chung b11b — Xác minh đăng nhập hoặc bấm Create của luồng tạo, Chung b4 — Sign In từ menu, Chung b4a — Chạm ô SĐT (+29 more)

### Community 12 - "build_random_steps"
Cohesion: 0.08
Nodes (7): build_random_steps(), finish_view(), B1–b3 xem menu ngẫu nhiên cho 12 máy — 14/11/2026, Q5FlowTests, adb(), adb(), adb()

### Community 13 - "StopResetTests"
Cohesion: 0.07
Nodes (4): emit(), retry_preparation(), StopResetTests, install()

### Community 14 - "cli.py"
Cohesion: 0.21
Nodes (9): main(), parser(), report(), open_amazon(), foreground(), get_device(), print_json(), Store (+1 more)

### Community 16 - "Ảnh hướng dẫn q1/q2 và menu chung lưu cục bộ"
Cohesion: 0.07
Nodes (29): 14 ảnh menu chung b1–b3 ngẫu nhiên — 14/11/2026, B16–b22 chung — Đổi marketplace sang United States (18/11/2026), B32–b39 — Reload Balance, thêm thẻ và địa chỉ thanh toán (21/11/2026), B6 — Hai ảnh đính kèm mới ngày 13/11/2026, Menu chung ảnh 01 — Danh sách chữ, Menu chung ảnh 02 — App Store bên phải sau khi Amazon mở, q1 b6 — US +1 hiện nhưng chạm không đóng hộp, 14/11/2026, q1 ảnh 01 — Menu và ba thẻ (+21 more)

### Community 18 - "MarketplaceFlowTests"
Cohesion: 0.07
Nodes (23): AttemptDeadline, MarketplaceFlowTests, read(), adb(), read(), tap(), read(), read() (+15 more)

### Community 19 - "marketplace_flow.py"
Cohesion: 0.17
Nodes (27): _account_tab(), build_marketplace_steps(), run(), account_target(), back_and_read_text(), foreground_ready(), recover_country_list(), _destination() (+19 more)

### Community 20 - "_read_nodes"
Cohesion: 0.13
Nodes (28): _at_or_after(), sign_in(), _ensure_menu(), home_visible(), menu_layout(), _read_nodes(), route_list_menu(), _tap() (+20 more)

### Community 21 - "MENU_ROUTING.md"
Cohesion: 0.23
Nodes (7): Bằng chứng và phạm vi, Kiểm chứng, Quy tắc chạy, Điều hướng hai dạng menu ba gạch, Luồng q1 từ menu ba gạch tới nhập OTP, Thử trên q1 đã có, Luồng q2 từ menu ba gạch

### Community 22 - "Q3Q4FlowTests"
Cohesion: 0.21
Nodes (3): build_q3_steps(), build_q4_steps(), Q3Q4FlowTests

### Community 23 - "_type_field"
Cohesion: 0.22
Nodes (3): _type_field(), FlowRecoveryTests, form()

### Community 24 - "ExtendedRecoveryTests"
Cohesion: 0.13
Nodes (7): MenuReadUnavailable, budget(), ExtendedRecoveryTests, fail(), read(), read(), menu()

### Community 25 - "Nghiên cứu và tích hợp Swarmote"
Cohesion: 0.40
Nodes (4): Hành vi có bằng chứng, Kiểm thử còn lại, Nghiên cứu và tích hợp Swarmote, Phần đã áp dụng

### Community 26 - "q7_state_machine.py"
Cohesion: 0.09
Nodes (14): _already_reached_result(), build_q7_pilot_steps(), _past_known_step(), ResultVerifier, StateDeadline, StateDetector, StateMachineStop, StateMachineTimeout (+6 more)

### Community 27 - "account_flow.py"
Cohesion: 0.12
Nodes (21): _ActionNotResolved, _country_nodes(), _CountryReadStop, _national_phone(), _parse_ui_nodes(), _read_hierarchy(), _read_login_sms_visual(), _read_nodes_once() (+13 more)

### Community 28 - "amazon_is_foreground"
Cohesion: 0.13
Nodes (6): amazon_is_foreground(), cloud_serials(), scan(), CloudBridgeTests, adb(), Ẩn cửa sổ cmd khi gọi ADB — 2026-11-13

### Community 30 - "RegistrationState"
Cohesion: 0.11
Nodes (3): RegistrationState, build_tail_steps(), RandomPrefixTests

### Community 31 - "PROJECT_INDEX.md"
Cohesion: 0.19
Nodes (6): Quy trình Swarmote hiện tại, Bản đồ repository, q3 — b1–b3 và nối luồng chung, q4 — Giỏ hàng, Pets, Home and DIY, q5 — ba thẻ riêng và b4–b11 chung, q6 — Trang chủ, Giỏ hàng, menu và một thẻ

### Community 32 - "build_random_steps"
Cohesion: 0.11
Nodes (4): RandomPrefixTests, adb(), adb(), adb()

### Community 33 - "core.py"
Cohesion: 0.28
Nodes (19): adb(), available_memory_mb(), check_play(), configure_avd(), connected_devices(), Device, device_avd_name(), device_resources() (+11 more)

### Community 34 - "vision.py"
Cohesion: 0.07
Nodes (19): _bounds(), _canonical_text(), _compact(), _engine(), _field_contents(), _field_is_blank(), _input_box(), _join_wrapped_categories() (+11 more)

### Community 36 - "_visible"
Cohesion: 0.15
Nodes (32): _bounds(), _text(), _visible(), _action(), _address_form(), _addresses(), _bounded_native(), run() (+24 more)

### Community 37 - "time"
Cohesion: 0.17
Nodes (12): main(), check_runtime(), main(), verify(), _app_installed(), _app_paths(), _check_external_apps(), _install_python_dependencies() (+4 more)

### Community 38 - "phone_window_layout.py"
Cohesion: 0.13
Nodes (5): arrange_on_open(), _row_if_fits(), _sort_key(), _tiles(), PhoneWindowLayoutTests

### Community 39 - "build_create_address_steps"
Cohesion: 0.24
Nodes (4): build_create_address_steps(), CreateAddressFlowTests, read(), node()

### Community 40 - "main"
Cohesion: 0.16
Nodes (9): main(), main(), Đợt tăng tốc và tự phục hồi b4–b11 ngày 13/11/2026, File dự án mà Graphify không phân tích trực tiếp, .gitignore, Launch Swarmote Tool.pyw, pyproject.toml, Ảnh PNG trong dự án (+1 more)

### Community 42 - "Bàn giao trạng thái dự án — 13/11/2026"
Cohesion: 0.12
Nodes (17): B6 danh sách quốc gia vẫn mở sau khi chọn — 13/11/2026, Bàn giao trạng thái dự án — 13/11/2026, Bản chính boom4may và bản dự phòng — 14/11/2026, Bộ cài offline chia sẻ — 14/11/2026, Cài đặt máy mới, Dừng riêng máy đang chọn — 14/11/2026, Mã hiện có, q3/q4 đã nối b1–b3 và thử đồng thời bốn luồng — 13/11/2026 (+9 more)

### Community 43 - "random_prefix.py"
Cohesion: 0.08
Nodes (31): scroll_view(), wait_until(), cloud_adb(), RecoverableStepError, build_random_steps(), browse(), action(), run_browse() (+23 more)

### Community 44 - "FakeControl"
Cohesion: 0.13
Nodes (5): ParallelInstallTests, PhoneWindow, FakeControl, InstallTests, descendants()

### Community 45 - "Bàn giao dừng theo yêu cầu người dùng — 13/11/2026"
Cohesion: 0.17
Nodes (10): _descendants(), inspect(), Bàn giao dừng theo yêu cầu người dùng — 13/11/2026, Bằng chứng trực tiếp đã có, Bối cảnh đã hoàn tất trước lỗi hiện tại, Cách tiếp tục, Kiểm chứng gần nhất, Lỗi chính chưa xử lý xong (+2 more)

### Community 46 - "ui_backend.py"
Cohesion: 0.14
Nodes (10): swarmote_tunnel_owner(), _connect(), country_reverse_points(), country_scroll(), _failed(), read_tree(), ready(), _session() (+2 more)

### Community 47 - "ToolError"
Cohesion: 0.14
Nodes (22): _keyboard_visible(), _scroll_up(), verify_menu_open(), swarmote_adb_path(), ToolError, _foreground(), open_menu(), read_menu() (+14 more)

### Community 48 - "ProxyConfig"
Cohesion: 0.18
Nodes (7): BatchItem, parse_proxy_line(), prepare_five(), create_profile(), ProxyConfig, BatchSafetyTests, CreationWindowVisibilityTests

### Community 49 - "swarmote_desktop.py"
Cohesion: 0.14
Nodes (15): package_path(), _activate_manager(), _create_profile_form(), _invoke(), _one(), _profile_checkbox(), _profile_form_open(), _proxy_postal_prefix() (+7 more)

### Community 50 - "ProfileManagerWindowError"
Cohesion: 0.22
Nodes (5): ensure_manager_ready(), ProfileManagerWindowError, _swarmote_exe(), ManagerStartupTests, unavailable()

### Community 51 - "b1–b11 Reliability and Latency Implementation Plan"
Cohesion: 0.18
Nodes (10): b1–b11 Reliability and Latency Implementation Plan, Completion Criteria, File Map, Global Constraints, Review Focus, Task 1: Measure current step latency and classify existing failures, Task 2: Define safe retry, reconcile, pause, and stop behavior, Task 3: Reduce redundant UI reads and unnecessary waits (+2 more)

### Community 52 - ".test_creation_session_runs_b11_confirmation_through_b15_on_all_twelve_slots"
Cohesion: 0.14
Nodes (3): browse(), tap(), tap()

### Community 53 - "Danh mục ảnh nằm trong dự án"
Cohesion: 0.25
Nodes (8): amazon_android/assets/obsidian_prism.png, assets/ui_history/machine7_input_before.png, assets/ui_history/reset_check.png, assets/ui_history/ui-12.png, assets/ui_history/ui_palette_preview.png, assets/ui_history/ui-preview.png, assets/ui_history/ui-screenshot.png, Danh mục ảnh nằm trong dự án

### Community 54 - "setup.py"
Cohesion: 0.24
Nodes (12): app_data_dir(), avd_names(), create_avd(), doctor(), executable(), installed_image(), run(), sdk_root() (+4 more)

### Community 55 - "Amazon Android Tool — Giai đoạn A/B"
Cohesion: 0.29
Nodes (7): Amazon Android Tool — Giai đoạn A/B, Cài trên máy Windows mới, Dán nhiều proxy, Sử dụng, Trạng thái nghiệm thu, Yêu cầu, Điện thoại đám mây Swarmote

### Community 56 - "profile_status"
Cohesion: 0.13
Nodes (11): visible_lookup(), _start_and_confirm(), _profile_row_status(), profile_status(), ProfileLookupError, ProfileNotFound, Các bước, Thiết kế yêu cầu (+3 more)

### Community 58 - "Giao diện vận hành"
Cohesion: 0.40
Nodes (4): Bố cục, Giao diện vận hành, Hướng thị giác, Quy tắc

### Community 59 - ".remaining"
Cohesion: 0.16
Nodes (4): country(), _country_full_row(), _same_country_position(), _tail_menu()

### Community 60 - "Amazon trên Swarmote"
Cohesion: 0.33
Nodes (5): Amazon trên Swarmote, Người dùng và công việc, Nền tảng, Điều chưa xác minh, Định hướng ngôn ngữ nếu xây dựng lại — 23/11/2026

### Community 61 - "CloudPhone"
Cohesion: 0.08
Nodes (19): CloudPhone, probe(), prop(), reported_installer(), reconcile(), route(), _confirm_menu_fallback(), _menu_evidence() (+11 more)

### Community 62 - "build_reload_payment_steps"
Cohesion: 0.13
Nodes (9): build_reload_payment_steps(), node(), ReloadPaymentTests, adb(), wait(), read(), read(), read() (+1 more)

### Community 63 - "Bộ cài chia sẻ Windows x64"
Cohesion: 0.50
Nodes (3): Bộ cài chia sẻ Windows x64, Dựng lại, Nguồn thành phần

### Community 64 - "CountryRecoveryTests"
Cohesion: 0.27
Nodes (4): CountryRecoveryTests, read(), wait(), node()

### Community 65 - "test_isolated_reader.py"
Cohesion: 0.20
Nodes (8): phone_reader(), PhoneReader, ReaderResponseError, _serve(), fake_worker(), IsolationTests, duplicate(), production_worker_with_fake_android()

### Community 66 - "VERIFICATION.md"
Cohesion: 0.17
Nodes (10): Kết luận và tích hợp, Kết quả thực tế, So sánh bộ đọc trên q1 — 13/11/2026, Thành phần thiết bị, b1–b3 bắt buộc có ba cú bấm — 14/11/2026, b1–b3 ngẫu nhiên cho 12 máy — 14/11/2026, b1–b3 ngẫu nhiên trên 12 máy, không dùng OCR — 14/11/2026, b6 cuộn tới đáy rồi vuốt ngược — 14/11/2026 (+2 more)

### Community 67 - "AppSettings"
Cohesion: 0.15
Nodes (7): save(), default_path(), AppSettings, load_settings(), save_settings(), settings_path(), SettingsTests

### Community 68 - "Biên bản kiểm tra thực tế — 2026-11-12"
Cohesion: 0.08
Nodes (24): b6 Country US +1 — 14/11/2026, B6 cuộn quốc gia và chọn lại — 13/11/2026, Biên bản kiểm tra thực tế — 2026-11-12, Cài và đo UiAutomator2 theo phê duyệt mới — 13/11/2026, Dừng riêng một máy — 14/11/2026, Focus ô nhập b4–b11 — 14/11/2026, Ghim taskbar — 13/11/2026, Giao diện sáng, dễ đọc — 2026-11-13 (+16 more)

### Community 69 - "run_batch"
Cohesion: 0.18
Nodes (12): _phone_preparation_lock(), _prepare_phone(), _prepare_phone_locked(), progress(), stop_here(), run_batch(), fill_slots(), manually_selected() (+4 more)

### Community 71 - "PROJECT_HANDOFF.md"
Cohesion: 0.11
Nodes (17): b1–b3 ngẫu nhiên cho q1–q12 — 14/11/2026, B4–b11 chạy đồng thời và OCR — 14/11/2026, b6 US +1 còn mở sau bốn cú chạm — 14/11/2026, Bản thử State Machine q7 và b1–b3 mở mục con — 14/11/2026, Bỏ thời hạn tổng sau menu — 14/11/2026, Bổ sung đọc ảnh OCR và chạm trực tiếp dự phòng cho b26 khi uiautomator dump WebView lỗi — 19/11/2026, Cơ chế chụp ảnh OCR quét chữ ấn luôn cho toàn bộ b26–b31 — 19/11/2026, Dán bảng Amazon có ghi chú thẻ live và URL OTP escaped — 14/11/2026 (+9 more)

### Community 74 - "ProfilesNavigationTests"
Cohesion: 0.13
Nodes (9): _open_profiles(), ProfileCreateNotSubmitted, visible_profile_names(), control(), ProfilesNavigationTests, descendants(), invoke(), descendants() (+1 more)

### Community 75 - "screen"
Cohesion: 0.16
Nodes (25): confirmed_login_otp_nodes(), continue_number(), enter_otp(), finish_auto(), finish_create(), finish_login(), focus_otp(), focus_phone() (+17 more)

### Community 77 - "AccountData"
Cohesion: 0.10
Nodes (11): _automatic_resume_slots(), ActionValidator, AccountData, RunJob, DesktopResumeTests, apartment_type(), PreparationThreadsTests, run() (+3 more)

### Community 78 - "001 — Tách dữ liệu từng mẻ và đối chiếu số hàng"
Cohesion: 0.29
Nodes (7): 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Rủi ro và bảo trì, Thiết kế yêu cầu, Điều kiện dừng

### Community 79 - "Giai đoạn 2 — bản thử State Machine riêng q7"
Cohesion: 0.40
Nodes (5): Cách thử bản pilot cũ (không áp dụng cho factory hiện hành), Giai đoạn 2 — bản thử State Machine riêng q7, Giới hạn, Phạm vi và quan hệ với luồng cũ, Sơ đồ

### Community 81 - "build_post_auth_steps"
Cohesion: 0.25
Nodes (8): Hướng dẫn khi tiếp tục dự án, build_post_auth_steps(), Nhận diện giao diện lúc chạy, Nhập liệu và lỗi, Quy tắc tự động hóa sau menu ba gạch, Trạng thái hiện tại của dự án, Từng máy độc lập, Tự phục hồi và đọc WebView — 13/11/2026

### Community 82 - "_choose_tail_target"
Cohesion: 0.33
Nodes (3): _choose_tail_target(), choose(), choose()

### Community 83 - "GRAPH_AUDIT.md"
Cohesion: 0.50
Nodes (3): Cách kiểm tra sau mỗi sửa đổi, Giới hạn đã xác nhận, Kiểm tra độ phủ Graphify — 13/11/2026

### Community 84 - "OTP_DESIGN.md"
Cohesion: 0.50
Nodes (3): Nối vào bước tạo tài khoản sau khi xác minh màn hình Amazon, Thiết kế OTP cho từng Profile, Đã chuẩn bị

## Knowledge Gaps
- **1 isolated node(s):** `amazon-android-tool`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 532 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **14 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ToolError` connect `ToolError` to `registration.py`, `build_common_steps`, `otp.py`, `BulkInputTests`, `swarmote_desktop.py`, `RunnerTests`, `PostMenuStep`, `ToolError`, `AddressDetailTests`, `003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật`, `build_random_steps`, `StopResetTests`, `cli.py`, `core.py`, `MarketplaceFlowTests`, `marketplace_flow.py`, `_read_nodes`, `_type_field`, `ExtendedRecoveryTests`, `q7_state_machine.py`, `account_flow.py`, `amazon_is_foreground`, `Window`, `RegistrationState`, `build_random_steps`, `core.py`, `vision.py`, `build_q1_steps`, `_visible`, `build_create_address_steps`, `random_prefix.py`, `ui_backend.py`, `ProxyConfig`, `swarmote_desktop.py`, `ProfileManagerWindowError`, `setup.py`, `profile_status`, `.remaining`, `CloudPhone`, `build_reload_payment_steps`, `CountryRecoveryTests`, `test_isolated_reader.py`, `AppSettings`, `run_batch`, `_find_scrolling`, `BatchDraft`, `ProfilesNavigationTests`, `screen`, `AccountData`, `.test_b10_stalled_whatsapp_pauses_only_affected_phone`?**
  _High betweenness centrality (0.383) - this node is a cross-community bridge._
- **Are the 58 inferred relationships involving `ToolError` (e.g. with `_read_nodes_once()` and `_resume_address_payment_index()`) actually correct?**
  _`ToolError` has 58 INFERRED edges - model-reasoned connections that need verification._
- **What connects `amazon-android-tool` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `build_common_steps` be split into smaller, more focused modules?**
  _Cohesion score 0.08956228956228957 - nodes in this community are weakly interconnected._
- **Why does `CloudPhone` connect `CloudPhone` to `registration.py`, `build_common_steps`, `swarmote_desktop.py`, `PostMenuStep`, `AddressDetailTests`, `build_random_steps`, `cli.py`, `core.py`, `MarketplaceFlowTests`, `_read_nodes`, `Q3Q4FlowTests`, `_type_field`, `ExtendedRecoveryTests`, `q7_state_machine.py`, `account_flow.py`, `amazon_is_foreground`, `Window`, `RegistrationState`, `build_random_steps`, `build_q1_steps`, `build_create_address_steps`, `random_prefix.py`, `ui_backend.py`, `ToolError`, `swarmote_desktop.py`, `.test_creation_session_runs_b11_confirmation_through_b15_on_all_twelve_slots`, `profile_status`, `.remaining`, `build_reload_payment_steps`, `CountryRecoveryTests`, `test_isolated_reader.py`, `AppSettings`, `run_batch`, `q5_flow.py`, `_find_scrolling`, `screen`, `AccountData`, `.test_b10_stalled_whatsapp_pauses_only_affected_phone`, `build_post_auth_steps`, `.test_manual_otp_repair_continues_with_confirmation_and_tail_for_both_modes`?**
  _High betweenness centrality (0.111) - this node is a cross-community bridge._
- **Are the 88 inferred relationships involving `CloudPhone` (e.g. with `build_common_steps()` and `_country_full_row()`) actually correct?**
  _`CloudPhone` has 88 INFERRED edges - model-reasoned connections that need verification._
- **Should `otp.py` be split into smaller, more focused modules?**
  _Cohesion score 0.10114942528735632 - nodes in this community are weakly interconnected._