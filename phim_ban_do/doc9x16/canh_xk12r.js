// ===== Chùa Một Cột (xk12). Ảnh: mc1(1) mc3(2) mc7(3) mc6(4) mc2(5) mc8(8) mc5(10) mc4(12). Cảnh 6,7,9,11 vẽ phẳng.
// ===== Dấu ấn riêng: nền AO SEN (xanh ngọc), vòng sóng nước lan ở đáy khung (y>1580)
{DR1.setAttribute('opacity',0);DR2.setAttribute('opacity',0);
 DARKG.firstChild.setAttribute('fill','#0f2523');
 [...PAPG.children].forEach(c=>{if(c.tagName=='g')c.setAttribute('opacity',0);if(c.tagName=='line')c.setAttribute('stroke','rgba(40,110,100,.12)')});
 PAPG.firstChild.setAttribute('fill','#dcead9');
 const mk=(p,col)=>{const g=el(p,'g',{});const rs=[0,1,2].map(i=>el(g,'ellipse',{cx:540,cy:1740,rx:10,ry:3,fill:'none',stroke:col,'stroke-width':4}));return rs};
 const a=mk(DARKG,'#5fb3a5'),b=mk(PAPG,'#2f8a7a');
 const lot=(p,x,y,c)=>{const g=el(p,'g',{opacity:.55,transform:`translate(${x},${y})`});for(let i=-2;i<=2;i++)el(g,'ellipse',{cx:i*18,cy:-Math.abs(i)*6,rx:12,ry:30,fill:c,transform:`rotate(${i*22} ${i*18} 0)`});return g};
 lot(DARKG,160,1760,'#e58aa6');lot(DARKG,900,1700,'#f0b0c4');lot(PAPG,160,1760,'#e58aa6');lot(PAPG,900,1700,'#f0b0c4');
 window.THEME_UPD=t=>{[a,b].forEach(rs=>rs.forEach((e,i)=>{const u=((t*.35+i/3)%1);e.setAttribute('rx',40+u*420);e.setAttribute('ry',10+u*70);e.setAttribute('opacity',(1-u)*.8)}))};
}

