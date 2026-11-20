# Bìa tm13 bản 5: con ngựa đồng đúc từ trống đồng; chữ lớn 4 chữ; logo 130 px, độ đậm .8, cách phải 44, trên 34
import numpy as np
from PIL import Image
from canh import *
from engine import *
from khung_dung import cam,PAP
cv=PAP.copy();c=cam(960,540,1.0)
put(cv,c,'t13_far',960,760,ay=1,k=1,o=.9);put(cv,c,'t13_mid',960,900,ay=1,o=.8)
put(cv,c,'t13x_ngua',1150,640,s=1.25)
put(cv,c,'t13_spr_matrong',380,640,s=.75,o=.95)
put(cv,c,'t13_frontL',-120,1120,ax=0,ay=1,s=.85);put(cv,c,'t13_frontR',2040,1120,ax=1,ay=1,s=.8)
put_screen(cv,band(1500,210,PAPER,.82,50),960,200)
put_screen(cv,text('TRỐNG HÓA THÀNH NGỰA',118,RED,700,glow=8),960,190)
put_screen(cv,text('Hai Bà Trưng · Mã Viện',46,INK,700),960,290)
lg=np.asarray(Image.open(D+'nguoi-gac-su.png').convert('RGBA').resize((130,130),Image.LANCZOS),np.float32)/255;lg[...,:3]*=lg[...,3:4]
blend(cv,lg,1920-44-130,34,.8)
im=Image.fromarray((np.clip(cv,0,1)*255+.5).astype(np.uint8));im.save('bia13/bia_tm13.png');im.convert('RGB').save('bia13/bia_tm13_youtube.jpg',quality=90);print('ok')
