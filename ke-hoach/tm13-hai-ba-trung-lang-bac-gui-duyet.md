# tm13 Hai Bà Trưng 40–43, bản 3: kể kèm phân tích (cổng C), 19/11/2026

**Trạng thái: CHỜ CHỦ KÊNH DUYỆT CỔNG C.** Chưa đọc giọng, chưa dựng. Lời đọc ở `ke-hoach/thu-giong-hai/tm13_full.json` (đoạn 188001–188017). Hook 1 do chủ kênh chọn 19/11.

17 đoạn, 976 chữ, khoảng 5.2 phút. Mạch truyện bản 2 dự kiến 4 đến 5 phút. Mẫu: tm11m bản 3.

## 0. Đã sửa so với bản 2 (bản 2 vừa gửi sáng nay chưa áp dụng quy tắc kể kèm phân tích)
- Bản 2 tôi viết đúng giới hạn 32 chữ và 2 câu cũ, ít phân tích, còn có lời cảm ơn cuối: chưa đúng `nguyen-tac-cot-loi.md` mục 10 và 10b hiện hành, vì trước khi viết tôi chưa đọc lại bản mới của quy tắc.
- Bản 3: bỏ giới hạn chữ và câu, ghép các đoạn ngắn thành đoạn theo nhịp kể, thêm 8 chỗ phân tích (bảng mục 3), bỏ lời cảm ơn cuối (mục 10: lời cảm ơn không bắt buộc). Bản 2 giữ ở `phim_ban_do/thuymac/viet_tm13_v2.py`.
- Thành thật về thứ tự làm: tôi viết đoạn từ mạch truyện đã duyệt rồi ghép lại, chưa viết một bản văn xuôi liền trước như `giong-van.md` mục 1 đòi. Mục 1 dưới đây là các đoạn ghép lại theo nhịp kể để anh đọc liền; nếu anh muốn tôi viết lại từ bản văn xuôi riêng thì nói.

## 1. Văn xuôi liền mạch (các đoạn ghép lại)

Viên thái thú nhà Hán bỏ chạy khỏi quận, vì hai người phụ nữ.

Ông ta tên Tô Định, quan đứng đầu quận Giao Chỉ, vùng đồng bằng sông Hồng mà nhà Hán đã cai trị hơn một trăm bốn mươi năm. Hai người phụ nữ ấy là chị em, Trưng Trắc và Trưng Nhị. Khi họ dấy binh, Cửu Chân, Nhật Nam và Hợp Phố đều hưởng ứng, sáu mươi lăm thành đáp lại.

Thế mà ba năm sau, cuộc nổi dậy đã tắt. Vì sao một tiếng gọi được cả vùng đáp lại, rồi vẫn không giữ nổi?

Trưng Trắc là con gái một Lạc tướng ở Mê Linh, người đứng đầu một vùng đất, và là vợ của Thi Sách ở Chu Diên. Theo sử ta, Tô Định dùng luật nhà Hán trói buộc dân Giao Chỉ, lại giết Thi Sách. Trưng Trắc tìm cách trả thù.

Mùa xuân năm bốn mươi, bà cùng em là Trưng Nhị dấy binh. Họ chiếm được nơi đặt trụ sở của quan nhà Hán, và Tô Định bỏ chạy về Nam Hải. Trưng Trắc xưng vương, đóng đô ở Mê Linh, quê bà.

Sử ta nói bà khởi binh để trả thù cho chồng. Nhưng sử cũng chép Tô Định trói buộc cả dân Giao Chỉ, chứ không riêng gia đình bà, nên có thể hiểu vì sao tiếng gọi của bà vang xa hơn một nhà. Còn mỗi vùng hưởng ứng vì lý do gì thì sử không nói.

Nhưng nhà Hán không bỏ quận ấy. Triều đình ở Lạc Dương chậm tay, đến năm bốn mươi hai mới sai tướng Mã Viện đem quân sang. Sử không nói vì sao chậm. Một tài liệu nhận xét rằng việc nhà Hán cử những tướng được tin cậy nhất cho thấy họ coi Giao Chỉ là vùng quan trọng.

