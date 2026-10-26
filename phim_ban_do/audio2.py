import json,math,wave,numpy as np,sys
import build2 as b
import importlib,os
C=importlib.import_module(os.environ.get('CONTENT','tq45_content'))
QA=getattr(C,'QUIET_AUDIO',False)
SR=44100;T,D,TOTAL=b.T,b.D,b.TOTAL
N=int(TOTAL*SR);rng=np.random.default_rng(7)
out=np.zeros(N,np.float32)
def lp(x,fc):
    a=math.exp(-2*math.pi*fc/SR);y=np.zeros_like(x);p=0.0
    # bộ lọc một cực, vector hóa bằng scipy nếu có
    try:
        from scipy.signal import lfilter
        return lfilter([1-a],[1,-a],x).astype(np.float32)
    except Exception:
        for i,v in enumerate(x): p=a*p+(1-a)*v;y[i]=p
        return y
def hp(x,fc): return x-lp(x,fc)
def add(sig,t0,g=1.0):
    i=int(t0*SR);j=min(N,i+len(sig))
    if i<N and j>i: out[i:j]+=sig[:j-i]*g
def env(n,a=0.005,d=0.15):
    t=np.arange(n)/SR;return np.minimum(t/a,1)*np.exp(-t/d)
# gió nền: nhiễu nâu lọc thấp, nhấp nhô chậm
w=lp(rng.normal(0,1,N).astype(np.float32),500);w=lp(w,300)
mod=0.55+0.45*np.sin(2*math.pi*np.arange(N)/SR/9.0+1.3)
out+=w*mod*(0.0 if QA else 0.9)
# tiếng vó ngựa phi: nhịp 4 bước
def hoof(t0,dur,spd=0.17):
    t=t0
    while t<t0+dur:
        for k,o in enumerate([0,0.05,0.12,0.19]):
            n=int(0.09*SR);s=lp(rng.normal(0,1,n).astype(np.float32),900)*env(n,0.002,0.025)*(0.9 if k%2==0 else 0.6)
            s+=np.sin(2*math.pi*110*np.arange(n)/SR).astype(np.float32)*env(n,0.002,0.03)*0.7
            add(s,t+o,0.9)
        t+=0.19+spd*0.8
def clop(t0,dur,g=0.55):
    t=t0
    while t<t0+dur:
        for o_,ff in ((0,520),(0.16,410)):
            m=int(0.07*SR);tq=np.arange(m)/SR
            s=(np.sin(2*math.pi*ff*tq)+0.5*np.sin(2*math.pi*ff*2.3*tq))*np.exp(-tq/0.018)+lp(rng.normal(0,1,m).astype(np.float32),2500)*np.exp(-tq/0.01)*0.6
            add(s.astype(np.float32),t+o_,g)
        t+=0.42
def bells(t0,dur,g=0.16):
    tt=t0
    while tt<t0+dur:
        f=rng.choice([2900,3300,3800,4300]);m=int(0.22*SR);tq=np.arange(m)/SR
        add((np.sin(2*math.pi*f*tq)*np.exp(-tq/0.06)+0.4*np.sin(2*math.pi*f*2.01*tq)*np.exp(-tq/0.03)).astype(np.float32),tt,g)
        tt+=rng.uniform(0.16,0.34)
def steps(t0,dur,bpm=104):
    iv=60/bpm;t=t0;i=0
    while t<t0+dur:
        n=int(0.12*SR);s=lp(rng.normal(0,1,n).astype(np.float32),600)*env(n,0.003,0.035)*(1 if i%2==0 else 0.8)
        add(s,t+rng.normal(0,0.012),0.8);t+=iv;i+=1
def drum(t0,g=1.0):
    n=int(0.7*SR);t=np.arange(n)/SR;f=70*np.exp(-t*3);ph=2*math.pi*np.cumsum(f)/SR
    s=np.sin(ph).astype(np.float32)*np.exp(-t/0.25);add(s,t0,g*1.2)
