"""Lê Hoàn bốn lần đánh lừa nhà Tống (lh6, bản sáng tạo). Số đoạn 1–113 (n = 17001–17113), BASE=17000, dùng trực tiếp số đoạn lh6.
Vị trí địa danh giống lh2 (mức B, chỉ gần đúng). Hiệu ứng thêm: thẻ đếm bốn lần đánh lừa, vòng sáng, cờ, lửa, khung so sánh, dòng thời gian.
Bố cục theo CLAUDE.md: không khung trích lời, không khung đùa (chủ kênh bỏ hài 26/10), Q() ẩn ghi chú khi giao tranh."""
from build2 import T,D,TOTAL,chap,PH
import build2 as _B
import world7 as _W
INF=1e9
BASE=17000
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
     'Chiêm Thành':(105.15,19.00,'mid')}
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
TABLES=[]
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
# ======================= CHƯƠNG 1: MỞ ĐẦU (1–5): bốn lần đánh lừa, chưa nêu tên người
TITLES.append((0.3,4.2,'BỐN LẦN ĐÁNH LỪA','NHÀ TỐNG','Đại Cồ Việt, từ năm 980 đến năm 990'))
show('Hoa Lư',1,113);show('Ung Châu',1,63);show('Quảng Châu',1,5);show('Triều Tống',1,5)
own('Hoa Lư',VT);own('Ung Châu',TG);own('Quảng Châu',TG);own('Triều Tống',TG)
S2(1,5,[H,UC,TT],1.9,hmax=380)
reg('NHÀ TỐNG',(110.6,23.2),P_TONG,TG,(1,5),alpha=12)
reg('ĐẠI CỒ VIỆT',(105.55,21.55),P_DCV,VT,(1,5),alpha=18)
PROPS.append((R(1,0.2),R(1,3.4),'ping',H[0],H[1],'g',0.9))
NT(2,0.4,3.2,TT[0],TT[1]-0.45,'ngay đầu năm 980: "thắng dễ như bẻ cành khô"',TG)
AR(3,0.3,3.6,LS,UC,TG,'')
G('Quân Tống rút về (mở đầu)',TG,9,[(R(3,0),LS[0],LS[1]),(R(3,0)+3.6,UC[0],UC[1]),(E(3,0),UC[0],UC[1])],kind='cav',show=(R(3,0),E(3,0)),emb='tri',seed=1601,spread=0.6,soff=(40,10),label=False)
# bốn vòng sáng xuất hiện lần lượt ở câu hỏi: chưa nói là gì
for _i,(_lo,_la) in enumerate([(105.90,20.28),(106.50,21.68),(106.35,21.00),(105.94,20.35)]):
    PROPS.append((R(4,0.4+1.0*_i),R(4,0.4+1.0*_i)+2.4,'ping',_lo,_la,'g',0.8))
