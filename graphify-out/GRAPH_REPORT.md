# Graph Report - boom4may  (2026-11-14)

## Corpus Check
- 117 files · ~90,152 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 1, .bat 1, .pyw 1)

## Summary
- 1430 nodes · 4703 edges · 59 communities (49 shown, 10 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 657 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `89626eb5`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- core.py
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
- ._label
- _read_nodes
- CloudPhone
- amazon-android-tool
- Ảnh hướng dẫn q1/q2 và menu chung lưu cục bộ
- Biên bản kiểm tra thực tế — 2026-11-12
- runner.py
- windows_identity.py
- _type_field
- ._apply_bulk_text
- Bàn giao dừng theo yêu cầu người dùng — 13/11/2026
- AttemptDeadline
- StopResetTests
- Nghiên cứu và tích hợp Swarmote
- Q3Q4FlowTests
- 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng
- vision.py
- ProxyConfig
- RecoverableStepError
- PLAN.md
- _ensure_menu
- desktop.py
- Luồng q1 từ menu ba gạch tới nhập OTP
- Q5_FLOW.md
- profile_status
- swarmote_desktop.py
- Điều hướng hai dạng menu ba gạch
- time
- Bàn giao trạng thái dự án — 13/11/2026
- FakeControl
- ResumeRegistrationStateTests
- PROJECT_HANDOFF.md
- BatchDraft
- CountryRecoveryTests
- Window
- b1–b11 Reliability and Latency Implementation Plan
- Danh mục ảnh nằm trong dự án
- Amazon Android Tool — Giai đoạn A/B
- run_batch
- Giao diện vận hành
- Quy tắc tự động hóa sau menu ba gạch
- Amazon trên Swarmote
- Bộ cài chia sẻ Windows x64
- Kiểm tra độ phủ Graphify — 13/11/2026
- PreparationThreadsTests
- VERIFICATION.md

## God Nodes (most connected - your core abstractions)
1. `ToolError` - 255 edges
2. `CloudPhone` - 166 edges
3. `RunJob` - 100 edges
4. `AttemptDeadline` - 92 edges
5. `Window` - 82 edges
6. `build_common_steps()` - 79 edges
7. `_read_nodes()` - 57 edges
8. `Q1FlowTests` - 51 edges
9. `PostMenuSession` - 48 edges
10. `PostMenuStep` - 45 edges

## Surprising Connections (you probably didn't know these)
- `Cách xử lý ảnh tiếp theo` --references--> `screen()`  [INFERRED]
  FLOW_PROGRESS.md → amazon_android/account_flow.py
- `b6 US +1 còn mở sau bốn cú chạm — 14/11/2026` --references--> `_wait_screen()`  [INFERRED]
  PROJECT_HANDOFF.md → amazon_android/account_flow.py
- `Quy tắc chạy` --references--> `_ensure_menu()`  [INFERRED]
  MENU_ROUTING.md → amazon_android/account_flow.py
- `q6 b1–b3a riêng, b4–b11 chung — 14/11/2026` --references--> `_ensure_menu()`  [INFERRED]
  PROJECT_HANDOFF.md → amazon_android/account_flow.py
- `Điều tra q1/q2 mượt, q3+ lỗi thất thường khi chạy song song — 14/11/2026` --references--> `_ensure_menu()`  [INFERRED]
  PROJECT_HANDOFF.md → amazon_android/account_flow.py

## Import Cycles
- None detected.

## Communities (59 total, 10 thin omitted)

### Community 0 - "core.py"
Cohesion: 0.05
Nodes (58): _table_cells(), main(), parser(), report(), adb(), app_data_dir(), available_memory_mb(), avd_names() (+50 more)

### Community 1 - "Q1FlowTests"
Cohesion: 0.08
Nodes (9): build_common_steps(), build_q1_steps(), Cách xử lý ảnh tiếp theo, Phần dùng chung đã được hướng dẫn, Phần riêng từng máy, Tiến độ hướng dẫn bằng ảnh — cập nhật 13/11/2026, node(), Q1FlowTests (+1 more)

### Community 2 - "otp.py"
Cohesion: 0.10
Nodes (8): browser_launch_options(), extract_otp(), _NoRedirect, read_otp(), _read_otp_in_browser(), wait_for_new_otp(), OtpTests, PackagedBrowserTests

### Community 3 - "parse_records"
Cohesion: 0.09
Nodes (11): BulkRecord, lines(), parse_column(), parse_records(), _proxy_rows(), _url_from_cell(), validate_card(), otp_token() (+3 more)

### Community 4 - "account_flow.py"
Cohesion: 0.13
Nodes (25): _ActionNotResolved, _bounds(), country(), _button(), _country_full_row(), _form_action(), _has(), _keyboard_visible() (+17 more)

### Community 5 - "_prepare_phone"
Cohesion: 0.11
Nodes (22): open_amazon(), _confirm_menu_fallback(), _menu_evidence(), ready_for_home_menu(), _prepare_phone(), progress(), _check_stop(), collapse_apps_panel() (+14 more)

### Community 6 - "RunnerTests"
Cohesion: 0.06
Nodes (17): ProfileRegistry, absent(), ProfileRegistryTests, lookup(), broken(), RunnerTests, create(), resume() (+9 more)

### Community 7 - "PostMenuSession"
Cohesion: 0.18
Nodes (9): PostMenuSession, PostMenuStep, RunJob, PostMenuTests, first_step(), reconcile(), first(), SharedStepRecoveryTests (+1 more)

### Community 8 - ".test_only_confirmed_target_names_are_selected_for_one_start_command"
Cohesion: 0.11
Nodes (5): checkbox(), toggle(), descendants(), FakeBox, FakeButton

### Community 9 - "PROJECT_INDEX.md"
Cohesion: 0.22
Nodes (6): Hướng dẫn khi tiếp tục dự án, Bản đồ repository, Luồng q2 từ menu ba gạch, q3 — b1–b3 và nối luồng chung, q4 — Giỏ hàng, Pets, Home and DIY, q6 — Trang chủ, Giỏ hàng, menu và một thẻ

### Community 10 - "002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ"
Cohesion: 0.07
Nodes (25): 002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ, Kiểm tra bắt buộc, Phạm vi, Rủi ro và bảo trì, Điều kiện dừng, 003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật, Các bước, Kiểm tra bắt buộc (+17 more)

### Community 11 - "Danh mục từng bước đã biết — 13/11/2026"
Cohesion: 0.06
Nodes (35): B1–B3 hiện hành — Ba lượt ngẫu nhiên q1–q12, Chung b10 — Chuyển WhatsApp sang SMS, Chung b11 — Lấy và gõ OTP SMS, Chung b11a — Chạm ô OTP trên màn SMS, Chung b11b — Bấm Create your Amazon account, Chung b4 — Sign In từ menu, Chung b4a — Chạm ô SĐT, Chung b5 — Gõ số điện thoại (+27 more)

### Community 13 - "_read_nodes"
Cohesion: 0.11
Nodes (26): continue_number(), create_account(), focus_phone(), name(), phone_number(), proceed(), send_sms(), _check_summary() (+18 more)

### Community 14 - "CloudPhone"
Cohesion: 0.05
Nodes (40): cloud_adb(), cloud_screenshot(), cloud_serials(), CloudPhone, foreground(), package_path(), probe(), prop() (+32 more)

### Community 16 - "Ảnh hướng dẫn q1/q2 và menu chung lưu cục bộ"
Cohesion: 0.08
Nodes (25): B6 — Hai ảnh đính kèm mới ngày 13/11/2026, Menu chung ảnh 01 — Danh sách chữ, Menu chung ảnh 02 — App Store bên phải sau khi Amazon mở, q1 b6 — US +1 hiện nhưng chạm không đóng hộp, 14/11/2026, q1 ảnh 01 — Menu và ba thẻ, q1 ảnh 02 — Sign In cuối menu, q1 ảnh 03 — Nhập số điện thoại, q1 ảnh 04 — Chọn mã quốc gia (+17 more)

### Community 17 - "Biên bản kiểm tra thực tế — 2026-11-12"
Cohesion: 0.07
Nodes (27): b6 Country US +1 — 14/11/2026, B6 cuộn quốc gia và chọn lại — 13/11/2026, Biên bản kiểm tra thực tế — 2026-11-12, Cài và đo UiAutomator2 theo phê duyệt mới — 13/11/2026, Cập nhật luồng mẻ trước đó — 2026-11-13, Dừng riêng một máy — 14/11/2026, Focus ô nhập b4–b11 — 14/11/2026, Ghim taskbar — 13/11/2026 (+19 more)

### Community 18 - "runner.py"
Cohesion: 0.19
Nodes (4): ensure_manager_ready(), ProfileManagerWindowError, ManagerStartupTests, unavailable()

### Community 19 - "windows_identity.py"
Cohesion: 0.27
Nodes (6): create_shortcut(), relaunch_command(), runtime(), set_process_identity(), set_window_identity(), WindowsIdentityTests

### Community 20 - "_type_field"
Cohesion: 0.14
Nodes (9): enter_otp(), focus_otp(), read_sms_form(), _field(), _tap_input(), _type_field(), Phục hồi khi ô nhập chưa nhận focus ở b4–b11 — 14/11/2026, FlowRecoveryTests (+1 more)

### Community 22 - "Bàn giao dừng theo yêu cầu người dùng — 13/11/2026"
Cohesion: 0.29
Nodes (6): Bàn giao dừng theo yêu cầu người dùng — 13/11/2026, Bối cảnh đã hoàn tất trước lỗi hiện tại, Cách tiếp tục, Kiểm chứng gần nhất, Lỗi chính chưa xử lý xong, Yêu cầu mới nhất

### Community 23 - "AttemptDeadline"
Cohesion: 0.09
Nodes (12): AttemptDeadline, RegistrationState, build_q5_steps(), build_q6_steps(), build_random_steps(), random_tap(), _PrefixDeadline, b1–b3 ngẫu nhiên cho q1–q12 — 14/11/2026 (+4 more)

### Community 25 - "Nghiên cứu và tích hợp Swarmote"
Cohesion: 0.40
Nodes (4): Hành vi có bằng chứng, Kiểm thử còn lại, Nghiên cứu và tích hợp Swarmote, Phần đã áp dụng

### Community 26 - "Q3Q4FlowTests"
Cohesion: 0.21
Nodes (3): build_q3_steps(), build_q4_steps(), Q3Q4FlowTests

### Community 27 - "001 — Tách dữ liệu từng mẻ và đối chiếu số hàng"
Cohesion: 0.29
Nodes (7): 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Rủi ro và bảo trì, Thiết kế yêu cầu, Điều kiện dừng

### Community 28 - "vision.py"
Cohesion: 0.07
Nodes (17): _bounds(), _canonical_text(), _engine(), _field_contents(), _field_is_blank(), _input_box(), _join_wrapped_categories(), _normalize() (+9 more)

### Community 29 - "ProxyConfig"
Cohesion: 0.35
Nodes (4): BatchItem, parse_proxy_line(), prepare_five(), BatchSafetyTests

### Community 30 - "RecoverableStepError"
Cohesion: 0.40
Nodes (4): RecoverableStepError, action(), action(), action()

### Community 32 - "_ensure_menu"
Cohesion: 0.15
Nodes (18): _at_or_after(), sign_in(), _ensure_menu(), _find_scrolling(), _tap_for_transition(), _unique(), cart_action(), action() (+10 more)

### Community 33 - "desktop.py"
Cohesion: 0.17
Nodes (4): _automatic_resume_slots(), AccountData, DesktopResumeTests, on_worker()

### Community 37 - "profile_status"
Cohesion: 0.10
Nodes (13): create_profile(), _create_profile_form(), _open_profiles(), ProfileCreateNotSubmitted, ProxyConfig, ProxyTestFailed, visible_profile_names(), Mục tiêu và bằng chứng (+5 more)

### Community 38 - "swarmote_desktop.py"
Cohesion: 0.10
Nodes (25): ToolError, _start_and_confirm(), _activate_manager(), _descendants(), inspect(), check_stop(), _invoke(), _main_window() (+17 more)

### Community 40 - "Điều hướng hai dạng menu ba gạch"
Cohesion: 0.50
Nodes (4): Bằng chứng và phạm vi, Kiểm chứng, Quy tắc chạy, Điều hướng hai dạng menu ba gạch

### Community 41 - "time"
Cohesion: 0.09
Nodes (18): _read_nodes_once(), current(), phone_reader(), PhoneReader, ReaderResponseError, _serve(), country_reverse_points(), country_scroll() (+10 more)

### Community 42 - "Bàn giao trạng thái dự án — 13/11/2026"
Cohesion: 0.07
Nodes (27): main(), main(), B6 danh sách quốc gia vẫn mở sau khi chọn — 13/11/2026, Bàn giao trạng thái dự án — 13/11/2026, Bản chính boom4may và bản dự phòng — 14/11/2026, Bộ cài offline chia sẻ — 14/11/2026, Cài đặt máy mới, Dừng riêng máy đang chọn — 14/11/2026 (+19 more)

### Community 44 - "FakeControl"
Cohesion: 0.13
Nodes (5): ParallelInstallTests, PhoneWindow, FakeControl, InstallTests, descendants()

### Community 45 - "ResumeRegistrationStateTests"
Cohesion: 0.23
Nodes (3): ResumeRegistrationStateTests, factory(), factory()

### Community 46 - "PROJECT_HANDOFF.md"
Cohesion: 0.12
Nodes (14): Nối vào bước tạo tài khoản sau khi xác minh màn hình Amazon, Thiết kế OTP cho từng Profile, Đã chuẩn bị, B4–b11 chạy đồng thời và OCR — 14/11/2026, b6 cuộn chạm đáy rồi vuốt ngược khoảng bốn quốc gia — 14/11/2026, b6 US +1 còn mở sau bốn cú chạm — 14/11/2026, Bỏ thời hạn tổng sau menu — 14/11/2026, File chính đã sửa (+6 more)

### Community 49 - "CountryRecoveryTests"
Cohesion: 0.27
Nodes (4): CountryRecoveryTests, read(), wait(), node()

### Community 51 - "b1–b11 Reliability and Latency Implementation Plan"
Cohesion: 0.18
Nodes (10): b1–b11 Reliability and Latency Implementation Plan, Completion Criteria, File Map, Global Constraints, Review Focus, Task 1: Measure current step latency and classify existing failures, Task 2: Define safe retry, reconcile, pause, and stop behavior, Task 3: Reduce redundant UI reads and unnecessary waits (+2 more)

### Community 53 - "Danh mục ảnh nằm trong dự án"
Cohesion: 0.29
Nodes (7): amazon_android/assets/obsidian_prism.png, assets/ui_history/reset_check.png, assets/ui_history/ui-12.png, assets/ui_history/ui_palette_preview.png, assets/ui_history/ui-preview.png, assets/ui_history/ui-screenshot.png, Danh mục ảnh nằm trong dự án

### Community 55 - "Amazon Android Tool — Giai đoạn A/B"
Cohesion: 0.29
Nodes (7): Amazon Android Tool — Giai đoạn A/B, Cài trên máy Windows mới, Dán nhiều proxy, Sử dụng, Trạng thái nghiệm thu, Yêu cầu, Điện thoại đám mây Swarmote

### Community 56 - "run_batch"
Cohesion: 0.11
Nodes (18): emit(), pause_if_requested(), stop_here(), run_batch(), fill_slots(), refresh_slots(), requested(), startup_progress() (+10 more)

### Community 58 - "Giao diện vận hành"
Cohesion: 0.40
Nodes (4): Bố cục, Giao diện vận hành, Hướng thị giác, Quy tắc

### Community 59 - "Quy tắc tự động hóa sau menu ba gạch"
Cohesion: 0.40
Nodes (5): Nhận diện giao diện lúc chạy, Nhập liệu và lỗi, Quy tắc tự động hóa sau menu ba gạch, Trạng thái hiện tại của dự án, Từng máy độc lập

### Community 60 - "Amazon trên Swarmote"
Cohesion: 0.40
Nodes (4): Amazon trên Swarmote, Người dùng và công việc, Nền tảng, Điều chưa xác minh

### Community 63 - "Bộ cài chia sẻ Windows x64"
Cohesion: 0.50
Nodes (3): Bộ cài chia sẻ Windows x64, Dựng lại, Nguồn thành phần

### Community 65 - "Kiểm tra độ phủ Graphify — 13/11/2026"
Cohesion: 0.67
Nodes (3): Cách kiểm tra sau mỗi sửa đổi, Giới hạn đã xác nhận, Kiểm tra độ phủ Graphify — 13/11/2026

### Community 67 - "PreparationThreadsTests"
Cohesion: 0.29
Nodes (4): apartment_type(), PreparationThreadsTests, run(), install()

### Community 70 - "VERIFICATION.md"
Cohesion: 0.15
Nodes (11): Kết luận và tích hợp, Kết quả thực tế, So sánh bộ đọc trên q1 — 13/11/2026, Thành phần thiết bị, b1–b3 ngẫu nhiên cho 12 máy — 14/11/2026, b6 cuộn tới đáy rồi vuốt ngược — 14/11/2026, File chính đã sửa, Kết quả và giới hạn (+3 more)

## Knowledge Gaps
- **1 isolated node(s):** `amazon-android-tool`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 385 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **10 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ToolError` connect `swarmote_desktop.py` to `core.py`, `Q1FlowTests`, `otp.py`, `parse_records`, `account_flow.py`, `_prepare_phone`, `RunnerTests`, `PostMenuSession`, `_read_nodes`, `CloudPhone`, `runner.py`, `_type_field`, `._apply_bulk_text`, `AttemptDeadline`, `StopResetTests`, `vision.py`, `ProxyConfig`, `RecoverableStepError`, `_ensure_menu`, `desktop.py`, `profile_status`, `unittest`, `time`, `BatchDraft`, `CountryRecoveryTests`, `Window`, `run_batch`?**
  _High betweenness centrality (0.403) - this node is a cross-community bridge._
- **Are the 42 inferred relationships involving `ToolError` (e.g. with `_read_nodes_once()` and `_tap_for_transition()`) actually correct?**
  _`ToolError` has 42 INFERRED edges - model-reasoned connections that need verification._
- **What connects `amazon-android-tool` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `core.py` be split into smaller, more focused modules?**
  _Cohesion score 0.052556615866685655 - nodes in this community are weakly interconnected._
- **Why does `CloudPhone` connect `CloudPhone` to `core.py`, `Q1FlowTests`, `account_flow.py`, `_prepare_phone`, `PostMenuSession`, `_read_nodes`, `runner.py`, `_type_field`, `AttemptDeadline`, `Q3Q4FlowTests`, `_ensure_menu`, `desktop.py`, `swarmote_desktop.py`, `unittest`, `time`, `ResumeRegistrationStateTests`, `CountryRecoveryTests`, `Window`, `run_batch`?**
  _High betweenness centrality (0.116) - this node is a cross-community bridge._
- **Are the 68 inferred relationships involving `CloudPhone` (e.g. with `build_common_steps()` and `_country_full_row()`) actually correct?**
  _`CloudPhone` has 68 INFERRED edges - model-reasoned connections that need verification._
- **Should `Q1FlowTests` be split into smaller, more focused modules?**
  _Cohesion score 0.08127721335268505 - nodes in this community are weakly interconnected._