Mã Viện mang hiệu Phục Ba tướng quân, vị tướng dẹp sóng. Quân đi qua vùng núi hiểm trở, còn thuyền chở lương chạy dọc bờ biển từ Quảng Đông theo sau. Số quân các sách ghi không giống nhau, từ chừng một vạn đến hơn ba vạn. Về quân của hai bà, sử không ghi con số nào, nên ta không thể đặt hai bên lên cân.

Mã Viện đánh hai bà ở Lãng Bạc, theo Toàn thư, bộ sử nước ta soạn thời nhà Lê. Sách xưa chép Lãng Bạc là Hồ Tây, người nay cho là vùng núi Tiên Du ở Bắc Ninh. Nhà nghiên cứu Ben Kiernan ghi quân nhà Hán chém hàng nghìn người theo hai bà, hơn mười nghìn người ra hàng. Nguồn khác ghi số người ra hàng còn lớn hơn.

Sau trận ấy, hai bà lui về Cấm Khê. Theo Toàn thư, nhiều người theo hai bà bỏ đi, vì cho rằng người đứng đầu là phụ nữ thì không thể thắng. Sử không nói bao nhiêu người bỏ đi, nên ta không biết điều ấy nặng đến đâu so với hàng nghìn người đã ngã xuống và hơn mười nghìn người đã ra hàng ở Lãng Bạc.

Cấm Khê ở đâu, đến nay chưa ai chỉ chắc. Sử cũ ghi vùng Vĩnh Tường ở Sơn Tây xưa, còn sách khác chép bà trốn vào hang ở Kim Khê. Mã Viện đuổi theo, đánh nhiều trận. Hậu Hán thư, bộ sử của phía nhà Hán, chép quân hai bà thua nhiều lần rồi tan chạy. Sang năm bốn mươi ba, hai chị em vẫn chống trả, nhưng đã bị cô lập và thua trận.

Hai bà mất ra sao thì sách kể khác nhau. Hậu Hán thư thì chép Mã Viện chém hai bà và nhiều người khác, gửi đầu về Lạc Dương. Toàn thư của ta chỉ ghi hai bà thua trận. Sử triều Nguyễn thì ghi hai bà bị bắt, còn cách mất thế nào cả hai bộ đều không nói.

Chuyện hai bà gieo mình xuống sông Hát không thấy trong hai bộ sử ấy. Đó là điều người đời giữ lại, gắn với đền thờ ở Hát Môn. Như vậy cái chết của hai bà có ba lớp kể, lớp của phía nhà Hán, lớp sử ta không nói rõ và lớp dân gian, và không lớp nào thay được lớp nào.

Sau khi thắng, theo ước tính của Ben Kiernan, quân nhà Hán giết khoảng năm đến mười nghìn người thuộc tầng lớp thủ lĩnh Lạc Việt và đưa vài trăm gia đình về Trung Quốc. Mã Viện còn cho nấu chảy trống đồng, vật các nhà nghiên cứu coi là biểu tượng quyền của thủ lĩnh Lạc Việt, đúc thành tượng ngựa, mùa thu năm bốn mươi bốn mang về dâng vua.

Phía nhà Hán cũng trả giá. Theo Hậu Hán thư, khi về kinh, quân của Mã Viện đã chết bốn, năm phần mười vì khí độc và dịch bệnh. Nhưng con số này tính cho cả chiến dịch, nên nó không cho ta biết riêng trận đánh với hai bà làm nhà Hán mất bao nhiêu người.

Vậy vì sao một tiếng gọi được sáu mươi lăm thành đáp lại mà không giữ nổi? Sử không đưa ra một lý do duy nhất. Sử chỉ ghi một đạo quân có thuyền chở lương theo bờ biển, và ghi rằng sau Lãng Bạc nhiều người đã bỏ đi. Sử gia Lê Văn Hưu thì nghĩ khác những người bỏ đi ấy, ông cho rằng việc hai bà là nữ giới không phải cớ để người nước ta tự coi thường mình.

