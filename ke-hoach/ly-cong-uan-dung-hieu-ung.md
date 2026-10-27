# Lý Công Uẩn: kịch bản dựng video bản đồ (bản nháp để chủ kênh duyệt)

Mã `ly1`, số câu 18001–18134 (134 đoạn), khoảng 14,6 phút (ước 3 chữ/giây; đo lại sau khi có giọng). Kiểu phim bản đồ động, giọng Puck, tiếng động mô phỏng, không nhạc nền. Mọi bố cục theo CLAUDE.md: không khung trích lời, ít banner, chữ nằm gọn trong khung 60–1860 px, chỉ một lớp chữ lớn mỗi lúc.

## 1. Việc phải làm mới so với các video bản đồ trước
| Việc | Chi tiết |
|---|---|
| Bản đồ nền | Các video cũ dùng nền Trung Hoa (`world4`). Video này cần nền vùng Đại Việt: đồng bằng sông Hồng, Thanh Hóa, Nghệ An, thêm một góc phía bắc (nhà Tống) và phía tây (Nam Chiếu). Zoom ra mức cả vùng, vào mức một khu thành. Tên địa danh chỉ dùng tên đương thời, không ghi tên tỉnh hiện nay. |
| Địa danh (`LOC`) | Cổ Pháp, Hoa Lư, Đại La (sau đổi Thăng Long), Ái Châu, Diễn Châu, vùng biển Biện Sơn, bến Kim Hoa, Nam Chiếu, nhà Tống. Toạ độ chỉ gần đúng (Kim Hoa và Biện Sơn chưa chắc vị trí), ghi rõ khi giao. |
| Sơ đồ khu thành | Một cảnh phóng to riêng của thành Thăng Long: bốn cửa (Tường Phù đông, Quảng Phúc tây, hai cửa còn lại), điện Càn Nguyên ở giữa, Tập Hiền và Giảng Võ hai bên, Long An và Long Thụy phía sau. Vẽ sơ đồ phẳng, cờ và biển để trơn, không chữ trên cờ. Dùng cho chương 8, 10, 11, 12. |
| Hiệu ứng "hai lớp thời gian" | Ô năm góc trái chạy theo lời kể (974 → 1005 → 1009 → 1010 → 1028). Ngày âm kèm ngày dương chỉ hiện ở các mốc có trong lời kể. Ghi chú nhỏ "ngày dương lịch quy đổi theo lịch Julian" ở phần mô tả, không đưa lên màn hình. |
| Logo | Logo cây đèn 130 px, góc trên bên phải, như `mapfilm3.py`. |
| Mở và kết | Thẻ tiêu đề ở giây đầu (3–4 giây), kết bằng mờ dần, không thẻ HẾT. |

## 2. Bảng hiệu ứng theo chương
Ký hiệu: `NT` ghi chú nổi (tối đa 4 mỗi chương, mỗi cái tối đa 3,5 giây), `J` khung đùa (tối đa 2 mỗi chương, tối đa 3 giây, chỉ nhắm tình huống hoặc quân xâm lược, không đùa Lý Công Uẩn, không đùa các vua bị giết), `NU` thẻ số, `Q` đoạn giao tranh (ẩn NT, J, NU).

### Chương 1: Đứa trẻ bên nhà thiền sư (18001–18012)
- **Hình:** mở bằng toàn cảnh đồng bằng sông Hồng, zoom vào châu Cổ Pháp, một chấm sáng nhấp nháy khi đọc 18001. Ô năm: 974. Dưới thời Đinh Bộ Lĩnh hiện hai chữ "nhà Đinh" bằng nhãn nhỏ. Tua nhanh năm tháng khi đọc 18006: ô năm chạy 974 → 980 và lá cờ nhà Đinh đổi sang cờ nhà Tiền Lê (cờ để trơn một màu). 18007 chùa Lục Tổ hiện icon chùa.
- **Câu 18011 (hook):** bản đồ tối đi nhẹ, icon cung điện Tiền Lê sáng lên, một dấu hỏi lớn mờ rồi tan; không thêm chữ.
- **NT:** 18001 "ngày sinh: 12 tháng 2 âm lịch"; 18004 "năm ba tuổi"; 18007 "chuyện kể về sau, chưa chắc" (đúng với câu 18008); 18010 "quan võ nhà Tiền Lê".
- **J:** không dùng (chương mở đầu nghiêm túc).
- **Âm thanh:** chuông chùa khẽ, gió; im lặng nửa giây trước câu hook.

