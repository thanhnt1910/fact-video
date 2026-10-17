"""Tạo TQ3.json và TQ3_anh.json (64 prompt vẽ) cho tập 3. Khóa ảnh = số cảnh (001...064). Quy tắc ảnh: xem CLAUDE.md."""
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
 "quanvu": ", always carrying his signature weapon the Green Dragon Crescent Blade (guandao): a very long straight dark-brown wooden pole with two plain gold bands, a small bronze ornate dragon-relief collar at the top, and ONE large, broad, curved single-edged polished silver blade sweeping out from the collar with a notch cut in its back edge, a small pointed brass cap at the bottom end of the pole (exactly as in the weapon reference image, simple and clean), held upright beside him or in one or both hands",
 "trieuphi": ", always carrying his signature weapon the serpent spear (zhangba shemao): a very long straight dark-brown wooden pole with two plain gold bands and a gold ring collar, topped by ONE long straight narrow leaf-shaped silver spearhead with a snake pattern engraved on it, a small steel spike at the bottom end of the pole (exactly as in the weapon reference image, simple and clean, straight blade, no loops), held upright beside him or in one or both hands",
 "liubei": ", wearing exactly ONE straight sword (jian) fully inside a plain dark scabbard at his left hip (a single sword only, never two, never crossed, blade not visible)",
 "lubo": ", carrying his signature weapon the Sky Piercer halberd (Fangtian Huaji): a long pole with a spear point and a crescent blade on one side",
 "taotao": ", a straight sword fully inside its scabbard at his waist (blade not visible)",
 "thaisutu": ", a bow and quiver on his back and a long halberd in hand",
}
for _k in list(NV):
    for _p, _t in WP.items():
        if _k.startswith(_p) and _p in ("quanvu","trieuphi","liubei","lubo","taotao","thaisutu"):
            NV[_k] = NV[_k] + _t
PK = tp["phu_kien"]
STYLE = tq["phong_cach"].replace("year 184 AD", "year 190 AD")
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
EXTRA.update({
 "dingnguyen": "Ding Yuan, a stern broad man of about 50 with a grey beard, dark robe under black-lacquered scale armour, a plain commander's helmet",
 "vuongdoan": "Wang Yun, a thin dignified elderly official of about 55 with a long grey beard and a tall black official cap, deep-brown robe",
 "huchan": "Hu Zhen, a lean anxious commander of about 40 with a thin moustache, grey-blue robe under plain iron armour",
 "tomau": "Zu Mao, a young loyal officer of about 30 with a clean-shaven youthful face, plain brown tunic with leather armour and a red cloth tied on his head",
 "vienthuat": "Yuan Shu, a heavy proud man of about 35 with a round face and a thin beard, rich yellow-brown robe under polished armour, arrogant look",
 "luungu": "Liu Yu, a gentle white-bearded old governor of about 55 in a plain pale-grey robe and a black cap, humble kindly look",
 "hanphuc": "Han Fu, a timid soft-faced man of about 45 with a thin beard, an anxious look, a pale-blue official robe and a black cap",
 "lythuc": "Li Su, a hard-faced officer of about 35 with a short beard, dark armour and a plain helmet",
 "hoangto": "a Jing Province archer commander of about 40 in plain leather armour with a short beard and a bow",
 "dan2": "a mixed group of frightened Han townspeople of all ages, an old man leaning on a stick, women carrying bundles, a boy, a bearded man pulling a handcart, each with a different face and different plain hemp clothes",
})
NV.update(EXTRA)
for k in list(NV):
    if k.startswith("lubo"): pass
