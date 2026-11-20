# Bìa tm16 bản 2: voi và áo vàng, chữ lớn "CÂU NÓI KHÔNG CÓ THẬT?"; logo 130 px, độ đậm .8, cách phải 44, trên 34
import numpy as np
from PIL import Image
from canh import *
from engine import *
from khung_dung import cam,PAP
cv=PAP.copy();c=cam(960,540,1.0)
put(cv,c,'t16_voi1',960,640,s=1.35)
put(cv,c,'t16_spr_voi',1000,660,s=1.7)
put_screen(cv,band(1300,210,PAPER,.82,50),900,200)
put_screen(cv,text('KHÔNG CÓ TRONG SỬ',124,RED,700,glow=8),900,190)
put_screen(cv,text('Câu nói nổi tiếng của Bà Triệu',46,INK,700),900,290)
lg=np.asarray(Image.open(D+'nguoi-gac-su.png').convert('RGBA').resize((130,130),Image.LANCZOS),np.float32)/255;lg[...,:3]*=lg[...,3:4]
blend(cv,lg,1920-44-130,34,.8)
im=Image.fromarray((np.clip(cv,0,1)*255+.5).astype(np.uint8));im.save('bia16/bia_tm16.png')
im.convert('RGB').save('bia16/bia_tm16_youtube.jpg',quality=90);print('ok')
