# Dựng mạch truyện, mở đầu, sáng tạo cách kể

> Chuyển nguyên văn từ CLAUDE.md, chờ gộp. Mục 'Độ dài và kết' viết mới ở đầu file. Nguồn: `archive/CLAUDE-truoc-tai-cau-truc-18-11.md`. Chuyển ngày 18/11/2026.

## Độ dài và câu kết (chủ kênh quyết 18/11/2026, thay sàn 10 phút và câu "tập sau" mặc định)

- **Không có sàn thời lượng hay số chữ.** Độ dài do chất liệu của câu chuyện quyết định. Chuyện chỉ đủ 6–7 phút thì làm 6–7 phút, không kéo bằng đoạn giải thích hay nhắc lại. Con số cũ (10 phút, 1.900 chữ, 70–90 beat; video dọc 60–80 giây) chỉ là mức tham khảo khi lên kế hoạch. Video quá ngắn so với chất liệu thì mới cần xem lại xem còn thiếu mạch nào.
- `review.py` không còn chặn ❌ theo thời lượng; chỉ báo ⚠️ khi video ngắn bất thường để chủ kênh biết.
- **Mỗi video tự hoàn chỉnh.** Không có câu kết mặc định "Tập sau sẽ kể tiếp" hay "Hẹn bạn ở tập tiếp theo". Chỉ mời xem tập sau khi hai tập thật sự nối tiếp và lời mời có giá trị với người xem; khi đó ghi lý do trong bản gửi duyệt.
- Đoạn cuối theo nguyên tắc cốt lõi (`nguyen-tac-cot-loi.md`).


## Khung 6 câu hỏi để xây kịch bản, rồi chia đoạn (chủ kênh yêu cầu 06/11/2026, áp dụng mọi kịch bản từ nay)
Trước khi viết lời kể, trả lời đủ 6 câu hỏi dưới đây cho chủ đề của video; sau đó mới chia thành các đoạn nội dung. **Mỗi đoạn chỉ giải quyết MỘT ý chính** (một câu hỏi, hoặc một phần của một câu hỏi).

| # | Câu hỏi | Nội dung cần có |
|---|---------|-----------------|
| 1 | Chuyện gì xảy ra? | Sự kiện lịch sử trung tâm, nói gọn một hai câu |
| 2 | Xảy ra khi nào, ở đâu? | Niên đại, địa danh (kèm vị trí ngày nay nếu giúp người nghe hình dung) |
| 3 | Vì sao xảy ra? | Nguyên nhân trực tiếp và nguyên nhân sâu xa |
| 4 | Ai tham gia? | Nhân vật, thế lực, vai trò của từng bên |
| 5 | Kết quả thế nào? | Thắng bại, thay đổi sau sự kiện |
| 6 | Có ý nghĩa gì? | Tác động và đánh giá lịch sử |

