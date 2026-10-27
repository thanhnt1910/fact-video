"""Lý Công Uẩn: từ cậu bé Cổ Pháp đến người dời đô (ly1). Số đoạn 1–134 (n = 18001–18134), BASE=18000.
Bố cục theo quy-tac/video-ban-do.md và mẫu lh6_content.py: không khung đùa, không khung trích lời, không nhạc nền, Q() ẩn ghi chú khi giao tranh.
Địa danh mức B (gần đúng): Kim Hoa, Nam Chiếu (ngoài mép bản đồ phía tây), Biện Sơn, Diễn Châu chỉ gần đúng."""
import os
from build2 import T,D,TOTAL,chap,PH
import build2 as _B
import world7 as _W
INF=1e9
BASE=18000
def _nx(n):
    while BASE+n not in T and n<400: n+=1
    return n
def _pv(n):
    while BASE+n not in T and n>0: n-=1
    return n
def R(n,o=0): n=_nx(n); return T[BASE+n]+o
def E(n,o=0): n=_pv(n); return T[BASE+n]+D[BASE+n]+o
def at(n,sub,off=0.0):
    n=_nx(n)
    for r in PH.get(str(BASE+n),[]):
        c,s_,e_=r[:3]
        if sub.lower() in c.lower():
            if len(r)>=5:
                p=c.lower().index(sub.lower())/max(1,len(c));s_=r[3]+(r[4]-r[3])*p-0.1
            return T[BASE+n]+0.12+s_+off
    txt=_B.texts[BASE+n].lower()
    p=txt.find(sub.lower())/max(1,len(txt)) if sub.lower() in txt else 0.2
    return T[BASE+n]+0.3+p*max(1.0,D[BASE+n]-0.8)+off
GR=(52,142,86);BL=(54,96,176);RD=(190,52,42);PU=(138,52,112);DK=(46,38,58);GD=(205,160,40)
BR=(150,100,60);GY=(110,110,110);NEU=(150,140,120)
LY=GR      # nhà Lý, quân của Lý Công Uẩn và triều đình mới
TL=BL      # nhà Tiền Lê
TG=RD      # nhà Tống
NC=PU      # Nam Chiếu
REB=(196,110,40)  # ba vị vương nổi loạn
LOC={'Cổ Pháp':(106.07,21.11,'mid'),'Hoa Lư':(105.90,20.28,'big'),'Đại La':(105.84,21.03,'big'),'Thăng Long':(105.84,21.03,'big'),
     'Ái Châu':(105.78,19.80,'mid'),'Cử Long':(105.47,20.22,'town'),'Diễn Châu':(105.58,19.05,'mid'),'Biện Sơn':(105.90,19.42,'town'),
     'Kim Hoa':(105.30,22.00,'town'),'Nam Chiếu':(104.55,22.55,'mid'),'Triều Tống':(110.80,24.60,'mid'),'Thọ Lăng':(106.05,21.07,'town')}
CITIES=dict(LOC)
CITY_SHOW={};CITY_OWN={}
def show(name,a,b): CITY_SHOW.setdefault(name,[]).append((R(a,-1),E(b,1)))
def show_t(name,t0,t1): CITY_SHOW.setdefault(name,[]).append((t0,t1))
def own(name,col0,*steps):
    seq=[(0,col0)]
    for (t,c) in steps: seq.append((t,seq[-1][1]));seq.append((t+2.0,c))
    CITY_OWN[name]=seq
GROUPS=[];BATT=[];FIRES=[];FX=[];OBJ=[];LETTERS=[];ARROWS=[];NOTES=[];MARKS=[];FACES=[];CARDS3=[];QUOTES=[];JOKES=[];METERS=[];NUMS=[];TITLES=[]
TABLES=[];REGIONS=[];RIVERS=[];ROUTES=[];TIDE=[];AMBIENT=[];PROPS=[]
WATER=[('VỊNH BẮC BỘ',(107.3,19.9),26)]
NIGHT=[(0,0)]
def night(t0,t1,a=0.55): NIGHT.extend([(t0,0),(t0+1.6,a),(t1,a),(t1+1.6,0)])
def G(name,col,n,keys,show=None,**kw):
    GROUPS.append(dict(name=name,col=col,n=n,keys=keys,show=show or (keys[0][0]-0.3,keys[-1][0]+3),**kw))
