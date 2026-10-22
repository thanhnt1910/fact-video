"""Hán Sở tranh hùng, video 1: Từ cơn mưa đến Bành Thành (209–205 TCN). Số câu 1–232 (n = 7001–7232).
Bản đồ world4. Vị trí thành và đường quân chỉ gần đúng. Bố cục theo quy tắc CLAUDE.md (không khung trích lời, đùa tối đa 3 giây)."""
from build2 import T,D,TOTAL,chap,PH
import build2 as _B
_B.ERA='trước Công nguyên'
INF=1e9
BASE=7000
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
SO=BL;HAN=GR;TAN=BK;KN=RD   # Sở xanh lam, Hán xanh lá, Tần xám đen, quân khởi nghĩa đỏ
LOC={'Cối Kê':(120.60,31.30,'mid'),'Bái':(116.93,34.73,'town'),'Đại Trạch Hương':(117.95,33.55,'town'),'Trần':(114.90,33.75,'mid'),
 'Định Đào':(115.57,35.07,'town'),'Cự Lộc':(114.95,37.20,'mid'),'An Dương':(115.40,35.90,'town'),'Bành Thành':(117.18,34.27,'big'),
 'Hàm Cốc':(110.45,34.52,'mid'),'Hồng Môn':(109.30,34.38,'mid'),'Bá Thượng':(109.00,34.27,'town'),'Hàm Dương':(108.72,34.33,'big'),
 'Hán Trung':(107.03,33.07,'big'),'Trần Thương':(107.38,34.37,'town'),'Lạc Dương':(112.45,34.62,'big'),'Lâm Truy':(118.35,36.85,'mid'),
 'Tân An':(111.77,34.77,'town'),'Hoài Âm':(119.05,33.55,'town'),'Nghiệp':(114.35,36.35,'town')}
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
REGIONS=[];RIVERS=[];ROUTES=[];TIDE=[];WATER=[]
NIGHT=[(0,0)]
def nt(n,o0,o1): NIGHT.extend([(R(n,o0),0),(R(n,o0+1.6),0.55),(R(n,o1),0.55),(R(n,o1+1.6),0)])
def G(name,col,n,keys,show=None,**kw):
    GROUPS.append(dict(name=name,col=col,n=n,keys=keys,show=show or (keys[0][0]-0.3,keys[-1][0]+3),**kw))
QUIET=[]
def Q(a,b): QUIET.append((R(a,0),E(b,0)))
def NT(n,o,dur,lo,la,txt,col=DK): NOTES.append((R(n,o),min(R(n,o+min(dur,3.5)),E(n,-0.1)),lo,la,txt,col))
def C3(n,o,dur,name,role,col): CARDS3.append((R(n,o),min(R(n,o+dur),E(n,-0.2)),name,role,col))
def J(n,icon,text,off=1.2,dur=3.0): JOKES.append((R(n,off),min(E(n,-0.1),R(n,off)+dur),icon,text))
def NU(n,big,small,delay=1.2): NUMS.append((BASE+n,big,small,delay))
def AR(n,o,dur,a,b,col,txt): ARROWS.append((R(n,o),min(R(n,o+dur),E(n,-0.1)),a,b,col,txt))
def X(name): return LOC[name][:2]
SCN=[]
def S(a,b,lo,la,z): SCN.append((a,b,lo,la,z))

def S2(a,b,pts,zmax=8.0,zmin=1.4):
    """Camera tự tính: các điểm cần thấy nằm trong vùng an toàn (x 170–1380, y 250–700), chừa chỗ phía trên cho nhãn, tránh phụ đề và bản đồ nhỏ."""
    px=lambda z:96.9*z;py=lambda z:117.2*z
    los=[p_[0] for p_ in pts];las=[p_[1] for p_ in pts]
    dlo=max(los)-min(los);dla=max(las)-min(las)
    z=zmax
    if dlo>0: z=min(z,1200/(dlo*96.9))
    if dla>0: z=min(z,440/(dla*117.2))
    z=max(zmin,z)
    cx=(max(los)+min(los))/2+(1380+170-1920)/2/px(z)*-1   # dịch sang phải một chút để điểm nằm lệch trái, chừa bên phải cho bản đồ nhỏ
    cx=(max(los)+min(los))/2+ (960-775)/px(z)
    cy=max(las)-(432-330)/py(z)
    if dla==0: cy=las[0]-(432-470)/py(z)
    SCN.append((a,b,cx,cy,z))
