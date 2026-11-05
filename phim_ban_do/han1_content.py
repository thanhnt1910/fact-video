"""Cách họ cai trị, tập 1: Chín quận (Tây Hán, năm 110 TCN). n = 41001–41013 (BASE=41000, không đổi chỉ số).
Bản đồ world7. Vị trí các quận chỉ là MINH HỌA gần đúng (Toàn thư không kê tên chín quận; chỉ gọi tên Giao Chỉ, Cửu Chân, Châu Nhai, Đạm Nhĩ).
Chấm quận không có nhãn tên trừ Giao Chỉ và Cửu Chân. Không đường biên. Không có giao tranh nên không dùng Q().
Khung đùa: không có (tập này về dân khổ, không đùa). Nguồn: ke-hoach/chinh-sach-tap-1-kich-ban.md."""
from build2 import T,D,TOTAL,chap,PH
import build2 as _B
import world7 as _W
BASE=41000
_B.ERA='trước Công nguyên'
def _nx(n):
    while BASE+n not in T and n<60: n+=1
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
GR=(52,142,86);BL=(54,96,176);RD=(190,52,42);PU=(138,52,112);DK=(46,38,58);GD=(205,160,40);BR=(150,100,60);GY=(110,110,110);NEU=(150,140,120)
HAN=RD;VT=GR
# Vị trí minh họa chín quận
Q9=[('Nam Hải',(113.26,23.13)),('Thương Ngô',(111.30,23.45)),('Uất Lâm',(109.60,23.10)),('Hợp Phố',(109.20,21.70)),('Giao Chỉ',(106.00,21.10)),
    ('Cửu Chân',(105.80,19.80)),('Nhật Nam',(106.60,18.20)),('Châu Nhai',(110.30,19.90)),('Đạm Nhĩ',(109.60,19.30))]
LOC={'Long Biên':(106.05,21.12,'big'),'Kinh đô nhà Hán':(110.80,24.70,'mid'),'Giao Chỉ':(106.00,21.10,'mid'),'Cửu Chân':(105.80,19.80,'mid')}
for nm,(lo,la) in Q9:
    if nm not in LOC: LOC[nm]=(lo,la,'town')
CITIES=dict(LOC)
CITY_SHOW={};CITY_OWN={}
def show(name,a,b): CITY_SHOW.setdefault(name,[]).append((R(a,-1),E(b,1)))
def show_t(name,t0,t1): CITY_SHOW.setdefault(name,[]).append((t0,t1))
def own(name,col0,*steps):
    seq=[(0,col0)]
    for (t,c) in steps: seq.append((t,seq[-1][1]));seq.append((t+2.0,c))
    CITY_OWN[name]=seq
GROUPS=[];BATT=[];FIRES=[];FX=[];OBJ=[];LETTERS=[];ARROWS=[];NOTES=[];MARKS=[];FACES=[];CARDS3=[];QUOTES=[];JOKES=[];METERS=[];NUMS=[];TITLES=[];TABLES=[]
REGIONS=[];RIVERS=[];ROUTES=[];TIDE=[];AMBIENT=[];PROPS=[];QUIET=[]
WATER=[('VỊNH BẮC BỘ',(107.3,19.5),26)]
NIGHT=[(0,0)]
def G(name,col,n,keys,show=None,**kw): GROUPS.append(dict(name=name,col=col,n=n,keys=keys,show=show or (keys[0][0]-0.3,keys[-1][0]+3),**kw))
def NT(n,o,dur,lo,la,txt,col=DK): NOTES.append((R(n,o),min(R(n,o+min(dur,3.5)),E(n,-0.1)),lo,la,txt,col))
def C3(n,o,dur,name,role,col): CARDS3.append((R(n,o),min(R(n,o+dur),E(n,-0.2)),name,role,col))
def NU(n,big,small,delay=1.2): NUMS.append((BASE+_nx(n),big,small,delay))
def AR(n,o,dur,a,b,col,txt): ARROWS.append((R(n,o),min(R(n,o+dur),E(n,-0.1)),X(a),X(b),col,txt))
def LET(n,o,dur,a,b,txt): LETTERS.append((R(n,o),R(n,o+dur),X(a),X(b),txt))
def X(name): return LOC[name][:2]
def FACE(n,o,dur,name,loc,kind,col,dx=0,dy=0):
    s=R(n,o);FACES.append((s,min(max(R(n,o+dur),s+2.2),E(n,-0.1)))+X(loc)+(name,kind,col,dx,dy))
SCN=[]
def S2(a,b,pts,zmax=8.0,zmin=0.9,hmax=440):
    px=lambda z:1920*z*_W.KX/_W.RW;py=lambda z:1920*z*_W.S/_W.RW
    los=[p_[0] for p_ in pts];las=[p_[1] for p_ in pts]
    dlo=max(los)-min(los);dla=max(las)-min(las);z=zmax
    if dlo>0: z=min(z,1200/(dlo*px(1)))
    if dla>0: z=min(z,hmax/(dla*py(1)))
    z=max(zmin,z)
    cx=(max(los)+min(los))/2+(960-775)/px(z);cy=max(las)-(432-330)/py(z)
    if dla==0: cy=las[0]-(432-470)/py(z)
    SCN.append((a,b,cx,cy,z))
def reg(name,lab,poly,c0,win,alpha=34):
    REGIONS.append(dict(name=name,lab=lab,poly=poly,own=[(0,c0)],alpha=alpha,win=(R(win[0],-1),E(win[1],1))))
