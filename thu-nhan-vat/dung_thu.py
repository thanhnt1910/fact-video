"""Bản thử: nhân vật dẫn chuyện vẽ bằng mã (SVG), ghép lên nền phẳng, chuyển động camera, phụ đề, con dấu.
Không dùng mô hình ảnh, không cần khóa nào. Chạy: python thu-nhan-vat/dung_thu.py  -> thu-nhan-vat/out/thu.mp4
Nhân vật và nền là thiết kế gốc, không sao chép nhân vật của video mẫu."""
import math, os, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from playwright.sync_api import sync_playwright

R = Path(__file__).resolve().parent
OUT = R / "out"; SP = OUT / "sprites"; BG = OUT / "bg"; FR = OUT / "frames"
for d in (SP, BG, FR): d.mkdir(parents=True, exist_ok=True)
W, H, FPS = 1280, 720, 24

INK = "#2b1d1a"; SKIN = "#f2c59c"; HAIR = "#3a2a24"; JACKET = "#2e6d73"; SCARF = "#c0392b"; SEAL = "#b3261e"

# ---------- nhân vật ----------
def eyes(kind, blink):
    L, Rr = (230, 330), (370, 330)
    if blink or kind == "half":
        return "".join(f'<path d="M{x-24} {y} q24 14 48 0" stroke="{INK}" stroke-width="7" fill="none" stroke-linecap="round"/>' for x, y in (L, Rr))
    if kind == "wide":
        return "".join(f'<circle cx="{x}" cy="{y}" r="26" fill="#fff" stroke="{INK}" stroke-width="5"/><circle cx="{x}" cy="{y}" r="8" fill="{INK}"/>' for x, y in (L, Rr))
    if kind == "up":
        return "".join(f'<circle cx="{x}" cy="{y}" r="22" fill="#fff" stroke="{INK}" stroke-width="5"/><circle cx="{x+4}" cy="{y-9}" r="9" fill="{INK}"/>' for x, y in (L, Rr))
    return "".join(f'<circle cx="{x}" cy="{y}" r="22" fill="#fff" stroke="{INK}" stroke-width="5"/><circle cx="{x}" cy="{y}" r="9" fill="{INK}"/>' for x, y in (L, Rr))

def brows(kind):
    s = f'stroke="{INK}" stroke-width="9" stroke-linecap="round" fill="none"'
    if kind == "up":
        return f'<path d="M198 280 q32 -22 64 -4" {s}/><path d="M338 276 q32 -18 64 4" {s}/>'
    if kind == "worry":
        return f'<path d="M198 292 L262 268" {s}/><path d="M338 268 L402 292" {s}/>'
    if kind == "sus":
        return f'<path d="M198 286 L262 292" {s}/><path d="M338 270 q32 -16 64 -2" {s}/>'
    return f'<path d="M198 282 q32 -10 64 0" {s}/><path d="M338 282 q32 -10 64 0" {s}/>'

def mouth(kind):
    s = f'stroke="{INK}" stroke-width="8" stroke-linecap="round" fill="none"'
    if kind == "o":
        return f'<ellipse cx="300" cy="424" rx="22" ry="28" fill="#7a2e2e" stroke="{INK}" stroke-width="6"/>'
    if kind == "smile":
        return f'<path d="M258 410 q42 44 84 0" {s}/>'
    if kind == "wave":
        return f'<path d="M258 428 q14 -16 28 0 t28 0 t28 0" {s}/>'
    if kind == "flat":
        return f'<path d="M262 424 L340 414" {s}/>'
    return f'<path d="M270 420 q30 12 60 0" {s}/>'

def arm_down():
    return (f'<path d="M150 560 q-60 70 -40 190" stroke="{INK}" stroke-width="6" fill="{JACKET}"/>'
            f'<path d="M450 560 q60 70 40 190" stroke="{INK}" stroke-width="6" fill="{JACKET}"/>'
            f'<circle cx="104" cy="760" r="30" fill="{SKIN}" stroke="{INK}" stroke-width="6"/>'
            f'<circle cx="496" cy="760" r="30" fill="{SKIN}" stroke="{INK}" stroke-width="6"/>')

