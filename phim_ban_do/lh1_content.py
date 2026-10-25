"""Lê Hoàn không lạy sứ Tống (đánh quân Tống năm 981). Số đoạn 1–87 (n = 11001–11087). Bản đồ world7 (Bắc Bộ, Lạng Sơn, Ung Châu, Quảng Châu).
Vị trí các nơi lấy theo chú thích "nay là" của bản dịch Đại Việt sử ký toàn thư hoặc theo vị trí hiện nay của địa danh (mức B), chỉ gần đúng:
Hoa Lư (Ninh Bình), Ái Châu (Thanh Hóa), Cát Lợi (Bắc Giang), Lạng Sơn, Chi Lăng (sông ở Chi Lăng, Lạng Sơn), Bạch Đằng, Sách Giang (Nam Sách), Núi Đọi (Duy Tiên),
Cử Long (Cẩm Thủy), Ung Châu (Nam Ninh), Quảng Châu (Phiên Ngung), Liêm Châu, Như Hồng (Khâm Châu). Tây Kết chưa xác định được vị trí: chấm chỉ là ước chừng ở phía bắc Lạng Sơn.
Chiêm Thành nằm ngoài khung bản đồ: chấm "phía nam" ở mép dưới. Triều đình nhà Tống (Biện Kinh) cũng ngoài khung: chấm "phía bắc" ở mép trên.
Vùng tô màu và các mũi tên là minh họa, không phải biên giới hay đường hành quân có chép. Trận Lạng Sơn chỉ minh họa kết quả (sử không kể từng bước).
Bố cục theo CLAUDE.md: không khung trích lời, khung đùa chỉ nhắm vào phía nhà Tống (tối đa hai khung mỗi chương), Q() ẩn ghi chú khi giao tranh.
Không có khung đùa nào về Lê Hoàn, Đinh Tiên Hoàng, Đinh Toàn hay các sử gia."""
from build2 import T,D,TOTAL,chap,PH
import build2 as _B
import world7 as _W
INF=1e9
BASE=11000
def _f(n): return BASE+n
def _l(n): return BASE+n
def _nx(n):
    while BASE+n not in T and n<200: n+=1   # đoạn đã bỏ khi sửa bố cục: lấy đoạn kế sau
    return n
def _pv(n):
    while BASE+n not in T and n>0: n-=1     # đoạn đã bỏ: lấy đoạn kế trước
    return n
def R(n,o=0): n=_nx(n); return T[BASE+n]+o
def E(n,o=0): n=_pv(n); return T[BASE+n]+D[BASE+n]+o
def at(n,sub,off=0.0):
    n=_nx(n)
    """Thời điểm chữ `sub` được đọc trong đoạn n (theo nhận dạng giọng); chưa có nhận dạng thì ước theo vị trí chữ."""
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
VT=GR      # Đại Cồ Việt xanh lá
TG=RD      # nhà Tống đỏ
BD=BL      # quân Nguyễn Bặc, Đinh Điền, Phạm Hạp xanh dương
CH=PU      # Chiêm Thành tím
LOC={'Hoa Lư':(105.90,20.28,'big'),'Ái Châu':(105.78,19.80,'mid'),'Cát Lợi':(106.20,21.20,'town'),'Cửa Đại Ác':(105.95,19.93,'town'),
     'Lạng Sơn':(106.76,21.85,'mid'),'Chi Lăng':(106.50,21.68,'town'),'Tây Kết':(106.05,22.15,'town'),'Bạch Đằng':(106.80,20.95,'town'),
     'Ung Châu':(108.35,22.82,'big'),'Quảng Châu':(113.26,23.13,'big'),'Triều Tống':(110.80,24.60,'mid'),'Liêm Châu':(109.15,21.65,'town'),
     'Sách Giang':(106.35,21.00,'town'),'Núi Đọi':(105.95,20.63,'town'),'Cử Long':(105.47,20.22,'town'),'Như Hồng':(108.55,21.75,'town'),
     'Chiêm Thành':(106.45,18.55,'mid')}
CITIES=dict(LOC)
CITY_SHOW={}
CITY_OWN={}
def show(name,a,b): CITY_SHOW.setdefault(name,[]).append((R(a,-1),E(b,1)))
def show_t(name,t0,t1): CITY_SHOW.setdefault(name,[]).append((t0,t1))
def own(name,col0,*steps):
    seq=[(0,col0)]
    for (t,c) in steps: seq.append((t,seq[-1][1]));seq.append((t+2.0,c))
    CITY_OWN[name]=seq
