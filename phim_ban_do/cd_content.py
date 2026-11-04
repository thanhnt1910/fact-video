"""Demo bản đồ Chu Du (208–210): icon nhân vật kèm quân, thuyền lửa, mũi tên, thư, bản đồ vector vùng Kinh – Dương. Câu 9001–9012."""
from build2 import T,D,TOTAL,chap,PH
INF=1e9
BASE=9000
def R(n,o=0): return T[BASE+n]+o
def E(n,o=0): return T[BASE+n]+D[BASE+n]+o
BL=(46,100,180);DK=(46,38,58);OR=(214,110,30);WH=(236,236,230);GD=(205,160,40);RD=(190,52,42)
FACE={'Chu Du':'zy','Hoàng Cái':'hg','Tào Nhân':'trn','Tôn Quyền':'sq','Trình Phổ':'tp'}
LOC={'Hạ Khẩu':(114.3,30.55,'mid'),'Xích Bích':(113.65,29.72,'mid'),'Giang Lăng':(112.2,30.35,'big'),'Ba Khâu':(113.1,29.37,'town'),'Kiến Nghiệp':(118.8,32.05,'big'),'Sài Tang':(116.0,29.72,'town'),'Tương Dương':(112.15,32.05,'mid')}
CITIES=dict(LOC)
CITY_SHOW={}
def show(name,a,b): CITY_SHOW.setdefault(name,[]).append((R(a,-1),E(b,1)))
CITY_OWN={}
def OW(name,col0,*steps):
    seq=[(0,col0)]
    for (n,o,c) in steps:
        seq.append((R(n,o),seq[-1][1]));seq.append((R(n,o+2.0),c))
    CITY_OWN[name]=seq