def arm_point():
    return (f'<path d="M150 560 q-60 70 -40 190" stroke="{INK}" stroke-width="6" fill="{JACKET}"/>'
            f'<circle cx="104" cy="760" r="30" fill="{SKIN}" stroke="{INK}" stroke-width="6"/>'
            f'<path d="M450 560 L660 470 L690 520 L480 620 Z" stroke="{INK}" stroke-width="6" fill="{JACKET}" stroke-linejoin="round"/>'
            f'<path d="M680 470 L760 450 L772 478 L694 510 Z" stroke="{INK}" stroke-width="6" fill="{SKIN}" stroke-linejoin="round"/>')

def arm_think():
    return (f'<path d="M150 560 q-60 70 -40 190" stroke="{INK}" stroke-width="6" fill="{JACKET}"/>'
            f'<circle cx="104" cy="760" r="30" fill="{SKIN}" stroke="{INK}" stroke-width="6"/>')

def front_think():
    return (f'<path d="M462 650 L372 520" stroke="{INK}" stroke-width="66" stroke-linecap="round"/>'
            f'<path d="M462 650 L372 520" stroke="{JACKET}" stroke-width="54" stroke-linecap="round"/>'
            f'<circle cx="352" cy="478" r="32" fill="{SKIN}" stroke="{INK}" stroke-width="6"/>')

def char_svg(eye, brow, mou, arm, blink=False, sweat=False, front=''):
    body = (f'<path d="M130 800 L130 600 Q130 520 230 506 L370 506 Q470 520 470 600 L470 800 Z" fill="{JACKET}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
            f'<path d="M222 506 L300 590 L378 506" fill="none" stroke="{INK}" stroke-width="6"/>'
            f'<rect x="240" y="470" width="120" height="50" rx="22" fill="{SCARF}" stroke="{INK}" stroke-width="6"/>'
            f'<path d="M330 510 q10 60 -4 100 l40 -6 q4 -52 -16 -98 Z" fill="{SCARF}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
    head = (f'<circle cx="300" cy="350" r="160" fill="{SKIN}" stroke="{INK}" stroke-width="7"/>'
            f'<path d="M140 330 Q130 170 300 170 Q470 170 460 330 Q420 250 350 236 Q300 262 240 238 Q170 252 140 330 Z" fill="{HAIR}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
            f'<path d="M270 176 Q236 112 300 92 Q282 132 326 176 Z" fill="{HAIR}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
            f'<circle cx="150" cy="370" r="22" fill="{SKIN}" stroke="{INK}" stroke-width="6"/><circle cx="450" cy="370" r="22" fill="{SKIN}" stroke="{INK}" stroke-width="6"/>')
    glasses = (f'<circle cx="230" cy="330" r="44" fill="none" stroke="{INK}" stroke-width="6"/><circle cx="370" cy="330" r="44" fill="none" stroke="{INK}" stroke-width="6"/>'
               f'<path d="M274 330 L326 330" stroke="{INK}" stroke-width="6"/>')
    extra = f'<path d="M462 250 q22 40 0 56 q-22 -16 0 -56 Z" fill="#8fd3f4" stroke="{INK}" stroke-width="4"/>' if sweat else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="900" height="820" viewBox="-40 0 900 820">'
            f'{arm}{body}{head}{eyes(eye, blink)}{brows(brow)}{glasses}{mouth(mou)}{extra}{front}</svg>')

EXPR = {
    "neutral":  ("dot",  "flat0", "small", arm_down, False),
    "surprise": ("wide", "up",    "o",     arm_down, False),
    "suspect":  ("half", "sus",   "flat",  arm_down, False),
    "scared":   ("wide", "worry", "wave",  arm_down, True),
    "point":    ("dot",  "up",    "smile", arm_point, False),
    "think":    ("up",   "sus",   "small", arm_think, False),
}

# ---------- nền (phẳng, gam đất) ----------
def svg(body, defs=""):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><defs>{defs}</defs>{body}</svg>'

