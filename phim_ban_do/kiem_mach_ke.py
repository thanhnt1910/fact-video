"""Kiểm mạch kể của kịch bản (bổ sung cho kiem_mo_dau.py và kiem_kich_ban.py).

    python phim_ban_do/kiem_mach_ke.py <mã> [<mã> ...]

Đọc ke-hoach/thu-giong-hai/<mã>_full.json (trường `hien` nếu có, không thì `text`). Đo:
  - độ dài câu hook (đoạn 1): ❌ > 25 chữ, ⚠️ > 20 chữ; ❌ nếu hook có năm
  - tỷ lệ đoạn mở bằng từ nối (nên, nhưng, thế là, vậy, vì thế, nhờ vậy, còn, rồi...): ⚠️ dưới 25%
  - chuỗi đoạn liên tiếp mở bằng cùng một chữ: ❌ từ 2 đoạn liền
  - số lần trích nguồn "Theo ...": ⚠️ > 2
  - đoạn có từ 2 con số/năm trở lên: ⚠️
  - đoạn có từ 4 tên riêng trở lên: ⚠️
  - số ý chính: không giới hạn (chủ kênh bỏ quy tắc 5-7 ý ngày 11/11/2026; độ dài và số ý theo nhu cầu giải thích)
Thoát mã 1 nếu có ❌.
"""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from kiem_mo_dau import ten_rieng, NAM_SO, NAM_CHU, CITE, R

NOI = ("nên", "nhưng", "thế là", "vậy", "vì thế", "nhờ vậy", "còn", "rồi", "vì", "do đó", "bởi", "tuy", "trong khi", "đến", "thế nhưng", "nhờ")
SO = re.compile(r"\d[\d.,]*")


def kiem(ma):
    d = json.load(open(R / f"ke-hoach/thu-giong-hai/{ma}_full.json", encoding="utf-8"))
    T = [(x["n"], x.get("hien") or x["text"], x["text"]) for x in d]
    loi = warn = 0
    print(f"== {ma}: {len(T)} đoạn")
    hook = T[0][1]
    nh = len(hook.split())
    print(f"   hook {nh} chữ: {hook}")
    if nh > 25 or SO.search(re.sub(r"\d[\d.]{3,}\s*đồng", "", hook)) and NAM_SO.search(hook):
        print("❌ hook quá dài hoặc có năm"); loi += 1
    elif nh > 20:
        print("⚠️ hook trên 20 chữ"); warn += 1
    dau = [t[2].split()[0].lower().strip(",.") for t in T]
    nd = sum(1 for t in T[1:] if t[2].lower().startswith(NOI))
    ty = nd / max(1, len(T) - 1)
    print(f"   đoạn mở bằng từ nối: {nd}/{len(T)-1} = {ty:.0%}")
    if ty < 0.25:
        print("⚠️ ít từ nối (mạch kể rời rạc)"); warn += 1
    for i in range(1, len(T)):
        if dau[i] == dau[i - 1]:
            print(f"❌ đoạn {T[i-1][0]} và {T[i][0]} cùng mở bằng \"{dau[i]}\""); loi += 1
    ct = sum(len(CITE.findall(t[1])) for t in T)
    print(f"   trích nguồn 'Theo...': {ct}")
    if ct > 2:
        print("⚠️ trích nguồn quá 2 lần"); warn += 1
    for n, h, _ in T:
        so = {m.strip('.,') for m in SO.findall(h)} - {''}
        if len(so) >= 2:
            print(f"⚠️ đoạn {n}: {len(so)} con số {sorted(so)}"); warn += 1
        tr = ten_rieng(h)
        if len(tr) >= 4:
            print(f"⚠️ đoạn {n}: {len(tr)} tên riêng {tr}"); warn += 1
    print(f"   -> {loi} ❌, {warn} ⚠️")
    return loi


if __name__ == "__main__":
    r = sum(kiem(m) for m in sys.argv[1:] if not m.startswith("-"))
    sys.exit(1 if r else 0)