QUIET=[]
def Q(a,b): QUIET.append((R(a,0),E(b,0)))
def NT(n,o,dur,lo,la,txt,col=DK): NOTES.append((R(n,o),min(R(n,o+min(dur,3.5)),E(n,-0.1)),lo,la,txt,col))
FACEMAP={'Lý Công Uẩn lúc bé':('Cổ Pháp','child'),'Lý Khánh Văn':('Cổ Pháp','noble'),'Vạn Hạnh':('Cổ Pháp','servant'),'Lê Hoàn':('Hoa Lư','king'),
 'Lê Long Việt':('Hoa Lư','prince'),'Lê Long Đĩnh':('Hoa Lư','king'),'Lý Công Uẩn':('Hoa Lư','general'),'Nguyễn Đê':('Hoa Lư','general'),
 'Đào Cam Mộc':('Hoa Lư','noble'),'Lý Công Uẩn, vua':('Hoa Lư','king'),'Lý Phật Mã':('Hoa Lư','prince'),'Cao Biền':('Đại La','noble'),
 'Dực Thánh Vương':('Thăng Long','prince'),'Đông Chinh Vương':('Thăng Long','prince'),'Vũ Đức Vương':('Thăng Long','prince'),
 'Lý Nhân Nghĩa':('Thăng Long','servant'),'Lê Phụng Hiểu':('Thăng Long','general'),'Vua Tống':('Triều Tống','king')}
def C3(n,o,dur,name,role,col):
    CARDS3.append((R(n,o),min(R(n,o+dur),E(n,-0.2)),name,role,col))
    if name in FACEMAP:
        loc,kind=FACEMAP[name]
        FACE(n,o,dur,name,loc,kind,col)
def NU(n,big,small,delay=1.2): NUMS.append((BASE+n,big,small,delay))
def AR(n,o,dur,a,b,col,txt): ARROWS.append((R(n,o),min(R(n,o+dur),E(n,-0.1)),a,b,col,txt))
def LET(n,o,dur,a,b,txt): LETTERS.append((R(n,o),R(n,o+dur),a,b,txt))
def X(name): return LOC[name][:2]
def FACE(n,o,dur,name,loc,kind,col,dx=0,dy=0,t_min=None):
    s=R(n,o)
    if t_min is not None: s=max(s,t_min)
    FACES.append((s,min(max(R(n,o+dur),s+2.2),E(n,-0.1)))+X(loc)+(name,kind,col,dx,dy))
SCN=[]
def S2(a,b,pts,zmax=8.0,zmin=0.9,hmax=440):
    px=lambda z:1920*z*_W.KX/_W.RW;py=lambda z:1920*z*_W.S/_W.RW
    los=[p_[0] for p_ in pts];las=[p_[1] for p_ in pts]
    dlo=max(los)-min(los);dla=max(las)-min(las)
    z=zmax
    if dlo>0: z=min(z,1200/(dlo*px(1)))
    if dla>0: z=min(z,hmax/(dla*py(1)))
    z=max(zmin,z)
    cx=(max(los)+min(los))/2+(960-775)/px(z)
    cy=max(las)-(432-330)/py(z)
    if dla==0: cy=las[0]-(432-470)/py(z)
    SCN.append((a,b,cx,cy,z))
def reg(name,lab,poly,c0,win,steps=(),alpha=34):
    seq=[(0,c0)]
    for (t,c) in steps: seq+=[(t,seq[-1][1]),(t+3,c)]
    REGIONS.append(dict(name=name,lab=lab,poly=poly,own=seq,alpha=alpha,win=(R(win[0],-1),E(win[1],1))))
