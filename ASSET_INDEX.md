# Danh mục ảnh nằm trong dự án

Graphify hiện không trích xuất nội dung pixel của PNG do thiếu backend ngữ nghĩa. Danh mục này giúp cây có dấu vết của từng file ảnh hiện có; không dùng chúng làm bằng chứng cho các màn Amazon q1/q2 nếu chưa xem trực tiếp ảnh.

## amazon_android/assets/obsidian_prism.png

1717 × 916 px. Tài nguyên ảnh của giao diện tool, được `desktop.py` nạp vào khung đầu trang.

## amazon_android/assets/swarmote_tool_square.png và swarmote_tool.ico

Icon ứng dụng nền xanh đậm, lăng kính tím sáng, vuông 1254 × 1254 px. `swarmote_tool.ico` được xuất từ PNG này với các cỡ vuông 16–256 px để Windows hiển thị rõ trên Taskbar. Icon cũ là ảnh ngang có nền trong suốt, rất khó thấy ở 16 px; bản cũ còn trong lịch sử Git.

## amazon_android/assets/icons/

28 icon Lucide 0.468.0 từ kho chính thức `lucide-icons/lucide`, có SVG gốc và PNG alpha 96×96 tương thích CustomTkinter. V3 chỉnh nét SVG thành 1,75 px và thêm `list`; `LICENSE` giữ giấy phép và ghi công. `desktop_theme.py` tô màu PNG theo design tokens rồi hiển thị ở 14–20 px; không dùng emoji và không cần tải icon khi chạy. Nhóm gồm smartphone, settings, list, layout-list, clipboard-list, globe, user-round, clipboard-paste, phone, key-round, credit-card, shield-check, link, copy, activity, sliders-horizontal, play, circle-play, square, refresh-cw, lock-keyhole, arrow-down-to-line, trash-2, circle-check, loader-circle, clock, circle-alert và chevron-down. Tk dùng chevron vector sẵn có của OptionMenu; các icon không đủ chỗ trên nhãn hẹp được giữ trong bộ tài nguyên mà không ép vào giao diện.

## assets/ui_history/v3_before.png, v3_after.png và v3_final.png

Ảnh Tk trước/sau V3 ở cùng kích thước 1460×750 px, scale 125%, cùng 12 hàng dữ liệu giả. Dùng để kiểm tra màu, phân cấp chữ, mật độ và trạng thái; không phải bằng chứng hoạt động của máy thật. Tự đánh giá và giới hạn trong DESIGN.md.

Ảnh `v3_final.png` ghi bản sau yêu cầu bỏ cột Proxy và mở lớn mặc định: phần nội dung 1472×724 px sau khi giới hạn theo màn hình kiểm tra 1536×864; giữ nguyên proxy bên phải. Dữ liệu hoàn toàn giả.

## assets/ui_history/reset_check.png

1743 × 1047 px. Ảnh PNG ở gốc dự án; nội dung chưa được trích xuất vào graph.

## assets/ui_history/ui-12.png

1375 × 788 px. Ảnh PNG ở gốc dự án; nội dung chưa được trích xuất vào graph.

## assets/ui_history/ui-preview.png

1375 × 788 px. Ảnh PNG ở gốc dự án; nội dung chưa được trích xuất vào graph.

## assets/ui_history/ui-screenshot.png

1375 × 788 px. Ảnh PNG ở gốc dự án; nội dung chưa được trích xuất vào graph.

## assets/ui_history/ui_palette_preview.png

1725 × 1000 px. Ảnh PNG ở gốc dự án; nội dung chưa được trích xuất vào graph.

## assets/ui_history/machine7_input_before.png

Ảnh người dùng gửi ngày 14/11/2026: Máy 7 được chọn nhưng phần đầu khung chi tiết
chỉ hiện ô proxy; các ô Amazon riêng nằm dưới vùng cuộn. Dùng để đối chiếu thứ tự
trình bày trước khi đưa thông tin Amazon lên đầu khung chi tiết.

Ảnh `flow_images/shared/b6_bottom_stalled_18nov.png` ghi danh sách mã điện thoại tại đáy Uruguay–Åland; đối chiếu thao tác vuốt ngược trong IMAGE_EVIDENCE.md.

Ảnh q1/q2, menu chung và 14 ảnh menu ngẫu nhiên mới nằm trong `flow_images/` và được lập danh mục trong [IMAGE_EVIDENCE.md](IMAGE_EVIDENCE.md). Bảy ảnh gốc b16–b22 ngày 18/11 nằm trong `flow_images/shared/marketplace_us/`, dùng chung hai luồng để đổi marketplace sang United States rồi mở tab hình người. Các bước cũng được chép thành văn bản trong `STEP_INVENTORY.md`, `MENU_ROUTING.md`, `Q1_FLOW.md`, `Q2_FLOW.md`; Graphify chưa đọc nội dung pixel của ảnh. Hai ảnh báo lỗi/trước b16 thêm ngày 18/11 nằm cùng thư mục, tên `08_b16_menu_before_account.png` và `09_b16_focus_error.png`. Bốn ảnh bổ sung 10–13 cùng thư mục ghi lỗi b16/b17 và màn tìm kiếm có bàn phím; ảnh 14 là cận cảnh nút EN cho b17; xem IMAGE_EVIDENCE.md để phân biệt màn thật với thông báo của tool.

Ảnh trạng thái Máy 4 phục hồi lần 45 nằm cùng nhóm b1–b3 ở `flow_images/shared/random_prefix_reference/15_q4_prefix_read_recovery.png`; diễn giải và giới hạn bằng chứng trong [IMAGE_EVIDENCE.md](IMAGE_EVIDENCE.md). Ảnh 16_q1_lens_camera_permission.png và 17_b15_browse_recovery_error.png trong cùng thư mục ghi lỗi chọn camera ở b13–b15 và không trở lại Browse.

Ảnh cận cảnh Account b23 và Your Addresses b24 nằm trong `flow_images/shared/create_address/13_b23_account_closeup.png` và `14_b24_your_addresses_closeup.png`; ảnh cận cảnh ô địa chỉ mặc định b29 và nút Add address b30 nằm tại `15_b29_empty_checkbox_closeup.png` và `16_b30_add_address_closeup.png` cùng thư mục. Sáu ảnh gốc b32–b38, hai ảnh b34 dừng, hai ảnh b37 báo không thấy, cùng ba ảnh cận cảnh mới `11_b33_reload_balance_closeup.png`–`13_b37_card_option_closeup.png` nằm trong `flow_images/shared/reload_payment/`, ánh xạ tại [IMAGE_EVIDENCE.md](IMAGE_EVIDENCE.md). Ảnh b39 nguyên bản `14_b39_use_this_address.png` nằm cùng thư mục theo yêu cầu người dùng; ảnh có tên và địa chỉ cá nhân. Không lưu thêm ảnh form có dữ liệu thẻ hoặc chép các giá trị đó vào tài liệu, log. Graphify chỉ lập chỉ mục tên file, không đọc nội dung ảnh.
