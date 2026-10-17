"""
HOẠT HÌNH NHẸ (không dùng AI): làm cây cỏ, hoa, cờ, nước, lửa lay động rất nhẹ trên chính ảnh 2D, cộng một chuyển động máy rất chậm.

  python anim_nhe.py TQ2 004,016,056            -> assets/clips_2d/TQ2_nhe/<số>.mp4  (1920x1080, 24 fps, 8 giây)
  python anim_nhe.py TQ2 004 --bao-cao          -> thêm ảnh "bản đồ chuyển động" và số liệu độ mượt

Vì sao dùng cách này: mỗi khung hình là chính bức tranh gốc, chỉ dịch điểm ảnh vài pixel theo một hàm sóng liên tục
(lấy mẫu dưới điểm ảnh, nội suy bậc ba), nên không giật, không biến dạng nhân vật và không đổi nét vẽ như video AI.
Vùng chuyển động xác định bằng màu (cỏ, lá, hoa hồng, nước, lửa) và khung chữ nhật chọn tay trong ke-hoach/nhan-vat/<MÃ>_nhe.json.
Người, giáp, vũ khí nằm ngoài vùng nên đứng yên.
"""
import json
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parent
W, H, FPS = 1920, 1080, 24


def load(path):
    im = cv2.imread(str(path), cv2.IMREAD_COLOR)
    h, w = im.shape[:2]
    s = W / w
    nh = round(h * s)
    im = cv2.resize(im, (W, nh), interpolation=cv2.INTER_LANCZOS4)
    top = max(0, (nh - H) // 2)
    return im[top:top + H].copy()


def box_mask(boxes, feather):
    m = np.zeros((H, W), np.float32)
    for x0, y0, x1, y1 in boxes:
        m[int(y0 * H):int(y1 * H), int(x0 * W):int(x1 * W)] = 1.0
    k = max(3, int(feather) | 1)
    return cv2.GaussianBlur(m, (k, k), 0)


def color_mask(hsv, sp):
    """sp: hue [[lo,hi],...] (thang 0-180 của OpenCV), smin, smax, vmin, vmax."""
    h, s, v = cv2.split(hsv)
    m = np.zeros((H, W), np.uint8)
    for lo, hi in sp.get("hue", [[0, 180]]):
        m |= ((h >= lo) & (h <= hi)).astype(np.uint8)
    m &= ((s >= sp.get("smin", 0)) & (s <= sp.get("smax", 255))).astype(np.uint8)
    m &= ((v >= sp.get("vmin", 0)) & (v <= sp.get("vmax", 255))).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    return m.astype(np.float32)


def layer_mask(hsv, L):
    m = np.ones((H, W), np.float32)
    if "mau" in L:
        m *= color_mask(hsv, L["mau"])
    if "vung" in L:
        m *= box_mask(L["vung"], L.get("lam_mem", 41))
    elif "mau" in L:
        pass
    k = int(L.get("lam_mem", 41)) | 1
    return cv2.GaussianBlur(m, (k, k), 0) if "mau" in L else m


def render(ma, key, spec, bao_cao=False, dur=8.0, hau_to=""):
    src = ROOT / "assets" / "anh_2d" / ma / f"{key}.jpg"
    img = load(src)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    layers = []
    Y0, X0 = np.mgrid[0:H, 0:W].astype(np.float32)
    for L in spec["lop"]:
        G = None
        if L.get("halo"):                            # quầng sáng tròn mềm quanh ngọn nến/đèn (không dùng lọc màu)
            G = np.zeros((H, W), np.float32)
            for x0, y0, x1, y1 in L["vung"]:
                gx, gy = (x0 + x1) / 2 * W, (y0 + y1) / 2 * H
                sx, sy = max(8.0, (x1 - x0) * W * 0.9), max(8.0, (y1 - y0) * H * 0.9)
                G = np.maximum(G, np.exp(-(((X0 - gx) / sx) ** 2 + ((Y0 - gy) / sy) ** 2)))
        layers.append((L, layer_mask(hsv, L), G))
    n = int(round(dur * FPS))
    Y, X = np.mgrid[0:H, 0:W].astype(np.float32)
    cx, cy = W / 2, H / 2
    zoom = float(spec.get("zoom", 0.03))
    pan = spec.get("pan", [6, 0])
    out_dir = ROOT / "assets" / "clips_2d" / f"{ma}_nhe"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{key}{hau_to}.mp4"
    ff = subprocess.Popen(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24",
                           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-an", "-c:v", "libx264", "-crf", "14",
                           "-preset", "medium", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out)],
                          stdin=subprocess.PIPE)
    prev = None
    diffs = []
    acc = np.zeros((H, W), np.float32) if bao_cao else None
    acc2 = np.zeros((H, W), np.float32) if bao_cao else None
    for i in range(n):
        t = i / FPS
        u = t / dur
        s = u * u * (3 - 2 * u)              # đẩy máy rất chậm, êm ở hai đầu
        z = 1.0 + zoom * s
        dx = np.zeros((H, W), np.float32)
        dy = np.zeros((H, W), np.float32)
        bright = np.ones((H, W), np.float32)
        for L, m, G in layers:
            a = float(L.get("bien", 2.5))
            c = float(L.get("nhip", 1))                 # số chu kỳ trong clip (nguyên => lặp khít)
            ph = 2 * np.pi * (c * u + L.get("pha_x", 0.6) * X / W + L.get("pha_y", 0.25) * Y / H)
            kind = L["loai"]
            if kind == "gio":                           # cỏ, cây, hoa: lắc ngang là chính
                dx += m * a * (np.sin(ph) + 0.35 * np.sin(2.3 * ph + 1.1))
                dy += m * a * 0.35 * np.sin(ph + 1.7)
            elif kind == "co":                          # cờ: sóng chạy dọc lá cờ
                ph2 = 2 * np.pi * (c * u - L.get("song", 3.0) * X / W)
                dy += m * a * np.sin(ph2)
                dx += m * a * 0.5 * np.sin(ph2 + 0.8)
            elif kind == "nuoc":                        # nước: gợn ngang theo dải
                ph3 = 2 * np.pi * (c * u + L.get("song", 14.0) * Y / H)
                dx += m * a * np.sin(ph3)
            elif kind == "lua":                         # lửa: bốc lên và chớp sáng
                ph4 = 2 * np.pi * (c * u + L.get("song", 9.0) * X / W)
                dy += m * -a * (0.5 + 0.5 * np.sin(ph4))
                dx += m * a * 0.5 * np.sin(ph4 * 1.7 + 0.4)
                flick = np.sin(2 * np.pi * (3 * c * u) + 0.9 * X / W * 6) + 0.5 * np.sin(2 * np.pi * (5 * c * u) + 1.3)
                bright += (G if G is not None else m) * float(L.get("chop", 0.10)) * flick
        mx = cx + (X - cx) / z - pan[0] * s + dx
        my = cy + (Y - cy) / z - pan[1] * s + dy
        fr = cv2.remap(img, mx, my, cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)
        if np.any(bright != 1.0):
            fr = np.clip(fr.astype(np.float32) * bright[..., None], 0, 255).astype(np.uint8)
        ff.stdin.write(fr.tobytes())
        if bao_cao:
            g = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY).astype(np.float32)
            acc += g
            acc2 += g * g
            if prev is not None:
                diffs.append(float(np.abs(g - prev).mean()))
            prev = g
    ff.stdin.close()
    ff.wait()
    info = {"clip": str(out.relative_to(ROOT)), "giay": dur, "fps": FPS}
    if bao_cao:
        std = np.sqrt(np.maximum(acc2 / n - (acc / n) ** 2, 0))
        hm = np.clip(std * 12, 0, 255).astype(np.uint8)
        hm = cv2.applyColorMap(hm, cv2.COLORMAP_INFERNO)
        cv2.imwrite(str(out_dir / f"{key}{hau_to}_bando.jpg"), cv2.addWeighted(img, 0.35, hm, 0.65, 0))
        d = np.array(diffs)
        info["chenh_lech_khung_tb"] = round(float(d.mean()), 3)
        info["do_nhay_lon_nhat"] = round(float(np.abs(np.diff(d)).max()), 3)
    return info


def main():
    ma = sys.argv[1]
    keys = [k for k in sys.argv[2].split(",") if k]
    bao_cao = "--bao-cao" in sys.argv
    ngan = "--ngan" in sys.argv                  # chỉ để kiểm tra nhanh: 3 giây
    khong_may = "--khong-may" in sys.argv        # tắt chuyển động máy để kiểm tra riêng vùng gió
    cfg = json.loads((ROOT / "ke-hoach" / "nhan-vat" / f"{ma}_nhe.json").read_text(encoding="utf-8"))
    for k in keys:
        if k not in cfg["anh"]:
            print(f"Bỏ qua {k}: chưa có cấu hình trong {ma}_nhe.json")
            continue
        spec = dict(cfg["anh"][k])
        if khong_may:
            spec["zoom"], spec["pan"] = 0.0, [0, 0]
        print(json.dumps(render(ma, k, spec, bao_cao, 3.0 if ngan else cfg.get("giay", 8.0), "_khongmay" if khong_may else ""), ensure_ascii=False))


if __name__ == "__main__":
    main()
