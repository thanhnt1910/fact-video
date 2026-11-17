import json
# Trận đánh thủy mặc tập 8: Chi Lăng, Xương Giang 1427 (mã tm8)
S=[
(1,"Một đạo quân năm vạn người đang tiến sang, bỗng quay đầu bỏ chạy dù chưa đánh trận lớn nào."),
(1,"Thứ khiến họ sợ không phải gươm giáo, mà là mấy lá thư và chiếc ấn của một người vừa chết."),
(1,"Đạo quân ấy là quân nhà Minh do Mộc Thạnh cầm đầu. Người vừa chết là Liễu Thăng, chủ tướng một đạo quân khác còn lớn hơn."),
(1,"Cả hai được gửi sang để cứu một đạo quân nhà Minh khác, đang bị vây chặt trong thành Đông Quan."),
(1,"Vậy chuyện gì đã xảy ra với Liễu Thăng, khiến chỉ mấy lá thư cũng đủ đuổi cả một đạo quân?"),
(2,"Đạo quân bị vây ấy là của Vương Thông. Cuối năm một nghìn bốn trăm hai mươi sáu, ông bị nghĩa quân Lam Sơn vây ở Đông Quan, tức Thăng Long."),
(2,"Nhà Minh bèn sai hai đạo quân sang cứu. Liễu Thăng đem mười vạn quân và hai vạn ngựa, theo đường Lạng Sơn kéo xuống."),
(2,"Cùng lúc ấy, Mộc Thạnh đem năm vạn quân theo đường Vân Nam tiến sang, nhắm cùng hội ở Đông Quan."),
(2,"Các tướng Lam Sơn muốn đánh ngay thành Đông Quan. Lê Lợi không chịu, vì đánh vào thành vững là cách kém nhất, chi bằng giữ sức chờ quân cứu viện."),
(2,"Vì thế, ông chọn đánh Liễu Thăng trước. Đạo quân lớn nhất mà tan, thì đạo quân kia khó lòng đứng vững."),
(3,"Rồi ở cửa ải đầu tiên, tướng Trần Lựu đánh vài trận rồi lui dần, lui mãi về tận ải Chi Lăng."),
(3,"Ải Chi Lăng là một thung lũng hẹp, hai bên là núi đá, giữa là đường đi và đầm lầy. Nghĩa quân đã phục sẵn ở đó."),
(3,"Thắng mấy trận đầu, Liễu Thăng sinh lòng khinh địch. Thấy quân Lam Sơn cứ lui, ông càng đuổi gấp hơn."),
(3,"Đến ngày hai mươi tháng Chín, ông chỉ đem hơn một trăm kỵ binh vượt lên trước, tới chân núi Mã Yên."),
(3,"Đúng lúc ấy, phục binh từ bốn phía đổ ra. Liễu Thăng bị giết ngay tại chỗ, trong khi đại quân của ông còn ở phía sau."),
(4,"Mất chủ tướng, đạo quân mười vạn người vẫn cố tiến về phía Đông Quan, nhưng đi đến đâu cũng bị chặn đánh."),
(4,"Chỉ năm ngày sau, tướng Lương Minh tử trận. Thêm ba ngày nữa, Thượng thư Lý Khánh cũng tự tử."),
(4,"Còn hai tướng Thôi Tụ và Hoàng Phúc dẫn quân tới thành Xương Giang, mong có chỗ dựa."),
(4,"Nhưng thành Xương Giang đã bị nghĩa quân hạ từ trước đó ít lâu. Quân nhà Minh đành đóng trại giữa cánh đồng trống."),
(4,"Thế là nghĩa quân vây chặt bốn mặt, cắt đường lấy lương. Đến tháng Mười, họ đánh vào, bắt sống cả Thôi Tụ lẫn Hoàng Phúc."),
(5,"Lúc ấy Mộc Thạnh đã vào tới vùng Lê Hoa, gần biên giới Vân Nam, và vẫn đóng quân chờ tin."),
(5,"Theo sử cũ, Lê Lợi sai đem những thư từ và ấn tín lấy được của Liễu Thăng đến cho Mộc Thạnh xem."),
(5,"Thấy thư và ấn của Liễu Thăng nằm trong tay đối phương, Mộc Thạnh biết đạo quân kia đã tan, liền bỏ chạy về nước."),
(5,"Nghĩa quân đuổi theo và đánh tan quân của Mộc Thạnh trên đường rút. Chính ông chỉ kịp chạy thoát thân."),
(6,"Hết hy vọng cứu viện, Vương Thông trong thành Đông Quan đành xin giảng hòa."),
(6,"Tháng Chạp năm ấy, hai bên làm lễ thề ở phía nam thành Đông Quan. Lê Lợi cho quân nhà Minh về nước, còn cấp cả thuyền và ngựa."),
(6,"Đầu năm sau, Nguyễn Trãi viết Bình Ngô đại cáo, nhắc lại từng ngày của chiến dịch này, từ Chi Lăng, Mã Yên đến Xương Giang."),
(6,"Còn mấy lá thư ở đầu câu chuyện có sức mạnh như vậy, là vì chúng chứng minh một điều: Liễu Thăng đã chết ở Mã Yên."),
(6,"Giết một chủ tướng ở Chi Lăng, nghĩa quân Lam Sơn đã đánh sập cả hai đạo quân cứu viện. Cảm ơn bạn đã lắng nghe câu chuyện này."),
]
json.dump([{'n':183001+i,'chuong':c,'tone':'story','text':t,'hien':t} for i,(c,t) in enumerate(S)],open('/tmp/pc/ke-hoach/thu-giong-hai/tm8_full.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
tot=sum(len(t.split()) for c,t in S);acc=0;seen=set()
print(len(S),'đoạn',tot,'chữ ~',round(tot/3.1/60,1),'phút')
for i,(c,t) in enumerate(S):
    if c not in seen: seen.add(c);print('chương',c,'đoạn',i+1,f'{acc/tot:.0%}')
    acc+=len(t.split())
