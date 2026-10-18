"""TQ45: tập 4 gộp (tập 4 + 5 cũ), 177 cảnh (mỗi cảnh một ảnh) -> TQ45.json, TQ45_anh.json (prompt ngắn, tích cực).
Khóa ảnh = số cảnh 001..177. Mô tả cảnh viết trong SC bên dưới."""
import json
from pathlib import Path
R = Path(__file__).resolve().parent
tq = json.loads((R/"TQ.json").read_text(encoding="utf-8"))
t2 = json.loads((R/"TQ2.json").read_text(encoding="utf-8"))
t4 = json.loads((R/"TQ4_trang_phuc.json").read_text(encoding="utf-8"))
t5 = json.loads((R/"TQ5_trang_phuc.json").read_text(encoding="utf-8"))
EXTRA = {
 "linh": "a Han soldier in a plain iron helmet and leather-and-iron scale armour over a dull red-brown tunic",
 "quan": "a county official in a black cap and a dark robe",
 "kybinh": "a Wuhuan horseman in fur-trimmed leather clothes",
 "vienthuat": "Yuan Shu, a proud arrogant man of about 40 with a round pale face, a thin moustache, a rich purple-brown silk robe and a tall black cap",
 "tuong": "a Han general in his forties with a stern face, a short beard, iron scale armour over a dark robe and a plain helmet",
 "kyl": "Ji Ling, a stocky grim general of about 40 with a square jaw, a short beard, iron scale armour and a plain iron helmet",
 "nu": "a gentle noblewoman of about 30 in a pale long wrapped robe with long sleeves, hair in a bun with a wooden hairpin",
 "danvien": "an old farmer with a white beard in a hemp tunic and a straw hat",
  "vuongdoan": "Wang Yun, a lean dignified old minister of about 60 with a long thin white beard and a stern face, a tall black cap and a dark-green formal robe",
 "lai": "a courier horseman in a dust-covered travelling cloak",
 "trinhduc_cu": "a tall composed strategist in his fifties with a long neat beard and steady eyes, black cap, sober dark-grey robe",
}
NV = {**tq["nhan_vat"], **t2["nhan_vat_phu"], **t4["trang_phuc"], **t5["trang_phuc"], **EXTRA}
PK = {**t4["phu_kien"], **t5["phu_kien"]}
def short(s, n=0):
    return s
CL = {  # trang phục theo mốc cốt truyện (mã trong TQ4/TQ5_trang_phuc.json)
 "LB": lambda n: "liubei_t4c" if n<=10 else "liubei_t4a" if n<=39 else "liubei_t4b" if n<=83 else "liubei_t4c" if n<=127 else "liubei_t5a" if n<=132 else "liubei_t5b" if n<=163 else "liubei_t5c",
 "QV": lambda n: "quanvu_t4a" if n<=57 else "quanvu_t4b" if n<=127 else "quanvu_t5",
 "TP": lambda n: "trieuphi_t4a" if n<=57 else "trieuphi_t4b" if n<=127 else "trieuphi_t5",
 "LBo": lambda n: "lubo_t5a" if n<=69 else "lubo_t5b" if n<=112 else "lubo_t5c" if n<=143 else "lubo_t5d",
 "TT": lambda n: "taotao_t4" if n<=69 else "taotao_t5a" if n<=163 else "taotao_t5b",
}
WP = {"quanvu":"carrying his guandao: a very long dark-brown pole with two gold bands, a bronze dragon collar and ONE broad curved silver blade","trieuphi":"holding his serpent spear: a very long straight dark-brown pole with two gold bands and ONE straight narrow leaf-shaped silver spearhead","lubo":"holding his halberd: a long pole with a spear point and ONE crescent blade"}
SOL = "Han soldiers in plain iron helmets and scale armour over dull red-brown tunics with spears upright"
NF = "no gore, no blood, soldiers with small simple faces"
S = {}
def sc(n, nv, m): S[n] = (nv, m)