Cách áp dụng:
- **Bước 1, lập khung:** ghi ra 6 câu trả lời (mỗi câu vài ý, kèm nguồn) vào đầu file kịch bản, mục "Khung 6 câu hỏi". Câu nào chưa có nguồn thì nói rõ "còn tranh cãi" hoặc bỏ, không bịa cho đủ.
- **Bước 2, chia đoạn:** mỗi ý trong khung thành một đoạn (20–30 chữ, tối đa 32, tối đa 2 câu). Đoạn nào chứa hai ý thì tách; ý nào cần nhiều câu thì thành nhiều đoạn liên tiếp, mỗi đoạn một ý nhỏ.
- **Bước 3, sắp thứ tự:** mở bằng điểm gây tò mò lấy từ câu 1 hoặc 5 (đúng quy tắc "cảnh mở đầu là sự kiện có thật"), rồi đi theo thứ tự thời gian và nguyên nhân – kết quả: 2 → 3 → 4 → diễn biến (1) → 5 → 6. Có thể đảo thứ tự TRÌNH BÀY ở phần mở, không đảo quan hệ nguyên nhân – kết quả.
- **Câu 6 (ý nghĩa, đánh giá):** chỉ dùng lời của sử gia có tên (Lê Văn Hưu, Ngô Sĩ Liên, hoặc tác giả bộ sử đã chốt làm nguồn). Lời đánh giá của kênh không đặt vào lời kể; muốn giữ thì để ở mô tả hoặc bình luận ghim. Không thêm câu "điều này cho thấy…" do kênh tự rút ra (xem các điểm đã gặp ở tập 2, 3).
- **Tự kiểm trước khi đọc giọng:** lập bảng đoạn → câu hỏi (1–6) nó trả lời. Đoạn nào không thuộc câu hỏi nào thì bỏ hoặc gộp; câu hỏi nào không có đoạn nào thì bổ sung hoặc ghi lý do bỏ. Ghi bảng này vào mục "Ghi chú độ chắc" để chủ kênh duyệt.
- **Video dọc ngắn:** vẫn dùng khung, nhưng chỉ chọn câu 1, 2 và một trong 3 hoặc 5 làm trục; các câu còn lại nằm ở phần mô tả hoặc ở video khác trong loạt.
- Khung này bổ sung, không thay thế các quy tắc về nguồn, giọng kể, bố cục cuốn hút, họ tên đủ và đoạn ngắn cho giọng đọc ở các mục trên.

## Kịch bản "Bí mật biểu tượng": xương sống là MẠCH KỂ (chủ kênh duyệt 10/11/2026; thay "6 câu hỏi" làm xương sống cho loạt này; skill `viet-kich-ban-bi-mat-bieu-tuong` là nơi gom quy tắc hiện hành)
- **Mạch kể:** hook đặt MỘT câu hỏi; mỗi đoạn trả lời hoặc đẩy tiếp câu hỏi của đoạn trước (nối bằng "nên", "nhưng", "thế là", "vậy thì…"); rồi bước ngoặt, câu trả lời, câu hỏi mở cuối gắn với chính căng thẳng của video (không "Bạn nghĩ…?" mãi). 6 câu hỏi cũ chỉ là danh sách kiểm đủ ý.
- **Hook** tối đa khoảng 20 chữ, không năm, không tên lạ; bối cảnh dồn sang đoạn 2.
- **Mỗi đoạn một ý lớn, tối đa một con số/năm.** Số ý và độ dài video theo nhu cầu giải thích của từng chủ đề, không giới hạn 5–7 ý (chủ kênh bỏ ngày 11/11/2026: người xem chưa biết gì phải hiểu được; chỉ giữ giới hạn mỗi đoạn). Trích nguồn tối đa 2 lần, mỗi lần một tầng ("Theo UNESCO, …"); nguồn còn lại ở mô tả và bình luận ghim.
- **Đọc to:** câu nào phải đọc hai lần thì viết lại; hai đoạn liền không mở cùng một chữ; câu kết thay đổi theo video.
- **Công cụ trước khi gửi duyệt:** `kiem_kich_ban.py`, `kiem_mo_dau.py`, `kiem_mach_ke.py <mã>` (đo hook, tỷ lệ đoạn mở bằng từ nối, chuỗi cùng chữ mở, số lần "Theo", đoạn ≥2 con số, đoạn ≥4 tên riêng). ❌ phải sửa.
- Lộ trình `ke-hoach/bi-mat-bieu-tuong-lo-trinh-30-video.md` đã dọn: giọng Leda, bỏ giới hạn 1858, độ dài tự do, bỏ nhãn "[kiểm]" (tra nguồn từng video khi viết).

