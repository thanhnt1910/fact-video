"""Nguyên Mông ba lần thua vì quân lương (nm2). Số đoạn 1–65 (n = 22001–22065), BASE=22000. Địa danh vị trí gần đúng (mức B).
Hiệu ứng: thẻ nhân vật, mặt, quân và thuyền di chuyển, bãi cọc và thủy triều Bạch Đằng, lửa vườn không nhà trống, trống, kèn, chiêng, nước.
Bố cục theo CLAUDE.md: không khung trích lời, không khung đùa, Q() ẩn ghi chú khi giao tranh."""
from build2 import T,D,TOTAL,chap,PH
import build2 as _B
import world7 as _W
INF=1e9
BASE=22000
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
VT=GR      # Đại Việt xanh lá
NG=RD      # quân Nguyên đỏ
LOC={'Thăng Long':(105.85,21.03,'big'),'Vân Đồn':(107.45,21.10,'mid'),'Bình Lệ Nguyên':(105.62,21.28,'town'),'Quy Hóa':(104.90,21.72,'mid'),
     'Bình Than':(106.45,21.17,'town'),'Chiêm Thành':(105.15,19.00,'mid'),'Lạng Sơn':(106.76,21.85,'mid'),'Vạn Kiếp':(106.38,21.07,'town'),
     'Đà Mạc':(106.00,20.58,'town'),'Thanh Hóa':(105.78,19.80,'mid'),'Hàm Tử':(106.02,20.84,'town'),'Chương Dương':(105.80,20.98,'town'),
     'Tây Kết':(106.22,20.70,'town'),'Bạch Đằng':(106.80,20.95,'town'),'Long Hưng':(106.35,20.55,'town'),'Tư Minh':(107.20,22.35,'town')}
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
# ---- tên vùng
H=X('Thăng Long');BLN=X('Bình Lệ Nguyên');QH=X('Quy Hóa');BT=X('Bình Than');VK=X('Vạn Kiếp');ĐM=X('Đà Mạc');HT=X('Hàm Tử');CD=X('Chương Dương')
TKT=X('Tây Kết');TH=X('Thanh Hóa');VD=X('Vân Đồn');BDG=X('Bạch Đằng');LH=X('Long Hưng');CT=X('Chiêm Thành');LS=X('Lạng Sơn');TM=X('Tư Minh')
P_DV=[(104.7,22.3),(106.5,22.6),(107.8,21.5),(107.3,20.3),(106.2,19.6),(105.3,19.0),(104.6,19.9),(104.5,21.2)]
P_NG=[(105.0,23.3),(106.6,23.0),(108.0,22.7),(108.6,22.3),(109.6,22.4),(111.0,22.6),(112.4,23.0),(112.4,25.0),(105.0,25.0)]
# ======================= CHƯƠNG 1: HAI BA NGÀY (1–4), hook
TITLES.append((0.3,3.8,'QUÂN LƯƠNG','ĐÁNH BẠI MÔNG CỔ','Đại Việt, từ năm 1258 đến năm 1288'))
show('Thăng Long',1,4);show('Vân Đồn',1,4)
own('Thăng Long',VT);own('Vân Đồn',VT)
S2(1,4,[H,VD],2.4,hmax=360)
G('Tướng bị xiềng giải về kinh',VT,4,[(R(1,0),VD[0],VD[1]),(R(1,5.5),H[0],H[1]),(E(2,0),H[0],H[1])],kind='cav',show=(R(1,0),E(2,0)),emb='sun',seed=2201,spread=0.4,soff=(40,10),label=False)
C3(1,0.4,3.0,'Trần Khánh Dư','bị xiềng tay, giải về kinh',VT)
G('Hạm đội quân Nguyên',NG,14,[(R(2,0),106.95,20.60),(R(2,7),106.50,20.75),(E(2,0),106.30,20.80)],kind='ship',show=(R(2,0),E(2,0)),emb='tri',seed=2202,spread=0.9,soff=(-55,30))
NT(2,0.4,3.2,VD[0],VD[1]-0.45,'hạm đội địch vượt qua vùng biển ông giữ',NG)
PROPS.append((R(3,0.5),R(3,3.4),'ping',VD[0],VD[1],'g',0.9))
PROPS.append((R(4,0.3),R(4,3.3),'ping',BDG[0],BDG[1],'g',0.9))
# ======================= CHƯƠNG 2: LẦN THỨ NHẤT (5–11)
S2(5,11,[QH,BLN,H],3.0,hmax=380)
reg('NGUYÊN MÔNG',(104.8,22.9),P_NG,NG,(5,11),alpha=12)
reg('ĐẠI VIỆT',(105.7,21.7),P_DV,VT,(5,11),alpha=14)
show('Bình Lệ Nguyên',5,8);show('Quy Hóa',5,11);show('Thăng Long',5,11)
own('Bình Lệ Nguyên',VT);own('Quy Hóa',VT)
NU(5,'năm 1257','Quân Mông Cổ đánh vào Đại Việt',0.4)
G('Quân Mông Cổ',NG,14,[(R(5,0),QH[0],QH[1]),(R(5,6),BLN[0],BLN[1]),(R(7,0),BLN[0],BLN[1]),(R(8,3),105.78,21.15),(at(9,'Đông Bộ Đầu'),H[0]+0.03,H[1]),(R(10,0),H[0]+0.03,H[1]),(at(10,'Quy Hóa'),QH[0],QH[1]),(E(11,0),QH[0],QH[1])],kind='cav',show=(R(5,0),E(11,0)),emb='tri',seed=2203,spread=0.7,soff=(-60,-20),
  alive=[(0,1),(at(9,'đánh tan'),1),(at(9,'đánh tan')+3.0,0.45)],defeats=[(at(10,'đánh thua'),'flag',E(11,0))])
