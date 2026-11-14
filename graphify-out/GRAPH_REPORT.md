# Graph Report - boom4may  (2026-11-14)

## Corpus Check
- 122 files · ~96,807 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 1, .bat 1, .pyw 1)

## Summary
- 1545 nodes · 5201 edges · 66 communities (58 shown, 8 thin omitted)
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 767 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `4d794644`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ToolError
- Q1FlowTests
- otp.py
- parse_records
- _read_nodes_once
- _prepare_phone
- RunnerTests
- PostMenuSession
- .test_only_confirmed_target_names_are_selected_for_one_start_command
- PROJECT_HANDOFF.md
- 002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ
- Danh mục từng bước đã biết — 13/11/2026
- start_device
- q7_state_machine.py
- _type_field
- amazon-android-tool
- Ảnh hướng dẫn q1/q2 và menu chung lưu cục bộ
- Biên bản kiểm tra thực tế — 2026-11-12
- profile_status
- batch.py
- screen
- setup_windows.py
- registration.py
- _read_nodes
- StopResetTests
- Nghiên cứu và tích hợp Swarmote
- Giai đoạn 2 — bản thử State Machine riêng q7
- vision.py
- setup.py
- pathlib
- cloud.py
- home_menu.py
- SafetyTests
- profile_status
- Bàn giao dừng theo yêu cầu người dùng — 13/11/2026
- CloudPhone
- Điều hướng hai dạng menu ba gạch
- time
- Bàn giao trạng thái dự án — 13/11/2026
- FakeControl
- RandomPrefixTests
- account_flow.py
- BatchDraft
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
- desktop.py
- ResumeRegistrationStateTests
- Bộ cài chia sẻ Windows x64
- swarmote_desktop.py
- cli.py
- main
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

## Communities (66 total, 8 thin omitted)

### Community 0 - "ToolError"
Cohesion: 0.12
Nodes (14): ToolError, _start_and_confirm(), create_profile(), _invoke(), _one(), _profile_checkbox(), ProxyConfig, _select_radio() (+6 more)

### Community 1 - "Q1FlowTests"
Cohesion: 0.08
Nodes (7): build_common_steps(), q3 — b1–b3 và nối luồng chung, q4 — Giỏ hàng, Pets, Home and DIY, q6 — Trang chủ, Giỏ hàng, menu và một thẻ, node(), Q1FlowTests, provider_read()

### Community 2 - "otp.py"
Cohesion: 0.09
Nodes (10): browser_launch_options(), extract_otp(), _NoRedirect, otp_token(), read_otp(), _read_otp_in_browser(), validate_otp_url(), wait_for_new_otp() (+2 more)

### Community 3 - "parse_records"
Cohesion: 0.09
Nodes (9): BulkRecord, lines(), parse_column(), parse_records(), _proxy_rows(), _table_cells(), _url_from_cell(), validate_card() (+1 more)

### Community 4 - "_read_nodes_once"
Cohesion: 0.36
Nodes (6): _read_hierarchy(), _read_nodes_once(), _read_visual_nodes(), _UiReadIncomplete, current(), fail()

### Community 5 - "_prepare_phone"
Cohesion: 0.12
Nodes (22): _check_stop(), collapse_apps_panel(), _descendants(), install_amazon(), check_stop(), open_adb_shell(), _pause(), _phone_window() (+14 more)

### Community 6 - "RunnerTests"
Cohesion: 0.06
Nodes (17): ProfileRegistry, absent(), ProfileRegistryTests, lookup(), broken(), RunnerTests, create(), resume() (+9 more)

### Community 7 - "PostMenuSession"
Cohesion: 0.14
Nodes (9): PostMenuSession, pause_if_requested(), PostMenuStep, PostMenuTests, first_step(), reconcile(), first(), SharedStepRecoveryTests (+1 more)

