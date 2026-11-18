# Bản dài tm11m: Dương Đình Nghệ lấy lại Đại La 931 (bộ tranh riêng t11_*), kịch bản mới kể kèm phân tích
import math,re,json
import khung_dung as K
from khung_dung import cam,cpath,PAP,W,H,title
from canh import *
from fx_tran import arrows,dust,sparks,fall
from dai_tm2 import big,tagfall,strike,lb
from dai_tm3 import night
V=K.setup('tm11m',{2:4.0,6:2.6,11:2.6})
T,E,mid,TX=V.T,V.E,V.mid,V.TX
P=PTS
CARDS={6:'Dương Đình Nghệ',11:'Sau Đại La'}
# mốc đầu từng câu trong đoạn: chia theo số chữ (tiếng đọc đều)
_SC={}
for _n,_t in TX.items():
    _s=[x for x in re.split(r'(?<=[.!?])\s+',_t) if x.strip()];_w=[len(x.split()) for x in _s];_tot=sum(_w);_c=[0]
    for _k in _w: _c.append(_c[-1]+_k/_tot)
    _SC[_n]=_c
def sb(n,k):
    """thời điểm bắt đầu câu k của đoạn n; k bằng số câu thì là hết đoạn"""
    return T[n]+(E[n]-T[n])*_SC[n][k]
def mcam(t,keys):
    cx,cy,z=cpath(t,keys);cx=min(max(cx,960/z),1920-960/z);cy=min(max(cy,540/z),1080-540/z);return cam(cx,cy,z)
def pt(k,dx=0,dy=0): return (P[k][0]+dx,P[k][1]+dy)
HD=(645,651)   # Hải Dương, tính từ tọa độ Đại La theo kinh vĩ độ
# ---------- 1. hook
def S_1(cv,t):
    c=cam(*cpath(t,[(0,(960,560,1.12)),(E[1]+.3,(960,540,1.0))]))
    if t<1.4: u=eo(t/1.3);put_screen(cv,A('blot'),W/2,H/2,(1-u)*.85,s=1.9*(1+u*.9))
    put(cv,c,'t11_con',960,570,s=.95)
    big(cv,'BA NGHÌN CON NUÔI',t,.25,3.2,RED,150,84,seed=1)
    big(cv,'MỘT TÒA THÀNH',t,3.3,E[1]+.3,INK,150,84,seed=2)
# ---------- 2. Đại La và họ Khúc (bản đồ)
def S_2(cv,t):
    c=mcam(t,[(T[2]-.5,(560,520,1.4)),(sb(2,1),(500,590,2.3)),(E[2],(540,620,2.0))])
    mapbg(cv,c,u=inn(t,T[2]-1.2,1.4))
    dl=P['daila']
    dot(cv,c,*dl,o=1);tag(cv,c,dl[0]-20,dl[1]-34,'Đại La',dy=0,sz=28)
    lb(cv,c,'nay là Hà Nội',dl[0]-20,dl[1]-70,t,T[2]+.6,sb(2,1)-.2,col=RED,sz=26)
    if t>sb(2,1):
        dot(cv,c,*HD,o=inn(t,sb(2,1)+.8,.4));tag(cv,c,HD[0]+14,HD[1]+34,'Hải Dương',o=inn(t,sb(2,1)+.8,.4),dy=0,sz=26)
        lb(cv,c,'họ Khúc, dòng hào trưởng',HD[0]+20,HD[1]+70,t,sb(2,1)+1.0,E[2]+.3,col=RED,sz=26)
    if t>sb(2,2):
        lb(cv,c,'đầu thế kỷ mười: xưng Tiết độ sứ',dl[0]+240,dl[1]-110,t,sb(2,2)+.2,mid(2,.93),col=INK,sz=28)
        lb(cv,c,'nhà Đường công nhận',dl[0]+240,dl[1]-70,t,sb(2,2)+2.4,E[2]+.3,col=RED,sz=28)
# ---------- 3. cải cách họ Khúc
def S_3a(cv,t):
    a,b=T[3],sb(3,1)
    c=cam(*cpath(t,[(a-.3,(960,560,1.0)),(b+.3,(960,560,1.08))]))
    put(cv,c,'t11_phu',960,520,s=.7)
    tagfall(cv,c,960,250,'Khúc Hạo',t,a+.3,sz=44,col=INK)
    lb(cv,c,'làm nhiều hơn là giữ thành',960,330,t,a+1.2,b+.3,col=RED,sz=38)