G('Quân Trần Thái Tông',VT,10,[(R(5,3),H[0],H[1]),(R(6,0),BLN[0]+0.06,BLN[1]-0.05),(R(6,5),H[0]-0.05,H[1]),(at(9,'thuyền lớn'),H[0]-0.05,H[1]),(at(9,'Đông Bộ Đầu'),H[0]+0.0,H[1]),(E(11,0),H[0],H[1])],kind='ship',show=(R(5,3),E(9,0)),emb='sun',seed=2204,spread=0.6,soff=(-70,25),label=False)
C3(5,2.2,3.0,'Trần Thái Tông','đích thân ra trận',VT)
C3(8,0.3,3.0,'Trần Thủ Độ','Thái sư',VT)
BATT.append((at(9,'đón đánh'),at(9,'đón đánh')+4.5,H[0]+0.02,H[1],['Quân Mông Cổ','Quân Trần Thái Tông']))
FX.append((at(9,'đón đánh'),at(9,'đón đánh',3.5),'drums',H,(H[0]+0.1,H[1])))
FX.append((at(5,'đánh vào'),at(5,'đánh vào',1.8),'horn',QH,QH))
Q(9,9)
PROPS.append((R(7,0.3),R(7,3.3),'scrolls2',BLN[0],BLN[1]+0.05,'',0.5))
NT(11,0.4,3.4,QH[0]+0.15,QH[1]-0.35,'hơn hai mươi năm sau, Mông Cổ quay lại với tên nhà Nguyên',NG)
# ======================= CHƯƠNG 3: BÌNH THAN (12–18)
S2(12,18,[BT,H],3.4,hmax=360)
show('Bình Than',12,18);show('Thăng Long',12,18);own('Bình Than',VT)
NU(12,'năm 1282','Hội nghị Bình Than',0.5)
G('Thuyền các vương hầu',VT,9,[(R(12,0),H[0],H[1]),(R(12,6),BT[0]-0.04,BT[1]+0.0),(E(18,0),BT[0]-0.04,BT[1])],kind='ship',show=(R(12,0),E(18,0)),emb='sun',seed=2205,spread=0.7,soff=(-70,20),label=False)
G('Thuyền chở than',NEU,2,[(R(13,0),BT[0]+0.18,BT[1]-0.08),(R(13,2.5),BT[0]+0.05,BT[1]-0.02),(E(15,0),BT[0]+0.05,BT[1]-0.02)],kind='ship',show=(R(13,0),E(16,0)),emb='circle',seed=2206,spread=0.3,soff=(70,20),label=False)
C3(13,2.0,3.0,'Trần Khánh Dư','đang bán than ở Chí Linh',VT)
FACEMAP['Trần Quốc Toản']=('Bình Than','youth')
C3(16,2.8,3.0,'Trần Quốc Toản','Hoài Văn hầu, còn trẻ',VT)
NT(14,0.3,3.2,BT[0]+0.2,BT[1]+0.28,'bị tước hết chức, về Chí Linh bán than',BR)
NT(17,0.3,3.4,BT[0]-0.1,BT[1]+0.3,'quả cam bị bóp nát trong tay',GD)
G('Gia nô Trần Quốc Toản',VT,8,[(at(17,'gom'),BT[0]-0.15,BT[1]+0.12),(at(17,'đóng thuyền'),BT[0]-0.15,BT[1]+0.12),(E(18,0),BT[0]-0.15,BT[1]+0.12)],show=(at(17,'gom'),E(18,0)),emb='circle',seed=2207,spread=0.6,soff=(-90,-40),label=False)
PROPS.append((at(18,'cờ'),E(18,0),'pennants',BT[0]-0.15,BT[1]+0.25,'g',0.55))
PROPS.append((R(12,1.0),R(12,4.0),'meeting',BT[0],BT[1]+0.05,'',0.55))
# ======================= CHƯƠNG 4: MƯỢN ĐƯỜNG (19–22)
S2(19,22,[CT,LS,H],1.9,hmax=380)
NU(19,'năm 1284','Nhà Nguyên xin mượn đường',0.5)
show('Chiêm Thành',19,22);show('Lạng Sơn',19,22);show('Thăng Long',19,22)
reg('NGUYÊN MÔNG',(108.2,23.4),P_NG,NG,(19,22),alpha=12)
AR(19,0.6,4.0,LS,CT,NG,'xin mượn đường đánh Chiêm Thành')
G('Đạo Thoát Hoan',NG,16,[(R(20,0),LS[0]+0.5,LS[1]+0.45),(R(20,5),LS[0]+0.05,LS[1]+0.02),(E(22,0),LS[0]+0.05,LS[1]+0.02)],kind='cav',show=(R(20,0),E(22,0)),emb='tri',seed=2208,spread=0.7,soff=(40,10))
C3(20,2.4,3.0,'Thoát Hoan','con trai Hốt Tất Liệt',NG)
C3(21,0.3,3.0,'Trần Thánh Tông','vua cha',VT)
PROPS.append((R(21,1.2),E(22,0),'meeting',H[0],H[1]+0.05,'',0.6))
FX.append((at(22,'hô đánh'),at(22,'hô đánh',2.2),'trumpet',H,H))
C3(22,3.0,3.0,'Trần Hưng Đạo','tổng chỉ huy quân đội',VT)
FACEMAP['Trần Hưng Đạo']=('Thăng Long','general')
# ======================= CHƯƠNG 5: LẦN THỨ HAI (23–29)
S2(23,29,[VK,H,TH],2.6,hmax=380)
NU(23,'năm 1285','Quân Nguyên tràn xuống',0.4)
show('Vạn Kiếp',23,29);show('Đà Mạc',23,29);show('Thanh Hóa',26,29);show('Thăng Long',23,29)
reg('NGUYÊN MÔNG',(108.2,23.4),P_NG,NG,(23,29),alpha=10)
G('Quân Ô Mã Nhi',NG,16,[(R(23,0),LS[0]-0.1,LS[1]-0.2),(at(23,'Vạn Kiếp'),VK[0],VK[1]),(R(24,0),VK[0],VK[1]),(R(25,0),ĐM[0]-0.2,ĐM[1]+0.1),(E(29,0),H[0]+0.05,H[1]-0.02)],kind='cav',show=(R(23,0),E(29,0)),emb='tri',seed=2209,spread=0.8,soff=(40,-25))
G('Quân Toa Đô',NG,14,[(R(24,0),CT[0],CT[1]),(R(24,6),TH[0],TH[1]-0.1),(R(25,0),105.90,20.40),(E(29,0),ĐM[0],ĐM[1])],kind='ship',show=(R(24,0),E(29,0)),emb='tri',seed=2210,spread=0.8,soff=(-65,10),label=False)
G('Quân Đại Việt lui',VT,10,[(R(23,0),VK[0],VK[1]),(at(23,'thua chạy'),VK[0]-0.1,VK[1]-0.05),(R(25,0),ĐM[0],ĐM[1]),(R(26,0),TH[0],TH[1]),(E(29,0),TH[0],TH[1])],show=(R(23,0),E(29,0)),emb='sun',seed=2211,spread=0.6,soff=(-80,-30),label=False)
BATT.append((R(23,2.0),R(23,6.5),VK[0],VK[1],['Quân Ô Mã Nhi','Quân Đại Việt lui']))
FX.append((R(23,1.5),R(23,6.0),'drums',VK,(VK[0]-0.1,VK[1])))
C3(25,0.4,3.0,'Trần Bình Trọng','Bảo Nghĩa Vương',VT)
FACEMAP['Trần Bình Trọng']=('Đà Mạc','general')
SKULL(26,0.9,3.2,ĐM[0],ĐM[1],'Trần Bình Trọng bị giết')
FX.append((at(26,'thét'),at(26,'thét',1.5),'gong',ĐM,ĐM))
NT(27,0.5,3.2,TH[0]+0.1,TH[1]+0.30,'vào Thanh Hóa lánh giặc',VT)
NT(28,0.3,3.2,H[0],H[1]+0.45,'giặc đi xa nhiều năm, chở lương hàng vạn dặm',NG)
FIRES.append((at(29,'vườn không nhà trống'),E(29,0),H[0]+0.1,H[1]+0.05))
FIRES.append((at(29,'vườn không nhà trống')+1.5,E(29,0),H[0]-0.12,H[1]-0.10))
NT(29,3.0,3.4,H[0],H[1]-0.4,'rút đi, không để lại lương thực',BR)
AMBIENT.append((R(23,0),E(24,0),'crowd',0.3))
PROPS.append((R(27,3.5),E(27,0),'ping',TH[0],TH[1],'g',0.8))
# ======================= CHƯƠNG 6: PHẢN CÔNG (30–37)
S2(30,37,[CD,HT,TKT],4.2,hmax=330)
NU(30,'mùa hạ năm 1285','Phản công',0.4)
show('Hàm Tử',30,37);show('Chương Dương',30,37);show('Tây Kết',30,37)
for _n in ('Hàm Tử','Chương Dương','Tây Kết'): own(_n,VT)
G('Quân Nguyên ở Hàm Tử',NG,12,[(R(30,0),HT[0]-0.03,HT[1]),(E(33,0),HT[0]-0.03,HT[1])],show=(R(30,0),E(33,0)),emb='tri',seed=2212,spread=0.6,soff=(-60,-75),defeats=[(at(32,'bỏ chạy'),'flag',E(33,0))],alive=[(0,1),(at(32,'bỏ chạy'),1),(at(32,'bỏ chạy')+3,0.3)])
G('Quân Trần Nhật Duật',VT,10,[(R(30,0),HT[0]+0.08,HT[1]-0.05),(E(33,0),HT[0]+0.08,HT[1]-0.05)],show=(R(30,0),E(33,0)),emb='sun',seed=2213,spread=0.5,soff=(85,-70),label=False)
C3(30,3.0,3.0,'Trần Nhật Duật','chỉ huy trận Hàm Tử',VT)
FACEMAP['Trần Nhật Duật']=('Hàm Tử','general')
NT(31,0.3,3.2,HT[0]+0.2,HT[1]+0.28,'người Tống theo Đại Việt, vẫn mặc áo Tống',BL)
BATT.append((at(32,'áo Tống')-0.5,at(32,'áo Tống')+4.5,HT[0],HT[1],['Quân Nguyên ở Hàm Tử','Quân Trần Nhật Duật']))
FX.append((at(32,'cung tên'),at(32,'cung tên',3.0),'drums',HT,HT))
C3(34,0.3,3.0,'Trần Quang Khải','Thượng tướng',VT)
FACEMAP['Trần Quang Khải']=('Chương Dương','general')
G('Quân Nguyên ở Chương Dương',NG,12,[(R(34,0),CD[0]-0.04,CD[1]+0.02),(E(35,0),CD[0]-0.04,CD[1]+0.02),(at(35,'sông Lô'),LS[0]-0.2,LS[1]-0.3),(E(36,0),LS[0]-0.2,LS[1]-0.3)],show=(R(34,0),E(36,0)),emb='tri',seed=2214,spread=0.6,soff=(-100,-75),label=False,defeats=[(at(34,'thua'),'flag',E(36,0))],alive=[(0,1),(at(34,'thua'),1),(at(34,'thua')+3,0.5)])
G('Quân Quang Khải, Quốc Toản',VT,10,[(R(34,0),CD[0]+0.08,CD[1]-0.06),(E(35,0),CD[0]+0.08,CD[1]-0.06)],show=(R(34,0),E(35,0)),emb='sun',seed=2215,spread=0.5,soff=(95,-60),label=False)
BATT.append((R(34,3.0),R(34,8.0),CD[0],CD[1],['Quân Nguyên ở Chương Dương','Quân Quang Khải, Quốc Toản']))
FX.append((R(34,3.0),R(34,8.0),'drums',CD,CD))
SKULL(35,2.2,3.2,TKT[0],TKT[1],'Toa Đô bị chém đầu')
FX.append((at(35,'chém đầu'),at(35,'chém đầu',1.6),'gong',TKT,TKT))
C3(36,0.3,3.0,'Toa Đô','tướng Nguyên mượn đường',NG)
FACEMAP['Toa Đô']=('Tây Kết','general')
PROPS.append((R(36,3.0),E(37,0),'seal',TKT[0],TKT[1]+0.05,'',0.55))
Q(30,35)
# ======================= CHƯƠNG 7: LẦN THỨ BA (38–47)
S2(38,41,[LS,VD,H],1.9,hmax=380)
NU(38,'năm 1287','Quân Nguyên lại kéo xuống',0.4)
show('Vân Đồn',38,47);show('Lạng Sơn',38,41);show('Bạch Đằng',45,56)
reg('NGUYÊN MÔNG',(108.2,23.4),P_NG,NG,(38,47),alpha=10)
G('Thoát Hoan đi đường bộ',NG,16,[(R(38,0),LS[0]+0.5,LS[1]+0.5),(R(38,6),LS[0],LS[1]),(R(39,0),LS[0],LS[1]),(R(40,0),VK[0]+0.2,VK[1]+0.3),(E(47,0),VK[0],VK[1]+0.05)],kind='cav',show=(R(38,0),E(47,0)),emb='tri',seed=2216,spread=0.8,soff=(30,20))
G('Hạm đội Ô Mã Nhi',NG,16,[(R(38,0),108.3,20.80),(R(38,7),VD[0]+0.3,VD[1]-0.2),(R(40,0),VD[0]-0.15,VD[1]-0.12),(R(41,0),106.70,20.90),(E(46,0),LH[0],LH[1]),(R(47,0),BDG[0],BDG[1])],kind='ship',show=(R(38,0),E(47,0)),emb='tri',seed=2217,spread=0.9,soff=(-50,-30),label=False)
G('Thuyền lương Trương Văn Hổ',BR,12,[(R(39,0),108.9,20.90),(R(39,8),VD[0]+0.5,VD[1]-0.25),(at(43,'chở lương'),VD[0]+0.15,VD[1]-0.12),(E(43,0),VD[0]+0.15,VD[1]-0.12)],kind='ship',show=(R(39,0),E(43,2)),emb='circle',seed=2218,spread=0.7,soff=(60,40),label=False,
  alive=[(0,1),(at(43,'đánh bại'),1),(at(43,'đánh bại')+2.5,0.1)],defeats=[(at(43,'đánh bại'),'flag',E(43,2))])
