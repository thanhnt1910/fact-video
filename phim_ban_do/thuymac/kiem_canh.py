"""Kiểm cảnh thủy mặc: python kiem_canh.py <mã>  — mỗi cảnh phải có chuyển động, không hai cảnh trùng nhau.
Chuyển động: khác biệt giữa khung đầu/giữa/cuối cảnh (bỏ phụ đề). Trùng: tương quan khung giữa của các cảnh, và số lần dùng từng tranh."""
import sys,importlib,re,numpy as np
mod=importlib.import_module('dai_'+sys.argv[1]);K=mod.K
SH=[s for s in mod.SH if s[1]-s[0]>1.5]
src=open(mod.__file__).read();paints=re.findall(r"'(t\d+_[a-z0-9]+)'",src)
def g(t):
    f=mod.frame(t);im=np.asarray(f,np.float32)[::6,::6].mean(2) if f.dtype!=np.uint8 else f[::6,::6].mean(2)/255
    return im[:int(im.shape[0]*.8)]
bad=0;mids=[]
for a,b,fn in SH:
    d=b-a;ts=[a+.25*d,a+.5*d,a+.75*d];ims=[g(min(t,b-.2)) for t in ts]
    mv=max(np.abs(ims[0]-ims[1]).mean(),np.abs(ims[1]-ims[2]).mean())
    mids.append(ims[1]);ok=mv>.004;bad+=not ok
    print(f'{fn.__name__:8s} {a:6.1f}-{b:6.1f}  chuyển động {mv:.4f} {"OK" if ok else "❌ TĨNH"}')
sim=0
for i in range(len(mids)):
    for j in range(i+1,len(mids)):
        c=np.corrcoef(mids[i].ravel(),mids[j].ravel())[0,1]
        if c>.97: print('❌ trùng',SH[i][2].__name__,SH[j][2].__name__,round(c,3));sim+=1
from collections import Counter
cn=Counter(paints);dup=[k for k,v in cn.items() if v>2 and False]
print(f'{len(SH)} cảnh, {len(set(paints))} tranh riêng; tĩnh {bad}; trùng {sim}')
