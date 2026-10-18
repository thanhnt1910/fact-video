"""Tạo TQ5.json (cảnh), TQ5_anh.json (88 prompt vẽ) và TQ5_trang_phuc.json cho TẬP 5 (đón hoàng đế về Hứa, Viên Thuật xưng đế).
Khóa ảnh = số beat lời kể (001...088), mỗi ảnh dùng một lần. Lời kể của từng beat nằm trong /home/claude/loi_ke_tap5.txt (đã chia sẵn thành /tmp/beats5.json
khi tạo; bản sao nằm ở ke-hoach/nhan-vat/TQ5_beats.json để chạy lại được).
Quy tắc ảnh (17/10): KHÔNG giới hạn số người, KHÔNG ép nửa người; cảnh vẽ đúng cốt truyện; ảnh nào cũng có nền; không vật hiện đại; không máu me, không cảnh giết."""
import json
from pathlib import Path
R = Path(__file__).resolve().parent
tq = json.loads((R / "TQ.json").read_text(encoding="utf-8"))
t2 = json.loads((R / "TQ2.json").read_text(encoding="utf-8"))
tp4 = json.loads((R / "TQ4_trang_phuc.json").read_text(encoding="utf-8"))
BEATS = json.loads((R / "TQ5_beats.json").read_text(encoding="utf-8"))

EXTRA = {
 "linh": "a Han soldier in a plain iron helmet and leather-and-iron scale armour over a dull red-brown tunic",
 "quan": "a court official in a black cap and a dark robe, tired and thin",
 "kybinh": "a Han cavalryman in a plain iron helmet and scale armour",
 "babat": "a rough leader of the White Wave rebel army in worn brown leather armour with a plain cloth headband",
 "hungno": "a Xiongnu king in a felt hat and a fur-trimmed leather robe with a broad belt, dark hair worn loose to the shoulders",
}
# --- trang phục / nhân vật tập 5 (mốc năm 195-199) ---
TP = {
 "hiende_t5": "Emperor Xian of Han at about fifteen, a slim serious teenage emperor, tall and thin for his age, pale grave thoughtful face, no beard, hair in a topknot under a small plain black cap, wearing a worn dark cross-collared robe with a plain sash, composed mature bearing, never cute, never a small child",
 "taotao_t5a": "Cao Cao, a short wiry man of about 41 with sharp clever eyes, a thin moustache and a small beard, dark charcoal cross-collared robe under dark iron scale armour with a dark cloak, the stern look of a general on campaign",
 "taotao_t5b": "Cao Cao, a short wiry man of about 41 with sharp clever eyes, a thin moustache and a small beard, hair in a topknot under a plain dark cap, wearing a dark charcoal cross-collared robe with a dark sash, a calm commanding look, no insignia",
 "liubei_t5": "Liu Bei at age 36, a tall slender man in his mid-thirties, calm gentle face, unusually long arms that hang down to his knees, unusually large earlobes, a thin moustache and a short sparse beard of fine hair along the jaw and chin (visibly bearded but much lighter and shorter than a full beard), hair in a topknot under a plain black cap, wearing a long dark-indigo cross-collared robe with slightly worn cuffs, a dark sash and a leather belt, plain dark shoes, a quiet watchful look",
 "lubo_t5": "Lu Bu, a tall powerfully built man with a strong jaw and sharp eyes, hair in a topknot under a plain iron helmet, wearing cleaned iron scale armour over a dark-red cross-collared robe with a dark-red cloak, the confident bearing of a man who has taken a province",
 "vienthuat_t5a": "Yuan Shu, a heavy-set proud man of about 40 with a round florid face, a thin moustache and a short beard, hair in a topknot under a tall black official cap, wearing a rich dark-red cross-collared robe with a wide sash over fine light armour, an arrogant impatient look",
 "vienthuat_t5b": "Yuan Shu, a heavy-set proud man of about 41 with a round florid face, a thin moustache and a short beard, wearing a flat-topped ceremonial crown with hanging bead strings and a black-and-ochre ceremonial robe with a wide sash, an arrogant self-satisfied look",
 "vienthieu_t5": "Yuan Shao, a handsome tall man of about 42 with a neat short beard, proud composed look, deep-blue official robe over light armour, a black cap",
 "tonsach_t5": "Sun Ce, a strong athletic young man of twenty with a square jaw, a sun-tanned weathered face, a faint thin moustache, bright determined eyes, hair in a topknot under a plain cloth band, wearing light iron scale armour over a short red-brown tunic, adult proportions, not boyish",
 "thaisutu_t5": "Taishi Ci, a lean athletic man of about 29 with alert determined eyes, hair in a topknot under a plain cloth band, wearing light leather armour with wrist guards and boots",
 "truongchieu_t5": "Zhang Zhao, a stern scholar of about forty with a long neat beard, black cap, pale-grey cross-collared scholar's robe with wide sleeves",
 "chauyu_t5": "Zhou Yu, a handsome calm man of about twenty with clear sharp eyes, hair in a topknot, dark-blue robe over light armour, adult proportions",
 "trinhduc_t5": "Cheng Yu, a composed tall strategist in his mid-fifties with a long neat beard and steady clear eyes, hair in a topknot under a plain black cap, wearing a sober dark-grey cross-collared robe with a dark sash",
 "tuanuc_t5": "Xun Yu, a refined slender scholar of about thirty-four with a clean elegant face and a thin moustache, hair in a topknot under a plain scholar's cap, wearing a pale-grey cross-collared robe with wide sleeves and a dark sash",
 "dongchieu_t5": "Dong Zhao, a lean clever official of about forty with a narrow face and a thin pointed beard, hair in a topknot under a black cap, wearing a plain dark-brown cross-collared robe with a dark sash",
 "dienvi_t5": "Dian Wei, a gigantic powerfully built bodyguard with a thick neck and a heavy bristly black moustache, hair in a topknot, wearing a sleeveless dark leather jerkin over a dark tunic and thick wrist guards",
 "truongtu_t5": "Zhang Xiu, a lean angular man of about thirty with sharp narrow eyes and a thin moustache, hair in a topknot under a plain iron helmet, dark iron scale armour over a dark-green tunic",
 "tranhkhue_t5": "Chen Gui, an elderly official of about sixty with a thin white beard, pale-grey robe with a dark sash, black cap",
 "duongphung_t5": "Yang Feng, a broad rough soldier-general of about forty with a square weathered face and a short stubbly beard, plain iron helmet, scale armour over a faded brown tunic",
 "hantiem_t5": "Han Xian, a wiry restless former rebel leader of about forty with a hawkish face and a thin moustache, a cloth headband, rough leather-and-iron armour",
 "dongthua_t5": "Dong Cheng, a dignified middle-aged commander with a long neat beard, black cap, dark-red robe over scale armour",
 "truongte_t5": "Zhang Ji, a broad calm general of about forty-five with a trimmed beard, iron helmet, dark armour over a dark-blue tunic",
 "lythoi_t5": "Li Jue, a heavy-set rough general of about fifty with a wide coarse face and a thick beard, iron scale armour over a dark-red tunic, arrogant bearing",
 "quachty_t5": "Guo Si, a lean hard general of about forty-five with a hawk nose, a narrow face and a thin moustache, iron scale armour over a dark-brown tunic",
 "taohong_t5": "Cao Hong, a sturdy loyal general of about thirty-five with a square face and a short beard, iron helmet, dark armour",
}
NV = {**tq["nhan_vat"], **t2["nhan_vat_phu"], **tp4["trang_phuc"], **EXTRA, **TP}
STYLE = tq["phong_cach"].replace("year 184 AD", "year 196 AD")
SOL = "Han soldiers in plain iron helmets and leather-and-iron scale armour over dull red-brown tunics, spears upright"
NF = "no gore, no blood, no one being struck or killed, soldiers with small simple faces"

