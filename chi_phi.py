"""
GHI CHI PHÍ GEMINI / VEO của mỗi lần dựng (ước tính theo bảng giá, để biết video nào tốn bao nhiêu).

- Mỗi lần gọi Gemini (giọng đọc, tự kiểm tra) hoặc Veo ghi 1 dòng vào chiphi_run.jsonl.
- ci_render.py xóa file này đầu mỗi lần chạy; review.py gửi bảng tổng kết kèm báo cáo Telegram
  và lưu logs/chiphi_<mã>.txt.

Giá là ƯỚC TÍNH (USD cho 1 triệu token, hoặc USD/giây với Veo). Số chính xác xem ở
Google Cloud Billing → Reports → Group by SKU.
"""
import json
import os
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RUN = ROOT / "chiphi_run.jsonl"
VND = float(os.environ.get("USD_VND", "26500"))

# (từ khóa trong tên model, giá đầu vào, giá đầu ra) — dòng đầu tiên khớp được dùng
TOKEN_PRICES = [
    (("tts", "pro"), 1.00, 20.00),
    (("tts",), 0.50, 10.00),
    (("lite",), 0.10, 0.40),
    (("pro",), 1.25, 10.00),
    (("flash",), 0.30, 2.50),
]
VEO_PRICES = [("lite", 0.05), ("fast", 0.10), ("veo", 0.40)]   # USD / giây video 720p

CURRENT = os.environ.get("FV_ID", "")


def _price(model):
    m = model.lower()
    for keys, pin, pout in TOKEN_PRICES:
        if all(k in m for k in keys):
            return pin, pout
    return TOKEN_PRICES[-1][1:]


def _write(row):
    row.setdefault("id", CURRENT or os.environ.get("FV_ID", "") or "?")
    row["t"] = time.strftime("%H:%M:%S")
    try:
        with RUN.open("a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    except Exception:
        pass


def add_tokens(kind, model, tokens_in, tokens_out, sid=None):
    pin, pout = _price(model)
    usd = (tokens_in * pin + tokens_out * pout) / 1e6
    _write({"kind": kind, "model": model, "in": int(tokens_in), "out": int(tokens_out), "usd": usd, **({"id": sid} if sid else {})})
    return usd


def add_usage(kind, model, usage, sid=None):
    """usage: usageMetadata trong phản hồi Gemini."""
    u = usage or {}
    tin = u.get("promptTokenCount", 0) or 0
    tout = (u.get("candidatesTokenCount", 0) or 0) + (u.get("thoughtsTokenCount", 0) or 0)
    return add_tokens(kind, model, tin, tout, sid)


def add_video(model, seconds, sid=None):
    rate = next((p for k, p in VEO_PRICES if k in model.lower()), VEO_PRICES[-1][1])
    usd = rate * seconds
    _write({"kind": "veo", "model": model, "giay": seconds, "usd": usd, **({"id": sid} if sid else {})})
    return usd


KIND_NAME = {"tts": "Giọng đọc", "review": "Tự kiểm tra", "precheck": "Kiểm tra kịch bản trước khi dựng", "veo": "Veo"}


def rows():
    if not RUN.exists():
        return []
    out = []
    for line in RUN.read_text(encoding="utf-8").splitlines():
        try:
            out.append(json.loads(line))
        except Exception:
            pass
    return out


def summary(sid=None):
    """Bảng chi phí ước tính (theo mã nếu có)."""
    rs = [r for r in rows() if sid is None or r.get("id") == sid]
    if not rs:
        return ""
    by = {}
    for r in rs:
        by[r["kind"]] = by.get(r["kind"], 0) + r["usd"]
    total = sum(by.values())
    head = f"💰 Chi phí Gemini ước tính{(' cho ' + sid) if sid else ' lần chạy này'}: ~{total * VND:,.0f}đ".replace(",", ".")
    lines = [head] + [f"   • {KIND_NAME.get(k, k)}: ~{v * VND:,.0f}đ".replace(",", ".") for k, v in by.items()]
    return "\n".join(lines)


if __name__ == "__main__":
    print(summary() or "Chưa có chi phí nào trong lần chạy này.")
