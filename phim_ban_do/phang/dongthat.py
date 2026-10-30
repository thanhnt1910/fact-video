"""Demo chuyển động thật: chèo thuyền, nước chảy, quân bước đi. python phim_ban_do/phang/dongthat.py <chay|hanh|ghep>"""
import sys, pathlib, subprocess, random
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import chitiet
from chitiet import *   # noqa
from playwright.sync_api import sync_playwright

FPS, DUR = 24, 8.0
T_ROW = 2.4


def waves(y, amp, per, col, op, sw=3, n=None, seed=1, h=140):
    """Dải sóng lặp kín: rộng hơn khung 2 chu kỳ, dịch đúng 1 chu kỳ là liền mạch."""
    r = random.Random(seed); o = ''
    for row in range(3):
        yy = y + row * h / 3
        d = f'M{-2*per},{yy}'
        for k in range(int(1920 / per) + 4):
            d += f' q{per/4},{-amp*(0.6+0.5*r.random()) if row%2==0 else -amp} {per/2},0 t{per/2},0'
        o += f'<path d="{d}" stroke="{col}" stroke-width="{sw}" fill="none" opacity="{op}"/>'
    return o


def rowing_scene():
    L = outdoor('dawn', sun=(1500, 480), cl=38, mt=700)
    L.append(G('far', ''.join(f'<g class="far">{boat2(x, 780 + k % 2 * 6, .38, col="#5a3a22", oars=False)[0]}{boat2(x, 780 + k % 2 * 6, .38, col="#5a3a22", oars=False)[1]}</g>' for k, x in enumerate((420, 1480, 1900)))))
    L.append(G('riverbase', '<defs><linearGradient id="rvg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e6a49f"/><stop offset="1" stop-color="#7a86a8"/></linearGradient></defs><rect y="740" width="1920" height="340" fill="url(#rvg)"/>'))
    L.append(sunpath(1500, 745, 1070))
    L.append(G('w1', waves(770, 5, 150, '#fff', .35, 2.4, seed=1)))
    L.append(G('w2', waves(840, 8, 220, '#fff', .38, 3, seed=2)))
    L.append(G('foam', ''.join(f'<ellipse class="foam" cx="{700-k*120}" cy="{936+(k%2)*8}" rx="{60-k*5}" ry="6" fill="#fff" opacity=".6"/>' for k in range(5))))
    bb, bf = boat2(960, 920, 2.1, oars=False)
    L.append(bb)
    L.append(G('staff', '<line x1="640" y1="870" x2="640" y2="520" stroke="#6b4a2a" stroke-width="8"/><path class="pen" d="M640,530 q52,10 92,-4 q-10,34 -28,70 q-30,-20 -64,-26Z" fill="#c0392b"/>'))
    L.append(sit('DTN', 840, 862, 1.7, pose='hands'))
    L.append(sit('OFF1', 1100, 862, 1.7, pose='hands', col='#6a5a3a', turban=None, crown='headband', beard='white_goatee', seed=175))
    L.append(bf)
    # mái chèo bên gần: trục xoay ở mạn thuyền
    for px in (840, 1100):
        L.append(f'<g transform="translate({px},868)"><g class="oar" data-px="{px}" data-py="868"><line x1="-62" y1="-52" x2="128" y2="106" stroke="#4a3220" stroke-width="9" stroke-linecap="round"/><line x1="-62" y1="-52" x2="128" y2="106" stroke="#8a6a44" stroke-width="3"/>'
                 f'<path d="M112,92 l40,32 l-12,14 l-40,-32Z" fill="#a98a5a" stroke="#4a3220" stroke-width="2"/><circle cx="0" cy="0" r="7" fill="#d8b04a"/></g></g>')
        L.append(f'<ellipse class="splash" cx="{px+150}" cy="{868+128}" rx="42" ry="7" fill="#fff" opacity="0"/>')
    L.append(G('bankL', '<path d="M0,1080 L0,930 Q200,880 420,930 L520,1080Z" fill="#4a5a3a"/>' + reeds(20, 1000, 14, 220)[0:0] ))
    L.append(reeds(20, 1000, 14, 220)); L.append(reeds(1640, 1010, 16, 200))
    L.append(birds(1100, 220, 5, '#3a2a45', 7))
    return svg(L, 'dawn')