S = {}
def sc(i, nv, m): S[i] = (nv, m)

sc(1, ["hiende_t5", "quan"], "in a borrowed plain house in burnt Luoyang the young emperor sits on a low bench in a bare room, thin court officials in black caps stand leaning against blackened half-collapsed mud-brick walls, charred beams overhead, cold autumn light, hunger and poverty shown by empty tables")
sc(2, ["taotao_t5a", "linh"], "Cao Cao rides at the head of an army coming from the east along a dusty road toward the grey ruins of Luoyang under an autumn sky, ranks of soldiers and plain dark banners behind him, seen from a low angle, "+NF)
sc(3, ["vienthuat_t5a", "quan"], "in a grand hall at Shouchun Yuan Shu stands before an empty low throne on a dais with one hand resting greedily on its arm, a few officials small and silent behind him, lamp light, rich red hangings")
sc(4, [], "wide aerial view of a central plain with a ruined walled capital city in the middle, two dusty roads leading toward it, one from the east and one from the south, tiny columns of soldiers with plain banners on both roads, soft dusk, no one fighting")
sc(5, ["lythoi_t5", "quachty_t5"], "in the burnt courtyard of the Chang'an palace two rival generals in armour stand face to face with proud hostile faces, broken pillars and thin black smoke behind them, tile roofs half collapsed, grey sky")
sc(6, ["dan"], "dry cracked fields around Chang'an in a drought, withered crops and bare trees, thin exhausted villagers sitting and lying along the roadside in ragged hemp clothes, a heavy sad mood, empty ox cart, no corpses shown")
sc(7, ["hiende_t5", "quan", "dan"], "in the palace yard officials ladle thin gruel from large clay pots into bowls for a long patient line of thin starving people, steam rising in the cold air, the young emperor watching from a covered porch")
sc(8, ["hiende_t5", "quan"], "the young emperor stands beside a big clay pot with a wooden ladle, frowning as he examines the thin gruel, an official kneels pale-faced before him, other officials watch anxiously, wooden dou measures of beans and rice on a low table")
sc(9, ["lythoi_t5", "quachty_t5", "linh"], "two rival armies face each other across a burning street of Chang'an with flames and smoke rising from palace roofs, lines of "+SOL+" behind each general, a tense moment of standoff, "+NF)
sc(10, ["hiende_t5", "truongte_t5", "linh"], "the young emperor sits in an ox-drawn open cart leaving the gate of Chang'an toward the east, soldiers with spears marching on both sides with a general riding beside, plain banners, dusty road, summer morning, "+NF)
sc(11, ["hiende_t5", "duongphung_t5", "dongthua_t5", "linh"], "beside the roadside cart of the emperor three armoured generals kneel on one knee receiving their commission, soldiers standing with spears behind them, dusty open country, plain banners")
sc(12, ["linh"], "at night a long low school building beside the road burns with tall flames and thick smoke, guards in iron helmets forming a protective line around a covered cart in the foreground, a dramatic fire light on their faces, "+NF)
sc(13, ["hiende_t5", "quan"], "the emperor's party sleeps in an open field at night under stars, tired officials huddled on straw mats around a small camp fire, torn plain banners, a covered cart in the background, cold exhausted mood")
sc(14, ["babat", "hungno", "hiende_t5"], "in an open field a leader of the White Wave rebels in rough leather armour and a Xiongnu king in a felt hat and fur-trimmed robe kneel before the emperor, who stands tired but dignified, a few soldiers behind them, dusty light, plain banners")
sc(15, ["kybinh", "babat", "linh"], "a long line of Xiongnu horsemen, rebels and Han soldiers draws up against pursuers on a plain, ranks with plain banners, dust, seen from behind and above, "+NF)
sc(16, ["hiende_t5", "quan", "linh"], "at night the emperor and a few officials descend a steep bank of the Yellow River to wooden boats, soldiers carrying torches and lowering carts, a wide dark river and distant bank, a tense escape, "+NF)
sc(17, ["hiende_t5"], "at dawn the emperor, a lonely slim young figure, stands at the small gate of the walled town of Anyi looking back across the wide river, a few guards behind him, thin mist, a modest wooden gate with a plain flag")
sc(18, ["hiende_t5", "quan"], "at Anyi the emperor performs a sacrifice to Heaven at an earthen altar in the open air, officials kneeling in rows, incense smoke rising, plain banners, a new year of reign being proclaimed, winter morning light")
sc(19, ["hantiem_t5", "dongthua_t5", "linh"], "inside a camp two generals, Han Xian and Dong Cheng, stand glaring at each other with their soldiers lined up behind each of them, spears still upright, a tense quarrel before a fight, tents and banners, grey light, "+NF)
sc(20, ["taotao_t5a", "linh"], "in the command tent at Yanzhou Cao Cao sits at a low table with bamboo-slip scrolls, officers standing around him, one hand at his chin, thinking deeply, plain dark banners and tent poles, lamp light")
sc(21, ["taotao_t5a", "trinhduc_t5"], "in a lamp-lit tent Cheng Yu speaks earnestly to Cao Cao with one hand raised, Cao Cao listening with a stern face, a small oil dish on a low table")
sc(22, ["taotao_t5a", "tuongquan", "quan"], "Cao Cao stands before a council of generals in the camp tent, some with arms crossed and doubtful faces, a hanging cloth map behind them, lamp light, serious mood")
sc(23, ["taotao_t5a", "tuanuc_t5", "trinhduc_t5"], "Xun Yu and Cheng Yu stand together urging Cao Cao across a low table with a bamboo-slip map, Cao Cao turning toward them with interest, lamp light")
sc(24, ["taohong_t5", "linh"], "Cao Hong leads a column of soldiers westward along a mountain road seen from behind, far ahead a narrow pass held by blockers with tiny banners on the rocks, plain dark banners, windy afternoon, "+NF)
sc(25, ["dongchieu_t5", "quan"], "Dong Zhao sits at a low desk by a clay oil lamp writing a letter with a brush on a bamboo slip, concentrating, bamboo slips and an ink stone beside him, a wooden lattice window with no glass")
sc(26, ["duongphung_t5", "quan"], "in a camp tent Yang Feng reads a letter with a pleased surprised face while an official stands beside him, tent walls and a spear rack, warm lamp light")
sc(27, ["duongphung_t5", "hantiem_t5", "dongthua_t5", "quan"], "the three generals Yang Feng, Han Xian and Dong Cheng together with officials gather around a low table to write a petition on a bamboo-slip scroll, tent interior, lamp light")
sc(28, ["hiende_t5", "linh"], "in summer the emperor and his escort arrive at the walls of burnt Luoyang along a dusty road, blackened ruined towers ahead, soldiers marching, plain banners, an ox cart in the middle, a mood of return to a ruined home, "+NF)
sc(29, ["hiende_t5"], "a plain modest house in the middle of ruins, the young emperor sits alone on a low bench in the courtyard where weeds grow between broken stones, burned walls around him, autumn light")
sc(30, ["taotao_t5a", "linh"], "Cao Cao's army marches toward the broken gate of Luoyang in autumn, ranks of soldiers and plain dark banners, ruined walls ahead, seen from behind and slightly above, "+NF)
sc(31, ["hiende_t5", "taotao_t5b", "quan"], "in the ruined hall of Luoyang the young emperor hands Cao Cao a bamboo staff with hanging tassels, a sign of delegated authority, officials watching, charred pillars, soft light")
sc(32, ["taotao_t5b", "dongthua_t5", "quan"], "Cao Cao seated on a low dais in a hall announces rewards to kneeling officials while at the dark side of the hall two other officials are quietly led away by guards, shadows and long light, a double-edged mood, no violence")
sc(33, ["dongchieu_t5", "taotao_t5b"], "Dong Zhao leans toward Cao Cao and whispers advice over a hanging cloth map in a lamp-lit room, Cao Cao listening with narrowed eyes")
sc(34, ["dongchieu_t5", "taotao_t5b"], "Cao Cao frowns and rests a hand on his chin while Dong Zhao explains a plan with a pointing finger toward the east on a cloth map, lamp light")
sc(35, ["hiende_t5", "linh"], "at dawn the emperor's party leaves a mountain pass toward the east, an ox cart and soldiers marching on both sides along a narrow road between steep hills, plain banners, mist, "+NF)
sc(36, ["duongphung_t5", "linh"], "Yang Feng rides away from his camp at dusk with a bitter face and a few riders, while far behind him the ranks of "+SOL+" advance toward his camp with plain dark banners, dust, "+NF)
sc(37, ["vienthieu_t5", "quan"], "in a hall Yuan Shao turns his head away in proud displeasure and pushes aside a lacquered edict box offered by a kneeling envoy, officials watching, rich blue hangings")
sc(38, ["taotao_t5b", "quan"], "Cao Cao bows slightly and hands a small bronze seal on a ribbon cord back to an envoy in a hall, officials watching, wooden pillars, a calm clever expression")
sc(39, ["dan", "linh"], "wide fields near Xu in spring where soldiers and peasants work together, ploughs pulled by oxen, men carrying seed baskets, a big granary with a thatched roof in the background, green hills, peaceful and productive, "+NF)
sc(40, ["taotao_t5b", "tuanuc_t5"], "in a modest timber hall of Xu Cao Cao hands a rolled bamboo-slip appointment to Xun Yu who bows to receive it, wooden pillars and plain cloth screens, morning light")
sc(41, ["tuanuc_t5"], "Xun Yu sits alone at a desk piled with bamboo-slip scrolls writing replies by an oil lamp, a rider waiting with a sealed letter at the door, night, quiet and busy")
sc(42, ["quan", "dan"], "scholars and officers in plain robes arrive on foot and on carts through the gate of the new capital of Xu, townsfolk watching, a busy dirt street with low tiled-roof buildings, morning light")
sc(43, ["kybinh", "dan"], "a rider leaves the gate of Xu carrying a sealed decree box with a plain flag, townsfolk and farmers on the road stopping to watch him pass, dust, a wide plain beyond")
sc(44, ["liubei_t5", "taotao_t5b", "quan"], "at the gate of Xu Cao Cao greets Liu Bei with joined hands as Liu Bei arrives with a small weary band of soldiers, officials and townsfolk watching, a warm but watchful meeting")
sc(45, ["taotao_t5b", "trinhduc_t5"], "in a lamp-lit room Cheng Yu whispers to Cao Cao who slowly shakes his head, a low table with a wine cup and bamboo slips")
sc(46, ["taotao_t5b"], "Cao Cao stands alone at night before a hanging cloth map studying the south-east, one hand behind his back, a clay oil lamp on a low table, shadows")
sc(47, ["liubei_t5", "linh"], "Liu Bei rides at the head of a small army toward the south-east along a long road across plains at golden hour, plain banners and soldiers behind him, a river in the distance, "+NF)
sc(48, ["vienthuat_t5a", "quan"], "Yuan Shu stands proudly before the grand wooden gate of his family mansion at Shouchun with servants and officials lined up at the steps, red hangings, a rich old house with grey tiles")
sc(49, ["vienthuat_t5a", "linh"], "a wide view of the walled city of Shouchun with large army camps on the plain, Yuan Shu on the gate-tower with soldiers on the wall, plain banners, grey sky, "+NF)
sc(50, ["tonsach_t5", "vienthuat_t5a", "quan"], "in the hall at Shouchun young Sun Ce stands bowing with only a few men behind him before the seated Yuan Shu, rich red hangings, officials watching, an ordinary humble arrival")
sc(51, ["vienthuat_t5a", "tonsach_t5", "linh"], "Yuan Shu points at ranks of "+SOL+" lined up in a yard as if handing them over, while Sun Ce stands outside the hall at the side looking thoughtful and disappointed, plain banners, "+NF)
sc(52, ["vienthuat_t5b", "quan"], "Yuan Shu in a black-and-ochre ceremonial robe and a flat-topped crown with bead strings sits proudly on a dais in a hall, officials kneeling and bowing before him, a grand but hollow ceremony, red hangings")
sc(53, ["vienthuat_t5a", "quan"], "Yuan Shu in front of a bronze incense tripod at the side of a hall listens to an old diviner who points to the sky, officials around them, smoke rising")
sc(54, ["vienthuat_t5b", "dan"], "inside a lavish hall Yuan Shu feasts with rows of dancing women and musicians while at the open gate in the rain a line of starving peasants in rags stands looking in, a sharp contrast of plenty and hunger")
sc(55, ["vienthuat_t5b", "quan"], "an elderly adviser bows deeply before Yuan Shu who sits impatiently on his dais with a cold face, other officials silent, lamp light")
sc(56, ["tonsach_t5"], "Sun Ce sits at a low desk by a lamp writing a firm letter on a bamboo slip, a determined face, a spear rack and a lattice window behind him, night")
sc(57, ["lubo_t5", "quan"], "in the governor's hall of Xu Province Lu Bu sits in armour and a dark-red cloak at the head of a table, officials seated along the walls, wooden pillars and oil lamps, a confident look")
sc(58, ["lubo_t5", "tranhkhue_t5", "quan"], "an elderly adviser, Chen Gui, whispers earnestly to Lu Bu while at the far end of the hall a decorated bridal cart waits in the courtyard with an envoy standing by, lamp light")
sc(59, ["lubo_t5", "linh", "quan"], "an envoy in a wooden neck-board is led by guards through a market square toward the gate while Lu Bu watches coldly from a platform, townspeople watching in silence, grey tiled roofs, no violence")
sc(60, ["dan"], "the market square of Xu seen from a corner, a crowd of townspeople looking quietly toward a tall empty wooden pole in the middle of the square, hushed and uneasy, grey tiled roofs, nothing hanging on it")
sc(61, ["lubo_t5", "tranhkhue_t5", "tranang_t4"], "Lu Bu writes a letter at a low desk while Chen Gui and his son Chen Deng stand beside him, Chen Deng holding a sealed message box, lamp light, wooden pillars")
sc(62, ["lubo_t5", "duongphung_t5", "hantiem_t5", "linh"], "Lu Bu's army with two allied generals Yang Feng and Han Xian drives back a retreating enemy force across a plain, ranks of soldiers and plain banners, dust, seen from a hill, "+NF)
sc(63, ["tonsach_t5"], "Sun Ce stands alone on a riverbank at dawn looking north across the wide Yangtze river with a rolled letter in his hand, mist over the water, a few soldiers waiting behind him")
sc(64, ["tonsach_t5", "linh"], "Sun Ce with a few hundred soldiers and horses crosses the wide Yangtze river on wooden boats and rafts at dawn, soldiers poling, horses on the boats, plain banners, mist, "+NF)
sc(65, ["tonsach_t5", "linh"], "Sun Ce stands at the open gate of a granary with soldiers carrying grain sacks out, a large thatched storehouse and stacked baskets, bright morning, a hill road behind them, "+NF)
sc(66, ["tonsach_t5", "thaisutu_t5"], "two young horsemen meet in a sudden duel on a muddy road near a river, Sun Ce thrusting at the horse of Taishi Ci and grabbing a small halberd while Taishi Ci seizes Sun Ce's helmet, dust flying, dramatic angle, no blood, no injury")
sc(67, ["tonsach_t5", "thaisutu_t5", "linh"], "in a camp Sun Ce personally unties the ropes from the hands of Taishi Ci and holds his arm with a half smile, soldiers watching around them, tents and banners, morning light")
sc(68, ["tonsach_t5", "thaisutu_t5"], "Sun Ce laughs and clasps the arm of Taishi Ci, handing him a general's token, soldiers cheering behind them, a bright camp, plain banners")
sc(69, ["tonsach_t5", "chauyu_t5", "truongchieu_t5"], "in a hall at Jiangdong Sun Ce stands with the scholar Zhang Zhao and the handsome young Zhou Yu around a low table with a bamboo-slip map, warm lamp light, wooden pillars, three different faces")
sc(70, ["tonsach_t5", "quan", "linh"], "Sun Ce on a hill overlooking the green land of Jiangdong with soldiers in ranks behind him, an envoy handing him a rolled appointment, plain banners, a river valley below, golden light, "+NF)
sc(71, ["taotao_t5a", "linh"], "Cao Cao's army marches in winter toward the walls of Wan, a city in the plains of the south, ranks of soldiers and plain dark banners, thin snow on the road, seen from behind and above, "+NF)
sc(72, ["truongtu_t5", "taotao_t5a", "linh"], "in a camp Zhang Xiu kneels in surrender before Cao Cao who sits in armour with a calm satisfied face, soldiers standing around them, tents and plain banners, winter light")
sc(73, ["linh"], "at night a large camp with wooden fences and tents catches fire, tall flames and smoke, silhouettes of soldiers running with torches in the dark, a sudden attack on a sleeping camp, no one struck or killed, "+NF)
sc(74, ["dienvi_t5"], "Dian Wei, a gigantic bodyguard with a thick neck and bristly moustache, stands at the gate of a camp fence seen from behind with a heavy halberd in both hands, blocking a rush of dark torchlit shapes beyond, flames in the background, no blood")
sc(75, ["taotao_t5a", "linh"], "Cao Cao rides away in the dark on a galloping horse with a few riders around him, torchlight and flames far behind, dust, an arrow stuck in the saddle, no blood, desperate escape")
sc(76, ["taotao_t5a", "quan"], "at dawn in camp Cao Cao stands bareheaded and weeping before a plain wooden coffin on a low bier, officers and soldiers bowing their heads around him, thin mist, grief and silence")
sc(77, ["taotao_t5a", "linh"], "Cao Cao leads an army eastward across the plain of Chen at the head of ranks of soldiers with plain dark banners, a long road and river in the distance, decisive, seen from a low angle, "+NF)
sc(78, ["vienthuat_t5a", "linh"], "at dusk Yuan Shu hurries onto wooden boats at the bank of the Huai river with a few riders while soldiers stand confused on the bank behind him, plain banners, grey water, a king abandoning his army, "+NF)
sc(79, ["truongte_t5", "linh"], "Zhang Ji leads a small column of soldiers along a road at dawn toward a southern walled town, ranks of soldiers and plain banners, mist on the river, "+NF)
sc(80, [], "the deserted ruined streets of Chang'an in grey light, a fallen plain banner lying on the ground beside abandoned wooden carts, burnt walls, no people at all, a mood of emptiness after power")
sc(81, ["duongphung_t5", "hantiem_t5"], "at a fork in a dusty road at dusk two riders, Yang Feng and Han Xian, part ways and ride off in different directions, a tall dead tree between the two roads, solitary mood")
sc(82, ["taotao_t5b", "quan"], "in a hall of Xu Cao Cao sits at a long table with piles of bamboo-slip scrolls while officials and clerks work in rows with brushes, rice and food on a side table, an orderly bustling court that contrasts with ruin")
sc(83, [], "a lonely small house at dusk beside a river, a single clay oil lamp glowing in a lattice window, empty road, late summer light, a place far from the capital, no people visible")
sc(84, ["vienthuat_t5a"], "Yuan Shu sits alone on a plain low bed in a nearly empty hall with a small bowl of dry barley before him, sighing heavily with a hand over his face, an empty throne seat far in the shadows, dim light, no blood")
sc(85, ["dan", "linh"], "a small group of women and children with a few bundles and an ox cart walks along a quiet road away from a city, heads down, with a few soldiers of a young general watching from a roadside, early morning, a humble end, "+NF)
sc(86, ["hiende_t5", "taotao_t5b", "quan"], "in the hall of Xu the young emperor sits on a low dais with Cao Cao standing at the side holding a bamboo-slip scroll, officials in rows below, wooden pillars, a calm outward order with an unspoken tension")
sc(87, [], "an empty ceremonial dais in a dusty dark hall with a flat-topped crown with bead strings lying alone on a low seat, cobwebs and dust, a single beam of light, a hollow throne")
sc(88, ["liubei_t5"], "Liu Bei sits alone at a low table at night in a room at Xu with a bamboo-slip scroll and a clay oil lamp, looking toward a wooden lattice window with no glass where dark mountains show in the starlight, thoughtful and watchful")