LU="lubo_t4a"; DT="dongtrac"; TK="tonkien"; VT="vienthieu"
sc(1,[LU,"quanvu_t4a","trieuphi_t4a","liubei_t4a"],"a dramatic stage-like fight in front of a huge ancient mountain pass fortress gate with grey brick walls and wooden gate towers: Lu Bu in iron armour on a galloping horse swings his halberd while three riders on horses circle him, the one in the middle with a sword, dust and banners flying, wide cinematic view, no blood")
S[1]=(["lubo_t4a","linh"],"a wide cinematic view of a huge ancient mountain pass fortress, grey brick walls and wooden gate towers on a narrow gorge, a lone armoured horseman with a halberd galloping out of the open gate toward three small riders waiting on the plain, dust, plain blank banners, dramatic stage-like light, no blood")
sc(2,["quanvu_t4a"],"Guan Yu in a green robe with a short sword in a scabbard rides out of a camp of tents toward the mountain pass while a general at the tent door holds a steaming bronze wine cup out to him, torches and tents, morning mist, no fighting")
sc(3,[],"a wide painted-scroll style view of the great Han pass fortress and a long ancient history archive room with stacked bamboo-slip scrolls tied with cord on low shelves, a low table and a clay oil lamp, no people, a feeling of searching")
sc(4,["quanvu_t4a","liubei_t4a"],"ONE single picture of exactly two men only, standing side by side on a low hill in a northern plain looking toward the far west: on the left Guan Yu, tall with a long black beard in a green robe holding his guandao upright, on the right Liu Bei, slightly shorter with a thin beard in a dark-blue robe with one sword in a scabbard at his hip, clearly different faces and clothes, a simple camp of a few small tents below them, a long road across the plain, dusk")
sc(5,["dongtrac","linh"],"the great palace city of Luoyang in the year 189: Dong Zhuo, a huge fat man in a dark fur-trimmed robe, rides in through the city gate at the head of a long column of Xiliang cavalry in fur-trimmed leather, townspeople watching nervously from the roadside, grey tiled palace roofs behind, plain blank banners")
sc(6,["dingnguyen","linh"],"the commander of the capital guard Ding Yuan, a stern grey-bearded man in black scale armour, stands before a long ranked formation of the capital soldiers in a barracks courtyard, a drill ground with wooden racks of spears, Luoyang walls behind, calm tense morning, no fighting")
sc(7,[LU,"dingnguyen"],"in a dim tent at night the young tall Lu Bu in armour stands behind the seated Ding Yuan who is reading a bamboo-slip scroll by a clay oil lamp, Lu Bu's shadow long on the tent wall, Lu Bu's hand resting still at his side, a tense quiet moment, no violence")
sc(8,[LU,"dongtrac"],"in a grand hall, Dong Zhuo seated on a low platform smiling and putting a hand on the shoulder of kneeling Lu Bu in armour who offers a closed black cloth bundle, the two clasp hands as if father and son, officers in rows watching, wooden pillars, oil lamps, plain hangings")
sc(9,["linh"],"a vast barracks outside Luoyang where many ranks of soldiers in iron armour kneel and then stand under plain dark blank banners, a bare wooden platform with an empty seat in front of them, an old city wall behind, evening light, no single hero in front, only soldiers of different faces")
sc(10,[VT,"dongtrac"],"in a great palace hall officials in black caps sit in two rows, Dong Zhuo on the platform with an angry thick face pointing, while the handsome young Yuan Shao stands upright holding his sheathed sword horizontally across his chest and bowing deeply, ready to walk out, wooden pillars, oil lamps")
sc(11,[VT],"Yuan Shao on a horse with a few attendants rides alone out through the east gate of Luoyang at dawn along a dirt road toward distant hills, the city walls behind him, the calm of a man who has chosen to leave")
sc(12,["dongtrac","linh"],"Dong Zhuo in a splendid dark robe and a high official cap walks up the stone steps of a palace hall wearing shoes and a sheathed sword while the bowing officials on both sides do not announce his name, rows of guards, palace roofs, grey stone, a feeling of unchecked power")
sc(13,[],"the same empty palace hall at dusk with rows of empty low seats and one empty seat at the head, a clay oil lamp flickering, long shadows from wooden pillars, an open doorway toward a far road, no people")
sc(14,[VT,"vienthuat","taotao_t4","congtonton"],"a large open-air council on a plain where regional lords gather in a camp of tents: the handsome Yuan Shao stands in the middle on a low earth platform, other lords in different armour and robes stand around him in a half circle, blank colourful banners, many soldiers behind, a sense of a great alliance")
sc(15,["linh"],"the allied camp in the evening: rows of tents and cooking fires, groups of soldiers sitting under their own plain blank banners each far from the others, none moving forward, a long empty road toward the west, smoke from fires, different faces among the soldiers")
sc(16,[TK,"linh"],"Sun Jian in a red headband, red robe and iron armour leads a long column of southern soldiers marching west along a dirt road through green hills toward distant Luoyang, red-brown plain banners, dust, determined faces")
sc(17,["dan2"],"a southern river bank where several rough pirates of different looks sit around heaps of goods and cloth bundles taken from merchants, in the background a boat with a middle-aged father and his seventeen-year-old son standing on the deck looking at the shore, river, reeds, early light")
sc(18,["dan2"],"on a sandy river bank a Han-era seventeen-year-old youth with a topknot and a plain cloth headband, in a short brown-grey hemp tunic with narrow sleeves and a rope belt, soft cloth shoes, holds ONE straight double-edged Han jian sword raised in his right hand and points his left hand to the opposite side as if signalling hidden troops east and west; around him six or seven rough grown MEN pirates of different looks (bearded, scarred, bald, wearing ragged vests) drop sacks and cloth bundles taken from merchants and scatter in panic along the shore, a river with a boat in the distance, reeds, early light, no women, no children, no old people, no fighting, no blood, no katana, no kimono, no bound books or paper, full-bleed picture with no white margin")
sc(19,[TK,"linh"],"the mature Sun Jian in armour on a hill at the head of his army looking west toward the distant walls of Luoyang with the wind in his red headband, soldiers resting on the slope behind him, a bold calm expression")
sc(20,[TK,"vienthuat"],"in the town of Luyang, Yuan Shu in rich armour sits in a hall and hands a sealed bamboo document to Sun Jian who stands bowing with his red headband, officials of Yuan Shu's court watching, wooden pillars, oil lamps, straw mats")
sc(21,[TK,"vienthuat"],"a hall scene in which Sun Jian stands slightly lower than the proud Yuan Shu who sits on a low platform, Sun Jian's own plain red banner stands behind Yuan Shu's yellow banner, blank banners, a feeling that one serves another")
sc(22,["dongtrac","tuongquan"],"Dong Zhuo, a huge fat man, sits in a hall speaking to a general with a half-smile, his hand turned out in a gesture of grudging respect, a map on a low table, an oil lamp, officers listening, wooden pillars")
sc(23,[TK,"linh"],"a battlefield east of the Liang town: a big army in plain red-brown armour of Dong Zhuo's Xiliang cavalry sweeps down a slope against a smaller column of Sun Jian's soldiers who stand together under red banners, dust, smoke, spears, no blood, no one fallen")
sc(24,[TK,"kybinh"],"Sun Jian on a galloping horse with a few dozen riders breaks out of the ring of enemy cavalry across a dusty field, his red headband streaming behind him, enemy horsemen around the edges, dust, wide action shot, no blood")
sc(25,[TK,"tomau"],"in the middle of the dusty ring of cavalry, Sun Jian takes off his red headband and hands it to the young officer Zu Mao who ties it onto his own head, Zu Mao's face determined, enemy riders closing in at the edge, a burnt field, no blood")
sc(26,["tomau"],"Zu Mao dismounted among old graves and a burnt wooden post at dusk, placing a red cloth headband upon the scorched post and creeping off into tall grass, grey stone mounds, a lone horse beside him, smoke")
sc(27,["kybinh","linh"],"enemy horsemen in fur-trimmed leather ride in a circle around a scorched wooden post with a red cloth on it, one rider leaning down to look closely, others turning their horses away in puzzlement, burnt ground, graves, evening light")
sc(28,[TK,"linh"],"Sun Jian in armour gathering his scattered soldiers on a hill at dawn, spears upright, red banners being raised again one by one, an officer reporting to him, a quiet determination, mist in the valley")
sc(29,["huchan",LU],"in a Dong Zhuo army camp, Hu Zhen in grey-blue robe stands before a map while several officers at the side turn their faces away with disdainful looks and Lu Bu in iron armour stands with arms folded apart from them, tents, torches")
sc(30,[LU,"linh"],"Lu Bu on horseback at night in front of a group of horsemen and a gate, one rider pointing back toward a distant walled town as if spreading a false rumour, torches and shadows, the sense of a whispered lie spreading through the camp")
sc(31,["huchan",TK],"a night field with Dong Zhuo's army in disorder, riders turning their horses in confusion and colliding, torches scattered, while a steady Sun Jian line with red banners advances in the background, dust, no blood")
sc(32,[],"a plain wooden table in a camp tent with a bamboo-slip scroll that is opened and a clay oil lamp, a few short sentences on the slips unreadable, a quiet empty tent, a wine cup, no people")
sc(33,["quanvu_t4a","liubei_t4a"],"ONE single picture of exactly two men only, standing side by side before a modest northern camp: on the left Guan Yu with a long black beard in a green robe holding his guandao upright, on the right Liu Bei with a thin beard in a dark-blue robe with one sword in a scabbard at his hip, clearly different faces and clothes, both looking toward the far mountains in the west, small tents behind them, wide quiet sky")
sc(34,[],"a bare ancient courtyard with a table holding a steaming bronze wine cup and a plain unlit lamp, wooden pillars with plain blank red hangings, quiet and empty, no people")
sc(35,[],"the ancient mountain pass fortress of Hulao on a narrow gorge: grey brick walls, wooden gate towers, a dirt road and quiet rocky hills, plain blank banners on the walls, mist, no people on the road")
sc(36,["linh"],"the burning of the palaces of Luoyang: tall columns of smoke rise from the wooden halls behind the city wall, a long caravan of carts and mounted soldiers escorting a covered carriage west along the road, townspeople driven along the roadside, dark sky, no blood")
sc(37,[TK,"linh"],"Sun Jian walking with a few soldiers through the ruins of a Han palace city: charred pillars, fallen roof tiles and ashes, he stoops to lift an old stone tablet, his officers shovelling earth to fill the open holes beside burial mounds, grey light, solemn mood")
sc(38,[TK,"linh"],"soldiers by an old stone well in the ruins at dawn: a soldier on a rope is lifted out of the well holding a small bundle wrapped in red cloth, Sun Jian waiting at the well edge with his hands out, burnt walls around, a lamp, solemn tension")
sc(39,["vienthuat"],"a hall scene with Yuan Shu in yellow-brown robe sitting greedily upright on a platform, officials at his side whispering, a small square jade seal on a low table in front of him in soft light, hangings, oil lamps")
sc(40,["vienthuat"],"Yuan Shu in his hall hearing a thin adviser whispering in his ear, a map on the low table, wooden pillars, suspicious expression, oil lamps, straw mats, a wary mood")
sc(41,[TK,"vienthuat"],"ONE single picture without panels or frame lines: inside a canvas tent Sun Jian in armour with a red headband kneels on the earth floor drawing lines in the ground with a stick to show a plan, while Yuan Shu in a yellow-brown robe stands over him with his arms folded, torches on poles and tent flaps, night")
sc(42,["linh","dan"],"allied soldiers of different lords sit around separate fires on a plain, watching each other across the dark ground, wary looks, spears piled apart, tents in clusters of different colours, a cold night, smoke")
sc(43,[TK,"hoangto"],"a mountain slope at dusk with Sun Jian riding alone on a horse up a narrow path toward the ridge, archers hidden among rocks and trees watch him pass in silence, a river valley and walls of Xiangyang far below, no violence shown")
sc(44,[],"a green mountain ridge near a river with a lone riderless horse standing on the path in the evening light, a red cloth headband caught on a bush, mist, quiet, no people")
sc(45,[],"the south of China: the broad Yangtze river with a pair of sailing boats, green hills, a small river port with grey tiled roofs and boats moored, rising sun, a hopeful distance")
sc(46,["linh"],"the allied camp breaking up in the morning: tents being folded, officers and soldiers heading in different directions along several dirt roads, carts and horses, plain blank banners lowered, a feeling of everyone going their own way")
sc(47,["vienthieu","hanphuc","luungu"],"a council in a northern hall: Yuan Shao and Han Fu speak earnestly to old Liu Yu who sits on a low platform shaking his head with both palms raised, officials in black caps around, wooden pillars, oil lamps")
sc(48,["hanphuc","congtonton"],"a northern plain with Gongsun Zan on a white horse leading a long column of cavalry in fur-trimmed armour toward a walled city in the distance, on the city wall the timid Han Fu looking down in worry, plain blank white banners, dust")
sc(49,["vienthieu","congtonton"],"a wide field between two rivers where two armies face each other in lines of infantry and horsemen under two plain banners, one with Yuan Shao among his officers, the other with Gongsun Zan on a white horse, a stone bridge between them, dust, no fighting shown")
sc(50,["liubei_t4a","congtonton"],"Liu Bei in a dark-blue robe with one sword in a sheathed scabbard stands with his old schoolmate Gongsun Zan in a modest northern county office, a map of the north laid on a low table, a small hall with wooden pillars and a straw mat floor, Liu Bei's humble pose")
sc(51,["liubei_t4a","quanvu_t4a","trieuphi_t4a"],"ONE single picture: Liu Bei in a dark-blue robe stands in front in the centre before the modest wooden gate of Pingyuan county; just behind him on the left stands Guan Yu, tall with a long black beard in a green robe and a guandao, and on the right Zhang Fei, stocky with a bushy black beard and a serpent spear; clearly different faces and clothes; a few county officials around, a flat northern plain, calm morning light")
sc(52,["linh"],"the huge fortress of Mei Wu being built in the Chang'an region: thick earthen walls as high as a city wall, workers hauling stones and carts of grain up ramps, long rows of granary storehouses with grey roofs, soldiers overseeing, dust, no whipping")
sc(53,["dongtrac",LU],"inside the fortress, Dong Zhuo stands before a vast granary of piled grain sacks and clay jars with satisfaction, in the background at the doorway Lu Bu in armour watches him with a still hard stare, oil lamp flickers between them")
sc(54,["dongtrac",LU],"a hall scene where Dong Zhuo angrily lifts a long-handled halberd as if to throw it while Lu Bu stands frozen with his head turned away, officials around freeze and look aside, wooden pillars, oil lamps, no one hit, no blood")
sc(55,[LU],"in a quiet lamp-lit inner courtyard of a Han mansion, Lu Bu in a dark robe stands alone near a plain screen looking uneasily over his shoulder at a closed door, a covered corridor and a stone path, a sense of a secret, no other person visible")
sc(56,["vuongdoan",LU,"lythuc"],"a night council in a small room: elderly Wang Yun in a black cap speaks in a low voice to Lu Bu and two other officers around a low table under a clay oil lamp, close heads, wooden pillars, straw mats, hanging plain cloth, a conspiracy feel")
sc(57,[LU,"lythuc"],"the Weiyang palace gate at dawn: tall plain wooden gate towers with a blank gate and no plaque, a stone road with a line of palace guards in plain dark armour and a hard-faced officer among them, an empty ox-drawn wooden cart waiting before the gate (no car, no truck), grey light, solemn silence, nothing violent shown")
sc(58,[LU],"Lu Bu stands alone in armour at the top of the stone steps of the palace gate looking down, in front of him an empty carriage and a spilled silk cloak on the steps, a long shadow, the morning wind, a quiet heavy ending, no blood")
sc(59,[TK],"Sun Jian in a red headband and iron armour standing on a river bank before a small walled town after a battle, his soldiers resting beside red-brown plain banners, a cloth-covered captured helmet on a stone, calm victory mood, no fighting")
sc(60,["quanvu_t4a","liubei_t4a"],"ONE single picture of exactly two men only: Guan Yu with a long black beard in a green robe and Liu Bei in a dark-blue robe sit side by side on a low bench at the door of a modest wooden house in a Han village on the northern plain, Guan Yu's guandao leaning on the wall, an old farmer pouring water, hills and a dirt road behind, Han Chinese architecture only, no churches, no towers, no European buildings")
sc(61,[],"a wide misty plain with a few plain blank banners fluttering over distant tents, a few long shadows of walking men across the road, a heavy cloud-filled sky, quiet and sorrowful, no people near")
sc(62,["liubei_t4a"],"Liu Bei in a dark-blue robe stands alone at the top of the earth wall of Pingyuan looking east over the plain at dusk, a smoke-grey sky, his small figure against the horizon, a single sword in its scabbard at his hip")
sc(63,["liubei_t4a"],"Liu Bei on horseback with a few riders on a long eastern road toward distant hills and rivers under a large sky, a messenger riding toward him from the far end of the road carrying a rolled bamboo document, soft golden light")
sc(64,[],"an old Han city gate on a road in the early morning with a rising sun behind misty hills, the road empty and long, birds in the sky, a quiet closing image, no people")
for i in range(1,65): assert i in S, i

