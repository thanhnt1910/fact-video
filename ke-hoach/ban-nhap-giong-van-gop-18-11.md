# Dự thảo gộp `quy-tac/giong-van.md` (18/11/2026)

**Trạng thái: DỰ THẢO, CHỜ CHỦ KÊNH DUYỆT. `quy-tac/giong-van.md` hiện hành chưa bị thay.**

Trình tự đã làm: (1) đọc và đối chiếu sáu mục; (2) xác định trùng, bổ sung, mâu thuẫn; (3) viết bản gộp giữ yêu cầu có giá trị; (4) gửi duyệt. Bước 5 (thay file gốc) chỉ làm sau khi được duyệt.

Sáu mục văn phong đã đối chiếu (số hiệu theo `giong-van.md` hiện hành):
- **M1** Làm kịch bản bằng ngôn ngữ tự nhiên (25/10)
- **M2** Câu chữ sáng tạo (11/11)
- **M3** Văn xuôi liền mạch trước, chia đoạn sau (12/11)
- **M4** Viết lịch sử rõ ràng, đầy đủ, không nói tắt (23/10)
- **M5** Sengoku và sử nước ngoài: viết cho người chưa biết gì (16/11)
- **M6** Nới quy tắc viết kịch bản (05/11)
Mục thứ bảy, "Diễn giải của người kể" (duyệt 01/11), giữ nguyên, không gộp.

## A. Bảng đối chiếu

### A1. Trùng lặp (gộp thành một câu)
| Ý | Nằm ở | Gộp thành |
|---|---|---|
| Đủ họ tên, không nói tắt | M1, M4, M5 | Một mục "Rõ ràng, không nói tắt" |
| Câu nối nhau bằng nguyên nhân – kết quả, không liệt kê | M1 (nối bằng "nhưng", "rồi", "vì vậy"), M3, M5 | Một mục "Mạch câu" |
| Đọc lại như người chưa biết, câu phải đọc hai lần thì viết lại | M1, M3, M5 | Một dòng ở bước tự rà |
| Câu khuôn không mang thông tin | M1 ("tránh câu khuôn máy"), M3 | Một dòng, xem A3-a |
| Ví von, đùa chỉ đặt sau khi người nghe đã đủ nền | M2, M5 | Gộp vào "Sáng tạo câu chữ" |
| Hài chỉ nhắm vào tình huống và phía xâm lược; không đùa anh hùng, nỗi đau | M2, và mục "Series sử Việt" của `dna-series.md` | Giữ ở `dna-series.md`; `giong-van.md` chỉ nhắc một dòng |
| Chi tiết cụ thể thay lời khen chung chung | M1, M5 (cực cấp không nguồn) | Gộp một dòng |

### A2. Bổ sung (mỗi mục thêm điều mục khác không có)
- M1 thêm: nhịp câu dài ngắn; không mở câu cùng một kiểu; không giải nghĩa kiểu từ điển.
- M2 thêm: danh sách cái được và không được phép sáng tạo; mật độ một điểm sáng tạo mỗi 3–4 đoạn.
- M3 thêm: thứ tự viết (văn xuôi trước, chia đoạn sau); xương sống một câu; câu dẫn đường và câu chốt ý được dùng; hiểu trước, bất ngờ sau; kiểm dữ kiện kể cả bản chủ kênh viết.
- M4 thêm: các ví dụ viết đủ (thủy triều lên, thuyền chiến của quân Nguyên, quân Đại Việt); nêu hệ quả của hiện tượng ngay trong câu; nêu tên người chỉ huy khi nhắc trận.
- M5 thêm: giải thích thuật ngữ, tên tổ chức, địa danh lạ ngay trong câu; không dịch sát gây hiểu sai; rà năm điểm (chủ ngữ, ai với ai, từ lạ, mốc khớp, cực cấp có nguồn); mốc nhất quán giữa các đoạn. Phần "hồ sơ vụ án" chỉ dành cho loạt Sengoku.
- M6 thêm: danh sách điều đã nới (không còn cấm).