H=X('Hoa Lư');CP=X('Cổ Pháp');DL=X('Đại La');AC=X('Ái Châu');CL=X('Cử Long');DC=X('Diễn Châu');BS=X('Biện Sơn');KH=X('Kim Hoa');NCZ=X('Nam Chiếu');TT=X('Triều Tống');TL_=X('Thọ Lăng')
P_DV=[(105.05,22.40),(106.40,22.55),(107.70,21.60),(107.10,20.30),(106.20,19.75),(105.40,19.15),(104.70,19.85),(104.55,21.40)]
_ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
def PIC(a,b,fn,z0=1.0,z1=1.1):
    t0=R(a,0.2);t1=min(E(b,-0.3),t0+6.0)
    return (t0,t1,'pic',dict(path=os.path.join(_ROOT,'assets','anh_2d','LY1F',fn),z0=z0,z1=z1,dx=0,dy=0))
# ======================= CHƯƠNG 1: ĐỨA TRẺ BÊN NHÀ THIỀN SƯ (1–12)
TITLES.append((0.3,4.2,'LÝ CÔNG UẨN','NGƯỜI DỜI ĐÔ','Từ năm 974 đến năm 1028'))
show('Cổ Pháp',1,12);show('Hoa Lư',6,134)
own('Cổ Pháp',LY);own('Hoa Lư',TL,(R(39,0),LY))
S2(1,5,[CP],5.0)
S2(6,12,[CP,H],2.6,hmax=380)
reg('ĐẠI CỒ VIỆT',(105.55,21.55),P_DV,TL,(1,12),alpha=14)
NU(1,'năm 974','Lý Công Uẩn chào đời ở châu Cổ Pháp',3.6)
PROPS.append((R(1,3.8),R(1,6.8),'ping',CP[0],CP[1],'g',0.9))
C3(3,0.2,2.8,'Lý Công Uẩn lúc bé','sinh năm 974',LY)
C3(4,0.5,3.0,'Lý Khánh Văn','thiền sư, cha nuôi',LY)
NU(6,'năm 980','Lê Hoàn lên thay nhà Đinh',0.8)
C3(6,3.0,2.8,'Lê Hoàn','mở triều Tiền Lê',TL)
C3(7,0.3,3.0,'Vạn Hạnh','sư ở chùa Lục Tổ',LY)
PROPS.append((R(10,0.3),E(10,0),'pennants',H[0]+0.12,H[1]+0.10,'g',0.45))
# ======================= CHƯƠNG 2: NGƯỜI GIỮ CUNG NHÀ LÊ (13–26)
S2(13,26,[H],5.0)
reg('ĐẠI CỒ VIỆT',(105.55,21.55),P_DV,TL,(13,26),alpha=14)
NU(14,'năm 1005','Lê Hoàn mất, các con tranh ngôi',0.8)
PROPS.append((R(14,0.3),E(15,0),'hall',H[0],H[1]+0.075,'',0.45))
C3(16,0.3,2.8,'Lê Long Việt','lên ngôi ba ngày',TL)
C3(16,3.2,2.6,'Lê Long Đĩnh','giết anh, lên thay',TL)
FX.append((at(16,'giết'),at(16,'giết',1.6),'gong',H,H))
C3(19,0.3,2.8,'Lý Công Uẩn','chỉ huy quân bảo vệ vua',LY)
INTER=[]
INTER.append(PIC(21,21,'018.jpg',1.0,1.08))
NU(25,'năm 1009','Lê Long Đĩnh qua đời',0.4)
# ======================= CHƯƠNG 3: LỜI NÓI KHÍCH VÀ NGÔI VUA (27–47)
S2(27,47,[H],6.2)
G('Năm trăm quân của Lý Công Uẩn',LY,10,[(R(27,0),105.82,20.24),(R(27,3.0),105.86,20.27),(E(47,0),105.86,20.27)],show=(R(27,0),E(47,0)),emb='sun',seed=1801,spread=0.5,soff=(-70,20),label=False)
G('Năm trăm quân của Nguyễn Đê',TL,10,[(R(27,0),105.98,20.24),(R(27,3.0),105.94,20.27),(E(39,0),105.94,20.27)],show=(R(27,0),E(39,0)),emb='circle',seed=1802,spread=0.5,soff=(70,20),label=False)
C3(27,0.4,2.8,'Nguyễn Đê','chỉ huy năm trăm quân',TL)
C3(29,0.2,2.8,'Đào Cam Mộc','quan hầu cận',LY)
PROPS.append((R(30,0.3),E(31,0),'meeting',H[0],H[1]+0.02,'',0.5))
PROPS.append((R(36,0.3),E(38,0),'hall',H[0],H[1]+0.03,'',0.8))
NU(39,'năm 1009','Lý Công Uẩn lên ngôi',0.6)
FX.append((at(39,'chính điện'),at(39,'chính điện',2.0),'trumpet',H,H))
C3(39,3.2,2.8,'Lý Công Uẩn, vua','lập nhà Lý',LY)
FX.append((at(40,'vạn tuế'),at(40,'vạn tuế',1.8),'gong',H,H))
NT(41,0.5,3.2,H[0],H[1]-0.42,'nhà Tiền Lê mất ngôi, nhà Lý bắt đầu',LY)
C3(43,0.3,2.8,'Lý Phật Mã','thái tử',LY)
PROPS.append((R(44,0.3),E(45,0),'seal',H[0]+0.02,H[1]-0.12,'',0.6))
# ======================= CHƯƠNG 4: HOA LƯ KHÔNG CÒN ĐỦ (48–55)
S2(48,55,[H],5.4)
NT(48,0.4,3.2,H[0],H[1]-0.42,'Hoa Lư: núi đá dựng đứng bao quanh',BR)
TABLES.append((R(52,0.2),min(E(52,-0.2),R(52,0.2)+6.5),'Vì sao ông muốn dời kinh đô',[
 ('Hoa Lư','Ẩm thấp, chật hẹp; núi đá bó chặt, khó mở rộng.'),
 ('Hai triều trước','Đều đóng đô ở Hoa Lư và đều ngắn ngủi.')]))
