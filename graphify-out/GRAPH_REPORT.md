# Graph Report - boom4may  (2026-11-14)

## Corpus Check
- 117 files · ~91,777 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 1, .bat 1, .pyw 1)

## Summary
- 1445 nodes · 4741 edges · 72 communities (59 shown, 13 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 674 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `699de059`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- cli.py
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
- core.py
- screen
- _nodes
- amazon-android-tool
- Ảnh hướng dẫn q1/q2 và menu chung lưu cục bộ
- Biên bản kiểm tra thực tế — 2026-11-12
- ensure_manager_ready
- windows_identity.py
- _type_field
- subprocess
- registration.py
- RegistrationState
- StopResetTests
- Nghiên cứu và tích hợp Swarmote
- Q3Q4FlowTests
- AttemptDeadline
- vision.py
- setup.py
- ._launch
- pathlib
- _ensure_menu
- desktop.py
- open_home_menu
- RecoverableStepError
- SafetyTests
- profile_status
- ToolError
- Điều hướng hai dạng menu ba gạch
- time
- Bàn giao trạng thái dự án — 13/11/2026
- CloudPhone
- FakeControl
- ResumeRegistrationStateTests
- PROJECT_HANDOFF.md
- BatchDraft
- build_q2_steps
- CountryRecoveryTests
- Window
- b1–b11 Reliability and Latency Implementation Plan
- Bàn giao dừng theo yêu cầu người dùng — 13/11/2026
- Danh mục ảnh nằm trong dự án
- 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng
- Amazon Android Tool — Giai đoạn A/B
- run_batch
- OTP_DESIGN.md
- Giao diện vận hành
- Quy tắc tự động hóa sau menu ba gạch
- Amazon trên Swarmote
- _crystal_art
- PLAN.md
- Bộ cài chia sẻ Windows x64
- Luồng q1 từ menu ba gạch tới nhập OTP
- Kiểm tra độ phủ Graphify — 13/11/2026
- Q5_FLOW.md
- PreparationThreadsTests
- ._poll
- .test_menu_read_failure_is_retried_without_new_tap
- VERIFICATION.md
- SharedFallbackTests

## God Nodes (most connected - your core abstractions)
1. `ToolError` - 254 edges
2. `CloudPhone` - 168 edges
3. `RunJob` - 102 edges
4. `AttemptDeadline` - 93 edges
5. `Window` - 82 edges
6. `build_common_steps()` - 79 edges
7. `_read_nodes()` - 54 edges
8. `Q1FlowTests` - 51 edges
9. `PostMenuSession` - 49 edges
10. `PostMenuStep` - 48 edges

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

## Communities (72 total, 13 thin omitted)

### Community 0 - "cli.py"
Cohesion: 0.17
Nodes (10): BatchItem, parse_proxy_line(), prepare_five(), main(), parser(), report(), get_device(), print_json() (+2 more)

### Community 1 - "Q1FlowTests"
Cohesion: 0.09
Nodes (7): build_common_steps(), build_q1_steps(), category(), Đã có trong graph, node(), Q1FlowTests, provider_read()

### Community 2 - "otp.py"
Cohesion: 0.10
Nodes (8): browser_launch_options(), extract_otp(), _NoRedirect, read_otp(), _read_otp_in_browser(), wait_for_new_otp(), OtpTests, PackagedBrowserTests

### Community 3 - "parse_records"
Cohesion: 0.09
Nodes (11): BulkRecord, lines(), parse_column(), parse_records(), _proxy_rows(), _table_cells(), _url_from_cell(), validate_card() (+3 more)

### Community 4 - "account_flow.py"
Cohesion: 0.13
Nodes (21): _ActionNotResolved, _bounds(), _button(), _country_full_row(), _form_action(), _has(), _keyboard_visible(), menu_layout() (+13 more)

### Community 5 - "_prepare_phone"
Cohesion: 0.12
Nodes (22): open_amazon(), ready_for_home_menu(), _prepare_phone(), progress(), _check_stop(), collapse_apps_panel(), install_amazon(), collect() (+14 more)

### Community 6 - "RunnerTests"
Cohesion: 0.06
Nodes (20): ProfileRegistry, ProfileLookupError, ProfileNotFound, Thiết kế yêu cầu, absent(), ProfileRegistryTests, lookup(), broken() (+12 more)

### Community 7 - "PostMenuSession"
Cohesion: 0.17
Nodes (9): PostMenuSession, PostMenuStep, RunJob, PostMenuTests, first_step(), reconcile(), first(), SharedStepRecoveryTests (+1 more)

### Community 8 - ".test_only_confirmed_target_names_are_selected_for_one_start_command"
Cohesion: 0.10
Nodes (8): ProfileStartNotSubmitted, start_profile(), BatchStartTests, checkbox(), toggle(), descendants(), FakeBox, FakeButton

### Community 9 - "PROJECT_INDEX.md"
Cohesion: 0.22
Nodes (6): Hướng dẫn khi tiếp tục dự án, Bản đồ repository, Luồng q2 từ menu ba gạch, q3 — b1–b3 và nối luồng chung, q4 — Giỏ hàng, Pets, Home and DIY, q6 — Trang chủ, Giỏ hàng, menu và một thẻ

### Community 10 - "002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ"
Cohesion: 0.07
Nodes (25): 002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ, Kiểm tra bắt buộc, Phạm vi, Rủi ro và bảo trì, Điều kiện dừng, 003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật, Các bước, Kiểm tra bắt buộc (+17 more)

### Community 11 - "Danh mục từng bước đã biết — 13/11/2026"
Cohesion: 0.06
Nodes (35): B1–B3 hiện hành — Ba lượt ngẫu nhiên q1–q12, Chung b10 — Chuyển WhatsApp sang SMS, Chung b11 — Lấy và gõ OTP SMS, Chung b11a — Chạm ô OTP trên màn SMS, Chung b11b — Bấm Create your Amazon account, Chung b4 — Sign In từ menu, Chung b4a — Chạm ô SĐT, Chung b5 — Gõ số điện thoại (+27 more)

### Community 12 - "core.py"
Cohesion: 0.28
Nodes (19): adb(), available_memory_mb(), check_play(), configure_avd(), connected_devices(), Device, device_avd_name(), device_resources() (+11 more)

### Community 13 - "screen"
Cohesion: 0.20
Nodes (19): continue_number(), create_account(), enter_otp(), focus_otp(), focus_phone(), name(), phone_number(), proceed() (+11 more)

### Community 14 - "_nodes"
Cohesion: 0.24
Nodes (4): MenuReadUnavailable, _nodes(), budget(), HomeMenuTests

### Community 16 - "Ảnh hướng dẫn q1/q2 và menu chung lưu cục bộ"
Cohesion: 0.08
Nodes (26): 14 ảnh menu chung b1–b3 ngẫu nhiên — 14/11/2026, B6 — Hai ảnh đính kèm mới ngày 13/11/2026, Menu chung ảnh 01 — Danh sách chữ, Menu chung ảnh 02 — App Store bên phải sau khi Amazon mở, q1 b6 — US +1 hiện nhưng chạm không đóng hộp, 14/11/2026, q1 ảnh 01 — Menu và ba thẻ, q1 ảnh 02 — Sign In cuối menu, q1 ảnh 03 — Nhập số điện thoại (+18 more)

### Community 17 - "Biên bản kiểm tra thực tế — 2026-11-12"
Cohesion: 0.08
Nodes (26): b6 Country US +1 — 14/11/2026, B6 cuộn quốc gia và chọn lại — 13/11/2026, Biên bản kiểm tra thực tế — 2026-11-12, Cài và đo UiAutomator2 theo phê duyệt mới — 13/11/2026, Dừng riêng một máy — 14/11/2026, Focus ô nhập b4–b11 — 14/11/2026, Ghim taskbar — 13/11/2026, Giao diện sáng, dễ đọc — 2026-11-13 (+18 more)

### Community 18 - "ensure_manager_ready"
Cohesion: 0.28
Nodes (4): ensure_manager_ready(), ProfileManagerWindowError, ManagerStartupTests, unavailable()

### Community 19 - "windows_identity.py"
Cohesion: 0.24
Nodes (6): create_shortcut(), relaunch_command(), runtime(), set_process_identity(), set_window_identity(), WindowsIdentityTests

### Community 20 - "_type_field"
Cohesion: 0.22
Nodes (4): _type_field(), Phục hồi khi ô nhập chưa nhận focus ở b4–b11 — 14/11/2026, FlowRecoveryTests, form()

### Community 21 - "subprocess"
Cohesion: 0.18
Nodes (12): main(), check_runtime(), main(), verify(), _app_installed(), _app_paths(), _check_external_apps(), _install_python_dependencies() (+4 more)

### Community 22 - "registration.py"
Cohesion: 0.20
Nodes (12): reconcile(), _field_for_label(), fill_identifier(), fill_signup_form(), _nodes(), open_entry(), status(), _tap() (+4 more)

### Community 23 - "RegistrationState"
Cohesion: 0.20
Nodes (6): build_random_steps(), browse(), RandomPrefixTests, adb(), adb(), adb()

### Community 25 - "Nghiên cứu và tích hợp Swarmote"
Cohesion: 0.40
Nodes (4): Hành vi có bằng chứng, Kiểm thử còn lại, Nghiên cứu và tích hợp Swarmote, Phần đã áp dụng

### Community 26 - "Q3Q4FlowTests"
Cohesion: 0.13
Nodes (7): RegistrationState, category_action(), build_q3_steps(), build_q4_steps(), build_q5_steps(), Q3Q4FlowTests, Q5FlowTests

### Community 27 - "AttemptDeadline"
Cohesion: 0.10
Nodes (8): route_list_menu(), verify_menu_open(), AttemptDeadline, Mã hiện có, ExtendedRecoveryTests, fail(), read(), MenuReturnTests

### Community 28 - "vision.py"
Cohesion: 0.07
Nodes (18): _bounds(), _canonical_text(), _compact(), _engine(), _field_contents(), _field_is_blank(), _input_box(), _join_wrapped_categories() (+10 more)

### Community 29 - "setup.py"
Cohesion: 0.23
Nodes (12): app_data_dir(), avd_names(), create_avd(), doctor(), executable(), installed_image(), run(), sdk_root() (+4 more)

### Community 31 - "pathlib"
Cohesion: 0.23
Nodes (7): save(), default_path(), AppSettings, load_settings(), save_settings(), settings_path(), SettingsTests

### Community 32 - "_ensure_menu"
Cohesion: 0.26
Nodes (18): _at_or_after(), country(), sign_in(), _ensure_menu(), _find_scrolling(), _read_nodes(), _tap_for_transition(), _visible() (+10 more)

### Community 33 - "desktop.py"
Cohesion: 0.12
Nodes (5): _automatic_resume_slots(), AccountData, DesktopResumeTests, Q2FlowTests, on_worker()

### Community 34 - "open_home_menu"
Cohesion: 0.19
Nodes (7): _confirm_menu_fallback(), _menu_evidence(), open_home_menu(), Thu panel Apps sau khi mở Amazon — 14/11/2026, ParallelNavigationRegressionTests, Cập nhật luồng mẻ trước đó — 2026-11-13, q14 mở Amazon lần đầu — 2026-11-13

### Community 35 - "RecoverableStepError"
Cohesion: 0.14
Nodes (9): RecoverableStepError, action(), sign_in(), _first_point(), _menu(), _size(), action(), action() (+1 more)

### Community 37 - "profile_status"
Cohesion: 0.14
Nodes (8): _open_profiles(), ProfileCreateNotSubmitted, ProxyTestFailed, visible_profile_names(), control(), ProfilesNavigationTests, descendants(), descendants()

### Community 38 - "ToolError"
Cohesion: 0.11
Nodes (23): ToolError, _tap(), _activate_manager(), create_profile(), _create_profile_form(), _descendants(), inspect(), check_stop() (+15 more)

### Community 40 - "Điều hướng hai dạng menu ba gạch"
Cohesion: 0.50
Nodes (4): Bằng chứng và phạm vi, Kiểm chứng, Quy tắc chạy, Điều hướng hai dạng menu ba gạch

### Community 41 - "time"
Cohesion: 0.08
Nodes (18): swarmote_tunnel_owner(), phone_reader(), PhoneReader, ReaderResponseError, _serve(), _connect(), country_reverse_points(), country_scroll() (+10 more)

### Community 42 - "Bàn giao trạng thái dự án — 13/11/2026"
Cohesion: 0.07
Nodes (26): main(), main(), B6 danh sách quốc gia vẫn mở sau khi chọn — 13/11/2026, Bàn giao trạng thái dự án — 13/11/2026, Bản chính boom4may và bản dự phòng — 14/11/2026, Bộ cài offline chia sẻ — 14/11/2026, Cài đặt máy mới, Dừng riêng máy đang chọn — 14/11/2026 (+18 more)

### Community 43 - "CloudPhone"
Cohesion: 0.11
Nodes (17): cloud_adb(), cloud_screenshot(), cloud_serials(), CloudPhone, foreground(), package_path(), probe(), prop() (+9 more)

### Community 44 - "FakeControl"
Cohesion: 0.13
Nodes (5): ParallelInstallTests, PhoneWindow, FakeControl, InstallTests, descendants()

### Community 45 - "ResumeRegistrationStateTests"
Cohesion: 0.25
Nodes (3): ResumeRegistrationStateTests, factory(), factory()

### Community 46 - "PROJECT_HANDOFF.md"
Cohesion: 0.12
Nodes (16): b1–b3 ngẫu nhiên cho q1–q12 — 14/11/2026, B1–b3 xem menu ngẫu nhiên cho 12 máy — 14/11/2026, B4–b11 chạy đồng thời và OCR — 14/11/2026, b6 cuộn chạm đáy rồi vuốt ngược khoảng bốn quốc gia — 14/11/2026, b6 US +1 còn mở sau bốn cú chạm — 14/11/2026, Bỏ thời hạn tổng sau menu — 14/11/2026, Dán bảng Amazon có ghi chú thẻ live và URL OTP escaped — 14/11/2026, File chính đã sửa (+8 more)

### Community 48 - "build_q2_steps"
Cohesion: 0.18
Nodes (11): home_visible(), _tap(), _unique(), visit_home(), build_q2_steps(), browse_menu(), home(), Cách xử lý ảnh tiếp theo (+3 more)

### Community 49 - "CountryRecoveryTests"
Cohesion: 0.27
Nodes (4): CountryRecoveryTests, read(), wait(), node()

### Community 50 - "Window"
Cohesion: 0.14
Nodes (3): _edge_light(), Window, PreparationProgressTests

### Community 51 - "b1–b11 Reliability and Latency Implementation Plan"
Cohesion: 0.18
Nodes (10): b1–b11 Reliability and Latency Implementation Plan, Completion Criteria, File Map, Global Constraints, Review Focus, Task 1: Measure current step latency and classify existing failures, Task 2: Define safe retry, reconcile, pause, and stop behavior, Task 3: Reduce redundant UI reads and unnecessary waits (+2 more)

### Community 52 - "Bàn giao dừng theo yêu cầu người dùng — 13/11/2026"
Cohesion: 0.29
Nodes (6): Bàn giao dừng theo yêu cầu người dùng — 13/11/2026, Bối cảnh đã hoàn tất trước lỗi hiện tại, Cách tiếp tục, Kiểm chứng gần nhất, Lỗi chính chưa xử lý xong, Yêu cầu mới nhất

### Community 53 - "Danh mục ảnh nằm trong dự án"
Cohesion: 0.29
Nodes (7): amazon_android/assets/obsidian_prism.png, assets/ui_history/reset_check.png, assets/ui_history/ui-12.png, assets/ui_history/ui_palette_preview.png, assets/ui_history/ui-preview.png, assets/ui_history/ui-screenshot.png, Danh mục ảnh nằm trong dự án

### Community 54 - "001 — Tách dữ liệu từng mẻ và đối chiếu số hàng"
Cohesion: 0.29
Nodes (7): 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Rủi ro và bảo trì, Thiết kế yêu cầu, Điều kiện dừng

### Community 55 - "Amazon Android Tool — Giai đoạn A/B"
Cohesion: 0.29
Nodes (7): Amazon Android Tool — Giai đoạn A/B, Cài trên máy Windows mới, Dán nhiều proxy, Sử dụng, Trạng thái nghiệm thu, Yêu cầu, Điện thoại đám mây Swarmote

### Community 56 - "run_batch"
Cohesion: 0.10
Nodes (16): emit(), pause_if_requested(), stop_here(), run_batch(), fill_slots(), refresh_slots(), requested(), startup_progress() (+8 more)

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

### Community 63 - "Bộ cài chia sẻ Windows x64"
Cohesion: 0.50
Nodes (3): Bộ cài chia sẻ Windows x64, Dựng lại, Nguồn thành phần

### Community 65 - "Kiểm tra độ phủ Graphify — 13/11/2026"
Cohesion: 0.50
Nodes (3): Cách kiểm tra sau mỗi sửa đổi, Giới hạn đã xác nhận, Kiểm tra độ phủ Graphify — 13/11/2026

### Community 67 - "PreparationThreadsTests"
Cohesion: 0.29
Nodes (4): apartment_type(), PreparationThreadsTests, run(), install()

### Community 70 - "VERIFICATION.md"
Cohesion: 0.13
Nodes (13): Kết luận và tích hợp, Kết quả thực tế, So sánh bộ đọc trên q1 — 13/11/2026, Thành phần thiết bị, b1–b3 bắt buộc có ba cú bấm — 14/11/2026, b1–b3 ngẫu nhiên cho 12 máy — 14/11/2026, b1–b3 ngẫu nhiên trên 12 máy, không dùng OCR — 14/11/2026, b6 cuộn tới đáy rồi vuốt ngược — 14/11/2026 (+5 more)

## Knowledge Gaps
- **1 isolated node(s):** `amazon-android-tool`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 392 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **13 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ToolError` connect `ToolError` to `cli.py`, `Q1FlowTests`, `otp.py`, `parse_records`, `account_flow.py`, `_prepare_phone`, `RunnerTests`, `PostMenuSession`, `.test_only_confirmed_target_names_are_selected_for_one_start_command`, `core.py`, `screen`, `_nodes`, `ensure_manager_ready`, `_type_field`, `registration.py`, `RegistrationState`, `StopResetTests`, `Q3Q4FlowTests`, `AttemptDeadline`, `vision.py`, `setup.py`, `._launch`, `pathlib`, `_ensure_menu`, `desktop.py`, `open_home_menu`, `RecoverableStepError`, `profile_status`, `unittest`, `time`, `CloudPhone`, `BatchDraft`, `build_q2_steps`, `CountryRecoveryTests`, `Window`, `run_batch`?**
  _High betweenness centrality (0.378) - this node is a cross-community bridge._
- **Are the 42 inferred relationships involving `ToolError` (e.g. with `_read_nodes_once()` and `_tap_for_transition()`) actually correct?**
  _`ToolError` has 42 INFERRED edges - model-reasoned connections that need verification._
- **What connects `amazon-android-tool` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Q1FlowTests` be split into smaller, more focused modules?**
  _Cohesion score 0.09098639455782313 - nodes in this community are weakly interconnected._
- **Why does `CloudPhone` connect `CloudPhone` to `cli.py`, `Q1FlowTests`, `account_flow.py`, `_prepare_phone`, `PostMenuSession`, `screen`, `_nodes`, `_type_field`, `registration.py`, `RegistrationState`, `Q3Q4FlowTests`, `AttemptDeadline`, `_ensure_menu`, `desktop.py`, `open_home_menu`, `RecoverableStepError`, `ToolError`, `unittest`, `time`, `ResumeRegistrationStateTests`, `build_q2_steps`, `CountryRecoveryTests`, `Window`, `run_batch`, `._poll`, `.test_menu_read_failure_is_retried_without_new_tap`, `SharedFallbackTests`?**
  _High betweenness centrality (0.121) - this node is a cross-community bridge._
- **Are the 70 inferred relationships involving `CloudPhone` (e.g. with `build_common_steps()` and `_country_full_row()`) actually correct?**
  _`CloudPhone` has 70 INFERRED edges - model-reasoned connections that need verification._
- **Should `otp.py` be split into smaller, more focused modules?**
  _Cohesion score 0.1010752688172043 - nodes in this community are weakly interconnected._