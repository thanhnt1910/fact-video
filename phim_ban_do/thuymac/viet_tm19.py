import sys,json;sys.path.insert(0,'/tmp/gen');from viet_chung import xuat2
# tm19 Phùng Hưng bản 1 (21/11): hook phương án 3 (gọi là cha mẹ), điểm nhấn Bố Cái Đại Vương. Mã đoạn 201001.
P=[p.strip() for p in open('/tmp/gen/tm19/van_xuoi_ban1.txt',encoding='utf-8').read().split('\n\n') if p.strip()]
NH=['hook1','hook2','hook4']+['goc_re']*5+['the_nguy']*4+['cao_trao']*2+['don_cuoi']*3+['goc_re']*2+['don_cuoi']*5+['ket']
NH=(NH+['don_cuoi']*40)[:len(P)-1]+['ket']
xuat2(list(zip(NH,P)),'tm19',201001)
p='/tmp/pc/ke-hoach/thu-giong-hai/tm19_full.json';J=json.load(open(p))
for d in J:
    x=d['text'].replace('năm bảy trăm chín mươi mốt','năm 791')
    if x!=d['text']: d['tts']=x
json.dump(J,open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