C3(39,2.6,3.0,'Trương Văn Hổ','chỉ huy thuyền lương',NG)
C3(39,0.2,2.2,'Trần Hưng Đạo','giao giữ biển Vân Đồn',VT)
G('Quân Trần Khánh Dư',VT,8,[(R(39,0),VD[0],VD[1]),(R(41,0),VD[0],VD[1]),(R(42,2),VD[0]-0.08,VD[1]-0.05),(at(43,'đánh bại'),VD[0]+0.1,VD[1]-0.10),(E(47,0),VD[0]+0.1,VD[1]-0.1)],kind='ship',show=(R(39,0),E(47,0)),emb='sun',seed=2219,spread=0.5,soff=(-65,15),label=False)
BATT.append((at(43,'đánh bại')-0.4,at(43,'đánh bại')+4.6,VD[0]+0.12,VD[1]-0.11,['Thuyền lương Trương Văn Hổ','Quân Trần Khánh Dư']))
FX.append((at(43,'đánh bại'),at(43,'đánh bại',3.5),'drums',VD,VD))
FX.append((at(43,'đánh bại'),at(43,'đánh bại',2.0),'splash',VD,VD))
C3(40,2.0,2.6,'Trần Khánh Dư','không chặn nổi hạm đội',VT)
LET(40,at(40,'xiềng')-R(40,0),3.6,VD,H,'giải về kinh')
NT(41,0.4,3.0,VD[0],VD[1]-0.45,'xin hoãn hai ba ngày',VT)
NT(42,0.3,3.0,VD[0],VD[1]-0.45,'hạm đội qua rồi, thuyền lương sẽ theo sau',BR)
LET(45,0.5,4.0,VD,LS,'thả tù binh về báo tin lương đã mất')
NT(44,0.3,3.2,VD[0],VD[1]+0.45,'lương thực, khí giới là chỗ dựa của quân Nguyên',NG)
show('Long Hưng',46,47)
SKULL(46,1.0,3.0,LH[0],LH[1],'mộ vua Trần Thái Tông bị đào')
FIRES.append((at(46,'đào mộ'),E(46,0),LH[0],LH[1]))
NT(47,0.3,3.4,BDG[0]+0.1,BDG[1]+0.3,'đón thuyền lương, nhưng không gặp',NG)
Q(43,43)
# ======================= CHƯƠNG 8: BẠCH ĐẰNG (48–56)
S(48,56,106.76,20.93,9.0*_W.RW/6031)
NU(48,'tháng ba năm 1288','Trận Bạch Đằng',0.6)
for _w in ((R(48,0),E(56,0)),): RIVERS.append(('SÔNG BẠCH ĐẰNG',[(106.40,21.10),(106.52,21.07),(106.63,21.01),(106.73,20.96),(106.82,20.91),(106.88,20.82),(106.93,20.72),(107.0,20.62)],7,(106.68,21.15),_w))
STK=[(106.69,20.985),(106.72,20.965),(106.745,20.955),(106.765,20.94),(106.785,20.93),(106.80,20.92),(106.815,20.905),(106.835,20.89),(106.70,20.96),(106.73,20.98),(106.76,20.955),(106.79,20.915),(106.82,20.925),(106.85,20.87)]
TIDE.append(([(106.60,21.03),(106.70,20.98),(106.80,20.92),(106.88,20.84),(106.92,20.75)],[(0,1.0),(at(49,'thủy triều lên'),1.0),(at(50,'thủy triều rút')-0.5,0.95),(at(50,'thủy triều rút')+3,0.08),(E(52,0),0.08),(E(52,0)+2,0.7)],STK,(R(48,0),R(48,5)),R(48,2.5),(R(48,0),E(56,6))))
NT(48,0.4,3.2,106.78,21.02,'cọc gỗ đầu nhọn phủ cỏ bên trên',BR)
NT(49,0.3,3.0,106.76,21.0,'thủy triều lên: cọc chìm dưới nước',BL)
AMBIENT.append((R(48,0),E(51,0),'sea',0.4))
FX.append((R(48,2.5),R(48,6.0),'crack',(106.76,20.95),(106.8,20.92)))
FX.append((at(49,'thủy triều lên'),E(49,0),'tide_up',(106.7,20.97),(106.9,20.8)))
G('Thuyền quân Nguyên',NG,16,[(R(48,0),106.97,20.71),(at(49,'đuổi theo'),106.88,20.83),(at(49,'bãi cọc')+0.5,106.76,20.95),(at(50,'vướng cọc'),106.74,20.96),(E(52,0),106.74,20.96)],show=(R(48,0),E(52,2)),emb='tri',seed=2220,kind='ship',spread=0.9,soff=(-60,30),
  alive=[(0,1),(at(50,'vướng cọc'),1),(at(52,'chết đuối'),0.55),(at(52,'chết đuối')+4,0.1)],defeats=[(E(52,-0.5),'flag',E(52,2))])
