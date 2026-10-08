"""
Dùng trên GitHub Actions: tìm các kịch bản mới hoặc đã sửa trong scripts/, dựng video,
ghi danh sách video vừa xong vào ci_outputs.txt và cập nhật rendered.json.

  python ci_render.py                 # dựng kịch bản mới/đã sửa
  python ci_render.py --all           # dựng lại tất cả
  python ci_render.py --only DV1,CD-F1
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "rendered.json"
MAX_PER_RUN = 12

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def digest(script_path):
    cfg = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
    voice_cfg = {k: cfg.get(k) for k in ("tts_engine", "vieneu", "voice", "voice_rate", "channel")}
    h = hashlib.sha256()
    h.update(script_path.read_bytes())
    h.update(json.dumps(voice_cfg, sort_keys=True, ensure_ascii=False).encode())
    return h.hexdigest()[:16]


def main():
    args = sys.argv[1:]
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.exists() else {}
    files = sorted((ROOT / "scripts").glob("*.json"))
    only = None
    if "--only" in args:
        only = {x.strip() for x in args[args.index("--only") + 1].split(",") if x.strip()}

    todo = []
    for f in files:
        try:
            sid = json.loads(f.read_text(encoding="utf-8")).get("id", f.stem)
        except Exception:
            sid = f.stem
        d = digest(f)
        if only is not None:
            if sid in only or f.stem in only:
                todo.append((f, sid, d))
        elif "--all" in args or manifest.get(sid) != d:
            todo.append((f, sid, d))

    if not todo:
        print("Không có kịch bản mới cần dựng.")
        (ROOT / "ci_outputs.txt").write_text("", encoding="utf-8")
        return
    if len(todo) > MAX_PER_RUN:
        print(f"Có {len(todo)} kịch bản, lần này dựng {MAX_PER_RUN}, phần còn lại lần chạy sau.")
        todo = todo[:MAX_PER_RUN]

    done, failed = [], []
    for f, sid, d in todo:
        print(f"\n===== {sid} =====", flush=True)
        r = subprocess.run([sys.executable, str(ROOT / "make_video.py"), str(f), "--force"])
        mp4 = ROOT / "output" / sid / f"{sid}.mp4"
        if r.returncode == 0 and mp4.exists():
            manifest[sid] = d
            done.append(sid)
        else:
            failed.append(sid)

    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    (ROOT / "ci_outputs.txt").write_text("\n".join(done), encoding="utf-8")
    print(f"\nXong: {', '.join(done) or '-'}")
    if failed:
        print(f"Lỗi: {', '.join(failed)}")
        (ROOT / "ci_failed.txt").write_text("\n".join(failed), encoding="utf-8")
        sys.exit(1)


if __name__ == "__main__":
    main()
