"""Demo Nguyên Mông: trận Bạch Đằng 1288 (thuyền, thủy triều, cọc). Số câu 1–16."""
from build2 import T,D,TOTAL,chap,PH
INF=1e9
BASE=4000
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
LOC={'Thăng Long':(105.85,21.03,'big'),'Vạn Kiếp':(106.40,21.10,'mid'),'Lạng Sơn':(106.76,21.85,'mid'),'Bạch Đằng':(106.88,20.84,'town')}
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
REGIONS=[];RIVERS=[];ROUTES=[]
WATER=[('VỊNH BẮC BỘ',(108.4,20.3),26),('SÔNG HỒNG',(104.9,21.35),22)]
NIGHT=[(0,0)]
def nt(n,o0,o1): NIGHT.extend([(R(n,o0),0),(R(n,o0+1.6),0.6),(R(n,o1),0.6),(R(n,o1+1.6),0)])
def G(name,col,n,keys,show=None,**kw):
    GROUPS.append(dict(name=name,col=col,n=n,keys=keys,show=show or (keys[0][0]-0.3,keys[-1][0]+3),**kw))
def NT(n,o,dur,lo,la,txt,col=DK): NOTES.append((R(n,o),R(n,o+dur),lo,la,txt,col))
def C3(n,o,dur,name,role,col): CARDS3.append((R(n,o),min(R(n,o+dur),E(n,-0.2)),name,role,col))
def Q(n,sub,text,who,col,dur=None):
    t0=at(n,sub);QUOTES.append((t0,min(E(n,-0.1),t0+(dur or 6.0)),text,who,col))
def J(n,icon,text,off=1.2): JOKES.append((R(n,off),E(n,-0.1),icon,text))
def NU(n,big,small,delay=1.2): NUMS.append((BASE+n,big,small,delay))
def SKULL(n,o,dur,lo,la,txt): MARKS.append((R(n,o),R(n,o+dur),lo,la,'skull',txt))
def AR(n,o,dur,a,b,col,txt): ARROWS.append((R(n,o),R(n,o+dur),a,b,col,txt))
def LET(n,o,dur,a,b,txt): LETTERS.append((R(n,o),R(n,o+dur),a,b,txt))
def X(name): return LOC[name][:2]
SCN=[]
def S(a,b,lo,la,z): SCN.append((a,b,lo,la,z))
def reg(name,lab,poly,c0,win,steps=(),alpha=34):
    seq=[(0,c0)]
    for (t,c) in steps: seq+=[(t,seq[-1][1]),(t+3,c)]
    REGIONS.append(dict(name=name,lab=lab,poly=poly,own=seq,alpha=alpha,win=(R(win[0],-1),E(win[1],1))))


# nhân vật: Nguyên đỏ, Đại Việt xanh lá
def X(name): return LOC[name][:2]
SCN=[]
def S(a,b,lo,la,z): SCN.append((a,b,lo,la,z))
def reg(name,lab,poly,c0,win,steps=(),alpha=34):
    seq=[(0,c0)]
    for (t,c) in steps: seq+=[(t,seq[-1][1]),(t+3,c)]
    REGIONS.append(dict(name=name,lab=lab,poly=poly,own=seq,alpha=alpha,win=(R(win[0],-1),E(win[1],1))))
