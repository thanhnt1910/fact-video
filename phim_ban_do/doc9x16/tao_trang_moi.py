#!/usr/bin/env python3
"""Tạo trang dựng kiểu #07 cho video N: python tao_trang_moi.py N  -> trang_vnNn.html
Ghép: phần đầu trang_vn7b.html (đến hàm S2) + _moi_map.js + canh_vnN.js + phần cuối (render)."""
import sys,re
KEY=sys.argv[1]
N=int(KEY) if KEY.isdigit() else KEY
TAG=f'vn{N}' if isinstance(N,int) else KEY
LABEL=f'#0{N}' if isinstance(N,int) else {'xk1':'#09','xk2':'#10','xk3':'#11','xk4':'#12','xk5':'#13','xk6':'#14','xk7':'#15','xk8':'#13','xk9':'#16','xk10':'#17','xk11':'#18','xk12':'#19','xk9r':'#16','xk10r':'#17','xk11r':'#18','xk12r':'#19','xk10t':'#16','xk13t':'#17','xk14t':'#22','xk15t':'#23','xk16t':'#24','xk17t':'#25','dola2s':'#26','xk19t':'#18','xk20t':'#19','xk25t':'#20'}.get(KEY,'#00')
CFG={7:(60000,'Wikimedia Commons (CC BY / phạm vi công cộng)','katiebordner, Bex Walton, J. Hałun (CC BY) · E. Gsell'),
     3:(56000,'Wikimedia Commons (phạm vi công cộng / CC)',''),
     4:(57000,'Wikimedia Commons (phạm vi công cộng / CC)',''),
     5:(58000,'Wikimedia Commons (CC0 / phạm vi công cộng)','VuThiAnh, Gary Todd (CC0) · Daaé'),
     6:(59000,'Wikimedia Commons (phạm vi công cộng / CC)',''),
     8:(61000,'Wikimedia Commons (phạm vi công cộng / CC)',''),
     'xk1':(91000,'Wikimedia Commons (CC BY, CC BY-SA, CC0, công cộng)','dronepicr, V. Argenberg, Phương Huy, T. A. Đức, B. T. Đ. Nguyên, AJ Oswald'),
     'xk2':(92000,'Wikimedia Commons (CC BY, CC BY-SA, CC0, công cộng)','ARABCREATOR7, GDJMSP, CarlosVdeHabsburgo, Hispalois, NTNU Vitenskapsmuseet'),
     'xk3':(93000,'Wikimedia Commons (công cộng, CC)',''),
     'xk4':(94000,'Wikimedia Commons (CC BY, CC BY-SA, CC0, công cộng)','Loi Nguyen Duc, Gieng Cung, Gary Todd, Underbar dk'),
     'xk5':(95000,'Wikimedia Commons (CC BY-SA, CC0, công cộng)','Nguyen Phu Duc, Lê Tấn Lộc, F. Guerraz, S. Schmitz, Kuroczynski, Christophe95, lumoplank, Hcxtd'),
     'xk6':(96000,'Wikimedia Commons (CC BY-SA, CC0, công cộng)','Awikimate, لا روسا, ProtoplasmaKid, Gary Todd, Julien Peytard, Txllxt TxllxT, Captmondo, Milky'),
     'xk7':(97000,'Wikimedia Commons (CC BY, CC BY-SA, CC0, công cộng)','ntt, joxeankoret, Thierry46, Minhquangdo, Quangpraha, Rungbachduong, Alf van Beem, Pouazity3, A. Kahn'),
     'xk8':(98000,'Wikimedia Commons (CC BY-SA, CC0, công cộng)','Nguyen Phu Duc, Lê Tấn Lộc, F. Guerraz, S. Schmitz, lumoplank, Hcxtd, Kondo Seisai'),
     'xk9':(99000,'Wikimedia Commons (CC BY, CC BY-SA, công cộng)','L. Kaliyappan, A.-L. Lepère, La Presse, USMC Archives, Library of Congress'),
     'xk10':(100000,'Wikimedia Commons (CC BY, CC BY-SA, công cộng)','xiquinhosilva, I. Giel, shankar s., Zossolino, YikyuenG'),
     'xk11':(101000,'Wikimedia Commons (CC BY, công cộng)','R. Mortel, P. Dieulefils, D. Stanley, dronepicr, B. Walton, C. Hicks'),
     'xk9r':(103000,'Wikimedia Commons (CC BY, CC BY-SA, công cộng)','L. Kaliyappan, A.-L. Lepère, La Presse, USMC Archives, Library of Congress'),
     'xk10r':(104000,'Wikimedia Commons (CC BY, CC BY-SA, công cộng)','xiquinhosilva, I. Giel, shankar s., Zossolino, YikyuenG'),
     'xk11r':(105000,'Wikimedia Commons (CC BY, công cộng)','R. Mortel, P. Dieulefils, D. Stanley, dronepicr, B. Walton, C. Hicks'),
     'xk12r':(106000,'Wikimedia Commons (CC0, CC BY, CC BY-SA, công cộng)','lumoplank, J.-P. Dalbéra, Cartacaro.fr, D. G. Jarvis, Newone, J. Láscar'),
     'xk10t':(111000,'Wikimedia Commons (CC BY-SA, công cộng)','Sumit Surai, An undesired fidelity (CC BY-SA) · La Domenica del Corriere, Roger-Violett'),
     'xk14t':(114000,'Wikimedia Commons (công cộng)','NASA Earth Observatory, U.S. Army'),
     'xk13t':(113000,'Wikimedia Commons (CC BY 2.0, CC BY-SA, công cộng)','J.-M. Moullec, Ngô Sĩ Liên'),
     'xk25t':(125000,'=Nguồn: Britannica, World History Encyclopedia, nghiên cứu của J. Haldon',''),
     'xk19t':(120000,'=Nguồn: Oxford, Đại học Hamburg, World History Encyclopedia',''),
     'xk12':(102000,'Wikimedia Commons (CC0, CC BY, CC BY-SA, công cộng)','lumoplank, J.-P. Dalbéra, Cartacaro.fr, D. G. Jarvis, Newone, J. Láscar')}
