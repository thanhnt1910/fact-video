"""
Tạo video "Sự thật thú vị" từ file kịch bản JSON.

Cách dùng:
  python make_video.py scripts/DV1.json            # tạo 1 video
  python make_video.py scripts                     # tạo tất cả video chưa làm trong thư mục
  python make_video.py scripts/DV1.json --preview  # bản xem nhanh (nhỏ, ít khung hình)
  python make_video.py scripts --check             # chỉ kiểm tra kịch bản, không dựng
  python make_video.py scripts/DV1.json --force    # dựng lại dù đã có video
  python make_video.py scripts/DV1.json --no-tts   # không cần mạng, giọng đọc thay bằng khoảng lặng
"""
import argparse
import array
import asyncio
import json
import math
import os
import random
import re
import shutil
import subprocess
import sys
import time
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SR = 24000  # sample rate cho âm thanh

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

SCENE_TYPES = {"hook", "explain", "compare", "number", "timeline", "text", "outro"}


# ---------------------------------------------------------------- tiện ích
def log(msg):
    print(msg, flush=True)


def ffmpeg_exe():
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        sys.exit("Không tìm thấy ffmpeg. Chạy: pip install imageio-ffmpeg")


def run_ffmpeg(args):
    cmd = [ffmpeg_exe(), "-hide_banner", "-loglevel", "error", "-y"] + args
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        raise RuntimeError("ffmpeg lỗi:\n" + r.stderr[-2000:])


def load_config():
    return json.loads((ROOT / "config.json").read_text(encoding="utf-8"))


# ---------------------------------------------------------------- kiểm tra kịch bản
def validate(script, cfg):
    errs = []
    for k in ("id", "topic", "title", "scenes"):
        if k not in script:
            errs.append(f"thiếu trường '{k}'")
    if script.get("id") and not re.fullmatch(r"[A-Za-z0-9_-]+", script["id"]):
        errs.append("id chỉ dùng chữ không dấu, số, '-' hoặc '_' (ví dụ DV1, CD-A1)")
    if script.get("topic") and script["topic"] not in cfg["topics"]:
        errs.append(f"topic '{script['topic']}' không có trong config.json ({', '.join(cfg['topics'])})")
    scenes = script.get("scenes") or []
    if not scenes:
        errs.append("không có cảnh nào")
    for i, s in enumerate(scenes, 1):
        if s.get("type") not in SCENE_TYPES:
            errs.append(f"cảnh {i}: type '{s.get('type')}' không hợp lệ ({', '.join(sorted(SCENE_TYPES))})")
        if not str(s.get("voice", "")).strip():
            errs.append(f"cảnh {i}: thiếu lời đọc 'voice'")
    if not script.get("sources"):
        errs.append("chưa có nguồn kiểm chứng 'sources' (bắt buộc theo quy trình)")
    return errs


# ---------------------------------------------------------------- âm thanh
def read_wav(path):
    with wave.open(str(path), "rb") as w:
        assert w.getnchannels() == 1 and w.getsampwidth() == 2 and w.getframerate() == SR
        a = array.array("h")
        a.frombytes(w.readframes(w.getnframes()))
        return a


def write_wav(path, samples):
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(samples.tobytes())


def to_wav(src, dst):
    run_ffmpeg(["-i", str(src), "-ac", "1", "-ar", str(SR), "-sample_fmt", "s16", str(dst)])


def silence(seconds):
    return array.array("h", [0]) * int(seconds * SR)


async def _tts(text, out, voice, rate, pitch):
    import edge_tts
    await edge_tts.Communicate(text, voice, rate=rate, pitch=pitch).save(str(out))


_LAST_TTS = [0.0]


def tts_to_wav(text, wav_path, cfg, no_tts):
    """Đọc 1 câu thoại thành wav. Có cache: cùng nội dung + giọng thì không đọc lại.
    Máy chủ Edge TTS giới hạn tốc độ (gửi dồn dập sẽ bị trả 'No audio'),
    nên giữa các lần gọi luôn giãn cách và khi bị chặn thì đợi lâu dần."""
    if no_tts:
        words = len(text.split())
        write_wav(wav_path, silence(0.4 + words / 3.4))
        return
    meta = wav_path.with_suffix(".txt")
    key = f"{cfg['voice']}|{cfg['voice_rate']}|{cfg['voice_pitch']}|{text}"
    if wav_path.exists() and meta.exists() and meta.read_text(encoding="utf-8") == key:
        return
    mp3 = wav_path.with_suffix(".mp3")
    gap = float(cfg.get("tts_delay", 6))
    backoff = [10, 20, 40, 60, 90]
    last = None
    for attempt in range(len(backoff) + 1):
        wait = _LAST_TTS[0] + gap - time.time()
        if wait > 0:
            time.sleep(wait)
        try:
            asyncio.run(_tts(text, mp3, cfg["voice"], cfg["voice_rate"], cfg["voice_pitch"]))
            _LAST_TTS[0] = time.time()
            to_wav(mp3, wav_path)
            mp3.unlink(missing_ok=True)
            meta.write_text(key, encoding="utf-8")
            return
        except Exception as e:
            _LAST_TTS[0] = time.time()
            last = e
            if attempt < len(backoff):
                log(f"     ⏳ Máy chủ giọng đọc đang giới hạn, đợi {backoff[attempt]}s rồi thử lại…")
                time.sleep(backoff[attempt])
    raise RuntimeError(f"Không tạo được giọng đọc (kiểm tra kết nối mạng): {last}")


