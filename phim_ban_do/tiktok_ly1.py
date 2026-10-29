"""Dựng video dọc 9:16 cho TikTok từ video dài đã dựng: python tiktok_ly1.py <video_dai.mp4> <ra.mp4> [giây=74.6]
Cắt phần đầu, nền mờ, khung hình 16:9 ở giữa (bỏ phụ đề cũ), phụ đề lớn dưới khung theo mốc cụm của phude_ly1.json.
Cần các biến môi trường như khi dựng video dài (SCRIPT, VOICE_DIR, PHUDE, FONT ...), để lấy mốc thời gian câu."""
import os, sys, json, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build2 as B

src, out = sys.argv[1], sys.argv[2]
DUR = float(sys.argv[3]) if len(sys.argv) > 3 else 74.6
FPS = 24
W, H = 1080, 1920
FONT = os.environ.get('FONT')


def font(sz, bold=True):
    f = ImageFont.truetype(FONT, sz)
    try:
        f.set_variation_by_name('Bold' if bold else 'Regular')
    except Exception:
        pass
    return f


def wrap(g, txt, f, maxw):
    lines, cur = [], ''
    for w in txt.split():
        t = (cur + ' ' + w).strip()
        if g.textlength(t, font=f) <= maxw: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur); return lines


# --- danh sách cụm phụ đề tuyệt đối: (bắt đầu, kết thúc, chữ) ---
caps = []
for n in sorted(B.T):
    for c in B.PH.get(str(n), []):
        caps.append((B.T[n] + c[1], B.T[n] + c[2], c[0]))
caps = [c for c in caps if c[0] < DUR]

FG_Y, FG_H = 330, 530          # khung 16:9 đã bỏ dải phụ đề: 1920x900 thu về 1080x506
CAP_Y = 960
LOGO = Image.open(os.environ['LOGO']).convert('RGBA')


def static_layer():
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); g = ImageDraw.Draw(im)
    f1, f2 = font(92), font(52, False)
    t1, t2 = 'LÝ CÔNG UẨN', 'NGƯỜI DỜI ĐÔ'
    for t, ff, y, col in ((t1, f1, 120, (244, 205, 90, 255)), (t2, f1, 220, (250, 244, 228, 255))):
        w = g.textlength(t, font=ff)
        g.text(((W - w) / 2 + 3, y + 4), t, font=ff, fill=(0, 0, 0, 200)); g.text(((W - w) / 2, y), t, font=ff, fill=col)
    h = 'NGƯỜI GÁC SỬ  ·  chuyện có thật trong lịch sử'
    sz = 52
    while g.textlength(h, font=font(sz, False)) > W - 120: sz -= 2
    f2 = font(sz, False)
    w = g.textlength(h, font=f2); g.text(((W - w) / 2, H - 150), h, font=f2, fill=(250, 244, 228, 190))
    lg = LOGO.resize((130, 130), Image.LANCZOS); lg.putalpha(lg.split()[3].point(lambda v: int(v * 0.8)))
    im.alpha_composite(lg, (W - 44 - 130, 34))
    return im


def cap_layer(txt):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); g = ImageDraw.Draw(im); f = font(78)
    lines = wrap(g, txt, f, W - 160); lh = 104; h = lh * len(lines) + 50
    g.rounded_rectangle((50, CAP_Y, W - 50, CAP_Y + h), 34, fill=(10, 6, 4, 190))
    for i, l in enumerate(lines):
        w = g.textlength(l, font=f); x = (W - w) / 2; y = CAP_Y + 25 + i * lh
        g.text((x + 3, y + 4), l, font=f, fill=(0, 0, 0, 255)); g.text((x, y), l, font=f, fill=(250, 244, 228, 255))
    return im


STATIC = static_layer()
CAPL = {}
rd = subprocess.Popen(['ffmpeg', '-v', 'error', '-t', str(DUR), '-i', src, '-vf', f'fps={FPS}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                      stdout=subprocess.PIPE)
wr = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                       '-t', str(DUR), '-i', src, '-map', '0:v', '-map', '1:a', '-t', str(DUR),
                       '-vf', f'fade=t=out:st={DUR - 1.2}:d=1.2', '-af', f'afade=t=out:st={DUR - 1.2}:d=1.2',
                       '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '160k', out],
                      stdin=subprocess.PIPE)
fs = 1920 * 1080 * 3
k = 0
while True:
    buf = rd.stdout.read(fs)
    if len(buf) < fs: break
    t = k / FPS
    fr = Image.frombytes('RGB', (1920, 1080), buf)
    fr.paste(fr.crop((1734, 24, 1736, 172)).resize((150, 148), Image.BILINEAR), (1738, 24))   # che logo nhỏ trong video gốc
    bg = fr.resize((W // 6, H // 6), Image.BILINEAR).resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(14))
    bg = Image.eval(bg, lambda v: int(v * 0.55))
    fg = fr.crop((0, 0, 1920, 940)).resize((W, FG_H), Image.LANCZOS)
    bg.paste(fg, (0, FG_Y))
    canvas = bg.convert('RGBA')
    canvas.alpha_composite(STATIC)
    c = next((c for c in caps if c[0] <= t < c[1]), None)
    if c:
        key = c[2]
        if key not in CAPL: CAPL[key] = cap_layer(key)
        a = min(1.0, (t - c[0]) / 0.12, (c[1] - t) / 0.1 + 0.3)
        lay = CAPL[key]
        if a < 1.0:
            lay = lay.copy(); lay.putalpha(lay.split()[3].point(lambda v: int(v * max(0, a))))
        canvas.alpha_composite(lay)
    wr.stdin.write(canvas.convert('RGB').tobytes())
    k += 1
wr.stdin.close(); wr.wait(); rd.wait()
print('xong', k, 'khung')
