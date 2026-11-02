# Bảng phân cảnh: Tào Tháo thật sự ác đến mức nào, theo chính sử? (bản nháp để chủ kênh duyệt, 02/11/2026)

Dựa trên kịch bản hiện tại (187 câu, khoảng 4.400 chữ, 24 phút) và tỷ lệ hình ảnh chủ kênh chọn: 50% nhân vật và sự kiện, 25% cảnh không gian, 15% bản đồ và sơ đồ, 10% tư liệu và chữ. Mỗi câu một hình (khóa hình = số câu).

## Số lượng

| Loại | Số câu | Tỷ lệ | Mục tiêu |
|---|---|---|---|
| A. Nhân vật và sự kiện | 97 | 52% | 50% |
| B. Cảnh không gian | 47 | 25% | 25% |
| C. Bản đồ và sơ đồ | 28 | 15% | 15% |
| D. Thẻ tư liệu và chữ | 15 | 8% | 10% |

- Tổng ảnh vẽ AI: 144 (nhóm A và B). Ảnh bản đồ và sơ đồ: 28. Thẻ chữ vẽ bằng code: 15.
- Clip Veo (ảnh sang video, chỉ cảnh có người di chuyển): 23 clip (mức sàn 20). Câu: 18, 30, 37, 40, 42, 44, 45, 48, 50, 52, 56, 57, 61, 70, 73, 78, 82, 113, 126, 139, 157, 167, 171.
- Cảnh hoạt hình nhẹ bằng `anim_nhe.py` (cảnh vắng người, chỉ khói, nước, cờ, đèn chuyển động nhẹ): 47 cảnh, cần `ke-hoach/nhan-vat/<MÃ>_nhe.json`.
- Ảnh tĩnh (người đứng yên hoặc tương tác tay, không làm clip): 74 ảnh nhóm A.

## Quy ước cho từng loại

- **A và B (ảnh AI):** đúng thời Hán, không máu, không cảnh chém giết (Từ Châu, chôn sống, Phục hoàng hậu, Hoa Đà vẽ gợi bằng khói, đường vắng, cổng đóng), không chữ trên ảnh, Tào Tháo tay không, mỗi người tối đa một kiếm, không hai người giống hệt nhau. Cảnh B vắng người ghi "completely empty, absolutely no people". Mỗi cảnh Tào Tháo một mình ghi "exactly ONE man only".
- **Veo (V):** prompt không có tên riêng ("the foreground man", "the officer"); chạy `python kiem_prompt_veo.py <file.md>` đạt mới giao. Làm thử 3 clip trước.
- **C (bản đồ, sơ đồ):** dựng bằng bộ dựng bản đồ; chữ nằm gọn trong 60 đến 1860 px; ít banner. Các khung thang đo ở chương 9 dùng chung một sơ đồ, mỗi câu làm sáng một dòng.
- **D (thẻ chữ):** vẽ bằng code, toàn màn hình, tối đa khoảng 3,5 giây, không đè phụ đề, không dùng khung trích lời dưới màn hình (quy định 22/10). Nội dung thẻ lấy từ đúng lời kể; chỉ trích nguyên văn khi đã đọc nguyên văn (hiện chỉ Hậu Hán thư quyển 9, 68, 70). Thẻ có tên sách phải ghi rõ nhãn nguồn.

## Bảng từng câu

### Chương 1. Mở đầu: dòng sông không chảy

Loại: A 2, B 3, C 3, D 2

