# Bảng khung tm11–tm15 (bước 1). Số đoạn mỗi nhịp lấy từ lời đọc.
import json
P='/tmp/pc/ke-hoach/thu-giong-hai/'
def lam(ma,meta,SV):
    J=json.load(open(P+ma+'_full.json'));nh=[]
    for d in J:
        if nh and nh[-1]['nhip']==d['nhip']: nh[-1]['doan']+=1
        else:
            sv,ng=SV[d['nhip']];nh.append(dict(nhip=d['nhip'],su_viec=sv,nguon=ng,doan=1))
    meta=dict(ma=ma,**meta,nhip=nh);json.dump(meta,open(P+ma+'_khung.json','w'),ensure_ascii=False,indent=1)
TT='Toàn thư'
lam('tm11',dict(ten='Dương Đình Nghệ lấy lại Đại La 931',n_hua=2,loi_hua='hai thứ: ba nghìn người con nuôi, và một viên tướng thân cận trở mặt',
 cau_hoi='Vì sao thành Đại La phải lấy lại tới hai lần?',soi_chi=['Đại La'],hinh_anh=['Đại La'],dem=['thứ đầu tiên','thứ hai']),{
 'hook1':('Nhắc chuyện thắng Nam Hán người ta chỉ nhớ Ngô Quyền, Bạch Đằng','kiểu mở "sự thật bị hiểu nhầm"'),
 'hook2':('Bảy năm trước Bạch Đằng, Nam Hán đã bị đuổi khỏi Đại La','Toàn thư (931)'),
 'hook3':('Dương Đình Nghệ cầm quân, cha vợ Ngô Quyền',TT),
 'hook4':('Vì sao Đại La phải lấy lại hai lần? Con nuôi và người trở mặt','lời hứa'),
 'goc_re':('Nhà Đường sụp; họ Khúc tự chủ; Nam Hán ở Quảng Đông muốn chiếm','Toàn thư, Tân Ngũ đại sử'),
 'the_nguy':('Năm 930 Nam Hán bắt người đứng đầu họ Khúc; Lý Tiến giữ Đại La','Toàn thư; Wikipedia (Khúc Thừa Mỹ): 930'),
 'diem_thap':('Họ Khúc mất, chưa ai cầm quân','diễn giải'),
 'buoc_ngoat':('Ái Châu: 3.000 người coi như con nuôi (thứ đầu tiên), lập trường đấu vật luyện võ; 931 vây Đại La','Tư trị thông giám, Toàn thư; Wikipedia (3.000 người coi như con nuôi)'),
 'lan1':('Lý Tiến cầu cứu; quân đồn trú đông bị đánh tan; Lý Tiến bỏ lính cùng các quan chạy về; Đại La lần đầu','Wikipedia (Dương Đình Nghệ)'),
 'lang':('Trình Bảo tới khi thành đã mất, vây ngược Đại La','Wikipedia (Dương Đình Nghệ)'),
 'cao_trao':('Từ trong thành đánh ra, chém Trình Bảo','Toàn thư; Wikipedia'),
 'chi_tiet_nguoi':('Tướng cũ từ đời Khúc Hạo nay tự xưng Tiết độ sứ','Wikipedia (Dương Đình Nghệ)'),
 'don_cuoi':('Sáu năm sau Kiều Công Tiễn giết (thứ hai); con rể Ngô Quyền giết Công Tiễn, lấy lại Đại La lần hai',TT),
 'ket':('Bạch Đằng có gốc từ Đại La năm ấy','diễn giải, nói rõ là cách nhìn')})
