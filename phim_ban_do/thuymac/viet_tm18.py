import sys,json;sys.path.insert(0,'/tmp/gen');from viet_chung import xuat2
# tm18 Mai Thúc Loan bản 1 (20/11): hook phương án 2 (vua Đen / tướng giặc), điểm nhấn hai chữ trong một bộ sử (gắn với ông). Mã đoạn 200001.
NH=['hook1','hook2','hook4','goc_re','goc_re','goc_re','goc_re','goc_re','the_nguy','the_nguy','the_nguy','the_nguy','don_cuoi','don_cuoi','cao_trao','cao_trao','cao_trao','don_cuoi','don_cuoi','goc_re','goc_re','goc_re','don_cuoi','don_cuoi','don_cuoi','don_cuoi','ket']
P=[p.strip() for p in open('/tmp/gen/tm18/van_xuoi_ban1.txt',encoding='utf-8').read().split('\n\n') if p.strip()]
assert len(P)==len(NH),(len(P),len(NH))
xuat2(list(zip(NH,P)),'tm18',200001)
p='/tmp/pc/ke-hoach/thu-giong-hai/tm18_full.json';J=json.load(open(p))
for d in J:
    x=d['text'].replace('năm bảy trăm hai mươi hai','năm 722')
    if x!=d['text']: d['tts']=x
json.dump(J,open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
