"""Nội dung hình ảnh video 1 (Từ Khăn Vàng đến Xích Bích). Số câu là số trong kịch bản (1–267)."""
from build2 import T,D,TOTAL,chap,PH
INF=1e9
def R(n,o=0): return T[1000+n]+o
def E(n,o=0): return T[1000+n]+D[1000+n]+o
def at(n,sub,off=0.0):
    for r in PH.get(str(1000+n),[]):
        c,s_,e_=r[:3]
        if sub.lower() in c.lower():
            if len(r)>=5:
                p=c.lower().index(sub.lower())/max(1,len(c));s_=r[3]+(r[4]-r[3])*p-0.1
            return T[1000+n]+0.12+s_+off
    return T[1000+n]+1.0+off
GR=(52,142,86);BL=(54,96,176);RD=(190,52,42);PU=(138,52,112);DK=(46,38,58);GD=(205,160,40)
TL=(40,140,150);BR=(150,100,60);OR=(200,110,40);GY=(110,110,110);OL=(110,130,50);BK=(60,60,60);YW=(214,176,40);NEU=(150,140,120);PUF=(122,96,140)
# ---- thành: (kinh độ, vĩ độ, loại)
LOC={'Lạc Dương':(112.45,34.62,'big'),'Trường An':(108.95,34.27,'big'),'Hứa':(113.83,34.03,'big'),'Nghiệp':(114.35,36.35,'big'),
 'Hạ Bì':(117.95,34.3,'big'),'Thọ Xuân':(116.78,32.6,'big'),'Tương Dương':(112.15,32.05,'big'),'Giang Lăng':(112.2,30.35,'big'),
 'Quảng Tông':(115.0,37.1,'mid'),'Dĩnh Xuyên':(113.6,34.2,'mid'),'Nam Dương':(112.53,33.0,'mid'),'Huỳnh Dương':(113.4,34.78,'town'),
 'Mi Ổ':(107.6,34.3,'town'),'Bình Nguyên':(116.43,37.17,'mid'),'Bắc Hải':(119.0,36.7,'mid'),'Lâm Tri':(118.35,36.8,'mid'),
 'Tiểu Bái':(116.93,34.73,'mid'),'Đàm':(118.3,34.62,'mid'),'Hu Di':(118.52,33.0,'town'),'Hải Tây':(119.3,33.85,'town'),
 'Bộc Dương':(115.05,35.75,'mid'),'Cự Dã':(116.1,35.4,'town'),'Quan Độ':(114.0,34.72,'mid'),'Bạch Mã':(114.52,35.57,'mid'),
 'Diên Tân':(114.2,35.15,'town'),'Ô Sào':(114.55,35.05,'town'),'Lê Dương':(114.5,35.75,'town'),'Nam Bì':(116.9,38.0,'town'),
 'Tân Dã':(112.35,32.5,'mid'),'Trường Bản':(111.8,30.8,'town'),'Hạ Khẩu':(114.3,30.55,'mid'),'Xích Bích':(113.65,29.85,'mid'),
 'Sài Tang':(115.95,29.7,'mid'),'Phan Dương':(116.6,29.3,'town'),'Kiến Nghiệp':(118.8,32.05,'mid'),'Ngô':(120.6,31.3,'mid'),
 'Vũ Quan':(110.2,33.75,'town'),'Trần Lưu':(114.35,34.8,'town'),'Lang Gia':(118.3,35.1,'town'),'Kế':(116.4,39.9,'mid'),'Lỗ Dương':(113.0,33.7,'town'),
 'Phàn Khẩu':(114.2,30.4,'town'),'Bạch Lang Sơn':(119.9,41.2,'town')}
CITIES=dict(LOC)
CITY_SHOW={}
def show(name,a,b):
    CITY_SHOW.setdefault(name,[]).append((R(a,-1),E(b,1)))
def own(*seq): return [(t,c) for t,c in seq]
CITY_OWN={}
def OW(name,col0,*steps):
    """steps: (câu, mốc giây, màu mới)"""
    seq=[(0,col0)]
    for (n,o,c) in steps:
        seq.append((R(n,o),seq[-1][1]));seq.append((R(n,o+2.0),c))
    CITY_OWN[name]=seq
# ---- các danh sách dữ liệu
GROUPS=[];BATT=[];FIRES=[];FX=[];OBJ=[];LETTERS=[];ARROWS=[];NOTES=[];MARKS=[];CARDS3=[];QUOTES=[];JOKES=[];METERS=[];NUMS=[];TITLES=[]
REGIONS=[];RIVERS=[];WATER=[];ROUTES=[];CARDS=[]
NIGHT=[(0,0)]
def nt(n,o0,o1): NIGHT.extend([(R(n,o0),0),(R(n,o0+1.6),0.6),(R(n,o1),0.6),(R(n,o1+1.6),0)])
def G(name,col,n,keys,show=None,**kw):
    GROUPS.append(dict(name=name,col=col,n=n,keys=keys,show=show or (keys[0][0]-0.3,keys[-1][0]+3),**kw))
def P(n,o,lo,la): return (R(n,o),lo,la)
def NT(n,o,dur,lo,la,txt,col=DK): NOTES.append((R(n,o),R(n,o+dur),lo,la,txt,col))
def C3(n,o,dur,name,role,col): CARDS3.append((R(n,o),min(R(n,o+dur),E(n,-0.2)),name,role,col))
def Q(n,sub,text,who,col,dur=None):
    t0=at(n,sub);CARDS_Q=(t0,min(E(n,-0.1),t0+(dur or 6.0)),text,who,col);QUOTES.append(CARDS_Q)
def J(n,icon,text,off=1.2): JOKES.append((R(n,off),E(n,-0.1),icon,text))
def NU(n,big,small,delay=1.2): NUMS.append((1000+n,big,small,delay))
def SKULL(n,o,dur,lo,la,txt): MARKS.append((R(n,o),R(n,o+dur),lo,la,'skull',txt))
def LT(n,o,dur,a,b,txt): LETTERS.append((R(n,o),R(n,o+dur),LOC[a][:2] if isinstance(a,str) else a,LOC[b][:2] if isinstance(b,str) else b,txt))
def AR(n,o,dur,a,b,col,txt): ARROWS.append((R(n,o),R(n,o+dur),a,b,col,txt))
def X(name): return LOC[name][:2]
SCN=[]
def S(a,b,lo,la,z): SCN.append((a,b,lo,la,z))
def reg(name,lab,poly,c0,steps=(),alpha=40):
    seq=[(0,c0)]
    for (t,c) in steps: seq+=[(t,seq[-1][1]),(t+3,c)]
    REGIONS.append(dict(name=name,lab=lab,poly=poly,own=seq,alpha=alpha))
def L(n,dx=0,dy=0): return (LOC[n][0]+dx,LOC[n][1]+dy)
# ======================= CHƯƠNG 1: MỞ ĐẦU (1–17)
S(1,5,113.0,34.5,2.0);S(6,6,113.5,34.5,1.4);S(7,7,115.0,36.0,2.4);S(8,8,112.6,34.6,3.0);S(9,9,113.0,34.5,1.6)
S(10,10,109.8,34.3,2.6);S(11,11,116.5,34.0,1.7);S(12,12,114.2,35.0,3.0);S(13,13,113.4,30.8,2.0);S(14,17,113.8,34.0,1.3)
TITLES.append((0.3,5.2,'VIDEO 1','TỪ KHĂN VÀNG ĐẾN XÍCH BÍCH','năm 184 đến năm 208'))
for nm in ('Lạc Dương','Trường An','Hứa','Nghiệp','Xích Bích','Hạ Bì','Quan Độ'): show(nm,1,17)
OW('Lạc Dương',GD)
reg('ĐẠI HÁN',(113.0,35.6),[(108.5,33.0),(108.5,36.5),(112.0,38.0),(117.0,38.2),(120.5,36.5),(120.5,32.5),(116.5,30.0),(111.0,29.8),(108.5,31.0)],GD)
C3(2,1.0,3.5,'Hoạn quan','người hầu trong cung',DK);C3(2,1.0,3.5,'Ngoại thích','họ hàng của hoàng hậu',OR)
NT(3,1.0,3.5,112.45,34.9,'vua còn là trẻ nhỏ',GD)
NT(5,0.8,5.5,112.5,34.0,'hạn hán · châu chấu · dịch bệnh',(120,100,40))
J(4,'scroll','Ba người lớn tranh nhau ký thay',1.5)
NU(7,'184','Khăn Vàng nổi dậy',1.2);NU(8,'189','Đổng Trác vào kinh đô',1.2);NU(9,'190','liên quân đánh Đổng Trác',1.2)
NU(10,'192','Đổng Trác bị giết',1.2);NU(11,'196','Tào Tháo đón hoàng đế về Hứa',1.2);NU(12,'200','Quan Độ',1.2);NU(13,'208','Xích Bích',1.2)
J(14,'flag','Một đế quốc, ba cái tên, một trận cháy lớn',1.5)
J(17,'fire','Bản đồ sẽ đổi màu mười mấy lần',0.8)
# ======================= CHƯƠNG 2: KHĂN VÀNG (18–35)
S(18,19,115.0,36.3,1.9);S(20,22,115.0,36.8,2.8);S(23,23,114.2,35.2,1.7);S(24,24,113.2,35.3,2.0);S(25,25,115.0,37.0,3.6)
S(26,27,113.6,34.4,3.8);S(28,29,115.0,37.0,2.8);S(30,32,115.5,35.6,1.5);S(33,35,113.5,34.5,1.7)
for nm in ('Quảng Tông','Dĩnh Xuyên','Lạc Dương','Hứa','Nghiệp','Nam Dương','Bình Nguyên','Cự Dã'): show(nm,18,35)
KV=[(115.0,37.0),(113.6,34.3),(112.5,33.0),(116.1,35.4),(118.4,36.6),(117.9,34.3),(117.0,32.2),(113.0,31.0)]
G('Trương Giác',YW,10,[(R(18),*X('Quảng Tông'))],show=(R(18),E(28)),emb='sun',seed=31,alive=[(0,1),(R(28,2),1),(R(28,6),0.15)],defeats=[(R(28,3),'lose',INF)])
for i,(lo,la) in enumerate(KV[1:]):
    G('Khăn Vàng',YW,6,[(R(19,1+i*0.4),lo,la)],show=(R(19,1+i*0.4),R(29)),emb='sun',seed=40+i,label=(i==0),alive=[(0,1),(R(28,2),1),(R(28,7),0.2)])
