"""Trader9x Masterclass – Khung thời gian H1 → H4 → D1 (dữ liệu thật MetalCharts)."""
import sys, os, math, subprocess
from datetime import timedelta
import numpy as np
from PIL import Image, ImageDraw
import importlib.util
_MAU = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "mau_macd")
sys.path.insert(0, _MAU)   # để bộ mẫu tìm thấy data.py của nó
_spec = importlib.util.spec_from_file_location("mau_render", os.path.join(_MAU, "render.py"))
R = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(R)   # phông, màu, chữ, logo, phụ đề… của bộ mẫu
sys.path.pop(0)
from tfdata import D1, H1, H4, VN

W, H, FPS = R.W, R.H, R.FPS
F, mix, prog, eio, clamp = R.F, R.mix, R.prog, R.eio, R.clamp
BG, PANEL, LINE, GRID = R.BG, R.PANEL, R.LINE, R.GRID
WHITE, MUTED, DIM, GOLD, GREEN, RED, BLUE, ORANGE, PURPLE = R.WHITE, R.MUTED, R.DIM, R.GOLD, R.GREEN, R.RED, R.BLUE, R.ORANGE, R.PURPLE
pill, dashed, circle, rich, vn, logo, wordmark, legend = R.pill, R.dashed, R.circle, R.rich, R.vn, R.logo, R.wordmark, R.legend

SER = {"H1": H1, "D1": D1, "H4": H4}
TF_COL = {"H1": BLUE, "H4": ORANGE, "D1": GOLD}
CX0, CX1 = 40, 925
PY0, PY1 = 300, 1400
VIEW = 40
BW = (CX1 - CX0) / VIEW

def idx_of(tf, utc_iso):
    for i, b in enumerate(SER[tf]):
        if b["t"].isoformat().startswith(utc_iso): return i
    raise KeyError(utc_iso)

class Cam:
    def __init__(s, tf, vs, nb):
        s.tf, s.vs, s.nb, s.S = tf, vs, nb, SER[tf]; s.N = len(s.S)
        lo0, hi0 = s._rng(math.floor(vs), math.floor(nb)); lo1, hi1 = s._rng(math.floor(vs) + 1, math.floor(nb) + 1)
        f = ((vs - math.floor(vs)) + (nb - math.floor(nb))) / 2
        s.plo, s.phi = lo0 + (lo1 - lo0) * f, hi0 + (hi1 - hi0) * f
    def _rng(s, a, b):
        i0 = max(0, int(a)); i1 = min(s.N, max(i0 + 6, int(b) + 1), int(a) + VIEW)
        lo = min(x["l"] for x in s.S[i0:i1]); hi = max(x["h"] for x in s.S[i0:i1])
        sp = max(hi - lo, 40); return lo - sp * .12, hi + sp * .16
    def x(s, i): return CX0 + (i - s.vs + .5) * BW
    def py(s, p): return PY1 - (p - s.plo) / (s.phi - s.plo) * (PY1 - PY0)
    def vis(s, i): return s.vs - .5 <= i <= s.vs + VIEW - .5

def tlabel(tf, t):
    v = t + VN
    return v.strftime("%d/%m") if tf == "D1" else v.strftime("%d/%m %Hh")