def march_scene():
    L = outdoor('grey', cl=35, mt=640)
    L.append(ground('grey', 780, '#6a6a48'))
    L.append(hut_row([(260, 790, .7), (520, 782, .55), (1500, 786, .6), (1700, 792, .75)]))
    L.append(road('grey', (740, 1180), 780, '#8a7a62'))
    L.append(grass(790, 1060, 3, '#4a5a36', 90))
    o = ''; r = random.Random(11)
    k0 = 0
    for (yy, scl, n) in ((792, .5, 8), (822, .62, 8), (860, .8, 7), (910, 1.0, 6), (980, 1.35, 5), (1075, 1.85, 3)):
        wid = 360 + (yy - 780) * 2.6
        for k in range(n):
            xx = 960 - wid / 2 + (k + .5) * wid / n + r.randint(-10, 10)
            o += f'<g class="mk" data-s="{scl}">' + person(xx, yy, scl, SCOL[(k + yy) % 5], hat='helmet', back=True, seed=k + yy % 9, pose='spear', spear='bare', armor='#4a4e58', sash='#b8352a')
            if k % 2 == 0:
                o += pen_droop(xx + 40 * scl, yy - 330 * scl, yy - 30 * scl, PEN_S if k % 4 == 0 else '#3a5a8a')
            o += '</g>'
            if scl >= 1.0:
                o += f'<ellipse class="puff" cx="{xx}" cy="{yy}" rx="{34*scl}" ry="{8*scl}" fill="#d8c49a" opacity="0"/>'
    L.append(G('troops', o))
    L.append(drum(300, 1020, 1.2)); L.append(drum(1650, 1010, 1.1))
    return svg(L, 'grey')


JS = """
(cfg) => {
  const A = []; let seed = 5; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
  const add = (el, kf, dur, phase=0, ease='ease-in-out') => { if(!el) return;
    const a = el.animate(kf, {duration: dur*1000, iterations: Infinity, easing: ease}); a.pause(); A.push([a, phase*1000]); };
  const tb = (el, o='center') => { el.style.transformBox='fill-box'; el.style.transformOrigin=o; };
  const Q = s => document.querySelectorAll(s);
  const svg = document.documentElement;
  const cam = document.createElementNS('http://www.w3.org/2000/svg','g');
  while (svg.childNodes.length > 1) cam.appendChild(svg.childNodes[1]);
  svg.appendChild(cam); cam.style.transformOrigin = cfg.zo;
  add(cam, [{transform:'scale(1.04) translate(0,0)'},{transform:'scale(1.12) translate('+cfg.pan+'px,'+(cfg.panY||0)+'px)'}], cfg.dur, 0, 'cubic-bezier(.4,0,.6,1)');
  Q('#clouds').forEach(e=>add(e,[{transform:'translateX(0)'},{transform:'translateX(-60px)'}], 30, 0,'linear'));
  Q('#mountains').forEach(e=>add(e,[{transform:'translateX(0)'},{transform:'translateX(-'+(cfg.mt||30)+'px)'}], 16, 0,'linear'));
  Q('#birds').forEach(e=>add(e,[{transform:'translate(0,0)'},{transform:'translate(240px,-50px)'}], 14, 0,'linear'));
  Q('.pen').forEach((e,i)=>{ tb(e,'left center'); const d=1.2+rnd()*1.0;
    add(e,[{rotate:'-2.5deg'},{rotate:'3.5deg'},{rotate:'-1.2deg'},{rotate:'2.6deg'},{rotate:'-2.5deg'}], d, rnd()*3);
    add(e,[{transform:'skewY(-3deg) scaleX(1)'},{transform:'skewY(3deg) scaleX(.92)'},{transform:'skewY(-3deg) scaleX(1)'}], d*1.4, rnd()*3); });
  Q('.eye').forEach(e=>{ tb(e); const d=3.2+rnd()*3.5; add(e,[{transform:'scaleY(1)',offset:0},{transform:'scaleY(1)',offset:.93},{transform:'scaleY(.08)',offset:.96},{transform:'scaleY(1)',offset:1}], d, rnd()*d,'linear'); });
  if (cfg.mode === 'row') {
    const T = cfg.T;
    // nước chảy: các dải sóng trôi sang trái, nhanh dần theo độ gần; liền mạch theo chu kỳ
    add(Q('#w1')[0],[{transform:'translateX(0)'},{transform:'translateX(-150px)'}], 1.6, 0,'linear');
    add(Q('#w2')[0],[{transform:'translateX(0)'},{transform:'translateX(-220px)'}], 1.5, 0,'linear');
    Q('#sunpath').forEach(e=>add(e,[{transform:'translateX(-10px) scaleX(1)'},{transform:'translateX(10px) scaleX(1.08)'}], 2.2));
    // thuyền nhấp nhô theo nhịp chèo
    ['#boat','#boatf','#staff','.fig'].forEach(sel => Q(sel).forEach(e=>{ e.style.transformBox='view-box'; e.style.transformOrigin='960px 920px';
      add(e,[{translate:'0 0'},{translate:'0 -4px'},{translate:'0 1px'},{translate:'0 0'}], T/2, 0); }));
    // mái chèo: thọc nước ở mũi, kéo về sau, nhấc lên, đưa trở lại
    Q('.oar').forEach((e,i)=>{ const px=+e.dataset.px, py=+e.dataset.py; e.style.transformBox='view-box'; e.style.transformOrigin='0 0';
      add(e,[{rotate:'-4deg',scale:'1',offset:0},{rotate:'0deg',scale:'1',offset:.08},{rotate:'62deg',scale:'1.0',offset:.55},{rotate:'62deg',scale:'.82',offset:.62},{rotate:'8deg',scale:'.8',offset:.9},{rotate:'-4deg',scale:'1',offset:1}], T, i*0.12, 'ease-in-out'); });
    // người chèo: ngả người ra trước rồi ngả ra sau theo nhịp
    Q('.fig').forEach((e,i)=>{ tb(e,'center bottom'); add(e,[{rotate:'6deg',offset:0},{rotate:'-5deg',offset:.55},{rotate:'-5deg',offset:.62},{rotate:'6deg',offset:1}], T, i*0.12,'ease-in-out'); });
    // bọt nước sau thuyền trôi dạt về sau và tan
    Q('.foam').forEach((e,i)=>{ tb(e); add(e,[{transform:'translateX(0) scaleX(.7)',opacity:.0},{opacity:.7,offset:.25},{transform:'translateX(-120px) scaleX(1.4)',opacity:0}], 2.2, i*.44,'ease-out'); });
    Q('.splash').forEach((e,i)=>{ tb(e); add(e,[{transform:'scale(.3)',opacity:0,offset:0},{transform:'scale(1)',opacity:.8,offset:.1},{transform:'scale(1.7)',opacity:0,offset:.35},{opacity:0,offset:1}], T, i*0.12,'ease-out'); });
    Q('#reeds').forEach((e,i)=>{ tb(e,'center bottom'); add(e,[{transform:'skewX(-1.5deg)'},{transform:'skewX(2.5deg)'},{transform:'skewX(-1.5deg)'}], 3.5+i, i*.8); });
    Q('.far').forEach((e,i)=>{ add(e,[{transform:'translateX(0)'},{transform:'translateX(-90px)'}], 16, 0,'linear'); });
  }
  if (cfg.mode === 'march') {
    const P = cfg.step; // một nhịp bước = 2 chân
    Q('.mk').forEach((g,i)=>{ const s=+g.dataset.s, ph=(i%3)*0.02; tb(g,'center bottom');
      add(g,[{translate:'0 0',rotate:'-1deg'},{translate:'0 '+(-5*s)+'px',rotate:'0deg'},{translate:'0 0',rotate:'1deg'},{translate:'0 '+(-5*s)+'px',rotate:'0deg'},{translate:'0 0',rotate:'-1deg'}], P*2, ph,'ease-in-out');
      g.querySelectorAll('.ftL').forEach(f=>{ tb(f); add(f,[{translate:'0 0',offset:0},{translate:'0 '+(-16*s)+'px',offset:.25},{translate:'0 0',offset:.5},{translate:'0 0',offset:1}], P*2, ph,'ease-in-out'); });
      g.querySelectorAll('.ftR').forEach(f=>{ tb(f); add(f,[{translate:'0 0',offset:0},{translate:'0 0',offset:.5},{translate:'0 '+(-16*s)+'px',offset:.75},{translate:'0 0',offset:1}], P*2, ph,'ease-in-out'); });
    });
    Q('.puff').forEach((e,i)=>{ tb(e); add(e,[{transform:'scale(.4) translateY(0)',opacity:0},{opacity:.45,offset:.3},{transform:'scale(1.5) translateY(-14px)',opacity:0}], P*2, (i%3)*.15,'ease-out'); });
    Q('.dust').forEach(e=>add(e,[{transform:'translate(-10px,6px)'},{transform:'translate(14px,-8px)'}], 5));
  }
  window.__seek = t => A.forEach(([a,p]) => { a.currentTime = t*1000 + p; });
}
"""


