"""Đinh Bộ Lĩnh dẹp mười hai sứ quân (Đại Cồ Việt, 968). Số đoạn 1–91 (n = 10001–10091). Bản đồ world7 (đồng bằng sông Hồng).
Vị trí các nơi lấy theo chú thích "nay là" của bản dịch Đại Việt sử ký toàn thư (mức B) nên chỉ gần đúng: Bình Kiều (Thanh Hóa), Đường Lâm (Ba Vì),
Phong Châu (Bạch Hạc), Bố Hải Khẩu (thị xã Thái Bình), Hoa Lư (Ninh Bình), Cổ Loa (kinh đô nhà Ngô). Tám sứ quân còn lại để chấm không nhãn,
vì Toàn thư chép tên và hiệu lệch nhau giữa hai đoạn. Những nơi sử không nói vị trí (sách Đào Áo, sách Bông, đất Ô Man, Đàm thôn) không đặt chấm riêng.
Vùng tô màu là minh họa, không phải biên giới chính xác. Mũi tên tỏa ra từ Hoa Lư ở đoạn 53 là hiệu ứng minh họa câu "một phen cất quân là dẹp yên",
không có nghĩa sử chép cụ thể hướng đánh hay thứ tự (xem mục Ghi chú độ chắc của kịch bản).
Bố cục theo quy tắc CLAUDE.md: không khung trích lời, đùa tối đa 3 giây và chỉ về tình huống mười hai người cùng xưng hùng, Q() ẩn ghi chú khi giao tranh.
Không có khung đùa nào về Đinh Bộ Lĩnh, Ngô Quyền, Lê Hoàn, Đinh Liễn, Hạng Lang."""
from build2 import T,D,TOTAL,chap,PH
import build2 as _B
import world7 as _W
INF=1e9
BASE=10000
def _f(n): return BASE+n
def _l(n): return BASE+n
def R(n,o=0): return T[BASE+n]+o
def E(n,o=0): return T[BASE+n]+D[BASE+n]+o
def at(n,sub,off=0.0):
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
VT=GR      # Đinh Bộ Lĩnh (Hoa Lư) xanh lá
NG=BL      # nhà Ngô xanh dương
SQ=PU      # các sứ quân tím
LOC={'Hoa Lư':(105.90,20.28,'big'),'Cổ Loa':(105.88,21.12,'big'),
     'Bình Kiều':(105.60,19.88,'town'),'Đường Lâm':(105.50,21.14,'town'),'Phong Châu':(105.43,21.32,'town'),'Bố Hải Khẩu':(106.34,20.45,'mid'),
     # tám sứ quân còn lại: chấm không nhãn (tên là khoảng trắng khác nhau)
     ' ':(105.52,21.25,'town'),'  ':(105.79,20.84,'town'),'   ':(105.85,20.96,'town'),'    ':(105.96,20.92,'town'),
     '         ':(105.50,21.14,'town'),'     ':(106.07,21.03,'town'),'      ':(106.03,21.15,'town'),'       ':(105.12,21.38,'town'),'        ':(106.05,20.67,'town')}
PIN8=[' ','  ','   ','    ','     ','      ','       ','        ']
PIN12=['Bình Kiều','Đường Lâm','Phong Châu','Bố Hải Khẩu']+PIN8
CITIES=dict(LOC)
CITY_SHOW={}
CITY_OWN={}
def show(name,a,b): CITY_SHOW.setdefault(name,[]).append((R(a,-1),E(b,1)))
def show_t(name,t0,t1): CITY_SHOW.setdefault(name,[]).append((t0,t1))
def own(name,col0,*steps):
    """steps = (thời điểm, màu mới): đổi màu cờ trong 2 giây."""
    seq=[(0,col0)]
    for (t,c) in steps: seq.append((t,seq[-1][1]));seq.append((t+2.0,c))
    CITY_OWN[name]=seq