def _norm(s):
    return "".join(ch for ch in s.lower() if ch.isalnum())


def _end_punct(s):
    s = s.strip()
    return s if s[-1:] in ".!?…" else s + "."


async def _tts_with_sentences(text, voice, rate, pitch):
    import edge_tts
    audio, sents = bytearray(), []
    comm = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch, boundary="SentenceBoundary")
    async for ch in comm.stream():
        if ch["type"] == "audio":
            audio += ch["data"]
        elif ch["type"] == "SentenceBoundary":
            sents.append({"start": ch["offset"] / 1e7, "end": (ch["offset"] + ch["duration"]) / 1e7,
                          "text": ch["text"]})
    return bytes(audio), sents


def align_scenes(scene_texts, sents):
    """Gán mỗi câu (sentence) của máy chủ cho đúng cảnh, dựa trên số ký tự chữ/số cộng dồn.
    Trả về danh sách (chỉ số câu đầu, chỉ số câu cuối) cho từng cảnh, hoặc None nếu không khớp."""
    need, acc = [], 0
    for t in scene_texts:
        acc += len(_norm(t))
        need.append(acc)
    have, acc = [], 0
    for s in sents:
        acc += len(_norm(s["text"]))
        have.append(acc)
    if not sents or abs(have[-1] - need[-1]) > max(3, need[-1] * 0.03):
        return None
    ranges, j = [], 0
    for k, target in enumerate(need):
        first = j
        while j < len(sents) - 1 and have[j] < target - 2:
            j += 1
        if j < first or abs(have[j] - target) > max(3, target * 0.03):
            return None
        ranges.append((first, j))
        j += 1
    if len(ranges) != len(scene_texts) or ranges[-1][1] != len(sents) - 1:
        return None
    return ranges


def voices_one_request(script, cfg, work):
    """Đọc cả kịch bản trong MỘT lần gọi máy chủ, rồi cắt âm thanh theo từng cảnh.
    Trả về list mảng mẫu âm thanh cho mỗi cảnh, hoặc None nếu không cắt được (khi đó đọc từng cảnh)."""
    texts = [_end_punct(s["voice"]) for s in script["scenes"]]
    full_text = " ".join(texts)
    key = f"{cfg['voice']}|{cfg['voice_rate']}|{cfg['voice_pitch']}|{full_text}"
    wav, meta = work / "voice_full.wav", work / "voice_full.json"
    sents = None
    if wav.exists() and meta.exists():
        m = json.loads(meta.read_text(encoding="utf-8"))
        if m.get("key") == key:
            sents = m["sentences"]
            log("  🎙️  Dùng lại giọng đọc đã có")
    if sents is None:
        log(f"  🎙️  Đọc toàn bộ lời thoại ({len(full_text.split())} từ) trong 1 lần gọi")
        gap = float(cfg.get("tts_delay", 6))
        backoff = [15, 30, 60, 120, 180]
        last = None
        for attempt in range(len(backoff) + 1):
            wait = _LAST_TTS[0] + gap - time.time()
            if wait > 0:
                time.sleep(wait)
            try:
                audio, sents = asyncio.run(_tts_with_sentences(full_text, cfg["voice"], cfg["voice_rate"], cfg["voice_pitch"]))
                _LAST_TTS[0] = time.time()
                if not audio:
                    raise RuntimeError("không nhận được âm thanh")
                break
            except Exception as e:
                _LAST_TTS[0] = time.time()
                last, sents = e, None
                if attempt < len(backoff):
                    log(f"     ⏳ Máy chủ giọng đọc đang giới hạn, đợi {backoff[attempt]}s rồi thử lại…")
                    time.sleep(backoff[attempt])
        if sents is None:
            raise RuntimeError("Máy chủ giọng đọc đang chặn tạm thời. Đợi 10–15 phút rồi chạy lại "
                               f"(video đã xong sẽ được bỏ qua). Chi tiết: {last}")
        mp3 = work / "voice_full.mp3"
        mp3.write_bytes(audio)
        to_wav(mp3, wav)
        mp3.unlink(missing_ok=True)
        meta.write_text(json.dumps({"key": key, "sentences": sents}, ensure_ascii=False, indent=1), encoding="utf-8")

    ranges = align_scenes(texts, sents)
    if ranges is None:
        log("  ℹ️  Không cắt được theo câu, chuyển sang đọc từng cảnh")
        return None
    full = read_wav(wav)
    total = len(full) / SR
    out = []
    for k, (a, b) in enumerate(ranges):
        prev_end = sents[ranges[k - 1][1]]["end"] if k else 0.0
        next_start = sents[ranges[k + 1][0]]["start"] if k + 1 < len(ranges) else total
        st = max(prev_end, sents[a]["start"] - 0.05) if k else max(0.0, sents[a]["start"] - 0.05)
        en = min(next_start, sents[b]["end"] + 0.12)
        out.append(trim_silence(full[int(st * SR):int(en * SR)]))
    return out


