# Âm thanh tm9 (khớp cảnh dai_tm9.py)
from amchung import *
from sfx import _guard
import dai_tm9 as D
V=D.V;T,E,mid=V.T,V.E,V.mid
M=Mix(V.TOTAL,29)
wind(M,.2,V.TOTAL-.5,.12)
CH=[(0,T[5]-4,'cang',1.0),(T[5],T[9]-2.4,'mo',.9),(T[9],E[12],'cang',.9),(T[13],E[16],'cang',.9),(T[17],E[18],'bi',.7),
    (T[19],E[21],'loan',1.0),(T[22],E[23],'bi',.8),(T[24],V.TOTAL-.5,'trang',.9)]
for a,b,md,v in CH: music(M,a,b,md,v)
drop(M,.15,.8);brush(M,mid(2,.4),1.2,.3)
wave_bed(M,T[3],E[3],.3);woodcrack(M,mid(3,.4),.4)
brush(M,mid(4,.55),1,.3);brush(M,mid(4,.8),1,.3)
t0=T[5]-3.6;whoosh(M,t0-.4,1.0,.4);gong(M,t0+.1,.55);stamp(M,t0+1.1,.6)
march(M,T[5],E[5],.3);wave_bed(M,T[6],E[6],.3);oars(M,T[6],E[6],.2)
stamp(M,T[7]+.5,.5);gong(M,mid(7,.35),.4)
wave_bed(M,T[8],E[8],.3);oars(M,T[8],E[8],.35,.8);war_drums(M,T[8],E[8],.25,.8)
for k in range(4): drum(M,T[9]+.4+k*(E[9]-T[9]-.8)/4,.4)
for n in D.CARDS: whoosh(M,T[n]-2.6,1.0,.4);gong(M,T[n]-2.1,.45);brush(M,T[n]-2.2,.7,.35)
oars(M,T[10],E[10],.3,.9)
fire=_guard(lambda m,t0,d,g=.2: m.add((lp(m.nz(int(d*SR)),2500)*.2).astype(np.float32),t0,g))
fire(M,T[11],E[11]-T[11],.25);gong(M,T[12]+.2,.45)
march(M,T[13],E[13],.3)
brush(M,T[14]+.3,1.5,.3);brush(M,T[15]+.3,1.5,.3);stamp(M,T[16]+.3,.3);stamp(M,mid(16,.6),.45)
wave_bed(M,T[17],E[18],.3);oars(M,T[17],E[18],.25,1.0)
horn(M,T[19]+.1,1.4,.5);battle(M,T[19]+.2,E[20],1.2,14)
for k in range(6): cannon(M,T[19]+.5+k*.25,.5)
for k in range(5): splash(M,T[19]+.8+k*.3,.4);woodcrack(M,T[20]+.3+k*.4,.35)
steps(M,T[21],E[21],.3,.4)
wave_bed(M,T[22],E[22],.25);oars(M,T[22],E[22],.2);gong(M,T[23]+.3,.4)
wave_bed(M,T[24],V.TOTAL-.5,.2);gong(M,mid(24,.5),.5)
finish(M,V,'/tmp/gen/bd/out/am_tm9.wav')
