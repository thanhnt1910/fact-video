"""Ghi kết quả tra nguồn (01/11/2026) vào ban-do-can-xac-minh.json. KHÔNG đổi trang_thai, KHÔNG điền toa_do, KHÔNG đặt duoc_ve.
Chạy SAU tao_ban_do_xac_minh.py. Nguồn đều là THỨ CẤP (bài tổng hợp có dẫn sách), chưa đối chiếu Đại Việt sử ký toàn thư, Tống sử, Tục tư trị thông giám trường biên.
python ke-hoach/anh/lt1v4/tra_nguon_ban_do.py"""
import json, os
D = os.path.dirname(os.path.abspath(__file__)); P = f'{D}/ban-do-can-xac-minh.json'
d = json.load(open(P, encoding='utf-8'))
NG = {
 'S1': dict(ten='Battle of Như Nguyệt River (1077), Wikipedia tiếng Anh (dẫn Anderson 2008; Taylor 2013; Trần Trọng Kim 1971; Kiernan 2019)', url='https://en.wikipedia.org/wiki/Battle_of_Nh%C6%B0_Nguy%E1%BB%87t_River_(1077)', loai='thứ cấp (bách khoa mở)'),
 'S2': dict(ten='Lý–Song War, Wikipedia tiếng Anh, bản lưu IPFS (dẫn Anderson 2008 tr.206–210; Kiernan 2019; Chapuis 1995)', url='https://ipfs.ssi.eecc.de/ipns/en.wikipedia-on-ipfs.org/wiki/L%C3%BD%E2%80%93Song_War', loai='thứ cấp (bách khoa mở)'),
 'S3': dict(ten='Trận Như Nguyệt, Wikipedia tiếng Việt (qua Wikiwand; chỉ có số chú thích, không có danh mục nguồn đầy đủ)', url='https://wikiwand.com/vi/articles/Tr%E1%BA%ADn_Nh%C6%B0_Nguy%E1%BB%87t', loai='thứ cấp (bách khoa mở)'),
 'S4': dict(ten='Diễn Châu, Wikipedia tiếng Anh (chỉ nói xã Diễn Châu hiện nay, tỉnh Nghệ An)', url='https://en.wikipedia.org/wiki/Di%E1%BB%85n_Ch%C3%A2u', loai='thứ cấp, không nói về châu thời Lý')}
