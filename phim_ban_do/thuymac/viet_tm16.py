import sys,json;sys.path.insert(0,'/tmp/gen');from viet_chung import xuat2
# tm16 Bà Triệu bản 2 (20/11): viết lại theo cách mới, khung "câu nói nổi tiếng không có trong sử" (điểm nhấn loại 5, gắn với bà). Mã đoạn mới 199001.
NH=['hook1','hook2','hook4','goc_re','goc_re','don_cuoi','don_cuoi','the_nguy','goc_re','goc_re','cao_trao','don_cuoi','cao_trao','don_cuoi','don_cuoi','goc_re','don_cuoi','don_cuoi','goc_re','ket']
P=[p.strip() for p in open('/tmp/gen/tm16/van_xuoi_ban2.txt',encoding='utf-8').read().split('\n\n') if p.strip()]
assert len(P)==len(NH),(len(P),len(NH))
xuat2(list(zip(NH,P)),'tm16',199001)
p='/tmp/pc/ke-hoach/thu-giong-hai/tm16_full.json';J=json.load(open(p))
for d in J:
    x=d['text'].replace('năm hai trăm bốn mươi tám','năm 248').replace('Năm hai trăm bốn mươi tám','Năm 248')
    if x!=d['text']: d['tts']=x
json.dump(J,open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