FX.append((R(4,0.4),R(4,2.0),'horn',H,H))
# ======================= CHƯƠNG 2: ĐỨA BÉ SÁU TUỔI VÀ NGƯỜI GIỮ QUYỀN (6–21)
S2(6,21,[H,AC],4.2,hmax=340)
reg('ĐẠI CỒ VIỆT',(105.55,21.55),P_DCV,VT,(6,21),alpha=14)
NU(6,'năm 979','Đinh Tiên Hoàng bị giết',0.8)
C3(6,3.4,3.0,'Đinh Toàn','sáu tuổi nối ngôi',VT)
C3(8,0.4,3.0,'Lê Hoàn','giữ quyền thay vua nhỏ',VT)
NT(12,0.3,3.2,105.90,20.28,'Phó Vương: người phụ chính bên cạnh vua nhỏ',VT)
C3(13,0.2,2.8,'Nguyễn Bặc','ngờ Lê Hoàn',BD)
C3(13,3.2,2.8,'Đinh Điền','ngờ Lê Hoàn',BD)
G('Quân Nguyễn Bặc',BD,8,[(R(14,0),105.78,19.82),(R(14,5),105.84,20.08),(R(15,0),105.86,20.20),(E(15,0),105.86,20.20)],show=(R(14,0),E(15,0)),emb='circle',seed=1602,spread=0.7,soff=(-50,10),defeats=[(at(15,'phóng lửa'),'flag',E(16,0))])
G('Thuyền Đinh Điền',BD,6,[(R(14,0),105.97,19.95),(R(14,5),105.98,20.14),(R(15,0),105.97,20.22),(E(15,0),105.97,20.22)],kind='ship',show=(R(14,0),E(15,0)),emb='circle',seed=1603,spread=0.6,soff=(50,0),label=False,defeats=[(at(15,'phóng lửa'),'flag',E(16,0))])
G('Quân Lê Hoàn',VT,10,[(R(14,0),105.90,20.28),(E(16,0),105.90,20.28)],show=(R(14,0),E(16,0)),emb='sun',seed=1604,spread=0.8,soff=(0,-35))
BATT.append((R(15,0.0),R(15,5.0),105.92,20.22,['Thuyền Đinh Điền','Quân Lê Hoàn']))
FIRES.append((at(15,'phóng lửa'),at(15,'phóng lửa',4.0),105.98,20.22))
FX.append((at(15,'phóng lửa'),at(15,'phóng lửa',3.0),'drums',(105.98,20.22),(105.98,20.22)))
G('Quân Phạm Hạp',BD,5,[(R(16,0),105.88,20.24),(R(16,5.0),106.20,21.20),(E(16,0),106.20,21.20)],show=(R(16,0),E(16,0)),emb='circle',seed=1605,spread=0.5,soff=(-30,0),defeats=[(at(16,'bắt sống'),'flag',E(16,0))],label=False)
show('Cát Lợi',16,16)
FACE(16,0.3,2.6,'Phạm Hạp','Cát Lợi','general',BD)
Q(14,16)
G('Thuyền Chiêm Thành',CH,14,[(R(17,0),106.45,18.90),(E(18,0),106.20,19.50),(R(19,0),105.95,19.93),(E(20,0),105.95,19.93)],kind='ship',show=(R(17,0),E(20,0)),emb='tri',seed=1606,spread=1.0,soff=(60,15),
  alive=[(0,1),(at(19,'bão'),1),(at(19,'bão')+3.0,0.08)],defeats=[(at(19,'lật đắm'),'flag',E(20,0))])