def reg(name,lab,poly,c0,win,steps=(),alpha=34):
    seq=[(0,c0)]
    for (t,c) in steps: seq+=[(t,seq[-1][1]),(t+3,c)]
    REGIONS.append(dict(name=name,lab=lab,poly=poly,own=seq,alpha=alpha,win=(R(win[0],-1),E(win[1],1))))
L=LOC
TITLES.append((0.3,5.2,'HÁN SỞ TRANH HÙNG','TỪ CƠN MƯA ĐẾN BÀNH THÀNH','năm 209 đến năm 205 trước Công nguyên'))
# ======================= CHƯƠNG 1: MỞ ĐẦU (1–17)
S2(1,10,[L['Bái'][:2],L['Cối Kê'][:2]],2.6);S2(11,17,[L['Hàm Dương'][:2],L['Bành Thành'][:2]],3.0)
show('Cối Kê',1,10);show('Bái',1,17);show('Bành Thành',11,17);show('Hàm Dương',11,17)
G('Hạng Vũ',SO,5,[(0,120.60,31.30)],show=(R(2,-0.5),R(5,6)),emb='tri',seed=701,soff=(-140,-60))
G('Lưu Bang',HAN,5,[(0,116.93,34.73)],show=(R(2,-0.5),R(5,6)),emb='sun',seed=702,soff=(-65,-70))
C3(5,0.3,3.0,'Hạng Vũ','quý tộc nước Sở',SO)
C3(5,3.6,3.0,'Lưu Bang','đình trưởng ở huyện Bái',HAN)
J(9,'scroll','Sử xưa hay ghi số quân to như nói chuyện chợ',1.2)
NU(11,'NĂM 209','Trần Thắng · Hạng Vũ · Lưu Bang khởi binh',0.8)
NU(13,'NĂM 207','Cự Lộc · nhà Tần sụp',0.8)
NU(15,'NĂM 205','Lưu Bang chiếm Bành Thành',0.8)
AR(15,1.0,5.0,X('Hàm Dương'),X('Bành Thành'),HAN,'quân Hán đi về phía đông')
NT(16,0.4,4.0,115.0,35.6,'người thắng nhiều trận nhất, vì sao thua cả cuộc chiến?',DK)
# ======================= CHƯƠNG 2: MỘT CƠN MƯA (18–40)
S2(18,19,[L['Bái'][:2],L['Trần'][:2],L['Đại Trạch Hương'][:2]],2.4);S2(20,24,[L['Đại Trạch Hương'][:2],L['Trần'][:2]],4.0);S2(25,25,[L['Trần'][:2]],4.0);S2(26,29,[L['Cối Kê'][:2]],5.0);S2(30,39,[L['Bái'][:2]],6.0);S2(40,40,[L['Trần'][:2],L['Bái'][:2],L['Cối Kê'][:2]],3.2)
for nm in ('Đại Trạch Hương','Trần'): show(nm,20,25)
show('Cối Kê',26,40);show('Bái',30,40);show('Bành Thành',40,40)
G('900 lính thú',KN,8,[(0,117.95,33.55)],show=(R(20,0),R(24,6)),emb='tri',seed=711,soff=(-60,-150))
G('Quân khởi nghĩa Trần Thắng',KN,14,[(R(24,0),117.95,33.55),(R(25,2),114.95,33.75),(INF,114.95,33.75)],show=(R(24,0),R(25,8)),emb='tri',seed=712,spread=0.8,soff=(0,-80))
G('Quân Hạng Vũ',SO,8,[(0,120.60,31.30)],show=(R(26,0),R(40,6)),emb='tri',seed=713,spread=0.6,soff=(80,-70))
G('Quân Lưu Bang',HAN,5,[(0,116.93,34.73)],show=(R(38,0),R(40,6)),emb='sun',seed=714,spread=0.5,soff=(-70,-70))
NU(18,'NĂM 210','Tần Thủy Hoàng mất · Triệu Cao cầm quyền',1.0)
C3(20,0.4,3.0,'Trần Thắng','chỉ huy toán lính thú',KN)
C3(20,3.8,3.0,'Ngô Quảng','chỉ huy toán lính thú',KN)
NT(21,0.5,4.0,117.95,33.9,'mưa lớn, đường ngập, không tới kịp hạn',DK)
J(24,'flag','Cờ có rồi. Giờ chỉ thiếu người đứng đầu',3.5)
NT(25,0.4,3.5,114.9,33.4,'Trần Thắng xưng vương, chưa đầy nửa năm thì bại',DK)
C3(26,0.4,3.0,'Hạng Vũ','cao lớn, chú là Hạng Lương',SO)
C3(30,0.4,3.0,'Lưu Bang','đình trưởng, chức nhỏ nhất',HAN)
NT(35,0.5,4.0,116.93,35.05,'áp giải tù đi Lệ Sơn, tù trốn dần',HAN)
J(36,'coin','Tính nhẩm xong: thả luôn cho đỡ mất đầu',3.0) if False else None
C3(39,0.4,3.0,'Tiêu Hà','viên chức trong huyện',HAN)
C3(39,3.8,3.0,'Phàn Khoái','người mổ chó',HAN)
NU(40,'3 ĐÁM LỬA','Trần Thắng đã tắt · Hạng Vũ · Lưu Bang',0.8)
# ======================= CHƯƠNG 3: ĐỊNH ĐÀO VÀ CỰ LỘC (41–73)
S2(41,46,[L['Cối Kê'][:2]],4.0);S2(47,48,[L['Định Đào'][:2],(114.0,34.7)],4.0);S2(49,49,[L['Cự Lộc'][:2],L['Định Đào'][:2]],4.0);S2(50,55,[L['Bành Thành'][:2],L['An Dương'][:2],L['Hàm Cốc'][:2]],3.0);S2(56,61,[L['An Dương'][:2]],5.0);S2(62,64,[(114.55,36.45),L['Nghiệp'][:2]],5.0);S2(65,66,[L['Cự Lộc'][:2],(114.85,36.9)],5.0);S2(67,69,[L['Cự Lộc'][:2],(113.5,36.5)],4.0);S2(70,72,[L['Tân An'][:2],L['Hàm Cốc'][:2]],5.0);S2(73,73,[L['Tân An'][:2],L['Hàm Dương'][:2]],3.0)
show('Cối Kê',41,46);show('Bành Thành',50,55)
for nm in ('Định Đào','Cự Lộc'): show(nm,47,73)
for nm in ('An Dương','Nghiệp'): show(nm,56,69)
show('Tân An',70,73);show('Hàm Cốc',50,73)
G('Quân Sở của Hạng Lương',SO,10,[(0,120.60,31.30),(R(44,0),120.60,31.30),(R(47,0),115.57,35.07),(INF,115.57,35.07)],show=(R(41,0),R(49,6)),emb='tri',seed=721,spread=0.7,soff=(-110,-70),alive=[(0,1),(R(48,0),1),(R(48,5),0.25)])
G('Quân Tần Chương Hàm',TAN,14,[(0,114.0,34.7),(R(46,0),114.0,34.7),(R(47,0),115.45,35.0),(R(49,0),115.0,37.15),(INF,115.0,37.15)],show=(R(46,0),R(69,6)),emb='tri',seed=722,spread=0.9,soff=(150,-20),alive=[(0,1),(R(66,3),1),(R(68,5),0.45)])
G('Quân Sở đi bắc',SO,14,[(0,117.18,34.27),(R(51,0),117.18,34.27),(R(55,0),115.40,35.88),(R(61,0),115.40,35.88),(R(63,0),114.55,36.45),(R(66,0),114.85,37.05),(INF,114.85,37.05)],show=(R(51,0),R(73,8)),emb='tri',seed=723,spread=0.9,soff=(120,40))
G('Quân Lưu Bang đi tây',HAN,7,[(0,117.18,34.27),(R(52,0),117.18,34.27),(R(54,0),115.65,34.4),(R(73,0),115.65,34.4)],show=(R(52,0),R(73,0)),emb='sun',seed=724,spread=0.6,soff=(-80,60),label=False)
C3(41,0.4,3.0,'Phạm Tăng','mưu sĩ già, bảy mươi tuổi',SO)
C3(44,0.4,3.0,'Hùng Tâm','cháu vua Sở, đang chăn cừu',SO)
NT(45,0.5,4.5,120.60,31.7,'lập lên làm Sở Hoài Vương',SO)
nt(47,0.0,5.0)
AR(51,1.0,5.0,X('Bành Thành'),(115.40,35.88),SO,'đường bắc cứu Triệu')
AR(52,1.0,5.0,X('Bành Thành'),X('Hàm Cốc'),HAN,'đường tây vào đất Tần')
NT(53,0.5,6.0,113.4,35.1,'ai vào Quan Trung trước thì làm vua nơi đó',DK)
C3(51,0.4,3.0,'Tống Nghĩa','chỉ huy cao nhất',SO) if False else None
NU(56,'46 NGÀY','Tống Nghĩa dừng ở An Dương',0.8)
J(58,'coin','Tiệc lớn giữa mưa rét, lính đói bụng',2.0)
C3(60,0.3,3.0,'Hạng Vũ','nắm quyền chỉ huy',SO)
FIRES.extend([(R(63,3.0),R(64,0.0),114.55,36.45)])
BATT.append((R(66,0.8),R(66,5.5),114.95,37.12,['Quân Sở đi bắc','Quân Tần Chương Hàm']))
NT(70,0.5,4.5,111.77,35.05,'Tân An: sử chép khoảng 200.000 hàng binh',DK)
J(73,'flag','Một người thắng bằng nồi vỡ, một người thắng bằng cái bánh',2.0) if False else None
# ======================= CHƯƠNG 4: VÀO KINH ĐÔ NHÀ TẦN (74–102)
S2(74,79,[(115.65,34.4),L['Hàm Dương'][:2]],3.0);S2(80,84,[L['Hàm Dương'][:2]],6.4);S2(85,93,[L['Hàm Dương'][:2],L['Bá Thượng'][:2]],8.4);S2(94,99,[L['Hàm Dương'][:2],L['Bá Thượng'][:2]],7.4);S2(100,102,[L['Bá Thượng'][:2],L['Hàm Cốc'][:2]],5.4)
show('Hàm Dương',74,102);show('Bá Thượng',85,99)
for nm in ('Hàm Cốc','Lạc Dương'): show(nm,74,102)
G('Quân Lưu Bang',HAN,7,[(0,115.65,34.4),(R(74,0),115.65,34.4),(R(76,0),112.6,33.2),(R(82,0),109.55,34.05),(R(85,0),109.0,34.27),(R(85,5),109.0,34.27),(INF,109.0,34.27)],show=(R(74,0),R(102,10)),emb='sun',seed=741,spread=0.5,soff=(90,-110))
C3(76,0.4,3.2,'Trương Lương','con cháu quý tộc nước Hàn',HAN)
NT(77,0.5,5.0,112.0,34.1,'thuê lực sĩ ném chùy vào xe vua Tần, chùy trượt',DK)

