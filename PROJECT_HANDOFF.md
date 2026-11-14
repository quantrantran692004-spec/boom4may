## Bản thử State Machine q7 và b1–b3 mở mục con — 14/11/2026

Trên nhánh `codex/q7-stage2`, chỉ b1–b3 của q7 thử bấm mục con có nhãn trong 14 ảnh tham
chiếu sau khi bấm thẻ, rồi xem thêm 10 giây mỗi bước (thêm tổng 30 giây). Nếu
không đọc được mục con hợp lệ từ cây Android hoặc cú bấm lỗi thì thử thẻ khác;
không đánh dấu hoàn tất chỉ vì bấm thẻ ngoài. Trước b4 quay về Browse menu.
Các máy khác giữ nguyên `random_prefix.py` và ba lượt hiện hành.

Q7 là máy duy nhất nối bản thử State Machine giai đoạn 2 quanh b4–b11. Module
`q7_state_machine.py` kiểm tra màn trước, dùng hành động chung hiện có, đọc
lại màn sau, giới hạn thời gian theo trạng thái và dừng khi màn lạ/sai. Sau
Create luôn dừng báo chưa có màn kết quả được hướng dẫn, không báo tài khoản
thành công. q1–q6 và q8–q12 không đổi đường b4–b11. Đã qua unittest mô phỏng;
chưa thử q7 thật. Người dùng sẽ tự thử q7; không tự đóng phiên tool đang mở vì
dữ liệu mẻ chỉ ở RAM. Xem [Q7_STATE_MACHINE_PILOT.md](Q7_STATE_MACHINE_PILOT.md).
Kết quả test ở cuối [Q7_STATE_MACHINE_PILOT.md](Q7_STATE_MACHINE_PILOT.md);
chỉ mô phỏng, chưa nghiệm thu q7 thật.
Trên nhánh này `_wait_screen()` chỉ đổi cách xử lý khi nhận `StateDeadline`
của q7: màn cũ hợp lệ được chờ có hạn, màn sai nhánh dừng, `UNKNOWN` không
chờ vô hạn. Các máy khác vẫn dùng `AttemptDeadline` cũ. Q7 b1–b3 có hạn
90 giây mỗi lượt. 334/334 unittest PASS; chưa chạy đăng ký thật.

## Thẻ tùy chọn khi dán nhiều hàng Amazon — 14/11/2026

Trong ô **Thông tin Amazon**, hàng `SĐT | Mật khẩu | Tên | URL OTP` hoặc hàng có cột thẻ trống đều hợp lệ; có thể trộn cùng hàng có thẻ trong một lần dán. Parser đã cho phép thẻ rỗng nhưng `Window._input_issue` trước đây vẫn bắt buộc trường thẻ cho mọi máy. Nay bộ kiểm tra chỉ yêu cầu SĐT, mật khẩu, tên và URL OTP; nếu thẻ có giá trị thì vẫn kiểm tra định dạng như cũ. Placeholder ghi thẻ tùy chọn. Kiểm thử dùng dữ liệu giả, không thao tác máy thật.

## B1–b3 xem menu ngẫu nhiên cho 12 máy — 14/11/2026

Theo chỉ dẫn mới nhất, b1–b3 chỉ cần xem/bấm các vùng thẻ và mục con được đánh đỏ trong 14 ảnh tham chiếu, không yêu cầu OCR hoặc xác nhận thẻ đã mở. `random_prefix.py` lấy kích thước Android thật theo serial của từng máy, chọn các điểm tỷ lệ trong vùng danh mục, giữ 1 giây sau cú bấm, thử tối đa bốn điểm và vuốt khi lệnh ADB lỗi. Trước b2/b3 và b4, tool chạm nút menu ba gạch theo kích thước máy; b4–b11 vẫn dùng bộ nhận diện hiện hành. Một mẻ mới dùng batch_id để xáo 12 điểm đầu: b1 của 12 máy khác nhau, nên cả chuỗi b1–b3 không trùng trong mẻ. Nếu không có lệnh bấm nào được ADB xác nhận, giữ đúng bước và tự thử lại; không chuyển thẳng b4. 307 unittest PASS, chưa thử 12 máy thật. `.venv` đang chạy có ONNX Runtime 1.32 bị crash khi import; bản 1.20.1 trong thư mục thử nghiệm chạy OCR được trên 14 ảnh, nhưng chưa thay `.venv` vì phiên tool đang mở dùng nó. Cần xử lý phiên chạy và kiểm thử b4 riêng sau khi dữ liệu mẻ được giữ an toàn.

## Dán bảng Amazon có ghi chú thẻ live và URL OTP escaped — 14/11/2026

