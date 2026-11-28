# Ảnh hướng dẫn q1/q2 và menu chung lưu cục bộ

Ảnh trạng thái [Máy 5 chờ tạo lại Profile sau mẻ](flow_images/shared/23nov_machine5_retry_wait.png) do người dùng gửi ngày 23/11/2026 chứng minh nhánh Tiếp tục cũ vẫn xếp hàng khi mẻ đang chạy; ảnh không cho biết Profile đã được tạo hay thao tác mới đã chạy thật.

## Video cuộn tay tới US +1 — 14/11/2026

Video người dùng cung cấp đã sao chép từ `D:\cuonus1.mp4` vào [cuonus1.mp4](flow_images/shared/cuonus1.mp4) theo yêu cầu lưu toàn bộ minh chứng trên Git. Khoảng giây 1 hộp quốc gia ở đầu danh sách; giây 6–8 đã tới các hàng cuối gồm Zimbabwe và Åland Islands; sau một cú vuốt ngược ngắn, United States +1 hiện khoảng giây 9–10; chạm hàng US làm hộp đóng và form hiện US +1 khoảng giây 16. Đây là bằng chứng cho thao tác tay, chưa đo tốc độ hoặc xác nhận hành vi của tool đang chạy. Không ghi lại SĐT trong tài liệu.

Ảnh bổ sung cùng bước ngày 18/11: [b6_bottom_stalled_18nov.png](flow_images/shared/b6_bottom_stalled_18nov.png) có danh sách Uruguay → Åland Islands, chưa thấy US +1; người dùng báo cuộn xuống cuối rồi đứng im. OCR thật nhận COUNTRY. Tính thử cú vuốt ngược từ các hàng trong ảnh: (152,432) → (152,482), 50 px/650 ms; ADB được mock, không có cú vuốt thật. Đã sửa đọc có hạn và vuốt ngược trực tiếp, test hai luồng qua một cú nhẹ rồi chọn US; chưa chứng minh phiên tool đang mở đã nạp mã.

## q1 b6 — US +1 hiện nhưng chạm không đóng hộp, 14/11/2026

- [15_b6_us_tap_error.png](flow_images/q1/15_b6_us_tap_error.png): tool báo chạm US +1 bốn lần nhưng Country vẫn mở.
- [16_b6_us_visible.png](flow_images/q1/16_b6_us_visible.png): United States +1 nhìn thấy rõ giữa United Kingdom và Uruguay; hàng trải rộng hơn bounding box chữ. Hai ảnh dùng để sửa b6 chung, chưa phải xác nhận trên máy thật sau sửa.

## q3/q4 — Ba ảnh đính kèm ngày 13/11/2026

- `codex-clipboard-1d920273-d283-4fca-9ed4-4b45b52b1f91.png`: menu thẻ, dùng cho q3 b1 Groceries and Drinks, b2 Home and DIY, b3 Books and Reading. Chữ một số thẻ xuống hai dòng.
- `codex-clipboard-88352ef6-876b-4830-b541-3a5252c8d547.png`: q4 b1, giỏ hàng trống và tab giỏ đang chọn.
- `codex-clipboard-9782ceeb-dabd-43c1-bfed-44c382ad92e2.png`: q4 b2 Pets được mở rộng với Pet Supplies/Dogs/Cats/Birds. Người dùng yêu cầu b3 Home and DIY trên menu; chưa có ảnh riêng đánh dấu q4 b3.

Các tệp mới ở thư mục đính kèm cục bộ, chưa chép vào repository công khai. OCR thật trong RAM đọc được ba nhãn q3, nhận màn giỏ hàng q4 và nhãn Pets; không ghi dữ liệu tài khoản trong ảnh ra log. Xem Q3_FLOW.md và Q4_FLOW.md.

## B6 — Hai ảnh đính kèm mới ngày 13/11/2026

`codex-clipboard-7deb55eb-dc22-4a3c-834d-f1712a2bd9f2.png` cho thấy hộp Country/region code với United States +1 giữa United Kingdom +44 và Uruguay +598; phía dưới là Uzbekistan, Vanuatu, Vatican City, Venezuela, Vietnam, Wallis a Futuna và Western Sahara. Người dùng hướng dẫn cuộn nhanh về cuối rồi vuốt ngón tay xuống ngắn để tìm lại US. `codex-clipboard-94c6d956-0ede-4e43-b4c8-886d3254af1e.png` báo b6 vẫn đọc COUNTRY trong lúc chờ IDENTIFIER. Ảnh nằm ở tệp đính kèm cục bộ, chưa sao chép vào repository. OCR thật đọc được COUNTRY và United States +1; chưa có thao tác kiểm thử trực tiếp trên thiết bị.

