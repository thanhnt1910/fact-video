# Kịch bản bản đồ: Lý Thường Kiệt, người đánh trước để giữ nước (để chủ kênh duyệt)

Mã `lt1`, **96 đoạn (19001–19096)**, khoảng 2030 chữ (ước tính từ bản 100 đoạn 2129 chữ sau khi bỏ bốn đoạn, chưa chạy lại bộ kiểm), khoảng 11,3 phút ở 3 chữ/giây; đọc thực tế khoảng 3,3 chữ/giây thì khoảng 10,3 phút, **chỉ vừa đủ sàn 10 phút**. 13 chương. Bộ kiểm `kiem_kich_ban.py lt1` chưa chạy lại sau các lần sửa 29/10 (bản trước: 0 lỗi, 3 cảnh báo nhẹ); đếm tay hiện có hai đoạn dài hơn 32 chữ: 19024 (34 chữ, câu do chủ kênh viết) và có thể cần kiểm lại 19027. File giọng: `ke-hoach/thu-giong-hai/lt1_full.json` (tone `story` toàn bộ, như ly1).

**Bản sửa 29/10 (21:10): bỏ cảnh vector, thay toàn bộ bằng ảnh chibi** vẽ bằng FLUX.1 schnell + LoRA `Muapi/chibi-characters-flux-dev` trên Kaggle (quy tắc ở `CLAUDE.md`, mục "Nhân vật chibi", và quy tắc vẽ ảnh ở `quy-tac/tam-quoc.md`). Cột "Cảnh" của 64 đoạn đổi từ "vector:" sang "chibi:", 32 đoạn bản đồ giữ nguyên (số đoạn đã giảm sau lần sửa lời kể bên dưới).

**Sửa lời kể 29/10 (21:30, theo yêu cầu của chủ kênh):** bỏ chữ "khai khẩn" (đổi thành "vỡ đất hoang, lập làng"); viết đủ tên địa danh ("Khâm Châu và Liêm Châu", "Ung Châu, Khâm Châu và Liêm Châu"); bỏ hẳn sử thần Ngô Sĩ Liên và câu lời bàn của ông (cũ 19054); bỏ lời dẫn "Sử Đại Việt chép rằng" ở ba đoạn (cũ 19030, 19049, 19056); lược phần giải thích quanh bài thơ (cũ 19065, 19068, 19069); "xua quân" đổi thành "đem quân" (cũ 19013 và 19091). **Lần sửa 21:45:** bỏ các lời dẫn nguồn "Sử cũ", "Sử chép rằng", "Theo sử Đại Việt" ở 19006, 19016, 19062, 19038 (chữ "theo sử Đại Việt" của số quân mười vạn chuyển sang lớp chữ video); đổi cách mở câu ở 19065 và 19085 (không còn hai đoạn liền cùng chữ đầu); bỏ nhận xét "bi thảm nhất" ở 19051, bỏ câu tóm tắt cuối chương ở 19074, và kết chương 19037 bằng việc sắp xảy ra. Bốn đoạn bị bỏ nên **các đoạn sau 19053 đã đánh số lại** (cũ 19055 thành 19054, cũ 19100 thành 19096).

**Nguồn chính:** toàn văn Đại Việt sử ký toàn thư (`ke-hoach/nguon/dai-viet-su-ky-toan-thu.txt`, quyển III, kỷ nhà Lý: năm 1069, 1072 đến 1084, 1101 đến 1105, kể cả chú thích của bản dịch dẫn Khâm định Việt sử thông giám cương mục). Đối chiếu thêm: Cương mục (đoạn dẫn trên trang Mộc bản triều Nguyễn), Việt sử lược của Trần Trọng Kim (giảng hòa, quân Tống chết quá nửa), tổng quan tiếng Anh về cuộc chiến Tống – Đại Việt (chỉ để biết chỗ các nguồn lệch nhau, KHÔNG dùng làm gốc cho lời kể).

## Ý tưởng chính (phần sáng tạo, chủ kênh duyệt)

- **Mở đầu bằng cảnh có thật trong chính video:** năm 1075 một đạo quân Đại Việt vượt biên giới, vây thành Ung Châu hơn 40 ngày và chất bao đất để trèo lên tường (Toàn thư chép đủ). Hook chỉ nêu việc lạ, không lộ kết cục (thành thất thủ, Tô Giám tự thiêu), rồi hỏi: vì sao đánh trước, và người dẫn quân là ai. Cảnh này được kể đầy đủ ở chương "Bốn mươi ngày bên tường thành".
- **Chuyển sang quá khứ bằng câu hỏi "người ấy là ai"**, không dùng cầu nối "để hiểu điều này, ta phải bắt đầu từ...".
- **Thân bài đúng thứ tự thời gian** (người hầu cận trong cung, 1069 đánh Chiêm Thành, 1072 vua nhỏ lên ngôi, 1075 tin từ phía bắc, Khâm Liêm Ung, 1076 đến 1077 sông Như Nguyệt, sau chiến tranh 1078 đến 1084, những năm cuối đến 1105). Mỗi chương gắn với một nơi: Thăng Long, Thanh Hóa – Nghệ An, Chiêm Thành, Quế Châu, Ung Châu, sông Cầu.
- **Kết quay lại Ung Châu và bài thơ bên sông**, không bình luận của mình, không có lời bàn của sử gia hay sử thần.
- **Bài thơ "Nam quốc sơn hà" chỉ được kể là chuyện người đời truyền lại** (đúng như Toàn thư chép trong ngoặc), không kể như sự kiện chắc chắn; lời kể mở bằng "Theo truyền thuyết dân gian" (các đoạn giải thích quanh bài thơ đã lược ở lần sửa 21:30).
- **Cảnh ở Ung Châu nói thẳng đây là phần nặng nề**, không tán dương số người chết và nói rõ con số là do sử Đại Việt chép, các nguồn khác khác đi.
- **Giọng hài:** chỉ nhắm vào tình huống và phía quân xâm lược: câu thơ người Tống tự chê "vì tham voi Giao Chỉ mà mất vàng Quảng Nguyên" (Toàn thư chép nguyên văn). Khung đùa tối đa hai khung mỗi chương, chỉ ở phía nhà Tống; tuyệt đối không đùa về Lý Thường Kiệt, vua Lý, Ỷ Lan.
- **Không có "tập sau"**; video trọn gói, kết ở kết cục của câu chuyện.

## Quyết định của chủ kênh (29/10/2026)

- **Lấy theo bản chủ kênh đã sửa lời** (file đính kèm ngày 29/10): giữ chương mở đầu "Thành bị vây" (hook bằng cảnh vây Ung Châu) (lời bàn của sử thần Ngô Sĩ Liên ở chương 7 đã được chủ kênh bỏ ở lần sửa 21:30). Giữ nguyên câu về số người chết ở Ung Châu. Lời kết (chương 13) theo đúng bản chủ kênh viết.
- Tôi chỉ sửa bốn chỗ nhỏ để qua bộ kiểm giọng đọc: bỏ hai chấm ở hai đoạn, đổi "đất Tống" thành "lãnh thổ nhà Tống" (đoạn 19011), rút ngắn hai đoạn dài hơn 32 chữ (19024, 19050).
- Cảnh vector tăng lên khoảng 67 phần trăm (đã thay bằng chibi ở bản sửa 21:10 cùng ngày). Giọng luôn Sadaltager, đọc từng đoạn một.

## Chương, độ chắc và nguồn

