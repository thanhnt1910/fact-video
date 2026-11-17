#!/usr/bin/env python3
"""Kiểm khung nhịp cố định của series thủy mặc (quy-tac/thuy-mac-khung.md).

Cách dùng: python phim_ban_do/kiem_khung.py <mã>
  - đọc ke-hoach/thu-giong-hai/<mã>_khung.json (bảng khung, bước 1)
  - nếu ke-hoach/thu-giong-hai/<mã>_full.json có trường "nhip" ở mỗi đoạn thì kiểm luôn lời đọc (bước 2)
❌ = phải sửa trước khi gửi duyệt; ⚠️ = ghi lý do trong hồ sơ gửi duyệt.
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

# Câu sáo, văn máy, từ dịch sát, từ dùng sai mà chủ kênh đã chê (thêm vào đây mỗi lần bị chê)
CAM = ['bước ngoặt quan trọng', 'chi tiết đặc biệt', 'nổi tiếng nhất', 'không thể quên', 'quyết liệt',
       'mạnh mẽ', 'rơi vào tay', 'thất thủ', 'điều đáng chú ý', 'có thể thấy', 'không chỉ', 'bảo toàn lực lượng',
       'được tổ chức', 'câu trả lời nằm ở', 'muốn trả lời', 'coi chung', 'núng thế', 'sắm sửa', 'dấy binh',
       'đặt làm', 'bên này', 'phía bên kia', 'có thể hiểu vì sao', 'kinh hoàng', 'khủng khiếp', 'chấn động',
       'định mệnh', 'không ai ngờ', 'giữ trọn', 'bài học', 'tinh thần quân giặc', 'cục diện']
TAT = re.compile(r'\bquân (Nguyên|Minh|Tống|Thanh|Hán|Nam Hán|Trần|Lý|Lê|Tây Sơn)\b')
TAT_MEM = re.compile(r'\bquân (Xiêm|Chiêm)\b')

def nhom(n):
    return 'cao' if n in CAO else ('lan' if re.match(r'lan\d', n) else n)

def kiem_thu_tu(ds, loi, nguon):
    """ds: danh sách tên nhịp theo thứ tự xuất hiện"""
    hang = [THU_TU.index(nhom(n)) if nhom(n) in THU_TU else -1 for n in ds]
    for i, (n, h) in enumerate(zip(ds, hang)):
        if h < 0: loi.append(f'❌ {nguon}: nhịp lạ "{n}"')
        elif i and h < hang[i - 1] and hang[i - 1] >= 0:
            loi.append(f'❌ {nguon}: nhịp "{n}" đứng sau "{ds[i-1]}" (sai thứ tự khung)')
    for n in BAT_BUOC:
        if n not in ds: loi.append(f'❌ {nguon}: thiếu nhịp "{TEN[n]}"')
    # khối cao trào phải liền nhau
    vt = [i for i, n in enumerate(ds) if n in CAO]
    if vt and vt[-1] - vt[0] + 1 != len(vt): loi.append(f'❌ {nguon}: khối cao trào (lặng, cao trào, chi tiết con người) bị cắt ngang')

def main(ma):
    goc = os.path.join(os.path.dirname(__file__), '..', 'ke-hoach', 'thu-giong-hai')
    K = json.load(open(os.path.join(goc, f'{ma}_khung.json'), encoding='utf-8'))
    loi, canh = [], []
    nh = K['nhip']; ds = [x['nhip'] for x in nh]
    print(f'== {ma}: khung {len(nh)} nhịp, lời hứa: {K.get("loi_hua")}')
    kiem_thu_tu(ds, loi, 'khung')
    for n in MOT_DOAN:
        if ds.count(n) > 1: loi.append(f'❌ khung: "{TEN[n]}" chỉ được có một')
    for x in nh:
        if not x.get('su_viec', '').strip(): loi.append(f'❌ khung: nhịp "{x["nhip"]}" chưa có sự việc')
        if not x['nhip'].startswith('hook4') and not x.get('nguon', '').strip():
            loi.append(f'❌ khung: nhịp "{x["nhip"]}" chưa ghi nguồn')
    if len(K.get('dem', [])) != K.get('n_hua'):
        loi.append(f'❌ khung: lời hứa {K.get("n_hua")} nhưng có {len(K.get("dem", []))} câu đếm')
    if not K.get('hinh_anh'): loi.append('❌ khung: chưa khai báo hình ảnh xuyên suốt')
    tong = sum(x.get('doan', 1) for x in nh); acc = 0; moc = {}
    for x in nh:
        moc.setdefault(nhom(x['nhip']), acc / tong); acc += x.get('doan', 1)
    duoi = sum(x.get('doan', 1) for x in nh if nhom(x['nhip']) in ('don_cuoi', 'ket'))
    if not 24 <= tong <= 42: canh.append(f'⚠️ khung: {tong} đoạn dự kiến (nên 24–42)')
    if moc.get('buoc_ngoat', 0) > .5: canh.append(f'⚠️ khung: bước ngoặt ở mốc {moc["buoc_ngoat"]:.0%} (nên ≤50%)')
    if not .55 <= moc.get('cao', 0) <= .85: canh.append(f'⚠️ khung: cao trào ở mốc {moc.get("cao",0):.0%} (nên 55–85%)')
    if duoi > 5: loi.append(f'❌ khung: phần sau cao trào {duoi} đoạn (tối đa 5)')

    J = json.load(open(os.path.join(goc, f'{ma}_full.json'), encoding='utf-8'))
    if all('nhip' in d for d in J):
        print(f'   lời đọc: {len(J)} đoạn có gắn nhịp')
        ds2 = [d['nhip'] for d in J]
        # gộp các đoạn liền nhau cùng nhịp
        gon = [n for i, n in enumerate(ds2) if i == 0 or n != ds2[i - 1]]
        kiem_thu_tu(gon, loi, 'lời đọc')
        thieu = [n for n in dict.fromkeys(ds) if n not in ds2]
        if thieu: loi.append(f'❌ lời đọc: chưa viết các nhịp của khung: {thieu}')
        w = [len(d['text'].split()) for d in J]; tw = sum(w); acc = 0; m2 = {}
        for d, k in zip(J, w):
            m2.setdefault(nhom(d['nhip']), acc / tw); acc += k
        print('   mốc: ' + ', '.join(f'{TEN.get(k, k) if k not in ("lan", "cao") else {"lan": "Lần/trận", "cao": "Khối cao trào"}[k]} {v:.0%}' for k, v in m2.items()))
        sau = sum(1 for d in J if nhom(d['nhip']) in ('don_cuoi', 'ket'))
        if sau > 5: loi.append(f'❌ lời đọc: phần sau cao trào {sau} đoạn (tối đa 5)')
        if not .55 <= m2.get('cao', 0) <= .85: canh.append(f'⚠️ lời đọc: khối cao trào bắt đầu ở mốc {m2.get("cao",0):.0%} (nên 55–85%)')
        low = [d['text'].lower() for d in J]
        ha = [h.lower() for h in K.get('hinh_anh', [])]
        co = [i for i, t in enumerate(low) if any(h in t for h in ha)]
        if not any(i < 4 for i in co): loi.append('❌ lời đọc: hình ảnh xuyên suốt không có ở hook')
        if len(J) - 1 not in co: loi.append('❌ lời đọc: câu kết không quay về hình ảnh xuyên suốt')
        if len(co) < 3: loi.append(f'❌ lời đọc: hình ảnh xuyên suốt chỉ xuất hiện {len(co)} lần (cần ≥3)')
        # sợi chỉ: câu hỏi xuyên suốt phải được nhắc ở hook 4 và ở đoạn cuối của bước ngoặt và của mỗi lần
        sc = [x.lower() for x in K.get('soi_chi', [])]
        if sc:
            cuoi = {}
            for i, d in enumerate(J):
                if d['nhip'] == 'hook4' or d['nhip'] == 'buoc_ngoat' or re.match(r'lan\d', d['nhip']): cuoi[d['nhip']] = i
            for n, i in cuoi.items():
                if not any(x in low[i] for x in sc):
                    loi.append(f'❌ lời đọc: đoạn cuối của nhịp "{n}" ({J[i]["n"]}) không nhắc lại câu hỏi xuyên suốt ({", ".join(K["soi_chi"])}); sự việc đang bị kể rời như liệt kê')
        else:
            canh.append('⚠️ khung chưa khai báo "soi_chi" (câu hỏi xuyên suốt)')
        than = ' '.join(low[4:])
        for p in K.get('dem', []):
            if p.lower() not in than: loi.append(f'❌ lời đọc: thiếu câu đếm "{p}"')
        if not J[-1]['text'].rstrip().endswith('Cảm ơn bạn đã lắng nghe câu chuyện này.'):
            loi.append('❌ lời đọc: đoạn cuối thiếu lời cảm ơn chuẩn')
    else:
        print('   lời đọc: chưa gắn nhịp (bước 2 chưa làm)')
    for d in J:  # kiểm câu chữ cho mọi bản, có gắn nhịp hay chưa
        t = d['text']; tl = t.lower()
        for c in CAM:
            if c in tl: loi.append(f'❌ {d["n"]}: câu sáo hoặc từ đã bị chê "{c}"')
        m = TAT.search(t)
        if m: loi.append(f'❌ {d["n"]}: nói tắt "{m.group(0)}" (viết "quân nhà ...")')
        m = TAT_MEM.search(t)
        if m: canh.append(f'⚠️ {d["n"]}: "{m.group(0)}" (cân nhắc "quân nước ...")')
    for x in loi + canh: print(x)
    print(f'   -> {len(loi)} ❌, {len(canh)} ⚠️')
    return 1 if loi else 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
