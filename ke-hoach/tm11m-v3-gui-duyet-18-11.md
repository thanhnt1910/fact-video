# tm11 MỚI, bản 3: kể kèm phân tích, không giới hạn chữ và câu (cổng C), 18/11/2026

**Trạng thái: CHỜ CHỦ KÊNH DUYỆT CỔNG C.** Chưa đọc giọng, chưa dựng. Bản 3 ở `ke-hoach/thu-giong-hai/tm11m_full.json` (đoạn 195001–195014). Bản 1 và 2 giữ ở `tm11m_v1_full.json`, `tm11m_v2_full.json`; tm11 cũ giữ nguyên.

Theo yêu cầu của anh: bỏ giới hạn 32 chữ và 2 câu, và kể kèm phân tích. 14 đoạn, 819 chữ, khoảng 4.1 phút (bản 2 chỉ 1,7 phút; mạch cổng B dự kiến 3 đến 4 phút).

## 0. Đã đổi trong quy tắc và bộ kiểm
- Bỏ 32 chữ và 2 câu ở `CLAUDE.md` mục 6, `nguyen-tac-cot-loi.md` mục 10, `giong-van.md`, `thuy-mac-khung.md`, `thuy-mac.md`; `kiem_kich_ban.py` không còn ❌ quá 32 chữ, ❌ quá 2 câu, ⚠️ dưới 12 chữ. Ghi ở `archive/quy-dinh-da-thay-the.md`.
- Thêm vào `giong-van.md`: kể lịch sử kèm phân tích, mỗi đoạn phân tích phải qua năm điều kiện diễn giải, và gửi duyệt phải kèm bảng phân tích (mục 3 dưới đây).
- **Rủi ro tôi phải nói rõ:** lý do cũ của giới hạn là giọng Gemini từng bỏ chữ ở đoạn dài. Bỏ giới hạn thì rủi ro ấy quay lại. Cách chặn: sau khi anh duyệt, kiểm giọng bằng nhận dạng không gợi ý; đoạn nào bị bỏ chữ thì ngắt đoạn đó, không rút ý. Tôi chưa chạy kiểm này.

## 1. Văn xuôi liền mạch

Có một viên tướng nuôi ba nghìn người làm con nuôi, rồi kéo quân ra lấy lại một tòa thành. Tòa thành ấy là Đại La, nay là Hà Nội. Muốn hiểu vì sao nó đáng giành lại thì phải bắt đầu từ họ Khúc, một dòng hào trưởng ở vùng Hải Dương bây giờ. Đầu thế kỷ mười, họ Khúc chiếm thành, xưng Tiết độ sứ, tức chức đứng đầu cả vùng, và nhà Đường công nhận. Người kế nghiệp là Khúc Hạo, và ông làm nhiều hơn là giữ thành. Theo nghiên cứu về vương triều họ Khúc, ông chia lại các lộ, phủ, châu, xã, định lại thuế ruộng cho đều, bỏ việc bắt dân đi lao dịch, và lập sổ ghi họ tên, quê quán từng người dân. Nhìn những việc ấy thì họ Khúc đang tự quản vùng đất này bằng sổ sách và thuế má của riêng mình, dù vẫn mang chức danh do nhà Đường công nhận. Họ Khúc giữ được ba đời. Đến người thứ ba là Khúc Thừa Mỹ, nhà Nam Hán, một nước ở vùng Quảng Đông bây giờ, đem quân sang, bắt ông đưa về Quảng Châu rồi chiếm thành. Các sách chép không thống nhất bắt ông năm nào, có sách ghi năm chín trăm hai mươi ba, có sách ghi năm chín trăm ba mươi. Vua Nam Hán đặt Lý Tiến làm thứ sử cai trị vùng này. Nói cách khác, quyền tự quản mà họ Khúc đã giữ không còn nữa. Nhưng ở Ái Châu, nay là Thanh Hóa, có một người chưa chịu.

