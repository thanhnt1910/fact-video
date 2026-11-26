import sys,json;sys.path.insert(0,'/tmp/gen');from viet_chung import xuat2
# tm28 Chế Bồng Nga và chiếc thuyền sơn xanh (1371–1390). Hook phương án A (chủ kênh duyệt 26/11). Mã đoạn 210001.
P=[p.strip() for p in open('/tmp/gen/tm28/van_xuoi_ban1.txt',encoding='utf-8').read().split('\n\n') if p.strip()]
NH=['hook1','hook2','hook2','hook4']+['goc_re']*7+['the_nguy']*8+['cao_trao']*17+['the_nguy']*12+['buoc_ngoat']*6+['cao_trao']*12+['don_cuoi']*7
NH=(NH+['don_cuoi']*40)[:len(P)-1]+['ket']
xuat2(list(zip(NH,P)),'tm28',210001)
