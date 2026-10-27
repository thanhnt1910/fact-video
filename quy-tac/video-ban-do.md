# Dạng video bản đồ động (Hán Sở, sử Việt, lịch sử thế giới)

Quy tắc kỹ thuật và bố cục của dạng video bản đồ (`phim_ban_do/`): chữ trong khung, bố cục, kiểm video, quy trình giọng đọc Gemini, mặt nhân vật, tiếng nền. Dùng cho mọi series làm theo dạng bản đồ. Cũng đọc `chung.md` và file của series tương ứng.

## Video bản đồ: mọi chữ trên màn hình phải nằm gọn trong khung (chủ kênh yêu cầu 20/10/2026, áp dụng mọi tập)

- Không chữ nào được dài quá khung 1920×1080: thẻ hài, tiêu đề, thẻ nhân vật, thẻ câu nói, nhãn, phụ đề đều phải tự xuống dòng hoặc thu nhỏ chữ khi quá rộng (chừa lề tối thiểu 60 px mỗi bên). Hàm vẽ chữ mới phải có sẵn bước đo độ rộng (`textlength`) và xuống dòng; không vẽ một dòng dài cố định.
- Trước khi dựng bản đầy đủ: chạy kiểm độ rộng cho mọi lớp chữ của nội dung (hộp bao `getchannel('A').getbbox()` phải nằm trong 60–1860 px) và xem ít nhất một khung của câu dài nhất mỗi loại.
- Khi sửa phụ đề: dùng `phude_tinh.py` (mốc theo đoạn có tiếng), không đặt mốc cố định.

## Video bản đồ: bố cục gọn mắt, không che nhau (chủ kênh chốt 22/10/2026, từ demo Hán Sở Hồng Môn yến, áp dụng mọi tập)

- **Không dùng khung trích lời (`QUOTES`) ở dưới màn hình:** nó đè lên phụ đề, mà phụ đề đã hiện đúng câu ấy. Lời nhân vật chỉ nằm trong phụ đề.
- **Khung đùa (`JOKES`) chỉ khoảng hai khung mỗi chương, mỗi khung hiện tối đa 3 giây** (`J(n,icon,text,off,dur=3.0)`). Không đặt khung đùa lên câu vốn đã là câu đùa, và không lặp nguyên văn câu đang đọc.
- **Không đặt thẻ tiêu đề hay thẻ kết lên lúc đang đọc câu cuối:** thẻ chữ lớn che bản đồ. Thẻ mở đầu chỉ ở giây đầu; kết video bằng mờ dần, không thêm thẻ "HẾT".
- **Nhãn và quân không đè lên tên thành:** dùng `soff` (dịch cả quân lẫn nhãn theo điểm ảnh) để đặt cụm quân lệch khỏi biểu tượng thành và nhãn tên thành; quân đứng yên dùng `spread` nhỏ (0,45–0,6); nhóm hai bên đóng gần nhau không để chồng lên nhau. Quân chạy về nơi có quân đứng yên thì dùng cùng `soff` để nhập vào đúng chỗ.
- **Ít banner chữ, nhất là lúc đánh nhau (chủ kênh yêu cầu 22/10/2026):** banner chữ che cảnh đánh nhau làm rối mắt. Ghi chú nổi (`NT`) tối đa khoảng 4 cái mỗi chương, mỗi cái hiện tối đa 3,5 giây, chỉ giữ ý quan trọng (mốc, con số, bước ngoặt); bỏ ghi chú nhắc lại điều phụ đề đã nói. Thẻ số (`NU`) chỉ ở mốc lớn (mở đầu, đổi năm quan trọng). Khung đùa vẫn tối đa hai khung mỗi chương. **Cảnh đánh nhau, giao tranh, vây thành thì khai báo `Q(câu đầu, câu cuối)` trong file nội dung:** bộ dựng tự ẩn ghi chú nổi, khung đùa và thẻ số trong các khoảng đó (và trong mọi khoảng `BATT`); chỉ còn phụ đề và nhãn quân.
- **Mỗi lúc chỉ một lớp chữ lớn:** thẻ nhân vật, ghi chú, khung đùa và thẻ số không hiện cùng lúc ở cùng vùng (giữ các thời điểm không chồng nhau, `dur` ngắn, bị cắt ở `E(n,-0.1)`).
- **Luôn xem khung hình thật ở cỡ lớn** (`python3 mapfilm3.py still <giây>...`) ở đầu, giữa, lúc nhiều quân nhất và câu cuối trước khi đẩy lệnh dựng; bản thu nhỏ không đủ.
- **Giọng đọc cụm nhiều câu hay cắt lệch** (chữ cuối câu này lẫn sang đầu câu sau). Nếu `kiem_video.py` báo ❌ "thừa/mất chữ" ở nhiều câu liền nhau thì đọc lại từng câu: xóa các câu ấy khỏi `thoi_luong.json` và mp3, đặt `ke-hoach/thu-giong-hai/cum.txt` là `1`, đẩy `chay.txt`, rồi chạy lại nhận dạng giọng (`asr.txt`) và `phude_tinh.py`.
- **Mẫu:** `phim_ban_do/hs1_content.py` (demo Hồng Môn yến, kiểm 0 lỗi).

