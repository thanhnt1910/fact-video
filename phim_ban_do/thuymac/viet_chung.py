import json
def xuat(S,ma,base):
    json.dump([{'n':base+i,'chuong':c,'tone':'story','text':t,'hien':t} for i,(c,t) in enumerate(S)],open(f'ke-hoach/thu-giong-hai/{ma}_full.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
    tot=sum(len(t.split()) for c,t in S);acc=0;seen=set();ch=[]
    for i,(c,t) in enumerate(S):
        if c not in seen: seen.add(c);ch.append((c,i+1,acc/tot))
        acc+=len(t.split())
    print(len(S),'đoạn',tot,'chữ ~',round(tot/3.1/60,1),'phút |',' '.join(f'C{c}@{i}:{p:.0%}' for c,i,p in ch))

def xuat2(S,ma,base):
    """S: danh sách (nhịp, lời). Chương suy ra từ nhịp theo quy-tac/thuy-mac-khung.md."""
    ch=[];c=0;truoc=None
    def nhom(n):
        if n.startswith('hook'): return 'hook'
        if n in ('the_nguy','diem_thap'): return 'nguy'
        if n in ('lang','cao_trao','chi_tiet_nguoi'): return 'cao'
        return n
    for n,t in S:
        g=nhom(n)
        if g!=truoc: c+=1;truoc=g
        ch.append(c)
    json.dump([{'n':base+i,'chuong':ch[i],'nhip':n,'tone':'story','text':t,'hien':t} for i,(n,t) in enumerate(S)],open(f'ke-hoach/thu-giong-hai/{ma}_full.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
    tot=sum(len(t.split()) for n,t in S);print(len(S),'đoạn',tot,'chữ ~',round(tot/3.1/60,1),'phút')