LT(22,1.5,4.0,(115.0,37.1),X('Lạc Dương'),'Đường Chu đi báo quan')
NT(22,5.5,3.0,112.45,34.62,'bắt giết cả ngàn người',(120,30,26))
NT(21,1.0,5,115.0,37.45,'khăn vàng trên đầu',YW)
C3(24,0.5,2.2,'Hà Tiến','anh trai của hoàng hậu',BR);C3(24,2.8,2.4,'Hoàng Phủ Tung','tướng nhà Hán',GD);C3(24,5.0,2.3,'Chu Tuấn','tướng nhà Hán',GD)
G('Quân nhà Hán',GD,10,[(R(24,2),*X('Lạc Dương')),(R(26,0),113.6,34.1)],show=(R(24,2),R(28,6)),emb='dia',seed=51,soff=(-130,60))
G('Lư Thực',GD,8,[(R(24,3),*X('Lạc Dương')),(R(25,0),114.9,36.8)],show=(R(24,3),R(28,5)),emb='dia',seed=52,soff=(-110,80))
C3(25,0.5,3.0,'Lư Thực','vây Trương Giác',GD)
NT(25,4.0,3.0,115.0,37.45,'không đưa quà, bị giam',(120,30,26))
NT(26,0.8,4,113.6,34.55,'trại giữa đồng cỏ khô',YW)
nt(27,0.2,8.5);FIRES.append((R(27,1.0),R(27,9),113.6,34.25));FIRES.append((R(27,1.5),R(27,9),113.66,34.31));FIRES.append((R(27,2.0),R(27,9),113.55,34.3))
C3(27,3.0,3.5,'Tào Tháo','mới 29 tuổi',BL)
G('Tào Tháo',BL,3,[(R(27,3),113.5,34.0)],show=(R(27,3),R(28,0)),emb='dia',seed=53,soff=(-80,90))
SKULL(28,1.0,4.5,115.0,37.1,'Trương Giác mất vì bệnh')
J(29,'fire','Ngọn lửa nhỏ vẫn còn đó',1.0)
C3(30,0.4,3.0,'Tào Tháo','con nhà quan lại',BL);C3(30,3.6,3.2,'Tôn Kiên','người Giang Đông',OR)
C3(31,0.5,3.4,'Lưu Bị','quan nhỏ ở An Hỷ',GR)
NT(31,1.0,5,115.2,38.2,'An Hỷ · chức nhỏ',GR)
G('Lưu Bị',GR,4,[(0,115.2,38.15)],show=(R(31),R(33)),emb='sun',seed=54)
C3(32,0.4,2.8,'Quan Vũ','anh em kết nghĩa',GR);C3(32,3.4,2.8,'Trương Phi','anh em kết nghĩa',GR)
G('Quan Vũ · Trương Phi',GR,4,[(0,115.4,38.1)],show=(R(32),R(33)),emb='sun',seed=55,soff=(120,30))
NT(33,1.0,5.5,113.0,34.5,'năm 188: châu mục được cầm quân',GD)
J(34,'flag','Quan có quân thì thích dẹp… hoàng đế',1.8)
# ======================= CHƯƠNG 3: TRANH CUNG ĐÌNH (36–50)
S(36,40,112.6,34.6,3.8);S(41,41,111.0,34.5,2.2);S(42,44,112.45,34.65,4.4);S(45,46,112.6,34.5,3.6);S(47,50,112.4,34.6,3.4)
for nm in ('Lạc Dương','Mi Ổ','Trường An','Vũ Quan','Huỳnh Dương'): show(nm,36,50)
OW('Lạc Dương',GD);OW('Trường An',NEU,(55,3,BK))
C3(36,0.5,3.0,'Linh Đế','hoàng đế vừa mất',GD)
C3(37,0.5,3.0,'Hà Tiến','cậu của Thiếu Đế',BR)
G('Hà Tiến',BR,8,[(0,112.35,34.55)],show=(R(37),R(42,4)),emb='tri',seed=61,soff=(-130,0))
G('Hoạn quan',DK,6,[(0,112.55,34.7)],show=(R(38),R(44,3)),emb='dia',seed=62,soff=(110,-20))
J(38,'flag','Một ghế, hai người cùng ngồi',2.0)
C3(40,0.5,3.2,'Viên Thiệu','khuyên gọi tướng về',PU)
G('Đổng Trác',BK,12,[(R(41,0),109.5,34.3),(R(41,6),112.2,34.5)],show=(R(41),R(50,9)),emb='tri',seed=63,kind='cav',alive=[(0,1),(R(47,0),0.35),(R(47,4),1.0)])
C3(41,0.5,3.4,'Đổng Trác','tướng vùng Tây Bắc',BK);NT(41,4.5,3.5,111.2,34.45,'dẫn sói vào nhà',(120,30,26))
NT(42,1.0,4.0,112.45,34.62,'Hà Tiến bị giết trong cung',(120,30,26));J(42,'scroll','Một cuộc họp, một kết cục',4.5)
FIRES.extend([(R(43,0.5),R(44,2),112.4,34.58),(R(43,1.0),R(44,2),112.5,34.66),(R(43,1.5),R(44,1),112.46,34.7)]);nt(43,0,12)
G('Viên Thiệu · Viên Thuật',PU,8,[(R(43,0),112.0,34.5),(R(43,2),112.4,34.62)],show=(R(43),R(44,6)),emb='tri',seed=64,soff=(-130,60))
C3(44,0.5,3.0,'Trương Nhượng','hoạn quan đầu sỏ',DK);NT(44,3.5,3.5,112.8,34.9,'hai đứa bé lạc trong đêm',(120,100,40))
C3(45,0.5,3.2,'Lưu Hiệp','em của Thiếu Đế, bình tĩnh',GD);NT(45,3.6,3,112.8,34.9,'cậu bé nói rành rọt',GD)
J(46,'coin','Một nhận xét chính trị, hậu quả rất lớn',2.0)
NT(47,0.5,5.5,112.6,34.9,'ban đêm ra, ban ngày vào',BK)
C3(48,0.5,3.0,'Lữ Bố','giết cha nuôi, theo Đổng Trác',DK)
C3(49,0.5,3.2,'Hiến Đế','ông vua cuối của nhà Hán',GD)
J(50,'flag','Triều đình chỉ còn là chữ ký',2.0)
# ======================= CHƯƠNG 4: LIÊN QUÂN (51–74)
S(51,51,112.6,34.5,3.0);S(52,54,113.5,34.8,1.9);S(55,56,110.6,34.4,2.3);S(57,58,112.45,34.62,4.5);S(59,62,113.4,34.8,3.2)
S(63,68,112.8,33.9,2.7);S(69,72,113.8,34.7,1.7);S(73,74,114.5,35.2,1.35)
for nm in ('Lạc Dương','Trường An','Huỳnh Dương','Lỗ Dương','Nam Dương','Nghiệp','Hứa','Mi Ổ','Vũ Quan'): show(nm,51,74)
NT(51,1.0,5,112.45,34.62,'cướp bóc, đào mồ',(120,30,26))
L4=[('Viên Thiệu',PU,(113.2,35.1)),('Tào Tháo',BL,(114.6,34.75)),('Viên Thuật',RD,(112.9,33.4)),('Trương Mạc',TL,(115.0,35.4)),('Hàn Phức',BR,(114.35,36.3)),('Tôn Kiên',OR,(113.0,33.1)),('Công Tôn Toản',OL,(116.4,39.7))]
for i,(nm,col,(lo,la)) in enumerate(L4):
    G(nm,col,6,[(0,lo,la)],show=(R(52,1+i*0.5),R(69,0)),emb='tri' if i%2 else 'dia',seed=70+i)
