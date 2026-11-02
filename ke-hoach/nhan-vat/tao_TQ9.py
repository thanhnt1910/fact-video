"""Tạo TQ9.json (nhân vật + cảnh) và TQ9_anh.json (prompt vẽ) cho video dài "Tào Tháo thật sự ác đến mức nào, theo chính sử?".
Khóa ảnh = số câu lời kể (001...187), mỗi ảnh dùng một lần. Chỉ vẽ nhóm A (nhân vật, sự kiện) và B (cảnh vắng người) theo
ke-hoach/tao-thao-ac-phan-canh.md; nhóm C (bản đồ, sơ đồ) và D (thẻ chữ) dựng bằng code, không vẽ AI.
Quy tắc: xem CLAUDE.md (Hán, không máu, không chữ, Tào Tháo tay không, cảnh một người ghi 'exactly ONE man only')."""
import json, re
from pathlib import Path
R = Path(__file__).resolve().parent
tq = json.loads((R / "TQ.json").read_text(encoding="utf-8"))
t2 = json.loads((R / "TQ2.json").read_text(encoding="utf-8"))
tp4 = json.loads((R / "TQ4_trang_phuc.json").read_text(encoding="utf-8"))
tp5 = json.loads((R / "TQ5_trang_phuc.json").read_text(encoding="utf-8"))
PLAN = {int(k): v for k, v in json.loads(Path("/tmp/pc/plan2.json").read_text(encoding="utf-8")).items()} if Path("/tmp/pc/plan2.json").exists() else json.loads((R / "TQ9_plan.json").read_text(encoding="utf-8"))
(R / "TQ9_plan.json").write_text(json.dumps(PLAN, ensure_ascii=False), encoding="utf-8")
BEATS = {}
for l in (R.parent / "tao-thao-ac-den-muc-nao-kich-ban.md").read_text(encoding="utf-8").splitlines():
    m = re.match(r"(\d+)\. \[[^\]]*\] (.*)", l)
    if m: BEATS[int(m.group(1))] = re.sub(r"\s*\[KIỂM[^\]]*\]", "", m.group(2))

