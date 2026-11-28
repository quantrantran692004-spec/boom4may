# Danh mục từng bước đã biết — 13/11/2026

> Mục này mô tả hành vi từng bước. Bản đồ duy nhất từ bước sang file mã, trạng thái và test ở mục “Một quy luật để sửa mã về sau” trong [PROJECT_INDEX.md](PROJECT_INDEX.md). Các đoạn có ngày cũ là lịch sử; đối chiếu mã và mục cập nhật mới nhất trước khi sửa.

**Trạng thái do người dùng báo 17/11/2026:** b1–b3 ngẫu nhiên đã ổn ở Máy 1–6;
Máy 7 dùng bản thử riêng và dừng tại b4; Máy 8–12 chưa có b1–b3 và chưa nối
b4–b11 trong phiên đang dùng. Checkout đã khai báo factory/bước chung cho
slot 8–12 và có test mô phỏng, nhưng chưa có xác nhận trên máy thật hoặc bằng
chứng phiên tool hiện hành nạp mã đó. Không đánh dấu Máy 8–12 hoàn tất.

## Bản thử q7 State Machine — 14/11/2026

Q7 từng dùng bản thử nhận diện, kiểm tra và xác minh màn b4–b11. Từ
26/11/2026, factory Máy 7 dùng toàn bộ `random_prefix.build_random_steps`
như 11 máy còn lại: b1–b3 chọn thẻ hoặc mục con, xem 3–5 giây; b1/b2
cuộn một lần sau cú bấm 2 giây, b3 không cuộn; b4–b11 dùng cùng `account_flow.build_common_steps`; b12 trở
đi cũng dùng chung. Quy tắc pilot thêm 30 giây, bắt buộc bấm mục con và lớp
State Machine riêng đều không chạy trong factory hiện hành. Lựa chọn ngẫu
nhiên, dữ liệu hàng và trạng thái Dừng/Tiếp tục vẫn tách riêng từng máy.
Xem [Q7_STATE_MACHINE_PILOT.md](Q7_STATE_MACHINE_PILOT.md).

## B1–B3 hiện hành — Ba lượt ngẫu nhiên q1–q12

**Luồng Settings “Đổi US từ đầu”, 28/11/2026:** Máy vẫn đi từ tạo Profile qua P01–P08 tới Amazon. Sau đó chạy b1 mở/xác nhận menu ba gạch và chờ đủ 4 giây; b2 bấm tab hình người; b3 tìm/bấm EN; b4 bấm Country/Region; b5 cuộn tìm United States; b6 chọn và xác nhận United States; b7 bấm Done rồi bấm ngay tab hình người khi thấy. Cập nhật b2 ngày 28/11/2026: bấm thẳng tab hình người ở vị trí thứ hai của thanh dưới theo kích thước Android đúng máy, không đọc nhãn, khớp ảnh hay kiểm tra màn trước cú bấm. B7 vẫn tìm tab sau Done theo điều kiện màn quốc gia đã rời. Các bước còn lại chỉ tìm mục tiêu của chính bước, không chốt loại màn đầu vào hoặc tự nhảy bước. Dấu chờ b1, chọn US và Done giữ riêng từng máy qua Dừng/Tiếp tục; thiếu mục tiêu/lỗi đọc sau giới hạn thì dừng máy ở đúng bước. Sau b7, b8 chờ đủ 6 giây rồi bấm Create account dưới Sign in; b9 chạm ô và nhập SĐT đúng hàng; b10 bấm Continue dưới SĐT US +1; b11 bấm Proceed to create an account; b12 chạm ô First and last name; b13 nhập đúng tên rồi Continue; b14 chạm ô, lấy OTP từ URL cùng hàng và nhập mã; b15 xác nhận mã trong ô rồi bấm Create your Amazon account; b16 Back khi thấy hộp Google che màn, đọc lại và tự Back lần hai nếu hộp vẫn còn (kể cả bản tiếng Anh), tối đa hai lần rồi xác nhận hộp đã ẩn; b17 bấm Create a passkey trên màn Account created. Chỉ cần proxy để bắt đầu, nhưng b9 phải có hàng Amazon của máy đó; thiếu thì PAUSED để bổ sung rồi Tiếp tục. Dấu Continue/Create/Back giữ riêng máy để không gửi lặp. Dừng sau b17, chưa suy diễn b18. Các quy tắc b1–b3 ngẫu nhiên bên dưới chỉ thuộc luồng Tạo/Đăng nhập hiện hành. Mã và test mô phỏng chưa chứng minh phiên tool đang mở đã nạp mã hoặc máy thật đã chạy.

**Nhịp cuộn hiện hành, sửa 26/11/2026:** B1/b2 chờ đủ 2 giây sau cú bấm rồi vuốt vừa từ dưới lên một lượt; b3 không vuốt, kể cả khi phải thử lại cú bấm lỗi. Cả ba bước của 12 máy đều xem 3–5 giây. Dừng/Tiếp tục giữ mốc chờ và dấu đã vuốt của b1/b2, không bấm hoặc cuộn lại. B13–b15 giữ quy tắc cuộn riêng của chúng. Đây là mã/test mô phỏng, chưa kiểm trên máy thật hoặc phiên tool đang mở.

**Nhịp vuốt 27/11/2026:** Giữ nguyên điểm đầu/cuối và một cú lướt liên tục của mã cũ; tăng thời gian cuộn xem b1/b2 từ 450 lên 700 ms và cú cuộn tìm hàng dự phòng từ 280 lên 700 ms. B3 vẫn không cuộn trong factory hiện hành. Bản q7 pilot cũ cũng chỉ đổi thời gian cú vuốt dự phòng; không nối pilot vào factory.

B1–b3 xem/bấm ngẫu nhiên các vùng danh mục theo kích thước Android của đúng máy, không cần OCR hay xác nhận màn đã đổi. Mỗi máy nhận điểm b1 riêng trong 12 điểm của mẻ; mẻ mới xáo lại. **Điều chỉnh 17/11:** b2/b3 chờ 0,6 giây sau khi mở menu; sau mỗi cú bấm xem mục 3–5 giây. Nếu Dừng khi đang xem, Tiếp tục chờ phần còn lại mà không bấm lặp. Lệnh bấm ADB lỗi thì thử điểm khác; b1/b2 có thể vuốt tìm hàng mới rồi tự thử lại cùng bước, b3 không vuốt; không có cú bấm nào thành công thì không chuyển b4. Trước b4 chạm menu ba gạch; b4–b11 giữ quy tắc nhận diện cũ. Các mốc q1–q6 cố định bên dưới là lịch sử. Ảnh tham chiếu ở [IMAGE_EVIDENCE.md](IMAGE_EVIDENCE.md); chưa thử trên 12 máy thật. **Cập nhật 18/11 theo lời nhắc mới:** B1–b3 chọn ngẫu nhiên cả thẻ và mục con đang hiện, giữ menu đang mở để mục con có thể được chọn ở lượt sau. Nếu cú bấm sang trang khác, vẫn xem đủ thời gian lượt đó, mở lại ba gạch cho lượt tiếp theo và chỉ tới b4 khi cả ba lượt đã hoàn tất. B4 luôn mở lại ba gạch trước Sign In. Sửa vòng phục hồi chậm ngày 18/11 theo ảnh Máy 4: giới hạn 12 giây cũ không có tác dụng vì gọi bộ đọc tự lặp. `_prefix_nodes` nay chỉ gọi một lượt đọc UI/OCR với ngân sách 6 giây của worker riêng; giữ đọc ảnh để chọn mục con, không dùng `_read_nodes` tự lặp. Khi sang trang khác, xem hết lượt rồi ưu tiên tab Browse đang hiện; thiếu nhãn thì dùng kích thước Android. Nếu Browse chưa đổi màn, Back một lần rồi mở lại ba gạch. Nếu mở ứng dụng ngoài thì Back, kiểm tra Amazon ở trước và bỏ locator cũ của ứng dụng ngoài. Không quay được về Amazon hoặc gặp form tài khoản thì dừng riêng máy đó, không vào vòng phục hồi vô hạn. Đọc không ra chữ thì giữ đường bấm theo kích thước cũ; vẫn đủ ba lượt xem 3–5 giây trước b4, giữ mốc Dừng/Tiếp tục. Từ 26/11, q7 dùng toàn bộ factory chung; giới hạn 90 giây thuộc bản thử cũ. B12–b15 cũng chọn mục con; khi sang trang khác thì mở lại ba gạch để tiếp tục các lượt còn lại. Không nhảy thẳng từ b1/b2 tới b4.

Tài liệu này là bản đồ từng mốc để phiên sau không coi ảnh chưa gửi là bước đã hoàn thành. Ảnh gốc q1/q2 đã lưu và ánh xạ tại [IMAGE_EVIDENCE.md](IMAGE_EVIDENCE.md); mở ảnh đó khi cần xem UI. `Đã nối mã` khác với `đã chạy thật`. Các bước được ghi từ hướng dẫn người dùng và mã hiện tại; không suy ra màn chưa có ảnh. Dữ liệu nhạy cảm không ghi vào file này.

## P01 — Dán và gán hàng dữ liệu

Dán 1–12 hàng `SĐT | Mật khẩu | Tên | Thẻ | URL OTP`. Cột trống, hàng gạch Markdown, thẻ có `\|` và link URL Markdown được nhận. Hàng n gắn Máy n, không tráo SĐT/URL. Thẻ và mật khẩu chỉ gắn dữ liệu, chưa dùng trong b1–b22. **Đã nối mã, đã test mô phỏng.**

**Sửa 27/11/2026:** Ô Markdown in đậm `**...**`/`__...__` được bỏ lớp định dạng trước khi kiểm tra, giữ đủ hàng đầu có dữ liệu nằm trên hàng gạch phân cách. Tab/CSV không bỏ dấu sao trong mật khẩu. Test bảng giả ba hàng và đường phân bổ UI xác nhận Máy 1–3 đúng SĐT/mật khẩu/tên/thẻ/URL và số máy bằng 3; chưa nạp vào phiên tool đang mở.

**Mật khẩu, 27/11/2026:** Bỏ yêu cầu tối thiểu 8 ký tự theo người dùng ở parser, kiểm tra mẻ, dữ liệu từng máy và form đăng ký. Mật khẩu ngắn được chuyển nguyên văn; vẫn không nhận rỗng hoặc ký tự ngoài ASCII không khoảng trắng. 81 test liên quan PASS bằng dữ liệu giả/mock, chưa nạp vào phiên tool đang mở.