def draw_chart(d, cam, a=1.0, zones=()):
    tf, S = cam.tf, cam.S
    span = cam.phi - cam.plo; step = 10 if span < 90 else 25 if span < 220 else 50 if span < 450 else 100
    p = math.ceil(cam.plo / step) * step
    while p < cam.phi:
        y = cam.py(p)
        if PY0 < y < PY1: d.line([(CX0, y), (CX1, y)], fill=mix(GRID, a)); d.text((CX1 + 10, y), vn(p, 0), font=F(22, "Medium"), fill=mix(DIM, a), anchor="lm")
        p += step
    every = {"H1": 6, "H4": 6, "D1": 5}[tf]
    for i in range(0, cam.N):
        if i % every == 0 and cam.vis(i):
            x = cam.x(i) - BW / 2
            if CX0 <= x <= CX1:
                d.line([(x, PY0), (x, PY1)], fill=mix(GRID, a))
                d.text((x + 6, PY1 - 30), tlabel(tf, S[i]["t"]), font=F(19, "SemiBold"), fill=mix(DIM, a))
    d.text((CX0 + 4, PY0 - 36), f"XAUUSD · {tf}", font=F(26, "Bold"), fill=mix(TF_COL[tf], a))
    d.text(((CX0 + CX1) / 2, (PY0 + PY1) / 2), tf, font=F(260, "Black"), fill=mix((16, 20, 30), a), anchor="mm")
    for z in zones: z(d, cam, a)
    nb = cam.nb; k = int(nb); fr = nb - k
    for i in range(max(0, int(cam.vs) - 1), min(cam.N, k + 1)):
        if not cam.vis(i): continue
        b = S[i]; o, h, l, c = b["o"], b["h"], b["l"], b["c"]
        if i == k:
            if fr <= 0: break
            c = o + (c - o) * fr; h = max(o, c) + (h - max(b["o"], b["c"])) * fr; l = min(o, c) - (min(b["o"], b["c"]) - l) * fr
        col = mix(GREEN if c >= o else RED, a); x = cam.x(i)
        d.line([(x, cam.py(h)), (x, cam.py(l))], fill=col, width=3)
        y0, y1 = sorted([cam.py(o), cam.py(c)]); d.rectangle([x - BW * .34, y0, x + BW * .34, max(y1, y0 + 2)], fill=col)
    if nb > 0 and a > .5:
        li = min(cam.N - 1, k if fr > 0 else k - 1); b = S[li]
        last = b["o"] + (b["c"] - b["o"]) * (fr if (fr > 0 and li == k) else 1)
        col = GREEN if last >= b["o"] else RED; y = cam.py(last)
        dashed(d, (CX0, y), (CX1, y), mix(col, .6 * a), 1, 6)
        f = F(21, "Bold"); txt = vn(last, 2); tw = d.textlength(txt, font=f)
        d.rounded_rectangle([CX1 + 2, y - 17, CX1 + 16 + tw, y + 17], 6, fill=mix(col, a)); d.text((CX1 + 9, y), txt, font=f, fill=BG, anchor="lm")

def zone_rect(i0, lo, hi, col, label=None, tf=None):
    def f(d, cam, a):
        if tf and cam.tf != tf: return
        x0 = max(CX0, cam.x(i0) - BW / 2); x1 = CX1
        if x1 <= x0: return
        fill = tuple(int(BG[j] + (col[j] - BG[j]) * .22) for j in range(3))
        d.rectangle([x0, cam.py(hi), x1, cam.py(lo)], fill=mix(fill, a), outline=mix(col, a), width=2)
        if label: d.text((x0 + 10, cam.py(hi) - 30), label, font=F(22, "Bold"), fill=mix(col, a))
    return f

# ---------- chrome ----------
PARTS = {1: ("Định nghĩa", "Khung thời gian là gì?"), 2: ("Thuật ngữ & ứng dụng", "H1 → H4 → D1 trên vàng thật")}
def header(d, part, title, sub, a=1.0):
    logo(d, 40, 54, 46, a)
    d.text((98, 77), "TRADER9X MASTERCLASS · XAUUSD", font=F(23, "Bold"), fill=mix(GOLD, a), anchor="lm")
    d.text((W - 40, 77), f"PHẦN {part}/2", font=F(23, "Bold"), fill=mix(GOLD, a), anchor="rm")
    d.text((40, 118), title, font=F(60, "ExtraBold"), fill=mix(WHITE, a))
    d.text((42, 196), sub, font=F(28, "Medium"), fill=mix(MUTED, a))
CAP_Y = 1470
def caption(d, t, caps, y=CAP_Y): R.caption(d, t, caps, y)
def footer(d, gt):
    y = 1730
    d.rectangle([40, y, W - 40, y + 6], fill=(26, 32, 44)); d.rectangle([40, y, 40 + (W - 80) * gt / TOTAL, y + 6], fill=GOLD)
    d.text((W / 2, 1822), "Nội dung giáo dục, không phải khuyến nghị đầu tư.", font=F(22, "Medium"), fill=DIM, anchor="mm")
    d.text((W / 2, 1854), "Giá thật MetalCharts: D1 01/10–27/11, H1 18–27/11 · giờ VN · © 2026 Trader9x", font=F(21, "Medium"), fill=DIM, anchor="mm")
