# Âm thanh tm8 (khớp cảnh dai_tm8.py)
from amchung import *
from sfx import _guard
import dai_tm8 as D
V=D.V;T,E,mid=V.T,V.E,V.mid
M=Mix(V.TOTAL,28)
wind(M,.2,V.TOTAL-.5,.12)
CH=[(0,T[5]-4,'cang',1.0),(T[5],T[9]-2.4,'mo',.9),(T[9],E[11],'cang',.9),(T[12],E[13],'bi',.7),(T[14],E[16],'loan',1.0),(T[17],E[18],'cang',.8),
    (T[19],E[21],'loan',1.0),(T[22],E[24],'cang',.8),(T[25],V.TOTAL-.5,'trang',.9)]
for a,b,md,v in CH: music(M,a,b,md,v)
drop(M,.15,.8);march(M,.5,E[1],.25)
hooves(M,T[2]+.2,2,.3);march(M,T[2],E[2],.25)
hooves(M,T[3],E[3]-T[3]-1,.3);gong(M,mid(3,.7),.5)
brush(M,mid(4,.6),1,.3);stamp(M,mid(4,.8),.45)
t0=T[5]-3.6;whoosh(M,t0-.4,1.0,.4);gong(M,t0+.1,.55);stamp(M,t0+1.1,.6)
stamp(M,T[5]+.2,.5);brush(M,T[6]+.3,2,.35);stamp(M,T[6]+.3,.4)
for n in D.CARDS: whoosh(M,T[n]-2.6,1.0,.4);gong(M,T[n]-2.1,.45);brush(M,T[n]-2.2,.7,.35)
drum(M,mid(7,.5),.5)
battle(M,T[9]+.5,E[9],.6,6);march(M,T[10],E[10],.35)
gong(M,mid(11,.3),.4)
hooves(M,T[13],E[13]-T[13],.35)
horn(M,T[14]+.2,1.4,.5);battle(M,T[14]+.3,E[14]+.4,1.2,20);thump(M,mid(14,.5)+.3,.6)
for i in range(9):
    if i%3!=1: thump(M,T[14]+.8+i*.25+.3,.35)
stamp(M,T[15]+.6,.6)
battle(M,T[16]+.3,E[16],.7,10)
march(M,T[17],E[17],.3);war_drums(M,mid(18,.5),E[18],.3,.8)
horn(M,T[19]+.2,1.4,.5);battle(M,T[19]+.3,E[19],1.2,18);woodcrack(M,T[19]+.6,.5)
steps(M,T[20],E[20],.2,.6);gong(M,T[21]+.2,.5)
hooves(M,mid(22,.4),2.5,.3);stamp(M,T[23]+.2,.6);hooves(M,mid(23,.4),E[23]-mid(23,.4),.4)
wave_bed(M,T[24],E[24],.25);oars(M,T[24],E[24],.2)
gong(M,mid(25,.5),.5)
finish(M,V,'/tmp/gen/bd/out/am_tm8.wav')
