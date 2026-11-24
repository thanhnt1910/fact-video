#!/usr/bin/env python3
"""Kiểm khung nhịp cố định của series thủy mặc (quy-tac/thuy-mac-khung.md).

Cách dùng: python phim_ban_do/kiem_khung.py <mã>
  - đọc ke-hoach/thu-giong-hai/<mã>_khung.json (bảng khung, bước 1)
  - nếu ke-hoach/thu-giong-hai/<mã>_full.json có trường "nhip" ở mỗi đoạn thì kiểm luôn lời đọc (bước 2)
❌ = lỗi thật, phải sửa trước khi gửi duyệt (sự việc, nguồn, câu sáo đã bị chê); ⚠️ = gợi ý, ghi lý do trong hồ sơ gửi duyệt.
Từ 18/11/2026 (chủ kênh duyệt, ke-hoach/kiem-khung-bang-chi-tiet-18-11.md): mọi kiểm cấu trúc theo khung nhịp chỉ còn ⚠️;
không có <mã>_khung.json thì bỏ qua phần khung (bỏ qua không có nghĩa là kịch bản đạt).
"""
import json, os, re, sys

THU_TU = ['hook1', 'hook2', 'hook3', 'hook4', 'goc_re', 'the_nguy', 'diem_thap', 'buoc_ngoat', 'lan', 'cao', 'don_cuoi', 'ket']
CAO = {'lang', 'cao_trao', 'chi_tiet_nguoi'}          # khối cao trào, thứ tự bên trong tự do
BAT_BUOC = ['hook1', 'hook2', 'hook3', 'hook4', 'goc_re', 'the_nguy', 'diem_thap', 'buoc_ngoat',
            'lang', 'cao_trao', 'chi_tiet_nguoi', 'don_cuoi', 'ket']
MOT_DOAN = {'hook1', 'hook2', 'hook3', 'hook4', 'diem_thap', 'lang', 'chi_tiet_nguoi'}
TEN = {'hook1': 'Hook 1: câu kể thường', 'hook2': 'Hook 2: lật lại', 'hook3': 'Hook 3: tên, nơi, hệ quả',
       'hook4': 'Hook 4: câu hỏi + lời hứa N', 'goc_re': 'Gốc rễ', 'the_nguy': 'Thế nguy',
       'diem_thap': 'Điểm thấp nhất', 'buoc_ngoat': 'Bước ngoặt', 'lan': 'Lần / trận', 'lang': 'Đoạn lặng',
       'cao_trao': 'Cao trào', 'chi_tiet_nguoi': 'Chi tiết con người', 'don_cuoi': 'Dồn cuối', 'ket': 'Kết'}

# Câu sáo, văn máy, từ dịch sát mà chủ kênh đã chê. Từ 18/11/2026 phân loại (ke-hoach/kiem-khung-b4-34-cum-18-11.md):
#   N1 = ❌ chặn: cụm sáo, gần như không hợp giọng kể.
#   CHO = ❌ tạm giữ: chờ chủ kênh xem cách dùng thật rồi quyết N1 hay N2.
#   LAP = ⚠️ chỉ khi một kịch bản dùng từ LAP_NGUONG lần trở lên (cụm thông dụng: dùng một hai lần là tự nhiên).
#   N2 = ⚠️ mỗi lần gặp: có thể đúng ngữ cảnh, cần xem lại. Công cụ chỉ nêu lý do và gợi ý, không tự sửa câu.
# Không đánh đồng từ ngữ với cách viết: cùng một cụm có thể sáo ở câu này, tự nhiên ở câu khác.
CAM = ['ông ta', 'Ông ta', 'quân Đại Việt yếu dần', 'quân ta yếu dần', 'bắt đầu lùi', 'đang lùi dần', 'dấy được dân', 'dấy dân', 'mộ quân', 'mộ mười vạn', 'giữ lấy châu', 'xưng đế', 'hào trưởng', 'xuất chúng', 'tính kế', 'thổi phồng thế giặc', 'lấy công', 'việc thành thì', 'bước ngoặt quan trọng', 'chi tiết đặc biệt', 'nổi tiếng nhất', 'không thể quên', 'quyết liệt',
       'mạnh mẽ', 'rơi vào tay', 'thất thủ', 'điều đáng chú ý', 'có thể thấy', 'không chỉ', 'bảo toàn lực lượng',
       'được tổ chức', 'câu trả lời nằm ở', 'muốn trả lời', 'coi chung', 'núng thế', 'sắm sửa', 'dấy binh',
       'đặt làm', 'bên này', 'phía bên kia', 'có thể hiểu vì sao', 'kinh hoàng', 'khủng khiếp', 'chấn động',
       'định mệnh', 'không ai ngờ', 'giữ trọn', 'bài học', 'tinh thần quân giặc', 'cục diện', 'trong khi chờ', 'quân thuyền']
