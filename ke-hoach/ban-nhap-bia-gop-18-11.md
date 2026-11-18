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
| Vùng an toàn: chữ chính trong y 70–1560 (đáy bị Facebook/TikTok che) | M2 | **BỎ** (chủ kênh 18/11 22:33: bìa chính 16:9) |
| Tiêu đề đọc được; viền là lớp riêng; padding để không cắt dấu; phông Oswald 700 ~206 px (đo ở khung dọc) | M2 | Bắt buộc phần "đọc được, không mất dấu"; phông và cỡ cụ thể là gợi ý, thử lại ở khung ngang |
| Bố cục HAN1 (khung dọc 1080×1920: bản đồ địa hình, thẻ đỏ mốc năm, thẻ trắng nghiêng, hai dòng, thẻ số tập, khẩu hiệu) | M2 | Mẫu dọc của series Chuyện cai trị ngàn năm; **không dùng cho bìa ngang** |
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
3. **Giới hạn thông tin:** ngoài tiêu đề hai dòng, bìa chỉ có logo, thẻ mốc và thương hiệu khi cần; không thêm đoạn chữ phụ (chủ kênh đã nêu ở 22:33, đã đưa vào B2).

## B. Bản gộp đề xuất (toàn văn; sửa 18/11 22:33 theo định hướng 16:9)

> Bản dưới thay cho ba mục ảnh bìa M1–M3. Bài Facebook và giao video giữ nguyên. Định hướng của chủ kênh: ảnh bìa chính theo video dài, **16:9, kích thước thiết kế 1920×1080**; bỏ vùng an toàn y 70–1560 và mọi thông số bố cục riêng cho ảnh dọc.

## Ảnh bìa video

Mỗi video một bìa (không làm nhiều bản cho chủ kênh chọn). Bìa phải khiến người lạ muốn xem, nhưng điều bìa hứa phải là điều video kể đúng. Mục B1–B3 và B5 là quy tắc chung; B4 là mẫu riêng của từng series, không bắt buộc cho series khác. Thiết kế theo video dài: chủ thể lớn, bố cục rõ, ít chữ, nhận ra được khi thu nhỏ.

### B1. Đúng nội dung (quy tắc chung, ưu tiên cao nhất của bìa)
- **Hình là chủ thể của video** (cầu Long Biên thì ảnh cây cầu, trống đồng thì ảnh trống). Không dùng chân dung nhân vật làm ảnh bìa khi chủ thể là vật hoặc công trình, không có ngoại lệ (chủ kênh 10/11/2026). Tên người nhắc trên bìa đi vào chữ, không đi vào hình. Chân dung chỉ dùng khi video kể về chính người đó.
- **Chữ trên bìa khớp điều video chứng minh được.** Không giật tít sai sự thật; khoanh, mũi tên, dấu "?" chỉ vào điều video thật sự kể, không ngụ ý điều video không nói.
- **Không để người xem hiểu sai thời đại.** Ảnh hiện đại, tranh vẽ về sau hay ảnh dựng không đặt kèm mốc năm theo kiểu như ảnh đương thời.
- **Một điểm gây tò mò** (điều lạ nhất của video), nhìn thấy ngay trên hình hoặc ở dòng chữ; không dồn khoanh, mũi tên và câu hỏi cùng lúc.
- Khi giao ghi một dòng: ảnh dùng (tác giả, giấy phép) và vì sao chọn.

