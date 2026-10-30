"""Bản thử MỨC CHI TIẾT CAO (4 ảnh mẫu): python phim_ban_do/phang/chitiet.py -> assets/anh_phang/lt1_ct/N.jpg"""
import sys, pathlib, io, random
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import flat
flat.DETAIL = True
from canh import *  # noqa
import canh
_song_hall = canh._song_hall

ROOT = pathlib.Path(__file__).resolve().parents[2]


def floor_tiles(y0=946, col='#3a2a22', line='#241712'):
    o = f'<polygon points="470,{y0} 1450,{y0} 1920,1080 0,1080" fill="{col}"/>'
    for k in range(1, 8):
        yy = y0 + (1080 - y0) * (k / 8) ** 1.6
        o += f'<line x1="{470-470*(yy-y0)/(1080-y0)}" y1="{yy}" x2="{1450+470*(yy-y0)/(1080-y0)}" y2="{yy}" stroke="{line}" stroke-width="3"/>'
    for k in range(-5, 6):
        o += f'<line x1="{960+k*98}" y1="{y0}" x2="{960+k*230}" y2="1080" stroke="{line}" stroke-width="3"/>'
    return G('floor', o)


def screen(x, y, w=620, h=380):
    o = f'<rect x="{x-w/2}" y="{y-h}" width="{w}" height="{h}" fill="#3a2a22"/>'
    for i in range(3):
        px = x - w/2 + 20 + i * (w - 40) / 3
        o += f'<rect x="{px}" y="{y-h+20}" width="{(w-40)/3-8}" height="{h-60}" fill="#c9b88a"/>'
        o += f'<path d="M{px},{y-90} L{px+60},{y-210} L{px+110},{y-150} L{px+150},{y-240} L{px+(w-40)/3-8},{y-110}Z" fill="#6f8a8c" opacity=".75"/>'
        o += f'<path d="M{px},{y-60} Q{px+70},{y-110} {px+(w-40)/3-8},{y-70} L{px+(w-40)/3-8},{y-50} L{px},{y-50}Z" fill="#4a6a6e" opacity=".8"/>'
        o += f'<circle cx="{px+90}" cy="{y-290}" r="22" fill="#e9d79a" opacity=".85"/>'
    o += f'<rect x="{x-w/2-12}" y="{y-12}" width="{w+24}" height="16" fill="#2a1a14"/>'
    return G('screen', o)


def incense(x, y, s=1.0):
    o = f'<ellipse cx="{x}" cy="{y}" rx="{44*s}" ry="{8*s}" fill="#000" opacity=".25"/><path d="M{x-34*s},{y-34*s} Q{x-40*s},{y} {x-20*s},{y} L{x+20*s},{y} Q{x+40*s},{y} {x+34*s},{y-34*s}Z" fill="#8a6a2a"/>'
    o += f'<rect x="{x-38*s}" y="{y-40*s}" width="{76*s}" height="{8*s}" fill="#c9a24a"/><rect x="{x-6*s}" y="{y-60*s}" width="{12*s}" height="{22*s}" fill="#8a6a2a"/>'
    for k, dx in enumerate((-10, 0, 12)):
        o += f'<path class="dust" d="M{x+dx*s},{y-62*s} q{-18*s},{-40*s} {6*s},{-80*s} q{22*s},{-40*s} {-4*s},{-90*s}" stroke="#ddd" stroke-width="{4*s}" fill="none" opacity=".35"/>'
    return G('incense', o)


def carve(x, y0, y1):
    o = ''
    for yy in range(int(y0) + 40, int(y1) - 30, 70):
        o += f'<path d="M{x-30},{yy} q15,-22 30,0 q15,22 30,0" stroke="#d7a85a" stroke-width="3" fill="none" opacity=".7"/>'
    return o


def brackets():
    o = ''
    for x in range(100, 1900, 170):
        o += f'<path d="M{x-45},176 L{x+45},176 L{x+30},150 L{x+14},150 L{x+14},134 L{x-14},134 L{x-14},150 L{x-30},150Z" fill="#6a3a28" stroke="#2a1812" stroke-width="2"/>'
    return G('brackets', o)


def reeds(x, y, n=9, h=150, col='#6a7a3a'):
    r = random.Random(x)
    o = ''
    for i in range(n):
        xx = x + i * 14 + r.randint(-4, 4); hh = h * (.6 + r.random() * .5)
        o += f'<path d="M{xx},{y} Q{xx+r.randint(-18,18)},{y-hh*.6} {xx+r.randint(-26,26)},{y-hh}" stroke="{col}" stroke-width="4" fill="none"/>'
        if i % 3 == 0:
            o += f'<ellipse cx="{xx+4}" cy="{y-hh+10}" rx="5" ry="16" fill="#7a5a30"/>'
    return G('reeds', o)


