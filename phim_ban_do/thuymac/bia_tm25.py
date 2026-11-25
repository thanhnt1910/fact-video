# Bìa tm25: hai lính nhà Nguyên khiêng ống đồng chạy trốn, phía sau quân nhà Trần đuổi, cờ Nguyên đổ; chữ lớn "TRỐN TRONG ỐNG ĐỒNG";
# logo 130 px, độ đậm .8, cách phải 44, trên 34
import numpy as np,math
from PIL import Image
from canh import *
from engine import *
from khung_dung import cam,PAP
import rig
for _k in ['m5','m6','lq','v4','v5','qk']: rig.PRE[_k]='t25n_r_'
cv=PAP.copy();c=cam(960,540,1.0)
put(cv,c,'t25_far',960,800,ay=1,k=1,o=.9);put(cv,c,'t25_mid',960,940,ay=1,o=.75)
put(cv,c,'t25_spr_coN',300,1000,ay=1,s=.8,r=-70)
for j,dx in enumerate((-300,300)):
    P=rig.hoang(1.2+j,.3,1.0);P['arF']=-160;P['faF']=0;P['arB']=-150;P['faB']=0
    rig.ve23(cv,c,['m5','m6'][j],1250+dx,1010,.95,P)
put(cv,c,'t25n_ongdong',1250,1010-200,s=.72,r=-1)
P=rig.hoang(.4,.2,1.1);rig.ve23(cv,c,'lq',1650,1010,.9,P,vk='daocong')
for i,k in enumerate(['v4','qk','v5']): rig.ve23(cv,c,k,180+i*230,1010,.8,rig.xung(i*1.3),vk=['giao','dao','giao'][i])
put(cv,c,'t25_frontL',-120,1120,ax=0,ay=1,s=.85);put(cv,c,'t25_frontR',2040,1120,ax=1,ay=1,s=.8)
put_screen(cv,band(1180,200,PAPER,.82,50),900,190)
put_screen(cv,text('TRỐN TRONG ỐNG ĐỒNG',104,RED,700,glow=8),900,180)
put_screen(cv,text('Thoát Hoan · năm 1285',44,INK,700),900,275)
lg=np.asarray(Image.open(D+'nguoi-gac-su.png').convert('RGBA').resize((130,130),Image.LANCZOS),np.float32)/255;lg[...,:3]*=lg[...,3:4]
blend(cv,lg,1920-44-130,34,.8)
im=Image.fromarray((np.clip(cv,0,1)*255+.5).astype(np.uint8))
import os;os.makedirs('bia25',exist_ok=True)
im.save('bia25/bia_tm25.png');im.convert('RGB').save('bia25/bia_tm25_youtube.jpg',quality=90);print('ok')