Các ảnh người dùng gửi đã được sao chép vào `flow_images/` để phiên sau xem lại pixel. Ảnh được lưu cùng mã nguồn theo yêu cầu bàn giao đầy đủ; repository GitHub hiện là **công khai** và ảnh có thể hiển thị SĐT hoặc OTP đã xuất hiện trong ảnh gốc. Không chép lại các giá trị này sang log hoặc tài liệu. Graphify chỉ lập chỉ mục các tiêu đề và liên kết dưới đây, **không đọc nội dung pixel**.

## q1 ảnh 01 — Menu và ba thẻ

[01_menu_cards.png](flow_images/q1/01_menu_cards.png): Gifting, Pets, Fashion and Beauty được đánh dấu b1–b3.

## q1 ảnh 02 — Sign In cuối menu

[02_sign_in_menu.png](flow_images/q1/02_sign_in_menu.png): hàng Sign In b4.

## q1 ảnh 03 — Nhập số điện thoại

[03_phone_input.png](flow_images/q1/03_phone_input.png): form nhập số b5.

## q1 ảnh 04 — Chọn mã quốc gia

[04_country_reference_q6.png](flow_images/q1/04_country_reference_q6.png): United States +1 b6. Tiêu đề cửa sổ trong ảnh là **q6**, nên đây là tham chiếu giao diện cho q1, chưa phải bằng chứng q1 thật.

## q1 ảnh 05 — Continue số điện thoại

[05_continue_number.png](flow_images/q1/05_continue_number.png): nút Continue b7.

## q1 ảnh 06 — Tạo tài khoản mới

[06_new_account.png](flow_images/q1/06_new_account.png): Proceed to create an account b8.

## q1 ảnh 07 — Form tên

[07_name_form.png](flow_images/q1/07_name_form.png): First and last name b9.

## q1 ảnh 08 — Chọn SMS thay WhatsApp

[08_whatsapp_sms_choice.png](flow_images/q1/08_whatsapp_sms_choice.png): Send code by SMS b10.

## q1 ảnh 09 — Nhập OTP SMS

[09_sms_otp.png](flow_images/q1/09_sms_otp.png): Verify mobile number, ô OTP SMS và nút Create b11. **Chưa có ảnh sau khi bấm Create.**

## q1 ảnh 10 — Form SĐT hiện tại

[10_identifier_current.png](flow_images/q1/10_identifier_current.png): q1 ở màn `Sign in or create account` với ô SĐT trống. Người dùng xác nhận đây là màn hiện tại sau các lần dừng. Khi bấm Tiếp tục, luồng chung cần đọc lại màn, quay về b4 và chạm ô trước khi gõ.

## q1 ảnh 11 — Lỗi b6 vùng bấm

[11_b6_invalid_region.png](flow_images/q1/11_b6_invalid_region.png): thông báo `Vùng bấm Amazon không hợp lệ` khi chọn US +1. Cây UI có thể có mục US ẩn hoặc bounds bằng 0; cần cuộn đến mục đang hiển thị thay vì bấm mục ẩn.

## q1 ảnh 12 — Lỗi b9 Continue

[12_b9_continue_ambiguous.png](flow_images/q1/12_b9_continue_ambiguous.png): thông báo có nhiều phần tử `Continue`. Chọn nút đang hiển thị, có thể bấm và thuộc form tên.

## q1 ảnh 13 — Lỗi URL OTP ở b10

[13_b10_otp_http403.png](flow_images/q1/13_b10_otp_http403.png): URL OTP trả HTTP 403 trước khi tool gửi SMS. Người dùng yêu cầu bấm gửi SMS trước, rồi mới đọc URL.

## q1 ảnh 14 — Lỗi b10 màn không khớp

[14_b10_not_whatsapp.png](flow_images/q1/14_b10_not_whatsapp.png): b10 báo q1 chưa ở màn chọn SMS; cần đọc lại màn hiện tại khi Tiếp tục và quay về đúng bước chung của máy này.

Hai ảnh người dùng gửi 17/11 (`codex-clipboard-a6f1474a-d530-4bdd-9e58-a29be4c7896c.png`, `codex-clipboard-ef43aef2-5fb4-4e49-9d86-bbb7dcc4b530.png`) cho thấy bảng của Máy 1 báo màn chuyển chậm `(WHATSAPP)` và màn Amazon vẫn có nút `Send code by SMS`. Ảnh không cho biết tool đang ở b7 hay b10; không chép ảnh có SĐT vào repository công khai. Mã mới xử lý cả hai đường chờ, chưa xác minh trên máy thật.