def whoosh(t0,dur,g=0.6):
    n=int(dur*SR);x=rng.normal(0,1,n).astype(np.float32);x=hp(lp(x,3000),300)
    e=np.sin(np.linspace(0,math.pi,n))**2;add(x*e,t0,g)
def crackle(t0,dur,g=0.5,rate=14):
    for _ in range(int(dur*rate)):
        tt=t0+rng.uniform(0,dur);n=int(rng.uniform(0.004,0.02)*SR);s=hp(rng.normal(0,1,n).astype(np.float32),1500)*env(n,0.001,0.006);add(s,tt,g*rng.uniform(0.3,1))
def murmur(t0,dur,g=0.5):
    n=int(dur*SR);x=lp(rng.normal(0,1,n).astype(np.float32),1400)*(0.6+0.4*np.sin(2*math.pi*np.arange(n)/SR*3.1+rng.uniform(0,6)))
    e=np.minimum(np.arange(n)/SR/0.6,1)*np.minimum((n-np.arange(n))/SR/0.6,1);add(x*e,t0,g)
def creak(t0,dur=1.6,g=0.4):
    n=int(dur*SR);t=np.arange(n)/SR;f=95+40*np.sin(t*5.3)+25*t;ph=2*math.pi*np.cumsum(f)/SR
    s=((np.sin(ph)+0.6*np.sin(2*ph)+0.4*np.sin(3*ph))*0.4*(0.5+0.5*np.sin(t*37))).astype(np.float32)
    e=np.minimum(t/0.2,1)*np.minimum((dur-t)/0.4,1);add(s*e,t0,g)
def tick(t0,g=0.5):
    n=int(0.05*SR);s=hp(rng.normal(0,1,n).astype(np.float32),2000)*env(n,0.001,0.01);add(s,t0,g)

def clang(t0,g=0.5):
    n=int(0.35*SR);tt=np.arange(n)/SR
    s=hp(rng.normal(0,1,n).astype(np.float32),1800)*env(n,0.001,0.02)
    s+=(np.sin(2*math.pi*rng.choice([1700,2300,3100])*tt)*np.exp(-tt/0.09)).astype(np.float32)*0.5
    add(s,t0,g)
def clangs(a,b,rate=5,g=0.45):
    t=a
    while t<b: clang(t,g*rng.uniform(0.5,1));t+=rng.exponential(1/rate)
def bow(t0,g=0.5):
    n=int(0.9*SR);tt=np.arange(n)/SR
    tw=(np.sin(2*math.pi*(150+60*np.exp(-tt/0.04))*tt)*np.exp(-tt/0.07)).astype(np.float32)*0.9
    add(tw[:int(0.3*SR)],t0,g)
    d=int(0.55*SR);u=np.arange(d)/SR;f=2600-1500*(u/0.55)
    ph=np.cumsum(2*math.pi*f/SR);ws=(np.sin(ph)*0.25+hp(rng.normal(0,1,d).astype(np.float32),2500)*0.35)*np.minimum(u/0.05,1)*np.minimum((0.55-u)/0.1,1)
    add(ws.astype(np.float32),t0+0.05,g*0.8)
    th=int(0.12*SR);tu=np.arange(th)/SR;add((lp(rng.normal(0,1,th).astype(np.float32),500)*np.exp(-tu/0.025)*3).astype(np.float32),t0+0.6,g*0.9)
def volley(a,b,n,g=0.45):
    for k in range(n): bow(a+(b-a)*k/max(1,n-1)+rng.uniform(-0.12,0.12),g*rng.uniform(0.6,1))

# ---------- âm thanh mới cho cảnh sông nước (Ngô Quyền – Bạch Đằng)
def wave_bed(t0,t1,g=0.4):
    n=int((t1-t0)*SR);t=np.arange(n)/SR
    x=lp(rng.normal(0,1,n).astype(np.float32),1100)
    sw=0.5+0.5*np.sin(2*math.pi*t/6.5+rng.uniform(0,6));sw2=0.5+0.5*np.sin(2*math.pi*t/4.1+rng.uniform(0,6))
    e=(0.25+0.75*sw*sw2)*np.minimum(t/1.5,1)*np.minimum((t1-t0-t)/1.5,1)
    add((x*e).astype(np.float32),t0,g)
