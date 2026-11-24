import sys,json;sys.path.insert(0,'/tmp/gen');from viet_chung import xuat2
# tm24 Hai chữ trên cánh tay (1284–1285), phần đầu của cuộc kháng chiến lần hai, tới lời bàn 'lấy nhàn chống mệt' (chủ kênh duyệt chia hai tập 24/11). Hook phương án 1. Mã đoạn 206001.
# Năm viết bằng chữ cả ở trường đọc (không đổi sang số) để Gemini khỏi đọc nhầm năm.
P=[p.strip() for p in open('/tmp/gen/tm24/van_xuoi_ban1.txt',encoding='utf-8').read().split('\n\n') if p.strip()]
NH=['hook1', 'hook2', 'hook2', 'hook2', 'hook4', 'goc_re', 'goc_re', 'goc_re', 'goc_re', 'goc_re', 'goc_re', 'the_nguy', 'the_nguy', 'the_nguy', 'the_nguy', 'the_nguy', 'the_nguy', 'the_nguy', 'the_nguy', 'the_nguy', 'the_nguy', 'the_nguy', 'the_nguy', 'cao_trao', 'cao_trao', 'cao_trao', 'cao_trao', 'cao_trao', 'cao_trao', 'cao_trao', 'cao_trao', 'cao_trao', 'cao_trao', 'cao_trao', 'cao_trao', 'cao_trao', 'cao_trao', 'cao_trao', 'cao_trao', 'buoc_ngoat', 'buoc_ngoat', 'buoc_ngoat', 'buoc_ngoat', 'buoc_ngoat', 'buoc_ngoat', 'buoc_ngoat', 'buoc_ngoat', 'buoc_ngoat', 'buoc_ngoat', 'buoc_ngoat', 'buoc_ngoat', 'buoc_ngoat', 'the_nguy', 'the_nguy', 'the_nguy', 'the_nguy', 'the_nguy', 'the_nguy', 'don_cuoi', 'don_cuoi', 'don_cuoi', 'don_cuoi', 'don_cuoi', 'don_cuoi', 'don_cuoi', 'don_cuoi']
NH=(NH+['don_cuoi']*40)[:len(P)-1]+['ket']
xuat2(list(zip(NH,P)),'tm24',206001)
