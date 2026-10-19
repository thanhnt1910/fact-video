"""TQ5N: bản chia lại Tập 5 theo câu: 173 ảnh (mỗi ảnh 1–2 câu lời kể).
Nửa đầu mỗi đoạn dùng lại ảnh TQ5 đã soi; nửa sau là cảnh mới (ghi ở dưới)."""
import json, sys, re, shutil
from pathlib import Path
R = Path(__file__).resolve().parent
sys.path.insert(0, str(R))
import tao_TQ5 as T
NV, STYLE, SUF = T.NV, T.STYLE, T.SUF
NV["taoang_t5"] = "Cao Ang, a slim young officer of about twenty-five with a clean youthful face and a faint moustache, hair in a topknot under a plain cap, wearing light iron scale armour over a dark tunic"
NV["nuthanh"] = "a young woman of about seventeen in a plain pale cross-collared robe with a dark sash, hair in a neat bun, a quiet sad face"
NV["tuonglinh"] = "a Han general in a plain iron helmet and scale armour over a dull red tunic"
units = json.load(open("/tmp/units5.json", encoding="utf-8")) if Path("/tmp/units5.json").exists() else json.load(open(R / "TQ5N_units.json", encoding="utf-8"))
json.dump(units, open(R / "TQ5N_units.json", "w", encoding="utf-8"), ensure_ascii=False)
old = {it["key"]: it for it in json.load(open(R / "TQ5_anh.json", encoding="utf-8"))}
N = {}
def n(b, nv, m): N[b] = (nv, m)
HD, TT, TA, TB = "hiende_t5", "taotao_t5a", "taotao_t5a", "taotao_t5b"
n(1, ["quan", "dan"], "thin court officials and townsfolk lean against half-collapsed blackened mud-brick walls in a ruined street of Luoyang, cold grey light, exhausted and silent")
n(2, ["vienthuat_t5a"], "exactly ONE man only: Yuan Shu stands alone in a grand hall of Shouchun gazing greedily at an empty low dais, no second figure, no crowd, red hangings")
n(3, ["vienthuat_t5b"], "exactly ONE man only: Yuan Shu in a bead-string crown sits slumped on the step of an empty dais in a dim hollow hall, no second figure, no crowd")
n(4, [], "dusk view of the walls of the new capital Xu rising from a wide plain, two dusty roads leading to it, plain banners on the walls, completely empty, absolutely no people")
n(5, ["lubo_t5", "kybinh"], "Lu Bu and a few riders gallop away from the burning gate of Chang'an at dawn, smoke rising behind them, dust, seen from the side")
n(6, [], "dry cracked fields beside Chang'an under a pale sky, withered crops, a bare tree, an abandoned empty ox cart, completely empty, absolutely no people")
n(7, [HD, "quan"], "the young emperor stands beside a big clay pot of gruel pointing at it with a questioning look while two officials look at each other worried, steam rising, palace yard")
n(8, [HD, "linh"], "the young emperor stands small and alone on the steps of a ruined palace facing an almost empty courtyard with only two thin guards, cold light")
n(9, ["quachty_t5", "linh"], "Guo Si's soldiers advance toward the palace gate with plain banners and raised spears, a few arrows arc through the air above, guards shield a covered cart, no one hit")
n(10, [HD, "quan", "dan"], "the emperor's ox cart passes through the east gate of Chang'an while villagers watch from both sides and officials walk behind it, morning light")
n(11, ["quachty_t5", "kybinh"], "Guo Si sits on his horse on a hill and watches a far-off column of carts and soldiers leave along the road, cold hard face, riders beside him")
n(12, ["truongte_t5", "lythoi_t5", "quachty_t5"], "three generals Zhang Ji, Li Jue and Guo Si meet on horseback at a crossroads, leaning toward each other, three different faces, plain banners behind")
n(13, ["babat", "hungno", "kybinh"], "rebel horsemen in rough leather and Xiongnu riders in felt hats and fur charge along a dusty road toward the viewer with plain banners")
n(14, ["linh", "kybinh"], "ranks of Han soldiers and rebel riders push forward in dust while far ahead the enemy ranks with red banners turn and retreat, seen from a hill, no one fighting up close")
n(15, [HD, "quan", "linh"], "at dawn the emperor and a few officials climb the northern bank of the Yellow River toward the small walled town of Anyi, boats behind them on the water")
n(16, ["dan", "quan", "linh"], "in the open yard of Anyi guards open a wooden pen and thin released prisoners walk out while townspeople cheer and officials stand by, winter light")
n(17, ["hantiem_t5", "dongthua_t5", "duongphung_t5"], "three generals Han Xian, Dong Cheng and Yang Feng stand apart from each other in a camp, arms folded, glaring in different directions, tents and plain banners")
n(18, [TA], "exactly ONE man only: Cao Cao stands on a hill at dawn looking north toward a far large army camp with many banners, no second figure, no crowd")
n(19, [TA, "trinhduc_t5"], "Cao Cao and Cheng Yu walk slowly side by side along a path in a mud-walled yard, Cheng Yu speaking quietly, morning light")
n(20, [TB, "tuanuc_t5", "trinhduc_t5"], "Cao Cao seated on a low platform with Xun Yu and Cheng Yu kneeling close on straw mats, talking earnestly, plain mud-walled room, daylight")
n(21, ["tuanuc_t5", TB], "Xun Yu speaks with a raised hand to Cao Cao who listens with a serious face, officials kneeling behind them on straw mats")
n(22, ["linh"], "a line of Yuan Shu's soldiers in red-brown with spears blocks a narrow mountain road while a far column with dark banners halts on the road behind, tense stand-off, no fighting")
n(23, ["dongchieu_t5"], "exactly ONE man only: Dong Zhao walks alone along a mountain road at dawn with a small cloth bundle, no second figure")
n(24, ["dongchieu_t5", "kybinh"], "Dong Zhao ties a closed bamboo-strip bundle with cord and hands it to a messenger rider who waits on his horse at a courtyard gate, morning light")
n(25, ["duongphung_t5", "tuongquan", "linh"], "Yang Feng stands in his camp speaking cheerfully to a few generals who nod, tents and plain banners behind")
n(26, [HD, "quan", "linh"], "the emperor's ox cart and a column of soldiers and thin officials arrive at the broken gate of Luoyang in summer heat, dust, ruined towers ahead")
n(27, [HD, "linh"], "the young emperor steps out of a small old walled house in the ruins with a guard at the door, weeds in the yard, soft light")
n(28, ["quan"], "thin officials in torn robes gather wild herbs and bark among the ruined walls of Luoyang, a quiet hungry mood")
n(29, ["truongte_t5", "hantiem_t5", "duongphung_t5", "quan"], "three armoured generals stand in a row bowing to the seated emperor in a ruined hall, charred pillars, officials behind them")
n(30, [TA, "linh", "dan"], "Cao Cao's army arrives at Luoyang with ox carts piled with grain sacks, soldiers walking beside them, dark banners, hungry officials watching from the ruined gate")
n(31, [TB, "quan"], "Cao Cao stands on a low dais in a ruined hall while kneeling officials hold out tied bamboo-strip bundles to him with both hands, charred pillars, soft light")
n(32, [HD, TB], "the young emperor and Cao Cao stand side by side on a dais with Cao Cao slightly in front, officials in rows below, plain mud-walled hall")
n(33, ["dongchieu_t5", TB], "Dong Zhao points southeast along a road across a wide plain while Cao Cao stands beside him on a hill looking in that direction, morning light")
n(34, ["dongchieu_t5", TB], "Dong Zhao speaks calmly to Cao Cao on a hillside while far below a small camp with banners can be seen")
n(35, [HD, "linh"], "the emperor's column winds along a mountain pass road seen from above, ox cart, soldiers and banners, autumn mist")
n(36, ["duongphung_t5", "kybinh"], "Yang Feng and a few riders ride south across open country toward distant city walls at dusk")
n(37, ["vienthieu_t5", "tuongquan"], "Yuan Shao sits on a hill with his officers and turns his head away in proud displeasure, camp tents and blue banners behind")
n(38, [TB, "quan"], "Cao Cao smiles slightly with hands joined to an envoy at the gate of a hall, officials watching, wooden pillars")
n(39, ["dan", "linh"], "soldiers and farmers harvest golden grain with sickles in wide fields, thatched granaries in the background, bright day")
n(40, ["tuanuc_t5", "quan"], "Xun Yu leads a line of clerks carrying tied bamboo-strip bundles across a courtyard, plain mud-walled hall behind")
n(41, ["tuanuc_t5", TB, "quan"], "Xun Yu brings three scholars in plain robes to the gate where Cao Cao greets them with joined hands, morning light")
n(42, ["vienthieu_t5", "linh"], "exactly ONE man only: Yuan Shao sits proudly on a horse in front of the walls of Ye with a large army camp stretching behind him, blue banners")
n(43, [TB], "exactly ONE man only: Cao Cao stands on the tower of the gate of Xu looking north at distant dust on the horizon, no second figure")
n(44, ["liubei_t5", "linh", "dan"], "a column of wagons loaded with grain sacks and a band of soldiers are given to Liu Bei at the gate of Xu while townsfolk watch, daylight")
n(45, [TB, HD, "dan"], "Cao Cao rides beside the emperor's ox cart through the gate of Xu while citizens bow along the street, banners, daylight")
n(46, [], "wide landscape of a plain in the southeast with two far army camps, one with red banners and one with dark-red banners, a river between, completely empty, absolutely no people close up")
n(47, ["vienthuat_t5a"], "exactly ONE man only: Yuan Shu stands alone on the gate tower of Shouchun at dusk looking northwest, no second figure, no crowd")
n(48, ["vienthuat_t5a", "linh"], "Yuan Shu rides in front of a vast army camp that spreads over a plain, ranks of soldiers with plain banners, proud look")
n(49, ["tonsach_t5", "linh"], "Sun Ce leads a small band of a few hundred tired soldiers through green hills, ragged plain banners, a few horses")
n(50, ["tonsach_t5", "kybinh"], "Sun Ce stands at the edge of a camp and watches Yuan Shu's mounted officers ride past without looking at him, a quiet cold look")
n(51, ["vienthuat_t5a", "quan"], "an old diviner points up at the night sky while Yuan Shu and officials look up at a long comet, torchlight, a courtyard")
n(52, [], "a red bonfire burning on a hillside beside a mound of yellow earth under a starry night sky, completely empty, absolutely no people")
n(53, ["dan"], "thin villagers with empty baskets sit and walk along a dusty roadside in the Huai valley, a hungry mood, no corpses")
n(54, ["quan"], "exactly ONE man only: an elderly adviser in a plain robe turns away and walks down the steps of a hall shaking his head, no second figure")
n(55, [TB], "exactly ONE man only: Cao Cao stands on the steps of a hall with a closed lacquered edict box held under his arm, calm look, no second figure")
n(56, ["lubo_t5", "linh", "dan"], "Lu Bu rides through the gate of Xiapi at the head of soldiers while townspeople watch from the side, banners")
n(57, ["tranhkhue_t5", "tranang_t4"], "the elder Chen Gui and his son Chen Deng talk quietly in a courtyard with worried faces, mud-walled houses")
n(58, ["lubo_t5", "kybinh"], "Lu Bu's riders gallop along a road in dust after a distant decorated bridal cart, a river beside the road")
n(59, ["lubo_t5"], "exactly ONE man only: Lu Bu stands on a platform with folded arms looking down at an empty square, grey tiled roofs, no second figure")
n(60, ["lubo_t5", "kybinh"], "Lu Bu hands a closed tied bamboo-strip bundle to a rider in a courtyard, the rider bowing, morning light")
n(61, ["duongphung_t5", "hantiem_t5", "linh"], "Yang Feng and Han Xian march with their soldiers under a red banner on a road, both with unhappy faces, dust")
n(62, ["tonsach_t5", "linh"], "Sun Ce drills his soldiers on a riverbank field at dawn, ranks of spearmen, plain banners, mist on the water")
n(63, ["tonsach_t5"], "exactly ONE man only: young Sun Ce stands on a hill at sunrise beside his horse, determined face, no second figure")
n(64, ["thaisutu_t5", "kybinh"], "Taishi Ci and a few horsemen come out of the mist on a hillside road, alert faces, seen from below")
n(65, ["tonsach_t5", "thaisutu_t5"], "Sun Ce holds a small halberd and Taishi Ci holds a helmet, each on his own horse, facing each other a short distance apart and grinning, muddy road")
n(66, ["tonsach_t5", "thaisutu_t5"], "Sun Ce laughs while Taishi Ci shrugs, the two men standing close in a camp, soldiers watching, plain banners")
n(67, ["tonsach_t5", "linh", "dan"], "Sun Ce's army enters the gate of a walled city at Kuaiji with plain banners while locals watch, morning light")
n(68, ["tonsach_t5", "linh"], "Sun Ce on horseback on a hill overlooks the green land of Jiangdong with his army in ranks behind him, golden light")
n(69, [], "winter view of the walls of the city of Wan on a plain with Cao Cao's army camps around it, thin snow, completely empty, absolutely no people close up")
n(70, ["truongtu_t5"], "exactly ONE man only: Zhang Xiu stands alone on the wall of Wan looking down at an enemy camp with cold anger, no second figure")
n(71, ["dienvi_t5", "linh"], "Dian Wei stands at the gate of a camp fence with a heavy halberd, firelight on his face, a few soldiers behind him, night")
n(72, ["linh"], "at dawn a large halberd stands planted upright in the ground at the gate of a camp while soldiers bow their heads around it, thin mist, grief, no one lying down")
n(73, [TA, "taoang_t5"], "young Cao Ang hands the reins of his horse to Cao Cao in the dark, torchlight and flames behind them, tense faces, no one injured")
n(74, [TA, "kybinh"], "Cao Cao and his tired riders lead a retreating column along a road with drooping banners at dawn")
n(75, ["tuongquan", "linh"], "a few generals and soldiers stand confused on the empty riverbank watching boats leave far away on the grey Huai river")
n(76, ["linh"], "Yuan Shu's army camp empties at dawn, soldiers leaving with bundles, fallen banners, abandoned carts, a sad hollow mood")
n(77, ["truongte_t5", "linh"], "soldiers carry a plain wooden coffin on a cart away from a southern walled town, banners drooping, grey light")
n(78, ["kybinh"], "a rider carries a closed wooden box wrapped in plain cloth toward the gate of Xu at dusk, dust")
n(79, ["hantiem_t5"], "exactly ONE man only: Han Xian rides alone north through empty hills at dusk, no second figure")
n(80, [TB, "dan", "linh"], "clerks and farmers bring ox carts of grain into a big storehouse yard of Xu while Cao Cao inspects the sacks, bright day")
n(81, ["vienthuat_t5a"], "exactly ONE man only: Yuan Shu lies on a plain low bed in a dim room with a hand on his chest and an empty wooden bowl on the floor, no second figure")
n(82, ["nuthanh", "linh"], "a young woman in a plain pale robe is escorted by a few soldiers through the gate of a palace in Jiangdong, morning light")
n(83, [TB, HD, "quan"], "seen from behind Cao Cao stands in the doorway of a hall facing the seated emperor while many officials bow in rows")
n(84, [], "a ruined mansion gate overgrown with grass and fallen plain banners in a dusty yard, completely empty, absolutely no people")
n(85, [HD], "exactly ONE man only: the young emperor stands at a wooden lattice window looking out over the walls and roofs of Xu at dusk, no second figure")
# --- đợt 1 sau khi soi (19/10): sửa 16 ảnh có biển chữ, sách, hai người giống nhau, ba người trên một ngựa ---
NOSIGN = "the buildings have bare plain walls and gates with no signboard, no plaque and no banner with writing above them"
n(2, ["vienthuat_t5a"], "exactly ONE man only: Yuan Shu in plain unmarked armour stands alone in a grand hall of Shouchun gazing greedily at a bare empty raised wooden platform with nothing on it, no second figure, no crowd, red hangings")
n(32, [HD, TB], "the young emperor, a slim beardless teenager with a smooth pale face in a pale cream robe, stands beside Cao Cao, a short man with a moustache in a dark charcoal robe, on a dais, two clearly different men, officials in rows below, plain mud-walled hall")
n(45, [TB, HD, "dan"], "the young emperor sits in an open ox-drawn cart while Cao Cao rides on a separate horse beside the cart, exactly one rider per horse, citizens bow along the street of Xu, banners, daylight")
n(55, [TB], "exactly ONE man only: Cao Cao stands on the steps of a hall holding a closed tied bamboo-strip bundle in his hand, calm look, no book, no second figure")
ADD = {1: NOSIGN, 10: NOSIGN, 15: "Han Chinese grey-tiled mud-brick houses only, no red-tiled roofs, no European buildings, no flowers in the foreground", 21: NOSIGN, 41: "flags and banners are plain solid colour with no emblem", 56: NOSIGN, 67: NOSIGN, 77: NOSIGN+", the coffin is a plain wooden box", 80: NOSIGN+", the storehouse has bare walls", 81: "the bed is a low straw-mat platform, the wall behind is bare with no hanging scrolls and no writing, no chair", 82: NOSIGN+", flags plain solid colour", 84: "no hanging banners, a single full-frame picture, no panels, no border, no frame"}