FACE(18,0.3,3.0,'Ngô Nhật Khánh','Cửa Đại Ác','lord',CH)
show('Cửa Đại Ác',17,20)
night(R(19,0.0),E(20,0.0))
FX.append((at(19,'bão'),at(19,'bão',3.0),'sea',(105.95,19.93),(105.95,19.93)))
PROPS.append((at(19,'bão')-0.5,E(20,0),'storm',105.98,19.84,'',0.45))
Q(19,20)
# ======================= CHƯƠNG 3: LÁ THƯ CỦA KẺ MUỐN ĐÁNH ÚP (22–34)
S2(22,34,[H,UC,TT,QC],1.7,hmax=360)
reg('NHÀ TỐNG',(110.6,23.2),P_TONG,TG,(22,63),alpha=13)
reg('ĐẠI CỒ VIỆT',(105.55,21.55),P_DCV,VT,(22,81),alpha=14)
show('Quảng Châu',22,63);show('Triều Tống',22,63)
C3(23,0.2,3.0,'Hầu Nhân Bảo','quan nhà Tống ở Ung Châu',TG)
NU(24,'năm 980','Hầu Nhân Bảo xin đánh úp Đại Cồ Việt',3.0)
LET(24,at(24,'dâng thư')-R(24,0),4.0,UC,TT,'thư xin đánh úp')
C3(26,0.4,3.0,'Lư Đa Tốn','bàn kế đánh úp',TG)
NT(28,0.4,3.2,UC[0],UC[1]-0.35,'ba mươi nghìn quân Kinh Hồ',TG)
G('Quân Tống ở Ung Châu',TG,12,[(at(31,'Ung Châu')-3.0,TT[0],TT[1]),(at(31,'Ung Châu')+1.5,UC[0],UC[1]),(E(34,0),UC[0],UC[1])],show=(at(31,'Ung Châu')-3.0,E(54,-1)),emb='tri',seed=1607,spread=0.8,soff=(-50,-20))
G('Quân Tống ở Quảng Châu',TG,10,[(at(31,'Quảng Châu')-3.0,TT[0],TT[1]),(at(31,'Quảng Châu')+1.5,QC[0],QC[1]),(E(34,0),QC[0],QC[1])],show=(at(31,'Quảng Châu')-3.0,E(54,-1)),emb='tri',seed=1608,spread=0.7,soff=(-40,-20))
AR(34,0.3,3.2,UC,LS,TG,'')
LET(33,0.2,3.4,LS,H,'tin cấp báo')
FX.append((at(31,'hẹn ngày'),at(31,'hẹn ngày',2.2),'horn',UC,UC))
PROPS.append((R(31,0.5),R(32,5.0),'pennants',UC[0]-0.6,UC[1]+0.15,'r',0.45))
# ======================= CHƯƠNG 4: TIẾNG HÔ VẠN TUẾ (35–42)
S2(35,42,[H],6.0)
PROPS.append((R(36,0.0),E(42,0),'hall',105.90,20.31,'',0.6))
C3(35,0.4,3.0,'Dương Thái hậu','mẹ vua Đinh Toàn',VT)
C3(35,3.4,2.8,'Phạm Cự Lạng','đại tướng quân',VT)
G('Các tướng của Phạm Cự Lạng',VT,9,[(R(36,0),105.72,20.20),(R(36,4.0),105.86,20.27),(E(38,0),105.86,20.27)],show=(R(36,0),E(38,0)),emb='sun',seed=1609,spread=0.9,soff=(-115,30),label=False)
FX.append((at(38,'vạn tuế'),at(38,'vạn tuế',1.8),'trumpet',H,H))
NU(40,'năm 980','Lê Hoàn lên ngôi hoàng đế',0.4)
FACE(40,3.4,3.4,'Lê Hoàn','Hoa Lư','king',GD,dy=-125)
FX.append((at(40,'lên ngôi'),at(40,'lên ngôi',1.6),'gong',H,H))
# ======================= CHƯƠNG 5: LẦN ĐÁNH LỪA THỨ NHẤT, MỘT LÁ THƯ (43–51)
S2(43,51,[H,UC,TT],2.0,hmax=380)
NUMS.append((_f(43),'Lần đánh lừa thứ nhất','Một lá thư mượn tên vua nhỏ',0.3))
LET(44,0.6,4.2,TT,H,'thư của vua Tống')
LET(46,at(46,'bức thư giả')-R(46,0)-0.4,4.2,H,TT,'thư giả mượn tên Đinh Toàn')
NT(47,0.6,3.0,TT[0],TT[1]-0.4,'xin hoãn việc đem quân',DK)
LET(48,0.8,4.0,TT,H,'thư trả lời: hai đường')
# ======================= CHƯƠNG 6: LẦN ĐÁNH LỪA THỨ HAI, GIẢ HÀNG (52–60)
S2(52,60,[LS,TK,BDG,(106.2,22.5)],3.4,hmax=360)
NU(52,'năm 981','Quân Tống áp sát bờ cõi',0.6)
for _nm in ('Lạng Sơn','Chi Lăng','Tây Kết','Bạch Đằng'): own(_nm,VT)
show('Lạng Sơn',52,63);show('Chi Lăng',52,63);show('Tây Kết',52,63);show('Bạch Đằng',52,63)
G('Đạo Hầu Nhân Bảo',TG,12,[(R(52,0),107.60,22.50),(at(52,'Lạng Sơn'),106.88,21.98),(R(55,0),106.80,21.88),(at(56,'mắc mưu'),106.58,21.74),(E(57,0),106.58,21.74)],show=(R(52,0),E(63,0)),emb='tri',seed=1610,spread=0.55,soff=(95,-55),
  alive=[(0,1),(at(56,'bị chém'),1),(at(56,'bị chém')+2.0,0.12)],defeats=[(at(56,'bị chém'),'flag',E(63,0))])
G('Đạo Trần Khâm Tộ',TG,12,[(R(52,3),107.00,22.70),(at(53,'Tây Kết'),106.10,22.18),(R(57,0),106.10,22.18),(at(57,'quay về'),106.90,22.80),(R(58,0),106.90,22.80),(at(58,'đuổi theo'),106.60,22.40),(E(58,0),106.60,22.40)],
  show=(R(52,3),E(63,0)),emb='tri',seed=1611,spread=0.6,soff=(-70,-45),alive=[(0,1),(at(58,'thua to'),1),(at(58,'thua to')+3.0,0.4)],defeats=[(at(58,'thua to'),'flag',E(63,0))])
