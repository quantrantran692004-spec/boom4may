# Điều hướng hai dạng menu ba gạch

**Từ 14/11/2026:** b1–b3 hiện hành của q1–q12 dùng `random_prefix.build_random_steps` để bấm/vuốt ngẫu nhiên theo kích thước Android, không đọc OCR. Nhánh cũ `route_list_menu` chỉ còn dùng cho factory cố định cũ.

## Bằng chứng và phạm vi

Ảnh [menu dạng danh sách](flow_images/shared/01_list_menu.png) hiển thị `Shop by Category`, Books, Electronics, Home services, See all, Today's Deals, Try Prime, Settings, Customer Service và Sign In. Bộ [14 ảnh menu mới](IMAGE_EVIDENCE.md) cho thấy 15 thẻ danh mục, các hàng mục con khi thẻ mở rộng, và Sign In ở cuối. Khi cuộn xuống, tiêu đề `Shop by category` có thể ra ngoài khung nhìn nhưng ba thẻ liền hàng vẫn xác nhận menu. Chưa có lượt chạy thật sau sửa.

## Quy tắc chạy

1. Từ menu đã xác nhận, lấy `wm size` của đúng serial và bấm một trong 12 vị trí tỷ lệ nằm trên các hàng thẻ trong ảnh. Không dùng số pixel cố định.
2. Batch ID xáo 12 vị trí đầu rồi gán một vị trí b1 riêng cho từng máy. B2/b3 chọn các vị trí khác, giữ lựa chọn trong phiên khi Tiếp tục.
3. Nếu ADB không xác nhận cú bấm, thử tối đa bốn vị trí, vuốt để xem hàng khác. Không có cú bấm nào thành công thì tự thử lại cùng bước. Không cần xác nhận tên thẻ hay màn hình đã đổi.
4. Trước b2/b3 và b4, chạm nút ba gạch theo kích thước máy. B4 kiểm tra đủ ba cú bấm rồi dùng bộ nhận diện Sign In cũ. B1–b3 không gửi OTP hoặc bấm Create.
5. b4–b11 là một bộ bước chung với SĐT, URL OTP, trạng thái SMS, mã và điểm dừng riêng cho từng máy. q1–q12 đều có ba bước bấm ngẫu nhiên trước b4 trong factory hiện hành.

Ở b4, menu có thể trả nhiều node cùng nhãn `Sign In` dù chỉ một hàng nhìn thấy. Bộ chọn chung ưu tiên node `clickable`; nếu nhãn vẫn lặp, dùng hàng `Customer Service` đang hiện ngay phía trên làm mốc và chỉ nhận một Sign In nằm dưới. Khi vẫn mơ hồ, tool dừng để sửa trên máy. Ảnh lỗi q1 ở [IMAGE_EVIDENCE.md](IMAGE_EVIDENCE.md).

## Kiểm chứng

Test mô phỏng kiểm tra đủ 12 máy có điểm b1 khác nhau, ba bước trước b4, thử vị trí khác và vuốt sau lỗi ADB, không chuyển b4 khi không có cú bấm nào thành công. Chưa thử 12 máy thật.

