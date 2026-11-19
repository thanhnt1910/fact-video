"""Kiểm cảnh thủy mặc (quy tắc 19/11/2026): python kiem_canh.py <mã>
Chạy với KIEM_TINH=1: máy quay đứng yên, tắt sương, chữ, triện, phụ đề. Chỉ còn chuyển động THẬT trong tranh
(người, ngựa, thuyền, nước, khói, lửa, nét vẽ đang hiện ra). Cảnh nào tỉ lệ điểm ảnh đổi < 0,3% là ❌ TĨNH.
Trùng: tương quan khung giữa của hai cảnh > 0,97 là ❌ TRÙNG; tranh dùng cho hơn một cảnh là ❌."""
import os,sys,importlib,re,numpy as np
from collections import Counter
os.environ['KIEM_TINH']='1'
mod=importlib.import_module('dai_'+sys.argv[1])
SH=[s for s in mod.SH if s[1]-s[0]>1.0]
src=open(mod.__file__).read()
def g(t):
    f=np.asarray(mod.frame(t),np.float32);f=f/255 if f.max()>1.5 else f
    return f[::4,::4].mean(2)
bad=0;mids=[]
for a,b,fn in SH:
    d=b-a;ts=[a+.2*d,a+.5*d,a+.8*d];ims=[g(min(t,b-.15)) for t in ts]
    mv=max((np.abs(ims[0]-ims[1])>.04).mean(),(np.abs(ims[1]-ims[2])>.04).mean())
    mids.append(ims[1]);ok=mv>.003;bad+=not ok
    print(f'{fn.__name__:8s} {a:6.1f}-{b:6.1f}  đổi {mv*100:5.2f}% {"OK" if ok else "❌ TĨNH"}')
sim=0
for i in range(len(mids)):
    for j in range(i+1,len(mids)):
        c=np.corrcoef(mids[i].ravel(),mids[j].ravel())[0,1]
        if c>.97: print('❌ trùng',SH[i][2].__name__,SH[j][2].__name__,round(c,3));sim+=1
uses=Counter()
for fn in [s[2] for s in SH]:
    body=re.search(r'def '+fn.__name__+r'\(.*?(?=\n(?:def |S=|MOV|_J|if FREEZE)|\Z)',src,re.S).group(0)
    for p in set(re.findall(r"'(t\d+_(?!spr)[a-z0-9_]+)'",body)): uses[p]+=1
dup=[k for k,v in uses.items() if v>1]
for k in dup: print('❌ tranh dùng nhiều cảnh:',k)
print(f'{len(SH)} cảnh, {len(uses)} tranh riêng; tĩnh {bad}; trùng {sim}; tranh lặp {len(dup)}')
