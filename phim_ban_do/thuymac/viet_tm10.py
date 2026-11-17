import sys,os;sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)));sys.path.insert(0,'/tmp/gen');from viet_chung import xuat2
# Thủy mặc tập 10: Ngọc Hồi, Đống Đa 1789 (mã tm10), theo mẫu tm5
S=[
('hook1',"Nếu sắp đánh một đạo quân đông gấp nhiều lần mình, bạn có dám hẹn trước cả ngày ăn mừng chiến thắng không?"),
('hook2',"Có một người đã dám. Theo lời kể cũ, Quang Trung Nguyễn Huệ cho quân ăn Tết sớm, rồi hẹn mồng bảy tháng Giêng sẽ vào Thăng Long ăn mừng."),
('hook3',"Đạo quân đang giữ Thăng Long lúc ấy là quân nhà Thanh, hai mươi chín vạn người theo sử ta. Và Quang Trung đã vào thành trước hẹn hai ngày."),
('hook4',"Vì sao lời hẹn ấy lại đến sớm như thế? Có hai thứ làm nên chuyện ấy: một cái Tết ăn trước, và những tấm ván phủ rơm ướt."),
('goc_re',"Năm một nghìn bảy trăm tám mươi tám, vua Lê Chiêu Thống bỏ Thăng Long chạy trốn quân nhà Tây Sơn. Mẹ và vợ con ông chạy sang nhà Thanh xin quân."),
('goc_re',"Thế là vua Thanh Càn Long nhận lời, sai Tôn Sĩ Nghị đem quân sang. Cuối năm ấy, quân nhà Thanh tràn qua biên giới, kéo thẳng về Thăng Long."),
('goc_re',"Còn tướng Tây Sơn giữ Bắc Hà là Ngô Văn Sở nghe theo kế của Ngô Thì Nhậm, không liều đánh, rút hết quân về giữ phòng tuyến Tam Điệp."),
('the_nguy',"Quân nhà Thanh vào Thăng Long gần như không mất một trận nào. Tôn Sĩ Nghị phong Lê Chiêu Thống làm An Nam quốc vương, đóng đại doanh ngay giữa kinh thành."),
('the_nguy',"Theo lời kể cũ, từ đó Lê Chiêu Thống ngày ngày phải sang dinh Tôn Sĩ Nghị chầu chực, việc gì cũng chờ lệnh của tướng nhà Thanh."),
('diem_thap',"Cả Bắc Hà đã nằm trong tay giặc, quân nhà Tây Sơn phải lùi sau núi Tam Điệp. Nhìn lúc ấy, hẹn ngày lấy lại Thăng Long nghe như chuyện không tưởng."),
('buoc_ngoat',"Nhưng tin dữ đã về tới Phú Xuân. Nguyễn Huệ lập đàn lên ngôi Hoàng đế, lấy niên hiệu Quang Trung, rồi lập tức kéo quân ra bắc."),
('buoc_ngoat',"Qua Nghệ An, ông tuyển thêm quân, đến Tam Điệp thì hội với Ngô Văn Sở. Ở đó, ông cho quân ăn Tết trước, rồi đưa ra lời hẹn ngày mồng bảy."),
('buoc_ngoat',"Thứ đầu tiên là cái Tết ăn sớm ấy. Đêm ba mươi, khi quân nhà Thanh còn đang mừng năm mới, quân nhà Tây Sơn đã vượt sông Gián Khẩu tiến ra."),
('lan1',"Rồi các đồn tiền tiêu của giặc tan rất nhanh. Đêm mồng ba Tết, quân nhà Tây Sơn lặng lẽ vây kín đồn Hà Hồi rồi đồng loạt hô vang."),
('lan1',"Quân trong đồn hoảng sợ, xin hàng ngay, chưa kịp đánh. Trên đường tới Thăng Long, nơi đã hẹn ăn mừng, chỉ còn đồn Ngọc Hồi chắn lối."),
('lang',"Thế nhưng Ngọc Hồi có lũy cao, có súng lớn, quân nhà Thanh lại đông. Đánh thẳng vào, người chết trước tiên sẽ là quân của Quang Trung."),
('lang',"Thứ hai là những tấm ván. Theo lời kể cũ, ông cho ghép ván, phủ rơm thấm nước, cứ hai mươi người khiêng một tấm che đi trước."),
('cao_trao',"Rạng sáng mồng năm Tết, những bức ván ướt tiến dần về lũy. Súng và tên trong đồn bắn ra, rơi xuống lớp rơm ướt."),
('cao_trao',"Đến sát lũy, quân nhà Tây Sơn bỏ ván, xông thẳng vào. Đồn Ngọc Hồi vỡ, quân nhà Thanh chạy tán loạn, giẫm lên nhau mà chết."),
('cao_trao',"Cùng sáng ấy, ở Khương Thượng, cánh quân của Đô đốc Long đánh tan đồn giặc. Tướng nhà Thanh Sầm Nghi Đống thắt cổ tự tử."),
('chi_tiet_nguoi',"Còn Tôn Sĩ Nghị đang ở trong thành. Theo lời kể cũ, ông sợ đến mức ngựa không kịp đóng yên, người không kịp mặc giáp, vượt cầu phao chạy trước."),
('don_cuoi',"Thế là quân nhà Thanh chen nhau qua cầu phao trên sông Hồng. Cầu đứt, rất nhiều người rơi xuống nước chết đuối, sông như bị chặn dòng."),
('don_cuoi',"Riêng Lê Chiêu Thống chạy theo sang nhà Thanh. Người từng được phong An Nam quốc vương, sang đó chỉ được một chức quan nhỏ, rồi chết nơi đất khách."),
('ket',"Trưa mồng năm Tết, Quang Trung vào Thăng Long, sớm hơn ngày đã hẹn hai ngày. Cảm ơn bạn đã lắng nghe câu chuyện này."),
]
xuat2(S,'tm10',185001)
