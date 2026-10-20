"""
Gửi nội dung đăng bài (tiêu đề, caption, hashtag, tag, ghi chú...) về Telegram, ngay sau tin video.

Dùng: python tg_text.py <file .txt> "<tiêu đề tin>"
Cần biến môi trường TG_TOKEN, TG_CHAT.

- Chia file theo các mục (dòng bắt đầu bằng "════" hoặc "────"); mỗi mục là một khối <pre>
  để bấm vào là copy được trên Telegram.
- Telegram giới hạn 4.096 ký tự mỗi tin: các mục được gom vào tin cho tới gần giới hạn;
  mục nào quá dài thì tách theo dòng, không cắt giữa một dòng.
"""
import html
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

LIMIT = 3800  # chừa chỗ cho thẻ HTML, dưới giới hạn 4.096 của Telegram


def sections(text):
    """Tách thành [(tên mục, nội dung)]. Dòng tiêu đề mục: bắt đầu bằng ════ hoặc ────."""
    out, name, buf = [], "", []
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("════") or s.startswith("────"):
            if any(x.strip() for x in buf):
                out.append((name, "\n".join(buf).strip("\n")))
            name, buf = s.strip("═─ ").strip(), []
        else:
            buf.append(line)
    if any(x.strip() for x in buf):
        out.append((name, "\n".join(buf).strip("\n")))
    return out


def blocks(name, body):
    """Một mục -> một hay nhiều khối HTML (mỗi khối < LIMIT)."""
    head = f"<b>{html.escape(name)}</b>\n" if name else ""
    pieces, cur = [], []
    for line in body.splitlines():
        trial = "\n".join(cur + [line])
        if cur and len(html.escape(trial)) + len(head) + 20 > LIMIT:
            pieces.append("\n".join(cur))
            cur = [line]
        else:
            cur.append(line)
    if cur:
        pieces.append("\n".join(cur))
    res = []
    for k, p in enumerate(pieces):
        h = head if k == 0 else (f"<b>{html.escape(name)} (tiếp)</b>\n" if name else "")
        # dòng quá dài một mình vẫn bị cắt cứng để không lỗi gửi
        res.append(h + "<pre>" + html.escape(p)[: LIMIT - len(h) - 20] + "</pre>")
    return res


def messages(title, text):
    msgs, cur = [], f"<b>{html.escape(title)}</b>"
    for name, body in sections(text):
        for b in blocks(name, body):
            if len(cur) + len(b) + 2 > LIMIT:
                msgs.append(cur)
                cur = b
            else:
                cur = cur + "\n\n" + b
    if cur:
        msgs.append(cur)
    return msgs


def send(msg):
    token, chat = os.environ.get("TG_TOKEN"), os.environ.get("TG_CHAT")
    if not chat and Path("telegram_chat_id.txt").exists():
        chat = Path("telegram_chat_id.txt").read_text().strip()
    data = urllib.parse.urlencode({"chat_id": chat, "text": msg, "parse_mode": "HTML",
                                   "disable_web_page_preview": "true"}).encode()
    req = urllib.request.Request(f"https://api.telegram.org/bot{token}/sendMessage", data=data)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r).get("ok")
    except urllib.error.HTTPError as e:
        print("Telegram báo lỗi:", e.code, e.read().decode("utf-8", "replace")[:300])
        return False


def main():
    if len(sys.argv) < 3:
        print("Dùng: python tg_text.py <file> <tiêu đề>")
        return 1
    f = Path(sys.argv[1])
    if not f.exists():
        print(f"Không có {f}, bỏ qua tin nội dung.")
        return 0
    msgs = messages(sys.argv[2], f.read_text(encoding="utf-8"))
    if os.environ.get("TG_DRY"):
        for m in msgs:
            print(f"--- tin ({len(m)} ký tự) ---\n{m}\n")
        return 0
    for m in msgs:
        print("Gửi nội dung:", "ok" if send(m) else "LỖI")
    return 0


if __name__ == "__main__":
    sys.exit(main())
