import numpy as np
from PIL import Image
from canh import *
from engine import *
from khung_dung import cam,PAP
cv=PAP.copy();c=cam(960,540,1.0)
put(cv,c,'t17_far',960,760,ay=1,k=1,o=.9);put(cv,c,'t17_mid',960,900,ay=1,o=.85)
put(cv,c,'t17x_dong',960,600,s=1.05)
for i,(x,y,s) in enumerate([(520,640,1.4),(1250,600,1.3),(900,700,1.6)]): put(cv,c,'t17_spr_doc',x,y,s=s,o=.75)
put(cv,c,'t17_spr_lb',965,900,s=.8,ay=1,o=.8)
put(cv,c,'t17_frontL',-120,1120,ax=0,ay=1,s=.85);put(cv,c,'t17_frontR',2040,1120,ax=1,ay=1,s=.8)
put_screen(cv,band(1400,220,PAPER,.8,50),960,215)
put_screen(cv,text('CÁI CHẾT BÍ ẨN',130,RED,700,glow=8),960,200)
put_screen(cv,text('Lý Nam Đế · nước Vạn Xuân',46,INK,700),960,300)
lg=np.asarray(Image.open(D+'nguoi-gac-su.png').convert('RGBA').resize((130,130),Image.LANCZOS),np.float32)/255;lg[...,:3]*=lg[...,3:4]
blend(cv,lg,1920-44-130,34,.8)
im=Image.fromarray((np.clip(cv,0,1)*255+.5).astype(np.uint8));im.save('bia17/bia_tm17.png');im.convert('RGB').save('bia17/bia_tm17_youtube.jpg',quality=90);print('ok')
