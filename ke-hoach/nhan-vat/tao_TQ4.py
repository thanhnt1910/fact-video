"""Tạo TQ4.json (cảnh) và TQ4_anh.json (86 prompt vẽ) cho tập 4. Khóa ảnh = số câu lời kể (001...086), mỗi ảnh dùng một lần.
Quy tắc ảnh (17/10): KHÔNG giới hạn số người, KHÔNG ép nửa người; cảnh vẽ theo đúng cốt truyện (binh lính, đám đông, hậu cảnh);
ảnh nào cũng có nền; không vật hiện đại; không vẽ cảnh máu me. Trang phục theo mã trong TQ4_trang_phuc.json."""
import json
from pathlib import Path
R = Path(__file__).resolve().parent
tq = json.loads((R / "TQ.json").read_text(encoding="utf-8"))
t2 = json.loads((R / "TQ2.json").read_text(encoding="utf-8"))
tp = json.loads((R / "TQ4_trang_phuc.json").read_text(encoding="utf-8"))
EXTRA = {
 "linh": "a Han soldier in a plain iron helmet and leather-and-iron scale armour over a dull red-brown tunic",
 "quan": "a county official in a black cap and a dark robe",
 "kybinh": "a Wuhuan horseman in fur-trimmed leather clothes",
}
NV = {**tq["nhan_vat"], **t2["nhan_vat_phu"], **tp["trang_phuc"], **EXTRA}

# Vũ khí theo truyện (luôn kèm theo nhân vật)
WP = {
 "quanvu": ", always carrying his signature weapon the Green Dragon Crescent Blade (Qinglong Yanyue dao): a very long wooden pole with a large single broad curved crescent-shaped blade at the top, held upright beside him or in his hands",
 "trieuphi": ", always carrying his signature weapon the serpent spear (zhangba shemao): a very long spear whose steel head is a narrow wavy snake-like blade, held upright beside him or in his hands",
 "liubei": ", wearing his pair of straight double-edged swords (shuangu jian) sheathed at his belt, one on each hip",
 "lubo": ", carrying his signature weapon the Sky Piercer halberd (Fangtian Huaji): a long pole with a spear point and a crescent blade on one side",
 "taotao": ", a sheathed straight sword at his waist",
 "thaisutu": ", a bow and quiver on his back and a long halberd in hand",
}
for _k in list(NV):
    for _p, _t in WP.items():
        if _k.startswith(_p) and _p in ("quanvu","trieuphi","liubei","lubo","taotao","thaisutu"):
            NV[_k] = NV[_k] + _t
PK = tp["phu_kien"]
STYLE = tq["phong_cach"].replace("year 184 AD", "year 193 AD")
OLD = json.loads(Path("/tmp/old_canh.json").read_text(encoding="utf-8")) if Path("/tmp/old_canh.json").exists() else {}

LB = lambda i: "liubei_t4a" if i <= 33 else ("liubei_t4b" if i <= 57 else "liubei_t4c")
QV = lambda i: "quanvu_t4a" if i <= 57 else "quanvu_t4b"
TP = lambda i: "trieuphi_t4a" if i <= 57 else "trieuphi_t4b"
SOL = "Han soldiers in plain iron helmets and leather-and-iron scale armour over dull red-brown tunics, spears upright"
NF = "no gore, no blood, no one being struck or killed, soldiers with small simple faces"
KEEP = ["003","004","006","014","050","058","059","062","063","066","068","071","074","086"]
G = "guards" # chỉ để đọc

S = {}
def sc(i, nv, m): S[i] = (nv, m)