def run(name):
    fd = pathlib.Path('/tmp/dongthat'); fd.mkdir(exist_ok=True)
    svgtxt, cfg = {'chay': (rowing_scene, dict(mode='row', T=T_ROW, dur=DUR, zo='960px 800px', pan=-30, panY=-10, mt=40)),
                   'hanh': (march_scene, dict(mode='march', step=.42, dur=DUR, zo='960px 900px', pan=0, panY=40, mt=20))}[name]
    p = fd / f'{name}.svg'; p.write_text(svgtxt(), encoding='utf-8')
    d = fd / name; d.mkdir(exist_ok=True)
    with sync_playwright() as pw:
        br = pw.chromium.launch(); pg = br.new_page(viewport={'width': 1920, 'height': 1080})
        pg.goto(p.as_uri()); pg.evaluate(JS, cfg)
        for i in range(int(FPS * DUR)):
            pg.evaluate('t=>window.__seek(t)', i / FPS); pg.screenshot(path=str(d / f'{i:04d}.png'))
        br.close()
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', str(d / '%04d.png'), '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', str(fd / f'{name}.mp4')], check=True)
    print('ok', name)


if __name__ == '__main__':
    if sys.argv[1] == 'ghep':
        fd = pathlib.Path('/tmp/dongthat'); (fd / 'l.txt').write_text(''.join(f"file '{fd/n}.mp4'\n" for n in ('chay', 'hanh')))
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', str(fd / 'l.txt'), '-c', 'copy', '/tmp/demo_dong3.mp4'], check=True)
    elif sys.argv[1] == 'thu':
        # chỉ chụp vài khung kiểm tra
        pass
    else:
        run(sys.argv[1])