NT(82,1.0,5.0,108.72,34.7,'chỉ hươu bảo ngựa',TAN)
NT(86,0.4,5.0,108.72,34.7,'Tử Anh ngồi xe trắng, dâng ấn',TAN)
C3(88,0.3,2.8,'Tử Anh','vua Tần cuối cùng',TAN)
NT(89,0.5,4.5,108.72,34.7,'vàng bạc chất đống, rèm gấm màn lụa',GD)
C3(91,0.3,2.8,'Phàn Khoái','can: làm vua hay làm nhà giàu?',HAN)
C3(94,0.3,2.8,'Tiêu Hà','giữ sổ sách nhà Tần',HAN)
NU(98,'3 ĐIỀU','giết người thì chết · gây thương và trộm bị trị tội · bỏ hết luật còn lại',0.8)
J(99,'coin','Người từng ghi nợ quán rượu giờ từ chối rượu miễn phí',2.5)
AR(100,1.0,5.0,X('Bá Thượng'),X('Hàm Cốc'),HAN,'đóng cửa ải Hàm Cốc')
G('Quân giữ ải',HAN,3,[(0,110.42,34.50)],show=(R(101,0),R(103,0)),emb='sun',seed=742,soff=(-70,-45))
# ======================= CHƯƠNG 5: HỒNG MÔN YẾN (103–142)
S(103,104,110.0,34.48,6.2);S(105,108,109.3,34.36,8.3);S(109,115,109.15,34.33,9.9);S(116,118,109.30,34.37,10.4);S(119,132,109.30,34.37,11.3);S(133,139,109.17,34.32,10.2);S(140,142,109.20,34.34,7.5)
for nm in ('Hàm Cốc','Hồng Môn','Bá Thượng','Hàm Dương'): show(nm,103,142)
OW('Hàm Cốc',HAN,(104,0.5,SO))
G('Quân Hạng Vũ',SO,10,[(0,110.55,34.58),(R(103,1.0),110.45,34.52),(R(104,0.4),110.45,34.52),(R(104,6.0),109.37,34.415),(INF,109.37,34.415)],show=(R(103,0),R(143,3)),emb='tri',seed=751,kind='inf',spread=0.6,soff=(70,-95))
G('Quân Lưu Bang',HAN,6,[(0,109.045,34.295)],show=(R(103,0),R(166,0)),emb='sun',seed=752,spread=0.45,soff=(-60,-85))
G('Quân giữ ải',HAN,3,[(0,110.42,34.50)],show=(R(103,0),R(104,3.0)),emb='sun',seed=753,soff=(-70,-45),alive=[(0,1),(R(104,1.0),1),(R(104,4.0),0.0)])
G('Hạng Bá',SO,1,[(0,109.36,34.41),(R(110,0.2),109.33,34.405),(R(110,5.0),109.06,34.30),(R(115,0.2),109.06,34.30),(R(115,4.5),109.33,34.405),(INF,109.33,34.405)],show=(R(110,0),R(116,0)),emb='tri',seed=754,kind='cav',soff=(-80,60),label=False)
G('Đoàn Lưu Bang',HAN,4,[(0,109.045,34.295),(R(116,0.2),109.045,34.295),(R(116,5.0),109.245,34.405),(INF,109.245,34.405)],show=(R(116,0),R(135,0.5)),emb='sun',seed=755,kind='cav',spread=0.6,soff=(-90,-70))
G('Lưu Bang chạy tắt',HAN,5,[(0,109.245,34.405),(R(135,0.1),109.245,34.405),(R(135,6.0),109.15,34.35),(R(136,3.0),109.045,34.295),(INF,109.045,34.295)],show=(R(135,0),R(139,3.0)),emb='sun',seed=756,spread=0.5,soff=(-60,-85),label=False)
C3(103,0.4,3.2,'Hạng Vũ','chỉ huy quân Sở',SO)
NT(103,3.6,2.8,110.2,34.62,'Lưu Bang cho đóng ải Hàm Cốc',HAN)
AR(104,1.0,5.0,X('Hàm Cốc'),X('Hồng Môn'),SO,'quân Sở vào ải')
NT(105,0.4,3.5,109.30,34.50,'sử chép 400.000 và 100.000 quân; thực tế ít hơn',DK)
C3(109,0.2,3.2,'Hạng Bá','chú của Hạng Vũ, bạn của Trương Lương',SO)
nt(110,0.0,7.0)
AR(110,0.8,5.5,X('Hồng Môn'),X('Bá Thượng'),SO,'tin báo trong đêm')
C3(112,0.3,3.0,'Trương Lương','mưu sĩ của Lưu Bang',HAN)
AR(116,1.0,4.5,X('Bá Thượng'),X('Hồng Môn'),HAN,'đến xin lỗi')
J(118,'scroll','Người đưa tin bị bán đứng',2.0) if False else None
NT(119,0.4,3.0,109.30,34.46,'tiệc ở Hồng Môn',SO)
C3(120,0.2,3.0,'Phạm Tăng','quân sư của Hạng Vũ',SO)
C3(121,0.2,3.0,'Hạng Trang','em họ của Hạng Vũ',SO)
C3(126,0.3,3.0,'Phàn Khoái','hộ vệ của Lưu Bang',HAN)
AR(135,0.6,5.5,(109.245,34.405),X('Bá Thượng'),HAN,'đường tắt')
J(133,'coin','Một chuyến đi nhà xí đổi cả lịch sử',2.5)
J(139,'scroll','Người báo tin nhận về một kết cục không hay',1.5)
# ======================= CHƯƠNG 6: HẠNG VŨ CHIA THIÊN HẠ (143–170)
S2(143,144,[L['Hàm Dương'][:2]],7.0);S2(145,149,[L['Hàm Dương'][:2],(111.0,34.2)],4.0);S2(150,152,[L['Bành Thành'][:2],(116.0,34.75)],3.5);S2(153,154,[L['Bành Thành'][:2],(113.8,30.8)],3.0);S2(155,158,[L['Bành Thành'][:2],(120.4,34.8),(115.4,33.6)],3.0);S2(159,159,[L['Lâm Truy'][:2],(118.3,37.2)],4.0);S2(160,162,[L['Hán Trung'][:2],L['Hàm Dương'][:2],(110.2,35.8)],3.0);S2(163,170,[L['Bá Thượng'][:2],L['Hán Trung'][:2]],4.0)
show('Hàm Dương',143,170)
for nm in ('Bành Thành','Lạc Dương','Hàn Cốc','Hán Trung','Hàm Cốc','Lâm Truy'):
    if nm in LOC: show(nm,145,170)