base,cr1,cr2=CFG[N]
s=open('trang_vn7b.html',encoding='utf-8').read()
i_end=s.index('function S2(');i_end=s.index('\n',i_end)+1
head=s[:i_end]
foot=s[s.index("SCN.forEach((s,i)=>{if(i>0&&s.bg!=SCN"):]
foot=foot.replace('window.render=function(t){let shx=0,shy=0;','window.render=function(t){if(window.THEME_UPD)THEME_UPD(t);let shx=0,shy=0;')
head=head.replace('60000',str(base)).replace('dims_vn7.js',f'dims_{TAG}.js').replace('#07',LABEL).replace('assets/vn7/',f'assets/{TAG}/')
# Facebook che góc: chữ HUD xuống dưới nút quay lại (y>=190), bỏ chữ NGƯỜI GÁC SỬ ở góc dưới trái
head=head.replace("T(HUD,52,82,","T(HUD,52,210,").replace("T(HUD,52,128,","T(HUD,52,256,").replace("T(HUD,52,156,","T(HUD,52,284,").replace("T(HUD,52,1862,'NGƯỜI GÁC SỬ',26,'#f1e9d2',7,'start');",'')
head=head.replace('Ảnh: Wikimedia Commons (CC BY / phạm vi công cộng)',cr1[1:] if cr1.startswith('=') else 'Ảnh: '+cr1)
head=head.replace('katiebordner, Bex Walton, J. Hałun (CC BY) · E. Gsell',cr2)
brick="const brick=(g,w,col)=>{const k=el(g,'g',{});el(k,'rect',{x:-w/2,y:-28,width:w,height:56,rx:6,fill:col,stroke:'#1b140c','stroke-width':5});for(let i=1;i<7;i++)el(k,'line',{x1:-w/2+i*w/7,y1:i%2?-28:0,x2:-w/2+i*w/7,y2:i%2?0:28,stroke:'#1b140c','stroke-width':3});el(k,'line',{x1:-w/2,y1:0,x2:w/2,y2:0,stroke:'#1b140c','stroke-width':3});return k};\n"
helpers=open('_moi_cc.js',encoding='utf-8').read()
out=head+brick+open('_moi_map.js',encoding='utf-8').read()+helpers+open(f'canh_{TAG}.js',encoding='utf-8').read()+'\n'+foot
open(f'trang_{TAG}n.html','w',encoding='utf-8').write(out);print(f'trang_{TAG}n.html',len(out))
