"""Kiểm tra khóa GEMINI_API_KEY: đọc thử 1 câu bằng từng model TTS và gọi thử 1 model chữ. Ghi logs/gemini_kiemtra.txt."""
import base64, json, os, time, urllib.request, urllib.error
from datetime import datetime, timezone
KEY = os.environ.get("GEMINI_API_KEY", "").strip()
API = "https://generativelanguage.googleapis.com/v1beta"
out = [f"Kiểm tra lúc {datetime.now(timezone.utc):%Y-%m-%d %H:%M:%S} UTC", f"Có khóa: {'có' if KEY else 'KHÔNG'}"]

def call(model, body):
    req = urllib.request.Request(f"{API}/models/{model}:generateContent", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json", "x-goog-api-key": KEY})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        t = e.read().decode("utf-8", "ignore")
        try:
            msg = json.loads(t)["error"]["message"]
        except Exception:
            msg = t
        return e.code, msg[:220].replace("\n", " ")

tts = {"contents": [{"parts": [{"text": "Xin chào, đây là câu đọc thử."}]}],
       "generationConfig": {"responseModalities": ["AUDIO"],
                            "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": "Sadaltager"}}}}}
for m in ("gemini-3.1-flash-tts-preview", "gemini-2.5-flash-preview-tts"):
    c, r = call(m, tts)
    ok = c == 200 and "inlineData" in json.dumps(r)
    out.append(f"TTS {m}: {'✅ đọc được' if ok else '⛔ HTTP ' + str(c)} {'' if ok else r}")
    time.sleep(2)
for m in ("gemini-flash-lite-latest", "gemini-flash-latest"):
    c, r = call(m, {"contents": [{"parts": [{"text": "Trả lời: ok"}]}]})
    out.append(f"Chữ {m}: {'✅ dùng được' if c == 200 else '⛔ HTTP ' + str(c) + ' ' + str(r)}")
    time.sleep(2)
open("logs/gemini_kiemtra.txt", "w", encoding="utf-8").write("\n".join(out) + "\n")
print("\n".join(out))
