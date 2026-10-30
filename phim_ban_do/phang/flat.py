"""Thư viện vẽ ảnh phẳng (vector SVG) cho video lịch sử: nhân vật mặt đơn giản, nền nhiều lớp.

Mọi ảnh dựng từ cùng bộ nhân vật và bộ nền nên đồng bộ, không bao giờ thừa tay/thừa người.
Mỗi lớp nằm trong một nhóm <g id="..."> để sau này làm chuyển động (mây, cờ, lửa, nhóm xa/gần).
"""
import random

W, H = 1920, 1080
DETAIL = False  # bật = thêm chi tiết mặt, nếp áo, hoa văn, giáp vảy
LIMBS = False  # bật = vẽ rõ cánh tay, bàn tay có ngón, hai chân (ống quần, xà cạp, bàn chân có ngón)
TONES = ['#e2ad7e', '#d99f6e', '#e8b88a', '#cf9565', '#dfa77a', '#d4a074']


def sh(c, f):
    c = c.lstrip('#')
    r, g, b = [int(c[i:i + 2], 16) for i in (0, 2, 4)]
    r, g, b = [max(0, min(255, int(v * f))) for v in (r, g, b)]
    return f'#{r:02x}{g:02x}{b:02x}'


# ------------------------------------------------------------------ nhân vật
def head(x, y, s, face=True, hair='#17121a', hat=None, turban=None, diadem=False, beard=None,
         seed=0, look=0, back=False, young=False, crown=None):
    rnd = random.Random(seed * 7 + 3)
    sk = TONES[seed % len(TONES)]
    r = 16 * s * (0.92 if young else 1)
    o = [f'<circle cx="{x}" cy="{y}" r="{r}" fill="{sk}"/>']
    if hat == 'cone':
        o.append(f'<path d="M{x-44*s},{y-4*s} L{x},{y-44*s} L{x+44*s},{y-4*s} Q{x},{y-12*s} {x-44*s},{y-4*s}Z" fill="#c9a45e"/>')
        o.append(f'<path d="M{x-44*s},{y-4*s} L{x},{y-44*s} L{x-12*s},{y-8*s}Z" fill="#a9863f"/>')
        for k in (-20, -8, 6, 18):
            o.append(f'<line x1="{x}" y1="{y-44*s}" x2="{x+k*2*s}" y2="{y-6*s}" stroke="#a9863f" stroke-width="{1.2*s}"/>')
        o.append(f'<path d="M{x-13*s},{y-3*s} Q{x-15*s},{y+14*s} {x},{y+17*s} Q{x+15*s},{y+14*s} {x+13*s},{y-3*s}" stroke="#7b2a22" stroke-width="{1.4*s}" fill="none"/>')
    elif hat == 'helmet':
        o.append(f'<path d="M{x-19*s},{y-2*s} Q{x},{y-34*s} {x+19*s},{y-2*s}Z" fill="#4a4e58"/><rect x="{x-20*s}" y="{y-5*s}" width="{40*s}" height="{4*s}" fill="#2e3038"/>')
        o.append(f'<path d="M{x},{y-30*s} q{4*s},{-14*s} {12*s},{-10*s} q{-4*s},{8*s} {-12*s},{10*s}Z" fill="#b8352a"/>')
        if DETAIL:
            o.append(f'<path d="M{x-19*s},{y-2*s} Q{x},{y-34*s} {x+19*s},{y-2*s}" fill="none" stroke="#fff" stroke-width="{1.2*s}" opacity=".18"/><line x1="{x}" y1="{y-32*s}" x2="{x}" y2="{y-5*s}" stroke="#2e3038" stroke-width="{1.4*s}"/>')
            for k in (-13, -6, 6, 13):
                o.append(f'<circle cx="{x+k*s}" cy="{y-8*s}" r="{1.2*s}" fill="#d8c98a"/>')
            o.append(f'<path d="M{x-20*s},{y-1*s} L{x-23*s},{y+12*s} L{x-15*s},{y+6*s}Z M{x+20*s},{y-1*s} L{x+23*s},{y+12*s} L{x+15*s},{y+6*s}Z" fill="#3a3d46"/>')
    elif hat == 'song':  # mũ phốc đầu của quan Tống: thân mũ cao, hai cánh dài nằm ngang
        o.append(f'<rect x="{x-15*s}" y="{y-34*s}" width="{30*s}" height="{30*s}" rx="{11*s}" fill="#14121a"/>')
        o.append(f'<rect x="{x-17*s}" y="{y-12*s}" width="{34*s}" height="{6*s}" fill="#e0b040"/>')
        o.append(f'<rect x="{x-15*s}" y="{y-26*s}" width="{30*s}" height="{3*s}" fill="#2a2630"/>')
        for sd in (-1, 1):
            o.append(f'<rect x="{x+(10 if sd>0 else -58)*s}" y="{y-23*s}" width="{48*s}" height="{6*s}" rx="{3*s}" fill="#14121a"/>')
            o.append(f'<rect x="{x+(10 if sd>0 else -58)*s}" y="{y-23*s}" width="{48*s}" height="{1.6*s}" rx="{1*s}" fill="#3a3642"/>')
            if DETAIL:
                for k in range(5):
                    o.append(f'<circle cx="{x+(sd*(18+k*8))*s}" cy="{y-20*s}" r="{0.9*s}" fill="#e0b040"/>')
        if DETAIL:
            o.append(f'<path d="M{x-12*s},{y-30*s} Q{x},{y-35*s} {x+12*s},{y-30*s}" stroke="#fff" stroke-width="{1.3*s}" fill="none" opacity=".2"/>')
            for k in (-8, 0, 8):
                o.append(f'<circle cx="{x+k*s}" cy="{y-9*s}" r="{1.3*s}" fill="#e8d890"/>')
    elif hat == 'crownS':  # mũ miện hoàng đế: tấm phẳng trên cao, rèm hạt ngọc hai bên
        o.append(f'<rect x="{x-17*s}" y="{y-24*s}" width="{34*s}" height="{18*s}" rx="{4*s}" fill="#14121a"/>')
        o.append(f'<rect x="{x-38*s}" y="{y-34*s}" width="{76*s}" height="{9*s}" rx="{2*s}" fill="#14121a"/><rect x="{x-38*s}" y="{y-34*s}" width="{76*s}" height="{2.4*s}" fill="#e0b040"/>')
        for k in range(-4, 5):
            o.append(f'<line x1="{x+k*8.5*s}" y1="{y-25*s}" x2="{x+k*8.5*s}" y2="{y-6*s}" stroke="#e8d890" stroke-width="{1.4*s}"/><circle cx="{x+k*8.5*s}" cy="{y-6*s}" r="{1.8*s}" fill="#e8d890"/>')
    elif hat == 'champa':  # mũ tầng vàng Chăm-pa
        for i, w in enumerate((24, 19, 14, 9)):
            o.append(f'<path d="M{x-w*s},{y-8*s-i*13*s} L{x-(w-3)*s},{y-21*s-i*13*s} L{x+(w-3)*s},{y-21*s-i*13*s} L{x+w*s},{y-8*s-i*13*s}Z" fill="#e0b040" stroke="#a9781d" stroke-width="{1.1*s}"/>')
    else:
        hairc = hair
        o.append(f'<path d="M{x-17*s},{y-2*s} Q{x},{y-26*s} {x+17*s},{y-2*s} Q{x},{y-10*s} {x-17*s},{y-2*s}Z" fill="{hairc}"/>')
        o.append(f'<circle cx="{x}" cy="{y-24*s}" r="{7*s}" fill="{hairc}"/>')
        if turban:
            o.append(f'<path d="M{x-18*s},{y-6*s} Q{x},{y-22*s} {x+18*s},{y-6*s} L{x+16*s},{y-12*s} Q{x},{y-26*s} {x-16*s},{y-12*s}Z" fill="{turban}"/>')
        if diadem:
            o.append(f'<path d="M{x-17*s},{y-8*s} L{x-12*s},{y-26*s} L{x-5*s},{y-14*s} L{x},{y-30*s} L{x+5*s},{y-14*s} L{x+12*s},{y-26*s} L{x+17*s},{y-8*s}Z" fill="#e2b13c" stroke="#a9781d" stroke-width="{1.2*s}"/>')
        if crown == 'headband':
            o.append(f'<rect x="{x-17*s}" y="{y-9*s}" width="{34*s}" height="{5*s}" fill="#b8352a"/>')
    o.append(f'<circle cx="{x-16*s}" cy="{y+2*s}" r="{3.4*s}" fill="{sk}"/><circle cx="{x+16*s}" cy="{y+2*s}" r="{3.4*s}" fill="{sk}"/>')
    if back:
        return ''.join(o)
    if face:
        o.append(f'<circle cx="{x-9*s}" cy="{y+6*s}" r="{3*s}" fill="#d9776a" opacity=".28"/><circle cx="{x+9*s}" cy="{y+6*s}" r="{3*s}" fill="#d9776a" opacity=".28"/>')
        o.append(f'<path d="M{x},{y+1*s} q{1.5*s},{4*s} 0,{5*s}" stroke="{sh(sk,.7)}" stroke-width="{1.2*s}" fill="none"/>')
        ex = (5.5 + rnd.random() * 2) * s
        dx = look * 3 * s
        o.append(f'<circle cx="{x-ex+dx}" cy="{y+1*s}" r="{1.9*s}" fill="#241a1a"/><circle cx="{x+ex+dx}" cy="{y+1*s}" r="{1.9*s}" fill="#241a1a"/>')
        bt = 1 + rnd.random()
        o.append(f'<line x1="{x-ex-3*s+dx}" y1="{y-4*s}" x2="{x-ex+3*s+dx}" y2="{y-4.5*s}" stroke="#2a1c1c" stroke-width="{bt*s}"/><line x1="{x+ex-3*s+dx}" y1="{y-4.5*s}" x2="{x+ex+3*s+dx}" y2="{y-4*s}" stroke="#2a1c1c" stroke-width="{bt*s}"/>')
        o.append(f'<path d="M{x-4*s+dx},{y+8*s} Q{x+dx},{y+10*s} {x+4*s+dx},{y+8*s}" stroke="#7b2a22" stroke-width="{1.4*s}" fill="none"/>')
        if DETAIL:
            for sd in (-1, 1):
                ex_ = x + sd * ex + dx
                o.append(f'<g class="eye"><ellipse cx="{ex_}" cy="{y+1*s}" rx="{3.4*s}" ry="{2.3*s}" fill="#fbf6ea"/><circle cx="{ex_+look*1.2*s}" cy="{y+1*s}" r="{1.7*s}" fill="#2a1a14"/><circle cx="{ex_+look*1.2*s+0.6*s}" cy="{y+0.3*s}" r="{0.55*s}" fill="#fff"/></g>')
                o.append(f'<path d="M{ex_-3.6*s},{y+0.4*s} Q{ex_},{y-2.6*s} {ex_+3.6*s},{y+0.4*s}" stroke="#2a1a14" stroke-width="{0.9*s}" fill="none"/>')
                o.append(f'<path d="M{ex_-3*s},{y+3.4*s} Q{ex_},{y+4.6*s} {ex_+3*s},{y+3.4*s}" stroke="{sh(sk,.8)}" stroke-width="{0.6*s}" fill="none"/>')
                o.append(f'<path d="M{x+sd*17*s},{y+0*s} q{sd*1.6*s},{3*s} 0,{6*s}" stroke="{sh(sk,.7)}" stroke-width="{0.9*s}" fill="none"/>')
            o.append(f'<ellipse cx="{x+3*s}" cy="{y+4.5*s}" rx="{2.6*s}" ry="{1.6*s}" fill="#000" opacity=".1"/>')
            o.append(f'<path d="M{x-9*s},{y-7*s} Q{x},{y-10*s} {x+9*s},{y-7*s}" stroke="#fff" stroke-width="{2*s}" fill="none" opacity=".12"/>')
            sm = rnd.random()
            if sm < .5:
                o.append(f'<path d="M{x-5*s+dx},{y+8*s} Q{x+dx},{y+12*s} {x+5*s+dx},{y+8*s}Z" fill="#7b2a22"/><path d="M{x-3*s+dx},{y+9*s} Q{x+dx},{y+10.6*s} {x+3*s+dx},{y+9*s}Z" fill="#f4eee2"/>')
            o.append(f'<ellipse cx="{x}" cy="{y+16*s}" rx="{13*s}" ry="{3*s}" fill="#000" opacity=".1"/>')
        bc = '#e9e4dc' if beard and beard.startswith('white') else '#1b1417'
        if beard in ('goatee', 'white_goatee'):
            o.append(f'<path d="M{x-5*s},{y+11*s} Q{x},{y+26*s} {x+5*s},{y+11*s}Z" fill="{bc}"/>')
        elif beard in ('long', 'white_long'):
            o.append(f'<path d="M{x-14*s},{y+6*s} Q{x-12*s},{y+34*s} {x},{y+52*s} Q{x+12*s},{y+34*s} {x+14*s},{y+6*s} Q{x},{y+14*s} {x-14*s},{y+6*s}Z" fill="{bc}"/>')
        elif beard in ('short', 'thick'):
            w = 15 if beard == 'thick' else 12
            o.append(f'<path d="M{x-w*s},{y+6*s} Q{x-w*s-1*s},{y+24*s} {x},{y+27*s} Q{x+w*s+1*s},{y+24*s} {x+w*s},{y+6*s} L{x+w*s-3*s},{y+11*s} Q{x},{y+14*s} {x-w*s+3*s},{y+11*s}Z" fill="{bc}"/>')
        elif beard == 'mustache':
            o.append(f'<path d="M{x-9*s},{y+7*s} Q{x},{y+4*s} {x+9*s},{y+7*s} Q{x},{y+9*s} {x-9*s},{y+7*s}Z" fill="{bc}"/>')
    return ''.join(o)


