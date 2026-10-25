"""LH5Q: 16 ảnh 2D cho ~35 giây mở đầu video Lê Hoàn bản điều tra (lh5, khung ngang 1344x768), mỗi ảnh ~2 giây.
Khóa ảnh = số thứ tự cảnh 001..016. Lời kể 16001–16005 (ke-hoach/thu-giong-hai/lh5_full.json).
Quy tắc: không chữ, không máu, nhân vật chính (Lê Hoàn) nghiêm trang; hài chỉ nhắm vào tình huống/phía nhà Tống; vật đúng thời (thế kỷ 10), không vật hiện đại."""
import json
from pathlib import Path
R = Path(__file__).resolve().parent
NV = {
 "lehoan": "Le Hoan, a broad-shouldered Vietnamese man of about 49 with a square weathered friendly face, thick straight eyebrows, a short dark beard, hair tied up under a plain dark headcloth, wearing a dark-brown crossed-collar tunic with a plain sash, firm calm dignified look, empty hands, no weapon",
 "lehoan_tre": "young Le Hoan at about 22, a sturdy young man with the same square face and thick straight eyebrows, no beard, hair tied up under a plain dark headcloth, plain brown tunic, honest determined look",
 "lehoan_be": "Le Hoan as a thin poor orphan boy of about eight with the same thick straight eyebrows, short messy dark hair, a worn patched brown tunic, bare feet, big sad hopeful eyes",
 "quan_ho_le": "a kind middle-aged village official with a gentle smile and a short grey beard, wearing a simple faded blue-grey crossed-collar robe and a plain cloth hat",
 "tong_a": "a Song dynasty envoy, a thin man of about 45 with a long thin moustache and narrow face, wearing a green round-collared robe with a wide belt and a black official hat with two straight flat wings",
 "tong_b": "a second Song envoy, a plump man of about 55 with a round face, a short grey beard and kind tired eyes, wearing a red round-collared robe with a wide belt and a black official hat with two straight flat wings",
 "tong_quan": "a proud Song official of about 50, lean, with a pointed chin beard and a smug raised chin, wearing a purple round-collared robe with a wide belt and a black official hat with two straight flat wings",
 "tong_de": "the Song emperor on a grand throne, a middle-aged man in a yellow robe and a flat-topped crown with hanging bead strings, calm and remote",
 "dinh_lien": "Dinh Lien, a handsome young prince of about 20 in a rich dark-red robe with a golden sash and a small crown, confident friendly look",
 "dinh_vuong": "King Dinh Tien Hoang, a stern dignified man of about 55 with a full dark beard, wearing a golden-yellow robe and a tall ornate crown, powerful presence",
 "dinh_toan": "little Dinh Toan, a six-year-old boy king in an oversized golden robe and a crown too big for his head, tiny, wide bewildered eyes",
}
STYLE = ("bright cheerful 2D cartoon illustration in the style of a popular educational history animation: thick clean dark outlines, vivid saturated colours, warm sunny daylight, "
         "rounded friendly faces with large expressive eyes and clear emotions, slightly simplified shapes, soft cel shading, lively eye-catching composition, "
         "background full of small active details, characters about five heads tall (strong and dignified, never a baby), single full-frame picture, no panels, no border")
SUF = ("10th century Vietnam and Song dynasty China: timber and thatch or grey-tiled halls, dirt roads, lattice windows without glass, low benches and straw mats, "
       "no chairs with backs, no candles, no paper books, no modern objects, no blood, no text, no letters, no watermark, no signs")
