"""Demo hiệu ứng mực cho tranh thủy mặc: mực loang hiện nhân vật, nét cọ quét chuyển cảnh, zoom chậm."""
import sys, subprocess, numpy as np, cv2
S = 720; FPS = 24
def load(p):
    im = cv2.imread(p); return cv2.resize(im, (S, S), interpolation=cv2.INTER_AREA).astype(np.float32)
def fractal(seed, size=S):
    r = np.random.RandomState(seed); n = np.zeros((size, size), np.float32)
    for k, w in ((8, .5), (16, .25), (32, .15), (64, .1)):
        n += w * cv2.resize(r.rand(k, k).astype(np.float32), (size, size), interpolation=cv2.INTER_CUBIC)
    return (n - n.min()) / (n.max() - n.min())
yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
NZ1, NZ2 = fractal(1), fractal(2)
paper = np.full((S, S, 3), (210, 232, 243), np.float32)  # giấy dó kem (BGR)
def zoom(im, z, cx=.5, cy=.4):
    w = S / z; x0 = (S - w) * cx; y0 = (S - w) * cy
    M = np.float32([[z, 0, -x0 * z], [0, z, -y0 * z]])
    return cv2.warpAffine(im, M, (S, S), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
def bloom(t, cx, cy):
    """mực loang từ (cx,cy): ngưỡng tăng dần, viền lởm chởm theo nhiễu"""
    d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / (S * .75)
    f = d + (NZ1 - .5) * .55
    thr = t * 1.25
    return np.clip((thr - f) * 9, 0, 1)
def brush(t, ang=0.0):
    """nét cọ quét ngang: mép lởm chởm, có vệt khô"""
    pos = -.2 + t * 1.5
    f = xx / S + (NZ2 - .5) * .35 + .06 * np.sin(yy / 23.0)
    m = np.clip((pos - f) * 14, 0, 1)
    return m
A = load("assets/anh_2d/NB3_cf/001.jpg"); B = load("assets/anh_2d/NB3_cf/002.jpg")
out = sys.argv[1]
p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{S}x{S}', '-r', str(FPS), '-i', '-',
                      '-c:v', 'libx264', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
def put(fr): p.stdin.write(np.clip(fr, 0, 255).astype(np.uint8).tobytes())
# 0-2.5s: mực loang hiện Nobunaga; 2.5-5s: zoom chậm; 5-6.5s: nét cọ quét sang Hideyoshi; 6.5-9s: zoom chậm
T = 9.0
for i in range(int(T * FPS)):
    t = i / FPS
    if t < 2.5:
        m = bloom(t / 2.5, S * .5, S * .4)[..., None]; fr = paper * (1 - m) + zoom(A, 1.0) * m
    elif t < 5.0:
        fr = zoom(A, 1.0 + .12 * (t - 2.5) / 2.5, .5, .25)
    elif t < 6.5:
        a = zoom(A, 1.12, .5, .25); b = zoom(B, 1.0)
        m = brush((t - 5.0) / 1.5)[..., None]; fr = a * (1 - m) + b * m
        edge = np.clip(1 - np.abs(brush((t - 5.0) / 1.5) - .5) * 2, 0, 1)[..., None] * (m * (1 - m) * 4)
        fr = fr * (1 - .5 * edge)  # vệt mực đậm ở mép nét cọ
    else:
        fr = zoom(B, 1.0 + .1 * (t - 6.5) / 2.5, .5, .3)
    put(fr)
p.stdin.close(); p.wait()
