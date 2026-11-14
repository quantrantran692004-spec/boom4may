# Graph Report - boom4may  (2026-11-14)

## Corpus Check
- 122 files · ~96,521 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 1, .bat 1, .pyw 1)

## Summary
- 1542 nodes · 5196 edges · 82 communities (65 shown, 17 thin omitted)
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 766 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `237a6412`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ToolError
- Q1FlowTests
- otp.py
- parse_records
- account_flow.py
- _prepare_phone
- RunnerTests
- PostMenuSession
- .test_only_confirmed_target_names_are_selected_for_one_start_command
- PROJECT_INDEX.md
- 002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ
- Danh mục từng bước đã biết — 13/11/2026
- start_device
- q7_state_machine.py
- _type_field
- amazon-android-tool
- Ảnh hướng dẫn q1/q2 và menu chung lưu cục bộ
- Biên bản kiểm tra thực tế — 2026-11-12
- ensure_manager_ready
- isolated_reader.py
- screen
- subprocess
- registration.py
- _read_nodes
- StopResetTests
- Nghiên cứu và tích hợp Swarmote
- Q3Q4FlowTests
- CloudPhone
- vision.py
- setup.py
- time
- pathlib
- cloud_adb
- core.py
- CloudPhone
- SafetyTests
- profile_status
- Bàn giao dừng theo yêu cầu người dùng — 13/11/2026
- AttemptDeadline
- Điều hướng hai dạng menu ba gạch
- time
- Bàn giao trạng thái dự án — 13/11/2026
- CloudBridgeTests
- FakeControl
- RecoverableStepError
- PROJECT_HANDOFF.md
- BatchDraft
- build_q2_steps
- CountryRecoveryTests
- Window
- b1–b11 Reliability and Latency Implementation Plan
- RunJob
- Danh mục ảnh nằm trong dự án
- build_random_steps
- Amazon Android Tool — Giai đoạn A/B
- run_batch
- OTP_DESIGN.md
- Giao diện vận hành
- Quy tắc tự động hóa sau menu ba gạch
- Amazon trên Swarmote
- windows_identity.py
- ResumeRegistrationStateTests
- Bộ cài chia sẻ Windows x64
- swarmote_desktop.py
- Kiểm tra độ phủ Graphify — 13/11/2026
- q7_random_prefix.py
- ._apply_bulk_text
- test_q1_flow.py
- 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng
- VERIFICATION.md
- run
- Store
- _field_for_label
- File dự án mà Graphify không phân tích trực tiếp
- _automatic_resume_slots
- _crystal_art
- PLAN.md
- Luồng q1 từ menu ba gạch tới nhập OTP
- Q5_FLOW.md
- PreparationProgressTests

## God Nodes (most connected - your core abstractions)
1. `ToolError` - 274 edges
2. `CloudPhone` - 185 edges
3. `RunJob` - 121 edges
4. `AttemptDeadline` - 112 edges
5. `Window` - 84 edges
6. `build_common_steps()` - 82 edges
7. `PostMenuStep` - 62 edges
8. `PostMenuSession` - 61 edges
9. `_read_nodes()` - 56 edges
10. `Q1FlowTests` - 51 edges

## Surprising Connections (you probably didn't know these)
- `Cách xử lý ảnh tiếp theo` --references--> `screen()`  [INFERRED]
  FLOW_PROGRESS.md → amazon_android/account_flow.py
- `b6 US +1 còn mở sau bốn cú chạm — 14/11/2026` --references--> `_wait_screen()`  [INFERRED]
  PROJECT_HANDOFF.md → amazon_android/account_flow.py
- `q6 b1–b3a riêng, b4–b11 chung — 14/11/2026` --references--> `_ensure_menu()`  [INFERRED]
  PROJECT_HANDOFF.md → amazon_android/account_flow.py
- `Điều tra q1/q2 mượt, q3+ lỗi thất thường khi chạy song song — 14/11/2026` --references--> `_ensure_menu()`  [INFERRED]
  PROJECT_HANDOFF.md → amazon_android/account_flow.py
- `Phần dùng chung đã được hướng dẫn` --references--> `build_common_steps()`  [INFERRED]
  FLOW_PROGRESS.md → amazon_android/account_flow.py

