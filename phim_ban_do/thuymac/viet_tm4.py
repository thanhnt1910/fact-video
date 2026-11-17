import json
# Trận đánh thủy mặc tập 4: Đông Bộ Đầu 1258 (mã tm4)
S=[
(1,"Thua trận, kinh thành sắp mất, nhà vua ngồi trên thuyền hỏi các quan bây giờ phải làm sao."),
(1,"Một người không nói gì, chỉ lấy ngón tay viết lên mạn thuyền hai chữ: sang nhà Tống. Ý là bỏ nước mà chạy."),
(1,"Còn một người khác thì đáp ngược hẳn: đầu thần chưa rơi xuống đất, xin bệ hạ đừng lo."),
(1,"Nhà vua ấy là Trần Thái Tông. Người viết chữ là Trần Nhật Hiệu, còn người nói câu kia là Trần Thủ Độ."),
(1,"Kẻ thù trước mặt họ là quân Mông Cổ. Vậy câu nói ấy là lời hứa thật, hay chỉ là lời trấn an trong lúc nguy?"),
(2,"Mấy tháng trước đó, mối nguy đến từ phía tây bắc. Quân Mông Cổ vừa đánh chiếm nước Đại Lý ở Vân Nam, ngay sát biên giới Đại Việt."),
(2,"Tướng Mông Cổ đóng ở đó là Ngột Lương Hợp Thai. Năm một nghìn hai trăm năm mươi bảy, ông sai sứ sang Thăng Long, đòi nhà Trần chịu hàng."),
(2,"Nhà Trần không hàng, còn giữ sứ giả lại. Làm vậy là đã chọn đánh, nên cả nước bắt đầu chuẩn bị."),
(2,"Vì thế, quân thủy và quân bộ được đưa lên giữ biên giới, do Trần Quốc Tuấn chỉ huy. Ông chính là Hưng Đạo Đại Vương sau này."),
(2,"Ít lâu sau, cả nước được lệnh sắm vũ khí. Nhưng cuối năm ấy, quân Mông Cổ vẫn tràn qua biên giới, theo dòng sông Thao đánh xuống."),
(3,"Đến ngày mười hai tháng Chạp, họ đã tới Bình Lệ Nguyên, chỉ còn cách kinh thành Thăng Long chừng ba mươi cây số."),
(3,"Vua Trần Thái Tông tự mình dẫn quân ra chặn, có cả voi chiến đi theo. Nhưng trận ấy, quân Đại Việt yếu thế dần."),
(3,"Cuối cùng, chỉ còn tướng Lê Phụ Trần một mình một ngựa xông pha giữa trận. Ông khuyên vua tạm lánh, đừng liều đánh tiếp."),
(3,"Vua nghe theo, cho quân rút về sông Lô, rồi lui xuống giữ sông Thiên Mạc ở phía dưới kinh thành."),
(3,"Kinh thành vì thế bị bỏ trống. Chỉ vài ngày sau, quân Mông Cổ kéo vào chiếm thành."),
(3,"Đó chính là lúc nhà vua ngồi trên thuyền ở sông Thiên Mạc, hỏi các quan câu hỏi ở đầu câu chuyện."),
(3,"Người đầu tiên vua tìm đến là em mình, Trần Nhật Hiệu, người đang coi việc quân. Ông không đứng dậy, chỉ lấy tay viết hai chữ sang nhà Tống."),
(3,"Nghe vậy, vua tìm đến Trần Thủ Độ, người đứng đầu triều đình. Và câu trả lời lần này là: đầu thần chưa rơi xuống đất, xin bệ hạ đừng lo."),
(3,"Nói thì dễ. Nhưng kinh thành đã mất, vậy nhà Trần lấy gì để giữ lời hứa ấy?"),
(4,"Nhà Trần chỉ thua một trận, chứ chưa mất quân. Nhà vua vẫn còn đoàn thuyền và quân lính ở dưới sông Thiên Mạc."),
(4,"Còn quân Mông Cổ thì chiếm được kinh thành, nhưng trong thành gần như không còn ai. Họ tàn phá, nhưng không tìm được bao nhiêu lương thực."),
(4,"Các nhà nghiên cứu cho rằng quân Mông Cổ cũng không quen khí hậu nơi đây. Ở được ít ngày, nhiều người đã bắt đầu ốm."),
(4,"Thế là kẻ chiếm thành lại thành kẻ bị kẹt trong thành. Còn triều đình nhà Trần thì vẫn ở ngay dưới sông, chờ lúc ra tay."),
(5,"Ngày ra tay là hai mươi bốn tháng Chạp, đúng mười hai ngày sau trận thua ở Bình Lệ Nguyên."),
(5,"Vua Trần Thái Tông cùng thái tử Trần Hoảng, khi ấy mới mười bảy tuổi, ngồi trên những chiếc thuyền lớn có lầu, dẫn quân ngược sông lên phía kinh thành."),
(5,"Đoàn thuyền nhắm thẳng vào bến Đông Bộ Đầu bên sông Hồng, gần chỗ cầu Long Biên ngày nay. Đó là nơi quân Mông Cổ đang đóng."),
(5,"Thế là quân Đại Việt đánh thẳng vào bến. Quân Mông Cổ thua to, bị đánh tan ngay tại Đông Bộ Đầu."),
(5,"Chỉ sau một trận, kinh thành được lấy lại. Quân Mông Cổ phải theo đường cũ, rút ngược lên phía Vân Nam."),
(6,"Nhưng đường rút cũng không yên. Đến trại Quy Hóa ở miền núi, chủ trại Hà Bổng gọi người trong vùng ra đánh úp quân Mông Cổ thêm một trận."),
(6,"Lần ấy quân Mông Cổ kéo sang rồi rút đi, không ở lại chiếm đất, nên người bấy giờ gọi chúng là giặc Phật."),
(6,"Còn Trần Nhật Hiệu, người từng muốn bỏ nước chạy sang nhà Tống, về sau bị sử gia Ngô Sĩ Liên chê là nhút nhát, không đáng dùng."),
(6,"Như vậy, lời của Trần Thủ Độ đã thành sự thật. Mười hai ngày sau trận thua, kinh thành đã trở về tay nhà Trần."),
(6,"Đó mới là lần đầu tiên Đại Việt đánh lui quân Mông Cổ. Gần ba mươi năm sau, họ còn quay lại thêm hai lần nữa."),
(6,"Thua một trận, mất cả kinh thành, nhưng nhà Trần chưa thua cuộc chiến. Cảm ơn bạn đã lắng nghe câu chuyện này."),
]
json.dump([{'n':179001+i,'chuong':c,'tone':'story','text':t,'hien':t} for i,(c,t) in enumerate(S)],open('/tmp/pc/ke-hoach/thu-giong-hai/tm4_full.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
tot=sum(len(t.split()) for c,t in S);acc=0;seen=set()
print(len(S),'đoạn',tot,'chữ ~',round(tot/3.1/60,1),'phút')
for i,(c,t) in enumerate(S):
    if c not in seen: seen.add(c);print('chương',c,'đoạn',i+1,f'{acc/tot:.0%}')
    acc+=len(t.split())
