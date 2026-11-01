# Gộp: khung 68 đoạn của chủ kênh (hai nước cờ) + chi tiết có nguồn từ bản lt1v5thu. Chạy: python tao_lt1v5hopnhat.py
import json, os, re
C = [
('Hai nước cờ', [
"Một vị tướng đưa quân đánh thẳng vào căn cứ của nhà Tống. Vài tháng sau, ông lại phải chặn chính đạo quân ấy ngay trên đất nước mình.",
"Một lần ra tay trước, một lần giữ vững phòng tuyến. Hai tình thế trái ngược nhau, nhưng cùng mang tên Lý Thường Kiệt.",
"Vì sao ông chọn đánh trước? Và khi quân Tống kéo xuống, ông đã giữ Đại Việt bằng cách nào?",
"Muốn trả lời, ta phải bắt đầu từ một tòa thành nằm bên kia biên giới, trong lãnh thổ của nhà Tống.",
]),
('Người cầm cờ tiết', [
"Các tài liệu thường ghi Lý Thường Kiệt sinh năm một nghìn không trăm mười chín, nhưng có sách ghi năm khác, nên năm sinh của ông chưa thật chắc.",
"Theo Đại Việt sử ký toàn thư, bộ chính sử của nước ta ngày trước, ông quê ở phường Thái Hòa trong thành Thăng Long, nhà nhiều đời làm quan.",
"Thuở nhỏ ông được chọn vào cung hầu vua vì vẻ mặt tươi đẹp. Toàn thư khen ông nhiều mưu lược và có tài làm tướng.",
"Vua Lý Thánh Tông trao cho ông tiết việt, tức là cờ và búa của người thay mặt vua, để đi thăm hỏi dân ở Thanh Hóa và Nghệ An.",
"Mùa xuân năm một nghìn không trăm sáu mươi chín, vua đi đánh Chiêm Thành. Ông làm tướng tiên phong và bắt được vua Chiêm là Chế Củ.",
"Nhờ công ấy ông được phong phụ quốc thái phó. Đến năm một nghìn không trăm bảy mươi lăm, ông giữ chức thái úy, người coi việc quân của cả triều đình.",
]),
('Chờ hay đánh', [
"Đúng lúc ấy, ở phía bắc, nhà Tống có một người nắm quyền đang tính chuyện chiếm nước ta. Đó là Vương An Thạch.",
"Toàn thư chép ông tâu với vua Tống rằng Đại Việt vừa bị Chiêm Thành đánh phá, quân còn lại không đầy một vạn người, nên có thể dùng kế chiếm lấy.",
"Vua Tống cử Thẩm Khởi và Lưu Di làm tri Quế Châu, tức quan đứng đầu một châu sát biên giới. Hai người ngầm gọi người miền núi vào quân ngũ.",
"Họ còn đóng thuyền, tập thủy chiến và cấm các châu huyện buôn bán với Đại Việt, và tin ấy truyền về Thăng Long.",
"Triều Lý đứng trước một câu hỏi khó. Ngồi chờ quân Tống sang, hay ra tay phá thế chuẩn bị của họ trước?",
"Toàn thư chỉ ghi những việc chuẩn bị ấy, không ghi nhà Tống định đánh vào ngày nào. Nên nói rằng quân Tống chắc chắn sắp đánh là đi xa hơn những gì sử chép.",
"Điều chắc hơn là triều Lý đã thấy một mối nguy đang lớn dần ở phía bắc. Họ chọn ra tay trước, và giao việc ấy cho Lý Thường Kiệt cùng Tông Đản.",
"Lời giải thích mà quân Đại Việt nêu ra, theo Toàn thư, là chính sách thanh miêu của nhà Tống. Nhà nước cho dân vay tiền lúc lúa còn non, đến mùa gặt phải trả cả vốn lẫn lãi.",
"Sử không ghi có người dân Tống nào kêu cứu, nên có thể hiểu đó là danh nghĩa cho cuộc tiến quân. Còn ý định thật của triều Lý thì sử không nói rõ.",
]),
('Đánh vào đâu', [
"Cuối năm một nghìn không trăm bảy mươi lăm, quân Đại Việt chia làm hai đạo thủy và bộ. Toàn thư ghi con số hơn mười vạn quân, còn các tài liệu khác ghi thấp hơn nhiều.",
"Lý Thường Kiệt đánh hai châu Khâm và Liêm ở ven biển. Theo bộ Cương mục soạn thời Nguyễn, việc ấy xảy ra vào tháng mười một.",
"Trong khi đó Tông Đản đem quân vây Ung Châu, nay thuộc Quảng Tây. Đây là thành lớn của nhà Tống ở vùng biên giới phía nam.",
"Trương Thủ Tiết, quan coi quân Quảng Tây của nhà Tống, đem quân đến cứu thành. Lý Thường Kiệt đón đánh ở cửa ải Côn Lôn.",
"Toàn thư ghi quân cứu viện bị phá tan và Trương Thủ Tiết bị chém ngay tại trận. Sau trận ấy, không còn đạo quân nào đến cứu Ung Châu.",
"Nhưng chặn được viện binh chưa có nghĩa là lấy được thành. Ung Châu sẽ là nơi thử thách nặng nhất của cả chiến dịch.",
]),
('Bốn mươi ngày bên tường thành', [
"Trong thành, tri châu Tô Giám nhất định không hàng. Quân Đại Việt đánh hơn bốn mươi ngày mà vẫn chưa vào được.",
"Một đạo quân có thể đi rất nhanh qua biên giới, nhưng trước tường thành kiên cố thì tốc độ không còn đủ. Cuộc chiến trở thành cuộc thử sức chịu đựng.",
"Cuối cùng quân Đại Việt chồng những bao đất lên cao như bậc thang, trèo lên mặt thành. Đầu năm một nghìn không trăm bảy mươi sáu, thành bị hạ.",
"Toàn thư ghi rằng không một người nào trong thành chịu hàng, vì cảm nghĩa Tô Giám. Ba mươi sáu người thân của ông chết trước, rồi ông tự đốt mình.",
"Cũng theo Toàn thư, quân Đại Việt giết hơn năm vạn tám nghìn người trong thành. Cộng với Khâm Châu và Liêm Châu, tổng số lên hơn mười vạn.",
"Đó là con số do sử ta chép, chưa được đối chiếu với nguồn khác. Nhưng dù hiểu thế nào, đây cũng là một chiến thắng phải trả giá rất đắt, và nạn nhân có cả dân thường.",
"Sau đó quân Đại Việt bắt người ở ba châu Ung, Khâm, Liêm đem về nước rồi rút đi. Toàn thư không ghi việc đặt quan cai trị ở đó.",
"Vì vậy có thể hiểu chuyến đi nhằm phá thế chuẩn bị của nhà Tống, chứ không để chiếm đất. Đó là cách hiểu từ những gì sử ghi, còn ý định của Lý Thường Kiệt thì sử không nói thẳng.",
"Nước cờ đánh trước đã xong. Nhưng nhà Tống sẽ không để yên, và nước cờ tiếp theo của Lý Thường Kiệt sẽ khó hơn nhiều.",
]),
('Giữ sông bằng gì', [
"Năm một nghìn không trăm bảy mươi sáu, vua Tống cử Quách Quỳ làm tướng chỉ huy, Triệu Tiết làm phó. Hai người đem quân của chín tướng xuống phía nam.",
"Toàn thư còn chép rằng quân Tống hợp với Chiêm Thành và Chân Lạp để đánh sang. Sử chỉ ghi một câu ngắn, không nói hai nước ấy đã làm gì.",
"Đầu năm một nghìn không trăm bảy mươi bảy, quân Tống đến bờ bắc sông Như Nguyệt, tức sông Cầu ngày nay. Theo các nhà nghiên cứu hiện đại, thủy quân của họ chưa đến kịp.",
"Lần này thế chủ động đã đổi chiều. Quân Tống là bên tiến sang, còn Lý Thường Kiệt phải chọn nơi để chặn họ.",
"Vì sao ông chọn một dòng sông? Vì sông rộng chia cắt đội hình, quân muốn sang phải tìm cách vượt qua dưới tầm đánh của đối phương.",
"Theo hai nhà sử học Keith Taylor và John Anderson, ông cho đắp lũy đất và dựng hàng rào tre dọc bờ nam. Toàn thư cũng chép lời truyền rằng ông làm hàng rào dọc sông để cố thủ.",
"Lần đầu, vài trăm quân Tống qua được sông thì cầu phao bị đốt, và họ không phá nổi hàng rào tre. Lần thứ hai, họ gặp cọc cắm dưới lòng sông.",
"Toàn thư ghi quân Đại Việt đánh tan quân Tống ở sông Như Nguyệt, quân Tống chết hơn một nghìn người. Kế hoạch tiến sâu của họ không thể diễn ra như dự tính.",
"Nhưng đây không phải chuỗi thắng liên tục. Theo Taylor và Anderson, sau khoảng một tháng giằng co, đợt đánh đêm của Lý Thường Kiệt vào trại quân Tống không thành.",
"Khi một đạo quân không vượt nổi chướng ngại, thời gian bắt đầu làm khó họ. Càng kéo dài, áp lực về lương thực và sức khỏe quân sĩ càng lớn.",
]),
('Bài thơ bên sông', [
"Giữa những ngày ấy, người ta nhắc đến một bài thơ gắn với sông Như Nguyệt. Sử ghi chuyện này theo hai cách khác nhau.",
"Toàn thư chép lời người đời truyền rằng đêm nọ, quân sĩ nghe tiếng đọc thơ vang lên trong đền thờ tướng họ Trương. Bài thơ nói sông núi nước Nam đã có vua nước Nam ở, được định sẵn trong sách trời.",
"Bài thơ còn nói kẻ nào sang xâm phạm thì sẽ thất bại. Đó là bài Nam quốc sơn hà.",
"Còn sách Thiền uyển tập anh, viết hơn hai thế kỷ sau, kể rằng chính Lý Thường Kiệt đọc bài thơ ấy để nâng sĩ khí vào cuối tháng hai.",
"Cả hai cách kể đều được chép rất lâu sau trận đánh. Vì vậy bài thơ là điều được truyền lại, chưa phải điều đã được chứng minh.",
"Dù ra đời thế nào, Nam quốc sơn hà vẫn trở thành biểu tượng của ý thức độc lập. Một phòng tuyến dựng bằng đất, tre và quân lính, nhưng người giữ nó còn cần biết mình đang bảo vệ điều gì.",
]),
('Khi nào thì dừng', [
"Chiến tranh không chỉ được quyết định bằng những trận đánh. Quân Tống vượt sông nhiều lần không được, lại hao dần trong khí hậu nóng ẩm.",
"Theo John Anderson và George Cœdès, sử Trung Quốc đổ cho khí hậu và bệnh tật. Nhà sử học Ben Kiernan ước tính quân Tống mất khoảng một nửa đến ba phần năm lực lượng trước khi rút.",
"Đó là ước tính hiện đại, không phải con số do sử thời ấy ghi. Nhưng quân Đại Việt cũng không thể đánh mãi, vì chiến trường nằm sát kinh thành.",
"Vậy khi đã chặn được đối phương, nên đánh tiếp hay tìm đường kết thúc chiến tranh? Nếu đánh tiếp, tổn thất sẽ còn lớn. Nếu dừng quá sớm, thắng lợi có thể không đổi thành hòa bình có lợi.",
"Toàn thư chỉ chép gọn rằng Quách Quỳ lui quân và lấy châu Quảng Nguyên của Đại Việt. Việc ai là người đề nghị hòa không có trong đoạn ấy.",
"Nhà sử học John Anderson ghi rằng chính Lý Thường Kiệt đề nghị hòa năm một nghìn không trăm bảy mươi bảy, vì lo chiến tranh kéo dài sát kinh thành. Đó là lý giải của người nghiên cứu, không phải lời ông tự nói.",
"Quách Quỳ đồng ý rút quân, nhưng giữ lại một số châu miền núi, trong đó Toàn thư nêu tên Quảng Nguyên và Tô Mậu. Vì thế việc đất đai chưa xong.",
]),
('Đòi lại đất', [
"Chiến sự đã dừng, và nhà Lý quay sang một mặt trận khác là đường ngoại giao. Ở đó, mọi thứ phải đổi bằng lễ vật và lời nói.",
"Đầu năm một nghìn không trăm bảy mươi tám, nhà Lý sai Đào Tống Nguyên mang năm con voi thuần sang biếu nhà Tống. Kèm theo là lời xin trả lại các châu Quảng Nguyên, Tô Mậu và những người dân bị bắt đi.",
"Năm một nghìn không trăm bảy mươi chín, Toàn thư ghi nhà Tống trả lại Quảng Nguyên nhưng đổi tên châu này thành Thuận Châu.",
"Hai năm sau, nhà Lý đáp lại bằng việc trả dân và lính bị bắt ở ba châu Ung, Khâm, Liêm, vì nhà Tống đã trả Quảng Nguyên.",
"Năm một nghìn không trăm tám mươi tư, Toàn thư ghi Lê Văn Thịnh đến trại Vĩnh Bình bàn việc cương giới với người nhà Tống. Nhiều tài liệu sau này ghi nhà Tống trả thêm một số huyện và động, nhưng con số cụ thể còn cần đối chiếu.",
"Ở Như Nguyệt, Lý Thường Kiệt phải giữ một dòng sông. Trên bàn thương lượng, triều Lý phải giữ lại những vùng đất thuộc về mình, và việc ấy mất nhiều năm.",
]),
('Những năm cuối', [
"Sau chiến tranh, Lý Thường Kiệt vẫn giữ chức thái úy. Vua còn giao cho ông việc dẹp loạn trong nước.",
"Mùa đông năm một nghìn một trăm linh ba, Toàn thư ghi vua sai ông đánh Lý Giác, người nổi loạn ở Diễn Châu. Lý Giác thua và chạy sang Chiêm Thành.",
"Năm sau, vua Chiêm Thành là Chế Ma Na lấy lại ba châu mà Chế Củ từng dâng cho Đại Việt. Lý Thường Kiệt lại đem quân đi đánh, phá được quân Chiêm Thành, và Chế Ma Na phải dâng nộp lại đất ấy.",
"Tháng sáu năm một nghìn một trăm linh năm, thái úy Lý Thường Kiệt mất, khi tuổi đã cao mà vẫn còn gánh việc quân của triều đình.",
]),
('Trở lại bên sông', [
"Ta trở lại câu hỏi ban đầu. Những yếu tố nào đã đưa cuộc chiến đến thương lượng, theo những gì sử ghi lại?",
"Yếu tố thứ nhất là đòn đánh trước, gồm trận chặn viện binh ở Côn Lôn và việc hạ Ung Châu. Có thể hiểu đó là cách làm rối thế chuẩn bị của nhà Tống, theo những gì Toàn thư ghi.",
"Yếu tố thứ hai là phòng tuyến Như Nguyệt, nơi Toàn thư ghi quân Tống chết hơn một nghìn người. Các nhà nghiên cứu ghi thêm rằng quân Tống không phá nổi hàng rào bờ nam.",
"Yếu tố thứ ba là sự hao tổn của cả hai phía, khi bệnh tật và chiến trường sát kinh thành làm cuộc chiến ngày càng khó kéo dài.",
"Ba yếu tố ấy không chứng minh Lý Thường Kiệt đã tính trước từng bước. Sử chỉ cho thấy chúng cùng có mặt, còn yếu tố nào nặng hơn thì các nhà nghiên cứu vẫn bàn.",
"Một người, hai nước cờ, một lần đánh trước và một lần giữ sông, rồi đổi thắng lợi quân sự lấy thương lượng. Cảm ơn bạn đã lắng nghe câu chuyện này.",
]),
]
def chia(t):
    ss=[x for x in re.split(r'(?<=[.!?])\s+', t) if x]
    if len(t.split())<=32 and len(ss)<=2: return [t]
    r=[]; cur=''
    for x in ss:
        if cur and (len((cur+' '+x).split())>32 or len(re.split(r'(?<=[.!?])\s+',cur+' '+x))>2): r.append(cur); cur=x
        else: cur=(cur+' '+x).strip()
    r.append(cur); return r
out=[]; n=31001
for ch, ds in C:
    for t in [y for d in ds for y in chia(d)]:
        out.append({'n':n,'chuong':ch,'tone':'story','text':t}); n+=1
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'lt1v5hopnhat_full.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(len(out))
