# Kịch bản Lý Công Uẩn: dời đô về Thăng Long (bản 2, hướng "Cánh cửa Quảng Phúc", để chủ kênh duyệt)

Mã `ly1`, 143 đoạn (18001–18143), 2,950 chữ, khoảng 16.4 phút ở 3 chữ/giây (đọc thực tế khoảng 3,3 chữ/giây nên khoảng 15–16 phút, vượt sàn 10 phút). Bộ kiểm `kiem_kich_ban.py ly1`: 0 lỗi, không đoạn nào dưới 14 chữ; đã thêm ngày tháng năm cho các mốc có ngày ghi trong sử (bản 3, 27/10/2026). File giọng: `ke-hoach/thu-giong-hai/ly1_full.json`. Chưa chạy giọng, chưa làm bản đồ, chưa dựng. Bản 1 (mở bằng câu hỏi cuối chiếu) đã bỏ vì dập khuôn Lê Hoàn.

**Nguồn đối chiếu:** toàn văn bản dịch Đại Việt sử ký toàn thư, lưu ở `ke-hoach/nguon/dai-viet-su-ky-toan-thu.txt` (kỷ nhà Lý, Thái Tổ Hoàng Đế, và đoạn năm 1028 ở cuối quyển II).

## Ý tưởng chính (phần sáng tạo, chủ kênh duyệt)

- **Mở đầu bằng cảnh năm 1028 ở cánh cửa Quảng Phúc:** ba vương nấp sau cánh cửa chờ thái tử. Đây là sự kiện có thật, được kể đầy đủ ở chương "Cánh cửa Quảng Phúc". Hook chỉ nêu mối nguy và câu hỏi vì sao vua cha bỏ kinh đô cũ để dựng cánh cửa ấy; không lộ kết cục.
- **Không dùng cầu nối "Muốn trả lời, ta phải bắt đầu từ..."** như video Lê Hoàn. Chuyển sang quá khứ bằng một câu tương phản: "Người dựng nó đã lớn lên bên một thiền sư chứ không phải trong cung điện."
- **Thân bài đúng thứ tự thời gian** (974, 1005, 1009, 1010, 1011–1015, 1028), mỗi chương gắn với một nơi chốn: Cổ Pháp, cửa cung nhà Lê, chính điện, Hoa Lư, Đại La, thuyền dưới chân thành, bốn cửa và các điện, điện Long An.
- **Một câu báo trước** ở chương dựng thành ("Hãy nhớ cánh cửa phía tây ấy, vì mười tám năm sau sẽ có hai vị vương nấp sau nó") và **kết quay lại đúng cánh cửa** mở đầu. Kết không bình luận, chỉ nối các sự việc: ông dựng cửa năm 1010, đến 1028 cửa ấy là nơi cuộc tranh ngôi kết thúc.
- **Đoạn viết liền mạch:** mỗi đoạn 2 vế, câu sau nêu lý do hoặc hệ quả của câu trước; không còn dòng cụt đứng riêng.
- **Toàn bộ tone `story`** (không trộn `tense`/`reflect`) để giọng Gemini không trôi cao độ giữa các lượt gọi (nguyên nhân xem ghi chú giọng ở cuối).
- **Không có câu đùa, không có "tập sau".**

## Chương và độ chắc (đã đối chiếu Toàn thư)

| Chương | Nội dung | Toàn thư |
|---|---|---|
| Cánh cửa phía tây | Mồng 1 tháng 3 nhật thực, ngày Mậu Tuất (mồng 3) vua băng; ba vương phục sẵn, Đông Chinh ở Long Thành, Dực Thánh và Vũ Đức ở cửa Quảng Phúc; cửa dựng năm 1010 | khớp (Q.II, năm Mậu Thìn 1028; Q.II, dựng bốn cửa); "hơn bốn mươi năm" tính từ Hoa Lư thời Đinh (968) |
| Đứa trẻ bên nhà thiền sư | Sinh 12/2 năm Giáp Tuất 974; ba tuổi nhà Lý Khánh Văn; Vạn Hạnh ở chùa Lục Tổ; không chăm sản nghiệp | khớp; truyện cha thần giao bỏ khỏi lời kể; lời khen của Vạn Hạnh nói là lời kể về sau |
| Người giữ cung nhà Lê | Trung Tông 3 ngày; ôm xác khóc; Tả thân vệ điện tiền chỉ huy sứ; hạt mận trong quả khế; Ngọa Triều; mất mùa đông 1009 | khớp |
| Lời nói khích và ngôi vua | Công Uẩn và Nguyễn Đê mỗi người 500 quân; Cam Mộc nói khích; giả vờ mắng; hôm sau; họp triều; Thuận Thiên; truy phong; gả con gái | khớp từng ý |
| Hoa Lư không còn đủ | "ẩm thấp chật hẹp, không đủ làm chỗ ở của đế vương"; nhà Đinh 2 vua, Tiền Lê 3 vua 29 năm | khớp; câu "núi đá che chở" là hiểu biết chung về địa thế |
| Đại La bên sông | Cao Biền đắp thành năm 866; "đô cũ của Cao Vương"; sông Hồng bên cạnh | khớp; các câu về thuyền bè và đất rộng suy từ chính bản chiếu |
| Lá chiếu dời đô | Mùa xuân 1010 về Cổ Pháp; sai sứ sang Tống; Bàn Canh 5 lần, nhà Chu 3 lần; phê Đinh, Lê; tả Đại La; câu hỏi cuối; bầy tôi đáp | khớp |
| Con thuyền dưới chân thành | Mùa thu tháng 7, thuyền đỗ dưới thành, rồng vàng, tên Thăng Long | khớp; nói rõ là điềm người xưa kể, không phải bằng chứng |
| Bốn cánh cửa và các điện | Điện Càn Nguyên, Tập Hiền, Giảng Võ, Long An, Long Thụy; bốn cửa Tường Phù (đông), Quảng Phúc (tây), Đại Hưng (nam), Diệu Đức (bắc); phủ Thiên Đức, phủ Trường Yên; cung Thúy Hoa; tha thuế 3 năm; Tống phong Giao Chỉ quận vương | khớp |
| Những năm trị vì | 10 đạo thành 24 lộ; Cử Long; Diễn Châu và lời khấn ở Biện Sơn; 6 loại thuế; Nam Chiếu, Dực Thánh Vương thắng ở Kim Hoa; 100 ngựa biếu Tống; chùa, chuông, Tam tạng; Cam Mộc mất 1015 | khớp |
| Điện Long An | Mười tám năm; mồng 1 tháng 3 nhật thực; băng ở điện Long An; thọ 55 (hơn 54 tuổi tròn); Thọ Lăng; lời đánh giá | khớp; cách nói hai cách tuổi đã chốt |
| Cánh cửa Quảng Phúc | Thái tử vào cửa Tường Phù đến điện Càn Nguyên; đóng cửa điện; Lý Nhân Nghĩa; thái tử im lặng; mở cửa đánh; Lê Phụng Hiểu bắt giết Vũ Đức Vương; hai vương thoát; báo tin trước linh cữu; Uất Trì Kính Đức | khớp từng ý |
| Kết | Các cửa và điện dựng 1010 là nơi diễn ra ngày 1028; nhà Lý hơn 200 năm; tên Thăng Long | nối các chương trên; nhà Lý 1009–1225 khoảng 216 năm (kỷ nhà Lý kết thúc ở Chiêu Hoàng) |

