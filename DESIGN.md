# Giao diện vận hành

## Swarmote V3 — đối chiếu ảnh mẫu 27/11/2026

**Đã chốt bản hiện tại ngày 27/11/2026.** Ảnh `codex-clipboard-9591314d-702f-4cef-8756-b742e969202b.png` là chuẩn bố cục/màu: header/footer ngọc nhạt, thẻ máy riêng và tiến độ đậm. Mặc định mở gần kín màn hình theo cỡ nhỏ hơn người dùng chọn. Phần thiết kế chỉ đổi trình bày; hai yêu cầu chức năng bổ sung sau đó được chốt cùng bản này: nhận đủ hàng Markdown in đậm và bỏ yêu cầu mật khẩu tối thiểu 8 ký tự. Runner, flow tự động, callback và quyền Dừng/Tiếp tục/sửa máy giữ nguyên.

### Phân tích màu ảnh mẫu

Các mã lấy từ vùng phẳng đại diện của ảnh, có sai lệch nhỏ vì gradient và khử răng cưa. Mẫu không dùng một màu xanh cho mọi chức năng: xanh ngọc tạo nền thương hiệu, xanh lam chỉ hoạt động/tiếp tục, xanh lá hoàn tất, cam chờ, đỏ dừng/lỗi. Chữ chính gần đen có sắc xanh than; chữ phụ xanh xám đủ đậm để đọc.

| Vùng/vai trò | Màu đại diện trong ảnh | Token triển khai | Ý nghĩa |
|---|---|---|---|
| Nền cửa sổ | #F5F9FA | #F5F9FA | Xanh xám rất nhạt, giảm chói so với trắng toàn màn |
| Bề mặt khung | khoảng #FEFEFE | #FEFEFE | Tách vùng nhập, danh sách và chi tiết |
| Header | #DAEFF1 / #CFEEED | #DAEFF1, sóng #CFEEED–#B0E1E4 | Xanh ngọc nhẹ, không chiếm màu chức năng |
| Footer | khoảng #C3E2E5–#CBEBE9 | #CFE9EB | Nền nhẹ cho ba nút lớn |
| Hàng được chọn | #F1F6FE | #F1F6FE | Mảng xanh lam rất nhạt |
| Viền chọn | khoảng #075CFF | #075CFF | Viền và vạch trái chỉ rõ máy đang sửa |
| Chữ chính | Xanh than gần đen | #082D3B / #183747 | Tiêu đề / nội dung |
| Chữ phụ | Xanh xám | #3F6074 | Profile và diễn giải phụ |
| Tiến trình / Tiếp tục | Xanh lam bão hòa | #0055DE | Phân biệt với thao tác nhập dữ liệu màu ngọc |
| Nút Chạy | khoảng #0455D3 | #0455D3 | Nút xanh, chữ trắng khi được phép chạy |
| Nút Dừng cả mẻ | khoảng #DA323E | #DA323E | Nút đỏ, chữ trắng khi được phép dừng |
| Hoàn tất / chờ / lỗi | Xanh lá / cam / đỏ | #087126 / #B45300 / #C32236 | Luôn kèm tên trạng thái và icon |
| Ô nhập và viền | Gần trắng / xanh xám nhạt | #FFFFFF / #B9CFDD | Đủ tách khỏi khung, focus màu ngọc |

Tương phản tính theo độ chói sRGB: tiêu đề/khung 14,37:1; nội dung 12,42:1; chữ phụ 6,64:1; tiến trình xanh trên hàng chọn 5,77:1; **bước đang chạy đậm 10,20:1**; hoàn tất 6,12:1; chờ 4,98:1; Dừng 5,49:1; chữ trắng trên Chạy 6,47:1 và Dừng cả mẻ 4,66:1. Placeholder 5,05:1, chữ footer 9,09:1. Viền nhập nhẹ là phân cách thị giác, không khẳng định toàn bộ giao diện đạt chuẩn tiếp cận chỉ từ phép đo chữ. Disabled giữ trung tính và giữ nguyên điều kiện khóa cũ.

### Bố cục được áp dụng

- Header có logo lớp, thương hiệu, vạch phân cách, chọn số máy và Settings trắng. Sóng ngọc là Canvas vector tĩnh, chỉ vẽ lại khi đổi kích thước, không có timer trang trí.
- Hai cột khoảng 7:4. Cột trái có khung dán dữ liệu rồi **Danh sách điện thoại**, số lượng ở badge riêng. Dán proxy và Amazon vẫn dùng đúng lệnh cũ.
- Mỗi máy là một thẻ riêng, bo góc, cách nhau 8 px logic. Ba vùng: icon/tên Máy 01/Profile, tiến độ, Tiếp tục/Dừng cạnh nhau. Có đường dọc ngăn nhận diện máy với tiến độ. Bỏ phần tóm tắt Amazon ở danh sách theo bố cục mẫu; dữ liệu gốc vẫn ở khung phải. Không thêm lại cột Proxy. Vẫn giữ đủ 12 thẻ để cuộn; máy ngoài mẻ ghi Chưa dùng.
- Máy chọn có nền lam nhạt, viền/vạch trái lam rõ; máy khác trắng hoặc xám nhẹ khi ngoài mẻ. Hover không thay trạng thái được chọn.
- Cột phải có tên máy, badge Profile và tiến độ ở đầu. Proxy, dán hàng Amazon, thông tin riêng phân nhóm bằng icon và đường mảnh. Đầy đủ tên, SĐT, mật khẩu, thẻ, URL OTP, host/port/user/pass và tên Profile; cuộn xuống để sửa các trường bên dưới. OTP vẫn chỉ hiện khi có mã như trước.
- Footer xanh ngọc nhạt; ba nút lớn Chạy xanh, Dừng đỏ, Mẻ mới trắng. Bật/khóa theo mã cũ. Dấu chấm phản ánh đang chạy hay đang nghỉ; thông báo footer gốc giữ nguyên.

