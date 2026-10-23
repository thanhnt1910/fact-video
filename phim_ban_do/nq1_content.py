"""Ngô Quyền và trận Bạch Đằng 938. Số câu 1–70 (n = 8001–8070). Bản đồ world7 (Quảng Châu – Giao Châu – vịnh Bắc Bộ).
Vị trí thành, Hải Môn và đường quân chỉ gần đúng. Bố cục theo quy tắc CLAUDE.md: không khung trích lời, đùa tối đa 3 giây, Q() ẩn ghi chú khi đánh nhau.
Hài chỉ nhắm vào phía Nam Hán và tình huống; không có khung đùa nào về Ngô Quyền, Dương Đình Nghệ hay nhân vật Việt."""
from build2 import T,D,TOTAL,chap,PH
import build2 as _B
import world7 as _W
INF=1e9
BASE=8000
def R(n,o=0): return T[BASE+n]+o
def E(n,o=0): return T[BASE+n]+D[BASE+n]+o
def at(n,sub,off=0.0):
    for r in PH.get(str(BASE+n),[]):
        c,s_,e_=r[:3]
        if sub.lower() in c.lower():
            if len(r)>=5:
                p=c.lower().index(sub.lower())/max(1,len(c));s_=r[3]+(r[4]-r[3])*p-0.1
            return T[BASE+n]+0.12+s_+off
    return T[BASE+n]+1.0+off
GR=(52,142,86);BL=(54,96,176);RD=(190,52,42);PU=(138,52,112);DK=(46,38,58);GD=(205,160,40)
TL=(40,140,150);BR=(150,100,60);OR=(200,110,40);GY=(110,110,110);OL=(110,130,50);BK=(60,60,60);YW=(214,176,40);NEU=(150,140,120)
NH=RD;VT=GR   # Nam Hán đỏ, Giao Châu (Việt) xanh lá
LOC={'Quảng Châu':(113.26,23.13,'big'),'Hải Môn':(109.20,21.45,'town'),'Đại La':(105.85,21.03,'big'),'Ái Châu':(105.78,19.80,'mid'),
     'Đường Lâm':(105.50,21.08,'town'),'Cổ Loa':(105.88,21.12,'mid'),'Nam Sách':(106.40,20.98,'town'),'Bạch Đằng':(106.82,20.90,'town')}
CITIES=dict(LOC)
CITY_SHOW={}
def show(name,a,b):
    CITY_SHOW.setdefault(name,[]).append((R(a,-1),E(b,1)))
CITY_OWN={}
def OW(name,col0,*steps):
    seq=[(0,col0)]
    for (n,o,c) in steps:
        seq.append((R(n,o),seq[-1][1]));seq.append((R(n,o+2.0),c))
    CITY_OWN[name]=seq
GROUPS=[];BATT=[];FIRES=[];FX=[];OBJ=[];LETTERS=[];ARROWS=[];NOTES=[];MARKS=[];CARDS3=[];QUOTES=[];JOKES=[];METERS=[];NUMS=[];TITLES=[]
REGIONS=[];RIVERS=[];ROUTES=[];TIDE=[];AMBIENT=[]
WATER=[('VỊNH BẮC BỘ',(108.3,20.0),26),('BIỂN ĐÔNG',(112.4,20.6),24)]
NIGHT=[(0,0)]
def nt(n,o0,o1): NIGHT.extend([(R(n,o0),0),(R(n,o0+1.6),0.55),(R(n,o1),0.55),(R(n,o1+1.6),0)])
def G(name,col,n,keys,show=None,**kw):
    GROUPS.append(dict(name=name,col=col,n=n,keys=keys,show=show or (keys[0][0]-0.3,keys[-1][0]+3),**kw))
