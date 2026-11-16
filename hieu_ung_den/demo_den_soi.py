"""Demo 15 giây: hiệu ứng "đèn soi sử" trên bản đồ (Okehazama, vùng Owari).
Đèn sáng tới đâu thì sử biết tới đó; chỗ tối là chỗ chưa ai biết.
Dữ liệu đất: Natural Earth 10m (phạm vi công cộng). Vị trí các điểm chỉ là minh họa.
Chạy: python demo_den_soi.py <land.geojson> <ra.mp4>
"""
import sys, json, math, subprocess, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS, DUR = 1920, 1080, 24, 15.0
LAT0, LAT1 = 34.52, 35.32
KY = H / (LAT1 - LAT0)
KX = KY * math.cos(math.radians(35.1))
LON0 = 136.05
HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, '..', 'assets', 'bia', 'fonts')
LOGO = os.path.join(HERE, '..', 'assets', 'logo', 'nguoi-gac-su.png')
rng = np.random.default_rng(7)

def P(lon, lat):
    return ((lon - LON0) * KX, (LAT1 - lat) * KY)

def fbm(w, h, octv=5, base=4):
    out = np.zeros((h, w), np.float32); amp = 1; tot = 0
    for o in range(octv):
        n = base * 2 ** o
        g = rng.random((int(n * h / w) + 2, n + 2)).astype(np.float32)
        im = Image.fromarray((g * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
        out += np.asarray(im, np.float32) / 255 * amp; tot += amp; amp *= 0.5
    return out / tot

def chaikin(pts, n=3):
    for _ in range(n):
        out = []
        m = len(pts)
        for i in range(m):
            a = pts[i]; b = pts[(i + 1) % m]
            out.append((0.75 * a[0] + 0.25 * b[0], 0.75 * a[1] + 0.25 * b[1]))
            out.append((0.25 * a[0] + 0.75 * b[0], 0.25 * a[1] + 0.75 * b[1]))
        pts = out
    return pts

def build_map(land_path):
    S = 2
    land = Image.new('L', (W * S, H * S), 0); d = ImageDraw.Draw(land)
    J = json.load(open(land_path))
    lon1 = LON0 + W / KX
    for f in J['features']:
        g = f['geometry']
        polys = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
        for poly in polys:
            ext = poly[0]
            xs = [p[0] for p in ext]; ys = [p[1] for p in ext]
            if max(xs) < LON0 or min(xs) > lon1 or max(ys) < LAT0 or min(ys) > LAT1: continue
            d.polygon(chaikin([(P(*p)[0] * S, P(*p)[1] * S) for p in ext]), fill=255)
            for h in poly[1:]:
                d.polygon(chaikin([(P(*p)[0] * S, P(*p)[1] * S) for p in h]), fill=0)
    land = land.resize((W, H), Image.LANCZOS)
    L = np.asarray(land, np.float32) / 255
    n1 = fbm(W, H, 6, 5); n2 = fbm(W, H, 4, 40)
    # đất: giấy dó có vân + sắc đồi nhẹ
    paper = np.stack([188, 160, 112], -1).astype(np.float32)
    gy, gx = np.gradient(n1 * 1.0)
    shade = np.clip(1 + (gx - gy) * 90, 0.7, 1.3)
    inland = np.asarray(land.filter(ImageFilter.GaussianBlur(70)), np.float32) / 255
    tint = np.stack([150, 148, 96], -1).astype(np.float32)[None, None, :]
    pap = paper[None, None, :] * (1 - 0.35 * np.clip(n1 - 0.45, 0, 1)[..., None] * 2) + tint * (0.35 * np.clip(n1 - 0.45, 0, 1)[..., None] * 2)
    land_rgb = paper[None, None, :] * (0.93 + 0.10 * n1[..., None]) * (0.985 + 0.03 * n2[..., None])
    # biển: xanh đậm, sáng hơn gần bờ
    near = np.asarray(land.filter(ImageFilter.GaussianBlur(26)), np.float32) / 255
    sea_rgb = np.stack([52, 96, 120], -1).astype(np.float32)[None, None, :] * (0.78 + 0.45 * near[..., None]) * (0.97 + 0.06 * n1[..., None])
    sea_rgb = sea_rgb + np.stack([14, 26, 30], -1)[None, None, :] * near[..., None]
    img = land_rgb * L[..., None] + sea_rgb * (1 - L[..., None])
    # nét bờ
    edge = np.asarray(land.filter(ImageFilter.GaussianBlur(2.2)), np.float32) / 255
    rim = np.clip(1 - np.abs(edge - 0.5) * 2.2, 0, 1) ** 2
    img = img * (1 - 0.8 * rim[..., None])
    return np.clip(img, 0, 255).astype(np.float32), L

def font(name, size): return ImageFont.truetype(os.path.join(FONT, name), size)

# ---- điểm minh họa
PTS = {
    'Kiyosu': (136.843, 35.208),
    'Atsuta': (136.908, 35.128),
    'Oke': (136.965, 35.070),
}
UNC_R_KM = 5.5

def km_to_px(km):  # theo kinh độ
    return km / 111.0 * KY

def ease(t): t = max(0, min(1, t)); return t * t * (3 - 2 * t)

def lamp_state(t):
    """trả về (x,y,R,cường độ) của đèn"""
    kx, ky = P(*PTS['Kiyosu']); ax, ay = P(*PTS['Atsuta']); ox, oy = P(*PTS['Oke'])
    if t < 1.6: x, y = kx, ky
    elif t < 4.6: x, y = kx, ky
    elif t < 7.6:
        u = ease((t - 4.6) / 3.0)
        # đi qua Atsuta rồi tới gần Okehazama
        if u < 0.5: v = ease(u / 0.5); x, y = kx + (ax - kx) * v, ky + (ay - ky) * v
        else: v = ease((u - 0.5) / 0.5); x, y = ax + (ox - ax) * v * 0.6, ay + (oy - ay) * v * 0.6
    elif t < 10.0:
        x, y = P(PTS['Atsuta'][0] + (PTS['Oke'][0] - PTS['Atsuta'][0]) * 0.6, PTS['Atsuta'][1] + (PTS['Oke'][1] - PTS['Atsuta'][1]) * 0.6)
    else: x, y = P(PTS['Atsuta'][0] + (PTS['Oke'][0] - PTS['Atsuta'][0]) * 0.6, PTS['Atsuta'][1] + (PTS['Oke'][1] - PTS['Atsuta'][1]) * 0.6)
    R = 400.0; inten = 1.0
    if t < 1.6: inten = ease((t - 0.7) / 0.9)
    if 10.0 <= t < 13.2:  # đèn yếu dần, chập chờn: sử không biết chắc
        u = (t - 10.0) / 3.2
        inten = 1 - 0.55 * ease(u)
        R = 400 - 150 * ease(u)
    if t >= 13.2:
        u = ease((t - 13.2) / 1.4)
        inten = 0.45 + 0.55 * u; R = 250 + 800 * u
    # chập chờn
    fl = 1 + 0.035 * math.sin(t * 17.0) + 0.03 * math.sin(t * 7.3 + 1.3) + 0.02 * math.sin(t * 31.0)
    if 10.0 <= t < 13.2: fl += 0.10 * math.sin(t * 23.0) * (1 - ease((t - 10.0) / 3.2) * 0.5) + (0.12 * math.sin(t * 47.0) if int(t * 9) % 4 == 0 else 0)
    return x, y, R * (1 + (fl - 1) * 0.4), max(0.0, inten * fl)

YY, XX = np.mgrid[0:H, 0:W].astype(np.float32)

def light_mask(t):
    x, y, R, inten = lamp_state(t)
    d2 = ((XX - x) ** 2 + (YY - y) ** 2) / (R * R)
    m = np.exp(-d2 * 1.9) * inten
    # vùng sáng lan chậm theo đường đi (đã soi rồi thì còn mờ sáng lại)
    return np.clip(m, 0, 1.4), (x, y, R, inten)

# ---- lớp chữ (chỉ hiện trong vùng được soi)
def text_layer():
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    f1 = font('BeVietnamPro-Bold.ttf', 34); f2 = font('BeVietnamPro-ExtraBold.ttf', 40)
    kx, ky = P(*PTS['Kiyosu']); ax, ay = P(*PTS['Atsuta']); ox, oy = P(*PTS['Oke'])
    def lab(x, y, s, f, dx=18, dy=-52):
        d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=(120, 24, 20, 255), outline=(255, 235, 200, 255), width=3)
        d.text((x + dx, y + dy), s, font=f, fill=(34, 20, 10, 255), stroke_width=5, stroke_fill=(250, 232, 196, 255))
    lab(kx, ky, 'Thành Kiyosu', f2)
    bx, by = P(136.78, 34.80)
    d.text((bx, by), 'Vịnh Ise', font=font('BeVietnamPro-Bold.ttf', 40), fill=(224, 238, 244, 255), stroke_width=5, stroke_fill=(20, 44, 60, 255))
    lab(ax, ay, 'Đền Atsuta (đi qua)', f1, dx=-370, dy=-14)
    # vùng không chắc: vòng nét đứt
    r = km_to_px(UNC_R_KM)
    for a in range(0, 360, 12):
        a0 = math.radians(a); a1 = math.radians(a + 6)
        d.line([(ox + r * math.cos(a0), oy + r * math.sin(a0)), (ox + r * math.cos(a1), oy + r * math.sin(a1))], fill=(120, 24, 20, 255), width=5)
    d.text((ox + r + 14, oy - 22), 'Okehazama:', font=f2, fill=(34, 20, 10, 255), stroke_width=5, stroke_fill=(250, 232, 196, 255))
    d.text((ox + r + 14, oy + 22), 'Nagoya hay Toyoake?', font=f1, fill=(34, 20, 10, 255), stroke_width=5, stroke_fill=(250, 232, 196, 255))
    return np.asarray(img, np.float32)

def route_layer(t):
    """đường quân Kiyosu -> Atsuta -> Okehazama vẽ dần, nét đứt"""
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    pts = [P(*PTS['Kiyosu']), P(*PTS['Atsuta']), P(PTS['Atsuta'][0] + (PTS['Oke'][0] - PTS['Atsuta'][0]) * 0.6, PTS['Atsuta'][1] + (PTS['Oke'][1] - PTS['Atsuta'][1]) * 0.6)]
    prog = ease((t - 4.6) / 3.0)
    if prog <= 0: return np.asarray(img, np.float32)
    seg = [math.dist(pts[0], pts[1]), math.dist(pts[1], pts[2])]
    total = sum(seg) * prog
    cur = 0
    for i in range(2):
        a, b = pts[i], pts[i + 1]; L = seg[i]
        use = min(L, max(0, total - cur)); cur += L
        if use <= 0: break
        n = int(use // 22)
        for k in range(n):
            u0 = (k * 22) / L; u1 = min(use, k * 22 + 12) / L
            d.line([(a[0] + (b[0] - a[0]) * u0, a[1] + (b[1] - a[1]) * u0), (a[0] + (b[0] - a[0]) * u1, a[1] + (b[1] - a[1]) * u1)], fill=(120, 24, 20, 255), width=6)
    return np.asarray(img, np.float32)

def stamp_img(text, w=520, h=130, color=(168, 30, 24)):
    S = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(S)
    d.rounded_rectangle([4, 4, w - 5, h - 5], radius=14, outline=color + (255,), width=9)
    d.rounded_rectangle([18, 18, w - 19, h - 19], radius=8, outline=color + (255,), width=3)
    f = font('Oswald.ttf', 84)
    bb = d.textbbox((0, 0), text, font=f)
    d.text(((w - (bb[2] - bb[0])) / 2 - bb[0], (h - (bb[3] - bb[1])) / 2 - bb[1] - 2), text, font=f, fill=color + (255,))
    # vân mực rách
    a = np.asarray(S).copy(); r = rng.random(a.shape[:2]); a[..., 3] = (a[..., 3] * (r > 0.12)).astype(np.uint8)
    return Image.fromarray(a)

STAMPS = [(3.0, 'CÓ SỬ', (1490, 235), -6, (168, 30, 24), 6.2), (11.0, 'KHÔNG AI BIẾT', (1010, 800), 5, (236, 226, 204), 13.2)]
STAMP_IMG = {s[1]: stamp_img(s[1], 700 if len(s[1]) > 6 else 460, 140, s[4]) for s in STAMPS}
SUB = {'CÓ SỬ': 'Nobunaga rời thành, đem quân ra đón đánh.', 'KHÔNG AI BIẾT': 'Chiến trường chính xác ở đâu? Sử chưa trả lời.'}

def draw_stamps(base_rgb, t):
    im = Image.fromarray(np.clip(base_rgb, 0, 255).astype(np.uint8)).convert('RGBA')
    shake = (0, 0)
    for (ts, name, (cx, cy), rot, col, te) in STAMPS:
        if t < ts or t > te: continue
        u = (t - ts)
        out = min(1, max(0, (te - t) / 0.5))
        sc = 1.0 + 0.9 * max(0, 1 - u / 0.14) ** 2   # đập xuống
        al = min(1, u / 0.06) * out
        s = STAMP_IMG[name]
        s2 = s.resize((int(s.width * sc), int(s.height * sc)), Image.LANCZOS).rotate(rot, expand=True, resample=Image.BICUBIC)
        a = np.asarray(s2).copy(); a[..., 3] = (a[..., 3] * al * (0.92 if u > 0.3 else 1)).astype(np.uint8)
        s2 = Image.fromarray(a)
        im.alpha_composite(s2, (int(cx - s2.width / 2), int(cy - s2.height / 2)))
        # dòng giải thích
        f = font('BeVietnamPro-Bold.ttf', 34)
        d = ImageDraw.Draw(im)
        txt = SUB[name]; tw = d.textlength(txt, font=f)
        fa = int(255 * min(1, max(0, (u - 0.5) / 0.4)) * out)
        if fa > 0:
            d.text((W / 2 - tw / 2, 940), txt, font=f, fill=(255, 244, 220, fa), stroke_width=4, stroke_fill=(20, 12, 8, fa))
    return np.asarray(im.convert('RGB'), np.float32)

def main(land_path, out):
    base, L = build_map(land_path)
    txt = text_layer()
    logo = Image.open(LOGO).convert('RGBA').resize((130, 130), Image.LANCZOS)
    la = np.asarray(logo, np.float32)
    # giảm 20% độ đậm như quy định logo
    la[..., 3] *= 0.8
    frames = int(DUR * FPS)
    os.makedirs('/tmp/den_frames', exist_ok=True)
    cold = np.array([0.55, 0.78, 1.0], np.float32); warm = np.array([1.12, 0.98, 0.78], np.float32)
    only = [float(x) for x in os.environ.get('ONLY', '').split(',') if x]
    def render(t):
        m, (lx, ly, R, inten) = light_mask(t)
        dark = base * 0.12 * cold[None, None, :]
        lit = base * warm[None, None, :] * 1.05
        mm = np.clip(m, 0, 1)[..., None]
        fr = dark * (1 - mm) + lit * mm + (np.clip(m - 1, 0, 0.4)[..., None]) * 40
        rt = route_layer(t)
        for layer in (txt, rt):
            a = layer[..., 3:4] / 255 * np.clip(m * 1.15, 0, 1)[..., None]
            fr = fr * (1 - a) + layer[..., :3] * a
        halo = np.exp(-(((XX - lx) ** 2 + (YY - ly) ** 2) / (70.0 ** 2))) * 0.35 * inten
        fr = fr + halo[..., None] * np.array([255, 190, 110], np.float32)[None, None, :] * 0.35
        vg = 1 - 0.55 * (((XX - W / 2) / (W / 2)) ** 2 + ((YY - H / 2) / (H / 2)) ** 2) ** 1.2
        fr = fr * np.clip(vg, 0.35, 1)[..., None]
        fr = draw_stamps(fr, t)
        im = Image.fromarray(np.clip(fr, 0, 255).astype(np.uint8)).convert('RGBA')
        la2 = la.copy(); la2[..., 3] *= min(1, t / 1.2)
        im.alpha_composite(Image.fromarray(la2.astype(np.uint8)), (W - 130 - 44, 34))
        d = ImageDraw.Draw(im)
        f = font('BeVietnamPro-ExtraBold.ttf', 30)
        d.text((60, 40), 'Okehazama, 1560', font=f, fill=(255, 232, 190, int(255 * min(1, t / 1.5))), stroke_width=4, stroke_fill=(10, 6, 4, 200))
        f3 = font('BeVietnamPro-Bold.ttf', 26)
        d.text((60, 82), 'Bản đồ minh họa, vị trí gần đúng', font=f3, fill=(220, 205, 175, int(160 * min(1, t / 1.5))))
        if t >= 13.4:
            u = ease((t - 13.4) / 0.8)
            f4 = font('BeVietnamPro-ExtraBold.ttf', 58)
            s2 = 'Đèn soi tới đâu, sử biết tới đó.'
            tw = d.textlength(s2, font=f4)
            d.text(((W - tw) / 2, H - 160), s2, font=f4, fill=(255, 240, 205, int(255 * u)), stroke_width=6, stroke_fill=(14, 8, 5, int(230 * u)))
        return im.convert('RGB')
    if only:
        for t in only: render(t).save(f'/tmp/den_still_{t:05.2f}.jpg', quality=92)
        return
    for i in range(frames):
        render(i / FPS).save(f'/tmp/den_frames/f{i:04d}.jpg', quality=93)
    # âm thanh: tiếng đập dấu
    aud = '/tmp/den_frames/a.wav'
    cmd = ['ffmpeg', '-y', '-loglevel', 'error']
    boom = os.path.join(HERE, '..', 'phim_ban_do', 'doc9x16', 'boom.wav')
    if os.path.exists(boom):
        flt = ''.join(f'[{k+1}:a]atrim=0:0.9,afade=t=out:st=0.5:d=0.4,volume=0.8,adelay={int(s[0]*1000)}|{int(s[0]*1000)}[b{k}];' for k, s in enumerate(STAMPS))
        mix = ''.join(f'[b{k}]' for k in range(len(STAMPS))) + f'amix=inputs={len(STAMPS)}:normalize=0,apad,atrim=0:{DUR}[a]'
        inputs = ['-framerate', str(FPS), '-i', '/tmp/den_frames/f%04d.jpg'] + sum([['-i', boom] for _ in STAMPS], [])
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error'] + inputs + ['-filter_complex', flt + mix, '-map', '0:v', '-map', '[a]', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-t', str(DUR), out], check=True)
    else:
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', '/tmp/den_frames/f%04d.jpg', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', out], check=True)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