BGRULE = "Every picture has a rich detailed background that fits the place and the story (architecture, landscape, tents, banners, hills), never a plain blank or solid-colour backdrop"
ANTI = ("Strictly Eastern Han dynasty, 2nd century AD, ancient China only: dirt roads and stone paths only (no asphalt, no road markings, no electric poles or wires), "
        "no glass windows (wooden lattice only), no door knobs or handles, no signboards or plaques on gates or buildings, no chairs with backs or modern furniture (people sit on straw mats or low benches), "
        "no candles (clay oil lamps only), no bound paper books and no sheets of paper (only bamboo-slip scrolls tied with cord), no mugs with handles, no lamp posts, no European, Korean or Japanese buildings (Han Chinese grey-tiled mud-brick and timber architecture), "
        "each person carries at most ONE sword (a single straight sword either sheathed at one hip or held in one hand), never two swords on one person, never crossed swords, never a sword plus extra blades, "
        "a sword worn at the hip or back is ALWAYS fully inside its scabbard, only the hilt and the scabbard are visible, a bare blade is drawn ONLY when the person holds the sword in his hand, "
        "no two people in the picture look the same: every person has a different face, age, hair, beard and clothing colour, no clones, no twins, no repeated faces, "
        "no striped awnings or canopies, no ceiling lamps, no desk lamps, no hanging signs, windows are plain square openings with vertical wooden bars only and no glass panes and no paper panes, roofs have heavy straight ridges and gently sloped eaves, not upturned curved Korean or Japanese eaves, no plaques, no bench with a backrest, no writing or Chinese characters anywhere (blank plain gates, blank banners, blank hanging cloths, blank scroll surfaces), no electric poles or wires, no baseball caps, no modern shoes (soft cloth shoes, boots or straw sandals), no writing on objects, signs or banners, "
        "ALL flags, banners, cloths, plaques and walls are completely blank: no symbols, no emblems, no characters, no pseudo-writing, no calligraphy; "
        "no lanterns hanging from poles, eaves or ceilings and no street lamps (light only from small clay oil lamps on tables and from torches), "
        "windows are ONLY plain small square holes in thick mud-brick walls with a few vertical wooden bars (no lattice grids, no sliding frames, no glass); "
        "roofs are plain, low, heavy, grey-tiled with a straight ridge and NO upturned corners and NO decorative ridge ornaments, buildings are simple rustic Han-era mud-brick and timber (not Korean hanok, not Japanese); "
        "full-bleed picture with no border, no frame and no white margin")
