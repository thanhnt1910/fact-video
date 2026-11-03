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
REDO[55]=("a wall painter on a low wooden scaffold finishing a large painted mural of a standing man in a teal robe with a black cap and a dark leather chest guard, the painted standing man fills the middle of the plaster wall in bright colours, the painter beside the mural looking back thoughtfully, warm bright light, onlookers watching from below",TOP+"The painter's right hand holds the brush against the wall and his left hand grips the scaffold rail; the onlookers are separate people with a little space between them. "+REDO[55][1])
REDO[56]=(REDO[56][0],TOP+"Exactly one man falls backward onto the platform, drawn as one body with two arms and two legs, and the storyteller stands a clear step apart from him; each bystander holds both hands to the mouth. "+REDO[56][1])
REDO[60]=(REDO[60][0],TOP+"Every audience member seen from behind has a topknot on the crown of the head; the storyteller holds one puppet in each hand. "+REDO[60][1])
REDO[61]=("Zhou Yu standing in a street with a tight embarrassed face while exactly five townsfolk stand in a loose arc behind him, three whispering behind raised long sleeves and two shaking their heads, every townsperson with a different face and clothes",TOP+"Townsfolk keep their hands hidden in long sleeves or folded in front of the chest.")
REDO[64]=("an empty quiet riverbank at dusk shown as four things in a row from left to right: a single plain arrow with a bare wooden shaft standing upright in the earth, a small clay bowl of steaming herbal medicine on a low plain wooden stool, a wide river, and far away on the river a burning fleet of boxy Han warships glowing orange, one continuous picture of an uninhabited landscape",SHIP)
REDO[71]=("a quiet room seen from the foot of a low plank bed: exactly one man, Zhou Yu, lies on his back with his head on a single pillow and a blanket drawn up to his chest, eyes closed, serene pale face, the rest of the room empty with one bronze oil dish on a low table, soft morning light through a lattice window",TOP+"The bed holds exactly one body with one head and two arms resting on the blanket; nobody else is in the room.")
REDO[75]=("exactly ONE townsman standing at a fork of a dirt road at dusk with one hand on his chin looking thoughtful, the left road leads to a wide river where a fleet of boxy Han warships burns in bright orange glow, the right road leads to an open square with a small wooden puppet stage and a plain lit screen, no second figure",TOP+"The townsman has a topknot under a small cap, one hand on his chin and the other hanging by his side. "+SHIP)


# --- Sửa lỗi 03/11 lần 4: soi 24 khung Veo, vẽ lại ảnh có tay thừa, người đứng dưới nước, tóc xõa, vật lơ lửng ---
REDO[5]=("Zhou Yu staggering backward clutching his chest with a pained face while exactly two officers rush in, one officer holding him under his left arm and the other under his right arm, a calm riverside camp at dusk behind them",TOP+"Zhou Yu's hair is gathered in a neat topknot under a cap with nothing hanging down; each of the three men has exactly two arms.")
REDO[11]=(None,TOP+"The courtyard gate is made of plain wooden planks without handles or metal fittings, the house behind has a low straight-ridged grey tiled roof without curved corners, Han mud-brick walls.")
REDO[16]=("Cao Cao standing on a tall earthen platform on dry land with one arm raised proclaiming to an enormous army of tiny soldiers standing in dense ranks on the dry riverbank, the river far in the background, plain blank banners, wind in his sleeves",TOP+"All soldiers stand on dry ground. The platform holds only Cao Cao and one guard.")
REDO[23]=("a row of small fast boats tied at a quay at dusk, sailors piling dry brushwood and straw onto them and pouring oil from clay jars, calm blue dusk sky, the boats unlit and the quay quiet",TOP+"Each sailor has exactly two arms and two hands.")
REDO[24]=(None,TOP+"Zhou Yu's cap is tied firmly with no ribbon or hair flying; the boats' sailors are small.")
REDO[25]=("the whole enemy fleet of boxy Han warships burning on a calm river at night, towering flames and black smoke filling the sky, the water mirroring the orange fire, the river empty apart from the burning boats, two officers stand on the dry bank at the far left watching",TOP+SHIP)
REDO[33]=("exactly ONE general on a horse: Cao Ren on the far river bank turning his horse away and raising one open hand, a plain blank cloth banner hanging from a tall pole planted firmly in the ground beside him, a few soldiers marching away behind, no second figure in front",TOP)
REDO[45]=("Zhou Yu at the gate of Jiangling city giving orders with one raised hand while two soldiers load a wooden cart beside the gate and a line of soldiers lines up behind them, bright morning light",TOP)
REDO[58]=(None,TOP+"Every soldier has hair in a topknot under a cap, nothing hanging down the neck.")

S=[(n,nv,ton,era,(REDO[n][0] or desc) if n in REDO else desc) for n,nv,ton,era,desc in S]
for n,(dd,fx) in REDO.items(): FIX[n]=fx