### Community 8 - ".test_only_confirmed_target_names_are_selected_for_one_start_command"
Cohesion: 0.10
Nodes (9): ProfileStartNotSubmitted, start_profile(), Hàng đợi 4 máy với giới hạn 2 Running — 14/11/2026, BatchStartTests, checkbox(), toggle(), descendants(), FakeBox (+1 more)

### Community 9 - "PROJECT_HANDOFF.md"
Cohesion: 0.10
Nodes (23): Hướng dẫn khi tiếp tục dự án, Cách xử lý ảnh tiếp theo, Phần dùng chung đã được hướng dẫn, Tiến độ hướng dẫn bằng ảnh — cập nhật 13/11/2026, Cách kiểm tra sau mỗi sửa đổi, Giới hạn đã xác nhận, Kiểm tra độ phủ Graphify — 13/11/2026, Quy trình Swarmote hiện tại (+15 more)

### Community 10 - "002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ"
Cohesion: 0.07
Nodes (25): 002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ, Kiểm tra bắt buộc, Phạm vi, Rủi ro và bảo trì, Điều kiện dừng, 003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật, Các bước, Kiểm tra bắt buộc (+17 more)

### Community 11 - "Danh mục từng bước đã biết — 13/11/2026"
Cohesion: 0.06
Nodes (36): B1–B3 hiện hành — Ba lượt ngẫu nhiên q1–q12, Bản thử q7 State Machine — 14/11/2026, Chung b10 — Chuyển WhatsApp sang SMS, Chung b11 — Lấy và gõ OTP SMS, Chung b11a — Chạm ô OTP trên màn SMS, Chung b11b — Bấm Create your Amazon account, Chung b4 — Sign In từ menu, Chung b4a — Chạm ô SĐT (+28 more)

### Community 12 - "start_device"
Cohesion: 0.28
Nodes (19): adb(), available_memory_mb(), check_play(), configure_avd(), connected_devices(), Device, device_avd_name(), device_resources() (+11 more)

### Community 13 - "q7_state_machine.py"
Cohesion: 0.11
Nodes (15): ActionValidator, build_q7_pilot_steps(), run(), RecoveryHandler, ResultVerifier, StateDeadline, StateDetector, StateMachineStop (+7 more)

### Community 14 - "_type_field"
Cohesion: 0.19
Nodes (4): _type_field(), Phục hồi khi ô nhập chưa nhận focus ở b4–b11 — 14/11/2026, FlowRecoveryTests, form()

### Community 16 - "Ảnh hướng dẫn q1/q2 và menu chung lưu cục bộ"
Cohesion: 0.08
Nodes (26): 14 ảnh menu chung b1–b3 ngẫu nhiên — 14/11/2026, B6 — Hai ảnh đính kèm mới ngày 13/11/2026, Menu chung ảnh 01 — Danh sách chữ, Menu chung ảnh 02 — App Store bên phải sau khi Amazon mở, q1 b6 — US +1 hiện nhưng chạm không đóng hộp, 14/11/2026, q1 ảnh 01 — Menu và ba thẻ, q1 ảnh 02 — Sign In cuối menu, q1 ảnh 03 — Nhập số điện thoại (+18 more)

### Community 17 - "Biên bản kiểm tra thực tế — 2026-11-12"
Cohesion: 0.05
Nodes (39): Kết luận và tích hợp, Kết quả thực tế, So sánh bộ đọc trên q1 — 13/11/2026, Thành phần thiết bị, b1–b3 bắt buộc có ba cú bấm — 14/11/2026, b1–b3 ngẫu nhiên cho 12 máy — 14/11/2026, b1–b3 ngẫu nhiên trên 12 máy, không dùng OCR — 14/11/2026, b6 Country US +1 — 14/11/2026 (+31 more)

### Community 18 - "profile_status"
Cohesion: 0.16
Nodes (8): visible_lookup(), _profile_row_status(), profile_status(), ProfileLookupError, ProfileNotFound, Các bước, Thiết kế yêu cầu, Nút New Profile trên Swarmote — 13/11/2026