## Bố cục video cuốn hút: giữ người lạ trong 3 giây đầu và 3 phút đầu (chủ kênh yêu cầu 24/10/2026, áp dụng mọi video từ nay; rút từ số liệu bài Ngô Quyền)
Số liệu video Ngô Quyền (12 phút 57 giây, Facebook): 559 lượt xem, chỉ 21% xem đủ 3 giây, 4% xem quá 1 phút, thời gian xem trung bình 51 giây, 81% người xem chưa theo dõi kênh. Người lạ bỏ đi ngay từ đầu; ai ở lại thì xem khá lâu. Vì vậy bố cục phải thắng ở phần mở đầu.
- **Giây 0–3:** có hình hoặc cảnh gây tò mò và một dòng chữ lớn (video hay tự phát không tiếng). Câu đầu tiên nên ngắn gọn (giới hạn 15 chữ đã bỏ 05/11/2026), không ngày tháng, không tên nước hay tên người lạ. Mẫu tốt: cảnh người cha nhìn con bị treo trên sào (Đinh Bộ Lĩnh).
- **Mở đầu tối đa 40 giây, không lộ đáp án.** Chỉ đặt câu hỏi, chưa nói cách giải (Ngô Quyền đã nói "thủy triều lên rồi sẽ rút" ngay đoạn 4 nên người xem thấy không cần xem tiếp). Không đặt câu giới thiệu nguồn hay lời rào đón ở đoạn đầu; nguồn để ở mô tả và bình luận ghim, hoặc một câu ngắn sau phút đầu.
- **Nhân vật chính và xung đột chính xuất hiện trước 1 phút 30 giây.** Phần bối cảnh trước đó tối đa 2 phút, chỉ giữ điều người nghe cần để hiểu xung đột; mỗi chương dẫn nhập tối đa 4 tên riêng mới. Danh sách tên, chức quan, số quân thì rút gọn hoặc đưa vào bản đồ và chữ trên màn hình.
- **Điểm hấp dẫn nhất (kế sách, trận đánh, bước ngoặt) phải bắt đầu trước 45% thời lượng video**, không để sau phút thứ 8 của video 13 phút.
- **Mỗi 60–90 giây có một "móc" mới:** một câu hỏi, một bước ngoặt, một cảnh hay hình mới. Cuối mỗi chương nêu việc sắp xảy ra hoặc câu hỏi dẫn sang chương sau.
- **Đổi giọng theo chương:** căng ở xung đột và trận đánh, trầm ở mất mát, sáng ở thắng lợi; không để cả video một tone (video Ngô Quyền cả 119 đoạn đều tone "calm").
- **Ảnh bìa:** một người hoặc một cảnh cụ thể, tối đa 4 chữ lớn, có logo kênh. Câu trên ảnh bìa là câu hỏi hoặc điều gây tò mò, không đặt tên chương.
- **Mỗi video dài có kèm một video dọc 60–80 giây** cắt từ cảnh gây tò mò nhất, kết bằng lời mời xem bản đầy đủ. Đây là đường chính kéo người lạ vào kênh.
- **Ghi chú tranh cãi, so sánh nguồn không nằm trong lời kể** mà ở mô tả và bình luận ghim (khớp mục kể liền mạch ở trên).
- **Tự kiểm trước khi đọc giọng:** in bảng thời điểm bắt đầu từng chương (tính theo số chữ chia 3 mỗi giây) và kiểm các điểm trên. Ghi kết quả vào mục "Ghi chú độ chắc" của kịch bản để chủ kênh duyệt.
- **Sau khi đăng, ghi lại số liệu (chủ kênh gửi ảnh Insights hoặc kết nối Metricool):** tỷ lệ xem đủ 3 giây, thời gian xem trung bình, tỷ lệ giữ chân ở 1 phút và ở giữa video. Mức tham chiếu của kênh hiện tại là 21% xem đủ 3 giây và 51 giây xem trung bình (Ngô Quyền); đặt mục tiêu cao hơn mức này ở video sau rồi chỉnh theo số liệu.

