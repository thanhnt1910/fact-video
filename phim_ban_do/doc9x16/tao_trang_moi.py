#!/usr/bin/env python3
"""Tạo trang dựng kiểu #07 cho video N: python tao_trang_moi.py N  -> trang_vnNn.html
Ghép: phần đầu trang_vn7b.html (đến hàm S2) + _moi_map.js + canh_vnN.js + phần cuối (render)."""
import sys,re
N=int(sys.argv[1])
CFG={3:(56000,'Wikimedia Commons (phạm vi công cộng / CC)',''),
     4:(57000,'Wikimedia Commons (phạm vi công cộng / CC)',''),
     5:(58000,'Wikimedia Commons (CC0 / phạm vi công cộng)','VuThiAnh, Gary Todd (CC0) · Daaé'),
     6:(59000,'Wikimedia Commons (phạm vi công cộng / CC)',''),
     8:(61000,'Wikimedia Commons (phạm vi công cộng / CC)','')}
base,cr1,cr2=CFG[N]
s=open('trang_vn7b.html',encoding='utf-8').read()
i_end=s.index('function S2(');i_end=s.index('\n',i_end)+1
head=s[:i_end]
foot=s[s.index("SCN.forEach((s,i)=>{if(i>0&&s.bg!=SCN"):]
head=head.replace('60000',str(base)).replace('dims_vn7.js',f'dims_vn{N}.js').replace('#07',f'#0{N}').replace('assets/vn7/',f'assets/vn{N}/')
head=head.replace('Ảnh: Wikimedia Commons (CC BY / phạm vi công cộng)','Ảnh: '+cr1)
head=head.replace('katiebordner, Bex Walton, J. Hałun (CC BY) · E. Gsell',cr2)
brick="const brick=(g,w,col)=>{const k=el(g,'g',{});el(k,'rect',{x:-w/2,y:-28,width:w,height:56,rx:6,fill:col,stroke:'#1b140c','stroke-width':5});for(let i=1;i<7;i++)el(k,'line',{x1:-w/2+i*w/7,y1:i%2?-28:0,x2:-w/2+i*w/7,y2:i%2?0:28,stroke:'#1b140c','stroke-width':3});el(k,'line',{x1:-w/2,y1:0,x2:w/2,y2:0,stroke:'#1b140c','stroke-width':3});return k};\n"
helpers=open('_moi_cc.js',encoding='utf-8').read()
out=head+brick+open('_moi_map.js',encoding='utf-8').read()+helpers+open(f'canh_vn{N}.js',encoding='utf-8').read()+'\n'+foot
open(f'trang_vn{N}n.html','w',encoding='utf-8').write(out);print(f'trang_vn{N}n.html',len(out))
