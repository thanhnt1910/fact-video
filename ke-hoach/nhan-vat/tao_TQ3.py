"""Tạo scripts/TQ3.json (video dài + ngắn) cho Tam Quốc tập 3 từ ke-hoach/tam-quoc-tap-3-kich-ban.md (bản chủ kênh đã duyệt).
Mỗi lời kể một ảnh (ảnh = câu − 1 từ câu 4 trở đi; câu 2 và 3 gộp thành một lời kể dùng ảnh 002). Tên chương lấy từ file md."""
import json, re
from pathlib import Path
R = Path(__file__).resolve().parent
ROOT = R.parents[1]
md = (ROOT / "ke-hoach" / "tam-quoc-tap-3-kich-ban.md").read_text(encoding="utf-8")
sec = md[md.index("## KỊCH BẢN VIDEO DÀI"):md.index("## KỊCH BẢN VIDEO NGẮN")]

def clean(t):
    t = re.sub(r"\s*\[[^\]]*\]", "", t)
    t = re.sub(r"\s*\(Lữ Bố truyện[^)]*\)", "", t)
    return t.strip()

chapters, cur, title = [], None, None
beats_txt = {}
for line in sec.split("\n"):
    m = re.match(r"^(MỞ ĐẦU|CHƯƠNG \d+: (.+)|LỜI KẾT)\s*$", line.strip())
    if m:
        title = m.group(2) or None
        if line.strip().startswith("MỞ ĐẦU"):
            title = None
        cur = {"title": title, "nums": []}
        if line.strip() == "CHƯƠNG 9: Lời kết":
            cur["title"] = "Lời kết"
        chapters.append(cur)
        continue
    m = re.match(r"^(\d+)\. (.+)$", line)
    if m and cur is not None:
        n = int(m.group(1)); beats_txt[n] = clean(m.group(2)); cur["nums"].append(n)
assert len(beats_txt) == 86, len(beats_txt)

def key(n):          # số câu -> số ảnh
    return "%03d" % (2 if n == 3 else (n if n <= 2 else n - 1))
def img(k): return f"assets/anh_2d/TQ3/{k}.jpg"
AI = "ancient Han China scene, 2D ligne claire"

out_ch = []
for ch in chapters:
    beats = []
    for n in ch["nums"]:
        if n == 3:
            continue
        text = beats_txt[n] + (" " + beats_txt[3] if n == 2 else "")
        beats.append({"text": text, "ai": AI, "anh_file": img(key(n))})
    c = {"beats": beats}
    if ch["title"]:
        c["title"] = ch["title"]
    out_ch.append(c)
used = [b["anh_file"] for c in out_ch for b in c["beats"]]
assert len(used) == len(set(used)) == 85
words = sum(len(b["text"].split()) for c in out_ch for b in c["beats"])
print(f"dài: {len(used)} cảnh, {words} chữ, ước tính {words*0.343/60:.1f} phút (chưa tính thẻ chương)")

NGAN = [
 ("hook", 1, ("001", "002")),
 ("boi_canh", 2, ("037", "026")),
 ("boi_canh", 3, ("033", "036")),
 ("leo_thang", 4, ("043", "044")),
 ("leo_thang", 5, ("046", "048")),
 ("leo_thang", 6, ("064", "080")),
 ("cu_lat", 7, ("075", "076")),
 ("cu_lat", 8, ("084", "063")),
 ("vong_lap", 9, ("085", "082")),
]
ngan_txt = {}
sec2 = md[md.index("## KỊCH BẢN VIDEO NGẮN"):md.index("## GỢI Ý ẢNH BÌA")]
for m in re.finditer(r"^(\d+)\. (.+)$", sec2, re.M):
    ngan_txt[int(m.group(1))] = clean(m.group(2))
assert len(ngan_txt) == 9
ngan_beats = [{"loai_canh": lc, "text": ngan_txt[i], "images": [{"anh_file": img(a)}, {"anh_file": img(b)}]} for lc, i, (a, b) in NGAN]
allk = [k for _, _, p in NGAN for k in p]
assert len(allk) == len(set(allk))

TITLE = "Ai thật sự chém Hoa Hùng? Hổ Lao có thật không?"
CAP = "Trong tiểu thuyết, Quan Vũ hâm rượu chém Hoa Hùng. Nhưng Tam quốc chí chép người chém ông ta là Tôn Kiên. Tam Quốc theo chính sử, tập 3 🏯"
GIONG = json.loads((ROOT / "scripts" / "TQ1.json").read_text(encoding="utf-8"))["giong_them"]
BIA = {"anh": img("018"), "nen": img("016"), "huy_hieu": "TAM QUỐC CHÍNH SỬ · TẬP 3", "dong1": "KHÔNG PHẢI", "dong2": "QUAN VŨ", "gach": True,
       "dong3": "Ai thật sự <b>chém</b> <b>Hoa Hùng</b>?"}
