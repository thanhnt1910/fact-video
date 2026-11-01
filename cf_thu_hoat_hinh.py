"""THỬ NGHIỆM phong cách hoạt hình nét viền dày (tham khảo video mẫu LSNT) bằng FLUX.2 klein trên Cloudflare.
KHÔNG phải ảnh sản xuất, KHÔNG ghi vào anh.json của lt1v4, KHÔNG thay Master Style. Ảnh nằm ở assets/thu_phong_cach/hoat-hinh/.
  python cf_thu_hoat_hinh.py     -> C0 (nhân vật), A1-A3 (có tham chiếu C0), B1-B3 (chỉ lời mô tả)"""
import base64, hashlib, json, sys, uuid, urllib.request
from pathlib import Path
from PIL import Image
import ai_images as ai
R = Path(__file__).resolve().parent
out = R / "assets/thu_phong_cach/hoat-hinh"; out.mkdir(parents=True, exist_ok=True)
W, H = 768, 1344   # khổ dọc 9:16
STYLE = ("flat vector cartoon illustration, thick clean black outlines, bold saturated colors, simple flat shading, large expressive eyes, "
         "clear readable silhouettes, detailed background in layers, no text, no letters, no writing, no logos. "
         "Ancient Vietnam, Ly dynasty 11th century: grey tiled roofs and thatched houses, wooden buildings, cloth headwraps, no modern objects, no flags, no guns, no glass, no electric items.")
CHAR = ("Ly Thuong Kiet, an elderly Vietnamese general with a black beard lightly streaked with grey, hair in a high topknot with a plain brown cloth headwrap, "
        "long wide-sleeved dark green robe with a leather belt and plain brown leather shoulder guards")
SCENES = {
 "1": "Inside a plain timber hall with grey tiled roof, the general stands behind a low wooden table looking down at an unrolled blank paper map, a clay oil dish with a small flame on the table, medium shot.",
 "2": "On the south bank of a wide river at dusk, the general stands in front of a long fence of bamboo stakes and an earth rampart, looking across the water toward the far bank, many small wooden boats behind him, wide shot.",
 "3": "At the foot of a tall stone city wall under a grey sky, the general points at the wall while several Vietnamese soldiers in plain cloth tunics and headwraps stack earth sacks into a rising ramp, wide shot.",
}
def run(prompt, refs, seed):
    acc, tok = ai._creds()
    fields = [("prompt", prompt[:2000]), ("width", str(W)), ("height", str(H)), ("seed", str(seed))]
    b = uuid.uuid4().hex
    body = b"".join(f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode() for k, v in fields)
    for k, p in enumerate(refs):
        im = Image.open(p).convert("RGB"); im.thumbnail((768, 768)); t = out / f"_ref{k}.jpg"; im.save(t, quality=88)
        body += f'--{b}\r\nContent-Disposition: form-data; name="input_image_{k}"; filename="{t.name}"\r\nContent-Type: image/jpeg\r\n\r\n'.encode() + t.read_bytes() + b"\r\n"
    body += f"--{b}--\r\n".encode()
    req = urllib.request.Request(f"https://api.cloudflare.com/client/v4/accounts/{acc}/ai/run/{ai.MODEL2}", data=body, method="POST",
        headers={"Authorization": f"Bearer {tok}", "Content-Type": f"multipart/form-data; boundary={b}"})
    with urllib.request.urlopen(req, timeout=240) as r:
        raw, ct = r.read(), r.headers.get("Content-Type", "")
    return raw if ct.startswith("image/") else base64.b64decode(json.loads(raw)["result"]["image"])
def save(name, data):
    p = out / f"{name}.png"; p.write_bytes(data); Image.open(p).convert("RGB").save(out / f"{name}.jpg", quality=92); p.unlink(); print("ok", name, flush=True)
seed = lambda s: int(hashlib.sha256(s.encode()).hexdigest()[:6], 16)
try:
    save("C0", run(f"{STYLE} Character design, full body, front view, plain light background: {CHAR}.", [], seed("C0")))
    c0 = out / "C0.jpg"
    for k, sc in SCENES.items():
        save(f"A{k}", run(f"{STYLE} The same character as in the reference image: {CHAR}. {sc}", [c0], seed("A" + k)))
        save(f"B{k}", run(f"{STYLE} {CHAR}. {sc}", [], seed("B" + k)))
except Exception as e:
    print("lỗi", str(e)[:300]); sys.exit(3)