NT(55,0.4,3.2,H[0],H[1]-0.42,'nhà Đinh hai vua, nhà Tiền Lê ba vua, hai mươi chín năm',TL)
# ======================= CHƯƠNG 5: ĐẠI LA BÊN SÔNG (56–63)
S2(56,63,[H,DL],3.0,hmax=380)
show('Đại La',56,74)
own('Đại La',NEU)
RIVERS.append(('SÔNG HỒNG',[(105.55,21.30),(105.68,21.18),(105.80,21.10),(105.90,21.00),(106.00,20.90),(106.12,20.78)],5,(106.22,20.70),(R(56,0),E(75,0))))
NU(57,'năm 866','Cao Biền đắp thành Đại La',0.8)
C3(57,3.4,3.0,'Cao Biền','tướng nhà Đường',NEU)
PROPS.append((R(58,0.3),E(58,0),'hall',DL[0],DL[1]+0.025,'',0.55))
PROPS.append((R(60,0.3),R(60,3.3),'ping',DL[0],DL[1],'g',0.9))
G('Thuyền bè cập bến Đại La',LY,6,[(R(60,0),106.10,20.80),(R(60,4.0),105.88,21.00),(E(61,0),105.88,21.00)],kind='ship',show=(R(60,0),E(61,0)),emb='sun',seed=1803,spread=0.5,soff=(40,10),label=False)
# ======================= CHƯƠNG 6: LÁ CHIẾU DỜI ĐÔ (64–71)
S2(64,71,[H,DL,CP],2.2,hmax=400)
NU(64,'năm 1010','Về thăm Cổ Pháp, rồi viết chiếu dời đô',0.6)
show('Cổ Pháp',64,64)
G('Đoàn vua về Cổ Pháp',LY,6,[(R(64,0),H[0],H[1]),(R(64,5.0),CP[0]-0.03,CP[1]-0.04),(E(64,0),CP[0]-0.03,CP[1]-0.04)],kind='cav',show=(R(64,0),E(64,0)),emb='sun',seed=1804,spread=0.4,soff=(-40,10),label=False)
G('Sứ sang nhà Tống',LY,4,[(R(65,0.5),DL[0],DL[1]),(R(65,5.5),TT[0],TT[1]),(E(65,0),TT[0],TT[1])],kind='cav',show=(R(65,0.3),E(65,0)),emb='sun',seed=1805,spread=0.3,soff=(30,0),label=False)
LET(66,0.4,4.5,H,DL,'bản chiếu dời đô')
NT(68,0.4,3.2,DL[0],DL[1]-0.22,'Đại La: rồng cuộn hổ ngồi, rộng mà bằng phẳng',LY)
PROPS.append((R(69,0.3),E(69,0),'scrolls2',DL[0]+0.06,DL[1]+0.06,'',0.5))
PROPS.append((R(70,0.3),R(70,3.3),'meeting',H[0]+0.02,H[1]+0.02,'',0.55))
# ======================= CHƯƠNG 7: CON THUYỀN DƯỚI CHÂN THÀNH (72–75)
S2(72,75,[H,DL],3.0,hmax=400)
NU(72,'năm 1010','Nhà vua rời Hoa Lư, đi thuyền ra Đại La',0.6)
G('Thuyền vua ra Đại La',LY,8,[(R(72,0.5),H[0]+0.02,H[1]+0.05),(R(72,6.5),106.10,20.80),(R(73,0.0),105.95,20.93),(R(73,0.2),105.88,21.00),(E(75,0),105.88,21.00)],kind='ship',show=(R(72,0.5),E(75,0)),emb='sun',seed=1806,spread=0.5,soff=(30,15),label=False)
INTER.append(PIC(73,73,'017.jpg',1.0,1.1))
FX.append((at(75,'Thăng Long'),at(75,'Thăng Long',1.6),'trumpet',DL,DL))
show_t('Thăng Long',R(75,-1),R(134,1))
NU(75,'Thăng Long','nghĩa là rồng bay lên',0.2)
# ======================= CHƯƠNG 8: BỐN CÁNH CỬA VÀ CÁC ĐIỆN (76–86)
S2(76,86,[DL],8.0)
PROPS.append((R(76,0.3),E(76,0),'hall',DL[0],DL[1]+0.012,'',0.8))
PROPS.append((R(77,0.3),E(77,0),'hall',DL[0],DL[1]+0.02,'',0.6))
PROPS.append((R(78,0.3),E(78,0),'granary',DL[0]-0.02,DL[1]+0.004,'',0.5))
show('Thăng Long',76,134)
NT(82,0.3,3.5,DL[0],DL[1]-0.42,'Cổ Pháp thành phủ Thiên Đức, Hoa Lư thành phủ Trường Yên',BR)
NU(83,'năm 1011','Xây cung Thúy Hoa, miễn thuế ba năm',0.6)
PROPS.append((R(84,0.3),E(84,0),'granary',DL[0]+0.02,DL[1]-0.01,'',0.5))
PROPS.append((R(85,0.3),E(85,0),'seal',DL[0]+0.03,DL[1]+0.03,'',0.6))
G('Sứ Tống phong vương',TG,5,[(R(85,0.0),TT[0],TT[1]),(R(85,5.5),DL[0]+0.02,DL[1]+0.03),(E(86,0),DL[0]+0.02,DL[1]+0.03)],kind='cav',show=(R(85,0),E(86,0)),emb='tri',seed=1807,spread=0.3,soff=(25,0),label=False)
# ======================= CHƯƠNG 9: NHỮNG NĂM TRỊ VÌ (87–106)
S2(87,88,[DL,H,AC],2.3,hmax=420)
NU(88,'năm 1010','Đổi mười đạo thành hai mươi bốn lộ',0.6)
reg('ĐẠI CỒ VIỆT',(105.55,21.55),P_DV,LY,(87,106),alpha=16)
S2(89,91,[DL,AC,CL],2.6,hmax=440)
show('Ái Châu',89,91);show('Cử Long',89,91)
G('Quân đi đánh giặc Cử Long',LY,10,[(R(89,0),DL[0],DL[1]),(R(89,5.0),105.80,20.30),(R(90,2.0),105.62,20.18),(R(91,0),105.52,20.20),(E(91,0),105.52,20.20)],show=(R(89,0),E(91,0)),emb='sun',seed=1808,spread=0.6,soff=(-35,10),label=True)
G('Giặc Cử Long',NEU,8,[(R(90,0),105.42,20.24),(E(91,0),105.42,20.24)],show=(R(90,0),E(91,0)),emb='circle',seed=1809,spread=0.6,soff=(-35,-20),defeats=[(at(91,'giặc tan'),'flag',E(91,0))])
BATT.append((R(91,0.0),E(91,-0.2),105.48,20.22,['Quân đi đánh giặc Cử Long','Giặc Cử Long']))
FIRES.append((at(91,'đốt'),E(91,0),105.43,20.25))
NT(90,0.4,3.0,CL[0],CL[1]-0.3,'hai triều trước không đánh nổi giặc này',GY)
Q(91,91)
S2(92,96,[AC,DC,BS],2.8,hmax=440)
show('Diễn Châu',92,96);show('Biện Sơn',92,96);show('Triều Tống',102,102);show('Triều Tống',85,86)
G('Thuyền đi đánh Diễn Châu',LY,10,[(R(92,0),DL[0],DL[1]),(R(92,5.5),105.95,19.30),(R(92,7.5),105.68,19.12),(R(93,0.3),105.68,19.12),(R(93,3.2),BS[0]-0.02,BS[1]-0.03),(E(96,0),BS[0]-0.02,BS[1]-0.03)],kind='ship',show=(R(92,0),E(96,0)),emb='sun',seed=1810,spread=0.6,soff=(75,-45),label=False)
FX.append((at(93,'tối sầm'),at(93,'tối sầm',3.0),'sea',BS,BS))
C3(94,0.3,3.0,'Lý Công Uẩn, vua','đốt hương khấn trời',LY)
FACEMAP['Lý Công Uẩn, vua']=('Biện Sơn','king')
AMBIENT.append((at(93,'tối sầm')-0.3,E(95,0),'rain',0.45))
S2(97,97,[DL],5.0)
NU(97,'năm 1013','Định sáu loại thuế',0.6)
S2(98,102,[KH,DL,NCZ],2.0,hmax=440)
show('Kim Hoa',98,101);show('Nam Chiếu',98,100)
NU(98,'năm 1014','Quân Nam Chiếu vào cướp',0.6)
G('Quân Nam Chiếu',NC,12,[(R(98,0),NCZ[0],NCZ[1]),(R(98,6.5),KH[0]+0.28,KH[1]-0.08),(R(100,0),KH[0]+0.28,KH[1]-0.08),(E(101,0),KH[0]+0.28,KH[1]-0.08)],kind='cav',show=(R(98,0),E(101,0)),emb='tri',seed=1811,spread=0.8,soff=(-30,10),
  defeats=[(at(100,'thắng lớn'),'flag',E(101,0))])
