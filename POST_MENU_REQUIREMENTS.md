# Quy tắc tự động hóa sau menu ba gạch

Phạm vi mới bắt đầu **sau** khi từng máy đã xác nhận `MENU_OPEN`. Luồng tạo Profile, Start, cài Amazon và mở menu hiện có được giữ nguyên. Các thao tác Amazon tiếp theo sẽ được bổ sung theo hướng dẫn màn hình của người dùng.

Người dùng hướng dẫn bằng ảnh màn hình từng máy, đã có **q1–q4** và hướng dẫn bằng chữ cho q5/q6. Với mỗi ảnh, cần xác định trạng thái màn hình, phân tích nhiều cách định vị và thao tác, chọn cách có thể kiểm tra kết quả, đồng thời tính đến lỗi thường gặp. **Chỉ phần trước b4 khác nhau theo máy (q6 có thêm b3a); từ b4 Sign In tới b11 OTP SMS và bấm tạo tài khoản là cùng một luồng cho q1–q12.** Mỗi máy vẫn có SĐT, tên, thẻ, URL OTP, trạng thái gửi mã, đồng hồ và điểm dừng/tiếp tục riêng. Thẻ hiện chỉ được giữ theo hàng, chưa sử dụng trong b1–b11. q7–q12 chỉ được nối sau khi người dùng hướng dẫn b1–b3 của từng máy.

Trước b1, bộ định tuyến đọc cây UI Amazon của từng máy để phân biệt menu dạng thẻ và dạng danh sách chữ. Dạng danh sách đi Home, **chỉ xem 2–5 giây**, về menu và chạy thẳng b4 Sign In; dạng thẻ chạy b1–b3 riêng. Không viết bộ thao tác riêng cho từng ảnh, không dùng tọa độ ảnh. Khi chưa phân loại được màn, dừng để người dùng sửa rồi Tiếp tục. Xem [MENU_ROUTING.md](MENU_ROUTING.md).

## Nhận diện giao diện lúc chạy

- Ảnh người dùng gửi là ví dụ để xác định luồng, **không phải tọa độ cố định** cho các lần chạy. Trước mỗi thao tác, tool đọc lại cây giao diện Android của đúng ADB serial/profile và xác định màn hình hiện tại.
- Với mỗi màn hình được hướng dẫn, chuẩn bị nhiều cách nhận diện theo thứ tự ưu tiên: `resource-id` hoặc `content-desc` ổn định; nhãn chữ cùng loại phần tử và quan hệ với ô nhập; cuối cùng là vùng bấm lấy từ cây giao diện hiện tại. Chỉ dùng ảnh/OCR làm phương án bổ trợ nếu cây giao diện không đủ thông tin và đã kiểm chứng trên máy thật.
- Một màn hình có thể có nhiều biến thể hợp lệ. Mỗi biến thể phải có dấu hiệu nhận diện riêng và cùng một kết quả cần xác minh. Sau khi bấm/gõ, tool đọc lại giao diện để xác nhận đã sang đúng bước hoặc giá trị ô nhập đã đúng.
- Nếu Amazon đổi bố cục nhưng vẫn nhận diện được biến thể đã kiểm chứng, tool tiếp tục. Nếu màn hình lạ, phần tử không duy nhất hoặc kết quả sau thao tác không rõ, tool dừng **chỉ máy đó** ngay tại màn hình hiện tại. Nút **Tiếp tục** đọc lại màn hình mới sau khi người dùng sửa, rồi chọn bước phù hợp; không bấm lại theo tọa độ cũ.
- Không có thời hạn tổng cho luồng sau menu. Mỗi lệnh ADB, đọc giao diện và lượt đọc OTP có timeout riêng; khi hết một lượt OTP, tự mở lại cho tới khi nhận mã mới hoặc người dùng bấm Dừng.

## Từng máy độc lập

- Máy q1 đến q12 có `RunJob`, dữ liệu Amazon/URL OTP, tiến trình và bước hiện tại riêng. Một máy lỗi không dừng các máy khác.
- Sau khi xác nhận menu ba gạch (`MENU_OPEN`), mỗi máy chạy liên tục từ b1 đến các bước đã được cấu hình, không có đồng hồ tổng 3/4/5 phút. Xong một bước đã xác nhận thì tự chạy bước tiếp theo. Lỗi đọc tạm thời và lượt lấy OTP chưa có mã được thử lại; nút Dừng vẫn ngắt máy đó.
- Mỗi lời gọi ADB, đọc UI và lượt mở trang OTP vẫn có timeout ngắn để phát hiện một lần gọi bị treo rồi đọc/thử lại. Lỗi dữ liệu, sai serial hoặc thao tác gửi SMS/Create không chắc kết quả vẫn phải kiểm tra trạng thái trước khi tiếp tục.

## Nhập liệu và lỗi

- Dữ liệu được **gõ từng ký tự** vào Android; không dùng clipboard, paste hoặc đưa cả chuỗi vào một lệnh nhập. Bước nhập phải kiểm tra lại nội dung trường trước khi gửi form.
- Hàm gõ hiện hỗ trợ ký tự ASCII in được. Nếu gặp ký tự ngoài tập này, nó dừng trước khi gõ để người dùng sửa trực tiếp; cách gõ Unicode sẽ được xác minh trên máy thật khi xây từng màn hình.
- Lỗi đọc/nhận diện tạm thời được thử lại trên đúng máy. Lỗi dữ liệu hoặc kết quả thao tác không thể xác nhận mới tạm dừng, giữ màn hiện tại và hiển thị bước/lý do ở đúng hàng.
- Bước sau menu đọc trạng thái màn hình trước thao tác; nếu màn đang tải/đọc lỗi tạm thời thì tự chờ và đọc lại cùng máy. Nếu người dùng bấm **Tiếp tục**, tool nối từ bước đang dừng sau khi đọc lại màn. SMS/Create không được gửi lại mù khi kết quả lần trước chưa rõ.
- Nếu có CAPTCHA hoặc màn hình Amazon không nhận diện được, áp dụng cùng cơ chế dừng và tiếp tục; không đoán vị trí nút.

## Trạng thái hiện tại của dự án

`amazon_android/post_menu.py` giữ phiên riêng từng máy, cơ chế dừng/tiếp tục đúng bước và hàm gõ từng ký tự. Giao diện đã nối nút **Tiếp tục** tới phiên sau menu khi phiên đó tạm dừng. `amazon_android/account_flow.py` giữ nhận diện UI và `build_common_steps` cho b4–b11; `q1_flow.py` đến `q6_flow.py` chỉ giữ b1–b3 riêng rồi gọi hàm chung. Mỗi máy tạo trạng thái OTP riêng. q1–q4 đã được nối theo ảnh, gồm chọn SMS thay WhatsApp, lấy mã từ URL cùng hàng và gõ vào ô OTP. q7–q12 vẫn dừng ở menu, chờ b1–b3 riêng của từng máy. Màn sau nút `Create your Amazon account` chưa được hướng dẫn nên trạng thái hiện chỉ nói đã xong các bước b1–b11, không khẳng định tạo tài khoản thành công.

Trạng thái sau menu chỉ giữ trong bộ nhớ phiên. **Làm lại / mẻ mới** xóa chúng cùng dữ liệu của các hàng trong tool.

