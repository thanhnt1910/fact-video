#!/usr/bin/env python3
"""Từ kịch bản md tạo src/<tên>/texts.json (phụ đề bỏ dấu *) và beats.json (cho tao_phu_de.py).
Dùng: python3 scripts/chuan_bi_video.py ../ke-hoach/khoa-hoc-video-N-<slug>-kich-ban.md <tên>"""
import json, re, sys, pathlib
md, name = sys.argv[1], sys.argv[2]
t = open(md, encoding='utf-8').read()
pairs = re.findall(r'^\d+\. Đọc: (.+)\n\s+Phụ đề: (.+)$', t, re.M)
d = pathlib.Path('src') / name
d.mkdir(parents=True, exist_ok=True)
json.dump([p[1].replace('*', '') for p in pairs], open(d / 'texts.json', 'w'), ensure_ascii=False, indent=1)
json.dump({'beats': [{'say': a, 'text': b} for a, b in pairs]}, open(d / 'beats.json', 'w'), ensure_ascii=False, indent=1)
print(len(pairs), 'câu')
