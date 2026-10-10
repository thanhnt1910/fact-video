"""
Phụ đề (.srt) và bản dịch tiếng Anh cho video dài.

- Phụ đề tiếng Việt: lấy đúng lời đọc, chia theo câu, khớp thời gian từng đoạn ảnh (beat).
- Bản tiếng Anh: Gemini (mô hình chữ, miễn phí) dịch tiêu đề, mô tả, tên chương và từng beat.
  Kết quả được lưu tạm (assets/tts_cache/tr_*.json) để lần sau không phải dịch lại.
Không đốt chữ lên video: đây là phụ đề rời, người xem tự bật (CC) trên YouTube.
"""
import hashlib
import json
import os
import re
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CACHE = ROOT / "assets" / "tts_cache"
API = "https://generativelanguage.googleapis.com/v1beta"
TEXT_MODELS = ["gemini-flash-latest", "gemini-2.5-flash", "gemini-2.0-flash"]
MAX_LINE = 42


# ------------------------------------------------------------------ chia câu, xếp thời gian
def _sentences(text):
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", " ".join(text.split()))
    parts = re.split(r"(?<=[.!?…])\s+", text)
    out = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        # câu quá dài -> tách ở dấu phẩy cho vừa 2 dòng
        while len(p) > 2 * MAX_LINE:
            cut = p.rfind(", ", 0, 2 * MAX_LINE)
            if cut < MAX_LINE // 2:
                cut = p.rfind(" ", 0, 2 * MAX_LINE)
            if cut <= 0:
                break
            out.append(p[:cut + 1].strip())
            p = p[cut + 1:].strip()
        out.append(p)
    return out


def _wrap(s):
    if len(s) <= MAX_LINE:
        return s
    mid = len(s) // 2
    left, right = s.rfind(" ", 0, mid + 1), s.find(" ", mid)
    cut = left if left > 0 and (right < 0 or mid - left <= right - mid) else right
    return s if cut <= 0 else s[:cut] + "\n" + s[cut + 1:]


def cues(segments):
    """segments: [(start, end, text)] theo từng beat -> cue phụ đề theo câu, chia thời gian theo độ dài chữ."""
    out = []
    for start, end, text in segments:
        sents = _sentences(text or "")
        if not sents:
            continue
        total = sum(len(s) for s in sents)
        t = start
        for s in sents:
            d = (end - start) * len(s) / total
            out.append((t, t + d - 0.05, _wrap(s)))
            t += d
    return out


def _ts(t):
    t = max(0.0, t)
    h, r = divmod(int(round(t * 1000)), 3600000)
    m, r = divmod(r, 60000)
    s, ms = divmod(r, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def write_srt(path, cs):
    lines = []
    for i, (a, b, text) in enumerate(cs, 1):
        lines += [str(i), f"{_ts(a)} --> {_ts(b)}", text, ""]
    Path(path).write_text("\n".join(lines), encoding="utf-8")
    return path


# ------------------------------------------------------------------ dịch bằng Gemini
PROMPT = """You translate Vietnamese content of a YouTube history-documentary channel ("Người Gác Sử", true strange stories from world history) into natural, engaging English for international viewers.

Rules:
- Return JSON with exactly the same keys as the input. "chapters" and "lines" must have exactly the same number of items, in the same order, one output item per input item.
- "title": a punchy English YouTube title, at most 95 characters (you may restructure it, e.g. "Why ...? | Event name").
- "description": 2–4 sentences, curiosity-driven, no spoilers of the final answer.
- "lines": faithful subtitle translations of the narration, concise and natural; keep "…" pauses where meaningful.
- Keep proper names in their original spelling (Strasbourg, Hiroo Onoda, Lubang…). Write numbers and years as digits (e.g. "năm một nghìn năm trăm mười tám" -> "1518").
- Do not add facts that are not in the source.
- Also add "hashtags": 4–6 short English hashtags without the # sign.

Input JSON:
"""


def _post(url, body, key, timeout=180):
    import urllib.error
    import urllib.request
    req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"), method="POST",
                                 headers={"Content-Type": "application/json", "x-goog-api-key": key})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:300]}")


def translate(payload, log=print):
    """payload: {title, description, chapters[], lines[]} tiếng Việt -> bản tiếng Anh (dict) hoặc None."""
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True)
    cache = CACHE / f"tr_{hashlib.sha1(raw.encode()).hexdigest()[:16]}.json"
    if cache.exists():
        return json.loads(cache.read_text(encoding="utf-8"))
    if not key:
        log("     ⚠️  chưa có GEMINI_API_KEY, bỏ qua bản tiếng Anh")
        return None
    body = {"contents": [{"parts": [{"text": PROMPT + json.dumps(payload, ensure_ascii=False, indent=1)}]}],
            "generationConfig": {"responseMimeType": "application/json", "temperature": 0.3}}
    errs = []
    for model in TEXT_MODELS:
        for attempt in range(4):
            try:
                res = _post(f"{API}/models/{model}:generateContent", body, key)
                text = "".join(p.get("text", "") for p in res["candidates"][0]["content"]["parts"])
                en = json.loads(re.sub(r"^```(?:json)?|```$", "", text.strip()).strip())
                if len(en.get("lines", [])) != len(payload["lines"]) or \
                        len(en.get("chapters", [])) != len(payload["chapters"]):
                    raise RuntimeError("số dòng dịch không khớp")
                CACHE.mkdir(parents=True, exist_ok=True)
                cache.write_text(json.dumps(en, ensure_ascii=False, indent=1), encoding="utf-8")
                log(f"     🌐 dịch tiếng Anh xong ({model})")
                return en
            except Exception as e:
                msg = str(e)
                if ("429" in msg or "503" in msg or "500" in msg) and attempt < 3:
                    time.sleep(20 * (attempt + 1))
                    continue
                errs.append(f"{model}: {msg[:200]}")
                break
    log("     ⚠️  không dịch được tiếng Anh: " + " | ".join(errs))
    return None
