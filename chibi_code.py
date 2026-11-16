"""Chibi vẽ bằng mã (SVG): nhân vật dựng sẵn, mặt luôn giống nhau. Thử cảnh 004 (bánh gạo) của NB1.
  python chibi_code.py  -> assets/anh_2d/NB1_code/004.png (1344x768)"""
from pathlib import Path

SKIN = "#ffd9b3"; OUT = "#2b1d1a"


def eyes(kind, cx, cy):
    if kind == "angry":
        return (f'<path d="M{cx-42} {cy-16} L{cx-12} {cy-4}" stroke="{OUT}" stroke-width="7" stroke-linecap="round"/>'
                f'<path d="M{cx+42} {cy-16} L{cx+12} {cy-4}" stroke="{OUT}" stroke-width="7" stroke-linecap="round"/>'
                f'<ellipse cx="{cx-24}" cy="{cy+8}" rx="9" ry="10" fill="{OUT}"/><ellipse cx="{cx+24}" cy="{cy+8}" rx="9" ry="10" fill="{OUT}"/>'
                f'<circle cx="{cx-21}" cy="{cy+4}" r="3" fill="#fff"/><circle cx="{cx+27}" cy="{cy+4}" r="3" fill="#fff"/>')
    if kind == "happy":
        return (f'<path d="M{cx-36} {cy+8} Q{cx-24} {cy-14} {cx-10} {cy+8}" stroke="{OUT}" stroke-width="7" fill="none" stroke-linecap="round"/>'
                f'<path d="M{cx+10} {cy+8} Q{cx+24} {cy-14} {cx+36} {cy+8}" stroke="{OUT}" stroke-width="7" fill="none" stroke-linecap="round"/>')
    if kind == "sleepy":
        return (f'<path d="M{cx-36} {cy+2} Q{cx-23} {cy+14} {cx-10} {cy+2}" stroke="{OUT}" stroke-width="6" fill="none" stroke-linecap="round"/>'
                f'<path d="M{cx+10} {cy+2} Q{cx+23} {cy+14} {cx+36} {cy+2}" stroke="{OUT}" stroke-width="6" fill="none" stroke-linecap="round"/>')
    if kind == "cheeky":
        return (f'<ellipse cx="{cx-22}" cy="{cy+4}" rx="10" ry="13" fill="#fff" stroke="{OUT}" stroke-width="4"/><ellipse cx="{cx+22}" cy="{cy+4}" rx="10" ry="13" fill="#fff" stroke="{OUT}" stroke-width="4"/>'
                f'<circle cx="{cx-19}" cy="{cy+6}" r="6" fill="{OUT}"/><circle cx="{cx+25}" cy="{cy+6}" r="6" fill="{OUT}"/>')
    return ""


def mouth(kind, cx, cy):
    if kind == "grit":   # nghiến răng
        return (f'<rect x="{cx-22}" y="{cy}" width="44" height="18" rx="6" fill="#fff" stroke="{OUT}" stroke-width="5"/>'
                f'<path d="M{cx-11} {cy} V{cy+18} M{cx} {cy} V{cy+18} M{cx+11} {cy} V{cy+18}" stroke="{OUT}" stroke-width="3"/>')
    if kind == "grin":
        return f'<path d="M{cx-34} {cy} Q{cx} {cy+44} {cx+34} {cy} Z" fill="#8a2b2b" stroke="{OUT}" stroke-width="5" stroke-linejoin="round"/><path d="M{cx-18} {cy+14} Q{cx} {cy+30} {cx+18} {cy+14} Q{cx} {cy+22} {cx-18} {cy+14}Z" fill="#ff8a8a"/>'
    if kind == "munch":
        return f'<ellipse cx="{cx}" cy="{cy+8}" rx="20" ry="15" fill="#8a2b2b" stroke="{OUT}" stroke-width="5"/>'
    return f'<path d="M{cx-14} {cy} Q{cx} {cy+10} {cx+14} {cy}" stroke="{OUT}" stroke-width="5" fill="none" stroke-linecap="round"/>'


