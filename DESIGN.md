# Giao diện vận hành

## Swarmote V3 — nghiệm thu 27/11/2026

**Bổ sung sau khi hoàn tất V3 theo hai ảnh mới:** Cửa sổ lần mở đầu lấy mốc vùng nội dung 1696×878 px (cả khung/title bar khoảng 1698×916 px như ảnh), căn giữa và giới hạn theo màn hình để không vượt vùng nhìn thấy. Trên màn hình 1536×864 của môi trường kiểm tra, kích thước nội dung tự giới hạn còn 1472×724 px. Bảng nay có bốn cột Máy / Amazon / Trạng thái / Thao tác; bỏ riêng cột Proxy và nhường chiều rộng cho trạng thái. Ô dán proxy ở phần nhập liệu và mọi trường proxy ở khung phải giữ nguyên. Đây là yêu cầu sau V3, thay thế quy tắc giữ năm cột của tài liệu ban đầu. Ảnh cuối ở `assets/ui_history/v3_final.png` dùng dữ liệu giả và kích thước mở mặc định thực tế trên màn hình kiểm tra.

Nghiệm thu bản cuối: 628 unittest toàn dự án PASS. Đã kiểm tra thêm focus/hover/pressed, nút khóa, tooltip Cài đặt và hộp thoại native thông tin/lỗi với dữ liệu thử; đóng đúng hộp thoại của tiến trình kiểm tra. Kiểm tra scale 100/125/150% xác nhận cột Proxy không còn trong bảng và các ô Proxy bên phải vẫn hiện. Các callback tự động hóa không được gọi trong kiểm tra giao diện.

V3 thay thế phần màu và trình bày V2 bên dưới; giữ hai cột, dữ liệu và các callback chạy máy. Màu dùng `desktop_theme.py`: nền #EDF1F3, khung #FAFBFC, nhập liệu #F2F5F7, chọn #EAF4F5, header #B4DFE1 và footer #F5F7F8. Các vùng nội dung/ô nhập/nút phụ chuyển về xám lạnh; màu thương hiệu chỉ còn ở header, trạng thái, vùng chọn và chức năng cần nhận diện. Primary vàng chỉ khi khả dụng, secondary trung tính có viền, danger đỏ nhạt cho Dừng/Xóa, disabled cùng màu chữ/icon trung tính.

Typography dùng các face cùng họ Segoe UI: thương hiệu bold, tiêu đề và tên máy Semibold 600, dữ liệu regular, nút regular, trạng thái chính Semibold 15–16, diễn giải regular 14. Bảng giữ nhãn Tk nhẹ có theo dõi DPI, các ô cùng nền toàn hàng, đường ngang 1 px; bỏ icon thừa và vạch trắng ở header. Tóm tắt Amazon còn ba dòng, quyền sửa và dữ liệu gốc không đổi. StatusCell giữ nguyên toàn bộ thông báo, hiển thị nhãn ngắn cùng mô tả rút gọn; hover xem đầy đủ, chọn hàng xem nguyên văn bên phải. Khung trạng thái không còn mảng nền màu lớn.

28 icon Lucide nét 1,75 px, thêm `list`; khoảng icon–chữ 6 px. Scrollbar màu #C1CCD2, hover #9DADB6, phần nhìn thấy 8 px trong vùng tương tác 16 px. Bề mặt phân tầng bằng sắc độ/viền; không thêm bóng giả hoặc animation. Nhãn dài đổi wrap theo chiều rộng; ở 150% bảng tự giảm wrap mà không giảm cỡ chữ. Ô mật khẩu bên phải dùng trọn chiều rộng trong khung để tránh ép nhãn. Settings vừa màn hình, nội dung cuộn được để nút Lưu không bị mất ở DPI lớn. Hộp thoại hệ điều hành giữ kiểu native.

Placeholder điều chỉnh nhẹ từ #687983 (4,12:1) sang #62727C để đạt 4,5:1. Các cặp chữ khả dụng và trạng thái đạt 4,5:1; icon/focus đạt 3:1. Border nhập liệu màu tinh tế theo bảng màu không đạt 3:1 nếu xét riêng đường viền; cần xác minh thêm với người dùng cần độ tương phản cao. Disabled không dùng để đánh giá tương phản của chức năng khả dụng.

Kiểm tra: cửa sổ Tk độc lập với dữ liệu giả, trống/3 hàng/12 hàng, chọn/hover, sáu trạng thái, tooltip đầy đủ, Settings, cuộn tới Máy 12. Mức scale ứng dụng tương đương 100%, 125%, 150% và cửa sổ 1460×751/1375×714; không thay DPI toàn Windows hoặc đóng phiên thật. Ở 150%, bảng yêu cầu 876 px trong 877 px, khung phải tối đa 469 px trong 481 px. 627 unittest toàn dự án PASS trước tinh chỉnh cuối kiểu chữ Settings. Ảnh trước/sau cùng kích thước và dữ liệu mẫu ở `assets/ui_history/v3_before.png` và `v3_after.png`.

Mẫu đo một lần ở 125%: V2 mở cửa sổ 1,42 s/RSS 59,45 MB; V3 khoảng 1,34 s/RSS 59,20 MB; 40 lượt hover 0,81/0,92 giây CPU. Dao động này không chứng minh thay đổi hiệu năng dài hạn. Khoảng cách từ hàng 1 tới hàng 12 giảm khoảng 9% ở cùng 125%. Chưa kiểm thử công việc thật nhiều giờ hoặc chuyển cửa sổ giữa các màn hình có DPI khác nhau.

Tự đánh giá dưới đây là nhận xét chủ quan dựa trên ảnh và kiểm tra UI, không phải chứng nhận đạt mục tiêu 9/10.

| Tiêu chí | Tự đánh giá | Bằng chứng và giới hạn |
|---|---:|---|
| Phối màu | 8,2/10 | Bề mặt trung tính, màu nhấn theo vai trò; cần phản hồi dùng lâu |
| Dễ nhìn | 8,2/10 | Đã đo tương phản chữ; viền nhập liệu còn nhẹ |
| Hiện đại | 8/10 | Bỏ mảng trạng thái và đường trắng dư; vẫn theo giới hạn Tk |
| Icon | 8,3/10 | Một bộ Lucide 1,75 px, bớt icon header |
| Phân cấp | 8,3/10 | Trạng thái hai cấp, giảm bold |
| Font/trình bày | 8,2/10 | Segoe UI/face Semibold, scaling nhất quán |
| Bố cục/không gian | 7,8/10 | Hàng gọn hơn; cửa sổ thấp vẫn cần cuộn |
| Nhất quán | 8,4/10 | Tokens, bốn vai trò nút và cùng hệ chữ |
| Cảm giác cao cấp | 7,8/10 | Bề mặt/viền tiết chế; cần người dùng xác nhận |

Các file triển khai: `desktop.py` (bố cục bên trong, trạng thái, density và kích thước mở), `desktop_theme.py` (tokens, typography, trạng thái hiển thị, thành phần Tk theo DPI), `assets/icons/` (nét Lucide 1,75 px và list), `tests/test_desktop_layout.py` (DPI, nguyên văn trạng thái, Proxy phải và kích thước mở), `tests/test_stop_reset.py` (cập nhật mock widget, giữ kiểm tra callback), cùng DESIGN/PROJECT_HANDOFF/ASSET_INDEX và Graphify. Không sửa runner, các file flow, registry, parser hoặc dữ liệu Settings/Profile.

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