**Cập nhật 17/11:** Hai ô dán nhanh Proxy/Thông tin Amazon tự nhận loại hàng từ clipboard, nên dán vào ô nào cũng phân bổ Proxy và hàng Amazon hợp lệ vào đúng nhóm. Dòng ghi chú, cột thừa, thẻ sai dạng và URL không hợp lệ ở cột thừa được bỏ; chỉ hàng Amazon có đủ SĐT, mật khẩu, tên và một URL OTP hợp lệ mới được giữ. URL trùng giữa các hàng chỉ nhận lần đầu; nếu một hàng chứa nhiều URL OTP hợp lệ khác nhau thì bỏ hàng đó để không gán nhầm máy. Dữ liệu được gán theo thứ tự các hàng hợp lệ, tối đa 12 máy và 100 proxy; phần proxy vượt 12 máy vẫn là dự phòng. Chưa thử thao tác dán trên cửa sổ đang chạy.

**Sửa từng máy sau lỗi tạo Profile, 21/11/2026:** Khi mẻ đã khóa, ô dán hàng loạt vẫn không ghi đè 12 máy. Chọn đúng máy có Profile chưa tạo và lỗi/đã dừng, dán một proxy vào ô máy đó hoặc sửa Host/Port/User/Pass, SĐT/Mật khẩu/Tên/Thẻ/URL OTP ngay trong khung chi tiết. Các máy đã có Device ID hoặc kết quả Create chưa chắc chắn không mở sửa proxy. Bấm Tiếp tục sau khi nhập xong để kiểm tra và cập nhật tác vụ riêng của máy đó; không tráo hàng với máy khác. Nếu máy đã chờ tạo lại, thao tác bắt đầu sửa hủy lượt chờ cũ để không dùng dữ liệu đang nhập dở. Đây là mã và test mô phỏng, chưa thử trên phiên tool đang mở.

**Cập nhật 23/11/2026; rà soát dán 26/11:** Khung máy đang chọn có nút xóa riêng proxy, hàng Amazon và OTP tạm trong RAM; tên Profile và các máy khác giữ nguyên. Ô một hàng nhận `SĐT | Mật khẩu | Tên | Thẻ | URL OTP` (thẻ có thể trống) rồi điền vào đúng máy đã chọn; nay cũng nhận hàng tab/CSV có cột thừa, giữ hàng ngăn bằng `|` như trước. Với mẻ đã khóa, chỉ máy lỗi/dừng trước Create và chưa có Device ID mới cho xóa hoặc thay hàng. Bấm Tiếp tục sau khi nhập đủ để tạo lại ngay; hai lượt tạo Profile dùng chung khóa cửa sổ Swarmote, không đợi kết thúc cả mẻ. Đây là mã và test mô phỏng; cửa sổ đang mở chưa nạp thay đổi.

## P02 — Kiểm tra proxy và tên Profile

Mỗi máy cần proxy tương ứng khi tạo profile mới. Tool kiểm tra tên qN đã tồn tại hay chưa; không tạo trùng hoặc tự đổi tên. Trên danh sách một trang, không gõ qN vào ô lọc chỉ để xác định vắng. **Đã nối mã; q1–q3 được thấy có sẵn ngày 13/11/2026. Chính sách dùng lại hay đặt tên mới còn chờ người dùng.**

## P03 — Mở form New Profile

Đưa cửa sổ quản lý Swarmote lên trước, bấm **New Profile**, xác nhận form có Create, Single Create, Profile Name, ip/Host trước khi điền. Nếu form không mở, dừng; không điền vào ô tìm kiếm Profile Name. **Đã thử trực tiếp mở form rồi Cancel; chưa gửi Create trong thử nghiệm mới.**

Theo lỗi focus người dùng gửi ngày 21/11/2026: khi Windows chưa đưa được cửa sổ quản lý lên trước, thử lại kích hoạt ba lượt ngắn và UIA `set_focus`; nếu vẫn lỗi trước khi gửi Create, runner thử lại đúng máy tối đa ba lượt trước khi chuyển máy khác. Mỗi lượt vẫn xác nhận form trước khi điền. Test mô phỏng đạt, chưa thử trên Swarmote thật; phiên đang mở không tự nạp mã mới.

Nút Tiếp tục cho lỗi trước Create: nếu registry của máy là `RESERVED/ERROR` hoặc `RESERVED/STOPPED`, chưa có Device ID thì gọi lại đường tạo Profile ngay cả khi mẻ còn chạy (sửa 23/11/2026). Khóa tạo Profile nối tiếp các thao tác trên cùng cửa sổ quản lý. Trạng thái `UNCERTAIN` hoặc đã gửi Create không được tạo lặp. Trước đây nhánh Tiếp tục đi sai vào `retry_preparation` chỉ dành cho máy đã có Device ID; đã sửa và test mô phỏng.

Sau khi sửa riêng proxy/thông tin của máy `RESERVED/ERROR` hoặc `RESERVED/STOPPED`, Tiếp tục tạo `RunJob` mới cho đúng máy từ các ô đang hiện, kiểm tra proxy và URL OTP, bỏ danh sách proxy dự phòng cũ nếu proxy chính đã đổi. Dữ liệu máy khác và tên Profile đã cấp giữ nguyên. Nếu dữ liệu chưa hợp lệ thì không xếp lại lượt tạo.

## P04 — Điền Single Create và Custom proxy

Chọn Single Create và Custom; điền tên Profile, host, port, tài khoản và mật khẩu proxy bằng UIA vào form đã xác nhận. **Đã nối mã; chưa kiểm thử lại toàn bộ sau sửa New Profile.**

## P05 — Test Proxy rồi Create

Bấm Test Proxy; chỉ khi hiện Test Passed **và** Country của kết quả là United States (US) mới bấm Create. Country khác US hoặc không đọc được Country được coi là proxy không đạt, giữ Create chưa gửi và dùng đường proxy dự phòng hiện có. Nếu form còn kết quả Test Proxy của lần trước, đóng bằng Cancel rồi mở form mới trước khi điền/thử proxy tiếp theo. Test Failed mới vẫn dừng trước Create. Sau Create, xác nhận đúng tên Profile và Device ID; nếu kết quả không chắc chắn, dừng để tránh tạo trùng. **Đã nối mã và test mô phỏng; chưa gửi Create trên Swarmote thật sau sửa 28/11/2026.**

## P06 — Start điện thoại và chờ slot

**Xếp cửa sổ 26/11/2026:** Khi cửa sổ điện thoại mới xuất hiện, tool xếp các cửa sổ Swarmote đang hiện trên cùng màn hình theo thứ tự số máy. Chỉ di chuyển cửa sổ Windows khi đủ chỗ, thu nhỏ nếu nhiều cửa sổ không còn vừa màn hình; bước Start, Device ID, ADB và luồng Amazon giữ nguyên. Cửa sổ khác, cửa sổ quản lý và máy đã thu nhỏ không được đưa vào bố cục. Xếp lỗi không chặn P07. Đã kiểm thử mô phỏng, chưa xếp trên phiên người dùng đang mở.

**Sửa 26/11/2026:** Settings đặt N chỉ cho Máy 1–N tự Start khi Chạy mẻ; Profile của máy sau vẫn được tạo nhưng chờ người dùng bấm Tiếp tục. Máy trước Offline không tự mở máy kế tiếp. Nút Tiếp tục Start riêng đúng máy đã chọn, không tính vào N lượt tự Start; bộ điều phối không Start lại máy đó. Mỗi máy giữ Device ID riêng. Nếu nút Start chưa sẵn sàng trước khi gửi, đường tự Start của N máy đầu vẫn thử lại có hạn; lỗi sau khi đã gọi Start phải xác minh trạng thái, không gửi lặp. Đây là mã/test mô phỏng, chưa xác nhận phiên Swarmote đang mở đã nạp thay đổi.

## P07 — Mở Apps, tìm z và cài Amazon

Trên đúng cửa sổ máy, mở Apps/App Store, tìm `z`, cài Amazon Shopping và xác nhận package qua ADB. Nếu app đã cài thì tiếp tục, không cài lặp. Kết quả cài đặt giữ serial ADB và Device ID vừa xác nhận để P08 dùng ngay cho đúng máy, tránh mở lại Terminal/Apps. **Đã nối mã; một số máy cũ từng được kiểm tra thật, không suy ra máy mới.**

## P08 — Mở Amazon tới menu ba gạch

Ngay sau khi cài Amazon và nối ADB đúng serial, nếu panel App Store còn mở bên phải cửa sổ máy thì bấm Apps để thu gọn ngay. Sau đó mở Amazon, dùng ADB mở và xác nhận Browse menu. Không bấm Apps khi panel đã thu. Sửa thứ tự 26/11/2026 theo yêu cầu người dùng; đã test mô phỏng, chưa đo trên máy thật hoặc phiên tool đang mở.

Mở Amazon, nếu hiện Skip sign in thì gửi Back trên điện thoại một lần thay vì bấm Skip (sửa 20/11/2026), bấm Browse menu Tab và xác nhận `Shop by category`/menu. Đây là điểm nối luồng riêng từng máy. Nếu registry đã ghi `MENU_OPEN` từ lượt trước, phải nối lại ADB serial của đúng máy trước khi phát sự kiện để chạy b1. Nếu thiếu hàng Amazon hoặc serial, báo rõ ở hàng máy; nếu Offline, nhắc Start rồi Tiếp tục. **Đã sửa mã và test mô phỏng cho q1/q2; q2 chưa xác minh lại thật sau báo cáo đứng ở menu.**

## P08a — Nhận diện biến thể menu dạng danh sách

Sau P08, đọc menu Android trực tiếp của đúng máy. Cả menu dạng thẻ và danh sách chữ đều chạy đủ ba lượt bấm ngẫu nhiên trên thẻ hoặc mục con đang hiện có vùng hợp lệ rồi nối b4 Sign In; không dùng tọa độ ảnh. Mỗi lượt đọc có hạn 15 giây; menu tạm chưa rõ thì thử lại cùng bước, không bỏ lượt. B4 kiểm tra dấu hoàn tất b1–b3 trước khi thao tác. **Đã nối mã và test mô phỏng; chưa thử máy thật.** Xem [MENU_ROUTING.md](MENU_ROUTING.md).

## Q1 b1 — Bấm Gifting

Từ menu, tìm thẻ Gifting trong cây UI hiện tại, cuộn khi cần và bấm. Khi mở trang danh mục, quay lại menu trước bước kế. **Đã nối mã theo ảnh; chưa thử thật q1.**

## Q1 b2 — Bấm Pets

