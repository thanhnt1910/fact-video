"""Vẽ thử vài ảnh theo các phong cách để duyệt trước (logs/ai_sample.jpg)."""
import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import ai_images

ROOT = Path(__file__).resolve().parent
PROMPTS = [
    "a frightened Japanese army officer in a worn 1940s uniform reading a paper leaflet in a tropical jungle",
    "a 1920s con man in an elegant suit presenting documents to businessmen around a table in a luxurious Paris hotel room",
    "a large flock of emus running across a golden wheat field in the Australian outback, dust rising, wide shot",
    "a former soldier clearing scrubland with an axe under the harsh sun of the Australian outback, a simple corrugated iron hut behind, 1920s",
    "soldiers hiding behind bushes near a small farm dam with a machine gun on a tripod, emus approaching the water, dawn",
    "a 1930s truck with a machine gun mounted on the back bouncing over rough outback ground chasing fast emus far ahead, dust cloud",
]
STYLES = {
    # A: tranh 2D hoạt hình sinh động
    "A": ai_images.STYLE,
    # B: tranh minh họa vẽ tay kiểu sơn dầu cổ (giống phong cách cũ, vẽ bằng FLUX.2)
    "B": ("detailed historical oil painting illustration, painterly brush strokes, warm sepia and amber tones, "
          "soft lantern light, storybook, accurate period details, no text, no watermark"),
    # C: tranh kỹ thuật số điện ảnh, bán chân thực (rõ là tranh vẽ, không giả ảnh chụp)
    "C": ("cinematic digital matte painting, semi-realistic concept art, dramatic natural lighting, rich detail, "
          "historically accurate clothing and setting, painted look, no text, no watermark, not a photograph"),
}
WIDE = "wide cinematic composition, main subject centered with space above and below"


def hf_generate(prompt, out, wide=True):
    """Vẽ miễn phí qua Hugging Face Space chính thức của FLUX.1 schnell (có giới hạn lượt GPU miễn phí mỗi ngày)."""
    import shutil
    from gradio_client import Client
    w, h = (1344, 768) if wide else (1024, 1024)
    tok = os.environ.get("HF_TOKEN") or None
    try:
        c = Client("black-forest-labs/FLUX.1-schnell", token=tok) if tok else Client("black-forest-labs/FLUX.1-schnell")
    except TypeError:
        c = Client("black-forest-labs/FLUX.1-schnell", hf_token=tok)
    res = c.predict(prompt=prompt, seed=0, randomize_seed=True, width=w, height=h, num_inference_steps=4, api_name="/infer")
    path = res[0] if isinstance(res, (list, tuple)) else res
    if isinstance(path, dict):
        path = path.get("path") or path.get("url")
    shutil.copy(path, out)
    return out


def main():
    out = ROOT / "logs" / "_sample"
    out.mkdir(parents=True, exist_ok=True)
    tiles = []
    for sk, st in STYLES.items():
        for i, p in enumerate(PROMPTS):
            f = out / f"{sk}{i}.jpg"
            try:
                if os.environ.get("SAMPLE_SOURCE") == "hf":
                    hf_generate(f"{p}, {WIDE}, {st}", f)
                else:
                    ai_images.generate(p + ", " + WIDE, f, style=st, wide=True)
                im = Image.open(f).convert("RGB")
            except Exception as e:
                print("lỗi", sk, i, e)
                with open(ROOT / "logs" / "ai_sample_err.txt", "a", encoding="utf-8") as fh:
                    fh.write(f"{sk}{i}: {type(e).__name__}: {str(e)[:500]}\n")
                im = Image.new("RGB", (512, 512), (60, 0, 0))
            im.thumbnail((640, 640))
            canvas = Image.new("RGB", (640, 400), (15, 15, 15))
            canvas.paste(im.resize((640, int(640 * im.height / im.width))).crop((0, 0, 640, 400)), (0, 0))
            d = ImageDraw.Draw(canvas)
            d.rectangle([0, 0, 60, 40], fill=(0, 0, 0))
            d.text((10, 8), f"{sk}{i}", fill=(255, 220, 120), font=ImageFont.load_default(size=22))
            tiles.append(canvas)
    cols = len(PROMPTS)
    rows = len(STYLES)
    sheet = Image.new("RGB", (cols * 648, rows * 408), (0, 0, 0))
    for k, t in enumerate(tiles):
        sheet.paste(t, ((k % cols) * 648, (k // cols) * 408))
    name = "ai_sample_hf.jpg" if os.environ.get("SAMPLE_SOURCE") == "hf" else "ai_sample.jpg"
    sheet.save(ROOT / "logs" / name, quality=88)
    print("xong")


if __name__ == "__main__":
    main()