SUF = ("cinematic composition that suits the story moment, dynamic framing (wide, medium or low-angle as the scene needs), foreground, middle ground and background all filled, "
       "every named hero's signature weapon is clearly visible and drawn exactly as described, every person has exactly two arms, two hands and two legs with natural adult proportions, serious weathered faces, no extra limbs, no deformed faces, no text, no letters, no watermark. "
       "Flags and banners are plain solid colour with no symbols. " + BGRULE + ". " + ANTI)
EXTRA_PK = lambda i, x: ""

TRIO = set()
import os as _os
RD = R / "refs"
REF_OF = {"tonkien": ["tonkien"], "lubo": ["lubo_cd"], "dongtrac": ["dongtrac"], "vienthieu": ["vienthieu"], "vienthuat": ["vienthuat"], "dingnguyen": ["dingnguyen"], "vuongdoan": ["vuongdoan"], "tomau": ["tomau"], "huchan": ["huchan"]}
REF_TXT = {"tonkien": "the face, hair, beard, build and clothing of Sun Jian (keep them exactly, this is the same person in every picture)", "lubo_cd": "the face, hair, beard, build and clothing of Lu Bu (keep them exactly, this is the same person in every picture)", "dongtrac": "the face, hair, beard, build and clothing of Dong Zhuo (keep them exactly, this is the same person in every picture)", "vienthieu": "the face, hair, beard, build and clothing of Yuan Shao (keep them exactly, this is the same person in every picture)", "vienthuat": "the face, hair, beard, build and clothing of Yuan Shu (keep them exactly, this is the same person in every picture)", "dingnguyen": "the face, hair, beard, build and clothing of Ding Yuan (keep them exactly, this is the same person in every picture)", "vuongdoan": "the face, hair, beard, build and clothing of Wang Yun (keep them exactly, this is the same person in every picture)", "tomau": "the face, hair, beard, build and clothing of Zu Mao (keep them exactly, this is the same person in every picture)", "huchan": "the face, hair, beard, build and clothing of Hu Zhen (keep them exactly, this is the same person in every picture)", "trio": "the lineup of the three sworn brothers standing side by side: Guan Yu on the LEFT, Liu Bei in the CENTRE, Zhang Fei on the RIGHT (keep this left-to-right order, their faces, beards, headwear and drawing style)",
           "quanvu": "the face, long black beard, cap, build and drawing style of Guan Yu (keep them exactly)",
           "trieuphi": "the face, bushy black beard, headscarf, build and drawing style of Zhang Fei (keep them exactly)",
           "liubei": "the face, thin beard, long earlobes, build and drawing style of Liu Bei (keep them exactly, but dress him in the costume described below)",
           "guandao": "Guan Yu's weapon, the Green Dragon Crescent Blade (draw his weapon exactly like this, plain and simple; the reference shows the weapon only: do NOT draw its stand or pedestal)",
           "xamau": "Zhang Fei's weapon, the serpent spear (draw his weapon exactly like this, straight narrow leaf blade; the reference shows the weapon only: do NOT draw its stand or pedestal)",
           "hoatich": "Lu Bu's weapon, the Sky Piercer halberd (draw his weapon exactly like this, straight narrow leaf blade; the reference shows the weapon only: do NOT draw its stand or pedestal)"}
