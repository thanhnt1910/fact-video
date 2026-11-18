# Quy trình giọng Puck, cân và chuẩn hóa giọng

> Đã bị mục 'dùng nguyên giọng gốc' (06/11) thay thế; giữ để tra. Nguồn: `archive/CLAUDE-truoc-tai-cau-truc-18-11.md`. Chuyển ngày 18/11/2026.

## Quy trình giọng đọc: kiểm TRƯỚC khi dựng (chủ kênh yêu cầu 23/10/2026, từ bản Hai Bà Trưng bị 30 lỗi giọng và dựng lại hai lần)

Thứ tự bắt buộc, không đảo: **đọc từng đoạn → nhận dạng → `kiem_giong.py` → (đọc lại) → mới dựng.** Không dựng video (45 phút mỗi lần) khi chưa kiểm giọng.
- **Dải số đoạn mỗi video (thư mục giọng `assets/thu_giong_hai/puck/` dùng chung, trùng số là ghi đè):** Hai Bà Trưng 9001–9144; Đinh Bộ Lĩnh 10001–10091. Video mới lấy dải kế tiếp, không dùng lại số cũ.
- **Đọc cụm 8 đoạn ngắn rồi cắt, `cum.txt` = `8` (chủ kênh chốt 24/10/2026, thay quy tắc `cum=1` ngày 23/10).** Lý do: Gemini giới hạn số lượt gọi mỗi khóa (khoảng 4 lượt mỗi khóa rồi báo 429 và không hồi lại trong cả 15 phút), mà đọc từng đoạn cần 119 lượt cho 119 đoạn nên hết hạn mức sau 20 đoạn. Cụm 8 đoạn chỉ cần khoảng 15 lượt. Để cắt không lệch chữ thì mỗi đoạn phải ngắn (xem dưới), và vẫn phải nhận dạng + `kiem_giong.py` trước khi dựng; đoạn nào lỗi thì đọc lại riêng (đặt `cum=1` cho lượt đọc lại đó).
- **Trước khi đọc giọng luôn chạy `python phim_ban_do/kiem_kich_ban.py <tên>`** (0 ❌): đoạn tối đa 32 chữ (nên 20–30), tối đa 2 câu, (ngoặc, ngoặc kép, gạch, hai chấm, chữ số: đã bỏ chặn 05/11/2026), không nói tắt, họ tên đủ, không mệnh đề chen giữa chủ ngữ và vị ngữ. Kịch bản viết cho giọng đọc ngay từ đầu, không sửa sau khi đã đọc.
- **Giữ hạn mức Gemini:** mỗi lần chạy giọng chỉ đọc đoạn còn thiếu, không xóa giọng đã đọc tốt. Tối thiểu 10 khóa trong `GEMINI_API_KEY` … `GEMINI_API_KEY_10`, từ các dự án Google khác nhau. Đầu log in bảng "tên secret → đuôi khóa" và chi tiết lỗi 429 (theo phút hay theo ngày). Khóa báo 401 (tài khoản dịch vụ bị xóa) thì mã tự bỏ qua; phải thay khóa đó. Nếu mọi khóa hết lượt thì dừng, báo chủ kênh, không đợi hơn 15 phút.
- **Đoạn lời ngắn:** mỗi đoạn khoảng 20–30 chữ, một hoặc hai câu. Đoạn dài 45–56 chữ hay bị Gemini bỏ câu đầu hoặc đọc lệch.
- **Nhận dạng chạy SAU khi giọng đã chốt** (workflow `phude-asr.yml`, không chạy song song với dựng). `phude_asr.py` đã nhớ mã nội dung file giọng: giọng đổi thì đoạn đó tự nhận dạng lại. Nếu thấy báo cáo "nhận dạng CŨ", xóa đoạn đó trong `asr_<tên>.json`.
- **Kiểm từng đoạn:** `python phim_ban_do/kiem_giong.py <tên> [--nguong 0.9] [--xoa]`. Đoạn nào khớp dưới 90% hoặc chưa có nhận dạng thì in ra; với `--xoa` thì xóa đoạn đó (giọng, hash, nhận dạng) để đẩy `chay.txt` đọc lại. Lặp đến khi sạch.
- **Đọc lại tối đa 3 lần mỗi đoạn.** Nếu vẫn bị bỏ câu hoặc đọc sai (đã gặp: "Vậy là nước Nam Việt, tồn tại gần một trăm năm, đã mất." bị đọc thành "ổn ạ"), đổi chữ nhẹ ở câu đó trong cả `<tên>_full.json` và file kịch bản `.md`, rồi đọc lại.
- Sau khi `kiem_giong.py` sạch mới tính phụ đề (`phude_tinh.py`), xem khung hình mẫu ở cỡ lớn, dựng, rồi chạy `kiem_video.py`. Có ❌ thì không giao.
- Dựng nên chia 16 đoạn song song nếu cần nhanh; chỉ đổi vài đoạn giọng thì cân nhắc chỉ dựng lại đoạn bị ảnh hưởng.
- Chi tiết dân gian (ví dụ voi chiến của Hai Bà Trưng) không có trong sử cũ chỉ được vẽ kèm ghi chú trên màn hình "theo truyền thuyết dân gian"; không đưa vào lời kể như sự kiện chắc chắn.

