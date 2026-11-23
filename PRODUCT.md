# Amazon trên Swarmote

## Người dùng và công việc

- Người dùng tự chuẩn bị proxy và thông tin đăng ký, muốn nhập vào phần mềm của mình thay vì gửi từng bộ trong chat.
- Một thao tác có thể chuẩn bị 1–12 điện thoại Swarmote; người dùng muốn lặp lại các mẻ có kích thước khác nhau.
- Công cụ tạo Profile, gán proxy, mở điện thoại và cài Amazon Shopping. q1 và q2 đã có b1–b3 riêng rồi dùng chung b4–b11 tới OTP SMS theo ảnh người dùng nhưng chưa thử thật; q3–q12 vẫn dừng ở menu ba gạch. SĐT, mật khẩu, tên, thẻ và URL OTP của mỗi hàng được gắn với đúng máy và giữ trong bộ nhớ phiên; thẻ chưa được dùng trong luồng hiện tại.

## Nền tảng

- Windows desktop, chạy cùng ứng dụng Swarmote đã đăng nhập.
- Điều khiển Swarmote bằng UI Automation nền; điều khiển điện thoại bằng ADB qua tunnel của Swarmote.
- Mật khẩu chỉ giữ trong bộ nhớ phiên, không ghi SQLite hay log.

## Định hướng ngôn ngữ nếu xây dựng lại — 23/11/2026

- Tool hiện tại chủ yếu viết bằng Python. Đây là định hướng cho bản xây dựng lại, chưa phải quyết định chuyển mã hiện tại.
- **C#/.NET là lựa chọn tổng thể cho tool Windows điều khiển nhiều máy Android:** phù hợp giao diện Windows, tác vụ song song và bảo trì lâu dài. [Microsoft khuyến nghị C# cho phần lớn ứng dụng Windows](https://learn.microsoft.com/en-au/windows/apps/get-started/windows-developer-faq).
- **C++** phù hợp phần xử lý ảnh thật sự cần hiệu năng và kiểm soát tài nguyên sát hơn, nếu phép đo trên máy thật chứng minh cần. [Tài liệu Microsoft về Win32/C++](https://learn.microsoft.com/en-us/windows/win32/desktop-programming).
- **Go** phù hợp điều phối nhiều công việc đồng thời nhờ goroutine nhẹ; với yêu cầu giao diện Windows của tool này, vẫn ưu tiên C#. [Tài liệu Go về goroutine](https://go.dev/tour/concurrency/1?m=text).
- Nếu xây lại: dùng C# cho toàn bộ tool; chỉ dùng C++ cho phần xử lý ảnh nếu đo thực tế thấy cần. Việc đổi ngôn ngữ không thay thế sửa logic nhận diện ô, quản lý trạng thái và ánh xạ dữ liệu riêng từng máy. Không giả định mức tiết kiệm RAM hay tốc độ khi chưa đo cùng một luồng trên máy thật.

## Điều chưa xác minh

- Biểu mẫu tên/mật khẩu của Amazon sau bước Continue chưa có thử nghiệm thật.
- Khởi chạy Profile từ Offline và một mẻ 5 máy chưa được thử end-to-end.
- Giới hạn slot Profile và tính năng tạo hàng loạt riêng của Swarmote chưa được kiểm chứng cho bản đang cài.
