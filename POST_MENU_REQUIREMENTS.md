# Quy tắc tự động hóa sau menu ba gạch

Phạm vi mới bắt đầu **sau** khi từng máy đã xác nhận `MENU_OPEN`. Luồng tạo Profile, Start, cài Amazon và mở menu hiện có được giữ nguyên. Các thao tác Amazon tiếp theo sẽ được bổ sung theo hướng dẫn màn hình của người dùng.

Người dùng đã thay yêu cầu b1–b3: cả q1–q12 chọn ba mục bấm ngẫu nhiên trên menu thật ở mỗi mẻ, không còn chuỗi cố định theo máy. Các ảnh và file q1–q6 ghi lại lịch sử trước thay đổi. Từ b4 Sign In tới b11 OTP SMS và bấm tạo tài khoản vẫn là cùng một luồng cho q1–q12. Mỗi máy vẫn có SĐT, tên, thẻ, URL OTP, trạng thái gửi mã và điểm dừng/tiếp tục riêng. Thẻ hiện chỉ được giữ theo hàng, chưa sử dụng trong b1–b11.

Trước b1, mỗi máy đọc cây UI Amazon theo serial của mình. Menu dạng thẻ và dạng danh sách đều chạy ba lượt bấm ngẫu nhiên từ các mục đang hiện rồi nối b4. Nhánh Home → b4 cũ chỉ còn trong mã factory cố định làm tham chiếu. Không dùng tọa độ ảnh. Nếu b1–b3 không có mục bấm rõ, báo trạng thái và để b4 tự kiểm tra menu/form. Xem [MENU_ROUTING.md](MENU_ROUTING.md).

## Nhận diện giao diện lúc chạy

- Ảnh người dùng gửi là ví dụ để xác định luồng, **không phải tọa độ cố định** cho các lần chạy. Trước mỗi thao tác, tool đọc lại cây giao diện Android của đúng ADB serial/profile và xác định màn hình hiện tại.
- Với mỗi màn hình được hướng dẫn, chuẩn bị nhiều cách nhận diện theo thứ tự ưu tiên: `resource-id` hoặc `content-desc` ổn định; nhãn chữ cùng loại phần tử và quan hệ với ô nhập; cuối cùng là vùng bấm lấy từ cây giao diện hiện tại. Chỉ dùng ảnh/OCR làm phương án bổ trợ nếu cây giao diện không đủ thông tin và đã kiểm chứng trên máy thật.
- Một màn hình có thể có nhiều biến thể hợp lệ. Mỗi biến thể phải có dấu hiệu nhận diện riêng và cùng một kết quả cần xác minh. Sau khi bấm/gõ, tool đọc lại giao diện để xác nhận đã sang đúng bước hoặc giá trị ô nhập đã đúng.
- Nếu Amazon đổi bố cục nhưng vẫn nhận diện được biến thể đã kiểm chứng, tool tiếp tục. Nếu màn hình lạ, phần tử không duy nhất hoặc kết quả sau thao tác không rõ, tool dừng **chỉ máy đó** ngay tại màn hình hiện tại. Nút **Tiếp tục** đọc lại màn hình mới sau khi người dùng sửa, rồi chọn bước phù hợp; không bấm lại theo tọa độ cũ.
- Không có thời hạn tổng cho luồng sau menu. Mỗi lệnh ADB, đọc giao diện và lượt đọc OTP có timeout riêng; khi hết một lượt OTP, tự mở lại cho tới khi nhận mã mới hoặc người dùng bấm Dừng.

## Từng máy độc lập

- Máy q1 đến q12 có `RunJob`, dữ liệu Amazon/URL OTP, tiến trình và bước hiện tại riêng. Một máy lỗi không dừng các máy khác.
- Nút **Dừng Máy N sau bước hiện tại** trong khung chi tiết đặt cờ cho đúng máy đang chọn. Máy hoàn tất thao tác hiện hành rồi tạm dừng trước bước sau; nếu bước hiện hành lỗi và đang thử lại, máy dừng ở ranh giới lần thử. **Tiếp tục** dùng lại đúng phiên và điểm dừng của máy đó. Nút **Dừng cả mẻ** vẫn dùng cờ chung cho toàn mẻ. Không nút nào tự tắt Profile Swarmote.
- Sau khi xác nhận menu ba gạch (`MENU_OPEN`), mỗi máy chạy liên tục từ b1 đến các bước đã được cấu hình, không có đồng hồ tổng 3/4/5 phút. Xong một bước đã xác nhận thì tự chạy bước tiếp theo. Lỗi đọc tạm thời và lượt lấy OTP chưa có mã được thử lại; nút Dừng vẫn ngắt máy đó.
- Mỗi lời gọi ADB, đọc UI và lượt mở trang OTP vẫn có timeout ngắn để phát hiện một lần gọi bị treo rồi đọc/thử lại. Lỗi dữ liệu, sai serial hoặc thao tác gửi SMS/Create không chắc kết quả vẫn phải kiểm tra trạng thái trước khi tiếp tục.

## Nhập liệu và lỗi

- Dữ liệu được **gõ từng ký tự** vào Android; không dùng clipboard, paste hoặc đưa cả chuỗi vào một lệnh nhập. Bước nhập phải kiểm tra lại nội dung trường trước khi gửi form.
- Hàm gõ hiện hỗ trợ ký tự ASCII in được. Nếu gặp ký tự ngoài tập này, nó dừng trước khi gõ để người dùng sửa trực tiếp; cách gõ Unicode sẽ được xác minh trên máy thật khi xây từng màn hình.
- Lỗi đọc/nhận diện tạm thời được thử lại trên đúng máy. Lỗi dữ liệu hoặc kết quả thao tác không thể xác nhận mới tạm dừng, giữ màn hiện tại và hiển thị bước/lý do ở đúng hàng.
- Bước sau menu đọc trạng thái màn hình trước thao tác; nếu màn đang tải/đọc lỗi tạm thời thì tự chờ và đọc lại cùng máy. Nếu người dùng bấm **Tiếp tục**, tool nối từ bước đang dừng sau khi đọc lại màn. SMS/Create không được gửi lại mù khi kết quả lần trước chưa rõ.
- Nếu có CAPTCHA hoặc màn hình Amazon không nhận diện được, áp dụng cùng cơ chế dừng và tiếp tục; không đoán vị trí nút.

## Trạng thái hiện tại của dự án

`amazon_android/post_menu.py` giữ phiên riêng từng máy, cơ chế dừng/tiếp tục đúng bước và hàm gõ từng ký tự. Giao diện đã nối nút **Tiếp tục** tới phiên sau menu khi phiên đó tạm dừng. `amazon_android/random_prefix.py` giữ ba lượt bấm ngẫu nhiên cho cả 12 máy; `account_flow.py` giữ nhận diện UI và `build_common_steps` cho b4–b11. Các file `q1_flow.py` đến `q6_flow.py` ghi lại luồng cố định cũ, không còn là factory đang chạy. Mỗi máy tạo trạng thái OTP riêng. Màn sau nút `Create your Amazon account` chưa được hướng dẫn nên trạng thái hiện chỉ nói đã xong các bước b1–b11, không khẳng định tạo tài khoản thành công.

Trạng thái sau menu chỉ giữ trong bộ nhớ phiên. **Làm lại / mẻ mới** xóa chúng cùng dữ liệu của các hàng trong tool.