def chibi(x, y, s, name, eye, mou, coat, hair="#1b1b22", extra="", arms="down", sweat=False, cheeks=True):
    g = [f'<g transform="translate({x},{y}) scale({s})">']
    g.append('<ellipse cx="0" cy="168" rx="70" ry="12" fill="#00000030"/>')            # bóng dưới chân
    # chân + dép
    g.append(f'<rect x="-34" y="130" width="26" height="34" rx="10" fill="{SKIN}"/><rect x="8" y="130" width="26" height="34" rx="10" fill="{SKIN}"/>')
    g.append('<ellipse cx="-22" cy="166" rx="24" ry="10" fill="#7a4a24"/><ellipse cx="22" cy="166" rx="24" ry="10" fill="#7a4a24"/>')
    # thân
    g.append(f'<path d="M-52 70 Q-60 140 -44 150 L44 150 Q60 140 52 70 Z" fill="{coat}" stroke="{OUT}" stroke-width="5"/>')
    g.append(f'<rect x="-48" y="108" width="96" height="14" fill="#3a2a22"/>')
    g.append(extra if name == "back" else "")
    # đầu
    g.append(f'<circle cx="0" cy="0" r="88" fill="{SKIN}" stroke="{OUT}" stroke-width="6"/>')
    g.append(extra if name != "back" else "")
    g.append(eyes(eye, 0, -4)); g.append(mouth(mou, 0, 38))
    if cheeks:
        g.append('<ellipse cx="-58" cy="26" rx="14" ry="9" fill="#ff9a9a" opacity=".7"/><ellipse cx="58" cy="26" rx="14" ry="9" fill="#ff9a9a" opacity=".7"/>')
    if sweat:
        g.append('<path d="M92 -50 Q108 -20 92 -8 Q76 -20 92 -50Z" fill="#8fd3ff" stroke="#2b6a99" stroke-width="3"/>')
    g.append('</g>')
    return "".join(g)


def topknot(col="#1b1b22", high=False):
    h = -150 if high else -128
    return (f'<path d="M-86 -20 Q-90 -86 0 -92 Q90 -86 86 -20 Q70 -62 0 -66 Q-70 -62 -86 -20Z" fill="{col}" stroke="{OUT}" stroke-width="5"/>'
            f'<path d="M-10 -88 Q-30 {h} 6 {h-18} Q40 {h} 14 -88Z" fill="{col}" stroke="{OUT}" stroke-width="5"/>')


