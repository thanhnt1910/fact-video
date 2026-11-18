#!/usr/bin/env python3
"""Quét đường dẫn trong các file quy tắc: báo đường dẫn không tồn tại.
Dùng: python tools/kiem_lien_ket.py [file ...]   (mặc định: CLAUDE.md, quy-tac/, mau-kich-ban/, PROMPT_KICH_BAN.md, review_checklist.md)
Chỉ xét chuỗi trong dấu `...` trông như đường dẫn tệp (có / hoặc đuôi .md/.py/.json/.yml/.txt/.html/.js/.mp4/.jpg/.png).
Bỏ qua chuỗi có <, >, *, {, } (mẫu), URL, và đường dẫn trong archive/ (lưu trữ chỉ để tra)."""
import re, sys, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
args = sys.argv[1:]
files = [root/a for a in args] if args else (
    [root/'CLAUDE.md', root/'PROMPT_KICH_BAN.md', root/'review_checklist.md']
    + sorted((root/'quy-tac').rglob('*.md')) + sorted((root/'mau-kich-ban').rglob('*.md')))
ext = ('.md','.py','.json','.yml','.yaml','.txt','.html','.js','.mp4','.jpg','.png','.sh','.mp3','.wav')
bad = 0
for f in files:
    if not f.exists(): continue
    for n, line in enumerate(f.read_text(encoding='utf-8').splitlines(), 1):
        for m in re.finditer(r'`([^`\n]+)`', line):
            t = m.group(1).strip().split(' ')[0].rstrip('.,;:)')
            if any(c in t for c in '<>*{}$|') or t.startswith(('http','~','/','-','.')): continue
            if '/' not in t and not t.endswith(ext): continue
            if not (t.endswith(ext) or t.endswith('/')): continue
            if '/' not in t and not (root/t).exists() and not list(root.rglob(t)): pass
            if t.startswith(('out/','leda/')) or t=='style_thu.txt' or re.search(r'[a-z]N[a-z._]',t): continue  # tạm hoặc mẫu có N   # sản phẩm tạm, không nằm trong repo
            bases = [root, root/'phim_ban_do', root/'phim_ban_do'/'doc9x16', root/'ke-hoach'/'thu-giong-hai']
            if any((b/t).exists() for b in bases) or (('/' not in t) and list(root.rglob(t))): continue
            bad += 1
            print(f"{f.relative_to(root)}:{n}: thiếu {t}")
print(f"\n{'ĐẠT: không có đường dẫn hỏng' if not bad else f'CÓ {bad} đường dẫn hỏng'}")
sys.exit(1 if bad else 0)