sc(1,["daokhiem_t4a","liubei_t4c"],"in a grand governor's hall of Xu Province, old Tao Qian holds out a lacquered seal box with both hands to Liu Bei, who raises his palms in refusal; rows of officials in black caps kneel behind them, wooden pillars, hanging cloth screens, oil lamps, theatrical dramatic light")
sc(2,["liubei_t4c"],"Liu Bei stands on the stone steps of a hall bowing and refusing with both hands raised, while a crowd of townspeople and officials kneel in the courtyard below begging him to accept, grey tiled rooftops of an ancient city behind, morning light, the dramatic stage-like scene of the novel")
sc(5,[LB(5) if False else "liubei_t4a"],"seen from a high hill, a wide plain with two roads: on the northern road a small column of soldiers marches toward distant mountains and on the eastern road another column marches toward a river city, plain banners, evening light, Liu Bei small in the foreground on a rock looking over both roads with his back to us")
sc(7,["liubei_t4a","linh"],"Liu Bei in a dark-blue robe and black cloth cap stands on the gate-tower of the small walled town of Pingyuan looking out over the northern plain, two guards beside him and soldiers with spears along the wall, plain banners, windy morning")
sc(8,["liubei_t4a","quan"],"inside the hall of Pingyuan an envoy of Gongsun Zan hands Liu Bei a rolled bamboo-slip appointment, officials and guards standing along the walls, wooden pillars and oil lamps")
sc(9,["linh"],"a wide plain seen from a hill: two armies in neat ranks face each other across a slow river, each army a block of many identical "+SOL+" with long spears and plain banners, no single soldier in the foreground, no close-up faces, every soldier has exactly one head, still tense moment before a battle, "+NF)
sc(10,["liubei_t4a","quanvu_t4a","trieuphi_t4a"],"inside a canvas army tent at night Liu Bei sits on a straw mat beside an oil lamp, tired and thoughtful, while Guan Yu and Zhang Fei stand guard at the open tent flap as dark silhouettes against the camp fires outside, an iron armour on a wooden stand, Composition: Liu Bei stands in the exact centre of the frame between the two, Guan Yu on his left and Zhang Fei on his right, Liu Bei the main figure.")
sc(11,["luubinh","liubei_t4a","quan"],"in the county hall Liu Ping stands among officials looking sourly at Liu Bei who is greeted warmly by townsfolk at the far end of the hall, wooden pillars, tiled roof, morning light, tension of jealousy")
sc(12,["liubei_t4a","thichkhach","quanvu_t4a","trieuphi_t4a"],"in a lamp-lit room the masked guest in plain dark clothes kneels on a straw mat before Liu Bei, bowing his head and confessing, empty hands, while Liu Bei listens in surprise and Guan Yu and Zhang Fei stand watchful behind Liu Bei, wooden walls and lattice window, Composition: Liu Bei stands in the exact centre of the frame between the two, Guan Yu on his left and Zhang Fei on his right, Liu Bei the main figure.")
sc(13,["liubei_t4a","dan"],"in a street of Pingyuan Liu Bei greets a crowd of grateful townspeople and peasants who gather around him with offerings of food, a kind calm smile, mud-brick houses with grey tiled roofs, warm morning light")
sc(15,["thaisutu_t4","linh"],"Taishi Ci, dusty and exhausted, dismounts from a sweating horse before the gate of Pingyuan holding a small rolled bamboo scroll, urgent expression, guards in armour hurrying toward him, thin smoke on the far horizon")
sc(16,["khongdung_t4","linh"],"Kong Rong stands on the wall of the besieged city of Beihai in scholar's robes with a few guards, looking out at a vast encampment of besiegers with many small tents and banners on the plain below, tense afternoon light")
sc(17,["liubei_t4a","thaisutu_t4","quanvu_t4a","trieuphi_t4a"],"in the hall of Pingyuan Liu Bei presses one hand to his chest, moved, listening to Taishi Ci who bows before him, Guan Yu and Zhang Fei standing behind Liu Bei, wooden pillars and oil lamps, Liu Bei in the centre of the frame between Taishi Ci and the two brothers")
sc(18,["linh"],"a small army camp at dusk at the foot of northern hills, a few "+SOL+" sitting around a camp fire and a sentry beside a tall plain red banner, "+NF)
sc(19,["linh"],"a column of about forty "+SOL+" marching along a dusty road behind a plain red banner, seen from behind and slightly above, three thousand troops going to a rescue, "+NF)
sc(20,["linh"],"a disciplined line of "+SOL+" seen from behind advancing across a plain toward distant besieging tents that are being struck and abandoned as the besiegers flee, plain banners, "+NF)
sc(21,["khongdung_t4","thaisutu_t4"],"in his hall at Beihai Kong Rong smiles in relief reading a message while Taishi Ci bows beside him, officials gathered, wooden pillars, oil lamps, warm light")
sc(22,["liubei_t4a","quanvu_t4a","linh"],"Liu Bei in the centre of the frame with Guan Yu beside him stand together on the gate-tower of Pingyuan at dusk looking east with soldiers on watch along the wall, a thoughtful mood, plain banners in the wind")
sc(23,["taotao_t4","linh"],"in the command tent of Cao Cao at Yanzhou, Cao Cao stands before a low table with officers around him, one hand on his sword hilt, sharp ambitious gaze, plain dark banners and tent poles, lamp light")
sc(24,["dan"],"a modest family convoy on a quiet mountain road toward Langya in Xu Province: two ox carts with luggage and an old man riding in one, a few servants walking beside, peaceful morning, green hills, no danger shown")
sc(25,["linh"],"a night road in mist where a small convoy of carts has halted, a distant ridge with torch lights and the shadowy outlines of riders, an overturned cart in the foreground, ominous mood, the tragedy implied only by the empty road, no violence shown, no victims")
sc(26,["taotao_t4","linh"],"a messenger kneels before Cao Cao in his tent delivering terrible news, Cao Cao stunned and white-faced with a clenched fist, officers behind him, lamp light, dark banners")
sc(27,["taotao_t4","linh"],"Cao Cao stands before an assembled army with a raised fist swearing revenge, rows of "+SOL+" and plain dark banners behind him under a stormy sky, "+NF)
sc(28,["daokhiem_t4a","quan"],"old Tao Qian sits at a low desk in his governor's hall, worn and worried, officials anxiously standing around him, wooden pillars, bamboo-slip scrolls on shelves, dim lamp light")
sc(29,["dan"],"a prosperous walled Chinese river city on a plain, busy wooden quay with merchants, porters carrying grain sacks and moored grain boats, carts on the dirt streets, grey tiled roofs, bright morning")
sc(30,["linh"],"the army of Cao Cao in long ranks before a walled city with thick smoke rising over its towers, plain dark banners, flames behind the wall, seen from a hill, a scene of conquest, "+NF)
sc(31,["dan"],"a long line of refugee villagers carrying bundles and pulling ox carts along a dirt road away from black smoke on the horizon, women and old people, tired and silent, seen from a distance, no violence shown")
sc(32,["dan"],"an empty dirt street inside an ancient Chinese town between low mud-brick houses with grey tiled roofs, overturned wooden carts and scattered baskets, drifting dust, a few surviving townsfolk huddled far in the distance")
sc(33,["tuongquan","quan","linh"],"in an army camp an exhausted messenger hands an urgent rolled letter to the commander Tian Kai while officers gather around him reading anxiously, tents and banners behind, grey morning")
sc(34,["tuongquan","liubei_t4b","linh"],"an army commander and Liu Bei ride side by side at dawn at the head of a marching army, ranks of "+SOL+" and plain banners stretching behind them down a dusty road, resolute, "+NF)
sc(35,["liubei_t4b","quanvu_t4a","trieuphi_t4a","linh"],"Liu Bei strides forward at the head of his own small army, his hand on the hilt of his sword, Guan Yu with a long curved-blade polearm and Zhang Fei with a long serpent-tipped spear beside him, soldiers following behind, banners in the wind, determination, "+NF+", Composition: Liu Bei stands in the exact centre of the frame between the two, Guan Yu on his left and Zhang Fei on his right, Liu Bei the main figure.")
sc(36,["linh","kybinh","dan"],"a small modest army camp at dusk: a handful of tents, a few "+SOL+" resting by camp fires, Wuhuan horsemen on horses at the edge, and hungry peasants lined up receiving food, plain banners, "+NF)
sc(37,["tuongquan","liubei_t4b","linh"],"on a muddy river bank east of a walled town an officer and Liu Bei look grimly toward enemy smoke while their small force of "+SOL+" regroups with tattered banners behind them, defeat in the air, "+NF)
sc(38,["daokhiem_t4a","liubei_t4b","dan"],"at the gate of the Xu Province city old Tao Qian welcomes Liu Bei and his soldiers entering, townsfolk and officials gathered and cheering with relief, banners, gate-tower behind, warm light")
sc(39,["daokhiem_t4a","liubei_t4b","linh"],"Tao Qian points toward rows of "+SOL+" lined up before a camp of tents, giving four thousand troops to Liu Bei who bows in thanks, plain banners, "+NF)
sc(40,["daokhiem_t4a","liubei_t4b","quan"],"in a hall Tao Qian and Liu Bei sit side by side on straw mats sharing a quiet cup of wine, officials seated along the walls watching with respect, a small oil lamp and a low table, warm evening light")
sc(41,["liubei_t4b","quan","linh"],"in the camp at Xiaopei an official hands Liu Bei a small bronze seal on a ribbon cord before assembled soldiers and officers, tents and banners, morning light")
sc(42,["linh"],"a small walled town on a plain at dusk with a few "+SOL+" standing on the wall and camp fires with resting soldiers outside the wall, plain banners, "+NF)
sc(43,["taotao_t4","linh"],"Cao Cao turns on the road to look back with a cold frown while a retreating column of "+SOL+" behind him marches away with lowered plain dark banners at dusk, dusty road, "+NF)
sc(44,["lubo_t4a","quan","linh"],"Lu Bu, seen from behind in iron armour, rides through the gate of Yanzhou welcomed by Zhang Miao and Chen Gong while soldiers and townspeople cheer on both sides, banners, his face not visible")
sc(45,["dan","linh"],"townsfolk and soldiers on the wall of the Xu Province city watch with relief as the distant army of Cao Cao withdraws along the road toward misty hills, the gate-tower open, calm morning")
sc(46,["linh"],"a stone road in the evening with a column of "+SOL+" marching away between plain red banners that are lowered, seen from behind, "+NF)
sc(47,["daokhiem_t4b","mitruc_t4","quan"],"on a low wooden couch with a straw mat old Tao Qian lies frail and pale, Mi Zhu kneels beside him and a physician in dark robes waits at the bedside, dim lamp light, curtains, a bowl of medicine, no death shown")
sc(48,["mitruc_t4","quan"],"Mi Zhu kneels on a straw mat beside a low couch with a worried gentle face, a few attendants waiting behind him, dim light from a small clay oil lamp, quiet and heavy mood")
sc(49,["daokhiem_t4b","mitruc_t4"],"Tao Qian whispers his last wish to Mi Zhu who bends close to listen, dim lamp light, curtains, intimate and solemn, a few attendants standing back in the shadows")
sc(51,["mitruc_t4","liubei_t4b","dan","linh"],"Mi Zhu leads a delegation of officials and townspeople to the camp at Xiaopei and bows before a startled Liu Bei, soldiers watching, tents and banners, dusty light")
sc(52,["liubei_t4b","mitruc_t4","dan","quan"],"Liu Bei raises both hands and shakes his head in refusal while the delegation of officials, elders and townspeople kneel around him pleading, a large dramatic scene before the camp gate")
sc(53,["tranang_t4","liubei_t4b","quan"],"in a tent or hall Chen Deng speaks earnestly to Liu Bei with one hand raised, several elders and officials of Xu Province listening behind him, lamp light, persuasive mood")
sc(54,["linh"],"a tall proud southern walled city, Shouchun, with a grand gate-tower, soldiers on the wall and a plain solid-colour banner above rice fields, grey sky, the seat of Yuan Shu, "+NF)
sc(55,["tranang_t4","liubei_t4b","quan"],"in a hall Chen Deng shakes his head firmly and answers Liu Bei, who listens carefully, other officials around them in a council, wooden pillars and oil lamps")
sc(56,["khongdung_t4","liubei_t4b","linh"],"Kong Rong, refined and firm, arrives at the camp with a small retinue of horsemen and urges Liu Bei to accept the province, gesturing toward the city behind them, afternoon light")
sc(57,["liubei_t4b","mitruc_t4","tranang_t4","dan","linh"],"Liu Bei bows slightly in acceptance with his hands joined before the city gate, officials and townspeople around him cheering and bowing, soldiers lined up with plain banners, dawn light, a solemn triumphant moment")
sc(60,["mitruc_t4","liubei_t4c","dan"],"in an ancient storeroom Mi Zhu opens a heavy wooden chest of old bronze coins for Liu Bei while servants carry bolts of silk and clay jars, light from small clay oil lamps")
sc(61,["liubei_t4c","quan","linh"],"Liu Bei in his governor's robe stands at the top of the stone steps of the city hall looking over the city, officials bowing and guards standing at attention below, grey tiled roofs behind, calm and weighty")
sc(64,["liubei_t4c","mitruc_t4","tranang_t4","quan"],"a council in the hall of Xu Province: Liu Bei listens with a thoughtful hand at his chin while Mi Zhu and Chen Deng speak and officials gather around, lamp light")
sc(65,["lubo_t4a","linh"],"the walled city of Yanzhou under the red banner of Lu Bu, cavalry on horses riding out of the gate, soldiers on the wall, evening light, "+NF)
sc(67,["liubei_t4c","mitruc_t4"],"in his office at night Liu Bei reads a bamboo-slip scroll by lamp light, tired and humane, while Mi Zhu waits respectfully beside him with more scrolls")
sc(69,["liubei_t4c","quanvu_t4b","trieuphi_t4b","linh"],"Liu Bei in his early thirties rides at the head of a small army across a plain at golden hour, Guan Yu and Zhang Fei riding beside him, soldiers and banners behind, a river valley and a distant ancient city, a sense of long road travelled, Composition: Liu Bei stands in the exact centre of the frame between the two, Guan Yu on his left and Zhang Fei on his right, Liu Bei the main figure.")
sc(70,["liubei_t4a","dan"],"the open wooden gate of a small ancient Chinese county town with a plain solid-colour flag in early morning light, a few villagers going about their work, a young junior official watching from the gate, blank gate with no writing")
sc(72,["liubei_t4a","quanvu_t4a","trieuphi_t4a"],"three small travellers, Liu Bei, Guan Yu and Zhang Fei, walking side by side on a long winding dirt road across wide hills toward a river city of tiled roofs, tiny in a vast landscape, golden light, Composition: Liu Bei stands in the exact centre of the frame between the two, Guan Yu on his left and Zhang Fei on his right, Liu Bei the main figure.")
sc(73,["quanvu_t4b","trieuphi_t4b","linh"],"Guan Yu with a long curved-blade polearm and Zhang Fei with a long serpent-tipped spear stand in front of rows of "+SOL+" and plain banners in an army camp at dusk, serious faces, "+NF)
sc(75,["dan"],"a rich walled ancient Chinese river city of grey tiled roofs with wooden grain boats moored at the bank, porters and merchants on the quay, under gathering dark clouds that threaten the city")
sc(76,["taotao_t4","linh"],"Cao Cao stands alone before a plain grave mound with incense smoking at grey dawn, soldiers kneeling in rows far behind him, bare trees, a heavy silent grief that turns to resolve")
sc(77,["quan","linh"],"a tall ancient Chinese city gate-tower above rice fields under a grey sky, guards on the wall and a plain solid-colour banner with no writing and no emblem, the southern city of Yuan Shu, "+NF)
sc(78,["quan"],"in a dim hall corridor with wooden pillars two or three officials of Xu Province whisper together with suspicious glances toward an inner door, long shadows, a small clay oil lamp on the floor")
sc(79,["liubei_t4c","quanvu_t4b","trieuphi_t4b","linh"],"Liu Bei stands on a stone city wall at dusk looking around at the four directions, worried, Guan Yu and Zhang Fei beside him, soldiers keeping watch along the wall, plain banners, Composition: Liu Bei stands in the exact centre of the frame between the two, Guan Yu on his left and Zhang Fei on his right, Liu Bei the main figure.")
sc(80,["kybinh","linh"],"four dirt roads meeting at an ancient Chinese city gate under a darkening sky, small groups of riders approaching along each road from the four directions, threatening mood, "+NF)
sc(81,["linh"],"a wide plain seen from a hill with two roads: on the northern road a small column of "+SOL+" marches toward Beihai and on the eastern road another column marches toward Xu Province, the two rescues in one picture, soft morning light, "+NF)
sc(82,["mitruc_t4","tranang_t4","khongdung_t4"],"three men stand together under the lanterns of a city gate at night welcoming Liu Bei: a rich merchant, a young scholar-official and a famous scholar, warm lamp light, stars above")
sc(83,["taotao_t4"],"a lacquered gift box with a gold clasp stands open on a low table in a hall, dark mist curling from it, and in the mist behind it the faint silhouettes of two armies, one to the north and one to the south, a poisoned gift")
sc(84,["lubo_t4b","linh"],"Lu Bu seen from behind, travel-stained and with a torn cloak, rides at the head of a small weary band of riders along a long dirt road toward the gate of Xiaopei at dusk, his face not visible")
sc(85,["lubo_t4b","linh"],"a rainy night: a small group of riders with torches arrives at the gate of an ancient Chinese city, guards at the gate looking out in uncertainty, one hanging oil lantern on the gate, mud and rain, a question hanging in the air")
sc(86,["liubei_t4c"],"Liu Bei sits alone at a low table at night with a bamboo-slip scroll tied with cord, a clay oil lamp beside him, looking toward a wooden lattice window with no glass where mountains show in the starlight")

