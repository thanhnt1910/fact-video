"""Tiếng hiệu ứng cho video dọc 9:16 (tổng hợp bằng numpy, không cần file ngoài).
Sự kiện lấy từ trang dựng: window.SFX = [[giây, loại, tham số]]. Mỗi loại ứng với một hiệu ứng trên bản đồ.
Quy ước mức: đỉnh mỗi tiếng khoảng -3 dBFS (mức thực do sidechain quyết định) trở xuống; khi trộn, dùng sidechain để TỰ HẠ khi có giọng đọc."""
import numpy as np, wave
SR = 44100
rng = np.random.default_rng(7)
def fit(y,n):
    y=np.asarray(y)[:n]; return np.pad(y,(0,n-len(y)))
def t_(d): return np.arange(int(d * SR)) / SR
def env(n, a=.005, r=.1):
    e = np.ones(n); na = max(1, int(a * SR)); nr = max(1, int(r * SR)); e[:na] = np.linspace(0, 1, na); e[-nr:] = np.minimum(e[-nr:], np.linspace(1, 0, nr)); return e
def lp(x, fc):
    a = np.exp(-2 * np.pi * fc / SR); y = np.zeros_like(x); s = 0.0
    for i, v in enumerate(x): s = (1 - a) * v + a * s; y[i] = s
    return y
def bp(x, lo, hi): return lp(x, hi) - lp(x, lo)
def noise(d): return rng.standard_normal(int(d * SR))
def pop(f=520, d=.22, g=1.0):
    t = t_(d); return g * np.sin(2 * np.pi * (f + 90 * np.exp(-t * 30)) * t) * np.exp(-t * 16)
def tit(f=1900, g=.7):
    # hai tiếng bíp ngắn 'tít tít'
    out = np.zeros(int(.2 * SR)); t = t_(.055)
    for k, st in enumerate((0, .09)):
        b = g * np.sin(2 * np.pi * f * t) * env(len(t), .004, .02); i = int(st * SR); out[i:i + len(b)] += b
    return out
def ping(f=760, d=.55, g=.8):
    t = t_(d); return g * (np.sin(2 * np.pi * f * t) + .35 * np.sin(2 * np.pi * f * 2.01 * t)) * np.exp(-t * 7)
def chime(f=660, d=.9, g=.8):
    t = t_(d); return g * (np.sin(2 * np.pi * f * t) * np.exp(-t * 4.5) + .6 * np.sin(2 * np.pi * f * 1.5 * t) * np.exp(-t * 5.5) + .3 * np.sin(2 * np.pi * f * 2 * t) * np.exp(-t * 7))
def thud(f=70, d=.28, g=1.0):
    t = t_(d); n = bp(noise(d), 60, 420) * 6; return g * (np.sin(2 * np.pi * (f + 40 * np.exp(-t * 28)) * t) * np.exp(-t * 14) + .25 * n * np.exp(-t * 40))
def stamp(g=1.0):
    n = int(.4 * SR); return fit(thud(55, .4, g), n) + fit(bp(noise(.05), 800, 3000) * np.exp(-t_(.05) * 70) * 5, n) * .6
def whoosh(d=.8, lo=300, hi=2800, g=.7, up=True):
    n = noise(d); y = bp(n, lo, hi) * 4; t = np.linspace(0, 1, len(y)); e = np.sin(np.pi * t) ** 2 if up else (1 - t) ** 2; return g * y * e
def flag(g=1.0):
    n = int(.45 * SR); return fit(whoosh(.45, 600, 3500, .8), n) + fit(np.pad(bp(noise(.04), 1500, 5000) * np.exp(-t_(.04) * 90) * 6, (int(.4 * SR), 0)), n) * .5
def coin(g=.8):
    t = t_(.16); return g * (np.sin(2 * np.pi * 2300 * t) * np.exp(-t * 28) + .7 * np.sin(2 * np.pi * 3100 * t) * np.exp(-t * 24))
def question(g=.8):
    t = t_(.55); f = 360 + 260 * np.clip(t / .35, 0, 1) ** 2; ph = 2 * np.pi * np.cumsum(f) / SR; return g * np.sin(ph) * env(len(t), .02, .25) * .7
def step(g=.9):
    t = t_(.07); return g * bp(noise(.07), 120, 900) * 14 * np.exp(-t * 55)
def murmur(d=3.0, g=.6):
    n = bp(noise(d), 180, 900) * 5; m = 1 + .5 * np.sin(2 * np.pi * np.arange(len(n)) / SR * 5.3); return g * n * m * env(len(n), d * .4, d * .4)
