"""Cảnh K.O. từ ảnh thủy mặc (Cloudflare FLUX): camera, mưa, chớp, hai vệt mực chéo, chữ K.O. Tự động hoàn toàn."""
import sys, subprocess, numpy as np, cv2
from canh_ko import slash, KO, smooth, PAPER, W, H, FPS, xx, yy
from PIL import Image
T = 6.5
src = cv2.imread('/home/claude/fact-video/assets/anh_2d/NBM_cf/001.jpg')
# xóa con dấu đỏ và chữ trên cờ bằng inpaint (ảnh AI hay tự vẽ chữ)
mask = np.zeros(src.shape[:2], np.uint8)
mask[920:1005, 470:540] = 255; mask[90:300, 860:1000] = 255
src = cv2.inpaint(src, mask, 7, cv2.INPAINT_TELEA)
main = cv2.resize(src, (720, 720), interpolation=cv2.INTER_CUBIC)
fill = cv2.GaussianBlur(cv2.resize(src, (1280, 1280))[280:1000], (0, 0), 30).astype(np.float32) * .55
BASE = fill.copy(); BASE[:, 280:1000] = main
fe = np.clip(np.minimum(np.arange(720), 719 - np.arange(720)) / 60.0, 0, 1)[None, :, None]
BASE[:, 280:1000] = main * fe + fill[:, 280:1000] * (1 - fe)
def frame(t):
    s = t if t < 2.2 else 2.2 + .25 * (t - 2.2) if t < 3.4 else 2.5 + (t - 3.4)
    z = 1.0 + .25 * smooth(s / 2.2) + .45 * smooth((s - 2.2) / .3) + .01 * np.sin(t * 2)
    cx, cy = 280 + 500 / 1024 * 720, 640 / 1024 * 720
    M = cv2.getRotationMatrix2D((cx, cy), 0, z)
    out = cv2.warpAffine(BASE, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    # mưa
    rain = np.zeros((H, W), np.uint8); rr = np.random.RandomState(int(t * 24) % 997)
    for _ in range(420):
        x0 = rr.randint(0, W + 60); y0 = rr.randint(-40, H); cv2.line(rain, (x0, y0), (x0 - 14, y0 + 48), 255, 1, cv2.LINE_AA)
    a = rain[..., None] / 255. * .35; out = out * (1 - a) + 235 * a
    # chớp lúc kiếm chạm và lúc va chạm
    fl = max(0, 1 - abs(t - 1.2) / .08) * .5 + max(0, 1 - abs(t - 2.75) / .1)
    out = out * (1 - fl * .9) + 255 * fl * .9
    o8 = np.ascontiguousarray(np.clip(out, 0, 255).astype(np.uint8))
    if t > 2.8: slash(o8, (60, 40), (1230, 690), smooth((t - 2.8) / .35))
    if t > 3.05: slash(o8, (1230, 60), (50, 680), smooth((t - 3.05) / .35))
    out = o8.astype(np.float32)
    if t > 3.5:
        u = smooth((t - 3.5) / .22); sc = 1.9 - .9 * u
        im = KO.resize((int(W * sc), int(H * sc)), Image.LANCZOS); a_ = np.asarray(im).astype(np.float32)
        y0 = int(H / 2 - im.height / 2); x0 = int(W / 2 - im.width / 2)
        y1, y2, x1, x2 = max(0, y0), min(H, y0 + im.height), max(0, x0), min(W, x0 + im.width)
        al = a_[y1 - y0:y2 - y0, x1 - x0:x2 - x0, 3:4] / 255 * u
        out[y1:y2, x1:x2] = out[y1:y2, x1:x2] * (1 - al) + a_[y1 - y0:y2 - y0, x1 - x0:x2 - x0, :3][..., ::-1] * al
    if 3.5 < t < 3.9:
        a = 18 * np.exp(-(t - 3.5) * 9); Mx = np.float32([[1, 0, np.sin(t * 90) * a], [0, 1, np.cos(t * 77) * a]]); out = cv2.warpAffine(out, Mx, (W, H), borderMode=cv2.BORDER_REFLECT)
    vg = 1 - .3 * np.clip(((xx - W / 2) / (W * .7)) ** 2 + ((yy - H / 2) / (H * .75)) ** 2, 0, 1)
    out = out * vg[..., None] + np.random.RandomState(int(t * 24)).randn(H, W, 1).astype(np.float32) * 4
    fade = smooth((t - 5.8) / .7); out = out * (1 - fade) + PAPER * fade
    if t < .3: out = out * (t / .3) + PAPER * (1 - t / .3)
    return np.clip(out, 0, 255)
if __name__ == '__main__':
    out = sys.argv[1]
    if len(sys.argv) > 2:
        for s_ in sys.argv[2:]: cv2.imwrite(f'/tmp/koa_{float(s_):04.1f}.jpg', frame(float(s_)).astype(np.uint8))
        sys.exit()
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    for i in range(int(T * FPS)): p.stdin.write(frame(i / FPS).astype(np.uint8).tobytes())
    p.stdin.close(); p.wait()