C3(52,0.8,3.6,'Viên Thiệu','đứng đầu liên quân',PU)
NT(53,1.0,6.5,113.5,35.5,'mười mấy đạo quân, mỗi người một chỗ',(120,100,40))
J(54,'flag','Không ai chịu gõ cửa đầu tiên',2.0)
G('Dân Lạc Dương',BR,16,[(R(55,2),112.45,34.55),(R(56,6),108.95,34.3)],show=(R(55,2),R(57,0)),emb='circle',seed=81,label=True,alive=[(0,1),(R(56,0),1),(R(56,7),0.55)])
G('Đổng Trác',BK,12,[(R(55,2),112.45,34.62),(R(56,6),108.95,34.3)],show=(R(55,2),R(58,0)),emb='tri',seed=82,kind='cav',soff=(100,-40))
NT(56,1.0,5,111.0,34.5,'người chết đầy đường',(120,30,26))
FIRES.extend([(R(57,0.5),R(58,6),112.4,34.58),(R(57,1.0),R(58,6),112.5,34.66),(R(57,1.5),R(58,6),112.46,34.54),(R(57,2.0),R(58,6),112.55,34.6)]);nt(57,0,15)
NU(57,'200 DẶM','quanh kinh đô gần như không còn nhà',3.0)
OW('Lạc Dương',GD,(57,3,DK))
Q(59,'sao ai cũng chờ','Sao ai cũng chờ?','Tào Tháo',BL,3.0)
G('Tào Tháo',BL,8,[(R(59,2),114.6,34.75),(R(60,0),113.4,34.75)],show=(R(59,2),R(62,0)),emb='dia',seed=91,soff=(-140,40),defeats=[(R(60,5),'lose',R(62))],alive=[(0,1),(R(60,3),1),(R(60,8),0.5)])
G('Từ Vinh',BK,10,[(R(60,0),112.8,34.7),(R(60,2),113.35,34.77)],show=(R(60,0),R(62,0)),emb='tri',seed=92,kind='cav')
BATT.append((R(60,3),R(60,8),113.4,34.77,['Tào Tháo','Từ Vinh']))
C3(61,0.4,3.2,'Tào Hồng','em họ của Tào Tháo',BL)
Q(61,'Thiên hạ có thể','Thiên hạ có thể không có Tào Hồng này, chứ không thể không có ông.','Tào Hồng',BL,6.5)
G('Tôn Kiên',OR,9,[(R(63,0),113.0,33.1),(R(63,6),112.7,34.35),(R(65,0),112.5,34.5)],show=(R(63,0),R(67,3)),emb='moon',seed=93,kind='cav',soff=(-130,40))
C3(63,0.5,3.0,'Tôn Kiên','đánh thật sự',OR)
G('Hoa Hùng',BK,8,[(R(63,5),112.5,34.3)],show=(R(63,5),R(65,0)),emb='tri',seed=94,defeats=[(R(64,3),'skull',INF)],alive=[(0,1),(R(64,3),1),(R(64,4),0.2)])
BATT.append((R(63,7),R(64,4),112.55,34.3,['Tôn Kiên','Hoa Hùng']))
C3(64,0.4,2.8,'Hoa Hùng','tướng của Đổng Trác',BK)
J(64,'scroll','Người ra trận lập công, người ăn tiệc lập danh sách khách mời',3.0)
NT(65,1.0,5.5,112.45,34.65,'dọn dẹp lăng tẩm',OR)
G('Viên Thuật',RD,6,[(0,113.0,33.45)],show=(R(66,0),R(68,6)),emb='tri',seed=95)
NT(66,0.5,5.0,113.0,33.8,'nghi ngờ, không gửi lương',RD)
G('Tôn Kiên',OR,3,[(R(67,0),112.5,34.4),(R(67,4),113.0,33.5)],show=(R(67,0),R(68,6)),emb='moon',seed=96,kind='cav')
Q(67,'vạch đất','Tôi đánh Đổng Trác vì nhà Hán, không vì tôi.','Tôn Kiên',OR,5.0)
NT(68,0.5,5,113.0,33.8,'Viên Thuật xấu hổ, đưa lương lại',RD)
NU(69,'LIÊN QUÂN TAN','không ai chịu để người khác lập công',1.5)
Q(71,'từ chối','Làm vua riêng thì khác gì Đổng Trác.','Tào Tháo',BL,4.5) if False else None
NT(71,1.0,5,114.6,34.75,'Tào Tháo từ chối',BL)
reg('VIÊN THIỆU',(114.5,37.4),[(113.6,36.0),(113.4,37.2),(113.9,38.45),(116.6,38.45),(116.9,37.4),(116.2,36.3),(115.3,35.85),(114.6,35.78)],NEU,[(R(72,2),PU)])
reg('VIÊN THUẬT',(112.8,32.0),[(111.5,31.2),(111.6,33.6),(113.5,33.8),(114.5,32.6),(114.0,31.2)],NEU,[(R(72,3),RD)])
reg('CÔNG TÔN TOẢN',(116.2,40.6),[(113.5,39.4),(113.5,41.5),(118.8,41.5),(118.8,39.4)],NEU,[(R(72,4),OL)])
reg('TÀO THÁO',(115.5,35.2),[(114.5,34.8),(114.6,35.7),(116.8,36.0),(117.0,34.8)],NEU,[(R(73,0),BL)])
J(74,'flag','Gặp nhau diệt kẻ ác, rồi thành kẻ mạnh mới',2.0)
# ======================= CHƯƠNG 5: ĐỔNG TRÁC CHẾT (75–86)
S(75,75,108.9,34.3,3.4);S(76,78,109.2,34.3,4.0);S(79,81,109.0,34.3,5.0);S(82,83,109.6,34.2,3.0);S(84,86,110.5,34.2,2.2)
for nm in ('Trường An','Mi Ổ','Vũ Quan','Lạc Dương'): show(nm,75,86)
OW('Trường An',BK)
NT(75,1.5,6.0,107.7,34.55,'pháo đài Mi Ổ, lương nhiều năm',BK)
Q(75,'nếu thắng','Nếu thắng, ta làm vua; nếu thua, ta về đây ở yên.','Đổng Trác',BK,6.0)
C3(76,0.5,3.2,'Vương Doãn','quan lớn, người cầm đầu phe chống',GD)
C3(77,0.5,3.2,'Lữ Bố','cận vệ của Đổng Trác',DK)
J(77,'scroll','Hai nỗi lo của một cận vệ',3.5)
G('Lữ Bố',DK,4,[(0,109.1,34.3)],show=(R(77),R(79,6)),emb='dia',seed=101,soff=(120,30),kind='cav')
G('Vương Doãn',GD,4,[(0,108.8,34.25)],show=(R(76),R(79,6)),emb='dia',seed=102,soff=(-130,30))
AR(78,0.8,3.5,(108.8,34.25),(109.1,34.3),GD,'kéo Lữ Bố về phe mình')
G('Đổng Trác',BK,8,[(0,108.95,34.4)],show=(R(75),R(79,6)),emb='tri',seed=103,defeats=[(R(79,5),'skull',INF)],alive=[(0,1),(R(79,5),1),(R(79,6),0.2)])
NU(79,'THÁNG TƯ · 192','Lữ Bố ra tay trước cổng cung',0.8)
SKULL(79,5.0,5.0,108.95,34.35,'Đổng Trác bị giết')
J(80,'fire','Dân Trường An đem rượu thịt ra đường ăn mừng',2.0)
nt(81,0,9);FIRES.append((R(81,1.5),R(81,9),108.95,34.25))
NT(81,2.0,5.5,108.95,34.5,'bấc đèn trên bụng',(120,100,40))
G('Lý Thôi · Quách Dĩ',OR,10,[(R(82,0),106.5,34.6),(R(82,6),108.85,34.3)],show=(R(82,0),R(84,0)),emb='tri',seed=104,kind='cav')
C3(82,0.5,3.2,'Lý Thôi','tướng cũ của Đổng Trác',OR);C3(82,3.9,3.2,'Quách Dĩ','tướng cũ của Đổng Trác',OR)
BATT.append((R(82,6),R(83,5),108.95,34.28,['Lý Thôi · Quách Dĩ','Lữ Bố']))
SKULL(83,1.0,5.0,108.95,34.3,'Vương Doãn bị giết')
G('Lữ Bố',DK,3,[(R(83,4),108.95,34.3),(R(83,9),110.2,33.8)],show=(R(83,4),R(85,2)),emb='dia',seed=105,kind='cav')
NT(83,5.0,4.0,109.8,34.0,'Lữ Bố chạy với vài trăm kỵ binh',DK)
J(84,'flag','Cùng hoàng đế, hai nhóm lính, đổi chủ trong vài ngày',2.0)
J(86,'scroll','Giết một con sâu, thấy cả tủ đã mọt',1.5)
# ======================= CHƯƠNG 6: CÁC LÃNH CHÚA CHIA ĐẤT (87–102)
S(87,88,114.4,36.2,3.0);S(89,89,116.4,39.0,2.4);S(90,90,112.8,33.2,2.8);S(91,91,111.5,31.8,2.5);S(92,92,112.3,32.2,3.4);S(93,93,119.8,31.6,2.6)
S(94,97,115.6,35.6,2.7);S(98,99,115.6,35.5,2.8);S(100,100,114.0,33.0,1.2);S(101,102,114.5,35.0,1.3)
for nm in ('Nghiệp','Kế','Nam Dương','Tương Dương','Ngô','Kiến Nghiệp','Cự Dã','Hứa','Lạc Dương','Thọ Xuân'): show(nm,87,102)
OW('Nghiệp',BR,(88,3,PU));OW('Nam Dương',RD);OW('Tương Dương',TL);OW('Ngô',OR);OW('Cự Dã',NEU,(97,0,BL));OW('Hứa',NEU,(98,0,BL))
NT(87,0.8,5.0,114.35,36.7,'Viên Thiệu muốn Ký Châu',PU)
LT(88,0.8,4.5,(114.4,35.4),X('Nghiệp'),'lời khuyên khéo')
G('Viên Thiệu',PU,10,[(R(87,0),114.0,35.6),(R(88,5),114.4,36.2)],show=(R(87,0),R(91,0)),emb='tri',seed=111)
J(88,'scroll','Đánh trận bằng lời',5.5)
G('Ngựa trắng',OL,10,[(0,116.4,39.7)],show=(R(89),R(90,2)),emb='sq',seed=112,kind='cav')
C3(89,0.5,3.5,'Công Tôn Toản','ngựa trắng, phía bắc',OL)
C3(90,0.5,3.0,'Viên Thuật','xa hoa, ở Nam Dương',RD)
G('Lưu Biểu',TL,1,[(R(91,0),110.8,31.4),(R(91,6),112.15,32.0)],show=(R(91,0),R(93,0)),emb='circle',seed=113,kind='cav')
C3(91,0.5,3.4,'Lưu Biểu','quan nhỏ đi ngựa một mình',TL)
G('Tôn Kiên',OR,6,[(R(92,0),113.0,33.3),(R(92,6),112.2,32.1)],show=(R(92,0),R(93,0)),emb='moon',seed=114,kind='cav')
SKULL(92,6.0,5.0,112.1,32.0,'Tôn Kiên mất · 191')
NU(92,'191','Tôn Kiên mất khi mới 36–37 tuổi',3.5)
C3(93,0.5,3.4,'Tôn Sách','mới 17 tuổi',OR)
G('Tôn Sách',OR,5,[(0,120.5,31.2)],show=(R(93),R(94)),emb='moon',seed=115)
G('Khăn Vàng',YW,10,[(R(94,0),115.8,35.5)],show=(R(94,0),R(96,0)),emb='sun',seed=116)
SKULL(94,2.0,5.0,115.7,35.4,'Lưu Đại bị giết')
G('Tào Tháo',BL,10,[(R(95,0),114.6,34.7),(R(95,6),115.7,35.4)],show=(R(95,0),R(102,9)),emb='dia',seed=117,soff=(-110,60),alive=[(0,1),(R(96,0),1),(R(96,6),1.0)])
C3(95,0.5,3.4,'Tào Tháo','được mời làm người đứng đầu',BL)
NU(96,'MẤY CHỤC VẠN','hàng quân Khăn Vàng thành Thanh Châu binh',2.0)
G('Thanh Châu binh',BL,12,[(R(96,5),115.9,35.3)],show=(R(96,5),R(102,9)),emb='sq',seed=118,soff=(110,50))
J(97,'coin','Đạo quân đầu tiên đến từ chính kẻ chống triều đình',2.5)
C3(98,0.5,2.6,'Tuân Úc','mưu sĩ bày đại sự',BL);C3(98,3.2,2.6,'Trình Dục','giữ vững hậu phương',BL);C3(98,5.9,2.4,'Quách Gia','mưu sĩ giỏi',BL)
Q(99,'đất Duyện Châu','Đất Duyện Châu là gốc; giữ vững nó thì tiến có thể đánh, lùi có thể giữ.','Tuân Úc',BL,7.0)
NT(100,0.5,4.0,107.8,33.4,'Ích Châu: Lưu Yên (xa về phía tây)',(110,70,30))
NT(100,4.5,3.5,120.4,31.5,'Giang Đông: chưa vào cuộc',OR)
J(102,'flag','Chưa ai là vua cờ, ai cũng giữ quân thật chặt',1.5)
# ======================= CHƯƠNG 7: LƯU BỊ VÀ TỪ CHÂU (103–125)
S(103,104,116.9,37.0,2.8);S(105,105,117.0,34.3,2.4);S(106,106,117.2,34.7,2.5);S(107,108,117.6,34.7,2.8);S(109,109,116.2,35.4,2.5)
S(110,112,117.8,34.5,3.0);S(113,113,117.7,33.4,2.6);S(114,116,118.0,34.2,3.8);S(117,117,118.6,34.0,2.6);S(118,120,116.9,34.7,3.5)
S(121,123,115.2,34.4,2.0);S(124,125,115.5,34.5,1.8)
for nm in ('Bình Nguyên','Bắc Hải','Lâm Tri','Tiểu Bái','Đàm','Hạ Bì','Hu Di','Hải Tây','Cự Dã','Bộc Dương','Thọ Xuân','Hứa','Lang Gia'): show(nm,103,125)
OW('Hạ Bì',(170,140,50),(110,3,GR),(115,6,DK));OW('Đàm',(170,140,50),(110,3,GR));OW('Tiểu Bái',NEU,(111,0,GR),(121,6,DK));OW('Bình Nguyên',GR);OW('Bộc Dương',BL,(109,0,DK),(125,0,BL));OW('Cự Dã',BL)
OW('Hạ Bì',(170,140,50),(110,3,GR),(115,6,DK))
reg('TỪ CHÂU',(117.9,35.15),[(116.55,35.1),(117.3,35.65),(118.4,35.45),(119.35,34.95),(119.45,34.1),(119.0,33.1),(118.3,32.85),(117.4,33.05),(116.7,33.6),(116.45,34.4)],(170,140,50),[(R(111,2),GR),(R(115,5),DK),(R(173,0),GR)])
G('Lưu Bị',GR,12,[(0,116.43,37.17),(R(107,1),116.43,37.17),(R(108,3),117.5,34.7),(R(110,8),117.2,34.72),(R(111,3),117.9,34.35)],show=(0,R(113,0)),emb='sun',seed=121,alive=[(0,0.5),(R(107,0),0.5),(R(108,4),1.0)])
C3(103,0.5,3.2,'Lưu Bị','giữ Bình Nguyên, dưới Công Tôn Toản',GR)
G('Thái Sử Từ',GR,4,[(R(104,0),116.4,37.1),(R(104,6),118.9,36.65)],show=(R(104,0),R(106,0)),emb='sun',seed=122)
C3(104,0.5,3.2,'Thái Sử Từ','xin cứu Bắc Hải',GR);NT(104,4.0,4.5,119.0,37.0,'3.000 quân, giặc rút',GR)
G('Tào Tung',BK,1,[(R(105,0),115.8,33.9),(R(105,5),118.3,35.05)],show=(R(105,0),R(106,3)),emb='dia',seed=123)
SKULL(105,5.5,4.0,118.3,35.05,'Tào Tung bị giết')
C3(105,0.5,3.0,'Tào Tung','cha của Tào Tháo',BL)
G('Tào Tháo',BL,14,[(R(106,0),116.1,35.4),(R(106,6),117.5,34.6),(R(109,0),117.5,34.6),(R(109,4),116.0,35.4)],show=(R(106,0),R(109,6)),emb='dia',seed=124,soff=(-120,40))
NU(106,'HƠN 10 THÀNH','Tào Tháo báo thù ở Từ Châu',2.0)
G('Đào Khiêm',BR,10,[(0,118.3,34.55)],show=(R(106,3),R(110,6)),emb='tri',seed=125,soff=(100,50))
G('Điền Giai',TL,8,[(R(107,0),118.35,36.8),(R(107,5),118.0,35.2)],show=(R(107,0),R(109,0)),emb='sq',seed=126)
C3(107,0.5,3.0,'Điền Giai','quan đứng đầu Thanh Châu',TL)
C3(108,0.5,3.4,'Đào Khiêm','chia thêm 4.000 quân Đan Dương',BR)
NT(108,3.5,4.0,116.93,34.95,'Lưu Bị giữ Tiểu Bái',GR)
G('Lữ Bố',DK,10,[(R(109,0),114.8,35.2)],show=(R(109,0),R(112,2)),emb='dia',seed=127,kind='cav')
C3(109,0.5,3.0,'Lữ Bố','được Trương Mạc, Trần Cung đón vào',DK)
C3(110,0.5,3.2,'Mi Trúc','dẫn dân cả châu',(190,150,60))
SKULL(110,1.0,5.5,118.3,34.62,'Đào Khiêm mất')
Q(110,'ngoài Lưu Bị','Ngoài Lưu Bị, không ai giữ yên được Từ Châu.','Đào Khiêm',BR,5.0)
C3(111,0.5,3.2,'Trần Đăng','người Hạ Bì',TL)
NT(111,3.8,4.0,117.95,34.65,'nhận Từ Châu bằng sự tin cậy',GR)
G('Lữ Bố',DK,6,[(R(112,0),115.0,35.0),(R(112,5),117.9,34.4)],show=(R(112,0),R(114,0)),emb='dia',seed=128,kind='cav')
NT(112,5.0,4.0,117.95,34.65,'chạy sang nhờ Lưu Bị',DK)
G('Viên Thuật',RD,14,[(R(113,0),116.78,32.6),(R(113,5),118.45,33.0)],show=(R(113,0),R(114,0)),emb='tri',seed=129)
G('Lưu Bị',GR,12,[(R(113,0),117.9,34.35),(R(113,4),118.5,33.2)],show=(R(113,0),R(116,0)),emb='sun',seed=121)
BATT.append((R(113,6),R(113,9),118.5,33.05,['Lưu Bị','Viên Thuật']))
NT(114,1.0,4.5,117.95,34.65,'Trương Phi giữ Hạ Bì',GR);C3(114,1.0,3.0,'Trương Phi','giữ Hạ Bì',GR)
NT(114,5.0,4,117.95,34.0,'trong thành có nội loạn',(120,30,26))
C3(115,0.5,3.0,'Hứa Đam','tướng của Lưu Bị',TL);LT(115,0.6,3.8,(118.2,34.0),(114.8,35.2),'thư mời Lữ Bố vào')
nt(115,2,10);G('Lữ Bố',DK,10,[(R(115,3),114.8,35.2),(R(115,8),117.9,34.35)],show=(R(115,3),R(117,6)),emb='dia',seed=130,kind='cav')
NU(115,'MỘT ĐÊM','Hạ Bì rơi vào tay Lữ Bố',5.0)
J(116,'coin','Nhà chủ không khóa cửa, khách nhìn kỹ cái chìa',2.0)
NT(117,0.5,4,117.95,34.65,'bắt vợ con Lưu Bị',DK);NT(117,4.5,4,119.3,34.15,'rút về Hải Tây, rồi cầu hòa',GR)
G('Lưu Bị',GR,12,[(R(117,0),118.5,33.2),(R(117,4),119.25,33.85),(R(117,9),116.93,34.7)],show=(R(117,0),R(121,0)),emb='sun',seed=121,alive=[(0,0.6),(R(117,0),0.6)])
G('Kỷ Linh',RD,16,[(R(118,0),116.78,32.6),(R(118,6),116.9,34.5)],show=(R(118,0),R(120,9)),emb='tri',seed=131)
NU(118,'3 VẠN QUÂN','Kỷ Linh đánh Tiểu Bái',1.5)
G('Lữ Bố',DK,8,[(R(119,0),117.95,34.3),(R(119,4),116.93,34.6)],show=(R(119,0),R(121,0)),emb='dia',seed=132,kind='cav')
NT(119,3.0,4.5,116.93,34.95,'một cây kích ở cổng doanh',DK)
NT(120,3.0,3.5,116.93,34.95,'TRÚNG!',(120,30,26));NU(120,'MỘT PHÁT','bắn trúng nhánh kích, hai bên bỏ về',5.5)
Q(120,'nếu ta bắn','Nếu ta bắn trúng nhánh nhỏ của cây kích, các ông rút quân.','Lữ Bố',DK,6.0)
G('Lưu Bị',GR,14,[(R(121,0),116.93,34.7),(R(121,5),116.0,34.5),(R(122,5),113.83,34.1)],show=(R(121,0),R(125,9)),emb='sun',seed=121,alive=[(0,1),(R(121,3),1),(R(121,6),0.5)],defeats=[(R(121,5),'lose',R(122,4))])
NU(121,'10.000+ QUÂN','Lưu Bị ở Tiểu Bái, rồi thua Lữ Bố',1.0)
C3(122,0.5,3.2,'Tào Tháo','đãi Lưu Bị rất hậu',BL)
NT(122,3.5,4.5,113.83,34.35,'Lưu Bị làm quan đứng đầu Dự Châu',GR)
C3(123,0.5,3.2,'Trình Dục','khuyên giết Lưu Bị',BL)
Q(123,'giết một người','Giết một người mà mất lòng thiên hạ thì không được.','Tào Tháo',BL,5.5)
J(124,'flag','Có những người ở dưới mình quá lâu thì nhìn ra mọi chỗ hở',1.5)
J(125,'scroll','Hai điều Lưu Bị học được',1.5)
# ======================= CHƯƠNG 8: HOÀNG ĐẾ VỀ HỨA (126–152)
S(126,128,109.0,34.3,4.5);S(129,130,110.6,34.5,2.2);S(131,132,112.45,34.62,4.0);S(133,135,113.5,35.5,1.8);S(136,138,113.4,34.5,2.3)
S(139,140,113.8,34.1,3.6);S(141,142,114.3,35.0,1.7);S(143,146,116.78,32.9,3.0);S(147,150,112.6,33.0,4.2);S(151,152,114.0,34.3,1.6)
for nm in ('Trường An','Vũ Quan','Lạc Dương','Hứa','Nghiệp','Thọ Xuân','Nam Dương','Huỳnh Dương','Quan Độ'): show(nm,126,152)
OW('Hứa',BL);OW('Lạc Dương',DK,(138,4,GD));OW('Trường An',BK)
G('Lý Thôi',OR,10,[(0,108.7,34.25)],show=(R(126),R(129,0)),emb='tri',seed=141,soff=(-110,40))
G('Quách Dĩ',BR,10,[(0,109.2,34.3)],show=(R(126),R(129,0)),emb='dia',seed=142,soff=(110,-30))
C3(126,0.5,2.8,'Lý Thôi','nắm quyền ở Trường An',OR);C3(126,3.5,2.8,'Quách Dĩ','nắm quyền ở Trường An',BR)
BATT.append((R(127,2),R(128,6),108.95,34.3,['Lý Thôi','Quách Dĩ']))
NT(127,0.5,4,108.95,34.65,'một người bắt hoàng đế, một người bắt các quan',(120,100,40))
NT(128,1.0,5.0,108.95,34.65,'đói, hết lương',(120,30,26));J(127,'flag','Họ cãi nhau bằng quân',5.5)
nt(129,0,9)
G('Hiến Đế',GD,3,[(R(129,0),108.95,34.27),(R(129,8),110.5,34.6),(R(130,6),111.6,34.6)],show=(R(129,0),R(131,2)),emb='sun',seed=143)
NT(129,2.0,5.0,109.8,34.4,'trốn trong đêm, vượt sông',GD)
G('Quân truy đuổi',BK,8,[(R(130,0),109.5,34.3),(R(130,5),111.0,34.55)],show=(R(130,0),R(131,0)),emb='tri',seed=144,kind='cav')
BATT.append((R(130,3),R(130,7),110.9,34.55,['Quân truy đuổi','Hiến Đế']))
NU(131,'THÁNG BẢY · 196','Hiến Đế về tới Lạc Dương cháy trơ',0.8)
NT(131,4.5,4,112.45,34.9,'căn nhà nhỏ, mái đổ',GD)
J(132,'coin','Hoàng đế của hàng trăm triệu dân xin cơm từng bữa',2.5)
C3(133,0.5,2.8,'Viên Thiệu','có đất lớn',PU);C3(133,3.4,2.8,'Tào Tháo','có đầu óc nhanh',BL)
C3(134,0.5,3.2,'Thư Thụ','mưu sĩ của Viên Thiệu',PU)
Q(134,'đón hoàng đế','Đón hoàng đế về, dùng danh nghĩa nhà Hán để ra lệnh cho các lãnh chúa.','Thư Thụ',PU,7.0)
J(135,'coin','Giữ hoàng đế nghèo thì tốn kém, lại phải nghe lời',2.0)
C3(136,0.5,3.0,'Tuân Úc','khuyên đón hoàng đế',BL);C3(137,0.5,3.0,'Mao Giới','khuyên mang vua trong tay',BL)
G('Tào Tháo',BL,14,[(R(138,0),115.7,35.4),(R(138,3),112.5,34.6),(R(138,7),113.8,34.1)],show=(R(137,5),R(152,9)),emb='dia',seed=145,soff=(-120,50))
NU(138,'THÁNG TÁM · 196','Tào Tháo đón Hiến Đế về Hứa',0.8)
LT(139,1.0,4.0,'Hứa','Lạc Dương','mệnh lệnh nhân danh nhà Hán') if False else None
J(139,'scroll','Mọi lệnh đều đóng dấu nhà Hán',2.0)
NT(140,1.0,6.0,113.8,34.4,'cày ruộng lấy lương',(120,100,40))
LT(141,0.5,4.0,'Nghiệp','Hứa','Viên Thiệu giận');NT(142,1.0,5.0,114.35,36.7,'Viên Thiệu chuẩn bị đánh Tào',PU)
G('Viên Thuật',RD,14,[(0,116.78,32.6)],show=(R(143,0),R(146,9)),emb='tri',seed=146,alive=[(0,1),(R(145,0),1),(R(145,8),0.2)])
NU(143,'197','Viên Thuật tự xưng hoàng đế',2.0)
J(144,'flag','Xưng đế mà không ai theo chỉ là người mặc áo đẹp ngồi trong phòng',2.0)
SKULL(145,4.0,5.0,116.78,32.6,'Viên Thuật mất · 199')
J(146,'coin','Một ly nước mật ong',1.5)
G('Tào Tháo',BL,10,[(R(147,0),113.8,34.2),(R(147,5),112.55,33.05)],show=(R(147,0),R(148,0)),emb='dia',seed=147,soff=(-120,50))
G('Trương Tú',BR,10,[(0,112.5,32.95)],show=(R(147,0),R(150,5)),emb='tri',seed=148,soff=(110,-20))
C3(147,0.5,3.0,'Trương Tú','hàng ở Uyển Thành',BR)
nt(148,0,9);BATT.append((R(148,5),R(149,8),112.55,33.0,['Trương Tú','Tào Tháo']))
NT(148,1.0,4,112.55,33.35,'lấy vợ góa của chú Trương Tú',(120,100,40))
C3(149,0.5,3.0,'Điển Vi','chặn cửa doanh',BL);SKULL(149,2.0,6.0,112.5,33.0,'Điển Vi · Tào Ngang · Tào An Dân')
Q(150,'lỗi này','Lỗi này là của ta, từ nay phải biết dừng.','Tào Tháo',BL,5.0)
J(151,'flag','Cầm hoàng đế mạnh thật, nhưng chưa đủ thắng mọi trận',2.0)
J(152,'scroll','Mũ đẹp vẫn phải đội trên đầu biết nghĩ',1.0)
# ======================= CHƯƠNG 9: LỮ BỐ CHẾT (153–176)
S(153,155,117.6,34.4,2.8);S(156,157,117.95,34.3,4.4);S(158,159,117.9,34.4,3.2);S(160,160,117.9,34.3,3.6);S(161,164,117.95,34.3,5.2)
S(165,169,117.95,34.3,4.6);S(170,172,115.8,34.2,1.9);S(173,173,117.9,34.3,3.0);S(174,176,116.0,35.3,2.0)
for nm in ('Hạ Bì','Tiểu Bái','Hứa','Đàm','Nghiệp','Lang Gia','Bộc Dương'): show(nm,153,176)
OW('Hạ Bì',DK,(173,0,GR),(175,2,BL));OW('Tiểu Bái',DK,(156,0,BL))
RIVERS.append(('SÔNG TỨ',[(116.95,35.7),(117.2,35.3),(117.55,34.95),(117.75,34.62),(117.95,34.3),(118.15,33.9),(118.3,33.5)],5,None))
G('Lữ Bố',DK,16,[(0,117.95,34.3)],show=(R(153),R(165,4)),emb='dia',seed=151,kind='cav',defeats=[(R(165,2),'skull',INF)],alive=[(0,1),(R(160,0),1),(R(161,6),0.6)])
NT(154,1.0,5,117.95,34.65,'giữ lời rồi trở mặt',DK)
G('Lưu Bị',GR,10,[(0,116.93,34.7)],show=(R(153),R(156,0)),emb='sun',seed=152,defeats=[(R(155,2),'lose',R(156,0))])
NT(155,3.0,4,116.93,35.05,'vợ con lại bị bắt',(120,30,26))
G('Tào Tháo',BL,16,[(R(156,0),115.5,35.0),(R(156,5),117.5,34.4)],show=(R(156,0),R(170,0)),emb='dia',seed=153,soff=(-130,60))
G('Lưu Bị',GR,8,[(R(156,2),116.9,34.7),(R(156,6),117.6,34.3)],show=(R(156,2),R(170,0)),emb='sun',seed=152,soff=(-70,-20))
NU(156,'3 THÁNG','Quân Tào vây Hạ Bì',2.0)
C3(157,0.5,3.0,'Trần Cung','mưu sĩ của Lữ Bố',(130,90,90))
Q(157,'đem quân ra ngoài','Đem quân ra ngoài đánh, tôi giữ thành, hai bên cùng đỡ nhau.','Trần Cung',(130,90,90),6.0)
J(158,'flag','Một võ tướng nổi danh dũng, mà không dám rời nhà',2.0)
C3(159,0.5,2.8,'Tuân Du','khuyên đánh tiếp',BL);C3(159,3.5,2.8,'Quách Gia','khuyên đánh tiếp',BL)
OBJ.append((R(160,1.0),R(167,0),'flood',(117.95,34.3),(117.95,34.3)))
NU(160,'HƠN 1 THÁNG','nước ngập quanh Hạ Bì',3.5)
C3(161,0.5,3.2,'Hầu Thành · Tống Hiến · Ngụy Tục','phản, mở cổng thành',DK)
NT(161,4.0,5,117.95,34.65,'Lữ Bố trèo lên Bạch Môn Lâu',DK)
def gate_open(t): return 1 if R(161,3)<=t<=R(163,0) else 0
Q(162,'trói chặt','Trói chặt quá, nới ra cho ta.','Lữ Bố',DK,3.0)
Q(162,'trói hổ','Trói hổ sao không chặt?','Tào Tháo',BL,3.0) if False else None
Q(163,'cho tôi cầm','Cho tôi cầm kỵ binh, ông cầm bộ binh, thiên hạ không khó định.','Lữ Bố',DK,6.0)
C3(164,0.5,3.0,'Lưu Bị','nhắc Tào Tháo',GR)
SKULL(165,2.0,6.0,117.95,34.3,'Lữ Bố bị xử tử')
C3(166,0.5,3.0,'Trần Cung','xin chết',(130,90,90))
NT(167,1.0,5.0,117.95,34.65,'Tào Tháo lo cho mẹ và vợ con Trần Cung',BL)
J(168,'flag','Đi theo người mạnh, và người dưới cũng làm đúng như thế',2.0)
J(169,'scroll','Ai từng trở mặt khó đòi người khác không trở mặt',1.0)
G('Lưu Bị',GR,10,[(R(170,0),117.95,34.3),(R(170,6),113.83,34.1)],show=(R(170,0),R(173,0)),emb='sun',seed=152)
NT(171,1.0,6,113.83,34.4,'giả vờ trồng rau',GR)
C3(172,0.5,3.2,'Đổng Thừa','mật chiếu trên đai áo',(130,90,90))
LT(172,3.5,3.5,'Hứa',(113.6,34.4),'mật chiếu') if False else None
G('Lưu Bị',GR,10,[(R(173,0),113.83,34.1),(R(173,6),117.9,34.35)],show=(R(173,0),R(175,0)),emb='sun',seed=152)
NT(173,3.0,4.5,117.95,34.65,'giết quan Tào, lấy lại Từ Châu',GR)
SKULL(174,1.0,5.5,113.83,34.0,'âm mưu Đổng Thừa bị lộ')
G('Tào Tháo',BL,16,[(R(175,0),113.83,34.1),(R(175,6),117.95,34.4)],show=(R(175,0),R(177,0)),emb='dia',seed=153)
G('Lưu Bị',GR,8,[(R(175,2),117.95,34.3),(R(175,7),114.35,36.3)],show=(R(175,2),R(177,0)),emb='sun',seed=152,defeats=[(R(175,3),'lose',INF)])
NT(175,5.0,4.5,114.35,36.7,'chạy sang Viên Thiệu',PU)
J(176,'flag','Lần thứ hai mất Từ Châu; quen không có nghĩa là thích',2.0)
# ======================= CHƯƠNG 10: QUAN ĐỘ (177–206), lấy từ bản thử
S(177,177,114.9,36.35,2.0);S(178,178,114.6,35.9,2.0);S(179,180,114.35,36.3,3.0);S(181,181,114.5,35.85,3.0);S(182,182,114.25,35.3,3.3)
S(183,183,114.48,35.45,4.2);S(184,184,114.4,35.7,3.0);S(185,185,114.25,35.2,2.4);S(186,187,114.3,35.4,2.8);S(188,189,114.25,35.1,4.0)
S(190,192,114.08,34.9,4.4);S(193,195,113.95,34.4,3.0);S(196,197,114.12,34.85,4.0);S(198,198,114.3,34.95,3.5);S(199,200,114.08,34.85,4.4)
S(201,202,114.3,35.4,2.9);S(203,204,114.05,34.8,4.4);S(205,206,114.3,36.0,1.9)
for nm in ('Hứa','Nghiệp','Quan Độ','Bạch Mã','Diên Tân','Ô Sào','Lê Dương','Lâm Tri','Lạc Dương'): show(nm,177,206)
OW('Hứa',BL);OW('Quan Độ',BL);OW('Diên Tân',BL);OW('Bạch Mã',BL);OW('Nghiệp',PU);OW('Lê Dương',PU);OW('Lâm Tri',PU);OW('Ô Sào',PU,(198,6,DK))
RIVERS.append(('HOÀNG HÀ',[(110.6,34.78),(111.5,34.86),(112.6,34.98),(113.5,35.03),(114.1,35.2),(114.5,35.67),(115.1,36.05),(115.9,36.5),(116.7,37.2),(117.6,37.7),(118.6,37.95),(119.6,38.2)],7,(115.75,36.35)))
TITLES.append((R(177,-0.2),R(177,3.8),'NĂM 200','QUAN ĐỘ','Viên Thiệu đối đầu Tào Tháo'))
reg('KÝ CHÂU',(114.9,37.3),[(113.6,36.0),(113.4,37.2),(113.9,38.45),(116.6,38.45),(116.9,37.4),(116.2,36.3),(115.3,35.85),(114.6,35.78)],PU,[(R(205),PUF)])
reg('TINH CHÂU',(111.9,37.3),[(110.3,36.0),(110.2,38.45),(113.4,38.45),(113.6,36.0)],PU,[(R(205),PUF)])
reg('THANH CHÂU',(118.5,37.45),[(116.9,37.4),(116.6,38.45),(120.2,38.45),(121.0,37.2),(120.2,36.4),(118.4,36.0),(117.2,36.2)],PU,[(R(205),PUF)])
reg('ĐẤT TÀO THÁO',(112.7,33.7),[(111.5,33.2),(111.6,34.95),(113.5,35.02),(114.1,35.12),(114.9,35.0),(116.5,34.7),(116.5,33.2),(114.5,32.9)],BL)
NU(198,'5.000 QUÂN','đêm đi tắt tới Ô Sào',1.6);NU(201,'KHOẢNG 800','kỵ binh theo Viên Thiệu qua sông',1.6)
NG=L('Nghiệp',0.02,0.14);LD=(114.75,36.0);QD=(114.0,34.68);VC=(114.1,34.95);BM=(114.45,35.62);DT=(114.2,35.1);OS=X('Ô Sào')
# Viên Thiệu (quân chính)
G(name='Viên Thiệu',col=PU,n=16,emb='tri',seed=2,soff=(170,10),show=(R(177),R(201)+6),
  keys=[(R(177),*NG),(R(181)-0.5,*NG),(R(181)+6,*LD),(R(190)-1,*LD),(R(190)+5,*VC),(R(199)+1,*VC),(R(199)+3.2,114.05,34.8)],
  alive=[(0,1),(R(199)+2,1),(R(200)+3.5,0.1)],defeats=[(R(200)+3.5,'lose',INF)])
