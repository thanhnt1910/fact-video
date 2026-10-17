# Nội dung bài Telegram cho từng tập. Định dạng HTML của Telegram: chỉ dùng <b>, <i>, <blockquote>.
# Mỗi tập gồm: ảnh + caption (<= 1024 ký tự), rồi các tin nhắn nội dung (mỗi tin <= 4096 ký tự).

TAGS = "#TamQuốc #ChínhSử #NgườiGácSử"

TAP = {}

# Ảnh 2D đã chọn (đường dẫn trong repo thanhnt1910/fact-video, nhánh có TQ3: tq2-sua-anh). Mỗi album: thẻ chữ + 9 ảnh 2D theo thứ tự câu chuyện.
ANH2D = {
    1: [f"TQ1/{n}.jpg" for n in ("001","009","011","015","022","032","061","036","044")],
    2: [f"TQ2/{n}.jpg" for n in ("001","007","016","025","028","037","042","052","056")],
    3: [f"TQ3/{n}.jpg" for n in ("001","006","016","026","038","043","048","062","066")],
}


# ---------------------------------------------------------------- TẬP 1
TAP[1] = {
    "anh": "tap1.png",
    "caption": """🏯 <b>TAM QUỐC THEO CHÍNH SỬ · TẬP 1</b>
<b>Lưu Bị bán giày cỏ: chính sử kể gì về khởi đầu của ông?</b>

Năm 184, hàng chục vạn người quấn khăn vàng nổi dậy, nhà Hán bắt đầu sụp đổ. Giữa lúc ấy, một người bán giày cỏ ở huyện Trác tập hợp được hai người bạn và một nhóm quân nhỏ.

Không phép thuật, không vườn đào: trong Tam quốc chí không có một chữ nào về vườn đào. Chỉ có những gì Tam quốc chí và Hậu Hán thư chép lại.

Nội dung đầy đủ ở các tin bên dưới 👇""",
    "tin": [
"""📖 <b>NỘI DUNG TẬP 1 (phần 1/2)</b>

<b>Câu hỏi của tập:</b> một người không binh, không tiền, không chức đã bắt đầu từ đâu? Câu chuyện dựa vào bộ Tam quốc chí của Trần Thọ cùng chú giải của Bùi Tùng Chi. Bộ tiểu thuyết của La Quán Trung chỉ được viết hơn một nghìn năm sau, và nhiều cảnh nổi tiếng trong đó không có trong sử.

Nhà Hán đã tồn tại gần bốn trăm năm và mục ruỗng từ bên trong. Hán do Lưu Bang lập ra; sau khi bị Vương Mãng cướp ngôi, một người họ Lưu khác dựng lại triều đại, sử gọi là Đông Hán. Hoàng đế Linh đế bán cả chức quan để lấy tiền, hoạn quan nắm quyền trong triều. Người bỏ tiền mua chức sẽ tìm cách lấy lại vốn, và người trả giá cuối cùng thường là dân thường. Nhiều năm liền thiên tai, dịch bệnh kéo đến, nông dân đói khổ, mất ruộng, mất cả nhà cửa.

Người đứng lên thu phục lòng dân là đạo sĩ Trương Giác ở Cự Lộc. Ông lập Thái Bình đạo, chữa bệnh bằng bùa nước và sám hối, có hàng chục vạn tín đồ khắp tám châu. Ông chia tín đồ thành ba mươi sáu phương, như ba mươi sáu đạo quân: phương lớn hơn một vạn người, phương nhỏ chừng sáu bảy nghìn, mỗi phương có một người đứng đầu. Họ hẹn khởi sự năm Giáp Tý (184) và quấn khăn vàng trên đầu. Khẩu hiệu: “Trời xanh đã chết, trời vàng sẽ lên”; “năm Giáp Tý, thiên hạ đại cát”.
Nhưng kế hoạch bị lộ: một người trong đạo là Đường Chu đi tố giác, nên Trương Giác phải khởi sự sớm hơn dự định. Triều đình hoảng loạn, ra lệnh cho các châu quận dấy nghĩa binh. Lửa loạn lan nhanh khắp tám châu, nhiều quan địa phương hoảng sợ bỏ trốn.

Ở huyện Trác, quận Trác có một thanh niên tên Lưu Bị. Ông tự nhận là con cháu Trung Sơn Tĩnh vương Lưu Thắng, con của Cảnh đế nhà Hán. Họ Lưu là họ hoàng đế, nhưng qua nhiều đời dòng dõi ấy đã xa và không mang lại cho ông đặc quyền nào. Cha mất sớm, hai mẹ con sống bằng nghề bán giày, dệt chiếu.
Sử chép ông cao bảy thước năm tấc (khoảng 1,73 m), tay dài quá gối, quay đầu có thể thấy tai mình. Ông ít nói, giỏi hạ mình, vui buồn không lộ ra mặt; không thích đọc sách, thích chó ngựa, âm nhạc và áo quần đẹp. Năm 15 tuổi ông đi học với Lư Thực cùng bạn học Công Tôn Toản; thầy Lư Thực sau này là một trong những tướng được triều đình giao đánh Hoàng Cân. Điều ông giỏi nhất là kết bạn: thích giao du với hào kiệt, nhiều người trẻ muốn đi theo.

Nhà ông có một cây dâu rất lớn, từ xa nhìn như chiếc lọng xe. Hồi nhỏ ông chỉ cây dâu mà nói: sau này ta sẽ ngồi xe có lọng như thế. Người chú nghe thấy, quát: đừng nói bậy, cả họ ta sẽ bị giết. Giữa thời nhà Hán còn nguyên vẹn, đó là lời đại nghịch. Tam quốc chí chép lại câu nói ấy, cho thấy ông mang tham vọng từ rất sớm.""",

"""📖 <b>NỘI DUNG TẬP 1 (phần 2/2)</b>

Khi loạn Hoàng Cân nổ ra, Lưu Bị bắt đầu tập hợp người ở quê nhà. Hai người theo ông ngay từ những ngày ấy là Quan Vũ và Trương Phi: Quan Vũ người Hà Đông, chạy loạn tới quận Trác; Trương Phi người quận Trác. Sử chỉ ghi rất ngắn: hai người làm hộ vệ cho Lưu Bị. Ông đối xử với họ ngủ chung giường, ân nghĩa như anh em. Quan Vũ lớn hơn Trương Phi vài tuổi nên Phi coi Vũ như anh.
Không có tế trời đất, không có lời thề sinh tử: trong Tam quốc chí không có một chữ nào về vườn đào. Tình nghĩa ấy không đến từ một buổi lễ mà từ nhiều năm đi bên nhau.

Ba người còn thiếu tiền để nuôi quân. Sử chép hai thương nhân buôn ngựa giàu có, Trương Thế Bình và Tô Song, đã cho Lưu Bị nhiều tiền vì thấy ông khác thường. Họ không phải quan lại, họ nhìn người bằng con mắt người làm ăn: ai đáng để đặt cược. Có tiền, ông tập hợp được một nhóm quân nhỏ. Chưa phải một đội quân lớn, nhưng với người từng không có gì, đó là bước đầu tiên.

Ông đem quân theo hiệu úy Trâu Tĩnh đi đánh Hoàng Cân; đi theo một hiệu úy của triều đình là cách nhanh nhất để một nhóm quân nhỏ có danh phận. Hoàng Cân không phải một toán cướp mà là cả một đạo quân tín ngưỡng, hàng chục vạn người. Triều đình phái các đạo quân lớn do Lư Thực, Hoàng Phủ Tung, Chu Tuấn chỉ huy: Lư Thực đánh ở phía bắc, Hoàng Phủ Tung và Chu Tuấn đánh ở phía nam. Trong vòng một năm, quân khăn vàng bị đánh tan ở nhiều mặt; Trương Giác bệnh mất giữa chừng, sau đó quan tài bị mở ra và đầu ông bị đưa về kinh đô.
Công trạng của Lưu Bị trong sử chỉ có một câu: đánh giặc Hoàng Cân, có công. Phần thưởng rất nhỏ: chức huyện úy ở huyện An Hỉ, một chức nhỏ trong bộ máy nhà Hán. Sau bao tháng đánh trận, người con cháu hoàng tộc vẫn chỉ là một viên quan nhỏ nơi xa.

Dập xong Hoàng Cân, nhiều tướng lĩnh và quan châu quận giờ có quân riêng, triều đình không còn đủ sức quản họ. Từ đây nhiều người hiểu rằng ai nắm quân trong tay, người đó nắm số phận.

Lưu Bị ngồi ở An Hỉ, và một ngày nọ một viên đốc bưu đến huyện. Sử chép rất rõ điều ông làm với người ấy: chính tay ông trói viên đốc bưu lại và đánh. Điều đó khác hẳn chuyện bạn từng nghe: trong tiểu thuyết, người đánh đốc bưu là Trương Phi; trong sử, đó là chính Lưu Bị.

Tóm lại: Lưu Bị khởi đầu từ nghèo khó: bán giày cỏ, dệt chiếu, dòng dõi hoàng tộc đã quá xa. Quan Vũ và Trương Phi là hộ vệ, ngủ chung giường, ân nghĩa như anh em; không có lời thề vườn đào trong Tam quốc chí. Tiền nuôi quân đến từ hai thương nhân buôn ngựa; công lớn nhất ông được ghi chỉ là một câu và phần thưởng là chức huyện úy An Hỉ.

<b>Tập sau:</b> vì sao một viên huyện úy lại dám trói đánh đốc bưu, và chuyện gì xảy ra sau đó?""",

"""🔎 <b>NGUỒN VÀ GHI CHÚ (tập 1)</b>

<b>Nguồn:</b> Tam quốc chí của Trần Thọ (Tiên chủ truyện, Quan Vũ truyện, Trương Phi truyện, cả nguyên văn lẫn bản dịch hiện đại); chú giải của Bùi Tùng Chi; Hậu Hán thư (Linh đế kỷ, Hoàng Phủ Tung truyện), đối chiếu qua nguồn thứ cấp về khởi nghĩa Hoàng Cân.

<b>Ghi chú:</b> hình minh họa chỉ là tranh vẽ 2D, không phải tư liệu lịch sử. Chi tiết về tướng mạo (cao bảy thước năm tấc, tay dài quá gối) là mô tả trong sử, còn ý nghĩa “người khác thường” là cách nhìn của người đời sau.

#TamQuốc #ChínhSử #NgườiGácSử #Tập1""",
    ],
}

