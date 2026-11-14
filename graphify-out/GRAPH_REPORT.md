# Graph Report - boom4may  (2026-11-14)

## Corpus Check
- 108 files · ~82,518 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 1, .bat 1, .pyw 1)

## Summary
- 1316 nodes · 4263 edges · 67 communities (58 shown, 9 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 583 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e51229bb`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- core.py
- build_common_steps
- time
- Window
- registration.py
- open_adb_shell
- RunnerTests
- PostMenuSession
- .test_only_confirmed_target_names_are_selected_for_one_start_command
- PROJECT_INDEX.md
- 002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ
- Danh mục từng bước đã biết — 13/11/2026
- bulk_input.py
- account_flow.py
- Biên bản kiểm tra thực tế — 2026-11-12
- amazon-android-tool
- Ảnh hướng dẫn q1/q2 và menu chung lưu cục bộ
- desktop.py
- _read_nodes
- ToolError
- run_batch
- BatchDraft
- ._label
- screen
- Nghiên cứu và tích hợp Swarmote
- validate_otp_url
- 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng
- vision.py
- ui_backend.py
- home_menu.py
- test_q3_q4_flow.py
- subprocess
- RunJob
- _type_field
- CloudPhone
- RecoverableStepError
- profile_status
- swarmote_desktop.py
- setup_windows.py
- route_list_menu
- Bàn giao trạng thái dự án — 13/11/2026
- windows_identity.py
- FakeControl
- b1–b11 Reliability and Latency Implementation Plan
- MENU_ROUTING.md
- PROJECT_HANDOFF.md
- CloudBridgeTests
- CountryRecoveryTests
- sys
- VERIFICATION.md
- ResumeRegistrationStateTests
- Danh mục ảnh nằm trong dự án
- Bàn giao dừng theo yêu cầu người dùng — 13/11/2026
- Amazon Android Tool — Giai đoạn A/B
- PreparationThreadsTests
- Giao diện vận hành
- Quy tắc tự động hóa sau menu ba gạch
- Amazon trên Swarmote
- File dự án mà Graphify không phân tích trực tiếp
- OTP_DESIGN.md
- Bộ cài chia sẻ Windows x64
- _NoRedirect
- Kiểm tra độ phủ Graphify — 13/11/2026
- PreparationProgressTests

## God Nodes (most connected - your core abstractions)
1. `ToolError` - 239 edges
2. `CloudPhone` - 146 edges
3. `RunJob` - 82 edges
4. `Window` - 77 edges
5. `AttemptDeadline` - 74 edges
6. `build_common_steps()` - 70 edges
7. `Q1FlowTests` - 51 edges
8. `_read_nodes()` - 49 edges
9. `screen()` - 42 edges
10. `PostMenuSession` - 41 edges

## Surprising Connections (you probably didn't know these)
- `Cách xử lý ảnh tiếp theo` --references--> `screen()`  [INFERRED]
  FLOW_PROGRESS.md → amazon_android/account_flow.py
- `b6 US +1 còn mở sau bốn cú chạm — 14/11/2026` --references--> `_wait_screen()`  [INFERRED]
  PROJECT_HANDOFF.md → amazon_android/account_flow.py
- `Trạng thái hiện tại của dự án` --references--> `build_common_steps()`  [INFERRED]
  POST_MENU_REQUIREMENTS.md → amazon_android/account_flow.py
- `Phạm vi q1–q12 sau phản hồi người dùng — 14/11/2026` --references--> `build_common_steps()`  [INFERRED]
  PROJECT_HANDOFF.md → amazon_android/account_flow.py
- `Tài liệu chi tiết` --references--> `build_common_steps()`  [INFERRED]
  PROJECT_HANDOFF.md → amazon_android/account_flow.py

## Import Cycles
- None detected.

## Communities (67 total, 9 thin omitted)

### Community 0 - "core.py"
Cohesion: 0.09
Nodes (39): BatchItem, parse_proxy_line(), prepare_five(), main(), parser(), report(), adb(), app_data_dir() (+31 more)

### Community 1 - "build_common_steps"
Cohesion: 0.07
Nodes (11): build_common_steps(), build_q1_steps(), category(), Cách xử lý ảnh tiếp theo, Phần dùng chung đã được hướng dẫn, Phần riêng từng máy, Tiến độ hướng dẫn bằng ảnh — cập nhật 13/11/2026, Đã có trong graph (+3 more)

### Community 2 - "time"
Cohesion: 0.12
Nodes (7): browser_launch_options(), extract_otp(), read_otp(), _read_otp_in_browser(), wait_for_new_otp(), OtpTests, PackagedBrowserTests

### Community 4 - "registration.py"
Cohesion: 0.21
Nodes (11): _field_for_label(), fill_identifier(), fill_signup_form(), _nodes(), open_entry(), status(), _tap(), _type_into() (+3 more)

### Community 5 - "open_adb_shell"
Cohesion: 0.10
Nodes (21): _check_stop(), ensure_manager_ready(), install_amazon(), check_stop(), collect(), open_adb_shell(), _pause(), _phone_window() (+13 more)

### Community 6 - "RunnerTests"
Cohesion: 0.06
Nodes (16): ProfileRegistry, ProfileLookupError, Thiết kế yêu cầu, absent(), ProfileRegistryTests, lookup(), broken(), RunnerTests (+8 more)

### Community 7 - "PostMenuSession"
Cohesion: 0.19
Nodes (4): PostMenuSession, PostMenuStep, PostMenuTests, first_step()

### Community 8 - ".test_only_confirmed_target_names_are_selected_for_one_start_command"
Cohesion: 0.11
Nodes (6): BatchStartTests, checkbox(), toggle(), descendants(), FakeBox, FakeButton

### Community 9 - "PROJECT_INDEX.md"
Cohesion: 0.23
Nodes (5): Hướng dẫn khi tiếp tục dự án, Quy trình Swarmote hiện tại, Bản đồ repository, q3 — b1–b3 và nối luồng chung, q4 — Giỏ hàng, Pets, Home and DIY

### Community 10 - "002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ"
Cohesion: 0.07
Nodes (25): 002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ, Kiểm tra bắt buộc, Phạm vi, Rủi ro và bảo trì, Điều kiện dừng, 003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật, Các bước, Kiểm tra bắt buộc (+17 more)

### Community 11 - "Danh mục từng bước đã biết — 13/11/2026"
Cohesion: 0.06
Nodes (32): Chung b10 — Chuyển WhatsApp sang SMS, Chung b11 — Lấy và gõ OTP SMS, Chung b11a — Chạm ô OTP trên màn SMS, Chung b11b — Bấm Create your Amazon account, Chung b4 — Sign In từ menu, Chung b4a — Chạm ô SĐT, Chung b5 — Gõ số điện thoại, Chung b6 — Chọn United States +1 (+24 more)

### Community 12 - "bulk_input.py"
Cohesion: 0.13
Nodes (7): BulkRecord, lines(), parse_column(), parse_records(), _table_cells(), _url_from_cell(), BulkInputTests

### Community 13 - "account_flow.py"
Cohesion: 0.15
Nodes (17): _ActionNotResolved, _bounds(), _keyboard_visible(), _national_phone(), _parse_ui_nodes(), _read_hierarchy(), _read_nodes_once(), _read_visual_nodes() (+9 more)

### Community 14 - "Biên bản kiểm tra thực tế — 2026-11-12"
Cohesion: 0.08
Nodes (24): b6 Country US +1 — 14/11/2026, B6 cuộn quốc gia và chọn lại — 13/11/2026, Biên bản kiểm tra thực tế — 2026-11-12, Cài và đo UiAutomator2 theo phê duyệt mới — 13/11/2026, Cập nhật luồng mẻ trước đó — 2026-11-13, Ghim taskbar — 13/11/2026, Giao diện sáng, dễ đọc — 2026-11-13, Hướng Swarmote theo ảnh người dùng (+16 more)

### Community 16 - "Ảnh hướng dẫn q1/q2 và menu chung lưu cục bộ"
Cohesion: 0.09
Nodes (23): B6 — Hai ảnh đính kèm mới ngày 13/11/2026, Menu chung ảnh 01 — Danh sách chữ, q1 b6 — US +1 hiện nhưng chạm không đóng hộp, 14/11/2026, q1 ảnh 01 — Menu và ba thẻ, q1 ảnh 02 — Sign In cuối menu, q1 ảnh 03 — Nhập số điện thoại, q1 ảnh 04 — Chọn mã quốc gia, q1 ảnh 05 — Continue số điện thoại (+15 more)

### Community 17 - "desktop.py"
Cohesion: 0.19
Nodes (7): save(), default_path(), AppSettings, load_settings(), save_settings(), settings_path(), SettingsTests

### Community 18 - "_read_nodes"
Cohesion: 0.23
Nodes (19): _at_or_after(), sign_in(), _ensure_menu(), _find_scrolling(), home_visible(), _read_nodes(), _tap(), _unique() (+11 more)

### Community 19 - "ToolError"
Cohesion: 0.15
Nodes (8): ToolError, _start_and_confirm(), create_profile(), ProxyConfig, Mục tiêu và bằng chứng, Tự phục hồi lỗi tạm thời trong mẻ nhiều máy — 14/11/2026, CreationWindowVisibilityTests, Tự phục hồi lỗi tạm thời trong mẻ nhiều máy — 14/11/2026

### Community 20 - "run_batch"
Cohesion: 0.26
Nodes (8): emit(), _prepare_phone(), progress(), run_batch(), fill_slots(), refresh_slots(), startup_progress(), visible_lookup()

### Community 21 - "BatchDraft"
Cohesion: 0.15
Nodes (3): BatchDraft, BatchDraftTests, StopResetTests

### Community 23 - "screen"
Cohesion: 0.19
Nodes (22): continue_number(), country(), create_account(), enter_otp(), focus_otp(), focus_phone(), name(), phone_number() (+14 more)

### Community 25 - "Nghiên cứu và tích hợp Swarmote"
Cohesion: 0.40
Nodes (4): Hành vi có bằng chứng, Kiểm thử còn lại, Nghiên cứu và tích hợp Swarmote, Phần đã áp dụng

### Community 26 - "validate_otp_url"
Cohesion: 0.25
Nodes (3): validate_card(), otp_token(), validate_otp_url()

### Community 27 - "001 — Tách dữ liệu từng mẻ và đối chiếu số hàng"
Cohesion: 0.29
Nodes (7): 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Rủi ro và bảo trì, Thiết kế yêu cầu, Điều kiện dừng

### Community 28 - "vision.py"
Cohesion: 0.07
Nodes (17): _bounds(), _canonical_text(), _engine(), _field_contents(), _field_is_blank(), _input_box(), _join_wrapped_categories(), _normalize() (+9 more)

### Community 29 - "ui_backend.py"
Cohesion: 0.09
Nodes (17): swarmote_tunnel_owner(), phone_reader(), PhoneReader, ReaderResponseError, _serve(), _connect(), country_scroll(), _failed() (+9 more)

### Community 30 - "home_menu.py"
Cohesion: 0.10
Nodes (13): open_amazon(), foreground(), _confirm_menu_fallback(), _menu_evidence(), MenuReadUnavailable, _nodes(), budget(), open_home_menu() (+5 more)

### Community 31 - "test_q3_q4_flow.py"
Cohesion: 0.15
Nodes (4): RegistrationState, build_q3_steps(), build_q4_steps(), Q3Q4FlowTests

### Community 32 - "subprocess"
Cohesion: 0.18
Nodes (7): confirm(), download_commandline_tools(), official_commandline_archive(), main(), check_runtime(), main(), verify()

### Community 33 - "RunJob"
Cohesion: 0.20
Nodes (6): _automatic_resume_slots(), AccountData, RunJob, DesktopResumeTests, install(), on_worker()

### Community 34 - "_type_field"
Cohesion: 0.28
Nodes (3): _type_field(), FlowRecoveryTests, form()

### Community 35 - "CloudPhone"
Cohesion: 0.08
Nodes (22): _country_full_row(), resume_common_index(), verify_menu_open(), cloud_adb(), cloud_serials(), CloudPhone, package_path(), probe() (+14 more)

### Community 36 - "RecoverableStepError"
Cohesion: 0.24
Nodes (6): RecoverableStepError, SharedStepRecoveryTests, action(), action(), action(), action()

### Community 37 - "profile_status"
Cohesion: 0.11
Nodes (12): _open_profiles(), _profile_row_status(), profile_status(), ProfileNotFound, _unfiltered_single_page(), visible_profile_names(), Các bước, control() (+4 more)

### Community 38 - "swarmote_desktop.py"
Cohesion: 0.13
Nodes (20): _activate_manager(), _create_profile_form(), _descendants(), inspect(), _invoke(), _main_window(), _one(), _profile_checkbox() (+12 more)

### Community 40 - "setup_windows.py"
Cohesion: 0.27
Nodes (9): _app_installed(), _app_paths(), _check_external_apps(), _install_python_dependencies(), main(), _offer_downloads(), _ready_file_matches(), _runtime_imports_work() (+1 more)

### Community 41 - "route_list_menu"
Cohesion: 0.32
Nodes (5): menu_layout(), route_list_menu(), route(), Quy tắc chạy, Mã hiện có

### Community 42 - "Bàn giao trạng thái dự án — 13/11/2026"
Cohesion: 0.17
Nodes (12): B6 danh sách quốc gia vẫn mở sau khi chọn — 13/11/2026, Bàn giao trạng thái dự án — 13/11/2026, Bản chính boom4may và bản dự phòng — 14/11/2026, Bộ cài offline chia sẻ — 14/11/2026, Cài đặt máy mới, Dự phòng dùng chung khi chạy song song — 14/11/2026, Mục tiêu và quy tắc đã chốt, q3/q4 đã nối b1–b3 và thử đồng thời bốn luồng — 13/11/2026 (+4 more)

### Community 43 - "windows_identity.py"
Cohesion: 0.27
Nodes (6): create_shortcut(), relaunch_command(), runtime(), set_process_identity(), set_window_identity(), WindowsIdentityTests

### Community 44 - "FakeControl"
Cohesion: 0.14
Nodes (4): ParallelInstallTests, PhoneWindow, FakeControl, InstallTests

### Community 45 - "b1–b11 Reliability and Latency Implementation Plan"
Cohesion: 0.18
Nodes (10): b1–b11 Reliability and Latency Implementation Plan, Completion Criteria, File Map, Global Constraints, Review Focus, Task 1: Measure current step latency and classify existing failures, Task 2: Define safe retry, reconcile, pause, and stop behavior, Task 3: Reduce redundant UI reads and unnecessary waits (+2 more)

### Community 46 - "MENU_ROUTING.md"
Cohesion: 0.27
Nodes (6): Bằng chứng và phạm vi, Kiểm chứng, Điều hướng hai dạng menu ba gạch, Luồng q1 từ menu ba gạch tới nhập OTP, Thử trên q1 đã có, Luồng q2 từ menu ba gạch

### Community 47 - "PROJECT_HANDOFF.md"
Cohesion: 0.18
Nodes (10): B4–b11 chạy đồng thời và OCR — 14/11/2026, b6 US +1 còn mở sau bốn cú chạm — 14/11/2026, Bỏ thời hạn tổng sau menu — 14/11/2026, File chính đã sửa, Kết quả và giới hạn, Lỗi chạy song song q3 Terminal trùng / q1 chưa thấy menu — 14/11/2026, Phạm vi q1–q12 sau phản hồi người dùng — 14/11/2026, Sửa lỗi chuẩn bị nhiều máy — 14/11/2026 (+2 more)

### Community 49 - "CountryRecoveryTests"
Cohesion: 0.31
Nodes (4): CountryRecoveryTests, read(), wait(), node()

### Community 50 - "sys"
Cohesion: 0.24
Nodes (4): main(), main(), Đợt tăng tốc và tự phục hồi b4–b11 ngày 13/11/2026, LauncherTests

### Community 51 - "VERIFICATION.md"
Cohesion: 0.20
Nodes (8): Kết luận và tích hợp, Kết quả thực tế, So sánh bộ đọc trên q1 — 13/11/2026, Thành phần thiết bị, File chính đã sửa, Kết quả và giới hạn, Lỗi chạy song song q3 Terminal trùng / q1 chưa thấy menu — 14/11/2026, Sửa lỗi chuẩn bị nhiều máy — 14/11/2026

### Community 52 - "ResumeRegistrationStateTests"
Cohesion: 0.31
Nodes (3): ResumeRegistrationStateTests, factory(), factory()

### Community 53 - "Danh mục ảnh nằm trong dự án"
Cohesion: 0.29
Nodes (7): amazon_android/assets/obsidian_prism.png, assets/ui_history/reset_check.png, assets/ui_history/ui-12.png, assets/ui_history/ui_palette_preview.png, assets/ui_history/ui-preview.png, assets/ui_history/ui-screenshot.png, Danh mục ảnh nằm trong dự án

### Community 54 - "Bàn giao dừng theo yêu cầu người dùng — 13/11/2026"
Cohesion: 0.29
Nodes (6): Bàn giao dừng theo yêu cầu người dùng — 13/11/2026, Bối cảnh đã hoàn tất trước lỗi hiện tại, Cách tiếp tục, Kiểm chứng gần nhất, Lỗi chính chưa xử lý xong, Yêu cầu mới nhất

### Community 55 - "Amazon Android Tool — Giai đoạn A/B"
Cohesion: 0.33
Nodes (6): Amazon Android Tool — Giai đoạn A/B, Cài trên máy Windows mới, Sử dụng, Trạng thái nghiệm thu, Yêu cầu, Điện thoại đám mây Swarmote

### Community 56 - "PreparationThreadsTests"
Cohesion: 0.40
Nodes (4): apartment_type(), PreparationThreadsTests, run(), install()

### Community 58 - "Giao diện vận hành"
Cohesion: 0.40
Nodes (4): Bố cục, Giao diện vận hành, Hướng thị giác, Quy tắc

### Community 59 - "Quy tắc tự động hóa sau menu ba gạch"
Cohesion: 0.40
Nodes (5): Nhận diện giao diện lúc chạy, Nhập liệu và lỗi, Quy tắc tự động hóa sau menu ba gạch, Trạng thái hiện tại của dự án, Từng máy độc lập

### Community 60 - "Amazon trên Swarmote"
Cohesion: 0.40
Nodes (4): Amazon trên Swarmote, Người dùng và công việc, Nền tảng, Điều chưa xác minh

### Community 61 - "File dự án mà Graphify không phân tích trực tiếp"
Cohesion: 0.40
Nodes (5): File dự án mà Graphify không phân tích trực tiếp, .gitignore, Launch Swarmote Tool.pyw, pyproject.toml, Ảnh PNG trong dự án

### Community 62 - "OTP_DESIGN.md"
Cohesion: 0.50
Nodes (3): Nối vào bước tạo tài khoản sau khi xác minh màn hình Amazon, Thiết kế OTP cho từng Profile, Đã chuẩn bị

### Community 63 - "Bộ cài chia sẻ Windows x64"
Cohesion: 0.50
Nodes (3): Bộ cài chia sẻ Windows x64, Dựng lại, Nguồn thành phần

### Community 65 - "Kiểm tra độ phủ Graphify — 13/11/2026"
Cohesion: 0.67
Nodes (3): Cách kiểm tra sau mỗi sửa đổi, Giới hạn đã xác nhận, Kiểm tra độ phủ Graphify — 13/11/2026

## Knowledge Gaps
- **1 isolated node(s):** `amazon-android-tool`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 357 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ToolError` connect `ToolError` to `core.py`, `build_common_steps`, `time`, `Window`, `registration.py`, `open_adb_shell`, `RunnerTests`, `PostMenuSession`, `bulk_input.py`, `account_flow.py`, `desktop.py`, `_read_nodes`, `run_batch`, `BatchDraft`, `screen`, `._apply_bulk_text`, `validate_otp_url`, `vision.py`, `ui_backend.py`, `home_menu.py`, `test_q3_q4_flow.py`, `subprocess`, `RunJob`, `_type_field`, `CloudPhone`, `RecoverableStepError`, `profile_status`, `swarmote_desktop.py`, `runner.py`, `CloudBridgeTests`, `CountryRecoveryTests`?**
  _High betweenness centrality (0.453) - this node is a cross-community bridge._
- **Are the 39 inferred relationships involving `ToolError` (e.g. with `_read_nodes_once()` and `_tap_for_transition()`) actually correct?**
  _`ToolError` has 39 INFERRED edges - model-reasoned connections that need verification._
- **What connects `amazon-android-tool` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `core.py` be split into smaller, more focused modules?**
  _Cohesion score 0.09107737874861163 - nodes in this community are weakly interconnected._
- **Why does `CloudPhone` connect `CloudPhone` to `core.py`, `build_common_steps`, `Window`, `registration.py`, `open_adb_shell`, `PostMenuSession`, `account_flow.py`, `desktop.py`, `_read_nodes`, `ToolError`, `run_batch`, `screen`, `ui_backend.py`, `home_menu.py`, `test_q3_q4_flow.py`, `RunJob`, `_type_field`, `profile_status`, `swarmote_desktop.py`, `runner.py`, `route_list_menu`, `CloudBridgeTests`, `CountryRecoveryTests`, `ResumeRegistrationStateTests`?**
  _High betweenness centrality (0.090) - this node is a cross-community bridge._
- **Are the 61 inferred relationships involving `CloudPhone` (e.g. with `build_common_steps()` and `_country_full_row()`) actually correct?**
  _`CloudPhone` has 61 INFERRED edges - model-reasoned connections that need verification._
- **Should `build_common_steps` be split into smaller, more focused modules?**
  _Cohesion score 0.07402597402597402 - nodes in this community are weakly interconnected._