def sunpath(x, y0, y1, col='#fff1c8'):
    o = ''
    for k in range(9):
        yy = y0 + (y1 - y0) * k / 9; w = 30 + k * 26
        o += f'<rect x="{x-w/2}" y="{yy}" width="{w}" height="5" rx="2.5" fill="{col}" opacity="{.55-k*.04}"/>'
    return G('sunpath', o)


def grass(y0, y1, seed=1, col='#4a6a30', n=120):
    r = random.Random(seed); o = ''
    for _ in range(n):
        x = r.randint(0, 1920); y = r.randint(y0, y1); h = 8 + (y - y0) * .06
        o += f'<path d="M{x},{y} l-3,-{h} M{x},{y} l0,-{h*1.2} M{x},{y} l3,-{h}" stroke="{col}" stroke-width="2" fill="none" opacity=".7"/>'
    return G('grass', o)


def hut_row(items):
    return G('huts', ''.join(hut(x, y, s) + f'<path class="dust" d="M{x+20*s},{y-110*s} q-10,-30 6,-56" stroke="#ccc" stroke-width="5" fill="none" opacity=".3"/>' for x, y, s in items))


def drum(x, y, s=1.0):
    o = f'<rect x="{x-50*s}" y="{y-96*s}" width="{100*s}" height="{96*s}" rx="{14*s}" fill="#8a2a24"/><ellipse cx="{x}" cy="{y-96*s}" rx="{50*s}" ry="{12*s}" fill="#d8c08a"/>'
    for k in range(-3, 4):
        o += f'<circle cx="{x+k*13*s}" cy="{y-70*s}" r="{2.4*s}" fill="#e0b040"/><circle cx="{x+k*13*s}" cy="{y-22*s}" r="{2.4*s}" fill="#e0b040"/>'
    o += f'<rect x="{x-56*s}" y="{y-8*s}" width="{112*s}" height="{10*s}" fill="#4a2c20"/>'
    return G('drum', o)



def boat2(x, y, s, col='#6a4a2a', mui=False, oars=True):
    """Thuyền sông: mũi và đuôi cong vút, ván ghép, mạn thuyền, mái nan (tuỳ chọn), mái chèo, gợn nước. Trả về (phần sau, phần trước)."""
    dk, lt = sh(col, .62), sh(col, 1.25)
    hull = (f'M{x-150*s},{y-52*s} Q{x-128*s},{y-18*s} {x-96*s},{y-6*s} L{x+96*s},{y-6*s} Q{x+130*s},{y-18*s} {x+156*s},{y-60*s} '
            f'Q{x+120*s},{y-34*s} {x+88*s},{y-30*s} L{x-88*s},{y-30*s} Q{x-120*s},{y-34*s} {x-150*s},{y-52*s}Z')
    b = f'<ellipse cx="{x}" cy="{y+6*s}" rx="{170*s}" ry="{9*s}" fill="#000" opacity=".22"/>'
    b += f'<ellipse cx="{x}" cy="{y+14*s}" rx="{150*s}" ry="{5*s}" fill="#fff" opacity=".25"/>'
    if oars:
        for sd, ox in ((-1, x - 70 * s), (1, x + 80 * s)):
            b += f'<line x1="{ox}" y1="{y-34*s}" x2="{ox+sd*60*s}" y2="{y+34*s}" stroke="{dk}" stroke-width="{5*s}"/><path d="M{ox+sd*52*s},{y+22*s} l{sd*22*s},{14*s} l{-sd*6*s},{12*s} l{-sd*22*s},{-12*s}Z" fill="{lt}"/>'
    b += f'<path d="{hull}" fill="{col}"/>'
    # ván thân thuyền
    for k in (1, 2):
        yy = y - 30 * s + k * 8 * s
        b += f'<path d="M{x-118*s+k*9*s},{yy} L{x+118*s-k*9*s},{yy}" stroke="{dk}" stroke-width="{1.6*s}" opacity=".75"/>'
    for k in range(-5, 6):
        b += f'<line x1="{x+k*18*s}" y1="{y-30*s}" x2="{x+k*16*s}" y2="{y-8*s}" stroke="{dk}" stroke-width="{1.2*s}" opacity=".45"/>'
    b += f'<path d="M{x-150*s},{y-52*s} Q{x-120*s},{y-34*s} {x-88*s},{y-30*s} L{x+88*s},{y-30*s} Q{x+120*s},{y-34*s} {x+156*s},{y-60*s}" stroke="{lt}" stroke-width="{4*s}" fill="none"/>'
    b += f'<path d="M{x-150*s},{y-52*s} q{-8*s},{-18*s} {-2*s},{-34*s} M{x+156*s},{y-60*s} q{8*s},{-18*s} {2*s},{-34*s}" stroke="{col}" stroke-width="{7*s}" fill="none" stroke-linecap="round"/>'
    b += f'<circle cx="{x-152*s}" cy="{y-86*s}" r="{5*s}" fill="#d8b04a"/><circle cx="{x+158*s}" cy="{y-94*s}" r="{5*s}" fill="#d8b04a"/>'
    f = f'<path d="M{x-96*s},{y-6*s} L{x+96*s},{y-6*s} L{x+88*s},{y-20*s} L{x-88*s},{y-20*s}Z" fill="{sh(col,.9)}"/>'
    f += f'<path d="M{x-150*s},{y-52*s} Q{x-128*s},{y-18*s} {x-96*s},{y-6*s}" stroke="{dk}" stroke-width="{2*s}" fill="none"/>'
    for k in range(-4, 5):
        f += f'<circle cx="{x+k*20*s}" cy="{y-13*s}" r="{1.6*s}" fill="{lt}"/>'
    f += f'<path d="M{x-170*s},{y+8*s} q{20*s},{-6*s} {40*s},0 t{40*s},0 M{x+90*s},{y+10*s} q{20*s},{-6*s} {40*s},0 t{40*s},0" stroke="#fff" stroke-width="{2.4*s}" fill="none" opacity=".5"/>'
    if mui:
        f += f'<path d="M{x-60*s},{y-30*s} Q{x},{y-110*s} {x+60*s},{y-30*s}Z" fill="#a98a4a"/>' + ''.join(f'<path d="M{x-60*s+k*15*s},{y-30*s} Q{x+(k*15-60)*0.3*s},{y-85*s} {x-30*s+k*15*s*0.5},{y-100*s}" stroke="#7a5f2c" stroke-width="{1.4*s}" fill="none"/>' for k in range(0, 9))
    return G('boat', b), G('boatf', f)


