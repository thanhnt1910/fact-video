# Ảnh bìa tm3 (Như Nguyệt 1077) và tm4 (Đông Bộ Đầu 1258): một cảnh thật của trận, chữ ≤4 từ, logo 130px/0,8/44/34
import sys,importlib,numpy as np
from PIL import Image
import dai_tm2
from canh import *
from dai import PAP
CF={'tm3':dict(mod='dai_tm3',fn='S_cau',n=21,f=.6,l1='KHÔNG QUA',l2='NỔI SÔNG?',seal='stitle3',ty=170,cx=(180,1180)),
    'tm4':dict(mod='dai_tm4',fn='S_h1',n=1,f=.7,l1='ĐẦU THẦN',l2='CHƯA RƠI',seal='stitle4',ty=170,cx=(470,1470)),
    'tm5':dict(mod='dai_tm5',fn='S_3',n=3,f=.5,l1='LÀM VƯƠNG',l2='HAY QUỶ?',seal='stitle5',ty=170,cx=(420,1500)),
    'tm6':dict(mod='dai_tm6',fn='S_22',n=22,f=.8,l1='ĐÁNH GIẶC',l2='NHÀN?',seal='stitle6',ty=170,cx=(420,1500)),
    'tm7':dict(mod='dai_tm7',fn='S_17',n=18,f=.5,l1='TIẾNG SÚNG',l2='KHÔNG NỔ',seal='stitle7',ty=170,cx=(350,1450)),
    'tm8':dict(mod='dai_tm8',fn='S_12',n=13,f=.6,l1='CÓ NÊN',l2='ĐUỔI THEO?',seal='stitle8',ty=170,cx=(420,1500)),
    'tm9':dict(mod='dai_tm9',fn='S_19',n=19,f=.6,l1='KHÚC SÔNG',l2='CHỌN SẴN',seal='stitle9',ty=170,cx=(420,1500)),
    'tm10':dict(mod='dai_tm10',fn='S_18',n=18,f=.6,l1='HẸN NGÀY',l2='ĂN MỪNG',seal='stitle10',ty=170,cx=(420,1500))}
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
        vz=min(150,int(950/(.62*max(len(c['l1']),len(c['l2'])))))
        put_screen(cv,text(c['l1'],vz,INK,700,glow=8),Wd/2,300)
        put_screen(cv,text(c['l2'],vz,RED,700,glow=8),Wd/2,300+vz*1.15)
        put_screen(cv,A(c['seal']),Wd-170,1640,s=.5,r=4)
    lg=np.asarray(Image.open(D+'nguoi-gac-su.png').convert('RGBA').resize((130,130),Image.LANCZOS),np.float32)/255;lg[...,:3]*=lg[...,3:4]
    blend(cv,lg,Wd-44-130,34,.8)
    im=Image.fromarray((np.clip(cv,0,1)*255+.5).astype(np.uint8));im.save(out);return im
import os
k=sys.argv[1];d=f'/tmp/gen/bd/bia{k[-1]}/' if k in ('tm3','tm4') else f'/tmp/gen/bd/bia_{k}/';os.makedirs(d,exist_ok=True)
im=make(k,d+f'bia_{k}.png');im.resize((1280,720),Image.LANCZOS).save(d+f'bia_{k}_youtube.jpg',quality=92)
make(k,d+f'bia_{k}d_doc.png',True);print('ok',k)