## Import Cycles
- None detected.

## Communities (82 total, 17 thin omitted)

### Community 0 - "ToolError"
Cohesion: 0.13
Nodes (17): BatchItem, parse_proxy_line(), prepare_five(), main(), parser(), report(), get_device(), print_json() (+9 more)

### Community 1 - "Q1FlowTests"
Cohesion: 0.09
Nodes (6): build_common_steps(), build_q1_steps(), category(), node(), Q1FlowTests, provider_read()

### Community 2 - "otp.py"
Cohesion: 0.09
Nodes (10): browser_launch_options(), extract_otp(), _NoRedirect, otp_token(), read_otp(), _read_otp_in_browser(), validate_otp_url(), wait_for_new_otp() (+2 more)

### Community 3 - "parse_records"
Cohesion: 0.09
Nodes (10): BulkRecord, lines(), parse_column(), parse_records(), _proxy_rows(), _table_cells(), _url_from_cell(), validate_card() (+2 more)

### Community 4 - "account_flow.py"
Cohesion: 0.15
Nodes (19): _ActionNotResolved, _bounds(), _country_full_row(), _keyboard_visible(), _parse_ui_nodes(), _read_hierarchy(), _read_nodes_once(), _read_visual_nodes() (+11 more)

### Community 5 - "_prepare_phone"
Cohesion: 0.08
Nodes (29): ready_for_home_menu(), progress(), _start_and_confirm(), _check_stop(), collapse_apps_panel(), install_amazon(), check_stop(), collect() (+21 more)

### Community 6 - "RunnerTests"
Cohesion: 0.06
Nodes (18): ProfileRegistry, ProfileNotFound, absent(), ProfileRegistryTests, lookup(), broken(), RunnerTests, create() (+10 more)

### Community 7 - "PostMenuSession"
Cohesion: 0.14
Nodes (9): route(), PostMenuSession, PostMenuStep, PostMenuTests, first_step(), reconcile(), first(), SharedStepRecoveryTests (+1 more)

### Community 8 - ".test_only_confirmed_target_names_are_selected_for_one_start_command"
Cohesion: 0.11
Nodes (6): BatchStartTests, checkbox(), toggle(), descendants(), FakeBox, FakeButton

### Community 9 - "PROJECT_INDEX.md"
Cohesion: 0.20
Nodes (6): Hướng dẫn khi tiếp tục dự án, Bản đồ repository, Luồng q2 từ menu ba gạch, q3 — b1–b3 và nối luồng chung, q4 — Giỏ hàng, Pets, Home and DIY, q6 — Trang chủ, Giỏ hàng, menu và một thẻ

### Community 10 - "002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ"
Cohesion: 0.06
Nodes (26): 002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ, Kiểm tra bắt buộc, Phạm vi, Rủi ro và bảo trì, Thiết kế yêu cầu, Điều kiện dừng, 003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật, Các bước (+18 more)

### Community 11 - "Danh mục từng bước đã biết — 13/11/2026"
Cohesion: 0.06
Nodes (36): B1–B3 hiện hành — Ba lượt ngẫu nhiên q1–q12, Bản thử q7 State Machine — 14/11/2026, Chung b10 — Chuyển WhatsApp sang SMS, Chung b11 — Lấy và gõ OTP SMS, Chung b11a — Chạm ô OTP trên màn SMS, Chung b11b — Bấm Create your Amazon account, Chung b4 — Sign In từ menu, Chung b4a — Chạm ô SĐT (+28 more)

### Community 12 - "start_device"
Cohesion: 0.37
Nodes (16): adb(), check_play(), connected_devices(), Device, device_avd_name(), device_resources(), emergency_stop(), emulator_processes() (+8 more)

### Community 13 - "q7_state_machine.py"
Cohesion: 0.10
Nodes (19): ActionValidator, build_q7_pilot_steps(), run(), RecoveryHandler, ResultVerifier, StateDeadline, StateDetector, StateMachineStop (+11 more)

### Community 14 - "_type_field"
Cohesion: 0.20
Nodes (5): _tap_input(), _type_field(), Phục hồi khi ô nhập chưa nhận focus ở b4–b11 — 14/11/2026, FlowRecoveryTests, form()