G('Thuyền nhử của Đại Việt',VT,6,[(R(48,0),106.66,21.01),(at(49,'giả vờ thua'),106.80,20.92),(at(49,'giả vờ thua')+2.5,106.88,20.84),(at(49,'đuổi theo'),106.78,20.94),(at(49,'đuổi theo')+3,106.66,21.01),(E(52,0),106.66,21.01)],show=(R(48,0),E(52,2)),emb='sun',seed=2221,kind='ship',spread=0.6,soff=(-10,-90),label=False)
G('Thuyền Đại Việt tung ra',VT,10,[(at(50,'tung ra')-1.0,106.60,21.03),(at(50,'tung ra')+2.5,106.70,20.99),(at(51,'bờ'),106.78,20.94),(E(52,0),106.80,20.93)],show=(at(50,'tung ra')-1.0,E(52,2)),emb='sun',seed=2222,kind='ship',spread=0.9,soff=(70,60),label=False)
G('Thuyền lương mắc cọc',BR,8,[(at(51,'thuyền lương')-1.5,106.98,20.70),(at(51,'thuyền lương')+2.5,106.80,20.92),(E(51,0),106.78,20.94)],kind='ship',show=(at(51,'thuyền lương')-1.5,E(52,2)),emb='circle',seed=2223,spread=0.6,soff=(60,40),label=False,alive=[(0,1),(at(51,'nghiêng đắm'),1),(at(51,'nghiêng đắm')+3,0.1)],defeats=[(at(51,'nghiêng đắm'),'flag',E(52,2))])
FIRES.append((at(51,'nghiêng đắm'),at(51,'nghiêng đắm',4.0),106.78,20.94))
BATT.append((at(50,'tung ra'),E(51,0),106.76,20.95,['Thuyền quân Nguyên','Thuyền Đại Việt tung ra']))
FX.append((at(50,'tung ra'),E(51,0),'drums',(106.7,20.97),(106.8,20.92)))
NUMS.append((at(52,'bốn trăm')-0.2,'Bốn trăm','chiếc thuyền của quân Nguyên bị mất',0.2))
C3(52,3.4,2.8,'Ô Mã Nhi','bị bắt sống',NG)
C3(52,0.3,2.8,'Thoát Hoan','trốn về Tư Minh',NG)
show('Tư Minh',52,52)
G('Thoát Hoan chạy',NG,6,[(at(52,'trốn'),BDG[0],BDG[1]),(E(52,0)+3,LS[0]+0.4,LS[1]+0.6)],kind='cav',show=(at(52,'trốn'),E(52,0)+3),emb='tri',seed=2224,spread=0.4,soff=(30,20),label=False)
C3(53,0.3,3.0,'Trần Thánh Tông','mời các tướng bị bắt',VT)
PROPS.append((R(53,1.0),E(53,0),'meeting',BDG[0]-0.05,BDG[1]-0.08,'',0.5))
NT(54,0.3,3.6,106.62,21.12,'Ngô Quyền dùng cọc và thủy triều ở đây năm 938',BR)
C3(56,0.3,3.0,'Trần Nhân Tông','làm thơ báo thắng trận',VT)
FACEMAP['Trần Nhân Tông']=('Long Hưng','king');FACEMAP['Trần Thánh Tông']=('Long Hưng','king');FACEMAP['Trần Thái Tông']=('Thăng Long','king')
PROPS.append((R(55,0.4),E(55,0),'tomb',LH[0],LH[1],'',0.7))
show('Long Hưng',55,56)
Q(49,52)
# ======================= CHƯƠNG 9: HAI NGƯỜI BỊ GẠT RA (57–65)
S2(57,65,[H,VD,BT,LS],2.0,hmax=380)
show('Thăng Long',57,65);show('Vân Đồn',60,65);show('Bình Than',62,65)
reg('ĐẠI VIỆT',(105.7,21.7),P_DV,VT,(57,65),alpha=15)
NT(57,0.5,3.2,H[0],H[1]+0.4,'cung điện bị giặc đốt hết',BR)
FIRES.append((R(57,0.3),R(57,3.6),H[0],H[1]))
NU(59,'năm 1294','Hốt Tất Liệt qua đời',0.4)
G('Quân Nguyên đóng ở biên giới',NG,12,[(R(58,0),LS[0]+0.2,LS[1]+0.25),(at(59,'rút quân'),LS[0]+0.2,LS[1]+0.25),(E(59,0)+2.5,LS[0]+1.2,LS[1]+1.2)],kind='cav',show=(R(58,0),E(59,0)+2.5),emb='tri',seed=2225,spread=0.6,soff=(40,10),label=False)
PROPS.append((R(60,0.4),R(60,3.4),'ping',VD[0],VD[1],'g',0.9))
PROPS.append((R(60,3.6),R(60,6.6),'ping',BDG[0],BDG[1],'g',0.9))
NT(61,0.3,3.2,VD[0]-0.2,VD[1]+0.35,'cả hai lần, thuyền lương rơi vào tay Đại Việt',BR)
FACE(62,0.3,3.0,'Trần Quốc Toản','Bình Than','youth',VT)
FACE(63,0.3,3.0,'Trần Khánh Dư','Vân Đồn','general',VT)
INTER_END=True