NV = {**t2["nhan_vat_phu"], **tp4["trang_phuc"], **tp5["trang_phuc"]}
E = ", empty hands, no weapon"
NV.update({
 "linh": "a Han soldier in a plain iron helmet and leather-and-iron scale armour over a dull red-brown tunic",
 "quan": "a court official in a black cap and a dark grey robe",
 "tt_boy": "Cao Cao as a lively clever boy of about twelve with bright cheeky eyes, hair in two tufts, a fine silk robe in dark blue",
 "tt20": "Cao Cao at about twenty, a short wiry young man with sharp clever eyes, clean-shaven with only a faint moustache, hair in a topknot under a black official cap, dark-blue cross-collared robe with a dark sash" + E,
 "tt34a": "Cao Cao at about thirty-four, a short wiry man with sharp clever eyes, a thin moustache and a small beard, black official cap, dark-blue cross-collared official robe" + E,
 "tt34b": "Cao Cao at about thirty-four, a short wiry man with sharp clever eyes, a thin moustache and a small beard, disguised in a plain brown traveller's robe and a cloth headband" + E,
 "tt38": tp4["trang_phuc"]["taotao_t4"] + E,
 "tt41": tp5["trang_phuc"]["taotao_t5b"] + E,
 "tt45": "Cao Cao at about forty-five, a short wiry man with sharp clever eyes, a thin moustache and a small beard, dark charcoal cross-collared robe over light iron armour, a commanding look" + E,
 "tt53": "Cao Cao at about fifty-three, a short wiry man with sharp clever eyes, a thin moustache and a small beard with a few grey hairs, dark charcoal cross-collared robe with a dark sash, hair in a topknot under a plain black cap" + E,
 "tt60": "Cao Cao at about sixty, a short thin man with sharp tired eyes, a thin grey moustache and a short grey beard, dark charcoal cross-collared robe with a wide sash, black cap" + E,
 "tt65": "Cao Cao at about sixty-five, a short thin man with grey hair under a black cap, a thin grey moustache and a short grey beard, deep lines on a tired stern face, dark charcoal cross-collared robe" + E,
 "kienthac": "Jian Shuo, a powerful court eunuch of about forty-five with a smooth beardless face, a proud cold look, black official cap and a long dark-purple robe",
 "chukt": "an arrogant older man of about fifty in a rich dark-green robe with a gold-coloured sash, a puffed-up proud face and a thin grey beard",
 "huathieu": "Xu Shao, a thin old fortune-teller scholar with a long white beard and keen narrow eyes, plain pale robe, hair in a topknot",
 "tctung": "Cao Song, an elderly man of about sixty with a kind tired face and a grey beard, hair in a topknot, a good plain brown robe",
 "tcfather": "Cao Song at about forty, a calm well-fed man with a short black beard, dark-green official robe and a black cap",
 "khanvang": "a rebel peasant fighter with a yellow cloth tied around his head, a rough ochre tunic and a plain wooden staff",
 "huatuo": "Hua Tuo, a lean vigorous healer of about fifty-five with a thin white-flecked beard and a calm clever face, plain pale-green robe, hair in a topknot, a small cloth medicine bag at his side",
 "fuhou": "Empress Fu, a noble woman of about forty in a deep-red empress robe with a wide sash, hair in a high bun with plain hairpins, a dignified sad face",
 "fuhuan": "Fu Wan, a worried official of about fifty-five in a dark robe and a black cap, a frightened thin face and a short grey beard",
 "caotiet": "Cao Jie, a young woman of about twenty in a deep-red robe, hair in a high bun, a calm noble face",
 "khongdung7": "Kong Rong, a refined scholar-official of about fifty-six with a thin grey-flecked beard and a proud thoughtful face, pale grey cross-collared scholar's robe with wide sleeves and a dark sash, black scholar's cap",
 "masieu": "Ma Chao, a handsome strong young man of about thirty with a proud face, hair under a plain iron helmet, light iron armour over a dark tunic",
 "mateng": "Ma Teng, a stern old general of about sixty with a grey beard, dark official robe and a black cap",
 "chentho": "Chen Shou, a quiet scholar of about fifty in a plain grey robe, a thin moustache, hair in a topknot under a plain cap",
 "caopi": "Cao Pi, a cold composed man of about thirty-three with a smooth face and a thin moustache, dark ceremonial robe and a black formal cap",
 "caoxung": "Cao Chong, a sickly pale boy of about twelve lying in bed under a quilt, a thin gentle face",
 "sugia": "an envoy in a travelling robe with a rolled bamboo letter tucked in his sash",
 "vokhuatuo": "a worried woman of about forty in a plain brown robe, hair in a bun",
 "luson": "a young country host of about twenty-five in a plain brown tunic, friendly but uneasy",
})
PHONGCACH = tq["phong_cach"].replace("year 184 AD", "year 190 AD")
SUF = ("Eastern Han China, 2nd century AD: dirt roads, grey-tiled mud-brick and timber buildings, wooden lattice windows without glass, shallow open bronze or clay oil dishes (no lamps, no candles), straw mats and low benches, bamboo-slip scrolls tied with cord; "
       "every banner, cloth hanging and sign is a plain blank piece of cloth with no marks, no writing on any wall, scroll or sign; no lamps or lanterns on walls or posts, no chimneys, no electric poles or wires, no switches, no clocks, no beds with mattress or pillow; no text, no letters, no watermark; every person has exactly two arms and two hands with natural adult proportions and a different face; no gore, no blood; "
       "single full-frame picture, no panels, no border; rich detailed background that fits the place")