def _tube(pts, w, col, outline=None):
    """Ống tay: đường cong đi qua các điểm, đầu tròn; có viền tối phía dưới."""
    d = f'M{pts[0][0]},{pts[0][1]} Q{pts[1][0]},{pts[1][1]} {pts[2][0]},{pts[2][1]}'
    o = ''
    if outline:
        o += f'<path d="{d}" stroke="{outline}" stroke-width="{w+1.8}" fill="none" stroke-linecap="round"/>'
    return o + f'<path d="{d}" stroke="{col}" stroke-width="{w}" fill="none" stroke-linecap="round"/>'


def _hand(cx, cy, s, ang=0, grip=False, point=False, skin=None):
    """Bàn tay có ngón: bàn tay (hình bầu dục), bốn ngón, ngón cái; grip = nắm cán giáo."""
    skin = skin or TONES[0]; dk = sh(skin, .7)
    o = f'<g transform="translate({cx},{cy}) rotate({ang})">'
    if grip:
        o += f'<rect x="{-5.5*s}" y="{-4.5*s}" width="{11*s}" height="{9*s}" rx="{3.4*s}" fill="{skin}" stroke="{dk}" stroke-width="{0.7*s}"/>'
        for k in range(4):
            o += f'<line x1="{(-4.2+k*2.8)*s}" y1="{-3.6*s}" x2="{(-4.2+k*2.8)*s}" y2="{3.6*s}" stroke="{dk}" stroke-width="{0.7*s}"/>'
        o += f'<ellipse cx="{-5.2*s}" cy="{-1*s}" rx="{2.2*s}" ry="{3.4*s}" fill="{skin}" stroke="{dk}" stroke-width="{0.6*s}"/>'
    else:
        o += f'<ellipse cx="0" cy="0" rx="{6.5*s}" ry="{4.6*s}" fill="{skin}" stroke="{dk}" stroke-width="{0.7*s}"/>'
        for k in range(4):
            o += f'<path d="M{(-4.5+k*3)*s},{-3*s} q{0.5*s},{-3.2*s} {2.2*s},{-3.4*s}" stroke="{dk}" stroke-width="{0.8*s}" fill="none" stroke-linecap="round"/>'
        o += f'<path d="M{-5.4*s},{1.4*s} q{-3.2*s},{-0.6*s} {-3.4*s},{-3.4*s}" stroke="{dk}" stroke-width="{1.1*s}" fill="none" stroke-linecap="round"/>'
        if point:
            o += f'<path d="M{5*s},{-1*s} l{10*s},{-1.4*s}" stroke="{skin}" stroke-width="{3*s}" stroke-linecap="round"/>'
    return o + '</g>'


