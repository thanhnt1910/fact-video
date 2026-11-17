import json
# Trận đánh thủy mặc tập 4: Đông Bộ Đầu 1258 (mã tm4)
S=[
(1,"Thua trận, kinh thành sắp mất, nhà vua ngồi trên thuyền hỏi các quan bây giờ phải làm sao."),
(1,"Một người không nói gì, chỉ lấy ngón tay viết lên mạn thuyền hai chữ: sang nhà Tống. Ý là bỏ nước mà chạy."),
(1,"Còn một người khác thì đáp ngược hẳn: đầu thần chưa rơi xuống đất, xin bệ hạ đừng lo."),
(1,"Nhà vua ấy là Trần Thái Tông. Người viết chữ là Trần Nhật Hiệu, còn người nói câu kia là Trần Thủ Độ."),
(1,"Kẻ thù trước mặt họ là quân Mông Cổ. Vậy câu nói ấy là lời hứa thật, hay chỉ là lời trấn an trong lúc nguy?"),
(2,"Lúc ấy, quân Mông Cổ vừa đánh chiếm nước Đại Lý ở Vân Nam, sát biên giới phía tây bắc của Đại Việt."),
(2,"Tướng Mông Cổ đóng ở Vân Nam là Ngột Lương Hợp Thai. Năm một nghìn hai trăm năm mươi bảy, ông sai sứ sang, đòi nhà Trần phải chịu hàng."),
(2,"Nhà Trần không chịu hàng, còn giữ sứ giả lại, và chiến tranh chỉ còn là chuyện sớm muộn."),
(2,"Vì thế, vua Trần Thái Tông sai các tướng thủy bộ ra giữ biên giới, do Trần Quốc Tuấn coi chung. Hai tháng sau, cả nước được lệnh sắm sửa vũ khí."),
(2,"Rồi cuối năm ấy, quân Mông Cổ vượt biên giới, theo dòng sông Thao đánh xuống vùng đồng bằng."),
(3,"Ngày mười hai tháng Chạp năm ấy, quân Mông Cổ tới Bình Lệ Nguyên, cách kinh thành Thăng Long chừng ba mươi cây số về phía tây bắc."),
(3,"Vua Trần Thái Tông tự mình ra trận, có cả voi chiến đi theo. Nhưng trận ấy, quân Đại Việt núng thế."),
(3,"Giữa lúc ấy, chỉ còn tướng Lê Phụ Trần một mình một ngựa xông pha giữa trận. Ông khuyên vua tạm lánh, đừng liều đánh tiếp."),
(3,"Nghe lời ông, vua cho quân lui về sông Lô, rồi xuống giữ sông Thiên Mạc ở phía dưới kinh thành."),
(3,"Thế là kinh thành Thăng Long bị bỏ lại phía sau. Vài ngày sau, quân Mông Cổ kéo vào chiếm thành."),
(3,"Chính trong những ngày ấy, trên thuyền ở sông Thiên Mạc, nhà vua đã hỏi các quan câu hỏi ở đầu câu chuyện."),
(3,"Vua tới thuyền của em mình là Trần Nhật Hiệu, người đang coi việc quân. Ông Nhật Hiệu không đứng dậy, chỉ lấy tay viết hai chữ sang nhà Tống."),
(3,"Rồi vua tới hỏi Trần Thủ Độ, người đứng đầu triều đình. Câu trả lời lần này chỉ có một ý: đầu thần chưa rơi xuống đất, xin bệ hạ đừng lo."),
(3,"Vậy trong tay nhà Trần lúc ấy còn gì để giữ lời hứa đó?"),
(4,"Vẫn còn khá nhiều. Quân Đại Việt thua một trận nhưng chưa tan, và nhà vua vẫn còn đoàn thuyền ở dưới sông."),
(4,"Trong khi ấy, quân Mông Cổ vào được một kinh thành gần như trống không. Chúng tàn phá trong thành, nhưng không tìm được bao nhiêu lương thực."),
(4,"Thêm vào đó, các nhà nghiên cứu cho rằng quân Mông Cổ không quen khí hậu nơi đây, nên ở được ít ngày đã có nhiều người ốm."),
(4,"Họ chiếm được kinh thành, nhưng không bắt được vua, cũng không bắt được triều đình. Mà triều đình thì đang ở ngay dưới sông, chờ lúc ra tay."),
(5,"Ngày hai mươi bốn tháng Chạp, đúng mười hai ngày sau trận thua ở Bình Lệ Nguyên, nhà Trần ra tay."),
(5,"Vua Trần Thái Tông cùng thái tử Trần Hoảng ngồi trên những chiếc thuyền lớn có lầu, đem quân từ sông Thiên Mạc ngược lên phía kinh thành."),
(5,"Thái tử Trần Hoảng khi ấy mới mười bảy tuổi. Mục tiêu của đoàn thuyền là bến Đông Bộ Đầu, ngay sát kinh thành Thăng Long."),
(5,"Bến Đông Bộ Đầu nằm bên sông Hồng, gần chỗ cầu Long Biên ngày nay. Đó là nơi quân Mông Cổ đang đóng."),
(5,"Thế là đoàn thuyền đánh thẳng vào bến. Quân Mông Cổ thua to, bị đánh tan ngay tại Đông Bộ Đầu."),
(5,"Chỉ sau một trận, quân Mông Cổ phải bỏ kinh thành Thăng Long, theo đường cũ rút ngược lên phía Vân Nam."),
(6,"Nhưng đường rút cũng không yên. Đến trại Quy Hóa ở miền núi, chủ trại Hà Bổng gọi người trong vùng ra đánh úp quân Mông Cổ."),
(6,"Vì quân Mông Cổ lần ấy kéo sang rồi rút đi mà không có ý ở lại chiếm đất, người bấy giờ gọi chúng là giặc Phật."),
(6,"Còn Trần Nhật Hiệu, người muốn bỏ nước chạy sang nhà Tống, về sau bị sử gia Ngô Sĩ Liên chê là người nhút nhát, không đáng dùng."),
(6,"Thế là lời của Trần Thủ Độ không chỉ để trấn an. Chỉ mười hai ngày sau trận thua, kinh thành đã được lấy lại."),
(6,"Và đây mới chỉ là lần đầu tiên Đại Việt đánh lui quân Mông Cổ. Gần ba mươi năm sau, họ còn quay lại thêm hai lần nữa."),
(6,"Thua một trận, mất cả kinh thành, nhưng nhà Trần chưa thua cuộc chiến. Cảm ơn bạn đã lắng nghe câu chuyện này."),
]
json.dump([{'n':179001+i,'chuong':c,'tone':'story','text':t,'hien':t} for i,(c,t) in enumerate(S)],open('/tmp/pc/ke-hoach/thu-giong-hai/tm4_full.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
tot=sum(len(t.split()) for c,t in S);acc=0;seen=set()
print(len(S),'đoạn',tot,'chữ ~',round(tot/3.1/60,1),'phút')
for i,(c,t) in enumerate(S):
    if c not in seen: seen.add(c);print('chương',c,'đoạn',i+1,f'{acc/tot:.0%}')
    acc+=len(t.split())