R = {  # id: (kết quả, [nguồn], mức, đề xuất)
 'CHUNG-01': ('CHƯA tra: chưa kiểm giấy phép bộ dữ liệu nền.', [], 'chua_tra', 'Cần tìm bộ dữ liệu nền có giấy phép rõ (đề xuất kiểm Natural Earth) và ghi nhãn "bản đồ hiện đại".'),
 'CHUNG-02': ('Đối chiếu tên cổ – tên nay tra được: Ung Châu = Nam Ninh (Quảng Tây); Quảng Nguyên = Cao Bằng; sông Như Nguyệt = một khúc sông Cầu; Diễn Châu nay thuộc Nghệ An. Chưa có: Quế, Khâm, Liêm, Tư Lang, Tô Mậu, Vĩnh Bình, Côn Lôn.', ['S1', 'S2', 'S3', 'S4'], 'mot_phan_thu_cap', 'Làm bảng đối chiếu cho các tên đã có nguồn; tên chưa có chỉ ghi tên cổ.'),
 'CHUNG-03': ('Không cần nguồn: là quy ước ghi chú.', [], 'khong_ap_dung', 'Chủ kênh duyệt quy ước: mũi tên không có sử liệu ghi nhãn "minh họa".'),
 'M1-01': ('CHƯA tra được nguồn cho vị trí Quế Châu (trang tham khảo bị chặn trong phiên này).', [], 'chua_tra', 'Cần nguồn riêng trước khi đặt nhãn.'),
 'M1-02': ('Không nguồn nào mô tả đường biên giới năm 1075 (Wikipedia tiếng Việt nói rõ không mô tả).', ['S3'], 'khong_co_nguon', 'Không vẽ đường biên. Chỉ ghi chữ "biên giới" bằng nhãn.'),
 'M1-03': ('Không nguồn nào nêu điểm xuất phát của Thẩm Khởi, Lưu Di.', [], 'khong_co_nguon', 'Chỉ nhãn tại Quế Châu (khi Quế Châu đã có nguồn), không mũi tên.'),
 'M1-04': ('Diễn giải, không phải địa lý.', [], 'khong_ap_dung', 'Giữ ở chữ trên màn hình, không ký hiệu bản đồ.'),
 'M2-01': ('Nguồn nói hạm đội Lý Thường Kiệt chiếm Khâm Châu và Liêm Châu tháng 10 năm 1075 (Anderson 2008, tr.207–208) nhưng KHÔNG nêu vị trí nay.', ['S2'], 'su_kien_co_nguon_vi_tri_chua', 'Chưa đặt vị trí; cần nguồn địa danh.'),
 'M2-02': ('Ung Châu (Yongzhou) = Nam Ninh hiện nay, Quảng Tây.', ['S2'], 'mot_phan_thu_cap', 'Có thể đánh dấu VERIFIED sau khi chủ kênh chấp nhận mức nguồn thứ cấp, hoặc tra thêm Tống sử.'),
 'M2-03': ('Không nguồn nào nêu nơi tập kết.', [], 'khong_co_nguon', 'Không vẽ điểm xuất phát.'),
 'M2-04': ('Không nguồn nào nêu tuyến biển cụ thể; nguồn chỉ nói đạo thủy chiếm Khâm, Liêm.', ['S2'], 'khong_co_nguon', 'Chỉ mũi tên ước lệ có nhãn "minh họa", hoặc không vẽ.'),
 'M2-05': ('Nguồn nói Tông Đản đưa quân vào Quảng Nam Tây đạo; không nêu tuyến cụ thể.', ['S2'], 'khong_co_nguon', 'Như M2-04.'),
 'M2-06': ('Phân công khớp: Tông Đản (nguồn ghi Nùng Tông Đản) đạo bộ, Lý Thường Kiệt đạo thủy (Anderson 2008 tr.207–208).', ['S2'], 'mot_phan_thu_cap', 'Có thể ghi nhãn chỉ huy; kiểm lại bằng Toàn thư.'),
 'M2-07': ('Nguồn KHÔNG khớp nhau về số quân: 63.000 (23.000 đạo bộ + 40.000 đạo thủy), 80.000, hoặc 80.000–100.000; có chỗ nói vua ra lệnh "hơn một trăm nghìn". Kịch bản ghi "hơn mười vạn".', ['S2'], 'mau_thuan_nguon', 'Không ghi số lên bản đồ. CẦN chủ kênh biết: câu "hơn mười vạn người" trong kịch bản chưa được nguồn nào ở đây xác nhận chắc; nên đối chiếu Toàn thư hoặc nói "theo lời kể".'),
 'M3-01': ('Ung Châu = Nam Ninh (xem M2-02). Chưa tính khoảng cách tới biên giới vì chưa có đường biên.', ['S2'], 'mot_phan_thu_cap', 'Không ước lượng bằng mắt.'),
 'M3-02': ('Không nguồn nào nêu đường rút.', [], 'khong_co_nguon', 'Không vẽ.'),
 'M3-03': ('Là lập luận trong kịch bản.', [], 'khong_ap_dung', 'Không vẽ vòng vây.'),
 'M4-01': ('CHƯA tra ranh giới các nước.', [], 'chua_tra', 'Không vẽ đường biên; có thể chỉ ghi nhãn tên nước.'),
 'M4-02': ('CHƯA tra.', [], 'chua_tra', 'Chưa đặt nhãn hướng.'),
 'M4-03': ('Diễn giải.', [], 'khong_ap_dung', 'Mũi tên áp lực chỉ là ký hiệu minh họa có nhãn.'),
 'M5-01': ('Như Nguyệt là một khúc sông Cầu; phòng tuyến chạy từ chân núi Tam Đảo dọc sông; hai bến chính Như Nguyệt (vùng Hiệp Hòa, Bắc Giang) và Thị Cầu (sau gọi Đáp Cầu). Bản tiếng Anh ghi Bắc Ninh, bản tiếng Việt nhắc Hiệp Hòa thuộc Bắc Giang: khác nhau về tên tỉnh (chưa kiểm có do thay đổi địa giới hành chính hay không).', ['S1', 'S3'], 'mot_phan_thu_cap', 'Chủ kênh chọn cách ghi tên nay (tránh ghi tên tỉnh), hoặc tra thêm.'),
 'M5-02': ('Chưa tra riêng vị trí Thăng Long thời Lý; nguồn chỉ nói sông Như Nguyệt "gần kinh đô Thăng Long".', ['S1'], 'chua_tra', 'Cần nguồn riêng (kiến thức chung: thuộc Hà Nội hiện nay, nhưng chưa dẫn nguồn trong phiên này).'),
 'M5-03': ('Quân Lý giữ bờ nam, quân Tống ở bờ bắc (Triệu Tiết đối diện bến Như Nguyệt; Quách Quỳ khoảng 30 km về phía đông, đối diện Thị Cầu).', ['S1', 'S3'], 'mot_phan_thu_cap', 'Khớp kịch bản; có thể ghi nhãn bờ nam, bờ bắc.'),
 'M5-04': ('Nguồn nói quân Quách Quỳ qua Lạng Sơn, Triệu Tiết qua cao nguyên Cao Bằng (Anderson 2008; Taylor 2013). Không có tuyến chi tiết.', ['S1', 'S3'], 'mot_phan_thu_cap', 'Chỉ mũi tên rất khái quát ước lệ, có nhãn "minh họa".'),
 'M5-05': ('Hai nguồn thứ cấp (Wikipedia tiếng Anh dẫn Trần Trọng Kim 1971 và tiếng Việt) cùng mô tả lũy đất đóng cọc tre nhiều lớp, hố chông dưới bãi sông, chạy dọc bờ nam. Chưa đối chiếu sử liệu gốc. Có liên quan DQ-003.', ['S1', 'S3'], 'mot_phan_thu_cap', 'Vị trí và hình dạng cụ thể vẫn chưa có: không vẽ thành đường cụ thể. Chủ kênh có thể xem lại mức của chi tiết "lũy đất cắm cọc" (hiện C) sau khi có nguồn gốc; em không tự nâng mức.'),
 'M6-01': ('Quảng Nguyên nay là Cao Bằng; Tư Lang, Môn, Tô Mậu, Quảng Lăng nay là phần lớn Cao Bằng và Lạng Sơn (câu này trong nguồn không có chú thích riêng).', ['S2'], 'mot_phan_thu_cap_yeu', 'Chỉ dùng Quảng Nguyên = Cao Bằng; ba châu còn lại cần nguồn riêng.'),
 'M6-02': ('Nguồn nói nhà Tống giữ Quảng Nguyên và đổi thành Thuận Châu (Shun\'anzhou). Năm đổi tên 1079 (kịch bản) chưa được trang này xác nhận.', ['S2'], 'mot_phan_thu_cap', 'Cùng vùng với Quảng Nguyên; năm cần nguồn.'),
 'M6-03': ('Nguồn nói cuộc đàm phán 1084 tổ chức tại trại Vĩnh Bình (Yongping) của nhà Tống, miền nam Quảng Nam; không nêu vị trí nay.', ['S2'], 'su_kien_co_nguon_vi_tri_chua', 'Chưa đặt vị trí.'),
 'M6-04': ('KHÔNG tìm thấy "sáu huyện ba động" trong nguồn đã đọc.', [], 'khong_co_nguon', 'Không đánh dấu; chỉ chữ trên màn hình theo kịch bản.'),
 'M6-05': ('Không có nguồn về ranh giới.', [], 'khong_co_nguon', 'Không vẽ đường biên.'),
 'M6-06': ('Nguồn thứ cấp ghi: 1077 nhà Tống giữ Quảng Nguyên và các châu khác; 1082 Đại Việt trả Ung, Khâm, Liêm cùng tù binh, đổi lại nhà Tống trả bốn châu và một huyện; 1084 đàm phán biên giới tại Vĩnh Bình (Anderson 2008 tr.209–210). Mốc 1082 này KHÔNG có trong kịch bản.', ['S2'], 'mau_thuan_nguon', 'CẦN chủ kênh biết: trình tự trong kịch bản (1079, 1084) chưa khớp hoàn toàn với nguồn này. Phải đối chiếu Toàn thư và Tục tư trị thông giám trước khi dùng nhãn năm.'),
 'M7-01': ('Chỉ tìm thấy Diễn Châu hiện nay là một xã thuộc Nghệ An; chưa có nguồn về châu Diễn thời Lý.', ['S4'], 'chua_tra', 'Chưa đặt vị trí châu thời Lý.'),
 'M7-02': ('KHÔNG tìm thấy nguồn về Lý Giác 1103 trong các trang đã đọc.', [], 'khong_co_nguon', 'Không đặt nhãn sự kiện.'),
}
miss = [x['id'] for x in d['items'] if x['id'] not in R]; assert not miss, miss
for x in d['items']:
    kq, ng, muc, dx = R[x['id']]
    x['tra_nguon'] = dict(ngay='2026-11-01', ket_qua=kq, nguon=[dict(ma=k, **NG[k]) for k in ng], muc_nguon=muc, de_xuat=dx,
                          ghi_chu='Chỉ là kết quả tra cứu; trang_thai giữ NEEDS_REVIEW, không tọa độ, không được vẽ, cho tới khi chủ kênh chấp nhận mức nguồn.')
