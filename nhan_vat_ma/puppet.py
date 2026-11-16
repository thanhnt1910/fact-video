"""Nhân vật chibi mặt trắng trơn vẽ hoàn toàn bằng mã (SVG), ghép từ các mảnh rời.

Mọi thứ do mã quyết định nên không bao giờ thừa tay, mất đồ hay lệch mặt:
- mỗi người đúng hai tay, vị trí tay tính bằng IK hai khúc từ tọa độ bàn tay;
- kiếm luôn nằm trong bao (chỉ vẽ bao và chuôi);
- mặt (mắt, mày, miệng, ria...) là lớp riêng, đổi biểu cảm bằng tham số.
"""
import math
from dataclasses import dataclass, field

CX = 300          # trục giữa nhân vật
GROUND = 735
HEAD_R = 118
INK = "#16120f"


def _ik(S, T, L1, L2, side):
    """Hai khúc xương: trả về khuỷu tay. side=+1 tay phải màn hình, -1 tay trái."""
    dx, dy = T[0] - S[0], T[1] - S[1]
    d = math.hypot(dx, dy)
    d = max(abs(L1 - L2) + 1e-3, min(L1 + L2 - 1e-3, d))
    ux, uy = dx / math.hypot(dx, dy or 1e-9), dy / math.hypot(dx or 1e-9, dy)
    n = math.hypot(dx, dy) or 1e-9
    ux, uy = dx / n, dy / n
    a = (L1 * L1 - L2 * L2 + d * d) / (2 * d)
    h = math.sqrt(max(L1 * L1 - a * a, 0))
    px, py = S[0] + a * ux, S[1] + a * uy
    c1 = (px - h * uy, py + h * ux)
    c2 = (px + h * uy, py - h * ux)
    # chọn khuỷu hướng ra ngoài và xuống dưới
    sc = lambda c: (c[0] - CX) * side + 0.35 * c[1]
    E = c1 if sc(c1) > sc(c2) else c2
    # chặn đầu hàng: hạn chế tay thật dài
    return E, (S[0] + dx * min(1, (L1 + L2 - 1e-3) / n), S[1] + dy * min(1, (L1 + L2 - 1e-3) / n))


def _stroke_limb(p, q, w, fill):
    return (f'<line x1="{p[0]:.1f}" y1="{p[1]:.1f}" x2="{q[0]:.1f}" y2="{q[1]:.1f}" stroke="{INK}" '
            f'stroke-width="{w + 10}" stroke-linecap="round"/>'
            f'<line x1="{p[0]:.1f}" y1="{p[1]:.1f}" x2="{q[0]:.1f}" y2="{q[1]:.1f}" stroke="{fill}" '
            f'stroke-width="{w}" stroke-linecap="round"/>')


@dataclass
class Look:
    """Bộ nhận diện một nhân vật (màu giáp, tóc, đặc điểm mặt)."""
    name: str = "Nobunaga"
    armor: str = "#7a2026"
    armor_dark: str = "#521418"
    trim: str = "#d2a24a"
    cape: str = "#1d1c22"
    cape_lining: str = "#a8252d"
    sleeve: str = "#1c1a1e"
    moustache: bool = True
    big_ears: bool = False
    whiskers: bool = False
    round_body: float = 1.0       # 1.0 = người thường, >1 = tròn hơn
    scale: float = 1.0            # <1 = nhỏ người
    hair_streak: bool = False
    headband: str = "#a8252d"
    belly: float = 0.0            # bụng tròn (0..1)
    shoe: str = "#16120f"
    kabuto: bool = False          # mũ sắt có sừng trăng
    sword: bool = True


@dataclass
class Pose:
    handL: tuple = (CX - 98, 500)     # tay trái màn hình (bàn tay)
    handR: tuple = (CX + 98, 500)
    legL: tuple = (0, 0)              # độ dịch chân (dx, nâng lên dy)
    legR: tuple = (0, 0)
    bob: float = 0.0                  # nhấp nhô cả người
    head_dy: float = 0.0
    head_tilt: float = 0.0            # độ nghiêng đầu
    torso_lean: float = 0.0
    prop_L: str = ""                  # '' | 'banner'
    prop_R: str = ""                  # '' | 'katana_hand'


@dataclass
class Face:
    eyes: str = "angry"    # angry | surprised | cheeky | sleepy | calm
    mouth: str = "flat"    # flat | open | grin | smile | frown
    brows: str = "angry"   # angry | raised | calm | one
    sweat: bool = False
    blush: bool = False