### Community 16 - "Ảnh hướng dẫn q1/q2 và menu chung lưu cục bộ"
Cohesion: 0.08
Nodes (26): 14 ảnh menu chung b1–b3 ngẫu nhiên — 14/11/2026, B6 — Hai ảnh đính kèm mới ngày 13/11/2026, Menu chung ảnh 01 — Danh sách chữ, Menu chung ảnh 02 — App Store bên phải sau khi Amazon mở, q1 b6 — US +1 hiện nhưng chạm không đóng hộp, 14/11/2026, q1 ảnh 01 — Menu và ba thẻ, q1 ảnh 02 — Sign In cuối menu, q1 ảnh 03 — Nhập số điện thoại (+18 more)

### Community 17 - "Biên bản kiểm tra thực tế — 2026-11-12"
Cohesion: 0.08
Nodes (26): b6 Country US +1 — 14/11/2026, B6 cuộn quốc gia và chọn lại — 13/11/2026, Biên bản kiểm tra thực tế — 2026-11-12, Cài và đo UiAutomator2 theo phê duyệt mới — 13/11/2026, Cập nhật luồng mẻ trước đó — 2026-11-13, Dừng riêng một máy — 14/11/2026, Focus ô nhập b4–b11 — 14/11/2026, Ghim taskbar — 13/11/2026 (+18 more)

### Community 18 - "ensure_manager_ready"
Cohesion: 0.22
Nodes (5): ensure_manager_ready(), ProfileManagerWindowError, _swarmote_exe(), ManagerStartupTests, unavailable()

### Community 19 - "isolated_reader.py"
Cohesion: 0.28
Nodes (6): phone_reader(), PhoneReader, ReaderResponseError, fake_worker(), IsolationTests, duplicate()

### Community 20 - "screen"
Cohesion: 0.19
Nodes (21): continue_number(), create_account(), enter_otp(), focus_otp(), focus_phone(), name(), phone_number(), proceed() (+13 more)

### Community 21 - "subprocess"
Cohesion: 0.15
Nodes (12): main(), main(), _app_installed(), _app_paths(), _check_external_apps(), _install_python_dependencies(), main(), _offer_downloads() (+4 more)

### Community 22 - "registration.py"
Cohesion: 0.30
Nodes (10): require_online(), fill_identifier(), fill_signup_form(), _nodes(), open_entry(), status(), _tap(), _type_into() (+2 more)

### Community 23 - "_read_nodes"
Cohesion: 0.20
Nodes (22): _at_or_after(), country(), sign_in(), _ensure_menu(), _find_scrolling(), _read_nodes(), _tap_for_transition(), _unique() (+14 more)

### Community 25 - "Nghiên cứu và tích hợp Swarmote"
Cohesion: 0.40
Nodes (4): Hành vi có bằng chứng, Kiểm thử còn lại, Nghiên cứu và tích hợp Swarmote, Phần đã áp dụng

### Community 26 - "Q3Q4FlowTests"
Cohesion: 0.23
Nodes (3): build_q3_steps(), build_q4_steps(), Q3Q4FlowTests

### Community 27 - "CloudPhone"
Cohesion: 0.14
Nodes (6): CloudPhone, reconcile(), type_characters(), HomeMenuTests, ParallelNavigationRegressionTests, SharedFallbackTests

### Community 28 - "vision.py"
Cohesion: 0.07
Nodes (18): _bounds(), _canonical_text(), _compact(), _engine(), _field_contents(), _field_is_blank(), _input_box(), _join_wrapped_categories() (+10 more)

### Community 29 - "setup.py"
Cohesion: 0.23
Nodes (11): avd_names(), create_avd(), doctor(), executable(), installed_image(), sdk_root(), confirm(), download_commandline_tools() (+3 more)

### Community 30 - "time"
Cohesion: 0.23
Nodes (5): _serve(), check_runtime(), main(), verify(), production_worker_with_fake_android()

### Community 31 - "pathlib"
Cohesion: 0.18
Nodes (7): save(), default_path(), AppSettings, load_settings(), save_settings(), settings_path(), SettingsTests

### Community 32 - "cloud_adb"
Cohesion: 0.20
Nodes (13): cloud_adb(), package_path(), probe(), prop(), reported_installer(), browse(), action(), run_browse() (+5 more)