GROUPS=[];BATT=[];FIRES=[];FX=[];OBJ=[];LETTERS=[];ARROWS=[];NOTES=[];MARKS=[];CARDS3=[];QUOTES=[];JOKES=[];METERS=[];NUMS=[];TITLES=[]
REGIONS=[];RIVERS=[];ROUTES=[];TIDE=[];AMBIENT=[];PROPS=[]
WATER=[('VỊNH BẮC BỘ',(107.3,19.9),26)]
NIGHT=[(0,0)]
def night(t0,t1): NIGHT.extend([(t0,0),(t0+1.6,0.55),(t1,0.55),(t1+1.6,0)])
def G(name,col,n,keys,show=None,**kw):
    GROUPS.append(dict(name=name,col=col,n=n,keys=keys,show=show or (keys[0][0]-0.3,keys[-1][0]+3),**kw))
QUIET=[]
def Q(a,b): QUIET.append((R(a,0),E(b,0)))
def NT(n,o,dur,lo,la,txt,col=DK): NOTES.append((R(n,o),min(R(n,o+min(dur,3.5)),E(n,-0.1)),lo,la,txt,col))
def C3(n,o,dur,name,role,col): CARDS3.append((R(n,o),min(R(n,o+dur),E(n,-0.2)),name,role,col))
def J(n,icon,text,off=1.2,dur=3.0): JOKES.append((R(n,off),min(E(n,-0.1),R(n,off)+dur),icon,text))
def NU(n,big,small,delay=1.2): NUMS.append((_f(n),big,small,delay))
def AR(n,o,dur,a,b,col,txt): ARROWS.append((R(n,o),min(R(n,o+dur),E(n,-0.1)),a,b,col,txt))
def LET(n,o,dur,a,b,txt): LETTERS.append((R(n,o),R(n,o+dur),a,b,txt))
def SKULL(n,o,dur,lo,la,txt): MARKS.append((R(n,o),R(n,o+dur),lo,la,'skull',txt))
def X(name): return LOC[name][:2]
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
# vùng minh họa (gần đúng)
P_NGO=[(105.15,21.55),(106.55,21.50),(106.95,20.60),(106.25,19.90),(105.40,19.70),(104.95,20.40)]
P_HL=[(105.76,20.40),(106.04,20.40),(106.06,20.18),(105.78,20.14)]
P_DCV=[(105.05,21.50),(106.55,21.45),(106.90,20.60),(106.30,19.95),(105.40,19.72),(104.95,20.45)]
# sông Hồng (gần đúng): Bạch Hạc, Hà Nội, rồi xuôi về cửa Ba Lạt
RIVER_HONG=[(105.43,21.30),(105.52,21.12),(105.72,21.06),(105.86,21.02),(105.95,20.86),(106.06,20.66),(106.17,20.44),(106.36,20.30),(106.55,20.22)]