# ---------------------------------------------------------------- TẬP 2
TAP[2] = {
    "anh": "tap2.png",
    "caption": """🏯 <b>TAM QUỐC THEO CHÍNH SỬ · TẬP 2</b>
<b>Ai đánh viên đốc bưu? Lưu Bị lang bạt thế nào trước loạn Đổng Trác</b>

Trong tiểu thuyết, người đánh đốc bưu là Trương Phi. Nhưng Tam quốc chí chép chính Lưu Bị trói và đánh đốc bưu hai trăm gậy, rồi bỏ chức chạy đi.

Sau đó là nhiều năm lang bạt: bỏ chức, đổi chủ, thất bại, cho tới khi gặp lại bạn học cũ Công Tôn Toản. Trong lúc ấy kinh đô nhà Hán sụp đổ năm 189 với Đổng Trác.

Nội dung đầy đủ ở các tin bên dưới 👇""",
    "tin": [
"""📖 <b>NỘI DUNG TẬP 2 (phần 1/2)</b>

<b>Câu hỏi của tập:</b> vì sao một viên huyện úy nhỏ bé dám đánh quan trên, và sau đêm ấy ông đi đâu? Câu trả lời không phải một chiến công mà là nhiều năm lang bạt: bỏ chức, đổi chủ, nhiều lần thất bại. Trong lúc ông chưa là ai, thiên hạ đã bắt đầu đổi chủ.

Đốc bưu là quan do quận phái xuống, đi kiểm tra các huyện và xét công tội của quan lại; một lời của đốc bưu có thể khiến một viên quan nhỏ mất chức và mất luôn đường sống. Bản chú Điển lược mà Bùi Tùng Chi dẫn kể rằng khi ấy có lệnh thải bớt những người được bổ chức nhờ quân công, và Lưu Bị lo mình nằm trong số đó. Ông xin gặp đốc bưu nhưng không được cho vào. Ông bèn dẫn lính tới nhà trạm, xông vào, nói: ta có mật lệnh của quan phủ, đến bắt đốc bưu. Rồi ông trói đốc bưu trên giường và đưa ra tận ranh giới huyện.
Tam quốc chí chép gọn hơn: ông trói viên đốc bưu, đánh hai trăm gậy, rồi bỏ chức chạy đi. Trong tiểu thuyết người ra tay là Trương Phi; trong sử là chính Lưu Bị.

Sử không chép ông về quê ngay; ông tiếp tục tìm đường làm lính, làm quan. Đại tướng quân Hà Tiến sai người tuyển quân ở Đan Dương và Lưu Bị đi theo. Quân tới Hạ Bì thì gặp giặc, ông đánh có công, được bổ một chức thừa ở huyện Hạ Mật; nhưng sử lại chép ông bỏ chức ấy, không một lời giải thích. Sau đó ông làm huyện úy ở Cao Đường, rồi làm huyện lệnh. Giặc đến đánh, quân huyện bị đánh tan, ông lại phải bỏ chạy.
Làm quan, mất chức, làm quan, chạy giặc: trong nhiều năm ông không có chỗ đứng cố định.

Cuối cùng ông tìm đến người bạn cũ cùng học dưới thầy Lư Thực: Công Tôn Toản, lúc ấy có quân ở phía bắc. Toản tâu xin cho Lưu Bị làm Biệt bộ tư mã. Lưu Bị cùng Điền Giai đánh quân của Viên Thiệu, nhiều lần lập công; nhờ vậy được thử làm lệnh Bình Nguyên rồi làm tướng Bình Nguyên. Lần đầu tiên, người từng bán giày cỏ được cai quản cả một vùng đất.

Khi ông làm tướng Bình Nguyên, sử chép Quan Vũ và Trương Phi được giao làm Biệt bộ tư mã, mỗi người chỉ huy một phần quân. Đây là lần đầu hai người có quân riêng, nhưng họ vẫn đi theo ông, không đi theo ai khác. Từ đầu sử đã gọi họ là người hộ vệ, nghĩa là người đứng ra phía trước ông khi có chuyện. Một viên quan chạy trốn như Lưu Bị lúc ấy không có gì để giữ người, không lương, không đất, không chức; vậy mà hai người vẫn ở lại. Sử không nói vì sao, chỉ chép rằng họ ở lại.
Tiểu thuyết giải thích bằng một lời thề; sử chỉ cho thấy họ đi cùng nhau rất lâu và không bỏ nhau. Trần Thọ nhận xét Quan Vũ cứng cỏi mà tự phụ, Trương Phi hung bạo mà thiếu ơn nghĩa với người dưới; hai người tính khí khác nhau, không hoàn hảo, nhưng cùng một lòng với Lưu Bị. Chính hai điểm yếu ấy sau này trả giá rất đắt, nhưng ở thời điểm này họ là hai người đáng tin nhất ông có.

Ở Bình Nguyên có Lưu Bình, rất coi thường Lưu Bị và không chịu được việc ông được dân quý. Lưu Bình thuê một thích khách đi giết ông. Lưu Bị không hay biết gì, vẫn đối đãi người khách ấy rất hậu. Người khách cảm động, nói thật mọi việc rồi bỏ đi. Ba chi tiết trong sử đều nói một điều: ông giữ người không bằng sức mạnh mà bằng cách đối xử, có thể là thứ duy nhất ông có khi chưa có binh, chưa có đất.""",

"""📖 <b>NỘI DUNG TẬP 2 (phần 2/2)</b>

Trong lúc Lưu Bị lang bạt, nhà Hán tự đổ sập từ bên trong. Năm 189 Linh đế mất. Con của hoàng hậu họ Hà là Lưu Biện lên ngôi khi còn rất trẻ; quyền thật nằm trong tay cậu ông, đại tướng quân Hà Tiến, vốn xuất thân từ nhà làm nghề đồ tể, nhờ em gái được vào cung mà lên chức cao nhất quân đội. Hà Tiến muốn trừ bọn hoạn quan nhưng thái hậu không đồng ý, nên ông triệu các tướng ngoài biên vào kinh để gây sức ép, trong đó có Đổng Trác. Kế hoạch bị lộ, hoạn quan ra tay trước và giết Hà Tiến ngay trong cung.
Viên Thiệu cùng nhiều người đem quân vào cung, giết rất nhiều hoạn quan, hoàng cung loạn như một đêm không có luật. Hoàng đế trẻ và em ông bị đưa ra ngoài thành. Đúng lúc ấy Đổng Trác dẫn quân tới, gặp hoàng đế và đưa về kinh. Từ đó quân đội kinh đô nằm trong tay một người đến từ vùng biên cương. Ông phế Thiếu đế, lập người em là Lưu Hiệp, sau này là Hán Hiến đế. Khi người có quân không còn ai quản được, triều đình chỉ còn cái tên. Còn một người nghèo như Lưu Bị lúc ấy quá xa kinh đô để can thiệp.

Nhiều châu quận nổi binh chống Đổng Trác, họp thành liên quân. Một trong những người đứng lên sớm nhất là Tào Tháo: khi Trác muốn dùng ông làm quan, ông bỏ kinh đô chạy trốn, dựng quân ở Trần Lưu bằng tiền của những người ủng hộ. Viên Thiệu được các châu quận đưa lên làm minh chủ; trong liên quân có Tào Tháo, Tôn Kiên và nhiều người khác. Nghe rất hùng mạnh: hơn mười đạo quân cùng kéo tới. Nhưng mỗi người đều lo giữ quân của mình trước, không ai muốn là người đầu tiên bị tổn thất.
Trong tiểu thuyết, đây là nơi ba anh em Lưu Bị, Quan Vũ, Trương Phi cùng đánh Lữ Bố ở Hổ Lao. Nhưng trong Tiên chủ truyện không có một chữ nào về trận ấy. Cái tên Hoa Hùng, vị tướng bị chém trong cảnh nổi tiếng đó, trong sử gắn với một người khác: nhiều nguồn chép người đánh bại Hoa Hùng là Tôn Kiên. Đổng Trác sợ liên quân, bắt hoàng đế dời đô về Trường An và cho đốt cả Lạc Dương. Liên quân đông nhưng nhiều người chỉ đứng nhìn; chỉ có quân của Tôn Kiên từ phương nam kéo lên. Tào Tháo trách các tướng chần chừ, tự dẫn quân đuổi theo Đổng Trác nhưng bị đánh bại: lần đầu người ta thấy một Tào Tháo thất bại và vẫn bước tiếp.

Lưu Bị lúc này mới thật sự có một vùng đất để cai quản. Ở phía bắc, Viên Thiệu và Công Tôn Toản bắt đầu tranh nhau, liên minh chống Đổng Trác nhanh chóng vỡ ra; giữa hai người ấy Lưu Bị đứng về phía người bạn học cũ. Chú giải của Bùi Tùng Chi dẫn Hiến Đế xuân thu: dân Từ Châu về sau muốn tôn nguyên tướng Bình Nguyên Lưu Bị làm chủ. Viên Thiệu khi nghe tin cũng nói: Lưu Huyền Đức hoằng nhã, có tín nghĩa, dân Từ Châu mến ông, đúng như mong đợi. Đó là lời khen của một người từng đứng ở phía đối lập.

Tóm lại: Người trói và đánh đốc bưu hai trăm gậy là chính Lưu Bị, không phải Trương Phi. Sau đó là nhiều năm lang bạt cho tới khi gặp lại Công Tôn Toản và làm tướng Bình Nguyên. Quan Vũ và Trương Phi ở lại vì nhiều năm đi cùng nhau, không phải vì một lời thề. Danh tiếng chưa phải quân đội, đất đai chưa phải chỗ đứng chắc chắn.

<b>Tập sau:</b> kinh đô đã vào tay Đổng Trác, ai sẽ đứng lên chống lại ông ta? Và người mà tiểu thuyết gán công lớn nhất ở Hổ Lao, trong sử đang đứng ở đâu?""",

"""🔎 <b>NGUỒN VÀ GHI CHÚ (tập 2)</b>

<b>Nguồn:</b> Tam quốc chí (Tiên chủ truyện, Quan Vũ truyện, Trương Phi truyện, Vũ Đế kỷ); Hậu Hán thư; chú giải của Bùi Tùng Chi.

<b>Từ chú giải (lời kể phụ, không phải chính văn):</b> lệnh thải bớt người được bổ chức nhờ quân công và chuyện Lưu Bị xông vào nhà trạm trói đốc bưu (chú Điển lược); lời của dân Từ Châu và lời khen của Viên Thiệu (Hiến Đế xuân thu).

<b>Ghi chú:</b> hình minh họa chỉ là tranh vẽ 2D. Chuyện Hổ Lao và Hoa Hùng sẽ được kể kỹ ở tập 3.

#TamQuốc #ChínhSử #NgườiGácSử #Tập2""",
    ],
}

