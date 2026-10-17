"""Cloudflare FLUX.2 klein 4B vẽ ảnh theo cf_job.json: {"ma":"TQ4","keys":["001"],"vars":"ab","refs":true}.
Prompt lấy từ ke-hoach/nhan-vat/<ma>_anh.json; nếu refs=true thì gắn ảnh tham chiếu (refs của từng cảnh, tối đa 3) làm input_image_N.
Ảnh ra assets/anh_2d/CF_<ma>/<key>_<bản>.jpg. Tự chuyển tài khoản khi hết lượt."""
import base64, json, os, urllib.request, urllib.error, uuid
from pathlib import Path
ROOT = Path(__file__).resolve().parent
job = json.loads((ROOT/"cf_job.json").read_text(encoding="utf-8"))
ma = job["ma"]; vars_ = job.get("vars", "ab"); use_refs = job.get("refs", False)
accs = []
for suf in ("", "_2", "_3"):
    a = os.environ.get("CF_ACCOUNT_ID" + suf, "").strip(); t = os.environ.get("CF_API_TOKEN" + suf, "").strip()
    if a and t: accs.append((a, t))
items = {x["key"]: x for x in json.loads((ROOT/f"ke-hoach/nhan-vat/{ma}_anh.json").read_text(encoding="utf-8"))}
out = ROOT/f"assets/anh_2d/CF_{ma}"; out.mkdir(parents=True, exist_ok=True)
RD = ROOT/"ke-hoach/nhan-vat/refs"
cur = 0; log = []
def multipart(fields, files):
    b = uuid.uuid4().hex; body = b""
    for k, v in fields.items():
        body += f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode()
    for k, (fn, data) in files.items():
        body += f'--{b}\r\nContent-Disposition: form-data; name="{k}"; filename="{fn}"\r\nContent-Type: image/jpeg\r\n\r\n'.encode() + data + b"\r\n"
    return body + f"--{b}--\r\n".encode(), f"multipart/form-data; boundary={b}"
def run(name, prompt, refs):
    global cur
    while cur < len(accs):
        a, t = accs[cur]
        url = f"https://api.cloudflare.com/client/v4/accounts/{a}/ai/run/@cf/black-forest-labs/flux-2-klein-4b"
        files = {f"input_image_{i}": (p.name, p.read_bytes()) for i, p in enumerate(refs)}
        body, ct = multipart({"prompt": prompt, "width": str(job.get("size",[1344,768])[0]), "height": str(job.get("size",[1344,768])[1]), "steps": "4"}, files)
        req = urllib.request.Request(url, data=body, method="POST", headers={"Authorization": f"Bearer {t}", "Content-Type": ct})
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                img = (json.loads(r.read().decode()).get("result") or {}).get("image")
            if img:
                (out/f"{name}.jpg").write_bytes(base64.b64decode(img)); log.append(f"{name}: OK ({len(refs)} ảnh mẫu, tk {cur+1})"); return
            log.append(f"{name}: không có ảnh"); return
        except urllib.error.HTTPError as e:
            m = e.read().decode("utf-8", "replace")
            if "neurons" in m or "4006" in m:
                log.append(f"tk {cur+1} hết lượt"); cur += 1; continue
            log.append(f"{name}: HTTP {e.code} {m[:300]}"); return
        except Exception as e:
            log.append(f"{name}: {e}"); return
    log.append(f"{name}: hết tài khoản")
for k in job["keys"]:
    it = items[k]
    names = job.get("ref_names", {}).get(k, it.get("refs", []))
    refs = [RD/f"{n}.jpg" for n in names if (RD/f"{n}.jpg").exists()][:3] if use_refs else []
    for v in vars_:
        if (out/f"{k}_{v}.jpg").exists(): continue
        run(f"{k}_{v}", it["prompt"], refs)
(out/"nhat_ky.txt").write_text("\n".join(log), encoding="utf-8"); print("\n".join(log))
