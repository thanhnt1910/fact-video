"""Tạo TQ1_anh.json (prompt đầy đủ từng ảnh) từ TQ1.json + TQ.json."""
import json
import re
from pathlib import Path
R = Path(__file__).resolve().parent
tq = json.loads((R / "TQ.json").read_text(encoding="utf-8"))
t1 = json.loads((R / "TQ1.json").read_text(encoding="utf-8"))
nv = {**tq["nhan_vat"], **t1["nhan_vat_phu"]}
SUF = ("medium shot, simple natural poses, every person has exactly two arms, two hands and two legs with natural adult proportions, "
       "serious weathered faces, no extra limbs, no duplicated people, no deformed faces, no text, no letters, no watermark. "
       "Flags and banners are plain solid colour with no symbols. All objects are realistic with no faces")
out = []
for c in t1["canh"]:
    n = c["so_nguoi"]
    cnt = "No people in the picture." if n == 0 else f"The picture contains exactly {n} {'person' if n == 1 else 'people'} in the foreground and no one else."
    chars = ""
    if c["nv"]:
        chars = " Characters (keep exactly this look): " + "; ".join(nv[k] for k in c["nv"]) + "."
    if n == 0:
        scene = re.sub(r",?\s*(no people|no figures|the scene is completely empty of people[^.]*)", "", c["mo_ta"])
        scene = re.sub(r"\bno people\b,?", "", scene)
        out.append({"key": c["key"], "nv": [], "prompt": scene + ". An empty quiet landscape, a still life of objects only. 2D franco-belgian ligne claire comic illustration of ancient China, clean uniform dark ink outlines, flat muted colours with soft shading, earthy palette of ochre, jade green, indigo and warm cream, no text, no numerals, no letters, no watermark, not 3D, not a photo"})
        continue
    out.append({"key": c["key"], "nv": c["nv"], "prompt": f'{c["mo_ta"]}. {cnt}{chars} {tq["phong_cach"]}. {SUF}'})
(R / "TQ1_anh.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(out))
