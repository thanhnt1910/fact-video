"""Cảnh có người, ngựa, voi DI CHUYỂN THẬT (nhìn nghiêng, tay chân tách rời, nền trượt): python phim_ban_do/phang/di_chuyen.py [số cảnh] [--thu t1 t2 ...]
Cảnh: 19009 (kỵ sĩ cầm cờ tiết), 19014 (quân Đại Việt vào đất Chiêm), 19015 (tiên phong cưỡi ngựa), 19038 (hai đạo quân tiến lên), 19042 (viện binh Tống),
19057 (quân Tống tràn xuống), 19076 (voi cống nạp), 19086 (đem quân dẹp loạn), 19071 (chèo thuyền: dùng nguoi_nghieng.row_side)."""
import sys, pathlib, subprocess, shutil, tempfile, random
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import chitiet
from chitiet import *            # noqa  (flat.DETAIL = True)
import nguoi_nghieng as ng
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / 'assets' / 'clips_phang' / 'lt1'
FPS, DUR = 24, 6.0


def side_horse(uid, x, y, s, col='#7a4a2e', mane='#2a1a14', ph=0.0, flip=1, cloth='#b8352a'):
    """Ngựa nhìn nghiêng quay sang phải, gốc = mặt đất dưới bụng. Chân: .hl (đùi) và .hk (cẳng) để JS xoay quanh khớp."""
    dk, lt = sh(col, .68), sh(col, 1.2)
    def leg(cls, c, hx):
        return (f'<g transform="translate({hx},-118)"><g class="hl {cls}"><path d="M-11,-4 Q-14,28 -9,58 L9,58 Q14,26 11,-4Z" fill="{c}"/>'
                f'<g transform="translate(0,56)"><g class="hk {cls}k"><path d="M-8,-2 L-7,52 L7,52 L8,-2Z" fill="{c}"/><path d="M-9,50 L9,50 L11,62 L-11,62Z" fill="#2a1d1a"/></g></g></g></g>')
    body = (f'<path d="M-122,-176 Q-132,-140 -104,-110 Q0,-92 108,-112 Q136,-140 124,-178 Q0,-200 -122,-176Z" fill="{col}"/>'
            f'<path d="M-100,-114 Q0,-96 104,-116 Q60,-104 0,-102 Q-50,-102 -100,-114Z" fill="{dk}" opacity=".55"/>'
            f'<path d="M-30,-190 Q40,-206 96,-190 L96,-150 Q30,-140 -30,-150Z" fill="{cloth}"/><path d="M-30,-152 Q30,-142 96,-152 L96,-146 Q30,-134 -30,-146Z" fill="#e0b040"/>')
    neck = (f'<g class="neck"><path d="M96,-176 Q132,-216 150,-238 L184,-224 Q168,-186 128,-142Z" fill="{col}"/>'
            f'<path d="M104,-192 Q124,-232 148,-246 Q132,-214 118,-176Z" fill="{mane}"/>'
            f'<g class="hd"><path d="M146,-240 Q176,-262 204,-238 Q226,-218 228,-198 Q222,-188 208,-192 Q186,-200 170,-214Z" fill="{col}"/>'
            f'<path d="M146,-240 L158,-262 L168,-242Z" fill="{dk}"/><circle cx="186" cy="-236" r="4" fill="#1b1417"/><path d="M216,-196 Q226,-198 226,-206" stroke="#2a1d1a" stroke-width="3" fill="none"/></g></g>')
    tail = f'<g transform="translate(-118,-170)"><g class="tail"><path d="M0,0 Q-30,18 -26,70 Q-14,40 6,12Z" fill="{mane}"/></g></g>'
    return (f'<g class="hs" id="{uid}" data-ph="{ph}" transform="translate({x},{y}) scale({s*flip},{s})"><ellipse cx="0" cy="2" rx="130" ry="10" fill="#000" opacity=".18"/>'
            f'{leg("hB2", dk, -88)}{leg("hF2", dk, 80)}<g class="hbody">{tail}{body}{neck}</g>{leg("hB1", col, -70)}{leg("hF1", col, 96)}</g>')