TITLES.append((0.3,4.0,'ĐINH BỘ LĨNH','DẸP MƯỜI HAI SỨ QUÂN','Đại Cồ Việt, năm 968'))
RIVERS.append(('SÔNG HỒNG',RIVER_HONG,6,(105.62,21.04),(0,R(15,0))))
# ======================= CHƯƠNG 1: MỞ ĐẦU (1–6): cảnh treo con trên ngọn sào, rồi hai câu hỏi
S2(1,2,[X('Hoa Lư'),(105.99,20.33)],5.0)
show('Hoa Lư',1,91);show('Cổ Loa',1,14);show('Cổ Loa',23,91)
own('Hoa Lư',VT);own('Cổ Loa',NG,(R(52,1.0),VT))
G('Quân nhà Ngô',NG,12,[(R(1,0),105.99,20.33),(E(2,0),105.99,20.33)],show=(R(1,0),E(2,0)),emb='tri',seed=901,spread=0.9,soff=(70,0))
G('Quân Đinh Bộ Lĩnh',VT,8,[(R(1,0),105.90,20.28),(E(2,0),105.90,20.28)],show=(R(1,0),E(2,0)),emb='sun',seed=902,spread=0.7,soff=(-60,5))
NT(1,4.4,3.0,105.99,20.33,'Đinh Liễn bị treo trên ngọn sào',NG)
FX.append((at(1,'cầm nỏ'),at(1,'cầm nỏ',2.6),'volley',X('Hoa Lư'),(105.99,20.33)))
reg('ĐỘNG HOA LƯ',(105.90,20.56),P_HL,VT,(1,2),alpha=26)
S2(3,6,[X('Cổ Loa'),X('Bình Kiều'),X('Hoa Lư'),X('Bố Hải Khẩu')],3.0,hmax=340)
reg('NHÀ NGÔ',(105.80,21.40),P_NGO,NG,(3,6),alpha=14)
# ======================= CHƯƠNG 2: NƯỚC KHÔNG CÓ CHỦ (7–14)
S2(7,14,[X('Cổ Loa'),(106.22,20.58)],3.0,hmax=340)
reg('NHÀ NGÔ',(105.80,21.40),P_NGO,NG,(7,14),steps=[(R(13,0.5),NEU)],alpha=24)
NU(7,'năm 944','Ngô Quyền mất',0.8)
C3(7,3.2,3.0,'Dương Tam Kha','anh của hoàng hậu, cướp quyền',NEU)
NU(8,'năm 951','Ngô Xương Văn lấy lại ngôi',0.6)
C3(9,0.4,3.0,'Ngô Xương Văn','xưng Nam Tấn Vương',NG)
C3(9,3.6,3.0,'Ngô Xương Ngập','xưng Thiên Sách Vương',NG)
NU(11,'năm 954','Ngô Xương Ngập mất',0.8)
NU(12,'năm 965','Nam Tấn Vương tử trận',0.6)
G('Quân Nam Tấn Vương',NG,10,[(R(12,0),105.88,21.12),(R(12,3.6),106.22,20.58),(E(12,0),106.22,20.58)],show=(R(12,0),E(12,0)),emb='tri',seed=903,spread=0.8,soff=(-40,0),alive=[(0,1),(at(12,'phục binh'),1),(at(12,'phục binh',2.4),0.2)])
NT(12,3.0,3.0,106.22,20.58,'hai thôn Đường và Nguyễn, bị phục binh bắn nỏ',DK)
Q(14,14)
# ======================= CHƯƠNG 3: MƯỜI HAI NGƯỜI XƯNG HÙNG (15–22)
S2(15,22,[X('Hồi Hồ') if 'Hồi Hồ' in LOC else LOC['       '][:2],X('Bố Hải Khẩu'),X('Bình Kiều'),X('Phong Châu')],2.4,hmax=340)
_t_end=E(91,1)
def pin(name,t0): show_t(name,t0,_t_end)
pin('Bình Kiều',at(16,'Bình Kiều'));show_t('Đường Lâm',at(16,'Đường Lâm'),R(23,0));show_t('         ',R(23,0),_t_end);pin('Phong Châu',at(17,'Phong Châu'));pin('Bố Hải Khẩu',at(17,'Bố Hải'))
for _i,_nm in enumerate(PIN8): pin(_nm,R(18,0.5+0.4*_i))
for _nm in PIN12+['         ']: own(_nm,SQ)
C3(16,0.3,2.9,'Ngô Xương Xí','sứ quân ở Bình Kiều',SQ)
C3(16,3.7,3.0,'Ngô Nhật Khánh','sứ quân ở Đường Lâm',SQ)
C3(17,0.3,2.8,'Kiểu Công Hãn','sứ quân ở Phong Châu',SQ)
C3(17,3.2,2.8,'Trần Lãm','sứ quân ở Bố Hải Khẩu',SQ)
J(20,'scroll','Ai cũng là đại vương, chưa ai chịu làm thần dân',3.0)
# ======================= CHƯƠNG 4: CẬU BÉ Ở ĐỘNG HOA LƯ (23–34)
S2(23,34,[X('Hoa Lư')],6.5)
reg('ĐỘNG HOA LƯ',(105.90,20.46),P_HL,VT,(23,34),alpha=26)
NT(23,1.2,3.4,105.90,20.28,'núi đá bốn mặt dựng đứng như vách tường',BR)
C3(23,5.0,3.0,'Đinh Bộ Lĩnh','người động Hoa Lư, châu Đại Hoàng',VT)
G('Dân các sách theo về',VT,8,[(R(30,0),105.74,20.46),(R(30,5.5),105.88,20.31),(E(34,0),105.88,20.31)],show=(R(30,0),E(34,0)),emb='sun',seed=904,spread=0.7,soff=(-40,25))
G('Dân các sách theo về ',VT,6,[(R(30,0),106.06,20.14),(R(30,5.5),105.93,20.26),(E(34,0),105.93,20.26)],show=(R(30,0),E(34,0)),emb='sun',seed=905,spread=0.6,soff=(40,30),label=False)
G('Quân sách Bông',NEU,10,[(R(31,2.5),106.14,20.40),(R(32,0.5),105.97,20.31),(R(32,6),105.97,20.31),(E(34,0),105.97,20.31)],show=(R(31,2.5),E(34,0)),emb='circle',seed=906,spread=0.8,soff=(60,-20),defeats=[(at(32,'phải hàng'),'flag',E(34,0))])
BATT.append((R(32,0.0),R(32,5.0),105.93,20.30,['Quân sách Bông','Dân các sách theo về']))
C3(33,0.6,3.0,'Vạn Thắng Vương','tên người đời gọi Đinh Bộ Lĩnh',VT)
# ======================= CHƯƠNG 5: CON TIN TRÊN NGỌN SÀO (35–43)
S2(35,43,[X('Cổ Loa'),X('Hoa Lư')],4.0)
G('Quân Đinh Bộ Lĩnh ',VT,8,[(R(35,0),105.90,20.28),(E(43,0),105.90,20.28)],show=(R(35,0),E(42,0)),emb='sun',seed=907,spread=0.7,soff=(-50,5),label=False)
G('Quân nhà Ngô ',NG,12,[(R(35,0),105.88,21.12),(R(38,0),105.88,21.12),(R(38,7),105.99,20.33),(R(42,1),105.99,20.33),(R(42,8),105.88,21.12),(E(42,0),105.88,21.12)],show=(R(35,0),E(42,0)),emb='tri',seed=908,spread=0.9,soff=(60,0))
G('Đinh Liễn (con tin)',VT,1,[(R(37,0),105.90,20.28),(R(37,6),105.88,21.12),(R(38,0),105.88,21.12),(R(38,7),105.99,20.33),(E(41,0),105.99,20.33)],show=(R(37,0),E(41,0)),emb='sun',seed=909,spread=0.3,soff=(80,-25),label=False)
C3(37,0.4,3.0,'Đinh Liễn','con trai Đinh Bộ Lĩnh, đi làm con tin',VT)
NT(39,2.0,3.0,105.99,20.33,'treo Đinh Liễn lên ngọn sào',NG)
FX.append((R(41,0.2),R(41,3.4),'volley',X('Hoa Lư'),(105.99,20.33)))
Q(40,42)
NU(43,'năm 965','Đinh Liễn trở về Hoa Lư',3.0)
G('Đinh Liễn',VT,1,[(at(43,'trở về'),105.90,20.28),(E(44,0),105.90,20.28)],show=(at(43,'trở về'),E(44,0)),emb='sun',seed=910,spread=0.3,soff=(30,30),label=False)
# ======================= CHƯƠNG 6: VỀ VỚI TRẦN MINH CÔNG (44–52)
S2(44,52,[X('Cổ Loa'),X('Bố Hải Khẩu'),X('Hoa Lư')],3.2,hmax=340)
NU(44,'năm 967','Nước vẫn chưa có người đứng đầu',0.6)
C3(45,0.5,3.0,'Trần Minh Công','tức sứ quân Trần Lãm',SQ)
G('Đinh Bộ Lĩnh và Đinh Liễn',VT,3,[(R(45,2.0),105.90,20.28),(R(46,0.0),106.30,20.43),(E(46,0),106.30,20.43),(R(47,0),106.30,20.43)],show=(R(45,2.0),R(47,0.5)),emb='sun',seed=911,spread=0.4,soff=(-40,35),label=False)
G('Quân Đinh Bộ Lĩnh  ',VT,10,[(R(47,0),106.30,20.43),(R(47,5.5),106.05,20.62),(R(48,2),106.05,20.62),(R(49,0),106.30,20.43),(E(51,-3),106.30,20.43),(E(51,0),105.80,20.80),(E(52,0),105.80,20.80)],show=(R(47,0),E(52,0)),emb='sun',seed=912,spread=0.8,soff=(-50,35))
own('        ',SQ,(at(48,'về hàng'),VT));
NT(48,0.6,3.2,106.05,20.67,'Phạm Phòng Át đem quân về hàng',VT)
NT(49,0.2,2.8,106.34,20.45,'Trần Minh Công mất',SQ)
G('Con cháu họ Ngô',NG,10,[(R(49,3.0),105.79,20.84),(R(50,0.0),106.03,20.64),(R(50,4.5),106.03,20.64),(E(50,0),105.79,20.84)],show=(R(49,3.0),E(50,0)),emb='tri',seed=913,spread=0.8,soff=(-40,-10),defeats=[(at(50,'đánh bại'),'flag',E(50,0))])
G('Dân làng Ô Man',NEU,6,[(R(50,0.0),106.12,20.60),(E(50,0),106.12,20.60)],show=(R(50,0.0),E(50,0)),emb='circle',seed=914,spread=0.5,soff=(60,10),label=False)
BATT.append((R(50,0.8),R(50,4.3),106.07,20.62,['Con cháu họ Ngô','Dân làng Ô Man']))
C3(50,0.2,2.8,'Ngô Phó sứ','người làng ở đất Ô Man',NEU)
own('  ',SQ,(E(51,-1.0),VT))
NT(51,0.8,3.0,105.79,20.84,'Đỗ Động Giang',VT)
NT(52,0.8,3.0,105.88,21.12,'dân kinh đô cũ theo về, nhà Ngô mất',NG)
# ======================= CHƯƠNG 7: MỘT PHEN CẤT QUÂN (53–56)
S2(53,56,[X('Hồi Hồ') if 'Hồi Hồ' in LOC else LOC['       '][:2],X('Bố Hải Khẩu'),X('Bình Kiều'),X('Phong Châu')],2.4,hmax=340)
_tf=at(53,'một phen')
for _nm in PIN12+['         ']:
    if _nm=='        ' or _nm=='  ': continue
    own(_nm,SQ,(_tf,VT))
