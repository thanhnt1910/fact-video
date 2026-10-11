"""
TÌM ẢNH TƯ LIỆU (không bản quyền) cho video dài, theo danh sách "ô ảnh" viết tay.

  python tim_anh.py ke-hoach/anh/ST1.json

File ô ảnh:
  {"id": "ST1", "slots": [
     {"slot": "S1", "beats": "1-3", "mo_ta": "Onoda bước ra khỏi rừng 1974",
      "queries": ["Hiroo Onoda", "Lubang jungle"], "subject": ""}
  ]}
Kết quả: logs/anh_tim/<mã>_<slot>.jpg (lưới ảnh đánh số) + logs/anh_tim/<mã>.json (đường dẫn, giấy phép, kích thước)
để chọn ảnh cho từng đoạn. Chỉ nhận ảnh hết bản quyền / CC0 / CC BY (images.py lọc sẵn).
"""
import json
import sys
import time
from pathlib import Path

import images

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "logs" / "anh_tim"
SOURCES = ["wikimedia", "openverse"]


def main():
    spec = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    sid = spec["id"]
    OUT.mkdir(parents=True, exist_ok=True)
    allres = []
    for s in spec["slots"]:
        cands, seen = [], set()
        for q in s.get("queries", []):
            for src in s.get("sources", SOURCES):
                try:
                    found = images.SOURCES[src](q)
                except Exception as e:
                    print(f"  ⚠️  {s['slot']} {src} \"{q}\": {e}")
                    found = []
                subj = s.get("subject", "")
                for c in found:
                    if c["url"] in seen or (subj and not images._relevant(c, subj)):
                        continue
                    seen.add(c["url"])
                    cands.append(dict(c, source=src, query=q))
                time.sleep(0.3)
        cands = cands[:16]
        print(f"{s['slot']} ({s.get('mo_ta', '')}): {len(cands)} ứng viên", flush=True)
        entry = {"scene": 0, "query": f"{s['slot']} · {s.get('mo_ta', '')}"[:90], "candidates": cands}
        # lưới 8 ảnh/hàng: tách thành 2 hàng nếu nhiều
        rows = [dict(entry, scene=k, candidates=cands[k * 8:(k + 1) * 8]) for k in range((len(cands) + 7) // 8)] or [entry]
        for k, r in enumerate(rows):
            r["query"] = entry["query"] + (f" (hàng {k + 1}: số trên ảnh + {k * 8})" if len(rows) > 1 else "")
        images.make_contact_sheet(rows, ROOT / "output" / "_tim" / sid / s["slot"], OUT / f"{sid}_{s['slot']}.jpg",
                                  OUT / f"{sid}_{s['slot']}_tmp.json")
        (OUT / f"{sid}_{s['slot']}_tmp.json").unlink(missing_ok=True)
        allres.append({"slot": s["slot"], "beats": s.get("beats"), "mo_ta": s.get("mo_ta"),
                       "candidates": [{"so": i, "url": c["url"], "w": c.get("w"), "h": c.get("h"),
                                       "credit": c["credit"], "text": c.get("text", "")[:200]}
                                      for i, c in enumerate(cands)]})
    (OUT / f"{sid}.json").write_text(json.dumps(allres, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
