# Kiểm tra lịch sử và bản đồ (địa lý, chủ quyền)

> Chuyển nguyên văn từ CLAUDE.md. Quy tắc Hoàng Sa, Trường Sa là bắt buộc. Nguồn: `archive/CLAUDE-truoc-tai-cau-truc-18-11.md`. Chuyển ngày 18/11/2026.

## Bản đồ có vùng biển phía đông Việt Nam: MỌI khung hình phải có Hoàng Sa và Trường Sa (chủ kênh yêu cầu 07/11/2026, nhắc lại cùng ngày: "phải note quy tắc này mỗi khi làm bản đồ")
- **Áp dụng cho mọi video có bản đồ, mọi cảnh, mọi khung hình** (cả cảnh zoom gần). Khung nào hiện vùng biển phía đông Việt Nam thì phải có quần đảo Hoàng Sa (khoảng 111,3–112°Đ, 16,5°B) kèm nhãn "Quần đảo Hoàng Sa (Việt Nam)". Trường Sa nằm ngoài ảnh nền `map_relief.jpg` (dừng ở vĩ 13,5°B): thêm thẻ "Trường Sa (Việt Nam) ở phía nam ↓" ở mép dưới khung. Vẫn không ghi tên "Biển Đông" và không vẽ biên giới.
- **Đừng zoom sát bờ biển rồi bỏ đảo ra ngoài khung** (lỗi cảnh Pina tập 2: zoom vào Đà Nẵng nên mất Hoàng Sa, chủ kênh phát hiện). Cảnh cần hiện vùng biển thì chọn mức zoom đủ rộng để Hoàng Sa nằm trong khung (khoảng 150 px mỗi độ, tâm 109,5°Đ, 16,4°B), hoặc nếu phải zoom gần hơn thì cảnh đó không được để lộ vùng biển phía đông.
- **Tự kiểm trước khi giao (bắt buộc, cùng bước xem khung hình):** liệt kê mọi cảnh bản đồ, xem khung đầu, giữa, cuối; cảnh nào có biển phía đông mà thiếu Hoàng Sa hoặc thẻ Trường Sa thì sửa. Ghi kết quả vào báo cáo giao video ("Hoàng Sa, Trường Sa: đủ ở các cảnh …").
- Hàm mẫu: `hsMake(L)` trong `phim_ban_do/doc9x16/trang_vn2.html` (đảo và nhãn Hoàng Sa vẽ trong lớp bị cắt theo khung bản đồ); thẻ Trường Sa dùng `strip(...)`. Video bản đồ 16:9 (`mapfilm3.py`) cũng áp dụng cùng quy tắc.

## Vị trí trên bản đồ phải nằm trên đất liền (chủ kênh nhắc 06/11/2026, từ tập 3: chấm thành và Nhật Nam rơi ra biển)
- Mọi điểm thành, quận, quân cờ phải nằm trên đất liền. Kiểm bằng màu ảnh nền `map_relief.jpg` (công thức px/py trong `trang.html`: x = (lon-102)*520*cos23°*0,5, y = (24,8-lat)*520*0,5 + 1482); điểm biển có xanh dương lớn hơn đỏ. Điểm rải ngẫu nhiên (chấm thành) phải tạo bằng mã, loại điểm nằm biển hoặc cách biển dưới 0,2 độ, rồi nhúng danh sách cố định vào file cảnh.
- Tọa độ quận trong `trang.html` (ví dụ `NN` Nhật Nam) có thể nằm biển ở khung hình khác: kiểm từng điểm trước khi dựng, ghi đè tọa độ riêng trong file cảnh của tập.
- Trước khi giao xem khung hình mọi cảnh có điểm thành, không chỉ vài khung mẫu.
