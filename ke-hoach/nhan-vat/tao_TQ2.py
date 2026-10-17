"""Tạo TQ2.json (cảnh), TQ2_anh.json (prompt vẽ) và scripts/TQ2.json (video dài + ngắn) cho tập 2.
Mỗi ảnh chỉ dùng một lần trong video dài (khóa ảnh = số thứ tự cảnh, 001...)."""
import json, re
from pathlib import Path
R = Path(__file__).resolve().parent
ROOT = R.parents[1]
tq = json.loads((R / "TQ.json").read_text(encoding="utf-8"))
t1 = json.loads((R / "TQ1.json").read_text(encoding="utf-8"))

PHU = {k: t1["nhan_vat_phu"][k] for k in ("docbuu", "hoanquan", "tuongquan", "dan", "linhde")}
PHU.update({
 "congtonton": "Gongsun Zan, a lean tall commander of about 35, sharp handsome face, thin moustache, strong clear gaze, dark-blue cross-collared robe under light iron scale armour",
 "hatien": "He Jin, a heavy-set man of about 50 with a broad red face and a short beard, dark-red official robe and a black official cap, confident arrogant bearing",
 "vienthieu": "Yuan Shao, a handsome tall man of about 35 with a neat short beard, proud composed look, deep-blue official robe over light armour",
 "dongtrac": "Dong Zhuo, a huge heavy fat man of about 55 with a thick neck, a heavy cruel face with a short thick beard, narrow suspicious eyes, dark fur-trimmed robe over an iron breastplate",
 "thieude": "Emperor Shao of Han, a thin pale frightened boy of about fourteen in rumpled dark-red robes and a small crooked crown",
 "hiende": "Liu Xie, a small serious boy of about nine in a plain dark robe, hair in two small tufts",
 "luubinh": "Liu Ping, a thin sour-faced official of about 40 with a pointed beard, plum-coloured robe and a black cap, contemptuous expression",
 "thichkhach": "an assassin, a lean man of about 30 in plain dark clothes, a cloth tied across his lower face, hands empty",
 "taotao": "Cao Cao, a short wiry man of about 35 with sharp clever eyes, a thin moustache and a small beard, dark-blue robe with plain light armour",
 "tonkien": "Sun Jian, a strong broad-faced man of about 45 with a short beard, a red cloth headband, red robe and iron armour",
})
PHU.update({
 "linhhan": "a Han foot soldier, adult man with a weathered face, plain dark iron helmet, grey-brown leather and iron-scale armour over a plain red tunic, long wooden-shafted spear",
 "giacuop": "a bandit rebel, lean adult man with a plain brown cloth tied around his head, ragged brown hemp tunic, wooden-shafted spear",
 "linhbien": "a frontier soldier from the north-west, broad adult man with a thick beard, round fur cap, dark fur-trimmed iron-scale armour, long spear",
 "linhtonkien": "a soldier of Sun Jian, adult man with a red cloth headband, plain red tunic, light iron armour, long spear",
 "huahung": "Hua Xiong, a huge burly general of about 40 with a fierce square face and a black beard, black iron armour with a dark-green cloak and a heavy iron helmet",
 "dancu": "a poor refugee villager, adult man with a cloth bundle on his back, ragged hemp clothes, tired face",
 "thieude_lung": "a thin pale teenage boy of about fourteen in rumpled dark-red robes, hair in a topknot under a small flat cap, clearly a boy",
 "quanlai": "a county clerk, thin adult man in a plain grey robe and a small black cloth cap, bowing respectfully",
})
NV = {**tq["nhan_vat"], **PHU}

