"""64 cảnh ảnh phẳng cho video Lý Thường Kiệt (mã lt1). Mỗi hàm trả về chuỗi SVG; số cảnh = số đoạn lời kể (19002...)."""
import random
from flat import *  # noqa

# ---------------------------------------------------------------- bảng nhân vật (một mô tả cố định, dùng cho mọi cảnh)
CAST = {
    'LTK_T': dict(col='#2e4a6b', turban='#14121a', seed=1, young=True, sash='#c0392b'),
    'LTK_G': dict(col='#8a2230', armor='#2e2530', turban='#1c1522', beard='short', sash='#e0b040', trim='#e0b040', seed=2),
    'LTK_L': dict(col='#8a2230', turban='#1c1522', beard='white_long', hair='#e9e4dc', sash='#e0b040', trim='#e0b040', seed=3),
    'TT': dict(col='#e8b83a', diadem=True, beard='white_long', hair='#cfcfd4', sash='#8a2a24', trim='#8a2a24', seed=4),
    'TTG': dict(col='#e8b83a', diadem=True, beard='mustache', sash='#8a2a24', trim='#8a2a24', seed=5),
    'NT': dict(col='#e8b83a', diadem=True, young=True, sash='#8a2a24', seed=6),
    'YL': dict(col='#9ccf9a', long=True, sash='#d8c070', seed=7, hair='#17121a'),
    'DTH': dict(col='#6a3a6b', long=True, hair='#8a8a92', sash='#c9a45e', seed=8),
    'LDT': dict(col='#2e3f78', turban='#14121a', beard='white_long', hair='#e9e4dc', sash='#c9a45e', seed=9),
    'CC': dict(col='#e8863a', hat='champa', beard='mustache', wide=True, sash='#f2efe6', seed=10),
    'TD': dict(col='#6a6a3a', armor='#4a4a30', hat='helmet', beard='thick', sash='#b8352a', seed=11),
    'DTN': dict(col='#7a5a3a', turban='#5a4128', beard='goatee', sash='#c0392b', seed=12),
    'LVT': dict(col='#5a6a8a', turban='#14121a', beard='mustache', sash='#c9a45e', seed=13),
    'LG': dict(col='#7a5a3a', crown='headband', sash='#6a4a2a', seed=14),
    'LTH': dict(col='#2e5a3a', turban='#14121a', beard='mustache', young=True, sash='#c9a45e', seed=15),
    'OFF1': dict(col='#4a6a4a', turban='#14121a', beard='goatee', sash='#c9a45e', seed=16),
    'OFF2': dict(col='#6a4a5a', turban='#14121a', sash='#c9a45e', seed=17, young=True),
    'OFF3': dict(col='#3a5a7a', turban='#14121a', beard='white_goatee', hair='#d8d8dc', sash='#c9a45e', seed=18),
    'TG': dict(col='#2e6a6a', hat='song', beard='goatee', hair='#8a8a92', wide=True, long=True, sash='#c9a45e', seed=21),
    'VAT': dict(col='#6a3a7a', hat='song', beard='white_goatee', hair='#8a8a92', wide=True, long=True, sash='#c9a45e', seed=22),
    'TK': dict(col='#8a5a3a', hat='song', wide=True, long=True, sash='#c9a45e', seed=23),
    'LD': dict(col='#3a7a4a', hat='song', beard='thick', wide=True, long=True, sash='#c9a45e', seed=24),
    'TTT': dict(col='#8a4a38', armor='#6a3a2a', hat='helmet', beard='thick', sash='#b8352a', seed=25),
    'QQ': dict(col='#3a3e4a', armor='#2a2e38', hat='helmet', beard='white_long', hair='#cfcfd4', sash='#b8352a', seed=26),
    'TT2': dict(col='#2a2a32', armor='#1e1e26', hat='helmet', beard='mustache', young=True, sash='#b8352a', seed=27),
    'SK': dict(col='#a88a30', hat='crownS', beard='mustache', wide=True, long=True, sash='#6a1f1a', seed=28),
}
SCALE = {'TK': 1.1, 'LD': .92, 'TTT': 1.05, 'QQ': 1.15, 'NT': .68}
PEN_V, PEN_S, PEN_O = '#a8452f', '#2e4a80', '#d9892e'
VCOL = ['#6b4a2e', '#7a5634', '#5c4228', '#6e5236', '#80603c', '#5a4a30']
SASHV = ['#c0392b', '#8a2a24', '#d08a2e', '#6a8a3a', '#a8452f']
SCOL = ['#3a4a6a', '#34445f', '#41506e', '#2e3d58', '#3c4c70']
PCOL = ['#7a5a3a', '#6a7a4a', '#8a6a4a', '#5a6a7a', '#8a5a4a', '#6a5a7a', '#9a7a4a']
_uid = [0]


def P(who, x, y, s=1.0, **ov):
    d = dict(CAST[who])
    d.update(ov)
    col = d.pop('col')
    return person(x, y, s * SCALE.get(who, 1.0), col, **d)


def sit(who_or_dict, x, seat_y, s=1.0, lap=True, **ov):
    d = dict(CAST[who_or_dict]) if isinstance(who_or_dict, str) else dict(who_or_dict)
    d.update(ov)
    col = d.pop('col')
    sc = s * (SCALE.get(who_or_dict, 1.0) if isinstance(who_or_dict, str) else 1.0)
    h = 150 * sc
    _uid[0] += 1
    cid = f'cp{_uid[0]}'
    fig = person(x, seat_y + h * 0.3, sc, col, **d)
    o = f'<clipPath id="{cid}"><rect x="0" y="0" width="1920" height="{seat_y}"/></clipPath><g clip-path="url(#{cid})">{fig}</g>'
    if lap:
        o += (f'<path d="M{x-40*sc},{seat_y-6*sc} Q{x},{seat_y+10*sc} {x+40*sc},{seat_y-6*sc} L{x+50*sc},{seat_y+22*sc} '
              f'Q{x},{seat_y+34*sc} {x-50*sc},{seat_y+22*sc}Z" fill="{sh(col,.78)}"/>')
    return o


def knee(who, x, y, s=1.4):
    d = CAST[who]
    return kneeler(x, y, s, d['col'], turban=d.get('turban', '#1b1620'), seed=d['seed'], hat=d.get('hat') if d.get('hat') == 'helmet' else None)


def soldier(x, y, s, i, side='viet', back=False, pose='spear', pen=True, penc=None):
    face = s > .9 and not back
    if side == 'viet':
        sp = (penc or PEN_V) if pen else 'bare'
        return person(x, y, s, VCOL[i % len(VCOL)], hat='cone', face=face, back=back, seed=i, pose=pose,
                      spear=sp if pose == 'spear' else None, sash=SASHV[i % len(SASHV)])
    sp = (penc or PEN_S) if pen else 'bare'
    return person(x, y, s, SCOL[i % len(SCOL)], hat='helmet', face=face, back=back, seed=i + 3, pose=pose, armor='#4a4e58',
                  spear=sp if pose == 'spear' else None, sash='#b8352a')


def rows(spec, side='viet', back=False, cx=960, pen=True, penc=None, spread=2.4, seed=0, base=780):
    """spec: [(y, s, n)] từ xa tới gần."""
    r = random.Random(seed)
    o = ''
    i = seed
    for (yy, sc, n) in spec:
        wid = 360 + (yy - base) * spread
        for k in range(n):
            xx = cx - wid / 2 + (k + .5) * wid / n + r.randint(-10, 10)
            o += soldier(xx, yy, sc, i, side, back, pen=pen and (k % 2 == 0), penc=penc)
            o += f'<ellipse cx="{xx}" cy="{yy+4*sc}" rx="{40*sc}" ry="{6*sc}" fill="#000" opacity=".12"/>'
            i += 1
    return G('troops', o)


def horse(x, y, s=1.0, col='#7a4a2e', facing=1):
    mane = sh(col, .55)
    o = f'<g transform="translate({x},{y}) scale({s*facing},{s})">'
    for dx in (-86, -62, 56, 80):
        o += f'<path d="M{dx-9},-110 L{dx-7},-14 L{dx+9},-14 L{dx+9},-110Z" fill="{sh(col,.82 if dx in (-62,80) else 1)}"/><rect x="{dx-10}" y="-14" width="20" height="14" rx="4" fill="#2a1d1a"/>'
    o += f'<ellipse cx="0" cy="-150" rx="112" ry="56" fill="{col}"/>'
    o += f'<path d="M64,-196 L112,-292 L152,-268 L128,-148Z" fill="{col}"/>'
    o += f'<path d="M104,-296 L186,-290 Q226,-256 214,-214 L190,-212 Q172,-236 140,-250 Z" fill="{col}"/>'
    o += f'<path d="M110,-298 L116,-326 L130,-296Z" fill="{col}"/>'
    o += f'<path d="M66,-198 Q82,-290 108,-306 L122,-290 Q100,-250 94,-190Z" fill="{mane}"/>'
    o += f'<circle cx="170" cy="-272" r="4" fill="#1a1216"/><ellipse cx="208" cy="-224" rx="5" ry="3" fill="#2a1d1a"/>'
    o += f'<path d="M-108,-176 Q-170,-160 -150,-84 Q-142,-120 -108,-130Z" fill="{mane}"/>'
    o += f'<path d="M-40,-198 Q0,-212 40,-198 L36,-186 Q0,-198 -36,-186Z" fill="#8a2a24"/>'
    o += '</g>'
    return G('horse', o)