CAM_N1 = ['có thể thấy', 'điều đáng chú ý', 'quân thuyền']
CAM_CHO = ['câu trả lời nằm ở']
CAM_LAP = ['không chỉ', 'bài học', 'phía bên kia', 'dấy binh']
LAP_NGUONG = 3
CAM_N2 = [c for c in CAM if c not in CAM_N1 + CAM_CHO + CAM_LAP]

# Nói tắt tên phe ("quân Nguyên", "quân Minh"...): từ 18/11/2026 KHÔNG còn báo lỗi hàng loạt.
# Cách gọi này dùng tự nhiên được khi phe đã được giới thiệu rõ ("nhà Nguyên", "nước Xiêm"...) ở đoạn trước hoặc trong cùng đoạn.
# Chỉ cảnh báo ⚠️ một lần cho mỗi phe, ở lần đầu "quân X" xuất hiện mà chưa có giới thiệu đầy đủ trước đó.
PHE = ['Nam Hán', 'Hán', 'Nguyên', 'Minh', 'Tống', 'Thanh', 'Trần', 'Lý', 'Lê', 'Tây Sơn', 'Xiêm', 'Chiêm']
TAT_QUAN = re.compile(r'(?<![\w])quân (' + '|'.join(PHE) + r')\b')

def gioi_thieu(phe):
    """regex của lời giới thiệu đầy đủ phe này (không tính 'quân X' rút gọn)"""
    x = re.escape(phe) if phe != 'Hán' else r'(?<!Nam )Hán'
    return re.compile(r'\b(nhà|triều|nước|vua|quân nhà|quân nước|đế quốc|người|vương triều|họ|tướng|binh)\s+' + x + r'\b|\b' + x + r'\s+(Mông|quốc)\b', re.I)

def kiem_tat(J, canh):
    da = set()
    for d in J:
        t = d['text']
        for m in TAT_QUAN.finditer(t):
            phe = m.group(1)
            if phe in da: continue
            truoc = ' '.join(x['text'] for x in J[:J.index(d)]) + ' ' + t[:m.start()]
            if not gioi_thieu(phe).search(truoc):
                canh.append(f'⚠️ {d["n"]}: "quân {phe}" xuất hiện lần đầu mà chưa giới thiệu phe này (nhà/nước {phe}...) trước đó; người nghe có thể không biết là lực lượng nào')
            da.add(phe)

def nhom(n):
    return 'cao' if n in CAO else ('lan' if re.match(r'lan\d', n) else n)

def kiem_thu_tu(ds, canh, nguon):
    """ds: danh sách tên nhịp theo thứ tự xuất hiện"""
    hang = [THU_TU.index(nhom(n)) if nhom(n) in THU_TU else -1 for n in ds]
    for i, (n, h) in enumerate(zip(ds, hang)):
        if h < 0: canh.append(f'⚠️ {nguon}: nhịp lạ "{n}" (không thuộc khung cũ; không bắt buộc)')
        elif i and h < hang[i - 1] and hang[i - 1] >= 0:
            canh.append(f'⚠️ {nguon}: nhịp "{n}" đứng sau "{ds[i-1]}" (khác thứ tự khung cũ; thứ tự do mạch nhân quả quyết định)')
    for n in BAT_BUOC:
        if n not in ds: canh.append(f'⚠️ {nguon}: không có nhịp "{TEN[n]}" (không ép mọi câu chuyện có đủ nhịp)')
    # khối cao trào phải liền nhau
    vt = [i for i, n in enumerate(ds) if n in CAO]
    if vt and vt[-1] - vt[0] + 1 != len(vt): canh.append(f'⚠️ {nguon}: khối cao trào (lặng, cao trào, chi tiết con người) bị cắt ngang (cách chia khối không bắt buộc)')