Đó là Dương Đình Nghệ, từng làm tướng dưới thời Khúc Hạo, nghĩa là ông từng làm việc ngay dưới chế độ tự quản ấy. Ông nhận ba nghìn người làm con nuôi, cho họ luyện võ và chiêu mộ thêm hào kiệt khắp nơi. Sử không cho biết vì sao ông chọn cách nhận con nuôi, cũng không nói chính ba nghìn người ấy có ra trận hay không. Điều sử ghi là hai việc nối nhau: ông gây dựng lực lượng, rồi ông kéo quân ra bắc. Năm chín trăm ba mươi mốt, ông đem quân ra bắc vây thành Đại La. Lý Tiến không giữ nổi, bỏ thành chạy về nước. Khi quân Nam Hán do Trần Bảo chỉ huy kéo sang cứu thì thành đã đổi chủ. Trần Bảo vẫn cho quân vây chặt Đại La. Người vừa đi vây thành bỗng thành người bị vây. Dương Đình Nghệ đem quân từ trong thành đánh ra, giết chết Trần Bảo ngay tại trận. Hãy nhìn vị trí hai bên. Quân Nam Hán sang để cứu một thành còn của mình, nhưng đến nơi lại phải đánh vào một thành đã mất, trong khi đối phương có tường thành ở sau lưng. Sử chép rằng ông chọn đánh ra thay vì ngồi giữ thành; còn vì sao ông chọn như vậy thì các nguồn tôi đọc không nói. Sau chiến thắng ấy, ông tự xưng Tiết độ sứ, giữ cái chức mà họ Khúc từng giữ. Nhìn từ chức danh ấy thì ông chọn nối vào con đường họ Khúc đã đi, chứ chưa đặt ra một chức vị mới.

Sáu năm sau, tháng ba năm chín trăm ba mươi bảy, một người dưới quyền ông là Kiều Công Tiễn, hào trưởng vùng Phong Châu, đã giết ông để đoạt chức Tiết độ sứ. Chức vị từng đưa ông lên cũng chính là thứ khiến người dưới quyền ra tay. Ngô Quyền, con rể ông, từ năm chín trăm ba mươi bốn đã cai quản Ái Châu. Ông tập hợp lực lượng, kéo ra bắc đánh Kiều Công Tiễn. Có sách chép rằng Kiều Công Tiễn, thế cô, đã cầu cứu nhà Nam Hán; cũng có sách không chép chuyện này. Điều các nguồn đều nói là Ngô Quyền tiến đánh thành Đại La và diệt Kiều Công Tiễn. Nhà Nam Hán vẫn đem quân sang, đạo thủy quân do Lưu Hoằng Tháo chỉ huy. Ngô Quyền cho đóng cọc gỗ bịt sắt ở cửa sông Bạch Đằng. Khi thủy triều lên, cọc chìm dưới nước, thuyền địch theo nước tiến vào. Khi thủy triều rút, cọc nhô lên chặn đường, quân Đại Việt đánh từ hai bên bờ. Thuyền chiến của quân Nam Hán bị đánh đắm, Lưu Hoằng Tháo bị giết, vua Nam Hán phải rút quân. Hai trận đánh cách nhau bảy năm, một trận ở thành Đại La, một trận ở cửa sông Bạch Đằng, và cách đánh khác nhau. Nhưng cả hai kết thúc giống nhau: quân Nam Hán thua và viên tướng cầm quân bị giết. Sử không nói Ngô Quyền có học từ người cha vợ hay không. Chỉ biết rằng người đánh bại Nam Hán năm 931 và người đánh bại họ năm 938 là cha vợ và con rể.

## 2. Chia đoạn cho giọng đọc (ngắt theo nhịp kể, không theo số chữ)

**195001.** Có một viên tướng nuôi ba nghìn người làm con nuôi, rồi kéo quân ra lấy lại một tòa thành.

**195002.** Tòa thành ấy là Đại La, nay là Hà Nội. Muốn hiểu vì sao nó đáng giành lại thì phải bắt đầu từ họ Khúc, một dòng hào trưởng ở vùng Hải Dương bây giờ. Đầu thế kỷ mười, họ Khúc chiếm thành, xưng Tiết độ sứ, tức chức đứng đầu cả vùng, và nhà Đường công nhận.

**195003.** Người kế nghiệp là Khúc Hạo, và ông làm nhiều hơn là giữ thành. Theo nghiên cứu về vương triều họ Khúc, ông chia lại các lộ, phủ, châu, xã, định lại thuế ruộng cho đều, bỏ việc bắt dân đi lao dịch, và lập sổ ghi họ tên, quê quán từng người dân. Nhìn những việc ấy thì họ Khúc đang tự quản vùng đất này bằng sổ sách và thuế má của riêng mình, dù vẫn mang chức danh do nhà Đường công nhận.