def rider(who, x, y_horse, s=1.0, facing=1, pose='hands', **ov):
    """Người ngồi trên lưng ngựa (nhìn chính diện, ngựa nhìn nghiêng)."""
    seat = y_horse - 205 * s + 30
    return sit(who, x, seat, s=s * 1.0, pose=pose, **ov)


def banner(x, ybase, ytop, col, w=70):
    return (f'<line x1="{x}" y1="{ybase}" x2="{x}" y2="{ytop}" stroke="#2a1d1a" stroke-width="6"/>'
            f'<path class="pen" d="M{x},{ytop} L{x+w},{ytop+6} L{x+w},{ytop+80} L{x},{ytop+74}Z" fill="{col}"/>')


def pen_droop(x, ytop, ybase, col):
    return (f'<line x1="{x}" y1="{ybase}" x2="{x}" y2="{ytop}" stroke="#2a1d1a" stroke-width="5"/>'
            f'<path d="M{x},{ytop+4} Q{x+10},{ytop+50} {x+6},{ytop+96} Q{x-6},{ytop+60} {x},{ytop+4}Z" fill="{col}"/>')


def dust(x, y, w=500, op=.28, col='#e6c79a'):
    return f'<ellipse class="dust" cx="{x}" cy="{y}" rx="{w}" ry="{w*.12}" fill="{col}" opacity="{op}"/><ellipse class="dust" cx="{x+w*.3}" cy="{y-w*.07}" rx="{w*.6}" ry="{w*.1}" fill="{col}" opacity="{op}"/>'


def outdoor(kind, sun=None, moon=False, cl=1, birds_=None, mt=650):
    L = [sky(kind, sun=sun, moon=moon), clouds(kind, cl)]
    if birds_:
        L.append(birds(*birds_, col='#3a2a45' if kind in ('dusk', 'dawn') else '#3d5566'))
    L.append(mountains(kind, mt, seed=cl + 2))
    return L


def road_back(kind, y=780):
    return road(kind, (740, 1180), y)


# =================================================================== CẢNH
SC = {}


def scene(n):
    def deco(f):
        SC[n] = f
        return f
    return deco


@scene(19002)
def _(): 
    L = outdoor('day', sun=(1500, 300))
    L.append(wall(560, 'grey', tower_x=420, side='song', h=520, merlon=True))
    # đoạn tường Tống: ngói + cờ lam
    L.append(pennant(1000, 300, 560, PEN_S))
    L.append(pennant(1500, 330, 560, PEN_S))
    L.append(ground('day', 860, '#7a6a3f'))
    # dốc đất đắp dần
    L.append(G('ramp', '<polygon points="500,1080 1500,1080 1360,800 760,760 600,780" fill="#9a7a4a"/><polygon points="760,760 1360,800 1420,860 700,830" fill="#b09258"/>'))
    L.append(G('sacks', sacks(1000, 800, .9, 6) + sacks(960, 780, .9, 4)))
    # lính khiêng bao đất, nhìn từ sau, nhỏ
    o = ''
    r = random.Random(2)
    for i in range(9):
        x = 300 + i * 150 + r.randint(-20, 20)
        y = 960 + (i % 3) * 40
        sc = 1.15 - (i % 3) * 0.12
        o += soldier(x, y, sc, i + 3, back=True, pose='hands', pen=False)
        o += f'<ellipse cx="{x+8*sc}" cy="{y-150*sc*0.9}" rx="{30*sc}" ry="{20*sc}" fill="#b09a68" transform="rotate(-18 {x} {y})"/>'
    L.append(G('carriers', o))
    return svg(L, 'day')


@scene(19003)
def _(): 
    L = outdoor('day', sun=(960, 240))
    L.append(ground('day', 820, '#62793f'))
    # trái: đồi xanh + làng tranh + cờ nâu đỏ
    L.append(G('left', '<ellipse cx="320" cy="860" rx="520" ry="150" fill="#6f9a4a"/><ellipse cx="560" cy="880" rx="380" ry="110" fill="#5f8a3e"/>'))
    L.append(huts('day', [(180, 840, .9), (360, 850, 1.1), (540, 835, .8)]))
    L.append(tree(90, 860, .9))
    L.append(pennant(700, 520, 840, PEN_V, 140))
    L.append(soldier(780, 900, 1.4, 5, pen=False, pose='hands'))
    # phải: pháo đài khổng lồ nhiều tầng + cờ lam
    L.append(G('right', '<rect x="1060" y="560" width="860" height="320" fill="#6a7684"/>'))
    for r in range(0, 8):
        L.append(f'<line x1="1060" y1="{580+r*40}" x2="1920" y2="{580+r*40}" stroke="#56606c" stroke-width="2"/>')
    L.append(pagoda(1500, 560, 1.7, '#566070', '#16202c', '#2e3a48', glow=False))
    L.append(pennant(1160, 300, 560, PEN_S, 140))
    L.append(soldier(1240, 920, 1.4, 6, side='song', pen=False, pose='hands'))
    L.append(wall(860, 'grey', side='song', h=220, merlon=False)) if False else None
    return svg([l for l in L if l], 'day')


@scene(19004)
def _():
    L = outdoor('dusk', sun=(1480, 430), cl=2, birds_=(1100, 250))
    L.append(huts('dusk', [(250, 860, .55), (470, 860, .7), (1250, 860, .6), (1560, 860, .75)]))
    L.append(tree(80, 880, 1, 'dusk'))
    L.append(tree(1840, 880, 1.1, 'dusk'))
    L.append(ground('dusk', 860))
    L.append(wall(780, 'dusk', tower_x=330, side='viet'))
    for x, hh in ((820, 260), (1260, 300), (1640, 250)):
        L.append(pennant(x, 780 - hh, 780, PEN_V))
    L.append(P('LTK_G', 1020, 786, 2.3, pose='hands', look=-1))
    L.append(torch(240, 790)); L.append(torch(1700, 790))
    return svg(L, 'dusk')


@scene(19007)
def _():
    L = [hall('gold')]
    L.append(throne(960, 830))
    L.append(sit('TT', 960, 780, 1.9, pose='hands'))
    L.append(mat('560,946 1360,946 1560,1080 360,1080'))
    L.append(P('LTK_T', 640, 1010, 2.4, pose='hands'))
    L.append(oildish(470, 740)); L.append(oildish(1470, 740))
    return svg(L)


@scene(19008)
def _():
    L = outdoor('day', sun=(1500, 300), cl=3)
    L.append(ground('day', 860, '#a9a090'))
    L.append(G('hall', pagoda(960, 560, 2.1, '#9a8a78', '#4a3a34', '#6a5a50')))
    # bậc đá
    o = ''
    for i in range(9):
        w = 520 + i * 90
        o += f'<rect x="{960-w/2}" y="{560+i*50}" width="{w}" height="52" fill="{sh("#b8ad98",1-i*0.03)}"/><rect x="{960-w/2}" y="{560+i*50}" width="{w}" height="8" fill="#d4cab4"/>'
    L.append(G('steps', o))
    L.append(P('LTK_T', 960, 800, 1.9, col='#1f3a5c', turban='#14121a', pose='hands'))  # lớn hơn, áo xanh đậm hơn, đội khăn cao hơn
    L.append(torch(520, 700)); L.append(torch(1400, 700))
    return svg(L, 'day')


@scene(19009)
def _():
    L = outdoor('day', sun=(400, 280), cl=4)
    L.append(ground('day', 860, '#8a7a5a'))
    L.append(wall(620, 'day', tower_x=420, side='viet', h=420))
    L.append(road_back('day', 820))
    # hai lính đi sau, lệch nhau
    L.append(horse(1480, 930, 0.95, '#6a4a2e', facing=1))
    L.append(rider('OFF2', 1480, 930, .95, col='#5a4a2e', hat='cone', turban=None, pose='hands', seed=31, sash='#8a2a24', **{}) if False else '')
    L.append(horse(1700, 960, 1.0, '#8a6a4a', facing=1))
    L.append(sit({'col': '#6b4a2e', 'hat': 'cone', 'seed': 32, 'sash': '#8a2a24'}, 1700, 960 - 205 + 30, 1.0, pose='hands'))
    L.append(horse(1240, 940, 0.98, '#5a3a24', facing=1))
    L.append(sit({'col': '#7a5634', 'hat': 'cone', 'seed': 33, 'sash': '#6a8a3a'}, 1240, 940 - 205 + 30, .98, pose='hands'))
    # sứ giả ở trước, cầm gậy tiết có tua
    L.append(horse(800, 990, 1.25, '#3a2a22', facing=1))
    L.append(sit('LTK_T', 800, 990 - 256 + 38, 1.25, pose='hands'))
    L.append(G('staff', '<line x1="905" y1="990" x2="905" y2="520" stroke="#6b4a2a" stroke-width="7"/><path d="M905,520 l0,-24 M905,520 l-14,-22 M905,520 l14,-22" stroke="#e0b040" stroke-width="6"/>'
               '<path class="pen" d="M905,540 q50,10 90,-4 q-10,34 -28,70 q-30,-20 -62,-26Z" fill="#c0392b"/>'
               '<path d="M905,610 l-6,50 M905,610 l6,50 M905,610 l0,56" stroke="#c0392b" stroke-width="4"/>'))
    L.append(dust(1200, 1050, 600))
    return svg(L, 'day')


