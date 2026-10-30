# Series lịch sử Việt Nam (Tây Sơn, Nguyên Mông, Đinh Bộ Lĩnh, Lê Hoàn, Lý Công Uẩn...)

Quy tắc nội dung và giọng hài cho sử Việt, kèm cách làm bản mẫu Đinh Bộ Lĩnh. Làm theo dạng bản đồ nên đọc thêm `video-ban-do.md` và `chung.md`. Hán Sở tranh hùng (tập 1) đang dừng, ghi chú ở mục đầu.

## Series lịch sử Việt Nam (Tây Sơn, Nguyên Mông...): quy tắc nội dung và giọng hài (chủ kênh chốt 23/10/2026, áp dụng mọi video sử Việt)

- **Hán Sở tranh hùng tập 1 đã DỪNG (23/10/2026)**, chuyển sang chủ đề Tây Sơn. Kịch bản, nội dung bản đồ và giọng đã đọc (7001–7058) giữ nguyên trong repo, không làm tiếp trừ khi chủ kênh yêu cầu.
- **Giọng hài chỉ nhắm vào tình huống và quân xâm lược** (tướng giặc chủ quan, lương thảo trục trặc, thua chạy...). **Không đùa cợt các anh hùng dân tộc** (Trần Hưng Đạo, Quang Trung – Nguyễn Huệ, Lê Lợi, Nguyễn Trãi, Ngô Quyền, Lý Thường Kiệt...): lời kể về họ nghiêm túc, trân trọng; khung đùa (`JOKES`), ghi chú, phụ đề không có câu giễu cợt, biệt danh hay so sánh bông đùa về họ. Khán giả Việt rất nhạy chuyện này, bình luận tiêu cực kéo cả video xuống. Khung đùa vẫn tối đa hai khung mỗi chương và chỉ rơi vào tình huống hoặc phía quân xâm lược.
- **Giới hạn thời gian: dừng trước năm 1858.** Không viết lịch sử cận đại và hiện đại (nhạy cảm chính trị, dễ bị báo cáo vi phạm). Không nói về pháp luật đương thời hay so sánh với thời nay.
- **Nguồn chính: Đại Việt sử ký toàn thư và Khâm định Việt sử thông giám cương mục** (lưu ý: Toàn thư chỉ chép đến 1675, không có thời Tây Sơn; thời Tây Sơn dựa Khâm định Việt sử, đối chiếu Đại Nam thực lục, Lê quý kỷ sự; Hoàng Lê nhất thống chí chỉ là nguồn phụ, xem `ke-hoach/tay-son-dan-y.md`). Ghi rõ nguồn trong phần mô tả video và bình luận, giống series "Tam Quốc theo chính sử". Chi tiết chỉ có ở tiểu thuyết, truyền thuyết hay sử liệu nước ngoài thì ghi rõ là lời kể hoặc còn tranh cãi, hoặc bỏ khỏi lời kể. Số quân, ngày tháng phải đối chiếu nguồn trước khi đọc giọng.
- Giữ quy tắc chung đã có: không bịa lời thoại, nội tâm; tên nhân vật ghi đủ; năm viết bằng chữ; từ cổ khó hiểu giải thích ngay; vẫn không phạm luật Việt Nam.

## Giọng đọc hào hùng và cách làm bản Đinh Bộ Lĩnh (chủ kênh duyệt giọng "khá ổn" 24/10/2026, dùng làm mẫu cho mọi video sử Việt)
- **Phong cách giọng:** Gemini giọng Puck, kiểu `STYLE_KE` + `TONE_KE` trong `thu_giong_hai.py`: sáng, vang, nhiều năng lượng, tốc độ vừa nhanh, có lên xuống theo ngữ cảnh. KHÔNG trầm, không buồn ngủ, không thì thầm, không giọng đều đều (chủ kênh chê giọng quá trầm, không hào hùng ngày 24/10). Video sử Việt dùng tone `story` ở mọi đoạn; cụm gồm các đoạn kề nhau, mỗi câu một nhịp có ngắt ngắn.
- **Đọc:** `cum.txt` = 16 (số đoạn mỗi lần gọi, ít lượt Gemini), file kịch bản trong `file.txt`, đẩy `chay.txt`. Chỉ đọc đoạn còn thiếu; muốn đọc lại cả video thì xóa các số đoạn của video đó khỏi `puck/thoi_luong.json`, `puck/hash.json` và các `puck/<số>.mp3`. Đoạn lỗi đọc lại riêng với `cum.txt` = `1` (dùng `kiem_giong.py --xoa`).
- **Cắt và chuẩn hóa (làm trên bản sao, không tốn hạn mức Gemini):**
  1. Ghép từng 16 đoạn thành một cụm, chạy nhận dạng `asr.txt` ("<tên>c medium 1"), rồi `python phim_ban_do/cat_lai_cum.py` cắt lại theo mốc chữ (thay cho cắt theo chỗ lặng, hay lệch).
  2. Chuẩn hóa từng đoạn: `atempo` về tốc độ trung vị (chỉ khi lệch quá 5%, giới hạn 0,90–1,10), `loudnorm=I=-16:TP=-1.5:LRA=11`, chỉnh độ lợi về đúng -16 LUFS, `alimiter=0.89`; ghi `thoi_luong.json` mới vào `<tên>_chuan/`. Kết quả Đinh Bộ Lĩnh: âm lượng -15,3 đến -15,6 LUFS.
  3. Nhận dạng từng đoạn (`asr.txt` "<tên> medium 1") rồi `kiem_giong.py <tên>`; phải đạt 100% đoạn trên 90% rồi mới tính `phude_tinh.py` và dựng. Lần này 3 đoạn lỗi (cắt lệch, bị bỏ chữ) và đọc lại một lượt là sạch.
