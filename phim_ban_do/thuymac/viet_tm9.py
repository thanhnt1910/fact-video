import sys,os;sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)));sys.path.insert(0,'/tmp/gen');from viet_chung import xuat2
# Thủy mặc tập 9: Rạch Gầm, Xoài Mút 1785 (mã tm9), bản 4 theo mẫu tm5
S=[
('hook1',"Nếu đang thua trên chính đất của mình, bạn có mời quân của một nước khác vào đánh giúp không?"),
('hook2',"Năm ấy có một người đã mời. Nguyễn Ánh, cháu các chúa Nguyễn, thua quân nhà Tây Sơn liên tiếp, nên sang nước Xiêm, nay là Thái Lan, xin quân."),
('hook3',"Mấy vạn quân nước Xiêm kéo sang. Chưa đầy một năm sau, gần như cả đoàn chiến thuyền của họ đã nằm lại trên sông Tiền."),
('hook4',"Lời cầu cứu ấy đã kết thúc ra sao? Hai thứ sẽ kể lại: những gì quân nước Xiêm làm trên đất Gia Định, và một khúc sông được chọn sẵn."),
('goc_re',"Mấy năm trước đó, ba anh em nhà Tây Sơn là Nguyễn Nhạc, Nguyễn Huệ, Nguyễn Lữ đã nhiều lần đánh vào Gia Định, vùng đất phương Nam."),
('goc_re',"Người giữ Gia Định là Nguyễn Ánh, và ông thua chạy hết lần này đến lần khác, có lúc phải trốn ra tận các đảo ngoài biển."),
('goc_re',"Năm một nghìn bảy trăm tám mươi tư, ông sang Xiêm cầu cứu. Vua Xiêm nhận lời, sai hai tướng Chiêu Tăng, Chiêu Sương đem quân sang."),
('goc_re',"Theo sử nhà Nguyễn, đạo quân ấy có hai vạn thủy binh với ba trăm chiến thuyền, thêm ba vạn quân bộ."),
('the_nguy',"Giữa năm ấy, quân nước Xiêm vào Rạch Giá. Đến cuối năm, họ đã chiếm Trà Ôn, Sa Đéc, Mân Thít, cả một dải miền Tây."),
('diem_thap',"Nhìn trên bản đồ, Gia Định tưởng như sắp về lại tay Nguyễn Ánh. Lời cầu cứu lúc ấy tưởng như đã chọn đúng."),
('buoc_ngoat',"Nhưng đi tới đâu, quân nước Xiêm cướp phá tới đó. Sử nhà Nguyễn, sử của chính phe Nguyễn Ánh, cũng chép rằng dân miền Tây rất oán."),
('buoc_ngoat',"Thứ đầu tiên là thế: đạo quân được mời sang cứu đã trở thành gánh nặng của chính dân Gia Định."),
('buoc_ngoat',"Tin về đạo quân được cầu cứu sang ấy tới Quy Nhơn, nơi nhà Tây Sơn đóng đô. Nguyễn Nhạc liền sai em là Nguyễn Huệ đem quân vào nam."),
('lan1',"Tới Mỹ Tho, thấy quân nước Xiêm đông hơn, lại đang thắng, Nguyễn Huệ không dàn trận đánh thẳng, mà chọn một khúc sông Tiền để chờ."),
('lan1',"Khúc sông ấy chạy từ rạch Gầm tới rạch Xoài Mút, giữa dòng có cù lao Thới Sơn che khuất tầm nhìn."),
('lan1',"Quân bộ và đại bác phục sẵn ở hai bờ và trên cù lao, thuyền chiến giấu trong các con rạch. Thứ hai là khúc sông ấy."),
('lang',"Sáng sớm một ngày tháng Giêng năm một nghìn bảy trăm tám mươi lăm, đoàn chiến thuyền nước Xiêm xuôi sông Tiền, định đánh vào Mỹ Tho."),
('lang',"Thuyền đi đầu đã tới Rạch Gầm, thuyền đi cuối cũng lọt vào Xoài Mút. Hai bờ vẫn im, cù lao vẫn im."),
('cao_trao',"Rồi thuyền của nhà Tây Sơn từ các con rạch lao ra, chặn cả đầu lẫn đuôi. Đại bác hai bờ và trên cù lao cùng nổ."),
('cao_trao',"Không còn lối thoát. Thuyền vỡ, thuyền chìm khắp khúc sông, gần như cả đoàn chiến thuyền nước Xiêm bị đánh tan."),
('chi_tiet_nguoi',"Hai tướng Chiêu Tăng, Chiêu Sương cùng vài nghìn người lên bờ, theo đường bộ qua Chân Lạp mà chạy về nước."),
('don_cuoi',"Còn Nguyễn Ánh cũng phải bỏ chạy, và nơi ông chạy tới lại chính là nước Xiêm, nơi ông đã sang xin quân năm trước."),
('don_cuoi',"Theo sử nhà Nguyễn, từ sau trận ấy, người Xiêm ngoài miệng tuy nói cứng, nhưng trong lòng sợ quân nhà Tây Sơn như sợ cọp."),
('ket',"Lời cầu cứu năm ấy đã đưa mấy vạn quân nước Xiêm vào đúng khúc sông Nguyễn Huệ chọn sẵn. Cảm ơn bạn đã lắng nghe câu chuyện này."),
]
xuat2(S,'tm9',184001)
