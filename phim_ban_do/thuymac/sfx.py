# Hiệu ứng âm thanh + nhạc nền tự tổng hợp (không dùng bản ghi có bản quyền)
import numpy as np,math,wave
from scipy.signal import lfilter
SR=44100
class Mix:
    def __init__(s,total,seed=7):
        s.N=int(total*SR);s.L=np.zeros(s.N,np.float32);s.R=np.zeros(s.N,np.float32);s.rng=np.random.default_rng(seed)
    def nz(s,n): return s.rng.normal(0,1,n).astype(np.float32)
    def add(s,sig,t0,g=1.0,pan=0.0):
        i=int(t0*SR);j=min(s.N,i+len(sig))
        if i<0 or i>=s.N or j<=i: return
        gl=g*math.cos((pan+1)*math.pi/4)*1.41;gr=g*math.sin((pan+1)*math.pi/4)*1.41
        s.L[i:j]+=sig[:j-i]*gl;s.R[i:j]+=sig[:j-i]*gr
def lp(x,fc):
    a=math.exp(-2*math.pi*fc/SR);return lfilter([1-a],[1,-a],x).astype(np.float32)
def hp(x,fc): return x-lp(x,fc)
def env(n,a=0.005,d=0.15):
    t=np.arange(n)/SR;return (np.minimum(t/a,1)*np.exp(-t/d)).astype(np.float32)
def fadeio(n,a,b):
    t=np.arange(n)/SR;return (np.minimum(t/a,1)*np.minimum((n/SR-t)/b,1)).astype(np.float32)
# ---- âm cụ thể
def wave_bed(m,t0,t1,g=.4):
    n=int((t1-t0)*SR);t=np.arange(n)/SR
    for p in (-.5,.5):
        x=lp(m.nz(n),1000);sw=.5+.5*np.sin(2*math.pi*t/6.5+m.rng.uniform(0,6));sw2=.5+.5*np.sin(2*math.pi*t/4.1+m.rng.uniform(0,6))
        m.add(x*(.25+.75*sw*sw2)*fadeio(n,1.5,1.5),t0,g,p)
def wind(m,t0,t1,g=.3):
    n=int((t1-t0)*SR);x=lp(lp(m.nz(n),600),400)*(.5+.5*np.sin(2*math.pi*np.arange(n)/SR/5.5+1))
    m.add(x*fadeio(n,2,2)*2.0,t0,g)
def lap(m,t0,t1,g=.25):  # nước vỗ mạn thuyền
    t=t0
    while t<t1:
        n=int(.25*SR);m.add(hp(lp(m.nz(n),1600),200)*env(n,.03,.07),t,g*m.rng.uniform(.4,1),m.rng.uniform(-.6,.6));t+=m.rng.uniform(.4,1.1)
def drop(m,t0,g=.8):  # giọt mực rơi
    n=int(.5*SR);tt=np.arange(n)/SR;f=900*np.exp(-tt*9)+180
    s=np.sin(np.cumsum(2*math.pi*f/SR))*np.exp(-tt/.09)
    m.add(s.astype(np.float32),t0,g);thump(m,t0+.03,.5)
def thump(m,t0,g=1.0):
    n=int(1.2*SR);t=np.arange(n)/SR;f=55*np.exp(-t*2.2)+28
    s=np.sin(2*math.pi*np.cumsum(f)/SR)*np.exp(-t/.35)+lp(m.nz(n),400)*np.exp(-t/.12)*1.2
    m.add(s.astype(np.float32),t0,g)
def stamp(m,t0,g=.7):  # triện đóng xuống
    n=int(.3*SR);tt=np.arange(n)/SR
    s=lp(m.nz(n),900)*np.exp(-tt/.025)*2+np.sin(2*math.pi*120*tt)*np.exp(-tt/.05)
    m.add(s.astype(np.float32),t0,g);thump(m,t0,.35)
def brush(m,t0,dur=.7,g=.35,pan=0):  # nét cọ quét
    n=int(dur*SR);x=hp(lp(m.nz(n),5000),900);e=np.sin(np.linspace(0,math.pi,n))**1.5
    m.add(x*e.astype(np.float32),t0,g,pan)