### Chương 2: Người giữ cung nhà Lê (18013–18026)
- **Hình:** bản đồ vào kinh đô Hoa Lư. Ô năm: 1005. Cảnh các hoàng tử tranh ngôi: ba icon hoàng tử chạm nhau, một bị mờ đi khi đọc 18016, chỉ dùng biểu tượng "thua" (cờ rũ), không máu, không đầu lâu. 18017: các icon quan chạy ra rìa, một icon ở lại giữa. 18019: thăng chức bằng thanh cấp bậc tăng.
- **NT:** 18015 "tám tháng không có vua"; 18019 "chỉ huy quân bảo vệ vua"; 18025 "năm 1009" (mốc chết của Lê Long Đĩnh). Không thêm NT cho chuyện hạt mận.
- **J (nhắm tình huống):** 18021 "Điềm báo từ quả khế" (chỉ nhắm vào chuyện mê tín, không chê người); bỏ nếu thấy nhạy.
- **NU:** một thẻ "1005 → 1009" ở đầu chương.
- **Âm thanh:** trống chậm, bước chân trong cung, tiếng đổ nhẹ khi 18016, im một nhịp ở câu 18017.

### Chương 3: Lời nói khích và ngôi vua (18027–18047)
- **Hình:** sơ đồ cung nội: hai đội 500 quân (Lý Công Uẩn và Nguyễn Đê) là hai cụm icon nhỏ cạnh ngai. 18030–18035 ban đêm (lớp tối `NIGHT`), hai icon người sát nhau dưới đèn dầu, không vẽ mặt. 18036–18038 các icon quan quây lại thành vòng tròn họp. 18039–18040 sáng dần, đoàn icon dìu một icon lên điện, hàng quan cúi.
- **Q:** không có giao tranh. 18041 hiện ba chấm sáng "không có một trận đánh nào": chỉ là nhịp, không chữ.
- **NT:** 18033 "người nói khích đầu tiên"; 18039 "21 tháng 11 âm lịch năm 1009"; 18042 "niên hiệu Thuận Thiên: thuận theo ý trời".
- **J:** không dùng (tập trung nghe để hiểu).
- **Âm thanh:** dế đêm, nhịp tim chậm ở 18032 và 18034; tiếng bước dìu và vải áo; sáng dần, tiếng hô "vạn tuế, vạn tuế" từ nhiều người (hạ nhỏ khi giọng đọc).

### Chương 4: Hoa Lư không còn đủ (18048–18055)
- **Hình:** hai khung so sánh: bên trái Hoa Lư giữa núi đá (núi vẽ đậm, đường vào hẹp), bên phải vùng đồng bằng mở rộng. 18049 hiện hai mũi tên: giặc khó vào, quân dễ giữ. 18054–18055 hai thanh thời gian ngắn: Đinh (hai vua), Tiền Lê (ba vua, 29 năm) hiện thành hai thanh.
- **NU:** thẻ số hai/ba/29 nhỏ đúng lúc đọc 18055 (không trùng NT).
- **NT:** 18049 "ưu: dễ phòng thủ"; 18052 "nhược: chật và ẩm thấp".
- **Âm thanh:** gió núi, tiếng vọng hang đá; nhịp suy tính đều.

### Chương 5: Đại La bên sông (18056–18063)
- **Hình:** camera chạy từ Hoa Lư sang Đại La theo đường nét đứt, sông Hồng hiện sáng; 18057 hiện tường thành cũ, ô năm lùi 866. 18060 thuyền bè nhiều nơi cập bến (ba bốn icon thuyền). 18062 hai icon "bỏ cung cũ, dựng lại" (cung cũ mờ, khung nền mới hiện). 
- **NT:** 18057 "thành do Cao Biền đắp năm 866"; 18060 "sông, thuyền, đất rộng".
- **Âm thanh:** nước sông, mái chèo, tiếng chim nước.

