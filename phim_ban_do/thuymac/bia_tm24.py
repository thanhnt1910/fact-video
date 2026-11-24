# Bìa tm24: Đỗ Khắc Chung giơ cánh tay trước Ô Mã Nhi, cận cánh tay có hai chữ Sát Thát (hình ảnh lặp lại); chữ lớn "VÌ SAO VẪN XĂM?";
# logo 130 px, độ đậm .8, cách phải 44, trên 34
import numpy as np,math
from PIL import Image
from canh import *
from engine import *
from khung_dung import cam,PAP
import rig
for _k in ['dkc','omn','m1','m2']: rig.PRE[_k]='t24n_r_'
cv=PAP.copy();c=cam(960,540,1.0)
put(cv,c,'t24_far',960,800,ay=1,k=1,o=.9);put(cv,c,'t24_mid',960,940,ay=1,o=.75)
put(cv,c,'t24n_trai',1250,900,ay=1,s=.6,o=.85)
put(cv,c,'t24_spr_colon',1820,1000,ay=1,s=.75)
rig.ve23(cv,c,'omn',1500,1000,.95,rig.dung(.2),flip=True,vk='daocong')
rig.ve23(cv,c,'m2',1700,1000,.85,rig.dung(.9),flip=True,vk='moc')
P=rig.dung(.4);P.update(arF=-150,faF=-10)
rig.ve23(cv,c,'dkc',1150,1000,1.0,P)
put(cv,c,'t24_frontL',-120,1120,ax=0,ay=1,s=.85);put(cv,c,'t24_frontR',2040,1120,ax=1,ay=1,s=.8)
put(cv,None,'t24n_canhtay',560,560,s=.55,screen=True)
put_screen(cv,band(1000,200,PAPER,.82,50),640,190)
put_screen(cv,text('VÌ SAO VẪN XĂM?',112,RED,700,glow=8),640,180)
put_screen(cv,text('Đỗ Khắc Chung · năm 1285',44,INK,700),640,275)
lg=np.asarray(Image.open(D+'nguoi-gac-su.png').convert('RGBA').resize((130,130),Image.LANCZOS),np.float32)/255;lg[...,:3]*=lg[...,3:4]
blend(cv,lg,1920-44-130,34,.8)
im=Image.fromarray((np.clip(cv,0,1)*255+.5).astype(np.uint8))
import os;os.makedirs('bia24',exist_ok=True)
im.save('bia24/bia_tm24.png');im.convert('RGB').save('bia24/bia_tm24_youtube.jpg',quality=90);print('ok')