Tìm thẻ Pets trên menu, bấm và quay lại menu khi cần. **Đã nối mã theo ảnh; chưa thử thật q1.**

## Q1 b3 — Bấm Fashion and Beauty

Tìm thẻ Fashion and Beauty trên menu, bấm. Bước chung b4 sẽ đưa về menu trước Sign In. **Đã nối mã theo ảnh; chưa thử thật q1.**

## Q2 b1 — Bấm Home và xem 2–5 giây

Từ menu, bấm Home Tab ở thanh dưới. Xác nhận trang chủ bằng `Sign in for the best experience` hoặc Home Tab được chọn; chờ một khoảng chọn trong 2, 3, 4, 5 giây. **Đã nối mã theo ảnh; chưa thử thật q2.**

## Q2 b2 — Bấm menu ba gạch

Từ trang chủ, bấm Browse menu Tab và xác nhận menu. **Đã nối mã theo ảnh; chưa thử thật q2.**

## Q2 b3 — Bấm Pets

Tìm Pets trên menu hiện tại, cuộn khi cần và bấm. Bước chung b4 đưa về menu trước Sign In. **Đã nối mã theo ảnh; chưa thử thật q2.**

## Q3/Q4 b1–b3 — Đã được hướng dẫn ngày 13/11/2026

- q3: Groceries and Drinks → Home and DIY → Books and Reading. Mã tại `q3_flow.py`, chi tiết [Q3_FLOW.md](Q3_FLOW.md).
- q4: tab Giỏ hàng và xác nhận màn giỏ → về menu/Pets → Home and DIY. Mã tại `q4_flow.py`, chi tiết [Q4_FLOW.md](Q4_FLOW.md).
- Cả hai nối nguyên b4–b11; mỗi hàng có serial, OTP, đồng hồ và RegistrationState riêng. Đã qua unittest và kiểm tra OCR ảnh tĩnh, chưa chạy trên máy thật. Quy tắc menu danh sách chữ dùng chung vẫn được giữ.

## Chung b4 — Sign In từ menu

Nếu b3/b3a của máy mở trang khác, b4 kiểm tra màn hiện tại, dùng tab Browse menu hoặc Back theo từng chặng rồi đọc lại đến khi MENU hiện; không chỉ Back một lần rồi chờ vô hạn. Khi đã ở MENU, không phát thao tác quay lại. Cơ chế này dùng chung nhưng đặc biệt quan trọng cho q3–q6 có bước cuối ở trang danh mục/Giỏ hàng. Chưa xác minh trên lượt chạy nhiều máy thật.

Tìm hàng Sign In ở cuối menu bằng chữ trong UI, cuộn khi cần, bấm và xác nhận form `Sign in or create account`. **Chạm vào ô SĐT để lấy focus** trước b5; nếu đã ở form này khi bấm Tiếp tục thì vẫn chạm vào ô. **Đã sửa mã chung cho q1/q2 sau ảnh q1 ở form SĐT; chưa xác minh lại trên máy thật.**

Ảnh q1 mới cho thấy b4 dừng vì cây UI có nhiều nhãn `Sign In` dù hàng Sign In hiện trong menu danh sách dưới Customer Service. Bộ chọn chung giờ ưu tiên node có thể bấm; khi nhãn vẫn lặp, dùng Customer Service đang hiện làm mốc và chỉ chọn một Sign In dưới mốc. Nếu vẫn nhiều ứng viên thì dừng để người dùng sửa và bấm Tiếp tục. Trong phiên tool cũ, có thể bấm Sign In thủ công rồi Tiếp tục từ form SĐT. **131 test mô phỏng đạt; chưa xác minh trên q1 thật.**

## Chung b4a — Chạm ô SĐT

Nhánh dự phòng chung cho ô SĐT, tên và OTP: sau khi chạm, đọc lại màn/ô; nếu focus chưa được xác nhận thì tìm lại vị trí và chạm thêm tối đa hai lần. Cây Android có `focused=true` là bằng chứng trực tiếp; khi thiếu cờ focus hoặc chỉ có OCR, cần xác nhận bàn phím đã hiện. Trước khi gõ, đọc lại nội dung để giữ phần đã nhập và tránh gõ lặp. Nếu vẫn không xác định được ô đúng thì không gõ. **Đã test mô phỏng ngày 14/11/2026; chưa thử trên máy thật.**

Sau Sign In, chờ form nhập SĐT rồi chạm vào ô đang hiện. Nhận diện form theo nhãn `Enter mobile number or email` cùng nút `Continue`, kể cả khi cây UI WebView tạm thiếu tiêu đề hoặc node EditText. Không phân loại thành màn chọn quốc gia chỉ vì cây UI còn nhãn `Country/region code`; cần thấy các hàng quốc gia hoặc không có dấu hiệu form nhập số. B5 thử chạm lại nếu Android vẫn báo ô chưa có focus. Đây là bước dùng chung cho các máy đã nối b4–b11. Ảnh q1 báo UNKNOWN dù form SĐT đang hiện; bộ phân loại chung đã được sửa theo các dấu hiệu trên, chưa xác minh lại trên Swarmote thật.

## Chung b5 — Gõ số điện thoại

Gõ nguyên chuỗi SĐT của đúng hàng từng ký tự vào ô `Enter mobile number or email`, rồi đọc lại. Không dán clipboard. **Đã nối mã; chưa thử thật.**

## Chung b6 — Chọn United States +1

B6 cuộn nhanh tới đáy danh sách quốc gia. Khi đọc thấy Vietnam/Việt Nam, **đổi chiều ngay**, không chờ hai lần OCR giống nhau và không cuộn xuống thêm; nếu nhãn cuối không đọc được thì vẫn dùng kiểm tra hàng đứng yên. Từ đáy, vuốt ngược **ngắn và chậm** trong danh sách rồi đọc lại; nếu chưa thấy `United States +1` thì tiếp tục vuốt ngược từng đoạn ngắn, không cuộn xuống lại. Sửa 18/11 theo ảnh đứng im ở đáy: thấy Vietnam/Zimbabwe/Åland thì phát cú ngược ADB trực tiếp trong danh sách, tối đa một hàng/10% chiều cao, rồi đọc lại sau từng cú cho tới khi thấy US. Không chờ đọc native lần nữa hoặc fling xuống trong pha ngược. Pha này giữ riêng qua Dừng/Tiếp tục. Bộ đọc b6 có ngân sách 12 giây/lượt và tối đa ba lần lỗi; không tự thử mãi. Test mô phỏng và OCR ảnh gốc đạt, chưa thao tác trên Android thật. Nếu US đã hiện thì không cuộn thêm. Cả UiAutomator2 lẫn ADB dùng thời gian vuốt ngược nhẹ 650 ms. Chạm chữ, đợi và đọc lại; nếu hộp vẫn mở với hàng US ở đúng vị trí thì chạm giữa toàn hàng theo chiều rộng Android. Sau mỗi cú chạm phải xác nhận hộp đã đóng hoặc trạng thái đã đổi. Chỉ bấm khi mục có vùng hợp lệ. **Sửa theo báo cáo đứng im ngày 17/11; test mô phỏng đạt, chưa đo trên Swarmote thật.**

**B6a/b6b bổ sung 19/11/2026; chỉnh b6a 20/11/2026:** Quãng vuốt ngược b6a đầu tiên tăng đúng 3 lần, vẫn 650 ms; b6b và các cú sau giữ nguyên. Sau khi nhận ra đã cuộn tới đáy, b6a gửi một cú vuốt ngược nhẹ từ trên xuống trong danh sách rồi đọc lại trước khi chọn US +1, kể cả khi US đã ló ở mép trên. Hàng còn sát mép nhưng hiện và bấm được vẫn là mục hợp lệ. Nếu chưa thấy US, b6b vuốt ngược nhẹ thêm một cú rồi đọc lại; các cú tiếp theo vẫn ngắn và có giới hạn. Tool báo b6a/b6b và số lần vuốt tiếp theo, giữ chiều và số cú qua Dừng/Tiếp tục. 79 bài kiểm tra q1 đạt; phiên tool đang mở chưa nạp mã mới.

Nếu Amazon chuyển thẳng từ b5/b6 sang WHATSAPP hoặc SMS, b6 ngừng cuộn/chọn quốc gia và giao cho bước xác minh đúng máy; không vuốt trên form OTP. Đã kiểm tra bằng test mô phỏng ngày 17/11, chưa thử trên máy thật.

Sau khi gõ số, mở Country/region code, cuộn tới đáy rồi vuốt ngược nhẹ tìm United States +1, chọn và đọc lại số/mã quốc gia. Không bấm mục US ẩn có vùng `[0,0][0,0]`; chỉ bấm mục đang hiển thị và có vùng bấm hợp lệ. Ảnh b6 ban đầu có tiêu đề cửa sổ q6, chỉ là tham chiếu UI. q1 đã báo lỗi vùng bấm b6; **đã sửa mã chung, chưa xác minh lại trên máy thật.**

Sáu ảnh q1 mới ngày 13/11 cho thấy dropdown vẫn ở chữ A khi báo lỗi. Mã hiện tại lọc cả ô mở mã quốc gia bị ẩn, và chỉ bấm mục US +1 có bounds hợp lệ sau khi cuộn. Có test hồi quy cho trạng thái danh sách đang ở đầu. Chưa xác nhận phiên tool trên màn đã nạp mã này.

## Chung b7 — Continue số điện thoại

Chỉ bấm Continue khi form và số US +1 khớp hàng của máy. Nếu Amazon đã chuyển thẳng tới màn xác minh WHATSAPP/SMS đúng SĐT, coi đây là nhánh **đăng nhập** và bỏ các hành động tạo tài khoản trung gian; nếu tới NEW_ACCOUNT/CREATE_FORM, giữ nhánh **tạo** cũ. B7 chờ tối đa 20 giây rồi đọc lại cùng máy nếu cú chạm chưa chuyển màn. Màn khác chưa được ảnh hướng dẫn hoặc sai SĐT thì dừng riêng. **Đã nối mã và test mô phỏng; chưa thử thật sau sửa 17/11.**

## Chung b8 — Proceed to create an account

Xác nhận màn `Looks like you are new to Amazon` và SĐT, rồi bấm `Proceed to create an account`. Chờ đọc và xác nhận form nhập tên; chuyển kết quả đọc đã xác nhận cho b9 để tránh đọc toàn màn thêm một lượt. Khi Dừng/Tiếp tục và không còn kết quả đọc trong RAM, b9 đọc lại màn thật trước khi gõ. **Đã nối mã và test mô phỏng; chưa thử thật.**

