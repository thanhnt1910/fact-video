# Bìa tm18: vua Đen đứng trên gò, cuộn sử "tướng giặc" bị gạch; chữ lớn 4 chữ; logo 130 px, độ đậm .8, cách phải 44, trên 34
import numpy as np
from PIL import Image
from canh import *
from engine import *
from khung_dung import cam,PAP
cv=PAP.copy();c=cam(960,540,1.0)
put(cv,c,'t18_far',960,800,ay=1,k=1,o=.9);put(cv,c,'t18_mid',960,940,ay=1,o=.75)
put(cv,c,'t18x_xungde',760,700,s=1.25)
put(cv,c,'t18_cuon',1540,640,s=.62,r=3)
put_screen(cv,text('tướng giặc',62,RED,700),1540,640)
put_screen(cv,band(360,10,RED,.9,2),1540,640,1,r=-8) if False else None
from engine import stroke as _st
put(cv,c,'t18_frontL',-120,1120,ax=0,ay=1,s=.85);put(cv,c,'t18_frontR',2040,1120,ax=1,ay=1,s=.8)
put_screen(cv,band(1260,200,PAPER,.82,50),840,190)
put_screen(cv,text('VUA ĐEN HAY GIẶC?',118,RED,700,glow=8),840,180)
put_screen(cv,text('Mai Thúc Loan · năm 722',44,INK,700),840,275)
lg=np.asarray(Image.open(D+'nguoi-gac-su.png').convert('RGBA').resize((130,130),Image.LANCZOS),np.float32)/255;lg[...,:3]*=lg[...,3:4]
blend(cv,lg,1920-44-130,34,.8)
im=Image.fromarray((np.clip(cv,0,1)*255+.5).astype(np.uint8))
from PIL import ImageDraw
d=ImageDraw.Draw(im);d.line([(1400,665),(1680,615)],fill=(163,38,28),width=12)
im.save('bia18/bia_tm18.png');im.convert('RGB').save('bia18/bia_tm18_youtube.jpg',quality=90);print('ok')
