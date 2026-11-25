import sys,json;sys.path.insert(0,'/tmp/gen');from viet_chung import xuat2
# tm26 Thuyền lương ở Vân Đồn (1287–1288): Trần Khánh Dư bán than, nón Ma Lôi, đánh đoàn thuyền lương. Hook phương án 1 (chủ kênh duyệt 25/11). Bản 2: mở rộng trận Vân Đồn theo Nguyên sử. Mã đoạn 208001.
# Năm viết bằng chữ cả ở trường đọc (không đổi sang số) để Gemini khỏi đọc nhầm năm.
P=[p.strip() for p in open('/tmp/gen/tm26/van_xuoi_ban2.txt',encoding='utf-8').read().split('\n\n') if p.strip()]
NH=['hook1','hook2','hook2','hook4']+['goc_re']*4+['the_nguy']*18+['buoc_ngoat']*9+['cao_trao']*10+['buoc_ngoat']*9+['don_cuoi']
NH=(NH+['don_cuoi']*40)[:len(P)-1]+['ket']
xuat2(list(zip(NH,P)),'tm26',208001)