GROUPS=[];BATT=[];FIRES=[];FX=[];OBJ=[];LETTERS=[];ARROWS=[];NOTES=[];MARKS=[];FACES=[];CARDS3=[];QUOTES=[];JOKES=[];METERS=[];NUMS=[];TITLES=[]
REGIONS=[];RIVERS=[];ROUTES=[];TIDE=[];AMBIENT=[];PROPS=[]
WATER=[('VỊNH BẮC BỘ',(107.3,19.9),26)]
NIGHT=[(0,0)]
def night(t0,t1): NIGHT.extend([(t0,0),(t0+1.6,0.55),(t1,0.55),(t1+1.6,0)])
def G(name,col,n,keys,show=None,**kw):
    GROUPS.append(dict(name=name,col=col,n=n,keys=keys,show=show or (keys[0][0]-0.3,keys[-1][0]+3),**kw))
QUIET=[]
def Q(a,b): QUIET.append((R(a,0),E(b,0)))
def NT(n,o,dur,lo,la,txt,col=DK): NOTES.append((R(n,o),min(R(n,o+min(dur,3.5)),E(n,-0.1)),lo,la,txt,col))
FACEMAP={'Lê Hoàn':('Hoa Lư','general'),'Đinh Toàn':('Hoa Lư','child'),'Dương Thái hậu':('Hoa Lư','noble'),'Phạm Cự Lạng':('Hoa Lư','general'),
 'Nguyễn Bặc':('Ái Châu','general'),'Đinh Điền':('Ái Châu','general'),'Phạm Hạp':('Ái Châu','general'),'Ngô Nhật Khánh':('Cửa Đại Ác','lord'),
 'Hầu Nhân Bảo':('Ung Châu','general'),'Lư Đa Tốn':('Triều Tống','noble'),'Vua Tống':('Triều Tống','king'),'Trần Khâm Tộ':('Tây Kết','general'),
 'Lưu Trừng':('Bạch Đằng','general'),'Lý Giác':('Sách Giang','noble'),'Pháp Thuận':('Sách Giang','servant'),'Tống Cảo':('Liêm Châu','noble'),'Lý Nhược Chuyết':('Triều Tống','noble')}
def C3(n,o,dur,name,role,col):
    CARDS3.append((R(n,o),min(R(n,o+dur),E(n,-0.2)),name,role,col))
    if name in FACEMAP:
        loc,kind=FACEMAP[name]
        FACE(n,o,dur,name,loc,kind,col)
def J(n,icon,text,off=1.2,dur=3.0): JOKES.append((R(n,off),min(E(n,-0.1),R(n,off)+dur),icon,text))
def NU(n,big,small,delay=1.2): NUMS.append((_f(n),big,small,delay))
def AR(n,o,dur,a,b,col,txt): ARROWS.append((R(n,o),min(R(n,o+dur),E(n,-0.1)),a,b,col,txt))
def LET(n,o,dur,a,b,txt): LETTERS.append((R(n,o),R(n,o+dur),a,b,txt))
def SKULL(n,o,dur,lo,la,txt): MARKS.append((R(n,o),R(n,o+dur),lo,la,'skull',txt))
def X(name): return LOC[name][:2]
def FACE(n,o,dur,name,loc,kind,col,dx=0,dy=0,t_min=None):
    s=R(n,o)
    if t_min is not None: s=max(s,t_min)
    FACES.append((s,min(max(R(n,o+dur),s+2.2),E(n,-0.1)))+X(loc)+(name,kind,col,dx,dy))