def rain(t0,t1,g=0.3):
    n=int((t1-t0)*SR);t=np.arange(n)/SR
    x=hp(lp(rng.normal(0,1,n).astype(np.float32),7000),1500)
    e=np.minimum(t/1.0,1)*np.minimum((t1-t0-t)/1.0,1);add((x*e).astype(np.float32),t0,g)
    crackle(t0,t1-t0,g*0.5,40)
def tide_rush(t0,dur,g=0.5,rising=True):
    n=int(dur*SR);t=np.arange(n)/SR;x=lp(rng.normal(0,1,n).astype(np.float32),900)
    u=t/dur;e=(u if rising else (1-u))**0.8*np.minimum((dur-t)/0.8,1)*np.minimum(t/0.3,1)
    sw=0.6+0.4*np.sin(2*math.pi*t*0.45);add((x*e*sw*1.4).astype(np.float32),t0,g)
def oars(t0,dur,g=0.35,iv=1.05):
    t=t0
    while t<t0+dur:
        n=int(0.35*SR);tt=np.arange(n)/SR
        s=lp(rng.normal(0,1,n).astype(np.float32),1800)*np.exp(-tt/0.09)*np.minimum(tt/0.02,1)
        add(s.astype(np.float32),t+rng.normal(0,0.03),g*rng.uniform(0.6,1));
        k=int(0.06*SR);add((lp(rng.normal(0,1,k).astype(np.float32),500)*env(k,0.002,0.02)).astype(np.float32),t+0.3,g*0.6)
        t+=iv*rng.uniform(0.92,1.08)
def splash(t0,g=0.6):
    n=int(0.9*SR);tt=np.arange(n)/SR
    s=hp(lp(rng.normal(0,1,n).astype(np.float32),4500),300)*np.exp(-tt/0.18)*np.minimum(tt/0.004,1)
    s+=lp(rng.normal(0,1,n).astype(np.float32),400)*np.exp(-tt/0.3)*0.9
    add(s.astype(np.float32),t0,g)
def woodcrack(t0,g=0.7):
    for k,o in enumerate([0,0.06,0.15]):
        n=int(0.25*SR);tt=np.arange(n)/SR
        s=hp(rng.normal(0,1,n).astype(np.float32),400)*np.exp(-tt/0.03)*np.minimum(tt/0.001,1)
        s+=(np.sin(2*math.pi*(180-60*k)*tt)*np.exp(-tt/0.06)).astype(np.float32)*0.8
        add(s.astype(np.float32),t0+o,g*(1-0.2*k))
    creak(t0+0.15,0.9,g*0.5);splash(t0+0.35,g*0.8)
def thunder(t0,g=0.8):
    n=int(3.2*SR);tt=np.arange(n)/SR
    s=lp(rng.normal(0,1,n).astype(np.float32),260)*np.exp(-tt/1.1)*np.minimum(tt/0.03,1)
    s+=lp(rng.normal(0,1,n).astype(np.float32),900)*np.exp(-tt/0.12)*np.minimum(tt/0.004,1)*0.7
    s+=(np.sin(2*math.pi*(55-10*tt)*tt)*np.exp(-tt/0.9)).astype(np.float32)*0.6
    add((s*1.2).astype(np.float32),t0,g)
def gong(t0,g=0.5):
    n=int(3.0*SR);tt=np.arange(n)/SR
    s=sum(np.sin(2*math.pi*f*tt+p)*a for f,a,p in [(96,1,0),(144,0.6,1),(213,0.45,2),(341,0.25,0.5)])*np.exp(-tt/1.1)
    s=s*np.minimum(tt/0.004,1)+hp(rng.normal(0,1,n).astype(np.float32),900)*np.exp(-tt/0.05)*0.4
    add((s*0.35).astype(np.float32),t0,g)