def chapter_card(im, t, du, num):
    title, sub = PARTS[num]
    a = min(prog(t, 0, .35), clamp((du - t) / .3))
    im.paste(Image.blend(im, Image.new("RGB", (W, H), BG), .82 * a)); d = ImageDraw.Draw(im)
    d.text((W / 2, 760), "PHẦN", font=F(40, "Bold"), fill=mix(MUTED, a), anchor="mm")
    d.text((W / 2, 880), f"{num:02d}", font=F(190, "Black"), fill=mix(GOLD, a), anchor="mm")
    w = 240 * prog(t, .15, .5); d.rectangle([W / 2 - w, 1000, W / 2 + w, 1005], fill=mix(GOLD, a))
    d.text((W / 2, 1070), title, font=F(66, "ExtraBold"), fill=mix(WHITE, a), anchor="mm")
    d.text((W / 2, 1140), sub, font=F(34, "Medium"), fill=mix(MUTED, a), anchor="mm")
def term_card(d, ti, a):
    nm, df, col = TERMS[ti]
    y = CAP_Y + 12; off = (1 - a) * 16
    d.rounded_rectangle([40, y + off, W - 40, y + 228 + off], 22, fill=mix(PANEL, a), outline=mix(col, a), width=3)
    d.text((76, y + 36 + off), f"THUẬT NGỮ {ti + 1}/{len(TERMS)}", font=F(22, "Bold"), fill=mix(MUTED, a), anchor="lm")
    d.text((76, y + 84 + off), nm, font=F(46, "ExtraBold"), fill=mix(col, a), anchor="lm")
    rich(d, 76, y + 124 + off, df, F(31, "SemiBold"), W - 160, a, 42)

# ---------- Phần 1: một ngày 25/11 trên 3 khung ----------
DAY_D1 = [b for b in D1 if b["t"].date().isoformat() == "2026-11-25"][0]
i25 = idx_of("H1", "2026-11-24T20:00")
DAY_H1 = H1[i25:i25 + 24]
DAY_H4 = [b for b in H4 if DAY_H1[0]["t"] <= b["t"] <= DAY_H1[-1]["t"]]
def draw_split(d, t, a):
    """t: thời gian trong cảnh p1. 0–4: D1 · 4–10: D1 · 10–15.5: H4 · ≥15.5: H1"""
    x0, x1, y0, y1 = 120, 900, 320, 1330
    lo, hi = DAY_D1["l"] - 15, DAY_D1["h"] + 15
    py = lambda p: y1 - (p - lo) / (hi - lo) * (y1 - y0)
    d.rounded_rectangle([x0 - 60, y0 - 40, x1 + 100, y1 + 70], 26, fill=mix(PANEL, a * .9), outline=mix(LINE, a), width=2)
    for p in range(3450, 3600, 50):
        y = py(p); d.line([(x0 - 40, y), (x1 + 20, y)], fill=mix(GRID, a)); d.text((x1 + 30, y), vn(p, 0), font=F(22, "Medium"), fill=mix(DIM, a), anchor="lm")
    stages = [("D1", [DAY_D1], 0.0), ("H4", DAY_H4, 10.0), ("H1", DAY_H1, 15.5)]
    for k, (tf, bars, ts) in enumerate(stages):
        te = stages[k + 1][2] if k + 1 < len(stages) else 99
        aa = a * min(prog(t, ts, .6), 1 - prog(t, te - .2, .5)) if t >= ts - .01 else 0
        if aa <= 0: continue
        n = len(bars); slot = (x1 - x0) / n; bw = min(slot * .62, 140)
        for i, b in enumerate(bars):
            gi = prog(t, ts + i * (2.2 / n), .4)
            if gi <= 0: continue
            x = x0 + (i + .5) * slot; col = mix(GREEN if b["c"] >= b["o"] else RED, aa * gi)
            d.line([(x, py(b["h"])), (x, py(b["l"]))], fill=col, width=max(3, int(bw * .08)))
            ya, yb = sorted([py(b["o"]), py(b["c"])]); d.rectangle([x - bw / 2, ya, x + bw / 2, max(yb, ya + 3)], fill=col)
        lab = {"D1": "D1 · 1 nến = 1 ngày", "H4": "H4 · 6 nến × 4 giờ", "H1": "H1 · 24 nến × 1 giờ"}[tf]
        pill(d, ((x0 + x1) / 2, y0 + 4), lab, aa, TF_COL[tf], 30, solid=True)
    if t >= 4.5:
        ab = prog(t, 4.5)
        if t < 10: pill(d, (x0 + 210, py(DAY_D1["l"]) + 2), "Đáy 3.426", ab * (1 - prog(t, 9.8, .3)), RED, 24, solid=True)
    if t >= 15.5:
        j = int(np.argmin([b["l"] for b in DAY_H1])); n = 24; slot = (x1 - x0) / n
        circle(d, (x0 + (j + .5) * slot, py(DAY_H1[j]["l"])), 20, RED, prog(t, 16.5))
        pill(d, (x0 + (j + .5) * slot + 26, py(DAY_H1[j]["l"]) + 4), "3.426 · 22h", prog(t, 16.5), RED, 22, anchor="lm", solid=True)