def S_3b(cv,t):
    a,b=sb(3,1),sb(3,2)
    c=cam(*cpath(t,[(a-.3,(900,560,1.0)),(b+.3,(1000,560,1.06))]))
    put(cv,c,'t11_ruong',960,500,s=.98)
    L=['chia lại lộ, phủ, châu, xã','thuế ruộng cho đều','bỏ việc bắt dân đi lao dịch','lập sổ họ tên, quê quán']
    d=(b-a)/4
    for i,s_ in enumerate(L):
        lb(cv,c,s_,960,150,t,a+.1+i*d,a+(i+1)*d,col=RED if i%2 else INK,sz=44)
    if t>a+3*d: put(cv,c,'t11_so',1500,560,s=.5,o=inn(t,a+3*d,.6))
def S_3c(cv,t):
    a,b=sb(3,2),E[3]
    c=cam(*cpath(t,[(a-.3,(960,540,1.0)),(b+.3,(960,540,1.07))]))
    put(cv,c,'t11_so',960,560,s=.95)
    lb(cv,c,'tự quản bằng sổ sách và thuế má của riêng mình',960,110,t,a+.3,b+.3,col=RED,sz=40)
    lb(cv,c,'vẫn mang chức do nhà Đường công nhận',960,990,t,mid(3,.8),b+.3,sz=36)
# ---------- 4. Nam Hán bắt Khúc Thừa Mỹ
def S_4(cv,t):
    a,b=T[4],E[4]
    c=mcam(t,[(a-.5,(520,520,1.5)),(sb(4,1)-.3,(960,540,1.0)),(b,(960,540,1.0))])
    mapbg(cv,c,u=1)
    dl,qc=P['daila'],P['quangchau']
    dot(cv,c,*dl,o=1);tag(cv,c,dl[0]+16,dl[1]+30,'Đại La',dy=0,sz=26)
    dot(cv,c,*qc,o=1);tag(cv,c,qc[0]-60,qc[1]+40,'Quảng Châu',dy=0,sz=26)
    if t<sb(4,1):
        lb(cv,c,'họ Khúc giữ được ba đời',dl[0]+300,dl[1]-150,t,a+.3,sb(4,1)-.2,sz=34)
    else:
        lb(cv,c,'nhà Nam Hán',qc[0]-110,qc[1]+80,t,sb(4,1)+.2,E[4]+.3,col=RED,sz=28)
        stroke(cv,c,[qc,(1250,330),(800,480),dl],inn(t,sb(4,1)+.5,2.4),wid=9,col=RED)
        if t>sb(4,1)+3.6: stroke(cv,c,[dl,(800,480),(1250,330),qc],inn(t,sb(4,1)+3.6,2.4),wid=7,col=INK,dash=14)
        lb(cv,c,'Khúc Thừa Mỹ bị đưa về Quảng Châu',1250,300,t,sb(4,1)+4.0,sb(4,2)-.2,sz=26)
    if t>sb(4,2):
        seal(cv,'s923',1330,260,sb(4,2)+.8,t,s=.8,r=-5);seal(cv,'s930',1560,330,sb(4,2)+2.6,t,s=.8,r=4)
        put_screen(cv,text('sách chép không thống nhất',34,INK,700,glow=4),W/2,150,inn(t,sb(4,2)+.2,.5)*(1-inn(t,E[4]+.1,.4)))
# ---------- 5. Lý Tiến, rồi Ái Châu
def S_5a(cv,t):
    a,b=T[5],sb(5,2)
    c=cam(*cpath(t,[(a-.3,(960,560,1.0)),(b+.3,(960,560,1.08))]))
    put(cv,c,'t11_phu',960,520,s=.7)
    tagfall(cv,c,960,250,'Lý Tiến, thứ sử Nam Hán',t,a+.3,sz=44,col=RED)
    big(cv,'QUYỀN TỰ QUẢN KHÔNG CÒN',t,sb(5,1)+.2,b,INK,140,66,seed=5)