## Mốc ngày tháng (mới, theo yêu cầu "ghi rõ ngày tháng năm với từng mốc")

**Cách tính (cần chủ kênh biết):** Toàn thư ghi ngày bằng can chi và tháng âm lịch, gần như không ghi số ngày. Mình đổi sang dương lịch bằng cách tính chu kỳ 60 ngày can chi (liên tục, không bị lệch) kết hợp lịch trăng tính bằng thiên văn. **Kiểm chứng:** ngày mồng 1 tháng 3 năm 1028 là ngày Bính Thân (sử chép nhật thực), và tính ra đúng 29/3/1028 với ngày Mậu Tuất là 31/3/1028 (mồng 3), khớp với "hai ngày sau". Các ngày này do mình **tính lại, không phải Toàn thư ghi sẵn**, **Đã đối chiếu (27/10/2026)** với bảng đổi lịch Trung Hoa – Julian giai đoạn Tống 960–1279 của Y. T. Liu (ytliu0.github.io/ChineseCalendar, tải mã về chạy cục bộ): ngày đầu mỗi tháng khớp với tính toán của mình, trừ năm chỗ lệch 1 ngày ở đầu hoặc cuối tháng (1005 tháng 3, 1010 tháng 7, 1014 và 1015 tháng giêng) đã sửa theo bảng. Mọi ngày tính bằng can chi (19/11/1009, 21/11/1009, 29/3/1028, 31/3/1028) không đổi. Lưu ý bảng này cũng là lịch tính bằng thiên văn, không phải lịch Tống–Việt thời ấy, nên đầu tháng vẫn có thể lệch 1 ngày so với lịch dùng lúc đó; ngày can chi thì không bị ảnh hưởng.

**Lịch dương trong lời kể là lịch Julian**, lịch chính thức thời ấy và là cách phần lớn sách sử Việt ghi mốc trước năm 1582. Muốn đổi sang lịch Gregorian hiện nay thì cộng 6 ngày (31/3/1028 thành 6/4/1028). Lời kể chỉ nói "dương lịch" cho gọn; chủ kênh quyết định có đổi sang Gregorian hay thêm chữ "Julian" trên màn hình hay không.

| Mốc | Âm lịch (Toàn thư) | Dương lịch Julian (tính) | Độ chắc |
|---|---|---|---|
| Lý Công Uẩn sinh | 12 tháng 2 năm Giáp Tuất | 8/3/974 | ngày âm ghi trong sử; đổi dương lịch có thể lệch 1 ngày vì lịch thời Đinh |
| Lê Hoàn mất | tháng 3 năm Ất Tỵ (Ứng Thiên 12) | trong khoảng 12/4–10/5/1005 | sử chỉ ghi tháng |
| Lê Long Việt lên ngôi 3 ngày rồi bị giết | mùa đông năm Ất Tỵ | cuối năm 1005 | sử chỉ ghi mùa, sau 8 tháng giằng co |
| Lê Long Đĩnh mất | ngày Tân Hợi, tháng 10 năm Kỷ Dậu | 19/11/1009 | ngày can chi chắc; theo bảng đổi lịch đây là ngày 30, ngày cuối của tháng 10, khớp với chữ "tháng 10 ngày Tân Hợi" trong sử |
| Lý Công Uẩn lên ngôi | ngày Quý Sửu cùng tháng | 21/11/1009 | ngày can chi chắc (Wikipedia tiếng Anh cũng ghi 21/11 trong phần nội dung). Theo bảng đây là mồng 2 tháng 11, trong khi sử viết "tháng ấy"; vì vậy lời kể chỉ đọc ngày dương lịch, không đọc tháng âm lịch của ngày này |
| Về thăm Cổ Pháp, sai sứ sang Tống, viết chiếu | tháng 2 năm Canh Tuất | trong khoảng 17/2–18/3/1010 (năm này có tháng 2 nhuận) | sử chỉ ghi tháng; ngày viết chiếu không rõ |
| Rời Hoa Lư, thuyền đỗ dưới thành Đại La, đổi tên Thăng Long | tháng 7 năm Canh Tuất | trong khoảng 13/8–10/9/1010 | sử chỉ ghi tháng |
| Cung Thúy Hoa xong, tha thuế 3 năm | tháng 12 năm Canh Tuất | trong khoảng 7/1–5/2/1011 | sử chỉ ghi tháng |
| Đánh giặc Cử Long | tháng 2 năm Tân Hợi | trong khoảng 8/3–5/4/1011 | sử chỉ ghi tháng |
| Diễn Châu, lời khấn ở Biện Sơn | năm Nhâm Tý | năm 1012 | sử không ghi tháng |
| Định sáu loại thuế | năm Quý Sửu | năm 1013 | sử không ghi tháng |
| Nam Chiếu vào cướp, trận Kim Hoa | tháng giêng năm Giáp Dần | trong khoảng 3/2–3/3/1014 | sử chỉ ghi tháng |
| Đào Cam Mộc mất | tháng giêng năm Ất Mão | trong khoảng 23/1–21/2/1015 | sử chỉ ghi tháng |
| Nhà vua không khỏe | tháng 2 năm Mậu Thìn | trong khoảng 28/2–28/3/1028 | sử chỉ ghi tháng |
| Nhật thực | mồng 1 tháng 3 (Bính Thân) | 29/3/1028 | ngày chắc (sử ghi can chi, đã kiểm bằng tính lịch) |
| Vua mất, ba vương phục binh, Lê Phụng Hiểu bắt giết Vũ Đức Vương | ngày Mậu Tuất (mồng 3) tháng 3 | 31/3/1028 | ngày chắc |

