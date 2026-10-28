"""Tìm ảnh trên Wikimedia Commons, CHỈ giữ ảnh phạm vi công cộng / CC0 / CC BY (không SA, NC, ND).
python tim_anh_commons.py <tên> : đọc ke-hoach/ten-duong/<tên>_anh_truy_van.txt (mỗi dòng một truy vấn),
tải bản 1280 px vào assets/ten_duong/<tên>/raw/, ghi ke-hoach/ten-duong/<tên>_anh_ung_vien.json (nguồn, tác giả, giấy phép)."""
import json, os, re, sys, time, urllib.parse, urllib.request, html
ten = sys.argv[1]; R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
UA = {'User-Agent': 'NguoiGacSuBot/1.0 (https://github.com/thanhnt1910/fact-video; contact via repo) python-urllib'}
API = 'https://commons.wikimedia.org/w/api.php'
def get(url, tries=4):
    for i in range(tries):
        try: return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()
        except Exception as e: print('  lỗi', str(e)[:80], flush=True); time.sleep(3 + 4 * i)
    return None
def tag(s): return html.unescape(re.sub(r'<[^>]+>', '', s or '')).strip()
def ok_license(lic):
    l = (lic or '').lower().strip()
    if l.startswith(('cc0', 'public domain', 'pd-', 'pd ')) or l == 'pd': return True
    t = re.split(r'[\s\-]+', l)
    return t[:2] == ['cc', 'by'] and not any(x in t for x in ('sa', 'nc', 'nd'))
qs = [l.strip() for l in open(f'{R}/ke-hoach/ten-duong/{ten}_anh_truy_van.txt', encoding='utf-8') if l.strip() and not l.startswith('#')]
out = {}; rej = {}
for q in qs:
    p = {'action': 'query', 'format': 'json', 'generator': 'search', 'gsrsearch': q, 'gsrnamespace': 6, 'gsrlimit': 25, 'prop': 'imageinfo',
         'iiprop': 'url|size|mime|extmetadata', 'iiurlwidth': 1280}
    d = get(API + '?' + urllib.parse.urlencode(p)); print('truy vấn', q, flush=True)
    if not d: continue
    for pg in (json.loads(d).get('query', {}).get('pages', {}) or {}).values():
        ii = (pg.get('imageinfo') or [{}])[0]; em = ii.get('extmetadata', {}); title = pg['title']
        if ii.get('mime') not in ('image/jpeg', 'image/png') or ii.get('width', 0) < 700: continue
        lic = tag(em.get('LicenseShortName', {}).get('value'))
        if not ok_license(lic): rej[title] = lic; continue
        out[title] = dict(query=q, title=title, page='https://commons.wikimedia.org/wiki/' + urllib.parse.quote(title.replace(' ', '_')), license=lic,
                          artist=tag(em.get('Artist', {}).get('value')), credit=tag(em.get('Credit', {}).get('value')), desc=tag(em.get('ImageDescription', {}).get('value'))[:200],
                          w=ii.get('width'), h=ii.get('height'), thumb=ii.get('thumburl') or ii.get('url'), attribution_required=tag(em.get('AttributionRequired', {}).get('value')))
    time.sleep(1)
os.makedirs(f'{R}/assets/ten_duong/{ten}/raw', exist_ok=True); n = 0
for i, (t, m) in enumerate(sorted(out.items())):
    fn = f'{i:03d}.jpg'; b = get(m['thumb'])
    if b: open(f'{R}/assets/ten_duong/{ten}/raw/{fn}', 'wb').write(b); m['file'] = fn; n += 1
json.dump(out, open(f'{R}/ke-hoach/ten-duong/{ten}_anh_ung_vien.json', 'w'), ensure_ascii=False, indent=1)
print(f'giữ {len(out)} ảnh đạt giấy phép (đã tải {n}); loại {len(rej)} ảnh vì giấy phép')
for t, l in list(rej.items())[:15]: print('  loại', t, '|', l)