def bg_tomb():
    blocks = "".join(f'<rect x="{x}" y="{y}" width="150" height="70" fill="{c}" stroke="#4a3a2c" stroke-width="3"/>'
                     for y in range(0, 720, 70) for x in range(-(y // 70 % 2) * 75, 1300, 150) for c in ["#8a7355" if (x // 150 + y // 70) % 3 else "#9a8363"])
    return svg(f'<rect width="{W}" height="{H}" fill="#6e5a42"/>{blocks}'
               f'<path d="M430 720 L430 260 Q640 90 850 260 L850 720 Z" fill="url(#g)"/>'
               f'<path d="M430 720 L430 260 Q640 90 850 260 L850 720" fill="none" stroke="#3a2c20" stroke-width="10"/>'
               f'<rect x="150" y="300" width="14" height="120" fill="#3a2c20"/><path d="M157 300 q-34 -50 0 -100 q34 50 0 100 Z" fill="#ffb347" stroke="#c0581f" stroke-width="5"/>'
               f'<rect y="600" width="{W}" height="120" fill="#4e3f2e" opacity="0.55"/>',
               '<radialGradient id="g" cx="50%" cy="40%" r="70%"><stop offset="0" stop-color="#ffe9a8"/><stop offset="1" stop-color="#d28a2e"/></radialGradient>')

def bg_desert():
    return svg(f'<rect width="{W}" height="{H}" fill="url(#s)"/><circle cx="1020" cy="190" r="86" fill="#ffd27a" opacity="0.95"/>'
               f'<path d="M420 470 L620 190 L820 470 Z" fill="#d9a35d" stroke="#8a5a28" stroke-width="5" stroke-linejoin="round"/>'
               f'<path d="M620 190 L820 470 L700 470 Z" fill="#b9823e"/>'
               f'<path d="M0 470 Q300 400 640 470 T1280 450 L1280 720 L0 720 Z" fill="#e8b873"/>'
               f'<path d="M0 560 Q320 500 700 570 T1280 540 L1280 720 L0 720 Z" fill="#d49d55"/>',
               '<linearGradient id="s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f6a56b"/><stop offset="1" stop-color="#fbe3b0"/></linearGradient>')

def bg_map():
    return svg(f'<rect width="{W}" height="{H}" fill="#5b4330"/><rect y="520" width="{W}" height="200" fill="#6e5039"/>'
               f'<rect x="170" y="110" width="940" height="520" rx="14" fill="#e9d7a6" stroke="#8a6b3a" stroke-width="8"/>'
               f'<path d="M260 480 Q330 300 470 330 Q560 220 700 300 Q860 250 950 380 Q900 540 700 520 Q520 580 260 480 Z" fill="#b9c78a" stroke="#6f7f45" stroke-width="5"/>'
               f'<path d="M300 560 Q520 600 760 560" fill="none" stroke="#5aa0c8" stroke-width="12" stroke-linecap="round"/>'
               f'<path d="M380 430 Q560 330 840 400" fill="none" stroke="{SEAL}" stroke-width="9" stroke-dasharray="26 18" stroke-linecap="round"/>'
               f'<path d="M820 372 L868 404 L812 424 Z" fill="{SEAL}"/><circle cx="380" cy="430" r="14" fill="{SEAL}"/>'
               f'<rect x="1080" y="140" width="16" height="90" fill="#3a2c20"/><path d="M1088 140 q-26 -40 0 -80 q26 40 0 80 Z" fill="#ffb347" stroke="#c0581f" stroke-width="4"/>')

def bg_hoard():
    coins = "".join(f'<circle cx="{40 + (i * 97) % 1200}" cy="{600 + (i * 53) % 110}" r="{26 + (i % 4) * 6}" fill="#f2c230" stroke="#a87b14" stroke-width="4"/>' for i in range(46))
    return svg(f'<rect width="{W}" height="{H}" fill="#2a2018"/><rect width="{W}" height="{H}" fill="url(#r)"/>{coins}'
               f'<path d="M200 600 Q300 470 420 600 Z" fill="#e9b823" stroke="#a87b14" stroke-width="5"/><path d="M820 600 Q940 440 1070 600 Z" fill="#e9b823" stroke="#a87b14" stroke-width="5"/>',
               '<radialGradient id="r" cx="50%" cy="85%" r="75%"><stop offset="0" stop-color="#ffd86b" stop-opacity="0.85"/><stop offset="1" stop-color="#2a2018" stop-opacity="0"/></radialGradient>')

def bg_museum():
    return svg(f'<rect width="{W}" height="{H}" fill="#cfd6d8"/><rect y="540" width="{W}" height="180" fill="#9aa5a8"/>'
               f'<rect x="470" y="520" width="340" height="200" fill="#e7ecee" stroke="#6b787c" stroke-width="6"/>'
               f'<rect x="500" y="170" width="280" height="350" rx="12" fill="#bfe3ef" opacity="0.55" stroke="#6b787c" stroke-width="6"/>'
               f'<path d="M570 480 L590 250 Q640 190 690 250 L710 480 Z" fill="#e8b72a" stroke="#8a6410" stroke-width="6"/>'
               f'<path d="M588 270 L692 270 M586 320 L694 320 M586 370 L694 370" stroke="#2f5da8" stroke-width="12"/>'
               f'<ellipse cx="640" cy="236" rx="44" ry="26" fill="#e8b72a" stroke="#8a6410" stroke-width="5"/>'
               f'<circle cx="622" cy="300" r="7" fill="{INK}"/><circle cx="658" cy="300" r="7" fill="{INK}"/><path d="M628 340 q12 8 24 0" stroke="{INK}" stroke-width="5" fill="none"/>'
               f'<path d="M220 80 L420 80 L380 150 L260 150 Z" fill="#fff6cf" opacity="0.7"/>')

def bg_night():
    stars = "".join(f'<circle cx="{(i * 173) % 1280}" cy="{(i * 71) % 330}" r="{2 + i % 3}" fill="#fff6d8"/>' for i in range(60))
    return svg(f'<rect width="{W}" height="{H}" fill="url(#n)"/>{stars}<circle cx="1050" cy="130" r="56" fill="#f6efd2"/>'
               f'<path d="M0 520 Q320 450 640 520 T1280 500 L1280 720 L0 720 Z" fill="#3b3a46"/>'
               f'<path d="M180 560 L320 360 L460 560 Z" fill="#7b6a58" stroke="#3a2c20" stroke-width="6" stroke-linejoin="round"/><path d="M320 360 L360 560 L320 560 Z" fill="#5b4c3d"/>'
               f'<path d="M900 640 q-34 -60 0 -120 q34 60 0 120 Z" fill="#ffb347" stroke="#c0581f" stroke-width="5"/><path d="M850 650 L950 650" stroke="#3a2c20" stroke-width="12" stroke-linecap="round"/>'
               f'<rect y="640" width="{W}" height="80" fill="#2b2a34"/>',
               '<linearGradient id="n" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1b2347"/><stop offset="1" stop-color="#3f4577"/></linearGradient>')

BGS = {"tomb": bg_tomb, "desert": bg_desert, "map": bg_map, "hoard": bg_hoard, "museum": bg_museum, "night": bg_night}

def render_assets():
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 900, "height": 820})
        for name, (e, br, m, arm, sw) in EXPR.items():
            for blink in (False, True):
                pg.set_content(f'<body style="margin:0;background:transparent">{char_svg(e, br, m, arm(), blink, sw, front_think() if name == 'think' else '')}</body>')
                pg.screenshot(path=str(SP / f"{name}{'_b' if blink else ''}.png"), omit_background=True)
        pg2 = b.new_page(viewport={"width": W, "height": H})
        for name, fn in BGS.items():
            pg2.set_content(f'<body style="margin:0">{fn()}</body>'); pg2.screenshot(path=str(BG / f"{name}.png"))
        b.close()

# ---------- ghép ----------
def font(size):
    f = subprocess.run(["fc-match", "-f", "%{file}", "Inter:bold"], capture_output=True, text=True).stdout
    return ImageFont.truetype(f, size)

def caption(img, text):
    d = ImageDraw.Draw(img, "RGBA"); f = font(34)
    tw = d.textlength(text, font=f); bw = tw + 70; x0 = (W - bw) / 2; y0 = H - 110
    d.rounded_rectangle([x0, y0, x0 + bw, y0 + 66], 33, fill=(255, 255, 255, 235))
    d.text((W / 2, y0 + 33), text, font=f, fill=(34, 24, 20, 255), anchor="mm")

def stamp(img, t):
    s = min(1, t / 0.25); ease = 1 + 0.35 * (1 - s) ** 2 if s < 1 else 1
    layer = Image.new("RGBA", (460, 170), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    d.rounded_rectangle([6, 6, 454, 164], 14, outline=SEAL, width=8)
    d.text((230, 52), "MỨC ĐỘ CHẮC CHẮN", font=font(32), fill=SEAL, anchor="mm")
    d.text((230, 120), "VỪA", font=font(64), fill=SEAL, anchor="mm")
    layer = layer.rotate(-6, expand=True, resample=Image.BICUBIC)
    layer = layer.resize((int(layer.width * ease), int(layer.height * ease)))
    layer.putalpha(layer.getchannel("A").point(lambda v: int(v * min(1, t / 0.12))))
    img.alpha_composite(layer, (W - layer.width - 70, 70))

# (nền, nhân vật, biểu cảm, vị trí x, y, cỡ, chữ, con dấu)
SHOTS = [
    ("tomb",   True,  "neutral",  0.30, 0.98, 0.52, "Cánh cửa đá mở ra.", False),
    ("tomb",   True,  "surprise", 0.50, 1.18, 1.05, "Người đầu tiên bước vào đã sững lại.", False),
    ("desert", True,  "scared",   0.72, 1.00, 0.62, "Rồi những cái chết bắt đầu được kể lại.", False),
    ("map",    True,  "point",    0.32, 1.02, 0.80, "Nhưng hãy xem bằng chứng nói gì.", False),
    ("museum", False, None,       0,    0,    0,    "Một chiếc mặt nạ vàng, nhìn từ rất gần.", False),
    ("night",  True,  "suspect",  0.62, 1.00, 0.78, "Lời nguyền có thật là nguyên nhân?", False),
    ("hoard",  True,  "think",    0.50, 1.02, 0.80, "Điều chắc chắn nằm ở đây.", True),
    ("desert", True,  "point",    0.36, 1.02, 0.80, "Còn bạn, sẽ chấm mức nào?", False),
]
SHOT_SEC = 3.0

def frame(shot, t, k, bgs, sprites):
    bgn, has, ex, cx, cy, sc, text, st = shot
    prog = t / SHOT_SEC
    z = 1.0 + 0.07 * prog
    base = bgs[bgn]; bw, bh = int(W * z), int(H * z)
    bgimg = base.resize((bw, bh), Image.BILINEAR)
    ox = int((bw - W) * (0.5 + 0.3 * (prog - 0.5))); oy = int((bh - H) * 0.5)
    img = bgimg.crop((ox, oy, ox + W, oy + H)).convert("RGBA")
    if has:
        blink = ex and ((t * 24) % (24 * 2.4) < 3 or abs(t - 1.6) < 0.08)
        spr = sprites[ex + ("_b" if blink else "")]
        s = sc * z * 0.92; w = int(spr.width * s); h = int(spr.height * s)
        spr = spr.resize((w, h), Image.BILINEAR)
        bob = math.sin(t * 3.2) * 6
        px = int(cx * W - w * 0.36 + (0.5 - prog) * 26); py = int(cy * H - h + bob)
        sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).ellipse([px + w * 0.2, py + h - 18, px + w * 0.75, py + h + 18], fill=(0, 0, 0, 70))
        img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)))
        img.alpha_composite(spr, (px, py))
    caption(img, text)
    if st and t > 1.0: stamp(img, t - 1.0)
    if t < 0.12:
        img = Image.blend(Image.new("RGBA", (W, H), (0, 0, 0, 255)), img, t / 0.12)
    return img.convert("RGB")

def main():
    render_assets()
    bgs = {n: Image.open(BG / f"{n}.png").convert("RGB") for n in BGS}
    sprites = {p.stem: Image.open(p).convert("RGBA") for p in SP.glob("*.png")}
    for f in FR.glob("*.jpg"): f.unlink()
    n = 0
    for shot in SHOTS:
        for i in range(int(SHOT_SEC * FPS)):
            frame(shot, i / FPS, i, bgs, sprites).save(FR / f"{n:05d}.jpg", quality=92); n += 1
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS), "-i", str(FR / "%05d.jpg"), "-c:v", "libx264", "-preset", "veryfast",
                    "-crf", "20", "-pix_fmt", "yuv420p", str(OUT / "thu.mp4")], check=True)
    print("xong", n, "khung ->", OUT / "thu.mp4")

if __name__ == "__main__":
    main()