# ---------------------------------------------------------------- TẬP 3
TAP[3] = {
    "anh": "tap3.png",
    "caption": """🏯 <b>TAM QUỐC THEO CHÍNH SỬ · TẬP 3</b>
<b>Ai thật sự chém Hoa Hùng? Hổ Lao có thật không?</b>

Trong tiểu thuyết: Quan Vũ hâm rượu chém Hoa Hùng, rồi ba anh em vây đánh Lữ Bố trước ải Hổ Lao.

Trong Tam quốc chí: người chém Hoa Hùng là <b>Tôn Kiên</b>, ở Dương Nhân. Truyện Quan Vũ không hề có Hoa Hùng hay Hổ Lao.

Vậy Lữ Bố đã làm gì ở Dương Nhân? Đổng Trác thật sự chết thế nào? Lúc ấy Lưu Bị ở đâu?

Nội dung đầy đủ ở các tin bên dưới 👇""",
    "tin": [
"""📖 <b>NỘI DUNG TẬP 3 (phần 1/2)</b>

<b>Câu hỏi của tập:</b> hai cảnh nổi nhất Tam Quốc diễn nghĩa (hâm rượu chém Hoa Hùng; ba anh em đánh Lữ Bố ở Hổ Lao) có trong sử không? Nếu không, đó là chuyện của ai?

Đổng Trác vào Lạc Dương nhưng quân kinh đô chưa hoàn toàn thuộc về ông. Người cản đường là Đinh Nguyên, chức Chấp Kim Ngô. Trác sai Lữ Bố, thuộc hạ của Đinh Nguyên, giết chủ rồi thu quân. Lữ Bố được phong kỵ đô úy, được Trác tin yêu, hai bên thề làm cha con.
Khi Trác bàn chuyện phế Thiếu đế, Viên Thiệu là người cầm ngang đao, vái dài rồi bỏ đi. Trác vẫn phong ông làm thái thú Bột Hải. Không lâu sau, Trác giết cả Thiếu đế và Hà thái hậu, lên Tướng quốc, được phong Mi hầu, có đặc quyền mang gươm đi giày lên điện.

Các châu quận phía đông ải Hàm Cốc nổi binh, tôn Viên Thiệu làm minh chủ. Nhưng ai cũng lo giữ quân mình, không ai muốn là người tiến lên trước. Chỉ quân của Tôn Kiên, người đất Ngô ở phương nam, kéo thẳng về Lạc Dương.
Ông gặp Viên Thuật ở Lỗ Dương, được Thuật dâng biểu làm Phá Lỗ tướng quân, lĩnh Dự Châu thứ sử. Nghĩa là ông đánh Đổng Trác với danh nghĩa một tướng của Viên Thuật, không phải chủ một đạo quân độc lập.
Sử còn kể chuyện năm ông 17 tuổi: đi thuyền tới Tiền Đường, gặp bọn cướp biển đang chia của trên bờ, ông cầm đao lên bờ, chỉ tay sang đông sang tây như đang chia quân bao vây. Bọn cướp tưởng quan quân tới nên bỏ của chạy.

Tôn Kiên dời quân tới phía đông Lương, bị quân Trác đánh dữ, cùng vài chục kỵ phá vây thoát ra. Ông thường đội khăn đỏ; giữa vòng vây, ông đưa khăn cho thuộc hạ Tổ Mậu đội. Kỵ binh Trác đổ xô đuổi theo Mậu, nhờ vậy Kiên thoát theo đường tắt. Mậu xuống ngựa, đặt khăn lên một cột cháy dở giữa đám mộ rồi nấp vào cỏ; kỵ binh đến gần mới nhận ra đó chỉ là cái cột.

Tôn Kiên thu quân, hợp chiến ở Dương Nhân. Tam quốc chí chép cả trận bằng một câu: ông đánh tan quân Trác, chém đô đốc Hoa Hùng. Không có chén rượu còn nóng, không có Quan Vũ, không có ba anh em nào chặn Lữ Bố.
<i>Lời kể phụ (chú giải của Bùi Tùng Chi):</i> Trác cử Hồ Chẩn làm đại đốc hộ, Lữ Bố làm kỵ đốc. Các tướng ghét và e ngại Hồ Chẩn, muốn làm hỏng việc của ông. Lữ Bố cùng đồng bọn loan tin sai rằng giặc trong thành Dương Nhân đã bỏ chạy, nên đuổi theo. Các nguồn thứ cấp kể quân Hồ Chẩn vì thế rối loạn và bị đánh lui (phần này chưa đối chiếu nguyên văn).
Trong sử, Hoa Hùng chỉ là một đô đốc của Đổng Trác, tên nằm trong truyện của Tôn Kiên. Tiểu thuyết lấy một người thật đã chết dưới tay Tôn Kiên rồi trao công ấy cho Quan Vũ. Hổ Lao là một cửa ải có thật, nhưng cảnh ba người đánh Lữ Bố ở đó không thấy trong sử.""",

"""📖 <b>NỘI DUNG TẬP 3 (phần 2/2)</b>

Sau trận ấy, Đổng Trác dời thiên tử về Trường An, đốt cung thất Lạc Dương và cho đào lăng mộ lấy bảo vật. Đó là kinh đô nhà Hán đã giữ hơn 160 năm.
Tôn Kiên tiến vào thành. Việc đầu tiên ông làm là sửa lại các lăng, lấp những chỗ Trác đã đào. <i>Một bản chú dẫn Ngô thư kể thêm:</i> ông cho người xuống một cái giếng và vớt được truyền quốc tỷ của nhà Hán. Một chú khác kể sau này Viên Thuật, khi định xưng đế, nghe tin ấy thì bắt phu nhân của Tôn Kiên để đoạt ngọc tỷ (chi tiết này cần kiểm thêm).
Viên Thuật nghi ngờ Tôn Kiên nên không chuyển lương. Kiên phải phi ngựa trong đêm tới gặp Thuật, vạch đất ra để bày tính. Liên quân sợ Đổng Trác, nhưng cũng sợ lẫn nhau.

Về sau ông đánh Lưu Biểu, vây Tương Dương, một mình cưỡi ngựa đi trên núi Hiện thì bị quân của Hoàng Tổ bắn chết. Các nguồn chép năm mất lệch nhau; Ngô lục chép ông mới 37 tuổi. Người đầu tiên thật sự kéo quân về Lạc Dương đã chết trước cả Đổng Trác. Con ông là Tôn Sách rồi Tôn Quyền sẽ lập nên Đông Ngô, nhưng đó là chuyện các tập sau.

Đổng Trác đã đi, không ai muốn nhường ai. Viên Thiệu cùng Hàn Phức muốn tôn Lưu Ngu, châu mục U Châu và là người tông thất nhà Hán, lên làm hoàng đế. Họ sai sứ dâng biểu nhưng Lưu Ngu không dám nhận. Công Tôn Toản đánh bại quân Hàn Phức ở An Bình rồi tiến vào Ký Châu, lấy danh nghĩa thảo Trác; Hàn Phức vốn nhút nhát, sợ hãi xin rời đi. Sau đó Viên Thiệu và Công Tôn Toản giao chiến ở phía nam Giới Kiều hai mươi dặm. Từ liên minh chống Đổng Trác, thiên hạ chuyển sang cuộc chiến giữa các chư hầu.
Còn Lưu Bị, bạn học cũ của Công Tôn Toản, lúc này chỉ là một viên tướng nhỏ giữ Bình Nguyên ở phía bắc. Quan Vũ truyện cho biết Quan Vũ và Trương Phi đi theo Lưu Bị; chính văn không kể họ làm gì ở Dương Nhân hay Lạc Dương, và truyện Quan Vũ không có Hoa Hùng hay Hổ Lao.

Ở Trường An, Trác xây ổ Mi cao ngang tường thành, tích lương đủ ba mươi năm. Nhưng kẻ gần ông nhất lại nguy hiểm nhất.
Lữ Bố truyện chép: có lần Trác chỉ vì chút không vừa ý đã rút kích ném Lữ Bố. Bố lại tư thông với một thị tỳ của Trác, sợ bị phát hiện nên bất an. Thị tỳ ấy không có tên; Điêu Thuyền không xuất hiện trong truyện Lữ Bố.
Tư đồ Vương Doãn, Sĩ Tôn Thụy và Lữ Bố cùng mưu giết Trác. Lý Túc dẫn người giả làm vệ sĩ canh cửa cung; Trác vào dự đại hội ở điện Vị Ương. Năm 192, chính Lữ Bố tự tay ra tay. Hơn chục đạo quân liên quân không hạ được Đổng Trác; người hạ ông là người con nuôi ông tin nhất.

Tóm lại: Người chém Hoa Hùng là Tôn Kiên, ở Dương Nhân, không phải Quan Vũ. Lữ Bố có mặt ở đó, nhưng không phải để đấu ba anh em: theo chú giải, ông cùng các tướng khác ghét và e ngại chính người chỉ huy của mình. Hổ Lao là cửa ải thật, nhưng cảnh ba người đánh Lữ Bố không thấy trong sử. Đổng Trác chết do mưu của Vương Doãn, Sĩ Tôn Thụy, Lữ Bố; Lữ Bố ra tay. Không có Điêu Thuyền trong truyện Lữ Bố. Đổng Trác chết nhưng nhà Hán không được cứu, loạn chỉ đổi người.

<b>Tập sau:</b> giữa lúc ấy Lưu Bị vẫn chỉ là tướng nhỏ ở Bình Nguyên, nhưng một châu ở phía đông sắp gọi tên ông. Vì sao một người chưa có đất, chưa có quân lớn, lại được cả một châu nhắc tới?""",

"""🔎 <b>PHẦN NÀO CHẮC, PHẦN NÀO LÀ LỜI KỂ PHỤ (tập 3)</b>

<b>Có trong chính văn Tam quốc chí:</b> Tôn Kiên chém Hoa Hùng ở Dương Nhân; Kiên bị vây, khăn đỏ Tổ Mậu; Trác dời đô, đốt Lạc Dương; Kiên sửa lăng; Kiên chết ở núi Hiện; chuyện Lữ Bố giết Đinh Nguyên, bị Trác ném kích, tư thông thị tỳ, giết Trác năm 192.

<b>Từ chú giải của Bùi Tùng Chi (lời kể phụ, không phải chính văn):</b> Hồ Chẩn và Lữ Bố ở Dương Nhân; Kiên vớt truyền quốc tỷ; Viên Thuật bắt phu nhân Kiên đoạt ngọc tỷ; Kiên mất lúc 37 tuổi.

<b>Còn cần kiểm thêm:</b> quân Hồ Chẩn rối loạn rồi bị đánh lui; chi tiết Hổ Lao (nhà nghiên cứu cần tra thêm các truyện khác); năm mất chính xác của Tôn Kiên; nửa sau chuyện cướp biển ở Tiền Đường; câu chữ chính xác của đoạn Lý Túc canh cửa cung và đại hội ở điện Vị Ương.

<b>Ghi chú:</b> hình minh họa chỉ là tranh vẽ; tên và kiểu vũ khí của các tướng là hình tượng của tiểu thuyết, chính sử không ghi.

<b>Nguồn đối chiếu:</b> Tam quốc chí (Tôn Phá Lỗ truyện, Đổng Trác truyện, Lữ Bố truyện, Quan Vũ truyện, Tiên chủ truyện, Viên Thiệu truyện) và chú của Bùi Tùng Chi.

#TamQuốc #ChínhSử #NgườiGácSử #Tập3""",
    ],
}