def trim_silence(samples, thresh=600, keep_head=0.04, keep_tail=0.12):
    """Cắt khoảng lặng ở đầu và cuối đoạn giọng đọc để nhịp video gọn và phụ đề khớp hơn."""
    win = int(0.01 * SR)
    n = len(samples)
    if n < win * 4:
        return samples

    def loud(i):
        seg = samples[i:i + win]
        return max(abs(min(seg)), abs(max(seg))) > thresh

    a = 0
    while a < n - win and not loud(a):
        a += win
    b = n - win
    while b > a and not loud(b):
        b -= win
    a = max(0, a - int(keep_head * SR))
    b = min(n, b + win + int(keep_tail * SR))
    return samples[a:b] if b - a > win * 4 else samples


SHORT_STYLE = ("Native Vietnamese narrator (Northern accent, Hanoi) for a 60-second true-history short video. "
               "Warm, captivating male storyteller with a hint of mystery, like telling a strange true tale by lantern light; "
               "lively pace but clear diction and natural Vietnamese tones; slow down and lower the voice before a "
               "surprising fact, then reveal it with energy; pause briefly at '…'. Pronounce foreign names naturally "
               "in their original language. Never robotic, never news-anchor flat.")


def voices_gemini(script, cfg, work):
    """Giọng Gemini (giống video dài): đọc cả kịch bản trong 1 lần, cắt theo khoảng lặng thành từng cảnh.
    Có lưu tạm trong assets/tts_cache nên chạy lại không tốn thêm."""
    import hashlib
    import gemini_tts
    import long_video
    voice = cfg.get("gemini_voice") or cfg.get("long", {}).get("voice", "Sadaltager")
    texts, hints = [], []
    for sc in script["scenes"]:
        t, h = gemini_tts.clean_text(_end_punct(sc["voice"]))
        texts.append(t)
        hints += h
    style = SHORT_STYLE + (" Specific emphasis: " + "; ".join(hints[:12]) + "." if hints else "")
    full = "\n\n".join(texts)
    cache = ROOT / "assets" / "tts_cache"
    cache.mkdir(parents=True, exist_ok=True)
    key = hashlib.sha1(f"short|{voice}|{style}|{full}".encode()).hexdigest()[:16]
    wav = cache / f"{key}.wav"
    if not wav.exists():
        log(f"  🎙️  Giọng Gemini {voice}: đọc cả kịch bản ({len(full.split())} tiếng)")
        raw = gemini_tts.synth(full, style, voice, log=log)
        tmp = work / f"{key}_raw.wav"
        tmp.write_bytes(raw)
        run_ffmpeg(["-i", str(tmp), "-ac", "1", "-ar", str(SR), "-sample_fmt", "s16", str(wav)])
    else:
        log("  🎙️  Dùng lại giọng Gemini đã có")
    audio = read_wav(wav)
    segs, _ = long_video.split_by_pauses(audio, [max(10, len(x)) for x in texts])
    return [trim_silence(audio[int(a):int(b)]) for a, b in segs]


def _vieneu_python(vc):
    py = ROOT / vc.get("python", ".venv-tts/Scripts/python.exe")
    if not py.exists():
        alt = ROOT / ".venv-tts" / "bin" / "python"
        py = alt if alt.exists() else py
    if not py.exists():
        raise RuntimeError("Chưa cài VieNeu-TTS. Bấm đúp cai-giong-doc.bat trước, "
                           "hoặc đặt \"tts_engine\": \"edge\" trong config.json")
    return py


def _apply_style(samples, style, work, tag):
    """Đổi tốc độ / cao độ / âm lượng 1 đoạn giọng bằng ffmpeg."""
    import audio_fx
    flt = audio_fx.style_filter(style)
    if not flt:
        return samples
    a, b = work / f"_st_{tag}_in.wav", work / f"_st_{tag}_out.wav"
    write_wav(a, samples)
    run_ffmpeg(["-i", str(a), "-af", flt, "-ac", "1", "-ar", str(SR), "-sample_fmt", "s16", str(b)])
    out = read_wav(b)
    a.unlink(missing_ok=True)
    b.unlink(missing_ok=True)
    return out


