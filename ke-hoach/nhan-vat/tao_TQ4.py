"""Tạo TQ4.json (cảnh) và TQ4_anh.json (86 prompt vẽ) cho tập 4. Khóa ảnh = số câu lời kể (001...086), mỗi ảnh dùng một lần.
Trang phục theo mã trong TQ4_trang_phuc.json (xem ke-hoach: claude/tam-quoc-tap-4-kich-ban.md)."""
import json
from pathlib import Path
R = Path(__file__).resolve().parent
tq = json.loads((R / "TQ.json").read_text(encoding="utf-8"))
t2 = json.loads((R / "TQ2.json").read_text(encoding="utf-8"))
tp = json.loads((R / "TQ4_trang_phuc.json").read_text(encoding="utf-8"))
NV = {**tq["nhan_vat"], **t2["nhan_vat_phu"], **tp["trang_phuc"]}
PK = tp["phu_kien"]
STYLE = tq["phong_cach"].replace("year 184 AD", "year 193 AD")

def lb(i): return "liubei_t4a" if i <= 33 else ("liubei_t4b" if i <= 57 else "liubei_t4c")
def qv(i): return "quanvu_t4a" if i <= 57 else "quanvu_t4b"
def tf(i): return "trieuphi_t4a" if i <= 57 else "trieuphi_t4b"
L = lambda i: lb(i)