### A3. Mâu thuẫn, cần quyết
a. **Câu khuôn.** M6 (05/11) bỏ cấm "câu khuôn" kiểu "Câu chuyện cho thấy…". M1 (25/10) vẫn cấm; M3 (12/11) lại cấm "câu khuôn không mang thông tin" nhưng cho phép câu dẫn đường và câu chốt ý. **Đề xuất:** không có danh sách cấm; chỉ nhắc ở bước biên tập "bỏ câu không mang thông tin hoặc hướng đi". Khớp nguyên tắc cốt lõi (checklist là công cụ biên tập).
b. **Số "tức là / nghĩa là"** (M1: không quá 5 lần) và **tỷ lệ mở câu** ("mỗi kiểu không quá 1/10") là ngưỡng cứng trong M1; mục "Diễn giải… ngưỡng mềm" (01/11) đã hạ chúng thành mục tiêu mềm. **Đề xuất:** ghi là gợi ý, không đưa con số vào luật.
c. **Độ dài đoạn.** M1 ghi 20–30 chữ; ngưỡng mềm 01/11 ghi 15–30, trung bình 26; giới hạn cứng 32 chữ, 2 câu (`kiem_kich_ban.py`). **Đề xuất:** viết một lần: "tối đa 32 chữ và 2 câu (cứng); khoảng 15–30 chữ là thuận tai (gợi ý)".
d. **Năm và chữ số trong lời đọc.** M6 (05/11) cho phép chữ số; nguyên tắc cốt lõi mục 10 vẫn ghi "năm, số viết bằng chữ"; thực tế 12/11 Gemini hay đọc sai năm viết bằng chữ. **Đề xuất:** mặc định viết năm bằng chữ ở trường `text`, kèm `hien` bằng số cho phụ đề; nếu giọng đã đọc sai một lượt thì chuyển sang chữ số, kiểm bằng nhận dạng không gợi ý (đã nằm ở `kiem-tra-ky-thuat.md`). Cần chủ kênh xác nhận một trong hai.
e. **Nguồn trong lời kể.** M1 cấm nhắc tên sách; M6 bỏ điều cấm này. **Đề xuất:** bỏ cấm. Nêu nguồn trong lời kể khi nó giúp người nghe tin hoặc hiểu (1–2 lần), phần còn lại ở mô tả và bình luận.
f. **Lời bàn sử gia (theo quyết định 18/11).** Giữ lời bàn có ghi tên; phân biệt lời trích dẫn và diễn giải của người kể; không biến lời bàn thành sự thật đã xác minh. Khớp với "Diễn giải của người kể" mục 1; chỉ cần thêm một mục "Lời sử gia" (xem B).

### A4. Nội dung chuyển đi
- M5 phần "Khung hồ sơ vụ án" (4 dấu CÓ SỬ, GIAI THOẠI, LỜI KHAI MÂU THUẪN, KHÔNG AI BIẾT, tranh thủy mặc, mẫu `nb1…`) → `quy-tac/series/sengoku.md` (file mới). Không để trong `giong-van.md`.
- M6: danh sách điều đã nới → một dòng "đã bỏ" trong `archive/quy-dinh-da-thay-the.md`; không nằm trong `giong-van.md`.

## B. Bản gộp đề xuất (toàn văn)

> Bản dưới thay cho sáu mục M1–M6. Mục "Diễn giải của người kể" ở cuối file hiện hành giữ nguyên.

### Giọng văn lời kể

Kể như người kể chuyện nói với bạn mình, cho người chưa biết gì về chuyện này. Nghe một lần là hiểu. Câu nào phải đọc hai lần thì viết lại. Đúng lịch sử là điều kiện; mọi thứ dưới đây là cách kể cho hay (nguyên tắc cốt lõi đứng trên).