const HB=[];const bm=(t,l)=>{sx(t,'boom',l?{light:true,g:.8}:{g:1});if(!l)HB.push(t)};
const PUT=(o,x,y,u,sc=1,rot=0)=>{o.setAttribute('transform',`translate(${x},${y}) rotate(${rot}) scale(${Math.max(.001,u)*sc})`);o.setAttribute('opacity',u>0?1:0)};
const SIG=(g,col,seed)=>{const k=el(g,'g',{});const r=rng(seed);let d='M-90 10';for(let i=0;i<7;i++)d+=` q${12+r()*10} ${-50-r()*40} ${22+r()*8} ${10+r()*20} t${22+r()*10} ${-6}`;el(k,'path',{d,fill:'none',stroke:col,'stroke-width':8,'stroke-linecap':'round','stroke-linejoin':'round'});return k};
const XX=(g,col='#e5483f')=>{const k=el(g,'g',{});el(k,'path',{d:'M-70 -70 L70 70 M70 -70 L-70 70',stroke:'#fff','stroke-width':34,'stroke-linecap':'round'});el(k,'path',{d:'M-70 -70 L70 70 M70 -70 L-70 70',stroke:col,'stroke-width':20,'stroke-linecap':'round'});return k};
const BEAM=(g,w)=>{const k=el(g,'g',{});el(k,'rect',{x:-w/2,y:-26,width:w,height:52,rx:8,fill:'#6d7378',stroke:'#fff','stroke-width':7});for(let i=0;i<w/52;i++)el(k,'path',{d:`M${-w/2+i*52} 24 L${-w/2+i*52+26} -24 L${-w/2+i*52+52} 24`,fill:'none',stroke:'#2d3236','stroke-width':5});return k};
// ===== v2: màu có nghĩa (đỏ = sai/thiếu/nguy hiểm, vàng đồng = đúng/có, xanh thép = nền/mốc đầu, kem = trung tính) và chuyển động theo lời
const CRED='#d8372d',CGOLD='#e0a63c',CSTEEL='#7fa6c4';
const strip2=(txt,kind,size=44,seed=2)=>{const cv=document.createElement('canvas').getContext('2d');cv.font=`900 ${size}px Inter`;const w=cv.measureText(txt).width+64,h=size+34;const g=mk();const s=el(g,'g',{filter:'url(#sh)'});el(s,'polygon',{points:jag(w,h,seed,4),fill:kind=='bad'?CRED:kind=='ok'?CGOLD:'#efe9d8'});const t=T(g,0,size*.36,txt,size,kind=='bad'?'#fff':'#17120c',0,'middle','none');t.setAttribute('stroke','none');return{g,w,h,at:(x,y,rot=0,sc=1,op=1)=>{g.setAttribute('transform',`translate(${x},${y}) rotate(${rot}) scale(${sc})`);g.setAttribute('opacity',op)}}};
const CK=(g,col=CGOLD)=>{const k=el(g,'g',{});const d='M-60 5 L-20 50 L65 -55';el(k,'path',{d,fill:'none',stroke:'#fff','stroke-width':34,'stroke-linecap':'round','stroke-linejoin':'round'});el(k,'path',{d,fill:'none',stroke:col,'stroke-width':20,'stroke-linecap':'round','stroke-linejoin':'round'});return k};
const shw=(s,t,x,y,rot,k)=>sh(s,t,x,y+Math.sin(t*1.9+x*.01)*4,rot+Math.sin(t*1.3+y*.01)*.8,k);
// ảnh + dải chữ + zoom tới đúng chỗ đang nói + vòng khoanh chạy tới + dấu ✗/✓. F={fx,fy,z,w:[từ,dự phòng],r,mark:'x'|'ok',m:[từ,dự phòng]}
const PH=(n,bg,key,mw,mh,lab,items,yr,F)=>S2(n,n,bg,yr?(t=>yr):null,g=>{const c=card(key,IMG+key+'.jpg',mw,mh,n*10+1);const L=lab?strip2(lab,'base',lab.length>34?22:26,n*10+2):null;const S=items.map((it,i)=>strip2(it[0],it[1],it[2],n*10+3+i));
 const rad=F&&F.r||130,col=F&&F.mark=='x'?CRED:CGOLD;const rg=F?el(c.top,'g',{}):null,rr=F?ring(rg,0,0,rad,col):null;const mkk=F&&F.mark?(F.mark=='x'?XX(c.top):CK(c.top)):null;
 return{upd:t=>{const e=inn(t,R(n)-.2,.6),rt=inn(t,R(n),E(n)-R(n));c.at(540,630,(n%2?-2:2)+Math.sin(t*1.1)*.5,1,e);
  if(!F)c.zoom(1+.1*rt,.5,.5);
  else{const tz=AT(n,F.w[0],F.w[1]),q=inn(t,tz,.9),ox=.5+(F.fx-.5)*q,oy=.5+(F.fy-.5)*q,s=1+.05*rt+(F.z-1)*q+.08*inn(t,tz+.9,Math.max(1,E(n)-tz));c.zoom(s,ox,oy);
   const px=-c.w/2+F.fx*c.w,py=-c.h/2+F.fy*c.h,qx=-c.w/2+ox*c.w,qy=-c.h/2+oy*c.h,X=qx+s*(px-qx),Y=qy+s*(py-qy);
   rg.setAttribute('transform',`translate(${X.toFixed(1)},${Y.toFixed(1)})`);rr.set(inn(t,tz+.35,.7));
   if(mkk){const tm=AT(n,F.m[0],F.m[1]);PUT(mkk,X+rad*.95,Y-rad*.8,popv(t,tm,.5),.5,0)}}
  if(L)shw(L,t,540,338,-1,e);items.forEach((it,i)=>shw(S[i],t,540,1085+i*110,(i%2?1:-1),PV(t,n,it[3],it[4])))}}});

