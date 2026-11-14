## b1–b3 ngẫu nhiên trên 12 máy, không dùng OCR — 14/11/2026

Theo yêu cầu mới, ba lượt chỉ bấm/vuốt trong vùng danh mục theo kích thước Android của từng serial. Mẻ mới xáo 12 điểm đầu và gán duy nhất cho từng máy; test hai batch xác nhận không trùng điểm b1 giữa 12 máy. Lỗi lệnh chạm thử các điểm khác và vuốt; b4 vẫn dùng bộ nhận diện cũ. `python -m unittest discover -s tests -q`: **307/307 PASS**. Bản ONNX Runtime 1.32 trong `.venv` hiện crash khi import; bản 1.20.1 thử riêng đọc được cả 14 ảnh, nhưng chưa thay `.venv` của tool đang chạy. Chưa chạy 12 máy thật.

## b1–b3 bắt buộc có ba cú bấm — 14/11/2026

Đối chiếu 14 ảnh menu mới đã lưu: thẻ danh mục mở mục con trong cùng menu; Sign In nằm ở cuối; khi cuộn thấp tiêu đề menu có thể biến mất. Kiểm thử mô phỏng xác nhận đủ ba bước trước b4, chặn b4 nếu thiếu một cú bấm, lỗi ADB không đánh dấu hoàn tất, thử mục con sau lỗi thẻ, mục lạ trong thân menu làm dự phòng, menu cuộn vẫn được nhận diện và nhãn thẻ xuống hai dòng được ghép. Không chạy ADB/tạo tài khoản trên máy thật.

`python -m unittest discover -s tests -q`: **311/311 PASS**.

## Nhiều proxy trên một dòng — 14/11/2026

`python -m unittest discover -s tests -q`: **300/300 PASS**. Parser và ô proxy máy đang chọn nhận bốn proxy giả lập cách nhau bằng dấu cách, giữ thứ tự Máy 1–4; mật khẩu của một proxy có dấu cách vẫn giữ nguyên nếu không có tiền tố proxy tiếp theo; giới hạn 100 mục vẫn được áp dụng sau tách. Không dùng proxy thật, không kiểm tra mạng hay tạo Profile Swarmote.

## b1–b3 ngẫu nhiên cho 12 máy — 14/11/2026

`python -m unittest discover -s tests -q`: **296/296 PASS**. Test mới kiểm tra 12 slot cùng dùng factory ngẫu nhiên, mỗi máy có ba bước trước b4 chung, không chọn Sign In, ưu tiên ba mục khác nhau, giữ lựa chọn khi dựng lại bước để Tiếp tục và bốc lại với trạng thái mẻ mới. Nhánh menu dạng danh sách không bỏ qua ba bước; khi menu chưa có mục bấm hoặc tạm chưa trở lại được, phần ngẫu nhiên không dừng máy. Lượt đọc b1–b3 có hạn 15 giây để tránh kẹt vô thời hạn. Chưa thao tác Swarmote thật hoặc xác minh 12 máy chạy đồng thời.

## b6 cuộn tới đáy rồi vuốt ngược — 14/11/2026

Chạy `.venv\Scripts\python.exe -m unittest discover -s tests -q` với thư mục tạm trong repository: **289/289 PASS**. Test b6 xác nhận chưa đảo chiều tại Wallis, tiếp tục fling khi thấy Zimbabwe, chỉ đảo chiều khi các hàng cuối đứng yên; phép vuốt ngược dùng khoảng cách bốn hàng và giới hạn trong vùng danh sách cho cả Android native và ADB dự phòng. Đây là kiểm thử mô phỏng; chưa thao tác trên Swarmote thật.

## Lỗi chạy song song q3 Terminal trùng / q1 chưa thấy menu — 14/11/2026

Hai ảnh người dùng báo q3 dừng "có nhiều nút Terminal đang hiện" và q1 dừng "Amazon chưa hiện menu ba gạch". Các ảnh thông báo không chứa ảnh Android hiện hành hoặc cây UIA nên chưa thể quy kết mọi trường hợp cụ thể. Đối chiếu mã tìm thấy hai điểm dừng quyết định bằng dấu hiệu thiếu: open_adb_shell đếm từng Text Terminal chứ không đếm Group cha duy nhất; open_home_menu chỉ nhận heading Shop by category và chỉ bấm Browse menu một lần.

Sửa mở ADB: dedup Group Terminal theo UIA runtime_id rồi mới kiểm tra số nút; hai nhãn của một Group chỉ Invoke một lần. Hai Group thật khác nhau vẫn dừng để tránh chọn nhầm q3.

Sửa mở menu: nhận thêm bộ ba tên danh mục của menu thẻ khi heading bị thiếu trong XML; nút Browse menu có thể bấm lại tối đa ba lần nếu hai lượt đọc kế tiếp xác nhận tab vẫn unselected. Sau timeout ADB của cú bấm, đọc màn tiếp theo trước khi quyết định bấm lại. Lỗi không phải timeout vẫn báo thay vì nuốt. Không thay b4–b11 và không tự gửi lại SMS/Create.

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


# Biên bản kiểm tra thực tế — 2026-11-12

## q1 menu danh sách b4 có nhiều Sign In — 2026-11-13

