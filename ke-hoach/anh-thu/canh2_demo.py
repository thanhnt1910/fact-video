from canh import *
def person(d,x,y,s,robe,hat=None,bald=False,hair=(30,26,28,255),pose=0):
    sk=(232,196,150,255)
    d.polygon([(x-s*.55,y),(x+s*.55,y),(x+s*.4,y-s*1.5),(x-s*.4,y-s*1.5)],fill=robe+(255,),outline=INK)
    d.ellipse((x-s*.32,y-s*2.2,x+s*.32,y-s*1.5),fill=sk,outline=INK,width=2)
    if not bald: d.pieslice((x-s*.36,y-s*2.3,x+s*.36,y-s*1.6),180,360,fill=hair)
    if hat=='quan': d.rectangle((x-s*.4,y-s*2.5,x+s*.4,y-s*2.15),fill=(30,26,28,255),outline=INK)
    if hat=='crown': d.rectangle((x-s*.45,y-s*2.55,x+s*.45,y-s*2.2),fill=(30,26,28,255),outline=INK);d.rectangle((x-s*.45,y-s*2.3,x+s*.45,y-s*2.2),fill=(224,176,62,255))
def night(d,a):
    d._image.alpha_composite(Image.new('RGBA',(CW,CH),(10,16,50,int(a))))
def s_chua(d,t):
    ground(d,400)
    # chùa
    d.rectangle((520,230,830,400),fill=(170,120,84,255),outline=INK,width=3)
    d.polygon([(480,240),(675,130),(870,240),(840,270),(510,270)],fill=(122,74,52,255),outline=INK)
    d.rectangle((640,300,710,400),fill=(40,28,20,255),outline=INK)
    # chuông treo
    d.line([(420,160),(420,230)],fill=INK,width=4);sw=math.sin(t*5)*10
    d.polygon([(380+sw,300),(460+sw,300),(445+sw,235),(395+sw,235)],fill=(214,170,60,255),outline=INK)
    d.rectangle((360,150,480,162),fill=(100,70,44,255),outline=INK)
    person(d,180,470,68,(120,84,56),bald=True)       # sư
    person(d,310,480,60,(150,70,90))                 # mẹ
    # cậu bé
    M.face_sprite  # noqa
    d.ellipse((250,418,290,458),fill=(232,196,150,255),outline=INK,width=2);d.ellipse((246,414,262,430),fill=(30,26,28,255));d.ellipse((280,414,296,430),fill=(30,26,28,255))
    d.polygon([(255,520),(285,520),(280,458),(260,458)],fill=(160,120,80,255),outline=INK)
    for k in range(3): d.ellipse((400+k*10+math.sin(t*3+k)*6,120-k*26,414+k*10,134-k*26),fill=(120,120,120,90))
def s_khoc(d,t):
    d.rectangle((6,6,CW-6,400),fill=(190,150,110,255));ground(d,400,(150,110,76,255))
    d.rectangle((330,150,570,330),fill=(150,40,34,255),outline=INK,width=3);d.rectangle((300,330,600,370),fill=(214,170,60,255),outline=INK,width=3)  # ngai
    d.rectangle((300,370,600,410),fill=(200,160,70,255),outline=INK)
    d.polygon([(560,480),(790,480),(760,430),(590,430)],fill=(246,244,238,255),outline=INK)    # vải trắng
    person(d,500,520,60,(60,70,110),pose=1)
    for i,x in enumerate((80,150,220)):
        person(d,x+math.sin(t*6+i)*0,470,40,(100,60,60),hat='quan')
        d.line([(x+30,430),(x+70,420)],fill=INK,width=2)
    d.polygon([(30,300),(30,400),(90,400),(90,300)],fill=(40,28,20,255),outline=INK)
    d.ellipse((810,100,850,140),fill=(250,200,90,255));d.line([(830,140),(830,200)],fill=INK,width=3)