QUIET=[]
def Q(a,b): QUIET.append((R(a,0),E(b,0)))
def NT(n,o,dur,lo,la,txt,col=DK): NOTES.append((R(n,o),min(R(n,o+min(dur,3.5)),E(n,-0.1)),lo,la,txt,col))
def C3(n,o,dur,name,role,col): CARDS3.append((R(n,o),min(R(n,o+dur),E(n,-0.2)),name,role,col))
def J(n,icon,text,off=1.2,dur=3.0): JOKES.append((R(n,off),min(E(n,-0.1),R(n,off)+dur),icon,text))
def NU(n,big,small,delay=1.2): NUMS.append((BASE+n,big,small,delay))
def AR(n,o,dur,a,b,col,txt): ARROWS.append((R(n,o),min(R(n,o+dur),E(n,-0.1)),a,b,col,txt))
def LET(n,o,dur,a,b,txt): LETTERS.append((R(n,o),R(n,o+dur),a,b,txt))
def SKULL(n,o,dur,lo,la,txt): MARKS.append((R(n,o),R(n,o+dur),lo,la,'skull',txt))
def X(name): return LOC[name][:2]
SCN=[]
def S(a,b,lo,la,z): SCN.append((a,b,lo,la,z))
def S2(a,b,pts,zmax=8.0,zmin=0.9):
    """Camera tự tính: các điểm cần thấy nằm trong vùng an toàn, chừa chỗ cho nhãn, phụ đề và bản đồ nhỏ."""
    px=lambda z:1920*z*_W.KX/_W.RW;py=lambda z:1920*z*_W.S/_W.RW
    los=[p_[0] for p_ in pts];las=[p_[1] for p_ in pts]
    dlo=max(los)-min(los);dla=max(las)-min(las)
    z=zmax
    if dlo>0: z=min(z,1200/(dlo*px(1)))
    if dla>0: z=min(z,440/(dla*py(1)))
    z=max(zmin,z)
    cx=(max(los)+min(los))/2+(960-775)/px(z)
    cy=max(las)-(432-330)/py(z)
    if dla==0: cy=las[0]-(432-470)/py(z)
    SCN.append((a,b,cx,cy,z))
def reg(name,lab,poly,c0,win,steps=(),alpha=34):
    seq=[(0,c0)]
    for (t,c) in steps: seq+=[(t,seq[-1][1]),(t+3,c)]
    REGIONS.append(dict(name=name,lab=lab,poly=poly,own=seq,alpha=alpha,win=(R(win[0],-1),E(win[1],1))))