def swell(d=1.6, g=.5):
    t = t_(d); y = (np.sin(2 * np.pi * 110 * t) + .6 * np.sin(2 * np.pi * 165 * t)) * np.sin(np.pi * t / d) ** 2; return g * y
def boom(g=1.0, light=False, rustle=.25):
    """Cú boom trầm kiểu video mẫu: sóng 45->35 Hz lên 50 ms tắt ~300 ms (+ thân 90-130 Hz để loa điện thoại vẫn nghe), tiếng giấy quét báo trước, tiếng tách đúng lúc đập."""
    if light: rustle = min(rustle, .12)
    pre = int(rustle * SR); d = .5; t = t_(d)
    ph = 2 * np.pi * np.cumsum(35 + 10 * np.exp(-t * 8)) / SR
    a = np.minimum(1, t / .05) * np.exp(-t * 7.7)
    low = np.sin(ph) * a * (0 if light else 1)
    body = (np.sin(2 * np.pi * (95 + 45 * np.exp(-t * 20)) * t) * np.exp(-t * (13 if light else 9)) * np.minimum(1, t / .012))
    clk = np.pad(bp(noise(.02), 2500, 7000) * np.exp(-t_(.02) * 160) * 10, (0, int((d - .02) * SR)))
    hit = (low * 1.0 + body * (.75 if not light else .9)) * 1.0 + clk * .35
    ru = bp(noise(rustle), 3500, 9000) * 6 * (np.linspace(0, 1, int(rustle * SR)) ** 2) * (.5 if not light else .35)
    y = np.concatenate([ru[:pre], np.zeros(len(hit))]); y[pre:pre + len(hit)] += hit
    return g * (.55 if light else 1.0) * y, pre / SR

def rip(g=1.0):
    """Tiếng vải/giấy xé: nhiễu dải cao, vài nhịp sột soạt."""
    d=.55; n=bp(noise(d),1500,7500)*6; t=np.linspace(0,1,len(n)); e=(np.abs(np.sin(t*40))*.6+.4)*np.exp(-t*2.2)*np.minimum(1,t/.02); return g*n*e
def morse(g=1.0, pat='... --- ...', f=700):
    """Tín hiệu Morse: chấm 70 ms, gạch 210 ms."""
    out=[]
    for ch in pat:
        if ch==' ': out.append(np.zeros(int(.14*SR))); continue
        d=.07 if ch=='.' else .21; t=t_(d); out.append(np.sin(2*np.pi*f*t)*env(len(t),.004,.01)*.8); out.append(np.zeros(int(.07*SR)))
    return g*np.concatenate(out)
def blast(g=1.0):
    """Vụ nổ: thump sâu + nhiễu rền tắt dần."""
    d=1.6; t=t_(d); lo=np.sin(2*np.pi*(48+60*np.exp(-t*9))*t)*np.exp(-t*3.2)*np.minimum(1,t/.006)
    nz=bp(noise(d),80,2500)*7*np.exp(-t*4.5)*np.minimum(1,t/.004); cr=bp(noise(.08),2000,8000)*np.exp(-t_(.08)*60)*8
    y=lo*1.0+nz*.55; y[:len(cr)]+=cr*.5; return g*y
def dig(g=1.0):
    """Cuốc xẻng chạm đất: tiếng thịch ngắn + hạt đất lạo xạo."""
    t=t_(.3); th=np.sin(2*np.pi*(95+50*np.exp(-t*30))*t)*np.exp(-t*20); gr=bp(noise(.3),600,3500)*5*np.exp(-t*14)*np.minimum(1,t/.01); return g*(th*.9+gr*.5)
def clink(g=1.0):
    """Gõ vào đất nung: tiếng cạch khô."""
    t=t_(.22); return g*((np.sin(2*np.pi*1450*t)*.6+np.sin(2*np.pi*2380*t)*.4)*np.exp(-t*26)+bp(noise(.22),1500,6000)*3*np.exp(-t*60))
def creak(g=1.0, d=1.1):
    """Dây thừng/ròng rọc kẹt kẹt: dao động thấp cộng nhiễu dải giữa."""
    t=t_(d); f=210+35*np.sin(2*np.pi*3.5*t); ph=2*np.pi*np.cumsum(f)/SR; y=(np.sign(np.sin(ph))*.25+np.sin(ph)*.4)*(.55+.45*np.sin(2*np.pi*7*t)**2)
    y=lp(y,1800)+bp(noise(d),900,2600)*1.2*np.abs(np.sin(2*np.pi*3.5*t)); return g*y*env(len(t),.05,.25)*.8
def wind(g=1.0, d=2.4):
    """Gió thổi: nhiễu dải thấp lên rồi xuống."""
    n=bp(noise(d),150,1400)*6; t=np.linspace(0,1,len(n)); return g*n*(np.sin(np.pi*t)**1.5)*(.8+.2*np.sin(2*np.pi*1.7*t*d))
