# Bìa tm19: Phùng Hưng giơ gươm trước phủ thành, tấm biển gỗ "BỐ CÁI" (hình ảnh lặp lại của video); chữ lớn 4 chữ;
# logo 130 px, độ đậm .8, cách phải 44, trên 34
import numpy as np
from PIL import Image
from canh import *
from engine import *
from khung_dung import cam,PAP
cv=PAP.copy();c=cam(960,540,1.0)
put(cv,c,'t19_far',960,800,ay=1,k=1,o=.9);put(cv,c,'t19_mid',960,940,ay=1,o=.75)
put(cv,c,'t19x_vaophu',1180,640,s=1.05)
put(cv,c,'t19n_ph2',560,1010,s=1.25,ay=1,scale_px=3)
for x in (860,980,1100): put(cv,c,'t19n_ta',x+380,1000,s=.75,ay=1,scale_px=3)
put(cv,c,'t19_frontL',-120,1120,ax=0,ay=1,s=.85);put(cv,c,'t19_frontR',2040,1120,ax=1,ay=1,s=.8)
put_screen(cv,band(1200,200,PAPER,.82,50),860,190)
put_screen(cv,text('VUA HAY CHA MẸ?',118,RED,700,glow=8),860,180)
put_screen(cv,text('Phùng Hưng · năm 791',44,INK,700),860,275)
put(cv,None,'t19_bien',1480,470,s=.62,screen=True)
put_screen(cv,text('BỐ CÁI',60,(.79,.64,.35),700),1480,465)
lg=np.asarray(Image.open(D+'nguoi-gac-su.png').convert('RGBA').resize((130,130),Image.LANCZOS),np.float32)/255;lg[...,:3]*=lg[...,3:4]
blend(cv,lg,1920-44-130,34,.8)
im=Image.fromarray((np.clip(cv,0,1)*255+.5).astype(np.uint8))
im.save('bia19/bia_tm19.png');im.convert('RGB').save('bia19/bia_tm19_youtube.jpg',quality=90);print('ok')
