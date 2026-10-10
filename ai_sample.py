"""Vẽ thử vài ảnh theo các phong cách để duyệt trước (logs/ai_sample.jpg)."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import ai_images

ROOT = Path(__file__).resolve().parent
PROMPTS = [
    "a large flock of emus running across a golden wheat field in the Australian outback, dust rising, wide shot",
    "a former soldier clearing scrubland with an axe under the harsh sun of the Australian outback, a simple corrugated iron hut behind, 1920s",
    "soldiers hiding behind bushes near a small farm dam with a machine gun on a tripod, emus approaching the water, dawn",
    "a 1930s truck with a machine gun mounted on the back bouncing over rough outback ground chasing fast emus far ahead, dust cloud",
]
STYLES = {
    "A": ai_images.STYLE,
    "B": ("2D illustrated graphic novel style, ink linework with soft watercolor wash, warm sepia and amber tones, "
          "hand-drawn, storybook, historical setting, no text, no watermark, not photorealistic, not 3D"),
}
WIDE = "wide cinematic composition, main subject centered with space above and below"


def main():
    out = ROOT / "logs" / "_sample"
    out.mkdir(parents=True, exist_ok=True)
    tiles = []
    for sk, st in STYLES.items():
        for i, p in enumerate(PROMPTS):
            f = out / f"{sk}{i}.jpg"
            try:
                ai_images.generate(p + ", " + WIDE, f, style=st, wide=True)
                im = Image.open(f).convert("RGB")
            except Exception as e:
                print("lỗi", sk, i, e)
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
    sheet.save(ROOT / "logs" / "ai_sample.jpg", quality=88)
    print("xong")


if __name__ == "__main__":
    main()
