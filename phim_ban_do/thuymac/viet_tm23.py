import sys,json;sys.path.insert(0,'/tmp/gen');from viet_chung import xuat2
# tm23 Bình Lệ Nguyên 1257–1258 bản 1 (24/11): hook phương án 1 (người gan nhất lại khuyên lui), nhân vật chính Lê Phụ Trần. Mã đoạn 205001.
# Năm viết bằng chữ cả ở trường đọc (không đổi sang số) để Gemini khỏi đọc nhầm năm.
P=[p.strip() for p in open('/tmp/gen/tm23/van_xuoi_ban1.txt',encoding='utf-8').read().split('\n\n') if p.strip()]
NH=['hook1','hook2','hook4']+['goc_re']*5+['the_nguy']*3+['cao_trao']*2+['the_nguy']*2+['buoc_ngoat']*4+['the_nguy']+['goc_re']*2+['cao_trao']*2+['goc_re']*2+['cao_trao']*2+['don_cuoi']*3+['goc_re']*2+['don_cuoi']*4
NH=(NH+['don_cuoi']*40)[:len(P)-1]+['ket']
xuat2(list(zip(NH,P)),'tm23',205001)