lam('tm12',dict(ten='Triệu Quang Phục ở đầm Dạ Trạch 546–550',n_hua=3,loi_hua='ba thứ: một cái đầm, những chiếc thuyền độc mộc, và một lệnh gọi về',
 cau_hoi='Một đạo quân chỉ ra tay trong đêm thì làm sao đuổi được giặc?',soi_chi=['đêm'],hinh_anh=['đêm'],dem=['thứ đầu tiên','thứ hai','thứ ba']),{
 'hook1':('Đạo quân đánh giặc nhiều năm mà ban ngày không ai thấy','kiểu mở "nghịch lý"'),
 'hook2':('Ngày tắt khói lửa, đêm thuyền nhỏ ra khỏi lau sậy','Toàn thư; Nhân Dân (ban ngày tắt hết khói lửa)'),
 'hook3':('Triệu Quang Phục, nước Vạn Xuân, Dạ Trạch Vương',TT),
 'hook4':('Làm sao đuổi giặc? Đầm, thuyền độc mộc, lệnh gọi về','lời hứa'),
 'goc_re':('Nhà Lương cai trị; Lý Bí lập Vạn Xuân; cha con Triệu Túc theo sớm nhất; Trần Bá Tiên sang','Toàn thư, Lương thư'),
 'the_nguy':('Lý Nam Đế thua, rút lên núi Phú Thọ (Khuất Lão), giao binh quyền',TT),
 'diem_thap':('Quân nhỏ trước đại quân vừa thắng','diễn giải'),
 'buoc_ngoat':('Vào đầm Dạ Trạch (thứ đầu tiên): bãi nổi, lạch nhỏ, ngày tắt khói lửa','Toàn thư; Phan Huy Chú mô tả đầm'),
 'lan1':('Thuyền độc mộc (thứ hai) đánh úp doanh trại, cướp lương',TT),
 'lan2':('Bá Tiên đánh mãi không được; kế trì cửu',TT),
 'lang':('Đánh úp chưa đuổi được giặc; Lý Nam Đế mất (548)',TT),
 'chi_tiet_nguoi':('Xưng Triệu Việt Vương; dân gọi Dạ Trạch Vương',TT),
 'cao_trao':('550 nhà Lương loạn Hầu Cảnh, gọi Bá Tiên về (thứ ba); Dương Sàn chết, quân Lương chạy','Toàn thư, Lương thư'),
 'don_cuoi':('Vào Long Biên; làm vua hơn 20 năm tới khi mất ngôi vào Lý Phật Tử (571)',TT),
 'ket':('Những đêm trong đầm giữ đạo quân sống tới ngày giặc gọi tướng về','tổng kết, đúng tác nhân')})
lam('tm13',dict(ten='Hai Bà Trưng, Lãng Bạc và Cấm Khê 40–43',n_hua=3,loi_hua='ba nơi: Mê Linh, Lãng Bạc, Cấm Khê',
 cau_hoi='Hai bà đã giữ đất nước ra sao trước đạo quân nhà Hán?',soi_chi=['giữ'],hinh_anh=['làm vua'],dem=['nơi đầu tiên','nơi thứ hai','nơi thứ ba']),{
 'hook1':('Hai chị em làm vua, không biết chắc đã mất thế nào','kiểu mở "số phận nhân vật"'),
 'hook2':('Sông Hát hay bị bắt chém: hai cách kể','thần tích, Toàn thư; Hậu Hán thư'),
 'hook3':('Trưng Trắc, Trưng Nhị làm vua ba năm','Toàn thư, Hậu Hán thư'),
 'hook4':('Giữ nước ra sao? Mê Linh, Lãng Bạc, Cấm Khê','lời hứa'),
 'goc_re':('Nhà Hán cai trị, quận Giao Chỉ; Tô Định tham bạo, giết Thi Sách; nổi lên ở Mê Linh (nơi đầu tiên) năm 40; 65 thành, Trưng Trắc làm vua','Hậu Hán thư, Việt sử lược, Toàn thư (việc giết Thi Sách chỉ có ở sử ta)'),
 'the_nguy':('Mã Viện sang, hơn 2 vạn quân và hơn 1 vạn quân địa phương, thuyền chở lương; Lãng Bạc (nơi thứ hai) xuân 42, thua, mấy nghìn chết, hơn vạn hàng','Hậu Hán thư (Mã Viện truyện)'),
 'diem_thap':('Rút đi, mất phần lớn quân','Hậu Hán thư'),
 'buoc_ngoat':('Quân Hán bệnh vì mưa nóng; lời Mã Viện kể diều hâu rơi xuống nước; hai bà còn quân','Hậu Hán thư (Mã Viện truyện)'),
 'lan1':('Cấm Khê (nơi thứ ba), đánh nhiều trận, bị cắt lương','Toàn thư (có sách chép Kim Khê); vị trí còn tranh luận: Tản Viên hay gần Mê Linh'),
 'lang':('Đầu năm 43 chỉ còn người theo tới cùng','Hậu Hán thư'),
 'cao_trao':('Trận cuối, hai bà thua; giữa năm 43 kháng cự tắt','Hậu Hán thư, Toàn thư'),
 'chi_tiet_nguoi':('Hai cách kể về cái chết','Hậu Hán thư; Toàn thư, thần tích'),
 'don_cuoi':('Quân Hán chết bốn, năm phần mười vì bệnh; Mã Viện sửa luật, chia huyện','Hậu Hán thư'),
 'ket':('Làm vua ba năm, đền Mê Linh, Hát Môn còn hương khói','hiện trạng di tích')})