PROPS.append((R(99,0.5),E(99,0),'camp',KH[0]+0.05,KH[1]+0.02,'r',0.4))
C3(100,0.3,2.8,'Dực Thánh Vương','tướng nhà Lý',LY)
G('Quân Dực Thánh Vương',LY,10,[(R(100,0),DL[0],DL[1]),(R(100,6.0),105.40,21.80),(E(101,0),105.40,21.80)],show=(R(100,0),E(101,0)),emb='sun',seed=1812,spread=0.6,soff=(30,15),label=False)
BATT.append((at(100,'thắng lớn')-1.0,E(101,-0.3),KH[0]+0.22,KH[1]-0.06,['Quân Dực Thánh Vương','Quân Nam Chiếu']))
FX.append((at(100,'thắng lớn')-1.0,at(100,'thắng lớn',2.8),'drums',DL,KH))
Q(100,101)
G('Sứ mang ngựa biếu nhà Tống',LY,5,[(R(102,0),DL[0],DL[1]),(R(102,6.0),TT[0],TT[1]),(E(102,0),TT[0],TT[1])],kind='cav',show=(R(102,0),E(102,0)),emb='sun',seed=1813,spread=0.4,soff=(30,0),label=False)
PROPS.append((R(102,4.0),E(102,0),'seal',TT[0]-0.1,TT[1]-0.35,'',0.6))
S2(103,106,[DL],5.2)
PROPS.append((R(104,0.3),E(104,0),'hall',DL[0]-0.012,DL[1]+0.03,'',0.55))
PROPS.append((R(104,0.5),E(104,0),'scrolls2',DL[0]+0.04,DL[1]+0.02,'',0.5))
NU(106,'năm 1015','Đào Cam Mộc qua đời',0.6)
PROPS.append((R(106,3.0),E(106,0),'tomb',DL[0]-0.05,DL[1]-0.03,'',0.7))
# ======================= CHƯƠNG 10: ĐIỆN LONG AN (107–112)
S2(107,112,[DL,CP],3.2,hmax=400)
NU(107,'mười tám năm','kể từ ngày dời đô',0.6)
PROPS.append((R(107,0.3),R(107,3.3),'ping',DL[0],DL[1],'g',0.9))
PROPS.append((R(108,0.3),E(108,0),'meeting',DL[0],DL[1]+0.02,'',0.55))
NU(109,'năm 1028','Lý Công Uẩn không khỏe',0.6)
FX.append((R(110,1.2),R(110,4.0),'drums',DL,DL))
PROPS.append((R(111,0.3),E(111,0),'hall',DL[0]-0.01,DL[1]+0.028,'',0.65))
show('Thọ Lăng',112,112)
PROPS.append((R(112,3.0),E(112,0),'tomb',TL_[0],TL_[1],'',0.7))
FX.append((R(112,3.0),R(112,5.0),'gong',TL_,TL_))
# ======================= CHƯƠNG 11: CÁNH CỬA QUẢNG PHÚC (113–126)
S2(113,126,[DL],8.0)
reg('ĐẠI CỒ VIỆT',(105.55,21.55),P_DV,LY,(113,134),alpha=14)
C3(115,0.2,2.6,'Đông Chinh Vương','giấu quân trong thành',REB)
C3(115,2.8,2.6,'Dực Thánh Vương','giấu quân trong thành',REB)
C3(115,5.4,2.6,'Vũ Đức Vương','giấu quân trong thành',REB)
G('Quân ba vương mai phục',REB,10,[(R(114,0),DL[0]-0.05,DL[1]+0.012),(R(115,0),DL[0]-0.04,DL[1]+0.012),(E(123,0),DL[0]-0.04,DL[1]+0.012)],show=(R(114,0),E(123,0)),emb='circle',seed=1814,spread=0.45,soff=(-70,45),
  defeats=[(at(123,'thua chạy'),'flag',E(123,0))],label=False)