**1. Thứ tự làm**
- Viết cả câu chuyện thành văn xuôi liền mạch trước, đối chiếu dữ kiện với nguồn, rồi mới chia đoạn cho giọng đọc. Không viết thẳng thành các mẩu ngắn.
- Nói được câu chuyện trong một câu ("hai tỉnh, hai câu chuyện đi song song, gặp nhau năm 1976") rồi mới viết. Thân bài đi theo xương sống ấy, không theo thứ tự mốc của nguồn.
- Chủ kênh viết bản của mình thì giữ câu chữ và mạch; chỉ đổi chỗ sai dữ kiện hoặc vượt giới hạn kỹ thuật, và liệt kê từng chỗ sửa kèm nguồn. Câu dễ nghe không được thay dữ kiện đúng.

**2. Mạch câu**
- Các câu cần có quan hệ hợp lý với nhau. Ưu tiên mạch nguyên nhân – kết quả, diễn biến thời gian hoặc đối lập khi phù hợp. Không liệt kê sự kiện rời rạc nếu giữa chúng có quan hệ cần giải thích. Câu giới thiệu nhân vật hay mô tả địa điểm không bắt buộc phải có từ nối nhân quả.
- Khi kể một sự kiện, cần làm rõ ai làm gì, với ai và vì sao khi thông tin đó cần thiết để hiểu câu chuyện. Nguồn chép ngắn thì mở rộng thành chuyện bằng điều nguồn cho phép, không tự suy ra.
- Câu dẫn đường ("Rồi vùng đất này rẽ thành hai câu chuyện.") và câu chốt sau đoạn phức tạp được dùng, nếu giúp người nghe biết mình đang ở đâu và không lặp điều vừa kể. Bỏ câu không mang thông tin hoặc hướng đi.
- Hiểu trước, bất ngờ sau: câu tạo bất ngờ chỉ đặt khi người nghe đã nắm chuyện đang xảy ra.
- Nền trước, hình ảnh sau: ví von, ví dụ, câu đùa đặt SAU khi người nghe đã biết đủ để thấy nó đúng. Thứ tự: ai/cái gì → chuyện gì xảy ra → ví von làm điểm nhấn → nguyên nhân hoặc bước tiếp.

**3. Nhịp và câu chữ (gợi ý, không phải ngưỡng cứng)**
- Kể như người nói chuyện, không viết kiểu nghị luận hay văn giáo khoa.
- Không cố tạo bí ẩn bằng câu hỏi tu từ liên tục. Tự hỏi tự đáp dùng thưa, mỗi lần có một câu trả lời thật ngay sau.
- Không lặp thông tin để kéo dài thời lượng; thiếu chất liệu thì thêm chi tiết có nguồn, không độn câu. Không dùng câu chuyển đoạn chỉ để nối cho đủ ý.
- Ưu tiên chi tiết lịch sử cụ thể thay vì nhận xét chung chung.
- Nhịp câu có dài có ngắn; chỗ cần nhấn dùng câu thật ngắn.
- Đổi cách mở câu; không mở nhiều câu liền nhau cùng một kiểu hay cùng một chữ.
- Không giải nghĩa kiểu từ điển: gộp lời giải vào chính câu. Dùng "tức là", "nghĩa là" khi đó là cách nghe tự nhiên nhất.
- Chi tiết cụ thể có nguồn thay lời khen chung chung ("đánh đâu thắng đó nên được gọi là Vạn Thắng Vương", không "ông là người tài giỏi").
- Đoạn ngắn, dễ nghe, có chỗ nghỉ tự nhiên. Khoảng 15–30 chữ chỉ là tham khảo, không chấm lỗi.
- 32 chữ và 2 câu mỗi đoạn là giới hạn kỹ thuật của giọng đọc, do `kiem_kich_ban.py` kiểm (chủ kênh đã chốt). "Chữ" ở đây là mỗi cụm cách nhau bởi dấu cách trong trường `text` (với tiếng Việt thường là một âm tiết, không phải "từ" ghép); câu đếm theo dấu . ! ? sau đó là dấu cách. Đây là quy tắc kỹ thuật, không phải tiêu chuẩn văn phong. Vượt giới hạn không có nghĩa là viết dở; chỗ nào vượt thì ngắt ở nhịp tự nhiên, không ngắt máy móc.