# ---------- timeline ----------
SC = []
def scene(n, du): SC.append((n, du))
scene("intro", 3.2); scene("card1", 2.2); scene("p1", 22.0); scene("card2", 2.2)
TERMS = [("Khung H1 – 1 giờ", "Mỗi nến = **1 giờ**, 24 nến một ngày. **Chi tiết nhất**, nhưng cũng **nhiễu nhất**.", BLUE),
         ("Khung H4 – 4 giờ", "Mỗi nến = **4 giờ**, 6 nến một ngày. **Cân bằng** giữa chi tiết và bức tranh chung.", ORANGE),
         ("Khung D1 – 1 ngày", "Mỗi nến = **1 ngày**. Cho thấy **xu hướng chính** và các vùng giá lớn.", GOLD),
         ("Xung đột khung", "Khi khung nhỏ **đi ngược** khung lớn, đó thường chỉ là **nhịp hồi**.", PURPLE),
         ("Phân tích đa khung (Top-down)", "Đi **từ khung lớn xuống khung nhỏ**: D1 → H4 → H1.", GREEN)]
P2 = [  # (t0, term, caption, timeframe)
    (0.0, 0, None, "H1"), (7.0, 0, "h1a", "H1"), (13.0, 0, "h1b", "H1"),
    (19.0, 1, None, "H4"), (26.0, 1, "h4a", "H4"), (32.0, 1, "h4b", "H4"),
    (38.0, 2, None, "D1"), (45.0, 2, "d1a", "D1"), (51.0, 2, "d1b", "D1"),
    (57.0, 3, None, "D1"), (63.0, 3, "c1", "D1"),
    (69.0, 4, None, "D1"), (75.0, 4, "td1", "D1"), (80.0, 4, "td2", "H4"), (86.0, 4, "td3", "H1"), (92.0, 4, "td4", "H1"),
    (97.0, None, "now1", "D1"), (102.0, None, "now2", "D1")]
P2_DUR = 109.0
scene("p2", P2_DUR); scene("check", 11.0); scene("outro", 4.5)
TOTAL = sum(du for _, du in SC)
CAPS = {
 "h1a": "27/11 trên H1: vàng bật từ **3.556** lên **3.685** chỉ trong khoảng **8 giờ** (8h–16h giờ VN).",
 "h1b": "H1 hợp để **canh điểm vào** cho chính xác, nhưng dễ gặp ~~tín hiệu giả~~ vì nhiều nhiễu.",
 "h4a": "Trên H4: 20/11 đáy **3.504**, 25/11 thủng xuống **3.426** rồi ++bật mạnh++ – **cấu trúc** hiện rõ.",
 "h4b": "H4 dùng để xác định **vùng giá quan trọng** và cấu trúc ngắn hạn.",
 "d1a": "Trên D1: các đỉnh **thấp dần** – 4.217 (12/10), 4.149 (10/11), 3.689 (23/11) → xu hướng chính ~~giảm~~.",
 "d1b": "D1 trả lời câu hỏi quan trọng nhất: **thị trường đang đi về hướng nào?**",
 "c1": "27/11: H1 tăng mạnh, nhưng trên D1 đó chỉ là **một nhịp hồi** trong xu hướng giảm.",
 "td1": "Bước 1 – **D1**: xu hướng chính đang ~~giảm~~, đỉnh sau thấp hơn đỉnh trước.",
 "td2": "Bước 2 – **H4**: vùng cản **3.681–3.689** – đỉnh 23/11, 24/11 và 27/11.",
 "td3": "Bước 3 – **H1**: 27/11 giá chạm vùng cản rồi bị đẩy xuống **3.617**.",
 "td4": "Ví dụ minh họa: **vào lệnh** khi H1 xác nhận (~3.646), **SL** trên vùng cản (~3.695).",
 "now1": "Hiện tại: phiên **27/11** đóng cửa quanh **3.654**.",
 "now2": "D1 vẫn ~~giảm~~, H4 đang hồi từ đáy 3.426, H1 giằng co dưới 3.685 → các khung **chưa đồng thuận**. Chờ xác nhận.",
}
def locate(gt):
    acc = 0
    for n, du in SC:
        if gt < acc + du: return n, gt - acc, du
        acc += du
    return SC[-1][0], SC[-1][1] - 1e-3, SC[-1][1]