def S_5b(cv,t):
    a,b=sb(5,2),E[5]
    c=mcam(t,[(a-.4,(500,640,1.6)),(a+1.2,(440,820,2.6)),(b,(440,830,2.6))])
    mapbg(cv,c,u=1)
    dl,ac=P['daila'],P['aichau']
    dot(cv,c,*dl,o=1);tag(cv,c,dl[0]+16,dl[1]-20,'Đại La',dy=0,sz=24)
    dot(cv,c,*ac,o=inn(t,a+.5,.4));tag(cv,c,ac[0]+22,ac[1]-4,'Ái Châu',o=inn(t,a+.5,.4),dy=0,sz=24)
    lb(cv,c,'có một người chưa chịu',ac[0]+20,ac[1]+46,t,a+1.4,b+.3,col=RED,sz=26)
# ---------- 6. Dương Đình Nghệ
def S_6(cv,t):
    a,b=T[6],E[6]
    c=cam(*cpath(t,[(a-.3,(1500,540,1.0)),(sb(6,2),(1100,560,1.0)),(b+.3,(900,560,1.08))]))
    put(cv,c,'t11_luyen',1400,480,s=.9)
    tagfall(cv,c,1900,300,'Dương Đình Nghệ',t,a+.4,sz=44,col=INK,b=sb(6,2))
    lb(cv,c,'từng làm tướng dưới thời Khúc Hạo',1700,380,t,a+2.4,sb(6,1)-.2,col=RED,sz=34)
    lb(cv,c,'ba nghìn con nuôi, luyện võ, chiêu mộ hào kiệt',1300,200,t,sb(6,1)+.2,sb(6,2)-.2,col=INK,sz=38)
    big(cv,'SỬ KHÔNG GHI',t,sb(6,2)+.2,sb(6,3)-.2,RED,150,60,seed=6)
    lb(cv,c,'vì sao nhận con nuôi?',960,330,t,sb(6,2)+1.2,sb(6,3)-.2,sz=40)
    lb(cv,c,'gây dựng lực lượng',700,200,t,sb(6,3)+.2,sb(6,3)+(E[6]-sb(6,3))*.55,col=INK,sz=40)
    lb(cv,c,'rồi kéo quân ra bắc',1200,200,t,sb(6,3)+(E[6]-sb(6,3))*.5,E[6]+.3,col=RED,sz=40)
# ---------- 7. 931: vây Đại La, Lý Tiến chạy, Trần Bảo tới
def S_7(cv,t):
    a,b=T[7],E[7]
    c=mcam(t,[(a-.4,(470,720,1.7)),(sb(7,1)-.4,(900,520,1.1)),(b,(960,540,1.0))])
    mapbg(cv,c,u=1)
    dl,ac,qc=P['daila'],P['aichau'],P['quangchau']
    dot(cv,c,*dl,o=1);tag(cv,c,dl[0]+16,dl[1]-20,'Đại La',dy=0,sz=26)
    dot(cv,c,*ac,o=1);tag(cv,c,ac[0]+20,ac[1],'Ái Châu',dy=0,sz=24)
    dot(cv,c,*qc,o=1);tag(cv,c,qc[0]-60,qc[1]+40,'Quảng Châu',dy=0,sz=24)
    seal(cv,'s931',1500,300,a+.2,t,s=.8,r=-4)
    stroke(cv,c,[ac,(380,720),dl],inn(t,a+.4,sb(7,1)-a-.6),wid=10,col=INK)
    lb(cv,c,'Dương Đình Nghệ vây thành',420,560,t,a+1.2,sb(7,1)+.5,sz=26)
    if t>sb(7,1):
        stroke(cv,c,[dl,(800,480),(1250,330),qc],inn(t,sb(7,1)+.2,2.2),wid=8,col=RED,dash=14)
        lb(cv,c,'Lý Tiến bỏ chạy về nước',860,460,t,sb(7,1)+.6,sb(7,2),col=RED,sz=26)
    if t>sb(7,2):
        stroke(cv,c,[qc,(1250,330),(800,480),pt('daila',40,-6)],inn(t,sb(7,2)+.2,2.0),wid=10,col=RED)
        lb(cv,c,'Trần Bảo đem quân cứu viện',1100,310,t,sb(7,2)+.4,E[7]+.3,col=RED,sz=28)
        lb(cv,c,'thành đã đổi chủ',dl[0]+120,dl[1]+60,t,sb(7,2)+2.6,E[7]+.3,col=INK,sz=28)
