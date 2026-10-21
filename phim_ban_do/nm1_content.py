"""Nội dung hình ảnh demo Nguyên Mông tập 1 (1257–1258). Số câu 1–14."""
from build2 import T,D,TOTAL,chap,PH
INF=1e9
BASE=3000
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
# ---- thành
LOC={'Thăng Long':(105.85,21.03,'big'),'Vân Nam':(102.7,25.05,'mid'),'Bình Lệ Nguyên':(105.55,21.3,'town'),'Phù Lỗ':(105.88,21.22,'town'),'Quy Hóa':(104.55,21.85,'town'),'Biên giới':(103.97,22.5,'town')}
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

P_DV=[(103.5,22.7),(104.2,23.1),(106.5,23.2),(107.8,22.0),(107.4,20.9),(106.5,19.95),(105.0,19.9),(103.8,21.0),(103.4,22.0)]
# ======================= DEMO (1–14)
S(1,3,104.7,22.9,1.0);S(4,5,103.4,24.2,1.9);S(6,6,104.0,23.3,2.0);S(7,8,105.6,21.3,3.8);S(9,11,105.9,21.1,3.8);S(12,12,105.0,21.8,2.4);S(13,14,104.7,22.9,1.0)
TITLES.append((0.3,5.2,'NGUYÊN MÔNG · TẬP 1','MÔNG CỔ VÀO ĐẠI VIỆT','năm 1257 đến năm 1258'))
for nm in LOC: show(nm,1,14)
OW('Thăng Long',RD);OW('Vân Nam',BK,(1,0,BK))
G('Kỵ binh Mông Cổ',BK,14,[(R(1,0),100.6,25.9),(R(2,5),102.6,25.1)],show=(R(1,0),R(5,6)),emb='tri',seed=401,kind='cav',soff=(-120,-40))
AR(1,1.0,5.5,(100.3,26.0),(102.4,25.2),BK,'từ thảo nguyên phía bắc')
reg('ĐẠI VIỆT',(105.4,19.75) if False else (105.3,22.6),P_DV,RD,(2,14),alpha=26)
C3(2,3.0,3.2,'Nhà Trần','đang cầm quyền ở Đại Việt',RD)
NT(2,0.6,5.5,108.5,24.6,'nhà Tống giàu có',NEU)
AR(3,1.0,6.5,(103.9,22.6),(108.4,23.1),BK,'đường vòng đánh nhà Tống')
NU(4,'1257','Mông Cổ sai sứ đến Đại Việt',3.0)
C3(4,0.4,3.2,'Ngột Lương Hợp Thai','tướng Mông Cổ ở Vân Nam',BK)
LET(4,1.5,5.5,X('Vân Nam'),X('Thăng Long'),'đòi đầu hàng')
C3(5,0.4,3.2,'Trần Thái Tông','vua Đại Việt, không chịu hàng',RD)
NT(5,3.6,5.0,105.85,21.5,'sứ giả vào rồi không thấy về',(120,100,40))
G('Quân Đại Việt',RD,26,[(0,105.55,21.3)],show=(R(7,0),R(11,0)),emb='sun',seed=402,soff=(-120,-30),alive=[(0,1),(R(8,0),1),(R(8,6),0.35)])
G('Quân Mông Cổ',BK,30,[(R(6,0),102.7,25.05),(R(6,9),103.97,22.5),(R(7,0),105.1,21.55),(R(7,5),105.55,21.28),(R(10,0),105.85,21.05),(R(12,0),105.85,21.05),(R(12,8),103.97,22.5)],show=(R(6,0),R(12,10)),emb='tri',seed=403,kind='cav',soff=(130,-40))
NT(6,4.0,4.5,104.2,22.4,'đi men theo sông',BK)
NU(7,'17/1/1258','Trận Bình Lệ Nguyên',0.6)
C3(7,3.5,3.0,'Trần Thái Tông','đích thân ra trận',RD)
BATT.append((R(7,2),R(8,0),105.55,21.3,['Quân Mông Cổ','Quân Đại Việt']))
NT(8,0.4,3.0,105.55,21.55,'quân Đại Việt thua',RD);NT(8,3.2,4.0,105.88,21.4,'hôm sau thua tiếp ở Phù Lỗ',RD)
C3(9,0.4,3.2,'Trần Thủ Độ','người nắm quyền trong triều',RD)
Q(9,'Đầu thần chưa','Đầu thần chưa rơi xuống đất, xin bệ hạ đừng lo.','Trần Thủ Độ',RD,6.5)
G('Vua và triều đình',RD,10,[(R(10,0),105.85,21.03),(R(10,5),106.0,20.7)],show=(R(10,0),R(11,3)),emb='sun',seed=404,soff=(110,40))
NT(10,0.8,4.0,105.85,21.5,'vua và triều đình rút khỏi kinh đô',RD);NT(10,5.0,4.5,105.6,20.7,'không tìm thấy lương thực',BK)
NU(11,'CHÍN NGÀY','quân Mông Cổ ở Thăng Long',0.6)
G('Vua Trần và thái tử',RD,12,[(R(11,2),106.0,20.7),(R(11,7),105.9,21.0)],show=(R(11,2),R(12,6)),emb='sun',seed=405,soff=(120,50))
BATT.append((R(11,6),R(11,10),105.88,21.02,['Quân Mông Cổ','Vua Trần và thái tử']))
NT(11,4.0,5.0,105.9,20.7,'Đông Bộ Đầu, bên sông Hồng',RD)
G('Người địa phương',OL,8,[(0,104.55,21.85)],show=(R(12,2),R(12,10)),emb='circle',seed=406,soff=(-100,40))
AR(12,0.4,5.0,(105.85,21.05),(103.97,22.5),BK,'quân Mông Cổ rút')
NT(12,4.0,4.5,104.55,22.15,'Quy Hóa: bị đánh úp',OL)
J(13,'scroll','Hai cuốn sử, hai kết luận',2.0)
NT(13,0.6,3.2,106.4,21.6,'sử Việt: chiến thắng',RD);NT(13,3.9,3.5,103.9,21.5,'sử Nguyên: chiếm Thăng Long',BK)
NU(14,'1258 → 1284','hơn hai mươi năm sau, họ quay lại',1.5)
TITLES.append((R(14,3.0),E(14,0.5),'HẾT DEMO','NĂM 1258','Lần đầu, chưa phải lần cuối'))
# ======================= HOÀN TẤT
SCN.sort(key=lambda x:x[0])
CAM=[(0,SCN[0][2],SCN[0][3],SCN[0][4])]
for (a_,b_,lo,la,z) in SCN:
    CAM.append((R(a_)+1.6,lo,la,z));CAM.append((E(b_)-0.2,lo+0.02,la,z*1.03))
CAM=sorted(CAM,key=lambda k:k[0])
NIGHT.append((TOTAL,0));NIGHT=sorted(NIGHT,key=lambda k:k[0])
MINI=[(0,TOTAL)]
def gate_open(t): return 0
def year_of(n):
    m=n-BASE
    return None if m<=3 else (1257 if m<=6 else 1258)
