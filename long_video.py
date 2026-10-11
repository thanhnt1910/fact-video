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
# ảnh FLUX là ảnh vuông, sẽ bị cắt trên/dưới cho vừa khung 16:9 -> dặn bố cục rộng, chủ thể ở giữa
WIDE_HINT = "wide cinematic composition, main subject centered with space above and below"
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
    scenes = script.get("scenes", [])
    for b in beats:   # "image": {"scene": n} -> dùng lại ảnh tư liệu của cảnh n trong video ngắn
        im = b.get("image")
        if isinstance(im, dict) and "scene" in im and not im.get("url"):
            n = int(im["scene"])
            src = scenes[n].get("image") if 0 <= n < len(scenes) else None
            if src:
                b["image"] = dict(src)
            else:
                b.pop("image")
    # mỗi ảnh tư liệu chỉ tải 1 lần, beat nào dùng lại cùng ảnh thì dùng chung
    uniq = {}
    for b in beats:
        if b.get("image"):
            k = json.dumps(b["image"], sort_keys=True, ensure_ascii=False)
            uniq.setdefault(k, {"image": b["image"]})
    if uniq:
        pseudo = {"topic": script.get("topic", ""), "scenes": list(uniq.values())}
        credits = images.fetch_scene_images(pseudo, work / "arch", log)
        for b in beats:
            if b.get("image"):
                src = uniq[json.dumps(b["image"], sort_keys=True, ensure_ascii=False)].get("image_src")
                if src:
                    b["image_src"] = src
    AI_CACHE.mkdir(parents=True, exist_ok=True)
    import os
    quota_hit = 0
    only_kaggle = os.environ.get("AI_SOURCE", "").strip().lower() == "kaggle"
    pending = []   # [(beat, key)] chưa vẽ được trên Cloudflare
    for b in beats:
        if b.get("ai") and not b.get("image_src"):
            key = hashlib.sha1((ai_images.STYLE_ID + "|" + b["ai"]).encode()).hexdigest()[:16]
            cached = (AI_CACHE / f"{key}.jpg").exists()
            if (quota_hit or only_kaggle) and not cached:
                pending.append((b, key))
                continue
            try:
                f = ai_images.generate(b["ai"] + ", " + WIDE_HINT, AI_CACHE / f"{key}.jpg", log=log, wide=True)
                b["image_src"] = f.resolve().as_uri()
                b.setdefault("fit", False)   # tranh AI: phủ kín khung 16:9
                used_ai = True
            except Exception as e:
                log(f"     ⚠️  không vẽ được ảnh: {e}")
                msg = str(e).lower()
                if any(k in msg for k in ("429", "neuron", "limit", "quota", "exceeded")):
                    quota_hit += 1
                    pending.append((b, key))
    if pending and os.environ.get("KAGGLE_KEY", "").strip():
        # Cloudflare hết lượt -> vẽ phần còn lại bằng đúng mô hình FLUX.2 klein 4B trên máy GPU miễn phí của Kaggle
        import kaggle_draw
        uniq = {}
        for b, key in pending:
            uniq.setdefault(key, f"{b['ai']}, {WIDE_HINT}, {ai_images.STYLE}")
        log(f"     ☁️  Cloudflare hết lượt / chọn Kaggle: vẽ {len(uniq)} tranh trên Kaggle")
        try:
            res = kaggle_draw.draw_batch([(k, p, 1344, 768) for k, p in uniq.items()], AI_CACHE, log=log, model="klein")
        except Exception as e:
            log(f"     ⚠️  Kaggle lỗi: {e}")
            res = {}
        left = []
        for b, key in pending:
            f = AI_CACHE / f"{key}.jpg"
            if f.exists():
                b["image_src"] = f.resolve().as_uri()
                b.setdefault("fit", False)
                used_ai = True
            else:
                left.append((b, key))
        pending = left
    quota_hit = len(pending)
    if quota_hit:
        # ảnh đã vẽ được vẫn lưu lại, lần chạy sau vẽ nốt
        raise RuntimeError(f"còn {quota_hit} ảnh AI chưa vẽ được (hết lượt Cloudflare, Kaggle cũng chưa vẽ được), sẽ thử lại lần chạy sau")
    prev, prev_fit = None, None
    for b in beats:
        if not b.get("image_src"):
            b["image_src"] = prev
            if prev_fit is not None:
                b.setdefault("fit", prev_fit)
        prev = b.get("image_src") or prev
        if b.get("image_src") and "fit" not in b:
            try:
                w, h = Image.open(b["image_src"].replace("file://", "")).size
                b["fit"] = h > w * 0.95 or w < 1200
            except Exception:
                b["fit"] = False
        prev_fit = b.get("fit")
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
    pending = None
    try:
        credits, used_ai = beat_images(script, beats_all, work)
    except RuntimeError as e:
        # thiếu ảnh AI: vẫn đọc giọng trước (lưu lại), lần sau chỉ còn phải vẽ nốt ảnh
        pending, credits, used_ai = e, [], True

    log(f"  🎙️  Giọng Gemini {voice} ({len(chapters)} chương)")
    import gemini_tts
    narr = array.array("h")
    shots, cards, marks, spoken = [], [], [], []
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
            st, en = t + (s0 - a) / SR, t + (s1 - a) / SR
            spoken.append({"start": st, "speech_end": en, "text": beat.get("text", "")})
            if shots and beat.get("image_src") and shots[-1]["src"] == beat.get("image_src") \
                    and not beat.get("label") and abs(shots[-1]["start"] + shots[-1]["dur"] - st) < 1.5:
                # cùng một ảnh với đoạn trước: kéo dài cảnh cũ (máy quay lướt chậm liền mạch), không tan ảnh vào chính nó
                shots[-1]["dur"] = en - shots[-1]["start"]
                continue
            shots.append({"start": st, "dur": (s1 - s0) / SR, "src": beat.get("image_src"),
                          "fit": bool(beat.get("fit")), "label": beat.get("label", "")})
        t += (b - a) / SR
        add_silence(GAP)
        if ci == 0 and len(chapters) > 1:
            cards.append({"start": t, "dur": CARD_TITLE, "kicker": cfg.get("channel", ""),
                          "title": L.get("title_card") or L["title"], "sub": cfg.get("catchphrase", "")})
            add_silence(CARD_TITLE)
    if pending:
        raise pending
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

    # ---- khung hình: trình duyệt vẽ lớp tĩnh + ảnh bìa, Python ghép từng khung (nhanh, chạy nhiều nhân)
    import long_render
    from playwright.sync_api import sync_playwright
    vis = [s for s in shots if s["src"]]
    silent = work / "silent.mp4"
    with sync_playwright() as p:
        br = p.chromium.launch()
        page = br.new_page(viewport={"width": 1920, "height": 1080})
        page.goto((ROOT / "templates" / "long.html").as_uri())
        page.evaluate("() => document.fonts.ready")
        # ảnh bìa YouTube
        key = next((s["src"] for s in vis if not s["fit"]), vis[0]["src"])
        page.evaluate("a => window.thumb(a[0], a[1], a[2])", [key, cfg.get("channel", ""), L.get("title_card") or L["title"]])
        page.wait_for_timeout(300)
        page.screenshot(path=str(out_dir / f"{script['id']}_dai_thumbnail.jpg"), type="jpeg", quality=92)
        # ảnh bìa cho Facebook: chữ ở giữa (Facebook cắt lưới video thành khung dọc)
        page.goto((ROOT / "templates" / "long.html").as_uri())
        page.evaluate("() => document.fonts.ready")
        page.evaluate("a => window.thumb(a[0], a[1], a[2], 'center')",
                      [key, cfg.get("channel", ""), L.get("title_card") or L["title"]])
        page.wait_for_timeout(300)
        page.screenshot(path=str(out_dir / f"{script['id']}_dai_thumbnail_fb.jpg"), type="jpeg", quality=92)
        page.goto((ROOT / "templates" / "long.html").as_uri())
        page.evaluate("() => document.fonts.ready")
        layers = long_render.render_layers(page, cfg.get("channel", ""), [s["label"] for s in vis if s.get("label")],
                                           cards, work / "layers")
        br.close()
    long_render.render(vis, cards, layers, total, FPS, silent, mv.ffmpeg_exe(), work, log=log)
    try:
        long_render.review_sheet(vis, cards, layers, out_dir / f"{script['id']}_dai_review.jpg")
    except Exception as e:
        log(f"     (không tạo được ảnh duyệt: {e})")

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
    try:
        en_note = subtitles_and_english(script, L, spoken, marks, credits, mcredit, used_ai, out_dir)
    except Exception as e:   # phụ đề / bản dịch lỗi không được làm hỏng video
        log(f"     ⚠️  phụ đề / bản tiếng Anh lỗi: {e}")
        en_note = []
    lines += en_note
    (out_dir / f"{script['id']}_dai_youtube.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    log(f"✅ Video dài: {final.name} ({_fmt(total)})")
    return final, total


def subtitles_and_english(script, L, spoken, marks, credits, mcredit, used_ai, out_dir):
    """Phụ đề tiếng Việt + tiếng Anh (.srt) và tiêu đề/mô tả tiếng Anh. Trả về vài dòng hướng dẫn để ghép vào file mô tả."""
    import subtitles
    sid = script["id"]
    spoken = [s for s in spoken if s.get("text")]
    segs = [(s["start"], s["speech_end"], s["text"]) for s in spoken]
    subtitles.write_srt(out_dir / f"{sid}_dai_vi.srt", subtitles.cues(segs))
    note = ["", "──── PHỤ ĐỀ ────",
            f"YouTube Studio → video → Phụ đề → Thêm ngôn ngữ → Tiếng Việt → Tải tệp lên → {sid}_dai_vi.srt"]
    payload = {"title": L["title"], "description": L.get("description", script.get("caption", "")),
               "chapters": [name for _, name in marks], "lines": [s["text"] for s in spoken]}
    en = subtitles.translate(payload, log)
    if not en:
        return note
    segs_en = [(a, b, t) for (a, b, _), t in zip(segs, en["lines"])]
    subtitles.write_srt(out_dir / f"{sid}_dai_en.srt", subtitles.cues(segs_en))
    tags = " ".join("#" + h.lstrip("#").replace(" ", "") for h in en.get("hashtags", []))
    out = [f"TITLE: {en['title'][:95]}", "", "DESCRIPTION:", en["description"], "",
           "🇻🇳 Narrated in Vietnamese. Turn on English subtitles (CC).", "", "📌 Chapters:"]
    out += [f"{_fmt(t)} {name}" for (t, _), name in zip(marks, en["chapters"])]
    out += ["", tags, "",
            "📌 This video uses an AI voice" + (" and AI-generated illustrations (FLUX)." if used_ai else ".")]
    short = mv._short_credits(credits)
    if short:
        out.append("📷 Archival images: " + "; ".join(short) + " · via Wikimedia Commons")
    if mcredit:
        out.append(f"🎵 Music: {mcredit}")
    (out_dir / f"{sid}_dai_youtube_en.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
    note += [f"Thêm tiếp ngôn ngữ Tiếng Anh: dán Tiêu đề + Mô tả trong file {sid}_dai_youtube_en.txt, "
             f"rồi tải phụ đề {sid}_dai_en.srt."]
    return note


def images_review(script, out_dir):
    """Chỉ chuẩn bị ảnh (ảnh tư liệu + vẽ tranh AI) và xuất bảng duyệt, chưa đọc giọng, chưa dựng video.
    logs: <id>_anh.jpg (lưới ảnh đánh số theo đoạn) + <id>_anh.txt (số, nguồn, lời đọc, prompt)."""
    from PIL import Image, ImageDraw, ImageFont
    work = out_dir / "_work_dai"
    work.mkdir(parents=True, exist_ok=True)
    beats = [b for ch in script["long"]["chapters"] for b in ch["beats"]]
    pending = None
    try:
        beat_images(script, beats, work)
    except RuntimeError as e:
        pending = e
    tw, th, cols = 384, 216, 6
    tiles, rows_txt = [], []
    font = ImageFont.load_default(size=18)
    for i, b in enumerate(beats):
        src = b.get("image_src")
        kind = "AI" if b.get("ai") else ("TL" if b.get("image") else "=")
        im = Image.new("RGB", (tw, th), (40, 0, 0))
        if src:
            try:
                im = Image.open(src.replace("file://", "")).convert("RGB")
                im.thumbnail((tw, th))
                bg = Image.new("RGB", (tw, th), (15, 15, 15))
                bg.paste(im, ((tw - im.width) // 2, (th - im.height) // 2))
                im = bg
            except Exception:
                pass
        d = ImageDraw.Draw(im)
        d.rectangle([0, 0, 70, 26], fill=(0, 0, 0))
        d.text((5, 3), f"{i + 1} {kind}", fill=(255, 210, 120), font=font)
        tiles.append(im)
        rows_txt.append(f"{i + 1:>3} [{kind}] {b.get('text', '')[:140]}\n      → {b.get('ai') or (b.get('image') or {}).get('credit', '(dùng ảnh đoạn trước)')[:140]}")
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (tw + 4), rows * (th + 4)), (0, 0, 0))
    for k, im in enumerate(tiles):
        sheet.paste(im, ((k % cols) * (tw + 4), (k // cols) * (th + 4)))
    sheet.save(out_dir / f"{script['id']}_anh.jpg", quality=85)
    (out_dir / f"{script['id']}_anh.txt").write_text("\n".join(rows_txt) + "\n", encoding="utf-8")
    n_ai = sum(1 for b in beats if b.get("ai"))
    log(f"  🖼️  Bảng duyệt ảnh: {len(beats)} đoạn, {n_ai} tranh AI" + (f" · {pending}" if pending else ""))


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    cfg = mv.load_config()
    bad = 0
    only_images = "--images-only" in sys.argv
    for arg in [a for a in sys.argv[1:] if not a.startswith("--")]:
        script = json.loads(Path(arg).read_text(encoding="utf-8"))
        if not script.get("long"):
            continue
        out_dir = ROOT / "output" / script["id"]
        out_dir.mkdir(parents=True, exist_ok=True)
        log(f"▶️  Video dài {script['id']}: {script['long']['title']}")
        if only_images:
            images_review(script, out_dir)
            continue
        try:
            build(script, cfg, out_dir)
        except Exception as e:
            log(f"❌ Video dài {script['id']}: {e}")
            bad += 1
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