E = "no people, the scene is completely empty of people"
# (key, nv, so_nguoi, mo_ta)
S = [
("001",[],0,"an empty guest-house room with an overturned wooden stool and a loose coil of rope on the floor, dim lamp light"),
("002",["liubei"],1,"waist-up of Liu Bei standing in a stone courtyard at night with a coil of rope in one hand, tense face, exactly one man, his far arm hidden behind his body"),
("003",["liubei"],1,"Liu Bei seen from behind walking out through a county gate at night carrying a small cloth bundle, exactly one man, both arms hidden"),
("004",[],0,"a quiet dirt road disappearing into low misty hills at first light, a few bare trees"),
("005",[],0,"the tiled roofs of a great palace seen far away above morning mist, towers and walls, a dim red sun"),
("006",[],0,"a bundle of bamboo-slip books and a brush on a wooden desk beside a clay oil lamp, warm night light"),
("007",[],0,"a plain wooden official carriage standing in front of the gate of a small county government office with a grey tiled roof, no horses"),
("008",["docbuu"],1,"waist-up of a provincial inspector seated at a desk writing on a bamboo slip with his one hand, arrogant face, exactly one man, the other hand hidden under the desk"),
("009",[],0,"a stack of bamboo-slip documents tied with cord and one rolled official order on a dark wooden table, candlelight"),
("010",[],0,"a closed wooden door of a roadside guest house at dusk with a pair of straw sandals before the step"),
("011",["liubei"],1,"waist-up of Liu Bei pushing a wooden door open with one hand, fierce determined face, exactly one man, his other arm hidden behind the door"),
("012",[],0,"a plain stone boundary marker standing beside a dirt road at dawn, grass and mist"),
("013",[],0,"a long wooden cane lying across a stone threshold in torchlight at night, a coil of rope beside it"),
("014",["liubei"],1,"a distant small man seen from behind hurrying along a moonlit road, a tiny figure in a wide dark landscape, exactly one man, arms hidden"),
("015",[],0,"a small bronze official seal with a cord ribbon lying on a stone step, morning light"),
("016",[],0,"a crossroads in a wide autumn field where three dirt roads meet, a single old tree, evening light"),
("017",["tuongquan"],1,"waist-up of a Han army officer in iron armour giving an order, holding a rolled scroll with one hand, other arm hidden behind his back, exactly one man"),
("018",["liubei"],1,"waist-up of Liu Bei in plain light armour standing in a military camp at dusk, tired but alert, a spear held upright in one hand, exactly one man, far arm hidden"),
("019",[],0,"an empty county government hall with a bare desk, an empty chair and one scroll left behind, grey window light"),
("020",["liubei"],1,"waist-up of Liu Bei in a plain dark robe and a small black official cap sitting at a county desk reading a bamboo slip, tired face, exactly one man, his free hand hidden under the desk"),
("021",[],0,"a small county town gate broken open with scattered baskets and a toppled cart, dust in the air"),
("022",[],0,"a worn pair of straw sandals and a small cloth bundle resting beside a roadside tree at dusk"),
("023",["congtonton"],1,"waist-up portrait of Gongsun Zan, a northern commander, calm sharp look, exactly one man, his arms hidden behind a wooden railing"),
("024",["congtonton","liubei"],2,"waist-up two-shot of Gongsun Zan and Liu Bei standing facing each other and greeting, both with hands tucked into their sleeves, warm meeting, exactly two men"),
("025",[],0,"a wide plain with rows of plain tents and tall plain red banners of an army camp at dawn, smoke from cooking fires, empty of people"),
("026",["liubei"],1,"waist-up of Liu Bei in a dark-blue robe and a black official cap, the look of a county chief, calm, exactly one man, both arms hidden in his sleeves"),
("027",[],0,"a walled county town on a flat river plain at morning with green fields and a slow river, seen from a hill"),
("028",["quanvu","trieuphi"],2,"waist-up two-shot of Guan Yu and Zhang Fei standing side by side, calm serious faces, exactly two men, their outer arms hidden"),
("029",["quanvu"],1,"waist-up of Guan Yu standing in front of a row of simple spears planted in the ground, giving an order, exactly one man, his far arm hidden"),
("030",["trieuphi"],1,"waist-up of Zhang Fei standing guard at a doorway holding a long spear in one hand, alert round eyes, exactly one man, the other arm hidden behind the spear"),
("031",[],0,"a long wooden spear and a plain sword in a sheath leaning against a door frame beside a rolled sleeping mat"),
("032",[],0,"an empty rice jar with a bare bottom and a flat empty cloth purse on a wooden table, soft light"),
("033",["quanvu","trieuphi"],2,"waist-up two-shot of Guan Yu and Zhang Fei sitting side by side near a small camp fire at night looking at the flames, exactly two men, outer arms hidden"),
("034",[],0,"a plain clay wine jar and three pottery cups on a rough wooden table, nothing else, evening light"),
("035",["liubei"],1,"waist-up of Liu Bei looking down with a grave quiet expression, exactly one man, both arms hidden"),
("036",["luubinh"],1,"waist-up of a sour-faced official looking down his nose with contempt, exactly one man, his arms hidden in his sleeves"),
("037",["luubinh","thichkhach"],2,"waist-up two-shot of an official handing a small cloth bag of coins to a masked man in dark clothes, exactly two men, their outer arms hidden, dim room"),
("038",["liubei","thichkhach"],2,"waist-up two-shot of Liu Bei pouring wine from a jug into a cup with one hand for a guest in dark clothes sitting opposite, friendly welcome, exactly two men, the guest's hands in his lap, Liu Bei's other arm hidden"),
("039",["thichkhach"],1,"waist-up of a lean man in dark plain clothes looking down with a troubled conscience, exactly one man, his arms hidden"),
("040",[],0,"a low table with a shared steaming pot and four wooden bowls, warm lamp light in a humble room"),
("041",["liubei","quanvu","trieuphi"],3,"three small distant figures walking side by side along a long dusty road at sunset, seen from far away from behind, exactly three men"),
("042",[],0,"the tall gate towers of a great palace at dusk with a cracked wall and a flag hanging limp"),
("043",["linhde"],1,"waist-up of Emperor Ling lying propped up on a bed, pale and gaunt, exhausted face, exactly one man, hands hidden under the blanket"),
("044",["thieude"],1,"waist-up of a thin frightened young emperor seated on a plain throne in an oversized crown, exactly one person, hands hidden in his sleeves"),
("045",["hatien"],1,"waist-up of a heavy-set general in a dark-red robe and black cap, confident arrogant bearing, exactly one man, his arms hidden in his sleeves"),
("046",["hatien","hoanquan"],2,"waist-up two-shot of a heavy-set general and a pale beardless eunuch facing each other with tense expressions, exactly two men, their hands hidden in sleeves"),
("047",[],0,"a bamboo message tube and a rolled summons scroll sealed with a red cord on a dark wooden table, candlelight"),
("048",[],0,"a long palace corridor at night with long shadows and a dropped black official cap on the floor, torch light"),
("049",["vienthieu"],1,"waist-up of Yuan Shao in light armour, stern determined face, one hand resting on his belt, exactly one man, the other arm hidden"),
("050",["thieude","hiende"],2,"waist-up two-shot of a frightened teenage emperor and his small young brother walking at night by a river, looking back, exactly two boys, their outer arms hidden"),
("051",["dongtrac"],1,"waist-up of a huge heavy general in iron armour with a cruel narrow-eyed face standing tall, exactly one man, arms hidden behind his back"),
("052",[],0,"a long column of cavalry dust approaching a city gate under a grey sky, tall plain red banners, no people visible"),
("053",["dongtrac","thieude"],2,"waist-up two-shot of a huge heavy general seated on a high-backed chair and a thin young emperor standing before him with head bowed, exactly two people, their hands hidden"),
("054",[],0,"an empty throne on a dais in a palace hall with a dark robe draped over its arm, cold light from a window"),
("055",[],0,"a large painted cloth map of Han lands spread on a table with a single small stone marker far in the north and a small palace sign in the south"),
("056",[],0,"a ridge crowded with tall plain banners of many different colours blowing in the wind, no people visible"),
("057",["taotao"],1,"waist-up of Cao Cao in plain travelling clothes on a night road looking back over his shoulder with sharp eyes, exactly one man, his arms hidden under his cloak"),
("058",["taotao"],1,"waist-up of Cao Cao standing in front of rows of simple spears planted in the ground, ambitious look, exactly one man, his far arm hidden"),
("059",[],0,"a large round table with a painted map, a plain jade cup and one empty chair in a tent, lamp light"),
("060",["taotao","tonkien"],2,"waist-up two-shot of Cao Cao and Sun Jian standing side by side, serious faces, exactly two men, their outer arms hidden"),
("061",[],0,"a tall fortress pass gate between two steep rocky cliffs in mist, heavy stone walls"),
("062",["liubei"],1,"Liu Bei seen from behind looking across a wide valley at a far fortress pass in mist, exactly one man, arms hidden"),
("063",[],0,"a heavy dented iron helmet resting on a rough wooden stand in a tent, soft light"),
("064",["tonkien"],1,"waist-up of Sun Jian with a red headband and a determined fierce look, exactly one man, his far arm hidden"),
("065",[],0,"the skyline of a great burning city at night with black smoke and orange flames over palace roofs"),
("066",[],0,"a wide encampment of many plain tents with cold cooking fires and empty ground, grey morning"),
("067",[],0,"a dust cloud of a single marching column going north along a road with one tall red banner"),
("068",[],0,"a quiet river plain with farmland and a small town in the distance, soft morning light"),
("069",["dan"],2,"waist-up of two poor peasant men side by side bowing respectfully with hands tucked into their sleeves, exactly two men"),
("070",["vienthieu"],1,"waist-up of Yuan Shao seated at a desk writing a letter with a brush in one hand, exactly one man, his other arm hidden under the desk"),
("071",["liubei"],1,"waist-up of Liu Bei sitting alone beneath a large mulberry tree looking up at its round crown, calm thoughtful face, exactly one man, his arms hidden"),
("072",[],0,"an empty grain storehouse with its door open and a bare earth floor, grey light"),
("073",["dongtrac"],1,"waist-up of a huge heavy general in dark fur-trimmed robe with a menacing narrow-eyed stare, exactly one man, his hands hidden in his sleeves"),
("074",["quanvu"],1,"waist-up of Guan Yu standing alone at a tent entrance at night holding a pottery cup in one hand, calm stern face, exactly one man, the other arm hidden"),
("075",[],0,"a road leading toward a far mountain pass at sunset, orange sky, empty land"),
("076",["quanvu"],1,"waist-up of Guan Yu in profile with his chin raised proudly, a long black beard, calm cold eyes, exactly one man, his arms hidden"),
("077",["trieuphi"],1,"waist-up of Zhang Fei with a fierce frowning face and bristling beard, glaring to the side, exactly one man, his arms hidden"),
("078",[],0,"a worn leather chest guard and a rough black headscarf hanging side by side on a wooden post in a tent, soft light"),
("079",[],0,"a long river with many small separate army camps on both banks, plain banners, early morning mist, empty of people"),
("080",["taotao"],1,"waist-up of Cao Cao leaning over a table with one hand pressed on a painted map, frowning impatient face, exactly one man, the other arm hidden"),
("081",[],0,"a broken spear and a torn plain blue banner lying on a riverbank after a lost battle, grey dusk"),
("082",["taotao"],1,"waist-up of Cao Cao standing at the edge of a river at dusk looking at the water with a hard determined face, exactly one man, his arms hidden"),
("083",["vienthieu","congtonton"],2,"waist-up two-shot of Yuan Shao and Gongsun Zan standing apart facing different directions with a painted map between them, cold tense mood, exactly two men, their outer arms hidden"),
("084",["liubei"],1,"waist-up of Liu Bei in profile facing left with a firm quiet look, exactly one man, both arms hidden in his sleeves"),
("085",[],0,"a letter written on a rolled silk sheet with a red wax seal resting on a dark wooden desk, soft candle light"),
]

