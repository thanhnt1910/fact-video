"""
GEMINI XEM TỪNG ẢNH 2D của một câu chuyện (nhân vật vẽ sẵn, ảnh nằm ở assets/anh_2d/<mã>/NNN.jpg).

  python kiem_tra_2d.py ST3 [ref=đường dẫn ảnh bảng nhân vật] [only=001,002,...]

Mỗi ảnh gửi cho Gemini cùng: bảng nhân vật mẫu (nếu có), mô tả cố định các nhân vật được cho là có mặt, lời kể của cảnh.
Gemini trả JSON: số người thấy / số người dự kiến, nhân vật nào trông như trẻ con, lệch nét so với bảng mẫu,
lỗi giải phẫu, chữ lạ, vật sai thời, ảnh lạc đề. Kết quả ghi logs/kiem_2d/<mã>.json và <mã>.txt (danh sách ảnh nên vẽ lại).
"""
import json
import sys
import time
from pathlib import Path

import review

ROOT = Path(__file__).resolve().parent

# Quy ước riêng từng loạt (khóa = tiền tố mã). era: mô tả "sai thời"; extra: trường JSON thêm; cac_loi: đổi tên trường -> lý do vẽ lại.
SERIES_MAC_DINH = {"era": "vật hiện đại không đúng năm 1914-1917, ví dụ máy tính, máy ảnh SLR, nhà kính hiện đại", "extra": "", "cac_loi": {}}
SERIES = {
    "TQ": {
        "era": "vật, trang phục không đúng Đông Hán năm 184-192 SCN: áo kiểu Minh/Thanh, bím tóc Mãn Thanh, trang điểm hí kịch, bàn đạp ngựa, súng, đường nhựa có vạch kẻ, cột điện, đèn điện / bóng đèn / chao đèn / đèn bàn / đèn lồng thủy tinh, cửa sổ kính ô vuông, ổ cắm hoặc công tắc trên tường, khung tranh, sách đóng gáy hiện đại, cốc có quai kiểu phương Tây, ghế kiểu phương Tây, vật hiện đại",
        "extra": ('"co_ngua": <true nếu có con ngựa nhìn thấy trong ảnh>, '
                  '"co_chu_bieu_tuong": <true nếu cờ, biển, áo hoặc vật nào có chữ, ký tự hay biểu tượng nhìn rõ; cờ phải trơn một màu>, '
                  '"bao_luc": <true nếu thấy máu, người bị chém, bị đâm, thi thể hoặc cảnh giết>, '
                  '"hai_nguoi_giong_het": <true nếu hai người trong ảnh có cùng một khuôn mặt, dáng, áo gần như sao chép nhau>, '
                  '"vat_sai_cau_tao": <true nếu có vật méo hoặc sai cấu tạo: vòi ấm ngược, vật lơ lửng không có chỗ đỡ, chim hoặc đồ vật đậu giữa không trung, cầu hoặc nhà vô lý, vật thừa/thiếu một phần>, '
                  '"khung_vien": <true nếu ảnh có viền khung đen hoặc viền trắng quanh mép>, '),
        "cac_loi": {"co_ngua": "có ngựa (quy ước không vẽ ngựa)", "co_chu_bieu_tuong": "cờ/vật có chữ hoặc biểu tượng",
                    "bao_luc": "có máu hoặc cảnh giết (không được)",
                    "hai_nguoi_giong_het": "hai người giống hệt nhau", "vat_sai_cau_tao": "vật sai cấu tạo / lơ lửng",
                    "khung_vien": "ảnh có viền khung"},
    },
}


def series(ma):
    for k, v in SERIES.items():
        if ma.startswith(k):
            return v
    return SERIES_MAC_DINH