def whoosh(m,t0,dur,g=.5):
    n=int(dur*SR);x=hp(lp(m.nz(n),2500),250);e=np.sin(np.linspace(0,math.pi,n))**2;m.add(x*e.astype(np.float32),t0,g)
def gong(m,t0,g=.5):
    n=int(3.5*SR);tt=np.arange(n)/SR
    s=sum(np.sin(2*math.pi*f*tt+p)*a for f,a,p in [(96,1,0),(144,.6,1),(213,.45,2),(341,.25,.5)])*np.exp(-tt/1.2)
    s=s*np.minimum(tt/.004,1)+hp(m.nz(n),900)*np.exp(-tt/.05)*.4;m.add((s*.35).astype(np.float32),t0,g)
def drum(m,t0,g=1.0):
    n=int(.7*SR);t=np.arange(n)/SR;f=70*np.exp(-t*3);m.add((np.sin(2*math.pi*np.cumsum(f)/SR)*np.exp(-t/.25)).astype(np.float32),t0,g*1.2)
def war_drums(m,t0,t1,g=.6,iv=.6):
    t=t0;i=0
    while t<t1: drum(m,t,g*(1 if i%4==0 else .55));drum(m,t+iv*.5,g*.3) if i%2 else None;t+=iv;i+=1
def oars(m,t0,t1,g=.3,iv=1.0,pan=0):
    t=t0
    while t<t1:
        n=int(.35*SR);tt=np.arange(n)/SR;s=lp(m.nz(n),1800)*np.exp(-tt/.09)*np.minimum(tt/.02,1)
        m.add(s.astype(np.float32),t+m.rng.normal(0,.03),g*m.rng.uniform(.6,1),pan);t+=iv*m.rng.uniform(.92,1.08)
def splash(m,t0,g=.6,pan=0):
    n=int(.9*SR);tt=np.arange(n)/SR
    s=hp(lp(m.nz(n),4500),300)*np.exp(-tt/.18)*np.minimum(tt/.004,1)+lp(m.nz(n),400)*np.exp(-tt/.3)*.9
    m.add(s.astype(np.float32),t0,g,pan)
def creak(m,t0,dur=1.4,g=.4):
    n=int(dur*SR);t=np.arange(n)/SR;f=95+40*np.sin(t*5.3)+25*t;ph=2*math.pi*np.cumsum(f)/SR
    s=((np.sin(ph)+.6*np.sin(2*ph)+.4*np.sin(3*ph))*.4*(.5+.5*np.sin(t*37)))*np.minimum(t/.2,1)*np.minimum((dur-t)/.4,1)
    m.add(s.astype(np.float32),t0,g)
def woodcrack(m,t0,g=.7,pan=0):
    for k,o in enumerate([0,.06,.15]):
        n=int(.25*SR);tt=np.arange(n)/SR
        s=hp(m.nz(n),400)*np.exp(-tt/.03)+np.sin(2*math.pi*(180-60*k)*tt)*np.exp(-tt/.06)*.8
        m.add(s.astype(np.float32),t0+o,g*(1-.2*k),pan)
    creak(m,t0+.15,.9,g*.5);splash(m,t0+.35,g*.8,pan)
def stake_hit(m,t0,g=.5):  # đóng cọc: tiếng gỗ đục
    n=int(.18*SR);tt=np.arange(n)/SR
    s=np.sin(2*math.pi*230*tt)*np.exp(-tt/.035)+lp(m.nz(n),1500)*np.exp(-tt/.012)
    m.add(s.astype(np.float32),t0,g,m.rng.uniform(-.5,.5))
def tide(m,t0,dur,g=.5,rising=True):
    n=int(dur*SR);t=np.arange(n)/SR;u=t/dur
    for p in (-.6,.6):
        x=lp(m.nz(n),800);e=(u if rising else 1-u)**.7*np.minimum((dur-t)/.8,1)*np.minimum(t/.3,1)
        m.add((x*e*(.6+.4*np.sin(2*math.pi*t*.45))*1.4).astype(np.float32),t0,g,p)
