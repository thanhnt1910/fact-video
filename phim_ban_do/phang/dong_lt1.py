"""Chuyển động cho ảnh phẳng lt1 (mức chi tiết cao): mỗi cảnh một clip 6 giây, 24 khung/giây.
  python phim_ban_do/phang/dong_lt1.py [số cảnh ...] [--shard i/n]  -> assets/clips_phang/lt1/N.mp4
Mọi cảnh: máy quay (đẩy, lùi, lia, đổi theo cảnh), núi mây trôi lệch tốc độ, cờ phấp phới, nước chảy, khói, lửa, đuốc, đèn dầu chập chờn,
người thở nhẹ và chớp mắt. Cảnh có thuyền: thuyền bập bềnh, sóng vòng. Cảnh chèo (19071): mái chèo chèo thật, nước chảy.
Cảnh quân hành quân nhìn từ sau (19066): chân bước luân phiên, bụi dưới chân."""
import sys, pathlib, subprocess, shutil, tempfile
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import chitiet, dong, dongthat
import flat; flat.LIMBS = True   # tay, chân rõ
from playwright.sync_api import sync_playwright

canh = chitiet.canh
ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / 'assets' / 'clips_phang' / 'lt1'
FPS, DUR = 24, 6.0
# (điểm gốc phóng, lia ngang px, lia dọc px, phóng cuối): đổi theo cảnh cho đỡ đơn điệu
PRE = [('960px 640px', -22, -6, 1.07), ('1300px 700px', 26, -8, 1.08), ('700px 760px', -30, 0, 1.06),
       ('960px 900px', 0, -14, 1.09), ('960px 540px', 18, 10, 1.05), ('560px 700px', 34, -4, 1.08)]

EXTRA = """
  // khói: cuộn lên, loãng dần; đám khói trôi sang một bên
  Q('.smoke').forEach((e,i)=>{ tb(e,'center bottom'); add(e,[{transform:'translate(0,0) scale(1)',opacity:1},{transform:'translate('+(10+i*3)+'px,-22px) scale(1.04,1.06)',opacity:.78},{transform:'translate(-6px,-40px) scale(1.08,1.1)',opacity:.9},{transform:'translate(0,0) scale(1)',opacity:1}], 5+rnd()*2, rnd()*5); });
  // lửa, đuốc, đèn dầu, lửa trại
  Q('[id^=torch],[id^=fire],[id^=camp],[id^=flame],[id^=lamp]').forEach((e,i)=>{ tb(e,'center bottom');
      add(e,[{opacity:.88,transform:'scale(1)'},{opacity:1,transform:'scale(1.04,1.1)'},{opacity:.8,transform:'scale(.97,.94)'},{opacity:1,transform:'scale(1.02,1.06)'},{opacity:.88,transform:'scale(1)'}], .9+rnd()*.5, rnd()); });
  // người đứng: chuyển trọng tâm rất nhẹ, mỗi người một nhịp (không nhún lên xuống)
  Q('#troops, #carriers, #column').forEach((g)=>{ tb(g,'center bottom'); add(g,[{transform:'rotate(-.15deg)'},{transform:'rotate(.2deg)'},{transform:'rotate(-.15deg)'}], 4.4, 0); });
  // thuyền nhỏ ở xa
  Q('#boats').forEach(e=>{ e.style.transformBox='fill-box'; add(e,[{translate:'0 -3px'},{translate:'4px 3px'},{translate:'0 -3px'}], 3.6, 0); });
  // hạt bụi bay
  Q('#ribbons').forEach(e=>add(e,[{transform:'translateX(-30px)'},{transform:'translateX(30px)'}], 8, 0));
  Q('.far').forEach(e=>add(e,[{transform:'translateX(0)'},{transform:'translateX(-60px)'}], 16, 0,'linear'));
  window.__seek ="""


def page_js():
    return dong.JS.replace('window.__seek =', EXTRA, 1)


def shots(pg, n, d):
    for i in range(int(FPS * DUR)):
        pg.evaluate('t=>window.__seek(t)', i / FPS)
        pg.screenshot(path=str(d / f'{i:04d}.jpg'), type='jpeg', quality=90)


def render_one(pg, n, tmp):
    d = tmp / str(n); d.mkdir(parents=True, exist_ok=True)
    p = tmp / f'{n}.svg'
    if n == 19071:                       # chèo thuyền thật
        p.write_text(dongthat.rowing_scene(), encoding='utf-8'); js = dongthat.JS
        cfg = dict(mode='row', T=dongthat.T_ROW, dur=DUR, zo='960px 800px', pan=-30, panY=-10, mt=40)
    elif n == 19066:                     # quân bước
        p.write_text(dongthat.march_scene(), encoding='utf-8'); js = dongthat.JS
        cfg = dict(mode='march', step=.42, dur=DUR, zo='960px 900px', pan=0, panY=40, mt=20)
    else:
        p.write_text((chitiet.SCN.get(n) or canh.SC[n])(), encoding='utf-8'); js = page_js()
        zo, pan, pany, zm = PRE[n % len(PRE)]
        cfg = dict(dur=DUR, zo=zo, pan=pan, fig=1.0, boat=['#boat', '#boatf'], rings=None)
    pg.goto(p.as_uri()); pg.evaluate(js, cfg)
    shots(pg, n, d)
    OUT.mkdir(parents=True, exist_ok=True)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', str(d / '%04d.jpg'),
                    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '23', '-preset', 'veryfast', str(OUT / f'{n}.mp4')], check=True)
    shutil.rmtree(d, ignore_errors=True)


def main():
    a = sys.argv[1:]
    shard = None
    if '--shard' in a:
        i = a.index('--shard'); k, m = map(int, a[i + 1].split('/')); shard = (k, m); del a[i:i + 2]
    ns = [int(x) for x in a] or sorted(set(canh.SC) | set(chitiet.SCN))
    if shard:
        ns = [n for j, n in enumerate(ns) if j % shard[1] == shard[0]]
    tmp = pathlib.Path(tempfile.mkdtemp())
    with sync_playwright() as p:
        br = p.chromium.launch(); pg = br.new_page(viewport={'width': 1920, 'height': 1080})
        for n in ns:
            try:
                render_one(pg, n, tmp); print('xong', n, flush=True)
            except Exception as e:
                print('LỖI', n, repr(e)[:200], flush=True)
        br.close()


if __name__ == '__main__':
    main()