## q2 ảnh 01 — Trang chủ

[01_home.png](flow_images/q2/01_home.png): b1 bấm tab nhà, xem 2–5 giây.

## q2 ảnh 02 — Menu và Pets

[02_menu_pets.png](flow_images/q2/02_menu_pets.png): b2 menu ba gạch, b3 Pets.

## Menu chung ảnh 01 — Danh sách chữ

[01_list_menu.png](flow_images/shared/01_list_menu.png): biến thể menu ba gạch gồm `Shop by Category`, các hàng danh mục và `Sign In`. Người dùng yêu cầu bấm Home, chỉ xem 2–5 giây, quay về menu rồi làm b4 Sign In. Bộ phân loại xử lý theo cây UI đang hiển thị, không phụ thuộc ảnh này; xem [MENU_ROUTING.md](MENU_ROUTING.md).

## Menu chung ảnh 02 — App Store bên phải sau khi Amazon mở

[02_apps_panel_open.png](flow_images/shared/02_apps_panel_open.png): panel App Store vẫn mở ở bên phải trong khi Amazon đã hiện ở điện thoại. Bấm lại nút Apps đang được chọn để thu panel, rồi mới tiếp tục mở menu. Áp dụng chung cho tất cả máy; chỉ bấm khi panel còn hiện.

## q1 ảnh lỗi mới 01–06 — b6, b9, b10

- [01_b6_error.png](flow_images/q1/latest_errors/01_b6_error.png): lỗi vùng bấm ở b6.
- [02_country_open.png](flow_images/q1/latest_errors/02_country_open.png): danh sách quốc gia còn ở đầu chữ A; phải cuộn tới United States +1 đang hiện và có bounds hợp lệ.
- [03_b9_error.png](flow_images/q1/latest_errors/03_b9_error.png): thông báo nhiều `Continue` ở b9.
- [04_name_form.png](flow_images/q1/latest_errors/04_name_form.png): form tên có bàn phím mở và một nút Continue nhìn thấy dưới ô tên.
- [05_b10_error.png](flow_images/q1/latest_errors/05_b10_error.png): thông báo URL OTP HTTP 403 khi tool ghi b10.
- [06_whatsapp.png](flow_images/q1/latest_errors/06_whatsapp.png): màn vẫn là Verify with WhatsApp, nút Send code by SMS chưa được bấm. Ảnh này cho thấy bản đang chạy đã đọc URL trước khi gửi SMS; mã nguồn hiện tại đọc URL ở b11 sau khi xác nhận màn SMS. Chưa kiểm chứng phiên tool đang chạy nạp phiên bản mã nào.

Ảnh bảng trạng thái người dùng gửi ngày 17/11 báo `Dừng tại b11 bấm Create your Amazon account` vì không xác định nút vàng dưới ô OTP. Người dùng xác nhận máy đó đi **nhánh đăng nhập** khi nhảy sớm tới xác minh; ảnh này chỉ chứa bảng trạng thái, không chứa màn Android SMS. Không dùng ảnh đó làm bằng chứng nhãn nút Verify trên thiết bị. Đường tạo tài khoản theo các ảnh cũ vẫn dùng Create.

Ảnh bảng trạng thái tiếp theo ngày 17/11 báo `Dừng tại b11 nhập OTP: Chưa xác nhận được nội dung ô 'Enter security code'`. Người dùng nói mã đã được gõ nhưng nút vàng chưa được bấm; đây là nhánh đăng nhập. Ảnh chỉ có thông báo tool, chưa thấy ô OTP hoặc nút trên Android nên không dùng làm bằng chứng pixel của nút.

Hai ảnh tiếp theo ngày 17/11 cho thấy **màn Android thật** của nhánh đăng nhập: OTP đã hiện trong ô, nút vàng ngay dưới ô ghi `Verify mobile number`, và tiêu đề phía trên cũng ghi đúng cụm này. Người dùng xác nhận lại ngày 18/11 rằng ảnh này là **đăng nhập**, không phải tạo tài khoản. Ảnh thông báo tool báo nhánh đăng nhập “chưa thấy nút Verify”; nguyên nhân là mã tìm nhãn `Verify` không khớp nút thật. Không ghi lại mã OTP hoặc SĐT từ ảnh vào tài liệu. Bộ chọn phải lấy nút cùng nhãn ở dưới ô mã, không lấy tiêu đề.

