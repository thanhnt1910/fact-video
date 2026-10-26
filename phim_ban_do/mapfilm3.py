import json,math,sys,random,os
import numpy as np
from PIL import Image,ImageDraw
import build2 as B
from build2 import T,D,TOTAL,texts,chap,W,H,FPS,ease,clamp,font,comp
from mapdraw import *
import mapdraw as MD
import importlib as _il
_wm=_il.import_module(os.environ.get('WORLDMOD','world3'));RW,RH,wp=_wm.RW,_wm.RH,_wm.wp
WORLD=Image.open(os.environ.get('WORLD','/tmp/proto/world3.jpg')).convert('RGB')
PYR=[WORLD]
for i in range(1,4): PYR.append(PYR[-1].resize((RW>>i,RH>>i),Image.LANCZOS))
def lerp(a,b,u): return a+(b-a)*u
def kf(t,lon,lat,z): x,y=wp(lon,lat);return (t,x,y,z)
import importlib
C=importlib.import_module(os.environ.get('CONTENT','qd_content'))
import mapdraw3 as M3
CAMK=[kf(*k) for k in C.CAM]
def cam(t):
    if t<=CAMK[0][0]: return CAMK[0][1:]
    for i in range(len(CAMK)-1):
        a,b=CAMK[i],CAMK[i+1]
        if t<=b[0]:
            u=ease((t-a[0])/max(1e-6,b[0]-a[0]))
            z=math.exp(math.log(a[3])+(math.log(b[3])-math.log(a[3]))*u)
            return a[1]+(b[1]-a[1])*u,a[2]+(b[2]-a[2])*u,z
    return CAMK[-1][1:]
ZMIN=max(W/RW*1.0,0)  # z=1 = nguyên bề ngang bản đồ
class View:
    def __init__(s,t):
        s.cx,s.cy,s.z=cam(t);s.z=max(s.z*(1.3 if B.P else 1.0),(RW*H/W)/RH*1.01)
        s.bw=RW/s.z;s.bh=s.bw*H/W
        s.x0=min(max(s.cx-s.bw/2,0),RW-s.bw);s.y0=min(max(s.cy-s.bh*0.40,0),RH-s.bh)
    def sc(s,lon,lat,k=1):
        x,y=wp(lon,lat);return ((x-s.x0)/s.bw*W*k,(y-s.y0)/s.bh*H*k)
def base_frame(v):
    lvl=0;mpp=W/v.bw
    while lvl<3 and mpp*(2**(lvl+1))<=1.0: lvl+=1
    im=PYR[lvl];f=2**lvl
    return im.resize((W,H),Image.BICUBIC,box=(max(0,v.x0/f),max(0,v.y0/f),min(im.width,(v.x0+v.bw)/f),min(im.height,(v.y0+v.bh)/f)))
def _vel(keys,i,ax):
    # vận tốc tại khóa i (đơn vị/giây); 0 nếu đầu/cuối đường hoặc kề đoạn đứng yên => không giật khi qua khóa
    if i<=0 or i>=len(keys)-1: return 0.0
    a,b,c=keys[i-1],keys[i],keys[i+1]
    if (a[1],a[2])==(b[1],b[2]) or (b[1],b[2])==(c[1],c[2]): return 0.0
    dt=c[0]-a[0]
    if dt<=1e-6: return 0.0
    return (c[ax]-a[ax])/dt
def path_pos(keys,t):
    if t<=keys[0][0]: return keys[0][1],keys[0][2],0.0
    for i in range(len(keys)-1):
        a,b=keys[i],keys[i+1]
        if t<=b[0]:
            moving=(a[1],a[2])!=(b[1],b[2])
            if b[0]<=a[0] or not moving: return b[1],b[2],0.0
            h=b[0]-a[0];u=(t-a[0])/h;u2=u*u;u3=u2*u
            h00=2*u3-3*u2+1;h10=u3-2*u2+u;h01=-2*u3+3*u2;h11=u3-u2
            out=[]
            for ax in (1,2):
                m0=_vel(keys,i,ax);m1=_vel(keys,i+1,ax)
                out.append(h00*a[ax]+h10*h*m0+h01*b[ax]+h11*h*m1)
            return out[0],out[1],(1.0 if 0<u<1 else 0.0)
    return keys[-1][1],keys[-1][2],0.0
def curve(pts,t,default=0.0):
    if not pts: return default
    if t<=pts[0][0]: return pts[0][1]
    for i in range(len(pts)-1):
        if t<=pts[i+1][0]: return lerp(pts[i][1],pts[i+1][1],ease((t-pts[i][0])/max(1e-6,pts[i+1][0]-pts[i][0])))
    return pts[-1][1]
def colcurve(pts,t):
    if t<=pts[0][0]: return pts[0][1]
    for i in range(len(pts)-1):
        if t<=pts[i+1][0]:
            u=ease((t-pts[i][0])/max(1e-6,pts[i+1][0]-pts[i][0]));return tuple(int(lerp(pts[i][1][k],pts[i+1][1][k],u)) for k in range(3))
    return pts[-1][1]
class Group:
    def __init__(s,name,col,n,keys,kind='inf',alive=None,show=(0,1e9),seed=1,spread=1.0,soff=(0,0),defeats=None,emb='circle',label=True,n2=0):
        s.name,s.col,s.n,s.keys,s.kind=name,col,n,keys,kind
        s.alive=alive or [(0,1.0)];s.show=show;s.soff=soff;s.defeats=defeats or [];s.emb=emb;s.spread=spread;s.label=label
        r=random.Random(seed);s.off=[(r.uniform(-1,1),r.uniform(-1,1)) for _ in range(n)];s.phase=[r.uniform(0,6.28) for _ in range(n)]
    def vis(s,t):
        w=s.show if isinstance(s.show,list) else [s.show]
        return any(a<=t<=b for a,b in w)
    def dead_at(s,t):
        for (t0,k,t1) in s.defeats:
            if t0<=t<t1: return (t0,k)
        return None
        r=random.Random(seed);s.off=[(r.uniform(-1,1),r.uniform(-1,1)) for _ in range(n)];s.phase=[r.uniform(0,6.28) for _ in range(n)]
    def frac(s,t): return curve(s.alive,t,1.0)
GROUPS=[Group(**{k:v for k,v in g.items() if k!='n2'}) for g in C.GROUPS]

# ---- máy quay bám theo: đi theo quân đang di chuyển, thư, và zoom vào nơi lời kể đang nhắc (bật bằng CAMFOLLOW=True trong nội dung)
_cam_base=cam
_TRK=None
def _ten_nho(tok): return tok.strip('.,;:!?…—"“”()')
def _mention_events():
    ev=[];LOC=getattr(C,'LOC',{});skip={'Kế','Đàm','Ngô','Hứa Du'}
    names=sorted([k for k in LOC if k not in skip],key=lambda k:-len(k.split()))
    for n,txt in texts.items():
        words=txt.split();toks=[_ten_nho(w) for w in words]
        rows=B.PH.get(str(n),[]);wt=[None]*len(words);k=0
        for r in rows:
            m=len(r[0].split());tm=r[5] if len(r)>=6 and r[5] else None
            for j in range(m):
                if k+j<len(words):
                    if tm: wt[k+j]=tm[j]
                    elif len(r)>=5: wt[k+j]=r[3]+(r[4]-r[3])*j/max(1,m)
                    else: wt[k+j]=r[1]+(r[2]-r[1])*j/max(1,m)
            k+=m
        i=0
        while i<len(toks):
            hit=None
            for nm in names:
                parts=nm.split()
                if toks[i:i+len(parts)]==parts: hit=(nm,len(parts));break
            if hit:
                tm=wt[i] if wt[i] is not None else 0.5*D[n]
                t0=T[n]+0.12+tm;ev.append((t0-0.4,t0+3.0,LOC[hit[0]][0],LOC[hit[0]][1],hit[0]));i+=hit[1]
            else: i+=1
    return ev
