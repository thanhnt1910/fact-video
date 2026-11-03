import json, re
HAN=("2D ligne claire comic art, Eastern Han China around 208 AD, clean dark ink outlines, bright vivid clean colours with soft shading, luminous natural light, rich saturated palette, ornate fine details, realistic adult proportions, elegant richly decorated silk robes with embroidered borders and patterns, authentic Han cross-collared cut and topknots, grey-tiled mud-brick houses with wooden lattice windows (no glass), full-bleed single picture, no border")
SONG=("2D ligne claire comic art, Song dynasty China around 1080 AD, clean dark ink outlines, bright vivid clean colours with soft shading, luminous natural light, rich saturated palette, ornate fine details, realistic adult proportions, elegant richly decorated silk long robes with wide sleeves and embroidered borders, wooden shopfronts with grey tiled roofs and wooden lattice windows (no glass), full-bleed single picture, no border")
W=" bright warm golden daylight, vibrant rich colours, cheerful luminous mood. "
C=" bright clear soft daylight, fresh clean vivid colours (not grey, not dim, not gloomy). "
F=" glowing vivid orange flames against a deep luminous blue night, vivid saturated colours. "
NV={
"zy":"Zhou Yu at about thirty-three, a handsome slim man with fine features, a thin moustache and a short neat beard, black hair in a topknot under a black cap, deep-teal long robe with a dark leather chest guard and a dark sash, empty hands",
"zyy":"young Zhou Yu at about twenty-four, handsome and clean-shaven, black topknot, deep-teal robe with a dark sash, empty hands",
"sc":"Sun Ce at about twenty-four, a stocky energetic young man with a short stubble beard and a broad grin, red-brown robe with a dark sash, empty hands",
"sq":"Sun Quan at about twenty-six, a young ruler with a square face and a short beard, dark-purple robe with gold trim, black ceremonial cap, empty hands",
"cc":"Cao Cao at about fifty-three, a short wiry man with sharp clever eyes, a thin moustache and a small beard with a few grey hairs, dark charcoal robe with a dark sash, black cap, empty hands, no weapon",
"hg":"Huang Gai, a tough old general of about sixty with a grey beard and weathered face, dark brown robe with a leather chest guard, empty hands",
"ls":"Lu Su, a stout calm man of about thirty-seven with a round kind face and a plain moustache, grey-green robe, empty hands",
"zgl":"Zhuge Liang at about twenty-seven, a tall slim man with a calm intelligent smile and a thin moustache, white-and-blue robe, a plain cloth scarf cap, empty hands",
"cr":"Cao Ren, a stern general of about fifty with a square jaw and a short black beard, dark robe with a leather chest guard, black cap",
"cp":"Cheng Pu, an old rugged officer with a grey beard and a scarred cheek, dark brown robe with a leather chest guard",
"lb":"Liu Bei at about forty-eight, a mild man with long earlobes and a faint moustache, plain green robe, empty hands",
"gy":"Guan Yu, a tall man with a very long black beard and a red face, green robe, empty hands",
"zf":"Zhang Fei, a burly man with a bristling black beard and wide eyes, dark robe, empty hands",
"ps":"Pei Songzhi, an elderly annotator of about sixty with a thin grey beard, plain grey robe and a black cap, gentle focused face",
"cs":"Chen Shou, a calm scholar-historian of about fifty in a plain dark robe and black cap, thoughtful face",
"kc":"a Song street storyteller of about fifty, thin face, short grey beard, plain brown long robe, simple black cloth cap",
"dan":"townspeople of different ages and faces in plain tunics, each face different",
"sb":"a Han soldier in a plain cloth tunic with a leather chest guard, simple face",
}

