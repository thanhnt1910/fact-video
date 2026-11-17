# Âm thanh tm4: hiệu ứng + nhạc tự tổng hợp; giọng Charon gốc giữ nguyên (không cân giọng)
import subprocess,wave
from sfx import *
from sfx import _guard
import dai_tm4 as V
T,E,mid=V.T,V.E,V.mid
M=Mix(V.TOTAL,17)
def hooves(m,t0,dur,g=.35,iv=.16):
    t=t0
    while t<t0+dur:
        for k,dt in enumerate((0,.05,.11,.15)):
            n=int(.07*SR);m.add(lp(m.nz(n),900)*env(n,.002,.02),t+dt,g*(1 if k%2==0 else .7),m.rng.uniform(-.3,.3))
        t+=iv*2.6
hooves=_guard(hooves)
def fire(m,t0,dur,g=.12):
    n=int(dur*SR);x=lp(m.nz(n),2500)*.2
    k=m.rng.random(n)<.0006;x+=hp(np.convolve(k.astype(np.float32),np.exp(-np.arange(300)/40),'same')*m.nz(n),1500)*.8
    m.add((x*fadeio(n,.5,.5)).astype(np.float32),t0,g)
fire=_guard(fire)
wind(M,.2,V.TOTAL-.5,.12)
CH=[(0,T[6]-4,'cang',1.0),(T[6],T[10],'mo',.9),(T[10],T[11]-2.4,'cang',.9),(T[11],E[13],'loan',1.0),(T[14],T[16],'bi',.8),(T[16],T[20]-2.4,'cang',.9),
    (T[20],T[24]-2.4,'mo',.8),(T[24],E[28],'loan',1.0),(T[29],E[30],'cang',.9),(T[31],V.TOTAL-.5,'trang',.9)]
for a,b,md,v in CH: music(M,a,b,md,v)
drop(M,.15,.8);wave_bed(M,0,E[3]+.5,.3);oars(M,.5,E[1],.2,1.1,.4)
for i in range(6): woodcrack(M,mid(2,.2)+i*.35,.1)
gong(M,mid(3,.3),.55)
for i in range(3): stamp(M,T[4]+.3+i*.7,.35)
hooves(M,T[5],4,.35);drum(M,mid(5,.45),.5)
t0=T[6]-3.6;whoosh(M,t0-.4,1.0,.4);gong(M,t0+.1,.55);stamp(M,t0+1.1,.6)
brush(M,T[6]+.2,1.5,.35)
stamp(M,T[7]+.2,.6);steps(M,T[7]+.2,mid(7,.5),.2,.5)
steps(M,T[8],T[8]+1.2,.3,.4);gong(M,mid(8,.55),.5)
march(M,T[9],E[9],.3);brush(M,T[10]+.3,2.5,.4)
for n in V.CARDS: whoosh(M,T[n]-2.6,1.0,.4);gong(M,T[n]-2.1,.45);brush(M,T[n]-2.2,.7,.35)
brush(M,mid(11,.5),1.0,.3)
horn(M,T[12]+.1,1.6,.5);hooves(M,T[12]+.6,4,.45);war_drums(M,T[12],E[13],.5,.45);shouts(M,mid(12,.3),3,.4);clangs(M,mid(12,.4),E[12],4,.3)
hooves(M,T[13],3,.4)
# mưa tên, va chạm, người ngựa ngã (khớp hình S_12, S_27, S_29)
volley(M,T[12]+.8,mid(12,.55)+1.0,9,.28);volley(M,T[12]+1.5,E[13]-.6,18,.3)
clangs(M,mid(12,.55),E[12]+.5,6,.3);shouts(M,mid(12,.55),3.5,.45)
for k,tt in enumerate([mid(12,.55)+.4+i*.25 for i in (2,4,5)]+[mid(12,.55)+.8+i*.1 for i in (1,6)]): thump(M,tt+.3,.5)
volley(M,T[27]+.8,mid(27,.6),6,.25);volley(M,mid(29,.5),E[29]+.3,14,.3)
for i in (0,2,4): thump(M,mid(27,.4)+i*.2+.3,.5)
for i in (2,5,7): thump(M,mid(29,.62)+i*.3+.3,.5)
brush(M,T[14]+.3,2.5,.35);oars(M,mid(14,.3),E[14],.2)
hooves(M,mid(15,.45),3.5,.4)
wave_bed(M,T[16],E[19]+.5,.3)
for i in range(6): woodcrack(M,mid(17,.45)+i*.35,.1)
gong(M,mid(18,.5),.6);drum(M,mid(19,.4),.5)
wave_bed(M,T[20],E[20]+.5,.3);oars(M,T[20],E[20],.25)
fire(M,T[21],E[22]-T[21],.25);murmur(M,T[22],E[22]-T[22],.12) if False else None
wave_bed(M,T[23],E[23],.2)
gong(M,T[24]+.2,.55);wave_bed(M,T[24],E[28]+.5,.35);oars(M,T[24],E[25],.35,.9,.4);war_drums(M,T[25],E[25],.3,.6)
brush(M,T[26]+.2,2.2,.35)
horn(M,T[27]+.1,1.5,.5);war_drums(M,T[27],E[27]+.3,.6,.4);volley(M,T[27]+.3,E[27],8,.3);shouts(M,T[27]+.3,3,.5);clangs(M,mid(27,.3),E[27],4,.3);hooves(M,T[28],3,.4)
gong(M,mid(28,.3),.5)
hooves(M,T[29],E[29]-T[29],.35);shouts(M,mid(29,.5),2.5,.4);clangs(M,mid(29,.55),E[29],3,.25)
gong(M,mid(30,.6),.5);hooves(M,T[30],3,.2)
stamp(M,mid(31,.5),.35)
shouts(M,T[32]+.2,2.0,.35);gong(M,T[32]+.4,.5)
brush(M,mid(33,.45),2,.35)
wave_bed(M,T[34],V.TOTAL-.5,.25);gong(M,mid(34,.5),.5)
# --- giọng gốc + trộn (giọng giữ nguyên mẫu, hiệu ứng nằm dưới)
def voice_mix(M,Ts,files,duck=.55):
    v=np.zeros(M.N,np.float32)
    for t0,f in zip(Ts,files):
        raw=subprocess.run(['ffmpeg','-v','error','-i',f,'-f','f32le','-ac','1','-ar',str(SR),'-'],capture_output=True).stdout
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
ns=sorted(V.TX);files=[f"{V.GD}/{V.NN[n]}.mp3" for n in ns]
v,d=voice_mix(M,[T[n] for n in ns],files)
write_mix(M,v,d,'/tmp/gen/bd/out/am_tm4.wav')
print('ok',round(V.TOTAL,1))
