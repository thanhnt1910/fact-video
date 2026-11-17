# Hồ sơ gửi duyệt lời đọc theo khung cố định (quy-tac/thuy-mac-khung.md). Chạy trong thư mục repo.
import json,subprocess,re,os
src=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'tao_gui_duyet.py')).read()
ns={};exec(src[:src.index('def run')],ns);M=ns['M']   # dùng lại phần ghi chú hook, nguồn của bản trước
NHAN={'hook1':'Hook 1','hook2':'Hook 2','hook3':'Hook 3','hook4':'Hook 4','goc_re':'Gốc rễ','the_nguy':'Thế nguy','diem_thap':'★ Điểm thấp nhất','buoc_ngoat':'Bước ngoặt','lang':'★ Đoạn lặng','cao_trao':'Cao trào','chi_tiet_nguoi':'★ Chi tiết con người','don_cuoi':'Dồn cuối','ket':'Kết'}
def nhan(n): return NHAN.get(n, f'Lần {n[3:]}' if n.startswith('lan') else n)
BO=['kiem_kich_ban','kiem_mach_ke','kiem_mo_dau','kiem_khung']
for k,m in M.items():
    J=json.load(open(f'ke-hoach/thu-giong-hai/{k}_full.json'));K=json.load(open(f'ke-hoach/thu-giong-hai/{k}_khung.json'))
    w=[len(d['text'].split()) for d in J];tw=sum(w);acc=0;moc=[]
    for x in w: moc.append(acc/tw);acc+=x
    o=[f'# {k}: {K["ten"]} (lời đọc theo khung, gửi duyệt)','',f'{len(J)} đoạn, {tw} chữ, khoảng {tw/3.1/60:.1f} phút. Giọng dự kiến: Charon, hồ sơ C, đọc từng câu. Chưa đọc giọng.',f'Lời hứa: **{K["loi_hua"]}**. Câu đếm: {", ".join(K["dem"])}. Hình ảnh xuyên suốt: "{K["hinh_anh"][0]}".','','## Kịch bản (theo nhịp)']
    truoc=None
    for i,d in enumerate(J):
        if d['nhip']!=truoc: truoc=d['nhip'];o+=['',f'**{nhan(truoc)}** (mốc {moc[i]:.0%})','']
        o.append(f'{i+1}. {d["text"]}')
    def vt(n): return ', '.join(str(i+1) for i,d in enumerate(J) if d['nhip']==n)
    ha=[h.lower() for h in K['hinh_anh']];vha=[str(i+1) for i,d in enumerate(J) if any(h in d['text'].lower() for h in ha)]
    o+=['','## Năm điểm nhấn cố định','',f'1. Hook: đoạn 1–4.',f'2. Điểm thấp nhất: đoạn {vt("diem_thap")}.',f'3. Đoạn lặng trước cao trào: đoạn {vt("lang")}.',f'4. Chi tiết con người: đoạn {vt("chi_tiet_nguoi")}.',f'5. Câu kết quay về hình ảnh mở đầu: hình ảnh xuất hiện ở đoạn {", ".join(vha)}.']
    o+=['','## Ba phương án hook','']+[f'{i+1}. {h}' for i,h in enumerate(m['hook'])]
    o+=['','## Ghi chú độ chắc (nguồn từng nhịp)','']+[f'- {nhan(x["nhip"])}: {x["nguon"]}.' for x in K['nhip']]
    o+=['','Ghi chú thêm:','']+[f'- {re.sub(r" ?\(?(ở )?đoạn \d+[^)]*\)?","",c)}' for c in m['chac']]
    o+=['','## Kết quả bốn bộ kiểm','']
    for c in BO:
        r=subprocess.run(['python3',f'phim_ban_do/{c}.py',k],capture_output=True,text=True).stdout.strip().splitlines()
        last=[l for l in r if re.search(r'lỗi ❌|-> |mở đầu gọn',l)]
        o.append(f'- `{c}.py`: {(last[-1] if last else r[-1]).strip()}')
    o+=['',f'Cảnh báo được chấp nhận: {m["canh"]}','']
    open(f'ke-hoach/{m["file"]}-gui-duyet.md','w').write('\n'.join(o));print(k,'ok')