# ---------- 8. người vây thành thành người bị vây
def S_8(cv,t):
    a,b=T[8],E[8];tc=sb(8,2)
    sh=fio(t,tc,tc+3.2)
    c=cam(*cpath(t,[(a-.3,(960,560,1.0)),(sb(8,1),(960,560,1.03)),(tc+3.0,(960,570,1.12))]),sx=4*math.sin(t*23)*sh,sy=3*math.sin(t*19)*sh)
    put(cv,c,'t11_thanh',960,470,s=.68)
    for i in range(9):   # quân vây ngoài tường
        xl=150+i*70;xr=1300+i*70
        for xx in (xl,xr):
            put(cv,c,'fig_quan',xx+(i%2)*12,650+(i%3)*12,ay=1,s=.42,o=inn(t,a+.1+i*.07,.4)*(1-inn(t,tc+1.5,.8)*.8))
    lb(cv,c,'Trần Bảo vây chặt Đại La',960,170,t,a+.2,sb(8,1)-.1,col=RED,sz=42)
    big(cv,'NGƯỜI VÂY THÀNH, THÀNH NGƯỜI BỊ VÂY',t,sb(8,1)+.1,tc-.3,INK,150,58,seed=8)
    if t>tc-.2:
        for i in range(12):
            st=tc+i*.12;u=inn(t,st,1.5)
            xs=960+(-1 if i%2 else 1)*lerp(0,150+i*45,u)
            put(cv,c,'fig_giap_giao',xs,650+(i%3)*10,ay=1,s=.45,o=inn(t,st,.2))
        sparks(cv,c,t,[(700,610),(820,620),(1100,610),(1220,620)],tc+.4,E[8],seed=8)
        tagfall(cv,c,1180,330,'Trần Bảo',t,tc+.2,fall=E[8]-.9,sz=44,col=RED)
        lb(cv,c,'đánh ra từ trong thành',960,170,t,tc+.3,E[8]+.3,col=INK,sz=40)
# ---------- 9. phân tích vị thế hai bên
def S_9(cv,t):
    a,b=T[9],E[9]
    c=cam(*cpath(t,[(a-.3,(960,560,1.0)),(b+.3,(960,560,1.06))]))
    put(cv,c,'t11_thanh',960,470,s=.68)
    big(cv,'NHÌN VỊ TRÍ HAI BÊN',t,a+.1,sb(9,1)-.2,RED,150,78,seed=9)
    for i in range(9): put(cv,c,'fig_quan',150+i*70,650,ay=1,s=.42,o=.9);put(cv,c,'fig_quan',1300+i*70,650,ay=1,s=.42,o=.9)
    lb(cv,c,'tường thành ở sau lưng',960,200,t,sb(9,1)+.3,sb(9,1)+(sb(9,2)-sb(9,1))*.5,col=INK,sz=42)
    lb(cv,c,'đánh vào một thành đã mất',500,560,t,sb(9,1)+(sb(9,2)-sb(9,1))*.45,sb(9,2)-.2,col=RED,sz=36)
    big(cv,'VÌ SAO ĐÁNH RA? NGUỒN KHÔNG NÓI',t,sb(9,2)+.2,b,RED,150,58,seed=10)
# ---------- 10. Tiết độ sứ
def S_10(cv,t):
    a,b=T[10],E[10]
    c=cam(*cpath(t,[(a-.3,(960,560,1.0)),(b+.3,(960,560,1.08))]))
    put(cv,c,'t11_phu',960,520,s=.7)
    seal(cv,'s931',1560,250,a+.4,t,s=.7,r=-4)
    tagfall(cv,c,960,250,'Tiết độ sứ',t,a+.5,sz=52,col=RED)
    lb(cv,c,'giữ cái chức mà họ Khúc từng giữ',960,330,t,a+2.2,sb(10,1)-.2,col=INK,sz=38)
    lb(cv,c,'nối vào đường họ Khúc đã đi',960,330,t,sb(10,1)+.2,b+.3,col=RED,sz=40)
    lb(cv,c,'chưa đặt một chức vị mới',960,990,t,sb(10,1)+1.6,b+.3,sz=34)