EXTRA_NEG = "nothing written or drawn on any wall, banner or object, no lamp, no chair with a back, no sheets of paper"
BEATS_NO = {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,70,71,72,73,74,75,76,77,78,79,80,81,82,84,85,86,87,88}
# ánh xạ số đoạn cũ -> cảnh mới nửa sau (n(1..85) theo thứ tự các đoạn có ≥2 câu)
second_beats = [u[0] for u in units if u[1] == 1]
assert len(second_beats) == len(N) == 85, (len(second_beats), len(N))
out, canh = [], []
dst = R.parent.parent / "assets" / "anh_2d" / "TQ5N"; dst.mkdir(parents=True, exist_ok=True)
src = R.parent.parent / "assets" / "anh_2d" / "TQ5"
si = 0
for k, (b, p, text) in enumerate(units, 1):
    key = f"{k:03d}"
    if p == 0:
        o = old[f"{b:03d}"]
        out.append({"key": key, "cau": k, "nv": o["nv"], "text": text, "prompt": o["prompt"], "tai_dung": f"{b:03d}"})
        canh.append({"key": key, "nv": o["nv"], "mo_ta": "dùng lại ảnh TQ5 %03d" % b})
        if (src / f"{b:03d}.jpg").exists() and not (dst / f"{key}.jpg").exists():
            shutil.copy(src / f"{b:03d}.jpg", dst / f"{key}.jpg")
    else:
        si += 1
        nv, m = N[si]
        if si in ADD: m = m + ". " + ADD[si]
        ch = "; ".join(NV[x] for x in nv)
        if nv:
            pr = f"{m}. {EXTRA_NEG}. Characters (keep exactly this look): {ch}. {STYLE}. {SUF} {EXTRA_NEG}."
        else:
            pr = m + ". An empty quiet scene of objects and landscape only. 2D franco-belgian ligne claire comic illustration of ancient China, clean uniform dark ink outlines, flat muted colours with soft shading, earthy palette of ochre, jade green, indigo and warm cream, no text, no numerals, no letters, no watermark, not 3D, not a photo. " + T.ANTI
        out.append({"key": key, "cau": k, "nv": nv, "text": text, "prompt": pr, "beat_cu": b})
        canh.append({"key": key, "nv": nv, "mo_ta": m})