- **Tắt tiếng nhiễu:** nội dung bản đồ đặt `QUIET_AUDIO=True` (bỏ tiếng gió, xẹt, bước chân, đám đông). Chỉ giữ nhạc nền và vài hiệu ứng rõ nghĩa (trống, kèn). Chủ kênh từng phàn nàn "nhiều tiếng xẹt xẹt".
- **Sửa kịch bản sau khi đã có nội dung bản đồ:** giữ nguyên số đoạn `n` còn lại; đoạn bỏ thì để trống số, và `R()`, `E()`, `at()` trong file nội dung tự lấy đoạn kề (đã làm trong `dbl1_content.py`). Mọi tham chiếu số đoạn trong nội dung phải kiểm lại sau khi bỏ đoạn.
- **Quy tắc kịch bản rút từ bản Đinh Bộ Lĩnh sửa theo bố cục cuốn hút:** mở đầu 4 đoạn (khoảng 35 giây), nguồn sử chuyển vào mấy chữ đầu chương sau ("Theo Đại Việt sử ký toàn thư, ..."), chương nền gộp tên riêng (bỏ tước hiệu phụ, lời chê của sử gia ở chương dẫn nhập), ghi chú "sách chép khác nhau" gộp vào một đoạn có lời kể. Mẫu: `ke-hoach/dinh-bo-linh-kich-ban.md` (86 đoạn, 2.129 chữ, dựng thực tế 11 phút 14 giây, tốc độ đọc khoảng 3,3 chữ/giây nên 2.100 chữ vẫn đủ sàn 10 phút).
- **Kiểm sau dựng:** `kiem_video.py` phải 0 ❌. Cảnh báo "cảnh gắn vào câu lệch" thì dời cảnh về đúng câu đang đọc ở lượt chỉnh kế tiếp.

## Lời kể sử Việt: không lời bình của sử gia, kể liền mạch như một câu chuyện (chủ kênh yêu cầu 27/10/2026)
- **Bỏ hết lời bình, lời chê khen của sử gia** (Lê Văn Hưu, Ngô Sĩ Liên, đoạn đánh giá cuối truyện của Toàn thư...) khỏi lời kể. Video kể lịch sử, không phân tích lời bình. Sử gia chỉ xuất hiện khi chính họ là một nhân vật của sự kiện.
- **Áp dụng cả cho bài đăng Facebook sử Việt** (chủ kênh yêu cầu 30/10/2026): bài chỉ kể cốt truyện, không có mục "Sử gia nói gì?", không lời bàn của sử gia, không lời khen chê của người viết. Chi tiết: `ke-hoach/nhan-vat-phu-series-dan-y.md`.
- **Không dịch sát từng câu sử.** Mỗi đoạn lời không là một ý rời; các câu phải nối nhau bằng quan hệ nguyên nhân – kết quả hoặc đối lập ("vì thế", "nhưng", "thấy vậy"), có hình ảnh dẫn xuyên suốt (ví dụ cánh cửa, câu hỏi cuối chiếu). Đọc nối các đoạn liền nhau phải thấy một mạch văn, không thấy danh sách.
- **Sáng tạo ở cách kể** (xem mục "Sáng tạo cho đỡ nhàm" trong `chung.md`): câu mở đầu ai nghe cũng hiểu (ai, chuyện gì), thân bài đúng thứ tự thời gian, báo trước và quay lại hình ảnh mở đầu ở cuối.

