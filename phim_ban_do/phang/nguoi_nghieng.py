"""Cách A: nhân vật nhìn nghiêng có tay chân tách rời, chuyển động bằng tính toán từng khung.
python phim_ban_do/phang/nguoi_nghieng.py <di|cheo|ghep>"""
import sys, pathlib, subprocess, random
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import chitiet
from chitiet import *   # noqa
from flat import sh, TONES
from playwright.sync_api import sync_playwright

FPS, DUR = 24, 8.0


def side_fig(uid, x, y, s, col, hat='cone', seed=0, pants='#4a3a2a', beard=None, armor=None, sash='#a8452f', spear=None, flip=1, shadow=True):
    """Người nhìn nghiêng quay sang phải. Gốc toạ độ cục bộ = hông. Các nhóm có class để JS xoay quanh khớp (gốc 0 0)."""
    sk = TONES[seed % len(TONES)]; dk = sh(col, .72); lt = sh(col, 1.25); pd = sh(pants, .8)
    def arm(cls, c):
        return (f'<g transform="translate(0,-58)"><g class="{cls}"><rect x="-5.5" y="-3" width="11" height="34" rx="5.5" fill="{c}"/>'
                f'<g transform="translate(0,30)"><g class="fore {cls}f"><rect x="-4.8" y="-3" width="9.6" height="29" rx="4.8" fill="{c}"/><rect x="-5.2" y="19" width="10.4" height="5" fill="{lt}"/><circle cx="0" cy="29" r="5.6" fill="{sk}"/></g></g></g></g>')
    def leg(cls, c):
        return (f'<g class="{cls}"><rect x="-7.5" y="-4" width="15" height="48" rx="7" fill="{c}"/>'
                f'<g transform="translate(0,42)"><g class="shin {cls}s"><rect x="-6.5" y="-3" width="13" height="46" rx="6" fill="{c}"/><path d="M-6,44 Q4,40 18,46 Q20,52 10,52 L-6,52Z" fill="#3a2a22"/></g></g></g>')
    hd = f'<circle cx="3" cy="-83" r="15" fill="{sk}"/><path d="M17,-84 l7,4 l-7,3Z" fill="{sh(sk,.92)}"/><circle cx="12" cy="-86" r="1.9" fill="#241a1a"/><path d="M8,-92 q5,-3 10,-1" stroke="#2a1c1c" stroke-width="1.8" fill="none"/><path d="M12,-74 q4,2 7,0" stroke="#7b2a22" stroke-width="1.5" fill="none"/><ellipse cx="-2" cy="-82" rx="3" ry="4.5" fill="{sh(sk,.85)}"/><circle cx="12" cy="-79" r="3" fill="#d9776a" opacity=".3"/>'
    if beard:
        hd += f'<path d="M6,-72 Q8,-56 16,-62 Q18,-70 12,-73Z" fill="{"#e9e4dc" if "white" in beard else "#1b1417"}"/>'
    if hat == 'cone':
        hd += '<path d="M-32,-92 L5,-128 L40,-92 Q4,-98 -32,-92Z" fill="#c9a45e"/><path d="M-32,-92 L5,-128 L-8,-95Z" fill="#a9863f"/><path d="M4,-80 Q2,-70 9,-68" stroke="#7b2a22" stroke-width="1.2" fill="none"/>'
    elif hat == 'helmet':
        hd += '<path d="M-14,-86 Q3,-112 20,-86Z" fill="#4a4e58"/><rect x="-15" y="-90" width="36" height="5" fill="#2e3038"/><path d="M3,-110 q4,-14 12,-10 q-4,8 -12,10Z" fill="#b8352a"/>' + ''.join(f'<circle cx="{k}" cy="-93" r="1.3" fill="#d8c98a"/>' for k in (-8, 0, 8, 16))
    elif hat == 'song':
        hd += '<rect x="-9" y="-122" width="26" height="30" rx="9" fill="#14121a"/><rect x="-10" y="-103" width="28" height="5" fill="#e0b040"/><rect x="-52" y="-113" width="104" height="6" rx="3" fill="#14121a"/>'
    else:
        hd += '<path d="M-13,-88 Q3,-104 19,-88 Q4,-94 -13,-88Z" fill="#17121a"/><circle cx="-12" cy="-96" r="7" fill="#17121a"/><rect x="-14" y="-92" width="34" height="5" fill="#b8352a"/>'
    arm_extra = ''
    torso = (f'<path d="M-15,-64 Q0,-70 15,-64 L21,30 L-21,30Z" fill="{col}"/><path d="M-15,-64 L-21,30 L-12,30 L-8,-62Z" fill="#fff" opacity=".07"/>'
             f'<path d="M4,-64 L21,30 L9,30 L2,-60Z" fill="#000" opacity=".12"/><rect x="-18" y="26" width="40" height="6" fill="{lt}"/>'
             f'<rect x="-17" y="-8" width="34" height="8" fill="{sash}"/><rect x="-3" y="-9" width="7" height="10" rx="2" fill="#e8d890"/>'
             f'<path d="M-6,-66 L10,-48 M10,-66 L-2,-52" stroke="{lt}" stroke-width="2.2" fill="none"/><rect x="-5" y="-72" width="10" height="9" fill="{sk}"/>')
    if armor:
        torso += f'<path d="M-14,-60 L14,-60 L16,-14 L-16,-14Z" fill="{armor}" opacity=".7"/>' + ''.join(f'<line x1="-14" y1="{-54+k*9}" x2="15" y2="{-54+k*9}" stroke="#000" stroke-width="1.1" opacity=".3"/>' for k in range(5))
    sp = ''
    if spear:
        sp = f'<g class="spear"><line x1="0" y1="40" x2="0" y2="-185" stroke="#6b4a2a" stroke-width="4"/><path d="M-5,-185 L0,-208 L5,-185Z" fill="#b9bcc4"/><path class="pen" d="M0,-176 q24,-5 46,3 q-22,8 -46,14Z" fill="{spear}"/></g>'
    return (f'<g class="sf" id="{uid}" transform="translate({x},{y}) scale({s*flip},{s})">{'<ellipse cx="4" cy="86" rx="38" ry="6" fill="#000" opacity=".16"/>' if shadow else ''}'
            f'<g class="body">{arm("armB", dk)}{leg("legB", pd)}<g class="torso">{torso}{hd}</g>{leg("legF", pants)}{sp}{arm("armF", col)}</g></g>')


