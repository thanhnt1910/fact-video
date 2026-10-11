"""Kiểm tra các tài khoản Cloudflare (CF_ACCOUNT_ID[_2,_3] + CF_API_TOKEN[_2,_3]): token hợp lệ không, vẽ thử 1 ảnh nhỏ
bằng FLUX.1 schnell (~60 neurons) xem còn lượt miễn phí không. Không in token ra log."""
import base64
import json
import os
import urllib.error
import urllib.request
from pathlib import Path

lines = []
for suf in ("", "_2", "_3"):
    a = os.environ.get("CF_ACCOUNT_ID" + suf, "").strip()
    t = os.environ.get("CF_API_TOKEN" + suf, "").strip()
    name = f"Tài khoản {suf or '_1'} (CF_ACCOUNT_ID{suf} / CF_API_TOKEN{suf})"
    if not a and not t:
        lines.append(f"{name}: chưa có")
        continue
    if not a or not t:
        lines.append(f"{name}: THIẾU {'CF_ACCOUNT_ID' + suf if not a else 'CF_API_TOKEN' + suf}")
        continue
    url = f"https://api.cloudflare.com/client/v4/accounts/{a}/ai/run/@cf/black-forest-labs/flux-1-schnell"
    req = urllib.request.Request(url, data=json.dumps({"prompt": "a small red apple on a wooden table", "steps": 4}).encode(),
                                 method="POST", headers={"Authorization": f"Bearer {t}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            res = json.loads(r.read().decode())
        img = (res.get("result") or {}).get("image")
        ok = bool(img) and len(base64.b64decode(img)) > 5000
        lines.append(f"{name}: ✅ vẽ thử được" if ok else f"{name}: ⚠️ không có ảnh trả về: {json.dumps(res)[:200]}")
    except urllib.error.HTTPError as e:
        msg = e.read().decode("utf-8", "replace")
        if "neurons" in msg or "4006" in msg:
            lines.append(f"{name}: ⛔ token đúng nhưng đã HẾT LƯỢT miễn phí hôm nay")
        elif e.code in (401, 403) or "10000" in msg:
            lines.append(f"{name}: ❌ token sai hoặc thiếu quyền Workers AI (HTTP {e.code}): {msg[:200]}")
        else:
            lines.append(f"{name}: ❌ HTTP {e.code}: {msg[:200]}")
    except Exception as e:
        lines.append(f"{name}: ❌ {e}")
Path("logs").mkdir(exist_ok=True)
Path("logs/cf_kiemtra.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines))