def gull(t0,g=0.25):
    n=int(0.7*SR);tt=np.arange(n)/SR;f=1500+500*np.sin(2*math.pi*tt*3)-500*tt
    ph=np.cumsum(2*math.pi*f/SR);s=(np.sin(ph)+0.4*np.sin(2*ph))*np.sin(np.linspace(0,math.pi,n))**1.2*0.4
    add(s.astype(np.float32),t0,g)
def war_drums(t0,t1,g=0.6,iv=0.75):
    t=t0;i=0
    while t<t1: drum(t,g*(1 if i%4==0 else 0.6));t+=iv;i+=1

def bt(n): return T[n]
_R_clangs,_R_volley,_R_murmur,_R_creak=clangs,volley,murmur,creak
if QA:
    _nop=lambda *a,**k:None
    tick=whoosh=crackle=murmur=clang=clangs=volley=bow=wave_bed=rain=creak=_nop

for (t0,t1,bl,bt_,who) in C.BATT:
    _R_clangs(t0,t1,6,0.55);_R_volley(t0+0.2,t1-0.5,max(3,int((t1-t0)*0.8)),0.45);drum(t0,0.8);_R_murmur(t0,t1-t0+1,0.45)
for (t0,t1,lon,lat) in C.FIRES: pass
fr_done=set()
for (t0,t1,lon,lat) in C.FIRES:
    k=int(t0)
    if k in fr_done: continue
    fr_done.add(k);crackle(t0,min(14,t1-t0),0.35,30)

def thump(t0,g=1.0):
    n=int(1.2*SR);t=np.arange(n)/SR;f=55*np.exp(-t*2.2)+28;ph=2*math.pi*np.cumsum(f)/SR
    s=np.sin(ph)*np.exp(-t/0.35)+lp(rng.normal(0,1,n).astype(np.float32),400)*np.exp(-t/0.12)*1.2
    add(s.astype(np.float32),t0,g)
def stone_whistle(t0,dur,g=0.4):
    n=int(dur*SR);t=np.arange(n)/SR;f=700-380*(t/dur);ph=np.cumsum(2*math.pi*f/SR)
    s=(np.sin(ph)*0.3+lp(rng.normal(0,1,n).astype(np.float32),1800)*0.25)*np.sin(np.linspace(0,math.pi,n))**1.5
    add(s.astype(np.float32),t0,g)
def horn(t0,dur=1.8,g=0.45):
    n=int(dur*SR);t=np.arange(n)/SR;f=116*(1+0.012*np.sin(t*6))*(1+0.06*np.minimum(t/0.3,1));ph=np.cumsum(2*math.pi*f/SR)
    s=(np.sin(ph)+0.7*np.sin(2*ph)+0.5*np.sin(3*ph)+0.3*np.sin(4*ph))*0.35
    e=np.minimum(t/0.25,1)*np.minimum((dur-t)/0.5,1);add((s*e).astype(np.float32),t0,g)
for (t0,t1,kind,a_,b_) in getattr(C,'FX',[]):
    if kind=='catapult':
        j=0
        while t0+j*2.2<=t1:
            ts=t0+j*2.2;creak(ts-0.2,0.5,0.3);thump(ts+0.25,0.5);stone_whistle(ts+0.3,1.2,0.35);thump(ts+1.5,1.0);crackle(ts+1.5,0.5,0.3,30);j+=1
    elif kind=='firearrows':
        volley(t0,t1,max(4,int((t1-t0)*3)),0.4);crackle(t0,t1-t0+1,0.3,18)
    elif kind=='horn':
        horn(t0,min(2.2,t1-t0+0.8),0.5)
    elif kind=='volley':
        volley(t0,t1,max(4,int((t1-t0)*2.5)),0.3)
for (t0,t1,kind,a_,b_) in getattr(C,'FX',[]):
    if kind=='crack': woodcrack(t0,0.8)
    elif kind=='splash': splash(t0,0.6)
    elif kind=='gong': gong(t0,0.6)
    elif kind=='oars': oars(t0,t1-t0,0.35)
    elif kind=='drums': war_drums(t0,t1,0.6)
    elif kind=='tide_up': tide_rush(t0,t1-t0,0.55,True)
    elif kind=='tide_down': tide_rush(t0,t1-t0,0.6,False)
