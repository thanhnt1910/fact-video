"""Tải ảnh theo danh sách JSON [{n,url,cap}], thu về tối đa 2000px, lưu vào thư mục, rồi gửi Telegram từng ảnh.
Dùng: python gui_anh_json.py telegram/anh_sl21.json telegram/anh_fb/SL21"""
import json, os, sys, io, urllib.request, urllib.parse, uuid
from pathlib import Path
from PIL import Image

UA = {"User-Agent": "fact-video/1.0 (https://github.com/thanhnt1910/fact-video; image fetch)"}

def post_photo(token, chat, path, cap):
    b = uuid.uuid4().hex
    body = b""
    for k, v in (("chat_id", chat), ("caption", cap)):
        body += f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode()
    body += f'--{b}\r\nContent-Disposition: form-data; name="photo"; filename="{path.name}"\r\nContent-Type: image/jpeg\r\n\r\n'.encode() + path.read_bytes() + f"\r\n--{b}--\r\n".encode()
    req = urllib.request.Request(f"https://api.telegram.org/bot{token}/sendPhoto", data=body, headers={"Content-Type": f"multipart/form-data; boundary={b}"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r).get("ok")

def main():
    items = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
    token, chat = os.environ.get("TG_TOKEN"), os.environ.get("TG_CHAT") or (Path("telegram_chat_id.txt").read_text().strip() if Path("telegram_chat_id.txt").exists() else "")
    bad = 0
    for it in items:
        p = out / f"{it['n']:02d}.jpg"
        try:
            req = urllib.request.Request(it["url"], headers=UA)
            with urllib.request.urlopen(req, timeout=120) as r:
                im = Image.open(io.BytesIO(r.read())).convert("RGB")
            im.thumbnail((2000, 2000)); im.save(p, quality=90)
            print(it["n"], "tải ok", im.size)
            if token and chat:
                print(it["n"], "gửi", "ok" if post_photo(token, chat, p, it["cap"]) else "LỖI")
        except Exception as e:
            bad += 1; print(it["n"], "LỖI", type(e).__name__, e)
    return 1 if bad else 0

sys.exit(main())
