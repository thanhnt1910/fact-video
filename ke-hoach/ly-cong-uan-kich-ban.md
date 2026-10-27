# Kịch bản Lý Công Uẩn: dời đô về Thăng Long (bản 2, hướng "Cánh cửa Quảng Phúc", để chủ kênh duyệt)

Mã `ly1`, 116 đoạn (18001–18116), 3,105 chữ, khoảng 17.2 phút ở 3 chữ/giây (đọc thực tế khoảng 3,3 chữ/giây nên khoảng 15–16 phút, vượt sàn 10 phút). Bộ kiểm `kiem_kich_ban.py ly1`: 0 lỗi, không đoạn nào dưới 14 chữ; đã thêm ngày tháng năm cho các mốc có ngày ghi trong sử (bản 3, 27/10/2026). File giọng: `ke-hoach/thu-giong-hai/ly1_full.json`. Chưa chạy giọng, chưa làm bản đồ, chưa dựng. Bản 1 (mở bằng câu hỏi cuối chiếu) đã bỏ vì dập khuôn Lê Hoàn.

**Nguồn đối chiếu:** toàn văn bản dịch Đại Việt sử ký toàn thư, lưu ở `ke-hoach/nguon/dai-viet-su-ky-toan-thu.txt` (kỷ nhà Lý, Thái Tổ Hoàng Đế, và đoạn năm 1028 ở cuối quyển II).

## Ý tưởng chính (phần sáng tạo, chủ kênh duyệt)

- **Mở đầu bằng cảnh năm 1028 ở cánh cửa Quảng Phúc:** ba vương nấp sau cánh cửa chờ thái tử. Đây là sự kiện có thật, được kể đầy đủ ở chương "Cánh cửa Quảng Phúc". Hook chỉ nêu mối nguy và câu hỏi vì sao vua cha bỏ kinh đô cũ để dựng cánh cửa ấy; không lộ kết cục.
- **Không dùng cầu nối "Muốn trả lời, ta phải bắt đầu từ..."** như video Lê Hoàn. Chuyển sang quá khứ bằng một câu tương phản: "Người dựng nó đã lớn lên bên một thiền sư chứ không phải trong cung điện."
- **Thân bài đúng thứ tự thời gian** (974, 1005, 1009, 1010, 1011–1015, 1028), mỗi chương gắn với một nơi chốn: Cổ Pháp, cửa cung nhà Lê, chính điện, Hoa Lư, Đại La, thuyền dưới chân thành, bốn cửa và các điện, điện Long An.
- **Một câu báo trước** ở chương dựng thành ("Hãy nhớ cánh cửa phía tây ấy, vì mười tám năm sau hai người con của ông sẽ nấp sau nó") và **kết quay lại đúng cánh cửa** mở đầu. Kết không bình luận, chỉ nối các sự việc: ông dựng cửa năm 1010, đến 1028 cửa ấy là nơi cuộc tranh ngôi kết thúc.
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

**Cách tính (cần chủ kênh biết):** Toàn thư ghi ngày bằng can chi và tháng âm lịch, gần như không ghi số ngày. Mình đổi sang dương lịch bằng cách tính chu kỳ 60 ngày can chi (liên tục, không bị lệch) kết hợp lịch trăng tính bằng thiên văn. **Kiểm chứng:** ngày mồng 1 tháng 3 năm 1028 là ngày Bính Thân (sử chép nhật thực), và tính ra đúng 29/3/1028 với ngày Mậu Tuất là 31/3/1028 (mồng 3), khớp với "hai ngày sau". Các ngày này do mình **tính lại, không phải Toàn thư ghi sẵn**, nên cần đối chiếu thêm với một bảng đổi lịch đã công bố trước khi đăng.

**Lịch dương trong lời kể là lịch Julian**, lịch chính thức thời ấy và là cách phần lớn sách sử Việt ghi mốc trước năm 1582. Muốn đổi sang lịch Gregorian hiện nay thì cộng 6 ngày (31/3/1028 thành 6/4/1028). Lời kể chỉ nói "dương lịch" cho gọn; chủ kênh quyết định có đổi sang Gregorian hay thêm chữ "Julian" trên màn hình hay không.

