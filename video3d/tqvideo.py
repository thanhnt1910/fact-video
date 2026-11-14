#!/usr/bin/env python3
"""TQ VIDEO v2 (Three.js) — dựng video 3D từ file kịch bản JSON.

  python3 tqvideo.py preview spec.json [t1,t2,...]   -> spec_preview.jpg (contact sheet)
  python3 tqvideo.py frame   spec.json t             -> spec_t.jpg (một khung hình full-size)
  python3 tqvideo.py render  spec.json               -> <spec>.mp4 (video + âm thanh)

Cần: node_modules/three (npm install three) cạnh file này; Chrome; playwright, numpy, scipy, PIL; ffmpeg.
"""
import functools, http.server, json, os, socketserver, subprocess, sys, threading, time
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
CHROME = os.environ.get('CHROME', '/usr/bin/google-chrome')
GL_ARGS = ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist',
           '--enable-webgl', '--disable-gpu-sandbox']
FONTS = ['600 52px Lora', 'italic 400 26px Lora', '500 30px Lora', '700 120px "Noto Serif CJK SC"']


def serve():
    class Q(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
    h = functools.partial(Q, directory=HERE)
    socketserver.TCPServer.allow_reuse_address = True
    srv = socketserver.ThreadingTCPServer(('127.0.0.1', 0), h)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


def page_for(spec, pw):
    srv = serve(); port = srv.server_address[1]
    html = ('<!DOCTYPE html><html><head><meta charset="utf-8"><link rel="icon" href="data:,"><style>html,body{margin:0;background:#000;overflow:hidden}'
            '#stage{position:relative}#stage canvas{position:absolute;left:0;top:0}</style>'
            '<script type="importmap">{"imports":{"three":"/node_modules/three/build/three.module.js",'
            '"three/addons/":"/node_modules/three/examples/jsm/"}}</script></head>'
            '<body><div id="stage"></div><script>window.SPEC=' + json.dumps(spec, ensure_ascii=False) + ';</script>'
            '<script type="module" src="/' + spec.get('engine', 'engine3d.js') + '"></script></body></html>')
    name = f'_page_{os.getpid()}.html'
    open(os.path.join(HERE, name), 'w').write(html)
    b = pw.chromium.launch(executable_path=CHROME, args=GL_ARGS)
    p = b.new_page(viewport={'width': spec['size'][0], 'height': spec['size'][1]})
    errs = []; p.on('pageerror', lambda e: errs.append(str(e)))
    p.on('console', lambda m: m.type == 'error' and errs.append(m.text))
    p.goto(f'http://127.0.0.1:{port}/{name}')
    p.wait_for_function('window.ready || window.__err || window.__fail', timeout=120000)
    err = p.evaluate('window.__err')
    if err or errs: raise SystemExit('JS error: ' + (err or errs[0]))
    for fn in FONTS:
        p.evaluate(f"document.fonts.load('{fn}')")
    return b, p, srv, os.path.join(HERE, name)


def close(b, srv, tmp):
    b.close(); srv.shutdown(); os.path.exists(tmp) and os.unlink(tmp)


def grab(p, quality=92):
    import base64
    return base64.b64decode(p.evaluate(f'window.grab({quality / 100})').split(',', 1)[1])


def preview(path, times):
    spec = json.load(open(path)); fps = spec.get('fps', 30)
    from PIL import Image, ImageDraw
    import io
    with sync_playwright() as pw:
        b, p, srv, tmp = page_for(spec, pw)
        dur = p.evaluate('window.DUR')
        if not times:
            acc, times = 0, []
            for s in spec['shots']:
                times.append(round(acc + s['dur'] * 0.6, 2)); acc += s['dur']
        shots = []
        for t in sorted(times):
            t0 = time.time(); p.evaluate(f'window.goto({int(t * fps)})')
            shots.append((t, Image.open(io.BytesIO(grab(p, 85))))); print(f't={t} {time.time() - t0:.1f}s', flush=True)
        close(b, srv, tmp)
    cols = 3; tw, th = 640, int(640 * spec['size'][1] / spec['size'][0])
    rows = (len(shots) + cols - 1) // cols
    sheet = Image.new('RGB', (tw * cols, th * rows))
    for i, (t, im) in enumerate(shots):
        im = im.resize((tw, th)); ImageDraw.Draw(im).text((8, 8), f't={t}s', fill=(255, 255, 0))
        sheet.paste(im, ((i % cols) * tw, (i // cols) * th))
    out = os.path.splitext(path)[0] + '_preview.jpg'; sheet.save(out, quality=85)
    print(out, f'duration={dur}s')


def frame(path, t):
    spec = json.load(open(path)); fps = spec.get('fps', 30)
    with sync_playwright() as pw:
        b, p, srv, tmp = page_for(spec, pw)
        p.evaluate(f'window.goto({int(t * fps)})')
        out = os.path.splitext(path)[0] + f'_{t}.jpg'; open(out, 'wb').write(grab(p, 90))
        close(b, srv, tmp)
    print(out)


def render(path):
    spec = json.load(open(path)); fps = spec.get('fps', 30)
    base = os.path.splitext(path)[0]; vtmp = base + '.tmp_video.mp4'; wav = base + '.wav'; out = base + '.mp4'
    with sync_playwright() as pw:
        b, p, srv, tmp = page_for(spec, pw)
        nframes = int(round(p.evaluate('window.DUR') * fps))
        ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(fps), '-c:v', 'mjpeg', '-i', '-',
                               '-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', vtmp], stdin=subprocess.PIPE)
        t0 = time.time()
        for f in range(nframes):
            p.evaluate(f'window.goto({f})')
            ff.stdin.write(grab(p))
            if f % 30 == 0: print(f'frame {f}/{nframes}  {time.time() - t0:.0f}s', flush=True)
        ff.stdin.close(); assert ff.wait() == 0
        log = p.evaluate('window.LOG'); close(b, srv, tmp)
    sys.path.insert(0, HERE); from audio import make_audio
    make_audio(spec, log, nframes / fps, wav)
    tmp_out = base + '.tmp_final.mp4'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', vtmp, '-i', wav, '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                    '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', tmp_out], check=True)
    os.replace(tmp_out, out); os.unlink(vtmp); os.unlink(wav)
    print('DONE', out)


