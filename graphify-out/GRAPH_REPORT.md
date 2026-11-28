# Graph Report - boom4may  (2026-11-28)

## Corpus Check
- 140 files · ~184,511 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 2, .bat 1, .pyw 1)

## Summary
- 2404 nodes · 8424 edges · 95 communities (75 shown, 20 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 1189 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `14db3013`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- cloud_adb
- build_common_steps
- otp.py
- BulkInputTests
- windows_identity.py
- open_adb_shell
- RunnerTests
- PostMenuStep
- ToolError
- AddressDetailTests
- 003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật
- Danh mục từng bước đã biết — 13/11/2026
- screen
- RunJob
- desktop.py
- amazon-android-tool
- Ảnh hướng dẫn q1/q2 và menu chung lưu cục bộ
- cli.py
- AttemptDeadline
- amazon_is_foreground
- ._start_post_menu
- Điều hướng hai dạng menu ba gạch
- CloudPhone
- build_change_us_steps
- Q7StateMachineTests
- Nghiên cứu và tích hợp Swarmote
- _tail_menu
- change_us_flow.py
- _find_scrolling
- RandomPrefixTests
- build_random_steps
- PROJECT_INDEX.md
- build_random_steps
- ui_backend.py
- isolated_reader.py
- _automatic_resume_slots
- _visible
- registration.py
- _type_field
- build_create_address_steps
- .test_b10_stalled_whatsapp_pauses_only_affected_phone
- _read_nodes
- FakeControl
- ._build_main
- Window
- ._refresh_devices
- route_list_menu
- CountryRecoveryTests
- ProxyConfig
- b1–b11 Reliability and Latency Implementation Plan
- vision.py
- Danh mục ảnh nằm trong dự án
- account_flow.py
- Amazon Android Tool — Giai đoạn A/B
- AppSettings
- core.py
- setup.py
- BatchDraft
- Amazon trên Swarmote
- Biên bản kiểm tra thực tế — 2026-11-12
- build_reload_payment_steps
- Bộ cài chia sẻ Windows x64
- SmoothScrollableFrame
- build_post_auth_steps
- VERIFICATION.md
- 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng
- run_batch
- time
- PROJECT_HANDOFF.md
- SafetyTests
- MachineCell
- ProfilesNavigationTests
- .test_b1_b2_wait_two_seconds_after_tap_before_view_scroll
- _CombinedStop
- .test_tail_child_page_scrolls_then_backs_before_next_menu_choice
- _choose_tail_target
- StatusCell
- build_q1_steps
- ProfileManagerWindowError
- parse_column
- RunJob
- Bàn giao trạng thái dự án — 13/11/2026
- Giai đoạn 2 — bản thử State Machine riêng q7
- parse_bulk_payload
- RegistrationState
- ToolError
- _proxy_postal_prefix
- validate_card
- _url_from_cell
- GRAPH_AUDIT.md
- q7_random_prefix.py
- OTP_DESIGN.md

## God Nodes (most connected - your core abstractions)
1. `ToolError` - 367 edges
2. `CloudPhone` - 238 edges
3. `AttemptDeadline` - 227 edges
4. `RunJob` - 175 edges
5. `RegistrationState` - 166 edges
6. `build_common_steps()` - 115 edges
7. `Window` - 115 edges
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

## Communities (95 total, 20 thin omitted)

### Community 0 - "cloud_adb"
Cohesion: 0.10
Nodes (26): _country_full_row(), _keyboard_visible(), _tap(), visit_home(), b2(), cloud_adb(), reported_installer(), _scroll_country() (+18 more)

### Community 1 - "build_common_steps"
Cohesion: 0.09
Nodes (4): build_common_steps(), _ScreenWaitExpired, node(), Q1FlowTests

### Community 2 - "otp.py"
Cohesion: 0.10
Nodes (9): browser_launch_options(), extract_otp(), _NoRedirect, read_otp(), _read_otp_in_browser(), validate_otp_url(), wait_for_new_otp(), OtpTests (+1 more)

### Community 4 - "windows_identity.py"
Cohesion: 0.17
Nodes (8): create_shortcut(), relaunch_command(), runtime(), set_process_identity(), set_tk_icon(), set_window_identity(), Sửa shortcut ghim mở nhầm IDLE — 13/11/2026, WindowsIdentityTests

### Community 5 - "open_adb_shell"
Cohesion: 0.09
Nodes (29): _check_stop(), collapse_apps_panel(), install_amazon(), collect(), open_adb_shell(), _pause(), _phone_window(), _progress_reporter() (+21 more)

### Community 6 - "RunnerTests"
Cohesion: 0.06
Nodes (19): ProfileRegistry, ProfileLookupError, ProfileNotFound, Thiết kế yêu cầu, absent(), ProfileRegistryTests, lookup(), broken() (+11 more)

### Community 7 - "PostMenuStep"
Cohesion: 0.09
Nodes (10): PostMenuSession, PostMenuStep, PostMenuTests, reconcile(), first(), ResumeRegistrationStateTests, factory(), factory() (+2 more)

### Community 8 - "ToolError"
Cohesion: 0.08
Nodes (14): ProfileStartNotSubmitted, _select_profile_rows(), _selected_profile_names(), start_profile(), start_profiles_together(), _wait_for_selected(), Hàng đợi 4 máy với giới hạn 2 Running — 14/11/2026, delayed_start() (+6 more)

### Community 9 - "AddressDetailTests"
Cohesion: 0.12
Nodes (7): build_create_address_detail_steps(), AddressDetailTests, read(), adb(), tap(), read(), item()

### Community 10 - "003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật"
Cohesion: 0.06
Nodes (26): 002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Rủi ro và bảo trì, Điều kiện dừng, 003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật, Các bước (+18 more)

### Community 11 - "Danh mục từng bước đã biết — 13/11/2026"
Cohesion: 0.06
Nodes (35): Bản thử q7 State Machine — 14/11/2026, Chung b10 — Chuyển WhatsApp sang SMS, Chung b11 — Lấy và gõ OTP SMS, Chung b11a — Chạm ô OTP trên màn SMS, Chung b11b — Xác minh đăng nhập hoặc bấm Create của luồng tạo, Chung b4 — Sign In từ menu, Chung b4a — Chạm ô SĐT, Chung b5 — Gõ số điện thoại (+27 more)

### Community 12 - "screen"
Cohesion: 0.21
Nodes (18): continue_number(), country(), finish_auto(), finish_create(), finish_login(), focus_phone(), phone_number(), proceed() (+10 more)

### Community 16 - "Ảnh hướng dẫn q1/q2 và menu chung lưu cục bộ"
Cohesion: 0.07
Nodes (28): B16–b22 chung — Đổi marketplace sang United States (18/11/2026), B32–b39 — Reload Balance, thêm thẻ và địa chỉ thanh toán (21/11/2026), B6 — Hai ảnh đính kèm mới ngày 13/11/2026, Menu chung ảnh 01 — Danh sách chữ, Menu chung ảnh 02 — App Store bên phải sau khi Amazon mở, q1 b6 — US +1 hiện nhưng chạm không đóng hộp, 14/11/2026, q1 ảnh 01 — Menu và ba thẻ, q1 ảnh 02 — Sign In cuối menu (+20 more)

### Community 17 - "cli.py"
Cohesion: 0.29
Nodes (6): main(), parser(), report(), get_device(), print_json(), Store

### Community 18 - "AttemptDeadline"
Cohesion: 0.06
Nodes (24): AttemptDeadline, ChangeUsFlowTests, node(), MarketplaceFlowTests, read(), adb(), read(), tap() (+16 more)

### Community 19 - "amazon_is_foreground"
Cohesion: 0.13
Nodes (7): cloud_serials(), package_path(), probe(), scan(), CloudBridgeTests, adb(), Ẩn cửa sổ cmd khi gọi ADB — 2026-11-13

### Community 20 - "._start_post_menu"
Cohesion: 0.12
Nodes (3): _markdown_cell_text(), Dán bảng Amazon có ghi chú thẻ live và URL OTP escaped — 14/11/2026, Trạng thái kiểm chứng và giới hạn

### Community 21 - "Điều hướng hai dạng menu ba gạch"
Cohesion: 0.50
Nodes (4): Bằng chứng và phạm vi, Kiểm chứng, Quy tắc chạy, Điều hướng hai dạng menu ba gạch

### Community 22 - "CloudPhone"
Cohesion: 0.07
Nodes (13): CloudPhone, prop(), type_characters(), category_action(), build_q3_steps(), build_q4_steps(), build_q5_steps(), HomeMenuTests (+5 more)

### Community 23 - "build_change_us_steps"
Cohesion: 0.14
Nodes (40): confirmed_login_otp_nodes(), enter_otp(), focus_otp(), name(), read_sms_form(), _check_summary(), _field(), _form_action() (+32 more)

### Community 24 - "Q7StateMachineTests"
Cohesion: 0.07
Nodes (25): RecoverableStepError, build_random_steps(), sign_in(), _menu(), _size(), ActionValidator, _already_reached_result(), build_q7_pilot_steps() (+17 more)

### Community 25 - "Nghiên cứu và tích hợp Swarmote"
Cohesion: 0.40
Nodes (4): Hành vi có bằng chứng, Kiểm thử còn lại, Nghiên cứu và tích hợp Swarmote, Phần đã áp dụng

### Community 26 - "_tail_menu"
Cohesion: 0.13
Nodes (28): _read_hierarchy(), _read_login_sms_visual(), _read_nodes_once(), _read_visual_nodes(), _UiReadIncomplete, amazon_is_foreground(), current(), _serve() (+20 more)

### Community 27 - "change_us_flow.py"
Cohesion: 0.15
Nodes (16): _account_icon_from_image(), _after_back(), _browse(), b16(), b17(), _google_sheet(), _passkey_page(), _person() (+8 more)

### Community 28 - "_find_scrolling"
Cohesion: 0.10
Nodes (4): _country_nodes(), _CountryReadStop, _find_scrolling(), b6 cuộn chạm đáy rồi vuốt ngược nhẹ tìm US +1 — 14/11/2026

### Community 30 - "build_random_steps"
Cohesion: 0.09
Nodes (7): resume_common_index(), build_random_steps(), finish_view(), adb(), adb(), adb(), adb()

### Community 31 - "PROJECT_INDEX.md"
Cohesion: 0.16
Nodes (8): Quy trình Swarmote hiện tại, Luồng q1 từ menu ba gạch tới nhập OTP, Thử trên q1 đã có, Luồng q2 từ menu ba gạch, q3 — b1–b3 và nối luồng chung, q4 — Giỏ hàng, Pets, Home and DIY, q5 — ba thẻ riêng và b4–b11 chung, q6 — Trang chủ, Giỏ hàng, menu và một thẻ

### Community 32 - "build_random_steps"
Cohesion: 0.12
Nodes (4): RandomPrefixTests, adb(), adb(), adb()

### Community 33 - "ui_backend.py"
Cohesion: 0.07
Nodes (16): swarmote_adb_path(), swarmote_tunnel_owner(), arrange_on_open(), _row_if_fits(), _sort_key(), _tiles(), _connect(), country_reverse_points() (+8 more)

### Community 34 - "isolated_reader.py"
Cohesion: 0.24
Nodes (7): phone_reader(), PhoneReader, ReaderResponseError, fake_worker(), IsolationTests, duplicate(), production_worker_with_fake_android()

### Community 36 - "_visible"
Cohesion: 0.12
Nodes (36): _bounds(), _scroll_up(), _text(), _visible(), _menu_visible(), _action(), _address_form(), _addresses() (+28 more)

### Community 37 - "registration.py"
Cohesion: 0.17
Nodes (13): require_online(), _field_for_label(), fill_identifier(), fill_signup_form(), _nodes(), open_entry(), status(), _tap() (+5 more)

### Community 38 - "_type_field"
Cohesion: 0.22
Nodes (3): _type_field(), FlowRecoveryTests, form()

### Community 39 - "build_create_address_steps"
Cohesion: 0.24
Nodes (4): build_create_address_steps(), CreateAddressFlowTests, read(), node()

### Community 42 - "_read_nodes"
Cohesion: 0.10
Nodes (26): _at_or_after(), sign_in(), _ensure_menu(), _read_nodes(), _unique(), cart_action(), action(), cart_visible() (+18 more)

### Community 44 - "FakeControl"
Cohesion: 0.13
Nodes (5): ParallelInstallTests, PhoneWindow, FakeControl, InstallTests, descendants()

### Community 45 - "._build_main"
Cohesion: 0.17
Nodes (7): Button, Entry, FooterNote, HeaderWave, icon(), ui_font(), section_heading()

### Community 46 - "Window"
Cohesion: 0.13
Nodes (4): Window, otp_token(), Các bước, PreparationProgressTests

### Community 47 - "._refresh_devices"
Cohesion: 0.16
Nodes (5): state_style(), status_title(), DesktopLayoutTests, __init__(), __init__()

### Community 48 - "route_list_menu"
Cohesion: 0.22
Nodes (4): menu_layout(), route_list_menu(), reconcile(), route()

### Community 49 - "CountryRecoveryTests"
Cohesion: 0.27
Nodes (4): CountryRecoveryTests, read(), wait(), node()

### Community 50 - "ProxyConfig"
Cohesion: 0.12
Nodes (11): BatchItem, parse_proxy_line(), prepare_five(), lines(), _proxy_rows(), _table_cells(), create_profile(), ProxyConfig (+3 more)

### Community 51 - "b1–b11 Reliability and Latency Implementation Plan"
Cohesion: 0.18
Nodes (10): b1–b11 Reliability and Latency Implementation Plan, Completion Criteria, File Map, Global Constraints, Review Focus, Task 1: Measure current step latency and classify existing failures, Task 2: Define safe retry, reconcile, pause, and stop behavior, Task 3: Reduce redundant UI reads and unnecessary waits (+2 more)

### Community 52 - "vision.py"
Cohesion: 0.07
Nodes (19): _bounds(), _canonical_text(), _compact(), _engine(), _field_contents(), _field_is_blank(), _input_box(), _join_wrapped_categories() (+11 more)

### Community 53 - "Danh mục ảnh nằm trong dự án"
Cohesion: 0.18
Nodes (11): amazon_android/assets/icons/, amazon_android/assets/obsidian_prism.png, amazon_android/assets/swarmote_tool_square.png và swarmote_tool.ico, assets/ui_history/machine7_input_before.png, assets/ui_history/reset_check.png, assets/ui_history/ui-12.png, assets/ui_history/ui_palette_preview.png, assets/ui_history/ui-preview.png (+3 more)

### Community 54 - "account_flow.py"
Cohesion: 0.15
Nodes (10): _ActionNotResolved, _parse_ui_nodes(), _resume_address_payment_index(), _same_country_position(), _visible_edit_fields(), _visual_form_button(), _yellow_form_button(), _account_content() (+2 more)

### Community 55 - "Amazon Android Tool — Giai đoạn A/B"
Cohesion: 0.29
Nodes (7): Amazon Android Tool — Giai đoạn A/B, Cài trên máy Windows mới, Dán nhiều proxy, Sử dụng, Trạng thái nghiệm thu, Yêu cầu, Điện thoại đám mây Swarmote

### Community 56 - "AppSettings"
Cohesion: 0.16
Nodes (9): _new_prefix(), save(), default_path(), AppSettings, load_settings(), save_settings(), settings_path(), Tăng số lần thử đọc cây Android và bổ sung phương án dự phòng cho b23–b31 — 19/11/2026 (+1 more)

### Community 57 - "core.py"
Cohesion: 0.25
Nodes (20): adb(), available_memory_mb(), check_play(), configure_avd(), connected_devices(), Device, device_avd_name(), device_resources() (+12 more)

### Community 58 - "setup.py"
Cohesion: 0.23
Nodes (12): app_data_dir(), avd_names(), create_avd(), doctor(), executable(), installed_image(), run(), sdk_root() (+4 more)

### Community 60 - "Amazon trên Swarmote"
Cohesion: 0.33
Nodes (5): Amazon trên Swarmote, Người dùng và công việc, Nền tảng, Điều chưa xác minh, Định hướng ngôn ngữ nếu xây dựng lại — 23/11/2026

### Community 61 - "Biên bản kiểm tra thực tế — 2026-11-12"
Cohesion: 0.08
Nodes (25): b6 Country US +1 — 14/11/2026, B6 cuộn quốc gia và chọn lại — 13/11/2026, Biên bản kiểm tra thực tế — 2026-11-12, Cài và đo UiAutomator2 theo phê duyệt mới — 13/11/2026, Dừng riêng một máy — 14/11/2026, Focus ô nhập b4–b11 — 14/11/2026, Ghim taskbar — 13/11/2026, Giao diện sáng, dễ đọc — 2026-11-13 (+17 more)

### Community 62 - "build_reload_payment_steps"
Cohesion: 0.13
Nodes (9): build_reload_payment_steps(), node(), ReloadPaymentTests, adb(), wait(), read(), read(), read() (+1 more)

### Community 63 - "Bộ cài chia sẻ Windows x64"
Cohesion: 0.50
Nodes (3): Bộ cài chia sẻ Windows x64, Dựng lại, Nguồn thành phần

### Community 64 - "SmoothScrollableFrame"
Cohesion: 0.05
Nodes (23): main(), animations_enabled(), SmoothScrollableFrame, main(), Bố cục, Bố cục được áp dụng, Chữ và tiến độ, Giao diện vận hành (+15 more)

### Community 65 - "build_post_auth_steps"
Cohesion: 0.18
Nodes (11): Hướng dẫn khi tiếp tục dự án, build_post_auth_steps(), Nhận diện giao diện lúc chạy, Nhập liệu và lỗi, Quy tắc tự động hóa sau menu ba gạch, Trạng thái hiện tại của dự án, Từng máy độc lập, Bản đồ repository (+3 more)

### Community 66 - "VERIFICATION.md"
Cohesion: 0.17
Nodes (10): Kết luận và tích hợp, Kết quả thực tế, So sánh bộ đọc trên q1 — 13/11/2026, Thành phần thiết bị, b1–b3 bắt buộc có ba cú bấm — 14/11/2026, b1–b3 ngẫu nhiên cho 12 máy — 14/11/2026, b1–b3 ngẫu nhiên trên 12 máy, không dùng OCR — 14/11/2026, b6 cuộn tới đáy rồi vuốt ngược — 14/11/2026 (+2 more)

### Community 67 - "001 — Tách dữ liệu từng mẻ và đối chiếu số hàng"
Cohesion: 0.29
Nodes (7): 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Rủi ro và bảo trì, Thiết kế yêu cầu, Điều kiện dừng

### Community 68 - "run_batch"
Cohesion: 0.12
Nodes (14): _prepare_phone_locked(), progress(), stop_here(), run_batch(), fill_slots(), manually_selected(), refresh_slots(), requested() (+6 more)

### Community 69 - "time"
Cohesion: 0.18
Nodes (12): main(), check_runtime(), main(), verify(), _app_installed(), _app_paths(), _check_external_apps(), _install_python_dependencies() (+4 more)

### Community 71 - "PROJECT_HANDOFF.md"
Cohesion: 0.11
Nodes (17): visit(), b1–b3 ngẫu nhiên cho q1–q12 — 14/11/2026, B4–b11 chạy đồng thời và OCR — 14/11/2026, b6 US +1 còn mở sau bốn cú chạm — 14/11/2026, Bản thử State Machine q7 và b1–b3 mở mục con — 14/11/2026, Bỏ thời hạn tổng sau menu — 14/11/2026, Bổ sung đọc ảnh OCR và chạm trực tiếp dự phòng cho b26 khi uiautomator dump WebView lỗi — 19/11/2026, Cơ chế chụp ảnh OCR quét chữ ấn luôn cho toàn bộ b26–b31 — 19/11/2026 (+9 more)

### Community 74 - "ProfilesNavigationTests"
Cohesion: 0.07
Nodes (29): _activate_manager(), _create_profile_form(), _descendants(), inspect(), _invoke(), _main_window(), _one(), _open_profiles() (+21 more)

### Community 78 - "_choose_tail_target"
Cohesion: 0.22
Nodes (4): _choose_tail_target(), _TailChoicesExhausted, choose(), choose()

### Community 79 - "StatusCell"
Cohesion: 0.13
Nodes (3): StatusCell, TableText, Tooltip

### Community 81 - "ProfileManagerWindowError"
Cohesion: 0.22
Nodes (5): ensure_manager_ready(), ProfileManagerWindowError, _swarmote_exe(), ManagerStartupTests, unavailable()

### Community 83 - "RunJob"
Cohesion: 0.08
Nodes (14): AccountData, _phone_preparation_lock(), _prepare_phone(), retry_preparation(), RunJob, P03 — Mở form New Profile, DesktopResumeTests, apartment_type() (+6 more)

### Community 84 - "Bàn giao trạng thái dự án — 13/11/2026"
Cohesion: 0.11
Nodes (15): B6 danh sách quốc gia vẫn mở sau khi chọn — 13/11/2026, Bàn giao trạng thái dự án — 13/11/2026, Bản chính boom4may và bản dự phòng — 14/11/2026, Bộ cài offline chia sẻ — 14/11/2026, Cài đặt máy mới, Dừng riêng máy đang chọn — 14/11/2026, Dự phòng dùng chung khi chạy song song — 14/11/2026, q3/q4 đã nối b1–b3 và thử đồng thời bốn luồng — 13/11/2026 (+7 more)

### Community 85 - "Giai đoạn 2 — bản thử State Machine riêng q7"
Cohesion: 0.40
Nodes (5): Cách thử bản pilot cũ (không áp dụng cho factory hiện hành), Giai đoạn 2 — bản thử State Machine riêng q7, Giới hạn, Phạm vi và quan hệ với luồng cũ, Sơ đồ

### Community 86 - "parse_bulk_payload"
Cohesion: 0.18
Nodes (3): BulkRecord, parse_bulk_payload(), Value

### Community 87 - "RegistrationState"
Cohesion: 0.15
Nodes (5): RegistrationState, build_tail_steps(), open_menu(), view(), visit_seconds()

### Community 88 - "ToolError"
Cohesion: 0.06
Nodes (27): verify_menu_open(), open_amazon(), foreground(), ToolError, _confirm_menu_fallback(), _menu_evidence(), MenuReadUnavailable, _nodes() (+19 more)

### Community 89 - "_proxy_postal_prefix"
Cohesion: 0.48
Nodes (3): _proxy_postal_prefix(), controls(), ProxyPostalPrefixTests

### Community 92 - "GRAPH_AUDIT.md"
Cohesion: 0.50
Nodes (3): Cách kiểm tra sau mỗi sửa đổi, Giới hạn đã xác nhận, Kiểm tra độ phủ Graphify — cập nhật 26/11/2026

### Community 96 - "q7_random_prefix.py"
Cohesion: 0.13
Nodes (11): scroll_view(), wait_until(), browse(), action(), run_browse(), finish_view(), _first_point(), PrefixDeadline (+3 more)

### Community 100 - "OTP_DESIGN.md"
Cohesion: 0.50
Nodes (3): Nối vào bước tạo tài khoản sau khi xác minh màn hình Amazon, Thiết kế OTP cho từng Profile, Đã chuẩn bị

## Knowledge Gaps
- **1 isolated node(s):** `amazon-android-tool`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 582 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **20 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ToolError` connect `ToolError` to `cloud_adb`, `build_common_steps`, `otp.py`, `BulkInputTests`, `open_adb_shell`, `RunnerTests`, `PostMenuStep`, `ToolError`, `AddressDetailTests`, `003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật`, `screen`, `RunJob`, `desktop.py`, `cli.py`, `AttemptDeadline`, `amazon_is_foreground`, `._start_post_menu`, `CloudPhone`, `build_change_us_steps`, `Q7StateMachineTests`, `_tail_menu`, `change_us_flow.py`, `_find_scrolling`, `RandomPrefixTests`, `build_random_steps`, `build_random_steps`, `ui_backend.py`, `isolated_reader.py`, `_visible`, `registration.py`, `_type_field`, `build_create_address_steps`, `.test_b10_stalled_whatsapp_pauses_only_affected_phone`, `_read_nodes`, `Window`, `._refresh_devices`, `CountryRecoveryTests`, `ProxyConfig`, `vision.py`, `account_flow.py`, `AppSettings`, `core.py`, `setup.py`, `BatchDraft`, `build_reload_payment_steps`, `run_batch`, `.__init__`, `PROJECT_HANDOFF.md`, `ProfilesNavigationTests`, `_choose_tail_target`, `build_q1_steps`, `ProfileManagerWindowError`, `parse_column`, `RunJob`, `parse_bulk_payload`, `RegistrationState`, `validate_card`, `_url_from_cell`, `q7_random_prefix.py`?**
  _High betweenness centrality (0.351) - this node is a cross-community bridge._
- **Are the 61 inferred relationships involving `ToolError` (e.g. with `_read_nodes_once()` and `_resume_address_payment_index()`) actually correct?**
  _`ToolError` has 61 INFERRED edges - model-reasoned connections that need verification._
- **What connects `amazon-android-tool` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `cloud_adb` be split into smaller, more focused modules?**
  _Cohesion score 0.10241820768136557 - nodes in this community are weakly interconnected._
- **Why does `Window` connect `Window` to `otp.py`, `BulkInputTests`, `windows_identity.py`, `RunnerTests`, `PostMenuStep`, `RunJob`, `desktop.py`, `._start_post_menu`, `CloudPhone`, `RandomPrefixTests`, `build_random_steps`, `_automatic_resume_slots`, `._build_main`, `._refresh_devices`, `route_list_menu`, `ProxyConfig`, `AppSettings`, `core.py`, `BatchDraft`, `SmoothScrollableFrame`, `001 — Tách dữ liệu từng mẻ và đối chiếu số hàng`, `run_batch`, `.__init__`, `MachineCell`, `StatusCell`, `RunJob`, `Bàn giao trạng thái dự án — 13/11/2026`, `ToolError`?**
  _High betweenness centrality (0.107) - this node is a cross-community bridge._
- **Are the 89 inferred relationships involving `CloudPhone` (e.g. with `build_common_steps()` and `_country_full_row()`) actually correct?**
  _`CloudPhone` has 89 INFERRED edges - model-reasoned connections that need verification._
- **Should `build_common_steps` be split into smaller, more focused modules?**
  _Cohesion score 0.08831168831168831 - nodes in this community are weakly interconnected._