"""Nội dung bản thử: chương Quan Độ (câu 1177–1206)."""
from build2 import T,D,TOTAL,chap,PH
def R(n,o=0): return T[n]+o
def E(n,o=0): return T[n]+D[n]+o
INF=1e9
def at(n,sub,off=0.0):
    """Thời điểm cụm lời kể chứa chữ `sub` bắt đầu được đọc (giây tuyệt đối)."""
    for c,s_,e_ in PH.get(str(n),[]):
        if sub.lower() in c.lower(): return T[n]+0.12+s_+off
    return T[n]+1.0+off
GR=(52,142,86);BL=(54,96,176);RD=(190,52,42);PU=(138,52,112);DK=(46,38,58);GD=(205,160,40)
TL=(40,140,150);BR=(150,100,60);OR=(200,110,40);GY=(110,110,110);OL=(110,130,50);BK=(60,60,60)
LOC={'Hứa':(113.83,34.03),'Lạc Dương':(112.45,34.62),'Quan Độ':(114.0,34.72),'Diên Tân':(114.2,35.15),'Bạch Mã':(114.52,35.57),
     'Lê Dương':(114.5,35.76),'Nghiệp':(114.35,36.35),'Ô Sào':(114.55,35.05),'Lâm Tri':(118.35,36.8),'Thường Sơn':(114.5,38.0)}
KIND={'Hứa':'big','Nghiệp':'big','Lạc Dương':'big','Quan Độ':'mid','Bạch Mã':'mid','Lâm Tri':'mid','Diên Tân':'town','Lê Dương':'town','Ô Sào':'town'}
CITIES={n:(*LOC[n],KIND[n]) for n in LOC if n!='Thường Sơn'}
def L(n,dx=0,dy=0): return (LOC[n][0]+dx,LOC[n][1]+dy)
def own(*seq): return [(t,c) for t,c in seq]
PUF=(122,96,140)
CITY_OWN={'Hứa':own((0,BL)),'Quan Độ':own((0,BL)),'Diên Tân':own((0,BL)),'Bạch Mã':own((0,BL)),
 'Nghiệp':own((0,PU)),'Lê Dương':own((0,PU)),'Lâm Tri':own((0,PU)),
 'Ô Sào':own((0,PU),(R(1198)+6,PU),(R(1198)+8,DK))}
def reg(name,lab,poly,c0,c1=None,tc=None):
    seq=[(0,c0)]
    if c1: seq+=[(tc,c0),(tc+3,c1)]
    return dict(name=name,lab=lab,poly=poly,own=seq,alpha=40)
REGIONS=[
 reg('KÝ CHÂU',(114.9,37.3),[(113.6,36.0),(113.4,37.2),(113.9,38.45),(116.6,38.45),(116.9,37.4),(116.2,36.3),(115.3,35.85),(114.6,35.78)],PU,PUF,R(1205)),
 reg('TINH CHÂU',(111.9,37.3),[(110.3,36.0),(110.2,38.45),(113.4,38.45),(113.6,36.0)],PU,PUF,R(1205)),
 reg('THANH CHÂU',(118.5,37.45),[(116.9,37.4),(116.6,38.45),(120.2,38.45),(121.0,37.2),(120.2,36.4),(118.4,36.0),(117.2,36.2)],PU,PUF,R(1205)),
 reg('ĐẤT TÀO THÁO',(112.7,33.7),[(111.5,33.2),(111.6,34.95),(113.5,35.02),(114.1,35.12),(114.9,35.0),(116.5,34.7),(116.5,33.2),(114.5,32.9)],BL)]
WATER=[]
RIVERS=[('HOÀNG HÀ',[(110.6,34.78),(111.5,34.86),(112.6,34.98),(113.5,35.03),(114.1,35.2),(114.5,35.67),(115.1,36.05),(115.9,36.5),(116.7,37.2),(117.6,37.7),(118.6,37.95),(119.6,38.2)],7,(115.75,36.35))]
SC=[(1177,1177,114.9,36.35,2.0),(1178,1178,114.6,35.9,2.0),(1179,1180,114.35,36.3,3.0),(1181,1181,114.5,35.85,3.0),(1182,1182,114.25,35.3,3.3),
    (1183,1183,114.48,35.45,4.2),(1184,1184,114.4,35.7,3.0),(1185,1185,114.25,35.2,2.4),(1186,1187,114.3,35.4,2.8),(1188,1189,114.25,35.1,4.0),
    (1190,1192,114.08,34.9,4.4),(1193,1195,113.95,34.4,3.0),(1196,1197,114.12,34.85,4.0),(1198,1198,114.3,34.95,3.5),(1199,1200,114.08,34.85,4.4),
    (1201,1202,114.3,35.4,2.9),(1203,1204,114.05,34.8,4.4),(1205,1206,114.3,36.0,1.9)]
