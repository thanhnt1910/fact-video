import sys;sys.path.insert(0,'/tmp/gen');from viet_chung import xuat2
# tm13 bản 4 (19/11): viết văn xuôi liền mạch trước (van_xuoi_ban4.txt), rồi chia đoạn theo đoạn văn. Ít dẫn nguồn và phân tích hơn bản 3. Nhãn nhịp chỉ để dựng.
NH=['hook1','hook2','hook4','goc_re','buoc_ngoat','buoc_ngoat','the_nguy','the_nguy','lan1','diem_thap','cao_trao','chi_tiet_nguoi','don_cuoi','don_cuoi','ket']
P=[p.strip() for p in open('/tmp/gen/tm13/van_xuoi_ban4.txt',encoding='utf-8').read().split('\n\n') if p.strip()]
assert len(P)==len(NH),(len(P),len(NH))
xuat2(list(zip(NH,P)),'tm13',188001)