### Chương 6: Lá chiếu dời đô (18064–18071)
- **Hình:** thẻ vua ngồi trước cuộn thẻ tre (không chữ đọc được). 18064 ghé Cổ Pháp: icon dân làng, tặng tiền lụa cho cụ già. 18065 icon sứ giả đi lên phía bắc đến nhà Tống. 18066–18068 ba biểu tượng lần lượt: chuyện nhà Thương, nhà Chu (hai cuộn), rồi hình rồng cuộn hổ ngồi vẽ cách điệu. 18069 vua đứng, các quan cúi; 18070 các quan cúi đầu; 18071 một nhịp sáng ấm.
- **NT:** 18066 "nhà Thương dời đô 5 lần, nhà Chu 3 lần"; 18069 "vua hỏi chứ không ra lệnh".
- **J:** không dùng.
- **Âm thanh:** cọ viết khẽ, lật thẻ tre; giọng kể chậm lại ở 18069.

### Chương 7: Con thuyền dưới chân thành (18072–18075)
- **Hình:** ô năm 1010, 18072 hiện cả ngày âm lẫn "khoảng tháng tám dương lịch". Đoàn thuyền rẽ sóng, ánh vàng chạy trên mặt nước khi đọc 18073, kèm nhãn nhỏ "theo lời kể" (đúng với câu 18074). 18075: nhãn "Đại La" mờ đi, nhãn "Thăng Long" sáng lên (đổi tên). Thẻ tiêu đề nhỏ chỉ 2 giây.
- **Âm thanh:** sóng, mái chèo, trống thuyền; tiếng vang nhẹ khi rồng "hiện" (chỉ nửa giây).

### Chương 8: Bốn cánh cửa và các điện (18076–18086)
- **Hình:** chuyển sang sơ đồ khu thành. Điện Càn Nguyên hiện đầu tiên, rồi Tập Hiền, Giảng Võ; Long An, Long Thụy phía sau (18076–18077). Kho tàng, tường thành, hào nước đào (18078). Bốn cửa hiện theo bốn hướng (18079), cửa tây sáng nhẹ ở 18080 rồi tắt. 18082 hai nhãn đổi tên: Cổ Pháp → phủ Thiên Đức, Hoa Lư → phủ Trường Yên. 18083–18084 thuế: biểu tượng túi thóc biến mất, 18085 cờ nhà Tống trao ấn cho ông.
- **NT:** 18079 "Tường Phù (đông), Quảng Phúc (tây)"; 18083 "miễn thuế ba năm"; 18085 "nhà Tống phong Giao Chỉ quận vương".
- **NU:** không dùng.
- **Âm thanh:** búa, đục, xe chở đá; cuối chương nhạc không có, chỉ tiếng chuông khi cửa tây sáng.

### Chương 9: Những năm trị vì (18087–18106)
- **Hình:** bản đồ cả nước. 18088 mười đạo thành hai mươi bốn lộ: mười vùng tách thành hai mươi bốn ô nhỏ. 18089–18091 quân đi đánh Cử Long ở Ái Châu (hai cụm icon đối diện, quân Đại Việt tiến, bộ lạc cháy nhẹ rồi quân giặc tan). 18092–18096 hành quân về Diễn Châu, biển Biện Sơn tối sầm, sấm chớp, vua đốt hương (icon vua đứng một mình trên thuyền, trời tối rồi sáng, đúng với "người ta kể"). 18098–18101 Nam Chiếu đóng trại ở Kim Hoa, Dực Thánh Vương tiến quân thắng, quân đối phương chạy (chuyển xám, cờ rũ, "THUA TRẬN"). 18102 ngựa bắt được dẫn sang nhà Tống. 18103–18105 chùa, tiếng chuông, đoàn người đi tu.
- **Q:** (18089, 18091), (18098, 18101): ẩn NT, J, NU. Chỉ giữ phụ đề và nhãn quân.
- **NT (ngoài Q):** 18088 "10 đạo → 24 lộ"; 18090 "hai triều trước không đánh nổi"; 18094 "theo lời kể: gió sấm yên".
- **J (nhắm quân xâm lược, tối đa 2):** 18101 "Nam Chiếu đến lấy ngựa, về mất cả ngựa"; chưa chắc nên chỉ dùng nếu chủ kênh duyệt.
- **NU:** một thẻ ở 18098: "năm 1014".
- **Âm thanh:** trống trận, vó ngựa, tiếng sấm (18093), chuông chùa (18103–18105).