| Mốc | Âm lịch (Toàn thư) | Dương lịch Julian (tính) | Độ chắc |
|---|---|---|---|
| Lý Công Uẩn sinh | 12 tháng 2 năm Giáp Tuất | 8/3/974 | ngày âm ghi trong sử; đổi dương lịch có thể lệch 1 ngày vì lịch thời Đinh |
| Lê Hoàn mất | tháng 3 năm Ất Tỵ (Ứng Thiên 12) | trong khoảng 11/4–10/5/1005 | sử chỉ ghi tháng |
| Lê Long Việt lên ngôi 3 ngày rồi bị giết | mùa đông năm Ất Tỵ | cuối năm 1005 | sử chỉ ghi mùa, sau 8 tháng giằng co |
| Lê Long Đĩnh mất | ngày Tân Hợi, tháng 10 năm Kỷ Dậu | 19/11/1009 | ngày can chi chắc; lịch tính hiện đại xếp ngày này vào mồng 1 tháng 11, lệch một ngày so với chữ "tháng 10" trong sử, có thể do lịch thời ấy tính đầu tháng khác cách tính thiên văn |
| Lý Công Uẩn lên ngôi | ngày Quý Sửu cùng tháng | 21/11/1009 | như trên |
| Về thăm Cổ Pháp, sai sứ sang Tống, viết chiếu | tháng 2 năm Canh Tuất | trong khoảng 17/2–17/3/1010 | sử chỉ ghi tháng; ngày viết chiếu không rõ |
| Rời Hoa Lư, thuyền đỗ dưới thành Đại La, đổi tên Thăng Long | tháng 7 năm Canh Tuất | trong khoảng 12/8–10/9/1010 | sử chỉ ghi tháng |
| Cung Thúy Hoa xong, tha thuế 3 năm | tháng 12 năm Canh Tuất | trong khoảng 7/1–5/2/1011 | sử chỉ ghi tháng |
| Đánh giặc Cử Long | tháng 2 năm Tân Hợi | trong khoảng 8/3–5/4/1011 | sử chỉ ghi tháng |
| Diễn Châu, lời khấn ở Biện Sơn | năm Nhâm Tý | năm 1012 | sử không ghi tháng |
| Định sáu loại thuế | năm Quý Sửu | năm 1013 | sử không ghi tháng |
| Nam Chiếu vào cướp, trận Kim Hoa | tháng giêng năm Giáp Dần | trong khoảng 2/2–3/3/1014 | sử chỉ ghi tháng |
| Đào Cam Mộc mất | tháng giêng năm Ất Mão | trong khoảng 23/1–20/2/1015 | sử chỉ ghi tháng |
| Nhà vua không khỏe | tháng 2 năm Mậu Thìn | trong khoảng 28/2–28/3/1028 | sử chỉ ghi tháng |
| Nhật thực | mồng 1 tháng 3 (Bính Thân) | 29/3/1028 | ngày chắc (sử ghi can chi, đã kiểm bằng tính lịch) |
| Vua mất, ba vương phục binh, Lê Phụng Hiểu bắt giết Vũ Đức Vương | ngày Mậu Tuất (mồng 3) tháng 3 | 31/3/1028 | ngày chắc |

Những mốc chỉ có tháng thì lời kể nói đúng "tháng X âm lịch", không bịa số ngày. Ngày dương lịch chỉ được đọc to ở bốn mốc có can chi hoặc ngày âm rõ (sinh, Long Đĩnh mất, lên ngôi, 1028); các mốc còn lại để thành ô ngày trên màn hình khi làm bản đồ.

## Điểm cần chủ kênh duyệt (phần sáng tạo, ghi độ chắc)

- **"Ba người em của thái tử", "hai người con của ông":** thái tử gọi ba vương là "anh em"; Dực Thánh Vương là con thứ theo chú thích; Vũ Đức Vương Toàn thư chú là "chưa rõ" thân thế. **Cần kiểm thêm** nếu muốn nói chắc "con của vua".
- **Câu mở đầu đã viết lại (27/10/2026):** "Vua vừa mất, ba hoàng tử đem quân phục sẵn trong cung để cướp ngôi." (15 chữ, không ngày tháng, ai cũng hiểu: có vua chết, có người cướp ngôi). Câu sau cho biết đó là vua đầu tiên nhà Lý và ngày mất. Hình ảnh nhật thực chuyển về chương "Điện Long An" (nhật thực mồng 1 tháng 3 là có thật). Lý do: câu cũ "Hai ngày sau khi mặt trời tắt giữa ban ngày, nhà vua qua đời" không nói vua nào, chuyện gì, nên khó hiểu.
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