# ---------------------------------------------------------------- TẬP 4
TAP[4] = {
    "anh": "tap4.png",
    "caption": """🏯 <b>TAM QUỐC THEO CHÍNH SỬ · TẬP 4</b>
<b>Vì sao Từ Châu chọn Lưu Bị? Có thật “ba lần nhường”?</b>

Trong tiểu thuyết: Đào Khiêm ba lần nhường Từ Châu, ba lần Lưu Bị từ chối.

Trong sử: Khiêm dặn Mi Trúc “ngoài Lưu Bị, không ai giữ yên được châu này”. Lưu Bị chưa dám nhận, rồi được Trần Đăng và Khổng Dung khuyên mới nhận. Không có ba lần từ chối, chỉ có một cuộc tính toán của cả một châu.

Đằng sau đó là hai chuyến đi cứu người: một ở Bắc Hải, một ở Từ Châu.

Nội dung đầy đủ ở các tin bên dưới 👇""",
    "tin": [
"""📖 <b>NỘI DUNG TẬP 4 (phần 1/2)</b>

<b>Câu hỏi của tập:</b> cảnh “Đào Khiêm ba lần nhường Từ Châu” có trong sử không, và sử kể Lưu Bị đến Từ Châu bằng cách nào? Đây cũng là câu trả lời cho câu hỏi cuối tập trước: vì sao một người chưa có đất, chưa có quân lớn, lại được cả một châu nhắc tới?

Lưu Bị giữ Bình Nguyên dưới trướng người bạn học cũ Công Tôn Toản. Chức của ông lên từng nấc nhỏ: Biệt bộ tư mã, rồi lệnh, rồi tướng Bình Nguyên. Nhiệm vụ: cùng Điền Giai, thứ sử Thanh Châu, chặn đường Viên Thiệu. Ông đánh được nhiều trận nhưng chức vẫn nhỏ.
Trong quận có Lưu Bình, thấy phải đứng dưới Lưu Bị là điều nhục, bèn thuê một người khách đi giết ông. Người khách đến nhưng không nỡ ra tay, nói thật mọi chuyện với Lưu Bị rồi bỏ đi.

Thái Sử Từ từ Bắc Hải tìm tới Bình Nguyên: Khổng Dung (hậu duệ của Khổng Tử, một danh sĩ thời ấy) đang bị giặc vây chặt, nguy trong sớm tối. Lưu Bị xúc động, nói: “Khổng Bắc Hải mà cũng biết trên đời có người tên Lưu Bị sao?”. Ông chia ngay ba nghìn quân tinh nhuệ cho Thái Sử Từ. Giặc nghe quân cứu viện kéo tới thì giải vây, tan chạy. Ông chưa có đất, nhưng đã có một người mang ơn mình: Khổng Dung.

Cha Tào Tháo là Tào Tung bỏ quan về quê, rồi tránh loạn sang Lang Gia, vùng đất thuộc Từ Châu. Ở đó ông cụ bị giết và tội ấy được ghi cho Đào Khiêm, châu mục Từ Châu. Ai ra tay và vì sao thì còn nhiều lời kể khác nhau, nhưng với Tào Tháo, cha mình đã chết trên đất Từ Châu là đủ để báo thù.
Năm 193, Tháo đem quân đánh Đào Khiêm, hạ hơn mười thành. Năm sau ông đánh tiếp, hạ thêm năm thành; quân đi tới đâu, nơi ấy có nhiều người bị giết. Từ Châu khi ấy giàu và đông dân, hẳn cũng là một cái mồi.

Đào Khiêm sai sứ báo gấp cho Điền Giai. Giai kéo quân đi cứu và Lưu Bị đi cùng. Lần này ông không còn là người chia quân cho người khác, mà tự mình đi, với hơn một nghìn quân riêng, kỵ binh Ô Hoàn và vài nghìn dân đói thu nhận trên đường.
Lưu Bị cùng Tào Báo, tướng của Đào Khiêm, đóng quân phía đông Đàm để chặn Tháo, và bị Tháo đánh bại. Nhưng Đào Khiêm thấy được điều khác: người từ xa tới cứu mình khi nhiều người chỉ ngồi nhìn. Ông chia thêm cho Lưu Bị bốn nghìn quân Đan Dương; Lưu Bị rời Điền Giai, theo về với Khiêm. Khiêm dâng biểu cho ông làm thứ sử Dự Châu, đóng quân ở Tiểu Bái.
Rồi Tào Tháo phải rút: năm 194 Trương Mạc và Trần Cung nổi dậy, đón Lữ Bố vào Duyện Châu, quận huyện đều hưởng ứng. Lữ Bố chính là người đã cùng Vương Doãn giết Đổng Trác năm 192 (tập 3). Nghĩa là Từ Châu thoát nạn không phải vì Lưu Bị thắng, mà vì Tào Tháo phải quay về. Nhưng người ta nhớ ai đã đến cứu, chứ không nhớ vì sao Tháo rút.""",

"""📖 <b>NỘI DUNG TẬP 4 (phần 2/2)</b>

Đào Khiêm lâm bệnh nặng. Người ở bên ông là biệt giá Mi Trúc, xuất thân gia tộc buôn bán nhiều đời, nuôi cả vạn người làm và khách, của cải lên tới hàng ức. Khiêm nói với Mi Trúc: ngoài Lưu Bị ra, không ai giữ yên được Từ Châu.
Khiêm mất. Mi Trúc vâng di mệnh, dẫn người cả châu ra đón Lưu Bị ở Tiểu Bái. <b>Và Lưu Bị không dám nhận.</b>
Trần Đăng, người Hạ Bì, khuyên: Hán thất đang suy, đây là lúc lập công; Từ Châu giàu có, dân số tới cả trăm vạn, mong ông về lo việc châu. Lưu Bị đáp: Viên Thuật ở Thọ Xuân, nhà bốn đời năm công, thiên hạ đang trông vào ông ta, sao không giao cho ông ta? Trần Đăng đáp: Viên Thuật kiêu ngạo, không phải người dẹp loạn. Khổng Dung, lúc ấy là tướng Bắc Hải, người Lưu Bị từng cứu, cũng khuyên: gọi Viên Thuật là khúc xương khô trong mộ, và nói trời cho mà không nhận thì hối không kịp.
Lúc ấy Lưu Bị mới nhận lĩnh Từ Châu. Ân huệ nhỏ ở Bắc Hải đã quay lại theo cách không ai tính trước.

Tiểu thuyết: Đào Khiêm nhường ba lần, Lưu Bị từ chối ba lần vì đức. Sử chép ngắn hơn nhiều: ông chưa dám nhận, được Trần Đăng và Khổng Dung khuyên, rồi mới nhận, và lý lẽ khuyên ông rất thực tế: Từ Châu giàu, nếu ông không nhận thì Viên Thuật sẽ nhận. Chỗ tiểu thuyết đúng với sử: Tào Tháo rút vì Lữ Bố chiếm Duyện Châu.
Hãy nhìn những người đưa ông lên: Mi Trúc (nhà buôn giàu), Trần Đăng (người Hạ Bì), Khổng Dung (danh sĩ Bắc Hải). Không ai là quân nhân. Đó là một liên minh của tiền bạc, danh tiếng và lòng dân địa phương, và với một người không có đất, hẳn đó là thứ vốn duy nhất có thể có. Điều đó không làm Lưu Bị nhỏ đi, chỉ làm ông bớt giống thánh nhân và giống người hơn.

Lưu Bị khi đó mới ngoài ba mươi tuổi. Mười năm trước, sau trận Khăn Vàng, ông chỉ được làm úy An Hỷ. Sử chép ông nhiều lần mất chức, bỏ quan, phải bắt đầu lại. Quan Vũ và Trương Phi vẫn đi cùng: khi ông làm tướng Bình Nguyên, hai người đều làm Biệt bộ tư mã, mỗi người thống lĩnh một phần quân; ba người ngủ cùng giường, ân nghĩa như anh em.

Một châu giàu cũng là một châu bị nhiều người nhòm ngó. Phía bắc Tào Tháo chưa quên món nợ của cha; phía nam Viên Thuật ngồi ở Thọ Xuân; trong Từ Châu, những người từng theo Đào Khiêm chưa chắc đã đồng lòng với người mới đến; và Lưu Bị không có đạo quân lớn để giữ tất cả.

Tóm lại: Lưu Bị có Từ Châu không phải vì may, cũng không phải vì “ba lần nhường”. Ông có nó vì hai lần đi cứu người (Bắc Hải và Từ Châu) khi nhiều người khác ngồi yên, và vì vài người đủ quan trọng ở Từ Châu đã chọn tin ông. Nhưng nhận được Từ Châu là một chuyện, giữ được nó lại là chuyện khác.

<b>Tập sau:</b> có một người đang trên đường tới cửa nhà ông, kẻ từng tự tay giết Đổng Trác. Vì sao người được ông cho nương nhờ lại là người lấy Từ Châu khỏi tay ông?""",

"""🔎 <b>PHẦN NÀO CHẮC, PHẦN NÀO CHƯA (tập 4)</b>

<b>Đã đối chiếu chữ Hán trong Tam quốc chí:</b> Tào Tung bị giết ở Lang Gia và tội ghi cho Đào Khiêm; Tháo đánh Từ Châu năm 193 và 194; Lưu Bị cùng Tào Báo đóng phía đông Đàm; Đào Khiêm cho bốn nghìn quân Đan Dương, dâng biểu Dự Châu thứ sử; lời trăn trối với Mi Trúc; Trần Đăng, Khổng Dung khuyên; Lưu Bị lĩnh Từ Châu; Lữ Bố được đón vào Duyện Châu; Lưu Bị cứu Khổng Dung (Thái Sử Từ truyện); Quan Vũ, Trương Phi làm Biệt bộ tư mã.

<b>Từ chú giải (lời kể phụ):</b> chuyện Lưu Bình thuê khách giết Lưu Bị; Lưu Bị cùng Điền Giai chống Viên Thiệu.

<b>Chưa chắc chắn:</b> ai trực tiếp giết Tào Tung (các sách kể khác nhau, nên không chọn bản nào); năm sinh của các nhân vật dùng để tính tuổi chỉ là nhớ, cần kiểm lại; số người bị giết ở Từ Châu mỗi nguồn một khác nên không nêu số.

<b>Ghi chú:</b> Điền Giai trong sử là Điền Khải (田楷), giữ cách đọc quen thuộc “Điền Giai”. Hình minh họa chỉ là tranh vẽ; tên và kiểu vũ khí của các tướng là hình tượng của tiểu thuyết.

<b>Nguồn đối chiếu:</b> Tam quốc chí (Vũ Đế kỷ, Tiên chủ truyện, Mi Trúc truyện, Thái Sử Từ truyện, Quan Vũ truyện) và chú của Bùi Tùng Chi.

#TamQuốc #ChínhSử #NgườiGácSử #Tập4""",
    ],
}

