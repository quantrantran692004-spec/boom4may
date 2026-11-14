# Graph Report - boom4may  (2026-11-14)

## Corpus Check
- 115 files · ~84,916 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 1, .bat 1, .pyw 1)

## Summary
- 1356 nodes · 4465 edges · 59 communities (54 shown, 5 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 621 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e92211e5`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- screen
- Q1FlowTests
- bulk_input.py
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
- open_home_menu
- amazon-android-tool
- Ảnh hướng dẫn q1/q2 và menu chung lưu cục bộ
- Biên bản kiểm tra thực tế — 2026-11-12
- test_isolated_reader.py
- ToolError
- _prepare_phone
- pathlib
- Window
- build_q2_steps
- AttemptDeadline
- Nghiên cứu và tích hợp Swarmote
- cli.py
- SafetyTests
- vision.py
- time
- main
- CloudPhone
- account_flow.py
- RunJob
- _type_field
- desktop.py
- .test_transition_keeps_observing_after_short_wait_without_tapping
- profile_status
- swarmote_desktop.py
- runner.py
- _nodes
- windows_identity.py
- Bàn giao trạng thái dự án — 13/11/2026
- Phần riêng từng máy
- FakeControl
- PreparationProgressTests
- MENU_ROUTING.md
- PROJECT_HANDOFF.md
- CloudBridgeTests
- CountryRecoveryTests
- Danh mục ảnh nằm trong dự án
- Amazon Android Tool — Giai đoạn A/B
- BatchDraft
- Giao diện vận hành
- Quy tắc tự động hóa sau menu ba gạch
- Amazon trên Swarmote
- OTP_DESIGN.md
- Bộ cài chia sẻ Windows x64
- Kiểm tra độ phủ Graphify — 13/11/2026

## God Nodes (most connected - your core abstractions)
1. `ToolError` - 240 edges
2. `CloudPhone` - 161 edges
3. `RunJob` - 91 edges
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

## Communities (59 total, 5 thin omitted)

### Community 0 - "screen"
Cohesion: 0.20
Nodes (18): continue_number(), create_account(), enter_otp(), focus_otp(), focus_phone(), name(), phone_number(), proceed() (+10 more)

### Community 1 - "Q1FlowTests"
Cohesion: 0.09
Nodes (6): build_common_steps(), build_q1_steps(), category(), node(), Q1FlowTests, provider_read()

### Community 2 - "bulk_input.py"
Cohesion: 0.06
Nodes (16): BulkRecord, lines(), parse_column(), parse_records(), _table_cells(), _url_from_cell(), browser_launch_options(), extract_otp() (+8 more)

### Community 3 - "core.py"
Cohesion: 0.28
Nodes (20): adb(), available_memory_mb(), check_play(), configure_avd(), connected_devices(), Device, device_avd_name(), device_resources() (+12 more)

### Community 4 - "subprocess"
Cohesion: 0.15
Nodes (13): main(), check_runtime(), main(), verify(), _app_installed(), _app_paths(), _check_external_apps(), _install_python_dependencies() (+5 more)

### Community 5 - "open_adb_shell"
Cohesion: 0.09
Nodes (25): ready_for_home_menu(), _tap(), _check_stop(), collapse_apps_panel(), ensure_manager_ready(), install_amazon(), open_adb_shell(), _pause() (+17 more)

### Community 6 - "RunnerTests"
Cohesion: 0.06
Nodes (15): ProfileRegistry, ProfileNotFound, absent(), ProfileRegistryTests, lookup(), broken(), RunnerTests, create() (+7 more)

### Community 7 - "PostMenuSession"
Cohesion: 0.07
Nodes (23): route(), PostMenuSession, PostMenuStep, RecoverableStepError, b1–b11 Reliability and Latency Implementation Plan, Completion Criteria, File Map, Global Constraints (+15 more)

### Community 8 - ".test_only_confirmed_target_names_are_selected_for_one_start_command"
Cohesion: 0.11
Nodes (6): BatchStartTests, checkbox(), toggle(), descendants(), FakeBox, FakeButton

### Community 9 - "PROJECT_INDEX.md"
Cohesion: 0.19
Nodes (7): Hướng dẫn khi tiếp tục dự án, Quy trình Swarmote hiện tại, Bản đồ repository, q3 — b1–b3 và nối luồng chung, q4 — Giỏ hàng, Pets, Home and DIY, q5 — ba thẻ riêng và b4–b11 chung, q6 — Trang chủ, Giỏ hàng, menu và một thẻ

### Community 10 - "002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ"
Cohesion: 0.05
Nodes (33): 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Rủi ro và bảo trì, Thiết kế yêu cầu, Điều kiện dừng, 002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ (+25 more)

### Community 11 - "Danh mục từng bước đã biết — 13/11/2026"
Cohesion: 0.06
Nodes (34): Chung b10 — Chuyển WhatsApp sang SMS, Chung b11 — Lấy và gõ OTP SMS, Chung b11a — Chạm ô OTP trên màn SMS, Chung b11b — Bấm Create your Amazon account, Chung b4 — Sign In từ menu, Chung b4a — Chạm ô SĐT, Chung b5 — Gõ số điện thoại, Chung b6 — Chọn United States +1 (+26 more)

### Community 12 - "setup.py"
Cohesion: 0.23
Nodes (12): app_data_dir(), avd_names(), create_avd(), doctor(), executable(), installed_image(), run(), sdk_root() (+4 more)

### Community 13 - "_read_nodes"
Cohesion: 0.26
Nodes (19): _at_or_after(), country(), sign_in(), _ensure_menu(), _find_scrolling(), _read_nodes(), _tap_for_transition(), _visible() (+11 more)

### Community 14 - "open_home_menu"
Cohesion: 0.19
Nodes (7): _confirm_menu_fallback(), _menu_evidence(), open_home_menu(), Thu panel Apps sau khi mở Amazon — 14/11/2026, ParallelNavigationRegressionTests, Cập nhật luồng mẻ trước đó — 2026-11-13, q14 mở Amazon lần đầu — 2026-11-13

### Community 16 - "Ảnh hướng dẫn q1/q2 và menu chung lưu cục bộ"
Cohesion: 0.08
Nodes (24): B6 — Hai ảnh đính kèm mới ngày 13/11/2026, Menu chung ảnh 01 — Danh sách chữ, Menu chung ảnh 02 — App Store bên phải sau khi Amazon mở, q1 b6 — US +1 hiện nhưng chạm không đóng hộp, 14/11/2026, q1 ảnh 01 — Menu và ba thẻ, q1 ảnh 02 — Sign In cuối menu, q1 ảnh 03 — Nhập số điện thoại, q1 ảnh 04 — Chọn mã quốc gia (+16 more)

### Community 17 - "Biên bản kiểm tra thực tế — 2026-11-12"
Cohesion: 0.09
Nodes (22): b6 Country US +1 — 14/11/2026, B6 cuộn quốc gia và chọn lại — 13/11/2026, Biên bản kiểm tra thực tế — 2026-11-12, Cài và đo UiAutomator2 theo phê duyệt mới — 13/11/2026, Ghim taskbar — 13/11/2026, Giao diện sáng, dễ đọc — 2026-11-13, Hướng Swarmote theo ảnh người dùng, Kiểm chứng bỏ thời hạn tổng sau menu — 14/11/2026 (+14 more)

### Community 18 - "test_isolated_reader.py"
Cohesion: 0.20
Nodes (6): phone_reader(), PhoneReader, ReaderResponseError, fake_worker(), IsolationTests, duplicate()

### Community 19 - "ToolError"
Cohesion: 0.11
Nodes (12): validate_card(), ToolError, _start_and_confirm(), create_profile(), check_stop(), ProxyConfig, Mục tiêu và bằng chứng, Tự phục hồi lỗi tạm thời trong mẻ nhiều máy — 14/11/2026 (+4 more)

### Community 20 - "_prepare_phone"
Cohesion: 0.15
Nodes (12): emit(), _prepare_phone(), progress(), run_batch(), fill_slots(), refresh_slots(), startup_progress(), visible_lookup() (+4 more)

### Community 21 - "pathlib"
Cohesion: 0.23
Nodes (7): save(), default_path(), AppSettings, load_settings(), save_settings(), settings_path(), SettingsTests

### Community 22 - "Window"
Cohesion: 0.09
Nodes (4): _edge_light(), Window, otp_token(), Các bước

### Community 23 - "build_q2_steps"
Cohesion: 0.12
Nodes (12): home_visible(), menu_layout(), resume_common_index(), route_list_menu(), _tap(), _unique(), visit_home(), build_q2_steps() (+4 more)

### Community 24 - "AttemptDeadline"
Cohesion: 0.14
Nodes (4): AttemptDeadline, type_characters(), read(), MenuReturnTests

### Community 25 - "Nghiên cứu và tích hợp Swarmote"
Cohesion: 0.40
Nodes (4): Hành vi có bằng chứng, Kiểm thử còn lại, Nghiên cứu và tích hợp Swarmote, Phần đã áp dụng

### Community 26 - "cli.py"
Cohesion: 0.14
Nodes (17): BatchItem, parse_proxy_line(), prepare_five(), main(), parser(), report(), open_amazon(), foreground() (+9 more)

### Community 28 - "vision.py"
Cohesion: 0.07
Nodes (17): _bounds(), _canonical_text(), _engine(), _field_contents(), _field_is_blank(), _input_box(), _join_wrapped_categories(), _normalize() (+9 more)

### Community 29 - "time"
Cohesion: 0.09
Nodes (21): swarmote_tunnel_owner(), reconcile(), _field_for_label(), fill_identifier(), fill_signup_form(), _nodes(), open_entry(), status() (+13 more)

### Community 30 - "main"
Cohesion: 0.20
Nodes (8): main(), Đợt tăng tốc và tự phục hồi b4–b11 ngày 13/11/2026, File dự án mà Graphify không phân tích trực tiếp, .gitignore, Launch Swarmote Tool.pyw, pyproject.toml, Ảnh PNG trong dự án, LauncherTests

### Community 31 - "CloudPhone"
Cohesion: 0.12
Nodes (10): CloudPhone, prop(), RegistrationState, build_q3_steps(), build_q4_steps(), Q3Q4FlowTests, Q5FlowTests, Q6FlowTests (+2 more)

### Community 32 - "account_flow.py"
Cohesion: 0.14
Nodes (22): _ActionNotResolved, _bounds(), _button(), _country_full_row(), _form_action(), _has(), _keyboard_visible(), _parse_ui_nodes() (+14 more)

### Community 33 - "RunJob"
Cohesion: 0.13
Nodes (10): _automatic_resume_slots(), AccountData, RunJob, DesktopResumeTests, apartment_type(), PreparationThreadsTests, run(), install() (+2 more)

### Community 34 - "_type_field"
Cohesion: 0.28
Nodes (3): _type_field(), FlowRecoveryTests, form()

### Community 35 - "desktop.py"
Cohesion: 0.13
Nodes (5): verify_menu_open(), _crystal_art(), main(), build_q5_steps(), set_process_identity()

### Community 37 - "profile_status"
Cohesion: 0.18
Nodes (6): _open_profiles(), visible_profile_names(), control(), ProfilesNavigationTests, descendants(), descendants()

### Community 38 - "swarmote_desktop.py"
Cohesion: 0.10
Nodes (30): _activate_manager(), _create_profile_form(), _descendants(), _invoke(), _main_window(), collect(), _one(), _profile_checkbox() (+22 more)

### Community 40 - "_nodes"
Cohesion: 0.24
Nodes (4): MenuReadUnavailable, _nodes(), budget(), HomeMenuTests

### Community 41 - "windows_identity.py"
Cohesion: 0.31
Nodes (5): create_shortcut(), relaunch_command(), runtime(), set_window_identity(), WindowsIdentityTests

### Community 42 - "Bàn giao trạng thái dự án — 13/11/2026"
Cohesion: 0.13
Nodes (15): B6 danh sách quốc gia vẫn mở sau khi chọn — 13/11/2026, Bàn giao trạng thái dự án — 13/11/2026, Bản chính boom4may và bản dự phòng — 14/11/2026, Bộ cài offline chia sẻ — 14/11/2026, Cài đặt máy mới, Dự phòng dùng chung khi chạy song song — 14/11/2026, Mục tiêu và quy tắc đã chốt, q3/q4 đã nối b1–b3 và thử đồng thời bốn luồng — 13/11/2026 (+7 more)

### Community 43 - "Phần riêng từng máy"
Cohesion: 0.50
Nodes (4): Cách xử lý ảnh tiếp theo, Phần dùng chung đã được hướng dẫn, Phần riêng từng máy, Tiến độ hướng dẫn bằng ảnh — cập nhật 13/11/2026

### Community 44 - "FakeControl"
Cohesion: 0.13
Nodes (5): ParallelInstallTests, PhoneWindow, FakeControl, InstallTests, descendants()

### Community 46 - "MENU_ROUTING.md"
Cohesion: 0.27
Nodes (6): Bằng chứng và phạm vi, Kiểm chứng, Điều hướng hai dạng menu ba gạch, Luồng q1 từ menu ba gạch tới nhập OTP, Thử trên q1 đã có, Luồng q2 từ menu ba gạch

### Community 47 - "PROJECT_HANDOFF.md"
Cohesion: 0.13
Nodes (12): Kết luận và tích hợp, Kết quả thực tế, So sánh bộ đọc trên q1 — 13/11/2026, Thành phần thiết bị, B4–b11 chạy đồng thời và OCR — 14/11/2026, b6 US +1 còn mở sau bốn cú chạm — 14/11/2026, Bỏ thời hạn tổng sau menu — 14/11/2026, Lỗi chạy song song q3 Terminal trùng / q1 chưa thấy menu — 14/11/2026 (+4 more)

### Community 48 - "CloudBridgeTests"
Cohesion: 0.23
Nodes (4): cloud_serials(), CloudBridgeTests, adb(), Ẩn cửa sổ cmd khi gọi ADB — 2026-11-13

### Community 49 - "CountryRecoveryTests"
Cohesion: 0.27
Nodes (4): CountryRecoveryTests, read(), wait(), node()

### Community 53 - "Danh mục ảnh nằm trong dự án"
Cohesion: 0.29
Nodes (7): amazon_android/assets/obsidian_prism.png, assets/ui_history/reset_check.png, assets/ui_history/ui-12.png, assets/ui_history/ui_palette_preview.png, assets/ui_history/ui-preview.png, assets/ui_history/ui-screenshot.png, Danh mục ảnh nằm trong dự án

### Community 55 - "Amazon Android Tool — Giai đoạn A/B"
Cohesion: 0.33
Nodes (6): Amazon Android Tool — Giai đoạn A/B, Cài trên máy Windows mới, Sử dụng, Trạng thái nghiệm thu, Yêu cầu, Điện thoại đám mây Swarmote

### Community 56 - "BatchDraft"
Cohesion: 0.14
Nodes (4): BatchDraft, BatchDraftTests, StopResetTests, install()

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
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 365 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ToolError` connect `ToolError` to `screen`, `Q1FlowTests`, `bulk_input.py`, `core.py`, `open_adb_shell`, `RunnerTests`, `PostMenuSession`, `setup.py`, `_read_nodes`, `open_home_menu`, `test_isolated_reader.py`, `_prepare_phone`, `pathlib`, `Window`, `build_q2_steps`, `AttemptDeadline`, `cli.py`, `vision.py`, `time`, `CloudPhone`, `account_flow.py`, `RunJob`, `_type_field`, `desktop.py`, `profile_status`, `swarmote_desktop.py`, `runner.py`, `_nodes`, `CloudBridgeTests`, `CountryRecoveryTests`, `BatchDraft`?**
  _High betweenness centrality (0.438) - this node is a cross-community bridge._
- **Are the 39 inferred relationships involving `ToolError` (e.g. with `_read_nodes_once()` and `_tap_for_transition()`) actually correct?**
  _`ToolError` has 39 INFERRED edges - model-reasoned connections that need verification._
- **What connects `amazon-android-tool` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Q1FlowTests` be split into smaller, more focused modules?**
  _Cohesion score 0.09098639455782313 - nodes in this community are weakly interconnected._
- **Why does `CloudPhone` connect `CloudPhone` to `screen`, `Q1FlowTests`, `open_adb_shell`, `PostMenuSession`, `_read_nodes`, `open_home_menu`, `test_isolated_reader.py`, `ToolError`, `_prepare_phone`, `Window`, `build_q2_steps`, `AttemptDeadline`, `cli.py`, `time`, `account_flow.py`, `RunJob`, `_type_field`, `desktop.py`, `.test_transition_keeps_observing_after_short_wait_without_tapping`, `swarmote_desktop.py`, `runner.py`, `_nodes`, `CloudBridgeTests`, `CountryRecoveryTests`?**
  _High betweenness centrality (0.088) - this node is a cross-community bridge._
- **Are the 66 inferred relationships involving `CloudPhone` (e.g. with `build_common_steps()` and `_country_full_row()`) actually correct?**
  _`CloudPhone` has 66 INFERRED edges - model-reasoned connections that need verification._
- **Should `bulk_input.py` be split into smaller, more focused modules?**
  _Cohesion score 0.0576271186440678 - nodes in this community are weakly interconnected._