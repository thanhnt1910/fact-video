"""Vẽ lt1t2 trên Cloudflare FLUX.2 klein, có ảnh tham chiếu 19901 (Đại Việt) và 19903 (Việt/Tống) nếu API nhận.
  python cf_ve_lt1t2.py 19902,19903 [ref]  -> assets/anh_chibi/lt1t2_cf/<n>.jpg"""
import base64, json, sys, uuid, urllib.request, urllib.error
from pathlib import Path
from PIL import Image
import ai_images as ai
R = Path(__file__).resolve().parent
items = {i["n"]: i for i in json.loads((R / "ke-hoach/chibi/lt1t2_chibi.json").read_text(encoding="utf-8"))}
want = sorted(items) if sys.argv[1] == "all" else [int(x) for x in sys.argv[1].split(",")]
use_ref = len(sys.argv) > 2 and sys.argv[2] == "ref"
REFS = {19901: [], 19902: [], 19903: [], 19904: [], 19905: [19901], 19906: [19901]}
# Quy chuẩn 01/11/2026: chỉ ảnh có trong tham-chieu-duoc-duyet.json (chủ kênh duyệt) mới được dùng làm tham chiếu.
_ap = R / "ke-hoach/anh/lt1v4/tham-chieu-duoc-duyet.json"
APPROVED = {x["image_id"] for x in json.loads(_ap.read_text(encoding="utf-8")).get("anh", [])} if _ap.exists() else set()
out = R / "assets/anh_chibi/lt1t2_cf"; out.mkdir(parents=True, exist_ok=True)
def run(prompt, refs, seed):
    acc, tok = ai._creds()
    fields = [("prompt", prompt[:2000]), ("width", "1344"), ("height", "768"), ("seed", str(seed))]
    files = []
    for k, n in enumerate(refs):
        p = R / f"assets/anh_chibi/lt1t_cf/{n}.jpg"
        im = Image.open(p).convert("RGB"); im.thumbnail((768, 768)); t = out / f"_ref{n}.jpg"; im.save(t, quality=88)
        files.append((f"input_image_{k}", t.name, t.read_bytes()))
    b = uuid.uuid4().hex
    body = b"".join(f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode() for k, v in fields)
    for k, fn, d in files:
        body += f'--{b}\r\nContent-Disposition: form-data; name="{k}"; filename="{fn}"\r\nContent-Type: image/jpeg\r\n\r\n'.encode() + d + b"\r\n"
    body += f"--{b}--\r\n".encode()
    url = f"https://api.cloudflare.com/client/v4/accounts/{acc}/ai/run/{ai.MODEL2}"
    req = urllib.request.Request(url, data=body, method="POST", headers={"Authorization": f"Bearer {tok}", "Content-Type": f"multipart/form-data; boundary={b}"})
    with urllib.request.urlopen(req, timeout=240) as r:
        raw, ct = r.read(), r.headers.get("Content-Type", "")
    return raw if ct.startswith("image/") else base64.b64decode(json.loads(raw)["result"]["image"])
for n in want:
    refs = [r for r in (REFS[n] if use_ref else []) if r in APPROVED]
    if use_ref and REFS[n] and len(refs) != len(REFS[n]):
        print(f"bỏ ảnh tham chiếu chưa được chủ kênh duyệt theo quy chuẩn hiện hành: {[r for r in REFS[n] if r not in APPROVED]}", flush=True)
    try:
        (out / f"{n}.png").write_bytes(run(items[n]["prompt"], refs, n))
        Image.open(out / f"{n}.png").convert("RGB").save(out / f"{n}.jpg", quality=92); (out / f"{n}.png").unlink()
        print("ok", n, "ref" if refs else "khong-ref", flush=True)
    except urllib.error.HTTPError as e:
        print("lỗi", n, e.code, e.read().decode("utf-8", "replace")[:300], flush=True)
    except Exception as e:
        print("lỗi", n, str(e)[:300], flush=True)
