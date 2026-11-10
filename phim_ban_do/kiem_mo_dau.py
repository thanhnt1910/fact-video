"""Kiểm phần mở đầu kịch bản: 25 giây đầu không được dồn năm, tên sách, tên riêng (số liệu Metricool 10/11/2026: người xem
rời đi ngay sau câu hook, đúng chỗ dồn mốc năm và tên). Chạy trước khi đọc giọng.

    python phim_ban_do/kiem_mo_dau.py <mã> [<mã> ...] [--cua-so 25]

Đọc ke-hoach/thu-giong-hai/<mã>_full.json (trường `hien` nếu có, không thì `text`). Thời điểm từng đoạn lấy từ
assets/thu_giong_hai/<mã>_chuan/thoi_luong.json nếu có, không thì ước tính 3,3 chữ mỗi giây cộng 0,4 giây nghỉ.
Quy tắc (❌ = sửa trước khi đọc giọng):
  ❌ trong cửa sổ: số năm + số lần trích nguồn >= 2
  ❌ đoạn ngay sau hook (đoạn 2) có năm hoặc trích nguồn
  ⚠️ trong cửa sổ: tên riêng mới > 4
  ⚠️ đoạn nào có từ 2 "vật nặng" (năm, nguồn, tên riêng) trở lên trong cửa sổ
Thoát mã 1 nếu có ❌.
"""
import json
import re
import sys
from pathlib import Path

R = Path(__file__).resolve().parent.parent
NGUONG_TEN = 4
CITE = re.compile(r"\b(Theo|theo|Sử chép|sử chép|sử sách|Sử sách)\b[^,.?!]{0,60}(sử|Sử|toàn thư|Toàn thư|thực lục|UNESCO|báo|Báo|Trung tâm|Viện|Bảo tàng|sách|Sách)")
NAM_SO = re.compile(r"\b(1[0-9]{3}|20[0-9]{2}|[2-9][0-9]{2})\b")
NAM_CHU = re.compile(r"\bnăm (một nghìn|hai nghìn|chín trăm|tám trăm|bảy trăm|sáu trăm|năm trăm)\b", re.I)
NOI = {"và", "của", "de", "du", "le", "la", "von", "van"}


def ten_rieng(cau):
    """Đếm cụm chữ hoa không đứng đầu câu (tên riêng); gộp các chữ hoa liền nhau (có thể xen từ nối)."""
    out = []
    for s in re.split(r"(?<=[.?!])\s+", cau):
        tu = re.findall(r"[^\s,.;:?!()\"“”]+", s)
        cur = []
        for i, w in enumerate(tu):
            if i > 0 and w[:1].isupper() and not w.isdigit():
                cur.append(w)
            elif cur and w.lower() in NOI:
                cur.append(w)
            else:
                if cur:
                    out.append(" ".join(cur).strip())
                cur = []
        if cur:
            out.append(" ".join(cur).strip())
    return list(dict.fromkeys(x for x in out if x.split()[-1].lower() not in NOI))


def chuan_hoa_nam(t):
    return len(set(NAM_SO.findall(t))) or len(NAM_CHU.findall(t))


def kiem(ma, cua_so):
    f = R / f"ke-hoach/thu-giong-hai/{ma}_full.json"
    d = json.load(open(f, encoding="utf-8"))
    dp = R / f"assets/thu_giong_hai/{ma}_chuan/thoi_luong.json"
    T = json.load(open(dp)) if dp.exists() else {}
    uoc = not T
    t = 0.3
    rows = []
    da_ten = set()
    tong_nam = tong_nguon = 0
    for k, s in enumerate(d):
        txt = s.get("hien", s["text"])
        du = T.get(str(s["n"])) if T else None
        if du is None:
            du = len(s["text"].split()) / 3.3
        nam = chuan_hoa_nam(txt)
        nguon = len(CITE.findall(txt))
        moi = [x for x in ten_rieng(txt) if x not in da_ten]
        rows.append(dict(i=k + 1, t=t, nam=nam, nguon=nguon, ten=moi, w=len(s["text"].split()), txt=txt))
        if t < cua_so:
            da_ten.update(moi)
            tong_nam += nam
            tong_nguon += nguon
        t += du + 0.4
    loi, canh = [], []
    trong = [r for r in rows if r["t"] < cua_so]
    ten_cs = sum(len(r["ten"]) for r in trong)
    if tong_nam + tong_nguon >= 2:
        loi.append(f"{cua_so} giây đầu có {tong_nam} mốc năm và {tong_nguon} lần trích nguồn (tối đa 1 tổng cộng)")
    if len(rows) > 1 and (rows[1]["nam"] or rows[1]["nguon"]) and rows[1]["t"] < cua_so:
        loi.append(f"đoạn 2 (giây {rows[1]['t']:.0f}) có {'năm' if rows[1]['nam'] else 'trích nguồn'}: ngay sau hook phải là bước ngoặt hoặc điều hứa hẹn, không phải bối cảnh")
    if ten_cs > NGUONG_TEN:
        canh.append(f"{ten_cs} tên riêng mới trong {cua_so} giây đầu (nên tối đa {NGUONG_TEN})")
    for r in trong:
        nang = (1 if r["nam"] else 0) + (1 if r["nguon"] else 0) + (1 if len(r["ten"]) >= 2 else 0)
        if nang >= 2 and r["i"] > 1:
            canh.append(f"đoạn {r['i']} (giây {r['t']:.0f}) dồn nặng: năm={r['nam']}, nguồn={r['nguon']}, tên mới={r['ten']}")
    return rows, loi, canh, uoc


def main():
    a = sys.argv[1:]
    cs = 25.0
    if "--cua-so" in a:
        i = a.index("--cua-so")
        cs = float(a[i + 1])
        del a[i:i + 2]
    if not a:
        print(__doc__)
        return 2
    ma_loi = 0
    for ma in a:
        try:
            rows, loi, canh, uoc = kiem(ma, cs)
        except FileNotFoundError:
            print(f"{ma}: không có ke-hoach/thu-giong-hai/{ma}_full.json")
            ma_loi = 2
            continue
        print(f"\n== {ma} (cửa sổ {cs:.0f}s, thời điểm {'ƯỚC TÍNH' if uoc else 'theo giọng thật'})")
        for r in rows:
            if r["t"] < cs:
                print(f"  {r['t']:5.1f}s đoạn {r['i']:2d} | năm={r['nam']} nguồn={r['nguon']} tên mới={len(r['ten'])} | {r['txt'][:80]}")
        for x in loi:
            print("  ❌", x)
        for x in canh:
            print("  ⚠️", x)
        if not loi and not canh:
            print("  ✅ mở đầu gọn")
        if loi:
            ma_loi = max(ma_loi, 1)
    return ma_loi


if __name__ == "__main__":
    sys.exit(main())