def _build_track():
    dt=0.2;N=int(TOTAL/dt)+2;ev=_mention_events()
    X=np.zeros(N);Y=np.zeros(N);Z=np.zeros(N)
    for i in range(N):
        t=i*dt;bx,by,bz=_cam_base(t);tgt=None
        for (t0,t1,bl,bt,who) in C.BATT:
            if t0-1<=t<=t1+1: x,y=wp(bl,bt);tgt=(x,y,max(bz,3.0));break
        if tgt is None:
            for (e0,e1,lo,la,nm) in ev:
                if e0<=t<=e1: x,y=wp(lo,la);tgt=(x,y,max(bz,2.6));break
        if tgt is None:
            pts=[]
            for g in GROUPS:
                if not g.vis(t): continue
                lon,lat,mv=path_pos(g.keys,t)
                if mv: pts.append(wp(lon,lat))
            for (t0,t1,a,b,nm) in C.LETTERS:
                if t0<=t<=t1:
                    u=ease((t-t0)/(t1-t0));pts.append(wp(lerp(a[0],b[0],u),lerp(a[1],b[1],u)))
            if pts:
                xs=[q[0] for q in pts];ys=[q[1] for q in pts];ex=max(xs)-min(xs);ey=max(ys)-min(ys)
                zf=min(RW*0.5/max(ex,1),RW*H/W*0.45/max(ey,1),3.2);z=min(3.2,max(2.2,zf,min(bz,3.4)))
                tgt=((max(xs)+min(xs))/2,(max(ys)+min(ys))/2,z)
        if tgt is None:
            for (t0,t1,lon,lat,txt,col) in C.NOTES:
                if t0<=t<=t1: x,y=wp(lon,lat);tgt=(x,y,max(bz,2.4));break
        if tgt is None:
            for m_ in C.MARKS:
                if m_[0]<=t<=m_[1]: x,y=wp(m_[2],m_[3]);tgt=(x,y,max(bz,2.4));break
        if tgt is None: tgt=(bx,by,bz)
        X[i],Y[i],Z[i]=tgt[0],tgt[1],math.log(tgt[2])
    sg=max(1,int(1.0/dt));k=np.exp(-0.5*(np.arange(-4*sg,4*sg+1)/sg)**2);k/=k.sum()
    def sm(a):
        pad=np.concatenate([np.full(4*sg,a[0]),a,np.full(4*sg,a[-1])]);return np.convolve(pad,k,'same')[4*sg:-4*sg]
    return dt,sm(X),sm(Y),np.exp(sm(Z))
# ---- máy quay theo tiêu điểm (CAMFOCUS): mỗi câu zoom vào đúng vật đang được kể, đặt giữa vùng an toàn của khung
SAFE=(100,170,1550,840)
BASE_N=getattr(C,'BASE',0)
def _beat_subjects(n):
    t0=T[n];t1=t0+D[n];prim=[];sec=[]
    for (f0,f1,fp,rep) in getattr(C,'FOC',[]):
        if f0<=n-BASE_N<=f1 and rep: return list(fp),[]
        if f0<=n-BASE_N<=f1: prim+=list(fp)
    def act(a,b): return a<t1 and b>t0
    for pr in getattr(C,'PROPS',[]):
        if act(pr[0],pr[1]): prim.append((pr[3],pr[4]))
    for x in C.NOTES:
        if act(x[0],x[1]): prim.append((x[2],x[3]))
    for x in C.ARROWS:
        if act(x[0],x[1]): prim+= [x[2],x[3]]
    for x in C.LETTERS:
        if act(x[0],x[1]): prim+= [x[2],x[3]]
    for x in C.FIRES:
        if act(x[0],x[1]): prim.append((x[2],x[3]))
    for x in C.BATT:
        if act(x[0],x[1]): prim.append((x[2],x[3]))
    for x in getattr(C,'OBJ',[]):
        if act(x[0],x[1]): prim+= [x[3],x[4][:2]]
    for x in getattr(C,'FX',[]):
        if act(x[0],x[1]): prim+= [x[3],x[4]]
    for (e0,e1,lo,la,nm) in _MEN:
        if act(e0,e1): prim.append((lo,la))
    for g in GROUPS:
        for k in range(6):
            t=t0+(t1-t0)*(k+0.5)/6
            if g.vis(t) and g.frac(t)>0.02:
                lon,lat,mv=path_pos(g.keys,t);sec.append((lon,lat))
    return prim,sec
def _focus_target(n,bz):
    prim,sec=_beat_subjects(n)
    if prim:
        pts=list(prim)
        cx0=sum(p[0] for p in pts)/len(pts);cy0=sum(p[1] for p in pts)/len(pts)
        r0=max(0.6,max(math.hypot(p[0]-cx0,p[1]-cy0) for p in pts))
        pts+= [q for q in sec if math.hypot(q[0]-cx0,q[1]-cy0)<=r0*1.2+0.5]
    elif sec: pts=list(sec)
    else: return None
    pad=0.28
    lo0=min(p[0] for p in pts)-pad;lo1=max(p[0] for p in pts)+pad;la0=min(p[1] for p in pts)-pad;la1=max(p[1] for p in pts)+pad
    (xa,ya),(xb,yb)=wp(lo0,la1),wp(lo1,la0)
    bwx=max(xb-xa,1);bhy=max(yb-ya,1)
    sw=SAFE[2]-SAFE[0];sh=SAFE[3]-SAFE[1]
    zw=RW*sw/(W*bwx);zh=(RW*H/W)*sh/(H*bhy)*1.0  # bh=bw*H/W, bhy*H/(bh*... ) -> z cho chiều cao
    zh=RW*(sh/H)*(H/W)*0+RW*sh/(W*bhy)
    z=min(zw,zh);z=max(0.9,min(4.2,z))
    if z>3.4: z=3.4
    bcx,bcy=(xa+xb)/2,(ya+yb)/2
    bw=RW/z;bh=bw*H/W
    cx=bcx+bw*(0.5-((SAFE[0]+SAFE[2])/2)/W)
    cy=bcy+bh*(0.40-((SAFE[1]+SAFE[3])/2)/H)
    return cx,cy,z
