# Graph Report - boom4may  (2026-11-27)

## Corpus Check
- 134 files · ~167,358 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 1, .bat 1, .pyw 1)

## Summary
- 2184 nodes · 7604 edges · 86 communities (74 shown, 12 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 1091 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `0b3d34e9`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- registration.py
- build_common_steps
- otp.py
- BulkInputTests
- windows_identity.py
- swarmote_desktop.py
- RunnerTests
- PostMenuStep
- ToolError
- AddressDetailTests
- 003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật
- Danh mục từng bước đã biết — 13/11/2026
- build_random_steps
- StopResetTests
- cloud.py
- amazon-android-tool
- Ảnh hướng dẫn q1/q2 và menu chung lưu cục bộ
- core.py
- MarketplaceFlowTests
- marketplace_flow.py
- _read_nodes
- MENU_ROUTING.md
- Q3Q4FlowTests
- _type_field
- ExtendedRecoveryTests
- Nghiên cứu và tích hợp Swarmote
- q7_state_machine.py
- ExtendedRecoveryTests
- amazon_is_foreground
- RegistrationState
- PROJECT_INDEX.md
- build_random_steps
- core.py
- vision.py
- AppSettings
- _visible
- time
- ._run
- build_create_address_steps
- File dự án mà Graphify không phân tích trực tiếp
- ProxyConfig
- Bàn giao trạng thái dự án — 13/11/2026
- random_prefix.py
- FakeControl
- VisionFieldTests
- ui_backend.py
- ToolError
- ProxyConfig
- ToolError
- ProfileManagerWindowError
- b1–b11 Reliability and Latency Implementation Plan
- runner.py
- Danh mục ảnh nằm trong dự án
- test_q1_flow.py
- Amazon Android Tool — Giai đoạn A/B
- profile_status
- _CombinedStop
- Giao diện vận hành
- ._launch
- Amazon trên Swarmote
- CloudPhone
- build_reload_payment_steps
- Bộ cài chia sẻ Windows x64
- CountryRecoveryTests
- test_isolated_reader.py
- VERIFICATION.md
- _recognize
- Bàn giao dừng theo yêu cầu người dùng — 13/11/2026
- run_batch
- 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng
- PROJECT_HANDOFF.md
- .test_transition_keeps_observing_after_short_wait_without_tapping
- _new_prefix
- ProfilesNavigationTests
- screen
- .__init__
- AccountData
- 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng
- build_post_auth_steps
- RunJob
- OTP_DESIGN.md
- ensure_manager_ready
- build_post_auth_steps
- ._apply_bulk_text
- GRAPH_AUDIT.md

## God Nodes (most connected - your core abstractions)
1. `ToolError` - 354 edges
2. `CloudPhone` - 234 edges
3. `AttemptDeadline` - 202 edges
4. `RunJob` - 164 edges
5. `RegistrationState` - 162 edges
6. `build_common_steps()` - 115 edges
7. `Window` - 99 edges
8. `PostMenuStep` - 93 edges
9. `Q1FlowTests` - 92 edges
10. `PostMenuSession` - 81 edges

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

## Communities (86 total, 12 thin omitted)

### Community 0 - "registration.py"
Cohesion: 0.21
Nodes (11): _field_for_label(), fill_identifier(), fill_signup_form(), _nodes(), open_entry(), status(), _tap(), _type_into() (+3 more)

### Community 1 - "build_common_steps"
Cohesion: 0.05
Nodes (6): build_common_steps(), node(), Q1FlowTests, read(), provider_read(), read()

### Community 2 - "otp.py"
Cohesion: 0.11
Nodes (8): extract_otp(), _NoRedirect, otp_token(), read_otp(), _read_otp_in_browser(), validate_otp_url(), wait_for_new_otp(), OtpTests

### Community 3 - "BulkInputTests"
Cohesion: 0.07
Nodes (8): BatchDraft, BulkRecord, parse_bulk_payload(), parse_column(), parse_records(), Dán bảng Amazon có ghi chú thẻ live và URL OTP escaped — 14/11/2026, BatchDraftTests, BulkInputTests

### Community 4 - "windows_identity.py"
Cohesion: 0.21
Nodes (6): create_shortcut(), relaunch_command(), runtime(), set_process_identity(), set_window_identity(), WindowsIdentityTests

### Community 5 - "swarmote_desktop.py"
Cohesion: 0.11
Nodes (22): ready_for_home_menu(), _check_stop(), collapse_apps_panel(), install_amazon(), open_adb_shell(), _pause(), _phone_window(), _progress_reporter() (+14 more)

### Community 6 - "RunnerTests"
Cohesion: 0.05
Nodes (19): ProfileRegistry, absent(), ProfileRegistryTests, lookup(), broken(), RunnerTests, create(), resume() (+11 more)

### Community 7 - "PostMenuStep"
Cohesion: 0.07
Nodes (15): resume_common_index(), PostMenuSession, PostMenuStep, PostMenuTests, first_step(), reconcile(), first(), ResumeRegistrationStateTests (+7 more)

### Community 8 - "ToolError"
Cohesion: 0.10
Nodes (8): ProfileStartNotSubmitted, start_profile(), BatchStartTests, checkbox(), toggle(), descendants(), FakeBox, FakeButton

### Community 9 - "AddressDetailTests"
Cohesion: 0.12
Nodes (7): build_create_address_detail_steps(), AddressDetailTests, read(), adb(), tap(), read(), item()

### Community 10 - "003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật"
Cohesion: 0.08
Nodes (20): 003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật, Các bước, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Quy trình đích, Rủi ro và bảo trì, Điều kiện dừng (+12 more)

### Community 11 - "Danh mục từng bước đã biết — 13/11/2026"
Cohesion: 0.06
Nodes (35): Bản thử q7 State Machine — 14/11/2026, Chung b10 — Chuyển WhatsApp sang SMS, Chung b11 — Lấy và gõ OTP SMS, Chung b11a — Chạm ô OTP trên màn SMS, Chung b11b — Xác minh đăng nhập hoặc bấm Create của luồng tạo, Chung b4 — Sign In từ menu, Chung b4a — Chạm ô SĐT, Chung b5 — Gõ số điện thoại (+27 more)

### Community 12 - "build_random_steps"
Cohesion: 0.06
Nodes (15): build_random_steps(), finish_view(), b1–b3 ngẫu nhiên cho q1–q12 — 14/11/2026, Cách thử bản pilot cũ (không áp dụng cho factory hiện hành), Giai đoạn 2 — bản thử State Machine riêng q7, Giới hạn, Phạm vi và quan hệ với luồng cũ, Sơ đồ (+7 more)

### Community 16 - "Ảnh hướng dẫn q1/q2 và menu chung lưu cục bộ"
Cohesion: 0.07
Nodes (28): B16–b22 chung — Đổi marketplace sang United States (18/11/2026), B32–b39 — Reload Balance, thêm thẻ và địa chỉ thanh toán (21/11/2026), B6 — Hai ảnh đính kèm mới ngày 13/11/2026, Menu chung ảnh 01 — Danh sách chữ, Menu chung ảnh 02 — App Store bên phải sau khi Amazon mở, q1 b6 — US +1 hiện nhưng chạm không đóng hộp, 14/11/2026, q1 ảnh 01 — Menu và ba thẻ, q1 ảnh 02 — Sign In cuối menu (+20 more)

### Community 17 - "core.py"
Cohesion: 0.10
Nodes (12): _confirm_menu_fallback(), _menu_evidence(), MenuReadUnavailable, _nodes(), budget(), open_home_menu(), Lỗi chạy song song q3 Terminal trùng / q1 chưa thấy menu — 14/11/2026, HomeMenuTests (+4 more)

### Community 18 - "MarketplaceFlowTests"
Cohesion: 0.07
Nodes (23): AttemptDeadline, MarketplaceFlowTests, read(), adb(), read(), tap(), read(), read() (+15 more)

### Community 19 - "marketplace_flow.py"
Cohesion: 0.19
Nodes (25): _account_tab(), build_marketplace_steps(), run(), account_target(), back_and_read_text(), foreground_ready(), recover_country_list(), _destination() (+17 more)

### Community 20 - "_read_nodes"
Cohesion: 0.15
Nodes (26): _at_or_after(), sign_in(), _country_nodes(), _CountryReadStop, _ensure_menu(), _find_scrolling(), home_visible(), _read_nodes() (+18 more)

### Community 21 - "MENU_ROUTING.md"
Cohesion: 0.23
Nodes (7): Bằng chứng và phạm vi, Kiểm chứng, Quy tắc chạy, Điều hướng hai dạng menu ba gạch, Luồng q1 từ menu ba gạch tới nhập OTP, Thử trên q1 đã có, Luồng q2 từ menu ba gạch

### Community 22 - "Q3Q4FlowTests"
Cohesion: 0.21
Nodes (3): build_q3_steps(), build_q4_steps(), Q3Q4FlowTests

### Community 23 - "_type_field"
Cohesion: 0.18
Nodes (5): _tap_input(), _type_field(), Phục hồi khi ô nhập chưa nhận focus ở b4–b11 — 14/11/2026, FlowRecoveryTests, form()

### Community 24 - "ExtendedRecoveryTests"
Cohesion: 0.13
Nodes (5): arrange_on_open(), _row_if_fits(), _sort_key(), _tiles(), PhoneWindowLayoutTests

### Community 25 - "Nghiên cứu và tích hợp Swarmote"
Cohesion: 0.40
Nodes (4): Hành vi có bằng chứng, Kiểm thử còn lại, Nghiên cứu và tích hợp Swarmote, Phần đã áp dụng

### Community 26 - "q7_state_machine.py"
Cohesion: 0.09
Nodes (18): ActionValidator, _already_reached_result(), _browse_ready_after_sms(), build_q7_pilot_steps(), run(), _past_known_step(), RecoveryHandler, ResultVerifier (+10 more)

### Community 27 - "ExtendedRecoveryTests"
Cohesion: 0.29
Nodes (3): _start_and_confirm(), ExtendedRecoveryTests, fail()

### Community 28 - "amazon_is_foreground"
Cohesion: 0.09
Nodes (10): CloudPhone, prop(), reconcile(), route(), type_characters(), CloudBridgeTests, adb(), step() (+2 more)

### Community 30 - "RegistrationState"
Cohesion: 0.07
Nodes (8): RegistrationState, build_tail_steps(), _choose_tail_target(), _TailChoicesExhausted, RandomPrefixTests, continuation(), choose(), choose()

### Community 31 - "PROJECT_INDEX.md"
Cohesion: 0.19
Nodes (6): Quy trình Swarmote hiện tại, Bản đồ repository, q3 — b1–b3 và nối luồng chung, q4 — Giỏ hàng, Pets, Home and DIY, q5 — ba thẻ riêng và b4–b11 chung, q6 — Trang chủ, Giỏ hàng, menu và một thẻ

### Community 32 - "build_random_steps"
Cohesion: 0.11
Nodes (4): RandomPrefixTests, adb(), adb(), adb()

### Community 33 - "core.py"
Cohesion: 0.09
Nodes (41): main(), parser(), report(), cloud_serials(), scan(), adb(), app_data_dir(), available_memory_mb() (+33 more)

### Community 34 - "vision.py"
Cohesion: 0.12
Nodes (10): _bounds(), _canonical_text(), _compact(), _field_contents(), _field_is_blank(), _join_wrapped_categories(), _normalize(), ocr_nodes() (+2 more)

### Community 35 - "AppSettings"
Cohesion: 0.15
Nodes (8): browser_launch_options(), default_path(), AppSettings, load_settings(), save_settings(), settings_path(), PackagedBrowserTests, SettingsTests

### Community 36 - "_visible"
Cohesion: 0.14
Nodes (34): _bounds(), _resume_address_payment_index(), _text(), _visible(), reported_installer(), _action(), _address_form(), _addresses() (+26 more)

### Community 37 - "time"
Cohesion: 0.11
Nodes (16): main(), main(), main(), check_runtime(), main(), verify(), _app_installed(), _app_paths() (+8 more)

### Community 38 - "._run"
Cohesion: 0.18
Nodes (8): emit(), 002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ, Các bước, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Rủi ro và bảo trì, Điều kiện dừng

### Community 39 - "build_create_address_steps"
Cohesion: 0.24
Nodes (4): build_create_address_steps(), CreateAddressFlowTests, read(), node()

### Community 40 - "File dự án mà Graphify không phân tích trực tiếp"
Cohesion: 0.40
Nodes (5): File dự án mà Graphify không phân tích trực tiếp, .gitignore, Launch Swarmote Tool.pyw, pyproject.toml, Ảnh PNG trong dự án

### Community 41 - "ProxyConfig"
Cohesion: 0.17
Nodes (8): BatchItem, parse_proxy_line(), prepare_five(), create_profile(), ProxyConfig, ready_for_registration(), BatchSafetyTests, CreationWindowVisibilityTests

### Community 42 - "Bàn giao trạng thái dự án — 13/11/2026"
Cohesion: 0.09
Nodes (18): save(), set_tk_icon(), B6 danh sách quốc gia vẫn mở sau khi chọn — 13/11/2026, Bàn giao trạng thái dự án — 13/11/2026, Bản chính boom4may và bản dự phòng — 14/11/2026, Bộ cài offline chia sẻ — 14/11/2026, Cài đặt máy mới, Dừng riêng máy đang chọn — 14/11/2026 (+10 more)

### Community 43 - "random_prefix.py"
Cohesion: 0.11
Nodes (17): scroll_view(), wait_until(), RecoverableStepError, build_random_steps(), browse(), action(), run_browse(), finish_view() (+9 more)

### Community 44 - "FakeControl"
Cohesion: 0.13
Nodes (5): ParallelInstallTests, PhoneWindow, FakeControl, InstallTests, descendants()

### Community 45 - "VisionFieldTests"
Cohesion: 0.24
Nodes (3): _input_box(), detection(), VisionFieldTests

### Community 46 - "ui_backend.py"
Cohesion: 0.13
Nodes (11): swarmote_adb_path(), swarmote_tunnel_owner(), _connect(), country_reverse_points(), country_scroll(), _failed(), read_tree(), ready() (+3 more)

### Community 47 - "ToolError"
Cohesion: 0.17
Nodes (21): _country_full_row(), _keyboard_visible(), _tap(), cloud_adb(), _foreground(), _read_text_region(), _scroll_country(), _size() (+13 more)

### Community 48 - "ProxyConfig"
Cohesion: 0.09
Nodes (8): lines(), _proxy_rows(), _table_cells(), _url_from_cell(), validate_card(), _automatic_resume_slots(), Dán nhiều proxy cách nhau bằng dấu cách — 14/11/2026, Value

### Community 49 - "ToolError"
Cohesion: 0.09
Nodes (33): open_amazon(), foreground(), package_path(), probe(), require_online(), ToolError, _tap(), _activate_manager() (+25 more)

### Community 50 - "ProfileManagerWindowError"
Cohesion: 0.12
Nodes (19): _ActionNotResolved, _button(), _form_action(), _parse_ui_nodes(), _read_hierarchy(), _read_login_sms_visual(), _read_nodes_once(), _read_visual_nodes() (+11 more)

### Community 51 - "b1–b11 Reliability and Latency Implementation Plan"
Cohesion: 0.18
Nodes (10): b1–b11 Reliability and Latency Implementation Plan, Completion Criteria, File Map, Global Constraints, Review Focus, Task 1: Measure current step latency and classify existing failures, Task 2: Define safe retry, reconcile, pause, and stop behavior, Task 3: Reduce redundant UI reads and unnecessary waits (+2 more)

### Community 52 - "runner.py"
Cohesion: 0.16
Nodes (6): ProfileCreateNotSubmitted, ProfileManagerWindowError, ProfileNotFound, ProxyTestFailed, unavailable(), Nút New Profile trên Swarmote — 13/11/2026

### Community 53 - "Danh mục ảnh nằm trong dự án"
Cohesion: 0.22
Nodes (9): amazon_android/assets/obsidian_prism.png, amazon_android/assets/swarmote_tool_square.png và swarmote_tool.ico, assets/ui_history/machine7_input_before.png, assets/ui_history/reset_check.png, assets/ui_history/ui-12.png, assets/ui_history/ui_palette_preview.png, assets/ui_history/ui-preview.png, assets/ui_history/ui-screenshot.png (+1 more)

### Community 54 - "test_q1_flow.py"
Cohesion: 0.11
Nodes (10): menu_layout(), _national_phone(), route_list_menu(), _ScreenWaitExpired, build_q1_steps(), category(), build_q5_steps(), Cách xử lý ảnh tiếp theo (+2 more)

### Community 55 - "Amazon Android Tool — Giai đoạn A/B"
Cohesion: 0.29
Nodes (7): Amazon Android Tool — Giai đoạn A/B, Cài trên máy Windows mới, Dán nhiều proxy, Sử dụng, Trạng thái nghiệm thu, Yêu cầu, Điện thoại đám mây Swarmote

### Community 56 - "profile_status"
Cohesion: 0.48
Nodes (3): _proxy_postal_prefix(), controls(), ProxyPostalPrefixTests

### Community 58 - "Giao diện vận hành"
Cohesion: 0.40
Nodes (4): Bố cục, Giao diện vận hành, Hướng thị giác, Quy tắc

### Community 60 - "Amazon trên Swarmote"
Cohesion: 0.33
Nodes (5): Amazon trên Swarmote, Người dùng và công việc, Nền tảng, Điều chưa xác minh, Định hướng ngôn ngữ nếu xây dựng lại — 23/11/2026

### Community 61 - "CloudPhone"
Cohesion: 0.08
Nodes (24): b6 Country US +1 — 14/11/2026, B6 cuộn quốc gia và chọn lại — 13/11/2026, Biên bản kiểm tra thực tế — 2026-11-12, Cài và đo UiAutomator2 theo phê duyệt mới — 13/11/2026, Dừng riêng một máy — 14/11/2026, Focus ô nhập b4–b11 — 14/11/2026, Ghim taskbar — 13/11/2026, Giao diện sáng, dễ đọc — 2026-11-13 (+16 more)

### Community 62 - "build_reload_payment_steps"
Cohesion: 0.13
Nodes (9): build_reload_payment_steps(), node(), ReloadPaymentTests, adb(), wait(), read(), read(), read() (+1 more)

### Community 63 - "Bộ cài chia sẻ Windows x64"
Cohesion: 0.50
Nodes (3): Bộ cài chia sẻ Windows x64, Dựng lại, Nguồn thành phần

### Community 64 - "CountryRecoveryTests"
Cohesion: 0.27
Nodes (4): CountryRecoveryTests, read(), wait(), node()

### Community 65 - "test_isolated_reader.py"
Cohesion: 0.20
Nodes (8): phone_reader(), PhoneReader, ReaderResponseError, _serve(), fake_worker(), IsolationTests, duplicate(), production_worker_with_fake_android()

### Community 66 - "VERIFICATION.md"
Cohesion: 0.17
Nodes (10): Kết luận và tích hợp, Kết quả thực tế, So sánh bộ đọc trên q1 — 13/11/2026, Thành phần thiết bị, b1–b3 bắt buộc có ba cú bấm — 14/11/2026, b1–b3 ngẫu nhiên cho 12 máy — 14/11/2026, b1–b3 ngẫu nhiên trên 12 máy, không dùng OCR — 14/11/2026, b6 cuộn tới đáy rồi vuốt ngược — 14/11/2026 (+2 more)

### Community 67 - "_recognize"
Cohesion: 0.21
Nodes (6): _engine(), _recognize(), check(), ParallelOcrTests, engine(), read()

### Community 68 - "Bàn giao dừng theo yêu cầu người dùng — 13/11/2026"
Cohesion: 0.25
Nodes (7): Bàn giao dừng theo yêu cầu người dùng — 13/11/2026, Bằng chứng trực tiếp đã có, Bối cảnh đã hoàn tất trước lỗi hiện tại, Cách tiếp tục, Kiểm chứng gần nhất, Lỗi chính chưa xử lý xong, Yêu cầu mới nhất

### Community 69 - "run_batch"
Cohesion: 0.11
Nodes (17): _phone_preparation_lock(), _prepare_phone(), _prepare_phone_locked(), progress(), stop_here(), retry_preparation(), run_batch(), fill_slots() (+9 more)

### Community 70 - "001 — Tách dữ liệu từng mẻ và đối chiếu số hàng"
Cohesion: 0.29
Nodes (7): 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Rủi ro và bảo trì, Thiết kế yêu cầu, Điều kiện dừng

### Community 71 - "PROJECT_HANDOFF.md"
Cohesion: 0.14
Nodes (13): B4–b11 chạy đồng thời và OCR — 14/11/2026, b6 US +1 còn mở sau bốn cú chạm — 14/11/2026, Bản thử State Machine q7 và b1–b3 mở mục con — 14/11/2026, Bỏ thời hạn tổng sau menu — 14/11/2026, Bổ sung đọc ảnh OCR và chạm trực tiếp dự phòng cho b26 khi uiautomator dump WebView lỗi — 19/11/2026, Cơ chế chụp ảnh OCR quét chữ ấn luôn cho toàn bộ b26–b31 — 19/11/2026, Không bỏ qua b1–b3 ngẫu nhiên; 14 ảnh menu mới — 14/11/2026, Phạm vi q1–q12 sau phản hồi người dùng — 14/11/2026 (+5 more)

### Community 74 - "ProfilesNavigationTests"
Cohesion: 0.16
Nodes (6): control(), ProfilesNavigationTests, descendants(), invoke(), descendants(), descendants()

### Community 75 - "screen"
Cohesion: 0.14
Nodes (25): confirmed_login_otp_nodes(), continue_number(), country(), enter_otp(), finish_auto(), finish_create(), finish_login(), focus_otp() (+17 more)

### Community 76 - ".__init__"
Cohesion: 0.23
Nodes (3): _crystal_art(), _edge_light(), Ô Amazon riêng Máy 1–12 dễ thấy hơn — 14/11/2026

### Community 81 - "build_post_auth_steps"
Cohesion: 0.11
Nodes (16): _scroll_up(), amazon_is_foreground(), browse(), open_menu(), read_menu(), return_to_menu(), view(), visit() (+8 more)

### Community 83 - "RunJob"
Cohesion: 0.13
Nodes (8): AccountData, RunJob, DesktopResumeTests, apartment_type(), PreparationThreadsTests, run(), install(), Q5FlowTests

### Community 84 - "OTP_DESIGN.md"
Cohesion: 0.50
Nodes (3): Nối vào bước tạo tài khoản sau khi xác minh màn hình Amazon, Thiết kế OTP cho từng Profile, Đã chuẩn bị

### Community 86 - "build_post_auth_steps"
Cohesion: 0.13
Nodes (9): Hướng dẫn khi tiếp tục dự án, build_post_auth_steps(), Nhận diện giao diện lúc chạy, Nhập liệu và lỗi, Quy tắc tự động hóa sau menu ba gạch, Trạng thái hiện tại của dự án, Từng máy độc lập, Một quy luật để sửa mã về sau — 20/11/2026 (+1 more)

### Community 92 - "GRAPH_AUDIT.md"
Cohesion: 0.50
Nodes (3): Cách kiểm tra sau mỗi sửa đổi, Giới hạn đã xác nhận, Kiểm tra độ phủ Graphify — cập nhật 26/11/2026

## Knowledge Gaps
- **1 isolated node(s):** `amazon-android-tool`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 538 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ToolError` connect `ToolError` to `registration.py`, `build_common_steps`, `otp.py`, `BulkInputTests`, `swarmote_desktop.py`, `RunnerTests`, `PostMenuStep`, `ToolError`, `AddressDetailTests`, `build_random_steps`, `StopResetTests`, `cloud.py`, `core.py`, `MarketplaceFlowTests`, `marketplace_flow.py`, `_read_nodes`, `_type_field`, `q7_state_machine.py`, `ExtendedRecoveryTests`, `amazon_is_foreground`, `._refresh_devices`, `RegistrationState`, `build_random_steps`, `core.py`, `vision.py`, `AppSettings`, `_visible`, `._run`, `build_create_address_steps`, `ProxyConfig`, `random_prefix.py`, `ui_backend.py`, `ToolError`, `ProxyConfig`, `ProfileManagerWindowError`, `runner.py`, `test_q1_flow.py`, `._launch`, `build_reload_payment_steps`, `CountryRecoveryTests`, `test_isolated_reader.py`, `_recognize`, `run_batch`, `_new_prefix`, `ProfilesNavigationTests`, `screen`, `001 — Tách dữ liệu từng mẻ và đối chiếu số hàng`, `build_post_auth_steps`, `RunJob`, `ensure_manager_ready`, `._apply_bulk_text`?**
  _High betweenness centrality (0.379) - this node is a cross-community bridge._
- **Are the 58 inferred relationships involving `ToolError` (e.g. with `_read_nodes_once()` and `_resume_address_payment_index()`) actually correct?**
  _`ToolError` has 58 INFERRED edges - model-reasoned connections that need verification._
- **What connects `amazon-android-tool` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `build_common_steps` be split into smaller, more focused modules?**
  _Cohesion score 0.05292702485966319 - nodes in this community are weakly interconnected._
- **Why does `CloudPhone` connect `amazon_is_foreground` to `registration.py`, `build_common_steps`, `swarmote_desktop.py`, `PostMenuStep`, `AddressDetailTests`, `build_random_steps`, `cloud.py`, `core.py`, `MarketplaceFlowTests`, `_read_nodes`, `Q3Q4FlowTests`, `_type_field`, `q7_state_machine.py`, `ExtendedRecoveryTests`, `RegistrationState`, `build_random_steps`, `core.py`, `AppSettings`, `_visible`, `build_create_address_steps`, `ProxyConfig`, `random_prefix.py`, `ui_backend.py`, `ToolError`, `ProxyConfig`, `ToolError`, `ProfileManagerWindowError`, `runner.py`, `test_q1_flow.py`, `._launch`, `build_reload_payment_steps`, `CountryRecoveryTests`, `test_isolated_reader.py`, `run_batch`, `.test_transition_keeps_observing_after_short_wait_without_tapping`, `screen`, `AccountData`, `001 — Tách dữ liệu từng mẻ và đối chiếu số hàng`, `build_post_auth_steps`, `RunJob`, `build_post_auth_steps`?**
  _High betweenness centrality (0.113) - this node is a cross-community bridge._
- **Are the 88 inferred relationships involving `CloudPhone` (e.g. with `build_common_steps()` and `_country_full_row()`) actually correct?**
  _`CloudPhone` has 88 INFERRED edges - model-reasoned connections that need verification._
- **Should `otp.py` be split into smaller, more focused modules?**
  _Cohesion score 0.11330049261083744 - nodes in this community are weakly interconnected._