P_TAYSO=[(115.6,33.6),(118.8,33.2),(120.6,31.0),(120.4,34.8),(119.0,35.5),(116.6,35.7),(115.4,34.9)]
P_HAN=[(106.2,32.2),(107.9,32.2),(108.2,33.6),(106.5,34.0)]
P_TAMTAN=[(108.2,34.0),(110.0,34.0),(110.2,35.8),(108.0,36.3)]
P_TE=[(117.0,36.9),(119.5,36.9),(119.8,35.7),(117.6,35.5)]
reg('TÂY SỞ',(117.7,34.4),P_TAYSO,SO,(155,170),alpha=26)
reg('TAM TẦN',(109.1,35.4),P_TAMTAN,TAN,(162,170),alpha=26)
reg('HÁN',(106.9,32.45),P_HAN,HAN,(160,170),alpha=30)
reg('TỀ',(118.3,36.2),P_TE,OR,(159,170),alpha=26)
FIRES.extend([(R(144,0.5),R(144,9),108.72,34.35),(R(144,1.2),R(144,9),108.60,34.30),(R(144,2.0),R(144,9),108.82,34.42)])
NT(144,0.6,6.0,108.72,34.62,'đốt cung điện nhà Tần: sử chép cháy ba tháng',OR)
G('Quân Hạng Vũ',SO,12,[(0,109.37,34.415),(R(143,0),109.37,34.415),(R(143,4),108.8,34.36),(R(146,0),108.8,34.36),(R(150,0),113.5,34.2),(R(155,0),117.18,34.27),(INF,117.18,34.27)],show=(R(143,0),R(213,0)),emb='tri',seed=761,spread=0.8,soff=(160,-40))
J(149,'flag','Lời chê đúng, nói sai chỗ',1.0) if False else None
AR(153,1.0,5.0,X('Bành Thành'),(113.8,30.8),SO,'đưa Nghĩa Đế đi vùng sông nước phía nam')
NT(154,0.5,4.5,114.4,31.4,'theo sử, Anh Bố được sai giết Nghĩa Đế dọc đường',DK)
C3(156,0.3,3.2,'Tây Sở Bá Vương','Hạng Vũ, kinh đô Bành Thành',SO)
NU(158,'18 NƯỚC','phong vương theo người thân',0.8)
C3(159,0.3,3.0,'Điền Vinh','quý tộc nước Tề, bị bỏ rơi',OR) if False else None
C3(160,0.3,3.2,'Hán Vương','Lưu Bang, vua nước Hán',HAN)
NT(161,0.5,4.5,106.9,32.0,'nước Hán nhỏ trong núi, tên triều đại bốn trăm năm',HAN)
NT(162,0.5,6.0,109.1,36.1,'Tam Tần chặn đúng cửa núi: Chương Hàm, Tư Mã Hân, Đổng Ế',TAN)
G('Quân Lưu Bang vào Hán Trung',HAN,12,[(0,109.0,34.27),(R(166,0),109.0,34.27),(R(168,0),108.2,33.8),(R(171,0),107.03,33.07),(INF,107.03,33.07)],show=(R(166,0),R(202,0)),emb='sun',seed=762,spread=0.8,soff=(-120,-110))
J(165,'flag','Ta sẽ nhịn: kế hoạch dài hạn của người nóng tính',1.5)
C3(167,0.3,3.0,'Trương Lương','khuyên đốt sạn đạo',HAN)
FIRES.extend([(R(170,0.5),R(170,8),107.95,33.55),(R(170,1.0),R(170,8),107.75,33.45),(R(170,1.6),R(170,8),107.55,33.35)])
NT(168,0.5,6.0,107.8,33.85,'sạn đạo: đường gỗ trên vách núi, đốt để tỏ ý không quay lại',DK)
# ======================= CHƯƠNG 7: HÀN TÍN (171–211)
S2(171,173,[L['Hán Trung'][:2]],6.0);S2(174,180,[L['Hoài Âm'][:2]],5.0);S2(181,185,[L['Hán Trung'][:2]],6.0);S2(186,193,[L['Hán Trung'][:2],(106.1,33.5)],5.0);S2(194,201,[L['Hán Trung'][:2]],6.0);S2(202,206,[L['Hán Trung'][:2],L['Trần Thương'][:2]],4.0);S2(207,208,[L['Hàm Dương'][:2],(109.4,34.8)],5.0);S2(209,211,[L['Hàm Dương'][:2]],5.5)
show('Hán Trung',171,211);show('Hoài Âm',174,180);show('Trần Thương',202,211);show('Hàm Dương',202,211);show('Hàm Cốc',202,211);show('Bành Thành',174,180)
C3(173,0.3,3.0,'Hàn Tín','người Hoài Âm, chưa có chức gì',OL)
G('Hàn Tín',OL,1,[(0,119.05,33.55)],show=(R(174,0),R(180,8)),emb='sun',seed=771,soff=(-80,-60))
NT(177,0.5,5.0,119.05,33.95,'chợ: chui qua háng tên côn đồ',OL)
C3(182,0.3,3.0,'Hạ Hầu Anh','thân cận của Lưu Bang',HAN)
C3(184,0.3,3.0,'Tiêu Hà','nhận ra kỳ tài',HAN)
AR(186,0.8,5.0,X('Hán Trung'),(106.1,33.5),HAN,'Tiêu Hà phóng ngựa đuổi trong đêm')
nt(186,0.0,5.5)
J(187,'coin','Thừa tướng trốn rồi! Hóa ra đi bắt người trốn',3.0) if False else None
NU(190,'ĐẠI TƯỚNG','tướng thường dễ kiếm · kỳ tài khó tìm',0.8)
NT(191,0.5,5.0,107.03,33.45,'chọn ngày, ăn chay, lập đàn, làm lễ bái đại tướng',HAN)
J(193,'flag','Cả quân đoán nhầm: ai cũng nghĩ mình là người được chọn',1.5)
NT(199,0.5,5.0,107.03,33.45,'dùng người tài · chia đất cho công thần · quân nhớ nhà sẽ theo',HAN)
G('Quân Hàn Tín',HAN,14,[(0,107.03,33.07),(R(202,0),107.03,33.07),(R(203,0),107.03,33.07),(R(205,0),107.3,34.0),(R(205,5),107.38,34.3),(R(207,0),108.45,34.3),(R(208,0),108.7,34.4),(INF,108.7,34.4)],show=(R(202,0),INF),emb='sun',seed=772,spread=0.9,soff=(-90,-70))
G('Lính sửa sạn đạo',HAN,4,[(0,107.5,33.6)],show=(R(204,0),R(206,8)),emb='sun',seed=773,soff=(70,50),label=False)
AR(203,1.0,6.0,X('Hán Trung'),(107.55,33.55),HAN,'sửa sạn đạo ở chỗ sáng')
AR(205,0.5,6.0,(107.03,33.07),X('Trần Thương'),HAN,'đi vòng, ra ở Trần Thương')
OW('Hàm Dương',NEU,(208,0.5,HAN))

