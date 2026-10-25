"""LH5 (bản kể theo kiểu điều tra, 89 đoạn, n = 16001–16089; đoạn gióng từ bản lh2 qua FIRST5/LAST5). Lê Hoàn không lạy sứ Tống (đánh quân Tống năm 981). Số đoạn 1–90 (n = 12001–12090; chỉ số trong file này là chỉ số của bản lh1 cũ, được đổi qua bảng M). Bản đồ world7 (Bắc Bộ, Lạng Sơn, Ung Châu, Quảng Châu).
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
BASE=16000
def M(n):
    """Chỉ số đoạn bản lh1 cũ (1..87) sang chỉ số lh2 (1..90)."""
    if n<=4: return n
    if n<=15: return n+1
    if n<=55: return n+2
    return n+3
def Mi2(m):
    for o in range(1,88):
        if M(o)>=m: return o
    return 87
# lh5: bảng gióng đoạn lh2 -> đoạn lh5 (khớp theo chữ giữa hai bản kịch bản)
FIRST5={1: 1, 2: 2, 3: 4, 4: 6, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: 11, 12: 12, 13: 13, 14: 14, 15: 14, 16: 15, 17: 17, 18: 17, 19: 19, 20: 20, 21: 21, 22: 21, 23: 22, 24: 23, 25: 23, 26: 24, 27: 25, 28: 26, 29: 27, 31: 28, 32: 29, 33: 30, 34: 31, 35: 32, 36: 33, 37: 34, 38: 35, 39: 36, 40: 37, 41: 38, 42: 39, 43: 40, 44: 41, 45: 42, 46: 43, 47: 44, 48: 45, 49: 46, 51: 47, 52: 48, 53: 49, 54: 50, 55: 50, 56: 51, 59: 54, 60: 55, 61: 56, 62: 58, 63: 59, 64: 60, 65: 61, 66: 62, 67: 63, 68: 65, 69: 66, 70: 68, 71: 69, 72: 73, 73: 73, 74: 75, 75: 76, 76: 77, 77: 78, 78: 78, 79: 79, 80: 80, 81: 81, 82: 82, 84: 83, 85: 83, 86: 84, 87: 85, 88: 86, 90: 88}
LAST5={1: 1, 2: 2, 3: 4, 4: 6, 6: 7, 7: 8, 8: 9, 9: 10, 10: 10, 11: 11, 12: 12, 13: 13, 14: 14, 15: 15, 16: 16, 17: 17, 18: 18, 19: 19, 20: 20, 21: 21, 22: 22, 23: 22, 24: 23, 25: 23, 26: 24, 27: 25, 28: 26, 29: 27, 31: 28, 32: 29, 33: 30, 34: 32, 35: 33, 36: 34, 37: 34, 38: 36, 39: 37, 40: 38, 41: 38, 42: 39, 43: 40, 44: 41, 45: 42, 46: 43, 47: 45, 48: 45, 49: 46, 51: 47, 52: 48, 53: 49, 54: 50, 55: 51, 56: 51, 59: 54, 60: 55, 61: 56, 62: 58, 63: 59, 64: 60, 65: 61, 66: 62, 67: 63, 68: 66, 69: 68, 70: 69, 71: 69, 72: 73, 73: 74, 74: 76, 75: 77, 76: 77, 77: 78, 78: 79, 79: 79, 80: 80, 81: 81, 82: 82, 84: 83, 85: 84, 86: 84, 87: 85, 88: 86, 90: 88}
SRC5={1: 1, 2: 2, 3: 2, 4: 3, 5: 3, 6: 6, 7: 6, 8: 8, 9: 9, 10: 9, 11: 11, 12: 12, 13: 13, 14: 14, 15: 15, 16: 16, 17: 18, 18: 18, 19: 19, 20: 20, 21: 21, 22: 23, 23: 25, 24: 26, 25: 27, 26: 28, 27: 29, 28: 31, 29: 32, 30: 33, 31: 34, 32: 35, 33: 36, 34: 36, 35: 38, 36: 39, 37: 39, 38: 41, 39: 42, 40: 43, 41: 44, 42: 45, 43: 46, 44: 47, 45: 48, 46: 49, 47: 51, 48: 52, 49: 53, 50: 54, 51: 55, 52: 55, 53: 55, 54: 59, 55: 60, 56: 61, 57: 61, 58: 62, 59: 63, 60: 64, 61: 65, 62: 66, 63: 67, 64: 67, 65: 68, 66: 68, 67: 69, 68: 70, 69: 71, 70: 71, 71: 71, 72: 71, 73: 72, 74: 73, 75: 74, 76: 75, 77: 76, 78: 77, 79: 79, 80: 80, 81: 81, 82: 82, 83: 85, 84: 85, 85: 87, 86: 88, 87: 88, 88: 90, 89: 90}
def _first(m):
    while m<=90 and m not in FIRST5: m+=1
    return FIRST5[min(m,90) if min(m,90) in FIRST5 else 90]
def _last(m):
    while m>=1 and m not in LAST5: m-=1
    return LAST5[max(m,1) if max(m,1) in LAST5 else 1]
def Mi(k): return Mi2(SRC5.get(k,1))
def _f(n): return BASE+_first(M(n))
def _l(n): return BASE+_last(M(n))
def _nx(n): return _first(M(n))
def _pv(n): return max(_last(M(n)),_first(M(n)))
from build2 import T,D,TOTAL,chap,PH
def R(n,o=0): return T[BASE+_nx(n)]+o
def E(n,o=0): k=_pv(n); return T[BASE+k]+D[BASE+k]+o
def at(n,sub,off=0.0):
    """Thời điểm chữ `sub` được đọc trong các đoạn lh5 ứng với đoạn n; chưa có nhận dạng thì ước theo vị trí chữ."""
    a=_nx(n);b=_pv(n)
    for k in range(a,b+1):
        txt=_B.texts[BASE+k].lower()
        if sub.lower() in txt:
            p=txt.find(sub.lower())/max(1,len(txt))
            return T[BASE+k]+0.3+p*max(1.0,D[BASE+k]-0.8)+off
    return T[BASE+a]+0.3+0.2*max(1.0,D[BASE+a]-0.8)+off
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
NU(5,'năm 979','Đinh Tiên Hoàng bị giết',4.2)
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
G('Các tướng của Phạm Cự Lạng',VT,9,[(R(24,0),105.72,20.20),(R(24,4.0),105.86,20.27),(E(26,0),105.86,20.27)],show=(R(24,0),E(26,0)),emb='sun',seed=1109,spread=0.9,soff=(-115,30),label=False)
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
G('Quân Lê Hoàn ',VT,14,[(R(38,0),105.90,20.28),(R(38,2.5),105.98,20.72),(R(38,5.0),106.46,21.62),(R(41,0),106.46,21.62),(at(42,'đuổi theo'),106.50,21.95),(R(43,0),106.60,22.35),(E(43,0),106.60,22.35),(E(43,0)+2.0,105.90,20.28)],
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
G('Quân Lê Hoàn đi nam',VT,12,[(at(52,'tự mình'),105.95,20.20),(at(52,'tự mình')+5.5,105.98,19.05),(R(54,0),105.98,19.05),(E(54,0),105.98,19.05)],kind='ship',show=(at(52,'tự mình'),E(54,0)),emb='sun',seed=1115,spread=0.9,soff=(-50,0))
G('Quân Chiêm Thành',CH,10,[(R(51,0),105.15,19.00),(E(54,0),105.15,19.00)],show=(R(51,0),E(54,0)),emb='tri',seed=1116,spread=0.6,soff=(-10,-20),defeats=[(at(53,'thua to'),'flag',E(54,0))])
NT(51,0.5,3.2,SOUTH[0],SOUTH[1]+0.40,'sứ giả Từ Mục, Ngô Tử Canh bị Chiêm Thành bắt giữ',CH)
BATT.append((at(53,'thua to')-1.2,at(53,'thua to')+3.8,105.50,19.02,['Quân Lê Hoàn đi nam','Quân Chiêm Thành']))
FX.append((at(53,'thua to')-1.0,at(53,'thua to')+3.6,'drums',(105.50,19.15),SOUTH))
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
G('Sứ Tống Cảo',TG,5,[(R(65,0),109.15,21.65),(R(65,6.5),106.85,20.95),(R(66,0),106.85,20.95),(R(66,3.0),106.35,20.58)],kind='ship',show=(R(65,0),R(66,3.0)),emb='tri',seed=1118,spread=0.4,soff=(60,5),label=False)
G('Sứ Tống Cảo đi bộ',TG,5,[(R(66,3.0),106.35,20.58),(R(66,5.5),106.20,20.45),(E(67,0),106.14,20.47)],kind='cav',show=(R(66,3.0),E(67,0)),emb='tri',seed=1118,spread=0.4,soff=(70,-25),label=False)
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
G('Quân Lê Hoàn đi Cử Long',VT,12,[(R(80,0),105.90,19.97),(R(80,4.0),105.75,20.08),(R(81,0),105.62,20.15),(R(81,3.5),105.58,20.14),(E(82,0),105.58,20.14)],kind='ship',show=(R(80,0),E(82,0)),emb='sun',seed=1121,spread=0.5)
RIVERS.append(('SÔNG MÃ',[(105.15,20.36),(105.26,20.29),(105.38,20.31),(105.50,20.22),(105.57,20.14),(105.66,20.17),(105.75,20.08),(105.82,20.09),(105.88,19.99),(105.95,19.93)],5,(105.48,20.02),(R(80,0),E(82,0))))
G('Giặc Cử Long',NEU,10,[(R(81,0),105.40,20.30),(E(82,0),105.40,20.30)],show=(R(81,0),E(82,0)),emb='circle',seed=1122,spread=0.7,soff=(-45,-40),defeats=[(at(82,'giặc tan vỡ'),'flag',E(82,0))])
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
PROPS.append((R(11,0.5),E(13,0),'camp',105.52,20.02,'',0.40))
PROPS.append((R(38,0.5),E(43,0),'pennants',106.30,22.05,'',0.55))
PROPS.append((R(36,0.5),E(41,0),'camp',107.20,22.20,'r',0.40))
PROPS.append((R(36,0.3),R(36,3.3),'ping',LS[0],LS[1],'r',0.8))
PROPS.append((R(65,0.5),R(65,3.5),'ping',109.15,21.65,'r',0.6))
AMBIENT.extend([(R(1,0),E(4,0),'wind',0.3),(R(5,0),E(15,0),'wind',0.35),(R(14,0),E(15,0),'sea',0.5),(R(16,0),E(22,0),'crowd',0.25),
 (R(23,0),E(28,0),'crowd',0.3),(R(36,0),E(44,0),'forest',0.4),(R(51,0),E(55,0),'sea',0.35),(R(56,0),E(64,0),'crowd',0.2),(R(59,0),E(62,0),'sea',0.25),
 (R(65,0),E(77,0),'crowd',0.25),(R(78,0),E(83,0),'wind',0.3),(R(84,0),TOTAL-1,'wind',0.3)])

# ======================= LH2: dẫn chương theo ba câu trả lời và khung so sánh
for _n,_big,_small in [(6,'Bằng chứng thứ nhất','Ông có ngôi vững'),(17,'Bằng chứng thứ hai','Ông đã thắng quân Tống'),(49,'Bằng chứng thứ ba','Ông biết lúc nào nên cúi')]:
    NUMS.append((BASE+_n,_big,_small,0.3))
TABLES.append((R(34,0.3),min(E(34,-0.2),R(34,0.3)+7.0),'Hai bức thư và hai đường nhà Tống đưa ra',[
 ('Thư vua Tống (tháng tám)','Ví nước ta như ngón tay ngón chân trên thân nhà Tống; không theo thì sẽ bị dẹp sạch.'),
 ('Thư giả của Lê Hoàn (tháng mười)','Mượn tên Đinh Toàn xin nhà Tống phong chức của cha, để nhà Tống hoãn đem quân sang.'),
 ('Thư trả lời của nhà Tống','Hai đường: Đinh Toàn làm thống soái, Lê Hoàn làm phó; hoặc mẹ con Đinh Toàn sang theo nhà Tống.')]))
# ======================= LH2: tông màu riêng + cảnh xen toàn khung (dùng số đoạn lh2 tuyệt đối)
def RA(m,o=0): return T[BASE+_first(m)]+o
def EA(m,o=0): k=max(_last(m),_first(m)); return T[BASE+k]+D[BASE+k]+o
GRADE={'sat':0.62,'tint':(188,212,232),'amt':0.8,'gain':0.97,'vig':0.6}
INTER=[]
INTER.append((RA(38,0.2),min(EA(38,-0.3),RA(38,0.2)+7.0),'split',{'head':'Tháng hai năm 981: hai bên đối mặt',
 'left':('Đại Cồ Việt','king',(200,60,50),['Vua Lê Hoàn đích thân cầm quân','Đóng cọc xuống sông Chi Lăng']),
 'right':('Nhà Tống','general',(60,90,170),['Quân chia ba hướng','Lạng Sơn, Tây Kết, sông Bạch Đằng'])}))
INTER.append((RA(51,0.2),min(EA(51,-0.3),RA(51,0.2)+6.0),'portrait',{'kind':'noble','col':(150,110,60),'name':'Lê Văn Hưu',
 'role':'Sử gia đời Trần','text':'Lê Hoàn bắt hai tướng Tống dễ như lùa trẻ con.'}))
INTER.append((T[BASE+69]+0.2,min(EA(70,-0.3),T[BASE+69]+7.0),'portrait',{'kind':'king','col':(200,60,50),'name':'Lê Hoàn',
 'role':'Lý do ông nói với sứ Tống (ông bịa ra)','text':'Năm ngoái đi đánh giặc, bị ngã ngựa đau chân.'}))
INTER.append((T[BASE+87]+0.3,min(EA(90,-0.3),T[BASE+87]+14.0),'timeline',{'head':'Bốn lần Lê Hoàn tiếp sứ nhà Tống','nodes':[
 ('986','Nhận thư phong chức rất kính cẩn, trả hai tướng Tống bị bắt'),
 ('987','Sứ Lý Giác sang, hai bên đối thơ'),
 ('990','Bưng thư đặt lên điện mà không lạy'),
 ('996','Ra đón ngoài thành, sau mới tạ lỗi')]}))
# ======================= ẢNH 2D CHEN TOÀN KHUNG (thử nghiệm, chương Bằng chứng thứ nhất) + máy quay bám tiêu điểm
CAMFOCUS=True
_PIC='/home/claude/fact-video/assets/anh_2d/LH5R/%03d.jpg'
def PIC(n,off,dur,img,z0=1.0,z1=1.08,dx=0,dy=0):
    t0=T[n]+off
    INTER.append((t0,min(t0+dur,T[n]+D[n]-0.1),'pic',{'path':_PIC%img,'z0':z0,'z1':z1,'dx':dx,'dy':dy}))
PIC(16006,0.4,3.0,17,1.0,1.10,0,1)      # đêm trăng, ngai trống
PIC(16007,0.3,3.0,20,1.08,1.0,1,0)      # vua nhỏ trên ngai
PIC(16007,3.6,2.6,21,1.0,1.08,-1,0)     # Lê Hoàn đứng sau ngai
PIC(16008,0.3,3.0,23,1.0,1.10,1,0)      # cậu bé mồ côi
PIC(16008,3.8,2.8,24,1.08,1.0,-1,0)     # được quan nhận nuôi
PIC(16009,0.3,2.6,28,1.0,1.08,0,-1)     # vua khen
PIC(16009,3.5,2.8,29,1.0,1.10,0,1)      # dẫn một nghìn quân
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
    m=Mi(n-BASE)
    for a,b,y in [(1,2,990),(3,3,980),(4,4,None),(5,15,979),(16,35,980),(36,50,981),(51,54,982),(55,55,983),(56,58,986),(59,64,987),(65,70,990),(71,71,995),(72,75,996),(76,77,997),
                  (78,78,984),(79,79,987),(80,80,999),(81,82,1001),(83,83,1002),(84,85,1005),(86,87,None)]:
        if a<=m<=b: return y
    return None
NO_GROUP_LABEL=True
SIDES=[('Đại Cồ Việt',VT,{g['name'].strip() for g in GROUPS if g['col']==VT}),('Nhà Tống',TG,{g['name'].strip() for g in GROUPS if g['col']==TG}),
       ('Bặc, Điền, Hạp',BD,{g['name'].strip() for g in GROUPS if g['col']==BD}),('Chiêm Thành',CH,{g['name'].strip() for g in GROUPS if g['col']==CH}),
       ('Địa phương',NEU,{g['name'].strip() for g in GROUPS if g['col']==NEU})]
SFX=[(at(21,'hẹn ngày'),'horn'),(at(26,'vạn tuế'),'trumpet'),(at(27,'lên ngôi'),'gong'),(at(45,'rút quân'),'horn'),(R(65,0.2),'horn'),(R(67,1.0),'gong')]
SFX_GROUPS=['Sứ nhà Tống','Sứ Tống Cảo','Sứ Tống Cảo đi bộ','Sứ Lý Giác','Quân Tống rút về']