# Tào Tháo (quân chính)
G(name='Tào Tháo',col=BL,n=12,emb='dia',seed=4,soff=(-190,10),show=(R(177),INF),
  keys=[(R(177),*L('Hứa',0,-0.1)),(R(180),*L('Hứa',0,-0.1)),(R(181)+6,*QD),(R(182)+1.0,*QD),(R(182)+3.0,*DT),(R(182)+3.6,*DT),(R(182)+7.2,114.4,35.32),(R(187)-0.5,114.4,35.32),
        (R(188)+4,*DT),(R(189)+6,*DT),(R(190)+4,*QD)])
# Bạch Mã
G(name='Nhan Lương',col=PU,n=7,kind='cav',emb='tri',seed=6,show=(R(181)-0.5,R(184)+3),
  keys=[(R(181)-0.5,*LD),(R(181)+4,114.38,35.7),(R(184)+4,114.38,35.7)],defeats=[(R(183)+5.2,'skull',INF)],
  alive=[(0,1),(R(183)+5,1),(R(183)+6,0.2)])
G(name='Lưu Diên',col=BL,n=4,emb='dia',seed=7,soff=(90,30),show=(R(181)+3,R(184)+3),keys=[(0,114.55,35.52)])
G(name='Quan Vũ',col=GR,n=3,kind='cav',emb='sun',seed=8,show=(R(183)-0.5,R(187)+3),
  keys=[(R(183)-0.5,114.34,35.28),(R(183)+2,114.34,35.28),(R(183)+4.4,114.42,35.6),(R(183)+7,114.36,35.34),(R(186)+0.6,114.36,35.34),(R(186)+7,114.38,36.1)])