def _legs(x, y, s, col, h):
    """Hai chân: ống quần, đầu gối, xà cạp quấn bắp chân, bàn chân có ngón (chân đất)."""
    pc = sh(col, .5); pl = sh(col, .66); wrap = sh(col, 1.05)
    o = ''
    for sgn, cls in ((-1, 'ftL'), (1, 'ftR')):
        hx = x + sgn * 9 * s; ax = x + sgn * 13.5 * s
        o += f'<path d="M{hx-8.5*s},{y-h*0.5} L{ax-6*s},{y-8*s} L{ax+6*s},{y-8*s} L{hx+8.5*s},{y-h*0.5}Z" fill="{pc if sgn<0 else pl}"/>'
        o += f'<path d="M{hx-2*s},{y-h*0.34} q{3*s},{3*s} {6*s},0" stroke="#000" stroke-width="{1.1*s}" fill="none" opacity=".25"/>'
        for k in range(3):
            yy = y - (20 - k * 4.2) * s
            o += f'<path d="M{ax-6.2*s},{yy} L{ax+6.2*s},{yy+1.8*s}" stroke="{wrap}" stroke-width="{2.1*s}" opacity=".85"/>'
        o += f'<g class="{cls}"><ellipse cx="{ax+sgn*1.5*s}" cy="{y-2*s}" rx="{10.5*s}" ry="{4.6*s}" fill="#caa078" stroke="{sh("#caa078",.7)}" stroke-width="{0.7*s}"/>'
        for k in range(4):
            tx = ax + sgn * (3.5 + k * 2.4) * s
            o += f'<line x1="{tx}" y1="{y-5*s}" x2="{tx}" y2="{y-1*s}" stroke="{sh("#caa078",.62)}" stroke-width="{0.7*s}"/>'
        o += '</g>'
    return o


def _shoes(x, y, s):
    """Giày vải mũi cong thò ra dưới vạt áo dài."""
    o = ''
    for sgn, cls in ((-1, 'ftL'), (1, 'ftR')):
        cx = x + sgn * 10.5 * s
        o += (f'<g class="{cls}"><path d="M{cx-9*s},{y-3*s} Q{cx-9*s},{y+4.5*s} {cx+sgn*3*s},{y+4.5*s} Q{cx+sgn*12*s},{y+4*s} {cx+sgn*13*s},{y-1*s} '
              f'Q{cx+sgn*13*s},{y-5*s} {cx+sgn*10*s},{y-4*s} L{cx+9*s},{y-3*s}Z" fill="#2a2024"/>'
              f'<path d="M{cx-8*s},{y+3.2*s} L{cx+sgn*10*s},{y+3.4*s}" stroke="#d9d0c0" stroke-width="{1.4*s}" stroke-linecap="round"/></g>')
    return o


def _arms(x, y, s, col, pose, wide=False):
    if pose == 'rein' and not LIMBS:
        pose = 'hands'
    if LIMBS:
        return _arms_limbs(x, y, s, col, pose, wide)
    return _arms_old(x, y, s, col, pose, wide)


def _arms_limbs(x, y, s, col, pose, wide=False):
    h = 150 * s
    c = sh(col, .9); dk = sh(col, .62); cuff = sh(col, 1.35)
    w = 13 * s * (1.35 if wide else 1.0)
    o = ''
    if pose == 'hands':
        for sgn in (-1, 1):
            sx, sy = x + sgn * 21 * s, y - h * 0.83
            ex, ey = x + sgn * (30 + (6 if wide else 0)) * s, y - h * 0.66
            wx, wy = x + sgn * 4 * s, y - h * 0.57
            o += _tube(((sx, sy), (ex, ey), (wx, wy)), w, c, dk)
            o += f'<path d="M{wx-sgn*1*s-6*s},{wy-4.5*s} L{wx-sgn*1*s+6*s},{wy+4.5*s}" stroke="{cuff}" stroke-width="{4.4*s}" stroke-linecap="round" opacity=".95"/>' if False else ''
        # hai bàn tay chắp, tay phải đè lên tay trái
        o += _hand(x - 2 * s, y - h * 0.575, s, ang=-8)
        o += _hand(x + 3 * s, y - h * 0.585, s, ang=8)
        o += f'<path d="M{x-9*s},{y-h*0.545} Q{x},{y-h*0.52} {x+9*s},{y-h*0.545}" stroke="{cuff}" stroke-width="{3.4*s}" fill="none" stroke-linecap="round"/>'
        return o
    if pose == 'rein':
        # người cưỡi ngựa: tay gần cầm dây cương đưa ra trước, tay xa đặt trên đùi
        o += _tube(((x - 21 * s, y - h * 0.83), (x - 33 * s, y - h * 0.66), (x - 18 * s, y - h * 0.5)), w * 0.86, c, dk)
        o += _hand(x - 16 * s, y - h * 0.495, s * 0.95, ang=-20)
        hx, hy = x + 46 * s, y - h * 0.6
        o += f'<path d="M{hx},{hy} Q{hx+80*s},{hy+14*s} {hx+144*s},{hy+2*s}" stroke="#3a2418" stroke-width="{2*s}" fill="none"/>'
        o += _tube(((x + 21 * s, y - h * 0.83), (x + 36 * s, y - h * 0.72), (hx - 2 * s, hy - 1 * s)), w * 0.86, c, dk)
        o += _hand(hx, hy, s, ang=0, grip=True)
        return o
    if pose == 'spear':
        # tay xa chống hông, tay gần nắm cán giáo
        o += _tube(((x - 21 * s, y - h * 0.83), (x - 33 * s, y - h * 0.66), (x - 15 * s, y - h * 0.5)), w * 0.86, c, dk)
        o += _hand(x - 13.5 * s, y - h * 0.49, s * 0.95, ang=-30)
        o += _tube(((x + 21 * s, y - h * 0.83), (x + 33 * s, y - h * 0.72), (x + 27 * s, y - h * 0.6)), w * 0.86, c, dk)
        o += _hand(x + 27 * s, y - h * 0.595, s, ang=0, grip=True)
        return o
    if pose == 'point':
        o += _tube(((x + 20 * s, y - h * 0.83), (x + 44 * s, y - h * 0.9), (x + 66 * s, y - h * 0.92)), w * 0.86, c, dk)
        o += _hand(x + 69 * s, y - h * 0.92, s, ang=-6, point=True)
        o += _tube(((x - 21 * s, y - h * 0.83), (x - 31 * s, y - h * 0.65), (x - 14 * s, y - h * 0.52)), w * 0.86, c, dk)
        o += _hand(x - 12 * s, y - h * 0.515, s * 0.95, ang=-20)
        return o
    if pose == 'up':
        o += _tube(((x + 20 * s, y - h * 0.83), (x + 34 * s, y - h * 0.93), (x + 46 * s, y - h * 0.99)), w * 0.86, c, dk)
        o += _hand(x + 47 * s, y - h * 1.0, s, ang=-70)
        o += _tube(((x - 21 * s, y - h * 0.83), (x - 31 * s, y - h * 0.65), (x - 14 * s, y - h * 0.52)), w * 0.86, c, dk)
        o += _hand(x - 12 * s, y - h * 0.515, s * 0.95, ang=-20)
        return o
    return ''