PROMPT = """Bạn là biên tập viên hình ảnh của kênh kể chuyện lịch sử. Ảnh cần kiểm tra là tranh 2D vẽ bằng AI cho một cảnh phim.
Câu chuyện: {story}
Phong cách mong muốn: truyện tranh 2D nét sạch (kiểu ligne claire), người LỚN với tỉ lệ cơ thể người trưởng thành, mặt sạm gió, nghiêm túc; KHÔNG giống trẻ con, KHÔNG hoạt hình tròn trịa.
{ref_note}
Nhân vật dự kiến xuất hiện trong ảnh này ({n_exp} người có tên):
{chars}
Lời kể đang đọc lúc ảnh hiện:
"{text}"

Hãy nhìn kỹ ảnh rồi trả lời JSON đúng dạng:
{{"so_nguoi_thay": <ĐẾM từng khuôn mặt / từng người trong ảnh; nếu nhiều hơn 8 người ở xa thì ghi 9>,
 "tre_con": <true nếu BẤT KỲ người nào có mặt tròn bầu bĩnh má hồng, mắt to, đầu to so với thân, dáng lùn tròn kiểu hoạt hình thiếu nhi, hoặc trông như trẻ em / bé gái / thiếu niên; false CHỈ KHI mọi người đều có tỉ lệ người lớn thật sự và gương mặt từng trải>,
 "lech_nhan_vat": [<các nhân vật có tên bị vẽ lệch rõ so với mô tả (tóc, râu, mũ, áo) hoặc lệch so với bảng mẫu>],
 "giai_phau": [<lỗi cụ thể: thừa/thiếu tay chân ngón, mặt méo, hai người dính nhau, vật mọc ra từ người...>],
 "chu_la": <true nếu có chữ vô nghĩa hoặc sai chính tả đọc được rõ trong ảnh; chữ nhỏ mờ trên tàu bỏ qua>,
 "sai_thoi": [<{era}>],
 "mat_sinh_vat": <true nếu tàu, thuyền, đảo hay đồ vật có mặt / mắt / miệng như hoạt hình>,
 "lac_de": <true nếu ảnh hoàn toàn không liên quan sự việc lời kể nói tới; ảnh bối cảnh chung của sự việc là chấp nhận được>,
 {extra}"diem": <1 đến 5, 5 = dùng ngay, 3 = tạm được, 1-2 = phải vẽ lại>,
 "ghi_chu": "<một câu tiếng Việt: lỗi chính hoặc 'ổn'>"}}
Chỉ báo lỗi thật sự thấy. Không phê bình phong cách. Bỏ qua tỉ lệ khung hình.
"""


def load(ma):
    sf = ROOT / "scripts" / f"{ma}.json"
    sc = json.loads(sf.read_text(encoding="utf-8")) if sf.exists() else {"title": ma, "long": {"chapters": []}}
    anh = {x["key"]: x for x in json.loads((ROOT / "ke-hoach" / "nhan-vat" / f"{ma}_anh.json").read_text(encoding="utf-8"))}
    spec_f = ROOT / "ke-hoach" / "nhan-vat" / f"{ma}v2.json"
    if not spec_f.exists():
        spec_f = ROOT / "ke-hoach" / "nhan-vat" / f"{ma}.json"
    spec = json.loads(spec_f.read_text(encoding="utf-8")) if spec_f.exists() else {}
    beats = {}
    for ch in sc["long"]["chapters"]:
        for b in ch["beats"]:
            if b.get("anh_file"):
                beats[Path(b["anh_file"]).stem] = b
    return sc, anh, spec, beats


def kiem_tra_mot(k, ma, sc, anh, spec, beats, ref):
    item = anh[k]
    b = beats.get(k, {})
    nv = item.get("nv", [])
    desc = spec.get("nhan_vat", {})
    named = [n for n in nv if n in desc and not any(w in desc[n].lower() for w in ("ship", "boat", "tug", "dogs", "shelter"))]
    chars = "\n".join(f"- {desc[n]}" for n in named) or "- (cảnh phong cảnh / tàu / vật, không có nhân vật chính)"
    story = sc.get("title") or ma
    img = ROOT / "assets" / "anh_2d" / ma / f"{k}.jpg"
    from PIL import Image
    small = ROOT / "output" / "_kt2d" / f"{k}.jpg"
    small.parent.mkdir(parents=True, exist_ok=True)
    im = Image.open(img).convert("RGB")
    im.thumbnail((1280, 1280))
    im.save(small, quality=88)
    parts = [{"text": PROMPT.format(story=story, ref_note=("Ảnh ĐẦU TIÊN là bảng nhân vật mẫu; ảnh THỨ HAI là ảnh cần kiểm tra." if ref else "Chỉ có một ảnh cần kiểm tra."),
                                    n_exp=len(named), chars=chars, text=b.get("text") or item.get("text", ""),
                                    era=series(ma)["era"], extra=series(ma)["extra"])}]
    if ref:
        parts.append(review.img_part(ref))
    parts.append(review.img_part(small))
    old = review.STAGE
    review.STAGE = "kiem2d"
    try:
        return review.ask(parts, f"k2d_{ma}_{k}", ROOT / "output" / "_kt2d", review.hashlib.sha1(small.read_bytes()).hexdigest())
    finally:
        review.STAGE = old


