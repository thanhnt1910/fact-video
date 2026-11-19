import sys;sys.path.insert(0,'/tmp/gen');from viet_chung import xuat2
# tm12 bản mới (19/11): viết văn xuôi liền mạch trước (van_xuoi_ban3.txt) theo mạch truyện chủ kênh duyệt, rồi chia đoạn theo đoạn văn. Nhãn nhịp chỉ để dựng.
NH=['hook1','hook2','hook4','goc_re','goc_re','lan1','cao_trao','don_cuoi','don_cuoi','buoc_ngoat','don_cuoi','don_cuoi','lan1','don_cuoi','don_cuoi','diem_thap','don_cuoi','don_cuoi','don_cuoi','cao_trao','don_cuoi','don_cuoi','lan1','don_cuoi','don_cuoi','cao_trao','don_cuoi','don_cuoi','ket']
# 20/11: nhãn nhịp điều khiển giọng (lan/cao_trao/buoc_ngoat/the_nguy = đọc to, nhanh). Chỉ gắn cho đoạn trận đánh và lúc quyết định; đoạn phân tích để don_cuoi (đọc bình thường).
P=[p.strip() for p in open('/tmp/gen/tm12/van_xuoi_ban3.txt',encoding='utf-8').read().split('\n\n') if p.strip()]
assert len(P)==len(NH),(len(P),len(NH))
xuat2(list(zip(NH,P)),'tm12',187001)

# tts: năm viết bằng chữ số để Gemini không đọc nhầm (557 từng bị đọc thành 555)
import json
p='/tmp/pc/ke-hoach/thu-giong-hai/tm12_full.json';J=json.load(open(p))
Y=[('năm trăm bốn mươi mốt','541'),('năm trăm bốn mươi sáu','546'),('năm trăm bốn mươi bảy','547'),('năm trăm bốn mươi tám','548'),('năm trăm năm mươi bảy','557'),('năm trăm năm mươi lăm','555'),('năm trăm bảy mươi mốt','571'),('năm trăm năm mươi','550')]
for d in J:
    x=d['text']
    for a,b in Y: x=x.replace('năm '+a,'năm '+b).replace('Năm '+a,'Năm '+b)
    if x!=d['text']: d['tts']=x
json.dump(J,open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
print([d['tts'][:0] or [w for w in d['tts'].split() if w[:1].isdigit()] for d in J if 'tts' in d])
