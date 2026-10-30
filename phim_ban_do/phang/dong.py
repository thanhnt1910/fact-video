"""Demo chuyển động cho ảnh phẳng: python phim_ban_do/phang/dong.py -> /tmp/demo_dong.mp4 (SVG + Web Animations API, chụp từng khung, ghép ffmpeg)."""
import sys, pathlib, subprocess, shutil, math
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import chitiet
from playwright.sync_api import sync_playwright

FPS, DUR = 24, 6.0
JS = """
(cfg) => {
  const A = [];
  let seed = 7; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
  const add = (el, kf, dur, phase=0, ease='ease-in-out') => { if(!el) return;
    const a = el.animate(kf, {duration: dur*1000, iterations: Infinity, easing: ease}); a.pause(); A.push([a, phase*1000]); };
  const tb = (el, o='center') => { el.style.transformBox='fill-box'; el.style.transformOrigin=o; };
  const Q = s => document.querySelectorAll(s);
  const svg = document.documentElement;
  const cam = document.createElementNS('http://www.w3.org/2000/svg','g');
  while (svg.childNodes.length > 1) { cam.appendChild(svg.childNodes[1]); }
  svg.appendChild(cam);
  cam.style.transformOrigin = cfg.zo;
  add(cam, [{transform:'scale(1) translate(0,0)'},{transform:'scale(1.06) translate('+cfg.pan+'px,-6px)'}], cfg.dur, 0, 'cubic-bezier(.45,0,.55,1)');
  // thị sai: núi trôi chậm hơn mây
  Q('#mountains').forEach(e=>add(e,[{transform:'translateX(-6px)'},{transform:'translateX(6px)'}], cfg.dur*2, 0,'ease-in-out'));
  Q('#clouds').forEach(e=>add(e,[{transform:'translateX(-40px)'},{transform:'translateX(40px)'}], 30, 0,'linear'));
  Q('#birds').forEach(e=>add(e,[{transform:'translate(0,0)'},{transform:'translate(220px,-50px)'}], 18, 0,'linear'));
  // cờ: lắc quanh cán + gợn, mỗi lá một nhịp riêng, có đợt gió mạnh
  Q('.pen').forEach((e,i)=>{ tb(e,'left center'); const d1 = 1.5+rnd()*1.3, d2 = 2.3+rnd()*1.7;
    add(e,[{rotate:'-2deg'},{rotate:'3.2deg'},{rotate:'-1deg'},{rotate:'2.4deg'},{rotate:'-2deg'}], d1, rnd()*3);
    add(e,[{transform:'skewY(-3deg) scaleX(1)'},{transform:'skewY(2.5deg) scaleX(.93)'},{transform:'skewY(-1.5deg) scaleX(.98)'},{transform:'skewY(-3deg) scaleX(1)'}], d2, rnd()*3); });
  // khói, bụi: trôi lên và sang ngang
  Q('.dust').forEach((e,i)=>{ add(e,[{transform:'translate(-10px,6px)'},{transform:'translate(6px,-14px)'},{transform:'translate(16px,-4px)'},{transform:'translate(-10px,6px)'}], 5+rnd()*3, rnd()*5); });
  // nước: dịch rất chậm, vệt nắng nhấp nháy bất quy tắc
  Q('#river').forEach(e=>add(e,[{transform:'translateX(-16px)'},{transform:'translateX(16px)'}], 6));
  Q('#sunpath').forEach(e=>{ add(e,[{transform:'translateX(-8px) scaleX(1)'},{transform:'translateX(8px) scaleX(1.06)'}], 4.1); });
  Q('#reeds').forEach((e,i)=>{ tb(e,'center bottom'); add(e,[{transform:'skewX(-1.2deg)'},{transform:'skewX(2.2deg)'},{transform:'skewX(-.4deg)'},{transform:'skewX(-1.2deg)'}], 3.8+rnd()*1.5, rnd()*4); });
  // thuyền: lắc ngang, bập bềnh, nghiêng — ba nhịp lệch nhau
  if (cfg.boat) cfg.boat.forEach(sel => Q(sel).forEach(e=>{ e.style.transformBox='view-box'; e.style.transformOrigin='960px 920px';
      add(e,[{translate:'0 -3px'},{translate:'0 3px'}], 3.1);
      add(e,[{rotate:'-0.5deg'},{rotate:'0.6deg'}], 4.3);
      add(e,[{transform:'translateX(-4px)'},{transform:'translateX(4px)'}], 6.7); }));
  // sóng quanh thân thuyền
  if (cfg.rings) { const ns='http://www.w3.org/2000/svg';
    cfg.rings.forEach(([x,y,w],k)=>{ const r=document.createElementNS(ns,'ellipse'); r.setAttribute('cx',x); r.setAttribute('cy',y); r.setAttribute('rx',w); r.setAttribute('ry',w*.09);
      r.setAttribute('fill','none'); r.setAttribute('stroke','#fff'); r.setAttribute('stroke-width','3'); r.style.transformBox='fill-box'; r.style.transformOrigin='center';
      cam.insertBefore(r, cam.querySelector('#boat')); add(r,[{transform:'scale(.8)',opacity:.0},{opacity:.5,offset:.35},{transform:'scale(1.25)',opacity:0}], 3.6, k*1.2,'ease-out'); }); }
  // người: gần như đứng yên, chỉ thở rất nhẹ, mỗi người một nhịp
  Q('.fig').forEach((e,i)=>{ tb(e,'center bottom'); const amp = cfg.fig;
      if (amp) add(e,[{transform:'translateY(0)'},{transform:'translateY(-'+amp+'px)'}], 3.2+rnd()*2.5, rnd()*5); });
  // chớp mắt, mỗi người một lúc
  Q('.eye').forEach((e,i)=>{ tb(e); const d = 3.2+rnd()*3.5;
      add(e,[{transform:'scaleY(1)',offset:0},{transform:'scaleY(1)',offset:.93},{transform:'scaleY(.08)',offset:.96},{transform:'scaleY(1)',offset:1}], d, rnd()*d,'linear'); });
  // đèn dầu, đuốc: chập chờn bất quy tắc
  Q('g[id^=oil], g[id^=torch], #torch, #oildish').forEach((e,i)=>{ tb(e,'center bottom');
      add(e,[{opacity:.9,transform:'scale(1)'},{opacity:1,transform:'scale(1.02,1.04)'},{opacity:.82,transform:'scale(.99,.97)'},{opacity:1,transform:'scale(1,1.03)'},{opacity:.9,transform:'scale(1)'}], 1.3+rnd()*.6, rnd()); });
  window.__seek = t => A.forEach(([a,p]) => { a.currentTime = t*1000 + p; });
}
"""