### Community 19 - "batch.py"
Cohesion: 0.40
Nodes (4): BatchItem, parse_proxy_line(), prepare_five(), BatchSafetyTests

### Community 20 - "screen"
Cohesion: 0.14
Nodes (30): _ActionNotResolved, _bounds(), continue_number(), country(), create_account(), enter_otp(), focus_otp(), focus_phone() (+22 more)

### Community 21 - "setup_windows.py"
Cohesion: 0.32
Nodes (8): _app_installed(), _app_paths(), _check_external_apps(), _install_python_dependencies(), main(), _offer_downloads(), _ready_file_matches(), _runtime_imports_work()

### Community 22 - "registration.py"
Cohesion: 0.20
Nodes (12): require_online(), _field_for_label(), fill_identifier(), fill_signup_form(), _nodes(), open_entry(), status(), _tap() (+4 more)

### Community 23 - "_read_nodes"
Cohesion: 0.14
Nodes (31): _at_or_after(), sign_in(), _ensure_menu(), _find_scrolling(), home_visible(), menu_layout(), _parse_ui_nodes(), _read_nodes() (+23 more)

### Community 25 - "Nghiên cứu và tích hợp Swarmote"
Cohesion: 0.40
Nodes (4): Hành vi có bằng chứng, Kiểm thử còn lại, Nghiên cứu và tích hợp Swarmote, Phần đã áp dụng

### Community 26 - "Giai đoạn 2 — bản thử State Machine riêng q7"
Cohesion: 0.40
Nodes (5): Cách thử thật q7 sau khi người dùng sẵn sàng, Giai đoạn 2 — bản thử State Machine riêng q7, Giới hạn, Phạm vi và quan hệ với luồng cũ, Sơ đồ

### Community 28 - "vision.py"
Cohesion: 0.07
Nodes (18): _bounds(), _canonical_text(), _compact(), _engine(), _field_contents(), _field_is_blank(), _input_box(), _join_wrapped_categories() (+10 more)

### Community 29 - "setup.py"
Cohesion: 0.15
Nodes (16): app_data_dir(), avd_names(), create_avd(), doctor(), executable(), installed_image(), run(), sdk_root() (+8 more)

### Community 31 - "pathlib"
Cohesion: 0.22
Nodes (7): save(), default_path(), AppSettings, load_settings(), save_settings(), settings_path(), SettingsTests

### Community 32 - "cloud.py"
Cohesion: 0.10
Nodes (26): _country_full_row(), _keyboard_visible(), cloud_adb(), cloud_screenshot(), package_path(), probe(), prop(), reported_installer() (+18 more)

### Community 34 - "home_menu.py"
Cohesion: 0.07
Nodes (16): open_amazon(), foreground(), _confirm_menu_fallback(), _menu_evidence(), MenuReadUnavailable, _nodes(), budget(), open_home_menu() (+8 more)

### Community 37 - "profile_status"
Cohesion: 0.14
Nodes (9): _create_profile_form(), _open_profiles(), ProfileCreateNotSubmitted, ProxyTestFailed, visible_profile_names(), control(), ProfilesNavigationTests, descendants() (+1 more)

### Community 38 - "Bàn giao dừng theo yêu cầu người dùng — 13/11/2026"
Cohesion: 0.29
Nodes (6): Bàn giao dừng theo yêu cầu người dùng — 13/11/2026, Bối cảnh đã hoàn tất trước lỗi hiện tại, Cách tiếp tục, Kiểm chứng gần nhất, Lỗi chính chưa xử lý xong, Yêu cầu mới nhất

### Community 39 - "CloudPhone"
Cohesion: 0.07
Nodes (15): resume_common_index(), verify_menu_open(), CloudPhone, reconcile(), AttemptDeadline, type_characters(), build_q3_steps(), build_q4_steps() (+7 more)