# ---------------------------------------------------------------- mảnh rời
def _legs(look, pose, y0):
    out = []
    for side, off in ((-1, pose.legL), (1, pose.legR)):
        x = CX + side * 34 + off[0]
        top = y0
        bot = GROUND - 22 - off[1]
        out.append(_stroke_limb((x, top), (x, bot), 50, "#26232b"))
        out.append(f'<ellipse cx="{x + side * 4:.1f}" cy="{bot + 14 - 0:.1f}" rx="34" ry="16" fill="{look.shoe}" stroke="{INK}" stroke-width="6"/>')
    return "".join(out)


def _cape(look, y_sh):
    c, l = look.cape, look.cape_lining
    p = (f'M{CX - 92},{y_sh} Q{CX - 150},{y_sh + 160} {CX - 140},{y_sh + 290} '
         f'L{CX + 140},{y_sh + 290} Q{CX + 150},{y_sh + 160} {CX + 92},{y_sh} Z')
    lining = (f'M{CX - 120},{y_sh + 130} Q{CX - 148},{y_sh + 210} {CX - 140},{y_sh + 290} '
              f'L{CX - 90},{y_sh + 290} Z M{CX + 120},{y_sh + 130} Q{CX + 148},{y_sh + 210} {CX + 140},{y_sh + 290} '
              f'L{CX + 90},{y_sh + 290} Z')
    return (f'<path d="{p}" fill="{c}" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>'
            f'<path d="{lining}" fill="{l}" stroke="{INK}" stroke-width="5"/>')


def _torso(look, y_t, w_extra=0):
    tw = 150 + w_extra
    x0, x1 = CX - tw / 2, CX + tw / 2
    h = 170
    a, ad, t = look.armor, look.armor_dark, look.trim
    s = [f'<rect x="{x0}" y="{y_t}" width="{tw}" height="{h}" rx="22" fill="{a}" stroke="{INK}" stroke-width="8"/>']
    # hàng giáp ngang
    for i in range(1, 7):
        yy = y_t + i * 24
        s.append(f'<line x1="{x0 + 8}" y1="{yy}" x2="{x1 - 8}" y2="{yy}" stroke="{ad}" stroke-width="4"/>')
    # dây buộc giữa
    s.append(f'<line x1="{CX}" y1="{y_t + 8}" x2="{CX}" y2="{y_t + h - 8}" stroke="{t}" stroke-width="5"/>')
    for i in range(0, 7):
        s.append(f'<circle cx="{CX}" cy="{y_t + 12 + i * 24}" r="4" fill="{t}"/>')
    # viền cổ áo
    s.append(f'<path d="M{CX - 34},{y_t} L{CX},{y_t + 36} L{CX + 34},{y_t}" fill="none" stroke="{t}" stroke-width="6"/>')
    return "".join(s)