@scene(19010)
def _():
    L = outdoor('day', sun=(1500, 280), cl=5, birds_=(1200, 200))
    L.append(rice(790))
    L.append(huts('day', [(260, 812, .8), (520, 812, .6), (1360, 812, .7), (1640, 812, .9)]))
    L.append(tree(120, 815, 1.1)); L.append(bamboo(1700, 850, 1.3))
    L.append(road_back('day'))
    # dân hai bên đường, mỗi người một vẻ
    o = ''
    cols = PCOL
    for i, (x, y, s) in enumerate(((560, 900, 1.2), (480, 960, 1.45), (1360, 900, 1.2), (1450, 970, 1.5), (640, 830, .9), (1290, 830, .9))):
        o += person(x, y, s, cols[i % 7], hat='cone' if i % 2 else None, turban='#5a4128' if i % 2 == 0 else None, seed=40 + i,
                    pose='up' if i % 2 == 0 else 'hands', sash=SASHV[i % 5], beard='goatee' if i == 3 else None)
    L.append(G('villagers', o))
    # ba người chính
    L.append(P('OFF3', 770, 1030, 2.3, col='#4a3a2a', pose='hands', beard='long'))  # tuỳ tùng gầy, râu dài
    L.append(P('LTK_T', 960, 1050, 2.5, pose='hands'))
    L.append(P('OFF2', 1150, 1030, 2.0, col='#5a4a3a', young=False, beard=None, long=False, pose='hands', seed=19))  # lùn tròn, không râu
    return svg(L, 'day')


@scene(19014)
def _():
    L = outdoor('day', sun=(400, 300), cl=6)
    L.append(rice(790))
    L.append(huts('day', [(300, 812, .6), (1500, 812, .7)]))
    L.append(bamboo(60, 830, 1.2)); L.append(bamboo(1720, 850, 1.4))
    L.append(road_back('day'))
    L.append(rows([(792, .5, 6), (830, .7, 6), (884, .95, 5), (968, 1.35, 4), (1070, 1.85, 3)], back=True, seed=2))
    L.append(dust(960, 1040, 900, .22))
    return svg(L, 'day')


@scene(19015)
def _():
    L = outdoor('day', sun=(1500, 300), cl=7)
    L.append(rice(790))
    L.append(road_back('day'))
    L.append(rows([(800, .45, 7), (840, .6, 7)], back=False, seed=6))
    L.append(horse(960, 1000, 1.7, '#4a2e22', facing=1))
    L.append(sit('LTK_G', 960, 1000 - 350 + 52, 1.7, pose='hands'))
    # kiếm trong bao đeo hông
    L.append(f'<path d="M{960-30},{1000-350+60} l-60,54 l10,10 l60,-50Z" fill="#2a1d1a"/><rect x="{960-34}" y="{1000-350+52}" width="14" height="14" fill="#e0b040"/>')
    L.append(pennant(1500, 560, 960, PEN_V, 150))
    L.append(dust(900, 1040, 700))
    return svg(L, 'day')


@scene(19016)
def _():
    # trong lều: vải lều, bàn thấp có bản đồ nét, vua đứng xem; bên phải mở cửa lều thấy lính nghỉ
    L = ['<rect width="1920" height="1080" fill="#8a7a58"/>']
    o = '<polygon points="0,0 1920,0 1920,120 960,60 0,120" fill="#6a5a3c"/>'
    for k in range(0, 1920, 120):
        o += f'<line x1="{k}" y1="0" x2="{960+(k-960)*0.4}" y2="{120-abs(k-960)/16}" stroke="#5a4a2e" stroke-width="3" opacity=".5"/>'
    L.append(G('canvas', o))
    L.append('<rect y="120" width="1920" height="960" fill="#a89468"/>')
    L.append('<rect y="940" width="1920" height="140" fill="#6a4a2a"/>')
    L.append('<polygon points="1240,150 1800,150 1800,940 1240,940" fill="#2a1d1a"/>')
    L.append(G('door', f'<rect x="1270" y="170" width="500" height="740" fill="url(#sk)"/><rect x="1270" y="700" width="500" height="210" fill="#62793f"/>'))
    L.append(sit({'col': '#6b4a2e', 'hat': 'cone', 'seed': 51, 'sash': '#c0392b'}, 1420, 900, 1.2, pose='hands'))
    L.append(sit({'col': '#5c4228', 'hat': 'cone', 'seed': 52, 'sash': '#6a8a3a', 'beard': 'goatee'}, 1620, 920, 1.2, pose='hands'))
    L.append(P('TTG', 640, 920, 2.6, pose='point', look=1))
    L.append(maptable(900, 1000, 360))
    L.append(oildish(300, 760)); L.append(oildish(1100, 740))
    return svg(L, 'day')


@scene(19017)
def _():
    L = outdoor('day', sun=(300, 260), cl=9)
    L.append(ground('day', 780, '#b8ad98'))
    L.append(G('hall', pagoda(960, 740, 2.3, '#9a8a78', '#4a3a34', '#6a5a50')))
    L.append(P('YL', 960, 1010, 2.5, pose='hands'))
    # giỏ gạo
    for x, y in ((760, 1030), (1160, 1040)):
        L.append(f'<ellipse cx="{x}" cy="{y}" rx="70" ry="22" fill="#7a5a3a"/><path d="M{x-70},{y} Q{x},{y-70} {x+70},{y}Z" fill="#f4eee0"/>')
    for i, (x, y, s, c) in enumerate(((420, 1000, 1.45, '#6b4a2e'), (600, 1050, 1.5, '#4a5a3a'), (1330, 1050, 1.5, '#7a5a3a'), (1510, 1000, 1.45, '#5a4a6a'))):
        L.append(kneeler(x, y, s, c, turban=['#5a4128', '#14121a', '#6a4a2e', '#3a2a1a'][i], seed=60 + i))
    return svg(L, 'day')


@scene(19018)
def _():
    L = outdoor('dawn', sun=(960, 520), cl=10, mt=660)
    L.append(rice(800, 7, '#4a5a3a', '#6f8a47'))
    L.append(road(' dawn'.strip(), (700, 1220), 800))
    L.append(rows([(820, .55, 8), (860, .7, 8), (920, .9, 7), (1000, 1.2, 6)], back=True, seed=4, pen=True))
    L.append(P('TTG', 960, 1040, 3.0, pose='hands', look=-1))
    return svg(L, 'dawn')


@scene(19019)
def _():
    L = outdoor('day', sun=(960, 260), cl=11)
    L.append(ground('day', 780, '#9a8a4f'))
    L.append(G('field', '<rect y="780" width="1920" height="300" fill="#a8984f"/>'))
    r = random.Random(9)
    o = ''
    for i in range(14):
        x = 120 + i * 62
        o += soldier(x, 880 + (i % 3) * 36, .8, i, 'viet', pen=(i % 2 == 0), penc=PEN_V, pose='spear')
    for i in range(14):
        x = 1800 - i * 62
        o += soldier(x, 880 + (i % 3) * 36, .8, i + 20, 'viet', pen=(i % 2 == 0), penc=PEN_O, pose='spear')
    L.append(G('armies', o))
    L.append(dust(500, 940, 360, .3)); L.append(dust(1420, 940, 360, .3)); L.append(dust(960, 920, 220, .4))
    return svg(L, 'day')


@scene(19020)
def _():
    L = outdoor('day', sun=(300, 260), cl=12)
    L.append(ground('day', 760, '#b8ad98'))
    L.append(G('temple', pagoda(960, 700, 2.4, '#8a5a4a', '#3a2a2a', '#5a4040')))
    o = ''
    for i in range(6):
        w = 420 + i * 70
        o += f'<rect x="{960-w/2}" y="{700+i*28}" width="{w}" height="30" fill="{sh("#b8ad98",1-i*.04)}"/>'
    L.append(G('steps', o))
    L.append(P('TTG', 960, 740, 1.5, pose='hands'))
    # bốn tù binh cúi đầu, một hàng; người đầu là vua Chăm-pa
    xs = (520, 700, 880, 1060)
    L.append(P('CC', 1060, 1030, 2.1, face=False, pose='hands'))
    L.append(person(880, 1030, 2.1, '#6a5a4a', face=False, seed=71, pose='hands', turban='#3a2a1a'))
    L.append(person(700, 1030, 2.1, '#4a5a6a', face=False, seed=72, pose='hands', turban='#14121a'))
    L.append(person(520, 1030, 2.1, '#7a5a3a', face=False, seed=73, pose='hands', turban='#5a4128'))
    return svg(L, 'day')


