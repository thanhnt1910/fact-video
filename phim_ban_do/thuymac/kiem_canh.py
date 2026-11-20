"""Kiểm cảnh thủy mặc: python kiem_canh.py <mã>
Bản 19/11: chạy với KIEM_TINH=1 (máy quay đứng yên, tắt sương, chữ, triện, phụ đề); cảnh đổi < 0,3% điểm ảnh là ❌ TĨNH;
khung giữa hai cảnh tương quan > 0,97 là ❌ TRÙNG; tranh dùng cho hơn một cảnh là ❌.
Bản 20/11 (quy tắc "độ chi tiết ngang video Ngô Quyền", thuy-mac.md mục 4) thêm, đếm bằng cách ghi lại mọi lệnh put:
  - LỚP: số hệ số thị sai k khác nhau (lớp trôi khác tốc độ) ở khung giữa, chạy máy quay thật. Dưới 3 là ❌ (cảnh bản đồ được miễn).
  - VẬT ĐỘNG: số vật đổi vị trí, góc hoặc cỡ giữa hai khung cách 0,6 giây khi máy quay đứng yên. Dưới 3 là ❌.
  - MƯỢN: hình nhỏ của tập khác (tNN_spr_* khác mã tập) cho người, quân, thuyền, voi, ngựa là ❌; chim, khói, lửa, nước được mượn."""
import os,sys,importlib,re,numpy as np
from collections import Counter
ma=sys.argv[1];num=re.sub(r'\D','',ma);PRE=f't{num}_'
TRANG_TRI=('chim','khoi','lua','nuoc','mist','bui','tia')
os.environ['KIEM_TINH']='1'
mod=importlib.import_module('dai_'+ma)
import engine
LOG=[]
_orig=engine.put
def _rec(cv,cam,img,x,y,s=1.0,r=0.0,o=1.0,ax=.5,ay=.5,k=1.0,scale_px=1.5,screen=False):
    nm=img if isinstance(img,str) else 'anh'
    if o>.05 and not screen: LOG.append((nm,round(k,2),x,y,s,r))
    return _orig(cv,cam,img,x,y,s=s,r=r,o=o,ax=ax,ay=ay,k=k,scale_px=scale_px,screen=screen)
for m in list(sys.modules.values()):
    try:
        if getattr(m,'put',None) is _orig: m.put=_rec
    except Exception: pass
SH=[s for s in mod.SH if s[1]-s[0]>1.0]
src=open(mod.__file__).read()
def g(t):
    f=np.asarray(mod.frame(t),np.float32);f=f/255 if f.max()>1.5 else f
    return f[::4,::4].mean(2)
def calls(fn,t):
    LOG.clear();cv=mod.PAP.copy() if hasattr(mod,'PAP') else None
    import khung_dung as K;cv=K.PAP.copy();fn(cv,t);return list(LOG)
def body(fn):
    m=re.search(r'def '+fn.__name__+r'\(.*?(?=\n(?:def |S=|MOV|_J|if FREEZE)|\Z)',src,re.S);return m.group(0) if m else ''
bad=0;mids=[];thieu=0;muon=set()
for a,b,fn in SH:
    d=b-a;ts=[a+.2*d,a+.5*d,a+.8*d];ims=[g(min(t,b-.15)) for t in ts]
    mv=max((np.abs(ims[0]-ims[1])>.04).mean(),(np.abs(ims[1]-ims[2])>.04).mean())
    mids.append(ims[1]);ok=mv>.003;bad+=not ok
    # vật động (máy quay đứng yên)
    best=0
    for tm in (a+.35*d,a+.6*d):
        c1=calls(fn,tm);c2=calls(fn,tm+.6)
        n=sum(1 for p,q in zip(c1,c2) if p[0]==q[0] and (abs(p[2]-q[2])>2 or abs(p[3]-q[3])>2 or abs(p[4]-q[4])>.01 or abs(p[5]-q[5])>.5))
        best=max(best,n)
    # lớp (máy quay thật)
    os.environ.pop('KIEM_TINH',None);mod.FREEZE=False
    ks=set(k for _,k,*_ in calls(fn,a+.5*d)); is_map='mapbg' in body(fn) or 'mcam' in body(fn)
    os.environ['KIEM_TINH']='1';mod.FREEZE=True
    names=set(n for n,*_ in calls(fn,a+.5*d))
    mu=[n for n in names if re.match(r't\d+_spr_',n) and not n.startswith(PRE) and not any(w in n for w in TRANG_TRI)]
    muon|=set(mu)
    loi=[]
    if not ok: loi.append('TĨNH')
    if best<3: loi.append(f'vật động {best}<3')
    if not is_map and len(ks)<3: loi.append(f'lớp {len(ks)}<3')
    if mu: loi.append('mượn '+','.join(sorted(mu)))
    thieu+=bool(loi)
    print(f'{fn.__name__:8s} {a:6.1f}-{b:6.1f}  đổi {mv*100:5.2f}%  lớp {len(ks)}{" (bản đồ)" if is_map else ""}  vật động {best:2d}  {"❌ "+"; ".join(loi) if loi else "OK"}')
sim=0
for i in range(len(mids)):
    for j in range(i+1,len(mids)):
        c=np.corrcoef(mids[i].ravel(),mids[j].ravel())[0,1]
        if c>.97: print('❌ trùng',SH[i][2].__name__,SH[j][2].__name__,round(c,3));sim+=1
uses=Counter()
for fn in [s[2] for s in SH]:
    for p in set(re.findall(r"'(t\d+x?_(?!spr|far|mid|front|in[LRb])[a-z0-9_]+)'",body(fn))): uses[p]+=1
dup=[k for k,v in uses.items() if v>1]
for k in dup: print('❌ tranh dùng nhiều cảnh:',k)
print(f'{len(SH)} cảnh, {len(uses)} tranh riêng; tĩnh {bad}; trùng {sim}; tranh lặp {len(dup)}; cảnh dưới chuẩn chi tiết {thieu}; hình mượn {sorted(muon)}')