SCN=[]
def S(a,b,lo,la,z): SCN.append((a,b,lo,la,z))
def S2(a,b,pts,zmax=8.0,zmin=0.9,hmax=440):
    """Camera tự tính: các điểm cần thấy nằm trong vùng an toàn, chừa chỗ cho nhãn, phụ đề và bản đồ nhỏ."""
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
H=X('Hoa Lư');AC=X('Ái Châu');CLG=X('Chi Lăng');LS=X('Lạng Sơn');TK=X('Tây Kết');BDG=X('Bạch Đằng');UC=X('Ung Châu');QC=X('Quảng Châu');TT=X('Triều Tống')
SOUTH=X('Chiêm Thành')
P_DCV=[(105.05,22.40),(106.40,22.55),(107.70,21.60),(107.10,20.30),(106.20,19.75),(105.40,19.15),(104.70,19.85),(104.55,21.40)]
P_TONG=[(105.9,23.2),(106.7,22.85),(107.6,22.45),(108.0,22.05),(108.6,21.60),(109.3,21.30),(111.0,21.25),(113.5,21.90),(114.8,22.50),(114.8,24.7),(105.9,24.7)]
# ======================= CHƯƠNG 1: MỞ ĐẦU (1–4): cảnh không lạy sứ Tống năm 990
TITLES.append((0.3,4.0,'LÊ HOÀN','KHÔNG LẠY SỨ TỐNG','Đại Cồ Việt, năm 990'))
show('Hoa Lư',1,87);show('Ung Châu',3,47);show('Quảng Châu',3,4);show('Triều Tống',3,4)
own('Hoa Lư',VT);own('Ung Châu',TG);own('Quảng Châu',TG);own('Triều Tống',TG)
S2(1,2,[H,(105.97,20.36)],6.0)
G('Sứ nhà Tống',TG,4,[(R(1,0),106.07,20.44),(R(2,1.0),105.97,20.36),(E(2,0),105.97,20.36)],kind='cav',show=(R(1,0),E(2,0)),emb='tri',seed=1101,spread=0.35,soff=(70,-10),label=False)
FACE(1,0.4,3.2,'Lê Hoàn','Hoa Lư','king',VT)
NT(2,0.3,3.0,105.90,20.28,'bưng thư vua Tống mà không lạy',DK)
NU(3,'năm 980','Quan nhà Tống tính đánh Đại Cồ Việt',3.5)
S2(3,4,[H,UC,TT],1.9,hmax=380)
reg('NHÀ TỐNG',(110.6,23.2),P_TONG,TG,(3,4),alpha=12)
reg('ĐẠI CỒ VIỆT',(105.55,21.55),P_DCV,VT,(3,4),alpha=16)
# ======================= CHƯƠNG 2: ĐỨA BÉ SÁU TUỔI VÀ NGƯỜI GIỮ QUYỀN (5–15)
S2(5,15,[H,AC],4.2,hmax=340)
reg('ĐẠI CỒ VIỆT',(105.55,21.55),P_DCV,VT,(5,15),alpha=14)
NU(5,'năm 979','Đinh Tiên Hoàng bị giết',0.8)
C3(5,3.4,3.0,'Đinh Toàn','sáu tuổi nối ngôi',VT)
C3(6,0.4,3.0,'Lê Hoàn','giữ quyền thay vua nhỏ',VT)
NT(9,0.3,3.2,105.90,20.28,'Phó Vương: người phụ chính bên cạnh vua nhỏ',VT)
C3(10,0.2,2.8,'Nguyễn Bặc','ngờ Lê Hoàn',BD)
C3(10,3.2,2.8,'Đinh Điền','ngờ Lê Hoàn',BD)
G('Quân Nguyễn Bặc',BD,8,[(R(11,0),105.78,19.82),(R(11,5),105.84,20.08),(R(12,0),105.86,20.20),(E(12,0),105.86,20.20)],show=(R(11,0),E(12,0)),emb='circle',seed=1102,spread=0.7,soff=(-50,10),defeats=[(at(12,'phóng lửa'),'flag',E(13,0))])
G('Thuyền Đinh Điền',BD,6,[(R(11,0),105.97,19.95),(R(11,5),105.98,20.14),(R(12,0),105.97,20.22),(E(12,0),105.97,20.22)],kind='ship',show=(R(11,0),E(12,0)),emb='circle',seed=1103,spread=0.6,soff=(50,0),label=False,defeats=[(at(12,'phóng lửa'),'flag',E(13,0))])
G('Quân Lê Hoàn',VT,10,[(R(11,0),105.90,20.28),(E(13,0),105.90,20.28)],show=(R(11,0),E(13,0)),emb='sun',seed=1104,spread=0.8,soff=(0,-35))
BATT.append((R(12,0.0),R(12,5.0),105.92,20.22,['Thuyền Đinh Điền','Quân Lê Hoàn']))
FIRES.append((at(12,'phóng lửa'),at(12,'phóng lửa',4.0),105.98,20.22))
G('Quân Phạm Hạp',BD,5,[(R(13,0),105.88,20.24),(R(13,5.0),106.20,21.20),(E(13,0),106.20,21.20)],show=(R(13,0),E(13,0)),emb='circle',seed=1105,spread=0.5,soff=(-30,0),defeats=[(at(13,'bắt sống'),'flag',E(13,0))],label=False)
show('Cát Lợi',13,13)
FACE(13,0.3,2.6,'Phạm Hạp','Cát Lợi','general',BD)
Q(11,13)
G('Thuyền Chiêm Thành',CH,14,[(R(14,0),106.45,18.90),(E(14,0),106.20,19.50),(R(15,0),105.95,19.93),(E(15,0),105.95,19.93)],kind='ship',show=(R(14,0),E(15,0)),emb='tri',seed=1106,spread=1.0,soff=(60,15),
  alive=[(0,1),(at(15,'bão'),1),(at(15,'bão')+3.0,0.08)],defeats=[(at(15,'lật đắm'),'flag',E(15,0))])