NV.update({
"zy":"Zhou Yu at about thirty-three, a handsome slim man with fine features, a thin moustache and a short neat beard, black hair in a topknot under a black silk cap with a jade pin, a deep-teal silk long robe with gold-embroidered cloud-pattern borders, a polished dark-leather and bronze chest guard with gold studs, a jade-buckled belt, empty hands",
"zyy":"young Zhou Yu at about twenty-four, handsome and clean-shaven, black topknot with a jade pin, a deep-teal silk robe with gold-embroidered borders and a jade belt, empty hands",
"sc":"Sun Ce at about twenty-four, a stocky energetic young man with a short stubble beard and a broad grin, a crimson silk robe with gold-thread borders and a dark jade belt, empty hands",
"sq":"Sun Quan at about twenty-six, a young ruler with a square face and a short beard, a purple silk robe with embroidered gold dragon-pattern borders and a jade belt, a tall black ceremonial cap, empty hands",
"cc":"Cao Cao at about fifty-three, a short wiry man with sharp clever eyes, a thin moustache and a small beard with a few grey hairs, a rich black silk robe with crimson borders and gold-thread embroidery, a jade belt, a tall black official cap, empty hands, no weapon",
"hg":"Huang Gai, a tough old general of about sixty with a grey beard and weathered face, a rich brown silk robe with embroidered borders under bronze-studded leather armour, empty hands",
"ls":"Lu Su, a stout calm man of about thirty-seven with a round kind face and a plain moustache, a sage-green silk robe with embroidered borders and a jade belt, empty hands",
"zgl":"Zhuge Liang at about twenty-seven, a tall slim man with a calm intelligent smile and a thin moustache, a white silk robe with sky-blue embroidered borders and a blue silk sash, a cloth scarf cap, empty hands",
"cr":"Cao Ren, a stern general of about fifty with a square jaw and a short black beard, a dark-red silk robe with a polished leather and bronze chest guard",
"cp":"Cheng Pu, an old rugged officer with a grey beard and a scarred cheek, a deep-brown silk robe with a bronze-studded leather chest guard",
"lb":"Liu Bei at about forty-eight, a mild man with long earlobes and a faint moustache, an emerald-green silk robe with gold borders, empty hands",
"gy":"Guan Yu, a tall man with a very long black beard and a red face, a bright green silk robe with gold borders, empty hands",
"zf":"Zhang Fei, a burly broad-faced man with a short bristling black beard and wide eyes, a dark-blue silk robe with silver borders, empty hands",
"ps":"Pei Songzhi, an elderly annotator of about sixty with a thin grey beard, a soft blue-grey silk robe with a black cap, gentle focused face",
"cs":"Chen Shou, a calm scholar-historian of about fifty in a deep-indigo silk robe with embroidered borders and a black cap, thoughtful face",
"kc":"a Song street storyteller of about fifty, thin face, short grey beard, a rust-brown silk long robe with embroidered borders, a soft cloth cap",
"dan":"townspeople of different ages and faces in colourful tunics in blue, ochre, green and rust, each face different",
"sb":"a Han soldier in a neat blue-grey or olive tunic with a polished leather chest guard, simple face",
})
# (so cau, nv, ton, era, mo ta)
S=[
(1,["zy"],W,"H","exactly ONE man only: Zhou Yu standing at the bow of a large warship on a broad river at sunset, behind him the burned wreck of an enemy fleet and drifting smoke, proud calm face, sleeves hiding both hands, no second figure"),
(2,["zy","zgl"],C,"H","two men facing each other across a low table in a tent, Zhou Yu in a teal robe glaring with a tight jaw and Zhuge Liang in a white-and-blue robe smiling calmly, clearly different faces and colours, opposite attitudes"),
(3,["zy"],C,"H","exactly ONE large man in the foreground: Zhou Yu seated on a mat at a low table with a tight jaw and narrowed jealous eyes, looking aside through the tent opening where a tiny white-robed figure stands far away in the camp, no second close figure"),
(4,["zy","zgl"],C,"H","Zhou Yu bending over a sand-table model of a river and hills in a tent, pointing to a small flag with a scheming smile, while outside the open tent door Zhuge Liang calmly strolls past with a knowing smile and sleeves hiding his hands, two clearly different faces"),
(5,["zy","sb"],F,"H","Zhou Yu staggering backward clutching his chest with a pained face, two officers rushing to catch him under his arms, dust and torch light, no blood, wide view, officers with different faces"),
(6,["kc","dan"],W,"S","a storyteller on a low platform in a Song market street telling a tale with an open hand, a crowd of townspeople nodding and smiling in satisfaction, shopfronts behind, a gentle bright afternoon"),
(7,["ps"],C,"H","exactly ONE scholar sitting at a plain low table with a hand on his chin and a doubtful raised eyebrow, a tied bundle of bamboo slips in front of him and a plain empty bed behind him, no second figure"),
(8,[],C,"H","three tied bundles of different sizes on a plain wooden table: one neat and plain, one with extra small bundles attached, one wrapped in coloured cloth, soft light through a lattice window, completely empty, absolutely no people"),
(9,[],W,"H","a mother holding a swaddled baby at the doorway of a well-off Han country house in Lujiang, her husband standing beside her with a proud smile, rice fields and green hills behind, two clearly different faces"),
(10,["zyy","sc"],W,"H","two young men of the same age side by side under a tree, arms on each other's shoulders, laughing, Zhou Yu slim in a teal robe and Sun Ce stocky in a red-brown robe, clearly different faces"),
(11,["zyy","sc"],W,"H","Zhou Yu opening the gate of a big courtyard mansion and sweeping his sleeve to invite Sun Ce in, Sun Ce bowing in thanks, a big house with tiled roofs on the south side of a country road, two different faces"),
(12,["zyy","sc"],W,"H","Zhou Yu walking out of the big mansion gate carrying a small cloth bundle with a light easy smile, while behind him in the courtyard Sun Ce is cheerfully unrolling a sleeping mat, two different faces and robes"),
(13,["zy","dan"],W,"H","a banquet hall with musicians: Zhou Yu holding a two-eared bronze wine cup turning his head sharply to look over his shoulder at a zither player who has played a wrong note and looks guilty, other guests unaware, three different faces"),
(14,["zy"],C,"H","exactly ONE man: Zhou Yu bending over a sand-table model of a river and hills in his tent, placing small plain blank flags on the model with careful focus, no second figure"),
(15,["sb"],C,"H","winter on the north bank of a wide river, a vast column of Cao army soldiers with plain blank banners marching down toward the water through light snow, tiny figures, wide view, grey sky"),
(16,["cc","sb"],C,"H","Cao Cao standing on a tall earthen platform with one arm raised proclaiming to an enormous army of tiny soldiers spread across the riverbank to the horizon, plain blank banners, wind in his sleeves"),
(17,["sb"],C,"H","northern soldiers worn out in a muddy riverside camp in cold rain: some slumped on the ground, some hunched and seasick at a ship rail, banners drooping, tired faces, each soldier different"),
(18,["sb"],C,"H","a rank of southern surrendered soldiers standing apart from the others, glancing at each other and whispering uncertainly toward a distant plain flag, wary faces, each face different, grey light"),
(19,["zy","sq"],W,"H","Zhou Yu bowing with hands joined before Sun Quan who sits on a low mat in a hall and nods, Zhou Yu in a teal robe and Sun Quan in dark purple, clearly different faces, two attendants far behind"),
(20,["zy","sb"],W,"H","Zhou Yu on a horse leading a long column of thirty thousand soldiers along a riverside road toward a distant river town, plain blank banners, dust, wide view, soldiers small"),
(21,["zy"],C,"H","a broad river: on the far right a huge enemy fleet filling the whole horizon with countless sails, on the left a small fleet of only a few ships, Zhou Yu tiny on the nearest deck looking calm, wide view"),
(22,["hg"],F,"H","exactly ONE old general: Huang Gai standing on a warship deck at dusk pointing toward the enemy fleet across the river with a sly sudden idea in his eyes, no second close figure, ships far away"),
(23,["sb"],F,"H","a row of small fast boats at a quay at dusk, sailors piling dry brushwood and straw onto them and pouring oil from clay jars, determined faces, each sailor different"),
(24,["sb"],F,"H","a line of small boats rushing across the middle of the river with sails swollen by a strong south-east wind, the lead boat's bow just catching flame, flags streaming, spray, dusk"),
(25,[],F,"H","the whole enemy fleet burning on the river at night, towering flames and black smoke filling the sky, tiny figures and a few small horses far away in the water, reflections of fire on the river, wide view"),
(26,["sb"],C,"H","defeated soldiers trudging along a muddy road through reeds at night toward a distant walled city, plain lowered banners, small tired figures, smoke far behind, wide view"),
(27,["zy","sb"],W,"H","Zhou Yu on a wooden command tower dispatching orders with a firm outstretched arm while three officers kneel below to receive them, Zhou Yu in teal, officers clearly different faces"),
(28,["zgl","sb"],W,"H","Zhuge Liang standing alone on a tall earthen altar with both arms raised and his robe whipped by wind, a few officers looking up at him from below in awe, a river and a storm sky behind"),
(29,["zy","cp"],W,"H","Zhou Yu and Cheng Pu standing side by side on a riverside mound looking across a wide river, Zhou Yu young and slim, Cheng Pu old with a grey beard, on the far bank the small camp of Cao Ren, clearly different faces"),
(30,["zy"],C,"H","exactly ONE man: Zhou Yu standing on a riverside mound with a tightening pained face and one hand pressed against his right side, a single arrow lying on the ground at his feet, no blood, no second figure"),
(31,["zy"],C,"H","exactly ONE man: Zhou Yu lying on a low plank bed under a blanket in a tent, face pale and eyes open, through the tent opening distant enemy banners gather on the far bank, no second figure"),
(32,["zy","sb"],W,"H","morning in a camp: Zhou Yu pushing himself up and walking between two lines of tents, one hand held against his side, soldiers on both sides standing straight and looking at him with surprise and admiration, each soldier different"),
(33,["cr"],C,"H","exactly ONE general on a horse: Cao Ren on the far river bank turning his horse away and raising a hand to signal retreat, his column of tiny soldiers turning back behind him, no second close figure"),
(34,["zy","sb"],F,"H","evening torch light: Zhou Yu walking slowly through the camp past rows of soldiers who bow their heads to him, his hand pressed lightly to his side, determined face, soldiers with different faces"),
(35,["zy"],C,"H","exactly ONE man: Zhou Yu standing at a window opening with no glass thoughtfully looking out toward a distant camp of a different banner colour across the river, no second figure"),
(36,["lb","dan"],W,"H","Liu Bei seated uneasily in a lavish palace hall, two court dancers with long sleeves dancing before him and open chests brimming with jade and gold beside him, he looks uncomfortable, three different faces"),
(37,["gy","zf","lb"],C,"H","Guan Yu and Zhang Fei standing outside a tall closed ornate gate looking anxiously toward it, while through the gate gap in the courtyard Liu Bei sits alone among silks, three clearly different faces"),
(38,["sq","zy"],C,"H","Sun Quan seated on a mat shaking his head and waving a sleeve to refuse, Zhou Yu bowing before him with a disappointed face, two clearly different faces and robe colours"),
(39,["zy"],C,"H","exactly ONE man: Zhou Yu at a table with three small groups of coloured markers on a map, frowning at them deep in thought, no second figure"),
(40,["zgl","sq","zy"],W,"H","Zhuge Liang speaking earnestly before Sun Quan seated on a mat in a hall, Zhou Yu standing aside with arms folded in his sleeves watching, three clearly different faces and robe colours"),
(41,["zy","zgl"],W,"H","Zhou Yu and Zhuge Liang sitting calmly on opposite mats with a teapot-less clay water jar between them, nodding to each other courteously, peaceful warm light, clearly different faces"),
(42,["zy","sq"],W,"H","Zhou Yu pointing at a sand-table model of western mountains and rivers in a hall, Sun Quan listening with interest, two clearly different faces"),
(43,["zy","sb"],W,"H","an army column marching west through a high mountain pass, two leaders on horses at the front looking ahead, plain blank banners, steep cliffs, wide view, soldiers small"),
(44,["zy"],W,"H","exactly ONE man seen from behind: Zhou Yu standing on a hill at sunrise looking west over a vast landscape of mountains and rivers, the Wu camp spread below him, no second figure"),
(45,["zy","sb"],W,"H","Zhou Yu at the gate of Jiangling city giving orders while officers load wagons and soldiers line up, morning light, Zhou Yu in teal, officers with different faces"),
(46,["zy","sb"],C,"H","a covered river boat with its curtains drawn gliding on a misty river at dusk, an officer standing at the stern with bowed head, soldiers marching along the bank, quiet sad mood"),
(47,["zy"],C,"H","Zhou Yu lying pale in a sickbed in a simple room, an old physician in a plain robe kneeling beside him and gently shaking his head, a steaming herbal bowl on a low table, two different faces"),
(48,["ps"],C,"H","exactly ONE elderly annotator sitting at a low table writing tiny notes beside a bundle of bamboo slips with a small map of river towns next to him, stroking his beard, no second figure"),
(49,["zy"],C,"H","exactly ONE man: Zhou Yu propped up in bed by a pillow roll, pale but resolute, writing carefully with a brush by the light of a Han bronze oil dish, no second figure"),
(50,["zy","sb"],C,"H","Zhou Yu handing a sealed letter to a kneeling messenger in a dim bedroom, pale face but firm eyes, messenger young and serious, two clearly different faces"),
(51,["sq","sb"],C,"H","Sun Quan in white mourning robes kneeling before a funeral hall hung with white cloth, tears on his face, two officers behind him moved and lowering their heads, three different faces"),
(52,["sq"],C,"H","exactly ONE man: Sun Quan in white mourning robes standing beside a plain wooden coffin draped in white cloth, looking up at the sky with tears on his face and one sleeve raised, no second figure"),
(53,["sq","sb"],W,"H","Sun Quan seated on a high dais speaking gravely, two rows of officers kneeling in the hall below, solemn and respectful mood, clearly different faces"),
(54,["cs"],C,"H","exactly ONE scholar-historian writing steadily with a brush at a low table, two plain blank wooden memorial plaques standing upright on the table in front of him, no second figure"),
(55,["zy","dan"],W,"H","a portrait painter at an easel brushing a dignified full-length portrait on a silk panel of Zhou Yu standing resolute in teal, the painter looking up thoughtfully, warm studio light, two clearly different faces"),
(56,["kc","dan"],W,"S","a storyteller in a Song market street acting out a man clutching his chest and falling backward, a crowd of townspeople gasping and covering their mouths, shopfronts behind"),
(57,["zgl","sb"],W,"H","Zhuge Liang standing on a high rock in bright sunlight with a warm halo behind him, officers below looking up at him in awe, plain green blank banners, clear sky"),
(58,["zy","sb"],W,"H","Zhou Yu on a warship deck acclaimed by cheering soldiers raising their arms after a victory, the smoking wreck of an enemy fleet far behind, bright morning light, soldiers with different faces"),
(59,["zy","zgl","sb"],W,"H","Zhou Yu in the foreground with folded arms and a sour jealous face looking aside, while far behind him a crowd of soldiers cheers around a tiny white-robed Zhuge Liang"),
(60,["kc","dan"],W,"S","a shadow-play screen lit from behind in a Song street, a tall white-robed silhouette held high in the light and a smaller teal silhouette bowing low beneath it, an audience seen from behind watching"),
(61,["zy","dan"],C,"H","Zhou Yu walking stiffly along a street while a group of townsfolk with sneering faces point and whisper behind their sleeves, Zhou Yu with a tight embarrassed face, townsfolk with different faces"),
(62,["zy","zgl"],W,"S","an open-air Song opera stage with a red curtain: an actor in a teal robe collapsing dramatically to the stage floor while an actor in a white-and-blue robe stands calmly with arms hidden in sleeves, an audience seen from behind"),
(63,["kc","dan"],W,"S","a storyteller at a table with three small wooden blocks laid in a row in front of him, leaning toward a captivated crowd with a wide grin, townspeople leaning in, warm glow"),
(64,[],F,"H","a wide river at dusk: in the left foreground a single arrow standing upright in the earth, in the middle the river with a burning fleet far away, on the right bank a small plain sickbed with a blanket, one continuous picture, completely empty, absolutely no people"),
(65,["ps"],C,"H","exactly ONE scholar placing a tied bundle of bamboo slips on the lowest of three plain shelves, the upper two shelves holding differently wrapped bundles, calm face, no second figure"),
(66,["zy"],F,"H","exactly ONE man: Zhou Yu standing at a ship stern at dusk with one hand lightly pressed to his right side, a burning fleet far behind him, calm resolute face, no second figure"),
(67,["ls","sq"],C,"H","Lu Su bowing before Sun Quan who wipes a tear with his sleeve, Lu Su stout in grey-green and Sun Quan in dark purple, a solemn hall, two clearly different faces"),
(68,["ps"],C,"H","exactly ONE elderly annotator writing at a table beside a small sand-table model of a river fleet whose tiny flags all lean in one direction as if blown by wind, no second figure"),
(69,["zy","zgl"],C,"H","Zhou Yu in the large foreground, red-faced with clenched fists and a furious expression, while far behind him Zhuge Liang stands small and calm with a gentle smile, sleeves hiding his hands"),
(70,["ps"],C,"H","exactly ONE scholar sitting at a table with two opened bundles of bamboo slips beside him and a third sealed bundle still tied in front of him, looking at the sealed bundle thoughtfully, no second figure"),
(71,["zy"],C,"H","exactly ONE man: Zhou Yu lying peacefully in bed with closed eyes and a serene pale face, soft morning light through a lattice window, no second figure"),
(72,[],C,"H","a bronze balance scale on a plain table: the left pan sagging low under several tied bundles of bamboo slips, the right pan high holding only a small wooden storyteller's block, soft window light, completely empty, absolutely no people"),
(73,["zy"],W,"H","exactly ONE man: Zhou Yu standing calmly in the centre, on the left behind him a grand courtyard house, on the right behind him a river with a burning fleet far away, golden light, no second figure"),
(74,[],C,"H","a riderless horse with an empty saddle standing at the edge of a misty river at dawn facing distant western mountains, a few tiny officers far behind with bowed heads, quiet sad mood, wide view"),
(75,["dan"],C,"S","exactly ONE townsman standing in a Song street at dusk with a hand on his chin looking thoughtful, in the sky behind him a faint warm image of a burning fleet on the left and a faint dark image of a man falling on the right, no second figure"),
(76,["dan"],W,"S","exactly ONE man seen from behind standing at a fork in a road, the left road leading to a grand stone hall of records and the right road leading to a lively market with a storyteller's platform, evening light, no second figure"),
]
FIX={
6:"The storyteller's hands are open and empty, standing on a plain low wooden platform.",
13:"Guests kneel on low reed mats at low bare-topped wooden tables; the musician kneels on a mat playing a round-bodied bronze-string pipa held upright.",
17:"All banners are plain cloth in a single flat colour.",
33:"Full-bleed picture filling the whole frame; the horse stands calmly beside him with four correct legs.",
35:"The window is an open wooden-lattice opening onto the river; the distant flag is plain flat-coloured cloth.",
36:"Liu Bei kneels on a low reed mat on the floor, the open chests of jade and gold beside him.",
39:"On the plain silk map lie small wooden pegs and tiny cloth markers; the map shows only simple lines, rivers and mountains.",
45:"Full-bleed picture filling the frame; the city gate is a plain open archway in a bare wall.",
54:"Chen Shou kneels on a low reed mat at a low wooden table writing with a brush on a bamboo-slip scroll; two plain wooden plaques stand upright on the table.",
55:"A portrait painter paints on a large silk panel hung on a wooden frame, the painted portrait of a standing man in teal visible on it; the onlookers are different people.",
58:"All flags are plain flat-coloured cloth.",
62:"The audience seen from behind wears simple tunics in blue, ochre and green with cloth caps or topknots.",
63:"The old storyteller has a topknot under a soft cloth cap, grey beard; the three blocks are small plain wooden cubes.",
70:"He kneels on a low reed mat at a low wooden table; the scrolls are rolled bamboo-slip bundles tied with cord; the wall behind is plain bare brick.",
76:"All shop signs are plain blank wooden boards.",
}
GEN=" Full-bleed single picture filling the whole frame."

