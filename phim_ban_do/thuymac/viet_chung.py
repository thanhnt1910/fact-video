import json
def xuat(S,ma,base):
    json.dump([{'n':base+i,'chuong':c,'tone':'story','text':t,'hien':t} for i,(c,t) in enumerate(S)],open(f'/tmp/pc/ke-hoach/thu-giong-hai/{ma}_full.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
    tot=sum(len(t.split()) for c,t in S);acc=0;seen=set();ch=[]
    for i,(c,t) in enumerate(S):
        if c not in seen: seen.add(c);ch.append((c,i+1,acc/tot))
        acc+=len(t.split())
    print(len(S),'đoạn',tot,'chữ ~',round(tot/3.1/60,1),'phút |',' '.join(f'C{c}@{i}:{p:.0%}' for c,i,p in ch))