## Kiểm video trước khi giao (công cụ `phim_ban_do/kiem_video.py`, chủ kênh yêu cầu 21/10/2026)

- Sau khi chốt giọng và dựng, chạy: `python phim_ban_do/kiem_video.py <tên> --tts <các file tts> --video <mp4>` (cần `asr_<tên>_final.json` mới, chạy `phude-asr.yml` SAU khi file giọng đã chốt; công cụ báo "nhận dạng CŨ" nếu lệch với file giọng).
- Công cụ kiểm: chữ thừa/mất/lặp ở đầu và cuối mỗi câu, năm đọc sai, từ hay sai (kỵ), phụ đề trễ/sớm/trống, ô năm góc trái so với lời kể, cảnh gắn vào câu quá dài, giọng trong video lệch khỏi cảnh, im lặng dài, hình đen/đứng, độ dài. Báo cáo: `logs/kiem_video/<tên>.md`. Có ❌ thì không giao video.

### Không để giọng đọc lặp câu (chủ kênh yêu cầu 22/10/2026, từ demo Hồng Môn yến bị lặp câu 6009 và 6023)

- Lỗi hay gặp: giọng đọc cụm nhiều câu một lần rồi cắt, nên **đuôi câu trước bị đọc lại ở đầu câu sau** (6009 mở đầu bằng "Hạng Vũ nghe theo" của câu 6008) hoặc **đầu câu sau lẫn vào cuối câu này** (6023). Người nghe thấy một câu bị nhắc hai lần.
- `kiem_video.py` kiểm các dạng lặp sau, tất cả là ❌ (không giao video): thừa chữ ở đầu hoặc cuối câu (tính theo khối khớp đầu/cuối, không bỏ sót khi chữ thừa dính chữ lệch); đầu câu đọc lại 3–6 chữ cuối câu trước; cuối câu đọc lẫn 3–6 chữ đầu câu sau; một vế của câu bị đọc từ hai lần; giọng nhiều hơn kịch bản từ 4 chữ; lặp cụm 2–3 chữ liền nhau.
- **Báo cáo 0 lỗi chưa đủ:** sau khi dựng, mở `logs/kiem_video/<tên>.md` và nghe lại ít nhất chỗ nối giữa các câu đã sửa; câu nào ASR dài hơn kịch bản thì nghe lại.
- Cách sửa giống mục bố cục: xóa các câu lỗi khỏi `thoi_luong.json` và mp3, `cum.txt` = `1`, đẩy `chay.txt` (chỉ khi chủ kênh cho chạy), chạy lại nhận dạng và `phude_tinh.py`, rồi kiểm lại đến khi sạch. Chỉ sửa giọng thì phải dựng lại video.

## Quy trình giọng đọc: kiểm TRƯỚC khi dựng (chủ kênh yêu cầu 23/10/2026, từ bản Hai Bà Trưng bị 30 lỗi giọng và dựng lại hai lần)