Những mốc chỉ có tháng thì lời kể nói đúng "tháng X âm lịch", không bịa số ngày. Ngày dương lịch chỉ được đọc to ở bốn mốc có can chi hoặc ngày âm rõ (sinh, Long Đĩnh mất, lên ngôi, 1028); các mốc còn lại để thành ô ngày trên màn hình khi làm bản đồ.

## Điểm cần chủ kênh duyệt (phần sáng tạo, ghi độ chắc)

- **Quan hệ của ba vương với vua (đã kiểm Toàn thư, 27/10/2026):** chỉ Đông Chinh Vương chắc là con vua (Toàn thư 1018: "phong Hoàng tử Lực làm Đông Chinh Vương"). Dực Thánh Vương: Đại Việt sử lược ghi là em của Lý Công Uẩn, còn Cương mục dẫn Nam Thiên trung nghĩa lục nói là con thứ, người biên dịch Toàn thư nghiêng về sử lược, nên chưa rõ. Vũ Đức Vương: chú thích Toàn thư ghi "chưa rõ", trước năm 1028 không thấy nhắc. Vì vậy lời kể **không còn gọi họ là con hay em của vua**, chỉ gọi là "ba vị vương trong hoàng tộc"; lời thái tử nói "anh em", "tình cốt nhục" vẫn giữ vì là lời chính thái tử trong sử.
- **Câu mở đầu đã viết lại (27/10/2026):** "Vua vừa mất, ba vị vương mai phục sẵn để cướp ngôi của thái tử." (15 chữ, không ngày tháng, ai cũng hiểu: có vua chết, có người cướp ngôi). Câu sau cho biết đó là vua đầu tiên nhà Lý và ngày mất. Hình ảnh nhật thực chuyển về chương "Điện Long An" (nhật thực mồng 1 tháng 3 là có thật). Lý do: câu cũ "Hai ngày sau khi mặt trời tắt giữa ban ngày, nhà vua qua đời" không nói vua nào, chuyện gì, nên khó hiểu.
- **Hai câu của người kể ở phần kết:** "Không ai biết ông có nghĩ trước đến ngày ấy hay không" và "kinh đô ông dựng vẫn đứng vững, ngôi vua vẫn truyền được cho con". Đây là nối sự việc, không phải lời bình của sử gia; chủ kênh quyết định giữ hay bỏ.
- **Câu báo trước "Hãy nhớ cánh cửa phía tây ấy"** là kỹ thuật kể, không thêm sự kiện.
- **Ghi chú giọng:** đo cao độ Lê Hoàn cho thấy hai cụm đọc (đoạn 17041–17048 và 17089–17096) trôi trầm 9% và 16% so với phần còn lại; các cụm trộn tone bị chia thành 35 lượt gọi độc lập. Đinh Bộ Lĩnh (toàn `story`, đọc cụm 16) không bị. Vì vậy ly1 đọc toàn `story`, cụm 16, rồi chạy `phim_ban_do/kiem_cao_do.py`.

## Đã chốt theo ý chủ kênh (27/10/2026)

- **Tuổi thọ:** Toàn thư ghi "thọ 55 tuổi [974-1028]" (tính theo cách xưa, kể cả năm sinh). Tính tròn từ 12 tháng 2 năm 974 đến mồng 3 tháng 3 năm 1028 là hơn 54 tuổi. Lời kể ghi cả hai: "thọ năm mươi lăm tuổi theo cách tính của người xưa, tức là hơn năm mươi bốn tuổi tròn".
- **Năm Cao Biền đắp thành:** đã kiểm, Toàn thư chép dưới năm Bính Tuất 866; lời kể ghi "năm tám trăm sáu mươi sáu, hơn một trăm bốn mươi năm trước".
- **Độ dài:** giữ khoảng 17 phút.
- **Chuyện hạt mận trong quả khế:** vẫn để trong lời kể (chương "Người giữ cung nhà Lê", 4 đoạn), chủ kênh quyết định bỏ hay giữ. Ý "màu sấm điềm": Toàn thư chép Lê Long Đĩnh tin đó là lời sấm báo họ Lý sẽ lên, nên đó là chuyện điềm báo, không phải sự kiện chính; video chỉ kể như chuyện sử chép.
- Tên "Trường Yên" theo Toàn thư (cách gọi hiện đại là Tràng An).

## Chi tiết đã bỏ khỏi lời kể

**Bản 4 (27/10/2026, chủ kênh yêu cầu): bỏ hết lời bình của sử gia** (Lê Văn Hưu chê xây chùa trước khi dựng tông miếu, Ngô Sĩ Liên chê tôn hiệu năm mươi chữ, và đoạn đánh giá "khoan thứ nhân từ... ưa dị đoan" cuối truyện), cùng chuyện tôn hiệu năm mươi chữ. Lời kể chỉ còn sự việc, viết liền mạch theo nguyên nhân kết quả, không còn lối dịch sát từng câu sử.