# ---- Đợt sửa 2026-10-15: bỏ ảnh đồ vật/cảnh vắng, thêm cảnh có người, quân đội, đánh trận (đúng thời Hán) ----
# key: (nhân vật, số người ở tiền cảnh, mô tả, có đám đông nhỏ phía sau)
OV = {
"007": ([],0,"a plain two-wheeled Han wooden official carriage with a small canopy standing in front of the gate, plain Chinese Han-dynasty county office: rammed-earth wall, simple wooden gate, pitched roof of grey tiles with short eaves, an empty yard",False),
"008": (["docbuu","quanlai"],2,"the provincial inspector standing upright at the top of the stone steps of a county office, chin raised, hands hidden in his wide sleeves, looking down with arrogance, while a small county clerk bows deeply on the steps below him, exactly two men",False),
"013": (["liubei","docbuu"],2,"Liu Bei standing in a torch-lit stone courtyard at night holding a long plain wooden rod planted upright on the ground with one hand, his other arm hidden behind his back, stern face; at his feet the provincial inspector sits on the ground with a rope tied round his chest and his head bowed, calm and upright, exactly two men",False),
"015": (["liubei"],1,"waist-up of Liu Bei hanging a small bronze seal on its cord on a wooden post beside a county gate with one hand, his other arm hidden, looking toward the road with quiet resolve, dawn light, exactly one man",False),
"016": (["liubei","tuongquan"],2,"waist-up of Liu Bei bowing slightly before a Han recruiting officer who sits behind a low table with a bamboo register, behind them a long line of poor men waiting on the road to join the army, exactly two men in the foreground",True),
"018": (["liubei","linhhan"],2,"Liu Bei in plain light armour holding a spear in both hands, advancing at the front with one Han soldier beside him against bandit rebels on a dusty field, smoke far behind, behind them rows of many small fighters clashing with spears",True),
"019": (["liubei"],1,"Liu Bei seen from behind standing in the open doorway of an empty county hall, leaving, his arms hidden; inside the hall a low wooden table with a rolled scroll and a reed sitting mat on the floor, a wooden lattice window with paper panes, only a low table and a reed mat as furniture, grey morning light, exactly one man",False),
"020": (["liubei"],1,"waist-up of Liu Bei in a plain dark robe and a small black cloth cap kneeling at a low wooden table reading a bamboo slip held in one hand, a reed mat on the floor, tired face, exactly one man, his other arm hidden",False),
"021": (["linhhan","giacuop"],2,"bandit rebels storming through the broken wooden gate of a small county town while county soldiers in grey-brown armour retreat, dust and smoke, in the foreground one retreating county soldier looking back and one rebel with a spear, behind them many small fighters",True),
"025": (["linhhan"],2,"wide shot of two armies of spearmen meeting on a wide plain seen from a low hill, two Han soldiers with lowered spears in the foreground, behind them dense ranks of many small soldiers with plain red banners on one side and plain dark-blue banners on the other",True),
"027": (["liubei","quanlai"],1,"waist-up of Liu Bei in a dark-blue robe and a black cap standing at the gate of a walled county town on a morning plain, his arms hidden in his sleeves, behind him two rows of townspeople and small officials bowing in welcome, green fields and a slow river behind",True),
"031": (["quanvu","trieuphi"],2,"waist-up two-shot of Guan Yu and Zhang Fei standing shoulder to shoulder in front of a tent entrance at night as guards, each holding a long spear upright with one hand, torch glow behind them, exactly two men, their outer arms hidden",False),
"032": (["liubei"],1,"waist-up of Liu Bei sitting on the bare floor of a poor hut looking down at an empty clay grain jar in front of him, tired but calm, exactly one man, his hands hidden in his sleeves",False),
"034": (["liubei","quanvu","trieuphi"],3,"Liu Bei, Guan Yu and Zhang Fei standing side by side under a blossoming peach tree in solemn silence, heads slightly bowed, hands clasped inside their sleeves, soft light, exactly three men",False),
"040": (["liubei","quanvu","trieuphi"],3,"three men sitting on a reed mat around a low table sharing a steaming pot of food, Liu Bei in the middle, a small bronze oil lamp with a tiny open flame on the table, their hands resting below the table edge, warm humble room, exactly three men",False),
"048": (["hoanquan","hatien"],2,"a narrow palace corridor at night with torchlight and long shadows, in the foreground a pale beardless court eunuch in a dark-purple robe waits in the shadow behind a wooden pillar with his hands hidden in his sleeves looking down the corridor, far down the corridor the small figure of a heavy-set general in a dark-red robe walks away from the viewer, exactly two men",False),
"050": (["thieude_lung","hiende"],2,"two boys seen from behind walking side by side along a dark river bank at night, a thin teenage boy in rumpled dark-red robes with his hair in a topknot under a small flat cap and a small boy of about nine in a plain dark robe with two small tufts of hair, their backs to the viewer, moonlight on the water, tall reeds, exactly two boys, both clearly male",False),
"052": (["linhbien"],1,"a long column of frontier soldiers in fur caps and fur-trimmed iron-scale armour marching in ranks through the great gate of Luoyang city, spears upright, tall plain dark-red banners, one foreground soldier and many small marching soldiers behind him",True),
"056": (["tuongquan"],1,"a coalition army camp on a wide ridge, rows of soldiers standing in formation before many tents under tall plain banners of many different colours blowing in the wind, in the foreground one army officer in iron armour looking over the camp",True),
"059": (["vienthieu","tuongquan"],2,"Yuan Shao in light armour standing on a low wooden platform being acclaimed as leader with a regional officer in armour beside him, before them rows of armoured officers and soldiers standing in ranks facing them",True),
"061": (["linhhan"],1,"a tall fortress pass gate between two steep rocky cliffs in mist, in front of it ranks of Han soldiers with spears and tall plain banners assembling, one foreground soldier seen from behind looking at the gate, exactly one man in the foreground",True),
"063": (["huahung"],1,"waist-up of Hua Xiong, a huge burly general in dark iron armour and a heavy iron helmet standing before the gate of a fortress, fierce confident stare, exactly one man, his arms hidden behind his back",False),
"064": (["tonkien"],1,"Sun Jian in a red headband and iron armour striding forward at the head of his soldiers with a long spear held in both hands, determined fierce face, behind him ranks of many small soldiers with spears and one tall plain red banner",True),
"065": (["dancu"],1,"a long column of refugees and soldiers with bundles and ox-carts leaving a city gate, one refugee with a bundle in the foreground seen from behind, behind them the great city burning at night with black smoke and orange flames over palace roofs",True),
"066": (["linhhan"],1,"the wide encampment of the coalition, soldiers standing idle and sitting on the ground beside piled spears and cold cooking pots in front of many plain tents, grey morning, nobody fighting, one soldier sitting in the foreground with his arms hidden",True),
"067": (["linhtonkien"],1,"a column of Sun Jian's soldiers marching north along a dusty road with spears upright and a tall plain red banner at the head, one soldier in a red headband marching in the foreground, many small marching figures behind in rows",True),
"075": (["linhhan"],1,"a long column of soldiers with spears and plain banners marching along a road toward a far mountain pass at sunset, orange sky, one soldier seen from behind in the foreground, many small dark figures ahead",True),
"079": (["tuongquan"],1,"a wide view down a river valley, many separate army camps on both banks and columns of soldiers converging under plain banners in early morning mist, one commander in iron armour seen from behind in the foreground on a hill, hundreds of tiny soldiers",True),
"081": (["linhhan"],2,"the defeated army retreating along a riverbank at dusk with torn plain blue banners and broken spears, two tired soldiers walking side by side in the foreground with heads down, behind them a long ragged line of retreating soldiers, grey sky",True),
}
CROWD = {k for k,v in OV.items() if v[3]}
S = [(k,)+OV[k][:3] if k in OV else (k,nv,n,m) for k,nv,n,m in S]
SKEYS = [s[0] for s in S]