G('Thuyền Lưu Trừng',TG,8,[(R(53,0),107.60,20.90),(at(53,'Bạch Đằng'),106.85,20.93),(E(57,0),106.85,20.93)],kind='ship',show=(R(53,0),E(63,0)),emb='tri',seed=1612,spread=0.4,soff=(80,25),label=False,
  alive=[(0,1),(at(57,'thua trận'),1),(at(57,'thua trận')+2.0,0.25)],defeats=[(at(57,'thua trận'),'flag',E(63,0))])
G('Quân Lê Hoàn ',VT,14,[(R(54,0),105.90,20.28),(R(54,2.5),105.98,20.72),(R(54,5.0),106.46,21.62),(R(57,0),106.46,21.62),(at(58,'đuổi theo'),106.50,21.95),(R(59,0),106.60,22.35),(E(59,0),106.60,22.35),(E(59,0)+2.0,105.90,20.28)],
  show=(R(54,0),E(60,0)),emb='sun',seed=1613,spread=0.6,soff=(-95,45))
FACE(54,0.3,3.0,'Lê Hoàn','Hoa Lư','general',VT,dx=0,dy=0,t_min=R(54,0.3))
BATT.append((at(58,'đuổi theo'),at(58,'đuổi theo')+4.6,106.60,22.35,['Đạo Trần Khâm Tộ','Quân Lê Hoàn ']))
NT(54,2.0,3.0,CLG[0],CLG[1],'đóng cọc cản đường trên sông Chi Lăng',BR)
NUMS.append((at(55,'lần đánh lừa thứ hai')-0.3,'Lần đánh lừa thứ hai','Cuộc đầu hàng giả',0.2))
FX.append((at(56,'bị chém'),at(56,'bị chém',3.0),'drums',CLG,CLG))
FX.append((at(58,'đuổi theo'),at(58,'đuổi theo',4.4),'drums',(106.50,21.95),(106.60,22.35)))
C3(59,0.4,2.8,'Quách Quân Biện','tướng Tống bị bắt',TG)
C3(59,3.3,2.6,'Triệu Phụng Huân','tướng Tống bị bắt',TG)
NT(60,0.4,3.2,CLG[0],CLG[1]-0.5,'trận quyết định chỉ chép vài dòng',DK)
Q(54,59)
PROPS.append((R(54,0.5),E(59,0),'pennants',106.30,22.05,'',0.55))
PROPS.append((R(52,0.5),E(57,0),'camp',107.20,22.20,'r',0.40))
PROPS.append((R(52,0.3),R(52,3.3),'ping',LS[0],LS[1],'r',0.8))
# ======================= CHƯƠNG 7: QUÂN TỐNG RÚT VỀ (61–67)
S2(61,67,[H,UC,TT,LS],1.9,hmax=380)
LET(61,0.5,3.6,UC,TT,'tin thua trận')
FX.append((at(61,'rút quân'),at(61,'rút quân',2.0),'horn',TT,TT))
G('Quân Tống rút về',TG,10,[(at(61,'rút quân'),106.60,22.35),(at(61,'rút quân')+5.5,UC[0],UC[1]),(E(63,0),UC[0],UC[1])],show=(at(61,'rút quân'),E(63,0)),emb='tri',seed=1614,spread=0.7,soff=(40,10),kind='cav',label=False)
NT(63,0.4,3.2,UC[0],UC[1]-0.45,'Vương Soạn bị giết ở Ung Châu',TG)
C3(65,0.4,3.0,'Lê Hoàn','được dâng tôn hiệu',VT)
C3(66,0.4,3.0,'Lê Văn Hưu','sử gia',GD)
# ======================= CHƯƠNG 8: ĐI ĐÁNH CHIÊM THÀNH (68–72)
S2(68,72,[H,SOUTH],1.9,hmax=380)
NU(69,'năm 982','Lê Hoàn đích thân đi đánh Chiêm Thành',3.4)
G('Quân Lê Hoàn đi nam',VT,12,[(at(69,'tự mình'),105.95,20.20),(at(69,'tự mình')+5.5,105.98,19.05),(R(71,0),105.98,19.05),(E(71,0),105.98,19.05)],kind='ship',show=(at(69,'tự mình'),E(71,0)),emb='sun',seed=1615,spread=0.9,soff=(-50,0))
G('Quân Chiêm Thành',CH,10,[(R(68,0),105.15,19.00),(E(71,0),105.15,19.00)],show=(R(68,0),E(71,0)),emb='tri',seed=1616,spread=0.6,soff=(-10,-20),defeats=[(at(70,'thua to'),'flag',E(71,0))])
NT(68,0.5,3.2,SOUTH[0],SOUTH[1]+0.40,'sứ giả Từ Mục, Ngô Tử Canh bị Chiêm Thành bắt giữ',CH)
BATT.append((at(70,'thua to')-1.2,at(70,'thua to')+3.8,105.50,19.02,['Quân Lê Hoàn đi nam','Quân Chiêm Thành']))
FX.append((at(70,'thua to')-1.0,at(70,'thua to')+3.6,'drums',(105.50,19.15),SOUTH))
Q(69,71)
NT(72,2.0,3.2,105.80,19.60,'kênh mới ở vùng núi Đồng Cổ, sông Bà Hòa',BR)
# ======================= CHƯƠNG 9: LẦN ĐÁNH LỪA THỨ BA, NGƯỜI COI SÔNG (73–84)
S2(73,75,[H,TT,UC],1.9,hmax=380)
NU(74,'năm 983','Thông hiếu với nhà Tống',3.0)
LET(74,at(74,'kết giao')-R(74,0),3.6,H,TT,'sứ sang thông hiếu')
LET(75,0.2,4.0,TT,H,'chế thư phong Tiết độ sứ')
PROPS.append((R(75,0.5),R(75,4.5),'seal',TT[0]-0.1,TT[1]-0.35,'',0.7))
C3(77,0.3,3.0,'Lê Hoàn','nhận chế thư rất kính cẩn',VT)
S2(78,84,[(106.35,21.00),H,LS],3.2,hmax=360)
show('Sách Giang',78,84)
NU(78,'năm 987','Sứ Tống Lý Giác sang',0.6)
G('Sứ Lý Giác',TG,5,[(R(78,0),LS[0],LS[1]),(at(79,'Lê Hoàn sai')+1.0,106.40,21.04),(E(82,0),106.40,21.04),(R(83,2.0),106.60,21.50),(E(84,0),LS[0]-0.05,LS[1]-0.1)],kind='cav',show=(R(78,0),E(84,0)),emb='tri',seed=1617,spread=0.4,soff=(55,0),label=False)
C3(78,2.4,2.6,'Lý Giác','sứ nhà Tống',TG)
NUMS.append((at(79,'lần đánh lừa thứ ba')-0.3,'Lần đánh lừa thứ ba','Nhà sư đóng vai người coi sông',0.2))
C3(79,3.4,2.8,'Pháp Thuận','sư, giả làm người coi sông',VT)
PROPS.append((R(80,0.3),E(82,0),'scrolls2',106.35,21.30,'',0.5))
NT(81,0.3,3.0,106.35,21.00,'đối thơ trên sông Sách',BR)
FACEMAP['Ngô Khuông Việt']=('Sách Giang','noble')
C3(83,0.3,2.8,'Ngô Khuông Việt','sư, làm bài từ tiễn',VT)
PROPS.append((R(80,0.0),R(81,5.0),'ping',106.35,21.00,'g',0.7))
# ======================= CHƯƠNG 10: LẦN ĐÁNH LỪA THỨ TƯ, KHÔNG LẠY (85–99)
S2(85,85,[(109.15,21.65),BDG,H],2.4,hmax=360)
NUMS.append((_f(85),'Lần đánh lừa thứ tư','Lần cuối cùng',0.4))
NU(85,'năm 990','Sứ Tống Cảo sang',3.2)
show('Liêm Châu',85,86)
G('Sứ Tống Cảo',TG,5,[(R(85,0),109.15,21.65),(R(85,6.5),106.85,20.95),(R(86,0),106.85,20.95),(R(86,3.0),106.35,20.58)],kind='ship',show=(R(85,0),R(86,3.0)),emb='tri',seed=1618,spread=0.4,soff=(60,5),label=False)
G('Sứ Tống Cảo đi bộ',TG,5,[(R(86,3.0),106.35,20.58),(R(86,5.5),106.20,20.45),(E(87,0),106.14,20.47)],kind='cav',show=(R(86,3.0),E(87,0)),emb='tri',seed=1618,spread=0.4,soff=(70,-25),label=False)
G('Thuyền đón sứ',VT,9,[(R(85,0.5),106.60,20.90),(R(85,6.5),106.85,20.95),(E(85,0),106.85,20.95)],kind='ship',show=(R(85,0.5),E(85,0)),emb='sun',seed=1619,spread=0.6,soff=(-30,-20),label=False)
C3(85,3.2,2.6,'Tống Cảo','sứ nhà Tống',TG)
S2(86,89,[H,(106.05,20.46)],5.0)
G('Thủy quân và khí giới',VT,10,[(R(86,2.0),105.80,20.18),(E(87,0),105.80,20.18)],show=(R(86,2.0),E(87,0)),emb='sun',seed=1620,spread=0.7,soff=(-60,15))
PROPS.append((R(88,0.0),E(89,0),'hall',105.90,20.31,'',0.6))
NT(88,0.4,3.2,105.90,20.28,'bưng thư vua Tống, không lạy',DK)
FACE(88,0.3,3.2,'Lê Hoàn','Hoa Lư','king',GD,dy=-190)
FX.append((at(88,'không lạy'),at(88,'không lạy',1.6),'gong',H,H))
S2(90,91,[H,LS,TT],1.9,hmax=380)
NT(90,0.4,3.2,LS[0],LS[1],'thư từ trao nhận ở biên giới',DK)
PROPS.append((R(90,1.0),R(91,3.0),'meeting',LS[0]+0.05,LS[1]-0.05,'',0.5))
S2(92,97,[H,UC,QC,TT],1.7,hmax=360)
NU(93,'năm 995','Vụ Như Hồng',0.4)
show('Như Hồng',93,98)
NT(93,1.6,3.2,108.55,21.75,'trấn Như Hồng bị cướp phá, theo quan Tống tâu',TG)
show('Quảng Châu',95,98)
LET(94,0.5,4.0,TT,H,'chiếu thư và đai ngọc')
C3(94,0.4,3.0,'Lý Nhược Chuyết','sứ nhà Tống',TG)
PROPS.append((R(94,3.4),R(95,0),'seal',TT[0]-0.1,TT[1]-0.35,'',0.6))
NT(96,0.5,3.4,QC[0],QC[1]-0.45,'Phiên Ngung (Quảng Châu): chỉ là lời nói, không có cuộc tấn công',GY)
AR(96,0.5,3.0,H,QC,GY,'')
NU(97,'năm 997','Nhà Tống phong Nam Bình Vương',3.4)
S2(98,99,[H,TT,UC],1.9,hmax=380)
NT(98,0.4,3.4,UC[0],UC[1]-0.45,'chỉ quan giữ biên giới nhận mệnh',TG)
PROPS.append((R(85,0.5),R(85,3.5),'ping',109.15,21.65,'r',0.6))
# ======================= CHƯƠNG 11: DỰNG NGHIỆP TRONG NƯỚC (100–105)
S2(100,101,[H,(105.95,20.63)],6.0)
PROPS.append((R(100,0.6),E(100,0),'hall',105.90,20.31,'',0.6))
NU(100,'năm 984','Đúc tiền Thiên Phúc',0.8)
show('Núi Đọi',101,101)
NU(101,'năm 987','Lần đầu cày ruộng tịch điền',0.6)
S2(102,104,[H,(105.47,20.22)],5.2,hmax=340)
NU(102,'năm 999','Đánh bốn mươi chín động',0.6)
show('Cử Long',103,104)
NU(103,'năm 1001','Đánh giặc ở Cử Long',0.6)
G('Quân Lê Hoàn đi Cử Long',VT,12,[(R(102,0),105.90,19.97),(R(102,4.0),105.75,20.08),(R(103,0),105.62,20.15),(R(103,3.5),105.58,20.14),(E(104,0),105.58,20.14)],kind='ship',show=(R(102,0),E(104,0)),emb='sun',seed=1621,spread=0.5)
RIVERS.append(('SÔNG MÃ',[(105.15,20.36),(105.26,20.29),(105.38,20.31),(105.50,20.22),(105.57,20.14),(105.66,20.17),(105.75,20.08),(105.82,20.09),(105.88,19.99),(105.95,19.93)],5,(105.48,20.02),(R(102,0),E(104,0))))
G('Giặc Cử Long',NEU,10,[(R(103,0),105.40,20.30),(E(104,0),105.40,20.30)],show=(R(103,0),E(104,0)),emb='circle',seed=1622,spread=0.7,soff=(-45,-40),defeats=[(at(104,'giặc tan vỡ'),'flag',E(104,0))])
BATT.append((R(103,3.0),E(104,-0.4),105.44,20.26,['Quân Lê Hoàn đi Cử Long','Giặc Cử Long']))
FACEMAP['Đinh Toàn']=('Cử Long','prince')
C3(104,0.3,2.8,'Đinh Toàn','Vệ Vương, trúng tên',VT)
Q(103,104)
S2(105,105,[H],5.2)
NU(105,'năm 1002','Đổi mười đạo thành lộ, phủ, châu',0.6)
# ======================= CHƯƠNG 12: KẾT (106–113)
S2(106,106,[H],5.4)
NU(106,'năm 1005','Lê Hoàn mất ở điện Trường Xuân',0.6)
PROPS.append((R(106,3.0),E(106,0),'tomb',105.93,20.34,'',0.8))
FACE(106,0.3,3.0,'Lê Hoàn','Hoa Lư','king',GD)
S2(107,113,[H,LS,UC],2.4,hmax=380)
reg('ĐẠI CỒ VIỆT',(105.55,21.55),P_DCV,VT,(107,113),alpha=16)
PROPS.append((R(112,0.4),R(112,3.4),'ping',LS[0],LS[1],'g',0.9))
PROPS.append((R(112,3.8),R(112,6.8),'ping',H[0],H[1],'g',0.9))
# ======================= HIỆU ỨNG THÊM
PROPS.append((R(14,0.5),E(16,0),'camp',105.52,20.02,'',0.40))
PROPS.append((R(98,0.3),R(98,3.3),'ping',UC[0],UC[1],'r',0.7))
AMBIENT.extend([(R(1,0),E(5,0),'wind',0.3),(R(6,0),E(21,0),'wind',0.35),(R(17,0),E(20,0),'sea',0.5),(R(22,0),E(34,0),'crowd',0.25),
 (R(35,0),E(42,0),'crowd',0.3),(R(52,0),E(60,0),'forest',0.4),(R(68,0),E(72,0),'sea',0.35),(R(73,0),E(84,0),'crowd',0.2),(R(78,0),E(82,0),'sea',0.25),
 (R(85,0),E(99,0),'crowd',0.25),(R(100,0),E(105,0),'wind',0.3),(R(106,0),TOTAL-1,'wind',0.3)])