Chuyện mẹ gặp người thần ở chùa Tiêu Sơn, chó con có chữ "thiên tử", cây gạo bị sét có sấm ký, lời Vạn Hạnh nói với Công Uẩn hơn 70 tuổi, các điềm lạ năm 1012 (vết chân thần), 1016, 1017, 1020, ngựa Bạch Long, tin đồn đầu độc, việc giết hai em của Lê Long Đĩnh (An Nam chí lược), các chi tiết bạo ngược nặng của Lê Long Đĩnh (róc mía trên đầu nhà sư, giết mèo cho các vương ăn...).

## Gợi ý tiêu đề

1. Vì sao Lý Công Uẩn bỏ Hoa Lư để ra Thăng Long?
2. Đứa trẻ nuôi trong nhà thiền sư và quyết định dời đô năm 1010
3. Một câu hỏi cuối lá chiếu đã đổi kinh đô nước Việt
4. Lê Phụng Hiểu và ngày ba vị vương phục binh trong cung vua
5. Cánh cửa Lý Công Uẩn dựng và ngày ba người con nấp sau nó


## Lời kể


> Bản 5 (27/10): bỏ đoạn hook mở đầu; vào thẳng cốt truyện từ lúc Lý Công Uẩn sinh, câu hỏi "vì sao dời đô" đặt ngay sau khi nhận làm con nuôi; cảnh ba vương phục sẵn kể đúng thứ tự thời gian ở cuối.

> Bản 6 (27/10): rà soát toàn bộ, tách câu thiếu chủ vị, bỏ chữ "cậu", "ta", "sử sách", "đó là lời bàn"; giải thích tên và từ cổ (Nguyễn Đê, Cao Vương, lộ, bệ hạ, trẫm, thiên thời); sửa các chữ "ông" mơ hồ.

> Bản 7 (27/10): mở đầu theo ý chủ kênh: bắt đầu từ ngày sinh, "có một cậu bé ra đời ở châu Cổ Pháp", thêm bối cảnh nhà Đinh, Hoa Lư, rồi mới nói em bé ấy là Lý Công Uẩn.

