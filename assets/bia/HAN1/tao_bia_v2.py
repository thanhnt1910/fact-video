"""Ảnh bìa dọc 1080x1920 tập 1 (kiểu đơn giản): bản đồ địa hình phủ khung, 9 chấm quận, thẻ HÁN, chữ lớn, logo kênh.
Chạy: python assets/bia/HAN1/tao_bia_v2.py [ra.png]. Logo: assets/logo/nguoi-gac-su.png (vuông 130 px, độ đậm 0,8, góc trên phải, cách mép phải 44 và mép trên 34)."""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
R = Path(__file__).resolve().parents[3]
out = sys.argv[1] if len(sys.argv) > 1 else str(Path(__file__).with_name('bia_v2.png'))
Q9 = [(113.26,23.13),(111.3,23.45),(109.6,23.1),(109.2,21.7),(106.3,21.3),(105.8,19.8),(105.6,18.7),(110.3,19.9),(109.6,19.3)]
S = 0.46; LON0, LAT0 = 103.2, 27.0   # tỉ lệ ảnh; góc trái-trên của khung theo kinh vĩ
ox = -(LON0-102)*239.4*S; oy = -(30.5-LAT0)*260*S
dots = ''.join(f'<g transform="translate({(lo-102)*239.4*S+ox:.0f},{(30.5-la)*260*S+oy:.0f})"><circle r="30" fill="#ff3b30" opacity=".25"/><circle r="17" fill="#fff"/><circle r="11" fill="#e0231a"/></g>' for lo, la in Q9)
html = f'''<!doctype html><meta charset=utf-8><style>
*{{margin:0}}body{{width:1080px;height:1920px;position:relative;overflow:hidden;background:#06121f;font-family:"DejaVu Sans",sans-serif;font-weight:800}}
.map{{filter:brightness(1.45) saturate(1.35) contrast(1.05);position:absolute;left:{ox}px;top:{oy}px;width:{3542*S}px;height:{4420*S}px}}
.sh{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(6,12,20,.35) 0,rgba(6,12,20,0) 22%,rgba(6,12,20,0) 52%,rgba(6,12,20,.9) 74%,#06101a 100%)}}
.brush{{position:absolute;background:linear-gradient(90deg,#8e0f0a,#d7261c 40%,#b8160e);transform:skewX(-8deg);box-shadow:0 8px 30px rgba(0,0,0,.5)}}
.t{{position:absolute;left:0;width:1080px;text-align:center;font-style:italic;text-transform:uppercase;line-height:1;white-space:nowrap;-webkit-text-stroke:0;text-shadow:0 8px 0 rgba(0,0,0,.55),0 0 30px rgba(0,0,0,.6)}}
</style><body>
<img class=map src="file://{R}/phim_ban_do/doc9x16/map_relief.jpg">
<div class=sh></div>
<svg style="position:absolute;left:0;top:0" width=1080 height=1920>{dots}</svg>
<div class=brush style="left:30px;top:70px;width:520px;height:140px"></div>
<div class=t style="left:56px;top:92px;width:480px;font-size:92px;top:104px;color:#fff;text-align:center">110 TCN</div>
<div class=brush style="left:780px;top:215px;width:190px;height:96px;border:6px solid #fff;border-radius:10px;transform:rotate(-6deg)"></div>
<div class=t style="left:780px;top:237px;width:190px;font-size:54px;color:#fff;transform:rotate(-6deg)">HÁN</div>
<div class=brush style="left:20px;top:1120px;width:1060px;height:480px;opacity:.92;clip-path:polygon(2% 6%,100% 0,97% 100%,0 94%)"></div>
<div class=t style="top:1160px;font-size:158px;color:#fff;letter-spacing:-4px">CHÍN QUẬN</div>
<div class=t style="top:1340px;font-size:158px;color:#ffd21f;letter-spacing:-4px">RỒI SAO?</div>
<div class=brush style="left:60px;top:1665px;width:960px;height:96px;background:linear-gradient(90deg,#7c0d08,#c4201a 50%,#7c0d08)"></div>
<div class=t style="top:1688px;font-size:40px;color:#fff;letter-spacing:1px">CHUYỆN CAI TRỊ NGÀN NĂM · <span style="color:#ffd21f">TẬP 1</span></div>
<img src="file://{R}/assets/logo/nguoi-gac-su.png" style="position:absolute;right:44px;top:34px;width:130px;height:130px;opacity:.8">
</body>'''
tmp = Path(__file__).with_name('_bia_v2.html'); tmp.write_text(html, encoding='utf-8')
with sync_playwright() as p:
    br = p.chromium.launch(args=['--allow-file-access-from-files']); pg = br.new_page(viewport={'width': 1080, 'height': 1920})
    pg.goto('file://' + str(tmp)); pg.wait_for_timeout(800); pg.screenshot(path=out); br.close()
tmp.unlink(); print(out)
