# Bìa tm23: Lê Phụ Trần một mình một ngựa giữa lính Mông Cổ, tên bay; chữ lớn 4 chữ "SAO LẠI RÚT?";
# logo 130 px, độ đậm .8, cách phải 44, trên 34
import numpy as np,math
from PIL import Image
from canh import *
from engine import *
from khung_dung import cam,PAP
import rig
cv=PAP.copy();c=cam(960,540,1.0)
put(cv,c,'t23_far',960,800,ay=1,k=1,o=.9);put(cv,c,'t23_mid',960,940,ay=1,o=.75)
for i,(x,k) in enumerate([(1350,'lm2'),(1560,'lm3'),(1760,'lm2'),(300,'lm3')]):
    rig.ve23(cv,c,k,x,1000,.95,rig.dung(i*.7),flip=(x>900),vk=['daocong','moc','daocong','moc'][i],o=.95)
rig.ngua(cv,c,'trang',820,1000,1.15,1.3,1.0,flip=False,nguoi='lpt',P=rig.ngoi(.3),vk='giao',t=.3)
import fx_tran
fx_tran.arrows(cv,c,1.2,0,3,[(1900,420),(1800,380)],[(600,760),(1000,780)],n=14,h=160,per=1.0,seed=7,col=(.42,.33,.24))
put(cv,c,'t23_frontL',-120,1120,ax=0,ay=1,s=.85);put(cv,c,'t23_frontR',2040,1120,ax=1,ay=1,s=.8)
put_screen(cv,band(1080,200,PAPER,.82,50),760,190)
put_screen(cv,text('SAO LẠI RÚT?',118,RED,700,glow=8),760,180)
put_screen(cv,text('Lê Phụ Trần · năm 1257',44,INK,700),760,275)
lg=np.asarray(Image.open(D+'nguoi-gac-su.png').convert('RGBA').resize((130,130),Image.LANCZOS),np.float32)/255;lg[...,:3]*=lg[...,3:4]
blend(cv,lg,1920-44-130,34,.8)
im=Image.fromarray((np.clip(cv,0,1)*255+.5).astype(np.uint8))
im.save('bia23/bia_tm23.png');im.convert('RGB').save('bia23/bia_tm23_youtube.jpg',quality=90);print('ok')