def s_khe(d,t):
    ground(d,420);cx,cy=450,270;r=140
    pts=[]
    for k in range(10):
        a=-math.pi/2+k*math.pi/5;rr=r if k%2==0 else r*0.55;pts.append((cx+math.cos(a)*rr,cy+math.sin(a)*rr))
    for q in range(8):
        d.ellipse((cx-170-q*3,cy-170-q*3,cx+170+q*3,cy+170+q*3),outline=(255,230,120,int(40-q*4)),width=3)
    d.polygon(pts,fill=(214,222,90,255),outline=INK)
    d.polygon([(cx+math.cos(-math.pi/2+k*math.pi/5)*(r*.7 if k%2==0 else r*.38),cy+math.sin(-math.pi/2+k*math.pi/5)*(r*.7 if k%2==0 else r*.38)) for k in range(10)],fill=(236,240,150,255))
    pulse=1+0.08*math.sin(t*6)
    d.ellipse((cx-30*pulse,cy-38*pulse,cx+30*pulse,cy+38*pulse),fill=(122,40,70,255),outline=INK,width=3)
    d.ellipse((cx-12,cy-26,cx-2,cy-12),fill=(210,120,150,255))
    d.text((cx,470),'hạt như hạt mận',font=M.font(30),fill=INK,anchor='mm')
def s_den(d,t):
    d.rectangle((6,6,CW-6,CH-6),fill=(70,56,44,255));d.rectangle((6,430,CW-6,CH-6),fill=(48,38,30,255))
    fl=math.sin(t*14)*5
    d.ellipse((410,440,490,462),fill=(150,100,60,255),outline=INK,width=2)
    d.polygon([(440,440),(450+fl,385),(460,440)],fill=(250,190,60,255));d.polygon([(444,440),(450+fl*.6,410),(456,440)],fill=(255,240,160,255))
    ov=Image.new('RGBA',(CW,CH),(10,16,50,90));od=ImageDraw.Draw(ov)
    od.polygon([(130,420),(130,170),(210,130),(290,170),(290,420)],fill=(0,0,0,120))
    od.polygon([(560,420),(560,230),(620,190),(680,230),(700,330),(760,320),(740,420)],fill=(0,0,0,120))
    d._image.alpha_composite(ov)
    person(d,150,540,70,(70,100,70),hat='quan');person(d,720,540,66,(110,70,70))
    d.line([(190,470),(260,430)],fill=(232,196,150,255),width=7)
def s_ngoi(d,t):
    d.rectangle((6,6,CW-6,380),fill=(190,150,110,255));ground(d,380,(150,110,76,255))
    for i in range(4): d.rectangle((250-i*0,260+i*24,650,284+i*24),fill=(214-i*14,170-i*14,70),outline=INK)
    d.rectangle((410,150,490,270),fill=(150,40,34,255),outline=INK,width=3)
    person(d,450,262,56,(224,176,60),hat='crown')
    for k in range(7):
        x=90+k*120;b=max(0,math.sin(t*3-k*.6))*14
        person(d,x,520+0*b,44,(100+k*8,70,60),hat='quan')
        d.polygon([(x-18,520-66+b),(x+18,520-66+b),(x+8,520-60+b)],fill=(0,0,0,0))
    for x in (150,750):
        pole(d,x,380,170);cloth(d,x+4,214,90,56,G,t)
def s_nui(d,t):
    d.rectangle((6,6,CW-6,CH-6),fill=(232,226,206,255))
    for (x,h,w,c) in ((150,300,170,(120,126,120)),(330,360,150,(104,112,106)),(560,330,170,(112,118,112)),(760,280,150,(124,130,124))):
        d.polygon([(x-w,470),(x-w*.2,470-h),(x+w*.1,470-h-30),(x+w,470)],fill=c+(255,),outline=INK)
        for q in range(4): d.line([(x-w*.1+q*18,470-h+40),(x-w*.2+q*26,470)],fill=(80,86,80,255),width=3)
    ground(d,470);d.rectangle((420,400,500,470),fill=(120,84,56,255),outline=INK);d.polygon([(400,400),(460,350),(520,400)],fill=(122,74,52,255),outline=INK)
    pole(d,520,470,120);cloth(d,524,350,70,44,G,t)
    for k in range(3):
        d.ellipse((60+k*260+math.sin(t*2+k)*14,330+k*20,260+k*260,380+k*20),fill=(255,255,255,110))
