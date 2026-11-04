"""Bản đồ vector chi tiết vùng Kinh – Dương (Trường Giang, Hán thủy, hồ Động Đình, Bà Dương...).
Nền phẳng kiểu giấy da, sông ngòi và hồ lấy từ Natural Earth (vector), núi vẽ biểu tượng, lưới kinh vĩ tuyến mảnh."""
import json,math,os
from PIL import Image,ImageDraw,ImageFilter
LON0,LON1,LAT0,LAT1=108.0,120.6,28.0,34.4
S=800;F=S/480;KX=S*math.cos(math.radians(31.2))
RW=int((LON1-LON0)*KX);RH=int((LAT1-LAT0)*S)
def wp(lon,lat): return ((lon-LON0)*KX,(LAT1-lat)*S)
NE=os.environ.get('NE','/tmp/claude-0/ne')
LAND=(236,224,190);SEA=(150,186,200);SEAD=(112,152,172);RIV=(78,134,170);RIVD=(52,100,140);LKF=(128,176,200)
HIDE_LAKES={'Danjiangkou Shuiku','Xinanjiang Shuiku'}
def rings(g):
    if g['type']=='Polygon': return [g['coordinates']]
    return g['coordinates']
def inb(pts,pad=0.5):
    xs=[p[0] for p in pts];ys=[p[1] for p in pts]
    return not(max(xs)<LON0-pad or min(xs)>LON1+pad or max(ys)<LAT0-pad or min(ys)>LAT1+pad)
MOUNT=[((115.6,31.2),1.3,9),((111.2,32.4),0.7,6),((110.2,31.1),0.9,7),((116.0,29.6),0.35,4),((109.2,33.3),0.9,7),((113.4,31.0),0.4,3),((117.6,30.3),0.6,5),((118.4,29.9),0.7,5),((119.4,31.0),0.4,3),((112.6,29.1),0.6,4),((110.6,29.4),0.8,6),((114.6,29.0),0.5,4),((115.2,33.5),0.0,0)]
if __name__=='__main__':
    print(RW,RH)
    img=Image.new('RGB',(RW,RH),SEA);d=ImageDraw.Draw(img)
    J=json.load(open(NE+'/ne_land.json'))
    for f in J['features']:
        for poly in rings(f['geometry']):
            if not inb(poly[0],1.5): continue
            d.polygon([wp(*p) for p in poly[0]],fill=LAND)
            for h in poly[1:]: d.polygon([wp(*p) for p in h],fill=SEA)
    # vùng nước nông quanh bờ biển (viền xanh nhạt)
    # lưới kinh vĩ
    for lo in range(int(LON0)+1,int(LON1)+1):
        x=wp(lo,LAT0)[0];d.line([(x,0),(x,RH)],fill=(206,194,160),width=3)
    for la in range(int(LAT0)+1,int(LAT1)+1):
        y=wp(LON0,la)[1];d.line([(0,y),(RW,y)],fill=(206,194,160),width=3)
    # hồ
    LK=json.load(open(NE+'/ne_lakes.json'))
    for f in LK['features']:
        g=f['geometry']
        if not g or (f['properties'].get('name') in HIDE_LAKES): continue
        for poly in rings(g):
            if not inb(poly[0],0.2): continue
            pts=[wp(*p) for p in poly[0]]
            d.polygon(pts,fill=LKF,outline=RIVD)
            d.line(pts+[pts[0]],fill=RIVD,width=int(3*F))
    # sông
    R=json.load(open(NE+'/ne_rivers.json'))
    wid={'Yangtze':14,'Han':9,'Huai':8,'Gan':7,'Yuan':6,'Xiang':7,'Fuchun':5,'Wu':5,'Hudi':4,'Quan':4,'Ying':5,'Dan':5,'Ou':4}
    for f in R['features']:
        g=f['geometry']
        if not g: continue
        n=f['properties'].get('name_en') or f['properties'].get('name') or ''
        w=wid.get(n,4)
        gs=g['coordinates'] if g['type']=='MultiLineString' else [g['coordinates']]
        for ln in gs:
            if not inb(ln,0.2): continue
            pts=[wp(*p[:2]) for p in ln]
            d.line(pts,fill=RIVD,width=int((w+4)*F),joint='curve');d.line(pts,fill=RIV,width=int(w*F),joint='curve')
    img=img.filter(ImageFilter.GaussianBlur(1.2))
    # núi: biểu tượng vector
    import random
    rnd=random.Random(5);d=ImageDraw.Draw(img,'RGBA')
    for (lo,la),r,k in MOUNT:
        cx,cy=wp(lo,la)
        for i in range(int(k*6*F*F*0.5)):
            a=rnd.uniform(0,6.283);rad=abs(rnd.gauss(0,r*S*0.45))
            x=cx+math.cos(a)*rad*1.3;y=cy+math.sin(a)*rad*0.8
            if not(0<x<RW and 0<y<RH): continue
            px=img.getpixel((int(x),int(y)))
            if px[2]>px[0]+10: continue
            s=rnd.uniform(14,26)*F
            d.polygon([(x-s,y+s*0.55),(x,y-s*0.9),(x+s,y+s*0.55)],fill=(176,152,104,235),outline=(96,72,44,255))
            d.polygon([(x,y-s*0.9),(x+s,y+s*0.55),(x+s*0.15,y+s*0.55)],fill=(110,86,56,170))
    # khung
    d.rectangle((0,0,RW-1,RH-1),outline=(96,72,44),width=10)
    img.save('world6.jpg',quality=90)
    img.resize((1960,int(1960*RH/RW)),Image.LANCZOS).save('/tmp/claude-0/world6_prev.jpg',quality=88)
