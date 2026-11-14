# q5 — ba thẻ riêng và b4–b11 chung

> B1–b3 cố định trong tài liệu này là lịch sử hướng dẫn. Factory đang chạy của q5 dùng ba lượt ngẫu nhiên trong `random_prefix.py`; b4–b11 vẫn là luồng chung.

Người dùng chốt q5 từ menu ba gạch: b1 **Toys, Kids and Baby**, b2 **Office & Professional**, b3 **Sports & Outdoors**. Tool bấm từng thẻ theo chữ trên giao diện thật. Nếu thẻ mở một trang riêng, tool tự quay về menu để tìm thẻ tiếp theo; nếu vẫn ở menu thì bấm tiếp ngay. Không có bước chờ riêng. Sau b3, `build_common_steps` đảm nhận b4–b11 như q1–q4.

Đã nối trong `amazon_android/q5_flow.py` và factory Máy 5. Chưa có ảnh q5 hay lượt chạy thật; nếu giao diện q5 khác, dừng tại bước chưa tìm được để người dùng hướng dẫn tiếp. q6–q12 vẫn dừng ở menu.
