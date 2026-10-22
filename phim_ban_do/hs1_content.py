"""Demo Hán Sở tranh hùng, video 1: Hồng Môn yến (năm 206 TCN). Số câu 1–28 (n = 6001–6028).
Vị trí thành và đường quân chỉ gần đúng."""
from build2 import T,D,TOTAL,chap,PH
INF=1e9
BASE=6000
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
# Sở (Hạng Vũ) xanh lam, Hán (Lưu Bang) xanh lá
SO=BL;HAN=GR
LOC={'Hàm Cốc':(110.45,34.52,'mid'),'Hồng Môn':(109.30,34.38,'mid'),'Bá Thượng':(109.00,34.27,'mid'),'Hàm Dương':(108.72,34.33,'big')}
CITIES=dict(LOC)
CITY_OWN={'Hàm Cốc':[(0,HAN),(R(2,0.5),HAN),(R(2,2.5),SO)],'Hàm Dương':[(0,NEU)]}
GROUPS=[];BATT=[];FIRES=[];FX=[];OBJ=[];LETTERS=[];ARROWS=[];NOTES=[];MARKS=[];CARDS3=[];QUOTES=[];JOKES=[];METERS=[];NUMS=[];TITLES=[]
REGIONS=[];RIVERS=[];ROUTES=[];TIDE=[];WATER=[]
NIGHT=[(0,0)]
def nt(n,o0,o1): NIGHT.extend([(R(n,o0),0),(R(n,o0+1.6),0.55),(R(n,o1),0.55),(R(n,o1+1.6),0)])
def G(name,col,n,keys,show=None,**kw):
    GROUPS.append(dict(name=name,col=col,n=n,keys=keys,show=show or (keys[0][0]-0.3,keys[-1][0]+3),**kw))
def NT(n,o,dur,lo,la,txt,col=DK): NOTES.append((R(n,o),min(R(n,o+dur),E(n,-0.1)),lo,la,txt,col))
def C3(n,o,dur,name,role,col): CARDS3.append((R(n,o),min(R(n,o+dur),E(n,-0.2)),name,role,col))
def Q(n,sub,text,who,col,dur=None):
    t0=at(n,sub);QUOTES.append((t0,min(E(n,-0.1),t0+(dur or 5.0)),text,who,col))
def J(n,icon,text,off=1.2): JOKES.append((R(n,off),E(n,-0.1),icon,text))
def AR(n,o,dur,a,b,col,txt): ARROWS.append((R(n,o),min(R(n,o+dur),E(n,-0.1)),a,b,col,txt))
def X(name): return LOC[name][:2]
SCN=[]
def S(a,b,lo,la,z): SCN.append((a,b,lo,la,z))
def reg(name,lab,poly,c0,win,steps=(),alpha=34):
    seq=[(0,c0)]
    for (t,c) in steps: seq+=[(t,seq[-1][1]),(t+3,c)]
    REGIONS.append(dict(name=name,lab=lab,poly=poly,own=seq,alpha=alpha,win=(R(win[0],-1),E(win[1],1))))