**4. Rõ ràng, không nói tắt**
- Viết đủ danh từ: "thuyền chiến của quân Nguyên" (không "thuyền Nguyên"), "thủy triều lên" (không "triều lên"), "quân Đại Việt" hoặc tên người chỉ huy (không "người Việt" chung chung khi nói về người đánh trận).
- Họ tên đủ lần đầu và khi dễ nhầm. Sau lần giới thiệu đầy đủ, có thể dùng tên gọi ngắn hoặc đại từ khi không gây nhầm lẫn; ưu tiên rõ ràng, không máy móc lặp lại danh xưng. Nhắc trận đánh thì nêu tên người chỉ huy ngay lần đầu, nếu sử liệu xác định được; không tự suy đoán khi nguồn không ghi rõ.
- Hiện tượng (thủy triều, mùa mưa, bão): nói luôn hệ quả trong câu.
- Thuật ngữ, tên tổ chức, địa danh lạ giải thích ngay trong câu hoặc câu liền sau; tên mới lần đầu có vai trò đi kèm.
- Không dịch sát gây hiểu sai ("quan lớn" cho lãnh chúa); dùng vai trò thật và nói rõ vật tranh chấp. Không cực cấp, nhận định không nguồn ("mạnh nhất").
- Mốc, tên, quan hệ phải khớp giữa các đoạn; chi tiết nhắc lại báo "như đã kể".

**5. Sáng tạo câu chữ (cho phép 11/11)**
- Được (là lời người kể): so sánh, ẩn dụ gần gũi; cường điệu rõ là cách nói; câu hỏi tự hỏi tự đáp ("Lý do hả? Nhà hết tiền."); câu cảm thán ngắn; nhịp đảo; khẩu ngữ nhẹ; đối lập; lời bình hóm hỉnh về tình huống.
- Không được: gán cho nhân vật câu nói, ý nghĩ, cảm xúc không có trong tài liệu; thêm hoặc đổi sự kiện, số, năm, tên cho câu hay; cường điệu làm sai số liệu; so sánh làm lệch bản chất.
- Sáng tạo câu chữ phục vụ việc kể chuyện, không phải mục tiêu tự thân. Chỉ dùng khi giúp người nghe hình dung, hiểu rõ hoặc nhớ lâu hơn. Không có mật độ quy định; có đoạn chỉ cần kể sự kiện. Tránh lặp một kiểu ví von, hài hước hay cảm thán trong những đoạn gần nhau.
- Đùa chỉ nhắm vào tình huống và chi tiết đời thường; không đùa nỗi đau, cái chết, phía bị hại, anh hùng dân tộc.

**6. Nguồn và lời sử gia trong lời kể**
- Nêu nguồn trong lời kể khi việc đó giúp người nghe hiểu xuất xứ thông tin hoặc đánh giá độ tin cậy. Không nhắc tên nguồn theo công thức hoặc lặp lại không cần thiết; phần còn lại ở mô tả và bình luận ghim.
- **Khi sử liệu khác nhau** về sự kiện, niên đại, quân số hoặc nhân vật: đối chiếu và ghi nhận sự khác biệt. Không tự chọn một dị bản rồi trình bày như sự thật đã xác minh. Một nguồn ghi chép không đồng nghĩa với sự kiện đã được xác minh độc lập. Phân biệt điều sử liệu ghi chép với điều giới nghiên cứu còn tranh luận. Nhận định của người kể phải có căn cứ, không vượt quá điều nguồn cho phép.
- **Lời bàn của sử gia có ghi tên** (Lê Văn Hưu, Ngô Sĩ Liên…) được giữ khi giúp giải thích hoặc làm sáng tỏ câu chuyện; trích tên.
- Phân biệt rõ ba lớp: sử liệu (điều nguồn ghi), lời sử gia (quan điểm của người viết sử, nêu tên), diễn giải của người kể (theo năm điều kiện bên dưới). Không trình bày lời bàn như sự thật đã xác minh khi nguồn chỉ là quan điểm. Không để lời của kênh thay lời sử gia.