# ---------- 11. Kiều Công Tiễn
def S_11(cv,t):
    a,b=T[11],E[11]
    c=cam(*cpath(t,[(a-.3,(960,560,1.0)),(b+.3,(960,560,1.07))]))
    put(cv,c,'t11_phu',960,520,s=.7)
    seal(cv,'s937',1560,250,a+.2,t,s=.7,r=4)
    tagfall(cv,c,1200,300,'Kiều Công Tiễn',t,a+.5,sz=44,col=RED)
    x=lerp(1700,1060,inn(t,a+3.0,3.0));put(cv,c,Af('fig_satthu'),x,640,ay=1,s=.5,o=inn(t,a+2.8,.5)*(1-inn(t,sb(11,1)-.3,.6)))
    lb(cv,c,'tháng ba, người dưới quyền ra tay',960,160,t,a+1.2,sb(11,1)-.2,col=INK,sz=38)
    lb(cv,c,'chức vị từng đưa ông lên cũng khiến người dưới quyền ra tay',960,160,t,sb(11,1)+.2,b+.3,col=RED,sz=36)
# ---------- 12. Ngô Quyền
def S_12(cv,t):
    a,b=T[12],E[12]
    c=mcam(t,[(a-.4,(440,820,2.2)),(sb(12,1),(480,720,1.5)),(sb(12,2),(1000,420,1.15)),(sb(12,3),(560,640,1.6)),(b,(500,650,1.7))])
    mapbg(cv,c,u=1)
    dl,ac,qc=P['daila'],P['aichau'],P['quangchau']
    dot(cv,c,*dl,o=1);tag(cv,c,dl[0]+16,dl[1]-20,'Đại La',dy=0,sz=26)
    dot(cv,c,*ac,o=1);tag(cv,c,ac[0]+20,ac[1]-4,'Ái Châu',dy=0,sz=26)
    seal(cv,'s934',1500,300,a+.3,t,s=.8,r=-4)
    lb(cv,c,'Ngô Quyền, con rể',ac[0]+20,ac[1]+40,t,a+.3,sb(12,1)-.2,col=INK,sz=26)
    if t>sb(12,1):
        stroke(cv,c,[ac,(380,720),dl],inn(t,sb(12,1)+.2,2.4),wid=10,col=INK)
        lb(cv,c,'kéo ra bắc đánh Kiều Công Tiễn',330,690,t,sb(12,1)+.6,sb(12,2)-.2,sz=26)
    if t>sb(12,2):
        qo=inn(t,sb(12,2)+.2,.5)*(1-inn(t,sb(12,3)-.3,.5))
        dot(cv,c,*qc,o=qo);tag(cv,c,qc[0]-60,qc[1]+40,'Quảng Châu',o=qo,dy=0,sz=24)
        stroke(cv,c,[dl,(800,480),(1250,330),qc],inn(t,sb(12,2)+.4,2.2),wid=7,col=RED,dash=14,o=qo)
        lb(cv,c,'có sách chép: cầu cứu Nam Hán; có sách không chép',900,440,t,sb(12,2)+.8,sb(12,3)-.2,col=RED,sz=26)
    if t>sb(12,3):
        lb(cv,c,'các nguồn đều nói: diệt Kiều Công Tiễn ở Đại La',dl[0]+300,dl[1]-90,t,sb(12,3)+.4,b+.3,col=INK,sz=28)
# ---------- 13. Bạch Đằng
def wl13(t): return 640+(895-640)*inn(t,sb(13,3),(E[13]-sb(13,3))*.7)
def boats13(t):
    a=sb(13,2);out=[]
    for i in range(5):
        x0=2050+i*170;xe=900+i*110;ye=wl13(t)+40+(i%3)*18
        if t<a: x=2300
        else: x=lerp(x0,xe,eo((t-a)/(sb(13,3)-a+.2)))
        sink=cl((t-sb(13,4)-.4-i*.5)/1.6)
        r=lerp(math.sin(t*1.5+i)*1.5,18+i*5,inn(t,sb(13,3)+.8,2.0))
        out.append(dict(x=x,y=ye+sink*55,s=.62+(i%3)*.08,r=r,o=1-sink*.9,flip=True))
    return out
