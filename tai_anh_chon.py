"""Tải các ảnh đã chọn (ảnh tư liệu miền công cộng/CC) về thư mục. Dùng: python tai_anh_chon.py assets/dola1/nguon.json"""
import json, sys, time, urllib.request
from pathlib import Path
p = Path(sys.argv[1]); d = p.parent
for k, v in json.loads(p.read_text(encoding="utf-8")).items():
    out = d / f"{k}.jpg"
    if out.exists() and out.stat().st_size > 5000:
        continue
    for t in range(3):
        try:
            req = urllib.request.Request(v["url"], headers={"User-Agent": "NguoiGacSu/1.0 (https://github.com/thanhnt1910/fact-video)"})
            out.write_bytes(urllib.request.urlopen(req, timeout=60).read()); print("ok", k, out.stat().st_size); break
        except Exception as e:
            print("lỗi", k, t, e); time.sleep(4 * (t + 1))