def _arms_old(x, y, s, col, pose, wide=False):
    h = 150 * s
    c = sh(col, .9)
    cuff = sh(col, 1.3)
    skin = TONES[0]
    w = 1.5 if wide else 1.0
    if pose == 'hands':
        o = (f'<path d="M{x-21*s},{y-h*0.84} Q{x-30*s*w},{y-h*0.55} {x-6*s},{y-h*0.52} L{x+6*s},{y-h*0.52} Q{x+30*s*w},{y-h*0.55} {x+21*s},{y-h*0.84} '
             f'L{x+14*s},{y-h*0.8} Q{x+16*s},{y-h*0.6} {x},{y-h*0.6} Q{x-16*s},{y-h*0.6} {x-14*s},{y-h*0.8}Z" fill="{c}"/>')
        o += f'<path d="M{x-8*s},{y-h*0.54} Q{x},{y-h*0.5} {x+8*s},{y-h*0.54} L{x+8*s},{y-h*0.57} Q{x},{y-h*0.53} {x-8*s},{y-h*0.57}Z" fill="{cuff}"/>'
        o += f'<circle cx="{x}" cy="{y-h*0.585}" r="{4.2*s}" fill="{skin}"/>'
        if wide:
            o += f'<path d="M{x-24*s},{y-h*0.8} Q{x-40*s},{y-h*0.5} {x-30*s},{y-h*0.3} L{x-18*s},{y-h*0.32} Q{x-22*s},{y-h*0.55} {x-16*s},{y-h*0.78}Z" fill="{c}" opacity=".85"/>'
            o += f'<path d="M{x+24*s},{y-h*0.8} Q{x+40*s},{y-h*0.5} {x+30*s},{y-h*0.3} L{x+18*s},{y-h*0.32} Q{x+22*s},{y-h*0.55} {x+16*s},{y-h*0.78}Z" fill="{c}" opacity=".85"/>'
        return o
    if pose == 'spear':
        return (f'<path d="M{x-21*s},{y-h*0.84} Q{x-32*s},{y-h*0.55} {x-14*s},{y-h*0.5} L{x-8*s},{y-h*0.56} Q{x-20*s},{y-h*0.6} {x-14*s},{y-h*0.8}Z" fill="{c}"/>'
                f'<circle cx="{x-11*s}" cy="{y-h*0.53}" r="{3.6*s}" fill="{skin}"/>'
                f'<path d="M{x+21*s},{y-h*0.84} Q{x+36*s},{y-h*0.7} {x+30*s},{y-h*0.6} L{x+22*s},{y-h*0.62} Q{x+24*s},{y-h*0.72} {x+14*s},{y-h*0.8}Z" fill="{c}"/>'
                f'<circle cx="{x+27*s}" cy="{y-h*0.6}" r="{4.2*s}" fill="{skin}"/>')
    if pose == 'point':
        return (f'<path d="M{x+20*s},{y-h*0.84} L{x+66*s},{y-h*0.95} L{x+68*s},{y-h*0.88} L{x+22*s},{y-h*0.7}Z" fill="{c}"/>'
                f'<circle cx="{x+70*s}" cy="{y-h*0.92}" r="{4.4*s}" fill="{skin}"/><path d="M{x+72*s},{y-h*0.93} l{9*s},{-2*s}" stroke="{skin}" stroke-width="{2.6*s}" stroke-linecap="round"/>'
                f'<path d="M{x-21*s},{y-h*0.84} Q{x-30*s},{y-h*0.6} {x-14*s},{y-h*0.5} L{x-8*s},{y-h*0.55} Q{x-18*s},{y-h*0.62} {x-14*s},{y-h*0.8}Z" fill="{c}"/>'
                f'<circle cx="{x-11*s}" cy="{y-h*0.53}" r="{3.6*s}" fill="{skin}"/>')
    if pose == 'up':
        return (f'<path d="M{x+20*s},{y-h*0.84} L{x+44*s},{y-h*1.0} L{x+50*s},{y-h*0.93} L{x+24*s},{y-h*0.72}Z" fill="{c}"/>'
                f'<circle cx="{x+47*s}" cy="{y-h*0.99}" r="{4.4*s}" fill="{skin}"/>'
                f'<path d="M{x-21*s},{y-h*0.84} Q{x-30*s},{y-h*0.6} {x-14*s},{y-h*0.5} L{x-8*s},{y-h*0.55} Q{x-18*s},{y-h*0.62} {x-14*s},{y-h*0.8}Z" fill="{c}"/>'
                f'<circle cx="{x-11*s}" cy="{y-h*0.53}" r="{3.6*s}" fill="{skin}"/>')
    return ''


def body(x, y, s, col, sash='#a8452f', trim=None, armor=None, pose='hands', spear=None, wide=False, long=False, skirt=False, back=False):
    h = 150 * s
    o = []
    dark = sh(col, .72)
    edge = trim or sh(col, 1.35)
    o.append(f'<ellipse cx="{x}" cy="{y+2*s}" rx="{44*s}" ry="{7*s}" fill="#000" opacity=".16"/>')
    if LIMBS and not (skirt or long):
        o.append(_legs(x, y, s, col, h))
    else:
        o.append(f'<ellipse class="ftL" cx="{x-9*s}" cy="{y}" rx="{10*s}" ry="{4*s}" fill="#caa078"/><ellipse class="ftR" cx="{x+9*s}" cy="{y}" rx="{10*s}" ry="{4*s}" fill="#caa078"/>')
    if LIMBS and not (skirt or long):
        pass
    elif skirt or long:
        o.append(f'<path d="M{x-17*s},{y-h*0.52} L{x-27*s},{y-2*s} L{x+27*s},{y-2*s} L{x+17*s},{y-h*0.52}Z" fill="{dark}"/>')
        o.append(f'<path d="M{x-26*s},{y-9*s} Q{x},{y-2*s} {x+26*s},{y-9*s} L{x+27*s},{y-2*s} L{x-27*s},{y-2*s}Z" fill="{edge}"/>')
        for k in (-14, -5, 5, 14):
            o.append(f'<line x1="{x+k*s}" y1="{y-h*0.4}" x2="{x+k*1.7*s}" y2="{y-10*s}" stroke="{sh(col,.58)}" stroke-width="{1.2*s}"/>')
    else:
        o.append(f'<path d="M{x-17*s},{y-h*0.52} L{x-22*s},{y-4*s} L{x+22*s},{y-4*s} L{x+17*s},{y-h*0.52}Z" fill="{dark}"/>')
        o.append(f'<line x1="{x}" y1="{y-h*0.4}" x2="{x}" y2="{y-4*s}" stroke="{sh(col,.55)}" stroke-width="{1.5*s}"/>')
        o.append(f'<rect x="{x-22*s}" y="{y-14*s}" width="{44*s}" height="{3*s}" fill="{sh(col,.6)}"/>')
    ext = 6 * s if wide else 0
    hem = h * 0.12 if long else h * 0.3
    # cổ
    o.append(f'<rect x="{x-6*s}" y="{y-h*0.9}" width="{12*s}" height="{h*0.07}" fill="{TONES[2]}"/>')
    o.append(f'<path d="M{x-21*s-ext},{y-h*0.86} L{x-24*s-ext},{y-hem} L{x+24*s+ext},{y-hem} L{x+21*s+ext},{y-h*0.86} Q{x},{y-h*0.9} {x-21*s-ext},{y-h*0.86}Z" fill="{col}"/>')
    # bóng bên phải + sáng bên trái
    o.append(f'<path d="M{x+4*s},{y-h*0.88} L{x+21*s+ext},{y-h*0.86} L{x+24*s+ext},{y-hem} L{x+6*s},{y-hem}Z" fill="#000" opacity=".12"/>')
    o.append(f'<path d="M{x-21*s-ext},{y-h*0.86} L{x-12*s},{y-h*0.86} L{x-14*s},{y-hem} L{x-24*s-ext},{y-hem}Z" fill="#fff" opacity=".08"/>')
    if not back:
        o.append(f'<path d="M{x-7*s},{y-h*0.9} L{x+1*s},{y-h*0.76} L{x+7*s},{y-h*0.9}" stroke="#f1ece0" stroke-width="{3*s}" fill="none" opacity=".95"/>')
        o.append(f'<path d="M{x-12*s},{y-h*0.88} L{x+5*s},{y-h*0.62} M{x+12*s},{y-h*0.88} L{x+5*s},{y-h*0.62}" stroke="{edge}" stroke-width="{2.4*s}" fill="none"/>')
    else:
        o.append(f'<line x1="{x}" y1="{y-h*0.88}" x2="{x}" y2="{y-h*0.42}" stroke="{sh(col,.6)}" stroke-width="{1.6*s}"/>')
    # nẹp gấu áo
    o.append(f'<path d="M{x-24*s-ext},{y-hem-6*s} L{x+24*s+ext},{y-hem-6*s} L{x+24*s+ext},{y-hem} L{x-24*s-ext},{y-hem}Z" fill="{edge}" opacity=".85"/>')
    if LIMBS and (skirt or long):
        o.append(_shoes(x, y, s))
    if armor:
        o.append(f'<path d="M{x-22*s},{y-h*0.85} Q{x-32*s},{y-h*0.78} {x-27*s},{y-h*0.68} L{x-15*s},{y-h*0.78}Z" fill="{armor}"/><path d="M{x+22*s},{y-h*0.85} Q{x+32*s},{y-h*0.78} {x+27*s},{y-h*0.68} L{x+15*s},{y-h*0.78}Z" fill="{armor}"/>')
        o.append(f'<path d="M{x-20*s},{y-h*0.8} L{x+20*s},{y-h*0.8} L{x+18*s},{y-h*0.52} L{x-18*s},{y-h*0.52}Z" fill="{armor}" opacity=".6"/>')
        for k in range(4):
            o.append(f'<line x1="{x-18*s}" y1="{y-h*(0.74-k*0.07)}" x2="{x+18*s}" y2="{y-h*(0.74-k*0.07)}" stroke="#000" stroke-width="{1.1*s}" opacity=".25"/>')
    if DETAIL:
        rr = random.Random(int(x * 3 + y))
        for k in range(3):
            xx = x + (-14 + k * 14 + rr.random() * 4) * s
            o.append(f'<path d="M{xx},{y-h*0.38} q{3*s},{h*0.12} {-2*s},{h*0.24} q{3*s},{h*0.1} {1*s},{h*0.15}" stroke="{sh(col,.62)}" stroke-width="{1.1*s}" fill="none" opacity=".7"/>')
        o.append(f'<path d="M{x-22*s},{y-h*0.8} Q{x-14*s},{y-h*0.62} {x-21*s},{y-h*0.45}" stroke="#fff" stroke-width="{1.4*s}" fill="none" opacity=".14"/>')
        if not armor:
            for k in range(-2, 3):
                o.append(f'<path d="M{x+k*10*s},{y-hem-3*s} l{3*s},{-3*s} l{3*s},{3*s} l{-3*s},{3*s}Z" fill="{sh(edge,1.1)}" opacity=".9"/>')
            o.append(f'<circle cx="{x}" cy="{y-h*0.66}" r="{6*s}" fill="none" stroke="{edge}" stroke-width="{1.2*s}" opacity=".8"/><circle cx="{x}" cy="{y-h*0.66}" r="{2.2*s}" fill="{edge}" opacity=".8"/>')
        else:
            for r_ in range(5):
                for c_ in range(-3, 4):
                    o.append(f'<path d="M{x+c_*5.4*s-2.7*s},{y-h*(0.77-r_*0.052)} q{2.7*s},{4*s} {5.4*s},0" stroke="#000" stroke-width="{0.8*s}" fill="none" opacity=".3"/>')
    o.append(f'<rect x="{x-23*s-ext}" y="{y-h*0.42}" width="{46*s+2*ext}" height="{8*s}" fill="{sash}"/><rect x="{x-3*s}" y="{y-h*0.425}" width="{7*s}" height="{9*s}" rx="{2*s}" fill="#e8d890" stroke="#8a6a20" stroke-width="{0.8*s}"/>')
    if not back:
        o.append(f'<path d="M{x+8*s},{y-h*0.4} l{4*s},{26*s} l{-9*s},0z" fill="{sash}"/>')
    o.append(_arms(x, y, s, col, pose, wide=wide))
    if pose == 'spear' and spear:
        o.append(f'<line x1="{x+27*s}" y1="{y+2*s}" x2="{x+27*s}" y2="{y-h*1.55}" stroke="#6b4a2a" stroke-width="{3.2*s}"/>')
        o.append(f'<path d="M{x+23*s},{y-h*1.55} L{x+27*s},{y-h*1.72} L{x+31*s},{y-h*1.55}Z" fill="#b9bcc4"/>')
        if spear != 'bare':
            o.append(f'<path class="pen" d="M{x+27*s},{y-h*1.5} q{26*s},{-6*s} {50*s},{4*s} q{-24*s},{8*s} {-50*s},{14*s}Z" fill="{spear}"/>')
    return ''.join(o)


