import sys,json;sys.path.insert(0,'/tmp/gen');from viet_chung import xuat2
# tm27 Bạch Đằng 1288: lời dọa của Ô Mã Nhi, Chiêu Lăng, sông Bạch Đằng. Hook phương án 1 (chủ kênh duyệt 25/11). Mã đoạn 209001.
# Năm viết bằng chữ cả ở trường đọc (không đổi sang số) để Gemini khỏi đọc nhầm năm.
P=[p.strip() for p in open('/tmp/gen/tm27/van_xuoi_ban1.txt',encoding='utf-8').read().split('\n\n') if p.strip()]
NH=['hook1','hook2','hook2','hook4']+['goc_re']*8+['the_nguy']*11+['cao_trao']*12+['buoc_ngoat']*6+['don_cuoi']*8
NH=(NH+['don_cuoi']*40)[:len(P)-1]+['ket']
xuat2(list(zip(NH,P)),'tm27',209001)
