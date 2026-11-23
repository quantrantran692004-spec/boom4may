# Graph Report - boom4may  (2026-11-23)

## Corpus Check
- 131 files · ~156,414 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 1, .bat 1, .pyw 1)

## Summary
- 2080 nodes · 7326 edges · 99 communities (75 shown, 24 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 1038 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `0d7c7e79`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- registration.py
- build_common_steps
- otp.py
- BulkInputTests
- _yellow_form_button
- swarmote_desktop.py
- RunnerTests
- PostMenuSession
- ToolError
- AddressDetailTests
- 003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật
- Danh mục từng bước đã biết — 13/11/2026
- run_batch
- StopResetTests
- desktop.py
- amazon-android-tool
- Ảnh hướng dẫn q1/q2 và menu chung lưu cục bộ
- core.py
- MarketplaceFlowTests
- marketplace_flow.py
- screen
- Điều hướng hai dạng menu ba gạch
- _restore_prefix_menu
- threading
- PreparationThreadsTests
- Nghiên cứu và tích hợp Swarmote
- Q7StateMachineTests
- build_post_auth_steps
- vision.py
- ._refresh_devices
- RegistrationState
- PROJECT_INDEX.md
- subprocess
- resume_common_index
- cli.py
- CloudPhone
- create_address_detail_flow.py
- _tap_child
- ._build_main
- build_create_address_steps
- Q3Q4FlowTests
- start_device
- Bàn giao trạng thái dự án — 13/11/2026
- .test_b10_stalled_whatsapp_pauses_only_affected_phone
- FakeControl
- build_random_steps
- ui_backend.py
- q7_state_machine.py
- PhoneReader
- ProfileManagerWindowError
- AppSettings
- b1–b11 Reliability and Latency Implementation Plan
- validate_otp_url
- Danh mục ảnh nằm trong dự án
- ExtendedRecoveryTests
- Amazon Android Tool — Giai đoạn A/B
- CountryRecoveryTests
- ToolError
- Giao diện vận hành
- reload_payment_flow.py
- Amazon trên Swarmote
- amazon_is_foreground
- AccountData
- Bộ cài chia sẻ Windows x64
- .test_creation_session_runs_b11_confirmation_through_b15_on_all_twelve_slots
- windows_identity.py
- VERIFICATION.md
- _CombinedStop
- Biên bản kiểm tra thực tế — 2026-11-12
- Bàn giao dừng theo yêu cầu người dùng — 13/11/2026
- ._accept_proxy_text
- PROJECT_HANDOFF.md
- _proxy_postal_prefix
- BatchDraft
- ProfilesNavigationTests
- json
- doctor
- File dự án mà Graphify không phân tích trực tiếp
- profile_status
- _tail_menu
- PLAN.md
- GRAPH_AUDIT.md
- Giai đoạn 2 — bản thử State Machine riêng q7
- build_q1_steps
- OTP_DESIGN.md
- Luồng q1 từ menu ba gạch tới nhập OTP
- batch.py
- _tail_candidates
- SafetyTests
- _choose_tail_target
- _ScreenWaitExpired
- build_q5_steps
- Value
- _bounded_native
- Q5_FLOW.md
- PreparationProgressTests
- .test_b11_taps_otp_field_even_when_provider_read_fails

## God Nodes (most connected - your core abstractions)
1. `ToolError` - 347 edges
2. `CloudPhone` - 229 edges
3. `AttemptDeadline` - 195 edges
4. `RunJob` - 161 edges
5. `RegistrationState` - 146 edges
6. `build_common_steps()` - 113 edges
7. `Window` - 97 edges
8. `Q1FlowTests` - 91 edges
9. `PostMenuStep` - 88 edges
10. `PostMenuSession` - 79 edges

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

## Communities (99 total, 24 thin omitted)

### Community 0 - "registration.py"
Cohesion: 0.21
Nodes (11): _field_for_label(), fill_identifier(), fill_signup_form(), _nodes(), open_entry(), status(), _tap(), _type_into() (+3 more)

### Community 1 - "build_common_steps"
Cohesion: 0.07
Nodes (3): build_common_steps(), node(), Q1FlowTests

### Community 2 - "otp.py"
Cohesion: 0.10
Nodes (8): browser_launch_options(), extract_otp(), _NoRedirect, read_otp(), _read_otp_in_browser(), wait_for_new_otp(), OtpTests, PackagedBrowserTests

### Community 3 - "BulkInputTests"
Cohesion: 0.08
Nodes (8): lines(), parse_column(), parse_records(), _proxy_rows(), _url_from_cell(), validate_card(), Dán nhiều proxy cách nhau bằng dấu cách — 14/11/2026, BulkInputTests

### Community 5 - "swarmote_desktop.py"
Cohesion: 0.12
Nodes (20): ready_for_home_menu(), _check_stop(), collapse_apps_panel(), install_amazon(), open_adb_shell(), _pause(), _phone_window(), _progress_reporter() (+12 more)

### Community 6 - "RunnerTests"
Cohesion: 0.06
Nodes (19): ProfileRegistry, ProfileNotFound, absent(), ProfileRegistryTests, lookup(), broken(), RunnerTests, create() (+11 more)

### Community 7 - "PostMenuSession"
Cohesion: 0.11
Nodes (11): PostMenuSession, PostMenuStep, _first_point(), _first_point(), RunJob, PostMenuTests, reconcile(), first() (+3 more)

### Community 8 - "ToolError"
Cohesion: 0.08
Nodes (17): _one(), _profile_checkbox(), ProfileStartNotSubmitted, _select_profile_rows(), _select_radio(), _selected_profile_names(), _set_value(), start_profile() (+9 more)

### Community 9 - "AddressDetailTests"
Cohesion: 0.13
Nodes (7): build_create_address_detail_steps(), AddressDetailTests, read(), adb(), tap(), read(), item()

### Community 10 - "003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật"
Cohesion: 0.08
Nodes (20): 003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật, Các bước, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Quy trình đích, Rủi ro và bảo trì, Điều kiện dừng (+12 more)

### Community 11 - "Danh mục từng bước đã biết — 13/11/2026"
Cohesion: 0.06
Nodes (35): Bản thử q7 State Machine — 14/11/2026, Chung b10 — Chuyển WhatsApp sang SMS, Chung b11 — Lấy và gõ OTP SMS, Chung b11a — Chạm ô OTP trên màn SMS, Chung b11b — Xác minh đăng nhập hoặc bấm Create của luồng tạo, Chung b4 — Sign In từ menu, Chung b4a — Chạm ô SĐT, Chung b5 — Gõ số điện thoại (+27 more)

### Community 12 - "run_batch"
Cohesion: 0.11
Nodes (14): _phone_preparation_lock(), _prepare_phone(), _prepare_phone_locked(), progress(), retry_preparation(), run_batch(), fill_slots(), refresh_slots() (+6 more)

### Community 14 - "desktop.py"
Cohesion: 0.16
Nodes (5): verify_menu_open(), BulkRecord, parse_bulk_payload(), _table_cells(), ProxyConfig

### Community 16 - "Ảnh hướng dẫn q1/q2 và menu chung lưu cục bộ"
Cohesion: 0.07
Nodes (28): B16–b22 chung — Đổi marketplace sang United States (18/11/2026), B32–b39 — Reload Balance, thêm thẻ và địa chỉ thanh toán (21/11/2026), B6 — Hai ảnh đính kèm mới ngày 13/11/2026, Menu chung ảnh 01 — Danh sách chữ, Menu chung ảnh 02 — App Store bên phải sau khi Amazon mở, q1 b6 — US +1 hiện nhưng chạm không đóng hộp, 14/11/2026, q1 ảnh 01 — Menu và ba thẻ, q1 ảnh 02 — Sign In cuối menu (+20 more)

### Community 18 - "MarketplaceFlowTests"
Cohesion: 0.07
Nodes (22): AttemptDeadline, MarketplaceFlowTests, read(), adb(), read(), tap(), read(), read() (+14 more)

### Community 19 - "marketplace_flow.py"
Cohesion: 0.16
Nodes (29): _read_hierarchy(), cloud_adb(), foreground(), _account_tab(), build_marketplace_steps(), run(), account_target(), back_and_read_text() (+21 more)

### Community 20 - "screen"
Cohesion: 0.05
Nodes (81): _at_or_after(), confirmed_login_otp_nodes(), continue_number(), country(), enter_otp(), finish_auto(), finish_create(), finish_login() (+73 more)

### Community 21 - "Điều hướng hai dạng menu ba gạch"
Cohesion: 0.50
Nodes (4): Bằng chứng và phạm vi, Kiểm chứng, Quy tắc chạy, Điều hướng hai dạng menu ba gạch

### Community 22 - "_restore_prefix_menu"
Cohesion: 0.22
Nodes (4): sign_in(), _menu(), _PrefixRecoveryStop, _restore_prefix_menu()

### Community 23 - "threading"
Cohesion: 0.13
Nodes (6): _national_phone(), _parse_ui_nodes(), route_list_menu(), _UiReadIncomplete, reported_installer(), _tail_input_action()

### Community 24 - "PreparationThreadsTests"
Cohesion: 0.29
Nodes (4): apartment_type(), PreparationThreadsTests, run(), install()

### Community 25 - "Nghiên cứu và tích hợp Swarmote"
Cohesion: 0.40
Nodes (4): Hành vi có bằng chứng, Kiểm thử còn lại, Nghiên cứu và tích hợp Swarmote, Phần đã áp dụng

### Community 26 - "Q7StateMachineTests"
Cohesion: 0.06
Nodes (25): build_random_steps(), browse(), action(), run_browse(), sign_in(), _menu(), PrefixDeadline, Q7PrefixTimeout (+17 more)

### Community 27 - "build_post_auth_steps"
Cohesion: 0.22
Nodes (9): Hướng dẫn khi tiếp tục dự án, build_post_auth_steps(), Nhận diện giao diện lúc chạy, Nhập liệu và lỗi, Quy tắc tự động hóa sau menu ba gạch, Trạng thái hiện tại của dự án, Từng máy độc lập, Một quy luật để sửa mã về sau — 20/11/2026 (+1 more)

### Community 28 - "vision.py"
Cohesion: 0.07
Nodes (19): _bounds(), _canonical_text(), _compact(), _engine(), _field_contents(), _field_is_blank(), _input_box(), _join_wrapped_categories() (+11 more)

### Community 30 - "RegistrationState"
Cohesion: 0.14
Nodes (5): RegistrationState, build_tail_steps(), open_menu(), view(), RandomPrefixTests

### Community 31 - "PROJECT_INDEX.md"
Cohesion: 0.22
Nodes (5): Bản đồ repository, Luồng q2 từ menu ba gạch, q3 — b1–b3 và nối luồng chung, q4 — Giỏ hàng, Pets, Home and DIY, q6 — Trang chủ, Giỏ hàng, menu và một thẻ

### Community 32 - "subprocess"
Cohesion: 0.18
Nodes (8): confirm(), download_commandline_tools(), official_commandline_archive(), setup_sdk(), main(), check_runtime(), main(), verify()

### Community 33 - "resume_common_index"
Cohesion: 0.13
Nodes (5): resume_common_index(), Dự phòng dùng chung khi chạy song song — 14/11/2026, ResumeRegistrationStateTests, factory(), factory()

### Community 34 - "cli.py"
Cohesion: 0.25
Nodes (7): main(), parser(), report(), scan(), get_device(), print_json(), Store

### Community 35 - "CloudPhone"
Cohesion: 0.10
Nodes (13): CloudPhone, prop(), _nodes(), open_home_menu(), _tap(), type_characters(), HomeMenuTests, MenuReturnTests (+5 more)

### Community 36 - "create_address_detail_flow.py"
Cohesion: 0.17
Nodes (29): _bounds(), _button(), _text(), _visible(), _action(), _address_form(), _addresses(), run() (+21 more)

### Community 37 - "_tap_child"
Cohesion: 0.20
Nodes (3): _new_prefix(), _tap_child(), Tăng số lần thử đọc cây Android và bổ sung phương án dự phòng cho b23–b31 — 19/11/2026

### Community 39 - "build_create_address_steps"
Cohesion: 0.27
Nodes (4): build_create_address_steps(), CreateAddressFlowTests, read(), node()

### Community 40 - "Q3Q4FlowTests"
Cohesion: 0.23
Nodes (3): build_q3_steps(), build_q4_steps(), Q3Q4FlowTests

### Community 41 - "start_device"
Cohesion: 0.32
Nodes (18): adb(), available_memory_mb(), check_play(), connected_devices(), Device, device_avd_name(), device_resources(), emergency_stop() (+10 more)

### Community 42 - "Bàn giao trạng thái dự án — 13/11/2026"
Cohesion: 0.09
Nodes (21): main(), main(), B6 danh sách quốc gia vẫn mở sau khi chọn — 13/11/2026, Bàn giao trạng thái dự án — 13/11/2026, Bản chính boom4may và bản dự phòng — 14/11/2026, Bộ cài offline chia sẻ — 14/11/2026, Cài đặt máy mới, Dừng riêng máy đang chọn — 14/11/2026 (+13 more)

### Community 44 - "FakeControl"
Cohesion: 0.13
Nodes (5): ParallelInstallTests, PhoneWindow, FakeControl, InstallTests, descendants()

### Community 45 - "build_random_steps"
Cohesion: 0.14
Nodes (6): build_random_steps(), finish_view(), B1–b3 xem menu ngẫu nhiên cho 12 máy — 14/11/2026, adb(), adb(), adb()

### Community 46 - "ui_backend.py"
Cohesion: 0.13
Nodes (11): swarmote_adb_path(), swarmote_tunnel_owner(), _connect(), country_reverse_points(), country_scroll(), _failed(), read_tree(), ready() (+3 more)

### Community 47 - "q7_state_machine.py"
Cohesion: 0.23
Nodes (10): _ActionNotResolved, RecoverableStepError, ActionValidator, RecoveryHandler, TransitionManager, UnknownStateHandler, Bảng trạng thái, action() (+2 more)

### Community 48 - "PhoneReader"
Cohesion: 0.18
Nodes (8): reconcile(), route(), phone_reader(), PhoneReader, ReaderResponseError, fake_worker(), IsolationTests, duplicate()

### Community 49 - "ProfileManagerWindowError"
Cohesion: 0.21
Nodes (7): ensure_manager_ready(), _main_window(), collect(), ProfileManagerWindowError, _swarmote_exe(), ManagerStartupTests, unavailable()

### Community 50 - "AppSettings"
Cohesion: 0.26
Nodes (7): save(), default_path(), AppSettings, load_settings(), save_settings(), settings_path(), SettingsTests

### Community 51 - "b1–b11 Reliability and Latency Implementation Plan"
Cohesion: 0.18
Nodes (10): b1–b11 Reliability and Latency Implementation Plan, Completion Criteria, File Map, Global Constraints, Review Focus, Task 1: Measure current step latency and classify existing failures, Task 2: Define safe retry, reconcile, pause, and stop behavior, Task 3: Reduce redundant UI reads and unnecessary waits (+2 more)

### Community 53 - "Danh mục ảnh nằm trong dự án"
Cohesion: 0.25
Nodes (8): amazon_android/assets/obsidian_prism.png, assets/ui_history/machine7_input_before.png, assets/ui_history/reset_check.png, assets/ui_history/ui-12.png, assets/ui_history/ui_palette_preview.png, assets/ui_history/ui-preview.png, assets/ui_history/ui-screenshot.png, Danh mục ảnh nằm trong dự án

### Community 54 - "ExtendedRecoveryTests"
Cohesion: 0.15
Nodes (7): MenuReadUnavailable, budget(), ExtendedRecoveryTests, fail(), read(), read(), menu()

### Community 55 - "Amazon Android Tool — Giai đoạn A/B"
Cohesion: 0.29
Nodes (7): Amazon Android Tool — Giai đoạn A/B, Cài trên máy Windows mới, Dán nhiều proxy, Sử dụng, Trạng thái nghiệm thu, Yêu cầu, Điện thoại đám mây Swarmote

### Community 56 - "CountryRecoveryTests"
Cohesion: 0.22
Nodes (5): _same_country_position(), CountryRecoveryTests, read(), wait(), node()

### Community 57 - "ToolError"
Cohesion: 0.10
Nodes (14): open_amazon(), package_path(), probe(), require_online(), ToolError, _confirm_menu_fallback(), _menu_evidence(), _start_and_confirm() (+6 more)

### Community 58 - "Giao diện vận hành"
Cohesion: 0.40
Nodes (4): Bố cục, Giao diện vận hành, Hướng thị giác, Quy tắc

### Community 59 - "reload_payment_flow.py"
Cohesion: 0.24
Nodes (13): _scroll(), current(), _foreground(), _read(), _read_text_region(), step(), _card_parts(), _field_target() (+5 more)

### Community 60 - "Amazon trên Swarmote"
Cohesion: 0.33
Nodes (5): Amazon trên Swarmote, Người dùng và công việc, Nền tảng, Điều chưa xác minh, Định hướng ngôn ngữ nếu xây dựng lại — 23/11/2026

### Community 61 - "amazon_is_foreground"
Cohesion: 0.14
Nodes (5): amazon_is_foreground(), cloud_serials(), CloudBridgeTests, adb(), Ẩn cửa sổ cmd khi gọi ADB — 2026-11-13

### Community 62 - "AccountData"
Cohesion: 0.07
Nodes (13): _automatic_resume_slots(), build_reload_payment_steps(), AccountData, DesktopResumeTests, Q2FlowTests, node(), ReloadPaymentTests, adb() (+5 more)

### Community 63 - "Bộ cài chia sẻ Windows x64"
Cohesion: 0.50
Nodes (3): Bộ cài chia sẻ Windows x64, Dựng lại, Nguồn thành phần

### Community 65 - "windows_identity.py"
Cohesion: 0.27
Nodes (6): create_shortcut(), relaunch_command(), runtime(), set_process_identity(), set_window_identity(), WindowsIdentityTests

### Community 66 - "VERIFICATION.md"
Cohesion: 0.17
Nodes (10): Kết luận và tích hợp, Kết quả thực tế, So sánh bộ đọc trên q1 — 13/11/2026, Thành phần thiết bị, b1–b3 bắt buộc có ba cú bấm — 14/11/2026, b1–b3 ngẫu nhiên cho 12 máy — 14/11/2026, b1–b3 ngẫu nhiên trên 12 máy, không dùng OCR — 14/11/2026, b6 cuộn tới đáy rồi vuốt ngược — 14/11/2026 (+2 more)

### Community 68 - "Biên bản kiểm tra thực tế — 2026-11-12"
Cohesion: 0.08
Nodes (25): b6 Country US +1 — 14/11/2026, B6 cuộn quốc gia và chọn lại — 13/11/2026, Biên bản kiểm tra thực tế — 2026-11-12, Cài và đo UiAutomator2 theo phê duyệt mới — 13/11/2026, Dừng riêng một máy — 14/11/2026, Focus ô nhập b4–b11 — 14/11/2026, Ghim taskbar — 13/11/2026, Giao diện sáng, dễ đọc — 2026-11-13 (+17 more)

### Community 69 - "Bàn giao dừng theo yêu cầu người dùng — 13/11/2026"
Cohesion: 0.17
Nodes (10): _descendants(), inspect(), Bàn giao dừng theo yêu cầu người dùng — 13/11/2026, Bằng chứng trực tiếp đã có, Bối cảnh đã hoàn tất trước lỗi hiện tại, Cách tiếp tục, Kiểm chứng gần nhất, Lỗi chính chưa xử lý xong (+2 more)

### Community 71 - "PROJECT_HANDOFF.md"
Cohesion: 0.12
Nodes (16): b1–b3 ngẫu nhiên cho q1–q12 — 14/11/2026, B4–b11 chạy đồng thời và OCR — 14/11/2026, b6 US +1 còn mở sau bốn cú chạm — 14/11/2026, Bản thử State Machine q7 và b1–b3 mở mục con — 14/11/2026, Bỏ thời hạn tổng sau menu — 14/11/2026, Bổ sung đọc ảnh OCR và chạm trực tiếp dự phòng cho b26 khi uiautomator dump WebView lỗi — 19/11/2026, Cơ chế chụp ảnh OCR quét chữ ấn luôn cho toàn bộ b26–b31 — 19/11/2026, Dán bảng Amazon có ghi chú thẻ live và URL OTP escaped — 14/11/2026 (+8 more)

### Community 72 - "_proxy_postal_prefix"
Cohesion: 0.48
Nodes (3): _proxy_postal_prefix(), controls(), ProxyPostalPrefixTests

### Community 73 - "BatchDraft"
Cohesion: 0.12
Nodes (9): BatchDraft, 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Rủi ro và bảo trì, Thiết kế yêu cầu, Điều kiện dừng (+1 more)

### Community 74 - "ProfilesNavigationTests"
Cohesion: 0.10
Nodes (15): _activate_manager(), _create_profile_form(), _invoke(), _open_profiles(), _profile_form_open(), ProfileCreateNotSubmitted, ProxyTestFailed, visible_profile_names() (+7 more)

### Community 75 - "json"
Cohesion: 0.31
Nodes (8): _app_installed(), _app_paths(), _check_external_apps(), _install_python_dependencies(), main(), _offer_downloads(), _ready_file_matches(), _runtime_imports_work()

### Community 76 - "doctor"
Cohesion: 0.32
Nodes (9): app_data_dir(), avd_names(), configure_avd(), create_avd(), doctor(), executable(), installed_image(), run() (+1 more)

### Community 77 - "File dự án mà Graphify không phân tích trực tiếp"
Cohesion: 0.40
Nodes (5): File dự án mà Graphify không phân tích trực tiếp, .gitignore, Launch Swarmote Tool.pyw, pyproject.toml, Ảnh PNG trong dự án

### Community 78 - "profile_status"
Cohesion: 0.11
Nodes (13): emit(), visible_lookup(), _profile_row_status(), profile_status(), ProfileLookupError, _unfiltered_single_page(), 002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ, Các bước (+5 more)

### Community 79 - "_tail_menu"
Cohesion: 0.17
Nodes (4): browse(), _tail_menu(), Chung b12–b15 — Mở ba gạch rồi ba lượt điều hướng ngẫu nhiên, tap()

### Community 81 - "GRAPH_AUDIT.md"
Cohesion: 0.67
Nodes (3): Cách kiểm tra sau mỗi sửa đổi, Giới hạn đã xác nhận, Kiểm tra độ phủ Graphify — 13/11/2026

### Community 82 - "Giai đoạn 2 — bản thử State Machine riêng q7"
Cohesion: 0.40
Nodes (5): Cách thử thật q7 sau khi người dùng sẵn sàng, Giai đoạn 2 — bản thử State Machine riêng q7, Giới hạn, Phạm vi và quan hệ với luồng cũ, Sơ đồ

### Community 84 - "OTP_DESIGN.md"
Cohesion: 0.50
Nodes (3): Nối vào bước tạo tài khoản sau khi xác minh màn hình Amazon, Thiết kế OTP cho từng Profile, Đã chuẩn bị

### Community 86 - "batch.py"
Cohesion: 0.40
Nodes (4): BatchItem, parse_proxy_line(), prepare_five(), BatchSafetyTests

### Community 88 - "_tail_candidates"
Cohesion: 0.20
Nodes (3): _browse_ready_after_sms(), _tail_candidates(), _tail_safe_page_choices()

### Community 90 - "_choose_tail_target"
Cohesion: 0.25
Nodes (4): _choose_tail_target(), _TailChoicesExhausted, choose(), choose()

## Knowledge Gaps
- **1 isolated node(s):** `amazon-android-tool`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 501 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **24 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ToolError` connect `ToolError` to `registration.py`, `build_common_steps`, `otp.py`, `BulkInputTests`, `swarmote_desktop.py`, `RunnerTests`, `PostMenuSession`, `ToolError`, `AddressDetailTests`, `run_batch`, `StopResetTests`, `desktop.py`, `core.py`, `MarketplaceFlowTests`, `marketplace_flow.py`, `screen`, `_restore_prefix_menu`, `threading`, `Q7StateMachineTests`, `vision.py`, `._refresh_devices`, `RegistrationState`, `subprocess`, `resume_common_index`, `cli.py`, `CloudPhone`, `create_address_detail_flow.py`, `_tap_child`, `build_create_address_steps`, `start_device`, `.test_b10_stalled_whatsapp_pauses_only_affected_phone`, `build_random_steps`, `ui_backend.py`, `q7_state_machine.py`, `PhoneReader`, `ProfileManagerWindowError`, `AppSettings`, `validate_otp_url`, `ExtendedRecoveryTests`, `CountryRecoveryTests`, `reload_payment_flow.py`, `amazon_is_foreground`, `AccountData`, `._accept_proxy_text`, `BatchDraft`, `ProfilesNavigationTests`, `doctor`, `profile_status`, `_tail_menu`, `build_q1_steps`, `batch.py`, `_choose_tail_target`, `_ScreenWaitExpired`, `.test_b11_taps_otp_field_even_when_provider_read_fails`?**
  _High betweenness centrality (0.429) - this node is a cross-community bridge._
- **Are the 57 inferred relationships involving `ToolError` (e.g. with `_read_nodes_once()` and `resume_common_index()`) actually correct?**
  _`ToolError` has 57 INFERRED edges - model-reasoned connections that need verification._
- **What connects `amazon-android-tool` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `build_common_steps` be split into smaller, more focused modules?**
  _Cohesion score 0.07242063492063493 - nodes in this community are weakly interconnected._
- **Why does `CloudPhone` connect `CloudPhone` to `registration.py`, `build_common_steps`, `swarmote_desktop.py`, `PostMenuSession`, `ToolError`, `AddressDetailTests`, `run_batch`, `desktop.py`, `core.py`, `MarketplaceFlowTests`, `marketplace_flow.py`, `screen`, `_restore_prefix_menu`, `threading`, `Q7StateMachineTests`, `build_post_auth_steps`, `._refresh_devices`, `RegistrationState`, `resume_common_index`, `cli.py`, `_tap_child`, `build_create_address_steps`, `Q3Q4FlowTests`, `.test_b10_stalled_whatsapp_pauses_only_affected_phone`, `build_random_steps`, `ui_backend.py`, `q7_state_machine.py`, `PhoneReader`, `validate_otp_url`, `ExtendedRecoveryTests`, `CountryRecoveryTests`, `ToolError`, `amazon_is_foreground`, `AccountData`, `.test_creation_session_runs_b11_confirmation_through_b15_on_all_twelve_slots`, `profile_status`, `_tail_menu`, `build_q1_steps`, `.test_manual_otp_repair_continues_with_confirmation_and_tail_for_both_modes`, `build_q5_steps`?**
  _High betweenness centrality (0.098) - this node is a cross-community bridge._
- **Are the 88 inferred relationships involving `CloudPhone` (e.g. with `build_common_steps()` and `_country_full_row()`) actually correct?**
  _`CloudPhone` has 88 INFERRED edges - model-reasoned connections that need verification._
- **Should `otp.py` be split into smaller, more focused modules?**
  _Cohesion score 0.10114942528735632 - nodes in this community are weakly interconnected._