def side_elephant(uid, x, y, s, ph=0.0, cloth='#b8352a'):
    col = '#8a8a96'; dk = sh(col, .72); lt = sh(col, 1.2)
    def leg(cls, c, hx):
        return (f'<g transform="translate({hx},-120)"><g class="hl {cls}"><path d="M-26,-6 Q-30,50 -24,122 L24,122 Q30,50 26,-6Z" fill="{c}"/>'
                f'<ellipse cx="0" cy="118" rx="27" ry="9" fill="#d9d4c4"/></g></g>')
    body = (f'<path d="M-170,-250 Q-200,-170 -150,-110 Q0,-70 150,-110 Q196,-170 160,-250 Q0,-300 -170,-250Z" fill="{col}"/>'
            f'<path d="M-130,-110 Q0,-78 140,-112 Q60,-96 0,-96 Q-70,-94 -130,-110Z" fill="{dk}" opacity=".5"/>'
            f'<path d="M-90,-286 Q10,-312 100,-284 L110,-236 Q10,-224 -100,-236Z" fill="{cloth}"/><path d="M-100,-238 Q10,-226 110,-238 L110,-228 Q10,-216 -100,-228Z" fill="#e0b040"/>')
    head = (f'<g class="hd"><path d="M130,-262 Q196,-290 236,-240 Q250,-186 226,-150 L170,-128 Q130,-170 134,-230Z" fill="{col}"/>'
            f'<ellipse cx="164" cy="-218" rx="30" ry="46" fill="{dk}" transform="rotate(14 164 -218)"/><circle cx="216" cy="-218" r="5" fill="#1b1417"/>'
            f'<path d="M222,-170 Q258,-168 270,-152 Q250,-158 228,-156Z" fill="#f2ecd8"/>'
            f'<g transform="translate(222,-168)"><g class="trunk"><path d="M-8,-4 Q30,6 34,56 Q36,106 12,128 L-6,120 Q10,96 8,54 Q4,22 -14,12Z" fill="{col}"/></g></g></g>')
    tail = f'<g transform="translate(-164,-230)"><g class="tail"><path d="M0,0 Q-20,30 -14,72 L-4,72 Q-8,36 8,6Z" fill="{dk}"/></g></g>'
    return (f'<g class="es" id="{uid}" data-ph="{ph}" transform="translate({x},{y}) scale({s},{s})"><ellipse cx="0" cy="2" rx="190" ry="12" fill="#000" opacity=".18"/>'
            f'{leg("eB2", dk, -110)}{leg("eF2", dk, 104)}<g class="ebody">{tail}{body}{head}</g>{leg("eB1", col, -128)}{leg("eF1", col, 130)}</g>')


def rider_on(uid, x, y, s, col, hat, seed, beard=None, armor=None, sash='#a8452f', spear=None, pants=None):
    f = ng.side_fig(uid, x, y, s, col, hat=hat, seed=seed, pants=pants or sh(col, .65), beard=beard, armor=armor, sash=sash, spear=spear, shadow=False)
    return f.replace(f'id="{uid}"', f'id="{uid}" data-seat="1"')