| Câu | Loại | Hình | Ghi chú |
|---|---|---|---|
| 1 | B | Dòng sông lớn lặng trong sương, bờ vắng | Chuyển động nhẹ (khói, nước, cờ, đèn) |
| 2 | C | Bản đồ Từ Châu năm 193, mũi tên quân Tào tiến vào | Bản đồ/sơ đồ |
| 3 | B | Dòng Tứ Thủy phủ khói, xe đổ ven bờ, không người | Chuyển động nhẹ (khói, nước, cờ, đèn) |
| 4 | B | Dòng sông Tứ Thủy sương mờ, thuyền nhỏ đứng yên, không người | Chuyển động nhẹ (khói, nước, cờ, đèn) |
| 5 | A | Tào Tháo một mình đứng trên đồng hoang, xương trắng ở xa | Ảnh tĩnh |
| 6 | A | Tào Tháo ra lệnh tìm người tài, quan lại cúi nhận | Ảnh tĩnh |
| 7 | D | Thẻ tiêu đề: "Tào Tháo ác đến mức nào?" | Thẻ chữ |
| 8 | C | Sơ đồ hai loại chuyện: chính văn / chú giải | Bản đồ/sơ đồ |
| 9 | D | Thẻ "Bùi Tùng Chi chép chú giải từ nhiều sách khác" | Thẻ chữ |
| 10 | C | Sơ đồ mỗi chương: việc đáng trách / việc làm được | Bản đồ/sơ đồ |

### Chương 2. Chàng trai ở Lạc Dương

Loại: A 14, B 3, C 1, D 2

| Câu | Loại | Hình | Ghi chú |
|---|---|---|---|
| 11 | B | Nhà quyền thế ở huyện Tiếu, sân vườn vắng | Chuyển động nhẹ (khói, nước, cờ, đèn) |
| 12 | A | Cậu thiếu niên họ Tào trong nhà giàu, cha và hoạn quan nuôi | Ảnh tĩnh |
| 13 | A | Thanh niên Tào Tháo ham chơi, cưỡi ngựa săn bắn | Ảnh tĩnh |
| 14 | A | Tào Tháo hai mươi tuổi nhận chức Bắc bộ úy | Ảnh tĩnh |
| 15 | B | Khu phố phía bắc Lạc Dương, đường vắng | Chuyển động nhẹ (khói, nước, cờ, đèn) |
| 16 | A | Roi ngũ sắc dựng trước công đường, Tào Tháo đứng cạnh | Ảnh tĩnh |
| 17 | A | Kiển Thạc, hoạn quan quyền thế, trong cung | Ảnh tĩnh |
| 18 | A | Người chú của Kiển Thạc đi đêm giữa phố, đèn dầu | Veo (người di chuyển) |
| 19 | A | Công đường ban đêm, bóng người cầm roi, không máu | Ảnh tĩnh |
| 20 | B | Phố Lạc Dương đêm vắng, không ai ra đường | Chuyển động nhẹ (khói, nước, cờ, đèn) |
| 21 | A | Tào Tháo trẻ hỏi nhà xem tướng Hứa Thiệu | Ảnh tĩnh |
| 22 | D | Thẻ trích Hậu Hán thư: "gian trá thời bình, anh hùng thời loạn" | Thẻ chữ |
| 23 | D | Thẻ bản chép khác: "quan giỏi thời bình, gian hùng thời loạn" | Thẻ chữ |
| 24 | C | Mốc thời gian năm 189: Linh Đế mất | Bản đồ/sơ đồ |
| 25 | A | Hà Tiến gọi Đổng Trác đem quân về | Ảnh tĩnh |
| 26 | A | Cung đình hỗn loạn, khói, cửa cung đóng | Ảnh tĩnh |
| 27 | A | Đổng Trác phế Thiếu Đế, đưa Hiến Đế lên ngôi | Ảnh tĩnh |
| 28 | A | Đổng Trác triệu Tào Tháo, trao chức kiêu kỵ hiệu úy | Ảnh tĩnh |
| 29 | A | Tào Tháo lắc đầu trước Đổng Trác | Ảnh tĩnh |
| 30 | A | Tào Tháo cải trang cưỡi ngựa rời Lạc Dương lúc sáng sớm | Veo (người di chuyển) |

### Chương 3. Một đêm ở nhà Lã Bá Xa

Loại: A 2, B 2, C 2, D 1