Thứ tự bắt buộc, không đảo: **đọc từng đoạn → nhận dạng → `kiem_giong.py` → (đọc lại) → mới dựng.** Không dựng video (45 phút mỗi lần) khi chưa kiểm giọng.
- **Dải số đoạn mỗi video (thư mục giọng `assets/thu_giong_hai/puck/` dùng chung, trùng số là ghi đè):** Hai Bà Trưng 9001–9144; Đinh Bộ Lĩnh 10001–10091. Video mới lấy dải kế tiếp, không dùng lại số cũ.
- **Đọc cụm 8 đoạn ngắn rồi cắt, `cum.txt` = `8` (chủ kênh chốt 24/10/2026, thay quy tắc `cum=1` ngày 23/10).** Lý do: Gemini giới hạn số lượt gọi mỗi khóa (khoảng 4 lượt mỗi khóa rồi báo 429 và không hồi lại trong cả 15 phút), mà đọc từng đoạn cần 119 lượt cho 119 đoạn nên hết hạn mức sau 20 đoạn. Cụm 8 đoạn chỉ cần khoảng 15 lượt. Để cắt không lệch chữ thì mỗi đoạn phải ngắn (xem dưới), và vẫn phải nhận dạng + `kiem_giong.py` trước khi dựng; đoạn nào lỗi thì đọc lại riêng (đặt `cum=1` cho lượt đọc lại đó).
- **Trước khi đọc giọng luôn chạy `python phim_ban_do/kiem_kich_ban.py <tên>`** (0 ❌): đoạn tối đa 32 chữ (nên 20–30), tối đa 2 câu, không ngoặc/ngoặc kép/gạch/hai chấm/chữ số, không nói tắt, họ tên đủ, không mệnh đề chen giữa chủ ngữ và vị ngữ. Kịch bản viết cho giọng đọc ngay từ đầu, không sửa sau khi đã đọc.
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


## Gemini trả 429 thì dừng, không gửi dồn (chủ kênh yêu cầu 25/10/2026)
- Khóa báo 429 (hết lượt) thì KHÔNG gửi thêm yêu cầu để thử lại liên tục: gửi nhiều có thể làm khóa bị khóa. `gemini_tts.py` đếm mọi lần 429 trong một lần chạy; đủ 8 lần (`GEMINI_MAX_429`) thì dừng hẳn (thoát mã 3), phần đã đọc vẫn được lưu. `max_wait.txt` = 30 giây.
- Gặp 429 theo ngày ("retry in" hàng giờ) thì đợi sang ngày, không chạy lại trong ngày. Chỉ chạy lại khi chủ kênh báo đã thêm khóa mới hoặc hạn mức đã có lại.

## Video bản đồ: mặt nhân vật hiện trên bản đồ khi được nhắc tên (chủ kênh yêu cầu 25/10/2026, áp dụng mọi video có nhân vật)
- Khi lời kể nhắc tên một nhân vật có nơi ở hoặc nơi hoạt động trên bản đồ, hiện một huy hiệu tròn có khuôn mặt tại đúng nơi ấy, kèm tên phía trên, vòng sóng lan ra ở địa điểm và hơi nảy lên khi xuất hiện (mỗi lần 2–3 giây, tắt dần). Hàm vẽ `face_sprite(kind, col)` trong `phim_ban_do/mapdraw.py`; vẽ trong `mapfilm3.py` (danh sách `FACES`); khai báo trong file nội dung bằng `FACE(n, o, dur, tên, nơi, kiểu, màu)`.
- **Kiểu mặt theo vai trò:** `king` (mũ miện, râu, tua ngọc, có tia sáng vàng khi lên ngôi), `general` (mũ giáp lông đỏ), `lord` (mũ màu phe, dùng cho sứ quân), `noble` (mũ cánh chuồn, quan lớn), `youth` / `prince` (thanh niên búi tóc, đai màu phe hoặc đai vàng), `child` (hai búi tóc, má hồng), `servant` (mũ xám). Màu viền theo phe, đúng màu cờ trong chú giải. Thêm kiểu mới thì thêm nhánh trong `face_sprite` rồi xem bảng mẫu ở cỡ lớn trước khi dùng.
- **Cách khai báo gọn:** đã có `C3(...)` (thẻ tên và chức) cho nhân vật nào thì ghi vào từ điển `FACEMAP` (tên → nơi, kiểu); `C3` tự gọi `FACE` đúng lúc. Nhân vật cần mặt mà chưa có thẻ thì gọi `FACE(...)` trực tiếp. Nhân vật đổi vai (Đinh Liễn: thanh niên rồi vương) thì đổi kiểu theo số câu ngay trong `C3`.
- **Chỉ đặt mặt khi nơi ấy đã hiện trên bản đồ:** sứ quân gắn với thành thì mặt chỉ hiện từ lúc thành được hiện (`t_min`), không để mặt chỉ vào chỗ trống. Mặt không đè nhãn tên thành (đặt phía trên, tự đẩy cao theo cỡ mặt).
- **Cỡ:** bán kính tối thiểu 44 px (theo khung 2×) để đọc được trên điện thoại.
- **Không đặt mặt** cho sử gia (không có nơi trên bản đồ) hoặc nhân vật chưa có tọa độ; không vẽ mặt thật của người thật (đây là hình vẽ phẳng theo vai trò, không giống ai).
- Xem vài khung thật ở cỡ lớn (`python3 mapfilm3.py still <giây>`) ở lúc mặt đang hiện, trước khi đẩy lệnh dựng.
- Mẫu: `phim_ban_do/dbl1_content.py` (24 lần hiện mặt, bản Đinh Bộ Lĩnh).

