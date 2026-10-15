"""Tạo câu mô tả vẽ ảnh nền cho bìa: scripts/<mã>.json -> long.bia.canh = {"rong": "...", "doc": "..."}
  python bia_anh.py TQ2  -> ke-hoach/nhan-vat/TQ2BIA_anh.json (3 phương án mỗi khổ: rộng 901-903, dọc 911-913)
Rồi chạy workflow "Vẽ ảnh 2D hàng loạt" với ma=TQ2BIA. Ảnh ra: assets/anh_2d/TQ2BIA/9xx.jpg
Bìa phải vẽ ĐÚNG nội dung tập: nhân vật chính, đạo cụ trong lời kể, bối cảnh đúng thời, KHÔNG có chữ (chữ do bia_dai.py dựng)."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STYLE = ("vivid saturated painterly digital illustration with a manga-inspired look, dramatic cinematic lighting, strong rim light, "
         "rich warm and cool colour contrast, sharp detailed faces, realistic adult proportions, authentic Eastern Han dynasty clothing and objects, "
         "epic movie-poster composition, every person has exactly two arms and two hands, no text, no letters, no numerals, no watermark, no modern objects")


def main():
    sid = sys.argv[1]
    sc = json.loads((ROOT / "scripts" / f"{sid}.json").read_text(encoding="utf-8"))
    canh = sc["long"]["bia"]["canh"]
    items = []
    for i in range(3):
        items.append({"key": str(901 + i), "w": 1344, "h": 768, "prompt": f'{canh["rong"]} {STYLE}'})
        items.append({"key": str(911 + i), "w": 768, "h": 1344, "prompt": f'{canh["doc"]} {STYLE}'})
    out = ROOT / "ke-hoach" / "nhan-vat" / f"{sid}BIA_anh.json"
    out.write_text(json.dumps(items, ensure_ascii=False, indent=1), encoding="utf-8")
    print("ok", out, len(items))


if __name__ == "__main__":
    main()