FACE(14,0.3,3.0,'Ngô Nhật Khánh','Cửa Đại Ác','lord',CH)
show('Cửa Đại Ác',14,15)
night(R(15,0.0),E(15,0.0))
Q(15,15)
# ======================= CHƯƠNG 3: NHÀ TỐNG NHÌN SANG (16–22)
S2(16,22,[H,UC,TT,QC],1.7,hmax=360)
reg('NHÀ TỐNG',(110.6,23.2),P_TONG,TG,(16,47),alpha=13)
reg('ĐẠI CỒ VIỆT',(105.55,21.55),P_DCV,VT,(16,35),alpha=14)
show('Quảng Châu',16,47);show('Triều Tống',16,47)
NU(17,'năm 980','Hầu Nhân Bảo xin đánh úp Đại Cồ Việt',3.0)
C3(16,3.2,3.0,'Hầu Nhân Bảo','quan nhà Tống giữ Ung Châu',TG)
LET(17,at(17,'dâng thư')-R(17,0),4.0,UC,TT,'thư xin đánh úp')
C3(18,0.4,3.0,'Lư Đa Tốn','bàn kế đánh úp',TG)
NT(19,0.4,3.2,UC[0],UC[1]-0.35,'ba mươi nghìn quân Kinh Hồ',TG)
J(20,'scroll','"Không tốn một mũi tên." Kế hoạch nghe rất gọn',2.4)
G('Quân Tống ở Ung Châu',TG,12,[(at(21,'Ung Châu')-3.0,TT[0],TT[1]),(at(21,'Ung Châu')+1.5,UC[0],UC[1]),(E(22,0),UC[0],UC[1])],show=(at(21,'Ung Châu')-3.0,E(36,-1)),emb='tri',seed=1107,spread=0.8,soff=(-50,-20))
G('Quân Tống ở Quảng Châu',TG,10,[(at(21,'Quảng Châu')-3.0,TT[0],TT[1]),(at(21,'Quảng Châu')+1.5,QC[0],QC[1]),(E(22,0),QC[0],QC[1])],show=(at(21,'Quảng Châu')-3.0,E(36,-1)),emb='tri',seed=1108,spread=0.7,soff=(-40,-20))
AR(22,0.3,3.2,UC,LS,TG,'')
LET(22,0.2,3.4,LS,H,'tin cấp báo')
FX.append((at(21,'hẹn ngày'),at(21,'hẹn ngày',2.2),'horn',UC,UC))
# ======================= CHƯƠNG 4: TIẾNG HÔ VẠN TUẾ (23–28)
S2(23,28,[H],6.0)
PROPS.append((R(24,0.0),E(28,0),'hall',105.90,20.31,'',0.6))
C3(23,0.4,3.0,'Dương Thái hậu','mẹ vua Đinh Toàn',VT)
C3(23,3.4,2.8,'Phạm Cự Lạng','đại tướng quân',VT)
G('Các tướng của Phạm Cự Lạng',VT,9,[(R(24,0),105.72,20.20),(R(24,4.0),105.86,20.27),(E(26,0),105.86,20.27)],show=(R(24,0),E(26,0)),emb='sun',seed=1109,spread=0.55,soff=(-30,20),label=False)
FX.append((at(26,'vạn tuế'),at(26,'vạn tuế',1.8),'trumpet',H,H))
NU(27,'năm 980','Lê Hoàn lên ngôi hoàng đế',0.4)
FACE(27,3.4,3.4,'Lê Hoàn','Hoa Lư','king',GD,dy=-125)
FX.append((at(27,'lên ngôi'),at(27,'lên ngôi',1.6),'gong',H,H))
# ======================= CHƯƠNG 5: HAI BỨC THƯ (29–35)
S2(29,35,[H,UC,TT],2.0,hmax=380)
LET(29,0.6,4.2,TT,H,'thư của vua Tống')
J(30,'scroll','Cả nước ta chỉ là ngón chân của họ',2.6)
LET(31,at(31,'thư giả')-R(31,0)-0.4,4.0,H,TT,'thư giả mượn tên Đinh Toàn')
NT(32,0.6,3.0,TT[0],TT[1]-0.4,'xin hoãn việc đem quân',DK)
LET(33,0.8,4.0,TT,H,'thư trả lời: hai đường')
NT(34,0.4,3.4,H[0]+0.5,H[1]+0.45,'làm phó, hoặc đưa mẹ con sang Tống',TG)
# ======================= CHƯƠNG 6: MÙA XUÂN Ở LẠNG SƠN (36–44)
S2(36,44,[LS,TK,BDG,(106.2,22.5)],3.4,hmax=360)
NU(36,'năm 981','Quân Tống áp sát bờ cõi',0.6)
for _nm in ('Lạng Sơn','Chi Lăng','Tây Kết','Bạch Đằng'): own(_nm,VT)
show('Lạng Sơn',36,47);show('Chi Lăng',36,47);show('Tây Kết',36,47);show('Bạch Đằng',36,47)
G('Đạo Hầu Nhân Bảo',TG,12,[(R(36,0),107.60,22.50),(at(36,'Lạng Sơn'),106.88,21.98),(R(39,0),106.80,21.88),(at(40,'mắc mưu'),106.58,21.74),(E(41,0),106.58,21.74)],show=(R(36,0),E(47,0)),emb='tri',seed=1110,spread=0.55,soff=(95,-55),
  alive=[(0,1),(at(40,'bị chém'),1),(at(40,'bị chém')+2.0,0.12)],defeats=[(at(40,'bị chém'),'flag',E(47,0))])
