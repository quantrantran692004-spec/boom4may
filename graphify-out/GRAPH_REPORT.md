# Graph Report - boom4may  (2026-11-14)

## Corpus Check
- 115 files · ~85,688 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 1, .bat 1, .pyw 1)

## Summary
- 1366 nodes · 4502 edges · 67 communities (58 shown, 9 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 631 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5d592d38`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- screen
- Q1FlowTests
- otp.py
- core.py
- subprocess
- open_adb_shell
- RunnerTests
- PostMenuSession
- .test_only_confirmed_target_names_are_selected_for_one_start_command
- PROJECT_INDEX.md
- 002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ
- Danh mục từng bước đã biết — 13/11/2026
- setup.py
- _read_nodes
- CloudPhone
- amazon-android-tool
- Ảnh hướng dẫn q1/q2 và menu chung lưu cục bộ
- Biên bản kiểm tra thực tế — 2026-11-12
- isolated_reader.py
- ToolError
- _prepare_phone
- browser_launch_options
- Window
- test_q1_flow.py
- AttemptDeadline
- Nghiên cứu và tích hợp Swarmote
- cli.py
- SafetyTests
- vision.py
- registration.py
- parse_records
- account_flow.py
- AccountData
- _type_field
- desktop.py
- .test_transition_keeps_observing_after_short_wait_without_tapping
- profile_status
- swarmote_desktop.py
- UiBackendTests
- Bàn giao trạng thái dự án — 13/11/2026
- build_q2_steps
- FakeControl
- PreparationProgressTests
- MENU_ROUTING.md
- PROJECT_HANDOFF.md
- CloudBridgeTests
- CountryRecoveryTests
- ._label
- b1–b11 Reliability and Latency Implementation Plan
- ResumeRegistrationStateTests
- Danh mục ảnh nằm trong dự án
- validate_card
- Amazon Android Tool — Giai đoạn A/B
- BatchDraft
- Giao diện vận hành
- Quy tắc tự động hóa sau menu ba gạch
- Amazon trên Swarmote
- ensure_manager_ready
- OTP_DESIGN.md
- Bộ cài chia sẻ Windows x64
- ._apply_bulk_text
- Kiểm tra độ phủ Graphify — 13/11/2026
- Bàn giao dừng theo yêu cầu người dùng — 13/11/2026
- PreparationThreadsTests
- 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng
- So sánh bộ đọc trên q1 — 13/11/2026

## God Nodes (most connected - your core abstractions)
1. `ToolError` - 245 edges
2. `CloudPhone` - 161 edges
3. `RunJob` - 93 edges
4. `AttemptDeadline` - 86 edges
5. `build_common_steps()` - 77 edges
6. `Window` - 77 edges
7. `_read_nodes()` - 54 edges
8. `Q1FlowTests` - 51 edges
9. `PostMenuSession` - 44 edges
10. `screen()` - 42 edges

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

## Communities (67 total, 9 thin omitted)

### Community 0 - "screen"
Cohesion: 0.16
Nodes (21): continue_number(), create_account(), enter_otp(), focus_otp(), focus_phone(), name(), phone_number(), proceed() (+13 more)

### Community 1 - "Q1FlowTests"
Cohesion: 0.09
Nodes (6): build_common_steps(), build_q1_steps(), category(), node(), Q1FlowTests, provider_read()

### Community 2 - "otp.py"
Cohesion: 0.11
Nodes (7): extract_otp(), _NoRedirect, read_otp(), _read_otp_in_browser(), validate_otp_url(), wait_for_new_otp(), OtpTests

### Community 3 - "core.py"
Cohesion: 0.28
Nodes (19): adb(), available_memory_mb(), check_play(), configure_avd(), connected_devices(), Device, device_avd_name(), device_resources() (+11 more)

### Community 4 - "subprocess"
Cohesion: 0.08
Nodes (26): save(), default_path(), AppSettings, load_settings(), save_settings(), settings_path(), create_shortcut(), relaunch_command() (+18 more)

### Community 5 - "open_adb_shell"
Cohesion: 0.11
Nodes (22): ready_for_home_menu(), _check_stop(), collapse_apps_panel(), _descendants(), open_adb_shell(), _pause(), _phone_window(), _progress_reporter() (+14 more)

### Community 6 - "RunnerTests"
Cohesion: 0.06
Nodes (18): ProfileRegistry, ProfileLookupError, ProfileNotFound, Thiết kế yêu cầu, absent(), ProfileRegistryTests, lookup(), broken() (+10 more)

### Community 7 - "PostMenuSession"
Cohesion: 0.14
Nodes (13): reconcile(), route(), PostMenuSession, PostMenuStep, RecoverableStepError, RunJob, PostMenuTests, first_step() (+5 more)

### Community 8 - ".test_only_confirmed_target_names_are_selected_for_one_start_command"
Cohesion: 0.09
Nodes (13): ProfileStartNotSubmitted, _select_profile_rows(), _selected_profile_names(), start_profile(), start_profiles_together(), _wait_for_selected(), delayed_start(), BatchStartTests (+5 more)

### Community 9 - "PROJECT_INDEX.md"
Cohesion: 0.19
Nodes (7): Hướng dẫn khi tiếp tục dự án, Quy trình Swarmote hiện tại, Bản đồ repository, q3 — b1–b3 và nối luồng chung, q4 — Giỏ hàng, Pets, Home and DIY, q5 — ba thẻ riêng và b4–b11 chung, q6 — Trang chủ, Giỏ hàng, menu và một thẻ

### Community 10 - "002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ"
Cohesion: 0.06
Nodes (26): 002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ, Các bước, Kiểm tra bắt buộc, Phạm vi, Rủi ro và bảo trì, Điều kiện dừng, 003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật, Các bước (+18 more)

### Community 11 - "Danh mục từng bước đã biết — 13/11/2026"
Cohesion: 0.06
Nodes (34): Chung b10 — Chuyển WhatsApp sang SMS, Chung b11 — Lấy và gõ OTP SMS, Chung b11a — Chạm ô OTP trên màn SMS, Chung b11b — Bấm Create your Amazon account, Chung b4 — Sign In từ menu, Chung b4a — Chạm ô SĐT, Chung b5 — Gõ số điện thoại, Chung b6 — Chọn United States +1 (+26 more)

### Community 12 - "setup.py"
Cohesion: 0.24
Nodes (12): app_data_dir(), avd_names(), create_avd(), doctor(), executable(), installed_image(), run(), sdk_root() (+4 more)

### Community 13 - "_read_nodes"
Cohesion: 0.24
Nodes (19): _at_or_after(), sign_in(), _ensure_menu(), _find_scrolling(), _read_nodes(), _tap_for_transition(), _unique(), cart_action() (+11 more)

### Community 14 - "CloudPhone"
Cohesion: 0.13
Nodes (12): CloudPhone, _confirm_menu_fallback(), _menu_evidence(), MenuReadUnavailable, _nodes(), budget(), open_home_menu(), _tap() (+4 more)

### Community 16 - "Ảnh hướng dẫn q1/q2 và menu chung lưu cục bộ"
Cohesion: 0.08
Nodes (24): B6 — Hai ảnh đính kèm mới ngày 13/11/2026, Menu chung ảnh 01 — Danh sách chữ, Menu chung ảnh 02 — App Store bên phải sau khi Amazon mở, q1 b6 — US +1 hiện nhưng chạm không đóng hộp, 14/11/2026, q1 ảnh 01 — Menu và ba thẻ, q1 ảnh 02 — Sign In cuối menu, q1 ảnh 03 — Nhập số điện thoại, q1 ảnh 04 — Chọn mã quốc gia (+16 more)

### Community 17 - "Biên bản kiểm tra thực tế — 2026-11-12"
Cohesion: 0.08
Nodes (24): b6 Country US +1 — 14/11/2026, B6 cuộn quốc gia và chọn lại — 13/11/2026, Biên bản kiểm tra thực tế — 2026-11-12, Cài và đo UiAutomator2 theo phê duyệt mới — 13/11/2026, Cập nhật luồng mẻ trước đó — 2026-11-13, Ghim taskbar — 13/11/2026, Giao diện sáng, dễ đọc — 2026-11-13, Hướng Swarmote theo ảnh người dùng (+16 more)

### Community 18 - "isolated_reader.py"
Cohesion: 0.19
Nodes (8): phone_reader(), PhoneReader, ReaderResponseError, _serve(), fake_worker(), IsolationTests, duplicate(), production_worker_with_fake_android()

### Community 19 - "ToolError"
Cohesion: 0.17
Nodes (8): BatchItem, parse_proxy_line(), prepare_five(), create_profile(), ProxyConfig, Mục tiêu và bằng chứng, BatchSafetyTests, CreationWindowVisibilityTests

### Community 20 - "_prepare_phone"
Cohesion: 0.23
Nodes (8): emit(), _prepare_phone(), progress(), run_batch(), fill_slots(), refresh_slots(), startup_progress(), Hàng đợi 4 máy với giới hạn 2 Running — 14/11/2026

### Community 23 - "test_q1_flow.py"
Cohesion: 0.19
Nodes (6): menu_layout(), resume_common_index(), route_list_menu(), visit_home(), Quy tắc chạy, Mã hiện có

### Community 24 - "AttemptDeadline"
Cohesion: 0.16
Nodes (5): verify_menu_open(), AttemptDeadline, type_characters(), fail(), Q6FlowTests

### Community 25 - "Nghiên cứu và tích hợp Swarmote"
Cohesion: 0.40
Nodes (4): Hành vi có bằng chứng, Kiểm thử còn lại, Nghiên cứu và tích hợp Swarmote, Phần đã áp dụng

### Community 26 - "cli.py"
Cohesion: 0.20
Nodes (9): main(), parser(), report(), cloud_serials(), scan(), get_device(), print_json(), Store (+1 more)

### Community 28 - "vision.py"
Cohesion: 0.07
Nodes (17): _bounds(), _canonical_text(), _engine(), _field_contents(), _field_is_blank(), _input_box(), _join_wrapped_categories(), _normalize() (+9 more)

### Community 29 - "registration.py"
Cohesion: 0.20
Nodes (14): require_online(), ToolError, _field_for_label(), fill_identifier(), fill_signup_form(), _nodes(), open_entry(), status() (+6 more)

### Community 30 - "parse_records"
Cohesion: 0.14
Nodes (7): BulkRecord, lines(), parse_column(), parse_records(), _table_cells(), _url_from_cell(), BulkInputTests

### Community 32 - "account_flow.py"
Cohesion: 0.15
Nodes (25): _ActionNotResolved, _bounds(), country(), _button(), _country_full_row(), _form_action(), _has(), _keyboard_visible() (+17 more)

### Community 33 - "AccountData"
Cohesion: 0.14
Nodes (5): _automatic_resume_slots(), AccountData, DesktopResumeTests, install(), on_worker()

### Community 34 - "_type_field"
Cohesion: 0.28
Nodes (3): _type_field(), FlowRecoveryTests, form()

### Community 35 - "desktop.py"
Cohesion: 0.12
Nodes (6): RegistrationState, build_q3_steps(), build_q4_steps(), build_q5_steps(), Q3Q4FlowTests, Q5FlowTests

### Community 36 - ".test_transition_keeps_observing_after_short_wait_without_tapping"
Cohesion: 0.17
Nodes (5): _start_and_confirm(), ExtendedRecoveryTests, read(), read(), menu()

### Community 37 - "profile_status"
Cohesion: 0.17
Nodes (6): _open_profiles(), visible_profile_names(), control(), ProfilesNavigationTests, descendants(), descendants()

### Community 38 - "swarmote_desktop.py"
Cohesion: 0.15
Nodes (15): visible_lookup(), _activate_manager(), _create_profile_form(), _invoke(), _one(), _profile_checkbox(), _profile_form_open(), _profile_row_status() (+7 more)

### Community 41 - "UiBackendTests"
Cohesion: 0.14
Nodes (10): swarmote_adb_path(), swarmote_tunnel_owner(), _connect(), country_scroll(), _failed(), read_tree(), ready(), _session() (+2 more)

### Community 42 - "Bàn giao trạng thái dự án — 13/11/2026"
Cohesion: 0.07
Nodes (26): main(), main(), B6 danh sách quốc gia vẫn mở sau khi chọn — 13/11/2026, Bàn giao trạng thái dự án — 13/11/2026, Bản chính boom4may và bản dự phòng — 14/11/2026, Bộ cài offline chia sẻ — 14/11/2026, Cài đặt máy mới, Dự phòng dùng chung khi chạy song song — 14/11/2026 (+18 more)

### Community 43 - "build_q2_steps"
Cohesion: 0.24
Nodes (6): build_q2_steps(), Cách xử lý ảnh tiếp theo, Phần dùng chung đã được hướng dẫn, Phần riêng từng máy, Tiến độ hướng dẫn bằng ảnh — cập nhật 13/11/2026, Q2FlowTests

### Community 44 - "FakeControl"
Cohesion: 0.12
Nodes (7): install_amazon(), check_stop(), ParallelInstallTests, PhoneWindow, FakeControl, InstallTests, descendants()

### Community 46 - "MENU_ROUTING.md"
Cohesion: 0.27
Nodes (6): Bằng chứng và phạm vi, Kiểm chứng, Điều hướng hai dạng menu ba gạch, Luồng q1 từ menu ba gạch tới nhập OTP, Thử trên q1 đã có, Luồng q2 từ menu ba gạch

### Community 47 - "PROJECT_HANDOFF.md"
Cohesion: 0.20
Nodes (8): B4–b11 chạy đồng thời và OCR — 14/11/2026, b6 US +1 còn mở sau bốn cú chạm — 14/11/2026, Bỏ thời hạn tổng sau menu — 14/11/2026, Lỗi chạy song song q3 Terminal trùng / q1 chưa thấy menu — 14/11/2026, Phạm vi q1–q12 sau phản hồi người dùng — 14/11/2026, Tách bộ đọc thành tiến trình riêng từng máy — 14/11/2026, Tự tìm và mở Swarmote khi chạy mẻ — 14/11/2026, Lỗi chạy song song q3 Terminal trùng / q1 chưa thấy menu — 14/11/2026

### Community 48 - "CloudBridgeTests"
Cohesion: 0.20
Nodes (7): open_amazon(), foreground(), package_path(), probe(), prop(), CloudBridgeTests, adb()

### Community 49 - "CountryRecoveryTests"
Cohesion: 0.27
Nodes (4): CountryRecoveryTests, read(), wait(), node()

### Community 51 - "b1–b11 Reliability and Latency Implementation Plan"
Cohesion: 0.18
Nodes (10): b1–b11 Reliability and Latency Implementation Plan, Completion Criteria, File Map, Global Constraints, Review Focus, Task 1: Measure current step latency and classify existing failures, Task 2: Define safe retry, reconcile, pause, and stop behavior, Task 3: Reduce redundant UI reads and unnecessary waits (+2 more)

### Community 52 - "ResumeRegistrationStateTests"
Cohesion: 0.25
Nodes (3): ResumeRegistrationStateTests, factory(), factory()

### Community 53 - "Danh mục ảnh nằm trong dự án"
Cohesion: 0.29
Nodes (7): amazon_android/assets/obsidian_prism.png, assets/ui_history/reset_check.png, assets/ui_history/ui-12.png, assets/ui_history/ui_palette_preview.png, assets/ui_history/ui-preview.png, assets/ui_history/ui-screenshot.png, Danh mục ảnh nằm trong dự án

### Community 55 - "Amazon Android Tool — Giai đoạn A/B"
Cohesion: 0.33
Nodes (6): Amazon Android Tool — Giai đoạn A/B, Cài trên máy Windows mới, Sử dụng, Trạng thái nghiệm thu, Yêu cầu, Điện thoại đám mây Swarmote

### Community 56 - "BatchDraft"
Cohesion: 0.15
Nodes (3): BatchDraft, BatchDraftTests, StopResetTests

### Community 58 - "Giao diện vận hành"
Cohesion: 0.40
Nodes (4): Bố cục, Giao diện vận hành, Hướng thị giác, Quy tắc

### Community 59 - "Quy tắc tự động hóa sau menu ba gạch"
Cohesion: 0.40
Nodes (5): Nhận diện giao diện lúc chạy, Nhập liệu và lỗi, Quy tắc tự động hóa sau menu ba gạch, Trạng thái hiện tại của dự án, Từng máy độc lập

### Community 60 - "Amazon trên Swarmote"
Cohesion: 0.40
Nodes (4): Amazon trên Swarmote, Người dùng và công việc, Nền tảng, Điều chưa xác minh

### Community 61 - "ensure_manager_ready"
Cohesion: 0.17
Nodes (8): ensure_manager_ready(), inspect(), _main_window(), collect(), ProfileManagerWindowError, _swarmote_exe(), ManagerStartupTests, unavailable()

### Community 62 - "OTP_DESIGN.md"
Cohesion: 0.50
Nodes (3): Nối vào bước tạo tài khoản sau khi xác minh màn hình Amazon, Thiết kế OTP cho từng Profile, Đã chuẩn bị

### Community 63 - "Bộ cài chia sẻ Windows x64"
Cohesion: 0.50
Nodes (3): Bộ cài chia sẻ Windows x64, Dựng lại, Nguồn thành phần

### Community 65 - "Kiểm tra độ phủ Graphify — 13/11/2026"
Cohesion: 0.50
Nodes (3): Cách kiểm tra sau mỗi sửa đổi, Giới hạn đã xác nhận, Kiểm tra độ phủ Graphify — 13/11/2026

### Community 66 - "Bàn giao dừng theo yêu cầu người dùng — 13/11/2026"
Cohesion: 0.25
Nodes (7): Bàn giao dừng theo yêu cầu người dùng — 13/11/2026, Bối cảnh đã hoàn tất trước lỗi hiện tại, Cách tiếp tục, Kiểm chứng gần nhất, Lỗi chính chưa xử lý xong, Yêu cầu mới nhất, Đường mã cần xem tiếp

### Community 67 - "PreparationThreadsTests"
Cohesion: 0.29
Nodes (4): apartment_type(), PreparationThreadsTests, run(), install()

### Community 68 - "001 — Tách dữ liệu từng mẻ và đối chiếu số hàng"
Cohesion: 0.29
Nodes (7): 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Rủi ro và bảo trì, Thiết kế yêu cầu, Điều kiện dừng

### Community 70 - "So sánh bộ đọc trên q1 — 13/11/2026"
Cohesion: 0.50
Nodes (4): Kết luận và tích hợp, Kết quả thực tế, So sánh bộ đọc trên q1 — 13/11/2026, Thành phần thiết bị

## Knowledge Gaps
- **1 isolated node(s):** `amazon-android-tool`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 367 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ToolError` connect `registration.py` to `screen`, `Q1FlowTests`, `otp.py`, `core.py`, `subprocess`, `open_adb_shell`, `RunnerTests`, `PostMenuSession`, `.test_only_confirmed_target_names_are_selected_for_one_start_command`, `setup.py`, `_read_nodes`, `CloudPhone`, `isolated_reader.py`, `ToolError`, `_prepare_phone`, `Window`, `test_q1_flow.py`, `AttemptDeadline`, `cli.py`, `vision.py`, `parse_records`, `account_flow.py`, `AccountData`, `_type_field`, `desktop.py`, `.test_transition_keeps_observing_after_short_wait_without_tapping`, `profile_status`, `swarmote_desktop.py`, `runner.py`, `UiBackendTests`, `build_q2_steps`, `FakeControl`, `CloudBridgeTests`, `CountryRecoveryTests`, `BatchDraft`, `ensure_manager_ready`, `._apply_bulk_text`?**
  _High betweenness centrality (0.458) - this node is a cross-community bridge._
- **Are the 40 inferred relationships involving `ToolError` (e.g. with `_read_nodes_once()` and `_tap_for_transition()`) actually correct?**
  _`ToolError` has 40 INFERRED edges - model-reasoned connections that need verification._
- **What connects `amazon-android-tool` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Q1FlowTests` be split into smaller, more focused modules?**
  _Cohesion score 0.08653061224489796 - nodes in this community are weakly interconnected._
- **Why does `build_common_steps()` connect `Q1FlowTests` to `screen`, `otp.py`, `PostMenuSession`, `PROJECT_INDEX.md`, `_read_nodes`, `CloudPhone`, `test_q1_flow.py`, `AttemptDeadline`, `registration.py`, `account_flow.py`, `AccountData`, `desktop.py`, `swarmote_desktop.py`, `runner.py`, `Bàn giao trạng thái dự án — 13/11/2026`, `build_q2_steps`, `MENU_ROUTING.md`, `PROJECT_HANDOFF.md`, `CountryRecoveryTests`, `b1–b11 Reliability and Latency Implementation Plan`, `Quy tắc tự động hóa sau menu ba gạch`?**
  _High betweenness centrality (0.088) - this node is a cross-community bridge._
- **Are the 66 inferred relationships involving `CloudPhone` (e.g. with `build_common_steps()` and `_country_full_row()`) actually correct?**
  _`CloudPhone` has 66 INFERRED edges - model-reasoned connections that need verification._
- **Should `otp.py` be split into smaller, more focused modules?**
  _Cohesion score 0.11330049261083744 - nodes in this community are weakly interconnected._