def refs_for(nv):
    names = []
    for x in nv:
        for pre, lst in REF_OF.items():
            if x.startswith(pre):
                for n in lst:
                    if n not in names and (RD / f"{n}.jpg").exists():
                        names.append(n)
    names.sort(key=lambda n: 0 if n in ("quanvu", "trieuphi", "liubei") else 1)
    names = [n for n in names if n != "guandao" or "quanvu" in names][:3] if False else names
    return names[:2]
def ref_guide(names):
    if not names:
        return ""
    return "Reference images are provided: " + "; ".join(f"image {i+1} shows {REF_TXT[n]}" for i, n in enumerate(names)) + ". The references are ONLY for faces, hair, beards, body proportions, weapon shapes and the flat clean comic drawing style: do NOT copy their backgrounds or poses, do NOT draw the reference pictures themselves, and do NOT add any person who is not named in the scene description. "
FIXKEYS = set()
def FIXPRE(i):
    if i not in FIXKEYS:
        return ""
    return ("ABSOLUTE RULES FOR THIS PICTURE: every flag, banner, hanging cloth, scroll on a wall, plaque and wall surface is a completely blank plain surface with no marks, no characters, no pseudo-writing; "
            "there are no hanging lanterns or lamps on walls, only small clay oil lamps on tables; houses are low plain mud-brick and timber with simple straight grey-tile roofs and tiny square windows with a few wooden bars; "
            "any sword at a hip is fully inside its scabbard. ")