Ngô Sĩ Liên, người soạn Toàn thư, ca ngợi khí phách của hai bà và tin rằng linh khí hai bà vẫn che chở dân sau khi mất. Hai người phụ nữ làm vua ba năm, và đến nay sử vẫn kể cái chết của họ theo những cách khác nhau.

## 2. Chia đoạn cho giọng đọc (theo nhịp kể)

**188001.** Viên thái thú nhà Hán bỏ chạy khỏi quận, vì hai người phụ nữ.

**188002.** Ông ta tên Tô Định, quan đứng đầu quận Giao Chỉ, vùng đồng bằng sông Hồng mà nhà Hán đã cai trị hơn một trăm bốn mươi năm. Hai người phụ nữ ấy là chị em, Trưng Trắc và Trưng Nhị. Khi họ dấy binh, Cửu Chân, Nhật Nam và Hợp Phố đều hưởng ứng, sáu mươi lăm thành đáp lại.

**188003.** Thế mà ba năm sau, cuộc nổi dậy đã tắt. Vì sao một tiếng gọi được cả vùng đáp lại, rồi vẫn không giữ nổi?

**188004.** Trưng Trắc là con gái một Lạc tướng ở Mê Linh, người đứng đầu một vùng đất, và là vợ của Thi Sách ở Chu Diên. Theo sử ta, Tô Định dùng luật nhà Hán trói buộc dân Giao Chỉ, lại giết Thi Sách. Trưng Trắc tìm cách trả thù.

**188005.** Mùa xuân năm bốn mươi, bà cùng em là Trưng Nhị dấy binh. Họ chiếm được nơi đặt trụ sở của quan nhà Hán, và Tô Định bỏ chạy về Nam Hải. Trưng Trắc xưng vương, đóng đô ở Mê Linh, quê bà.

**188006.** Sử ta nói bà khởi binh để trả thù cho chồng. Nhưng sử cũng chép Tô Định trói buộc cả dân Giao Chỉ, chứ không riêng gia đình bà, nên có thể hiểu vì sao tiếng gọi của bà vang xa hơn một nhà. Còn mỗi vùng hưởng ứng vì lý do gì thì sử không nói.

**188007.** Nhưng nhà Hán không bỏ quận ấy. Triều đình ở Lạc Dương chậm tay, đến năm bốn mươi hai mới sai tướng Mã Viện đem quân sang. Sử không nói vì sao chậm. Một tài liệu nhận xét rằng việc nhà Hán cử những tướng được tin cậy nhất cho thấy họ coi Giao Chỉ là vùng quan trọng.

**188008.** Mã Viện mang hiệu Phục Ba tướng quân, vị tướng dẹp sóng. Quân đi qua vùng núi hiểm trở, còn thuyền chở lương chạy dọc bờ biển từ Quảng Đông theo sau. Số quân các sách ghi không giống nhau, từ chừng một vạn đến hơn ba vạn. Về quân của hai bà, sử không ghi con số nào, nên ta không thể đặt hai bên lên cân.

**188009.** Mã Viện đánh hai bà ở Lãng Bạc, theo Toàn thư, bộ sử nước ta soạn thời nhà Lê. Sách xưa chép Lãng Bạc là Hồ Tây, người nay cho là vùng núi Tiên Du ở Bắc Ninh. Nhà nghiên cứu Ben Kiernan ghi quân nhà Hán chém hàng nghìn người theo hai bà, hơn mười nghìn người ra hàng. Nguồn khác ghi số người ra hàng còn lớn hơn.

**188010.** Sau trận ấy, hai bà lui về Cấm Khê. Theo Toàn thư, nhiều người theo hai bà bỏ đi, vì cho rằng người đứng đầu là phụ nữ thì không thể thắng. Sử không nói bao nhiêu người bỏ đi, nên ta không biết điều ấy nặng đến đâu so với hàng nghìn người đã ngã xuống và hơn mười nghìn người đã ra hàng ở Lãng Bạc.

**188011.** Cấm Khê ở đâu, đến nay chưa ai chỉ chắc. Sử cũ ghi vùng Vĩnh Tường ở Sơn Tây xưa, còn sách khác chép bà trốn vào hang ở Kim Khê. Mã Viện đuổi theo, đánh nhiều trận. Hậu Hán thư, bộ sử của phía nhà Hán, chép quân hai bà thua nhiều lần rồi tan chạy. Sang năm bốn mươi ba, hai chị em vẫn chống trả, nhưng đã bị cô lập và thua trận.

