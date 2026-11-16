"""Vẽ 3 ảnh thủy mặc NB3 bằng Cloudflare Workers AI (FLUX.1 schnell). Dừng ngay khi gặp 429. Không in token."""
import base64, json, os, urllib.error, urllib.request
from pathlib import Path

items = json.loads(Path("ke-hoach/nhan-vat/NB3_anh.json").read_text(encoding="utf-8"))
a = os.environ.get("CF_ACCOUNT_ID", "").strip()
t = os.environ.get("CF_API_TOKEN", "").strip()
Path("logs").mkdir(exist_ok=True)
out = Path("assets/anh_2d/NB3_cf"); out.mkdir(parents=True, exist_ok=True)
log = []
if not a or not t:
    log.append("Chưa có CF_ACCOUNT_ID / CF_API_TOKEN")
else:
    url = f"https://api.cloudflare.com/client/v4/accounts/{a}/ai/run/@cf/black-forest-labs/flux-1-schnell"
    for it in items:
        req = urllib.request.Request(url, data=json.dumps({"prompt": it["prompt"][:2000], "steps": 8}).encode(), method="POST",
                                     headers={"Authorization": f"Bearer {t}", "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                res = json.loads(r.read().decode())
            img = (res.get("result") or {}).get("image")
            if img:
                (out / f"{it['key']}.jpg").write_bytes(base64.b64decode(img))
                log.append(f"{it['key']}: OK")
            else:
                log.append(f"{it['key']}: không có ảnh " + json.dumps(res)[:200])
        except urllib.error.HTTPError as e:
            log.append(f"{it['key']}: HTTP {e.code} " + e.read().decode("utf-8", "replace")[:200])
            if e.code == 429:
                log.append("429: dừng, không gọi thêm"); break
        except Exception as e:
            log.append(f"{it['key']}: lỗi {e}")
Path("logs/cf_thuy_mac.txt").write_text("\n".join(log) + "\n", encoding="utf-8")
print("\n".join(log))
