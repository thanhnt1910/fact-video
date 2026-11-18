# Quy tắc video bản đồ 16:9 (mapfilm3.py)

> Kiểu bản đồ 16:9 đã bỏ; giữ để tra. Nguồn: `archive/CLAUDE-truoc-tai-cau-truc-18-11.md`. Chuyển ngày 18/11/2026.

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
