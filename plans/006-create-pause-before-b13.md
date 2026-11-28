# Công tắc dừng trước b13 của luồng Tạo

**Yêu cầu 28/11/2026:** Settings có công tắc cho luồng Tạo tài khoản thường. Khi bật, máy hoàn tất b11 xác nhận tài khoản và b12 mở menu, rồi tạm dừng trước cú bấm b13. Khi người dùng bấm Tiếp tục, chạy từ b13 một lần. Khi tắt, luồng hiện tại chạy liên tục. Đăng nhập và Đổi US từ đầu không đổi.

**Thiết kế:** Lưu boolean mặc định tắt trong `AppSettings/settings.json`; đọc file Settings cũ với mặc định tắt. Lấy snapshot khi mỗi `PostMenuSession` bắt đầu. Tại vòng chạy bước, khi bước kế là b13 và mode là `create`, dừng một lần trên session đó, giữ `next_step` ở b13 và báo rõ trên đúng hàng máy. Không thay đổi factory, thứ tự b1–b39 hay thao tác Android.

## Công việc

- [x] Test đỏ: đọc/lưu Settings cũ và mới; bật thì b12 hoàn tất nhưng b13 chưa gửi, Tiếp tục từ b13; tắt và hai mode khác không dừng.
- [x] Thêm boolean trong settings, công tắc ở dialog và snapshot vào registration của từng máy.
- [x] Thêm chốt dừng một lần trước b13 trong `PostMenuSession.run`, bảo toàn Dừng/Tiếp tục cũ.
- [x] Chạy test mục tiêu, test toàn dự án và kiểm tra Settings giao diện bằng Tk giả nếu khả thi.
- [x] Cập nhật mục cùng chủ đề trong `PROJECT_HANDOFF.md`, `STEP_INVENTORY.md`, `README.md`/`VERIFICATION.md`; chạy Graphify update/tree, kiểm tra Git, commit/push `main`.