def render(page, n, cfg, out, frames_dir):
    svg = chitiet.SCN[n]()
    p = frames_dir / f'{n}.svg'; p.write_text(svg, encoding='utf-8')
    page.goto(p.as_uri()); page.evaluate(JS, cfg)
    d = frames_dir / str(n); d.mkdir(exist_ok=True)
    for i in range(int(FPS * cfg['dur'])):
        page.evaluate('t=>window.__seek(t)', i / FPS)
        page.screenshot(path=str(d / f'{i:04d}.png'))
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', str(d / '%04d.png'),
                    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', str(out)], check=True)

if __name__ == '__main__':
    fd = pathlib.Path('/tmp/dong_frames2'); fd.mkdir(exist_ok=True)
    only = int(sys.argv[1]) if len(sys.argv) > 1 else None
    jobs = [(19071, dict(dur=DUR, zo='960px 700px', boat=['#boat', '#boatf', '#staff', '.fig'], fig=0, pan=-14, rings=[(960,938,230),(960,938,190)])),
            (19066, dict(dur=DUR, zo='960px 800px', fig=1.2, pan=10)),
            (19054, dict(dur=DUR, zo='960px 650px', fig=1.0, pan=-8))]
    if only:
        with sync_playwright() as p:
            br = p.chromium.launch(); pg = br.new_page(viewport={'width': 1920, 'height': 1080})
            for n, cfg in jobs:
                if n == only: render(pg, n, cfg, fd / f'{n}.mp4', fd)
            br.close()
    else:
        outs = [fd / f'{n}.mp4' for n, _ in jobs]
        lst = fd / 'l.txt'; lst.write_text(''.join(f"file '{o}'\n" for o in outs))
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', str(lst), '-c', 'copy', '/tmp/demo_dong2.mp4'], check=True)
        print('ok')
