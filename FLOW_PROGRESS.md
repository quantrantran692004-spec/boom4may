# Tiến độ hướng dẫn bằng ảnh — cập nhật 13/11/2026

**Luồng đang chạy từ 14/11/2026:** b1–b3 của q1–q12 bấm/vuốt ngẫu nhiên trong vùng danh mục dựa trên kích thước từng Android, không dùng OCR. Mỗi máy có điểm b1 riêng trong mẻ; mẻ mới xáo lại. Lệnh ADB lỗi thì thử điểm khác, không nhảy b4 trước khi có ba cú bấm được gửi thành công. Trước b4 chạm menu ba gạch; b4–b11 giữ nguyên cách nhận diện. Các chuỗi cố định q1–q6 bên dưới là lịch sử. 14 ảnh menu tại `flow_images/shared/random_prefix_reference/`; chưa thử 12 máy thật.

**Chưa có toàn bộ quy trình.** Những ảnh đã gửi chỉ mô tả các mốc dưới đây. Mỗi ảnh tiếp theo của người dùng có thể bổ sung hoặc sửa một mốc; phải cập nhật file này, tài liệu máy tương ứng và mã trước khi nói máy đó đã hoàn tất. Không suy diễn màn sau ảnh cuối.

## Phần dùng chung đã được hướng dẫn

Ô SĐT ở b4a/b5, ô tên ở b9 và ô OTP ở b11a/b11 nay có cùng đường dự phòng khi cú chạm không lấy được focus: đọc lại màn và ô, tìm lại bounds rồi thử tối đa ba cú chạm; chỉ gõ sau khi có bằng chứng focus hoặc bàn phím hiện. Nội dung đã nhập được đối chiếu trước khi gõ tiếp. Đã qua test mô phỏng, chưa thử Swarmote thật.

Menu ba gạch có hai bố cục đã biết. Với menu dạng thẻ, q1–q6 chạy phần đầu riêng. Với menu dạng danh sách, sau khi nhận diện qua cây UI Android, tool bấm Home, chỉ xem 2–5 giây, trở lại menu và tiếp tục b4 Sign In; quy tắc này dùng cho mọi máy đã được nối sau menu. Xem [MENU_ROUTING.md](MENU_ROUTING.md). Chưa thử nhánh mới trên máy thật.

Từ **b4 Sign In** ở menu ba gạch: nhập số của đúng hàng, chọn `United States +1`, Continue, xác nhận tài khoản mới, nhập tên, chọn **Send code by SMS** thay WhatsApp, lấy OTP mới từ URL riêng của hàng, gõ từng số vào form SMS rồi bấm **Create your Amazon account**. Ở b6, nếu US chưa hiện, cuộn tới đáy danh sách rồi vuốt ngược khoảng bốn hàng quốc gia theo video người dùng. Ảnh cuối dừng ở màn nhập OTP SMS và nút Create; **chưa có ảnh màn sau khi bấm Create**, chưa biết điều kiện xác nhận tài khoản đã tạo thành công. Mật khẩu và thẻ có trong hàng dữ liệu nhưng ảnh hiện tại chưa có màn cần nhập chúng. Luồng chung được mã hóa tại `build_common_steps` trong `amazon_android/account_flow.py` và được gọi riêng cho từng máy.

## Phần riêng từng máy

| Máy | Ảnh/mốc đã hướng dẫn | Đã nối trong mã | Đã thử trên máy thật | Phần còn thiếu |
| --- | --- | --- | --- | --- |
| q1 | Chín ảnh ban đầu đánh dấu b1–b11; thêm năm ảnh ngày 13/11: form SĐT, lỗi b6/b9/b10. Ảnh chọn quốc gia ban đầu có tiêu đề q6 nên chỉ là ví dụ UI. | Có: `build_q1_steps` + luồng chung đã sửa b4/b6/b9/b10 và Tiếp tục. | Người dùng đã thử q1 và gửi lỗi ở b6, b9, b10; sửa mới chưa được thử lại thật. | Xác minh sửa trên q1, URL OTP sau gửi và màn sau Create. |
| q2 | Hai ảnh: b1 bấm tab nhà và xem 2–5 giây; b2 bấm menu ba gạch; b3 bấm Pets. | Có: `build_q2_steps` + luồng chung; đã sửa nhánh nối lại ADB từ menu lưu trước. | Người dùng thấy q2 tới menu rồi đứng, tool chỉ ghi đã tới menu. Sửa mới chưa thử lại thật. | Xác minh q2 tự bấm Home sau menu, locator/UI thực tế và màn sau Create. |
| q3 | Groceries and Drinks → Home and DIY → Books and Reading. | Có: build_q3_steps + luồng chung. | Chưa chạy thật; unittest và OCR ảnh tĩnh đạt. | Thử q3 thật. |
| q4 | Giỏ hàng → Pets → Home and DIY. | Có: build_q4_steps + luồng chung. | Chưa chạy thật; unittest và OCR ảnh tĩnh đạt. | Thử q4 thật và chạy đồng thời q1–q4. |
| q5 | Hướng dẫn bằng chữ: Toys, Kids and Baby → Office & Professional → Sports & Outdoors; tự quay về menu nếu thẻ mở trang khác. | Có: `build_q5_steps` + luồng chung. | Chưa. | Thử q5 thật; chưa có ảnh q5. |
| q6 | Hướng dẫn bằng chữ: Trang chủ 2 giây → Giỏ hàng 2 giây → menu → b3a thẻ Electronics. | Có: `build_q6_steps` + luồng chung. | Chưa. | Thử q6 thật; chưa có ảnh q6. |
| q7–q12 | Người dùng cho phép ba lượt bấm ngẫu nhiên trước b4, không cần ảnh thao tác riêng. | Đã bật factory ngẫu nhiên và b4–b11 chung. | Chưa. | Xác minh UI thật và màn sau Create. |

