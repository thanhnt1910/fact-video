"""Sổ ghi video đã gửi Telegram (mỗi mã + loại chỉ gửi MỘT lần).
  python da_gui.py check PV7 ngan   -> thoát 0 nếu ĐÃ gửi rồi (bỏ qua), 1 nếu chưa
  python da_gui.py mark PV7 ngan    -> ghi nhận đã gửi
Gửi lại có chủ đích: đặt biến GUI_LAI=yes (check luôn trả 1)."""
import datetime as dt
import json
import os
import sys
from pathlib import Path

F = Path(__file__).resolve().parent / "logs" / "da_gui.json"


def load():
    try:
        return json.loads(F.read_text(encoding="utf-8"))
    except Exception:
        return {}


if __name__ == "__main__":
    cmd, sid, kind = sys.argv[1:4]
    key = f"{sid}:{kind}"
    d = load()
    if cmd == "check":
        sys.exit(1 if os.environ.get("GUI_LAI") == "yes" or key not in d else 0)
    d[key] = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    F.parent.mkdir(exist_ok=True)
    F.write_text(json.dumps(d, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8")
