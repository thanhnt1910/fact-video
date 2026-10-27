# Kịch bản Lý Công Uẩn: dời đô về Thăng Long (bản 2, hướng "Cánh cửa Quảng Phúc", để chủ kênh duyệt)

Mã `ly1`, 120 đoạn (18001–18120), 3,099 chữ, khoảng 17.2 phút ở 3 chữ/giây (đọc thực tế khoảng 3,3 chữ/giây nên khoảng 15–16 phút, vượt sàn 10 phút). Bộ kiểm `kiem_kich_ban.py ly1`: 0 lỗi, không đoạn nào dưới 14 chữ. File giọng: `ke-hoach/thu-giong-hai/ly1_full.json`. Chưa chạy giọng, chưa làm bản đồ, chưa dựng. Bản 1 (mở bằng câu hỏi cuối chiếu) đã bỏ vì dập khuôn Lê Hoàn.

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
| Lời nói khích và ngôi vua | Công Uẩn và Nguyễn Đê mỗi người 500 quân; Cam Mộc nói khích; giả vờ mắng; hôm sau; họp triều; Thuận Thiên; tôn hiệu 50 chữ; Ngô Sĩ Liên chê; truy phong; gả con gái | khớp từng ý |
| Hoa Lư không còn đủ | "ẩm thấp chật hẹp, không đủ làm chỗ ở của đế vương"; nhà Đinh 2 vua, Tiền Lê 3 vua 29 năm | khớp; câu "núi đá che chở" là hiểu biết chung về địa thế |
| Đại La bên sông | Cao Biền đắp thành năm 866; "đô cũ của Cao Vương"; sông Hồng bên cạnh | khớp; các câu về thuyền bè và đất rộng suy từ chính bản chiếu |
| Lá chiếu dời đô | Mùa xuân 1010 về Cổ Pháp; sai sứ sang Tống; Bàn Canh 5 lần, nhà Chu 3 lần; phê Đinh, Lê; tả Đại La; câu hỏi cuối; bầy tôi đáp | khớp |
| Con thuyền dưới chân thành | Mùa thu tháng 7, thuyền đỗ dưới thành, rồng vàng, tên Thăng Long | khớp; nói rõ là điềm người xưa kể, không phải bằng chứng |
| Bốn cánh cửa và các điện | Điện Càn Nguyên, Tập Hiền, Giảng Võ, Long An, Long Thụy; bốn cửa Tường Phù (đông), Quảng Phúc (tây), Đại Hưng (nam), Diệu Đức (bắc); phủ Thiên Đức, phủ Trường Yên; cung Thúy Hoa; tha thuế 3 năm; Tống phong Giao Chỉ quận vương | khớp |
| Những năm trị vì | 10 đạo thành 24 lộ; Cử Long; Diễn Châu và lời khấn ở Biện Sơn; 6 loại thuế; Nam Chiếu, Dực Thánh Vương thắng ở Kim Hoa; 100 ngựa biếu Tống; chùa, chuông, Tam tạng; Lê Văn Hưu chê; Cam Mộc mất 1015 | khớp |
| Điện Long An | Mười tám năm; mồng 1 tháng 3 nhật thực; băng ở điện Long An; thọ 55 (hơn 54 tuổi tròn); Thọ Lăng; lời đánh giá | khớp; cách nói hai cách tuổi đã chốt |
| Cánh cửa Quảng Phúc | Thái tử vào cửa Tường Phù đến điện Càn Nguyên; đóng cửa điện; Lý Nhân Nghĩa; thái tử im lặng; mở cửa đánh; Lê Phụng Hiểu bắt giết Vũ Đức Vương; hai vương thoát; báo tin trước linh cữu; Uất Trì Kính Đức | khớp từng ý |
| Kết | Các cửa và điện dựng 1010 là nơi diễn ra ngày 1028; nhà Lý hơn 200 năm; tên Thăng Long | nối các chương trên; nhà Lý 1009–1225 khoảng 216 năm (kỷ nhà Lý kết thúc ở Chiêu Hoàng) |