def trumpet(t0,dur=1.3,g=0.5):
    n=int(dur*SR);t=np.arange(n)/SR;f=380*(1+0.35*np.minimum(t/0.2,1))*(1-0.25*np.clip((t-0.7)/0.6,0,1))*(1+0.02*np.sin(t*40));ph=np.cumsum(2*math.pi*f/SR)
    s=(np.sin(ph)+0.8*np.sin(2*ph)+0.5*np.sin(3*ph)+0.3*np.sin(5*ph))*0.3+lp(rng.normal(0,1,n).astype(np.float32),2500)*0.12
    e=np.minimum(t/0.08,1)*np.minimum((dur-t)/0.4,1);add((s*e).astype(np.float32),t0,g)
for (t0,t1,kind,a_,b_) in getattr(C,'FX',[]):
    if kind=='trumpet': trumpet(t0,min(1.6,t1-t0+0.6),0.5)
for g_ in C.GROUPS:
    if g_.get('kind')=='ele':
        ks=g_['keys']
        for i in range(len(ks)-1):
            if (ks[i+1][1],ks[i+1][2])!=(ks[i][1],ks[i][2]):
                tt=ks[i][0]
                while tt<ks[i+1][0]-0.3: thump(tt,0.35);tt+=0.95
for (t0,t1,kind,gn) in getattr(C,'AMBIENT',[]):
    if kind=='sea': wave_bed(t0,t1,gn)
    elif kind=='rain': rain(t0,t1,gn)
    elif QA and kind!='gulls': pass
    elif kind=='wind':
        n=int((t1-t0)*SR);x=lp(lp(rng.normal(0,1,n).astype(np.float32),700),500);x=x*(0.5+0.5*np.sin(2*math.pi*np.arange(n)/SR/5.5+rng.uniform(0,6)))
        add(x*np.minimum(np.minimum(np.arange(n)/SR/1.5,1),np.minimum((n-np.arange(n))/SR/1.5,1)).astype(np.float32),t0,gn*2.2)
    elif kind=='forest':
        tt=t0+0.5
        while tt<t1-0.5:
            f0=rng.uniform(2200,3800);m=int(0.16*SR);tq=np.arange(m)/SR
            add((np.sin(2*math.pi*(f0*tq+900*tq**2))*env(m,0.01,0.07)).astype(np.float32),tt,gn*0.5)
            if rng.random()<0.6: add((np.sin(2*math.pi*(f0*1.12*tq+700*tq**2))*env(m,0.01,0.06)).astype(np.float32),tt+0.2,gn*0.4)
            tt+=rng.uniform(1.2,3.8)
        n=int((t1-t0)*SR);add(lp(rng.normal(0,1,n).astype(np.float32),600)*0.5,t0,gn*0.8)
    elif kind=='night':
        n=int((t1-t0)*SR);tc=np.arange(n)/SR
        cr=(np.sin(2*math.pi*4300*tc)*(np.sin(2*math.pi*17*tc)>0.3)).astype(np.float32)*(0.6+0.4*np.sin(2*math.pi*tc/4.3))
        add(cr*np.minimum(np.minimum(tc/1.5,1),np.minimum((t1-t0-tc)/1.5,1)).astype(np.float32),t0,gn*0.35)
        tt=t0+rng.uniform(2,6)
        while tt<t1-2:
            m=int(0.55*SR);tq=np.arange(m)/SR;add((np.sin(2*math.pi*(420*tq-120*tq**2))*env(m,0.05,0.25)).astype(np.float32),tt,gn*0.35);tt+=rng.uniform(7,14)
    elif kind=='crowd':
        tt=t0
        while tt<t1-0.5: murmur(tt,min(3.0,t1-tt),gn);tt+=2.4
    elif kind=='fire': crackle(t0,t1-t0,gn,16)
    elif kind=='gulls':
        tt=t0
        while tt<t1: gull(tt,gn);tt+=rng.uniform(3,7)