def voices_vieneu(script, cfg, work):
    """Giọng VieNeu-TTS chạy trên máy. Mỗi cảnh được tách thành từng đoạn theo câu và dấu "…",
    mỗi đoạn có nhấn nhá riêng (tốc độ, cao độ, âm lượng) rồi ghép lại với khoảng ngừng tự nhiên.
    Trả về list (mẫu âm thanh, [(chữ phụ đề, bắt đầu, kết thúc)]) cho từng cảnh."""
    import hashlib
    import audio_fx
    vc = cfg.get("vieneu", {})
    py = _vieneu_python(vc)
    ref = (vc.get("ref_audio") or "").strip()
    ref_path = (ROOT / ref) if ref and not Path(ref).is_absolute() else (Path(ref) if ref else None)
    if ref_path and not ref_path.exists():
        raise RuntimeError(f"Không thấy file giọng mẫu: {ref_path}")
    sig = f"vieneu|{vc.get('mode', '')}|{vc.get('voice', '')}|"
    if ref_path:
        st = ref_path.stat()
        sig += f"{ref_path.name}|{st.st_size}|{int(st.st_mtime)}"

    auto = cfg.get("auto_prosody", True)
    plans = [audio_fx.parse_voice(s["voice"], s["type"], auto, cfg.get("pauses")) for s in script["scenes"]]
    # "pronounce": {"Göbekli Tepe": "Gơ bếch li Tê pê"} — đổi cách đọc, phụ đề vẫn giữ chữ gốc
    pron = {**cfg.get("pronounce", {}), **script.get("pronounce", {})}
    for plan in plans:
        for seg in plan:
            for k, v in pron.items():
                seg["tts"] = seg["tts"].replace(k, v)
    cache = work / "seg"
    cache.mkdir(exist_ok=True)

    def seg_path(text):
        return cache / (hashlib.sha1((sig + "|" + text).encode("utf-8")).hexdigest()[:16] + ".wav")

    need = {}
    for plan in plans:
        for seg in plan:
            pth = seg_path(seg["tts"])
            if not pth.exists():
                need[seg["tts"]] = pth
    if need:
        log(f"  🎙️  VieNeu đọc {len(need)} đoạn (lần đầu nạp mô hình hơi lâu)…")
        items = [{"text": t, "out": str(p.with_name(p.stem + "_raw.wav"))} for t, p in need.items()]
        job = {"voice": vc.get("voice") or None, "ref_audio": str(ref_path) if ref_path else None,
               "mode": vc.get("mode") or None, "items": items}
        jf = work / "vieneu_job.json"
        jf.write_text(json.dumps(job, ensure_ascii=False), encoding="utf-8")
        proc = subprocess.Popen([str(py), str(ROOT / "vieneu_tts.py"), str(jf)], stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace")
        tail = []
        for line in proc.stdout:
            line = line.rstrip()
            tail = (tail + [line])[-15:]
            if line.startswith("[vieneu]"):
                log("     " + line[9:])
        if proc.wait() != 0:
            raise RuntimeError("VieNeu lỗi:\n" + "\n".join(tail))
        for it, pth in zip(items, need.values()):
            raw = Path(it["out"])
            tmp = pth.with_name(pth.stem + "_tmp.wav")
            to_wav(raw, tmp)
            write_wav(pth, trim_silence(read_wav(tmp), keep_head=0.02, keep_tail=0.06))
            tmp.unlink(missing_ok=True)
            raw.unlink(missing_ok=True)
    else:
        log("  🎙️  Dùng lại giọng đọc đã có")

    out = []
    for si, plan in enumerate(plans):
        audio = array.array("h")
        timings = []
        for k, seg in enumerate(plan):
            audio.extend(silence(seg["pause_before"]))
            clip = _apply_style(read_wav(seg_path(seg["tts"])), seg["style"], work, f"{si}_{k}")
            t0 = len(audio) / SR
            audio.extend(clip)
            timings.append((seg["show"], t0, len(audio) / SR))
            audio.extend(silence(seg["pause_after"]))
        out.append((audio, timings))
    return out


def make_whoosh(seconds=0.45, seed=7):
    """Âm 'vút' nhẹ khi chuyển cảnh, tự sinh nên không cần file ngoài."""
    rnd = random.Random(seed)
    n = int(seconds * SR)
    out = array.array("h", [0]) * n
    lp = 0.0
    for i in range(n):
        x = i / n
        cutoff = 0.02 + 0.35 * math.sin(math.pi * x)       # quét tần số lên rồi xuống
        lp += cutoff * (rnd.uniform(-1, 1) - lp)
        env = math.sin(math.pi * x) ** 2
        out[i] = int(max(-1, min(1, lp * env * 2.2)) * 32767)
    return out


def mix_into(base, clip, at_sec, gain):
    start = int(at_sec * SR)
    for i, v in enumerate(clip):
        j = start + i
        if j >= len(base):
            break
        base[j] = max(-32768, min(32767, base[j] + int(v * gain)))


# ---------------------------------------------------------------- phụ đề
def split_subs(text, max_words):
    parts = re.split(r"(?<=[.!?…,;:])\s+", text.strip())
    chunks = []
    for p in parts:
        words = p.split()
        while len(words) > max_words:
            cut = max_words if len(words) - max_words >= 3 else math.ceil(len(words) / 2)
            chunks.append(" ".join(words[:cut]))
            words = words[cut:]
        if words:
            chunks.append(" ".join(words))
    # gộp mẩu quá ngắn vào mẩu trước
    merged = []
    for c in chunks:
        if merged and len(c.split()) <= 2 and len(merged[-1].split()) + len(c.split()) <= max_words + 2:
            merged[-1] += " " + c
        else:
            merged.append(c)
    return merged


def build_subs_timed(timings, start, max_words):
    """Phụ đề theo đúng mốc từng đoạn giọng (khớp hơn chia đều theo độ dài chữ)."""
    out = []
    for text, a, b in timings:
        out += build_subs(text, start + a, b - a, max_words)
    return out


def build_subs(text, start, speech_dur, max_words):
    text = re.sub(r"\s*\[[^\]]*\]\s*", " ", text).strip()
    chunks = split_subs(text, max_words)
    total = sum(len(c) for c in chunks) or 1
    t = start
    out = []
    for c in chunks:
        d = speech_dur * len(c) / total
        out.append({"text": c.rstrip(",;:"), "start": round(t, 3), "end": round(t + d, 3)})
        t += d
    return out


# ---------------------------------------------------------------- dựng video
def build_timeline(script, cfg, work, no_tts):
    scenes, subs = [], []
    narration = array.array("h")
    t = 0.0
    starts = []
    engine = cfg.get("tts_engine", "edge")
    if no_tts:
        voices = None
    elif engine == "vieneu":
        voices = voices_vieneu(script, cfg, work)
    elif engine == "gemini":
        voices = voices_gemini(script, cfg, work)
    else:
        voices = voices_one_request(script, cfg, work)
    for i, s in enumerate(script["scenes"]):
        timings = None
        if voices is not None:
            voice = voices[i]
            if isinstance(voice, tuple):
                voice, timings = voice
        else:
            wav = work / f"voice_{i:02d}.wav"
            log(f"  🎙️  Giọng đọc cảnh {i + 1}/{len(script['scenes'])}")
            tts_to_wav(s["voice"], wav, cfg, no_tts)
            voice = read_wav(wav)
        speech = len(voice) / SR
        pad = cfg["pad_after_hook"] if s["type"] == "hook" else cfg["pad_after_scene"]
        dur = max(cfg["min_scene_seconds"], speech + pad, float(s.get("min_seconds", 0)))
        narration.extend(voice)
        narration.extend(silence(dur - speech))
        scene = dict(s)
        scene.update(start=round(t, 3), dur=round(dur, 3))
        scenes.append(scene)
        starts.append(t)
        if cfg.get("subtitles", True) and (s["type"] != "hook" or cfg.get("subtitle_on_hook")):
            if timings:
                subs += build_subs_timed(timings, t, cfg["subtitle_max_words"])
            else:
                subs += build_subs(s["voice"], t, speech, cfg["subtitle_max_words"])
        t += dur

    write_wav(work / "narration.wav", narration)
    sfx_cfg = cfg.get("sfx", {"enabled": cfg.get("transition_sfx", True), "volume": 0.55})
    if sfx_cfg.get("enabled", True):
        import audio_fx
        audio_fx.build_sfx_track(scenes, t, work / "sfx.wav", float(sfx_cfg.get("volume", 0.55)),
                                 style=cfg.get("style", ""), ambience=float(sfx_cfg.get("ambience", 0.0)))
    else:
        (work / "sfx.wav").unlink(missing_ok=True)
    return scenes, subs, t


def render(script, cfg, out_dir, preview=False, no_tts=False):
    from playwright.sync_api import sync_playwright

    work = out_dir / "_work"
    work.mkdir(parents=True, exist_ok=True)
    script["_credits"] = []
    if cfg.get("images", True) and any(sc.get("image") for sc in script["scenes"]):
        import images
        log("  🖼️  Tìm ảnh minh họa (chỉ ảnh giấy phép mở)")
        try:
            script["_credits"] = images.fetch_scene_images(script, work, log)
        except Exception as e:
            log(f"     ⚠️  Bỏ qua ảnh: {e}")
    mark_image_fit(script)
    if not preview and any(sc.get("image_src") for sc in script["scenes"]):
        import kiem_tra_anh
        items, seen = [], {}
        for sc in script["scenes"]:
            src = sc.get("image_src")
            if not src:
                continue
            if src not in seen:
                spec = sc.get("image") if isinstance(sc.get("image"), dict) else {}
                seen[src] = {"src": src, "texts": [], "ai": False, "label": sc.get("type", ""),
                             "title": spec.get("credit", "")[:200]}
                items.append(seen[src])
            seen[src]["texts"].append(re.sub(r"\[[^\]]*\]", "", sc.get("voice", "")).strip())
        res = kiem_tra_anh.check(items, script["id"], "ngan", log)
        bad = [it for it in items if any(m == "loi" for m, _ in res.get(it["src"], []))]
        if bad and os.environ.get("FV_IMG_STRICT", "1") not in ("0", "no"):
            raise RuntimeError("ảnh không đạt kiểm tra, chưa dựng (xem logs/anh_%s_ngan_kiemtra.txt)" % script["id"])
    add_motion(script, cfg)
    scenes, subs, total = build_timeline(script, cfg, work, no_tts)
    theme = cfg["topics"][script["topic"]]
    data = {"config": cfg, "theme": theme, "scenes": scenes, "subtitles": subs, "total": total}
    (work / "timeline.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    fps = cfg["preview_fps"] if preview else cfg["fps"]
    scale = 0.5 if preview else 1
    n_frames = int(math.ceil(total * fps))
    name = script["id"] + ("_preview" if preview else "")
    mp4 = out_dir / f"{name}.mp4"

    import audio_fx
    if cfg.get("music_library"):
        import music as music_lib
        music, credit = music_lib.pick(script, log)
        has_music = music is not None
        script["_music_credit"] = credit
    else:
        music = ROOT / cfg.get("music_file", "")
        has_music = bool(cfg.get("music_file")) and music.is_file()
    sfx_wav = work / "sfx.wav"
    args = ["-f", "image2pipe", "-framerate", str(fps), "-c:v", "mjpeg", "-i", "-",
            "-i", str(work / "narration.wav")]
    idx = 2
    vchain = audio_fx.VOICE_CHAIN if cfg.get("voice_fx", True) else "anull"
    graph = [f"[1:a]{vchain},aresample=44100,asplit=2[v][vk]"]
    mix = ["[v]"]
    if sfx_wav.exists():
        args += ["-i", str(sfx_wav)]
        graph.append(f"[{idx}:a]aresample=44100[s]")
        mix.append("[s]")
        idx += 1
    if has_music:
        args += ["-stream_loop", "-1", "-i", str(music)]
        # chuẩn hóa độ to từng bài nhạc (bài nào cũng nghe đều nhau) rồi mới chỉnh âm lượng
        norm = f"loudnorm=I={cfg['music_lufs']}:LRA=11:TP=-3," if cfg.get("music_lufs") is not None else ""
        graph.append(f"[{idx}:a]{norm}aresample=44100,volume={cfg['music_volume']},afade=t=in:d=1.2,"
                     f"afade=t=out:st={max(0, total - 2.0):.2f}:d=2.0[mraw]")
        dk = cfg.get("music_duck", {})
        graph.append(f"[mraw][vk]sidechaincompress=threshold={dk.get('threshold', 0.03)}:ratio={dk.get('ratio', 5)}"
                     f":attack=40:release=400[m]")
        mix.append("[m]")
        idx += 1
    else:
        graph.append("[vk]anullsink")
    lufs = cfg.get("loudness_lufs", -14)
    graph.append(f"{''.join(mix)}amix=inputs={len(mix)}:duration=first:normalize=0,"
                 f"loudnorm=I={lufs}:TP=-1.5:LRA=11,aresample=44100[a]")
    args += ["-filter_complex", ";".join(graph), "-map", "0:v", "-map", "[a]"]
    args += ["-c:v", "libx264", "-preset", "veryfast" if preview else "medium", "-crf", "21",
             "-pix_fmt", "yuv420p", "-r", str(fps), "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2",
             "-t", f"{total:.3f}", "-movflags", "+faststart", str(mp4)]
    cmd = [ffmpeg_exe(), "-hide_banner", "-loglevel", "error", "-y"] + args

    log(f"  🎬 Dựng {n_frames} khung hình ({total:.1f} giây, {fps} fps)")
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    with sync_playwright() as p:
        # cho phép WebGL đọc ảnh/bản đồ độ sâu trên đĩa (hiệu ứng parallax)
        browser = p.chromium.launch(args=["--allow-file-access-from-files", "--enable-unsafe-swiftshader"])
        page = browser.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=scale)
        page.goto((ROOT / "templates" / "scene.html").as_uri())
        page.evaluate("d => window.setup(d)", data)
        page.wait_for_timeout(300)
        t0 = time.time()
        try:
            for f in range(n_frames):
                page.evaluate(f"window.renderAt({f / fps})")
                proc.stdin.write(page.screenshot(type="jpeg", quality=92))
                if f % (fps * 5) == 0 and f:
                    el = time.time() - t0
                    log(f"     … {f}/{n_frames} khung, còn khoảng {el / f * (n_frames - f):.0f}s")
            # ảnh bìa: giữa cảnh hook
            if not preview:
                hook = next((s for s in scenes if s["type"] == "hook"), scenes[0])
                page.evaluate(f"window.renderAt({hook['start'] + min(2.2, hook['dur'] * 0.8)})")
                page.screenshot(path=str(out_dir / f"{script['id']}_thumbnail.jpg"), type="jpeg", quality=92)
                review_sheet(page, scenes, out_dir / f"{script['id']}_review.jpg", work)
        finally:
            browser.close()
            proc.stdin.close()
            err = proc.stderr.read().decode("utf-8", "replace")
            proc.wait()
    if proc.returncode != 0:
        raise RuntimeError("ffmpeg lỗi khi ghép video:\n" + err[-2000:])
    if has_music:
        try:
            _log_music_level(work, music, cfg, total, log)
        except Exception as e:
            log(f"     (không đo được độ to nhạc: {e})")
    if not has_music and cfg.get("music_file") and not cfg.get("music_library"):
        log(f"  ℹ️  Chưa có nhạc nền ({cfg['music_file']}), video chỉ có giọng đọc")
    return mp4, total


def add_motion(script, cfg):
    """Hiệu ứng chuyển động: chọn lớp hạt cho từng cảnh, tính bản đồ độ sâu cho ảnh (parallax 2.5D)."""
    import motion
    mc = motion.settings(cfg)
    cfg["motion"] = mc            # trang dựng hình đọc từ config
    for sc in script["scenes"]:
        sc["fx"] = motion.pick_fx(sc, auto=mc.get("fx_auto", True)) if mc["fx"] else ""
    if not mc["parallax"]:
        return
    srcs = [sc for sc in script["scenes"] if sc.get("image_src")]
    if not srcs:
        return
    log("  🌀 Bản đồ độ sâu cho hiệu ứng 3D (parallax)")
    done = {}
    for sc in srcs:
        k = sc["image_src"]
        if k not in done:
            done[k] = motion.depth_map(k, log=log)
        if done[k]:
            sc["depth_src"] = Path(done[k]).resolve().as_uri()
    log(f"     {sum(1 for v in done.values() if v)}/{len(done)} ảnh có độ sâu · lớp hạt: "
        + ", ".join(sc.get("fx") or "-" for sc in script["scenes"]))


def mark_image_fit(script):
    """Ảnh ngang đặt vào khung dọc sẽ bị cắt mất hai bên (có thể mất cả chủ thể).
    Mặc định hiện trọn ảnh ngang trên nền mờ; kịch bản có thể ghi "fit": false hoặc "focus": "30% 50%" để cắt theo ý."""
    from PIL import Image
    from urllib.parse import unquote, urlparse
    for sc in script["scenes"]:
        src, spec = sc.get("image_src"), sc.get("image") or {}
        if not src or not isinstance(spec, dict):
            continue
        if spec.get("focus"):
            sc["image_focus"] = spec["focus"]
        if "fit" in spec:
            sc["image_fit"] = bool(spec["fit"])
            continue
        try:
            path = unquote(urlparse(src).path) if src.startswith("file:") else src
            w, h = Image.open(path).size
            sc["image_fit"] = w / h > 1.05 and not spec.get("focus")
        except Exception:
            pass


def review_sheet(page, scenes, out, work):
    """Ảnh duyệt: 1 khung giữa mỗi cảnh, để kiểm tra bố cục/cắt hình trước khi gửi."""
    from PIL import Image
    tiles = []
    for k, sc in enumerate(scenes):
        page.evaluate(f"window.renderAt({sc['start'] + sc['dur'] * 0.6})")
        f = work / f"review_{k:02d}.jpg"
        page.screenshot(path=str(f), type="jpeg", quality=80)
        im = Image.open(f).convert("RGB")
        im.thumbnail((360, 640))
        tiles.append(im)
    if not tiles:
        return
    sheet = Image.new("RGB", (360 * len(tiles) + 8 * (len(tiles) - 1), 640), (20, 20, 20))
    for k, im in enumerate(tiles):
        sheet.paste(im, (k * 368, 0))
    sheet.save(out, quality=85)


def _log_music_level(work, music, cfg, total, log):
    """Đo nhạc nền nhỏ hơn giọng bao nhiêu dB (khi đang nói) để kiểm tra mà không cần nghe."""
    import audio_fx
    import numpy as np
    vchain = audio_fx.VOICE_CHAIN if cfg.get("voice_fx", True) else "anull"
    norm = f"loudnorm=I={cfg['music_lufs']}:LRA=11:TP=-3," if cfg.get("music_lufs") is not None else ""
    dk = cfg.get("music_duck", {})
    outs = {}
    for name, g in {
        "voice": f"[0:a]{vchain},aresample=44100[a]",
        "music": (f"[0:a]{vchain},aresample=44100[vk];[1:a]{norm}aresample=44100,volume={cfg['music_volume']}[m];"
                  f"[m][vk]sidechaincompress=threshold={dk.get('threshold', 0.03)}:ratio={dk.get('ratio', 5)}"
                  f":attack=40:release=400[a]"),
    }.items():
        out = work / f"_lv_{name}.wav"
        inputs = ["-i", str(work / "narration.wav")]
        if name == "music":
            inputs += ["-stream_loop", "-1", "-t", f"{total:.2f}", "-i", str(music)]
        run_ffmpeg(inputs + ["-filter_complex", g, "-map", "[a]", "-t", f"{total:.2f}", "-ac", "1", "-ar", "44100", str(out)])
        import wave
        with wave.open(str(out)) as w:
            outs[name] = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float64) / 32768
    v, m = outs["voice"], outs["music"]
    n = min(len(v), len(m))
    v, m = v[:n], m[:n]
    win = 4410
    k = n // win
    rv = np.sqrt((v[:k * win].reshape(k, win) ** 2).mean(1))
    rm = np.sqrt((m[:k * win].reshape(k, win) ** 2).mean(1))
    talk = rv > 10 ** (-40 / 20)
    db = lambda x: 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9)
    if talk.any() and (~talk).any():
        gap = db(rm[~talk])
    else:
        gap = float("nan")
    log(f"  🎚️  Giọng {db(rv[talk]):.1f} dB · nhạc khi đang nói {db(rm[talk]):.1f} dB "
        f"(nhỏ hơn giọng {db(rv[talk]) - db(rm[talk]):.1f} dB) · nhạc lúc nghỉ {gap:.1f} dB")


