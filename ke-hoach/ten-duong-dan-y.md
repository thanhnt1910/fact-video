# Series "Tên đường": dàn ý, phong cách hình ảnh, nguồn ảnh và kịch bản mẫu

Quy tắc nội dung: `quy-tac/ten-duong.md` (tiểu sử đơn giản, không giới hạn năm, có nguồn). Tài liệu này là kế hoạch làm series, chủ kênh duyệt trước khi dựng.

## 1. Mục tiêu và định dạng
- Mỗi video dọc 1080×1920, 60–100 giây, một nhân vật có tên đường. Một câu hỏi mở đầu gần gũi ("Con đường bạn đi hằng ngày mang tên ai?"), rồi tiểu sử theo thứ tự thời gian.
- Nội dung cố định mỗi video: **nguồn gốc → năm sinh → công danh theo thứ tự → năm mất → vì sao đường mang tên ông/bà** (chỉ khi chắc).
- Giọng Puck như các video khác; quy trình giọng đã chuẩn hóa (nghỉ đều, nhịp đều) dùng lại nguyên.

## 2. Phong cách hình ảnh KHÁC video lịch sử hiện tại
Hiện tại: nền giấy ấm, bảng đỏ nâu, đèn cầm thước, cảnh vẽ bằng code. Series này đổi sang cảm giác **bảng tên đường thật**:
- **Biển tên đường** làm trục thiết kế: nền xanh dương đậm (#0B4EA2), viền trắng bo góc, chữ trắng. Biển trượt vào ở giây đầu, ghi tên đường in hoa, dòng nhỏ bên dưới là danh hiệu và năm sinh–năm mất, đúng kiểu biển tên đường ở Việt Nam. Sau đó biển thu nhỏ lên góc trên.
- **Nền**: xanh than tối (#0E1A2B) với đường kẻ mảnh như bản vẽ quy hoạch, hoặc ảnh thật làm mờ; không dùng nền giấy kem.
- **Khung ảnh thật** ở giữa: ảnh tư liệu chuyển động chậm (zoom và lia nhẹ), viền trắng mỏng, góc dưới ghi nguồn ảnh bằng chữ nhỏ.
- **Dòng thời gian** dưới ảnh: thanh ngang có các mốc năm (sinh, các chức danh, mất) sáng dần khi đọc tới.
- **Phụ đề**: nền tối trong mờ ở dưới, chữ trắng, từ đang đọc tô vàng nhạt.
- **Nhân vật đèn**: đề xuất giữ nhỏ ở góc dưới như logo sống (không cầm thước), vì ảnh thật cần nhiều chỗ. Chủ kênh quyết (mục 7).
- **Font** (đều miễn phí, giấy phép SIL OFL, có đủ dấu tiếng Việt): biển tên đường dùng *Barlow Condensed* SemiBold; tiêu đề lớn dùng *Playfair Display* Bold; phụ đề và chữ nhỏ dùng *Be Vietnam Pro* (đã có trong repo). Phải tải đúng bản có tập ký tự tiếng Việt và kiểm bằng cách vẽ thử câu có đủ dấu ("Nguyễn Trãi, Lệ Chi Viên, Ức Trai") trước khi dựng.

## 3. Ảnh thật không bản quyền: quy trình
Chỉ dùng ảnh thuộc **phạm vi công cộng hoặc CC0**, hoặc CC BY (có ghi công trong video và mô tả). **Không dùng** CC BY-SA, NC, ND, ảnh "chỉ dùng cho giáo dục", ảnh báo chí, ảnh chụp tranh và tượng mới vẽ khi chưa rõ người vẽ và giấy phép.
Kho tìm ảnh:
1. **Wikimedia Commons** (giấy phép ghi rõ ở từng ảnh; lọc Public domain, CC0, CC BY). Ảnh tư liệu cũ (tranh khắc, bản đồ, ảnh chụp trước năm 1900) thường là phạm vi công cộng; phải đọc trang mô tả của từng ảnh.
2. **Thư viện số Pháp Gallica / Thư viện Quốc hội Mỹ / Thư viện Anh**: ảnh, bản khắc thời thuộc địa, tư liệu về Việt Nam, nhiều ảnh phạm vi công cộng; kiểm tra điều khoản từng thư viện.
3. **Bộ sưu tập mở của bảo tàng** (Metropolitan Museum Open Access, Rijksmuseum, Smithsonian: CC0): dùng làm ảnh minh họa phụ như thư pháp, đồ gốm, tranh sơn thủy Á Đông.
4. **Ảnh thực địa hiện nay** (đền thờ, tượng, di tích, biển tên đường): chỉ lấy loại CC0 hoặc CC BY; hoặc ảnh do chủ kênh tự chụp.
5. **Pexels, Unsplash**: ảnh phong cảnh, đường phố, dùng được tự do nhưng không phải CC0; chỉ dùng làm nền, không minh họa nhân vật.
Quy tắc bắt buộc:
- Mỗi ảnh ghi trong `ke-hoach/ten-duong-<tên>-anh.json`: link trang gốc, tác giả, giấy phép, ngày kiểm, và câu ghi nguồn hiển thị.
- **Chân dung**: nhiều tranh chân dung nhân vật cổ là tranh vẽ hiện đại (còn bản quyền họa sĩ) hoặc không có ảnh thật. Khi không có ảnh hợp lệ, dùng tượng đài hay đền thờ được phép dùng, bản khắc cũ, hoặc chân dung vẽ đơn giản bằng code (giống `assets/icon_nhan_vat/`), ghi rõ "tranh minh họa".
- Không cắt bỏ tên tác giả khỏi ảnh có yêu cầu ghi công; nguồn ảnh liệt kê trong mô tả video và bình luận ghim.
- **Ràng buộc kỹ thuật:** môi trường làm việc ở đây không tải được Wikimedia và các kho ảnh (mạng chỉ cho phép kho gói và GitHub). Việc tìm và tải ảnh phải chạy trong workflow GitHub Actions: gọi API Commons theo từ khóa, lọc theo giấy phép, lưu ảnh kèm tệp siêu dữ liệu vào nhánh, rồi mới soi từng ảnh ở cỡ lớn để chọn.

## 4. Khung kịch bản mỗi video (12–16 đoạn, mỗi đoạn 20–30 chữ)
1. **Mở**: câu hỏi hoặc tình huống đời thường quanh tên đường (không bịa chuyện).
2. **Biển tên đường**: "Đường X mang tên ông/bà X, người thế nào."
3. **Xuất thân**: quê quán, gia đình.
4. **Năm sinh**.
5–9. **Công danh theo thứ tự thời gian**, mỗi đoạn một mốc (khoa bảng, chức vụ, việc lớn, tác phẩm hoặc trận đánh).
10. **Năm mất** và hoàn cảnh (ngắn, trung tính).
11. **Sau khi mất**: truy tặng, danh hiệu, nơi thờ (chỉ dữ kiện chắc).
12. **Chốt**: một câu về con đường mang tên; một câu hỏi nhẹ để người xem bình luận ("Đường nào gần nhà bạn mang tên người nhắc trong video này?").
Quy tắc viết như các kịch bản khác: năm viết bằng chữ, họ tên đầy đủ, không từ cổ khó hiểu, không nói tắt, câu ngắn, kiểm bằng `kiem_kich_ban.py`.

## 5. Kịch bản mẫu: Nguyễn Trãi (nhãn độ chắc ở cuối mỗi đoạn, không đọc)
Nguồn đối chiếu trước khi đọc giọng: Đại Việt sử ký toàn thư (phần thời Hậu Lê sơ), Đại Việt thông sử, Khâm định Việt sử thông giám cương mục; năm tháng nào cũng phải dò lại ở ít nhất hai nguồn.

1. Đường Nguyễn Trãi có ở rất nhiều thành phố. Ông là ai mà tên được đặt cho nhiều con đường như vậy? [chắc: tên đường có ở nhiều nơi, cần liệt kê cụ thể nếu nêu số]
2. Nguyễn Trãi sinh năm một nghìn ba trăm tám mươi, tại kinh thành Thăng Long. [chắc]
3. Quê gốc của gia đình ông ở làng Chi Ngại, nay thuộc thành phố Chí Linh, tỉnh Hải Dương. [cần kiểm tên đơn vị hành chính hiện nay]
4. Cha ông là Nguyễn Phi Khanh, một người học giỏi. Mẹ ông là bà Trần Thị Thái, con quan Tư đồ Trần Nguyên Đán. [chắc: tên cha mẹ; cần kiểm chức Trần Nguyên Đán]
5. Năm một nghìn bốn trăm, ông thi đỗ Thái học sinh, tức học vị tiến sĩ ngày nay, dưới triều nhà Hồ. [chắc năm; cần kiểm cách giải thích "tương đương tiến sĩ"]
6. Ông ra làm quan với chức Ngự sử đài chánh chưởng, một chức trông coi việc kiểm tra, giám sát quan lại. [cần kiểm tên chức]
7. Năm một nghìn bốn trăm linh bảy, quân nhà Minh sang đánh nước ta, cha ông bị bắt đưa sang Trung Quốc. [chắc]
8. Sau đó ông tìm đến Lê Lợi ở Lam Sơn và trở thành người giúp Lê Lợi soạn thư từ, bàn mưu đánh giặc. [cần kiểm năm gặp Lê Lợi; không nêu năm trong lời kể]
9. Năm một nghìn bốn trăm hai mươi tám, ông soạn Bình Ngô đại cáo, bài cáo tuyên bố chiến thắng quân Minh và nước ta độc lập. [chắc]
10. Ông còn để lại nhiều tác phẩm như Quân trung từ mệnh tập, Quốc âm thi tập và Dư địa chí. [chắc tên tác phẩm; cần kiểm Dư địa chí có thuộc ông]
11. Năm một nghìn bốn trăm bốn mươi hai, vua Lê Thái Tông đột ngột qua đời ở Lệ Chi Viên, và Nguyễn Trãi bị kết tội, gia đình ông bị xử nặng. [chắc]
12. Hai mươi hai năm sau, năm một nghìn bốn trăm sáu mươi tư, vua Lê Thánh Tông minh oan cho ông. [chắc năm; kiểm lại "hai mươi hai năm"]
13. Năm một nghìn chín trăm tám mươi, tổ chức UNESCO của Liên Hợp Quốc vinh danh ông là Danh nhân văn hóa thế giới. [chắc: năm 1980 trong danh sách; cần kiểm cách gọi tên chính thức]
14. Vì những đóng góp ấy mà nhiều thành phố đặt tên ông cho một con đường. Đường Nguyễn Trãi ở gần nhà bạn nằm ở đâu? [câu hỏi cuối]

Ước lượng: khoảng 290–330 chữ, tức khoảng 95–105 giây giọng đọc. Rút còn 11–12 đoạn nếu muốn đủ 80 giây.
Ảnh gợi ý: biển tên đường thật (CC0 hoặc tự chụp), bản dập hoặc bản in cổ Bình Ngô đại cáo, ảnh đền Nguyễn Trãi ở Côn Sơn (chọn ảnh cho phép dùng), bản đồ cổ Thăng Long, chân dung vẽ đơn giản có ghi "tranh minh họa".

## 6. Danh sách nhân vật đề xuất làm trước (chỉ tên và thời kỳ; năm sinh, năm mất kiểm nguồn khi viết kịch bản)
- **Cổ trung đại:** Hai Bà Trưng, Ngô Quyền, Đinh Bộ Lĩnh, Lê Hoàn, Lý Thái Tổ (Lý Công Uẩn, đã có), Lý Thường Kiệt, Trần Hưng Đạo, Trần Nhân Tông, Chu Văn An, Lê Lợi, Nguyễn Trãi, Lê Thánh Tông, Lê Quý Đôn.
- **Cận đại:** Quang Trung (Nguyễn Huệ), Nguyễn Du, Nguyễn Đình Chiểu, Hoàng Diệu, Phan Đình Phùng.
- **Cuối thế kỷ 19 đến 20:** Phan Bội Châu, Phan Châu Trinh, Nguyễn Thái Học (dữ kiện chắc, trung tính theo quy tắc).
Thứ tự đề xuất theo mức quen thuộc của tên đường: Trần Hưng Đạo, Lê Lợi, Nguyễn Trãi, Lý Thường Kiệt, Nguyễn Huệ, Hai Bà Trưng.

## 7. Cần chủ kênh quyết trước khi dựng
1. Giữ nhân vật đèn (nhỏ, ở góc) hay bỏ hẳn?
2. Màu chủ đạo xanh biển tên đường (#0B4EA2) và nền xanh than, có đồng ý không?
3. Chấp nhận ảnh CC BY (ghi công tác giả trong video và mô tả) hay chỉ CC0 và phạm vi công cộng?
4. Chân dung nhân vật không có ảnh hợp lệ: dùng tranh vẽ đơn giản bằng code có ghi "tranh minh họa", có ổn không?
5. Độ dài mục tiêu: 60–80 giây hay 90–100 giây?

## 8. Việc kỹ thuật cần làm (theo thứ tự)
1. Workflow tìm ảnh Commons (lọc giấy phép, lưu siêu dữ liệu) và công cụ soi ảnh cỡ lớn.
2. Module dựng `phim_ban_do/tenduong.py`: biển tên đường, khung ảnh có zoom, thanh mốc thời gian, phụ đề mới; tái dùng `doc2.py` cho phần phụ đề và nhịp.
3. Tải và kiểm font có dấu tiếng Việt.
4. Làm thử một video (Nguyễn Trãi) để chủ kênh duyệt phong cách, sau đó mới nhân rộng.