## Hook "lật lại điều ai cũng tưởng": thử nghiệm cho video từ #16 (chủ kênh chốt 10/11/2026; KHÔNG làm lại video đã làm)
Số liệu 8–9/11: video "Tên nước Việt Nam suýt là Nam Việt?" đạt 5.051 lượt xem Facebook, gấp 4–8 lần các video cùng ngày (620–1.417). Chưa biết chắc hook là nguyên nhân, nên đây là THỬ NGHIỆM, không phải luật.
- **Áp dụng cho kịch bản mới từ #16 trở đi.** Video đã làm (#01–#15) giữ nguyên, kể cả #09, #10, #13, #14 có hook yếu hơn (chủ kênh không cho sửa).
- **Câu mở "Bạn có biết, …?" ưu tiên kiểu lật lại:** (1) đánh vào điều quen thuộc với người xem (tên nước, tiền, công trình, vật nổi tiếng); (2) có điểm đảo ngược hoặc "suýt nữa thì khác" ("suýt là", "không phải như nhiều người nghĩ", "nhưng hóa ra"); (3) có tác nhân rõ (một người, một quyết định) thay vì chỉ nêu sự thật. Câu mở không quá khoảng 25 chữ, không năm tháng, không chi tiết phụ (tránh kiểu #14 Rosetta mở dài).
- **Tiêu đề đăng giữ cùng công thức**, dạng câu hỏi ngắn gây sốc ("Cầu Long Biên có phải của Eiffel?"), vẫn đúng sự thật, không giật tít sai.
- **Chủ đề không có điểm đảo ngược thật thì không bịa cho có**: dùng hook hỏi một điều lạ nhất có nguồn; nhưng khi chọn chủ đề mới, ưu tiên chủ đề có sẵn điểm lật lại.
- **Theo dõi:** sau 24 giờ của mỗi video, lấy số liệu Metricool (lượt xem, like, thời gian xem trung bình Facebook; lượt xem, like TikTok) và ghi vào cột so sánh "hook lật lại" với "hook thường". Bốn video mẫu để so: Nam Việt 5.051 xem/14 like/18 s; Trống đồng 620/5/12 s; Cổ Loa 1.417/10/20 s; Bạch Đằng 673/5/18 s. Đủ ít nhất 4–5 video mới mới kết luận; nếu hook lật lại không hơn thì bỏ quy tắc này.

## Sáng tạo cho đỡ nhàm, nhưng không đổi cốt truyện chính (chủ kênh yêu cầu 24/10/2026, áp dụng mọi video từ nay)
Sử chép khô dễ làm video nhàm. Được phép sáng tạo ở CÁCH KỂ, không được sáng tạo ở NỘI DUNG sử.
- **Được:** mở đầu bằng một cảnh gây tò mò rồi mới kể từ đầu; đảo thứ tự TRÌNH BÀY (nhưng phần thân vẫn đi đúng thứ tự thời gian và nguyên nhân – kết quả); rút gọn chương khô (danh sách chức quan, số quân, chế độ) còn các việc lớn; dồn chất liệu có nguồn vào cảnh xung đột; dùng bản đồ động, hiệu ứng, nhịp đổi cảnh, khung đùa nhẹ về tình huống hoặc quân xâm lược; câu hỏi gợi mở dẫn vào chương.
- **Không được:** đổi, thêm hay bỏ sự kiện chính; đổi kết cục, người thắng thua, nguyên nhân; bịa lời thoại, nội tâm, nhân vật; kể truyền thuyết như sự thật; đảo ngược quan hệ nguyên nhân – kết quả; dùng lời "kết luận" của mình thay cho lời sử (lời bàn phải là của sử gia có tên, ví dụ Lê Văn Hưu, Ngô Sĩ Liên).
- **Cảnh mở đầu gây tò mò phải là sự kiện có thật trong chính video**, sẽ được kể đầy đủ ở chương của nó (không dựng cảnh mở đầu riêng không có trong sử). Phần sáng tạo phải ghi trong kịch bản, mục "Ghi chú độ chắc", để chủ kênh duyệt.
- Mỗi video vẫn trọn gói một chủ đề, không nối sang video khác (chủ kênh 24/10/2026): không có "tập sau", chỉ kết bằng kết cục của chính câu chuyện.
- Video sử Việt vẫn tuân thủ mục "Series lịch sử Việt Nam": hài chỉ nhắm vào tình huống và quân xâm lược, không đùa anh hùng dân tộc.
- Mẫu: `ke-hoach/dinh-bo-linh-kich-ban.md` (mở đầu bằng cảnh Đinh Liễn bị treo trên sào, chương lập triều đình rút gọn).