def scene_rice():
    W, H = 1344, 768
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    # nền phòng: vách giấy + cửa mở ra vườn
    s.append(f'<rect width="{W}" height="{H}" fill="#f6ead2"/>')
    s.append('<rect x="380" y="60" width="584" height="380" fill="#bfe3a8"/><rect x="380" y="260" width="584" height="180" fill="#8fc67a"/>')
    s.append('<circle cx="560" cy="170" r="70" fill="#dff1c2"/><path d="M820 110 Q800 70 830 40 Q860 70 840 110Z" fill="#2f6b3a"/><rect x="826" y="110" width="8" height="150" fill="#5a3b22"/>')
    s.append('<path d="M420 300 Q470 200 520 300Z" fill="#3b7a47"/><path d="M880 300 Q930 190 980 300Z" fill="#3b7a47"/>')
    for i in range(0, 380, 76):
        s.append(f'<rect x="{0}" y="{60+i}" width="{380}" height="0" />')
    s.append('<rect x="0" y="40" width="380" height="410" fill="#fff8e6" stroke="#8a6a44" stroke-width="8"/><rect x="964" y="40" width="380" height="410" fill="#fff8e6" stroke="#8a6a44" stroke-width="8"/>')
    for x0 in (0, 964):
        for k in range(1, 4):
            s.append(f'<line x1="{x0+k*95}" y1="40" x2="{x0+k*95}" y2="450" stroke="#8a6a44" stroke-width="5"/>')
        for k in range(1, 4):
            s.append(f'<line x1="{x0}" y1="{40+k*103}" x2="{x0+380}" y2="{40+k*103}" stroke="#8a6a44" stroke-width="5"/>')
    s.append('<rect x="0" y="40" width="1344" height="26" fill="#6b4426"/>')
    # sàn tatami
    s.append('<rect x="0" y="450" width="1344" height="318" fill="#d9c27a"/>')
    for i in range(0, 1344, 224):
        s.append(f'<line x1="{i}" y1="450" x2="{i-60}" y2="768" stroke="#a8914f" stroke-width="5"/>')
    s.append('<line x1="0" y1="600" x2="1344" y2="600" stroke="#a8914f" stroke-width="5"/>')
    # bàn thấp + bánh gạo khổng lồ
    s.append('<rect x="330" y="470" width="684" height="46" rx="14" fill="#7a4a24" stroke="#2b1d1a" stroke-width="6"/><rect x="370" y="516" width="30" height="120" fill="#5a3418"/><rect x="944" y="516" width="30" height="120" fill="#5a3418"/>')
    s.append('<ellipse cx="672" cy="440" rx="190" ry="78" fill="#ffffff" stroke="#2b1d1a" stroke-width="6"/><ellipse cx="640" cy="410" rx="90" ry="24" fill="#f1f1f1"/>')
    # nhân vật
    N = chibi(300, 330, 1.0, "n", "angry", "grit", "#c8281e", extra=topknot(high=True) + '<path d="M-60 12 Q0 4 60 12" stroke="#1b1b22" stroke-width="5" fill="none"/>', sweat=True, cheeks=False)
    # áo choàng + búa
    N += '<path d="M240 400 Q220 470 250 500 L290 470Z" fill="#8f1a14" stroke="#2b1d1a" stroke-width="5"/>'
    mallet = ('<g transform="translate(430,300) rotate(25)"><rect x="-12" y="-20" width="24" height="220" rx="8" fill="#8a5a2b" stroke="#2b1d1a" stroke-width="5"/>'
              '<rect x="-52" y="-80" width="104" height="70" rx="16" fill="#a8743a" stroke="#2b1d1a" stroke-width="6"/></g>')
    arm_n = f'<circle cx="408" cy="470" r="26" fill="{SKIN}" stroke="{OUT}" stroke-width="5"/>'
    Hh = chibi(672, 470, 0.78, "h", "cheeky", "grin", "#ff8a1f", extra=topknot() + '<path d="M-92 -10 Q-118 -6 -112 24 Q-96 30 -88 14Z" fill="#ffd9b3" stroke="#2b1d1a" stroke-width="5"/><path d="M92 -10 Q118 -6 112 24 Q96 30 88 14Z" fill="#ffd9b3" stroke="#2b1d1a" stroke-width="5"/><path d="M-24 62 L-30 82 M0 66 L0 86 M24 62 L30 82" stroke="#1b1b22" stroke-width="4"/>')
    arm_h = f'<circle cx="610" cy="470" r="22" fill="{SKIN}" stroke="{OUT}" stroke-width="5"/><circle cx="738" cy="470" r="22" fill="{SKIN}" stroke="{OUT}" stroke-width="5"/>'
    Ii = chibi(1040, 400, 1.12, "i", "happy", "munch", "#4a8a52", extra=topknot() + '', cheeks=True)
    # Ieyasu tròn bụng + đũa + miếng bánh
    Ii += '<ellipse cx="1040" cy="520" rx="80" ry="52" fill="#4a8a52" stroke="#2b1d1a" stroke-width="5" opacity=".0"/>'
    chop = ('<g transform="translate(985,440) rotate(-30)"><rect x="0" y="0" width="150" height="9" rx="4" fill="#d8b070" stroke="#2b1d1a" stroke-width="3"/>'
            '<rect x="0" y="22" width="150" height="9" rx="4" fill="#d8b070" stroke="#2b1d1a" stroke-width="3"/></g>')
    piece = '<ellipse cx="960" cy="412" rx="34" ry="24" fill="#fff" stroke="#2b1d1a" stroke-width="5"/>'
    # hiệu ứng: nét rung, bột bay
    fx = ('<g stroke="#2b1d1a" stroke-width="7" stroke-linecap="round"><path d="M478 340 l30 -34 M508 360 l44 -20 M470 372 l-22 -30"/></g>'
          '<g fill="#fff" stroke="#2b1d1a" stroke-width="3"><circle cx="560" cy="360" r="9"/><circle cx="600" cy="332" r="6"/><circle cx="700" cy="340" r="8"/></g>')
    s += [N, mallet, arm_n, Hh, arm_h, Ii, chop, piece, fx, '</svg>']
    return "\n".join(s)


if __name__ == "__main__":
    out = Path("assets/anh_2d/NB1_code"); out.mkdir(parents=True, exist_ok=True)
    (out / "004.svg").write_text(scene_rice(), encoding="utf-8")
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1344, "height": 768})
        pg.goto("file://" + str((out / "004.svg").resolve())); pg.screenshot(path=str(out / "004.png")); b.close()
    print("xong", out / "004.png")