**188012.** Hai bà mất ra sao thì sách kể khác nhau. Hậu Hán thư thì chép Mã Viện chém hai bà và nhiều người khác, gửi đầu về Lạc Dương. Toàn thư của ta chỉ ghi hai bà thua trận. Sử triều Nguyễn thì ghi hai bà bị bắt, còn cách mất thế nào cả hai bộ đều không nói.

**188013.** Chuyện hai bà gieo mình xuống sông Hát không thấy trong hai bộ sử ấy. Đó là điều người đời giữ lại, gắn với đền thờ ở Hát Môn. Như vậy cái chết của hai bà có ba lớp kể, lớp của phía nhà Hán, lớp sử ta không nói rõ và lớp dân gian, và không lớp nào thay được lớp nào.

**188014.** Sau khi thắng, theo ước tính của Ben Kiernan, quân nhà Hán giết khoảng năm đến mười nghìn người thuộc tầng lớp thủ lĩnh Lạc Việt và đưa vài trăm gia đình về Trung Quốc. Mã Viện còn cho nấu chảy trống đồng, vật các nhà nghiên cứu coi là biểu tượng quyền của thủ lĩnh Lạc Việt, đúc thành tượng ngựa, mùa thu năm bốn mươi bốn mang về dâng vua.

**188015.** Phía nhà Hán cũng trả giá. Theo Hậu Hán thư, khi về kinh, quân của Mã Viện đã chết bốn, năm phần mười vì khí độc và dịch bệnh. Nhưng con số này tính cho cả chiến dịch, nên nó không cho ta biết riêng trận đánh với hai bà làm nhà Hán mất bao nhiêu người.

**188016.** Vậy vì sao một tiếng gọi được sáu mươi lăm thành đáp lại mà không giữ nổi? Sử không đưa ra một lý do duy nhất. Sử chỉ ghi một đạo quân có thuyền chở lương theo bờ biển, và ghi rằng sau Lãng Bạc nhiều người đã bỏ đi. Sử gia Lê Văn Hưu thì nghĩ khác những người bỏ đi ấy, ông cho rằng việc hai bà là nữ giới không phải cớ để người nước ta tự coi thường mình.

**188017.** Ngô Sĩ Liên, người soạn Toàn thư, ca ngợi khí phách của hai bà và tin rằng linh khí hai bà vẫn che chở dân sau khi mất. Hai người phụ nữ làm vua ba năm, và đến nay sử vẫn kể cái chết của họ theo những cách khác nhau.