# ---- Chương 1: mở đầu (1-10)
sc(1,["daokhiem_t4a","LB"],"in a grand governor's hall of Xu Province, old Tao Qian holds out a lacquered seal box with both hands to Liu Bei, who raises his palms in refusal; officials in black caps kneel behind them, timber pillars, hanging cloth screens, clay oil lamps, theatrical light")
sc(2,["LB"],"Liu Bei stands on stone steps bowing and refusing with both hands raised while a crowd of townspeople and officials kneel in the courtyard below begging him, grey-tiled rooftops of an ancient city behind, morning light")
sc(3,["TP","tuong"],"at a feast in a Han hall Zhang Fei with a flushed face and a bronze wine cup in one hand sits on a straw mat, his serpent spear leaning on the wall beside him, a stern general facing him across a low table with a wine jar, clay oil lamps, timber pillars")
sc(4,[],"a low wooden table in a Han hall holding a lacquered seal box on one side and a clay wine jar with a bronze cup on the other, a clay oil lamp between them, timber pillars, a straw mat floor, no people")
sc(5,[],"a tall wooden shelf full of tied bamboo-slip scrolls in a Han archive room, one scroll unrolled on a low table beside a clay oil lamp, a small square window with wooden bars showing hills; the room is completely empty, absolutely no people or figures anywhere")
sc(6,["LB","mitruc_t4","tranang_t4"],"in a council room Liu Bei listens thoughtfully while a rich merchant in a silk robe and a young scholar-official speak earnestly, an open chest of bronze coins on the floor, straw mats, clay oil lamps, timber pillars")
sc(7,["LB"],"Liu Bei stands small and alone on a rocky hill at dusk looking toward a distant walled river city under a huge sky, a thoughtful question in his face, wind in his sleeves")
sc(8,[],"a wide plain seen from a hill with two dirt roads: on the northern road a small column of "+SOL+" marches toward far mountains and on the eastern road another column marches toward a river city, plain banners, soft evening light")
sc(9,["LB","linh"],"Liu Bei in a governor's robe stands on the wall of a Han river city at night with a guard, torches along the wall, dark clouds over the plain beyond, tense mood")
sc(10,["LB","QV","TP"],"the three sworn brothers stand together on a hill at dusk above a walled city: Liu Bei in the centre, Guan Yu on his left, Zhang Fei on his right, all looking out over the plain, banners in the wind")
# ---- Chương 2: Bình Nguyên (11-21)
sc(11,["LB","congtonton"],"on the gate-tower of the small walled town of Pingyuan Liu Bei stands beside his old schoolmate Gongsun Zan, both looking out over the northern plain, soldiers with spears along the wall, windy morning")
sc(12,["LB","quan"],"in the hall of Pingyuan an envoy hands Liu Bei a rolled bamboo-slip appointment, officials and guards stand along the timber walls, clay oil lamps")
sc(13,["LB","tuongquan"],"Liu Bei and the commander Tian Kai stand over a cloth map spread on a low table in an army tent, pointing north toward the enemy, officers around them, lamp light")
sc(14,[],"two armies in neat ranks face each other across a slow river on a wide plain, each a block of identical "+SOL+" with plain banners, tense still moment, no close-up faces, "+NF)
sc(15,["luubinh","LB","quan"],"in the county hall Liu Ping stands among officials glaring sourly at Liu Bei, who is greeted warmly by townsfolk at the far end of the hall, timber pillars, grey tiled roof")
sc(16,["LB","thichkhach"],"in a lamp-lit room a masked man in plain dark clothes with empty hands kneels on a straw mat before Liu Bei, confessing with bowed head, Liu Bei listening in surprise, mud-brick walls")
sc(17,["thichkhach","LB"],"at dawn the plain-clothed man walks out of the wooden gate of a Han county compound, seen from behind, while Liu Bei watches him go from the doorway, empty dirt road, hills")
sc(18,["LB","QV","TP","dan"],"in a street of Pingyuan the three sworn brothers walk side by side, Liu Bei in the centre, Guan Yu on his left, Zhang Fei on his right, townsfolk gathering around them with offerings, mud-brick houses with grey tiled roofs")
sc(19,["QV","TP","linh"],"in an army camp at dusk Guan Yu and Zhang Fei stand before separate groups of soldiers drawn up in ranks, serious faces, tents and plain banners")
sc(20,["LB","QV","TP"],"inside a canvas tent at night the three brothers lie asleep side by side under woollen blankets on a low wooden platform, Liu Bei in the middle, a clay oil lamp glowing beside them, their weapons leaning on a tent pole")
sc(21,["LB","linh"],"the small walled town of Pingyuan on a plain at dusk with Liu Bei a tiny figure on its wall, guards beside him, camp fires outside, a modest place")
# ---- Chương 3: Bắc Hải (22-29)
sc(22,["thaisutu_t4","linh"],"Taishi Ci, dusty and exhausted, dismounts from a sweating horse before the gate of Pingyuan holding a small rolled bamboo scroll, guards hurrying toward him, thin smoke on the far horizon")
sc(23,["khongdung_t4","linh"],"Kong Rong stands on the wall of the besieged city of Beihai in scholar's robes with a few guards, looking out at a vast encampment of besiegers with many small tents on the plain below, afternoon light")
sc(24,["LB","thaisutu_t4"],"in the hall of Pingyuan Liu Bei presses a hand to his chest, moved, listening to Taishi Ci who bows before him, timber pillars, clay oil lamps")
sc(25,["LB"],"Liu Bei stands alone at a small square window with wooden bars looking at hills in the evening, quiet and thoughtful, a straw mat and a clay oil lamp behind him")
sc(26,["LB","thaisutu_t4","linh"],"Liu Bei points firmly toward a block of "+SOL+" lined up before a camp and hands command to Taishi Ci, plain banners, "+NF)
sc(27,[],"a column of about forty "+SOL+" marching along a dusty road behind a plain red banner toward distant besieging tents that are being struck as the besiegers flee, seen from behind, "+NF)
sc(28,["khongdung_t4","thaisutu_t4"],"in his hall at Beihai Kong Rong sits on a straw mat smiling in relief while Taishi Ci bows before him, officials gathered, timber pillars, warm lamp light")
sc(29,["LB","linh"],"Liu Bei stands on the gate-tower of Pingyuan at dusk looking north where soldiers light watch fires along the wall, a thoughtful mood")
# ---- Chương 4: Tào Tháo & Từ Châu (30-39)
sc(30,["TT","tuong"],"in his command tent at Yanzhou Cao Cao stands before a low table with officers around him, one hand on his sword hilt, sharp ambitious gaze, plain dark banners, lamp light")
sc(31,[],"a modest family convoy on a quiet mountain road: two ox carts with luggage and an old man riding in one, a few servants walking beside, peaceful morning, green hills, no danger shown")
sc(32,[],"a night road in mist where a small convoy of carts has halted, a distant ridge with torch lights and shadowy outlines of riders, an overturned cart in the foreground, ominous mood, no victims")
sc(33,["TT","lai"],"a courier kneels before Cao Cao in his tent delivering terrible news, Cao Cao stunned and white-faced with a clenched fist, officers behind him, lamp light")
sc(34,["TT"],"Cao Cao stands alone before a plain grave mound with incense smoking at grey dawn, bare trees, soldiers kneeling in rows far behind, heavy silent grief turning to resolve")
sc(35,[],"a prosperous walled river city on a plain, busy wooden quay with merchants, porters carrying grain sacks and moored grain boats, carts on dirt streets, grey tiled roofs, bright morning")
sc(36,["TT","linh"],"Cao Cao in dark armour rides at the head of a long army marching toward a walled city on a plain, plain dark banners, dusty road, "+NF)
sc(37,[],"the army in long ranks before a walled city with thick smoke rising over its towers, plain dark banners, seen from a hill, a scene of conquest, "+NF)
sc(38,["dan"],"a long line of refugee villagers carrying bundles and pulling ox carts along a dirt road away from black smoke on the horizon, women and old people, tired and silent, seen from a distance")
sc(39,["dan"],"an empty dirt street between low mud-brick houses with grey tiled roofs, overturned wooden carts and scattered baskets, drifting dust, one old farmer reaches out a bowl of food to a passing small column of soldiers, quiet gratitude")
# ---- Chương 5: lời cầu cứu thứ hai (40-49)
sc(40,["tuongquan","quan","lai"],"in an army camp a courier hands an urgent rolled letter to the commander Tian Kai while officers gather around reading anxiously, tents and banners behind, grey morning")
sc(41,["LB","tuongquan","linh"],"Liu Bei and an army commander ride side by side at dawn at the head of a marching army, ranks of "+SOL+" behind them on a dusty road, resolute, "+NF)
sc(42,["LB","kybinh","dan","linh"],"a small modest army camp at dusk: a few tents, soldiers resting by camp fires, Wuhuan horsemen on horses at the edge, hungry peasants lined up receiving food, Liu Bei walking among them, plain banners")
sc(43,["LB","tuong","linh"],"on a muddy river bank east of a walled town a general and Liu Bei look grimly toward enemy smoke while their small force regroups with tattered banners behind them, defeat in the air, "+NF)
sc(44,["tuong"],"a stern middle-aged general in iron armour, the very man who guards the lower gate, stands on a gate-tower looking over a river city at dusk, arms folded, a quiet watchful figure to remember, torches along the wall")
sc(45,["daokhiem_t4a","LB","dan"],"at the gate of the Xu Province city old Tao Qian welcomes Liu Bei and his soldiers, townsfolk and officials cheering with relief, gate-tower behind, warm light")
sc(46,["daokhiem_t4a","LB","linh"],"Tao Qian points toward rows of "+SOL+" lined up before a camp of tents, giving four thousand troops to Liu Bei who bows in thanks, plain banners, "+NF)
sc(47,["daokhiem_t4a","LB"],"in a hall Tao Qian and Liu Bei sit side by side on straw mats sharing a quiet cup of wine, officials seated along the walls watching with respect, a low table and a clay oil lamp")
sc(48,["LB","quan","linh"],"in the camp at Xiaopei an official hands Liu Bei a small bronze seal on a ribbon cord before assembled soldiers and officers, tents and banners, morning light")
sc(49,[],"a small walled town on a plain at dusk with a few "+SOL+" standing on the wall and camp fires with resting soldiers outside the wall, plain banners, "+NF)
# ---- Chương 6: Lữ Bố chạy khỏi Trường An (50-59)
sc(50,["TT","linh"],"Cao Cao turns on the road to look back with a cold frown while a retreating column of soldiers behind him marches away with lowered plain dark banners at dusk, dusty road, "+NF)
sc(51,[],"the burned ruins of an old capital at dawn: broken walls, charred timber beams and thin smoke over a wide palace compound, empty paved courtyards, grey sky, no people")
sc(52,["vuongdoan","LBo"],"in a grand court hall Wang Yun hands a general's commission to Lu Bu, who bows slightly in iron armour, officials in black caps standing along the pillars, clay oil lamps, formal moment")
sc(53,["LBo","linh"],"Lu Bu stands uneasy on a palace terrace looking out at a distant dark crowd of Liangzhou soldiers gathering outside the city walls under a stormy sky, a few guards behind him")
sc(54,["linh"],"two armies face each other on a plain before the walls of Chang'an, one in rows of "+SOL+" and the other a mass of horsemen with plain banners, a single rider in the gap between them, tense, "+NF)
sc(55,["LBo","linh"],"Lu Bu on a horse retreats from a wall under smoke while enemy soldiers pour in through a far gate, his small band behind him, seen from a distance, "+NF)
sc(56,["LBo","linh"],"Lu Bu rides with a few hundred riders through a mountain pass at dusk toward a distant gate in a hill wall, banners lowered, dust")
sc(57,["vienthuat","LBo"],"in a hall of Shouchun Yuan Shu turns his head away with cold distaste and a raised hand, refusing, while Lu Bu stands before him with a stiff proud face, officials watching, clay oil lamps")
sc(58,["LBo"],"Lu Bu stands alone in the dusk on an empty dirt road at the gate of a city that has shut its doors, his horse beside him, shoulders lowered, grey tiled walls")
sc(59,["LBo","linh"],"Lu Bu and a handful of riders turn their horses north along a wide empty road toward distant hills at sunrise, seen from behind and from the side, determined")
# ---- Chương 7: Xích Thố (60-69)
sc(60,["vienthieu","LBo","linh"],"on a hill Yuan Shao and Lu Bu ride side by side looking down at a huge army camp in the plain below, tents and plain banners, riders massing at the foot of the hills")
sc(61,["LBo"],"Lu Bu on his great red horse Red Hare, a magnificent crimson-red horse, rides at a gallop across an open plain with his halberd upright, dust and wind, hills behind")
sc(62,["LBo","linh"],"Lu Bu on his red horse leads a small band of riders charging into a mass of enemy horsemen, spears lowered, dust clouds, banners, the enemy scattering, no one struck, "+NF)
sc(63,["vienthieu","LBo","linh"],"in a camp tent Yuan Shao sits tense watching through the tent flap as Lu Bu's undisciplined soldiers scatter among the villages, carts and bundles on the road outside, grey light")
sc(64,["vienthieu","lai"],"at night in Yuan Shao's tent, Yuan Shao in a deep-blue robe whispers orders to several shadowed men in dark clothes with empty hands, a single clay oil lamp, long shadows")
sc(65,[],"an empty army tent at night with a low table holding a zither (guqin) and a clay oil lamp, straw mats and blankets laid out, a quiet moment, no people")
sc(66,[],"an army tent at night with a rumpled bed of straw mats and blankets by a clay oil lamp, tent flaps ajar and torchlight outside, shadows of soldiers on the canvas wall, nothing violent shown")
sc(67,["vienthieu","linh"],"at dawn Yuan Shao stands on the wall above a gate that soldiers are closing and barring, his face grim, soldiers on the wall, the road empty below")
sc(68,["LBo","linh"],"Lu Bu and a few riders ride along a river road while a distant pursuing troop hangs back, hesitating; the pursuers keep their distance from him, dust, hills")
sc(69,["LBo"],"Lu Bu sits alone on a rock at the edge of a camp at dusk with his halberd across his knees, a lonely powerful figure, camp fires and tents far behind him")
# ---- Chương 8: Trương Mạc (70-79)
sc(70,["TT","truongmac_t5"],"in a hall of Yanzhou Cao Cao and Zhang Miao sit facing each other on straw mats as old friends, warm trust, Cao Cao clasping Zhang Miao's forearm, timber pillars, clay oil lamps")
sc(71,["TT","truongmac_t5"],"Cao Cao in dark armour, about to depart, speaks quietly to Zhang Miao at a courtyard gate, family members in plain robes standing back, the army waiting outside the gate")
sc(72,["TT","truongmac_t5"],"Cao Cao and Zhang Miao stand in a hall with tears in their eyes, then Zhang Miao turns aside with a troubled look and a hand on his sleeve, an unspoken worry, lamp light")
sc(73,["tranchung_t5","truongmac_t5"],"at night in a quiet room Chen Gong and Zhang Miao and one more official lean over a low table whispering secretly, a single clay oil lamp, long shadows on the mud-brick wall")
sc(74,["tranchung_t5","truongmac_t5"],"Chen Gong, calm and sharp, points to a cloth map on a low table showing Yanzhou while Zhang Miao listens, a few officials behind, lamp light")
sc(75,["tranchung_t5","truongmac_t5"],"Chen Gong speaks with one hand raised and a persuasive look to a thoughtful Zhang Miao, a clay oil lamp, timber pillars, officials listening in the shadows")
sc(76,["truongmac_t5","LBo","tranchung_t5"],"Zhang Miao and Chen Gong welcome Lu Bu in his dusty armour at the gate of Yanzhou, soldiers and townspeople lining both sides of the road, banners, welcoming crowd")
sc(77,["linh"],"three small walled towns on a flat plain seen from above, each with a plain banner and soldiers on the wall, while the rest of the plain is dotted with other towns under a different banner, strategic map-like view, "+NF)
sc(78,["TT","linh"],"Cao Cao turns back at the head of his army on a road leading toward Yanzhou, the army wheeling around, resolute, banners in the wind, dusty road, "+NF)
sc(79,["dan","linh"],"on the wall of the Xu Province city townsfolk and soldiers watch with relief as the distant army withdraws along the road toward misty hills, the gate-tower open, calm morning")
# ---- Chương 9: Lời trăn trối (80-84)
sc(80,["daokhiem_t4b","mitruc_t4"],"old Tao Qian lies frail and pale on a low wooden platform under a blanket, Mi Zhu kneels beside him and a physician in dark robes waits, dim lamp light, curtains, a bowl of medicine, no death shown")
sc(81,["mitruc_t4","dan"],"in an ancient storeroom Mi Zhu stands among stacked grain sacks, bolts of silk, bronze coins in chests and many servants and workers, the wealth of a merchant clan, light from small clay oil lamps")
sc(82,["daokhiem_t4b","mitruc_t4"],"Tao Qian whispers his last wish to Mi Zhu who bends close to listen, dim lamp light, curtains, a few attendants standing back in the shadows")
sc(83,["mitruc_t4","tranang_t4","quan"],"officials of Xu Province stand together in a hall, quiet and worried, looking at an empty low wooden platform where the old governor used to lie, lamp light, nobody speaks")
sc(84,["mitruc_t4","LB","dan","linh"],"Mi Zhu leads a delegation of officials and townspeople to the camp at Xiaopei and bows before a startled Liu Bei who raises both hands in refusal, soldiers watching, tents and banners, dusty light")
# ---- Chương 10: Những người khuyên (85-92)
sc(85,["tranang_t4","LB","quan"],"Chen Deng speaks earnestly to Liu Bei with one hand raised in a hall, several elders and officials of Xu Province listening behind him, lamp light, persuasive mood")
sc(86,["LB","tranang_t4"],"Liu Bei, with a raised hand toward the south, argues his case with Chen Deng across a low table, other officials around them in a council, timber pillars, clay oil lamps")
sc(87,["tranang_t4","khongdung_t4"],"Chen Deng shakes his head firmly, and beside him Kong Rong in scholar's robes stands with a small retinue, both urging; elders behind them, hall with timber pillars")
sc(88,["khongdung_t4","LB","linh"],"Kong Rong, refined and firm, arrives at the camp with a small retinue of horsemen and urges Liu Bei to accept the province, gesturing toward the city behind them, afternoon light")
sc(89,["LB","mitruc_t4","tranang_t4","dan","linh"],"Liu Bei bows slightly in acceptance with his hands joined before the city gate, officials and townspeople around him cheering and bowing, soldiers lined up with plain banners, dawn light")
sc(90,["mitruc_t4","tranang_t4","khongdung_t4"],"three men stand together under torchlight at a city gate at night welcoming Liu Bei: a rich merchant, a young scholar-official and a famous scholar, warm light, stars above")
sc(91,["mitruc_t4","tranang_t4","khongdung_t4"],"the same three civilians, a rich merchant, an official and a scholar, stand in a hall with no weapon among them while behind them in a courtyard a few armed soldiers wait at a distance, to show they are not soldiers, lamp light")
sc(92,["LB","mitruc_t4","dan"],"in an ancient storeroom Mi Zhu opens a heavy wooden chest of old bronze coins for Liu Bei while servants carry bolts of silk and clay jars, light from small clay oil lamps")
# ---- Chương 11: Ba lần nhường hay tính toán (93-105)
sc(93,["LB","quan","linh"],"Liu Bei in his governor's robe stands at the top of the stone steps of the city hall looking over the city, officials bowing and guards standing at attention below, grey tiled roofs behind")
sc(94,[],"the stone gate of a Han government compound with plain timber pillars and a grey tiled roof, a bronze seal on a low wooden stand before the gate, a courtyard with paving stones; the courtyard is completely empty, absolutely no people or figures anywhere")
sc(95,["daokhiem_t4a","LB"],"a stage-like scene of the novel: old Tao Qian kneels offering a seal box while Liu Bei refuses with both palms raised, a ring of kneeling townspeople, grand hall, dramatic light")
sc(96,["LB","tranang_t4","khongdung_t4"],"Liu Bei listens carefully with a hand at his chin while Chen Deng and Kong Rong advise him in a council hall, timber pillars, clay oil lamps")
sc(97,["LB","mitruc_t4","tranang_t4"],"at a low table Liu Bei, Mi Zhu and Chen Deng weigh a plan, a cloth map spread out and bronze coins stacked beside it, practical faces, lamp light")
sc(98,["TT","LBo"],"two armies far apart on two plains seen from a hill: on one a dark banner column of Cao Cao turning back, on the other riders of Lu Bu holding a walled town, plain banners, evening light")
sc(99,[],"a pair of balance scales on a low table in a Han hall, a heap of bronze coins on one pan and a folded robe and a seal on the other, balanced, clay oil lamp, no people")
sc(100,["LB"],"Liu Bei in a plain robe sits on a straw mat at a low table in a quiet room, an ordinary thoughtful man rather than a saint, clay oil lamp and bamboo-slip scrolls beside him")
sc(101,["LB","QV","TP"],"in his early thirties Liu Bei rides at the head of a small army across a plain at golden hour, Guan Yu on his left and Zhang Fei on his right, soldiers and banners behind, a distant walled city")
sc(102,["LB","quan"],"a younger Liu Bei in plain dark clothes and a cloth cap stands before a small county gate with a junior-official's duties, village houses behind, a modest early-career scene")
sc(103,["LB","dan"],"Liu Bei, with a bundle on his back, walks away from a government building down a dusty road past villagers, a quiet fall from office, grey tiled roofs behind")
sc(104,["LB","QV","TP"],"three small travellers, Liu Bei in the centre, Guan Yu on the left and Zhang Fei on the right, walk side by side on a long winding dirt road across wide hills toward a river city, tiny in a vast landscape, golden light")
sc(105,[],"a long dirt road winding from a small county gate through hills and rivers to a distant great walled city, the road drawn as a golden thread, early morning light; completely empty landscape, absolutely no people or figures anywhere")
# ---- Chương 12: Món quà có độc (106-112)
sc(106,["TT","linh"],"Cao Cao stands on a hilltop at dusk with his arm pointing toward a far-off rich river city on the horizon, a grim cold look, his banners behind him")
sc(107,["vienthuat","linh"],"a tall proud southern walled city, Shouchun, with a grand gate-tower, soldiers on the wall and a plain banner above rice fields, grey sky, a robed Yuan Shu watching from its tower, "+NF)
sc(108,["quan","mitruc_t4","tranang_t4"],"in a dim hall corridor with timber pillars two or three officials of Xu Province whisper together glancing toward an inner door, long shadows, a small clay oil lamp on the floor")
sc(109,["LB","QV","TP","linh"],"Liu Bei stands on a stone city wall at dusk looking around at the four directions, worried, Guan Yu on his left and Zhang Fei on his right, soldiers keeping watch along the wall, plain banners")
sc(110,["kybinh","linh"],"four dirt roads meeting at an ancient city gate under a darkening sky, small groups of riders approaching along each of the four roads, threatening mood, "+NF)
sc(111,[],"a lacquered gift box with a gold clasp stands open on a low table in a hall, dark mist curling from it, and in the mist behind it the faint outlines of two armies, one in the north and one in the south")
sc(112,["LB"],"a rich walled river city at night seen from a hill, its walls glowing with torches, and one dark silent corner of the wall in shadow where no one is watching, Liu Bei tiny on a far hill gazing at the bright side")
# ---- Chương 13: Kết cục Duyện Châu (113-121)
sc(113,["TT","LBo"],"two armies face each other across a wide river plain at Yanzhou for many days, Cao Cao's dark banners on one bank and Lu Bu's riders on the other, tents and smoke from camp fires, heavy summer haze")
sc(114,["TT"],"Cao Cao on horseback seen from a distance galloping through a corridor of flames and dust, his cloak flying, thick smoke, no injury shown")
sc(115,[],"dry cracked fields under a harsh sun with swarms of locusts darkening the sky over withered grain and an empty village gate, parched earth, a distant town wall, no people")
sc(116,["TT","vienthieu","lai"],"in Cao Cao's tent Cao Cao sits tired while an envoy of Yuan Shao in a deep-blue robe offers a rolled message, an almost empty grain jar behind, lamp light")
sc(117,["TT","trinhduc_t5"],"Cheng Yu stands before Cao Cao in a tent with a hand raised firmly against the offer, Cao Cao listening and slowly nodding, lamp light, strategic tension")
sc(118,["TT","linh"],"the army of Cao Cao surrounds a hill fortress town named Yongqiu on a plain, ranks of soldiers and plain dark banners around its walls, siege ladders at rest, smoke, "+NF)
sc(119,["truongmac_t5","linh"],"Zhang Miao rides out of a camp gate at night with a small escort heading south, a worried face under a torch, dark road, hills")
sc(120,["LBo","linh"],"Lu Bu and a band of riders gallop east along a wide dirt road at dawn toward the distant walls of Xu Province, his red horse in front, dust, banners lowered")
sc(121,["LBo","linh"],"Lu Bu on his red horse sits waiting before the gate of a Han city at dusk, guards looking down from the tower in uncertainty, torches, his face weary")
# ---- Chương 14: Người cho nương nhờ (122-127)
sc(122,["LBo","LB"],"Lu Bu in his weathered armour bows his head respectfully to Liu Bei at the gate of a Han city, a few riders behind him, Liu Bei standing calmly with polite hands joined, evening light")
sc(123,["LBo","LB"],"in a hall Lu Bu sits across from Liu Bei on straw mats telling his tale with expressive hands, a clay oil lamp and a low table with cups between them, timber pillars")
sc(124,["LBo","LB","nu"],"inside a tent Lu Bu has Liu Bei sit on the bed of Lu Bu's wife, who bows gracefully and pours wine from a clay jar, Lu Bu smiling broadly, a low wooden platform with straw mats and blankets, lamp light")
sc(125,["LB"],"Liu Bei sits composed on a straw mat with a polite smile on his lips but a troubled look in his eyes, a clay wine cup untouched in front of him, lamp light")
sc(126,["LB","QV","TP"],"Liu Bei in the centre, Guan Yu on his left and Zhang Fei on his right, stand on the gate-tower looking at a distant camp of strangers beyond the walls, uneasy, soldiers on the wall")
sc(127,["LB","LBo"],"inside a Han city courtyard Liu Bei stands calmly at the left while Lu Bu, in cleaner armour with his halberd, stands confidently at the right as the real master of the house, plain blank dark banners behind, a single frame, no banner text")
# ---- Chương 15: Hạ Bì (128-143)
sc(128,["TT","LB","quan"],"in a hall Cao Cao's envoy presents Liu Bei with a ribbon cord and a bronze seal of Zhendong General, officials watching, lamp light, a formal moment")
sc(129,["LB","vienthuat","linh"],"Liu Bei's army in ranks faces Yuan Shu's army across a stream at Huai Yin, two blocks of soldiers with plain banners in a river valley, Liu Bei on a rock with a commander, "+NF)
sc(130,["tuong"],"a general in iron armour stands alone on the gate-tower of the walled city of Xiapi at night guarding the rear, torches along the wall, the vast river plain behind, a quiet, uneasy watch")
sc(131,["TP","tuong"],"at a feast in the hall of Xiapi Zhang Fei with a flushed face holds a bronze cup high, his serpent spear leaning on the wall, while a stern general frowns at him across a low table with a wine jar, clay oil lamps, the novel's famous scene")
sc(132,["LBo","linh"],"Lu Bu on his red horse leads cavalry toward the dark gate of a river city at night, his halberd upright, torches flickering on the gate-tower, the gate slowly opening")
sc(133,["LB","linh"],"Liu Bei retreats with his column of weary soldiers along a river bank at dawn, banners lowered, mist on the water, a distant city behind them")
sc(134,["tranang_t4"],"a rolled bamboo-slip scroll tied with cord lies on a low table in a quiet room with a clay oil lamp and a small square barred window, a line of old scrolls on a shelf, no people")
sc(135,["tuong","lai","TP"],"at night a secret courier in a dark cloak hands a message to a general in a lamp-lit tent while Zhang Fei stands a short way off in the doorway, long shadows")
sc(136,["vienthuat","LBo"],"Yuan Shu in his hall writes a letter on a bamboo-slip scroll with a brush while a courier waits holding out his hands, a clay oil lamp, timber pillars, a plan being made")
sc(137,["linh"],"a thousand soldiers in iron helmets crowd inside the west gate of a white-walled city at night, torches in their hands, listening, some looking up at the gate bar, tense but orderly, "+NF)
sc(138,["LBo","linh"],"at dawn Lu Bu's riders reach the foot of the city wall in a long column on a dusty road, the gates swinging wide open before them, soldiers at the gates, "+NF)
sc(139,["LBo","linh"],"Lu Bu sits on the top of the gate-tower while his cavalry gallops through the open gates with torches, flames and smoke rising over the city wall behind, banners, no one struck, "+NF)
sc(140,["TP","linh"],"Zhang Fei with his serpent spear stands in the night street of Xiapi among a few of his soldiers looking toward the gate, smoke and torchlight, a troubled expression")
sc(141,[],"a lacquered wine jar tipped on its side beside a bronze cup on a low table, wine spilled on the straw mat, a clay oil lamp, an empty hall, a novel's invented cause shown as an overturned cup, no people")
sc(142,["linh"],"a column of four thousand soldiers in iron helmets with spears and plain banners marching through a river gate, seen from behind, mist, hills, a thought about where soldiers come from, "+NF)
sc(143,["linh"],"a river city caught between two grey armies: on the left a block of soldiers with plain banners, on the right another block, and in the middle the city with its gate standing open from inside, seen from a hill, "+NF)
# ---- Chương 16: Cầu hòa (144-151)
sc(144,["LB","LBo"],"Liu Bei stands before Lu Bu in a hall with hands joined asking for peace, a woman and child in plain robes standing safely behind Liu Bei, Lu Bu seated on a platform nodding, timber pillars")
sc(145,["LBo","LB","linh"],"Lu Bu in a general's robe stands on a hall step as the new lord of Xu Province while a humble Liu Bei with a few soldiers marches out of the gate toward a small town in the distance, banners, morning light")
sc(146,["LB","LBo"],"Liu Bei standing outside a small town gate of Xiaopei looking back toward the big city where Lu Bu's banner flies, wry resignation on his face, a roads and hills at dusk")
sc(147,["vienthuat","lai"],"a courier on a horse carries a sealed bamboo-slip letter along a river road toward a walled city, a long dirt road with hills behind, dawn light")
sc(148,[],"a bamboo-slip letter unrolled on a low table with a brush and an ink stone beside it, a clay oil lamp, three small clay pots arranged in a row on the table for three achievements, no people, no writing visible")
sc(149,["vienthuat","LBo","lai"],"Yuan Shu in his hall points proudly toward the north while the courier bows, a heap of grain sacks piled at the hall door, officials standing along the wall, clay oil lamps, a tempting bargain")
sc(150,["vienthuat"],"Yuan Shu stands proudly in a storehouse yard in front of a tall stack of grain sacks, pointing a finger forward with a satisfied look, plain blank sacks, a single full-frame picture, no panels, no border")
sc(151,["vienthuat","LB"],"in one frame the proud Yuan Shu in the foreground waves a hand dismissively with a smirk, and far behind him in the background small Liu Bei stands humbly at a gate, a single full-frame picture, no panels, no border")
# ---- Chương 17: Bắn kích (152-162)
sc(152,["kyl","linh"],"Ji Ling at the head of a vast army of thirty thousand foot soldiers and cavalry marches across a plain toward a small walled town, plain banners in the wind, "+NF)
sc(153,["LBo","tuong"],"in Lu Bu's tent officers lean toward Lu Bu whispering with sly looks and Lu Bu shakes his head, a clay oil lamp, tent poles")
sc(154,["LBo"],"Lu Bu stands before a cloth map on a low table in a tent pointing at his own position surrounded by arrows pointing in from north and south, a calculating look, lamp light")
sc(155,["LBo","linh"],"Lu Bu on his red horse leads a thousand foot soldiers and two hundred riders along a road toward a small walled town, halberd upright, dust, banners, "+NF)
sc(156,["kyl","LBo"],"at a camp southwest of the little town Lu Bu hosts Ji Ling at a low table with cups and food, both seated on straw mats with smiles, a clay oil lamp, tent walls")
sc(157,["LBo","kyl"],"Lu Bu stands holding a cup and speaks with open hands to the seated Ji Ling and his officers, a friendly but commanding stance, lamp light, tent walls")
sc(158,["LBo","linh"],"at the camp gate soldiers plant a tall halberd upright in the ground, its small side-blade visible, Lu Bu pointing at it from some distance with a bow in one hand while generals stand watching, camp tents and banners")
sc(159,["LBo","kyl","linh"],"Lu Bu draws a great bow aiming at the halberd planted at the camp gate while the camp watches, generals' faces amazed, tents and banners, dramatic stillness before the shot")
sc(160,["LBo","kyl"],"the next day Lu Bu and Ji Ling feast together again with cups, then the armies depart on two roads, banners lowered, peaceful dusk")
sc(161,[],"a tall halberd standing in the dirt at an army camp gate with a bow lying at its foot, a lone symbol of a famous tale, torch light fading at dusk, no people")
sc(162,["LBo","LB"],"a scene of cold calculation: Lu Bu watches Liu Bei bowing his thanks from a distance with a faint calculating smile, Liu Bei bowing politely at a town gate, evening light")
# ---- Chương 18: Chạy sang Tào (163-166)
sc(163,["LB","linh"],"in the small town of Xiaopei Liu Bei reviews a growing army of over ten thousand soldiers drawn up in ranks before him, banners and spears, a hopeful commander, morning light, "+NF)
sc(164,["LB","TT","linh"],"Cao Cao welcomes Liu Bei warmly at a camp gate, hands joined, with soldiers lined up and a gift of grain carts behind them, lamp-lit tents, a seal on a ribbon cord")
sc(165,["trinhduc_t5","TT"],"Cheng Yu speaks earnestly in low tones to Cao Cao in a tent, one hand lifted toward the east, Cao Cao listening with a thoughtful face, lamp light")
sc(166,["TT"],"Cao Cao shakes his head slowly, a calm commanding look, hand resting on a low table, one clay oil lamp, tent walls, heroes to be gathered")
# ---- Chương 19: Lời kết (167-177)
sc(167,["LB"],"Liu Bei stands on a hill at dawn with a calm clear face looking toward a golden horizon, no kneeling crowd, an honest ordinary man's view")
sc(168,[],"a wide plain seen from a hill with two roads: on the northern road a small column of "+SOL+" marches toward Beihai and on the eastern road another column marches toward Xu Province, the two rescues in one picture, soft morning light, "+NF)
sc(169,["LBo"],"a city gate standing open at night in a river city, torchlight inside, a shadowy rider with a halberd in the dark road outside, a quiet moment, no wine jar, only a gate and an enemy")
sc(170,["LBo","LB"],"Lu Bu in his fine armour sits on the top step of a hall in Xiapi while Liu Bei stands below at a humble distance with hands joined, a grim irony, grey tiled roofs")
sc(171,[],"a lacquered seal box and a clay wine jar side by side on a low table with a clay oil lamp, one of the stage props of a novel, dramatic light, timber pillars, no people")
sc(172,[],"a Han river city with a gate marked by nothing but its three dangers: a banner on a hill to the south, one on a hill to the north, and a small lit house inside the walls, evening light, quiet, no people")
sc(173,["LB","TT","linh"],"Liu Bei rides through the gate of Cao Cao's camp with a few weary soldiers, Cao Cao standing at the gate in dark armour to greet him, tents and banners, dusk")
sc(174,["TT","hiende","linh"],"Cao Cao in a dark cap and cloak walks beside a small procession escorting the young Emperor Xian in a covered cart along a dirt road past ruined walls of Luoyang toward the east, soldiers with plain banners, dawn light")
sc(175,[],"an ancestral temple of the Han with timber pillars and a grey tiled roof, ritual bronze vessels on a stone altar in the courtyard, incense smoking, a calm restored order, morning light, no people")
sc(176,["TT","LB"],"Cao Cao and Liu Bei sit across from each other at a low table in a lamp-lit hall, cups of wine between them, both polite and watchful, officials along the walls")
sc(177,["LB","QV","TP"],"Liu Bei in the centre, Guan Yu on his left, Zhang Fei on his right, stand at a city gate at dusk looking toward a distant glowing capital, banners in the wind, quiet resolve")