G(name='Lưu Bị',col=GR,n=5,emb='sun',seed=9,show=(R(184)-0.5,R(188)),keys=[(0,114.4,36.15)])
# Diên Tân
G(name='Văn Sửu',col=PU,n=7,kind='cav',emb='tri',seed=10,show=(R(188)-0.3,R(190)-0.5),
  keys=[(R(188)-0.3,114.5,35.6),(R(188)+5,114.25,35.2),(R(189)+7,114.25,35.2)],defeats=[(R(189)+5.8,'skull',INF)],
  alive=[(0,1),(R(189)+5.5,1),(R(189)+6.5,0.2)])
# Hứa Du, đột kích Ô Sào
G(name='Hứa Du',col=OL,n=1,emb='dia',seed=11,show=(R(196)+3.5,R(198)),keys=[(R(196)+3.5,*VC),(R(196)+7,114.03,34.76),(R(198),114.03,34.76)])
G(name='quân canh kho',col=PU,n=4,emb='tri',seed=12,show=(R(197)+3,R(198)+7.5),keys=[(0,*OS)],defeats=[(R(198)+6.8,'lose',INF)],
  alive=[(0,1),(R(198)+6,1),(R(198)+7,0.2)])
G(name='quân mang cờ Viên Thiệu',col=PU,n=9,emb='tri',seed=13,show=(R(198)+0.4,R(198)+4.3),keys=[(R(198)+0.4,*QD),(R(198)+4.2,114.55,35.0)])
G(name='Tào Tháo',col=BL,n=9,emb='dia',seed=14,show=(R(198)+4.3,R(199)+4),keys=[(0,114.55,35.0)],soff=(0,40))
# Trương Cáp, Cao Lãm
G(name='Trương Cáp · Cao Lãm',col=PU,n=5,emb='tri',seed=15,show=(R(199)+0.3,R(199)+4.6),keys=[(R(199)+0.3,*VC),(R(199)+3.6,114.03,34.77),(R(199)+5,114.03,34.77)],soff=(40,0))
G(name='Trương Cáp · Cao Lãm',col=BL,n=5,emb='dia',seed=16,show=(R(199)+4.6,R(201)),keys=[(0,114.03,34.77)],soff=(40,0))
# Viên Thiệu bỏ chạy
G(name='Viên Thiệu',col=PU,n=4,kind='cav',emb='tri',seed=17,show=(R(201)+0.3,R(202)),keys=[(R(201)+0.3,*VC),(R(201)+4,114.4,35.4),(R(201)+7.6,114.7,35.95)])
BATT+=[(R(183)+3.6,R(183)+6.8,114.5,35.6,['Quan Vũ','Nhan Lương']),
      (R(189)+3.2,R(189)+6.3,114.25,35.17,['Văn Sửu','Tào Tháo']),
      (R(199)+2.2,R(200)+3.4,114.04,34.79,['Viên Thiệu','Tào Tháo'])]
