# Bìa tm28: hỏa súng bắn trúng chiếc thuyền sơn xanh của Chế Bồng Nga trên sông Hải Triều;
# chữ lớn "CHIẾC THUYỀN SƠN XANH"; logo 130 px, độ đậm .8, cách phải 44, trên 34
import sys;sys.argv=['x','soi']
import numpy as np
from PIL import Image
import dai_tm28 as Dm
from engine import put_screen,text,band,blend
from canh import RED,INK,PAPER,D
t=Dm.T[70]+.7
cv=Dm.PAP.copy();Dm.NOCAP=True
Dm.S_68.__globals__['nhan']=lambda *a,**k:None
Dm.S_68(cv,t)
put_screen(cv,band(1240,210,PAPER,.86,50),900,190)
put_screen(cv,text('CHIẾC THUYỀN SƠN XANH',104,RED,700,glow=8),900,180)
put_screen(cv,text('Chế Bồng Nga · năm 1390',44,INK,700),900,280)
lg=np.asarray(Image.open(D+'nguoi-gac-su.png').convert('RGBA').resize((130,130),Image.LANCZOS),np.float32)/255;lg[...,:3]*=lg[...,3:4]
blend(cv,lg,1920-44-130,34,.8)
im=Image.fromarray((np.clip(cv,0,1)*255+.5).astype(np.uint8))
import os;os.makedirs('/tmp/out',exist_ok=True)
im.save('/tmp/out/bia_tm28.png');im.convert('RGB').save('/tmp/out/bia_tm28_youtube.jpg',quality=90);print('ok')
