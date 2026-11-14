#!/usr/bin/env python3
"""Đọc giọng cho video 3D: TỪNG ĐOẠN một lần gọi Gemini (cum = 1, theo quy tắc kênh), kiểm bằng nhận dạng, chuẩn hóa.

  python video3d/doc_giong.py doc   <loi_doc.json> <giọng> <thư mục>   # đọc các đoạn còn thiếu
  python video3d/doc_giong.py kiem  <loi_doc.json> <thư mục> [ngưỡng]  # nhận dạng (faster-whisper), xóa đoạn khớp dưới ngưỡng
  python video3d/doc_giong.py chuan <loi_doc.json> <thư mục>           # loudnorm -16 + chỉnh nhịp 0,90–1,10 -> <thư mục>/chuan

Chạy từ gốc repo (cần gemini_tts.py, gemini_keys.py, audio_fx.py). Kết quả: <thư mục>/<n>.mp3, thoi_luong.json, kiem.json.
"""
import difflib, io, json, os, re, subprocess, sys, wave
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

STYLE = ("Native Vietnamese narrator, Northern accent (Hanoi), for a calm historical documentary about Vietnam's first "
         "university. Warm, respectful, unhurried storytelling pace with natural short pauses between phrases; clear "
         "diction and correct Vietnamese tones; read numbers and years exactly as written in words. Never robotic, "
         "never rushed, never news-anchor flat. Read the text exactly, word for word, nothing added.")


DV = ['không', 'một', 'hai', 'ba', 'bốn', 'năm', 'sáu', 'bảy', 'tám', 'chín']


def _ba(n, day):   # đọc 0..999; day = có nhóm đứng trước (đọc đủ "không trăm", "linh")
    tr, ch, dv = n // 100, n // 10 % 10, n % 10; o = []
    if tr or day: o += [DV[tr], 'trăm']
    if ch > 1: o += [DV[ch], 'mươi']
    elif ch == 1: o += ['mười']
    elif dv and (tr or day): o += ['linh']
    if dv: o += ['mốt' if dv == 1 and ch > 1 else 'lăm' if dv == 5 and ch >= 1 else 'tư' if dv == 4 and ch > 1 else DV[dv]]
    return o


def so_thanh_chu(n):
    """Đọc số nguyên kiểu Bắc bộ, để so lời nhận dạng (hay ra chữ số) với kịch bản (viết bằng chữ)."""
    if n == 0: return ['không']
    nhom = []
    while n: nhom.append(n % 1000); n //= 1000
    ten = ['', 'nghìn', 'triệu', 'tỷ']; o = []
    for i in range(len(nhom) - 1, -1, -1):
        g = nhom[i]
        if g == 0: continue
        o += _ba(g, bool(o)) + ([ten[i]] if ten[i] else [])
    return o


DONG_NGHIA = {'lẻ': 'linh', 'nghìn': 'nghìn', 'ngàn': 'nghìn', 'bẩy': 'bảy', 'tư': 'bốn', 'mốt': 'một', 'lăm': 'năm', 'nhăm': 'năm', 'm2': 'mét vuông'}


def am(w):
    """Bỏ dấu thanh và gộp các phụ âm Whisper hay nhầm với giọng Bắc (d/gi/r, tr/ch, s/x, l/n)."""
    import unicodedata
    w = ''.join(c for c in unicodedata.normalize('NFD', w) if unicodedata.category(c) != 'Mn').replace('đ', 'd')
    for a_, b_ in (('ngh', 'ng'), ('gh', 'g'), ('gi', 'z'), ('tr', 'c'), ('ch', 'c'), ('k', 'c'), ('q', 'c')):
        if w.startswith(a_): w = b_ + w[len(a_):]; break
    if w[:1] in ('d', 'r'): w = 'z' + w[1:]
    if w[:1] == 's': w = 'x' + w[1:]
    if w[:1] == 'n' and not w.startswith('ng') and not w.startswith('nh'): w = 'l' + w[1:]
    return w


def khop(text, asr):
    """Tỉ lệ khớp theo âm (bỏ thanh), và tỉ lệ số tiếng nhận dạng / kịch bản (bắt bỏ câu, đọc lặp)."""
    a, b = [am(w) for w in tieng(text)], [am(w) for w in tieng(asr)]
    return difflib.SequenceMatcher(None, a, b).ratio(), len(b) / max(1, len(a))


