# Giao diện vận hành

## Hướng thị giác

Theo đặc tả Swarmote V2 ngày 27/11/2026: nền `#E8EEEE`, header `#BCE4E4`, footer `#F0F5F5`, khung `#F8FAFA`, ô nhập `#F0F4F4`. Tiêu đề graphite `#192D31`, nội dung `#293D42`, chữ phụ `#58686D`, thương hiệu/focus `#006D77`. Nút Chạy khả dụng dùng vàng champagne `#F3D36C` (hover `#EAC65A`, pressed `#DEB94E`); nút phụ xanh ngọc nhẹ, Dừng đỏ trầm trên nền đỏ nhạt. Nút khóa và icon cùng màu trung tính. Không phủ vàng lên nền lớn, không gradient hay chuyển động mới.

Mọi màu và quy chuẩn icon tập trung ở `amazon_android/desktop_theme.py`. Lucide 0.468.0 dùng SVG nét 1,8 px và PNG alpha 96×96 tương thích Tk, tô màu bằng Pillow sẵn có; không cần mạng hay thư viện render SVG khi chạy. Icon khu vực 20 px, nút/trạng thái 16 px, tiêu đề bảng 14 px; khoảng icon–chữ 6 px. Cài đặt có tooltip, tên native và điều khiển bằng bàn phím. Chỉ đặt icon ở nơi còn đủ chỗ; nhãn mật khẩu nửa cột giữ nguyên chữ để không đẩy rộng form.

Chữ đang chờ dùng `#88651B` thay `#8B681D`, placeholder dùng `#637277` thay `#647378`: hai màu gốc chỉ đạt 4,39 và 4,44:1 trên nền chỉ định. Hai điều chỉnh nhỏ đạt yêu cầu 4,5:1; các cặp chữ khả dụng và trạng thái còn lại đạt 4,5:1. Màu vô hiệu hóa giữ nguyên theo đặc tả.

## Bố cục

- Thanh đầu: tên công cụ, chọn số máy trong mẻ và Cài đặt.
- Cột chính: hai ô dán proxy/Amazon và bảng đủ 12 máy, kể cả máy chưa dùng trong mẻ. Hai ô dán hàng loạt vẫn hiện khi mẻ chạy nhưng bị khóa để tránh ghi đè nhiều máy. Bấm một hàng để chọn máy.
- Cột chi tiết: máy đang chọn, trạng thái đậm ngay dưới tên máy; mã OTP và sao chép chỉ xuất hiện khi đã có mã theo yêu cầu trước V2. Hai ô dán proxy/hàng Amazon rồi các trường riêng giữ vị trí hiện có. Mọi ô sửa luôn hiện; proxy của máy chưa tạo Profile được sửa khi máy dừng/lỗi, Amazon của máy dừng/lỗi được sửa riêng. Proxy đã gắn vào Profile hiện khóa để tránh báo sai rằng sửa trong tool đã đổi proxy của Swarmote. Công cụ gắn máy từ menu ở cuối khung.
- Thanh cuối cố định: Chạy, Dừng cả mẻ, Mẻ mới và thông báo. Tiếp tục/Dừng từng máy nằm ngay trong hàng bảng của máy đó.
- Không có cột danh sách máy trùng bảng, khối hình 3D, hay nút cuộn tới bảng. Các nút thao tác có biểu tượng tương ứng và chữ ngắn để tránh nhầm khi nhiều máy chạy.
- V2 giữ nguyên toàn bộ font, cỡ chữ, kích thước, vị trí và bố cục tại lúc nhận đặc tả: Segoe UI, dữ liệu bảng cỡ 17, tiêu đề cột/nút 16, nút hàng cao 40. Tiếp tục/Dừng xếp dọc; cuộn để xem các hàng còn lại. Bảng dùng một nền liên tục toàn hàng, nền lẻ `#F8FAFA`, chẵn `#F1F5F5`, chọn `#E3F1F1`, hover `#EDF5F5`; không còn mảng nền rời quanh từng ô. Icon và màu trạng thái không đổi dữ liệu, thứ tự bước hay quyền Dừng/Tiếp tục.

## Quy tắc

- Danh sách được kiểm tra khi dán; lỗi hiện cạnh vùng dán và trong thông báo vận hành.
- Vùng dán được xóa sau khi áp dụng; mật khẩu và thẻ trong chi tiết được che, bảng chỉ cho thấy trạng thái đã có dữ liệu và đuôi thẻ.
- Không tự bấm nút gửi đăng ký Amazon. Trạng thái kết quả phải phản ánh bước thực sự đã xác minh.