assert sorted(S) == list(range(1, 89)), [i for i in range(1, 89) if i not in S]
assert len(BEATS) == 88

# --- sửa sau khi soi ảnh lần 1 (18/10): thêm câu cấm riêng cho các ảnh lỗi ---
NOTXT = "absolutely no writing, no Chinese characters, no letters on any banner, wall hanging, cloth, armour or object; banners and hangings are plain solid colour"
NOLAMP = "no electric lamp, no lampshade, no glass lantern: if light is needed show only a small shallow open bronze oil dish with a tiny flame"
NOPAPER = "no sheets of paper: writing is only on bamboo-slip scrolls, narrow strips of bamboo tied with cord"
NOCHAIR = "no chair with a back: people sit on straw mats, low benches or low platforms"
NOMAP = "any map is a plain cream cloth with a few simple abstract lines and no coastlines, no continents, no text"
FIX = {
 3: NOTXT+", the hall has no signboard or plaque at all",
 18: NOTXT+", flags are plain with no circles or emblems",
 20: NOLAMP+", "+NOPAPER,
 22: NOTXT+", "+NOMAP+", "+NOLAMP,
 23: NOLAMP+", "+NOPAPER+", "+NOMAP,
 25: NOTXT+", "+NOPAPER+", "+NOCHAIR+", the window is an open wooden lattice with no glass",
 26: NOTXT+", "+NOPAPER+": he reads a rolled bamboo-slip strip",
 27: NOTXT+", "+NOPAPER+", "+NOLAMP+", flags are plain with no emblem",
 32: NOTXT+", no banners with writing on the walls",
 33: NOTXT+", "+NOMAP+", "+NOLAMP,
 34: NOLAMP+", "+NOMAP+", "+NOPAPER,
 38: "flags are plain with no star or emblem",
 41: NOPAPER+", "+NOCHAIR+", "+NOLAMP+", no candle",
 45: NOTXT+", no glass wine glass: a two-eared bronze wine cup only, no wall text",
 46: NOTXT+", "+NOMAP+", "+NOLAMP,
 48: NOTXT+", plain unmarked armour, no signboard on the gate",
 54: NOCHAIR,
 56: NOLAMP+", "+NOPAPER+", "+NOCHAIR+", flags plain with no emblem",
 57: NOLAMP+", "+NOCHAIR,
 58: NOTXT+", "+NOLAMP,
 60: "the pole in the middle of the square is a single straight tall vertical wooden pole with absolutely no crossbar, not a cross, not a T shape",
 61: NOTXT+", "+NOPAPER,
 69: NOTXT+", "+NOLAMP+", "+NOMAP,
 80: NOTXT+", the fallen banner is a plain solid-colour cloth with no characters",
 82: NOTXT+", "+NOPAPER+", "+NOCHAIR+" (clerks sit on low benches at low tables)",
 84: NOCHAIR+" (he sits on a low bed platform), no chair or backrest at all",
 87: "the crown is a Han-style flat-topped ceremonial board hat with hanging bead strings, not a European crown with points or jewels",
 88: NOCHAIR+", "+NOPAPER+", "+NOTXT,
}

