import sys,numpy as np
from PIL import Image
import dai_tm2
from canh import *
from dai import PAP
import dai_tm11m as mod
for m in (mod,dai_tm2):
    for nm in ('tagfall','lb','big'): setattr(m,nm,lambda *a,**kw:None)
sc=PAP.copy();mod.S_8(sc,mod.mid(8,.7))
cv=sc.copy()
put_screen(cv,band(1100,330,PAPER,.8,50),960,245)
put_screen(cv,text('NGƯỜI VÂY THÀNH',120,INK,700,glow=8),960,170)
put_screen(cv,text('THÀNH NGƯỜI BỊ VÂY',120,RED,700,glow=8),960,320)
put_screen(cv,A('s931'),1740,880,s=.5,r=4)
lg=np.asarray(Image.open(D+'nguoi-gac-su.png').convert('RGBA').resize((130,130),Image.LANCZOS),np.float32)/255;lg[...,:3]*=lg[...,3:4]
blend(cv,lg,1920-44-130,34,.8)
im=Image.fromarray((np.clip(cv,0,1)*255+.5).astype(np.uint8));im.save('bia11/bia_tm11m.png')
im.resize((320,180),Image.LANCZOS).save('bia11/small.png');print('ok')