### Community 33 - "core.py"
Cohesion: 0.15
Nodes (3): available_memory_mb(), apartment_type(), on_worker()

### Community 34 - "CloudPhone"
Cohesion: 0.18
Nodes (9): _confirm_menu_fallback(), _menu_evidence(), MenuReadUnavailable, _nodes(), budget(), open_home_menu(), _tap(), read() (+1 more)

### Community 37 - "profile_status"
Cohesion: 0.16
Nodes (7): _open_profiles(), ProfileCreateNotSubmitted, visible_profile_names(), control(), ProfilesNavigationTests, descendants(), descendants()

### Community 38 - "Bàn giao dừng theo yêu cầu người dùng — 13/11/2026"
Cohesion: 0.29
Nodes (6): Bàn giao dừng theo yêu cầu người dùng — 13/11/2026, Bối cảnh đã hoàn tất trước lỗi hiện tại, Cách tiếp tục, Kiểm chứng gần nhất, Lỗi chính chưa xử lý xong, Yêu cầu mới nhất

### Community 39 - "AttemptDeadline"
Cohesion: 0.13
Nodes (6): verify_menu_open(), AttemptDeadline, Bản thử State Machine q7 và b1–b3 mở mục con — 14/11/2026, read(), MenuReturnTests, Q6FlowTests

### Community 40 - "Điều hướng hai dạng menu ba gạch"
Cohesion: 0.50
Nodes (4): Bằng chứng và phạm vi, Kiểm chứng, Quy tắc chạy, Điều hướng hai dạng menu ba gạch

### Community 41 - "time"
Cohesion: 0.12
Nodes (12): swarmote_adb_path(), swarmote_tunnel_owner(), port_occupied(), _connect(), country_reverse_points(), country_scroll(), _failed(), read_tree() (+4 more)

### Community 42 - "Bàn giao trạng thái dự án — 13/11/2026"
Cohesion: 0.11
Nodes (18): B6 danh sách quốc gia vẫn mở sau khi chọn — 13/11/2026, Bàn giao trạng thái dự án — 13/11/2026, Bản chính boom4may và bản dự phòng — 14/11/2026, Bộ cài offline chia sẻ — 14/11/2026, Cài đặt máy mới, Dừng riêng máy đang chọn — 14/11/2026, Dự phòng dùng chung khi chạy song song — 14/11/2026, Mục tiêu và quy tắc đã chốt (+10 more)

### Community 43 - "CloudBridgeTests"
Cohesion: 0.22
Nodes (6): cloud_serials(), open_amazon(), foreground(), scan(), CloudBridgeTests, adb()

### Community 44 - "FakeControl"
Cohesion: 0.13
Nodes (5): ParallelInstallTests, PhoneWindow, FakeControl, InstallTests, descendants()

### Community 45 - "RecoverableStepError"
Cohesion: 0.13
Nodes (14): RecoverableStepError, build_random_steps(), browse(), action(), sign_in(), _menu(), _size(), RandomPrefixTests (+6 more)

### Community 46 - "PROJECT_HANDOFF.md"
Cohesion: 0.13
Nodes (14): b1–b3 ngẫu nhiên cho q1–q12 — 14/11/2026, B1–b3 xem menu ngẫu nhiên cho 12 máy — 14/11/2026, B4–b11 chạy đồng thời và OCR — 14/11/2026, b6 cuộn chạm đáy rồi vuốt ngược khoảng bốn quốc gia — 14/11/2026, b6 US +1 còn mở sau bốn cú chạm — 14/11/2026, Bỏ thời hạn tổng sau menu — 14/11/2026, Dán bảng Amazon có ghi chú thẻ live và URL OTP escaped — 14/11/2026, Dán nhiều proxy cách nhau bằng dấu cách — 14/11/2026 (+6 more)

### Community 48 - "build_q2_steps"
Cohesion: 0.22
Nodes (6): build_q2_steps(), Cách xử lý ảnh tiếp theo, Phần dùng chung đã được hướng dẫn, Phần riêng từng máy, Tiến độ hướng dẫn bằng ảnh — cập nhật 13/11/2026, Q2FlowTests

### Community 49 - "CountryRecoveryTests"
Cohesion: 0.27
Nodes (4): CountryRecoveryTests, read(), wait(), node()