| Câu | Loại | Hình | Ghi chú |
|---|---|---|---|
| 31 | C | Bản đồ Lạc Dương đến Thành Cao | Bản đồ/sơ đồ |
| 32 | C | Sơ đồ ba ghi chép kể khác nhau về nhà Lã Bá Xa | Bản đồ/sơ đồ |
| 33 | A | Gia đình Lã Bá Xa chuẩn bị bữa tiệc đãi khách | Ảnh tĩnh |
| 34 | B | Sân nhà ban đêm tối, đèn dầu Hán, không người | Chuyển động nhẹ (khói, nước, cờ, đèn) |
| 35 | B | Bếp nhà quê trống, nồi nguội, đèn dầu Hán, không người | Chuyển động nhẹ (khói, nước, cờ, đèn) |
| 36 | D | Thẻ câu nói nổi tiếng, nguồn Tôn Thịnh Tạp ký | Thẻ chữ |
| 37 | A | Tào Tháo cưỡi ngựa tới Trần Lưu, vung tiền nhà chiêu quân | Veo (người di chuyển) |

### Chương 4. Có đất, có lính

Loại: A 6, B 1, C 1

| Câu | Loại | Hình | Ghi chú |
|---|---|---|---|
| 38 | C | Bản đồ liên quân các lãnh chúa năm 190 | Bản đồ/sơ đồ |
| 39 | A | Các lãnh chúa họp bàn, cãi nhau, Tào Tháo đứng ngoài | Ảnh tĩnh |
| 40 | A | Liên quân tan, từng đoàn quân quay về | Veo (người di chuyển) |
| 41 | B | Đồng hoang, cờ gãy, khói xa, không người | Chuyển động nhẹ (khói, nước, cờ, đèn) |
| 42 | A | Quân Khăn Vàng tràn vào Duyện Châu | Veo (người di chuyển) |
| 43 | A | Quan địa phương mời Tào Tháo giữ đất | Ảnh tĩnh |
| 44 | A | Hàng quân Khăn Vàng và dân kéo dài trên đường đầu hàng | Veo (người di chuyển) |
| 45 | A | Tào Tháo chọn người khỏe lập đội quân riêng | Veo (người di chuyển) |

### CHƯƠNG 5 – TỪ CHÂU: CUỘC BÁO THÙ ĐẪM MÁU

Loại: A 13, B 7, C 2, D 1

| Câu | Loại | Hình | Ghi chú |
|---|---|---|---|
| 46 | A | Tào Tháo nhận tin cha mất, sững người | Ảnh tĩnh |
| 47 | B | Nhà cũ của Tào Tung ở Từ Châu, vắng | Chuyển động nhẹ (khói, nước, cờ, đèn) |
| 48 | A | Đoàn xe của Tào Tung đi qua đất Đào Khiêm | Veo (người di chuyển) |
| 49 | A | Tào Tháo trước bản đồ quân, mặt nghiêm | Ảnh tĩnh |
| 50 | A | Quân Tào tiến vào Từ Châu qua cổng thành | Veo (người di chuyển) |
| 51 | C | Bản đồ Bành Thành và thành Đàm | Bản đồ/sơ đồ |
| 52 | A | Quân Tào tràn qua Thủ Lư, Thùy Lăng, Hạ Khâu | Veo (người di chuyển) |
| 53 | A | Dân làng đứng bên đường trong khói | Ảnh tĩnh |
| 54 | D | Thẻ trích Hậu Hán thư: "gà chó cũng không còn" | Thẻ chữ |
| 55 | B | Làng hoang, nhà cháy, khói bay, không người | Chuyển động nhẹ (khói, nước, cờ, đèn) |
| 56 | A | Người chạy loạn từ kinh đô đến Từ Châu | Veo (người di chuyển) |
| 57 | A | Dân chạy loạn gánh đồ đi trên đường | Veo (người di chuyển) |
| 58 | B | Bến sông Từ Châu vắng, thuyền bỏ không | Chuyển động nhẹ (khói, nước, cờ, đèn) |
| 59 | B | Dòng sông Tứ Thủy chảy chậm, khói, không người | Chuyển động nhẹ (khói, nước, cờ, đèn) |
| 60 | B | Cánh đồng sau chiến trận, tro tàn, không người | Chuyển động nhẹ (khói, nước, cờ, đèn) |
| 61 | A | Quân Tào rút đi vì thiếu lương | Veo (người di chuyển) |
| 62 | C | Bản đồ lần đánh thứ hai qua Lang Nha, Đông Hải | Bản đồ/sơ đồ |
| 63 | A | Tào Tháo nhìn khói từ xa | Ảnh tĩnh |
| 64 | A | Dân thường ngồi bên đống nhà đổ | Ảnh tĩnh |
| 65 | A | Trương Mạc, Trần Cung đón Lã Bố vào Duyện Châu | Ảnh tĩnh |
| 66 | B | Nhà danh sĩ Biên Nhượng đóng cửa, sân vắng | Chuyển động nhẹ (khói, nước, cờ, đèn) |
| 67 | B | Phòng đọc sách tối, thẻ tre cuộn trên giá, không người | Chuyển động nhẹ (khói, nước, cờ, đèn) |
| 68 | A | Tào Tháo và Lã Bố đối trận, quân hai bên xa | Ảnh tĩnh |