d['tra_nguon_tong_ket'] = dict(ngay='2026-11-01', nguon_dung=NG, han_che='Chỉ đọc được các trang tổng hợp thứ cấp; Đại Việt sử ký toàn thư, Tống sử, Tục tư trị thông giám trường biên CHƯA được đối chiếu. Trang về Quế Châu, Khâm, Liêm bị chặn trong phiên này.',
    thong_ke={k: sum(1 for x in d['items'] if x['tra_nguon']['muc_nguon'] == k) for k in sorted({x['tra_nguon']['muc_nguon'] for x in d['items']})})
# Chủ kênh chấp nhận nguồn thứ cấp (01/11/2026): mục mức 'mot_phan_thu_cap' -> VERIFIED, chỉ cho phần đã nêu trong ket_qua. KHÔNG tọa độ, KHÔNG duoc_ve (nguồn không cho tọa độ).
for x in d['items']:
    t = x['tra_nguon']
    if t['muc_nguon'] == 'mot_phan_thu_cap':
        x['trang_thai'] = 'VERIFIED'
        x['nguon_xac_minh'] = [dict(ma=k['ma'], ten=k['ten'], url=k['url'], loai=k['loai']) for k in t['nguon']]
        x['xac_minh'] = dict(nguoi_chap_nhan='chủ kênh', ngay='2026-11-01', muc_nguon='thứ cấp, chưa đối chiếu sử liệu gốc', pham_vi_xac_minh=t['ket_qua'])
d['tra_nguon_tong_ket']['chap_nhan'] = 'Chủ kênh chấp nhận nguồn thứ cấp 01/11/2026: các mục mức mot_phan_thu_cap đã VERIFIED (chỉ phần đã ghi), vẫn chưa tọa độ và chưa được vẽ.'
json.dump(d, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(d['tra_nguon_tong_ket']['thong_ke'])