### Community 51 - "b1–b11 Reliability and Latency Implementation Plan"
Cohesion: 0.18
Nodes (10): b1–b11 Reliability and Latency Implementation Plan, Completion Criteria, File Map, Global Constraints, Review Focus, Task 1: Measure current step latency and classify existing failures, Task 2: Define safe retry, reconcile, pause, and stop behavior, Task 3: Reduce redundant UI reads and unnecessary waits (+2 more)

### Community 52 - "RunJob"
Cohesion: 0.17
Nodes (6): AccountData, RunJob, DesktopResumeTests, PreparationThreadsTests, run(), install()

### Community 53 - "Danh mục ảnh nằm trong dự án"
Cohesion: 0.29
Nodes (7): amazon_android/assets/obsidian_prism.png, assets/ui_history/reset_check.png, assets/ui_history/ui-12.png, assets/ui_history/ui_palette_preview.png, assets/ui_history/ui-preview.png, assets/ui_history/ui-screenshot.png, Danh mục ảnh nằm trong dự án

### Community 54 - "build_random_steps"
Cohesion: 0.10
Nodes (10): RegistrationState, build_q5_steps(), build_random_steps(), Đợt tăng tốc và tự phục hồi b4–b11 ngày 13/11/2026, Phạm vi và quan hệ với luồng cũ, Q5FlowTests, RandomPrefixTests, adb() (+2 more)

### Community 55 - "Amazon Android Tool — Giai đoạn A/B"
Cohesion: 0.29
Nodes (7): Amazon Android Tool — Giai đoạn A/B, Cài trên máy Windows mới, Dán nhiều proxy, Sử dụng, Trạng thái nghiệm thu, Yêu cầu, Điện thoại đám mây Swarmote

### Community 56 - "run_batch"
Cohesion: 0.15
Nodes (14): emit(), pause_if_requested(), _prepare_phone(), stop_here(), run_batch(), fill_slots(), refresh_slots(), requested() (+6 more)

### Community 57 - "OTP_DESIGN.md"
Cohesion: 0.50
Nodes (3): Nối vào bước tạo tài khoản sau khi xác minh màn hình Amazon, Thiết kế OTP cho từng Profile, Đã chuẩn bị

### Community 58 - "Giao diện vận hành"
Cohesion: 0.40
Nodes (4): Bố cục, Giao diện vận hành, Hướng thị giác, Quy tắc

### Community 59 - "Quy tắc tự động hóa sau menu ba gạch"
Cohesion: 0.40
Nodes (5): Nhận diện giao diện lúc chạy, Nhập liệu và lỗi, Quy tắc tự động hóa sau menu ba gạch, Trạng thái hiện tại của dự án, Từng máy độc lập

### Community 60 - "Amazon trên Swarmote"
Cohesion: 0.40
Nodes (4): Amazon trên Swarmote, Người dùng và công việc, Nền tảng, Điều chưa xác minh

### Community 61 - "windows_identity.py"
Cohesion: 0.26
Nodes (6): create_shortcut(), relaunch_command(), runtime(), set_process_identity(), set_window_identity(), WindowsIdentityTests

### Community 62 - "ResumeRegistrationStateTests"
Cohesion: 0.25
Nodes (3): ResumeRegistrationStateTests, factory(), factory()

### Community 63 - "Bộ cài chia sẻ Windows x64"
Cohesion: 0.50
Nodes (3): Bộ cài chia sẻ Windows x64, Dựng lại, Nguồn thành phần

### Community 64 - "swarmote_desktop.py"
Cohesion: 0.12
Nodes (22): _activate_manager(), _create_profile_form(), _descendants(), inspect(), _invoke(), _main_window(), _one(), _profile_checkbox() (+14 more)

### Community 65 - "Kiểm tra độ phủ Graphify — 13/11/2026"
Cohesion: 0.67
Nodes (3): Cách kiểm tra sau mỗi sửa đổi, Giới hạn đã xác nhận, Kiểm tra độ phủ Graphify — 13/11/2026

### Community 68 - "test_q1_flow.py"
Cohesion: 0.28
Nodes (4): menu_layout(), resume_common_index(), route_list_menu(), Mã hiện có