CAM=[(0,SC[0][2],SC[0][3],SC[0][4])]
for (a_,b_,lo,la,z) in SC:
    CAM.append((R(a_)+1.6,lo,la,z));CAM.append((E(b_)-0.2,lo+0.02,la,z*1.03))
CAM=sorted(CAM,key=lambda k:k[0])
GROUPS=[]
def G(**k): GROUPS.append(k)
NG=L('Nghiệp',0.02,0.14);LD=(114.75,36.0);QD=(114.0,34.68);VC=(114.1,34.95);BM=(114.45,35.62);DT=(114.2,35.1);OS=LOC['Ô Sào']
# Viên Thiệu (quân chính)
G(name='Viên Thiệu',col=PU,n=16,emb='tri',seed=2,soff=(170,10),show=(0,R(1201)+6),
  keys=[(0,*NG),(R(1181)-0.5,*NG),(R(1181)+6,*LD),(R(1190)-1,*LD),(R(1190)+5,*VC),(R(1199)+1,*VC),(R(1199)+3.2,114.05,34.8)],
  alive=[(0,1),(R(1199)+2,1),(R(1200)+3.5,0.1)],defeats=[(R(1200)+3.5,'lose',INF)])
# Tào Tháo (quân chính)
G(name='Tào Tháo',col=BL,n=12,emb='dia',seed=4,soff=(-190,10),show=(0,INF),
  keys=[(0,*L('Hứa',0,-0.1)),(R(1180),*L('Hứa',0,-0.1)),(R(1181)+6,*QD),(R(1182)+1.0,*QD),(R(1182)+3.0,*DT),(R(1182)+3.6,*DT),(R(1182)+7.2,114.4,35.32),(R(1187)-0.5,114.4,35.32),
        (R(1188)+4,*DT),(R(1189)+6,*DT),(R(1190)+4,*QD)])
# Bạch Mã
G(name='Nhan Lương',col=PU,n=7,kind='cav',emb='tri',seed=6,show=(R(1181)-0.5,R(1184)+3),
  keys=[(R(1181)-0.5,*LD),(R(1181)+4,114.38,35.7),(R(1184)+4,114.38,35.7)],defeats=[(R(1183)+5.2,'skull',INF)],
  alive=[(0,1),(R(1183)+5,1),(R(1183)+6,0.2)])
G(name='Lưu Diên',col=BL,n=4,emb='dia',seed=7,soff=(90,30),show=(R(1181)+3,R(1184)+3),keys=[(0,114.55,35.52)])
G(name='Quan Vũ',col=GR,n=3,kind='cav',emb='sun',seed=8,show=(R(1183)-0.5,R(1187)+3),
  keys=[(R(1183)-0.5,114.34,35.28),(R(1183)+2,114.34,35.28),(R(1183)+4.4,114.42,35.6),(R(1183)+7,114.36,35.34),(R(1186)+0.6,114.36,35.34),(R(1186)+7,114.38,36.1)])
G(name='Lưu Bị',col=GR,n=5,emb='sun',seed=9,show=(R(1184)-0.5,R(1188)),keys=[(0,114.4,36.15)])
# Diên Tân
G(name='Văn Sửu',col=PU,n=7,kind='cav',emb='tri',seed=10,show=(R(1188)-0.3,R(1190)-0.5),
  keys=[(R(1188)-0.3,114.5,35.6),(R(1188)+5,114.25,35.2),(R(1189)+7,114.25,35.2)],defeats=[(R(1189)+5.8,'skull',INF)],
  alive=[(0,1),(R(1189)+5.5,1),(R(1189)+6.5,0.2)])
# Hứa Du, đột kích Ô Sào
G(name='Hứa Du',col=OL,n=1,emb='dia',seed=11,show=(R(1196)+3.5,R(1198)),keys=[(R(1196)+3.5,*VC),(R(1196)+7,114.03,34.76),(R(1198),114.03,34.76)])
G(name='quân canh kho',col=PU,n=4,emb='tri',seed=12,show=(R(1197)+3,R(1198)+7.5),keys=[(0,*OS)],defeats=[(R(1198)+6.8,'lose',INF)],
  alive=[(0,1),(R(1198)+6,1),(R(1198)+7,0.2)])