lam('tm14',dict(ten='Nguyễn Trung Trực đốt tàu Hy Vọng ở Nhật Tảo 1861',n_hua=2,loi_hua='hai thứ: một cách giả làm ghe buôn, và một câu nói về cỏ',
 cau_hoi='Làm sao mấy chiếc ghe nhỏ đốt được con tàu ấy?',soi_chi=['ghe'],hinh_anh=['cỏ'],dem=['thứ đầu tiên','thứ hai']),{
 'hook1':('Giữa trưa, năm ghe nhỏ áp sát tàu Pháp','kiểu mở "sự kiện bất ngờ"; Wikipedia dẫn sử Pháp'),
 'hook2':('Không súng, chỉ dao giáo; tàu bốc cháy','Wikipedia (Nguyễn Trung Trực)'),
 'hook3':('Nguyễn Trung Trực, người chài lưới; câu nói về cỏ','báo Pháp luật; lsvn'),
 'hook4':('Làm sao ghe nhỏ đốt được tàu? giả ghe buôn, câu nói về cỏ','lời hứa'),
 'goc_re':('Pháp đánh miền Nam; Chí Hòa vỡ 2/1861; nghĩa quân Trương Định','Đại Nam thực lục; Wikipedia'),
 'the_nguy':('Tàu Pháp chặn sông; tàu Hy Vọng ở vàm Nhật Tảo','Wikipedia; vietnamplus'),
 'diem_thap':('Ghe nhỏ, dao giáo, đánh thẳng là nộp mạng','diễn giải'),
 'buoc_ngoat':('150 người, ba toán; giả ghe buôn xin giấy (thứ đầu tiên); súng lớn vô dụng khi áp sát','Wikipedia (dẫn tư liệu Pháp); chuyện đám cưới là lời kể khác'),
 'lan1':('Trưa 10/12/1861, toán nhử; năm ghe cặp mạn tàu','Wikipedia'),
 'lang':('Trên tàu mấy chục người, súng đầy đủ','Wikipedia (số người trên tàu các nguồn khác nhau)'),
 'cao_trao':('Nhảy lên tàu, giáp lá cà; phá thân tàu, đốt; vài người trốn thoát','Wikipedia'),
 'chi_tiet_nguoi':('Tự Đức khen, thăng chức','Wikipedia: Tự Đức phong Lãnh binh Hà Tiên'),
 'don_cuoi':('Hòa ước 1862 cắt ba tỉnh; 1868 chiếm đồn Rạch Giá; mẹ bị bắt làm con tin; câu nói về cỏ (thứ hai); bị chém 27/10/1868','Wikipedia; lsvn'),
 'ket':('Con tàu cháy và câu nói về cỏ','tổng kết')})
lam('tm15',dict(ten='Trận Cầu Giấy 1873',n_hua=2,loi_hua='hai thứ: một tòa thành mất trong một buổi sáng, và một bản hòa ước ký sau trận thắng',
 cau_hoi='Chuyện gì chờ Garnier sau gò đất ấy?',soi_chi=['Garnier'],hinh_anh=['Cầu Giấy'],dem=['thứ đầu tiên','thứ hai']),{
 'hook1':('Viên chỉ huy Pháp bỏ thương thuyết đuổi theo','kiểu mở "trận chiến"; Wikipedia (Garnier Expedition)'),
 'hook2':('Pháo sa bùn, chạy lên gò đất ngoài Cầu Giấy','Wikipedia'),
 'hook3':('Garnier, một tháng trước chiếm Hà Nội với dưới 200 lính','Wikipedia'),
 'hook4':('Chuyện gì chờ ông? thành mất buổi sáng, hòa ước sau trận thắng','lời hứa'),
 'goc_re':('Pháp đã có sáu tỉnh Nam Kỳ; Dupuis chở vũ khí, muối; Garnier ra Hà Nội, đứng về Dupuis','Wikipedia, Đại Nam thực lục'),
 'the_nguy':('20/11/1873 thành Hà Nội mất (thứ đầu tiên); Nguyễn Tri Phương bị thương, bị bắt, nhịn ăn mà mất; mất năm tỉnh thành','Wikipedia (Battle of Hanoi 1873): từ chối chữa trị, tuyệt thực, mất 20/12'),
 'diem_thap':('Vài trăm lính nắm gần hết đồng bằng','Wikipedia'),
 'buoc_ngoat':('Hoàng Kế Viêm ở Sơn Tây, quân Cờ Đen của Lưu Vĩnh Phúc; kéo về khi đang bàn đình chiến','Wikipedia; Đại Nam thực lục'),
 'lan1':('21/12 Cờ Đen đánh tới, bị pháo đẩy lui; Garnier đuổi với 18 lính, 1 pháo','Wikipedia'),
 'lang':('Pháo sa bùn, bỏ lại','Wikipedia'),
 'cao_trao':('Lên gò, phục binh đổ ra, Garnier bị giết; Balny bị giết gần đền Voi Phục','Wikipedia'),
 'chi_tiet_nguoi':('Chết đúng một tháng sau khi chiếm thành','Wikipedia (20/11 và 21/12)'),
 'don_cuoi':('Triều đình bàn hòa, Pháp trả thành (thứ hai); hòa ước 15/3/1874 công nhận sáu tỉnh Nam Kỳ, mở sông Hồng','Wikipedia (Treaty of Saigon 1874)'),
 'ket':('Thắng ở Cầu Giấy nhưng phải thừa nhận miền Nam đã mất','tổng kết')})