## Chung b9 — Nhập tên và Continue

Khi cây UI trả nhiều mục Continue có vùng lồng nhau bên dưới ô tên, dùng vùng ngoài cùng của cùng một nút. Nếu còn nhiều vùng riêng biệt, giữ điểm dừng. Dùng lại cây UI đã đọc để xác nhận ô tên và tìm nút.

Trên form Create account, gõ `First and last name` từ đúng hàng từng ký tự, đọc lại rồi bấm Continue đang hiển thị, có thể bấm và nằm dưới ô tên. Bỏ qua bản sao nhãn ẩn hoặc không thể bấm. Ảnh chưa có ô mật khẩu; không tự điền mật khẩu vào chỗ khác. q1 đã báo lỗi nhiều Continue; **đã sửa mã chung, chưa xác minh lại trên máy thật.**

## Chung b10 — Chuyển WhatsApp sang SMS

**Sửa 21/11/2026 theo lỗi dừng luồng Tạo:** B10 không dừng chỉ vì dấu `create_flow_seen` trong RAM chưa được ghi khi màn chuyển nhanh hoặc người dùng Tiếp tục ở WhatsApp/SMS. B10 vẫn xác nhận màn và SĐT của đúng hàng, chỉ gửi SMS tối đa hai lần theo quy tắc cũ. Nếu màn SMS có nút `Create your Amazon account`, ghi lại dấu luồng Tạo; ở bước cuối vẫn phải nhận đúng nút Create mới bấm. Khi Tiếp tục tại SMS, khôi phục dấu này từ màn thật và không đánh dấu nhảy Đăng nhập cho chế độ Tạo. Đây là mã và test mô phỏng; chưa xác minh trên máy thật hoặc phiên tool đang mở.

Ở màn Verify with WhatsApp, xác nhận đúng SĐT, bấm `Send code by SMS` rồi chờ màn SMS. Nếu sau 20 giây nút còn hiện trên màn WhatsApp của **cùng SĐT**, thử chạm thêm đúng một lần; sau lần hai chờ tối đa 25 giây, còn kẹt thì dừng riêng. **Chỉ sau khi xác nhận màn SMS mới đọc URL OTP** của đúng hàng. Nếu Amazon đã tới SMS từ b5/b6 hoặc người dùng đã bấm gửi trước khi Tiếp tục, nhận màn đó mà không bấm gửi lặp. Màn SMS sai SĐT phải dừng. HTTP 403 trước khi gửi không được chặn thao tác gửi nữa; HTTP 403 kéo dài sau khi gửi làm máy dừng tại b11. **Đã sửa mã chung và test mô phỏng; chưa xác minh lại trên máy thật.**

Ảnh mới 17/11 cho thấy một máy vẫn ở `Verify with WhatsApp`, nút `Send code by SMS` còn hiện trong khi bảng báo màn chuyển chậm `(WHATSAPP)`; các máy khác chạy mượt. Trạng thái trong ảnh chưa xác định chính xác tool đang ở b7 hay b10, nên cả hai đường chờ đã được sửa. Cú chạm thứ hai ở b10 chỉ xảy ra sau khi đọc lại cùng màn và đúng SĐT, không lặp vô hạn. Khi Tiếp tục ở màn SMS, máy đi tiếp không gửi lặp. Chưa thử trên Swarmote thật; phiên tool đang mở không tự nạp mã mới.

Ảnh mới cho thấy báo HTTP 403 ở b10 trong khi màn còn WhatsApp. Mã nguồn hiện tại không gọi URL tại b10; test hồi quy xác nhận thứ tự bấm SMS → xác nhận màn SMS → đọc URL tại b11. Đây là dấu hiệu phiên tool trên màn có thể đang chạy mã cũ, chưa có bằng chứng phiên hiện tại đã nạp bản mới.

## Chung b11a — Chạm ô OTP trên màn SMS

Xác nhận màn SMS và đúng SĐT của hàng, sau đó chạm vào ô `Enter security code` nếu ô chưa có đủ sáu số. Bước này chạy trước khi đọc URL OTP nên lỗi nguồn mã không chặn thao tác chạm ô.

## Chung b11 — Lấy và gõ OTP SMS

Sau mốc 4 giây từ lúc gửi, đọc URL đúng hàng bằng Chrome ẩn hoặc Edge ẩn. Khi có mã, đọc lại màn SMS và xác nhận SĐT. Nếu Android báo ô mất focus, chạm lại trước khi gõ từng số. Đọc lại nội dung đã gõ. **Riêng nhánh đăng nhập:** nếu cây Android trả ô trống sau khi đã gõ, đọc ảnh Amazon trên đúng máy để đối chiếu đủ sáu số; chỉ khi xác nhận được mới qua b11b bấm Verify. Giữ dấu đã gửi phím và mã trong RAM, nên Tiếp tục không gõ lại mù khi ảnh chưa rõ. Nhánh tạo vẫn dùng đường nhập/xác nhận cũ. Nếu trình duyệt ẩn không đọc được, bấm Tiếp tục ở đúng hàng để mở trình duyệt thường hoặc nhập mã trên Amazon. Phản hồi chỉ có mã, không có dấu thời gian để phân biệt mã cũ. **Đã test mô phỏng; chưa thử thật sau sửa.**

## Chung b11b — Xác minh đăng nhập hoặc bấm Create của luồng tạo

B9 và b11 ưu tiên chữ và mô tả nút trong cây Android. Nếu chưa chọn được nút, tìm vùng nút vàng rộng dưới ô đã xác nhận bằng ảnh Android hiện tại. Nếu có nhiều vùng, chỉ chọn khi chữ của nút trong cây UI xác định được duy nhất một vùng.

Sau khi OTP đúng, nhánh tạo bấm Create một lần với khoảng kiểm tra riêng; nếu màn chưa chuyển, dừng để người dùng xem, không bấm lặp. **Ảnh Android mới xác nhận nhánh đăng nhập có nút vàng `Verify mobile number` dưới ô OTP**, cùng chữ với tiêu đề phía trên; chọn theo vị trí dưới ô để không bấm tiêu đề. Khi cây Android ẩn mã/nút, đọc lại ảnh, đối chiếu OTP và SĐT của đúng máy rồi chọn nút này; nếu chưa nhận diện được thì dừng đúng máy, không dùng đường ảnh nút vàng của Create. **Cập nhật 18/11:** Nếu đã thử bấm Verify mà SMS vẫn hiện, Tiếp tục đọc lại đúng SĐT, OTP và nút dưới ô rồi chỉ thử thêm một lần; sau hai lần vẫn ở SMS thì dừng riêng. Sửa 21/11/2026: tại đúng ranh giới b11b → b12 của nhánh Đăng nhập, Tiếp tục đọc màn một lần; nếu vẫn là SMS của đúng SĐT thì quay về b11b để thử Verify lần hai trong giới hạn hiện có. Nếu đã qua b12, giữ bước đã lưu và không quét lại SMS. 151 test b1–b15/Tiếp tục PASS; chưa thử trên máy thật. Dấu và số lần bấm giữ riêng từng máy. **Đã nối mã và test mô phỏng; chưa thử trên Swarmote thật sau sửa. Không khẳng định tài khoản thành công.** Settings mặc định Tạo; bật Đăng nhập để gắn luồng đăng nhập riêng cho máy mới. Ảnh tĩnh người dùng đã được bộ OCR trong `.venv` đọc đủ sáu ký tự và định vị nút dưới ô bằng ONNX Runtime 1.20.1; đây chưa phải cú bấm trên máy thật. **Chờ chuyển màn sau b11 (18/11):** sau khi bấm Create/Verify, đọc lại màn tối đa 45 giây thay vì 10 giây; màn trống/chỉ hiện Amazon hoặc Loading chưa tính là đã chuyển xong. Trong thời gian chờ không bấm xác nhận lặp; Dừng riêng vẫn được nhận. Máy 7 cũng chờ kết quả tới 45 giây thay chốt 8 giây, với ngân sách b11b 90 giây cho thao tác và xác minh. Màn chuyển xong thì chạy tiếp ngay, không bắt buộc đợi đủ 45 giây. Chưa kiểm chứng trên Swarmote thật.

Nếu cây WebView không xuất nút `Verify mobile number`, riêng nhánh đăng nhập dùng ảnh Android để tìm **một** nút vàng rộng dưới ô OTP đã xác nhận; chữ đen trên nút có thể chia dải màu thành hai phần nên bộ dò ghép chúng khi cùng một nút. Đã thử bộ dò màu trực tiếp với ảnh người dùng gửi, trả đúng vùng nút dưới ô; đường dò và ngưỡng của nhánh Create giữ nguyên. Nếu có nhiều nút vàng không phân biệt được, dừng máy đó.

## Chung b12–b15 — Mở ba gạch rồi ba lượt điều hướng ngẫu nhiên

**Nhịp cuộn hiện hành, sửa 26/11/2026:** B13/b14/b15 chờ nửa thời gian xem sau cú bấm, vuốt vừa một lần từ dưới lên trong menu/trang con, rồi xem hết nửa còn lại trước khi Back khỏi trang con. B13/b14 giữ 16 giây ở Tạo và 1 giây ở Đăng nhập; b15 xem 40 giây ở Tạo và 10 giây ở Đăng nhập theo yêu cầu tăng gần gấp đôi. Dừng/Tiếp tục sau cú vuốt không cuộn hoặc bấm lại, chỉ chờ phần thời gian còn lại. Đây là mã/test mô phỏng; chưa kiểm trên Swarmote thật.

**Nhịp vuốt 27/11/2026:** Cú cuộn tìm mục mới trong menu và cú cuộn xem menu/trang con giữ nguyên quãng vuốt, tăng thời gian lên 700 ms. Vẫn chỉ cuộn khi bước cũ yêu cầu và giữ dấu đã cuộn khi Dừng/Tiếp tục.

**Bổ sung b13–b15 ngày 20/11/2026:** Sau OTP có thể hiện menu thẻ hoặc menu danh sách. Nếu cây Android chỉ thấy tiêu đề mà thiếu các hàng, đọc OCR ảnh hiện tại để chọn mục trước khi cuộn/dừng. OCR ảnh thật nhận đủ sáu mục danh sách; test mô phỏng đạt, chưa chạy Swarmote thật.