- Ảnh q1 cho thấy menu danh sách mở, Sign In hiện dưới Customer Service, nhưng tool dừng b4 vì cây UI có nhiều nhãn Sign In. Ảnh lưu ở `flow_images/q1/15_b4_list_sign_in_ambiguous.png`.
- Đã sửa bộ chọn chung của b4: ưu tiên phần tử có thể bấm; nếu nhãn lặp, dùng Customer Service hiện trên cùng menu làm mốc. Nếu vẫn mơ hồ thì giữ nguyên cơ chế dừng và Tiếp tục. `131/131` unittest PASS, gồm hai trường hợp nhãn lặp và một trường hợp dừng khi vẫn mơ hồ.
- `cloud-scan` không tìm thấy ADB Swarmote/Android SDK trong môi trường này; chưa xác minh trực tiếp cây UI q1 hoặc bản mã của tiến trình tool đang mở. Cách tiếp tục ngay: bấm Sign In thủ công trên máy rồi bấm Tiếp tục ở Máy 1; b4 nhận form SĐT nếu đã hiện.

## Sáu ảnh q1 mới: b6, b9, b10 — 2026-11-13

- Ảnh cho thấy dropdown quốc gia ở đầu chữ A khi b6 báo bounds lỗi; form b9 có bàn phím và một Continue thấy được; b10 báo URL HTTP 403 trong khi màn vẫn là WhatsApp, nút Send code by SMS chưa bấm. Lưu ảnh gốc ở `flow_images/q1/latest_errors/`.
- Mã nguồn hiện tại lọc vùng bấm hợp lệ trước khi mở dropdown, cuộn tới mục US +1 hiện ra; b9 chọn nút Continue đang thấy và dưới ô tên; b10 bấm SMS rồi xác nhận màn SMS, URL chỉ được đọc tại b11. Hai test hồi quy mới kiểm tra b6 cuộn từ đầu danh sách và thứ tự b10. `128/128` unittest PASS.
- `cloud-scan` không tìm được ADB Swarmote/Android SDK trong môi trường này. Chưa đọc UI q1 thật, chưa kiểm chứng tiến trình tool hiện trên màn đã nạp mã mới. Không khởi động lại tool vì dữ liệu mẻ chỉ ở RAM.

## Menu ba gạch dạng danh sách — 2026-11-13

- Người dùng gửi ảnh menu dạng danh sách chữ và xác nhận thao tác: bấm Home, chỉ xem 2–5 giây, quay về menu, bấm Sign In ở b4. Ảnh được lưu ở `flow_images/shared/01_list_menu.png`.
- Đã nối bộ phân loại dùng cây UI Android hiện tại, định tuyến chung cho q1/q2: danh sách bỏ qua b1–b3 thẻ, Home 2–5 giây trong thời hạn lượt rồi b4 quay lại menu; dạng thẻ giữ luồng riêng. Tiếp tục hồi phục được nếu đã ở Home. Không dùng tọa độ ảnh.
- PASS mô phỏng: `126/126` unittest, gồm phân loại bố cục, định tuyến q1/q2, giữ dạng thẻ, hồi phục từ Home và b4 quay về Sign In. **Chưa thử trên Swarmote thật** vì phiên kiểm tra không có ADB q1/q2; chưa xác minh biến thể UI khác hoặc màn sau Create.

## Mẻ 12 máy và tên cố định — 2026-11-13

- Mẻ vừa rồi chỉ tạo q16. Registry cũ ghi q17–q27 `UNCERTAIN/CREATING` với cùng lỗi “Cần đúng một cửa sổ quản lý Swarmote; tìm thấy 2”; kiểm tra danh sách Swarmote hiện chỉ có q16. Đây là lỗi tìm cửa sổ trước bước Create, không phải 11 Profile đã tạo.
- Bộ tìm cửa sổ nay chọn đúng cửa sổ Profiles khi có thêm một cửa sổ Swarmote khác; nếu vẫn không xác định được thì báo lỗi trước Create và dừng các hàng còn lại thay vì giữ 11 tên ở trạng thái chưa rõ. Tên mẻ mới cố định Máy 1=q1 đến Máy 12=q12, chặn tên đã có trong Swarmote. Workspace dùng metadata trong bộ nhớ phiên; nút Làm lại và lần mở app tiếp theo bắt đầu lại từ q1. Đã bỏ file metadata cũ; Profile q16 trên Swarmote vẫn còn. 75/75 bài test PASS. Chưa chạy lại mẻ 12 proxy thật vì dữ liệu proxy cũ chỉ ở bộ nhớ tiến trình đã đóng.

## Nút Làm lại / mẻ mới — 2026-11-13

- Sửa `_set_editing(False)` không khóa nút Làm lại khi chỉ khóa ô nhập của mẻ đã bắt đầu. Nút vẫn bị khóa riêng trong `_launch` khi runner thực sự đang chạy và được mở lại khi runner kết thúc. Vì thế mẻ được khôi phục nhưng không có việc tự chạy có thể chuyển sang mẻ mới bằng một lần bấm.
- Kiểm tra UI với mẻ khôi phục lỗi: nút ở trạng thái `normal`, bấm `_reset` xóa jobs cũ, mở lại ô nhập và đưa số máy về 1. Bộ test hiện có 73/73 PASS. Đã nạp lại giao diện; ảnh chụp cửa sổ thật xác nhận nút Làm lại sáng và các ô nhập đã mở trong mẻ mới q16.

## Giao diện sáng, dễ đọc — 2026-11-13