SCN = {}


def sc(n):
    def d(f): SCN[n] = f; return f
    return d


@sc(19054)
def _():
    L = _song_hall()
    L.append(brackets())
    L.append(G('carv', carve(150, 176, 946) + carve(520, 176, 946) + carve(1400, 176, 946) + carve(1770, 176, 946)))
    L.append(floor_tiles())
    L.append(screen(960, 640))
    L.append(throne(960, 830, seat='#2e4a80'))
    L.append(sit('SK', 960, 780, 1.9, pose='hands'))
    L.append(mat('620,946 1300,946 1520,1080 400,1080', '#7a2a2a'))
    L.append(G('rugpat', ''.join(f'<path d="M{960+k*70},956 l18,-0 l-6,124 l-18,0Z" fill="#e0b040" opacity=".25"/>' for k in range(-4, 5))))
    # hai hàng quan đứng hầu hai bên
    for i, (who, x, yy) in enumerate((('TG', 330, 1000), ('LD', 520, 985), ('TK', 1410, 985), ('VAT', 1600, 1000))):
        L.append(P(who, x, yy, 1.5, pose='hands'))
    for x in (260, 1660):
        L.append(P('TTT', x, 940, 1.2, pose='spear', spear='bare'))
    L.append(kneeler(780, 1050, 1.7, '#6a7284', turban='#14121a', seed=26, hat='helmet'))
    L.append(kneeler(1140, 1050, 1.6, '#5a5a70', turban='#14121a', seed=27, hat='helmet'))
    L.append(incense(960, 1000, 1.2))
    L.append(oildish(470, 740)); L.append(oildish(1470, 740))
    return svg(L)


@sc(19066)
def _():
    L = outdoor('grey', cl=35, mt=640)
    L.append(ground('grey', 780, '#6a6a48'))
    L.append(hut_row([(260, 790, .7), (520, 782, .55), (1500, 786, .6), (1700, 792, .75)]))
    L.append(road('grey', (740, 1180), 780, '#8a7a62'))
    L.append(grass(790, 1060, 3, '#4a5a36', 90))
    o = ''; r = random.Random(11)
    for (yy, scl, n) in ((792, .5, 8), (822, .62, 8), (860, .8, 7), (910, 1.0, 6), (980, 1.35, 5), (1075, 1.85, 3)):
        wid = 360 + (yy - 780) * 2.6
        for k in range(n):
            xx = 960 - wid / 2 + (k + .5) * wid / n + r.randint(-10, 10)
            o += person(xx, yy, scl, SCOL[(k + yy) % 5], hat='helmet', back=True, seed=k + yy % 9, pose='spear', spear='bare', armor='#4a4e58', sash='#b8352a')
            if k % 2 == 0:
                o += pen_droop(xx + 40 * scl, yy - 330 * scl, yy - 30 * scl, PEN_S if k % 4 == 0 else '#3a5a8a')
    L.append(G('troops', o))
    L.append(drum(300, 1020, 1.2)); L.append(drum(1650, 1010, 1.1))
    L.append(dust(960, 1040, 760, .22))
    return svg(L, 'grey')