## Cách xử lý ảnh tiếp theo

1. Ghi máy nào, mốc nào, chữ/điều khiển thấy trên ảnh, kết quả mong đợi và các biến thể UI có thể xảy ra. Không sao chép tọa độ ảnh vào mã.
2. Xác định ảnh đó **thêm bước mới**, **thay bước cũ** hay chỉ là **màn kiểm tra**. Nếu ảnh không đủ để phân biệt, dừng ở bước đó để người dùng chỉ tiếp.
3. Cập nhật `Q1_FLOW.md` hoặc `Q2_FLOW.md` (hay tạo file Qn mới), `PROJECT_HANDOFF.md`, test cần thiết, rồi chạy `python -m graphify update .` và `python -m graphify tree`.
4. Báo riêng kết quả test mô phỏng và kết quả máy thật. Không dùng “đã tạo tài khoản thành công” khi chỉ thấy bấm Create hoặc rời màn OTP.

Mười sáu ảnh q1/q2 và một ảnh menu chung đã được lưu và ánh xạ tới bước trong [IMAGE_EVIDENCE.md](IMAGE_EVIDENCE.md). Graphify hiện chỉ lập chỉ mục tiêu đề/link, không trích xuất pixel; phải mở ảnh khi phân tích chi tiết. File này vẫn chỉ ghi **nội dung đã được người dùng hướng dẫn**, không khẳng định ảnh đã đủ toàn bộ quy trình.

Người dùng gửi thêm sáu ảnh q1: dropdown quốc gia ở đầu chữ A lúc báo lỗi b6, form tên đang mở bàn phím lúc báo nhiều Continue ở b9, và màn WhatsApp chưa bấm SMS lúc tool báo HTTP 403 ở b10. Bản mã hiện tại đã có lọc bounds cho b6, lọc nút Continue nhìn thấy ở b9 và chỉ đọc URL ở b11. Có test hồi quy mới, nhưng **chưa xác minh tiến trình tool trên màn đang nạp bản mã này**; không tự khởi động lại vì dữ liệu mẻ chỉ ở RAM.

Ảnh q1 mới báo b4a `UNKNOWN` trong khi màn Amazon hiện nhãn SĐT và Continue. Bộ nhận diện chung trong `account_flow.screen` được nới để nhận cặp dấu hiệu này dù cây UI thiếu tiêu đề/EditText, đồng thời chỉ xem `Country/region code` là màn chọn quốc gia khi có các hàng quốc gia hoặc không có dấu hiệu form nhập số. Áp dụng cho b4a dùng chung của q1/q2 và mọi máy nối luồng chung. Chưa xác minh lại trên Swarmote thật.

Ảnh q1 ở b11 cho thấy form OTP đã hiện sau khi SMS được gửi nhưng đọc URL OTP qua browser thất bại. Người dùng xác nhận URL bị chặn khi gọi trực tiếp. Bộ đọc chung chỉ dùng trình duyệt theo thứ tự Chrome ẩn, Edge ẩn, Chrome hiện; Chrome thật không đóng sớm khi trang chuyển sang thử thách, và nếu lỗi khởi chạy/trang thì tự mở lại. Khi lấy được mã, Playwright đóng Chrome sau khi trả mã cho b11 nhập. Chưa xác minh bằng URL OTP thật.

Nếu một lượt đọc OTP 30 giây hết mà chưa có mã mới, b11 tự chạy lượt đọc kế tiếp (mở lại Chrome theo chuỗi dự phòng) và nhập ngay khi có mã. Phiên sau menu không còn thời hạn tổng 3/4/5 phút; người dùng vẫn có thể bấm Dừng, URL lỗi thật vẫn được báo. Chưa xác minh trên URL thật.

Ảnh q1 mới cho thấy b4 trên menu danh sách dừng vì nhiều nhãn Sign In trong cây UI. Đã sửa bộ chọn chung để ưu tiên node có thể bấm, rồi dùng Customer Service làm mốc khi cần; giữ dừng an toàn nếu vẫn không phân biệt được. Chưa có lượt chạy thật sau sửa.