**195004.** Họ Khúc giữ được ba đời. Đến người thứ ba là Khúc Thừa Mỹ, nhà Nam Hán, một nước ở vùng Quảng Đông bây giờ, đem quân sang, bắt ông đưa về Quảng Châu rồi chiếm thành. Các sách chép không thống nhất bắt ông năm nào, có sách ghi năm chín trăm hai mươi ba, có sách ghi năm chín trăm ba mươi.  
*(phụ đề: Họ Khúc giữ được ba đời. Đến người thứ ba là Khúc Thừa Mỹ, nhà Nam Hán, một nước ở vùng Quảng Đông bây giờ, đem quân sang, bắt ông đưa về Quảng Châu rồi chiếm thành. Các sách chép không thống nhất bắt ông năm nào, có sách ghi năm 923, có sách ghi năm 930.)*

**195005.** Vua Nam Hán đặt Lý Tiến làm thứ sử cai trị vùng này. Nói cách khác, quyền tự quản mà họ Khúc đã giữ không còn nữa. Nhưng ở Ái Châu, nay là Thanh Hóa, có một người chưa chịu.

**195006.** Đó là Dương Đình Nghệ, từng làm tướng dưới thời Khúc Hạo, nghĩa là ông từng làm việc ngay dưới chế độ tự quản ấy. Ông nhận ba nghìn người làm con nuôi, cho họ luyện võ và chiêu mộ thêm hào kiệt khắp nơi. Sử không cho biết vì sao ông chọn cách nhận con nuôi, cũng không nói chính ba nghìn người ấy có ra trận hay không. Điều sử ghi là hai việc nối nhau: ông gây dựng lực lượng, rồi ông kéo quân ra bắc.

**195007.** Năm chín trăm ba mươi mốt, ông đem quân ra bắc vây thành Đại La. Lý Tiến không giữ nổi, bỏ thành chạy về nước. Khi quân Nam Hán do Trần Bảo chỉ huy kéo sang cứu thì thành đã đổi chủ.  
*(phụ đề: Năm 931, ông đem quân ra bắc vây thành Đại La. Lý Tiến không giữ nổi, bỏ thành chạy về nước. Khi quân Nam Hán do Trần Bảo chỉ huy kéo sang cứu thì thành đã đổi chủ.)*

**195008.** Trần Bảo vẫn cho quân vây chặt Đại La. Người vừa đi vây thành bỗng thành người bị vây. Dương Đình Nghệ đem quân từ trong thành đánh ra, giết chết Trần Bảo ngay tại trận.

**195009.** Hãy nhìn vị trí hai bên. Quân Nam Hán sang để cứu một thành còn của mình, nhưng đến nơi lại phải đánh vào một thành đã mất, trong khi đối phương có tường thành ở sau lưng. Sử chép rằng ông chọn đánh ra thay vì ngồi giữ thành; còn vì sao ông chọn như vậy thì các nguồn tôi đọc không nói.

**195010.** Sau chiến thắng ấy, ông tự xưng Tiết độ sứ, giữ cái chức mà họ Khúc từng giữ. Nhìn từ chức danh ấy thì ông chọn nối vào con đường họ Khúc đã đi, chứ chưa đặt ra một chức vị mới.

**195011.** Sáu năm sau, tháng ba năm chín trăm ba mươi bảy, một người dưới quyền ông là Kiều Công Tiễn, hào trưởng vùng Phong Châu, đã giết ông để đoạt chức Tiết độ sứ. Chức vị từng đưa ông lên cũng chính là thứ khiến người dưới quyền ra tay.  
*(phụ đề: Sáu năm sau, tháng 3 năm 937, một người dưới quyền ông là Kiều Công Tiễn, hào trưởng vùng Phong Châu, đã giết ông để đoạt chức Tiết độ sứ. Chức vị từng đưa ông lên cũng chính là thứ khiến người dưới quyền ra tay.)*

**195012.** Ngô Quyền, con rể ông, từ năm chín trăm ba mươi bốn đã cai quản Ái Châu. Ông tập hợp lực lượng, kéo ra bắc đánh Kiều Công Tiễn. Có sách chép rằng Kiều Công Tiễn, thế cô, đã cầu cứu nhà Nam Hán; cũng có sách không chép chuyện này. Điều các nguồn đều nói là Ngô Quyền tiến đánh thành Đại La và diệt Kiều Công Tiễn.  
*(phụ đề: Ngô Quyền, con rể ông, từ năm 934 đã cai quản Ái Châu. Ông tập hợp lực lượng, kéo ra bắc đánh Kiều Công Tiễn. Có sách chép rằng Kiều Công Tiễn, thế cô, đã cầu cứu nhà Nam Hán; cũng có sách không chép chuyện này. Điều các nguồn đều nói là Ngô Quyền tiến đánh thành Đại La và diệt Kiều Công Tiễn.)*