def ground_marks(y0, y1, cls, seed, n=30, col='#6a5a42'):
    r = random.Random(seed); o = ''
    for _ in range(n):
        x = r.randint(-200, 4200); y = r.randint(y0, y1); w = r.randint(30, 90)
        o += f'<ellipse cx="{x}" cy="{y}" rx="{w}" ry="{3+(y-y0)*.03}" fill="{col}" opacity=".5"/>'
    return f'<g class="{cls}">{o}</g>'


def march_side():
    L = outdoor('grey', cl=35, mt=640)
    L.append(G('mtn2', ''))
    far = ''.join(hut(x, 800, .6) for x in range(100, 4200, 520)) + ''.join(tree(x + 230, 800, .8, 'grey') for x in range(100, 4200, 520))
    L.append(f'<g class="bgfar">{far}</g>')
    L.append(ground('grey', 800, '#6a6a48'))
    L.append(f'<rect y="800" width="1920" height="280" fill="#8a7a62" opacity=".85"/>')
    L.append(ground_marks(820, 880, 'gm1', 1)); L.append(ground_marks(900, 970, 'gm2', 2)); L.append(ground_marks(990, 1070, 'gm3', 3))
    rows = ((880, .75, 'gm1', 5, 205), (975, 1.0, 'gm2', 4, 270), (1075, 1.3, 'gm3', 3, 350))
    i = 0; out = ''
    for yy, s, cls, n, gap in rows:
        for k in range(n):
            xx = 340 + k * gap + (60 if yy == 975 else 0) + random.Random(i).randint(-16, 16)
            col = SCOL[i % 5]
            out += side_fig(f'w{i}', xx, yy - 86 * s, s, col, hat='helmet' if i % 2 == 0 else 'cone', seed=i + 2, pants=sh(col, .65), armor='#4a4e58', sash='#b8352a',
                            spear=(PEN_S if i % 2 == 0 else '#3a5a8a'), beard=('white_goatee' if i % 7 == 3 else None))
            out = out.replace(f'id="w{i}"', f'id="w{i}" data-s="{s}" data-ph="{(i*0.37)%6.28:.2f}"')
            i += 1
    L.append(G('troops', out))
    return svg(L, 'grey')


