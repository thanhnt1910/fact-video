# Danh sách cảnh tm28 (chủ kênh 26/11): 100% tranh thủy mặc vẽ bằng FLUX, khoảng 40 cảnh chuyển thành clip Veo (chủ kênh làm tay trong Google Flow).
# Mỗi cảnh: (mã, đoạn, mô tả tranh tiếng Anh, chuyển động Veo hoặc None). Chạy: python3 canh_tm28.py -> NBTM28A/B/C_anh.json + ke-hoach/tm28-veo-flow.md
import json
S=("Traditional East Asian ink wash painting on warm aged rice paper, monochrome black ink with faint sepia wash, bold expressive brush strokes, soft ink bleeding, drifting mist, epic heroic mood, "
   "cinematic wide horizontal composition with all important subjects inside the middle horizontal band, plain empty paper at top and bottom. "
   "No text, no calligraphy, no letters, no red seal, no stamp, no signature, no border, no frame.")
VN="14th century Vietnamese Tran dynasty soldiers in dark knee-length tunics, cloth headbands, round rattan shields and long spears"
CH="Cham soldiers of Champa with bare chests, white head wraps and dark wrapped sarongs, long spears and tall narrow shields"
CBN="the Cham king Che Bong Nga, a bearded man with a tall pointed crown and a long dark robe with patterned borders"
DT="a Vietnamese king in a plain black robe over hard lamellar armour, short beard"
DL="a stern middle-aged Vietnamese general with a long beard in leather armour"
DTB="a plump Vietnamese mandarin in a wide-sleeved court robe and black winged official hat"
NT="an elderly Vietnamese retired king with a white beard in a pale robe and low crown"
TKC="the Vietnamese general Tran Khat Chan, middle-aged, short black beard, dark robe over bronze scale armour, a sash at the waist and a sword"
BLK="a thin young Cham servant in a short pale tunic and white head wrap, barefoot"
LN="a Cham general in armour riding a war elephant"
XANH="one boat in the fleet is painted muted jade green, the only colour in the painting"
C=[
('a01',1,'A broad river crowded with over a hundred ancient wooden war boats with square sails, low morning mist, '+XANH+'.','Slow push-in over the river; sails ripple in the wind, the boats drift slowly forward, mist moves across the water.'),
('a02',2,'From a riverbank camp of '+VN+', '+BLK+' runs in fear toward the soldiers and points his arm out at the fleet on the river, '+XANH+'.','The servant runs a few steps toward the soldiers and slowly raises his arm to point at the river; soldiers turn their heads; the camera stays still.'),
('a03',3,CBN+' stands on the deck of a large war boat, surrounded by spearmen, looking toward a distant walled city on the horizon.','Slow push-in toward the king; his robe and the banners move in the wind; the boat rocks gently.'),
('a04',4,'Close view of an outstretched pointing hand in the foreground, beyond it a misty river full of war boats with sails.',None),
('a05',5,'A vast map-like ink landscape seen from very high above: a long coastline, mountains along the west, rivers flowing to the sea, a kingdom in the north and another stretching along the southern coast.',None),
('a06',6,'A fleet of Cham war boats with square sails entering a wide river mouth from the open sea, waves crashing, '+CH+' crowding the decks.','The fleet moves forward into the river mouth; waves roll and break; sails fill with wind.'),
('a07',7,'A royal boat with a canopy crossing a wide river in haste, courtiers rowing hard, an empty city wall on the far bank behind them.',None),
('a08',8,'A Vietnamese wooden palace with curved tiled roofs on fire at night, tall flames and thick smoke, '+CH+' running through the courtyard, scrolls and papers burning on the ground.','Flames rise and flicker, smoke billows upward, burning papers drift in the air; small figures run across the courtyard.'),
('a09',9,'In a dim hall, a grieving noblewoman in a dark mourning robe kneels and speaks to a seated foreign king, candles burning.',None),
('a10',10,'An abandoned frontier fortress with broken wooden gates and empty watchtowers, weeds growing, a quiet road running south through the hills.',None),
('a11',11,'An old Vietnamese scholar-historian in a robe writes with a brush at a low desk by lamplight, stacks of bound books around him.',None),
('a12',12,'Ranks of '+CH+' training on a field under a hot sun, raising spears together, war elephants standing behind them, '+CBN+' and a general watching from a platform.',None),
('a13',13,'A great army of '+CH+' with war elephants advancing over the dunes of a southern coastline, banners flying.','The army marches forward, elephants sway, banners and dust stream in the wind; slow lateral camera move.'),
('a14',14,'A Vietnamese frontier garrison camp in a mountain pass near the sea, '+DTB+' standing at the gate with soldiers.',None),
('a15',15,'A procession of Cham envoys carrying ten round trays heaped with gold ingots on their shoulders toward a Vietnamese camp gate.',None),
('a16',16,'Close view of ten round trays piled with gleaming gold ingots on a low table in a tent, '+DTB+' leaning over them with greedy eyes.','Slow push-in on the gold trays; the lamp flame flickers and light shimmers on the gold; the mandarin leans slightly closer.'),
('a17',17,DTB+' writing a report with a brush at a desk at night, the trays of gold hidden behind a curtain in the shadow.',None),
('a18',18,'In a royal hall, '+DT+' rises angrily from the throne holding a report scroll, officials bowing low on both sides.',None),
('a19',19,'An old official kneels before the throne in a royal hall holding up a memorial in both hands, pleading.',None),
('a20',20,'An old official walks away alone along a long empty road at dusk, his official hat left behind on a stone at the roadside.',None),
('a21',21,'A huge Vietnamese army of '+VN+' marching out of a city gate, banners and flags covering the road as far as the eye can see.','The army marches toward the camera, banners ripple, dust rises; slow pull-back revealing more columns.'),
('a22',22,'A fleet of Vietnamese war boats sailing along a coast while '+DT+' on horseback leads infantry along the sandy shore.','Boats sail forward on the sea, the king and the infantry move along the beach, waves wash the sand.'),
('a23',23,'Long lines of porters and oxcarts carrying sacks of rice along a mountain road, an official in a court robe on horseback supervising.',None),
('a24',24,'A large army camp on a coastal plain at dawn, in the distance the brick walls and towers of the Cham capital city Do Ban among palm trees.','Slow push-in toward the distant city; mist drifts, camp flags ripple.'),
('a25',25,'Outside a brick city wall, a camp of '+CH+' among palm trees, a lone Cham official in a robe walking out toward a Vietnamese camp.',None),
('a26',26,'Inside a Vietnamese command tent, a small Cham official kneels and bows low before '+DT+', who stands and listens eagerly.','The kneeling official bows lower, the king leans forward slightly; lamp flame flickers; camera still.'),
('a27',27,'A quiet brick city gate with the gates half open and nobody in sight, deep shadows inside, the feeling of a hidden trap.',None),
('a28',28,DT+' mounted on a mottled black-and-white horse the colour of mud, sword raised, generals and soldiers ready behind him.','The king raises his sword higher, the horse stamps and turns its head, banners behind flap in the wind.'),
('a29',29,DL+' steps forward and bows with folded hands before the mounted king, urging caution.',None),
('a30',30,DT+' on horseback points his sword forward and shouts, refusing the advice, soldiers watching.',None),
('a31',31,'In front of the troops, two soldiers put a long flowing women\'s robe over the shoulders of '+DL+', who keeps his head lowered in shame, the king turning his back.','The two soldiers slowly drape the robe over the general\'s shoulders, the general lowers his head; the troops stay still; camera still.'),
('a32',32,'A very long thin column of '+VN+' marching in single file along a narrow road between hills and palm trees, stretching into the distance like a string of fish.','Slow aerial-like move along the column as it marches forward; dust rises from the road.'),
('a33',33,'Seen from a hilltop, the front of a marching Vietnamese column far separated from the rear, an empty gap of road between them.',None),
('a34',34,'From both sides of a road, '+CH+' charge out of the trees and tall grass with spears, crashing into a column of '+VN+'.','The ambushers rush forward out of the grass, dust and leaves fly, the column turns in confusion. No one is struck, no blood.'),
('a34b',34,'Chaotic battle on a dusty road, horses rearing, broken banners falling, '+CH+' surrounding a group of Vietnamese cavalry.','Dust swirls, horses rear, banners fall slowly; camera shakes slightly. No blood.'),
('a35',35,'A shattered Vietnamese army fleeing across a plain under a midday sun, abandoned spears and banners on the ground, smoke rising.','Soldiers run away across the plain, smoke drifts, dropped banners flap on the ground.'),
('a36',36,'A fallen black-robed king in hard armour lies on the battlefield among broken spears, a riderless mottled horse standing nearby, dust settling.','Dust slowly settles, the riderless horse lowers its head, a torn banner flutters; camera slowly pulls back.'),
('a37',37,'A Vietnamese prince in a white robe is led away captive by '+CH+', a white horse left behind.',None),
('a38',38,DTB+' sitting safely on horseback far behind the battle, watching the smoke on the horizon without moving his troops.',None),
('a39',39,'A rice convoy turning back on a mountain road, an official on horseback leading the carts away in a hurry.',None),
('a40',40,'A prisoner cart with a wooden cage carrying '+DTB+' through a village, villagers throwing tiles and bricks at it and shouting.',None),
('a41',41,'Inside a royal hall, a mandarin stripped of his hat kneels while guards hand him a soldier\'s spear and tunic.',None),
('a42',42,'Cham war boats caught in a violent storm at a river mouth, giant waves breaking, masts snapping, sailors falling into the sea.','Huge waves crash over the boats, masts bend and break, rain sweeps across; camera rocks.'),
('a43',43,'A Vietnamese official with arms bound standing before Cham soldiers who force him to kneel, a burning city behind.',None),
('a44',44,'The bound Vietnamese official stands upright and refuses to kneel, head held high, Cham spears around him.','The official lifts his chin and stays upright, the spearmen step closer; smoke drifts behind. No blood.'),
('a45',45,'A long line of '+CH+' and war elephants moving quietly along the foot of misty mountains toward a distant city.',None),
('a46',46,'War elephants charging out of a forest at the foot of mountains, scattering Vietnamese soldiers, dust everywhere.','Elephants charge forward through the dust, trees shake, soldiers scatter; camera shakes. No blood.'),
('a47',47,'At a river landing, '+NT+' steps into a royal boat with attendants, while a young scholar in a long robe runs into the shallow water toward the boat.','The boat begins to push off from the landing; the scholar runs into the water, splashing; robes move in the wind.'),
('a48',48,'A young scholar in a soaked long robe and scholar hat stands waist-deep in the river gripping the side of a royal boat with both hands, '+NT+' inside the boat.','The scholar pulls on the side of the boat, water ripples around him, the old king turns his face away; camera still.'),
('a49',49,'The royal boat sailing away across a wide misty river, a lone young scholar left standing in the water watching it go.','The boat glides slowly away into the mist; the lone scholar stays still in the water; ripples spread.'),
('a50',50,'An old historian writes at a desk at night, behind him a ghostly ink image of a lone scholar standing in a river.',None),
('a51',51,'A Vietnamese army camp beside a river in Thanh Hoa, an official in a court robe and armour mounting a horse.',None),
('a52',52,'A dam of logs and earth bursting, a flood of water rushing down a valley, war elephants charging behind the water toward Vietnamese troops.','Water bursts through the dam and rushes forward, elephants charge behind the wave, spray fills the air; camera shakes.'),
('a53',53,'A grey battlefield after defeat, abandoned helmets and spears in the mud, a lone general riding away from the battle in the distance.',None),
('a54',54,'An empty throne hall at dusk, a war map on the floor, an old retired king sitting alone and thinking.',None),
('a55',55,NT+' handing a war tally to '+TKC+', who kneels before him in a palace courtyard, soldiers of the guard behind.',None),
('a56',56,TKC+' bows deeply with tears on his face before '+NT+', who also weeps, then the general turns to lead his troops out of the gate.','The general bows slowly then rises, the old king wipes his eyes; banners ripple; camera slowly pushes in.'),
('a57',57,'A Vietnamese army halted on a riverbank, '+TKC+' standing on a rise looking across at the enemy camp on the other side.',None),
('a58',58,'A quiet river with fortified banks lined with stakes and wooden palisades, Vietnamese boats waiting behind the fortifications, winter mist.',None),
('a59',59,'A Vietnamese nobleman in a court robe leading a group of soldiers across a field toward a Cham camp with banners, turning his back on his homeland.',None),
('a60',60,'Two armies camped facing each other across a wide winter river, cooking smoke rising from both banks, still water.','Slow pan across the river; cooking smoke rises from both camps, mist drifts on the still water.'),
('a61',61,'A wide river suddenly filled with countless sails of approaching war boats, morning light, '+XANH+'.','The sails advance toward the camera, the water ripples, mist parts in front of the fleet.'),
('a62',62,CBN+' standing at the bow of a large boat painted muted jade green, looking toward the Vietnamese camp, many war boats behind him.','The king slowly raises his hand to shade his eyes, the boat moves forward, banners flap behind.'),
('a63',63,'Seen from behind Vietnamese palisades, a loose scattered fleet of war boats not yet in formation on the river, '+XANH+'.',None),
('a64',64,BLK+' running barefoot along a riverbank toward a Vietnamese camp, looking back over his shoulder in fear.','The servant runs toward the camera, glancing back; reeds sway; camera tracks slowly.'),
('a65',65,BLK+' kneeling and trembling before Vietnamese guards in a camp, his face full of fear.',None),
('a66',66,BLK+' standing beside '+TKC+' on the riverbank and pointing at the fleet on the river, '+XANH+'.','The servant extends his arm to point at the river, the general turns his head to look; camera still.'),
('a67',67,'A ghostly faded memory image: a small Cham official kneeling before a black-robed king in a tent, painted in very light pale ink like a dream.',None),
('a68',68,TKC+' raises his sword and gives the order, beside him a row of '+VN+' holding bronze hand cannons aimed at the river.','The general sweeps his sword down to give the order, the soldiers brace the cannons; camera still.'),
('a69',69,'A row of Vietnamese bronze hand cannons firing from the riverbank, bursts of flame and huge billowing clouds of gunpowder smoke rolling over the river.','Flashes of fire burst from the cannons, thick smoke billows and rolls across the river; camera shakes.'),
('a69b',69,'Thick gunpowder smoke drifting across a river full of war boats, sails half hidden in the smoke, '+XANH+'.','Smoke drifts and swirls across the water, sails appear and disappear in the smoke.'),
('a70',70,'A war boat painted muted jade green being struck, wooden planks splintering, its crew thrown into confusion.','Splinters fly from the hull, the boat rocks heavily, people on deck stagger. No blood.'),
('a71',71,'On the deck of the jade green boat, people kneel around a fallen figure in a pointed crown, weeping, smoke drifting over the river.','Smoke drifts slowly, the kneeling people bow and sway in grief; camera slowly pulls back.'),
('a72',72,'A man in a Vietnamese court robe running along the riverbank carrying a wrapped bundle, two Vietnamese guard soldiers rushing at him with spears.',None),
('a73',73,'A fleet of Cham war boats breaking apart and fleeing in every direction on the river, sails turning, smoke in the air.','The boats turn and scatter in all directions, sails swing, smoke drifts; camera slowly pulls back.'),
('a74',74,'A small boat carrying a closed wooden chest sailing down a dark river at night under the moon, a lantern at the bow.',None),
('a75',75,NT+' waking with a start in a tent at night by lamplight, reaching for a sword, guards rushing in.','The old king sits up abruptly, the lamp flame shakes, the guards burst in through the tent flap.'),
('a76',76,'Officials in court robes kneeling in rows in a lantern-lit courtyard at night, raising their arms in celebration before the retired king.',None),
('a77',77,NT+' standing at night looking out over a calm river under the moon, relieved.',None),
('a78',78,'A funeral pyre burning on a riverbank at dusk, Cham soldiers standing in silence around it, war elephants behind.','Flames rise from the pyre, sparks drift into the sky, the soldiers stand still; smoke curls.'),
('a79',79,LN+' scattering coins and treasures on a mountain road behind him as Vietnamese soldiers stop to pick them up.','Coins fly through the air from the general\'s hand, the chasing soldiers stop and bend down; the elephant keeps walking.'),
('a80',80,'A Cham general crowned king in a brick tower temple, while far away two young Cham nobles flee north on foot.',None),
('a81',81,'A wide ink landscape of the Red River and the city of Thang Long under drifting smoke, ruins of palaces, a misty southern coastline beyond.','Smoke drifts slowly over the city, the river flows; slow aerial camera move.'),
('a82',82,'A calm empty river at sunset, a single abandoned war boat painted muted jade green drifting among the reeds, '+'distant mountains.','The empty green boat drifts slowly, reeds sway, sunlight glints on the water; slow pull-back.'),
]
def main():
    V=[c for c in C if c[3]]
    for part,(a,b) in zip('ABC',[(0,30),(30,60),(60,len(C))]):
        json.dump([{'key':k,'nv':[],'w':1024,'h':1024,'prompt':(p+' '+S)} for k,_,p,_ in C[a:b]],open(f'/tmp/pc/ke-hoach/nhan-vat/NBTM28{part}_anh.json','w'),ensure_ascii=False,indent=1)
    print(len(C),'cảnh,',len(V),'clip Veo')
if __name__=='__main__': main()
