"""Bản nhẹ của dungban.py: cắt vùng Bắc Bộ – Quảng Tây, bỏ đảo li ti, đơn giản hóa đường bờ (Douglas–Peucker 0,35 px) -> geo_nhe.js
(đường bờ 1,3 MB làm mỗi khung hình mất 1,3 giây; bản nhẹ để dựng cả video)."""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LON0, LON1, LAT0, LAT1 = 100.0, 115.0, 17.5, 26.5
W, H = 3600, 2160
K = math.cos(math.radians(22))
S = min(W / ((LON1 - LON0) * K), H / (LAT1 - LAT0))


def proj(lon, lat):
    return ((lon - LON0) * K * S, (LAT1 - lat) * S)


def dp(pts, eps):
    if len(pts) < 3:
        return pts
    keep = [False] * len(pts)
    keep[0] = keep[-1] = True
    st = [(0, len(pts) - 1)]
    while st:
        a, b = st.pop()
        ax, ay = pts[a]
        bx, by = pts[b]
        dx, dy = bx - ax, by - ay
        L = math.hypot(dx, dy) or 1e-9
        md, mi = -1.0, -1
        for i in range(a + 1, b):
            d = abs(dy * (pts[i][0] - ax) - dx * (pts[i][1] - ay)) / L
            if d > md:
                md, mi = d, i
        if md > eps:
            keep[mi] = True
            st.append((a, mi))
            st.append((mi, b))
    return [p for p, k in zip(pts, keep) if k]


def main():
    d = json.load(open(ROOT / "assets/ten_duong/ne_10m_land.json"))
    rings, n0, n1 = [], 0, 0
    for f in d["features"]:
        g = f["geometry"]
        polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        for poly in polys:
            for ring in poly:
                xs = [p[0] for p in ring]
                ys = [p[1] for p in ring]
                if max(xs) < 101.5 or min(xs) > 114 or max(ys) < 18 or min(ys) > 26.2:
                    continue
                pts = [proj(x, y) for x, y in ring]
                n0 += len(pts)
                area = abs(sum(pts[i][0] * pts[i - 1][1] - pts[i - 1][0] * pts[i][1] for i in range(len(pts)))) / 2
                if area < 4:
                    continue
                h = len(pts) // 2
                q = dp(pts[:h + 1], 5)[:-1] + dp(pts[h:], 5)
                if len(q) < 4:
                    continue
                n1 += len(q)
                rings.append("M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in q) + "Z")
    out = {"land": " ".join(rings), "scale": S, "lon0": LON0, "lat1": LAT1, "k": K, "w": W, "h": H}
    (ROOT / "phim_ban_do/vecmap/geo_nhe.js").write_text("window.GEO=" + json.dumps(out) + ";", encoding="utf-8")
    print(n0, "->", n1, "điểm;", len(rings), "vòng;", len(out["land"]) // 1024, "KB")


main()