**195013.** Nhà Nam Hán vẫn đem quân sang, đạo thủy quân do Lưu Hoằng Tháo chỉ huy. Ngô Quyền cho đóng cọc gỗ bịt sắt ở cửa sông Bạch Đằng. Khi thủy triều lên, cọc chìm dưới nước, thuyền địch theo nước tiến vào. Khi thủy triều rút, cọc nhô lên chặn đường, quân Đại Việt đánh từ hai bên bờ. Thuyền chiến của quân Nam Hán bị đánh đắm, Lưu Hoằng Tháo bị giết, vua Nam Hán phải rút quân.

**195014.** Hai trận đánh cách nhau bảy năm, một trận ở thành Đại La, một trận ở cửa sông Bạch Đằng, và cách đánh khác nhau. Nhưng cả hai kết thúc giống nhau: quân Nam Hán thua và viên tướng cầm quân bị giết. Sử không nói Ngô Quyền có học từ người cha vợ hay không. Chỉ biết rằng người đánh bại Nam Hán năm 931 và người đánh bại họ năm 938 là cha vợ và con rể.

## 3. Bảng phân tích (năm điều kiện của người kể)
| Đoạn | Câu phân tích | Dựa vào sự việc nào (đã kể trong video, có nguồn) | Rào đón và giới hạn |
|---|---|---|---|
| 195003 | "họ Khúc đang tự quản vùng đất này bằng sổ sách và thuế má của riêng mình" | Các cải cách của Khúc Hạo (N1) | "Nhìn những việc ấy thì"; không nói họ Khúc chống nhà Đường, vì họ vẫn mang chức do Đường công nhận |
| 195004 | Các sách không thống nhất năm bị bắt (923 hay 930) | N1, N2 | Nêu đúng cả hai số, không chọn |
| 195005 | "quyền tự quản mà họ Khúc đã giữ không còn nữa" | Nam Hán chiếm thành, đặt thứ sử (N1, N2, N3) | Hệ quả trực tiếp của việc đặt quan cai trị, không thêm ý đồ |
| 195006 | "ông từng làm việc ngay dưới chế độ tự quản ấy"; sử không nói vì sao nhận con nuôi, không nói ba nghìn người có ra trận | Dương Đình Nghệ là tướng dưới Khúc Hạo (N1, N5, N6) | Nói thẳng chỗ sử không ghi; không gán động cơ, không nối ba nghìn người với trận đánh (lỗi của bản 1) |
| 195008 | Vị trí hai bên đảo ngược, đối phương có tường thành sau lưng; vì sao ông chọn đánh ra thì nguồn không nói | Thành đã đổi chủ trước khi viện binh tới; ông đánh từ trong thành ra (N5, N6, N3) | Chỉ mô tả vị trí; không nói đó là nguyên nhân thắng; ghi nguồn không nói lý do |
| 195009 | Ông nối vào đường họ Khúc đã đi, chưa đặt chức vị mới | Tự xưng Tiết độ sứ, chức họ Khúc từng giữ (N2, N4, N5, N6) | "Nhìn từ chức danh ấy thì"; không nói ông có ý định hay không có ý định xưng vương |
| 195010 | "Chức vị từng đưa ông lên cũng chính là thứ khiến người dưới quyền ra tay" | Kiều Công Tiễn giết ông để đoạt chức Tiết độ sứ (N4, Nhân dân) | Chỉ lặp lại mục đích mà nguồn ghi |
| 195014 | Hai trận khác cách đánh nhưng kết thúc giống nhau; sử không nói Ngô Quyền có học từ cha vợ; chỉ biết hai người là cha vợ và con rể | Trần Bảo bị giết 931; Hoằng Tháo bị giết 938; quan hệ cha vợ con rể (N4, N5, N6, Nhân dân) | So sánh hai sự việc có nguồn, nói rõ sử không xác nhận quan hệ học hỏi; không nói trận 931 "dẫn đến" Bạch Đằng |

