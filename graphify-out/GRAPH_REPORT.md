# Graph Report - boom4may  (2026-11-14)

## Corpus Check
- 111 files · ~83,540 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 1, .bat 1, .pyw 1)

## Summary
- 1334 nodes · 4339 edges · 64 communities (54 shown, 10 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 598 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `073efd3c`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- core.py
- Q1FlowTests
- time
- ._refresh_devices
- subprocess
- open_adb_shell
- RunnerTests
- PostMenuSession
- .test_only_confirmed_target_names_are_selected_for_one_start_command
- PROJECT_INDEX.md
- 002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ
- Danh mục từng bước đã biết — 13/11/2026
- bulk_input.py
- 002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ
- Biên bản kiểm tra thực tế — 2026-11-12
- amazon-android-tool
- Ảnh hướng dẫn q1/q2 và menu chung lưu cục bộ
- setup_windows.py
- desktop.py
- ProxyConfig
- run_batch
- BatchDraft
- Window
- CloudPhone
- ._apply_bulk_text
- Nghiên cứu và tích hợp Swarmote
- cli.py
- 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng
- vision.py
- ui_backend.py
- ToolError
- Q3Q4FlowTests
- build_q1_steps
- RunJob
- main
- post_menu.py
- windows_identity.py
- profile_status
- swarmote_desktop.py
- SafetyTests
- Bàn giao dừng theo yêu cầu người dùng — 13/11/2026
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
- _crystal_art
- Amazon Android Tool — Giai đoạn A/B
- StopResetTests
- validate_otp_url
- Giao diện vận hành
- Quy tắc tự động hóa sau menu ba gạch
- Amazon trên Swarmote
- OTP_DESIGN.md
- Bộ cài chia sẻ Windows x64
- Kiểm tra độ phủ Graphify — 13/11/2026

## God Nodes (most connected - your core abstractions)
1. `ToolError` - 240 edges
2. `CloudPhone` - 151 edges
3. `RunJob` - 86 edges
4. `Window` - 77 edges
5. `AttemptDeadline` - 77 edges
6. `build_common_steps()` - 74 edges
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

## Communities (64 total, 10 thin omitted)

### Community 0 - "core.py"
Cohesion: 0.28
Nodes (18): adb(), available_memory_mb(), check_play(), connected_devices(), Device, device_avd_name(), device_resources(), emergency_stop() (+10 more)

### Community 1 - "Q1FlowTests"
Cohesion: 0.11
Nodes (3): build_common_steps(), node(), Q1FlowTests

### Community 2 - "time"
Cohesion: 0.10
Nodes (8): browser_launch_options(), extract_otp(), _NoRedirect, read_otp(), _read_otp_in_browser(), wait_for_new_otp(), OtpTests, PackagedBrowserTests

### Community 4 - "subprocess"
Cohesion: 0.17
Nodes (16): app_data_dir(), avd_names(), create_avd(), doctor(), executable(), installed_image(), run(), sdk_root() (+8 more)

### Community 5 - "open_adb_shell"
Cohesion: 0.11
Nodes (22): ready_for_home_menu(), _check_stop(), collapse_apps_panel(), install_amazon(), collect(), open_adb_shell(), _pause(), _phone_window() (+14 more)

### Community 6 - "RunnerTests"
Cohesion: 0.07
Nodes (17): ProfileRegistry, ProfileLookupError, ProfileNotFound, Thiết kế yêu cầu, absent(), ProfileRegistryTests, lookup(), broken() (+9 more)

### Community 7 - "PostMenuSession"
Cohesion: 0.14
Nodes (10): PostMenuSession, PostMenuStep, RecoverableStepError, PostMenuTests, first_step(), SharedStepRecoveryTests, action(), action() (+2 more)

### Community 8 - ".test_only_confirmed_target_names_are_selected_for_one_start_command"
Cohesion: 0.09
Nodes (11): _select_profile_rows(), _selected_profile_names(), start_profile(), start_profiles_together(), _wait_for_selected(), BatchStartTests, checkbox(), toggle() (+3 more)

### Community 9 - "PROJECT_INDEX.md"
Cohesion: 0.21
Nodes (6): Hướng dẫn khi tiếp tục dự án, Quy trình Swarmote hiện tại, Bản đồ repository, q3 — b1–b3 và nối luồng chung, q4 — Giỏ hàng, Pets, Home and DIY, q5 — ba thẻ riêng và b4–b11 chung

### Community 10 - "002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ"
Cohesion: 0.08
Nodes (20): 003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật, Các bước, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Quy trình đích, Rủi ro và bảo trì, Điều kiện dừng (+12 more)

### Community 11 - "Danh mục từng bước đã biết — 13/11/2026"
Cohesion: 0.06
Nodes (33): Chung b10 — Chuyển WhatsApp sang SMS, Chung b11 — Lấy và gõ OTP SMS, Chung b11a — Chạm ô OTP trên màn SMS, Chung b11b — Bấm Create your Amazon account, Chung b4 — Sign In từ menu, Chung b4a — Chạm ô SĐT, Chung b5 — Gõ số điện thoại, Chung b6 — Chọn United States +1 (+25 more)

### Community 12 - "bulk_input.py"
Cohesion: 0.15
Nodes (6): BulkRecord, lines(), parse_column(), parse_records(), _url_from_cell(), BulkInputTests

### Community 13 - "002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ"
Cohesion: 0.33
Nodes (6): 002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Rủi ro và bảo trì, Điều kiện dừng

### Community 14 - "Biên bản kiểm tra thực tế — 2026-11-12"
Cohesion: 0.05
Nodes (35): _confirm_menu_fallback(), _menu_evidence(), MenuReadUnavailable, _nodes(), budget(), open_home_menu(), _tap(), HomeMenuTests (+27 more)

### Community 16 - "Ảnh hướng dẫn q1/q2 và menu chung lưu cục bộ"
Cohesion: 0.08
Nodes (24): B6 — Hai ảnh đính kèm mới ngày 13/11/2026, Menu chung ảnh 01 — Danh sách chữ, Menu chung ảnh 02 — App Store bên phải sau khi Amazon mở, q1 b6 — US +1 hiện nhưng chạm không đóng hộp, 14/11/2026, q1 ảnh 01 — Menu và ba thẻ, q1 ảnh 02 — Sign In cuối menu, q1 ảnh 03 — Nhập số điện thoại, q1 ảnh 04 — Chọn mã quốc gia (+16 more)

### Community 17 - "setup_windows.py"
Cohesion: 0.14
Nodes (15): save(), default_path(), AppSettings, load_settings(), save_settings(), settings_path(), _app_installed(), _app_paths() (+7 more)

### Community 19 - "ProxyConfig"
Cohesion: 0.19
Nodes (6): BatchItem, parse_proxy_line(), prepare_five(), ProxyConfig, BatchSafetyTests, CreationWindowVisibilityTests

### Community 20 - "run_batch"
Cohesion: 0.14
Nodes (12): emit(), _prepare_phone(), progress(), run_batch(), fill_slots(), refresh_slots(), startup_progress(), visible_lookup() (+4 more)

### Community 22 - "Window"
Cohesion: 0.17
Nodes (3): _edge_light(), Window, PreparationProgressTests

### Community 23 - "CloudPhone"
Cohesion: 0.05
Nodes (84): _ActionNotResolved, _at_or_after(), _bounds(), continue_number(), country(), create_account(), enter_otp(), focus_otp() (+76 more)

### Community 25 - "Nghiên cứu và tích hợp Swarmote"
Cohesion: 0.40
Nodes (4): Hành vi có bằng chứng, Kiểm thử còn lại, Nghiên cứu và tích hợp Swarmote, Phần đã áp dụng

### Community 26 - "cli.py"
Cohesion: 0.19
Nodes (10): _table_cells(), main(), parser(), report(), get_device(), print_json(), Store, open_entry() (+2 more)

### Community 27 - "001 — Tách dữ liệu từng mẻ và đối chiếu số hàng"
Cohesion: 0.29
Nodes (7): 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Rủi ro và bảo trì, Thiết kế yêu cầu, Điều kiện dừng

### Community 28 - "vision.py"
Cohesion: 0.07
Nodes (17): _bounds(), _canonical_text(), _engine(), _field_contents(), _field_is_blank(), _input_box(), _join_wrapped_categories(), _normalize() (+9 more)

### Community 29 - "ui_backend.py"
Cohesion: 0.08
Nodes (18): swarmote_adb_path(), swarmote_tunnel_owner(), phone_reader(), PhoneReader, ReaderResponseError, _serve(), _connect(), country_scroll() (+10 more)

### Community 30 - "ToolError"
Cohesion: 0.16
Nodes (14): configure_avd(), ToolError, _field_for_label(), fill_identifier(), fill_signup_form(), _nodes(), _tap(), _type_into() (+6 more)

### Community 31 - "Q3Q4FlowTests"
Cohesion: 0.19
Nodes (3): build_q3_steps(), build_q4_steps(), Q3Q4FlowTests

### Community 32 - "build_q1_steps"
Cohesion: 0.14
Nodes (6): build_q1_steps(), category(), Cách xử lý ảnh tiếp theo, Phần dùng chung đã được hướng dẫn, Phần riêng từng máy, Tiến độ hướng dẫn bằng ảnh — cập nhật 13/11/2026

### Community 33 - "RunJob"
Cohesion: 0.15
Nodes (7): AccountData, RunJob, DesktopResumeTests, apartment_type(), PreparationThreadsTests, run(), install()

### Community 34 - "main"
Cohesion: 0.16
Nodes (9): main(), main(), Đợt tăng tốc và tự phục hồi b4–b11 ngày 13/11/2026, File dự án mà Graphify không phân tích trực tiếp, .gitignore, Launch Swarmote Tool.pyw, pyproject.toml, Ảnh PNG trong dự án (+1 more)

### Community 35 - "post_menu.py"
Cohesion: 0.33
Nodes (3): RegistrationState, build_q5_steps(), Q5FlowTests

### Community 36 - "windows_identity.py"
Cohesion: 0.27
Nodes (5): create_shortcut(), relaunch_command(), runtime(), set_window_identity(), WindowsIdentityTests

### Community 37 - "profile_status"
Cohesion: 0.21
Nodes (4): control(), ProfilesNavigationTests, descendants(), descendants()

### Community 38 - "swarmote_desktop.py"
Cohesion: 0.12
Nodes (19): _activate_manager(), create_profile(), _create_profile_form(), _descendants(), inspect(), _invoke(), _main_window(), _one() (+11 more)

### Community 41 - "Bàn giao dừng theo yêu cầu người dùng — 13/11/2026"
Cohesion: 0.25
Nodes (8): Bàn giao dừng theo yêu cầu người dùng — 13/11/2026, Bằng chứng trực tiếp đã có, Bối cảnh đã hoàn tất trước lỗi hiện tại, Cách tiếp tục, Kiểm chứng gần nhất, Lỗi chính chưa xử lý xong, Yêu cầu mới nhất, Đường mã cần xem tiếp

### Community 42 - "Bàn giao trạng thái dự án — 13/11/2026"
Cohesion: 0.14
Nodes (14): B6 danh sách quốc gia vẫn mở sau khi chọn — 13/11/2026, Bàn giao trạng thái dự án — 13/11/2026, Bản chính boom4may và bản dự phòng — 14/11/2026, Bộ cài offline chia sẻ — 14/11/2026, Cài đặt máy mới, Dự phòng dùng chung khi chạy song song — 14/11/2026, Mục tiêu và quy tắc đã chốt, q3/q4 đã nối b1–b3 và thử đồng thời bốn luồng — 13/11/2026 (+6 more)

### Community 43 - "ensure_manager_ready"
Cohesion: 0.28
Nodes (4): ensure_manager_ready(), ProfileManagerWindowError, ManagerStartupTests, unavailable()

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
Cohesion: 0.18
Nodes (8): B4–b11 chạy đồng thời và OCR — 14/11/2026, b6 US +1 còn mở sau bốn cú chạm — 14/11/2026, Bỏ thời hạn tổng sau menu — 14/11/2026, Lỗi chạy song song q3 Terminal trùng / q1 chưa thấy menu — 14/11/2026, Phạm vi q1–q12 sau phản hồi người dùng — 14/11/2026, Tách bộ đọc thành tiến trình riêng từng máy — 14/11/2026, Tự tìm và mở Swarmote khi chạy mẻ — 14/11/2026, Lỗi chạy song song q3 Terminal trùng / q1 chưa thấy menu — 14/11/2026

### Community 48 - "CloudBridgeTests"
Cohesion: 0.18
Nodes (10): cloud_serials(), open_amazon(), foreground(), package_path(), probe(), require_online(), scan(), CloudBridgeTests (+2 more)

### Community 49 - "CountryRecoveryTests"
Cohesion: 0.31
Nodes (4): CountryRecoveryTests, read(), wait(), node()

### Community 51 - "So sánh bộ đọc trên q1 — 13/11/2026"
Cohesion: 0.50
Nodes (4): Kết luận và tích hợp, Kết quả thực tế, So sánh bộ đọc trên q1 — 13/11/2026, Thành phần thiết bị

### Community 52 - "ResumeRegistrationStateTests"
Cohesion: 0.29
Nodes (3): ResumeRegistrationStateTests, factory(), factory()

### Community 53 - "Danh mục ảnh nằm trong dự án"
Cohesion: 0.29
Nodes (7): amazon_android/assets/obsidian_prism.png, assets/ui_history/reset_check.png, assets/ui_history/ui-12.png, assets/ui_history/ui_palette_preview.png, assets/ui_history/ui-preview.png, assets/ui_history/ui-screenshot.png, Danh mục ảnh nằm trong dự án

### Community 55 - "Amazon Android Tool — Giai đoạn A/B"
Cohesion: 0.33
Nodes (6): Amazon Android Tool — Giai đoạn A/B, Cài trên máy Windows mới, Sử dụng, Trạng thái nghiệm thu, Yêu cầu, Điện thoại đám mây Swarmote

### Community 57 - "validate_otp_url"
Cohesion: 0.25
Nodes (3): validate_card(), otp_token(), validate_otp_url()

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
Cohesion: 0.50
Nodes (3): Cách kiểm tra sau mỗi sửa đổi, Giới hạn đã xác nhận, Kiểm tra độ phủ Graphify — 13/11/2026

## Knowledge Gaps
- **1 isolated node(s):** `amazon-android-tool`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 362 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **10 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ToolError` connect `ToolError` to `core.py`, `Q1FlowTests`, `time`, `._refresh_devices`, `subprocess`, `open_adb_shell`, `RunnerTests`, `PostMenuSession`, `.test_only_confirmed_target_names_are_selected_for_one_start_command`, `bulk_input.py`, `002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ`, `Biên bản kiểm tra thực tế — 2026-11-12`, `setup_windows.py`, `desktop.py`, `ProxyConfig`, `run_batch`, `BatchDraft`, `Window`, `CloudPhone`, `._apply_bulk_text`, `cli.py`, `vision.py`, `ui_backend.py`, `build_q1_steps`, `RunJob`, `post_menu.py`, `profile_status`, `swarmote_desktop.py`, `runner.py`, `ensure_manager_ready`, `CloudBridgeTests`, `CountryRecoveryTests`, `StopResetTests`, `validate_otp_url`?**
  _High betweenness centrality (0.456) - this node is a cross-community bridge._
- **Are the 39 inferred relationships involving `ToolError` (e.g. with `_read_nodes_once()` and `_tap_for_transition()`) actually correct?**
  _`ToolError` has 39 INFERRED edges - model-reasoned connections that need verification._
- **What connects `amazon-android-tool` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Q1FlowTests` be split into smaller, more focused modules?**
  _Cohesion score 0.10897435897435898 - nodes in this community are weakly interconnected._
- **Why does `CloudPhone` connect `CloudPhone` to `Q1FlowTests`, `._refresh_devices`, `open_adb_shell`, `PostMenuSession`, `Biên bản kiểm tra thực tế — 2026-11-12`, `desktop.py`, `run_batch`, `Window`, `cli.py`, `ui_backend.py`, `ToolError`, `Q3Q4FlowTests`, `build_q1_steps`, `RunJob`, `post_menu.py`, `swarmote_desktop.py`, `runner.py`, `CloudBridgeTests`, `CountryRecoveryTests`, `ResumeRegistrationStateTests`?**
  _High betweenness centrality (0.095) - this node is a cross-community bridge._
- **Are the 63 inferred relationships involving `CloudPhone` (e.g. with `build_common_steps()` and `_country_full_row()`) actually correct?**
  _`CloudPhone` has 63 INFERRED edges - model-reasoned connections that need verification._
- **Should `time` be split into smaller, more focused modules?**
  _Cohesion score 0.10114942528735632 - nodes in this community are weakly interconnected._