**Bổ sung b13–b15 ngày 21/11/2026:** Ưu tiên bấm mục lớn đang hiện; chỉ dùng mục con nếu các mục lớn không còn lựa chọn hợp lệ. Sau khi xem trang con, đọc trạng thái tối đa 4 giây; nếu chậm/lỗi vẫn cuộn một lượt rồi Back, không chèn thêm lượt đọc giữa hai thao tác. Nếu vẫn ở MENU thì không cuộn/Back. Dừng/Tiếp tục giữ trạng thái lượt đã bấm, thời gian xem hiện hành. 54 test random PASS; chưa thử máy thật và phiên tool đang mở chưa nạp bản mới.

**Đính chính b14 ngày 20/11/2026:** Menu dạng danh sách trong ảnh là hợp lệ. B14 không tự hoàn tất khi chưa bấm; chọn một mục còn dùng được, xem và trở về menu trước b15. Nếu thật sự không xác định được mục, giữ bước để kiểm tra. Chỉ là mã/test mô phỏng; chưa chạy thật.

**Cập nhật 18/11/2026:** Sau b11 nhập OTP và xác nhận, Amazon tự về Trang chủ; b12 chỉ mở menu ba gạch (Browse), b13–b15 là ba lượt điều hướng ngẫu nhiên trên đúng máy. Có thể chọn thẻ, mục con, Giỏ hàng hoặc điều khiển điều hướng đang hiện chưa có trong ảnh tham chiếu. Không chọn Trang chủ; không lặp nhãn đã thử trong chính máy đó. Chuỗi ba lựa chọn hoàn chỉnh không trùng với máy khác trong cùng mẻ, kể cả khi worker chạy đồng thời. Màn chậm/SMS cũ được đọc lại tối đa ba lần, chờ 2 rồi 4 giây; không cần khớp một ảnh mẫu. Nếu Trang chủ ẩn nhãn Browse, xác nhận Amazon ở trước rồi dùng kích thước đúng serial để chạm ba gạch và đọc lại menu. Giữ lựa chọn/điểm dừng khi Tiếp tục. Sau b15 nối b16–b22 chung theo mục kế tiếp. Đã kiểm thử mô phỏng, chưa thử 12 máy thật. **Nhịp xem điều chỉnh 18/11:** b12 chờ menu ổn định 2 giây; sau mỗi lựa chọn b13–b15 xem ngẫu nhiên 3–5 giây thay vì 0,4 giây. Thời điểm hết lượt xem giữ riêng từng máy; Dừng/Tiếp tục hoặc dựng lại bước chỉ chờ phần còn lại, không mở lại menu/chạm lại mục đã bấm. **Siết khác nhau giữa các máy ngày 18/11:** B12 cố định mở ba gạch, không bốc ngẫu nhiên. B13, b14 và b15 mỗi lượt giữ chỗ nhãn dưới khóa chung của mẻ: cùng một bước không được chọn cùng nhãn với máy khác, kể cả 12 worker cùng chọn đồng thời. Trước đây chỉ chặn trùng cả chuỗi nên từng lượt vẫn có thể trùng; nay loại cả trường hợp đó. Trong một máy vẫn loại nhãn đã thử ở mọi lượt. Nếu mục đang hiện đều đã được dùng ở bước đó, đọc/cuộn tìm mục khác tối đa ba lượt; không âm thầm chọn lại nhãn đã bị giữ chỗ. Dừng/Tiếp tục giữ lựa chọn, nhịp b12=2 giây và b13–b15=3–5 giây. Mẻ mới có sổ giữ chỗ riêng. Chưa thử trên Swarmote thật. **Điều chỉnh theo lỗi b14 ngày 19/11/2026:** B13–b15 đọc màn Amazon hiện tại, thấy mục bấm được và không phải Search/Lens/quyền/trả tiền/xóa thì chọn ngay, không cần quay lại Browse hay đợi Trang chủ. Sau cú bấm, luồng Tạo tài khoản xem 8 giây mỗi lượt b13–b15; luồng Đăng nhập xem 0,5 giây. Hết b15 chuyển thẳng b16 hình người. Mốc xem giữ riêng máy qua Dừng/Tiếp tục, không bấm lại lượt đã gửi. Nếu màn không có mục phù hợp, thử ba gạch hoặc Back rồi đọc lại. Ưu tiên nhãn khác máy; sau hai lượt tìm mà chỉ còn nhãn đã dùng ở máy khác thì cho phép trùng giữa máy để khỏi kẹt, vẫn không lặp nhãn trong chính máy. Giữ dấu đã bấm khi Dừng/Tiếp tục. 48 test random và 502 test toàn dự án PASS; chưa nạp vào phiên tool đang mở. **Bổ sung cùng ngày theo ảnh lỗi b13:** Menu ba gạch có cả dạng thẻ và dạng danh sách; dạng danh sách cho chọn Books, Electronics, Home services, See all, Today’s Deals, Try Prime. Không dừng chỉ vì mười hai máy chia sáu mục: sau hai lượt tìm mục khác, có thể trùng giữa máy nhưng không trùng trong chính máy. **Chốt lại ngày 20/11/2026 theo yêu cầu mới:** B13–b15 chỉ bốc thẻ/mục con đang hiện trong menu ba gạch; không bốc Giỏ hàng, tab khác, nút trên trang sản phẩm hoặc điều hướng ngoài menu. Sau khi bấm, giữ nguyên thời gian xem hiện hành (Tạo 8 giây, Đăng nhập 0,5 giây). Nếu mở trang/thẻ con, cuộn một lượt trong trang đó rồi Back, xác nhận lại menu Browse trước khi hoàn tất bước và chọn mục khác ở bước tiếp theo. Nếu mục con vẫn mở trong menu thì tiếp tục từ menu. Dừng/Tiếp tục giữ cú bấm, mốc xem, dấu đã cuộn và đã gửi Back riêng từng máy; không bấm lại lựa chọn cũ. Không coi b13–b15 hoàn tất khi chưa trở về menu. **Điều chỉnh 21/11/2026:** gấp đôi thời gian xem b13–b15 thành 16 giây ở luồng Tạo và 1 giây ở luồng Đăng nhập; Dừng/Tiếp tục giữ phần thời gian còn lại. Mã và test mô phỏng đã cập nhật; chưa xác minh Swarmote thật, phiên đang mở không tự nạp mã mới.

**Sửa b13–b15 theo ảnh Lens và tìm kiếm — 18/11:** `_tail_candidates` trước đây cho lọt nhiều nút clickable không phải điều hướng, gồm ô Search/camera; `_tail_menu` chỉ thử Browse, không thoát Lens hoặc bàn phím và còn gọi bộ đọc tự lặp. Đã loại điều khiển nhập/tìm kiếm, Camera/Lens/Scan, quyền truy cập và đóng popup khỏi tập chọn ngẫu nhiên; vẫn chọn thẻ, mục con, Giỏ hàng và điều hướng mới đang hiện, không ép chuỗi cố định. Giữ `secrets.choice` và khóa giữ chỗ mỗi bước giữa các máy. Mẻ mới còn loại nhãn cùng bước của cùng slot ở mẻ gần nhất trong sổ RAM; thiếu mục thì cuộn tìm mục mới, không chọn trùng. Lịch sử này không tồn tại sau khi đóng tool. Tiếp tục vẫn giữ cú bấm và thời gian xem đã xác nhận, đủ ba lượt 3–5 giây trước b16. Khi tìm kiếm/bàn phím che tab thì Back, đọc lại rồi thoát tìm kiếm nếu cần; khi Lens có nút Not now duy nhất thì từ chối, Back khỏi Lens rồi mở Browse. Không bấm Allow access. Không coi MENU phía sau popup/bàn phím là menu đang thao tác; kiểm tra foreground trước khi nhận menu. Tối đa ba hành động phục hồi và một lượt đọc cuối để xác nhận đã về menu; đọc đơn có ngân sách 12 giây, lỗi đọc tối đa ba lần thay vì vòng thử mãi. Phản hồi ADB chưa rõ thì đọc lại trước cú thoát tiếp theo. Auth/OTP giữ chốt cũ; B12 vẫn mở Browse và ổn định 2 giây. 484 unittest PASS: bộ lọc Search/camera, bàn phím che menu, Not now → Back → Browse, timeout không gửi thoát đôi, popup có focus, hai mẻ × 12 máy không trùng từng bước/mẻ trước, và giữ Dừng/Tiếp tục. OCR thật ảnh Lens mới nhận overlay=True, một Not now và không có ứng viên ngẫu nhiên. Ảnh 16/17 lưu cùng nhóm random_prefix_reference. Chưa bấm trên Android thật. Hai pythonw của tool được thấy khởi động trước bản sửa random_prefix.py này; không tự nạp mã mới, không đóng/reset phiên RAM.



**Chờ Trang chủ sau OTP và chuyển b15 → b16 — 19/11:** Amazon có thể hiện Trang chủ trước khi menu/cây UI tải xong. B12 đọc lại để mở Browse tối đa 90 giây/8 lượt phục hồi; b13–b15 tối đa 60 giây/5 lượt. Tool báo đang chờ hoặc lỗi cụ thể trên hàng máy, giữ mốc chờ khi Dừng/Tiếp tục. Sau b15 đủ 3–5 giây, đánh dấu hoàn tất và báo chuyển b16 hình người ngay, không bấm lặp mục ngẫu nhiên. Chưa thử lại trên Swarmote thật với phiên mã mới.

## Tạo tài khoản b23–b31 — Account và Your Addresses

**Nhịp vuốt 27/11/2026 cho các bước có cuộn:** B24/25 tìm Your Addresses dùng 750 ms khi cuộn xuống, giữ 650 ms cho cú vuốt ngược ngắn; b29/b30 cuộn form địa chỉ dùng 900 ms; b32/b33 tìm Reload Balance dùng 850 ms; b34/b36 cuộn ngắn tìm Buy Now dùng 700 ms. Chỉ đổi thời gian của lệnh vuốt cũ, giữ nguyên điểm đầu/cuối, điều kiện đọc màn, số lần thử và dấu Dừng/Tiếp tục. Hai đoạn tìm US ở b6 và b19 giữ nguyên. Đây là mã/test mô phỏng, chưa đo cú cuộn trên phiên Swarmote thật.

**Nhánh Đăng nhập tùy chọn, cập nhật 26/11/2026:** Hai công tắc mới trong Settings chỉ tác động máy bắt đầu ở chế độ Đăng nhập: “thêm địa chỉ rồi thẻ” nối b23–b39 sau b22, còn “chỉ thêm thẻ” nối b32–b39 sau b22. B32 trong nhánh chỉ thẻ lấy b22 hoàn tất làm điều kiện vào, không cần b31. Hai công tắc loại trừ nhau; nếu đều tắt, Đăng nhập vẫn dừng ở b22. Luồng Tạo vẫn dùng b23–b39 hiện có. Đây là mã và test mô phỏng; chưa xác nhận trên phiên tool thật.

