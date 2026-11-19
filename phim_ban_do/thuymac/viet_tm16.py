import sys,json;sys.path.insert(0,'/tmp/gen');from viet_chung import xuat2
# tm16 Bà Triệu bản 1 (19/11): văn xuôi liền mạch theo mạch truyện đã duyệt (hook 1). Nhãn nhịp mạnh chỉ cho đoạn nổi dậy và trận đánh.
NH=['hook1','hook2','hook4','goc_re','goc_re','don_cuoi','don_cuoi','the_nguy','goc_re','goc_re','don_cuoi','cao_trao','cao_trao','cao_trao','don_cuoi','don_cuoi','don_cuoi','don_cuoi','don_cuoi','don_cuoi','don_cuoi','ket']
P=[p.strip() for p in open('/tmp/gen/tm16/van_xuoi_ban1.txt',encoding='utf-8').read().split('\n\n') if p.strip()]
assert len(P)==len(NH),(len(P),len(NH))
xuat2(list(zip(NH,P)),'tm16',196001)
p='/tmp/pc/ke-hoach/thu-giong-hai/tm16_full.json';J=json.load(open(p))
Y=[('hai trăm bốn mươi tám','248')]
for d in J:
    x=d['text']
    for a,b in Y: x=x.replace('năm '+a,'năm '+b).replace('Năm '+a,'Năm '+b)
    if x!=d['text']: d['tts']=x
json.dump(J,open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