## Điểm cần chủ kênh duyệt (phần sáng tạo, ghi độ chắc)

- **"Ba người em của thái tử", "hai người con của ông":** thái tử gọi ba vương là "anh em"; Dực Thánh Vương là con thứ theo chú thích; Vũ Đức Vương Toàn thư chú là "chưa rõ" thân thế. **Cần kiểm thêm** nếu muốn nói chắc "con của vua".
- **"Mặt trời tắt giữa ban ngày" (nhật thực):** hình ảnh mở đầu; nhật thực mồng 1 tháng 3 là có thật.
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

Chuyện mẹ gặp người thần ở chùa Tiêu Sơn, chó con có chữ "thiên tử", cây gạo bị sét có sấm ký, lời Vạn Hạnh nói với Công Uẩn hơn 70 tuổi, các điềm lạ năm 1012 (vết chân thần), 1016, 1017, 1020, ngựa Bạch Long, tin đồn đầu độc, việc giết hai em của Lê Long Đĩnh (An Nam chí lược), các chi tiết bạo ngược nặng của Lê Long Đĩnh (róc mía trên đầu nhà sư, giết mèo cho các vương ăn...).

## Gợi ý tiêu đề

1. Vì sao Lý Công Uẩn bỏ Hoa Lư để ra Thăng Long?
2. Đứa trẻ nuôi trong nhà thiền sư và quyết định dời đô năm 1010
3. Một câu hỏi cuối lá chiếu đã đổi kinh đô nước Việt
4. Lê Phụng Hiểu và ngày ba vị vương phục binh trong cung vua
5. Cánh cửa Lý Công Uẩn dựng và ngày ba người con nấp sau nó

## Lời kể