# (chương, lời kể, khóa ảnh)
B = [
("Mở đầu","Tập trước kết thúc ở một cảnh rất lạ: một viên đốc bưu bị trói, và bị đánh hai trăm gậy.","001"),
("Mở đầu","Trong tiểu thuyết, người ra tay là Trương Phi. Nhưng Tam quốc chí chép rõ: đó là chính Lưu Bị.","002"),
("Mở đầu","Vì sao một viên huyện úy nhỏ bé dám làm vậy? Và sau đêm ấy, ông đi đâu?","003"),
("Mở đầu","Câu trả lời không phải một chiến công. Đó là nhiều năm lang bạt: bỏ chức, đổi chủ, và nhiều lần thất bại.","004"),
("Mở đầu","Còn ở kinh đô, trong lúc ông chưa là ai, thiên hạ đã bắt đầu đổi chủ.","005"),
("Mở đầu","Đây là Tam Quốc theo chính sử, tập hai.","006"),
("Viên đốc bưu","Đốc bưu là quan do quận phái xuống, đi kiểm tra các huyện và xét công tội của quan lại.","007"),
("Viên đốc bưu","Một lời của đốc bưu có thể khiến một viên quan nhỏ mất chức, và mất luôn đường sống.","008"),
("Viên đốc bưu","Bản chú Điển lược mà Bùi Tùng Chi dẫn kể rằng khi ấy có lệnh thải bớt những người được bổ chức nhờ quân công, và Lưu Bị lo mình nằm trong số đó.","009"),
("Viên đốc bưu","Ông xin gặp đốc bưu nhưng không được cho vào.","010"),
("Viên đốc bưu","Ông bèn dẫn lính tới nhà trạm, xông vào, nói: ta có mật lệnh của quan phủ, đến bắt đốc bưu.","011"),
("Viên đốc bưu","Rồi ông trói đốc bưu trên giường và đưa ra tận ranh giới huyện.","012"),
("Viên đốc bưu","Tam quốc chí chép gọn hơn: ông trói viên đốc bưu, đánh hai trăm gậy, rồi bỏ chức chạy đi.","013"),
("Viên đốc bưu","Một viên huyện úy vừa đánh quan trên thì chỉ còn một đường: biến mất.","014"),
("Viên đốc bưu","Ông bỏ luôn chức quan duy nhất mình có, và không biết ngày mai sẽ ở đâu.","015"),
("Làm quan rồi mất chức","Sử không chép ông về quê ngay. Ông tiếp tục tìm đường làm lính, làm quan.","016"),
("Làm quan rồi mất chức","Theo Tam quốc chí, đại tướng quân Hà Tiến sai người đi tuyển quân ở Đan Dương, và Lưu Bị đi theo.","017"),
("Làm quan rồi mất chức","Quân đi tới Hạ Bì thì gặp giặc. Ông đánh có công, được bổ một chức thừa ở huyện Hạ Mật.","018"),
("Làm quan rồi mất chức","Nhưng sử lại chép ông bỏ chức ấy. Không có một lời giải thích.","019"),
("Làm quan rồi mất chức","Sau đó ông làm huyện úy ở Cao Đường, rồi làm huyện lệnh.","020"),
("Làm quan rồi mất chức","Rồi giặc đến đánh, quân của huyện bị đánh tan, ông lại phải bỏ chạy.","021"),
("Làm quan rồi mất chức","Làm quan, mất chức, làm quan, chạy giặc. Trong nhiều năm, ông không có một chỗ đứng cố định.","022"),
("Làm quan rồi mất chức","Cuối cùng ông tìm đến một người bạn cũ từng học chung dưới trướng thầy Lư Thực: Công Tôn Toản.","023"),
("Làm quan rồi mất chức","Công Tôn Toản lúc ấy có quân ở phía bắc. Ông tâu xin cho Lưu Bị làm Biệt bộ tư mã.","024"),
("Làm quan rồi mất chức","Lưu Bị cùng Điền Giai đánh quân của Viên Thiệu, và nhiều lần lập công.","025"),
("Làm quan rồi mất chức","Nhờ những chiến công ấy, ông được thử làm lệnh Bình Nguyên, rồi làm tướng Bình Nguyên.","026"),
("Làm quan rồi mất chức","Lần đầu tiên, người từng bán giày cỏ được cai quản cả một vùng đất.","027"),
("Những người ở lại","Khi ông làm tướng Bình Nguyên, sử chép Quan Vũ và Trương Phi được giao làm Biệt bộ tư mã, mỗi người chỉ huy một phần quân.","028"),
("Những người ở lại","Đây là lần đầu hai người có quân riêng. Nhưng họ vẫn đi theo ông, không đi theo ai khác.","029"),
("Những người ở lại","Từ đầu, sử đã gọi họ là người hộ vệ. Hộ vệ nghĩa là người đứng ra phía trước ông khi có chuyện.","030"),
("Những người ở lại","Khi nguy hiểm đến, họ không đứng sau. Đó là ý nghĩa của hai chữ ấy.","031"),
("Những người ở lại","Một viên quan chạy trốn như Lưu Bị lúc ấy không có gì để giữ người: không lương, không đất, không chức.","032"),
("Những người ở lại","Vậy mà hai người vẫn ở lại. Sử không nói vì sao, chỉ chép rằng họ ở lại.","033"),
("Những người ở lại","Tiểu thuyết giải thích điều đó bằng một lời thề. Còn sử chỉ cho ta một sự thật đơn giản hơn: họ đi cùng nhau rất lâu, và không bỏ nhau.","034"),
("Những người ở lại","Mấy chục năm sau, khi Quan Vũ rồi Trương Phi lần lượt mất, người ta mới thấy bốn chữ ân nghĩa như anh em nặng đến mức nào.","035"),
("Những người ở lại","Trần Thọ, tác giả Tam quốc chí, nhận xét rằng Quan Vũ cứng cỏi mà tự phụ, còn Trương Phi hung bạo mà thiếu ơn nghĩa với người dưới.","076"),
("Những người ở lại","Hai người tính khí khác nhau rõ rệt, và cũng không hoàn hảo. Nhưng cùng một lòng với Lưu Bị.","077"),
("Những người ở lại","Chính hai điểm yếu ấy sau này đã trả giá rất đắt. Nhưng ở thời điểm này, họ là hai người đáng tin nhất mà ông có.","078"),
("Những người ở lại","Ở Bình Nguyên có một người tên Lưu Bình, rất coi thường Lưu Bị, và không chịu được việc ông được dân quý.","036"),
("Những người ở lại","Lưu Bình bèn thuê một thích khách đi giết ông.","037"),
("Những người ở lại","Lưu Bị không hay biết gì, vẫn đối đãi người khách ấy rất hậu.","038"),
("Những người ở lại","Người khách cảm động, nói thật mọi việc với ông, rồi bỏ đi.","039"),
("Những người ở lại","Ba chi tiết trong sử đều nói một điều: ông giữ người không bằng sức mạnh, mà bằng cách đối xử.","040"),
("Những người ở lại","Đó có thể là thứ duy nhất ông có, khi chưa có binh và chưa có đất.","041"),
("Trong lúc ấy, ở kinh đô","Trong lúc Lưu Bị lang bạt khắp nơi, nhà Hán đang tự đổ sập từ bên trong.","042"),
("Trong lúc ấy, ở kinh đô","Năm một trăm tám mươi chín, Hoàng đế Linh đế mất.","043"),
("Trong lúc ấy, ở kinh đô","Con của hoàng hậu họ Hà là Lưu Biện lên ngôi, khi còn rất trẻ. Quyền thật nằm trong tay cậu ông, đại tướng quân Hà Tiến.","044"),
("Trong lúc ấy, ở kinh đô","Hà Tiến vốn xuất thân từ nhà làm nghề đồ tể, nhờ em gái được vào cung mà lên tới chức vị cao nhất của quân đội.","045"),
("Trong lúc ấy, ở kinh đô","Ông muốn trừ bọn hoạn quan, những kẻ đã nắm quyền từ thời Linh đế bán chức quan.","046"),
("Trong lúc ấy, ở kinh đô","Nhưng thái hậu không đồng ý. Hà Tiến liền triệu các tướng ngoài biên vào kinh để gây sức ép, trong đó có Đổng Trác.","047"),
("Trong lúc ấy, ở kinh đô","Kế hoạch bị lộ. Hoạn quan ra tay trước và giết Hà Tiến ngay trong cung.","048"),
("Trong lúc ấy, ở kinh đô","Viên Thiệu cùng nhiều người đem quân vào cung, giết rất nhiều hoạn quan, và cả hoàng cung loạn như một đêm không có luật.","049"),
("Trong lúc ấy, ở kinh đô","Trong cảnh hỗn loạn ấy, hoàng đế trẻ và em ông bị đưa ra ngoài thành.","050"),
("Trong lúc ấy, ở kinh đô","Đúng lúc ấy, Đổng Trác dẫn quân tới nơi, gặp hoàng đế và đưa về kinh.","051"),
("Trong lúc ấy, ở kinh đô","Từ đó, quân đội trong kinh đô nằm trong tay một người đến từ vùng biên cương.","052"),
("Trong lúc ấy, ở kinh đô","Ông phế Thiếu đế, lập người em là Lưu Hiệp, người sau này là Hán Hiến đế.","053"),
("Trong lúc ấy, ở kinh đô","Đó chính là điều tập một đã nói: khi người có quân không còn ai quản được, triều đình chỉ còn cái tên.","054"),
("Trong lúc ấy, ở kinh đô","Một người nghèo như Lưu Bị lúc ấy còn quá xa kinh đô để có thể can thiệp vào chuyện này.","055"),
("Liên quân năm 190","Năm một trăm chín mươi, nhiều châu quận nổi binh chống Đổng Trác, họp thành một liên quân.","056"),
("Liên quân năm 190","Một trong những người đứng lên sớm nhất là Tào Tháo. Khi Đổng Trác muốn dùng ông làm quan, ông bỏ kinh đô chạy trốn.","057"),
("Liên quân năm 190","Ông dựng quân ở Trần Lưu, bằng tiền của những người ủng hộ mình.","058"),
("Liên quân năm 190","Viên Thiệu được các châu quận đưa lên làm minh chủ của liên quân.","059"),
("Liên quân năm 190","Trong liên quân có Tào Tháo, Tôn Kiên và nhiều người khác.","060"),
("Liên quân năm 190","Nghe thì rất hùng mạnh: hơn mười đạo quân từ nhiều châu quận cùng kéo tới.","079"),
("Liên quân năm 190","Nhưng mỗi người đều lo giữ quân của mình trước. Không ai muốn là người đầu tiên bị tổn thất.","080"),
("Liên quân năm 190","Trong tiểu thuyết, đây là nơi ba anh em Lưu Bị, Quan Vũ, Trương Phi cùng đánh Lữ Bố ở Hổ Lao.","061"),
("Liên quân năm 190","Nhưng trong Tiên chủ truyện không có một chữ nào về trận ấy.","062"),
("Liên quân năm 190","Và cái tên Hoa Hùng, vị tướng bị chém trong cảnh nổi tiếng ấy, trong sử cũng gắn với một người khác.","063"),
("Liên quân năm 190","Nhiều nguồn chép rằng người đánh bại Hoa Hùng là Tôn Kiên.","064"),
("Liên quân năm 190","Đổng Trác sợ liên quân, bắt hoàng đế dời đô về Trường An, và cho đốt cả Lạc Dương.","065"),
("Liên quân năm 190","Liên quân đông người, nhưng nhiều người chỉ đứng nhìn, không ai muốn tiến lên trước.","066"),
("Liên quân năm 190","Chỉ có một đạo quân từ phương nam kéo lên, và đó là quân của Tôn Kiên.","067"),
("Liên quân năm 190","Tào Tháo trách các tướng chần chừ, và tự mình dẫn quân đuổi theo Đổng Trác, nhưng bị đánh bại.","081"),
("Liên quân năm 190","Đó là lần đầu người ta thấy một Tào Tháo thất bại, và vẫn bước tiếp.","082"),
("Người mà cả một châu muốn đón","Quay lại Bình Nguyên: Lưu Bị lúc này mới thật sự có một vùng đất để cai quản.","068"),
("Người mà cả một châu muốn đón","Cùng lúc ấy, ở phía bắc, Viên Thiệu và Công Tôn Toản đã bắt đầu tranh nhau. Liên minh chống Đổng Trác nhanh chóng vỡ ra.","083"),
("Người mà cả một châu muốn đón","Và giữa hai người ấy, Lưu Bị đứng về phía người bạn học cũ.","084"),
("Người mà cả một châu muốn đón","Chú giải của Bùi Tùng Chi dẫn Hiến Đế xuân thu: dân Từ Châu về sau muốn tôn nguyên tướng Bình Nguyên Lưu Bị làm chủ.","069"),
("Người mà cả một châu muốn đón","Viên Thiệu khi nghe tin cũng nói: Lưu Huyền Đức hoằng nhã, có tín nghĩa, dân Từ Châu mến ông, đúng như mong đợi.","070"),
("Người mà cả một châu muốn đón","Cho nên lời khen của Viên Thiệu dành cho ông là lời khen của một người từng đứng ở phía đối lập.","085"),
("Người mà cả một châu muốn đón","Người từng bị chú quát vì một câu nói về chiếc xe lọng, giờ được cả một châu nhắc tên.","071"),
("Người mà cả một châu muốn đón","Nhưng danh tiếng chưa phải là quân đội, và đất đai chưa phải là chỗ đứng chắc chắn.","072"),
("Người mà cả một châu muốn đón","Kinh đô đã vào tay Đổng Trác. Câu hỏi của tập sau là: ai sẽ đứng lên chống lại ông ta?","073"),
("Người mà cả một châu muốn đón","Và người mà tiểu thuyết gán cho công lớn nhất ở Hổ Lao, trong sử, đang đứng ở đâu?","074"),
("Người mà cả một châu muốn đón","Tập sau sẽ kể tiếp.","075"),
]
# ghép nhóm theo chương (mỗi chương tối đa 7 câu để giọng đọc khớp ảnh)
def _split(bs, mx=7):
    n = -(-len(bs) // mx); sz = -(-len(bs) // n)
    return [bs[i:i+sz] for i in range(0, len(bs), sz)]
GIONG = json.loads((ROOT / "scripts" / "TQ1.json").read_text(encoding="utf-8"))["giong_them"]

def img(k): return f"assets/anh_2d/TQ2/{k}.jpg"
order = []
for t,_,k in B:
    if t not in order: order.append(t)
chapters = []
for t in order:
    bs = [(x,k) for tt,x,k in B if tt == t]
    for part in _split(bs):
        chapters.append({"beats": [{"text": x, "ai": "ancient Han China scene, 2D ligne claire", "anh_file": img(k)} for x,k in part]})
used = [k for _,_,k in B]
assert len(used) == len(set(used)), "ảnh lặp"
assert set(used) <= set(SKEYS) and set(SKEYS) <= set(used), (set(used) ^ set(SKEYS))
words = sum(len(x.split()) for _,x,_ in B)
print(f"dài: {len(B)} cảnh, {words} chữ, ước tính {words*0.343/60:.1f} phút")

NGAN = [
("hook","Tập trước, Lưu Bị trói một viên đốc bưu và đánh hai trăm gậy. Trong tiểu thuyết, đó là Trương Phi. Trong sử, là chính ông.",("013","011")),
("boi_canh","Rồi ông bỏ chức và biến mất.",("014","015")),
("boi_canh","Nhiều năm sau, ông lại làm quan, lại mất chức, rồi lại phải chạy giặc.",("019","021")),
("leo_thang","Cuối cùng ông tìm đến bạn học cũ Công Tôn Toản, và đánh nhiều trận cho ông ta.",("023","024")),
("leo_thang","Nhờ chiến công, ông lên làm tướng Bình Nguyên, lần đầu tiên cai quản cả một vùng đất.",("026","027")),
("leo_thang","Có kẻ thuê người đến giết ông. Ông không biết, vẫn đối đãi người ấy rất hậu. Thích khách cảm động, nói thật rồi bỏ đi.",("037","038")),
("cu_lat","Trong lúc đó, kinh đô vỡ vụn: Hà Tiến bị giết, và Đổng Trác dẫn quân vào thành.",("048","051")),
("cu_lat","Lưu Bị không có binh, không có tiền, nhưng ông có một thứ: cách đối xử khiến người ta ở lại.",("040","041")),
("vong_lap","Nhưng liên quân đánh Đổng Trác sắp bắt đầu. Và cảnh nổi tiếng ở Hổ Lao… không giống như bạn từng nghe. Sử thật… lạ hơn cả truyện.",("061","074")),
]
ngan_beats = [{"loai_canh": lc, "text": t, "images": [{"anh_file": img(a)}, {"anh_file": img(b)}]} for lc,t,(a,b) in NGAN]
BIA = {"anh": img("011"), "nen": img("010"), "huy_hieu": "TAM QUỐC CHÍNH SỬ · TẬP 2", "dong1": "KHÔNG PHẢI", "dong2": "TRƯƠNG PHI", "gach": True,
       "dong3": "Ai thật sự đánh viên đốc bưu?"}
script = {
 "id": "TQ2", "topic": "lich-su",
 "title": "Ai đánh viên đốc bưu? Lưu Bị lang bạt thế nào trước loạn Đổng Trác",
 "caption": "Trong tiểu thuyết là Trương Phi, nhưng sử chép chính Lưu Bị trói và đánh đốc bưu. Rồi ông đi đâu? Tam Quốc theo chính sử, tập 2 🏯",
 "hashtags": ["nguoigacsu","tamquoc","luubi","lichsu","dongtrac","chinhsu"],
 "sources": [
  "Trần Thọ, Tam quốc chí, Thục thư, Tiên chủ truyện (bản dịch tiếng Anh, the-scholars.com) và chú giải Bùi Tùng Chi (Điển lược, Ngụy thư, Hiến Đế xuân thu) qua sanguozhi.5000yan.com",
  "Hậu Hán thư và Tư trị thông giám (phần kinh đô năm 189 và liên quân năm 190) — chưa đối chiếu nguyên văn",
 ],
 "nguon_link": [
  {"ten": "Bản dịch hiện đại Tiên chủ truyện, sanguozhi.5000yan.com", "url": "https://sanguozhi.5000yan.com/", "ngon_ngu": "tiếng Trung"},
  {"ten": "Bản dịch tiếng Anh Tiên chủ truyện, the-scholars.com", "url": "https://the-scholars.com/", "ngon_ngu": "tiếng Anh"},
 ],
 "music": "none", "giong_them": GIONG, "pronounce": {},
 "long": {
  "chuyen_canh": "fade",
  "title": "Ai đánh viên đốc bưu? Lưu Bị lang bạt thế nào trước loạn Đổng Trác | Tam Quốc theo chính sử, tập 2",
  "title_card": "Tam Quốc chính sử: **Đốc bưu** bị trói",
  "description": "Trong tiểu thuyết, Trương Phi đánh viên đốc bưu. Nhưng Tam quốc chí chép chính Lưu Bị làm vậy, rồi bỏ chức chạy đi. Tập 2 của series Tam Quốc theo chính sử kể về những năm lang bạt của Lưu Bị, cách ông giữ được Quan Vũ và Trương Phi, và kinh đô nhà Hán sụp đổ năm 189 với Đổng Trác.",
  "voice": "Sadaltager", "music": "none", "bia": BIA, "chapters": chapters,
 },
 "binh_luan": {
  "dai": {"ghim": "Tập này kể tiếp vụ đốc bưu: tiểu thuyết cho Trương Phi đánh, còn Tam quốc chí chép là Lưu Bị. Một số chi tiết ở phần kinh đô năm 189 và liên quân năm 190 lấy từ Hậu Hán thư; hình ảnh là tranh minh họa.", "phu": []},
  "ngan": {"ghim": "Về người đánh đốc bưu: Tam quốc chí chép chính Lưu Bị trói và đánh đốc bưu hai trăm gậy; tiểu thuyết đổi thành Trương Phi 🏯", "phu": []},
 },
 "ngan": {
  "hook_text": "Đánh đốc bưu là Lưu Bị\n**không phải Trương Phi**",
  "hooks": ["Trong tiểu thuyết là Trương Phi đánh đốc bưu. Nhưng sử chép là một người khác."],
  "caption": "Trong tiểu thuyết là Trương Phi, nhưng sử chép chính Lưu Bị trói và đánh đốc bưu. Rồi ông đi đâu? Tam Quốc theo chính sử, tập 2 🏯",
  "beats": ngan_beats, "bia": BIA, "anh_bia": img("011"),
 },
}
script["scenes"] = [{"type": "hook" if i == 0 else "text", "text": b["text"], "voice": b["text"]} for i,b in enumerate(ngan_beats)]
(ROOT/"scripts"/"TQ2.json").write_text(json.dumps(script, ensure_ascii=False, indent=1), encoding="utf-8")

# TQ2.json + TQ2_anh.json
t2 = {"ma": "TQ2", "ghi_chu": "Tập 2: đốc bưu, lang bạt, kinh đô 189, liên quân 190", "nhan_vat_phu": PHU,
      "canh": [{"key": k, "nv": nv, "so_nguoi": n, "mo_ta": m} for k,nv,n,m in S],
      "ngan": [{"beat": i+1, "anh": list(p)} for i,(_,_,p) in enumerate(NGAN)]}
(R/"TQ2.json").write_text(json.dumps(t2, ensure_ascii=False, indent=1), encoding="utf-8")
SUF = ("medium shot, simple natural poses, every person has exactly two arms, two hands and two legs with natural adult proportions, "
       "serious weathered faces, no extra limbs, no duplicated people, no deformed faces, no text, no letters, no watermark. "
       "Flags and banners are plain solid colour with no symbols. All objects are realistic with no faces")
ARMY = ("Han dynasty soldiers: iron lamellar or scale armour over knee-length tunics, plain iron helmets, long wooden-shafted spears, halberds, straight single-edged swords, "
        "rectangular wooden shields and crossbows, soldiers on foot hold spears upright or lowered with both hands")
SUF_WIDE = SUF.replace("medium shot, simple natural poses", "wide establishing shot, orderly ranks, simple natural poses")
out = []
for k,nv,n,m in S:
    cnt = "No people in the picture." if n == 0 else f"The picture contains exactly {n} {'person' if n == 1 else 'people'} in the foreground and no one else."
    if n == 0:
        out.append({"key": k, "nv": [], "prompt": m + ". An empty quiet scene of objects and landscape only. 2D franco-belgian ligne claire comic illustration of ancient China, clean uniform dark ink outlines, flat muted colours with soft shading, earthy palette of ochre, jade green, indigo and warm cream, no text, no numerals, no letters, no watermark, not 3D, not a photo"})
        continue
    if k in CROWD:
        cnt = f"The picture contains exactly {n} {'person' if n == 1 else 'people'} in the foreground, and behind them a large crowd of many small distant figures in orderly rows."
    chars = " Characters (keep exactly this look): " + "; ".join(NV[x] for x in nv) + "."
    out.append({"key": k, "nv": nv, "prompt": f'{m}. {cnt}{chars} {tq["phong_cach"]}. ' + (f"{ARMY}. {SUF_WIDE}" if k in CROWD else SUF)})
(R/"TQ2_anh.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print("ok", len(S), "ảnh")