def person(x, y, s, col, hat=None, face=True, hair='#17121a', turban=None, diadem=False, beard=None, seed=0,
           back=False, young=False, crown=None, look=0, long=False, wide=False, skirt=False, **kw):
    h = 150 * s
    b = body(x, y, s, col, long=long, wide=wide, skirt=skirt, back=back, **kw)
    hd = head(x, y - h * 0.98, s, face=face and not back, hat=hat, turban=turban, diadem=diadem, beard=beard,
              seed=seed, hair=hair, back=back, young=young, crown=crown, look=look)
    return f'<g class="fig">{b}{hd}</g>'


def kneeler(x, y, s, col, turban='#1b1620', seed=0, hair='#17121a', hat=None):
    h = 150 * s
    o = f'<path d="M{x-46*s},{y} Q{x-40*s},{y-60*s} {x-18*s},{y-h*0.62} L{x+18*s},{y-h*0.62} Q{x+40*s},{y-60*s} {x+46*s},{y}Z" fill="{col}"/>'
    o += f'<path d="M{x-18*s},{y-h*0.62} Q{x},{y-h*0.5} {x+18*s},{y-h*0.62} L{x+30*s},{y-h*0.4} Q{x},{y-h*0.34} {x-30*s},{y-h*0.4}Z" fill="{sh(col,.8)}"/>'
    o += head(x, y - h * 0.74, s, face=False, turban=turban, seed=seed, hair=hair, hat=hat, back=False)
    return f'<g class="fig">{o}</g>'


# ------------------------------------------------------------------ nền
SK = {
    'dusk': [(0, '#3a2a5a'), (.55, '#d0627a'), (1, '#ffc58a')],
    'day': [(0, '#5d9bc2'), (.6, '#cfe5ec'), (1, '#f7eed6')],
    'night': [(0, '#070b24'), (.6, '#16224a'), (1, '#2c3b6a')],
    'grey': [(0, '#6f7a85'), (.6, '#9fa8b0'), (1, '#c8ccce')],
    'dawn': [(0, '#5c6c9e'), (.55, '#e6a49f'), (1, '#ffe2b8')],
    'smoke': [(0, '#4a3a3a'), (.55, '#b8683f'), (1, '#e8a45e')],
}
MT = {
    'dusk': ('#a8707c', '#7a5068', '#523a56'),
    'day': ('#8aa3b0', '#62798a', '#41596a'),
    'night': ('#26335a', '#1b2547', '#121a38'),
    'grey': ('#8a949c', '#6c777f', '#55606a'),
    'dawn': ('#a7919f', '#7d6a85', '#574a66'),
    'smoke': ('#8a5a4a', '#6a4638', '#4a3028'),
}
GR = {'dusk': '#2a2030', 'day': '#62793f', 'night': '#101a2a', 'grey': '#59614a', 'dawn': '#4a5a4a', 'smoke': '#4a3a30'}


def svg(layers, kind='day', extra_defs=''):
    st = SK[kind]
    g = ('<linearGradient id="sk" x1="0" y1="0" x2="0" y2="1">' +
         ''.join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in st) + '</linearGradient>')
    grain = ('<filter id="gr"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="3"/>'
             '<feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .07 0"/></filter>')
    body_ = ''.join(layers)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
            f'<defs>{g}{grain}<radialGradient id="vg" cx=".5" cy=".5" r=".75"><stop offset=".6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".28"/></radialGradient>{extra_defs}</defs>{body_}<rect width="{W}" height="{H}" fill="url(#vg)"/><rect width="{W}" height="{H}" filter="url(#gr)"/></svg>')


def G(name, content):
    return f'<g id="{name}">{content}</g>'


def sky(kind, sun=None, moon=False, stars=False):
    o = '<rect width="1920" height="1080" fill="url(#sk)"/>'
    if sun and kind != 'night':
        x, y = sun
        c = '#ffe7bd' if kind in ('dusk', 'dawn', 'smoke') else '#fff6dc'
        o += f'<circle cx="{x}" cy="{y}" r="220" fill="{c}" opacity=".18"/><circle cx="{x}" cy="{y}" r="140" fill="{c}" opacity=".3"/><circle cx="{x}" cy="{y}" r="96" fill="{c}"/>'
    if moon or kind == 'night':
        x, y = moon if isinstance(moon, tuple) else (1450, 250)
        o += f'<circle cx="{x}" cy="{y}" r="160" fill="#dfe8ff" opacity=".12"/><circle cx="{x}" cy="{y}" r="70" fill="#f1f5ff"/><circle cx="{x+22}" cy="{y-10}" r="64" fill="url(#sk)" opacity="0"/>'
    if stars or kind == 'night':
        r = random.Random(11)
        for _ in range(110):
            o += f'<circle cx="{r.randint(0,1920)}" cy="{r.randint(0,560)}" r="{r.choice([1.2,1.6,2.2,2.8])}" fill="#fff" opacity="{r.uniform(.5,1):.2f}"/>'
    return G('sky', o)


def clouds(kind, seed=1, n=6):
    col = {'dusk': '#f6a77d', 'day': '#ffffff', 'night': '#3a4a7a', 'grey': '#dfe2e4', 'dawn': '#ffd3b0', 'smoke': '#8a6a5a'}[kind]
    op = .45 if kind != 'grey' else .6
    r = random.Random(seed)
    o = ''
    for _ in range(n):
        x, y, w = r.randint(0, 1920), r.randint(60, 330), r.randint(180, 420)
        o += (f'<ellipse cx="{x}" cy="{y}" rx="{w}" ry="{w*0.055}" fill="{col}" opacity="{op}"/>'
              f'<ellipse cx="{x+w*.25}" cy="{y-9}" rx="{w*.6}" ry="{w*0.04}" fill="{col}" opacity="{op}"/>')
    return G('clouds', o)


def birds(x, y, seed=3, col='#3a2a45', n=8):
    r = random.Random(seed)
    o = ''
    for _ in range(n):
        a, b, s = x + r.randint(-140, 140), y + r.randint(-60, 60), r.uniform(.6, 1.3)
        o += f'<path d="M{a-14*s},{b} Q{a-7*s},{b-9*s} {a},{b} Q{a+7*s},{b-9*s} {a+14*s},{b}" stroke="{col}" stroke-width="2.4" fill="none"/>'
    return G('birds', o)