- Chuyển bảng màu desktop sang nền xanh xám nhạt, thẻ trắng, chữ xanh than và nút chính xanh ngọc; giữ cột máy và khối hình 3D xanh than. Đổi màu hover, selected, disabled và trạng thái trong bảng; khi khôi phục mẻ, lỗi cũ hiện đúng trạng thái đỏ thay vì “Đợi máy trống”.
- Đã xem ảnh chụp giao diện mới ở kích thước 1725×1000. Các cặp chữ/nền chính đạt tương phản tối thiểu 4,97:1; kiểm tra 73/73 test PASS và detector không báo lỗi. Đã nạp bản giao diện mới vào tiến trình desktop, xác nhận các Profile q11–q15 không đổi trạng thái do việc thay giao diện.

## q14 mở Amazon lần đầu — 2026-11-13

- Registry q14 ban đầu `ERROR/APP_INSTALLED` với thông báo “đã thoát hoặc crash sau khi mở”. ADB xác nhận package Amazon đã cài nhưng không có PID; màn trước là launcher. Android events ghi `wm_create_activity` cho Amazon lúc 22:46:07.255 và `wm_task_removed` lúc 22:46:07.421; crash buffer chỉ ghi crash `com.android.gallery3d`, không có `am_crash` Amazon trong phần log kiểm tra. Vì vậy chưa đủ bằng chứng gọi đây là crash Amazon.
- Gửi lại lệnh `monkey` trên q14: Amazon có PID ngay và lên foreground sau khoảng 2 giây. Đã sửa `open_amazon` để giữ nguyên app nếu đã foreground, theo dõi tối đa 8 lần kiểm tra mỗi lần mở, thử lại nhiều nhất một lần khi không còn tiến trình, và phân biệt app chạy nhưng không foreground với app không giữ được tiến trình.
- Kiểm tra thật sau sửa: `open_amazon` trả `amazon_foreground=True`; `open_home_menu` trả `HOME_MENU_OPEN`, `account_input_sent=False`. Registry q14 được cập nhật `DONE/MENU_OPEN`. `python -m unittest discover -s tests -q`: 71/71 PASS.
- Giao diện đang mở trước đó vẫn là tiến trình cũ nên chưa nạp sửa lỗi. Đã bổ sung khôi phục an toàn: khi khởi động lại, runner tính mọi Profile đang Running trong mẻ vào giới hạn máy, còn giao diện chỉ tự tiếp tục Profile READY/RUNNING chưa tới menu. Kiểm tra 73/73 test PASS. Đã khởi động lại giao diện; Swarmote xác nhận q13 và q14 Running, q15 Offline/READY và tiếp tục đợi chỗ theo Settings = 2. q11 ERROR/APP_INSTALLED giữ nguyên để người dùng chọn Tiếp tục riêng; q12–q14 không bị chạy lại.

## Ẩn cửa sổ quản lý khi tạo Profile — 2026-11-13

- Settings có tùy chọn lưu qua phiên `Ẩn cửa sổ Swarmote khi tạo Profile`, mặc định tắt để các mẻ cũ giữ nguyên cách chạy. Khi bật, chỉ cửa sổ quản lý được ẩn trong `create_profile` và được hiện lại bằng `SW_SHOWNA` ở cả nhánh thành công lẫn lỗi. Cửa sổ điện thoại Running không bị ẩn.
- Đã thử thật trên Swarmote đang mở: ẩn cửa sổ quản lý, đọc được 264 UIA nodes qua handle; kích hoạt `New Profile` khi cửa sổ ẩn, thấy form `Create`, bấm `Cancel` và khôi phục cửa sổ. q11/q12 vẫn visible trong lúc cửa sổ quản lý ẩn. Không tạo Profile mới trong phép thử này.
- Settings dialog dựng được ở chế độ ẩn (kích thước yêu cầu 427 px, cửa sổ đặt 450 px). `python -m unittest discover -s tests -q`: 69/69 PASS.

## q8/q9 ADB và màn xác minh — 2026-11-13

- q9 đã cài Amazon nhưng lệnh `uiautomator dump` từng trả mã Windows `3221225786` dù stdout xác nhận XML đã được ghi. Hàm đọc UI nay chấp nhận trường hợp này sau khi đọc và kiểm tra XML thực, thử lại tối đa ba lần khi dump lỗi. Đã khởi động lại cửa sổ tool để nạp sửa lỗi; registry xác nhận q9 `DONE/MENU_OPEN`.
- q8 hiện có giao diện Amazon `Authentication required` / `Verify mobile number` / `Enter security code` (đọc qua ADB). Không bấm Back hoặc thay đổi màn xác minh. Tool sẽ báo rõ trạng thái này và dừng ngay khi gặp trong các lần chạy sau. q10 đã tạo Profile, còn chờ chỗ trống theo giới hạn hai máy Running.
- `python -m unittest discover -s tests -q`: 65/65 PASS, gồm dump có mã thoát bất thường nhưng XML hợp lệ, retry dump lỗi, và giữ nguyên màn xác minh.

## Ẩn cửa sổ cmd khi gọi ADB — 2026-11-13

- `core.run` trước đây khởi chạy `adb.exe` từ `pythonw.exe` mà không có cờ Windows `CREATE_NO_WINDOW`; nhiều lệnh kiểm tra package và giao diện Android có thể làm cửa sổ cmd xuất hiện lặp lại. Đã thêm cờ này cho các lệnh nền trên Windows, không đổi đầu ra/timeout.
- `python -m unittest discover -s tests -q`: 62/62 PASS. Bài kiểm tra mới xác nhận `subprocess.run` nhận `CREATE_NO_WINDOW` trên Windows. Gọi ADB thật qua `cloud_serials()` sau sửa vẫn thấy 2 thiết bị đang kết nối.