def p2_beat(t):
    k = 0
    for i, b in enumerate(P2):
        if t >= b[0]: k = i
    t1 = P2[k + 1][0] if k + 1 < len(P2) else P2_DUR
    return k, t - P2[k][0], t1 - P2[k][0]

# camera per beat: (tf, vs_from, vs_to, nb_from, nb_to)
nH1, nH4, nD1 = len(H1), len(H4), len(D1)
H1_END = nH1 - 2          # bỏ 2 nến sau giờ đóng cửa 27/11
CAMS = {
 0: ("H1", H1_END - 40, H1_END - 40, H1_END - 39, H1_END - 28), 1: ("H1", H1_END - 40, H1_END - 40, H1_END - 28, H1_END - 14), 2: ("H1", H1_END - 40, H1_END - 40, H1_END - 14, H1_END),
 3: ("H4", nH4 - 40, nH4 - 40, nH4 - 39, nH4 - 26), 4: ("H4", nH4 - 40, nH4 - 40, nH4 - 26, nH4), 5: ("H4", nH4 - 40, nH4 - 40, nH4, nH4),
 6: ("D1", nD1 - 40, nD1 - 40, nD1 - 39, nD1 - 22), 7: ("D1", nD1 - 40, nD1 - 40, nD1 - 22, nD1), 8: ("D1", nD1 - 40, nD1 - 40, nD1, nD1),
 9: ("D1", nD1 - 40, nD1 - 40, nD1, nD1), 10: ("D1", nD1 - 40, nD1 - 40, nD1, nD1),
 11: ("D1", nD1 - 40, nD1 - 40, nD1, nD1), 12: ("D1", nD1 - 40, nD1 - 40, nD1, nD1), 13: ("H4", nH4 - 40, nH4 - 40, nH4, nH4),
 14: ("H1", H1_END - 40, H1_END - 40, H1_END - 14, H1_END - 7), 15: ("H1", H1_END - 40, H1_END - 40, H1_END - 7, H1_END),
 16: ("D1", nD1 - 40, nD1 - 40, nD1, nD1), 17: ("D1", nD1 - 40, nD1 - 40, nD1, nD1),
}
# mốc thật
LH = [("12/10", "2026-10-12"), ("10/11", "2026-11-10"), ("23/11", "2026-11-23")]
D1_IDX = {b["t"].date().isoformat(): i for i, b in enumerate(D1)}
H4_LOW20 = min(range(nH4), key=lambda i: H4[i]["l"] if H4[i]["t"].day == 20 else 1e9)
H4_LOW25 = min(range(nH4), key=lambda i: H4[i]["l"])
H1_RALLY0 = idx_of("H1", "2026-11-27T01:00"); H1_TOP27 = idx_of("H1", "2026-11-27T09:00"); H1_LOW27 = idx_of("H1", "2026-11-27T15:00")
H1_ENTRY = idx_of("H1", "2026-11-27T13:00")
RES = (3681.20, 3689.08)