G(name='quân mang cờ Viên Thiệu',col=PU,n=9,emb='tri',seed=13,show=(R(1198)+0.4,R(1198)+4.3),keys=[(R(1198)+0.4,*QD),(R(1198)+4.2,114.55,35.0)])
G(name='Tào Tháo',col=BL,n=9,emb='dia',seed=14,show=(R(1198)+4.3,R(1199)+4),keys=[(0,114.55,35.0)],soff=(0,40))
# Trương Cáp, Cao Lãm
G(name='Trương Cáp · Cao Lãm',col=PU,n=5,emb='tri',seed=15,show=(R(1199)+0.3,R(1199)+4.6),keys=[(R(1199)+0.3,*VC),(R(1199)+3.6,114.03,34.77),(R(1199)+5,114.03,34.77)],soff=(40,0))
G(name='Trương Cáp · Cao Lãm',col=BL,n=5,emb='dia',seed=16,show=(R(1199)+4.6,R(1201)),keys=[(0,114.03,34.77)],soff=(40,0))
# Viên Thiệu bỏ chạy
G(name='Viên Thiệu',col=PU,n=4,kind='cav',emb='tri',seed=17,show=(R(1201)+0.3,R(1202)),keys=[(R(1201)+0.3,*VC),(R(1201)+4,114.4,35.4),(R(1201)+7.6,114.7,35.95)])
BATT=[(R(1183)+3.6,R(1183)+6.8,114.5,35.6,['Quan Vũ','Nhan Lương']),
      (R(1189)+3.2,R(1189)+6.3,114.25,35.17,['Văn Sửu','Tào Tháo']),
      (R(1199)+2.2,R(1200)+3.4,114.04,34.79,['Viên Thiệu','Tào Tháo'])]
FIRES=[(R(1198)+5,R(1200)+2,*OS),(R(1198)+5.4,R(1200)+1,OS[0]+0.04,OS[1]+0.03),(R(1198)+5.8,R(1200)+1.5,OS[0]-0.04,OS[1]+0.03),
       (R(1203)+2.5,E(1203),113.96,34.66)]
NIGHT=[(0,0),(R(1196)+2,0),(R(1196)+4,0.6),(R(1198)+9,0.6),(R(1199)+1,0)]
# công trình
TW=[(113.97,34.87),(114.07,34.88),(114.17,34.87)]
OBJ=[];FX=[(R(1181)+4.5,R(1181)+7,'horn',(114.45,35.62),(114.45,35.62))]
for j,tw in enumerate(TW):
    c0=R(1191)+0.4+j*2.4
    OBJ.append((R(1190)+2.0+j*0.5,c0+1.5,'tower',tw,tw))
    FX.append((R(1190)+2.6+j*0.5,c0+1.5,'volley',tw,(114.02,34.72)))
    FX.append((c0,c0+2.2,'catapult',(114.05,34.70),tw))
OBJ+=[(R(1192)+0.5,R(1192)+8,'tunnel',(114.08,34.96),(114.0,34.78)),(R(1192)+4,INF,'ditch',(113.86,34.8),(114.16,34.8)),
      (R(1188)+2.5,R(1189)+3,'loot',(114.48,35.5),(114.22,35.14))]
LETTERS=[(R(1186)+0.4,R(1186)+4,LOC['Bạch Mã'],LOC['Quan Độ'],'thư từ biệt'),(R(1193)+2,R(1193)+5.5,LOC['Quan Độ'],LOC['Hứa'],'nên rút không?'),
         (R(1194)+0.5,R(1194)+3.6,LOC['Hứa'],LOC['Quan Độ'],'xin ông cứ giữ')]
ARROWS=[(R(1182)+1.0,R(1182)+3.6,LOC['Quan Độ'],LOC['Diên Tân'],BL,'giả vờ ở Diên Tân'),(R(1182)+4.2,R(1182)+7.4,LOC['Diên Tân'],LOC['Bạch Mã'],RD,'đánh gấp Bạch Mã'),
        (R(1205)+3,E(1205)-0.3,LOC['Quan Độ'],LOC['Nghiệp'],BL,'phía bắc không còn đối thủ')]
NOTES=[(R(1180)+3.6,E(1180)-0.3,*L('Nghiệp'),'Điền Phong bị giam',DK),(R(1184)+0.6,R(1184)+3.8,114.46,35.38,'Hán Thọ đình hầu',GR),
       (R(1196)+7,R(1197)+2.5,114.03,34.76,'Hứa Du đào ngũ',OL),(R(1199)+4.6,R(1200)+2.4,114.03,34.77,'đầu hàng Tào Tháo',BL),
       (R(1202)+3.5,E(1202)-0.2,114.0,34.7,'chồng thư bắt được',(110,70,30)),(R(1177)+0.6,R(1178)+0.5,114.9,38.2,'U Châu ở xa hơn về phía bắc',PU)]