G('Đạo Trần Khâm Tộ',TG,12,[(R(36,3),107.00,22.70),(at(37,'Tây Kết'),106.10,22.18),(R(41,0),106.10,22.18),(at(41,'quay về'),106.90,22.80),(R(42,0),106.90,22.80),(at(42,'đuổi theo'),106.60,22.40),(E(42,0),106.60,22.40)],
  show=(R(36,3),E(47,0)),emb='tri',seed=1111,spread=0.6,soff=(-70,-45),alive=[(0,1),(at(42,'thua to'),1),(at(42,'thua to')+3.0,0.4)],defeats=[(at(42,'thua to'),'flag',E(47,0))])
G('Thuyền Lưu Trừng',TG,8,[(R(37,0),107.60,20.90),(at(37,'Bạch Đằng'),106.85,20.93),(E(41,0),106.85,20.93)],kind='ship',show=(R(37,0),E(47,0)),emb='tri',seed=1112,spread=0.4,soff=(80,25),label=False,
  alive=[(0,1),(at(41,'thua trận'),1),(at(41,'thua trận')+2.0,0.25)],defeats=[(at(41,'thua trận'),'flag',E(47,0))])
G('Quân Lê Hoàn ',VT,14,[(R(38,0),105.90,20.28),(R(38,5.0),106.46,21.62),(R(41,0),106.46,21.62),(at(42,'đuổi theo'),106.50,21.95),(R(43,0),106.60,22.35),(E(43,0),106.60,22.35),(E(43,0)+2.0,105.90,20.28)],
  show=(R(38,0),E(44,0)),emb='sun',seed=1113,spread=0.6,soff=(-95,45))