G('Đoàn thái tử',LY,6,[(R(116,0),DL[0]+0.075,DL[1]+0.01),(R(116,4.0),DL[0]+0.034,DL[1]+0.004),(R(117,1.0),DL[0]+0.004,DL[1]+0.012),(E(125,0),DL[0]+0.004,DL[1]+0.012)],show=(R(116,0),E(125,0)),emb='sun',seed=1815,spread=0.4,soff=(40,10),label=False)
C3(116,0.3,2.8,'Lý Phật Mã','thái tử',LY)
PROPS.append((R(117,0.3),E(117,0),'hall',DL[0]+0.004,DL[1]+0.02,'',0.6))
G('Lính canh trong cung',LY,10,[(R(120,0),DL[0]+0.004,DL[1]+0.012),(at(120,'xông ra'),DL[0]-0.012,DL[1]+0.012),(E(123,0),DL[0]-0.02,DL[1]+0.012)],show=(R(120,0),E(123,0)),emb='sun',seed=1816,spread=0.45,soff=(45,-15),label=False)
C3(120,0.3,2.6,'Lý Nhân Nghĩa','nội thị',LY)
BATT.append((at(120,'xông ra'),E(122,-0.1),DL[0]-0.03,DL[1]+0.012,['Lính canh trong cung','Quân ba vương mai phục']))
FX.append((at(120,'xông ra'),at(120,'xông ra',3.5),'drums',DL,DL))
C3(121,0.2,2.8,'Lê Phụng Hiểu','tướng nhà Lý',LY)
Q(120,123)
FX.append((at(126,'Thái Tông'),at(126,'Thái Tông',1.8),'gong',DL,DL))
NU(126,'năm 1028','Thái tử lên ngôi, tức vua Lý Thái Tông',0.6)
# ======================= CHƯƠNG 12: KẾT (127–134)
S2(127,134,[DL,H],2.4,hmax=400)
INTER.append((R(129,0.2),min(E(131,-0.3),R(129,0.2)+14.0),'timeline',{'head':'Lý Công Uẩn và kinh đô mới','nodes':[
 ('1009','Được tôn lên ngôi, không có trận đánh nào'),
 ('1010','Dời đô từ Hoa Lư ra Đại La, đổi tên Thăng Long'),
 ('1028','Mất; thái tử Lý Phật Mã lên ngôi')]}))
