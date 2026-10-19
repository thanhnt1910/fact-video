import json,math,wave,numpy as np,sys
sys.argv=['x','none']
import importlib.util
spec=importlib.util.spec_from_file_location('b','/tmp/proto/build.py');b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
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
out+=w*mod*0.9
# tiếng vó ngựa phi: nhịp 4 bước
def hoof(t0,dur,spd=0.17):
    t=t0
    while t<t0+dur:
        for k,o in enumerate([0,0.05,0.12,0.19]):
            n=int(0.09*SR);s=lp(rng.normal(0,1,n).astype(np.float32),900)*env(n,0.002,0.025)*(0.9 if k%2==0 else 0.6)
            s+=np.sin(2*math.pi*110*np.arange(n)/SR).astype(np.float32)*env(n,0.002,0.03)*0.7
            add(s,t+o,0.9)
        t+=0.19+spd*0.8
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
# --- lịch tiếng động theo bản đồ
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
t128,t129,t131,t132,t133,t134,t135,t136,t137,t138,t139,t140,t141=[T[i] for i in (128,129,131,132,133,134,135,136,137,138,139,140,141)]
whoosh(t128+3.0,5.5,0.5);tick(t128+0.8,0.5)
steps(t129+0.3,4.0);murmur(t129+4.5,6.0,0.5);clangs(t129+4.5,t129+10.5,6);volley(t129+4.6,t129+9,5)
drum(t129+4.5,0.9)
hoof(t132+0.6,2.2,0.2);murmur(t132,D[132],0.2)
clangs(t133,t133+3.5,1.6,0.25);volley(t133+0.5,t133+3,2,0.3)
whoosh(t135+3.0,3.8,0.4);whoosh(t136+0.2,3.4,0.5)
clangs(t137+1.5,t137+5.5,5);murmur(t137,5,0.3);creak(t137+6.5)
steps(t138,6.0);murmur(t138,5,0.4)
drum(t139+0.4,1.0);hoof(t139+0.1,3.0);clangs(t139+0.5,t139+4.5,6);volley(t139+0.6,t139+3.5,4,0.4)
for n in(139,140): crackle(T[n],D[n],0.55 if n==139 else 0.3)
crackle(t139+0.5,D[139]-1,0.55,34);drum(t141+0.6,1.0);murmur(T[143],D[143],0.3)
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
with wave.open('/tmp/proto/a.wav','wb') as f: f.setnchannels(1);f.setsampwidth(2);f.setframerate(SR);f.writeframes(pcm.tobytes())
print('ok',TOTAL)