def tieng(t):
    t = t.lower().replace('m²', ' mét vuông')
    t = re.sub(r"(\d)[.,](\d{3})\b", r"\1\2", t); t = re.sub(r"(\d)[.,](\d{3})\b", r"\1\2", t)
    t = re.sub(r"(\d+)\s*m2\b", r"\1 mét vuông", t)
    t = re.sub(r"\d+", lambda m: ' '.join(so_thanh_chu(int(m.group()))), t)
    out = []
    for w in re.findall(r"[a-zà-ỹđ]+", t):
        out += DONG_NGHIA.get(w, w).split()
    return out


def load(p, default):
    return json.loads(Path(p).read_text()) if Path(p).exists() else default


def doc(src, voice, out):
    import gemini_tts, gemini_keys
    from audio_fx import VOICE_CHAIN
    segs = json.loads(Path(src).read_text()); d = Path(out); d.mkdir(parents=True, exist_ok=True)
    dur = load(d / 'thoi_luong.json', {})
    ks = gemini_keys.all_keys()
    print('Khóa Gemini:', ', '.join(f'…{k[-4:]}' for k in ks) or 'KHÔNG CÓ', flush=True)
    todo = [s for s in segs if not (str(s['n']) in dur and (d / f"{s['n']}.mp3").exists())]
    print('Còn thiếu', len(todo), '/', len(segs), 'đoạn; giọng', voice, flush=True)
    for s in todo:
        try:
            wav = gemini_tts.synth(s['text'], STYLE, voice)
        except Exception as e:
            print('DỪNG ở đoạn', s['n'], ':', str(e)[:300], flush=True)
            break
        with wave.open(io.BytesIO(wav)) as f:
            sr = f.getframerate(); n = f.getnframes()
        tmp = d / f"{s['n']}.wav"; tmp.write_bytes(wav)
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', str(tmp), '-af',
                        'silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,'
                        + VOICE_CHAIN, '-ar', '44100', '-b:a', '160k', str(d / f"{s['n']}.mp3")], check=True)
        tmp.unlink()
        dur[str(s['n'])] = round(probe(d / f"{s['n']}.mp3"), 3)
        (d / 'thoi_luong.json').write_text(json.dumps(dur, indent=0))
        print(f"OK {s['n']:3d}  {dur[str(s['n'])]:.1f}s  {s['text'][:60]}", flush=True)
    miss = [s['n'] for s in segs if str(s['n']) not in dur]
    print('Thiếu', len(miss), 'đoạn:', miss[:40], flush=True)


def probe(p):
    """Thời lượng (giây) bằng cách giải mã ra PCM 16 kHz (không cần ffprobe)."""
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(p), '-f', 's16le', '-ac', '1', '-ar', '16000', '-'],
                       capture_output=True, check=True)
    return len(r.stdout) / 32000.0