// ===== Bộ vẽ phẳng dùng chung cho bản viết lại #16–#19
const SHEET=(g,w,h,seed)=>{const k=el(g,'g',{});el(k,'rect',{x:-w/2,y:-h/2,width:w,height:h,rx:10,fill:'#efe6cf',stroke:'#17120c','stroke-width':7});const r=rng(seed);for(let i=0;i<Math.floor(h/46)-1;i++)el(k,'line',{x1:-w/2+40,y1:-h/2+50+i*46,x2:w/2-40-r()*130,y2:-h/2+50+i*46,stroke:'rgba(60,50,40,.35)','stroke-width':5,'stroke-linecap':'round'});return k};
const TOWER=(g,col='#7a6652',sw=7)=>{const k=el(g,'g',{});el(k,'path',{d:'M-90 260 L-14 -250 L14 -250 L90 260 Z',fill:col,stroke:'#17120c','stroke-width':sw,'stroke-linejoin':'round'});for(let i=0;i<5;i++){const y=-160+i*85,w=14+i*17;el(k,'path',{d:`M${-w} ${y} L${w} ${y+45} M${w} ${y} L${-w} ${y+45}`,stroke:'#17120c','stroke-width':4})}el(k,'rect',{x:-6,y:-310,width:12,height:60,fill:'#17120c'});return k};
const WV=(g,col,n=3)=>[...Array(n)].map(()=>el(g,'circle',{fill:'none',stroke:col,'stroke-width':7,r:1,opacity:0}));
const WVU=(ws,t,R0,cx,cy,sp=.5,on=1)=>ws.forEach((e,i)=>{const u=((t*sp+i/ws.length)%1);e.setAttribute('cx',cx);e.setAttribute('cy',cy);e.setAttribute('r',10+u*R0);e.setAttribute('opacity',(1-u)*.85*on)});
const BIG=(g,txt,size,fill='#fff',stroke='#17120c')=>{const k=el(g,'g',{});const a=T(k,0,size*.36,txt,size,fill,stroke?14:0,'middle',stroke||'none');a.setAttribute('font-weight',900);return {k,set:s=>{a.textContent=s}}};
const POLEFLAG=(g,col='#da251d')=>{const k=el(g,'g',{});el(k,'rect',{x:-8,y:-300,width:16,height:600,fill:'#b9b2a4',stroke:'#17120c','stroke-width':6});const f=el(k,'path',{d:'M8 -296 L240 -296 L240 -150 L8 -150Z',fill:col,stroke:'#17120c','stroke-width':6});return{k,f}};
const PEOPLE=(g,n,col,seed)=>{const k=el(g,'g',{});const r=rng(seed);for(let i=0;i<n;i++){const x=(i-(n-1)/2)*70,h=70+r()*18;el(k,'circle',{cx:x,cy:-h-18,r:17,fill:col,stroke:'#17120c','stroke-width':4});el(k,'rect',{x:x-17,y:-h,width:34,height:h,rx:12,fill:col,stroke:'#17120c','stroke-width':4})}return k};
const FIG=(g,cols)=>{const k=el(g,'g',{});el(k,'rect',{x:-70,y:-20,width:140,height:260,rx:30,fill:cols[1],stroke:'#17120c','stroke-width':7});el(k,'circle',{cx:0,cy:-95,r:62,fill:cols[0],stroke:'#17120c','stroke-width':7});el(k,'rect',{x:-90,y:60,width:180,height:50,rx:12,fill:cols[2],stroke:'#17120c','stroke-width':6});return k};
const PUZ=(g,seed,n)=>{const k=el(g,'g',{});const r=rng(seed);for(let i=0;i<n;i++){const x=(r()-.5)*640,y=(r()-.3)*200,a=r()*360;el(k,'polygon',{points:'-34,-8 20,-24 38,12 -10,26',fill:i%2?'#a8643f':'#8a4a2a',stroke:'#17120c','stroke-width':5,transform:`translate(${x},${y}) rotate(${a})`})}return k};
const PHONE=(g)=>{const k=el(g,'g',{});el(k,'rect',{x:-90,y:-170,width:180,height:340,rx:34,fill:'#2b2f36',stroke:'#fff','stroke-width':8});el(k,'rect',{x:-72,y:-140,width:144,height:250,rx:10,fill:'#9fd0e8'});el(k,'circle',{cx:0,cy:140,r:16,fill:'#fff'});return k};
const PAG=(g,top=true,tilt=0)=>{const k=el(g,'g',{});const pil=el(k,'g',{transform:`rotate(${tilt})`});el(pil,'rect',{x:-34,y:-20,width:68,height:300,fill:'#b9b2a4',stroke:'#17120c','stroke-width':7});const up=el(pil,'g',{});if(top){el(up,'rect',{x:-130,y:-120,width:260,height:100,fill:'#5a3a24',stroke:'#17120c','stroke-width':7});el(up,'path',{d:'M-190 -118 Q-120 -150 0 -230 Q120 -150 190 -118 Q100 -126 0 -190 Q-100 -126 -190 -118Z',fill:'#8a4a2a',stroke:'#17120c','stroke-width':7,'stroke-linejoin':'round'});for(let i=0;i<4;i++)el(up,'rect',{x:-96+i*60,y:-104,width:20,height:70,fill:'#17120c'})}return{k,up,pil}};
const POND=(g,w=860)=>{const k=el(g,'g',{});el(k,'rect',{x:-w/2,y:280,width:w,height:150,rx:20,fill:'#2f6d6a',stroke:'#fff','stroke-width':8});for(let i=0;i<3;i++)el(k,'ellipse',{cx:-250+i*250,cy:350,rx:60,ry:14,fill:'none',stroke:'rgba(255,255,255,.4)','stroke-width':4});return k};
PH(1,'d','mc1',940,700,'CHÙA MỘT CỘT · HÀ NỘI',[['TỪNG BỊ NỔ TUNG','bad',40,'nổ',2.2],['CHÙA HÔM NAY DỰNG LẠI TỪ ẢNH CŨ','base',26,'dựng',5.0]],null,{fx:.44,fy:.3,z:1.9,w:['nổ',2.2],r:200,mark:'x',m:['nổ',2.8]});
sx(AT(1,'nổ',2.2),'blast',{g:.7});
S2(2,2,'p',null,g=>{const P=PAG(g,true,0);const pd=POND(g);const sol=PEOPLE(g,4,'#5a6a4a',22);const dy=el(g,'g',{});el(dy,'rect',{x:-30,y:-14,width:60,height:28,rx:6,fill:CRED,stroke:'#fff','stroke-width':5});el(dy,'path',{d:'M0 -14 q10 -30 28 -34',stroke:CGOLD,'stroke-width':5,fill:'none'});const A=strip2('QUÂN PHÁP CHUẨN BỊ RÚT KHỎI MIỀN BẮC','base',24,21),B=strip2('KẺ LẠ MẶT ĐẶT THUỐC NỔ','bad',36,22);
 return{upd:t=>{const e=popv(t,R(2)+.1,.6);PUT(pd,540,640,e,1,0);PUT(P.k,540,720,e,1.25,0);const u=inn(t,R(2)+.4,3.2);PUT(sol,1000-u*700,1060,e,.9,0);PUT(dy,540,990,popv(t,AT(2,'đặt',4.4),.5),1.2,Math.sin(t*10)*3);shw(A,t,540,1130,-1,PV(t,2,'Khi',.2));shw(B,t,540,1235,1,PV(t,2,'đặt',4.4))}}});