assert sorted(S) == list(range(1,178)), [i for i in range(1,178) if i not in S]
TRIO = {n for n,(nv,_) in S.items() if {"LB","QV","TP"} <= set(nv)}
HAN2 = ("Setting: Eastern Han China, year 194, plain and rustic. Buildings: thick rammed-earth and grey-brick walls, low heavy grey-tile roofs with a straight ridge and gently sloping eaves, huge red-brown timber pillars, bare unpainted walls, plain bamboo blinds, tiny square windows with a few vertical bars, straw mats and low wooden tables. "
        "Clothing: crossed-collar wide-sleeved robes (right lapel over left) tied with a cloth sash, officials in black gauze caps, soldiers in leather-and-iron scale armour with pointed-top iron caps and neck guards (never round modern helmets, never green army uniforms), cloth shoes or boots. "
        "Every banner, wall, screen and scroll is completely blank plain cloth with no marks. Light only from torches or small clay oil lamps on tables, no hanging lanterns. Nobody holds a bare blade unless the story says so; a sword at the hip is fully in its scabbard. "
        "2D ligne claire comic illustration, clean dark outlines, flat muted earthy colours. A rich detailed background fills the whole wide frame with several people and objects at different depths; every person stands or sits upright with head up, exactly two arms, two hands and two legs, and every face is different. No text, no letters, no frame or border, not a photo, not 3D.")
