"""Vẽ thử FLUX.2 klein 4B trên Cloudflare Workers AI: 3 cảnh vật tập 3, có và không có ảnh mẫu tông. Không in token."""
import base64, json, os, sys, urllib.request, urllib.error, uuid
from pathlib import Path
ROOT = Path(__file__).resolve().parent
a = os.environ.get("CF_ACCOUNT_ID", "").strip(); t = os.environ.get("CF_API_TOKEN", "").strip()
URL = f"https://api.cloudflare.com/client/v4/accounts/{a}/ai/run/@cf/black-forest-labs/flux-2-klein-4b"
items = {x["key"]: x for x in json.loads((ROOT/"ke-hoach/nhan-vat/TQ3_anh.json").read_text(encoding="utf-8"))}
out = ROOT/"assets/anh_2d/CF_thu"; out.mkdir(parents=True, exist_ok=True)
log = []
def multipart(fields, files):
    b = uuid.uuid4().hex; body = b""
    for k, v in fields.items():
        body += f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode()
    for k, (fn, data) in files.items():
        body += f'--{b}\r\nContent-Disposition: form-data; name="{k}"; filename="{fn}"\r\nContent-Type: image/jpeg\r\n\r\n'.encode() + data + b"\r\n"
    body += f"--{b}--\r\n".encode()
    return body, f"multipart/form-data; boundary={b}"
def run(name, prompt, refs=()):
    fields = {"prompt": prompt, "width": "1024", "height": "576", "steps": "4"}
    files = {f"input_image_{i}": (p.name, p.read_bytes()) for i, p in enumerate(refs)}
    body, ct = multipart(fields, files)
    req = urllib.request.Request(URL, data=body, method="POST", headers={"Authorization": f"Bearer {t}", "Content-Type": ct})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            res = json.loads(r.read().decode())
        img = (res.get("result") or {}).get("image")
        if img:
            (out/f"{name}.jpg").write_bytes(base64.b64decode(img)); log.append(f"{name}: OK ({len(refs)} ảnh mẫu)")
        else:
            log.append(f"{name}: không có ảnh: {json.dumps(res)[:300]}")
    except urllib.error.HTTPError as e:
        log.append(f"{name}: HTTP {e.code}: {e.read().decode('utf-8','replace')[:400]}")
    except Exception as e:
        log.append(f"{name}: {e}")
style = ROOT/"assets/anh_2d/TQ4/073.jpg"
for k in ("003", "035", "009"):
    run(f"{k}_khong_mau", items[k]["prompt"])
    if style.exists():
        run(f"{k}_co_mau", "Draw in exactly the same drawing style, line weight and colours as the reference image. " + items[k]["prompt"], [style])
(out/"nhat_ky.txt").write_text("\n".join(log), encoding="utf-8"); print("\n".join(log))