def cam_at(k, tb, bd):
    tf, v0, v1, n0, n1 = CAMS[k]; u = eio(tb / max(bd * .85, .1))
    return Cam(tf, v0 + (v1 - v0) * u, n0 + (n1 - n0) * u)

def p2_layers(k, t):
    zones = []
    if k >= 13 and k <= 15:
        tf = CAMS[k][0]
        i0 = {"H4": next(i for i, b in enumerate(H4) if b["t"] >= H1[idx_of("H1", "2026-11-23T12:00")]["t"]), "H1": H1_END - 40}[tf]
        zones.append(zone_rect(i0, *RES, RED, "VÙNG CẢN 3.681–3.689"))
    return zones

def annotate_p2(d, cam, k, tb, t):
    a = prog(tb, .3)
    if k == 1:
        i0, i1 = H1_RALLY0, H1_TOP27
        if cam.nb > i1:
            p0, p1 = (cam.x(i0), cam.py(H1[i0]["l"])), (cam.x(i1), cam.py(H1[i1]["h"]))
            d.line([p0, p1], fill=mix(GREEN, a), width=5); circle(d, p1, 16, GREEN, a)
            pill(d, (p1[0] - 20, p1[1] - 40), "+129 giá / 8 giờ", a, GREEN, 22, anchor="rm", solid=True)
    if k == 4 and cam.nb > H4_LOW25:
        for i, txt in [(H4_LOW20, "20/11 · 3.504"), (H4_LOW25, "25/11 · 3.426")]:
            p_ = (cam.x(i), cam.py(H4[i]["l"])); circle(d, p_, 18, RED, a); pill(d, (p_[0], p_[1] + 46), txt, a, RED, 22, solid=True)
    if k in (7, 8, 11, 12):
        pts = []
        for j, (lab, iso) in enumerate(LH):
            i = D1_IDX[iso]
            if not cam.vis(i) or cam.nb < i + 1: continue
            p_ = (cam.x(i), cam.py(D1[i]["h"])); pts.append(p_)
            circle(d, p_, 16, RED, prog(tb, .3 + j * .5)); pill(d, (p_[0], p_[1] - 40), f"{lab} · {vn(D1[i]['h'], 0)}", prog(tb, .3 + j * .5), RED, 21, solid=True)
        if len(pts) >= 2:
            u = prog(tb, 1.5, 1.2)
            if u > 0:
                q = pts[0]; r = (pts[0][0] + (pts[-1][0] - pts[0][0]) * u, pts[0][1] + (pts[-1][1] - pts[0][1]) * u)
                d.line([q, r], fill=mix(RED, .9), width=4)
    if k in (9, 10):
        i = nD1 - 1; p_ = (cam.x(i), cam.py(D1[i]["h"]))
        circle(d, (cam.x(i), cam.py((D1[i]["o"] + D1[i]["c"]) / 2)), 28, PURPLE, a)
        pill(d, (p_[0] - 30, p_[1] - 44), "27/11 · nhịp hồi", a, PURPLE, 22, anchor="rm", solid=True)
    if k in (14, 15):
        i = H1_TOP27; p_ = (cam.x(i), cam.py(H1[i]["h"])); circle(d, p_, 16, RED, a)
        if k == 14: pill(d, (p_[0], p_[1] - 70), "Chạm cản 3.685", a, RED, 22, solid=True)
        if cam.nb > H1_LOW27:
            q = (cam.x(H1_LOW27), cam.py(H1[H1_LOW27]["l"])); circle(d, q, 16, GOLD, a)
            pill(d, (q[0], q[1] + 44), "3.617", a, GOLD, 22, solid=True)
    if k == 15:
        ae = prog(tb, .3); xe = cam.x(H1_ENTRY); ent = H1[H1_ENTRY]["c"]; sl = 3695.0
        for val, txt, col in [(ent, f"Entry {vn(ent, 0)}", GOLD), (sl, "SL 3.695", RED)]:
            y_ = cam.py(val); x2 = xe - (xe - cam.x(H1_ENTRY - 7)) * ae
            d.line([(x2, y_), (xe, y_)], fill=mix(col, ae), width=4)
            pill(d, (x2 - 10, y_ + (24 if col == GOLD else -24)), txt, ae, col, 22, anchor="rm", solid=True)
    if k >= 16:
        i = nD1 - 1; y = cam.py(D1[i]["c"]); pill(d, (cam.x(i) - 30, y + 60), "27/11 · 3.654,4", a, GOLD, 24, anchor="rm", solid=True)