### B2. Chữ và bố cục dễ đọc (quy tắc chung)
- Thiết kế ảnh bìa theo tỷ lệ 16:9, kích thước chuẩn 1920×1080.
- Tiêu đề tối đa hai dòng, ngắn gọn, ưu tiên khoảng 3–6 từ nếu phù hợp.
- Chủ thể chính phải nhận ra ngay khi ảnh thu nhỏ.
- Chữ có tương phản rõ với nền, dấu tiếng Việt đầy đủ, không bị cắt hoặc chạm vào nhau (dấu chấm dưới Ạ, Ị; mũ trên Â, Ô; huyền, sắc). Kỹ thuật gợi ý: viền chữ là lớp riêng phía sau chữ, không dùng `-webkit-text-stroke` trên chữ chính; padding đủ để không cắt dấu dưới; hai dòng cách nhau đủ để dấu dòng dưới không chạm dòng trên.
- Ngoài tiêu đề chỉ giữ logo, thẻ mốc năm hoặc thương hiệu khi thực sự cần thiết.
- Không nhồi số liệu, đoạn mô tả hoặc nhiều điểm gây chú ý cùng lúc.
- Phông và cỡ chữ là gợi ý, chọn theo kích thước chủ thể; thử Oswald 700 (OFL, ở `assets/bia/fonts/`) cỡ đủ lớn để đọc ở kích thước thu nhỏ. Be Vietnam Pro Black quá nhỏ dấu, Anton dính dấu: không dùng cho tiêu đề (kinh nghiệm từ bìa dọc, cần thử lại ở khung ngang).

### B3. Logo và chuẩn thương hiệu (khung ngang 1920×1080)
- Mọi bìa có logo cây đèn `assets/logo/nguoi-gac-su.png`, đặt giống logo trong video: vuông 130 px, độ đậm 0,8, góc trên bên phải, cách mép phải 44 px và mép trên 34 px. Không phóng to, không đổ bóng, không bỏ.
- Không để chữ hay hình đè lên logo. Nếu lấy khung hình bản đồ làm nền thì cắt bỏ khung HUD (hộp năm, chú giải, la bàn, phụ đề) trước khi đặt chữ.
- Bìa dùng ở nền tảng khác (Facebook, TikTok) cắt hoặc dựng lại từ bản 1920×1080, vẫn giữ logo đúng quy tắc trên bản cắt.

### B4. Mẫu riêng của từng series (tham khảo; mẫu dọc chưa dùng cho bìa ngang)
- **Video bản đồ 16:9** (`assets/bia/NQ1/tao_bia.py`, `python assets/bia/NQ1/tao_bia.py <khung.jpg>`): mẫu duy nhất đã ở khung 1920×1080 (script cũng xuất bản dọc cho TikTok). Dùng làm điểm xuất phát cho bìa ngang; sửa chữ và vùng cắt cho video mới. Cần rà lại theo B1–B3 trước khi dùng (có phù hợp, có nhồi chữ không).
- **Chuyện cai trị ngàn năm** (tạm dừng): mẫu `assets/bia/HAN1/bia_v3.png` và `assets/bia/tao_bia_mau.py` là KHUNG DỌC 1080×1920, không dùng cho bìa ngang. Giữ làm tham khảo ý tưởng (thẻ mốc năm, thẻ triều đại, tiêu đề hai dòng, chân trang thương hiệu); khi series chạy lại thì làm mẫu ngang mới.
- **Bí mật biểu tượng** (`assets/bia/XK/tao_bia.py`): mẫu dọc 1080×1920, vòng khoanh đỏ kèm "?" (`hook=dict(cx, cy, r, q)`), khai báo `chu_the` khớp tên video. Chưa có mẫu ngang; ý "một điểm gây tò mò, khoanh đúng chỗ video kể" là phong cách của loạt, không phải khuôn của series khác.
- Series khác (thủy mặc, Sengoku, Tên tỉnh thành…): tự thiết kế theo B1–B3 ở 1920×1080, không bắt chước mẫu của series khác; có mẫu riêng thì ghi vào đây khi chủ kênh duyệt.