| n | chương | lời | mốc ngày (Julian, tính lại) |
|---|---|---|---|
| 18001 | Đứa trẻ bên nhà thiền sư | Ngày mười hai tháng hai âm lịch năm chín trăm bảy mươi bốn, tức khoảng ngày tám tháng ba, có một cậu bé ra đời. | 974: 12 tháng 2 âm ≈ 8/3/974 (Julian), khoảng |
| 18002 | Đứa trẻ bên nhà thiền sư | Nơi cậu bé chào đời là châu Cổ Pháp, một vùng đất nằm phía bắc sông Hồng. |  |
| 18003 | Đứa trẻ bên nhà thiền sư | Lúc ấy đất nước do vua Đinh Bộ Lĩnh trị vì, và kinh đô đặt ở Hoa Lư. |  |
| 18004 | Đứa trẻ bên nhà thiền sư | Hơn ba mươi năm sau, cậu bé ấy sẽ lên ngôi vua, mở đầu nhà Lý và dời kinh đô khỏi Hoa Lư. |  |
| 18005 | Đứa trẻ bên nhà thiền sư | Cậu bé ấy chính là Lý Công Uẩn. |  |
| 18006 | Đứa trẻ bên nhà thiền sư | Năm ba tuổi, Lý Công Uẩn được mẹ đưa đến nhà thiền sư Lý Khánh Văn, thiền sư nhận ông làm con nuôi và từ đó ông mang họ Lý. |  |
| 18007 | Đứa trẻ bên nhà thiền sư | Ông lớn lên rất thông minh, lại có dáng người tuấn tú khác thường. |  |
| 18008 | Đứa trẻ bên nhà thiền sư | Khi ông khoảng sáu tuổi, tướng Lê Hoàn lên thay nhà Đinh, mở ra triều Tiền Lê, và ông lớn lên dưới triều đại mới ấy. |  |
| 18009 | Đứa trẻ bên nhà thiền sư | Lúc đi học ở chùa Lục Tổ, ông gặp sư Vạn Hạnh, và người ta kể rằng vị sư đã nói ông sau này sẽ làm bậc minh chủ. |  |
| 18010 | Đứa trẻ bên nhà thiền sư | Lời ấy chỉ là chuyện kể về sau, còn điều thấy rõ hơn là tính cách của ông. |  |
| 18011 | Đứa trẻ bên nhà thiền sư | Ông không chuyên tâm chuyện học hành, nhưng sống khảng khái và có chí lớn. |  |
| 18012 | Đứa trẻ bên nhà thiền sư | Khi trưởng thành, ông vào làm quan võ trong triều đình nhà Tiền Lê, rồi dần lên chỉ huy quân bảo vệ cung vua. |  |
| 18013 | Đứa trẻ bên nhà thiền sư | Làm sao một viên tướng chỉ huy quân bảo vệ vua, đứng cạnh vị vua thích giết người, lại được tôn lên ngôi mà không có một trận đánh nào? |  |
| 18014 | Đứa trẻ bên nhà thiền sư | Câu trả lời nằm ở những năm cuối của triều Tiền Lê. |  |
| 18015 | Người giữ cung nhà Lê | Triều Tiền Lê khi ấy do vua Lê Hoàn dựng nên và trị vì hơn hai mươi năm. |  |
| 18016 | Người giữ cung nhà Lê | Tháng ba âm lịch năm một nghìn không trăm linh năm, Lê Hoàn mất, và các con của ông liền tranh ngôi. |  |
| 18017 | Người giữ cung nhà Lê | Cuộc giành giật kéo dài tám tháng, trong nước không có vua. | 1005: mùa đông (tháng 10 âm = 5/11–3/12/1005) |
| 18018 | Người giữ cung nhà Lê | Mùa đông năm ấy Lê Long Việt lên ngôi, và ba ngày sau bị em là Lê Long Đĩnh giết rồi lên thay. |  |
| 18019 | Người giữ cung nhà Lê | Các quan sợ hãi bỏ chạy hết, chỉ riêng Lý Công Uẩn ở lại ôm xác nhà vua mà khóc. |  |
| 18020 | Người giữ cung nhà Lê | Thấy vậy, Lê Long Đĩnh khen ông là người trung thành. |  |
| 18021 | Người giữ cung nhà Lê | Vua cho ông giữ quân canh kinh thành, rồi thăng dần đến chức đứng đầu đội quân canh giữ cung vua. |  |
| 18022 | Người giữ cung nhà Lê | Nhưng phục vụ vị vua mới không hề dễ, vì Lê Long Đĩnh thích giết người và nổi tiếng là một ông vua bạo ngược. |  |
| 18023 | Người giữ cung nhà Lê | Có lần vua ăn quả khế thấy hạt mận, mà chữ Lý cũng có nghĩa là cây mận, nên vua tin đó là điềm báo người họ Lý sẽ làm vua. |  |
| 18024 | Người giữ cung nhà Lê | Từ đó vua ngầm cho người tìm giết những người họ Lý. |  |
| 18025 | Người giữ cung nhà Lê | Vậy mà Lý Công Uẩn ngày ngày đứng cạnh vua, mà vua không hề biết. |  |
| 18026 | Người giữ cung nhà Lê | Về sau Lê Long Đĩnh mắc bệnh trĩ nặng, phải nằm nghe việc triều đình, nên người đời gọi ông là Lê Ngọa Triều, nghĩa là vua nằm nghe việc nước. |  |
| 18027 | Người giữ cung nhà Lê | Ngày mười chín tháng mười một năm một nghìn không trăm linh chín, Lê Long Đĩnh qua đời. | 1009: ngày Tân Hợi = 19/11/1009 |
| 18028 | Người giữ cung nhà Lê | Người con của ông còn quá nhỏ, chưa thể tự lo việc nước. |  |
| 18029 | Lời nói khích và ngôi vua | Khi ấy Lý Công Uẩn và một viên tướng tên Nguyễn Đê mỗi người dẫn năm trăm quân canh giữ trong cung. |  |
| 18030 | Lời nói khích và ngôi vua | Hai đạo quân ấy mạnh nhất hoàng cung, nên ngai vàng như nằm trong tay hai người. |  |
| 18031 | Lời nói khích và ngôi vua | Một viên quan hầu cận tên Đào Cam Mộc nhìn ra cơ hội ấy. |  |
| 18032 | Lời nói khích và ngôi vua | Một hôm vắng người, ông ta tìm đến Lý Công Uẩn nói khích. |  |
| 18033 | Lời nói khích và ngôi vua | Ông ta nói rằng vua cũ tàn bạo, vua mới còn nhỏ, sao ông không thuận theo ý trời và lòng dân mà làm vua? |  |
| 18034 | Lời nói khích và ngôi vua | Lý Công Uẩn thích lời ấy nhưng còn ngờ Đào Cam Mộc có mưu khác, nên giả vờ mắng và dọa sẽ bắt ông ta. |  |
| 18035 | Lời nói khích và ngôi vua | Đào Cam Mộc đáp rằng ông ta không sợ chết, vì chính lòng người đã khiến ông ta dám nói. |  |
| 18036 | Lời nói khích và ngôi vua | Thấy ông ta thật lòng, Lý Công Uẩn mới nói thật, rằng ông chỉ sợ chuyện lộ ra thì cả hai cùng bị giết. |  |
| 18037 | Lời nói khích và ngôi vua | Hôm sau Đào Cam Mộc lại đến, nói rằng ai cũng bảo họ Lý sắp dựng nghiệp lớn. |  |
| 18038 | Lời nói khích và ngôi vua | Lý Công Uẩn đáp rằng mình đã hiểu ý ấy, và ý ấy giống hệt ý sư Vạn Hạnh. |  |
| 18039 | Lời nói khích và ngôi vua | Đào Cam Mộc liền đem chuyện nói với các quan, và ngay hôm ấy họ họp bàn. |  |
| 18040 | Lời nói khích và ngôi vua | Họ cho rằng dân đã chán vua cũ, còn vua nối thì quá bé nên không ai muốn theo. |  |
| 18041 | Lời nói khích và ngôi vua | Họ nói nếu không nhân lúc này tôn Lý Công Uẩn lên, lỡ có biến thì chưa chắc còn giữ được cái đầu. |  |
| 18042 | Lời nói khích và ngôi vua | Vậy là ngày hai mươi mốt tháng mười một năm một nghìn không trăm linh chín, cả triều dìu ông lên chính điện. | 1009: ngày Quý Sửu = 21/11/1009 |
| 18043 | Lời nói khích và ngôi vua | Trăm quan lạy rạp dưới sân và hô chúc nhà vua sống muôn năm. |  |
| 18044 | Lời nói khích và ngôi vua | Cuộc đổi ngôi ấy diễn ra êm thấm, không có một trận giao tranh nào. |  |
| 18045 | Lời nói khích và ngôi vua | Tân hoàng đế tha tội cho nhiều người trong cả nước, rồi lấy năm sau làm năm đầu niên hiệu Thuận Thiên, nghĩa là thuận theo ý trời. |  |
| 18046 | Lời nói khích và ngôi vua | Ông ban danh hiệu cho cha mẹ đã mất và lập con trai trưởng là Lý Phật Mã làm thái tử. |  |
| 18047 | Lời nói khích và ngôi vua | Rồi ông gả con gái lớn cho Đào Cam Mộc. |  |
| 18048 | Lời nói khích và ngôi vua | Người đã ngỏ lời đầu tiên ấy được phong làm Nghĩa Tín Hầu. |  |
| 18049 | Lời nói khích và ngôi vua | Từ một viên quan hầu cận, ông ta trở thành người có công lớn của triều mới. |  |
| 18050 | Lời nói khích và ngôi vua | Có ngôi vua rồi, ông còn một câu hỏi lớn phải trả lời, đó là triều đình mới nên đặt ở đâu. |  |
| 18051 | Hoa Lư không còn đủ | Kinh đô lúc ấy là Hoa Lư, nơi vua Đinh Bộ Lĩnh dựng cung điện hơn bốn mươi năm trước, giữa những dãy núi đá dựng đứng. |  |
| 18052 | Hoa Lư không còn đủ | Trong thời loạn, núi đá như bức tường che chở khiến nơi này rất dễ giữ. |  |
| 18053 | Hoa Lư không còn đủ | Nhưng nhà vua cho rằng thời bình cần một kinh đô có những cánh cửa mở ra bốn phương. |  |
| 18054 | Hoa Lư không còn đủ | Kinh đô ấy cần dân cư đông đúc, đường đi thuận tiện và đất rộng để mở mang dần. |  |
| 18055 | Hoa Lư không còn đủ | Trong khi đó, theo ông, Hoa Lư lại ẩm thấp và chật hẹp. |  |
| 18056 | Hoa Lư không còn đủ | Nhà vua cũng nhìn lại hai triều trước. |  |
| 18057 | Hoa Lư không còn đủ | Cả hai đều đóng đô ở Hoa Lư và đều ngắn ngủi. |  |
| 18058 | Hoa Lư không còn đủ | Nhà Đinh chỉ có hai vua, còn nhà Tiền Lê có ba vua và tồn tại hai mươi chín năm. |  |
| 18059 | Đại La bên sông | Lý Công Uẩn không muốn đi vào vận ngắn ngủi ấy, nên ông nhìn về thành Đại La bên sông Hồng. |  |
| 18060 | Đại La bên sông | Đó là tòa thành cũ do tướng Cao Biền của nhà Đường đắp từ năm tám trăm sáu mươi sáu, hơn một trăm bốn mươi năm trước. |  |
| 18061 | Đại La bên sông | Các quan nhà Đường từng ngồi đó cai trị vùng đất Giao Châu lúc bấy giờ. |  |
| 18062 | Đại La bên sông | Chính bản chiếu của vua cũng gọi nơi này là đô cũ của Cao Vương, tức Cao Biền. |  |
| 18063 | Đại La bên sông | Thành có sông Hồng chảy ngay bên cạnh nên thuyền bè nhiều nơi có thể cập bến, còn đất quanh đó thì rộng và bằng phẳng. |  |
| 18064 | Đại La bên sông | Ở đó kinh đô có thể mở rộng mãi, chứ không bị núi đá bó chặt như Hoa Lư. |  |
| 18065 | Đại La bên sông | Dời đô là việc rất lớn, vì phải bỏ cung điện cũ và dựng lại từ đầu ở một nơi xa. |  |
| 18066 | Đại La bên sông | Vì thế nhà vua viết một bản chiếu để thuyết phục cả triều đình. |  |
| 18067 | Lá chiếu dời đô | Tháng hai âm lịch năm một nghìn không trăm mười, nhà vua về thăm châu Cổ Pháp quê mình và ban tiền lụa cho các cụ già trong làng. | 1010: tháng 2 âm = 17/2–18/3/1010 |
| 18068 | Lá chiếu dời đô | Cũng trong năm ấy ông sai sứ sang nhà Tống để giữ tình hòa hảo. |  |
| 18069 | Lá chiếu dời đô | Chiếu mở đầu bằng chuyện xưa của Trung Hoa, rằng nhà Thương năm lần dời đô và nhà Chu ba lần, để mưu nghiệp lớn cho con cháu muôn đời. |  |
| 18070 | Lá chiếu dời đô | Còn nhà Đinh và nhà Tiền Lê thì cứ yên đóng đô một chỗ, nên vận nước ngắn ngủi và trăm họ hao tổn. |  |
| 18071 | Lá chiếu dời đô | Chiếu tả Đại La có thế đất như rồng cuộn hổ ngồi, rộng mà bằng phẳng, cao mà sáng sủa, muôn vật đều tươi tốt. |  |
| 18072 | Lá chiếu dời đô | Cuối chiếu, ông không ra lệnh mà hỏi bầy tôi rằng nhân thế đất tốt ấy mà định nơi ở, các quan nghĩ thế nào? |  |
| 18073 | Lá chiếu dời đô | Bầy tôi đáp rằng nhà vua lập kế lâu dài cho thiên hạ, điều lợi như thế thì ai dám không theo. |  |
| 18074 | Lá chiếu dời đô | Nhà vua rất mừng. |  |
| 18075 | Con thuyền dưới chân thành | Tháng bảy âm lịch năm một nghìn không trăm mười, vào khoảng tháng tám dương lịch, nhà vua rời Hoa Lư, đi thuyền ra Đại La. | 1010: tháng 7 âm = 13/8–10/9/1010 |
| 18076 | Con thuyền dưới chân thành | Thuyền vừa dừng dưới chân thành thì có người kể rằng một con rồng vàng hiện lên. |  |
| 18077 | Con thuyền dưới chân thành | Không ai chứng minh được điều đó, nhưng người xưa tin rằng đây là dấu hiệu trời chọn nơi này và chọn vị vua ấy. |  |
| 18078 | Con thuyền dưới chân thành | Nhà vua liền đổi tên Đại La thành Thăng Long, nghĩa là rồng bay lên. |  |
| 18079 | Con thuyền dưới chân thành | Cái tên do chính ông đặt ấy sống lâu hơn cả triều đại nhà Lý. |  |
| 18080 | Bốn cánh cửa và các điện | Cũng trong năm ấy nhà vua dựng điện Càn Nguyên ở phía trước làm nơi họp triều, hai bên là điện Tập Hiền và điện Giảng Võ. |  |
| 18081 | Bốn cánh cửa và các điện | Sau điện Càn Nguyên là hai điện Long An và Long Thụy, nơi nhà vua nghỉ ngơi. |  |
| 18082 | Bốn cánh cửa và các điện | Rồi ông cho dựng kho tàng, đắp thành và đào hào. |  |
| 18083 | Bốn cánh cửa và các điện | Bốn mặt thành mở bốn cửa, cửa phía đông tên Tường Phù, cửa phía tây tên Quảng Phúc, cửa phía nam tên Đại Hưng và cửa phía bắc tên Diệu Đức. |  |
| 18084 | Bốn cánh cửa và các điện | Không ai ngờ cánh cửa phía tây ấy sẽ còn chứng kiến một biến cố lớn. |  |
| 18085 | Bốn cánh cửa và các điện | Các nơi cũ cũng được đổi tên để ghi nhớ nguồn gốc. |  |
| 18086 | Bốn cánh cửa và các điện | Châu Cổ Pháp quê ông thành phủ Thiên Đức, còn Hoa Lư thành phủ Trường Yên. |  |
| 18087 | Bốn cánh cửa và các điện | Tháng mười hai âm lịch, tức đầu năm một nghìn không trăm mười một, cung Thúy Hoa xây xong, và nhân dịp ấy ông tha thuế cho cả nước ba năm. | 1010: tháng 12 âm = 7/1–5/2/1011 |
| 18088 | Bốn cánh cửa và các điện | Những người mồ côi, góa chồng, già yếu mà còn thiếu thuế từ lâu cũng được tha hết. |  |
| 18089 | Bốn cánh cửa và các điện | Cũng năm ấy nhà Tống phong ông làm Giao Chỉ quận vương. |  |
| 18090 | Bốn cánh cửa và các điện | Vậy là kinh đô mới vừa dựng đã được nước láng giềng phương bắc công nhận. |  |
| 18091 | Những năm trị vì | Dời đô chỉ là bước đầu, vì kinh đô chỉ vững khi cả đất nước cũng vững. |  |
| 18092 | Những năm trị vì | Vì thế ngay năm ấy ông đổi mười đạo thành hai mươi bốn lộ, tức chia đất nước thành các vùng nhỏ hơn cho dễ cai quản. |  |
| 18093 | Những năm trị vì | Tháng hai âm lịch năm một nghìn không trăm mười một, ông đem quân đi đánh giặc Cử Long ở Ái Châu. | 1010: tháng 2 âm = 17/2–18/3/1010 |
| 18094 | Những năm trị vì | Hai triều Đinh và Tiền Lê đều không đánh nổi bọn giặc này. |  |
| 18095 | Những năm trị vì | Nhưng lần ấy nhà vua đốt các bộ lạc của chúng và bắt kẻ đầu sỏ, nên giặc tan. |  |
| 18096 | Những năm trị vì | Năm một nghìn không trăm mười hai ông thân chinh đi đánh Diễn Châu. |  |
| 18097 | Những năm trị vì | Trên đường về, đến vùng biển Biện Sơn, trời đất bỗng tối sầm, gió sấm dữ dội. |  |
| 18098 | Những năm trị vì | Nhà vua đốt hương khấn rằng mình là người ít đức, không dám cậy binh uy mà đánh bừa, chỉ vì Diễn Châu làm điều tàn ngược nên buộc phải đánh. |  |
| 18099 | Những năm trị vì | Ông xin rằng nếu lỡ giết oan người hiền thì trời cứ trách riêng mình. |  |
| 18100 | Những năm trị vì | Người ta kể rằng khấn xong gió sấm đều yên lặng. |  |
| 18101 | Những năm trị vì | Sau chiến trận ông lo việc trong nước, và năm một nghìn không trăm mười ba ông định ra các thứ thuế, chia làm sáu loại. |  |
| 18102 | Những năm trị vì | Đến tháng giêng âm lịch năm một nghìn không trăm mười bốn, quân của nước Nam Chiếu ở phía tây bắc kéo rất đông vào cướp. | 1014: tháng giêng âm = 3/2–3/3/1014 |
| 18103 | Những năm trị vì | Họ đóng trại ở bến Kim Hoa. |  |
| 18104 | Những năm trị vì | Nhà vua sai Dực Thánh Vương, một vị vương trong hoàng tộc, đem quân đánh thắng lớn. |  |
| 18105 | Những năm trị vì | Quân của nhà vua bắt được rất nhiều quân và ngựa của đối phương. |  |
| 18106 | Những năm trị vì | Ông cho đem một trăm con ngựa bắt được sang biếu nhà Tống, và vua Tống ban thưởng mũ, đai, tiền bạc cho sứ giả. |  |
| 18107 | Những năm trị vì | Bên cạnh việc quân, nhà vua dốc sức cho Phật giáo. |  |
| 18108 | Những năm trị vì | Ông cho xây nhiều chùa, đúc chuông, chép kinh Tam tạng, và cho hơn một nghìn người ở kinh đô đi tu. |  |
| 18109 | Những năm trị vì | Điều ấy không lạ, vì ông từng lớn lên bên nhà thiền sư và suốt thời trị vì vẫn coi trọng đạo Phật. |  |
| 18110 | Những năm trị vì | Tháng giêng âm lịch năm một nghìn không trăm mười lăm, Đào Cam Mộc, người từng khuyên ông lên ngôi, qua đời và được tặng chức Thái sư á vương. | 1015: tháng giêng âm = 23/1–21/2/1015 |
| 18111 | Điện Long An | Mười tám năm đã trôi qua từ ngày dời đô, và kinh thành Thăng Long đã có cung điện, có thành, có bốn cửa mở ra bốn phương. |  |
| 18112 | Điện Long An | Thái tử Lý Phật Mã đã trưởng thành và từng thay cha cầm quân đi đánh các nơi, còn nhà vua bước vào năm cuối đời. |  |
| 18113 | Điện Long An | Tháng hai âm lịch năm một nghìn không trăm hai mươi tám, nhà vua không khỏe. | 1010: tháng 2 âm = 17/2–18/3/1010 |
| 18114 | Điện Long An | Đến mồng một tháng ba, tức hai mươi chín tháng ba, mặt trời bị nhật thực che khuất giữa ban ngày. | 1028: mồng 1 tháng 3 (Bính Thân) = 29/3/1028 |
| 18115 | Điện Long An | Hai ngày sau, ngày ba mươi mốt tháng ba, nhà vua mất ngay tại điện Long An do chính ông dựng, thọ năm mươi lăm tuổi theo cách tính của người xưa. | 1028: ngày Mậu Tuất = 31/3/1028 |
| 18116 | Điện Long An | Tính theo ngày sinh thì ông mới hơn năm mươi bốn tuổi, ở ngôi mười tám năm và được an táng ở Thọ Lăng. |  |
| 18117 | Cánh cửa Quảng Phúc | Nhà Lý chưa kịp lo xong tang lễ thì mối nguy đã nổ ra ngay trong hoàng tộc. |  |
| 18118 | Cánh cửa Quảng Phúc | Nó nổ ra đúng tại cánh cửa Quảng Phúc, cửa phía tây do chính nhà vua vừa mất đã dựng. |  |
| 18119 | Cánh cửa Quảng Phúc | Ba vị vương là Đông Chinh Vương, Dực Thánh Vương và Vũ Đức Vương đã đem quân phủ mình vào ẩn sẵn trong thành, chờ thái tử Lý Phật Mã. |  |
| 18120 | Cánh cửa Quảng Phúc | Đông Chinh Vương nấp ở Long Thành, còn Dực Thánh Vương và Vũ Đức Vương nấp ở cửa Quảng Phúc, chờ thái tử đi qua để đánh úp. |  |
| 18121 | Cánh cửa Quảng Phúc | Một lát sau thái tử đi vào từ cửa Tường Phù, và khi đến điện Càn Nguyên thì ông nhận ra có biến. |  |
| 18122 | Cánh cửa Quảng Phúc | Ông cho đóng hết các cửa điện và sai lính canh trong cung phòng giữ, rồi nói rằng mình không hề phụ bạc anh em. |  |
| 18123 | Cánh cửa Quảng Phúc | Ông nói ba vương đã quên lời cha dặn mà định chiếm ngôi báu, và hỏi các quan xung quanh nên làm thế nào. |  |
| 18124 | Cánh cửa Quảng Phúc | Viên nội thị Lý Nhân Nghĩa xin cho đánh một trận để quyết thắng thua, nhưng thái tử chưa chịu. |  |
| 18125 | Cánh cửa Quảng Phúc | Thái tử im lặng hồi lâu rồi nói rằng vua cha vừa mất chưa kịp quàn mà anh em đã giết nhau thì muôn đời sẽ chê cười. |  |
| 18126 | Cánh cửa Quảng Phúc | Ông muốn che giấu tội của ba vương để họ tự rút quân, giữ trọn tình ruột thịt, nhưng quân của ba vương lại bao vây càng gấp. |  |
| 18127 | Cánh cửa Quảng Phúc | Lúc ấy thái tử nói rằng nếu thế thì ông chỉ còn biết mặc áo tang đứng hầu vua cha, còn mọi việc xin giao cho các quan. |  |
| 18128 | Cánh cửa Quảng Phúc | Lý Nhân Nghĩa cùng các quan lạy hai lạy, nói rằng chết vì vua gặp nạn là bổn phận của họ, rồi ra lệnh mở cửa cho vệ sĩ xông ra đánh. |  |
| 18129 | Cánh cửa Quảng Phúc | Vệ sĩ trong cung ai cũng vui lòng xông pha, mỗi người địch với trăm người, nhưng hai bên giao chiến mãi chưa phân thắng bại. |  |
| 18130 | Cánh cửa Quảng Phúc | Bỗng tướng Lê Phụng Hiểu tức giận rút gươm, chạy thẳng tới cửa Quảng Phúc. |  |
| 18131 | Cánh cửa Quảng Phúc | Ông hô lớn rằng Vũ Đức Vương nhòm ngó ngôi báu, trên quên ơn vua cha, dưới trái nghĩa tôi con. |  |
| 18132 | Cánh cửa Quảng Phúc | Rồi ông xông thẳng tới chỗ ngựa của Vũ Đức Vương, vương quay ngựa tránh nhưng ngựa quỵ xuống, và Vũ Đức Vương bị Lê Phụng Hiểu bắt giết. |  |
| 18133 | Cánh cửa Quảng Phúc | Quân của ba vương thua chạy, và chỉ có hai vương Đông Chinh cùng Dực Thánh thoát được. |  |
| 18134 | Cánh cửa Quảng Phúc | Lê Phụng Hiểu trở về, mặc nguyên áo trận vào báo tin thắng ngay trước linh cữu của vua cha, rồi sang điện Càn Nguyên báo cho thái tử. |  |
| 18135 | Cánh cửa Quảng Phúc | Thái tử khen rằng ông còn trung dũng hơn Uất Trì Kính Đức, vị công thần nổi tiếng của nhà Đường. |  |
| 18136 | Cánh cửa Quảng Phúc | Sau đó thái tử lên ngôi, và đó là vua Lý Thái Tông. |  |
| 18137 | Kết | Cửa Tường Phù, cửa Quảng Phúc, điện Càn Nguyên và điện Long An, những nơi diễn ra ngày hôm ấy, đều do Lý Công Uẩn dựng năm một nghìn không trăm mười. |  |
| 18138 | Kết | Khi dựng chúng, ông đã viết trong bản chiếu rằng nhà Đinh và nhà Tiền Lê vận nước ngắn ngủi vì cứ yên đóng đô một chỗ. |  |
| 18139 | Kết | Không ai biết ông có nghĩ trước đến ngày ba mươi mốt tháng ba năm một nghìn không trăm hai mươi tám ấy hay không. | 1028: 31/3/1028 |
| 18140 | Kết | Nhưng đến ngày ấy kinh đô ông dựng vẫn đứng vững, và ngôi vua vẫn truyền được cho con. |  |
| 18141 | Kết | Nhà Lý giữ ngôi hơn hai trăm năm, còn cái tên Thăng Long mà ông đặt cho nơi con thuyền dừng lại cũng sống lâu hơn cả triều đại của ông. |  |
| 18142 | Kết | Mười tám năm trước ông chỉ hỏi bầy tôi một câu, rằng nhân đất tốt ấy mà định nơi ở thì các quan nghĩ thế nào. |  |
| 18143 | Kết | Và ở cánh cửa Quảng Phúc, cánh cửa phía tây ông dựng, một cuộc tranh ngôi ngay trong hoàng tộc của ông đã kết thúc. |  |