def paper(g=1.0):
    """Giấy sột soạt / đặt thư xuống."""
    d=.35; n=bp(noise(d),2000,9000)*5; t=np.linspace(0,1,len(n)); return g*n*np.exp(-t*3)*(.6+.4*np.abs(np.sin(t*28)))*np.minimum(1,t/.02)
def hammer(g=1.0):
    """Búa gõ kim loại."""
    t=t_(.4); return g*((np.sin(2*np.pi*880*t)*.5+np.sin(2*np.pi*1320*t)*.35+np.sin(2*np.pi*2050*t)*.2)*np.exp(-t*12)+bp(noise(.4),1500,7000)*2.5*np.exp(-t*70))
def siren(g=1.0, d=2.0):
    """Còi hụ lên xuống chậm (còi thành phố)."""
    t=t_(d); f=420+260*np.sin(np.pi*np.clip(t/(d*.55),0,1))**2*(t<d*.55)+ (t>=d*.55)*(420+260*np.exp(-(t-d*.55)*3)); ph=2*np.pi*np.cumsum(f)/SR
    return g*(np.sin(ph)*.7+np.sin(2*ph)*.2)*env(len(t),.15,.5)*.8
def anthem(g=1.0, d=3.0):
    """Hợp âm kèn đồng dài (tiếng nhạc nền lễ), không phải giai điệu có bản quyền."""
    t=t_(d); y=(np.sin(2*np.pi*196*t)+.6*np.sin(2*np.pi*247*t)+.5*np.sin(2*np.pi*294*t)+.25*np.sin(2*np.pi*392*t)); return g*y*env(len(t),.4,.9)*.35
def render(events, total):
    out = np.zeros(int(total * SR) + SR * 3)
    def put(t, y):
        i = int(t * SR); y = np.asarray(y)
        if i < 0 or i >= len(out): return
        j = min(len(out), i + len(y)); out[i:j] += y[:j - i]
    for ev in events:
        t, k = ev[0], ev[1]; p = ev[2] if len(ev) > 2 else {}
        g = p.get('g', 1.0)
        if k == 'pop': put(t, pop(p.get('f', 520), g=g))
        elif k == 'tit': put(t, tit(p.get('f', 1900), g * .7))
        elif k == 'ping': put(t, ping(p.get('f', 760), g=g))
        elif k == 'chime': put(t, chime(p.get('f', 660), g=g))
        elif k == 'boom':
            y, off = boom(g, p.get('light', False), p.get('rustle', .25)); put(max(0, t - off), y)
        elif k == 'thud': put(t, thud(p.get('f', 70), g=g))
        elif k == 'stamp': put(t, stamp(g))
        elif k == 'whoosh': put(t, whoosh(p.get('d', .8), g=.7 * g))
        elif k == 'flag': put(t, flag(g))
        elif k == 'coin': put(t, coin(.8 * g))
        elif k == 'question': put(t, question(g))
        elif k == 'steps':
            n = int(p.get('n', 6)); dt = p.get('dt', .42)
            for i in range(n): put(t + i * dt + (.05 if i % 2 else 0), step(g * (.85 if i % 2 else 1)))
        elif k == 'murmur': put(t, murmur(p.get('d', 3.0), .6 * g))
        elif k == 'swell': put(t, swell(p.get('d', 1.6), .5 * g))
        elif k == 'rip': put(t, rip(g))
        elif k == 'morse': put(t, morse(g, p.get('pat','... --- ...'), p.get('f',700)))
        elif k == 'blast': put(t, blast(g))
        elif k == 'dig': put(t, dig(g))
        elif k == 'clink': put(t, clink(g))
        elif k == 'creak': put(t, creak(g, p.get('d',1.1)))
        elif k == 'wind': put(t, wind(.7*g, p.get('d',2.4)))
        elif k == 'paper': put(t, paper(g))
        elif k == 'hammer': put(t, hammer(g))
        elif k == 'siren': put(t, siren(.8*g, p.get('d',2.0)))
        elif k == 'anthem': put(t, anthem(g, p.get('d',3.0)))
    pk = np.abs(out).max() or 1; out = out / pk * (10 ** (-3 / 20))   # đỉnh -3 dBFS (còn bị sidechain hạ thêm khi có giọng)
    return out
def write(path, mono, total):
    n = int(total * SR); y = np.zeros(n); m = min(n, len(mono)); y[:m] = mono[:m]
    st = np.stack([y, y], 1); a = (np.clip(st, -1, 1) * 32767).astype('<i2')
    with wave.open(path, 'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(a.tobytes())
