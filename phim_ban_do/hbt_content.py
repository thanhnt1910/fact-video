"""Hai Bà Trưng (năm 40–43). Số đoạn 1–73 (n = 9001–9073). Bản đồ world7 (Lĩnh Nam: Quảng Châu – Giao Châu – vịnh Bắc Bộ).
Vị trí thành, Lãng Bạc, Cấm Khê và đường quân chỉ gần đúng (nhãn "ước lượng"). Bố cục theo CLAUDE.md: không khung trích lời, đùa tối đa 3 giây, Q() ẩn ghi chú khi đánh nhau.
Khung đùa chỉ nhắm vào phía nhà Hán và tình huống; không có khung đùa nào về Hai Bà Trưng hay nhân vật Việt.
Bảng ánh xạ đoạn → câu kịch bản: xem ke-hoach/hai-ba-trung-kich-ban.md (73 đoạn gộp từ 145 câu)."""
from build2 import T,D,TOTAL,chap,PH
import build2 as _B
import world7 as _W
INF=1e9
BASE=9000
_B.ERA=''   # năm ghi kèm TCN/SCN trong year_of
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
NH=RD;VT=GR;NV=BL   # nhà Hán đỏ, Nam Việt (Triệu Đà) xanh dương, người Việt / Hai Bà Trưng xanh lá
LOC={'Phiên Ngung':(113.26,23.13,'big'),'Thạch Môn':(113.12,23.50,'town'),'Hợp Phố':(109.35,21.65,'mid'),'Mê Linh':(105.72,21.20,'big'),'Luy Lâu':(106.10,21.03,'town'),
     'Chu Diên':(105.80,20.62,'town'),'Cửu Chân':(105.78,19.80,'mid'),'Nhật Nam':(106.55,18.55,'mid'),'Lãng Bạc':(106.05,21.12,'town'),'Cấm Khê':(105.35,21.05,'town'),
     'Cư Phong':(105.45,19.45,'town'),'Hát Giang':(105.52,21.16,'town')}
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
    if dla>0: z=min(z,320/(dla*py(1)))
    z=max(zmin,z)
    cx=(max(los)+min(los))/2+(960-775)/px(z)
    cy=max(las)-(432-300)/py(z)
    if dla==0: cy=las[0]-(432-470)/py(z)
    SCN.append((a,b,cx,cy,z))
def reg(name,lab,poly,c0,win,steps=(),alpha=34):
    seq=[(0,c0)]
    for (t,c) in steps: seq+=[(t,seq[-1][1]),(t+3,c)]
    REGIONS.append(dict(name=name,lab=lab,poly=poly,own=seq,alpha=alpha,win=(R(win[0],-1),E(win[1],1))))
def P(a,b,pts,o0=0.6,o1=-0.6):
    """Đường đi đều đặn từ đầu đoạn a đến cuối đoạn b (không phụ thuộc độ dài giọng)."""
    t0=R(a,o0);t1=E(b,o1);k=len(pts)-1
    return [(t0+(t1-t0)*i/k,p_[0],p_[1]) for i,p_ in enumerate(pts)]