_MEN=_mention_events() if getattr(C,'CAMFOCUS',False) else []
_FTRK=None
def _build_focus():
    dt=0.2;N=int(TOTAL/dt)+2;X=np.zeros(N);Y=np.zeros(N);Z=np.zeros(N)
    order=sorted(T.keys());last=None
    beatof=lambda t: B.beat_of(t)
    cur=None;cur_n=None
    for i in range(N):
        t=i*dt+0.5;n=beatof(min(t,TOTAL-0.01))
        if n!=cur_n:
            cur_n=n;bx,by,bz=_cam_base(T[n]+0.1);tg=_focus_target(n,bz)
            if tg is None: tg=(bx,by,bz)
            if cur is not None:
                bwc=RW/cur[2]
                if abs(tg[0]-cur[0])<0.12*bwc and abs(tg[1]-cur[1])<0.12*bwc and abs(math.log(tg[2]/cur[2]))<0.18: tg=cur
            cur=tg
        X[i],Y[i],Z[i]=cur[0],cur[1],math.log(cur[2])
    sg=max(1,int(1.6/dt));k=np.exp(-0.5*(np.arange(-4*sg,4*sg+1)/sg)**2);k/=k.sum()
    def sm(a):
        pad=np.concatenate([np.full(4*sg,a[0]),a,np.full(4*sg,a[-1])]);return np.convolve(pad,k,'same')[4*sg:-4*sg]
    return dt,sm(X),sm(Y),np.exp(sm(Z))
def cam(t):
    global _TRK,_FTRK
    if getattr(C,'CAMFOCUS',False):
        if _FTRK is None: _FTRK=_build_focus()
        dt,X,Y,Z=_FTRK;f=min(max(t/dt,0),len(X)-1.001);i=int(f);u=f-i
        return X[i]+(X[i+1]-X[i])*u,Y[i]+(Y[i+1]-Y[i])*u,Z[i]+(Z[i+1]-Z[i])*u
    if not getattr(C,'CAMFOLLOW',False): return _cam_base(t)
    if _TRK is None: _TRK=_build_track()
    dt,X,Y,Z=_TRK;f=min(max(t/dt,0),len(X)-1.001);i=int(f);u=f-i
    return X[i]+(X[i+1]-X[i])*u,Y[i]+(Y[i+1]-Y[i])*u,Z[i]+(Z[i+1]-Z[i])*u
# nền trang trí
_r=random.Random(77);DECO=[];_p=PYR[3]
for _ in range(9000):
    _w3=os.environ.get('WORLDMOD','world3')=='world3';lo=_r.uniform(107.2 if _w3 else _wm.LON0+0.2,121.6 if _w3 else _wm.LON1-0.2);la=_r.uniform(28.8 if _w3 else _wm.LAT0+0.2,41.4 if _w3 else _wm.LAT1-0.2);x,y=wp(lo,la)
    px=_p.getpixel((min(_p.width-1,int(x/8)),min(_p.height-1,int(y/8))))
    water=px[2]>px[0]+10
    DECO.append((lo,la,'wave' if water else ('tree' if _r.random()<0.5 else 'none'),_r.random()))
PAPER=paper() if False else None
def vign():
    yy,xx=np.mgrid[0:H,0:W];vv=np.sqrt(((xx-W/2)/(W/2))**2+((yy-H/2)/(H/2))**2)
    return Image.fromarray(np.stack([np.zeros((H,W),np.uint8)]*3+[(np.clip(vv-0.35,0,1)*120).astype(np.uint8)],-1),'RGBA')
VIGN=vign()
MD.W,MD.H=W,H
PAPER=MD.paper()
STATIC=Image.alpha_composite(VIGN,PAPER)
_h=Image.new('RGBA',(W,H),(0,0,0,0));_hd=ImageDraw.Draw(_h);MD.compass(_hd,W-110,245,46);MD.scalebar(_hd,W-290,320,170)
def _logo(px,a):
    lg=Image.open(os.environ.get('LOGO','/home/claude/fact-video/assets/logo/nguoi-gac-su.png')).convert('RGBA').resize((px,px),Image.LANCZOS)
    al=lg.split()[3].point(lambda v:int(v*a));lg.putalpha(al);return lg
_h.alpha_composite(_logo(130,0.8),(W-44-130,34))
STATIC=Image.alpha_composite(STATIC,_h)
CARDL={}
for c in getattr(C,'CARDS3',[]): CARDL[(c[2],c[3])]=M3.card3(c[2],c[3],c[4])
def _quiet(t):
    for (a,b) in list(getattr(C,'QUIET',[]))+[(x[0]-0.5,x[1]+0.5) for x in C.BATT]:
        if a<=t<=b: return True
    return False
TITL={i:M3.title_layer(*x[2:]) for i,x in enumerate(getattr(C,'TITLES',[]))}
QUOL={i:M3.quote_layer(x[2],x[3],x[4]) for i,x in enumerate(getattr(C,'QUOTES',[]))}
MINI0=M3.minimap_base(PYR[3],300,int(300*RH/RW))
NUML={i:B.num_layer(x[1],x[2]) for i,x in enumerate(C.NUMS)}
NUMT={}
CHIPS={}
def chip_for(n):
    ch=chap[n];yr=C.year_of(n);k=(ch,yr)
    if k not in CHIPS: CHIPS[k]=B.chip_layer(ch,yr)
    return CHIPS[k]
def dashed(d,pts,col,w,K,dash=22,alpha=150):
    for i in range(len(pts)-1):
        p,q=pts[i],pts[i+1];L=math.dist(p,q)
        if L<8: continue
        n=max(1,int(L/(dash*K)))
        for j in range(0,n,2):
            u0=j/n;u1=min(1,(j+1)/n);d.line([(lerp(p[0],q[0],u0),lerp(p[1],q[1],u0)),(lerp(p[0],q[0],u1),lerp(p[1],q[1],u1))],fill=col+(alpha,),width=int(w*K*0.55))
def _boat_unit(d,x,y,s,col,face,bob,alpha=255):
    M3.boat(d,x,y+math.sin(bob*0.35)*s*0.18,s*0.95,col,face)
def UNIT(kind): return soldier if kind=='inf' else (_boat_unit if kind=='ship' else (elephant if kind=='ele' else horse))
def stake(d,x,y,h,a):
    d.line([(x,y),(x,y-h)],fill=(92,62,34,a),width=max(2,int(h*0.2)))
    d.polygon([(x-h*0.22,y-h*0.78),(x,y-h*1.12),(x+h*0.22,y-h*0.78)],fill=(150,152,158,a),outline=(40,36,32,a))
_VIG={}
def _grade(im,gr):
    a=np.asarray(im.convert('RGB'),dtype=np.float32)
    g=a.mean(axis=2,keepdims=True);sat=gr.get('sat',1.0)
    a=g+(a-g)*sat
    tint=np.array(gr.get('tint',(255,255,255)),dtype=np.float32)/255.0;amt=gr.get('amt',0.0)
    a=a*(1-amt)+a*tint*amt*1.0+0
    a=a*gr.get('gain',1.0)
    h,w=a.shape[:2]
    if (h,w) not in _VIG:
        yy,xx=np.mgrid[0:h,0:w].astype(np.float32);r=np.sqrt(((xx-w/2)/(w/2))**2+((yy-h/2)/(h/2))**2)/1.414
        _VIG[(h,w)]=r[...,None]**2
    a=a*(1-gr.get('vig',0.0)*_VIG[(h,w)])
    return Image.fromarray(np.clip(a,0,255).astype(np.uint8)).convert('RGBA')