# ---------------------------------------------------------------- TẬP 5
TAP[5] = {
    "anh": "tap5.png",
    "caption": """🏯 <b>TAM QUỐC THEO CHÍNH SỬ · TẬP 5</b>
<b>Ai thật sự làm mất Từ Châu? Trương Phi có say rượu không?</b>

Trong tiểu thuyết: Trương Phi uống say, đánh Tào Báo, Lữ Bố nhân đó chiếm Hạ Bì.

Trong sử: Viên Thuật đánh Lưu Bị suốt một tháng, Lữ Bố thừa lúc trống mà đánh úp Hạ Bì, tướng giữ thành Tào Báo phản đón Bố. Đoạn sử chính không có tên Trương Phi và không có chén rượu nào.

Và vì sao người Lưu Bị cho nương nhờ lại là người lấy thành của ông?

Nội dung đầy đủ ở các tin bên dưới 👇""",
    "tin": [
"""📖 <b>NỘI DUNG TẬP 5 (phần 1/2)</b>

<b>Câu hỏi của tập:</b> cảnh “Trương Phi say rượu, đánh Tào Báo, làm mất Từ Châu” có trong sử không? Nếu không thì Từ Châu mất bằng cách nào, và vì sao người Lưu Bị cho nương nhờ lại là người lấy thành của ông?

Sau khi Đổng Trác chết, Vương Doãn phong Lữ Bố làm Phấn Vũ tướng quân, giả tiết, tước Ôn hầu, cùng nắm triều chính. Nhưng Bố sợ và ghét người Lương Châu, họ cũng oán ông, nên Lý Thôi cùng đồng bọn kéo về đánh Trường An. Trác chết chưa đầy hai tháng thì Bố cũng bại. Bố dẫn vài trăm kỵ ra Vũ Quan định tìm Viên Thuật, vì cho rằng giết Trác là báo thù hộ Thuật; nhưng Thuật ghét tính hay phản phúc của ông và từ chối.
<i>Theo lời kể phụ (chú giải):</i> trước khi bại, Bố ra giữa hai quân, nói với Quách Tỵ hãy tự quyết thắng bại rồi đâm trúng Tỵ.
Ông quay lên phía bắc, tới chỗ Viên Thiệu, cùng đánh Trương Yên ở Thường Sơn. Ông có ngựa quý Xích Thố; người đời có câu “trong người có Lữ Bố, trong ngựa có Xích Thố”. Cùng vài thân tín, ông xông thẳng vào trận phá tan quân Yên. Nhưng ông xin thêm quân, tướng sĩ lại cướp bóc, Viên Thiệu ghét và e ngại. Ông xin đi, Thiệu sợ ông quay lại hại mình nên sai tráng sĩ đêm tới giết, không được (lời kể phụ tả thêm: ông cho người ngồi đánh đàn tranh trong trướng rồi lẻn đi, nửa đêm lính chém loạn lên giường chăn). Quân Thiệu đuổi theo nhưng ai cũng sợ ông không dám đến gần; ông tới nương Trương Dương ở Hà Nội.

Tháo giữ Duyện Châu và tin Trương Mạc hơn ai hết: trước khi đi đánh Từ Châu, ông dặn nhà rằng nếu không về thì đến nương Mạc. Nhưng Mạc sợ cuối cùng Tháo sẽ vì Viên Thiệu mà đánh mình. Năm 194, khi Tháo lại đi đánh Từ Châu, em Mạc là Trương Siêu cùng Trần Cung bàn phản. Trần Cung nói: quân châu đã đi xa, nơi này trống, Lữ Bố là tráng sĩ, hãy tạm đón về cùng cai quản Duyện Châu rồi xem thế thiên hạ. Mạc nghe theo; Bố làm Duyện Châu mục, đóng Bộc Dương, quận huyện hưởng ứng, chỉ còn Chân Thành, Đông A, Phạm giữ cho Tháo (đây là lúc Tháo phải rút, Từ Châu thoát nạn, như tập 4).
Hai bên giằng co hơn một trăm ngày. Có lần Tháo cưỡi ngựa phi qua lửa, ngã, cháy lòng bàn tay trái. Năm ấy hạn hán, châu chấu, một hộc thóc giá hơn năm mươi vạn tiền, người ăn thịt nhau. Viên Thiệu cho người đề nghị hòa, Tháo định nhận, Trình Dục ngăn lại và Tháo nghe theo. Năm 195 Tháo đánh bại Bố ở Cự Dã. Siêu giữ Ung Khâu bị vây rồi tự sát; Mạc đi cầu cứu Viên Thuật và bị chính quân mình giết. Sử chép gọn: Bố chạy về phía đông, đến nương Lưu Bị.

Lúc ấy Lưu Bị đã là chủ Từ Châu. <i>Theo lời kể phụ (chú giải):</i> Lữ Bố rất kính Bị, nói “ta với ngươi đều là người vùng biên ải”; nói thêm rằng sau khi giết Trác, các tướng Quan Đông không ai dung ta. Ông mời Bị ngồi trong trướng, trên giường của vợ mình, bảo vợ ra bái, rót rượu, gọi Bị là em. Còn Lưu Bị thấy lời Bố chẳng nhất quán, ngoài mặt đồng ý, trong lòng không vui. Ở phía nam là Viên Thuật, phía bắc là Tào Tháo, và ngay trong nhà là Lữ Bố.""",

"""📖 <b>NỘI DUNG TẬP 5 (phần 2/2)</b>

Tào Tháo tâu cho Lưu Bị làm Trấn Đông tướng quân, phong Nghi Thành đình hầu. Cũng năm ấy Viên Thuật đem quân đánh Bị; Bị cự Thuật ở Hu Di và Hoài Âm, hai bên giằng co suốt một tháng. Ở phía sau, trong thành Hạ Bì, người giữ thành là Tào Báo, chính viên tướng của Đào Khiêm từng cùng Lưu Bị đóng quân phía đông Đàm (tập 4).
Sử chép rằng Lữ Bố thừa lúc trống đánh úp Hạ Bì; tướng giữ thành là Tào Báo phản, ngầm đón Bố vào. Bố bắt vợ con Lưu Bị, Bị phải rút quân về Hải Tây. Trong đoạn ấy, sử không nhắc tên Trương Phi và không có chuyện ai say rượu.
Tiểu thuyết lại kể rằng Trương Phi giữ Hạ Bì, uống say, đánh Tào Báo; Báo ôm hận, tự mở cổng; Lữ Bố nhân đó chiếm thành.
<i>Lời kể phụ trong chú giải kể cụ thể hơn:</i> Hứa Đam, một tướng của Bị, ban đêm sai tư mã Chương Cuống tới gặp Bố, báo rằng Trương Phi tranh chấp với Tào Báo, giết Báo, trong thành đại loạn. Một nghìn quân Đan Dương đóng ở cổng tây Bạch Thành nghe Bố tới sẽ mở cổng đón. Bố tiến quân trong đêm, sáng tới chân thành, quân Đan Dương mở hết cổng; Bố ngồi trên cổng, cho bộ kỵ phóng lửa, phá tan quân Phi, bắt cả gia quyến của Bị.
Một bộ sử khác kể cùng chuyện theo thứ tự rõ hơn: Viên Thuật viết thư xúi Bố đánh Hạ Bì; trong thành Phi và Báo bất hòa, Phi giết Báo; rồi Hứa Đam mở cổng đón Bố. Cũng không có chén rượu nào (phần này đọc qua bản dịch, cần kiểm nguyên văn).
Vậy, tiểu thuyết đặt Trương Phi đúng chỗ ấy và cho ông xung đột với Tào Báo; cái nó thêm vào là chén rượu, và chuyện Báo ôm hận rồi tự mở cổng. Theo sử, người làm mất Từ Châu không phải một người say, mà là một châu bị kẹp giữa hai phía, và bên trong có người chọn mở cửa.

Lưu Bị cầu hòa, Bố trả lại vợ con. Bị trở về, Bố cho đóng ở Tiểu Bái, còn mình tự xưng Từ Châu thứ sử. Người từng là chủ giờ phải nương nhờ, người từng được nương nhờ giờ thành chủ.
<i>Lời kể phụ:</i> Viên Thuật gửi thư cho Bố, kể ba công của Bố (giết Trác là báo thù cho Thuật, phá Duyện Châu là rửa nhục cho Thuật, và nhờ uy Bố mà Thuật đánh bại được Lưu Bị) và hứa tặng hai mươi vạn hộc gạo; nói từ khi sinh ra chưa nghe thiên hạ có Lưu Bị. Rồi Thuật sai Kỷ Linh đem ba vạn quân đánh Bị ở Tiểu Bái. Các tướng của Bố nói có thể mượn tay Thuật giết Bị; Bố đáp không được, vì nếu Thuật phá được Bị thì sẽ nối với các tướng Thái Sơn ở phía bắc và Bố nằm trong vòng vây của Thuật. Ông đem một nghìn bộ, hai trăm kỵ phi tới Tiểu Bái, dựng một cây kích ở cổng doanh và nói bắn trúng nhánh nhỏ thì các ông rút quân. Bố bắn trúng; Kỷ Linh thu quân. Đó là cảnh “bắn kích viên môn” nổi tiếng, nhưng nằm trong lời kể phụ, không thuộc đoạn sử chính. Lý do Bố tự nói ra là tính toán của riêng ông, nên tình “anh em” ở đây hẳn cũng có phần tính toán.

Lưu Bị ở Tiểu Bái lại hợp được hơn một vạn quân. Bố ghét điều ấy, tự đem quân đánh; Bị bại, chạy về Tào Tháo. Tháo đãi rất hậu, cho làm Dự Châu mục, cấp lương và thêm quân để đánh Bố.
Trình Dục nói với Tháo rằng Lưu Bị có hùng tài, rất được lòng người, sẽ không chịu dưới ai, nên sớm trừ đi. Tháo đáp: bây giờ là lúc thu nạp anh hùng, giết một người mà mất lòng thiên hạ thì không được.

Tóm lại: Từ Châu không mất vì một chén rượu: Lưu Bị đi cự Viên Thuật suốt một tháng, phía sau bỏ trống, một tướng giữ thành chọn mở cổng, và Lữ Bố thừa lúc ấy. Lữ Bố không cướp Từ Châu từ một người xa lạ mà từ chính người đã cho ông nương nhờ.

<b>Tập sau:</b> cũng trong năm 196, Tào Tháo đón thiên tử từ Lạc Dương đổ nát về Hứa. Vì sao một người vừa nắm trong tay thiên tử lại giữ cạnh mình một người mà chính mưu sĩ của ông nói là không chịu dưới ai?""",

"""🔎 <b>PHẦN NÀO CHẮC, PHẦN NÀO CHƯA (tập 5)</b>

<b>Đã đối chiếu chữ Hán trong Tam quốc chí:</b> Lữ Bố chạy Trường An, bị Viên Thuật từ chối, nương Viên Thiệu rồi Trương Dương; Trương Mạc, Trần Cung đón Bố vào Duyện Châu; Tháo ngã ngựa cháy tay, đại hạn, Cự Dã; Bố “đông bôn Lưu Bị”; Tháo tâu Bị làm Trấn Đông tướng quân; Bố đánh úp Hạ Bì, Tào Báo phản đón Bố; Bị chạy về Tháo; Trình Dục khuyên trừ Bị, Tháo đáp “lúc thu nạp anh hùng”; Tháo đón thiên tử về Hứa.

<b>Từ chú giải của Bùi Tùng Chi (lời kể phụ, không phải chính văn):</b> Lữ Bố đâm Quách Tỵ; Bố thoát khỏi Viên Thiệu bằng đàn tranh; lời Bố nói với Bị và việc ngồi giường vợ; Hứa Đam, Chương Cuống, Trương Phi giết Tào Báo, quân Đan Dương mở cổng; thư Viên Thuật; bắn kích viên môn.

<b>Chưa chắc chắn, cần kiểm nguyên văn:</b> Cách kể thứ tự Phi giết Báo rồi Hứa Đam mở cổng theo một bộ sử khác mới thấy qua bản dịch, chưa thấy nguyên văn Hán. Truyện Trương Phi chưa đọc lại đầy đủ, nên chưa chắc truyện riêng của Phi không có chuyện ở đoạn này. Quân Đan Dương mở cổng ở Hạ Bì có phải chính là bốn nghìn quân Đan Dương Đào Khiêm cho Lưu Bị hay không: chỉ có suy đoán, chưa có nguồn gốc. Chữ 章誑 trong chú giải được hiểu là tên một người (tư mã Chương Cuống), dựa trên các tài liệu thứ cấp.

<b>Ghi chú:</b> Tào Báo (曹豹) là tướng của Đào Khiêm, không phải Tào Tháo (曹操). Hình minh họa chỉ là tranh vẽ; tên và kiểu vũ khí của các tướng là hình tượng của tiểu thuyết.

<b>Nguồn đối chiếu:</b> Tam quốc chí (Vũ Đế kỷ, Lữ Bố truyện kèm Trương Mạc truyện, Tiên chủ truyện) và chú của Bùi Tùng Chi; Tư trị thông giám qua bản dịch.

#TamQuốc #ChínhSử #NgườiGácSử #Tập5""",
    ],
}