def _short_credits(credits):
    """Rút gọn nguồn ảnh: chỉ giữ ảnh CC BY (bắt buộc ghi nguồn), dạng 'Tác giả (CC BY 4.0)'."""
    import re
    out = []
    for c in credits or []:
        m = re.match(r'^"(?P<file>[^"]+)"\s+–\s+(?P<author>.+?),\s+(?P<lic>CC BY[^()]*?)\s*\((?P<url>[^)]+)\)\s*$', c)
        if not m:
            continue
        author = re.sub(r"^(Photo|Creator|Ảnh):\s*", "", m["author"].strip())
        if author.lower() in ("không rõ", "unknown") or not author:
            author = "Wellcome Collection" if "Wellcome" in m["file"] else m["file"].rsplit(".", 1)[0][:40]
        item = f"{author} ({m['lic'].strip()})"
        if item not in out:
            out.append(item)
    return out


def write_caption(script, cfg, out_dir):
    """File caption: các khối dán thẳng lên từng nền tảng + phần ghi chú để bạn lưu lại."""
    theme = cfg["topics"][script["topic"]]
    tags = " ".join("#" + t.lstrip("#") for t in (script.get("hashtags") or []))
    cap = script.get("caption", script["title"])
    music = script.get("_music_credit")
    img = _short_credits(script.get("_credits"))
    short = []
    if img:
        short.append("📷 Ảnh: " + "; ".join(img) + " · nguồn Wikimedia Commons")
    if music:
        name = music.split('"')[1] if '"' in music else music
        short.append(f"🎵 Nhạc: \"{name}\" – Kevin MacLeod (incompetech.com), CC BY 4.0")
    social = [cap, "", tags] + ([""] + short if short else [])
    yt_desc = [cap, "", tags, ""] + [x for x in short if not x.startswith("🎵")]
    if music:
        yt_desc.append(f"🎵 Nhạc: {music}")
    title = script["title"]
    lines = [
        "════ FACEBOOK REELS / TIKTOK — copy nguyên khối dưới đây ════",
        *social,
        "",
        "════ YOUTUBE SHORTS ════",
        f"Tiêu đề: {title[:95]}",
        "Mô tả:",
        *yt_desc,
        *__import__("binh_luan").lines(script, "ngan"),
        "",
        "════ GHI CHÚ (không đăng) ════",
        f"Chủ đề: {theme['icon']} {theme['label']}",
        "Nhớ bật nhãn \"Nội dung do AI tạo\" (giọng đọc AI) khi đăng.",
        "Nguồn kiểm chứng:",
    ] + [f"- {s}" for s in script.get("sources", [])]
    if script.get("_credits"):
        lines += ["Nguồn ảnh đầy đủ:"] + [f"- {c}" for c in script["_credits"]]
    (out_dir / f"{script['id']}_caption.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---------------------------------------------------------------- main
def collect(path):
    p = Path(path)
    if p.is_dir():
        return sorted(x for x in p.glob("*.json"))
    return [p]


def main():
    ap = argparse.ArgumentParser(description="Tạo video Sự thật thú vị từ kịch bản JSON")
    ap.add_argument("target", help="file .json hoặc thư mục chứa kịch bản")
    ap.add_argument("--preview", action="store_true", help="bản xem nhanh 540x960, 15 fps")
    ap.add_argument("--check", action="store_true", help="chỉ kiểm tra kịch bản")
    ap.add_argument("--force", action="store_true", help="dựng lại dù đã có video")
    ap.add_argument("--no-tts", action="store_true", help="không đọc giọng (không cần mạng)")
    ap.add_argument("--out", default="output", help="thư mục xuất video")
    a = ap.parse_args()

    cfg = load_config()
    files = collect(a.target)
    if not files:
        sys.exit("Không tìm thấy file kịch bản .json nào.")

    ok, bad, skipped = 0, 0, 0
    for f in files:
        try:
            script = json.loads(f.read_text(encoding="utf-8"))
        except Exception as e:
            log(f"❌ {f.name}: JSON sai cú pháp: {e}")
            bad += 1
            continue
        errs = validate(script, cfg)
        if errs:
            log(f"❌ {f.name}:\n   - " + "\n   - ".join(errs))
            bad += 1
            continue
        if a.check:
            log(f"✅ {f.name}: hợp lệ ({len(script['scenes'])} cảnh)")
            ok += 1
            continue
        out_dir = (ROOT / a.out / script["id"]) if not Path(a.out).is_absolute() else Path(a.out) / script["id"]
        out_dir.mkdir(parents=True, exist_ok=True)
        final = out_dir / (script["id"] + ("_preview" if a.preview else "") + ".mp4")
        if final.exists() and not a.force:
            log(f"⏭️  {script['id']}: đã có video, bỏ qua (thêm --force để dựng lại)")
            skipped += 1
            continue
        log(f"▶️  {script['id']}: {script['title']}")
        t = time.time()
        try:
            if script.get("ngan") and not a.preview:
                # khung video ngắn mới (kế hoạch: 20-30 hình, phụ đề theo cụm từ, chuyển cảnh theo cấu trúc)
                import short_v2
                mp4, dur = short_v2.build(script, cfg, out_dir)
                if script["ngan"].get("ab_test"):
                    # kế hoạch (Âm thanh, C): thử A/B — thêm bản cũ chỉ ảnh + giọng đọc một lượt để so với bản mới
                    try:
                        short_v2.build(script, cfg, out_dir, variant="cu")
                    except Exception as e:
                        log(f"  ⚠️  Không dựng được bản cũ A/B: {e}")
            else:
                mp4, dur = render(script, cfg, out_dir, preview=a.preview, no_tts=a.no_tts)
                write_caption(script, cfg, out_dir)
            if script.get("post") and not a.preview:
                try:
                    import post
                    if script.get("ngan") and not any(sc.get("image_src") for sc in script["scenes"]):
                        # khung mới không tải ảnh theo "scenes" -> tải ở đây để album ảnh Facebook có ảnh nền
                        import images
                        images.fetch_scene_images(script, out_dir / "_work", log)
                    post.render_post(script, cfg, out_dir / "_work", out_dir, log)
                except Exception as e:
                    log(f"  ⚠️  Không tạo được bài đăng ảnh: {e}")
            log(f"✅ Xong {mp4.relative_to(ROOT) if mp4.is_relative_to(ROOT) else mp4}  ({dur:.1f}s video, mất {time.time() - t:.0f}s)")
            ok += 1
        except Exception as e:
            log(f"❌ {script['id']}: {e}")
            bad += 1
    log(f"\nTổng kết: {ok} thành công, {bad} lỗi, {skipped} bỏ qua")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