Đọc pixel trực tiếp trên ảnh này cho thấy chữ đen ở giữa làm ngắt các hàng vàng liên tục; ngưỡng dò cũ không nhận được nút. Ngưỡng riêng của nhánh đăng nhập nhận đúng một vùng vàng dưới ô OTP, không cần OCR để xác định màu. Kết quả này chỉ xác nhận bộ chọn trên ảnh tĩnh, chưa xác nhận cú bấm trên máy thật. Ngày 18/11, sau khi cài ONNX Runtime 1.20.1 và sửa nhận diện viền ô nhập chồng nhau, OCR đọc được ô mã đủ sáu ký tự và vùng nút Verify nằm dưới ô từ chính ảnh này; không lưu giá trị mã hoặc SĐT.

## q1 ảnh 15 — b4 Sign In trên menu danh sách

[15_b4_list_sign_in_ambiguous.png](flow_images/q1/15_b4_list_sign_in_ambiguous.png): q1 hiện menu dạng danh sách, Sign In nằm dưới Customer Service nhưng tool báo không xác định được duy nhất `Sign In`. Bộ chọn b4 cần ưu tiên phần tử có thể bấm, hoặc phần tử ở dưới Customer Service khi cây UI trả nhãn lặp. Chưa có ADB dump của chính máy này để xác minh thuộc tính các node.

Ảnh mới về menu ngẫu nhiên được lập danh mục bên dưới. Khi nhận ảnh khác, lưu tên theo máy và thứ tự, cập nhật `STEP_INVENTORY.md`, file Qn tương ứng, `PROJECT_HANDOFF.md` rồi cập nhật Graphify.

## 14 ảnh menu chung b1–b3 ngẫu nhiên — 14/11/2026

Ảnh người dùng gửi chỉ là tham chiếu giao diện, không ghi máy qN hoặc chứng minh tool đã bấm thành công. Viền xanh cho biết một thẻ đang mở; các hàng mục con xuất hiện ngay trong menu. Khi cuộn xuống, `Shop by category` có thể ra khỏi khung nhìn; `Sign In` nằm ở cuối menu và chỉ dành cho b4. B1–b3 được phép bấm thẻ hoặc mục con đang hiện, không lấy tọa độ cố định từ các ảnh này. Lời nhắc 18/11: chọn mục con sang trang khác vẫn xem đủ lượt và đủ cả b1–b3, mở ba gạch ở lượt kế; b12–b15 cũng mở lại menu khi sang trang khác.

- [01_menu_cards.png](flow_images/shared/random_prefix_reference/01_menu_cards.png): đầu menu với các thẻ danh mục và tab menu.
- [02_menu_bottom_sign_in.png](flow_images/shared/random_prefix_reference/02_menu_bottom_sign_in.png): cuối menu, Customer Service và Sign In dưới các thẻ Office, Sports, Your Stuff.
- [03_gifting_expanded.png](flow_images/shared/random_prefix_reference/03_gifting_expanded.png): Gifting mở Gift Cards.
- [04_deals_expanded.png](flow_images/shared/random_prefix_reference/04_deals_expanded.png): Deals & Savings mở Today's Deals, Bank Promotions, Clearance Store, Promotions, Vouchers.
- [05_inspired_expanded.png](flow_images/shared/random_prefix_reference/05_inspired_expanded.png): Be Inspired, Save More mở International Store và Weekly New Arrivals.
- [06_groceries_expanded.png](flow_images/shared/random_prefix_reference/06_groceries_expanded.png): Groceries and Drinks mở Grocery.
- [07_health_expanded.png](flow_images/shared/random_prefix_reference/07_health_expanded.png): Health and Personal Care mở Health & Personal Care.
- [08_pets_expanded.png](flow_images/shared/random_prefix_reference/08_pets_expanded.png): Pets mở Pets Supplies, Dogs, Cats, Birds, Fish, Small Animals.
- [09_fashion_expanded.png](flow_images/shared/random_prefix_reference/09_fashion_expanded.png): Fashion and Beauty mở Fashion, Apparel, Shoes, Watches, Jewellery, Beauty, Luxury Beauty.
- [10_home_diy_expanded.png](flow_images/shared/random_prefix_reference/10_home_diy_expanded.png): Home and DIY mở Home & Kitchen, Lawn & Garden, Arts, Crafts & Sewing, DIY Tools & Automotive.
- [11_devices_expanded.png](flow_images/shared/random_prefix_reference/11_devices_expanded.png): Devices and Electronics mở Electronics, Mobile & Accessories, Computers, Tablets, TV.
- [12_music_expanded.png](flow_images/shared/random_prefix_reference/12_music_expanded.png): Music, Video and Gaming mở Music, Musical Instruments, Video Games, DVD, Gaming Store.
- [13_books_expanded.png](flow_images/shared/random_prefix_reference/13_books_expanded.png): Books and Reading mở Books, STEAM Store; Sign In ở phía dưới.
- [14_toys_expanded.png](flow_images/shared/random_prefix_reference/14_toys_expanded.png): Toys, Kids and Baby mở Toys & Games, Baby, Baby Clothes, Girls' Clothes, Boys' Clothes, STEAM Store.