def frame(t):
    v=View(t);im=base_frame(v).convert('RGBA')
    _gr=getattr(C,'GRADE',None)
    if _gr: im=_grade(im,_gr)
    K=2;ov=Image.new('RGBA',(W*K,H*K),(0,0,0,0));d=ImageDraw.Draw(ov)
    z=v.z;ik=min(2.0,max(0.85,z**0.38))*13.0*K
    MD.deco(d,v,K,z,ik,DECO)
    # vùng (châu)
    for rg in C.REGIONS:
        if rg.get('win') and not(rg['win'][0]<=t<=rg['win'][1]): continue
        fc=colcurve(rg['own'],t);pts=[v.sc(*p,K) for p in rg['poly']]
        d.polygon(pts,fill=fc+(rg.get('alpha',30),))
        dashed(d,pts+[pts[0]],fc,5,K,26,200)
        cx_,cy_=v.sc(*rg['lab'],K);d.text((cx_,cy_),rg['name'],font=MD.F(34*K*min(1.6,z**0.3)*0.9),fill=fc+(150,),anchor='mm')
    for nm,(lo,la),sz in C.WATER:
        x,y=v.sc(lo,la,K);d.text((x,y),nm,font=MD.F(sz*K*min(1.7,z**0.3)),fill=(70,100,120,150),anchor='mm')
    for _rv in getattr(C,'RIVERS',[]):
        nm,pts,wd,lab=_rv[:4]
        if len(_rv)>4 and not(_rv[4][0]<=t<=_rv[4][1]): continue
        P=[v.sc(*p,K) for p in pts]
        M3.draw_river(d,P,wd*K*min(2.2,z**0.45)*0.9,t,K)
        if lab:
            lx,ly=v.sc(*lab,K);d.text((lx,ly),nm,font=MD.F(30*K*min(1.7,z**0.3)),fill=(40,78,110,200),anchor='mm',stroke_width=3,stroke_fill=(230,240,246,200))
    # thủy triều và cọc: TIDE=[(đường sông, mực nước [(t,0..1)], cọc [(lon,lat)], nhãn)]
    for _td in getattr(C,'TIDE',[]):
        poly,lvl,stakes_,tlab=_td[:4];t_show=_td[4] if len(_td)>4 else 0
        _w=_td[5] if len(_td)>5 else None
        if _w and not(_w[0]<=t<=_w[1]): continue
        Lv=curve(lvl,t,1.0);P=[v.sc(*p,K) for p in poly];S_=M3.smooth(P,8);bw_=ik*(1.1+2.4*Lv)
        mud=clamp((0.5-Lv)/0.5)
        d.line(S_,fill=(150,128,92,int(150*mud)),width=int(ik*3.6),joint='curve')
        d.line(S_,fill=(76,134,184,int(70+130*Lv)),width=int(bw_),joint='curve')
        for (lo,la) in stakes_:
            x,y=v.sc(lo,la,K)
            if -200<x<W*K+200 and -200<y<H*K+200:
                stake(d,x,y,ik*(0.9+0.5*mud),int(255*max(0.22,clamp((0.62-Lv)/0.25))*clamp((t-t_show)/1.2)))
        if tlab and tlab[0]<=t<=tlab[1]:
            mx,my=P[max(1,len(P)//4)]
            ff=font(int(24*K*min(1.3,z**0.2)));txt='TRIỀU LÊN' if Lv>0.5 else 'TRIỀU RÚT'
            bb=d.textbbox((0,0),txt,font=ff);tw=bb[2]-bb[0]
            d.rounded_rectangle((mx-tw/2-16,my-ik*5.4,mx+tw/2+16,my-ik*5.4+(bb[3]-bb[1])+18),10,fill=(30,70,110,225) if Lv>0.5 else (120,84,40,225))
            d.text((mx-tw/2,my-ik*5.4+6),txt,font=ff,fill=(250,244,226,255))
    # thành
    for nm,(lo,la,kind) in C.CITIES.items():
        cw=getattr(C,'CITY_SHOW',{}).get(nm)
        if hasattr(C,'CITY_SHOW') and (cw is None or not any(a<=t<=b for a,b in cw)): continue
        x,y=v.sc(lo,la,K)
        if not(-200<x<W*K+200 and -200<y<H*K+200): continue
        oc=colcurve(C.CITY_OWN[nm],t) if nm in C.CITY_OWN else None
        if kind=='big':
            city_icon(d,x,y,ik*1.5,open_=C.gate_open(t) if nm=='Hạ Bì' else 0)
            if oc:
                d.line([(x,y-ik*1.9),(x,y-ik*3.6)],fill=(70,50,30,255),width=max(2,int(ik*0.12)))
                d.polygon([(x,y-ik*3.6),(x+ik*1.3,y-ik*3.2),(x,y-ik*2.7)],fill=oc+(255,),outline=(25,18,12,255))
        elif kind=='mid':
            city_icon(d,x,y,ik*1.1)
            if oc:
                d.line([(x,y-ik*1.5),(x,y-ik*2.9)],fill=(70,50,30,255),width=max(2,int(ik*0.1)))
                d.polygon([(x,y-ik*2.9),(x+ik*1.0,y-ik*2.6),(x,y-ik*2.2)],fill=oc+(255,),outline=(25,18,12,255))
        else:
            d.ellipse((x-ik*0.5,y-ik*0.5,x+ik*0.5,y+ik*0.5),fill=(oc or (60,44,30))+(255,),outline=(246,238,214,255),width=3)
        f=MD.F(max(24,26*K*min(1.4,z**0.28)))
        d.text((x,y+ik*(1.9 if kind!='town' else 1.2)),nm,font=f,fill=(40,28,18,255),anchor='mt',stroke_width=int(3*K*0.6),stroke_fill=(246,236,208,255))
    # đường đi lịch sử
    for (t0,t1,pts,col,lab) in C.ROUTES:
        if t<t0: continue
        u=1.0 if t>=t1 else ease((t-t0)/(t1-t0))
        P=[v.sc(*p,K) for p in pts];tot=sum(math.dist(P[i],P[i+1]) for i in range(len(P)-1));acc=0;Q=[P[0]]
        for i in range(len(P)-1):
            L=math.dist(P[i],P[i+1])
            if acc+L<=u*tot: Q.append(P[i+1]);acc+=L
            else:
                r=(u*tot-acc)/max(L,1e-6);Q.append((lerp(P[i][0],P[i+1][0],r),lerp(P[i][1],P[i+1][1],r)));break
        dashed(d,Q,col,9,K,20,210)
    # vết di chuyển nhóm
    for g in GROUPS:
        if not g.vis(t): continue
        col=g.col;ks=g.keys;pts=[]
        for i in range(len(ks)):
            if ks[i][0]<=t and (i==0 or (ks[i][1],ks[i][2])!=(ks[i-1][1],ks[i-1][2])): pts.append(v.sc(ks[i][1],ks[i][2],K))
        cur=path_pos(ks,t);pts.append(v.sc(cur[0],cur[1],K));dashed(d,pts,col,6,K,22,150)
    # quân
    for g in GROUPS:
        if not g.vis(t): continue
        lon,lat,mv=path_pos(g.keys,t);x,y=v.sc(lon,lat,K);x+=g.soff[0]*K;y+=g.soff[1]*K
        if not(-300<x<W*K+300 and -300<y<H*K+300): continue
        col=g.col;fr=g.frac(t);s=ik*(1.0 if g.kind=='inf' else 0.9)
        ks=g.keys;face=1
        for i in range(len(ks)-1):
            if ks[i][0]<=t<=ks[i+1][0] and ks[i+1][1]!=ks[i][1]: face=1 if ks[i+1][1]>=ks[i][1] else -1
        infight=None
        for (t0,t1,bl,bt,who) in C.BATT:
            if t0-1<=t<=t1+1 and g.name in who: infight=(t0<=t<=t1);bx,by=v.sc(bl,bt,K);face=1 if bx>=x else -1
        spr=ik*(2.2 if g.kind=='inf' else 3.0)*g.spread
        dd=g.dead_at(t);dead=dd is not None
        nfall=int(g.n*max(fr,0.5)) if dead else None
        for i in range(g.n):
            ox,oy=g.off[i];px=x+ox*spr*1.7;py=y+oy*spr*0.85
            alive=(i<nfall) if dead else (i/g.n)<fr
            if not alive: continue
            bob=t*(9 if mv else 0)+g.phase[i]
            if infight: bob=t*14+g.phase[i];px+=math.sin(t*10+g.phase[i])*s*0.5*face
            if dead:
                gc=tuple(int(0.35*c+0.65*110) for c in col);py+=s*0.35
                UNIT(g.kind)(d,px,py,s*0.95,gc,face,0.0,alpha=190)
            else: UNIT(g.kind)(d,px,py,s,col,face,bob)
        if g.kind=='ele' and mv and not dead:
            for k_ in range(7):
                ph_=(t*1.3+k_/7.0)%1.0;rr=s*(0.5+1.4*ph_);ax=x-face*spr*(0.9+1.6*ph_)+math.sin(k_*2.1)*s*0.8;ay=y+spr*0.6+math.cos(k_*1.7)*s*0.5
                d.ellipse((ax-rr,ay-rr*0.6,ax+rr,ay+rr*0.6),fill=(196,176,138,int(110*(1-ph_))))
        fcol=(120,120,126) if dead else col
        if dead: flag(d,x-spr*1.9,y-spr*0.1,s*0.7,fcol)
        else: flag(d,x-spr*1.9,y-spr*0.6,s*1.05,col)
        if g.label and not getattr(C,'NO_GROUP_LABEL',False): tag2(d,x,y+spr*1.1,g,col,int(24*K*min(1.3,z**0.25)),max(fr,0.0),dead,t)
        if dead:
            u=(t-dd[0])/0.8
            badge(d,x,y-spr*1.5-ik*1.2,ik*2.3,dd[1],u)
            tg='BỊ DIỆT' if dd[1]=='skull' else 'THUA TRẬN'
            ff=font(int(22*K*min(1.3,z**0.2)));bb=d.textbbox((0,0),tg,font=ff)
            d.rounded_rectangle((x-(bb[2]-bb[0])/2-14,y-spr*1.5+ik*1.3,x+(bb[2]-bb[0])/2+14,y-spr*1.5+ik*1.3+(bb[3]-bb[1])+16),10,fill=(110,30,26,235))
            d.text((x-(bb[2]-bb[0])/2,y-spr*1.5+ik*1.3+6),tg,font=ff,fill=(250,244,226,255))
    # dấu cá nhân (đầu lâu / thua)
    for (tm,tm1,lon,lat,kind,lab) in C.MARKS:
        if tm<=t<tm1:
            x,y=v.sc(lon,lat,K)
            if -200<x<W*K+200 and -200<y<H*K+200:
                badge(d,x,y-ik*1.6,ik*1.9,kind,(t-tm)/0.8)
                if lab: tag(d,x,y+ik*0.6,lab,(120,30,26),int(22*K*min(1.3,z**0.2)))
    # mặt nhân vật hiện trên bản đồ khi được nhắc tên
    for (t0,t1,lon,lat,nm_,kind_,col_,dx_,dy_) in getattr(C,'FACES',[]):
        if not(t0<=t<=t1): continue
        x,y=v.sc(lon,lat,K)
        if not(-300<x<W*K+300 and -300<y<H*K+300): continue
        u_=t-t0;k_=min(clamp(u_/0.45),clamp((t1-t)/0.4))
        pop=ease(clamp(u_/0.45))*(1+0.16*math.sin(clamp(u_/0.45)*math.pi))
        r_=max(ik*2.15,44*K)*pop*(0.5+0.5*min(1,k_*2));bob=math.sin(t*3.2+lon*9)*ik*0.14
        fx=x+dx_*K;fy=y-max(ik*4.6,r_+ik*1.6)+dy_*K-bob
        # vòng sóng lan ra tại điểm nhắc tên
        for j_ in range(2):
            ph_=((u_*0.9)+j_*0.5)%1.0
            d.ellipse((x-ik*(0.6+2.2*ph_),y-ik*(0.6+2.2*ph_)*0.62,x+ik*(0.6+2.2*ph_),y+ik*(0.6+2.2*ph_)*0.62),outline=col_+(int(190*(1-ph_)*k_),),width=max(2,int(3*K*0.7)))
        d.polygon([(fx-r_*0.30,fy+r_*0.80),(fx+r_*0.30,fy+r_*0.80),(x,y-ik*1.3)],fill=col_+(int(255*k_),),outline=(34,24,18,int(255*k_)))
        sp_=MD.face_sprite(kind_,col_,name=nm_)
        sz_=max(8,int(r_*2));sp2=sp_.resize((sz_,sz_),Image.LANCZOS)
        if k_<1:
            al_=sp2.getchannel('A').point(lambda a_:int(a_*k_));sp2.putalpha(al_)
        ov.paste(sp2,(int(fx-r_),int(fy-r_)),sp2)
        if kind_=='king' and u_<1.4:
            for q_ in range(10):
                an_=q_*0.628+0.3;rr_=r_*(1.05+0.9*(u_/1.4));d.line([(fx+math.cos(an_)*rr_*0.95,fy+math.sin(an_)*rr_*0.95),(fx+math.cos(an_)*rr_*1.25,fy+math.sin(an_)*rr_*1.25)],fill=(255,226,120,int(230*(1-u_/1.4))),width=max(3,int(4*K*0.6)))
        tag(d,fx,fy-r_-ik*1.35,nm_,col_,int(24*K*min(1.3,z**0.2)))
    # trận
    for (t0,t1,bl,bt,who) in C.BATT:
        if t0<=t<=t1:
            bx,by=v.sc(bl,bt,K);rr=ik*3.2
            for i in range(14):
                ph=((t*1.6+i*0.37)%1);side=1 if i%2 else -1
                sx_=bx-side*rr*1.3;ex_=bx+side*rr*1.3;ay=by-rr*0.4+(i%5-2)*ik*0.8
                px=lerp(sx_,ex_,ph);py=ay-math.sin(ph*math.pi)*rr*1.1
                nx=lerp(sx_,ex_,min(1,ph+0.04));ny=ay-math.sin(min(1,ph+0.04)*math.pi)*rr*1.1
                d.line([(px,py),(nx,ny)],fill=(50,36,24,230),width=int(3*K*0.6))
            for i in range(6):
                u=(t*3+i*0.31)%1;qx=bx+math.sin(i*2.1+t*5)*rr*0.5;qy=by+math.cos(i*1.7+t*4)*ik*1.2
                for kk in range(5):
                    ang=kk*1.26+i;d.line([(qx,qy),(qx+math.cos(ang)*ik*1.7*u,qy+math.sin(ang)*ik*1.7*u)],fill=(255,240,180,int(220*(1-u))),width=int(3*K*0.55))
    # hiệu ứng phụ: máy bắn đá, tên lửa, kèn
    for (t0,t1,kind,a,b) in getattr(C,'FX',[]):
        if not(t0<=t<=t1+2.5): continue
        ax,ay=v.sc(*a,K);bx,by=v.sc(*b,K);dist=math.hypot(bx-ax,by-ay)
        if kind=='catapult':
            fl=1.5;nsh=max(1,int((t1-t0)/2.2))
            if t<=t1: # máy: khung gỗ và cần ném giật
                kk=((t-t0)%2.2)/2.2;arm=-0.9+1.9*min(1,kk*3)
                d.line([(ax-ik*1.6,ay+ik*0.6),(ax+ik*1.6,ay+ik*0.6)],fill=(70,48,28,255),width=int(8*K*0.6))
                d.line([(ax,ay+ik*0.6),(ax+math.cos(arm-1.6)*ik*2.4,ay+ik*0.6+math.sin(arm-1.6)*ik*2.4)],fill=(100,70,38,255),width=int(7*K*0.6))
                d.ellipse((ax-ik*0.5,ay+ik*0.6-ik*0.5,ax+ik*0.5,ay+ik*0.6+ik*0.5),fill=(60,40,24,255))
            for j in range(nsh):
                u=(t-t0-j*2.2)/fl
                if 0<=u<=1:
                    px=lerp(ax,bx,u);py=lerp(ay,by,u)-math.sin(u*math.pi)*(dist*0.28+ik*3)
                    d.ellipse((px-ik*0.5,py-ik*0.5,px+ik*0.5,py+ik*0.5),fill=(90,84,78,255),outline=(40,36,32,255))
                w=t-t0-j*2.2-fl
                if 0<=w<=1.6:
                    r=ik*(0.6+2.4*ease(min(1,w/0.6)));al=int(235*(1-w/1.6))
                    d.ellipse((bx-r*1.6,by-r*0.7,bx+r*1.6,by+r*0.7),outline=(230,214,170,al),width=int(5*K*0.6))
                    for q in range(9):
                        ang=q*0.7+j;dd_=r*(0.5+w);d.ellipse((bx+math.cos(ang)*dd_*1.4-ik*0.3,by-abs(math.sin(ang))*dd_*1.1-ik*0.3,bx+math.cos(ang)*dd_*1.4+ik*0.3,by-abs(math.sin(ang))*dd_*1.1+ik*0.3),fill=(120,100,80,al))
        elif kind=='firearrows' and t<=t1:
            for i in range(10):
                u=((t-t0)*0.9+i*0.1)%1;off=(i-5)*ik*0.7
                px=lerp(ax,bx,u)+off;py=lerp(ay,by,u)-math.sin(u*math.pi)*(dist*0.22+ik*2)+off*0.3
                for tr in range(5):
                    uu=max(0,u-tr*0.02);qx=lerp(ax,bx,uu)+off;qy=lerp(ay,by,uu)-math.sin(uu*math.pi)*(dist*0.22+ik*2)+off*0.3
                    d.ellipse((qx-ik*0.22*(1-tr*0.15),qy-ik*0.22*(1-tr*0.15),qx+ik*0.22,qy+ik*0.22),fill=(255,150-tr*20,40,int(240-tr*40)))
        elif kind=='volley' and t<=t1:
            for i in range(12):
                u=((t-t0)*0.8+i*0.083)%1;off=(i-6)*ik*0.45
                px=lerp(ax,bx,u)+off;py=lerp(ay,by,u)-math.sin(u*math.pi)*(dist*0.2+ik*1.5)
                u2=max(0,u-0.05);qx=lerp(ax,bx,u2)+off;qy=lerp(ay,by,u2)-math.sin(u2*math.pi)*(dist*0.2+ik*1.5)
                d.line([(qx,qy),(px,py)],fill=(40,28,18,235),width=int(4*K*0.6))
        elif kind in ('horn','trumpet') and t<=t1:
            k=(t-t0)/(t1-t0)
            for r_ in range(3):
                rr=ik*(1.5+((k*2+r_*0.33)%1)*5);al=int(200*(1-((k*2+r_*0.33)%1)))
                d.ellipse((ax-rr,ay-rr,ax+rr,ay+rr),outline=(250,230,160,al),width=int(4*K*0.6))
    for (t0,t1,kind,a,b) in getattr(C,'OBJ',[]):
        if t<t0: continue
        if kind=='fireboat' and t>t1: continue
        if kind=='flood' and len(b)>2 and t>t1+b[2]: continue
        ax,ay=v.sc(*a,K);bx,by=v.sc(*b[:2],K)
        if kind=='tower':
            if t<=t1: M3.tower(d,ax,ay,ik*0.9,t)
            elif t<=t1+1.8: M3.debris(d,ax,ay,ik*0.9,(t-t1)/1.8)
        elif kind=='ditch':
            u=clamp((t-t0)/2.5);ex,ey=lerp(ax,bx,u),lerp(ay,by,u)
            d.line([(ax,ay),(ex,ey)],fill=(70,50,30,255),width=int(15*K*0.6));d.line([(ax,ay),(ex,ey)],fill=(150,112,66,255),width=int(8*K*0.6))
        elif kind=='tunnel':
            u=clamp((t-t0)/2.5);al=int(230*(1-clamp((t-t1)/1.0)))
            if al>0:
                ex,ey=lerp(ax,bx,u),lerp(ay,by,u)
                dashed(d,[(ax,ay),(ex,ey)],(110,70,36),9,K,16,al)
                for j in range(int(u*6)):
                    q=(j+1)/7;mx,my=lerp(ax,bx,q),lerp(ay,by,q)
                    d.polygon([(mx-ik*0.5,my),(mx,my-ik*0.5),(mx+ik*0.5,my)],fill=(120,84,48,al),outline=(50,36,24,al))
        elif kind=='fleet':
            u=clamp((t-t0)/1.0);n_=int(b[2]) if len(b)>2 else 6
            for j in range(n_):
                q=j/max(1,n_-1);M3.boat(d,lerp(ax,bx,q),lerp(ay,by,q)+math.sin(t*2+j)*ik*0.15,ik*0.9,(70,60,50),1)
            for j in range(n_-1):
                q0=j/max(1,n_-1);q1=(j+1)/max(1,n_-1);d.line([(lerp(ax,bx,q0),lerp(ay,by,q0)),(lerp(ax,bx,q1),lerp(ay,by,q1))],fill=(40,34,30,255),width=int(4*K*0.6))
        elif kind=='fireboat':
            u=clamp((t-t0)/(t1-t0))
            for j in range(5):
                px=lerp(ax,bx,u)+j*ik*0.7;py=lerp(ay,by,u)+(j-2)*ik*0.8
                M3.boat(d,px,py,ik*0.8,(120,80,40),-1);fire(d,px,py-ik*0.4,ik*0.8,t,j+int(ax))
        elif kind=='flood':
            u=clamp((t-t0)/3.0);rr=ik*(2+u*9)
            d.ellipse((ax-rr*1.6,ay-rr*0.9,ax+rr*1.6,ay+rr*0.9),fill=(90,140,190,int(120*u)),outline=(60,110,170,int(200*u)),width=int(4*K*0.6))
        elif kind=='loot':
            u=clamp((t-t0)/2.0)
            for j in range(int(u*7)):
                q=(j+0.5)/7;mx,my=lerp(ax,bx,q),lerp(ay,by,q)+((j%2)*2-1)*ik*0.7
                (M3.saddle if j%2 else M3.sack)(d,mx,my,ik*0.9,255 if t<t1 else int(255*(1-clamp((t-t1)/1.0))))
    # hình minh họa nổi (PROPS)
    for pr in getattr(C,'PROPS',[]):
        t0,t1,kind,lon,lat,arg=pr[:6];sc_=pr[6] if len(pr)>6 else 1.0
        if not(t0<=t<=t1): continue
        x,y=v.sc(lon,lat,K)
        if not(-300<x<W*K+300 and -300<y<H*K+300): continue
        import mapprops as MP
        fa=min(clamp((t-t0)/0.4),clamp((t1-t)/0.4));u_=(t-t0)/max(1e-6,t1-t0)
        if fa>=0.999: MP.draw(d,kind,x,y,ik*1.7*sc_,u_,t,arg)
        else:
            lay=Image.new('RGBA',(W*K,H*K),(0,0,0,0));MP.draw(ImageDraw.Draw(lay),kind,x,y,ik*1.7*sc_,u_,t,arg)
            lay.putalpha(lay.getchannel('A').point(lambda a_,f_=fa:int(a_*f_)));d.bitmap((0,0),Image.new('L',(1,1))) if False else ov.alpha_composite(lay)
    # lửa
    for (t0,t1,lon,lat) in C.FIRES:
        if t0<=t<=t1:
            x,y=v.sc(lon,lat,K);fire(d,x,y,ik*1.5*min(1,(t-t0)/1.0+0.2),t,int(lon*100))
    # mũi tên chiến lược
    for (t0,t1,a,b,col,lab) in C.ARROWS:
        if t0<=t<=t1:
            k=min(clamp((t-t0)/0.8),clamp((t1-t)/0.5));ax,ay=v.sc(*a,K);bx,by=v.sc(*b,K)
            ex,ey=lerp(ax,bx,k),lerp(ay,by,k);d.line([(ax,ay),(ex,ey)],fill=col+(235,),width=int(10*K*0.6))
            ang=math.atan2(ey-ay,ex-ax);L_=ik*2.2
            d.polygon([(ex+math.cos(ang)*L_*0.2,ey+math.sin(ang)*L_*0.2),(ex+math.cos(ang+2.5)*L_,ey+math.sin(ang+2.5)*L_),(ex+math.cos(ang-2.5)*L_,ey+math.sin(ang-2.5)*L_)],fill=col+(255,))
            if lab: tag(d,lerp(ax,bx,0.5),lerp(ay,by,0.5)-ik*3,lab,col,int(26*K*min(1.3,z**0.2)))
    # thư / sứ giả
    for (t0,t1,a,b,nm) in C.LETTERS:
        if t0<=t<=t1:
            u=ease((t-t0)/(t1-t0));ax,ay=v.sc(*a,K);bx,by=v.sc(*b,K)
            ctl=(lerp(ax,bx,0.5),min(ay,by)-abs(bx-ax)*0.28-ik*6)
            bez=lambda u:((1-u)**2*ax+2*(1-u)*u*ctl[0]+u*u*bx,(1-u)**2*ay+2*(1-u)*u*ctl[1]+u*u*by)
            for j in range(0,int(u*40),2):
                p=bez(j/40);q=bez(min(1,(j+1)/40));d.line([p,q],fill=(120,90,50,200),width=int(5*K*0.6))
            px,py=bez(u);scroll(d,px,py,ik*1.1)
            if nm: tag(d,px,py-ik*3.8,nm,(110,70,30),int(20*K*min(1.3,z**0.2)))
    # ghi chú nổi
    for (t0,t1,lon,lat,txt,col) in C.NOTES:
        if t0<=t<=t1 and not _quiet(t):
            k=min(clamp((t-t0)/0.4),clamp((t1-t)/0.4));x,y=v.sc(lon,lat,K)
            if -200<x<W*K+200 and -200<y<H*K+200: tag(d,x,y-ik*(3.6+0.8*(1-ease(k))),txt,col,int(26*K*min(1.3,z**0.2)))
    ov=ov.resize((W,H),Image.BILINEAR)
    out=Image.alpha_composite(im,ov)
    n_=curve(C.NIGHT,t,0.0)
    if n_>0.01:
        arr=np.asarray(out.convert('RGB'),np.float32)
        arr*=np.array([1-0.58*n_,1-0.5*n_,1-0.22*n_],np.float32)
        glow=None
        for (t0,t1,lon,lat) in C.FIRES:
            if t0<=t<=t1:
                if glow is None:
                    glow=np.zeros((H,W),np.float32);yy,xx=np.mgrid[0:H,0:W]
                x,y=v.sc(lon,lat);r=80*min(2.2,z**0.5)
                glow+=np.exp(-(((xx-x)**2+(yy-y)**2)/(2*r*r)))*(0.8+0.2*math.sin(t*13+lon*50))*0.55
        if glow is not None: arr+=glow[...,None]*np.array([110,64,18],np.float32)*n_
        out=Image.fromarray(np.clip(arr,0,255).astype(np.uint8)).convert('RGBA')
    out=Image.alpha_composite(out,STATIC)
    n=B.beat_of(t)
    ttl=None
    for i,x in enumerate(getattr(C,'TITLES',[])):
        if x[0]<=t<=x[1]:
            k=min(clamp((t-x[0])/0.7),clamp((x[1]-t)/0.7));ttl=(i,k)
    if ttl: out=Image.blend(out,Image.new('RGBA',(W,H),(8,5,3,255)),0.55*ease(ttl[1]))
    out=comp(out,chip_for(n),(50,40),clamp((t-0.6)/0.6)*clamp((TOTAL-1.2-t)/0.5)*(0 if ttl else 1))
    act=[c for c in getattr(C,'CARDS3',[]) if c[0]<=t<=c[1]]
    for idx,c in enumerate(act):
        k=min(clamp((t-c[0])/0.5),clamp((c[1]-t)/0.4));out=comp(out,CARDL[(c[2],c[3])],(50-int((1-ease(k))*160),215+idx*136),ease(k))
    for ni,nx in enumerate(C.NUMS):
        cn,dl=nx[0],nx[3];du=nx[4] if len(nx)>4 else 2.6
        if n==cn or (len(nx)>4 and T[cn]+dl<=t<=T[cn]+dl+du):
            s_=T[cn]+dl;e=s_+du
            if s_<=t<=e and not _quiet(t):
                k=min(clamp((t-s_)/0.25),clamp((e-t)/0.4));out=comp(out,NUML[ni],(0,0),ease(k))
    # thanh sức mạnh
    for (t0,t1,title,rows) in getattr(C,'METERS',[]):
        if t0<=t<=t1:
            k=min(clamp((t-t0)/0.5),clamp((t1-t)/0.4))
            ml=M3.meter_layer(title,[(lab,col,curve(cv,t)) for lab,col,cv in rows])
            out=comp(out,ml,(30-int((1-ease(k))*160),(1000 if B.P else 500)),ease(k))
    # khung so sánh / sơ đồ
    for ti,(t0,t1,title,rows) in enumerate(getattr(C,'TABLES',[])):
        if t0<=t<=t1:
            if ('_tb',ti) not in CARDL: CARDL[('_tb',ti)]=M3.table_layer(title,rows)
            tl=CARDL[('_tb',ti)];k=min(clamp((t-t0)/0.4),clamp((t1-t)/0.4))
            out=comp(out,tl,((1920-tl.size[0])//2,max(60,(1080-tl.size[1])//2-30)),ease(k))
    # chú giải phe (thay nhãn tên trên từng nhóm): chỉ liệt kê phe đang có mặt trên màn hình
    sides=getattr(C,'SIDES',None)
    if sides and not ttl:
        vis_=[(nm,col) for nm,col,names in sides if any(gg.vis(t) and (gg.name.strip() in names) for gg in GROUPS)]
        if vis_:
            fl=font(int(26*(1 if not B.P else 1.2)));rh=48;pw=300;ph=rh*len(vis_)+24
            lay=Image.new('RGBA',(pw,ph),(0,0,0,0));ld=ImageDraw.Draw(lay)
            ld.rounded_rectangle((0,0,pw-1,ph-1),14,fill=(28,20,12,200),outline=(246,238,214,230),width=2)
            for i,(nm,col) in enumerate(vis_):
                cy=12+i*rh+rh//2
                ld.line([(26,cy-18),(26,cy+18)],fill=(70,50,30,255),width=4)
                ld.polygon([(26,cy-18),(60,cy-8),(26,cy+2)],fill=col+(255,),outline=(250,244,226,255))
                ld.text((76,cy),nm,font=fl,fill=(250,244,226,255),anchor='lm')
            out=comp(out,lay,(W-44-300,(530 if not B.P else 700)),clamp(t/0.8))
    # bản đồ nhỏ
    mm=getattr(C,'MINI',None)
    if mm is not None and any(a<=t<=b for a,b in mm) and not ttl and not B.P:
        m=MINI0.copy();g_=ImageDraw.Draw(m);mw,mh=m.size
        def mp(lon,lat):
            x_,y_=wp(lon,lat);return x_/RW*mw,y_/RH*mh
        x0_=v.x0/RW*mw;y0_=v.y0/RH*mh;x1_=(v.x0+v.bw)/RW*mw;y1_=(v.y0+v.bh)/RH*mh
        g_.rectangle((x0_,y0_,x1_,y1_),outline=(250,230,120,255),width=3)
        for gg in GROUPS:
            if gg.vis(t):
                lon,lat,_=path_pos(gg.keys,t);px_,py_=mp(lon,lat);g_.ellipse((px_-5,py_-5,px_+5,py_+5),fill=gg.col+(255,),outline=(255,255,255,255))
        out=comp(out,m,(W-44-300,370),clamp((t-0.8)/0.6))
    for i,x in enumerate(getattr(C,'QUOTES',[])):
        if x[0]<=t<=x[1]:
            k=min(clamp((t-x[0])/0.5),clamp((x[1]-t)/0.4));ql=QUOL[i];out=comp(out,ql,((W-ql.width)//2,int((1250 if B.P else 770)-ql.height+(1-ease(k))*40)),ease(k))
    if ttl: out=comp(out,TITL[ttl[0]],(0,0),ease(ttl[1]))
    for (t0,t1,icon,txt) in getattr(C,'JOKES',[]):
        if t0<=t<=t1 and not _quiet(t):
            k=min(clamp((t-t0)/0.45),clamp((t1-t)/0.4));out=comp(out,M3.joke_layer(icon,txt,t,k),(0,int((1-ease(k))*60)),ease(k))
    for ii,(t0,t1,kind,dat) in enumerate(getattr(C,'INTER',[])):
        if t0<=t<=t1 and kind=='pic':
            # cảnh ảnh 2D toàn khung, máy quay trượt/phóng chậm (dat: path, z0, z1, dx, dy)
            if ('_pic',ii) not in CARDL:
                _im=Image.open(dat['path']).convert('RGB');_s=max(W/_im.width,H/_im.height)*1.18
                CARDL[('_pic',ii)]=_im.resize((int(_im.width*_s),int(_im.height*_s)),Image.LANCZOS)
            _bg=CARDL[('_pic',ii)];u=clamp((t-t0)/max(t1-t0,0.01));z=dat.get('z0',1.0)+(dat.get('z1',1.08)-dat.get('z0',1.0))*u
            vw=int(_bg.width/1.18/z);vh=int(vw*H/W)
            cx=_bg.width/2+dat.get('dx',0)*(u-0.5)*_bg.width*0.06;cy=_bg.height/2+dat.get('dy',0)*(u-0.5)*_bg.height*0.06
            box=(int(cx-vw/2),int(cy-vh/2),int(cx+vw/2),int(cy+vh/2))
            _fr=_bg.crop(box).resize((W,H),Image.BILINEAR).convert('RGBA')
            k=min(clamp((t-t0)/0.3),clamp((t1-t)/0.3));out=comp(out,_fr,(0,0),ease(k))
            continue
        if t0<=t<=t1:
            if ('_in',ii) not in CARDL: CARDL[('_in',ii)]=M3.inter_layer(kind,dat)
            k=min(clamp((t-t0)/0.5),clamp((t1-t)/0.5));out=comp(out,CARDL[('_in',ii)],(0,0),ease(k))
    sl,sa=B.sub_at(t)
    if sl is not None: out=comp(out,sl,(0,0),ease(sa))
    if t<0.5: out=Image.blend(Image.new('RGBA',(W,H),(8,5,3,255)),out,ease(t/0.5))
    if t>TOTAL-1.0: out=Image.blend(out,Image.new('RGBA',(W,H),(8,5,3,255)),ease((t-(TOTAL-1.0))/1.0))
    return out.convert('RGB')
def work(i): return frame(i/FPS).tobytes()
if __name__=='__main__':
    import subprocess,multiprocessing as mp
    if len(sys.argv)>1 and sys.argv[1]=='still':
        for a in sys.argv[2:]:
            frame(float(a)).save(f'/tmp/proto/m3_{a}.jpg',quality=90);print('ok',a)
        sys.exit()
    N=int(TOTAL*FPS);out=sys.argv[1] if len(sys.argv)>1 else '/tmp/proto/mv3.mp4'
    a0,a1=(int(sys.argv[2]),int(sys.argv[3])) if len(sys.argv)>3 else (0,N)
    p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',out],stdin=subprocess.PIPE)
    with mp.Pool(int(os.environ.get('NPROC','2'))) as pool:
        for i,b in enumerate(pool.imap(work,range(a0,a1),chunksize=4)):
            p.stdin.write(b)
            if i%300==0: print(i,a1-a0,flush=True)
    p.stdin.close();p.wait();print('xong')
