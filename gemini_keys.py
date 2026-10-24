"""Nhiều khóa Gemini, tự đổi khóa khi một khóa hết lượt (429) / hết tiền (402) / bị từ chối (403).
Đọc: GEMINI_API_KEY, GEMINI_API_KEY_2 … _12, GEMINI_API_KEYS (cách nhau dấu phẩy/xuống dòng). Khóa trùng chỉ tính một."""
import os
import re
import time

_BAD = {}      # khóa -> thời điểm được dùng lại
_COOL = 90     # giây nghỉ cho một khóa vừa báo hết lượt (giới hạn theo phút); 402/403 nghỉ lâu hơn
_i = [0]


def all_keys():
    names = ["GEMINI_API_KEY"] + [f"GEMINI_API_KEY_{i}" for i in range(2, 13)]
    vals = [os.environ.get(n, "") for n in names] + re.split(r"[,\s]+", os.environ.get("GEMINI_API_KEYS", ""))
    out = []
    for v in vals:
        v = v.strip()
        if v and v not in out:
            out.append(v)
    return out


def has_key():
    return bool(all_keys())


def current():
    ks = all_keys()
    if not ks:
        return ""
    now = time.time()
    for n in range(len(ks)):
        k = ks[(_i[0] + n) % len(ks)]
        if _BAD.get(k, 0) <= now:
            _i[0] = (_i[0] + n) % len(ks)
            return k
    return ""   # mọi khóa đang nghỉ


def is_quota_error(msg):
    return any(c in msg for c in ("429", "402", "403", "401", "RESOURCE_EXHAUSTED", "PERMISSION_DENIED", "UNAUTHENTICATED"))


def mark_bad(key, msg=""):
    """Khóa này hết lượt: cho nghỉ rồi chuyển sang khóa kế. Trả về True nếu còn khóa khác dùng được."""
    long = any(c in msg for c in ("401", "402", "403", "PERMISSION_DENIED", "UNAUTHENTICATED", "prepayment", "per day", "PerDay"))
    _BAD[key] = time.time() + (6 * 3600 if long else _COOL)
    ks = all_keys()
    if key in ks:
        _i[0] = (ks.index(key) + 1) % len(ks)
    return bool(current())


def wait_seconds():
    """Giây phải đợi cho tới khi có khóa dùng lại được (0 nếu có rồi)."""
    if current():
        return 0
    ks = all_keys()
    return max(1, min(_BAD.get(k, 0) for k in ks) - time.time()) if ks else 0
