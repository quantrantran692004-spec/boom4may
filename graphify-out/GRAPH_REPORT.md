# Graph Report - boom4may  (2026-11-27)

## Corpus Check
- 136 files · ~173,509 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 2, .bat 1, .pyw 1)

## Summary
- 2237 nodes · 7773 edges · 102 communities (81 shown, 21 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 1125 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `6628da4e`
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
- amazon-android-tool
- Ảnh hướng dẫn q1/q2 và menu chung lưu cục bộ
- open_home_menu
- MarketplaceFlowTests
- marketplace_flow.py
- screen
- Điều hướng hai dạng menu ba gạch
- Q3Q4FlowTests
- core.py
- q7_state_machine.py
- Nghiên cứu và tích hợp Swarmote
- swarmote_desktop.py
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
- .remaining
- cli.py
- Bàn giao trạng thái dự án — 13/11/2026
- q7_random_prefix.py
- FakeControl
- desktop_theme.py
- pathlib
- cloud_adb
- phone_window_layout.py
- cli.py
- SafetyTests
- b1–b11 Reliability and Latency Implementation Plan
- VisionFieldTests
- Danh mục ảnh nằm trong dự án
- .test_b10_stalled_whatsapp_pauses_only_affected_phone
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
- ExtendedRecoveryTests
- PROJECT_HANDOFF.md
- _tail_menu
- ._continue_profile
- ProxyConfig
- account_flow.py
- _choose_tail_target
- _tail_candidates
- PLAN.md
- Luồng q1 từ menu ba gạch tới nhập OTP
- Q5_FLOW.md
- build_q1_steps
- ._run
- AccountData
- OTP_DESIGN.md
- ensure_manager_ready
- _restore_prefix_menu
- Giai đoạn 2 — bản thử State Machine riêng q7
- _prefix_nodes
- PreparationThreadsTests
- test_q5_flow.py
- _proxy_postal_prefix
- GRAPH_AUDIT.md
- File dự án mà Graphify không phân tích trực tiếp
- _country_nodes
- _ScreenWaitExpired
- _new_prefix
- ._run_post_menu
- MenuReturnTests
- .test_b11_taps_otp_field_even_when_provider_read_fails

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

## Communities (102 total, 21 thin omitted)

### Community 0 - "registration.py"
Cohesion: 0.21
Nodes (11): _field_for_label(), fill_identifier(), fill_signup_form(), _nodes(), open_entry(), status(), _tap(), _type_into() (+3 more)

### Community 1 - "build_common_steps"
Cohesion: 0.07
Nodes (3): build_common_steps(), node(), Q1FlowTests

### Community 2 - "otp.py"
Cohesion: 0.09
Nodes (9): lines(), _proxy_rows(), _table_cells(), extract_otp(), _NoRedirect, read_otp(), _read_otp_in_browser(), wait_for_new_otp() (+1 more)

### Community 3 - "BulkInputTests"
Cohesion: 0.07
Nodes (9): BulkRecord, parse_bulk_payload(), parse_column(), parse_records(), _url_from_cell(), validate_card(), Dán bảng Amazon có ghi chú thẻ live và URL OTP escaped — 14/11/2026, BulkInputTests (+1 more)

### Community 4 - "windows_identity.py"
Cohesion: 0.24
Nodes (5): create_shortcut(), relaunch_command(), runtime(), set_window_identity(), WindowsIdentityTests

### Community 5 - "swarmote_desktop.py"
Cohesion: 0.08
Nodes (32): package_path(), require_online(), _check_stop(), collapse_apps_panel(), _descendants(), install_amazon(), check_stop(), open_adb_shell() (+24 more)

### Community 6 - "RunnerTests"
Cohesion: 0.05
Nodes (21): default_path(), ProfileRegistry, ProfileNotFound, absent(), ProfileRegistryTests, lookup(), broken(), RunnerTests (+13 more)

### Community 7 - "PostMenuStep"
Cohesion: 0.08
Nodes (14): current(), PostMenuSession, PostMenuStep, RunJob, Một quy luật để sửa mã về sau — 20/11/2026, PostMenuTests, reconcile(), first() (+6 more)

### Community 8 - "ToolError"
Cohesion: 0.10
Nodes (8): ProfileStartNotSubmitted, start_profile(), BatchStartTests, checkbox(), toggle(), descendants(), FakeBox, FakeButton

### Community 9 - "AddressDetailTests"
Cohesion: 0.14
Nodes (7): build_create_address_detail_steps(), AddressDetailTests, read(), adb(), tap(), read(), item()

### Community 10 - "003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật"
Cohesion: 0.08
Nodes (20): 003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật, Các bước, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Quy trình đích, Rủi ro và bảo trì, Điều kiện dừng (+12 more)

### Community 11 - "Danh mục từng bước đã biết — 13/11/2026"
Cohesion: 0.06
Nodes (36): Bản thử q7 State Machine — 14/11/2026, Chung b10 — Chuyển WhatsApp sang SMS, Chung b11 — Lấy và gõ OTP SMS, Chung b11a — Chạm ô OTP trên màn SMS, Chung b11b — Xác minh đăng nhập hoặc bấm Create của luồng tạo, Chung b16–b22 — Tài khoản và marketplace United States, Chung b4 — Sign In từ menu, Chung b4a — Chạm ô SĐT (+28 more)

### Community 12 - "adb"
Cohesion: 0.12
Nodes (4): adb(), adb(), adb(), adb()

### Community 13 - "StopResetTests"
Cohesion: 0.07
Nodes (4): emit(), retry_preparation(), P03 — Mở form New Profile, StopResetTests

### Community 16 - "Ảnh hướng dẫn q1/q2 và menu chung lưu cục bộ"
Cohesion: 0.07
Nodes (28): B16–b22 chung — Đổi marketplace sang United States (18/11/2026), B32–b39 — Reload Balance, thêm thẻ và địa chỉ thanh toán (21/11/2026), B6 — Hai ảnh đính kèm mới ngày 13/11/2026, Menu chung ảnh 01 — Danh sách chữ, Menu chung ảnh 02 — App Store bên phải sau khi Amazon mở, q1 b6 — US +1 hiện nhưng chạm không đóng hộp, 14/11/2026, q1 ảnh 01 — Menu và ba thẻ, q1 ảnh 02 — Sign In cuối menu (+20 more)

### Community 17 - "open_home_menu"
Cohesion: 0.12
Nodes (11): _confirm_menu_fallback(), _menu_evidence(), MenuReadUnavailable, _nodes(), budget(), open_home_menu(), _tap(), HomeMenuTests (+3 more)

### Community 18 - "MarketplaceFlowTests"
Cohesion: 0.05
Nodes (28): AttemptDeadline, build_q7_pilot_steps(), ResultVerifier, StateDeadline, StateDetector, Bản thử State Machine q7 và b1–b3 mở mục con — 14/11/2026, MarketplaceFlowTests, read() (+20 more)

### Community 19 - "marketplace_flow.py"
Cohesion: 0.19
Nodes (25): _account_tab(), build_marketplace_steps(), run(), account_target(), back_and_read_text(), foreground_ready(), recover_country_list(), _destination() (+17 more)

### Community 20 - "screen"
Cohesion: 0.18
Nodes (26): _at_or_after(), sign_in(), _ensure_menu(), _find_scrolling(), home_visible(), menu_layout(), _read_nodes(), route_list_menu() (+18 more)

### Community 21 - "Điều hướng hai dạng menu ba gạch"
Cohesion: 0.50
Nodes (4): Bằng chứng và phạm vi, Kiểm chứng, Quy tắc chạy, Điều hướng hai dạng menu ba gạch

### Community 22 - "Q3Q4FlowTests"
Cohesion: 0.21
Nodes (3): build_q3_steps(), build_q4_steps(), Q3Q4FlowTests

### Community 23 - "core.py"
Cohesion: 0.22
Nodes (22): adb(), available_memory_mb(), avd_names(), check_play(), configure_avd(), connected_devices(), create_avd(), Device (+14 more)

### Community 24 - "q7_state_machine.py"
Cohesion: 0.10
Nodes (21): browse(), action(), run_browse(), sign_in(), _menu(), PrefixDeadline, Q7PrefixTimeout, _size() (+13 more)

### Community 25 - "Nghiên cứu và tích hợp Swarmote"
Cohesion: 0.40
Nodes (4): Hành vi có bằng chứng, Kiểm thử còn lại, Nghiên cứu và tích hợp Swarmote, Phần đã áp dụng

### Community 26 - "swarmote_desktop.py"
Cohesion: 0.11
Nodes (19): visible_lookup(), _activate_manager(), _invoke(), _one(), _profile_checkbox(), _profile_form_open(), _profile_row_status(), profile_status() (+11 more)

### Community 28 - "amazon_is_foreground"
Cohesion: 0.10
Nodes (12): amazon_is_foreground(), CloudPhone, open_amazon(), probe(), prop(), reported_installer(), ready_for_home_menu(), type_characters() (+4 more)

### Community 29 - "Window"
Cohesion: 0.10
Nodes (5): Window, set_process_identity(), Các bước, Trạng thái kiểm chứng và giới hạn, PreparationProgressTests

### Community 30 - "RegistrationState"
Cohesion: 0.13
Nodes (6): RegistrationState, build_tail_steps(), open_menu(), view(), visit_seconds(), RandomPrefixTests

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
Cohesion: 0.11
Nodes (10): _bounds(), _canonical_text(), _compact(), _field_contents(), _field_is_blank(), _join_wrapped_categories(), _normalize(), ocr_nodes() (+2 more)

### Community 35 - "subprocess"
Cohesion: 0.11
Nodes (17): main(), main(), main(), check_runtime(), main(), verify(), Đợt tăng tốc và tự phục hồi b4–b11 ngày 13/11/2026, _app_installed() (+9 more)

### Community 36 - "_visible"
Cohesion: 0.16
Nodes (29): _bounds(), _text(), _visible(), _action(), _address_form(), _addresses(), _bounded_native(), run() (+21 more)

### Community 37 - "setup.py"
Cohesion: 0.30
Nodes (9): app_data_dir(), doctor(), executable(), installed_image(), sdk_root(), confirm(), download_commandline_tools(), official_commandline_archive() (+1 more)

### Community 38 - "_type_field"
Cohesion: 0.17
Nodes (6): focus_phone(), _tap_input(), _type_field(), Phục hồi khi ô nhập chưa nhận focus ở b4–b11 — 14/11/2026, FlowRecoveryTests, form()

### Community 39 - "build_create_address_steps"
Cohesion: 0.24
Nodes (4): build_create_address_steps(), CreateAddressFlowTests, read(), node()

### Community 40 - ".remaining"
Cohesion: 0.13
Nodes (17): country(), _country_full_row(), _read_hierarchy(), _read_login_sms_visual(), _read_nodes_once(), _read_visual_nodes(), _same_country_position(), _scroll_up() (+9 more)

### Community 41 - "cli.py"
Cohesion: 0.13
Nodes (13): BatchItem, parse_proxy_line(), prepare_five(), ToolError, _start_and_confirm(), create_profile(), ready_for_registration(), Dán nhiều proxy cách nhau bằng dấu cách — 14/11/2026 (+5 more)

### Community 42 - "Bàn giao trạng thái dự án — 13/11/2026"
Cohesion: 0.10
Nodes (18): save(), set_tk_icon(), B6 danh sách quốc gia vẫn mở sau khi chọn — 13/11/2026, Bàn giao trạng thái dự án — 13/11/2026, Bản chính boom4may và bản dự phòng — 14/11/2026, Bộ cài offline chia sẻ — 14/11/2026, Cài đặt máy mới, Dừng riêng máy đang chọn — 14/11/2026 (+10 more)

### Community 43 - "q7_random_prefix.py"
Cohesion: 0.08
Nodes (18): Hướng dẫn khi tiếp tục dự án, scroll_view(), wait_until(), RecoverableStepError, build_random_steps(), finish_view(), _first_point(), build_post_auth_steps() (+10 more)

### Community 44 - "FakeControl"
Cohesion: 0.13
Nodes (5): ParallelInstallTests, PhoneWindow, FakeControl, InstallTests, descendants()

### Community 45 - "desktop_theme.py"
Cohesion: 0.07
Nodes (14): Button, Entry, FooterNote, icon(), startup_geometry(), state_style(), status_title(), StatusCell (+6 more)

### Community 46 - "pathlib"
Cohesion: 0.18
Nodes (6): browser_launch_options(), load_settings(), save_settings(), settings_path(), PackagedBrowserTests, SettingsTests

### Community 47 - "cloud_adb"
Cohesion: 0.17
Nodes (18): _keyboard_visible(), _resume_address_payment_index(), cloud_adb(), foreground(), _account_content(), run(), _foreground(), _read_text_region() (+10 more)

### Community 48 - "phone_window_layout.py"
Cohesion: 0.14
Nodes (5): arrange_on_open(), _row_if_fits(), _sort_key(), _tiles(), PhoneWindowLayoutTests

### Community 49 - "cli.py"
Cohesion: 0.22
Nodes (8): main(), parser(), report(), scan(), get_device(), print_json(), Store, inspect()

### Community 51 - "b1–b11 Reliability and Latency Implementation Plan"
Cohesion: 0.18
Nodes (10): b1–b11 Reliability and Latency Implementation Plan, Completion Criteria, File Map, Global Constraints, Review Focus, Task 1: Measure current step latency and classify existing failures, Task 2: Define safe retry, reconcile, pause, and stop behavior, Task 3: Reduce redundant UI reads and unnecessary waits (+2 more)

### Community 52 - "VisionFieldTests"
Cohesion: 0.24
Nodes (3): _input_box(), detection(), VisionFieldTests

### Community 53 - "Danh mục ảnh nằm trong dự án"
Cohesion: 0.18
Nodes (11): amazon_android/assets/icons/, amazon_android/assets/obsidian_prism.png, amazon_android/assets/swarmote_tool_square.png và swarmote_tool.ico, assets/ui_history/machine7_input_before.png, assets/ui_history/reset_check.png, assets/ui_history/ui-12.png, assets/ui_history/ui_palette_preview.png, assets/ui_history/ui-preview.png (+3 more)

### Community 55 - "Amazon Android Tool — Giai đoạn A/B"
Cohesion: 0.29
Nodes (7): Amazon Android Tool — Giai đoạn A/B, Cài trên máy Windows mới, Dán nhiều proxy, Sử dụng, Trạng thái nghiệm thu, Yêu cầu, Điện thoại đám mây Swarmote

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
Cohesion: 0.07
Nodes (27): cloud_serials(), b6 Country US +1 — 14/11/2026, B6 cuộn quốc gia và chọn lại — 13/11/2026, Biên bản kiểm tra thực tế — 2026-11-12, Cài và đo UiAutomator2 theo phê duyệt mới — 13/11/2026, Dừng riêng một máy — 14/11/2026, Focus ô nhập b4–b11 — 14/11/2026, Ghim taskbar — 13/11/2026 (+19 more)

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

### Community 67 - "BatchDraft"
Cohesion: 0.13
Nodes (9): BatchDraft, 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Rủi ro và bảo trì, Thiết kế yêu cầu, Điều kiện dừng (+1 more)

### Community 68 - "_prepare_phone"
Cohesion: 0.14
Nodes (14): _phone_preparation_lock(), _prepare_phone(), _prepare_phone_locked(), progress(), stop_here(), run_batch(), fill_slots(), manually_selected() (+6 more)

### Community 70 - "ExtendedRecoveryTests"
Cohesion: 0.19
Nodes (5): ExtendedRecoveryTests, fail(), read(), read(), menu()

### Community 71 - "PROJECT_HANDOFF.md"
Cohesion: 0.13
Nodes (14): b1–b3 ngẫu nhiên cho q1–q12 — 14/11/2026, B4–b11 chạy đồng thời và OCR — 14/11/2026, b6 US +1 còn mở sau bốn cú chạm — 14/11/2026, Bỏ thời hạn tổng sau menu — 14/11/2026, Bổ sung đọc ảnh OCR và chạm trực tiếp dự phòng cho b26 khi uiautomator dump WebView lỗi — 19/11/2026, Cơ chế chụp ảnh OCR quét chữ ấn luôn cho toàn bộ b26–b31 — 19/11/2026, Không bỏ qua b1–b3 ngẫu nhiên; 14 ảnh menu mới — 14/11/2026, Lỗi chạy song song q3 Terminal trùng / q1 chưa thấy menu — 14/11/2026 (+6 more)

### Community 72 - "_tail_menu"
Cohesion: 0.12
Nodes (7): _tail_menu(), Nhận diện giao diện lúc chạy, Nhập liệu và lỗi, Quy tắc tự động hóa sau menu ba gạch, Trạng thái hiện tại của dự án, Từng máy độc lập, continuation()

### Community 74 - "ProxyConfig"
Cohesion: 0.11
Nodes (14): _create_profile_form(), _open_profiles(), ProfileCreateNotSubmitted, ProfileManagerWindowError, ProxyConfig, ProxyTestFailed, visible_profile_names(), unavailable() (+6 more)

### Community 75 - "account_flow.py"
Cohesion: 0.12
Nodes (31): _ActionNotResolved, confirmed_login_otp_nodes(), continue_number(), enter_otp(), finish_auto(), finish_create(), finish_login(), focus_otp() (+23 more)

### Community 76 - "_choose_tail_target"
Cohesion: 0.29
Nodes (3): _choose_tail_target(), choose(), choose()

### Community 77 - "_tail_candidates"
Cohesion: 0.17
Nodes (4): _tail_candidates(), _tail_input_action(), _tail_safe_page_choices(), Chung b12–b15 — Mở ba gạch rồi ba lượt điều hướng ngẫu nhiên

### Community 82 - "._run"
Cohesion: 0.22
Nodes (7): 002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ, Các bước, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Rủi ro và bảo trì, Điều kiện dừng

### Community 83 - "AccountData"
Cohesion: 0.11
Nodes (6): _automatic_resume_slots(), AccountData, AppSettings, DesktopResumeTests, Q2FlowTests, on_worker()

### Community 84 - "OTP_DESIGN.md"
Cohesion: 0.50
Nodes (3): Nối vào bước tạo tài khoản sau khi xác minh màn hình Amazon, Thiết kế OTP cho từng Profile, Đã chuẩn bị

### Community 85 - "ensure_manager_ready"
Cohesion: 0.27
Nodes (5): ensure_manager_ready(), _main_window(), collect(), _swarmote_exe(), ManagerStartupTests

### Community 86 - "_restore_prefix_menu"
Cohesion: 0.25
Nodes (3): _menu(), _PrefixRecoveryStop, _restore_prefix_menu()

### Community 87 - "Giai đoạn 2 — bản thử State Machine riêng q7"
Cohesion: 0.40
Nodes (5): Cách thử bản pilot cũ (không áp dụng cho factory hiện hành), Giai đoạn 2 — bản thử State Machine riêng q7, Giới hạn, Phạm vi và quan hệ với luồng cũ, Sơ đồ

### Community 88 - "_prefix_nodes"
Cohesion: 0.25
Nodes (7): _prefix_nodes(), Cách xử lý ảnh tiếp theo, Phần riêng từng máy, Tiến độ hướng dẫn bằng ảnh — cập nhật 13/11/2026, 14 ảnh menu chung b1–b3 ngẫu nhiên — 14/11/2026, B1–b3 xem menu ngẫu nhiên cho 12 máy — 14/11/2026, B1–B3 hiện hành — Ba lượt ngẫu nhiên q1–q12

### Community 89 - "PreparationThreadsTests"
Cohesion: 0.29
Nodes (4): apartment_type(), PreparationThreadsTests, run(), install()

### Community 91 - "_proxy_postal_prefix"
Cohesion: 0.48
Nodes (3): _proxy_postal_prefix(), controls(), ProxyPostalPrefixTests

### Community 92 - "GRAPH_AUDIT.md"
Cohesion: 0.50
Nodes (3): Cách kiểm tra sau mỗi sửa đổi, Giới hạn đã xác nhận, Kiểm tra độ phủ Graphify — cập nhật 26/11/2026

### Community 94 - "File dự án mà Graphify không phân tích trực tiếp"
Cohesion: 0.40
Nodes (5): File dự án mà Graphify không phân tích trực tiếp, .gitignore, Launch Swarmote Tool.pyw, pyproject.toml, Ảnh PNG trong dự án

### Community 95 - "_country_nodes"
Cohesion: 0.50
Nodes (3): _country_nodes(), _CountryReadStop, b6 cuộn chạm đáy rồi vuốt ngược nhẹ tìm US +1 — 14/11/2026

## Knowledge Gaps
- **1 isolated node(s):** `amazon-android-tool`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 554 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **21 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ToolError` connect `cli.py` to `registration.py`, `build_common_steps`, `otp.py`, `BulkInputTests`, `swarmote_desktop.py`, `RunnerTests`, `PostMenuStep`, `ToolError`, `AddressDetailTests`, `adb`, `StopResetTests`, `cloud.py`, `open_home_menu`, `MarketplaceFlowTests`, `marketplace_flow.py`, `screen`, `core.py`, `q7_state_machine.py`, `swarmote_desktop.py`, `amazon_is_foreground`, `Window`, `RegistrationState`, `build_random_steps`, `ui_backend.py`, `vision.py`, `_visible`, `setup.py`, `_type_field`, `build_create_address_steps`, `.remaining`, `q7_random_prefix.py`, `pathlib`, `cloud_adb`, `cli.py`, `.test_b10_stalled_whatsapp_pauses_only_affected_phone`, `_recognize`, `build_reload_payment_steps`, `CountryRecoveryTests`, `test_isolated_reader.py`, `BatchDraft`, `_prepare_phone`, `ExtendedRecoveryTests`, `_tail_menu`, `._continue_profile`, `ProxyConfig`, `account_flow.py`, `build_q1_steps`, `._run`, `AccountData`, `ensure_manager_ready`, `_restore_prefix_menu`, `_prefix_nodes`, `._apply_bulk_text`, `_country_nodes`, `_ScreenWaitExpired`, `_new_prefix`, `.test_b11_taps_otp_field_even_when_provider_read_fails`?**
  _High betweenness centrality (0.356) - this node is a cross-community bridge._
- **Are the 58 inferred relationships involving `ToolError` (e.g. with `_read_nodes_once()` and `_resume_address_payment_index()`) actually correct?**
  _`ToolError` has 58 INFERRED edges - model-reasoned connections that need verification._
- **What connects `amazon-android-tool` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `build_common_steps` be split into smaller, more focused modules?**
  _Cohesion score 0.06919945725915876 - nodes in this community are weakly interconnected._
- **Why does `CloudPhone` connect `amazon_is_foreground` to `registration.py`, `build_common_steps`, `swarmote_desktop.py`, `PostMenuStep`, `AddressDetailTests`, `cloud.py`, `open_home_menu`, `MarketplaceFlowTests`, `screen`, `Q3Q4FlowTests`, `q7_state_machine.py`, `swarmote_desktop.py`, `.test_manual_otp_repair_continues_with_confirmation_and_tail_for_both_modes`, `Window`, `RegistrationState`, `build_random_steps`, `ui_backend.py`, `_type_field`, `build_create_address_steps`, `.remaining`, `cli.py`, `q7_random_prefix.py`, `cloud_adb`, `cli.py`, `.test_b10_stalled_whatsapp_pauses_only_affected_phone`, `.test_creation_session_runs_b11_confirmation_through_b15_on_all_twelve_slots`, `build_reload_payment_steps`, `CountryRecoveryTests`, `test_isolated_reader.py`, `_prepare_phone`, `ExtendedRecoveryTests`, `_tail_menu`, `._continue_profile`, `account_flow.py`, `build_q1_steps`, `AccountData`, `_restore_prefix_menu`, `test_q5_flow.py`, `._run_post_menu`, `MenuReturnTests`?**
  _High betweenness centrality (0.114) - this node is a cross-community bridge._
- **Are the 88 inferred relationships involving `CloudPhone` (e.g. with `build_common_steps()` and `_country_full_row()`) actually correct?**
  _`CloudPhone` has 88 INFERRED edges - model-reasoned connections that need verification._
- **Should `otp.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08712121212121213 - nodes in this community are weakly interconnected._