FACE(38,0.3,3.0,'Lê Hoàn','Hoa Lư','general',VT,dx=0,dy=0,t_min=R(38,0.3))
BATT.append((at(42,'đuổi theo'),at(42,'đuổi theo')+4.6,106.60,22.35,['Đạo Trần Khâm Tộ','Quân Lê Hoàn ']))
NT(38,2.0,3.0,CLG[0],CLG[1],'đóng cọc cản đường trên sông Chi Lăng',BR)
FX.append((at(40,'bị chém'),at(40,'bị chém',3.0),'drums',CLG,CLG))
FX.append((at(42,'đuổi theo'),at(42,'đuổi theo',4.4),'drums',(106.50,21.95),(106.60,22.35)))
C3(43,0.4,2.8,'Quách Quân Biện','tướng Tống bị bắt',TG)
C3(43,3.3,2.6,'Triệu Phụng Huân','tướng Tống bị bắt',TG)
NT(44,0.4,3.2,CLG[0],CLG[1]-0.5,'trận quyết định chỉ chép vài dòng',DK)
Q(38,43)
# ======================= CHƯƠNG 7: QUÂN TỐNG RÚT VỀ (45–50)
S2(45,50,[H,UC,TT,LS],1.9,hmax=380)
J(45,'scroll','Chưa tốn một mũi tên, đã tốn cả một đạo quân',2.8)
LET(45,0.5,3.6,UC,TT,'tin thua trận')
FX.append((at(45,'rút quân'),at(45,'rút quân',2.0),'horn',TT,TT))
G('Quân Tống rút về',TG,10,[(at(45,'rút quân'),106.60,22.35),(at(45,'rút quân')+5.5,UC[0],UC[1]),(E(47,0),UC[0],UC[1])],show=(at(45,'rút quân'),E(47,0)),emb='tri',seed=1114,spread=0.7,soff=(40,10),kind='cav',label=False)
NT(47,0.4,3.2,UC[0],UC[1]-0.45,'Vương Soạn bị giết ở Ung Châu',TG)
C3(48,0.4,3.0,'Lê Hoàn','được dâng tôn hiệu',VT)
C3(49,0.4,3.0,'Lê Văn Hưu','sử gia',GD)
# ======================= CHƯƠNG 8: ĐI ĐÁNH CHIÊM THÀNH (51–55)
S2(51,55,[H,SOUTH],1.9,hmax=380)
NU(52,'năm 982','Lê Hoàn đích thân đi đánh Chiêm Thành',3.4)
G('Quân Lê Hoàn đi nam',VT,12,[(at(52,'tự mình'),105.95,20.20),(at(52,'tự mình')+5.5,106.45,18.80),(R(54,0),106.45,18.80),(E(54,0),106.45,18.80)],kind='ship',show=(at(52,'tự mình'),E(54,0)),emb='sun',seed=1115,spread=0.9,soff=(-50,0))
G('Quân Chiêm Thành',CH,10,[(R(51,0),106.55,18.60),(E(54,0),106.55,18.60)],show=(R(51,0),E(54,0)),emb='tri',seed=1116,spread=0.7,soff=(55,5),defeats=[(at(53,'thua to'),'flag',E(54,0))])
NT(51,0.5,3.2,SOUTH[0],SOUTH[1]+0.40,'sứ giả Từ Mục, Ngô Tử Canh bị Chiêm Thành bắt giữ',CH)
BATT.append((at(53,'thua to')-1.2,at(53,'thua to')+3.8,106.50,18.68,['Quân Lê Hoàn đi nam','Quân Chiêm Thành']))
FX.append((at(53,'thua to')-1.0,at(53,'thua to')+3.6,'drums',(106.40,18.95),SOUTH))
Q(52,54)
NT(55,2.0,3.2,105.80,19.60,'kênh mới ở vùng núi Đồng Cổ, sông Bà Hòa',BR)
# ======================= CHƯƠNG 9: SỨ NHÀ TỐNG VÀ HAI CON NGỖNG (56–64)
S2(56,58,[H,TT,UC],1.9,hmax=380)
NU(56,'năm 983','Thông hiếu với nhà Tống',3.0)
LET(56,at(56,'thông hiếu')-R(56,0),3.6,H,TT,'sứ sang thông hiếu')
LET(57,0.2,4.0,TT,H,'chế thư phong Tiết độ sứ')
PROPS.append((R(57,0.5),R(57,4.5),'seal',TT[0]-0.1,TT[1]-0.35,'',0.7))
C3(58,0.3,3.0,'Lê Hoàn','nhận chế thư rất kính cẩn',VT)
S2(59,64,[(106.35,21.00),H,LS],3.2,hmax=360)
show('Sách Giang',59,64)
NU(59,'năm 987','Sứ Tống Lý Giác sang',0.6)
G('Sứ Lý Giác',TG,5,[(R(59,0),LS[0],LS[1]),(at(59,'Lê Hoàn sai')+1.0,106.40,21.04),(E(62,0),106.40,21.04),(R(63,2.0),106.60,21.50),(E(64,0),LS[0]-0.05,LS[1]-0.1)],kind='cav',show=(R(59,0),E(64,0)),emb='tri',seed=1117,spread=0.4,soff=(55,0),label=False)
C3(59,3.2,2.8,'Lý Giác','sứ nhà Tống',TG)
C3(59,6.1,2.2,'Pháp Thuận','sư, giả làm người coi sông',VT)
PROPS.append((R(60,0.3),E(62,0),'scrolls2',106.35,21.30,'',0.5))
NT(61,0.3,3.0,106.35,21.00,'đối thơ trên sông Sách',BR)
FACEMAP['Ngô Khuông Việt']=('Sách Giang','noble')
C3(63,0.3,2.8,'Ngô Khuông Việt','sư, làm bài từ tiễn',VT)
# ======================= CHƯƠNG 10: KHÔNG LẠY SỨ GIẢ (65–77)
S2(65,65,[(109.15,21.65),BDG,H],2.4,hmax=360)
NU(65,'năm 990','Sứ Tống Cảo sang',0.4)
show('Liêm Châu',65,66)
G('Sứ Tống Cảo',TG,5,[(R(65,0),109.15,21.65),(R(65,6.5),106.85,20.95),(R(66,0),106.85,20.95),(R(66,5.0),105.99,20.38),(E(67,0),105.97,20.36)],kind='cav',show=(R(65,0),E(67,0)),emb='tri',seed=1118,spread=0.4,soff=(60,5),label=False)
G('Thuyền đón sứ',VT,9,[(R(65,0.5),106.60,20.90),(R(65,6.5),106.85,20.95),(E(65,0),106.85,20.95)],kind='ship',show=(R(65,0.5),E(65,0)),emb='sun',seed=1119,spread=0.6,soff=(-30,-20),label=False)
C3(65,0.4,2.9,'Tống Cảo','sứ nhà Tống',TG)
S2(66,67,[H,(106.05,20.46)],5.0)
G('Thủy quân và khí giới',VT,10,[(R(66,2.0),105.80,20.18),(E(67,0),105.80,20.18)],show=(R(66,2.0),E(67,0)),emb='sun',seed=1120,spread=0.7,soff=(-60,15))
PROPS.append((R(67,0.0),E(67,0),'hall',105.90,20.31,'',0.6))
NT(67,0.4,3.2,105.90,20.28,'bưng thư vua Tống, không lạy',DK)
FACE(67,0.3,3.2,'Lê Hoàn','Hoa Lư','king',GD,dy=-190)
S2(68,70,[H,LS,TT],1.9,hmax=380)
NT(69,0.4,3.2,LS[0],LS[1],'thư từ trao nhận ở biên giới',DK)
PROPS.append((R(69,1.0),R(70,3.0),'meeting',LS[0]+0.05,LS[1]-0.05,'',0.5))
S2(71,75,[H,UC,QC,TT],1.7,hmax=360)
NU(71,'năm 995','Vụ Như Hồng',0.4)
show('Như Hồng',71,75)
NT(71,1.6,3.2,108.55,21.75,'trấn Như Hồng bị cướp phá, theo quan Tống tâu',TG)
show('Quảng Châu',73,75)
LET(72,0.5,4.0,TT,H,'chiếu thư và đai ngọc')
C3(72,0.4,3.0,'Lý Nhược Chuyết','sứ nhà Tống',TG)
PROPS.append((R(72,3.4),R(73,0),'seal',TT[0]-0.1,TT[1]-0.35,'',0.6))
NT(74,0.5,3.4,QC[0],QC[1]-0.45,'Phiên Ngung (Quảng Châu): chỉ là lời nói, không có cuộc tấn công',GY)
AR(74,0.5,3.0,H,QC,GY,'')
NU(75,'năm 997','Nhà Tống phong Nam Bình Vương',3.4)
S2(76,77,[H,TT,UC],1.9,hmax=380)
NT(77,0.4,3.4,UC[0],UC[1]-0.45,'chỉ quan giữ biên giới nhận mệnh',TG)
# ======================= CHƯƠNG 11: DỰNG NGHIỆP TRONG NƯỚC (78–83)
S2(78,79,[H,(105.95,20.63)],6.0)
PROPS.append((R(78,0.6),E(78,0),'hall',105.90,20.31,'',0.6))
NU(78,'năm 984','Đúc tiền Thiên Phúc',0.8)
show('Núi Đọi',79,79)
NU(79,'năm 987','Lần đầu cày ruộng tịch điền',0.6)
S2(80,82,[H,(105.47,20.22)],5.2,hmax=340)
NU(80,'năm 999','Đánh bốn mươi chín động',0.6)
show('Cử Long',81,82)
NU(81,'năm 1001','Đánh giặc ở Cử Long',0.6)
G('Quân Lê Hoàn đi Cử Long',VT,12,[(R(80,0),105.90,20.28),(R(80,4.0),105.65,20.24),(R(81,0),105.65,20.24),(R(81,3.5),105.50,20.22),(E(82,0),105.50,20.22)],kind='ship',show=(R(80,0),E(82,0)),emb='sun',seed=1121,spread=0.8,soff=(40,10))
G('Giặc Cử Long',NEU,10,[(R(81,0),105.40,20.30),(E(82,0),105.40,20.30)],show=(R(81,0),E(82,0)),emb='circle',seed=1122,spread=0.7,soff=(-45,-5),defeats=[(at(82,'giặc tan vỡ'),'flag',E(82,0))])
BATT.append((R(81,3.0),E(82,-0.4),105.44,20.26,['Quân Lê Hoàn đi Cử Long','Giặc Cử Long']))
FACEMAP['Đinh Toàn']=('Cử Long','prince')
C3(82,0.3,2.8,'Đinh Toàn','Vệ Vương, trúng tên',VT)
Q(81,82)
S2(83,83,[H],5.2)
NU(83,'năm 1002','Đổi mười đạo thành lộ, phủ, châu',0.6)
# ======================= CHƯƠNG 12: KẾT (84–87)
S2(84,84,[H],5.4)
NU(84,'năm 1005','Lê Hoàn mất ở điện Trường Xuân',0.6)
PROPS.append((R(84,3.0),E(84,0),'tomb',105.93,20.34,'',0.8))
FACE(84,0.3,3.0,'Lê Hoàn','Hoa Lư','king',GD)
S2(85,85,[H,LS,UC],2.4,hmax=380)
reg('ĐẠI CỒ VIỆT',(105.55,21.55),P_DCV,VT,(85,87),alpha=16)
S2(86,87,[H,LS,UC],2.4,hmax=380)
PROPS.append((R(86,0.4),R(86,3.4),'ping',LS[0],LS[1],'g',0.9))
PROPS.append((R(86,3.8),R(86,6.8),'ping',H[0],H[1],'g',0.9))
# ======================= HIỆU ỨNG THÊM
PROPS.append((R(11,0.5),E(13,0),'camp',105.82,20.14,'',0.45))
PROPS.append((R(38,0.5),E(43,0),'pennants',106.30,22.05,'',0.55))
PROPS.append((R(36,0.5),E(41,0),'camp',107.20,22.20,'r',0.40))
PROPS.append((R(36,0.3),R(36,3.3),'ping',LS[0],LS[1],'r',0.8))
PROPS.append((R(65,0.5),R(65,3.5),'ping',109.15,21.65,'r',0.6))
AMBIENT.extend([(R(1,0),E(4,0),'wind',0.3),(R(5,0),E(15,0),'wind',0.35),(R(14,0),E(15,0),'sea',0.5),(R(16,0),E(22,0),'crowd',0.25),
 (R(23,0),E(28,0),'crowd',0.3),(R(36,0),E(44,0),'forest',0.4),(R(51,0),E(55,0),'sea',0.35),(R(56,0),E(64,0),'crowd',0.2),(R(59,0),E(62,0),'sea',0.25),
 (R(65,0),E(77,0),'crowd',0.25),(R(78,0),E(83,0),'wind',0.3),(R(84,0),TOTAL-1,'wind',0.3)])