### Chương 10: Điện Long An (18107–18112)
- **Hình:** sơ đồ thành buổi chiều, đèn dầu lên dần. Ô năm: 1028. 18108 icon thái tử đứng bên ngoài. 18110 nhật thực: một vòng tròn đen che dần mặt trời ở rìa màn hình, khung hình tối nhẹ. 18111 ngôi điện sáng một lần rồi dịu. Không vẽ cảnh nằm hay cảnh chết.
- **NT:** 18110 "nhật thực 29 tháng 3"; 18112 "ở ngôi 18 năm". 
- **Âm thanh:** gió, chuông xa; tắt hết tiếng động ở 18110 (im lặng thật), giọng kể trầm chậm; sau 18112 một nhịp lặng rồi vào chương sau.

### Chương 11: Cánh cửa Quảng Phúc (18113–18126)
- **Hình:** sơ đồ khu thành, Quảng Phúc ở rìa tây. 18114–18115 ba cụm quân nhỏ giấu sau cổng (chỉ thấy bóng và cờ trơn, đúng với "ba vương đem quân giấu sẵn"). 18116 thái tử đi vào cửa Tường Phù, đường nét sáng. 18117 cửa đóng, quân bố trí quanh điện. 18118–18119 thái tử mặc áo tang đứng hầu, ánh sáng dịu. 18120 cổng mở, lính cung xông ra; 18121 hai bên đối mặt giữa sân, icon Lê Phụng Hiểu chạy tới cửa; 18122 Vũ Đức Vương: chỉ dùng biểu tượng "BỊ DIỆT" mờ, không đầu lâu rõ, không mô phỏng chém giết; 18123 quân phản loạn chạy, chuyển xám cờ rũ. 18124–18125 icon tướng vẫn mặc giáp bước vào điện báo tin, rồi sang điện Càn Nguyên. 18126 thái tử bước lên ngai, dải sáng chạy ngang.
- **Q:** (18117, 18123): ẩn NT, J, NU, chỉ còn phụ đề và nhãn quân.
- **NT (ngoài Q):** 18113 "tang lễ chưa xong"; 18126 "Lý Thái Tông". Chỉ hai cái.
- **J:** không dùng (cảnh đau thương trong hoàng tộc, không đùa).
- **Âm thanh:** trống dồn nhưng đều; bước chân, cửa gỗ nặng đóng mở; vó ngựa (18121) hạ nhỏ; tắt hết khi 18119 (áo tang); sau 18123 mọi tiếng tắt đột ngột, chỉ còn chuông.

### Chương 12: Kết (18127–18134)
- **Hình:** sơ đồ thành, bốn nơi sáng lần lượt đúng thứ tự trong 18127: Tường Phù, Quảng Phúc, Càn Nguyên, Long An. Ô năm: 1010 rồi nhảy 1028 khi đọc 18129. 18130–18131 cửa tây sáng, một dòng sáng nối tới điện Càn Nguyên. 18132 hiện lại chữ nhỏ "Đại La?" mờ rồi tan. 18133 ô năm chạy tới đầu thế kỷ mười ba (hơn hai trăm năm nhà Lý). 18134 camera kéo ra cao dần: toàn cảnh Thăng Long nhìn từ trên cao, thuyền trên sông, nhãn "Thăng Long" sáng nhất rồi mờ dần ra kết.
- **NT:** 18133 "hơn 200 năm" (một cái duy nhất). Không thẻ HẾT.
- **Âm thanh:** sóng sông trở lại; giọng kể chậm ở 18134; mờ dần cả hình lẫn tiếng.

## 2b. Tiểu cảnh phóng vào (bổ sung theo yêu cầu 27/10: nhiều hiệu ứng hơn, kiểu cày ruộng ở demo Lê Hoàn)
Cách làm giống `plough`: từ một điểm trên bản đồ, một khung tranh nhỏ phóng ra, có người và vật chuyển động nhẹ trong vài giây, rồi thu về. Khai báo bằng `PROPS.append((t0, t1, loại, kinh độ, vĩ độ, tham số, cỡ))`. Mỗi lúc chỉ một tiểu cảnh, không đặt trong đoạn `Q` giao tranh, cờ và biển để trơn, không chữ. Gồm 23 tiểu cảnh; chín cảnh dùng lại hình đã có trong `mapprops.py` (`calendar`, `banner`, `meeting`, `scrolls2`, `granary`, `storm`, `tomb`, `ditch`, khung `orange`), khoảng 16 hình còn lại phải vẽ mới.