# (số câu, nhân vật, số người, mô tả)
S = [
(1,["daokhiem_t4a"],1,"waist-up of Tao Qian, an old governor, holding out a small lacquered seal box with one hand in a ceremonial offer, the other arm hidden in his sleeve, exactly one man"),
(2,[lb(2) if False else "liubei_t4c"],1,"waist-up of Liu Bei bowing his head and shaking it gently in refusal, both hands tucked into his sleeves, exactly one man"),
(3,[],0,"an open bundle of bamboo-slip history books on a dark wooden desk with a brush beside it, warm candlelight"),
(4,[],0,"the gate of a prosperous walled city on a river plain with tiled towers and grain boats at the quay, soft morning light"),
(5,[],0,"a fork in a dirt road across a wide plain, one road heading toward northern hills and the other toward a river in the east, evening light"),
(6,[],0,"a stone ink slab and a stand of brushes on a plain wooden table at dawn"),
(7,[],0,"a small walled county town on a flat northern plain with a grey brick wall and one plain red banner, morning mist"),
(8,[],0,"a low official desk with three stacked bamboo-slip appointment documents and a small bronze seal, grey window light"),
(9,[],0,"two army camps far apart on a wide plain separated by a slow river, plain banners, a thin line of smoke, seen from a hill"),
(10,["liubei_t4a"],1,"waist-up of Liu Bei sitting alone at night beside a clay oil lamp, tired but thoughtful, an iron armour on a wooden stand behind him, exactly one man, his far hand hidden under the table"),
(11,["luubinh"],1,"waist-up of Liu Ping standing at a doorway with a sour contemptuous expression, hands hidden in his sleeves, exactly one man"),
(12,["liubei_t4a","thichkhach"],2,"waist-up two-shot of Liu Bei and a guest in plain dark clothes sitting across a low table, the guest bowing his head and speaking quietly, Liu Bei listening in surprise, hands hidden in sleeves, exactly two men, nothing in their hands"),
(13,["liubei_t4a"],1,"waist-up portrait of Liu Bei with a calm gentle face and the hint of a kind smile, both hands tucked into his sleeves, exactly one man"),
(14,[],0,"a row of tiled county roofs at dusk with a single lit window, quiet and small beneath a wide darkening sky"),
(15,["thaisutu_t4"],1,"waist-up of Taishi Ci arriving dusty and out of breath with an urgent expression, one hand holding a small rolled letter, the other arm hidden behind his back, exactly one man"),
(16,["khongdung_t4"],1,"waist-up portrait of Kong Rong, a refined scholar, calm and thoughtful, both hands tucked into his sleeves, a distant city wall faint behind him, exactly one man"),
(17,["liubei_t4a","thaisutu_t4"],2,"waist-up two-shot of Liu Bei moved and surprised, one hand pressed to his chest, and Taishi Ci bowing before him, exactly two men, outer arms hidden"),
(18,[],0,"a lone small army camp at dusk with a single tall plain red banner at the foot of northern hills, a thin cooking fire"),
(19,[],0,"a wooden cart at a camp gate loaded with spears, shields and plain iron helmets, no people"),
(20,[],0,"bare fields at dawn with abandoned cooking fires and dropped plain flags after an army has fled, empty of people"),
(21,[],0,"a small clay cup and a folded letter on a scholar's table in warm lamp light"),
(22,[],0,"a closed wooden gate at evening with a small hanging lantern, calm and waiting"),
(23,["taotao_t4"],1,"waist-up of Cao Cao with a sharp ambitious gaze looking forward, one hand resting on his sword hilt, the other arm hidden under his cloak, exactly one man"),
(24,[],0,"a quiet country house with a courtyard and a bamboo grove on a green hillside, peaceful morning"),
(25,[],0,"an empty lonely road at dusk in mist with a single overturned small cart and a few scattered belongings, no people"),
(26,[],0,"a dark river crossing with a broken wooden bridge at night and distant torch light, no people"),
(27,["taotao_t4"],1,"waist-up of Cao Cao with a cold clenched jaw and a hard gaze, a plain dark banner behind him, both arms hidden under his cloak, exactly one man"),
(28,["daokhiem_t4a"],1,"waist-up of Tao Qian seated at a desk with a tired worried face, hands hidden in his sleeves, exactly one man"),
(29,[],0,"a rich walled city on a river plain with grain boats at the quay and market stalls under striped awnings, no people"),
(30,[],0,"a walled city with thick grey smoke rising over its towers and abandoned fields before it, no people"),
(31,[],0,"dry abandoned fields and an empty river bank under a heavy sky, black smoke far away, no people"),
(32,[],0,"an empty market street with overturned stalls and drifting dust in grey light, no people"),
(33,["tuongquan"],1,"waist-up of a Han army commander reading an urgent rolled letter with one hand, serious face, the other arm hidden behind his back, exactly one man"),
(34,["tuongquan","liubei_t4b"],2,"waist-up two-shot of an army commander and Liu Bei standing side by side looking east at dawn, resolute, outer arms hidden, exactly two men"),
(35,["liubei_t4b"],1,"waist-up of Liu Bei striding forward at the head of his camp, determined face, one hand on the hilt of his sword, the other arm hidden, exactly one man"),
(36,[],0,"a small modest army camp at dusk with a handful of tents, sacks of grain and a few horses grazing, no people"),
(37,["tuongquan","liubei_t4b"],2,"waist-up two-shot of an officer and Liu Bei on a muddy river bank east of a walled town looking grimly toward enemy smoke, outer arms hidden, exactly two men"),
(38,["daokhiem_t4a"],1,"waist-up of Tao Qian at a window looking out hopefully at the road, hands hidden in his sleeves, exactly one man"),
(39,["daokhiem_t4a","liubei_t4b"],2,"waist-up two-shot of Tao Qian pointing toward a line of tents with one hand while Liu Bei bows in thanks with hands joined, exactly two men"),
(40,[],0,"a quiet hall with two empty seats side by side and a low table with a single ceramic cup, soft light"),
(41,[],0,"a small bronze official seal on a ribbon cord resting on a lacquered tray beside a rolled bamboo-slip memorial, morning light"),
(42,[],0,"a small walled town on a plain at dusk with a few camp fires outside the wall, no people"),
(43,["taotao_t4"],1,"waist-up of Cao Cao turning to look back over his shoulder with a cold frown, a dusty cloak around him, exactly one man, arms hidden"),
(44,["lubo_t4a"],1,"waist-up of Lu Bu seen from behind in armour, looking toward a distant gate, his face not visible, exactly one man, arms hidden"),
(45,[],0,"the gate of a city standing open onto a calm morning road, a thin mist, no people"),
(46,[],0,"a stone road leading away from a field camp with a few plain red banners lowered, no people"),
(47,["daokhiem_t4b"],1,"waist-up of Tao Qian propped on pillows in a dim room, frail and tired, one hand hidden under the blanket, exactly one man"),
(48,["mitruc_t4"],1,"waist-up of Mi Zhu seated at a bedside with a worried gentle face, hands hidden in his sleeves, dim lamp light, exactly one man"),
(49,["daokhiem_t4b","mitruc_t4"],2,"waist-up two-shot of Tao Qian whispering to Mi Zhu who bends close to listen, dim lamp light, exactly two men, outer arms hidden"),
(50,[],0,"an empty lamp-lit room with a low bed, curtains drawn and a bowl of medicine on a small stool"),
(51,["mitruc_t4","liubei_t4b"],2,"waist-up two-shot of Mi Zhu bowing before Liu Bei in a camp, Liu Bei startled, hands hidden in sleeves, exactly two men"),
(52,["liubei_t4b"],1,"waist-up of Liu Bei hesitating and shaking his head, hands tucked into his sleeves, uneasy look, exactly one man"),
(53,["tranang_t4"],1,"waist-up of Chen Deng speaking earnestly with one hand raised palm out, the other arm hidden, exactly one man"),
(54,[],0,"a tall proud southern walled city with a grand gate-tower and a banner above rice fields, grey sky, no people"),
(55,["tranang_t4","liubei_t4b"],2,"waist-up two-shot of Chen Deng shaking his head firmly while Liu Bei listens carefully, hands hidden in sleeves, exactly two men"),
(56,["khongdung_t4"],1,"waist-up of Kong Rong urging with a firm kind look, hands hidden in his sleeves, exactly one man"),
(57,["liubei_t4b"],1,"waist-up of Liu Bei bowing slightly in acceptance with his hands joined in front of him, solemn face, exactly one man"),
(58,[],0,"a small spring stream flowing into a wide calm river on a plain, soft light"),
(59,[],0,"three objects on a wooden table: a jade pendant, a rolled scroll and a small clay bowl, warm light"),
(60,[],0,"a wooden chest of coins and bolts of silk stacked in a storeroom, lamp light, no people"),
(61,["liubei_t4c"],1,"waist-up of Liu Bei in his governor's robe standing at the top of the steps of a city hall looking over the city, calm and weighty, hands hidden in his sleeves, exactly one man"),
(62,[],0,"a heavy ring of city keys and a seal on a wooden stand beside an open city gate, morning light"),
(63,[],0,"two empty cushions facing each other across a closed lacquered box in a quiet hall, soft light"),
(64,["liubei_t4c"],1,"waist-up of Liu Bei listening with a thoughtful look, one hand at his chin, the other arm hidden, exactly one man"),
(65,[],0,"a walled city on a plain with a single red banner on its tower at evening, no people"),
(66,[],0,"a balance scale on a wooden table with a small jade piece on one side and a small bag of coins on the other, soft light"),
(67,["liubei_t4c"],1,"waist-up of Liu Bei with a tired humane look reading a bamboo slip, hands hidden in his sleeves, exactly one man"),
(68,[],0,"an unrolled blank bamboo-slip scroll beside a closed wooden box in dawn light"),
(69,["liubei_t4c"],1,"waist-up portrait of Liu Bei in his early thirties, calm and weathered, looking slightly to the side, hands hidden, exactly one man"),
(70,[],0,"a small county gate with a plain flag in early morning light, no people"),
(71,[],0,"a worn straw sandal and a discarded black cap lying on a stone step, morning light"),
(72,[],0,"a long winding road across hills with milestone stones leading from a village to a river city, golden light"),
(73,["quanvu_t4b","trieuphi_t4b"],2,"waist-up two-shot of Guan Yu and Zhang Fei standing side by side, calm serious faces, outer arms hidden, exactly two men"),
(74,[],0,"one wide wooden bed with three folded blankets in a modest room, a clay lamp glowing"),
(75,[],0,"a rich walled city on a river with grain boats moored under gathering dark clouds, no people"),
(76,[],0,"a plain grave mound with incense sticks smoking at grey dawn, bare trees, no people"),
(77,[],0,"a tall gate-tower of a southern city above rice fields, banner flying under a grey sky, no people"),
(78,[],0,"a half-open door with a lamp in a government hall corridor, long shadows, no people"),
(79,["liubei_t4c"],1,"waist-up of Liu Bei alone on a city wall at dusk looking around at the four directions, worried, hands hidden in his sleeves, exactly one man"),
(80,[],0,"four roads meeting at a city gate, each fading into hills under a darkening sky, no people"),
(81,[],0,"two sets of footprints on a dirt road, one heading north and one heading east, in soft morning light"),
(82,[],0,"three lit lanterns at a gate at night, warm glow in the dark"),
(83,[],0,"a lacquered gift box with a gold clasp slightly open, dark mist curling around it on a table"),
(84,["lubo_t4b"],1,"a small distant figure of Lu Bu seen from behind on a long empty road leading toward a city gate at dusk, travel-stained, exactly one man, arms hidden"),
(85,[],0,"a rainy night at a city gate with a lone lantern and a bundle left on the road, no people"),
(86,[],0,"a closed bamboo-slip scroll tied with cord on a desk beneath a clay lamp at night"),
]
assert [s[0] for s in S] == list(range(1, 87)), "thiếu hoặc lặp ảnh"
# phụ kiện chức vụ
EXTRA = {}
for i, nv, n, m in S:
    for x in nv:
        if x == "liubei_t4b" and 41 <= i <= 57: EXTRA[(i, x)] = PK["day_an_thu_su"]
        if x == "khongdung_t4" and i == 56: EXTRA[(i, x)] = PK["an_tuong_bac_hai"]

