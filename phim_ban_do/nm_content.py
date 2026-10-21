"""Nội dung hình ảnh video Nguyên Mông trọn bộ (1257–1288). Số câu 1–332 (khóa n = 5000 + số câu)."""
from build2 import T,D,TOTAL,chap,PH
INF=1e9
BASE=5000
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
TL=(40,140,150);BR=(150,100,60);OR=(200,110,40);GY=(110,110,110);OL=(110,130,50);BK=(60,60,60);YW=(214,176,40);NEU=(150,140,120);PUF=(122,96,140)
NG=RD;VT=GR
# ---- địa danh
LOC={'Thăng Long':(105.85,21.03,'big'),'Vân Nam':(102.7,25.05,'mid'),'Đại Lý':(100.25,25.6,'town'),
     'Bình Lệ Nguyên':(105.55,21.3,'town'),'Phù Lỗ':(105.9,21.22,'town'),'Quy Hóa':(104.55,21.85,'town'),
     'Vạn Kiếp':(106.40,21.10,'mid'),'Lạng Sơn':(106.76,21.85,'mid'),'Bạch Đằng':(106.88,20.84,'town'),
     'Vân Đồn':(107.45,21.05,'mid'),'Cửa Lục':(107.08,20.95,'town'),'Thanh Hóa':(105.78,19.86,'town'),
     'Thiên Trường':(106.18,20.43,'town')}
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
REGIONS=[];RIVERS=[];ROUTES=[];TIDE=[]
WATER=[('VỊNH BẮC BỘ',(108.4,20.3),26),('SÔNG HỒNG',(104.9,21.35),22)]
NIGHT=[(0,0)]
def G(name,col,n,keys,show=None,**kw):
    GROUPS.append(dict(name=name,col=col,n=n,keys=keys,show=show or (keys[0][0]-0.3,keys[-1][0]+3),**kw))
def NT(n,o,dur,lo,la,txt,col=DK): NOTES.append((R(n,o),min(R(n,o+dur),E(n,-0.1)),lo,la,txt,col))
def NT2(n0,n1,lo,la,txt,col=DK): NOTES.append((R(n0,0.3),E(n1,-0.15),lo,la,txt,col))
def C3(n,name,role,col,o=0.3,dur=3.4): CARDS3.append((R(n,o),min(R(n,o+dur),E(n,-0.2)),name,role,col))
def Q(n,sub,text,who,col,dur=None):
    t0=at(n,sub);QUOTES.append((t0,min(E(n,-0.1),t0+(dur or 6.0)),text,who,col))
def J(n,icon,text,off=1.2): JOKES.append((R(n,off),E(n,-0.1),icon,text))
def NU(n,big,small,delay=1.2): NUMS.append((BASE+n,big,small,delay))
def AR(n,o,dur,a,b,col,txt): ARROWS.append((R(n,o),R(n,o+dur),a,b,col,txt))
def AR2(n0,n1,a,b,col,txt): ARROWS.append((R(n0,0.2),E(n1,-0.1),a,b,col,txt))
def LET(n,o,dur,a,b,txt): LETTERS.append((R(n,o),R(n,o+dur),a,b,txt))
def X(name): return LOC[name][:2]
SCN=[]
def S(a,b,lo,la,z): SCN.append((a,b,lo,la,z))
def reg(name,lab,poly,c0,win,steps=(),alpha=34):
    seq=[(0,c0)]
    for (t,c) in steps: seq+=[(t,seq[-1][1]),(t+3,c)]
    REGIONS.append(dict(name=name,lab=lab,poly=poly,own=seq,alpha=alpha,win=(R(win[0],-1),E(win[1],1))))
def METER(n0,n1,title,rows): METERS.append((R(n0,0.5),E(n1,-0.2),title,rows))

