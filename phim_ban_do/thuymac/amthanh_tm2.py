# Âm thanh tm2: hiệu ứng + nhạc tự tổng hợp; giọng Charon gốc giữ nguyên (không cân giọng)
import subprocess,wave
from sfx import *
from sfx import _guard
import dai_tm2 as V
T,E,mid=V.T,V.E,V.mid
M=Mix(V.TOTAL,11)
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
def murmur(m,t0,dur,g=.2): shouts(m,t0,dur,g)
# âm nền: gió nhẹ suốt video
wind(M,.2,V.TOTAL-.5,.12)
# nhạc theo chương
CH=[(0,T[5]-4,'cang',1.0),(T[5],T[15],'mo',.9),(T[15],T[16]-2.4,'cang',.8),(T[16],T[19],'binh',.9),(T[19],T[21],'trang',.9),(T[21],T[25]-2.4,'cang',.8),
    (T[25],T[28],'cang',.9),(T[28],E[29],'loan',1.0),(T[30],T[33]-2.4,'mo',.8),(T[33],T[35],'cang',.9),(T[36],E[39],'loan',1.0),(T[40],T[44]-2.4,'bi',.8),(T[44],V.TOTAL-.5,'trang',.9)]
for a,b,md,v in CH: music(M,a,b,md,v)
# --- chương 1
drop(M,.15,.8);creak(M,.9,2.0,.35);creak(M,T[2]+.2,2.6,.45);thump(M,mid(2,.72),.8);gong(M,mid(2,.75),.45)
stamp(M,T[3]+.3,.5);stamp(M,mid(3,.45),.5);thump(M,mid(3,.8),.6)
for i in range(3): woodcrack(M,mid(4,.62)+i*.35,.25)
t0=T[5]-3.6;whoosh(M,t0-.4,1.0,.4);gong(M,t0+.1,.55);stamp(M,t0+1.1,.6)
# --- chương 2
stamp(M,T[5]+.2,.6);clang(M,mid(5,.45),.4);thump(M,mid(5,.85),.5)
steps(M,mid(6,.72),E[6],.18,.5)
war_drums(M,mid(7,.3),E[7],.25,.8);wave_bed(M,mid(7,.45),E[7]+.5,.3);oars(M,mid(7,.5),E[7],.25,1.0,.5)
brush(M,T[8]+.8,1.6,.35)
brush(M,T[9]+.1,1.0,.3);stamp(M,T[9]+.2,.6);stamp(M,mid(9,.4),.45);whoosh(M,mid(9,.78),1.2,.4)
steps(M,T[10]+.3,T[10]+1.8,.2,.45)
creak(M,T[11]+.3,2.0,.4)
gong(M,T[12]+.3,.45);war_drums(M,mid(12,.5),E[12]+.5,.25,.7)
for k in range(4): brush(M,T[13]+.3+k*.6,.8,.3,pan=k*.2-.3)
march(M,T[13]+.5,E[13],.25)
t=T[14]
while t<E[14]: drop(M,t,.25);t+=.62
pluck(M,mid(15,.55),NT['A3'],.3,2.0)
# --- chương 3
for n in V.CARDS: whoosh(M,T[n]-2.6,1.0,.4);gong(M,T[n]-2.1,.45);brush(M,T[n]-2.2,.7,.35)
stamp(M,mid(16,.55),.4)
steps(M,mid(17,.28),E[17],.35,.42);clangs(M,mid(17,.3),E[17],2,.18)
murmur(M,T[18]+.3,E[18]-T[18],.15)
shouts(M,T[19]+.1,2.6,.45);gong(M,mid(19,.35),.6);creak(M,mid(19,.6),1.5,.35)
whoosh(M,T[20]+.2,1.0,.3);stamp(M,mid(20,.55),.35)
whoosh(M,T[21],1.2,.35);brush(M,mid(21,.28),1.0,.3);thump(M,mid(21,.5),.5)
steps(M,T[22],E[22],.22,.5)
stamp(M,mid(23,.3)+.9,.45);stamp(M,mid(23,.62)+.9,.45)
fire(M,T[24]+.4,2.4,.3);thump(M,mid(24,.5)+.5,.8);war_drums(M,mid(24,.55),E[24]+1,.3,.55)
# --- chương 4
stamp(M,T[25]+.2,.6);brush(M,mid(25,.3),2.0,.35);brush(M,mid(25,.55),2.0,.35,.4);march(M,mid(25,.3),E[25],.2);oars(M,mid(25,.55),E[25],.22)
wave_bed(M,T[26],E[29]+.5,.35);oars(M,T[26],mid(26,.42),.3)
sw=mid(26,.42)
for i in range(18): stake_hit(M,sw+.6+i*.12+.4,.35)
stamp(M,T[27]+.3,.5);tide(M,mid(27,.3),2.0,.3,False);woodcrack(M,mid(27,.5),.3)
horn(M,T[28]+.1,1.8,.5);war_drums(M,T[28],E[28]+.4,.6,.45);volley(M,T[28]+.4,E[28],8,.3);clangs(M,mid(28,.3),E[28],3,.3);shouts(M,mid(28,.2),3.5,.35)
creak(M,mid(28,.7),1.6,.3)
for k in range(4): woodcrack(M,T[29]+.6+k*.5,.45,pan=k*.2-.3)
tide(M,T[29],2.5,.35,False);gong(M,mid(29,.6),.5)
fire(M,T[30],E[31]-T[30],.2)
for k in range(3):
    st=T[31]+.2+k*(E[31]-T[31])/3.4;hooves(M,st,1.5,.35)
t=T[31]+.5
while t<E[31]: drop(M,t,.18);t+=.4+.6*(t-T[31])/(E[31]-T[31]+1e-6)
drum(M,mid(32,.45),.6)
# --- chương 5
brush(M,T[33]+.4,1.8,.4);march(M,T[33],E[33],.3)
march(M,T[34],E[34],.25);hooves(M,T[34]+.3,4,.25)
pad(M,T[35],E[35],[NT['D2']],.12)
horn(M,mid(36,.05),1.8,.6);shouts(M,mid(36,.1),3.0,.55);clangs(M,mid(36,.15),mid(36,.7),5,.35);war_drums(M,mid(36,.05),mid(36,.7),.6,.35);thump(M,mid(36,.62),.9)
volley(M,mid(36,.1),mid(36,.75),14,.3)
gong(M,mid(37,.5),.7)
brush(M,mid(38,.35),2.0,.4)
hooves(M,T[39],E[39]-T[39],.35);shouts(M,mid(39,.2),3.0,.35);war_drums(M,T[39],E[39],.5,.4)
steps(M,T[40],E[40],.25,.5)
gong(M,T[41]+.1,.4);brush(M,mid(41,.3),.6,.35)
for i in range(2):
    st=T[42]+i*(E[42]-T[42])*.5;stamp(M,st+.7,.45);thump(M,st+1.4,.35)
murmur(M,T[43],E[43]-T[43],.2);drum(M,mid(43,.55),.5)
# --- chương 6
steps(M,T[44],E[44],.2,.55);pluck(M,mid(44,.6),NT['D5'],.25,1.5)
pluck(M,mid(45,.62),NT['A4'],.3,2.5)
for i,f in enumerate(['D4','G4','D5']): pluck(M,mid(46,.05+.3*i),NT[f],.35,1.8)
gong(M,mid(47,.5),.5)
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
write_mix(M,v,d,'/tmp/gen/bd/out/am_tm2.wav')
print('ok',round(V.TOTAL,1))
