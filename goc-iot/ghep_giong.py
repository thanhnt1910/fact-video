"""Ghép giọng đọc vào video Góc IoT: chuẩn tốc độ + âm lượng từng cảnh, căn chữ phụ đề theo chỗ nghỉ thật của giọng,
dựng hình theo thời lượng thật, trộn tiếng động (nhỏ hơn giọng) rồi xuất mp4.
Dùng: python goc-iot/ghep_giong.py <số video> <thư mục làm việc> [âm lượng tiếng động, mặc định 0.35]"""
import json, re, statistics, subprocess, sys, wave
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent))
import audio_fx

SR = 44100


def run(*a, **k):
    return subprocess.run(a, check=True, capture_output=True, text=True, **k)


def dur(f):
    return float(run("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)).stdout)


def silences(f):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(f), "-af", "silencedetect=noise=-35dB:d=0.12", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", r)]
    en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r)]
    return list(zip(st, en + [None] * (len(st) - len(en))))


def align(text, f, total):
    """Giờ bắt đầu từng từ (giây, tính từ đầu cảnh, đã cộng 0,25 s trễ): chia câu theo chỗ nghỉ thật, trong câu chia theo độ dài chữ."""
    words = text.split(" ")
    ends = [i for i, w in enumerate(words) if re.search(r"[.!?…]$", w)]
    sents = []
    s0 = 0
    for e in ends:
        sents.append((s0, e)); s0 = e + 1
    if s0 < len(words):
        sents.append((s0, len(words) - 1))
    sil = [(a, b) for a, b in silences(f) if b is not None]
    lead = sil[0][1] if sil and sil[0][0] < 0.05 else 0.0
    tail = sil[-1][0] if sil and sil[-1][1] is not None and total - sil[-1][1] < 0.05 else total
    inner = [(a, b) for a, b in sil if a > lead + 0.1 and b < tail - 0.1]
    gaps = sorted(sorted(inner, key=lambda g: g[1] - g[0], reverse=True)[:max(0, len(sents) - 1)])
    if len(gaps) < len(sents) - 1:
        gaps = []
    bounds = []
    cur = lead
    for i in range(len(sents)):
        end = gaps[i][0] if i < len(gaps) else tail
        bounds.append((cur, end))
        cur = gaps[i][1] if i < len(gaps) else tail
    if not gaps and len(sents) > 1:
        span = (tail - lead) / len(sents)
        bounds = [(lead + i * span, lead + (i + 1) * span) for i in range(len(sents))]
    out = [0.0] * len(words)
    for (a, b), (w0, w1) in zip(bounds, sents):
        ws = words[w0:w1 + 1]
        tot = sum(len(w) + 1 for w in ws)
        c = 0
        for k, w in enumerate(ws):
            out[w0 + k] = round(0.25 + a + (b - a) * c / tot, 3)
            c += len(w) + 1
    return out


def main():
    n = int(sys.argv[1]); W = Path(sys.argv[2]); W.mkdir(parents=True, exist_ok=True)
    sfxvol = float(sys.argv[3]) if len(sys.argv) > 3 else 0.35
    G = ROOT / "giong"
    kb = json.loads((ROOT / "kich-ban.json").read_text(encoding="utf-8"))
    texts = next(v for v in kb["videos"] if v["id"] == n)["scenes"]
    tl = json.loads((G / "thoi-luong.json").read_text(encoding="utf-8"))
    keys = [f"v{n}_s{i}" for i in range(1, len(texts) + 1)]
    target = statistics.median(tl[k]["tu_moi_giay"] for k in keys)
    new, al = {}, {}
    (W / "aud").mkdir(exist_ok=True)
    for k, text in zip(keys, texts):
        r = max(0.93, min(1.07, target / tl[k]["tu_moi_giay"]))
        o = W / "aud" / f"{k}.wav"
        run("ffmpeg", "-y", "-loglevel", "error", "-i", str(G / f"{k}.wav"), "-af",
            f"atempo={r:.4f},loudnorm=I=-16:TP=-1.5:LRA=11,aresample={SR}", "-ac", "1", str(o))
        d = dur(o)
        new[k] = dict(tl[k], giay=round(d, 3))
        al[k] = align(text, o, d)
    (W / "tl.json").write_text(json.dumps(new, ensure_ascii=False), encoding="utf-8")
    (W / "align.json").write_text(json.dumps(al), encoding="utf-8")
    # giọng: mỗi cảnh trễ 0,25 s, đệm tới giay + 0,7 để khớp độ dài cảnh trong bộ dựng hình
    track = []
    for k in keys:
        total = new[k]["giay"] + 0.7
        o = W / "aud" / f"p_{k}.wav"
        run("ffmpeg", "-y", "-loglevel", "error", "-i", str(W / "aud" / f"{k}.wav"), "-af",
            f"adelay=250,apad=whole_dur={total:.3f}", "-t", f"{total:.3f}", "-ar", str(SR), "-ac", "1", str(o))
        track.append(o)
    (W / "aud" / "list.txt").write_text("".join(f"file '{p.name}'\n" for p in track), encoding="utf-8")
    run("ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(W / "aud" / "list.txt"), "-c", "copy", str(W / "voice.wav"))
    # hình theo thời lượng thật
    env = dict(__import__("os").environ, TLFILE=str(W / "tl.json"), ALIGN=str(W / "align.json"))
    subprocess.run(["node", str(ROOT / "dung_hinh.cjs"), str(n), str(W), "full"], check=True, env=env)
    run("ffmpeg", "-y", "-loglevel", "error", "-framerate", "24", "-i", str(W / "f%05d.png"), "-c:v", "libx264", "-preset", "veryfast",
        "-crf", "20", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(W / "silent.mp4"))
    # tiếng động
    info = json.loads((W / "events.json").read_text(encoding="utf-8"))
    nn = int((info["total"] + 1.0) * SR)
    sfx = np.zeros(nn)
    for e in info["events"]:
        clip = audio_fx.get_sfx(e["name"]) * e["gain"]
        st = int(max(0.0, e["t"]) * SR); en = min(nn, st + len(clip))
        sfx[st:en] += clip[:en - st]
    sfx = np.clip(sfx * sfxvol, -1, 1)
    with wave.open(str(W / "sfx.wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((sfx * 32767).astype(np.int16).tobytes())
    run("ffmpeg", "-y", "-loglevel", "error", "-i", str(W / "voice.wav"), "-i", str(W / "sfx.wav"), "-filter_complex",
        "[0:a][1:a]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]", "-map", "[a]", str(W / "mix.wav"))
    out = W / f"video-{n}-giong.mp4"
    run("ffmpeg", "-y", "-loglevel", "error", "-i", str(W / "silent.mp4"), "-i", str(W / "mix.wav"), "-c:v", "copy", "-c:a", "aac",
        "-b:a", "160k", "-shortest", str(out))
    for p in W.glob("f*.png"):
        p.unlink()
    print("xong", out, "dài", round(dur(out), 1), "giây")


if __name__ == "__main__":
    main()