def total_frames(spec):
    return int(round(sum(s['dur'] for s in spec['shots']) * spec.get('fps', 30)))


def doan(path, i, n, out):
    """Dựng đoạn thứ i (0..n-1) của video, chỉ hình, ra out (mp4). Dùng để dựng song song nhiều máy."""
    spec = json.load(open(path)); fps = spec.get('fps', 30); N = total_frames(spec)
    a0, a1 = N * i // n, N * (i + 1) // n
    print(f'đoạn {i}/{n}: khung {a0}..{a1 - 1} / {N}', flush=True)
    with sync_playwright() as pw:
        b, p, srv, tmp = page_for(spec, pw)
        ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(fps), '-c:v', 'mjpeg', '-i', '-',
                               '-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
        t0 = time.time()
        for f in range(a0, a1):
            p.evaluate(f'window.goto({f})')
            ff.stdin.write(grab(p))
            if (f - a0) % 30 == 0: print(f'khung {f - a0}/{a1 - a0}  {time.time() - t0:.0f}s', flush=True)
        ff.stdin.close(); assert ff.wait() == 0
        close(b, srv, tmp)
    print('XONG', out, f'{time.time() - t0:.0f}s')


def write_log(path, out):
    """Chạy mô phỏng cả video (không vẽ) để lấy mốc lửa, tên, tiếng nước cho âm thanh."""
    spec = json.load(open(path))
    with sync_playwright() as pw:
        b, p, srv, tmp = page_for(spec, pw)
        log = p.evaluate('window.simAll()'); close(b, srv, tmp)
    json.dump(log, open(out, 'w'))
    print('LOG', out)


def ghep(path, out, log_path, segs):
    """Ghép các đoạn hình theo thứ tự rồi tạo âm thanh và trộn vào."""
    spec = json.load(open(path)); fps = spec.get('fps', 30)
    base = os.path.splitext(out)[0]; lst = base + '_list.txt'; vtmp = base + '.tmp_video.mp4'; wav = base + '.wav'
    open(lst, 'w').write(''.join(f"file '{os.path.abspath(s)}'\n" for s in segs))
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', vtmp], check=True)
    sys.path.insert(0, HERE); from audio import make_audio
    make_audio(spec, json.load(open(log_path)), total_frames(spec) / fps, wav)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', vtmp, '-i', wav, '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                    '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', out], check=True)
    for f in (lst, vtmp, wav): os.unlink(f)
    print('DONE', out)


if __name__ == '__main__':
    cmd, path = sys.argv[1], sys.argv[2]
    if cmd == 'doan':
        doan(path, int(sys.argv[3]), int(sys.argv[4]), sys.argv[5])
    elif cmd == 'log':
        write_log(path, sys.argv[3])
    elif cmd == 'ghep':
        ghep(path, sys.argv[3], sys.argv[4], sys.argv[5:])
    elif cmd == 'preview':
        preview(path, [float(x) for x in sys.argv[3].split(',')] if len(sys.argv) > 3 else None)
    elif cmd == 'frame':
        frame(path, float(sys.argv[3]))
    elif cmd == 'render':
        render(path)
