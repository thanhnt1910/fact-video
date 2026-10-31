"""Tạo ban-do-can-xac-minh.json: danh sách dữ liệu địa lý phải xác minh cho M1–M7. KHÔNG có tọa độ, KHÔNG có đường biên.
Mọi mục NEEDS_REVIEW cho tới khi chủ kênh/nguồn xác minh; chỉ mục VERIFIED có nguồn mới được vẽ."""
import json, os
D = os.path.dirname(os.path.abspath(__file__))
DL, DQ, DG = 'DIA_LY', 'DUONG_QUAN_SU', 'DIEN_GIAI'
n = {}
def add(m, loai, nd, doan, can_gi):
    k = n.setdefault(m, []); k.append(dict(id=f'{m}-{len(k)+1:02d}', map=m, loai=loai, noi_dung=nd, co_so_kich_ban=f'đoạn {doan}' if doan else '-', can_xac_minh=can_gi,
        nguon_xac_minh=None, toa_do=None, trang_thai='NEEDS_REVIEW', duoc_ve=False))
# --- chung
for nd, cg in [('Bản đồ nền (bờ biển, sông, địa hình) dùng cho cả bảy bản đồ', 'dữ liệu nền có giấy phép rõ; ghi rõ là bản đồ HIỆN ĐẠI hay bản dựng lịch sử; không dùng bờ biển hiện đại như thể là bờ biển thế kỷ 11 nếu khác nhau'),
               ('Cách gọi địa danh: tên cổ (thời Lý–Tống) và tên hiện đại', 'bảng đối chiếu tên cổ – tên nay có nguồn; chỗ chưa chắc chỉ ghi tên cổ, không gắn tên nay'),
               ('Quy ước nét vẽ: mũi tên quân đội có nhãn "minh họa" nếu tuyến không có sử liệu', 'chủ kênh duyệt quy ước ghi chú')]: add('CHUNG', DG if 'Quy ước' in nd else DL, nd, None, cg)