for (t0,t1,kind,a_,b_) in getattr(C,'OBJ',[]):
    if kind=='tower': thump(t1+0.05,0.9);crackle(t1,1.2,0.3,25)
    elif kind in ('tunnel','ditch'): steps(t0,2.5)
    elif kind=='loot': tick(t0+0.5,0.5)
for x in getattr(C,'TITLES',[]): thump(x[0],1.0);horn(x[0]+0.1,2.4,0.4)
for (ts,kd) in getattr(C,'SFX',[]):
    if kd=='horn': horn(ts,1.8,0.45)
    elif kd=='gong': gong(ts,0.6)
    elif kd=='trumpet': trumpet(ts,1.3,0.5)
    elif kd=='thunder': thunder(ts,0.8)
for x in getattr(C,'JOKES',[]): tick(x[0],0.9);tick(x[0]+0.12,0.5)
for x in getattr(C,'QUOTES',[]): tick(x[0],0.5)
for x in getattr(C,'CARDS3',[]): tick(x[0],0.35)
for x in getattr(C,'METERS',[]): tick(x[0],0.5)
for (t0,t1,a_,b_,nm) in C.LETTERS: whoosh(t0,min(4,t1-t0),0.35)
for (t0,t1,a_,b_,col,lab) in C.ARROWS: tick(t0,0.35)
for g in C.GROUPS:
    ks=g['keys'];kind=g.get('kind','inf')
    if QA and g.get('label') is False and g['name'] not in getattr(C,'SFX_GROUPS',()): continue
    for i in range(len(ks)-1):
        a_,b_=ks[i],ks[i+1]
        if (a_[1],a_[2])!=(b_[1],b_[2]) and b_[0]-a_[0]>0.6 and b_[0]<TOTAL:
            if kind=='cav':
                hoof(a_[0]+0.3,min(b_[0]-a_[0],8.0),0.2)
                if g['name'] in getattr(C,'SFX_GROUPS',()): clop(a_[0]+0.3,min(b_[0]-a_[0],8.0));bells(a_[0]+0.3,min(b_[0]-a_[0],8.0))
            elif kind=='ship':
                oars(a_[0]+0.3,min(b_[0]-a_[0],8.0),0.4);_R_creak(a_[0]+0.5,1.6,0.3)
            else: steps(a_[0]+0.3,min(b_[0]-a_[0],8.0))
if C.__name__=='tq45_content':
    for t0 in (C.R(137)+6.5,C.R(144)): creak(t0)
for (t0,t1,tx,ty,txt,col) in C.NOTES:
    if txt in ('TRÚNG!',): tick(t0,0.8)
for m in C.MARKS: drum(m[0],0.9)
if C.__name__!='tq45_content':
  for g in C.GROUPS:
    for (td,kd,te) in g.get('defeats',[]) or []:
        if td<TOTAL: drum(td,0.8)
# nhạc nền tự tổng hợp (không dùng bản nhạc có bản quyền). Chỉ chạy khi file nội dung khai báo MUSIC=[(bắt đầu, kết thúc, tâm trạng, âm lượng)].
def _pluck(t0,f,g=0.5,dec=0.9):
    n=int(min(2.5,dec*4)*SR);t=np.arange(n)/SR
    y=(np.sin(2*math.pi*f*t)+0.4*np.sin(2*math.pi*2*f*t)+0.15*np.sin(2*math.pi*3*f*t))*np.exp(-t/dec)*np.minimum(t/0.006,1)
    add(y.astype(np.float32),t0,g)
def _pad(t0,t1,freqs,g=0.3,steady=False):
    n=int((t1-t0)*SR);t=np.arange(n)/SR;y=np.zeros(n,np.float32)
    for k,f in enumerate(freqs):
        for dt in ((0.0,) if steady else (-0.7,0.7)): y+=np.sin(2*math.pi*(f+dt)*t+k).astype(np.float32)
    y*=np.minimum(np.minimum(t/1.8,1),np.minimum((t1-t0-t)/1.8,1)).astype(np.float32)
    if not steady: y*=(0.8+0.2*np.sin(2*math.pi*t/7.0)).astype(np.float32)
    add(lp(y,1400)/max(1,len(freqs))*(1.6 if steady else 1.0),t0,g)