## Sửa New Profile và chờ Apps — 2026-11-13

- `python -m unittest discover -s tests -q`: 61/61 PASS. Tên qN mới được cấp bằng registry và đọc tên đang hiển thị qua UIA; runner không nhập qN vào ô tìm kiếm `Profile Name` trước Create. Bài kiểm tra Apps mô phỏng giao diện xuất hiện trễ và xác nhận nút được kích hoạt theo tên/vai trò UIA. Bài kiểm tra khôi phục mẻ chỉ nhận mẻ mới nhất còn việc, không tự khôi phục mẻ cũ.
- Registry của mẻ này từng ghi q5 và q6 `ERROR/STARTED` với cùng lý do `không thấy nút Apps sau khi máy khởi động`. Sau khi giao diện tải xong, UIA đọc được nút Apps ở cả hai máy. Đã mở Apps, tìm `z`, cài Amazon và xác nhận package qua ADB trên q5/q6; sau đó mở Amazon tới menu ba gạch trên cả hai. Không nhập dữ liệu tài khoản.
- Hàm `show_apps` chờ sự xuất hiện của điều khiển Apps/App Store tối đa 120 giây nhưng thao tác ngay khi thấy; không dựa vào tọa độ hoặc ảnh. Đã thay cửa sổ tool cũ bằng bản mới; bản mới khôi phục đúng mẻ q5–q7. Sau khi q6 về Offline, q7 tự gửi Start, mở Apps, cài Amazon và tới menu ba gạch. Registry xác nhận q5/q6/q7 đều `DONE/MENU_OPEN`.

## Luồng tạo và mở song song — 2026-11-13

- `python -m unittest discover -s tests -q`: 56/56 PASS. Có kiểm tra q2 được tạo khi q1 còn đang cài, lệnh Start trả về ngay khi máy còn khởi động, giới hạn 2 máy không mở q3 trước khi một máy tắt, tự mở q3 sau khi có chỗ, nút Dừng kết thúc hàng đợi, nút Tiếp tục vẫn tính máy khác đang Running trong cùng mẻ, tìm và Start Profile nằm ngoài trang danh sách hiện tại.
- Runner hiện gửi Start ngay sau khi xác nhận từng Profile; luồng điện thoại mở Apps, tìm `z`, cài Amazon và mở menu trên cửa sổ riêng trong khi luồng quản lý tiếp tục tạo Profile kế tiếp. `Terminal` chỉ dùng ADB và giao diện trở về Apps. Settings lưu giới hạn số máy Running của mẻ từ 1 đến 12.
- Trước thay đổi lịch chạy này, đã kiểm tra thật q2, q3, q4: cả ba Start, cài Amazon từ Apps, mở tới menu ba gạch; trạng thái Android và Swarmote được xác nhận. Các Profile đó đã được đánh dấu `MENU_OPEN` trong registry.
- Đã kiểm tra thật bộ lọc `Profile Name` của Swarmote qua UIA: tìm đúng q2, kiểm tra tên không tồn tại và khôi phục ô lọc ban đầu. Nhánh này cho phép kiểm tra Profile khi danh sách vượt 20 dòng/trang mà không chuyển trang bằng chuột.
- Luồng xen kẽ mới chưa chạy thử trên một mẻ 12 proxy thật. Kiểm tra 53 bài là mô phỏng runner và các nhánh UIA; không suy ra tốc độ hay độ tin cậy thực tế của Swarmote khi tạo và cài đồng thời 12 máy.

## Cập nhật luồng mẻ trước đó — 2026-11-13

- `python -m unittest discover -s tests -q`: 42/42 PASS. Có bài kiểm tra mẻ 3 → 5 → 4, cấp tên qN qua lần mở registry, dùng lại tên lỗi trước Create, giữ tên Create chưa chắc chắn, tạo hết Profile trước khi mở máy, Tiếp tục sau khi cài app không cài lần hai, nhóm Start 1–12 và Settings được giữ qua phiên sau. Mô phỏng UIA xác nhận Start(2) chỉ chọn đúng q2/q3 và bỏ chọn q1 cũ.
- Smoke test cửa sổ CustomTkinter không nối Swarmote: dán mẻ 3 → Mẻ mới → 5 → Mẻ mới → 4; số hàng, trạng thái nút Chạy và dữ liệu đuôi PASS.
- Smoke test snapshot GUI: sau Chạy, các ô dán/sửa và chọn số máy bị khóa; Mẻ mới mở lại input và bỏ snapshot cũ. PASS.
- Smoke test GUI: chỉ dán proxy vẫn bật Chạy; Settings mở được; Làm lại / mẻ mới xóa dữ liệu nhập. PASS.
- Sau mẻ lỗi được báo: metadata q2–q7 đều `ERROR/RESERVED`; kiểm tra read-only trên Swarmote xác nhận q2–q7 đều vắng. Bản code mới dự kiến q2–q4 cho mẻ ba máy. Bấm trạng thái lỗi trong bảng sẽ hiện nguyên nhân cụ thể; metadata mới lưu `last_error` không chứa proxy hoặc thông tin Amazon.
- UI Automation đọc trực tiếp Swarmote: q1 đang Offline; q2 không tồn tại; bộ cấp tên với file tạm chọn q2. Không dùng chuột/focus và không tạo Profile mới trong phép thử này.
- q1 đã được mở thật, Amazon đã có trên máy và UI Android tới menu ba gạch. Lần đầu bộ nhận diện đòi chữ `Shop by category.` có dấu chấm, trong khi máy trả `Shop by category`; sau sửa, kiểm tra trực tiếp `open_home_menu` trả `HOME_MENU_OPEN` và `account_input_sent=False`. q1 sau đó được xác nhận Offline.
- Form Swarmote đang cài có `Batch Create` (chọn proxy đã lưu) và `Batch Import` (Download/Import Template), nhưng chưa xác minh định dạng hay kết quả tạo riêng từng máy. Đã mở form chỉ để đọc nhãn UIA rồi đóng bằng Cancel, không tạo Profile.
- Tạo Profile mới, Start nhiều Profile bằng `Start(N)`, chạy mẻ 3/5/4 thật và cài Amazon theo runner mới: NOT TESTED. Các thao tác này tiêu thụ slot/tài nguyên Swarmote và cần proxy mẻ đang sử dụng. Không có kết luận tốc độ thực tế hoặc độ tin cậy của `Start(N)` từ unit test.

