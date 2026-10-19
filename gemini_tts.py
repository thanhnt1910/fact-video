"""
Giọng đọc Google Gemini TTS: điều khiển cách đọc bằng lời mô tả (giọng kể chuyện, hồi hộp, hào hứng…).
Cần biến môi trường GEMINI_API_KEY (lấy miễn phí ở aistudio.google.com/apikey).

Thử lần lượt:
  1) Interactions API với model gemini-3.8-flash-tts (style trong speech_metadata, chữ đọc nguyên văn)
  2) generateContent với gemini-2.5-flash-preview-tts (style viết thành lời dặn đứng trước đoạn đọc)
"""
import base64
import io
import json
import os
import re
import time
import urllib.error
import urllib.request
import wave

API = "https://generativelanguage.googleapis.com/v1beta"
MODELS_NEW = ["gemini-3.8-flash-tts", "gemini-3.1-flash-tts-preview"]
MODELS_OLD = ["gemini-2.5-flash-preview-tts", "gemini-2.5-pro-preview-tts"]

# Lời "đạo diễn" mặc định cho kênh
BASE_STYLE = ("Native Vietnamese narrator (Northern accent, Hanoi) for a short true-history storytelling video. "
              "Warm, captivating storyteller with a hint of mystery, like telling a strange true tale by lantern light: "
              "clear diction, natural Vietnamese tones, "
              "varied pace — slow down and lower the voice before a surprising fact, then reveal it with "
              "energy and a smile; pause briefly at '…'. Never robotic, never news-anchor flat.")

SCENE_STYLE = {
    "hook": "Open with suspense: a slightly hushed, intriguing question, then a punchy, amazed reveal.",
    "compare": "Playful contrast, ask the question with genuine curiosity.",
    "explain": "Friendly explainer, confident and clear, medium pace.",
    "number": "Emphasize the number slowly and impressively.",
    "timeline": "Calm storytelling pace, like guiding the listener through time.",
    "text": "Build up, then deliver the surprising fact with excitement.",
    "outro": "Upbeat, satisfied wrap-up; say 'Hóa ra là vậy!' with a delighted, knowing tone; friendly call to follow.",
}

TAG_STYLE = {
    "nhấn": "emphasized, slower and stronger", "nhan": "emphasized, slower and stronger",
    "nhanh": "a bit faster, light", "chậm": "slower and clear", "cham": "slower and clear",
    "cao": "excited, higher pitch", "trầm": "lower, mysterious", "tram": "lower, mysterious",
    "nhỏ": "softly, like telling a secret", "nho": "softly, like telling a secret",
}


def clean_text(text, pronounce=None):
    """Bỏ thẻ [..] của hệ thống cũ, áp dụng cách đọc tên riêng; trả về (chữ đọc, gợi ý nhấn nhá)."""
    hints = []
    for m in re.finditer(r"\[([^\]]+)\]\s*([^.!?…]*)", text):
        tag = m.group(1).strip().lower()
        if tag in TAG_STYLE and m.group(2).strip():
            hints.append(f'"{m.group(2).strip()[:60]}" → {TAG_STYLE[tag]}')
    t = re.sub(r"\[[^\]]*\]\s*", "", text).strip()
    for k, v in (pronounce or {}).items():
        t = t.replace(k, v)
    return t, hints


def _post(url, body, key, timeout=120):
    req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"), method="POST",
                                 headers={"Content-Type": "application/json", "x-goog-api-key": key})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:600]}")


def _wav_from_any(raw, mime=""):
    """Trả về bytes WAV (24 kHz mono 16-bit) từ WAV hoặc PCM thô."""
    if raw[:4] == b"RIFF":
        return raw
    buf = io.BytesIO()
    rate = 24000
    m = re.search(r"rate=(\d+)", mime or "")
    if m:
        rate = int(m.group(1))
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(raw)
    return buf.getvalue()


def _synth_interactions(model, text, style, voice, key):
    body = {
        "model": model,
        "input": [{"type": "user_input", "content": [{
            "type": "text", "text": text,
            "annotations": [{"type": "speech_metadata", "style": style}]}]}],
        "response_format": {"type": "audio"},
        "generation_config": {"speech_config": [{"voice": voice}]},
    }
    res = _post(f"{API}/interactions", body, key)
    for step in reversed(res.get("steps", [])):
        for c in reversed(step.get("content", []) or []):
            if c.get("type") == "audio" and c.get("data"):
                return _wav_from_any(base64.b64decode(c["data"]), c.get("mime_type", ""))
    raise RuntimeError("không thấy audio trong phản hồi: " + json.dumps(res)[:400])


