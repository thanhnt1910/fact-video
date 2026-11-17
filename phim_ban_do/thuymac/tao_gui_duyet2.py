# Hồ sơ gửi duyệt lời đọc theo khung cố định (quy-tac/thuy-mac-khung.md). Chạy trong thư mục repo.
import json,subprocess,re,os
src=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'tao_gui_duyet.py')).read()
ns={};exec(src[:src.index('def run')],ns);M=ns['M']   # dùng lại phần ghi chú hook, nguồn của bản trước

# Bản viết lại theo bài mẫu tm5 (17/11/2026): thay phương án hook và ghi chú độ chắc
import sys
M2={
'tm6':dict(hook=['(Đang dùng) Câu hỏi cho người nghe: có dám đáp "năm nay đánh giặc nhàn"? Trần Quốc Tuấn đã đáp vậy; hứa hai thứ: thuyền lương, sông cũ.','Nghịch lý: người nói "đánh giặc nhàn" mấy tháng sau phải bỏ trống kinh thành.','Số phận nhân vật: Ô Mã Nhi, kẻ phá lăng vua Trần, bị bắt sống trên sông Bạch Đằng.'],
 chac=['Câu "năm nay đánh giặc nhàn": Toàn thư. CẦN đối chiếu câu chữ.','Trần Khánh Dư thua trận đầu, bị sai bắt về kinh, xin hoãn để lập công: Toàn thư.','Ô Mã Nhi phá lăng vua Trần Thái Tông ở Long Hưng: Toàn thư.','Lời thề chỉ xuống sông Bạch Đằng: Toàn thư. CẦN đối chiếu câu chữ.','Hơn bốn trăm thuyền bị bắt; bắt sống Ô Mã Nhi, Phàn Tiếp, Tích Lệ Cơ: Toàn thư.']),
'tm7':dict(hook=['(Đang dùng) Câu hỏi: biết trước ám hiệu tấn công của đạo quân đông hơn, bạn làm gì? Lam Sơn chọn nằm im; hứa hai thứ: do thám, tiếng súng.','Trận chiến: quân Minh đi tắt vào ruộng lầy im phăng phắc.','Số phận nhân vật: Vương Thông sang giữ đất, bị nhốt trong thành mình giữ.'],
 chac=['Bắt do thám, lộ kế ba đường và ám hiệu tiếng súng: Toàn thư. CẦN đối chiếu nguyên văn.','Số quân Minh chết: sử ta và Minh sử ghi khác nhau, đã nói cả hai trong lời đọc.','Trần Hiệp, Lý Lượng chết; Vương Thông bị thương: Toàn thư, Bình Ngô đại cáo.']),
'tm8':dict(hook=['(Đang dùng) Câu hỏi: kẻ địch cứ đánh rồi lùi, bạn có đuổi không? Liễu Thăng đã đuổi; hứa hai thứ: ngọn núi, con dấu.','Số phận nhân vật: chủ tướng mười vạn quân chết với hơn trăm kỵ binh.','Nghịch lý: Lê Lợi không đánh thành mà thắng cả hai đạo cứu viện.'],
 chac=['Lê Lợi không đánh thành, chờ đánh viện binh: Toàn thư. CẦN đối chiếu.','Hơn một trăm kỵ binh vượt lên trước, chết ở Mã Yên ngày hai mươi tháng Chín: Toàn thư.','Hoàng Phúc được tha vì từng làm quan ở nước ta: CẦN đối chiếu lý do.','Đưa thư và dấu của Liễu Thăng cho Mộc Thạnh xem: Việt Nam sử lược. CẦN kiểm với Toàn thư.']),
'tm9':dict(hook=['(Đang dùng) Câu hỏi: thua trên đất mình, có mời quân nước khác vào không? Nguyễn Ánh đã mời; hứa hai thứ: việc quân Xiêm làm ở Gia Định, khúc sông.','Trận chiến: đoàn thuyền xuôi sông, hai bờ im lặng.','Số phận nhân vật: người cầu cứu lại chạy sang chính nước đã cầu cứu.'],
 chac=['Quân số Xiêm: Đại Nam thực lục.','Quân Xiêm cướp phá, dân oán: Đại Nam thực lục. CẦN đối chiếu câu chữ.','Ngày đánh: sách ghi 19 hoặc 20 tháng 1 năm 1785; lời đọc chỉ nói "một ngày tháng Giêng".','Khúc sông, cù lao Thới Sơn, phục binh: nghiên cứu hiện đại.','Câu "sợ như sợ cọp": Đại Nam thực lục. CẦN đối chiếu.']),
'tm10':dict(file='tm10-ngoc-hoi-dong-da-1789',ten='Ngọc Hồi, Đống Đa 1789',
 hook=['(Đang dùng) Câu hỏi: đánh đạo quân đông hơn, có dám hẹn trước ngày ăn mừng? Quang Trung hẹn mồng bảy, vào thành mồng năm; hứa hai thứ: Tết ăn trước, ván phủ rơm ướt.','Số phận nhân vật: vua được phong An Nam quốc vương rồi chết nơi đất khách với một chức quan nhỏ.','Trận chiến: những bức ván rơm ướt tiến về lũy Ngọc Hồi lúc rạng sáng.'],
 chac=['Lời hẹn mồng bảy, ăn Tết trước, ván phủ rơm ướt, hai mươi người một tấm, Tôn Sĩ Nghị không kịp đóng yên: Hoàng Lê nhất thống chí (tiểu thuyết lịch sử), lời đọc đã gắn "theo lời kể cũ".','Hai mươi chín vạn quân Thanh: sử ta; sử nhà Thanh ghi ít hơn.','Ngô Văn Sở rút về Tam Điệp theo kế Ngô Thì Nhậm; Nguyễn Huệ lên ngôi ở Phú Xuân: Cương mục, Đại Nam chính biên liệt truyện.','Sầm Nghi Đống tự tử ở Khương Thượng (Đống Đa); cầu phao đứt: Cương mục.','Lê Chiêu Thống sang Thanh được chức tá lĩnh, chết năm 1793: CẦN đối chiếu.'],
 canh='Nhiều đoạn có 4–5 tên riêng; bản đồ sẽ hiện tên đất.'),
}
for k,v in M2.items(): M.setdefault(k,{}).update(v)
if len(sys.argv)>1: M={k:M[k] for k in sys.argv[1:]}
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
