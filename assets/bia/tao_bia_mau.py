"""MẪU ẢNH BÌA DỌC 1080x1920 (chủ kênh duyệt 06/11/2026, từ tập 1 "Chín quận"): bản đồ địa hình phủ kín, chấm điểm phát sáng, tiêu đề 2 dòng, chân trang thương hiệu.
Chạy: python assets/bia/tao_bia_mau.py <cau_hinh.json> [ra.png]   (mẫu cấu hình: assets/bia/HAN1/bia.json)
Cấu hình: the_nam (thẻ đỏ trên cùng), the_trieu (thẻ trắng nghiêng), d1 (dòng trắng), d2 (dòng vàng, thường là câu hỏi), phu (thẻ tên loạt), phu_vang (phần vàng của thẻ phụ),
chan_chinh (tên kênh), chan_phu (khẩu hiệu), diem (danh sách [kinh, vĩ]), lon0, scale, oy (khung bản đồ).
Quy tắc đã chốt: chữ chính nằm trong y 70-1560 (Facebook/TikTok che đáy); chân trang là thương hiệu, không để nền đen; logo vuông 130 px, độ đậm 0,8, góc trên phải (cách phải 44, trên 34).
Tiêu đề phông Oswald 700 cỡ ~206 px, viền là LỚP RIÊNG phía sau (không dùng text-stroke trên chữ chính vì ăn mất dấu), khung chữ có padding để không cắt dấu dưới (Ạ, Ị); luôn xem ảnh cắt ở cỡ lớn và bản thu 270x480 trước khi giao.
Phông (OFL) ở assets/bia/fonts."""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
R = Path(__file__).resolve().parents[2]; F = R / 'assets/bia/fonts'
import json
C = json.load(open(sys.argv[1], encoding='utf-8'))
out = sys.argv[2] if len(sys.argv) > 2 else str(Path(sys.argv[1]).with_name('bia.png'))
Q9 = C['diem']
SX = SY = C.get('scale', 0.50); LON0 = C.get('lon0', 105.2)
ox = -(LON0-102)*239.4*SX; oy = C.get('oy', -640)
dots = ''.join(f'<g transform="translate({(lo-102)*239.4*SX+ox:.0f},{(30.5-la)*260*SY+oy:.0f})"><circle r="46" fill="url(#g)"/><circle r="24" fill="none" stroke="#ffd45a" stroke-width="3" opacity=".8"/><circle r="13" fill="#fff6d6" stroke="#e8a317" stroke-width="5"/></g>' for lo, la in Q9)
html = f'''<!doctype html><meta charset=utf-8><style>
@font-face{{font-family:A;src:url(file://{F}/Anton-Regular.ttf)}}
@font-face{{font-family:O;font-weight:200 700;src:url(file://{F}/Oswald.ttf)}}
@font-face{{font-family:B;src:url(file://{F}/BeVietnamPro-ExtraBold.ttf)}}
@font-face{{font-family:BB;src:url(file://{F}/BeVietnamPro-Black.ttf)}}
*{{margin:0}}body{{width:1080px;height:1920px;position:relative;overflow:hidden;background:#0a1c30}}
.map{{position:absolute;left:{ox}px;top:{oy}px;width:{3542*SX}px;height:{4420*SY}px;-webkit-mask-image:linear-gradient(180deg,#000 0,#000 {1180-oy}px,transparent {1540-oy}px);filter:brightness(1.15) saturate(1.15) contrast(1.08)}}
.sh{{position:absolute;inset:0;background:
 radial-gradient(ellipse at 50% 66%,rgba(5,12,22,.62) 0,rgba(5,12,22,0) 62%),
 linear-gradient(180deg,rgba(5,12,22,.55) 0,rgba(5,12,22,0) 16%,rgba(5,12,22,0) 36%,rgba(5,12,22,.5) 60%,rgba(8,22,40,.78) 82%,rgba(10,26,46,.92) 100%)}}
.ab{{position:absolute;left:0;width:1080px;text-align:center;white-space:nowrap;text-transform:uppercase;line-height:1}}
.big{{font-family:O;font-weight:700;font-size:206px;letter-spacing:2px;padding:50px 0 60px;margin-top:-50px}}
.bk{{color:#2a0504;-webkit-text-stroke:16px #2a0504;filter:drop-shadow(0 10px 0 rgba(0,0,0,.5)) drop-shadow(0 0 30px rgba(220,40,25,.6))}}
.w{{background:linear-gradient(180deg,#fff 30%,#f3e6c8 100%);-webkit-background-clip:text;color:transparent}}
.y{{background:linear-gradient(180deg,#fff2a8 5%,#ffc928 45%,#f08a00 100%);-webkit-background-clip:text;color:transparent}}
.pill{{position:absolute;display:inline-block;font-family:B;color:#fff;letter-spacing:1px;border:3px solid #f2c14e;background:linear-gradient(180deg,#c3201a,#85100b);box-shadow:0 6px 22px rgba(0,0,0,.55);white-space:nowrap}}
.rule{{position:absolute;height:5px;background:linear-gradient(90deg,transparent,#f2c14e 20%,#fff2a8 50%,#f2c14e 80%,transparent)}}
</style><body>
<img class=map src="file://{R}/phim_ban_do/doc9x16/map_relief.jpg">
<div class=sh></div>
<svg style="position:absolute;left:0;top:0" width=1080 height=1920><defs><radialGradient id=g><stop offset="0" stop-color="#ff7a2a" stop-opacity=".95"/><stop offset=".45" stop-color="#ff4a1a" stop-opacity=".45"/><stop offset="1" stop-color="#ff3b1a" stop-opacity="0"/></radialGradient></defs>{dots}</svg>
<div class=pill style="left:36px;top:70px;font-size:70px;padding:12px 40px 8px;border-radius:14px;font-family:A;letter-spacing:3px">{C["the_nam"]}</div>
<div class=pill style="left:36px;top:190px;font-size:44px;padding:8px 30px;border-radius:12px;background:linear-gradient(180deg,#fff,#e9dcc0);color:#8d0f0a;border-color:#8d0f0a;transform:rotate(-3deg)">{C["the_trieu"]}</div>
<div class=rule style="left:90px;width:900px;top:900px"></div>
<div class="ab big bk" style="top:965px">{C["d1"]}</div>
<div class="ab big bk" style="top:1235px">{C["d2"]}</div>
<div class="ab big w" style="top:965px">{C["d1"]}</div>
<div class="ab big y" style="top:1235px">{C["d2"]}</div>
<div class=rule style="left:90px;width:900px;top:1478px"></div>
<div class=ab style="top:1505px"><span class=pill style="position:static;font-size:38px;padding:14px 40px;border-radius:40px;background:rgba(8,20,36,.82)">{C["phu"]} <span style="color:#ffd45a">{C["phu_vang"]}</span></span></div>
<div class=ab style="top:1640px;font-family:BB;font-size:64px;letter-spacing:10px;color:#f2e2b0;text-shadow:0 4px 18px rgba(0,0,0,.8)">{C["chan_chinh"]}</div>
<div class=rule style="left:200px;width:680px;top:1730px"></div>
<div class=ab style="top:1752px;font-family:B;font-size:32px;letter-spacing:3px;color:#d9c89a;text-shadow:0 3px 12px rgba(0,0,0,.8)">{C["chan_phu"]}</div>
<img src="file://{R}/assets/logo/nguoi-gac-su.png" style="position:absolute;right:44px;top:34px;width:130px;height:130px;opacity:.8">
</body>'''
tmp = Path(__file__).with_name('_bia_tmp.html'); tmp.write_text(html, encoding='utf-8')
with sync_playwright() as p:
    br = p.chromium.launch(args=['--allow-file-access-from-files']); pg = br.new_page(viewport={'width': 1080, 'height': 1920})
    pg.goto('file://' + str(tmp)); pg.wait_for_timeout(1200); pg.screenshot(path=out); br.close()
tmp.unlink(); print(out)
