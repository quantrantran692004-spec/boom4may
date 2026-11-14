# q4 — Giỏ hàng, Pets, Home and DIY

> B1–b3 cố định trong tài liệu này là lịch sử hướng dẫn. Factory đang chạy của q4 dùng ba lượt ngẫu nhiên trong `random_prefix.py`; b4–b11 vẫn là luồng chung.

Theo hướng dẫn cùng hai ảnh người dùng ngày 13/11/2026:

| Bước | Thao tác |
| --- | --- |
| b1 | Bấm tab giỏ hàng và xác nhận màn giỏ hàng |
| b2 | Trở về menu ba gạch, tìm và bấm Pets |
| b3 | Trở về menu nếu cần, tìm và bấm Home and DIY |
| b4–b11 | Dùng nguyên `build_common_steps`, cùng q1/q2/q3 |

`amazon_android/q4_flow.py` khai báo ba bước riêng; `profile_navigation.py` xử lý điều hướng. Giỏ hàng được tìm bằng content-desc `Cart Tab...` trong cây Android, không bấm hình giỏ hàng trong nội dung trang bằng tọa độ ảnh. Xác nhận bằng tab đã chọn hoặc dấu hiệu màn giỏ hàng trống trong ảnh. Nếu lúc tiếp tục đã ở giỏ hàng thì không chạm tab lần nữa. Thiếu tab được đọc lại trước khi báo lỗi.

Trước Pets/Home and DIY, `_ensure_menu` dùng tab Browse menu hoặc đường về menu hiện có. Thẻ Pets có thể mở rộng danh sách Pet Supplies/Dogs/Cats/Birds; bước sau tìm Home and DIY trong menu và cuộn khi cần. Menu danh sách chữ vẫn dùng quy tắc định tuyến chung tại MENU_ROUTING.md.

q4 được nối vào factory Máy 4 và nút Thử q4 từ menu ba gạch; thông tin hàng 4, serial, RegistrationState, OTP và thời hạn độc lập. Đã kiểm tra unittest, OCR trên ảnh giỏ hàng và ảnh Pets. Chưa chạy b1–b11 trên q4 thật; chưa tự tạo/khởi chạy Profile q4 để thử.
