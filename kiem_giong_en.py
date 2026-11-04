"""Nghe thử giọng RN1 bằng Gemini (nhận dạng âm thanh): cắt các câu có CROATOAN trong bản xem nhanh,
nhờ Gemini chép lại đúng như nghe thấy và ghi cách phát âm. Hết mọi khóa thì dừng ngay.
  python kiem_giong_en.py <video.mp4>
"""
import base64, json, subprocess, sys, urllib.request, urllib.error
from pathlib import Path
import gemini_keys

CLIPS = [("00:54.0", "00:01:00.6"), ("03:58.0", "04:07.0"), ("06:55.5", "07:01.6"),
         ("07:11.4", "07:16.4"), ("08:39.8", "08:45.4"), ("12:13.6", "12:18.3")]
MODELS = ["gemini-3.8-flash", "gemini-flash-latest"]
ASK = ("Listen to this clip of an English documentary narrator. 1) Transcribe it exactly as spoken. "
       "2) The text contains the word Croatoan (a place name; correct pronunciation is kro-uh-TAN, "
       "also acceptable: kro-uh-TOH-an). Spell phonetically, syllable by syllable with the stressed syllable in CAPITALS, "
       "how the narrator actually says it each time. 3) Say whether the word is clearly pronounced and whether "
       "any extra words (like instructions) were spoken that are not in the transcript. Be short and literal.")


def ask(b64, key):
    import time
    last = ""
    for m in MODELS * 5:
        time.sleep(0 if not last else 20)
        body = {"contents": [{"parts": [{"text": ASK}, {"inline_data": {"mime_type": "audio/mp3", "data": b64}}]}]}
        req = urllib.request.Request(
            f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent",
            data=json.dumps(body).encode(), method="POST",
            headers={"Content-Type": "application/json", "x-goog-api-key": key})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.loads(r.read())["candidates"][0]["content"]["parts"][0]["text"]
        except urllib.error.HTTPError as e:
            last = f"{m} HTTP {e.code}: {e.read().decode('utf-8','replace')[:200]}"; print("   ", last[:230], flush=True)
            if e.code in (429, 402, 403):
                raise RuntimeError(last)
        except Exception as e:
            last = str(e)
    raise ValueError(last)


def main():
    vid = sys.argv[1]
    out = Path("output/_kiem_giong"); out.mkdir(parents=True, exist_ok=True)
    for i, (a, b) in enumerate(CLIPS, 1):
        mp3 = out / f"c{i}.mp3"
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", a if a.count(":") == 2 else "00:" + a, "-to",
                        b if b.count(":") == 2 else "00:" + b, "-i", vid, "-vn", "-ac", "1", "-ar", "24000", str(mp3)], check=True)
        b64 = base64.b64encode(mp3.read_bytes()).decode()
        while True:
            key = gemini_keys.current()
            if not key:
                print("⛔ Mọi khóa Gemini đều hết lượt: DỪNG.", flush=True); sys.exit(3)
            try:
                print(f"\n=== Clip {i} ({a}–{b}) ===\n{ask(b64, key)}", flush=True); break
            except RuntimeError as e:
                print(f"   khóa …{key[-4:]} hết lượt: {str(e)[:80]}, đổi khóa", flush=True)
                gemini_keys.mark_bad(key, str(e))
            except ValueError as e:
                print(f"   clip {i} lỗi: {e}", flush=True); break


if __name__ == "__main__":
    main()