GROUPS=[];BATT=[];FIRES=[];FX=[];OBJ=[];LETTERS=[];ARROWS=[];NOTES=[];MARKS=[];CARDS3=[];QUOTES=[];JOKES=[];METERS=[];NUMS=[];TITLES=[]
REGIONS=[];RIVERS=[];ROUTES=[]
WATER=[('TRƯỜNG GIANG',(113.0,30.12),26),('HỒ ĐỘNG ĐÌNH',(112.9,28.95),22),('HÁN THỦY',(113.4,31.0),18)]
NIGHT=[(0,0)]
def nt(n,o0,o1): NIGHT.extend([(R(n,o0),0),(R(n,o0+1.6),0.6),(R(n,o1),0.6),(R(n,o1+1.6),0)])
def G(name,col,n,keys,show=None,**kw): GROUPS.append(dict(name=name,col=col,n=n,keys=keys,show=show or (keys[0][0]-0.3,keys[-1][0]+3),**kw))
def NT(n,o,dur,lo,la,txt,col=DK): NOTES.append((R(n,o),R(n,o+dur),lo,la,txt,col))
def C3(n,o,dur,name,role,col): CARDS3.append((R(n,o),min(R(n,o+dur),E(n,-0.2)),name,role,col))
def NU(n,big,small,delay=1.2): NUMS.append((BASE+n,big,small,delay))
def AR(n,o,dur,a,b,col,txt): ARROWS.append((R(n,o),R(n,o+dur),a,b,col,txt))
def LET(n,o,dur,a,b,txt): LETTERS.append((R(n,o),R(n,o+dur),a,b,txt))
def X(name): return LOC[name][:2]
SCN=[]
def S(a,b,lo,la,z): SCN.append((a,b,lo,la,z))
# ---- camera
S(1,5,113.55,29.85,2.7);S(6,8,112.4,30.3,4.2);S(9,9,115.4,31.0,1.7);S(10,10,112.7,29.9,3.3);S(11,12,118.3,32.1,2.3)
TITLES.append((0.3,4.6,'CHU DU · DEMO BẢN ĐỒ','XÍCH BÍCH ĐẾN BA KHÂU','năm 208 đến năm 210'))
show('Xích Bích',1,5);show('Giang Lăng',5,10);show('Ba Khâu',10,10);show('Kiến Nghiệp',9,12)
OW('Giang Lăng',DK,(8,2,BL));OW('Kiến Nghiệp',BL)
# ---- Xích Bích
G('Quân Tào',DK,34,[(0,113.78,29.98)],show=(R(1,-1),R(5,3)),emb='tri',seed=801,soff=(40,-50),alive=[(0,1),(R(4,0),1),(R(4,7),0.3)],label=False)
G('Quân Ngô',BL,24,[(0,113.45,29.58)],show=(R(1,-1),R(6,-0.5)),emb='sun',seed=802,soff=(-150,40),label=False)
G('Chu Du',BL,1,[(0,113.62,29.64)],show=(R(1,-1),R(6,-0.5)),emb='face_zy',seed=803,soff=(30,110))
G('Hoàng Cái',OR,1,[(R(3,0),113.58,29.66),(R(3,6),113.75,29.95)],show=(R(1,6),R(4,2)),emb='face_hg',seed=805,soff=(-90,-100))
G('Thuyền lửa',OR,10,[(R(3,0),113.58,29.66),(R(3,6),113.75,29.95)],show=(R(2,0),R(4,2)),emb='circle',seed=804,soff=(60,-10),label=False)
C3(1,2.6,3.4,'Chu Du','chỉ huy quân Ngô',BL)
C3(2,0.4,3.0,'Hoàng Cái','tướng Ngô, nghĩ ra kế đánh lửa',OR)
NT(3,0.4,3.2,114.0,29.45,'gió đông nam nổi gấp',DK)
FX.append((R(2,3.0),R(4,3.5),'wind',(114.3,29.3),(113.1,30.4)))
FX.append((R(3,3.2),R(3,6.5),'firearrows',(113.58,29.66),(113.78,29.97)))
FIRES.extend([(R(3,5.5),R(5,5),113.8,29.97),(R(3,6.0),R(5,5),113.74,30.0),(R(3,6.4),R(5,5),113.85,29.93),(R(4,0.2),R(5,5),113.7,29.94),(R(4,0.6),R(5,5),113.84,30.0)])
BATT.append((R(3,5.5),R(4,5),113.78,29.97,['Thuyền lửa Hoàng Cái','Quân Tào']))
NU(1,'208','trận Xích Bích',0.5)
AR(5,0.6,3.4,(113.8,29.97),(112.2,30.35),DK,'')
G('Trình Phổ',BL,1,[(R(6,0),113.5,29.6),(R(6,6),112.4,30.05),(R(8,0),112.4,30.05)],show=(R(6,0),R(8,5)),emb='face_tp',seed=815,soff=(-190,-40))
# ---- Nam Quận
G('Quân Ngô ',BL,24,[(R(6,0),113.45,29.58),(R(6,6),112.5,30.15)],show=(R(6,0),R(8,5)),emb='sun',seed=811,soff=(-150,50),label=False)
G('Chu Du ',BL,1,[(R(6,0),113.62,29.64),(R(6,6),112.5,30.1),(R(8,0),112.5,30.1)],show=(R(6,0),R(8,5)),emb='face_zy',seed=812,soff=(40,110),label=True)
G('Quân Tào ',DK,20,[(0,112.2,30.38),(R(8,3),112.2,30.38),(R(8,8),112.15,32.0)],show=(R(5,3),R(8,10)),emb='tri',seed=813,soff=(40,-60),label=False)
G('Tào Nhân',DK,1,[(0,112.2,30.38),(R(8,3),112.2,30.38),(R(8,8),112.15,32.0)],show=(R(5,3),R(8,10)),emb='face_trn',seed=814,soff=(-110,-30))
C3(6,3.0,3.4,'Tào Nhân','giữ Nam Quận',DK)
FX.append((R(7,0.8),R(7,2.2),'arrow1',(112.2,30.42,0,-20),(112.5,30.1,40,110)))
AR(8,5.5,3.0,(112.2,30.4),(112.15,32.0),DK,'')
# ---- Kế hoạch cuối
NU(9,'210','kế hoạch lấy đất Thục',0.8)
LET(9,1.0,4.0,X('Giang Lăng'),X('Kiến Nghiệp'),'xin đi lấy đất Thục')
LET(9,4.5,3.0,X('Kiến Nghiệp'),X('Giang Lăng'),'Tôn Quyền đồng ý')
G('Tôn Quyền',BL,1,[(0,118.8,32.05)],show=(R(9,0),R(12,0)),emb='face_sq',seed=821,soff=(70,60))
C3(9,0.3,3.0,'Tôn Quyền','chủ nước Ngô',BL)
G('Chu Du  ',BL,1,[(R(9,0),112.5,30.1),(R(9,8),112.2,30.35),(R(10,0),112.2,30.35),(R(10,7),113.1,29.4)],show=(R(9,0),R(10,9)),emb='face_zy',seed=831,soff=(0,110))
NT(10,4.0,3.5,113.35,29.1,'mất ở Ba Khâu, ba mươi sáu tuổi',DK)
nt(10,3.5,8.0)
# ---- Tang lễ
G('Tôn Quyền áo tang',WH,1,[(R(12,0),118.8,32.05)],show=(R(12,0),E(12,3)),emb='face_sqt',seed=822,soff=(70,60))
C3(12,0.4,3.2,'Tôn Quyền','mặc áo tang trắng, đến khóc',WH)
TITLES.append((R(12,4.5),E(12,0.5),'HẾT DEMO','CHU DU, NĂM 210','mất ở tuổi ba mươi sáu'))
CAM=[(0,113.6,29.85,2.7),
 (R(1,3),113.6,29.8,2.9),(R(2,0.5),113.55,29.78,4.2),(E(2,-0.5),113.62,29.82,4.6),
 (R(3,0.5),113.68,29.86,6.0),(R(3,6.0),113.76,29.95,7.5),(R(4,0),113.78,29.97,8.0),(E(4,0),113.78,29.97,8.0),
 (R(5,0.5),113.0,30.1,3.0),(E(5,0),112.7,30.2,3.2),
 (R(6,0.5),112.5,30.2,4.4),(E(6,-0.5),112.5,30.15,5.2),
 (R(7,0),112.42,30.2,6.5),(R(7,1.2),112.5,30.12,9.5),(R(7,3.2),112.5,30.1,9.5),(E(7,-0.2),112.5,30.1,6.0),
 (R(8,0.5),112.45,30.2,4.4),(E(8,-0.2),112.3,30.6,3.0),
 (R(9,0.5),115.4,31.0,1.7),(E(9,-0.2),115.4,31.0,1.75),
 (R(10,0.5),112.7,29.95,3.6),(E(10,-0.2),113.1,29.5,4.2),
 (R(11,0.5),115.4,31.0,1.5),(R(12,0.2),118.3,32.1,2.3),(E(12,0),118.3,32.1,2.4)]
CAM=sorted(CAM,key=lambda k:k[0])
NIGHT.append((TOTAL,0));NIGHT=sorted(NIGHT,key=lambda k:k[0])
MINI=[(0,TOTAL)]
def gate_open(t): return 0
def year_of(n):
    return 208 if n-BASE<=8 else 210