OV = {
 3: ([], "an empty low wooden table in a hall with a tied bamboo-slip scroll and a small clay oil lamp, wooden pillars and a straw mat floor, a wooden lattice window with a mountain view, no people"),
 14: ([], "an ancient Han Chinese mud-brick farmhouse at night, grey tiled roof, a wooden lattice window with warm lamplight, a straw mat and clay jar at the door, village houses and dark hills behind under stars, no people, no bench"),
 31: (["dan"], "a column of tired porters and peasants carrying sacks and pulling wooden carts along a dirt road past mud-brick houses with grey tiled roofs, smoke rising from far hills, plain banners, no awnings, no poles"),
 47: (["daokhiem_t4b","liubei_t4b"], "in a sick-room the very old white-bearded Tao Qian in a pale robe lies propped up on straw mats on a low wooden platform, pale and weak, while the younger Liu Bei in armour and a pale headband kneels on a straw mat at his bedside listening, a clay oil lamp, wooden bars at the window, hanging cloth screens"),
 48: (["liubei_t4b","linh"], "Liu Bei kneels on a straw mat refusing with his hands raised, officials of Xu Province in dark robes standing behind him, a low wooden platform and a clay oil lamp, tent flaps and hills outside"),
 50: ([], "an empty plain Han sickroom with a straw mat, a low wooden platform without a backrest, a clay bowl and a clay oil lamp, a hanging plain cloth, wooden lattice window with no glass, no people"),
 61: (["liubei_t4c","linh"], "Liu Bei in a dark robe stands beside an armoured officer before a Han governor's hall in a river city, officials and townsfolk kneeling and bowing on the stone steps, grey tiled roofs and timber pillars, no signboards"),
 62: ([], "the stone gate of a Han Chinese government compound with plain timber pillars and a grey tiled roof, a bronze seal on a low wooden stand before the gate, courtyard with paving stones, no signboard on the gate, no writing"),
 63: ([], "a quiet Han governor's inner hall with two folded dark-blue and green cloth robes tied with cord on a low lacquered table, wooden pillars, a straw mat floor, a hanging cloth screen and a clay oil lamp, window of wooden lattice with a view of hills"),
 67: (["liubei_t4c","mitruc_t4"], "at night Liu Bei sits on a straw mat at a low table reading a bamboo-slip scroll by a clay oil lamp, Mi Zhu standing beside him, wooden lattice window with stars outside, bamboo-slip scrolls stacked on a shelf, a canvas tent wall behind, no lamp posts, no wires, no chairs"),
 70: (["liubei_t4a","dan"], "Liu Bei in a dark-blue robe speaks with a poor peasant at the wooden gate of a village, mud-brick houses with grey tiled roofs, hills behind, no hanging sign, no awning"),
 74: ([], "a low wooden table with folded dark-blue and green cloth robes tied with cord, a clay oil lamp beside it, mud-brick wall, wooden lattice window with a view of hills, straw mats on the floor"),
 78: (["quan"], "in a dim corridor with timber pillars two or three officials in dark robes whisper together, glancing toward an inner wooden door, long shadows, a small clay oil lamp on the floor, wooden lattice screens, no glass"),
 84: (["lubo_t4b","linh"], "Lu Bu seen from behind, travel-stained and wearing a torn cloak, rides at the head of a small weary band of riders along a long dirt road toward the plain gate-tower of Xiaopei at dusk, hills behind, his face not visible, empty sky with no wires"),
 85: (["lubo_t4b","linh"], "a rainy night: a small group of riders with torches arrives at the plain wooden gate of a Han city, guards at the gate looking out in uncertainty, one hanging clay oil lantern, mud and rain, no awnings"),
 86: (["liubei_t4c"], "a low wooden table at night with a tied bamboo-slip scroll, a clay oil lamp and clay jars, a wooden lattice window with no glass where mountains show in the starlight, straw mats, no people"),
}