def S_13a(cv,t):
    a,b=T[13],sb(13,1)
    c=mcam(t,[(a-.4,(1200,560,1.1)),(a+1.8,(900,420,1.15)),(b,(640,600,1.5))])
    mapbg(cv,c,u=1)
    qc,hm,bd=P['quangchau'],P['haimon'],P['bachdang']
    dot(cv,c,*qc,o=1);tag(cv,c,qc[0]-60,qc[1]+40,'Quảng Châu',dy=0,sz=24)
    dot(cv,c,*bd,o=1);tag(cv,c,bd[0]+20,bd[1]-10,'cửa sông Bạch Đằng',dy=0,sz=24)
    stroke(cv,c,[qc,hm,(850,520),bd],inn(t,a+.4,sb(13,1)-a-1.0),wid=10,col=RED)
    lb(cv,c,'thủy quân Nam Hán, Lưu Hoằng Tháo chỉ huy',1150,360,t,a+.8,b+.3,col=RED,sz=28)
def S_13b(cv,t):
    a,b=sb(13,1),E[13];tl=sb(13,3);sh=fio(t,sb(13,3),sb(13,4))
    c=cam(*cpath(t,[(a-.3,(1100,560,1.0)),(sb(13,2),(1160,640,1.12)),(tl,(1100,760,1.3)),(sb(13,4),(1100,780,1.3)),(b+.3,(1000,740,1.2))]),sx=3*math.sin(t*31)*sh,sy=2*math.sin(t*27)*sh)
    wl=wl13(t)
    river(cv,c,t,PAP,wl=wl,clx=-330,boats=boats13(t),viet=[],under=.04*inn(t,sb(13,2),2),stakes=t>sb(13,1)+.5,dark=.06)
    put(cv,c,'t11_cua',960,420,s=.7,o=.0)
    lb(cv,c,'cọc gỗ bịt sắt',1100,360,t,a+.5,sb(13,2)-.2,col=RED,sz=40)
    lb(cv,c,'thủy triều lên, cọc chìm dưới nước',1100,330,t,sb(13,2)+.2,tl-.2,col=INK,sz=40)
    lb(cv,c,'thủy triều rút, cọc nhô lên chặn đường',1100,330,t,tl+.2,sb(13,4)-.2,col=RED,sz=40)
    if t>tl-.5: arrows(cv,c,t,tl+.6,sb(13,4)+.4,[(420,520),(520,500),(380,560)],[(1000,700),(1100,720),(1200,700)],n=10,h=60,per=.9,seed=13)
    if tl+.6<t<E[13]:
        o=fio(t,tl+.6,E[13]+.5,.5);gx,gy=W-110,600
        put_screen(cv,A('gauge'),gx,gy,o*.9,s=.45)
        yy=gy-140+280*(wl-640)/(895-640)
        stroke(cv,Cam(960,540,1,W,H),[(gx-70,yy),(gx-24,yy)],1,wid=5,col=RED,o=o)
        put_screen(cv,text('thủy triều',26,INK,700,glow=3),gx,gy+170,o)
    if t>sb(13,4): lb(cv,c,'Lưu Hoằng Tháo bị giết, vua Nam Hán rút quân',1100,330,t,sb(13,4)+.4,b+.3,col=RED,sz=36)
    seal(cv,'s938',W-300,330,sb(13,4)+.8,t,s=1.0)