| Chương | Đoạn | Nội dung | Độ chắc và nguồn |
|---|---|---|---|
| Thành bị vây | 19001–19004 | Hook: vượt biên giới, vây thành 40 ngày, bao đất | khớp Toàn thư (Bản kỷ III, năm Ất Mão 1075) |
| Người hầu cận trong cung | 19005–19011 | Thái Hòa, hoàng môn chi hậu, nội thị sảnh đô tri, thái bảo, tiết việt, Thanh Hóa, Nghệ An | khớp phần chép sau khi ông mất (Toàn thư, Ất Dậu 1105); **năm sinh bỏ khỏi lời kể** (các sách ghi 1019 hoặc 1030, chưa chắc) |
| Mặt trận phía nam | 19012–19022 | 1069 vua thân chinh, tiên phong, Cư Liên, Ỷ Lan, Chế Củ và 5 vạn dân, dâng ba châu, phụ quốc thái phó | khớp Toàn thư (Kỷ Dậu 1069 và đoạn chép sau khi ông mất) |
| Một đứa trẻ bảy tuổi | 19023–19028 | 1072 Nhân Tông 7 tuổi, Ỷ Lan, thái hậu họ Dương, Lý Đạo Thành; 1075 đánh Chiêm không thắng, vẽ địa đồ ba châu, thái úy | khớp Toàn thư (Nhâm Tý 1072, Ất Mão 1075 mùa thu) |
| Tin từ phía bắc | 19029–19037 | Vương An Thạch, Thẩm Khởi, Lưu Di ở Quế Châu, đóng thuyền, cấm buôn bán, Lý Thường Kiệt và Tông Đản; lời tuyên bố phép thanh miêu | khớp Toàn thư; lý do thật của chiến tranh ghi rõ là **lời sử Đại Việt chép**, người nay còn bàn |
| Đi trước một bước | 19038–19044 | Hai đạo thủy bộ hơn 10 vạn quân, Khâm Liêm, Ung, cửa ải Côn Lôn, Trương Thủ Tiết bị chém | khớp Toàn thư; **số quân 10 vạn là số của Toàn thư**; Cương mục không chép số này |
| Bốn mươi ngày bên tường thành | 19045–19053 | Tô Giám, vây trên 40 ngày, bao đất, thành hạ, 36 người nhà, 5 vạn 8 nghìn, 10 vạn, bắt sống người ba châu, thụy Trung Dũng | khớp Toàn thư; **con số người chết là của sử Đại Việt, nguồn Trung Hoa chép khác**, lời kể đã nói rõ |
| Quân Tống kéo xuống | 19054–19058 | Quách Quỳ, Triệu Tiết, chín tướng, Chiêm Thành, Chân Lạp, cuối năm 1076 | khớp Toàn thư (nhưng Toàn thư ghi nhầm tháng 3 năm 1076, Cương mục sửa; lời kể chỉ nói "cuối năm") |
| Phòng tuyến sông Như Nguyệt | 19059–19066 | Sông Cầu, hàng rào, quân Tống chết trên 1000, đền hai anh em họ Trương, bài thơ, Quách Quỳ lui và lấy Quảng Nguyên | khớp Toàn thư; hàng rào và bài thơ là **chuyện người đời truyền** (Toàn thư ghi trong ngoặc) |
| Cuộc giằng co | 19067–19074 | Quân Tống không vượt sông, bệnh tật, hơn 8 vạn chết quá nửa, xin hòa, giữ lại 4 châu, khoảng năm 1077 | Việt sử lược và Cương mục; **số 8 vạn và "quá nửa" chỉ là tài liệu thứ cấp, lời kể ghi "có sách chép"**; tháng ngừng chiến không rõ |
| Sau chiến tranh | 19075–19082 | 1078 Đào Tống Nguyên cống 5 voi, 1079 trả Thuận Châu, 1081 trả tù binh, 1084 Lê Văn Thịnh, 6 huyện 3 động, câu thơ người Tống | khớp Toàn thư (các năm Mậu Ngọ, Kỷ Mùi, Tân Dậu, Giáp Tý) |
| Những năm cuối | 19083–19091 | Thái úy, 1101 kiêm chức, 1103 Lý Giác, 1104 Chế Ma Na, mất tháng 6 năm 1105, Việt quốc công, Lý Thường Hiến | khớp Toàn thư (các năm Tân Tỵ, Quý Mùi, Giáp Thân, Ất Dậu) |
| Trở lại bên tường thành | 19092–19096 | Ba đời vua, hai chấm Ung Châu và Như Nguyệt, bài thơ | nối các chương trên; "khoảng một năm" giữa hai trận là tính gần đúng |

## Chi tiết đã bỏ khỏi lời kể (nghi vấn hoặc chỉ có ở nguồn thứ cấp)

- Năm sinh 1019 (hoặc 1030): sử cũ không ghi, các sách khác nhau.
- Họ gốc Ngô hay Quách, chuyện thời trẻ theo Nhữ Bá Sĩ (đời Nguyễn): nguồn muộn, không dùng.
- "Là hoạn quan": Toàn thư không chép, chỉ chép chức hoàng môn chi hậu; không đưa vào.
- Thời điểm Khâm, Liêm, Ung: Toàn thư xếp vào tháng 2 năm 1075 và còn chép Khâm, Liêm hai lần (1075 và 1077); Cương mục sửa lại theo Cương mục tục biên là mùa đông 1075, Ung Châu vỡ tháng giêng 1076, chỉ một lần. Lời kể chỉ nói "mùa đông năm 1075".
- Triệu Tiết "sang xâm lấn tháng 12 năm 1077": Cương mục cho là chép nhầm (chỉ là phó tướng của Quách Quỳ năm 1076). Bỏ.
- Chi tiết kỹ thuật nguồn thứ cấp (máy bắn đá, cọc dưới lòng sông, trận Kháo Túc, hai hoàng tử chết đuối, số quân Tống 5 vạn lính 10 vạn phu): chưa kiểm được từ nguồn gốc nên chưa đưa. Nếu chủ kênh muốn thêm cảnh trận chiến thì cần tìm nguồn trước.
- Số quân Tống 8 vạn: chỉ ở dạng "có sách chép", không dùng làm số chắc.
- Bài thơ có nhiều dị bản; lời kể dùng đúng nghĩa của bản Toàn thư.
- Vợ con, "phải tự xử tội", các chuyện dân gian về đền thờ: bỏ.

## Cảnh bản đồ và cảnh chibi

Tổng 96 đoạn: **64 đoạn ảnh chibi** (cột "Cảnh" bắt đầu bằng "chibi") và **32 đoạn bản đồ** (giữ nguyên như bản trước; hướng bản đồ ở bản trước vẫn dùng: mở rộng phía bắc Quế Châu, Ung Châu, Khâm, Liêm, ải Côn Lôn, Quảng Nguyên, sông Cầu; phía nam Chiêm Thành, ba châu, Thanh Hóa, Nghệ An, Diễn Châu; mũi tên dày, hai đạo thủy bộ hai màu; số liệu chỉ hiện đúng lúc được nói, kèm nhãn "theo sử Đại Việt"). Ghi chú nhỏ (số liệu lệch, chuyện truyền lại) vẫn là khung chú thích trên bản đồ. Mỗi ảnh chibi chỉ dùng một lần (một ảnh mỗi đoạn, khóa ảnh = số đoạn).

### Cách vẽ (theo quy tắc đã có)

