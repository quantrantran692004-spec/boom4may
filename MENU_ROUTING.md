# Điều hướng hai dạng menu ba gạch

**Từ 14/11/2026:** b1–b3 hiện hành của q1–q12 dùng `random_prefix.build_random_steps` trên cả menu thẻ và menu danh sách. Nhánh cũ `route_list_menu` chỉ còn dùng khi gọi các factory q1–q6 cố định cũ.

## Bằng chứng và phạm vi

Ảnh [menu dạng danh sách](flow_images/shared/01_list_menu.png) hiển thị `Shop by Category`, Books, Electronics, Home services, See all, Today's Deals, Try Prime, Settings, Customer Service và Sign In. Trước đây người dùng hướng dẫn Home rồi b4 cho dạng này; chỉ dẫn mới thay b1–b3 bằng ba lượt ngẫu nhiên. Các ảnh menu dạng thẻ của q1/q2 vẫn ở [IMAGE_EVIDENCE.md](IMAGE_EVIDENCE.md). Chưa có lượt chạy thật sau sửa.

## Quy tắc chạy

1. Sau khi xác nhận menu trên ADB serial của máy, đọc cây Android hiện tại và lấy các mục danh mục hoặc tab Home/Cart đang hiện, có vùng bấm hợp lệ. Không dùng tọa độ từ ảnh.
2. Mỗi máy bốc một mục cho từng bước b1, b2, b3; ưu tiên chưa lặp trong cùng mẻ. Cả menu thẻ và menu danh sách dùng cách này. Chỉ chọn trong các nhãn điều hướng/danh mục đã nhận diện; bỏ qua Sign In, Settings và thao tác tài khoản.
3. Nếu lần bấm mở trang khác, bước kế dùng `_ensure_menu` quay lại. Lượt đọc b1–b3 có hạn 15 giây; không tìm được mục phù hợp thì báo và chuyển tiếp. B4 tự đưa máy về menu nếu cần, tìm Sign In và xác nhận form số điện thoại.
4. Khi bấm Tiếp tục, giữ lựa chọn đã bốc của máy và bước hiện tại. Không bốc lại toàn bộ mẻ. B1–b3 không gửi OTP hoặc bấm Create; các điểm dừng an toàn của b4–b11 vẫn giữ.
5. b4–b11 là một bộ bước chung với SĐT, URL OTP, trạng thái SMS, mã và điểm dừng riêng cho từng máy. q1–q12 đều có ba bước bấm ngẫu nhiên trước b4 trong factory hiện hành.

Ở b4, menu có thể trả nhiều node cùng nhãn `Sign In` dù chỉ một hàng nhìn thấy. Bộ chọn chung ưu tiên node `clickable`; nếu nhãn vẫn lặp, dùng hàng `Customer Service` đang hiện ngay phía trên làm mốc và chỉ nhận một Sign In nằm dưới. Khi vẫn mơ hồ, tool dừng để sửa trên máy. Ảnh lỗi q1 ở [IMAGE_EVIDENCE.md](IMAGE_EVIDENCE.md).

## Kiểm chứng

Test mô phỏng kiểm tra phân loại hai bố cục, q1/q2 bỏ qua b1–b3 khi gặp danh sách, giữ các bước riêng khi gặp thẻ, hồi phục từ Home và b4 quay lại menu trước Sign In. Chưa có ADB của q1/q2 trong môi trường kiểm tra hiện tại, nên kết quả trên máy thật và các biến thể UI khác chưa được xác nhận. Khi có dump thực tế, đối chiếu chữ, `content-desc`, trạng thái chọn và vùng bấm rồi sửa bộ phân loại chung nếu cần.