FIRES+=[(R(198)+5,R(200)+2,*OS),(R(198)+5.4,R(200)+1,OS[0]+0.04,OS[1]+0.03),(R(198)+5.8,R(200)+1.5,OS[0]-0.04,OS[1]+0.03),
       (R(203)+2.5,E(203),113.96,34.66)]
NIGHT+=[(0,0),(R(196)+2,0),(R(196)+4,0.6),(R(198)+9,0.6),(R(199)+1,0)]
# công trình
TW=[(113.97,34.87),(114.07,34.88),(114.17,34.87)]
OBJ+=[];FX=[(R(181)+4.5,R(181)+7,'horn',(114.45,35.62),(114.45,35.62))]
for j,tw in enumerate(TW):
    c0=R(191)+0.4+j*2.4
    OBJ.append((R(190)+2.0+j*0.5,c0+1.5,'tower',tw,tw))
    FX.append((R(190)+2.6+j*0.5,c0+1.5,'volley',tw,(114.02,34.72)))
    FX.append((c0,c0+2.2,'catapult',(114.05,34.70),tw))
OBJ+=[(R(192)+0.5,R(192)+8,'tunnel',(114.08,34.96),(114.0,34.78)),(R(192)+4,INF,'ditch',(113.86,34.8),(114.16,34.8)),
      (R(188)+2.5,R(189)+3,'loot',(114.48,35.5),(114.22,35.14))]
LETTERS+=[(R(186)+0.4,R(186)+4,X('Bạch Mã'),X('Quan Độ'),'thư từ biệt'),(R(193)+2,R(193)+5.5,X('Quan Độ'),X('Hứa'),'nên rút không?'),
         (R(194)+0.5,R(194)+3.6,X('Hứa'),X('Quan Độ'),'xin ông cứ giữ')]
ARROWS+=[(R(182)+1.0,R(182)+3.6,X('Quan Độ'),X('Diên Tân'),BL,'giả vờ ở Diên Tân'),(R(182)+4.2,R(182)+7.4,X('Diên Tân'),X('Bạch Mã'),RD,'đánh gấp Bạch Mã'),
        (R(205)+3,E(205)-0.3,X('Quan Độ'),X('Nghiệp'),BL,'phía bắc không còn đối thủ')]
NOTES+=[(R(180)+3.6,E(180)-0.3,*L('Nghiệp'),'Điền Phong bị giam',DK),(R(184)+0.6,R(184)+3.8,114.46,35.38,'Hán Thọ đình hầu',GR),
       (R(196)+7,R(197)+2.5,114.03,34.76,'Hứa Du đào ngũ',OL),(R(199)+4.6,R(200)+2.4,114.03,34.77,'đầu hàng Tào Tháo',BL),
       (R(202)+3.5,E(202)-0.2,114.0,34.7,'chồng thư bắt được',(110,70,30)),(R(177)+0.6,R(178)+0.5,114.9,38.2,'U Châu ở xa hơn về phía bắc',PU)]
MARKS+=[]
def cd(n,sub,dur,name,role,col,off=0.0): 
    t0=at(n,sub,off);return (t0,min(t0+dur,E(n)-0.2),name,role,col)
CARDS3+=[cd(179,'Điền Phong và',4.3,'Điền Phong','khuyên kéo dài',TL),cd(179,'Điền Phong và',4.3,'Thư Thụ','khuyên kéo dài',TL),
 cd(179,'Thẩm Phối',9,'Thẩm Phối','khuyên đánh ngay',OR),cd(179,'Thẩm Phối',9,'Quách Đồ','khuyên đánh ngay',OR),
 cd(181,'Nhan Lương dẫn',3.6,'Nhan Lương','tiên phong của Viên Thiệu',PU),cd(182,'Tuân Du',3.4,'Tuân Du','mưu sĩ của Tào Tháo',BL),
 cd(183,'Trương Liêu và',3.4,'Quan Vũ','tướng của Lưu Bị',GR),cd(185,'Trương Liêu',3.0,'Trương Liêu','tướng của Tào Tháo',BL),
 cd(188,'Văn Sửu',3.8,'Văn Sửu','tướng giỏi thứ hai của Viên Thiệu',PU),cd(193,'Tuân Úc',3.4,'Tuân Úc','giữ Hứa cho Tào Tháo',BL),
 cd(196,'Hứa Du',3.6,'Hứa Du','mưu sĩ của Viên Thiệu',OL),
 cd(199,'Hai tướng',5.5,'Trương Cáp','tướng của Viên Thiệu',PU),cd(199,'Hai tướng',5.5,'Cao Lãm','tướng của Viên Thiệu',PU)]
QUOTES+=[(at(185,'đã thề'),E(185)-0.1,'Ta đã thề cùng sống chết với Lưu tướng quân, không thể phụ.','Quan Vũ',GR),
 (at(186,'mỗi người một chủ'),E(186)-0.1,'Mỗi người một chủ, để ông ấy đi.','Tào Tháo',BL),
 (at(194,'lùi trước'),E(194)-0.1,'Ai lùi trước, người ấy thua. Xin ông cứ giữ.','Tuân Úc',BL),
 (at(197,'kho lương của'),at(197,'kho lương của')+5.2,'Kho lương của Viên Thiệu ở Ô Sào, chỉ có một ít quân canh giữ.','Hứa Du',OL),
 (at(203,'Ông nói'),E(203)-0.1,'Lúc Viên Thiệu mạnh như vậy, ta còn không tự bảo đảm được mình, huống chi người khác.','Tào Tháo',BL)]
JOKES+=[(R(187)+1.3,E(187)-0.1,'coin','Lời hứa đắt hơn vàng'),(R(195)+0.8,E(195)-0.1,'scroll','Một lá thư, vài tháng cho cả bản đồ'),
 (R(200)+2.4,E(200)-0.1,'fire','Một kho lương, cả đạo quân'),(R(204)+1.4,E(204)-0.1,'fire','Đốt thư: giữ người rẻ nhất'),
 (R(206)+1.2,E(206)-0.1,'fire','Thua thường chỉ vì một nhà kho cháy')]
def cv(a,b,t0,t1): return [(0,a),(t0,a),(t1,b)]
METERS+=[(R(178)+1.2,E(178)+0.2,'BINH LỰC (hình dung)',[('Viên Thiệu',PU,cv(0.95,0.95,0,1)),('Tào Tháo',BL,cv(0.4,0.4,0,1))]),
 (R(193)+0.3,R(201),'LƯƠNG THỰC',[('Quân Tào',BL,[(0,0.65),(R(193),0.65),(R(193)+6,0.18),(R(198)+9,0.18)]),('Quân Viên',PU,[(0,0.9),(R(198)+4.5,0.9),(R(198)+6.5,0.05)])]),]