## Giọng đọc đồng đều trong một video (chủ kênh yêu cầu 24/10/2026, áp dụng mọi video từ nay)
Mỗi lượt gọi Gemini tạo giọng độc lập, nên nhịp nói và âm lượng khác nhau giữa các lượt (đo ở Ngô Quyền: đoạn đọc riêng nhanh hơn khoảng 8% và to hơn khoảng 0,9 dB so với đoạn đọc trong cụm 8). Người nghe thấy chỗ nối giữa hai kiểu đọc như "đổi người".
- **Đọc cả video theo một cách:** cùng một `cum.txt`, cùng một mô hình, cùng một đợt nếu còn đủ hạn mức. Chỉ đọc lại riêng (`cum=1`) những đoạn lỗi. Không để phần đầu video đọc kiểu khác phần sau.
- **Chuẩn hóa ở bước âm thanh, không tốn hạn mức Gemini, không đọc lại:** làm trên bản sao của từng đoạn (giữ nguyên mp3 gốc), trước `audio2.py` và trước khi tính `phude_tinh.py`.
  1. Âm lượng: `ffmpeg -i <đoạn> -af loudnorm=I=-16:TP=-1.5:LRA=11` cho từng đoạn, cùng một mức cho cả video.
  2. Tốc độ: tính số chữ trên giây của từng đoạn (số chữ lời đọc chia thời lượng); lấy trung vị của các đoạn đọc trong cụm làm chuẩn. Đoạn nào lệch quá 5% thì chỉnh bằng `atempo` (chỉ trong khoảng 0,90 đến 1,10, giữ nguyên cao độ), không chỉnh cắt chữ.
  3. Sau khi chỉnh tốc độ phải cập nhật `thoi_luong.json` (thời lượng mới) rồi mới tính phụ đề và dựng; nhận dạng giọng chạy trên bản đã chuẩn hóa.
- **Kiểm trước khi dựng:** in bảng theo nhóm đoạn (đọc riêng, đọc cụm, đọc lại): từ/giây trung bình và âm lượng trung bình; chênh giữa các nhóm phải dưới 5% tốc độ và dưới 0,5 dB. Không tự ý đổi giọng hoặc mô hình giữa chừng.
- Video Ngô Quyền đã giao (12 phút 57 giây) chưa áp dụng bước này; chỉ áp dụng cho video sau.

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

## Cân giọng đồng đều theo ÂM SẮC, máy tự phát hiện đoạn lệch (chủ kênh yêu cầu 05/11/2026, từ video Chu Du, áp dụng mọi video từ nay)
Chủ kênh KHÔNG phải nghe từng câu để liệt kê đoạn lệch: máy tự đo, tự chọn, tự báo đoạn cần đọc lại.
- **Giọng mốc do chủ kênh chọn** (ví dụ Chu Du: câu 9012–9015, khoảng 147 Hz, 3,9 chữ/giây). Mọi câu so với mốc này.
- **KHÔNG kéo cao độ bằng `asetrate`:** nó dịch vùng cộng hưởng nên nghe thành người khác (đo ở Chu Du: câu 9008 xa mốc 0,9 lên 1,57 sau khi kéo cao độ; không ép cả cao độ lẫn nhịp qua nhiều lượt). Dùng `rubberband` có `formant=preserved`.
- **Công cụ:** `python phim_ban_do/can_giong_am_sac.py <tên> --goc <mp3 gốc> --kich-ban <json> --moc <các câu mốc> --ra assets/thu_giong_hai/<tên>_chuan`. Mỗi câu thử 3 bản (không đổi cao độ / kéo hết / kéo nửa), chuẩn nhịp 0,90–1,10 và loudnorm −16, so phổ 40 dải mel với mốc, chọn bản gần mốc nhất. Thay cho `chuan_hoa_giong.py` ở các video mới.
- **Đoạn vẫn xa mốc** (điểm lệch > trung vị + 4 MAD, công cụ in "ĐỌC LẠI" và ghi `can_doc_lai.json`) thì đọc lại, KHÔNG cố chỉnh thêm; mỗi đoạn đọc lại tối đa 3 lượt, giữ bản gần mốc nhất.
- **Đoạn mốc nằm trong cùng một prompt với mọi câu.** Nhật ký giọng cho thấy cả video đọc từng câu, cùng mô hình, cùng giọng, cùng hồ sơ phong cách. Khác biệt đến từ lấy mẫu ngẫu nhiên của Gemini (không đặt temperature/seed), nên đọc lại chỉ là bốc thăm lại: dùng chọn bản tốt nhất, không trông chờ đổi prompt.
- Không dựng video (45 phút) khi bước này chưa chạy và danh sách "ĐỌC LẠI" chưa xử lý. Báo chủ kênh danh sách đoạn lệch kèm số đo, không hỏi chủ kênh nghe thử.
- Cái này bổ sung cho mục "Giọng đọc đồng đều trong một video" ở trên (cân âm lượng, tốc độ); hai bước dùng chung và bước này thay phần chỉnh cao độ.

## Kiểm cắt giọng: chữ dính cuối và chữ đầu lệch (rút từ #07, 07/11/2026)
- Cụm đọc cắt lệch có thể làm câu cuối đoạn này tràn sang đầu đoạn sau mà `kiem_giong.py` vẫn báo đạt (nhận dạng có gợi ý bịa chữ cuối). Trước khi dựng, với mỗi đoạn kiểm: (1) có từ 2 chữ trở lên cuối đoạn trùng một mốc thời gian sát hết file (chữ dính cuối = nhận dạng bịa, giọng bị cụt); (2) chữ đầu tiên bắt đầu sau 1 giây (đoạn có lời thừa ở đầu). Có thì cắt lại ranh giới (nối phần tràn về đoạn trước, cắt ở chỗ lặng), cập nhật `thoi_luong.json`, xóa nhận dạng hai đoạn đó rồi chạy lại.
- Tiếng boom/hiệu ứng nhấn đi đường riêng, không qua sidechain hạ theo giọng (`dung_9x16.py` tự làm khi có sự kiện `boom`), nếu không sẽ gần như không nghe thấy.
