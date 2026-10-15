"""
VẼ ẢNH 2D + TỰ KIỂM + TỰ VẼ LẠI ẢNH LỖI (một lệnh, không cần người nhắc).

  python ve_kiem_anh.py TQ3                  -> vẽ ảnh chưa có, kiểm, vẽ lại ảnh lỗi, tối đa 3 vòng
  python ve_kiem_anh.py TQ3 vong=2           -> tối đa 2 vòng vẽ lại
  python ve_kiem_anh.py TQ3 chi_kiem=1       -> không vẽ, chỉ kiểm ảnh đang có (và ghi báo cáo)
  python ve_kiem_anh.py TQ3 only=007,031     -> chỉ làm các ảnh này

Mỗi ảnh qua ba lớp kiểm (lớp nào báo lỗi nặng thì vẽ lại ảnh đó với hạt giống mới):
  1. Kỹ thuật, miễn phí: quá nhỏ, mờ nhòe, gần một màu, vỡ khối.
  2. Trùng ảnh, miễn phí: hai ảnh quá giống nhau (mỗi ảnh chỉ dùng một lần trong video).
  3. Gemini xem từng ảnh (kiem_tra_2d.py): thừa/thiếu người, giống trẻ con, lệch nhân vật, tay chân méo, chữ lạ,
     sai thời (TQ: có ngựa, cờ có chữ, có máu, áo Minh/Thanh…), lạc đề so với lời kể.
Ảnh cũ bị loại được cất ở assets/anh_2d/<mã>/_loi/ . Báo cáo: logs/kiem_2d/<mã>_tong_hop.txt (+ .json).
Không có khóa Gemini thì lớp 3 KHÔNG chạy và báo rõ "chưa kiểm bằng AI" (không tính là đạt).
Thoát mã 0 = mọi ảnh đạt cả ba lớp; mã 2 = còn ảnh lỗi hoặc chưa kiểm được (người xem báo cáo).
"""
import json
import shutil
import sys
import time
from pathlib import Path

import kiem_tra_2d as k2d
import kiem_tra_anh

ROOT = Path(__file__).resolve().parent
NV = ROOT / "ke-hoach" / "nhan-vat"


def co_khoa_gemini():
    try:
        import review
        review._key()
        return True
    except Exception:
        return False


def dhash(path, n=16):
    from PIL import Image
    import numpy as np
    im = Image.open(path).convert("L").resize((n + 1, n))
    a = np.asarray(im, dtype=np.int16)
    return (a[:, 1:] > a[:, :-1]).flatten()


def trung_anh(ma, keys, nguong=0.06):
    """{key: 'trùng ảnh NNN'} cho ảnh đứng sau trong cặp quá giống nhau (tỉ lệ bit khác <= nguong)."""
    d = ROOT / "assets" / "anh_2d" / ma
    hs = {k: dhash(d / f"{k}.jpg") for k in sorted(keys) if (d / f"{k}.jpg").exists()}
    out = {}
    ks = list(hs)
    for i, a in enumerate(ks):
        for b in ks[:i]:
            if b in out:
                continue
            if float((hs[a] != hs[b]).mean()) <= nguong:
                out[a] = f"trùng ảnh {b}"
                break
    return out


def kiem(ma, keys, ai=True, log=print):
    """-> {key: {"loi": [...], "canh_bao": [...], "diem": n|None, "ghi_chu": str, "da_kiem_ai": bool}}"""
    sc, anh, spec, beats = k2d.load(ma)
    d = ROOT / "assets" / "anh_2d" / ma
    res = {}
    for k in keys:
        f = d / f"{k}.jpg"
        r = {"loi": [], "canh_bao": [], "diem": None, "ghi_chu": "", "da_kiem_ai": False}
        if not f.exists():
            r["loi"].append("chưa có ảnh")
            res[k] = r
            continue
        for muc, mo_ta in kiem_tra_anh.tech(str(f), "dai"):
            (r["loi"] if muc == "loi" else r["canh_bao"]).append(mo_ta)
        res[k] = r
    for k, v in trung_anh(ma, keys).items():
        res[k]["loi"].append(v)
    if not ai:
        return res
    for k in keys:
        if res[k]["loi"] and any(x == "chưa có ảnh" for x in res[k]["loi"]):
            continue
        try:
            g = k2d.kiem_tra_mot(k, ma, sc, anh, spec, beats, None)
        except Exception as e:
            res[k]["canh_bao"].append(f"Gemini không kiểm được: {str(e)[:80]}")
            continue
        named = [n for n in anh[k].get("nv", []) if n in spec.get("nhan_vat", {})]
        ly_do = k2d.danh_gia(g, len(named), ma)
        res[k]["loi"] += ly_do
        res[k]["diem"] = g.get("diem")
        res[k]["ghi_chu"] = str(g.get("ghi_chu", ""))[:120]
        res[k]["da_kiem_ai"] = True
        log(f"   {k}: điểm {g.get('diem')} · {'; '.join(ly_do) or 'ổn'}")
    return res


