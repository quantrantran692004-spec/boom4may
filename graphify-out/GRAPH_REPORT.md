# Graph Report - boom4may  (2026-11-21)

## Corpus Check
- 131 files · ~154,470 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 1, .bat 1, .pyw 1)

## Summary
- 2067 nodes · 7294 edges · 87 communities (73 shown, 14 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 1036 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `9587f861`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- CloudPhone
- build_common_steps
- otp.py
- BulkInputTests
- screen
- open_adb_shell
- RunnerTests
- PostMenuSession
- .test_only_confirmed_target_names_are_selected_for_one_start_command
- AddressDetailTests
- 003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật
- Danh mục từng bước đã biết — 13/11/2026
- run_batch
- StopResetTests
- account_flow.py
- amazon-android-tool
- Ảnh hướng dẫn q1/q2 và menu chung lưu cục bộ
- ._run
- MarketplaceFlowTests
- _text
- account_flow.py
- Điều hướng hai dạng menu ba gạch
- random_prefix.py
- RunJob
- Nghiên cứu và tích hợp Swarmote
- Q7StateMachineTests
- _tail_candidates
- vision.py
- _tap_child
- RegistrationState
- PROJECT_INDEX.md
- ._build_main
- _visual_form_button
- _type_field
- ToolError
- _visible
- RecoverableStepError
- Window
- core.py
- Q3Q4FlowTests
- setup.py
- Bàn giao trạng thái dự án — 13/11/2026
- SafetyTests
- FakeControl
- isolated_reader.py
- time
- ProxyConfig
- build_random_steps
- cli.py
- AppSettings
- b1–b11 Reliability and Latency Implementation Plan
- subprocess
- Danh mục ảnh nằm trong dự án
- ensure_manager_ready
- Amazon Android Tool — Giai đoạn A/B
- CountryRecoveryTests
- RandomPrefixTests
- Giao diện vận hành
- cloud_adb
- Amazon trên Swarmote
- amazon_is_foreground
- build_reload_payment_steps
- Bộ cài chia sẻ Windows x64
- adb
- main
- VERIFICATION.md
- _CombinedStop
- Biên bản kiểm tra thực tế — 2026-11-12
- .test_selected_stop_finishes_install_before_stopping_that_phone
- windows_identity.py
- PROJECT_HANDOFF.md
- _proxy_postal_prefix
- BatchDraft
- swarmote_desktop.py
- _choose_tail_target
- q5_flow.py
- Q5_FLOW.md
- Bàn giao dừng theo yêu cầu người dùng — 13/11/2026
- ._apply_bulk_text
- GRAPH_AUDIT.md
- Giai đoạn 2 — bản thử State Machine riêng q7
- build_q1_steps
- OTP_DESIGN.md
- retry_preparation
- PreparationProgressTests

## God Nodes (most connected - your core abstractions)
1. `ToolError` - 345 edges
2. `CloudPhone` - 229 edges
3. `AttemptDeadline` - 193 edges
4. `RunJob` - 161 edges
5. `RegistrationState` - 146 edges
6. `build_common_steps()` - 113 edges
7. `Window` - 94 edges
8. `Q1FlowTests` - 91 edges
9. `PostMenuStep` - 88 edges
10. `PostMenuSession` - 79 edges

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

## Communities (87 total, 14 thin omitted)

### Community 0 - "CloudPhone"
Cohesion: 0.09
Nodes (22): CloudPhone, package_path(), probe(), prop(), reported_installer(), require_online(), reconcile(), route() (+14 more)

### Community 1 - "build_common_steps"
Cohesion: 0.05
Nodes (6): build_common_steps(), node(), Q1FlowTests, read(), provider_read(), read()

### Community 2 - "otp.py"
Cohesion: 0.10
Nodes (9): browser_launch_options(), extract_otp(), _NoRedirect, read_otp(), _read_otp_in_browser(), validate_otp_url(), wait_for_new_otp(), OtpTests (+1 more)

### Community 3 - "BulkInputTests"
Cohesion: 0.06
Nodes (14): BulkRecord, lines(), parse_bulk_payload(), parse_column(), parse_records(), _proxy_rows(), _table_cells(), _url_from_cell() (+6 more)

### Community 4 - "screen"
Cohesion: 0.10
Nodes (30): confirmed_login_otp_nodes(), continue_number(), enter_otp(), finish_auto(), finish_create(), finish_login(), focus_otp(), name() (+22 more)

### Community 5 - "open_adb_shell"
Cohesion: 0.12
Nodes (22): _check_stop(), collapse_apps_panel(), install_amazon(), collect(), open_adb_shell(), _pause(), _phone_window(), _progress_reporter() (+14 more)

### Community 6 - "RunnerTests"
Cohesion: 0.06
Nodes (19): ProfileRegistry, ProfileNotFound, absent(), ProfileRegistryTests, lookup(), broken(), RunnerTests, create() (+11 more)

### Community 7 - "PostMenuSession"
Cohesion: 0.07
Nodes (19): PostMenuSession, PostMenuStep, RecoverableStepError, sign_in(), _first_point(), _size(), Một quy luật để sửa mã về sau — 20/11/2026, PostMenuTests (+11 more)

### Community 8 - ".test_only_confirmed_target_names_are_selected_for_one_start_command"
Cohesion: 0.11
Nodes (6): BatchStartTests, checkbox(), toggle(), descendants(), FakeBox, FakeButton

### Community 9 - "AddressDetailTests"
Cohesion: 0.12
Nodes (6): build_create_address_detail_steps(), AddressDetailTests, adb(), tap(), read(), item()

### Community 10 - "003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật"
Cohesion: 0.08
Nodes (20): 003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật, Các bước, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Quy trình đích, Rủi ro và bảo trì, Điều kiện dừng (+12 more)

### Community 11 - "Danh mục từng bước đã biết — 13/11/2026"
Cohesion: 0.06
Nodes (35): Bản thử q7 State Machine — 14/11/2026, Chung b10 — Chuyển WhatsApp sang SMS, Chung b11 — Lấy và gõ OTP SMS, Chung b11a — Chạm ô OTP trên màn SMS, Chung b11b — Xác minh đăng nhập hoặc bấm Create của luồng tạo, Chung b4 — Sign In từ menu, Chung b4a — Chạm ô SĐT, Chung b5 — Gõ số điện thoại (+27 more)

### Community 12 - "run_batch"
Cohesion: 0.13
Nodes (15): _prepare_phone(), _prepare_phone_locked(), progress(), stop_here(), run_batch(), fill_slots(), refresh_slots(), requested() (+7 more)

### Community 14 - "account_flow.py"
Cohesion: 0.16
Nodes (6): menu_layout(), _parse_ui_nodes(), route_list_menu(), _UiReadIncomplete, verify_menu_open(), cloud_screenshot()

### Community 16 - "Ảnh hướng dẫn q1/q2 và menu chung lưu cục bộ"
Cohesion: 0.07
Nodes (28): B16–b22 chung — Đổi marketplace sang United States (18/11/2026), B32–b39 — Reload Balance, thêm thẻ và địa chỉ thanh toán (21/11/2026), B6 — Hai ảnh đính kèm mới ngày 13/11/2026, Menu chung ảnh 01 — Danh sách chữ, Menu chung ảnh 02 — App Store bên phải sau khi Amazon mở, q1 b6 — US +1 hiện nhưng chạm không đóng hộp, 14/11/2026, q1 ảnh 01 — Menu và ba thẻ, q1 ảnh 02 — Sign In cuối menu (+20 more)

### Community 17 - "._run"
Cohesion: 0.20
Nodes (8): 002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ, Các bước, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Rủi ro và bảo trì, Thiết kế yêu cầu, Điều kiện dừng

### Community 18 - "MarketplaceFlowTests"
Cohesion: 0.07
Nodes (22): AttemptDeadline, MarketplaceFlowTests, read(), adb(), read(), tap(), read(), read() (+14 more)

### Community 19 - "_text"
Cohesion: 0.17
Nodes (26): _button(), _account_tab(), build_marketplace_steps(), run(), account_target(), back_and_read_text(), foreground_ready(), recover_country_list() (+18 more)

### Community 20 - "account_flow.py"
Cohesion: 0.17
Nodes (24): _at_or_after(), country(), proceed(), sign_in(), _country_nodes(), _CountryReadStop, _ensure_menu(), _find_scrolling() (+16 more)

### Community 21 - "Điều hướng hai dạng menu ba gạch"
Cohesion: 0.50
Nodes (4): Bằng chứng và phạm vi, Kiểm chứng, Quy tắc chạy, Điều hướng hai dạng menu ba gạch

### Community 22 - "random_prefix.py"
Cohesion: 0.12
Nodes (15): _read_nodes_once(), _read_visual_nodes(), amazon_is_foreground(), current(), _read(), _read_text_region(), _first_point(), _prefix_nodes() (+7 more)

### Community 24 - "RunJob"
Cohesion: 0.11
Nodes (10): _automatic_resume_slots(), AccountData, RunJob, DesktopResumeTests, apartment_type(), PreparationThreadsTests, run(), install() (+2 more)

### Community 25 - "Nghiên cứu và tích hợp Swarmote"
Cohesion: 0.40
Nodes (4): Hành vi có bằng chứng, Kiểm thử còn lại, Nghiên cứu và tích hợp Swarmote, Phần đã áp dụng

### Community 26 - "Q7StateMachineTests"
Cohesion: 0.08
Nodes (17): ActionValidator, _already_reached_result(), build_q7_pilot_steps(), run(), _past_known_step(), RecoveryHandler, ResultVerifier, StateDeadline (+9 more)

### Community 27 - "_tail_candidates"
Cohesion: 0.29
Nodes (4): _tail_candidates(), _tail_input_action(), _tail_safe_page_choices(), Chung b12–b15 — Mở ba gạch rồi ba lượt điều hướng ngẫu nhiên

### Community 28 - "vision.py"
Cohesion: 0.07
Nodes (19): _bounds(), _canonical_text(), _compact(), _engine(), _field_contents(), _field_is_blank(), _input_box(), _join_wrapped_categories() (+11 more)

### Community 29 - "_tap_child"
Cohesion: 0.24
Nodes (6): browse(), action(), run_browse(), PrefixDeadline, Q7PrefixTimeout, _tap_child()

### Community 30 - "RegistrationState"
Cohesion: 0.16
Nodes (4): RegistrationState, build_tail_steps(), open_menu(), view()

### Community 31 - "PROJECT_INDEX.md"
Cohesion: 0.18
Nodes (8): Quy trình Swarmote hiện tại, Bản đồ repository, Luồng q1 từ menu ba gạch tới nhập OTP, Thử trên q1 đã có, Luồng q2 từ menu ba gạch, q3 — b1–b3 và nối luồng chung, q4 — Giỏ hàng, Pets, Home and DIY, q6 — Trang chủ, Giỏ hàng, menu và một thẻ

### Community 33 - "_visual_form_button"
Cohesion: 0.50
Nodes (3): _ActionNotResolved, _visual_form_button(), _yellow_form_button()

### Community 34 - "_type_field"
Cohesion: 0.18
Nodes (5): focus_phone(), _tap_input(), _type_field(), FlowRecoveryTests, form()

### Community 35 - "ToolError"
Cohesion: 0.07
Nodes (21): open_amazon(), foreground(), ToolError, _confirm_menu_fallback(), _menu_evidence(), MenuReadUnavailable, _nodes(), budget() (+13 more)

### Community 36 - "_visible"
Cohesion: 0.16
Nodes (31): _bounds(), _same_country_position(), _text(), _visible(), _action(), _address_form(), _addresses(), run() (+23 more)

### Community 37 - "RecoverableStepError"
Cohesion: 0.18
Nodes (5): build_random_steps(), RandomPrefixTests, adb(), adb(), adb()

### Community 39 - "core.py"
Cohesion: 0.27
Nodes (19): adb(), available_memory_mb(), check_play(), configure_avd(), connected_devices(), Device, device_avd_name(), device_resources() (+11 more)

### Community 40 - "Q3Q4FlowTests"
Cohesion: 0.15
Nodes (3): build_q3_steps(), build_q4_steps(), Q3Q4FlowTests

### Community 41 - "setup.py"
Cohesion: 0.16
Nodes (16): app_data_dir(), avd_names(), create_avd(), doctor(), executable(), installed_image(), run(), sdk_root() (+8 more)

### Community 42 - "Bàn giao trạng thái dự án — 13/11/2026"
Cohesion: 0.11
Nodes (18): B6 danh sách quốc gia vẫn mở sau khi chọn — 13/11/2026, Bàn giao trạng thái dự án — 13/11/2026, Bản chính boom4may và bản dự phòng — 14/11/2026, Bộ cài offline chia sẻ — 14/11/2026, Cài đặt máy mới, Dừng riêng máy đang chọn — 14/11/2026, Dự phòng dùng chung khi chạy song song — 14/11/2026, q3/q4 đã nối b1–b3 và thử đồng thời bốn luồng — 13/11/2026 (+10 more)

### Community 44 - "FakeControl"
Cohesion: 0.13
Nodes (5): ParallelInstallTests, PhoneWindow, FakeControl, InstallTests, descendants()

### Community 45 - "isolated_reader.py"
Cohesion: 0.20
Nodes (8): phone_reader(), PhoneReader, ReaderResponseError, _serve(), fake_worker(), IsolationTests, duplicate(), production_worker_with_fake_android()

### Community 46 - "time"
Cohesion: 0.13
Nodes (11): swarmote_adb_path(), swarmote_tunnel_owner(), _connect(), country_reverse_points(), country_scroll(), _failed(), read_tree(), ready() (+3 more)

### Community 47 - "ProxyConfig"
Cohesion: 0.08
Nodes (18): _activate_manager(), create_profile(), _create_profile_form(), _invoke(), _open_profiles(), ProfileCreateNotSubmitted, ProxyConfig, ProxyTestFailed (+10 more)

### Community 48 - "build_random_steps"
Cohesion: 0.20
Nodes (3): resume_common_index(), build_random_steps(), finish_view()

### Community 49 - "cli.py"
Cohesion: 0.17
Nodes (11): BatchItem, parse_proxy_line(), prepare_five(), main(), parser(), report(), scan(), get_device() (+3 more)

### Community 50 - "AppSettings"
Cohesion: 0.15
Nodes (9): _new_prefix(), save(), default_path(), AppSettings, load_settings(), save_settings(), settings_path(), Tăng số lần thử đọc cây Android và bổ sung phương án dự phòng cho b23–b31 — 19/11/2026 (+1 more)

### Community 51 - "b1–b11 Reliability and Latency Implementation Plan"
Cohesion: 0.18
Nodes (10): b1–b11 Reliability and Latency Implementation Plan, Completion Criteria, File Map, Global Constraints, Review Focus, Task 1: Measure current step latency and classify existing failures, Task 2: Define safe retry, reconcile, pause, and stop behavior, Task 3: Reduce redundant UI reads and unnecessary waits (+2 more)

### Community 52 - "subprocess"
Cohesion: 0.32
Nodes (8): _app_installed(), _app_paths(), _check_external_apps(), _install_python_dependencies(), main(), _offer_downloads(), _ready_file_matches(), _runtime_imports_work()

### Community 53 - "Danh mục ảnh nằm trong dự án"
Cohesion: 0.25
Nodes (8): amazon_android/assets/obsidian_prism.png, assets/ui_history/machine7_input_before.png, assets/ui_history/reset_check.png, assets/ui_history/ui-12.png, assets/ui_history/ui_palette_preview.png, assets/ui_history/ui-preview.png, assets/ui_history/ui-screenshot.png, Danh mục ảnh nằm trong dự án

### Community 54 - "ensure_manager_ready"
Cohesion: 0.32
Nodes (3): ensure_manager_ready(), _swarmote_exe(), ManagerStartupTests

### Community 55 - "Amazon Android Tool — Giai đoạn A/B"
Cohesion: 0.29
Nodes (7): Amazon Android Tool — Giai đoạn A/B, Cài trên máy Windows mới, Dán nhiều proxy, Sử dụng, Trạng thái nghiệm thu, Yêu cầu, Điện thoại đám mây Swarmote

### Community 56 - "CountryRecoveryTests"
Cohesion: 0.27
Nodes (4): CountryRecoveryTests, read(), wait(), node()

### Community 58 - "Giao diện vận hành"
Cohesion: 0.40
Nodes (4): Bố cục, Giao diện vận hành, Hướng thị giác, Quy tắc

### Community 59 - "cloud_adb"
Cohesion: 0.15
Nodes (25): _country_full_row(), _keyboard_visible(), _read_hierarchy(), _scroll_up(), _tap(), cloud_adb(), _foreground(), _scroll_country() (+17 more)

### Community 60 - "Amazon trên Swarmote"
Cohesion: 0.40
Nodes (4): Amazon trên Swarmote, Người dùng và công việc, Nền tảng, Điều chưa xác minh

### Community 61 - "amazon_is_foreground"
Cohesion: 0.14
Nodes (4): cloud_serials(), CloudBridgeTests, adb(), Ẩn cửa sổ cmd khi gọi ADB — 2026-11-13

### Community 62 - "build_reload_payment_steps"
Cohesion: 0.08
Nodes (18): Hướng dẫn khi tiếp tục dự án, build_create_address_steps(), build_post_auth_steps(), build_reload_payment_steps(), Nhận diện giao diện lúc chạy, Nhập liệu và lỗi, Quy tắc tự động hóa sau menu ba gạch, Trạng thái hiện tại của dự án (+10 more)

### Community 63 - "Bộ cài chia sẻ Windows x64"
Cohesion: 0.50
Nodes (3): Bộ cài chia sẻ Windows x64, Dựng lại, Nguồn thành phần

### Community 64 - "adb"
Cohesion: 0.10
Nodes (5): adb(), tap(), adb(), adb(), tap()

### Community 65 - "main"
Cohesion: 0.16
Nodes (9): main(), main(), Đợt tăng tốc và tự phục hồi b4–b11 ngày 13/11/2026, File dự án mà Graphify không phân tích trực tiếp, .gitignore, Launch Swarmote Tool.pyw, pyproject.toml, Ảnh PNG trong dự án (+1 more)

### Community 66 - "VERIFICATION.md"
Cohesion: 0.17
Nodes (10): Kết luận và tích hợp, Kết quả thực tế, So sánh bộ đọc trên q1 — 13/11/2026, Thành phần thiết bị, b1–b3 bắt buộc có ba cú bấm — 14/11/2026, b1–b3 ngẫu nhiên cho 12 máy — 14/11/2026, b1–b3 ngẫu nhiên trên 12 máy, không dùng OCR — 14/11/2026, b6 cuộn tới đáy rồi vuốt ngược — 14/11/2026 (+2 more)

### Community 68 - "Biên bản kiểm tra thực tế — 2026-11-12"
Cohesion: 0.08
Nodes (25): b6 Country US +1 — 14/11/2026, B6 cuộn quốc gia và chọn lại — 13/11/2026, Biên bản kiểm tra thực tế — 2026-11-12, Cài và đo UiAutomator2 theo phê duyệt mới — 13/11/2026, Cập nhật luồng mẻ trước đó — 2026-11-13, Dừng riêng một máy — 14/11/2026, Focus ô nhập b4–b11 — 14/11/2026, Ghim taskbar — 13/11/2026 (+17 more)

### Community 70 - "windows_identity.py"
Cohesion: 0.24
Nodes (6): create_shortcut(), relaunch_command(), runtime(), set_process_identity(), set_window_identity(), WindowsIdentityTests

### Community 71 - "PROJECT_HANDOFF.md"
Cohesion: 0.12
Nodes (16): b1–b3 ngẫu nhiên cho q1–q12 — 14/11/2026, B4–b11 chạy đồng thời và OCR — 14/11/2026, b6 US +1 còn mở sau bốn cú chạm — 14/11/2026, Bản thử State Machine q7 và b1–b3 mở mục con — 14/11/2026, Bỏ thời hạn tổng sau menu — 14/11/2026, Bổ sung đọc ảnh OCR và chạm trực tiếp dự phòng cho b26 khi uiautomator dump WebView lỗi — 19/11/2026, Cơ chế chụp ảnh OCR quét chữ ấn luôn cho toàn bộ b26–b31 — 19/11/2026, Không bỏ qua b1–b3 ngẫu nhiên; 14 ảnh menu mới — 14/11/2026 (+8 more)

### Community 72 - "_proxy_postal_prefix"
Cohesion: 0.48
Nodes (3): _proxy_postal_prefix(), controls(), ProxyPostalPrefixTests

### Community 74 - "swarmote_desktop.py"
Cohesion: 0.14
Nodes (19): _descendants(), inspect(), _main_window(), _one(), _profile_checkbox(), _profile_form_open(), _profile_row_status(), profile_status() (+11 more)

### Community 75 - "_choose_tail_target"
Cohesion: 0.20
Nodes (4): _choose_tail_target(), _TailChoicesExhausted, choose(), choose()

### Community 78 - "Bàn giao dừng theo yêu cầu người dùng — 13/11/2026"
Cohesion: 0.25
Nodes (7): Bàn giao dừng theo yêu cầu người dùng — 13/11/2026, Bằng chứng trực tiếp đã có, Bối cảnh đã hoàn tất trước lỗi hiện tại, Cách tiếp tục, Kiểm chứng gần nhất, Lỗi chính chưa xử lý xong, Yêu cầu mới nhất

### Community 80 - "._apply_bulk_text"
Cohesion: 0.15
Nodes (8): 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng, Các bước, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Rủi ro và bảo trì, Thiết kế yêu cầu, Điều kiện dừng

### Community 81 - "GRAPH_AUDIT.md"
Cohesion: 0.50
Nodes (3): Cách kiểm tra sau mỗi sửa đổi, Giới hạn đã xác nhận, Kiểm tra độ phủ Graphify — 13/11/2026

### Community 82 - "Giai đoạn 2 — bản thử State Machine riêng q7"
Cohesion: 0.33
Nodes (5): Cách thử thật q7 sau khi người dùng sẵn sàng, Giai đoạn 2 — bản thử State Machine riêng q7, Giới hạn, Phạm vi và quan hệ với luồng cũ, Sơ đồ

### Community 83 - "build_q1_steps"
Cohesion: 0.17
Nodes (7): build_q1_steps(), category(), build_q2_steps(), Cách xử lý ảnh tiếp theo, Phần riêng từng máy, Tiến độ hướng dẫn bằng ảnh — cập nhật 13/11/2026, Q2FlowTests

### Community 84 - "OTP_DESIGN.md"
Cohesion: 0.50
Nodes (3): Nối vào bước tạo tài khoản sau khi xác minh màn hình Amazon, Thiết kế OTP cho từng Profile, Đã chuẩn bị

### Community 91 - "retry_preparation"
Cohesion: 0.20
Nodes (4): emit(), _phone_preparation_lock(), retry_preparation(), P03 — Mở form New Profile

## Knowledge Gaps
- **1 isolated node(s):** `amazon-android-tool`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 498 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **14 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ToolError` connect `ToolError` to `CloudPhone`, `build_common_steps`, `otp.py`, `BulkInputTests`, `screen`, `open_adb_shell`, `RunnerTests`, `PostMenuSession`, `.test_only_confirmed_target_names_are_selected_for_one_start_command`, `AddressDetailTests`, `run_batch`, `StopResetTests`, `account_flow.py`, `._run`, `MarketplaceFlowTests`, `_text`, `account_flow.py`, `random_prefix.py`, `threading`, `RunJob`, `Q7StateMachineTests`, `vision.py`, `_tap_child`, `RegistrationState`, `_visual_form_button`, `_type_field`, `_visible`, `RecoverableStepError`, `Window`, `core.py`, `Q3Q4FlowTests`, `setup.py`, `isolated_reader.py`, `time`, `ProxyConfig`, `build_random_steps`, `cli.py`, `AppSettings`, `ensure_manager_ready`, `CountryRecoveryTests`, `RandomPrefixTests`, `cloud_adb`, `amazon_is_foreground`, `build_reload_payment_steps`, `adb`, `.test_selected_stop_finishes_install_before_stopping_that_phone`, `BatchDraft`, `swarmote_desktop.py`, `_choose_tail_target`, `._apply_bulk_text`, `build_q1_steps`, `retry_preparation`?**
  _High betweenness centrality (0.392) - this node is a cross-community bridge._
- **Are the 57 inferred relationships involving `ToolError` (e.g. with `_read_nodes_once()` and `resume_common_index()`) actually correct?**
  _`ToolError` has 57 INFERRED edges - model-reasoned connections that need verification._
- **What connects `amazon-android-tool` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `CloudPhone` be split into smaller, more focused modules?**
  _Cohesion score 0.09302325581395349 - nodes in this community are weakly interconnected._
- **Why does `RunJob` connect `RunJob` to `CloudPhone`, `build_common_steps`, `BulkInputTests`, `screen`, `RunnerTests`, `PostMenuSession`, `run_batch`, `StopResetTests`, `account_flow.py`, `._run`, `MarketplaceFlowTests`, `account_flow.py`, `random_prefix.py`, `threading`, `Q7StateMachineTests`, `RegistrationState`, `_type_field`, `RecoverableStepError`, `Window`, `Q3Q4FlowTests`, `Bàn giao trạng thái dự án — 13/11/2026`, `ProxyConfig`, `build_random_steps`, `CountryRecoveryTests`, `RandomPrefixTests`, `build_reload_payment_steps`, `adb`, `.test_selected_stop_finishes_install_before_stopping_that_phone`, `_choose_tail_target`, `build_q1_steps`, `OTP_DESIGN.md`, `retry_preparation`?**
  _High betweenness centrality (0.105) - this node is a cross-community bridge._
- **Are the 88 inferred relationships involving `CloudPhone` (e.g. with `build_common_steps()` and `_country_full_row()`) actually correct?**
  _`CloudPhone` has 88 INFERRED edges - model-reasoned connections that need verification._
- **Should `build_common_steps` be split into smaller, more focused modules?**
  _Cohesion score 0.0533515731874145 - nodes in this community are weakly interconnected._