"""
Dùng trên GitHub Actions: tìm các kịch bản mới hoặc đã sửa trong scripts/, dựng video,
ghi danh sách video vừa xong vào ci_outputs.txt và cập nhật rendered.json.

  python ci_render.py                 # dựng kịch bản mới/đã sửa
  python ci_render.py --all           # dựng lại tất cả
  python ci_render.py --only DV1,CD-F1
"""
import hashlib
import json
import os
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

    # chi phí Gemini của lần chạy này (review.py gửi tổng kết lên Telegram)
    (ROOT / "chiphi_run.jsonl").unlink(missing_ok=True)

    # kiểm tra kịch bản TRƯỚC khi dựng: lỗi nội dung thì không dựng (đỡ tốn tiền giọng đọc, tranh, kiểm tra video)
    blocked = {}
    if os.environ.get("FV_SKIP_PRECHECK", "").strip().lower() not in ("1", "yes", "true") and (todo or todo_long):
        import review
        want = {}
        for f, sid, _ in todo:
            want.setdefault(sid, []).append("ngan")
        for f, sid, _ in todo_long[:MAX_LONG_PER_RUN]:
            want.setdefault(sid, []).append("dai")
        for sid, parts in want.items():
            print(f"\n===== {sid}: kiểm tra kịch bản trước khi dựng =====", flush=True)
            review.chi_phi_id(sid)
            try:
                errs = review.precheck(sid, parts)
            except Exception as e:
                print(f"   (bỏ qua bước kiểm tra trước: {e})")
                errs = []
            if errs:
                blocked[sid] = errs
                for x in errs:
                    print(f"   ❌ [{x['nhom']} · {x['vi_tri']}] {x['mo_ta']}")
                print(f"   ⛔ Chưa dựng {sid}: sửa kịch bản rồi đẩy lại (hoặc chạy với ô 'Bỏ qua kiểm tra' = yes)")
        todo = [x for x in todo if x[1] not in blocked]
        todo_long = [x for x in todo_long if x[1] not in blocked]
    (ROOT / "ci_blocked.json").write_text(json.dumps(blocked, ensure_ascii=False, indent=1), encoding="utf-8")

    done, failed, done_long, failed_long = [], [], [], []
    if len(todo) > MAX_PER_RUN:
        print(f"Có {len(todo)} kịch bản, lần này dựng {MAX_PER_RUN}, phần còn lại lần chạy sau.")
        todo = todo[:MAX_PER_RUN]
    for f, sid, d in todo:
        print(f"\n===== {sid} (video ngắn + bài ảnh) =====", flush=True)
        r = subprocess.run([sys.executable, str(ROOT / "make_video.py"), str(f), "--force"], env=dict(os.environ, FV_ID=sid))
        mp4 = ROOT / "output" / sid / f"{sid}.mp4"
        if r.returncode == 0 and mp4.exists():
            manifest[sid] = d
            done.append(sid)
        else:
            failed.append(sid)
        MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")

    for f, sid, dl in todo_long[:MAX_LONG_PER_RUN]:
        print(f"\n===== {sid} (video dài) =====", flush=True)
        r = subprocess.run([sys.executable, str(ROOT / "long_video.py"), str(f)], env=dict(os.environ, FV_ID=sid))
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
        print("Không có kịch bản mới cần dựng." if not blocked else "Không dựng gì (kịch bản có lỗi, xem ở trên).")
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