C3(210,0.3,3.0,'Tiêu Hà','ở lại giữ Quan Trung',HAN)
# ======================= CHƯƠNG 8: QUAY RA QUAN TRUNG, ĐÁNH BÀNH THÀNH (212–232)
S2(212,215,[L['Bành Thành'][:2],L['Lâm Truy'][:2]],3.0);S2(216,217,[L['Hàm Dương'][:2],L['Hàm Cốc'][:2],L['Lạc Dương'][:2]],4.0);S2(218,222,[L['Lạc Dương'][:2]],6.0);S2(223,224,[L['Lạc Dương'][:2],L['Bành Thành'][:2]],3.0);S2(225,229,[L['Bành Thành'][:2]],6.0);S2(230,232,[L['Bành Thành'][:2],L['Lạc Dương'][:2]],3.0)
for nm in ('Lâm Truy','Bành Thành'): show(nm,212,232)
for nm in ('Hàm Cốc','Lạc Dương'): show(nm,216,232)
show('Hàm Dương',216,223)
G('Quân Hạng Vũ ở Tề',SO,14,[(0,117.18,34.27),(R(214,0),117.18,34.27),(R(214,8),118.0,36.4),(INF,118.0,36.4)],show=(R(213,0),INF),emb='tri',seed=781,spread=0.9,soff=(70,-70))
G('Quân Điền Vinh',OR,8,[(0,118.35,36.85)],show=(R(213,0),R(215,8)),emb='sun',seed=782,soff=(-80,-60))
C3(213,0.3,3.0,'Điền Vinh','quý tộc nước Tề',OR)
C3(213,3.6,3.0,'Bành Việt','thủ lĩnh quân du kích',OR)
NT(215,0.5,5.0,118.2,37.2,'đốt thành, bắt người: dân Tề nổi dậy khắp nơi',OR)
G('Quân Lưu Bang ra đông',HAN,16,[(0,108.7,34.4),(R(216,0),109.5,34.5),(R(216,5),110.45,34.52),(R(217,0),111.8,34.6),(R(217,6),112.45,34.62),(R(219,0),112.45,34.62),(R(222,0),112.45,34.62),(R(223,0),114.0,34.4),(R(225,0),116.0,34.3),(R(226,0),117.18,34.27),(INF,117.18,34.27)],show=(R(216,0),INF),emb='sun',seed=783,spread=0.9,soff=(-60,-130))
NU(216,'ĐẦU NĂM 205','Lưu Bang ra khỏi Hàm Cốc',0.8)
C3(218,0.3,3.0,'Cụ già Lạc Dương','chặn ngựa Lưu Bang',HAN)
NT(220,0.5,5.0,112.45,34.2,'Lưu Bang để tang ba ngày cho Nghĩa Đế',DK)
NT(224,0.5,5.0,114.5,35.2,'sử chép 560.000 quân; con số hiếm khi được tin',DK)
OW('Bành Thành',SO,(226,0.5,HAN))
NT(227,0.5,4.5,117.18,34.65,'chiếm kho báu, bắt phụ nữ trong cung, thu vàng bạc',GD)
NT(229,0.5,4.5,117.18,34.65,'chỉ khoảng một năm: từ bị đẩy vào núi đến ngồi trong kinh đô của kẻ đày mình',HAN)
J(226,'flag','Vào nhà người ta, gặp kho mà không gặp chủ',1.5)
TITLES.append((R(232,4.0),E(232,0.5),'HẾT PHẦN 1','BÀNH THÀNH','Hạng Vũ đang quay về')) if False else None
# ======================= HOÀN TẤT
SCN.sort(key=lambda x:x[0])
CAM=[(0,SCN[0][2],SCN[0][3],SCN[0][4])]
for (a_,b_,lo,la,z) in SCN:
    CAM.append((R(a_)+1.6,lo,la,z));CAM.append((E(b_)-0.2,lo+0.01,la,z*1.03))
CAM=sorted(CAM,key=lambda k:k[0])
NIGHT.append((TOTAL,0));NIGHT=sorted(NIGHT,key=lambda k:k[0])
MINI=[(0,TOTAL)]
def gate_open(t): return 0
def year_of(n):
    m=n-BASE
    for a,b,y in [(1,10,None),(11,12,209),(13,14,207),(15,15,205),(16,17,None),(18,19,210),(20,40,209),(41,46,209),(47,50,208),(51,69,207),(70,70,207),(71,73,207),
                  (74,84,207),(85,102,207),(103,142,206),(143,170,206),(171,201,206),(202,206,206),(207,208,206),(209,211,205),(212,215,205),(216,232,205)]:
        if a<=m<=b: return y
    return None

# cảnh đánh nhau: tự ẩn ghi chú, khung đùa, thẻ số
Q(47,48);Q(51,52);Q(66,69);Q(207,208);Q(214,215);Q(230,232)
