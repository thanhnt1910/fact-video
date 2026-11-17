import json
# Trận đánh thủy mặc tập 6: Bạch Đằng 1288 (mã tm6)
S=[
(1,"Giặc sắp kéo sang lần thứ ba. Vua hỏi tình hình, vị tướng giỏi nhất nước đáp: năm nay đánh giặc nhàn."),
(1,"Nghe thì như nói cho vua yên lòng. Lần này giặc sang đông hơn, có cả một đoàn thuyền chở lương đi theo đường biển."),
(1,"Rồi kinh thành lại bị bỏ trống, triều đình lại phải lui. Cảnh ấy chẳng có gì giống một cuộc chiến nhàn cả."),
(1,"Người nói câu ấy là Trần Quốc Tuấn, tức Hưng Đạo Đại Vương. Còn kẻ sắp sang là quân nhà Nguyên, mới thua ở Đại Việt ba năm trước."),
(1,"Vậy ông nhìn thấy điều gì mà dám nói nhàn? Câu trả lời nằm ở một đoàn thuyền lương, và ở một con sông cũ."),
(2,"Cuối năm một nghìn hai trăm tám mươi bảy, Thoát Hoan lại dẫn đại quân theo đường bộ tràn qua biên giới phía bắc."),
(2,"Cùng lúc ấy, tướng Ô Mã Nhi dẫn đoàn chiến thuyền vượt biển, tiến vào vùng biển Đông Bắc của Đại Việt."),
(2,"Theo sau Ô Mã Nhi là đoàn thuyền chở lương do Trương Văn Hổ chỉ huy. Đại quân trên bộ trông cả vào số lương ấy."),
(2,"Nhưng Ô Mã Nhi chỉ lo tiến cho nhanh. Ông để đoàn thuyền lương nặng nề đi chậm lại phía sau."),
(3,"Giữ vùng biển Vân Đồn lúc ấy là Phó tướng Trần Khánh Dư. Thoạt đầu, quân của ông đánh không lại đoàn chiến thuyền của Ô Mã Nhi."),
(3,"Chiến thuyền giặc đi qua rồi, đoàn thuyền lương mới tới. Lần này Trần Khánh Dư đánh chặn được, quân giặc tan vỡ ngay tại Vân Đồn."),
(3,"Theo sử cũ, lương thực và khí giới bắt được nhiều không kể xiết. Trương Văn Hổ phải bỏ thuyền, một mình chạy về nước."),
(3,"Trong khi đó, quân giặc trên bộ vẫn tiến về Thăng Long, và kinh thành lại bị bỏ trống thêm một lần."),
(3,"Nhưng chiếm thành xong, quân nhà Nguyên không tìm được lương. Thuyền lương thì không bao giờ tới."),
(4,"Thiếu ăn, quân giặc phải tỏa đi cướp bóc khắp nơi. Ô Mã Nhi còn kéo quân về Long Hưng, phá lăng mộ của vua Trần Thái Tông."),
(4,"Càng đi cướp, quân giặc càng bị đánh úp, càng mỏi mệt. Rồi mùa hè lại sắp tới, mùa mà ba năm trước quân nhà Nguyên đã khổ vì nóng và bệnh."),
(4,"Vì vậy, đầu năm một nghìn hai trăm tám mươi tám, ông quyết định rút. Quân bộ rút theo đường Lạng Sơn, còn đoàn chiến thuyền theo sông Bạch Đằng ra biển."),
(4,"Đúng như Trần Quốc Tuấn đã nhìn thấy: không có lương, đội quân mạnh đến đâu cũng phải tự lui."),
(4,"Còn con sông giặc chọn để rút, chính là sông Bạch Đằng, nơi hơn ba trăm năm trước Ngô Quyền đã đánh tan quân Nam Hán."),
(5,"Trần Quốc Tuấn sai người đóng cọc xuống lòng sông Bạch Đằng, phủ cỏ lên trên. Khi thủy triều lên, nước sẽ phủ kín những hàng cọc ấy."),
(5,"Trước khi ra trận, ông chỉ xuống dòng sông mà thề: trận này không phá xong giặc Nguyên thì không về đến sông này nữa."),
(5,"Ngày mồng tám tháng Ba, đoàn chiến thuyền của Ô Mã Nhi tới khúc sông có cọc. Lúc ấy thủy triều đang lên, mặt nước mênh mông."),
(5,"Một toán thuyền nhỏ của Đại Việt ra khiêu chiến rồi giả thua chạy. Quân giặc đuổi theo, đi sâu vào khúc sông đã chuẩn bị sẵn."),
(5,"Rồi thủy triều rút xuống. Những hàng cọc nhô lên khỏi mặt nước, và thuyền giặc mắc cọc, vỡ, nghiêng ngả khắp lòng sông."),
(5,"Đúng lúc ấy, quân Đại Việt từ hai bên bờ và từ trên sông cùng đổ ra đánh. Thuyền giặc tiến không được, lùi cũng không xong."),
(5,"Ô Mã Nhi bị bắt sống, cùng các tướng Phàn Tiếp, Tích Lệ Cơ. Theo sử cũ, số thuyền giặc bị bắt hơn bốn trăm chiếc."),
(6,"Còn Thoát Hoan đi đường bộ cũng chẳng yên. Trên đường rút về Lạng Sơn, quân giặc liên tục bị chặn đánh và phải chạy trốn qua biên giới."),
(6,"Đó là lần cuối quân nhà Nguyên sang đánh Đại Việt. Hốt Tất Liệt về sau còn tính đánh tiếp, nhưng đến khi mất vẫn không đánh được."),
(6,"Sau chiến tranh, người ta tìm thấy một hòm thư của những người trong triều từng lén liên lạc với giặc."),
(6,"Thượng hoàng Trần Thánh Tông không mở ra xem, sai đốt hết đi, để những người từng dao động được yên lòng."),
(6,"Vậy vì sao Trần Quốc Tuấn dám nói đánh giặc nhàn? Vì đạo quân ấy đánh xa nhà, sống nhờ thuyền lương, mà lương đã mất ở Vân Đồn."),
(6,"Mất lương, quân giặc phải rút, và con đường rút lại đi qua đúng khúc sông có cọc đang chờ. Cảm ơn bạn đã lắng nghe câu chuyện này."),
]
json.dump([{'n':181001+i,'chuong':c,'tone':'story','text':t,'hien':t} for i,(c,t) in enumerate(S)],open('/tmp/pc/ke-hoach/thu-giong-hai/tm6_full.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
tot=sum(len(t.split()) for c,t in S);acc=0;seen=set()
print(len(S),'đoạn',tot,'chữ ~',round(tot/3.1/60,1),'phút')
for i,(c,t) in enumerate(S):
    if c not in seen: seen.add(c);print('chương',c,'đoạn',i+1,f'{acc/tot:.0%}')
    acc+=len(t.split())
