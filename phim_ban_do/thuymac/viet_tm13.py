import sys,json;sys.path.insert(0,'/tmp/gen');from viet_chung import xuat2
# tm13 Hai Bà Trưng bản 5 (20/11): viết lại theo cách mới, khung trống đồng (điểm nhấn gắn với Trưng Trắc, con gái Lạc tướng). Mã đoạn mới 198001.
NH=['hook1','hook2','hook4','goc_re','goc_re','don_cuoi','the_nguy','the_nguy','don_cuoi','don_cuoi','goc_re','the_nguy','cao_trao','don_cuoi','cao_trao','don_cuoi','don_cuoi','don_cuoi','goc_re','don_cuoi','goc_re','don_cuoi','ket']
P=[p.strip() for p in open('/tmp/gen/tm13/van_xuoi_ban5.txt',encoding='utf-8').read().split('\n\n') if p.strip()]
assert len(P)==len(NH),(len(P),len(NH))
xuat2(list(zip(NH,P)),'tm13',198001)
p='/tmp/pc/ke-hoach/thu-giong-hai/tm13_full.json';J=json.load(open(p))
Y=[('bốn mươi bốn','44'),('bốn mươi ba','43'),('bốn mươi hai','42'),('bốn mươi','40')]
for d in J:
    x=d['text']
    for a,b in Y: x=x.replace('năm '+a,'năm '+b)
    if x!=d['text']: d['tts']=x
json.dump(J,open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