L=LOC
# Vùng (màu thể hiện bên nào cai quản). Đa giác gần đúng.
P_NV=[(104.0,24.4),(108.0,24.7),(111.5,24.8),(116.3,24.6),(116.3,22.4),(112.0,21.6),(109.8,21.5),(108.0,21.2),(107.4,20.95),(106.5,19.95),(105.0,19.6),(103.9,20.3),(103.5,21.4),(103.6,22.4),(104.6,23.6)]
P_GC=[(103.6,22.4),(105.0,22.9),(106.7,22.6),(108.0,21.6),(107.4,20.95),(106.5,19.95),(105.0,19.6),(103.9,20.3),(103.5,21.4)]
P_LN=P_NV  # vùng Lĩnh Nam dưới thời Hai Bà
P_NL=[(109.5,24.9),(116.3,24.9),(116.3,24.4),(113.0,24.35),(109.5,24.45)]   # dãy Ngũ Lĩnh (mép bắc bản đồ)
TITLES.append((0.3,3.8,'HAI BÀ TRƯNG','NỔI DẬY NĂM 40','sau Công nguyên'))
# ======================= CHƯƠNG 1: MỞ ĐẦU (1–4): viên quan bỏ chạy
S2(1,2,[X('Mê Linh'),(108.0,22.6)],3.2)
S2(3,4,[X('Mê Linh'),X('Phiên Ngung')],2.6)
show('Mê Linh',1,4);show('Luy Lâu',1,2)
reg('GIAO CHỈ',(105.2,22.2),P_GC,NH,(1,2),alpha=22)
reg('LĨNH NAM',(110.0,23.6),P_LN,NH,(2,4),steps=[(R(2,3.0),VT)],alpha=22)
G('Thái thú chạy về nước',NH,5,P(1,2,[X('Luy Lâu'),(106.6,21.9),(108.2,23.0),(110.2,24.3)],0.3,-0.2),show=(R(1,0),E(2,0)),emb='tri',seed=901,soff=(-30,-30),spread=0.7)
G('Quân hai bà',VT,12,[(R(2,0),105.72,21.20),(E(4,0),105.72,21.20)],show=(R(2,0),E(4,0)),emb='sun',seed=902,soff=(45,30),spread=0.6)
AR(3,0.5,3.5,(112.6,24.7),X('Mê Linh'),NH,'nhà Hán sai tướng đến')
# ======================= CHƯƠNG 2: TRIỆU ĐÀ (5–10)
S2(5,10,[X('Phiên Ngung'),X('Cửu Chân')],2.7)
show('Phiên Ngung',5,10);show('Mê Linh',8,10);show('Cửu Chân',8,10)
reg('NAM VIỆT',(110.2,23.9),P_NV,NV,(5,10),alpha=22)
NU(5,'207 TCN','nhà Tần suy yếu',0.5)
C3(6,0.6,3.2,'Triệu Đà','người phương bắc, chiếm Lĩnh Nam',NV)
NU(7,'207 TCN','Triệu Đà xưng Nam Việt Vương',0.5)
NT(7,2.5,3.2,113.3,23.5,'kinh đô ở Phiên Ngung, nay là Quảng Châu',NV)
G('Sứ Triệu Đà',NV,3,P(8,8,[X('Phiên Ngung'),(109.0,22.2),X('Mê Linh')],0.5,-0.2),show=(R(8,0),E(8,0)),emb='dia',seed=903,soff=(-20,30),spread=0.5)
LET(9,1.0,4.0,(112.6,24.7),X('Phiên Ngung'),'vua Hán phong cho Triệu Đà')
NU(9,'196 TCN','nhà Hán phong Triệu Đà làm Nam Việt Vương',0.4)
# ======================= CHƯƠNG 3: THÁI HẬU HỌ CÙ VÀ LỮ GIA (11–22)
S2(11,22,[X('Phiên Ngung'),(112.4,24.5)],4.6)
show('Phiên Ngung',11,22)
reg('NAM VIỆT',(110.2,23.9),P_NV,NV,(11,22),alpha=18)
C3(11,0.6,3.0,'Triệu Minh Vương','từng làm con tin ở nhà Hán',NV)
C3(12,0.6,3.0,'Ai Vương','vua trẻ, mẹ là người Hán',NV)
C3(14,0.4,3.2,'Lữ Gia','tể tướng ba đời vua',NV)
NT(13,0.6,3.2,113.3,23.5,'bỏ cửa ải, ba năm chầu vua Hán một lần',NV)
LET(17,0.5,3.6,(112.6,24.7),X('Phiên Ngung'),'vua Hán nghe tin')
C3(18,0.4,3.0,'Hàn Thiên Thu','tướng cũ của nhà Hán',NH)
J(19,'scroll','Hứa ba trăm người, mang hai nghìn cho chắc ăn',2.0)
G('Quân Hàn Thiên Thu',NH,12,P(19,21,[(112.4,24.7),(112.7,24.1),(113.0,23.65),(113.05,23.5)],0.5,-1.0),show=(R(19,0),E(21,0)),emb='tri',seed=904,soff=(-45,-35),spread=0.8)
G('Quân Lữ Gia',NV,12,P(20,21,[X('Phiên Ngung'),(113.2,23.4),(113.05,23.48)],0.5,-1.0),show=(R(20,0),E(21,0)),emb='dia',seed=905,soff=(40,40),spread=0.8,alive=[(0,1),(R(21,6),1)])
BATT.append((R(21,3.5),R(21,9),113.05,23.5,['Quân Hàn Thiên Thu','Quân Lữ Gia']))
Q(21,21)
NT(22,0.5,3.0,112.4,24.4,'nhà Hán sẽ đáp trả bằng đạo quân lớn hơn',NH)
# ======================= CHƯƠNG 4: NHÀ HÁN CHIẾM NAM VIỆT (23–30)
S2(23,28,[X('Phiên Ngung'),(110.6,24.5)],3.4)
S2(29,30,[X('Phiên Ngung'),X('Nhật Nam')],2.0)
show('Phiên Ngung',23,30);show('Thạch Môn',23,28);show('Mê Linh',29,30);show('Cửu Chân',29,30);show('Nhật Nam',29,30)
reg('NAM VIỆT',(110.2,23.9),P_NV,NV,(23,28),alpha=22)
reg('NHÀ HÁN',(110.2,23.9),P_NV,NV,(29,30),steps=[(R(23,0),NH)],alpha=26)
NU(23,'111 TCN','nhà Hán đánh Nam Việt',0.5)
AR(24,0.5,3.4,(110.4,24.7),X('Phiên Ngung'),NH,'nhiều đạo quân cùng tiến vào')
AR(24,2.0,3.0,(113.3,24.7),X('Thạch Môn'),NH,'đạo quân đi đường sông')
C3(25,0.4,3.2,'Dương Bộc','dẫn chín nghìn quân tinh nhuệ',NH)
NT(25,3.2,3.0,113.12,23.62,'ải Thạch Môn bị phá',NH)
G('Đạo quân Dương Bộc',NH,12,P(24,27,[(113.3,24.7),X('Thạch Môn'),(113.45,23.0)],0.5,-1.5),show=(R(24,0),E(28,0)),emb='tri',seed=906,soff=(-45,-30),spread=0.8)
G('Đạo quân Lộ Bác Đức',NH,10,P(24,27,[(110.6,24.6),(112.2,23.9),(113.0,23.3)],0.5,-1.5),show=(R(24,0),E(28,0)),emb='tri',seed=907,soff=(-70,25),spread=0.7)
FIRES.append((R(27,3.0),E(27,0),113.26,23.13))
Q(27,27)
G('Vua và Lữ Gia chạy ra biển',NV,4,[(R(28,0),113.26,23.13),(R(28,5),113.95,22.55)],show=(R(28,0),E(28,0)),emb='dia',seed=908,spread=0.4,soff=(30,-25))
OW('Phiên Ngung',NV,(28,3.0,NH),(48,0.8,VT),(70,0.5,NH))
OW('Mê Linh',NH,(47,1.5,VT),(70,0.5,NH));OW('Luy Lâu',NH,(47,1.5,VT),(70,0.5,NH))
C3(29,0.5,3.0,'Chín quận','Giao Chỉ, Cửu Chân, Nhật Nam ở phía nam',NH)
# ======================= CHƯƠNG 5: HAI THÁI THÚ TỐT (31–37)
S2(31,37,[X('Mê Linh'),X('Cửu Chân')],3.8)
show('Mê Linh',31,37);show('Cửu Chân',31,37);show('Luy Lâu',31,37)
reg('GIAO CHỈ',(105.2,22.2),P_GC,NH,(31,37),alpha=24)
NU(33,'29 SCN','sứ Giao Chỉ sang cống nhà Hán',0.6)
C3(34,0.4,3.2,'Tích Quang','thái thú Giao Chỉ, dạy dân lễ nghĩa',NEU)
C3(35,0.4,3.2,'Nhâm Diên','thái thú Cửu Chân, dạy dân cày cấy',NEU)
NT(36,0.5,3.0,105.8,19.95,'hai nghìn người cưới vợ cùng một lúc',NEU)
# ======================= CHƯƠNG 6: TÔ ĐỊNH (38–40)
S2(38,40,[X('Luy Lâu')],6.0)
show('Luy Lâu',38,40);show('Mê Linh',38,40)
reg('GIAO CHỈ',(105.2,22.2),P_GC,NH,(38,40),alpha=30)
C3(38,0.4,3.2,'Tô Định','đứng đầu việc cai trị Giao Chỉ',NH)
NU(38,'39 SCN','Tô Định cai trị Giao Chỉ',0.8)
# ======================= CHƯƠNG 7: HAI CHỊ EM Ở MÊ LINH (41–44)
S2(41,44,[X('Mê Linh'),X('Chu Diên')],6.0)
show('Mê Linh',41,44);show('Chu Diên',41,44)
reg('GIAO CHỈ',(105.2,22.2),P_GC,NH,(41,44),alpha=16)
RIVERS.append(('SÔNG HỒNG',[(103.8,22.6),(104.5,22.2),(105.0,21.8),(105.4,21.3),(105.85,21.05),(106.3,20.65),(106.55,20.3)],6,(104.4,21.95),(R(41,0),E(44,0))))
C3(41,0.5,3.2,'Trưng Trắc','con gái Lạc tướng ở Mê Linh',VT)
AR(42,0.5,3.2,X('Mê Linh'),X('Chu Diên'),VT,'hôn nhân hai nhà tướng')
C3(43,0.4,3.0,'Trưng Nhị','em gái của Trưng Trắc',VT)
# ======================= CHƯƠNG 8: KHỞI BINH MÙA XUÂN NĂM 40 (45–50)
S2(45,47,[X('Mê Linh'),(108.4,23.3)],3.6)
S2(48,50,[X('Phiên Ngung'),X('Nhật Nam')],2.35)
show('Mê Linh',45,50);show('Luy Lâu',45,47)
reg('GIAO CHỈ',(105.2,22.2),P_GC,NH,(45,47),steps=[(R(47,1.5),VT)],alpha=26)
reg('LĨNH NAM',(110.0,23.6),P_LN,NH,(48,50),steps=[(R(48,0.5),VT)],alpha=26)
NU(45,'mùa xuân 40','Hai Bà Trưng khởi binh',0.6)
G('Quân Hai Bà Trưng',VT,16,P(45,46,[X('Mê Linh'),(105.9,21.1),X('Luy Lâu')],0.8,-0.5),show=(R(45,0),E(47,0)),emb='sun',seed=909,soff=(45,-30),spread=0.9)
G('Quân Hai Bà Trưng ',VT,16,[(R(47,0),106.10,21.03),(E(50,0),105.72,21.20)],show=(R(47,0),E(50,0)),emb='sun',seed=909,soff=(45,-30),spread=0.7,label=False)
G('Thái thú Tô Định chạy',NH,5,P(46,47,[X('Luy Lâu'),(106.8,22.0),(108.4,23.3),(110.2,24.4)],0.4,-0.2),show=(R(46,0),E(47,0)),emb='tri',seed=910,soff=(-50,-25),spread=0.7)
Q(46,46)
J(47,'flag','Quan lớn nhất vùng, thoát thân bằng chính đôi chân',1.5)
NT(48,0.6,3.2,109.35,21.9,'bốn quận hưởng ứng: Nam Hải, Hợp Phố, Cửu Chân, Nhật Nam',VT)
OW('Hợp Phố',NH,(48,1.5,VT),(70,0.5,NH));OW('Cửu Chân',NH,(48,2.5,VT),(70,0.5,NH));OW('Nhật Nam',NH,(48,3.5,VT),(70,0.5,NH))
show('Phiên Ngung',48,50);show('Hợp Phố',48,50);show('Cửu Chân',48,50);show('Nhật Nam',48,50)
NT(49,0.6,3.2,110.3,22.9,'con số 65 thành còn được các nhà nghiên cứu bàn',VT)
C3(50,0.5,3.2,'Trưng Vương','xưng vương, đóng đô ở Mê Linh',VT)
# ======================= CHƯƠNG 9: NHÀ HÁN ĐÁP TRẢ: MÃ VIỆN (51–55)
S2(51,52,[X('Phiên Ngung'),X('Mê Linh')],2.5)
S2(53,55,[X('Hợp Phố'),X('Mê Linh')],3.4)
show('Phiên Ngung',51,55);show('Hợp Phố',51,55);show('Mê Linh',51,55);show('Lãng Bạc',55,55)
reg('LĨNH NAM',(110.0,23.6),P_LN,VT,(51,55),steps=[],alpha=22)
NU(51,'41 SCN','nhà Hán thấy họ Trưng xưng vương',0.5)
AR(52,0.5,3.4,(112.9,24.7),X('Hợp Phố'),NH,'chuẩn bị xe, thuyền, đường, thóc lương')
NT(52,3.6,3.0,111.2,24.1,'Trường Sa nằm xa hơn về phía bắc',NH)
C3(54,0.4,3.2,'Mã Viện','Phục Ba tướng quân',NH)
J(54,'scroll','Chuẩn bị kỹ đến mức làm đường trước khi đi đánh',2.6)
NU(55,'42 SCN','Mã Viện đem quân tiến về phương nam',0.5)
G('Quân Mã Viện',NH,14,P(55,55,[X('Hợp Phố'),(108.3,21.75),(107.2,21.3),(106.45,21.15)],0.5,-0.6),show=(R(55,0),E(55,0)),emb='tri',seed=911,soff=(-50,-30),spread=0.9)
# ======================= CHƯƠNG 10: LÃNG BẠC VÀ CẤM KHÊ (56–59)
S2(56,59,[X('Lãng Bạc'),X('Cấm Khê')],6.0)
show('Lãng Bạc',56,59);show('Cấm Khê',56,59);show('Mê Linh',56,59)
reg('LĨNH NAM',(110.0,23.6),P_LN,VT,(56,59),alpha=14)
NU(56,'tháng giêng 42','trận Lãng Bạc',0.5)
NT(56,2.5,3.0,106.05,21.28,'Lãng Bạc, vị trí ước lượng',NH)
G('Quân Mã Viện ',NH,16,[(R(56,0),106.62,21.08),(R(56,5),106.18,21.10),(R(57,6),106.15,21.10),(R(58,4),106.0,21.12),(R(59,3),105.55,21.08),(E(59,0),105.45,21.06)],show=(R(56,0),E(59,0)),emb='tri',seed=912,soff=(-50,-30),spread=0.8,label=False)
G('Quân Trưng Vương',VT,16,[(R(56,0),105.82,21.14),(R(56,6),106.02,21.12),(R(58,0),106.02,21.12),(R(58,8),105.8,21.1),(R(59,5),105.35,21.05),(E(59,0),105.35,21.05)],show=(R(56,0),E(59,0)),emb='sun',seed=913,soff=(45,30),spread=0.85,alive=[(0,1),(R(58,8),1),(E(59,0),0.55)],label=False)
BATT.append((R(56,5),R(57,6),106.08,21.12,['Quân Mã Viện ','Quân Trưng Vương']))
NT(59,0.5,3.0,105.35,21.22,'Cấm Khê, vị trí ước lượng',VT)
Q(56,59)
# ======================= CHƯƠNG 11: NĂM 43 VÀ NHỮNG GÌ CÒN LẠI (60–65)
S2(60,61,[X('Cấm Khê'),X('Cư Phong')],3.2)
S2(62,63,[X('Cấm Khê'),X('Cư Phong')],3.2)
S2(64,65,[X('Hát Giang'),X('Phiên Ngung')],2.4)
show('Cấm Khê',60,61);show('Cư Phong',60,63);show('Hát Giang',64,65);show('Phiên Ngung',64,65)
NU(60,'43 SCN','tháng giêng, hai bà qua đời',0.6)
G('Quân Mã Viện đuổi theo',NH,14,P(60,61,[(105.45,21.06),(105.4,20.4),X('Cư Phong')],0.4,-0.5),show=(R(60,0),E(61,0)),emb='tri',seed=914,soff=(-50,-25),spread=0.8)
G('Quân Đô Dương',VT,8,P(60,61,[(105.35,21.05),(105.35,20.3),X('Cư Phong')],0.4,-0.4),show=(R(60,0),E(63,0)),emb='sun',seed=915,soff=(45,30),spread=0.6,alive=[(0,0.6),(R(61,3),0.6),(R(61,6),0.15)])
Q(60,60)
NT(61,0.6,3.0,105.45,19.65,'Đô Dương xin hàng ở Cư Phong',VT)
NT(62,0.6,3.5,105.1,20.2,'cột đồng: theo sử chép, vị trí chưa rõ',NH)
NT(63,0.5,3.0,105.9,21.0,'thành Kiển Giang hình tròn như cái kén',NH)
NT(64,0.6,3.2,105.52,21.35,'đền thờ ở xã Hát Giang',VT)
NT(65,0.4,3.0,113.26,23.4,'đền thờ cả ở Phiên Ngung',VT)
# ======================= CHƯƠNG 12: VÌ SAO CHỈ BA NĂM (66–73)
S2(66,67,[X('Mê Linh'),X('Cửu Chân')],3.6)
S2(68,69,[(112.0,24.6),X('Mê Linh')],2.4)
S2(70,71,[X('Phiên Ngung'),X('Nhật Nam')],2.35)
S2(72,73,[X('Mê Linh'),(108.4,23.3)],3.2)
show('Mê Linh',66,73)
reg('LĨNH NAM',(110.0,23.6),P_LN,VT,(66,69),alpha=22);reg('NHÀ HÁN',(110.0,23.6),P_LN,NH,(70,73),alpha=22)
reg('NGŨ LĨNH',(111.4,24.6),P_NL,GY,(68,69),alpha=40)
NT(66,0.5,3.0,105.72,21.4,'ở ngôi ba năm (năm 40–43)',VT)
NT(68,0.6,3.5,112.0,24.3,'dãy núi Ngũ Lĩnh, cửa ngõ phía bắc',GY)
NU(70,'82 năm','nhà Hán cai trị trở lại từ năm 44',0.6)
G('Thái thú chạy về nước (nhắc lại)',NH,5,P(72,72,[X('Luy Lâu'),(106.8,22.0),(108.4,23.3),(110.2,24.4)],0.8,-0.3),show=(R(72,0),E(72,0)),emb='tri',seed=916,soff=(-50,-25),spread=0.7)
G('Quân hai bà ',VT,12,[(R(72,0),105.72,21.20),(E(73,0),105.72,21.20)],show=(R(72,0),E(73,0)),emb='sun',seed=917,soff=(45,30),spread=0.6,label=False)
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
    for a,b,y in [(1,4,'40 SCN'),(5,8,'207 TCN'),(9,9,'196 TCN'),(23,30,'111 TCN'),(38,40,'39 SCN'),(45,50,'40 SCN'),(51,54,'41 SCN'),(55,59,'42 SCN'),(60,65,'43 SCN')]:
        if a<=m<=b: return y
    return None
NO_GROUP_LABEL=True
SIDES=[('Nhà Hán',NH,{g['name'].strip() for g in GROUPS if g['col']==NH}),('Nam Việt',NV,{g['name'].strip() for g in GROUPS if g['col']==NV}),('Hai Bà Trưng',VT,{g['name'].strip() for g in GROUPS if g['col']==VT})]