# ===== CD2: vẽ lại toàn bộ trên Kaggle, độ phân giải cao, giảm ảnh một người, tập trung ảnh minh họa đúng cốt truyện =====
NEW={
1:(["zy","sb"],W,"H","a brilliant victory at sunrise on a broad river: sailors on the deck of a boxy Han flagship cheering with raised arms, the burnt wreck of an enemy fleet drifting behind, and at the centre a general in teal standing proudly among his men, golden light on the water","exactly the same teal-robed general stands at the centre; every sailor is a different face. "+SHIP),
3:(["zy","zgl"],C,"H","in the foreground Zhou Yu seated on a mat at a low table with a tight jaw and narrowed jealous eyes, and behind him through the open tent flap Zhuge Liang in white calmly speaking to a group of listening officers who nod with respect","Two clearly different faces in the foreground and background."),
4:(["zy","zgl"],C,"H","two men playing a board game of go at a low table in a tent: Zhuge Liang in white has already placed his stone on the round wooden board with a calm smile, while Zhou Yu in teal frowns with a stone in his fingers, rows of black and white stones on the board","The board has plain lines and round black and white stones only."),
7:(["ps"],C,"H","a young scholar pushing open a heavy wooden door into a high archive room whose walls are filled with shelves of tied bamboo-slip bundles, bright light streaming across the floor, an old keeper beside him holding an oil dish","Each of the two men has exactly two arms and two hands."),
8:(["kc","dan"],W,"H","a three-storey Han tower seen from outside in bright daylight: the ground floor is a sturdy stone archive with a keeper standing beside neatly tied bundles, the middle floor is an open wooden hall where three scholars crowd over a table adding small bundles to larger ones, the top floor is an open painted stage with colourful cloth streamers where a storyteller spreads his arms before a cheering crowd","Each floor is clearly different in material and mood; every person has a topknot and exactly two arms; no writing anywhere."),
17:(["zy","sb"],C,"H","Zhou Yu and two officers around a sand-table of a river valley counting with small clay markers: a small group of tired grey markers on the north bank and a larger group of green markers apart on the east side, the three men leaning over the table with focused faces","Each man has exactly two arms; markers are plain round clay discs."),
21:(["zy"],C,"H","a broad river seen from a high bank: on the right a vast crowded enemy fleet of boxy Han war-barges covering the whole water to the horizon, on the left a small compact fleet of only a few similar warships with tiny sailors on the decks, a calm general in teal on the nearest deck","The two fleets are clearly very different in size."),
22:(["hg","zy"],C,"H","on the deck of a boxy Han warship at dusk the old general Huang Gai points across the water to the enemy fleet whose ships lie tied close together in long rows, and Zhou Yu in teal beside him listens with a thoughtful nod","Each man has exactly two arms; the enemy ships are boxy Han war-barges tied side by side in rows."),
30:(["zy","sb"],C,"H","on a riverside mound Zhou Yu clutching his right side with a pained face, a single arrow lying on the ground at his feet, two officers hurrying to him from both sides to hold his arms, the wide river behind","Exactly three men in the picture, each with two arms."),
31:(["cr","sb"],C,"H","Cao Ren on a horse before a line of assembled cavalry on a riverbank, pointing across the wide river at the far bank where a few enemy tents stand quietly in the morning light, the riders with different faces and plain blank banners","The cavalry riders each have topknots under caps."),
32:(["zy","sb"],C,"H","in a tent Zhou Yu pushing himself up from a low plank bed with one hand pressed to his side, an officer and a physician in plain robes supporting him on both sides, morning light through the open tent flap showing soldiers waiting outside","Exactly three men, each with two arms."),
35:(["zy","lb","gy"],W,"H","Zhou Yu and Liu Bei sitting at a low table on a riverside terrace at sunset sharing wine cups with polite smiles, Guan Yu with his long black beard standing watchfully behind Liu Bei and an officer in teal standing behind Zhou Yu","Four men, each with a different face, each with two arms."),
39:(["zy","ls"],C,"H","Zhou Yu and Lu Su bending over a sand-table model of a river city, on the model three small clay figures stand close together in a cluster and Zhou Yu's finger rests on the space between them and the city, thoughtful faces","The three clay figures are plain, tiny and faceless."),
44:(["zy","sb"],W,"H","Zhou Yu and a younger officer on horseback on a ridge at sunrise looking west toward a far line of high mountains, a long army column resting on the slope below them, golden light","Two riders on separate horses with a clear gap between them."),
48:(["ps","dan"],C,"H","an elderly annotator and two assistants at a wide low table comparing two small maps of river towns, the old man pointing at one town on the first map while an assistant holds the second map, bright window light","Each of the three men has exactly two arms; maps show plain lines and dots only."),
52:(["sq","sb"],C,"H","Sun Quan in white mourning robes standing beside a plain wooden coffin draped in white cloth with his hand resting on it and tears on his face, a row of officers in white bowing behind him in a bright hall","Every man has a topknot; each man has two arms."),
54:(["cs","dan"],C,"H","Chen Shou the historian kneeling at a low table writing with a brush while two assistants kneel at his sides holding tied bamboo-slip bundles, a soft window light","Each of the three men has exactly two arms."),
66:(["zy","sb"],C,"H","at the stern of a warship at dusk Zhou Yu stands with one hand pressed lightly to his right side while soldiers around him look at him with respect, the burning remains of an enemy fleet glowing far behind on the water","Zhou Yu stands among a few soldiers; everyone stands on the deck."),
68:(["ps","dan"],C,"H","an old annotator kneeling at a low table pointing at a small flag on a river map, an assistant beside him holding a tied bundle, a small windsock of plain cloth on a pole in the courtyard showing a strong wind from the east","The windsock is a plain cloth strip."),
71:(["zy","dan"],C,"H","a quiet room seen from the foot of a low plank bed: Zhou Yu lies on his back with his head on a single pillow and a blanket to his chest, eyes closed, a physician in a plain robe sitting beside the bed holding his wrist and an attendant standing at the door","The bed holds exactly one body with one head."),
76:(["dan"],C,"H","a street wall hung with three large painted cloth portraits of different men in Han robes, a woman and a boy standing before them looking up thoughtfully, bright afternoon light","The portraits are flat paintings on cloth without any writing."),
}
for _n,(_nv,_ton,_era,_desc,_fx) in NEW.items():
    S=[(_n,_nv,_ton,_era,_desc) if x[0]==_n else x for x in S]
    FIX[_n]=TOP+_fx

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