# 12 mũi tên cùng tỏa ra từ Hoa Lư (hiệu ứng minh họa "một phen cất quân", không phải đường đánh có sử chép)
for _nm in PIN12: ARROWS.append((_tf,_tf+2.2,X('Hoa Lư'),LOC[_nm][:2],VT,''))
FX.append((_tf,_tf+2.4,'horn',X('Hoa Lư'),X('Hoa Lư')))
NT(53,0.3,3.0,106.75,20.05,'sử chỉ chép một câu',DK)
NU(54,'năm 968','Đinh Bộ Lĩnh đủ mạnh để lên ngôi',3.2)
C3(55,0.4,3.0,'Lê Văn Hưu','sử gia',GD)
C3(56,0.4,3.0,'Ngô Sĩ Liên','sử gia',GD)
# ======================= CHƯƠNG 8: ĐẠI CỒ VIỆT VÀ KINH ĐÔ HOA LƯ (57–66)
S2(57,59,[X('Hoa Lư')],6.5)
NT(59,0.8,3.2,105.90,20.28,'núi đá bao quanh làm thành tự nhiên',BR)
S2(60,66,[X('Cổ Loa'),X('Bình Kiều'),X('Hoa Lư'),X('Bố Hải Khẩu')],2.8,hmax=340)
reg('ĐẠI CỒ VIỆT',(105.80,21.40),P_DCV,VT,(60,66),alpha=18)
NU(60,'năm 968','Đinh Bộ Lĩnh lên ngôi, quốc hiệu Đại Cồ Việt',1.2)
FX.append((at(60,'lên ngôi'),at(60,'lên ngôi',1.8),'trumpet',X('Hoa Lư'),(105.95,20.40)))
PROPS.append((R(61,0.6),E(61,0),'hall',105.90,20.31,'',0.9))
C3(62,0.4,3.0,'Đại Thắng Minh Hoàng Đế','hiệu các quan dâng Đinh Bộ Lĩnh',VT)
FX.append((R(62,0.3),R(62,1.5),'gong',X('Hoa Lư'),X('Hoa Lư')))
NT(64,0.8,3.2,105.90,20.28,'vạc dầu lớn và cũi hổ ở sân triều',BR)
C3(66,0.6,3.0,'Đinh Liễn','con trưởng, Nam Việt Vương',VT)
# ======================= CHƯƠNG 9: LẬP TRIỀU ĐÌNH, GIAO HẢO VỚI NHÀ TỐNG (67–72)
S(67,72,106.3,21.7,1.7)
_NORTH=(107.5,23.7)
LET(67,at(67,'sai sứ')-R(67,0),4.2,X('Hoa Lư'),_NORTH,'sứ sang nhà Tống')
NT(67,5.0,2.6,_NORTH[0],_NORTH[1],'nhà Tống ở phương bắc',RD)
C3(69,0.3,3.0,'Nguyễn Bặc','Định quốc công',VT)
C3(69,3.4,3.0,'Lê Hoàn','Thập đạo tướng quân',VT)
LET(70,at(70,'Nhà Tống')-R(70,0),4.4,_NORTH,X('Hoa Lư'),'phong vương')
C3(71,0.4,3.2,'Đinh Liễn','tiết độ sứ do nhà Tống phong',VT)
S2(72,72,[X('Hoa Lư')],5.2)
import math as _m
for _i in range(10):
    _a=_m.pi*2*_i/10
    G('Đạo quân %d'%(_i+1),VT,3,[(at(72,'mười đạo')+0.25*_i,105.90+0.13*_m.cos(_a),20.28+0.09*_m.sin(_a)),(E(72,0),105.90+0.13*_m.cos(_a),20.28+0.09*_m.sin(_a))],show=(at(72,'mười đạo')+0.25*_i,E(72,0)),emb='sun',seed=920+_i,spread=0.35,label=False)
