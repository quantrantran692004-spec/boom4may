# Graph Report - boom4may  (2026-11-28)

## Corpus Check
- 140 files · ~182,484 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 2, .bat 1, .pyw 1)

## Summary
- 2375 nodes · 8328 edges · 91 communities (81 shown, 10 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 1187 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `35666e87`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- AttemptDeadline
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
- screen
- RunJob
- amazon-android-tool
- Ảnh hướng dẫn q1/q2 và menu chung lưu cục bộ
- profile_status
- MarketplaceFlowTests
- CloudPhone
- ._start_post_menu
- MENU_ROUTING.md
- Q3Q4FlowTests
- build_change_us_steps
- Q7StateMachineTests
- Nghiên cứu và tích hợp Swarmote
- _tail_menu
- settings
- phone_window_layout.py
- resume_common_index
- build_random_steps
- PROJECT_INDEX.md
- build_random_steps
- ui_backend.py
- VisionFieldTests
- desktop.py
- _visible
- swarmote_desktop.py
- _type_field
- build_create_address_steps
- _find_scrolling
- .test_transition_keeps_observing_after_short_wait_without_tapping
- _read_nodes
- .test_manual_otp_repair_continues_with_confirmation_and_tail_for_both_modes
- FakeControl
- ._build_main
- Window
- ._refresh_devices
- test_q1_flow.py
- CountryRecoveryTests
- ProxyConfig
- b1–b11 Reliability and Latency Implementation Plan
- vision.py
- Danh mục ảnh nằm trong dự án
- PostMenuStep
- Amazon Android Tool — Giai đoạn A/B
- AppSettings
- core.py
- RecoverableStepError
- q7_random_prefix.py
- Amazon trên Swarmote
- Biên bản kiểm tra thực tế — 2026-11-12
- build_reload_payment_steps
- Bộ cài chia sẻ Windows x64
- SmoothScrollableFrame
- _recognize
- VERIFICATION.md
- ._apply_bulk_text
- runner.py
- time
- .test_login_otp_uses_visual_readback_then_verify_without_retyping
- PROJECT_HANDOFF.md
- ExtendedRecoveryTests
- File dự án mà Graphify không phân tích trực tiếp
- ProfilesNavigationTests
- .test_missing_target_fallback_backs_then_uses_fresh_locale_text_on_all_modes_and_slots
- _CombinedStop
- HeaderWave
- StatusCell
- main
- RunJob
- Bàn giao trạng thái dự án — 13/11/2026
- RegistrationState
- _nodes
- _proxy_postal_prefix
- .test_both_modes_and_all_slots_share_one_continuation_extension_point
- GRAPH_AUDIT.md
- cloud_adb
- OTP_DESIGN.md

## God Nodes (most connected - your core abstractions)
1. `ToolError` - 364 edges
2. `CloudPhone` - 238 edges
3. `AttemptDeadline` - 227 edges
4. `RunJob` - 175 edges
5. `RegistrationState` - 166 edges
6. `build_common_steps()` - 115 edges
7. `Window` - 110 edges
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

## Communities (91 total, 10 thin omitted)

### Community 0 - "AttemptDeadline"
Cohesion: 0.11
Nodes (5): AttemptDeadline, type_characters(), ChangeUsFlowTests, node(), MenuReturnTests

### Community 1 - "build_common_steps"
Cohesion: 0.08
Nodes (4): build_common_steps(), node(), Q1FlowTests, provider_read()

### Community 2 - "otp.py"
Cohesion: 0.10
Nodes (8): browser_launch_options(), extract_otp(), _NoRedirect, read_otp(), _read_otp_in_browser(), wait_for_new_otp(), OtpTests, PackagedBrowserTests

### Community 3 - "BulkInputTests"
Cohesion: 0.06
Nodes (6): BatchDraft, parse_column(), parse_records(), BatchDraftTests, BulkInputTests, Value

### Community 4 - "windows_identity.py"
Cohesion: 0.17
Nodes (6): create_shortcut(), relaunch_command(), runtime(), set_process_identity(), set_window_identity(), WindowsIdentityTests

### Community 5 - "swarmote_desktop.py"
Cohesion: 0.09
Nodes (28): ready_for_home_menu(), _check_stop(), install_amazon(), open_adb_shell(), _pause(), _phone_window(), _progress_reporter(), report() (+20 more)

### Community 6 - "RunnerTests"
Cohesion: 0.05
Nodes (19): ProfileRegistry, absent(), ProfileRegistryTests, lookup(), broken(), RunnerTests, create(), resume() (+11 more)

### Community 7 - "PostMenuStep"
Cohesion: 0.09
Nodes (9): route(), PostMenuSession, Bỏ thời hạn tổng sau menu — 14/11/2026, Không bỏ qua b1–b3 ngẫu nhiên; 14 ảnh menu mới — 14/11/2026, PostMenuTests, first_step(), reconcile(), step() (+1 more)

### Community 8 - "ToolError"
Cohesion: 0.11
Nodes (5): checkbox(), toggle(), descendants(), FakeBox, FakeButton

### Community 9 - "AddressDetailTests"
Cohesion: 0.10
Nodes (9): build_create_address_detail_steps(), _new_prefix(), Tăng số lần thử đọc cây Android và bổ sung phương án dự phòng cho b23–b31 — 19/11/2026, AddressDetailTests, read(), adb(), tap(), read() (+1 more)

### Community 10 - "003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật"
Cohesion: 0.08
Nodes (20): 003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật, Các bước, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Quy trình đích, Rủi ro và bảo trì, Điều kiện dừng (+12 more)

### Community 11 - "Danh mục từng bước đã biết — 13/11/2026"
Cohesion: 0.05
Nodes (37): B1–B3 hiện hành — Ba lượt ngẫu nhiên q1–q12, Bản thử q7 State Machine — 14/11/2026, Chung b10 — Chuyển WhatsApp sang SMS, Chung b11 — Lấy và gõ OTP SMS, Chung b11a — Chạm ô OTP trên màn SMS, Chung b11b — Xác minh đăng nhập hoặc bấm Create của luồng tạo, Chung b16–b22 — Tài khoản và marketplace United States, Chung b4 — Sign In từ menu (+29 more)

### Community 12 - "screen"
Cohesion: 0.13
Nodes (31): _ActionNotResolved, confirmed_login_otp_nodes(), continue_number(), country(), finish_auto(), finish_create(), finish_login(), focus_phone() (+23 more)

### Community 16 - "Ảnh hướng dẫn q1/q2 và menu chung lưu cục bộ"
Cohesion: 0.07
Nodes (29): 14 ảnh menu chung b1–b3 ngẫu nhiên — 14/11/2026, B16–b22 chung — Đổi marketplace sang United States (18/11/2026), B32–b39 — Reload Balance, thêm thẻ và địa chỉ thanh toán (21/11/2026), B6 — Hai ảnh đính kèm mới ngày 13/11/2026, Menu chung ảnh 01 — Danh sách chữ, Menu chung ảnh 02 — App Store bên phải sau khi Amazon mở, q1 b6 — US +1 hiện nhưng chạm không đóng hộp, 14/11/2026, q1 ảnh 01 — Menu và ba thẻ (+21 more)

### Community 17 - "profile_status"
Cohesion: 0.11
Nodes (15): verify_menu_open(), visible_lookup(), _profile_row_status(), profile_status(), ProfileLookupError, ProfileNotFound, 002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ, Các bước (+7 more)

### Community 18 - "MarketplaceFlowTests"
Cohesion: 0.15
Nodes (7): MarketplaceFlowTests, read(), pause(), read(), tap_action(), read(), node()

### Community 19 - "CloudPhone"
Cohesion: 0.06
Nodes (24): amazon_is_foreground(), cloud_serials(), CloudPhone, package_path(), probe(), prop(), reported_installer(), scan() (+16 more)

### Community 20 - "._start_post_menu"
Cohesion: 0.16
Nodes (3): otp_token(), validate_otp_url(), Dán bảng Amazon có ghi chú thẻ live và URL OTP escaped — 14/11/2026

### Community 21 - "MENU_ROUTING.md"
Cohesion: 0.23
Nodes (7): Bằng chứng và phạm vi, Kiểm chứng, Quy tắc chạy, Điều hướng hai dạng menu ba gạch, Luồng q1 từ menu ba gạch tới nhập OTP, Thử trên q1 đã có, Luồng q2 từ menu ba gạch

### Community 22 - "Q3Q4FlowTests"
Cohesion: 0.23
Nodes (3): build_q3_steps(), build_q4_steps(), Q3Q4FlowTests

### Community 23 - "build_change_us_steps"
Cohesion: 0.13
Nodes (41): _after_back(), _browse(), build_change_us_steps(), account(), b1(), b10(), b11(), b12() (+33 more)

### Community 24 - "Q7StateMachineTests"
Cohesion: 0.11
Nodes (17): _menu(), ActionValidator, _already_reached_result(), _browse_ready_after_sms(), run(), _past_known_step(), RecoveryHandler, ResultVerifier (+9 more)

### Community 25 - "Nghiên cứu và tích hợp Swarmote"
Cohesion: 0.40
Nodes (4): Hành vi có bằng chứng, Kiểm thử còn lại, Nghiên cứu và tích hợp Swarmote, Phần đã áp dụng

### Community 26 - "_tail_menu"
Cohesion: 0.17
Nodes (23): _account_icon_from_image(), _person(), _account_tab(), build_marketplace_steps(), run(), account_target(), back_and_read_text(), foreground_ready() (+15 more)

### Community 27 - "settings"
Cohesion: 0.10
Nodes (11): read(), adb(), read(), tap(), read(), read(), read(), read() (+3 more)

### Community 28 - "phone_window_layout.py"
Cohesion: 0.13
Nodes (5): arrange_on_open(), _row_if_fits(), _sort_key(), _tiles(), PhoneWindowLayoutTests

### Community 29 - "resume_common_index"
Cohesion: 0.10
Nodes (5): resume_common_index(), reconcile(), ResumeRegistrationStateTests, factory(), factory()

### Community 30 - "build_random_steps"
Cohesion: 0.05
Nodes (19): Hướng dẫn khi tiếp tục dự án, build_post_auth_steps(), build_random_steps(), browse(), finish_view(), Nhận diện giao diện lúc chạy, Nhập liệu và lỗi, Quy tắc tự động hóa sau menu ba gạch (+11 more)

### Community 31 - "PROJECT_INDEX.md"
Cohesion: 0.18
Nodes (6): Quy trình Swarmote hiện tại, Bản đồ repository, q3 — b1–b3 và nối luồng chung, q4 — Giỏ hàng, Pets, Home and DIY, q5 — ba thẻ riêng và b4–b11 chung, q6 — Trang chủ, Giỏ hàng, menu và một thẻ

### Community 32 - "build_random_steps"
Cohesion: 0.11
Nodes (4): RandomPrefixTests, adb(), adb(), adb()

### Community 33 - "ui_backend.py"
Cohesion: 0.08
Nodes (19): swarmote_adb_path(), swarmote_tunnel_owner(), phone_reader(), PhoneReader, ReaderResponseError, _serve(), _connect(), country_reverse_points() (+11 more)

### Community 34 - "VisionFieldTests"
Cohesion: 0.21
Nodes (4): _input_box(), _single_input_border(), detection(), VisionFieldTests

### Community 35 - "desktop.py"
Cohesion: 0.17
Nodes (3): _automatic_resume_slots(), startup_geometry(), status_title()

### Community 36 - "_visible"
Cohesion: 0.11
Nodes (36): _bounds(), _country_full_row(), _resume_address_payment_index(), _same_country_position(), _text(), _visible(), _menu_visible(), _action() (+28 more)

### Community 37 - "swarmote_desktop.py"
Cohesion: 0.12
Nodes (22): require_online(), ToolError, collapse_apps_panel(), _descendants(), check_stop(), _main_window(), collect(), _one() (+14 more)

### Community 38 - "_type_field"
Cohesion: 0.13
Nodes (7): enter_otp(), focus_otp(), _tap_input(), _type_field(), Phục hồi khi ô nhập chưa nhận focus ở b4–b11 — 14/11/2026, FlowRecoveryTests, form()

### Community 39 - "build_create_address_steps"
Cohesion: 0.24
Nodes (4): build_create_address_steps(), CreateAddressFlowTests, read(), node()

### Community 40 - "_find_scrolling"
Cohesion: 0.11
Nodes (4): _country_nodes(), _CountryReadStop, _find_scrolling(), b6 cuộn chạm đáy rồi vuốt ngược nhẹ tìm US +1 — 14/11/2026

### Community 42 - "_read_nodes"
Cohesion: 0.15
Nodes (24): _at_or_after(), sign_in(), _ensure_menu(), home_visible(), _read_nodes(), _unique(), visit_home(), cart_action() (+16 more)

### Community 43 - ".test_manual_otp_repair_continues_with_confirmation_and_tail_for_both_modes"
Cohesion: 0.18
Nodes (5): Cách thử bản pilot cũ (không áp dụng cho factory hiện hành), Giai đoạn 2 — bản thử State Machine riêng q7, Giới hạn, Phạm vi và quan hệ với luồng cũ, Sơ đồ

### Community 44 - "FakeControl"
Cohesion: 0.13
Nodes (5): ParallelInstallTests, PhoneWindow, FakeControl, InstallTests, descendants()

### Community 45 - "._build_main"
Cohesion: 0.30
Nodes (5): Button, Entry, icon(), ui_font(), section_heading()

### Community 46 - "Window"
Cohesion: 0.13
Nodes (3): FooterNote, Window, PreparationProgressTests

### Community 47 - "._refresh_devices"
Cohesion: 0.16
Nodes (4): state_style(), Trạng thái kiểm chứng và giới hạn, __init__(), __init__()

### Community 48 - "test_q1_flow.py"
Cohesion: 0.10
Nodes (7): menu_layout(), _parse_ui_nodes(), route_list_menu(), _ScreenWaitExpired, build_q1_steps(), category(), Q6FlowTests

### Community 49 - "CountryRecoveryTests"
Cohesion: 0.27
Nodes (4): CountryRecoveryTests, read(), wait(), node()

### Community 50 - "ProxyConfig"
Cohesion: 0.07
Nodes (19): BatchItem, parse_proxy_line(), prepare_five(), BulkRecord, lines(), _markdown_cell_text(), parse_bulk_payload(), _proxy_rows() (+11 more)

### Community 51 - "b1–b11 Reliability and Latency Implementation Plan"
Cohesion: 0.18
Nodes (10): b1–b11 Reliability and Latency Implementation Plan, Completion Criteria, File Map, Global Constraints, Review Focus, Task 1: Measure current step latency and classify existing failures, Task 2: Define safe retry, reconcile, pause, and stop behavior, Task 3: Reduce redundant UI reads and unnecessary waits (+2 more)

### Community 52 - "vision.py"
Cohesion: 0.13
Nodes (9): _bounds(), _canonical_text(), _compact(), _field_contents(), _field_is_blank(), _join_wrapped_categories(), _normalize(), ocr_nodes() (+1 more)

### Community 53 - "Danh mục ảnh nằm trong dự án"
Cohesion: 0.18
Nodes (11): amazon_android/assets/icons/, amazon_android/assets/obsidian_prism.png, amazon_android/assets/swarmote_tool_square.png và swarmote_tool.ico, assets/ui_history/machine7_input_before.png, assets/ui_history/reset_check.png, assets/ui_history/ui-12.png, assets/ui_history/ui_palette_preview.png, assets/ui_history/ui-preview.png (+3 more)

### Community 54 - "PostMenuStep"
Cohesion: 0.26
Nodes (3): PostMenuStep, build_q7_pilot_steps(), Q7StateMachineTests

### Community 55 - "Amazon Android Tool — Giai đoạn A/B"
Cohesion: 0.29
Nodes (7): Amazon Android Tool — Giai đoạn A/B, Cài trên máy Windows mới, Dán nhiều proxy, Sử dụng, Trạng thái nghiệm thu, Yêu cầu, Điện thoại đám mây Swarmote

### Community 56 - "AppSettings"
Cohesion: 0.19
Nodes (6): default_path(), AppSettings, load_settings(), save_settings(), settings_path(), SettingsTests

### Community 57 - "core.py"
Cohesion: 0.06
Nodes (51): main(), parser(), report(), adb(), app_data_dir(), available_memory_mb(), avd_names(), check_play() (+43 more)

### Community 58 - "RecoverableStepError"
Cohesion: 0.19
Nodes (9): RecoverableStepError, build_random_steps(), sign_in(), _size(), SharedStepRecoveryTests, action(), action(), action() (+1 more)

### Community 59 - "q7_random_prefix.py"
Cohesion: 0.20
Nodes (7): browse(), action(), run_browse(), _first_point(), PrefixDeadline, Q7PrefixTimeout, _tap_child()

### Community 60 - "Amazon trên Swarmote"
Cohesion: 0.33
Nodes (5): Amazon trên Swarmote, Người dùng và công việc, Nền tảng, Điều chưa xác minh, Định hướng ngôn ngữ nếu xây dựng lại — 23/11/2026

### Community 61 - "Biên bản kiểm tra thực tế — 2026-11-12"
Cohesion: 0.08
Nodes (24): b6 Country US +1 — 14/11/2026, B6 cuộn quốc gia và chọn lại — 13/11/2026, Biên bản kiểm tra thực tế — 2026-11-12, Cài và đo UiAutomator2 theo phê duyệt mới — 13/11/2026, Dừng riêng một máy — 14/11/2026, Focus ô nhập b4–b11 — 14/11/2026, Ghim taskbar — 13/11/2026, Giao diện sáng, dễ đọc — 2026-11-13 (+16 more)

### Community 62 - "build_reload_payment_steps"
Cohesion: 0.13
Nodes (9): build_reload_payment_steps(), node(), ReloadPaymentTests, adb(), wait(), read(), read(), read() (+1 more)

### Community 63 - "Bộ cài chia sẻ Windows x64"
Cohesion: 0.50
Nodes (3): Bộ cài chia sẻ Windows x64, Dựng lại, Nguồn thành phần

### Community 64 - "SmoothScrollableFrame"
Cohesion: 0.08
Nodes (14): animations_enabled(), SmoothScrollableFrame, Bố cục, Bố cục được áp dụng, Chữ và tiến độ, Giao diện vận hành, Hướng thị giác, Kiểm chứng và phạm vi (+6 more)

### Community 65 - "_recognize"
Cohesion: 0.21
Nodes (6): _engine(), _recognize(), check(), ParallelOcrTests, engine(), read()

### Community 66 - "VERIFICATION.md"
Cohesion: 0.17
Nodes (10): Kết luận và tích hợp, Kết quả thực tế, So sánh bộ đọc trên q1 — 13/11/2026, Thành phần thiết bị, b1–b3 bắt buộc có ba cú bấm — 14/11/2026, b1–b3 ngẫu nhiên cho 12 máy — 14/11/2026, b1–b3 ngẫu nhiên trên 12 máy, không dùng OCR — 14/11/2026, b6 cuộn tới đáy rồi vuốt ngược — 14/11/2026 (+2 more)

### Community 67 - "._apply_bulk_text"
Cohesion: 0.15
Nodes (8): 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng, Các bước, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Rủi ro và bảo trì, Thiết kế yêu cầu, Điều kiện dừng

### Community 68 - "runner.py"
Cohesion: 0.09
Nodes (18): open_amazon(), foreground(), _phone_preparation_lock(), _prepare_phone(), _prepare_phone_locked(), progress(), stop_here(), run_batch() (+10 more)

### Community 69 - "time"
Cohesion: 0.17
Nodes (13): main(), check_runtime(), main(), verify(), _app_installed(), _app_paths(), _check_external_apps(), _install_python_dependencies() (+5 more)

### Community 71 - "PROJECT_HANDOFF.md"
Cohesion: 0.13
Nodes (14): visit(), b1–b3 ngẫu nhiên cho q1–q12 — 14/11/2026, B4–b11 chạy đồng thời và OCR — 14/11/2026, b6 US +1 còn mở sau bốn cú chạm — 14/11/2026, Bản thử State Machine q7 và b1–b3 mở mục con — 14/11/2026, Bổ sung đọc ảnh OCR và chạm trực tiếp dự phòng cho b26 khi uiautomator dump WebView lỗi — 19/11/2026, Cơ chế chụp ảnh OCR quét chữ ấn luôn cho toàn bộ b26–b31 — 19/11/2026, Phạm vi q1–q12 sau phản hồi người dùng — 14/11/2026 (+6 more)

### Community 72 - "ExtendedRecoveryTests"
Cohesion: 0.22
Nodes (5): _start_and_confirm(), Tự phục hồi lỗi tạm thời trong mẻ nhiều máy — 14/11/2026, ExtendedRecoveryTests, fail(), Tự phục hồi lỗi tạm thời trong mẻ nhiều máy — 14/11/2026

### Community 73 - "File dự án mà Graphify không phân tích trực tiếp"
Cohesion: 0.40
Nodes (5): File dự án mà Graphify không phân tích trực tiếp, .gitignore, Launch Swarmote Tool.pyw, pyproject.toml, Ảnh PNG trong dự án

### Community 74 - "ProfilesNavigationTests"
Cohesion: 0.09
Nodes (16): _activate_manager(), _create_profile_form(), _invoke(), _open_profiles(), ProfileCreateNotSubmitted, _proxy_test_country(), ProxyTestFailed, Mã hiện có (+8 more)

### Community 75 - ".test_missing_target_fallback_backs_then_uses_fresh_locale_text_on_all_modes_and_slots"
Cohesion: 0.25
Nodes (3): read(), back(), read()

### Community 79 - "StatusCell"
Cohesion: 0.08
Nodes (5): MachineCell, StatusCell, TableText, Tooltip, DesktopLayoutTests

### Community 80 - "main"
Cohesion: 0.23
Nodes (3): main(), main(), LauncherTests

### Community 83 - "RunJob"
Cohesion: 0.07
Nodes (12): AccountData, retry_preparation(), RunJob, P03 — Mở form New Profile, DesktopResumeTests, apartment_type(), PreparationThreadsTests, run() (+4 more)

### Community 84 - "Bàn giao trạng thái dự án — 13/11/2026"
Cohesion: 0.08
Nodes (19): save(), set_tk_icon(), B6 danh sách quốc gia vẫn mở sau khi chọn — 13/11/2026, Bàn giao trạng thái dự án — 13/11/2026, Bản chính boom4may và bản dự phòng — 14/11/2026, Bộ cài offline chia sẻ — 14/11/2026, Cài đặt máy mới, Dừng riêng máy đang chọn — 14/11/2026 (+11 more)

### Community 87 - "RegistrationState"
Cohesion: 0.08
Nodes (7): RegistrationState, build_tail_steps(), _choose_tail_target(), _TailChoicesExhausted, RandomPrefixTests, choose(), choose()

### Community 88 - "_nodes"
Cohesion: 0.36
Nodes (3): MenuReadUnavailable, _nodes(), budget()

### Community 89 - "_proxy_postal_prefix"
Cohesion: 0.48
Nodes (3): _proxy_postal_prefix(), controls(), ProxyPostalPrefixTests

### Community 92 - "GRAPH_AUDIT.md"
Cohesion: 0.67
Nodes (3): Cách kiểm tra sau mỗi sửa đổi, Giới hạn đã xác nhận, Kiểm tra độ phủ Graphify — cập nhật 26/11/2026

### Community 96 - "cloud_adb"
Cohesion: 0.09
Nodes (40): _keyboard_visible(), _read_hierarchy(), _read_login_sms_visual(), _read_nodes_once(), _read_visual_nodes(), _scroll_up(), _tap(), _UiReadIncomplete (+32 more)

### Community 100 - "OTP_DESIGN.md"
Cohesion: 0.50
Nodes (3): Nối vào bước tạo tài khoản sau khi xác minh màn hình Amazon, Thiết kế OTP cho từng Profile, Đã chuẩn bị

## Knowledge Gaps
- **1 isolated node(s):** `amazon-android-tool`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 582 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **10 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ToolError` connect `swarmote_desktop.py` to `AttemptDeadline`, `build_common_steps`, `otp.py`, `BulkInputTests`, `swarmote_desktop.py`, `RunnerTests`, `PostMenuStep`, `AddressDetailTests`, `screen`, `RunJob`, `desktop.py`, `profile_status`, `MarketplaceFlowTests`, `CloudPhone`, `._start_post_menu`, `build_change_us_steps`, `Q7StateMachineTests`, `_tail_menu`, `resume_common_index`, `build_random_steps`, `build_random_steps`, `ui_backend.py`, `desktop.py`, `_visible`, `_type_field`, `build_create_address_steps`, `_find_scrolling`, `_read_nodes`, `Window`, `._refresh_devices`, `test_q1_flow.py`, `CountryRecoveryTests`, `ProxyConfig`, `vision.py`, `PostMenuStep`, `AppSettings`, `core.py`, `RecoverableStepError`, `q7_random_prefix.py`, `build_reload_payment_steps`, `_recognize`, `._apply_bulk_text`, `runner.py`, `PROJECT_HANDOFF.md`, `ExtendedRecoveryTests`, `ProfilesNavigationTests`, `RunJob`, `RegistrationState`, `_nodes`, `cloud_adb`?**
  _High betweenness centrality (0.347) - this node is a cross-community bridge._
- **Are the 61 inferred relationships involving `ToolError` (e.g. with `_read_nodes_once()` and `_resume_address_payment_index()`) actually correct?**
  _`ToolError` has 61 INFERRED edges - model-reasoned connections that need verification._
- **What connects `amazon-android-tool` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `AttemptDeadline` be split into smaller, more focused modules?**
  _Cohesion score 0.10795454545454546 - nodes in this community are weakly interconnected._
- **Why does `Window` connect `Window` to `BulkInputTests`, `RunnerTests`, `PostMenuStep`, `RunJob`, `desktop.py`, `profile_status`, `CloudPhone`, `._start_post_menu`, `Q3Q4FlowTests`, `resume_common_index`, `build_random_steps`, `desktop.py`, `swarmote_desktop.py`, `._build_main`, `._refresh_devices`, `ProxyConfig`, `PostMenuStep`, `AppSettings`, `core.py`, `SmoothScrollableFrame`, `._apply_bulk_text`, `HeaderWave`, `StatusCell`, `main`, `RunJob`, `Bàn giao trạng thái dự án — 13/11/2026`, `RegistrationState`?**
  _High betweenness centrality (0.102) - this node is a cross-community bridge._
- **Are the 89 inferred relationships involving `CloudPhone` (e.g. with `build_common_steps()` and `_country_full_row()`) actually correct?**
  _`CloudPhone` has 89 INFERRED edges - model-reasoned connections that need verification._
- **Should `build_common_steps` be split into smaller, more focused modules?**
  _Cohesion score 0.08299240210403273 - nodes in this community are weakly interconnected._