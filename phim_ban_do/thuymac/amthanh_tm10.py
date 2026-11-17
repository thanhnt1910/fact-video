# Âm thanh tm10 (khớp cảnh dai_tm10.py)
from amchung import *
from sfx import _guard
import dai_tm10 as D
V=D.V;T,E,mid=V.T,V.E,V.mid
M=Mix(V.TOTAL,30)
wind(M,.2,V.TOTAL-.5,.12)
CH=[(0,T[5]-4,'cang',1.0),(T[5],T[8]-2.4,'mo',.9),(T[8],E[10],'bi',.8),(T[11],E[13],'cang',1.0),(T[14],E[17],'cang',.9),
    (T[18],E[21],'loan',1.0),(T[22],E[23],'bi',.8),(T[24],V.TOTAL-.5,'trang',.9)]
for a,b,md,v in CH: music(M,a,b,md,v)
drop(M,.15,.8);murm=_guard(lambda m,t0,d,g=.1: m.add((lp(m.nz(int(d*SR)),600)*.3).astype(np.float32),t0,g));murm(M,.3,E[1],.15)
brush(M,mid(2,.5),1.2,.3);march(M,T[3],E[3],.3)
brush(M,mid(4,.55),1,.3);brush(M,mid(4,.8),1,.3)
t0=T[5]-3.6;whoosh(M,t0-.4,1.0,.4);gong(M,t0+.1,.55);stamp(M,t0+1.1,.6)
steps(M,T[5],E[5],.25,.5);stamp(M,T[6]+.3,.4);brush(M,mid(6,.4),2,.35)
march(M,T[7],E[7],.3)
for n in D.CARDS: whoosh(M,T[n]-2.6,1.0,.4);gong(M,T[n]-2.1,.45);brush(M,T[n]-2.2,.7,.35)
stamp(M,mid(8,.55)+.5,.6);gong(M,mid(9,.4),.35)
gong(M,mid(11,.45),.6);drum(M,mid(11,.5),.5)
murm(M,T[12],E[12]-T[12],.2);drum(M,mid(12,.65),.6)
wave_bed(M,T[13],E[13],.3);oars(M,T[13],E[13],.3,.8)
march(M,T[14],E[14],.25);shouts(M,mid(14,.6),2.5,.5);drum(M,mid(14,.6),.6)
cannon(M,T[16]+.5,.4);march(M,T[17],E[17],.35)
for k in range(8): cannon(M,T[18]+.4+k*.5,.4)
volley(M,T[18]+.3,T[19],14,.3)
horn(M,T[19],1.5,.5);battle(M,T[19]+.1,E[19],1.3,10)
for i in range(8):
    if i%2==0: thump(M,mid(19,.4)+i*.2+.3,.4)
battle(M,T[20]+.3,E[20],.8,6);thump(M,E[20]-.2,.5)
hooves(M,mid(21,.4),E[21]-mid(21,.4),.45)
woodcrack(M,mid(22,.45),.6);creak(M,mid(22,.4),1.4,.4)
for k in range(5): splash(M,mid(22,.5)+k*.25,.45)
gong(M,mid(23,.5),.4)
war_drums(M,T[24],E[24],.3,.6);gong(M,mid(24,.5),.5)
finish(M,V,'/tmp/gen/bd/out/am_tm10.wav')
