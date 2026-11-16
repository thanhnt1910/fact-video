"""Chuỗi: hai tướng giao kiếm (001) -> vệt mực chéo -> kết quả (004): máy quay từ người gục ngước lên người giơ kiếm, K.O. đóng xuống."""
import sys, subprocess, numpy as np, cv2
from PIL import Image
from canh_ko import KO, smooth, PAPER, W, H, FPS, xx, yy
import canh_ko_anh as A
T = 8.4
src = cv2.imread('/home/claude/fact-video/assets/anh_2d/NBM_cf/004.jpg')
m = np.zeros(src.shape[:2], np.uint8); m[930:995, 25:95] = 255
src = cv2.inpaint(src, m, 7, cv2.INPAINT_TELEA)
main = cv2.resize(src, (720, 720), interpolation=cv2.INTER_CUBIC)
fill = cv2.GaussianBlur(cv2.resize(src, (1280, 1280))[280:1000], (0, 0), 30).astype(np.float32) * .55
fe = np.clip(np.minimum(np.arange(720), 719 - np.arange(720)) / 60.0, 0, 1)[None, :, None]
B2 = fill.copy(); B2[:, 280:1000] = main * fe + fill[:, 280:1000] * (1 - fe)
KOs = KO.resize((int(W * .62), int(H * .62)), Image.LANCZOS); KOa = np.asarray(KOs).astype(np.float32)
def f2(t):  # t: giây tính từ lúc cắt sang ảnh kết quả
    u = smooth(t / 2.4)
    cx = 280 + (500 / 1024) * 720; cy = (900 + (300 - 900) * u) / 1024 * 720
    z = 1.9 - .65 * u + .015 * np.sin(t * 2)
    out = cv2.warpAffine(B2, cv2.getRotationMatrix2D((cx, cy), 0, z), (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    rain = np.zeros((H, W), np.uint8); rr = np.random.RandomState(int(t * 24 + 500) % 997)
    for _ in range(380):
        x0 = rr.randint(0, W + 60); y0 = rr.randint(-40, H); cv2.line(rain, (x0, y0), (x0 - 14, y0 + 48), 255, 1, cv2.LINE_AA)
    a = rain[..., None] / 255. * .3; out = out * (1 - a) + 235 * a
    fl = max(0, 1 - abs(t - 0.0) / .12) + max(0, 1 - abs(t - 2.3) / .1) * .8 + max(0, 1 - abs(t - 2.5) / .06) * .5
    out = out * (1 - fl * .85) + 255 * fl * .85
    if t > 2.5:  # K.O. đóng xuống góc trên bên trái
        k = smooth((t - 2.5) / .2); sc = 1.5 - .5 * k
        im = KOs.resize((int(KOs.width * sc), int(KOs.height * sc)), Image.LANCZOS); a_ = np.asarray(im).astype(np.float32)
        x0 = int(330 - im.width / 2); y0 = int(250 - im.height / 2)
        y1, y2, x1, x2 = max(0, y0), min(H, y0 + im.height), max(0, x0), min(W, x0 + im.width)
        al = a_[y1 - y0:y2 - y0, x1 - x0:x2 - x0, 3:4] / 255 * k
        out[y1:y2, x1:x2] = out[y1:y2, x1:x2] * (1 - al) + a_[y1 - y0:y2 - y0, x1 - x0:x2 - x0, :3][..., ::-1] * al
        if t < 2.9:
            a2 = 16 * np.exp(-(t - 2.5) * 9); Mx = np.float32([[1, 0, np.sin(t * 90) * a2], [0, 1, np.cos(t * 77) * a2]]); out = cv2.warpAffine(out, Mx, (W, H), borderMode=cv2.BORDER_REFLECT)
    vg = 1 - .3 * np.clip(((xx - W / 2) / (W * .7)) ** 2 + ((yy - H / 2) / (H * .75)) ** 2, 0, 1)
    out = out * vg[..., None] + np.random.RandomState(int(t * 24) + 7).randn(H, W, 1).astype(np.float32) * 4
    return np.clip(out, 0, 255)
def frame(t):
    if t < 3.4: out = A.frame(t)
    else: out = f2(t - 3.4)
    fade = smooth((t - 7.6) / .8); return out * (1 - fade) + PAPER * fade
if __name__ == '__main__':
    out = sys.argv[1]
    if len(sys.argv) > 2:
        for s_ in sys.argv[2:]: cv2.imwrite(f'/tmp/kc_{float(s_):04.1f}.jpg', frame(float(s_)).astype(np.uint8))
        sys.exit()
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    for i in range(int(T * FPS)): p.stdin.write(frame(i / FPS).astype(np.uint8).tobytes())
    p.stdin.close(); p.wait()