Phân tích này khác câu kết của bản 1 ("con đường ra bắc ấy đã được người cha vợ mở sẵn…"): bản 1 nối nhân quả mà nguồn không nói; bản 3 nói thẳng rằng sử không xác nhận.

## 4. Bảng nguồn từng dữ kiện mới và dữ kiện giữ lại
Mã nguồn: N1 Trần Hữu Thắng (IUH 2025); N2 Tia Sáng; N3 hoduongvietnam.com.vn; N4 giaoduc.net.vn; N5 nguoikesu.com; N6 chonthieng.com; N7 nhandan.vn "Ngô Quyền và chiến thắng Bạch Đằng lịch sử"; N8 vjol.info.vn/tctbgd/article/download/105537 (tạp chí Giáo dục, lời bình Lê Văn Hưu). Chưa mở bản gốc Toàn thư, Khâm định, Tư trị thông giám, nên lời kể không gắn tên sách.

| Đoạn | Dữ kiện | Nguồn | Kết luận |
|---|---|---|---|
| 195001–195002 | Như bản 2: ba nghìn con nuôi; Đại La nay là Hà Nội; họ Khúc ở vùng Hải Dương; đầu thế kỷ mười xưng Tiết độ sứ, Đường công nhận | N1, N2, N3, N5, N6 | Đủ (xem bảng bản 2) |
| 195003 | Khúc Hạo kế nghiệp cha | N1 (907 kế vị) | Một nguồn đọc được, kết luận chung được N2, N3 xác nhận ba đời họ Khúc |
| 195003 | Chia lại lộ, phủ, châu, xã; bình quân thuế ruộng; bỏ lực dịch; lập sổ họ tên, quê quán | **Chỉ N1** (qua Khâm định) | Một nguồn, đã nói đúng mức: lời kể ghi "Theo nghiên cứu về vương triều họ Khúc". Cần anh biết: không mở được nguồn thứ hai. Nếu anh muốn chắc hơn, tôi bỏ dòng này hoặc tra thêm |
| 195004 | Bị đưa về Quảng Châu | N1 (Toàn thư, Khâm định) | Một nguồn đọc được |
| 195004 | Năm bị bắt 923 hay 930 | N1, N2 | Nêu cả hai |
| 195004 | Nam Hán ở vùng Quảng Đông | Phổ thông; Quảng Châu là kinh đô Nam Hán | Chấp nhận |
| 195005–195007 | Như bản 2 (Lý Tiến, Ái Châu, tướng của Khúc Hạo, con nuôi, 931, Trần Bảo, giết tại trận) | N1–N6 | Đủ (xem bảng bản 2) |
| 195009 | Tự xưng Tiết độ sứ sau chiến thắng | N2, N4, N5, N6 | Đủ |
| 195010 | Tháng 3/937; Kiều Công Tiễn giết ông; mục đích đoạt chức Tiết độ sứ | N4, N7, N5, N6 | Đủ |
| 195010 | Kiều Công Tiễn là hào trưởng vùng Phong Châu | N4, N7 | Đủ |
| 195011 | Ngô Quyền con rể, cai quản Ái Châu từ 934 | N4 (934); con rể N4, N5, N6 | Năm 934 chỉ N4: một nguồn, giữ vì khớp với việc ông ở Ái Châu |
| 195011 | Ngô Quyền tiến đánh Đại La, diệt Kiều Công Tiễn | N4, N7, N8 | Đủ |
| 195011 | Kiều cầu cứu Nam Hán | N4, N6 có; N5 ghi không có; N7 không nói ai mời | **Lệch giữa nguồn**, lời kể nói rõ "có sách chép… cũng có sách không chép" |
| 195012 | Thủy quân Nam Hán do Lưu Hoằng Tháo chỉ huy | N4, N7, N8 | Đủ |
| 195012 | Cọc gỗ bịt sắt ở cửa sông Bạch Đằng; thủy triều lên cọc chìm, triều rút cọc nhô lên chặn thuyền | N4, N7 | Đủ |
| 195012 | Thuyền Nam Hán bị đánh đắm; Hoằng Tháo bị giết; vua Nam Hán rút quân | N4, N7 | Đủ. N4 viết "bắt được đem giết", N7 viết "chết tại trận": lời kể chỉ nói "bị giết" |
| 195012 | Quân Đại Việt đánh từ hai bên bờ | N7 (quân mai phục hai bên bờ và các nhánh sông); N4 (nhiều hướng) | Đủ |
| 195013 | Trận 938 (năm) | N4, N7, N8 | Đủ. Ngày chính xác các sử ghi khác nhau (N7), lời kể không nêu ngày |
| 195013 | Hai trận cách nhau bảy năm | 931 và 938 | Phép trừ |

