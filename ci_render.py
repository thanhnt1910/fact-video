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
MAX_LONG_PER_RUN = 2
MAX_PER_RUN = 12

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def digest(script_path, part="short"):
    """Mã nhận diện nội dung: video ngắn (bỏ phần "long") hoặc video dài (chỉ phần "long")."""
    cfg = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
    data = json.loads(script_path.read_text(encoding="utf-8"))
    if part == "long":
        payload = {"long": data.get("long"), "topic": data.get("topic"), "cfg": cfg.get("long")}
    else:
        data.pop("long", None)
        payload = {"script": data, "voice": {k: cfg.get(k) for k in ("tts_engine", "vieneu", "voice", "voice_rate", "channel")}}
    return hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:16]


def main():
    args = sys.argv[1:]
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.exists() else {}
    files = sorted((ROOT / "scripts").glob("*.json"))
    only = None
    if "--only" in args:
        only = {x.strip() for x in args[args.index("--only") + 1].split(",") if x.strip()}

    todo, todo_long = [], []
    for f in files:
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            data = {}
        sid = data.get("id", f.stem)
        d, dl = digest(f), digest(f, "long")
        if only is not None:
            if sid in only or f.stem in only or f"{sid}:ngan" in only:
                todo.append((f, sid, d))
            if data.get("long") and (sid in only or f.stem in only or f"{sid}:dai" in only):
                todo_long.append((f, sid, dl))
        else:
            if "--all" in args or manifest.get(sid) != d:
                todo.append((f, sid, d))
            if data.get("long") and ("--all" in args or manifest.get(sid + ":dai") != dl):
                todo_long.append((f, sid, dl))

    done, failed, done_long, failed_long = [], [], [], []
    if len(todo) > MAX_PER_RUN:
        print(f"Có {len(todo)} kịch bản, lần này dựng {MAX_PER_RUN}, phần còn lại lần chạy sau.")
        todo = todo[:MAX_PER_RUN]
    for f, sid, d in todo:
        print(f"\n===== {sid} (video ngắn + bài ảnh) =====", flush=True)
        r = subprocess.run([sys.executable, str(ROOT / "make_video.py"), str(f), "--force"])
        mp4 = ROOT / "output" / sid / f"{sid}.mp4"
        if r.returncode == 0 and mp4.exists():
            manifest[sid] = d
            done.append(sid)
        else:
            failed.append(sid)
        MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")

    for f, sid, dl in todo_long[:MAX_LONG_PER_RUN]:
        print(f"\n===== {sid} (video dài) =====", flush=True)
        r = subprocess.run([sys.executable, str(ROOT / "long_video.py"), str(f)])
        mp4 = ROOT / "output" / sid / f"{sid}_dai.mp4"
        if r.returncode == 0 and mp4.exists():
            manifest[sid + ":dai"] = dl
            done_long.append(sid)
        else:
            failed_long.append(sid)
        MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")

    (ROOT / "ci_outputs.txt").write_text("".join(x + "\n" for x in done), encoding="utf-8")
    (ROOT / "ci_long.txt").write_text("".join(x + "\n" for x in done_long), encoding="utf-8")
    (ROOT / "ci_long_failed.txt").write_text("".join(x + "\n" for x in failed_long), encoding="utf-8")
    if not todo and not todo_long:
        print("Không có kịch bản mới cần dựng.")
        return
    print(f"\nXong video ngắn: {', '.join(done) or '-'} · video dài: {', '.join(done_long) or '-'}")
    if failed_long:
        print(f"Video dài chưa xong (sẽ thử lại lần chạy sau): {', '.join(failed_long)}")
    if failed:
        print(f"Lỗi: {', '.join(failed)}")
        (ROOT / "ci_failed.txt").write_text("".join(x + "\n" for x in failed), encoding="utf-8")
        sys.exit(1)


if __name__ == "__main__":
    main()