- Mô hình: FLUX.1 schnell (GGUF Q8) + LoRA `Muapi/chibi-characters-flux-dev`, câu mở đầu prompt `A vibrant chibi-style illustration`, vẽ trên Kaggle, không dùng Gemini. Mỗi cảnh ghi **độ mạnh LoRA**: 1,0 cho cảnh một đến hai người, **0,6 cho cảnh nhiều người** (LoRA làm mặt hơi giống nhau, hạ độ mạnh rồi so sánh). Hạ độ mạnh vẫn làm mặt giống thì dùng phương án "không LoRA, chỉ viết chibi trong câu lệnh".
- Thứ tự prompt: cảnh, nhân vật (lấy nguyên mô tả ở bảng nhân vật bên dưới, tên viết tắt trong ngoặc vuông), hậu tố. Cảnh một người thêm "exactly ONE character only, no second figure, no crowd". Cảnh vật trống thêm "completely empty, absolutely no people". Mọi prompt thêm "single full-frame picture, no panels, no border, no text".
- **Quy tắc ảnh áp dụng:** không chữ (cờ, biển, giấy, bản đồ, cuộn tâu để trơn; **lời thơ và con số do lớp chữ của video hiện, không nằm trong ảnh**), không máu và không cảnh giết người (chiến tranh vẽ hai bên đối mặt, hàng quân, khói, thành bị vây; lính ở xa hoặc nhìn từ sau thì mặt đơn giản), mỗi người một khuôn mặt, tuổi, râu tóc và màu áo riêng, mỗi người tối đa một vũ khí và kiếm đeo luôn nằm trong bao, nền có chi tiết, đúng thời.
- **Đúng thời (cần chủ kênh duyệt):** Đại Việt thế kỷ 11 (nhà Lý): áo nâu hoặc chàm, mái ngói xám và mái tranh, cờ **đỏ trơn**; nhà Tống: áo quan rộng tay, mũ quan hai cánh, thành lũy mái nhiều tầng, cờ **xanh đậm trơn**; Chiêm Thành: cờ **cam trơn**. Cấm vật hiện đại (kính, nến cọc, ghế tựa, giấy hiện đại, bảng hiệu). Quy ước này mới, chưa có tệp trang phục như `TQn_trang_phuc.json`, nếu duyệt tôi sẽ tạo `lt1_trang_phuc.json` cho đủ nhân vật.
- **Soi ảnh bằng mắt ở cỡ lớn** trước khi dùng; ảnh lỗi vẽ lại hạt giống khác. Chỉ chạy workflow khi chủ kênh yêu cầu, một kernel Kaggle, không chạy song song.

### Bảng nhân vật chibi (mô tả cố định, dùng đúng chữ này trong mọi prompt)

| Mã | Nhân vật | Mô tả riêng (tuổi, râu tóc, áo) |
|---|---|---|
| LTK-T | Lý Thường Kiệt thuở hầu cận | young slim attendant, smooth face no beard, black hair in a topknot, plain black cap, dark blue court robe |
| LTK-G | Lý Thường Kiệt tướng và thái úy | dignified middle-aged general, short neat black beard, serious calm face, deep crimson robe over dark lamellar armor, sword always sheathed |
| LTK-L | Lý Thường Kiệt những năm cuối | dignified elderly man, white beard and thin white hair, same deep crimson robe, calm eyes |
| TT | vua Lý Thái Tông | elderly king, grey beard, golden yellow robe, small gold crown |
| TTG | vua Lý Thánh Tông | strong middle-aged king, thin black mustache no beard, golden yellow robe with dragon pattern, gold crown |
| NT | vua Lý Nhân Tông lúc bảy tuổi | tiny seven-year-old boy king, round face, oversized golden robe, small gold crown |
| YL | Nguyên phi Ỷ Lan | graceful woman, hair in a high bun with one jade pin, pale green silk dress |
| DTH | thái hậu họ Dương | older woman, stern face, grey-streaked bun, plum purple robe |
| LDT | thái sư Lý Đạo Thành | elderly scholar-official, long white beard, indigo robe, black official hat |
| CC | Chế Củ, vua Chiêm Thành | Champa king, thin mustache, tall tiered golden crown, orange and white wrapped garments |
| TD | Tông Đản | broad-shouldered general, thick black beard, olive brown armor, helmet with a short red plume |
| TG | Tô Giám | Song official, middle-aged, thin grey beard, dark teal official robe with wide sleeves, black two-winged official hat |
| VAT | Vương An Thạch | Song chancellor, long thin face, thin grey beard, purple official robe, black two-winged official hat |
| TK | Thẩm Khởi | tall thin Song official, clean shaven, brown robe, black official hat |
| LD | Lưu Di | short stout Song official, round black beard, green robe, black official hat |
| TTT | Trương Thủ Tiết | Song general, heavy build, black beard, red-brown armor, helmet with long red tassel |
| QQ | Quách Quỳ | big strong Song commander, white-streaked beard, dark steel armor, tall helmet |
| TT2 | Triệu Tiết | younger Song general, thin mustache, black armor, plain helmet |
| DTN | Đào Tống Nguyên | Đại Việt envoy, goatee, mid-brown robe, round hat |
| LVT | Lê Văn Thịnh | scholar-official, small mustache, blue-grey robe, black official hat |
| LG | Lý Giác (kẻ nổi dậy) | rough sturdy man in plain brown peasant clothes, headband, no armor |
| LTH | Lý Thường Hiến | younger brother, smooth face with a light mustache, dark green robe |

Vua Tống (không rõ tên trong lời kể): middle-aged emperor, thin mustache, dark gold robe, flat-topped crown with hanging beads; dùng chung ở mọi cảnh, không gọi tên. Lính Đại Việt: áo nâu da, nón tròn, cờ đỏ trơn; lính Tống: áo giáp xám, mũ có tua, cờ xanh đậm trơn. Đề xuất: prompt chỉ mô tả theo hình dáng, không đưa tên người và địa danh vào (mô hình không biết các nhân vật này, tên chỉ làm prompt dài thêm).

### Điểm cần lưu ý về giọng điệu (cần chủ kênh quyết)

- **Phong cách chibi dễ gây cảm giác đùa với các anh hùng** (quy tắc "không đùa cợt anh hùng dân tộc"). Biện pháp: Lý Thường Kiệt, vua Lý, Ỷ Lan luôn vẽ **nghiêm trang, thần thái trầm tĩnh, không nhăn nhó, không lè lưỡi, không biểu cảm hài**; khung đùa chỉ rơi vào quân Tống (đúng quy tắc cũ).
- **Chương Ung Châu (19045–19054) rất nặng nề** (nói thẳng số người chết). Cảnh được vẽ gần như không có người: khói, tường thành, đường vắng, xe đổ, một mình Tô Giám nghiêm nghị, và hạ chibi xuống mức dễ thương thấp (tông màu xám cam, không biểu cảm to). Nếu thử ra ảnh quá "dễ thương", đề xuất chuyển các cảnh này sang bản đồ hoặc để chủ kênh duyệt riêng.

## Lời kể (mã `lt1`, 19001 trở đi)

