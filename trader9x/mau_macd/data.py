import numpy as np
def ema(x, n):
    a = 2 / (n + 1); out = np.zeros_like(x); out[0] = x[0]
    for i in range(1, len(x)): out[i] = a * x[i] + (1 - a) * out[i - 1]
    return out
# MetalCharts XAU/USD daily (US dates, weekdays only)
ALL = [("20/10", 4141.76, 4155.90, 4111.84, 4120.80), ("21/10", 4120.72, 4142.03, 4106.88, 4134.54), ("22/10", 4134.23, 4142.67, 4020.92, 4026.14),
       ("23/10", 4026.45, 4034.68, 3975.83, 4000.88), ("26/10", 3993.57, 4029.98, 3977.58, 4013.44), ("27/10", 4013.57, 4065.54, 3988.99, 4062.29),
       ("28/10", 4061.98, 4070.81, 4028.01, 4070.21), ("29/10", 4068.99, 4081.97, 4006.15, 4022.12), ("30/10", 4022.30, 4030.80, 3871.19, 3883.59),
       ("02/11", 3875.35, 3969.99, 3866.02, 3944.31), ("03/11", 3942.99, 3969.20, 3896.21, 3919.20), ("04/11", 3919.75, 4070.46, 3917.42, 4058.02),
       ("05/11", 4057.70, 4147.60, 4056.94, 4114.40), ("06/11", 4113.99, 4115.82, 4028.59, 4063.33), ("09/11", 4065.98, 4138.39, 4054.86, 4134.03),
       ("10/11", 4133.40, 4149.01, 4013.81, 4030.42), ("11/11", 4030.25, 4066.53, 3982.17, 3987.03), ("12/11", 3986.93, 4000.94, 3853.27, 3883.66),
       ("13/11", 3883.75, 3923.92, 3868.62, 3875.68)]
HID_DAYS = 4          # 20/10–23/10 hidden warm-up (real), display starts 26/10
PER = 6
def day_path(o, h, l, c, rng):
    if c >= o: wp = [o, l, (l + h) / 2, h - (h - c) * .3, h, c]
    else: wp = [o, h, (h + l) / 2, l + (c - l) * .4, l, c]
    xs = np.linspace(0, PER, len(wp)); t = np.arange(PER + 1)
    pts = np.clip(np.interp(t, xs, wp) + np.r_[0, rng.normal(0, (h - l) * .04, PER - 1), 0], l, h)
    b = []
    for i in range(PER):
        bo, bc = pts[i], pts[i + 1]
        b.append([bo, max(bo, bc) + abs(rng.normal(0, (h - l) * .03)), min(bo, bc) - abs(rng.normal(0, (h - l) * .03)), bc])
    b = np.array(b)
    b[np.argmax(b[:, 1]), 1] = h; b[np.argmin(b[:, 2]), 2] = l
    b[:, 1] = np.minimum(b[:, 1], h); b[:, 2] = np.maximum(b[:, 2], l)
    b[:, 1] = np.maximum(b[:, 1], b[:, [0, 3]].max(1)); b[:, 2] = np.minimum(b[:, 2], b[:, [0, 3]].min(1))
    return b
def build(seed=1, slope=0.0):
    rng = np.random.default_rng(seed)
    WU = 60
    c = np.linspace(4140 - slope, 4140, WU) + np.cumsum(rng.normal(0, 3, WU)); c += np.linspace(0, 4141.76 - c[-1], WU)
    warm = []; prev = c[0]
    for x in c:
        warm.append([prev, max(prev, x) + abs(rng.normal(0, 5)), min(prev, x) - abs(rng.normal(0, 5)), x]); prev = x
    days = np.vstack([day_path(*d[1:], rng) for d in ALL])
    allb = np.vstack([np.array(warm), days]); cl = allb[:, 3]
    e12, e26 = ema(cl, 12), ema(cl, 26); m = e12 - e26; s = ema(m, 9)
    sl = slice(WU + HID_DAYS * PER, None)
    return dict(o=allb[sl, 0], h=allb[sl, 1], l=allb[sl, 2], c=allb[sl, 3], e12=e12[sl], e26=e26[sl], macd=m[sl], sig=s[sl], hist=(m - s)[sl],
                days=[d[0] for d in ALL[HID_DAYS:]])
def signals(D):
    m, s = D["macd"], D["sig"]; N = len(m)
    cr = [(i, "up" if m[i] > s[i] else "dn") for i in range(1, N) if (m[i-1]-s[i-1])*(m[i]-s[i]) < 0]
    z = [(i, "up" if m[i] > 0 else "dn") for i in range(1, N) if m[i-1]*m[i] < 0]
    return cr, z
if __name__ == "__main__":
    D = build(); cr, z = signals(D); N = len(D["c"])
    print("N", N, "days", D["days"])
    print("cross", [(i, d, D["days"][i//6]) for i, d in cr]); print("zero", [(i, d, D["days"][i//6]) for i, d in z])
    print("macd by day end", [round(D["macd"][i],1) for i in range(5, N, 6)])