def NU(n,big,small,delay=1.2): NUMS.append((BASE+n,big,small,delay))
def J(n,icon,text,off=1.2): JOKES.append((R(n,off),E(n,-0.1),icon,text))
def NT(n,o,dur,lo,la,txt,col=DK): NOTES.append((R(n,o),R(n,o+dur),lo,la,txt,col))
def C3(n,o,dur,name,role,col): CARDS3.append((R(n,o),min(R(n,o+dur),E(n,-0.2)),name,role,col))
def AR(n,o,dur,a,b,col,txt): ARROWS.append((R(n,o),R(n,o+dur),a,b,col,txt))
P_DV=[(103.5,22.7),(104.2,23.1),(106.5,23.2),(107.8,22.0),(107.4,20.9),(106.5,19.95),(105.0,19.9),(103.8,21.0),(103.4,22.0)]
NG=RD;VT=GR
TIDE=[]
# ---------------- máy quay
S(1,2,106.2,21.35,3.4);S(3,4,106.4,21.2,4.6);S(5,6,106.58,21.5,4.0);S(7,9,106.68,20.97,6.8);S(10,15,106.72,20.95,7.0);S(16,16,105.9,21.4,2.2)
TITLES.append((0.3,5.2,'NGUYÊN MÔNG · DEMO','TRẬN BẠCH ĐẰNG','năm 1288'))
for nm in LOC: show(nm,1,16)
OW('Thăng Long',VT);OW('Vạn Kiếp',NEU,(1,0,NG),(16,0,NEU)) if False else None
reg('ĐẠI VIỆT',(105.3,22.6),P_DV,VT,(1,16),alpha=24)
RIVERS.append(('SÔNG BẠCH ĐẰNG',[(106.40,21.10),(106.52,21.07),(106.63,21.01),(106.73,20.96),(106.82,20.91),(106.88,20.82),(106.93,20.72),(107.0,20.62)],7,(106.68,21.15)))
# ---------------- quân bộ của Thoát Hoan
G('Quân Thoát Hoan',NG,16,[(0,105.85,21.03),(R(1,3),106.40,21.10),(R(5,0),106.40,21.10),(R(5,8),106.55,21.45),(R(6,3),106.76,21.85),(R(6,9),106.95,22.15)],show=(0,R(7,3)),emb='tri',seed=411,kind='cav',soff=(-90,-20),alive=[(0,1),(R(6,2),1),(R(6,8),0.15)])
G('Quân Đại Việt phục kích',VT,12,[(0,106.70,21.70)],show=(R(5,2),R(6,11)),emb='sun',seed=412,soff=(110,30))
C3(2,0.4,3.4,'Thoát Hoan','chỉ huy quân Nguyên',NG)
AR(2,1.2,4.5,X('Vạn Kiếp'),X('Lạng Sơn'),NG,'đường bộ')
AR(2,2.2,4.5,X('Vạn Kiếp'),(106.98,20.68),NG,'đường thủy')
METERS.append((R(1,0.8),E(2,-0.2),'LƯƠNG THỰC',[('Nguyên',NG,[(R(1,0),0.30),(R(2,0),0.05)])]))
NT(1,0.2,3.6,106.40,21.25,'quân Nguyên đói, rút về Vạn Kiếp',NG)
C3(3,0.4,3.4,'Trần Quốc Tuấn','chỉ huy quân Đại Việt',VT)
NT(4,0.2,2.8,106.58,21.35,'chọn đúng đường, rồi chờ',VT)
NT(5,0.6,3.0,106.52,21.32,'phá cầu, chặt cây, đặt bẫy',VT)
J(5,'scroll','Đường về nhà: bản đi vòng',2.4)
BATT.append((R(6,1.2),R(6,5.2),106.76,21.82,['Quân Thoát Hoan','Quân Đại Việt phục kích']))
NT(6,0.2,2.6,106.76,22.0,'Thoát Hoan trúng tên độc',NG)
# ---------------- thủy quân và cọc
G('Hạm đội Ô Mã Nhi',NG,8,[(R(7,0),106.45,21.10),(R(7,9),106.60,21.03),(R(10,0),106.64,21.01),(R(10,8),106.78,20.93)],show=(R(7,0),E(15,0)),emb='tri',seed=421,kind='ship',spread=0.9,soff=(-70,-45),alive=[(0,1),(R(13,1),1),(R(13,9),0.2)],defeats=[(R(13,5),'flag',E(15,0))])
G('Thuyền Đại Việt',VT,6,[(R(10,0),106.86,20.88),(R(10,2),106.86,20.88),(R(10,5),106.73,20.97),(R(10,9),106.86,20.88),(R(13,0),106.86,20.88),(R(13,4),106.80,20.93)],show=(R(10,0),E(15,0)),emb='sun',seed=422,kind='ship',spread=0.7,soff=(80,75))
C3(7,0.4,3.2,'Ô Mã Nhi','tướng thủy quân Nguyên',NG)
NT(7,1.0,4.0,106.55,21.13,'thủy quân rút xuôi sông',NG)
STK=[(106.69,20.985),(106.72,20.965),(106.745,20.955),(106.765,20.94),(106.785,20.93),(106.80,20.92),(106.815,20.905),(106.835,20.89),(106.70,20.96),(106.73,20.98),(106.76,20.955),(106.79,20.915),(106.82,20.925),(106.85,20.87)]
TIDE.append(([(106.60,21.03),(106.70,20.98),(106.80,20.92),(106.88,20.84),(106.92,20.75)],[(0,1.0),(R(10,6),1.0),(R(11,0),0.95),(R(12,3),0.08),(R(14,2),0.08),(R(15,2),0.7)],STK,(R(9,0),E(14,0)),R(8,0.5)))
NT(8,0.6,3.2,106.76,21.02,'cọc gỗ đầu bịt sắt',BR)
NT(8,4.0,3.5,106.76,21.02,'nước lên: cọc chìm dưới nước',BL)
NU(10,'9/4/1288','Trận Bạch Đằng',0.5)
NT(10,2.6,3.0,106.62,20.90,'thuyền nhỏ giả vờ rút',VT)
NT(11,0.2,2.0,106.80,20.99,'nước bắt đầu xuống',BL)
NT(12,0.6,4.0,106.80,20.97,'thuyền lớn mắc cọc',NG)
J(12,'coin','Thủy triều: đúng giờ, không nhận lương',3.0)
BATT.append((R(13,0.8),R(13,6.0),106.79,20.93,['Hạm đội Ô Mã Nhi','Thuyền Đại Việt']))
OBJ.append((R(13,2.0),R(13,7.0),'fireboat',(106.74,20.955),(106.83,20.90)))
NT(13,5.4,3.2,106.82,20.86,'Ô Mã Nhi bị bắt',NG)
NU(14,'năm 938','Ngô Quyền cũng dùng cọc và thủy triều',1.4)
NT(15,0.4,3.5,106.80,20.97,'hạm đội Nguyên coi như mất',NG)
NU(16,'1258 · 1285 · 1288','ba lần, không lần nào đổ',1.0)
TITLES.append((R(16,3.2),E(16,0.5),'HẾT DEMO','BẠCH ĐẰNG','Cọc gỗ, thủy triều và bữa tối của quân Nguyên'))
# ======================= HOÀN TẤT
SCN.sort(key=lambda x:x[0])
CAM=[(0,SCN[0][2],SCN[0][3],SCN[0][4])]
for (a_,b_,lo,la,z) in SCN:
    CAM.append((R(a_)+1.6,lo,la,z));CAM.append((E(b_)-0.2,lo+0.01,la,z*1.03))
CAM=sorted(CAM,key=lambda k:k[0])
NIGHT.append((TOTAL,0));NIGHT=sorted(NIGHT,key=lambda k:k[0])
MINI=[(0,TOTAL)]
def gate_open(t): return 0
def year_of(n): return 1288