### Community 40 - "Điều hướng hai dạng menu ba gạch"
Cohesion: 0.50
Nodes (4): Bằng chứng và phạm vi, Kiểm chứng, Quy tắc chạy, Điều hướng hai dạng menu ba gạch

### Community 41 - "time"
Cohesion: 0.08
Nodes (19): swarmote_adb_path(), swarmote_tunnel_owner(), phone_reader(), PhoneReader, ReaderResponseError, _serve(), _connect(), country_reverse_points() (+11 more)

### Community 42 - "Bàn giao trạng thái dự án — 13/11/2026"
Cohesion: 0.11
Nodes (19): B6 danh sách quốc gia vẫn mở sau khi chọn — 13/11/2026, Bàn giao trạng thái dự án — 13/11/2026, Bản chính boom4may và bản dự phòng — 14/11/2026, Bộ cài offline chia sẻ — 14/11/2026, Cài đặt máy mới, Dừng riêng máy đang chọn — 14/11/2026, Dự phòng dùng chung khi chạy song song — 14/11/2026, Mục tiêu và quy tắc đã chốt (+11 more)

### Community 44 - "FakeControl"
Cohesion: 0.13
Nodes (5): ParallelInstallTests, PhoneWindow, FakeControl, InstallTests, descendants()

### Community 45 - "RandomPrefixTests"
Cohesion: 0.21
Nodes (4): RandomPrefixTests, adb(), adb(), adb()

### Community 46 - "account_flow.py"
Cohesion: 0.14
Nodes (7): route(), RegistrationState, build_q5_steps(), build_random_steps(), browse(), b1–b3 ngẫu nhiên cho q1–q12 — 14/11/2026, Q5FlowTests

### Community 47 - "BatchDraft"
Cohesion: 0.15
Nodes (9): BatchDraft, 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Rủi ro và bảo trì, Thiết kế yêu cầu, Điều kiện dừng (+1 more)

### Community 49 - "CountryRecoveryTests"
Cohesion: 0.31
Nodes (4): CountryRecoveryTests, read(), wait(), node()

### Community 50 - "Window"
Cohesion: 0.11
Nodes (3): _edge_light(), Window, Các bước

### Community 51 - "b1–b11 Reliability and Latency Implementation Plan"
Cohesion: 0.18
Nodes (10): b1–b11 Reliability and Latency Implementation Plan, Completion Criteria, File Map, Global Constraints, Review Focus, Task 1: Measure current step latency and classify existing failures, Task 2: Define safe retry, reconcile, pause, and stop behavior, Task 3: Reduce redundant UI reads and unnecessary waits (+2 more)

### Community 52 - "RunJob"
Cohesion: 0.16
Nodes (8): AccountData, RunJob, DesktopResumeTests, apartment_type(), PreparationThreadsTests, run(), install(), on_worker()

### Community 53 - "Danh mục ảnh nằm trong dự án"
Cohesion: 0.25
Nodes (8): amazon_android/assets/obsidian_prism.png, assets/ui_history/machine7_input_before.png, assets/ui_history/reset_check.png, assets/ui_history/ui-12.png, assets/ui_history/ui_palette_preview.png, assets/ui_history/ui-preview.png, assets/ui_history/ui-screenshot.png, Danh mục ảnh nằm trong dự án

### Community 54 - "build_random_steps"
Cohesion: 0.14
Nodes (6): build_random_steps(), _first_point(), RandomPrefixTests, adb(), adb(), adb()

### Community 55 - "Amazon Android Tool — Giai đoạn A/B"
Cohesion: 0.29
Nodes (7): Amazon Android Tool — Giai đoạn A/B, Cài trên máy Windows mới, Dán nhiều proxy, Sử dụng, Trạng thái nghiệm thu, Yêu cầu, Điện thoại đám mây Swarmote

### Community 56 - "run_batch"
Cohesion: 0.25
Nodes (10): emit(), _prepare_phone(), progress(), stop_here(), run_batch(), fill_slots(), refresh_slots(), requested() (+2 more)

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