## 3. Bảng phân tích (năm điều kiện của người kể)
| Đoạn | Câu phân tích | Dựa vào sự việc nào (đã kể trong video, có nguồn) | Rào đón và giới hạn |
|---|---|---|---|
| 188006 | có thể hiểu vì sao tiếng gọi của bà vang xa hơn một nhà; mỗi vùng hưởng ứng vì lý do gì thì sử không nói | Tô Định trói buộc cả dân Giao Chỉ; sáu mươi lăm thành hưởng ứng (Toàn thư NK 3/2a–3a) | "có thể hiểu"; nói rõ sử không nêu lý do từng vùng; không nói đó là nguyên nhân khởi nghĩa |
| 188007 | nhà Hán cử tướng được tin cậy nhất cho thấy họ coi Giao Chỉ là vùng quan trọng; sử không nói vì sao chậm | Nhà Hán sai Mã Viện năm bốn mươi hai (Toàn thư; Hậu Hán thư qua Wikipedia) | Gắn "một tài liệu nhận xét"; nói thẳng sử không nói lý do chậm tay |
| 188008 | sử không ghi quân hai bà bao nhiêu nên không đặt hai bên lên cân | Số quân Hán các sách ghi khác nhau; quân hai bà không có số | Chỉ nói chỗ sử thiếu, không ước lượng |
| 188010 | sử không nói bao nhiêu người bỏ đi nên không biết nặng đến đâu so với số người ngã xuống và ra hàng | Toàn thư ghi nhiều người bỏ đi (NK 3/2b); Kiernan ghi số chém và ra hàng ở Lãng Bạc | Nói thẳng sử không có số; không nói họ bỏ đi là lý do thua |
| 188013 | cái chết của hai bà có ba lớp kể (phía nhà Hán, sử ta không nói rõ, dân gian), không lớp nào thay được lớp nào | Hậu Hán thư chép chém; Toàn thư không mô tả; Cương mục ghi bị bắt; sông Hát chỉ có trong lời kể dân gian (đã kể ở 188012–188013) | So sánh nguồn, không chọn một cách; không nói cách nào đúng |
| 188014 | các nhà nghiên cứu coi trống đồng là biểu tượng quyền của thủ lĩnh Lạc Việt | Mã Viện nấu trống đồng đúc ngựa mùa thu 44 (Hậu Hán thư qua Bielestein; Bronze drum) | Gắn "các nhà nghiên cứu coi là"; không nói Mã Viện nghĩ gì khi làm |
| 188015 | con số chết tính cho cả chiến dịch, không cho biết riêng trận đánh với hai bà | Hậu Hán thư: bốn, năm phần mười chết vì khí độc và dịch bệnh khi về kinh | Chỉ giới hạn phạm vi con số; không nói nhà Hán yếu đi vì nó |
| 188016 | sử không đưa ra một lý do duy nhất; sử chỉ ghi thuyền chở lương theo bờ biển và người bỏ đi; Lê Văn Hưu nghĩ khác những người bỏ đi | Đoạn 188007–188010; Lê Văn Hưu (Toàn thư NK 3/3a) | Trả lời câu hỏi hook bằng điều sử ghi; không xếp hạng điều nào nặng hơn; lời của Lê Văn Hưu gắn tên |