L=LOC
P_NH=[(104.6,24.4),(108.0,24.6),(111.5,24.8),(116.4,24.6),(116.4,22.3),(112.0,21.7),(109.8,21.5),(108.2,21.9),(107.0,22.6),(105.8,23.3),(104.8,23.6)]
P_GC=[(103.6,22.4),(105.0,22.9),(106.7,22.6),(108.0,21.6),(107.4,20.95),(106.5,19.95),(105.0,19.6),(103.9,20.3),(103.5,21.4)]
TITLES.append((0.3,5.2,'NGÔ QUYỀN','TRẬN BẠCH ĐẰNG','năm 938'))
# ======================= CHƯƠNG 1: MỞ ĐẦU (1–4): đoàn thuyền Nam Hán tiến vào sông
S2(1,4,[X('Hải Môn'),(106.95,20.75)],2.4)
show('Hải Môn',1,4);show('Bạch Đằng',1,4)
reg('GIAO CHÂU',(105.4,22.0),P_GC,VT,(1,4),alpha=22)
G('Đoàn thuyền Nam Hán',NH,10,[(R(1,0),109.20,21.45),(R(2,0),107.9,20.9),(R(3,0),107.2,20.72),(R(4,4),106.92,20.80)],show=(R(1,0),E(4,0)),emb='tri',seed=811,kind='ship',spread=0.9,soff=(-40,30))
AMBIENT.append((R(1,0),E(4,0),'sea',0.4))
# ======================= CHƯƠNG 2: KHI NHÀ ĐƯỜNG MẤT (5–10)
S2(5,10,[X('Quảng Châu'),X('Đại La')],3.0)
show('Quảng Châu',5,18);show('Đại La',5,18)
reg('NAM HÁN',(110.5,24.0),P_NH,NH,(5,10),alpha=24);reg('GIAO CHÂU',(105.0,21.8),P_GC,VT,(5,10),alpha=24)
NU(5,'năm 907','nhà Đường mất',0.8)
C3(6,0.3,3.0,'Khúc Hạo','người bản xứ giữ Giao Châu',VT)
NT(7,0.4,3.2,109.5,23.4,'Lưu Nham lập nước Hán (Nam Hán), năm 917',NH)
G('Sứ Khúc Thừa Mỹ',VT,3,[(R(8,0),105.85,21.03),(R(8,6),108.5,22.2),(R(8,10),113.26,23.13)],show=(R(8,0),R(9,0)),emb='sun',seed=812,soff=(-20,40))
AR(10,0.3,3.0,X('Quảng Châu'),X('Đại La'),NH,'Nam Hán nổi giận')
# ======================= CHƯƠNG 3: MỘT CUỘC ĐÁNH ÚP VÀ MỘT NGƯỜI TRỞ VỀ (11–18)
S2(11,18,[X('Quảng Châu'),X('Ái Châu')],2.6)
reg('NAM HÁN',(110.5,24.0),P_NH,NH,(11,18),alpha=24);reg('GIAO CHÂU',(105.0,21.8),P_GC,VT,(11,18),alpha=24)
OW('Đại La',VT,(11,6.5,NH),(12,5.0,VT),(17,3.0,VT))
NU(11,'năm 923','Lý Khắc Chính đánh Giao Châu',0.6)
G('Quân Lý Khắc Chính',NH,12,[(R(11,0),113.26,23.13),(R(11,5),110.9,22.5),(R(11,9),108.3,22.3),(R(12,2),105.85,21.03),(R(12,6),105.85,21.03),(R(12,12),106.6,22.0),(R(13,4),108.5,22.3),(R(13,12),113.26,23.13)],show=(R(11,0),R(13,14)),emb='tri',seed=813,soff=(-60,-30),alive=[(0,1),(R(12,4),1),(R(12,10),0.2)])
G('Quân Dương Đình Nghệ',VT,12,[(0,105.78,19.80),(R(12,3),105.78,19.80),(R(12,8),105.85,21.03),(R(18,6),105.85,21.03)],show=(R(12,3),E(18,0)),emb='sun',seed=814,soff=(60,40))
C3(15,0.4,3.2,'Dương Đình Nghệ','tướng cũ của họ Khúc, người Ái Châu',VT)
NU(15,'năm 931','Dương Đình Nghệ lại đánh Nam Hán',0.6)
G('Quân Trần Bảo',NH,12,[(R(16,6),113.26,23.13),(R(17,0),110.9,22.5),(R(17,4),108.3,22.3),(R(17,8),106.6,21.7),(R(17,12),105.9,21.2),(R(18,2),105.9,21.2)],show=(R(16,6),E(18,0)),emb='tri',seed=815,soff=(-60,-30),alive=[(0,1),(R(17,10),1),(R(18,0),0.1)])
BATT.append((R(17,11),R(18,2),105.88,21.10,['Quân Trần Bảo','Quân Dương Đình Nghệ']))
NT(16,1.5,3.0,105.85,21.2,'Lý Tiến cho ngựa báo về Quảng Châu',NH)
NT(18,0.5,3.0,105.85,21.2,'Đình Nghệ tự xưng tiết độ sứ',VT)
# ======================= CHƯƠNG 4: NGƯỜI TƯỚNG Ở ÁI CHÂU (19–23)
S2(19,23,[X('Ái Châu'),X('Đại La')],4.2)
show('Ái Châu',19,23);show('Đại La',19,23);show('Đường Lâm',19,23)
reg('GIAO CHÂU',(104.8,21.9),P_GC,VT,(19,23),alpha=22)
C3(19,0.4,3.2,'Ngô Quyền','nha tướng của Dương Đình Nghệ',VT)
NT(20,0.4,3.0,105.50,21.25,'quê Đường Lâm',VT)
G('Ngô Quyền ở Ái Châu',VT,8,[(0,105.78,19.80)],show=(R(21,0),E(22,0)),emb='sun',seed=816,soff=(50,35),spread=0.5)
NT(21,3.0,3.0,105.78,19.95,'được gả con gái, giữ Ái Châu',VT)
NU(22,'năm 937','Kiều Công Tiễn giết chủ tướng',2.0)
SKULL(22,4.0,3.5,105.85,21.03,'Dương Đình Nghệ bị giết')
# ======================= CHƯƠNG 5: LỜI CẦU CỨU CỦA KẺ PHẢN CHỦ (24–33)
S2(24,25,[X('Ái Châu'),X('Quảng Châu')],2.2)
S2(26,33,[X('Quảng Châu'),X('Đại La'),(106.9,20.75)],2.4)
show('Quảng Châu',24,33);show('Đại La',24,33);show('Hải Môn',26,33);show('Ái Châu',24,25)
reg('NAM HÁN',(110.5,24.0),P_NH,NH,(24,33),alpha=24);reg('GIAO CHÂU',(105.0,21.8),P_GC,VT,(24,33),alpha=24)
NU(24,'cuối năm 938','Ngô Quyền đánh Kiều Công Tiễn',1.0)
G('Quân Ngô Quyền',VT,12,[(R(24,0),105.78,19.80),(R(24,7),105.85,21.03),(R(33,6),105.85,21.03)],show=(R(24,0),E(33,0)),emb='sun',seed=817,soff=(55,35))
LET(24,4.5,4.5,X('Đại La'),X('Quảng Châu'),'xin Nam Hán cứu')
C3(26,0.3,3.0,'Lưu Hoằng Tháo','con trai vua Nam Hán',NH)
G('Lưu Cung (đứng sau)',NH,6,[(R(28,0),113.26,23.13),(R(28,9),109.20,21.45),(R(48,0),109.20,21.45)],show=(R(28,0),E(48,0)),emb='tri',seed=818,kind='ship',soff=(-50,-35),spread=0.5)
G('Thuyền Hoằng Tháo',NH,10,[(R(26,2),113.26,23.13),(R(28,2),111.2,21.9),(R(31,0),109.20,21.45),(R(32,4),108.0,20.95),(R(33,6),107.1,20.72)],show=(R(26,2),E(33,0)),emb='tri',seed=819,kind='ship',spread=0.9,soff=(-95,75))
NT(26,3.2,3.0,113.2,23.3,'phong Giao Vương, vua của vùng chưa chiếm',NH)
J(27,'crown','Phong vua cho vùng đất chưa ai đặt chân tới',1.8)
C3(29,0.4,3.0,'Tiêu Ích','quan can ngăn Lưu Cung',NH)
J(33,'scroll','Vượt biển cứu một người không chờ nổi',2.5)
SKULL(33,0.4,3.2,105.85,21.03,'Kiều Công Tiễn bị giết')
AMBIENT.append((R(26,0),E(33,0),'sea',0.35));AMBIENT.append((R(31,0),E(31,5),'rain',0.35))
FX.append((R(28,6),R(28,9),'oars',X('Quảng Châu'),X('Hải Môn')))
FX.append((R(32,3),R(32,10),'drums',X('Hải Môn'),(107.0,20.75)))
# ======================= CHƯƠNG 6: CON SÔNG VÀ NƯỚC TRIỀU (34–40)
S(34,40,106.72,20.97,8.8*_W.RW/6031)
show('Bạch Đằng',34,40);show('Nam Sách',34,47)
reg('GIAO CHÂU',(106.2,21.5),P_GC,VT,(34,47),alpha=14)
for _w in ((R(1,0),E(4,2)),(R(33,0),E(48,0))): RIVERS.append(('SÔNG BẠCH ĐẰNG',[(106.40,21.10),(106.52,21.07),(106.63,21.01),(106.73,20.96),(106.82,20.91),(106.88,20.82),(106.93,20.72),(107.0,20.62)],7,(106.68,21.15),_w))
G('Ngô Quyền',VT,10,[(R(34,0),106.62,21.03),(R(34,6),106.62,21.03),(R(47,8),106.62,21.03)],show=(R(34,0),E(47,0)),emb='sun',seed=821,soff=(-190,-30),spread=0.6)
STK=[(106.69,20.985),(106.72,20.965),(106.745,20.955),(106.765,20.94),(106.785,20.93),(106.80,20.92),(106.815,20.905),(106.835,20.89),(106.70,20.96),(106.73,20.98),(106.76,20.955),(106.79,20.915),(106.82,20.925),(106.85,20.87)]
TIDE.append(([(106.60,21.03),(106.70,20.98),(106.80,20.92),(106.88,20.84),(106.92,20.75)],[(0,1.0),(R(43,0),1.0),(R(44,1),0.95),(R(45,3),0.08),(R(47,4),0.08),(R(48,2),0.7)],STK,(R(41,0),E(47,0)),R(37,2.0),(R(37,0),E(47,6))))
NT(35,0.4,3.0,106.78,21.0,'địch xa tới, đã mệt',NH)
NT(37,0.5,3.2,106.78,21.02,'cọc gỗ lớn, đầu nhọn bịt sắt',BR)
NT(38,0.3,3.2,106.76,21.0,'nước lên: cọc chìm dưới nước',BL)
NT(39,0.5,3.0,106.76,21.0,'cọc đóng ngầm ở cửa biển',BR)
AMBIENT.append((R(34,0),E(40,0),'sea',0.35))
FX.append((R(37,2),R(39,8),'crack',(106.76,20.95),(106.8,20.92)))
FX.append((R(40,0),E(41,0),'tide_up',(106.7,20.97),(106.9,20.8)))
# ======================= CHƯƠNG 7: TRẬN BẠCH ĐẰNG (41–47)
S(41,47,106.76,20.93,9.0*_W.RW/6031)
NU(41,'cuối năm 938','Trận Bạch Đằng',0.6)
G('Thuyền Nam Hán',NH,12,[(R(41,0),107.0,20.65),(R(42,2),106.92,20.74),(R(42,8),106.85,20.87),(R(43,2),106.78,20.94),(R(43,9),106.74,20.96),(R(44,1),106.74,20.96),(R(47,0),106.74,20.96)],show=(R(41,0),E(47,2)),emb='tri',seed=822,kind='ship',spread=0.9,soff=(-55,-20),alive=[(0,1),(R(45,0),1),(R(46,2),0.12)],defeats=[(R(46,3),'skull',E(47,6))])
G('Thuyền nhử',VT,5,[(R(41,0),106.66,21.01),(R(41,3),106.80,20.92),(R(41,6),106.86,20.86),(R(42,2),106.84,20.88),(R(42,8),106.66,21.01),(R(47,0),106.66,21.01)],show=(R(41,0),E(47,2)),emb='sun',seed=823,kind='ship',spread=0.6,soff=(-10,-90))
G('Thuyền Giao Châu',VT,8,[(R(44,0),106.60,21.03),(R(44,1),106.60,21.03),(R(44,5),106.70,20.99),(R(45,3),106.78,20.94),(R(47,0),106.80,20.93)],show=(R(44,0),E(47,2)),emb='sun',seed=824,kind='ship',spread=0.9,soff=(70,60))
J(42,'scroll','Địch chạy, thấy ngon ăn. Chẳng ai hỏi vì sao',1.6)
J(43,'glasses','Hóa ra không ai nhìn xuống nước',1.4)
FX.append((R(41,2),R(42,6),'oars',(106.8,20.92),(106.7,20.98)))
FX.append((R(44,0),R(44,3),'horn',(106.62,21.02),(106.76,20.95)))
FX.append((R(44,3),R(46,6),'drums',(106.62,21.02),(106.76,20.95)))
FX.append((R(44,0),E(45,0),'tide_down',(106.7,20.97),(106.9,20.8)))
FX.append((R(46,0.6),R(46,1.0),'crack',(106.76,20.95),(106.80,20.92)))
FX.append((R(46,2.2),R(46,2.6),'crack',(106.78,20.94),(106.82,20.90)))
FX.append((R(46,3.8),R(46,4.2),'splash',(106.78,20.94),(106.82,20.90)))
BATT.append((R(45,3.0),R(46,7.0),106.77,20.94,['Thuyền Nam Hán','Thuyền Giao Châu']))
SKULL(47,0.5,4.0,106.78,20.94,'Hoằng Tháo bị bắt và giết')
AMBIENT.append((R(41,0),E(47,6),'sea',0.45));AMBIENT.append((E(47,2),E(48,0),'gulls',0.2))
Q(44,47)
# ======================= CHƯƠNG 8: VUA NAM HÁN RÚT LUI (48–53)
S2(48,53,[X('Hải Môn'),(106.9,20.75)],2.6)
show('Hải Môn',48,53)
G('Lưu Cung rút quân',NH,6,[(R(48,4),109.20,21.45),(R(49,6),111.2,22.2),(R(49,12),113.26,23.13)],show=(R(48,4),E(49,2)),emb='tri',seed=825,kind='ship',soff=(-50,-35),spread=0.7)
reg('NAM HÁN',(110.5,24.0),P_NH,NH,(48,53),alpha=22)
J(49,'flag','Đi thì rầm rộ, về thì lặng lẽ',1.5)
AMBIENT.append((R(48,0),E(49,0),'sea',0.35))
# ======================= CHƯƠNG 9: XƯNG VƯƠNG Ở LOA THÀNH (54–59)
S2(54,59,[X('Cổ Loa'),X('Đường Lâm')],6.0)
show('Cổ Loa',54,59);show('Đường Lâm',54,59)
OW('Cổ Loa',VT)
C3(54,0.4,3.2,'Ngô Quyền','xưng vương năm 939',VT)
NU(55,'năm 939','Ngô Quyền xưng vương',1.0)
NT(55,3.0,3.0,105.88,21.30,'đặt trăm quan, định triều nghi',VT)
NU(59,'năm 944','Ngô Quyền mất',1.0)
# ======================= CHƯƠNG 10: SAU KHI NGÔ QUYỀN MẤT (60–65)
S2(60,65,[X('Cổ Loa'),X('Nam Sách')],4.2)
show('Cổ Loa',60,65);show('Nam Sách',60,65)
C3(61,0.4,3.0,'Dương Tam Kha','cướp ngôi năm 945',NEU)
NT(62,1.5,3.0,106.40,21.10,'Ngô Xương Ngập trốn về Nam Sách',VT)
G('Ngô Xương Ngập trốn',VT,3,[(R(62,1),105.88,21.12),(R(62,8),106.40,20.98),(E(65,0),106.40,20.98)],show=(R(62,1),E(65,0)),emb='sun',seed=826,soff=(-60,-55),spread=0.4)
# ======================= CHƯƠNG 11: KẾT (66–70)
S2(66,70,[X('Quảng Châu'),X('Ái Châu')],2.2)
show('Đại La',66,70);show('Quảng Châu',66,70)
reg('GIAO CHÂU',(105.0,21.8),P_GC,VT,(66,70),alpha=24);reg('NAM HÁN',(110.5,24.0),P_NH,NH,(66,70),alpha=22)
TITLES.append((R(70,0.2),E(70,1.5),'','',''))if False else None
# ======================= HOÀN TẤT
SCN.sort(key=lambda x:x[0])
CAM=[(0,SCN[0][2],SCN[0][3],SCN[0][4])]
for (a_,b_,lo,la,z) in SCN:
    CAM.append((R(a_)+1.6,lo,la,z));CAM.append((E(b_)-0.2,lo+0.01,la,z*1.03))
CAM=sorted(CAM,key=lambda k:k[0])
NIGHT.append((TOTAL,0));NIGHT=sorted(NIGHT,key=lambda k:k[0])
MINI=[(0,TOTAL)]
def gate_open(t): return 0
def year_of(n):
    m=n-BASE
    for a,b,y in [(1,4,938),(5,10,907),(11,14,923),(15,18,931),(19,23,937),(24,53,938),(54,58,939),(59,59,944),(60,65,945),(66,70,None)]:
        if a<=m<=b: return y
    return None
