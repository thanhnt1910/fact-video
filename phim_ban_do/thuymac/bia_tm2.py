# Ảnh bìa tm2: thung lũng Chi Lăng, toán quân xin hàng, quân phục trên sườn núi; cành khô; chữ ≤4 từ; logo 130px/0,8/44/34
import os
import dai_tm2 as V
from dai_tm2 import *
def scene(t):
    V.tagfall=lambda *a,**k:None;V.lb=lambda *a,**k:None
    cv=PAP.copy();V.S_chilang(cv,t);return cv
def make(out,vertical=False):
    t=V.mid(35,.55)
    sc=scene(t)
    if not vertical:
        cv=sc.copy()
        put_screen(cv,band(900,520,PAPER,.85,50),500,330)
        V.branch(cv,500,500,.5,7,1,hands=.9,t=0)
        put_screen(cv,text('DỄ BẺ',140,INK,700,glow=8),490,215)
        put_screen(cv,text('CÀNH KHÔ?',140,RED,700,glow=8),490,365)
        put_screen(cv,A('stitle2'),1740,880,s=.5,r=4)
        Wd,Hd=1920,1080
    else:
        Wd,Hd=1080,1920
        cv=np.ones((Hd,Wd,3),np.float32)*PAP[0:1,0:1,:]
        cv[:]=np.asarray(Image.fromarray((np.clip(PAP,0,1)*255).astype(np.uint8)).resize((Wd,Hd)),np.float32)/255
        crop=sc[:, 420:1500]
        m=np.clip(np.arange(1080)/160,0,1)[:,None,None]
        cv[700:1780]=cv[700:1780]*(1-m)+crop*m
        put_screen(cv,text('DỄ BẺ',150,INK,700,glow=8),Wd/2,260)
        put_screen(cv,text('CÀNH KHÔ?',150,RED,700,glow=8),Wd/2,430)
        V.branch(cv,Wd/2,600,.6,7,1,hands=1,t=0)
        put_screen(cv,A('stitle2'),Wd-170,1640,s=.5,r=4)
    lg=np.asarray(Image.open(D+'nguoi-gac-su.png').convert('RGBA').resize((130,130),Image.LANCZOS),np.float32)/255;lg[...,:3]*=lg[...,3:4]
    blend(cv,lg,Wd-44-130,34,.8)
    im=Image.fromarray((np.clip(cv,0,1)*255+.5).astype(np.uint8));im.save(out);return im
im=make('/tmp/gen/bd/bia2/bia_tm2.png');im.resize((1280,720),Image.LANCZOS).save('/tmp/gen/bd/bia2/bia_tm2_youtube.jpg',quality=92)
make('/tmp/gen/bd/bia2/bia_tm2d_doc.png',True);print('ok')