**7. Tự rà trước khi gửi duyệt**
Đọc liền một mạch như người chưa biết chuyện: chỗ nào phải tự nối hai mốc, tên nào xuất hiện mà chưa giới thiệu thì thêm câu dẫn hoặc giới thiệu. Với sử nước ngoài, rà từng câu theo năm điểm (chủ ngữ rõ; ai với ai rõ; từ lạ đã giải thích; mốc khớp các đoạn khác; cực cấp và nhận định có nguồn) và ghi kết quả vào bản gửi duyệt.
Với mọi kịch bản (cả sử Việt Nam) rà thêm ba câu hỏi:
- Người nghe có phân biệt được đâu là sự kiện, đâu là truyền thuyết hoặc giai thoại không?
- Số liệu, mốc thời gian, quan hệ nhân vật đã kiểm bằng nguồn chưa?
- Có chỗ nào người kể suy diễn quá mức từ một chi tiết sử liệu không?

## B2. Ghi chú đi kèm bản gộp (chủ kênh góp ý 18/11, tối)
- Ba ý vừa thêm ở mục 3 (không nghị luận/giáo khoa; không câu hỏi tu từ liên tục; không lặp để kéo dài) trước đó bị thiếu: ý thứ ba vốn nằm trong quy định thời lượng đã lưu trữ và bị bỏ sót khi chuyển.
- Năm câu tự rà "tầng 3" (hook đã hấp dẫn chưa; có chi tiết lịch sử đáng nhớ không; nhịp kể có giữ chân không; kết có dư âm không; rút gọn được mà không mất thông tin không) chưa đưa vào `bien-tap.md`; sẽ đưa khi bản gộp được duyệt.
- Cách phân tầng cho công cụ và người đọc: tầng 1 (sai sử, sai niên đại, nguồn sai) là cổng duyệt của người, công cụ chỉ kiểm có ghi sự việc và nguồn; tầng 2 công cụ chỉ bắt dấu hiệu bề mặt, phần đánh giá do Claude đọc và ghi lý do, đề xuất; tầng 3 là câu hỏi cho người đọc.

## B3. Chủ kênh đã chốt (18/11, 22:20)
- Duyệt có điều kiện, 7 nhóm giữ nguyên cấu trúc; chín chỉnh sửa trên đã đưa vào bản B. A3-a, b, e, f và A4 (tách Sengoku): đồng ý. A3-c: đồng ý có điều chỉnh (đã tách kỹ thuật khỏi văn phong). A3-d: năm viết bằng chữ ở `text`, số ở `hien`; nếu giọng đọc sai thì thử chữ số và kiểm bằng âm thanh thật.
- Còn lại: chủ kênh đọc bản hoàn chỉnh, rồi mới thay `giong-van.md`.

## B4. Bốn điểm kiểm lần cuối (22:23)
- Đã sửa theo đúng ba điểm đầu (mục 2, mục 4, mục 3) và giữ nguyên mục 6 như điểm 4.

## C. Điều đã bỏ khỏi bản gộp (để chủ kênh biết)
- Danh sách cụm cấm cứng ("Điều đáng chú ý là", "Có thể thấy", "Không chỉ… mà còn"…) và con số "không quá 5 lần", "không quá 1/10". Chuyển thành gợi ý ở bước biên tập.
- Khung hồ sơ vụ án và hướng dẫn tranh thủy mặc: sang `quy-tac/series/sengoku.md`.
- Các điều "ĐÃ BỎ" (05/11) và danh sách nới: sang `archive/quy-dinh-da-thay-the.md`.

## D. Chủ kênh duyệt giúp
1. Bản gộp ở mục B có giữ đúng các yêu cầu có giá trị chưa? Điều gì bị mất hoặc bị làm yếu?
2. A3-a đến A3-e: đồng ý với đề xuất từng điểm không? Riêng A3-d (năm bằng chữ hay chữ số) cần anh chọn.
3. Có tách `quy-tac/series/sengoku.md` như A4 không?
4. Sau khi duyệt, mình thay `giong-van.md` bằng bản gộp + mục "Diễn giải của người kể" giữ nguyên, chạy `tools/kiem_lien_ket.py`, rồi sang `dang-bai-va-bia.md`.
