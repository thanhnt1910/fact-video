"""Dữ liệu thật 3 khung: D1 (MetalCharts daily), H1 (MetalCharts hourly), H4 gộp từ H1.
Phiên ngày MetalCharts: 20:00 UTC hôm trước → 19:59 UTC. Nhãn giờ hiển thị theo giờ Việt Nam (UTC+7)."""
import csv
from datetime import datetime, timedelta
VN = timedelta(hours=7)
def _f(r): return [float(r[k]) for k in ("open", "high", "low", "close")]
def load_d1():
    rows = list(csv.DictReader(open(__file__.rsplit("/", 1)[0] + "/d1.csv")))
    return [dict(t=datetime.fromisoformat(r["date"]), o=_f(r)[0], h=_f(r)[1], l=_f(r)[2], c=_f(r)[3]) for r in rows]
def load_h1():
    rows = list(csv.DictReader(open(__file__.rsplit("/", 1)[0] + "/h1.csv")))
    out = []
    for r in rows:
        t = datetime.fromisoformat(r["time_utc"].replace("Z", ""))
        o, h, l, c = _f(r); out.append(dict(t=t, o=o, h=h, l=l, c=c))
    return out
def agg(bars):
    return dict(t=bars[0]["t"], o=bars[0]["o"], h=max(b["h"] for b in bars), l=min(b["l"] for b in bars), c=bars[-1]["c"], n=len(bars))
def to_h4(h1):
    """Gộp theo ô 4 giờ neo vào 20:00 UTC (20,00,04,08,12,16) – khớp phiên ngày."""
    groups = {}
    for b in h1:
        k = b["t"] - timedelta(hours=(b["t"].hour - 20) % 4, minutes=b["t"].minute)
        groups.setdefault(k, []).append(b)
    return [agg(groups[k]) for k in sorted(groups)]
def session_day(t):  # ngày phiên MetalCharts của một nến giờ
    return (t + timedelta(hours=4)).date()
def to_d1(h1):
    g = {}
    for b in h1: g.setdefault(session_day(b["t"]), []).append(b)
    return {k: agg(v) for k, v in g.items()}
D1, H1 = load_d1(), load_h1()
H4 = to_h4(H1)
if __name__ == "__main__":
    print("D1", len(D1), "H1", len(H1), "H4", len(H4))
    dd = {b["t"].date(): b for b in D1}
    for k, a in sorted(to_d1(H1).items()):
        if k in dd:
            b = dd[k]; print(k, "n", a["n"], "| O", round(a["o"],2), b["o"], "H", a["h"], b["h"], "L", a["l"], b["l"], "C", a["c"], b["c"])
        else: print(k, "(không có dòng ngày)", a["n"])