# ======================= CHƯƠNG 11: BẮC YÊN, NAM ĐỘNG (207–238)
S(207,208,114.8,37.0,2.6);S(209,209,114.4,36.3,3.0);S(210,211,114.35,36.2,4.0);S(212,212,116.0,37.8,2.0);S(213,214,117.0,39.6,1.5);S(215,216,119.6,40.4,1.8)
S(217,217,115.0,37.5,1.2);S(218,220,112.4,33.2,2.6);S(221,222,112.1,32.1,4.0);S(223,226,112.0,32.0,3.2);S(227,227,114.0,34.3,1.8)
S(228,229,112.9,33.2,2.0);S(230,232,112.0,31.6,2.4);S(233,235,111.9,30.9,4.2);S(236,238,113.0,30.8,2.0)
for nm in ('Nghiệp','Nam Bì','Bình Nguyên','Bạch Lang Sơn','Kế','Hứa','Nam Dương','Tân Dã','Tương Dương','Giang Lăng','Trường Bản','Hạ Khẩu','Lạc Dương'): show(nm,207,238)
OW('Nghiệp',PU,(210,6,BL));OW('Nam Bì',PU,(212,0,BL));OW('Hứa',BL);OW('Tương Dương',TL,(229,2,BL));OW('Giang Lăng',TL,(229,3,BL));OW('Tân Dã',TL,(229,2,BL));OW('Hạ Khẩu',TL);OW('Nam Dương',BL)
RIVERS.append(('HOÀNG HÀ',[(110.6,34.78),(111.5,34.86),(112.6,34.98),(113.5,35.03),(114.1,35.2),(114.5,35.67),(115.1,36.05),(115.9,36.5),(116.7,37.2),(117.6,37.7),(118.6,37.95),(119.6,38.2)],7,None))
RIVERS.append(('SÔNG CHƯƠNG',[(113.4,36.1),(114.0,36.25),(114.6,36.4),(115.4,36.5),(116.0,36.6)],4,None))
reg('PHÍA BẮC SÔNG HOÀNG HÀ',(115.4,37.8),[(110.2,36.0),(110.2,41.4),(121.0,41.4),(121.0,36.5),(118.4,36.0),(116.2,36.3),(114.6,35.78),(113.6,36.0)],PU,[(R(217,0),BL)],alpha=34)
reg('KINH CHÂU',(111.4,31.4),[(110.2,30.0),(110.2,33.0),(113.0,33.4),(114.8,32.2),(114.8,30.2),(113.0,29.6)],TL,[(R(229,2),BL)],alpha=30)
C3(207,0.5,3.2,'Viên Thiệu','mất năm 202, không chọn người kế vị',PU);SKULL(207,2.0,5.0,114.35,36.35,'Viên Thiệu mất · 202')
C3(208,0.5,2.6,'Viên Đàm','con cả',PU);C3(208,3.4,2.8,'Viên Thượng','con nhỏ, được mẹ cưng',(180,80,150))
G('Viên Đàm',PU,10,[(0,116.4,37.2)],show=(R(208),R(212,4)),emb='tri',seed=201,defeats=[(R(212,3),'skull',INF)],alive=[(0,1),(R(212,3),1),(R(212,4),0.3)])
G('Viên Thượng',(180,80,150),10,[(0,114.35,36.4)],show=(R(208),R(212,6)),emb='dia',seed=202)
BATT.append((R(208,4),R(209,0),115.4,36.8,['Viên Đàm','Viên Thượng']))
J(209,'flag','Nhà đang cãi nhau, địch ở cổng',2.0)
NU(210,'NĂM 204','Tào Tháo vây Nghiệp',0.8)
G('Tào Tháo',BL,16,[(R(209,0),114.0,35.5),(R(210,0),114.1,36.15)],show=(R(209,0),R(214,0)),emb='dia',seed=203,soff=(-130,60))
NT(210,3.0,4.5,114.4,36.1,'đào hào, dẫn nước sông Chương',BL)
OBJ.append((R(210,3.5),R(211,0),'flood',(114.35,36.35),(114.35,36.35)))
SKULL(211,3.0,5.0,114.3,36.5,'Thẩm Phối không hàng, bị xử tử')
NT(211,0.6,3.0,114.5,36.5,'Tào Tháo khóc ở mộ Viên Thiệu',BL)
NU(212,'NĂM 205','Viên Đàm chết ở Nam Bì',2.0)
G('Tào Tháo',BL,14,[(R(213,0),114.1,36.4),(R(213,5),116.2,39.3),(R(214,5),117.5,40.6),(R(214,9),119.7,41.0)],show=(R(213,0),R(216,3)),emb='dia',seed=204,soff=(-130,60))
NU(213,'NĂM 207','Tào Tháo đánh lên vùng biên cương phía bắc',3.0)
NT(214,0.6,5.0,117.4,40.3,'lầy lội · hết lương · giết ngựa lấy thức ăn',(120,100,40))
NT(214,6.0,3.0,119.7,41.5,'Bạch Lang Sơn: quân Tào thắng',BL)
G('Người Ô Hoàn',GY,12,[(0,119.8,41.1)],show=(R(213,6),R(215,2)),emb='dia',seed=205,defeats=[(R(214,8),'lose',INF)])
BATT.append((R(214,7),R(214,10),119.8,41.15,['Tào Tháo','Người Ô Hoàn']))
G('Viên Thượng · Viên Hy',PU,5,[(R(215,0),119.0,40.7),(R(215,5),121.4,41.0)],show=(R(215,0),R(216,0)),emb='dia',seed=206,kind='cav')
SKULL(215,6.0,5.0,121.4,41.0,'Công Tôn Khang nộp đầu hai anh em')
C3(216,0.5,3.0,'Quách Gia','mất năm 207, mới 38 tuổi',BL);SKULL(216,2.5,5.0,119.0,40.5,'Quách Gia mất')
NU(217,'CẢ PHÍA BẮC','một người từng suýt mất tất cả, giờ mạnh nhất nhà Hán',1.5)
J(217,'flag','Mười bảy năm sau Huỳnh Dương',5.0)
G('Lưu Bị',GR,10,[(R(218,0),115.0,34.5),(R(218,6),112.3,32.5)],show=(R(218,0),R(229,0)),emb='sun',seed=211,soff=(-110,50))
C3(218,0.5,3.3,'Lưu Bị','mất đất, nương nhờ Lưu Biểu',GR);NT(218,4.0,4,112.0,32.1,'Kinh Châu',TL)
G('Lưu Biểu',TL,6,[(0,112.15,32.05)],show=(R(218,4),R(229,6)),emb='circle',seed=212,soff=(100,10))
NT(219,1.0,5.5,112.35,32.85,'Tân Dã: hàng rào chống Tào',GR)
NU(220,'7 NĂM','Lưu Bị ở Tân Dã',1.0)
Q(220,'ngày tháng trôi','Ngày tháng trôi, già đến nơi mà công danh chưa có gì.','Lưu Bị',GR,5.5)
J(221,'coin','Anh hùng khóc vì bắp đùi mập ra',2.0)
C3(222,0.5,2.8,'Từ Thứ','bạn của Lưu Bị',TL);C3(222,3.4,3.2,'Gia Cát Lượng','Ngọa Long, chưa đầy 30 tuổi',TL)
G('Gia Cát Lượng',TL,2,[(0,111.9,32.0)],show=(R(222,2),R(226,8)),emb='circle',seed=213)
NT(223,0.6,3.0,111.9,32.35,'đến thăm ba lần',GR)
AR(223,3.0,3.5,(113.8,34.0),(112.3,32.6),BL,'Tào Tháo: không đánh trực diện')
AR(224,0.5,4.0,(112.3,32.5),(107.6,32.2),GR,'lấy Kinh Châu rồi Ích Châu')
Q(225,'cá gặp nước','Tôi gặp Khổng Minh như cá gặp nước.','Lưu Bị',GR,4.0)
J(226,'flag','Trong nhà, có khi một câu là đủ',2.0)
NU(227,'THỪA TƯỚNG','Tào Tháo cầm cả triều, không chỉ hoàng đế',1.0)
NT(228,0.5,5.0,112.15,32.45,'Lưu Biểu mất, Lưu Tông lên thay',TL);SKULL(228,0.5,4.0,112.15,32.05,'Lưu Biểu mất')
G('Tào Tháo',BL,40,[(R(228,0),113.8,34.1),(R(228,6),112.5,33.1),(R(229,4),112.2,32.2)],show=(R(228,0),R(232,0)),emb='dia',seed=221,soff=(-120,60))
NU(228,'THÁNG BẢY · 208','Tào Tháo đem quân xuống phía nam',3.5)
C3(229,0.5,2.8,'Khoái Việt','khuyên đầu hàng',TL);C3(229,3.4,2.8,'Phó Tốn','khuyên đầu hàng',TL)
NT(229,5.5,3.0,112.15,32.35,'đầu hàng mà không báo Lưu Bị',(120,30,26))
G('Dân Kinh Châu',BR,24,[(R(230,2),112.15,32.1),(R(232,8),111.8,30.8)],show=(R(230,2),R(235,8)),emb='circle',seed=222,spread=1.3)
G('Lưu Bị',GR,12,[(R(230,0),112.15,32.05),(R(232,8),111.8,30.8),(R(233,3),111.9,30.6),(R(236,5),113.3,30.55),(R(236,9),114.3,30.55)],show=(R(230,0),R(238,9)),emb='sun',seed=223,alive=[(0,1),(R(233,0),1),(R(233,6),0.3)])
NU(230,'VÀI VẠN → 10 VẠN','dân Kinh Châu theo Lưu Bị',2.0)
Q(231,'làm việc lớn','Làm việc lớn phải lấy người làm gốc.','Lưu Bị',GR,4.5)
G('Kỵ binh Tào Tháo',BL,10,[(R(232,0),112.2,32.3),(R(232,8),111.8,30.85)],show=(R(232,0),R(234,0)),emb='dia',seed=224,kind='cav')
NU(232,'300 DẶM','một ngày một đêm, kỵ binh nhẹ',1.0)
NT(232,1.0,5,111.8,31.2,'đuổi kịp ở Trường Bản',BL)
BATT.append((R(233,0),R(233,6),111.8,30.82,['Kỵ binh Tào Tháo','Lưu Bị']))
G('Trương Phi',GR,3,[(0,111.8,30.9)],show=(R(234,0),R(235,0)),emb='sun',seed=225,kind='cav')
C3(234,0.5,3.0,'Trương Phi','20 kỵ binh, chặn trên cây cầu',GR)
Q(234,'ta là Trương Dực Đức','Ta là Trương Dực Đức đây, ai dám đến liều chết với ta?','Trương Phi',GR,6.0)
C3(235,0.5,3.2,'Triệu Vân','quay lại tìm vợ con chủ',GR);NT(235,3.5,4,111.9,30.7,'cứu Lưu Thiền',GR)
NT(236,0.5,4,113.0,30.75,'đến Hán Tân, gặp thuyền Quan Vũ',GR);C3(236,4.6,3.0,'Lưu Kỳ','con trưởng của Lưu Biểu',TL)
G('Quan Vũ',GR,4,[(0,113.8,30.6)],show=(R(236,0),R(238,9)),emb='sun',seed=226)
J(237,'flag','Một cách thoát: tìm đồng minh',2.0)
NT(238,0.5,6,117.5,30.0,'đồng minh ở Giang Đông: đánh hay hàng?',OR)
# ======================= CHƯƠNG 12: XÍCH BÍCH (239–267)
S(239,239,116.2,29.9,3.0);S(240,240,113.6,30.7,2.4);S(241,242,115.5,29.9,2.8);S(243,243,116.2,30.3,2.0);S(244,246,116.0,29.7,4.2)
S(247,248,116.0,29.8,3.4);S(249,249,114.8,30.0,2.6);S(250,250,113.8,29.95,4.0);S(251,254,113.7,29.9,4.4);S(255,256,113.7,29.9,4.6)
S(257,258,112.5,30.8,2.2);S(259,260,113.4,30.5,2.0);S(261,265,114.0,32.0,1.3);S(266,267,114.0,33.5,1.15)
for nm in ('Sài Tang','Phan Dương','Hạ Khẩu','Xích Bích','Phàn Khẩu','Giang Lăng','Trường Bản','Kiến Nghiệp','Ngô','Tương Dương','Hứa'): show(nm,239,267)
OW('Sài Tang',OR);OW('Phan Dương',OR);OW('Kiến Nghiệp',OR);OW('Ngô',OR);OW('Hạ Khẩu',GR);OW('Giang Lăng',BL,(260,0,BL));OW('Xích Bích',NEU)
RIVERS.append(('TRƯỜNG GIANG',[(111.0,30.6),(112.2,30.3),(113.2,29.9),(114.3,30.5),(115.3,30.1),(116.2,29.8),(117.5,30.3),(118.8,31.9),(120.6,31.8)],10,(113.0,30.0)) ) if False else None
C3(239,0.5,3.4,'Tôn Quyền','26 tuổi, giữ Giang Đông',OR)
G('Tôn Quyền',OR,12,[(0,115.95,29.7)],show=(R(239),R(248,9)),emb='moon',seed=231)
C3(240,0.5,3.0,'Lỗ Túc','đi dò Kinh Châu',OR)
G('Lỗ Túc',OR,3,[(R(240,0),115.9,29.8),(R(240,6),111.9,30.9)],show=(R(240,0),R(241,0)),emb='moon',seed=232,kind='cav')
G('Gia Cát Lượng',TL,2,[(R(241,0),114.3,30.55),(R(241,6),115.9,29.7)],show=(R(241,0),R(246,0)),emb='circle',seed=233,kind='cav')
NT(241,5.0,4,115.95,30.05,'hoặc đánh, hoặc hàng, đừng lưng chừng',TL)
Q(242,'Điền Hoành','Điền Hoành chỉ là một tráng sĩ nước Tề mà còn giữ nghĩa không nhục.','Gia Cát Lượng',TL,6.5)
LT(243,0.8,4.5,'Phan Dương','Sài Tang','thư Tào Tháo') if False else None
LETTERS.append((R(243,0.8),R(243,5.5),(113.7,30.5),X('Sài Tang'),'thư Tào Tháo'))
NU(243,'80 VẠN','Tào Tháo xưng số thủy quân',2.5)
C3(244,0.5,3.0,'Trương Chiêu','khuyên đầu hàng',OR);J(244,'scroll','Thuận lý thì hàng',4.5)
Q(245,'chủ công mà hàng','Chủ công mà hàng, thì còn đâu chỗ ngồi?','Lỗ Túc',OR,5.0)
G('Chu Du',OR,8,[(R(246,0),116.6,29.3),(R(246,7),115.95,29.7)],show=(R(246,0),R(249,0)),emb='moon',seed=234,kind='cav')
C3(246,0.5,3.0,'Chu Du','tướng giỏi, bình tĩnh',OR)
METERS.append((R(247,1.5),R(247,9),'SỐ QUÂN TÀO THÁO',[('Tào Tháo xưng',BL,[(0,1.0),(R(247),1.0)]),('Chu Du tính',OR,[(0,0.2),(R(247),0.2)])]))
NT(247,1.0,6,116.0,30.15,'chỉ khoảng 15–16 vạn · quân Kinh Châu chưa phục',OR)
NT(248,0.5,4,115.95,30.05,'chém một góc bàn',OR);NU(248,'3 VẠN QUÂN','Tôn Quyền giao cho Chu Du',4.0)
G('Thủy quân Chu Du',OR,12,[(R(249,0),115.95,29.7),(R(249,7),114.3,30.35)],show=(R(249,0),R(250,0)),emb='moon',seed=235)
G('Lưu Bị',GR,8,[(R(249,0),114.3,30.55),(R(249,7),114.3,30.4)],show=(R(249,0),R(250,6)),emb='sun',seed=236,soff=(-100,40))
NT(249,4.5,4,114.25,30.2,'hợp lực ở Phàn Khẩu',GR)
G('Quân Tào Tháo',BL,40,[(R(250,0),112.3,30.7),(R(250,4),113.5,30.15),(R(250,9),113.8,29.95)],show=(R(250,0),R(259,0)),emb='dia',seed=237,alive=[(0,1),(R(250,2),0.9),(R(250,6),0.75),(R(256,0),0.75),(R(257,0),0.4),(R(258,5),0.3)])
NT(250,0.8,4,113.5,30.35,'dịch bệnh trong quân Tào',(120,30,26));NT(250,5.0,4,113.7,29.5,'Xích Bích: quân Tào thua, rút về Ô Lâm',BL)
OBJ.append((R(251,0.5),R(256,2),'fleet',(113.55,30.0),(113.85,29.95,7)))
NT(251,3.0,5,113.7,30.25,'thuyền nối đuôi nhau',BL)
C3(252,0.5,3.0,'Hoàng Cái','tướng của Chu Du',OR);Q(252,'thuyền Tào nối đuôi','Thuyền Tào nối đuôi nhau, có thể dùng lửa đánh đuổi.','Hoàng Cái',OR,5.5)
NT(253,0.5,5,113.9,29.65,'thuyền nhỏ chất củi, tẩm dầu',OR);LETTERS.append((R(253,3.0),R(253,7.5),(113.9,29.7),(113.6,30.0),'thư xin hàng giả'))
nt(254,0,17);NT(254,1.0,5,114.0,29.5,'gió đông nam thổi gấp',OR)
OBJ.append((R(254,2.0),R(255,2.0),'fireboat',(114.05,29.7),(113.78,29.93,5)))
FIRES.extend([(R(255,2.5),R(257,1),113.5,30.0),(R(255,2.8),R(257,1),113.62,29.98),(R(255,3.2),R(257,1),113.75,29.96),(R(255,3.6),R(257,0),113.88,29.94),(R(256,1.0),R(257,0),113.55,30.15),(R(256,1.5),R(257,0),113.45,30.2)])
NU(255,'GIÓ ĐÔNG NAM','cả hàng thuyền Tào cháy cùng lúc',1.5)
NT(256,0.5,5,113.5,30.4,'người chết cháy, chết đuối, giẫm đạp',(120,30,26))
G('Chu Du · Lưu Bị',OR,12,[(R(256,2),114.0,29.8),(R(256,8),113.4,30.1)],show=(R(256,2),R(258,0)),emb='moon',seed=238,soff=(100,60))
G('Quân Tào Tháo',BL,18,[(R(257,0),113.5,30.1),(R(257,6),112.6,30.9),(R(258,3),112.0,31.8)],show=(R(257,0),R(260,0)),emb='dia',seed=239,alive=[(0,0.8),(R(257,6),0.4)])
NT(257,3.5,5,113.0,30.55,'đường bùn, lót cỏ cho ngựa',(120,100,40))
C3(258,0.5,3.0,'Tào Nhân','giữ Giang Lăng',BL);C3(258,3.4,3.0,'Từ Hoảng','giữ Giang Lăng',BL)
G('Tào Nhân · Từ Hoảng',BL,10,[(0,112.2,30.4)],show=(R(258,0),R(262,5)),emb='dia',seed=240,soff=(-100,50))
J(259,'scroll','Một cách thua rất nhã nhặn',2.5);LETTERS.append((R(259,0.5),R(259,4.5),(112.5,31.5),(115.95,29.7),'thư Tào Tháo gửi Tôn Quyền'))
NU(260,'HƠN 1 NĂM','Chu Du đánh Giang Lăng',0.8)
NT(260,4.0,5,113.0,28.9,'Lưu Bị chiếm bốn quận phía nam Kinh Châu',GR)
reg('PHÍA NAM KINH CHÂU',(112.7,29.2),[(110.6,28.7),(110.6,30.0),(113.6,30.0),(115.2,29.6),(115.2,28.7)],NEU,[(R(260,3),GR)],alpha=40)
reg('GIANG ĐÔNG',(118.0,30.6),[(115.4,29.7),(115.4,31.4),(117.6,32.9),(120.8,32.6),(121.6,30.0),(120.0,28.8),(115.8,28.8)],OR,alpha=30)
reg('PHÍA BẮC',(114.0,35.4),[(110.2,32.8),(110.2,36.0),(113.6,36.0),(116.2,36.3),(119.0,35.2),(119.0,32.8),(114.5,32.9)],BL,alpha=26)
NU(261,'BA PHẦN','Tào Tháo · Tôn Quyền · Lưu Bị',1.0)
J(262,'flag','Mang quân trên thuyền đi đánh người sống trên sông',2.0)
J(264,'fire','Một mảnh đất lửa cháy mới tắt, nhưng cũng đủ',2.0)
J(265,'scroll','Ba người, ba mảnh đất, một câu hỏi',1.5)
TITLES.append((R(266,2.5),E(267,0.5),'HẾT PHẦN 1','NĂM 208','Vì sao không ai gom nổi thiên hạ?'))
# ======================= HOÀN TẤT
REG_WIN={'ĐẠI HÁN':(1,17),'VIÊN THIỆU':(72,102),'VIÊN THUẬT':(72,102),'CÔNG TÔN TOẢN':(72,102),'TÀO THÁO':(73,102),'TỪ CHÂU':(103,176),
 'KÝ CHÂU':(177,206),'TINH CHÂU':(177,206),'THANH CHÂU':(177,206),'ĐẤT TÀO THÁO':(177,206),'PHÍA BẮC SÔNG HOÀNG HÀ':(207,238),'KINH CHÂU':(207,238),
 'PHÍA NAM KINH CHÂU':(260,267),'GIANG ĐÔNG':(261,267),'PHÍA BẮC':(261,267)}
for rg in REGIONS:
    w=REG_WIN.get(rg['name'])
    if w: rg['win']=(R(w[0],-1),E(w[1],1))
SCN.sort(key=lambda x:x[0])
CAM=[(0,SCN[0][2],SCN[0][3],SCN[0][4])]
for (a_,b_,lo,la,z) in SCN:
    CAM.append((R(a_)+1.6,lo,la,z));CAM.append((E(b_)-0.2,lo+0.02,la,z*1.03))
CAM=sorted(CAM,key=lambda k:k[0])
NIGHT.append((TOTAL,0));NIGHT=sorted(NIGHT,key=lambda k:k[0])
MINI=[(0,TOTAL)]
def year_of(n):
    m=n-1000
    for a,b,y in [(1,17,None),(18,35,184),(36,50,189),(51,74,190),(75,86,192),(87,102,191),(103,112,193),(113,125,196),(126,130,195),(131,142,196),
                  (143,152,197),(153,172,198),(173,173,199),(174,176,200),(177,180,199),(181,206,200),(207,209,202),(210,211,204),(212,212,205),(213,227,207),(228,267,208)]:
        if a<=m<=b: return y
    return None