def main(ma):
    goc = os.path.join(os.path.dirname(__file__), '..', 'ke-hoach', 'thu-giong-hai')
    loi, canh, bo_qua = [], [], []
    kpath = os.path.join(goc, f'{ma}_khung.json')
    K = json.load(open(kpath, encoding='utf-8')) if os.path.exists(kpath) else None
    if K is None:
        print(f'== {ma}: không có {ma}_khung.json, bỏ qua phần khung (không có nghĩa là kịch bản đạt); vẫn kiểm câu chữ')
    else:
        nh = K['nhip']; ds = [x['nhip'] for x in nh]
        print(f'== {ma}: khung {len(nh)} nhịp, lời hứa: {K.get("loi_hua")}')
        kiem_thu_tu(ds, canh, 'khung')
        for n in MOT_DOAN:
            if ds.count(n) > 1: canh.append(f'⚠️ khung: "{TEN[n]}" có {ds.count(n)} đoạn (một ý có thể cần nhiều đoạn để kể rõ)')
        for x in nh:
            if not x.get('su_viec', '').strip(): loi.append(f'❌ khung: nhịp "{x["nhip"]}" chưa có sự việc')
            if not x['nhip'].startswith('hook4') and not x.get('nguon', '').strip():
                loi.append(f'❌ khung: nhịp "{x["nhip"]}" chưa ghi nguồn')
        if K.get('n_hua') is not None and 'dem' in K:
            if len(K['dem']) != K['n_hua']:
                canh.append(f'⚠️ khung: lời hứa {K["n_hua"]} nhưng có {len(K["dem"])} câu đếm (câu đếm không bắt buộc)')
        else:
            bo_qua.append('số câu đếm (khung không khai báo n_hua/dem)')
        if not K.get('hinh_anh'): bo_qua.append('hình ảnh xuyên suốt (khung không khai báo)')
        tong = sum(x.get('doan', 1) for x in nh); acc = 0; moc = {}
        for x in nh:
            moc.setdefault(nhom(x['nhip']), acc / tong); acc += x.get('doan', 1)
        duoi = sum(x.get('doan', 1) for x in nh if nhom(x['nhip']) in ('don_cuoi', 'ket'))
        if not 24 <= tong <= 42: canh.append(f'⚠️ khung: {tong} đoạn dự kiến (nên 24–42)')
        if moc.get('buoc_ngoat', 0) > .5: canh.append(f'⚠️ khung: bước ngoặt ở mốc {moc["buoc_ngoat"]:.0%} (nên ≤50%)')
        if not .55 <= moc.get('cao', 0) <= .85: canh.append(f'⚠️ khung: cao trào ở mốc {moc.get("cao",0):.0%} (nên 55–85%)')
        if duoi > 5: canh.append(f'⚠️ khung: phần sau cao trào {duoi} đoạn (hơn 5): đánh giá đoạn kết có thực sự cần thiết không; không mặc định cắt xuống 5 đoạn')

    J = json.load(open(os.path.join(goc, f'{ma}_full.json'), encoding='utf-8'))
    if K is not None and all('nhip' in d for d in J):
        nh = K['nhip']; ds = [x['nhip'] for x in nh]
        print(f'   lời đọc: {len(J)} đoạn có gắn nhịp')
        ds2 = [d['nhip'] for d in J]
        # gộp các đoạn liền nhau cùng nhịp
        gon = [n for i, n in enumerate(ds2) if i == 0 or n != ds2[i - 1]]
        kiem_thu_tu(gon, canh, 'lời đọc')
        thieu = [n for n in dict.fromkeys(ds) if n not in ds2]
        if thieu: canh.append(f'⚠️ lời đọc: chưa có các nhịp của khung: {thieu} (lời đọc không bắt buộc tái hiện đủ khung)')
        w = [len(d['text'].split()) for d in J]; tw = sum(w); acc = 0; m2 = {}
        for d, k in zip(J, w):
            m2.setdefault(nhom(d['nhip']), acc / tw); acc += k
        print('   mốc: ' + ', '.join(f'{TEN.get(k, k) if k not in ("lan", "cao") else {"lan": "Lần/trận", "cao": "Khối cao trào"}[k]} {v:.0%}' for k, v in m2.items()))
        sau = sum(1 for d in J if nhom(d['nhip']) in ('don_cuoi', 'ket'))
        if sau > 5: canh.append(f'⚠️ lời đọc: phần sau cao trào {sau} đoạn (hơn 5): đánh giá đoạn kết có thực sự cần thiết không; không mặc định cắt xuống 5 đoạn')
        if not .55 <= m2.get('cao', 0) <= .85: canh.append(f'⚠️ lời đọc: khối cao trào bắt đầu ở mốc {m2.get("cao",0):.0%} (nên 55–85%)')
        low = [d['text'].lower() for d in J]
        ha = [h.lower() for h in K.get('hinh_anh', [])]
        if ha:
            co = [i for i, t in enumerate(low) if any(h in t for h in ha)]
            if not any(i < 4 for i in co): canh.append('⚠️ lời đọc: hình ảnh xuyên suốt không có ở hook (không ép gài cho đủ số lần)')
            if len(J) - 1 not in co: canh.append('⚠️ lời đọc: câu kết không quay về hình ảnh xuyên suốt')
            if len(co) < 3: canh.append(f'⚠️ lời đọc: hình ảnh xuyên suốt chỉ xuất hiện {len(co)} lần (gợi ý ≥3, không ép)')
        # câu hỏi xuyên suốt: chỉ nhắc, không ép thêm câu cho đủ
        sc = [x.lower() for x in K.get('soi_chi', [])]
        if sc:
            cuoi = {}
            for i, d in enumerate(J):
                if d['nhip'] == 'hook4' or d['nhip'] == 'buoc_ngoat' or re.match(r'lan\d', d['nhip']): cuoi[d['nhip']] = i
            for n, i in cuoi.items():
                if not any(x in low[i] for x in sc):
                    canh.append(f'⚠️ lời đọc: đoạn cuối của nhịp "{n}" ({J[i]["n"]}) không nhắc lại câu hỏi xuyên suốt ({", ".join(K["soi_chi"])}); đừng thêm câu chỉ để nhắc lại')
        else:
            bo_qua.append('câu hỏi xuyên suốt (khung không khai báo soi_chi)')
        than = ' '.join(low[4:])
        dem = K.get('dem')
        if dem:
            for pdem in dem:
                if pdem.lower() not in than: canh.append(f'⚠️ lời đọc: không thấy câu đếm "{pdem}" (câu đếm không bắt buộc)')
        else:
            bo_qua.append('thân bài có câu đếm (khung không khai báo dem)')
    elif K is not None:
        print('   lời đọc: chưa gắn nhịp (bước 2 chưa làm)')
    dem_lap = {c: [] for c in CAM_LAP}
    for d in J:  # kiểm câu chữ cho mọi bản, có khung hay không
        tl = d['text'].lower()
        for c in CAM_N1 + CAM_CHO:
            if c in tl: loi.append(f'❌ {d["n"]}: câu sáo hoặc từ đã bị chê "{c}"' + (' (tạm giữ ❌, chờ chủ kênh quyết N1 hay N2)' if c in CAM_CHO else ''))
        for c in CAM_N2:
            if c in tl: canh.append(f'⚠️ {d["n"]}: "{c}" dễ thành câu sáo hoặc dịch sát; xem ngữ cảnh, nếu nghe tự nhiên thì giữ, nếu không thì nói cụ thể ai làm gì')
        for c in CAM_LAP:
            if c in tl: dem_lap[c].append(d['n'])
    for c, ds_ in dem_lap.items():
        if len(ds_) >= LAP_NGUONG:
            canh.append(f'⚠️ "{c}" dùng {len(ds_)} lần (đoạn {", ".join(map(str, ds_))}): dùng nhiều thì dễ thành thói quen; xem lại các chỗ chưa cần')
    kiem_tat(J, canh)
    if bo_qua:
        print('   ℹ️ bỏ qua vì thiếu dữ liệu (bỏ qua không có nghĩa là đạt): ' + '; '.join(bo_qua))
    for x in loi + canh: print(x)
    print(f'   -> {len(loi)} ❌, {len(canh)} ⚠️')
    return 1 if loi else 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