Máy kiểm thử: Windows 11 Pro, Intel Core i3-10100F, RAM vật lý khoảng 8 GB.

| Hạng mục | Kết quả | Bằng chứng |
| --- | --- | --- |
| Python và kiểm tra môi trường | PASS | `python -m amazon_android.cli doctor` chạy bằng Python 3.11.0. |
| Android SDK | PASS | Công cụ Google được tải từ `dl.google.com`, checksum gói Command-line Tools khớp repository của Google. ADB, emulator, avdmanager và system image Android 35 Google Play đều được `doctor` tìm thấy. |
| Tăng tốc phần cứng | PASS | `emulator -accel-check`: `WHPX(10.0.26300) is installed and usable`. |
| Tạo hai AVD riêng | PASS | `create-avd 1` và `create-avd 2` chạy thành công; `doctor` liệt kê `Amazon_Android_01`, `Amazon_Android_02`; mỗi cấu hình dùng Google Play image, `PlayStore.enabled=yes`, RAM 1536 MB. |
| Khởi động Android 01 | PASS với ngoại lệ RAM | Người dùng cho phép `--force-low-memory`; emulator boot xong sau 88,6 giây với 1535 MB RAM trống lúc bắt đầu. Máy còn khoảng 244 MB RAM khi boot xong. Đã dừng emulator sau thử nghiệm. |
| ADB kết nối Android 01 | PASS | `adb devices` thấy `emulator-5554`; `sys.boot_completed=1`; `adb emu avd name` trả `Amazon_Android_01`. |
| ADB kết nối Android 02 | NOT TESTED | Android 02 chưa khởi động. |
| Google Play trên Android 01 | PASS | `check-play 1` xác nhận `com.android.vending` và `com.google.android.gms`. |
| Cài và mở Amazon Shopping trên Android 01 | NOT TESTED | Đã mở trang Google Play, nhưng Play Store hiển thị màn hình chưa đăng nhập. Người dùng chuyển hướng sang Swarmote trước khi cài. |
| Điều hướng đăng ký, OTP, hai thiết bị độc lập | NOT TESTED | Cần hoàn thành thử nghiệm A/B trước. |

Mười một phép thử đơn vị an toàn đã qua bằng `python -m unittest discover -s tests -v`; chúng không thay thế kiểm thử Android/Amazon thật. Chưa triển khai Appium, FastAPI, React/Tauri hoặc đăng ký Amazon.

## Hướng Swarmote theo ảnh người dùng

Swarmote đang chạy Profile 3 dưới dạng điện thoại đám mây, trên ảnh hiển thị Amazon Shopping 32.2.0.100 đã cài. Tài liệu chính thức Swarmote mô tả mỗi Profile là một cloud phone độc lập và App Center có Amazon Shopping. Proxy là cấu hình mạng của Profile; không phải tiến trình tạo Android trên máy Windows. Phân tích tĩnh đã tìm thấy cơ chế tunnel ADB qua Terminal, nhưng `adb devices` trên Windows hiện chưa thấy Profile Swarmote nào. Chưa có bằng chứng rằng App Center lấy APK từ Google Play. Vì vậy chưa báo PASS cho thử nghiệm Amazon trên Swarmote theo đặc tả.

Đã nghiên cứu ứng dụng Swarmote đang cài bằng REA và thêm kết nối với tunnel ADB do Terminal của Swarmote tạo. Ngày 2026-11-12 đã mở `Terminal > ADB Shell` trên Profile 6. `cloud-scan` thấy `127.0.0.1:49596`, Android 13, Google Play/Play Services và package Amazon. `cloud-open-amazon` xác nhận ứng dụng còn tiến trình và ở màn hình trước. `reported_installer=com.android.vending` nhưng nguồn APK chưa xác minh độc lập. Cổng ADB này chỉ tồn tại khi tunnel hoạt động, không phải cấu hình cố định.

Đã thêm lệnh đọc giao diện Swarmote và tạo Profile với proxy SOCKS5 qua UI Automation không chiếm chuột. Người dùng cung cấp proxy, Profile `Amazon 01` được tạo thật và danh sách Swarmote xác nhận Device ID `ACN986192827056137` cùng IP kiểm tra. Lệnh tạo lúc đầu báo timeout vì giao diện cập nhật chậm; kiểm tra lại xác nhận đã tạo, không thử tạo lại. Profile được khởi chạy trong Swarmote; chưa xác minh lệnh `swarmote-start` đã tự khởi chạy từ trạng thái Offline.

