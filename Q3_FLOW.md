# q3 — b1–b3 và nối luồng chung

> B1–b3 cố định trong tài liệu này là lịch sử hướng dẫn. Factory đang chạy của q3 dùng ba lượt ngẫu nhiên trong `random_prefix.py`; b4–b11 vẫn là luồng chung.

Theo hướng dẫn cùng ảnh người dùng ngày 13/11/2026:

| Bước | Thao tác |
| --- | --- |
| b1 | Tìm và bấm Groceries and Drinks |
| b2 | Về menu nếu đang ở trang danh mục riêng, tìm và bấm Home and DIY |
| b3 | Về menu nếu cần, tìm và bấm Books and Reading |
| b4–b11 | Dùng nguyên `build_common_steps`, cùng q1/q2/q4 |

`amazon_android/q3_flow.py` chỉ khai báo ba bước riêng. `profile_navigation.py` tìm mục bằng nhãn trên giao diện trực tiếp của đúng serial; có thể cuộn khi mục chưa thấy. Thẻ có thể mở rộng ngay trong menu hoặc mở trang riêng. OCR dự phòng ghép chữ hai dòng của đúng thẻ, không dùng tọa độ cố định từ ảnh. Khi máy đã ở form đăng ký lúc tiếp tục, bỏ qua thao tác thăm danh mục đã qua.

q3 được nối vào factory Máy 3 và nút Thử q3 từ menu ba gạch. Menu danh sách chữ vẫn dùng quy tắc định tuyến chung tại MENU_ROUTING.md. SĐT/tên/thẻ/URL OTP, RegistrationState và đồng hồ riêng của Máy 3. Dữ liệu đầu vào phải ở hàng 3.

Đã kiểm tra unittest và OCR trên ảnh tĩnh. Chưa chạy b1–b11 trên q3 thật; chưa có tiêu chí màn sau Create.