### Chữ và tiến độ

Segoe UI trên Windows, face Semibold cho tiêu đề/tên máy/trạng thái. Tên máy 17, trạng thái 16; dữ liệu và nút 14–16 px logic. **Bước đang làm là thông tin ưu tiên:** mô tả trong danh sách 15 Semibold xanh than, bên phải 17 Semibold và giữ nguyên toàn bộ thông báo. Nhãn trạng thái dùng màu ngữ nghĩa và icon 16 px. Danh sách rút gọn thông báo dài, tooltip giữ đầy đủ; chọn máy luôn xem nguyên văn bên phải. Bỏ dòng lặp Chưa chạy nhưng không bỏ trạng thái gốc hay OTP khỏi dữ liệu.

29 icon Lucide 0.468.0, nét 1,75 px; thêm `layers-2`. PNG alpha được tô bằng Pillow đã có, không thêm dependency chạy thật. Các ô nhập bên phải cao 36 px logic; ô dán hàng loạt 42; nút từng máy 38; nút footer 48. Kích thước và cỡ chữ theo scaling ứng dụng. Không dùng CSS vì đây là CustomTkinter.

### Kích thước và cuộn

Mặc định mở gần kín màn hình, mốc tối đa 1840×960 px trên Full HD; màn thử 1536×864 mở phần nội dung 1504×760 px, chừa khung/title bar/thanh tác vụ. Đây là cỡ nhỏ hơn đã được người dùng chốt cùng bản hiện tại. Bản 1616×972 chỉ là cỡ cửa sổ đối chiếu bố cục, không dùng làm mặc định.

Giữ nguyên `SmoothScrollableFrame` ở hai cột và Settings: cuộn pixel 16 ms khi có thao tác, đáp ứng khoảng 45 ms, giữ delta nhỏ, đảo hướng từ vị trí đang thấy và ngắt khi kéo/click scrollbar. Không có timer cuộn khi đứng yên; tôn trọng tùy chọn animation Windows. Không thay cuộn Android hoặc quy tắc tìm US.

### Kiểm chứng và phạm vi

639 unittest toàn dự án PASS khi nghiệm thu bản chốt bằng `.venv/Scripts/python.exe -m unittest discover -s tests -q`. Đã kiểm tra focus, hover, pressed, disabled, tooltip và bố cục Tk bằng dữ liệu giả. So AST với mốc 4667831: 55 phương thức Window giữ nguyên; ngoài phần trình bày, hai phương thức kiểm tra mật khẩu chỉ bỏ ngưỡng 8 ký tự theo yêu cầu. Parser nhận đủ ba hàng in đậm, giữ ánh xạ SĐT/mật khẩu/tên/thẻ/URL; mật khẩu ngắn được chuyển nguyên văn. Quyết định quyền chạy, Dừng/Tiếp tục/chỉnh sửa và logic lưu Settings khớp mốc. Không gọi tạo/Start/sửa Profile thật trong kiểm thử.

Scale ứng dụng 100/125/150%, chọn Máy 12, thông báo dài, sáu loại trạng thái, dữ liệu trống/3/12 hàng, cuộn và Settings đã được xem thử. Ở 125% mặc định: bảng yêu cầu tối đa 897 px trong 913 px; chi tiết 499 trong 507 px. Ở 150% nhãn đổi wrap, nút cùng hàng, không tràn ngang trong bài kiểm tra. Màn thấp/DPI lớn cần cuộn, không ép đủ 12 máy. Không đổi DPI toàn Windows hoặc đóng/reset phiên tool thật.

Ảnh `assets/ui_history/v3_contrast_before.png` là mốc trước đợt sửa; `v3_final.png` là cửa sổ gần kín màn hình, `v3_reference_layout.png` là đối chiếu lớn 1616×972, `v3_reference_ready.png` cho thấy nút Chạy khả dụng. Tất cả ảnh thử dùng dữ liệu giả. Gradient, bóng mềm và tile icon của mockup được chuyển thành màu phẳng/Canvas nhẹ trong Tk; không tuyên bố khớp pixel tuyệt đối. Phiên tool đang mở không tự nạp mã, dữ liệu phiên thật được giữ nguyên.

### Tự rà soát chín tiêu chí

Các điểm số V3 cũ không còn dùng làm kết luận sau phản hồi thực tế của người dùng.

| Tiêu chí | Kết quả quan sát | Giới hạn |
|---|---|---|
| Phối màu | Màu nền dịu, lam/lá/cam/đỏ phân vai rõ | Đã được chốt; chưa đo sử dụng nhiều giờ |
| Dễ nhìn | Bước hiện tại đậm, tương phản chữ đã đo | Màn thấp phải cuộn |
| Hiện đại | Thẻ tách rời, badge và hai cột đúng mẫu | Bóng/gradient giản lược cho Tk |
| Icon | Một bộ nét, icon nhóm đúng chức năng | Tile điện thoại đơn giản hơn ảnh |
| Phân cấp | Tiến độ ưu tiên trước dữ liệu sửa | Thông báo dài còn cần tooltip/khung phải |
| Font | Segoe UI/Semibold và scaling nhất quán | Chưa thử font fallback ngoài Windows |
| Bố cục | Nút hai bên không dính, dữ liệu sửa đầy đủ | Không cố nhét mọi trường vào màn đầu |
| Nhất quán | Tokens, màu chức năng và hệ chữ chung | Nút khóa vẫn theo trạng thái thật |
| Cảm giác hoàn thiện | Có bản xem thử thật và ảnh đối chiếu | Đã được chốt; chưa đo vận hành nhiều giờ |

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