def gull(m,t0,g=.2):
    n=int(.7*SR);tt=np.arange(n)/SR;f=1500+500*np.sin(2*math.pi*tt*3)-500*tt;ph=np.cumsum(2*math.pi*f/SR)
    m.add(((np.sin(ph)+.4*np.sin(2*ph))*np.sin(np.linspace(0,math.pi,n))**1.2*.4).astype(np.float32),t0,g,m.rng.uniform(-.7,.7))
def gulls(m,t0,t1,g=.18):
    t=t0+1
    while t<t1-1: gull(m,t,g);t+=m.rng.uniform(3,7)
def bow(m,t0,g=.5,pan=0):  # tên bay
    d=int(.55*SR);u=np.arange(d)/SR;f=2600-1500*(u/.55);ph=np.cumsum(2*math.pi*f/SR)
    ws=(np.sin(ph)*.2+hp(m.nz(d),2500)*.35)*np.minimum(u/.05,1)*np.minimum((.55-u)/.1,1);m.add(ws.astype(np.float32),t0,g,pan)
    th=int(.1*SR);tu=np.arange(th)/SR;m.add((lp(m.nz(th),600)*np.exp(-tu/.02)*2.5).astype(np.float32),t0+.5,g*.6,pan)
def volley(m,a,b,n,g=.4):
    for k in range(n): bow(m,a+(b-a)*k/max(1,n-1)+m.rng.uniform(-.12,.12),g*m.rng.uniform(.6,1),m.rng.uniform(-.8,.8))
def clang(m,t0,g=.4):
    n=int(.35*SR);tt=np.arange(n)/SR
    s=hp(m.nz(n),1800)*env(n,.001,.02)+np.sin(2*math.pi*m.rng.choice([1700,2300,3100])*tt)*np.exp(-tt/.09)*.5
    m.add(s.astype(np.float32),t0,g,m.rng.uniform(-.7,.7))
def clangs(m,a,b,rate=4,g=.35):
    t=a
    while t<b: clang(m,t,g*m.rng.uniform(.5,1));t+=m.rng.exponential(1/rate)
def shouts(m,t0,dur,g=.45):  # tiếng hô của đám đông (nhiễu lọc dải, không lời)
    n=int(dur*SR);t=np.arange(n)/SR;x=np.zeros(n,np.float32)
    for k in range(5):
        f0=m.rng.uniform(180,320);ph=np.cumsum(2*math.pi*(f0*(1+.08*np.sin(t*m.rng.uniform(3,6))))/SR)
        x+=(np.sin(ph)+.5*np.sin(2*ph)+.3*np.sin(3*ph)).astype(np.float32)*(.5+.5*np.sin(t*m.rng.uniform(1,2.5)+k))
    x=lp(x*.15+lp(m.nz(n),1200)*.5,1800);m.add(x*fadeio(n,.4,.8),t0,g)
def horn(m,t0,dur=1.8,g=.45):
    n=int(dur*SR);t=np.arange(n)/SR;f=116*(1+.012*np.sin(t*6))*(1+.06*np.minimum(t/.3,1));ph=np.cumsum(2*math.pi*f/SR)
    s=(np.sin(ph)+.7*np.sin(2*ph)+.5*np.sin(3*ph)+.3*np.sin(4*ph))*.35*np.minimum(t/.25,1)*np.minimum((dur-t)/.5,1);m.add(s.astype(np.float32),t0,g)
