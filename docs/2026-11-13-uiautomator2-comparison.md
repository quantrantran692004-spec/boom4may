# So sánh bộ đọc trên q1 — 13/11/2026

Người dùng đã cho phép cài phương án phù hợp để tăng tốc. Đã cài UiAutomator2 3.7.1, adbutils 2.12.0 trong `.venv`, xác nhận cửa sổ q1 `ACN988108301336632` có tunnel `127.0.0.1:57451` bằng bộ đọc Swarmote UIA sau khi người dùng đồng ý dùng cách này thay agent-desktop bị lỗi DACL. Dùng ADB server Swarmote có sẵn tại 127.0.0.1:5037; không chọn serial tự động.

## Thành phần thiết bị

UiAutomator2 3.7.1 chép `u2.jar` vào `/data/local/tmp/u2.jar` và chạy máy chủ qua `app_process` dưới quyền adb shell. Không dùng hàm nhập liệu/clipboard/IME của thư viện; không cài APK bàn phím, không thay bàn phím hay cấu hình bảo mật. Các phiên đo dừng máy chủ khi kết thúc, giữ file JAR để lần dùng sau không phải chép lại nếu nội dung đã đúng. Mã ứng dụng giữ client theo từng serial và thư viện dừng máy chủ do client tạo khi tiến trình thoát.

## Kết quả thực tế

q1 đang ở menu, không còn ở hộp chọn quốc gia trong ảnh trước. Không điều hướng, bấm hay gõ trên Android để ép tới một màn kiểm thử.

| Phương án | Các lượt đọc | Nhận diện |
| --- | --- | --- |
| ADB `uiautomator dump` + đọc XML | 2491,8 / 2409,7 / 2384,0 ms | MENU, 105 node Amazon ở mỗi lượt |
| ADB screenshot + OCR | 8757,1 ms lúc khởi tạo; 6882,3 / 6763,2 ms sau đó | MENU ở cả ba lượt |
| UiAutomator2 mặc định lúc mới gắn | 502,7 / 415,5 / 375,2 / 370,3 / 267,8 ms | UNKNOWN, 46 node; chưa đủ để dùng làm kết luận |
| UiAutomator2 chỉ định đầy đủ root | 520,1 ms (depth 50, root_in_active=False), 379,6 ms (depth 150, False), 396,1 ms (depth 150, True) | MENU, 106 node, có một vùng scrollable |
| ADB đọc lại sau khi dừng UiAutomator2 | 2466,0 ms | MENU, 107 node |
| Adapter tích hợp, depth 150/all roots | 8126,5 ms gồm khởi tạo; 579,8 / 307,4 ms khi tái sử dụng client | MENU, 111 node ở cả ba lượt |

Lần khởi tạo thư viện riêng ban đầu là 3487,6 ms; cold start không được tính là lượt đọc đã giữ kết nối. Nội dung menu có node động, nên số node thay đổi giữa các loạt. Không suy ra tốc độ toàn bộ b1–b11 từ thời gian dump. Chưa đo hộp quốc gia, form nhập hoặc q2 bằng UiAutomator2.

## Kết luận và tích hợp

Kết hợp: ưu tiên UiAutomator2 đọc XML với đầy đủ root; ADB cũ khi thư viện không hoạt động; OCR khi WebView vẫn thiếu nội dung. Kết quả trên menu cho thấy đọc UiAutomator2 khi có kết nối nhanh hơn dump ADB trong các lượt đã đo. Không có dữ liệu để tuyên bố mọi màn đều nhanh hoặc chính xác hơn.

`amazon_android/ui_backend.py` quản lý client và khóa riêng từng serial. Lỗi kết nối/XML làm ngừng client lỗi, nghỉ 30 giây trước khi thử lại; trong lúc đó dùng ADB cũ. Không khởi tạo client mới khi thời hạn bước còn dưới 35 giây. OCR không bỏ qua client UiAutomator2 đang khỏe.

B6 chỉ dùng cuộn native khi cây mới có tiêu đề Country/region code và duy nhất một container Amazon scrollable. Xa US dùng fling.toEnd với tối đa ba swipe; gần US dùng cú vuốt ngắn trong bounds mới của container. Khi kết quả RPC không rõ, không phát thêm ADB swipe trong cùng lần gọi. Không có native container thì dùng đường ADB/OCR đã có. Nhánh native này đã kiểm tra bằng unittest, chưa chạy trực tiếp trên danh sách quốc gia q1.

Dependencies bộ cài đã thêm UiAutomator2. Tool đang mở vẫn giữ mã đã nạp trước đó; chỉ bản khởi chạy sau mới dùng adapter. Không đóng hoặc đặt lại mẻ hiện tại vì dữ liệu chỉ ở RAM.