Ảnh báo lỗi bổ sung 18/11: [15_q4_prefix_read_recovery.png](flow_images/shared/random_prefix_reference/15_q4_prefix_read_recovery.png) cho thấy Máy 4 báo “Đọc màn hình chưa xong · đang tự phục hồi lần 45”. Người dùng báo sau lượt ngẫu nhiên sang màn lạ phục hồi lâu. Ảnh chỉ có bảng trạng thái, không xác định màn Android hoặc bước đang chạy. Kiểm tra mã tìm thấy `_prefix_nodes` gọi bộ đọc tự lặp nên thời hạn 12 giây không dừng được vòng này; đã đổi sang đọc một lượt có ngân sách, thêm Browse/Back dự phòng và test. Chưa xác minh cú bấm trên máy thật.

Ảnh lỗi b13–b15 bổ sung 18/11: [16_q1_lens_camera_permission.png](flow_images/shared/random_prefix_reference/16_q1_lens_camera_permission.png) là Lens có hộp Allow camera access, Not now và Allow access; [17_b15_browse_recovery_error.png](flow_images/shared/random_prefix_reference/17_b15_browse_recovery_error.png) báo b15 không tìm lại được Browse sau ba lượt đọc. Người dùng nói ô tìm kiếm làm bàn phím che tab. OCR thật trên ảnh 16 nhận overlay và một Not now, không có ứng viên chọn ngẫu nhiên. Mã đã lọc đầu vào/camera và bổ sung thoát màn trước khi mở Browse; đây là đối chiếu ảnh và test mô phỏng, chưa thao tác trên máy thật.
Ảnh ngày 19/11: [18_b14_wait_menu.png](flow_images/shared/random_prefix_reference/18_b14_wait_menu.png) là trạng thái b14 lặp “chờ Trang chủ và menu”; không cho thấy màn Android. Theo yêu cầu mới, b13–b15 chọn điều hướng đang hiện trước, chỉ dùng ba gạch/Back khi không có mục, không chờ Trang chủ giữa các lượt.

## Tạo tài khoản b23–b25 — Account và Your Addresses (19/11/2026)

