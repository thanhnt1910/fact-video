import sys,json;sys.path.insert(0,'/tmp/gen');from viet_chung import xuat2
# tm25 Ba bến sông (1285): quân nhà Trần đánh trở lại, Hàm Tử, Chương Dương, Tây Kết, ống đồng. Hook phương án 1 (chủ kênh duyệt 25/11). Mã đoạn 207001.
# Năm viết bằng chữ cả ở trường đọc (không đổi sang số) để Gemini khỏi đọc nhầm năm.
P=[p.strip() for p in open('/tmp/gen/tm25/van_xuoi_ban1.txt',encoding='utf-8').read().split('\n\n') if p.strip()]
NH=['hook1', 'hook2', 'hook2', 'hook4', 'goc_re', 'goc_re', 'goc_re', 'goc_re', 'the_nguy', 'the_nguy', 'the_nguy', 'the_nguy', 'the_nguy', 'the_nguy', 'the_nguy', 'the_nguy', 'cao_trao', 'cao_trao', 'cao_trao', 'cao_trao', 'cao_trao', 'cao_trao', 'cao_trao', 'cao_trao', 'cao_trao', 'cao_trao', 'cao_trao', 'cao_trao', 'cao_trao', 'cao_trao', 'cao_trao', 'buoc_ngoat', 'buoc_ngoat', 'buoc_ngoat', 'buoc_ngoat', 'buoc_ngoat', 'buoc_ngoat', 'buoc_ngoat', 'cao_trao', 'cao_trao', 'cao_trao', 'cao_trao', 'cao_trao', 'cao_trao', 'cao_trao', 'cao_trao', 'cao_trao', 'cao_trao', 'cao_trao', 'cao_trao', 'don_cuoi', 'don_cuoi', 'don_cuoi', 'don_cuoi']
NH=(NH+['don_cuoi']*40)[:len(P)-1]+['ket']
xuat2(list(zip(NH,P)),'tm25',207001)
