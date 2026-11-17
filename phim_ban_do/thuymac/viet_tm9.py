import json
# Trận đánh thủy mặc tập 9: Rạch Gầm, Xoài Mút 1785 (mã tm9)
S=[
(1,"Năm vạn quân vượt biên giới sang nước ta. Ít tháng sau, số người chạy về được nước chỉ còn vài nghìn."),
(1,"Phần lớn đội quân ấy tan chỉ trong một trận, trên một khúc sông dài chừng sáu, bảy cây số."),
(1,"Đội quân ấy là quân Xiêm, nay là Thái Lan. Người chờ họ trên khúc sông là Nguyễn Huệ, khi đó mới ngoài ba mươi."),
(1,"Còn người mời quân Xiêm sang lại là Nguyễn Ánh, một người nước ta đang tranh giành đất Gia Định với nhà Tây Sơn."),
(1,"Vậy làm sao Nguyễn Huệ khiến cả một đoàn chiến thuyền tự đi vào chỗ chết?"),
(2,"Lúc ấy, nhà Tây Sơn của ba anh em Nguyễn Nhạc, Nguyễn Huệ, Nguyễn Lữ đã mấy lần đánh vào Gia Định. Nguyễn Ánh thua chạy hết lần này đến lần khác."),
(2,"Vì thế, năm một nghìn bảy trăm tám mươi tư, Nguyễn Ánh sang Xiêm cầu cứu. Vua Xiêm nhận lời, sai hai tướng Chiêu Tăng, Chiêu Sương đem quân sang."),
(2,"Theo sử nhà Nguyễn, quân Xiêm có hai vạn thủy binh với ba trăm chiến thuyền, thêm ba vạn quân đi đường bộ."),
(2,"Rồi giữa năm ấy, quân Xiêm tiến vào Rạch Giá. Đến cuối năm, họ đã chiếm nhiều nơi ở miền Tây như Trà Ôn, Sa Đéc, Mân Thít."),
(2,"Nhưng đi tới đâu, quân Xiêm cướp phá tới đó. Chính sử nhà Nguyễn, vốn đứng về phía Nguyễn Ánh, cũng phải chép lại cảnh dân bị hại."),
(3,"Tin dữ về tới Quy Nhơn. Nguyễn Nhạc liền sai em là Nguyễn Huệ đem quân thủy bộ vào nam."),
(3,"Cuối năm ấy theo âm lịch, Nguyễn Huệ tới Gia Định, rồi đóng đại bản doanh ở Mỹ Tho."),
(3,"Quân Xiêm đông hơn nhiều. Vì thế, Nguyễn Huệ không dàn trận đánh thẳng, mà chọn một khúc sông Tiền để đặt bẫy."),
(3,"Đó là khúc sông từ rạch Gầm tới rạch Xoài Mút, giữa dòng có cù lao Thới Sơn che khuất tầm nhìn."),
(3,"Quân bộ và súng đại bác phục sẵn ở hai bờ và trên cù lao. Thuyền chiến thì giấu trong hai con rạch nhỏ, chờ lệnh."),
(4,"Sáng sớm ngày hai mươi tháng Một năm một nghìn bảy trăm tám mươi lăm, đoàn thuyền Xiêm từ Trà Tân xuôi sông Tiền, định đánh vào Mỹ Tho."),
(4,"Chẳng bao lâu, thuyền đi đầu đã tới Rạch Gầm, thuyền đi cuối cũng lọt vào Xoài Mút. Cả đoàn thuyền nằm gọn trong khúc sông đã chọn."),
(4,"Đúng lúc ấy, thuyền Tây Sơn từ hai con rạch lao ra, chặn cả đầu lẫn đuôi đoàn thuyền Xiêm."),
(4,"Từ hai bên bờ và trên cù lao, súng đại bác cùng bắn vào. Thuyền Xiêm bị dồn vào giữa dòng, không còn lối thoát."),
(4,"Thế là thuyền vỡ, thuyền chìm trôi khắp khúc sông. Gần như cả đoàn chiến thuyền Xiêm bị đánh tan ngay trong trận ấy."),
(4,"Kết cục, quân Xiêm chết mấy vạn người. Chiêu Tăng, Chiêu Sương cùng vài nghìn người lên bờ, chạy bộ qua Chân Lạp mà về nước."),
(5,"Nguyễn Ánh cũng phải bỏ chạy, một lần nữa sang nương nhờ đất Xiêm."),
(5,"Theo sử nhà Nguyễn, từ sau trận ấy, người Xiêm ngoài miệng tuy nói cứng, nhưng trong lòng sợ quân Tây Sơn như sợ cọp."),
(5,"Chỉ bốn năm sau, cũng chính Nguyễn Huệ đem quân ra bắc, đánh tan quân nhà Thanh ở Ngọc Hồi, Đống Đa."),
(5,"Vậy Nguyễn Huệ đã làm gì để đoàn chiến thuyền ấy tự đi vào chỗ chết? Ông không ra đón địch, mà chờ ở đúng khúc sông chúng phải đi qua."),
(5,"Năm vạn quân sang, chỉ vài nghìn người về được, vì khúc sông Rạch Gầm, Xoài Mút đã chờ sẵn họ. Cảm ơn bạn đã lắng nghe câu chuyện này."),
]
json.dump([{'n':184001+i,'chuong':c,'tone':'story','text':t,'hien':t} for i,(c,t) in enumerate(S)],open('/tmp/pc/ke-hoach/thu-giong-hai/tm9_full.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
tot=sum(len(t.split()) for c,t in S);acc=0;seen=set()
print(len(S),'đoạn',tot,'chữ ~',round(tot/3.1/60,1),'phút')
for i,(c,t) in enumerate(S):
    if c not in seen: seen.add(c);print('chương',c,'đoạn',i+1,f'{acc/tot:.0%}')
    acc+=len(t.split())
