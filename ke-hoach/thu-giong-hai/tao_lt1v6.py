# Kịch bản của chủ kênh (68 đoạn, nguyên văn) + thay RIÊNG các câu còn thắc mắc. Không sửa câu nào khác ngoài: số -> chữ, dấu hai chấm, tách đoạn quá dài.
import json, os, re
D = os.path.dirname(os.path.abspath(__file__))
src = open(f'{D}/kich-ban-chu-kenh-68-doan.md', encoding='utf-8').read().split('\n')
chap = None; items = []
for ln in src:
    m = re.match(r'## CHƯƠNG \d+\. (.+)', ln)
    if m: chap = m.group(1).capitalize(); continue
    m = re.match(r'\*\*(\d+)\.\*\* (.+)', ln)
    if m: items.append((int(m.group(1)), chap, m.group(2).strip()))
# câu thay thế: (số đoạn) -> [(câu cũ, câu mới)]
REP = {
 5: [("Lý Thường Kiệt sinh năm 1019, tên thật là Ngô Tuấn, quê ở phường Thái Hòa, thành Thăng Long theo cách gọi ngày nay.",
      "Các tài liệu thường ghi Lý Thường Kiệt sinh năm 1019, quê ở phường Thái Hòa, thành Thăng Long, nhưng năm sinh còn chưa chắc.")],
 6: [("Ngô Tuấn đã vào triều", "ông đã vào triều")],
 13: [("Các hoạt động tập hợp quân, lương thực và căn cứ hậu cần đặt triều đình nhà Lý trước một lựa chọn khó khăn.",
       "Toàn thư chép rằng hai quan nhà Tống là Thẩm Khởi và Lưu Di ngầm gọi người miền núi vào quân ngũ, đóng thuyền và cấm buôn bán với Đại Việt.")],
 17: [("Sử liệu ghi nhận Đại Việt đưa ra những lý do liên quan đến việc nhà Tống chuẩn bị đánh nước ta.",
       "Theo Toàn thư, lý lẽ quân Đại Việt nêu ra là chính sách thanh miêu của nhà Tống, bắt dân vay tiền rồi trả cả vốn lẫn lãi.")],
 20: [("Đây là các địa điểm có vai trò trong hệ thống quân sự và hậu cần của nhà Tống ở vùng biên giới phía nam.",
       "Đây là hai châu ven biển của nhà Tống, ở phía nam.")],
 22: [("Đại Việt đang nhắm đến những mắt xích trong hệ thống chuẩn bị chiến tranh của đối phương.",
       "Theo Toàn thư, Lý Thường Kiệt còn đón đánh viện binh của nhà Tống ở cửa ải Côn Lôn.")],
 44: [("chủ quyền của người Việt.", "chủ quyền của Đại Việt."), ("trở thành một biểu tượng", "trở thành biểu tượng")],
 51: [("Triều đình nhà Lý lựa chọn con đường thương lượng.", "Theo nhà sử học John Anderson, chính Lý Thường Kiệt đề nghị thương lượng.")],
 56: [("nhà Tống trao trả thêm sáu huyện và ba động theo ghi chép lịch sử.", "nhà Tống trao trả thêm một số huyện và động. Số cụ thể còn cần đối chiếu."), ("các cuộc đàm phán tại Vĩnh Bình", "đàm phán tại Vĩnh Bình")],
}
# chỉ đổi hình thức (không đổi lời): dấu hai chấm -> "là" / dấu phẩy
FORM = {32: [("khó khăn hơn: đối mặt", "khó khăn hơn là đối mặt")], 15: [("câu hỏi lớn: nên chờ", "câu hỏi lớn là nên chờ")],
        41: [("câu chuyện đặc biệt: bài thơ", "câu chuyện đặc biệt là bài thơ")], 49: [("cho Lý Thường Kiệt: khi", "cho Lý Thường Kiệt, khi")],
        64: [(" và tổ chức phòng thủ", ". Hai là tổ chức phòng thủ"), ("cùng nhau: tiến công sang đất Tống", "cùng nhau. Một là tiến công sang lãnh thổ nhà Tống")], 16: [("sang đất Tống", "sang lãnh thổ nhà Tống")]}
U = {0: '', 1: 'một', 2: 'hai', 3: 'ba', 4: 'bốn', 5: 'năm', 6: 'sáu', 7: 'bảy', 8: 'tám', 9: 'chín'}
def two(n, lead0):
    t, u = divmod(n, 10)
    if t == 0: return ('linh ' + U[u]) if lead0 else U[u]
    if t == 1: return 'mười' + (' ' + ('lăm' if u == 5 else U[u]) if u else '')
    s = U[t] + ' mươi'
    if u == 0: return s
    return s + ' ' + {1: 'mốt', 4: 'tư', 5: 'lăm'}.get(u, U[u])
def year(y):
    th, r = divmod(y, 1000); h, r = divmod(r, 100)
    s = U[th] + ' nghìn ' + (U[h] + ' trăm' if h else 'không trăm')
    return s + ((' ' + two(r, True)) if r else '')
def words(t): return re.sub(r'\b(1\d{3})\b', lambda m: year(int(m.group(1))), t)
def chia(t):
    ss = [x for x in re.split(r'(?<=[.!?])\s+', t) if x]
    if len(t.split()) <= 32 and len(ss) <= 2: return [t]
    r = []; cur = ''
    for x in ss:
        if cur and (len((cur + ' ' + x).split()) > 32 or len(re.split(r'(?<=[.!?])\s+', cur + ' ' + x)) > 2): r.append(cur); cur = x
        else: cur = (cur + ' ' + x).strip()
    r.append(cur); return r
out = []; n = 32001; LOG = []
for no, ch, t in items:
    for a, b in REP.get(no, []):
        assert a in t, (no, a); t = t.replace(a, b)
    for a, b in FORM.get(no, []):
        assert a in t, (no, a); t = t.replace(a, b)
    t = words(t)
    for p in chia(t):
        out.append({'n': n, 'chuong': ch, 'tone': 'story', 'text': p, 'goc': no}); n += 1
json.dump(out, open(f'{D}/lt1v6_full.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(out))