# ======================= HOÀN TẤT
SCN.sort(key=lambda x:x[0])
CAM=[(0,SCN[0][2],SCN[0][3],SCN[0][4])]
for (a_,b_,lo,la,z) in SCN:
    CAM.append((R(a_)+1.6,lo,la,z));CAM.append((E(b_)-0.2,lo+0.01,la,z*1.03))
CAM=sorted(CAM,key=lambda k:k[0])
NIGHT.append((TOTAL,0));NIGHT=sorted(NIGHT,key=lambda k:k[0])
MINI=[(0,TOTAL)]
QUIET_AUDIO=True
MUSIC=[(0,R(4,0),'cang',1.0),(R(4,0),R(5,0),'mo',1.0),(R(5,0),R(11,0),'bi',1.0),(R(11,0),R(16,0),'cang',1.0),(R(16,0),R(23,0),'cang',0.9),(R(23,0),R(29,0),'trang',1.0),
       (R(29,0),R(36,0),'cang',0.9),(R(36,0),R(45,0),'hanh',1.0),(R(45,0),R(51,0),'trang',1.0),(R(51,0),R(56,0),'hanh',1.0),(R(56,0),R(65,0),'binh',0.9),
       (R(65,0),R(71,0),'mo',0.9),(R(71,0),R(78,0),'binh',0.9),(R(78,0),R(84,0),'binh',1.0),(R(84,0),R(86,0),'bi',1.0),(R(86,0),TOTAL,'trang',1.0)]