def row_side():
    L = outdoor('dawn', sun=(1500, 480), cl=38, mt=700)
    L.append(G('far', ''.join(f'<g class="far">{boat2(x, 780 + k % 2 * 6, .38, col="#5a3a22", oars=False)[0]}{boat2(x, 780 + k % 2 * 6, .38, col="#5a3a22", oars=False)[1]}</g>' for k, x in enumerate((420, 1480, 1900)))))
    L.append(G('riverbase', '<defs><linearGradient id="rvg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e6a49f"/><stop offset="1" stop-color="#7a86a8"/></linearGradient></defs><rect y="740" width="1920" height="340" fill="url(#rvg)"/>'))
    L.append(sunpath(1500, 745, 1070))
    import dongthat
    L.append(G('w1', dongthat.waves(770, 5, 150, '#fff', .35, 2.4, seed=1)))
    L.append(G('w2', dongthat.waves(840, 8, 220, '#fff', .38, 3, seed=2)))
    L.append(G('foam', ''.join(f'<ellipse class="foam" cx="{700-k*120}" cy="{936+(k%2)*8}" rx="{60-k*5}" ry="6" fill="#fff" opacity=".6"/>' for k in range(5))))
    bb, bf = boat2(960, 920, 2.1, oars=False)
    L.append(bb)
    L.append(G('staff', '<line x1="640" y1="870" x2="640" y2="520" stroke="#6b4a2a" stroke-width="8"/><path class="pen" d="M640,530 q52,10 92,-4 q-10,34 -28,70 q-30,-20 -64,-26Z" fill="#c0392b"/>'))
    s = 1.55
    r1 = side_fig('r0', 830, 850, s, '#6a5a3a', hat='cone', seed=3, pants='#4a3a2a', sash='#c0392b', shadow=False)
    r2 = side_fig('r1', 1090, 850, s, '#5a6a4a', hat='cone', seed=9, pants='#4a3a2a', beard='white_goatee', sash='#d08a2e', shadow=False)
    L.append(r1.replace('id="r0"', 'id="r0" data-px="930" data-hx="830"')); L.append(r2.replace('id="r1"', 'id="r1" data-px="1190" data-hx="1090"'))
    L.append(bf)
    for k, px in enumerate((930, 1190)):
        L.append(f'<g transform="translate({px},868)"><g class="oar2" id="o{k}"><line class="shaft" x1="-80" y1="0" x2="140" y2="0" stroke="#4a3220" stroke-width="9" stroke-linecap="round"/><line class="shaft2" x1="-80" y1="0" x2="140" y2="0" stroke="#8a6a44" stroke-width="3"/>'
                 f'<rect x="100" y="-9" width="46" height="18" rx="4" fill="#a98a5a" stroke="#4a3220" stroke-width="2"/><circle cx="0" cy="0" r="7" fill="#d8b04a"/></g></g>')
        L.append(f'<ellipse class="splash" cx="{px+105}" cy="{868+88}" rx="42" ry="7" fill="#fff" opacity="0"/>')
    L.append(reeds(20, 1000, 14, 220)); L.append(reeds(1640, 1010, 16, 200))
    return svg(L, 'dawn')


