import json
# Trận đánh thủy mặc tập 3: sông Như Nguyệt 1077 (mã tm3)
S=[
(1,"Cầu phao vừa bắc xong, một toán quân giặc đã tràn sang bờ nam, chọc thủng phòng tuyến chắn đường tới kinh thành."),
(1,"Sau lưng chúng là mười vạn quân đang chờ qua sông. Từ chỗ ấy tới kinh thành Thăng Long chỉ còn vài chục cây số."),
(1,"Đó là sông Như Nguyệt, nay là sông Cầu, và người giữ con sông ấy là Lý Thường Kiệt."),
(1,"Toán quân giặc có giữ nổi bờ nam không? Và vì sao đến cuối cùng, người đang thắng lại là người đề nghị thôi đánh?"),
(2,"Một năm trước đó, người vượt biên giới đánh trước lại là quân Đại Việt. Khi ấy nhà Tống đang gom quân và đóng thuyền ở biên giới."),
(2,"Năm một nghìn không trăm bảy mươi lăm, Lý Thường Kiệt đánh vào ba châu của nhà Tống. Ung Châu bị vây hơn bốn mươi ngày, kho lương bị phá sạch."),
(2,"Bị đánh ngay trên đất mình, nhà Tống quyết trả đũa. Năm sau, vua Tống giao cho tướng Quách Quỳ cầm quân sang đánh Đại Việt."),
(2,"Đi cùng Quách Quỳ là phó tướng Triệu Tiết. Nhà Tống còn hẹn với Chiêm Thành và Chân Lạp, hai nước ở phía nam, cùng đánh vào Đại Việt."),
(2,"Cuối năm ấy, đạo quân nhà Tống kéo sang với khoảng mười vạn quân, một vạn ngựa và hai mươi vạn dân phu gánh lương."),
(2,"Ngoài biển còn một đoàn thuyền chở thêm quân và lương. Theo kế hoạch, đoàn thuyền ấy sẽ gặp quân bộ ở phía trước, giúp quân bộ qua sông."),
(2,"Nhưng kế hoạch ấy có một chỗ yếu. Nếu đoàn thuyền không tới, mười vạn quân trên bộ sẽ bị kẹt lại trước những con sông lớn."),
(3,"Và Lý Thường Kiệt đánh đúng vào chỗ yếu ấy. Ông sai tướng Lý Kế Nguyên đem thủy quân ra biển Đông Kênh, chặn đoàn thuyền nhà Tống."),
(3,"Hai bên đánh nhau nhiều trận trên biển. Đoàn thuyền nhà Tống không tiến sâu được, và rốt cuộc không bao giờ tới được chỗ quân bộ đang chờ."),
(3,"Thế là lần chặn đầu tiên đã xảy ra ở ngoài biển, cách con sông rất xa. Còn trên bộ, mười vạn quân vẫn tiếp tục tiến xuống."),
(3,"Tháng Giêng năm một nghìn không trăm bảy mươi bảy, họ vượt biên giới ở Lạng Sơn, vừa đi vừa bị các toán quân miền núi chặn đánh."),
(3,"Rồi họ tới bờ bắc sông Như Nguyệt, nay là sông Cầu. Từ đây tới kinh thành Thăng Long chỉ còn vài chục cây số."),
(3,"Nhưng bờ nam đã được chuẩn bị từ trước. Quân Đại Việt đắp lũy đất, dựng hàng rào, giữ chặt các bến sông."),
(3,"Không thuyền, không cầu, Quách Quỳ sẽ đưa mười vạn quân qua sông bằng cách nào?"),
(4,"Thoạt đầu, Quách Quỳ cho quân đóng trại dọc bờ bắc để chờ thuyền. Ông đóng ở khúc sông Thị Cầu, còn Triệu Tiết đóng đối diện bến Như Nguyệt."),
(4,"Chờ mãi không thấy thuyền, quân nhà Tống đành tự bắc cầu phao. Đó chính là cây cầu phao ở đầu câu chuyện."),
(4,"Một toán quân vượt sang bờ nam, chọc thủng phòng tuyến và tiến sâu vào trong. Có lúc tưởng như con sông đã bị vượt qua."),
(4,"Nhưng Lý Thường Kiệt dồn quân phản công. Quân nhà Tống bị đánh bật trở lại, theo sử cũ thì chết hơn một nghìn người."),
(4,"Họ còn thử chở quân sang bằng bè, và lần ấy cũng bị đánh lui. Đến đây, con sông đã chặn quân nhà Tống lần thứ hai."),
(4,"Từ đó, Quách Quỳ không cho quân vượt sông nữa. Hai bên đóng quân ở hai bờ, nhìn nhau qua một dòng nước."),
(4,"Người đời sau truyền rằng, trong những ngày ấy, từ đền thờ hai anh em Trương Hống, Trương Hát bên bờ nam vang lên tiếng đọc một bài thơ."),
(4,"Bài thơ nói sông núi nước Nam là của vua Nam, sách trời đã định sẵn. Giặc nào dám đến xâm phạm thì sẽ chuốc lấy thất bại."),
(4,"Ai là người đọc, đến nay không ai biết chắc. Nhưng bài thơ ấy đã được truyền đọc suốt gần một nghìn năm, tới tận hôm nay."),
(5,"Còn bên bờ bắc, quân nhà Tống đứng yên một chỗ mà vẫn mất người mỗi ngày."),
(5,"Lương mang theo cạn dần. Trời ẩm thấp làm bệnh tật lan khắp các trại, người ốm và người chết ngày một nhiều."),
(5,"Đúng lúc quân giặc yếu nhất, Lý Thường Kiệt cho quân bất ngờ vượt sông, đánh thẳng vào doanh trại quân nhà Tống."),
(5,"Quân nhà Tống thua to. Lần thứ ba này, họ bị chặn ngay trong trại của chính mình."),
(5,"Những trận giằng co trên sông cũng làm quân Đại Việt mất nhiều người, trong đó có hai hoàng tử nhà Lý là Hoằng Chân và Chiêu Văn."),
(5,"Đến lúc này, quân và dân phu nhà Tống đã mất quá nửa, rất nhiều người chết vì bệnh."),
(5,"Giặc đã kiệt sức như thế, vậy mà Lý Thường Kiệt lại không đánh nốt. Vì sao?"),
(6,"Ông sai người sang gặp Quách Quỳ, đề nghị hai bên thôi đánh và làm hòa. Quách Quỳ nhận lời, rút quân về nước."),
(6,"Nhưng khi rút, quân nhà Tống vẫn giữ lại châu Quảng Nguyên ở vùng biên giới."),
(6,"Sử không chép Lý Thường Kiệt đã nghĩ gì. Nhưng nhà Tống là một nước rất lớn, thua trận này vẫn có thể đem quân sang trận khác."),
(6,"Còn nếu đánh đến cùng, quân dân Đại Việt cũng sẽ chết thêm rất nhiều. Dừng lại khi đang thắng giúp cuộc chiến sớm kết thúc."),
(6,"Rồi đất cũ cũng được đòi về. Hai năm sau, nhờ sứ giả sang thương lượng, nhà Tống trả lại châu Quảng Nguyên cho Đại Việt."),
(6,"Mười vạn quân không qua nổi một con sông, và người giữ con sông ấy đã biết dừng đúng lúc. Cảm ơn bạn đã lắng nghe câu chuyện này."),
]
json.dump([{'n':178001+i,'chuong':c,'tone':'story','text':t,'hien':t} for i,(c,t) in enumerate(S)],open('/tmp/pc/ke-hoach/thu-giong-hai/tm3_full.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
tot=sum(len(t.split()) for c,t in S);acc=0;seen=set()
print(len(S),'đoạn',tot,'chữ ~',round(tot/3.1/60,1),'phút')
for i,(c,t) in enumerate(S):
    if c not in seen: seen.add(c);print('chương',c,'đoạn',i+1,f'{acc/tot:.0%}')
    acc+=len(t.split())
