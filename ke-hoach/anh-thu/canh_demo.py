import sys,math,random
sys.path.insert(0,'/tmp/lh/phim_ban_do');sys.path.insert(0,'/tmp/ly/demo')
from PIL import Image,ImageDraw,ImageFilter
import mapdraw as M, mapprops as P
from co import cloth,pole,phuong,long as longf
INK=(30,22,16,255);PAPER=(236,224,190,255)
G=(52,142,86);R_=(188,52,42);OR=(214,120,40);PU=(130,70,130);GD=(190,150,50);BR=(130,92,56)
CW,CH=900,600
def cell(cap,fn,t=0.35,bg=PAPER):
    im=Image.new('RGBA',(CW,CH),bg);d=ImageDraw.Draw(im,'RGBA')
    d.rectangle((0,0,CW-1,CH-1),outline=(90,66,40,255),width=6)
    fn(d,t)
    f=M.font(30);d.rounded_rectangle((20,CH-62,CW-20,CH-18),12,fill=(20,14,8,215));d.text((CW//2,CH-40),cap,font=f,fill=(250,240,215,255),anchor='mm')
    return im
def sheet(cells,fn):
    S=Image.new('RGB',(CW*2,CH*3),(30,24,18))
    for i,c in enumerate(cells): S.paste(c.convert('RGB'),((i%2)*CW,(i//2)*CH))
    S.save(fn)
def ground(d,y,col=(196,178,130,255)):
    d.rectangle((6,y,CW-6,CH-6),fill=col)
def tree(d,x,y,s=1):
    d.rectangle((x-5*s,y-40*s,x+5*s,y),fill=(100,70,44,255));d.ellipse((x-34*s,y-92*s,x+34*s,y-30*s),fill=(70,120,70,255),outline=INK,width=2)
# ---------- Tờ 1: cờ, quân, lọng, chân dung
def droop(d,x,y,col=(140,140,144,255)):
    d.line([(x,y),(x+46,y-62)],fill=(86,58,34,255),width=8)
    d.polygon([(x+46,y-62),(x+84,y-30),(x+78,y+8),(x+40,y-34)],fill=col,outline=INK)
def quan(d,t,x0,y0,col,defeat=False,flagcol=None):
    r=random.Random(3);pos=[]
    for row in range(2):
        for i in range(4):
            x=x0+i*104+row*48;y=y0+row*76+r.uniform(-3,3);pos.append((x,y))
    for k,(x,y) in enumerate(pos):
        if defeat: M.soldier(d,x,y,44,(128,128,134),1,0,alpha=210)
        else: M.soldier(d,x,y,44,col,1,t*7+k)
    for k,i in enumerate((1,6)):
        x,y=pos[i]
        if defeat: droop(d,x+30,y+10)
        else: pole(d,x+30,y+10,130);cloth(d,x+35,y-118,92,58,flagcol or col,t+k,band=False)
    if not defeat:
        gx=x0-120;gy=y0+60
        M.horse(d,gx,gy,56,col,1,t*6)
        pole(d,gx-62,gy+14,210);cloth(d,gx-57,gy-190,150,92,flagcol or col,t,band=True)
def f1(d,t):
    ground(d,360);tree(d,850,360,1.1);quan(d,t,290,390,G)
def f2(d,t):
    ground(d,360);quan(d,t,230,390,OR,defeat=True);M.whiteflag(d,800,330,80)
def f3(d,t):  # vua với lọng
    ground(d,400);M.soldier(d,430,430,64,(214,176,40),1,t*4)
    longf(d,430+60,460,92)
    for dx in (-190,190):
        M.soldier(d,430+dx,440,50,G,1,t*6+dx);pole(d,430+dx+30,450,150);cloth(d,430+dx+34,300,100,64,G,t+dx,band=True)
    # quạt lông
    d.ellipse((260,330,330,400),fill=(246,240,226,255),outline=INK,width=3)
def f4(d,t):  # chip chân dung
    d.rectangle((0,0,CW,CH),fill=(224,212,178,255))
    items=[('king',(214,176,40),'Lý Công Uẩn (vua)'),('general',G,'Lê Phụng Hiểu'),('lord',(190,150,50),'Lê Long Đĩnh'),('noble',G,'Đào Cam Mộc'),('prince',G,'Lý Phật Mã'),('child',G,'Lý Công Uẩn (bé)')]
    for i,(k,c,nm) in enumerate(items):
        S=190;im=M.face_sprite(k,c,S);x=70+(i%3)*270;y=80+(i//3)*220
        d._image.paste(im,(x,y),im)
        d.text((x+S//2,y+S+18),nm,font=M.font(24),fill=(40,30,20,255),anchor='mm')
def f5(d,t):  # đổi triều: cờ cũ hạ, cờ mới kéo lên
    ground(d,420)
    d.line([(300,420),(300,120)],fill=(86,58,34,255),width=12);d.line([(600,420),(600,120)],fill=(86,58,34,255),width=12)
    cloth(d,306,300,150,90,(176,150,60),t,band=True)       # cờ cũ hạ thấp
    cloth(d,606,130,150,90,G,t,band=True)                   # cờ mới trên cao
    d.line([(450,200),(450,330)],fill=(120,90,60,255),width=5);d.polygon([(450,340),(440,320),(460,320)],fill=(120,90,60,255))
    d.text((300,455),'nhà Tiền Lê',font=M.font(28),fill=INK,anchor='mm');d.text((600,455),'nhà Lý',font=M.font(28),fill=INK,anchor='mm')
def f6(d,t):  # trại quân
    ground(d,380);P.draw(d,'camp',450,440,50,0.5,t,'')
    for i,x in enumerate((110,790)):
        M.soldier(d,x,470,46,G,1,t*3+i);pole(d,x+28,478,150);cloth(d,x+33,330,92,58,G,t+i)
def scene_sheet1(fn):
    sheet([cell('Cụm quân có lính cầm cờ, tướng cầm cờ lớn',f1),cell('Quân thua: cờ rũ, lính chuyển xám, cờ trắng',f2),cell('Vua đi dưới lọng vàng, quạt lông, quân cầm cờ',f3),cell('Chân dung tròn theo vai trò (mẫu khuôn có sẵn)',f4),cell('Đổi triều: cờ cũ hạ xuống, cờ mới kéo lên',f5),cell('Trại quân: lều, cờ, lửa bếp, lính gác',f6)],fn)
scene_sheet1('/tmp/ly/demo/to1.png')