INTER=[]
INTER.append((T[BASE+61]+0.2,min(T[BASE+61]+D[BASE+61]-0.3,T[BASE+61]+0.2+5.0),'timeline',{'head':'Hai lần cuối thua vì thuyền lương','nodes':[
 ('1285','Vườn không nhà trống: giặc đi sâu, thiếu ăn'),
 ('1287','Thuyền lương bị đánh ở Vân Đồn'),
 ('1288','Thuyền lương mắc cọc ở Bạch Đằng')]}))
GRADE={'sat':0.62,'tint':(188,212,232),'amt':0.8,'gain':0.97,'vig':0.6}
SCN.sort(key=lambda x:x[0])
CAM=[(0,SCN[0][2],SCN[0][3],SCN[0][4])]
for (a_,b_,lo,la,z) in SCN:
    CAM.append((R(a_)+1.6,lo,la,z));CAM.append((E(b_)-0.2,lo+0.01,la,z*1.03))
CAM=sorted(CAM,key=lambda k:k[0])
def CLOSE(t0,t1,lo,la,z,push=1.08):
    global CAM
    CAM=[k for k in CAM if not (t0-1.8<=k[0]<=t1+1.2)]
    CAM+= [(t0,lo,la,z),(t1,lo+0.001,la,z*push)]
    CAM=sorted(CAM,key=lambda k:k[0])