| n | Chương | Lời kể | Cảnh |
|---|---|---|---|
| 19001 | Thành bị vây | Mùa đông năm một nghìn không trăm bảy mươi lăm, một đạo quân vượt biên giới đi về phía bắc, tiến thẳng vào lãnh thổ nhà Tống. | bản đồ Đại Việt và nhà Tống, mũi tên đỏ vượt biên giới |
| 19002 | Thành bị vây | Họ vây hãm một tòa thành hơn bốn mươi ngày, rồi chất bao đất cao dần để tràn lên mặt thành. | chibi (LoRA 0,6): Toàn cảnh thành Ung Châu tường đá xám cao, cờ Tống xanh đậm trơn. Dưới chân tường hàng lính Đại Việt áo nâu, cờ đỏ trơn, khiêng bao đất xếp dần thành dốc. Lính nhìn từ xa hoặc từ sau lưng, mặt đơn giản. |
| 19003 | Thành bị vây | Một quốc gia nhỏ bé chủ động tấn công một đế chế khổng lồ phương Bắc là điều hiếm thấy trong lịch sử nước ta. | chibi (LoRA 1,0): Hai bờ cõi cạnh nhau: bên trái vùng đồi nhỏ có làng mái tranh và cờ đỏ trơn, bên phải thành lũy đồ sộ nhiều tầng mái, cờ xanh đậm trơn, gió thổi cờ. Mỗi bên một lính gác nhỏ, hai người khác mặt. |
| 19004 | Thành bị vây | Vậy vì sao quân Đại Việt lại đi trước một bước? Và người dẫn dắt đạo quân ấy là ai? | chibi (LoRA 1,0): [LTK-G] một mình đứng trên tường thành Thăng Long nhìn về phía bắc, gió thổi vạt áo. Đúng một người, không ai khác. |
| 19005 | Người hầu cận trong cung | Người ấy là Lý Thường Kiệt, quê ở phường Thái Hòa, kinh thành Thăng Long, sinh ra trong một gia tộc nhiều đời làm quan. | Thăng Long, ghim phường Thái Hòa |
| 19006 | Người hầu cận trong cung | Năm sinh của ông chưa ai biết chắc, nên các tài liệu ngày nay mỗi nơi ghi một khác. | chữ trên bản đồ: năm sinh chưa rõ |
| 19007 | Người hầu cận trong cung | Thuở thiếu thời, nhờ dung mạo khôi ngô, ông được tuyển vào cung giữ chức hoàng môn chi hậu, kề cận phục vụ nhà vua. | chibi (LoRA 1,0): Sân cung. [LTK-T] đứng hầu bên vua [TT] đang ngồi, hai người, nền cung điện mái ngói, cột đỏ. |
| 19008 | Người hầu cận trong cung | Ông theo hầu vua Lý Thái Tông, rồi dần được thăng lên chức nội thị sảnh đô tri, nắm quyền cai quản công việc trong cung. | chibi (LoRA 1,0): [LTK-T] đã lớn hơn, bước lên bậc thềm cung, áo xanh sẫm có đai và mũ cao hơn trước. Một mình, nền cung điện. |
| 19009 | Người hầu cận trong cung | Dưới thời vua Lý Thánh Tông, ông được phong làm thái bảo và được trao cờ tiết để thay mặt vua đi tuần thú, dò xét dân tình. | chibi (LoRA 1,0): [LTK-T] cầm cờ tiết (cán dài, tua trơn, không chữ) cưỡi ngựa ra cổng thành, hai lính hộ tống phía sau khác nhau. |
| 19010 | Người hầu cận trong cung | Ông đi qua hai vùng đất phía nam là Thanh Hóa và Nghệ An, hỏi han đời sống con dân rồi mới hồi triều. | chibi (LoRA 0,6): [LTK-T] cùng hai quan tùy tùng (một người gầy râu dài, một người thấp tròn không râu) đi qua làng Thanh Hóa, dân làng đứng đón hai bên đường, nhà tranh và ruộng. |
| 19011 | Người hầu cận trong cung | Nhưng hành trình của ông đã bắt đầu từ nhiều năm trước đó, rất lâu trước khi ông trở thành vị tướng tấn công sang lãnh thổ nhà Tống. | trở lại Thăng Long, lùi thời gian |
| 19012 | Mặt trận phía nam | Đại Việt thời bấy giờ có hai đường biên giới cần canh giữ, phía bắc giáp nhà Tống và phía nam giáp nước Chiêm Thành. | bản đồ: hai biên giới tô màu |
| 19013 | Mặt trận phía nam | Chiêm Thành nhiều lần đem quân quấy rối bờ cõi, khiến vua Lý Thánh Tông quyết định thân chinh đi đánh dẹp. | mũi tên Chiêm Thành đỏ lên biên giới |
| 19014 | Mặt trận phía nam | Mùa xuân, tháng hai năm một nghìn không trăm sáu mươi chín, nhà vua dẫn đại quân tiến vào đất Chiêm. | chibi (LoRA 0,6): Hàng quân Đại Việt đi xuống phía nam, nhìn từ sau lưng và từ xa, cờ đỏ trơn bay, núi và đường đất. |
| 19015 | Mặt trận phía nam | Lý Thường Kiệt đi trong đạo quân ấy và giữ vai trò tiên phong, mở đường xuyên phá đội hình địch. | chibi (LoRA 1,0): [LTK-G] cưỡi ngựa đi đầu đoàn quân, kiếm nằm trong bao bên hông, quân lính phía sau nhỏ và xa. |
| 19016 | Mặt trận phía nam | Trận đầu gian nan: nhà vua đánh mãi không hạ được địch, bèn hạ lệnh lui binh. | chibi (LoRA 1,0): Trong lều ở Cư Liên, vua [TTG] đứng nhìn tấm bản đồ trải trên bàn, bên ngoài vài lính ngồi nghỉ cạnh lều. Bản đồ chỉ có nét vẽ, không chữ. |
| 19017 | Mặt trận phía nam | Về đến châu Cư Liên, vua nghe tin Nguyên phi Ỷ Lan ở lại kinh đô điều hành quốc sự rất khéo léo, muôn dân yên ấm. | chibi (LoRA 1,0): Trong cung, [YL] phát gạo cho dân, dân quỳ gối chắp tay cảm tạ; thúng gạo, sân cung. |
| 19018 | Mặt trận phía nam | Nhà vua than rằng, một người phụ nữ còn làm được như thế, mình là bậc nam nhi lẽ nào lại bỏ dở việc lớn. | chibi (LoRA 1,0): Vua [TTG] đứng trước đoàn quân, nhìn về phía nam, nét mặt quyết tâm; quân lính phía sau nhìn từ sau lưng. |
| 19019 | Mặt trận phía nam | Vua lập tức cho quân quay lại và giành đại thắng, bắt sống vua Chiêm Thành là Chế Củ cùng năm vạn người. | chibi (LoRA 0,6): Hai đoàn quân giáp mặt giữa đồng, bụi mù cuộn lên, bên trái cờ đỏ trơn Đại Việt, bên phải cờ cam trơn Chiêm Thành. Lính ở xa, mặt đơn giản, không máu, không ai ngã. |
| 19020 | Mặt trận phía nam | Tháng bảy năm ấy, đoàn quân khải hoàn về kinh, dâng tù binh lên Thái Miếu để cáo công với tổ tiên nhà Lý. | chibi (LoRA 1,0): Sân Thái Miếu, tù binh đứng cúi đầu thành hàng trước đền, [CC] đứng đầu hàng; không xích nặng, không cảnh hành hạ; vua [TTG] đứng trên thềm. |
| 19021 | Mặt trận phía nam | Để chuộc mạng, Chế Củ xin dâng ba châu Địa Lý, Ma Linh và Bố Chính. Nhà vua ưng thuận và tha cho ông ta về nước. | bản đồ: ba châu đổi màu sang Đại Việt |
| 19022 | Mặt trận phía nam | Nhờ lập công lớn ở vị trí tiên phong, Lý Thường Kiệt được thăng làm phụ quốc thái phó, dự bàn quốc sự trong triều. | chibi (LoRA 0,6): Trong điện, [LTK-G] quỳ nhận lễ phong chức từ vua [TTG], hai quan đứng hầu hai bên, khác tuổi khác râu. |
| 19023 | Một đứa trẻ bảy tuổi | Năm một nghìn không trăm bảy mươi hai, vua Lý Thánh Tông băng hà, thái tử Càn Đức lên ngôi, tức là vua Lý Nhân Tông. | chibi (LoRA 0,6): Tang lễ Thánh Tông: đoàn người áo trắng đi sau linh xa trong sân cung, nhìn từ xa, không thấy rõ mặt. |
| 19024 | Một đứa trẻ bảy tuổi | Vua mới lên bảy, chưa tự lo việc nước. Vì thế mẹ vua Ỷ Lan cùng thái hậu họ Dương và thái sư Lý Đạo Thành đứng sau hỗ trợ, lo việc chính sự. | chibi (LoRA 1,0): Ngai vàng lớn có bé [NT] bảy tuổi ngồi nhỏ xíu, sau tấm rèm hiện bóng hai bà [DTH] và [YL]; [LDT] đứng bên cạnh ngai. |
| 19025 | Một đứa trẻ bảy tuổi | Lúc ấy người ngồi trên ngai vàng còn là một cậu bé, nên quyền hành trong triều được chia cho nhiều phe cùng nắm giữ. | chibi (LoRA 0,6): Các quan chia ba nhóm áo ba màu khác nhau (xanh lam, nâu, lục) đứng quanh ngai nhỏ có bé [NT] ngồi giữa; mỗi người một tuổi một râu khác nhau. |
| 19026 | Một đứa trẻ bảy tuổi | Năm một nghìn không trăm bảy mươi lăm, Lý Thường Kiệt lãnh mệnh đi đánh Chiêm Thành nhưng không phân thắng bại. | mũi tên xuống phía nam, dừng lại |
| 19027 | Một đứa trẻ bảy tuổi | Ông vẽ lại địa đồ ba châu Bố Chính, Địa Lý và Ma Linh rồi rút về, đổi tên hai châu và chiêu mộ dân đến vỡ đất hoang, lập làng. | bản đồ ba châu, tên mới hiện ra |
| 19028 | Một đứa trẻ bảy tuổi | Triều đình thăng ông làm thái úy, thống lĩnh toàn bộ binh quyền. Và ngay năm ấy, tin dữ báo về từ phương bắc. | chibi (LoRA 1,0): [LTK-G] quỳ một gối nhận ấn thái úy từ tay một quan lễ, nền điện có cột son. |
| 19029 | Tin từ phía bắc | Nhà Tống đương thời đang tiến hành cải cách, dưới sự điều hành của tể tướng Vương An Thạch. | chibi (LoRA 1,0): Triều đình Tống: vua Tống ngồi trên ngai, [VAT] đứng cầm cuộn tâu (cuộn để trơn, không chữ). |
| 19030 | Tin từ phía bắc | Vương An Thạch mật tấu với vua Tống rằng Đại Việt vừa bị Chiêm Thành đánh phá. | chibi (LoRA 1,0): Cận hai người: [VAT] cúi mình thì thầm tâu với vua Tống đang nghiêng đầu nghe, nền bình phong. |
| 19031 | Tin từ phía bắc | Ông ta khẳng định quân số Đại Việt còn lại chưa đầy một vạn, nhà Tống hoàn toàn có thể dùng mưu chiếm lấy. | chibi (LoRA 1,0): [VAT] đưa tay chỉ vào tấm bản đồ trên bàn, vua Tống đứng cạnh nhìn theo. Bản đồ chỉ có nét vẽ, không chữ. |
| 19032 | Tin từ phía bắc | Đó là lời chép trong sử Đại Việt, còn giới học giả ngày nay vẫn đang tranh luận về nguyên nhân thực sự của cuộc chiến. | ghi chú nhỏ: nguồn lệch nhau |
| 19033 | Tin từ phía bắc | Bất luận lý do là gì, vua Tống đã phái hai viên quan là Thẩm Khởi và Lưu Di đến vùng Quế Châu sát biên giới. | chibi (LoRA 1,0): Trước cổng thành Quế Châu, cờ Tống xanh đậm trơn, hai quan [TK] (cao gầy, áo nâu, không râu) và [LD] (thấp tròn, áo lục, râu tròn) đứng nhận lệnh. |
| 19034 | Tin từ phía bắc | Hai người này ra sức đóng chiến thuyền, luyện thủy quân, chiêu mộ dân miền núi, đồng thời cấm các châu huyện giao thương với Đại Việt. | chibi (LoRA 0,6): Xưởng đóng thuyền ven sông, thợ đóng thân thuyền gỗ, phía xa lính Tống tập trận hàng ngang; nhìn từ xa, mặt đơn giản. |
| 19035 | Tin từ phía bắc | Tình báo đưa về Thăng Long. Triều đình lập tức lệnh cho Lý Thường Kiệt và tướng Tông Đản dẫn quân xuất kích. | mũi tên tin Quế Châu về Thăng Long, hai tướng hiện |
| 19036 | Tin từ phía bắc | Nhà Lý tuyên bố rằng việc cất quân là để hỏi tội nhà Tống, vì phép thanh miêu của họ làm lầm than bá tánh Trung Hoa. | chibi (LoRA 0,6): Sứ giả Đại Việt mở cuộn giấy trơn (không chữ) đứng trước hàng quân cờ đỏ trơn, hàng quân nhìn từ sau lưng. |
| 19037 | Tin từ phía bắc | Phép thanh miêu là cho nông dân vay tiền khi lúa còn xanh, đến vụ gặt phải trả cả vốn lẫn lãi. Rồi hai đạo quân Đại Việt lên đường. | chibi (LoRA 1,0): Bên ruộng lúa còn xanh, một nông dân Tống nhận túi tiền từ một viên lại, hai người khác tuổi khác áo, tay cầm cuộn sổ trơn. |
| 19038 | Đi trước một bước | Binh lực chia thành hai đạo thủy bộ, tổng quân số lên tới hơn mười vạn người. | chibi (LoRA 0,6) (lớp chữ video: số quân theo sử Đại Việt): Hai đạo xuất quân: bên trái thuyền chiến xuôi sông, bên phải hàng quân bộ trên đường, cờ đỏ trơn; nhìn từ trên cao, lính nhỏ, mặt đơn giản. |
| 19039 | Đi trước một bước | Đạo thủy quân do Lý Thường Kiệt chỉ huy, đánh thốc vào hai châu ven biển là Khâm Châu và Liêm Châu. | mũi tên thủy Khâm Châu, Liêm Châu |
| 19040 | Đi trước một bước | Khâm Châu và Liêm Châu nhanh chóng thất thủ, quân Đại Việt bắt người dân tại đây mang về làm tù binh. | chibi (LoRA 0,6): Thuyền chiến Đại Việt cập bờ Khâm Châu, trên bờ một hàng dân thường bị dẫn đi, nhìn từ xa và từ sau lưng, không bạo lực. |
| 19041 | Đi trước một bước | Cùng lúc, tướng Tông Đản dẫn đạo quân bộ tiến thẳng về Ung Châu, tòa thành kiên cố nhất trong vùng. | mũi tên bộ Tông Đản đến Ung Châu |
| 19042 | Đi trước một bước | Quan trấn giữ Quảng Tây của nhà Tống là Trương Thủ Tiết vội vã dẫn viện binh đến cứu nguy cho Ung Châu. | chibi (LoRA 1,0): [TTT] mặc giáp đỏ nâu, mũ giáp có tua đỏ, cưỡi ngựa dẫn quân Tống đi cứu Ung Châu; quân phía sau nhỏ và xa. |
| 19043 | Đi trước một bước | Lý Thường Kiệt phục kích đánh chặn tại ải Côn Lôn, Trương Thủ Tiết bị chém chết ngay tại trận. | chibi (LoRA 0,6): Ải Côn Lôn giữa hai vách núi: bên trái quân Đại Việt cờ đỏ trơn mai phục sau đá, bên phải quân Tống cờ xanh trơn tiến vào, bụi mù cuộn lên, không cảnh chém giết, không máu. |
| 19044 | Đi trước một bước | Viện binh tan vỡ, Ung Châu giờ đây hoàn toàn bị cô lập, chỉ còn biết trông cậy vào lực lượng thủ thành. | chibi (LoRA 1,0): [TD] đứng trước vô số lều trại Đại Việt dựng quanh thành Ung Châu phía xa, cờ đỏ trơn. |
| 19045 | Bốn mươi ngày bên tường thành | Quan giữ thành Ung Châu là tri châu Tô Giám, một viên tướng thề chết không hàng. | chibi (LoRA 1,0): [TG] một mình đứng trên tường thành, hai tay chống lên lan can, mắt nhìn xuống, thần sắc kiên quyết. |
| 19046 | Bốn mươi ngày bên tường thành | Quân Đại Việt vây hãm suốt hơn bốn mươi ngày, nhưng tường thành quá cao không thể leo lên. | chibi (LoRA 1,0): Tường thành cao, dưới chân tường lều trại dựng dày thêm; trên trời mặt trời và mặt trăng nối nhau thành một dải biểu thị ngày tháng trôi qua. Không chữ, không lịch. |
| 19047 | Bốn mươi ngày bên tường thành | Cuối cùng, họ dùng chiến thuật chất bao đất thành một dốc lài, để quân sĩ có thể tràn thẳng lên mặt thành. | chibi (LoRA 1,0): Bao đất xếp chồng thành một dốc lài sát chân tường thành, vài lính khiêng bao, nhìn từ xa, mặt đơn giản. |
| 19048 | Bốn mươi ngày bên tường thành | Ung Châu thất thủ. Tô Giám bức tử ba mươi sáu người trong gia quyến, rồi châm lửa tự thiêu. | chibi (LoRA 1,0): Cổng thành Ung Châu, khói đen bốc lên từ bên trong, bầu trời xám cam. Không có người, không máu. |
| 19049 | Bốn mươi ngày bên tường thành | Trong thành không một ai chịu đầu hàng, và hơn năm vạn tám nghìn người đã tử trận tại đây. | chữ trên bản đồ: con số theo sử Đại Việt |
| 19050 | Bốn mươi ngày bên tường thành | Cộng cả Khâm Châu và Liêm Châu, thương vong lên tới hơn mười vạn. Đây là số liệu do sử Đại Việt chép, còn các nguồn khác có sự chênh lệch. | ghi chú nhỏ: số liệu lệch giữa các nguồn |
| 19051 | Bốn mươi ngày bên tường thành | Phần lớn những người ngã xuống ở Ung Châu không phải lính mà là dân thường trong thành. | chibi (LoRA 1,0): Con đường vắng trước thành, một chiếc xe đổ, khói cuộn ở phía xa, bầu trời ửng đỏ. Không có người. |
| 19052 | Bốn mươi ngày bên tường thành | Trận đánh kết thúc, quân Đại Việt bắt người dân ở ba châu đem về nước, rồi rút toàn bộ lực lượng khỏi vùng đất này. | chibi (LoRA 0,6): Một hàng dài dân thường đi về phía nam trên đường chiều tà, nhìn từ sau lưng, vài lính áp tải phía xa; không thấy mặt, không bạo lực. |
| 19053 | Bốn mươi ngày bên tường thành | Vua Tống truy tặng Tô Giám thụy hiệu Trung Dũng để ghi nhận sự trung thành gan dạ, đồng thời ban nhà cửa, ruộng đất cho con cháu ông. | chibi (LoRA 0,6): Gia quyến Tô Giám (một bà lão áo trắng và hai trẻ nhỏ khác tuổi) nhận lễ ban thưởng từ một quan Tống trước ngôi nhà ngói xám. |
| 19054 | Quân Tống kéo xuống | Nhưng nhà Tống không dễ dàng chấp nhận thất bại. Họ cử Quách Quỳ làm chiêu thảo sứ thống lĩnh đại quân, cùng phó tướng Triệu Tiết. | chibi (LoRA 1,0): Trong điện, hai tướng Tống [QQ] và [TT2] quỳ nhận lệnh trước vua Tống. |
| 19055 | Quân Tống kéo xuống | Nhà Tống đã huy động quân lực của chín tướng, liên kết cùng Chiêm Thành và Chân Lạp để kẹp đánh Đại Việt. | chibi (LoRA 1,0): Chín lá cờ tướng Tống màu khác nhau xếp hàng trên bãi tập, cờ để trơn; ở xa vài bóng tướng đứng nhỏ. |
| 19056 | Quân Tống kéo xuống | Chân Lạp là vương quốc nằm ở vùng lãnh thổ thuộc Campuchia ngày nay, còn Chiêm Thành án ngữ ngay phía nam Đại Việt. | bản đồ: chỉ Chân Lạp và Chiêm Thành |
| 19057 | Quân Tống kéo xuống | Cuối năm một nghìn không trăm bảy mươi sáu, đại quân Tống tràn xuống theo đường bộ, nhắm thẳng hướng Thăng Long. | chibi (LoRA 0,6): Quân Tống hành quân xuống đồng bằng, nhìn từ xa và từ sau lưng, cờ xanh đậm trơn, bụi đường. |
| 19058 | Quân Tống kéo xuống | Lý Thường Kiệt ý thức được rằng phải chặn đứng mũi tiến công này, và ông đã chọn một khúc sông hiểm yếu. | bản đồ: chỉ sông Cầu |
| 19059 | Phòng tuyến sông Như Nguyệt | Đó là sông Như Nguyệt, tức sông Cầu ngày nay, ranh giới tự nhiên vắt ngang con đường huyết mạch từ phía bắc về Thăng Long. | sông Cầu sáng lên, nhãn Như Nguyệt |
| 19060 | Phòng tuyến sông Như Nguyệt | Người đời truyền lại rằng Lý Thường Kiệt đã cho dựng một phòng tuyến hàng rào kiên cố dọc bờ sông để cản bước quân thù. | chibi (LoRA 1,0): Hàng rào tre cao dựng dọc bờ sông Cầu, hai bên là bãi cỏ; không người hoặc chỉ một lính gác nhỏ ở xa. |
| 19061 | Phòng tuyến sông Như Nguyệt | Áp sát bờ bắc, quân Tống phóng tầm mắt sang bờ bên kia, nhưng hoàn toàn bế tắc trong việc tìm đường vượt sông. | chibi (LoRA 0,6): Quân Tống đứng bờ bắc nhìn sang bờ bên kia dòng sông, nhìn từ sau lưng, cờ xanh trơn. |
| 19062 | Phòng tuyến sông Như Nguyệt | Quân Tống thử tiến công nhưng bị đánh bật, bỏ xác hơn một nghìn người. | chibi (LoRA 0,6): Quân Tống tiến đến bờ sông thì khựng lại trước hàng rào tre, giơ khiên đỡ, vài người lùi, không máu, không ai ngã. |
| 19063 | Phòng tuyến sông Như Nguyệt | Theo truyền thuyết dân gian, vào một đêm thanh vắng, quân sĩ bỗng nghe từ trong đền thờ hai anh em họ Trương vang lên tiếng ngâm một bài thơ. | chibi (LoRA 1,0): Đền nhỏ ven sông về đêm, mái ngói, đèn sáng le lói, trời đầy sao. Không có người. |
| 19064 | Phòng tuyến sông Như Nguyệt | Bài thơ khẳng định sông núi nước Nam là của vua nước Nam, điều ấy đã được định đoạt rõ ràng trong sách trời. | chibi (LoRA 1,0): Bầu trời đêm sao trên dòng sông, những dải sáng mềm như nét bút bay trên mặt nước. Không chữ trong ảnh; từng câu thơ do lớp chữ của video hiện ra. |
| 19065 | Phòng tuyến sông Như Nguyệt | Rồi bài thơ chất vấn lũ giặc cớ sao dám sang xâm phạm, và báo trước một kết cục thảm bại không thể tránh khỏi. | cuối bài thơ, ánh sáng nhẹ |
| 19066 | Phòng tuyến sông Như Nguyệt | Quách Quỳ buộc phải lui binh, còn châu Quảng Nguyên của Đại Việt thì rơi vào tay nhà Tống. | chibi (LoRA 0,6): Quân Tống rút về phía bắc, cờ xanh rũ xuống, bước chân mệt mỏi; nhìn từ xa và từ sau lưng. |
| 19067 | Cuộc giằng co | Cuộc chiến lâm vào thế giằng co. Quân Tống chôn chân ở bờ bắc, không thể tiến thêm được một bước. | bản đồ: hai bờ, đồng hồ ngày |
| 19068 | Cuộc giằng co | Vùng đồng bằng oi bức và ẩm thấp hơn hẳn quê nhà của lính Tống, khiến dịch bệnh bùng phát tàn phá doanh trại. | chibi (LoRA 0,6): Trong doanh trại Tống, vài lính nằm nghỉ trên chiếu, một người ngồi ôm đầu, trời xám; ba người khác tuổi khác râu, không máu. |
| 19069 | Cuộc giằng co | Vượt một chặng đường dài hiểm trở, để rồi đành bất lực đứng nhìn qua bờ kia dòng nước. | chibi (LoRA 1,0): Một lính Tống trẻ ngồi mệt mỏi bên bờ sông, ánh mắt nhìn sang bờ bên kia. |
| 19070 | Cuộc giằng co | Có sách chép rằng quân Tống ban đầu có hơn tám vạn người, về sau bỏ mạng quá nửa vì bệnh tật và thất bại. | chữ trên bản đồ: số liệu từ sách sử |
| 19071 | Cuộc giằng co | Nhận thấy thế trận giằng co không mang lại lợi ích, triều đình nhà Lý chủ động sai sứ sang nghị hòa. | chibi (LoRA 1,0): Một sứ giả Đại Việt cầm cờ hiệu sứ (cán dài, tua trơn, không chữ) ngồi trên thuyền nhỏ chèo qua sông, người chèo đứng sau. |
| 19072 | Cuộc giằng co | Vua Tống chấp thuận rút quân, nhưng vẫn giữ quyền kiểm soát các châu Quảng Nguyên, Tư Lang, Tô Mậu và huyện Quảng Lang. | bản đồ: Tống rút về, giữ lại vùng biên giới |
| 19073 | Cuộc giằng co | Thời điểm ngưng chiến được các sách ghi chép khác nhau, nên ta chỉ có thể xác định là vào khoảng năm một nghìn không trăm bảy mươi bảy. | chữ trên bản đồ: khoảng năm 1077 |
| 19074 | Cuộc giằng co | Chiến sự tạm dừng, nhưng nhiều vùng đất biên giới vẫn nằm trong tay nhà Tống. | chibi (LoRA 0,6): Doanh trại Tống đang thu quân, lính gấp lều, xếp đồ lên xe, nhìn từ xa; mặt đơn giản. |
| 19075 | Sau chiến tranh | Sau chiến tranh, triều đình Đại Việt vẫn canh cánh việc đòi lại những vùng lãnh thổ đang bị chiếm đóng. | bản đồ: các châu còn thuộc Tống |
| 19076 | Sau chiến tranh | Năm một nghìn không trăm bảy mươi tám, nhà Lý phái Đào Tống Nguyên mang năm con voi thuần hóa sang cống nạp nhà Tống. | chibi (LoRA 1,0): [DTN] mặc áo nâu cầm cờ hiệu sứ dẫn năm con voi đi trên đường, mỗi con voi một người quản tượng khác nhau. |
| 19077 | Sau chiến tranh | Sứ đoàn đưa ra yêu cầu trao trả châu Quảng Nguyên, Tô Mậu cùng những người dân đã bị bắt đi. | chibi (LoRA 0,6): Sứ đoàn Đại Việt đi trên đường đất dẫn đến một cổng thành Tống phía xa, cờ đỏ trơn, nhìn từ xa và sau lưng. |
| 19078 | Sau chiến tranh | Năm một nghìn không trăm bảy mươi chín, nhà Tống trả lại châu Quảng Nguyên, nhưng lúc này đã bị đổi tên thành Thuận Châu. | Quảng Nguyên đổi tên Thuận Châu |
| 19079 | Sau chiến tranh | Hai năm sau, Đại Việt cũng trao trả lại cho nhà Tống những binh lính và dân thường bị bắt từ Ung Châu, Khâm Châu và Liêm Châu. | chibi (LoRA 0,6): Đoàn người trở về nơi biên giới, hai bên đứng đối diện nhau (bên trái quan Đại Việt áo nâu, bên phải quan Tống áo xanh), dân thường đi qua giữa. |
| 19080 | Sau chiến tranh | Năm một nghìn không trăm tám mươi tư, Lê Văn Thịnh đến trại Vĩnh Bình để đàm phán phân định biên giới với người Tống. | chibi (LoRA 1,0): Trong trại Vĩnh Bình, [LVT] ngồi một bên bàn, một quan Tống ngồi đối diện, giữa bàn trải tấm bản đồ chỉ có nét vẽ, không chữ. |
| 19081 | Sau chiến tranh | Kết quả, nhà Tống buộc phải trả thêm cho Đại Việt sáu huyện và ba động. | sáu huyện, ba động đổi màu |
| 19082 | Sau chiến tranh | Người Tống khi ấy có câu thơ ngậm ngùi rằng vì tham voi của Giao Chỉ mà để mất vàng Quảng Nguyên. | thơ chữ nhỏ bên bản đồ |
| 19083 | Những năm cuối | Khói lửa tan đi, Lý Thường Kiệt vẫn tiếp tục đảm đương chức thái úy, thống lĩnh binh quyền cả nước. | chibi (LoRA 1,0): Trong phủ thái úy, [LTK-G] ngồi bên bàn gỗ, trước mặt là tấm bản đồ chỉ có nét vẽ, vài ngọn nến, một võ quan đứng hầu bên cạnh. |
| 19084 | Những năm cuối | Năm một nghìn một trăm linh một, nhà vua giao cho ông kiêm nhiệm thêm chức vụ quản lý công việc trong ngoài hoàng cung. | Thăng Long, hiện chức mới |
| 19085 | Những năm cuối | Đến năm một nghìn một trăm linh ba, một kẻ tên Lý Giác làm phản, dấy binh chiếm giữ Diễn Châu. | chibi (LoRA 0,6): [LG] (áo nâu thường dân, mặt rắn rỏi) đứng trên một đoạn thành đất vừa đắp ở Diễn Châu, dân làng nhìn từ xa, cờ trơn. |
| 19086 | Những năm cuối | Vua lệnh cho Lý Thường Kiệt đem quân thảo phạt. Lý Giác đại bại phải tháo chạy sang Chiêm Thành, bè đảng bị dẹp yên. | chibi (LoRA 0,6): Quân Đại Việt kéo đến Diễn Châu trên đường đất, cờ đỏ trơn, nhìn từ xa; thành đất nhỏ phía trước. |
| 19087 | Những năm cuối | Năm sau, vua Chiêm Thành là Chế Ma Na đem quân lên đánh chiếm lại ba châu mà vua cũ Chế Củ từng dâng. | Chiêm Thành lấn lên ba châu |
| 19088 | Những năm cuối | Lý Thường Kiệt một lần nữa nhận lệnh xuất chinh và giành chiến thắng, buộc Chế Ma Na phải dâng trả lại vùng đất ấy. | chibi (LoRA 1,0): Doanh trại Đại Việt về đêm, đèn trại sáng; [LTK-L] đứng giữa trại nhìn về phía nam. |
| 19089 | Những năm cuối | Đó cũng là lần cuối cùng sử sách ghi nhận tên ông cầm quân ra trận, chỉ hơn một năm trước khi ông qua đời. | chibi (LoRA 1,0): [LTK-L] ngồi bên cửa sổ nhìn ra xa, ánh chiều tà, trong phủ. |
| 19090 | Những năm cuối | Mùa hạ, tháng sáu năm một nghìn một trăm linh năm, thái úy Lý Thường Kiệt nhắm mắt xuôi tay. | chibi (LoRA 1,0): Phòng làm việc phủ thái úy yên lặng, một ngọn đèn dầu nhỏ, chiếc ghế trống và bộ áo mão treo trên giá. Không có người. |
| 19091 | Những năm cuối | Triều đình truy tặng ông tước Việt quốc công, và ân chuẩn cho người em trai là Lý Thường Hiến được thế tập tước hầu. | chibi (LoRA 0,6): Trong triều, [LTH] quỳ nhận tước hầu từ một quan lễ, quan khác đứng bên chứng kiến. |
| 19092 | Trở lại bên tường thành | Từ một cậu bé hầu cận trong cung đến vị thái úy uy dũng chặn đứng quân Tống bên bờ Như Nguyệt, ông đã phụng sự qua ba đời vua nhà Lý. | chibi (LoRA 1,0): Ba ngai vàng xếp hàng, mỗi ngai một vị vua (Thái Tông, Thánh Tông, Nhân Tông bé) hiện lần lượt như ký ức, [LTK-L] đứng nhỏ phía trước. |
| 19093 | Trở lại bên tường thành | Cuộc đời ông khởi đầu từ chốn thâm cung và khép lại ở đỉnh cao của quyền lực quân sự. | Thăng Long, hai chấm đầu và cuối |
| 19094 | Trở lại bên tường thành | Trận vây thành Ung Châu và phòng tuyến sông Như Nguyệt diễn ra cách nhau chỉ khoảng một năm. | bản đồ: hai chấm Ung Châu, Như Nguyệt nối bằng một đường |
| 19095 | Trở lại bên tường thành | Một trận ông mang quân dội bão lửa sang đất địch, một trận ông vững vàng bảo vệ tấc đất quê hương. | hai mũi tên ngược chiều |
| 19096 | Trở lại bên tường thành | Còn bài thơ vọng vang trong đêm bên bờ sông thuở ấy, vẫn được người đời lưu truyền mãi đến tận hôm nay. | chibi (LoRA 1,0): Bờ sông Cầu về đêm trăng, hàng rào tre, sương mỏng. Không chữ trong ảnh; lời thơ do lớp chữ video hiện. |

