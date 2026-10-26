"""Kiểm kịch bản đọc giọng TRƯỚC khi gửi Gemini đọc (quy tắc CLAUDE.md, chủ kênh yêu cầu 23/10/2026).
python phim_ban_do/kiem_kich_ban.py <tên> [--ten "Hoằng Tháo=Lưu Hoằng Tháo,..."]
Đầu vào: ke-hoach/thu-giong-hai/<tên>_full.json (n, chuong, tone, text). Thoát mã 1 nếu có ❌.
Mục tiêu: đoạn ngắn, một ý, câu đơn giản để Gemini đọc đúng ngay lần đầu và người nghe hiểu ngay.
"""
import json, os, re, sys
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
ten = sys.argv[1]
d = json.load(open(f'{R}/ke-hoach/thu-giong-hai/{ten}_full.json', encoding='utf-8'))
# tên ngắn -> tên đủ (lời kể luôn ghi đủ họ tên). Có thể thêm bằng --ten
TEN = {'Hoằng Tháo': 'Lưu Hoằng Tháo', 'Tam Kha': 'Dương Tam Kha', 'Đình Nghệ': 'Dương Đình Nghệ', 'Công Tiễn': 'Kiều Công Tiễn',
       'Thừa Mỹ': 'Khúc Thừa Mỹ', 'Khắc Chính': 'Lý Khắc Chính', 'Xương Ngập': 'Ngô Xương Ngập', 'Xương Văn': 'Ngô Xương Văn',
       'Trưng Trắc': 'Trưng Trắc', 'Tô Định': 'Tô Định'}
if '--ten' in sys.argv:
    for kv in sys.argv[sys.argv.index('--ten') + 1].split(','):
        a, b = kv.split('='); TEN[a.strip()] = b.strip()
# cụm nói tắt cấm (phải viết đủ: "thuyền chiến của quân Nam Hán", "thủy triều lên")
TAT = [r'\b(thuyền|chiến thuyền|hạm đội|đất|lãnh thổ) (Nam Hán|Nguyên|Hán|Tống|Đường|Lương)\b', r'(?i)(?<!thủy )\btriều (lên|rút|xuống)\b', r'\bnước (triều|rút|lên|xuống)\b',
       r'\bngười (phương Bắc|Bắc)\b', r'\bngười Việt\b']
# từ cổ cần giải thích ngay trong đoạn (có "nghĩa là", "tức là", "là ... " thì bỏ qua)
CO = ['tiết độ sứ', 'tiết việt', 'nha tướng', 'châu mục', 'châu lỵ', 'triều nghi', 'phẩm phục', 'thanh viện', 'Sùng văn sứ', 'kiệt hiệt', 'thái thú', 'thứ sử', 'Lạc tướng', 'lạc hầu', 'xa giá', 'đại xá', 'thượng thư', 'đồn điền']
GIAI = re.compile(r'(nghĩa là|tức là|là viên|là người|là chức|là cờ|là nơi|là tên|là quan|là vùng|là kinh|là tên gọi)')
bad, warn = [], []
def B(n, m): bad.append(f'❌ {n}: {m}')
def W(n, m): warn.append(f'⚠️ {n}: {m}')
tot = 0
for x in d:
    n, t = x['n'], x['text'].strip(); w = t.split(); tot += len(w)
    sents = [s for s in re.split(r'(?<=[.!?])\s+', t) if s]
    if len(w) > 32: B(n, f'dài {len(w)} chữ (tối đa 32, nên 20–30): tách đoạn')
    elif len(w) > 30: W(n, f'{len(w)} chữ, hơi dài')
    if len(w) < 12: W(n, f'ngắn {len(w)} chữ, dễ thành câu cụt: gộp với đoạn kề hoặc thêm chủ thể, nguyên nhân, bối cảnh (trừ câu hỏi hoặc câu nhấn có chủ ý)')
    if len(sents) > 2: B(n, f'{len(sents)} câu trong một đoạn (tối đa 2)')
    if len(re.findall(r',', t)) > 3: W(n, 'nhiều hơn 3 dấu phẩy, câu dễ bị đọc lệch')
    if re.search(r'[()"“”—–…:;]|\.\.|\d', t): B(n, 'có ký tự dễ đọc sai (ngoặc, ngoặc kép, gạch, hai chấm, chấm phẩy, chấm lửng, chữ số); năm viết bằng chữ')
    for p in TAT:
        m = re.search(p, t)
        if m: B(n, f'nói tắt "{m.group(0)}": viết đủ ("thuyền chiến của quân Nam Hán", "thủy triều lên", "quân Đại Việt"...)')
    for a, full in TEN.items():
        if a == full: continue
        for m in re.finditer(re.escape(a), t):
            if not t[:m.start()].endswith(full[:len(full) - len(a)]):
                B(n, f'tên chưa đủ họ tên: "{a}" -> "{full}"'); break
    # mệnh đề chen giữa chủ ngữ và vị ngữ (dễ bị đọc thành lời lạ: "Nam Việt, tồn tại gần một trăm năm, đã mất")
    for s in sents:
        m = re.match(r'^(Vậy là |Và |Nhưng |Rồi )?([^,]{3,40}), ([^,]{12,}), (đã|sẽ|vẫn|còn|không|bị|được|phải) ', s)
        if m: B(n, f'mệnh đề chen giữa chủ ngữ và vị ngữ: "{s[:60]}": tách thành hai câu')
    for c in CO:
        if re.search(re.escape(c), t, re.I) and not GIAI.search(t): W(n, f'từ cổ "{c}" chưa giải thích ngay trong đoạn: đổi chữ dễ hiểu hoặc thêm "nghĩa là"')
    if not x.get('tone'): W(n, 'thiếu tone')
print(f'{ten}: {len(d)} đoạn, {tot} chữ (~{tot / 3 / 60:.1f} phút ở 3 chữ/giây), trung bình {tot / len(d):.0f} chữ/đoạn')
for l in bad + warn: print(l)
print(f'{len(bad)} lỗi ❌, {len(warn)} cảnh báo ⚠️')
sys.exit(1 if bad else 0)
