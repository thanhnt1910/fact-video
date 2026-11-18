# Loạt 'Chuyện cai trị ngàn năm' (9:16)

> Quy tắc riêng của loạt. Nguồn: `archive/CLAUDE-truoc-tai-cau-truc-18-11.md`. Chuyển ngày 18/11/2026.

## Video dọc 9:16 kiểu bản đồ phủ kín khung: loạt "Chuyện cai trị ngàn năm" (trước đó tên "Cách họ cai trị"; chủ kênh đổi nhãn 05/11/2026, nhãn trên video: "CHUYỆN CAI TRỊ NGÀN NĂM · #01"; chốt 05/11/2026, từ tập 1 "Chín quận")
Chủ kênh đã duyệt hướng này sau khi bỏ các kiểu: bản đồ 16:9, tranh hoạt hình nhân vật 2D, tranh phẳng minh họa, mô hình 3D. Lý do bỏ: nhân vật vẽ bằng mã trông như trẻ con, không có biểu cảm; thẻ banner che bản đồ.
- **Bản đồ phủ kín cả khung 1080×1920**, giống video mẫu `demo_chia_quan_huyen`: năm lớn góc trái, nguồn nhỏ dưới năm, logo góc phải, la bàn, khung vàng hai lớp, thanh tiến trình, hộp phụ đề ở khoảng y 1290–1500.
- **Mọi mô phỏng vẽ thẳng lên bản đồ, KHÔNG dùng thẻ/banner.** Dùng: chấm thành, quân cờ (pawn) cho người, bao thóc cho thuế, đường nét đứt cho đường đi, vòng sáng lan cho cảm xúc, nhãn chữ có viền ngay cạnh vật. Màu vùng đổi đỏ → xanh để chỉ dân khổ → yên.
- **Bản đồ nền:** `phim_ban_do/doc9x16/map_pretty.jpg` (từ `world7`, đã chỉnh màu: đất vàng nâu, biển xanh đậm có viền nước nông). Không vẽ biên giới, không ghi Biển Đông (đúng quy tắc bản đồ chung). Vị trí các quận chỉ là minh họa nếu sử không nêu; chỉ gắn tên quận mà nguồn chính có nêu, còn lại ghi rõ "minh họa" trong kịch bản.
- **Kinh đô không đặt tọa độ**: mũi tên đi ra mép trên bản đồ, nhãn "rất xa, phía bắc".
- **Phụ đề cụm ngắn:** tối đa khoảng 8 chữ, hai dòng, cỡ 56, chữ sáng dần theo lời đọc (chủ kênh chê phụ đề dài ngày 05/11). Chia ở dấu câu, thời gian chia theo số chữ trong thời lượng giọng thật của từng đoạn.
- **Chữ không che chữ:** vật mang số liệu (bao thóc) đặt LỆCH khỏi nhãn tên chỗ (chủ kênh phát hiện bao thóc che chữ "Giao Chỉ", "Cửu Chân" ngày 05/11). Xem khung hình thật ở cỡ lớn ở đầu, giữa, lúc nhiều vật nhất và câu cuối trước khi giao.
- **Mỗi cảnh chỉ hiện đồ họa của cảnh đó** (trang dựng tự ẩn phần tử của cảnh khác); tiêu đề cảnh không chồng nhau.
- **Mã nguồn:** trang dựng `phim_ban_do/doc9x16/trang.html` (hàm `render(t)`), chạy `python phim_ban_do/dung_9x16.py <tên> <thư mục giọng chuẩn hóa> <ra.mp4>` (chụp khung bằng Chromium, ghép ffmpeg, mốc theo `thoi_luong.json` của giọng thật). Ảnh bìa: `python assets/bia/HAN1/tao_bia.py`. Tập mới: sao chép `trang.html`, đổi phần cảnh (khối `scene(...)`), tọa độ và nhãn.
- **Quy trình một tập:** kịch bản (`kiem_kich_ban` 0 ❌) → giọng Orus từng đoạn (`cum.txt` = 1, `giong.txt` = Orus; trigger `chay.txt`) → chuẩn hóa (`chuan_hoa_giong.py <tên> --nguon assets/thu_giong_hai/orus`) → nhận dạng (`asr.txt`) → `kiem_giong.py` đạt hết → dựng → xem khung → gửi Telegram kèm tiêu đề, hashtag, ảnh bìa.
- **Độ dài:** video dọc 60–80 giây theo quy định chung; tập 1 hiện dài hơn (khoảng 100 giây) vì kịch bản đầy đủ ý theo yêu cầu chủ kênh ngày 05/11; chủ kênh đã đồng ý ("đầy đủ ý, 180–260 chữ chỉ là ví dụ").
- **Nhánh làm việc:** `claude/cach-ho-cai-tri-tap-1` (workflow giọng và nhận dạng đã được thêm nhánh này vào `on.push.branches`).