**B28, cập nhật 20/11/2026:** Ảnh mới cho thấy Street address đã có địa chỉ nhưng mã tìm kiếm đôi khi vào ô ngay dưới (Unit). Trước khi gõ, ô focus phải nằm trọn vùng Street và không chồng sang Unit; nếu Street đã có địa chỉ mà ZIP chưa rõ thì dừng b28 để đọc/sửa trên máy, không nhập lại số. Đã kiểm tra test mô phỏng, chưa xác minh thao tác máy thật.

**Ảnh bổ sung b28 cùng ngày:** Sau b27, bàn phím có thể đã mở và Street đã focus. B28 vẫn chạm tâm ô Street hiện tại; khi focus chưa rõ thì ưu tiên ảnh mới để tìm chữ và vùng ô Street. Sau cú chạm phải xác nhận focus bằng cây Android trước khi gõ; OCR không tự cho phép nhập mã vào ô bất kỳ.

**Cập nhật b27–b28 ngày 23/11/2026:** B27 bấm chữ xanh `Enter an address manually` xong thì hoàn tất và sang b28 ngay. B28 gửi số tìm địa chỉ của đúng máy vào bàn phím đang mở, không đọc ảnh/cây, không chạm lại ô Street và không kiểm focus trước khi nhập; quy tắc này thay các ghi chú 20–21/11 về xác nhận focus trước khi gõ. Dấu gửi được đặt trước lệnh ADB để Tiếp tục không nhập lặp nếu kết quả chưa rõ. Sau khi nhập mới OCR vùng gợi ý; thấy dòng bắt đầu bằng số đó thì chọn ngay. Nếu chưa có gợi ý sau 45 giây, giữ b28 để người dùng kiểm tra máy. OCR vùng gợi ý dùng hai engine chung có giới hạn; thông báo thiếu kết quả không gọi là mạng chậm. Đã kiểm mô phỏng và ảnh tĩnh, chưa xác minh phiên tool đang mở.

**B29, cập nhật 20/11/2026:** Ảnh mới cho thấy ô Make this my default address đang trống nhưng tool chưa tích được. Khi cây Android trả nhãn, b29 vẫn tìm chữ trên ảnh để định vị ô vuông bên trái, bấm tâm ô và đọc lại trạng thái; không lấy vùng chữ làm mục tiêu. Đã kiểm tra ảnh tĩnh và test mô phỏng, chưa xác minh cú bấm trên máy thật.

**B29, cập nhật 21/11/2026:** Phiên desktop đang chạy đã khởi động sau bản sửa 20/11 nhưng người dùng vẫn báo kẹt. Sau cú bấm, thấy dấu tích trong đúng ô là hoàn tất b29 và sang b30 ngay; không đợi OCR tìm lại nhãn. Sửa nhận diện ảnh cho ô đã tích màu sáng và nhãn OCR sai một chữ. Theo phản hồi tiếp cùng ngày, b29 chụp OCR trước để tránh chờ cây Android trên WebView; native chỉ dự phòng nếu ảnh lỗi. Trạng thái `checked=true` của dòng chữ không đủ chứng minh ô vuông đã tích: phải kiểm tra pixel và bấm ô nếu trống. 26 test địa chỉ PASS; chưa thử cú tích thật sau sửa. Bản sửa mới cần phiên tool nạp lại, nhưng không đóng phiên hiện hành vì dữ liệu nhập chỉ nằm trong RAM.

**B27–b28, cập nhật 21/11/2026:** Ảnh người dùng cho thấy b27 báo đọc chậm dù form địa chỉ đã hiện, đồng thời b28 có tiền sử nhập số sang ô Unit. B27 đọc OCR khi cây Android chỉ trả một phần form, không chỉ khi rỗng. B28 yêu cầu nhãn Street và giới hạn bounds trước hàng Unit kể cả khi ô có `resource-id` giống Street. OCR ảnh thật nhận form và điểm chạm ô Street; 21 test địa chỉ PASS. Chưa kiểm thao tác máy thật, phiên hiện hành chưa nạp mã mới.

**B28, bổ sung cùng ngày:** Trước khi nhập, bắt buộc chụp ảnh OCR để lấy vị trí Street/Address line 1 và ô nằm trước Unit/ZIP; chạm vị trí ảnh tìm được. Giao diện đang tải hoặc OCR chưa rõ: chờ hai giây, chụp lại tối đa ba lượt rồi dừng mà chưa nhập. 23 test địa chỉ PASS, có ca nhãn khác và ảnh tải chậm. Chưa chạy trên đúng máy thật, phiên hiện hành chưa nạp mã mới.

**B28–b30, đính chính theo ba ảnh mới 21/11/2026:** Sau khi nhập số ở Street, thấy danh sách gợi ý thì b28 chọn ngay một địa chỉ, không chờ ZIP hoặc kiểm nội dung gợi ý. B29 chỉ dùng OCR tìm chữ Make this my default address để định vị ô vuông bên trái rồi bấm một lần; không đọc trạng thái tích trước hoặc sau, vì ảnh đầu vào cho thấy ô trống. B30 cuộn xuống khi chưa thấy Add address, chụp tìm đúng chữ rồi bấm ngay; sau cú bấm vẫn xác nhận Address saved/Personal Addresses trước khi sang b31. Đây là mã và 24 test mô phỏng PASS, chưa chạy trên máy thật; phiên desktop đang mở không tự nạp mã mới. Các mô tả kiểm pixel/tích trước đó là lịch sử đã được thay bằng chỉ dẫn này.

**B31, đính chính 21/11; sửa nhịp 26/11/2026:** Ảnh 11 cho thấy sau `Address saved`, bấm tab hình người ở thanh dưới. B31 hoàn tất ngay sau cú bấm; b32 chờ 2,5 giây tính từ cú bấm rồi mới cuộn, không đọc xác nhận trang Account. Tìm tab từ cây Android một lượt; thiếu nhãn dùng vị trí tab trên máy hiện tại. Dừng/Tiếp tục giữ mốc chờ, không bấm hình người thêm lần nữa. Đây là mã/test mô phỏng, chưa xác nhận trên máy thật hoặc phiên đang mở.

**B24–b25, cập nhật 21/11/2026:** Sau b23, b24 chụp OCR tìm đúng chữ Your Addresses; thấy thì chuyển b25, chưa thấy thì cuộn xuống và chụp lại, kể cả ảnh ít chữ. Nếu sau cú cuộn vẫn chỉ là trang chen vào không có nội dung Account, Back một lần rồi chụp tìm tiếp; không bấm lại Account. B25 chụp mới, thấy đúng chữ Your Addresses thì bấm ngay. Các nhãn khác chỉ giúp quyết định Back khỏi trang chen vào, không là điều kiện để chọn Your Addresses. 9 test create_address_flow PASS; chưa có ảnh quảng cáo cụ thể hay thử máy thật, phiên hiện hành chưa nạp mã mới.

**B32–b39, bổ sung 21/11/2026:** B32 cuộn ngay sau cú bấm hình người; b33 tìm chữ Reload Balance, chưa thấy thì cuộn tiếp và thấy thì bấm ngay. B34 vuốt ngắn ngay sau cú bấm b33, không đọc màn mới trước; b36 tìm chữ Buy Now, chưa thấy thì vuốt ngắn tiếp và thấy thì bấm ngay; b37 bấm Add a credit or debit card trên màn Your Auto-Reload Setting; b38 tìm đúng ba ô thẻ, nhập số thẻ/MM-YY/tên cùng hàng của đúng máy rồi đọc vùng nút Add and continue và bấm ngay khi thấy chữ. B39 chỉ tìm chữ Use this address trên ảnh rồi bấm ngay, không kiểm trạng thái chọn địa chỉ hay bố cục màn; kết thúc tại đó. Ảnh b35 là trạng thái Low Balance Auto-Reload mặc định, không có thao tác riêng; không đổi $25/$10. Không bấm Set up now. Màn tải chậm được đọc lại tối đa năm lượt; thiếu thẻ/ô không rõ thì dừng riêng trước nhập. Card chỉ trong RAM, không ghi đầy đủ vào log/tài liệu. Test mô phỏng mới PASS; chưa thử máy thật, phiên hiện hành chưa nạp mã mới. **Sửa b38 ngày 23/11/2026:** Quét OCR vùng ba ô một lượt, chỉ nhập khi đã xác định đủ Card number, Expiration date và Name on card; dùng đúng hàng máy, giữ dấu từng ô khi Tiếp tục. Chưa thử máy thật.

**B36–b38 điều chỉnh thêm 25/11/2026:** b36/b37 chỉ đọc vùng chữ cần bấm, không quét toàn màn/cây Android khi vùng thiếu chữ; b38 nhập từng ký tự, nghỉ 0,4 giây giữa ký tự.

**B38 sửa 25/11/2026:** Sau một lượt OCR xác định đủ ba ô thẻ, nhập từng nhóm tối đa bốn ký tự và nghỉ 0,3 giây giữa các nhóm. Nếu bàn phím vẫn hiện sau ô tên thì đóng bàn phím; quét chữ Add and continue trong vùng 30–80% chiều cao rồi bấm ngay. Vùng cũ 55–98% bỏ sót nút nằm khoảng 45% trong ảnh form đã lưu. Không quét toàn màn khi tìm nút; chưa xác minh trên máy thật.

Kiểm tra tốc độ 21/11/2026: b23 giữ đúng nhịp chờ 3 giây sau b22, mốc chờ riêng máy giữ qua Dừng/Tiếp tục; hết chờ chỉ OCR vùng có chữ Account và bấm khi thấy đúng một nhãn, không phân loại toàn màn hoặc đòi thêm nội dung. B24–b25 tiếp tục đọc OCR chữ Your Addresses trước. B26–b27 quét chữ ở nửa trên, b30 ưu tiên OCR để bấm Add address ngay khi thấy. B33/b34/b36/b37 quét vùng có nút, giữ tọa độ toàn màn để bấm; b34 vuốt trước khi đọc và vuốt tiếp ngay khi vùng chưa có Buy Now. B38 vẫn xác định từng ô thẻ. OCR b37 trên ảnh lưu đọc đúng dòng; phép đo OCR ảnh tĩnh đã làm nóng: toàn ảnh trung bình 4,33 giây, vùng nút 2,36 giây (ba lần mỗi cách), chưa gồm ADB và chưa đo trên máy thật.