S = {}
def sc(i, nv, m, cau): S[i] = (nv, m, cau)
sc(1, ["tong_a"], "dramatic low angle: a Song envoy gallops on a brown horse along a mountain road toward a Vietnamese timber fortress gate on a hill, a yellow silk scroll case slung on his back, dust cloud and flying leaves, plain banners of one solid colour", 16001)
sc(2, ["lehoan", "tong_a", "tong_b"], "Le Hoan stands tall with chin raised in a sunny courtyard while a long row of Vietnamese officials behind him bow deeply, only Le Hoan upright, the two Song envoys hold out a rolled yellow silk scroll with stunned faces", 16001)
sc(3, ["lehoan"], "comic close-up: a huge cloth-bandaged foot fills the lower foreground, behind it Le Hoan sits calm on a low bench with a composed face, exactly ONE man, warm sunlight, sparkles around the bandage", 16002)
sc(4, [], "a saddled brown horse stands alone on a dirt road, reins hanging, a dropped dark headcloth lies on the ground beside it, little puff of dust, morning light, completely empty, absolutely no people", 16002)
sc(5, ["tong_a", "tong_b"], "the two Song envoys put their hands on their hearts with worried sympathetic faces, nodding, small sparkles above their heads, bright timber hall, exactly two men with clearly different faces", 16002)
sc(6, [], "huge Song dynasty capital city seen from above with towering grey walls, golden pagoda towers and endless ranks of tiny soldiers with plain red banners marching along a wide avenue, grand and overwhelming scale", 16003)
sc(7, ["tong_a", "tong_b"], "a giant golden question mark floats above the heads of the two Song envoys who look up at it puzzled, bright sunny courtyard, cartoon humour, exactly two men", 16003)
sc(8, ["tong_a"], "exactly ONE man only: the thin Song envoy scratches his chin with a puzzled look, a thought bubble above him shows a tiny horse, bright timber hall, no second figure", 16003)
sc(9, ["lehoan"], "heroic low-angle view: exactly ONE man only, Le Hoan stands on the steps of his hall at sunrise with golden light behind him, strong and dignified, hands hidden in sleeves", 16004)
sc(10, ["lehoan"], "exactly ONE man only: close portrait of Le Hoan with a calm knowing half-smile and one eyebrow slightly raised, warm light, sparkles in the air", 16004)
sc(11, ["tong_quan", "tong_de"], "in a grand bright Song hall the proud Song official in purple points confidently at a large map on a low table with a sweeping arm, officials listening behind him, the emperor small in the background", 16004)
sc(12, ["tong_quan"], "exactly ONE man only: the proud Song official in purple laughs smugly with his chin raised, beside him a quiver full of untouched arrows leans against a pillar, bright grand hall", 16004)
sc(13, ["lehoan"], "exactly ONE man only: Le Hoan stands at a low table pointing with one finger at three scrolls that glow softly, curious detective mood, warm lamp-like glow, bright timber hall", 16005)
sc(14, [], "three rolled scrolls made of narrow bamboo slips strung with cord stand in a row on a dark table, each with a floating glowing golden orb above it, the third one glows the brightest, sparkles, completely empty, absolutely no people", 16005)
sc(15, [], "extreme close-up of a bamboo-slip scroll glowing with golden light and rays, tied with cord, magical mystery mood, sparkles, completely empty, absolutely no people", 16005)
sc(16, [], "wide sunny landscape of limestone hills and a rice plain with a winding path leading to a distant timber citadel, birds in the sky, the start of a journey, completely empty, absolutely no people", 16005)
sc(17, [], "night view of a silent timber palace under a huge full moon, all windows dark, a long empty throne seen through the open doors, deep blue colours with silver moonlight, solemn mood, completely empty, absolutely no people", 16006)
sc(18, [], "close view of an empty carved royal throne in a dark hall with a single small clay oil dish flame beside it, a black cloth draped over the throne arm, solemn blue and gold tones, no people, no blood", 16006)
sc(19, [], "two palace guards stand with bowed heads and spears upright on the steps of a timber hall at night in light rain, lanterns of bronze dishes with tiny flames, sombre but gentle mood, seen from behind, plain banners, no blood", 16006)
sc(20, ["dinh_toan"], "a tiny six-year-old boy king sits on a huge golden throne with his feet dangling far above the floor, wearing an oversized crown, looking up bewildered, rows of ministers behind him, exactly one child", 16007)
sc(21, ["lehoan", "dinh_toan"], "Le Hoan stands protectively right behind the boy king's throne with a steady dignified look, the boy looks small in front of him, golden light from a window, exactly two main figures", 16007)
sc(22, ["lehoan", "dinh_toan"], "the boy king looks up trustfully at Le Hoan who stands beside him and looks ahead with a firm calm face, a bright palace courtyard with banners of one solid colour", 16007)
sc(23, ["lehoan_be"], "exactly ONE child: a thin poor orphan boy sits alone on a mud bank at the edge of a rice field at dusk holding an empty wooden bowl, villagers tiny in the far distance, warm orange sky", 16008)
sc(24, ["lehoan_be", "quan_ho_le"], "the kind village official holds the orphan boy's hand and leads him along a village path toward a thatched house, warm golden evening light, both smiling gently", 16008)
sc(25, ["lehoan_be"], "exactly ONE child: the orphan boy carries two small water buckets on a shoulder pole across a sunny village yard, working hard but smiling, chickens and a buffalo in the background", 16008)
sc(26, ["lehoan_be"], "exactly ONE child: the boy swings a long bamboo stick like a sword in a sunrise yard, determined face, dust and leaves flying around him", 16008)
sc(27, ["lehoan_tre", "dinh_lien"], "in a bright palace courtyard young Le Hoan bows respectfully to the young prince Dinh Lien who greets him with a friendly nod, banners of one solid colour, timber hall behind them", 16009)
sc(28, ["dinh_vuong", "lehoan_tre"], "King Dinh Tien Hoang on his throne nods approvingly toward young Le Hoan who stands before him, a golden glow of sparkles around Le Hoan, courtiers watching, bright grand hall", 16009)
sc(29, ["lehoan_tre"], "seen from behind: young Le Hoan walks at the head of a long column of a thousand soldiers with spears upright and plain banners across a sunny plain, dust and distant hills", 16009)
sc(30, [], "bird's-eye view of a large army camp where ranks of tiny soldiers train in neat square formations on a sunny field, plain banners, thatched tents, hills in the background", 16009)
lh = {x["n"]: x["text"] for x in json.loads((R.parent / "thu-giong-hai" / "lh5_full.json").read_text(encoding="utf-8"))}
anh, canh = [], []
for i in sorted(S):
    nv, m, cau = S[i]
    chars = "; ".join(NV[n] for n in nv)
    p = f"{m}. Characters (keep exactly this look): {chars}. {STYLE}. {SUF}." if nv else f"{m}. {STYLE}. {SUF}."
    k = f"{i:03d}"
    anh.append({"key": k, "cau": cau, "nv": nv, "text": lh[cau], "prompt": p, "w": 1344, "h": 768})
    canh.append({"key": k, "nv": nv, "mo_ta": m[:80]})
(R / "LH5Q_anh.json").write_text(json.dumps(anh, ensure_ascii=False, indent=1), encoding="utf-8")
(R / "LH5Q.json").write_text(json.dumps({"ma": "LH5Q", "ghi_chu": "thử phong cách sáng, dễ thương (mẫu video giáo dục), 16 cảnh mở đầu lh5", "nhan_vat": NV, "canh": canh}, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(anh), max(len(a["prompt"]) for a in anh))