P_DV=[(103.5,22.7),(104.2,23.1),(106.5,23.2),(107.8,22.0),(107.4,20.9),(106.5,19.95),(105.0,19.9),(103.8,21.0),(103.4,22.0)]
END=332
# ======================================================= MÁY QUAY
S(1,3,101.3,25.3,2.5);S(4,4,102.4,24.9,1.9);S(5,9,104.2,23.3,1.3);S(10,14,104.7,24.4,0.86)
S(15,26,104.0,24.2,0.95)
S(27,33,104.2,23.4,2.0);S(34,38,105.4,22.0,2.4)
S(39,55,104.5,23.0,1.3)
S(56,65,105.6,21.4,3.8)
S(66,80,105.7,21.1,3.6)
S(81,89,105.6,21.0,3.2);S(90,95,105.2,21.45,3.0)
S(96,109,105.2,22.0,2.2)
S(110,122,105.5,21.6,1.6)
S(123,131,106.3,21.3,3.6)
S(132,136,106.2,21.9,2.4);S(137,147,105.95,21.35,3.0)
S(148,150,105.9,21.8,2.6);S(151,152,105.9,20.7,2.6)
S(153,163,106.0,21.2,3.6)
S(164,174,106.0,20.9,3.2)
S(175,183,105.9,20.9,4.5)
S(184,196,105.85,20.5,2.8)
S(197,209,106.0,20.62,4.0)
S(210,214,106.2,21.3,3.4)
S(215,221,105.5,21.8,1.8)
S(222,228,104.5,24.0,0.95)
S(229,237,106.9,21.5,2.2)
S(238,254,107.35,21.15,4.0)
S(255,265,106.1,21.1,3.4)
S(266,269,106.4,21.2,4.6)
S(270,275,106.6,21.3,3.2)
S(276,284,106.55,21.5,4.0)
S(285,291,106.62,21.0,6.4)
S(292,303,106.72,20.95,7.0)
S(304,309,106.9,21.0,4.0)
S(310,318,105.8,21.6,1.7)
S(319,332,105.5,22.2,1.5)
# ======================================================= TIÊU ĐỀ
TITLES.append((0.3,5.2,'NGUYÊN MÔNG · TRỌN BỘ','BA LẦN KHÔNG ĐỔ','1258 · 1285 · 1288'))
TITLES.append((R(332,0.2),E(332,0.6),'NGƯỜI GÁC SỬ','CẢM ƠN BẠN ĐÃ XEM','chuyện có thật, kể theo tài liệu lịch sử'))
# ======================================================= THÀNH
show('Thăng Long',1,END);show('Vân Nam',1,66);show('Đại Lý',27,55)
show('Bình Lệ Nguyên',56,65);show('Phù Lỗ',56,65);show('Quy Hóa',90,95)
show('Lạng Sơn',148,163);show('Lạng Sơn',210,214);show('Lạng Sơn',229,237);show('Lạng Sơn',266,284)
show('Vạn Kiếp',156,163);show('Vạn Kiếp',231,237);show('Vạn Kiếp',255,309)
show('Bạch Đằng',270,309);show('Vân Đồn',238,254);show('Vân Đồn',304,309);show('Cửa Lục',238,254)
show('Thanh Hóa',184,200);show('Thiên Trường',164,174)
OW('Thăng Long',GR,(75,0,RD),(87,0,GR),(169,2,RD),(210,0,GR),(256,0,RD))
OW('Vạn Kiếp',GR,(159,3,RD))
reg('ĐẠI VIỆT',(105.3,22.6),P_DV,GR,(31,END),alpha=22)
RIVERS.append(('SÔNG BẠCH ĐẰNG',[(106.40,21.10),(106.52,21.07),(106.63,21.01),(106.73,20.96),(106.82,20.91),(106.88,20.82),(106.93,20.72),(107.0,20.62)],7,(106.68,21.15),(R(229,0),E(309,1))))
# ======================================================= PHẦN MỘT
# ---- chương 1
G('Kỵ binh Mông Cổ',NG,14,[(R(1,0),100.7,25.5),(R(3,5),101.5,25.3),(R(4,5),102.6,25.05),(R(14,0),102.7,25.05)],show=(R(1,0),E(14,0)),emb='tri',seed=501,kind='cav',soff=(-60,-20))
AR2(2,4,(100.2,25.9),(102.2,25.15),NG,'từ thảo nguyên phía bắc')
J(2,'flag','Thi toát mồ hôi: họ thắng khỏi chấm')
NU(7,'1258 · 1285 · 1288','ba lần đứng trước đế quốc',1.0)
# ---- chương 2
NU(16,'THÀNH CÁT TƯ HÃN','gom các bộ tộc thảo nguyên',1.0)
NT2(20,22,105.6,22.3,'đất ngập nước: sân nhà của Đại Việt',GR)
J(21,'flag','Ngựa thảo nguyên giữa ruộng nước')
NT2(23,24,102.7,25.6,'mượn thợ và máy bắn đá',NG)
J(25,'coin','Xin việc: không biết làm, biết thuê')
# ---- chương 3
AR2(28,28,(102.4,25.0),(108.3,23.1),NG,'đường vòng đánh nhà Tống')
NU(29,'KHOẢNG 1253','Mông Cổ vào Đại Lý, sát biên giới Đại Việt',1.5)
C3(32,'Trần Thủ Độ','người sắp đặt cuộc đổi triều',GR)
C3(33,'Trần Thái Tông','vua Đại Việt lúc này',GR,o=2.0)
NT2(37,38,105.4,21.8,'vương hầu nhà Trần đều cầm quân',GR)
# ---- chương 4
NU(39,'1257','Mông Cổ sai sứ đến Đại Việt',1.5)
C3(39,'Ngột Lương Hợp Thai','tướng Mông Cổ ở Vân Nam',NG,o=3.0)
LET(40,0.4,5.0,X('Vân Nam'),X('Thăng Long'),'đòi đầu hàng')
C3(41,'Trần Thái Tông','vua Đại Việt, không chịu hàng',GR,o=0.2,dur=2.4)
NT2(42,44,105.85,21.55,'hai sứ giả đi vào rồi không về',(120,100,40))
J(43,'scroll','Thư đòi nợ, người đưa thư mất tích')
NT2(49,51,106.9,23.1,'lấy cả nước, hay chỉ mượn đường?',NG)
G('Quân Mông Cổ 1257',NG,30,[(R(53,0),102.7,25.05),(R(55,6),103.97,22.5)],show=(R(53,0),R(56,0)),emb='tri',seed=502,kind='cav',soff=(0,-30))
AR2(53,55,X('Vân Nam'),(103.97,22.5),NG,'đi men theo sông')
# ---- chương 5
NU(56,'17/1/1258','Trận Bình Lệ Nguyên',0.6)
G('Quân Mông Cổ',NG,30,[(R(56,0),104.2,22.3),(R(56,5),105.1,21.55),(R(57,5),105.55,21.28),(R(60,0),105.9,21.2),(R(62,0),105.86,21.05),(R(89,0),105.86,21.05),(R(90,4),105.0,21.5),(R(93,0),104.55,21.85),(R(95,6),103.97,22.5)],show=(R(56,0),E(95,1)),emb='tri',seed=503,kind='cav',soff=(130,-40))
G('Quân Đại Việt',GR,26,[(0,105.55,21.3)],show=(R(58,0),E(61,0)),emb='sun',seed=504,soff=(-120,-30),alive=[(0,1),(R(59,0),1),(R(59,5),0.35)])
C3(58,'Trần Thái Tông','đích thân ra trận',GR,o=0.2,dur=2.6)
BATT.append((R(58,2.0),R(59,3.5),105.55,21.3,['Quân Mông Cổ','Quân Đại Việt']))
NT2(59,59,105.55,21.6,'Đại Việt thua',GR)
NT2(60,61,105.95,21.45,'hôm sau, Phù Lỗ: thua tiếp',GR)
# ---- chương 6
C3(67,'Trần Thủ Độ','người nắm quyền trong triều',GR,o=0.2,dur=2.6)
Q(69,'Đầu thần','Đầu thần chưa rơi xuống đất, xin bệ hạ đừng lo.','Trần Thủ Độ',GR,5.5)
G('Vua và triều đình',GR,10,[(R(71,0),105.85,21.03),(R(72,6),106.0,20.7)],show=(R(71,0),E(80,0)),emb='sun',seed=505,soff=(110,40))
NT2(72,73,105.45,20.65,'vườn không nhà trống',(120,100,40))
J(77,'coin','Kho trống, sạch sẽ, thoáng mát')
METER(76,80,'LƯƠNG THỰC',[('Mông Cổ',NG,[(R(75,0),0.7),(R(80,0),0.08)])])
# ---- chương 7
NU(81,'CHÍN NGÀY','quân Mông Cổ ở Thăng Long',0.8)
J(83,'scroll','Chín ngày: đủ để biết mình nhầm chỗ')
G('Vua Trần và thái tử',GR,12,[(R(84,0),106.0,20.7),(R(85,3),105.93,21.0)],show=(R(84,0),E(88,0)),emb='sun',seed=506,kind='ship',soff=(110,50))
BATT.append((R(85,3),R(87,0),105.9,21.02,['Quân Mông Cổ','Vua Trần và thái tử']))
NT2(85,86,106.15,20.8,'Đông Bộ Đầu, bên sông Hồng',GR)
AR2(90,91,X('Thăng Long'),X('Quy Hóa'),NG,'quân Mông Cổ rút')
G('Người địa phương',OL,8,[(0,104.55,21.85)],show=(R(93,0),E(95,0)),emb='circle',seed=507,soff=(-100,40))
NT2(93,94,104.55,22.15,'Quy Hóa: bị đánh úp',OL)
# ---- chương 8
NT2(97,97,105.2,21.8,'sử nhà Trần: chiến thắng',GR)
NT2(98,98,106.2,21.7,'sử Mông Cổ: chiếm Thăng Long',NG)
J(100,'scroll','Hai bộ sử, hai chiến thắng')
C3(104,'Trần Thánh Tông','lên ngôi khi vua cha nhường',GR,o=0.2,dur=2.6)
C3(108,'Hốt Tất Liệt','lập nhà Nguyên',NG,o=0.2,dur=2.6)
NU(109,'HƠN HAI MƯƠI NĂM','rồi họ quay lại',1.2)
# ======================================================= PHẦN HAI
# ---- chương 9
NT2(111,111,104.4,22.6,'nhà Nguyên: hạm đội, máy công thành, quân Hán',NG)
J(112,'scroll','Hai mươi năm nuôi cơn tức')
NT2(114,116,105.5,20.2,'Chiêm Thành ở phía nam, qua đất Đại Việt',(120,100,40))
J(117,'flag','Đi tắt qua sân nhà hàng xóm')
NU(119,'1281','Nguyên phong Trần Di Ái làm vua An Nam',1.2)
C3(119,'Trần Di Ái','một quân cờ của nhà Nguyên',NG,o=3.2,dur=2.4)
J(120,'flag','Làm quân cờ chưa bao giờ dễ')
NU(121,'1282','quân Nguyên đưa ông về, bị chặn lại',1.2)
# ---- chương 10
NT2(124,125,106.55,20.98,'hội nghị lớn ở Bình Than',GR)
C3(124,'Hai vua nhà Trần','vua Nhân Tông và vua cha',GR,o=0.2,dur=2.6)
C3(126,'Trần Quốc Toản','cậu bé mười sáu tuổi bị gạt ra',GR,o=0.2,dur=2.8)
J(128,'scroll','Quả cam nổi tiếng nhất lịch sử')
G('Đội quân của Trần Quốc Toản',GR,10,[(0,106.45,21.12)],show=(R(129,0),E(130,0)),emb='sun',seed=508,soff=(-100,30))
Q(129,'Phá cường địch','Phá cường địch, báo hoàng ân.','lá cờ của Trần Quốc Toản',GR,5.0)
NT2(131,131,105.9,20.35,'Toa Đô đánh Chiêm Thành từ phía nam',NG)
# ---- chương 11
NU(133,'1284','Thoát Hoan đem quân xuống phía nam',1.0)
C3(133,'Thoát Hoan','con trai Hốt Tất Liệt',NG,o=3.0,dur=2.6)
LET(134,0.4,5.0,(106.75,22.45),X('Thăng Long'),'xin mượn đường')
J(136,'scroll','"Mượn đường chút": lời đe dọa lịch sự')
NT2(137,137,105.85,21.55,'Đại Việt từ chối',GR)
NT2(139,141,105.85,21.3,'Diên Hồng: các cụ già đáp "Đánh!"',GR)
Q(141,'Đánh','"Đánh!"','các bô lão ở Diên Hồng',GR,2.5)
J(142,'scroll','Cuộc bỏ phiếu ngắn nhất lịch sử')
C3(145,'Trần Quốc Tuấn','được giao chỉ huy toàn quân',GR,o=0.2,dur=2.8)
NT2(146,147,106.5,21.75,'Toa Đô xin lập hẳn một tỉnh của Nguyên',NG)
# ---- chương 12
NU(148,'27/1/1285','quân Nguyên vượt biên giới',0.6)
G('Đạo Thoát Hoan',NG,30,[(R(148,0),106.9,22.5),(R(149,6),106.76,21.85),(R(155,0),106.5,21.55),(R(157,0),106.4,21.12),(R(163,5),106.3,21.1),(R(164,0),106.1,21.2),(R(165,0),105.95,21.05),(R(169,5),105.85,21.03),(R(209,0),105.85,21.03),(R(211,0),106.4,21.1),(R(214,5),106.76,21.85)],show=(R(148,0),E(214,1)),emb='tri',seed=511,kind='cav',soff=(120,-30))
G('Đạo sông Chảy',NG,14,[(R(148,0),104.3,22.6),(R(150,6),104.9,21.95),(R(154,0),105.1,21.55)],show=(R(148,0),E(155,0)),emb='tri',seed=512,kind='cav',soff=(-100,-20))
G('Đạo Toa Đô',NG,16,[(R(151,0),105.85,19.86),(R(152,5),105.85,20.1)],show=(R(151,0),E(152,0)),emb='tri',seed=513,soff=(0,-20))
G('Quân Trần',GR,24,[(R(148,0),106.85,22.1),(R(155,0),106.55,21.5),(R(156,3),106.4,21.15)],show=(R(148,0),E(163,0)),emb='sun',seed=514,soff=(-110,30),alive=[(0,1),(R(159,0),1),(R(160,2),0.5)])
AR(148,0.5,6.0,(106.9,22.5),X('Lạng Sơn'),NG,'đường chính')
AR(150,0.0,5.0,(104.3,22.6),(105.1,21.55),NG,'theo sông Chảy')
AR(151,0.0,6.0,(105.85,19.85),(105.9,20.45),NG,'từ phía nam')
NT2(153,153,106.95,22.2,'ải biên giới: không giữ nổi',GR)
NT2(154,154,104.7,21.85,'Thu Vật: Trần Nhật Duật chặn',GR)
NT2(155,155,106.6,21.72,'Nội Bàng: thua',GR)
BATT.append((R(157,1.0),R(159,4.0),106.4,21.12,['Đạo Thoát Hoan','Quân Trần']))
NT2(158,159,106.55,20.9,'thủy chiến ở Vạn Kiếp',GR)
# ---- chương 13
NT2(164,165,106.18,21.2,'sông Đuống',DK)
NT2(167,167,105.95,20.55,'Lý Nhân: vẫn không thắng',GR)
G('Vua Trần Nhân Tông',GR,10,[(R(165,0),105.95,21.05),(R(169,0),105.95,20.95),(R(172,5),106.18,20.43)],show=(R(165,0),E(174,0)),emb='sun',seed=515,soff=(120,50))
J(171,'coin','Có bài học phải học hai lần')
G('Dân rời làng',OL,10,[(R(173,0),105.5,20.8),(R(174,5),106.0,20.25)],show=(R(173,0),E(174,0)),emb='circle',seed=516,soff=(-100,30))
NT2(173,174,105.55,20.55,'dân rời làng, mang theo gạo',OL)
# ---- chương 14
NT2(175,176,105.9,20.78,'trận Đà Mạc, trên bãi sông',GR)
C3(176,'Trần Bình Trọng','tướng trẻ chặn giặc cho vua rút',GR,o=0.2,dur=3.0)
G('Quân Trần Bình Trọng',GR,8,[(0,105.9,20.85)],show=(R(176,0),E(180,0)),emb='sun',seed=517,soff=(-80,30))
Q(179,'Thà làm ma','Thà làm ma nước Nam, còn hơn làm vua đất Bắc.','Trần Bình Trọng',GR,6.5)
# ---- chương 15
G('Quân Toa Đô',NG,16,[(R(184,0),105.9,19.82),(R(185,5),105.78,19.9),(R(188,0),105.78,19.95),(R(196,0),105.85,20.4)],show=(R(184,0),E(198,0)),emb='tri',seed=518,soff=(-80,-20))
C3(185,'Toa Đô','đánh từ Chiêm Thành ra bắc',NG,o=0.2,dur=2.8)
AR(185,0.5,6.0,(105.9,19.85),(105.85,20.4),NG,'từ phía nam')
NT2(188,188,105.78,19.78,'Thanh Hóa: Trần Kiện đầu hàng',DK)
J(190,'flag','Hai người cùng kéo ổ bánh mì')
METER(193,196,'LƯƠNG THỰC',[('Mông Cổ',NG,[(R(193,0),0.6),(R(196,0),0.1)])])
NT2(194,195,106.5,20.55,'nóng ẩm, thiếu nước sạch, bệnh tật',DK)
# ---- chương 16
J(198,'flag','Đến đoạn cuối mới có nhạc hùng tráng')
G('Thủy quân Đại Việt',GR,10,[(R(199,0),105.95,20.5),(R(204,0),106.0,20.6),(R(206,5),105.97,20.66)],show=(R(199,0),E(209,0)),emb='sun',seed=519,kind='ship',soff=(60,50))
G('Thủy quân Nguyên',NG,10,[(R(199,0),106.12,20.54),(R(204,0),106.05,20.62),(R(206,5),105.99,20.68)],show=(R(199,0),E(208,0)),emb='tri',seed=520,kind='ship',soff=(-60,-30),defeats=[(R(203,0),'flag',E(209,0))])
NT2(199,200,106.45,20.38,'Hàm Tử: đánh vào thuyền Toa Đô',GR)
C3(200,'Trần Quốc Toản','giờ đã là chỉ huy trẻ',GR,o=0.2,dur=2.6)
BATT.append((R(199,3.0),R(201,3.0),106.0,20.52,['Thủy quân Đại Việt','Thủy quân Nguyên']))
NT2(202,203,106.4,20.56,'Tây Kết: Toa Đô tử trận',NG)
C3(204,'Trần Quang Khải','dẫn quân chủ lực ở Chương Dương',GR,o=0.2,dur=2.8)
NT2(204,208,105.45,20.6,'Chương Dương: đánh úp trên sông',GR)
BATT.append((R(204,2.0),R(208,0),106.0,20.64,['Thủy quân Đại Việt','Thủy quân Nguyên']))
NU(210,'GIỮA 1285','Thăng Long được lấy lại',0.8)
NT2(213,213,107.05,20.7,'Ô Mã Nhi chạy đường biển',NG)
# ---- chương 17
NU(215,'ĐẠI VIỆT THẮNG','nhưng phải trả giá',1.0)
NT2(217,218,105.2,20.9,'làng bỏ trống, mất mùa',OL)
NU(220,'CHƯA ĐẦY SÁU THÁNG','kinh đô đổi chủ rồi đổi lại',1.0)
# ======================================================= PHẦN BA
# ---- chương 18
C3(222,'Hốt Tất Liệt','không chịu thua',NG,o=1.5,dur=3.0)
J(224,'scroll','Phép tính sai dù đã đổi bút')
NU(225,'1286','phong Trần Ích Tắc làm vua An Nam',1.2)
NT2(227,228,108.3,24.8,'hoãn đánh Nhật Bản',NG)
# ---- chương 19
NU(229,'CUỐI 1287','quân Nguyên lại tiến xuống',0.8)
G('Quân bộ Thoát Hoan',NG,32,[(R(229,0),106.9,22.5),(R(231,3),106.76,21.85),(R(236,0),106.4,21.12),(R(255,0),106.4,21.12),(R(256,3),105.88,21.03),(R(265,0),105.88,21.03),(R(267,0),106.4,21.12),(R(276,0),106.4,21.12),(R(279,5),106.55,21.45),(R(280,3),106.76,21.85),(R(282,5),106.95,22.25)],show=(R(229,0),E(284,0)),emb='tri',seed=531,kind='cav',soff=(-110,-30),alive=[(0,1),(R(280,2),1),(R(282,6),0.15)])
G('Hạm đội Ô Mã Nhi',NG,10,[(R(229,0),109.3,20.95),(R(238,0),108.2,21.1),(R(243,0),107.5,21.02),(R(246,0),107.05,20.95),(R(250,5),106.55,21.06),(R(268,0),106.42,21.1),(R(285,0),106.45,21.10),(R(289,0),106.60,21.03),(R(292,0),106.64,21.01),(R(293,8),106.78,20.93)],show=(R(229,0),E(303,0)),emb='tri',seed=532,kind='ship',spread=0.9,soff=(-70,-45),alive=[(0,1),(R(297,1),1),(R(297,9),0.2)],defeats=[(R(298,0),'flag',E(303,0))])
G('Thuyền lương Trương Văn Hổ',NG,10,[(R(232,0),109.4,21.0),(R(243,0),108.2,21.1),(R(248,5),107.62,21.05)],show=(R(232,0),E(251,3)),emb='tri',seed=533,kind='ship',soff=(40,40),alive=[(0,1),(R(249,0),1),(R(250,4),0.05)],defeats=[(R(250,0),'flag',E(251,3))])
AR(229,0.5,5.0,(106.9,22.5),X('Lạng Sơn'),NG,'đường bộ')
AR(231,0.0,6.0,(109.5,20.9),X('Vạn Kiếp'),NG,'đường thủy')
C3(230,'Thoát Hoan','chỉ huy đạo quân đi bộ',NG,o=0.5,dur=2.6)
C3(231,'Ô Mã Nhi','chỉ huy đạo quân đi thuyền',NG,o=0.5,dur=2.6)
NT2(231,231,106.4,21.4,'hẹn gặp nhau ở Vạn Kiếp',NG)
C3(236,'Trần Quốc Tuấn','lại được giao chỉ huy toàn quân',GR,o=0.2,dur=2.8)
# ---- chương 20
C3(238,'Trần Khánh Dư','tướng nhà Trần, từng bị phạt',GR,o=0.3,dur=3.0)
NT2(240,240,107.7,21.45,'Vân Đồn: vùng đảo ngoài vịnh',BL)
G('Quân Trần Khánh Dư',GR,10,[(0,107.5,21.0)],show=(R(241,0),E(254,0)),emb='sun',seed=534,kind='ship',soff=(-40,60))
J(244,'flag','Quên báo cho nhau mình ở đâu')
J(247,'scroll','Xin gia hạn dũng cảm nhất lịch sử')
BATT.append((R(249,0.0),R(250,5.0),107.55,21.04,['Thuyền lương Trương Văn Hổ','Quân Trần Khánh Dư']))
OBJ.append((R(249,1.0),R(250,6.0),'fireboat',(107.42,21.0),(107.62,21.06)))
NU(251,'THÁNG GIÊNG 1288','đoàn thuyền lương bị chặn ở Vân Đồn',1.0)
NT2(252,252,107.12,20.82,'Vân Đồn và Cửa Lục',GR)
C3(253,'Trần Khánh Dư','được tha lỗi cũ',GR,o=0.2,dur=2.4)
# ---- chương 21
NT2(257,258,105.85,21.42,'kinh thành vắng, kho trống',DK)
NT2(259,259,106.3,21.3,'thuyền lương không bao giờ đến',(120,100,40))
NT2(260,261,106.35,20.55,'phá lăng vua Trần ở Thái Bình',NG)
J(264,'coin','Ăn bằng niềm tin: sớm muộn cũng đói')
METER(257,267,'LƯƠNG THỰC',[('Mông Cổ',NG,[(R(256,0),0.5),(R(259,0),0.25),(R(266,0),0.03)])])
# ---- chương 22
NU(267,'5/3/1288','rút về Vạn Kiếp',0.6)
C3(269,'Thoát Hoan','họp các tướng, quyết định rút',NG,o=0.3,dur=3.0)
AR(270,0.3,4.5,X('Vạn Kiếp'),X('Lạng Sơn'),NG,'đường bộ')
AR(270,1.3,4.5,X('Vạn Kiếp'),(106.98,20.68),NG,'đường thủy')
C3(273,'Trần Quốc Tuấn','đã chờ đúng khoảnh khắc này',GR,o=0.2,dur=2.6)
NT2(275,275,106.55,21.32,'chọn đúng con đường, rồi chờ',GR)
# ---- chương 23
NT2(277,277,106.5,21.35,'phá cầu, chặt cây, đặt bẫy',GR)
J(278,'flag','Đường về nhà thành đường vòng')
G('Quân Đại Việt phục kích',GR,12,[(0,106.7,21.7)],show=(R(277,0),E(282,0)),emb='sun',seed=535,soff=(110,30))
BATT.append((R(280,1.0),R(281,5.0),106.76,21.82,['Quân bộ Thoát Hoan','Quân Đại Việt phục kích']))
NT2(280,280,106.78,22.05,'Thoát Hoan trúng tên độc',NG)
NT2(283,283,106.95,22.4,'vượt núi biên giới: tổn thất rất nặng',NG)
# ---- chương 24
C3(285,'Ô Mã Nhi','tướng thủy quân Nguyên',NG,o=0.3,dur=2.8)
NT2(285,286,106.5,21.3,'thủy quân rút xuôi sông',NG)
G('Thuyền Đại Việt',GR,6,[(R(292,0),106.86,20.88),(R(292,2),106.86,20.88),(R(293,0),106.73,20.97),(R(293,6),106.86,20.88),(R(297,0),106.86,20.88),(R(297,4),106.80,20.93)],show=(R(292,0),E(303,0)),emb='sun',seed=536,kind='ship',spread=0.7,soff=(80,75))
STK=[(106.69,20.985),(106.72,20.965),(106.745,20.955),(106.765,20.94),(106.785,20.93),(106.80,20.92),(106.815,20.905),(106.835,20.89),(106.70,20.96),(106.73,20.98),(106.76,20.955),(106.79,20.915),(106.82,20.925),(106.85,20.87)]
TIDE.append(([(106.60,21.03),(106.70,20.98),(106.80,20.92),(106.88,20.84),(106.92,20.75)],[(0,1.0),(R(293,3),1.0),(R(294,0),0.95),(R(295,3),0.08),(R(297,2),0.08),(R(303,2),0.7)],STK,(R(289,0),E(298,0)),R(287,0.5),(R(286,0),E(304,0))))
NT2(287,288,106.76,21.02,'cọc gỗ đầu bịt sắt',BR)
NT2(289,289,106.76,21.02,'nước lên: cọc chìm dưới nước',BL)
NU(292,'9/4/1288','Trận Bạch Đằng',0.5)
NT2(293,293,106.62,20.9,'thuyền nhỏ giả vờ rút',GR)
NT2(294,294,106.80,20.99,'nước bắt đầu xuống',BL)
NT2(295,295,106.80,20.97,'thuyền lớn mắc cọc',NG)
J(296,'coin','Thủy triều: không nhận lương')
BATT.append((R(297,0.8),R(298,6.0),106.79,20.93,['Hạm đội Ô Mã Nhi','Thuyền Đại Việt']))
OBJ.append((R(297,2.0),R(298,8.0),'fireboat',(106.74,20.955),(106.83,20.90)))
NT2(298,298,106.82,20.86,'Ô Mã Nhi bị bắt',NG)
NU(300,'năm 938','Ngô Quyền cũng dùng cọc và thủy triều',1.4)
# ---- chương 25
NT2(303,303,106.80,20.97,'hạm đội Nguyên coi như mất',NG)
NT2(304,304,107.4,21.2,'đoàn thuyền lương: mất từ Vân Đồn',NG)
NU(307,'TẾT 1289','những người sống sót về đến đất Nguyên',1.0)
NU(310,'1289','Đại Việt thả phần lớn tù binh',1.0)
NT2(313,313,105.5,20.4,'nạn đói kéo dài',OL)
NU(315,'1292','tượng người bằng vàng và lời xin lỗi',1.0)
NU(316,'1294','Hốt Tất Liệt mất',1.0)
NU(318,'1305','Chế Mân cưới công chúa Huyền Trân',1.0)
# ---- chương 26
AR(319,0.3,6.0,(103.97,22.5),(105.85,21.1),NG,'1258')
AR(319,1.5,6.0,(106.9,22.45),(106.0,21.1),NG,'1285')
AR(320,0.5,7.0,(109.0,21.0),(106.45,21.1),NG,'1288')
NT2(321,321,104.0,22.45,'1. Lùi, chờ, đánh điểm yếu',GR)
NT2(322,322,104.0,22.05,'2. Quân đội nào cũng phải ăn',GR)
NT2(323,323,104.0,21.65,'3. Dùng đất, nước và mùa',GR)
NT2(324,324,104.0,21.25,'4. Dân và tướng cùng chống',GR)
NU(327,'NĂM 1300','Trần Quốc Tuấn mất ở Vạn Kiếp',1.0)
J(331,'coin','Lo bữa tối trước khi hành quân')
# ======================================================= HÌNH MINH HỌA (mapprops)
PROPS=[]
def PR(n0,n1,kind,lo,la,arg=None,sc=1.0,o0=0.2,o1=-0.1): PROPS.append((R(n0,o0),E(n1,o1),kind,lo,la,arg,sc))
PR(76,80,'granary',105.1,21.3,None,0.8)
PR(81,83,'calendar',105.35,21.35,9,0.8)
PR(97,98,'scrolls2',105.2,22.15,None,0.8)
PR(119,121,'pawn',105.0,21.95,None,0.7)
PR(124,125,'meeting',106.2,21.2,True,0.8)
PR(127,128,'orange',106.2,21.25,None,0.8)
PR(129,130,'banner',106.75,20.95,'Phá cường địch báo hoàng ân',0.65)
PR(139,142,'hall',105.7,21.5,'ĐÁNH!',0.7)
PR(145,145,'seal',106.15,21.5,None,0.8)
PR(173,173,'granary',105.3,21.1,None,0.8)
PR(193,193,'bowl',106.1,20.75,None,0.8)
PR(194,196,'heat',105.5,20.8,None,0.8)
PR(260,260,'tomb',106.35,20.85,None,0.8)
PR(277,277,'bridge',106.5,21.35,None,0.7)
PR(315,315,'statue',105.9,21.3,None,0.9)
PR(37,38,'pennants',105.4,21.5,'g',0.8)
PR(62,65,'ping',105.85,21.03,'g',1.0)
PR(84,88,'pennants',105.6,21.4,'g',0.8)
PR(99,100,'scrolls2',105.2,22.15,None,0.8)
PR(110,113,'pennants',105.0,22.7,None,0.8)
PR(156,163,'camp',106.2,21.3,None,0.8)
PR(175,178,'pennants',105.9,21.0,'g',0.8)
PR(180,182,'banner',105.95,21.1,'Thà làm ma nước Nam',0.6)
PR(210,214,'ping',105.85,21.03,'g',1.0)
PR(217,217,'bowl',105.8,21.3,None,0.7)
PR(225,226,'pawn',104.6,23.4,None,0.7)
PR(255,256,'pennants',105.9,21.3,None,0.8)
PR(271,272,'bowl',105.3,21.15,None,0.7)
PR(314,314,'seal',105.7,21.6,None,0.7)
PR(327,328,'pennants',106.4,21.15,'g',0.8)
def FXA(n0,n1,kind,a,b,o0=0.3,o1=0.0): FX.append((R(n0,o0),E(n1,o1),kind,a,b))
FXA(56,56,'horn',(105.5,21.3),(105.5,21.3))
FXA(58,59,'volley',(105.4,21.34),(105.6,21.28))
FXA(60,61,'volley',(105.7,21.17),(105.9,21.22))
FXA(85,87,'volley',(105.78,21.0),(105.95,21.03))
FXA(87,87,'horn',(105.9,21.02),(105.9,21.02))
FXA(157,159,'catapult',(106.25,21.1),(106.42,21.13))
FXA(158,159,'firearrows',(106.3,21.05),(106.45,21.12))
FXA(201,203,'volley',(105.9,20.48),(106.05,20.52))
FXA(205,207,'catapult',(105.85,20.68),(105.97,20.63))
FXA(249,250,'firearrows',(107.3,21.02),(107.5,21.04))
FXA(280,281,'volley',(106.68,21.92),(106.8,21.8))
FXA(297,298,'firearrows',(106.68,20.99),(106.8,20.93))
# ======================================================= HOÀN TẤT
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
    for a,b,y in [(39,55,1257),(56,109,1258),(110,120,1281),(121,131,1282),(132,132,1283),(133,147,1284),(148,221,1285),(222,224,1285),(225,228,1286),(229,250,1287),(251,309,1288),(310,314,1289),(315,315,1292),(316,317,1294),(318,318,1305)]:
        if a<=m<=b: return y
    return None
