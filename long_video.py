"""
VIDEO DÀI 16:9 (YouTube / Facebook) kể chuyện bằng ảnh + chuyển cảnh, giọng Gemini Sadaltager.

Kịch bản: trường "long" trong scripts/<mã>.json
  "long": {
    "title": "Tiêu đề YouTube (≤ 95 ký tự)",
    "title_card": "Tiêu đề hiện trên màn hình (có thể **tô màu**)",
    "description": "Đoạn mô tả đầu cho YouTube",
    "voice": "Sadaltager",                       (không có thì lấy config long.voice)
    "chapters": [
      {"title": "", "beats": [...]},             chương đầu không có tiêu đề = đoạn mở đầu gây tò mò
      {"title": "Thành phố đói khát", "beats": [
         {"text": "lời kể (2–4 câu)", "ai": "mô tả ảnh tiếng Anh cho FLUX", "label": "Strasbourg · 1518"},
         {"text": "...", "image": {"url": "...", "credit": "..."}}     ảnh tư liệu (như video ngắn)
      ]}
    ]
  }

  python long_video.py scripts/SL1.json      -> output/<mã>/<mã>_dai.mp4 (+ ảnh bìa, mô tả YouTube)
Lỗi giọng Gemini (hết lượt) -> dừng, không đổi giọng; lần chạy sau làm tiếp (âm thanh đã đọc được lưu lại).
"""
import array
import hashlib
import json
import math
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

import audio_fx
import make_video as mv

ROOT = Path(__file__).resolve().parent
TTS_CACHE = ROOT / "assets" / "tts_cache"
AI_CACHE = ROOT / "assets" / "ai_cache"
SR = mv.SR
FPS = 24
CARD_TITLE, CARD_CHAPTER, CARD_END = 4.5, 3.2, 6.0
GAP = 0.6   # nghỉ sau mỗi chương

LONG_STYLE = ("Native Vietnamese narrator (Northern accent, Hanoi) for a long-form history documentary on YouTube. "
              "Warm, deep, knowledgeable male storyteller with a hint of mystery; calm, unhurried, engaging; "
              "clear diction and natural Vietnamese tones; vary the pace, slow down before surprising facts; "
              "leave a natural pause between paragraphs. Pronounce foreign names naturally. Never robotic.")

log = mv.log


def _fmt(sec):
    sec = int(sec)
    return f"{sec // 60:02d}:{sec % 60:02d}" if sec < 3600 else f"{sec // 3600}:{sec % 3600 // 60:02d}:{sec % 60:02d}"


# ------------------------------------------------------------------ giọng đọc
def chapter_audio(text, voice, work):
    """Đọc 1 chương bằng Gemini (có lưu tạm). Trả về mẫu âm 24 kHz."""
    import gemini_tts
    TTS_CACHE.mkdir(parents=True, exist_ok=True)
    key = hashlib.sha1(f"{voice}|{LONG_STYLE}|{text}".encode()).hexdigest()[:16]
    wav = TTS_CACHE / f"{key}.wav"
    if not wav.exists():
        t = time.time()
        raw = gemini_tts.synth(text, LONG_STYLE, voice, log=log)
        tmp = work / f"{key}_raw.wav"
        tmp.write_bytes(raw)
        mv.run_ffmpeg(["-i", str(tmp), "-ac", "1", "-ar", str(SR), "-sample_fmt", "s16", str(wav)])
        log(f"     🎙️  Gemini đọc xong 1 chương ({time.time() - t:.0f}s)")
    return mv.read_wav(wav)


def split_by_pauses(samples, weights):
    """Chia âm thanh 1 chương thành các đoạn theo khoảng lặng gần nhất với tỉ lệ độ dài chữ."""
    x = np.frombuffer(samples.tobytes(), np.int16).astype(np.float32)
    win = int(0.02 * SR)
    k = len(x) // win
    rms = np.sqrt((x[:k * win].reshape(k, win) ** 2).mean(1) + 1e-6)
    speech = rms[rms > np.percentile(rms, 40)]
    thr = max(150.0, 0.1 * float(np.median(speech)) if len(speech) else 150.0)
    quiet = rms < thr
    # cắt lặng đầu/cuối
    nz = np.where(~quiet)[0]
    a, b = (nz[0], nz[-1] + 1) if len(nz) else (0, k)
    runs, i = [], a
    while i < b:
        if quiet[i]:
            j = i
            while j < b and quiet[j]:
                j += 1
            if j - i >= 12:            # ≥ 0,24 giây
                runs.append(((i + j) / 2, j - i))
            i = j
        else:
            i += 1
    total = b - a
    cum = np.cumsum(weights)[:-1] / sum(weights)
    cuts, last = [], a
    for c in cum:
        exp = a + c * total
        cands = [r for r in runs if r[0] > last + 25]
        if cands:
            best = min(cands, key=lambda r: abs(r[0] - exp) - 0.6 * r[1])
            pos = best[0] if abs(best[0] - exp) < 0.25 * total else exp
        else:
            pos = exp
        cuts.append(int(pos))
        last = pos
    bounds = [a] + cuts + [b]
    return [(bounds[n] * win, bounds[n + 1] * win) for n in range(len(bounds) - 1)], (a * win, b * win)


