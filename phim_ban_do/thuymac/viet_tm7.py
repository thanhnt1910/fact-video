import json
# Trận đánh thủy mặc tập 7: Tốt Động, Chúc Động 1426 (mã tm7)
S=[
(1,"Mấy vạn quân giặc đang chờ một tiếng súng hiệu. Hễ súng nổ, tất cả sẽ cùng ập vào một toán quân nhỏ phía trước."),
(1,"Nhưng tiếng súng ấy không vang lên. Đội quân đông gấp nhiều lần cứ thế bước vào giữa một vùng ruộng lầy im phăng phắc."),
(1,"Đó là trận Tốt Động, Chúc Động. Một bên là quân nhà Minh của tướng Vương Thông, một bên là nghĩa quân Lam Sơn."),
(1,"Đội quân ấy sang để giữ lấy đất nước ta cho nhà Minh. Rồi chính họ lại phải chạy vào thành Đông Quan mà trốn."),
(1,"Vậy ai đã giữ cho tiếng súng hiệu ấy không bao giờ nổ?"),
(2,"Năm một nghìn bốn trăm linh bảy, nhà Minh chiếm nước ta, đổi tên thành quận Giao Chỉ và đặt quan cai trị."),
(2,"Rồi mười một năm sau, Lê Lợi dựng cờ khởi nghĩa ở Lam Sơn, Thanh Hóa. Những năm đầu, nghĩa quân nhiều lần bị vây và phải rút lên núi."),
(2,"Đến năm một nghìn bốn trăm hai mươi sáu, nghĩa quân đã làm chủ từ Nghệ An trở vào. Lê Lợi bắt đầu đưa quân ra bắc."),
(2,"Vì thế, một cánh quân nhỏ do Lý Triện, Đỗ Bí chỉ huy tiến sát thành Đông Quan, tức Thăng Long. Ở Ninh Kiều, họ giết được khoảng hai nghìn quân giặc."),
(2,"Thấy nguy, nhà Minh vội sai tướng Vương Thông đem thêm năm vạn quân sang. Gộp với quân đóng sẵn, sử ta chép Vương Thông có tới mười vạn người."),
(3,"Có quân đông trong tay, Vương Thông chia làm ba đường, kéo ra khỏi thành Đông Quan, nhắm vào cánh quân nhỏ của Lý Triện."),
(3,"Lý Triện giả thua, lui qua cầu Tam La vào một vùng ruộng lầy. Quân nhà Minh đuổi theo và sa xuống bùn, rồi bị phục binh đổ ra đánh."),
(3,"Nhưng quân nhà Minh vẫn còn rất đông. Họ dựng hàng rào chông tre, và voi chiến của nghĩa quân giẫm phải chông, quay đầu chạy loạn."),
(3,"Thế trận nguy dần, nên Lý Triện và Đỗ Bí phải gửi tin xin cứu viện gấp."),
(3,"Đinh Lễ và Nguyễn Xí lập tức đem ba nghìn quân cùng hai con voi đến tiếp sức. Dù vậy, quân Lam Sơn vẫn ít hơn giặc nhiều lần."),
(4,"Đúng lúc ấy, nghĩa quân bắt được mấy tên do thám của giặc. Từ miệng chúng, kế hoạch của Vương Thông lộ ra hết."),
(4,"Vương Thông đóng quân ở Ninh Kiều. Ông định cho quân chính vượt sông đánh thẳng vào, còn một cánh khác lén vòng ra sau lưng nghĩa quân."),
(4,"Ám hiệu là tiếng súng. Hễ nghe súng nổ, cả đạo quân cùng xông vào, dồn tên bắn vào trận của nghĩa quân."),
(4,"Biết vậy, Đinh Lễ và Lý Triện ra lệnh cho quân giữ im lặng tuyệt đối. Họ phục sẵn ở Tốt Động và Chúc Động, hai làng ven cánh đồng lầy."),
(5,"Quân nhà Minh đi tới, không nghe súng nổ, cũng không thấy bóng người. Họ cho rằng quanh đó không có quân Lam Sơn, liền đi tắt cho nhanh."),
(5,"Nhưng con đường tắt ấy dẫn thẳng vào giữa ruộng lầy, nơi phục binh đã chờ sẵn ở cả hai bên."),
(5,"Lập tức, phục binh đổ ra từ hai làng. Quân nhà Minh bị kẹp giữa, chạy dồn về phía sông, rất nhiều người chết đuối."),
(5,"Hai viên quan lớn của nhà Minh là Trần Hiệp và Lý Lượng đều chết trong trận này."),
(5,"Vương Thông cũng bị thương, phải cùng tàn quân chạy ngược về thành Đông Quan."),
(5,"Theo sử ta, quân nhà Minh chết và bị bắt mấy vạn người. Sử nhà Minh chép ít hơn, nhưng cũng nhận hai, ba vạn người chết."),
(6,"Sau trận, khí giới, ngựa và lương thực bỏ lại đầy đồng, nghĩa quân thu được rất nhiều."),
(6,"Nghe tin thắng lớn, Lê Lợi kéo đại quân từ Nghệ An ra bắc, vây chặt thành Đông Quan."),
(6,"Thế là đội quân sang để giữ đất lại bị nhốt trong thành. Từ đây, Vương Thông chỉ còn trông vào quân cứu viện từ phương bắc."),
(6,"Về sau, trong Bình Ngô đại cáo, Nguyễn Trãi nhắc lại cảnh xác giặc phơi đầy cánh đồng Tốt Động."),
(6,"Còn tiếng súng hiệu kia không nổ, vì những người lính Lam Sơn đã biết trước và nằm im giữa ruộng lầy, chờ giặc tự bước vào."),
(6,"Biết trước kế của giặc, quân ít đã thắng quân đông ở Tốt Động, Chúc Động. Cảm ơn bạn đã lắng nghe câu chuyện này."),
]
json.dump([{'n':182001+i,'chuong':c,'tone':'story','text':t,'hien':t} for i,(c,t) in enumerate(S)],open('/tmp/pc/ke-hoach/thu-giong-hai/tm7_full.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
tot=sum(len(t.split()) for c,t in S);acc=0;seen=set()
print(len(S),'đoạn',tot,'chữ ~',round(tot/3.1/60,1),'phút')
for i,(c,t) in enumerate(S):
    if c not in seen: seen.add(c);print('chương',c,'đoạn',i+1,f'{acc/tot:.0%}')
    acc+=len(t.split())
