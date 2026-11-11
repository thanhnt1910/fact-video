"""Ảnh bìa dọc 1080x1920 loạt Bí mật biểu tượng #09-#14 (xen kẽ v4), mẫu giấy xé của VN8. python assets/bia/XK/tao_bia.py <mã 1-6> [ra.png]
Chữ chính trong y 70-1560, logo cây đèn 130 px độ đậm 0,8 góc trên phải (cách mép phải 44, mép trên 34)."""
import sys, random
from pathlib import Path
from playwright.sync_api import sync_playwright
R = Path(__file__).resolve().parents[3]; F = R / 'assets/bia/fonts'
K = sys.argv[1]
CFG = {
 '1': dict(img='xk1/cd5.jpg', pos='50% 55%', num='#09', stamp='1835', tag='CỬU ĐỈNH CUNG ĐÌNH HUẾ', l1='9 CHIẾC ĐỈNH ĐỒNG', l2='KHẮC CẢ NƯỚC VIỆT'),
 '2': dict(img='xk2/ds5.jpg', pos='50% 50%', num='#10', stamp='?', tag='NGUỒN GỐC DẤU ĐÔ LA', l1='DẤU $ RA ĐỜI', l2='AI VẼ RA NÓ?'),
 '3': dict(img='xk3/ts1.jpg', pos='50% 18%', num='#11', stamp='1886', tag='TƯỢNG NỮ THẦN TỰ DO', l1='QUÀ KỶ NIỆM', l2='100 NĂM NƯỚC MỸ'),
 '4': dict(img='xk4/hd9.jpg', pos='50% 50%', num='#12', stamp='1407', tag='HỒ NGUYÊN TRỪNG', l1='SÚNG THẦN CƠ', l2='CỦA CON HỒ QUÝ LY'),
 '5': dict(img='xk5/ha6.jpg', pos='50% 50%', num='#13', stamp='1719', tag='CHÙA CẦU HỘI AN', l1='CẦU CÓ MÁI CHE', l2='CÓ CẢ CHÙA TRÊN CẦU'),
 '6': dict(img='xk6/rs5.jpg', pos='50% 50%', num='#14', stamp='1799', tag='PHIẾN ĐÁ ROSETTA', l1='TẢNG ĐÁ LÍNH PHÁP', l2='ĐỌC ĐƯỢC CHỮ AI CẬP'),
 '7': dict(img='xk7/lb12.jpg', pos='62% 60%', num='#15', stamp='1902', tag='HÀ NỘI · SÔNG HỒNG', l1='CẦU LONG BIÊN', l2='EIFFEL CÓ KÝ TÊN?', chu_the='cầu Long Biên', hook=dict(cx=610, cy=590, r=190, q='?')),
 '8': dict(img='xk8/ha7.jpg', pos='50% 50%', num='#13', stamp='1719', tag='CHÙA CẦU · HỘI AN', l1='CẦU MÀ GỌI LÀ', l2='CHÙA CẦU?', chu_the='chùa Cầu Hội An', hook=dict(cx=540, cy=560, r=170, q='?')),
 '9': dict(img='xk9/ef1.jpg', pos='50% 35%', num='#16', stamp='1889', tag='PARIS · THÁP EIFFEL', l1='THÁP EIFFEL', l2='CHỈ ĐỨNG 20 NĂM?', chu_the='tháp Eiffel', hook=dict(cx=540, cy=470, r=180, q='?')),
 '10': dict(img='xk10/tc2.jpg', pos='50% 40%', num='#17', stamp='210 TCN', tag='TÂY AN · TRUNG QUỐC', l1='ĐẦU TƯỢNG ĐẤT NUNG', l2='BỊ VỨT NGOÀI ĐỒNG?', chu_the='tượng lính đất nung', hook=dict(cx=540, cy=560, r=200, q='?')),
 '11': dict(img='xk11/cc1.jpg', pos='35% 50%', num='#18', stamp='1812', tag='HÀ NỘI · THÀNH CỔ', l1='CỘT CỜ HÀ NỘI', l2='CỜ BỊ GIÓ XÉ?', chu_the='cột cờ Hà Nội', hook=dict(cx=300, cy=440, r=170, q='?')),
 '12': dict(img='xk12/mc1.jpg', pos='45% 50%', num='#19', stamp='1954', tag='HÀ NỘI · CHÙA MỘT CỘT', l1='CHÙA MỘT CỘT', l2='TỪNG BỊ NỔ TUNG?', chu_the='chùa Một Cột', hook=dict(cx=540, cy=560, r=190, q='?')),
}[K]
def fs(t): return round(118*min(1, 16/len(t)))
out = sys.argv[2] if len(sys.argv) > 2 else str(Path(__file__).with_name(f'bia_xk{K}.png'))
def jag(w, h, seed, amp=7, step=34):
    r = random.Random(seed); P = []
    def side(x0, y0, x1, y1):
        L = ((x1-x0)**2+(y1-y0)**2)**.5; n = max(2, round(L/step))
        for i in range(n):
            u = i/n; P.append((x0+(x1-x0)*u+(r.random()-.5)*amp*2, y0+(y1-y0)*u+(r.random()-.5)*amp*2))
    side(0,0,w,0); side(w,0,w,h); side(w,h,0,h); side(0,h,0,0)
    return 'polygon('+','.join(f'{x:.1f}px {y:.1f}px' for x,y in P)+')'