| Câu | Tiểu cảnh | Chuyển động | Trạng thái |
|---|---|---|---|
| 18001 | **Tờ lịch** ở châu Cổ Pháp: số ngày chạy tới 12, hiện chữ "tháng hai" | Lật số | Dùng lại `calendar` |
| 18004 | **Sân chùa**: người mẹ đưa cậu bé tới, nhà sư đưa tay đón, chuông chùa rung | Bước đi, chuông đung đưa, khói hương | Vẽ mới `chua` |
| 18006 | **Đổi triều**: lá cờ nhà Đinh hạ xuống, cờ nhà Tiền Lê kéo lên (cờ trơn) | Cờ kéo lên cột | Dùng lại `banner`, đổi màu |
| 18008-18010 | **Chùa Lục Tổ**: cậu bé đọc thẻ tre bên sư Vạn Hạnh; sau đó mặc áo võ quan đứng gác | Lật thẻ tre, hóa trang bằng mờ chồng | Vẽ mới `hoc_chua` |
| 18014-18016 | **Ngai vàng trống** giữa điện: ba bóng hoàng tử xoay quanh, một bóng lùi ra, chỉ còn một bóng đứng cạnh ngai | Bóng xoay, ngai sáng tắt | Vẽ mới `ngai_tranh` |
| 18017 | **Điện vắng**: các quan chạy ra cửa, chỉ một người quỳ lại cạnh tấm vải trắng (không vẽ thi thể) | Quan chạy, một bóng quỳ, đèn lung lay | Vẽ mới `quy_khoc` |
| 18021 | **Quả khế bổ đôi**, lòng quả có hạt mận lộ ra, quả bị xoay chậm | Quả xoay, ánh sáng loé | Dùng khung `orange`, vẽ mới ruột quả `khe` |
| 18027-18028 | **Hai đội 500 quân** đứng hai bên ngai (hai hàng icon nhỏ), nhãn "500" ở mỗi hàng | Hàng quân xếp ngay ngắn | Vẽ mới `hai_doi` |
| 18030-18035 | **Đêm đèn dầu**: hai bóng người sát nhau, đèn dầu chập chờn, bóng một người giơ tay (giả vờ mắng), bóng kia lùi | Ngọn đèn dầu lung lay, bóng đổ trên tường | Vẽ mới `den_dau` |
| 18036-18038 | **Họp của các quan**: vòng tròn quan quanh bàn, từng người gật đầu | Gật đầu lần lượt | Dùng lại `meeting` |
| 18039-18040 | **Lên ngôi**: một bóng được dìu lên bậc điện, hàng quan cúi xuống từng lớp, cờ phất | Quan cúi theo sóng, cờ bay | Vẽ mới `len_ngoi` |
| 18049 | **Hoa Lư giữa núi đá**: núi dựng như tường thành, quân giữ ở cửa ải hẹp | Cờ bay, mây trôi qua đỉnh núi | Vẽ mới `nui_da` |
| 18068-18069 | **Cuộn chiếu** mở ra dài, cọ viết lướt, rồng cuộn hổ ngồi hiện mờ sau lưng | Cuộn mở, nét cọ chạy | Dùng lại `scrolls2`, vẽ thêm cọ viết `co_viet` |
| 18073-18075 | **Rồng vàng** cuộn bay lên từ mặt sông, thuyền nhỏ dưới chân thành, nhãn "theo lời kể" | Rồng uốn, sóng vỗ | Vẽ mới `rong_vang` |
| 18076-18079 | **Dựng thành**: thợ nâng cột, đắp tường, đào hào, bốn cửa lần lượt dựng lên | Thợ khiêng, bụi bay, hào đầy nước | Vẽ mới `dung_thanh`, dùng lại `ditch` |
| 18083-18084 | **Kho thóc** mở cửa, thóc chảy ra chia cho dân (thuế được miễn) | Thóc rơi, người nhận | Dùng lại `granary` |
| 18093-18096 | **Bão Biện Sơn**: thuyền nhỏ giữa sấm chớp, bóng vua đốt hương, mây tan sau lời khấn (theo lời kể) | Mưa xiên, tia chớp, khói hương, trời sáng | Dùng lại `storm`, vẽ thêm khói hương `huong` |
| 18104 | **Đúc chuông**: lò rực lửa, đổ đồng vào khuôn, chuông treo lên gác | Lửa bập bùng, tia đồng nóng chảy | Vẽ mới `duc_chuong` |
| 18110 | **Nhật thực**: vòng đen che dần mặt trời, chim bay về tổ, ánh sáng tối đi | Vòng đen trượt, màn tối | Vẽ mới `nhat_thuc` |
| 18112 | **Thọ Lăng**: gò đất và bia đá, khói hương bay lên | Khói hương | Dùng lại `tomb` |
| 18114-18116 | **Cửa Quảng Phúc**: cánh cửa gỗ nặng, bóng quân giấu sau cánh, thái tử đi vào từ cửa Tường Phù | Cửa khép mở, bóng quân động | Vẽ mới `cua_thanh` |
| 18119 | **Thái tử mặc áo tang** đứng cạnh linh cữu trắng, nến đèn lung lay | Áo tang bay nhẹ, đèn dầu | Vẽ mới `ao_tang` |
| 18126 | **Lên ngôi lần hai**: ngai vàng sáng, bóng thái tử bước lên | Bước lên bậc | Dùng lại `len_ngoi` |

