# Graph Report - boom4may  (2026-11-14)

## Corpus Check
- 108 files · ~82,961 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 1, .bat 1, .pyw 1)

## Summary
- 1323 nodes · 4286 edges · 61 communities (51 shown, 10 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 587 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ff78535b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- core.py
- Q1FlowTests
- time
- Window
- isolated_reader.py
- open_adb_shell
- RunnerTests
- PostMenuSession
- .test_only_confirmed_target_names_are_selected_for_one_start_command
- PROJECT_INDEX.md
- 002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ
- Danh mục từng bước đã biết — 13/11/2026
- bulk_input.py
- profile_status
- Biên bản kiểm tra thực tế — 2026-11-12
- amazon-android-tool
- Ảnh hướng dẫn q1/q2 và menu chung lưu cục bộ
- desktop.py
- _read_nodes
- runner.py
- run_batch
- BatchDraft
- ._label
- screen
- ._apply_bulk_text
- Nghiên cứu và tích hợp Swarmote
- build_common_steps
- 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng
- vision.py
- ui_backend.py
- ToolError
- CloudPhone
- build_q1_steps
- RunJob
- _type_field
- AttemptDeadline
- ExtendedRecoveryTests
- profile_status
- swarmote_desktop.py
- runner.py
- StopResetTests
- route_list_menu
- Bàn giao trạng thái dự án — 13/11/2026
- ensure_manager_ready
- FakeControl
- b1–b11 Reliability and Latency Implementation Plan
- MENU_ROUTING.md
- PROJECT_HANDOFF.md
- CloudBridgeTests
- CountryRecoveryTests
- So sánh bộ đọc trên q1 — 13/11/2026
- ResumeRegistrationStateTests
- Danh mục ảnh nằm trong dự án
- Amazon Android Tool — Giai đoạn A/B
- PreparationThreadsTests
- Giao diện vận hành
- Quy tắc tự động hóa sau menu ba gạch
- Amazon trên Swarmote
- OTP_DESIGN.md
- Bộ cài chia sẻ Windows x64
- Kiểm tra độ phủ Graphify — 13/11/2026

## God Nodes (most connected - your core abstractions)
1. `ToolError` - 240 edges
2. `CloudPhone` - 146 edges
3. `RunJob` - 83 edges
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
- `Phần dùng chung đã được hướng dẫn` --references--> `build_common_steps()`  [INFERRED]
  FLOW_PROGRESS.md → amazon_android/account_flow.py
- `Trạng thái hiện tại của dự án` --references--> `build_common_steps()`  [INFERRED]
  POST_MENU_REQUIREMENTS.md → amazon_android/account_flow.py
- `Phạm vi q1–q12 sau phản hồi người dùng — 14/11/2026` --references--> `build_common_steps()`  [INFERRED]
  PROJECT_HANDOFF.md → amazon_android/account_flow.py

## Import Cycles
- None detected.

## Communities (61 total, 10 thin omitted)

### Community 0 - "core.py"
Cohesion: 0.08
Nodes (42): BatchItem, parse_proxy_line(), prepare_five(), main(), parser(), report(), adb(), app_data_dir() (+34 more)

### Community 2 - "time"
Cohesion: 0.10
Nodes (8): browser_launch_options(), extract_otp(), _NoRedirect, read_otp(), _read_otp_in_browser(), wait_for_new_otp(), OtpTests, PackagedBrowserTests

### Community 4 - "isolated_reader.py"
Cohesion: 0.20
Nodes (7): phone_reader(), PhoneReader, ReaderResponseError, fake_worker(), IsolationTests, duplicate(), production_worker_with_fake_android()

### Community 5 - "open_adb_shell"
Cohesion: 0.13
Nodes (19): _check_stop(), collapse_apps_panel(), open_adb_shell(), _pause(), _phone_window(), _progress_reporter(), report(), show_apps() (+11 more)

### Community 6 - "RunnerTests"
Cohesion: 0.07
Nodes (14): ProfileRegistry, absent(), ProfileRegistryTests, lookup(), broken(), RunnerTests, create(), resume() (+6 more)

### Community 7 - "PostMenuSession"
Cohesion: 0.15
Nodes (12): reconcile(), PostMenuSession, PostMenuStep, RunJob, Bỏ thời hạn tổng sau menu — 14/11/2026, PostMenuTests, first_step(), SharedStepRecoveryTests (+4 more)

### Community 8 - ".test_only_confirmed_target_names_are_selected_for_one_start_command"
Cohesion: 0.11
Nodes (6): BatchStartTests, checkbox(), toggle(), descendants(), FakeBox, FakeButton

### Community 9 - "PROJECT_INDEX.md"
Cohesion: 0.23
Nodes (5): Hướng dẫn khi tiếp tục dự án, Quy trình Swarmote hiện tại, Bản đồ repository, q3 — b1–b3 và nối luồng chung, q4 — Giỏ hàng, Pets, Home and DIY

### Community 10 - "002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ"
Cohesion: 0.08
Nodes (20): 003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật, Các bước, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Quy trình đích, Rủi ro và bảo trì, Điều kiện dừng (+12 more)

### Community 11 - "Danh mục từng bước đã biết — 13/11/2026"
Cohesion: 0.06
Nodes (32): Chung b10 — Chuyển WhatsApp sang SMS, Chung b11 — Lấy và gõ OTP SMS, Chung b11a — Chạm ô OTP trên màn SMS, Chung b11b — Bấm Create your Amazon account, Chung b4 — Sign In từ menu, Chung b4a — Chạm ô SĐT, Chung b5 — Gõ số điện thoại, Chung b6 — Chọn United States +1 (+24 more)

### Community 12 - "bulk_input.py"
Cohesion: 0.10
Nodes (10): BulkRecord, lines(), parse_column(), parse_records(), _table_cells(), _url_from_cell(), validate_card(), otp_token() (+2 more)

### Community 13 - "profile_status"
Cohesion: 0.14
Nodes (14): visible_lookup(), _profile_row_status(), profile_status(), ProfileLookupError, ProfileNotFound, 002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ, Các bước, Kiểm tra bắt buộc (+6 more)

### Community 14 - "Biên bản kiểm tra thực tế — 2026-11-12"
Cohesion: 0.05
Nodes (34): _confirm_menu_fallback(), _menu_evidence(), MenuReadUnavailable, _nodes(), budget(), open_home_menu(), HomeMenuTests, ParallelNavigationRegressionTests (+26 more)

### Community 16 - "Ảnh hướng dẫn q1/q2 và menu chung lưu cục bộ"
Cohesion: 0.08
Nodes (24): B6 — Hai ảnh đính kèm mới ngày 13/11/2026, Menu chung ảnh 01 — Danh sách chữ, Menu chung ảnh 02 — App Store bên phải sau khi Amazon mở, q1 b6 — US +1 hiện nhưng chạm không đóng hộp, 14/11/2026, q1 ảnh 01 — Menu và ba thẻ, q1 ảnh 02 — Sign In cuối menu, q1 ảnh 03 — Nhập số điện thoại, q1 ảnh 04 — Chọn mã quốc gia (+16 more)

### Community 17 - "desktop.py"
Cohesion: 0.05
Nodes (35): _crystal_art(), main(), save(), main(), default_path(), AppSettings, load_settings(), save_settings() (+27 more)

### Community 18 - "_read_nodes"
Cohesion: 0.25
Nodes (19): _at_or_after(), sign_in(), _ensure_menu(), _find_scrolling(), home_visible(), _read_nodes(), _tap(), _unique() (+11 more)

### Community 19 - "runner.py"
Cohesion: 0.13
Nodes (7): create_profile(), ProfileCreateNotSubmitted, ProfileManagerWindowError, ProxyConfig, ProxyTestFailed, unavailable(), CreationWindowVisibilityTests

### Community 20 - "run_batch"
Cohesion: 0.29
Nodes (7): emit(), _prepare_phone(), progress(), run_batch(), fill_slots(), refresh_slots(), startup_progress()

### Community 23 - "screen"
Cohesion: 0.12
Nodes (31): _ActionNotResolved, _bounds(), continue_number(), country(), create_account(), focus_otp(), focus_phone(), name() (+23 more)

### Community 25 - "Nghiên cứu và tích hợp Swarmote"
Cohesion: 0.40
Nodes (4): Hành vi có bằng chứng, Kiểm thử còn lại, Nghiên cứu và tích hợp Swarmote, Phần đã áp dụng

### Community 27 - "001 — Tách dữ liệu từng mẻ và đối chiếu số hàng"
Cohesion: 0.29
Nodes (7): 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Rủi ro và bảo trì, Thiết kế yêu cầu, Điều kiện dừng

### Community 28 - "vision.py"
Cohesion: 0.07
Nodes (17): _bounds(), _canonical_text(), _engine(), _field_contents(), _field_is_blank(), _input_box(), _join_wrapped_categories(), _normalize() (+9 more)

### Community 29 - "ui_backend.py"
Cohesion: 0.09
Nodes (20): swarmote_tunnel_owner(), _field_for_label(), fill_identifier(), fill_signup_form(), _nodes(), open_entry(), status(), _tap() (+12 more)

### Community 30 - "ToolError"
Cohesion: 0.19
Nodes (9): open_amazon(), ToolError, ready_for_home_menu(), _tap(), _start_and_confirm(), install_amazon(), check_stop(), ready_for_registration() (+1 more)

### Community 31 - "CloudPhone"
Cohesion: 0.11
Nodes (16): cloud_adb(), cloud_screenshot(), cloud_serials(), CloudPhone, foreground(), package_path(), probe(), prop() (+8 more)

### Community 32 - "build_q1_steps"
Cohesion: 0.14
Nodes (6): build_q1_steps(), category(), Cách xử lý ảnh tiếp theo, Phần dùng chung đã được hướng dẫn, Phần riêng từng máy, Tiến độ hướng dẫn bằng ảnh — cập nhật 13/11/2026

### Community 33 - "RunJob"
Cohesion: 0.13
Nodes (5): _automatic_resume_slots(), AccountData, DesktopResumeTests, Q2FlowTests, on_worker()

### Community 34 - "_type_field"
Cohesion: 0.21
Nodes (4): enter_otp(), _type_field(), FlowRecoveryTests, form()

### Community 35 - "AttemptDeadline"
Cohesion: 0.14
Nodes (14): _country_full_row(), _keyboard_visible(), _read_hierarchy(), _read_nodes_once(), _read_visual_nodes(), resume_common_index(), _scroll_up(), _tap_input() (+6 more)

### Community 36 - "ExtendedRecoveryTests"
Cohesion: 0.19
Nodes (5): ExtendedRecoveryTests, fail(), read(), read(), menu()

### Community 37 - "profile_status"
Cohesion: 0.18
Nodes (6): _open_profiles(), visible_profile_names(), control(), ProfilesNavigationTests, descendants(), descendants()

### Community 38 - "swarmote_desktop.py"
Cohesion: 0.10
Nodes (24): _activate_manager(), _create_profile_form(), _descendants(), inspect(), _invoke(), _one(), _profile_checkbox(), _profile_form_open() (+16 more)

### Community 41 - "route_list_menu"
Cohesion: 0.28
Nodes (5): menu_layout(), _parse_ui_nodes(), route_list_menu(), route(), Quy tắc chạy

### Community 42 - "Bàn giao trạng thái dự án — 13/11/2026"
Cohesion: 0.14
Nodes (14): B6 danh sách quốc gia vẫn mở sau khi chọn — 13/11/2026, Bàn giao trạng thái dự án — 13/11/2026, Bản chính boom4may và bản dự phòng — 14/11/2026, Bộ cài offline chia sẻ — 14/11/2026, Cài đặt máy mới, Dự phòng dùng chung khi chạy song song — 14/11/2026, Mã hiện có, Mục tiêu và quy tắc đã chốt (+6 more)

### Community 43 - "ensure_manager_ready"
Cohesion: 0.27
Nodes (5): ensure_manager_ready(), _main_window(), collect(), _swarmote_exe(), ManagerStartupTests

### Community 44 - "FakeControl"
Cohesion: 0.13
Nodes (5): ParallelInstallTests, PhoneWindow, FakeControl, InstallTests, descendants()

### Community 45 - "b1–b11 Reliability and Latency Implementation Plan"
Cohesion: 0.18
Nodes (10): b1–b11 Reliability and Latency Implementation Plan, Completion Criteria, File Map, Global Constraints, Review Focus, Task 1: Measure current step latency and classify existing failures, Task 2: Define safe retry, reconcile, pause, and stop behavior, Task 3: Reduce redundant UI reads and unnecessary waits (+2 more)

### Community 46 - "MENU_ROUTING.md"
Cohesion: 0.27
Nodes (6): Bằng chứng và phạm vi, Kiểm chứng, Điều hướng hai dạng menu ba gạch, Luồng q1 từ menu ba gạch tới nhập OTP, Thử trên q1 đã có, Luồng q2 từ menu ba gạch

### Community 47 - "PROJECT_HANDOFF.md"
Cohesion: 0.20
Nodes (7): B4–b11 chạy đồng thời và OCR — 14/11/2026, b6 US +1 còn mở sau bốn cú chạm — 14/11/2026, Lỗi chạy song song q3 Terminal trùng / q1 chưa thấy menu — 14/11/2026, Phạm vi q1–q12 sau phản hồi người dùng — 14/11/2026, Tách bộ đọc thành tiến trình riêng từng máy — 14/11/2026, Tự tìm và mở Swarmote khi chạy mẻ — 14/11/2026, Lỗi chạy song song q3 Terminal trùng / q1 chưa thấy menu — 14/11/2026

### Community 49 - "CountryRecoveryTests"
Cohesion: 0.31
Nodes (4): CountryRecoveryTests, read(), wait(), node()

### Community 51 - "So sánh bộ đọc trên q1 — 13/11/2026"
Cohesion: 0.50
Nodes (4): Kết luận và tích hợp, Kết quả thực tế, So sánh bộ đọc trên q1 — 13/11/2026, Thành phần thiết bị

### Community 52 - "ResumeRegistrationStateTests"
Cohesion: 0.25
Nodes (3): ResumeRegistrationStateTests, factory(), factory()

### Community 53 - "Danh mục ảnh nằm trong dự án"
Cohesion: 0.29
Nodes (7): amazon_android/assets/obsidian_prism.png, assets/ui_history/reset_check.png, assets/ui_history/ui-12.png, assets/ui_history/ui_palette_preview.png, assets/ui_history/ui-preview.png, assets/ui_history/ui-screenshot.png, Danh mục ảnh nằm trong dự án

### Community 55 - "Amazon Android Tool — Giai đoạn A/B"
Cohesion: 0.33
Nodes (6): Amazon Android Tool — Giai đoạn A/B, Cài trên máy Windows mới, Sử dụng, Trạng thái nghiệm thu, Yêu cầu, Điện thoại đám mây Swarmote

### Community 56 - "PreparationThreadsTests"
Cohesion: 0.29
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
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 359 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **10 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ToolError` connect `ToolError` to `core.py`, `Q1FlowTests`, `time`, `Window`, `isolated_reader.py`, `open_adb_shell`, `RunnerTests`, `PostMenuSession`, `bulk_input.py`, `profile_status`, `Biên bản kiểm tra thực tế — 2026-11-12`, `desktop.py`, `_read_nodes`, `runner.py`, `run_batch`, `BatchDraft`, `screen`, `._apply_bulk_text`, `build_common_steps`, `vision.py`, `ui_backend.py`, `CloudPhone`, `build_q1_steps`, `RunJob`, `_type_field`, `AttemptDeadline`, `ExtendedRecoveryTests`, `profile_status`, `swarmote_desktop.py`, `runner.py`, `StopResetTests`, `route_list_menu`, `ensure_manager_ready`, `CloudBridgeTests`, `CountryRecoveryTests`?**
  _High betweenness centrality (0.444) - this node is a cross-community bridge._
- **Are the 39 inferred relationships involving `ToolError` (e.g. with `_read_nodes_once()` and `_tap_for_transition()`) actually correct?**
  _`ToolError` has 39 INFERRED edges - model-reasoned connections that need verification._
- **What connects `amazon-android-tool` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `core.py` be split into smaller, more focused modules?**
  _Cohesion score 0.07860011474469306 - nodes in this community are weakly interconnected._
- **Why does `CloudPhone` connect `CloudPhone` to `core.py`, `Q1FlowTests`, `Window`, `isolated_reader.py`, `PostMenuSession`, `profile_status`, `Biên bản kiểm tra thực tế — 2026-11-12`, `desktop.py`, `_read_nodes`, `runner.py`, `run_batch`, `screen`, `build_common_steps`, `ui_backend.py`, `ToolError`, `build_q1_steps`, `RunJob`, `_type_field`, `AttemptDeadline`, `ExtendedRecoveryTests`, `swarmote_desktop.py`, `runner.py`, `route_list_menu`, `CloudBridgeTests`, `CountryRecoveryTests`, `ResumeRegistrationStateTests`?**
  _High betweenness centrality (0.100) - this node is a cross-community bridge._
- **Are the 61 inferred relationships involving `CloudPhone` (e.g. with `build_common_steps()` and `_country_full_row()`) actually correct?**
  _`CloudPhone` has 61 INFERRED edges - model-reasoned connections that need verification._
- **Should `Q1FlowTests` be split into smaller, more focused modules?**
  _Cohesion score 0.14333333333333334 - nodes in this community are weakly interconnected._