## Video bản đồ: tiếng nền và hiệu ứng âm thanh (chủ kênh yêu cầu 25/10/2026)
- **Nhạc nền không được có tiếng phập phồng.** Lớp nền (`_pad` trong `audio2.py`) mặc định gồm hai âm lệch nhau 1,4 Hz, nên nghe thành "weo weo"; ở đoạn yên tĩnh (vạc dầu, hổ trong cũi) phải dùng tâm trạng `'vac'` (nền không lệch âm). Gặp đoạn nào nghe phập phồng thì tách đoạn ấy thành một khoảng `MUSIC` riêng với `'vac'`.
- **Mọi nhóm quân hay đoàn người đi lại có nghĩa trong truyện phải có tiếng** (vó ngựa, bước chân, lục lạc). Trong chế độ giảm ồn (`QUIET_AUDIO=True`) nhóm không nhãn (`label=False`) bị tắt tiếng mặc định; nhóm cần tiếng thì thêm tên vào `SFX_GROUPS` trong file nội dung (đoàn sứ đi và về nhà Tống: vó ngựa `clop`, lục lạc `bells`).
- Mốc quan trọng thêm tiếng riêng bằng `SFX=[(giây, 'horn'|'gong'|'trumpet')]` (xuất phát: tù và; đến nơi: kèn đồng; lễ tiếp nhận hoặc về đến nơi: chiêng).
- Tiếng đi lại phải đo được trong bản âm thanh tổng hợp, không tin vào việc "đã thêm lệnh": chạy `audio2.py` không giọng, so với bản cũ ở đúng khoảng giây của cảnh.

## Cao độ giọng đồng đều: toàn tone story, một kiểu đọc, kiểm cao độ trước khi dựng (chủ kênh báo 27/10/2026, từ Lê Hoàn)
Video Lê Hoàn có hai cụm đọc bị trôi trầm đột ngột (đoạn 17041–17048 thấp hơn mức chung khoảng 9%, đoạn 17089–17096 thấp hơn khoảng 16%). Âm lượng và tốc độ đã chuẩn hóa nên chỗ lệch còn lại là cao độ.
- **Nguyên nhân (đo trên các file đã chuẩn hóa):** mỗi lượt gọi Gemini tự quyết cao độ, câu chỉ dẫn không giữ được. Chỉ dẫn `tense` ghi "low" nhưng cụm `tense` của Lê Hoàn lại cao (166–171 Hz), còn ba cụm `story` bị trầm (130–141 Hz). Lê Hoàn trộn `story`/`tense`/`reflect` nên bị chia thành 35 lượt gọi độc lập (cụm cắt mỗi khi đổi tone). Đinh Bộ Lĩnh toàn `story`, cụm 16, chỉ 9 lượt và không có cụm nào trầm.
- **Quy tắc:** mọi đoạn của một video đặt `tone` là `story` (sắc thái đổi bằng lời kể, nhạc và âm thanh, không bằng tone đọc). Đọc cùng một cỡ cụm cho cả video (cụm 16 như Đinh Bộ Lĩnh, ít lượt gọi hơn cụm 8). Lệch chữ khi cắt thì dùng `cat_lai_cum.py`.
- **Kiểm sau khi chuẩn hóa, trước `phude_tinh.py` và dựng:** `python phim_ban_do/kiem_cao_do.py <tên> [--cum 16]`. ❌ là cụm có cao độ trung bình lệch quá 8% so với trung vị video; đoạn lẻ lệch chỉ ⚠️ (ngữ điệu hỏi hoặc nhấn tự nhiên cao thấp). Cụm cao hơn ở đầu video có thể là phần hook, nghe thử rồi quyết.
- **Sửa:** xóa các số đoạn của cụm ❌ khỏi `thoi_luong.json`, `hash.json` và mp3, đọc lại cả cụm với cùng cỡ cụm (tối đa 3 lần), kiểm lại. Không dùng đọc riêng từng đoạn để vá vì nhịp khác nhóm.