# Nội dung thẻ ảnh
CARD = {
    3: {"tieu_de": ["AI THẬT SỰ CHÉM", "HOA HÙNG?"], "phu": "Hổ Lao có thật không?",
        "tt": ["Quan Vũ hâm rượu chém Hoa Hùng", "Ba anh em vây đánh Lữ Bố ở Hổ Lao", "Điêu Thuyền mưu giết Đổng Trác"],
        "su": ["Tôn Kiên chém Hoa Hùng ở Dương Nhân", "Truyện Quan Vũ không có Hoa Hùng, Hổ Lao", "Lữ Bố giết Trác năm 192; truyện Lữ Bố không có Điêu Thuyền"]},
    4: {"tieu_de": ["VÌ SAO TỪ CHÂU", "CHỌN LƯU BỊ?"], "phu": "Có thật “ba lần nhường”?",
        "tt": ["Đào Khiêm ba lần nhường Từ Châu", "Lưu Bị từ chối ba lần vì đức", "Cả châu quỳ xuống van xin"],
        "su": ["Khiêm dặn: ngoài Lưu Bị không ai giữ yên được", "Bị chưa dám nhận; Trần Đăng, Khổng Dung khuyên", "Một cuộc tính toán, sau hai lần đi cứu người"]},
    5: {"tieu_de": ["AI THẬT SỰ LÀM", "MẤT TỪ CHÂU?"], "phu": "Trương Phi có say rượu không?",
        "tt": ["Trương Phi say rượu, đánh Tào Báo", "Lữ Bố nhân đó chiếm Hạ Bì", "Một chén rượu làm mất cơ nghiệp"],
        "su": ["Bị đi cự Viên Thuật một tháng, Bố đánh úp Hạ Bì", "Tướng giữ thành Tào Báo phản, đón Bố", "Sử chính không có tên Phi, không có chén rượu"]},
}

CARD[1] = {"tieu_de": ["LƯU BỊ BÁN", "GIÀY CỎ"], "phu": "Chính sử kể gì về khởi đầu của ông?",
        "tt": ["Ba anh em kết nghĩa vườn đào", "Lời thề sinh tử dưới gốc đào", "Dấy binh từ một lời thề"],
        "su": ["Tam quốc chí không có một chữ về vườn đào", "Quan Vũ, Trương Phi làm hộ vệ, ngủ chung giường", "Tiền nuôi quân từ hai thương nhân buôn ngựa"]}
CARD[2] = {"tieu_de": ["AI ĐÁNH VIÊN", "ĐỐC BƯU?"], "phu": "Lưu Bị lang bạt thế nào trước loạn Đổng Trác",
        "tt": ["Trương Phi đánh đốc bưu", "Ba anh em đánh Lữ Bố ở Hổ Lao"],
        "su": ["Chính Lưu Bị trói và đánh đốc bưu hai trăm gậy", "Tiên chủ truyện không có trận Hổ Lao", "Nhiều năm lang bạt rồi mới có Bình Nguyên"]}
