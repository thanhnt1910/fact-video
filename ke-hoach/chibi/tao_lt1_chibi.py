"""Tạo prompt ảnh chibi cho video Lý Thường Kiệt (mã lt1) từ kịch bản ke-hoach/ly-thuong-kiet-kich-ban.md.

  python ke-hoach/chibi/tao_lt1_chibi.py     -> ghi ke-hoach/chibi/lt1_chibi.json

Mỗi đoạn có cảnh "chibi (LoRA x,x): ..." trong kịch bản được ghép một prompt tiếng Anh:
  câu mở đầu + cảnh (có mô tả riêng từng nhân vật) + bối cảnh thời + hậu tố.
Quy tắc ảnh (CLAUDE.md, quy-tac/tam-quoc.md): không chữ, không máu, đúng thời, mỗi người một mặt riêng, một ảnh mỗi đoạn.
FLUX schnell chỉ đọc tối đa 256 token: prompt được kiểm độ dài, dài quá thì báo.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MD = ROOT / "ke-hoach" / "ly-thuong-kiet-kich-ban.md"
OUT = ROOT / "ke-hoach" / "chibi" / "lt1_chibi.json"

OPEN_VN = "Realistic historical illustration with natural human proportions and a detailed painterly look, set in ancient Vietnam, Dai Viet under the Ly dynasty, 11th century"
OPEN_SONG = "Realistic historical illustration with natural human proportions and a detailed painterly look, set in Song dynasty China, 11th century"
OPEN = OPEN_VN

# Mô tả cố định từng nhân vật (khớp bảng "Bảng nhân vật chibi" trong kịch bản). Chỉ mô tả hình dáng, không dùng tên riêng.
CH = {
    "LTK-T": "a slim handsome young palace attendant with a smooth beardless face, black topknot, plain black wrapped cloth turban and a dark blue crossed-collar narrow-sleeved tunic",
    "LTK-G": "a dignified middle-aged general with a short neat black beard, calm serious face, deep crimson crossed-collar narrow-sleeved tunic over dark armor",
    "LTK-L": "a dignified elderly man with a white beard and thin white hair, calm eyes, deep crimson crossed-collar narrow-sleeved tunic",
    "TT": "an elderly king with a grey beard, golden yellow crossed-collar narrow-sleeved tunic and a small gold diadem",
    "TTG": "a strong middle-aged king with a thin black mustache, golden yellow narrow-sleeved dragon tunic and a gold diadem with small ornaments",
    "NT": "a tiny seven-year-old boy king with a round face, an oversized golden crossed-collar narrow-sleeved tunic and a small gold diadem",
    "YL": "a graceful woman with her hair in a high bun with one jade pin and a pale green crossed-collar silk tunic and long skirt",
    "DTH": "a stern older woman with a grey-streaked bun and a plum purple crossed-collar narrow-sleeved tunic",
    "LDT": "an elderly scholar-official with a long white beard, indigo crossed-collar narrow-sleeved tunic and a black wrapped cloth turban",
    "CC": "a Champa king with a thin mustache, a tall tiered golden crown and orange and white wrapped garments",
    "TD": "a broad-shouldered general with a thick black beard, olive brown armor and a helmet with a short red plume",
    "TG": "a middle-aged Song official with a thin grey beard, a dark teal wide-sleeved official robe and a black two-winged official hat",
    "VAT": "a Song chancellor with a long thin face, thin grey beard, purple official robe and a black two-winged official hat",
    "TK": "a tall thin clean-shaven Song official in a brown robe and black official hat",
    "LD": "a short stout Song official with a round black beard, green robe and black official hat",
    "TTT": "a heavy-built Song general with a black beard, red-brown armor and a helmet with a long red tassel",
    "QQ": "a big strong Song commander with a white-streaked beard, dark steel armor and a tall helmet",
    "TT2": "a younger Song general with a thin mustache, black armor and a plain helmet",
    "DTN": "a Vietnamese envoy with a goatee, mid-brown crossed-collar narrow-sleeved tunic and a round woven hat",
    "LVT": "a scholar-official with a small mustache, blue-grey crossed-collar narrow-sleeved tunic and a black wrapped cloth turban",
    "LG": "a rough sturdy man in plain brown peasant clothes and a headband, no armor",
    "LTH": "a younger man with a smooth face and a light mustache in a dark green crossed-collar narrow-sleeved tunic",
    "SK": "a middle-aged Song emperor with a thin mustache, a dark gold robe and a flat-topped crown with hanging beads",
}

# Cảnh tiếng Anh theo số đoạn. {MÃ} được thay bằng mô tả nhân vật ở trên.
E = {
    19002: "wide view of the tall grey stone walls of a Song city with plain dark blue flags; at the foot of the wall rows of Vietnamese soldiers in brown tunics with plain red flags carry earth sacks and pile them into a growing slope, soldiers seen from far away or from behind with simple faces",
    19003: "two lands side by side: on the left small green hills with a thatched village and a plain red flag, on the right a huge multi-tier walled fortress with a plain dark blue flag, wind blowing the flags, one small guard on each side with different faces",
    19004: "{LTK-G} stands alone on the wall of a hilltop citadel looking north, wind blowing his sleeves, exactly ONE character only, no second figure",
    19007: "palace courtyard, {LTK-T} stands attending beside {TT} who sits on a low throne, two people only, wooden palace hall",
    19008: "{LTK-T}, now a little older and taller, in a darker blue belted robe and a taller black cap, climbs the stone steps of a palace, exactly ONE character only",
    19009: "{LTK-T} holding a long staff with plain tassels rides a horse out of a city gate, two different guards riding behind him",
    19010: "{LTK-T} with two attendants, one thin with a long beard and one short and round without a beard, walks through a village, villagers stand on both sides of the road welcoming them, thatched houses and rice fields",
    19014: "a column of Vietnamese soldiers marching south seen from behind and far away, plain red flags flying, mountains and a dirt road",
    19015: "{LTK-G} rides a horse at the head of an army, his sword in its scabbard at his waist, soldiers behind him small and far away",
    19016: "inside a tent, {TTG} stands looking at a map spread on a table (drawn lines only, no writing), outside a few soldiers rest beside the tent",
    19017: "in a palace courtyard, {YL} hands out rice to villagers who kneel with palms together in thanks, baskets of rice",
    19018: "{TTG} stands in front of his army looking south with a determined face, soldiers behind him seen from behind",
    19019: "two armies meet in a field, dust clouds rising, on the left a plain red flag, on the right a plain orange flag, soldiers far away with simple faces, everyone standing",
    19020: "courtyard of an ancestral temple, a row of four prisoners with bowed heads, the front one {CC}, no heavy chains, {TTG} stands on the temple steps",
    19022: "inside a palace hall, {LTK-G} kneels to receive an honor from {TTG}, two court officials of different ages and beards stand on either side",
    19023: "a funeral procession of people in plain white hemp robes carrying a wooden bier on two poles through an ancient Vietnamese palace courtyard with tiled roofs, seen from far away, faces not visible, no vehicles",
    19024: "a golden throne with {NT} sitting tiny on it, behind a hanging curtain the dark shadows of two women, an elderly scholar-official with a long white beard stands beside the throne, three people visible",
    19025: "court officials in three groups wearing three different colours (blue, brown, green) stand around a small throne where {NT} sits in the middle, each official a different age and beard",
    19028: "{LTK-G} kneels on one knee receiving a seal from a ceremonial official, palace hall with dark wooden pillars",
    19029: "Song court: the Song emperor ({SK}) sits on a throne, {VAT} stands holding a plain blank scroll",
    19030: "close view of two people, {VAT} bows and whispers to the Song emperor ({SK}) who tilts his head to listen, a folding screen behind",
    19031: "{VAT} points at a map on a table (drawn lines only, no writing), the Song emperor ({SK}) stands beside him watching",
    19033: "in front of the gate of a Song city with plain dark blue flags, {TK} and {LD} stand receiving orders",
    19034: "a riverside shipyard, workers building a wooden ship hull, far away Song soldiers drilling in a row, seen from far with simple faces",
    19036: "a Vietnamese envoy unrolls a blank paper scroll in front of ranks of soldiers with plain red flags, the soldiers seen from behind",
    19037: "beside a green rice field a Song farmer receives a small bag of coins from a clerk holding a blank scroll, the two men of different ages and clothes",
    19038: "two armies set out: on the left wooden war boats with woven sails going down a river, on the right a column of foot soldiers on a road, plain red flags, seen from above, small soldiers with simple faces",
    19040: "wooden war boats with woven sails land on the shore of a coastal town, on the shore a line of ordinary villagers being led away, seen from far and from behind, calm",
    19042: "{TTT} riding a horse leading Song soldiers to rescue a city, soldiers behind him small and far away",
    19043: "a mountain pass between two steep cliffs, on the left soldiers with plain red flags hiding behind rocks, on the right soldiers with plain blue flags marching in, dust clouds, a tense silent standoff",
    19044: "{TD} stands in front of countless tents of an army camp set around a distant walled city, plain red flags",
    19045: "{TG} alone stands on a city wall, both hands on the parapet, looking down with a resolute face, exactly ONE character only",
    19046: "a tall city wall, at its foot more and more tents pitched, in the sky the sun and moon follow one another in a band showing days passing, no text, no calendar",
    19047: "sacks of earth piled into a gentle ramp against the foot of a city wall, a few soldiers carrying sacks, seen from far, simple faces",
    19048: "gate of a walled city with black smoke rising from inside, grey-orange sky, completely empty, absolutely no people",
    19051: "an empty road in front of a city, an overturned cart, smoke curling in the distance, a reddish sky, completely empty, absolutely no people",
    19052: "a long line of ordinary people walking south on a road at dusk, seen from behind, a few escort soldiers far away, no faces, calm",
    19053: "the family of a Song official (an old woman in white and two small children of different ages) receive a reward from a Song official in front of a grey tiled house",
    19054: "inside a palace hall, two Song generals {QQ} and {TT2} kneel receiving orders before the Song emperor ({SK})",
    19055: "nine Song general flags of nine different plain colours lined up on a training ground, flags blank, a few small general figures far away",
    19057: "Song army marching down onto a plain, seen from far away and behind, plain dark blue flags, road dust",
    19060: "a tall bamboo palisade built along the bank of a river, grassy banks on both sides, completely empty, no people",
    19061: "Song soldiers standing on the north bank looking across the river, seen from behind, plain blue flags",
    19062: "Song soldiers reach the river bank and halt in front of a bamboo palisade, raising shields, a few stepping back, everyone standing",
    19063: "a small temple by a river at night, tiled roof, a dim lamp glowing, a sky full of stars, completely empty, no people",
    19064: "a starry night sky over a river, soft ribbons of light like brush strokes floating over the water, no text, no people",
    19066: "Song army withdrawing north, blue flags drooping, tired steps, seen from far and behind",
    19068: "inside a Song camp, a few soldiers lying on mats, one sitting holding his head, grey sky, three men of different ages and beards",
    19069: "one young Song soldier sits tired on a river bank looking across to the other bank, exactly ONE character only",
    19071: "a Vietnamese envoy holding a long staff with plain tassels sits on a small boat crossing a river, a boatman standing behind him",
    19074: "a Song camp breaking up, soldiers folding tents and loading things onto carts, seen from far, simple faces",
    19076: "{DTN} holding a staff with plain tassels leads five tame elephants along a road, each elephant with a different handler",
    19077: "a Vietnamese embassy walking along a dirt road toward a distant Song city gate, plain red flags, seen from far and behind",
    19079: "returning people at a border: on the left Vietnamese officials in brown, on the right Song officials in blue, ordinary people walking through the middle",
    19080: "inside an army camp, {LVT} sits on a mat on one side of a low table, a Song official sits on a mat opposite, a map with drawn lines only and no writing lies between them",
    19083: "inside a general's residence, {LTK-G} sits on a woven mat beside a low wooden table with a map of drawn lines only, a small clay oil dish with a tiny flame, a military officer standing beside him",
    19085: "{LG} stands on a section of freshly built earth wall, villagers far away, plain flags",
    19086: "Vietnamese army arriving on a dirt road, plain red flags, seen from far, a small earth fort ahead",
    19088: "an army camp at night, small clay oil dishes and campfires glowing, {LTK-L} stands in the middle of the camp looking south",
    19089: "{LTK-L} sits by a window looking far away in the evening light, inside a mansion, exactly ONE character only",
    19090: "a quiet room with one small clay oil dish, an empty low wooden seat on a mat and a court robe and hat hanging on a wooden stand, bare plain walls, no pictures, completely empty, no people",
    19091: "in the court, {LTH} kneels receiving a marquis title from a ceremonial official, another official standing by",
    19092: "three golden thrones in a row, on each a faint translucent king like a memory, an elderly man with a white beard in a crimson narrow-sleeved tunic standing small in front, exactly four figures",
    19096: "a moonlit night on a river bank, a bamboo palisade, thin mist, completely empty, no people",
}

SONG = {19029, 19030, 19031, 19033, 19034, 19037, 19042, 19045, 19046, 19047, 19048, 19051, 19053, 19054,
        19055, 19057, 19061, 19062, 19066, 19068, 19069, 19074}
MIX = {19002, 19003, 19019, 19038, 19040, 19043, 19052, 19060, 19063, 19064, 19079, 19080, 19096, 19023}
SOMBER = set(range(19045, 19054))
NOMOD = "wood, bamboo, clay and woven cloth only, dirt roads, bare plain walls"
VN_DRESS = ("Vietnamese villagers and soldiers wear crossed-collar tunics with narrow sleeves tied by a cloth sash, short trousers, "
            "simple straw sandals, hair in a topknot or a wrapped cloth turban")
ERA_VN = (VN_DRESS + "; low wooden halls with dark brown pillars and grey tiled roofs with curved dragon-head ridge ends, "
          "thatched houses, simple brown leather vests or quilted cloth armor over the tunic, round iron helmets with a small rim, conical bamboo hats, long wooden spears, woven rattan shields, bows, plain brown-red triangular cloth pennants; " + NOMOD)
ERA_SONG = ("grey tiled roofs, black cloth hats with two flat side wings, soldiers in dull dark-grey lamellar armor with iron helmets with a rounded pointed top and a short neck guard, no wide brim, no feathers, officials in black hats with two long flat wings sticking out sideways, no writing or signboards anywhere, "
            "plain dark blue triangular cloth pennants; " + NOMOD)
ARMED = re.compile(r"soldier|army|armies|troop|warrior|guard|general|spear|battle|march|fleet|archer|officer|pennant|flag|cavalry|war ", re.I)
CIVIL_VN = (VN_DRESS.replace("villagers and soldiers", "villagers and officials") + "; low wooden halls with dark brown pillars and grey tiled roofs with curved dragon-head ridge ends, thatched houses; "
            "wood, bamboo, clay and woven cloth only, no soldiers, no weapons, no armor, no helmets, no banners unless described, no writing anywhere")
CIVIL_SONG = ("grey tiled roofs, plain clay walls; officials in black cloth hats with two long straight flat wings sticking out sideways; "
              "wood, bamboo, clay and woven cloth only, no soldiers unless described, no writing or signboards anywhere")
SUFFIX = ("each person drawn once with two arms, every face, age and build different, single full-frame picture, one single image, no border, no text, detailed background")


def build(n, scene):
    s = re.sub(r"\{([A-Z0-9-]+)\}", lambda m: CH[m.group(1)], scene)
    s = re.sub(r"plain (red|orange) flags?", lambda m: "plain brown-red cloth pennants" if m.group(1) == "red" else "plain orange cloth pennants", s)
    s = re.sub(r"plain (dark blue|blue) flags?", "plain dark blue cloth pennants", s)
    s = re.sub(r"\bflags\b", "cloth pennants", s)
    s = re.sub(r"\bflag\b", "cloth pennant", s)
    armed = bool(ARMED.search(scene))
    era = (ERA_SONG if armed else CIVIL_SONG) if n in SONG else (ERA_VN if armed else CIVIL_VN)
    tone = "muted grey and orange tones, somber mood" if n in SOMBER else ""
    parts = [OPEN_SONG if n in SONG else OPEN_VN, s]
    if era:
        parts.append(era)
    if tone:
        parts.append(tone)
    parts.append(SUFFIX)
    return ", ".join(parts)


def main():
    md = MD.read_text(encoding="utf-8")
    rows = re.findall(r"^\| (19\d\d\d) \| [^|]+ \| [^|]+ \| (chibi \(LoRA ([\d,]+)\)[^|]*) \|$", md, re.M)
    items, warn = [], []
    nums = {int(r[0]) for r in rows}
    if nums != set(E):
        raise SystemExit(f"Số đoạn chibi trong kịch bản và trong E không khớp: thiếu {sorted(nums - set(E))}, thừa {sorted(set(E) - nums)}")
    for n, _, lora in rows:
        n = int(n)
        p = build(n, E[n])
        w = len(p.split())
        if w > 175:
            warn.append((n, w))
        items.append({"n": n, "lora": 0.0, "seed": n, "prompt": p})
    OUT.write_text(json.dumps(items, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Ghi {len(items)} prompt -> {OUT}; dài nhất {max(len(i['prompt'].split()) for i in items)} từ; cảnh báo dài >175 từ: {warn}")


if __name__ == "__main__":
    main()