def frame(gt):
    name, t, du = locate(gt)
    im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
    if name == "outro":
        a = prog(t, .1, .5)
        logo(d, W / 2 - 85, 560, 170, a); wordmark(d, W / 2, 780, 88, prog(t, .3), anchor="ma")
        d.text((W / 2, 920), "Tập sau: Hỗ trợ & kháng cự", font=F(40, "SemiBold"), fill=mix(WHITE, prog(t, .6)), anchor="mm")
        pill(d, (W / 2, 1040), "Theo dõi để không bỏ lỡ", prog(t, .9), GOLD, 34, solid=True)
        footer(d, gt)
        if t > du - .4: im = Image.blend(Image.new("RGB", (W, H)), im, clamp((du - t) / .4))
        return im
    if name == "intro":
        draw_chart(d, Cam("D1", nD1 - 40, nD1), .22)
        im.paste(Image.blend(im, Image.new("RGB", (W, H), BG), .55)); d = ImageDraw.Draw(im)
        a = prog(t, .1, .5); logo(d, W / 2 - 55, 470, 110, a)
        d.text((W / 2, 640), "TRADER9X MASTERCLASS", font=F(34, "Bold"), fill=mix(GOLD, a), anchor="mm")
        d.text((W / 2, 770), "KHUNG", font=F(150, "Black"), fill=mix(WHITE, prog(t, .3)), anchor="mm")
        d.text((W / 2, 905), "THỜI GIAN", font=F(110, "Black"), fill=mix(WHITE, prog(t, .35)), anchor="mm")
        for j, tf in enumerate(("H1", "H4", "D1")):
            pill(d, (W / 2 - 220 + j * 220, 1040), tf, prog(t, .5 + j * .15), TF_COL[tf], 40, solid=True)
        d.text((W / 2, 1150), "Định nghĩa · Thuật ngữ & Ứng dụng", font=F(40, "SemiBold"), fill=mix(GOLD, prog(t, .8)), anchor="mm")
        d.text((W / 2, 1210), "Ví dụ thật trên Vàng XAU/USD", font=F(32, "Medium"), fill=mix(MUTED, prog(t, .9)), anchor="mm")
        if t > du - .3: im = Image.blend(Image.new("RGB", (W, H), BG), im, clamp((du - t) / .3))
        return im
    if name in ("card1", "p1"):
        header(d, 1, "Khung thời gian là gì?", "Một ngày vàng 25/11 trên 3 khung")
        if name == "p1":
            draw_split(d, t, prog(t, .1))
            caption(d, t, [(.2, 4.5, "**Khung thời gian** (timeframe) là khoảng thời gian mà **mỗi cây nến** gói gọn bên trong."),
                           (4.5, 10.0, "Ngày 25/11 trên **D1** chỉ là **một cây nến**: râu dưới rất dài, đóng cửa gần giá mở."),
                           (10.0, 15.5, "Tách ra **H4**: 6 cây nến, mỗi cây 4 giờ – thấy rõ cú ~~rơi~~ rồi ++bật lên++."),
                           (15.5, 22.0, "Xuống **H1**: 24 cây nến – thấy từng nhịp, đáy **3.426** lúc **22h giờ Việt Nam**.")])
        footer(d, gt)
        if name == "card1": chapter_card(im, t, du, 1); d = ImageDraw.Draw(im); footer(d, gt)
        return im
    if name == "card2":
        draw_chart(d, Cam("H1", H1_END - 40, H1_END - 39)); header(d, 2, *PARTS[2]); footer(d, gt)
        chapter_card(im, t, du, 2); d = ImageDraw.Draw(im); footer(d, gt); return im
    if name == "p2":
        k, tb, bd = p2_beat(t); term, cap, tf = P2[k][1], P2[k][2], P2[k][3]
        cam = cam_at(k, tb, bd)
        # chuyển khung: mờ dần sang khung mới trong 0,5 s đầu nhịp nếu khung đổi
        prev_tf = P2[k - 1][3] if k > 0 else tf
        fade = prog(tb, 0, .5) if prev_tf != tf else 1.0
        draw_chart(d, cam, fade, p2_layers(k, t))
        if fade >= .99: annotate_p2(d, cam, k, tb, t)
        if term is not None: title, sub = TERMS[term][0], f"Thuật ngữ {term + 1}/{len(TERMS)} · khung đang xem: {tf}"
        else: title, sub = "Hiện tại: vàng ~3.654", "Ba khung đang nói gì?"
        header(d, 2, title, sub)
        legend(d, 1, [("H1 = 1 giờ", BLUE), ("H4 = 4 giờ", ORANGE), ("D1 = 1 ngày", GOLD)], PY1 + 34)
        if k >= 12 and k <= 15:
            steps = [("D1", "xu hướng"), ("H4", "vùng giá"), ("H1", "điểm vào")]
            cur = {12: 0, 13: 1, 14: 2, 15: 2}[k]
            for j, (s_tf, lab) in enumerate(steps):
                x = 590 + j * 150; y = 250
                col = TF_COL[s_tf] if j <= cur else DIM
                d.rounded_rectangle([x, y - 4, x + 136, y + 44], 12, fill=PANEL, outline=col, width=3 if j == cur else 2)
                d.text((x + 68, y + 20), f"{j + 1}. {s_tf}", font=F(24, "Bold"), fill=col, anchor="mm")
        if cap is None and term is not None:
            a = min(prog(tb, 0, .35), clamp((bd - tb) / .3)); term_card(d, term, a)
        elif cap: caption(d, tb, [(0.1, bd, CAPS[cap])])
        footer(d, gt); return im
    # check
    draw_chart(d, Cam("D1", nD1 - 40, nD1))
    im.paste(Image.blend(im, Image.new("RGB", (W, H), BG), .78 * prog(t, 0, .4))); d = ImageDraw.Draw(im)
    header(d, 2, "Checklist", "Dùng khung thời gian cho đúng")
    a = prog(t, .2)
    d.rounded_rectangle([40, 300, W - 40, 1400], 26, fill=mix(PANEL, a), outline=mix(GOLD, a), width=3)
    d.text((80, 350), "Dùng khung thời gian hiệu quả", font=F(46, "ExtraBold"), fill=mix(GOLD, a))
    items = ["Bắt đầu từ **khung lớn (D1)** để biết xu hướng",
             "Dùng **H4** tìm vùng giá quan trọng",
             "Dùng **H1** canh điểm vào, không đoán xu hướng",
             "Khung nhỏ **ngược** khung lớn = thường chỉ là nhịp hồi",
             "Vàng biến động mạnh: **luôn đặt Stop Loss**"]
    for i, it in enumerate(items):
        ai = prog(t, .8 + i * .9); y = 470 + i * 180
        d.ellipse([80, y, 130, y + 50], fill=mix(GREEN, ai))
        d.line([(93, y + 26), (103, y + 36), (119, y + 15)], fill=mix(BG, ai, GREEN), width=5)
        rich(d, 160, y + 2, it, F(40, "SemiBold"), W - 240, ai, 52)
    caption(d, t, [(5.6, 11.0, "Không có khung nào đúng nhất. Quan trọng là các khung **đồng thuận** với nhau.")])
    footer(d, gt); return im

def starts():
    acc = 0; out = {}
    for n, du in SC: out[n] = acc; acc += du
    return out
def render(out, t0, t1):
    p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", out + ".tmp.mp4"], stdin=subprocess.PIPE)
    for i in range(int(round(t0 * FPS)), int(round(t1 * FPS))): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close()
    if p.wait() == 0: os.rename(out + ".tmp.mp4", out)
if __name__ == "__main__":
    if sys.argv[1] == "still":
        ts = [float(x) for x in sys.argv[2:]]; ims = [frame(t) for t in ts]
        sh = Image.new("RGB", (432 * len(ims), 768))
        for i, m in enumerate(ims): sh.paste(m.resize((432, 768)), (i * 432, 0))
        sh.save("stills.jpg", quality=85)
    elif sys.argv[1] == "info": print(TOTAL, starts())
    else: render(sys.argv[2], float(sys.argv[3]), float(sys.argv[4]))