JS = r"""
(cfg) => {
  const A = []; let seed = 5; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
  const add = (el, kf, dur, phase=0, ease='ease-in-out') => { if(!el) return;
    const a = el.animate(kf, {duration: dur*1000, iterations: Infinity, easing: ease}); a.pause(); A.push([a, phase*1000]); };
  const tb = (el, o='center') => { el.style.transformBox='fill-box'; el.style.transformOrigin=o; };
  const Q = s => document.querySelectorAll(s), $ = s => document.querySelector(s);
  const D = Math.PI/180, svg = document.documentElement;
  const cam = document.createElementNS('http://www.w3.org/2000/svg','g');
  while (svg.childNodes.length > 1) cam.appendChild(svg.childNodes[1]);
  svg.appendChild(cam); cam.style.transformOrigin = cfg.zo;
  add(cam, [{transform:'scale(1.03)'},{transform:'scale(1.09) translate('+cfg.pan+'px,0)'}], cfg.dur, 0, 'cubic-bezier(.4,0,.6,1)');
  Q('#clouds').forEach(e=>add(e,[{transform:'translateX(0)'},{transform:'translateX(-60px)'}], 30, 0,'linear'));
  Q('#mountains').forEach(e=>add(e,[{transform:'translateX(0)'},{transform:'translateX(-60px)'}], 16, 0,'linear'));
  Q('.pen').forEach((e,i)=>{ tb(e,'left center'); const d=1.2+rnd();
    add(e,[{rotate:'-3deg'},{rotate:'4deg'},{rotate:'-1.5deg'},{rotate:'3deg'},{rotate:'-3deg'}], d, rnd()*3);
    add(e,[{transform:'skewY(-3deg) scaleX(1)'},{transform:'skewY(3deg) scaleX(.92)'},{transform:'skewY(-3deg) scaleX(1)'}], d*1.4, rnd()*3); });
  const setR = (el, deg) => { if (el) el.style.transform = 'rotate('+deg+'deg)'; };
  const sub = (f, c) => f.querySelector(c);
  // ---------- ĐI BỘ ----------
  const walkers = [...Q('.sf[data-ph]')];
  const P = cfg.P || 0.9;
  function walk(t) {
    walkers.forEach(f => {
      const ph = +f.dataset.ph, s = +f.dataset.s, w = 2*Math.PI*t/P + ph, sn = Math.sin(w), cs = Math.cos(w);
      const thigh = (a) => -26*Math.sin(a), knee = (a) => 4 + 48*Math.pow(Math.max(0, Math.cos(a)), 1.4);
      setR(sub(f,'.legF'), thigh(w)); setR(sub(f,'.legFs'), knee(w));
      setR(sub(f,'.legB'), thigh(w+Math.PI)); setR(sub(f,'.legBs'), knee(w+Math.PI));
      setR(sub(f,'.armB'), -30*Math.sin(w+Math.PI)*-1); setR(sub(f,'.armBf'), -22 - 12*Math.max(0, Math.sin(w)));
      setR(sub(f,'.armF'), -38 + 3*sn); setR(sub(f,'.armFf'), -62);
      setR(sub(f,'.torso'), 4 + 1.5*cs);
      const sp = sub(f,'.spear'); if (sp) { sp.style.transform = 'translate(22px,-8px) rotate('+(4+2*cs)+'deg)'; }
      sub(f,'.body').style.transform = 'translateY('+(-3.2*Math.abs(Math.cos(w)) )+'px)';
    });
    // nền trượt về trái theo bước chân từng hàng
    const v = (cls, k) => Q(cls).forEach(e => e.style.transform = 'translateX('+(-t*k)+'px)');
    const base = 2*34*Math.PI/180; // không dùng
    v('.gm1', 154*.75); v('.gm2', 154*1.0); v('.gm3', 154*1.3); v('.bgfar', 70);
  }
  // ---------- CHÈO ----------
  const rowers = [...Q('.sf[data-px]')];
  function row(t) {
    const T = cfg.T, L1 = 30, L2 = 29;
    rowers.forEach((f, i) => {
      const u = ((t/T + i*0.07) % 1 + 1) % 1, px = +f.dataset.px, s = 1.55, hx = +f.dataset.hx, py = 868, hy = 850;
      // góc cán chèo phía ngoài: 40° (thọc nước) -> 105° (kéo xong); phục hồi 45% còn lại
      const drive = 0.55; let a, k;
      if (u < drive) { const e = u/drive, m = 0.5 - 0.5*Math.cos(Math.PI*e); a = 40 + 65*m; k = 1; }
      else { const e = (u-drive)/(1-drive), m = 0.5 - 0.5*Math.cos(Math.PI*e); a = 105 - 65*m; k = 1 - 0.2*Math.sin(Math.PI*e); }
      const lean = -12 + 28*(a-40)/65;
      const inner = 82, ca = Math.cos(a*D), sa = Math.sin(a*D);
      const Hx = px - inner*ca, Hy = py - inner*sa;           // tay nắm cán
      // vai trong toạ độ cục bộ (hông = gốc), thân nghiêng 'lean'
      const lx = (Hx - hx)/s, ly = (Hy - hy)/s, sx = 60*Math.sin(lean*D), sy = -60*Math.cos(lean*D);
      let dx = lx - sx, dy = ly - sy, d = Math.hypot(dx, dy); const dd = Math.min(Math.max(d, 18), L1+L2-1);
      const base = Math.atan2(dy, dx), ang1 = Math.acos((L1*L1 + dd*dd - L2*L2)/(2*L1*dd));
      // khuỷu hạ xuống phía dưới
      const sh = base + ang1, elbow = Math.acos((L1*L1 + L2*L2 - dd*dd)/(2*L1*L2));
      const up = sh/D - 90, fore = (Math.PI - elbow)/D;      // cánh tay thả xuống = 0°
      setR(sub(f,'.torso'), lean);
      // đặt vai theo thân nghiêng: nhóm tay nằm ngoài torso nên dịch gốc vai
      ['armB','armF'].forEach(c => { const el = sub(f,'.'+c); el.parentNode.setAttribute('transform','translate('+sx.toFixed(2)+','+sy.toFixed(2)+')'); setR(el, up); setR(sub(f,'.'+c+'f'), -fore); });
      // chân ngồi: đùi đưa ra trước, cẳng chân thả xuống
      setR(sub(f,'.legF'), -88); setR(sub(f,'.legFs'), 92); setR(sub(f,'.legB'), -80); setR(sub(f,'.legBs'), 85);
      // mái chèo quay đúng theo góc a, cán trong kéo dài tới bàn tay
      const o = $('#o'+i); o.style.transform = 'rotate('+a+'deg) scale(1)';
      const sh1 = o.querySelector('.shaft'), sh2 = o.querySelector('.shaft2'); const inn = Math.hypot(Hx-px, Hy-py)+8, out = 140*k;
      [sh1, sh2].forEach(e => { e.setAttribute('x1', -inn); e.setAttribute('x2', out); });
      const bl = o.querySelector('rect'); bl.setAttribute('x', out-40);
      const bob = Math.sin(2*Math.PI*t/(T/2))*-3; f.style.translate = '0 '+bob+'px';
    });
  }
  window.__seek = t => { A.forEach(([a,p]) => { a.currentTime = t*1000 + p; });
    if (cfg.mode === 'walk') walk(t);
    if (cfg.mode === 'row') { row(t);
      const T = cfg.T;
      Q('#w1').forEach(e=>e.style.transform='translateX('+(-((t/1.6)%1)*150)+'px)'); Q('#w2').forEach(e=>e.style.transform='translateX('+(-((t/1.5)%1)*220)+'px)');
      Q('.foam').forEach((e,i)=>{ const u=((t/2.2 + i*.2)%1); e.style.transformBox='fill-box'; e.style.transformOrigin='center'; e.style.transform='translateX('+(-120*u)+'px) scaleX('+(.7+.7*u)+')'; e.style.opacity=Math.sin(Math.PI*u)*.7; });
      Q('.splash').forEach((e,i)=>{ const u=((t/T + i*.07)%1); e.style.transformBox='fill-box'; e.style.transformOrigin='center'; const a=Math.max(0,1-Math.abs(u-.55)/.18); e.style.opacity=a*.8; e.style.transform='scale('+(.5+a)+')'; });
      ['#boat','#boatf','#staff'].forEach(sel => Q(sel).forEach(e=>{ e.style.transform='translateY('+(Math.sin(2*Math.PI*t/(T/2))*-3)+'px)'; }));
    } };
}
"""