# --- 19/10: sửa lỗi ngựa (dính vào người, thừa/thiếu chân, ngựa trong nhà) ---
HFIX = ("Every horse is drawn complete: one head, one neck, four legs, one tail, clearly separate from every person; "
        "each person stands or sits fully in front of or beside a horse, never overlapping a horse body, no horse behind a person's back")
HKEYS = "020 022 024 026 029 030 050 054 064 079 080 082 094 099 115 118 148 155 156".split()
INDOOR = "049 089".split()
for o in out:
    if o["key"] in HKEYS: o["prompt"] = o["prompt"].rstrip() + " " + HFIX + "."
    if o["key"] in INDOOR: o["prompt"] = o["prompt"].rstrip() + " An interior of a room with only the people, desk, lamp and wall hangings described here and nothing else; the whole picture is inside the room."
    if o["key"] == "099": o["prompt"] = o["prompt"].rstrip() + " Sun Ce walks on foot with ordinary human legs in cloth trousers and boots."
(R / "TQ5N.json").write_text(json.dumps({"ma": "TQ5N", "ghi_chu": "Tập 5 chia lại theo câu: 173 ảnh (88 dùng lại từ TQ5, 85 mới)", "canh": canh}, ensure_ascii=False, indent=1), encoding="utf-8")
(R / "TQ5N_anh.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
(R / "TQ5N_moi.txt").write_text(",".join(o["key"] for o in out if "beat_cu" in o), encoding="utf-8")
print("ok", len(out), "ảnh;", sum(1 for o in out if 'beat_cu' in o), "ảnh mới")
