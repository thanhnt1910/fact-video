"""Thử MỘT lần gọi Cloudflare Workers AI (FLUX.1 schnell) với prompt chibi cảnh 004 của NB1. Không in token."""
import base64, json, os, urllib.error, urllib.request
from pathlib import Path

items = json.loads(Path("ke-hoach/nhan-vat/NB1_anh.json").read_text(encoding="utf-8"))
prompt = next(i["prompt"] for i in items if i["key"] == "004")[:2000]
a = os.environ.get("CF_ACCOUNT_ID", "").strip()
t = os.environ.get("CF_API_TOKEN", "").strip()
Path("logs").mkdir(exist_ok=True)
if not a or not t:
    msg = "Chưa có CF_ACCOUNT_ID / CF_API_TOKEN"
else:
    url = f"https://api.cloudflare.com/client/v4/accounts/{a}/ai/run/@cf/black-forest-labs/flux-1-schnell"
    req = urllib.request.Request(url, data=json.dumps({"prompt": prompt, "steps": 8}).encode(), method="POST",
                                 headers={"Authorization": f"Bearer {t}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            res = json.loads(r.read().decode())
        img = (res.get("result") or {}).get("image")
        if img:
            out = Path("assets/anh_2d/NB1_cf"); out.mkdir(parents=True, exist_ok=True)
            (out / "004.jpg").write_bytes(base64.b64decode(img))
            msg = "OK: đã vẽ 1 ảnh"
        else:
            msg = "Không có ảnh: " + json.dumps(res)[:300]
    except urllib.error.HTTPError as e:
        msg = f"HTTP {e.code}: " + e.read().decode("utf-8", "replace")[:300]
    except Exception as e:
        msg = f"Lỗi: {e}"
Path("logs/cf_chibi_thu.txt").write_text(msg + "\n", encoding="utf-8")
print(msg)
