"""Cloudflare FLUX.2 klein 4B vẽ ảnh tập 3 cho cảnh không có nhân vật chính (danh sách trong cf_tq3_keys.json). Mỗi cảnh 2 bản (a, b).
Cảnh không người dùng ảnh mẫu tông (không có người); cảnh quân đội/đám đông không dùng ảnh mẫu (tránh chép người). Tự chuyển tài khoản khi hết lượt."""
import base64, json, os, urllib.request, urllib.error, uuid
from pathlib import Path
ROOT = Path(__file__).resolve().parent
accs = []
for suf in ("", "_2", "_3"):
    a = os.environ.get("CF_ACCOUNT_ID" + suf, "").strip(); t = os.environ.get("CF_API_TOKEN" + suf, "").strip()
    if a and t: accs.append((a, t))
items = {x["key"]: x for x in json.loads((ROOT/"ke-hoach/nhan-vat/TQ3_anh.json").read_text(encoding="utf-8"))}
keys = json.loads((ROOT/"cf_tq3_keys.json").read_text())
out = ROOT/"assets/anh_2d/CF_TQ3"; out.mkdir(parents=True, exist_ok=True)
style = ROOT/"assets/anh_2d/CF_thu/035_co_mau.jpg"
cur = 0; log = []
def multipart(fields, files):
    b = uuid.uuid4().hex; body = b""
    for k, v in fields.items():
        body += f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode()
    for k, (fn, data) in files.items():
        body += f'--{b}\r\nContent-Disposition: form-data; name="{k}"; filename="{fn}"\r\nContent-Type: image/jpeg\r\n\r\n'.encode() + data + b"\r\n"
    return body + f"--{b}--\r\n".encode(), f"multipart/form-data; boundary={b}"
def run(name, prompt, ref=None):
    global cur
    while cur < len(accs):
        a, t = accs[cur]
        url = f"https://api.cloudflare.com/client/v4/accounts/{a}/ai/run/@cf/black-forest-labs/flux-2-klein-4b"
        body, ct = multipart({"prompt": prompt, "width": "1344", "height": "768", "steps": "4"}, {"input_image_0": (ref.name, ref.read_bytes())} if ref else {})
        req = urllib.request.Request(url, data=body, method="POST", headers={"Authorization": f"Bearer {t}", "Content-Type": ct})
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                img = (json.loads(r.read().decode()).get("result") or {}).get("image")
            if img:
                (out/f"{name}.jpg").write_bytes(base64.b64decode(img)); log.append(f"{name}: OK (tk {cur+1})"); return
            log.append(f"{name}: không có ảnh"); return
        except urllib.error.HTTPError as e:
            m = e.read().decode("utf-8", "replace")
            if "neurons" in m or "4006" in m:
                log.append(f"tk {cur+1} hết lượt"); cur += 1; continue
            log.append(f"{name}: HTTP {e.code} {m[:200]}"); return
        except Exception as e:
            log.append(f"{name}: {e}"); return
    log.append(f"{name}: hết tài khoản")
for k in keys:
    it = items[k]
    ref = style if (not it["nv"] and k != "035" and style.exists()) else None
    pre = "Draw in exactly the same drawing style, line weight and colours as the reference image, but a completely different place and no people from the reference. " if ref else ""
    for v in "ab":
        if (out/f"{k}_{v}.jpg").exists(): continue
        run(f"{k}_{v}", pre + it["prompt"], ref)
(out/"nhat_ky.txt").write_text("\n".join(log), encoding="utf-8"); print("\n".join(log))