out, canh = [], []
for i in range(1, 65):
    nv, m = S[i]; k = f"{i:03d}"
    canh.append({"key": k, "nv": nv, "mo_ta": m})
    if not nv:
        out.append({"key": k, "nv": [], "prompt": FIXPRE(i) + m + ". An empty quiet scene of objects and landscape only. 2D franco-belgian ligne claire comic illustration of ancient China, clean uniform dark ink outlines, flat muted colours with soft shading, earthy palette of ochre, jade green, indigo and warm cream, no text, no numerals, no letters, no watermark, not 3D, not a photo. " + ANTI})
        continue
    named = [x for x in nv if x not in EXTRA]
    if i in TRIO:
        pos = {"quanvu_t4a":"LEFT","quanvu_t4b":"LEFT","liubei_t4a":"CENTRE","liubei_t4b":"CENTRE","liubei_t4c":"CENTRE","trieuphi_t4a":"RIGHT","trieuphi_t4b":"RIGHT"}
        nv = sorted(nv, key=lambda x: {"LEFT":0,"CENTRE":1,"RIGHT":2}.get(pos.get(x),3))
        ch = "; ".join((pos[x] + " of the three: " if x in pos else "") + NV[x] for x in nv)
    else:
      ch = "; ".join(NV[x] + ((", " + EXTRA_PK(i, x)) if EXTRA_PK(i, x) else "") for x in nv)
    rf = refs_for(nv)
    out.append({"key": k, "nv": nv, "refs": rf, "prompt": f"{FIXPRE(i)}{ref_guide(rf)}{m}. Characters (keep exactly this look): {ch}. {STYLE}. {SUF}"})
(R / "TQ3.json").write_text(json.dumps({"ma": "TQ3", "ghi_chu": "Tập 3: Hổ Lao, Dương Nhân, Lạc Dương", "canh": canh}, ensure_ascii=False, indent=1), encoding="utf-8")
V = []
for it in out:
    if int(it["key"]) in TRIO or int(it["key"]) == 0:
        for v in (1, 2, 3, 4):
            V.append({**it, "key": str(v * 1000 + int(it["key"]))})
import os
if os.environ.get("BIENTHE"):
    out = out + V
(R / "TQ3_anh.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print("ok", len(out), "ảnh;", len([c for c in canh if c['key'] not in KEEP]), "ảnh cần vẽ lại")