### B5. Chọn ảnh và kiểm trước khi giao
- **Chọn ảnh:** xem mọi ảnh ứng viên cạnh nhau. Ưu tiên ảnh toàn cảnh, rõ hình dáng đặc trưng, sáng, không bị che quá một phần ba; chủ thể lớn trong khung ngang. Tránh ảnh cận chi tiết (biển tên, đinh tán), ảnh mờ, ảnh có logo kho ảnh; ảnh chi tiết chỉ dùng khi chính chi tiết đó là điểm gây tò mò.
- **Kiểm (bắt buộc):** (1) mở bìa 1920×1080 ở cỡ lớn, tự hỏi "chưa biết video, nhìn ảnh này đoán chuyện gì?"; đoán sai hoặc không đoán được thì đổi ảnh; (2) thu nhỏ về cỡ hiển thị gợi ý của YouTube (khoảng 320×180) và kiểm chủ thể vẫn nhận ra, chữ vẫn đọc được, dấu tiếng Việt còn rõ; (3) so hình và chữ với tên video, tiêu đề đăng và câu 1 kịch bản. Không giao khi chưa kiểm.

## C. Điều bị bỏ hoặc hạ cấp (chủ kênh biết)
- **Bỏ:** vùng an toàn y 70–1560 và mọi thông số bố cục dành riêng cho ảnh dọc 1080×1920 (chủ kênh 18/11 22:33). Mẫu HAN1 và XK vì thế thành tham khảo, không chuẩn.
- "Dòng 2 là câu hỏi" hạ thành gợi ý: dòng 2 là điều lạ nhất mà video chứng minh được.
- "Tối đa 4 chữ mỗi dòng" (đo ở khung dọc) thay bằng "tối đa hai dòng, khoảng 3–6 từ nếu phù hợp".
- "Bố cục và logo giữ nguyên mẫu đã duyệt" (M3): bố cục thành mẫu riêng của series (B4); logo vẫn bắt buộc (B3).
- "Mỗi bìa phải có khoanh đỏ hoặc mũi tên" (M3) thành phong cách riêng; chung chỉ còn "một điểm gây tò mò, đúng nội dung".
- Không bỏ quy tắc nào về đúng sử, logo, kiểm dấu tiếng Việt.

## D. Kiểm nhất quán với các file đã cập nhật
- `giong-van.md`: tiêu đề video và bìa phải theo mục 6 (phân biệt sử liệu, lời đồn); bìa không biến giai thoại thành sự thật. B1 đã khớp ("chữ trên bìa khớp điều video chứng minh được").
- `bien-tap.md`: bước kiểm bìa nằm cùng bước giao video; không mâu thuẫn. Câu hỏi tự rà tầng 3 ("hook hấp dẫn chưa") áp dụng cho cả bìa như một câu hỏi, không là điều kiện chặn.
- `dna-series.md`: B4 chỉ nêu mẫu theo series có trong bảng series; series dừng (Chuyện cai trị ngàn năm) ghi "tạm dừng" để mẫu HAN1 không bị coi là chuẩn chung.
- Tham chiếu đường dẫn trong dự thảo (`assets/bia/...`, `assets/logo/...`) sẽ kiểm bằng `tools/kiem_lien_ket.py` sau khi thay.

## E. Chủ kênh duyệt giúp
1. Bản B có giữ đủ điều quan trọng chưa? Điều gì bị mất hoặc yếu đi?
2. Ba điểm A4 (ảnh không đương thời; tiêu đề bìa khớp tiêu đề đăng; giới hạn thông tin trên bìa): thêm hay không?
3. B4: HAN1 và XK là mẫu dọc nên tôi đánh dấu "chưa dùng cho bìa ngang"; chỉ NQ1 đang ở 1920×1080. Anh có muốn làm mẫu ngang mới cho Bí mật biểu tượng (video dọc 9:16 nhưng bìa 16:9)? Mặc định của tôi: chưa làm, đến khi cần mới làm.
4. Sau khi duyệt, tôi thay ba mục trong `dang-bai-va-bia.md` bằng bản B (bài Facebook và giao video giữ nguyên), chạy `tools/kiem_lien_ket.py`.
