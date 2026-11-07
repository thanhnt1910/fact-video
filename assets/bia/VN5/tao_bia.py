"""Ảnh bìa dọc 1080x1920 cho VN5 (Bí mật biểu tượng #05): kiểu giấy xé giống video. python assets/bia/VN5/tao_bia.py [ra.png]
Chữ chính trong y 70-1560, logo cây đèn 130 px độ đậm 0,8 góc trên phải (cách mép phải 44, mép trên 34)."""
import sys, random
from pathlib import Path
from playwright.sync_api import sync_playwright
R = Path(__file__).resolve().parents[3]; F = R / 'assets/bia/fonts'
out = sys.argv[1] if len(sys.argv) > 1 else str(Path(__file__).with_name('bia.png'))
def jag(w, h, seed, amp=7, step=34):
    r = random.Random(seed); P = []
    def side(x0, y0, x1, y1):
        L = ((x1-x0)**2+(y1-y0)**2)**.5; n = max(2, round(L/step))
        for i in range(n):
            u = i/n; P.append((x0+(x1-x0)*u+(r.random()-.5)*amp*2, y0+(y1-y0)*u+(r.random()-.5)*amp*2))
    side(0,0,w,0); side(w,0,w,h); side(w,h,0,h); side(0,h,0,0)
    return 'polygon('+','.join(f'{x:.1f}px {y:.1f}px' for x,y in P)+')'
CW, CH = 1000, 740
html = f'''<!doctype html><meta charset=utf-8><style>
@font-face{{font-family:A;src:url(file://{F}/Anton-Regular.ttf)}}
@font-face{{font-family:O;font-weight:200 700;src:url(file://{F}/Oswald.ttf)}}
@font-face{{font-family:B;src:url(file://{F}/BeVietnamPro-ExtraBold.ttf)}}
*{{margin:0}}body{{width:1080px;height:1920px;position:relative;overflow:hidden;background:#141312}}
.news{{position:absolute;inset:0;background:repeating-linear-gradient(180deg,transparent 0 38px,#1d1c1a 38px 48px);opacity:.9}}
.vg{{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 45%,rgba(0,0,0,0) 55%,rgba(0,0,0,.8) 100%)}}
.card{{position:absolute;left:40px;top:190px;width:{CW}px;height:{CH}px;transform:rotate(-2deg);filter:drop-shadow(0 18px 20px rgba(0,0,0,.7))}}
.card .bd{{position:absolute;inset:-12px;background:#eee7d3;clip-path:{jag(CW+24,CH+24,3)}}}
.card .im{{position:absolute;inset:0;clip-path:{jag(CW,CH,9,5)};background:url(file://{R}/assets/bia/VN5/nen.jpg) 50% 50%/cover no-repeat}}
.tape{{position:absolute;left:420px;top:-30px;width:170px;height:48px;background:rgba(236,226,180,.6);transform:rotate(-5deg)}}
.pill{{position:absolute;left:36px;top:60px;font-family:B;font-size:34px;color:#fff;letter-spacing:1px;padding:12px 30px 10px;background:#d8372d;clip-path:{jag(560,64,5,3,30)};width:560px;box-sizing:border-box;transform:rotate(-2deg)}}
.stamp{{position:absolute;right:46px;top:790px;font-family:A;font-size:120px;color:#e5483f;letter-spacing:4px;padding:6px 34px 0;border:10px solid #e5483f;border-radius:12px;background:rgba(20,10,8,.55);transform:rotate(7deg)}}
.ab{{position:absolute;left:0;width:1080px;text-align:center;white-space:nowrap;text-transform:uppercase;line-height:1}}
.big{{font-family:O;font-weight:700;font-size:150px;letter-spacing:2px;padding:50px 0 60px;margin-top:-50px}}
.bk{{color:#2a0504;-webkit-text-stroke:18px #2a0504;filter:drop-shadow(0 10px 0 rgba(0,0,0,.5))}}
.w{{background:linear-gradient(180deg,#fff 30%,#f3e6c8 100%);-webkit-background-clip:text;color:transparent}}
.y{{background:linear-gradient(180deg,#fff2a8 5%,#ffc928 45%,#f08a00 100%);-webkit-background-clip:text;color:transparent}}
.tag{{position:absolute;left:60px;top:950px;font-family:B;font-size:34px;color:#17120c;background:#efe9d8;padding:12px 24px 8px;clip-path:{jag(600,64,7,3,30)};width:600px;box-sizing:border-box;transform:rotate(-3deg);text-align:center}}
.rule{{position:absolute;left:140px;width:800px;height:5px;background:linear-gradient(90deg,transparent,#f2c14e 20%,#fff2a8 50%,#f2c14e 80%,transparent)}}
</style><body>
<div class=news></div><div class=vg></div>
<div class=card><div class=bd></div><div class=im></div><div class=tape></div></div>
<div class=pill>BÍ MẬT BIỂU TƯỢNG · #05</div>
<div class=stamp>CỔ LOA</div>
<div class=tag>THÀNH ỐC CỔ LOA</div>
<div class="ab big bk" style="top:1040px">9 VÒNG XOÁY</div><div class="ab big w" style="top:1040px">9 VÒNG XOÁY</div>
<div class="ab big bk" style="top:1242px">CHỈ 3 VÒNG?</div><div class="ab big y" style="top:1242px">CHỈ 3 VÒNG?</div>
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