def _synth_generate(model, text, style, voice, key):
    prompt = f"{style}\n\nRead the following Vietnamese text aloud exactly as written:\n{text}"
    body = {"contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseModalities": ["AUDIO"],
                                 "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}}}
    res = _post(f"{API}/models/{model}:generateContent", body, key)
    part = res["candidates"][0]["content"]["parts"][0]["inlineData"]
    return _wav_from_any(base64.b64decode(part["data"]), part.get("mimeType", ""))


MAX_WAIT = int(os.environ.get("GEMINI_MAX_WAIT", "900"))
_WORKING = {}


def synth(text, style, voice, key=None, log=print):
    """Đọc 1 đoạn. Trả về bytes WAV. Tự nhớ cách gọi nào chạy được."""
    import gemini_keys
    fixed = key
    if not (fixed or gemini_keys.has_key()):
        raise RuntimeError("Chưa có GEMINI_API_KEY")
    order = ([_WORKING["way"]] if "way" in _WORKING else []) + \
            [("i", m) for m in MODELS_NEW] + [("g", m) for m in MODELS_OLD]
    errs = []
    for way in order:
        kind, model = way
        waited, attempt, shown = 0, 0, False
        while True:
            try:
                fn = _synth_interactions if kind == "i" else _synth_generate
                key = fixed or gemini_keys.current()
                if not key:   # mọi khóa đang nghỉ: đợi khóa sớm nhất
                    w = min(120, gemini_keys.wait_seconds() + 1)
                    log(f"   [gemini] mọi khóa đang hết lượt, đợi {w:.0f}s…")
                    waited += w
                    if waited >= MAX_WAIT:
                        raise RuntimeError("mọi khóa Gemini đều hết lượt")
                    time.sleep(w)
                    continue
                wav = fn(model, text, style, voice, key)
                try:   # ghi chi phí ước tính: âm thanh Gemini = 25 token/giây, chữ ≈ 4 ký tự/token
                    import chi_phi
                    with wave.open(io.BytesIO(wav)) as w:
                        sec = w.getnframes() / float(w.getframerate())
                    chi_phi.add_tokens("tts", model, len(text + style) / 4, sec * 25)
                except Exception:
                    pass
                if "way" not in _WORKING:
                    _WORKING["way"] = way
                    log(f"   [gemini] dùng {model} ({'interactions' if kind == 'i' else 'generateContent'})")
                return wav
            except Exception as e:
                msg = str(e)
                if not fixed and key and gemini_keys.is_quota_error(msg) and "HTTP" in msg:
                    more = gemini_keys.mark_bad(key, msg)
                    log(f"   [gemini] khóa …{key[-4:]} hết lượt/bị từ chối ({msg[:60]!r}), đổi khóa"
                        + ("" if more else " (hết khóa dự phòng)"))
                    if more:
                        continue
                if ("429" in msg or "RESOURCE_EXHAUSTED" in msg or "503" in msg or "500" in msg) and waited < MAX_WAIT:
                    if not shown:
                        log(f"   [gemini] {model} báo: {' '.join(msg.split())[:260]}")
                        shown = True
                    # máy chủ thường nói rõ cần đợi bao lâu ("retryDelay": "37s" / "retry in 37.2s")
                    m = re.search(r'retry(?:Delay"?\s*:\s*"?| in )\s*([0-9.]+)\s*s', msg, re.I)
                    wait = min(120, float(m.group(1)) + 2) if m else min(90, 15 * (attempt + 1))
                    attempt += 1
                    waited += wait
                    log(f"   [gemini] {model} bận/giới hạn, đợi {wait:.0f}s…")
                    time.sleep(wait)
                    continue
                errs.append(f"{model}: {msg[:300]}")
                break
    raise RuntimeError("Gemini TTS lỗi:\n  " + "\n  ".join(errs))


def scene_style(scene_type, hints=None, extra=""):
    s = BASE_STYLE + " " + SCENE_STYLE.get(scene_type, "")
    if hints:
        s += " Specific emphasis: " + "; ".join(hints) + "."
    if extra:
        s += " " + extra
    return s
