# Âm thanh tm3: hiệu ứng + nhạc tự tổng hợp; giọng Charon gốc giữ nguyên (không cân giọng)
import subprocess,wave
from sfx import *
from sfx import _guard
import dai_tm3 as V
from amthanh_tm2 import hooves,fire,murmur
T,E,mid=V.T,V.E,V.mid
M=Mix(V.TOTAL,13)
wind(M,.2,V.TOTAL-.5,.12)
CH=[(0,T[6]-4,'cang',1.0),(T[6],T[11],'mo',.9),(T[11],T[12]-2.4,'cang',.8),(T[12],E[14],'loan',.9),(T[15],T[19]-2.4,'cang',.9),
    (T[19],T[20],'mo',.8),(T[20],E[23],'loan',1.0),(T[24],T[28]-2.4,'bi',.8),(T[28],T[30],'mo',.8),(T[30],E[31],'loan',1.0),(T[32],T[35]-2.4,'bi',.8),(T[35],V.TOTAL-.5,'trang',.9)]
for a,b,md,v in CH: music(M,a,b,md,v)
# hook
drop(M,.15,.8);wave_bed(M,0,E[4]+.5,.3)
for i in range(9): woodcrack(M,1.0+i*.45,.12)
steps(M,1.0,E[2],.3,.35);march(M,T[2],E[2],.25);brush(M,mid(2,.55),1.0,.3)
gong(M,T[3]+.2,.5);drum(M,T[4]+.2,.5);drum(M,mid(4,.45),.5)
t0=T[6]-3.6;whoosh(M,t0-.4,1.0,.4);gong(M,t0+.1,.55);stamp(M,t0+1.1,.6)
# chương 2
for k in range(3): brush(M,mid(6,.3)+k*.4,1.6,.3)
stamp(M,T[7]+.2,.6);war_drums(M,T[7]+.3,E[7],.3,.6);fire(M,mid(7,.75),2.0,.3)
gong(M,T[8]+.2,.45);stamp(M,mid(8,.4),.4);stamp(M,mid(8,.62),.4)
march(M,T[9],E[9],.3);steps(M,mid(9,.45),E[9],.2,.5)
wave_bed(M,T[10],E[10]+.5,.35);oars(M,T[10],E[10],.25,1.0,.4)
brush(M,T[11]+.2,2.0,.3);pluck(M,mid(11,.4),NT['A3'],.3,2.0)
for n in V.CARDS: whoosh(M,T[n]-2.6,1.0,.4);gong(M,T[n]-2.1,.45);brush(M,T[n]-2.2,.7,.35)
# chương 3
brush(M,T[12]+.4,2.0,.35)
wave_bed(M,T[13],E[14],.35);horn(M,T[13]+.1,1.6,.45);war_drums(M,T[13],E[13]+.3,.5,.45);volley(M,T[13]+.4,E[13],8,.3);oars(M,T[13],E[13],.25)
gong(M,T[14]+.6,.45);march(M,mid(14,.5),E[14],.3)
stamp(M,T[15]+.2,.55);brush(M,T[15]+.4,2.6,.4);march(M,T[15],E[15],.25)
brush(M,mid(16,.4),1.0,.3)
for i in range(6): steps(M,mid(17,.5)+i*.08,mid(17,.5)+i*.08+.4,.15,.4)
wave_bed(M,T[18],E[18]+.5,.3);drum(M,mid(18,.55),.6)
# chương 4
fire(M,T[19],E[19]-T[19],.2)
t=mid(19,.4)
while t<E[19]: drop(M,t,.16);t+=.5
for i in range(12): woodcrack(M,T[20]+.4+i*.2,.18)
wave_bed(M,T[20],E[24]+.5,.35)
steps(M,T[21],E[21],.4,.35);horn(M,T[21]+.2,1.5,.4);clangs(M,mid(21,.3),E[21],2,.25)
shouts(M,T[22]+.1,3.0,.5);war_drums(M,T[22],E[22]+.3,.6,.4);clangs(M,T[22]+.3,E[22],4,.35);thump(M,mid(22,.5),.6)
volley(M,T[23]+.3,mid(23,.6),6,.3);oars(M,T[23],E[23],.25);gong(M,mid(23,.6),.5)
# đêm ở đền
pad(M,T[25],E[27],[NT['D2'],NT['A2']],.12)
for i in range(4): pluck(M,T[26]+i*(E[26]-T[26])/4.2,NT[['D4','F4','G4','A4'][i]],.25,2.2)
gong(M,T[27]+.1,.5)
# chương 5
fire(M,T[28],E[29]-T[28],.25);murmur(M,T[29],E[29]-T[29],.12)
oars(M,T[30]+.2,E[30],.3,.9,.4);fire(M,T[30],E[31]-T[30],.2)
shouts(M,T[31]+.1,3.5,.55);war_drums(M,T[31],E[31]+.4,.6,.35);clangs(M,T[31]+.3,E[31],5,.35);fire(M,mid(31,.3),3.0,.4)
gong(M,mid(31,.6),.6)
stamp(M,mid(32,.35),.35);stamp(M,mid(32,.35)+.4,.35)
drum(M,mid(34,.35),.6)
# chương 6
oars(M,T[35],E[35],.25,1.0,.4);wave_bed(M,T[35],E[35]+.5,.3)
brush(M,T[36]+.2,2.5,.35);march(M,T[36],E[36],.2)
pluck(M,T[37]+.2,NT['A3'],.3,2.0);gong(M,T[38]+.2,.4)
murmur(M,T[39],E[39]-T[39],.15)
pluck(M,mid(40,.5),NT['D5'],.3,1.8)
wave_bed(M,T[41],V.TOTAL-.5,.25);gong(M,mid(41,.5),.5)
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
write_mix(M,v,d,'/tmp/gen/bd/out/am_tm3.wav')
print('ok',round(V.TOTAL,1))