**Thêm hiệu ứng nhỏ trên bản đồ (không phải tiểu cảnh):**
- `ping` nhấp nháy ở Cổ Pháp, Hoa Lư, Đại La khi nhắc tới tên lần đầu.
- Đường nét đứt chạy từ Hoa Lư tới Đại La (18056, 18072), thuyền chạy dọc theo đường.
- `REGIONS` (vùng được tô màu): câu 18088, mười đạo được tô màu, rồi tách ra thành hai mươi bốn lộ, mỗi lộ một sắc nhạt khác nhau.
- Lớp đêm `NIGHT` ở chương 3 (18030–18035) và lớp tối nhật thực ở chương 10.
- `FX` đã có: `horn`, `trumpet`, `gong`, `drums`, `volley`, `crack` (cửa nặng), `thunder`, `sea`, `splash`. Thêm tiếng mới: chuông chùa, dế đêm, búa đục, mái chèo.

## 2c. Làm lại cờ và dấu hiệu quân (chủ kênh nhận xét 27/10: cờ chiến còn đơn giản)
**Cờ đang đại diện cho gì (theo mã hiện có):**
- Lá cờ cắm cạnh mỗi cụm quân (`flag` trong `mapfilm3.py`): đánh dấu **phe của cụm quân** bằng màu cờ; khi quân thua, cờ chuyển xám và thu nhỏ.
- Hàng cờ nhỏ (`pennants`): đánh dấu **nơi đóng quân hoặc nơi một phe đang có mặt**.
- Lá cờ trên thẻ nhân vật (`card3`): chỉ **màu phe của nhân vật**.
- Phù hiệu tròn trên thẻ tên quân: **phe** (không phải cá nhân).
Như vậy cờ chỉ nói "bên nào", cùng một việc với màu thẻ tên, nên trong video này cờ cạnh quân là phần thừa nhất.

Hiện nay cờ chỉ là một cột với một mảnh tam giác phẳng (`flag` trong `mapdraw.py`), hàng cờ nhỏ (`pennants`) và huy hiệu tròn trên thẻ tên. Đề xuất thay bằng năm thứ sau, ảnh thử `ke-hoach/anh-thu/co_demo.png`:

1. **Cờ vải lượn sóng:** vải gợn theo gió, sáng tối theo nếp, viền vàng hai mép, tua rua ở mép phải, đầu cột có mũi nhọn. Hướng gió thuận theo hướng quân đi.
2. **Cờ phướn dài:** dải cờ treo dọc dưới thanh ngang, đuôi răng cưa, hai đai vàng; dùng cho đạo quân lớn, đoàn thuyền và điện lớn.
3. **Lọng vàng và quạt lông:** đi theo vua và thái tử, giúp nhận ra "nhà vua đi đâu" mà không cần chữ. Dùng ở chương 3, 7, 11 và 12.
4. **Quân cầm cờ:** trong mỗi cụm quân, cứ vài lính có một lính cầm cờ riêng, cờ bay theo bước đi; tướng dẫn đầu cầm cờ lớn hơn. Cờ chỉ có màu và dải viền, không chữ, không biểu tượng.
5. **Cờ đổi theo trạng thái:** thắng thì cờ dựng thẳng, thua thì cờ rũ rồi đổ xuống, đổi triều thì cờ cũ hạ xuống và cờ mới kéo lên (câu 18006, 18039–18041).