def mountains(kind, base=650, seed=3):
    c1, c2, c3 = MT[kind]
    o = ''
    for k, (b, amp, c, sd) in enumerate(((base, 280, c1, seed), (base + 90, 220, c2, seed + 4), (base + 170, 150, c3, seed + 8))):
        r = random.Random(sd)
        pts = [f'0,{H}'] + [f'{i*W/11:.0f},{b-r.random()*amp:.0f}' for i in range(12)] + [f'{W},{H}']
        o += f'<polygon points="{" ".join(pts)}" fill="{c}"/>'
        if k < 2:
            o += f'<rect y="{b-amp*0.45}" width="{W}" height="{amp*0.5}" fill="#ffffff" opacity=".07"/>'
    return G('mountains', o)


def ground(kind, y=860, col=None):
    return G('ground', f'<rect y="{y}" width="1920" height="{H-y}" fill="{col or GR[kind]}"/>')


def rice(y0=790, n=8, base='#62793f', line='#86a352'):
    o = f'<rect y="{y0}" width="1920" height="{H-y0}" fill="{base}"/>'
    for i in range(n):
        y = y0 + 4 + i * 32
        o += f'<rect y="{y}" width="1920" height="8" fill="{line}" opacity=".8"/>'
    o += f'<rect y="{y0}" width="1920" height="12" fill="#8db3c4" opacity=".55"/>'
    return G('rice', o)


def road(kind='day', top=(740, 1180), y=780, col='#b8905f'):
    c = {'night': '#4a4038', 'dusk': '#7a5a48', 'grey': '#8a7a62', 'smoke': '#7a5a40'}.get(kind, col)
    return G('road', f'<polygon points="{top[0]},{y} {top[1]},{y} 1920,1080 0,1080" fill="{c}"/>')


def hut(x, y, s, wall='#7a5a3a', roof='#5a4128', line='#3a2a1a'):
    o = f'<rect x="{x-52*s}" y="{y-48*s}" width="{104*s}" height="{48*s}" fill="{wall}"/><rect x="{x-12*s}" y="{y-36*s}" width="{24*s}" height="{36*s}" fill="#1a1216"/>'
    o += f'<path d="M{x-80*s},{y-42*s} L{x},{y-112*s} L{x+80*s},{y-42*s}Z" fill="{roof}"/>'
    for k in range(1, 6):
        o += f'<line x1="{x-80*s+k*13*s}" y1="{y-42*s}" x2="{x}" y2="{y-112*s}" stroke="{line}" stroke-width="{1.4*s}" opacity=".6"/>'
    return o


def huts(kind, items):
    pal = {'day': ('#7a5a3a', '#5a4128', '#3a2a1a'), 'dusk': ('#3a2a3a', '#231a2b', '#4a3a52'),
           'night': ('#1e2640', '#141a30', '#2a3454'), 'grey': ('#6a5a48', '#4a3e32', '#2e2620'),
           'dawn': ('#5a4a50', '#3a2e38', '#2a2030'), 'smoke': ('#4a3228', '#2e1e18', '#1e130e')}[kind]
    return G('huts', ''.join(hut(x, y, s, *pal) for x, y, s in items))


def tree(x, y, s, kind='day'):
    trunk, leaf = {'day': ('#4a3524', '#2f4a2a'), 'dusk': ('#2a1f2e', '#35283b'), 'night': ('#0c1220', '#14223a'),
                   'grey': ('#3e3228', '#3c4a34'), 'dawn': ('#2e2430', '#34423a'), 'smoke': ('#2a1a14', '#3a2a20')}[kind]
    o = f'<path d="M{x-14*s},{y} L{x-8*s},{y-130*s} L{x+8*s},{y-130*s} L{x+14*s},{y}Z" fill="{trunk}"/>'
    for dx, dy, r in ((0, -190, 80), (-70, -150, 60), (70, -150, 64), (-30, -240, 50), (40, -230, 52)):
        o += f'<circle cx="{x+dx*s}" cy="{y+dy*s}" r="{r*s}" fill="{leaf}"/>'
    return G('tree', o)


def bamboo(x, y, s, kind='day', n=6):
    col, dark = {'day': ('#2c5a3a', '#1d3d27'), 'dusk': ('#2a2f3a', '#1c2029'), 'night': ('#14263a', '#0c1826'),
                 'grey': ('#3a5a44', '#2a4232'), 'dawn': ('#2c4a40', '#1e3430'), 'smoke': ('#2a3a2a', '#1a261a')}[kind]
    o = ''
    for i in range(n):
        dx = x + i * 22 * s
        hh = (300 + i * 35) * s
        lean = (i % 3 - 1) * 26 * s
        o += f'<path d="M{dx},{y} Q{dx+lean/2},{y-hh/2} {dx+lean},{y-hh}" stroke="{col}" stroke-width="{7*s}" fill="none"/>'
        for k in range(1, 6):
            t = k / 6
            px, py = dx + lean * t * t, y - hh * t
            o += f'<line x1="{px-5*s}" y1="{py}" x2="{px+5*s}" y2="{py}" stroke="{dark}" stroke-width="{2*s}"/>'
            if k > 2:
                o += (f'<path d="M{px},{py} q{36*s},{-8*s} {60*s},{14*s} q{-34*s},{0} {-60*s},{-14*s}Z" fill="{dark}"/>'
                      f'<path d="M{px},{py} q{-36*s},{-8*s} {-58*s},{12*s} q{34*s},{0} {58*s},{-12*s}Z" fill="{col}"/>')
    return G('bamboo', o)


def pagoda(x, y, s, wall, roof, line, glow=True):
    o = f'<rect x="{x-120*s}" y="{y-110*s}" width="{240*s}" height="{110*s}" fill="{wall}"/>'
    for k in range(5):
        o += f'<rect x="{x-110*s+k*46*s}" y="{y-110*s}" width="{6*s}" height="{110*s}" fill="{sh(wall,.8)}"/>'
    o += f'<path d="M{x-175*s},{y-100*s} Q{x-130*s},{y-112*s} {x-100*s},{y-150*s} L{x+100*s},{y-150*s} Q{x+130*s},{y-112*s} {x+175*s},{y-100*s}Z" fill="{roof}"/>'
    o += (f'<path d="M{x-175*s},{y-100*s} q{-14*s},{-10*s} {-6*s},{-26*s}" stroke="{roof}" stroke-width="{7*s}" fill="none"/>'
          f'<path d="M{x+175*s},{y-100*s} q{14*s},{-10*s} {6*s},{-26*s}" stroke="{roof}" stroke-width="{7*s}" fill="none"/>')
    for k in range(7):
        o += f'<line x1="{x-150*s+k*50*s}" y1="{y-148*s}" x2="{x-170*s+k*56*s}" y2="{y-102*s}" stroke="{line}" stroke-width="{2*s}"/>'
    o += f'<rect x="{x-78*s}" y="{y-240*s}" width="{156*s}" height="{92*s}" fill="{wall}"/>'
    o += f'<path d="M{x-120*s},{y-232*s} Q{x-80*s},{y-244*s} {x-52*s},{y-282*s} L{x+52*s},{y-282*s} Q{x+80*s},{y-244*s} {x+120*s},{y-232*s}Z" fill="{roof}"/>'
    o += f'<path d="M{x-14*s},{y-282*s} L{x},{y-312*s} L{x+14*s},{y-282*s}Z" fill="{roof}"/>'
    o += f'<rect x="{x-26*s}" y="{y-92*s}" width="{52*s}" height="{92*s}" rx="{26*s}" fill="#150f18"/>'
    if glow:
        for k in (-1, 1):
            o += f'<rect x="{x+k*38*s-8*s}" y="{y-205*s}" width="{16*s}" height="{36*s}" rx="{8*s}" fill="#ffcf6a" opacity=".85"/>'
    return o


WALLC = {'viet': ('#5a4458', '#1c1522', '#33273a'), 'song': ('#566070', '#16202c', '#2e3a48'),
         'day': ('#9a8a78', '#4a3a34', '#6a5a50'), 'grey': ('#7a8088', '#2e343c', '#505860')}


