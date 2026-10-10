"""Thử vẽ 2 tranh trên Kaggle (logs/kaggle_test.jpg + logs/kaggle_last.txt)."""
from pathlib import Path
from PIL import Image
import ai_images, kaggle_draw
ROOT = Path(__file__).resolve().parent
W = "wide cinematic composition, main subject centered with space above and below"
jobs = [
    ("t1", f"a frightened Japanese army officer in a worn 1940s uniform reading a paper leaflet in a tropical jungle, {W}, {ai_images.STYLE}", 1344, 768),
    ("t2", "a flock of emus running across a golden wheat field in the Australian outback, dust rising, the emus are tall flightless "
           f"Australian birds with shaggy grey-brown feathers, long thin necks and small dark heads, not turkeys, {W}, {ai_images.STYLE}", 1344, 768),
    ("t3", "an old 1930s army truck with a mounted machine gun driving on a dusty outback road, two Australian soldiers of 1932 in khaki "
           f"uniforms and slouch hats, {W}, {ai_images.STYLE}", 1344, 768),
    ("t4", f"a ghost sailing ship drifting alone on a grey Atlantic ocean, torn sails, no crew on deck, misty morning, {W}, {ai_images.STYLE}", 1344, 768),
]
res = kaggle_draw.draw_batch(jobs, ROOT / "output" / "_kt")
ims = [Image.open(res[k]) for k, *_ in jobs if k in res]
if ims:
    sheet = Image.new("RGB", (672 * 2, 384 * ((len(ims) + 1) // 2)))
    for i, im in enumerate(ims):
        sheet.paste(im.resize((672, 384)), ((i % 2) * 672, (i // 2) * 384))
    sheet.save(ROOT / "logs" / "kaggle_test.jpg", quality=88)
print("kết quả:", list(res))
