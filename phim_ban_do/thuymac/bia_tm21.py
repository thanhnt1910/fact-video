# Bìa tm21: Khúc Thừa Mỹ cầm chiếc tiết (hình ảnh lặp lại) bên trái, vua Nam Hán Lưu Nham chỉ tay giận dữ bên phải trước cổng Quảng Châu;
# tô màu nước như bản dựng; chữ lớn ở trên không đè người; logo 130 px, độ đậm .8, cách phải 44, trên 34
import numpy as np,os
from PIL import Image
from canh import *
from engine import *
from khung_dung import cam,PAP
import mau21
cv=PAP.copy();c=cam(960,540,1.0)
put(cv,c,'t21_far',960,800,ay=1,k=1,o=.9);put(cv,c,'t21_mid',960,940,ay=1,o=.75)
put(cv,c,'t21_cong',1620,1010,ay=1,s=.9)
mau21.to_mau(cv)
put(cv,c,'t21n_thuamy',470,1030,s=1.3,ay=1,scale_px=3)
put(cv,c,Af('t21n_luunham'),1020,1030,s=1.25,ay=1,scale_px=3)
mau21.bui(cv,3.0)
put(cv,c,'t21_frontL',-120,1120,ax=0,ay=1,s=.85);put(cv,c,'t21_frontR',2040,1120,ax=1,ay=1,s=.8)
put_screen(cv,band(1220,210,PAPER,.86,50),900,190)
put_screen(cv,text('XIN CỜ NƠI XA',118,RED,700,glow=8),900,175)
put_screen(cv,text('Ba đời họ Khúc · năm 905–930',46,INK,700),900,272)
lg=np.asarray(Image.open(D+'nguoi-gac-su.png').convert('RGBA').resize((130,130),Image.LANCZOS),np.float32)/255;lg[...,:3]*=lg[...,3:4]
blend(cv,lg,1920-44-130,34,.8)
os.makedirs('/tmp/pc/assets/bia/TM21',exist_ok=True)
im=Image.fromarray((np.clip(cv,0,1)*255+.5).astype(np.uint8))
im.save('/tmp/pc/assets/bia/TM21/bia_tm21.png');im.convert('RGB').save('/tmp/pc/assets/bia/TM21/bia_tm21_youtube.jpg',quality=90);print('ok')
