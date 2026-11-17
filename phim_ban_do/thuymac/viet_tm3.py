import json
# Trận đánh thủy mặc tập 3: sông Như Nguyệt 1077 (mã tm3)
S=[
(1,"Một cây cầu phao vừa nối hai bờ sông. Quân giặc lập tức tràn sang bờ nam, mở đường tiến về kinh thành."),
(1,"Phía sau họ là mười vạn quân đang chờ vượt sông. Kinh thành chỉ còn cách đó vài chục cây số."),
(1,"Vậy mà đạo quân đông như thế, cuối cùng vẫn không qua nổi dòng sông này."),
(1,"Điều gì đã xảy ra trên dòng sông này? Và vì sao người đang nắm thế thắng lại chính là người đề nghị thôi đánh?"),
(1,"Đó là sông Như Nguyệt, nay là sông Cầu. Người giữ phòng tuyến bên bờ nam là Lý Thường Kiệt."),
(2,"Một năm trước đó, người vượt biên giới đánh trước lại là quân Đại Việt. Khi ấy, nhà Tống đang gom quân, trữ lương và đóng thuyền ở vùng biên giới."),
(2,"Năm một nghìn không trăm bảy mươi lăm, Lý Thường Kiệt đem quân đánh vào ba châu của nhà Tống. Ung Châu bị vây hơn bốn mươi ngày rồi mới bị hạ."),
(2,"Bị đánh ngay trên đất mình, vua Tống quyết trả đũa. Năm sau, ông giao cho Quách Quỳ làm chủ tướng và Triệu Tiết làm phó, dẫn quân sang đánh Đại Việt."),
(2,"Đạo quân ấy có khoảng mười vạn quân, cùng rất đông dân phu gánh lương đi theo sau."),
(2,"Ngoài biển, nhà Tống còn cho một đoàn thuyền chở quân và lương, hẹn gặp quân bộ để cùng tiến xuống."),
(2,"Kế hoạch ấy rất lớn, nhưng có một chỗ yếu. Nếu đoàn thuyền không tới, quân bộ sẽ rất khó vượt qua những con sông lớn."),
(3,"Và Lý Thường Kiệt đánh đúng vào chỗ yếu ấy. Ông giao cho tướng Lý Kế Nguyên đem thủy quân ra vùng biển Đông Kênh, chặn đoàn thuyền nhà Tống."),
(3,"Hai bên đánh nhau nhiều trận trên biển. Đoàn thuyền nhà Tống bị chặn lại, không tiến sâu được để gặp quân bộ."),
(3,"Thế là lần chặn đầu tiên đã xảy ra ở ngoài biển. Nhưng trên đất liền, Quách Quỳ vẫn tiếp tục tiến quân."),
(3,"Đầu năm một nghìn không trăm bảy mươi bảy, quân nhà Tống vượt biên giới ở Lạng Sơn, vừa đi vừa bị quân Đại Việt chặn đánh."),
(3,"Rồi họ cũng tới bờ bắc sông Như Nguyệt. Từ đây, kinh thành Thăng Long chỉ còn cách vài chục cây số."),
(3,"Nhưng bờ nam không bỏ trống. Lý Thường Kiệt đã cho đắp lũy đất, dựng hàng rào và đặt quân giữ các bến sông."),
(3,"Trước mặt Quách Quỳ là một dòng sông, bên kia là phòng tuyến của Đại Việt. Không cầu, không thuyền, ông sẽ đưa quân qua bằng cách nào?"),
(4,"Quách Quỳ cho quân đóng trại dọc bờ bắc, chờ đoàn thuyền tới. Nhưng chờ mãi, đoàn thuyền vẫn không thấy đâu."),
(4,"Cuối cùng, quân nhà Tống phải tự bắc cầu phao để vượt sông. Đó chính là cây cầu ở đầu câu chuyện."),
(4,"Một toán quân vượt được sang bờ nam, chọc vào phòng tuyến của Đại Việt. Có lúc tưởng như con sông đã bị vượt qua."),
(4,"Nhưng Lý Thường Kiệt lập tức dồn quân phản công. Toán quân ấy bị đánh bật trở lại bờ bắc, theo sử cũ thì chết hơn một nghìn người."),
(4,"Quân nhà Tống còn thử vượt sông thêm lần nữa, nhưng vẫn không qua được. Dòng sông Như Nguyệt đã chặn họ lần thứ hai."),
(4,"Từ đó, Quách Quỳ không cho đại quân vượt sông nữa. Hai bên đóng quân ở hai bờ, nhìn nhau qua một dòng nước."),
(4,"Người đời sau truyền rằng, trong những ngày ấy, từ đền thờ hai anh em Trương Hống, Trương Hát bên bờ nam vang lên một bài thơ."),
(4,"Bài thơ nói sông núi nước Nam là của vua Nam, sách trời đã định sẵn. Kẻ nào dám xâm phạm thì sẽ phải nhận lấy thất bại."),
(4,"Đó là bài thơ Nam quốc sơn hà. Ai là người đọc đầu tiên, đến nay vẫn chưa ai biết chắc."),
(5,"Còn bên bờ bắc, quân nhà Tống bị kẹt lại. Họ không tiến được, mà cũng chưa dễ rút về."),
(5,"Lương mang theo cạn dần. Trời ẩm thấp, bệnh tật lan khắp các trại, người ốm và người chết ngày một nhiều."),
(5,"Đúng lúc quân giặc yếu nhất, Lý Thường Kiệt cho quân bất ngờ vượt sông, đánh thẳng vào doanh trại quân nhà Tống."),
(5,"Lần này, trận đánh không còn ở bờ sông mà ở ngay trong trại giặc. Quân nhà Tống thua to, và đó là lần thứ ba họ bị chặn."),
(5,"Phía Đại Việt cũng mất nhiều người. Hai hoàng tử nhà Lý là Hoằng Chân và Chiêu Văn đã tử trận trong những trận giằng co ấy."),
(5,"Đến lúc này, quân và dân phu nhà Tống đã mất quá nửa, rất nhiều người chết vì bệnh. Nhưng trước mặt Đại Việt vẫn là một đạo quân lớn."),
(5,"Lý Thường Kiệt phải chọn. Đánh tiếp cho đến cùng, hay tìm cách kết thúc cuộc chiến?"),
(6,"Ông chọn cách thứ hai. Ông sai người sang gặp Quách Quỳ, đề nghị hai bên thôi đánh và làm hòa."),
(6,"Quách Quỳ nhận lời và rút quân về nước, nhưng vẫn giữ lại châu Quảng Nguyên ở vùng biên giới."),
(6,"Vì sao đang thắng mà ông lại dừng? Sử không chép Lý Thường Kiệt đã nghĩ gì lúc ấy."),
(6,"Nhưng nhà Tống là một nước rất lớn. Thua trận này, họ vẫn có thể đem quân sang đánh trận khác."),
(6,"Còn nếu đánh đến cùng, quân dân Đại Việt cũng sẽ phải chết thêm rất nhiều người."),
(6,"Hai năm sau, nhờ sứ giả sang thương lượng, nhà Tống trả lại châu Quảng Nguyên cho Đại Việt."),
(6,"Mười vạn quân không qua nổi một dòng sông, và người giữ dòng sông ấy đã biết dừng đúng lúc. Cảm ơn bạn đã lắng nghe câu chuyện này."),
]
json.dump([{'n':178001+i,'chuong':c,'tone':'story','text':t,'hien':t} for i,(c,t) in enumerate(S)],open('/tmp/pc/ke-hoach/thu-giong-hai/tm3_full.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
tot=sum(len(t.split()) for c,t in S);acc=0;seen=set()
print(len(S),'đoạn',tot,'chữ ~',round(tot/3.1/60,1),'phút')
for i,(c,t) in enumerate(S):
    if c not in seen: seen.add(c);print('chương',c,'đoạn',i+1,f'{acc/tot:.0%}')
    acc+=len(t.split())