| n | chương | lời |
|---|---|---|
| 18001 | Cánh cửa phía tây | Hai ngày sau khi mặt trời tắt giữa ban ngày, nhà vua qua đời trong cung. |
| 18002 | Cánh cửa phía tây | Các quan kéo đến xin thái tử nối ngôi theo lời cha dặn, nhưng ba người em của ông đã đem quân vào thành và ẩn sẵn để chờ ông đi qua. |
| 18003 | Cánh cửa phía tây | Một đạo quân nấp trong Long Thành, còn hai đạo kia nấp ngay sau cánh cửa Quảng Phúc, cánh cửa mở ra ở phía tây kinh thành. |
| 18004 | Cánh cửa phía tây | Cánh cửa ấy do chính vua cha dựng mười tám năm trước, trên một vùng đất mà ông phải bỏ cả kinh đô cũ mới có được. |
| 18005 | Cánh cửa phía tây | Vì sao một vị vua lại chịu bỏ nơi đã làm kinh đô hơn bốn mươi năm, để dựng nên cánh cửa ấy ở một vùng đất mới bên sông? |
| 18006 | Đứa trẻ bên nhà thiền sư | Người dựng nó đã lớn lên bên một thiền sư chứ không phải trong cung điện, và ông tên là Lý Công Uẩn. |
| 18007 | Đứa trẻ bên nhà thiền sư | Ông sinh ngày mười hai tháng hai âm lịch năm chín trăm bảy mươi bốn ở châu Cổ Pháp, mẹ ông họ Phạm. |
| 18008 | Đứa trẻ bên nhà thiền sư | Về người cha chỉ có truyền thuyết nên ta bỏ qua. Câu chuyện thật bắt đầu năm ông ba tuổi, khi mẹ ẵm ông đến nhà thiền sư Lý Khánh Văn. |
| 18009 | Đứa trẻ bên nhà thiền sư | Thiền sư nhận ông làm con nuôi nên ông mang họ Lý từ đó, và đứa bé lớn lên thông minh, dáng người tuấn tú khác thường. |
| 18010 | Đứa trẻ bên nhà thiền sư | Lúc nhỏ đi học, ông gặp sư Vạn Hạnh ở chùa Lục Tổ. Người ta kể rằng vị sư khen cậu bé sau này sẽ làm bậc minh chủ. |
| 18011 | Đứa trẻ bên nhà thiền sư | Đó là lời kể về sau nên ta không coi nó là bằng chứng, và điều chắc chắn hơn nằm ở tính cách của ông. |
| 18012 | Đứa trẻ bên nhà thiền sư | Lớn lên ông không chăm lo sản nghiệp, chỉ học kinh sử qua loa, nhưng khảng khái và có chí lớn, rồi bước vào triều đình nhà Lê. |
| 18013 | Người giữ cung nhà Lê | Triều Tiền Lê do vua Lê Hoàn dựng nên, nhưng ông vừa mất thì các con đã tranh nhau ngôi. |
| 18014 | Người giữ cung nhà Lê | Năm một nghìn không trăm linh năm, Lê Long Việt mới lên ngôi được ba ngày đã bị em là Lê Long Đĩnh giết, và các quan sợ hãi bỏ đi hết. |
| 18015 | Người giữ cung nhà Lê | Chỉ riêng Lý Công Uẩn ở lại ôm xác nhà vua mà khóc, nên Lê Long Đĩnh khen ông là người trung thành. |
| 18016 | Người giữ cung nhà Lê | Ông được làm phó chỉ huy quân canh giữ kinh thành, rồi thăng đến chức Tả thân vệ điện tiền chỉ huy sứ, đứng đầu đội quân canh giữ cung vua. |
| 18017 | Người giữ cung nhà Lê | Nhưng vị vua mới không phải người dễ phục vụ, vì Lê Long Đĩnh thích giết người và nổi tiếng là một ông vua bạo ngược. |
| 18018 | Người giữ cung nhà Lê | Một lần vua ăn quả khế thì thấy hạt mận, mà chữ Lý trong tên họ cũng có nghĩa là cây mận, nên vua tin đó là lời sấm. |
| 18019 | Người giữ cung nhà Lê | Từ đó vua ngầm cho người đi tìm giết những người họ Lý, vậy mà Lý Công Uẩn đang đứng ngay bên cạnh vua và vua vẫn không hề biết. |
| 18020 | Người giữ cung nhà Lê | Về sau Lê Long Đĩnh mắc bệnh trĩ nặng, phải nằm để nghe việc triều đình, nên người đời gọi là Lê Ngọa Triều, nghĩa là ông vua nằm nghe việc nước. |
| 18021 | Người giữ cung nhà Lê | Mùa đông năm một nghìn không trăm linh chín, Lê Long Đĩnh qua đời, và người con nối ngôi lúc ấy còn quá bé. |
| 18022 | Lời nói khích và ngôi vua | Lúc ấy Lý Công Uẩn và Nguyễn Đê mỗi người dẫn năm trăm quân vào canh trong cung, nên sức mạnh lớn nhất của hoàng cung nằm trong tay họ. |
| 18023 | Lời nói khích và ngôi vua | Một viên quan hầu cận tên Đào Cam Mộc nhận ra điều đó, nên nhân lúc vắng người ông ta nói khích. |
| 18024 | Lời nói khích và ngôi vua | Ông ta bảo vua cũ bạo ngược nên trời chán ghét, còn vua nối thì quá nhỏ. |
| 18025 | Lời nói khích và ngôi vua | Rồi ông ta hỏi vì sao Lý Công Uẩn không thuận lòng trời, theo ý dân, mà cứ giữ mãi những lễ nhỏ. |
| 18026 | Lời nói khích và ngôi vua | Lý Công Uẩn thích lời ấy nhưng còn ngờ Đào Cam Mộc có mưu khác, nên ông giả vờ mắng rằng sao lại nói thế, tôi phải bắt ông nộp quan. |
| 18027 | Lời nói khích và ngôi vua | Đào Cam Mộc thong thả đáp rằng ông thấy thiên thời nhân sự là như vậy nên mới dám nói, và ông không sợ chết. |
| 18028 | Lời nói khích và ngôi vua | Lúc ấy Lý Công Uẩn mới đáp rằng mình đâu nỡ tố cáo ai, chỉ sợ lời ấy lọt ra ngoài thì cả hai cùng chết. |
| 18029 | Lời nói khích và ngôi vua | Hôm sau Đào Cam Mộc lại tìm ông, nói rằng ai cũng bảo họ Lý sắp khởi nghiệp lớn, và đây là lúc trời trao người theo, còn ngại gì nữa. |
| 18030 | Lời nói khích và ngôi vua | Lý Công Uẩn đáp rằng mình hiểu ý ông ta, và ý ấy giống hệt ý sư Vạn Hạnh. |
| 18031 | Lời nói khích và ngôi vua | Đào Cam Mộc liền đem chuyện ấy nói với các quan trong triều, và ai cũng vui lòng theo. |
| 18032 | Lời nói khích và ngôi vua | Ngay hôm ấy họ họp bàn, nói rằng dân chán vua cũ và không ai muốn theo vua nối. |
| 18033 | Lời nói khích và ngôi vua | Họ còn nói nếu không nhân lúc này tôn Lý Công Uẩn lên, lỡ có biến thì chưa chắc còn giữ được cái đầu. |
| 18034 | Lời nói khích và ngôi vua | Thế là cả triều cùng dìu ông lên chính điện, và trăm quan lạy rạp dưới sân, hô chúc nhà vua sống muôn năm. |
| 18035 | Lời nói khích và ngôi vua | Cuộc đổi ngôi ấy không có một trận giao tranh nào được ghi lại, và tân hoàng đế tha tội cho nhiều người trong cả nước. |
| 18036 | Lời nói khích và ngôi vua | Ông lấy năm sau làm năm đầu của niên hiệu Thuận Thiên, nghĩa là thuận theo ý trời, còn các quan dâng cho ông một tôn hiệu dài tới năm mươi chữ. |
| 18037 | Lời nói khích và ngôi vua | Sử gia Ngô Sĩ Liên về sau chê rằng như vậy là nịnh vua, vì người xưa tôn vua nhiều lắm cũng chỉ hơn mười chữ. |
| 18038 | Lời nói khích và ngôi vua | Nhà vua truy phong cha là Hiển Khánh Vương, mẹ là Minh Đức Thái hậu, và lập con trai trưởng là Lý Phật Mã làm thái tử. |
| 18039 | Lời nói khích và ngôi vua | Ông còn gả con gái trưởng cho Đào Cam Mộc và phong người đã ngỏ lời đầu tiên ấy làm Nghĩa Tín Hầu. |
| 18040 | Lời nói khích và ngôi vua | Nhưng ngôi vua đã có thì còn một câu hỏi lớn đang chờ, là triều đình mới của ông sẽ đặt ở đâu. |
| 18041 | Hoa Lư không còn đủ | Kinh đô lúc ấy là Hoa Lư, nơi vua Đinh Bộ Lĩnh dựng cung điện hơn bốn mươi năm trước giữa những dãy núi đá. |
| 18042 | Hoa Lư không còn đủ | Trong thời loạn, núi đá che chở khiến Hoa Lư rất dễ giữ, nhưng thời loạn đã qua, và một kinh đô cho thời bình cần nhiều thứ hơn núi đá. |
| 18043 | Hoa Lư không còn đủ | Nó cần chỗ cho dân cư đông đúc, cần đường đi thuận tiện, và cần đất rộng để thành phố lớn dần. |
| 18044 | Hoa Lư không còn đủ | Chính nhà vua nhận xét rằng thành Hoa Lư ẩm thấp và chật hẹp, không đủ làm chỗ ở của bậc đế vương. |
| 18045 | Hoa Lư không còn đủ | Hơn nữa, hai triều đại trước đều ngồi ở đây, và cả hai đều ngắn ngủi. |
| 18046 | Hoa Lư không còn đủ | Nhà Đinh chỉ có hai vua, còn nhà Tiền Lê có ba vua và tồn tại hai mươi chín năm. |
| 18047 | Đại La bên sông | Lý Công Uẩn muốn tránh con đường ấy, nên ông nhìn về thành Đại La bên sông Hồng. |
| 18048 | Đại La bên sông | Đại La là tòa thành cũ do tướng Cao Biền của nhà Đường cho đắp từ năm tám trăm sáu mươi sáu, hơn một trăm bốn mươi năm trước đó. |
| 18049 | Đại La bên sông | Thời nhà Đường đây là nơi các quan cai trị đất Giao Châu, và chính bản chiếu của vua gọi nó là đô cũ của Cao Vương. |
| 18050 | Đại La bên sông | Vị trí của thành rất đặc biệt vì sông Hồng chảy ngay bên cạnh, nên thuyền bè từ nhiều nơi có thể cập bến. |
| 18051 | Đại La bên sông | Đất đai quanh thành lại rộng rãi và bằng phẳng, đúng là chỗ để một kinh đô lớn lên thành một thành phố. |
| 18052 | Đại La bên sông | Nhưng dời kinh đô là bỏ những cung điện đã dựng để dựng lại từ đầu ở một nơi xa, nên nhà vua cần một lý lẽ thật vững. |
| 18053 | Lá chiếu dời đô | Mùa xuân năm một nghìn không trăm mười, nhà vua về thăm châu Cổ Pháp, quê mình, và ban tiền lụa cho các cụ già trong làng theo từng bậc khác nhau. |
| 18054 | Lá chiếu dời đô | Cũng trong năm ấy ông sai sứ sang nhà Tống để giữ hòa hảo, rồi tự tay viết bản chiếu dời đô, văn bản nhà vua gửi cho cả triều đình. |
| 18055 | Lá chiếu dời đô | Bản chiếu mở đầu bằng chuyện xưa của Trung Hoa, rằng nhà Thương đến đời vua Bàn Canh đã năm lần dời đô, còn nhà Chu cũng ba lần. |
| 18056 | Lá chiếu dời đô | Theo bản chiếu, các vua ấy không dời đô bừa theo ý riêng, mà làm vậy để mưu nghiệp lớn và lo cho con cháu muôn đời. |
| 18057 | Lá chiếu dời đô | Rồi ông nói thẳng về hai triều đại ngay trước mình, rằng nhà Đinh và nhà Tiền Lê theo ý riêng, cứ yên đóng đô một chỗ. |
| 18058 | Lá chiếu dời đô | Vì thế, nhà vua viết, vận nước ngắn ngủi và trăm họ hao tổn, nên ông rất đau đớn mà không thể không dời. |
| 18059 | Lá chiếu dời đô | Tiếp đó ông tả Đại La bằng những lời đầy tự hào, rằng thành ở giữa vùng trời đất, thế đất như rồng cuộn hổ ngồi. |
| 18060 | Lá chiếu dời đô | Đất ở đó rộng mà bằng phẳng, cao mà sáng sủa, dân không khổ vì thấp trũng tối tăm, muôn vật đều tươi tốt. |
| 18061 | Lá chiếu dời đô | Kết lại, nhà vua cho rằng đó là nơi tụ hội quan trọng của bốn phương, xứng đáng làm kinh đô muôn đời. |
| 18062 | Lá chiếu dời đô | Cuối bản chiếu, ông hỏi bầy tôi rằng trẫm muốn nhân thế đất tốt ấy để định nơi ở, các khanh nghĩ thế nào? |
| 18063 | Lá chiếu dời đô | Bầy tôi đáp rằng bệ hạ vì thiên hạ lập kế lâu dài, điều lợi như thế thì ai dám không theo, và nhà vua cả mừng. |
| 18064 | Con thuyền dưới chân thành | Mùa thu, tháng bảy năm một nghìn không trăm mười, nhà vua rời thành Hoa Lư để ra thành Đại La, và thuyền ngự tạm đỗ dưới chân thành. |
| 18065 | Con thuyền dưới chân thành | Từ chỗ ấy người xưa kể lại một chi tiết rất lạ, rằng có một con rồng vàng hiện lên trên thuyền của nhà vua. |
| 18066 | Con thuyền dưới chân thành | Đây là điềm lạ do người xưa ghi lại chứ không ai chứng minh được, nhưng ý nghĩa của nó thì rõ ràng. |
| 18067 | Con thuyền dưới chân thành | Người ta muốn nói rằng đất này được trời chấp nhận và vị vua này là người được chọn. Nhà vua đổi tên thành thành Thăng Long, nghĩa là rồng bay lên. |
| 18068 | Con thuyền dưới chân thành | Cái tên ấy do chính ông đặt, và nó sống lâu hơn cả triều đại nhà Lý. |
| 18069 | Bốn cánh cửa và các điện | Có tên rồi thì phải có cung điện, nên phía trước nhà vua dựng điện Càn Nguyên làm nơi coi chầu, hai bên là điện Tập Hiền và điện Giảng Võ. |
| 18070 | Bốn cánh cửa và các điện | Sau điện Càn Nguyên là hai điện Long An và Long Thụy, nơi nhà vua nghỉ ngơi, rồi ông cho dựng kho tàng, đắp thành và đào hào. |
| 18071 | Bốn cánh cửa và các điện | Bốn mặt thành mở bốn cửa, cửa phía đông tên Tường Phù, cửa phía tây tên Quảng Phúc, cửa phía nam tên Đại Hưng và cửa phía bắc tên Diệu Đức. |
| 18072 | Bốn cánh cửa và các điện | Hãy nhớ cánh cửa phía tây ấy, vì mười tám năm sau hai người con của ông sẽ nấp sau nó. |
| 18073 | Bốn cánh cửa và các điện | Các nơi cũ cũng được đổi tên để ghi nhớ nguồn gốc, châu Cổ Pháp quê ông thành phủ Thiên Đức, còn thành Hoa Lư thành phủ Trường Yên. |
| 18074 | Bốn cánh cửa và các điện | Tháng mười hai cung Thúy Hoa xây xong, và nhân dịp khánh thành ông tha thuế cho cả nước trong ba năm. |
| 18075 | Bốn cánh cửa và các điện | Những người mồ côi, góa chồng, già yếu mà còn thiếu thuế từ lâu cũng được tha hết. |
| 18076 | Bốn cánh cửa và các điện | Cũng năm ấy nhà Tống phong ông là Giao Chỉ quận vương, nên kinh đô mới vừa dựng đã được nước láng giềng phương bắc công nhận. |
| 18077 | Những năm trị vì | Dời đô chỉ là bước đầu, vì cùng năm ấy ông đổi mười đạo thành hai mươi bốn lộ để chia nhỏ đất nước cho dễ cai quản. |
| 18078 | Những năm trị vì | Năm sau ông đem sáu quân đi đánh giặc Cử Long ở Ái Châu, bọn giặc mà hai triều Đinh và Lê đều không đánh nổi. |
| 18079 | Những năm trị vì | Lần này nhà vua đốt các bộ lạc của chúng và bắt kẻ đầu sỏ, nên giặc ấy tan. |
| 18080 | Những năm trị vì | Năm một nghìn không trăm mười hai ông thân chinh đi đánh Diễn Châu, và trên đường về, đến vùng biển Biện Sơn, trời đất bỗng tối sầm, gió sấm dữ dội. |
| 18081 | Những năm trị vì | Nhà vua đốt hương khấn rằng mình là người ít đức, không dám cậy binh uy mà đánh bừa, vì Diễn Châu làm điều tàn ngược nên buộc phải đánh. |
| 18082 | Những năm trị vì | Ông xin rằng nếu lỡ giết oan người hiền thì trời cứ trách riêng mình, và người ta kể rằng khấn xong gió sấm đều yên lặng. |
| 18083 | Những năm trị vì | Năm một nghìn không trăm mười ba ông định ra các thứ thuế trong nước, chia làm sáu loại, rồi năm sau quân Nam Chiếu tràn vào cướp ở phía bắc. |
| 18084 | Những năm trị vì | Nhà vua sai Dực Thánh Vương đem quân đánh thắng lớn ở bến Kim Hoa, bắt được rất nhiều quân và ngựa. |
| 18085 | Những năm trị vì | Ông cho đem một trăm con ngựa bắt được sang biếu nhà Tống, và vua Tống sai quan đón tiếp sứ giả suốt dọc đường, rồi ban thưởng mũ, đai, tiền bạc. |
| 18086 | Những năm trị vì | Bên cạnh việc quân, nhà vua dốc sức cho Phật giáo, cho xây nhiều chùa, đúc chuông, chép kinh Tam tạng, và cho hơn một nghìn người ở kinh đô đi tu. |
| 18087 | Những năm trị vì | Sử gia Lê Văn Hưu chê rằng tông miếu chưa dựng mà đã vội xây tám ngôi chùa, rồi trách việc ấy tốn của dân. |
| 18088 | Những năm trị vì | Chuyện ấy cũng dễ hiểu, vì ông từng lớn lên bên nhà thiền sư và suốt thời trị vì vẫn dành cho đạo Phật sự coi trọng ấy. |
| 18089 | Những năm trị vì | Năm một nghìn không trăm mười lăm Đào Cam Mộc, người từng khuyên ông nhận ngôi, qua đời, và nhà vua tặng ông ta chức Thái sư á vương. |
| 18090 | Điện Long An | Mười tám năm đã trôi qua từ ngày dời đô, và kinh thành Thăng Long đã có cung điện, có thành, có bốn cửa mở ra bốn phương. |
| 18091 | Điện Long An | Thái tử Lý Phật Mã đã trưởng thành và từng thay cha cầm quân đi đánh các nơi. Mùa xuân năm một nghìn không trăm hai mươi tám, nhà vua không khỏe. |
| 18092 | Điện Long An | Rồi đến ngày mồng một tháng ba âm lịch, khi trời có nhật thực, và hai ngày sau nhà vua mất ngay tại điện Long An do chính ông dựng. |
| 18093 | Điện Long An | Ông thọ năm mươi lăm tuổi theo cách tính của người xưa, tức là hơn năm mươi bốn tuổi tròn, ở ngôi mười tám năm và được an táng ở Thọ Lăng. |
| 18094 | Điện Long An | Người xưa đánh giá ông là người khoan thứ nhân từ, hòa nhã, có lượng của bậc đế vương. |
| 18095 | Điện Long An | Nhưng người xưa cũng trách rằng ông chưa làm sáng tỏ đạo học, lại ưa tin điềm lạ. |
| 18096 | Cánh cửa Quảng Phúc | Nhà Lý chưa kịp lo xong tang thì mối nguy đã nổ ra ngay trong hoàng tộc, đúng tại cánh cửa mà ta đã gặp lúc đầu. |
| 18097 | Cánh cửa Quảng Phúc | Ba người em của thái tử Lý Phật Mã là Đông Chinh Vương, Dực Thánh Vương và Vũ Đức Vương đã đem quân phủ mình vào ẩn sẵn trong thành. |
| 18098 | Cánh cửa Quảng Phúc | Đông Chinh Vương nấp ở Long Thành, còn Dực Thánh Vương và Vũ Đức Vương nấp ở cửa Quảng Phúc, chờ thái tử đi qua để đánh úp. |
| 18099 | Cánh cửa Quảng Phúc | Một lát sau thái tử đi vào từ cửa Tường Phù, đến điện Càn Nguyên thì nhận ra có biến. |
| 18100 | Cánh cửa Quảng Phúc | Ông cho đóng hết các cửa điện và sai lính canh trong cung phòng giữ. |
| 18101 | Cánh cửa Quảng Phúc | Ông nói với những người xung quanh rằng mình không hề phụ bạc anh em, mà ba vương lại quên lời cha dặn, định chiếm ngôi báu. |
| 18102 | Cánh cửa Quảng Phúc | Viên nội thị Lý Nhân Nghĩa xin cho đánh một trận để quyết thua được, nhưng thái tử chưa chịu. |
| 18103 | Cánh cửa Quảng Phúc | Thái tử im lặng hồi lâu rồi nói rằng vua cha vừa mất chưa kịp quàn mà anh em đã giết nhau thì muôn đời sẽ chê cười. |
| 18104 | Cánh cửa Quảng Phúc | Ông muốn che giấu tội của ba vương để họ tự rút quân, giữ trọn tình ruột thịt, nhưng quân của ba vương lại bao vây càng gấp. |
| 18105 | Cánh cửa Quảng Phúc | Lúc ấy thái tử nói rằng nếu thế thì ông chỉ còn biết mặc áo tang đứng hầu vua cha, còn việc còn lại giao cho các quan. |
| 18106 | Cánh cửa Quảng Phúc | Lý Nhân Nghĩa cùng các quan lạy hai lạy, nói rằng chết vì vua gặp nạn là bổn phận của họ, rồi ra lệnh mở cửa cho vệ sĩ xông ra đánh. |
| 18107 | Cánh cửa Quảng Phúc | Vệ sĩ trong cung ai cũng vui lòng xông pha, mỗi người địch với trăm người, nhưng hai bên giao chiến mãi chưa phân thắng bại. |
| 18108 | Cánh cửa Quảng Phúc | Bỗng tướng Lê Phụng Hiểu tức giận rút gươm, chạy thẳng tới cửa Quảng Phúc. |
| 18109 | Cánh cửa Quảng Phúc | Ông hô lớn rằng Vũ Đức Vương nhòm ngó ngôi báu, trên quên ơn vua cha, dưới trái nghĩa tôi con. |
| 18110 | Cánh cửa Quảng Phúc | Rồi ông xông thẳng tới chỗ ngựa của Vũ Đức Vương, vương quay ngựa tránh nhưng ngựa quỵ xuống, và Vũ Đức Vương bị Lê Phụng Hiểu bắt giết. |
| 18111 | Cánh cửa Quảng Phúc | Quân của ba vương thua chạy, và chỉ có hai vương Đông Chinh cùng Dực Thánh thoát được. |
| 18112 | Cánh cửa Quảng Phúc | Lê Phụng Hiểu trở về, mặc nguyên áo trận vào báo tin thắng ngay trước linh cữu của vua cha, rồi sang điện Càn Nguyên báo cho thái tử. |
| 18113 | Cánh cửa Quảng Phúc | Thái tử khen rằng ông còn trung dũng hơn cả Uất Trì Kính Đức, vị công thần nổi tiếng của nhà Đường, rồi lên ngôi, và đó là vua Lý Thái Tông. |
| 18114 | Kết | Cửa Tường Phù, cửa Quảng Phúc, điện Càn Nguyên và điện Long An, những nơi diễn ra ngày hôm ấy, đều do Lý Công Uẩn dựng năm một nghìn không trăm mười. |
| 18115 | Kết | Khi dựng chúng, ông đã viết trong bản chiếu rằng nhà Đinh và nhà Tiền Lê vận nước ngắn ngủi vì cứ yên đóng đô một chỗ. |
| 18116 | Kết | Không ai biết ông có nghĩ trước đến ngày năm một nghìn không trăm hai mươi tám ấy hay không. |
| 18117 | Kết | Nhưng đến ngày ấy kinh đô ông dựng vẫn đứng vững, và ngôi vua vẫn truyền được cho con. |
| 18118 | Kết | Nhà Lý giữ ngôi hơn hai trăm năm, còn cái tên Thăng Long mà ông đặt cho nơi con thuyền dừng lại cũng sống lâu hơn cả triều đại của ông. |
| 18119 | Kết | Mười tám năm trước ông chỉ hỏi bầy tôi một câu, rằng nhân đất tốt ấy mà định nơi ở thì các khanh nghĩ thế nào. |
| 18120 | Kết | Và ở cánh cửa Quảng Phúc, cánh cửa phía tây ông dựng, một cuộc tranh ngôi trong chính con cháu ông đã kết thúc. |