NT(72,1.0,3.0,105.55,20.55,'mười đạo quân, mỗi đạo mười quân',VT)
# ======================= CHƯƠNG 10: NĂM HOÀNG HẬU VÀ ĐỨA CON NHỎ (73–78)
S2(73,78,[X('Hoa Lư')],5.5)
NT(73,0.4,3.0,105.90,20.28,'lập năm hoàng hậu',BR)
C3(75,0.6,3.0,'Hạng Lang','con nhỏ được vua yêu quý',VT)
NU(76,'năm 978','Lập Hạng Lang làm thái tử',0.6)
C3(76,3.6,3.0,'Đinh Toàn','con thứ, Vệ Vương',VT)
C3(78,0.4,3.0,'Ngô Sĩ Liên','sử gia',GD)
# ======================= CHƯƠNG 11: ĐÊM YẾN TIỆC (79–83)
S2(79,83,[X('Hoa Lư'),(105.97,20.34)],6.5)
night(R(79,0.2),E(83,0.0))
NU(79,'mùa đông 979','Yến tiệc ban đêm trong cung',1.0)
C3(80,0.4,3.0,'Đỗ Thích','chi hậu nội nhân',NEU)
NT(81,0.3,3.0,105.90,20.28,'vua Đinh bị giết ở sân cung',DK)
NT(82,3.0,3.0,105.90,20.28,'táng ở sơn lăng Trường Yên',BR)
SKULL(83,0.5,3.2,105.92,20.30,'Đỗ Thích bị xử tử')
# ======================= CHƯƠNG 12: KẾT (84–91)
S2(84,85,[X('Hoa Lư')],5.5)
C3(84,0.4,3.0,'Đinh Toàn','sáu tuổi nối ngôi',VT)
C3(84,4.0,3.0,'Lê Hoàn','nắm quyền hành',VT)
S2(86,88,[X('Hồi Hồ') if 'Hồi Hồ' in LOC else LOC['       '][:2],X('Bố Hải Khẩu'),X('Bình Kiều'),X('Phong Châu')],2.4,hmax=340)
reg('ĐẠI CỒ VIỆT',(105.80,21.40),P_DCV,VT,(86,91),alpha=16)
C3(88,0.4,3.0,'Ngô Sĩ Liên','sử gia',GD)
S2(89,89,[X('Hoa Lư')],5.2)
night(R(89,0.2),E(89,0.0))
S2(90,91,[X('Hồi Hồ') if 'Hồi Hồ' in LOC else LOC['       '][:2],X('Bố Hải Khẩu'),X('Bình Kiều'),X('Phong Châu')],2.4,hmax=340)
C3(90,0.4,3.0,'Ngô Sĩ Liên','sử gia',GD)
# ======================= HIỆU ỨNG THÊM (hình và âm, không thêm chữ trên màn hình)
# trại và cờ hiệu
PROPS.append((R(23,0.5),E(34,0),'pennants',105.62,20.14,'g',0.6))
PROPS.append((R(30,0.5),E(34,0),'camp',105.64,20.34,'',0.42))
PROPS.append((R(35,0.5),E(42,0),'camp',106.16,21.04,'',0.42))
PROPS.append((R(35,0.5),E(42,0),'pennants',106.18,21.26,'',0.6))
PROPS.append((R(45,3.0),R(47,1.0),'meeting',106.34,20.52,'',0.55))
# vòng sóng lan ra khi nơi nào về một cờ (chỉ minh họa)
for _i,_nm in enumerate(PIN12+['         ']):
    _lo,_la=LOC[_nm][:2];PROPS.append((_tf+1.6+0.22*_i,_tf+4.4+0.22*_i,'ping',_lo,_la,'g',0.55))
