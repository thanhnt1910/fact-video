import sys,json;sys.path.insert(0,'/tmp/gen');from viet_chung import xuat2
# tm17 Lý Bí bản 3 (20/11, khung bí ẩn cái chết, cách viết mới): theo mạch truyện đã duyệt (hook 1, kể gọn 545–548, giữ câu "nhiều bài viết kể khác", có lời cảm ơn). Nhãn nhịp mạnh chỉ cho đoạn nổi dậy và trận đánh.
NH=['hook1', 'hook2', 'hook4', 'goc_re', 'goc_re', 'goc_re', 'don_cuoi', 'don_cuoi', 'don_cuoi', 'the_nguy', 'don_cuoi', 'the_nguy', 'don_cuoi', 'cao_trao', 'goc_re', 'don_cuoi', 'don_cuoi', 'don_cuoi', 'the_nguy', 'cao_trao', 'don_cuoi', 'goc_re', 'the_nguy', 'cao_trao', 'don_cuoi', 'don_cuoi', 'goc_re', 'don_cuoi', 'ket']
P=[p.strip() for p in open('/tmp/gen/tm17/van_xuoi_ban3.txt',encoding='utf-8').read().split('\n\n') if p.strip()]
assert len(P)==len(NH),(len(P),len(NH))
xuat2(list(zip(NH,P)),'tm17',197001)
p='/tmp/pc/ke-hoach/thu-giong-hai/tm17_full.json';J=json.load(open(p))
Y=[('năm trăm bốn mươi mốt','541'),('năm trăm bốn mươi ba','543'),('năm trăm bốn mươi tư','544'),('năm trăm bốn mươi lăm','545'),('năm trăm bốn mươi tám','548')]
for d in J:
    x=d['text']
    for a,b in Y: x=x.replace('năm '+a,'năm '+b).replace('Năm '+a,'Năm '+b)
    if x!=d['text']: d['tts']=x
json.dump(J,open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
