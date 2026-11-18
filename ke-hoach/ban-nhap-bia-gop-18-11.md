# Dự thảo gộp ba mục ảnh bìa trong `quy-tac/dang-bai-va-bia.md` (18/11/2026)

**Trạng thái: DỰ THẢO, CHỜ CHỦ KÊNH DUYỆT.** `dang-bai-va-bia.md` chưa bị thay. Ba lưu ý của chủ kênh (22:28) đã dùng làm khung: (1) bìa thu hút nhưng không làm sai lệch nội dung lịch sử; (2) chữ dễ đọc trên điện thoại, không nhồi thông tin; (3) tách quy tắc chung khỏi yêu cầu riêng của từng series, không biến một phong cách thành khuôn bắt buộc.

Ba mục cũ: **M1** "luôn có logo kênh" (24/10), **M2** "bìa dọc 1080×1920 mẫu đã duyệt" (06/11, từ tập "Chín quận" của series Chuyện cai trị ngàn năm), **M3** "đúng cốt truyện và cuốn hút" (10/11, từ bìa #15 Cầu Long Biên). Hai mục không thuộc phạm vi gộp (bài Facebook, giao video) giữ nguyên.

## A. Bảng đối chiếu

### A1. Trùng lặp (gộp thành một)
| Nội dung | Ở đâu | Cách gộp |
|---|---|---|
| Logo cây đèn góc trên phải, không đè | M1 (số đo), M2 ("đúng quy tắc logo"), M3 ("giữ nguyên") | Ghi số đo MỘT lần, các chỗ khác bỏ |
| Xem bìa ở cỡ lớn trước khi giao | M1, M2, M3 | Một mục "kiểm trước khi giao" |
| Kiểm dấu tiếng Việt ở cỡ nhỏ | M2 (270×480), M3 (270×480) | Gộp |
| Chữ trong vùng y 70–1560, đáy chỉ thương hiệu | M2, M3 | Một lần |

### A2. Yêu cầu riêng (mỗi mục thêm điều mục khác không có)
| Yêu cầu | Từ | Loại đề xuất |
|---|---|---|
| Logo: 130 px, độ đậm 0,8, cách mép phải 44 và trên 34; không phóng to, không đổ bóng | M1 | Bắt buộc chung (thương hiệu) |
| Không để chữ, hình đè logo; cắt bỏ HUD khỏi khung bản đồ làm nền | M1 | Bắt buộc chung |
| Vùng an toàn: chữ chính trong y 70–1560 (đáy bị Facebook/TikTok che) | M2 | Bắt buộc chung (kỹ thuật nền tảng) |
| Tiêu đề đọc được cỡ điện thoại; viền là lớp riêng; padding để không cắt dấu; phông Oswald 700 ~206 px | M2 | Bắt buộc phần "đọc được, không mất dấu"; phông và cỡ cụ thể là gợi ý |
| Bố cục HAN1 (bản đồ địa hình, thẻ đỏ mốc năm, thẻ trắng nghiêng, hai dòng, thẻ số tập, khẩu hiệu) | M2 | **Riêng series** Chuyện cai trị ngàn năm, không áp cho series khác |
| Hình đúng chủ thể của video; không dùng chân dung khi chủ thể là vật hoặc công trình, không ngoại lệ | M3 | Bắt buộc chung (đã chốt 10/11, "không thêm ngoại lệ") |
| Chọn ảnh: so các ứng viên, toàn cảnh, sáng, không che quá 1/3, tránh ảnh cận, mờ, logo kho ảnh | M3 | Gợi ý, trừ điều "đoán được chủ đề" |
| Mỗi bìa MỘT điểm gây tò mò (khoanh đỏ "?", mũi tên, X đỏ), dòng 1 chủ thể, dòng 2 câu hỏi, tối đa 4 chữ mỗi dòng | M3 | **Phong cách của loạt Bí mật biểu tượng (`assets/bia/XK`)**; chỉ điều "một điểm gây tò mò, không giật tít sai" là chung |
| Khai báo `chu_the`, thẻ tên khớp vật trong ảnh | M3 | Kỹ thuật của công cụ `XK/tao_bia.py` |
| Mỗi video một bìa | M3 | Chung |
| Khi giao ghi: ảnh dùng (tác giả, giấy phép), vì sao chọn | M3 | Bắt buộc chung |
| Bản mẫu cũ `HAN1/tao_bia.py` không dùng cho bố cục mới | M2 | Ghi chú tham khảo |

### A3. Điểm mâu thuẫn hoặc dễ hiểu nhầm
a. **Mẫu M2 vs M3.** M3 viết "bố cục và logo giữ nguyên mẫu đã duyệt" như áp dụng mọi bìa; M2 chỉ nói mẫu dùng "cho mọi video cùng bố cục". **Đề xuất:** mẫu HAN1 và vòng khoanh XK là mẫu của từng series, series khác tự có mẫu; chỉ điều quy tắc chung (mục B1) bắt buộc.
b. **"Dòng 2 là câu hỏi"** (M2, M3) thành luật cho mọi bìa: không phải video nào cũng có câu hỏi thật. Câu hỏi giả chỉ để câu khách vi phạm lưu ý 1. **Đề xuất:** dòng 2 là "điều lạ nhất mà video chứng minh được" (có thể câu hỏi, có thể một sự kiện).
c. **"Tối đa 4 chữ mỗi dòng"** là giới hạn thẩm mỹ của khung 1080 và phông ~206 px, không phải giới hạn lịch sử. **Đề xuất:** viết thành giới hạn đọc được (xem B2): số chữ ít vừa để đọc ở 270×480; con số "khoảng 4" là gợi ý.
d. **"Khoanh đỏ vào đúng chỗ của câu hỏi chính"** có nguy cơ chỉ vào chi tiết ảnh mà video không kể. **Đề xuất:** thêm điều kiện: chỗ khoanh phải là điều được kể trong video.

### A4. Quy tắc còn thiếu (đề xuất thêm, chủ kênh quyết)
1. **Ảnh không phải tư liệu đương thời** (ảnh hiện đại, tranh vẽ sau này, ảnh AI) không đặt kèm mốc năm hay chữ gây hiểu là ảnh thời đó. Chưa có quy tắc nào về việc này.
2. **Tiêu đề bìa khớp tiêu đề đăng và câu 1 kịch bản** (M3 chỉ nói khớp câu 1); tránh bìa hứa một điều, tiêu đề hứa điều khác.
3. **Giới hạn thông tin:** ngoài tiêu đề hai dòng, bìa chỉ có logo, một thẻ mốc (nếu có) và thương hiệu; không thêm đoạn chữ phụ.

## B. Bản gộp đề xuất (toàn văn)

> Bản dưới thay cho ba mục ảnh bìa M1–M3. Bài Facebook và giao video giữ nguyên.

## Ảnh bìa video

Mỗi video một bìa (không làm nhiều bản cho chủ kênh chọn). Bìa phải khiến người lạ muốn xem, nhưng điều bìa hứa phải là điều video kể đúng. Mục B1–B3 là quy tắc chung; B4 là mẫu riêng của từng series, không bắt buộc cho series khác.

### B1. Đúng nội dung (quy tắc chung, ưu tiên cao nhất của bìa)
- **Hình là chủ thể của video** (cầu Long Biên thì ảnh cây cầu, trống đồng thì ảnh trống). Không dùng chân dung nhân vật làm ảnh bìa khi chủ thể là vật hoặc công trình, không có ngoại lệ (chủ kênh 10/11/2026). Tên người nhắc trên bìa đi vào chữ, không đi vào hình. Chân dung chỉ dùng khi video kể về chính người đó.
- **Chữ trên bìa khớp điều video chứng minh được.** Không giật tít sai sự thật; khoanh, mũi tên, dấu "?" chỉ vào điều video thật sự kể, không ngụ ý điều video không nói.
- **Không để người xem hiểu sai thời đại.** Ảnh hiện đại, tranh vẽ về sau hay ảnh dựng không đặt kèm mốc năm theo kiểu như ảnh đương thời.
- **Bìa tạo tò mò bằng đúng một điểm** (điều lạ nhất của video), nhìn thấy ngay trên hình hoặc ở dòng chữ; không đủ cả khoanh, mũi tên và câu hỏi cùng lúc.
- Khi giao ghi một dòng: ảnh dùng (tác giả, giấy phép) và vì sao chọn.

### B2. Chữ đọc được trên điện thoại (quy tắc chung)
- Tiêu đề tối đa hai dòng, mỗi dòng ngắn (khoảng 4 chữ là gợi ý cho khung dọc 1080). Ngoài tiêu đề chỉ có logo, một thẻ mốc nếu cần và thương hiệu; không thêm đoạn chữ phụ, không nhồi số liệu.
- Phải đọc được rõ ở cỡ 270×480, mọi dấu tiếng Việt còn nhìn thấy (dấu chấm dưới Ạ, Ị; mũ trên Â, Ô; huyền, sắc). Viền là lớp riêng phía sau chữ, không dùng `-webkit-text-stroke` trên chữ chính; padding đủ để không cắt dấu dưới; hai dòng cách nhau đủ để dấu dòng dưới không chạm dòng trên.
- Phông gợi ý: Oswald 700 (cỡ khoảng 206 px ở khung 1080). Be Vietnam Pro Black quá nhỏ dấu, Anton dính dấu: không dùng cho tiêu đề. Phông (OFL) ở `assets/bia/fonts/`.
- Chữ chính nằm trong y 70–1560 (khung dọc 1080×1920); vùng đáy Facebook/TikTok che, đáy chỉ là chân trang thương hiệu, không để đáy đen trơn.

### B3. Logo và chuẩn thương hiệu (quy tắc chung)
- Mọi bìa (YouTube, Facebook, TikTok) có logo cây đèn `assets/logo/nguoi-gac-su.png`, đặt giống logo trong video: vuông 130 px, độ đậm 0,8, góc trên bên phải, cách mép phải 44 px và mép trên 34 px (khổ 1920 rộng; khổ dọc 1080 dùng cùng cỡ và vị trí). Không phóng to, không đổ bóng, không bỏ.
- Không để chữ hay hình đè lên logo. Nếu lấy khung hình bản đồ làm nền thì cắt bỏ khung HUD (hộp năm, chú giải, la bàn, phụ đề) trước khi đặt chữ.

### B4. Mẫu riêng của từng series (tham khảo, không bắt buộc cho series khác)
- **Chuyện cai trị ngàn năm** (tạm dừng): mẫu `assets/bia/HAN1/bia_v3.png`. Bản đồ địa hình phủ kín khung, chấm điểm phát sáng ở nửa trên, thẻ đỏ viền vàng (mốc năm), thẻ trắng nghiêng (triều đại hoặc bên chính), tiêu đề hai dòng (dòng 1 trắng ngà, dòng 2 vàng), thẻ tên loạt và số tập, chân trang "NGƯỜI GÁC SỬ" và khẩu hiệu "LỊCH SỬ THEO CHÍNH SỬ". Mã tạo: `python assets/bia/tao_bia_mau.py <cau_hinh.json> [ra.png]`; cấu hình mẫu `assets/bia/HAN1/bia.json` (tập mới: sao chép sang `assets/bia/<MÃ>/`, đổi chữ, danh sách điểm (kinh, vĩ), `lon0`, `scale`, `oy`). Mẫu cũ `assets/bia/HAN1/tao_bia.py` (nền khung video) chỉ tham khảo.
- **Bí mật biểu tượng** (`assets/bia/XK/tao_bia.py`): vòng khoanh đỏ kèm "?" (`hook=dict(cx, cy, r, q)`, tọa độ theo khung 1080×1920), hoặc mũi tên, dấu X đỏ, hình đối lập; dòng 1 nêu chủ thể, dòng 2 là điều lạ nhất của video (có thể là câu hỏi). Khai báo `chu_the` (vật trong ảnh) và chỉ giao khi khớp tên video; thẻ tên nhỏ trên ảnh phải đúng vật trong ảnh. Ảnh được tăng nhẹ tương phản và màu (đã đặt sẵn trong `tao_bia.py`). Vòng khoanh và dấu "?" không che chủ thể, không đè logo, thẻ năm, thẻ tên.
- **Video bản đồ** (NQ1): mẫu `assets/bia/NQ1/tao_bia.py` (`python assets/bia/NQ1/tao_bia.py <khung.jpg>`; sửa chữ và vùng cắt cho video mới).
- Series khác (thủy mặc, Sengoku, Tên tỉnh thành…) có thể đặt mẫu riêng ở đây khi chủ kênh duyệt; chưa có thì tự thiết kế theo B1–B3, không bắt chước mẫu của series khác.

### B5. Chọn ảnh và kiểm trước khi giao
- **Chọn ảnh:** xem mọi ảnh ứng viên cạnh nhau. Ưu tiên ảnh toàn cảnh, rõ hình dáng đặc trưng, sáng, không bị che quá một phần ba. Tránh ảnh cận chi tiết (biển tên, đinh tán), ảnh mờ, ảnh có logo kho ảnh; ảnh chi tiết chỉ dùng khi chính chi tiết đó là điểm gây tò mò.
- **Kiểm (bắt buộc):** mở bìa ở cỡ lớn, tự hỏi "chưa biết video, nhìn ảnh này đoán chuyện gì?"; đoán sai hoặc không đoán được thì đổi ảnh. So hình và chữ với tên video, tiêu đề đăng và câu 1 kịch bản; kiểm dấu tiếng Việt ở cỡ 270×480 (xem ảnh cắt vùng tiêu đề ở cỡ lớn). Không giao khi chưa kiểm.

## C. Điều bị bỏ hoặc hạ cấp (chủ kênh biết)
- "Dòng 2 là câu hỏi" (M2, M3) hạ thành gợi ý: dòng 2 là điều lạ nhất mà video chứng minh được.
- "Tối đa 4 chữ mỗi dòng" hạ thành gợi ý đọc được; bắt buộc là đọc được ở 270×480.
- "Bố cục và logo giữ nguyên mẫu đã duyệt" (M3): bố cục thành mẫu riêng của series (B4); logo vẫn bắt buộc (B3).
- "Mỗi bìa phải có khoanh đỏ hoặc mũi tên" (M3) thành phong cách của Bí mật biểu tượng; chung chỉ còn "một điểm gây tò mò, đúng nội dung".
- Không bỏ quy tắc nào về đúng sử, logo, vùng an toàn, kiểm dấu tiếng Việt.

## D. Kiểm nhất quán với các file đã cập nhật
- `giong-van.md`: tiêu đề video và bìa phải theo mục 6 (phân biệt sử liệu, lời đồn); bìa không biến giai thoại thành sự thật. B1 đã khớp ("chữ trên bìa khớp điều video chứng minh được").
- `bien-tap.md`: bước kiểm bìa nằm cùng bước giao video; không mâu thuẫn. Câu hỏi tự rà tầng 3 ("hook hấp dẫn chưa") áp dụng cho cả bìa như một câu hỏi, không là điều kiện chặn.
- `dna-series.md`: B4 chỉ nêu mẫu theo series có trong bảng series; series dừng (Chuyện cai trị ngàn năm) ghi "tạm dừng" để mẫu HAN1 không bị coi là chuẩn chung.
- Tham chiếu đường dẫn trong dự thảo (`assets/bia/...`, `assets/logo/...`) sẽ kiểm bằng `tools/kiem_lien_ket.py` sau khi thay.

## E. Chủ kênh duyệt giúp
1. Bản B có giữ đủ điều quan trọng chưa? Điều gì bị mất hoặc yếu đi?
2. Ba điểm A4 (ảnh không đương thời; tiêu đề bìa khớp tiêu đề đăng; giới hạn thông tin trên bìa): thêm hay không?
3. Phân loại ở B4 (mẫu riêng của từng series) có đúng ý anh không?
4. Sau khi duyệt, tôi thay ba mục trong `dang-bai-va-bia.md` bằng bản B (bài Facebook và giao video giữ nguyên), chạy `tools/kiem_lien_ket.py`.