**Thay những chỗ đang dùng cờ:**
- Hàng cờ `pennants` ở đóng quân → **trại quân**: lều, cờ vải nhỏ, khói bếp, lính đi tuần (dùng `camp` có sẵn rồi nâng cấp).
- Cờ đánh dấu chiếm thành → **cột cờ trên tường thành**, cờ kéo lên theo nhịp.
- Phù hiệu tròn trên thẻ tên → giữ nhưng thêm **viền theo màu cờ** để khớp với cờ vải.
- Dấu chấm nhấp nháy `ping` ở địa danh → giữ chỗ nhắc tên lần đầu, không dùng thay cờ.
- Cờ mọi bên đều để trơn một màu theo màu phe; không chữ, không hình trên cờ.

## 2d. Chân dung nhân vật (icon tròn xuất hiện khi nhắc tên lần đầu)
Demo Lê Hoàn đã có sẵn cơ chế này: lệnh `FACE(n, giây, thời gian, tên, địa danh, loại, màu phe)` làm một huy hiệu tròn nảy lên cạnh địa danh, viền theo màu phe. Chủ kênh đã loại hình khuôn vẽ phẳng theo vai trò (27/10: xấu); video này chỉ dùng ảnh chân dung vẽ bằng AI `assets/icon_nhan_vat/<tên không dấu>.jpg`. Danh sách lệnh vẽ: `ke-hoach/nhan-vat/LY1F_anh.json` (16 chân dung và hai hình minh họa rồng vàng, quả khế). Đã có sẵn `lehoan.jpg` và `vuatong.jpg`; các nhân vật còn lại cần vẽ mới.

| Nhân vật | Xuất hiện | Màu viền | Mô tả chân dung (ảnh minh họa, không phải khuôn mặt có thật) |
|---|---|---|---|
| Lý Công Uẩn, cậu bé | 18004 | xanh lá (nhà Lý) | Cậu bé khoảng ba, bốn tuổi, tóc búi hai bên, áo vải nâu, nền sân chùa |
| Lý Công Uẩn, tướng trẻ | 18010 | xanh lá | Người trẻ khoảng hai mươi lăm tuổi, vóc người cao tuấn tú, mũ võ quan, áo giáp nhẹ, tay không |
| Lý Công Uẩn, nhà vua | 18039 | xanh lá | Người đàn ông ngoài ba mươi, mũ vua và áo bào vàng đơn giản, ánh mắt điềm tĩnh |
| Lý Khánh Văn | 18004 | nâu (nhà chùa) | Thiền sư trung niên, đầu cạo, áo nâu |
| Vạn Hạnh | 18007 | nâu | Sư già, đầu cạo, áo nâu, râu thưa |
| Lê Hoàn | 18006 | vàng đồng (Tiền Lê) | Dùng lại `lehoan.jpg` |
| Lê Long Việt | 18016 | vàng đồng | Người trẻ mặc áo bào vua, vẻ non nớt |
| Lê Long Đĩnh | 18016 | vàng đồng | Người đàn ông gầy, sắc mặt nhợt nhạt, mũ vua, ánh mắt khó đoán (không vẽ biểu cảm quái dị) |
| Nguyễn Đê | 18027 | vàng đồng | Tướng quân trung niên, mũ võ, râu ngắn |
| Đào Cam Mộc | 18029 | xanh lá | Quan hầu cận trung niên, mũ quan, râu mỏng, vẻ lanh lợi |
| Lý Phật Mã | 18043 | xanh lá | Thái tử trẻ, tóc búi cao, trán rộng; sau lên ngôi thành vua Lý Thái Tông (18126) mặc áo vua |
| Cao Biền (Cao Vương) | 18057 | xám xanh (nhà Đường) | Tướng nhà Đường, mũ giáp nhà Đường, râu dài |
| Vua Tống | 18065 | đỏ (nhà Tống) | Dùng lại `vuatong.jpg` |
| Dực Thánh Vương | 18100 | xanh lá | Hoàng tử cầm quân, mũ giáp, vẻ nghiêm nghị |
| Đông Chinh Vương | 18115 | cam (phản loạn) | Hoàng tử trung niên, áo hoàng tộc |
| Vũ Đức Vương | 18115 | cam | Hoàng tử trẻ, áo hoàng tộc |
| Lý Nhân Nghĩa | 18120 | xanh lá | Hoạn quan trung niên, mũ nhỏ, không râu |
| Lê Phụng Hiểu | 18121 | xanh lá | Võ tướng vạm vỡ, giáp nhẹ, vẻ dũng mãnh; **tay không**, không vẽ gươm trần |

