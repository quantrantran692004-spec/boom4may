# q6 — Trang chủ, Giỏ hàng, menu và một thẻ

> B1–b3a cố định trong tài liệu này là lịch sử hướng dẫn. Factory đang chạy của q6 dùng ba lượt ngẫu nhiên trong `random_prefix.py`; b4–b11 vẫn là luồng chung.

Người dùng chốt luồng riêng q6 từ menu ba gạch:

| Mốc | Thao tác |
| --- | --- |
| b1 | Bấm Trang chủ, xem 2 giây. |
| b2 | Bấm Giỏ hàng, xem 2 giây. |
| b3 | Tự về menu ba gạch. |
| b3a | Bấm thẻ Devices and Electronics; ở menu dạng danh sách, dùng hàng Electronics tương ứng. |
| b4–b11 | Dùng nguyên `build_common_steps`; nếu b3a mở trang khác, b4 tự về menu để tìm Sign In. |

b3 và b3a nằm trong một `PostMenuStep` để b4 chung vẫn ở vị trí thứ tư như các máy khác. Luồng danh sách không bỏ qua các bước riêng của q6. Mỗi thao tác dùng đúng ADB serial của q6. Chưa chạy trên máy thật; nếu menu có biến thể khác, dừng tại bước chưa nhận được và chờ người dùng hướng dẫn.