| n | chương | lời | mốc ngày (Julian, tính lại) |
|---|---|---|---|
| 18001 | Cánh cửa phía tây | Vua vừa mất, ba hoàng tử đem quân phục sẵn trong cung để cướp ngôi. |  |
| 18002 | Cánh cửa phía tây | Đó là vị vua đầu tiên của nhà Lý, mất ngày mồng ba tháng ba âm lịch, tức ba mươi mốt tháng ba năm một nghìn không trăm hai mươi tám. | 1028: mồng 3 tháng 3 = 31/3/1028 |
| 18003 | Cánh cửa phía tây | Các quan kéo đến cung Long Đức xin thái tử vâng di chiếu lên ngôi, còn ba người em của ông nghe tin liền đem quân vào phục sẵn trong thành. |  |
| 18004 | Cánh cửa phía tây | Một đạo quân nấp trong Long Thành, còn hai đạo kia nấp sau cánh cửa Quảng Phúc, cửa phía tây của kinh thành, chờ thái tử đến để đánh úp. |  |
| 18005 | Cánh cửa phía tây | Cánh cửa ấy do chính vua cha dựng mười tám năm trước, trên một vùng đất mà ông đã phải rời bỏ cả kinh đô cũ để có được. |  |
| 18006 | Cánh cửa phía tây | Vì sao một vị vua lại bỏ kinh đô đã đóng hơn bốn mươi năm, để dựng cánh cửa ấy ở một vùng đất mới bên sông? |  |
| 18007 | Cánh cửa phía tây | Người dựng nên nó không sinh ra trong cung điện mà lớn lên bên một thiền sư, và ông tên là Lý Công Uẩn. |  |
| 18008 | Đứa trẻ bên nhà thiền sư | Ông sinh ngày mười hai tháng hai âm lịch năm chín trăm bảy mươi bốn, tức khoảng ngày tám tháng ba, ở châu Cổ Pháp, và mẹ ông họ Phạm. | 974: 12/2 âm = 8/3/974 (±1 ngày) |
| 18009 | Đứa trẻ bên nhà thiền sư | Về người cha chỉ có truyền thuyết nên ta bỏ qua, còn chuyện có thật bắt đầu khi cậu bé lên ba, được mẹ ẵm đến nhà thiền sư Lý Khánh Văn. |  |
| 18010 | Đứa trẻ bên nhà thiền sư | Thiền sư nhận cậu làm con nuôi, nên từ đó cậu mang họ Lý, lớn lên thông minh và có dáng người tuấn tú khác thường. |  |
| 18011 | Đứa trẻ bên nhà thiền sư | Lúc đi học ở chùa Lục Tổ, cậu gặp sư Vạn Hạnh, và người ta kể rằng vị sư đã nói cậu bé sau này sẽ làm bậc minh chủ. |  |
| 18012 | Đứa trẻ bên nhà thiền sư | Đó chỉ là lời kể về sau nên ta không coi là bằng chứng, còn điều chắc chắn hơn nằm ở chính tính cách của cậu. |  |
| 18013 | Đứa trẻ bên nhà thiền sư | Cậu không chăm lo của cải, học kinh sử cũng chỉ qua loa, nhưng khảng khái và có chí lớn, nên khi trưởng thành đã bước vào triều đình nhà Lê. |  |
| 18014 | Người giữ cung nhà Lê | Triều Tiền Lê do vua Lê Hoàn dựng nên, nhưng ông mất vào tháng ba âm lịch năm một nghìn không trăm linh năm thì các con liền tranh ngôi. | 1005: tháng 3 âm = 11/4–10/5/1005 |
| 18015 | Người giữ cung nhà Lê | Cuộc giành giật kéo dài tám tháng, trong nước không có vua, rồi mùa đông Lê Long Việt lên ngôi và ba ngày sau bị em là Lê Long Đĩnh giết. | 1005: mùa đông (tháng 10 âm = 5/11–3/12/1005) |
| 18016 | Người giữ cung nhà Lê | Các quan sợ hãi bỏ chạy hết, chỉ riêng Lý Công Uẩn ở lại ôm xác nhà vua mà khóc. |  |
| 18017 | Người giữ cung nhà Lê | Thấy vậy, Lê Long Đĩnh khen ông là người trung thành, rồi cho ông giữ quân canh kinh thành và thăng dần đến chức đứng đầu đội quân canh giữ cung vua. |  |
| 18018 | Người giữ cung nhà Lê | Nhưng phục vụ vị vua mới không hề dễ, vì Lê Long Đĩnh thích giết người và nổi tiếng là một ông vua bạo ngược. |  |
| 18019 | Người giữ cung nhà Lê | Có lần vua ăn quả khế thấy hạt mận, mà chữ Lý cũng có nghĩa là cây mận, nên vua tin đó là lời sấm báo họ Lý sẽ lên. |  |
| 18020 | Người giữ cung nhà Lê | Từ đó vua ngầm cho người tìm giết những người họ Lý, vậy mà Lý Công Uẩn đứng ngay bên cạnh vua và vua vẫn không hề biết. |  |
| 18021 | Người giữ cung nhà Lê | Về sau Lê Long Đĩnh mắc bệnh trĩ nặng, phải nằm nghe việc triều đình, nên người đời gọi ông là Lê Ngọa Triều, nghĩa là vua nằm nghe việc nước. |  |
| 18022 | Người giữ cung nhà Lê | Ngày mười chín tháng mười một năm một nghìn không trăm linh chín, Lê Long Đĩnh qua đời, để lại một người con còn quá bé để nối ngôi. | 1009: ngày Tân Hợi = 19/11/1009 |
| 18023 | Lời nói khích và ngôi vua | Lúc ấy Lý Công Uẩn và Nguyễn Đê mỗi người dẫn năm trăm quân vào canh trong cung, nên lực lượng mạnh nhất của hoàng cung nằm trong tay hai người. |  |
| 18024 | Lời nói khích và ngôi vua | Một viên quan hầu cận tên Đào Cam Mộc nhận ra điều đó, và nhân lúc vắng người ông ta tìm đến nói khích Lý Công Uẩn. |  |
| 18025 | Lời nói khích và ngôi vua | Ông ta nói vua cũ bạo ngược, vua nối còn bé, vậy sao Lý Công Uẩn không thuận lòng trời, theo ý dân mà cứ giữ lễ nhỏ? |  |
| 18026 | Lời nói khích và ngôi vua | Lý Công Uẩn thích lời ấy nhưng còn ngờ Đào Cam Mộc có mưu khác, nên giả vờ mắng và dọa sẽ bắt ông ta nộp quan. |  |
| 18027 | Lời nói khích và ngôi vua | Đào Cam Mộc thong thả đáp rằng chính thiên thời và nhân sự khiến ông ta dám nói, và ông ta không sợ chết. |  |
| 18028 | Lời nói khích và ngôi vua | Đến lúc ấy Lý Công Uẩn mới nói thật, rằng mình đâu nỡ tố cáo ai, chỉ sợ lời ấy lọt ra ngoài thì cả hai cùng chết. |  |
| 18029 | Lời nói khích và ngôi vua | Hôm sau Đào Cam Mộc lại tìm ông và nói rằng ai cũng bảo họ Lý sắp dựng nghiệp lớn, nên đây là lúc trời trao người theo, còn ngại gì nữa. |  |
| 18030 | Lời nói khích và ngôi vua | Lý Công Uẩn đáp rằng mình đã hiểu ý ấy, và ý ấy giống hệt ý sư Vạn Hạnh. |  |
| 18031 | Lời nói khích và ngôi vua | Đào Cam Mộc liền đem chuyện nói với các quan, và ngay hôm ấy họ họp bàn, cho rằng dân chán vua cũ mà không ai muốn theo vua nối. |  |
| 18032 | Lời nói khích và ngôi vua | Họ nói nếu không nhân lúc này tôn Lý Công Uẩn lên, lỡ có biến thì chưa chắc còn giữ được cái đầu. |  |
| 18033 | Lời nói khích và ngôi vua | Vậy là ngày hai mươi mốt tháng mười một năm một nghìn không trăm linh chín, cả triều dìu ông lên chính điện. | 1009: ngày Quý Sửu = 21/11/1009 |
| 18034 | Lời nói khích và ngôi vua | Trăm quan lạy rạp dưới sân và hô chúc nhà vua sống muôn năm, còn cuộc đổi ngôi ấy không có một trận giao tranh nào được ghi lại. |  |
| 18035 | Lời nói khích và ngôi vua | Tân hoàng đế tha tội cho nhiều người trong cả nước, rồi lấy năm sau làm năm đầu niên hiệu Thuận Thiên, nghĩa là thuận theo ý trời. |  |
| 18036 | Lời nói khích và ngôi vua | Ông truy phong cha mẹ và lập con trai trưởng là Lý Phật Mã làm thái tử, rồi gả con gái lớn cho Đào Cam Mộc. |  |
| 18037 | Lời nói khích và ngôi vua | Người đã ngỏ lời đầu tiên ấy được phong làm Nghĩa Tín Hầu, và từ một viên quan hầu cận trở thành bậc công thần của triều mới. |  |
| 18038 | Lời nói khích và ngôi vua | Nhưng ngôi vua đã có thì còn một câu hỏi lớn đang chờ, là triều đình mới của ông sẽ đặt ở đâu. |  |
| 18039 | Hoa Lư không còn đủ | Kinh đô lúc ấy là Hoa Lư, nơi vua Đinh Bộ Lĩnh dựng cung điện hơn bốn mươi năm trước, giữa những dãy núi đá dựng đứng. |  |
| 18040 | Hoa Lư không còn đủ | Trong thời loạn, núi đá như bức tường che chở khiến nơi này rất dễ giữ, nhưng thời bình cần một kinh đô có những cánh cửa mở ra bốn phương. |  |
| 18041 | Hoa Lư không còn đủ | Một kinh đô như thế cần dân cư đông đúc, đường đi thuận tiện và đất rộng để thành phố lớn dần, trong khi Hoa Lư lại ẩm thấp và chật hẹp. |  |
| 18042 | Hoa Lư không còn đủ | Chính nhà vua nhận xét như thế, và ông còn nhìn lại hai triều trước, cả hai đều đóng đô ở Hoa Lư và đều ngắn ngủi. |  |
| 18043 | Hoa Lư không còn đủ | Nhà Đinh chỉ có hai vua, còn nhà Tiền Lê có ba vua và tồn tại hai mươi chín năm. |  |
| 18044 | Đại La bên sông | Lý Công Uẩn muốn tránh con đường ấy, nên ông nhìn về thành Đại La bên sông Hồng. |  |
| 18045 | Đại La bên sông | Đó là tòa thành cũ do tướng Cao Biền của nhà Đường đắp từ năm tám trăm sáu mươi sáu, hơn một trăm bốn mươi năm trước. |  |
| 18046 | Đại La bên sông | Các quan nhà Đường từng ngồi đó cai trị đất Giao Châu, và chính bản chiếu của vua gọi nơi này là đô cũ của Cao Vương. |  |
| 18047 | Đại La bên sông | Thành có sông Hồng chảy ngay bên cạnh nên thuyền bè nhiều nơi có thể cập bến, còn đất quanh đó thì rộng và bằng phẳng. |  |
| 18048 | Đại La bên sông | Ở đó một kinh đô có thể lớn dần lên thành một thành phố, chứ không bị núi đá bó chặt như Hoa Lư. |  |
| 18049 | Đại La bên sông | Nhưng dời kinh đô là bỏ những cung điện đã dựng để làm lại từ đầu ở một nơi xa, nên nhà vua cần một lý lẽ thật vững. |  |
| 18050 | Lá chiếu dời đô | Tháng hai âm lịch năm một nghìn không trăm mười, nhà vua về thăm châu Cổ Pháp quê mình và ban tiền lụa cho các cụ già trong làng. | 1010: tháng 2 âm = 17/2–17/3/1010 |
| 18051 | Lá chiếu dời đô | Cũng trong năm ấy ông sai sứ sang nhà Tống để giữ hòa hảo, rồi tự tay viết bản chiếu dời đô gửi cho cả triều đình. |  |
| 18052 | Lá chiếu dời đô | Bản chiếu mở đầu bằng chuyện xưa của Trung Hoa, rằng nhà Thương đến đời vua Bàn Canh đã năm lần dời đô, còn nhà Chu cũng ba lần. |  |
| 18053 | Lá chiếu dời đô | Theo bản chiếu, các vua ấy không dời đô bừa theo ý riêng, mà làm vậy để mưu nghiệp lớn và lo cho con cháu muôn đời. |  |
| 18054 | Lá chiếu dời đô | Rồi chiếu nói thẳng về hai triều ngay trước, rằng nhà Đinh và nhà Tiền Lê theo ý riêng, cứ yên đóng đô một chỗ. |  |
| 18055 | Lá chiếu dời đô | Vì thế, nhà vua viết, vận nước ngắn ngủi và trăm họ hao tổn, nên ông rất đau đớn mà không thể không dời. |  |
| 18056 | Lá chiếu dời đô | Tiếp đó chiếu tả Đại La bằng những lời đầy tự hào, rằng thành ở giữa vùng trời đất, thế đất như rồng cuộn hổ ngồi. |  |
| 18057 | Lá chiếu dời đô | Đất ở đó rộng mà bằng phẳng, cao mà sáng sủa, dân không khổ vì thấp trũng tối tăm, muôn vật đều tươi tốt. |  |
| 18058 | Lá chiếu dời đô | Kết lại, nhà vua cho rằng đó là nơi tụ hội quan trọng của bốn phương, xứng đáng làm kinh đô muôn đời. |  |
| 18059 | Lá chiếu dời đô | Và ở cuối bản chiếu, ông không ra lệnh mà hỏi bầy tôi rằng, trẫm muốn nhân thế đất tốt ấy để định nơi ở, các khanh nghĩ thế nào? |  |
| 18060 | Lá chiếu dời đô | Bầy tôi đáp rằng bệ hạ vì thiên hạ lập kế lâu dài, điều lợi như thế thì ai dám không theo, và nhà vua cả mừng. |  |
| 18061 | Con thuyền dưới chân thành | Tháng bảy âm lịch năm một nghìn không trăm mười, khoảng giữa tháng tám dương lịch, nhà vua rời Hoa Lư ra Đại La, thuyền ngự tạm đỗ dưới chân thành. | 1010: tháng 7 âm = 12/8–10/9/1010 |
| 18062 | Con thuyền dưới chân thành | Người xưa kể rằng lúc ấy có rồng vàng hiện lên trên thuyền của nhà vua, nhưng đó là điềm lạ được ghi lại chứ không ai chứng minh được. |  |
| 18063 | Con thuyền dưới chân thành | Dù vậy, ý nghĩa của nó rất rõ, là đất này được trời chấp nhận và vị vua này là người được chọn. |  |
| 18064 | Con thuyền dưới chân thành | Nhà vua liền đổi tên thành thành Thăng Long, nghĩa là rồng bay lên, và cái tên do chính ông đặt ấy sống lâu hơn cả triều đại nhà Lý. |  |
| 18065 | Bốn cánh cửa và các điện | Có tên rồi thì phải có cung điện, nên phía trước nhà vua dựng điện Càn Nguyên làm nơi coi chầu, hai bên là điện Tập Hiền và điện Giảng Võ. |  |
| 18066 | Bốn cánh cửa và các điện | Sau điện Càn Nguyên là hai điện Long An và Long Thụy, nơi nhà vua nghỉ ngơi, rồi ông cho dựng kho tàng, đắp thành và đào hào. |  |
| 18067 | Bốn cánh cửa và các điện | Bốn mặt thành mở bốn cửa, cửa phía đông tên Tường Phù, cửa phía tây tên Quảng Phúc, cửa phía nam tên Đại Hưng và cửa phía bắc tên Diệu Đức. |  |
| 18068 | Bốn cánh cửa và các điện | Hãy nhớ cánh cửa phía tây ấy, vì mười tám năm sau hai người con của ông sẽ nấp sau nó. |  |
| 18069 | Bốn cánh cửa và các điện | Các nơi cũ cũng được đổi tên để ghi nhớ nguồn gốc, châu Cổ Pháp quê ông thành phủ Thiên Đức, còn thành Hoa Lư thành phủ Trường Yên. |  |
| 18070 | Bốn cánh cửa và các điện | Tháng mười hai âm lịch, tức đầu năm một nghìn không trăm mười một, cung Thúy Hoa xây xong, và nhân dịp ấy ông tha thuế cho cả nước ba năm. | 1010: tháng 12 âm = 7/1–5/2/1011 |
| 18071 | Bốn cánh cửa và các điện | Những người mồ côi, góa chồng, già yếu mà còn thiếu thuế từ lâu cũng được tha hết, và cũng năm ấy nhà Tống phong ông làm Giao Chỉ quận vương. |  |
| 18072 | Bốn cánh cửa và các điện | Vậy là kinh đô mới vừa dựng đã được nước láng giềng phương bắc công nhận. |  |
| 18073 | Những năm trị vì | Dời đô chỉ là bước đầu, vì cùng năm ấy ông đổi mười đạo thành hai mươi bốn lộ để chia nhỏ đất nước cho dễ cai quản. |  |
| 18074 | Những năm trị vì | Tháng hai âm lịch năm một nghìn không trăm mười một, ông đem sáu quân đi đánh giặc Cử Long ở Ái Châu. | 1011: tháng 2 âm = 8/3–5/4/1011 |
| 18075 | Những năm trị vì | Hai triều Đinh và Lê đều không đánh nổi bọn giặc này, nhưng lần ấy nhà vua đốt các bộ lạc của chúng và bắt kẻ đầu sỏ, nên giặc tan. |  |
| 18076 | Những năm trị vì | Năm một nghìn không trăm mười hai ông thân chinh đi đánh Diễn Châu, và trên đường về, đến vùng biển Biện Sơn, trời đất bỗng tối sầm, gió sấm dữ dội. |  |
| 18077 | Những năm trị vì | Nhà vua đốt hương khấn rằng mình là người ít đức, không dám cậy binh uy mà đánh bừa, chỉ vì Diễn Châu làm điều tàn ngược nên buộc phải đánh. |  |
| 18078 | Những năm trị vì | Ông xin rằng nếu lỡ giết oan người hiền thì trời cứ trách riêng mình, và người ta kể rằng khấn xong gió sấm đều yên lặng. |  |
| 18079 | Những năm trị vì | Năm một nghìn không trăm mười ba ông định ra các thứ thuế trong nước, chia làm sáu loại. |  |
| 18080 | Những năm trị vì | Đến tháng giêng âm lịch năm một nghìn không trăm mười bốn, quân Nam Chiếu đem rất đông người tràn vào cướp ở phía bắc và đóng trại ở bến Kim Hoa. | 1014: tháng giêng âm = 2/2–3/3/1014 |
| 18081 | Những năm trị vì | Nhà vua sai Dực Thánh Vương đem quân đánh thắng lớn, bắt được rất nhiều quân và ngựa của đối phương. |  |
| 18082 | Những năm trị vì | Ông cho đem một trăm con ngựa bắt được sang biếu nhà Tống, và vua Tống ban thưởng mũ, đai, tiền bạc cho sứ giả. |  |
| 18083 | Những năm trị vì | Bên cạnh việc quân, nhà vua dốc sức cho Phật giáo, cho xây nhiều chùa, đúc chuông, chép kinh Tam tạng, và cho hơn một nghìn người ở kinh đô đi tu. |  |
| 18084 | Những năm trị vì | Điều đó cũng dễ hiểu, vì ông từng lớn lên bên nhà thiền sư và suốt thời trị vì vẫn dành cho đạo Phật sự coi trọng ấy. |  |
| 18085 | Những năm trị vì | Tháng giêng âm lịch năm một nghìn không trăm mười lăm, Đào Cam Mộc, người từng khuyên ông lên ngôi, qua đời và được tặng chức Thái sư á vương. | 1015: tháng giêng âm = 23/1–20/2/1015 |
| 18086 | Điện Long An | Mười tám năm đã trôi qua từ ngày dời đô, và kinh thành Thăng Long đã có cung điện, có thành, có bốn cửa mở ra bốn phương. |  |
| 18087 | Điện Long An | Thái tử Lý Phật Mã đã trưởng thành và từng thay cha cầm quân đi đánh các nơi, còn nhà vua bước vào năm cuối đời. |  |
| 18088 | Điện Long An | Tháng hai âm lịch năm một nghìn không trăm hai mươi tám, nhà vua không khỏe. | 1028: tháng 2 âm = 28/2–28/3/1028 |
| 18089 | Điện Long An | Đến mồng một tháng ba, tức hai mươi chín tháng ba, mặt trời bị nhật thực che khuất giữa ban ngày. | 1028: mồng 1 tháng 3 (Bính Thân) = 29/3/1028 |
| 18090 | Điện Long An | Hai ngày sau, ngày ba mươi mốt tháng ba, nhà vua mất ngay tại điện Long An do chính ông dựng, thọ năm mươi lăm tuổi theo cách tính của người xưa. | 1028: ngày Mậu Tuất = 31/3/1028 |
| 18091 | Điện Long An | Tính tròn thì ông hơn năm mươi bốn tuổi, ở ngôi mười tám năm và được an táng ở Thọ Lăng. |  |
| 18092 | Cánh cửa Quảng Phúc | Nhà Lý chưa kịp lo xong tang lễ thì mối nguy đã nổ ra ngay trong hoàng tộc, đúng tại cánh cửa mà ta đã gặp lúc đầu. |  |
| 18093 | Cánh cửa Quảng Phúc | Ba người em của thái tử Lý Phật Mã là Đông Chinh Vương, Dực Thánh Vương và Vũ Đức Vương đã đem quân phủ mình vào ẩn sẵn trong thành. |  |
| 18094 | Cánh cửa Quảng Phúc | Đông Chinh Vương nấp ở Long Thành, còn Dực Thánh Vương và Vũ Đức Vương nấp ở cửa Quảng Phúc, chờ thái tử đi qua để đánh úp. |  |
| 18095 | Cánh cửa Quảng Phúc | Một lát sau thái tử đi vào từ cửa Tường Phù, và khi đến điện Càn Nguyên thì ông nhận ra có biến. |  |
| 18096 | Cánh cửa Quảng Phúc | Ông cho đóng hết các cửa điện và sai lính canh trong cung phòng giữ, rồi nói rằng mình không hề phụ bạc anh em. |  |
| 18097 | Cánh cửa Quảng Phúc | Ông nói ba vương đã quên lời cha dặn mà định chiếm ngôi báu, và hỏi các quan xung quanh nên làm thế nào. |  |
| 18098 | Cánh cửa Quảng Phúc | Viên nội thị Lý Nhân Nghĩa xin cho đánh một trận để quyết thua được, nhưng thái tử chưa chịu. |  |
| 18099 | Cánh cửa Quảng Phúc | Thái tử im lặng hồi lâu rồi nói rằng vua cha vừa mất chưa kịp quàn mà anh em đã giết nhau thì muôn đời sẽ chê cười. |  |
| 18100 | Cánh cửa Quảng Phúc | Ông muốn che giấu tội của ba vương để họ tự rút quân, giữ trọn tình ruột thịt, nhưng quân của ba vương lại bao vây càng gấp. |  |
| 18101 | Cánh cửa Quảng Phúc | Lúc ấy thái tử nói rằng nếu thế thì ông chỉ còn biết mặc áo tang đứng hầu vua cha, còn mọi việc xin giao cho các quan. |  |
| 18102 | Cánh cửa Quảng Phúc | Lý Nhân Nghĩa cùng các quan lạy hai lạy, nói rằng chết vì vua gặp nạn là bổn phận của họ, rồi ra lệnh mở cửa cho vệ sĩ xông ra đánh. |  |
| 18103 | Cánh cửa Quảng Phúc | Vệ sĩ trong cung ai cũng vui lòng xông pha, mỗi người địch với trăm người, nhưng hai bên giao chiến mãi chưa phân thắng bại. |  |
| 18104 | Cánh cửa Quảng Phúc | Bỗng tướng Lê Phụng Hiểu tức giận rút gươm, chạy thẳng tới cửa Quảng Phúc. |  |
| 18105 | Cánh cửa Quảng Phúc | Ông hô lớn rằng Vũ Đức Vương nhòm ngó ngôi báu, trên quên ơn vua cha, dưới trái nghĩa tôi con. |  |
| 18106 | Cánh cửa Quảng Phúc | Rồi ông xông thẳng tới chỗ ngựa của Vũ Đức Vương, vương quay ngựa tránh nhưng ngựa quỵ xuống, và Vũ Đức Vương bị Lê Phụng Hiểu bắt giết. |  |
| 18107 | Cánh cửa Quảng Phúc | Quân của ba vương thua chạy, và chỉ có hai vương Đông Chinh cùng Dực Thánh thoát được. |  |
| 18108 | Cánh cửa Quảng Phúc | Lê Phụng Hiểu trở về, mặc nguyên áo trận vào báo tin thắng ngay trước linh cữu của vua cha, rồi sang điện Càn Nguyên báo cho thái tử. |  |
| 18109 | Cánh cửa Quảng Phúc | Thái tử khen rằng ông còn trung dũng hơn Uất Trì Kính Đức, vị công thần nổi tiếng của nhà Đường, rồi lên ngôi, và đó là vua Lý Thái Tông. |  |
| 18110 | Kết | Cửa Tường Phù, cửa Quảng Phúc, điện Càn Nguyên và điện Long An, những nơi diễn ra ngày hôm ấy, đều do Lý Công Uẩn dựng năm một nghìn không trăm mười. |  |
| 18111 | Kết | Khi dựng chúng, ông đã viết trong bản chiếu rằng nhà Đinh và nhà Tiền Lê vận nước ngắn ngủi vì cứ yên đóng đô một chỗ. |  |
| 18112 | Kết | Không ai biết ông có nghĩ trước đến ngày ba mươi mốt tháng ba năm một nghìn không trăm hai mươi tám ấy hay không. | 1028: 31/3/1028 |
| 18113 | Kết | Nhưng đến ngày ấy kinh đô ông dựng vẫn đứng vững, và ngôi vua vẫn truyền được cho con. |  |
| 18114 | Kết | Nhà Lý giữ ngôi hơn hai trăm năm, còn cái tên Thăng Long mà ông đặt cho nơi con thuyền dừng lại cũng sống lâu hơn cả triều đại của ông. |  |
| 18115 | Kết | Mười tám năm trước ông chỉ hỏi bầy tôi một câu, rằng nhân đất tốt ấy mà định nơi ở thì các khanh nghĩ thế nào. |  |
| 18116 | Kết | Và ở cánh cửa Quảng Phúc, cánh cửa phía tây ông dựng, một cuộc tranh ngôi giữa chính các con ông đã kết thúc. |  |
