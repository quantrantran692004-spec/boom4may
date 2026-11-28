# Graph Report - boom4may  (2026-11-28)

## Corpus Check
- 140 files · ~182,113 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 2, .bat 1, .pyw 1)

## Summary
- 2374 nodes · 8320 edges · 93 communities (73 shown, 20 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 1185 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `46678318`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ToolError
- Q1FlowTests
- otp.py
- BulkInputTests
- desktop.py
- swarmote_desktop.py
- RunnerTests
- PostMenuStep
- ToolError
- AddressDetailTests
- 003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật
- Danh mục từng bước đã biết — 13/11/2026
- build_common_steps
- RunJob
- amazon-android-tool
- Ảnh hướng dẫn q1/q2 và menu chung lưu cục bộ
- profile_status
- AttemptDeadline
- open_home_menu
- ._start_post_menu
- Điều hướng hai dạng menu ba gạch
- Q3Q4FlowTests
- build_change_us_steps
- Q7StateMachineTests
- Nghiên cứu và tích hợp Swarmote
- build_q1_steps
- test_isolated_reader.py
- phone_window_layout.py
- BatchDraft
- RegistrationState
- PROJECT_INDEX.md
- build_random_steps
- ui_backend.py
- cloud_adb
- build_post_auth_steps
- _visible
- .test_b10_stalled_whatsapp_pauses_only_affected_phone
- _type_field
- build_create_address_steps
- parse_column
- ExtendedRecoveryTests
- _read_nodes
- Giai đoạn 2 — bản thử State Machine riêng q7
- FakeControl
- ._build_main
- Window
- ._refresh_devices
- account_flow.py
- CountryRecoveryTests
- bulk_input.py
- b1–b11 Reliability and Latency Implementation Plan
- vision.py
- Danh mục ảnh nằm trong dự án
- ._run
- Amazon Android Tool — Giai đoạn A/B
- AppSettings
- Q2FlowTests
- parse_bulk_payload
- Bàn giao dừng theo yêu cầu người dùng — 13/11/2026
- Amazon trên Swarmote
- Biên bản kiểm tra thực tế — 2026-11-12
- build_reload_payment_steps
- Bộ cài chia sẻ Windows x64
- SmoothScrollableFrame
- Luồng q1 từ menu ba gạch tới nhập OTP
- VERIFICATION.md
- 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng
- run_batch
- time
- DesktopLayoutTests
- PROJECT_HANDOFF.md
- MachineCell
- File dự án mà Graphify không phân tích trực tiếp
- ProfilesNavigationTests
- CloudPhone
- _CombinedStop
- _ScreenWaitExpired
- StatusCell
- main
- MenuReturnTests
- _confirm_menu_fallback
- AccountData
- Bàn giao trạng thái dự án — 13/11/2026
- PLAN.md
- Q5_FLOW.md
- build_random_steps
- _proxy_postal_prefix
- GRAPH_AUDIT.md
- random_prefix.py
- ensure_manager_ready
- OTP_DESIGN.md

## God Nodes (most connected - your core abstractions)
1. `ToolError` - 364 edges
2. `CloudPhone` - 237 edges
3. `AttemptDeadline` - 227 edges
4. `RunJob` - 175 edges
5. `RegistrationState` - 165 edges
6. `build_common_steps()` - 115 edges
7. `Window` - 110 edges
8. `PostMenuStep` - 94 edges
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

## Communities (93 total, 20 thin omitted)

### Community 0 - "ToolError"
Cohesion: 0.06
Nodes (61): BatchItem, parse_proxy_line(), prepare_five(), main(), parser(), report(), adb(), app_data_dir() (+53 more)

### Community 2 - "otp.py"
Cohesion: 0.10
Nodes (9): browser_launch_options(), extract_otp(), _NoRedirect, read_otp(), _read_otp_in_browser(), validate_otp_url(), wait_for_new_otp(), OtpTests (+1 more)

### Community 4 - "desktop.py"
Cohesion: 0.11
Nodes (7): startup_geometry(), create_shortcut(), relaunch_command(), runtime(), set_process_identity(), set_window_identity(), WindowsIdentityTests

### Community 5 - "swarmote_desktop.py"
Cohesion: 0.09
Nodes (31): ready_for_home_menu(), _check_stop(), collapse_apps_panel(), _descendants(), inspect(), install_amazon(), _one(), open_adb_shell() (+23 more)

### Community 6 - "RunnerTests"
Cohesion: 0.06
Nodes (16): ProfileRegistry, absent(), ProfileRegistryTests, RunnerTests, create(), resume(), create(), failed_start() (+8 more)

### Community 7 - "PostMenuStep"
Cohesion: 0.07
Nodes (15): reconcile(), route(), current(), PostMenuSession, PostMenuStep, Dự phòng dùng chung khi chạy song song — 14/11/2026, PostMenuTests, reconcile() (+7 more)

### Community 8 - "ToolError"
Cohesion: 0.09
Nodes (10): _select_profile_rows(), _selected_profile_names(), start_profiles_together(), _wait_for_selected(), BatchStartTests, checkbox(), toggle(), descendants() (+2 more)

### Community 9 - "AddressDetailTests"
Cohesion: 0.12
Nodes (7): build_create_address_detail_steps(), AddressDetailTests, read(), adb(), tap(), read(), item()

### Community 10 - "003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật"
Cohesion: 0.10
Nodes (15): 003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật, Các bước, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Quy trình đích, Rủi ro và bảo trì, Điều kiện dừng (+7 more)

### Community 11 - "Danh mục từng bước đã biết — 13/11/2026"
Cohesion: 0.06
Nodes (35): Bản thử q7 State Machine — 14/11/2026, Chung b10 — Chuyển WhatsApp sang SMS, Chung b11 — Lấy và gõ OTP SMS, Chung b11a — Chạm ô OTP trên màn SMS, Chung b11b — Xác minh đăng nhập hoặc bấm Create của luồng tạo, Chung b4 — Sign In từ menu, Chung b4a — Chạm ô SĐT, Chung b5 — Gõ số điện thoại (+27 more)

### Community 13 - "RunJob"
Cohesion: 0.07
Nodes (6): retry_preparation(), RunJob, P03 — Mở form New Profile, Q5FlowTests, StopResetTests, install()

### Community 16 - "Ảnh hướng dẫn q1/q2 và menu chung lưu cục bộ"
Cohesion: 0.07
Nodes (28): B16–b22 chung — Đổi marketplace sang United States (18/11/2026), B32–b39 — Reload Balance, thêm thẻ và địa chỉ thanh toán (21/11/2026), B6 — Hai ảnh đính kèm mới ngày 13/11/2026, Menu chung ảnh 01 — Danh sách chữ, Menu chung ảnh 02 — App Store bên phải sau khi Amazon mở, q1 b6 — US +1 hiện nhưng chạm không đóng hộp, 14/11/2026, q1 ảnh 01 — Menu và ba thẻ, q1 ảnh 02 — Sign In cuối menu (+20 more)

### Community 17 - "profile_status"
Cohesion: 0.09
Nodes (18): visible_lookup(), _start_and_confirm(), _profile_form_open(), _profile_row_status(), profile_status(), ProfileLookupError, ProfileNotFound, _unfiltered_single_page() (+10 more)

### Community 18 - "AttemptDeadline"
Cohesion: 0.05
Nodes (25): AttemptDeadline, type_characters(), ChangeUsFlowTests, node(), MarketplaceFlowTests, read(), adb(), read() (+17 more)

### Community 19 - "open_home_menu"
Cohesion: 0.10
Nodes (11): MenuReadUnavailable, _nodes(), budget(), open_home_menu(), _tap(), Lỗi chạy song song q3 Terminal trùng / q1 chưa thấy menu — 14/11/2026, HomeMenuTests, ParallelNavigationRegressionTests (+3 more)

### Community 20 - "._start_post_menu"
Cohesion: 0.13
Nodes (3): otp_token(), Dán bảng Amazon có ghi chú thẻ live và URL OTP escaped — 14/11/2026, Trạng thái kiểm chứng và giới hạn

### Community 21 - "Điều hướng hai dạng menu ba gạch"
Cohesion: 0.50
Nodes (4): Bằng chứng và phạm vi, Kiểm chứng, Quy tắc chạy, Điều hướng hai dạng menu ba gạch

### Community 22 - "Q3Q4FlowTests"
Cohesion: 0.23
Nodes (3): build_q3_steps(), build_q4_steps(), Q3Q4FlowTests

### Community 23 - "build_change_us_steps"
Cohesion: 0.09
Nodes (57): confirmed_login_otp_nodes(), continue_number(), enter_otp(), focus_otp(), focus_phone(), read_sms_form(), _button(), _check_summary() (+49 more)

### Community 24 - "Q7StateMachineTests"
Cohesion: 0.08
Nodes (16): ActionValidator, _already_reached_result(), build_q7_pilot_steps(), _past_known_step(), RecoveryHandler, ResultVerifier, StateDeadline, StateDetector (+8 more)

### Community 25 - "Nghiên cứu và tích hợp Swarmote"
Cohesion: 0.40
Nodes (4): Hành vi có bằng chứng, Kiểm thử còn lại, Nghiên cứu và tích hợp Swarmote, Phần đã áp dụng

### Community 27 - "test_isolated_reader.py"
Cohesion: 0.24
Nodes (7): phone_reader(), PhoneReader, ReaderResponseError, fake_worker(), IsolationTests, duplicate(), production_worker_with_fake_android()

### Community 28 - "phone_window_layout.py"
Cohesion: 0.13
Nodes (5): arrange_on_open(), _row_if_fits(), _sort_key(), _tiles(), PhoneWindowLayoutTests

### Community 30 - "RegistrationState"
Cohesion: 0.08
Nodes (9): RegistrationState, build_tail_steps(), open_menu(), view(), visit_seconds(), _choose_tail_target(), RandomPrefixTests, choose() (+1 more)

### Community 31 - "PROJECT_INDEX.md"
Cohesion: 0.23
Nodes (5): Bản đồ repository, Luồng q2 từ menu ba gạch, q3 — b1–b3 và nối luồng chung, q4 — Giỏ hàng, Pets, Home and DIY, q6 — Trang chủ, Giỏ hàng, menu và một thẻ

### Community 32 - "build_random_steps"
Cohesion: 0.11
Nodes (4): RandomPrefixTests, adb(), adb(), adb()

### Community 33 - "ui_backend.py"
Cohesion: 0.13
Nodes (11): swarmote_adb_path(), swarmote_tunnel_owner(), _connect(), country_reverse_points(), country_scroll(), _failed(), read_tree(), ready() (+3 more)

### Community 34 - "cloud_adb"
Cohesion: 0.09
Nodes (29): country(), _country_full_row(), _keyboard_visible(), _scroll_up(), _tap(), cloud_adb(), action(), browse_view() (+21 more)

### Community 35 - "build_post_auth_steps"
Cohesion: 0.20
Nodes (10): Hướng dẫn khi tiếp tục dự án, build_post_auth_steps(), Nhận diện giao diện lúc chạy, Nhập liệu và lỗi, Quy tắc tự động hóa sau menu ba gạch, Trạng thái hiện tại của dự án, Từng máy độc lập, Một quy luật để sửa mã về sau — 20/11/2026 (+2 more)

### Community 36 - "_visible"
Cohesion: 0.10
Nodes (55): _bounds(), _resume_address_payment_index(), _text(), _visible(), _menu_visible(), _action(), _address_form(), _addresses() (+47 more)

### Community 38 - "_type_field"
Cohesion: 0.16
Nodes (4): _type_field(), Phục hồi khi ô nhập chưa nhận focus ở b4–b11 — 14/11/2026, FlowRecoveryTests, form()

### Community 39 - "build_create_address_steps"
Cohesion: 0.24
Nodes (4): build_create_address_steps(), CreateAddressFlowTests, read(), node()

### Community 40 - "parse_column"
Cohesion: 0.20
Nodes (4): lines(), parse_column(), _proxy_rows(), Dán nhiều proxy cách nhau bằng dấu cách — 14/11/2026

### Community 41 - "ExtendedRecoveryTests"
Cohesion: 0.18
Nodes (5): ExtendedRecoveryTests, fail(), read(), read(), menu()

### Community 42 - "_read_nodes"
Cohesion: 0.09
Nodes (43): _at_or_after(), finish_auto(), finish_create(), finish_login(), name(), phone_number(), proceed(), send_sms() (+35 more)

### Community 43 - "Giai đoạn 2 — bản thử State Machine riêng q7"
Cohesion: 0.40
Nodes (5): Cách thử bản pilot cũ (không áp dụng cho factory hiện hành), Giai đoạn 2 — bản thử State Machine riêng q7, Giới hạn, Phạm vi và quan hệ với luồng cũ, Sơ đồ

### Community 44 - "FakeControl"
Cohesion: 0.13
Nodes (5): ParallelInstallTests, PhoneWindow, FakeControl, InstallTests, descendants()

### Community 45 - "._build_main"
Cohesion: 0.18
Nodes (7): Button, Entry, FooterNote, HeaderWave, icon(), ui_font(), section_heading()

### Community 47 - "._refresh_devices"
Cohesion: 0.17
Nodes (3): state_style(), status_title(), Các bước

### Community 48 - "account_flow.py"
Cohesion: 0.12
Nodes (16): _ActionNotResolved, _country_nodes(), _CountryReadStop, _parse_ui_nodes(), _read_hierarchy(), _read_login_sms_visual(), _read_nodes_once(), _read_visual_nodes() (+8 more)

### Community 49 - "CountryRecoveryTests"
Cohesion: 0.27
Nodes (4): CountryRecoveryTests, read(), wait(), node()

### Community 50 - "bulk_input.py"
Cohesion: 0.18
Nodes (6): BulkRecord, _markdown_cell_text(), _table_cells(), _url_from_cell(), validate_card(), _card_parts()

### Community 51 - "b1–b11 Reliability and Latency Implementation Plan"
Cohesion: 0.18
Nodes (10): b1–b11 Reliability and Latency Implementation Plan, Completion Criteria, File Map, Global Constraints, Review Focus, Task 1: Measure current step latency and classify existing failures, Task 2: Define safe retry, reconcile, pause, and stop behavior, Task 3: Reduce redundant UI reads and unnecessary waits (+2 more)

### Community 52 - "vision.py"
Cohesion: 0.07
Nodes (19): _bounds(), _canonical_text(), _compact(), _engine(), _field_contents(), _field_is_blank(), _input_box(), _join_wrapped_categories() (+11 more)

### Community 53 - "Danh mục ảnh nằm trong dự án"
Cohesion: 0.18
Nodes (11): amazon_android/assets/icons/, amazon_android/assets/obsidian_prism.png, amazon_android/assets/swarmote_tool_square.png và swarmote_tool.ico, assets/ui_history/machine7_input_before.png, assets/ui_history/reset_check.png, assets/ui_history/ui-12.png, assets/ui_history/ui_palette_preview.png, assets/ui_history/ui-preview.png (+3 more)

### Community 54 - "._run"
Cohesion: 0.18
Nodes (8): emit(), 002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ, Các bước, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Rủi ro và bảo trì, Điều kiện dừng

### Community 55 - "Amazon Android Tool — Giai đoạn A/B"
Cohesion: 0.29
Nodes (7): Amazon Android Tool — Giai đoạn A/B, Cài trên máy Windows mới, Dán nhiều proxy, Sử dụng, Trạng thái nghiệm thu, Yêu cầu, Điện thoại đám mây Swarmote

### Community 56 - "AppSettings"
Cohesion: 0.15
Nodes (7): _new_prefix(), save(), default_path(), load_settings(), save_settings(), settings_path(), Tăng số lần thử đọc cây Android và bổ sung phương án dự phòng cho b23–b31 — 19/11/2026

### Community 59 - "Bàn giao dừng theo yêu cầu người dùng — 13/11/2026"
Cohesion: 0.25
Nodes (7): Bàn giao dừng theo yêu cầu người dùng — 13/11/2026, Bối cảnh đã hoàn tất trước lỗi hiện tại, Cách tiếp tục, Kiểm chứng gần nhất, Lỗi chính chưa xử lý xong, Phần sửa Stop/Reset đã viết nhưng chưa thử GUI thật, Yêu cầu mới nhất

### Community 60 - "Amazon trên Swarmote"
Cohesion: 0.33
Nodes (5): Amazon trên Swarmote, Người dùng và công việc, Nền tảng, Điều chưa xác minh, Định hướng ngôn ngữ nếu xây dựng lại — 23/11/2026

### Community 61 - "Biên bản kiểm tra thực tế — 2026-11-12"
Cohesion: 0.09
Nodes (23): b6 Country US +1 — 14/11/2026, B6 cuộn quốc gia và chọn lại — 13/11/2026, Biên bản kiểm tra thực tế — 2026-11-12, Cài và đo UiAutomator2 theo phê duyệt mới — 13/11/2026, Dừng riêng một máy — 14/11/2026, Focus ô nhập b4–b11 — 14/11/2026, Ghim taskbar — 13/11/2026, Giao diện sáng, dễ đọc — 2026-11-13 (+15 more)

### Community 62 - "build_reload_payment_steps"
Cohesion: 0.13
Nodes (9): build_reload_payment_steps(), node(), ReloadPaymentTests, adb(), wait(), read(), read(), read() (+1 more)

### Community 63 - "Bộ cài chia sẻ Windows x64"
Cohesion: 0.50
Nodes (3): Bộ cài chia sẻ Windows x64, Dựng lại, Nguồn thành phần

### Community 64 - "SmoothScrollableFrame"
Cohesion: 0.08
Nodes (14): animations_enabled(), SmoothScrollableFrame, Bố cục, Bố cục được áp dụng, Chữ và tiến độ, Giao diện vận hành, Hướng thị giác, Kiểm chứng và phạm vi (+6 more)

### Community 66 - "VERIFICATION.md"
Cohesion: 0.17
Nodes (10): Kết luận và tích hợp, Kết quả thực tế, So sánh bộ đọc trên q1 — 13/11/2026, Thành phần thiết bị, b1–b3 bắt buộc có ba cú bấm — 14/11/2026, b1–b3 ngẫu nhiên cho 12 máy — 14/11/2026, b1–b3 ngẫu nhiên trên 12 máy, không dùng OCR — 14/11/2026, b6 cuộn tới đáy rồi vuốt ngược — 14/11/2026 (+2 more)

### Community 67 - "001 — Tách dữ liệu từng mẻ và đối chiếu số hàng"
Cohesion: 0.29
Nodes (7): 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Rủi ro và bảo trì, Thiết kế yêu cầu, Điều kiện dừng

### Community 68 - "run_batch"
Cohesion: 0.10
Nodes (20): _phone_preparation_lock(), _prepare_phone(), _prepare_phone_locked(), progress(), stop_here(), run_batch(), fill_slots(), manually_selected() (+12 more)

### Community 69 - "time"
Cohesion: 0.17
Nodes (12): main(), check_runtime(), main(), verify(), _app_installed(), _app_paths(), _check_external_apps(), _install_python_dependencies() (+4 more)

### Community 70 - "DesktopLayoutTests"
Cohesion: 0.33
Nodes (3): DesktopLayoutTests, __init__(), __init__()

### Community 71 - "PROJECT_HANDOFF.md"
Cohesion: 0.12
Nodes (16): visit(), b1–b3 ngẫu nhiên cho q1–q12 — 14/11/2026, B4–b11 chạy đồng thời và OCR — 14/11/2026, b6 US +1 còn mở sau bốn cú chạm — 14/11/2026, Bản thử State Machine q7 và b1–b3 mở mục con — 14/11/2026, Bỏ thời hạn tổng sau menu — 14/11/2026, Bổ sung đọc ảnh OCR và chạm trực tiếp dự phòng cho b26 khi uiautomator dump WebView lỗi — 19/11/2026, Cơ chế chụp ảnh OCR quét chữ ấn luôn cho toàn bộ b26–b31 — 19/11/2026 (+8 more)

### Community 73 - "File dự án mà Graphify không phân tích trực tiếp"
Cohesion: 0.40
Nodes (5): File dự án mà Graphify không phân tích trực tiếp, .gitignore, Launch Swarmote Tool.pyw, pyproject.toml, Ảnh PNG trong dự án

### Community 74 - "ProfilesNavigationTests"
Cohesion: 0.08
Nodes (20): _activate_manager(), create_profile(), _create_profile_form(), _invoke(), _open_profiles(), ProfileCreateNotSubmitted, _proxy_test_country(), ProxyConfig (+12 more)

### Community 75 - "CloudPhone"
Cohesion: 0.11
Nodes (16): amazon_is_foreground(), cloud_serials(), CloudPhone, open_amazon(), foreground(), package_path(), probe(), prop() (+8 more)

### Community 79 - "StatusCell"
Cohesion: 0.13
Nodes (3): StatusCell, TableText, Tooltip

### Community 80 - "main"
Cohesion: 0.31
Nodes (3): main(), main(), LauncherTests

### Community 83 - "AccountData"
Cohesion: 0.14
Nodes (6): _automatic_resume_slots(), AccountData, AppSettings, DesktopResumeTests, SettingsTests, on_worker()

### Community 84 - "Bàn giao trạng thái dự án — 13/11/2026"
Cohesion: 0.09
Nodes (17): set_tk_icon(), B6 danh sách quốc gia vẫn mở sau khi chọn — 13/11/2026, Bàn giao trạng thái dự án — 13/11/2026, Bản chính boom4may và bản dự phòng — 14/11/2026, Bộ cài offline chia sẻ — 14/11/2026, Cài đặt máy mới, Dừng riêng máy đang chọn — 14/11/2026, q3/q4 đã nối b1–b3 và thử đồng thời bốn luồng — 13/11/2026 (+9 more)

### Community 88 - "build_random_steps"
Cohesion: 0.07
Nodes (8): resume_common_index(), build_random_steps(), browse(), B1–b3 xem menu ngẫu nhiên cho 12 máy — 14/11/2026, adb(), tap(), wait(), tap()

### Community 89 - "_proxy_postal_prefix"
Cohesion: 0.48
Nodes (3): _proxy_postal_prefix(), controls(), ProxyPostalPrefixTests

### Community 92 - "GRAPH_AUDIT.md"
Cohesion: 0.50
Nodes (3): Cách kiểm tra sau mỗi sửa đổi, Giới hạn đã xác nhận, Kiểm tra độ phủ Graphify — cập nhật 26/11/2026

### Community 96 - "random_prefix.py"
Cohesion: 0.08
Nodes (25): scroll_view(), wait_until(), RecoverableStepError, build_random_steps(), browse(), action(), run_browse(), finish_view() (+17 more)

### Community 97 - "ensure_manager_ready"
Cohesion: 0.24
Nodes (6): ensure_manager_ready(), _main_window(), collect(), ProfileManagerWindowError, ManagerStartupTests, unavailable()

### Community 100 - "OTP_DESIGN.md"
Cohesion: 0.50
Nodes (3): Nối vào bước tạo tài khoản sau khi xác minh màn hình Amazon, Thiết kế OTP cho từng Profile, Đã chuẩn bị

## Knowledge Gaps
- **1 isolated node(s):** `amazon-android-tool`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 581 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **20 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ToolError` connect `ToolError` to `Q1FlowTests`, `otp.py`, `BulkInputTests`, `desktop.py`, `swarmote_desktop.py`, `RunnerTests`, `PostMenuStep`, `ToolError`, `AddressDetailTests`, `build_common_steps`, `RunJob`, `desktop.py`, `profile_status`, `AttemptDeadline`, `open_home_menu`, `._start_post_menu`, `build_change_us_steps`, `Q7StateMachineTests`, `build_q1_steps`, `test_isolated_reader.py`, `BatchDraft`, `RegistrationState`, `build_random_steps`, `ui_backend.py`, `cloud_adb`, `_visible`, `.test_b10_stalled_whatsapp_pauses_only_affected_phone`, `_type_field`, `build_create_address_steps`, `parse_column`, `ExtendedRecoveryTests`, `_read_nodes`, `Window`, `._refresh_devices`, `account_flow.py`, `CountryRecoveryTests`, `bulk_input.py`, `vision.py`, `._run`, `AppSettings`, `parse_bulk_payload`, `build_reload_payment_steps`, `run_batch`, `PROJECT_HANDOFF.md`, `ProfilesNavigationTests`, `CloudPhone`, `_ScreenWaitExpired`, `_confirm_menu_fallback`, `AccountData`, `build_random_steps`, `random_prefix.py`, `ensure_manager_ready`?**
  _High betweenness centrality (0.372) - this node is a cross-community bridge._
- **Are the 62 inferred relationships involving `ToolError` (e.g. with `_read_nodes_once()` and `_resume_address_payment_index()`) actually correct?**
  _`ToolError` has 62 INFERRED edges - model-reasoned connections that need verification._
- **What connects `amazon-android-tool` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `ToolError` be split into smaller, more focused modules?**
  _Cohesion score 0.056598016781083144 - nodes in this community are weakly interconnected._
- **Why does `Window` connect `Window` to `ToolError`, `BulkInputTests`, `desktop.py`, `RunnerTests`, `PostMenuStep`, `RunJob`, `desktop.py`, `profile_status`, `._start_post_menu`, `Q3Q4FlowTests`, `BatchDraft`, `RegistrationState`, `build_random_steps`, `._build_main`, `._refresh_devices`, `._run`, `SmoothScrollableFrame`, `001 — Tách dữ liệu từng mẻ và đối chiếu số hàng`, `run_batch`, `DesktopLayoutTests`, `MachineCell`, `ProfilesNavigationTests`, `CloudPhone`, `StatusCell`, `main`, `AccountData`, `Bàn giao trạng thái dự án — 13/11/2026`?**
  _High betweenness centrality (0.107) - this node is a cross-community bridge._
- **Are the 89 inferred relationships involving `CloudPhone` (e.g. with `build_common_steps()` and `_country_full_row()`) actually correct?**
  _`CloudPhone` has 89 INFERRED edges - model-reasoned connections that need verification._
- **Should `Q1FlowTests` be split into smaller, more focused modules?**
  _Cohesion score 0.08527131782945736 - nodes in this community are weakly interconnected._