sx(R(2)+.4,'steps',{n:6,dt:.45,g:.5});sx(AT(2,'đặt',4.4),'dig',{g:.5});
S2(3,3,'d',t=>'9/1954',g=>{const P=PAG(g,true,0);const pd=POND(g);const bs=el(g,'g',{});for(let i=0;i<12;i++){const a=i/12*Math.PI*2;el(bs,'path',{d:`M0 0 L${Math.cos(a-.12)*190} ${Math.sin(a-.12)*190} L${Math.cos(a)*(i%2?300:240)} ${Math.sin(a)*(i%2?300:240)} L${Math.cos(a+.12)*190} ${Math.sin(a+.12)*190}Z`,fill:i%2?CRED:CGOLD,stroke:'#fff','stroke-width':5})}const sm=[];for(let i=0;i<5;i++)sm.push(el(g,'circle',{r:60+i*14,fill:'rgba(70,60,55,.7)'}));const A=strip2('ĐẾN NAY KHÔNG RÕ KẺ ĐÓ LÀ AI','bad',28,31),B=strip2('CHẤT NỔ GIẤU DƯỚI BÁT NHANG','base',28,32);
 return{upd:t=>{const e=popv(t,R(3)+.1,.6);PUT(pd,540,640,e,1,0);const w=AT(3,'nổ',7.0),u=inn(t,w,.5);const sk=u>0&&u<1?Math.sin(t*60)*8:0;PUT(P.k,540+sk,720,e,1.25,0);const bu=popv(t,w+.1,.3);PUT(bs,540,640,bu*(1.2-inn(t,w+.1,.9)*.5),1.0,t*40);bs.setAttribute('opacity',Math.max(0,1-inn(t,w+.4,1.0)));sm.forEach((c,i)=>{const v=inn(t,w+.2+i*.1,2.4);c.setAttribute('transform',`translate(${540+(i-2)*60},${620-v*320})`);c.setAttribute('opacity',(1-v)*.8*(u>0?1:0))});P.up.setAttribute('opacity',1-inn(t,w,.3));shw(A,t,540,1130,-1,PV(t,3,'Đến',2.2));shw(B,t,540,1235,1,PV(t,3,'chất',6.2))}}});
