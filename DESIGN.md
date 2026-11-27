# Giao diện vận hành

## Hướng thị giác

Màn hình vận hành sáng với nền xám ấm nhạt, thẻ trắng, chữ xám than và nút chính xanh trầm. Bảng máy và ô nhập dùng nền trung tính để đọc lâu không mỏi mắt; hàng được chọn tô xám xanh rất nhẹ. Trạng thái dùng xanh lá trầm cho thành công, đỏ trầm cho lỗi và luôn kèm chữ. Biểu tượng chỉ dùng cho thao tác tương ứng; không có ảnh trang trí chiếm vùng làm việc.

## Bố cục

- Thanh đầu: tên công cụ, chọn số máy trong mẻ và Cài đặt.
- Cột chính: hai ô dán proxy/Amazon và bảng đủ 12 máy, kể cả máy chưa dùng trong mẻ. Hai ô dán hàng loạt vẫn hiện khi mẻ chạy nhưng bị khóa để tránh ghi đè nhiều máy. Bấm một hàng để chọn máy.
- Cột chi tiết: máy đang chọn, OTP ở đầu, hai ô dán proxy/hàng Amazon để sửa máy đó, rồi các trường Amazon và proxy riêng. Mọi ô luôn hiện; proxy của máy chưa tạo Profile được sửa khi máy dừng/lỗi, Amazon của máy dừng/lỗi được sửa riêng. Proxy đã gắn vào Profile hiện khóa để tránh báo sai rằng sửa trong tool đã đổi proxy của Swarmote. Công cụ gắn máy từ menu ở cuối khung.
- Thanh cuối cố định: Chạy, Dừng cả mẻ, Mẻ mới và thông báo. Tiếp tục/Dừng từng máy nằm ngay trong hàng bảng của máy đó.
- Không có cột danh sách máy trùng bảng, khối hình 3D, hay nút cuộn tới bảng. Các nút thao tác có biểu tượng tương ứng và chữ ngắn để tránh nhầm khi nhiều máy chạy.
- Chữ dữ liệu trong bảng máy cỡ 18 bằng Segoe UI, tên máy đậm; tiêu đề cột và nút từng hàng cỡ 15, nút cao 40. Hai nút của máy đang dùng xếp dọc để dành chiều rộng cho thông tin; không ép đủ 12 máy vào một màn hình, cuộn bảng để xem máy còn lại. Máy chưa nhập Amazon hiện một dòng gọn thay cho nhiều dòng giữ chỗ. Các nhãn và ô ở khung chi tiết dùng cùng font, cỡ 14–20 theo mức quan trọng.

## Quy tắc

- Danh sách được kiểm tra khi dán; lỗi hiện cạnh vùng dán và trong thông báo vận hành.
- Vùng dán được xóa sau khi áp dụng; mật khẩu và thẻ trong chi tiết được che, bảng chỉ cho thấy trạng thái đã có dữ liệu và đuôi thẻ.
- Không tự bấm nút gửi đăng ký Amazon. Trạng thái kết quả phải phản ánh bước thực sự đã xác minh.