@scene(19022)
def _():
    L = [hall('gold')]
    L.append(throne(960, 830))
    L.append(sit('TTG', 960, 780, 1.9, pose='hands'))
    L.append(mat('560,946 1360,946 1560,1080 360,1080'))
    L.append(knee('LTK_G', 960, 1040, 1.7))
    L.append(P('LDT', 380, 1000, 2.3, pose='hands'))
    L.append(P('LVT', 1560, 1000, 2.3, pose='hands'))
    L.append(oildish(470, 740)); L.append(oildish(1470, 740))
    return svg(L)


@scene(19023)
def _():
    L = outdoor('grey', cl=13)
    L.append(ground('grey', 800, '#a8a090'))
    for x in (300, 960, 1620):
        L.append(pagoda(x, 720, 1.5, '#8a8078', '#34383e', '#505860', glow=False))
    L.append(G('court', '<rect y="720" width="1920" height="360" fill="#b0a898"/>'))
    # kiệu gỗ trên hai đòn, bốn người khiêng áo gai trắng, nhìn từ xa
    L.append(G('bier', '<rect x="560" y="780" width="840" height="14" fill="#6a4a2a"/><rect x="560" y="830" width="840" height="14" fill="#6a4a2a"/>'
               '<rect x="700" y="690" width="560" height="100" fill="#8a6a44"/><rect x="700" y="690" width="560" height="14" fill="#6a4a2a"/><rect x="740" y="660" width="480" height="40" fill="#efe9dc"/>'))
    for i, x in enumerate((600, 800, 1160, 1360)):
        L.append(person(x, 960, 1.15, '#f1ede2', back=True, seed=80 + i, pose='hands', sash='#d8d2c4', turban='#f1ede2'))
    for i in range(7):
        L.append(person(300 + i * 220, 1040, 1.1, '#e8e3d6', back=True, seed=90 + i, pose='hands', sash='#d8d2c4', turban='#e8e3d6'))
    return svg(L, 'grey')


@scene(19024)
def _():
    L = [hall('gold')]
    L.append(throne(960, 830))
    # rèm sau ngai: hai bóng người phụ nữ
    L.append(G('curtain', '<rect x="360" y="260" width="360" height="640" fill="#d9a84a" opacity=".85"/><rect x="360" y="260" width="360" height="640" fill="none" stroke="#8a2a24" stroke-width="10"/>'
               + ''.join(f'<line x1="{360+k*60}" y1="260" x2="{360+k*60}" y2="900" stroke="#b8862e" stroke-width="3"/>' for k in range(1, 6))))
    L.append(G('shadows', '<g fill="#3a1f18" opacity=".8"><circle cx="470" cy="520" r="30"/><circle cx="470" cy="492" r="14"/><path d="M420,640 Q470,540 520,640 L540,900 L400,900Z"/>'
               '<circle cx="600" cy="540" r="30"/><circle cx="600" cy="512" r="14"/><path d="M550,660 Q600,560 650,660 L670,900 L530,900Z"/></g>'))
    L.append(sit('NT', 960, 782, 1.9, pose='hands'))
    L.append(P('LDT', 1500, 1000, 2.3, pose='hands'))
    L.append(mat('560,946 1360,946 1560,1080 360,1080'))
    L.append(oildish(1130, 740)); 
    return svg(L)


@scene(19025)
def _():
    L = [hall('gold', curtains=False)]
    L.append(throne(960, 830))
    L.append(sit('NT', 960, 782, 1.7, pose='hands'))
    L.append(mat('460,946 1460,946 1660,1080 260,1080'))
    groups = [('#2e4a7a', 'OFF3', (330, 520)), ('#7a5a3a', 'OFF1', (1180, 1380)), ('#3a6a4a', 'OFF2', (1560, 1730))]
    spec = [
        (330, 1000, 2.0, '#2e4a7a', dict(beard='white_goatee', hair='#d8d8dc', seed=101)),
        (480, 1040, 2.1, '#3a5a8a', dict(seed=102, young=True)),
        (610, 1000, 2.0, '#27406a', dict(beard='goatee', seed=103)),
        (1150, 1010, 2.0, '#7a5a3a', dict(seed=104, beard='mustache')),
        (1290, 1050, 2.1, '#8a6a44', dict(seed=105, beard='white_long', hair='#e9e4dc')),
        (1430, 1010, 2.0, '#6a4a2e', dict(seed=106, young=True)),
        (1580, 1000, 2.0, '#3a6a4a', dict(seed=107, beard='thick')),
        (1720, 1040, 2.1, '#4a7a5a', dict(seed=108)),
        (1860, 1000, 1.9, '#2e5a3a', dict(seed=109, beard='goatee')),
    ]
    for x, y, s, c, kw in spec:
        L.append(person(x, y, s, c, turban='#14121a', sash='#c9a45e', pose='hands', **kw))
    return svg(L)


@scene(19028)
def _():
    L = [hall('gold')]
    L.append(mat('560,946 1360,946 1560,1080 360,1080'))
    L.append(knee('LTK_G', 760, 1030, 1.7))
    # quan lễ trao ấn
    L.append(P('OFF1', 1160, 1010, 2.3, pose='hands'))
    L.append(f'<rect x="1130" y="740" width="60" height="50" rx="6" fill="#e0b040" stroke="#a9781d" stroke-width="4"/><rect x="1148" y="716" width="24" height="28" rx="6" fill="#e0b040"/>')
    L.append(oildish(470, 740)); L.append(oildish(1470, 740))
    return svg(L)


def _song_hall():
    return [hall('gold', curtain='#2e4a80', windows=(330, 1590))]


@scene(19029)
def _():
    L = _song_hall()
    L.append(throne(960, 830, seat='#2e4a80'))
    L.append(sit('SK', 960, 780, 1.9, pose='hands'))
    L.append(mat('560,946 1360,946 1560,1080 360,1080', '#8a8a9a'))
    L.append(P('VAT', 1400, 1010, 2.5, pose='hands'))
    L.append(scroll_blank(1355, 900, 1.6))
    L.append(oildish(470, 740)); L.append(oildish(1470, 740))
    return svg(L)


@scene(19030)
def _():
    L = [hall('dim', curtains=False)]
    # bình phong gấp, tranh núi nét đơn giản
    o = ''
    for i in range(4):
        x = 560 + i * 200
        o += f'<rect x="{x}" y="280" width="190" height="640" fill="#d8c8a0" stroke="#5a3a2a" stroke-width="8"/>'
        o += f'<path d="M{x+10},{780} L{x+70},{660} L{x+110},{720} L{x+160},{620} L{x+180},{780}Z" fill="#8a9a8a" opacity=".8"/>'
    L.append(G('screen', o))
    L.append(sit('SK', 1280, 880, 3.0, pose='hands', look=-1))
    L.append(P('VAT', 700, 1030, 3.0, pose='hands', look=1))
    L.append(mat('300,946 1620,946 1800,1080 120,1080', '#8a8a9a'))
    return svg(L)


@scene(19031)
def _():
    L = _song_hall()
    L.append(mat('360,946 1560,946 1700,1080 220,1080', '#8a8a9a'))
    L.append(maptable(800, 1020, 520))
    L.append(P('VAT', 620, 1000, 2.6, pose='point', look=1))
    L.append(P('SK', 1280, 1000, 2.4, pose='hands', look=-1))
    L.append(oildish(300, 760)); L.append(oildish(1620, 760))
    return svg(L)


@scene(19033)
def _():
    L = outdoor('grey', cl=14)
    L.append(ground('grey', 800))
    L.append(wall(700, 'grey', tower_x=960, side='song', h=380))
    L.append(pennant(560, 380, 700, PEN_S)); L.append(pennant(1500, 380, 700, PEN_S))
    L.append(road('grey', (900, 1020), 840, '#8a7a62'))
    L.append(P('TK', 760, 1040, 2.4, pose='hands'))
    L.append(P('LD', 1160, 1040, 2.4, pose='hands'))
    return svg(L, 'grey')


@scene(19034)
def _():
    L = outdoor('day', sun=(1500, 280), cl=15)
    L.append(river(780, 1080))
    L.append(G('bank', '<rect y="700" width="1920" height="130" fill="#7a6a3f"/>'))
    # thân thuyền đang đóng: sườn gỗ
    o = '<path d="M300,900 Q600,980 1000,900 L940,780 Q600,830 360,780Z" fill="#8a6a44"/>'
    for k in range(9):
        o += f'<line x1="{360+k*70}" y1="{790+abs(k-4)*6}" x2="{340+k*72}" y2="{930-abs(k-4)*6}" stroke="#5a3a24" stroke-width="10"/>'
    o += '<rect x="280" y="900" width="740" height="14" fill="#5a3a24"/>'
    L.append(G('hull', o))
    L.append(G('bankF', '<rect y="940" width="1920" height="140" fill="#8a7a4a"/><rect y="936" width="1920" height="8" fill="#a08e5a"/>'))
    L.append(G('workers', ''.join(person(x, y, 1.6, cc, crown='headband', seed=110 + i, beard=bd, pose='hands', sash='#6a4a2a') for i, (x, y, cc, bd) in enumerate(((240, 1030, '#7a5a3a', None), (520, 1050, '#6a5a4a', 'goatee'), (1020, 1040, '#8a6a4a', None), (1300, 1050, '#5a4a3a', 'mustache'))))))
    # lính Tống tập đội hình ở xa
    L.append(G('drill', ''.join(soldier(1260 + i * 70, 800, .5, i + 40, 'song', pen=False, pose='hands') for i in range(8))))
    return svg(L, 'day')