PROPS.append((R(60,0.0),R(60,4.0),'ping',105.90,20.28,'g',0.9))
PROPS.append((R(52,0.5),R(52,3.5),'ping',105.88,21.12,'g',0.8))
# quân tỏa từ Hoa Lư ra các nơi (minh họa câu "một phen cất quân")
for _i,_nm in enumerate(PIN12):
    _lo,_la=LOC[_nm][:2]
    G('Đạo tỏa %d'%_i,VT,3,[(_tf+0.2,105.90,20.28),(_tf+3.2,_lo,_la),(_tf+6.0,_lo,_la)],show=(_tf+0.2,_tf+6.0),emb='sun',seed=940+_i,spread=0.25,label=False)
FX.append((_tf+2.2,_tf+5.5,'drums',X('Hoa Lư'),X('Bố Hải Khẩu')))
# trận phục binh, các trận đã kể
FX.append((at(12,'phục binh'),at(12,'phục binh',2.6),'volley',(105.88,21.12),(106.22,20.58)))
FX.append((R(32,0.5),R(32,4.5),'drums',X('Hoa Lư'),(105.97,20.31)))
FX.append((R(50,0.8),R(50,4.0),'drums',(106.03,20.64),(106.12,20.60)))
FX.append((R(48,0.0),R(48,1.5),'horn',(106.05,20.62),(106.05,20.62)))
# đoàn sứ đi sang nhà Tống và trở về
G('Đoàn sứ',VT,5,[(at(67,'sai sứ'),105.90,20.28),(at(67,'sai sứ')+6.5,_NORTH[0],_NORTH[1]),(R(69,0),_NORTH[0],_NORTH[1])],kind='cav',show=(at(67,'sai sứ'),R(69,0)),emb='sun',seed=960,spread=0.35,label=False)
G('Đoàn sứ về',VT,5,[(at(70,'Nhà Tống'),_NORTH[0],_NORTH[1]),(at(70,'Nhà Tống')+6.5,105.90,20.28),(E(71,0),105.90,20.28)],kind='cav',show=(at(70,'Nhà Tống'),E(71,0)),emb='sun',seed=961,spread=0.35,label=False)
PROPS.append((at(70,'Nhà Tống')+0.5,at(70,'Nhà Tống')+4.5,'seal',107.2,23.45,'',0.7))
# đêm yến tiệc: vòng đỏ nhỏ ở Hoa Lư lúc biến cố
PROPS.append((at(81,'giết'),at(81,'giết')+3.0,'ping',105.90,20.28,'r',0.7))
# nền âm thanh theo chương (audio2.py)
AMBIENT.extend([(R(1,0),E(6,0),'wind',0.35),(R(7,0),E(14,0),'wind',0.4),(R(15,0),E(22,0),'crowd',0.3),(R(23,0),E(34,0),'forest',0.45),
 (R(35,0),E(43,0),'wind',0.4),(R(44,0),E(52,0),'forest',0.35),(R(45,4),E(47,0),'sea',0.25),(R(53,0),E(56,0),'wind',0.35),
 (R(57,0),E(66,0),'crowd',0.3),(R(60,0),E(66,0),'gulls',0.2),(R(67,0),E(72,0),'crowd',0.25),(R(73,0),E(78,0),'crowd',0.2),
 (R(79,0),E(83,0),'night',0.5),(R(79,0),E(83,0),'fire',0.2),(R(84,0),E(88,0),'wind',0.3),(R(89,0),E(89,0),'night',0.45),(R(90,0),TOTAL-1,'wind',0.3)])