def ve(ma, keys, dot):
    """Vẽ các ảnh trong keys (dot=0: ảnh chưa có; dot>=1: vẽ lại với hạt giống mới). Trả về số ảnh nhận được."""
    import kaggle_draw
    items = {x["key"]: x for x in json.loads((NV / f"{ma}_anh.json").read_text(encoding="utf-8"))}
    out = ROOT / "assets" / "anh_2d" / ma
    out.mkdir(parents=True, exist_ok=True)
    jobs = []
    for k in keys:
        it = items[k]
        jobs.append((k, it["prompt"], it.get("w", 1344), it.get("h", 768), int(k) + 1000 * dot,
                     str(ROOT / it["sua_tu"]) if it.get("sua_tu") else ""))
    if not jobs:
        return 0
    print(f"Vẽ {len(jobs)} ảnh (đợt {dot})", flush=True)
    res = kaggle_draw.draw_batch(jobs, out, model="klein", timeout_min=150)
    print(f"Nhận về {len(res)}/{len(jobs)} ảnh", flush=True)
    return len(res)


def cat_anh_cu(ma, keys, vong):
    d = ROOT / "assets" / "anh_2d" / ma
    loi = d / "_loi"
    loi.mkdir(exist_ok=True)
    for k in keys:
        f = d / f"{k}.jpg"
        if f.exists():
            shutil.move(str(f), str(loi / f"{k}_vong{vong}.jpg"))


def main():
    ma = sys.argv[1]
    opts = dict(a.split("=", 1) for a in sys.argv[2:] if "=" in a)
    vong_max = int(opts.get("vong", 3))
    chi_kiem = opts.get("chi_kiem") == "1"
    items = json.loads((NV / f"{ma}_anh.json").read_text(encoding="utf-8"))
    tat_ca = [x["key"] for x in items]
    only = [x for x in opts.get("only", "").split(",") if x]
    keys = only or tat_ca
    d = ROOT / "assets" / "anh_2d" / ma
    ai = co_khoa_gemini()
    if not ai:
        print("⚠️ Không có khóa Gemini: bỏ lớp kiểm bằng AI (chỉ kiểm kỹ thuật và trùng ảnh).", flush=True)
    t0 = time.time()
    vong = 0
    # vòng 0: vẽ ảnh còn thiếu
    if not chi_kiem:
        thieu = [k for k in keys if not (d / f"{k}.jpg").exists()]
        if thieu:
            ve(ma, thieu, 0)
    while True:
        print(f"== Kiểm ảnh (vòng {vong}) ==", flush=True)
        res = kiem(ma, keys, ai)
        hong = [k for k, r in res.items() if r["loi"]]
        print(f"Vòng {vong}: {len(hong)} ảnh lỗi / {len(keys)}: {','.join(hong)}", flush=True)
        if chi_kiem or not hong or vong >= vong_max:
            break
        vong += 1
        cat_anh_cu(ma, hong, vong)
        ve(ma, hong, vong)
    # báo cáo
    chua_ai = [k for k, r in res.items() if not r["da_kiem_ai"] and not r["loi"]]
    lines = [f"TỔNG HỢP KIỂM ẢNH · {ma} · {len(keys)} ảnh · {time.time() - t0:.0f} giây · {vong} vòng vẽ lại",
             f"Còn lỗi ({len(hong)}): {','.join(hong) or 'không'}",
             f"Chưa kiểm bằng AI ({len(chua_ai)}): {','.join(chua_ai) or 'không'}", ""]
    for k in keys:
        r = res[k]
        lines.append(f"{k} · {'LỖI: ' + '; '.join(r['loi']) if r['loi'] else 'đạt'}"
                     f"{' · cảnh báo: ' + '; '.join(r['canh_bao']) if r['canh_bao'] else ''}"
                     f"{' · điểm ' + str(r['diem']) if r['diem'] else ''}")
    out = ROOT / "logs" / "kiem_2d"
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{ma}_tong_hop.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (out / f"{ma}_tong_hop.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\n".join(lines[:3]))
    sys.exit(0 if (not hong and not chua_ai) else 2)


if __name__ == "__main__":
    main()