def danh_gia(r, n_exp, ma="", vang=False):
    """Trả về (loi_nang, ghi_chu): loi_nang là danh sách lý do bắt buộc vẽ lại."""
    why = []
    if r.get("tre_con"):
        why.append("có người giống trẻ con / hoạt hình")
    if r.get("giai_phau"):
        why.append("giải phẫu: " + "; ".join(map(str, r["giai_phau"]))[:140])
    if r.get("lech_nhan_vat"):
        why.append("lệch nhân vật: " + "; ".join(map(str, r["lech_nhan_vat"]))[:140])
    if r.get("sai_thoi"):
        why.append("sai thời: " + "; ".join(map(str, r["sai_thoi"]))[:100])
    if r.get("mat_sinh_vat"):
        why.append("vật có mặt hoạt hình")
    if r.get("chu_la"):
        why.append("chữ lạ")
    if r.get("lac_de"):
        why.append("lạc đề")
    try:
        if vang and int(r.get("so_nguoi_thay", 0)) > 0:
            why.append(f"có người trong cảnh phải vắng người ({r.get('so_nguoi_thay')} người)")
    except Exception:
        pass
    for fld, ly_do in series(ma).get("cac_loi", {}).items():
        if r.get(fld):
            why.append(ly_do)
    try:
        if n_exp and int(r.get("so_nguoi_thay", n_exp)) != n_exp and n_exp <= 4 and int(r.get("so_nguoi_thay", 0)) > n_exp:
            why.append(f"thừa người ({r.get('so_nguoi_thay')} thay vì {n_exp})")
    except Exception:
        pass
    try:
        if int(r.get("diem", 5)) <= 2:
            why.append(f"điểm {r.get('diem')}/5")
    except Exception:
        pass
    return why


def main():
    ma = sys.argv[1]
    opts = dict(a.split("=", 1) for a in sys.argv[2:] if "=" in a)
    ref = ROOT / opts["ref"] if opts.get("ref") else None
    if ref and not ref.exists():
        print("không thấy bảng mẫu:", ref)
        ref = None
    sc, anh, spec, beats = load(ma)
    only = [x for x in opts.get("only", "").split(",") if x]
    keys = only or sorted(k for k in anh if (ROOT / "assets" / "anh_2d" / ma / f"{k}.jpg").exists())
    res, fail = {}, []
    t0 = time.time()
    for i, k in enumerate(keys):
        try:
            r = kiem_tra_mot(k, ma, sc, anh, spec, beats, ref)
        except Exception as e:
            fail.append(k)
            print(f"{k}: không kiểm tra được ({str(e)[:120]})", flush=True)
            continue
        named = [n for n in anh[k].get("nv", []) if n in spec.get("nhan_vat", {})
                 and not any(w in spec["nhan_vat"][n].lower() for w in ("ship", "boat", "tug", "dogs", "shelter"))]
        r["_ly_do"] = danh_gia(r, len(named), ma, anh[k].get("so_nguoi") == 0)
        res[k] = r
        print(f"{k}: điểm {r.get('diem')} · {'; '.join(r['_ly_do']) or 'ổn'} · {r.get('ghi_chu', '')[:80]}", flush=True)
        if (i + 1) % 25 == 0:
            print(f"… {i + 1}/{len(keys)} ({time.time() - t0:.0f} giây)", flush=True)
    out = ROOT / "logs" / "kiem_2d"
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{ma}.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    redo = [k for k, r in res.items() if r["_ly_do"]]
    lines = [f"GEMINI XEM ẢNH 2D · {ma} · {len(res)}/{len(keys)} ảnh đã kiểm tra",
             f"Nên vẽ lại ({len(redo)}): {','.join(redo)}", f"Không kiểm tra được ({len(fail)}): {','.join(fail)}", ""]
    for k, r in res.items():
        lines.append(f"{k} · điểm {r.get('diem')} · {'; '.join(r['_ly_do']) or 'ổn'} · {r.get('ghi_chu', '')}")
    (out / f"{ma}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(lines[0], lines[1], lines[2], sep="\n")


if __name__ == "__main__":
    main()