## 4. Bảng nguồn từng dữ kiện
Nguồn: T = Toàn thư NK 3 (bản dịch Hawaii, đã đọc); C = Cương mục Tiền biên quyển 2 (Hawaii, đã đọc); W = Wikipedia (Trưng sisters' rebellion, Trưng sisters, Bronze drum) dẫn Bielestein, Yü, Kiernan 2019, Lai 2015; HHT = Hậu Hán thư, CHƯA đọc bản gốc, chỉ qua W.

| Đoạn | Dữ kiện | Nguồn | Mức |
|---|---|---|---|
| 188001–188003 | Tô Định bỏ chạy; Giao Chỉ; hơn 140 năm dưới nhà Hán; Cửu Chân, Nhật Nam, Hợp Phố; 65 thành | T (110 trước CN đến 39), NK 3/2a–3a | Đủ |
| 188004 | Trưng Trắc con gái Lạc tướng ở Mê Linh, vợ Thi Sách ở Chu Diên; Tô Định dùng luật, giết Thi Sách | T NK 3/2a (HHT và Giao Châu ngoại vực ký nói khác về Thi Sách, không dùng) | Một chính sử, gắn "theo sử ta" |
| 188005 | Mùa xuân 40 dấy binh, chiếm trị sở, Tô Định về Nam Hải, xưng vương ở Mê Linh | T NK 3/2a–2b (tháng hai âm lịch; W ghi tháng ba) | Đủ, chỉ nói "mùa xuân" |
| 188007 | Năm 42 sai Mã Viện; Lạc Dương chậm; tướng tin cậy | T; W (HHT, Bielestein) | Chậm tay là W; chưa đọc HHT |
| 188008 | Phục Ba tướng quân; thuyền chở lương từ Quảng Đông; số quân một đến ba vạn | W (Bielestein, Yü, Kiernan); các trang W không khớp số | Nói khoảng, nêu thẳng các nguồn khác nhau |
| 188009 | Lãng Bạc (Hồ Tây hay Tiên Du); chém hàng nghìn, hơn mười nghìn ra hàng | T/C (Dâm Đàm = Hồ Tây); W Kiernan; nguồn khác hơn hai vạn | Địa điểm tranh cãi, nói thẳng |
| 188010 | Lui về Cấm Khê; nhiều người theo bỏ đi vì chủ là phụ nữ | T NK 3/2b | Một chính sử, lời sử gia chép |
| 188011 | Cấm Khê: Vĩnh Tường (C), Kim Khê (Nam Việt chí qua C); Mã Viện đuổi, thắng nhiều lần (HHT); 43 bị cô lập và thua (T NK 3/3b) | T, C, W | Vị trí không rõ, nói thẳng |
| 188012–188013 | Bị chém, gửi đầu (HHT qua W); T không mô tả; C: bị bắt; sông Hát không có trong T, C, đền Hát Môn (C) | T, C, W | Ba cách, nói rõ |
| 188014 | Kiernan 5.000–10.000 thủ lĩnh bị giết, vài trăm gia đình đưa về; nấu trống đồng đúc ngựa dâng mùa thu 44 | W (Kiernan 2019; Bielestein; Bronze drum) | Gắn tên Kiernan; chưa đọc HHT |
| 188015 | Bốn, năm phần mười quân Hán chết vì khí độc, dịch bệnh | W (HHT) | Gắn "theo Hậu Hán thư"; scope cả chiến dịch |
| 188016–188017 | Lê Văn Hưu; Ngô Sĩ Liên; làm vua ba năm | T NK 3/2a, 3/3a–4a | Đủ |

**Điểm lệch giữa nguồn:** (a) Lãng Bạc là Hồ Tây (T/C) hay Tiên Du (W); (b) Lãng Bạc năm 42, thua tháng giêng 43 (T) so với quân Hán tới đồng bằng đầu 43, dập tắt tháng tư 43 (W/HHT); lời đọc dùng "năm bốn mươi hai", "năm bốn mươi ba", không nói tháng; (c) số quân Hán một đến ba vạn; (d) số ra hàng hơn mười nghìn so với hơn hai vạn; (e) cách hai bà mất.
**Chi tiết đã bỏ:** phong tục hôn nhân và trường học (nguồn thứ cấp), cột đồng, Đoàn Chí và Lưu Long (không cần), câu "diều hâu rơi xuống nước" (không tìm được nguồn), lời thề Mê Linh (nguồn không rõ).

## 5. Kết quả bộ kiểm
- `kiem_kich_ban`: 0 ❌, 10 ⚠️; `kiem_mach_ke`: 0 ❌, 11 ⚠️; `kiem_mo_dau`: 0 ❌; `kiem_giong_van`: 0 ❌, 0 ⚠️; `kiem_khung`: không áp dụng.
- Biến cố chính: Mã Viện xuất hiện ở mốc khoảng 26%, trận Lãng Bạc khoảng 39%, trước 45%.

## 6. Tự rà (đọc thành tiếng, rà từng cặp đoạn kề nhau)
- Đại từ: "ông ta" (188002) chỉ Tô Định; "bà" là Trưng Trắc; "hai bà" là cả hai. Số: một đến ba vạn là quân Hán; mười nghìn là người ra hàng ở Lãng Bạc; không trộn.
- Thứ tự: khởi nghĩa, nhà Hán sai quân, Lãng Bạc, Cấm Khê, thua, cái chết, hậu quả, trả lời câu hỏi. Mỗi việc có kết quả trước khi sang việc sau.
- Chỗ tôi còn lo: (a) đoạn 188009, 188011 dày tên đất; (b) ba chỗ gắn tên Kiernan: một nguồn; (c) HHT chỉ qua nguồn thứ cấp; (d) 5,2 phút là dài hơn dự kiến một chút.

## 7. Cần chủ kênh duyệt
1. Mức phân tích (8 chỗ) và độ dài 5,2 phút đã đúng ý chưa? Nhiều hơn hay ít hơn?
2. Bỏ lời cảm ơn cuối (theo mục 10 mới, không bắt buộc): được không, hay giữ "Cảm ơn bạn đã lắng nghe câu chuyện này." như các video trước?
3. Có muốn tôi viết lại từ một bản văn xuôi riêng (như `giong-van.md` mục 1) thay vì ghép từ đoạn không?