SUF = ("medium shot, simple natural poses, every person has exactly two arms, two hands and two legs with natural adult proportions, "
       "serious weathered faces, no extra limbs, no duplicated people, no deformed faces, no text, no letters, no watermark. "
       "Flags and banners are plain solid colour with no symbols. All objects are realistic with no faces")
out, canh = [], []
for i, nv, n, m in S:
    k = f"{i:03d}"
    canh.append({"key": k, "nv": nv, "so_nguoi": n, "mo_ta": m})
    if n == 0:
        out.append({"key": k, "nv": [], "prompt": m + ". An empty quiet scene of objects and landscape only. 2D franco-belgian ligne claire comic illustration of ancient China, clean uniform dark ink outlines, flat muted colours with soft shading, earthy palette of ochre, jade green, indigo and warm cream, no text, no numerals, no letters, no watermark, not 3D, not a photo"})
        continue
    cnt = f"The picture contains exactly {n} {'person' if n == 1 else 'people'} in the foreground and no one else."
    chars = " Characters (keep exactly this look): " + "; ".join(NV[x] + ((", " + EXTRA[(i, x)]) if (i, x) in EXTRA else "") for x in nv) + "."
    out.append({"key": k, "nv": nv, "prompt": f"{m}. {cnt}{chars} {STYLE}. {SUF}"})
(R / "TQ4.json").write_text(json.dumps({"ma": "TQ4", "ghi_chu": "Tập 4: Bình Nguyên, Bắc Hải, Từ Châu", "canh": canh}, ensure_ascii=False, indent=1), encoding="utf-8")
(R / "TQ4_anh.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print("ok", len(S), "ảnh")