Trên `Amazon 01`, công cụ mở ADB Shell bằng UIA nền, xác nhận Android 13 qua serial tạm thời `127.0.0.1:64832`, thấy Amazon chưa cài, tìm Amazon Shopping trong App Store Swarmote và kích hoạt nút Install bằng UIA. ADB sau đó xác nhận package Amazon xuất hiện và `cloud-open-amazon` xác nhận tiến trình ở màn hình trước. Android UI hierarchy cho thấy nút `Create an account`; đã bấm nút đó bằng ADB theo bounds của nút và tới màn `Sign in or create account` với đúng một ô email/số điện thoại và nút Continue. Lệnh `swarmote-ready 'Amazon 01'` chạy lại thành công theo trạng thái idempotent. Chưa nhập thông tin tài khoản, bấm Continue hoặc gửi đăng ký; chưa xác minh nguồn APK độc lập.

Đã thêm giao diện cục bộ cho 1–5 máy và mã điền tên/số điện thoại/mật khẩu rồi dừng trước nút gửi. Giao diện đã được kiểm tra import/biên dịch; bước điền form Amazon sau Continue chưa có dữ liệu người dùng để kiểm thử thật. Nếu locator không nhận ra trường cần điền, mã báo lỗi và dừng, không tự bấm ngẫu nhiên. `Amazon 01` hiện đã được người dùng dừng (Offline), nên không khởi chạy lại chỉ để thử nghiệm.

## Q1 từ menu ba gạch tới OTP SMS — 13/11/2026

- PASS: 118 bài `python -m unittest discover -s tests -q`, gồm phân loại các màn b1–b11, ngăn bấm gửi SMS/Create lặp khi màn phản hồi chậm, ánh xạ ADB serial đúng profile, kiểm tra URL OTP riêng từng máy trong luồng b4–b11 dùng chung, đường gắn q1/q2 đã có chỉ chạy sau khi xác nhận Running + menu, bảng 12 hàng có cột trống/thẻ/URL dạng link Markdown cùng hàng, và form tạo Profile chỉ được điền sau khi New Profile mở thật.
- PASS: smoke test cửa sổ desktop dán 12 hàng thẻ + URL, hiện `count=12`, hàng Máy 12 giữ đúng thẻ/URL và bảng chỉ hiện đuôi thẻ. Mô phỏng gắn q1 từ menu vẫn giữ 12 hàng; nút chạy mẻ và Tiếp tục của q2 bị khóa.
- PASS: khởi tạo cửa sổ desktop với nút **Thử q1 từ menu ba gạch**.
- READ-ONLY: kiểm tra Swarmote ngày 13/11/2026 cho q1 `Offline`, Device ID `ACN987500546883608`.
- Tại phép kiểm tra ban đầu, chưa thử b1–b11 thật vì q1 Offline. Sau đó người dùng đã thử q1 và cung cấp các lỗi b6/b9/b10; xem mục năm ảnh lỗi bên dưới. Chưa có lượt hoàn tất b1–b11 trên q1.
- NOT TESTED: GET URL OTP thật và màn Amazon sau nút `Create your Amazon account`. Tool chưa xác nhận tài khoản đã tạo thành công từ ảnh hiện có.
- NOT TESTED: b1–b11 trên q2 thật. Hai ảnh q2 chỉ xác nhận ba thao tác riêng; mã đã nối b4–b11 dùng chung và nút thử q2 xuất hiện khi chọn Máy 2.

## Nút New Profile trên Swarmote — 13/11/2026

- UIA read-only thấy danh sách hiện có q1, q2, q3 và nút New Profile. Với tên q4 vắng trên cùng trang, `profile_status` mới trả `ProfileNotFound` mà không thay đổi ô tìm kiếm.
- Lệnh UIA `Invoke` vào New Profile khi cửa sổ quản lý bị che có thể trả thành công nhưng không mở form. Đã sửa nhánh tạo: đưa cửa sổ quản lý lên trước, bấm New Profile và xác nhận đủ dấu hiệu form trước khi điền tên/proxy. Test Proxy và Create cũng kích hoạt cửa sổ trước khi bấm; tùy chọn ẩn cửa sổ vẫn ẩn giữa các lần bấm.
- PASS trực tiếp: kích hoạt New Profile theo cách mới làm form xuất hiện; bấm Cancel trở lại danh sách. Không nhập proxy và không gửi Create trong phép thử này.

## Năm ảnh lỗi q1 và sửa luồng chung — 13/11/2026

- Người dùng gửi ảnh q1 đang ở form SĐT trống, b6 lỗi vùng bấm US +1, b9 có nhiều Continue, b10 URL OTP HTTP 403 trước khi gửi SMS và b10 không ở màn chọn SMS. Người dùng xác nhận q1 hiện ở form SĐT.
- Đã sửa `account_flow.py` dùng chung cho mọi máy: chạm ô ở b4; cuộn qua mục quốc gia ẩn/không có bounds; lọc nút Continue đang hiển thị và có thể bấm; bấm gửi SMS rồi mới đọc URL. Tiếp tục có thể quay về b4 từ màn SĐT mà không xóa hàng dữ liệu. Màn SMS đã được người dùng mở thủ công được nhận mà không bấm gửi lần hai.
- `otp.py` thử lại HTTP 403 trong giới hạn chờ sau khi SMS được gửi. Nếu kéo dài, dừng tại b11 để kiểm tra link của đúng hàng. Vì APIFC chỉ trả nội dung SMS và không có dấu thời gian, lần đầu sau gửi chưa thể chứng minh mã khác mã cũ nếu không đọc trước.
- PASS mô phỏng: `118/118` unittest. Lệnh `python -m amazon_android.cli cloud-scan` trong môi trường này báo không tìm thấy ADB Swarmote/Android SDK; chưa thử lại trên q1/q2 thật, chưa gọi URL OTP thật và chưa xác minh màn sau Create.