MARKS=[]
TITLES=[(0.3,4.3,'NĂM 200','QUAN ĐỘ','Viên Thiệu đối đầu Tào Tháo')]
def cd(n,sub,dur,name,role,col,off=0.0): 
    t0=at(n,sub,off);return (t0,min(t0+dur,E(n)-0.2),name,role,col)
CARDS3=[cd(1179,'Điền Phong và',4.3,'Điền Phong','khuyên kéo dài',TL),cd(1179,'Điền Phong và',4.3,'Thư Thụ','khuyên kéo dài',TL),
 cd(1179,'Thẩm Phối',9,'Thẩm Phối','khuyên đánh ngay',OR),cd(1179,'Thẩm Phối',9,'Quách Đồ','khuyên đánh ngay',OR),
 cd(1181,'Nhan Lương dẫn',3.6,'Nhan Lương','tiên phong của Viên Thiệu',PU),cd(1182,'Tuân Du',3.4,'Tuân Du','mưu sĩ của Tào Tháo',BL),
 cd(1183,'Trương Liêu và',3.4,'Quan Vũ','tướng của Lưu Bị',GR),cd(1185,'Trương Liêu',3.0,'Trương Liêu','tướng của Tào Tháo',BL),
 cd(1188,'Văn Sửu',3.8,'Văn Sửu','tướng giỏi thứ hai của Viên Thiệu',PU),cd(1193,'Tuân Úc',3.4,'Tuân Úc','giữ Hứa cho Tào Tháo',BL),
 cd(1196,'Hứa Du',3.6,'Hứa Du','mưu sĩ của Viên Thiệu',OL),
 cd(1199,'Hai tướng',5.5,'Trương Cáp','tướng của Viên Thiệu',PU),cd(1199,'Hai tướng',5.5,'Cao Lãm','tướng của Viên Thiệu',PU)]
CARDS=[]
QUOTES=[(at(1185,'đã thề'),E(1185)-0.1,'Ta đã thề cùng sống chết với Lưu tướng quân, không thể phụ.','Quan Vũ',GR),
 (at(1186,'mỗi người một chủ'),E(1186)-0.1,'Mỗi người một chủ, để ông ấy đi.','Tào Tháo',BL),
 (at(1194,'lùi trước'),E(1194)-0.1,'Ai lùi trước, người ấy thua. Xin ông cứ giữ.','Tuân Úc',BL),
 (at(1197,'kho lương của'),at(1197,'kho lương của')+5.2,'Kho lương của Viên Thiệu ở Ô Sào, chỉ có một ít quân canh giữ.','Hứa Du',OL),
 (at(1203,'Ông nói'),E(1203)-0.1,'Lúc Viên Thiệu mạnh như vậy, ta còn không tự bảo đảm được mình, huống chi người khác.','Tào Tháo',BL)]
JOKES=[(R(1187)+1.3,E(1187)-0.1,'coin','Lời hứa đắt hơn vàng'),(R(1195)+0.8,E(1195)-0.1,'scroll','Một lá thư, vài tháng cho cả bản đồ'),
 (R(1200)+2.4,E(1200)-0.1,'fire','Một kho lương, cả đạo quân'),(R(1204)+1.4,E(1204)-0.1,'fire','Đốt thư: giữ người rẻ nhất'),
 (R(1206)+1.2,E(1206)-0.1,'fire','Thua thường chỉ vì một nhà kho cháy')]
def cv(a,b,t0,t1): return [(0,a),(t0,a),(t1,b)]
METERS=[(R(1178)+1.2,E(1178)+0.2,'BINH LỰC (hình dung)',[('Viên Thiệu',PU,cv(0.95,0.95,0,1)),('Tào Tháo',BL,cv(0.4,0.4,0,1))]),
 (R(1193)+0.3,R(1201),'LƯƠNG THỰC',[('Quân Tào',BL,[(0,0.65),(R(1193),0.65),(R(1193)+6,0.18),(R(1198)+9,0.18)]),('Quân Viên',PU,[(0,0.9),(R(1198)+4.5,0.9),(R(1198)+6.5,0.05)])]),]
MINI=[(0,R(1201)+8),(R(1203),TOTAL)]
NUMS=[(1198,'5.000 QUÂN','đêm đi tắt tới Ô Sào',1.6),(1201,'KHOẢNG 800','kỵ binh theo Viên Thiệu qua sông',1.6)]
def year_of(n): return 199 if n<=1180 else 200

ROUTES=[]