HAN2S = ("Eastern Han China, plain rustic: grey-brick and rammed-earth walls, low heavy grey-tile roofs with straight ridges and gently sloping eaves, big timber pillars, bare blank walls, tiny square windows with a few vertical bars and no glass, straw mats, low tables, clay oil lamps and torches only (no hanging lanterns, no candles, no chairs). "
 "Crossed-collar wide-sleeved robes, black caps, scale armour with pointed iron caps. All banners, scrolls, walls and signs are blank, no text anywhere. Nobody holds a drawn blade; any sword at a hip is hidden in its scabbard. Gate plaques, hanging banners and cloths are plain blank. "
 "2D ligne claire comic illustration, clean dark outlines, flat muted colours, rich detailed background, every person upright with exactly two arms, two hands and two legs, all faces different.")
STYLE = HAN2S
REFD = R/"refs"
def refs_for(keys):
    names=[]
    for k in keys:
        if k.startswith("liubei"): names.append("liubei")
        elif k.startswith("quanvu"): names.append("quanvu")
        elif k.startswith("trieuphi"): names.append("trieuphi")
        elif k.startswith("lubo"): names.append("lubo_cd")
        elif k.startswith("vienthieu"): names.append("vienthieu")
        elif k=="vienthuat": names.append("vienthuat")
    if {"liubei","quanvu","trieuphi"} <= set(names): return []
    return [n for n in dict.fromkeys(names) if (REFD/f"{n}.jpg").exists()][:2]