### CHƯƠNG 6 – NGƯỜI NẮM QUYỀN

Loại: A 13, B 10, C 4, D 2

| Câu | Loại | Hình | Ghi chú |
|---|---|---|---|
| 69 | B | Cung điện Lạc Dương đổ nát, không người | Chuyển động nhẹ (khói, nước, cờ, đèn) |
| 70 | A | Hiến Đế lưu lạc giữa quân phiệt, đoàn người lơ thơ | Veo (người di chuyển) |
| 71 | A | Tào Tháo nhìn hoàng đế từ xa | Ảnh tĩnh |
| 72 | A | Tuân Úc khuyên Tào Tháo đón vua | Ảnh tĩnh |
| 73 | A | Tào Tháo đưa Hiến Đế về Hứa, đoàn xe và quân hộ tống | Veo (người di chuyển) |
| 74 | A | Hiến Đế ngồi trên ngai, Tào Tháo đứng bên | Ảnh tĩnh |
| 75 | B | Kho lương trống, bao rỗng | Chuyển động nhẹ (khói, nước, cờ, đèn) |
| 76 | B | Ruộng bỏ hoang, cỏ mọc | Chuyển động nhẹ (khói, nước, cờ, đèn) |
| 77 | A | Tảo Chi và Hàn Hạo trình đề xuất đồn điền | Ảnh tĩnh |
| 78 | A | Dân và lính cùng cày ruộng đồn điền | Veo (người di chuyển) |
| 79 | C | Sơ đồ đồn điền: ruộng, lương, quân | Bản đồ/sơ đồ |
| 80 | B | Kho lương đầy, lúa vàng, không người | Chuyển động nhẹ (khói, nước, cờ, đèn) |
| 81 | C | Bản đồ Tào Tháo và Viên Thiệu hai bên sông | Bản đồ/sơ đồ |
| 82 | A | Hai đạo quân đối mặt ở Quan Độ | Veo (người di chuyển) |
| 83 | A | Quân Tào lật tìm thư trong doanh trại Viên Thiệu | Ảnh tĩnh |
| 84 | B | Lều trướng Viên Thiệu ban đêm, hòm thư mở, không người | Chuyển động nhẹ (khói, nước, cờ, đèn) |
| 85 | A | Tào Tháo đứng bên đống lửa đốt thư, tay không | Ảnh tĩnh |
| 86 | B | Doanh trại Viên Thiệu ban đêm, đống lửa tàn | Chuyển động nhẹ (khói, nước, cờ, đèn) |
| 87 | B | Đống tro thư còn bốc khói, trong lều trống | Chuyển động nhẹ (khói, nước, cờ, đèn) |
| 88 | B | Doanh trại sau trận, cờ rũ, không người | Chuyển động nhẹ (khói, nước, cờ, đèn) |
| 89 | B | Bãi chiến trường Quan Độ yên ắng, cờ rách, không người | Chuyển động nhẹ (khói, nước, cờ, đèn) |
| 90 | C | Sơ đồ con số: tám vạn hay bảy vạn | Bản đồ/sơ đồ |
| 91 | C | Sơ đồ đối chiếu Tư trị thông giám khảo dị | Bản đồ/sơ đồ |
| 92 | B | Bãi Quan Độ yên ắng lúc bình minh | Chuyển động nhẹ (khói, nước, cờ, đèn) |
| 93 | A | Tào Tháo tiếp người tài, quan giỏi đứng chờ | Ảnh tĩnh |
| 94 | D | Thẻ trích lệnh cầu hiền năm 217: dùng cả người bất nhân, bất hiếu miễn có tài | Thẻ chữ |
| 95 | D | Thẻ trích lệnh năm 214: người có hạnh chưa chắc lập công | Thẻ chữ |
| 96 | A | Hai người đứng trước Tào Tháo, một người hiền lành, một người giỏi công trạng | Ảnh tĩnh |
| 97 | A | Tào Tháo chọn người theo tài | Ảnh tĩnh |