PROPS.append((R(133,0.3),R(133,3.3),'ping',DL[0],DL[1],'g',0.9))
PROPS.append((R(134,0.3),R(134,3.5),'ping',DL[0],DL[1],'g',0.9))
# ======================= TIỂU CẢNH (phóng vào từ điểm bản đồ, như cảnh cày tịch điền của Lê Hoàn; chỉ ở các mốc chính)
FOC=[]
def SC(a,b,kind,pt,sc=1.0,o0=0.2):
    PROPS.append((R(a,o0),E(b,0),kind,pt[0],pt[1],'',sc));FOC.append((a,b,[pt],True))
FOC.append((6,6,[H],True))
SC(4,4,'canh_chua',CP)
SC(24,24,'canh_ngoa_trieu',H)
SC(40,40,'canh_van_tue',H)
SC(60,60,'canh_ben_song',DL)
SC(79,79,'canh_thang_long',DL)
SC(93,96,'canh_khan',BS)
SC(110,110,'canh_nhat_thuc',DL)
SC(121,122,'canh_cua_tay',DL)
# ======================= HOÀN TẤT
AMBIENT.extend([(R(1,0),E(12,0),'wind',0.3),(R(27,0),E(47,0),'crowd',0.25),(R(60,0),E(75,0),'sea',0.25),(R(76,0),E(86,0),'crowd',0.2),(R(113,0),E(126,0),'crowd',0.3),(R(127,0),TOTAL-1,'wind',0.3)])
SCN.sort(key=lambda x:x[0])
CAM=[(0,SCN[0][2],SCN[0][3],SCN[0][4])]
for (a_,b_,lo,la,z) in SCN:
    CAM.append((R(a_)+1.6,lo,la,z));CAM.append((E(b_)-0.2,lo+0.01,la,z*1.03))