# --- lần 2 (dot=2): câu tả điều CẦN CÓ (mô hình bỏ qua câu cấm) ---
BARE = "the walls are bare plastered mud with nothing written or drawn on them, hanging cloths are plain solid colour"
BAM = "bundles of plain narrow bamboo strips tied with cord lie on the low table"
FIX.update({
 3: "light comes from small shallow bronze oil dishes on low stands, hanging cloths are plain solid red and green, the carved dais is a low platform",
 22: "the big cloth hanging behind them is plain blank cream cloth with nothing drawn on it; a small shallow bronze oil dish with a tiny flame on a low table; "+BARE,
 23: BAM+"; "+BARE+"; a small shallow bronze oil dish with a tiny flame",
 25: "he writes with a brush on a long narrow bamboo strip held flat on the table; "+BARE+"; a plain open wooden lattice window",
 26: "he holds a closed bamboo-strip bundle tied with cord; the tent walls are plain canvas lit only by daylight",
 27: "the four men look down at "+BAM+"; "+BARE+"; flags plain solid green and blue; a small shallow bronze oil dish with a tiny flame",
 32: BARE+"; plain cloth hangings of solid dark blue and green",
 33: BARE+"; "+BAM+"; a small shallow bronze oil dish with a tiny flame",
 41: "he writes with a brush on a long narrow bamboo strip; the wooden post by the door is bare wood; a small shallow bronze oil dish with a tiny flame; he sits on a low stool",
 45: "on the low table lie bamboo strips and a two-eared bronze wine cup; "+BARE,
 46: "behind him hangs a plain blank cream cloth with nothing on it, a small shallow bronze oil dish on a low table, flags plain solid colour",
 54: BARE+"; low tables and straw mats, plain solid-colour hanging cloths",
 56: "a small shallow bronze oil dish with a tiny flame lights the low desk; he writes with a brush on a long narrow bamboo strip and sits on a low stool; flag plain solid green",
 61: "he writes with a brush on a long narrow bamboo strip; "+BARE,
 82: BARE+"; clerks sit on low benches and write on bamboo strips with brushes at long low tables",
})

