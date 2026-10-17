"""GEMINI XEM TỪNG ẢNH 2D của series Tam Quốc (quy tắc ảnh trong CLAUDE.md).

  python kiem_tra_tq.py TQ45 [dir=assets/anh_2d/CF_TQ45] [only=001,002] [suffix=_a]

Đọc ke-hoach/nhan-vat/<mã>.json (cảnh: nv, mo_ta) và <mã>_anh.json (prompt). Ảnh: <dir>/<key><suffix>.jpg.
Gemini (suffix=- nghĩa là không có hậu tố) trả JSON các lỗi theo quy tắc của chủ kênh: thừa tay/chân, người ngược, hai kiếm / kiếm trần ở hông, vũ khí sai hình, chữ trên cờ/tường,
mái nhà Hàn-Nhật, vật hiện đại (đèn treo, kính, nến, ghế tựa), người không có nền, hai người giống hệt, trẻ con, máu me, lạc đề.
Kết quả: logs/kiem_2d/<mã>_tq.json và <mã>_tq.txt (danh sách ảnh nên vẽ lại)."""
import json
import sys
import time
from pathlib import Path

import review

ROOT = Path(__file__).resolve().parent
PROMPT = """Bạn là biên tập viên hình ảnh của kênh lịch sử Tam Quốc (thời Đông Hán, thế kỷ 2). Ảnh là tranh 2D (truyện tranh nét sạch) vẽ bằng AI cho một cảnh phim. Hãy soi KỸ ảnh, chỉ báo lỗi THẬT SỰ nhìn thấy.
Cảnh cần vẽ: {mo_ta}
Nhân vật dự kiến (nếu có):
{chars}

Trả lời JSON đúng dạng:
{{"so_nguoi_thay": <số người nhìn thấy; hơn 8 người ở xa ghi 9>,
 "tay_chan_thua": [<người nào thừa/thiếu tay, chân, ngón, đầu, hoặc tay mọc từ chỗ lạ>],
 "nguoi_nguoc": [<người bị vẽ ngược (đầu xuống, quay mặt ra sau thân), lưng-mặt lẫn lộn, hai người dính nhau, mặt méo>],
 "kiem": [<người nào có HAI kiếm trở lên, kiếm chéo nhau, kiếm trần (thấy lưỡi) ở hông khi không cầm trong tay>],
 "vu_khi_sai": [<vũ khí vẽ sai hình: giáo/mâu thành đao hai lưỡi, kích có nhiều lưỡi, đao có hai lưỡi, cán cong, vũ khí xuyên người; chỉ nêu nếu rõ ràng>],
 "chu": <true nếu có chữ, ký tự, chữ giả hoặc biểu tượng trên cờ, tường, biển, vải>,
 "mai_han_nhat": <true nếu mái nhà/cửa/kiến trúc có góc mái cong vút kiểu Hàn-Nhật-Việt hiện đại thay vì nhà gạch bùn mái ngói xám thẳng thời Hán>,
 "sai_thoi": [<vật hiện đại hoặc sai thời: đèn treo/đèn đường, kính cửa, nến, ghế tựa có lưng, sách đóng gáy hoặc giấy, cốc có quai, dây điện, đường nhựa, mũ lưỡi trai, đồng hồ, bảng hiệu>],
 "khong_nen": <true nếu người/nhân vật đứng trên nền trơn một màu hoặc nền trắng/xám, không có bối cảnh>,
 "nguoi_giong_nhau": <true nếu có hai người trong ảnh có khuôn mặt/dáng/trang phục giống hệt nhau như nhân bản>,
 "lech_nhan_vat": [<CHỈ nhân vật bị vẽ lệch NẶNG: sai tuổi hẳn, hói không có búi tóc, mắt trắng không con ngươi, sai giới tính; KHÔNG báo thiếu kiếm ở hông, thiếu chi tiết nhỏ hay lệch màu áo nhẹ>],
 "tre_con": <true nếu ai đó trông như trẻ em hoặc hoạt hình tròn trịa mà cảnh không yêu cầu>,
 "mau_me": <true nếu có máu, vết thương, người bị đâm/chặt, xác>,
 "lac_de": <true nếu ảnh hoàn toàn không liên quan cảnh cần vẽ>,
 "diem": <1-5; 5 = dùng ngay; 3 = tạm được; 1-2 = phải vẽ lại>,
 "ghi_chu": "<một câu tiếng Việt: lỗi chính hoặc 'ổn'>"}}
Không phê bình phong cách. Bỏ qua tỉ lệ khung hình.
"""
NANG = ("tay_chan_thua", "nguoi_nguoc", "kiem", "vu_khi_sai", "sai_thoi", "lech_nhan_vat")