Cách vẽ: mỗi người một khuôn mặt khác nhau, cùng phong cách hoạt hình phẳng với bộ có sẵn, không chữ, không biểu tượng trên mũ áo, nền một màu giấy; trang phục theo thời Lý và Tiền Lê, không vẽ đồ thời sau; không vẽ vũ khí trần. Tuổi theo năm đang kể (Lý Công Uẩn sinh 974). Cần hai đến ba bản mỗi nhân vật rồi chọn bản đúng nhất; xem từng ảnh ở cỡ lớn trước khi dùng. Vẽ bằng workflow vẽ ảnh khi chủ kênh cho chạy. Nhân vật nhà Tống, Cao Biền chỉ hiện một lần.

Mỗi lần hiện chân dung dùng tối đa 3 giây, không đặt trong đoạn `Q`; chỉ một chân dung hiện cùng lúc, không trùng với thẻ nhân vật (`C3`).

## 3. Quy tắc chung của video này
1. **Không đùa các anh hùng và nhân vật chính:** chỉ khung đùa nhắm vào tình huống hoặc quân xâm lược; không đùa Lý Công Uẩn, Lý Thái Tông, Lý Phật Mã, Đào Cam Mộc, Lê Phụng Hiểu, Lê Hoàn; không đùa cái chết hay bệnh tật của Lê Long Đĩnh.
2. **Không máu, không cảnh giết:** chết/thua dùng cờ rũ, chuyển xám, "THUA TRẬN" hoặc "BỊ DIỆT" nhỏ; tránh đầu lâu to.
3. **Truyền thuyết có nhãn:** rồng vàng (18073), gió sấm yên sau lời khấn (18096), lời sư Vạn Hạnh (18007): luôn có nhãn nhỏ "theo lời kể" hoặc "chưa chắc", đúng với câu trong lời kể.
4. **Ghi chú nổi:** tổng cộng khoảng 25–30 cái cho cả video, mỗi cái tối đa 3,5 giây, không đặt trong đoạn `Q`.
5. **Khung đùa:** tối đa 2 cái mỗi chương, thực tế đề xuất chỉ 1–2 cái cho cả video (chương 2 và chương 9), chủ kênh duyệt.
6. **Bố cục:** nhãn quân và nhãn thành dùng `soff` để không đè nhau; quân đứng yên `spread` 0,45–0,6; thẻ nhân vật chỉ ở lần xuất hiện đầu (Lý Công Uẩn, Lê Long Đĩnh, Đào Cam Mộc, Lê Phụng Hiểu, Lý Phật Mã).
7. **Màu phe:** Đại Việt (nhà Lê rồi nhà Lý) xanh lá, giữ cùng một màu qua đổi triều và chỉ đổi phù hiệu; nhà Tống đỏ; Nam Chiếu tím; giặc Cử Long xám nâu; quân phản loạn cam (chỉ ở chương 11).
8. **Chữ trong khung:** mọi thẻ tự xuống dòng hoặc thu nhỏ, lề tối thiểu 60 px; kiểm hộp bao chữ trước khi dựng.

## 4. Quy trình sau khi chủ kênh duyệt (không tự chạy workflow)
1. Viết `phim_ban_do/ly1_content.py` theo mẫu `hs1_content.py`.
2. Chạy `kiem_kich_ban.py ly1` (còn đoạn 18001 dài 45 chữ, quyết định giữ hay tách).
3. Chủ kênh bảo mới chạy giọng (`cum.txt`, tone `story`), nhận dạng, `kiem_giong.py`, chuẩn hóa âm lượng và tốc độ, `phude_tinh.py`.
4. Xem các khung hình thật (đầu, giữa, nhiều quân nhất, câu cuối) bằng `mapfilm3.py still`.
5. Dựng, rồi `kiem_video.py` đến khi không còn ❌; đo thời lượng thật (≥ 10 phút), làm bìa có logo.

## 5. Điểm cần chủ kênh quyết
- Có dùng hai khung đùa (câu 18021 chuyện quả khế, câu 18101 Nam Chiếu mất ngựa) hay không dùng khung đùa nào.
- Câu hook 18011: giữ một dấu hỏi mờ hay để hoàn toàn không hiệu ứng.
- Vị trí gần đúng của Kim Hoa, Biện Sơn có chấp nhận ghi "vị trí gần đúng".
- Có thêm một lớp tua nhanh năm tháng ở chương 1 hay giữ ô năm đơn giản.