BGRULE = "Every picture has a rich detailed background that fits the place and the story (architecture, landscape, tents, banners, hills), never a plain blank or solid-colour backdrop"
ANTI = ("Strictly Eastern Han dynasty, 2nd century AD, ancient China only: dirt roads and stone paths only (no asphalt, no road markings, no electric poles or wires), "
        "no glass windows (wooden lattice only), no door knobs or handles, no signboards or plaques on gates or buildings, no chairs with backs or modern furniture (people sit on straw mats or low benches), "
        "no candles (clay oil lamps only), no bound paper books and no sheets of paper (only bamboo-slip scrolls tied with cord), no mugs with handles, no lamp posts, no European, Korean or Japanese buildings (Han Chinese grey-tiled mud-brick and timber architecture), "
        "no striped awnings, no baseball caps, no modern shoes (soft cloth shoes, boots or straw sandals), no writing on objects, signs or banners")
SUF = ("cinematic composition that suits the story moment, dynamic framing (wide, medium or low-angle as the scene needs), foreground, middle ground and background all filled, "
       "every person has exactly two arms, two hands and two legs with natural adult proportions, serious weathered faces, no extra limbs, no deformed faces, no text, no letters, no watermark. "
       "Flags and banners are plain solid colour with no symbols. Horses, where present, have four legs and correct anatomy with a simple Han-era saddle cloth and no stirrups. " + BGRULE + ". " + ANTI)