# ---------- 14. kết: hai trận cách nhau bảy năm
def S_14(cv,t):
    a,b=T[14],E[14]
    c=mcam(t,[(a-.4,(560,600,1.5)),(sb(14,2),(520,620,1.6)),(b,(520,640,1.6))])
    mapbg(cv,c,u=1)
    dl,bd,ac=P['daila'],P['bachdang'],P['aichau']
    dot(cv,c,*dl,o=1);tag(cv,c,dl[0]-30,dl[1]-34,'Đại La',dy=0,sz=28)
    dot(cv,c,*bd,o=1);tag(cv,c,bd[0]+24,bd[1]-6,'Bạch Đằng',dy=0,sz=28)
    seal(cv,'s931',dl[0]-170,dl[1]+80,a+.5,t,s=.7,r=-4);seal(cv,'s938',bd[0]+260,bd[1]+10,a+2.2,t,s=.7,r=4)
    lb(cv,c,'một trận ở thành, một trận trên sông',520,330,t,a+.3,sb(14,1)-.2,col=INK,sz=32)
    lb(cv,c,'cả hai: quân Nam Hán thua, tướng cầm quân bị giết',520,330,t,sb(14,1)+.2,sb(14,2)-.2,col=RED,sz=32)
    lb(cv,c,'sử không nói Ngô Quyền có học từ cha vợ hay không',520,330,t,sb(14,2)+.2,sb(14,3)-.2,col=INK,sz=30)
    if t>sb(14,3):
        lb(cv,c,'cha vợ và con rể',520,330,t,sb(14,3)+.3,b+.3,col=RED,sz=40)
        stroke(cv,c,[ac,(380,720),dl],inn(t,sb(14,3)+.3,2.2),wid=8,col=INK)
def S_end(cv,t):
    a=E[14]-1.2
    c=cam(960,560,1.0+.012*(t-a))
    put(cv,c,'t11_cua',960,520,s=.7,o=.9);put(cv,c,'sun',1600,300,o=.5,k=.2);flock(cv,c,t,.6)
    tx=text('Năm 931 và năm 938, cha vợ và con rể',54,INK,700);put_screen(cv,wipe(tx,inn(t,a+.3,1.2),0,.3,seed=13),W/2,200)
    seal(cv,'stitle11',W/2,400,a+1.6,t,s=.55,r=3)
    put_screen(cv,text('Người Gác Sử',34,INK,600),W/2,H-80,inn(t,a+2.5,1))
S=lambda n:T[n]-.3
SB=lambda n,k:sb(n,k)-.3
SH=[(0,S(2),S_1),(S(2),S(3),S_2),(S(3),SB(3,1),S_3a),(SB(3,1),SB(3,2),S_3b),(SB(3,2),S(4),S_3c),(S(4),S(5),S_4),(S(5),SB(5,2),S_5a),(SB(5,2),S(6),S_5b),
 (S(6),S(7),S_6),(S(7),S(8),S_7),(S(8),S(9),S_8),(S(9),S(10),S_9),(S(10),S(11),S_10),(S(11),S(12),S_11),(S(12),S(13),S_12),(S(13),SB(13,1),S_13a),(SB(13,1),S(14),S_13b),
 (S(14),E[14]-1.2,S_14),(E[14]-1.2,V.TOTAL+1,S_end)]
_J=json.load(open('/tmp/pc/ke-hoach/thu-giong-hai/tm11m_full.json'))
SENT={}
for _i,_d in enumerate(_J):
    _hs=[x for x in re.split(r'(?<=[.!?])\s+',_d['hien']) if x.strip()]
    SENT[_i+1]=_hs if len(_hs)==len(_SC[_i+1])-1 else [_d['hien']]
def caps(cv,t):
    for n,hs in SENT.items():
        for k,h in enumerate(hs):
            a=sb(n,k) if len(hs)>1 else T[n];b=sb(n,k+1) if len(hs)>1 else E[n]
            if a-.3<t<b+.35: caption(cv,h,inn(t,a-.25,.25)*(1-inn(t,b+.05,.25)),False)
def ov(cv,t):
    TT=T[2]
    if TT-4.2<t<TT+.2: title(cv,t,TT-3.6,'ĐẠI LA · 931','stitle11',.55)
    caps(cv,t)
V.NHAN={2:'Đại La – Hà Nội ngày nay',4:'Nam Hán – nước ở vùng Quảng Đông ngày nay',5:'Ái Châu – Thanh Hóa ngày nay',6:'Dương Đình Nghệ – tướng cũ của họ Khúc',12:'Ngô Quyền – con rể Dương Đình Nghệ'}
class _V2: pass
V2=_V2();V2.__dict__.update(V.__dict__);V2.TX={}   # phụ đề vẽ theo từng câu trong ov, không vẽ cả đoạn
def frame(t): return K.compose(V2,SH,t,ov,CARDS)
TOTAL=V.TOTAL
if __name__=='__main__': K.main(V,frame)