### Chương 7. Những người bị giết

Loại: A 20, B 8, C 6, D 1

| Câu | Loại | Hình | Ghi chú |
|---|---|---|---|
| 98 | A | Tào Tháo ngồi triều, quan chia hai hàng | Ảnh tĩnh |
| 99 | A | Quan bất đồng đứng một góc | Ảnh tĩnh |
| 100 | A | Khổng Dung giữa triều đình | Ảnh tĩnh |
| 101 | A | Khổng Dung viết văn châm biếm | Ảnh tĩnh |
| 102 | A | Sứ giả của Tôn Quyền tiếp kiến Khổng Dung; ông bị cáo buộc bất kính, chống đối | Ảnh tĩnh |
| 103 | B | Công đường trống, bàn án trống | Chuyển động nhẹ (khói, nước, cờ, đèn) |
| 104 | B | Nhà họ Khổng vắng, cổng khóa | Chuyển động nhẹ (khói, nước, cờ, đèn) |
| 105 | C | Sơ đồ bảy văn nhân thời Kiến An | Bản đồ/sơ đồ |
| 106 | B | Phủ Tào Tháo ban đêm, đèn dầu Hán | Chuyển động nhẹ (khói, nước, cờ, đèn) |
| 107 | A | Hoa Đà, thầy thuốc nổi tiếng, trên đường khám bệnh | Ảnh tĩnh |
| 108 | A | Hoa Đà chữa đau đầu cho Tào Tháo | Ảnh tĩnh |
| 109 | A | Hoa Đà nhìn ra cửa, ngần ngại | Ảnh tĩnh |
| 110 | A | Hoa Đà xin về vì vợ ốm | Ảnh tĩnh |
| 111 | A | Sứ giả của Tào Tháo đến nhà Hoa Đà | Ảnh tĩnh |
| 112 | C | Sơ đồ: ốm thật thì nghỉ, giả thì bị bắt | Bản đồ/sơ đồ |
| 113 | A | Hoa Đà bị áp giải về Hứa, đoàn lính | Veo (người di chuyển) |
| 114 | A | Tuân Úc xin tha cho Hoa Đà | Ảnh tĩnh |
| 115 | A | Tào Tháo lắc đầu từ chối | Ảnh tĩnh |
| 116 | A | Hoa Đà trong ngục với cuộn sách | Ảnh tĩnh |
| 117 | A | Người giữ ngục lùi lại, Hoa Đà đốt sách | Ảnh tĩnh |
| 118 | A | Tào Tháo ôm đầu đau, Tào Xung ốm | Ảnh tĩnh |
| 119 | A | Tào Tháo hối hận trước cửa phòng bệnh | Ảnh tĩnh |
| 120 | B | Thư phòng cổ, thẻ tre, không người | Chuyển động nhẹ (khói, nước, cờ, đèn) |
| 121 | B | Cuộn thẻ tre nằm trên bàn, đèn dầu | Chuyển động nhẹ (khói, nước, cờ, đèn) |
| 122 | B | Phòng ghi sử, thẻ tre xếp gọn, vắng | Chuyển động nhẹ (khói, nước, cờ, đèn) |
| 123 | C | Bản đồ phía tây | Bản đồ/sơ đồ |
| 124 | C | Bản đồ Mã Siêu, Hàn Toại nổi dậy năm 211 | Bản đồ/sơ đồ |
| 125 | A | Mã Siêu thất bại, Mã Đằng ở triều đình | Ảnh tĩnh |
| 126 | A | Mã Đằng bị đưa đi giữa lính | Veo (người di chuyển) |
| 127 | D | Thẻ thư Mã Siêu dâng Lưu Bị | Thẻ chữ |
| 128 | B | Sân nhà họ Mã vắng, cổng mở | Chuyển động nhẹ (khói, nước, cờ, đèn) |
| 129 | B | Con đường vắng trải dài trong bụi | Chuyển động nhẹ (khói, nước, cờ, đèn) |
| 130 | C | Sơ đồ ba vụ: Khổng Dung, Hoa Đà, Mã Đằng | Bản đồ/sơ đồ |
| 131 | C | Sơ đồ ba vụ: nguyên nhân khác nhau | Bản đồ/sơ đồ |
| 132 | A | Tào Tháo một mình giữa đại sảnh | Ảnh tĩnh |