for k in KEEP:
    i = int(k)
    o = OLD.get(k)
    assert o, f"thiếu mô tả cũ {k}"
    S[i] = (o["nv"], o["m"])
for i,v in OV.items(): S[i]=v
missing = [i for i in range(1, 87) if i not in S]
assert not missing, missing
for i in S: assert 1 <= i <= 86

BGRULE = "Every picture has a rich detailed background that fits the place and the story (architecture, landscape, tents, banners, hills), never a plain blank or solid-colour backdrop"
ANTI = ("Strictly Eastern Han dynasty, 2nd century AD, ancient China only: dirt roads and stone paths only (no asphalt, no road markings, no electric poles or wires), "
        "no glass windows (wooden lattice only), no door knobs or handles, no signboards or plaques on gates or buildings, no chairs with backs or modern furniture (people sit on straw mats or low benches), "
        "no candles (clay oil lamps only), no bound paper books and no sheets of paper (only bamboo-slip scrolls tied with cord), no mugs with handles, no lamp posts, no European, Korean or Japanese buildings (Han Chinese grey-tiled mud-brick and timber architecture), "
        "no striped awnings or canopies, no ceiling lamps, no desk lamps, no hanging signs, windows are plain square openings with vertical wooden bars only and no glass panes and no paper panes, roofs have heavy straight ridges and gently sloped eaves, not upturned curved Korean or Japanese eaves, no plaques, no bench with a backrest, no writing or Chinese characters anywhere, no baseball caps, no modern shoes (soft cloth shoes, boots or straw sandals), no writing on objects, signs or banners")