# --- M1
add('M1', DL, 'Quế Châu: vị trí', 11, 'vị trí thành/châu thời Tống, nguồn địa lý có thể kiểm')
add('M1', DL, 'Đường biên giới Đại Việt – Tống thời điểm 1075 (kịch bản chỉ nói Quế Châu "sát biên giới")', 11, 'nguồn về biên giới; không tự vẽ đường biên')
add('M1', DQ, 'Thẩm Khởi và Lưu Di được phái tới vùng Quế Châu: kịch bản KHÔNG nói họ đi từ đâu', 11, 'nếu không có nguồn về điểm xuất phát thì chỉ ghi nhãn tại Quế Châu, không vẽ mũi tên đường đi')
add('M1', DG, 'Ý "nhà Tống chuẩn bị đánh Đại Việt" (lời Vương An Thạch trong kịch bản)', 11, 'chỉ là diễn giải/lời kể; không thể hiện bằng ký hiệu địa lý như dữ kiện')
# --- M2
add('M2', DL, 'Khâm Châu và Liêm Châu: vị trí (kịch bản: hai vùng ven biển của nhà Tống)', 20, 'vị trí hai châu thời Tống và đối chiếu với tên nay')
add('M2', DL, 'Ung Châu: vị trí', '19-21', 'vị trí thành thời Tống')
add('M2', DL, 'Điểm xuất phát của đạo thủy và đạo bộ (kịch bản không nêu)', 19, 'nguồn sử về nơi tập kết; nếu không có thì không vẽ điểm xuất phát')
add('M2', DQ, 'Đường đi của đạo thủy (Lý Thường Kiệt) tới Khâm Châu, Liêm Châu', '19-20', 'kịch bản chỉ nói đạo thủy tiến công hai châu; tuyến biển cụ thể cần nguồn, nếu không chỉ vẽ mũi tên ước lệ có nhãn "minh họa"')
add('M2', DQ, 'Đường đi của đạo bộ (Tông Đản) tới Ung Châu', '19, 21', 'tuyến bộ cụ thể cần nguồn; kịch bản không nêu')
add('M2', DG, 'Phân công chỉ huy: Lý Thường Kiệt – đạo thủy, Tông Đản – đạo bộ (lời kể trong kịch bản)', 19, 'đối chiếu nguồn sử; nhãn chỉ huy chỉ ghi khi đã đối chiếu')
add('M2', DG, 'Số quân "hơn mười vạn người"', 19, 'số liệu phải có nguồn; không ghi lên bản đồ nếu chưa đối chiếu')
# --- M3
add('M3', DL, 'Ung Châu: vị trí và khoảng cách tới biên giới', '32-33', 'khoảng cách tính trên dữ liệu đã xác minh, không ước lượng bằng mắt')
add('M3', DQ, 'Đường rút về nước của quân Đại Việt (kịch bản chỉ nói "mất đường rút về nước")', 33, 'tuyến rút cụ thể không có trong kịch bản; không vẽ nếu chưa có nguồn')
add('M3', DG, 'Lý do không ở lại giữ thành: "có thể bị bao vây và mất đường rút" (diễn giải trong lời đọc)', 33, 'là lập luận trong kịch bản; không vẽ vòng vây hay mũi tên bao vây như sự kiện đã xảy ra')
# --- M4
add('M4', DL, 'Phạm vi (lãnh thổ) Đại Việt, nhà Tống, Chiêm Thành, Chân Lạp khoảng 1075', 35, 'nguồn về ranh giới các nước; không tự vẽ đường biên')
add('M4', DL, 'Vị trí tương đối của Chiêm Thành và Chân Lạp so với Đại Việt (phía nam? tây nam?)', 35, 'kịch bản không nêu hướng; phải có nguồn trước khi đặt nhãn')
add('M4', DG, 'Ý "tạo sức ép từ nhiều phía" và việc nhà Tống liên kết hai nước', 35, 'diễn giải; mũi tên áp lực chỉ là ký hiệu minh họa có nhãn, không phải đường hành quân')
# --- M5
add('M5', DL, 'Sông Như Nguyệt: đoạn sông cụ thể nơi đặt phòng tuyến (kịch bản chỉ nói "khúc sông này")', '38-40', 'xác định đoạn sông có nguồn; tên cổ – tên nay')
add('M5', DL, 'Thăng Long (thời Lý): vị trí', 39, 'vị trí kinh thành thời Lý')
add('M5', DL, 'Bờ bắc và bờ nam của đoạn sông (bờ nam là phía Đại Việt giữ)', '40-41', 'hướng chảy và bờ theo dữ liệu đã xác minh')
add('M5', DQ, 'Đường quân Tống tiến về kinh thành qua khúc sông (kịch bản: "nằm trên đường tiến về kinh thành")', '39-40', 'tuyến bộ từ biên giới đến sông cần nguồn')
add('M5', DG, 'Phòng tuyến dọc bờ nam: vị trí và hình dạng (kịch bản: "theo những ghi chép và truyền lại về sau")', 40, 'vị trí cụ thể chưa có; không vẽ phòng tuyến thành đường cụ thể trên bản đồ')
# --- M6
add('M6', DL, 'Quảng Nguyên, Tư Lang, Tô Mậu: vị trí các châu', '52-53', 'vị trí và tên nay có nguồn')
add('M6', DL, 'Thuận Châu (tên mới của Quảng Nguyên từ năm một nghìn không trăm bảy mươi chín): vị trí', 57, 'vị trí; xác nhận cùng vùng đất với Quảng Nguyên')
add('M6', DL, 'Trại Vĩnh Bình (nơi đàm phán năm một nghìn không trăm tám mươi tư): vị trí', 59, 'vị trí có nguồn')
add('M6', DL, 'Sáu huyện và ba động được trả lại (kịch bản không nêu tên)', 59, 'tên và vị trí từng nơi; nếu chưa có thì KHÔNG đánh dấu, chỉ ghi chữ trên màn hình')
add('M6', DL, 'Ranh giới trước và sau khi trả đất', '53, 57, 59', 'nguồn về ranh giới; không tự vẽ đường biên')
add('M6', DG, 'Trình tự trả đất theo năm (một nghìn không trăm bảy mươi chín, một nghìn không trăm tám mươi tư)', '57, 59', 'mốc năm đối chiếu nguồn; thể hiện bằng nhãn năm, không bằng đường biên')
# --- M7
add('M7', DL, 'Diễn Châu: vị trí', 61, 'vị trí châu thời Lý và tên nay')
add('M7', DG, 'Lý Giác dấy binh năm một nghìn một trăm linh ba (sự kiện trong kịch bản)', 61, 'chỉ đặt nhãn sự kiện tại Diễn Châu nếu vị trí đã xác minh; không vẽ đường hành quân')
# co_so_kich_ban theo số đoạn của bản tách 90 đoạn (chủ kênh duyệt 01/11/2026); số cũ giữ trong co_so_kich_ban_ban_cu
import re as _re
_AX = json.load(open(f'{D}/../../thu-giong-hai/lt1v4_tach_anh-xa.json', encoding='utf-8'))['vi_tri_cu_sang_moi']
def _moi(t):
    def r(m):
        a_, b_ = int(m.group(1)), int(m.group(2) or m.group(1)); return f'{min(_AX[str(a_)])}-{max(_AX[str(b_)])}' if a_ != b_ or len(_AX[str(a_)]) > 1 else str(_AX[str(a_)][0])
    return _re.sub(r'(\d+)(?:-(\d+))?', r, t)
for _k in n.values():
    for _x in _k:
        if _x['co_so_kich_ban'] != '-': _x['co_so_kich_ban_ban_cu'] = _x['co_so_kich_ban']; _x['co_so_kich_ban'] = _moi(_x['co_so_kich_ban'])
out = dict(project='lt1v4', quy_tac=['Không tự đặt tọa độ hay đường biên.', 'Không tạo bản đồ chỉ dựa trên suy đoán.', 'Ba loại thông tin tách riêng: DIA_LY (dữ kiện địa lý), DUONG_QUAN_SU (đường tiến quân/rút lui), DIEN_GIAI (diễn giải lịch sử).',
                                'Mục chỉ được vẽ (duoc_ve=true) khi trang_thai=VERIFIED và có nguon_xac_minh; toa_do chỉ điền khi VERIFIED.', 'Cột co_so_kich_ban chỉ cho biết kịch bản nhắc tới điều gì, KHÔNG phải nguồn địa lý.'],
           chu_kenh_duyet_danh_sach=dict(trang_thai='APPROVED', nguoi_duyet='chủ kênh', ngay_duyet='2026-11-01',
               pham_vi='Duyệt DANH SÁCH các mục cần xác minh (33 mục, 7 bản đồ) làm kế hoạch xác minh. KHÔNG phải xác minh: mọi mục vẫn NEEDS_REVIEW, không tọa độ, không đường biên, duoc_ve=false cho tới khi có trang_thai=VERIFIED kèm nguon_xac_minh.'),
           items=[x for k in n.values() for x in k])
json.dump(out, open(f'{D}/ban-do-can-xac-minh.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print({k: len(v) for k, v in n.items()}, sum(len(v) for v in n.values()), 'mục NEEDS_REVIEW')