# ------------------------------------------------------------------ hình ảnh
def beat_images(script, beats, work):
    import ai_images
    import images
    from PIL import Image
    credits, used_ai = [], False
    arch = [b for b in beats if b.get("image")]
    if arch:
        pseudo = {"topic": script.get("topic", ""), "scenes": arch}
        credits = images.fetch_scene_images(pseudo, work / "arch", log)
    AI_CACHE.mkdir(parents=True, exist_ok=True)
    for b in beats:
        if b.get("ai") and not b.get("image_src"):
            key = hashlib.sha1(b["ai"].encode()).hexdigest()[:16]
            try:
                f = ai_images.generate(b["ai"], AI_CACHE / f"{key}.jpg", log=log)
                b["image_src"] = f.resolve().as_uri()
                used_ai = True
            except Exception as e:
                log(f"     ⚠️  không vẽ được ảnh: {e}")
    prev = None
    for b in beats:
        if not b.get("image_src"):
            b["image_src"] = prev
        prev = b.get("image_src") or prev
        if b.get("image_src") and "fit" not in b:
            try:
                w, h = Image.open(b["image_src"].replace("file://", "")).size
                b["fit"] = h > w * 0.95 or w < 1200
            except Exception:
                b["fit"] = False
    return credits, used_ai


# ------------------------------------------------------------------ dựng
def build(script, cfg, out_dir):
    L = script["long"]
    lc = cfg.get("long", {})
    voice = L.get("voice") or lc.get("voice", "Sadaltager")
    work = out_dir / "_work_dai"
    work.mkdir(parents=True, exist_ok=True)
    chapters = L["chapters"]
    beats_all = [b for ch in chapters for b in ch["beats"]]

    log("  🖼️  Ảnh cho video dài")
    credits, used_ai = beat_images(script, beats_all, work)

    log(f"  🎙️  Giọng Gemini {voice} ({len(chapters)} chương)")
    import gemini_tts
    narr = array.array("h")
    shots, cards, marks = [], [], []
    t = 0.0

    def add_silence(sec):
        nonlocal t
        narr.extend(mv.silence(sec))
        t += sec

    for ci, ch in enumerate(chapters):
        if ch.get("title"):
            cards.append({"start": t, "dur": CARD_CHAPTER, "kicker": f"Phần {sum(1 for c in chapters[:ci + 1] if c.get('title'))}",
                          "title": ch["title"]})
            marks.append((t, ch["title"]))
            add_silence(CARD_CHAPTER)
        elif ci == 0:
            marks.append((0.0, "Mở đầu"))
        texts = [gemini_tts.clean_text(b["text"])[0] for b in ch["beats"]]
        audio = chapter_audio("\n\n".join(texts), voice, work)
        segs, (a, b) = split_by_pauses(audio, [max(10, len(x)) for x in texts])
        narr.extend(audio[a:b])
        for (s0, s1), beat in zip(segs, ch["beats"]):
            shots.append({"start": t + (s0 - a) / SR, "dur": (s1 - s0) / SR, "src": beat.get("image_src"),
                          "fit": bool(beat.get("fit")), "label": beat.get("label", "")})
        t += (b - a) / SR
        add_silence(GAP)
        if ci == 0 and len(chapters) > 1:
            cards.append({"start": t, "dur": CARD_TITLE, "kicker": cfg.get("channel", ""),
                          "title": L.get("title_card") or L["title"], "sub": cfg.get("catchphrase", "")})
            add_silence(CARD_TITLE)
    cards.append({"start": t, "dur": CARD_END, "kicker": "Cảm ơn bạn đã nghe chuyện", "title": cfg.get("catchphrase", ""),
                  "sub": f"Đăng ký {cfg.get('channel', '')} để mở trang sử tiếp theo"})
    add_silence(CARD_END)
    total = t
    # ảnh kéo dài lấp chỗ thẻ tiêu đề
    for i, s in enumerate(shots):
        nxt = shots[i + 1]["start"] if i + 1 < len(shots) else total
        s["dur"] = max(0.5, nxt - s["start"])
    mv.write_wav(work / "narration.wav", narr)
    log(f"  ⏱️  Thời lượng {_fmt(total)} · {len(shots)} cảnh ảnh")

    # ---- khung hình
    from playwright.sync_api import sync_playwright
    data = {"channel": cfg.get("channel", ""), "shots": [s for s in shots if s["src"]], "cards": cards}
    silent = work / "silent.mp4"
    n = int(math.ceil(total * FPS))
    cmd = [mv.ffmpeg_exe(), "-hide_banner", "-loglevel", "error", "-y", "-f", "image2pipe", "-framerate", str(FPS),
           "-c:v", "mjpeg", "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-pix_fmt", "yuv420p",
           str(silent)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    t0 = time.time()
    with sync_playwright() as p:
        br = p.chromium.launch()
        page = br.new_page(viewport={"width": 1920, "height": 1080})
        page.goto((ROOT / "templates" / "long.html").as_uri())
        page.evaluate("d => window.setup(d)", data)
        for i in range(n):
            page.evaluate(f"window.renderAt({i / FPS})")
            proc.stdin.write(page.screenshot(type="jpeg", quality=90))
            if i % (FPS * 60) == 0 and i:
                el = time.time() - t0
                log(f"     … {i // FPS // 60} phút / {_fmt(total)}, còn khoảng {el / i * (n - i) / 60:.0f} phút")
        # ảnh bìa YouTube
        key = next((s["src"] for s in shots if s["src"] and not s["fit"]), shots[0]["src"])
        page.evaluate("a => window.thumb(a[0], a[1], a[2])", [key, cfg.get("channel", ""), L.get("title_card") or L["title"]])
        page.wait_for_timeout(300)
        page.screenshot(path=str(out_dir / f"{script['id']}_dai_thumbnail.jpg"), type="jpeg", quality=92)
        br.close()
    proc.stdin.close()
    proc.wait()
    if proc.returncode != 0:
        raise RuntimeError("ffmpeg lỗi khi ghép khung hình")

    # ---- âm thanh: giọng + nhạc (tự hạ khi có giọng)
    import music
    track, mcredit = music.pick({"id": script["id"] + "-dai", "topic": script.get("topic", ""),
                                 "music": L.get("music") or script.get("music")}, log)
    final = out_dir / f"{script['id']}_dai.mp4"
    args = ["-i", str(silent), "-i", str(work / "narration.wav")]
    graph = [f"[1:a]{audio_fx.VOICE_CHAIN},aresample=44100,asplit=2[v][vk]"]
    if track:
        args += ["-stream_loop", "-1", "-i", str(track)]
        dk = cfg.get("music_duck", {})
        graph += [f"[2:a]loudnorm=I={cfg.get('music_lufs', -17)}:LRA=11:TP=-3,aresample=44100,afade=t=in:d=2,"
                  f"afade=t=out:st={max(0, total - 3):.2f}:d=3[mr]",
                  f"[mr][vk]sidechaincompress=threshold={dk.get('threshold', 0.06)}:ratio={dk.get('ratio', 3)}:attack=40:release=500[m]",
                  f"[v][m]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=44100[a]"]
    else:
        graph += ["[vk]anullsink", "[v]loudnorm=I=-14:TP=-1.5:LRA=11,aresample=44100[a]"]
    mv.run_ffmpeg(args + ["-filter_complex", ";".join(graph), "-map", "0:v", "-map", "[a]", "-c:v", "copy",
                          "-c:a", "aac", "-b:a", "192k", "-ac", "2", "-t", f"{total:.3f}", "-movflags", "+faststart",
                          str(final)])

    # ---- mô tả YouTube
    lines = [f"TIÊU ĐỀ YOUTUBE: {L['title'][:95]}", "", "MÔ TẢ:", L.get("description", script.get("caption", "")), "",
             "📌 Mục lục:"] + [f"{_fmt(s)} {name}" for s, name in marks] + [
             "", " ".join("#" + h.lstrip("#") for h in script.get("hashtags", [])), "",
             "📌 Video sử dụng giọng đọc AI" + (" và ảnh minh họa vẽ bằng AI (FLUX)." if used_ai else ".")]
    short = mv._short_credits(credits)
    if short:
        lines.append("📷 Ảnh tư liệu: " + "; ".join(short) + " · nguồn Wikimedia Commons")
    if mcredit:
        lines.append(f"🎵 Nhạc: {mcredit}")
    lines += ["", "──── GHI CHÚ (không đăng) ────", "Nguồn kiểm chứng:"] + [f"- {s}" for s in script.get("sources", [])]
    (out_dir / f"{script['id']}_dai_youtube.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    log(f"✅ Video dài: {final.name} ({_fmt(total)})")
    return final, total


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    cfg = mv.load_config()
    bad = 0
    for arg in sys.argv[1:]:
        script = json.loads(Path(arg).read_text(encoding="utf-8"))
        if not script.get("long"):
            continue
        out_dir = ROOT / "output" / script["id"]
        out_dir.mkdir(parents=True, exist_ok=True)
        log(f"▶️  Video dài {script['id']}: {script['long']['title']}")
        try:
            build(script, cfg, out_dir)
        except Exception as e:
            log(f"❌ Video dài {script['id']}: {e}")
            bad += 1
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