sx(AT(3,'nổ',7.0),'blast',{g:.9});
PH(4,'p','mc6',940,640,'TƯỢNG QUAN ÂM TRONG CHÙA',[['TƯỢNG VẪN NGUYÊN CHỖ CŨ','ok',34,'nguyên',2.8],['CHỈ RỜI VÀI CÁNH TAY GỖ','base',32,'chỉ',5.0]],null,{fx:.55,fy:.35,z:1.6,w:['nguyên',2.8],r:180,mark:'ok',m:['nguyên',3.4]});
sx(AT(4,'chỉ',5.0),'thud',{g:.4});
PH(5,'d','mc9',940,640,'ẢNH CŨ: CHÙA MỘT CỘT (TONKIN HANOI)',[['ÔNG NGUYỄN BÁ LĂNG DỰNG LẠI CHÙA','ok',28,'ông',2.4],['DỰA TRÊN ẢNH CHỤP CUỐI THẾ KỶ 19','base',28,'dựa',7.0]],null,{fx:.5,fy:.4,z:1.6,w:['dựa',7.0],r:200,mark:'ok',m:['họa',6.0]});
sx(AT(5,'ông',2.4),'paper',{g:.6});
PH(6,'p','mc8',940,700,'CHÙA MỘT CỘT SAU KHI DỰNG LẠI',[['CỘT ĐÁ ĐƯỢC GIỮ NGUYÊN','ok',34,'cột',4.0],['PHẦN TRÊN LÀM MỚI','base',36,'phần',6.0]],null,{fx:.5,fy:.55,z:1.6,w:['cột',4.0],r:200,mark:'ok',m:['giữ',4.8]});
sx(AT(6,'phần',6.0),'hammer',{g:.5});sx(AT(6,'phần',6.0)+.6,'hammer',{g:.4});
S2(7,7,'d',null,g=>{const pil=el(g,'g',{});el(pil,'rect',{x:-60,y:-20,width:120,height:150,fill:'#b9b2a4',stroke:'#17120c','stroke-width':7});el(pil,'rect',{x:-60,y:-170,width:120,height:150,fill:'#a8a090',stroke:'#17120c','stroke-width':7});el(pil,'line',{x1:-60,y1:-20,x2:60,y2:-20,stroke:'#17120c','stroke-width':9});const d1=el(g,'g',{});el(d1,'line',{x1:-130,y1:0,x2:-130,y2:260,stroke:CGOLD,'stroke-width':8});T(d1,-210,140,'4 m',48,CGOLD,0,'middle','none');const d2=el(g,'g',{});el(d2,'line',{x1:-60,y1:-210,x2:60,y2:-210,stroke:CRED,'stroke-width':8});T(d2,0,-240,'1,2 m',48,CRED,0,'middle','none');const A=strip2('TRỤ ĐÁ GỒM HAI KHỐI GHÉP LIỀN','base',28,71),B=strip2('ĐƯỜNG KÍNH 1,2 M · CAO 4 M','ok',32,72);
 return{upd:t=>{const e=popv(t,R(7)+.1,.6);PUT(pil,540,720,e,1.5,0);PUT(d2,540,720,popv(t,AT(7,'đường',3.6),.5),1.5,0);PUT(d1,540,720,popv(t,AT(7,'cao',5.4),.5),1.5,0);shw(A,t,540,1130,-1,PV(t,7,'Trụ',.2));shw(B,t,540,1235,1,PV(t,7,'đường',3.6))}}});