- [01_b23_account.png](flow_images/shared/create_address/01_b23_account.png) và [13_b23_account_closeup.png](flow_images/shared/create_address/13_b23_account_closeup.png): Sau b22 giữ chờ 3 giây; thấy chữ Account trong ảnh thì bấm ngay, không cần điều kiện nhận diện trang khác.
- [02_b24_top.png](flow_images/shared/create_address/02_b24_top.png): Đầu trang Account; Your Addresses chưa hiện, cần cuộn xuống.
- [03_b24_addresses.png](flow_images/shared/create_address/03_b24_addresses.png) và [14_b24_your_addresses_closeup.png](flow_images/shared/create_address/14_b24_your_addresses_closeup.png): Your Addresses đã hiện dưới Account settings; thấy đúng chữ thì chọn, không đòi thêm nhãn khác. Người dùng báo đôi khi quảng cáo chen vào sau b23 cần Back; chưa có ảnh quảng cáo riêng.
- [04_b25_addresses.png](flow_images/shared/create_address/04_b25_addresses.png): Mục Your Addresses cần bấm ở b25; ảnh sau cú bấm là 05_b26_add_new_address.png.
- [05_b26_add_new_address.png](flow_images/shared/create_address/05_b26_add_new_address.png): Trang Your Addresses; b26 chọn Add a new address.
- [06_b27_enter_manually.png](flow_images/shared/create_address/06_b27_enter_manually.png): B27 chọn Enter an address manually. Ảnh chữ xanh mới ngày 23/11 xác nhận bấm `Enter an address manually` rồi bàn phím/form mở; b28 nhập số ngay, không đợi xác nhận focus bằng OCR/cây Android.
- [07_b28_street_form.png](flow_images/shared/create_address/07_b28_street_form.png): Form địa chỉ sau b27; b28 hiện nhập số tìm địa chỉ ngay vào bàn phím đang mở, không đọc/kiểm ô Street trước khi nhập.
- [08_b28_suggestions.png](flow_images/shared/create_address/08_b28_suggestions.png): Sau khi nhập số, thấy gợi ý địa chỉ thì chọn ngay một dòng, không đợi xác nhận ZIP.
- [09_b29_default_address.png](flow_images/shared/create_address/09_b29_default_address.png) và [15_b29_empty_checkbox_closeup.png](flow_images/shared/create_address/15_b29_empty_checkbox_closeup.png): Sau khi chọn gợi ý, tìm chữ Make this my default address rồi bấm thẳng ô vuông bên trái một lần; ảnh cận cảnh cho thấy ô ban đầu trống. Không đọc trạng thái ô trước hoặc sau cú bấm.
- [10_b30_add_address.png](flow_images/shared/create_address/10_b30_add_address.png) và [16_b30_add_address_closeup.png](flow_images/shared/create_address/16_b30_add_address_closeup.png): B30 cuộn khi chưa thấy Add address, thấy chữ thì bấm ngay; sau cú bấm mới đọc kết quả lưu.
- [11_b31_address_saved.png](flow_images/shared/create_address/11_b31_address_saved.png): Address saved/Personal Addresses xác nhận b30; b31 bấm tab hình người ở thanh dưới, b32 cuộn ngay để tìm Reload Balance, không đọc xác nhận Account.
- [12_proxy_test_postal.png](flow_images/shared/create_address/12_proxy_test_postal.png): Sau Test Passed của Swarmote, mã bưu chính cạnh City; lấy 4 chữ số đầu cho b28 của đúng máy (ví dụ 36547 → 3654), nếu không đọc được thì dùng dự phòng cũ.

### B32–b39 — Reload Balance, thêm thẻ và địa chỉ thanh toán (21/11/2026)

- [01_b32_account_reload_balance.png](flow_images/shared/reload_payment/01_b32_account_reload_balance.png) và [11_b33_reload_balance_closeup.png](flow_images/shared/reload_payment/11_b33_reload_balance_closeup.png): Sau tab hình người, cuộn tìm đúng chữ Reload Balance rồi bấm ngay.
- [02_b34_reload_product_top.png](flow_images/shared/reload_payment/02_b34_reload_product_top.png): Đầu trang Amazon Gift Card Balance Reload trước khi cuộn.
- [03_b36_buy_now.png](flow_images/shared/reload_payment/03_b36_buy_now.png) và [12_b36_buy_now_closeup.png](flow_images/shared/reload_payment/12_b36_buy_now_closeup.png): Sau Reload Balance, vuốt ngắn ngay trên màn mới; thấy Buy Now thì bấm ngay, không đọc lại ở bước sau.
- [04_b37_add_payment_method.png](flow_images/shared/reload_payment/04_b37_add_payment_method.png) và [13_b37_card_option_closeup.png](flow_images/shared/reload_payment/13_b37_card_option_closeup.png): Thấy Add a credit or debit card thì bấm ngay, không chọn Set up now.
- [05_b38_card_form_empty.png](flow_images/shared/reload_payment/05_b38_card_form_empty.png): Form thẻ ba ô đang trống, nút Add and continue chưa hoạt động. OCR vùng 5–58% của ảnh trống này nhận đủ ba ô; b38 xác định cả ba trước khi nhập.
- [06_b38_add_and_continue.png](flow_images/shared/reload_payment/06_b38_add_and_continue.png): Form đã nhập, nút Add and continue sáng; ảnh mới cùng trạng thái đã được kiểm tra OCR vùng nút và không lưu thêm vì chứa dữ liệu thẻ. Sau khi nhập xong, thấy chữ Add and continue thì bấm ngay. Ảnh b39 được lưu nguyên bản theo yêu cầu người dùng; xem mục riêng bên dưới.
- [14_b39_use_this_address.png](flow_images/shared/reload_payment/14_b39_use_this_address.png): màn Select a billing address với nút Use this address. Ảnh nguyên bản có tên và địa chỉ cá nhân; không chép lại các giá trị vào văn bản.
- [07_b34_product_stalled.png](flow_images/shared/reload_payment/07_b34_product_stalled.png): ảnh mới 21/11 cho thấy trang Amazon Gift Card Balance Reload đã hiện nhưng Buy Now còn dưới màn; người dùng yêu cầu vuốt ngắn từ dưới lên.
- [08_b34_error.png](flow_images/shared/reload_payment/08_b34_error.png): tool dừng ở b34 vì chưa thấy mục cần bấm, dù ảnh trang sản phẩm đã hiện. Chưa xác nhận phiên tool đang mở đã nạp mã mới.
- [09_b37_visible_card_option.png](flow_images/shared/reload_payment/09_b37_visible_card_option.png): ảnh mới cho thấy rõ Add a credit or debit card trên Your Auto-Reload Setting; OCR vùng 20–65% đọc được chữ và vị trí.
- [10_b37_not_found_error.png](flow_images/shared/reload_payment/10_b37_not_found_error.png): tool báo dừng b37 vì không thấy mục dù ảnh bên cạnh có nút; chưa xác nhận phiên hiện tại đã nạp sửa đổi.