@sc(19071)
def _():
    L = outdoor('dawn', sun=(1500, 480), cl=38, mt=700)
    L.append(river(740, 1080, 'dawn'))
    L.append(sunpath(1500, 745, 1070))
    L.append(boat2(300, 800, .5, col='#5a3a22', mui=True, oars=False)[0]+boat2(300, 800, .5, col='#5a3a22', mui=True, oars=False)[1]); L.append(boat2(1750, 790, .4, col='#5a3a22', oars=False)[0]+boat2(1750, 790, .4, col='#5a3a22', oars=False)[1])
    
    L.append(G('bank', '<path d="M0,1080 L0,930 Q200,880 420,930 L520,1080Z" fill="#4a5a3a"/><path d="M1500,1080 L1620,950 Q1800,900 1920,930 L1920,1080Z" fill="#4a5a3a"/>'))
    L.append(reeds(20, 1000, 14, 220)); L.append(reeds(1640, 1010, 16, 200))
    bb, bf = boat2(960, 920, 2.1)
    L.append(bb)
    L.append(G('staff', '<line x1="780" y1="880" x2="780" y2="460" stroke="#6b4a2a" stroke-width="8"/><path d="M780,470 l0,-26 M780,470 l-14,-22 M780,470 l14,-22" stroke="#e0b040" stroke-width="6"/>'
               '<path class="pen" d="M780,490 q50,10 90,-4 q-10,34 -28,70 q-30,-20 -62,-26Z" fill="#c0392b"/>'))
    L.append(sit('DTN', 880, 860, 1.9, pose='hands'))
    L.append(P('OFF1', 1180, 880, 1.7, col='#6a5a3a', turban=None, crown='headband', pose='spear', spear='bare', beard='white_goatee', seed=175))
    L.append(bf)
    L.append(birds(1100, 220, 5, '#3a2a45', 7))
    return svg(L, 'dawn')


@sc(19085)
def _():
    L = outdoor('day', sun=(1500, 280), cl=43, mt=680)
    L.append(rice(800))
    L.append(hut_row([(330, 800, .6), (620, 795, .5), (1300, 797, .55), (1580, 802, .65)]))
    L.append(G('earthwall', '<polygon points="0,1080 0,880 400,800 1000,790 1500,800 1920,880 1920,1080" fill="#8a6a44"/><polygon points="0,880 400,800 1000,790 1500,800 1920,880 1920,910 1500,830 1000,820 400,830 0,910" fill="#a6845a"/>'))
    L.append(grass(880, 1070, 7, '#5a7a38', 100))
    L.append(bamboo(120, 830, .8)); L.append(bamboo(1790, 840, .9))
    L.append(G('fence', ''.join(f'<line x1="{x}" y1="800" x2="{x}" y2="740" stroke="#6a4a2a" stroke-width="6"/><path d="M{x-4},740 l4,-12 l4,12Z" fill="#6a4a2a"/>' for x in range(300, 1700, 60))))
    L.append(P('LG', 960, 830, 2.6, pose='hands'))
    L.append(pennant(500, 520, 810, PEN_V)); L.append(pennant(1500, 520, 810, PEN_V))
    L.append(pennant(760, 600, 820, '#d08a2e', 120)); L.append(pennant(1160, 600, 820, '#d08a2e', 120))
    L.append(G('far', ''.join(person(200 + i * 230, 770, .5, PCOL[i % 7], hat='cone', face=False, seed=220 + i, pose='hands') for i in range(8) if 3 <= i <= 4 or i in (0, 1, 6, 7))))
    L.append(drum(1700, 1000, 1.1)); L.append(torch(260, 1000, 1.3))
    return svg(L, 'day')


if __name__ == '__main__':
    from playwright.sync_api import sync_playwright
    from PIL import Image
    out = ROOT / 'assets' / 'anh_phang' / 'lt1_ct'; out.mkdir(parents=True, exist_ok=True)
    sv = ROOT / 'ke-hoach' / 'phang' / 'lt1_ct_svg'; sv.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        br = p.chromium.launch(); pg = br.new_page(viewport={'width': 1920, 'height': 1080})
        for n, f in SCN.items():
            (sv / f'{n}.svg').write_text(f(), encoding='utf-8'); pg.goto((sv / f'{n}.svg').as_uri())
            Image.open(io.BytesIO(pg.screenshot())).convert('RGB').save(out / f'{n}.jpg', quality=93)
        br.close()
    print('xong', list(SCN))