TABLES.append((R(48,0.3),min(E(48,-0.2),R(48,0.3)+7.0),'Hai bức thư và hai đường nhà Tống đưa ra',[
 ('Thư vua Tống (tháng tám)','Ví nước ta như ngón tay ngón chân trên thân nhà Tống; không theo thì sẽ bị dẹp sạch.'),
 ('Thư giả của Lê Hoàn (tháng mười)','Mượn tên Đinh Toàn xin nhà Tống phong chức của cha, để nhà Tống hoãn đem quân sang.'),
 ('Thư trả lời của nhà Tống','Hai đường: Đinh Toàn làm thống soái, Lê Hoàn làm phó; hoặc mẹ con Đinh Toàn sang theo nhà Tống.')]))
# ======================= tông màu riêng + cảnh xen toàn khung
def RA(n,o=0): return T[BASE+n]+o
def EA(n,o=0): return T[BASE+n]+D[BASE+n]+o
GRADE={'sat':0.62,'tint':(188,212,232),'amt':0.8,'gain':0.97,'vig':0.6}
INTER=[]
INTER.append((RA(54,0.2),min(EA(54,-0.3),RA(54,0.2)+7.0),'split',{'head':'Tháng hai năm 981: hai bên đối mặt',
 'left':('Đại Cồ Việt','king',(200,60,50),['Vua Lê Hoàn đích thân cầm quân','Đóng cọc xuống sông Chi Lăng']),
 'right':('Nhà Tống','general',(60,90,170),['Quân chia ba hướng','Lạng Sơn, Tây Kết, sông Bạch Đằng'])}))