@scene(19036)
def _():
    L = outdoor('day', sun=(400, 280), cl=16)
    L.append(ground('day', 760, '#8a7a5a'))
    L.append(rows([(800, .7, 9), (850, .85, 8)], back=True, seed=3, pen=True, base=780, spread=3.2))
    L.append(P('DTN', 960, 960, 2.0, pose='hands'))
    L.append(scroll_blank(960, 850, 3.2))
    L.append(rows([(1010, 1.5, 3), (1070, 1.8, 3)], back=True, seed=12, pen=True, base=780, spread=3.2))
    return svg(L, 'day')


@scene(19037)
def _():
    L = outdoor('day', sun=(1500, 280), cl=17)
    L.append(rice(790, 8, '#5f8a3e', '#86b04e'))
    L.append(huts('day', [(300, 812, .8), (1560, 812, .9)]))
    L.append(P('TG', 1180, 1030, 2.4, col='#3a7a7a', pose='hands', seed=36, beard=None, hair='#14121a'))
    L.append(scroll_blank(1130, 900, 1.5))
    L.append(person(700, 1030, 2.3, '#7a5a3a', hat='cone', seed=37, pose='hands', sash='#6a4a2a', beard='white_goatee'))
    L.append('<g><path d="M940,880 q30,-26 60,0 q0,30 -30,34 q-30,-4 -30,-34Z" fill="#8a6a44"/><path d="M958,872 q12,-14 24,0" stroke="#5a3a24" stroke-width="3" fill="none"/></g>')
    return svg(L, 'day')


@scene(19038)
def _():
    L = [sky('day', sun=(1700, 160)), clouds('day', 18, 4)]
    L.append('<rect y="0" width="1920" height="1080" fill="#7aa05a"/>')
    L.append('<polygon points="0,200 760,200 560,1080 0,1080" fill="#5f95b0"/>')  # sông, nhìn từ trên cao
    L.append(G('road', '<polygon points="1040,150 1220,150 1500,1080 1060,1080" fill="#b8905f"/>'))
    L.append(G('boats', ''.join(boat(220 + (i % 2) * 150, 330 + i * 130, .6) for i in range(5))))
    o = ''
    for i in range(18):
        x = 1130 + (i % 3) * 36 + i * 12
        y = 230 + i * 46
        o += soldier(x, y, .55, i + 60, pen=(i % 3 == 0), pose='spear')
    L.append(G('column', o))
    for x, y in ((820, 300), (870, 700), (1580, 400)):
        L.append(tree(x, y, .6))
    return svg(L, 'day')


@scene(19040)
def _():
    L = outdoor('day', sun=(300, 260), cl=19)
    L.append(river(700, 1080, 'day'))
    L.append(G('shore', '<polygon points="0,700 1920,700 1920,800 1500,860 0,820" fill="#c9b283"/><rect y="760" width="1920" height="40" fill="#b09a68"/>'))
    L.append(huts('day', [(1360, 770, .8), (1560, 765, .7), (1740, 770, .9)]))
    L.append(tree(1840, 780, .8))
    L.append(boat(400, 920, 1.2)); L.append(boat(820, 880, 1.0)); L.append(boat(1180, 940, 1.1))
    # hàng dân được dẫn đi, từ xa và từ sau, bình thản
    L.append(G('line', ''.join(person(700 + i * 85, 790 + (i % 2) * 8, .62, PCOL[i % 7], back=True, seed=120 + i, pose='hands', hat='cone' if i % 2 else None, turban='#5a4128' if i % 2 == 0 else None) for i in range(8))))
    L.append(G('guards', ''.join(soldier(660 + i * 300, 830, .7, i + 70, back=True, pen=False, pose='spear') for i in range(3))))
    return svg(L, 'day')


@scene(19042)
def _():
    L = outdoor('grey', cl=20)
    L.append(ground('grey', 780, '#7a7a5a'))
    L.append(road('grey', (720, 1200), 790, '#8a7a62'))
    L.append(rows([(800, .45, 8), (830, .55, 8)], side='song', seed=8, penc=PEN_S))
    L.append(horse(900, 1010, 1.8, '#5a3a2a', facing=1))
    L.append(sit('TTT', 900, 1010 - 369 + 55, 1.8, pose='hands'))
    L.append(pennant(1500, 540, 960, PEN_S, 150))
    L.append(dust(900, 1040, 700, .25))
    return svg(L, 'grey')


@scene(19043)
def _():
    L = [sky('day'), clouds('day', 21, 3)]
    L.append(G('cliffL', '<polygon points="0,0 560,0 680,500 520,1080 0,1080" fill="#6a6258"/><polygon points="0,200 380,0 560,0 640,420 0,640" fill="#7a7266"/>'))
    L.append(G('cliffR', '<polygon points="1920,0 1360,0 1240,500 1400,1080 1920,1080" fill="#6a6258"/><polygon points="1920,200 1540,0 1360,0 1280,420 1920,640" fill="#7a7266"/>'))
    L.append(G('valley', '<polygon points="680,500 1240,500 1400,1080 520,1080" fill="#a8946a"/>'))
    for x, y, w in ((300, 900, 160), (520, 800, 120), (180, 700, 140)):
        L.append(f'<ellipse cx="{x}" cy="{y}" rx="{w}" ry="{w*.6}" fill="#58524a"/>')
    # quân nâu đỏ nấp sau đá bên trái, chỉ thấy nửa người
    for i, (x, y) in enumerate(((300, 900), (520, 800), (180, 700))):
        L.append(f'<g>{soldier(x, y + 20, 1.0, i + 80, pen=(i == 0), pose="spear")}</g>')
        L.append(f'<ellipse cx="{x}" cy="{y+60}" rx="{160 if i==0 else 120}" ry="{96 if i==0 else 72}" fill="#58524a"/>')
    # quân lam hành quân bên phải
    L.append(G('blue', ''.join(soldier(1500 + (i % 2) * 90, 700 + i * 70, .8 + i * .1, i + 90, 'song', pen=(i % 2 == 0), pose='spear') for i in range(5))))
    L.append(dust(1500, 1000, 400, .3))
    return svg(L, 'day')