SUF = ("cinematic composition that suits the story moment, dynamic framing (wide, medium or low-angle as the scene needs), foreground, middle ground and background all filled, "
       "every named hero's signature weapon is clearly visible and drawn exactly as described, every person has exactly two arms, two hands and two legs with natural adult proportions, serious weathered faces, no extra limbs, no deformed faces, no text, no letters, no watermark. "
       "Flags and banners are plain solid colour with no symbols. " + BGRULE + ". " + ANTI)
EXTRA_PK = lambda i, x: PK["day_an_thu_su"] if (x == "liubei_t4b" and 41 <= i <= 57) else (PK["an_tuong_bac_hai"] if (x == "khongdung_t4" and i == 56) else "")

TRIO = {10,12,35,69,72,79}
out, canh = [], []
for i in range(1, 87):
    nv, m = S[i]; k = f"{i:03d}"
    canh.append({"key": k, "nv": nv, "mo_ta": m})
    if not nv:
        out.append({"key": k, "nv": [], "prompt": m + ". An empty quiet scene of objects and landscape only. 2D franco-belgian ligne claire comic illustration of ancient China, clean uniform dark ink outlines, flat muted colours with soft shading, earthy palette of ochre, jade green, indigo and warm cream, no text, no numerals, no letters, no watermark, not 3D, not a photo. " + ANTI})
        continue
    named = [x for x in nv if x not in EXTRA]
    if i in TRIO:
        pos = {"quanvu_t4a":"LEFT","quanvu_t4b":"LEFT","liubei_t4a":"CENTRE","liubei_t4b":"CENTRE","liubei_t4c":"CENTRE","trieuphi_t4a":"RIGHT","trieuphi_t4b":"RIGHT"}
        nv = sorted(nv, key=lambda x: {"LEFT":0,"CENTRE":1,"RIGHT":2}.get(pos.get(x),3))
        ch = "; ".join((pos[x] + " of the three: " if x in pos else "") + NV[x] for x in nv)
    else:
      ch = "; ".join(NV[x] + ((", " + EXTRA_PK(i, x)) if EXTRA_PK(i, x) else "") for x in nv)
    out.append({"key": k, "nv": nv, "prompt": f"{m}. Characters (keep exactly this look): {ch}. {STYLE}. {SUF}"})
(R / "TQ4.json").write_text(json.dumps({"ma": "TQ4", "ghi_chu": "Tập 4: Bình Nguyên, Bắc Hải, Từ Châu", "canh": canh}, ensure_ascii=False, indent=1), encoding="utf-8")
(R / "TQ4_anh.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print("ok", len(out), "ảnh;", len([c for c in canh if c['key'] not in KEEP]), "ảnh cần vẽ lại")