INTER.append((RA(66,0.2),min(EA(66,-0.3),RA(66,0.2)+6.0),'portrait',{'kind':'noble','col':(150,110,60),'name':'Lê Văn Hưu',
 'role':'Sử gia đời Trần','text':'Lê Hoàn bắt hai tướng Tống dễ như lùa trẻ con.'}))
INTER.append((RA(88,0.2),min(EA(88,-0.3),RA(88,0.2)+7.0),'portrait',{'kind':'king','col':(200,60,50),'name':'Lê Hoàn',
 'role':'Lý do ông nói với sứ Tống (ông bịa ra)','text':'Năm ngoái đi đánh giặc, bị ngã ngựa đau chân.'}))
INTER.append((RA(110,0.3),min(EA(112,-0.3),RA(110,0.3)+15.0),'timeline',{'head':'Bốn lần Lê Hoàn đánh lừa nhà Tống','nodes':[
 ('980','Thư giả mượn tên vua nhỏ, nhà Tống hoãn việc đem quân'),
 ('981','Giả hàng, dụ Hầu Nhân Bảo mắc mưu'),
 ('987','Nhà sư đóng vai người coi sông, đối thơ với sứ Tống'),
 ('990','Bưng thư đặt lên điện, nói đau chân, không lạy')]}))
