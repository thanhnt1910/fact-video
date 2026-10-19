import json,math,numpy as np
from PIL import Image,ImageDraw,ImageFilter
LON0,LON1,LAT0,LAT1=108.2,121.8,31.7,38.5
S=640;KX=S*math.cos(math.radians(34.2))
RW=int((LON1-LON0)*KX);RH=int((LAT1-LAT0)*S)
def wp(lon,lat): return ((lon-LON0)*KX,(LAT1-lat)*S)
if __name__=='__main__':
    print(RW,RH)
    rng=np.random.default_rng(11)
    def fbm(w,h,oct=5,base=6):
        out=np.zeros((h,w),np.float32);amp=1;tot=0
        for o in range(oct):
            n=base*2**o;g=rng.random((int(n*h/w)+2,n+2)).astype(np.float32)
            im=Image.fromarray((g*255).astype(np.uint8)).resize((w,h),Image.BICUBIC)
            out+=np.asarray(im,np.float32)/255*amp;tot+=amp;amp*=0.5
        return out/tot
    # mặt nạ đất
    land=Image.new('L',(RW,RH),0);ld=ImageDraw.Draw(land)
    J=json.load(open('ne_land.json'))
    def rings(geom):
        if geom['type']=='Polygon': return [geom['coordinates']]
        return geom['coordinates']
    for f in J['features']:
        for poly in rings(f['geometry']):
            ext=poly[0]
            xs=[p[0] for p in ext];ys=[p[1] for p in ext]
            if max(xs)<LON0-1 or min(xs)>LON1+1 or max(ys)<LAT0-1 or min(ys)>LAT1+1: continue
            ld.polygon([wp(*p) for p in ext],fill=255)
            for h in poly[1:]: ld.polygon([wp(*p) for p in h],fill=0)
    lk=json.load(open('ne_lakes.json'))
    lakes=Image.new('L',(RW,RH),0);kd=ImageDraw.Draw(lakes)
    for f in lk['features']:
        g=f['geometry']
        if not g: continue
        for poly in rings(g):
            ext=poly[0];xs=[p[0] for p in ext];ys=[p[1] for p in ext]
            if max(xs)<LON0 or min(xs)>LON1 or max(ys)<LAT0 or min(ys)>LAT1: continue
            kd.polygon([wp(*p) for p in ext],fill=255)
    L=np.asarray(land,np.float32)/255
    Lk=np.asarray(lakes,np.float32)/255
    # địa hình giả: nhiễu + dãy núi vẽ tay
    e=fbm(RW//4,RH//4,6,5)
    ele=np.asarray(Image.fromarray((e*255).astype(np.uint8)).resize((RW,RH),Image.BICUBIC),np.float32)/255
    ridges=[((117.1,36.25),0.9,1.0),((118.2,35.7),0.55,0.8),((115.4,36.4),0.5,0.5),((113.3,33.3),1.0,0.9),((112.6,34.6),0.7,0.8),((115.2,31.9),0.9,0.9),((117.3,31.9),0.8,0.7),((119.0,31.9),0.6,0.7),((118.6,34.9),0.5,0.5),((121.0,36.5),0.6,0.7),((114.0,37.0),1.2,1.0),((113.8,38.4),0.9,1.0),((109.3,33.9),1.3,1.0),((111.0,33.9),0.9,0.9),((112.4,33.4),0.8,0.8),((119.3,36.2),0.5,0.6),((116.0,38.2),0.4,0.3)]
    X,Y=np.meshgrid(np.arange(RW,dtype=np.float32),np.arange(RH,dtype=np.float32))
    mount=np.zeros((RH,RW),np.float32)
    for (lo,la),r,h in ridges:
        cx,cy=wp(lo,la);rr=r*S
        mount+=h*np.exp(-(((X-cx)**2+(Y-cy)**2)/(2*(rr*0.55)**2)))
        rid=1-np.abs(2*np.asarray(Image.fromarray((fbm(RW//5,RH//5,6,7)*255).astype(np.uint8)).resize((RW,RH),Image.BICUBIC),np.float32)/255-1)
    mm=np.clip(mount,0,1.2)
    ele=np.clip(ele*0.22+mm*(0.30+0.65*rid),0,1)
    # đổ bóng nổi (hillshade) từ độ cao
    gy,gx=np.gradient(ele*40.0)
    shade=np.clip(0.5+(-gx*0.7+gy*0.7)*0.9,0,1)
    base=np.zeros((RH,RW,3),np.float32)
    lowc=np.array([226,212,170],np.float32);midc=np.array([196,184,130],np.float32);hic=np.array([150,132,92],np.float32)
    t=ele[...,None]
    col=np.where(t<0.5,lowc+(midc-lowc)*(t/0.5),midc+(hic-midc)*((t-0.5)/0.5))
    # vùng xanh (đồng bằng phì nhiêu): pha ít xanh lục ở nơi thấp
    green=np.clip(0.55-ele,0,1)[...,None]*np.array([-16,10,-18],np.float32)
    col=col+green
    col*= (0.70+0.62*shade)[...,None]
    grain=np.asarray(Image.fromarray((rng.random((RH//2,RW//2))*255).astype(np.uint8)).resize((RW,RH),Image.BILINEAR),np.float32)/255
    col+= (grain[...,None]-0.5)*10
    # biển
    sea=np.array([118,156,170],np.float32)+((fbm(RW//6,RH//6,4,8)-0.5)*26)[...,None].repeat(3,2)[:RH//1,:,:] if False else None
    sn=np.asarray(Image.fromarray((fbm(RW//6,RH//6,4,8)*255).astype(np.uint8)).resize((RW,RH),Image.BICUBIC),np.float32)/255
    seac=np.array([132,170,184],np.float32)+(sn[...,None]-0.5)*28
    # độ sâu: tối dần xa bờ
    Limg=Image.fromarray((L*255).astype(np.uint8))
    dist=np.asarray(Limg.filter(ImageFilter.GaussianBlur(90)),np.float32)/255  # >0 gần đất
    seac=seac*(0.78+0.30*np.clip(dist*2.2,0,1))[...,None]
    # sóng ngang mảnh
    waves=((np.sin(Y/9.0+sn*8)>0.965)*9).astype(np.float32)
    seac+=waves[...,None]
    Lm=np.asarray(Limg.filter(ImageFilter.GaussianBlur(2)),np.float32)/255
    img=col*Lm[...,None]+seac*(1-Lm[...,None])
    # bờ biển: viền tối + bóng nông
    edge=np.clip(np.asarray(Limg.filter(ImageFilter.GaussianBlur(5)),np.float32)/255,0,1)
    rim=(1-np.abs(edge-0.5)*2)
    img*= (1-0.30*rim)[...,None]
    shallow=np.clip(np.asarray(Limg.filter(ImageFilter.GaussianBlur(26)),np.float32)/255-0.05,0,0.5)*(1-Lm)
    img+= (shallow[...,None]*np.array([30,34,30],np.float32))
    # hồ
    lkm=np.asarray(Image.fromarray((Lk*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.5)),np.float32)/255
    pass
    pil=Image.fromarray(np.clip(img,0,255).astype(np.uint8))
    d=ImageDraw.Draw(pil)
    R=json.load(open('ne_rivers.json'))
    want={'Huai':0,'Yi':5,'Ying':6,'Chang Jiang':12,'Yangtze':12,'Han':6,'Huang':9}
    for f in R['features']:
        n=f['properties'].get('name') or f['properties'].get('name_en')
        if n in want and want[n]>0 and f['geometry']:
            gs=f['geometry']['coordinates'] if f['geometry']['type']=='MultiLineString' else [f['geometry']['coordinates']]
            for ln in gs:
                pts=[wp(*p[:2]) for p in ln]
                if n=='Huang': continue
                d.line(pts,fill=(92,140,164),width=want[n],joint='curve')
    # sông cổ: Tứ thủy chảy qua Hạ Bì rồi đổ vào Hoài
    SI=[(116.95,35.7),(117.2,35.3),(117.55,34.95),(117.75,34.62),(117.95,34.3),(118.15,33.9),(118.3,33.5),(118.5,33.2)]
    HUAI=[(110.0,32.2),(111.0,32.3),(112.0,32.35),(113.5,32.45),(114.7,32.6),(115.7,32.7),(116.8,32.95),(117.7,33.1),(118.3,33.3),(118.85,33.45),(119.3,33.55),(119.9,33.9),(120.3,34.2)]
    d.line([wp(*p) for p in HUAI],fill=(92,140,164),width=9,joint='curve')
    d.line([wp(*p) for p in SI],fill=(92,140,164),width=6,joint='curve')
    pil=pil.filter(ImageFilter.GaussianBlur(0.6))
    # núi vẽ tay: biểu tượng tam giác
    d=ImageDraw.Draw(pil,'RGBA')
    for (lo,la),r,h in ridges:
        cx,cy=wp(lo,la)
        for k in range(int(60*r*h)+10):
            a=rng.uniform(0,2*math.pi);rad=abs(rng.normal(0,r*S*0.33))
            x=cx+math.cos(a)*rad*1.3;y=cy+math.sin(a)*rad*0.8
            if not(0<x<RW and 0<y<RH): continue
            if L[int(y),int(x)]<0.5: continue
            s=rng.uniform(16,30)
            d.polygon([(x-s,y+s*0.6),(x,y-s*0.9),(x+s,y+s*0.6)],fill=(120,100,70,150),outline=(70,52,34,200))
            d.polygon([(x,y-s*0.9),(x+s,y+s*0.6),(x+s*0.2,y+s*0.6)],fill=(70,52,34,110))
    pil.save('world2.png')
    pil.resize((1960,1097),Image.LANCZOS).save('world2_prev.jpg',quality=88)