def ly_do(r):
    why = []
    for f in NANG:
        if r.get(f):
            why.append(f"{f}: " + "; ".join(map(str, r[f]))[:110])
    for f, t in (("chu", "có chữ"), ("mai_han_nhat", "mái Hàn/Nhật"), ("khong_nen", "người không có nền"),
                 ("nguoi_giong_nhau", "hai người giống hệt"), ("tre_con", "giống trẻ con"), ("mau_me", "máu me"), ("lac_de", "lạc đề")):
        if r.get(f):
            why.append(t)
    try:
        if int(r.get("diem", 5)) <= 2:
            why.append(f"điểm {r['diem']}/5")
    except Exception:
        pass
    return why


def main():
    ma = sys.argv[1]
    o = dict(a.split("=", 1) for a in sys.argv[2:] if "=" in a)
    d = ROOT / o.get("dir", f"assets/anh_2d/CF_{ma}")
    suf = o.get("suffix", "_a")
    suf = "" if suf == "-" else suf
    nv = json.loads((ROOT / "ke-hoach/nhan-vat" / f"{ma}.json").read_text(encoding="utf-8"))["canh"]
    anh = {x["key"]: x for x in json.loads((ROOT / "ke-hoach/nhan-vat" / f"{ma}_anh.json").read_text(encoding="utf-8"))}
    cn = {c["key"]: c for c in nv}
    only = [x for x in o.get("only", "").split(",") if x]
    keys = only or sorted(k for k in cn if (d / f"{k}{suf}.jpg").exists())
    from PIL import Image
    res, fail, t0 = {}, [], time.time()
    for i, k in enumerate(keys):
        try:
            p = anh[k]["prompt"]
            ch = p.split("Characters:", 1)[1].rsplit("2D ligne", 1)[0].strip() if "Characters:" in p else "(không có nhân vật chính)"
            small = ROOT / "output" / "_kttq" / f"{k}{suf}.jpg"
            small.parent.mkdir(parents=True, exist_ok=True)
            im = Image.open(d / f"{k}{suf}.jpg").convert("RGB")
            im.thumbnail((1280, 1280))
            im.save(small, quality=88)
            parts = [{"text": PROMPT.format(mo_ta=cn[k]["mo_ta"], chars=ch)}, review.img_part(small)]
            old = review.STAGE
            review.STAGE = "kiemtq"
            try:
                r = review.ask(parts, f"ktq_{ma}_{k}{suf}", ROOT / "output" / "_kttq", review.hashlib.sha1(small.read_bytes()).hexdigest())
            finally:
                review.STAGE = old
        except Exception as e:
            fail.append(k)
            print(f"{k}: không kiểm tra được ({str(e)[:120]})", flush=True)
            continue
        r["_ly_do"] = ly_do(r)
        res[k] = r
        print(f"{k}: điểm {r.get('diem')} · {'; '.join(r['_ly_do']) or 'ổn'} · {str(r.get('ghi_chu', ''))[:80]}", flush=True)
        if (i + 1) % 25 == 0:
            print(f"… {i + 1}/{len(keys)} ({time.time() - t0:.0f} giây)", flush=True)
    out = ROOT / "logs" / "kiem_2d"
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{ma}_tq.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    redo = [k for k, r in res.items() if r["_ly_do"]]
    lines = [f"GEMINI XEM ẢNH TAM QUỐC · {ma} · {len(res)}/{len(keys)} ảnh", f"Nên vẽ lại ({len(redo)}): {','.join(redo)}",
             f"Không kiểm tra được ({len(fail)}): {','.join(fail)}", ""]
    lines += [f"{k} · điểm {r.get('diem')} · {'; '.join(r['_ly_do']) or 'ổn'} · {r.get('ghi_chu', '')}" for k, r in res.items()]
    (out / f"{ma}_tq.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(lines[0], lines[1], lines[2], sep="\n")


if __name__ == "__main__":
    main()