## q2 đứng ở menu ba gạch — 13/11/2026

- Người dùng báo q2 đã tới menu ba gạch rồi đứng; tool chỉ ghi đã tới menu, không có lỗi. Chưa nhận được ảnh trạng thái chi tiết hoặc xác nhận nút khởi chạy, nên không khẳng định một nguyên nhân duy nhất.
- Phát hiện nhánh `run_batch` với registry đã có `MENU_OPEN` phát `done` nhưng không gọi `menu_ready`, khiến desktop thiếu ADB serial và bỏ qua `_start_post_menu`. Đã sửa để nối lại đúng serial q2 Running trước khi phát `done`. Khi q2 Offline, báo Start máy rồi Tiếp tục. Khi thiếu hàng Amazon hoặc serial, desktop hiện rõ lý do tại hàng Máy 2.
- PASS mô phỏng: `122/122` unittest, gồm kiểm tra q2 đã có `MENU_OPEN` nhận đúng ADB serial trước `done`, q2 Offline không báo chạy tiếp, và hai trường hợp thiếu serial/dữ liệu không dừng im lặng. **Chưa thử lại trên q2 thật** vì môi trường phiên này không tìm thấy ADB Swarmote/Android SDK.

## Tự phục hồi và đọc WebView — 13/11/2026

- PASS: `.venv/Scripts/python.exe -m unittest discover -s tests`: 187 bài, 0 lỗi. Bao gồm học chế độ OCR riêng từng serial và hết hạn gợi ý, OCR sau dump hỏng, hai lần đọc lỗi liên tiếp, nút Dừng, màn đang tải, ô tạm biến mất, focus tên, vị trí ô thay đổi, gõ dở sau lỗi ADB, ngăn gõ lặp từ tiền tố OCR, lỗi truyền sau cú chạm, giữ dấu SMS/Create khi dựng lại luồng và nối lại serial khi bước không đổi.
- PASS: 12 bài riêng bộ tìm ô trên ảnh: nhiều kích thước/lề, ô có chữ, viền focus xanh, khung form lồng ngoài ô, nút bị bàn phím che, loại vùng vàng/đường phân cách/đoạn văn, OCR bỏ sót chữ và ô trống chỉ có con trỏ.
- PASS: RapidOCR 3.10.0 thật chạy trên ảnh tổng hợp 600×1100: form trống và form chứa `Example User` đều có một EditText; nội dung đọc lại khớp. Một lượt sau khởi tạo engine khoảng 0,79 giây trên ảnh tổng hợp; đây không phải tốc độ ADB hoặc thời gian toàn luồng trên Swarmote.
- PASS: OCR cục bộ trên phần điện thoại trong ảnh lỗi b8 người dùng gửi: nhận `CREATE_FORM`, một ô tên trống, bounds `[26,120][303,156]`. Ảnh chỉ được xử lý trong RAM, không lưu bản cắt và không ghi chữ riêng tư ra log.
- PASS: cài dependencies vào `.venv` bằng `pip install -e .`, `pip check` không báo xung đột; `_runtime_imports_work()` của bộ cài thành công. Đã ghi dấu môi trường sẵn sàng của bộ cài. Launcher `.pyw` dùng Python trong `.venv` ở lần mở sau; hai bài kiểm tra launcher dùng mock tiến trình, không mở GUI thật.
- NOT TESTED: tốc độ và thao tác b4–b11 của bản này trên q1/q2 đang chạy. Phiên q1 được giữ nguyên, không khởi động lại tool hay bấm/gõ trên máy thật. Không dùng kết quả trên ảnh tĩnh để khẳng định đã thao tác thành công trên thiết bị.

## B6 cuộn quốc gia và chọn lại — 13/11/2026

- PASS: 191 unittest toàn dự án; bốn kiểm tra thêm cho vùng vuốt OCR nằm trong danh sách thay vì form nền, hộp chọn chưa đóng sau lần chạm đầu, sai số nhỏ của bounds và giới hạn bốn lần chọn lại.
- PASS: RapidOCR thật trên ảnh quốc gia mới người dùng gửi nhận COUNTRY và đúng mục United States +1. Đây là kiểm tra ảnh tĩnh, chưa xác minh cú vuốt/bấm trên q1 thật.
- B6 vẫn phát gesture bằng ADB; cây Android là đường đọc thông thường và OCR là dự phòng cho WebView thiếu node. Chưa cài hoặc đánh giá UiAutomator2 trên Android; người dùng trước đó yêu cầu phê duyệt riêng trước khi cài thành phần thiết bị.

## Cài và đo UiAutomator2 theo phê duyệt mới — 13/11/2026

