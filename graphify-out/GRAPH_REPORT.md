# Graph Report - boom4may  (2026-11-27)

## Corpus Check
- 135 files · ~167,419 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 1, .bat 1, .pyw 1)

## Summary
- 2182 nodes · 7599 edges · 99 communities (79 shown, 20 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 1093 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `6e2d86d6`
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
- amazon-android-tool
- Ảnh hướng dẫn q1/q2 và menu chung lưu cục bộ
- core.py
- MarketplaceFlowTests
- marketplace_flow.py
- _read_nodes
- Điều hướng hai dạng menu ba gạch
- Q3Q4FlowTests
- _type_field
- ExtendedRecoveryTests
- Nghiên cứu và tích hợp Swarmote
- q7_state_machine.py
- ExtendedRecoveryTests
- CloudPhone
- Window
- RegistrationState
- PROJECT_INDEX.md
- build_random_steps
- core.py
- vision.py
- settings.py
- _visible
- time
- profile_status
- build_create_address_steps
- main
- cli.py
- Bàn giao trạng thái dự án — 13/11/2026
- random_prefix.py
- FakeControl
- PostMenuStep
- ProfileRegistry
- cloud_adb
- Value
- swarmote_desktop.py
- .remaining
- b1–b11 Reliability and Latency Implementation Plan
- open_amazon
- Danh mục ảnh nằm trong dự án
- build_q1_steps
- Amazon Android Tool — Giai đoạn A/B
- profile_status
- _CombinedStop
- Giao diện vận hành
- validate_card
- Amazon trên Swarmote
- CloudPhone
- build_reload_payment_steps
- Bộ cài chia sẻ Windows x64
- CountryRecoveryTests
- test_isolated_reader.py
- VERIFICATION.md
- BatchDraft
- _prepare_phone
- run_batch
- .test_b10_stalled_whatsapp_pauses_only_affected_phone
- PROJECT_HANDOFF.md
- .test_creation_session_runs_b11_confirmation_through_b15_on_all_twelve_slots
- otp_token
- ProfilesNavigationTests
- ToolError
- retry_preparation
- AccountData
- test_q1_flow.py
- run
- validate_otp_url
- action
- .get
- desktop.py
- OTP_DESIGN.md
- ensure_manager_ready
- build_post_auth_steps
- .test_manual_otp_repair_continues_with_confirmation_and_tail_for_both_modes
- File dự án mà Graphify không phân tích trực tiếp
- 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng
- .__init__
- .test_selected_stop_finishes_install_before_stopping_that_phone
- GRAPH_AUDIT.md
- PLAN.md
- Luồng q1 từ menu ba gạch tới nhập OTP
- Q5_FLOW.md
- PreparationProgressTests

## God Nodes (most connected - your core abstractions)
1. `ToolError` - 354 edges
2. `CloudPhone` - 234 edges
3. `AttemptDeadline` - 202 edges
4. `RunJob` - 164 edges
5. `RegistrationState` - 162 edges
6. `build_common_steps()` - 115 edges
7. `Window` - 97 edges
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

## Communities (99 total, 20 thin omitted)

### Community 0 - "registration.py"
Cohesion: 0.20
Nodes (10): require_online(), _field_for_label(), fill_identifier(), fill_signup_form(), _nodes(), _tap(), _type_into(), _unique_button() (+2 more)

### Community 1 - "build_common_steps"
Cohesion: 0.07
Nodes (5): build_common_steps(), _find_scrolling(), node(), Q1FlowTests, provider_read()

### Community 2 - "otp.py"
Cohesion: 0.10
Nodes (8): browser_launch_options(), extract_otp(), _NoRedirect, read_otp(), _read_otp_in_browser(), wait_for_new_otp(), OtpTests, PackagedBrowserTests

### Community 3 - "BulkInputTests"
Cohesion: 0.09
Nodes (6): parse_bulk_payload(), parse_column(), parse_records(), _url_from_cell(), Dán bảng Amazon có ghi chú thẻ live và URL OTP escaped — 14/11/2026, BulkInputTests

### Community 4 - "windows_identity.py"
Cohesion: 0.23
Nodes (6): create_shortcut(), relaunch_command(), runtime(), set_process_identity(), set_window_identity(), WindowsIdentityTests

### Community 5 - "swarmote_desktop.py"
Cohesion: 0.09
Nodes (29): _check_stop(), collapse_apps_panel(), install_amazon(), check_stop(), open_adb_shell(), _pause(), _phone_window(), _progress_reporter() (+21 more)

### Community 6 - "RunnerTests"
Cohesion: 0.10
Nodes (6): RunnerTests, create(), resume(), create(), failed_start(), resume()

### Community 7 - "PostMenuStep"
Cohesion: 0.09
Nodes (12): PostMenuSession, _first_point(), RunJob, PostMenuTests, first_step(), reconcile(), first(), SharedStepRecoveryTests (+4 more)

### Community 8 - "ToolError"
Cohesion: 0.09
Nodes (11): _select_profile_rows(), _selected_profile_names(), start_profile(), start_profiles_together(), _wait_for_selected(), BatchStartTests, checkbox(), toggle() (+3 more)

### Community 9 - "AddressDetailTests"
Cohesion: 0.12
Nodes (7): build_create_address_detail_steps(), AddressDetailTests, read(), adb(), tap(), read(), item()

### Community 10 - "003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật"
Cohesion: 0.08
Nodes (21): 002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Rủi ro và bảo trì, Điều kiện dừng, 003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật, Các bước (+13 more)

### Community 11 - "Danh mục từng bước đã biết — 13/11/2026"
Cohesion: 0.06
Nodes (36): B1–B3 hiện hành — Ba lượt ngẫu nhiên q1–q12, Bản thử q7 State Machine — 14/11/2026, Chung b10 — Chuyển WhatsApp sang SMS, Chung b11 — Lấy và gõ OTP SMS, Chung b11a — Chạm ô OTP trên màn SMS, Chung b11b — Xác minh đăng nhập hoặc bấm Create của luồng tạo, Chung b4 — Sign In từ menu, Chung b4a — Chạm ô SĐT (+28 more)

### Community 12 - "build_random_steps"
Cohesion: 0.06
Nodes (10): resume_common_index(), build_random_steps(), finish_view(), B1–b3 xem menu ngẫu nhiên cho 12 máy — 14/11/2026, Dự phòng dùng chung khi chạy song song — 14/11/2026, adb(), adb(), adb() (+2 more)

### Community 16 - "Ảnh hướng dẫn q1/q2 và menu chung lưu cục bộ"
Cohesion: 0.07
Nodes (29): 14 ảnh menu chung b1–b3 ngẫu nhiên — 14/11/2026, B16–b22 chung — Đổi marketplace sang United States (18/11/2026), B32–b39 — Reload Balance, thêm thẻ và địa chỉ thanh toán (21/11/2026), B6 — Hai ảnh đính kèm mới ngày 13/11/2026, Menu chung ảnh 01 — Danh sách chữ, Menu chung ảnh 02 — App Store bên phải sau khi Amazon mở, q1 b6 — US +1 hiện nhưng chạm không đóng hộp, 14/11/2026, q1 ảnh 01 — Menu và ba thẻ (+21 more)

### Community 17 - "core.py"
Cohesion: 0.10
Nodes (13): _confirm_menu_fallback(), _menu_evidence(), MenuReadUnavailable, _nodes(), budget(), open_home_menu(), ready_for_home_menu(), _tap() (+5 more)

### Community 18 - "MarketplaceFlowTests"
Cohesion: 0.07
Nodes (23): AttemptDeadline, MarketplaceFlowTests, read(), adb(), read(), tap(), read(), read() (+15 more)

### Community 19 - "marketplace_flow.py"
Cohesion: 0.18
Nodes (25): _account_tab(), build_marketplace_steps(), run(), account_target(), back_and_read_text(), foreground_ready(), recover_country_list(), _country_card() (+17 more)

### Community 20 - "_read_nodes"
Cohesion: 0.17
Nodes (21): _at_or_after(), sign_in(), _ensure_menu(), home_visible(), _read_nodes(), _unique(), visit_home(), cart_action() (+13 more)

### Community 21 - "Điều hướng hai dạng menu ba gạch"
Cohesion: 0.50
Nodes (4): Bằng chứng và phạm vi, Kiểm chứng, Quy tắc chạy, Điều hướng hai dạng menu ba gạch

### Community 22 - "Q3Q4FlowTests"
Cohesion: 0.21
Nodes (3): build_q3_steps(), build_q4_steps(), Q3Q4FlowTests

### Community 23 - "_type_field"
Cohesion: 0.19
Nodes (4): _type_field(), Phục hồi khi ô nhập chưa nhận focus ở b4–b11 — 14/11/2026, FlowRecoveryTests, form()

### Community 24 - "ExtendedRecoveryTests"
Cohesion: 0.14
Nodes (5): arrange_on_open(), _row_if_fits(), _sort_key(), _tiles(), PhoneWindowLayoutTests

### Community 25 - "Nghiên cứu và tích hợp Swarmote"
Cohesion: 0.40
Nodes (4): Hành vi có bằng chứng, Kiểm thử còn lại, Nghiên cứu và tích hợp Swarmote, Phần đã áp dụng

### Community 26 - "q7_state_machine.py"
Cohesion: 0.08
Nodes (17): ActionValidator, _already_reached_result(), build_q7_pilot_steps(), run(), _past_known_step(), RecoveryHandler, ResultVerifier, StateDeadline (+9 more)

### Community 27 - "ExtendedRecoveryTests"
Cohesion: 0.14
Nodes (7): _start_and_confirm(), Tự phục hồi lỗi tạm thời trong mẻ nhiều máy — 14/11/2026, ExtendedRecoveryTests, fail(), read(), read(), menu()

### Community 28 - "CloudPhone"
Cohesion: 0.15
Nodes (7): amazon_is_foreground(), CloudPhone, reconcile(), route(), CloudBridgeTests, step(), SharedFallbackTests

### Community 30 - "RegistrationState"
Cohesion: 0.08
Nodes (8): RegistrationState, build_tail_steps(), _choose_tail_target(), Q5FlowTests, RandomPrefixTests, continuation(), choose(), choose()

### Community 31 - "PROJECT_INDEX.md"
Cohesion: 0.23
Nodes (5): Bản đồ repository, Luồng q2 từ menu ba gạch, q3 — b1–b3 và nối luồng chung, q4 — Giỏ hàng, Pets, Home and DIY, q6 — Trang chủ, Giỏ hàng, menu và một thẻ

### Community 32 - "build_random_steps"
Cohesion: 0.11
Nodes (4): RandomPrefixTests, adb(), adb(), adb()

### Community 33 - "core.py"
Cohesion: 0.06
Nodes (44): swarmote_adb_path(), swarmote_tunnel_owner(), adb(), app_data_dir(), available_memory_mb(), avd_names(), check_play(), configure_avd() (+36 more)

### Community 34 - "vision.py"
Cohesion: 0.07
Nodes (19): _bounds(), _canonical_text(), _compact(), _engine(), _field_contents(), _field_is_blank(), _input_box(), _join_wrapped_categories() (+11 more)

### Community 35 - "settings.py"
Cohesion: 0.18
Nodes (6): default_path(), AppSettings, load_settings(), save_settings(), settings_path(), SettingsTests

### Community 36 - "_visible"
Cohesion: 0.14
Nodes (33): _bounds(), _resume_address_payment_index(), _text(), _visible(), _action(), _address_form(), _addresses(), _bounded_native() (+25 more)

### Community 37 - "time"
Cohesion: 0.18
Nodes (12): main(), check_runtime(), main(), verify(), _app_installed(), _app_paths(), _check_external_apps(), _install_python_dependencies() (+4 more)

### Community 38 - "profile_status"
Cohesion: 0.15
Nodes (9): _profile_row_status(), profile_status(), _unfiltered_single_page(), Các bước, Giới hạn và lựa chọn cần xác minh, Kế hoạch sửa luồng mẻ Swarmote, Kết luận đã xác minh, Quy trình đích (+1 more)

### Community 39 - "build_create_address_steps"
Cohesion: 0.24
Nodes (4): build_create_address_steps(), CreateAddressFlowTests, read(), node()

### Community 40 - "main"
Cohesion: 0.31
Nodes (3): main(), main(), LauncherTests

### Community 41 - "cli.py"
Cohesion: 0.09
Nodes (21): BatchItem, parse_proxy_line(), prepare_five(), BulkRecord, lines(), _proxy_rows(), _table_cells(), main() (+13 more)

### Community 42 - "Bàn giao trạng thái dự án — 13/11/2026"
Cohesion: 0.12
Nodes (15): save(), B6 danh sách quốc gia vẫn mở sau khi chọn — 13/11/2026, Bàn giao trạng thái dự án — 13/11/2026, Bản chính boom4may và bản dự phòng — 14/11/2026, Bộ cài offline chia sẻ — 14/11/2026, Cài đặt máy mới, Dừng riêng máy đang chọn — 14/11/2026, q3/q4 đã nối b1–b3 và thử đồng thời bốn luồng — 13/11/2026 (+7 more)

### Community 43 - "random_prefix.py"
Cohesion: 0.06
Nodes (31): scroll_view(), wait_until(), _new_prefix(), RecoverableStepError, build_random_steps(), browse(), action(), run_browse() (+23 more)

### Community 44 - "FakeControl"
Cohesion: 0.13
Nodes (5): ParallelInstallTests, PhoneWindow, FakeControl, InstallTests, descendants()

### Community 45 - "PostMenuStep"
Cohesion: 0.17
Nodes (4): PostMenuStep, ResumeRegistrationStateTests, factory(), factory()

### Community 46 - "ProfileRegistry"
Cohesion: 0.17
Nodes (8): ProfileRegistry, ProfileLookupError, ProfileNotFound, Thiết kế yêu cầu, absent(), ProfileRegistryTests, lookup(), broken()

### Community 47 - "cloud_adb"
Cohesion: 0.23
Nodes (14): _country_full_row(), _keyboard_visible(), _tap(), cloud_adb(), reported_installer(), _foreground(), _scroll_country(), _size() (+6 more)

### Community 49 - "swarmote_desktop.py"
Cohesion: 0.18
Nodes (14): _activate_manager(), _create_profile_form(), _descendants(), _invoke(), _one(), _profile_checkbox(), _profile_form_open(), ProfileCreateNotSubmitted (+6 more)

### Community 50 - ".remaining"
Cohesion: 0.20
Nodes (12): _read_hierarchy(), _read_login_sms_visual(), _read_nodes_once(), _read_visual_nodes(), _UiReadIncomplete, current(), ReaderResponseError, _serve() (+4 more)

### Community 51 - "b1–b11 Reliability and Latency Implementation Plan"
Cohesion: 0.18
Nodes (10): b1–b11 Reliability and Latency Implementation Plan, Completion Criteria, File Map, Global Constraints, Review Focus, Task 1: Measure current step latency and classify existing failures, Task 2: Define safe retry, reconcile, pause, and stop behavior, Task 3: Reduce redundant UI reads and unnecessary waits (+2 more)

### Community 52 - "open_amazon"
Cohesion: 0.16
Nodes (9): cloud_serials(), open_amazon(), foreground(), package_path(), probe(), prop(), scan(), adb() (+1 more)

### Community 53 - "Danh mục ảnh nằm trong dự án"
Cohesion: 0.22
Nodes (9): amazon_android/assets/obsidian_prism.png, amazon_android/assets/swarmote_tool_square.png và swarmote_tool.ico, assets/ui_history/machine7_input_before.png, assets/ui_history/reset_check.png, assets/ui_history/ui-12.png, assets/ui_history/ui_palette_preview.png, assets/ui_history/ui-preview.png, assets/ui_history/ui-screenshot.png (+1 more)

### Community 54 - "build_q1_steps"
Cohesion: 0.11
Nodes (8): build_q1_steps(), category(), build_q5_steps(), Cách xử lý ảnh tiếp theo, Phần riêng từng máy, Tiến độ hướng dẫn bằng ảnh — cập nhật 13/11/2026, Đã có trong graph, Q6FlowTests

### Community 55 - "Amazon Android Tool — Giai đoạn A/B"
Cohesion: 0.29
Nodes (7): Amazon Android Tool — Giai đoạn A/B, Cài trên máy Windows mới, Dán nhiều proxy, Sử dụng, Trạng thái nghiệm thu, Yêu cầu, Điện thoại đám mây Swarmote

### Community 56 - "profile_status"
Cohesion: 0.48
Nodes (3): _proxy_postal_prefix(), controls(), ProxyPostalPrefixTests

### Community 58 - "Giao diện vận hành"
Cohesion: 0.40
Nodes (4): Bố cục, Giao diện vận hành, Hướng thị giác, Quy tắc

### Community 60 - "Amazon trên Swarmote"
Cohesion: 0.33
Nodes (5): Amazon trên Swarmote, Người dùng và công việc, Nền tảng, Điều chưa xác minh, Định hướng ngôn ngữ nếu xây dựng lại — 23/11/2026

### Community 61 - "CloudPhone"
Cohesion: 0.08
Nodes (24): b6 Country US +1 — 14/11/2026, B6 cuộn quốc gia và chọn lại — 13/11/2026, Biên bản kiểm tra thực tế — 2026-11-12, Cài và đo UiAutomator2 theo phê duyệt mới — 13/11/2026, Dừng riêng một máy — 14/11/2026, Focus ô nhập b4–b11 — 14/11/2026, Ghim taskbar — 13/11/2026, Giao diện sáng, dễ đọc — 2026-11-13 (+16 more)

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
Cohesion: 0.29
Nodes (6): phone_reader(), PhoneReader, fake_worker(), IsolationTests, duplicate(), production_worker_with_fake_android()

### Community 66 - "VERIFICATION.md"
Cohesion: 0.15
Nodes (11): Kết luận và tích hợp, Kết quả thực tế, So sánh bộ đọc trên q1 — 13/11/2026, Thành phần thiết bị, b1–b3 bắt buộc có ba cú bấm — 14/11/2026, b1–b3 ngẫu nhiên cho 12 máy — 14/11/2026, b1–b3 ngẫu nhiên trên 12 máy, không dùng OCR — 14/11/2026, b6 cuộn tới đáy rồi vuốt ngược — 14/11/2026 (+3 more)

### Community 68 - "_prepare_phone"
Cohesion: 0.17
Nodes (9): _prepare_phone(), _prepare_phone_locked(), progress(), stop_here(), Thu panel Apps sau khi mở Amazon — 14/11/2026, apartment_type(), PreparationThreadsTests, run() (+1 more)

### Community 69 - "run_batch"
Cohesion: 0.17
Nodes (11): run_batch(), fill_slots(), manually_selected(), refresh_slots(), requested(), stop_job(), visible_lookup(), ProfileStartNotSubmitted (+3 more)

### Community 71 - "PROJECT_HANDOFF.md"
Cohesion: 0.13
Nodes (14): b1–b3 ngẫu nhiên cho q1–q12 — 14/11/2026, B4–b11 chạy đồng thời và OCR — 14/11/2026, b6 US +1 còn mở sau bốn cú chạm — 14/11/2026, Bản thử State Machine q7 và b1–b3 mở mục con — 14/11/2026, Bỏ thời hạn tổng sau menu — 14/11/2026, Bổ sung đọc ảnh OCR và chạm trực tiếp dự phòng cho b26 khi uiautomator dump WebView lỗi — 19/11/2026, Cơ chế chụp ảnh OCR quét chữ ấn luôn cho toàn bộ b26–b31 — 19/11/2026, Không bỏ qua b1–b3 ngẫu nhiên; 14 ảnh menu mới — 14/11/2026 (+6 more)

### Community 72 - ".test_creation_session_runs_b11_confirmation_through_b15_on_all_twelve_slots"
Cohesion: 0.17
Nodes (3): browse(), tap(), tap()

### Community 74 - "ProfilesNavigationTests"
Cohesion: 0.14
Nodes (8): _open_profiles(), visible_profile_names(), control(), ProfilesNavigationTests, descendants(), invoke(), descendants(), descendants()

### Community 75 - "ToolError"
Cohesion: 0.11
Nodes (39): _ActionNotResolved, confirmed_login_otp_nodes(), continue_number(), country(), enter_otp(), finish_auto(), finish_create(), finish_login() (+31 more)

### Community 76 - "retry_preparation"
Cohesion: 0.18
Nodes (4): emit(), _phone_preparation_lock(), retry_preparation(), P03 — Mở form New Profile

### Community 78 - "test_q1_flow.py"
Cohesion: 0.22
Nodes (3): menu_layout(), route_list_menu(), _ScreenWaitExpired

### Community 79 - "run"
Cohesion: 0.18
Nodes (4): run(), run(), run(), run()

### Community 81 - "action"
Cohesion: 0.39
Nodes (8): open_menu(), read_menu(), return_to_menu(), view(), visit(), action(), visit_seconds(), Tự động chuyển bước sau 60 giây nếu không thấy menu Browse ở b13–b15 — 19/11/2026

### Community 83 - "desktop.py"
Cohesion: 0.09
Nodes (4): _automatic_resume_slots(), AccountData, DesktopResumeTests, on_worker()

### Community 84 - "OTP_DESIGN.md"
Cohesion: 0.50
Nodes (3): Nối vào bước tạo tài khoản sau khi xác minh màn hình Amazon, Thiết kế OTP cho từng Profile, Đã chuẩn bị

### Community 85 - "ensure_manager_ready"
Cohesion: 0.21
Nodes (7): ensure_manager_ready(), _main_window(), collect(), ProfileManagerWindowError, _swarmote_exe(), ManagerStartupTests, unavailable()

### Community 86 - "build_post_auth_steps"
Cohesion: 0.18
Nodes (11): Hướng dẫn khi tiếp tục dự án, build_post_auth_steps(), Nhận diện giao diện lúc chạy, Nhập liệu và lỗi, Quy tắc tự động hóa sau menu ba gạch, Trạng thái hiện tại của dự án, Từng máy độc lập, b6 cuộn chạm đáy rồi vuốt ngược nhẹ tìm US +1 — 14/11/2026 (+3 more)

### Community 87 - ".test_manual_otp_repair_continues_with_confirmation_and_tail_for_both_modes"
Cohesion: 0.18
Nodes (5): Cách thử bản pilot cũ (không áp dụng cho factory hiện hành), Giai đoạn 2 — bản thử State Machine riêng q7, Giới hạn, Phạm vi và quan hệ với luồng cũ, Sơ đồ

### Community 88 - "File dự án mà Graphify không phân tích trực tiếp"
Cohesion: 0.40
Nodes (5): File dự án mà Graphify không phân tích trực tiếp, .gitignore, Launch Swarmote Tool.pyw, pyproject.toml, Ảnh PNG trong dự án

### Community 89 - "001 — Tách dữ liệu từng mẻ và đối chiếu số hàng"
Cohesion: 0.29
Nodes (7): 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Rủi ro và bảo trì, Thiết kế yêu cầu, Điều kiện dừng

### Community 90 - ".__init__"
Cohesion: 0.17
Nodes (5): set_tk_icon(), Sửa shortcut ghim mở nhầm IDLE — 13/11/2026, Ô Amazon riêng Máy 1–12 dễ thấy hơn — 14/11/2026, DesktopLayoutTests, __init__()

### Community 92 - "GRAPH_AUDIT.md"
Cohesion: 0.50
Nodes (3): Cách kiểm tra sau mỗi sửa đổi, Giới hạn đã xác nhận, Kiểm tra độ phủ Graphify — cập nhật 26/11/2026

## Knowledge Gaps
- **1 isolated node(s):** `amazon-android-tool`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 536 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **20 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ToolError` connect `ToolError` to `registration.py`, `build_common_steps`, `otp.py`, `BulkInputTests`, `swarmote_desktop.py`, `RunnerTests`, `PostMenuStep`, `ToolError`, `AddressDetailTests`, `003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật`, `build_random_steps`, `StopResetTests`, `cloud.py`, `core.py`, `MarketplaceFlowTests`, `marketplace_flow.py`, `_read_nodes`, `_type_field`, `q7_state_machine.py`, `ExtendedRecoveryTests`, `CloudPhone`, `Window`, `RegistrationState`, `build_random_steps`, `core.py`, `vision.py`, `settings.py`, `_visible`, `build_create_address_steps`, `cli.py`, `random_prefix.py`, `PostMenuStep`, `ProfileRegistry`, `cloud_adb`, `swarmote_desktop.py`, `.remaining`, `open_amazon`, `build_q1_steps`, `validate_card`, `build_reload_payment_steps`, `CountryRecoveryTests`, `test_isolated_reader.py`, `BatchDraft`, `_prepare_phone`, `run_batch`, `.test_b10_stalled_whatsapp_pauses_only_affected_phone`, `otp_token`, `ProfilesNavigationTests`, `retry_preparation`, `test_q1_flow.py`, `validate_otp_url`, `action`, `desktop.py`, `ensure_manager_ready`, `.test_selected_stop_finishes_install_before_stopping_that_phone`?**
  _High betweenness centrality (0.351) - this node is a cross-community bridge._
- **Are the 58 inferred relationships involving `ToolError` (e.g. with `_read_nodes_once()` and `_resume_address_payment_index()`) actually correct?**
  _`ToolError` has 58 INFERRED edges - model-reasoned connections that need verification._
- **What connects `amazon-android-tool` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `build_common_steps` be split into smaller, more focused modules?**
  _Cohesion score 0.06921529175050302 - nodes in this community are weakly interconnected._
- **Why does `CloudPhone` connect `CloudPhone` to `registration.py`, `build_common_steps`, `swarmote_desktop.py`, `PostMenuStep`, `AddressDetailTests`, `build_random_steps`, `cloud.py`, `core.py`, `MarketplaceFlowTests`, `_read_nodes`, `Q3Q4FlowTests`, `_type_field`, `q7_state_machine.py`, `ExtendedRecoveryTests`, `Window`, `RegistrationState`, `build_random_steps`, `core.py`, `build_create_address_steps`, `cli.py`, `random_prefix.py`, `PostMenuStep`, `cloud_adb`, `swarmote_desktop.py`, `.remaining`, `open_amazon`, `build_q1_steps`, `validate_card`, `build_reload_payment_steps`, `CountryRecoveryTests`, `test_isolated_reader.py`, `_prepare_phone`, `.test_b10_stalled_whatsapp_pauses_only_affected_phone`, `ToolError`, `AccountData`, `test_q1_flow.py`, `desktop.py`, `build_post_auth_steps`, `.test_manual_otp_repair_continues_with_confirmation_and_tail_for_both_modes`?**
  _High betweenness centrality (0.130) - this node is a cross-community bridge._
- **Are the 88 inferred relationships involving `CloudPhone` (e.g. with `build_common_steps()` and `_country_full_row()`) actually correct?**
  _`CloudPhone` has 88 INFERRED edges - model-reasoned connections that need verification._
- **Should `otp.py` be split into smaller, more focused modules?**
  _Cohesion score 0.10114942528735632 - nodes in this community are weakly interconnected._