ONE = "exactly ONE man only, no second figure, no crowd. "
S = {}
def sc(n, nv, d): S[n] = (nv, d)
# ---- Chương 1
sc(1, [], "a great river flowing slowly through a misty ancient Chinese plain at dawn, bare banks and a lone broken wooden pier, soft thick mist over the water")
sc(3, [], "the Si River in northern China under a grey sky, thick smoke drifting over the still brown water, an overturned wooden cart and a torn cloth banner on the bank")
sc(4, [], "the river in the mist at dawn, a small empty wooden boat floating motionless, reeds and a pale low sun")
sc(5, ["tt38"], ONE + "Cao Cao stands alone on a barren field at dusk looking at pale bones scattered far off in the grass, hands hidden in his sleeves, heavy grief on his face, bare trees, dark sky")
sc(6, ["tt53", "quan"], "Cao Cao seated on a low dais gives an order to a court official who bows with both hands in his sleeves, shelves of bamboo-slip scrolls behind them, an oil dish on a low table, warm evening light")
# ---- Chương 2
sc(11, [], "a rich walled country house in the county of Qiao in the Eastern Han era, a courtyard with grey tiled roofs, a stone path and a carved wooden gate, afternoon sun")
sc(12, ["tt_boy", "hoanquan", "tcfather"], "a clever boy in a fine robe stands between his father and a smiling court eunuch in a wealthy house hall, wooden pillars, silk screens, a low table with food, warm light")
sc(13, ["tt20"], ONE + "young Cao Cao rides a horse at a gallop across a hunting field, a hawk perched on a post far behind, hills and wide grass, carefree and mischievous face, correct four-legged horse")
sc(14, ["tt20", "quanlai"], "young Cao Cao in an official cap stands on the steps of a district office in Luoyang with a clerk bowing beside him, a long wooden hall with a tiled roof behind, morning light")
sc(15, [], "a quiet northern district of Luoyang, a long street of grey mud-brick houses with tiled roofs between high walls, a wooden watchtower at the end, early morning")
sc(16, ["tt20"], ONE + "young Cao Cao in an official cap stands at the foot of the steps of a district office beside a tall wooden rack with five rods painted five colours, hands hidden in his sleeves, a firm serious face")
sc(17, ["kienthac"], ONE + "a powerful court eunuch sits on a carved low couch in a palace hall, wooden pillars and hanging red cloth, an oil dish on a table, a proud cold face")
sc(18, ["chukt"], "an arrogant older man in a rich robe strolls down the middle of a night street of Luoyang with two servants carrying torches, ignoring a closed gate, mud-brick houses and a watchtower behind, orange torch light")
sc(19, ["tt20", "quanlai"], "night scene in the courtyard of a district office: young Cao Cao seated on a low dais, clerks standing beside the rod rack, a wooden screen hides what lies beyond, torches on posts, no violence shown")
sc(20, [], "a street of Luoyang at night, completely deserted, closed wooden doors on both sides, a watchtower with a faint red glow, thin mist")
sc(21, ["tt20", "huathieu"], "the old fortune-teller Xu Shao sits in a quiet room studying young Cao Cao who kneels respectfully before him on a straw mat, an oil dish between them, wooden lattice window, dim warm light")
sc(25, ["hatien", "quan"], "He Jin in his hall hands a sealed bamboo letter to a kneeling messenger who bows, wooden pillars and red cloth, an oil dish, tense mood")
sc(26, ["hoanquan"], "a court eunuch hurries through a palace courtyard at night carrying a torch, smoke rising from distant palace roofs, wooden doors flung open, chaos implied only by smoke and fire light, no violence shown")
sc(27, ["dongtrac", "thieude", "hiende"], "on a palace dais the huge Dong Zhuo stands before a frightened young emperor who is led down from the throne, a smaller boy ready to take his place, kneeling officials in rows, pillars and red cloth")
sc(28, ["dongtrac", "tt34a"], "in a palace hall the huge Dong Zhuo offers an official post to Cao Cao with a broad hand gesture, Cao Cao stands calm with his hands in his sleeves, kneeling officials, pillars, lamp light")
sc(29, ["tt34a"], ONE + "Cao Cao stands in a hall corridor and slowly shakes his head, hands in his sleeves, a firm cold look, wooden pillars and a wall of dark shadows")
sc(30, ["tt34b"], ONE + "a disguised Cao Cao rides a horse out of the east gate of Luoyang at sunrise, a plain cloak, a tall city wall and gate-tower behind, a dirt road leading east, correct four-legged horse")
# ---- Chương 3
sc(33, ["tt34b", "luson"], "inside a country house a host and his family prepare a meal on a low table with bowls and clay jars, the guest Cao Cao sits on a straw mat in a plain traveller's robe, an oil dish, wooden lattice window")
sc(34, [], "the dark yard of a country house at night, a low table and clay jars, a small oil dish glowing, wooden doors half open, nobody present")
sc(35, [], "an empty country kitchen: a clay stove with a cold pot, bundles of firewood, hanging dried herbs, wooden shelves, warm dim light")
sc(37, ["tt34b", "dan"], "Cao Cao rides across a plain toward distant hills followed by two servants pulling a cart of wooden chests, a dirt road, wide sky, determined face, correct four-legged horse")
# ---- Chương 4
sc(39, ["vienthieu_t5", "tt38", "tuongquan"], "a council of warlords in a large tent, a low table, several leaders arguing with raised hands while Cao Cao stands at the side with his hands in his sleeves, a map-less table, oil dishes, tent poles")
sc(40, ["linh"], "columns of Han soldiers turn away from a mountain pass and march back in different directions under plain banners, dusty roads, a grey sky, a feeling of an army dissolving")
sc(41, [], "an abandoned battlefield plain with torn plain banners stuck in the ground, cold ashes, a few broken carts, a distant mountain range, grey sky")
sc(42, ["khanvang"], "a crowd of rebel peasants with yellow cloths on their heads pours across a plain toward a walled city under plain yellow banners, dust, farm fields")
sc(43, ["tt38", "quan"], "local officials in black caps bow in a courtyard and invite Cao Cao to take charge, Cao Cao stands calm with his hands in his sleeves, tiled roofs and wooden pillars")
sc(44, ["khanvang", "dan"], "a very long column of former rebel soldiers and their families walks slowly to surrender along a river road, carts and bundles, Cao Cao's soldiers watch from the side, wide plain, grey light")
sc(45, ["tt38", "linh"], "Cao Cao stands before lines of tall strong soldiers picked from a large crowd, choosing men for his own army while soldiers in armour hold plain banners behind him, a camp of tents, dusty light")
# ---- Chương 5
sc(46, ["tt38"], ONE + "Cao Cao sits alone in his tent reading a short bamboo-slip letter on a low table, his hands in his sleeves, a stunned grieving face, a small oil dish, tent poles and dark banners")
sc(47, [], "an old mansion of the Cao family in Xu Province, a quiet courtyard with fallen leaves, closed doors, a stone well, grey tiled roofs")
sc(48, ["tctung", "dan"], "a modest family convoy of two ox carts with luggage travels along a mountain road, an old man rides in one cart, servants walk beside, peaceful morning, green hills, no danger shown")
sc(49, ["tt38"], ONE + "Cao Cao stands before a low table with a large cloth map and small wooden markers, a stern angry face, hands hidden in his sleeves, dark banners and lamp light in a command tent")
sc(50, ["linh"], "Cao Cao's army in plain dark banners marches in long ranks through the gate of a walled city of Xu Province, spears upright, seen from outside the wall, bright afternoon light")
sc(52, ["linh"], "an army advances through a green countryside past villages of mud-brick houses with thin smoke rising far ahead, plain dark banners, a dusty road, a heavy mood")
sc(53, ["dan"], "villagers stand silently by a roadside in thick drifting smoke, women, old men and children, ragged clothes, tired faces, nothing violent shown, a burning house far away")
sc(55, [], "a deserted village after soldiers have passed: mud-brick houses with blackened roofs, drifting smoke, an overturned cart and scattered baskets, not a single person")
sc(56, ["dan"], "a long line of refugees from the capital region carries bundles and pulls small carts into a river town of Xu Province, tired faces, evening light, mud-brick houses behind")
sc(57, ["dan"], "families carrying bundles on poles walk along a dirt road toward a river, children by the hand, old people leaning on sticks, a dim hopeful light, grey hills")
sc(58, [], "an empty river dock of Xu Province with moored wooden boats left behind, ropes, stacked jars, soft morning mist, no people")
sc(59, [], "the Si River flowing slowly between low banks under heavy smoke drifting from the horizon, floating wreckage and an overturned boat, a quiet horror implied by emptiness")
sc(60, [], "a cold wide field after a battle: broken spears stuck in the ground, black ashes, torn banners, thin smoke rising to a grey sky, not a single person")
sc(61, ["linh"], "a tired army with lowered plain banners marches away along a dry road, soldiers carrying empty grain sacks, grey sky, a low sun, a sense of hunger")
sc(63, ["tt38"], ONE + "Cao Cao stands alone on a hill looking toward distant columns of smoke on the horizon, his hands in his sleeves, a stern unreadable face, wind in his cloak, evening sky")
sc(64, ["dan"], "a family of villagers sits among the ruins of a mud-brick house, a mother with a small child, an old man, empty bowls, thin smoke, a heavy quiet mood, no violence")
sc(65, ["quan", "lubo_t5"], "at the gate of Yanzhou the warlord Lu Bu rides in on a tall horse while two officials welcome him with bows, townspeople and soldiers watching from the wall, banners, correct four-legged horse")
sc(66, [], "the closed gate and courtyard of a scholar's house, a quiet garden with a stone table, bamboo-slip scrolls on a low desk, dusk light")
sc(67, [], "a dim study room: shelves full of rolled bamboo-slip scrolls, a low desk with a clay inkstone, a small oil dish, a wooden lattice window, no one present")
sc(68, ["tt38", "lubo_t5"], "two armies face each other across a wide plain, plain dark banners on the left and plain red banners on the right, in front a small short commander on one side and a tall commander in iron armour on a horse on the other, distant ranks of soldiers, grey sky")
# ---- Chương 6
sc(69, [], "the ruined palace of Luoyang: broken tiled roofs, blackened wooden pillars, weeds in a vast courtyard, grey sky, nobody present")
sc(70, ["hiende_t5", "linh"], "a young emperor in a worn robe walks on a dusty road with a thin line of tired officials and a few poorly armed soldiers, an ox cart behind, a bleak plain, wandering without protection")
sc(71, ["tt41"], ONE + "Cao Cao stands on a hill at dawn looking down at a distant small column of a wandering court, hands in his sleeves, a calculating thoughtful face")
sc(72, ["tuanuc_t5", "tt41"], "Xun Yu in a pale grey robe speaks to Cao Cao in a hall, hands in his sleeves, Cao Cao listens with a thoughtful look, a low table with an oil dish, wooden pillars")
sc(73, ["hiende_t5", "tt41", "linh"], "a long procession escorting a young emperor on a carriage toward the city of Xuchang, soldiers with spears and plain dark banners, Cao Cao riding beside the carriage, a dusty road, golden light, correct four-legged horse")
sc(74, ["hiende_t5", "tt41"], "a young emperor sits on a throne on a wide dais, Cao Cao stands beside it with his hands in his sleeves, officials kneel in rows below, pillars and red cloth, formal mood")
sc(75, [], "an empty grain storehouse with large wooden bins and bare floors, a few empty sacks, a ray of light through a high lattice window")
sc(76, [], "a wide field of abandoned farmland with dry weeds and cracked earth, a broken plough, distant mud-brick huts, grey sky")
sc(77, ["quan", "tt41"], "two officials in grey robes bow and present a rolled bamboo-slip plan to Cao Cao in a hall, Cao Cao reads it thoughtfully with his hands hidden in his sleeves, a table with a map, an oil dish")
sc(78, ["dan", "linh"], "peasants and soldiers farm together in neat rows of a large field, oxen pulling wooden ploughs, soldiers' spears planted at the field's edge, a young green crop, wide plain, morning light")
sc(80, [], "a full grain storehouse with rows of tall wooden bins brimming with golden grain and stacked sacks, warm light from a lattice window, no people")
sc(82, ["vienthieu_t5", "tt45"], "two great armies face each other across the Yellow River at Guandu: a vast army under plain blue banners on the far bank and a smaller army under plain dark banners on the near bank, two commanders watching, spear ranks, dust, grey sky")
sc(83, ["linh"], "inside a captured camp, soldiers carry open wooden chests full of rolled bamboo-slip letters out of a command tent, officers watch, torches and tent poles at night")
sc(85, ["tt45", "linh"], "Cao Cao stands before a pile of rolled bamboo-slip letters burning in a large bronze brazier in front of his tent, flames lighting his stern face, a few soldiers watching from a distance, hands hidden in his sleeves")
sc(93, ["tt53", "quan"], "Cao Cao seated on a low dais receives two scholars who bow before him, a hall with a low table and bamboo-slip scrolls, an oil dish, wooden pillars, warm light")
sc(96, ["tt53"], "Cao Cao sits on a low dais, before him stand two men: a gentle scholar in a plain pale robe with a spotless modest look and a stern capable officer in dark armour with a proud look, a hall with pillars and an oil dish, the dais slightly raised")
sc(97, ["tt53", "quan"], "Cao Cao points with an open palm toward a kneeling capable officer, hands otherwise in his sleeves, officials standing in two rows in a hall, wooden pillars, evening light")
sc(98, ["tt53", "quan"], "Cao Cao presides over a court in a large hall, officials in black caps standing in two long rows facing each other, a wide empty central aisle, wooden pillars and red cloth")
sc(84, [], "the command tent of a defeated warlord at night, an open lacquered chest of rolled bamboo-slip letters on the floor, a small oil dish, tent poles, no people")
sc(86, [], "a large army camp at night after a defeat, a dying camp fire with embers, empty tents and plain dark banners, thin smoke, no people")
sc(87, [], "inside an empty tent a heap of grey ash still smoking on the ground, a toppled chest, faint orange glow, no people")
sc(88, [], "a camp after a battle at dawn, plain banners drooping on poles, stacked spears, cold fire pits, grey sky, no people")
sc(89, [], "the quiet plain of Guandu after the battle, torn plain banners stuck in the ground, trampled earth, low mist, no people")
sc(92, [], "the Guandu plain at sunrise, thin mist over trampled fields, torn banners, a pale pink sky, silence, no people")
# ---- Chương 7
sc(99, ["quan"], "a small group of officials in black caps stand together in a corner of a palace hall with serious faces, whispering, hands in sleeves, the other officials far away, wooden pillars")
sc(100, ["khongdung7", "quan"], "Kong Rong stands among the courtiers in a palace hall, upright and calm in a pale grey scholar's robe, other officials turn their heads toward him, pillars and red cloth")
sc(101, ["khongdung7"], ONE + "Kong Rong sits at a low desk with bamboo-slip scrolls and a brush, writing by the light of an oil dish, a quiet smile of irony, wooden lattice window, night")
sc(102, ["khongdung7", "sugia"], "Kong Rong receives an envoy from the south in a hall, both bowing politely, an envoy in a different southern-style robe, officials looking on warily, wooden pillars, oil dishes")
sc(103, [], "an empty courtroom: a raised dais with a low judge's table, rows of empty mats, a rack of rods against the wall, grey light from a lattice window")
sc(104, [], "a scholar's family house with a closed carved gate and a sealed wooden door, an empty courtyard, a dry tree, cold grey light")
sc(106, [], "Cao Cao's mansion at night: a tiled roof under a pale moon, an oil dish glowing in a lattice window, silent courtyard, no people")
sc(107, ["huatuo"], ONE + "Hua Tuo walks along a country road with a small cloth medicine bag, green fields and hills, a calm friendly face, morning light")
sc(108, ["huatuo", "tt53"], "Cao Cao sits on a straw mat holding his forehead in pain while the healer Hua Tuo sits beside him calmly, a low table with a small clay jar, an oil dish, a quiet room")
sc(109, ["huatuo"], ONE + "Hua Tuo stands at a wooden lattice window looking out at a road, hesitating, hands in his sleeves, a quiet room with an oil dish and shelves")
sc(110, ["huatuo", "tt53"], "Hua Tuo kneels with hands in his sleeves before Cao Cao, who sits on a low seat, a respectful request, a hall with pillars and an oil dish")
sc(111, ["sugia", "vokhuatuo"], "an envoy stands at the wooden gate of a modest house while a worried woman looks out of the doorway, a courtyard with a clay jar and a small tree, afternoon light")
sc(113, ["huatuo", "linh"], "Hua Tuo walks with his head high between two soldiers on a dusty road toward a distant city wall, a few villagers watching from the side, evening light, no violence")
sc(114, ["tuanuc_t5", "tt53"], "Xun Yu kneels and pleads before Cao Cao in a hall, hands in his sleeves, Cao Cao sits with a cold face, an oil dish on a table, wooden pillars")
sc(115, ["tt53"], ONE + "Cao Cao sits alone on his seat and slowly shakes his head, a cold closed expression, hands in his sleeves, dark hall, one oil dish")
sc(116, ["huatuo"], ONE + "Hua Tuo sits on a straw mat in a prison cell with wooden bars, a bundle of bamboo-slip scrolls beside him, a tired calm face, a thin ray of light from a high slit")
sc(117, ["huatuo", "linh"], "Hua Tuo kneels beside a small clay brazier where a bundle of bamboo slips burns, hands in his sleeves, a jailer stands far back by the open cell door with his back turned, faint orange light")
sc(118, ["tt53", "caoxung"], "Cao Cao sits on a low wooden platform covered with straw mat holding his own forehead, beside him a sick boy lies on the same straw mat under a plain quilt with his head on a wooden headrest, an oil dish and a clay bowl of medicine, dim light")
sc(119, ["tt53"], ONE + "Cao Cao stands before the doorway of a sickroom closed by a hanging reed curtain, head bowed in regret, hands in his sleeves, a lone oil dish on the floor, night")
sc(120, [], "an old study: a low desk with a few rolled bamboo-slip scrolls and a clay inkstone, shelves of scrolls, a small oil dish, a lattice window, nobody present")
sc(121, [], "a few bamboo-slip scrolls tied with cord lying on a wooden table, a small oil dish, soft shadows, warm light, no people")
sc(122, [], "a records room: shelves of rolled bamboo scrolls in rows, a low desk, an oil dish, dust in a ray of light, no people")
sc(125, ["masieu", "linh"], "Ma Chao rides at the head of a few weary riders across a dusty western plain at dusk after a defeat, banners lowered, hills far away, correct four-legged horses")
sc(126, ["mateng", "linh"], "old Ma Teng walks out of a palace gate between two guards, head held high, officials watching from the stairs, not bound, no violence, morning light")
sc(128, [], "the empty yard of a western general's house, a gate wide open, a stone horse-trough, dry leaves blowing, no one present")
sc(129, [], "a long empty dirt road stretching through dry hills in a haze of dust, a lone dead tree, a pale sky, no people")
# ---- Chương 8
sc(132, ["tt53"], ONE + "Cao Cao stands alone in the middle of a vast palace hall with tall pillars and long shadows, small against the hall, hands in his sleeves")
sc(133, ["tt53", "quan"], "Cao Cao stands holding nothing, a bronze tally lies on the table beside him, behind him officials stand in rows, his hand held out calmly over the tally, a hall with pillars")
sc(134, ["hiende_t5", "fuhou"], "the young emperor and Empress Fu sit side by side in a quiet palace room, silent and apart, an oil dish, silk screens, wooden pillars, dim light")
sc(135, ["fuhou"], ONE + "Empress Fu sits at a low desk writing a letter on bamboo slips with a brush resting in her hand, an oil dish, a silk screen behind her, a worried noble face")
sc(136, ["fuhuan", "sugia"], "a messenger hands a rolled letter to Fu Wan in his house, Fu Wan takes it with trembling hands, an oil dish and a wooden screen, a tense hushed scene")
sc(137, ["fuhuan"], ONE + "Fu Wan kneels beside a closed lacquered chest, hands in his sleeves, a frightened face, afraid to open it, an oil dish, night")
sc(138, ["tt60", "quan"], "a kneeling official presents a rolled bamboo letter to Cao Cao who sits in a dark hall with a stern cold face, an oil dish, wooden pillars")
sc(139, ["linh", "quan"], "soldiers in iron helmets with spears enter a palace hall, their leader an officer in front, palace maids and attendants step aside, no violence, pillars and red cloth, morning light")
sc(140, ["fuhou"], ONE + "Empress Fu crouches in a narrow gap between a wall and a wooden partition, a frightened face half hidden, a torn silk sleeve, dim light, no violence")
sc(141, ["fuhou", "hiende_t5"], "Empress Fu with loose hair meets the emperor on the steps outside a palace hall, both pale and silent, guards far in the background, a grey sky")
sc(142, ["fuhou"], ONE + "Empress Fu with loose messy hair and bare feet walks across a stone courtyard, a few guards far behind her, tall palace walls, grey dawn")
sc(143, ["hiende_t5"], ONE + "the young emperor stands on the palace steps with his head bowed, hands in his sleeves, powerless, a heavy mood, grey light")
sc(144, [], "a palace with heavy closed doors, a long stone corridor, an oil dish on the floor, long shadows, nobody present")
sc(146, [], "a long empty dirt road to the far north under a cold sky, a lone wooden cart wheel on the roadside, dry grass, no people")
sc(147, ["caotiet"], ONE + "Cao Jie in a deep-red empress robe sits on a low throne in a palace room with a calm noble face, silk screens and pillars, an oil dish")
sc(149, ["hiende_t5", "tt60", "quan"], "the emperor sits on a throne on a dais surrounded by officials in dark robes, Cao Cao stands among them with hands in his sleeves, a formal hall, the emperor looks small")
sc(150, [], "an empty throne on a high dais in a palace hall, red cloth and tall pillars, a ray of light on the seat, no one present")
sc(153, [], "the city of Ye at dusk, a tall wall with a gate-tower and plain dark banners, a dusty road, red evening sky, no people")
sc(154, ["tt60"], ONE + "Cao Cao stands beside a table with a large cloth map and an oil dish at night, deep in thought, hands in his sleeves, the room otherwise empty")
sc(155, [], "the courtyard of a king's mansion at night lit by tall open bronze fire bowls with burning wood on tripod stands, empty armour racks, a closed gate, long shadows, no people")
sc(157, ["linh", "dan"], "a funeral procession slowly carries a plain wooden coffin on a cart through a gate, soldiers and mourners in white hemp robes walk behind, plain white banners with no writing, grey sky, a sombre mood")
sc(158, ["hiende_t5", "caopi"], "the emperor stands on a dais and hands over a small lacquered box set on a cushion to Cao Pi who bows, officials kneel in rows, a hall with red cloth, the moment of an abdication")
# ---- Chương 9
sc(160, ["chentho"], ONE + "the historian Chen Shou sits at a low desk writing on bamboo slips with a brush resting in his hand, shelves of scrolls, an oil dish, a quiet focused face, night")
sc(161, [], "a historian's study with a low desk, an inkstone, rolled bamboo-slip scrolls, a small oil dish, a lattice window and moonlight, nobody present")
sc(162, [], "a library of the southern kingdom: tall wooden racks of bamboo scrolls under a tiled roof, soft light, no people")
sc(163, [], "a wooden rack full of tied bamboo-slip scrolls with a small oil dish at its side, warm glow, no people")
sc(167, ["dan"], "villagers run through a field with bundles in their arms toward a river, thick smoke rising on the horizon behind them, women and children, panic implied only by movement and smoke, no violence")
sc(169, ["fuhou"], ONE + "exactly ONE woman only: Empress Fu sits alone on a straw mat in a dim palace room looking toward the door, a sad quiet face, an oil dish, silk screens")
sc(171, ["linh", "dan"], "lines of captured soldiers with their heads bowed walk quietly through the gate of a camp between rows of guards, a wide field, a grey sky, no violence")
sc(173, [], "an empty prisoners' camp enclosed by a rough wooden fence, bare trampled ground, a closed gate, a grey sky, no people")
sc(174, [], "an old city gate standing open after a disaster, dust drifting, a broken cart, a torn banner on the wall, silence, no people")
sc(175, ["huatuo", "khongdung7"], "two men stand apart in a dim hall with sad faces, the healer Hua Tuo with a medicine bag on the left and the scholar Kong Rong on the right, an oil dish, pillars, long shadows")
sc(177, [], "a dirt road splitting into two paths in dry hills, a blank rough stone marker with no writing between them, grey sky, no people")
sc(178, [], "a lonely fork in a plain dirt road at dusk, two paths leading in different directions, dry grass, a pale sky, no people")
sc(181, ["tt53", "dan"], "Cao Cao stands on a hill overlooking a large farming colony and a military camp in the plain below, scholars and officials around him bowing, farmers far away in the fields, hands in his sleeves, golden light")
sc(182, ["tt53"], ONE + "Cao Cao stands from behind before a small fire in a camp, rolled bamboo letters turning to ash, the dark camp silent around him, hands in his sleeves")
sc(183, ["tt53", "dan"], "Cao Cao stands before a line of hungry thin peasants on a ruined road, his head slightly bowed, his hands in his sleeves, a burnt village far behind, grey light, a feeling of responsibility")
sc(184, [], "a devastated land: an empty village street with blackened walls and fallen roof beams, a stray ox cart, grey smoke, a pale sky, no people")
sc(185, ["tt60"], ONE + "Cao Cao stands on a city wall at dawn looking straight ahead at a wide plain, hands in his sleeves, a tired but resolute face, soft morning light")
sc(186, ["tt60", "quan"], "Cao Cao stands in the centre of a great hall while officials bow deeply on both sides, a wide aisle, he stands small and alone amid the bowing crowd, pillars and red cloth")
sc(187, ["tt65"], ONE + "an elderly Cao Cao seen from the chest up, in front of the grey gate-tower of a palace at dusk, a tired stern face, looking toward the viewer, hands out of frame")