script = {
 "id": "TQ3", "topic": "lich-su",
 "title": TITLE, "caption": CAP,
 "hashtags": ["nguoigacsu", "tamquoc", "tonkien", "lichsu", "hoahung", "chinhsu"],
 "sources": [
  "Trần Thọ, Tam quốc chí: Ngô thư, Tôn Phá Lỗ truyện (quyển 46) kèm chú giải Bùi Tùng Chi (Anh hùng ký, Ngô thư, Giang biểu truyện, Ngô lục); Ngụy thư, Đổng Trác truyện (quyển 6), Viên Thiệu truyện, Lữ Bố truyện (quyển 7), qua Wikisource (chữ Hán)",
  "Hậu Hán thư, Tư trị thông giám và tổng hợp Wikipedia (liên quân tan rã, việc Hồ Chẩn rối loạn, Hổ Lao) — chưa đối chiếu nguyên văn; Quan Vũ truyện, Trương Phi truyện chưa đối chiếu được nguyên văn",
 ],
 "nguon_link": [
  {"ten": "Tam quốc chí, Tôn Phá Lỗ truyện, Wikisource", "url": "https://zh.wikisource.org/wiki/三國志/卷46", "ngon_ngu": "chữ Hán"},
  {"ten": "Tam quốc chí, Đổng Trác truyện (Tứ khố toàn thư), Wikisource", "url": "https://zh.wikisource.org/wiki/三國志_(四庫全書本)/魏志/卷06", "ngon_ngu": "chữ Hán"},
  {"ten": "Tam quốc chí, Lữ Bố truyện, Wikisource", "url": "https://zh.wikisource.org/wiki/三國志/卷07", "ngon_ngu": "chữ Hán"},
 ],
 "music": "none", "giong_them": GIONG, "pronounce": {},
 "long": {
  "chuyen_canh": "fade",
  "title": TITLE + " | Tam Quốc theo chính sử, tập 3",
  "title_card": "Tam Quốc chính sử: Ai chém **Hoa Hùng**?",
  "thumb_title": "Ai chém **Hoa Hùng**?", "badge": "Tam Quốc chính sử",
  "description": "Trong tiểu thuyết, Quan Vũ hâm rượu chém Hoa Hùng và ba anh em đánh Lữ Bố ở Hổ Lao. Tam quốc chí chép khác: Tôn Kiên đánh tan quân Đổng Trác ở Dương Nhân và chém Hoa Hùng. Tập 3 của series Tam Quốc theo chính sử kể về Tôn Kiên, Lữ Bố, cuộc đốt Lạc Dương và cái chết của Đổng Trác.",
  "voice": "Sadaltager", "music": "none", "bia": BIA, "chapters": out_ch,
 },
 "binh_luan": {
  "dai": {"ghim": "Tập này đặt sử bên cạnh tiểu thuyết: công chém Hoa Hùng, Tam quốc chí chép là của Tôn Kiên, còn tiểu thuyết trao cho Quan Vũ. Một số chi tiết về Lữ Bố, liên quân tan rã và Lưu Ngu lấy từ tổng hợp thứ cấp; hình ảnh là tranh minh họa.", "phu": []},
  "ngan": {"ghim": "Về người chém Hoa Hùng: Tam quốc chí chép Tôn Kiên chém đô đốc Hoa Hùng ở Dương Nhân; tiểu thuyết trao công ấy cho Quan Vũ 🏯", "phu": []},
 },
 "ngan": {
  "hook_text": "Chém Hoa Hùng là Tôn Kiên\n**không phải Quan Vũ**",
  "hooks": ["Trong tiểu thuyết, Quan Vũ hâm rượu chém Hoa Hùng. Nhưng sử chép là một người khác."],
  "caption": CAP, "beats": ngan_beats, "bia": BIA, "anh_bia": img("018"),
 },
}
script["scenes"] = [{"type": "hook" if i == 0 else "text", "text": b["text"], "voice": b["text"]} for i, b in enumerate(ngan_beats)]
(ROOT / "scripts" / "TQ3.json").write_text(json.dumps(script, ensure_ascii=False, indent=1), encoding="utf-8")
print("ok scripts/TQ3.json")