Tối ưu thêm: b26–b27 và b33–b37 tìm nhãn bằng OCR trên ảnh mới trước, dùng cây Android dự phòng khi ảnh thiếu nhãn. B28 xác nhận focus Street bằng cây Android, b29 bấm trực tiếp ô vuông theo chữ; b30 xác nhận kết quả lưu sau cú bấm, b38 xác nhận từng ô trước khi nhập. Đây là thay đổi thứ tự đọc, không bỏ xác nhận thao tác.

Theo hai ảnh b34 mới 21/11: trang Amazon Gift Card Balance Reload đã hiện nhưng Buy Now còn dưới khung nhìn. **Đính chính tiếp theo yêu cầu người dùng:** sau b33 bấm Reload Balance, b34 vuốt ngắn từ khoảng 72% lên 43% chiều cao ngay, không chờ quét/khớp tiêu đề hay chữ nào trên trang; sau vuốt mới tìm Buy Now, chưa thấy thì vuốt ngắn tiếp trong giới hạn hiện hành. B28 sau khi nhập số ưu tiên OCR vùng danh sách gợi ý và chọn ngay một dòng hiện ra, không đợi ZIP tự điền; khi chưa thấy thì đọc dự phòng. **Đính chính b29 cùng ngày:** không tin `checked=true` của dòng chữ native, vì người dùng thấy ô vuông vẫn trống và máy đã sang bước sau. Luôn tìm ô vuông cạnh chữ trên ảnh, đọc pixel; chỉ hoàn tất khi ô đã tích, nếu trống thì bấm chính ô vuông và kiểm tra lại. Không thấy rõ ô thì giữ b29. Đính chính 21/11: ô đã tích phải có nền xanh trong vùng vuông; pixel tối đơn thuần không được tính là dấu tích. Nếu ô trống, bấm đúng ô rồi chỉ chụp kiểm tra ô đó tối đa ba lượt ngắn, không OCR lại toàn form; chưa thấy tích thì giữ b29 và chặn b30. 28 test địa chỉ mô phỏng PASS; chưa thử trên máy thật.

Ngày 21/11/2026, sau b22 chờ đủ 3 giây. B23 chụp vùng đầu màn, thấy đúng chữ `Account` thì bấm ngay; không đòi các điều kiện nhận diện trang khác. B24 chụp tìm `Your Addresses`; nếu mục đã hiện thì không cuộn, nếu chưa thấy thì cuộn xuống rồi chụp lại, trang quảng cáo chen vào thì Back để trở về. B25 chụp mới thấy đúng chữ thì bấm `Your Addresses` rồi sang b26; b26–b31 đã có ảnh và mã nối tiếp. B23–b25 chỉ thuộc luồng Tạo tài khoản, chung cho 12 máy kể cả q7. Dừng/Tiếp tục giữ riêng bước đã xong và phần thời gian chờ còn lại. Màn chậm được chụp đọc lại có giới hạn; b24 không tự bấm lại Account. Tìm mục tối đa 32 lượt trong tối đa 120 giây mỗi bước và vuốt ngược nhẹ khi danh sách đứng; thấy mục là xử lý ngay. Tool báo trên hàng máy đang đọc, chờ tải, cuộn, tìm thấy hoặc lỗi cụ thể; hết hạn thì dừng riêng với bước, mục và số lần cuộn. Theo sửa mới 21/11, b23–b25 chỉ dùng OCR chữ ở vùng cần tìm; không yêu cầu phân loại trang Account trước khi bấm nhãn đích. Ảnh tham chiếu lưu tại `flow_images/shared/create_address/`; chưa thao tác thật với mã mới. B26 chọn Add a new address, b27 chọn Enter an address manually. Sau Test Passed khi tạo Profile, thử đọc mã bưu chính cạnh City từ cây UI Swarmote và giữ 4 chữ số đầu riêng từng máy (ví dụ 36547 → 3654); lỗi hoặc thiếu mã không cản tạo Profile. B28 chặn chọn nhầm Unit or suite number: chỉ nhận ô trong vùng Street address trước nhãn Unit/ZIP; nếu cây Android thiếu ô thì OCR tìm placeholder Street trước khi gõ. Ảnh 20/11 cho thấy dữ liệu đã vào Unit trên máy thật, chưa tự sửa máy. B28 ưu tiên nhập 4 số đã giữ, nếu không có mới dùng chuỗi 3–4 chữ số dự phòng không lặp qua các phiên trong `%LOCALAPPDATA%/Swarmote/address_prefixes.json`; sau đó OCR vùng gợi ý và chọn ngay một dòng hiện ra, không đợi ZIP tự điền. Không ghi địa chỉ cá nhân hoặc mã bưu chính đầy đủ vào log. B29 chụp tìm chữ Make this my default address và bấm thẳng ô vuông bên trái một lần; theo ảnh mới, ô ban đầu chưa tích. Sửa 20/11: khi cây Android thiếu mục nhưng form vẫn có node, đọc OCR trước khi cuộn; xác định trạng thái ô trên ảnh nếu native không có checked, cuộn dài tối đa ba lượt. B30 đọc OCR tìm Add address trước khi cuộn thêm. B30 cuộn tìm Add address, giới hạn hai lần gửi và phải thấy Address saved/Personal Addresses mới coi là xong. Sau xác nhận, b31 bấm tab hình người và chỉ hoàn tất khi đọc lại xác nhận trang Account; nếu chưa xác nhận thì giữ b31, không cho b32 cuộn. B26–b27 ưu tiên OCR vùng có nhãn; b28 vẫn kiểm tra focus Street, b29 bấm ô cạnh chữ không kiểm trạng thái, b30 ưu tiên OCR Add address, b31 xác nhận Account; mỗi bước tối đa 120 giây, đọc lỗi tối đa ba lần, chạm lại có giới hạn khi màn chưa đổi. 8 ảnh mới là tài liệu tham chiếu 05–12. Đây là mã và test mô phỏng; phiên tool đang mở chưa nạp mã mới, chưa thử b26–b31 trên máy thật.

## Chung b16–b22 — Tài khoản và marketplace United States

Ngày 18/11/2026 người dùng hướng dẫn bằng 7 ảnh; áp dụng chung cả Tạo và Đăng nhập trên 12 máy. Hành động tập trung trong `marketplace_flow.py`, nối sau b15 tại `build_post_auth_steps`, không chép riêng theo máy/luồng. Ảnh gốc và ánh xạ từng bước: [IMAGE_EVIDENCE.md](IMAGE_EVIDENCE.md), thư mục `flow_images/shared/marketplace_us/`.

| Bước | Thao tác và kiểm tra |
| --- | --- |
| b16 | Từ menu/trang đang hiện, bấm tab hình người ở thanh dưới và chuyển ngay sang b17 sau cú bấm thành công, không đợi nội dung Account tải xong. Ảnh b16 khoanh đỏ là màn sau cú bấm, không phải điều kiện trước. Giữ thời điểm bấm riêng máy để b17 chờ đủ 10 giây qua Dừng/Tiếp tục. Nếu đã ở tài khoản hoặc đã mở phần quốc gia thì nhận trạng thái hiện tại. |
| b17 | Sau b16 hình người, chờ đủ 10 giây kể từ cú bấm rồi quét chữ EN ở đầu màn và bấm. Không bấm Account hoặc Back giữa b16 và b17; không đòi đủ bố cục Account hay thêm điều kiện nhận diện màn. Nếu chưa thấy EN mới dùng nhánh đọc/phục hồi hiện có. Cập nhật 26/11/2026; test mô phỏng, chưa chạy máy thật với mã mới. |
| b18 | Mở ô Country/Region để vào danh sách marketplace. |
| b19 | Vuốt dưới lên, đọc lại sau từng lần cho tới khi United States hiện. Nếu danh sách đứng yên, thử vuốt ngược nhẹ. Chỉ tìm, chưa chọn. |
| b20 | Bấm hàng United States, chờ ô Country/Region phía trên đổi thành United States. Không dùng dòng US ở Previously visited làm bằng chứng đã chọn. |
| b21 | Bấm Done sau khi đối chiếu quốc gia rồi chuyển ngay sang b22 khi cú bấm thành công; không chờ xác nhận màn đổi quốc gia. Nếu cú bấm chưa rõ kết quả, giữ dấu đã gửi qua Dừng/Tiếp tục và đọc lại trước khi thử thêm Done. |
| b22 | Sau Done ưu tiên đọc cây UI: thấy tab hình người hoặc xác định được từ thanh điều hướng là bấm ngay, kể cả nội dung đang Loading hoặc trang Account đã hiện. Chỉ chờ khi chưa xác định được tab; không đợi ảnh Trang chủ hoặc OCR khi cây UI đã đủ bằng chứng. Sau cú bấm mới xác nhận đã vào Account. |

B16–b22 có hạn chờ 75 giây, lỗi đọc thử lại tối đa ba lần; b17 giữ mốc 10 giây tính từ b16 hình người. Nút dùng cây UI, OCR là dự phòng; tab hình người có đường dự phòng dựa trên thanh tab/kích thước đúng Android sau khi xác nhận Amazon ở trước. Màn lệch được đưa về tài khoản và phần quốc gia đã biết; nút Retry/Reload chỉ dùng khi xác định duy nhất. Gặp lại form xác minh thì dừng riêng, không tự đổi luồng. Trạng thái hoàn tất, Done và số lần thử riêng từng máy. Đã kiểm tra mô phỏng và OCR ảnh tĩnh, chưa đổi quốc gia trên thiết bị thật. B23 trở đi mô tả ở mục Tạo tài khoản bên trên.

### Bỏ b16a — cập nhật 26/11/2026

Người dùng hủy cả bước Account xem 4 giây và kế hoạch chọn 12 đích ngẫu nhiên. Sau b16 hình người, b17 chờ đến mốc 10 giây của đúng máy rồi bấm EN đang hiện; không chèn bước xem trang khác hay Back. Kịch bản 12 đích chưa từng được triển khai; ảnh cũ chỉ là tham chiếu màn sau b16. Dừng/Tiếp tục giữ mốc b16 và chờ phần còn lại, không bấm lại hình người. Test mô phỏng không chứng minh phiên Swarmote đang mở đã nạp mã mới.


