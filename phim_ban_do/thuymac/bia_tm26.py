# Bìa tm26: đoàn thuyền lương nhà Nguyên giữa biển đảo, quân nhà Nguyên hoảng sợ đổ gạo xuống biển, thuyền nhỏ Đại Việt lao tới;
# chữ lớn "AI CHẶN THUYỀN LƯƠNG?"; logo 130 px, độ đậm .8, cách phải 44, trên 34
import numpy as np,math
from PIL import Image
from canh import *
from engine import *
from khung_dung import cam,PAP
import rig
for _k in ['tvh','m7','m8','m9','v8','v6','tkd']: rig.PRE[_k]='t26n_r_'
cv=PAP.copy();c=cam(960,540,1.0)
put(cv,c,'t26_bien',960,760,ay=1,k=1,o=.95);put(cv,c,'t26_song',960,640,ay=0,s=1.0,o=.95)
def thuyen(x,y,s,lon,flip,ngoi):
    f=-1 if flip else 1
    for key,dx,P in ngoi: rig.ve23(cv,c,key,0,0,s,P,flip=flip,hip=(x+f*dx*s,y-46*s))
    nm='t23n_thuyenlon' if lon else 't23n_thuyen'
    put(cv,c,Af(nm) if flip else nm,x,y,s=s,ay=.8,scale_px=3)
def ngoi(**k):
    P=rig.ngoi(0);P.update(thF=-80,thB=-76,knF=84,knB=82);P.update(k);return P
so=dict(arF=-120,faF=-70,arB=-100,faB=-80,lean=-10,mat='S')
thuyen(1250,860,1.0,True,True,[('tvh',170,ngoi(**so)),('m8',-170,ngoi(**so))])
put(cv,c,'t26n_bao',1290,820,s=.6,ay=1)
for k,(x,y,r) in enumerate([(960,700,40),(880,800,120),(1010,880,200)]): put(cv,c,'t26n_gao',x,y,s=.42,r=r)
put_screen(cv,band(260,40,INK,.35,8),930,990)
for i,(x,y) in enumerate([(260,960),(560,1010)]):
    thuyen(x,y,.75,False,False,[('v8',-40,ngoi(arF=-75,faF=-20,lean=12,mat='G')),('v6',50,ngoi(arF=-80,faF=-10,lean=10,mat='G'))])
put(cv,c,'t26_dao',960,1100,ay=1,s=1.0,o=.9)
put_screen(cv,band(1220,210,PAPER,.84,50),880,190)
put_screen(cv,text('AI CHẶN THUYỀN LƯƠNG?',100,RED,700,glow=8),880,180)
put_screen(cv,text('Vân Đồn · cuối năm 1287',44,INK,700),880,278)
lg=np.asarray(Image.open(D+'nguoi-gac-su.png').convert('RGBA').resize((130,130),Image.LANCZOS),np.float32)/255;lg[...,:3]*=lg[...,3:4]
blend(cv,lg,1920-44-130,34,.8)
im=Image.fromarray((np.clip(cv,0,1)*255+.5).astype(np.uint8))
import os;os.makedirs('bia26',exist_ok=True)
im.save('bia26/bia_tm26.png');im.convert('RGB').save('bia26/bia_tm26_youtube.jpg',quality=90);print('ok')
