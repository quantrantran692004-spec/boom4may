> Cập nhật 14/11/2026: người dùng đã yêu cầu tiếp tục sửa bằng code. Đã sửa cấu hình COM đa luồng, phạm vi tìm cửa sổ, Stop/progress chuẩn bị và bảng trạng thái; 230 unittest PASS. Chưa xác minh Swarmote thật. Đọc mục đầu PROJECT_HANDOFF.md. Nội dung bên dưới là snapshot bàn giao trước sửa.

# Bàn giao dừng theo yêu cầu người dùng — 13/11/2026

## Yêu cầu mới nhất

Người dùng yêu cầu dừng ở đây để đổi tài khoản và giao người khác xử lý. Chưa tiếp tục sửa/điều khiển sau bản bàn giao này. Không tự chạy mẻ, không reset, không đóng tool/điện thoại; dữ liệu người dùng chỉ trong RAM.

Root thực tế: `D:/visua_code/sinhvientudonghoa-main/sinhvientudonghoa-main` (workspace ngoài còn một cấp thư mục cùng tên). Python dự án: `.venv/Scripts/python.exe`. Chưa có Git repository khả dụng tại root này trong các lần kiểm tra trước.

## Lỗi chính chưa xử lý xong

Chạy nhiều máy cùng lúc: các cloud phone q1–q4 đã khởi động nhưng đều nằm ở Android launcher (System Tools/App Store/Toolbox), chưa mở side panel Apps/App Store để tìm/cài Amazon. GUI tool giữ dòng **Đang tìm z và cài Amazon · q1**, hoặc chỉ **Đang chạy**, không cho biết đang chờ chặng nào. Máy q5 có lúc đợi chỗ vì giới hạn Running. Đây là lỗi trước Amazon/menu/b1–b11, không phải lỗi OTP hay cấu hình q3/q4.

Ảnh báo lỗi gốc trong thư mục `C:/Users/quanminh/AppData/Local/Temp/`:

- `codex-clipboard-364ed3e8-2b00-46b5-811b-886ba6407442.png`: Stop đã bấm nhưng Làm lại và Tiếp tục của các máy lỗi bị khóa; q1 còn cài Amazon, nhiều máy khác báo lỗi.
- `codex-clipboard-25e69cd4-fdae-471f-88a6-0ef41b738f45.png`: q1–q4 cùng đứng Android launcher.
- `codex-clipboard-de985846-2980-48d3-aa79-1fb1e3359f9a.png`: q1–q4 Đang chạy, q5 đợi máy trống.
- `codex-clipboard-0493d296-a050-4514-a8a6-70676ea0bcc1.png`: dòng trạng thái gộp Đang tìm z và cài Amazon.

Ảnh có thông tin riêng tư. Không chép số điện thoại, proxy credential, thẻ, URL token vào log/báo cáo; ảnh mới chưa được sao chép vào repository công khai.

## Bằng chứng trực tiếp đã có

agent-desktop `list-windows` chạy ngoài sandbox đọc được các cửa sổ Swarmote. Lúc kiểm tra gần nhất q1–q4 không còn hiện trong inventory; chỉ thấy main Profiles và:

- q5 — ACN988158062493797 — HWND 788898.
- q6 — ACN988158347837553 — HWND 1509148.

Các giá trị trên là snapshot, có thể đã đổi; phải kiểm tra lại trước khi thao tác.

User trước đó đã cho phép dùng bộ đọc UI Automation sẵn của dự án khi agent-desktop snapshot bị lỗi DACL. Trong đợt lỗi này chỉ dùng UIA để đọc, chưa kích hoạt nút Apps:

- `_phone_window` + `_descendants` đọc q5 trong khoảng 282 ms, q6 khoảng 55 ms.
- Cả hai có đúng một Text `Apps` visible, parent Group. Có Text Terminal visible và một Terminal hidden. Không có TabItem `App Store`.
- Group cha của Apps trên q5 lấy được `iface_invoke`; `iface_selection_item` báo NoPatternInterfaceError; truy cập thuộc tính `iface_legacy_iaccessible` báo AttributeError (không suy ra chắc chắn mọi Legacy pattern đều thiếu).
- Chưa gọi Invoke thực tế để kiểm tra tác dụng, chưa đưa điện thoại lên trước, chưa dùng click tọa độ. Không được kết luận chắc rằng thiếu Invoke hay che cửa sổ là nguyên nhân.

## Đường mã cần xem tiếp

- `runner._prepare_phone`: phát dòng Đang tìm z và cài Amazon rồi gọi `install_amazon`.
- `swarmote_desktop.install_amazon`: gọi `show_apps`; chờ Enter content 20 giây; điền z; chờ Amazon Shopping 60 giây; tìm nút Install cùng hàng; sau đó mở ADB Shell và xác nhận package tối đa 180 giây.
- `show_apps`: `_phone_window(...seconds=60)` rồi lặp tối đa 120 giây, tìm Text Apps và gọi `parent().invoke()`, chờ TabItem App Store 10 giây. Lỗi invoke bị giữ trong `last_seen` và thử lại; không phát tiến trình chi tiết ra GUI. Đây là nhánh nghi vấn đầu tiên vì Apps có mà App Store chưa mở.
- `_descendants` duyệt UIA trực tiếp; mỗi `_prepare_phone` chạy trong thread riêng, có CoInitialize. Chưa chứng minh có lỗi UIA đa luồng.
- Cần thêm tiến trình phân biệt: tìm cửa sổ → mở Apps → chờ App Store → tìm Amazon → xác nhận Install → chờ package. Nếu không tiến triển, cần lý do cụ thể thay vì im lặng lâu.
- Nếu thử foreground/tuần tự hóa thao tác Swarmote, phải kiểm chứng trước; giữ phần Android/OTP theo từng serial song song. Chưa triển khai cách này.

