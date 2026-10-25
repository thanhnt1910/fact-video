"""
HOẠT HÌNH CẮT LỚP (không dùng AI tạo video): tách nhân vật khỏi nền rồi cho nhân vật thở, lắc nhẹ, gật đầu; nền trượt chậm hơn (thị sai).

  python anim_cat_lop.py <ảnh.jpg> <x0,y0,x1,y1 (tỉ lệ 0-1, khung bao nhân vật)> <ra.mp4> [giây=4] [kiểu=nhe|noi]

- Tách bằng GrabCut trong khung bao; vùng nhân vật bị khoét thì tô lại nền bằng inpaint.
- Chuyển động: nhân vật "thở" (co giãn dọc quanh chân), lắc ngang tăng dần về phía đầu, gật đầu nhẹ; nền phóng chậm hơn.
- Chỉ dùng cho ảnh có một nhân vật (hoặc một nhóm) đứng trong khung bao đã chọn.
"""
import math
import subprocess
import sys

import cv2
import numpy as np


def tach(img, box):
    h, w = img.shape[:2]
    x0, y0, x1, y1 = box
    rect = (int(x0 * w), int(y0 * h), int((x1 - x0) * w), int((y1 - y0) * h))
    mask = np.zeros((h, w), np.uint8)
    bgd = np.zeros((1, 65), np.float64)
    fgd = np.zeros((1, 65), np.float64)
    small = 0.5
    im_s = cv2.resize(img, None, fx=small, fy=small, interpolation=cv2.INTER_AREA)
    m_s = np.zeros(im_s.shape[:2], np.uint8)
    r_s = tuple(int(v * small) for v in rect)
    cv2.grabCut(im_s, m_s, r_s, bgd, fgd, 6, cv2.GC_INIT_WITH_RECT)
    m = np.where((m_s == cv2.GC_FGD) | (m_s == cv2.GC_PR_FGD), 255, 0).astype(np.uint8)
    m = cv2.resize(m, (w, h), interpolation=cv2.INTER_LINEAR)
    # giữ khối lớn nhất, lấp lỗ, làm mềm mép
    n, lab, st, _ = cv2.connectedComponentsWithStats((m > 127).astype(np.uint8))
    if n > 1:
        keep = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
        m = np.where(lab == keep, 255, 0).astype(np.uint8)
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, k)
    m = cv2.GaussianBlur(m, (5, 5), 0)
    return m


def main():
    src, box_s, out = sys.argv[1], sys.argv[2], sys.argv[3]
    sec = float(sys.argv[4]) if len(sys.argv) > 4 else 4.0
    kieu = sys.argv[5] if len(sys.argv) > 5 else "nhe"
    box = [float(v) for v in box_s.split(",")]
    img = cv2.imread(src)
    W, H = 1280, 720
    img = cv2.resize(img, (W, H), interpolation=cv2.INTER_AREA)
    m = tach(img, box)
    dil = cv2.dilate((m > 40).astype(np.uint8) * 255, np.ones((15, 15), np.uint8))
    bg = cv2.inpaint(img, dil, 5, cv2.INPAINT_TELEA)
    ys, xs = np.where(m > 127)
    top, bot = ys.min(), ys.max()
    cx = int(xs.mean())
    A = 1.0 if kieu == "nhe" else 1.8
    fps = 24
    n = int(sec * fps)
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    hh = max(bot - top, 1)
    wgt = np.clip((bot - yy) / hh, 0, 1)  # 0 ở chân, 1 ở đầu
    fg_a = (m.astype(np.float32) / 255.0)
    for i in range(n):
        t = i / fps
        z = 1.0 + 0.035 * i / n
        M = cv2.getRotationMatrix2D((W / 2, H / 2), 0, z)
        bg_f = cv2.warpAffine(bg, M, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        breath = 1.0 + 0.010 * A * math.sin(2 * math.pi * t / 2.4)
        sway = 3.0 * A * math.sin(2 * math.pi * t / 3.2)
        nod = 5.0 * A * max(0.0, math.sin(2 * math.pi * t / 2.0)) ** 2
        zf = 1.0 + 0.055 * i / n
        # ánh xạ ngược: điểm đích (x,y) lấy từ nguồn
        ys_src = bot - (bot - yy) / breath
        ys_src = ys_src - nod * np.exp(-((yy - top - 0.08 * hh) ** 2) / (2 * (0.14 * hh) ** 2))
        xs_src = xx - sway * wgt ** 1.5
        # phóng nhẹ quanh chân nhân vật (nhanh hơn nền)
        xs_src = cx + (xs_src - cx) / zf
        ys_src = bot + (ys_src - bot) / zf
        fg_w = cv2.remap(img, xs_src.astype(np.float32), ys_src.astype(np.float32), cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        a_w = cv2.remap(fg_a, xs_src.astype(np.float32), ys_src.astype(np.float32), cv2.INTER_LINEAR, borderValue=0)[..., None]
        fr = bg_f.astype(np.float32) * (1 - a_w) + fg_w.astype(np.float32) * a_w
        p.stdin.write(np.clip(fr, 0, 255).astype(np.uint8).tobytes())
    p.stdin.close()
    p.wait()
    cv2.imwrite(out.rsplit(".", 1)[0] + "_mask.png", m)
    print("xong", out)


if __name__ == "__main__":
    main()