- PASS: UiAutomator2 3.7.1 trong `.venv`; u2.jar chạy thành công trên q1 đúng tunnel đã xác nhận. Không cài APK bàn phím, không gọi send_keys/clipboard, không bấm/gõ tài khoản.
- PASS: adapter thực đọc MENU ba lần; lần đầu gồm khởi tạo 8126,5 ms, hai lần giữ kết nối 579,8 và 307,4 ms. So sánh đọc thuần cùng menu: ADB XML khoảng 2,4 giây; OCR sau khởi tạo khoảng 6,7 giây. Màn MENU có nội dung động, không khẳng định các snapshot giống nhau từng pixel.
- PASS: 200 unittest toàn dự án, gồm chín bài cho client riêng serial, tái sử dụng kết nối, hierarchy đầy đủ, lỗi/cooldown, cây rỗng, từ chối tunnel không thuộc Swarmote, native fling có giới hạn, mini swipe theo bounds và không vuốt trùng khi RPC lỗi không rõ đã giao.
- PASS: `pip check`, import dependencies của bộ cài và cập nhật dấu `.venv` sẵn sàng. Metadata editable install đã cập nhật dependency UiAutomator2.
- NOT TESTED: native scroll và độ chính xác trên hộp quốc gia q1, các form WebView sau menu, hoặc q2. Tool đang mở chưa nạp mã mới. Xem [báo cáo so sánh](docs/2026-11-13-uiautomator2-comparison.md).


## Nối q3/q4 và kiểm tra bốn worker — 13/11/2026

- PASS: 211 unittest toàn dự án. Kiểm tra thứ tự b1–b3 q3/q4 và phần b4–b11 trùng luồng chung; q4 chạm tab Cart và xác nhận trang; không chạm lại khi đã ở Cart; Pets/Home and DIY gọi đường về menu; gắn q3/q4 đúng profile/serial.
- PASS: bốn thread chạy b10/b11 bằng bốn factory thật, cùng đạt barrier chờ OTP trong thời hạn test, nhận bốn mã giả từ đúng URL giả và đưa vào đúng serial/callback. Bốn PostMenuSession độc lập đều DONE. Không gọi mạng hoặc gõ lên thiết bị trong kiểm tra này.
- PASS: RapidOCR thật trên ba ảnh đính kèm: đủ Groceries and Drinks, Home and DIY, Books and Reading; nhận giỏ hàng trống và Pets. Đã có hồi quy nhãn xuống dòng với bounds chồng nhẹ và từ chối ghép chữ khác cột.
- NOT TESTED: chạy b1–b11 q3/q4 thật, và bốn cloud phone thật cùng lúc. Chưa tự chạy mẻ, tạo profile, đóng/reset tool hay thay Settings của phiên người dùng.


## Ghim taskbar — 13/11/2026

- PASS: 213 unittest, gồm relaunch chạy đúng module desktop và AppID được đặt sau lệnh/tên relaunch.
- PASS: đọc lại shortcut ghim và Desktop: Target .venv/pythonw.exe, Arguments -m amazon_android.desktop, WorkingDirectory đúng dự án.
- PASS: cửa sổ Swarmote · Amazon workspace hiện; AppID và RelaunchCommand được đọc lại từ Windows property store đúng giá trị. Chưa bấm vật lý vào biểu tượng taskbar đã ghim để kiểm tra cache Explorer.
## Kiểm chứng bỏ thời hạn tổng sau menu — 14/11/2026

Test mới xác nhận q1–q4 dùng đúng cùng code b4–b11, phiên cũ hơn một giờ từ lúc mở menu vẫn chạy b4 và tiếp bước sau; 265 unittest PASS. `py_compile` cho post_menu/account_flow/desktop PASS. Không thử Swarmote thật. Giới hạn 3/4/5 phút trước đây nằm ở PostMenuSession, không phải khác biệt trong b4–b11 của q3/q4.

## b6 Country US +1 — 14/11/2026

Hai ảnh q1 mới xác nhận hàng United States +1 đã nhìn thấy nhưng popup không đóng sau bốn lần chạm. Test tái hiện hai nhánh: vùng chữ không đóng popup nhưng giữa hàng đóng; fling tới cuối rồi reverse để tìm US. Toàn bộ unittest 267 PASS, `py_compile` mã liên quan PASS. Đây là kiểm thử mô phỏng; chưa bấm trên máy thật.

## Focus ô nhập b4–b11 — 14/11/2026

- Bộ xử lý chung chỉ gõ SĐT, tên hoặc OTP sau khi chạm và đọc lại đúng ô/màn, có focus trực tiếp hoặc xác nhận bàn phím khi cờ focus thiếu/OCR. Thử tìm lại bounds và chạm tối đa ba lần; không gõ nếu vẫn chưa xác nhận. Có test cho chạm trượt, ô dịch vị trí, khung WebView trống tạm và giá trị nhập dở.
- `.venv/Scripts/python.exe -m unittest discover -s tests -q`: **288/288 PASS** trên đối tượng giả. Test thời hạn tổng cũ được sửa để kiểm tra Stop theo quy tắc hiện hành. Chưa kiểm chứng trên Swarmote thật; tool đang mở chưa tự nạp bản mã mới.

## Dừng riêng một máy — 14/11/2026

Nút trong khung chi tiết đặt cờ riêng theo máy, không đặt cờ dừng cả mẻ. Runner kiểm tra cờ ở ranh giới tạo Profile, Start, cài Amazon, nối ADB và mở menu; phiên b1–b11 kiểm tra trước bước kế tiếp và ở ranh giới thử lại khi bước lỗi. Test mô phỏng dừng q2 khi chờ slot, q3 vẫn tự Start; dừng một phiên sau b1, phiên khác vẫn hoàn tất và phiên đã dừng tiếp tục từ b2. Chưa thử GUI/Swarmote thật; tiến trình tool đang mở không tự nạp mã mới.

`python -m unittest discover -s tests -q`: **305/305 PASS**.