# --- Sửa lỗi lần vẽ 03/11 (chữ, tàu kiểu Tây, giá vẽ, màn nhung, màn chiếu): đổi cảnh và ghi chú, tả điều cần có ---
SHIP="All ships are boxy flat-hulled Han river warships with raised wooden deck-towers, rows of oars and plain flat-coloured square mat sails on a single mast."
SQUARE="Plain tiled-roof houses with bare wooden walls and bare eaves stand behind; every wall is plain and bare."
REDO={
6:("an old storyteller standing on a low plain wooden platform in an open Song market square telling a tale with an open hand, a crowd of townspeople nodding and smiling in satisfaction, plain tiled-roof houses and trees behind, a gentle bright afternoon",SQUARE+" The storyteller's hands are open and empty."),
7:("exactly ONE scholar sitting at a plain low table with a hand on his chin and a doubtful raised eyebrow, a plain clay teacup in front of him and a plain empty bed behind him, no second figure",""),
8:("three wooden boxes of different sizes on a plain wooden table: one small and plain, one tall with a simple brass clasp, one wrapped in coloured silk cloth, soft light through a lattice window, completely empty, absolutely no people",""),
12:("young Zhou Yu walking out of the big mansion gate carrying a small cloth bundle with a light easy smile, while behind him in the courtyard Sun Ce stands cheerfully with a rolled sleeping mat under his arm, two different faces and robes","The wall beside the gate is plain bare grey brick."),
21:("a broad river: on the far right a huge enemy fleet of boxy Han war-barges filling the whole horizon, on the left a small fleet of only a few similar barges, Zhou Yu tiny on the nearest deck looking calm, wide view",SHIP),
22:("exactly ONE old general: Huang Gai standing on the deck of a boxy wooden Han warship at dusk pointing toward the enemy fleet across the river with a sly sudden idea in his eyes, no second close figure, ships far away",SHIP),
39:("exactly ONE man: Zhou Yu at a low table on which lies a plain sand-table model of rivers and hills with three small groups of coloured wooden pegs, frowning at them deep in thought, no second figure",""),
54:("exactly ONE scholar-historian kneeling on a low reed mat at a low plain wooden table with his brush lifted, gazing thoughtfully out of a lattice window, a plain closed wooden box on the table, no second figure","He kneels on the floor mat with his legs folded under him; the wall behind is plain bare brick."),
55:("a wall painter on a low wooden scaffold brushing a large flat painted mural portrait of a standing man in a teal robe onto a plain plaster wall, the mural is a flat painting on the wall, the painter looking back thoughtfully, warm bright light, onlookers watching from below","Onlookers in different robes stand below the scaffold."),
56:("a storyteller on a low plain wooden platform in an open Song market square acting out a man clutching his chest and falling backward, a crowd of townspeople gasping and covering their mouths, plain tiled-roof houses and trees behind",SQUARE),
60:("a storyteller on a low platform holding up two small wooden puppets, a tall white-robed puppet raised high in the light and a smaller teal puppet bowing low beneath it, townspeople watching with interest","The audience seen from behind wears simple tunics in blue, ochre and green with cloth caps or topknots. "+SQUARE),
62:("an open-air Song market square with a low wooden platform: a performer in a teal robe collapsing dramatically to the platform floor while a performer in a white-and-blue robe stands calmly with arms hidden in sleeves, an audience seen from behind","The audience seen from behind wears simple tunics in blue, ochre and green with cloth caps or topknots. "+SQUARE),
64:("a wide river at dusk: in the left foreground a single plain arrow with a bare wooden shaft standing upright in the earth, in the middle the river with a burning fleet of boxy Han warships far away, on the right bank a low plain wooden bed with a plain blanket, one continuous picture, completely empty, absolutely no people",SHIP),
66:(None,SHIP),
68:("exactly ONE elderly annotator kneeling on a reed mat at a low table with a brush in his hand, beside a small sand-table model of a river with tiny plain single-colour cloth flags all leaning in one direction as if blown by wind, no second figure","The tiny flags are plain flat red, yellow and green cloth triangles without any marks."),
70:("exactly ONE scholar sitting at a low table with two opened lacquered boxes beside him and a third box still closed and tied with cord in front of him, looking at the closed box thoughtfully, no second figure","He kneels on a low reed mat; the wall behind is plain bare brick."),
73:(None,SHIP+" Each ship has exactly one mast."),
75:("exactly ONE townsman standing in a Song street at dusk with a hand on his chin looking thoughtful, behind him on the left a faint warm glow of burning boats on the river and on the right a quiet empty street, no second figure",SHIP),
}

