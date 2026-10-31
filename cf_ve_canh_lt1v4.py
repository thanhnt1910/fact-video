"""Vẽ ảnh sản xuất lt1v4 theo Scene Planner trên Cloudflare FLUX.2 klein. CHỈ vẽ cảnh mà cổng sản xuất cho phép (PLAN_APPROVED, không còn gì chặn).
  python cf_ve_canh_lt1v4.py L04,L32,L33  -> assets/anh_lt1v4/<cảnh>_a<lần>.jpg   (lần vẽ theo anh.json; tối đa 1 + 3 lần vẽ lại)
Ảnh tham chiếu: chỉ ảnh trong tham-chieu-duoc-duyet.json (face_only). Không tự ghi PASS: người soi ảnh ghi anh.json (dem_thu_cong)."""
import base64, hashlib, json, subprocess, sys, uuid, urllib.request, urllib.error
from pathlib import Path
from PIL import Image
import ai_images as ai
sys.path.insert(0, str(Path(__file__).resolve().parent / "phim_ban_do"))
import anh_quy_tac as Q
R = Path(__file__).resolve().parent
P = json.loads((R / "ke-hoach/anh/lt1v4/scene-planner.json").read_text(encoding="utf-8"))
sc = {s["scene_id"]: s for s in P["scenes"]}
A = json.loads((R / "ke-hoach/anh/lt1v4/anh.json").read_text(encoding="utf-8"))["images"]
want = sys.argv[1].split(",")
out = R / "assets/anh_lt1v4"; out.mkdir(parents=True, exist_ok=True)
rc = 0
def ve(prompt, refs, seed):
    acc, tok = ai._creds()
    fields = [("prompt", prompt[:2000]), ("width", "1344"), ("height", "768"), ("seed", str(seed))]
    b = uuid.uuid4().hex
    body = b"".join(f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode() for k, v in fields)
    for k, rid in enumerate(refs):
        im = Image.open(R / f"assets/anh_nhan_vat/lt1v4/{rid}.jpg").convert("RGB"); im.thumbnail((768, 768)); t = out / f"_ref_{rid}.jpg"; im.save(t, quality=88)
        body += f'--{b}\r\nContent-Disposition: form-data; name="input_image_{k}"; filename="{t.name}"\r\nContent-Type: image/jpeg\r\n\r\n'.encode() + t.read_bytes() + b"\r\n"
    body += f"--{b}--\r\n".encode()
    req = urllib.request.Request(f"https://api.cloudflare.com/client/v4/accounts/{acc}/ai/run/{ai.MODEL2}", data=body, method="POST", headers={"Authorization": f"Bearer {tok}", "Content-Type": f"multipart/form-data; boundary={b}"})
    with urllib.request.urlopen(req, timeout=240) as r:
        raw, ct = r.read(), r.headers.get("Content-Type", "")
    return raw if ct.startswith("image/") else base64.b64decode(json.loads(raw)["result"]["image"])
for sid in want:
    s = sc[sid]
    g = subprocess.run([sys.executable, "phim_ban_do/kiem_scene_planner.py", "lt1v4", "--cong", sid], cwd=R, capture_output=True, text=True).stdout
    if "CHO PHÉP" not in g: print("không vẽ", sid, "cổng chặn:", g.strip()[:300], flush=True); rc = 2; continue
    assert hashlib.sha256(s["image_prompt"].encode()).hexdigest() == s["prompt_sha256"], sid
    rs = sorted([r for r in A if r["scene_id"] == sid and r["status"] != "STALE"], key=lambda r: r["attempt"])
    code, why = Q.quyet_dinh_ve(A, sid)
    if code != "VE": print("không vẽ", sid, code, why, flush=True); rc = 2; continue
    att = (rs[-1]["attempt"] + 1) if rs else 1
    refs = [r["image_id"] for r in s.get("reference_images", []) if Q.tham_chieu_hop_le("lt1v4", r["image_id"])[0]]
    seed = int(hashlib.sha256(f"{sid}-{att}".encode()).hexdigest()[:6], 16)
    try:
        (out / f"{sid}_a{att}.png").write_bytes(ve(s["image_prompt"], refs, seed))
        Image.open(out / f"{sid}_a{att}.png").convert("RGB").save(out / f"{sid}_a{att}.jpg", quality=92); (out / f"{sid}_a{att}.png").unlink()
        print("ok", sid, "lần", att, "seed", seed, "ref", refs, flush=True)
    except Exception as e:
        print("lỗi", sid, str(e)[:300], flush=True)
        if "hết lượt" in str(e) or "4006" in str(e): rc = 3; break
sys.exit(rc)
