import numpy as np
from PIL import Image
from canh import *
from engine import *
import dai_tm16 as mod
from khung_dung import cam,PAP
cv=PAP.copy();c=cam(960,540,1.0)
put(cv,c,'t16_voi1',960,640,s=1.35)
put(cv,c,'t16_spr_voi',900,655,s=1.7)
put_screen(cv,band(1300,200,PAPER,.8,50),960,215)
put_screen(cv,text('BÀ KHÔNG RA HÀNG',130,RED,700,glow=8),960,215)
put_screen(cv,A('s248'),1700,760,s=.55,r=4)
lg=np.asarray(Image.open(D+'nguoi-gac-su.png').convert('RGBA').resize((130,130),Image.LANCZOS),np.float32)/255;lg[...,:3]*=lg[...,3:4]
blend(cv,lg,1920-44-130,34,.8)
im=Image.fromarray((np.clip(cv,0,1)*255+.5).astype(np.uint8));im.save('bia16/bia_tm16.png')
im.convert('RGB').save('bia16/bia_tm16_youtube.jpg',quality=90)
im.resize((320,180),Image.LANCZOS).save('bia16/small.png');print('ok')
