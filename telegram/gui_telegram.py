#!/usr/bin/env python3
"""Gửi bài Telegram từng tập: album (thẻ chữ + ảnh 2D) có caption, rồi các tin nội dung.

Dùng:
  BOT_TOKEN=... CHAT_ID=@kenh_cua_ban python3 gui_telegram.py 1 2 3
  python3 gui_telegram.py --dry-run 1 2 3      (chỉ kiểm tra độ dài và file ảnh, không gửi)

Cần: pip install requests. Bot phải là quản trị viên của kênh/nhóm nhận tin.
Không đặt CHAT_ID thì đọc telegram_chat_id.txt cạnh script hoặc ở thư mục cha.
"""
import json, os, re, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import noi_dung as n


def plain(s):
    return re.sub(r"<[^>]+>", "", s)


def album_files(k):
    """Thẻ chữ đầu tiên, rồi các ảnh 2D (nếu tập có)."""
    t = n.TAP[k]
    files = [os.path.join(HERE, t["anh"])]
    files += [os.path.join(HERE, "anh", rel) for rel in n.ANH2D.get(k, [])]
    return files


def kiem_tra(eps):
    for k in eps:
        t = n.TAP[k]
        assert len(plain(t["caption"])) <= 1024, f"tập {k}: caption quá 1024"
        for i, m in enumerate(t["tin"], 1):
            assert len(plain(m)) <= 4096, f"tập {k}: tin {i} quá 4096"
        fs = album_files(k)
        assert len(fs) <= 10, f"tập {k}: album quá 10 ảnh"
        for f in fs:
            assert os.path.isfile(f), f"thiếu ảnh {f}"
        print(f"Tập {k}: OK ({len(fs)} ảnh, {len(t['tin'])} tin nội dung)")


def kiem_loi(r, nhan):
    """Báo lỗi Telegram rõ ràng (không in token) rồi dừng."""
    if r.status_code != 200:
        print(f"::error::{nhan}: HTTP {r.status_code} {r.text[:300]}")
        sys.exit(1)


def main(argv):
    dry = "--dry-run" in argv
    eps = [int(a) for a in argv if a.isdigit()] or sorted(n.TAP)
    kiem_tra(eps)
    if dry:
        return
    import requests
    token = os.environ.get("BOT_TOKEN", "")
    if not token:
        print("::error::Chưa có secret TELEGRAM_BOT_TOKEN trong repo")
        sys.exit(1)
    chat = os.environ.get("CHAT_ID")
    if not chat:
        for d in (HERE, os.path.dirname(HERE)):
            p = os.path.join(d, "telegram_chat_id.txt")
            if os.path.isfile(p):
                chat = open(p, encoding="utf-8").read().strip()
                break
    assert chat, "Chưa có CHAT_ID"
    api = f"https://api.telegram.org/bot{token}"
    for k in eps:
        t = n.TAP[k]
        fs = album_files(k)
        if len(fs) == 1:
            with open(fs[0], "rb") as f:
                r = requests.post(f"{api}/sendPhoto", data={"chat_id": chat, "caption": t["caption"], "parse_mode": "HTML"}, files={"photo": f}, timeout=120)
        else:
            media, files, handles = [], {}, []
            for i, p in enumerate(fs):
                h = open(p, "rb"); handles.append(h); files[f"f{i}"] = h
                item = {"type": "photo", "media": f"attach://f{i}"}
                if i == 0:
                    item["caption"], item["parse_mode"] = t["caption"], "HTML"
                media.append(item)
            r = requests.post(f"{api}/sendMediaGroup", data={"chat_id": chat, "media": json.dumps(media)}, files=files, timeout=300)
            for h in handles:
                h.close()
        kiem_loi(r, f'tập {k}: album'); time.sleep(2)
        for m in t["tin"]:
            r = requests.post(f"{api}/sendMessage", data={"chat_id": chat, "text": m, "parse_mode": "HTML", "disable_web_page_preview": "true"}, timeout=60)
            kiem_loi(r, f'tập {k}: tin nội dung'); time.sleep(1.5)
        print("Đã gửi tập", k)


if __name__ == "__main__":
    main(sys.argv[1:])