**Điểm lệch giữa nguồn** (thêm so với cổng B): (a) Kiều Công Tiễn cầu cứu Nam Hán (N4, N6 có; N5 không; N7 không nêu); (b) N1 ghi Dương Đình Nghệ đuổi đánh Lý Khắc Chinh, trong khi N3, N5, N6 nêu Lý Tiến: lời kể dùng Lý Tiến như cổng B và không nhắc Lý Khắc Chinh; (c) năm khởi đầu họ Khúc 905, 906, 907 (N1): lời kể chỉ nói "đầu thế kỷ mười"; (d) như cổng B: 923/930, Trần/Trình Bảo, Ngô Quyền ở trận 931, 905/906.

**Chi tiết đã bỏ ở bản 3:** treo đầu Kiều Công Tiễn (chỉ N4, và nặng nề); vua Nam Hán đóng ở Hải Môn, Tiêu Ích can ngăn, đổ tội cho Trước tác Tá Lang hầu Dung (một nguồn mỗi chi tiết); Ngô Quyền xưng vương, đóng đô Cổ Loa (chỉ N7, và là chuyện của video sau); Khúc Thừa Mỹ sang Quảng Châu dò xét (chỉ N1); trường đấu vật (một nguồn thứ cấp).

## 5. Kết quả bộ kiểm
- `kiem_kich_ban`: 0 ❌, 11 ⚠️ (dấu phẩy nhiều và chữ số ở phụ đề, vì đoạn dài hơn; chữ số chỉ nằm ở trường `hien`, trường `text` là chữ).
- `kiem_giong_van`: 0 ❌, 0 ⚠️. `kiem_khung`: không có khung, bỏ qua (không có nghĩa là đạt).
- `kiem_mach_ke`: 0 ❌, 9 ⚠️: ít từ nối đầu đoạn; nhiều tên riêng ở các đoạn 195002, 195004, 195005, 195011, 195012, 195013; hai con số ở 195004, 195010, 195013. Tôi giữ nguyên vì tên đều cần cho người nghe; nếu anh thấy dày thì tôi bớt Hải Dương, Quảng Đông.
- `kiem_mo_dau`: ⚠️ 5 tên riêng mới trong 25 giây đầu (Hà Nội, Khúc, Hải Dương, Tiết độ sứ, Đường). Hook chỉ 20 chữ, không năm, không tên riêng.
- Lỗi tôi đã sửa sau khi chạy kiểm: "triều rút" thành "thủy triều rút"; "Hoằng Tháo" thành "Lưu Hoằng Tháo".

## 6. Tự rà (đọc thành tiếng, theo `giong-van.md`)
- Không gán ý nghĩ hay lời nói cho nhân vật; không động cơ ngoài điều nguồn ghi (Kiều Công Tiễn đoạt chức).
- Mọi phân tích có bảng ở mục 3, mỗi chỗ sử không nói đều được nói thẳng.
- Chỗ tôi còn lo: (a) đoạn 195003 và 195012 dày thông tin, có thể nặng khi nghe; (b) phần Bạch Đằng ở 195012 chồng với video riêng về Bạch Đằng (bd2), tôi để ngắn; (c) cải cách Khúc Hạo chỉ một nguồn.
- Câu hỏi tầng 3: hook cụ thể; chi tiết đáng nhớ là thành đổi chủ trước khi viện binh tới và chuyện người vây thành thành người bị vây; nhịp căng ở 195007 đến 195008; kết bằng so sánh hai trận chứ không bằng lời cảm ơn.

## 7. Cần chủ kênh duyệt
1. Độ dài khoảng 4.1 phút và mức phân tích này có đúng ý anh chưa? Nhiều hơn hay ít hơn?
2. Cải cách Khúc Hạo (một nguồn): giữ hay bỏ?
3. Phần Bạch Đằng (195012) có để trong video này không, hay chỉ nhắc một câu?
4. Duyệt xong tôi sẽ chạy kiểm giọng nhận dạng để xem đoạn dài có bị bỏ chữ không.