def _skirt(look, y_s, w_extra=0):
    a, ad, t = look.armor, look.armor_dark, look.trim
    s = []
    tw = 165 + w_extra
    # đai
    s.append(f'<rect x="{CX - tw / 2}" y="{y_s - 22}" width="{tw}" height="30" rx="10" fill="{ad}" stroke="{INK}" stroke-width="7"/>')
    s.append(f'<circle cx="{CX}" cy="{y_s - 7}" r="14" fill="{t}" stroke="{INK}" stroke-width="5"/>')
    # ba tấm váy giáp (kusazuri)
    pw = tw / 3
    for i in range(3):
        x = CX - tw / 2 + i * pw
        s.append(f'<path d="M{x + 4},{y_s + 6} L{x + pw - 4},{y_s + 6} L{x + pw - 10},{y_s + 78} L{x + 10},{y_s + 78} Z" '
                 f'fill="{a}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
        s.append(f'<line x1="{x + 12}" y1="{y_s + 30}" x2="{x + pw - 12}" y2="{y_s + 30}" stroke="{ad}" stroke-width="4"/>')
        s.append(f'<line x1="{x + 14}" y1="{y_s + 56}" x2="{x + pw - 14}" y2="{y_s + 56}" stroke="{ad}" stroke-width="4"/>')
        s.append(f'<line x1="{x + 10}" y1="{y_s + 76}" x2="{x + pw - 10}" y2="{y_s + 76}" stroke="{t}" stroke-width="5"/>')
    return "".join(s)


def _shoulder_plate(look, S, side):
    a, ad, t = look.armor, look.armor_dark, look.trim
    x, y = S
    s = []
    for i, w in enumerate((74, 66, 58)):
        yy = y - 22 + i * 17
        s.append(f'<rect x="{x - w / 2 + side * 10}" y="{yy}" width="{w}" height="26" rx="10" fill="{a}" '
                 f'stroke="{INK}" stroke-width="6"/>')
        s.append(f'<line x1="{x - w / 2 + side * 10 + 8}" y1="{yy + 20}" x2="{x + w / 2 + side * 10 - 8}" y2="{yy + 20}" '
                 f'stroke="{t}" stroke-width="4"/>')
    return "".join(s)


def _hand(p):
    return f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="21" fill="#ffffff" stroke="{INK}" stroke-width="7"/>'


def _katana(look, hip):
    """Kiếm trong bao treo thẳng bên hông phải màn hình: chỉ thấy bao và chuôi."""
    x = CX + 92
    y = hip
    s = []
    s.append(f'<rect x="{x - 9}" y="{y + 6}" width="18" height="190" rx="9" fill="#14110f" stroke="{INK}" stroke-width="5"/>')
    for yy in (y + 40, y + 120):
        s.append(f'<rect x="{x - 11}" y="{yy}" width="22" height="9" rx="4" fill="{look.trim}" stroke="{INK}" stroke-width="3"/>')
    s.append(f'<rect x="{x - 8}" y="{y - 40}" width="16" height="48" rx="6" fill="#3a2b20" stroke="{INK}" stroke-width="5"/>')
    s.append(f'<ellipse cx="{x}" cy="{y + 6}" rx="18" ry="7" fill="{look.trim}" stroke="{INK}" stroke-width="4"/>')
    return "".join(s)


def _banner(hand, look):
    x, y = hand
    top = y - 300
    bot = y + 250
    s = [f'<line x1="{x}" y1="{top}" x2="{x}" y2="{bot}" stroke="{INK}" stroke-width="16" stroke-linecap="round"/>',
         f'<line x1="{x}" y1="{top}" x2="{x}" y2="{bot}" stroke="#6b4a2c" stroke-width="9" stroke-linecap="round"/>']
    # cờ đỏ trơn, không biểu tượng
    fx = x - 6
    cloth = (f'M{fx},{top + 6} L{fx - 120},{top + 14} Q{fx - 138},{top + 90} {fx - 118},{top + 170} '
             f'L{fx},{top + 176} Z')
    s.append(f'<path d="{cloth}" fill="#b3262d" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
    s.append(f'<line x1="{fx - 112}" y1="{top + 12}" x2="{fx - 124}" y2="{top + 168}" stroke="#7a1a1f" stroke-width="5"/>')
    return "".join(s)


def _face(face: Face, look: Look, hx, hy):
    s = []
    ex = 44
    ey = hy + 4
    # mắt
    if face.eyes == "angry":
        for sd in (-1, 1):
            s.append(f'<ellipse cx="{hx + sd * ex}" cy="{ey}" rx="8" ry="13" fill="{INK}"/>')
    elif face.eyes == "surprised":
        for sd in (-1, 1):
            s.append(f'<circle cx="{hx + sd * ex}" cy="{ey - 2}" r="16" fill="#fff" stroke="{INK}" stroke-width="5"/>')
            s.append(f'<circle cx="{hx + sd * ex}" cy="{ey - 2}" r="6" fill="{INK}"/>')
    elif face.eyes == "cheeky":
        for sd in (-1, 1):
            s.append(f'<path d="M{hx + sd * ex - 15},{ey + 4} Q{hx + sd * ex},{ey - 14} {hx + sd * ex + 15},{ey + 4}" '
                     f'fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>')
    elif face.eyes == "sleepy":
        for sd in (-1, 1):
            s.append(f'<path d="M{hx + sd * ex - 15},{ey} Q{hx + sd * ex},{ey + 12} {hx + sd * ex + 15},{ey}" '
                     f'fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>')
    else:
        for sd in (-1, 1):
            s.append(f'<circle cx="{hx + sd * ex}" cy="{ey}" r="9" fill="{INK}"/>')
    # lông mày
    by = ey - 34
    if face.brows == "angry":
        s.append(f'<path d="M{hx - ex - 24},{by - 14} L{hx - ex + 22},{by + 8}" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>')
        s.append(f'<path d="M{hx + ex + 24},{by - 14} L{hx + ex - 22},{by + 8}" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>')
    elif face.brows == "raised":
        for sd in (-1, 1):
            s.append(f'<path d="M{hx + sd * ex - 20},{by - 6} Q{hx + sd * ex},{by - 24} {hx + sd * ex + 20},{by - 6}" fill="none" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>')
    elif face.brows == "one":
        s.append(f'<path d="M{hx - ex - 20},{by + 2} L{hx - ex + 20},{by - 2}" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>')
        s.append(f'<path d="M{hx + ex - 20},{by - 12} Q{hx + ex},{by - 26} {hx + ex + 22},{by - 8}" fill="none" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>')
    else:
        for sd in (-1, 1):
            s.append(f'<path d="M{hx + sd * ex - 18},{by} L{hx + sd * ex + 18},{by}" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>')
    # ria mép
    if look.moustache:
        s.append(f'<path d="M{hx - 4},{ey + 46} Q{hx - 26},{ey + 40} {hx - 50},{ey + 56}" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>')
        s.append(f'<path d="M{hx + 4},{ey + 46} Q{hx + 26},{ey + 40} {hx + 50},{ey + 56}" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>')
    if look.whiskers:
        for sd in (-1, 1):
            for k, dy in enumerate((40, 56)):
                s.append(f'<line x1="{hx + sd * 40}" y1="{ey + dy}" x2="{hx + sd * 72}" y2="{ey + dy + (k - 0.5) * 12}" stroke="{INK}" stroke-width="3.5" stroke-linecap="round"/>')
    # miệng
    my = ey + 66
    if face.mouth == "flat":
        s.append(f'<path d="M{hx - 16},{my} L{hx + 16},{my + 2}" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>')
    elif face.mouth == "frown":
        s.append(f'<path d="M{hx - 18},{my + 6} Q{hx},{my - 8} {hx + 18},{my + 6}" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>')
    elif face.mouth == "open":
        s.append(f'<ellipse cx="{hx}" cy="{my + 4}" rx="14" ry="18" fill="#3b1015" stroke="{INK}" stroke-width="5"/>')
    elif face.mouth == "grin":
        s.append(f'<path d="M{hx - 34},{my - 6} Q{hx},{my + 40} {hx + 34},{my - 6} Z" fill="#fff" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
    else:
        s.append(f'<path d="M{hx - 20},{my - 2} Q{hx},{my + 14} {hx + 20},{my - 2}" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>')
    if face.blush:
        for sd in (-1, 1):
            s.append(f'<ellipse cx="{hx + sd * 72}" cy="{ey + 34}" rx="18" ry="10" fill="#f6a6a0" opacity="0.8"/>')
    if face.sweat:
        s.append(f'<path d="M{hx + 100},{hy - 60} q-16,28 0,40 q16,-12 0,-40 z" fill="#8fd0f0" stroke="{INK}" stroke-width="4"/>')
    return "".join(s)


def _head(look, face, hx, hy, tilt):
    r = HEAD_R
    s = [f'<g transform="rotate({tilt:.1f} {hx} {hy + r})">']
    # tai
    if look.big_ears:
        for sd in (-1, 1):
            s.append(f'<ellipse cx="{hx + sd * (r + 6)}" cy="{hy + 6}" rx="26" ry="38" fill="#fff" stroke="{INK}" stroke-width="7"/>')
            s.append(f'<ellipse cx="{hx + sd * (r + 8)}" cy="{hy + 8}" rx="11" ry="22" fill="#f0d9d2"/>')
    else:
        for sd in (-1, 1):
            s.append(f'<ellipse cx="{hx + sd * (r + 2)}" cy="{hy + 8}" rx="13" ry="22" fill="#fff" stroke="{INK}" stroke-width="6"/>')
    s.append(f'<defs><clipPath id="hc{int(hx)}"><circle cx="{hx}" cy="{hy}" r="{r}"/></clipPath></defs>')
    s.append(f'<circle cx="{hx}" cy="{hy}" r="{r}" fill="#ffffff"/>')
    # tóc (cắt theo đầu)
    s.append(f'<g clip-path="url(#hc{int(hx)})">'
             f'<path d="M{hx - r - 10},{hy - r - 10} H{hx + r + 10} V{hy - 18} Q{hx + 60},{hy - 70} {hx},{hy - 62} Q{hx - 60},{hy - 70} {hx - r - 10},{hy - 18} Z" fill="{INK}"/>'
             f'<path d="M{hx - r - 6},{hy - 30} Q{hx - r + 24},{hy + 10} {hx - r + 20},{hy + 40} L{hx - r + 6},{hy + 40} Z" fill="{INK}"/>'
             f'<path d="M{hx + r + 6},{hy - 30} Q{hx + r - 24},{hy + 10} {hx + r - 20},{hy + 40} L{hx + r - 6},{hy + 40} Z" fill="{INK}"/>')
    if look.hair_streak:
        s.append(f'<path d="M{hx - 10},{hy - 62} L{hx - 4},{hy - 100} L{hx + 14},{hy - 62} Z" fill="#8b8b92"/>')
    s.append('</g>')
    # búi tóc và băng đô
    s.append(f'<circle cx="{hx}" cy="{hy - r - 16}" r="32" fill="{INK}" stroke="{INK}" stroke-width="6"/>')
    s.append(f'<rect x="{hx - 30}" y="{hy - r + 2}" width="60" height="20" rx="7" fill="{look.headband}" stroke="{INK}" stroke-width="5"/>')
    if look.kabuto:
        s.append(f'<path d="M{hx - 10},{hy - r - 6} Q{hx - 70},{hy - r - 70} {hx - 124},{hy - r - 40} Q{hx - 80},{hy - r - 34} {hx - 28},{hy - r + 10} Z" fill="{look.trim}" stroke="{INK}" stroke-width="6"/>')
        s.append(f'<path d="M{hx + 10},{hy - r - 6} Q{hx + 70},{hy - r - 70} {hx + 124},{hy - r - 40} Q{hx + 80},{hy - r - 34} {hx + 28},{hy - r + 10} Z" fill="{look.trim}" stroke="{INK}" stroke-width="6"/>')
    s.append(f'<circle cx="{hx}" cy="{hy}" r="{r}" fill="none" stroke="{INK}" stroke-width="9"/>')
    s.append(_face(face, look, hx, hy))
    s.append('</g>')
    return "".join(s)


# ----------------------------------------------------------------- ghép
def render_svg(look: Look, pose: Pose, face: Face, w=600, h=800, bg=None):
    sc = look.scale
    bob = pose.bob
    body_w = int((look.round_body - 1) * 70)
    y_head = 252 + bob + pose.head_dy
    y_torso = 372 + bob + pose.torso_lean
    y_skirt = 546 + bob
    y_leg = 580 + bob
    shoulderL = (CX - 88 - body_w / 2, y_torso + 34)
    shoulderR = (CX + 88 + body_w / 2, y_torso + 34)
    L1, L2 = 62, 58
    eL, hL = _ik(shoulderL, pose.handL, L1, L2, -1)
    eR, hR = _ik(shoulderR, pose.handR, L1, L2, 1)

    parts = []
    parts.append(f'<ellipse cx="{CX}" cy="{GROUND + 10}" rx="130" ry="20" fill="#000" opacity="0.14"/>')
    parts.append(_cape(look, y_torso + 4))
    parts.append(_legs(look, pose, y_leg))
    # banner (tay trái màn hình) vẽ trước bàn tay
    if pose.prop_L == "banner":
        parts.append(_banner(hL, look))
    parts.append(_torso(look, y_torso, body_w))
    parts.append(_skirt(look, y_skirt, body_w))
    if look.belly > 0:
        bw = 92 + 40 * look.belly
        parts.append(f'<ellipse cx="{CX}" cy="{y_torso + 118}" rx="{bw}" ry="{74 + 20 * look.belly}" fill="{look.armor}" stroke="{INK}" stroke-width="8"/>')
        for k in range(-3, 4):
            yy = y_torso + 118 + k * 20
            half = bw * math.sqrt(max(0.0, 1 - ((k * 20) / (74 + 20 * look.belly)) ** 2)) - 10
            parts.append(f'<path d="M{CX - half:.1f},{yy} Q{CX},{yy + 10} {CX + half:.1f},{yy}" fill="none" stroke="{look.armor_dark}" stroke-width="4"/>')
        parts.append(f'<circle cx="{CX}" cy="{y_torso + 118}" r="11" fill="{look.trim}" stroke="{INK}" stroke-width="4"/>')
    if look.sword:
        parts.append(_katana(look, y_skirt - 6))
    # tay: tay áo + bracer
    for (S, E, H, sd) in ((shoulderL, eL, hL, -1), (shoulderR, eR, hR, 1)):
        parts.append(_stroke_limb(S, E, 36, look.sleeve))
        parts.append(_stroke_limb(E, H, 34, look.sleeve))
        mid = ((E[0] * 0.45 + H[0] * 0.55), (E[1] * 0.45 + H[1] * 0.55))
        parts.append(_stroke_limb(E, mid, 30, look.armor_dark))
    parts.append(_shoulder_plate(look, shoulderL, -1))
    parts.append(_shoulder_plate(look, shoulderR, 1))
    if pose.prop_R == "bowl":
        bx, by = (hL[0] + hR[0]) / 2, (hL[1] + hR[1]) / 2 - 6
        parts.append(f'<path d="M{bx - 40},{by - 14} H{bx + 40} Q{bx + 36},{by + 36} {bx},{by + 38} Q{bx - 36},{by + 36} {bx - 40},{by - 14} Z" fill="#3b6e8f" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
        parts.append(f'<ellipse cx="{bx}" cy="{by - 14}" rx="40" ry="9" fill="#8a5a2b" stroke="{INK}" stroke-width="5"/>')
        parts.append(f'<path d="M{bx - 12},{by - 34} q-8,-14 0,-24 M{bx + 10},{by - 34} q-8,-14 0,-24" fill="none" stroke="#9aa" stroke-width="4" stroke-linecap="round" opacity="0.8"/>')
    parts.append(_hand(hL))
    parts.append(_hand(hR))
    parts.append(_head(look, face, CX, y_head, pose.head_tilt))
    body = "".join(parts)
    bgrect = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'{bgrect}<g transform="translate({CX * (1 - sc):.1f},{GROUND * (1 - sc):.1f}) scale({sc})">{body}</g></svg>')


# ------------------------------------------------------------ tư thế & mặt
def pose_stand():
    return Pose(handL=(CX - 112, 520), handR=(CX + 100, 505), prop_R="katana_hand")


def pose_walk(phase):
    s = math.sin(phase)
    return Pose(handL=(CX - 100 - 8 * s, 520 - 30 * s), handR=(CX + 100 + 8 * s, 520 + 30 * s),
                legL=(-14 * s, max(0, 22 * s)), legR=(14 * s, max(0, -22 * s)),
                bob=-6 * abs(math.sin(phase)), head_tilt=2.5 * s)


def pose_point():
    return Pose(handL=(CX - 100, 510), handR=(CX + 210, 330), head_tilt=-4)


def pose_bow():
    return Pose(handL=(CX - 28, 505), handR=(CX + 28, 505), head_dy=52, torso_lean=24, bob=18, head_tilt=14,
                legL=(0, 0), legR=(0, 0))


def pose_banner():
    return Pose(handL=(CX - 125, 455), handR=(CX + 100, 505), prop_L="banner")


def pose_bowl():
    return Pose(handL=(CX - 40, 478), handR=(CX + 40, 478), head_tilt=3, prop_R="bowl")


def pose_cheer():
    return Pose(handL=(CX - 118, 280), handR=(CX + 118, 280), bob=-8, head_tilt=-3)


FACES = {
    "giận": Face("angry", "frown", "angry"),
    "ngạc nhiên": Face("surprised", "open", "raised", sweat=True),
    "tinh nghịch": Face("cheeky", "grin", "one", blush=True),
    "buồn ngủ": Face("sleepy", "smile", "calm"),
    "bình thản": Face("calm", "flat", "calm"),
}

NOBUNAGA = Look(kabuto=True)
HIDEYOSHI = Look(name="Hideyoshi", armor="#e0782a", armor_dark="#a04e12", trim="#f3c75c", cape="#4a3322",
                 cape_lining="#e0782a", sleeve="#3b2a1d", moustache=False, big_ears=True, whiskers=True,
                 scale=0.8, headband="#f3c75c", shoe="#c8a35a", kabuto=False)
IEYASU = Look(name="Ieyasu", armor="#2f6b46", armor_dark="#1d4430", trim="#d2a24a", cape="#2d2a22",
              cape_lining="#2f6b46", sleeve="#2a2822", moustache=False, round_body=2.0, belly=1.0,
              headband="#6b4a2c", sword=False)