# ======================= HOÀN TẤT
SCN.sort(key=lambda x:x[0])
CAM=[(0,SCN[0][2],SCN[0][3],SCN[0][4])]
for (a_,b_,lo,la,z) in SCN:
    CAM.append((R(a_)+1.6,lo,la,z));CAM.append((E(b_)-0.2,lo+0.01,la,z*1.03))
CAM=sorted(CAM,key=lambda k:k[0])
NIGHT.append((TOTAL,0));NIGHT=sorted(NIGHT,key=lambda k:k[0])
MINI=[(0,TOTAL)]
QUIET_AUDIO=True
MUSIC=[(0,R(5,0),'cang',1.0),(R(5,0),R(17,0),'bi',1.0),(R(17,0),R(22,0),'cang',1.0),(R(22,0),R(35,0),'cang',0.9),(R(35,0),R(43,0),'trang',1.0),
       (R(43,0),R(52,0),'cang',0.9),(R(52,0),R(61,0),'hanh',1.0),(R(61,0),R(68,0),'trang',1.0),(R(68,0),R(73,0),'hanh',1.0),(R(73,0),R(85,0),'binh',0.9),
       (R(85,0),R(92,0),'mo',0.9),(R(92,0),R(100,0),'binh',0.9),(R(100,0),R(106,0),'binh',1.0),(R(106,0),R(108,0),'bi',1.0),(R(108,0),TOTAL,'trang',1.0)]
