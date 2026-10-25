"""LH5O: 16 ảnh 2D cho ~35 giây mở đầu video Lê Hoàn bản điều tra (lh5, khung ngang 1344x768), mỗi ảnh ~2 giây.
Khóa ảnh = số thứ tự cảnh 001..016. Lời kể 16001–16005 (ke-hoach/thu-giong-hai/lh5_full.json).
Quy tắc: không chữ, không máu, nhân vật chính (Lê Hoàn) nghiêm trang; hài chỉ nhắm vào tình huống/phía nhà Tống; vật đúng thời (thế kỷ 10), không vật hiện đại."""
import json
from pathlib import Path
R = Path(__file__).resolve().parent
NV = {
 "lehoan": "Le Hoan, a broad-shouldered Vietnamese warlord-king of about 49 with a square weathered face, thick straight eyebrows, a short dark beard, hair tied up under a plain dark headcloth, wearing a dark-brown crossed-collar tunic with a plain sash, firm calm dignified look, empty hands, no weapon",
 "tong_a": "a Song dynasty envoy, a thin man of about 45 with a long thin moustache and narrow face, wearing a green round-collared robe with a wide belt and a black official hat with two straight flat wings",
 "tong_b": "a second Song envoy, a plump man of about 55 with a round face, a short grey beard and kind tired eyes, wearing a red round-collared robe with a wide belt and a black official hat with two straight flat wings",
 "tong_quan": "a proud Song official of about 50, lean, with a pointed chin beard and a smug raised chin, wearing a purple round-collared robe with a wide belt and a black official hat with two straight flat wings",
 "tong_de": "the Song emperor on a grand throne, a middle-aged man in a yellow robe and a flat-topped crown with hanging bead strings, calm and remote",
}
STYLE = ("2D flat cartoon illustration, bold clean dark outlines, flat saturated earthy colours with simple cel shading, expressive readable faces, stylised ADULT proportions (about six heads tall, never chibi, never a child), "
         "dramatic cinematic composition with a detailed background, single full-frame picture, no panels, no border")
SUF = ("10th century Vietnam and Song dynasty China: timber and thatch or grey-tiled halls, dirt roads, lattice windows without glass, low benches and straw mats, "
       "no chairs with backs, no candles, no paper books, no modern objects, no blood, no text, no letters, no watermark, no signs")
S = {}
def sc(i, nv, m, cau): S[i] = (nv, m, cau)
sc(1, ["tong_a"], "a Song envoy gallops on a brown horse along a misty mountain road at dawn toward a Vietnamese timber fortress gate in the distance, a yellow silk scroll case slung across his back, dust trail behind, plain banners on the gate", 16001)
sc(2, ["lehoan", "tong_a", "tong_b"], "in the courtyard of a timber hall Le Hoan stands tall and upright with chin raised and hands hidden in his sleeves, refusing to bow, while the two Song envoys in front hold out a rolled yellow silk scroll with stunned faces, a few Vietnamese guards with spears upright stand behind, exactly three main figures with three different faces", 16001)
sc(3, ["lehoan"], "exactly ONE man only: Le Hoan sits composed on a low wooden bench in a timber hall, one foot thickly wrapped in cloth bandage and resting on a small stool, a calm unreadable face, no second figure", 16002)
sc(4, [], "a saddled brown horse stands alone on a dirt road in front of a timber fortress gate, reins hanging loose, dust settling, soft morning light, completely empty, absolutely no people", 16002)
sc(5, ["tong_a", "tong_b"], "close shot of the two Song envoys side by side nodding with worried sympathetic faces, looking toward the left, timber hall behind them, exactly two men with clearly different faces", 16002)
sc(6, ["lehoan"], "exactly ONE man only: close side view of Le Hoan glancing sideways with a calm unreadable face, half of his face in shadow, dim timber hall, no second figure", 16002)
sc(7, [], "huge Song dynasty capital city with towering grey walls, many-tiered pagoda towers and endless ranks of tiny soldiers with plain red banners marching along a wide avenue, grand and overwhelming scale, seen from above", 16003)
sc(8, ["tong_de"], "the Song emperor sits tiny on a grand throne at the far end of a vast hall, rows of kneeling officials in red and green robes in the foreground, great scale, golden light, exactly one emperor", 16003)
sc(9, ["tong_a"], "exactly ONE man only: the thin Song envoy stands alone in a timber hall with a puzzled look, one eyebrow raised and a hand at his chin, as if something does not add up, no second figure", 16003)
sc(10, ["lehoan"], "exactly ONE man only: Le Hoan stands on the steps of his timber hall at dawn with hands hidden in his sleeves, strong and dignified, green hills behind and a few banners of a single plain solid colour with no star, no emblem and no symbol, no second figure", 16004)
sc(11, ["tong_quan", "tong_de"], "in a grand Song hall the proud Song official in purple stands before the emperor's low dais with chin raised and one arm sweeping confidently over a large map spread on a low table, other officials listening behind him, the emperor small in the background", 16004)
sc(12, ["tong_quan"], "exactly ONE man only: close shot of the proud Song official in purple smiling smugly with eyes half closed and chin raised, grand hall behind, no second figure", 16004)
sc(13, [], "a bamboo quiver full of arrows and a bow hang unused on a timber wall, a single sunbeam through a lattice window, dust in the air, completely empty, absolutely no people", 16004)
sc(14, [], "three rolled scrolls made of narrow bamboo slips (flat wooden strips strung together with cord, clearly NOT paper) lie in a row on a low dark wooden table, warm dawn light through a lattice window, a feeling of mystery and clues, completely empty, absolutely no people", 16005)
sc(15, ["lehoan"], "exactly ONE man only: Le Hoan looks straight ahead with a determined face, dawn light glowing behind his head, strong and dignified, no second figure", 16005)
sc(16, [], "wide dawn landscape of limestone hills and a rice plain with a distant timber citadel and a winding river, mist, soft golden light, completely empty, absolutely no people", 16005)
lh = {x["n"]: x["text"] for x in json.loads((R.parent / "thu-giong-hai" / "lh5_full.json").read_text(encoding="utf-8"))}
anh, canh = [], []
for i in sorted(S):
    nv, m, cau = S[i]
    chars = "; ".join(NV[n] for n in nv)
    p = f"{m}. Characters (keep exactly this look): {chars}. {STYLE}. {SUF}." if nv else f"{m}. {STYLE}. {SUF}."
    k = f"{i:03d}"
    anh.append({"key": k, "cau": cau, "nv": nv, "text": lh[cau], "prompt": p, "w": 1344, "h": 768})
    canh.append({"key": k, "nv": nv, "mo_ta": m[:80]})
(R / "LH5O_anh.json").write_text(json.dumps(anh, ensure_ascii=False, indent=1), encoding="utf-8")
(R / "LH5O.json").write_text(json.dumps({"ma": "LH5O", "ghi_chu": "16 ảnh mở đầu lh5, khung ngang", "nhan_vat": NV, "canh": canh}, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(anh), max(len(a["prompt"]) for a in anh))
