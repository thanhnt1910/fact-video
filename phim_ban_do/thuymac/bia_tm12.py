import numpy as np
from PIL import Image
from canh import *
from engine import *
import dai_tm12 as mod
from khung_dung import cam,PAP
cv=PAP.copy();c=cam(960,540,1.0)
put(cv,c,'t12_dem',1000,520,s=1.5)

put_screen(cv,band(1300,200,PAPER,.8,50),960,215)
put_screen(cv,text('VUA ĐẦM ĐÊM',130,RED,700,glow=8),960,215)
put_screen(cv,A('s547'),1700,330,s=.55,r=4)
lg=np.asarray(Image.open(D+'nguoi-gac-su.png').convert('RGBA').resize((130,130),Image.LANCZOS),np.float32)/255;lg[...,:3]*=lg[...,3:4]
blend(cv,lg,1920-44-130,34,.8)
im=Image.fromarray((np.clip(cv,0,1)*255+.5).astype(np.uint8));im.save('bia12/bia_tm12.png')
im.resize((320,180),Image.LANCZOS).save('bia12/small.png');print('ok')