# ---- nhạc nền: đàn tranh gảy (âm ngũ cung) trên nền âm trầm
NT={'D2':73.4,'A2':110.0,'F2':87.3,'D3':146.8,'A3':220.0,'E3':164.8,'C4':261.6,'D4':293.7,'E4':329.6,'F4':349.2,'G4':392.0,'A4':440.0,'C5':523.3,'D5':587.3}
MOOD={'binh':(['D2','A2','D3'],['D4','E4','G4','A4','D5'],2.2,.9),'mo':(['D2','A2','E3'],['A4','G4','E4','D4'],3.0,.8),
'bi':(['D2','F2','A2'],['D4','F4','A4','G4'],3.0,1.0),'cang':(['D2','A2'],['A3','D4','F4','E4'],1.6,.6),'loan':(['D2','A2','F2'],['D4','F4','E4','A4','C5'],1.0,.45),
'trang':(['D2','A2','D3','A3'],['D4','E4','G4','A4','D5'],1.5,.9)}
def pluck(m,t0,f,g=.5,dec=.9):
    n=int(min(2.5,dec*4)*SR);t=np.arange(n)/SR
    y=(np.sin(2*math.pi*f*t)+.4*np.sin(2*math.pi*2*f*t)+.15*np.sin(2*math.pi*3*f*t))*np.exp(-t/dec)*np.minimum(t/.006,1)
    # rung dây (luyến) như đàn tranh
    y*=1+.0*t;m.add(y.astype(np.float32),t0,g,m.rng.uniform(-.4,.4))
def pad(m,t0,t1,fs,g=.3):
    n=int((t1-t0)*SR);t=np.arange(n)/SR;y=np.zeros(n,np.float32)
    for k,f in enumerate(fs):
        for dt in (-.7,.7): y+=np.sin(2*math.pi*(f+dt)*t+k).astype(np.float32)
    y*=fadeio(n,1.8,1.8)*(.8+.2*np.sin(2*math.pi*t/7)).astype(np.float32);m.add(lp(y,1400)/len(fs),t0,g)
def music(m,t0,t1,mood,vol=1.0):
    dr,mel,gap,dec=MOOD[mood];pad(m,t0,t1+1,[NT[x] for x in dr],.2*vol);t=t0+.5
    while t<t1-.8: pluck(m,t,NT[mel[int(m.rng.integers(len(mel)))]],.15*vol,dec);t+=gap*(.75+.5*m.rng.random())
def write(m,path,total):
    L,R=m.L,m.R;f=int(.6*SR)
    for x in (L,R): x[:f]*=np.linspace(0,1,f);x[-f:]*=np.linspace(1,0,f)
    L=lp(L,11000);R=lp(R,11000);pk=max(np.max(np.abs(L)),np.max(np.abs(R)),1e-6)
    # nén nhẹ rồi chuẩn hóa
    st=np.stack([L,R],1);q=np.percentile(np.abs(st),99.7);st=st/max(q,1e-6)*.55;st=np.tanh(st*1.3)/1.3*1.05;st=np.clip(st,-.95,.95)
    with wave.open(path,'wb') as w: w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((st*32767).astype(np.int16).tobytes())

def steps(m,t0,t1,g=.35,iv=.5):
    t=t0;i=0
    while t<t1:
        n=int(.12*SR);m.add(lp(m.nz(n),600)*env(n,.003,.035)*(1 if i%2==0 else .8),t+m.rng.normal(0,.012),g,m.rng.uniform(-.5,.5));t+=iv;i+=1
def march(m,t0,t1,g=.35):
    for k in range(4): steps(m,t0+k*.11,t1,g*.6,.55)
# bỏ qua sự kiện nằm ngoài thời lượng (cảnh không dùng trong bản này)
import functools as _ft
def _guard(f):
    @_ft.wraps(f)
    def w(m,t0,*a,**k):
        if t0<0 or t0>=m.N/SR-0.05: return
        if a and isinstance(a[0],(int,float)) and f.__name__ in ('wave_bed','wind','lap','steps','march','oars','war_drums','gulls','clangs','volley','music','pad') and a[0]<=t0: return
        if f.__name__ in ('tide','shouts','whoosh','brush','creak') and a and a[0]<=0: return
        return f(m,t0,*a,**k)
    return w
for _n in ['wave_bed','wind','lap','drop','thump','stamp','brush','whoosh','gong','drum','war_drums','oars','splash','creak','woodcrack','stake_hit','tide','gull','gulls','bow','volley','clang','clangs','shouts','horn','pluck','pad','music','steps','march']:
    globals()[_n]=_guard(globals()[_n])
