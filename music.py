"""
Nhạc nền không bản quyền cho video.

- Danh sách bài: assets/music/library.json (chỉ bản thu Public Domain / CC0 trên Wikimedia Commons; nhạc CC BY đã tắt).
- Tự chọn bài theo chủ đề (topic_moods); kịch bản có thể chỉ định: "music": "Teller of the Tales"
  hoặc "music": "none" để tắt nhạc.
- Bài được tải về assets/music/cache/ ở lần dùng đầu.

  python music.py --probe      # tải thử toàn bộ thư viện, tạo đoạn nghe thử demo/nhac-*.mp3
"""
import hashlib
import json
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LIB = ROOT / "assets" / "music" / "library.json"
CACHE = ROOT / "assets" / "music" / "cache"
UA = "Mozilla/5.0 (NguoiGacSuVideo/1.0; +https://github.com/thanhnt1910/fact-video)"


def load():
    return json.loads(LIB.read_text(encoding="utf-8"))


def _slug(name):
    return "".join(c if c.isalnum() else "-" for c in name.lower()).strip("-")


def fetch(track, log=print):
    CACHE.mkdir(parents=True, exist_ok=True)
    dest = CACHE / f"{_slug(track['name'])}.mp3"
    if dest.exists() and dest.stat().st_size > 50000:
        return dest
    data = b""
    try:
        req = urllib.request.Request(track["url"], headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=60) as r:
            data = r.read()
    except Exception as e:
        if not track.get("url_goc"):
            raise
        log(f"     (bản mp3 chuyển mã chưa có: {e}; tải file gốc)")
    is_mp3 = data[:3] == b"ID3" or (len(data) > 1 and data[0] == 0xFF and data[1] & 0xE0 == 0xE0)
    if (len(data) < 50000 or not is_mp3) and track.get("url_goc"):
        # file gốc ogg/flac trên Commons -> đổi sang mp3 bằng ffmpeg
        req = urllib.request.Request(track["url_goc"], headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=120) as r:
            raw = r.read()
        src = CACHE / (_slug(track["name"]) + "_goc" + Path(track["url_goc"]).suffix)
        src.write_bytes(raw)
        import make_video as mv
        mv.run_ffmpeg(["-i", str(src), "-ac", "2", "-ar", "44100", "-b:a", "192k", str(dest)])
        return dest
    if len(data) < 50000 or not is_mp3:
        raise ValueError(f"không phải file nhạc ({len(data)} byte)")
    dest.write_bytes(data)
    return dest


def candidates(script, lib=None):
    lib = lib or load()
    tracks = [t for t in lib["tracks"] if not t.get("disabled")]
    want = script.get("music")
    if want:
        hit = [t for t in tracks if t["name"].lower() == str(want).lower()]
        if hit:
            return hit
        # bài ghi trong kịch bản đã bị tắt (vd nhạc CC BY cũ): chọn bài PD/CC0 theo chủ đề
    moods = lib["topic_moods"].get(script.get("topic", ""), lib["topic_moods"]["default"])
    pool = [t for t in tracks if set(t["moods"]) & set(moods)] or tracks
    # mỗi video một bài khác nhau nhưng cố định theo mã kịch bản
    h = int(hashlib.sha1(script.get("id", "").encode()).hexdigest(), 16)
    k = h % len(pool)
    return pool[k:] + pool[:k]


def pick(script, log=print):
    """Trả về (đường_dẫn_mp3, dòng_ghi_nguồn) hoặc (None, None)."""
    if str(script.get("music", "")).lower() in ("none", "off", "khong"):
        return None, None
    for t in candidates(script):
        try:
            p = fetch(t, log)
            log(f"  🎵 Nhạc nền: {t['name']}")
            return p, t.get("credit")
        except Exception as e:
            log(f"     ⚠️  không tải được nhạc \"{t['name']}\": {e}")
    return None, None


def probe():
    """Tải thử toàn bộ thư viện; tạo đoạn nghe thử 25 giây cho mỗi bài."""
    lib = load()
    out = ROOT / "demo"
    out.mkdir(exist_ok=True)
    ok, rows = [], []
    for t in lib["tracks"]:
        try:
            p = fetch(t)
            dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                        str(p)], capture_output=True, text=True).stdout.strip() or 0)
            start = 8 if dur > 60 else 0
            clip = out / f"nhac-{_slug(t['name'])}.mp3"
            subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-ss", str(start), "-t", "25", "-i", str(p),
                            "-af", "afade=t=in:d=1,afade=t=out:st=23:d=2,loudnorm=I=-16",
                            "-metadata", f"title=[{', '.join(t['moods'])}] {t['name']}",
                            "-metadata", "artist=Kevin MacLeod", "-b:a", "128k", str(clip)], check=True)
            ok.append(f"{'/'.join(t['moods'])}|{t['name']}|{clip.name}|{dur:.0f}")
            rows.append(f"OK   {t['name']:<24} {dur:5.0f}s  {','.join(t['moods'])}")
        except Exception as e:
            rows.append(f"LỖI  {t['name']:<24} {e}")
    (out / "music-list.txt").write_text("".join(x + "\n" for x in ok), encoding="utf-8")
    (ROOT / "logs").mkdir(exist_ok=True)
    (ROOT / "logs" / "music-probe.txt").write_text("\n".join(rows) + "\n", encoding="utf-8")
    print("\n".join(rows))


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    if "--probe" in sys.argv:
        probe()
