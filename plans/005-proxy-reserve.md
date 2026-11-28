# Proxy dự phòng trong RAM Implementation Plan

> **For agentic workers:** Thực hiện từng task theo TDD; test đỏ trước khi sửa mã.

**Goal:** Thêm dòng dán proxy dự phòng; cấp phát đúng một proxy cho máy có Test Proxy thất bại hoặc Country không phải US trước Create; giữ phần chưa dùng qua Mẻ mới và chỉ mất khi đóng ứng dụng.

**Architecture:** Một pool FIFO có khóa thuộc vòng đời `Window` giữ tối đa 100 proxy dự phòng trong RAM. Runner chỉ lấy qua callback theo `batch_id`; UI nhận sự kiện trong bộ nhớ để cập nhật đúng hàng máy và số lượng còn lại. Proxy dư từ ô dán Proxy hiện tại đi vào cùng pool.

**Tech Stack:** Python 3.12, CustomTkinter, unittest; không thêm dependency.

**Spec:** Yêu cầu và ảnh người dùng ngày 28/11/2026; chỉ dùng proxy dự phòng ở Test Failed/Country khác US trước khi tạo Profile.

## Global Constraints

- Không lưu proxy dự phòng ra đĩa hoặc log thông tin nhạy cảm.
- Không sửa proxy của Profile đã tạo; không dùng dự phòng cho lỗi OTP, ADB hoặc Amazon.
- Mẻ mới không đóng/reset phiên Swarmote thật và không cho worker mẻ cũ lấy pool của mẻ mới.
- Giữ mapping proxy/SĐT/mật khẩu/tên/thẻ/URL OTP theo đúng hàng máy.

## Review Focus

- Dán trùng hoặc dán lại danh sách đã tiêu thụ: không cấp phát cùng proxy lần hai trong một phiên ứng dụng.
- Hai máy lỗi gần nhau: mỗi máy nhận một proxy khác nhau theo thứ tự FIFO.
- Dán thêm khi mẻ đang chạy: runner thấy proxy mới mà không cần tạo lại job.
- Mẻ mới khi worker cũ còn thoát: worker cũ không lấy proxy chưa dùng.
- Proxy dự phòng thất bại tiếp: lấy mục kế tiếp; hết pool thì dừng đúng máy.

### Task 1: Pool và dán dự phòng

**Files:** `amazon_android/proxy_reserve.py`, `amazon_android/desktop.py`, `tests/test_proxy_reserve.py`, `tests/test_bulk_input.py`

- [x] Viết test đỏ cho pool FIFO, trùng, giới hạn 100, batch guard và dán riêng không gán vào 12 máy.
- [x] Chạy test mục tiêu và xác nhận lỗi đúng yêu cầu.
- [x] Thêm pool RAM; thêm dòng Proxy dự phòng giữa hai dòng cũ; nhận proxy bằng parser hiện có, báo số còn lại, cho dán khi mẻ khóa.
- [x] Chạy test mục tiêu đến xanh; bảo toàn cách dán proxy dư qua ô cũ.

### Task 2: Cấp phát và vòng đời mẻ

**Files:** `amazon_android/runner.py`, `amazon_android/desktop.py`, `tests/test_runner.py`, `tests/test_stop_reset.py`

- [x] Viết test đỏ cho Test Failed/non-US lấy và xóa một proxy, không lấy ở lỗi khác, cập nhật proxy đúng máy, Mẻ mới giữ phần chưa dùng.
- [x] Chạy test mục tiêu và xác nhận lỗi đúng yêu cầu.
- [x] Runner lấy atomically qua callback chỉ trong `ProxyTestFailed`; UI cập nhật qua event queue, thay `RunJob.proxy` đúng hàng, giữ pool khi reset và đổi batch guard.
- [x] Chạy test mục tiêu đến xanh.

### Task 3: Bố cục hẹp và xác minh

**Files:** `amazon_android/desktop.py`, `tests/test_desktop_layout.py`, `PROJECT_HANDOFF.md`, `DESIGN.md`

- [x] Dùng test bố cục đang đỏ (460 > 382) làm kiểm chứng; xếp hai panel dọc khi không đủ chiều rộng, vẫn hai cột khi đủ.
- [x] Chạy test giao diện mục tiêu và toàn bộ `.venv/Scripts/python.exe -m unittest discover -s tests -q`.
- [x] Ghi kết quả mô phỏng và giới hạn phiên thật vào mục cũ của PROJECT_HANDOFF; cập nhật DESIGN nếu bố cục đổi.
- [x] Chạy `python -m graphify update .`, `python -m graphify tree`; xác nhận file/symbol trong graph, Git sạch sau commit/push.
