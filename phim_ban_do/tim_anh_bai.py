"""Tìm ảnh thật cho bài Facebook trên Wikimedia Commons, CHỈ giữ ảnh phạm vi công cộng / CC0 / CC BY (không SA, NC, ND), rồi gửi Telegram.

  python tim_anh_bai.py <mã> [--khong-gui]
Đọc ke-hoach/nhan-vat-phu/<mã>_anh_truy_van.txt, mỗi dòng "mục | truy vấn" (mục = phần của bài mà ảnh sẽ minh họa).
Tải bản 1280 px vào assets/anh_that/<mã>/raw/, ghi ke-hoach/nhan-vat-phu/<mã>_anh_ung_vien.json (nguồn, tác giả, giấy phép),
gửi mỗi ảnh vào Telegram kèm mục, tác giả, giấy phép, link. Mỗi mục tối đa PER ảnh (mặc định 4)."""
import json, os, re, sys, time, urllib.parse, urllib.request, html
ma = sys.argv[1]; GUI = '--khong-gui' not in sys.argv
PER = int(os.environ.get('PER', '4'))
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
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


qs = []
for l in open(f'{R}/ke-hoach/nhan-vat-phu/{ma}_anh_truy_van.txt', encoding='utf-8'):
    l = l.strip()
    if l and not l.startswith('#') and '|' in l:
        m, q = [x.strip() for x in l.split('|', 1)]; qs.append((m, q))
cand = {}; rej = {}; seen = set()
for muc, q in qs:
    p = {'action': 'query', 'format': 'json', 'generator': 'search', 'gsrsearch': q, 'gsrnamespace': 6, 'gsrlimit': 30, 'prop': 'imageinfo',
         'iiprop': 'url|size|mime|extmetadata', 'iiurlwidth': 1280}
    d = get(API + '?' + urllib.parse.urlencode(p)); print('truy vấn', muc, '|', q, flush=True)
    if not d: continue
    pages = sorted((json.loads(d).get('query', {}).get('pages', {}) or {}).values(), key=lambda x: x.get('index', 0))
    for pg in pages:
        ii = (pg.get('imageinfo') or [{}])[0]; em = ii.get('extmetadata', {}); title = pg['title']
        if title in seen: continue
        if ii.get('mime') not in ('image/jpeg', 'image/png') or ii.get('width', 0) < 900: continue
        lic = tag(em.get('LicenseShortName', {}).get('value'))
        if not ok_license(lic): rej[title] = lic; continue
        seen.add(title)
        cand.setdefault(muc, []).append(dict(muc=muc, query=q, title=title, page='https://commons.wikimedia.org/wiki/' + urllib.parse.quote(title.replace(' ', '_')),
            license=lic, artist=tag(em.get('Artist', {}).get('value')), desc=tag(em.get('ImageDescription', {}).get('value'))[:200],
            date=tag(em.get('DateTimeOriginal', {}).get('value'))[:40], w=ii.get('width'), h=ii.get('height'), thumb=ii.get('thumburl') or ii.get('url')))
    time.sleep(1)
os.makedirs(f'{R}/assets/anh_that/{ma}/raw', exist_ok=True); out = []; k = 0
for muc in dict.fromkeys(m for m, _ in qs):
    for m in cand.get(muc, [])[:PER]:
        b = get(m['thumb']); fn = f'{k:03d}.jpg'; k += 1
        if b: open(f'{R}/assets/anh_that/{ma}/raw/{fn}', 'wb').write(b); m['file'] = fn; out.append(m)
os.makedirs(f'{R}/ke-hoach/nhan-vat-phu', exist_ok=True)
json.dump(out, open(f'{R}/ke-hoach/nhan-vat-phu/{ma}_anh_ung_vien.json', 'w'), ensure_ascii=False, indent=1)
tom = {muc: len([m for m in out if m['muc'] == muc]) for muc in dict.fromkeys(m for m, _ in qs)}
print(f'giữ {len(out)} ảnh đạt giấy phép; loại {len(rej)} ảnh vì giấy phép (SA/NC/ND/không rõ). Theo mục: {tom}')
for t, l in list(rej.items())[:15]: print('  loại', t, '|', l)
if GUI:
    import requests
    tok = os.environ['TG_TOKEN']; chat = os.environ.get('TG_CHAT') or open(f'{R}/telegram_chat_id.txt').read().strip()
    u = f'https://api.telegram.org/bot{tok}/'
    txt = f'Ảnh ứng viên cho bài {ma}: {len(out)} ảnh (chỉ public domain, CC0, CC BY). Theo mục: ' + '; '.join(f'{a}: {b}' for a, b in tom.items()) + \
          '\nThiếu ảnh ở mục nào thì mục đó được ghi 0.'
    r = requests.post(u + 'sendMessage', data={'chat_id': chat, 'text': txt}); print('tin tổng hợp', r.status_code)
    fail = 0
    for i, m in enumerate(out, 1):
        cap = f"[{m['muc']}] {i}/{len(out)}\n{m['title']}\nTác giả: {m['artist'][:150] or 'không rõ'}\nGiấy phép: {m['license']}\n{m['page']}"[:1000]
        fp = f"{R}/assets/anh_that/{ma}/raw/{m['file']}"
        with open(fp, 'rb') as f:
            r = requests.post(u + 'sendPhoto', data={'chat_id': chat, 'caption': cap}, files={'photo': f}, timeout=120)
        if r.status_code != 200:
            with open(fp, 'rb') as f:
                r = requests.post(u + 'sendDocument', data={'chat_id': chat, 'caption': cap}, files={'document': f}, timeout=120)
        print(i, m['file'], r.status_code, flush=True); fail += r.status_code != 200; time.sleep(1.2)
    print('gửi xong, lỗi', fail)