### Community 61 - "desktop.py"
Cohesion: 0.11
Nodes (8): _automatic_resume_slots(), _crystal_art(), create_shortcut(), relaunch_command(), runtime(), set_process_identity(), set_window_identity(), WindowsIdentityTests

### Community 62 - "ResumeRegistrationStateTests"
Cohesion: 0.27
Nodes (3): ResumeRegistrationStateTests, factory(), factory()

### Community 63 - "Bộ cài chia sẻ Windows x64"
Cohesion: 0.50
Nodes (3): Bộ cài chia sẻ Windows x64, Dựng lại, Nguồn thành phần

### Community 64 - "swarmote_desktop.py"
Cohesion: 0.10
Nodes (16): _activate_manager(), ensure_manager_ready(), inspect(), _main_window(), collect(), _profile_form_open(), ProfileManagerWindowError, _select_profile_rows() (+8 more)

### Community 72 - "cli.py"
Cohesion: 0.21
Nodes (9): main(), parser(), report(), cloud_serials(), scan(), get_device(), print_json(), Store (+1 more)

### Community 74 - "main"
Cohesion: 0.16
Nodes (9): main(), main(), Đợt tăng tốc và tự phục hồi b4–b11 ngày 13/11/2026, File dự án mà Graphify không phân tích trực tiếp, .gitignore, Launch Swarmote Tool.pyw, pyproject.toml, Ảnh PNG trong dự án (+1 more)

## Knowledge Gaps
- **1 isolated node(s):** `amazon-android-tool`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 408 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ToolError` connect `ToolError` to `Q1FlowTests`, `otp.py`, `parse_records`, `_read_nodes_once`, `_prepare_phone`, `RunnerTests`, `PostMenuSession`, `.test_only_confirmed_target_names_are_selected_for_one_start_command`, `start_device`, `q7_state_machine.py`, `_type_field`, `profile_status`, `batch.py`, `screen`, `registration.py`, `_read_nodes`, `StopResetTests`, `vision.py`, `setup.py`, `pathlib`, `cloud.py`, `home_menu.py`, `threading`, `profile_status`, `CloudPhone`, `time`, `RandomPrefixTests`, `account_flow.py`, `BatchDraft`, `CountryRecoveryTests`, `Window`, `build_random_steps`, `run_batch`, `desktop.py`, `swarmote_desktop.py`, `cli.py`?**
  _High betweenness centrality (0.393) - this node is a cross-community bridge._
- **Are the 48 inferred relationships involving `ToolError` (e.g. with `_read_nodes_once()` and `_tap_for_transition()`) actually correct?**
  _`ToolError` has 48 INFERRED edges - model-reasoned connections that need verification._
- **What connects `amazon-android-tool` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `ToolError` be split into smaller, more focused modules?**
  _Cohesion score 0.12169312169312169 - nodes in this community are weakly interconnected._
- **Why does `CloudPhone` connect `CloudPhone` to `ToolError`, `Q1FlowTests`, `_read_nodes_once`, `_prepare_phone`, `PostMenuSession`, `q7_state_machine.py`, `_type_field`, `profile_status`, `screen`, `registration.py`, `_read_nodes`, `cloud.py`, `home_menu.py`, `threading`, `time`, `RandomPrefixTests`, `account_flow.py`, `CountryRecoveryTests`, `Window`, `RunJob`, `build_random_steps`, `run_batch`, `desktop.py`, `ResumeRegistrationStateTests`, `swarmote_desktop.py`, `cli.py`?**
  _High betweenness centrality (0.105) - this node is a cross-community bridge._
- **Are the 79 inferred relationships involving `CloudPhone` (e.g. with `build_common_steps()` and `_country_full_row()`) actually correct?**
  _`CloudPhone` has 79 INFERRED edges - model-reasoned connections that need verification._
- **Should `Q1FlowTests` be split into smaller, more focused modules?**
  _Cohesion score 0.08163265306122448 - nodes in this community are weakly interconnected._