def wall(y=760, kind='dusk', tower_x=None, side='viet', h=320, merlon=True):
    base = {'dusk': '#4a3a48', 'night': '#222a40', 'day': '#9a8a78', 'grey': '#7a8088', 'dawn': '#5a4a58', 'smoke': '#5a4036'}[kind]
    line = sh(base, .78)
    o = f'<rect y="{y}" width="1920" height="{h}" fill="{base}"/>'
    for r in range(0, int(h / 40)):
        yy = y + 10 + r * 40
        o += f'<line x1="0" y1="{yy}" x2="1920" y2="{yy}" stroke="{line}" stroke-width="2"/>'
        for k in range(0, 1920, 110):
            o += f'<line x1="{k+(r%2)*55}" y1="{yy}" x2="{k+(r%2)*55}" y2="{yy+40}" stroke="{line}" stroke-width="2"/>'
    if merlon:
        for i in range(0, 1920, 100):
            o += f'<rect x="{i+14}" y="{y-44}" width="70" height="46" fill="{base}"/><rect x="{i+14}" y="{y-44}" width="70" height="8" fill="{sh(base,1.15)}"/>'
    o += f'<rect y="{y}" width="1920" height="12" fill="{sh(base,1.2)}"/>'
    if tower_x is not None:
        wc, rc, lc = WALLC[side]
        if kind == 'night':
            wc, rc, lc = sh(wc, .55), sh(rc, .6), sh(lc, .6)
        o += pagoda(tower_x, y, 1.55, wc, rc, lc)
    return G('wall', o)


def pennant(x, ytop, ybase, col='#a8452f', length=150, ph=0):
    return (f'<g class="pen"><line x1="{x}" y1="{ybase}" x2="{x}" y2="{ytop}" stroke="#2a1d1a" stroke-width="7"/>'
            f'<path d="M{x},{ytop+8} Q{x-70},{ytop+14} {x-length},{ytop+34} Q{x-70},{ytop+44} {x},{ytop+64}Z" fill="{col}"/>'
            f'<path d="M{x},{ytop+8} Q{x-70},{ytop+14} {x-length},{ytop+34} L{x-70},{ytop+30}Z" fill="{sh(col,1.2)}"/></g>')


def torch(x, y, s=1):
    return (f'<g class="fire"><rect x="{x-6*s}" y="{y-124*s}" width="{12*s}" height="{124*s}" fill="#2a1d1a"/>'
            f'<path d="M{x},{y-164*s} q{18*s},{26*s} 0,{52*s} q{-18*s},{-26*s} 0,{-52*s}" fill="#ffb347"/>'
            f'<circle cx="{x}" cy="{y-134*s}" r="{52*s}" fill="#ffb347" opacity=".18"/></g>')


def campfire(x, y, s=1):
    return (f'<g class="fire"><circle cx="{x}" cy="{y-20*s}" r="{70*s}" fill="#ffb347" opacity=".2"/>'
            f'<path d="M{x-26*s},{y} L{x+26*s},{y-10*s} M{x+26*s},{y} L{x-26*s},{y-10*s}" stroke="#4a2c20" stroke-width="{7*s}"/>'
            f'<path d="M{x},{y-62*s} q{22*s},{28*s} {10*s},{54*s} q{-16*s},{6*s} {-30*s},{0} q{-12*s},{-26 *s} {20*s},{-54*s}" fill="#ff9a3c"/>'
            f'<path d="M{x},{y-34*s} q{10*s},{14*s} {4*s},{28*s} q{-8*s},{3*s} {-14*s},{0} q{-4*s},{-14*s} {10*s},{-28*s}" fill="#ffd25a"/></g>')


def smoke(x, y, h=200, col='#ffffff', op=.3, w=12):
    return (f'<path class="smoke" d="M{x},{y} q-16,-{h*0.2} 8,-{h*0.38} q22,-{h*0.26} -6,-{h*0.42}" stroke="{col}" stroke-width="{w}" fill="none" opacity="{op}" stroke-linecap="round"/>')


def tent(x, y, s, col='#9a8a68', dark='#6a5a40', cap='#c9b890'):
    return (f'<path d="M{x-90*s},{y} L{x},{y-100*s} L{x+90*s},{y}Z" fill="{col}"/><path d="M{x},{y-100*s} L{x+90*s},{y} L{x+10*s},{y}Z" fill="{dark}"/>'
            f'<path d="M{x-14*s},{y} L{x},{y-48*s} L{x+14*s},{y}Z" fill="#1a1216"/><line x1="{x}" y1="{y-100*s}" x2="{x}" y2="{y-120*s}" stroke="{dark}" stroke-width="{3*s}"/>')


def river(y0=760, y1=1080, kind='day'):
    c = {'day': ('#5f95b0', '#8fbad0'), 'dusk': ('#6a4a70', '#d0627a'), 'night': ('#101a38', '#2c3b6a'),
         'grey': ('#6a7c88', '#9fb0ba'), 'dawn': ('#7a86a8', '#e6a49f'), 'smoke': ('#6a4a40', '#c0734a')}[kind]
    o = f'<defs><linearGradient id="rv" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c[1]}"/><stop offset="1" stop-color="{c[0]}"/></linearGradient></defs>'
    o += f'<rect y="{y0}" width="1920" height="{y1-y0}" fill="url(#rv)"/>'
    r = random.Random(5)
    for _ in range(26):
        x, y, w = r.randint(0, 1900), r.randint(y0 + 20, y1 - 10), r.randint(40, 150)
        o += f'<path d="M{x},{y} q{w/4},-6 {w/2},0 t{w/2},0" stroke="#ffffff" stroke-width="2.5" fill="none" opacity=".35"/>'
    return G('river', o)


def boat(x, y, s, sail=True, col='#6a4a2a'):
    o = f'<path d="M{x-110*s},{y-20*s} Q{x},{y+22*s} {x+110*s},{y-20*s} L{x+88*s},{y-4*s} Q{x},{y+14*s} {x-88*s},{y-4*s}Z" fill="{col}"/>'
    o += f'<rect x="{x-90*s}" y="{y-24*s}" width="{180*s}" height="{6*s}" fill="{sh(col,.7)}"/>'
    if sail:
        o += f'<line x1="{x}" y1="{y-22*s}" x2="{x}" y2="{y-150*s}" stroke="#3a2a1a" stroke-width="{5*s}"/>'
        o += f'<path d="M{x+4*s},{y-146*s} Q{x+70*s},{y-90*s} {x+4*s},{y-34*s}Z" fill="#cdb88a"/>'
        for k in range(1, 4):
            o += f'<line x1="{x+4*s}" y1="{y-146*s+k*28*s}" x2="{x+50*s}" y2="{y-130*s+k*24*s}" stroke="#9a8658" stroke-width="{1.5*s}"/>'
    return G('boat', o)


def palisade(x0, x1, y, s=1, col='#6a4a2a'):
    o = ''
    x = x0
    while x < x1:
        hh = (110 + (int(x) * 7) % 22) * s
        o += f'<path d="M{x},{y} L{x},{y-hh} L{x+9*s},{y-hh-16*s} L{x+18*s},{y-hh} L{x+18*s},{y}Z" fill="{col}"/><line x1="{x+9*s}" y1="{y}" x2="{x+9*s}" y2="{y-hh}" stroke="{sh(col,.7)}" stroke-width="{1.4*s}"/>'
        x += 19 * s
    o += f'<rect x="{x0}" y="{y-54*s}" width="{x1-x0}" height="{7*s}" fill="{sh(col,.7)}"/>'
    return G('palisade', o)


def sacks(x, y, s, n=5):
    o = ''
    for i in range(n):
        o += f'<ellipse cx="{x+i*46*s-n*20*s}" cy="{y-14*s}" rx="{26*s}" ry="{16*s}" fill="#b09a68"/><path d="M{x+i*46*s-n*20*s-8*s},{y-26*s} q{8*s},{-8*s} {16*s},0" stroke="#7a6a44" stroke-width="{2*s}" fill="none"/>'
    return o


def mat(poly, col='#b08a54'):
    return f'<polygon points="{poly}" fill="{col}"/>'


def oildish(x, y, s=1, glow=True):
    o = (f'<g class="fire"><rect x="{x-14*s}" y="{y}" width="{28*s}" height="{206*s}" fill="#3a251c"/><rect x="{x-34*s}" y="{y-4*s}" width="{68*s}" height="{14*s}" fill="#5a3a2a"/>'
         f'<ellipse cx="{x}" cy="{y-6*s}" rx="{32*s}" ry="{9*s}" fill="#8a5a3a"/><path d="M{x},{y-10*s} q{12*s},{-34*s} 0,{-52*s} q{-12*s},{18*s} 0,{52*s}z" fill="#ffd25a"/>')
    if glow:
        o += f'<circle cx="{x}" cy="{y-40*s}" r="{70*s}" fill="#ffd25a" opacity=".22"/>'
    return o + '</g>'