@scene(19044)
def _():
    L = outdoor('day', sun=(300, 260), cl=22)
    L.append(ground('day', 760, '#8a7a4a'))
    L.append(wall(620, 'grey', tower_x=1450, side='song', h=170, merlon=True))
    r = random.Random(4)
    o = ''
    for row, (y, s) in enumerate(((820, .5), (870, .65), (930, .85), (1000, 1.1))):
        for k in range(0, 1920, int(180 * s) + 20):
            o += tent(k + r.randint(0, 40), y, s, col=['#9a8a68', '#a89870', '#8a7a58'][(k // 100 + row) % 3])
    L.append(G('tents', o))
    L.append(pennant(500, 520, 840, PEN_V)); L.append(pennant(1100, 540, 840, PEN_V))
    L.append(P('TD', 860, 1060, 2.7, pose='hands', look=1))
    return svg(L, 'day')


@scene(19045)
def _():
    L = outdoor('smoke', sun=(500, 460), cl=23, mt=700)
    L.append(ground('smoke', 860))
    L.append(P('TG', 960, 860, 2.5, pose='hands', look=0))
    L.append(wall(780, 'smoke', tower_x=None, side='song', h=300))
    L.append(pennant(300, 450, 780, PEN_S)); L.append(pennant(1620, 450, 780, PEN_S))
    return svg(L, 'smoke')


@scene(19046)
def _():
    L = [sky('grey'), clouds('grey', 24, 4)]
    # băng trời: mặt trời và trăng nối nhau theo một cung, nói về ngày tháng trôi
    o = ''
    for i in range(6):
        x = 260 + i * 280
        y = 250 - abs(i - 2.5) * 20
        if i % 2 == 0:
            o += f'<circle cx="{x}" cy="{y}" r="58" fill="#ffd9a0" opacity=".95"/><circle cx="{x}" cy="{y}" r="96" fill="#ffd9a0" opacity=".2"/>'
        else:
            o += f'<circle cx="{x}" cy="{y}" r="52" fill="#e8eeff"/><circle cx="{x+20}" cy="{y-8}" r="44" fill="#9fa8b0"/>'
    L.append(G('days', o))
    L.append(ground('grey', 900))
    L.append(wall(420, 'grey', tower_x=1560, side='song', h=480))
    r = random.Random(6)
    t = ''
    for row, (y, s) in enumerate(((930, .55), (980, .7), (1040, .9))):
        n = 5 + row * 2
        for k in range(n):
            t += tent(120 + k * (1700 / n) + r.randint(0, 30), y, s, col=['#9a8a68', '#a89870', '#8a7a58'][(k + row) % 3])
    L.append(G('tents', t))
    return svg(L, 'grey')


@scene(19047)
def _():
    L = outdoor('grey', cl=25, mt=700)
    L.append(ground('grey', 860))
    L.append(wall(500, 'grey', tower_x=1400, side='song', h=420))
    L.append(G('ramp', '<polygon points="200,1080 1800,1080 1500,700 900,600 560,780" fill="#9a8450"/><polygon points="900,600 1500,700 1560,760 840,680" fill="#b09a68"/>'))
    L.append(G('sacks', sacks(1100, 860, 1.2, 6) + sacks(920, 780, 1.0, 4) + sacks(1260, 780, 1.0, 4) + sacks(720, 940, 1.2, 5)))
    for i, (x, y) in enumerate(((560, 960), (760, 1020), (1360, 1010), (1560, 950))):
        L.append(soldier(x, y, .85, i + 100, back=True, pose='hands', pen=False))
        L.append(f'<ellipse cx="{x+8}" cy="{y-128*.85}" rx="30" ry="20" fill="#b09a68" transform="rotate(-18 {x} {y})"/>')
    return svg(L, 'grey')


@scene(19048)
def _():
    L = [sky('smoke'), clouds('smoke', 26, 4), mountains('smoke', 700, 4)]
    L.append(ground('smoke', 880))
    L.append(wall(620, 'smoke', tower_x=960, side='song', h=400))
    big = ''
    for x in (780, 960, 1160):
        big += f'<ellipse class="smoke" cx="{x}" cy="300" rx="130" ry="200" fill="#1c1614" opacity=".75"/><ellipse class="smoke" cx="{x+40}" cy="140" rx="180" ry="150" fill="#2a201c" opacity=".6"/>'
    big += '<ellipse cx="960" cy="520" rx="320" ry="90" fill="#ff7a2a" opacity=".35"/>'
    L.append(G('smoke', big))
    L.append(road('smoke', (900, 1020), 880, '#6a4a38'))
    return svg(L, 'smoke')


@scene(19051)
def _():
    L = [sky('smoke'), clouds('smoke', 27, 4), mountains('smoke', 640, 6)]
    L.append(ground('smoke', 780, '#5a4030'))
    L.append(road('smoke', (700, 1220), 780, '#7a5a40'))
    L.append(wall(620, 'smoke', tower_x=1450, side='song', h=170))
    L.append(cart_overturned(860, 960, 2.2))
    L.append(smoke(1500, 600, 300, '#1c1614', .6, 22)); L.append(smoke(1300, 620, 260, '#2a201c', .5, 18))
    L.append(bamboo(80, 850, 1.1, 'smoke'))
    return svg(L, 'smoke')


@scene(19052)
def _():
    L = outdoor('dusk', sun=(960, 480), cl=28, mt=680)
    L.append(rice(800, 7, '#3a3a40', '#4a4a56'))
    L.append(road_back('dusk', 800))
    r = random.Random(7)
    o = ''
    for row, (y, s, n) in enumerate(((810, .5, 9), (850, .65, 8), (910, .85, 6), (1000, 1.1, 4), (1070, 1.45, 3))):
        wid = 300 + (y - 800) * 2.1
        for k in range(n):
            x = 960 - wid / 2 + (k + .5) * wid / n + r.randint(-14, 14)
            c = PCOL[(k + row) % 7]
            o += person(x, y, s, c, back=True, seed=130 + row * 10 + k, hat='cone' if (k + row) % 2 else None, turban='#5a4128' if (k + row) % 2 == 0 else None, pose='hands', sash=SASHV[k % 5])
            o += f'<line x1="{x-18*s}" y1="{y-130*s}" x2="{x+22*s}" y2="{y-150*s}" stroke="#4a3220" stroke-width="{3*s}"/><ellipse cx="{x+22*s}" cy="{y-146*s}" rx="{12*s}" ry="{9*s}" fill="#8a6a44"/>'
    L.append(G('people', o))
    L.append(G('escort', ''.join(soldier(560 + i * 400, 790, .42, i + 110, back=True, pen=False, pose='hands') for i in range(3))))
    return svg(L, 'dusk')


@scene(19053)
def _():
    L = outdoor('day', sun=(300, 260), cl=29, mt=700)
    L.append(ground('day', 840, '#8a7a5a'))
    # nhà ngói xám
    L.append(G('house', '<rect x="620" y="560" width="680" height="300" fill="#8a8680"/><path d="M560,570 Q700,560 760,470 L1160,470 Q1220,560 1360,570 L1300,610 L620,610Z" fill="#4a4e54"/>'
               + ''.join(f'<line x1="{600+k*50}" y1="470" x2="{570+k*56}" y2="590" stroke="#34383e" stroke-width="3"/>' for k in range(14))
               + '<rect x="900" y="660" width="120" height="200" fill="#2a1d1a"/>'))
    L.append(P('TG', 1400, 1040, 2.3, col='#3a7a7a', pose='hands', seed=39, hair='#14121a'))
    L.append('<rect x="1250" y="880" width="110" height="26" rx="6" fill="#8a2a24"/><rect x="1262" y="866" width="86" height="18" rx="5" fill="#e0b040"/>')
    L.append(person(700, 1040, 2.0, '#efe9dc', seed=140, pose='hands', hair='#cfcfd4', long=True, sash='#d8d2c4', turban='#efe9dc'))
    L.append(person(880, 1060, 1.3, '#9a8a6a', seed=141, pose='hands', sash='#c0392b', young=True))
    L.append(person(1050, 1060, 1.65, '#6a8aa0', seed=142, pose='hands', sash='#d08a2e'))
    return svg(L, 'day')


@scene(19054)
def _():
    L = _song_hall()
    L.append(throne(960, 830, seat='#2e4a80'))
    L.append(sit('SK', 960, 780, 1.9, pose='hands'))
    L.append(mat('560,946 1360,946 1560,1080 360,1080', '#8a8a9a'))
    L.append(kneeler(740, 1040, 1.7, '#6a7284', turban='#14121a', seed=26, hat='helmet'))
    L.append(kneeler(1180, 1040, 1.6, '#5a5a70', turban='#14121a', seed=27, hat='helmet'))
    L.append(oildish(470, 740)); L.append(oildish(1470, 740))
    return svg(L)


@scene(19055)
def _():
    L = outdoor('day', sun=(960, 240), cl=30, mt=700)
    L.append(ground('day', 800, '#a8984f'))
    cols = ['#2e4a80', '#8a2a24', '#d9892e', '#3a6a4a', '#6a3a7a', '#e0b040', '#2e6a6a', '#7a7a80', '#a84a7a']
    o = ''
    for i, c in enumerate(cols):
        x = 120 + i * 205
        o += f'<line x1="{x}" y1="900" x2="{x}" y2="470" stroke="#2a1d1a" stroke-width="8"/><path class="pen" d="M{x},{480} L{x+130},{490} L{x+130},{640} L{x},{630}Z" fill="{c}"/><path d="M{x},{480} L{x+130},{490} L{x+130},{505} L{x},{495}Z" fill="{sh(c,1.25)}"/>'
    L.append(G('flags', o))
    L.append(G('gen', ''.join(person(420 + i * 520, 1000, .65, ['#2a2a32', '#3a3e4a', '#8a4a38'][i], hat='helmet', face=False, seed=150 + i, armor='#4a4e58', pose='hands', sash='#b8352a') for i in range(3))))
    return svg(L, 'day')


@scene(19057)
def _():
    L = outdoor('grey', cl=31, mt=620)
    L.append(ground('grey', 780, '#6a6a48'))
    L.append(road('grey', (740, 1180), 780, '#8a7a62'))
    L.append(rows([(792, .5, 6), (830, .7, 6), (884, .95, 5), (968, 1.35, 4), (1070, 1.85, 3)], side='song', back=True, seed=5, penc=PEN_S))
    L.append(dust(960, 1040, 900, .22))
    return svg(L, 'grey')


@scene(19060)
def _():
    L = outdoor('day', sun=(300, 280), cl=32, mt=680)
    L.append(river(760, 1080, 'day'))
    L.append(G('bankN', '<rect y="640" width="1920" height="140" fill="#6f9a4a"/><rect y="700" width="1920" height="80" fill="#5f8a3e"/>'))
    L.append(palisade(80, 1840, 700, 1.4))
    L.append(bamboo(1650, 720, 1.0)); L.append(tree(180, 720, .9))
    return svg(L, 'day')


@scene(19061)
def _():
    L = outdoor('grey', cl=33, mt=680)
    L.append(river(700, 1080, 'grey'))
    L.append(palisade(120, 1800, 690, .8, '#5a4a38'))
    L.append(G('bankS', '<rect y="900" width="1920" height="180" fill="#6a6a48"/>'))
    L.append(rows([(960, 1.35, 5), (1040, 1.65, 4)], side='song', back=True, seed=2, spread=2.0, penc=PEN_S, base=900))
    return svg(L, 'grey')


@scene(19062)
def _():
    L = outdoor('grey', cl=34, mt=700)
    L.append(ground('grey', 780, '#6a6a48'))
    L.append(palisade(60, 1860, 800, 1.6))
    o = ''
    for i in range(9):
        x = 160 + i * 205
        y = 1020 + (i % 2) * 20
        s = 1.6
        dx = -26 if i in (2, 6) else 0  # vài người lùi lại
        o += soldier(x + dx, y, s, i + 160, 'song', pen=False, pose='hands')
        o += f'<ellipse cx="{x+dx+30*s}" cy="{y-70*s}" rx="{32*s}" ry="{38*s}" fill="#5a4a30" stroke="#2a1d1a" stroke-width="5"/><circle cx="{x+dx+30*s}" cy="{y-70*s}" r="{10*s}" fill="#b0944a"/>'
    L.append(G('shields', o))
    return svg(L, 'grey')


@scene(19063)
def _():
    L = [sky('night'), mountains('night', 650, 3)]
    L.append(river(780, 1080, 'night'))
    L.append(G('bank', '<rect y="700" width="1920" height="130" fill="#101a2a"/>'))
    L.append(G('temple', '<rect x="760" y="520" width="400" height="200" fill="#26304a"/>'
               '<path d="M690,530 Q760,520 810,440 L1110,440 Q1160,520 1230,530 L1190,570 L730,570Z" fill="#0c1220"/>'
               '<path d="M690,530 q-24,-12 -10,-36 M1230,530 q24,-12 10,-36" stroke="#0c1220" stroke-width="10" fill="none"/>'
               '<rect x="900" y="590" width="120" height="130" fill="#0a0e1a"/><circle cx="960" cy="620" r="70" fill="#ffd25a" opacity=".22"/>'
               '<ellipse cx="960" cy="640" rx="26" ry="8" fill="#8a5a3a"/><path class="fire" d="M960,634 q10,-26 0,-40 q-10,14 0,40z" fill="#ffd25a"/>'))
    L.append(tree(520, 740, 1.0, 'night')); L.append(bamboo(1320, 740, 1.1, 'night'))
    return svg(L, 'night')


@scene(19064)
def _():
    L = [sky('night'), mountains('night', 700, 5)]
    L.append(river(780, 1080, 'night'))
    # dải sáng như nét cọ trên sông và trời
    o = ''
    for i, (c, y) in enumerate((('#7affc8', 300), ('#9ab8ff', 380), ('#c8a0ff', 460))):
        o += f'<path d="M0,{y} C400,{y-120} 700,{y+120} 1100,{y-40} S1700,{y-140} 1920,{y+20}" stroke="{c}" stroke-width="{46-i*8}" fill="none" opacity=".28" stroke-linecap="round"/>'
        o += f'<path d="M0,{y+520} C400,{y+400} 700,{y+640} 1100,{y+480} S1700,{y+380} 1920,{y+540}" stroke="{c}" stroke-width="{30-i*6}" fill="none" opacity=".16" stroke-linecap="round"/>'
    L.append(G('ribbons', o))
    return svg(L, 'night')


@scene(19066)
def _():
    L = outdoor('grey', cl=35, mt=640)
    L.append(ground('grey', 780, '#6a6a48'))
    L.append(road('grey', (740, 1180), 780, '#8a7a62'))
    o = ''
    r = random.Random(11)
    for (yy, sc, n) in ((792, .5, 6), (830, .7, 6), (884, .95, 5), (968, 1.35, 4), (1070, 1.85, 3)):
        wid = 360 + (yy - 780) * 2.4
        for k in range(n):
            xx = 960 - wid / 2 + (k + .5) * wid / n + r.randint(-10, 10)
            o += person(xx, yy, sc, SCOL[k % 5], hat='helmet', back=True, seed=k + yy % 7, pose='spear', spear='bare', armor='#4a4e58', sash='#b8352a')
            if k % 2 == 0:
                o += pen_droop(xx + 27 * sc, yy - 150 * sc * 1.45, yy, PEN_S)
    L.append(G('army', o))
    return svg(L, 'grey')


@scene(19068)
def _():
    L = [sky('grey'), clouds('grey', 36, 4), mountains('grey', 640, 7)]
    L.append(ground('grey', 780, '#6a6a48'))
    L.append(G('tents', tent(360, 820, 1.3) + tent(1540, 830, 1.2, col='#8a7a58', dark='#6a5a40')))
    L.append(mat('620,960 1300,960 1340,1060 580,1060', '#8a7a58'))
    # hai người nằm, một người ngồi ôm đầu
    def lying(x, y, s, col, seed, beard=None):
        return (f'<g class="fig"><rect x="{x-110*s}" y="{y-30*s}" width="{160*s}" height="{40*s}" rx="{16*s}" fill="{col}"/>'
                f'<rect x="{x+40*s}" y="{y-24*s}" width="{70*s}" height="{26*s}" rx="{10*s}" fill="{sh(col,.7)}"/>'
                f'<circle cx="{x-130*s}" cy="{y-20*s}" r="{18*s}" fill="{TONES[seed % 6]}"/><path d="M{x-148*s},{y-26*s} Q{x-130*s},{y-48*s} {x-112*s},{y-26*s}Z" fill="#14121a"/>'
                + (f'<path d="M{x-142*s},{y-10*s} Q{x-130*s},{y+8*s} {x-118*s},{y-10*s}Z" fill="#1b1417"/>' if beard else '') + '</g>')
    L.append(lying(820, 1000, 1.5, '#3a4a6a', 3, 'x'))
    L.append(lying(1120, 1030, 1.5, '#41506e', 5))
    L.append(sit({'col': '#34445f', 'hat': 'helmet', 'seed': 161, 'armor': '#4a4e58', 'beard': 'white_goatee', 'sash': '#b8352a'}, 480, 960, 1.9, pose='hands'))
    return svg(L, 'grey')


@scene(19069)
def _():
    L = outdoor('grey', cl=37, mt=700)
    L.append(river(760, 1080, 'grey'))
    L.append(G('bank', '<polygon points="0,880 1100,860 1500,1080 0,1080" fill="#6a6a48"/><polygon points="0,880 1100,860 1140,880 0,900" fill="#8a8a60"/>'))
    L.append(sit({'col': '#3a4a6a', 'hat': 'helmet', 'seed': 171, 'armor': '#4a4e58', 'young': True, 'sash': '#b8352a'}, 560, 960, 2.3, pose='hands', look=1))
    L.append(bamboo(1500, 780, 1.0, 'grey'))
    return svg(L, 'grey')


@scene(19071)
def _():
    L = outdoor('dawn', sun=(1500, 480), cl=38, mt=700)
    L.append(river(740, 1080, 'dawn'))
    L.append(boat(960, 900, 2.3, sail=False))
    L.append(G('staff', '<line x1="780" y1="880" x2="780" y2="460" stroke="#6b4a2a" stroke-width="8"/><path d="M780,470 l0,-26 M780,470 l-14,-22 M780,470 l14,-22" stroke="#e0b040" stroke-width="6"/>'
               '<path class="pen" d="M780,490 q50,10 90,-4 q-10,34 -28,70 q-30,-20 -62,-26Z" fill="#c0392b"/>'))
    L.append(sit('DTN', 880, 860, 1.9, pose='hands'))
    L.append(P('OFF1', 1180, 880, 1.7, col='#6a5a3a', turban=None, crown='headband', pose='spear', spear='bare', beard='white_goatee', seed=175))
    return svg(L, 'dawn')


@scene(19074)
def _():
    L = outdoor('grey', cl=39, mt=680)
    L.append(ground('grey', 780, '#6a6a48'))
    o = ''
    for i, x in enumerate((260, 520, 1560)):
        o += f'<path d="M{x-90},880 L{x-20},800 L{x+70},880Z" fill="#9a8a68" opacity=".9"/>'  # lều xẹp
    L.append(G('foldedtents', o))
    L.append(G('carts', cart(1100, 900, 1.2) + cart(1400, 940, 1.1)))
    for i, x in enumerate((1040, 1160, 1340, 1460)):
        L.append(f'<ellipse cx="{x}" cy="{810+ (i%2)*12}" rx="40" ry="26" fill="#9a8a68"/>')
    L.append(G('men', ''.join(soldier(x, y, .62, i + 180, 'song', pen=False, pose='hands') for i, (x, y) in enumerate(((300, 950), (560, 980), (780, 940), (940, 990), (1240, 1000), (1560, 980))))))
    return svg(L, 'grey')


@scene(19076)
def _():
    L = outdoor('day', sun=(1500, 280), cl=40, mt=660)
    L.append(rice(790))
    L.append(road_back('day', 800))
    cols = ['#7d7a80', '#8a8590', '#6e6a72', '#85808a', '#757078']
    hc = ['#7a5a3a', '#4a5a7a', '#8a4a3a', '#5a7a4a', '#7a6a9a']
    for i in range(5):
        x = 260 + i * 350
        y = 940 + (i % 2) * 40
        L.append(elephant(x, y, .85, cols[i]))
        L.append(person(x + 190, y + 6, 1.3, hc[i], crown='headband' if i % 2 else None, hat='cone' if i % 2 == 0 else None, seed=190 + i, pose='hands', sash=SASHV[i]))
    L.append(P('DTN', 960, 1060, 2.2, pose='hands'))
    L.append(G('staff', '<line x1="1060" y1="1060" x2="1060" y2="640" stroke="#6b4a2a" stroke-width="8"/><path class="pen" d="M1060,660 q50,10 90,-4 q-10,34 -28,70 q-30,-20 -62,-26Z" fill="#c0392b"/>'))
    return svg(L, 'day')


@scene(19077)
def _():
    L = outdoor('day', sun=(400, 300), cl=41, mt=660)
    L.append(rice(790))
    L.append(wall(700, 'grey', tower_x=1450, side='song', h=100, merlon=False))
    L.append(road_back('day', 800))
    L.append(pennant(560, 520, 800, PEN_V))
    L.append(rows([(830, .55, 4), (890, .8, 4), (970, 1.15, 3), (1070, 1.7, 3)], back=True, seed=21, pen=True))
    return svg(L, 'day')


@scene(19079)
def _():
    L = outdoor('day', sun=(960, 240), cl=42, mt=700)
    L.append(ground('day', 780, '#8a7a5a'))
    L.append(road('day', (780, 1140), 790, '#b8905f'))
    # cột mốc biên giới trơn
    L.append('<rect x="940" y="700" width="40" height="150" fill="#8a8680"/><path d="M930,700 L960,660 L990,700Z" fill="#6a6660"/>')
    for i, (x, y, c, kw) in enumerate(((330, 980, '#6a4a2e', dict(turban='#14121a', beard='goatee', seed=201)), (520, 1030, '#7a5a3a', dict(turban='#14121a', seed=202, young=True)), (710, 990, '#5c4228', dict(turban='#14121a', beard='white_goatee', seed=203)))):
        L.append(person(x, y, 2.0, c, sash='#c9a45e', pose='hands', **kw))
    for i, (x, y, c, kw) in enumerate(((1210, 990, '#2e6a8a', dict(seed=204, beard='thick')), (1400, 1030, '#34567a', dict(seed=205, young=True)), (1590, 990, '#2e4a80', dict(seed=206, beard='mustache')))):
        L.append(person(x, y, 2.0, c, hat='song', long=True, wide=True, sash='#c9a45e', pose='hands', **kw))
    L.append(G('people', ''.join(person(840 + i * 48, 900 + (i % 2) * 24, .9, PCOL[i % 7], hat='cone' if i % 2 else None, turban='#5a4128' if i % 2 == 0 else None, seed=210 + i, pose='hands', sash=SASHV[i % 5]) for i in range(5))))
    return svg(L, 'day')


@scene(19080)
def _():
    L = ['<rect width="1920" height="1080" fill="#8a7a58"/>']
    L.append(G('canvas', '<polygon points="0,0 1920,0 1920,140 960,70 0,140" fill="#6a5a3c"/>'))
    L.append('<rect y="140" width="1920" height="800" fill="#a89468"/><rect y="940" width="1920" height="140" fill="#6a4a2a"/>')
    L.append(mat('300,950 1620,950 1760,1080 160,1080', '#b08a54'))
    L.append(sit('LVT', 520, 930, 2.4, pose='hands', look=1))
    L.append(sit({**CAST['TG'], 'col': '#2e6a8a'}, 1400, 930, 2.4, pose='hands', look=-1))
    L.append(maptable(960, 1020, 420))
    L.append(oildish(300, 700)); L.append(oildish(1620, 700))
    return svg(L, 'day')


@scene(19083)
def _():
    L = [hall('dim', curtains=False, windows=(330, 1590))]
    L.append(mat('360,946 1560,946 1700,1080 220,1080'))
    L.append(sit('LTK_G', 660, 940, 2.4, pose='hands', look=1))
    L.append(maptable(1040, 1020, 460))
    L.append(P('TD', 1560, 1010, 2.3, pose='hands', look=-1))
    L.append(oildish(1160, 790, .9))
    return svg(L)


@scene(19085)
def _():
    L = outdoor('day', sun=(1500, 280), cl=43, mt=680)
    L.append(rice(800))
    L.append(G('earthwall', '<polygon points="0,1080 0,880 400,800 1000,790 1500,800 1920,880 1920,1080" fill="#8a6a44"/><polygon points="0,880 400,800 1000,790 1500,800 1920,880 1920,910 1500,830 1000,820 400,830 0,910" fill="#a6845a"/>'))
    L.append(bamboo(120, 830, .8)); 
    L.append(G('fence', ''.join(f'<line x1="{x}" y1="800" x2="{x}" y2="740" stroke="#6a4a2a" stroke-width="6"/>' for x in range(300, 1700, 60))))
    L.append(P('LG', 960, 830, 2.6, pose='hands'))
    L.append(pennant(500, 520, 810, PEN_V)); L.append(pennant(1500, 520, 810, PEN_V))
    L.append(G('far', ''.join(person(200 + i * 330, 760, .3, PCOL[i % 7], hat='cone', face=False, seed=220 + i, pose='hands') for i in range(5))))
    return svg(L, 'day')


@scene(19086)
def _():
    L = outdoor('day', sun=(400, 300), cl=44, mt=640)
    L.append(rice(790))
    L.append(road_back('day', 800))
    L.append(G('fort', '<rect x="800" y="640" width="320" height="140" fill="#8a6a44"/>' + ''.join(f'<rect x="{810+k*52}" y="610" width="30" height="34" fill="#8a6a44"/>' for k in range(6))
               + '<path d="M780,650 L960,560 L1140,650Z" fill="#5a4128"/>'))
    L.append(pennant(1160, 520, 780, PEN_V, 100))
    L.append(rows([(840, .5, 8), (880, .62, 8), (940, .8, 7), (1010, 1.05, 5)], seed=9, pen=True))
    return svg(L, 'day')


@scene(19088)
def _():
    L = [sky('night'), mountains('night', 700, 9), ground('night', 820, '#142030')]
    for i, x in enumerate((220, 520, 1400, 1700)):
        L.append(tent(x, 860 + (i % 2) * 20, 1.3, col='#6a6a60', dark='#4a4a44'))
        L.append(f'<ellipse cx="{x}" cy="{760}" rx="140" ry="120" fill="#ffb347" opacity=".08"/>')
    for x, y in ((420, 1010), (1100, 1040), (1560, 1000), (760, 1050)):
        L.append(campfire(x, y, 1.2))
    for x in (360, 1260, 1620):
        L.append(oildish(x, 840, .7, glow=True))
    L.append(P('LTK_L', 960, 1040, 2.6, pose='hands', look=-1))
    return svg(L, 'night')


@scene(19089)
def _():
    L = [hall('dim', curtains=False, windows=(1500,), glow_center=(1500, 470))]
    L.append(mat('360,946 1560,946 1700,1080 220,1080'))
    L.append(sit('LTK_L', 760, 950, 2.6, pose='hands', look=1))
    L.append(oildish(300, 780, .8))
    return svg(L)


@scene(19090)
def _():
    L = [hall('dim', curtains=False, windows=(1500,), glow_center=(960, 560))]
    L.append(mat('560,946 1360,946 1500,1080 420,1080'))
    L.append(G('seat', '<rect x="760" y="880" width="260" height="30" fill="#6a4a2a"/><rect x="780" y="910" width="24" height="56" fill="#4a3220"/><rect x="976" y="910" width="24" height="56" fill="#4a3220"/>'))
    L.append(G('stand', '<rect x="1230" y="360" width="16" height="590" fill="#4a3220"/><rect x="1130" y="380" width="220" height="14" rx="6" fill="#4a3220"/>'
               '<path d="M1150,394 L1330,394 L1350,700 L1130,700Z" fill="#8a2230"/><path d="M1180,394 L1240,500 L1300,394" stroke="#6a1f1a" stroke-width="5" fill="none"/>'
               '<ellipse cx="1238" cy="350" rx="44" ry="18" fill="#14121a"/><rect x="1196" y="350" width="84" height="30" fill="#14121a"/>'))
    L.append(oildish(500, 780, .9))
    return svg(L)


@scene(19091)
def _():
    L = [hall('gold')]
    L.append(mat('560,946 1360,946 1560,1080 360,1080'))
    L.append(knee('LTH', 760, 1040, 1.7))
    L.append(P('OFF3', 1160, 1010, 2.3, pose='hands'))
    L.append(scroll_blank(1110, 830, 1.8))
    L.append(P('OFF1', 1620, 1000, 2.2, pose='hands'))
    L.append(oildish(470, 740)); L.append(oildish(1470, 740))
    return svg(L)


@scene(19092)
def _():
    L = [hall('dim', curtains=False)]
    for i, x in enumerate((420, 960, 1500)):
        L.append(throne(x, 830))
    for i, (who, x) in enumerate((('TT', 420), ('TTG', 960), ('NT', 1500))):
        L.append(f'<g opacity=".4">{sit(who, x, 780, 1.6, pose="hands")}</g>')
    L.append(mat('560,946 1360,946 1560,1080 360,1080'))
    L.append(P('LTK_L', 960, 1060, 2.0, pose='hands', back=True, face=False))
    return svg(L)


@scene(19096)
def _():
    L = [sky('night'), mountains('night', 680, 4)]
    L.append(river(780, 1080, 'night'))
    L.append(G('bank', '<rect y="680" width="1920" height="130" fill="#101a2a"/>'))
    L.append(palisade(100, 1820, 740, 1.3, '#2e3a50'))
    L.append(G('mist', '<ellipse cx="500" cy="760" rx="600" ry="50" fill="#cfdcff" opacity=".18"/><ellipse cx="1400" cy="790" rx="700" ry="60" fill="#cfdcff" opacity=".16"/><ellipse cx="960" cy="860" rx="900" ry="50" fill="#cfdcff" opacity=".14"/>'))
    return svg(L, 'night')
