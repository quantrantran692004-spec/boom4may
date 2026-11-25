# Graph Report - boom4may  (2026-11-25)

## Corpus Check
- 131 files · ~157,325 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 1, .bat 1, .pyw 1)

## Summary
- 2087 nodes · 7354 edges · 86 communities (72 shown, 14 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 1041 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `9717246d`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- registration.py
- build_common_steps
- otp.py
- BulkInputTests
- swarmote_desktop.py
- swarmote_desktop.py
- RunnerTests
- PostMenuSession
- ToolError
- AddressDetailTests
- 003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật
- Danh mục từng bước đã biết — 13/11/2026
- run_batch
- StopResetTests
- bulk_input.py
- amazon-android-tool
- Ảnh hướng dẫn q1/q2 và menu chung lưu cục bộ
- MarketplaceFlowTests
- marketplace_flow.py
- _read_nodes
- Điều hướng hai dạng menu ba gạch
- _tail_menu
- pathlib
- RunJob
- Nghiên cứu và tích hợp Swarmote
- Q7StateMachineTests
- account_flow.py
- subprocess
- ._refresh_devices
- RegistrationState
- PROJECT_INDEX.md
- _type_field
- resume_common_index
- vision.py
- CloudPhone
- create_address_detail_flow.py
- build_random_steps
- _crystal_art
- build_create_address_steps
- Q3Q4FlowTests
- core.py
- Bàn giao trạng thái dự án — 13/11/2026
- .remaining
- FakeControl
- AppSettings
- ui_backend.py
- random_prefix.py
- PhoneReader
- ProfileManagerWindowError
- b1–b11 Reliability and Latency Implementation Plan
- ._apply_bulk_text
- Danh mục ảnh nằm trong dự án
- ExtendedRecoveryTests
- Amazon Android Tool — Giai đoạn A/B
- ._launch
- profile_status
- Giao diện vận hành
- reload_payment_flow.py
- Amazon trên Swarmote
- amazon_is_foreground
- build_reload_payment_steps
- Bộ cài chia sẻ Windows x64
- CountryRecoveryTests
- windows_identity.py
- VERIFICATION.md
- on_worker
- Biên bản kiểm tra thực tế — 2026-11-12
- action
- .test_selected_stop_finishes_install_before_stopping_that_phone
- PROJECT_HANDOFF.md
- _proxy_postal_prefix
- BatchDraft
- ProfilesNavigationTests
- Value
- File dự án mà Graphify không phân tích trực tiếp
- retry_preparation
- MenuReturnTests
- PLAN.md
- GRAPH_AUDIT.md
- _automatic_resume_slots
- OTP_DESIGN.md
- build_q1_steps
- PreparationProgressTests

## God Nodes (most connected - your core abstractions)
1. `ToolError` - 349 edges
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

## Communities (86 total, 14 thin omitted)

### Community 0 - "registration.py"
Cohesion: 0.11
Nodes (20): require_online(), ToolError, _field_for_label(), fill_identifier(), fill_signup_form(), _nodes(), open_entry(), status() (+12 more)

### Community 1 - "build_common_steps"
Cohesion: 0.06
Nodes (5): build_common_steps(), node(), Q1FlowTests, read(), read()

### Community 2 - "otp.py"
Cohesion: 0.11
Nodes (8): browser_launch_options(), extract_otp(), _NoRedirect, read_otp(), _read_otp_in_browser(), wait_for_new_otp(), OtpTests, PackagedBrowserTests

### Community 4 - "swarmote_desktop.py"
Cohesion: 0.12
Nodes (18): _activate_manager(), _descendants(), inspect(), _invoke(), _main_window(), collect(), _one(), _profile_checkbox() (+10 more)

### Community 5 - "swarmote_desktop.py"
Cohesion: 0.09
Nodes (28): _check_stop(), collapse_apps_panel(), install_amazon(), open_adb_shell(), _pause(), _phone_window(), _progress_reporter(), report() (+20 more)

### Community 6 - "RunnerTests"
Cohesion: 0.06
Nodes (17): ProfileRegistry, absent(), ProfileRegistryTests, lookup(), RunnerTests, create(), resume(), create() (+9 more)

### Community 7 - "PostMenuSession"
Cohesion: 0.06
Nodes (17): route(), PostMenuSession, PostMenuStep, build_q7_pilot_steps(), Một quy luật để sửa mã về sau — 20/11/2026, Cách thử thật q7 sau khi người dùng sẵn sàng, Giai đoạn 2 — bản thử State Machine riêng q7, Giới hạn (+9 more)

### Community 8 - "ToolError"
Cohesion: 0.10
Nodes (9): ProfileStartNotSubmitted, start_profile(), Hàng đợi 4 máy với giới hạn 2 Running — 14/11/2026, BatchStartTests, checkbox(), toggle(), descendants(), FakeBox (+1 more)

### Community 9 - "AddressDetailTests"
Cohesion: 0.12
Nodes (7): build_create_address_detail_steps(), AddressDetailTests, read(), adb(), tap(), read(), item()

### Community 10 - "003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật"
Cohesion: 0.08
Nodes (20): 003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật, Các bước, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Quy trình đích, Rủi ro và bảo trì, Điều kiện dừng (+12 more)

### Community 11 - "Danh mục từng bước đã biết — 13/11/2026"
Cohesion: 0.06
Nodes (35): Bản thử q7 State Machine — 14/11/2026, Chung b10 — Chuyển WhatsApp sang SMS, Chung b11 — Lấy và gõ OTP SMS, Chung b11a — Chạm ô OTP trên màn SMS, Chung b11b — Xác minh đăng nhập hoặc bấm Create của luồng tạo, Chung b4 — Sign In từ menu, Chung b4a — Chạm ô SĐT, Chung b5 — Gõ số điện thoại (+27 more)

### Community 12 - "run_batch"
Cohesion: 0.19
Nodes (10): _prepare_phone(), _prepare_phone_locked(), progress(), stop_here(), run_batch(), fill_slots(), refresh_slots(), requested() (+2 more)

### Community 14 - "bulk_input.py"
Cohesion: 0.11
Nodes (9): BulkRecord, lines(), parse_bulk_payload(), parse_column(), _proxy_rows(), _table_cells(), _url_from_cell(), Dán bảng Amazon có ghi chú thẻ live và URL OTP escaped — 14/11/2026 (+1 more)

### Community 16 - "Ảnh hướng dẫn q1/q2 và menu chung lưu cục bộ"
Cohesion: 0.07
Nodes (28): B16–b22 chung — Đổi marketplace sang United States (18/11/2026), B32–b39 — Reload Balance, thêm thẻ và địa chỉ thanh toán (21/11/2026), B6 — Hai ảnh đính kèm mới ngày 13/11/2026, Menu chung ảnh 01 — Danh sách chữ, Menu chung ảnh 02 — App Store bên phải sau khi Amazon mở, q1 b6 — US +1 hiện nhưng chạm không đóng hộp, 14/11/2026, q1 ảnh 01 — Menu và ba thẻ, q1 ảnh 02 — Sign In cuối menu (+20 more)

### Community 18 - "MarketplaceFlowTests"
Cohesion: 0.06
Nodes (23): AttemptDeadline, _CombinedStop, type_characters(), MarketplaceFlowTests, read(), adb(), read(), tap() (+15 more)

### Community 19 - "marketplace_flow.py"
Cohesion: 0.17
Nodes (26): _account_tab(), build_marketplace_steps(), run(), account_target(), back_and_read_text(), foreground_ready(), recover_country_list(), _country_card() (+18 more)

### Community 20 - "_read_nodes"
Cohesion: 0.15
Nodes (22): _at_or_after(), country(), sign_in(), _country_nodes(), _CountryReadStop, _ensure_menu(), _find_scrolling(), _read_nodes() (+14 more)

### Community 21 - "Điều hướng hai dạng menu ba gạch"
Cohesion: 0.50
Nodes (4): Bằng chứng và phạm vi, Kiểm chứng, Quy tắc chạy, Điều hướng hai dạng menu ba gạch

### Community 22 - "_tail_menu"
Cohesion: 0.14
Nodes (8): _tail_menu(), _tail_overlay(), Nhận diện giao diện lúc chạy, Nhập liệu và lỗi, Quy tắc tự động hóa sau menu ba gạch, Trạng thái hiện tại của dự án, Từng máy độc lập, Chung b12–b15 — Mở ba gạch rồi ba lượt điều hướng ngẫu nhiên

### Community 23 - "pathlib"
Cohesion: 0.18
Nodes (3): main(), main(), LauncherTests

### Community 24 - "RunJob"
Cohesion: 0.14
Nodes (5): AccountData, RunJob, DesktopResumeTests, Q2FlowTests, Q5FlowTests

### Community 25 - "Nghiên cứu và tích hợp Swarmote"
Cohesion: 0.40
Nodes (4): Hành vi có bằng chứng, Kiểm thử còn lại, Nghiên cứu và tích hợp Swarmote, Phần đã áp dụng

### Community 26 - "Q7StateMachineTests"
Cohesion: 0.13
Nodes (16): ActionValidator, _already_reached_result(), _browse_ready_after_sms(), run(), _past_known_step(), RecoveryHandler, ResultVerifier, StateDeadline (+8 more)

### Community 27 - "account_flow.py"
Cohesion: 0.09
Nodes (35): _ActionNotResolved, continue_number(), finish_auto(), finish_create(), finish_login(), name(), phone_number(), proceed() (+27 more)

### Community 28 - "subprocess"
Cohesion: 0.18
Nodes (12): main(), check_runtime(), main(), verify(), _app_installed(), _app_paths(), _check_external_apps(), _install_python_dependencies() (+4 more)

### Community 30 - "RegistrationState"
Cohesion: 0.06
Nodes (17): RegistrationState, build_random_steps(), browse(), build_tail_steps(), open_menu(), view(), _choose_tail_target(), _tail_candidates() (+9 more)

### Community 31 - "PROJECT_INDEX.md"
Cohesion: 0.21
Nodes (6): Hướng dẫn khi tiếp tục dự án, Bản đồ repository, Luồng q2 từ menu ba gạch, q3 — b1–b3 và nối luồng chung, q4 — Giỏ hàng, Pets, Home and DIY, q6 — Trang chủ, Giỏ hàng, menu và một thẻ

### Community 32 - "_type_field"
Cohesion: 0.12
Nodes (12): confirmed_login_otp_nodes(), enter_otp(), focus_otp(), focus_phone(), read_sms_form(), _field(), _read_login_sms_visual(), _tap_input() (+4 more)

### Community 33 - "resume_common_index"
Cohesion: 0.09
Nodes (3): ResumeRegistrationStateTests, factory(), factory()

### Community 34 - "vision.py"
Cohesion: 0.07
Nodes (19): _bounds(), _canonical_text(), _compact(), _engine(), _field_contents(), _field_is_blank(), _input_box(), _join_wrapped_categories() (+11 more)

### Community 35 - "CloudPhone"
Cohesion: 0.10
Nodes (17): CloudPhone, reconcile(), _confirm_menu_fallback(), _menu_evidence(), MenuReadUnavailable, _nodes(), budget(), open_home_menu() (+9 more)

### Community 36 - "create_address_detail_flow.py"
Cohesion: 0.18
Nodes (27): _bounds(), _text(), _visible(), _action(), _address_form(), _addresses(), _bounded_native(), run() (+19 more)

### Community 37 - "build_random_steps"
Cohesion: 0.16
Nodes (5): build_random_steps(), RandomPrefixTests, adb(), adb(), adb()

### Community 39 - "build_create_address_steps"
Cohesion: 0.27
Nodes (4): build_create_address_steps(), CreateAddressFlowTests, read(), node()

### Community 40 - "Q3Q4FlowTests"
Cohesion: 0.21
Nodes (3): build_q3_steps(), build_q4_steps(), Q3Q4FlowTests

### Community 41 - "core.py"
Cohesion: 0.08
Nodes (43): BatchItem, parse_proxy_line(), prepare_five(), main(), parser(), report(), scan(), adb() (+35 more)

### Community 42 - "Bàn giao trạng thái dự án — 13/11/2026"
Cohesion: 0.11
Nodes (19): B6 danh sách quốc gia vẫn mở sau khi chọn — 13/11/2026, Bàn giao trạng thái dự án — 13/11/2026, Bản chính boom4may và bản dự phòng — 14/11/2026, Bộ cài offline chia sẻ — 14/11/2026, Cài đặt máy mới, Dừng riêng máy đang chọn — 14/11/2026, Dự phòng dùng chung khi chạy song song — 14/11/2026, q3/q4 đã nối b1–b3 và thử đồng thời bốn luồng — 13/11/2026 (+11 more)

### Community 43 - ".remaining"
Cohesion: 0.21
Nodes (11): _country_full_row(), _read_hierarchy(), _read_nodes_once(), _read_visual_nodes(), _scroll_up(), _UiReadIncomplete, current(), _serve() (+3 more)

### Community 44 - "FakeControl"
Cohesion: 0.13
Nodes (5): ParallelInstallTests, PhoneWindow, FakeControl, InstallTests, descendants()

### Community 45 - "AppSettings"
Cohesion: 0.22
Nodes (7): save(), default_path(), AppSettings, load_settings(), save_settings(), settings_path(), SettingsTests

### Community 46 - "ui_backend.py"
Cohesion: 0.13
Nodes (11): swarmote_adb_path(), swarmote_tunnel_owner(), _connect(), country_reverse_points(), country_scroll(), _failed(), read_tree(), ready() (+3 more)

### Community 47 - "random_prefix.py"
Cohesion: 0.06
Nodes (28): _new_prefix(), RecoverableStepError, browse(), action(), run_browse(), sign_in(), _first_point(), _menu() (+20 more)

### Community 48 - "PhoneReader"
Cohesion: 0.24
Nodes (7): phone_reader(), PhoneReader, ReaderResponseError, fake_worker(), IsolationTests, duplicate(), production_worker_with_fake_android()

### Community 49 - "ProfileManagerWindowError"
Cohesion: 0.28
Nodes (4): ensure_manager_ready(), ProfileManagerWindowError, ManagerStartupTests, unavailable()

### Community 51 - "b1–b11 Reliability and Latency Implementation Plan"
Cohesion: 0.18
Nodes (10): b1–b11 Reliability and Latency Implementation Plan, Completion Criteria, File Map, Global Constraints, Review Focus, Task 1: Measure current step latency and classify existing failures, Task 2: Define safe retry, reconcile, pause, and stop behavior, Task 3: Reduce redundant UI reads and unnecessary waits (+2 more)

### Community 52 - "._apply_bulk_text"
Cohesion: 0.16
Nodes (8): 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng, Các bước, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Rủi ro và bảo trì, Thiết kế yêu cầu, Điều kiện dừng

### Community 53 - "Danh mục ảnh nằm trong dự án"
Cohesion: 0.25
Nodes (8): amazon_android/assets/obsidian_prism.png, assets/ui_history/machine7_input_before.png, assets/ui_history/reset_check.png, assets/ui_history/ui-12.png, assets/ui_history/ui_palette_preview.png, assets/ui_history/ui-preview.png, assets/ui_history/ui-screenshot.png, Danh mục ảnh nằm trong dự án

### Community 54 - "ExtendedRecoveryTests"
Cohesion: 0.27
Nodes (3): ExtendedRecoveryTests, read(), menu()

### Community 55 - "Amazon Android Tool — Giai đoạn A/B"
Cohesion: 0.29
Nodes (7): Amazon Android Tool — Giai đoạn A/B, Cài trên máy Windows mới, Dán nhiều proxy, Sử dụng, Trạng thái nghiệm thu, Yêu cầu, Điện thoại đám mây Swarmote

### Community 56 - "._launch"
Cohesion: 0.15
Nodes (3): validate_card(), otp_token(), validate_otp_url()

### Community 57 - "profile_status"
Cohesion: 0.11
Nodes (15): visible_lookup(), _profile_row_status(), profile_status(), ProfileLookupError, ProfileNotFound, 002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ, Các bước, Kiểm tra bắt buộc (+7 more)

### Community 58 - "Giao diện vận hành"
Cohesion: 0.40
Nodes (4): Bố cục, Giao diện vận hành, Hướng thị giác, Quy tắc

### Community 59 - "reload_payment_flow.py"
Cohesion: 0.23
Nodes (17): _keyboard_visible(), cloud_adb(), reported_installer(), _scroll(), _foreground(), _read_text_region(), _scroll_country(), _size() (+9 more)

### Community 60 - "Amazon trên Swarmote"
Cohesion: 0.33
Nodes (5): Amazon trên Swarmote, Người dùng và công việc, Nền tảng, Điều chưa xác minh, Định hướng ngôn ngữ nếu xây dựng lại — 23/11/2026

### Community 61 - "amazon_is_foreground"
Cohesion: 0.11
Nodes (10): amazon_is_foreground(), cloud_serials(), open_amazon(), foreground(), package_path(), probe(), prop(), CloudBridgeTests (+2 more)

### Community 62 - "build_reload_payment_steps"
Cohesion: 0.16
Nodes (8): build_reload_payment_steps(), node(), ReloadPaymentTests, adb(), read(), read(), read(), read()

### Community 63 - "Bộ cài chia sẻ Windows x64"
Cohesion: 0.50
Nodes (3): Bộ cài chia sẻ Windows x64, Dựng lại, Nguồn thành phần

### Community 64 - "CountryRecoveryTests"
Cohesion: 0.27
Nodes (4): CountryRecoveryTests, read(), wait(), node()

### Community 65 - "windows_identity.py"
Cohesion: 0.23
Nodes (6): create_shortcut(), relaunch_command(), runtime(), set_process_identity(), set_window_identity(), WindowsIdentityTests

### Community 66 - "VERIFICATION.md"
Cohesion: 0.17
Nodes (10): Kết luận và tích hợp, Kết quả thực tế, So sánh bộ đọc trên q1 — 13/11/2026, Thành phần thiết bị, b1–b3 bắt buộc có ba cú bấm — 14/11/2026, b1–b3 ngẫu nhiên cho 12 máy — 14/11/2026, b1–b3 ngẫu nhiên trên 12 máy, không dùng OCR — 14/11/2026, b6 cuộn tới đáy rồi vuốt ngược — 14/11/2026 (+2 more)

### Community 67 - "on_worker"
Cohesion: 0.23
Nodes (5): apartment_type(), PreparationThreadsTests, run(), install(), on_worker()

### Community 68 - "Biên bản kiểm tra thực tế — 2026-11-12"
Cohesion: 0.08
Nodes (24): b6 Country US +1 — 14/11/2026, B6 cuộn quốc gia và chọn lại — 13/11/2026, Biên bản kiểm tra thực tế — 2026-11-12, Cài và đo UiAutomator2 theo phê duyệt mới — 13/11/2026, Dừng riêng một máy — 14/11/2026, Focus ô nhập b4–b11 — 14/11/2026, Ghim taskbar — 13/11/2026, Giao diện sáng, dễ đọc — 2026-11-13 (+16 more)

### Community 69 - "action"
Cohesion: 0.60
Nodes (5): read_menu(), return_to_menu(), visit(), action(), Tự động chuyển bước sau 60 giây nếu không thấy menu Browse ở b13–b15 — 19/11/2026

### Community 71 - "PROJECT_HANDOFF.md"
Cohesion: 0.12
Nodes (16): b1–b3 ngẫu nhiên cho q1–q12 — 14/11/2026, B4–b11 chạy đồng thời và OCR — 14/11/2026, b6 US +1 còn mở sau bốn cú chạm — 14/11/2026, Bản thử State Machine q7 và b1–b3 mở mục con — 14/11/2026, Bỏ thời hạn tổng sau menu — 14/11/2026, Bổ sung đọc ảnh OCR và chạm trực tiếp dự phòng cho b26 khi uiautomator dump WebView lỗi — 19/11/2026, Cơ chế chụp ảnh OCR quét chữ ấn luôn cho toàn bộ b26–b31 — 19/11/2026, Không bỏ qua b1–b3 ngẫu nhiên; 14 ảnh menu mới — 14/11/2026 (+8 more)

### Community 72 - "_proxy_postal_prefix"
Cohesion: 0.48
Nodes (3): _proxy_postal_prefix(), controls(), ProxyPostalPrefixTests

### Community 74 - "ProfilesNavigationTests"
Cohesion: 0.10
Nodes (14): create_profile(), _create_profile_form(), _open_profiles(), ProfileCreateNotSubmitted, ProxyConfig, ProxyTestFailed, visible_profile_names(), control() (+6 more)

### Community 77 - "File dự án mà Graphify không phân tích trực tiếp"
Cohesion: 0.40
Nodes (5): File dự án mà Graphify không phân tích trực tiếp, .gitignore, Launch Swarmote Tool.pyw, pyproject.toml, Ảnh PNG trong dự án

### Community 78 - "retry_preparation"
Cohesion: 0.18
Nodes (5): emit(), _phone_preparation_lock(), retry_preparation(), Mã hiện có, P03 — Mở form New Profile

### Community 80 - "PLAN.md"
Cohesion: 0.20
Nodes (4): Quy trình Swarmote hiện tại, Luồng q1 từ menu ba gạch tới nhập OTP, Thử trên q1 đã có, q5 — ba thẻ riêng và b4–b11 chung

### Community 81 - "GRAPH_AUDIT.md"
Cohesion: 0.50
Nodes (3): Cách kiểm tra sau mỗi sửa đổi, Giới hạn đã xác nhận, Kiểm tra độ phủ Graphify — 13/11/2026

### Community 84 - "OTP_DESIGN.md"
Cohesion: 0.50
Nodes (3): Nối vào bước tạo tài khoản sau khi xác minh màn hình Amazon, Thiết kế OTP cho từng Profile, Đã chuẩn bị

### Community 92 - "build_q1_steps"
Cohesion: 0.11
Nodes (8): menu_layout(), route_list_menu(), build_q1_steps(), category(), build_q5_steps(), Cách xử lý ảnh tiếp theo, Phần riêng từng máy, Tiến độ hướng dẫn bằng ảnh — cập nhật 13/11/2026

## Knowledge Gaps
- **1 isolated node(s):** `amazon-android-tool`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 502 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **14 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ToolError` connect `registration.py` to `build_common_steps`, `otp.py`, `BulkInputTests`, `swarmote_desktop.py`, `swarmote_desktop.py`, `RunnerTests`, `PostMenuSession`, `ToolError`, `AddressDetailTests`, `run_batch`, `StopResetTests`, `bulk_input.py`, `core.py`, `MarketplaceFlowTests`, `marketplace_flow.py`, `_read_nodes`, `_tail_menu`, `pathlib`, `RunJob`, `Q7StateMachineTests`, `account_flow.py`, `._refresh_devices`, `RegistrationState`, `_type_field`, `resume_common_index`, `vision.py`, `CloudPhone`, `create_address_detail_flow.py`, `build_random_steps`, `build_create_address_steps`, `core.py`, `.remaining`, `AppSettings`, `ui_backend.py`, `random_prefix.py`, `PhoneReader`, `ProfileManagerWindowError`, `batch_state.py`, `._apply_bulk_text`, `ExtendedRecoveryTests`, `._launch`, `profile_status`, `reload_payment_flow.py`, `amazon_is_foreground`, `build_reload_payment_steps`, `CountryRecoveryTests`, `action`, `.test_selected_stop_finishes_install_before_stopping_that_phone`, `BatchDraft`, `ProfilesNavigationTests`, `retry_preparation`?**
  _High betweenness centrality (0.423) - this node is a cross-community bridge._
- **Are the 57 inferred relationships involving `ToolError` (e.g. with `_read_nodes_once()` and `resume_common_index()`) actually correct?**
  _`ToolError` has 57 INFERRED edges - model-reasoned connections that need verification._
- **What connects `amazon-android-tool` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `registration.py` be split into smaller, more focused modules?**
  _Cohesion score 0.10668563300142248 - nodes in this community are weakly interconnected._
- **Why does `CloudPhone` connect `CloudPhone` to `registration.py`, `build_common_steps`, `swarmote_desktop.py`, `swarmote_desktop.py`, `PostMenuSession`, `AddressDetailTests`, `run_batch`, `core.py`, `MarketplaceFlowTests`, `marketplace_flow.py`, `_read_nodes`, `_tail_menu`, `RunJob`, `Q7StateMachineTests`, `account_flow.py`, `._refresh_devices`, `RegistrationState`, `_type_field`, `resume_common_index`, `build_random_steps`, `build_create_address_steps`, `Q3Q4FlowTests`, `core.py`, `.remaining`, `AppSettings`, `ui_backend.py`, `random_prefix.py`, `PhoneReader`, `ExtendedRecoveryTests`, `._launch`, `profile_status`, `reload_payment_flow.py`, `amazon_is_foreground`, `build_reload_payment_steps`, `CountryRecoveryTests`, `MenuReturnTests`, `build_q1_steps`?**
  _High betweenness centrality (0.095) - this node is a cross-community bridge._
- **Are the 88 inferred relationships involving `CloudPhone` (e.g. with `build_common_steps()` and `_country_full_row()`) actually correct?**
  _`CloudPhone` has 88 INFERRED edges - model-reasoned connections that need verification._
- **Should `build_common_steps` be split into smaller, more focused modules?**
  _Cohesion score 0.055077452667814115 - nodes in this community are weakly interconnected._