def hall(kind='gold', glow_center=(960, 560), windows=(330, 1590), curtains=True, floor_y=946, curtain='#8a2a24'):
    """Bên trong điện: xà gỗ, cột nâu, cửa chấn song gỗ không kính, rèm vải."""
    dim = kind == 'dim'
    bgc, wall_c = ('#1e1412', '#2a1c18') if dim else ('#2b1c18', '#3a2620')
    o = f'<rect width="1920" height="1080" fill="{bgc}"/><rect width="1920" height="150" fill="#120b0a"/>'
    for x in range(60, 1900, 170):
        o += f'<rect x="{x}" y="60" width="18" height="100" fill="#3a241c"/>'
    o += '<rect y="130" width="1920" height="40" fill="#4a2c20"/><rect y="168" width="1920" height="8" fill="#e0b040" opacity=".5"/>'
    o += f'<rect y="176" width="1920" height="{floor_y-176}" fill="{wall_c}"/>'
    o += ('<defs><radialGradient id="gl"><stop offset="0" stop-color="#ffd48a" stop-opacity="%s"/><stop offset="1" stop-color="#ffd48a" stop-opacity="0"/></radialGradient></defs>' % ('.5' if dim else '.95'))
    o += f'<ellipse cx="{glow_center[0]}" cy="{glow_center[1]}" rx="760" ry="430" fill="url(#gl)"/>'
    for cx in windows:
        o += f'<rect x="{cx-140}" y="260" width="280" height="420" fill="#ffcf80" opacity="{.3 if dim else .55}"/>'
        for k in range(1, 6):
            o += f'<line x1="{cx-140+k*46.6}" y1="260" x2="{cx-140+k*46.6}" y2="680" stroke="#4a2c20" stroke-width="8"/>'
        for k in range(1, 5):
            o += f'<line x1="{cx-140}" y1="{260+k*84}" x2="{cx+140}" y2="{260+k*84}" stroke="#4a2c20" stroke-width="8"/>'
        o += f'<rect x="{cx-148}" y="252" width="296" height="436" fill="none" stroke="#4a2c20" stroke-width="14"/>'
    if curtains:
        for x, w in ((700, 150), (1070, 150)):
            o += f'<path d="M{x},176 L{x+w},176 L{x+w-10},700 Q{x+w/2},720 {x+10},700Z" fill="{curtain}"/>'
            for k in range(1, 5):
                o += f'<line x1="{x+k*w/5}" y1="176" x2="{x+k*w/5}" y2="700" stroke="{sh(curtain,.75)}" stroke-width="3"/>'
    for x in (150, 520, 1400, 1770):
        o += f'<rect x="{x-38}" y="176" width="76" height="{floor_y-176+10}" fill="#5a3426"/><rect x="{x-38}" y="176" width="22" height="{floor_y-166}" fill="#7a4a34"/><rect x="{x-48}" y="{floor_y-46}" width="96" height="46" fill="#2f1b14"/>'
    o += f'<rect y="{floor_y}" width="1920" height="{H-floor_y}" fill="#2f1f19"/>'
    return G('hall', o)


def throne(x=960, y=830, gold='#e0b040', seat='#8a2a24'):
    o = f'<rect x="{x-260}" y="{y+50}" width="520" height="66" fill="#6a3a2a"/><rect x="{x-220}" y="{y-4}" width="440" height="56" fill="#7d4634"/><rect x="{x-220}" y="{y-4}" width="440" height="8" fill="{gold}"/>'
    o += f'<rect x="{x-140}" y="{y-270}" width="280" height="270" rx="16" fill="{seat}"/><rect x="{x-140}" y="{y-270}" width="280" height="14" fill="{gold}"/>'
    o += f'<path d="M{x-150},{y-260} Q{x},{y-400} {x+150},{y-260} Q{x},{y-310} {x-150},{y-260}Z" fill="{gold}"/>'
    for sd in (-1, 1):
        o += f'<path d="M{x+sd*160},{y-70} q{sd*50},-60 0,-120 q{sd*-10},50 {sd*-40},120Z" fill="{gold}"/>'
    return G('throne', o)


def scroll_blank(x, y, s=1, col='#e8dcc0'):
    return (f'<rect x="{x-26*s}" y="{y-8*s}" width="{52*s}" height="{16*s}" rx="{6*s}" fill="{col}"/>'
            f'<rect x="{x-30*s}" y="{y-10*s}" width="{6*s}" height="{20*s}" rx="{3*s}" fill="#6a4a2a"/><rect x="{x+24*s}" y="{y-10*s}" width="{6*s}" height="{20*s}" rx="{3*s}" fill="#6a4a2a"/>')


def lowtable(x, y, w=240, h=60, col='#5a3a2a'):
    return (f'<rect x="{x-w/2}" y="{y-h}" width="{w}" height="{12}" fill="{sh(col,1.2)}"/><rect x="{x-w/2+10}" y="{y-h+12}" width="{12}" height="{h-12}" fill="{col}"/><rect x="{x+w/2-22}" y="{y-h+12}" width="{12}" height="{h-12}" fill="{col}"/>')


def maptable(x, y, w=260):
    """Tấm bản đồ vẽ nét (không chữ) trải trên bàn thấp."""
    return (f'<polygon points="{x-w/2},{y-62} {x+w/2},{y-62} {x+w/2+20},{y-44} {x-w/2-20},{y-44}" fill="#e2d4b0"/>'
            f'<path d="M{x-w/2+14},{y-56} q{w/6},-4 {w/3},2 t{w/3},-2" stroke="#8a6a3a" stroke-width="2.5" fill="none"/>'
            f'<path d="M{x-w/4},{y-50} l{w/8},-4 l{w/10},4" stroke="#8a6a3a" stroke-width="2.5" fill="none"/>' + lowtable(x, y - 44, w + 30, 44))


def cart_overturned(x, y, s=1):
    return (f'<g><rect x="{x-70*s}" y="{y-36*s}" width="{140*s}" height="{18*s}" fill="#6a4a2a" transform="rotate(-24 {x} {y})"/>'
            f'<circle cx="{x+40*s}" cy="{y-24*s}" r="{34*s}" fill="none" stroke="#4a3220" stroke-width="{6*s}"/>'
            f'<line x1="{x+40*s-34*s}" y1="{y-24*s}" x2="{x+40*s+34*s}" y2="{y-24*s}" stroke="#4a3220" stroke-width="{4*s}"/>'
            f'<line x1="{x+40*s}" y1="{y-58*s}" x2="{x+40*s}" y2="{y+10*s}" stroke="#4a3220" stroke-width="{4*s}"/></g>')


def cart(x, y, s=1):
    return (f'<rect x="{x-70*s}" y="{y-70*s}" width="{140*s}" height="{26*s}" fill="#6a4a2a"/>'
            f'<rect x="{x-60*s}" y="{y-96*s}" width="{120*s}" height="{26*s}" fill="#9a8658"/>'
            f'<circle cx="{x-40*s}" cy="{y-26*s}" r="{30*s}" fill="none" stroke="#4a3220" stroke-width="{6*s}"/><circle cx="{x+40*s}" cy="{y-26*s}" r="{30*s}" fill="none" stroke="#4a3220" stroke-width="{6*s}"/>'
            f'<line x1="{x-70*s}" y1="{y-26*s}" x2="{x-110*s}" y2="{y-34*s}" stroke="#4a3220" stroke-width="{5*s}"/>')


def elephant(x, y, s=1, col='#7d7a80', rider=None):
    o = f'<ellipse cx="{x}" cy="{y-110*s}" rx="{120*s}" ry="{80*s}" fill="{col}"/>'
    for dx in (-80, -30, 36, 86):
        o += f'<rect x="{x+dx*s-18*s}" y="{y-80*s}" width="{36*s}" height="{80*s}" rx="{12*s}" fill="{sh(col,.85)}"/>'
    o += f'<ellipse cx="{x+110*s}" cy="{y-140*s}" rx="{46*s}" ry="{50*s}" fill="{col}"/>'
    o += f'<path d="M{x+140*s},{y-120*s} q{30*s},{40*s} {10*s},{96*s} q{-8*s},{6*s} {-16*s},{0} q{10*s},{-50*s} {-18*s},{-70*s}Z" fill="{sh(col,.92)}"/>'
    o += f'<ellipse cx="{x+90*s}" cy="{y-142*s}" rx="{20*s}" ry="{32*s}" fill="{sh(col,.8)}"/>'
    o += f'<circle cx="{x+128*s}" cy="{y-150*s}" r="{4*s}" fill="#1a1216"/>'
    o += f'<path d="M{x+128*s},{y-118*s} q{26*s},{16*s} {32*s},{-2*s}" stroke="#efe6d0" stroke-width="{8*s}" fill="none" stroke-linecap="round"/>'
    o += f'<path d="M{x-40*s},{y-182*s} L{x+60*s},{y-182*s} L{x+50*s},{y-150*s} L{x-30*s},{y-150*s}Z" fill="#8a2a24"/>'
    return G('elephant', o)
