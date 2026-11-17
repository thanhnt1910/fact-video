# Phần chung âm thanh tm5–tm10: giọng gốc giữ nguyên, hiệu ứng và nhạc nằm dưới
import subprocess,wave
from sfx import *
import sys as _s;_s.path.insert(0,'/tmp/pc');from audio_fx import VOICE_CHAIN as CHAIN
from sfx import _guard
def hooves(m,t0,dur,g=.35,iv=.16):
    t=t0
    while t<t0+dur:
        for k,dt in enumerate((0,.05,.11,.15)):
            n=int(.07*SR);m.add(lp(m.nz(n),900)*env(n,.002,.02),t+dt,g*(1 if k%2==0 else .7),m.rng.uniform(-.3,.3))
        t+=iv*2.6
hooves=_guard(hooves)
def rainsnd(m,t0,dur,g=.15):
    n=int(dur*SR);x=lp(hp(m.nz(n),800),6000)*.5
    m.add((x*fadeio(n,.8,.8)).astype(np.float32),t0,g)
rainsnd=_guard(rainsnd)
def cannon(m,t0,g=.6):
    n=int(1.6*SR);x=lp(m.nz(n),180)*env(n,.003,.5)*3+lp(m.nz(n),1200)*env(n,.001,.08)
    m.add(x.astype(np.float32),t0,g,m.rng.uniform(-.4,.4))
cannon=_guard(cannon)
def battle(m,a,b,g=1.0,arrows=10):
    war_drums(m,a,b,.5*g,.45);volley(m,a+.2,b,arrows,.3*g);shouts(m,a+.3,min(3.5,b-a),.45*g);clangs(m,a+.5,b,5,.3*g)
def voice_mix(M,Ts,files,duck=.55,cuts=None):
    v=np.zeros(M.N,np.float32)
    for k,(t0,f) in enumerate(zip(Ts,files)):
        cut=['-ss',f'{cuts[k][0]:.3f}','-to',f'{cuts[k][1]:.3f}'] if cuts else []
        af=['-af',CHAIN] if cuts else []   # giọng cả video: qua cùng chuỗi lọc 'radio' như các tập tm2–tm4 (một file liền nên không làm lệch giữa các câu)
        raw=subprocess.run(['ffmpeg','-v','error',*cut,'-i',f,*af,'-f','f32le','-ac','1','-ar',str(SR),'-'],capture_output=True).stdout
        a=np.frombuffer(raw,np.float32);i=int(t0*SR);j=min(M.N,i+len(a));v[i:j]+=a[:j-i]
    e=np.convolve(np.abs(v),np.ones(4000)/4000,'same');d=1-duck*np.clip(e*12,0,1)
    return v,d.astype(np.float32)
def write_mix(M,v,d,path):
    L,R=M.L*d,M.R*d;f=int(.6*SR)
    for x in (L,R): x[:f]*=np.linspace(0,1,f);x[-f:]*=np.linspace(1,0,f)
    L=lp(L,11000);R=lp(R,11000)
    vr=np.sqrt(np.mean(v[np.abs(v)>1e-3]**2))
    st=np.stack([L,R],1);sr=np.sqrt(np.mean(st**2))+1e-9;st=st/sr*vr*.32
    hr=np.maximum(0,.99-np.abs(v))[:,None];st=np.clip(st,-hr,hr)
    out=np.clip(st+v[:,None],-1,1)
    with wave.open(path,'wb') as w: w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((out*32767).astype(np.int16).tobytes())
def finish(M,Vv,path):
    if getattr(Vv,'CH',None):
        v,d=voice_mix(M,[c[0] for c in Vv.CH],[c[1] for c in Vv.CH],cuts=[(c[2],c[3]) for c in Vv.CH]);write_mix(M,v,d,path);print('ok chương',round(Vv.TOTAL,1));return
    ns=sorted(Vv.TX);files=[f"{__import__('khung_dung').GD}/{Vv.NN[n]}.mp3" for n in ns]
    v,d=voice_mix(M,[Vv.T[n] for n in ns],files);write_mix(M,v,d,path);print('ok',round(Vv.TOTAL,1))