CAM=sorted(CAM,key=lambda k:k[0])
GRADE={'sat':0.62,'tint':(188,212,232),'amt':0.8,'gain':0.97,'vig':0.6}
NIGHT.append((TOTAL,0));NIGHT=sorted(NIGHT,key=lambda k:k[0])
MINI=[(0,TOTAL)]
QUIET_AUDIO=True
FLAG2=True  # lính cầm cờ trong cụm quân thay cờ đơn giản
CAMFOCUS=True
MUSIC=[]
def gate_open(t): return 0
def year_of(n):
    m=n-BASE
    for a,b,y in [(1,5,974),(6,12,980),(13,15,1005),(16,26,1009),(27,47,1009),(48,71,1010),(72,86,1010),(87,102,1011),(103,106,1015),(107,112,1028),(113,134,1028)]:
        if a<=m<=b: return y
    return None
NO_GROUP_LABEL=True
SIDES=[('Nhà Lý',LY,{g['name'].strip() for g in GROUPS if g['col']==LY}),('Nhà Tiền Lê',TL,{g['name'].strip() for g in GROUPS if g['col']==TL}),
       ('Nhà Tống',TG,{g['name'].strip() for g in GROUPS if g['col']==TG}),('Nam Chiếu',NC,{g['name'].strip() for g in GROUPS if g['col']==NC}),
       ('Ba vị vương',REB,{g['name'].strip() for g in GROUPS if g['col']==REB}),('Địa phương',NEU,{g['name'].strip() for g in GROUPS if g['col']==NEU})]
SFX=[(R(40,0.2),'trumpet'),(R(85,0.2),'horn'),(R(112,3.0),'gong')]
SFX_GROUPS=['Sứ Tống phong vương','Sứ mang ngựa biếu nhà Tống','Sứ sang nhà Tống','Đoàn vua về Cổ Pháp','Thuyền vua ra Đại La','Thuyền đi đánh Diễn Châu']
_s0=at(93,'tối sầm')-0.3
for _m in range(int(_s0/2.6)+1,int(E(95,0)/2.6)+1): SFX.append((_m*2.6+0.45,'thunder'))
