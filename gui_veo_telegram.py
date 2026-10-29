"""Gửi từng ảnh chibi kèm prompt Google Flow (ảnh -> video) vào Telegram.
  python gui_veo_telegram.py lt1            -> gửi mọi cảnh trong ke-hoach/chibi/<mã>_veo.json
  python gui_veo_telegram.py lt1 19004,19024 -> chỉ gửi các đoạn này
Đầu vào: ke-hoach/chibi/<mã>_veo.json = [{"n": số đoạn, "prompt": "..."}]; ảnh: assets/anh_chibi/<mã>/<n>.jpg.
Cần biến môi trường TG_TOKEN; chat lấy từ TG_CHAT hoặc telegram_chat_id.txt. Prompt không có tên riêng người thật (chạy kiem_prompt_veo.py trước)."""
import json, os, sys, time, uuid, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def post_photo(token, chat, path, cap):
    b = uuid.uuid4().hex
    body = b""
    for k, v in (("chat_id", chat), ("caption", cap)):
        body += f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode()
    body += (f'--{b}\r\nContent-Disposition: form-data; name="photo"; filename="{path.name}"\r\n'
             f'Content-Type: image/jpeg\r\n\r\n').encode() + path.read_bytes() + f"\r\n--{b}--\r\n".encode()
    req = urllib.request.Request(f"https://api.telegram.org/bot{token}/sendPhoto", data=body,
                                 headers={"Content-Type": f"multipart/form-data; boundary={b}"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r).get("ok")


def main():
    ma = sys.argv[1] if len(sys.argv) > 1 else "lt1"
    items = json.loads((ROOT / "ke-hoach" / "chibi" / f"{ma}_veo.json").read_text(encoding="utf-8"))
    if len(sys.argv) > 2 and sys.argv[2]:
        want = {int(x) for x in sys.argv[2].replace(" ", "").split(",") if x}
        items = [i for i in items if i["n"] in want]
    token = os.environ.get("TG_TOKEN", "")
    f = ROOT / "telegram_chat_id.txt"
    chat = os.environ.get("TG_CHAT") or (f.read_text().strip() if f.exists() else "")
    if not (token and chat):
        sys.exit("Thiếu TG_TOKEN hoặc chat id")
    bad = 0
    for it in items:
        img = ROOT / "assets" / "anh_chibi" / ma / f"{it['n']}.jpg"
        cap = f"Ảnh {it['n']} — prompt Google Flow:\n{it['prompt']}"[:1024]
        try:
            assert img.exists(), "thiếu ảnh"
            print(it["n"], "gửi", "ok" if post_photo(token, chat, img, cap) else "LỖI", flush=True)
            time.sleep(1.5)
        except Exception as e:
            bad += 1; print(it["n"], "LỖI", type(e).__name__, e, flush=True)
    sys.exit(1 if bad else 0)


main()