# --- Ảnh phần hai của câu dài (quy tắc: clip Veo 8 giây, câu dài hơn thì vẽ thêm ảnh; mã 100 + số câu) ---
EXTRA={
101:("H",C,"a single shallow bronze oil dish on a low plain wooden table at dusk, its tiny flame bending low and small, through a lattice window behind it the glow of a burning fleet on the river fading to dark, completely empty, absolutely no people",""),
116:("H",C,"a wide view from a hill over a vast riverside camp: countless small tents in endless rows and a packed crowd of small boats along the bank reaching the horizon, plain blank banners, tiny soldiers, cold winter light",SHIP),
121:("H",C,"a sand-table model of a river on a plain wooden table seen from above: on the right a huge field of tiny red clay markers, on the left a small group of tiny blue clay markers, a calm hand placing one blue marker, soft window light, only the hand visible",""),
124:("H",F,"the first fire boats crashing into the enemy fleet of boxy Han warships at night, bright flames leaping from ship to ship, strong wind bending the flames, black smoke, small figures on the decks, wide view",SHIP),
127:("H",C,"in the foreground a plain empty reed mat with a neatly folded white scarf on it, behind it a bare wooden command tower made of plain timber posts with no signboard where Zhou Yu in teal gives orders and officers listen with different faces, bright daylight, the mat in the foreground is clearly empty",TOP),
143:("H",W,"a plain wooden table with a sand-table model of western mountains and rivers: a pointer rests on a path that winds through a narrow gorge, one small clay city marker is left behind at the river and a second marker waits far to the west, bright warm light, completely empty, absolutely no people",""),
158:("H",W,"two men standing side by side on a bright street: a tall man in a white robe with a blue border on a high wooden step beside a shorter teal-robed general on the lower level, townsmen with different faces look up at the white-robed man with admiration",TOP+"Every man has black hair gathered into a neat topknot on the crown of his head with nothing hanging down his neck or back. "),
162:("H",C,"a plain wooden table in bright light with three small wooden blocks standing in a row, the first two upright and the third knocked over on its side, completely empty, absolutely no people",""),
174:("H",C,"a sand-table model of western mountains and rivers on a plain wooden table, a path marked with small flags only up to the middle and the remaining flags still lying in a wooden tray beside it, soft dawn light through a lattice window, completely empty, absolutely no people",""),
}
for k,(era,ton,desc,fx) in EXTRA.items():
    anh.append({"key":str(k),"cau":k-100,"nv":[],"text":beats.get(k-100,""),"prompt":desc+"."+ton+(HAN if era=="H" else SONG)+" "+fx+GEN})
    canh.append({"key":str(k),"nv":[],"mo_ta":desc})

assert [a["cau"] for a in anh][:76]==list(range(1,77)) and len(beats)==76
json.dump({"ma":"CD2","ghi_chu":"Video dài Chu Du có thật sự bị Gia Cát Lượng chọc tức đến chết","nhan_vat":NV,"canh":canh},open("ke-hoach/nhan-vat/CD2.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
for _a in anh: _a["w"]=1920; _a["h"]=1088
json.dump(anh,open("ke-hoach/nhan-vat/CD2_anh.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print(len(anh),max(len(a["prompt"]) for a in anh),sum(1 for a in anh if len(a["prompt"])>1900))
