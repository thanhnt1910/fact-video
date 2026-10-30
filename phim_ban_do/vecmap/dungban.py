"""Bản đồ vector MỚI (không dùng mapfilm3): cắt đất liền Natural Earth quanh Việt Nam – Quảng Tây, xuất ra
phim_ban_do/vecmap/geo.js (đường bờ biển đã chiếu sang tọa độ màn hình). Chạy: python phim_ban_do/vecmap/dungban.py
Cửa sổ: kinh độ 101–114, vĩ độ 18–26; chiếu phẳng có hiệu chỉnh cos(vĩ độ giữa)."""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LON0, LON1, LAT0, LAT1 = 100.0, 115.0, 17.5, 26.5
W, H = 3600, 2160          # khung thế giới: có thể phóng to khi quay máy
K = math.cos(math.radians(22))


def proj(lon, lat):
    sx = W / ((LON1 - LON0) * K)
    sy = H / (LAT1 - LAT0)
    s = min(sx, sy)
    return ((lon - LON0) * K * s, (LAT1 - lat) * s)


def main():
    d = json.load(open(ROOT / "assets/ten_duong/ne_10m_land.json"))
    rings = []
    for f in d["features"]:
        g = f["geometry"]
        polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        for poly in polys:
            for ring in poly:
                xs = [p[0] for p in ring]
                ys = [p[1] for p in ring]
                if max(xs) < LON0 or min(xs) > LON1 or max(ys) < LAT0 or min(ys) > LAT1:
                    continue
                pts = [proj(x, y) for x, y in ring]
                rings.append("M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + "Z")
    sx = W / ((LON1 - LON0) * K)
    sy = H / (LAT1 - LAT0)
    s = min(sx, sy)
    out = {"land": " ".join(rings), "scale": s, "lon0": LON0, "lat1": LAT1, "k": K, "w": W, "h": H}
    (ROOT / "phim_ban_do/vecmap/geo.js").write_text("window.GEO=" + json.dumps(out) + ";", encoding="utf-8")
    print("vòng đất:", len(rings), "| kích thước:", len(out["land"]) // 1024, "KB | s =", round(s, 1))


if __name__ == "__main__":
    main()