`bulk_input.parse_records(account_table=True)` nhận hàng tab nhiều cột trống với thẻ dạng `số|tháng|năm|live=>√【nguồn】` và URL OTP dán dạng `https\://...\`. Parser chỉ giữ ba thành phần thẻ, bỏ ghi chú nguồn, bỏ ký tự escape của URL rồi áp dụng kiểm tra URL/token cũ; ánh xạ cùng hàng SĐT, mật khẩu, tên, thẻ, URL giữ nguyên. Dùng dữ liệu giả trong test, không ghi giá trị thật người dùng gửi vào mã hoặc tài liệu. Không đổi giao diện hay phần xử lý khác.

## Không bỏ qua b1–b3 ngẫu nhiên; 14 ảnh menu mới — 14/11/2026

Người dùng báo tool đi thẳng b4 dù yêu cầu phải xem/bấm b1, b2, b3 trên cả 12 máy. Nguyên nhân trong `random_prefix.py` là ba nhánh trả về thành công khi đọc menu lỗi, không có mục phù hợp hoặc màn đã ở form; `_tap_for_transition` còn nuốt lỗi lệnh chạm. `PostMenuSession` vì vậy tăng `next_step` như thể cú bấm đã xảy ra. Nay mỗi bước chỉ ghi `registration.prefix_completed` sau khi `_tap` ADB trả thành công; lỗi vẫn ở đúng bước để tự đọc lại. Sau lỗi chạm, tool đọc menu mới và thử mục khác, gồm các hàng con trong ảnh. B4 có chốt yêu cầu đủ ba dấu hoàn tất rồi tự về Browse menu trước Sign In. Không dùng tọa độ cố định từ ảnh, không chọn Sign In/Settings ở b1–b3.

14 ảnh người dùng gửi đã sao chép nguyên bản vào `flow_images/shared/random_prefix_reference/` và giải thích từng ảnh tại [IMAGE_EVIDENCE.md](IMAGE_EVIDENCE.md). Ảnh cho thấy 15 thẻ danh mục, mục con mở rộng trong cùng menu và Sign In ở cuối; tiêu đề menu có thể cuộn khỏi màn. Mã nhận menu bằng ba thẻ đang hiện và ghép nhãn OCR xuống dòng. Đã test mô phỏng; chưa chạy trên Swarmote thật. Tool đang mở không tự nạp thay đổi và không được reset vì dữ liệu mẻ chỉ ở RAM.

`python -m unittest discover -s tests -q`: 311/311 PASS.

## Dán nhiều proxy cách nhau bằng dấu cách — 14/11/2026

Người dùng dán nhiều proxy dạng `host:port:username:password` trên cùng một dòng, ngăn bằng dấu cách; trước đây `bulk_input.lines` chỉ tách theo xuống dòng nên toàn bộ bị coi là một proxy và phần còn lại nhập nhầm vào mật khẩu. `parse_column("proxy")` nay tách trước mỗi tiền tố proxy tiếp theo theo khoảng trắng, vẫn giữ trường hợp một mật khẩu đơn có dấu cách như trước, giới hạn 100 mục sau khi tách và báo lỗi theo thứ tự mục. Cả ô Proxy dán nhanh lẫn ô proxy máy đang chọn dùng cùng parser; nhiều mục được gán Máy 1–12 theo thứ tự và phần dư là proxy dự phòng như trước. Không lưu hoặc ghi giá trị proxy thật của người dùng. Chuỗi bốn trường hiện không mang thông tin giao thức; `parse_proxy_line` và đường tạo Profile vẫn dùng SOCKS5, chưa suy đoán HTTP/HTTPS theo tên nhà cung cấp. **300 unittest PASS**, gồm kiểm thử bốn proxy trên một dòng và đường phân bổ từ ô proxy đơn. Không thử proxy thật hoặc tạo Profile, không đóng phiên tool đang mở.

## b1–b3 ngẫu nhiên cho q1–q12 — 14/11/2026

Người dùng đổi yêu cầu: ba thao tác đầu chỉ cần bấm ngẫu nhiên, chọn nhầm mục không quan trọng; mỗi mẻ tạo mới phải bốc lại, không giữ chuỗi cố định q1–q6. `desktop.POST_MENU_STEP_FACTORIES` nối cả 12 slot tới `random_prefix.build_random_steps`. Bản đầu chọn mục từ menu thật nhưng cho phép đi tiếp khi chưa bấm được; lỗi này đã sửa ở mục bàn giao mới phía trên. Nhánh menu danh sách cũng không bỏ qua ba bước. Các file `q1_flow.py`–`q6_flow.py` còn lại làm tham chiếu cho luồng cố định cũ; b4–b11 không đổi. Chưa xác minh trên 12 máy thật. Không đóng phiên đang mở vì dữ liệu mẻ nằm trong RAM; tiến trình đó chưa tự nạp mã mới.

## b6 cuộn chạm đáy rồi vuốt ngược khoảng bốn quốc gia — 14/11/2026

Theo video `D:\cuonus1.mp4` và chỉ dẫn mới của người dùng, khi US +1 chưa hiện, luồng chung b6 fling trong hộp Country tới khi nhóm hàng cuối Zimbabwe/Åland Islands xuất hiện; tiếp tục fling và chỉ đảo chiều khi các hàng quốc gia cuối không đổi giữa hai lần đọc. Sau đó vuốt ngược trong chính vùng danh sách khoảng bốn khoảng cách hàng (có giới hạn theo chiều cao hộp), đọc lại để tìm United States +1; nếu chưa thấy thì tiếp tục vuốt ngược và đọc lại. Cả UiAutomator2 và ADB dự phòng dùng cùng phép tính quãng vuốt; nếu US đã nhìn thấy thì chọn ngay. Không thay đổi các bước khác hay đóng phiên tool đang mở. **289 unittest PASS**, gồm kiểm thử cuộn và chọn quốc gia; chưa xác minh trên Swarmote thật. Phiên tool đang chạy cần nạp mã mới để dùng thay đổi này.

## Phục hồi khi ô nhập chưa nhận focus ở b4–b11 — 14/11/2026

`account_flow._tap_input` dùng chung cho ô SĐT, tên và OTP: sau cú chạm đọc lại đúng màn và ô, xác nhận `focused=true` từ cây Android hoặc bàn phím đã hiện khi cây không có cờ focus/OCR; nếu chưa đạt thì tìm lại bounds và chạm tối đa ba lần. Một khung WebView chưa đủ chữ được đọc lại trước khi kết luận màn đổi. `_type_field` chỉ gõ sau xác nhận, đọc lại giá trị trước khi gõ để tránh nhập lặp khi cú chạm hoặc lần gõ trước trả kết quả muộn. Nếu vẫn không rõ focus thì giữ ô và dừng an toàn, không gửi ký tự sang điều khiển khác. B4a, b5, b9, b11a và b11 cùng dùng nhánh này; b7/b8/b10/Create không đổi cách bấm. Test timeout cũ trong `test_extended_recovery.py` được cập nhật theo quy tắc không còn thời hạn tổng, vẫn xác nhận Stop ngắt được lần đọc tạm thời. Toàn bộ **288 unittest PASS**, gồm 19 test `test_flow_recovery.py` và 43 test `test_q1_flow.py`. Chưa xác minh trên Swarmote thật; phiên tool đang mở chưa nạp mã mới, không tự đóng hoặc đặt lại.

## b6 US +1 còn mở sau bốn cú chạm — 14/11/2026

Video cuộn tay `D:\cuonus1.mp4` xác nhận chuỗi: tới cuối danh sách (Zimbabwe/Åland Islands), vuốt ngược ngắn một lần để United States +1 hiện, rồi bấm hàng US; hộp đóng và form hiện US +1. Đoạn này ghi nhận phân tích video trước khi người dùng yêu cầu thay đổi b6 ở mục đầu tài liệu. Video không chứng minh phiên tool đang mở đã nạp mã mới hoặc gesture tự động có cùng kết quả. Xem [IMAGE_EVIDENCE.md](IMAGE_EVIDENCE.md).

Ảnh mới của q1 cho thấy `United States +1` đang nhìn thấy giữa United Kingdom và Uruguay, nhưng tool báo đã chọn bốn lần mà hộp Country vẫn mở. Nguyên nhân mã: sau cú chạm, `_wait_screen` cho phép `COUNTRY` là kết quả nên trả ngay khi hộp chưa đóng; vòng lặp chạm lại cùng bounding box chữ sau 0,2 giây. Bản sửa trước đã thêm bước chạm vùng chữ, đợi 0,8 giây và đọc lại; nếu vẫn mở thì chạm giữa toàn hàng theo chiều rộng Android thực. Cách cuộn trước đó đảo chiều ngay khi thấy Wallis/Western Sahara/Zimbabwe; nay đã được thay bằng quy tắc ở mục đầu. Chưa thử trực tiếp trên q1 thật; tool đang mở chưa nạp mã mới.

Người dùng báo ngoài thực tế: lần đầu bước báo lỗi, không sửa gì, bấm Tiếp tục thì thành công. Đổi `_wait_screen` sang tiếp tục đọc cây/OCR tới khi màn mục tiêu xuất hiện hoặc người dùng Dừng; bỏ giới hạn hai lần phục hồi cho b1–b9 và đọc lại cùng bước sau lỗi nhận diện tạm. Mỗi lần ADB/browser vẫn có timeout cục bộ. b10 không gửi SMS lần nữa khi trạng thái gửi chưa rõ; b11 đọc lại URL theo các lượt 30 giây. Test liên quan bước tiếp tục tự phục hồi đạt; cập nhật các test tổng hợp cũ trước lần chạy toàn bộ tiếp theo.

## Bỏ thời hạn tổng sau menu — 14/11/2026

Người dùng xác nhận q1/q2 chạy b4–b11 tốt, yêu cầu q3/q4 dùng đúng hàm chung và bỏ quy định dừng sau 3/4/5 phút. Kiểm tra mã và unittest xác nhận b4–b11 của q1–q4 cùng tên và cùng implementation `build_common_steps`; khác biệt nằm ở b1–b3 hoặc màn Android thực tế. `PostMenuSession` nay dùng `AttemptDeadline(None)` cho toàn phiên, không tính thời gian từ `MENU_OPEN`, không còn chu kỳ 3/4/5 phút. Xong bước nào thì tự chuyển bước kế; mỗi lời gọi ADB/browser vẫn dùng timeout ngắn, Stop vẫn hoạt động. OTP tiếp tục vòng đọc 30 giây khi chưa có mã. Chưa chạy trên Swarmote thật. 265 unittest PASS.

## Phạm vi q1–q12 sau phản hồi người dùng — 14/11/2026

Các hàm mở Swarmote, ADB, Amazon/menu và `build_common_steps` b4–b11 không gắn riêng q1/q4. Đã kiểm thử tạo 12 bộ bước chung với 12 serial và RegistrationState độc lập. `POST_MENU_STEP_FACTORIES` hiện mới có q1–q4 vì b1–b3 riêng của q5–q12 chưa được cung cấp; trước đây `_start_post_menu` trả về im lặng cho các máy này. Nay tool báo rõ máy đã tới menu nhưng còn thiếu b1–b3, không tự bỏ qua bước hay đoán thao tác. 263 unittest PASS. Chưa xác minh 12 thiết bị thật.

## Lỗi chạy song song q3 Terminal trùng / q1 chưa thấy menu — 14/11/2026

Hai ảnh người dùng báo q3 dừng "có nhiều nút Terminal đang hiện" và q1 dừng "Amazon chưa hiện menu ba gạch". Các ảnh thông báo không chứa ảnh Android hiện hành hoặc cây UIA nên chưa thể quy kết mọi trường hợp cụ thể. Đối chiếu mã tìm thấy hai điểm dừng quyết định bằng dấu hiệu thiếu: open_adb_shell đếm từng Text Terminal chứ không đếm Group cha duy nhất; open_home_menu chỉ nhận heading Shop by category và chỉ bấm Browse menu một lần.

Sửa mở ADB: dedup Group Terminal theo UIA runtime_id; hai nhãn của một Group chỉ Invoke một lần. Nếu có nhiều Group thật trong đúng cửa sổ q3, thử lần lượt và xác nhận ADB Shell sau mỗi lần (xem cập nhật cuối tài liệu).

Sửa mở menu: nhận thêm bộ ba tên danh mục của menu thẻ khi heading bị thiếu trong XML; nút Browse menu có thể bấm lại tối đa ba lần nếu hai lượt đọc kế tiếp xác nhận tab vẫn unselected. Sau timeout ADB của cú bấm, đọc màn tiếp theo trước khi quyết định bấm lại. Bộ đọc Android chung hỗ trợ xác nhận menu khi XML thiếu chữ. b1–b9 được bổ sung retry có kiểm tra; không tự gửi lại SMS/Create.

Kiểm thử hồi quy tái hiện các nhánh trên bằng UIA/Android giả. Chưa có màn/cây thật của lượt q1/q3 mới, chưa xác minh trên Swarmote thật; tool đang mở cần nạp mã mới bằng cách mở lại sau khi giữ dữ liệu. Nếu q1 vẫn dừng, cần trạng thái Android và cây UI của chính lượt đó để xác định biến thể còn thiếu. Graphify chưa cập nhật vì Python dự án thiếu module.

## Tự phục hồi lỗi tạm thời trong mẻ nhiều máy — 14/11/2026

Đã rà runner (tạo/Start/chuẩn bị), bộ đọc process riêng, account_flow và PostMenuSession. Không cam kết toàn bộ 12 máy chạy hết luồng thật: q5–q12 thiếu b1–b3 theo hướng dẫn; sau Create chưa có tiêu chí kết quả được hướng dẫn. Không tự triển khai các mốc còn thiếu.

Các sửa mới:
- `_read_nodes` không dừng sau đúng ba lỗi đọc tạm thời. Tự đọc lại với backoff tối đa 1 giây trong thời hạn hiện tại, nhận Stop, phát tiến trình, không reset đồng hồ. Lỗi dữ liệu/serial không được biến thành retry nhập liệu.
- `_wait_screen` dùng thời gian còn lại của lượt; khoảng seconds cũ trở thành mốc báo chuyển màn chậm. Chỉ quan sát, không phát lại tap/SMS/Create. Màn đọc được nhanh vẫn trả ngay.
- `_wait_for` Swarmote tự đọc lại khi provider UIA lỗi tạm thời trong timeout của chặng; báo tên loại lỗi nếu hết timeout. Không phát lại hành động Create/Install trong helper này.
- `_start_and_confirm` gửi Start một lần. Nếu phản hồi lỗi thì đọc trạng thái tối đa ba lần, tiếp tục chỉ khi cùng Device ID và Running/Starting. Không gửi Start lại; ID khác bị chặn.
- MenuReadUnavailable phân biệt lỗi đọc menu với màn xác minh tài khoản. open_home_menu đọc lại lỗi quan sát trong thời hạn, giữ các dấu đã bấm menu/Skip/Back. Stop được truyền từ runner; ngân sách ADB dump/cat lấy theo thời gian còn lại và không bấm sau khi Stop.

Kiểm chứng mới gồm 12 job giả lập từ create/start/install đến menu với serial riêng, mỗi hành động một lần; 12 bộ đọc cùng lỗi bốn lần rồi hồi phục; màn chuyển chậm vượt khoảng ngắn; lỗi UIA tạm thời; Start đã được gửi nhưng mất phản hồi; sai ID và sai SĐT không được bỏ qua; deadline vẫn kết thúc; Stop trong lúc đọc menu không bấm tiếp. Không gọi dịch vụ tài khoản hoặc Android thật trong các test.

Các điểm vẫn phải dừng: proxy không đạt và hết proxy dự phòng; kết quả Create Profile không xác nhận được; sai/không rõ serial hoặc thông tin tài khoản; UI chưa được hướng dẫn; lỗi kéo dài hết thời hạn; người dùng bấm Stop. Không retry nguyên một bước gửi SMS/Create/gõ dữ liệu một cách mù quáng. Không khẳng định đã hết mọi lỗi lặt vặt trên thiết bị thật. Graphify vẫn thiếu module.

## Tách bộ đọc thành tiến trình riêng từng máy — 14/11/2026

Theo yêu cầu 12 máy độc lập, bỏ hàng đợi OCR hai engine dùng chung trong luồng desktop sau menu. `isolated_reader.py` tạo process spawn riêng (lazy ở lần đọc đầu) cho mỗi worker máy, serial cố định, UIAutomator2 client/cache và một OCR model riêng. Desktop gắn context cho toàn bộ PostMenuSession; account_flow chuyển đọc UI/ảnh/OCR sang child. Native country scroll cũng đi cùng child để dùng đúng client đã khởi tạo. Hành động nhập liệu, OTP, RegistrationState và điều phối bước vẫn ở worker/thread riêng từng máy của parent, không chuyển cả ứng dụng sang 12 process.

Mỗi RPC có request ID và serial, kiểm tra khi nhận, loại kết quả muộn. Hủy/treo/kết nối hỏng đóng riêng process tương ứng; lần đọc tiếp theo có thể tạo lại, lỗi đọc bình thường giữ backend đã warm. Cuộn có kết quả không rõ không được bù ngay bằng ADB swipe. Context chặn hai worker nhận cùng serial. Process đóng khi phiên kết thúc/tạm dừng; retry giữ RegistrationState ở parent. Launch .pyw có main guard để spawn không mở lại GUI. Cơ chế chưa được hot-load vào phiên tool đang mở.

Theo chỉ dẫn mới nhất không ép CPU threads = 1: OCR dùng mặc định RapidOCR/ONNX. Không áp hạn mức hai reader dùng chung. Tổng CPU/RAM và ADB server vẫn là tài nguyên vật lý chung; không khẳng định chạy vô hạn hoặc không thể quá tải. Có thể dùng tới 12 model OCR khi cả 12 máy cần OCR, chưa đo bộ nhớ của máy người dùng. Thời hạn lượt và nút Stop vẫn giữ để phát hiện treo, không tự gửi lại SMS/Create. Tạo profile vẫn tuần tự vì cùng form Swarmote. q5–q12 vẫn chưa có hướng dẫn b1–b3; không tự sao chép luồng máy khác.

Kiểm chứng: 12 process thật với PID khác nhau và serial riêng, một process bị treo không chặn process khác, Stop trước spawn, server production với Android giả cho read/scroll, định tuyến đọc của account_flow, chặn trùng serial. Không chạy 12 điện thoại thật, chưa có benchmark tốc độ/RAM hay bằng chứng mọi lỗi b4–b11 đã hết. Graphify thiếu module; graph chưa cập nhật.

## B4–b11 chạy đồng thời và OCR — 14/11/2026

Kiểm tra cloud_screenshot xác nhận chụp Android trực tiếp bằng adb -s serial exec-out screencap, không chụp desktop Windows. ui_backend giữ session/lock theo serial. Chưa tìm thấy bằng chứng ảnh bị tráo do cửa sổ chồng nhau.

Điểm nghẽn xác nhận trong code: vision.ocr_nodes dùng duy nhất một engine/lock cho toàn bộ máy; các máy chờ OCR trong thời hạn lượt riêng. Sửa thành pool tối đa hai engine độc lập, mỗi engine giới hạn ONNX intra/inter threads = 1 để tránh nhân số CPU threads. Kết quả boxes/text/scores được sao chép trước khi trả engine vào pool. Chờ slot kiểm tra Stop/deadline mỗi 0,1 giây; sau OCR kiểm tra lại trước khi trả kết quả. account_flow truyền Stop/deadline vào OCR. Không tự bỏ qua xác nhận số điện thoại, SMS hoặc Create; không thay luồng các máy.

Đã kiểm tra hai RapidOCR thật khởi tạo riêng và nhận cấu hình 1/1; kiểm thử cạnh tranh hai reader với barrier, kết quả giữ đúng caller, hủy sau OCR bỏ kết quả cũ, lỗi trả slot. Chưa đo tốc độ hay xác minh toàn bộ lỗi của bốn máy thật. OCR native đang chạy không bị cưỡng bức hủy; chỉ bỏ kết quả sau khi lời gọi trả về. Hai engine dùng thêm RAM so với một engine, giới hạn pool tránh tạo 12 bộ model.

## Tự tìm và mở Swarmote khi chạy mẻ — 14/11/2026

Khi đọc Profiles thất bại trước mẻ, runner gọi ensure_manager_ready: tìm executable của tiến trình Swarmote đang chạy hoặc bản cài trong LocalAppData/Program Files, chỉ khởi chạy một lần khi chưa có tiến trình, chờ cửa sổ và trang Profiles tối đa 60 giây, cập nhật tiến trình từng hàng và nhận Stop giữa các vòng polling. Không mở thêm instance khi app đang tải/đăng nhập; nếu hết thời gian báo lý do và nhắc đăng nhập thủ công. Nhiều bản Swarmote chạy từ đường dẫn khác nhau được báo mơ hồ thay vì tự chọn.

Kiểm thử mới kiểm tra mở một lần, dùng lại app đang mở và Stop trước khi mở. Không chạy Swarmote thật trong lượt này. Không tự cài app, nhập tài khoản hoặc reset dữ liệu. Đây là bước khởi động Swarmote trước tạo profile; không thay quy trình mở Amazon trên Android. Cần mở lại tool để nạp mã.

## Sửa lỗi chuẩn bị nhiều máy — 14/11/2026

Người dùng yêu cầu tiếp tục từ NEXT_SESSION_HANDOFF.md và chỉ kiểm tra/sửa code, không yêu cầu mở Swarmote để đo máy thật. Không đóng/reset tool, không tạo profile, không cài phần mềm lên Android trong lượt sửa này.

### Bằng chứng trong code và kiểm thử

- Bộ điều phối `Window._run` và worker `_prepare_phone` dùng `pythoncom.CoInitialize()` (STA). `pywinauto 0.6.x/uia_defines.py` giữ IUIA/COM client trong singleton toàn tiến trình. Các worker truy cập chung client dù khởi tạo ở các STA riêng; coordinator còn chờ futures. Đây là lỗi cấu hình luồng UIA, phù hợp nguy cơ kẹt khi chạy song song; chưa có stack dump của lượt Swarmote bị kẹt để kết luận nó là nguyên nhân duy nhất.
- Test gọi `ole32.CoGetApartmentType` thật trong bộ điều phối và 12 worker xác nhận bản cũ trả STA/MAINSTA (0/3), không phải MTA (1). Sau sửa, tất cả trả 1. Tham chiếu chính thức: https://learn.microsoft.com/en-us/windows/win32/winauto/uiauto-threading (UIA worker nên là MTA, không sở hữu cửa sổ).
- `_phone_window` cũ gọi `Desktop(backend="uia").windows()` mỗi lần cho mỗi máy: đọc provider toàn desktop rồi mới lọc. Bản sửa lọc HWND bằng Win32 title chính xác qN + Device ID và đường dẫn executable, chỉ tạo một wrapper UIA cho cửa sổ đã xác nhận. Không lấy HWND cũ làm bằng chứng đủ để bỏ qua tên/Device ID.
- Các vòng chờ `show_apps`, `_phone_window`, `open_adb_shell` thiếu Stop; nhánh catch trong Apps có thể nuốt lỗi hủy. Bản sửa nối cờ hủy, dùng Event.wait để thoát khi Dừng và kiểm tra lại hủy trước/sau các chặng.
- Bảng `_refresh_table` thay mọi thông báo running bằng “Đang chạy”, che chặng đang chờ. Bản sửa hiện thông báo chặng và xuống dòng trong ô trạng thái; callbacks gắn đúng hàng/profile. Vòng đợi phát cập nhật mỗi 3 giây khi đang polling.

### File chính đã sửa

- `amazon_android/runner.py`: worker MTA, truyền progress/stop theo đúng job, báo lỗi ra hàng nếu khởi tạo COM thất bại. Import pythoncom ở caller trước khi tạo worker; từng worker dùng CoInitializeEx(COINIT_MULTITHREADED), không dựa vào apartment mặc định ở lần import đầu.
- `amazon_android/desktop.py`: các luồng nền dùng MTA; bảng hiện trạng thái chuẩn bị cụ thể thay nhãn running chung. GUI chính vẫn chạy như cũ.
- `amazon_android/swarmote_desktop.py`: tìm cửa sổ có phạm vi, Stop/progress cho Apps và Terminal, nhận điều khiển visible trong nhánh chuẩn bị. Giữ `_wait_for` mặc định không lọc visibility cho các luồng tạo profile ẩn trước đây.
- Tests mới: `test_preparation_threads.py`, `test_swarmote_waits.py`, `test_parallel_install.py`, `test_preparation_progress.py`; `worker_helpers.py` chạy worker trên thread thật như app. Cập nhật fixture cũ nhận stop/progress và chạy đúng luồng nền.

### Kết quả và giới hạn

- `.venv/Scripts/python.exe -m unittest discover -s tests`: **230 PASS**, 10,133 giây. TMP/TEMP/TMPDIR trỏ `.test_tmp` trong workspace.
- `py_compile` cho ba module chính PASS.
- Test 12 luồng kiểm tra apartment bằng COM thật; test 12 cài đặt dùng các hàm Apps/install/Terminal thật nhưng UIA/Android là đối tượng giả. Đã xác nhận mỗi luồng bấm Install một lần, đọc đúng cổng ADB riêng, nhận đúng callback tiến trình.
- Không kiểm thử Swarmote thật theo chỉ dẫn mới nhất của người dùng. Không khẳng định 12 máy thật đã chạy hết hoặc đo được tốc độ nhanh hơn.
- Stop ngắt các vòng polling; không thể ngắt giữa một lời gọi COM/ADB đồng bộ đang bị provider giữ. Tiến trình mỗi 3 giây cũng chỉ phát khi loop đang chạy, không phải watchdog riêng. Nếu vẫn kẹt ở một lời gọi native, cần stack dump/cô lập process sau; không tạo thêm thread bấm lặp vào cùng máy để vượt timeout.
- Không thay b1–b11, OTP, driver Android hoặc giới hạn Running. Không tăng timeout để che lỗi. Phiên tool đang mở chưa tự nạp code; giữ dữ liệu trước khi mở lại, không tự restart/reset.
- Graphify thiếu module trong Python dự án; không tuyên bố graph đã cập nhật.


> **Điểm dừng mới nhất 13/11/2026:** người dùng yêu cầu dừng để đổi tài khoản. Đọc [NEXT_SESSION_HANDOFF.md](NEXT_SESSION_HANDOFF.md) trước khi tiếp tục. Lỗi mở Apps/cài Amazon khi nhiều máy chạy CHƯA sửa xong. Phần Stop/Reset mới đã có 221 unittest PASS, chưa thử GUI thật và chưa nạp vào tool đang mở.

# Bàn giao trạng thái dự án — 13/11/2026

## Cài đặt máy mới

- `Install Swarmote Tool.bat` tìm Python 3.11+, mở trang tải Python chính thức nếu chưa có, rồi gọi `setup_windows.py`.
- `setup_windows.py` kiểm tra Swarmote và Chrome/Edge, hỏi trước khi mở trang tải khi thiếu, tạo `.venv`, hỏi trước khi cài dependencies bằng `pip install -e .`, rồi khởi chạy giao diện qua Python ảo.
- Bản cài cần một trong Chrome hoặc Edge cho OTP. Điện thoại Swarmote vẫn cần Profile Running và tunnel được mở bằng **Terminal > ADB Shell**. Java/Android SDK chỉ dành cho Android Emulator cục bộ.
- Setuptools package discovery được giới hạn vào `amazon_android*` trong `pyproject.toml`; `.venv/` được Git bỏ qua.

## Mục tiêu và quy tắc đã chốt

Tool desktop CustomTkinter điều khiển Swarmote/Amazon Shopping cho tối đa 12 máy. Mỗi hàng Amazon chứa SĐT, mật khẩu, tên, thẻ và URL OTP riêng; hàng n gắn Máy n. Bảng Markdown có cột trống, hàng gạch phân cách, thẻ `số|tháng|năm` viết `\|`, và link URL dạng `[nhãn](URL)` phải được đọc đúng. Bảng chỉ hiện đuôi thẻ; dữ liệu giữ trong bộ nhớ phiên. Thẻ chưa được dùng trong b1–b11.

Từ menu ba gạch, chỉ b1–b3 khác nhau theo máy. b4 Sign In đến b11 nhập OTP SMS rồi bấm Create dùng chung. Người dùng sẽ hướng dẫn b1–b3 của từng máy; hiện đã có q1 và q2. Mỗi máy có ADB serial, SĐT, URL OTP, mã, trạng thái gửi, đồng hồ và điểm dừng/tiếp tục riêng. Gõ từng ký tự, không dán vào Android. Nếu lỗi, dừng ngay tại bước đó; người dùng sửa trên máy rồi bấm Tiếp tục. Chu kỳ thời hạn mỗi máy: 3, 4, 5, 4 phút rồi lặp lại; tính lại khi Tiếp tục. Đồng hồ kết thúc khi OTP SMS đã nhập đúng, sau đó bấm Create.

Menu ba gạch có thêm biến thể dạng danh sách: trên các máy đã nối sau menu, đọc cây UI hiện tại; nếu thấy danh sách chữ, bấm Home, chỉ xem/chờ 2–5 giây, quay lại menu rồi làm b4 Sign In. Dạng thẻ vẫn chạy b1–b3 riêng. Không cuộn Home và không dùng tọa độ ảnh. Xem [MENU_ROUTING.md](MENU_ROUTING.md) cùng ảnh trong `flow_images/shared/`. q3–q12 vẫn chưa được bật sau menu.

## Mã hiện có

- `amazon_android/bulk_input.py`, `batch_state.py`, `desktop.py`, `runner.py`: ánh xạ hàng, dữ liệu thẻ/OTP, UI 12 máy; khi gắn q1, 12 hàng vẫn hiện.
- `amazon_android/otp.py`: xác thực URL APIFC, tách đúng 6 số từ phản hồi Amazon và đọc sau khi gửi SMS; Chrome và Edge ẩn dùng để đọc OTP. APIFC không cung cấp dấu thời gian để chứng minh mã là mới khi URL đã có mã cũ.
- `amazon_android/post_menu.py`: phiên riêng từng máy, thời hạn, dừng/tiếp tục cùng bước, gõ từng ký tự.
- `amazon_android/account_flow.py`: nhận diện UI Android, phân loại menu dạng thẻ/danh sách, dùng `route_list_menu` và `visit_home`, cùng `build_common_steps` cho b4–b11. `amazon_android/q1_flow.py`: b1 Gifting, b2 Pets, b3 Fashion and Beauty. `amazon_android/q2_flow.py`: b1 tab Home và xem 2–5 giây, b2 tab Browse menu, b3 Pets. `amazon_android/post_menu.py` chuyển thẳng tới b4 khi menu dạng danh sách. `amazon_android/desktop.py` gắn profile từ menu theo máy được chọn. Không dùng tọa độ ảnh. q1 và q2 được nối; q3–q12 dừng ở menu.
- `amazon_android/swarmote_desktop.py`: khi tạo profile, kiểm tra tên trùng; nếu tên vắng trên danh sách một trang thì không gõ vào ô lọc. Đưa cửa sổ quản lý lên trước để bấm New Profile, xác nhận form trước khi điền, sau đó Test Proxy và Create.
- `Launch Swarmote Tool.pyw` gọi `amazon_android/launcher.py` để mở desktop. Graphify không phân tích trực tiếp `.pyw`; xem [SOURCE_INDEX.md](SOURCE_INDEX.md) cho các file bị bỏ qua.

## Trạng thái kiểm chứng và giới hạn

- B6 xác nhận mục `United States +1` nằm cùng vị trí trong hai lần đọc liên tiếp rồi mới bấm. Nếu form trả mã khác, ví dụ SG +65, mở lại danh sách, tiếp tục tìm và chỉ hoàn tất khi ô mã quốc gia hiện US +1. Nếu danh sách đã tới đáy thì vuốt ngón tay xuống ngắn. Chưa thử trên máy thật.

- B6 kiểm tra danh sách sau khi vuốt mạnh. Nếu hiện các nước sau Mỹ hoặc danh sách đứng yên khi vuốt về cuối, tool vuốt ngón tay xuống từng đoạn ngắn để tìm `United States +1`. B6 tiếp tục tìm trong thời hạn lượt hoặc đến khi người dùng bấm Dừng, kể cả khi vài ảnh chụp cây UI liên tiếp giống nhau. Chưa xác minh thao tác trên Swarmote thật.

- B9 Continue và b11 Create dùng chữ, mô tả và quan hệ điều khiển từ cây Android trước. Nếu vẫn mơ hồ, chụp trực tiếp màn Android vào bộ nhớ và tìm nút vàng rộng bên dưới ô đã xác nhận. Nếu có nhiều vùng vàng, chỉ chọn khi vị trí nhãn đúng trong cây UI xác định duy nhất một vùng. B11 kiểm tra SĐT trước nhánh ảnh và đối chiếu OTP nếu phiên đã có mã. Test mô phỏng với vùng vàng và màn SMS. Chưa kiểm tra trên Swarmote thật vì phiên này không tìm thấy ADB.

- Luồng dùng chung tự đọc lại khi ADB hết hạn, lấy file thất bại hoặc trả XML chưa hợp lệ. Trong lúc chờ màn kế tiếp, các lỗi đọc tạm thời được thử lại theo thời hạn. Nếu cú bấm chuyển màn hết hạn ở ADB, kiểm tra màn sau cú bấm trước khi quyết định bước tiếp theo. Gửi SMS và Create vẫn giữ dấu đã bấm để tránh gửi lặp. Khi không thể xác nhận, thông báo ghi màn đọc được và màn cần thấy, không kèm dữ liệu tài khoản. 148 bài test đã qua, gồm cú bấm SMS bị timeout nhưng đã chuyển màn và XML lỗi được đọc lại. Chưa xác minh trên Swarmote thật.

- B11 thử Chrome ẩn, Edge ẩn rồi tự mở một cửa sổ Chrome riêng nếu chưa đọc được mã. Tool dành một phần thời hạn đọc OTP cho cửa sổ này, chờ người dùng xử lý xác minh nếu trang yêu cầu và đóng cửa sổ sau khi lấy mã, hết hạn hoặc dừng. Nếu vẫn lỗi, Tiếp tục giữ phương án nhập tay. Chưa xác minh với APIFC thật.

- B11a chạm ô OTP ngay khi nhận ra màn SMS và xác nhận đúng SĐT. Khi nhận được mã, b11 đọc lại màn, xác nhận đúng SĐT và kiểm tra focus trước khi gõ. Test mô phỏng bao gồm trường hợp nguồn mã lỗi sau khi ô đã được chạm và ô mất focus trong lúc chờ mã. 145 bài test đạt. Ảnh q1 báo đúng chuỗi lỗi 403 của bộ đọc HTTP cũ, đã bỏ khỏi luồng mặc định tại `07ab6d1`. Chưa đọc được q1 thật vì phiên kiểm tra không thấy ADB.

- B9 gặp nhiều Continue khi bàn phím mở. Bộ chọn nhận cả text và content-desc, giữ node nút gốc. Nếu vẫn chưa chọn được, kiểm tra Android có bàn phím đang hiện, đóng bàn phím một lần, đọc lại form, xác nhận SĐT và tên rồi mới bấm Continue. Chưa đối chiếu cây UI của q1 thật vì không thấy ADB trong phiên kiểm tra.

- Ảnh q1 mới cho thấy form tạo tài khoản đã hiện dù b8 báo chưa nhận diện được màn. Bộ nhận diện chung đọc cả `text` và `content-desc`, chấp nhận tiêu đề biến thể và dùng nhãn tên hoặc tiêu đề cùng Mobile number, Continue và một ô nhập hiện hữu. Khi b8 đọc được form đã mở, chuyển sang b9 mà không bấm lại. Mô phỏng đã kiểm tra các biến thể và trường hợp mơ hồ. Chưa đọc được cây UI q1 thật vì không thấy ADB Swarmote.

- Danh sách quốc gia dài. Sau cú vuốt nhanh rồi nhả, nếu màn vẫn hiện các nước nhóm A–S, b6 tiếp tục dùng cú vuốt mạnh. Gần nhóm T/U thì cuộn có kiểm soát và cuộn ngược nếu vượt qua mục Mỹ.

- Ảnh b6 mới cho thấy danh sách đã tới United States nhưng lệnh ADB hết hạn sau 6 giây. B6 dùng lại cây UI đã đọc để chọn mục đang hiện hoặc quyết định cú vuốt đầu. Nếu thao tác đọc cây UI hết hạn ở ADB, thử đọc lại một lần trong thời hạn của máy, không lặp cú vuốt hoặc bấm. Chưa có số đo trên máy thật.

- Tăng lực vuốt đầu ở b6 bằng thao tác 65 ms qua 92% vùng danh sách khi cây UI cung cấp vùng cuộn. Tool đọc lại để xác nhận đúng United States +1 và cuộn ngược ngắn nếu vượt qua mục Mỹ. Giảm khoảng nghỉ cuộn thường và kiểm tra một số lần chuyển màn. Chưa đo quãng vuốt hoặc thời gian trên máy Swarmote thật.

- Trình duyệt có thể khởi động trong lúc chờ SMS. Chỉ điều hướng tới URL của máy khi đủ 4 giây từ lúc bấm gửi và màn SMS đã được nhận diện. Chrome ẩn là mặc định, Edge ẩn dự phòng khi Chrome không mở hoặc không đọc được trang.

- B11 mặc định đọc OTP qua Chrome ẩn và thử Edge ẩn nếu Chrome không mở hoặc không đọc được trang. Máy đích cần cài Chrome hoặc Edge và Playwright qua dependencies. Đã chạy trình duyệt ẩn thật với máy chủ thử nghiệm cục bộ, nhận phản hồi chờ rồi tải lại và tách được 6 số. Chưa xác nhận với URL APIFC của lượt SMS thật. Nếu trình duyệt ẩn không đọc được, dùng phương án mở trình duyệt thường tại Tiếp tục.

- Ở b11, người dùng xác nhận cùng URL có SMS đúng mẫu trong trình duyệt khi tool báo HTTP 403. Bấm Tiếp tục ở máy lỗi để mở URL đúng hàng và dán phản hồi SMS hoặc 6 số vào tool. Tool xác nhận lại số điện thoại trên màn SMS trước khi điền. OTP chỉ giữ trong bộ nhớ. Bộ đọc phân biệt phản hồi có header `cf-mitigated: challenge` với HTTP 403 thông thường. Chưa xác định nguyên nhân 403 trên máy người dùng hoặc kiểm chứng tự đọc URL thật.

- Ảnh q1 mới báo b9 chưa xác nhận được nội dung ô tên dù tên đã hiện. Luồng chung đọc lại tối đa ba lần sau khi gõ, không gõ lặp và chỉ bấm Continue khi nội dung khớp tên của máy. Kiểm tra mô phỏng giá trị tên cập nhật trễ. Chưa xác nhận trên Swarmote thật.

- Sau ảnh q1 dừng tại b4 dù form đã xuất hiện, luồng chung tách b4a chạm ô SĐT thành bước riêng giữa Sign In và gõ số. B4a chờ form, chạm ô và b5 kiểm tra lại focus trước khi gõ. Form cũng được nhận khi có nhãn SĐT, Continue và một ô nhập hiện hữu dù cây UI thiếu tiêu đề. Giảm khoảng nghỉ khi kiểm tra màn và cuộn thường. Chưa kiểm chứng trên Swarmote thật.

- Luồng chung giữ quan hệ cha con trong cây UI Android. Bộ chọn nút quy các nhãn lặp về điều khiển cha có thể bấm trước khi so sánh vùng bấm. Áp dụng cho Sign In, Continue, Proceed to create an account, Send code by SMS và Create your Amazon account. Đã thêm kiểm tra với cây XML mô phỏng, chưa có ADB Swarmote để đối chiếu cây UI thật.

- Máy 2 báo b9 còn nhiều mục Continue sau khi tên đã điền. Bộ chọn chung ưu tiên nút duy nhất nằm dưới và phủ gần hết chiều ngang ô tên khi còn nhiều vùng bấm. Nếu có hai vùng cùng thỏa thì giữ điểm dừng. Kiểm tra mô phỏng, chưa có cây UI của màn lỗi trên máy thật.

- B4–b5 dùng chung nhận diện form `Sign in or create account` có nút Continue và một ô nhập hiện hữu ngay cả khi cây UI thiếu nhãn SĐT. B4 chạm vào ô. B5 kiểm tra lại focus nếu ô chưa được chọn, thử chạm lại trước khi gõ và báo rõ nếu vẫn lỗi. Dùng cho q1, q2 và các máy nối sau. Chưa thử bản sửa trên Swarmote thật.

- B6 dùng một cú vuốt dài và nhanh hướng về cuối danh sách quốc gia, sau đó đọc lại để tìm `United States +1`. Nếu thấy các mục sau Mỹ mà chưa thấy mục cần chọn, tool vuốt ngược ngắn để tìm lại. Áp dụng cho luồng chung. Chưa đo khoảng cuộn thực tế trên Swarmote.

- Luồng SMS dùng chung đợi đủ 4 giây tính từ lúc bấm gửi rồi mới đọc URL OTP. Thời gian chuyển màn được tính vào 4 giây. Nếu người dùng đã gửi tay, tính từ lúc tool nhận ra màn SMS lần đầu. Mỗi lần thử gọi lại URL với yêu cầu kiểm tra lại bộ nhớ đệm. 133 bài kiểm tra đã qua, gồm kiểm tra thời gian chờ còn lại. Chưa xác minh với URL thật.

- Báo cáo mới trên q1 cho thấy b6 cuộn chậm, b9 báo nhiều Continue và b11 nhận HTTP 403 dù Amazon đã xác nhận gửi SMS. Sửa trong `build_common_steps` cho mọi máy. B6 vuốt dài trong vùng danh sách khi nhận diện được và chỉ bấm đúng `United States +1`. B9 gộp các vùng Continue lồng nhau và dùng lại cây UI đã xác nhận ô tên. Giảm khoảng chờ giữa các lần kiểm tra màn. B11 báo rõ lỗi URL OTP và vẫn cho tiếp tục từ mã nhập tay. 133 bài kiểm tra đã qua. `cloud-scan` chưa thấy ADB nên chưa đo tốc độ hay kiểm chứng cây UI thật.

- 131 bài unittest đã qua, gồm nhánh menu danh sách, b4 chọn Sign In khi cây UI có nhãn lặp và dừng khi vẫn mơ hồ, b6 cuộn qua mục US ẩn và b10 bấm SMS trước mọi lần đọc URL; đồng thời các kiểm tra trước đó cho luồng chung b4–b11 và nối lại q2 từ mốc menu đã lưu. Nhánh `MENU_OPEN` nối lại ADB serial trước khi báo q2 đã tới menu; tool báo rõ nếu thiếu hàng Amazon hoặc serial. Test cửa sổ nhận 12 hàng, giữ đúng thẻ/URL theo máy và hiện nút thử q2. Đã thử trực tiếp mở form New Profile và đóng bằng Cancel, không gửi Create. Chưa thử lại trên máy thật.
- Lúc kiểm tra ngày 13/11/2026, Swarmote có q1, q2, q3. Người dùng đã thử q1 và gửi năm ảnh mới: form SĐT cùng lỗi b6/b9/b10; sau đó xác nhận q1 hiện ở form SĐT. Người dùng báo q2 tới menu ba gạch rồi dừng, tool chỉ ghi đã tới menu mà không báo lỗi. Mã có nhánh mốc `MENU_OPEN` cũ không nối lại ADB và các điều kiện âm thầm dừng; đã sửa và test mô phỏng, chưa thử lại q2 thật. Chưa xác minh URL OTP sau gửi hoặc màn sau Create. Lệnh `cloud-scan` trong môi trường phiên này không tìm thấy ADB Swarmote/Android SDK nên không thể tự đọc máy trực tiếp.
- Người dùng gửi tiếp sáu ảnh q1: b6 lỗi khi danh sách quốc gia vẫn ở chữ A, b9 báo nhiều Continue dù form có một nút nhìn thấy, b10 báo HTTP 403 khi vẫn ở màn WhatsApp và nút SMS chưa được bấm. Mã nguồn hiện tại chọn nút b9 theo khả năng bấm/vị trí dưới ô tên, chỉ đọc URL tại b11 sau khi bấm SMS; đã bổ sung lọc bounds cho ô mở mã quốc gia và test hồi quy b6/b10. Các thông báo trên màn phù hợp với tiến trình tool chưa nạp mã mới, nhưng chưa xác minh được tiến trình đó. Không đóng hoặc đặt lại phiên vì hàng nhập chỉ ở RAM. Sáu ảnh mới ở `flow_images/q1/latest_errors/` và [IMAGE_EVIDENCE.md](IMAGE_EVIDENCE.md).
- Người dùng gửi ảnh q1 dừng tại b4 dù menu danh sách hiện Sign In ngay dưới Customer Service. Bộ chọn cũ dùng `_unique` nên dừng khi cây UI có nhãn lặp. Mã mới ưu tiên Sign In có thể bấm, rồi giới hạn theo mốc Customer Service; nếu vẫn nhiều ứng viên thì dừng. Có thể bấm Sign In thủ công rồi Tiếp tục trên phiên cũ; b4 nhận form SĐT hiện tại. Chưa có dump ADB q1 thật, chưa xác minh sửa trên máy. Ảnh lưu `flow_images/q1/15_b4_list_sign_in_ambiguous.png`.
- Tên q1–q12 được cố định cho các slot; tool dừng nếu tên đã có để tránh trùng. Người dùng chưa quyết định sẽ dùng lại q1–q3 hay tạo profile mới tên khác. Đây là câu hỏi cần giải trước khi đổi chính sách tên.
- `graphify.exe` trên máy hiện báo lỗi `uv trampoline failed to canonicalize script path`; `python -m graphify` hoạt động.
- Graphify đã tạo `graphify-out/graph.json`, `graph.html`, `GRAPH_TREE.html` và `GRAPH_REPORT.md`. Xem [GRAPH_AUDIT.md](GRAPH_AUDIT.md) để biết chính xác phần đã lập chỉ mục và phần còn thiếu. Graph chứa AST mã nguồn cùng file/tiêu đề/liên kết tài liệu sau `python -m graphify update .`. Xem [ASSET_INDEX.md](ASSET_INDEX.md) cho sáu PNG giao diện (năm ảnh lịch sử đã gom vào `assets/ui_history/`) và [IMAGE_EVIDENCE.md](IMAGE_EVIDENCE.md) cho hai mươi ba ảnh q1/q2 cùng một ảnh menu chung trong `flow_images/`. Các ảnh này được đưa lên repository công khai theo yêu cầu bàn giao; có thể hiển thị SĐT/OTP trên ảnh gốc. Nội dung pixel chưa được trích xuất ngữ nghĩa vì không có LLM API key hoặc Ollama; phải mở ảnh gốc khi cần. Các cạnh INFERRED của Graphify có thể sai, cần đối chiếu mã. Xem số node/cạnh hiện tại trong `GRAPH_REPORT.md` để tránh dùng số cũ.

## Tài liệu chi tiết

Kế hoạch cải thiện độ ổn định và thời gian chờ b1–b11, chưa triển khai mã, ở [2026-11-13-b1-b11-reliability.md](docs/superpowers/plans/2026-11-13-b1-b11-reliability.md). Kế hoạch giữ nguyên driver ADB, yêu cầu đo baseline trước khi chỉnh timeout/retry, và không đụng phiên q1 đang hoạt động.

Ảnh q1 ở b11 cho thấy Amazon đã gửi SMS và form nhập OTP đang hiện, nhưng trình đọc URL OTP báo không đọc được. Người dùng xác nhận URL bị chặn khi gọi trực tiếp, nên bộ đọc chung bỏ gọi HTTP trực tiếp; ưu tiên Chrome ẩn, Edge ẩn rồi Chrome có giao diện qua trang thử thách/chuyển hướng. Nếu Chrome hiện tự tắt hoặc lỗi trang, tự mở lại. Mỗi lượt đọc dài tối đa 30 giây; nếu chưa có mã mới, b11 chạy lượt đọc tiếp theo cho tới hết hạn tổng của lượt tự động hóa, rồi báo rõ rằng chưa lấy được OTP mới. Playwright tự đóng Chrome sau khi đọc được OTP hoặc hết hạn tổng. Chưa xác minh trực tiếp với URL OTP thật.

Ảnh q1 mới cho thấy b4a báo `UNKNOWN` khi form Amazon vẫn hiện nhãn `Enter mobile number or email` và nút `Continue`. Bộ nhận diện dùng chung trong `amazon_android/account_flow.py` đã sửa để nhận cặp dấu hiệu đó dù cây UI WebView thiếu tiêu đề hoặc EditText, đồng thời tránh coi riêng nhãn `Country/region code` là màn chọn quốc gia khi dấu hiệu form vẫn còn. Sửa áp dụng cho q1, q2 và mọi máy đang dùng `build_common_steps`. Chưa xác minh trên máy thật; không khởi động lại phiên đang mở vì dữ liệu chỉ ở RAM.

**Đây là quy trình đang được hướng dẫn từng ảnh, chưa phải quy trình đầy đủ.** Đọc [STEP_INVENTORY.md](STEP_INVENTORY.md) để thấy từng mốc P01–P08a, q1/q2 b1–b3, b4–b11 và các mốc chưa có ảnh. Đọc [FLOW_PROGRESS.md](FLOW_PROGRESS.md) để biết mức kiểm chứng. Sau đó đọc [POST_MENU_REQUIREMENTS.md](POST_MENU_REQUIREMENTS.md), [MENU_ROUTING.md](MENU_ROUTING.md), [Q1_FLOW.md](Q1_FLOW.md), [Q2_FLOW.md](Q2_FLOW.md), [OTP_DESIGN.md](OTP_DESIGN.md), [VERIFICATION.md](VERIFICATION.md), [README.md](README.md). Không suy ra q3–q12 đã được tự động hóa chỉ vì b4–b11 dùng chung.

- Ngày 13/11/2026: ảnh q1 mới dừng tại b8 dù Amazon đang hiện form `Create account` với ô `First and last name`; các lỗi trước đó cũng dừng ở ô SĐT. Nguyên nhân chung là UIAutomator chỉ thấy WebView nên thiếu chữ và `EditText`. Đã nối OCR ảnh chụp trực tiếp trong bộ đọc dùng chung b4–b11: khi cây Android không phân loại được màn hình hoặc thiếu ô nhập, OCR tạo nhãn/vùng ô tạm trong RAM; b4a, b5, b9, b11a và b11 dùng lại bộ chọn ô này. Với ô OCR, app thử chạm tối đa ba lần và xác nhận bàn phím Android hiện trước khi gõ. Thêm `rapidocr` và `onnxruntime` vào dependencies; bộ cài xác minh hai thư viện này và tải cùng dependencies dự án. Đã kiểm tra cú pháp Python (`py_compile`); chưa chạy unittest, chưa cài OCR vào môi trường đang mở và chưa xác minh trên q1 thật. Vì vậy tiến trình app q1 đang mở chưa nạp mã mới; cần nạp lại app sau khi người dùng đã lưu trạng thái phiên.

## Đợt tăng tốc và tự phục hồi b4–b11 ngày 13/11/2026

- Bộ đọc học cách đọc WebView theo serial trong từng lượt: sau khi OCR nhận ra màn hợp lệ, các lần đọc kế tiếp chụp ảnh mới và OCR trước, không dump lại cây Android trong 20 giây. Hết khoảng này hoặc OCR không đọc được thì thử lại cây Android. Không giữ ảnh hay vùng bấm cũ làm kết quả cho màn mới; nhánh OCR kiểm tra Amazon là cửa sổ có focus trước khi dùng ảnh.
- Lỗi XML, timeout ADB, ảnh đọc tạm thời thất bại được thử lại tối đa ba lần. Màn UNKNOWN ở đầu các bước form được đọc lại trong tối đa 6 giây trước khi từ chối; không áp dụng cho màn sau Create chưa có đặc tả. Giới hạn chờ màn kế tiếp là 20 giây và trả về ngay khi màn đúng hiện ra; không thêm một lần ngủ 20 giây. Tổng thời hạn của từng máy và nút Dừng vẫn được kiểm tra.
- Ô tạm biến mất được đọc lại trước khi gõ. Mọi trường tên/SĐT/OTP có cùng kiểm tra focus; khi chạm lại ô OCR phải đọc vị trí mới và xác nhận bàn phím thực sự hiện. Nếu ADB lỗi khi gõ, đọc lại nội dung trước; chỉ gõ phần thiếu khi cây Android xác nhận tiền tố ổn định. OCR có thể bỏ sót ký tự nên không được dùng một tiền tố OCR để quyết định gõ nối, kể cả tại lần Tiếp tục.
- `RegistrationState` thuộc `PostMenuSession`, giữ dấu gửi SMS, mã trong RAM và dấu Create khi luồng được dựng lại. Khi serial đổi, các callback được nối lại đúng serial dù điểm tiếp tục không đổi. Ghi ý định SMS/Create trước khi gọi ADB và quan sát màn sau lỗi truyền; không tự gửi lặp chỉ vì kết quả ADB không rõ. Các trạng thái đang tự thử lại được phát qua bảng tiến trình hiện có.
- Đã cài dependencies khai báo vào `.venv` của dự án bằng `pip install -e .`, gồm RapidOCR 3.10.0 và onnxruntime; `pip check` và kiểm tra import của bộ cài đạt. Mô hình OCR trong gói được nạp thành công. `Launch Swarmote Tool.pyw` qua `launcher.main` ưu tiên Python của `.venv` khi có, để dùng đúng dependencies ở lần mở tiếp theo. Không đóng/mở lại phiên q1 đang chạy; dữ liệu mẻ đang mở vẫn chỉ trong RAM.
- Bộ tìm viền ô dùng pixel và tọa độ chữ mới, nhận viền xám/xanh và tách ô khỏi khung bao form. Không suy ra ô bằng tỷ lệ màn hình khi không có viền. Nếu OCR bỏ sót toàn bộ chữ có sẵn, kiểm tra mực chữ trong ô ngăn coi nhầm ô là trống; con trỏ mảnh vẫn được chấp nhận. Ảnh lỗi mới của người dùng được OCR cục bộ trong RAM, nhận đúng CREATE_FORM cùng một ô tên trống; không đưa nội dung tài khoản vào log.
- PASS: 187 unittest trong `.venv`, `pip check`, import dependencies bộ cài và RapidOCR thật trên form tổng hợp trống/đã có chữ cùng ảnh lỗi người dùng. Không có thao tác bấm/gõ trên q1 thật trong đợt này; chưa có số đo tốc độ toàn luồng sau thay đổi. Graphify của Python hiện tại chưa có module và `uv` bị từ chối truy cập, nên graph chưa được cập nhật cho đợt này. Chi tiết tại [VERIFICATION.md](VERIFICATION.md).

## B6 danh sách quốc gia vẫn mở sau khi chọn — 13/11/2026

Ảnh mới có United States +1 nằm giữa United Kingdom +44 và Uruguay +598; lỗi báo vẫn COUNTRY trong lúc chờ IDENTIFIER. B6 dùng chung sửa vùng vuốt khi đọc bằng OCR: lấy các hàng quốc gia hiện bên dưới tiêu đề, không lấy kích thước toàn form nền. Xa US dùng vuốt dài nhanh; tới nhóm gần US hoặc cuối danh sách thì dùng cú vuốt ngắn theo hướng cần tìm, không lặp fling mạnh. Sai số nhỏ của bounds OCR được chấp nhận khi kiểm tra hàng đã đứng yên. Sau cú chọn, nếu hộp COUNTRY chưa đóng, đọc lại và chọn lại đúng hàng US +1 tối đa bốn lần; chỉ hoàn tất khi form hiện US +1. Không tự đóng hoặc nạp lại app đang mở. PASS: 191 unittest và OCR thật trên ảnh đính kèm nhận COUNTRY/United States +1; chưa thử lại b6 trên thiết bị thật. Graphify vẫn chưa cập nhật vì môi trường thiếu module.

## UiAutomator2 được cho phép cài và đã tích hợp — 13/11/2026

Yêu cầu mới của người dùng cho phép cài phương án phù hợp để tăng tốc, thay thế giới hạn chưa cài thành phần Android của lần đánh giá trước. Đã cài UiAutomator2 3.7.1 vào `.venv`, triển khai u2.jar và chạy bộ đọc độc lập trên q1 đúng serial 127.0.0.1:57451 qua ADB Swarmote 5037. Không cài IME hoặc thao tác tài khoản. q1 lúc đo ở MENU; đọc native khi giữ kết nối khoảng 0,31–0,58 giây, ADB dump khoảng 2,4 giây, ADB screenshot+OCR khoảng 6,7 giây sau khởi tạo. Cold start riêng có thể 3–8 giây. Không suy rộng số đo menu sang b6 hoặc toàn luồng.

`amazon_android/ui_backend.py` giữ client/khóa theo serial, đọc đầy đủ roots ở depth 150; lỗi thì ngừng client và nghỉ 30 giây trước khi thử lại. `account_flow` ưu tiên bộ đọc này và dùng đường ADB/OCR dự phòng; b6 dùng fling.toEnd giới hạn ba swipe khi xác nhận được duy nhất một native container, còn cú vuốt ngắn nằm trong bounds container mới. Không lặp ADB swipe sau RPC có kết quả không rõ. Đã thêm dependency và kiểm tra bộ cài. PASS: 200 unittest và kiểm tra đọc thật của adapter trên q1. Chưa thử native scroll trên hộp quốc gia hoặc q2; phiên tool đang mở chưa nạp adapter, không tự đóng vì dữ liệu RAM. Báo cáo đầy đủ: [2026-11-13-uiautomator2-comparison.md](docs/2026-11-13-uiautomator2-comparison.md). Graphify hiện thiếu module nên graph chưa có file mới.


## q3/q4 đã nối b1–b3 và thử đồng thời bốn luồng — 13/11/2026

Người dùng hướng dẫn q3 Groceries and Drinks → Home and DIY → Books and Reading; q4 tab Giỏ hàng → Pets → Home and DIY. Đã thêm q3_flow.py, q4_flow.py và profile_navigation.py; desktop.POST_MENU_STEP_FACTORIES chứa slot 0–3. Nút Thử qN và luồng sau menu của q3/q4 được bật. q5–q12 vẫn chờ hướng dẫn. q1/q2 giữ nguyên b1–b3; b4–b11 vẫn chỉ ở build_common_steps, trạng thái mỗi máy do PostMenuSession.registration giữ riêng.

Cart được tìm bằng content-desc Cart Tab và xác nhận tab chọn/màn giỏ hàng; trước Pets và Home and DIY quay về menu khi cần. OCR dự phòng ghép đúng nhãn thẻ hai dòng, kể cả bbox chữ hai dòng chồng nhẹ; không ghép chữ giữa hai cột. Đã đối chiếu thật bằng OCR với ba ảnh đính kèm: đủ ba nhãn q3, màn giỏ q4, và Pets. Không lưu ảnh riêng tư vào repo.

PASS: 211 unittest. Một kiểm tra dùng bốn thread và barrier, dựng bốn factory thật, chạy b10/b11 đồng thời với dữ liệu/nguồn OTP giả riêng; mã về đúng callback/hàng/serial, cả bốn session DONE và RegistrationState riêng. Kiểm tra này không gọi URL hay thao tác điện thoại thật. Người dùng sẽ tự chạy thử q1–q4; chưa khẳng định đã chạy bốn máy thật.

Để dùng bốn profile đã có: chọn số máy 4, nhập đủ bốn hàng trước khi gắn máy đầu tiên, Start các profile và mở Amazon ở menu, rồi lần lượt chọn Máy 1–4 và bấm Thử qN; worker máy trước vẫn chạy khi gắn máy kế. Nếu tạo mẻ profile mới thì Settings giới hạn Running phải ít nhất 4 để cả bốn được Start cùng đợt. Không tự tạo trùng q1–q4; không tự đóng hoặc đặt lại phiên tool đang mở. Cần mở lại tool sau khi giữ dữ liệu để nạp factory mới. Chi tiết tại Q3_FLOW.md, Q4_FLOW.md, VERIFICATION.md. Graphify hiện thiếu module nên graph chưa có symbol mới.


## Sửa shortcut ghim mở nhầm IDLE — 13/11/2026

Người dùng báo biểu tượng ghim lại mở IDLE. Kiểm tra shortcut TaskBar IDLE (Python 3.12 64-bit).lnk thấy Arguments trỏ tới idlelib/idle.pyw, không phải tool. Đã sao lưu shortcut gốc vào .test_tmp/original_idle_pin.lnk rồi sửa đúng shortcut đang ghim: Target là .venv/Scripts/pythonw.exe, Arguments -m amazon_android.desktop, WorkingDirectory là root dự án. Tạo thêm Swarmote Tool.lnk trên Desktop OneDrive của người dùng; không thay liên kết file Python toàn hệ thống và không khởi động lại Explorer.

Module windows_identity.py gán AppUserModelID Swarmote.AmazonWorkspace, lệnh relaunch, tên và icon cho cửa sổ; desktop khởi tạo identity trước/sau tạo root. windows_identity.create_shortcut tạo .lnk có cùng AppID. Icon swarmote_tool.ico chuyển định dạng từ asset prism có sẵn, đã thêm package-data. Đã mở tool thật, agent-desktop xác nhận cửa sổ Swarmote · Amazon workspace hiện; đọc property store xác nhận AppID và lệnh relaunch đúng. Không reset dữ liệu mẻ, không chạy máy Android. PASS: 213 unittest (hai bài mới cho lệnh relaunch và thứ tự ghi properties). Graphify thiếu module nên graph chưa được cập nhật.
## Dự phòng dùng chung khi chạy song song — 14/11/2026

Các lỗi q3 nhiều nhãn Terminal và q1 không xác nhận được menu đã có nhánh xử lý tiếp trong thời hạn: Terminal được gom theo Group UIA, lần lượt thử từng Group riêng của đúng cửa sổ q3 và đọc lại ADB Shell sau mỗi lần; menu nhận thêm tên các thẻ danh mục, thử lại Browse khi tab vẫn chưa chọn và dùng bộ đọc Android chung khi XML thiếu chữ. Không dùng ảnh cửa sổ desktop chồng nhau để quyết định máy.

Các bước b1–b9 của q1–q4 tự thử lại tối đa hai lần khi bộ đọc/locator báo lỗi tạm thời, mỗi lần đọc trạng thái hiện tại trước khi hành động. Bộ đọc Android tự thử đến hết thời hạn của máy. b10 gửi SMS, b11 OTP và Create không được phát lại mù khi kết quả gửi chưa rõ; mã giữ dấu đã gửi và quan sát màn tương ứng. Lỗi dữ liệu sai hàng, sai Device ID hoặc trạng thái không phân biệt được vẫn báo dừng để tránh tác động nhầm máy. q5–q12 chưa có b1–b3 được hướng dẫn; không khẳng định có thể chạy hết 12 máy. Chưa thử trên Swarmote thật hoặc xác minh màn sau Create.

Unittest mô phỏng: 261 PASS; py_compile các module liên quan PASS. Graphify chưa chạy được vì Python dự án không có module graphify.


## Bộ cài offline chia sẻ — 14/11/2026
Thêm packaging/build_bundle.py và install_bundle.py: ZIP Windows x64 kèm CPython 3.12, dependencies/models, Chromium đúng revision Playwright, VC++ runtime và Swarmote 1.2.0 (checksum chính thức). Bản đóng gói đặt đường dẫn browser qua sitecustomize; bản nguồn giữ browser channel hiện có. Có manifest SHA256, kiểm tra import/OCR/browser trước shortcut. Không tự chạy installer hoặc thao tác điện thoại trên máy hiện tại. Xem packaging/README.md. Hai test browser mới và bảy test OTP PASS; toàn suite dừng sau 54 dấu tiến độ, chưa hoàn tất. Graphify query/update/tree thất bại vì Python thiếu module graphify. Chưa thử Windows sạch hoặc luồng thật trên nhiều điện thoại.

## Bản chính boom4may và bản dự phòng — 14/11/2026

`D:\boom4may` là checkout riêng của `quantrantran692004-spec/boom4may`; `D:\sinhvien` giữ nguyên làm bản dự phòng của `sinhvientudonghoa`. Không trộn mã, môi trường `.venv`, dữ liệu mẻ hoặc Git history giữa hai thư mục. Boom4may có `Q1_FLOW.md`–`Q4_FLOW.md`, 26 ảnh trong `flow_images/` và 42 ảnh trong `docs/user_screenshots/`; q5–q12 vẫn chờ hướng dẫn b1–b3. Cây Graphify phải được cập nhật từ chính thư mục này sau thay đổi, không dùng cây của bản dự phòng. Tool đang mở không tự nạp mã sau khi cập nhật tài liệu hoặc cây.

## Thu panel Apps sau khi mở Amazon — 14/11/2026

Thêm bước chung trong `_prepare_phone`: sau `open_amazon`, trước `open_home_menu`, kiểm tra panel App Store của đúng cửa sổ Swarmote. Nếu còn hiện, Invoke nút Apps một lần và xác nhận panel ẩn; nếu đã ẩn thì đi tiếp. Không đổi b1–b11 hay luồng riêng q1–q4. Ảnh gốc lưu ở `flow_images/shared/02_apps_panel_open.png`. Chưa thử trên máy thật sau sửa; tool đang mở chưa tự nạp mã mới.

## q5 b1–b3 riêng, b4–b11 chung — 14/11/2026

Người dùng chốt q5 bấm Toys, Kids and Baby → Office & Professional → Sports & Outdoors. Chỉ bấm từng thẻ; nếu thẻ mở trang riêng, tự quay về menu để tìm thẻ tiếp, nếu menu vẫn hiện thì bấm ngay. Đã nối `q5_flow.py` vào factory Máy 5, dùng nguyên `build_common_steps` từ b4; không sửa luồng q1–q4. Chưa có ảnh hoặc lượt chạy q5 thật. q6–q12 còn chờ b1–b3 riêng.

## q6 b1–b3a riêng, b4–b11 chung — 14/11/2026

Người dùng chốt q6: b1 Trang chủ xem 2 giây, b2 Giỏ hàng xem 2 giây, b3 về menu, b3a bấm một thẻ rồi chuyển b4. Chọn Devices and Electronics từ menu thẻ, Electronics ở menu danh sách; b3a là phần con của bước thứ ba để giữ b4 chung ở index 3. Nếu thẻ mở trang khác, b4 `_ensure_menu` tự về menu để tìm Sign In. q6 không đi theo nhánh menu danh sách vốn bỏ qua b1–b3 của máy khác. Chưa thử q6 trên máy thật. q7–q12 chưa có hướng dẫn riêng.

## Điều tra q1/q2 mượt, q3+ lỗi thất thường khi chạy song song — 14/11/2026

Chưa có lỗi/màn hiện hành của q3+ để quy kết từng lần dừng. Kiểm tra mã thấy hai điểm có thể làm lỗi thay đổi theo thời điểm: (1) sau thẻ danh mục, `_ensure_menu` trước đây chỉ phát một lần Back hoặc Browse rồi chờ MENU mãi; một lần Back có thể tới Home, nhất là ở q3–q6 có bước riêng khác q1/q2. Nay nhánh chưa ở MENU đọc lại sau mỗi thao tác và đi tiếp tối đa bốn chặng đã xác nhận; nhánh đã ở MENU không chạm. (2) mỗi máy dùng process OCR riêng, RapidOCR/ONNX mặc định `intra_op_num_threads=-1`, `inter_op_num_threads=-1`, có thể tạo nhiều luồng CPU trên mỗi process. Nay mỗi engine đặt 1/1; đã khởi tạo RapidOCR thật và xác nhận cấu hình. Khi kiểm tra, Windows 8 luồng CPU/7,92 GB RAM, còn 1,36 GB RAM trống và ADB thấy 2 cloud phone; đây không phải đo tại lượt nhiều máy bị lỗi. Chưa khẳng định hai sửa này giải quyết mọi lỗi; cần chạy q3/q4 thật để đối chiếu.

## Hàng đợi 4 máy với giới hạn 2 Running — 14/11/2026

Người dùng xác nhận Settings đang đặt tối đa 2 Running, đã tạo 4 Profile và phải bấm Tiếp tục để mở hai máy sau khi tắt hai máy đầu. Đọc trực tiếp Settings thấy `start_group_size=2`; Swarmote tại lúc kiểm tra cho thấy q1/q2 Offline và q3/q4 Running, nhưng trạng thái này không chứng minh lần chuyển lượt trước tự động. Trong mã, `run_batch` đã có hàng đợi và polling Offline mỗi 2 giây; điểm yếu là nếu Swarmote vừa tắt máy nhưng nút Start chưa sẵn sàng, `start_profile` báo lỗi và `fill_slots` dừng cả hàng đợi.

`ProfileStartNotSubmitted` nay phân biệt lỗi trước khi gọi nút Start. Runner giữ máy đó trong hàng đợi và tự thử lại tối đa 60 giây, báo rõ trạng thái chờ; sau thời hạn vẫn dừng để người dùng sửa. Nếu lời gọi Start đã bắt đầu mà kết quả chưa rõ, runner chỉ đọc lại trạng thái, không tự gửi lặp. Không thay số slot, thứ tự hàng đợi, luồng Amazon hoặc trạng thái riêng từng máy. Test mô phỏng 4 máy/2 slot kiểm tra q3/q4 tự Start sau khi q1/q2 Offline, và nút Start chưa sẵn sàng một lượt vẫn tự phục hồi. 27 test runner/Start PASS. Chưa tắt/mở các máy thật vì phiên người dùng đang chạy; code mới chưa tự nạp vào tool đang mở. Cần giữ dữ liệu phiên trước khi mở lại.

## Settings hiện chậm — 14/11/2026

Theo yêu cầu tách riêng phần giao diện, `_open_settings` nay đưa cửa sổ Settings lên trước và xử lý các tác vụ vẽ đang chờ ngay sau khi tạo Toplevel, rồi mới dựng các điều khiển bên trong. Mục tiêu là có phản hồi nhìn thấy ngay khi bấm Settings. Không đổi giá trị Settings, giới hạn Running hoặc luồng máy. Chưa đo thời gian hiển thị trên phiên GUI thật; phiên đang mở không tự nạp mã mới.

## Dừng riêng máy đang chọn — 14/11/2026

Nút **Dừng Máy N sau bước hiện tại** ở khung chi tiết đặt `phone_stop_after_step[index]` cho máy đang chọn; nút toàn cục đổi nhãn thành **Dừng cả mẻ**. Runner giữ cờ riêng qua hàng đợi, tạo Profile, Start và chuẩn bị máy; PostMenuSession tạm dừng trước bước tiếp theo hoặc tại ranh giới thử lại nếu bước hiện tại lỗi. Dữ liệu, registry, serial và điểm tiếp tục của máy khác không bị xóa. **Tiếp tục** xóa cờ riêng khi chạy lại đúng máy. Dừng tự động hóa không tắt Swarmote Profile, nên slot Running chỉ trống khi Profile chuyển Offline. Có kiểm thử mô phỏng nhiều máy, chưa bấm trên phiên thật; không reset hoặc đóng tool đang mở để nạp mã.

`python -m unittest discover -s tests -q`: 305/305 PASS.

