# Ảnh bìa tm3 (Như Nguyệt 1077) và tm4 (Đông Bộ Đầu 1258): một cảnh thật của trận, chữ ≤4 từ, logo 130px/0,8/44/34
import sys,importlib,numpy as np
from PIL import Image
import dai_tm2
from canh import *
from dai import PAP
CF={'tm3':dict(mod='dai_tm3',fn='S_cau',n=21,f=.6,l1='KHÔNG QUA',l2='NỔI SÔNG?',seal='stitle3',ty=170,cx=(180,1180)),
    'tm4':dict(mod='dai_tm4',fn='S_h1',n=1,f=.7,l1='ĐẦU THẦN',l2='CHƯA RƠI',seal='stitle4',ty=170,cx=(470,1470))}
def make(k,out,vertical=False):
    c=CF[k];mod=importlib.import_module(c['mod'])
    for m in (mod,dai_tm2):
        for nm in ('tagfall','lb','big'): setattr(m,nm,lambda *a,**kw:None)
    sc=PAP.copy();getattr(mod,c['fn'])(sc,mod.mid(c['n'],c['f']))
    if not vertical:
        Wd,Hd=1920,1080;cv=sc.copy()
        put_screen(cv,band(1100,330,PAPER,.8,50),960,c['ty']+75)
        put_screen(cv,text(c['l1'],130,INK,700,glow=8),960,c['ty'])
        put_screen(cv,text(c['l2'],130,RED,700,glow=8),960,c['ty']+150)
        put_screen(cv,A(c['seal']),1740,880,s=.5,r=4)
    else:
        Wd,Hd=1080,1920
        cv=np.asarray(Image.fromarray((np.clip(PAP,0,1)*255).astype(np.uint8)).resize((Wd,Hd)),np.float32)/255
        a,b=c['cx'];crop=sc[0:1080,a:b]
        crop=np.asarray(Image.fromarray((np.clip(crop,0,1)*255).astype(np.uint8)).resize((1080,1170),Image.LANCZOS),np.float32)/255
        y=np.arange(1170);m=(np.clip(y/200,0,1)*np.clip((1169-y)/220,0,1))[:,None,None]
        cv[620:1790]=cv[620:1790]*(1-m)+crop*m
        put_screen(cv,text(c['l1'],150,INK,700,glow=8),Wd/2,300)
        put_screen(cv,text(c['l2'],150,RED,700,glow=8),Wd/2,470)
        put_screen(cv,A(c['seal']),Wd-170,1640,s=.5,r=4)
    lg=np.asarray(Image.open(D+'nguoi-gac-su.png').convert('RGBA').resize((130,130),Image.LANCZOS),np.float32)/255;lg[...,:3]*=lg[...,3:4]
    blend(cv,lg,Wd-44-130,34,.8)
    im=Image.fromarray((np.clip(cv,0,1)*255+.5).astype(np.uint8));im.save(out);return im
k=sys.argv[1];d=f'/tmp/gen/bd/bia{k[-1]}/'
im=make(k,d+f'bia_{k}.png');im.resize((1280,720),Image.LANCZOS).save(d+f'bia_{k}_youtube.jpg',quality=92)
make(k,d+f'bia_{k}d_doc.png',True);print('ok',k)
