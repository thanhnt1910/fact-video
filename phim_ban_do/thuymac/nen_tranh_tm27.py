# Xử lý nền FLUX cho tm27: xóa chữ Hán giả và dấu triện đỏ (tự dò), xóa thêm vùng chỉ định (thuyền, người lạ),
# đổi về tông giấy và mực của series, lưu thành PNG trong a/ (t27_bg_<tên>.png, khổ 1024).
import cv2,numpy as np,sys,os
sys.path.insert(0,'/tmp/gen/bd')
from engine import INK,PAPER
SRC={'bd_chieu':'NBTM27B','bd_trieu':'NBTM27B','bien_a':'NBTM27B','bien_b':'NBTM27B','dem_bien':'NBTM27B','deo_d':'NBTM27B',
     'dong_b':'NBTM27B','mo_a':'NBTM27B','ngua_da':'NBTM27B','rung_a':'NBTM27B','song_hoa':'NBTM27B',
     'deo_a':'NBTM27','song_a':'NBTM27','song_b':'NBTM27','deo_b':'NBTM27'}
THEM={'deo_d':[(950,745,992,855)],'bd_trieu':[(0,380,260,470),(380,370,470,420),(560,380,620,420)],'bien_a':[(260,470,330,500)],'bien_b':[(170,520,230,600)],
      'dong_b':[(950,640,1015,770)],'mo_a':[(128,478,204,557),(838,486,928,566)],'dem_bien':[(0,0,1024,40),(0,0,40,1024),(984,0,1024,1024),(0,980,1024,1024)],'song_hoa':[]}
def xu_ly(k):
    im=cv2.imread(f'/tmp/pc/assets/anh_2d/{SRC[k]}_cf/{k}.jpg');h,w=im.shape[:2]
    b,g,r=[im[...,i].astype(np.int16) for i in range(3)];L=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY).astype(np.float32)
    red=((r-g)>38)&(r>110)
    loc=cv2.blur(L,(41,41))
    txt=(L<125)&(loc>165)
    zone=np.zeros_like(txt);zone[:int(h*.5),:240]=1;zone[:int(h*.5),w-240:]=1;zone[int(h*.82):,:200]=1;zone[int(h*.82):,w-200:]=1
    m=((red|(txt&zone))*255).astype(np.uint8)
    for x0,y0,x1,y1 in THEM.get(k,[]):
        if k!='dem_bien': m[y0:y1,x0:x1]=255
    m=cv2.dilate(m,np.ones((11,11),np.uint8))
    out=cv2.inpaint(im,m,11,cv2.INPAINT_TELEA)
    pap=np.percentile(im.reshape(-1,3),97,axis=0)
    bright=(m>0)&(cv2.blur(L,(81,81))>150)
    if k=='mo_a': bright[:]=False
    out[bright]=(out[bright]*.15+pap*.85).astype(np.uint8)
    if k=='dem_bien':   # khung viền tối: cắt bỏ rồi phóng lại
        out=cv2.resize(out[50:974,50:974],(1024,1024),interpolation=cv2.INTER_CUBIC)
    L=cv2.cvtColor(out,cv2.COLOR_BGR2GRAY).astype(np.float32)
    p=np.percentile(L,97);v=np.clip(L/p,0,1)**1.12
    if k=='dem_bien': v=np.clip(L/np.percentile(L,99.5),0,1)
    rgb=INK[None,None,:]+v[...,None]*(PAPER-INK)[None,None,:]
    o=(np.clip(rgb,0,1)*255).astype(np.uint8)
    cv2.imwrite(f'/tmp/gen/bd/a/t27n_bg_{k}.png',cv2.cvtColor(o,cv2.COLOR_RGB2BGR),[cv2.IMWRITE_PNG_COMPRESSION,9])
    return m
if __name__=='__main__':
    from PIL import Image
    ks=sys.argv[1:] or list(SRC);tiles=[]
    for k in ks:
        xu_ly(k);tiles.append(Image.open(f'/tmp/gen/bd/a/t27n_bg_{k}.png').resize((300,300)))
    s=Image.new('RGB',(1500,300*((len(tiles)+4)//5)))
    for i,t in enumerate(tiles): s.paste(t,((i%5)*300,(i//5)*300))
    s.save('/dev/shm/bgx.jpg');print(ks)
