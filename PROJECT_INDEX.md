> Bản đồ file và quy tắc tìm chỗ sửa nằm ở đây. Hành vi hiện hành của từng bước nằm trong [STEP_INVENTORY.md](STEP_INVENTORY.md); trạng thái chạy thật, lần sửa và mức xác minh nằm trong [PROJECT_HANDOFF.md](PROJECT_HANDOFF.md) và [VERIFICATION.md](VERIFICATION.md). Đoạn ghi ngày cũ là lịch sử, không được dùng thay cho mã đang chạy và ảnh màn hiện tại.

# Bản đồ repository

## Một quy luật để sửa mã về sau — 20/11/2026

Luồng Tạo/Đăng nhập bắt đầu ở `desktop.POST_MENU_STEP_FACTORIES`: từ 26/11/2026, cả 12 slot đều dùng `random_prefix.build_random_steps`, kể cả Máy 7. Lựa chọn Settings “Đổi US từ đầu” đi qua P01–P08 rồi chạy `change_us_flow.build_change_us_steps` b1–b17 riêng từng máy, không gọi factory ngẫu nhiên. Các bước sau xác minh của luồng Tạo/Đăng nhập được nối một lần qua `random_prefix.build_post_auth_steps`. `PostMenuSession` giữ trạng thái đúng máy. Tên bước có hậu tố như b4a, b11a, b11b là bước thật trong danh sách, không suy ra chỉ số bằng số b.

| Mốc | File sở hữu hành vi | Trạng thái/điều kiện chuyển bước | Test cần xem |
| --- | --- | --- | --- |
| P01–P08, mở Amazon/menu | `desktop.py`, `bulk_input.py`, `proxy_reserve.py`, `runner.py`, `swarmote_desktop.py`, `home_menu.py`; `phone_window_layout.py` chỉ xếp cửa sổ Windows khi tìm thấy viewer mới | `BatchDraft` và trạng thái chuẩn bị trong `runner.py`; pool proxy dự phòng ở RAM qua Mẻ mới, chỉ cấp khi Test Proxy lỗi trước Create; khi Profile chưa tạo và máy lỗi, sửa dữ liệu riêng tại `desktop.py` rồi Tiếp tục bằng `RunJob` mới của đúng hàng | `test_bulk_input.py`, `test_proxy_reserve.py`, `test_stop_reset.py`, `test_runner.py`, `test_home_menu.py`, `test_swarmote_waits.py`, `test_phone_window_layout.py` |
| b1–b17 “Đổi US từ đầu” | `settings.py`, `desktop.py`, `change_us_flow.py` | b1–b7 đổi US; b8–b15 tạo tài khoản bằng SĐT/tên/OTP đúng hàng máy; b16 Back đóng hộp Google; b17 Create a passkey; có thể chạy đầu luồng chỉ với proxy, b9 cần hàng Amazon | `test_settings.py`, `test_desktop_resume.py`, `test_change_us_flow.py` |
| b1–b3 cả 12 máy | `random_prefix.py` | `prefix_choices`, `prefix_view_until`, `prefix_completed`; đủ ba lượt xem rồi mới b4 | `test_random_prefix.py`, `test_resume_state.py` |
| b4–b11b Tạo/Đăng nhập cả 12 máy | `account_flow.py` | Các dấu SMS/OTP/Create/Verify trong `RegistrationState`; xác nhận màn thật trước bước kế | `test_q1_flow.py`, `test_resume_state.py` |
| b12–b15 chung | `random_prefix.py` | `tail_choices`, `tail_view_until`, `tail_viewed`, `tail_page_scrolled`, `tail_back_sent`, `tail_completed`; về menu rồi mới hoàn tất lượt | `test_random_prefix.py`, `test_resume_state.py` |
| b16–b22 chung | `marketplace_flow.py` | `marketplace_completed` và các dấu Done; xác nhận United States và màn sau Done | `test_marketplace_flow.py` |
| b23–b25 chỉ Tạo | `create_address_flow.py` | `create_address_completed`, `create_address_wait_until`; mở Your Addresses | `test_create_address_flow.py` |
| b26–b31 chỉ Tạo | `create_address_detail_flow.py` | Dấu nhập/chọn gợi ý/lưu trong `RegistrationState`; b27 bấm Enter an address manually xong chuyển ngay b28, b28 nhập số theo hàng máy rồi mới đọc gợi ý, b30 xác nhận đã lưu | `test_create_address_detail_flow.py` |
| b32–b39 chỉ Tạo | `reload_payment_flow.py` | Sau b31 cuộn ngay, OCR chữ Reload Balance/Buy Now/mục thêm thẻ; b38 nhập ba ô theo đúng hàng máy rồi bấm Add and continue; b39 thấy Use this address thì bấm | `test_reload_payment_flow.py` |
| Dừng/Tiếp tục và trạng thái máy | `post_menu.py`, `runner.py`, `desktop.py` | `PostMenuSession.next_step`, `RegistrationState`, serial và khóa riêng máy; không phát lại hành động đã xác nhận | `test_post_menu.py`, `test_resume_state.py`, `test_stop_reset.py`, `test_runner.py` |

