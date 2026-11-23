# Bìa tm22: thung lũng Hoa Lư bốn bề núi đá (điểm nhấn), Đinh Bộ Lĩnh đứng giữa khe núi, quân nhà Ngô ở xa dừng lại;
# tô màu nước như bản dựng; chữ lớn ở trên không đè người; logo 130 px, độ đậm .8, cách phải 44, trên 34
import numpy as np,os
from PIL import Image
from canh import *
from engine import *
from khung_dung import cam,PAP
import mau21
cv=PAP.copy();c=cam(960,540,1.0)
put(cv,c,'t22_far',960,800,ay=1,k=1,o=.9)
put(cv,c,'t22x_hoalu',960,600,s=1.0)
mau21.to_mau(cv)
put(cv,c,'t22n_dbl2',960,1010,s=1.35,ay=1,scale_px=3)
put(cv,c,'t22n_ngo',1650,960,s=.55,ay=1,scale_px=3,o=.85)
put(cv,c,'t22n_dinh',330,980,s=.6,ay=1,scale_px=3)
mau21.bui(cv,3.0)
put(cv,c,'t22_frontL',-120,1120,ax=0,ay=1,s=.85);put(cv,c,'t22_frontR',2040,1120,ax=1,ay=1,s=.8)
put_screen(cv,band(1280,210,PAPER,.86,50),900,190)
put_screen(cv,text('HAI VUA KHÔNG HẠ NỔI',112,RED,700,glow=8),900,175)
put_screen(cv,text('Đinh Bộ Lĩnh và Hoa Lư · năm 944–968',46,INK,700),900,272)
lg=np.asarray(Image.open(D+'nguoi-gac-su.png').convert('RGBA').resize((130,130),Image.LANCZOS),np.float32)/255;lg[...,:3]*=lg[...,3:4]
blend(cv,lg,1920-44-130,34,.8)
os.makedirs('/tmp/pc/assets/bia/TM22',exist_ok=True)
im=Image.fromarray((np.clip(cv,0,1)*255+.5).astype(np.uint8))
im.save('/tmp/pc/assets/bia/TM22/bia_tm22.png');im.convert('RGB').save('/tmp/pc/assets/bia/TM22/bia_tm22_youtube.jpg',quality=90);print('ok')
