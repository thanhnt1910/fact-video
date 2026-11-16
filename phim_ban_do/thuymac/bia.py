# Ảnh bìa: cảnh thủy triều rút, thuyền mắc cọc lật; chữ lớn ≤4 từ; logo góc phải (130 px, 0,8, cách phải 44, trên 34)
from canh import *
import dai
def make(W,H,out,V=False):
    PAP=(A('paper_v') if V else A('paper_h'))[...,:3].copy()
    cv=PAP.copy()
    c=Cam(1140 if V else 1060,800 if V else 770,(H/1080)*1.05 if V else 1.35,W,H)
    t=3.0;wl=895
    boats=[]
    for i,(x,ln,r) in enumerate([(880,0,-10),(1010,2,24),(1150,1,-38),(1290,2,62),(1380,0,12)]):
        s=.6+ln*.13;y=LANE_TIP[ln]+12+(30 if abs(r)>30 else 0)
        boats.append(dict(x=x,y=y,s=s,r=r,o=1 if abs(r)<50 else .85,flip=True,ln=ln))
    boats.sort(key=lambda b:b['ln'])
    viet=[dict(x=560+i*70,y=wl+80+(i%3)*30,s=.62) for i in range(4)]+[dict(x=1620-i*60,y=wl+70+(i%3)*30,s=.62,flip=True) for i in range(3)]
    def fx(cv,cam):
        put(cv,cam,'splash',1290,LANE_TIP[2]+60,s=.9,o=.55,ay=.95)
        put(cv,cam,'splash',1010,LANE_TIP[2]+60,s=.7,o=.45,ay=.95)
    river(cv,c,t,PAP,wl=wl,boats=boats,viet=viet,under=.06,fx=[fx],cliffs=True,clx=-330,mist=.25,sun=0,reeds=1)
    put(cv,c,'sun',1500,560,s=1.6,o=.85,k=.15) if False else None
    # chữ lớn
    if V:
        put_screen(cv,band(900,330,PAPER,.8,50),W/2,420)
        put_screen(cv,text('YẾU HƠN',150,INK,700,glow=8),W/2,330)
        put_screen(cv,text('MÀ THẮNG?',150,RED,700,glow=8),W/2,500)
        put_screen(cv,A('stitle'),W-150,1560,s=.6,r=4)
    else:
        put_screen(cv,band(820,360,PAPER,.78,50),470,330)
        put_screen(cv,text('YẾU HƠN',138,INK,700,glow=8),470,250)
        put_screen(cv,text('MÀ THẮNG?',138,RED,700,glow=8),470,420)
        put_screen(cv,A('stitle'),1760,880,s=.55,r=4)
    lg=np.asarray(Image.open(D+'nguoi-gac-su.png').convert('RGBA').resize((130,130),Image.LANCZOS),np.float32)/255;lg[...,:3]*=lg[...,3:4]
    blend(cv,lg,W-44-130,34,.8)
    im=Image.fromarray((np.clip(cv,0,1)*255+.5).astype(np.uint8));im.save(out)
    return im
import os;os.makedirs('/tmp/gen/bd/bia',exist_ok=True)
im=make(1920,1080,'/tmp/gen/bd/bia/bia_bd2.png');im.resize((1280,720),Image.LANCZOS).save('/tmp/gen/bd/bia/bia_bd2_youtube.jpg',quality=92)
make(1080,1920,'/tmp/gen/bd/bia/bia_bd2d_doc.png',V=True)
print('ok')
