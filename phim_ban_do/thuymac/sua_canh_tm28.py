# Vẽ lại 25 tranh tm28 sau khi soát toàn bộ 84 tranh (26/11): thuyền xanh trông hiện đại, nhiều thuyền xanh, thuyền kiểu châu Âu,
# đường nhựa, cờ sao vàng, mũ sắt hiện đại, bản đồ thế giới, súng trường, vua Chăm giống hoàng đế Trung Quốc, thành kiểu châu Âu, cảnh không khớp lời.
import json,sys
sys.path.insert(0,'/tmp/pc/phim_ban_do/thuymac');import canh_tm28 as c
S=c.S.replace("no glasses.","no glasses, no modern ships, no European sailing ships, no steamships, no paved roads, no national flags, no stars on flags, no modern helmets, no rifles, no muskets.")
BOAT="ancient 14th-century Southeast Asian wooden war boats with long narrow planked hulls, high curved carved prows and sterns, rows of oars, a single mast with one rectangular sail of woven bamboo matting"
GB="among them exactly one boat of the same ancient kind has its wooden hull lacquered faded jade green, the only green thing in the picture; every other boat is unpainted dark wood"
CBN="the Cham king Che Bong Nga of Champa, dark-skinned, curled black beard, gold necklaces and armbands, a tall tiered pointed golden crown shaped like a Cham brick temple tower, a dark red robe with gold borders, not Chinese, not an emperor's flat hat"
VN=c.VN;CH=c.CH;BLK=c.BLK;TKC=c.TKC;DTB=c.DTB;DT=c.DT
GUN="hand cannons that are short bronze tubes fixed on the end of long wooden poles, held under the arm and lit with a slow match, not rifles"
DOBAN="the Cham capital Do Ban: thick red-brick city walls without battlements, and tall Cham brick tower temples with tiered roofs rising inside, palm trees"
R={
'a01':'A broad misty river crowded with over a hundred '+BOAT+', '+GB+'.',
'a02':'From a riverbank camp of '+VN+', '+BLK+' runs in fear toward the soldiers and points his arm at the river, where '+BOAT+' float; '+GB+'.',
'a03':CBN+' stands on the deck of a large '+BOAT.split(' with ')[0].replace('boats','boat')+', surrounded by Cham spearmen with white head wraps, looking north across the sea.',
'a09':'In a dim hall with plain wooden walls, a grieving Vietnamese noblewoman in a dark mourning robe kneels and pleads before '+CBN+', who sits listening, an oil lamp burning, no writing anywhere.',
'a14':'A Vietnamese frontier garrison camp of wooden palisades in a mountain pass near the sea, '+DTB+' standing at the gate with '+VN+', everyone bareheaded or with black head cloths.',
'a19':'An old Vietnamese official kneels on a tiled floor before an empty throne, holding up a blank folded paper memorial in both hands, plain walls with no writing.',
'a20':'An old Vietnamese official in a long robe walks away alone along a narrow dirt footpath between rice fields at dusk, his black official hat left behind on a stone by the path.',
'a21':'A huge Vietnamese army of '+VN+' marching out through a wooden city gate, plain long dark cloth banners without any symbols, dust rising.',
'a24':'A large Vietnamese army camp on a coastal plain at dawn; in the distance '+DOBAN+'.',
'a25':'Outside the walls of '+DOBAN+', a camp of '+CH+', a lone Cham official in a white wrapped garment walking out toward a distant Vietnamese camp.',
'a33':'Seen from a hilltop, one single long column of Vietnamese soldiers on a dirt road through palm-covered hills, the front part of the column far ahead and separated from the rear part by a long empty stretch of road.',
'a39':'A rice convoy of oxcarts turning back on a narrow dirt mountain track, an official in a court robe on horseback leading them away in a hurry.',
'a42':'Ancient Cham '+BOAT.split('ancient 14th-century Southeast Asian ')[1]+' caught in a violent storm at a river mouth, giant waves breaking, masts snapping, sailors falling into the sea.',
'a53':'A grey battlefield after defeat in a muddy river valley, abandoned spears, broken rattan shields and torn dark banners in the mud, a lone rider leaving in the distance.',
'a54':'An empty wooden throne hall at dusk, '+c.NT+' sitting alone deep in thought, a simple hand-drawn sketch of rivers and mountains on a paper scroll unrolled on the floor.',
'a61':'A wide river suddenly filled with the sails of over a hundred approaching '+BOAT+', morning mist, '+GB+'.',
'a62':CBN+' stands at the bow of an ancient wooden war boat with a carved curved prow and a woven matting sail, its hull lacquered faded jade green, many dark wooden war boats behind him.',
'a63':'Seen from behind Vietnamese wooden palisades on a riverbank, a loose scattered fleet of '+BOAT+' not yet in formation on the river, '+GB+'.',
'a66':BLK+' stands beside '+TKC+' on the riverbank and points at the river, where '+BOAT+' float; '+GB+'.',
'a68':TKC+' raises his sword and gives the order, beside him a row of Vietnamese soldiers holding '+GUN+', aimed at the river.',
'a69':'On a riverbank, a row of Vietnamese soldiers in dark tunics firing '+GUN+', bursts of flame from the tube mouths and huge clouds of gunpowder smoke rolling over the river.',
'a69b':'Thick white gunpowder smoke drifting across a river full of '+BOAT+', sails half hidden in the smoke, '+GB+'.',
'a71':'On the deck of an ancient wooden war boat with a jade green lacquered hull, Cham attendants with white head wraps kneel around a fallen man wearing a tall pointed golden Cham crown, weeping, smoke drifting over the river.',
'a80':'A Cham general being crowned king before a tall red-brick Cham tower temple with tiered roof, Cham priests around him; far away on a road two young Cham nobles flee north on foot.',
'a82':'A calm empty river at sunset, a single abandoned ancient wooden war boat with a carved curved prow and a torn woven matting sail, its hull lacquered faded jade green, drifting among reeds, distant mountains, no people.',
}
if __name__=='__main__':
    L=[{'key':k,'nv':[],'w':1344,'h':768,'seed':900+i,'prompt':p+' '+S} for i,(k,p) in enumerate(R.items())]
    json.dump(L,open('/tmp/pc/ke-hoach/nhan-vat/NBTM28S_anh.json','w'),ensure_ascii=False,indent=1);print(len(L))
