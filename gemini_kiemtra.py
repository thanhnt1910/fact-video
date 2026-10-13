"""Kiểm tra mọi khóa Gemini trong GitHub Secrets: GEMINI_API_KEY, GEMINI_API_KEY_2 ... _12, và GEMINI_API_KEYS (nhiều khóa, cách nhau dấu phẩy/xuống dòng).
Báo: tên secret nào có, khóa nào TRÙNG nhau (so bằng dấu vân tay, không in khóa), khóa nào đọc giọng/dùng chữ được. Ghi logs/gemini_kiemtra.txt."""
import hashlib, json, os, re, time, urllib.request, urllib.error
from datetime import datetime, timezone

API = "https://generativelanguage.googleapis.com/v1beta"
out = [f"Kiểm tra lúc {datetime.now(timezone.utc):%Y-%m-%d %H:%M:%S} UTC"]

names = ["GEMINI_API_KEY"] + [f"GEMINI_API_KEY_{i}" for i in range(2, 13)]
keys = []  # (nhãn, khóa)
for n in names:
    v = os.environ.get(n, "").strip()
    if v:
        keys.append((n, v))
for k, v in enumerate(re.split(r"[,\s]+", os.environ.get("GEMINI_API_KEYS", "").strip())):
    if v:
        keys.append((f"GEMINI_API_KEYS#{k + 1}", v))


def fp(k):
    return hashlib.sha256(k.encode()).hexdigest()[:8]


def call(key, model, body):
    req = urllib.request.Request(f"{API}/models/{model}:generateContent", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json", "x-goog-api-key": key})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        t = e.read().decode("utf-8", "ignore")
        try:
            j = json.loads(t)["error"]
            msg = f"{j.get('status', '')}: {j.get('message', '')}"
        except Exception:
            msg = t
        return e.code, msg[:160].replace("\n", " ")
    except Exception as e:
        return 0, str(e)[:160]


tts = {"contents": [{"parts": [{"text": "Xin chào, đây là câu đọc thử."}]}],
       "generationConfig": {"responseModalities": ["AUDIO"],
                            "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": "Sadaltager"}}}}}
out.append(f"Số khóa tìm thấy: {len(keys)}")
seen = {}
for label, k in keys:
    f = fp(k)
    dup = seen.get(f)
    seen.setdefault(f, label)
    out.append(f"\n[{label}] dấu vân tay {f}, độ dài {len(k)}" + (f"  ⚠️ TRÙNG với {dup}" if dup else ""))
    if dup:
        continue
    for m in ("gemini-3.1-flash-tts-preview", "gemini-2.5-flash-preview-tts"):
        c, r = call(k, m, tts)
        ok = c == 200 and "inlineData" in json.dumps(r)
        out.append(f"   TTS {m}: {'✅ đọc được' if ok else '⛔ HTTP ' + str(c) + ' ' + str(r)}")
        time.sleep(2)
    c, r = call(k, "gemini-flash-lite-latest", {"contents": [{"parts": [{"text": "Trả lời: ok"}]}]})
    out.append(f"   Chữ flash-lite: {'✅ dùng được' if c == 200 else '⛔ HTTP ' + str(c) + ' ' + str(r)}")
    time.sleep(2)
open("logs/gemini_kiemtra.txt", "w", encoding="utf-8").write("\n".join(out) + "\n")
print("\n".join(out))