def back_far(kind, dx=520):
    far = ''.join(hut(x, 800, .6) for x in range(100, 4200, dx)) + ''.join(tree(x + dx // 2 - 30, 800, .8, kind) for x in range(100, 4200, dx))
    return f'<g class="bgfar">{far}</g>'


def base_scene(kind, sun=None, cl=35, mt=640, ground_col='#6a6a48', road_col='#8a7a62', far=True, birds_=None):
    L = outdoor(kind, sun=sun, cl=cl, mt=mt, birds_=birds_)
    if far: L.append(back_far(kind))
    L.append(ground(kind, 800, ground_col))
    L.append(f'<rect y="800" width="1920" height="280" fill="{road_col}" opacity=".85"/>')
    L.append(ng.ground_marks(820, 880, 'gm1', 1)); L.append(ng.ground_marks(900, 970, 'gm2', 2)); L.append(ng.ground_marks(990, 1070, 'gm3', 3))
    return L


def marchers(side, rows, i0=0, xshift=0):
    out = ''; i = i0
    for yy, s, n, gap, x0 in rows:
        for k in range(n):
            xx = x0 + k * gap + xshift + random.Random(i).randint(-14, 14)
            if side == 'viet':
                col = VCOL[i % len(VCOL)]; hat = 'cone'; arm = None; sash = SASHV[i % len(SASHV)]; sp = PEN_V if i % 2 == 0 else 'bare'
            else:
                col = SCOL[i % 5]; hat = 'helmet'; arm = '#4a4e58'; sash = '#b8352a'; sp = PEN_S if i % 2 == 0 else '#3a5a8a'
            f = ng.side_fig(f'w{i}', xx, yy - 86 * s, s, col, hat=hat, seed=i + 2, pants=sh(col, .65), armor=arm, sash=sash, spear=sp,
                            beard=('white_goatee' if i % 7 == 3 else None))
            out += f.replace(f'id="w{i}"', f'id="w{i}" data-s="{s}" data-ph="{(i * 0.37) % 6.28:.2f}"')
            i += 1
    return out


ROWS3 = ((880, .75, 5, 205, 300), (975, 1.0, 4, 270, 380), (1075, 1.3, 3, 350, 340))


def sc_viet_march(kind='day', sun=(1500, 300)):
    L = base_scene(kind, sun=sun, cl=7, ground_col='#7a6a3f', road_col='#9a8250')
    L.append(G('troops', marchers('viet', ROWS3)))
    return svg(L, kind)


def sc_song_march(kind='grey'):
    L = base_scene(kind)
    L.append(G('troops', marchers('song', ROWS3)))
    return svg(L, kind)


def sc_viet_rider(kind='day', sun=(1500, 300)):                    # 19015: tiên phong cưỡi ngựa, lính bước theo
    L = base_scene(kind, sun=sun, cl=7, ground_col='#7a6a3f', road_col='#9a8250')
    L.append(G('troops', marchers('viet', ((880, .75, 3, 210, 120), (975, 1.0, 2, 260, 100)), 30)))
    L.append(side_horse('h0', 1130, 1060, 1.25, '#4a2e22', ph=0.0))
    L.append(rider_on('r0', 1130 + 8, 1060 - 120 * 1.25 - 60 * 1.25 + 30, 1.3, '#8a2a24', 'cone', 4, beard='black', armor='#4a4e58', sash='#e0b040'))
    L.append(f'<g class="pole"><line x1="1290" y1="700" x2="1290" y2="1000" stroke="#6b4a2a" stroke-width="7"/><path class="pen" d="M1290,712 q60,10 110,-4 q-10,40 -30,86 q-40,-24 -80,-30Z" fill="{PEN_V}"/></g>')
    return svg(L, kind)


def sc_song_rider(kind='day', sun=(300, 300)):                    # 19042: Trương Thủ Tiết dẫn viện binh
    L = base_scene(kind, sun=sun, cl=9)
    L.append(G('troops', marchers('song', ((880, .75, 3, 210, 120), (975, 1.0, 2, 260, 100)), 40)))
    L.append(side_horse('h0', 1120, 1060, 1.25, '#6a4a2e', ph=0.0, cloth='#3a5a8a'))
    L.append(rider_on('r0', 1128, 1060 - 120 * 1.25 - 60 * 1.25 + 30, 1.3, '#34445f', 'helmet', 6, beard='black', armor='#4a4e58', sash='#b8352a'))
    return svg(L, kind)


def sc_envoy_rider(kind='day', sun=(1500, 300)):                  # 19009: cưỡi ngựa cầm cờ tiết đi tuần thú
    L = base_scene(kind, sun=sun, cl=5, ground_col='#6f8a4a', road_col='#9a8250')
    L.append(side_horse('h0', 960, 1050, 1.4, '#6a3a2a', ph=0.0))
    L.append(rider_on('r0', 970, 1050 - 120 * 1.4 - 60 * 1.4 + 34, 1.45, '#3a4a6a', 'cone', 3, beard='black', sash='#e0b040'))
    L.append(f'<g class="pole"><line x1="1140" y1="640" x2="1140" y2="960" stroke="#6b4a2a" stroke-width="7"/><path class="pen" d="M1140,654 q70,12 130,-4 q-14,46 -34,100 q-50,-30 -96,-34Z" fill="#c0392b"/><circle cx="1140" cy="640" r="9" fill="#e0b040"/></g>')
    return svg(L, kind)


def sc_elephants(kind='day', sun=(1500, 300)):                     # 19076
    L = base_scene(kind, sun=sun, cl=7, ground_col='#6f8a4a', road_col='#9a8250')
    L.append(G('troops', marchers('viet', ((880, .75, 2, 220, 250),), 60)))
    for k, (x, sc_) in enumerate(((620, 1.0), (1180, 1.15))):
        L.append(side_elephant(f'e{k}', x, 1030 + k * 20, sc_, ph=k * 0.9))
        L.append(rider_on(f'er{k}', x + 130 * sc_, 1030 + k * 20 - 300 * sc_ + 14, .9, ['#3a4a6a', '#6a3a2a'][k], 'cone', 8 + k, beard=('white_goatee' if k else None)))
    return svg(L, kind)


ANIM = r"""
  const D2 = Math.PI/180;
  const hsAll = [...Q('.hs, .es')];
  function animals(t) {
    hsAll.forEach(g => {
      const ph = +g.dataset.ph, el = g.classList.contains('es'), P = el ? 1.5 : 0.95, w = 2*Math.PI*t/P + ph;
      const A = el ? 14 : 24, B = el ? 0 : 34;
      const pose = (cls, off) => { const a = w + off;
        const hl = g.querySelector('.'+cls), hk = g.querySelector('.'+cls+'k');
        if (hl) hl.style.transform = 'rotate('+(A*Math.sin(a))+'deg)';
        if (hk) hk.style.transform = 'rotate('+(-B*Math.max(0, Math.cos(a))- (el?0:4))+'deg)';
        else if (hl && el) hl.style.transform = 'rotate('+(A*Math.sin(a))+'deg) translateY('+(-5*Math.max(0, Math.cos(a)))+'px)'; };
      const q = el ? [['eF1', 0], ['eB2', Math.PI*0.5], ['eB1', Math.PI], ['eF2', Math.PI*1.5]]
                   : [['hF1', 0], ['hB2', Math.PI*0.5], ['hB1', Math.PI], ['hF2', Math.PI*1.5]];
      q.forEach(([c, o]) => pose(c, o));
      const hb = g.querySelector('.hbody, .ebody'); if (hb) hb.style.transform = 'translateY('+(-(el?4:5)*Math.abs(Math.sin(w*2)*0.5+Math.sin(w)*0.5))+'px) rotate('+(0.8*Math.sin(w))+'deg)';
      const hd = g.querySelector('.hd'); if (hd) { hd.style.transformBox='fill-box'; hd.style.transformOrigin='20% 90%'; hd.style.transform='rotate('+(el?3:5)*Math.sin(w*2+1)+'deg)'; }
      const tr = g.querySelector('.trunk'); if (tr) { tr.style.transformBox='fill-box'; tr.style.transformOrigin='top center'; tr.style.transform='rotate('+(16*Math.sin(w*0.9))+'deg)'; }
      const tl = g.querySelector('.tail'); if (tl) { tl.style.transformBox='fill-box'; tl.style.transformOrigin='top center'; tl.style.transform='rotate('+(10*Math.sin(w*1.3+2))+'deg)'; }
    });
    // người cưỡi: ngồi, chân buông, thân nhún theo bước
    Q('.sf[data-seat]').forEach(f => { const w = 2*Math.PI*t/0.95;
      setR(sub(f,'.legF'), -70); setR(sub(f,'.legFs'), 62); setR(sub(f,'.legB'), -64); setR(sub(f,'.legBs'), 68);
      setR(sub(f,'.armB'), -20); setR(sub(f,'.armBf'), -40); setR(sub(f,'.armF'), -30); setR(sub(f,'.armFf'), -50);
      setR(sub(f,'.torso'), 2 + 1.5*Math.sin(w*2));
      f.style.translate = '0 '+(-4*Math.abs(Math.sin(w)))+'px'; });
    Q('.pole').forEach(e => { e.style.transformBox='fill-box'; e.style.transformOrigin='bottom center'; e.style.transform='rotate('+(1.2*Math.sin(2*Math.PI*t/0.95*2))+'deg)'; });
  }
"""


def page_js():
    js = ng.JS.replace("window.__seek = t => { A.forEach(([a,p]) => { a.currentTime = t*1000 + p; });",
                       ANIM + "\n  window.__seek = t => { A.forEach(([a,p]) => { a.currentTime = t*1000 + p; }); animals(t);", 1)
    assert 'animals(t)' in js
    return js


SPEC = {19009: (sc_envoy_rider, dict(mode='walk', P=.95, speed=1.1)), 19014: (sc_viet_march, dict(mode='walk', P=1.1)),
        19015: (sc_viet_rider, dict(mode='walk', P=.95)), 19038: (lambda: sc_viet_march('day', (1700, 160)), dict(mode='walk', P=1.1)),
        19042: (sc_song_rider, dict(mode='walk', P=.95)), 19057: (sc_song_march, dict(mode='walk', P=1.1)),
        19076: (sc_elephants, dict(mode='walk', P=1.1)), 19086: (lambda: sc_viet_march('grey', None), dict(mode='walk', P=1.1))}


def render(pg, n, tmp, stills=None):
    if n == 19071:
        svgtxt = ng.row_side(); cfg = dict(mode='row', T=2.4, dur=DUR, zo='960px 800px', pan=-20); js = ng.JS
    else:
        fn, cfg = SPEC[n]; cfg = dict(cfg, dur=DUR, zo='960px 900px', pan=-20); svgtxt = fn(); js = page_js()
    p = tmp / f'{n}.svg'; p.write_text(svgtxt, encoding='utf-8')
    pg.goto(p.as_uri()); pg.evaluate(js, cfg)
    if stills:
        for t in stills:
            pg.evaluate('t=>window.__seek(t)', t); pg.screenshot(path=str(tmp / f'{n}_{t}.png'))
        return
    d = tmp / str(n); d.mkdir(exist_ok=True)
    for i in range(int(FPS * DUR)):
        pg.evaluate('t=>window.__seek(t)', i / FPS); pg.screenshot(path=str(d / f'{i:04d}.jpg'), type='jpeg', quality=90)
    OUT.mkdir(parents=True, exist_ok=True)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', str(d / '%04d.jpg'), '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
                    '-crf', '23', '-preset', 'veryfast', str(OUT / f'{n}.mp4')], check=True)
    shutil.rmtree(d, ignore_errors=True)


if __name__ == '__main__':
    a = sys.argv[1:]; stills = None
    if '--thu' in a:
        i = a.index('--thu'); stills = [float(x) for x in a[i + 1:]]; a = a[:i]
    ns = [int(x) for x in a] or sorted(list(SPEC) + [19071])
    tmp = pathlib.Path(tempfile.mkdtemp())
    with sync_playwright() as pw:
        br = pw.chromium.launch(); pg = br.new_page(viewport={'width': 1920, 'height': 1080})
        for n in ns:
            try:
                render(pg, n, tmp, stills); print('xong', n, flush=True)
            except Exception as e:
                import traceback; traceback.print_exc(); print('LỖI', n, repr(e)[:200], flush=True)
        br.close()
    if stills: print(tmp)