### Community 69 - "001 — Tách dữ liệu từng mẻ và đối chiếu số hàng"
Cohesion: 0.29
Nodes (7): 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Rủi ro và bảo trì, Thiết kế yêu cầu, Điều kiện dừng

### Community 70 - "VERIFICATION.md"
Cohesion: 0.17
Nodes (10): Kết luận và tích hợp, Kết quả thực tế, So sánh bộ đọc trên q1 — 13/11/2026, Thành phần thiết bị, b1–b3 bắt buộc có ba cú bấm — 14/11/2026, b1–b3 ngẫu nhiên cho 12 máy — 14/11/2026, b1–b3 ngẫu nhiên trên 12 máy, không dùng OCR — 14/11/2026, b6 cuộn tới đáy rồi vuốt ngược — 14/11/2026 (+2 more)

### Community 71 - "run"
Cohesion: 0.40
Nodes (3): app_data_dir(), run(), Ẩn cửa sổ cmd khi gọi ADB — 2026-11-13

### Community 74 - "File dự án mà Graphify không phân tích trực tiếp"
Cohesion: 0.40
Nodes (5): File dự án mà Graphify không phân tích trực tiếp, .gitignore, Launch Swarmote Tool.pyw, pyproject.toml, Ảnh PNG trong dự án

## Knowledge Gaps
- **1 isolated node(s):** `amazon-android-tool`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 407 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **17 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ToolError` connect `ToolError` to `Q1FlowTests`, `otp.py`, `parse_records`, `account_flow.py`, `_prepare_phone`, `RunnerTests`, `PostMenuSession`, `.test_only_confirmed_target_names_are_selected_for_one_start_command`, `start_device`, `q7_state_machine.py`, `_type_field`, `ensure_manager_ready`, `isolated_reader.py`, `screen`, `registration.py`, `_read_nodes`, `StopResetTests`, `CloudPhone`, `vision.py`, `setup.py`, `time`, `pathlib`, `cloud_adb`, `core.py`, `CloudPhone`, `threading`, `profile_status`, `AttemptDeadline`, `time`, `CloudBridgeTests`, `RecoverableStepError`, `BatchDraft`, `build_q2_steps`, `CountryRecoveryTests`, `Window`, `RunJob`, `build_random_steps`, `run_batch`, `swarmote_desktop.py`, `q7_random_prefix.py`, `._apply_bulk_text`, `test_q1_flow.py`, `run`, `_field_for_label`?**
  _High betweenness centrality (0.390) - this node is a cross-community bridge._
- **Are the 48 inferred relationships involving `ToolError` (e.g. with `_read_nodes_once()` and `_tap_for_transition()`) actually correct?**
  _`ToolError` has 48 INFERRED edges - model-reasoned connections that need verification._
- **What connects `amazon-android-tool` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `ToolError` be split into smaller, more focused modules?**
  _Cohesion score 0.1282051282051282 - nodes in this community are weakly interconnected._
- **Why does `CloudPhone` connect `CloudPhone` to `ToolError`, `Q1FlowTests`, `account_flow.py`, `_prepare_phone`, `PostMenuSession`, `q7_state_machine.py`, `_type_field`, `isolated_reader.py`, `screen`, `registration.py`, `_read_nodes`, `Q3Q4FlowTests`, `time`, `cloud_adb`, `core.py`, `CloudPhone`, `threading`, `AttemptDeadline`, `time`, `CloudBridgeTests`, `RecoverableStepError`, `build_q2_steps`, `CountryRecoveryTests`, `Window`, `RunJob`, `build_random_steps`, `run_batch`, `ResumeRegistrationStateTests`, `swarmote_desktop.py`, `q7_random_prefix.py`, `test_q1_flow.py`, `.test_transition_keeps_observing_after_short_wait_without_tapping`?**
  _High betweenness centrality (0.101) - this node is a cross-community bridge._
- **Are the 79 inferred relationships involving `CloudPhone` (e.g. with `build_common_steps()` and `_country_full_row()`) actually correct?**
  _`CloudPhone` has 79 INFERRED edges - model-reasoned connections that need verification._
- **Should `Q1FlowTests` be split into smaller, more focused modules?**
  _Cohesion score 0.08653061224489796 - nodes in this community are weakly interconnected._