# --- Sửa lỗi 03/11 lần 3: tóc búi trên đỉnh đầu, đúng hai tay, không dính thân, bỏ giường ngoài bờ sông ---
TOP="Every man and boy has black hair gathered up into a neat topknot on the crown of his head, under a small cap or headcloth, and every person has exactly two arms and two hands, each clearly drawn and separate from the others. "
def _fx(n,extra=""):
    old=REDO[n][1] if n in REDO else ""
    return (None if n not in REDO else REDO[n][0], TOP+extra+" "+old)
REDO[43]=(None,TOP+"Soldiers wear small flat caps over their topknots; the two leaders ride separate horses with a clear gap between them.")
REDO[46]=(None,TOP+"The officer at the stern stands alone with his arms by his sides; the soldiers walk in a loose line, each a separate person.")
REDO[48]=(None,TOP+"One hand holds the brush and the other rests flat on the table.")
REDO[55]=(REDO[55][0],TOP+"The painter's right hand holds the brush against the wall and his left hand grips the scaffold rail; the onlookers are separate people with a little space between them. "+REDO[55][1])
REDO[56]=(REDO[56][0],TOP+"Exactly one man falls backward onto the platform, drawn as one body with two arms and two legs, and the storyteller stands a clear step apart from him; each bystander holds both hands to the mouth. "+REDO[56][1])
REDO[60]=(REDO[60][0],TOP+"Every audience member seen from behind has a topknot on the crown of the head; the storyteller holds one puppet in each hand. "+REDO[60][1])
REDO[61]=("Zhou Yu standing in a street with a tight embarrassed face while exactly five townsfolk stand in a loose arc behind him, three whispering behind raised long sleeves and two shaking their heads, every townsperson with a different face and clothes",TOP+"Townsfolk keep their hands hidden in long sleeves or folded in front of the chest.")
REDO[64]=("a wide river at dusk: in the left foreground a single plain arrow with a bare wooden shaft standing upright in the earth, in the middle the river with a burning fleet of boxy Han warships far away, on the right bank a small military tent of plain cloth with its flap tied open and a warm oil lamp glowing inside, one continuous picture, completely empty, absolutely no people",SHIP)
REDO[71]=("a quiet room seen from the foot of a low plank bed: exactly one man, Zhou Yu, lies on his back with his head on a single pillow and a blanket drawn up to his chest, eyes closed, serene pale face, the rest of the room empty with one bronze oil dish on a low table, soft morning light through a lattice window",TOP+"The bed holds exactly one body with one head and two arms resting on the blanket; nobody else is in the room.")
REDO[75]=(REDO[75][0],TOP+"The townsman has a topknot under a small cap and one hand on his chin, the other hanging by his side. "+REDO[75][1])