## Phần sửa Stop/Reset đã viết nhưng chưa thử GUI thật

Các file đang thay đổi: `amazon_android/desktop.py`, `runner.py`, `swarmote_desktop.py`, `tests/test_stop_reset.py`, `tests/test_runner.py`.

- `_request_stop` đặt cờ, hủy yêu cầu retry còn đợi và refresh GUI ngay.
- Sau Stop, `_reset` cho tạo form/draft mới để nhập lại trong khi worker cũ kết thúc. Giữ danh sách worker cũ đang draining; chặn chạy/gắn máy mới cho đến khi chúng kết thúc.
- Reset thay queue/dictionary/cancel token bằng đối tượng mới; batch worker, post-menu worker và attach worker giữ context/queue cũ. Kết quả muộn không được ghi serial/OTP/trạng thái vào mẻ mới.
- Máy lỗi có thể bấm Tiếp tục khi mẻ khác còn chuẩn bị: xếp vào `_pending_retries`; chạy lại khi coordinator hiện tại kết thúc. Không chạy đồng thời hai coordinator tạo profile. Đây là retry có hàng đợi, không phải chạy lại lập tức.
- `_wait_for(...stop=...)` và `install_amazon(...stop=...)` nhận cờ hủy. Các vòng đợi Enter content/Amazon/package kiểm tra cờ. `_prepare_phone` nhận biết hủy và báo stopped thay vì error, kiểm tra cờ giữa các chặng.
- **Còn thiếu:** `show_apps`, `_phone_window` và phần mở ADB Shell vẫn có các vòng chờ riêng chưa nhận cờ Stop. Nếu đang kẹt các hàm này, worker cũ vẫn có thể mất thời gian mới thoát; form mới nhập được nhưng chưa chạy mới được. Cần giải quyết cùng lỗi Apps nêu trên.
- GUI tool đang mở chưa tự nạp các thay đổi này. Không hot-patch, không đóng/reset giúp người dùng khi chưa được yêu cầu.

## Kiểm chứng gần nhất

` .venv/Scripts/python.exe -m unittest discover -s tests `: **221 tests PASS**, khoảng 10,1 giây, sau các sửa Stop/Reset. Tám bài mới gồm reset sau Stop, không reset lúc đang chạy chưa Stop, queue retry của hàng lỗi, canceled wait, dừng install báo stopped, chặn mẻ mới khi worker cũ chưa xong, kết quả batch cũ không viết vào draft mới, Stop xóa retry queue.

`py_compile` các file desktop/runner/swarmote_desktop đạt lúc bàn giao. Chưa thử Stop/Reset/Continue trên GUI thật và chưa sửa xong nhánh mở Apps.

Một lượt unittest cũ bị kẹt do fixture install chưa nhận keyword `stop`; đã dừng riêng phiên test bằng Ctrl+C, cập nhật ba fixture rồi chạy lại đủ 221 PASS. Không dừng tiến trình tool của người dùng.

## Bối cảnh đã hoàn tất trước lỗi hiện tại

- q1–q4 đã nối b1–b3 riêng; b4–b11 chung. q3: Groceries and Drinks → Home and DIY → Books and Reading; q4: Cart → Pets → Home and DIY. q5–q12 chưa có hướng dẫn b1–b3.
- UiAutomator2 3.7.1 đã cài và tích hợp ưu tiên đọc; ADB/OCR dự phòng. Chỉ đo đọc MENU q1, chưa kiểm chứng mọi form hoặc b6 native thật.
- Đã sửa shortcut ghim mở IDLE: shortcut trỏ `.venv/pythonw.exe -m amazon_android.desktop`; Desktop có Swarmote Tool.lnk. Windows AppID và relaunch properties riêng đã thêm. Xem PROJECT_HANDOFF.md.
- Graphify: `python -m graphify` đang thiếu module, `uv` từng bị từ chối truy cập. Không khẳng định graph đã cập nhật các symbol mới.

## Cách tiếp tục

Đọc AGENTS.md, PROJECT_HANDOFF.md và bản bàn giao này. Xem lại cửa sổ/serial hiện hành bằng read-only trước; không dùng HWND/serial cũ một cách cố định. Ưu tiên xác nhận vì sao Apps Invoke không mở App Store; đồng thời nối Stop vào các vòng chờ còn thiếu và thêm trạng thái chi tiết. Sau đó thử bằng mock và thử một cửa sổ có người dùng cho phép trước khi kết luận đã chạy được bốn máy.