# ---------------- máy quay: ải rộng, rồi hai doanh trại, rồi quay lại doanh
S(1,2,110.0,34.48,4.6);S(3,4,109.3,34.36,6.2);S(5,6,109.15,34.33,7.4);S(7,8,109.15,34.33,7.0)
S(9,11,109.30,34.37,7.8);S(12,16,109.30,34.37,8.4);S(17,21,109.30,34.37,8.8);S(22,24,109.17,34.32,7.6);S(25,28,109.20,34.34,5.6)
TITLES.append((0.3,5.2,'HÁN SỞ TRANH HÙNG','HỒNG MÔN YẾN','năm 206 trước Công nguyên · bản demo'))
# ---------------- quân
# Hạng Vũ (xanh lam, đông) từ Hàm Cốc vào Hồng Môn; sau đó đóng ở Hồng Môn
G('Quân Hạng Vũ',SO,10,[(0,110.55,34.58),(R(1,1.0),110.45,34.52),(R(2,0.4),110.45,34.52),(R(2,6.0),109.37,34.415),(INF,109.37,34.415)],show=(0,INF),emb='tri',seed=611,kind='inf',soff=(70,-95))
G('Quân Lưu Bang',HAN,6,[(0,109.045,34.295)],show=(0,INF),emb='sun',seed=612,soff=(140,40))
G('Quân giữ ải',HAN,3,[(0,110.42,34.50)],show=(0,R(2,3.0)),emb='sun',seed=613,soff=(-70,-45),alive=[(0,1),(R(2,1.0),1),(R(2,4.0),0.0)])
# Hạng Bá phi ngựa trong đêm sang doanh Lưu Bang, rồi về
G('Hạng Bá',SO,1,[(0,109.36,34.41),(R(5,0.2),109.33,34.405),(R(5,5.0),109.06,34.30),(R(8,0.2),109.06,34.30),(R(8,4.5),109.33,34.405),(INF,109.33,34.405)],show=(R(5,0),R(9,0)),emb='tri',seed=614,kind='cav',soff=(-80,60),label=False)
# Lưu Bang và đoàn kỵ binh đến Hồng Môn xin lỗi, ở lại đến hết tiệc
G('Đoàn Lưu Bang',HAN,4,[(0,109.045,34.295),(R(9,0.2),109.045,34.295),(R(9,5.0),109.245,34.405),(INF,109.245,34.405)],show=(R(9,0),R(23,0.5)),emb='sun',seed=615,kind='cav',spread=0.6,soff=(-90,-70))
# Lưu Bang chạy bộ theo đường tắt về Bá Thượng với bốn người
G('Lưu Bang chạy tắt',HAN,5,[(0,109.245,34.405),(R(23,0.1),109.245,34.405),(R(23,6.0),109.15,34.35),(R(24,3.0),109.045,34.295),(INF,109.045,34.295)],show=(R(23,0),R(26,3.0)),emb='sun',seed=616,soff=(95,-20),label=False)
# ---------------- thẻ nhân vật (mỗi lần xuất hiện đầu tiên)
C3(1,0.4,3.4,'Hạng Vũ','chỉ huy quân Sở',SO)
C3(4,0.2,3.2,'Hạng Bá','chú của Hạng Vũ, bạn của Trương Lương',SO)
C3(6,0.3,3.0,'Trương Lương','mưu sĩ của Lưu Bang',HAN)
C3(14,0.2,3.0,'Phạm Tăng','quân sư của Hạng Vũ',SO)
C3(17,0.3,3.0,'Phàn Khoái','hộ vệ của Lưu Bang',HAN)
# ---------------- chú thích ngắn (không chồng nhau)
NT(1,0.4,3.0,110.2,34.62,'Lưu Bang cho đóng ải Hàm Cốc',HAN)
AR(2,1.0,5.0,X('Hàm Cốc'),X('Hồng Môn'),SO,'quân Sở vào ải')
NT(2,4.4,2.6,109.30,34.46,'doanh Hồng Môn',SO)
NT(3,0.6,3.6,109.30,34.46,'Tào Vô Thương mách tin',SO)
nt(5,0.0,7.0)
AR(5,0.8,5.5,X('Hồng Môn'),X('Bá Thượng'),SO,'tin báo trong đêm')
NT(5,5.8,2.0,109.00,34.35,'doanh Bá Thượng',HAN)
NT(7,0.5,3.0,109.00,34.35,'rót rượu, hứa kết thông gia',HAN)
AR(9,1.0,4.5,X('Bá Thượng'),X('Hồng Môn'),HAN,'đến xin lỗi')
J(11,'scroll','Người đưa tin bị bán đứng',2.0)
NT(12,0.4,3.0,109.30,34.46,'tiệc ở Hồng Môn',SO)
J(16,'flag','Điệu múa nhiều tính toán nhất lịch sử',2.2)
J(20,'coin','Một cái đùi lợn sống, một lời can',1.6) if False else None
AR(23,0.6,5.5,(109.245,34.405),X('Bá Thượng'),HAN,'đường tắt')
NT(25,0.4,3.2,109.20,34.40,'chén ngọc bị đập vỡ',SO)
J(28,'coin','Một chuyến đi nhà xí đổi cả lịch sử',2.5)
TITLES.append((R(28,3.4),E(28,0.5),'HẾT BẢN DEMO','HỒNG MÔN YẾN','Bữa tiệc suýt đổi cả lịch sử'))
# ======================= HOÀN TẤT
SCN.sort(key=lambda x:x[0])
CAM=[(0,SCN[0][2],SCN[0][3],SCN[0][4])]
for (a_,b_,lo,la,z) in SCN:
    CAM.append((R(a_)+1.6,lo,la,z));CAM.append((E(b_)-0.2,lo+0.01,la,z*1.03))
CAM=sorted(CAM,key=lambda k:k[0])
NIGHT.append((TOTAL,0));NIGHT=sorted(NIGHT,key=lambda k:k[0])
MINI=[(0,TOTAL)]
def gate_open(t): return 0
def year_of(n): return None
