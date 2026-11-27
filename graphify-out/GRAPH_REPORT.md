# Graph Report - boom4may  (2026-11-27)

## Corpus Check
- 138 files · ~174,489 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 2, .bat 1, .pyw 1)

## Summary
- 2263 nodes · 7832 edges · 91 communities (80 shown, 11 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 1128 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `8f761751`
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
- PostMenuStep
- Nghiên cứu và tích hợp Swarmote
- ToolError
- ResumeRegistrationStateTests
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
- swarmote_desktop.py
- cloud_adb
- phone_window_layout.py
- cli.py
- SafetyTests
- b1–b11 Reliability and Latency Implementation Plan
- VisionFieldTests
- Danh mục ảnh nằm trong dự án
- .test_b10_stalled_whatsapp_pauses_only_affected_phone
- Amazon Android Tool — Giai đoạn A/B
- desktop.py
- _CombinedStop
- Giao diện vận hành
- _recognize
- Amazon trên Swarmote
- CloudPhone
- build_reload_payment_steps
- Bộ cài chia sẻ Windows x64
- SmoothScrollableFrame
- test_isolated_reader.py
- VERIFICATION.md
- BatchDraft
- _prepare_phone
- .stop
- ExtendedRecoveryTests
- PROJECT_HANDOFF.md
- build_post_auth_steps
- ._continue_profile
- ProxyConfig
- account_flow.py
- _choose_tail_target
- main
- StateSpec
- DesktopLayoutTests
- PreparationProgressTests
- ._run
- RunJob
- ensure_manager_ready
- Giai đoạn 2 — bản thử State Machine riêng q7
- test_q5_flow.py
- _proxy_postal_prefix
- GRAPH_AUDIT.md
- ._apply_bulk_text
- File dự án mà Graphify không phân tích trực tiếp
- MenuReturnTests

## God Nodes (most connected - your core abstractions)
1. `ToolError` - 354 edges
2. `CloudPhone` - 234 edges
3. `AttemptDeadline` - 202 edges
4. `RunJob` - 170 edges
5. `RegistrationState` - 162 edges
6. `build_common_steps()` - 115 edges
7. `Window` - 109 edges
8. `PostMenuStep` - 93 edges
9. `Q1FlowTests` - 92 edges
10. `PostMenuSession` - 85 edges

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

## Communities (91 total, 11 thin omitted)

### Community 0 - "registration.py"
Cohesion: 0.22
Nodes (9): _field_for_label(), fill_identifier(), fill_signup_form(), _nodes(), _tap(), _type_into(), _unique_button(), _wait_nodes() (+1 more)

### Community 1 - "build_common_steps"
Cohesion: 0.05
Nodes (9): build_common_steps(), _ScreenWaitExpired, build_q1_steps(), category(), B1–b3 xem menu ngẫu nhiên cho 12 máy — 14/11/2026, Phạm vi và quan hệ với luồng cũ, node(), Q1FlowTests (+1 more)

### Community 2 - "otp.py"
Cohesion: 0.10
Nodes (8): browser_launch_options(), extract_otp(), _NoRedirect, read_otp(), _read_otp_in_browser(), wait_for_new_otp(), OtpTests, PackagedBrowserTests

### Community 3 - "BulkInputTests"
Cohesion: 0.08
Nodes (6): parse_bulk_payload(), parse_column(), parse_records(), Dán bảng Amazon có ghi chú thẻ live và URL OTP escaped — 14/11/2026, BulkInputTests, Value

### Community 4 - "windows_identity.py"
Cohesion: 0.21
Nodes (6): create_shortcut(), relaunch_command(), runtime(), set_process_identity(), set_window_identity(), WindowsIdentityTests

### Community 5 - "swarmote_desktop.py"
Cohesion: 0.08
Nodes (30): ready_for_home_menu(), _check_stop(), collapse_apps_panel(), _descendants(), install_amazon(), open_adb_shell(), _pause(), _phone_window() (+22 more)

### Community 6 - "RunnerTests"
Cohesion: 0.05
Nodes (20): default_path(), ProfileRegistry, absent(), ProfileRegistryTests, lookup(), broken(), RunnerTests, create() (+12 more)

### Community 7 - "PostMenuStep"
Cohesion: 0.09
Nodes (11): PostMenuSession, PostMenuTests, first_step(), reconcile(), step(), first(), SharedStepRecoveryTests, action() (+3 more)

### Community 8 - "ToolError"
Cohesion: 0.09
Nodes (11): _select_profile_rows(), _selected_profile_names(), start_profile(), start_profiles_together(), _wait_for_selected(), BatchStartTests, checkbox(), toggle() (+3 more)

### Community 9 - "AddressDetailTests"
Cohesion: 0.10
Nodes (9): build_create_address_detail_steps(), _new_prefix(), Tăng số lần thử đọc cây Android và bổ sung phương án dự phòng cho b23–b31 — 19/11/2026, AddressDetailTests, read(), adb(), tap(), read() (+1 more)

### Community 10 - "003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật"
Cohesion: 0.08
Nodes (20): 003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật, Các bước, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Quy trình đích, Rủi ro và bảo trì, Điều kiện dừng (+12 more)

### Community 11 - "Danh mục từng bước đã biết — 13/11/2026"
Cohesion: 0.06
Nodes (35): Bản thử q7 State Machine — 14/11/2026, Chung b10 — Chuyển WhatsApp sang SMS, Chung b11 — Lấy và gõ OTP SMS, Chung b11a — Chạm ô OTP trên màn SMS, Chung b11b — Xác minh đăng nhập hoặc bấm Create của luồng tạo, Chung b4 — Sign In từ menu, Chung b4a — Chạm ô SĐT, Chung b5 — Gõ số điện thoại (+27 more)

### Community 12 - "adb"
Cohesion: 0.06
Nodes (7): adb(), adb(), tap(), adb(), wait(), adb(), tap()

### Community 16 - "Ảnh hướng dẫn q1/q2 và menu chung lưu cục bộ"
Cohesion: 0.07
Nodes (28): B16–b22 chung — Đổi marketplace sang United States (18/11/2026), B32–b39 — Reload Balance, thêm thẻ và địa chỉ thanh toán (21/11/2026), B6 — Hai ảnh đính kèm mới ngày 13/11/2026, Menu chung ảnh 01 — Danh sách chữ, Menu chung ảnh 02 — App Store bên phải sau khi Amazon mở, q1 b6 — US +1 hiện nhưng chạm không đóng hộp, 14/11/2026, q1 ảnh 01 — Menu và ba thẻ, q1 ảnh 02 — Sign In cuối menu (+20 more)

### Community 17 - "open_home_menu"
Cohesion: 0.12
Nodes (12): CloudPhone, reconcile(), route(), _confirm_menu_fallback(), _menu_evidence(), _nodes(), open_home_menu(), _tap() (+4 more)

### Community 18 - "MarketplaceFlowTests"
Cohesion: 0.06
Nodes (27): AttemptDeadline, type_characters(), CountryRecoveryTests, read(), wait(), node(), MarketplaceFlowTests, read() (+19 more)

### Community 19 - "marketplace_flow.py"
Cohesion: 0.19
Nodes (25): _account_tab(), build_marketplace_steps(), run(), account_target(), back_and_read_text(), foreground_ready(), recover_country_list(), _destination() (+17 more)

### Community 20 - "screen"
Cohesion: 0.14
Nodes (27): _at_or_after(), sign_in(), _ensure_menu(), _find_scrolling(), menu_layout(), _read_nodes(), route_list_menu(), _tap() (+19 more)

### Community 21 - "Điều hướng hai dạng menu ba gạch"
Cohesion: 0.50
Nodes (4): Bằng chứng và phạm vi, Kiểm chứng, Quy tắc chạy, Điều hướng hai dạng menu ba gạch

### Community 22 - "Q3Q4FlowTests"
Cohesion: 0.23
Nodes (3): build_q3_steps(), build_q4_steps(), Q3Q4FlowTests

### Community 23 - "core.py"
Cohesion: 0.27
Nodes (19): adb(), available_memory_mb(), check_play(), configure_avd(), connected_devices(), Device, device_avd_name(), device_resources() (+11 more)

### Community 24 - "PostMenuStep"
Cohesion: 0.12
Nodes (9): PostMenuStep, build_q7_pilot_steps(), ResultVerifier, StateDeadline, StateDetector, StateMachineStop, StateMachineTimeout, Q7StateMachineTests (+1 more)

### Community 25 - "Nghiên cứu và tích hợp Swarmote"
Cohesion: 0.40
Nodes (4): Hành vi có bằng chứng, Kiểm thử còn lại, Nghiên cứu và tích hợp Swarmote, Phần đã áp dụng

### Community 26 - "ToolError"
Cohesion: 0.14
Nodes (15): ToolError, _PrefixRecoveryStop, _start_and_confirm(), _activate_manager(), _create_profile_form(), check_stop(), _invoke(), _one() (+7 more)

### Community 27 - "ResumeRegistrationStateTests"
Cohesion: 0.10
Nodes (3): ResumeRegistrationStateTests, factory(), factory()

### Community 28 - "amazon_is_foreground"
Cohesion: 0.16
Nodes (3): amazon_is_foreground(), CloudBridgeTests, adb()

### Community 29 - "Window"
Cohesion: 0.10
Nodes (6): state_style(), status_title(), Window, Trạng thái kiểm chứng và giới hạn, __init__(), __init__()

### Community 30 - "RegistrationState"
Cohesion: 0.08
Nodes (9): RegistrationState, build_tail_steps(), open_menu(), view(), visit_seconds(), Mã hiện có, RandomPrefixTests, continuation() (+1 more)

### Community 31 - "PROJECT_INDEX.md"
Cohesion: 0.16
Nodes (8): Quy trình Swarmote hiện tại, Luồng q1 từ menu ba gạch tới nhập OTP, Thử trên q1 đã có, Luồng q2 từ menu ba gạch, q3 — b1–b3 và nối luồng chung, q4 — Giỏ hàng, Pets, Home and DIY, q5 — ba thẻ riêng và b4–b11 chung, q6 — Trang chủ, Giỏ hàng, menu và một thẻ

### Community 32 - "build_random_steps"
Cohesion: 0.11
Nodes (4): RandomPrefixTests, adb(), adb(), adb()

### Community 33 - "ui_backend.py"
Cohesion: 0.12
Nodes (13): cloud_serials(), swarmote_adb_path(), swarmote_tunnel_owner(), _connect(), country_reverse_points(), country_scroll(), _failed(), read_tree() (+5 more)

### Community 34 - "vision.py"
Cohesion: 0.13
Nodes (9): _bounds(), _canonical_text(), _compact(), _field_contents(), _field_is_blank(), _join_wrapped_categories(), _normalize(), ocr_nodes() (+1 more)

### Community 35 - "subprocess"
Cohesion: 0.12
Nodes (17): save(), AppSettings, load_settings(), save_settings(), settings_path(), check_runtime(), main(), verify() (+9 more)

### Community 36 - "_visible"
Cohesion: 0.16
Nodes (30): _bounds(), _scroll_up(), _text(), _visible(), _action(), _address_form(), _addresses(), _bounded_native() (+22 more)

### Community 37 - "setup.py"
Cohesion: 0.18
Nodes (13): app_data_dir(), avd_names(), create_avd(), doctor(), executable(), installed_image(), run(), sdk_root() (+5 more)

### Community 38 - "_type_field"
Cohesion: 0.19
Nodes (4): enter_otp(), _type_field(), FlowRecoveryTests, form()

### Community 39 - "build_create_address_steps"
Cohesion: 0.24
Nodes (4): build_create_address_steps(), CreateAddressFlowTests, read(), node()

### Community 40 - ".remaining"
Cohesion: 0.08
Nodes (19): _read_hierarchy(), _read_login_sms_visual(), _read_nodes_once(), _read_visual_nodes(), _UiReadIncomplete, browse(), action(), read_menu() (+11 more)

### Community 41 - "cli.py"
Cohesion: 0.11
Nodes (13): BatchItem, parse_proxy_line(), prepare_five(), BulkRecord, lines(), _proxy_rows(), _url_from_cell(), create_profile() (+5 more)

### Community 42 - "Bàn giao trạng thái dự án — 13/11/2026"
Cohesion: 0.11
Nodes (16): set_tk_icon(), B6 danh sách quốc gia vẫn mở sau khi chọn — 13/11/2026, Bàn giao trạng thái dự án — 13/11/2026, Bản chính boom4may và bản dự phòng — 14/11/2026, Bộ cài offline chia sẻ — 14/11/2026, Cài đặt máy mới, Dừng riêng máy đang chọn — 14/11/2026, q3/q4 đã nối b1–b3 và thử đồng thời bốn luồng — 13/11/2026 (+8 more)

### Community 43 - "q7_random_prefix.py"
Cohesion: 0.12
Nodes (20): scroll_view(), wait_until(), RecoverableStepError, build_random_steps(), browse(), action(), run_browse(), finish_view() (+12 more)

### Community 44 - "FakeControl"
Cohesion: 0.13
Nodes (5): ParallelInstallTests, PhoneWindow, FakeControl, InstallTests, descendants()

### Community 45 - "desktop_theme.py"
Cohesion: 0.09
Nodes (9): Button, Entry, FooterNote, icon(), StatusCell, TableText, Tooltip, ui_font() (+1 more)

### Community 46 - "swarmote_desktop.py"
Cohesion: 0.12
Nodes (13): open_amazon(), package_path(), probe(), require_online(), _profile_row_status(), ProfileCreateNotSubmitted, ProfileLookupError, ProfileManagerWindowError (+5 more)

### Community 47 - "cloud_adb"
Cohesion: 0.14
Nodes (21): _keyboard_visible(), _resume_address_payment_index(), cloud_adb(), foreground(), prop(), reported_installer(), _account_content(), run() (+13 more)

### Community 48 - "phone_window_layout.py"
Cohesion: 0.13
Nodes (5): arrange_on_open(), _row_if_fits(), _sort_key(), _tiles(), PhoneWindowLayoutTests

### Community 49 - "cli.py"
Cohesion: 0.20
Nodes (10): _table_cells(), main(), parser(), report(), scan(), get_device(), print_json(), Store (+2 more)

### Community 51 - "b1–b11 Reliability and Latency Implementation Plan"
Cohesion: 0.18
Nodes (10): b1–b11 Reliability and Latency Implementation Plan, Completion Criteria, File Map, Global Constraints, Review Focus, Task 1: Measure current step latency and classify existing failures, Task 2: Define safe retry, reconcile, pause, and stop behavior, Task 3: Reduce redundant UI reads and unnecessary waits (+2 more)

### Community 52 - "VisionFieldTests"
Cohesion: 0.21
Nodes (4): _input_box(), _single_input_border(), detection(), VisionFieldTests

### Community 53 - "Danh mục ảnh nằm trong dự án"
Cohesion: 0.18
Nodes (11): amazon_android/assets/icons/, amazon_android/assets/obsidian_prism.png, amazon_android/assets/swarmote_tool_square.png và swarmote_tool.ico, assets/ui_history/machine7_input_before.png, assets/ui_history/reset_check.png, assets/ui_history/ui-12.png, assets/ui_history/ui_palette_preview.png, assets/ui_history/ui-preview.png (+3 more)

### Community 55 - "Amazon Android Tool — Giai đoạn A/B"
Cohesion: 0.29
Nodes (7): Amazon Android Tool — Giai đoạn A/B, Cài trên máy Windows mới, Dán nhiều proxy, Sử dụng, Trạng thái nghiệm thu, Yêu cầu, Điện thoại đám mây Swarmote

### Community 56 - "desktop.py"
Cohesion: 0.12
Nodes (3): _automatic_resume_slots(), startup_geometry(), on_worker()

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
Nodes (25): b6 Country US +1 — 14/11/2026, B6 cuộn quốc gia và chọn lại — 13/11/2026, Biên bản kiểm tra thực tế — 2026-11-12, Cài và đo UiAutomator2 theo phê duyệt mới — 13/11/2026, Cập nhật luồng mẻ trước đó — 2026-11-13, Dừng riêng một máy — 14/11/2026, Focus ô nhập b4–b11 — 14/11/2026, Ghim taskbar — 13/11/2026 (+17 more)

### Community 62 - "build_reload_payment_steps"
Cohesion: 0.13
Nodes (9): build_reload_payment_steps(), node(), ReloadPaymentTests, adb(), wait(), read(), read(), read() (+1 more)

### Community 63 - "Bộ cài chia sẻ Windows x64"
Cohesion: 0.50
Nodes (3): Bộ cài chia sẻ Windows x64, Dựng lại, Nguồn thành phần

### Community 64 - "SmoothScrollableFrame"
Cohesion: 0.15
Nodes (3): animations_enabled(), SmoothScrollableFrame, DesktopScrollTests

### Community 65 - "test_isolated_reader.py"
Cohesion: 0.20
Nodes (8): phone_reader(), PhoneReader, ReaderResponseError, _serve(), fake_worker(), IsolationTests, duplicate(), production_worker_with_fake_android()

### Community 66 - "VERIFICATION.md"
Cohesion: 0.17
Nodes (10): Kết luận và tích hợp, Kết quả thực tế, So sánh bộ đọc trên q1 — 13/11/2026, Thành phần thiết bị, b1–b3 bắt buộc có ba cú bấm — 14/11/2026, b1–b3 ngẫu nhiên cho 12 máy — 14/11/2026, b1–b3 ngẫu nhiên trên 12 máy, không dùng OCR — 14/11/2026, b6 cuộn tới đáy rồi vuốt ngược — 14/11/2026 (+2 more)

### Community 68 - "_prepare_phone"
Cohesion: 0.18
Nodes (13): _phone_preparation_lock(), _prepare_phone(), _prepare_phone_locked(), progress(), stop_here(), run_batch(), fill_slots(), manually_selected() (+5 more)

### Community 69 - ".stop"
Cohesion: 0.20
Nodes (3): current(), Dự phòng dùng chung khi chạy song song — 14/11/2026, install()

### Community 70 - "ExtendedRecoveryTests"
Cohesion: 0.15
Nodes (7): MenuReadUnavailable, budget(), ExtendedRecoveryTests, fail(), read(), read(), menu()

### Community 71 - "PROJECT_HANDOFF.md"
Cohesion: 0.09
Nodes (20): visit(), Nối vào bước tạo tài khoản sau khi xác minh màn hình Amazon, Thiết kế OTP cho từng Profile, Đã chuẩn bị, b1–b3 ngẫu nhiên cho q1–q12 — 14/11/2026, B4–b11 chạy đồng thời và OCR — 14/11/2026, b6 US +1 còn mở sau bốn cú chạm — 14/11/2026, Bản thử State Machine q7 và b1–b3 mở mục con — 14/11/2026 (+12 more)

### Community 72 - "build_post_auth_steps"
Cohesion: 0.18
Nodes (11): Hướng dẫn khi tiếp tục dự án, build_post_auth_steps(), Nhận diện giao diện lúc chạy, Nhập liệu và lỗi, Quy tắc tự động hóa sau menu ba gạch, Trạng thái hiện tại của dự án, Từng máy độc lập, Bản đồ repository (+3 more)

### Community 73 - "._continue_profile"
Cohesion: 0.14
Nodes (3): validate_card(), otp_token(), validate_otp_url()

### Community 74 - "ProxyConfig"
Cohesion: 0.10
Nodes (12): visible_lookup(), _open_profiles(), profile_status(), _unfiltered_single_page(), visible_profile_names(), control(), ProfilesNavigationTests, descendants() (+4 more)

### Community 75 - "account_flow.py"
Cohesion: 0.07
Nodes (47): _ActionNotResolved, confirmed_login_otp_nodes(), continue_number(), country(), finish_auto(), finish_create(), finish_login(), focus_otp() (+39 more)

### Community 76 - "_choose_tail_target"
Cohesion: 0.22
Nodes (5): _choose_tail_target(), _TailChoicesExhausted, Đồng bộ cơ chế chờ thẻ con tải, tối đa 10s tự Back, 12 máy ngẫu nhiên độc lập cho cả 2 luồng — 19/11/2026, choose(), choose()

### Community 77 - "main"
Cohesion: 0.31
Nodes (3): main(), main(), LauncherTests

### Community 78 - "StateSpec"
Cohesion: 0.60
Nodes (3): _already_reached_result(), _past_known_step(), StateSpec

### Community 82 - "._run"
Cohesion: 0.22
Nodes (7): 002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ, Các bước, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Rủi ro và bảo trì, Điều kiện dừng

### Community 83 - "RunJob"
Cohesion: 0.08
Nodes (12): emit(), _first_point(), AccountData, retry_preparation(), RunJob, P03 — Mở form New Profile, DesktopResumeTests, apartment_type() (+4 more)

### Community 85 - "ensure_manager_ready"
Cohesion: 0.21
Nodes (6): ensure_manager_ready(), inspect(), _main_window(), collect(), _swarmote_exe(), ManagerStartupTests

### Community 87 - "Giai đoạn 2 — bản thử State Machine riêng q7"
Cohesion: 0.50
Nodes (4): Cách thử bản pilot cũ (không áp dụng cho factory hiện hành), Giai đoạn 2 — bản thử State Machine riêng q7, Giới hạn, Sơ đồ

### Community 91 - "_proxy_postal_prefix"
Cohesion: 0.48
Nodes (3): _proxy_postal_prefix(), controls(), ProxyPostalPrefixTests

### Community 92 - "GRAPH_AUDIT.md"
Cohesion: 0.50
Nodes (3): Cách kiểm tra sau mỗi sửa đổi, Giới hạn đã xác nhận, Kiểm tra độ phủ Graphify — cập nhật 26/11/2026

### Community 93 - "._apply_bulk_text"
Cohesion: 0.14
Nodes (8): 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng, Các bước, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Rủi ro và bảo trì, Thiết kế yêu cầu, Điều kiện dừng

### Community 94 - "File dự án mà Graphify không phân tích trực tiếp"
Cohesion: 0.40
Nodes (5): File dự án mà Graphify không phân tích trực tiếp, .gitignore, Launch Swarmote Tool.pyw, pyproject.toml, Ảnh PNG trong dự án

## Knowledge Gaps
- **1 isolated node(s):** `amazon-android-tool`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 558 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **11 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ToolError` connect `ToolError` to `registration.py`, `build_common_steps`, `otp.py`, `BulkInputTests`, `swarmote_desktop.py`, `RunnerTests`, `PostMenuStep`, `ToolError`, `AddressDetailTests`, `adb`, `StopResetTests`, `cloud.py`, `open_home_menu`, `MarketplaceFlowTests`, `marketplace_flow.py`, `screen`, `core.py`, `PostMenuStep`, `ResumeRegistrationStateTests`, `amazon_is_foreground`, `Window`, `RegistrationState`, `build_random_steps`, `ui_backend.py`, `vision.py`, `subprocess`, `_visible`, `setup.py`, `_type_field`, `build_create_address_steps`, `.remaining`, `cli.py`, `q7_random_prefix.py`, `swarmote_desktop.py`, `cloud_adb`, `cli.py`, `.test_b10_stalled_whatsapp_pauses_only_affected_phone`, `desktop.py`, `_recognize`, `build_reload_payment_steps`, `test_isolated_reader.py`, `BatchDraft`, `_prepare_phone`, `.stop`, `ExtendedRecoveryTests`, `PROJECT_HANDOFF.md`, `._continue_profile`, `ProxyConfig`, `account_flow.py`, `_choose_tail_target`, `._run`, `RunJob`, `ensure_manager_ready`, `._apply_bulk_text`?**
  _High betweenness centrality (0.346) - this node is a cross-community bridge._
- **Are the 58 inferred relationships involving `ToolError` (e.g. with `_read_nodes_once()` and `_resume_address_payment_index()`) actually correct?**
  _`ToolError` has 58 INFERRED edges - model-reasoned connections that need verification._
- **What connects `amazon-android-tool` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `build_common_steps` be split into smaller, more focused modules?**
  _Cohesion score 0.0519219736087206 - nodes in this community are weakly interconnected._
- **Why does `CloudPhone` connect `open_home_menu` to `registration.py`, `build_common_steps`, `swarmote_desktop.py`, `PostMenuStep`, `AddressDetailTests`, `adb`, `cloud.py`, `MarketplaceFlowTests`, `screen`, `Q3Q4FlowTests`, `PostMenuStep`, `ToolError`, `ResumeRegistrationStateTests`, `amazon_is_foreground`, `Window`, `RegistrationState`, `build_random_steps`, `ui_backend.py`, `_visible`, `_type_field`, `build_create_address_steps`, `.remaining`, `cli.py`, `q7_random_prefix.py`, `swarmote_desktop.py`, `cloud_adb`, `cli.py`, `.test_b10_stalled_whatsapp_pauses_only_affected_phone`, `desktop.py`, `build_reload_payment_steps`, `test_isolated_reader.py`, `_prepare_phone`, `.stop`, `ExtendedRecoveryTests`, `build_post_auth_steps`, `._continue_profile`, `ProxyConfig`, `account_flow.py`, `RunJob`, `test_q5_flow.py`, `MenuReturnTests`?**
  _High betweenness centrality (0.115) - this node is a cross-community bridge._
- **Are the 88 inferred relationships involving `CloudPhone` (e.g. with `build_common_steps()` and `_country_full_row()`) actually correct?**
  _`CloudPhone` has 88 INFERRED edges - model-reasoned connections that need verification._
- **Should `otp.py` be split into smaller, more focused modules?**
  _Cohesion score 0.10114942528735632 - nodes in this community are weakly interconnected._