## B16–b22 chung — Đổi marketplace sang United States (18/11/2026)

Bảy ảnh gốc người dùng gửi đã được lưu nguyên bản, áp dụng cho cả Tạo và Đăng nhập. Ảnh có cả vùng điều khiển Swarmote bên phải; mã thao tác Android theo serial, không bấm theo tọa độ toàn ảnh.

| Mốc | Ảnh gốc | Thao tác được hướng dẫn |
| --- | --- | --- |
| b16 | [01_b16_account_tab.png](flow_images/shared/marketplace_us/01_b16_account_tab.png) | Tab hình người ở thanh dưới; màn tài khoản có thể báo lỗi tải các khối nội dung. |
| b17 | [02_b17_locale_button.png](flow_images/shared/marketplace_us/02_b17_locale_button.png), [14_b17_en_closeup.png](flow_images/shared/marketplace_us/14_b17_en_closeup.png) | Sau khi bấm hình người, thấy chữ EN cạnh cờ thì bấm ngay; không cần nhận diện toàn trang Account. |
| b18 | [03_b18_country_setting.png](flow_images/shared/marketplace_us/03_b18_country_setting.png) | Mở ô Country/Region trên màn Country/Region and Language. |
| b19 | [04_b19_country_list_top.png](flow_images/shared/marketplace_us/04_b19_country_list_top.png) | Vuốt từ dưới lên trong danh sách marketplace để tìm United States. Không phải danh sách mã điện thoại US +1 của b6. |
| b20 | [05_b20_united_states.png](flow_images/shared/marketplace_us/05_b20_united_states.png) | Chọn hàng United States / Amazon.com. |
| b21 | [06_b21_done_us.png](flow_images/shared/marketplace_us/06_b21_done_us.png) | Ô Country/Region đã là United States; bấm Done. |
| b22 | [07_b22_account_after_done.png](flow_images/shared/marketplace_us/07_b22_account_after_done.png) | Sau Done thấy tab hình người là bấm ngay; chỉ chờ khi chưa tìm được tab, không đợi ảnh Trang chủ; chưa có hướng dẫn b23. |

Ảnh bổ sung 18/11: [08_b16_menu_before_account.png](flow_images/shared/marketplace_us/08_b16_menu_before_account.png) cho thấy menu đang cuộn thấp, hình người vẫn ở thanh dưới; [09_b16_focus_error.png](flow_images/shared/marketplace_us/09_b16_focus_error.png) báo “Amazon chưa ở phía trước”. Người dùng xác nhận ảnh b16 ban đầu là kết quả sau khi bấm tab, không phải màn tool phải đợi trước khi bấm. OCR ảnh menu mới nhận MENU. ADB read-only trên hai serial đang online xác nhận lệnh `dumpsys window windows` không xuất focus; full `window` và `activity activities` đều thấy Amazon, có display phụ focus null. Mã đã sửa guard và test cú bấm hình người từ menu/thiếu nhãn icon; chưa bấm thật hoặc nạp lại phiên RAM.