def gate_open(t): return 0
def year_of(n):
    m=n-BASE
    for a,b,y in [(1,2,990),(3,3,980),(4,4,None),(5,15,979),(16,35,980),(36,50,981),(51,54,982),(55,55,983),(56,58,986),(59,64,987),(65,70,990),(71,71,995),(72,75,996),(76,77,997),
                  (78,78,984),(79,79,987),(80,80,999),(81,82,1001),(83,83,1002),(84,85,1005),(86,87,None)]:
        if a<=m<=b: return y
    return None
NO_GROUP_LABEL=True
SIDES=[('Đại Cồ Việt',VT,{g['name'].strip() for g in GROUPS if g['col']==VT}),('Nhà Tống',TG,{g['name'].strip() for g in GROUPS if g['col']==TG}),
       ('Quân Bặc, Điền, Hạp',BD,{g['name'].strip() for g in GROUPS if g['col']==BD}),('Chiêm Thành',CH,{g['name'].strip() for g in GROUPS if g['col']==CH}),
       ('Địa phương',NEU,{g['name'].strip() for g in GROUPS if g['col']==NEU})]
SFX=[(at(21,'hẹn ngày'),'horn'),(at(26,'vạn tuế'),'trumpet'),(at(27,'lên ngôi'),'gong'),(at(45,'rút quân'),'horn'),(R(65,0.2),'horn'),(R(67,1.0),'gong')]
SFX_GROUPS=['Sứ nhà Tống','Sứ Tống Cảo','Sứ Lý Giác','Quân Tống rút về']
