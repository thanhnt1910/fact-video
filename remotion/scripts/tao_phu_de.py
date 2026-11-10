#!/usr/bin/env python3
"""Tính mốc phụ đề cụm ngắn (tối đa 4 từ) theo giọng đọc thật.
Dùng: python3 scripts/tao_phu_de.py beats.json ../demo/era/leda src/eratosthenes/caps.json
Mỗi câu: tìm đoạn có tiếng / đoạn lặng trong file wav, trọng số từng từ = số âm tiết ước lượng,
chia thời gian chỉ trên phần có tiếng nên chỗ ngắt nghỉ không làm lệch các cụm sau."""
import json, re, subprocess, sys
import numpy as np
from scipy.io import wavfile

beats = json.load(open(sys.argv[1]))['beats']
folder = sys.argv[2]
OFF = 0.15  # giọng bắt đầu sau đầu nhịp 0,15 giây (trùng với bước ghép âm thanh)

def syll(w):
    w = re.sub(r'[^\wÀ-ỹ]', '', w.replace('*', '').lower())
    if re.fullmatch(r'[a-z]+', w) and len(w) > 3:  # từ nước ngoài: đếm cụm nguyên âm
        return max(1, len(re.findall(r'[aeiouy]+', w)))
    return 1

def speech_intervals(f):
    sr, x = wavfile.read(f); x = x.astype(float) / 32768
    if x.ndim > 1: x = x[:, 0]
    h = int(sr * 0.01); n = len(x) // h
    e = np.sqrt((x[:n * h].reshape(n, h) ** 2).mean(1)) + 1e-9
    db = 20 * np.log10(e); on = db > (db.max() - 38)
    # lấp chỗ lặng ngắn hơn 90 ms
    i = 0
    while i < n:
        if not on[i]:
            j = i
            while j < n and not on[j]: j += 1
            if 0 < i and j < n and (j - i) < 9: on[i:j] = True
            i = j
        else: i += 1
    iv, i = [], 0
    while i < n:
        if on[i]:
            j = i
            while j < n and on[j]: j += 1
            iv.append((i * 0.01, j * 0.01)); i = j
        else: i += 1
    return iv, n * 0.01

def mark_words(text):
    """Từ khóa nằm trong *...* (có thể nhiều từ, dấu câu đi ngay sau dấu * đóng): gắn dấu * riêng cho từng từ."""
    out, on = [], False
    for tok in text.split(' '):
        if not tok: continue
        opens = tok.startswith('*')
        core = tok[1:] if opens else tok
        if opens: on = True
        closes = '*' in core
        core = core.replace('*', '')
        m = re.match(r'^(.*?)([,.;:?!]*)$', core)
        word, suf = m.group(1), m.group(2)
        out.append(('*%s*%s' % (word, suf)) if on and word else core)
        if closes: on = False
    return ' '.join(out)

def chunks(text, mx=4):
    out = []
    text = mark_words(text) if '*' in text else text
    for part in re.split(r'(?<=[,.;:?!])\s+', text.strip()):
        w = part.split()
        if not w: continue
        k = -(-len(w) // mx); i = 0
        for a in range(k):
            t = round((len(w) - i) / (k - a)); out.append(w[i:i + t]); i += t
    return out

res = []
for bi, b in enumerate(beats):
    iv, total = speech_intervals('%s/%02d.wav' % (folder, bi + 1))
    cum = np.cumsum([0] + [e - s for s, e in iv]); sp = cum[-1]
    def real(u):  # thời gian có tiếng -> thời gian thật
        for k, (s, e) in enumerate(iv):
            if u <= cum[k + 1] + 1e-9: return s + (u - cum[k])
        return iv[-1][1]
    ch = chunks(b['text'])
    # Phụ đề có chữ số (1774, 5,5...) nhưng giọng đọc thành chữ: trọng số của số = phần âm tiết còn lại của bản đọc
    # Phụ đề có chữ số (1774, 5,5...) nhưng giọng đọc thành chữ: ước lượng số âm tiết khi đọc số.
    # (Trước đây dồn toàn bộ âm tiết thừa của bản đọc vào chữ số, nên khi phụ đề rút gọn thì cụm có số đứng 4–5 giây.)
    def numw(w):
        d = len(re.sub(r'\D', '', w))
        if d == 0: return 1  # ký hiệu ÷ × = + ≈ đọc thành một tiếng
        return {1: 1, 2: 3, 3: 5, 4: 6}.get(d, d + 2) + (1 if ',' in w else 0) + (2 if '%' in w else 0)
    wts = [sum(numw(w) if re.search(r'[\d÷×=+≈]', w) else syll(w) for w in c) for c in ch]
    tw = sum(wts)
    acc, items = 0, []
    for c, w in zip(ch, wts):
        items.append({'text': ' '.join(c), 'start': round(OFF + real(sp * acc / tw), 3)})
        acc += w
    for k, it in enumerate(items):
        it['end'] = items[k + 1]['start'] if k + 1 < len(items) else round(OFF + iv[-1][1] + 0.12, 3)
    res.append(items)
json.dump(res, open(sys.argv[3], 'w'), ensure_ascii=False, indent=1)
print(sum(len(r) for r in res), 'cụm')
