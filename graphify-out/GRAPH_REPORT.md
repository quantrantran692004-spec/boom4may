# Graph Report - boom4may  (2026-11-28)

## Corpus Check
- 140 files · ~184,342 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 2, .bat 1, .pyw 1)

## Summary
- 2402 nodes · 8419 edges · 97 communities (78 shown, 19 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 1189 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `05ef3c2a`
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
- desktop.py
- amazon-android-tool
- Ảnh hướng dẫn q1/q2 và menu chung lưu cục bộ
- cli.py
- MarketplaceFlowTests
- amazon_is_foreground
- ._start_post_menu
- MENU_ROUTING.md
- Q3Q4FlowTests
- build_change_us_steps
- Q7StateMachineTests
- Nghiên cứu và tích hợp Swarmote
- _tail_menu
- settings
- phone_window_layout.py
- CloudPhone
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
- .test_transition_keeps_observing_after_short_wait_without_tapping
- _read_nodes
- FakeControl
- ._build_main
- Window
- ._refresh_devices
- test_q1_flow.py
- CountryRecoveryTests
- bulk_input.py
- b1–b11 Reliability and Latency Implementation Plan
- vision.py
- Danh mục ảnh nằm trong dự án
- reload_payment_flow.py
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
- node
- VERIFICATION.md
- 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng
- run_batch
- time
- .__init__
- PROJECT_HANDOFF.md
- SafetyTests
- MachineCell
- ProfilesNavigationTests
- .test_missing_target_fallback_backs_then_uses_fresh_locale_text_on_all_modes_and_slots
- _CombinedStop
- .test_tail_child_page_scrolls_then_backs_before_next_menu_choice
- .test_b17_recovers_search_then_reopens_account_before_locale
- StatusCell
- main
- ProfileManagerWindowError
- Bàn giao dừng theo yêu cầu người dùng — 13/11/2026
- RunJob
- Bàn giao trạng thái dự án — 13/11/2026
- q5_flow.py
- Value
- RegistrationState
- ToolError
- _proxy_postal_prefix
- validate_card
- Q2FlowTests
- GRAPH_AUDIT.md
- _prefix_nodes
- Tạo tài khoản b23–b25 — Account và Your Addresses (19/11/2026)
- cloud_adb
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

## Communities (97 total, 19 thin omitted)

### Community 0 - "AttemptDeadline"
Cohesion: 0.15
Nodes (3): AttemptDeadline, ChangeUsFlowTests, node()

### Community 1 - "build_common_steps"
Cohesion: 0.05
Nodes (6): build_common_steps(), node(), Q1FlowTests, read(), provider_read(), read()

### Community 2 - "otp.py"
Cohesion: 0.10
Nodes (9): browser_launch_options(), extract_otp(), _NoRedirect, read_otp(), _read_otp_in_browser(), validate_otp_url(), wait_for_new_otp(), OtpTests (+1 more)

### Community 4 - "windows_identity.py"
Cohesion: 0.24
Nodes (5): create_shortcut(), relaunch_command(), runtime(), set_window_identity(), WindowsIdentityTests

### Community 5 - "swarmote_desktop.py"
Cohesion: 0.08
Nodes (35): package_path(), _check_stop(), collapse_apps_panel(), _descendants(), ensure_manager_ready(), inspect(), install_amazon(), _main_window() (+27 more)

### Community 6 - "RunnerTests"
Cohesion: 0.05
Nodes (20): ProfileRegistry, ProfileNotFound, absent(), ProfileRegistryTests, lookup(), broken(), RunnerTests, create() (+12 more)

### Community 7 - "PostMenuStep"
Cohesion: 0.07
Nodes (15): current(), PostMenuSession, PostMenuStep, PostMenuTests, first_step(), reconcile(), first(), ResumeRegistrationStateTests (+7 more)

### Community 8 - "ToolError"
Cohesion: 0.09
Nodes (11): ProfileStartNotSubmitted, _select_profile_rows(), _selected_profile_names(), start_profile(), _wait_for_selected(), BatchStartTests, checkbox(), toggle() (+3 more)

### Community 9 - "AddressDetailTests"
Cohesion: 0.12
Nodes (7): build_create_address_detail_steps(), AddressDetailTests, read(), adb(), tap(), read(), item()

### Community 10 - "003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật"
Cohesion: 0.06
Nodes (26): 002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ, Kiểm tra bắt buộc, Phạm vi, Rủi ro và bảo trì, Thiết kế yêu cầu, Điều kiện dừng, 003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật, Các bước (+18 more)

### Community 11 - "Danh mục từng bước đã biết — 13/11/2026"
Cohesion: 0.06
Nodes (36): Bản thử q7 State Machine — 14/11/2026, Chung b10 — Chuyển WhatsApp sang SMS, Chung b11 — Lấy và gõ OTP SMS, Chung b11a — Chạm ô OTP trên màn SMS, Chung b11b — Xác minh đăng nhập hoặc bấm Create của luồng tạo, Chung b16–b22 — Tài khoản và marketplace United States, Chung b4 — Sign In từ menu, Chung b4a — Chạm ô SĐT (+28 more)

### Community 12 - "screen"
Cohesion: 0.10
Nodes (30): continue_number(), country(), finish_auto(), finish_create(), finish_login(), focus_phone(), name(), phone_number() (+22 more)

### Community 13 - "RunJob"
Cohesion: 0.07
Nodes (3): retry_preparation(), P03 — Mở form New Profile, StopResetTests

### Community 16 - "Ảnh hướng dẫn q1/q2 và menu chung lưu cục bộ"
Cohesion: 0.08
Nodes (26): B16–b22 chung — Đổi marketplace sang United States (18/11/2026), B6 — Hai ảnh đính kèm mới ngày 13/11/2026, Menu chung ảnh 01 — Danh sách chữ, Menu chung ảnh 02 — App Store bên phải sau khi Amazon mở, q1 b6 — US +1 hiện nhưng chạm không đóng hộp, 14/11/2026, q1 ảnh 01 — Menu và ba thẻ, q1 ảnh 02 — Sign In cuối menu, q1 ảnh 03 — Nhập số điện thoại (+18 more)

### Community 17 - "cli.py"
Cohesion: 0.19
Nodes (9): BatchItem, parse_proxy_line(), prepare_five(), main(), parser(), report(), get_device(), Store (+1 more)

### Community 19 - "amazon_is_foreground"
Cohesion: 0.11
Nodes (11): amazon_is_foreground(), cloud_serials(), open_amazon(), foreground(), probe(), prop(), reported_installer(), scan() (+3 more)

### Community 21 - "MENU_ROUTING.md"
Cohesion: 0.23
Nodes (7): Bằng chứng và phạm vi, Kiểm chứng, Quy tắc chạy, Điều hướng hai dạng menu ba gạch, Luồng q1 từ menu ba gạch tới nhập OTP, Thử trên q1 đã có, Luồng q2 từ menu ba gạch

### Community 22 - "Q3Q4FlowTests"
Cohesion: 0.21
Nodes (3): build_q3_steps(), build_q4_steps(), Q3Q4FlowTests

### Community 23 - "build_change_us_steps"
Cohesion: 0.09
Nodes (55): confirmed_login_otp_nodes(), enter_otp(), focus_otp(), read_sms_form(), _button(), _check_summary(), _field(), _form_action() (+47 more)

### Community 24 - "Q7StateMachineTests"
Cohesion: 0.09
Nodes (15): ActionValidator, _already_reached_result(), build_q7_pilot_steps(), _past_known_step(), ResultVerifier, StateDeadline, StateDetector, StateMachineStop (+7 more)

### Community 25 - "Nghiên cứu và tích hợp Swarmote"
Cohesion: 0.40
Nodes (4): Hành vi có bằng chứng, Kiểm thử còn lại, Nghiên cứu và tích hợp Swarmote, Phần đã áp dụng

### Community 26 - "_tail_menu"
Cohesion: 0.15
Nodes (28): _text(), _account_tab(), build_marketplace_steps(), run(), account_target(), back_and_read_text(), recover_country_list(), _country_card() (+20 more)

### Community 27 - "settings"
Cohesion: 0.14
Nodes (9): read(), read(), read(), read(), tap_action(), read(), read(), read() (+1 more)

### Community 28 - "phone_window_layout.py"
Cohesion: 0.14
Nodes (5): arrange_on_open(), _row_if_fits(), _sort_key(), _tiles(), PhoneWindowLayoutTests

### Community 29 - "CloudPhone"
Cohesion: 0.14
Nodes (7): CloudPhone, reconcile(), route(), type_characters(), HomeMenuTests, MenuReturnTests, step()

### Community 30 - "build_random_steps"
Cohesion: 0.06
Nodes (23): Hướng dẫn khi tiếp tục dự án, resume_common_index(), build_post_auth_steps(), build_random_steps(), finish_view(), Nhận diện giao diện lúc chạy, Nhập liệu và lỗi, Quy tắc tự động hóa sau menu ba gạch (+15 more)

### Community 31 - "PROJECT_INDEX.md"
Cohesion: 0.18
Nodes (6): Quy trình Swarmote hiện tại, Bản đồ repository, q3 — b1–b3 và nối luồng chung, q4 — Giỏ hàng, Pets, Home and DIY, q5 — ba thẻ riêng và b4–b11 chung, q6 — Trang chủ, Giỏ hàng, menu và một thẻ

### Community 32 - "build_random_steps"
Cohesion: 0.11
Nodes (4): RandomPrefixTests, adb(), adb(), adb()

### Community 33 - "ui_backend.py"
Cohesion: 0.14
Nodes (10): swarmote_adb_path(), _connect(), country_reverse_points(), country_scroll(), _failed(), read_tree(), ready(), _session() (+2 more)

### Community 34 - "isolated_reader.py"
Cohesion: 0.20
Nodes (8): phone_reader(), PhoneReader, ReaderResponseError, _serve(), fake_worker(), IsolationTests, duplicate(), production_worker_with_fake_android()

### Community 36 - "_visible"
Cohesion: 0.15
Nodes (27): _bounds(), _visible(), _menu_visible(), _action(), _address_form(), _addresses(), _bounded_native(), run() (+19 more)

### Community 37 - "registration.py"
Cohesion: 0.16
Nodes (13): require_online(), _field_for_label(), fill_identifier(), fill_signup_form(), _nodes(), open_entry(), status(), _tap() (+5 more)

### Community 38 - "_type_field"
Cohesion: 0.15
Nodes (7): _keyboard_visible(), _tap_input(), _type_field(), _UiReadIncomplete, fail(), FlowRecoveryTests, form()

### Community 39 - "build_create_address_steps"
Cohesion: 0.24
Nodes (4): build_create_address_steps(), CreateAddressFlowTests, read(), node()

### Community 42 - "_read_nodes"
Cohesion: 0.10
Nodes (33): _at_or_after(), sign_in(), _country_nodes(), _CountryReadStop, _ensure_menu(), _find_scrolling(), home_visible(), _read_nodes() (+25 more)

### Community 44 - "FakeControl"
Cohesion: 0.13
Nodes (5): ParallelInstallTests, PhoneWindow, FakeControl, InstallTests, descendants()

### Community 45 - "._build_main"
Cohesion: 0.17
Nodes (7): Button, Entry, FooterNote, HeaderWave, icon(), ui_font(), section_heading()

### Community 46 - "Window"
Cohesion: 0.12
Nodes (4): Window, emit(), Các bước, PreparationProgressTests

### Community 47 - "._refresh_devices"
Cohesion: 0.15
Nodes (5): state_style(), status_title(), DesktopLayoutTests, __init__(), __init__()

### Community 48 - "test_q1_flow.py"
Cohesion: 0.15
Nodes (7): _ActionNotResolved, menu_layout(), _parse_ui_nodes(), route_list_menu(), _ScreenWaitExpired, _visual_form_button(), _yellow_form_button()

### Community 49 - "CountryRecoveryTests"
Cohesion: 0.27
Nodes (4): CountryRecoveryTests, read(), wait(), node()

### Community 50 - "bulk_input.py"
Cohesion: 0.10
Nodes (10): BulkRecord, lines(), _markdown_cell_text(), parse_bulk_payload(), parse_column(), _proxy_rows(), _table_cells(), _url_from_cell() (+2 more)

### Community 51 - "b1–b11 Reliability and Latency Implementation Plan"
Cohesion: 0.18
Nodes (10): b1–b11 Reliability and Latency Implementation Plan, Completion Criteria, File Map, Global Constraints, Review Focus, Task 1: Measure current step latency and classify existing failures, Task 2: Define safe retry, reconcile, pause, and stop behavior, Task 3: Reduce redundant UI reads and unnecessary waits (+2 more)

### Community 52 - "vision.py"
Cohesion: 0.07
Nodes (19): _bounds(), _canonical_text(), _compact(), _engine(), _field_contents(), _field_is_blank(), _input_box(), _join_wrapped_categories() (+11 more)

### Community 53 - "Danh mục ảnh nằm trong dự án"
Cohesion: 0.18
Nodes (11): amazon_android/assets/icons/, amazon_android/assets/obsidian_prism.png, amazon_android/assets/swarmote_tool_square.png và swarmote_tool.ico, assets/ui_history/machine7_input_before.png, assets/ui_history/reset_check.png, assets/ui_history/ui-12.png, assets/ui_history/ui_palette_preview.png, assets/ui_history/ui-preview.png (+3 more)

### Community 54 - "reload_payment_flow.py"
Cohesion: 0.18
Nodes (13): _resume_address_payment_index(), _account_content(), run(), _read_text_region(), _add_button(), step(), _card_parts(), _field_target() (+5 more)

### Community 55 - "Amazon Android Tool — Giai đoạn A/B"
Cohesion: 0.29
Nodes (7): Amazon Android Tool — Giai đoạn A/B, Cài trên máy Windows mới, Dán nhiều proxy, Sử dụng, Trạng thái nghiệm thu, Yêu cầu, Điện thoại đám mây Swarmote

### Community 56 - "AppSettings"
Cohesion: 0.22
Nodes (7): save(), default_path(), AppSettings, load_settings(), save_settings(), settings_path(), SettingsTests

### Community 57 - "core.py"
Cohesion: 0.32
Nodes (18): adb(), available_memory_mb(), check_play(), connected_devices(), Device, device_avd_name(), device_resources(), emergency_stop() (+10 more)

### Community 58 - "setup.py"
Cohesion: 0.22
Nodes (13): app_data_dir(), avd_names(), configure_avd(), create_avd(), doctor(), executable(), installed_image(), run() (+5 more)

### Community 60 - "Amazon trên Swarmote"
Cohesion: 0.33
Nodes (5): Amazon trên Swarmote, Người dùng và công việc, Nền tảng, Điều chưa xác minh, Định hướng ngôn ngữ nếu xây dựng lại — 23/11/2026

### Community 61 - "Biên bản kiểm tra thực tế — 2026-11-12"
Cohesion: 0.07
Nodes (27): b6 Country US +1 — 14/11/2026, B6 cuộn quốc gia và chọn lại — 13/11/2026, Biên bản kiểm tra thực tế — 2026-11-12, Cài và đo UiAutomator2 theo phê duyệt mới — 13/11/2026, Cập nhật luồng mẻ trước đó — 2026-11-13, Dừng riêng một máy — 14/11/2026, Focus ô nhập b4–b11 — 14/11/2026, Ghim taskbar — 13/11/2026 (+19 more)

### Community 62 - "build_reload_payment_steps"
Cohesion: 0.13
Nodes (9): build_reload_payment_steps(), node(), ReloadPaymentTests, adb(), wait(), read(), read(), read() (+1 more)

### Community 63 - "Bộ cài chia sẻ Windows x64"
Cohesion: 0.50
Nodes (3): Bộ cài chia sẻ Windows x64, Dựng lại, Nguồn thành phần

### Community 64 - "SmoothScrollableFrame"
Cohesion: 0.07
Nodes (14): animations_enabled(), SmoothScrollableFrame, Bố cục, Bố cục được áp dụng, Chữ và tiến độ, Giao diện vận hành, Hướng thị giác, Kiểm chứng và phạm vi (+6 more)

### Community 65 - "node"
Cohesion: 0.16
Nodes (4): read(), read(), read(), node()

### Community 66 - "VERIFICATION.md"
Cohesion: 0.13
Nodes (13): Kết luận và tích hợp, Kết quả thực tế, So sánh bộ đọc trên q1 — 13/11/2026, Thành phần thiết bị, b1–b3 bắt buộc có ba cú bấm — 14/11/2026, b1–b3 ngẫu nhiên cho 12 máy — 14/11/2026, b1–b3 ngẫu nhiên trên 12 máy, không dùng OCR — 14/11/2026, b6 cuộn tới đáy rồi vuốt ngược — 14/11/2026 (+5 more)

### Community 67 - "001 — Tách dữ liệu từng mẻ và đối chiếu số hàng"
Cohesion: 0.29
Nodes (7): 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Rủi ro và bảo trì, Thiết kế yêu cầu, Điều kiện dừng

### Community 68 - "run_batch"
Cohesion: 0.16
Nodes (14): _phone_preparation_lock(), _prepare_phone(), _prepare_phone_locked(), progress(), stop_here(), run_batch(), fill_slots(), manually_selected() (+6 more)

### Community 69 - "time"
Cohesion: 0.16
Nodes (14): print_json(), main(), check_runtime(), main(), verify(), _app_installed(), _app_paths(), _check_external_apps() (+6 more)

### Community 71 - "PROJECT_HANDOFF.md"
Cohesion: 0.10
Nodes (19): b1–b3 ngẫu nhiên cho q1–q12 — 14/11/2026, B4–b11 chạy đồng thời và OCR — 14/11/2026, b6 US +1 còn mở sau bốn cú chạm — 14/11/2026, Bản thử State Machine q7 và b1–b3 mở mục con — 14/11/2026, Bỏ thời hạn tổng sau menu — 14/11/2026, Bổ sung đọc ảnh OCR và chạm trực tiếp dự phòng cho b26 khi uiautomator dump WebView lỗi — 19/11/2026, Cơ chế chụp ảnh OCR quét chữ ấn luôn cho toàn bộ b26–b31 — 19/11/2026, File chính đã sửa (+11 more)

### Community 74 - "ProfilesNavigationTests"
Cohesion: 0.08
Nodes (19): _activate_manager(), create_profile(), _create_profile_form(), _invoke(), ProfileCreateNotSubmitted, _proxy_test_country(), ProxyConfig, ProxyTestFailed (+11 more)

### Community 75 - ".test_missing_target_fallback_backs_then_uses_fresh_locale_text_on_all_modes_and_slots"
Cohesion: 0.22
Nodes (4): tap(), read(), back(), read()

### Community 77 - ".test_tail_child_page_scrolls_then_backs_before_next_menu_choice"
Cohesion: 0.25
Nodes (3): browse(), tap(), tap()

### Community 79 - "StatusCell"
Cohesion: 0.13
Nodes (3): StatusCell, TableText, Tooltip

### Community 80 - "main"
Cohesion: 0.15
Nodes (9): main(), main(), Đợt tăng tốc và tự phục hồi b4–b11 ngày 13/11/2026, File dự án mà Graphify không phân tích trực tiếp, .gitignore, Launch Swarmote Tool.pyw, pyproject.toml, Ảnh PNG trong dự án (+1 more)

### Community 81 - "ProfileManagerWindowError"
Cohesion: 0.29
Nodes (3): ProfileManagerWindowError, ManagerStartupTests, unavailable()

### Community 82 - "Bàn giao dừng theo yêu cầu người dùng — 13/11/2026"
Cohesion: 0.29
Nodes (6): Bàn giao dừng theo yêu cầu người dùng — 13/11/2026, Bối cảnh đã hoàn tất trước lỗi hiện tại, Cách tiếp tục, Kiểm chứng gần nhất, Lỗi chính chưa xử lý xong, Yêu cầu mới nhất

### Community 83 - "RunJob"
Cohesion: 0.13
Nodes (9): AccountData, RunJob, DesktopResumeTests, apartment_type(), PreparationThreadsTests, run(), install(), install() (+1 more)

### Community 84 - "Bàn giao trạng thái dự án — 13/11/2026"
Cohesion: 0.09
Nodes (17): set_tk_icon(), B6 danh sách quốc gia vẫn mở sau khi chọn — 13/11/2026, Bàn giao trạng thái dự án — 13/11/2026, Bản chính boom4may và bản dự phòng — 14/11/2026, Bộ cài offline chia sẻ — 14/11/2026, Cài đặt máy mới, Dừng riêng máy đang chọn — 14/11/2026, Hàng đợi 4 máy với giới hạn 2 Running — 14/11/2026 (+9 more)

### Community 87 - "RegistrationState"
Cohesion: 0.05
Nodes (12): RegistrationState, build_tail_steps(), open_menu(), view(), visit_seconds(), _choose_tail_target(), _TailChoicesExhausted, RandomPrefixTests (+4 more)

### Community 88 - "ToolError"
Cohesion: 0.10
Nodes (15): ToolError, _confirm_menu_fallback(), _menu_evidence(), MenuReadUnavailable, _nodes(), budget(), open_home_menu(), ready_for_home_menu() (+7 more)

### Community 89 - "_proxy_postal_prefix"
Cohesion: 0.48
Nodes (3): _proxy_postal_prefix(), controls(), ProxyPostalPrefixTests

### Community 90 - "validate_card"
Cohesion: 0.40
Nodes (3): validate_card(), _unfiltered_single_page(), Đã có trong graph

### Community 92 - "GRAPH_AUDIT.md"
Cohesion: 0.67
Nodes (3): Cách kiểm tra sau mỗi sửa đổi, Giới hạn đã xác nhận, Kiểm tra độ phủ Graphify — cập nhật 26/11/2026

### Community 93 - "_prefix_nodes"
Cohesion: 0.50
Nodes (3): _prefix_nodes(), 14 ảnh menu chung b1–b3 ngẫu nhiên — 14/11/2026, B1–B3 hiện hành — Ba lượt ngẫu nhiên q1–q12

### Community 96 - "cloud_adb"
Cohesion: 0.08
Nodes (29): _read_hierarchy(), scroll_view(), wait_until(), cloud_adb(), RecoverableStepError, build_random_steps(), browse(), action() (+21 more)

### Community 100 - "OTP_DESIGN.md"
Cohesion: 0.50
Nodes (3): Nối vào bước tạo tài khoản sau khi xác minh màn hình Amazon, Thiết kế OTP cho từng Profile, Đã chuẩn bị

## Knowledge Gaps
- **1 isolated node(s):** `amazon-android-tool`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 582 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **19 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ToolError` connect `ToolError` to `AttemptDeadline`, `build_common_steps`, `otp.py`, `BulkInputTests`, `swarmote_desktop.py`, `RunnerTests`, `PostMenuStep`, `ToolError`, `AddressDetailTests`, `screen`, `RunJob`, `desktop.py`, `cli.py`, `MarketplaceFlowTests`, `amazon_is_foreground`, `._start_post_menu`, `build_change_us_steps`, `Q7StateMachineTests`, `_tail_menu`, `CloudPhone`, `build_random_steps`, `build_random_steps`, `ui_backend.py`, `isolated_reader.py`, `_visible`, `registration.py`, `_type_field`, `build_create_address_steps`, `_read_nodes`, `Window`, `test_q1_flow.py`, `CountryRecoveryTests`, `bulk_input.py`, `vision.py`, `reload_payment_flow.py`, `AppSettings`, `core.py`, `setup.py`, `BatchDraft`, `build_reload_payment_steps`, `run_batch`, `.__init__`, `ProfilesNavigationTests`, `ProfileManagerWindowError`, `RunJob`, `RegistrationState`, `validate_card`, `_prefix_nodes`, `cloud_adb`?**
  _High betweenness centrality (0.345) - this node is a cross-community bridge._
- **Are the 61 inferred relationships involving `ToolError` (e.g. with `_read_nodes_once()` and `_resume_address_payment_index()`) actually correct?**
  _`ToolError` has 61 INFERRED edges - model-reasoned connections that need verification._
- **What connects `amazon-android-tool` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `build_common_steps` be split into smaller, more focused modules?**
  _Cohesion score 0.0522466039707419 - nodes in this community are weakly interconnected._
- **Why does `RunJob` connect `RunJob` to `AttemptDeadline`, `build_common_steps`, `BulkInputTests`, `swarmote_desktop.py`, `RunnerTests`, `PostMenuStep`, `RunJob`, `desktop.py`, `MarketplaceFlowTests`, `._start_post_menu`, `Q3Q4FlowTests`, `build_change_us_steps`, `Q7StateMachineTests`, `CloudPhone`, `build_random_steps`, `build_random_steps`, `_type_field`, `_read_nodes`, `Window`, `._refresh_devices`, `test_q1_flow.py`, `CountryRecoveryTests`, `bulk_input.py`, `build_reload_payment_steps`, `node`, `run_batch`, `.__init__`, `ProfilesNavigationTests`, `.test_missing_target_fallback_backs_then_uses_fresh_locale_text_on_all_modes_and_slots`, `q5_flow.py`, `RegistrationState`, `Q2FlowTests`, `cloud_adb`, `OTP_DESIGN.md`?**
  _High betweenness centrality (0.105) - this node is a cross-community bridge._
- **Are the 89 inferred relationships involving `CloudPhone` (e.g. with `build_common_steps()` and `_country_full_row()`) actually correct?**
  _`CloudPhone` has 89 INFERRED edges - model-reasoned connections that need verification._
- **Should `otp.py` be split into smaller, more focused modules?**
  _Cohesion score 0.10080645161290322 - nodes in this community are weakly interconnected._