#!/usr/bin/env python3
"""Ghi src/<tên>/leda_dur.json = thời lượng từng file ../demo/<tên>/leda/NN.wav (giây, 2 chữ số)."""
import json, sys, wave, glob
name = sys.argv[1]
fs = sorted(glob.glob('../demo/%s/leda/*.wav' % name))
out = []
for f in fs:
    with wave.open(f) as w: out.append(round(w.getnframes() / w.getframerate(), 2))
json.dump(out, open('src/%s/leda_dur.json' % name, 'w'))
print(len(out), 'câu', round(sum(out)), 'giây giọng')