### Chương 8. Hoàng đế và hoàng hậu

Loại: A 14, B 5, C 3, D 2

| Câu | Loại | Hình | Ghi chú |
|---|---|---|---|
| 133 | A | Tào Tháo cầm lệnh bài, quan đứng sau | Ảnh tĩnh |
| 134 | A | Hiến Đế và Phục hoàng hậu ngồi trong cung | Ảnh tĩnh |
| 135 | A | Phục hoàng hậu viết thư | Ảnh tĩnh |
| 136 | A | Thư gửi Phục Hoàn, người đưa thư | Ảnh tĩnh |
| 137 | A | Phục Hoàn cất thư không dám làm gì | Ảnh tĩnh |
| 138 | A | Tào Tháo nhận tin thư cũ bị phát giác | Ảnh tĩnh |
| 139 | A | Quân của Tào Tháo vào cung, hoàng hậu bị phế | Veo (người di chuyển) |
| 140 | A | Phục hoàng hậu ẩn sau vách tường | Ảnh tĩnh |
| 141 | A | Hoàng hậu gặp Hiến Đế ngoài điện | Ảnh tĩnh |
| 142 | A | Hoàng hậu tóc rối, chân không giày | Ảnh tĩnh |
| 143 | A | Hiến Đế cúi đầu bất lực | Ảnh tĩnh |
| 144 | B | Cung điện vắng, cửa nặng đóng | Chuyển động nhẹ (khói, nước, cờ, đèn) |
| 145 | C | Sơ đồ gia tộc họ Phục: bị giết, bị đày | Bản đồ/sơ đồ |
| 146 | B | Con đường lưu đày, hoang vắng | Chuyển động nhẹ (khói, nước, cờ, đèn) |
| 147 | A | Tào Tiết, con gái Tào Tháo, lên làm hoàng hậu | Ảnh tĩnh |
| 148 | C | Sơ đồ ngôi hoàng hậu về họ Tào | Bản đồ/sơ đồ |
| 149 | A | Hiến Đế ngồi ngai, xung quanh người của Tào Tháo | Ảnh tĩnh |
| 150 | B | Ngai vàng bỏ trống trong điện | Chuyển động nhẹ (khói, nước, cờ, đèn) |
| 151 | C | Sơ đồ Ngụy công, Ngụy vương, vẫn là danh nhà Hán | Bản đồ/sơ đồ |
| 152 | D | Thẻ bài tự thuật cuối năm 210 | Thẻ chữ |
| 153 | B | Thành Nghiệp lúc hoàng hôn, vắng | Chuyển động nhẹ (khói, nước, cờ, đèn) |
| 154 | A | Tào Tháo bên bản đồ và đèn dầu | Ảnh tĩnh |
| 155 | B | Phủ Ngụy vương, lính canh, đêm | Chuyển động nhẹ (khói, nước, cờ, đèn) |
| 156 | D | Thẻ "buông quyền lực = đặt cả gia tộc vào hiểm nguy" | Thẻ chữ |

### Chương 9. Tào Tháo tàn bạo đến mức nào?

Loại: A 13, B 8, C 6, D 4