def run(name):
    fd = pathlib.Path('/tmp/nghieng'); fd.mkdir(exist_ok=True)
    fn, cfg = {'di': (march_side, dict(mode='walk', P=1.1, dur=DUR, zo='960px 900px', pan=-20)),
               'cheo': (row_side, dict(mode='row', T=2.4, dur=DUR, zo='960px 800px', pan=-20))}[name]
    p = fd / f'{name}.svg'; p.write_text(fn(), encoding='utf-8'); d = fd / name; d.mkdir(exist_ok=True)
    stills = [float(a) for a in sys.argv[2:]]
    with sync_playwright() as pw:
        br = pw.chromium.launch(); pg = br.new_page(viewport={'width': 1920, 'height': 1080}); pg.goto(p.as_uri()); pg.evaluate(JS, cfg)
        if stills:
            for t in stills:
                pg.evaluate('t=>window.__seek(t)', t); pg.screenshot(path=f'/tmp/nghieng/{name}_{t}.png')
            br.close(); return
        for i in range(int(FPS * DUR)):
            pg.evaluate('t=>window.__seek(t)', i / FPS); pg.screenshot(path=str(d / f'{i:04d}.png'))
        br.close()
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', str(d / '%04d.png'), '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', str(fd / f'{name}.mp4')], check=True)
    print('ok', name)


if __name__ == '__main__':
    if sys.argv[1] == 'ghep':
        fd = pathlib.Path('/tmp/nghieng'); (fd / 'l.txt').write_text(''.join(f"file '{fd/n}.mp4'\n" for n in ('di', 'cheo')))
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', str(fd / 'l.txt'), '-c', 'copy', '/tmp/demo_dong4.mp4'], check=True)
    else:
        run(sys.argv[1])
