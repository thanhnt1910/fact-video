# Bìa tm20: Dương Thanh giơ đao trước con đường đêm, hàng quân quay đầu về phủ thành; ngọn giáo quay đầu (hình ảnh lặp lại);
# chữ lớn 4 chữ; logo 130 px, độ đậm .8, cách phải 44, trên 34
import numpy as np,os
from PIL import Image
from canh import *
from engine import *
from khung_dung import cam,PAP
cv=PAP.copy();c=cam(960,540,1.0)
put(cv,c,'t20_far',960,800,ay=1,k=1,o=.9);put(cv,c,'t20_mid',960,940,ay=1,o=.75)
put(cv,c,'t20x_demhanh',1100,620,s=1.05)
for x in (900,1060,1220): put(cv,c,Af('t20n_ta'),x+300,1010,s=.75,ay=1,scale_px=3)
put(cv,c,Af('t20n_thanh2'),600,1020,s=1.3,ay=1,scale_px=3)
put(cv,c,'t20_frontL',-120,1120,ax=0,ay=1,s=.85);put(cv,c,'t20_frontR',2040,1120,ax=1,ay=1,s=.8)
ink_wash(cv,.28,col=np.array((.1,.1,.18),np.float32))
put_screen(cv,band(1280,210,PAPER,.84,50),900,190)
put_screen(cv,text('QUAY QUÂN GIỮA ĐÊM',112,RED,700,glow=8),900,175)
put_screen(cv,text('Dương Thanh · năm 819',46,INK,700),900,270)
put(cv,None,'t20_giao',1620,520,s=.55,r=180,screen=True)
lg=np.asarray(Image.open(D+'nguoi-gac-su.png').convert('RGBA').resize((130,130),Image.LANCZOS),np.float32)/255;lg[...,:3]*=lg[...,3:4]
blend(cv,lg,1920-44-130,34,.8)
os.makedirs('bia20',exist_ok=True)
im=Image.fromarray((np.clip(cv,0,1)*255+.5).astype(np.uint8))
im.save('bia20/bia_tm20.png');im.convert('RGB').save('bia20/bia_tm20_youtube.jpg',quality=90);print('ok')
