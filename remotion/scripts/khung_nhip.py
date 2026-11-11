#!/usr/bin/env python3
"""In số khung hình (giữa mỗi nhịp, +offset giây) để chụp: python3 scripts/khung_nhip.py <tên> [giây]"""
import json, sys
n = sys.argv[1]; off = float(sys.argv[2]) if len(sys.argv) > 2 else 1.6
d = json.load(open('src/%s/leda_dur.json' % n))
f = 0; out = []
for x in d:
    dur = round(max(x + .5, 2.4) * 30)
    out.append(f + min(int(off * 30), dur - 5)); f += dur
print(' '.join(map(str, out)))