**Sửa phục hồi b16–b22 ngày 18/11 sau ảnh tìm kiếm:** Màn tìm kiếm có bàn phím che thanh dưới không được dùng tọa độ hình người cũ. `_search_active` nhận Search with photo/camera hoặc ô Search đang focus; `_navigation_ready` xác nhận tab thật/menu. Nếu thiếu thanh tab thì Back, chờ 2 giây và đọc lại trước từng thao tác; tối đa ba Back trong một bước. Khi menu/thanh tab đã hiện thì bấm hình người trực tiếp, không bắt buộc qua ba gạch và không chờ ACCOUNT trước cú bấm. Dùng chung đường phục hồi này khi b17–b21 bị lệch trang và ở b22 sau Done. Màn Loading chỉ được chờ khi chưa xác định được thanh tab; có tab hình người thì bấm ngay, không Back hoặc đợi nội dung tải xong. Stop được kiểm lại trước Back/cú chạm; trạng thái mỗi serial và hai luồng giữ riêng. Test mới chạy hết b16–b22 qua 24 tổ hợp Tạo/Đăng nhập × 12 factory với bàn phím → tìm kiếm → menu → hình người → EN → danh sách/US → Done → tải → trang toàn màn hình → Back → hình người, dùng guard foreground thật trên dữ liệu dumpsys giả, cùng test b17 phục hồi, giới hạn Back và Stop. 462 unittest toàn dự án PASS; OCR thật nhận đúng 7 ảnh b16–b22 và ảnh tìm kiếm mới, chọn được EN/Country/Region/US/Done. Read-only ADB ở hai serial online ban đầu xác nhận Amazon đang ở trước; lượt đọc native tiếp theo thấy một serial online có tab hình người và lấy được bounds từ UI. Chưa bấm/đổi marketplace trên thiết bị thật. Tiến trình tool khởi động trước thời điểm sửa cloud.py/marketplace_flow.py; desktop import hai module lúc khởi động, phiên hiện tại không tự nạp mã. Không đóng/reset phiên RAM. Bốn ảnh mới 10–13 lưu cùng thư mục marketplace_us, không suy tên máy từ serial nếu chưa đối chiếu.

**Ưu tiên hình người sau Done — cập nhật 18/11:** B21 không đợi hai khung ổn định nếu đã thấy thanh điều hướng sau Done; sang b22 ngay. B22 đọc native trước, thấy tab thì bấm ngay dù vẫn có Loading; không đợi ảnh Trang chủ. Sau Done quét lại mỗi 0,3 giây khi chưa thấy tab. Nếu tab xuất hiện sau Back/Reload thì bỏ thời gian chờ Back/Reload trước cú bấm hình người đầu tiên; vẫn kiểm tra foreground và Stop. `_read_navigation_nodes` chạy trong reader riêng theo serial với operation navigation, trả cây UI ngay khi đủ bằng chứng, không chạy OCR thêm. Dự phòng ngoài ảnh: content-desc/tên tab → resource-id điều hướng → vị trí nội suy từ Home/Cart/Browse trên đúng Android. OCR đọc chữ là dự phòng khi native không đủ, không so khớp toàn ảnh mẫu. Giữ đường Back khi tìm kiếm che thanh tab. 471 unittest PASS: 24 tổ hợp hai luồng × 12 factory thấy tab trên màn Loading rồi bấm cùng mốc thời gian mô phỏng, gồm nhãn/ID/thanh tab; native không gọi OCR, OCR dự phòng, Stop và định tuyến worker đúng serial. Chưa đo dung lượng hoặc thử bấm trên thiết bị thật; việc bấm sớm không phải cơ chế chặn mạng tải ảnh. Phiên đang mở không tự nạp mã mới, không reset dữ liệu RAM.

**Dự phòng Back rồi đọc chữ — bổ sung 18/11:** Giữ đường chạy chính b16–b22 của hai luồng. Chỉ khi đường nhận diện/đọc chữ/Retry hiện có không ra mục mới dùng Back một màn, chờ 0,5 giây, xác nhận Amazon ở trước rồi chụp và OCR ảnh mới trên đúng serial. Ảnh mới được dùng ngay trong cùng bước để tìm lại nhãn tương ứng, không dùng bounds từ màn trước Back và không tua số bước. Bố cục tài khoản không giống ảnh nhưng có một mục Country and language/EN được nhận theo chữ, không đòi đủ các khối Orders/Lists cũ. B17–b21 thiếu mục hai lượt sau các dự phòng cũ mới Back; nếu danh sách quốc gia đã hết 16 lượt cuộn thì có thêm đúng một lần Back/đọc ảnh/mở lại ô Country/Region trước khi thử tiếp. Tổng Back vẫn tối đa ba mỗi lần chạy bước, giữ hạn 75 giây. Không chọn nhãn trùng/vùng không rõ, không Back lại giao dịch Done đang chờ; nếu trở về form xác minh thì dừng riêng. Không sửa SMS/OTP/Create, không phát lại các bước ngẫu nhiên; b22 thấy hình người vẫn bấm ngay. Test mới kiểm 24 tổ hợp Tạo/Đăng nhập × 12 factory: chính thất bại → Back → OCR ảnh mới → bấm Country and language trên bố cục khác; đường chính không thêm Back/OCR, giữ Done đã gửi, gặp auth thì dừng, nhãn trùng không đoán, và chỉ phục hồi danh sách sau khi hết các lượt cuộn cũ. 477 unittest toàn dự án PASS sau bổ sung dự phòng này. Chưa chạy bấm thật; phiên đang mở không tự nạp mã, không đóng/reset dữ liệu RAM.

## E01 — Dừng lỗi và Tiếp tục

Trước khi dừng vì lỗi đọc tạm thời, tool thử lại cây giao diện trong thời hạn của máy. Nếu ADB hết hạn khi bấm nút chuyển màn, tool đọc màn kế tiếp để xác định cú bấm có tới Android chưa. Nếu không xác nhận được, báo màn đã đọc và màn cần thấy. Bước gửi SMS và Create giữ trạng thái đã thử bấm để tránh tự gửi lặp.

Mỗi máy có bước hiện tại và lỗi riêng, không còn đồng hồ tổng 3→4→5→4 phút sau menu. Xong một bước thì chạy bước kế. Khi lỗi không tự giải quyết được, máy dừng tại chỗ; người dùng sửa trực tiếp rồi bấm Tiếp tục để đọc lại UI đúng bước đang dừng. Cập nhật 21/11/2026: sau b11, kể cả b37 hết hạn, Tiếp tục giữ `next_step` và không đọc/tua lại form đăng ký; test mô phỏng PAUSED tại b37 chạy đúng b37, phiên thật chưa nạp bản mới. Nếu máy đang ở màn SĐT dù mốc lưu đã tới b10, tool quay về b4 của chính máy đó và tạo lại trạng thái bước; không xóa hàng dữ liệu. Không gửi SMS hoặc bấm Create lặp khi màn phản hồi chậm; mốc Create đã bấm không tự tua lại. **Đã nối mã và test mô phỏng; cần thử thật sau sửa.** **Sửa Tiếp tục ngày 18/11 theo ảnh Máy 3:** bỏ nhánh xếp Tiếp tục của máy đã có Profile vào cuối mẻ. Máy có ADB nối ngay phiên sau menu; máy có Device ID đã xác nhận chạy worker chuẩn bị riêng, không đợi máy khác. Worker dùng đúng metadata/serial của hàng, không tạo Profile trùng; MENU_OPEN chỉ nối lại ADB. Khóa theo (batch, máy) ngăn hai worker chuẩn bị cùng máy, nhưng không khóa máy khác. Dừng riêng/Dừng cả mẻ và Làm lại vẫn giữ hoặc cách ly đúng worker/queue. Thiếu Device ID đã xác nhận thì báo lỗi rõ trên hàng thay vì chờ im. Đã test mô phỏng, chưa bấm trên phiên thật. **Tiếp tục sau khi người dùng thao tác hộ (18/11):** bỏ chốt chỉ cho tua lùi trong b4–b11. Khi phiên đang dừng, đọc màn thật của đúng serial và đối chiếu hàng SĐT để chọn bước còn cần làm; đã chọn US +1 thì tới Continue, đã tới form tên/xác minh thì bỏ bước trung gian đã qua. Ô OTP đủ sáu số trên đúng máy được nhận làm mã hiện tại và tới nút xác nhận, không gõ lại. Nếu người dùng đã xác nhận SMS và máy đang ở Trang chủ/Browse, tiếp từ b12 bằng dấu hoàn tất thủ công riêng; không chạm Create/Verify lần nữa và không khẳng định tài khoản thành công. Không cho tua qua b1–b3 hoặc các lượt xem ngẫu nhiên chưa hoàn tất. Chưa thử trên phiên Swarmote thật.

## U01 — Màn sau Create chưa được hướng dẫn

Người dùng xác nhận Amazon tự về Trang chủ sau b11; b12 mở ba gạch rồi b13–b15 điều hướng ngẫu nhiên. B16–b22 chung đã được hướng dẫn và nối như mục trên. Chưa có tiêu chí xác nhận tài khoản tạo thành công; chỉ báo xong thao tác tới b22 và chờ b23.

## q5 b1–b3 — Ba thẻ riêng

b1 Toys, Kids and Baby; b2 Office & Professional; b3 Sports & Outdoors. Bấm theo chữ giao diện thật trên đúng serial q5. Nếu sau cú bấm menu vẫn hiện thì tiếp bước kế ngay; nếu mở trang khác thì tự quay về menu trước cú bấm kế. Sau b3 nối b4–b11 chung. Chưa có ảnh q5 hay xác minh trên máy thật.

## q6 b1–b3a — Trang chủ, Giỏ hàng, menu và thẻ

b1 Trang chủ xem 2 giây; b2 Giỏ hàng xem 2 giây; b3 về menu ba gạch; b3a bấm Devices and Electronics ở menu thẻ hoặc Electronics ở menu danh sách. Nếu thẻ mở trang khác, b4 chung tự về menu tìm Sign In. Chưa có ảnh q6 hay xác minh trên máy thật; xem [Q6_FLOW.md](Q6_FLOW.md).

## U02 — q7–q12 dùng phần ngẫu nhiên chung

Người dùng đã cho phép b1–b3 của cả q1–q12 bấm ngẫu nhiên từ menu thật. q7–q12 nay dùng factory chung, không sao chép chuỗi cố định của q1–q6. Chưa thử trên máy thật.

## U03 — Ảnh tiếp theo có thể bổ sung hoặc sửa quy trình

Đây là danh mục **những gì đã biết**, không phải quy trình cuối cùng. Khi nhận ảnh mới, cập nhật đúng máy và mốc, ghi màn trước/sau và mức kiểm chứng, sửa mã nếu cần, rồi cập nhật graph. Không tự điền bước chưa được người dùng chỉ.







\r\n