_N={'D2':73.4,'A2':110.0,'F2':87.3,'G2':98.0,'D3':146.8,'A3':220.0,'F3':174.6,'E3':164.8,'G3':196.0,'B3':246.9,'C4':261.6,'D4':293.7,'E4':329.6,'F4':349.2,'G4':392.0,'A4':440.0,'B4':493.9,'C5':523.3,'D5':587.3}
_MOOD={'binh':(['D2','A2','D3'],['D4','E4','G4','A4','B4'],2.4,0.9),'mo':(['D2','A2','E3'],['A4','G4','E4','D4'],3.2,0.8),
 'bi':(['D2','F2','A2'],['D4','F4','A4','G4'],3.0,1.0),'loan':(['D2','A2','F3'],['D4','F4','E4','A4','C5'],1.4,0.5),
 'cang':(['D2','A2'],['A3','D4','F4'],1.8,0.6),'hanh':(['D2','A2','D3'],['D4','F4','G4','A4'],1.1,0.45),
 'vac':(['D2','A2','D3'],['D4','E4','G4','A4','B4'],2.2,0.9),
 'trang':(['D2','A2','D3','A3'],['D4','E4','G4','A4','B4','D5'],1.6,0.9),'dem':(['D2','A2'],['A3','D4','E4'],3.8,1.2)}
_rm=np.random.default_rng(11)
for (m0,m1,mood,vol) in getattr(C,'MUSIC',[]):
    if m1<=m0 or mood not in _MOOD: continue
    drone,mel,gap,dec=_MOOD[mood]
    _pad(m0,min(m1+1.0,TOTAL-0.5),[_N[x] for x in drone],0.20*vol,steady=(mood=='vac'))
    t=m0+0.6
    while t<m1-0.8:
        _pluck(t,_N[mel[int(_rm.integers(len(mel)))]],0.16*vol,dec);t+=gap*(0.75+0.5*_rm.random())
    if mood in ('cang','hanh','loan'):
        iv={'cang':0.9,'hanh':0.62,'loan':0.5}[mood];tt=m0+0.3
        while tt<m1-0.3: thump(tt,0.35*vol) if 'thump' in globals() else drum(tt,0.35*vol);tt+=iv
# phủ mờ vào/ra, chuẩn hóa
fade=int(0.8*SR);out[:fade]*=np.linspace(0,1,fade);out[-fade:]*=np.linspace(1,0,fade)
out=lp(out,9000);out=out/np.max(np.abs(out))*0.7
import os,subprocess
VD=os.environ.get('VOICE_DIR','')
if VD:
    sfx=out.copy();voice=np.zeros(N,np.float32)
    for n in T:
        raw=subprocess.run(['ffmpeg','-v','error','-i',f'{VD}/{n}.mp3','-f','f32le','-ac','1','-ar',str(SR),'-'],capture_output=True).stdout
        v=np.frombuffer(raw,np.float32);i0=int((T[n]+0.12)*SR);j0=min(N,i0+len(v));voice[i0:j0]+=v[:j0-i0]
    voice=voice/max(1e-6,np.max(np.abs(voice)))*0.85
    # nhường tiếng: SFX nhỏ lại khi đang đọc
    m=np.convolve(np.abs(voice),np.ones(2000)/2000,'same');duck=1-0.55*np.clip(m*14,0,1)
    out=np.clip(voice+sfx*duck*0.9,-1,1)
pcm=(out*32767).astype(np.int16)
with wave.open(__import__('os').environ.get('A2_OUT','/tmp/proto/a2.wav'),'wb') as f: f.setnchannels(1);f.setsampwidth(2);f.setframerate(SR);f.writeframes(pcm.tobytes())
print('ok',TOTAL)