def gate_open(t): return 0
def year_of(n):
    m=n-BASE
    for a,b,y in [(1,5,980),(6,21,979),(22,34,980),(35,42,980),(43,51,980),(52,67,981),(68,71,982),(72,72,983),(73,77,986),(78,84,987),(85,92,990),(93,95,995),(96,97,996),(98,99,997),
                  (100,100,984),(101,101,987),(102,102,999),(103,104,1001),(105,105,1002),(106,113,1005)]:
        if a<=m<=b: return y
    return None
NO_GROUP_LABEL=True
SIDES=[('Đại Cồ Việt',VT,{g['name'].strip() for g in GROUPS if g['col']==VT}),('Nhà Tống',TG,{g['name'].strip() for g in GROUPS if g['col']==TG}),
       ('Bặc, Điền, Hạp',BD,{g['name'].strip() for g in GROUPS if g['col']==BD}),('Chiêm Thành',CH,{g['name'].strip() for g in GROUPS if g['col']==CH}),
       ('Địa phương',NEU,{g['name'].strip() for g in GROUPS if g['col']==NEU})]
SFX=[(at(31,'hẹn ngày'),'horn'),(at(38,'vạn tuế'),'trumpet'),(at(40,'lên ngôi'),'gong'),(at(61,'rút quân'),'horn'),(R(85,0.2),'horn'),(R(88,1.0),'gong')]
SFX_GROUPS=['Sứ nhà Tống','Sứ Tống Cảo','Sứ Tống Cảo đi bộ','Sứ Lý Giác','Quân Tống rút về','Quân Tống rút về (mở đầu)']