CW, CH = 1000, 740
H = CFG.get('hook')
HOOK = (f"<div class=hook style='left:{H['cx']-H['r']}px;top:{H['cy']-H['r']}px;width:{2*H['r']}px;height:{2*H['r']}px'></div><div class=q style='left:{H['cx']+H['r']-90}px;top:{H['cy']-H['r']-40}px'>{H['q']}</div>" if H else '')
html = f'''<!doctype html><meta charset=utf-8><style>
@font-face{{font-family:A;src:url(file://{F}/Anton-Regular.ttf)}}
@font-face{{font-family:O;font-weight:200 700;src:url(file://{F}/Oswald.ttf)}}
@font-face{{font-family:B;src:url(file://{F}/BeVietnamPro-ExtraBold.ttf)}}
*{{margin:0}}body{{width:1080px;height:1920px;position:relative;overflow:hidden;background:#141312}}
.news{{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 40%,#2a2218,#141312 75%)}}
.vg{{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 45%,rgba(0,0,0,0) 55%,rgba(0,0,0,.8) 100%)}}
.card{{position:absolute;left:40px;top:190px;width:{CW}px;height:{CH}px;transform:rotate(-2deg);filter:drop-shadow(0 18px 20px rgba(0,0,0,.7))}}
.card .bd{{position:absolute;inset:-12px;background:#eee7d3;clip-path:{jag(CW+24,CH+24,3)}}}
.card .im{{position:absolute;inset:0;clip-path:{jag(CW,CH,9,5)};background:url(file://{R}/assets/{CFG['img']}) {CFG['pos']}/cover no-repeat;filter:contrast(1.14) saturate(1.22) brightness(1.03)}}
.tape{{position:absolute;left:420px;top:-30px;width:170px;height:48px;background:rgba(236,226,180,.6);transform:rotate(-5deg)}}
.pill{{position:absolute;left:36px;top:60px;font-family:B;font-size:34px;color:#fff;letter-spacing:1px;padding:12px 30px 10px;background:#d8372d;clip-path:{jag(560,64,5,3,30)};width:560px;box-sizing:border-box;transform:rotate(-2deg)}}
.stamp{{position:absolute;right:46px;top:790px;font-family:A;font-size:120px;color:#e5483f;letter-spacing:4px;padding:6px 34px 0;border:10px solid #e5483f;border-radius:12px;background:rgba(20,10,8,.55);transform:rotate(7deg)}}
.ab{{position:absolute;left:0;width:1080px;text-align:center;white-space:nowrap;text-transform:uppercase;line-height:1}}
.big{{font-family:O;font-weight:700;font-size:118px;letter-spacing:2px;padding:50px 0 60px;margin-top:-50px}}
.bk{{color:#2a0504;-webkit-text-stroke:18px #2a0504;filter:drop-shadow(0 10px 0 rgba(0,0,0,.5))}}
.w{{background:linear-gradient(180deg,#fff 30%,#f3e6c8 100%);-webkit-background-clip:text;color:transparent}}
.y{{background:linear-gradient(180deg,#fff2a8 5%,#ffc928 45%,#f08a00 100%);-webkit-background-clip:text;color:transparent}}
.tag{{position:absolute;left:60px;top:950px;font-family:B;font-size:34px;color:#17120c;background:#efe9d8;padding:12px 24px 8px;clip-path:{jag(600,64,7,3,30)};width:600px;box-sizing:border-box;transform:rotate(-3deg);text-align:center}}
.hook{{position:absolute;border:12px solid #e5483f;border-radius:50%;box-shadow:0 0 0 6px rgba(20,10,8,.55),0 0 40px rgba(229,72,63,.8);transform:rotate(-2deg)}}
.q{{position:absolute;font-family:A;font-size:104px;line-height:132px;color:#fff;background:#e5483f;width:150px;height:150px;border-radius:50%;text-align:center;padding-top:0;box-sizing:border-box;border:8px solid #fff;filter:drop-shadow(0 8px 10px rgba(0,0,0,.6))}}
.rule{{position:absolute;left:140px;width:800px;height:5px;background:linear-gradient(90deg,transparent,#f2c14e 20%,#fff2a8 50%,#f2c14e 80%,transparent)}}
</style><body>
<div class=news></div><div class=vg></div>
<div class=card><div class=bd></div><div class=im></div><div class=tape></div></div>
{HOOK}
<div class=pill>BÍ MẬT BIỂU TƯỢNG · {CFG['num']}</div>
<div class=stamp>{CFG['stamp']}</div>
<div class=tag>{CFG['tag']}</div>
<div class="ab big bk" style="top:1085px;font-size:{fs(CFG['l1'])}px">{CFG['l1']}</div><div class="ab big w" style="top:1085px;font-size:{fs(CFG['l1'])}px">{CFG['l1']}</div>
<div class="ab big bk" style="top:1240px;font-size:{fs(CFG['l2'])}px">{CFG['l2']}</div><div class="ab big y" style="top:1240px;font-size:{fs(CFG['l2'])}px">{CFG['l2']}</div>
<div class=rule style="top:1640px"></div>
<div class=ab style="top:1665px;font-family:B;font-size:50px;color:#f1e9d2;letter-spacing:6px">NGƯỜI GÁC SỬ</div>
<div class=ab style="top:1740px;font-family:B;font-size:28px;color:#f2c14e;letter-spacing:5px">LỊCH SỬ THEO CHÍNH SỬ</div>
<img src="file://{R}/assets/logo/nguoi-gac-su.png" style="position:absolute;left:906px;top:34px;width:130px;height:130px;opacity:.8">
'''
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width':1080,'height':1920})
    h = Path(out).with_suffix('.html'); h.write_text(html, encoding='utf-8')
    pg.goto('file://' + str(h)); pg.wait_for_timeout(1500); pg.screenshot(path=out); b.close(); h.unlink()
print(out)