# ======================= HOÀN TẤT
SCN.sort(key=lambda x:x[0])
CAM=[(0,SCN[0][2],SCN[0][3],SCN[0][4])]
for (a_,b_,lo,la,z) in SCN:
    CAM.append((R(a_)+1.6,lo,la,z));CAM.append((E(b_)-0.2,lo+0.01,la,z*1.03))
CAM=sorted(CAM,key=lambda k:k[0])
NIGHT.append((TOTAL,0));NIGHT=sorted(NIGHT,key=lambda k:k[0])
MINI=[(0,TOTAL)]
# âm nhạc nền tự tổng hợp (audio2.py), theo từng chương: (bắt đầu, kết thúc, tâm trạng, âm lượng)
QUIET_AUDIO=True   # tắt mọi tiếng nhiễu (gió, tick, whoosh, lửa, đám đông, bước chân nhóm nhỏ); chỉ giữ nhạc, trống, kèn, chiêng
MUSIC=[(0,R(3,0),'cang',1.0),(R(3,0),R(7,0),'mo',1.0),(R(7,0),R(15,0),'bi',1.0),(R(15,0),R(23,0),'loan',1.0),(R(23,0),R(35,0),'binh',1.0),
       (R(35,0),R(44,0),'cang',1.0),(R(44,0),R(53,0),'hanh',1.0),(R(53,0),_tf,'cang',1.0),(_tf,R(57,0),'trang',1.0),(R(57,0),R(67,0),'trang',0.9),
       (R(67,0),R(73,0),'binh',0.9),(R(73,0),R(79,0),'bi',1.0),(R(79,0),R(84,0),'dem',1.0),(R(84,0),R(89,0),'bi',1.0),(R(89,0),E(89,0),'dem',1.0),
       (E(89,0),TOTAL,'trang',1.0)]
def gate_open(t): return 0
def year_of(n):
    m=n-BASE
    for a,b,y in [(1,6,None),(7,7,944),(8,10,951),(11,11,954),(12,12,965),(13,22,966),(23,34,None),(35,42,None),(43,43,965),(44,52,967),(53,53,967),(54,56,968),(57,65,968),(66,66,969),
                  (67,67,970),(68,69,971),(70,71,973),(72,72,974),(73,73,970),(74,75,None),(76,76,978),(77,83,979),(84,84,979),(85,91,None)]:
        if a<=m<=b: return y
    return None
# bỏ nhãn tên trên nhóm quân; phe phân biệt bằng màu cờ + bảng chú giải góc phải
NO_GROUP_LABEL=True
SIDES=[('Nhà Ngô',NG,{g['name'].strip() for g in GROUPS if g['col']==NG}),('Các sứ quân',SQ,{g['name'].strip() for g in GROUPS if g['col']==SQ}),
       ('Đinh Bộ Lĩnh',VT,{g['name'].strip() for g in GROUPS if g['col']==VT}),('Địa phương',NEU,{g['name'].strip() for g in GROUPS if g['col']==NEU})]