## Mô tả video và nguồn (để dán khi đăng)

Lý Thường Kiệt là ai, và vì sao quân Đại Việt đánh sang thành Ung Châu của nhà Tống vào cuối năm 1075? Video kể từ cậu bé hầu cận trong cung đến vị thái úy chặn quân Tống bên sông Như Nguyệt, theo sử cũ.

Nguồn chính: Đại Việt sử ký toàn thư (Bản kỷ, quyển III, kỷ nhà Lý), Khâm định Việt sử thông giám cương mục. Chi tiết chỉ có trong chuyện truyền lại (bài thơ bên sông Như Nguyệt) được nói rõ là chuyện truyền. Số liệu người chết ở Ung Châu là con số do sử Đại Việt chép, các nguồn khác chép khác.

**Tiêu đề đề xuất:** Lý Thường Kiệt: vì sao Đại Việt đánh sang Ung Châu trước?
**Hashtag:** #NguoiGacSu #LyThuongKiet #LichSuVietNam #NhaLy #NamQuocSonHa #SongNhuNguyet #ChongTong

## Việc cần chủ kênh quyết

1. [Đã duyệt 29/10: giữ nguyên câu số người chết ở Ung Châu; lấy theo bản chủ kênh đã sửa.]
2. [Đã đổi 29/10 21:10, cập nhật 21:30] Bỏ vector, 64 đoạn dùng ảnh chibi (39 đoạn LoRA 1,0 và 25 đoạn LoRA 0,6 cho cảnh nhiều người), 32 đoạn bản đồ.
3. Có thêm trận Như Nguyệt chi tiết (máy bắn đá, cọc dưới sông) không: cần tìm thêm nguồn trước.
4. Giọng: luôn Sadaltager (quy tắc chủ kênh 29/10), đọc từng đoạn một (`cum.txt` = 1). Gemini đang hết hạn mức ngày, làm mới khoảng 16:00 giờ Nhật.
5. **Mới (chibi):** duyệt bảng nhân vật và quy ước trang phục ở mục "Cảnh bản đồ và cảnh chibi"; duyệt cách xử lý chương Ung Châu (19045–19053; ít người, tông xám cam, hoặc chuyển sang bản đồ).
6. **Mới (chibi):** khổ ảnh. Bản thử dùng 1152×768 (3:2); video 1920×1080 cần 16:9, đề xuất 1344×768 như bộ Tam Quốc rồi cắt vừa khung. Chủ kênh chốt.
7. **Mới (chibi):** vẽ thử 3 đến 4 cảnh trước (đề xuất 19004 Lý Thường Kiệt trên tường thành, 19024 vua nhỏ sau rèm, 19019 hai đoàn quân, 19045 Tô Giám) để soi mặt và độ trang nghiêm, rồi mới vẽ cả 67 ảnh. Chỉ chạy khi chủ kênh yêu cầu.