def s_rong(d,t):
    d.rectangle((6,6,CW-6,CH-6),fill=(196,224,232,255))
    for k in range(8):
        for x in range(0,CW,70):
            d.arc((x+math.sin(t*3+k)*10-40,300+k*34,x+60,330+k*34),200,340,fill=(90,140,170,255),width=4)
    d.polygon([(80,360),(200,360),(180,400),(100,400)],fill=(120,84,56,255),outline=INK)    # thuyền
    for q in range(10): d.ellipse((420-q*14,40-q*10,820+q*14,320+q*10),outline=(255,230,120,max(0,28-q*3)),width=3)
    pts=[]
    for i in range(40):
        u=i/39;x=140+u*620;y=280-math.sin(u*math.pi)*190+math.sin(u*11-t*6)*28;pts.append((x,y))
    for i in range(39):
        w=44-i*0.8
        d.line([pts[i],pts[i+1]],fill=(236,190,50,255),width=int(w+4));d.line([pts[i],pts[i+1]],fill=(250,226,120,255),width=int(w*.45))
    hx,hy=pts[-1];d.ellipse((hx-24,hy-22,hx+30,hy+20),fill=(236,190,50,255),outline=INK,width=3);d.ellipse((hx+8,hy-8,hx+16,hy),fill=INK)
    d.polygon([(hx,hy-18),(hx-6,hy-50),(hx+10,hy-28)],fill=(224,160,40,255));d.line([(hx+24,hy),(hx+70,hy+14),(hx+90,hy+4)],fill=(224,160,40,255),width=5)
    for i in range(2,38,3):
        px,py=pts[i];d.arc((px-10,py-10,px+10,py+10),200,340,fill=(176,120,20,255),width=3)
    d.text((CW//2,520),'theo lời kể',font=M.font(30),fill=(60,60,70,255),anchor='mm')
def s_nhat(d,t):
    d.rectangle((6,6,CW-6,CH-6),fill=(160,200,230,255));u=min(1,t/0.7)
    d.rectangle((6,6,CW-6,CH-6),fill=(int(160-130*u),int(200-150*u),int(230-150*u),255))
    cx,cy=450,240;d.ellipse((cx-90,cy-90,cx+90,cy+90),fill=(255,236,150,255))
    for k in range(24):
        a=k*math.pi/12;d.line([(cx+math.cos(a)*110,cy+math.sin(a)*110),(cx+math.cos(a)*(150+14*math.sin(t*6+k)),cy+math.sin(a)*(150+14*math.sin(t*6+k)))],fill=(255,240,180,255),width=4)
    d.ellipse((cx-90+95*(1-u*0.9),cy-90,cx+90+95*(1-u*0.9),cy+90),fill=(12,10,20,255))
    ground(d,430,(96,86,60,255))
    for i in range(5): d.line([(120+i*140,330+i*10),(140+i*140,320+i*10),(160+i*140,330+i*10)],fill=INK,width=3)
    d.rectangle((100,360,200,430),fill=(120,84,56,255),outline=INK);d.polygon([(85,360),(150,315),(215,360)],fill=(122,74,52,255),outline=INK)
def s_cua(d,t):
    d.rectangle((6,6,CW-6,CH-6),fill=(200,214,224,255));d.rectangle((60,200,840,440),fill=(150,138,120,255),outline=INK,width=4)
    for x in range(60,840,60): d.rectangle((x,170,x+34,200),fill=(150,138,120,255),outline=INK)
    ground(d,440);op=0.5+0.5*math.sin(t*3)*0.4
    d.rectangle((310,260,590,440),fill=(40,28,20,255),outline=INK,width=3)
    for i,x in enumerate((340,400)): M.soldier(d,x+10,440,50,(130,90,60),1,t*2+i)
    w=int(110*(1-op*0.6))
    d.rectangle((310,260,310+w,440),fill=(120,76,44,255),outline=INK,width=3);d.rectangle((590-w,260,590,440),fill=(120,76,44,255),outline=INK,width=3)
    for q in range(5):
        d.line([(310,300+q*30),(310+w,300+q*30)],fill=(70,44,26,255),width=3);d.line([(590-w,300+q*30),(590,300+q*30)],fill=(70,44,26,255),width=3)
    for x in (310,590): d.ellipse((x-10,340,x+10,360),fill=(224,176,62,255),outline=INK)
    for x in (140,700): pole(d,x,200,100);cloth(d,x+4,110,80,50,(214,120,40),t)
def s_chuong(d,t):
    d.rectangle((6,6,CW-6,CH-6),fill=(80,56,40,255));ground(d,460,(60,44,34,255))
    for i in range(3): d.ellipse((90,330,320,470),fill=(60,40,30,255),outline=INK,width=3)
    M.fire(d,205,440,120,t,7)
    d.rectangle((420,200,780,230),fill=(120,84,56,255),outline=INK);d.rectangle((420,200,450,470),fill=(120,84,56,255),outline=INK);d.rectangle((750,200,780,470),fill=(120,84,56,255),outline=INK)
    d.line([(600,230),(600,300)],fill=INK,width=5)
    d.polygon([(540,430),(660,430),(640,300),(560,300)],fill=(214,170,60,255),outline=INK);d.ellipse((540,415,660,445),fill=(190,140,40,255),outline=INK)
    p=(t*1.6)%1
    d.line([(320,360),(380,300)],fill=(255,150,40,255),width=int(10*(1-p)+4));d.ellipse((370,290,400,320),fill=(255,190,60,255))
    for k in range(10): d.ellipse((330+k*30+math.sin(t*5+k)*8,420-((t*1.2+k*.1)%1)*160,340+k*30,430-((t*1.2+k*.1)%1)*160),fill=(255,170,60,170))
def s_thanh(d,t):
    d.rectangle((6,6,CW-6,CH-6),fill=(210,226,232,255));ground(d,430)
    d.rectangle((6,470,CW-6,CH-6),fill=(90,150,190,255))
    for k in range(10): d.arc((20+k*90+math.sin(t*3+k)*8,490,100+k*90,520),200,340,fill=(200,230,250,255),width=3)
    rise=min(1,t/0.6)
    d.rectangle((120,430-int(190*rise),780,430),fill=(160,146,126,255),outline=INK,width=3)
    for i,x in enumerate((100,240,380,520,660,800)):
        d.line([(x,430),(x,180)],fill=(120,84,56,255),width=6)
    for y in (250,330): d.line([(100,y),(800,y)],fill=(120,84,56,255),width=6)
    for i,x in enumerate((200,420,640)):
        person(d,x+math.sin(t*4+i)*10,430,38,(150,100,70),hat=None)
        d.line([(x-20+math.sin(t*4+i)*10,380),(x+60+math.sin(t*4+i)*10,360)],fill=(120,84,56,255),width=7)
def s_tang(d,t):
    d.rectangle((6,6,CW-6,400),fill=(190,150,110,255));ground(d,400,(150,110,76,255))
    for x in (130,770):
        fl=math.sin(t*14)*3;d.rectangle((x-6,300,x+6,440),fill=(120,84,56,255));d.polygon([(x-10,296),(x+fl,250),(x+10,296)],fill=(250,190,60,255))
    d.rectangle((300,330,600,400),fill=(246,244,238,255),outline=INK,width=3);d.rectangle((300,400,600,430),fill=(214,170,60,255),outline=INK)
    person(d,330,540,74,(246,244,238),hat=None)
    d.rectangle((300,300,600,330),fill=(246,244,238,255),outline=INK)
    for i,x in enumerate((500,580,660)): person(d,x+60,560,46,(120,100,90),hat='quan')
cells1=[cell('Sân chùa: sư đón cậu bé, chuông đung đưa, khói hương',s_chua),cell('Điện vắng: quan chạy, một người quỳ lại (vải trắng)',s_khoc),cell('Quả khế bổ đôi, hạt như hạt mận',s_khe),cell('Đêm đèn dầu: hai người, bóng đổ dài trên tường',s_den,bg=(70,56,44,255)),cell('Lên ngôi: quan cúi theo lượt, cờ hai bên',s_ngoi),cell('Hoa Lư giữa núi đá, mây trôi, một cửa ải hẹp',s_nui)]
cells2=[cell('Rồng vàng bay lên từ sông (theo lời kể)',s_rong),cell('Nhật thực: vòng đen che dần mặt trời',s_nhat,t=0.55),cell('Cửa Quảng Phúc: hai cánh cửa mở, bóng quân sau cửa',s_cua),cell('Đúc chuông: lửa lò, đồng nóng chảy, chuông treo',s_chuong),cell('Dựng thành: thợ khiêng gỗ, tường lên, hào nước',s_thanh,t=0.6),cell('Thái tử mặc áo tang đứng cạnh linh cữu trắng',s_tang)]
sheet(cells1,'/tmp/ly/demo/to2.png');sheet(cells2,'/tmp/ly/demo/to3.png')