Ảnh lỗi bổ sung cùng mục ngày 18/11: [10_q3_b16_focus_error.png](flow_images/shared/marketplace_us/10_q3_b16_focus_error.png), [11_search_keyboard_without_tabs.png](flow_images/shared/marketplace_us/11_search_keyboard_without_tabs.png), [12_q3_b16_focus_error_detail.png](flow_images/shared/marketplace_us/12_q3_b16_focus_error_detail.png), [13_b17_focus_error.png](flow_images/shared/marketplace_us/13_b17_focus_error.png). Ảnh 11 là màn tìm kiếm Amazon.sg có bàn phím, chưa có thanh tab hình người/ba gạch để bấm. OCR thật nhận search=True, navigation_ready=False. Mã đã thêm Back có giới hạn và đọc lại thanh điều hướng; test mô phỏng qua đủ b16–b22, chưa bấm trên Android thật. Các ảnh báo focus không chứng minh app khác đang ở trước; ADB đọc hiện tại xác nhận Amazon. Phiên tool đang mở có từ trước bản sửa focus và chưa tự nạp mã.

OCR thật bằng môi trường .venv đã nhận đúng loại màn của cả 7 ảnh, chọn được vùng EN, Country/Region, United States và Done trên ảnh tĩnh. Dòng Previously visited có United States không chứng minh quốc gia hiện tại đã chọn US; phải đối chiếu ô Country/Region phía trên. Chưa kiểm chứng cú bấm, cuộn hoặc thay marketplace trên Swarmote thật.

**Ảnh bổ sung luồng Settings “Đổi US từ đầu” ngày 28/11/2026:** [01_account_tab.png](flow_images/shared/change_us_from_start/01_account_tab.png) là biểu tượng hình người cho b2/b7; [02_en.png](flow_images/shared/change_us_from_start/02_en.png) là cờ/EN cho b3; [03_country_card.png](flow_images/shared/change_us_from_start/03_country_card.png) là ô Country/Region Singapore cho b4. [account_tab_template.png](flow_images/shared/change_us_from_start/account_tab_template.png) là crop chỉ chứa biểu tượng; b2 nay bấm trực tiếp theo kích thước máy, còn b7 vẫn dùng ảnh khi thiếu nhãn. Crop đã khớp hai ảnh toàn màn b16/b22 có sẵn. [05_b2_account_selected.png](flow_images/shared/change_us_from_start/05_b2_account_selected.png) do người dùng gửi sau khi bấm Tiếp tục cho thấy tab hình người đang được chọn và màn Account đã mở, dù tool còn báo dừng ở b2; đây là bằng chứng lỗi nhận diện/phiên mã cũ, không phải lỗi tọa độ. B5–b7 dùng chứng cứ United States/Done/hình người trong bộ ảnh b19–b22 phía trên; ảnh b8–b17 được mô tả ngay dưới đây. Ảnh và test mô phỏng chưa phải lượt chạy máy thật.

Chín ảnh gốc người dùng gửi tiếp trong cùng luồng đã được lưu nguyên bản theo yêu cầu đẩy đủ ảnh: [b8_create_account.png](flow_images/shared/change_us_from_start/b8_create_account.png), [b9_phone_field.png](flow_images/shared/change_us_from_start/b9_phone_field.png), [b10_continue_phone.png](flow_images/shared/change_us_from_start/b10_continue_phone.png), [b11_proceed.png](flow_images/shared/change_us_from_start/b11_proceed.png), [b12_name_field.png](flow_images/shared/change_us_from_start/b12_name_field.png), [b13_continue_name.png](flow_images/shared/change_us_from_start/b13_continue_name.png), [b14_b15_otp_create.png](flow_images/shared/change_us_from_start/b14_b15_otp_create.png), [b16_google_spanish.png](flow_images/shared/change_us_from_start/b16_google_spanish.png), [b17_passkey.png](flow_images/shared/change_us_from_start/b17_passkey.png). B14 và b15 dùng chung một ảnh. OCR ảnh tĩnh nhận đủ nhãn b8–b17, gồm dấu hiệu hộp Google b16 và màn không còn hộp b17. Ảnh có SĐT/tên/OTP; phần chữ bàn giao không chép lại các giá trị đó. Ảnh tĩnh chưa chứng minh thao tác trên máy thật.

Ảnh bổ sung b16 [04_b16_google_english.png](flow_images/shared/change_us_from_start/04_b16_google_english.png) cho thấy sau Back lần đầu, hộp Google có thể vẫn che màn và đổi sang tiếng Anh (`Sign in to your Google Account to create passkeys`, `Cancel`, `Sign in`). OCR ảnh tĩnh nhận đúng hộp; b16 đọc lại rồi Back lần hai nếu hộp vẫn còn, tối đa hai cú Back và chỉ sang b17 sau khi thấy hộp đã ẩn. Ảnh không chứa SĐT/OTP và được lưu cùng nhóm luồng mới.