| Câu | Loại | Hình | Ghi chú |
|---|---|---|---|
| 157 | A | Tào Tháo mất, linh cữu đưa đi | Veo (người di chuyển) |
| 158 | A | Tào Phi nhận ngôi từ Hiến Đế, lập nhà Ngụy | Ảnh tĩnh |
| 159 | D | Thẻ Trần Thọ: "người phi thường, bậc anh kiệt" | Thẻ chữ |
| 160 | A | Nhà sử Trần Thọ viết trên thẻ tre | Ảnh tĩnh |
| 161 | B | Thư phòng sử gia vắng | Chuyển động nhẹ (khói, nước, cờ, đèn) |
| 162 | B | Thư viện Đông Ngô, kệ thẻ tre, vắng | Chuyển động nhẹ (khói, nước, cờ, đèn) |
| 163 | B | Kệ thẻ tre, đèn dầu, không người | Chuyển động nhẹ (khói, nước, cờ, đèn) |
| 164 | D | Thẻ câu hỏi "Tàn bạo đến mức nào?" | Thẻ chữ |
| 165 | C | Sơ đồ hai tiêu chí: nặng đến đâu / tin được đến đâu | Bản đồ/sơ đồ |
| 166 | C | Thang đo: Từ Châu nặng nhất | Bản đồ/sơ đồ |
| 167 | A | Dân Từ Châu chạy giữa khói, gánh đồ | Veo (người di chuyển) |
| 168 | C | Thang đo: giết cả gia tộc | Bản đồ/sơ đồ |
| 169 | A | Phục hoàng hậu ngồi trong cung, nhìn ra cửa | Ảnh tĩnh |
| 170 | C | Thang đo: độ chắc của nguồn Hậu Hán thư | Bản đồ/sơ đồ |
| 171 | A | Hàng quân Viên Thiệu cúi đầu đi qua cổng trại | Veo (người di chuyển) |
| 172 | C | Thang đo: số người và tình trạng | Bản đồ/sơ đồ |
| 173 | B | Doanh trại tù binh trống, hàng rào gỗ | Chuyển động nhẹ (khói, nước, cờ, đèn) |
| 174 | B | Cổng thành vắng sau cơn biến | Chuyển động nhẹ (khói, nước, cờ, đèn) |
| 175 | A | Hoa Đà và Khổng Dung đứng hai bên, nét mặt buồn | Ảnh tĩnh |
| 176 | C | Thang đo: Biên Nhượng, Lã Bá Xa căn cứ yếu | Bản đồ/sơ đồ |
| 177 | B | Hai con đường rẽ, bia không chữ | Chuyển động nhẹ (khói, nước, cờ, đèn) |
| 178 | B | Con đường chia hai ngả, vắng | Chuyển động nhẹ (khói, nước, cờ, đèn) |
| 179 | D | Thẻ nghịch lý: chuyện nổi tiếng không phải vững nhất | Thẻ chữ |
| 180 | D | Thẻ "hình ảnh nhân vật không chỉ từ giai thoại" | Thẻ chữ |
| 181 | A | Tào Tháo thu phục nhân tài, đồn điền, đánh đối thủ | Ảnh tĩnh |
| 182 | A | Tào Tháo đốt thư, tay không | Ảnh tĩnh |
| 183 | A | Tào Tháo đứng trước dân đói, trách nhiệm | Ảnh tĩnh |
| 184 | B | Từ Châu hoang, đường vắng | Chuyển động nhẹ (khói, nước, cờ, đèn) |
| 185 | A | Tào Tháo nhìn về phía trước | Ảnh tĩnh |
| 186 | A | Tào Tháo đứng giữa quyền lực | Ảnh tĩnh |
| 187 | A | Chân dung Tào Tháo, câu hỏi cho người xem | Ảnh tĩnh |

## Điểm cần chủ kênh duyệt

- Chương 9 có nhiều câu liên tiếp dùng thang đo (C); nếu thấy đơn điệu, có thể đổi vài câu sang ảnh nhân vật (A).
- Cảnh Từ Châu và chôn sống vẽ gợi, không thấy người chết; có thể gây cảm giác nhẹ hơn lời kể.
- Ảnh nhân vật cần mẫu: Tào Tháo ở tuổi hai mươi, ba mươi lăm, năm mươi và sáu mươi lăm; Đổng Trác, Hứa Thiệu, Hoa Đà, Tuân Úc, Phục hoàng hậu, Hiến Đế, Khổng Dung. Chưa tạo.