RN={"liubei":"Liu Bei","quanvu":"Guan Yu","trieuphi":"Zhang Fei","lubo_cd":"Lu Bu","vienthieu":"Yuan Shao","vienthuat":"Yuan Shu"}
def RG(rf):
    if not rf: return ""
    return "Reference image(s) show the face, hair and beard of "+" and ".join(RN[x] for x in rf)+": keep those faces exactly, but follow the costume, pose and scene written here, and draw everyone else with different faces. "
canh,out=[],[]
for n in range(1,178):
    nv,m=S[n]
    keys=[CL[x](n) if x in CL else x for x in nv]
    descs=[]
    for k in keys:
        d=short(NV[k])
        for pre,w in WP.items():
            if k.startswith(pre): d+=", "+w
        if k.startswith("liubei") or k.startswith("taotao"): d+=", empty hands, no weapon"
        if k=="liubei_t5a" and n>=128: d+=", "+PK["an_tran_dong"]
        if k=="liubei_t5c" and n>=164: d+=", "+PK["an_du_chau_muc"]
        if k=="lubo_t5d": d+=", "+PK["dai_tu_chau_thu_su"]
        descs.append(d)
    if n in TRIO:
        pos={"liubei":"CENTRE","quanvu":"LEFT","trieuphi":"RIGHT"}
        order=sorted(range(len(keys)),key=lambda i:{"LEFT":0,"CENTRE":1,"RIGHT":2}.get(pos.get(keys[i].split("_")[0]),3))
        descs=[(pos[keys[i].split("_")[0]]+" of the three: " if keys[i].split("_")[0] in pos else "")+descs[i] for i in order]
        m+=", Liu Bei is exactly in the centre between Guan Yu on his left and Zhang Fei on his right"
    canh.append({"key":f"{n:03d}","nv":keys,"mo_ta":m})
    rf=refs_for(keys)
    ch=(" Characters: "+"; ".join(descs)+".") if descs else " An empty quiet scene of objects and landscape only."
    out.append({"key":f"{n:03d}","nv":keys,"refs":rf,"prompt":f"{m}.{ch} {RG(rf)}{STYLE}"})
(R/"TQ45.json").write_text(json.dumps({"ma":"TQ45","canh":canh},ensure_ascii=False,indent=1),encoding="utf-8")
(R/"TQ45_anh.json").write_text(json.dumps(out,ensure_ascii=False,indent=1),encoding="utf-8")
L=[len(o["prompt"]) for o in out]
print("ok",len(out),"ảnh; prompt dài tối đa",max(L),"trung bình",sum(L)//len(L),"; trio",sorted(TRIO))