ALL=[p for _,p in Q9]
# ---------- Phần 0: Bạn có biết (41001): cả vùng, chín chấm hiện lần lượt
TITLES.append((0.3,3.2,'CÁCH HỌ CAI TRỊ','CHÍN QUẬN','Tập 1'))
S2(1,2,ALL,2.4,hmax=380)
for i,(nm,_) in enumerate(Q9):
    show_t(nm,R(1,0.6+0.35*i),TOTAL)
    own(nm,HAN)
NU(1,'9','quận',1.0)
# ---------- Phần 1: Ban hành (41002–41003)
NU(2,'110 TCN','Nhà Hán lập chín quận',0.4)
C3(3,0.3,3.0,'Thạch Đái','quan nhà Hán đứng đầu',HAN)
FACE(3,0.3,3.0,'Thạch Đái','Long Biên','noble',HAN)
LET(3,2.5,2.8,'Kinh đô nhà Hán','Long Biên','Lệnh bổ nhiệm từ kinh đô nhà Hán')
S2(3,3,[X('Kinh đô nhà Hán'),X('Long Biên')],2.0,hmax=380)
NT(2,0.4,3.0,106.0,22.0,'Các điểm là minh họa, không phải biên giới',DK)
# ---------- Phần 2: Cách thực hiện (41004–41006)
S2(4,5,ALL,2.4,hmax=380)
reg('GIAO CHÂU',(108.4,22.3),[(105.0,18.6),(107.2,18.6),(110.4,21.0),(110.4,23.9),(105.0,22.9)],HAN,(4,5),alpha=26)
NT(4,0.6,3.0,108.3,24.2,'Châu đứng trên, trông coi các quận',HAN)
NT(5,0.3,3.0,106.0,22.1,'Đất của ta: Giao Chỉ, Cửu Chân',VT)
own('Giao Chỉ',VT);own('Cửu Chân',VT)
S2(6,6,[X('Long Biên'),X('Cửu Chân'),X('Giao Chỉ')],5.0,hmax=360)
show('Long Biên',5,6)
AR(5,1.5,3.0,'Long Biên','Cửu Chân',HAN,'')
AR(6,0.6,3.0,'Long Biên','Giao Chỉ',HAN,'')
G('Người đưa lệnh',HAN,3,[(R(6,0.3),106.05,21.12),(E(6,0),105.85,19.95)],kind='cav',show=(R(6,0.2),E(6,0.5)),emb='circle',seed=4106,spread=0.3,label=False)
# ---------- Phần 3: Kết quả, dân khổ (41007–41011)
S2(7,8,[X('Long Biên'),X('Kinh đô nhà Hán')],1.8,hmax=380)
NU(7,'gần 300 năm','Quan nhà Hán thay nhau cai quản',0.5)
NT(7,1.5,3.2,106.2,22.2,'Ngọc trai, đồi mồi, hương, gỗ quý bị vơ vét',HAN)
AR(7,3.0,5.0,'Long Biên','Kinh đô nhà Hán',HAN,'của cải đưa về kinh đô')
LET(8,0.5,3.4,'Long Biên','Kinh đô nhà Hán','Dân kêu: kinh đô quá xa')
S2(9,9,[X('Giao Chỉ'),X('Cửu Chân'),X('Long Biên')],5.0,hmax=360)
NT(9,0.5,3.0,105.7,21.6,'Dân tụ họp chống đối',VT)
G('Dân tụ họp',VT,10,[(R(9,0.2),105.95,20.40),(R(9,2.5),106.00,21.00),(E(9,0),106.02,21.08)],show=(R(9,0.1),E(9,1.0)),emb='circle',seed=4109,spread=0.8,label=False)
S2(10,11,[X('Long Biên'),X('Kinh đô nhà Hán'),X('Cửu Chân')],2.0,hmax=380)
C3(10,0.3,3.2,'Giả Tông','quan được chọn lại',HAN)
FACE(10,0.3,3.2,'Giả Tông','Long Biên','noble',HAN)
NT(10,3.3,3.2,106.2,22.2,'Tha bớt thuế, chọn người tốt giữ các quận huyện',GD)
own('Giao Chỉ',VT);own('Cửu Chân',VT)
NT(11,0.4,3.0,106.2,22.0,'Trăm họ được yên',GD)
# ---------- Phần 4: Kết (41012–41013)
S2(12,13,ALL,2.4,hmax=380)
NU(13,'Một người quan','đổi cả vùng đổi theo',0.8)
GRADE={'sat':0.8,'tint':(225,205,170),'amt':0.35,'gain':0.99,'vig':0.5}
INTER=[]
INTER=[x for x in INTER if x]
# ---------- Hoàn tất
SCN.sort(key=lambda x:x[0])
CAM=[(0,SCN[0][2],SCN[0][3],SCN[0][4])]
for (a_,b_,lo,la,z) in SCN:
    CAM.append((R(a_)+1.6,lo,la,z));CAM.append((E(b_)-0.2,lo+0.01,la,z*1.03))
CAM=sorted(CAM,key=lambda k:k[0])
NIGHT.append((TOTAL,0));NIGHT=sorted(NIGHT,key=lambda k:k[0])
MINI=[(0,TOTAL)]
QUIET_AUDIO=True
MUSIC=[(0,R(2,0),'mo',1.0),(R(2,0),R(7,0),'cang',0.9),(R(7,0),R(10,0),'bi',1.0),(R(10,0),R(12,0),'trang',1.0),(R(12,0),TOTAL,'binh',0.9)]
def gate_open(t): return 0
def year_of(n):
    n-=BASE
    if 2<=n<=6: return 110
    return None
NO_GROUP_LABEL=True
SIDES=None
SFX=[(R(3,0.4),'gong'),(R(9,0.5),'horn')]
SFX_GROUPS=['Người đưa lệnh']
