# Bộ cài chia sẻ Windows x64

Gửi file `dist/SwarmoteTool-Windows-x64-*.zip`. Người nhận giải nén **toàn bộ**, chạy `CAI_DAT.bat`, hoàn tất bộ cài Swarmote nếu được mở, rồi mở shortcut **Swarmote Tool** trên Desktop. Không cần Python hoặc pip cài sẵn. Khuyến nghị Windows 11 x64.

Gói có runtime CPython 3.12, toàn bộ thư viện trong môi trường dự án, mô hình RapidOCR, Chromium đúng revision của Playwright, bộ cài Microsoft Visual C++ x64 và Swarmote 1.2.0. Cài riêng theo người dùng; mỗi lần cài tạo thư mục mới trong `%LOCALAPPDATA%/Programs/SwarmoteTool`. Cần đủ chỗ cho ZIP, bản giải nén và bản cài, dự kiến ít nhất 5 GB trống.

Trình cài kiểm tra SHA256 từng tệp, chạy thử OCR và trang browser offline trước khi tạo shortcut. Swarmote/ADB phải có trong vị trí mặc định theo người dùng. Bộ cài Microsoft có thể yêu cầu xác nhận UAC hoặc khởi động lại Windows. Hủy hoặc cài sai vị trí sẽ báo lỗi; không báo thành công khi thiếu ADB.

Người nhận tự đăng nhập Swarmote, cần Internet và quyền dùng cloud phone/profile, cùng dữ liệu đầu vào/proxy của họ. Gói chứa mã nguồn, tài liệu và ảnh dự án đã được yêu cầu lưu trữ; không lấy cookies, dữ liệu đăng nhập hoặc profile Windows từ máy nguồn. Đóng gói không khắc phục hay xác nhận các lỗi tự động hóa đang tồn tại, không chứng minh 12 máy chạy hoàn chỉnh.

## Nguồn thành phần

- Chromium: [Playwright browsers](https://playwright.dev/python/docs/browsers). Mỗi phiên bản Playwright cần browser revision tương ứng.
- Microsoft Visual C++: `https://aka.ms/vs/17/release/vc_redist.x64.exe`; tệp đã kiểm tra chữ ký Microsoft hợp lệ khi dựng gói.
- Swarmote: bộ cài cache 1.2.0, SHA512 đối chiếu `https://oss.swarmote.cn/release/win/latest.yml` ngày 14/11/2026. Không có chữ ký Authenticode; checksum khớp máy chủ cập nhật của ứng dụng.
- Giấy phép thư viện/Python/Chromium được giữ trong runtime và thư mục browser.

## Dựng lại

Chạy `.venv/Scripts/python.exe packaging/build_bundle.py` trên máy Windows x64 có CPython 3.12, các dependencies của dự án, bộ cài Swarmote cache đúng checksum, Microsoft runtime installer tại `.test_tmp/vc_redist.x64.exe` và Chromium tương ứng tại `.test_tmp/bundle-browsers` hoặc cache Playwright. Script dừng nếu thiếu hoặc sai phiên bản; không tự nhận bản cũ là tương thích.

`install_bundle.py --check` chỉ xác minh gói và runtime; không cài Swarmote, không tạo shortcut, không điều khiển điện thoại.