def kiem(src, out, nguong=0.85, phan=None):
    """phan=(i, n): chỉ nhận dạng các đoạn thứ i, i+n, ... (chạy song song), ghi kiem_phan_<i>.json, không xóa gì.
    Không có phan: gộp mọi kiem_phan_*.json vào kiem.json, nhận dạng đoạn chưa có, rồi xóa đoạn khớp dưới ngưỡng."""
    segs = json.loads(Path(src).read_text()); d = Path(out)
    dur = load(d / 'thoi_luong.json', {}); res = load(d / 'kiem.json', {})
    for f in sorted(d.glob('kiem_phan_*.json')):
        res.update(json.loads(f.read_text()))
    if phan:
        segs = segs[phan[0]::phan[1]]
    todo = [s for s in segs if (d / f"{s['n']}.mp3").exists() and not (str(s['n']) in res and res[str(s['n'])].get('dur') == dur.get(str(s['n'])))]
    m = None
    if todo:
        from faster_whisper import WhisperModel
        m = WhisperModel(os.environ.get('WHISPER_MODEL', 'medium'), device='cpu', compute_type='int8')
    bad = []
    for s in segs:
        k = str(s['n']); f = d / f'{k}.mp3'
        if not f.exists():
            continue
        if k in res and res[k].get('dur') == dur.get(k):
            r = res[k]['khop']
        else:
            import numpy as np
            pcm = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(f), '-f', 's16le', '-ac', '1', '-ar', '16000', '-'], capture_output=True, check=True).stdout
            parts, _ = m.transcribe(np.frombuffer(pcm, np.int16).astype(np.float32) / 32768.0, language='vi', beam_size=5, vad_filter=False)
            asr = ' '.join(p.text for p in parts)
            r, dl = khop(s['text'], asr)
            if not 0.85 <= dl <= 1.15: r = min(r, 0.5)   # thừa hoặc thiếu nhiều tiếng: chắc chắn lỗi
            res[k] = {'khop': round(r, 3), 'do_dai': round(dl, 2), 'asr': asr.strip(), 'dur': dur.get(k)}
        if r < nguong:
            bad.append(k)
        print(f"{k:>4} {r:.2f} {'❌' if r < nguong else '✓'}  {res[k]['asr'][:70]}", flush=True)
    if phan:
        mine = {str(s['n']): res[str(s['n'])] for s in segs if str(s['n']) in res}
        (d / f'kiem_phan_{phan[0]}.json').write_text(json.dumps(mine, ensure_ascii=False, indent=0))
        print(f'Phần {phan[0]}/{phan[1]}: {len(mine)} đoạn, {len(bad)} đoạn khớp dưới {nguong}', flush=True)
        return 0
    (d / 'kiem.json').write_text(json.dumps(res, ensure_ascii=False, indent=0))
    for f in d.glob('kiem_phan_*.json'):
        f.unlink()
    lan = load(d / 'doc_lai.json', {})
    xoa = []
    for k in bad:   # đọc lại tối đa 3 lần mỗi đoạn; quá 3 lần thì giữ bản hiện có và báo
        if lan.get(k, 0) < 3:
            lan[k] = lan.get(k, 0) + 1; xoa.append(k)
            (d / f'{k}.mp3').unlink(missing_ok=True); dur.pop(k, None); res.pop(k, None)
    (d / 'doc_lai.json').write_text(json.dumps(lan)); (d / 'thoi_luong.json').write_text(json.dumps(dur, indent=0))
    (d / 'kiem.json').write_text(json.dumps(res, ensure_ascii=False, indent=0))
    print(f'Khớp dưới {nguong}: {len(bad)} đoạn {bad}; xóa để đọc lại: {xoa}', flush=True)
    return len(xoa)


def chuan(src, out):
    """Cùng âm lượng (loudnorm -16 LUFS) và nhịp gần trung vị (atempo 0,90–1,10, giữ cao độ). Làm trên bản sao."""
    segs = json.loads(Path(src).read_text()); d = Path(out); c = d / 'chuan'; c.mkdir(exist_ok=True)
    dur = load(d / 'thoi_luong.json', {})
    rate = {str(s['n']): len(tieng(s['text'])) / dur[str(s['n'])] for s in segs if str(s['n']) in dur}
    med = sorted(rate.values())[len(rate) // 2]
    out_dur, bang = {}, []
    for k, r in rate.items():
        f = 1.0
        if abs(r / med - 1) > 0.05:
            f = min(1.10, max(0.90, med / r))
        af = (f'atempo={f:.4f},' if f != 1.0 else '') + 'loudnorm=I=-16:TP=-1.5:LRA=11'
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', str(d / f'{k}.mp3'), '-af', af, '-ar', '44100',
                        '-b:a', '160k', str(c / f'{k}.mp3')], check=True)
        out_dur[k] = round(probe(c / f'{k}.mp3'), 3); bang.append((k, r, f))
    (c / 'thoi_luong.json').write_text(json.dumps(out_dur, indent=0))
    tot = sum(out_dur.values())
    print(f'Nhịp trung vị {med:.2f} tiếng/giây; chỉnh nhịp {sum(1 for b in bang if b[2] != 1.0)} đoạn; '
          f'tổng lời đọc {tot / 60:.1f} phút', flush=True)


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'doc':
        doc(sys.argv[2], sys.argv[3], sys.argv[4])
    elif cmd == 'kiem':
        ph = os.environ.get('PHAN')   # "i/n"
        n = kiem(sys.argv[2], sys.argv[3], float(sys.argv[4]) if len(sys.argv) > 4 else 0.85,
                 tuple(map(int, ph.split('/'))) if ph else None)
        Path(os.environ.get('GITHUB_OUTPUT', '/dev/null')).open('a').write(f'doc_lai={n}\n')
    elif cmd == 'chuan':
        chuan(sys.argv[2], sys.argv[3])