S=[(n,nv,ton,era,(REDO[n][0] or desc) if n in REDO else desc) for n,nv,ton,era,desc in S]
for n,(dd,fx) in REDO.items(): FIX[n]=fx
beats={}
for l in open("ke-hoach/chu-du-co-bi-choc-tuc-chet-kich-ban.md",encoding="utf-8"):
    m=re.match(r"(\d+)\. \[[^\]]*\] (.*)",l.strip())
    if m: beats[int(m.group(1))]=m.group(2)
anh=[];canh=[]
for n,nv,ton,era,desc in S:
    ch="; ".join(NV[k] for k in nv)
    p=(desc+(". "+ch if ch else "")+"."+ton+(HAN if era=="H" else SONG)+" "+FIX.get(n,"")+GEN)
    k=f"{n:03d}"
    anh.append({"key":k,"cau":n,"nv":nv,"text":beats.get(n,""),"prompt":p})
    canh.append({"key":k,"nv":nv,"mo_ta":desc})
assert [a["cau"] for a in anh]==list(range(1,77)) and len(beats)==76
json.dump({"ma":"CD","ghi_chu":"Video dài Chu Du có thật sự bị Gia Cát Lượng chọc tức đến chết","nhan_vat":NV,"canh":canh},open("ke-hoach/nhan-vat/CD.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
json.dump(anh,open("ke-hoach/nhan-vat/CD_anh.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print(len(anh),max(len(a["prompt"]) for a in anh),sum(1 for a in anh if len(a["prompt"])>1900))