NIGHT.append((TOTAL,0));NIGHT=sorted(NIGHT,key=lambda k:k[0])
MINI=[(0,TOTAL)]
QUIET_AUDIO=True
CAMFOCUS=True
FOC=[(48,56,[(106.55,21.05),(107.00,20.70)],True)]
MUSIC=[]
def gate_open(t): return 0
def year_of(n):
    m=n-BASE
    for a,b,y in [(5,11,1257),(12,18,1282),(19,22,1284),(23,37,1285),(38,47,1287),(48,56,1288),(57,58,1288),(59,65,1294)]:
        if a<=m<=b: return y
    return None
NO_GROUP_LABEL=True
SIDES=[('Đại Việt',VT,{g['name'].strip() for g in GROUPS if g['col']==VT}),('Quân Nguyên',NG,{g['name'].strip() for g in GROUPS if g['col']==NG}),
       ('Thuyền lương',BR,{g['name'].strip() for g in GROUPS if g['col']==BR}),('Thuyền chở than',NEU,{g['name'].strip() for g in GROUPS if g['col']==NEU})]
SFX=[(at(5,'đánh vào'),'horn'),(at(22,'hô đánh'),'trumpet'),(at(26,'thét'),'gong'),(at(35,'chém đầu'),'gong'),(R(38,0.3),'horn'),(at(43,'đánh bại'),'trumpet'),(at(52,'bắt sống'),'gong')]
SFX_GROUPS=['Quân Mông Cổ','Quân Ô Mã Nhi','Đạo Thoát Hoan','Thoát Hoan đi đường bộ','Hạm đội Ô Mã Nhi','Quân Nguyên đóng ở biên giới','Thoát Hoan chạy','Thuyền lương Trương Văn Hổ','Thuyền lương mắc cọc','Thuyền quân Nguyên','Quân Toa Đô']
AMBIENT.extend([(R(1,0),E(4,0),'wind',0.3),(R(5,0),E(11,0),'forest',0.3),(R(12,0),E(18,0),'crowd',0.25),(R(19,0),E(22,0),'crowd',0.25),(R(23,0),E(29,0),'wind',0.3),
 (R(30,0),E(37,0),'crowd',0.25),(R(38,0),E(47,0),'sea',0.4),(R(57,0),TOTAL-1,'wind',0.3)])
_s0=at(41,'xin hoãn')
FX.append((at(53,'rượu'),at(53,'rượu',1.5),'splash',BDG,BDG))
PROPS.append((R(48,2.5),E(49,-0.1),'stakes',106.76,20.95,'',0.8))