sx(AT(7,'đường',3.6),'tit',{f:1400,g:.5});sx(AT(7,'cao',5.4),'tit',{f:1100,g:.5});
PH(8,'p','mc7',560,900,'TƯỢNG VUA LÝ THÁI TÔNG TRONG CHÙA',[['THEO TOÀN THƯ: VUA NẰM MỘNG','base',28,'Theo',3.4],['THẤY PHẬT QUAN ÂM TRÊN TÒA SEN','ok',28,'thấy',6.6]],null,{fx:.4,fy:.22,z:1.9,w:['thấy',6.6],r:150,mark:'ok',m:['sen',8.0]});
sx(AT(8,'thấy',6.6),'chime',{g:.5});
PH(9,'d','mc2',940,700,'CỘT ĐÁ GIỮA AO VUÔNG',[['DỰNG CHÙA TRÊN MỘT CỘT ĐÁ GIỮA AO','ok',26,'dựng',.6],['THEO HÌNH TÒA SEN ẤY','base',34,'theo',3.6]],'1049',{fx:.47,fy:.82,z:1.9,w:['cột',3.0],r:170,mark:'ok',m:['sen',4.4]});
sx(AT(9,'cột',3.0),'stamp',{g:.6});
PH(10,'p','mc3',940,640,'BƯU THIẾP CŨ: CHÙA MỘT CỘT',[['HOCQUARD MÔ TẢ NĂM 1884','base',32,'một',3.0],['NHÀ DỰNG TRÊN CỘT ĐÁ GIỮA AO BÈO VÀ SEN','ok',24,'cột',5.4]],'1884',{fx:.4,fy:.5,z:1.7,w:['cột',5.4],r:200});
PH(11,'d','mc5',640,900,'TRỤ ĐÁ DƯỚI CHÙA',[['CỘT ĐÁ CÒN ĐỨNG','ok',38,'cột',.6],['CỦA NGHÌN NĂM TRƯỚC? CÁC NGUỒN KHÔNG NÓI CHẮC','bad',22,'các',4.6]],null,{fx:.5,fy:.58,z:1.9,w:['các',4.6],r:160,mark:'x',m:['chắc',7.0]});
PH(12,'p','mc4',940,640,'BƯU THIẾP CŨ: PAGODE MONTÉE SUR UN PILIER',[['TỪ CỘT ĐÁ ĐẾN MÁI NGÓI','base',34,'từ',1.6],['PHẦN NÀO CÒN LÀ CỦA NGÀY XƯA?','bad',30,'phần',4.4]],null,{fx:.55,fy:.45,z:1.7,w:['phần',4.4],r:200},TOTAL);
sx(R(12)+.3,'wind',{d:2.2,g:.4});

sx(R(1)+.1,'whoosh',{d:.5,g:.5});
for(let i=1;i<=12;i++)bm(R(i)+.3,i%3!=1);
sx(R(12)+.3,'question',{g:.7});
