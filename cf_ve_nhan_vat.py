"""Vẽ ỨNG VIÊN Character Reference (Lý Thường Kiệt, Tông Đản) bằng FLUX.2 klein trên Cloudflare, KHÔNG ảnh tham chiếu.
  python cf_ve_nhan_vat.py CR-LTK-1,CR-LTK-2 -> assets/anh_nhan_vat/lt1v4/<id>.jpg  (chỉ ứng viên, chưa được duyệt)
Chạy lại bộ kiểm trước khi vẽ; thoát mã 3 nếu hết lượt Cloudflare."""
import hashlib, json, subprocess, sys
from pathlib import Path
from PIL import Image
import ai_images as ai
R = Path(__file__).resolve().parent
P = json.loads((R / "ke-hoach/anh/lt1v4/character-reference.json").read_text(encoding="utf-8"))
sc = {s["scene_id"]: s for s in P["scenes"]}
want = sorted(sc) if sys.argv[1] == "all" else sys.argv[1].split(",")
chk = subprocess.run([sys.executable, "phim_ban_do/kiem_scene_planner.py", "lt1v4", "--file", "ke-hoach/anh/lt1v4/character-reference.json", "--anh", "/nonexist"], cwd=R, capture_output=True, text=True)
if chk.returncode: print(chk.stdout[-1500:]); sys.exit("Bộ kiểm báo lỗi: không vẽ")
out = R / "assets/anh_nhan_vat/lt1v4"; out.mkdir(parents=True, exist_ok=True)
rc = 0
for cid in want:
    s = sc[cid]
    assert hashlib.sha256(s["image_prompt"].encode()).hexdigest() == s["prompt_sha256"]
    try:
        ai._klein(s["image_prompt"], out / f"{cid}.png", True, seed=s["seed"])
        Image.open(out / f"{cid}.png").convert("RGB").save(out / f"{cid}.jpg", quality=92); (out / f"{cid}.png").unlink()
        print("ok", cid, flush=True)
    except Exception as e:
        print("lỗi", cid, str(e)[:300], flush=True)
        if "hết lượt" in str(e): rc = 3; break
sys.exit(rc)