# ---- tạo file
need = sorted(n for n, v in PLAN.items() if v[0] in "AB")
miss = [n for n in need if n not in S]; extra = [n for n in S if n not in need]
assert not miss and not extra, (miss, extra)
for n in need:
    nv, m = S[n]
    assert (PLAN[n][0] == "B") == (len(nv) == 0), n
canh, out = [], []
for n in need:
    nv, m = S[n]; k = f"{n:03d}"
    canh.append({"key": k, "nv": nv, "mo_ta": m})
    if nv:
        ch = "; ".join(NV[x] for x in nv)
        prompt = f"{m}. Characters (keep exactly this look): {ch}. {PHONGCACH}. {SUF}."
        it = {"key": k, "cau": n, "nv": nv, "text": BEATS[n], "prompt": prompt}
    else:
        prompt = f"Empty scenery illustration with ZERO people, no human figure anywhere in the frame: {m}. Only buildings, objects and landscape. {PHONGCACH}. {SUF}."
        it = {"key": k, "cau": n, "nv": [], "so_nguoi": 0, "text": BEATS[n], "prompt": prompt}
    out.append(it)
used = sorted({x for n in need for x in S[n][0]})
(R / "TQ9.json").write_text(json.dumps({"ma": "TQ9", "ghi_chu": "Video dài Tào Tháo thật sự ác đến mức nào, theo chính sử", "nhan_vat": {x: NV[x] for x in used}, "canh": canh}, ensure_ascii=False, indent=1), encoding="utf-8")
(R / "TQ9_anh.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
L = [len(i["prompt"]) for i in out]
print("ok", len(out), "ảnh; prompt dài nhất", max(L), "trung bình", sum(L)//len(L))
