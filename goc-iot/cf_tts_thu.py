"""Thử đọc tiếng Việt bằng Cloudflare Workers AI (MeloTTS) rồi nhận dạng lại bằng Whisper để xem có hiểu được không.
Dùng CF_ACCOUNT_ID[_2,_3] + CF_API_TOKEN[_2,_3]. Ra: goc-iot/logs/cf_tts.txt và goc-iot/logs/cf/*.mp3. Không in token."""
import base64, json, os, subprocess, time, urllib.error, urllib.request
from pathlib import Path
ROOT = Path(__file__).resolve().parent
out = ROOT / "logs" / "cf"; out.mkdir(parents=True, exist_ok=True)
TEXT = "Điều gì xảy ra nếu TV thông minh ghi lại bạn đang xem gì?"
lines = [time.strftime("Thử lúc %Y-%m-%d %H:%M:%S UTC", time.gmtime()), "Câu thử: " + TEXT]

def run(acc, tok, model, body):
    url = f"https://api.cloudflare.com/client/v4/accounts/{acc}/ai/run/{model}"
    req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST",
                                 headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as r:
        raw = r.read()
        ct = r.headers.get("Content-Type", "")
    return raw, ct

def dur(p):
    try:
        return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout.strip())
    except Exception:
        return 0.0

acc = tok = ""
for suf in ("", "_2", "_3"):
    a = os.environ.get("CF_ACCOUNT_ID" + suf, "").strip(); t = os.environ.get("CF_API_TOKEN" + suf, "").strip()
    if a and t:
        acc, tok = a, t; lines.append(f"Dùng tài khoản {suf or '_1'}"); break
if not acc:
    lines.append("THIẾU CF_ACCOUNT_ID / CF_API_TOKEN")
for lang in ("vi", "en"):
    if not acc: break
    try:
        raw, ct = run(acc, tok, "@cf/myshell-ai/melotts", {"prompt": TEXT, "lang": lang})
        if "json" in ct:
            res = json.loads(raw.decode()); au = (res.get("result") or {}).get("audio")
            if not au:
                lines.append(f"[melotts {lang}] không có audio: {json.dumps(res)[:300]}"); continue
            data = base64.b64decode(au)
        else:
            data = raw
        f = out / f"thu_{lang}.mp3"; f.write_bytes(data)
        lines.append(f"[melotts {lang}] OK {len(data)} byte, {dur(f):.2f}s")
        try:
            raw2, ct2 = run(acc, tok, "@cf/openai/whisper-large-v3-turbo", {"audio": base64.b64encode(data).decode(), "language": "vi"})
            res2 = json.loads(raw2.decode()); lines.append(f"  Whisper nghe được: {(res2.get('result') or {}).get('text', json.dumps(res2)[:200])!r}")
        except urllib.error.HTTPError as e:
            lines.append(f"  Whisper lỗi HTTP {e.code}: {e.read().decode('utf-8','replace')[:200]}")
        except Exception as e:
            lines.append(f"  Whisper lỗi: {e}")
    except urllib.error.HTTPError as e:
        lines.append(f"[melotts {lang}] HTTP {e.code}: {e.read().decode('utf-8','replace')[:300]}")
    except Exception as e:
        lines.append(f"[melotts {lang}] lỗi: {e}")
(ROOT / "logs" / "cf_tts.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines))