out, canh = [], []
for i in range(1, 89):
    nv, m = S[i]; k = f"{i:03d}"
    canh.append({"key": k, "nv": nv, "mo_ta": m})
    text = BEATS[i - 1]["text"]
    if not nv:
        out.append({"key": k, "cau": i, "nv": [], "text": text, "prompt": m + ((". " + FIX[i]) if i in FIX else "") + ". An empty quiet scene of objects and landscape only. 2D franco-belgian ligne claire comic illustration of ancient China, clean uniform dark ink outlines, flat muted colours with soft shading, earthy palette of ochre, jade green, indigo and warm cream, no text, no numerals, no letters, no watermark, not 3D, not a photo. " + ANTI})
        continue
    ch = "; ".join(NV[x] for x in nv)
    ex = (" " + FIX[i] + ".") if i in FIX else ""
    out.append({"key": k, "cau": i, "nv": nv, "text": text, "prompt": f"{m}.{ex} Characters (keep exactly this look): {ch}. {STYLE}. {SUF}{ex}"})
(R / "TQ5.json").write_text(json.dumps({"ma": "TQ5", "ghi_chu": "Tập 5: Tào Tháo đón hoàng đế về Hứa, Viên Thuật xưng đế", "canh": canh}, ensure_ascii=False, indent=1), encoding="utf-8")
(R / "TQ5_anh.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
dai_cau = {}
for i, (nv, _) in S.items():
    for x in nv:
        if x in TP:
            dai_cau.setdefault(x, []).append(i)
(R / "TQ5_trang_phuc.json").write_text(json.dumps({"ma": "TQ5", "ghi_chu": "Mã trang phục/nhân vật tập 5 (mốc 195-199). NV = {**TQ.json, **TQ2.json nhan_vat_phu, **TQ4_trang_phuc, **TQ5_trang_phuc}. Tạo bởi tao_TQ5.py.",
        "trang_phuc": TP, "dai_cau": {k: v for k, v in dai_cau.items()}}, ensure_ascii=False, indent=1), encoding="utf-8")
print("ok", len(out), "ảnh,", len(TP), "mã nhân vật/trang phục")
