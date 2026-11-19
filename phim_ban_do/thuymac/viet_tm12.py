import sys;sys.path.insert(0,'/tmp/gen');from viet_chung import xuat2
# tm12 bản mới (19/11): viết văn xuôi liền mạch trước (van_xuoi_ban2.txt) theo mạch truyện chủ kênh duyệt, rồi chia đoạn theo đoạn văn. Nhãn nhịp chỉ để dựng.
NH=['hook1','hook2','hook4','goc_re','goc_re','the_nguy','the_nguy','the_nguy','buoc_ngoat','buoc_ngoat','buoc_ngoat','buoc_ngoat','lan1','lan1','lan1','diem_thap','diem_thap','diem_thap','cao_trao','cao_trao','cao_trao','cao_trao','don_cuoi','don_cuoi','don_cuoi','don_cuoi','don_cuoi','don_cuoi','ket']
P=[p.strip() for p in open('/tmp/gen/tm12/van_xuoi_ban2.txt',encoding='utf-8').read().split('\n\n') if p.strip()]
assert len(P)==len(NH),(len(P),len(NH))
xuat2(list(zip(NH,P)),'tm12',187001)