`q7_random_prefix.py` và `q7_state_machine.py` giữ bản thử cũ làm tham chiếu;
factory hiện hành không gọi hai file này.

Quy tắc sửa: tìm mốc trong bảng này → đọc mục tương ứng trong `STEP_INVENTORY.md` → đọc ảnh tại `IMAGE_EVIDENCE.md` nếu là lỗi nhận diện → sửa ở file sở hữu → cập nhật trạng thái/test nếu có thao tác hoặc điểm Dừng/Tiếp tục → ghi kết quả thật hay mô phỏng vào mục cũ của `PROJECT_HANDOFF.md`. Sau đó chạy test liên quan, `python -m graphify update .` và `python -m graphify tree`. Không coi test mô phỏng là bằng chứng phiên Swarmote đang mở đã nạp mã mới.

Quy tắc file: `cloud.py`/`ui_backend.py`/`vision.py` là lớp ADB, cây Android và OCR dùng chung; `*_flow.py` quyết định hành động của bước; `post_menu.py` giữ trạng thái và thứ tự; `desktop.py` nối UI với runner. `q1_flow.py`–`q6_flow.py` và Q1–Q6 Markdown còn phần tham chiếu lịch sử; luồng thường hiện tại lấy từ `random_prefix.py`. Khi có hành vi mới sau một mốc, nối ở factory chung thay vì sao chép vào từng máy.

Đây là điểm bắt đầu để tiếp tục dự án mà không bỏ sót mốc đã biết. Ảnh người dùng cung cấp đã hướng dẫn q1–q4; q5/q6 được hướng dẫn bằng chữ; chưa có toàn bộ quy trình.

| Phần | Vị trí | Mục đích |
| --- | --- | --- |
| Chạy tool | [README.md](README.md), [Launch Swarmote Tool.pyw](Launch%20Swarmote%20Tool.pyw), `amazon_android/` | Cài đặt, mở giao diện và mã nguồn. |
| Cài máy mới | [Install Swarmote Tool.bat](Install%20Swarmote%20Tool.bat), [setup_windows.py](setup_windows.py) | Kiểm tra Python, trình duyệt, Swarmote; hỏi tải phần mềm và dependencies còn thiếu. |
| Bàn giao | [PROJECT_HANDOFF.md](PROJECT_HANDOFF.md), [FLOW_PROGRESS.md](FLOW_PROGRESS.md), [STEP_INVENTORY.md](STEP_INVENTORY.md) | Trạng thái thật, từng bước đã biết và phần còn thiếu. |
| Luồng Amazon | [POST_MENU_REQUIREMENTS.md](POST_MENU_REQUIREMENTS.md), [MENU_ROUTING.md](MENU_ROUTING.md), [Q1_FLOW.md](Q1_FLOW.md), [Q2_FLOW.md](Q2_FLOW.md), [Q3_FLOW.md](Q3_FLOW.md), [Q4_FLOW.md](Q4_FLOW.md), [Q5_FLOW.md](Q5_FLOW.md), [Q6_FLOW.md](Q6_FLOW.md), [OTP_DESIGN.md](OTP_DESIGN.md) | Hai bố cục menu, quy tắc tự động hóa và OTP theo máy. |
| Minh chứng ảnh | [IMAGE_EVIDENCE.md](IMAGE_EVIDENCE.md), `flow_images/q1/`, `flow_images/q2/`, `flow_images/shared/` | Ảnh gốc từng bước; phải mở ảnh để xem pixel. |
| Giao diện cũ | [ASSET_INDEX.md](ASSET_INDEX.md), `assets/ui_history/` | Các ảnh chụp giao diện qua những lần thiết kế. |
| Kiểm chứng | [VERIFICATION.md](VERIFICATION.md), `tests/` | Kết quả kiểm tra thật và test mô phỏng. |
| Kế hoạch | `plans/`, [PLAN.md](PLAN.md), [PRODUCT.md](PRODUCT.md), [DESIGN.md](DESIGN.md) | Quyết định, yêu cầu, giao diện. |
| Cây dự án | [GRAPH_AUDIT.md](GRAPH_AUDIT.md), [SOURCE_INDEX.md](SOURCE_INDEX.md), `graphify-out/` | Graphify, giới hạn lập chỉ mục và file không được phân tích. |
| Quy tắc phiên sau | [AGENTS.md](AGENTS.md) | Cách tiếp tục, cập nhật graph và bảo toàn dữ liệu từng máy. |

`graphify-out/` chỉ đưa lên các đầu ra đọc được (`graph.json`, `graph.html`, `GRAPH_TREE.html`, `GRAPH_REPORT.md`, `manifest.json`); cache và trạng thái dựng tạm được Git bỏ qua. `__pycache__/`, `.test_tmp/` và file chạy tạm cũng không phải mã nguồn. Dữ liệu nhập thật của phiên đang chạy chỉ ở bộ nhớ và không có trong repository.

