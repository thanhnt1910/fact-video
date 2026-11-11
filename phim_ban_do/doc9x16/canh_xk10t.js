// ===== Mona Lisa (xk10t). Ảnh: ml1(1) ml2(2) ml3(3) ml5(5) ml7(7) ml10(10) ml11(11) ml12(12) ml13(13). Cảnh 4,6,8,9,14 vẽ phẳng.
// ===== Dấu ấn riêng: nền nhung đỏ thẫm bảo tàng + khung vàng; bốn móc treo tranh trống ở đáy (y>1640), một sợi dây đung đưa
{DR1.setAttribute('opacity',0);DR2.setAttribute('opacity',0);
 DARKG.firstChild.setAttribute('fill','#1c0e12');
 [...PAPG.children].forEach(c=>{if(c.tagName=='g')c.setAttribute('opacity',0);if(c.tagName=='line')c.setAttribute('stroke','rgba(120,70,40,.14)')});
 PAPG.firstChild.setAttribute('fill','#e8dcc2');
 const hk=(p,col,cord)=>{const g=el(p,'g',{});const cs=[];[150,390,690,930].forEach((x,i)=>{el(g,'circle',{cx:x,cy:1650,r:9,fill:col});const c=el(g,'path',{d:`M${x} 1650 L${x} 1720`,stroke:cord,'stroke-width':4,'stroke-linecap':'round'});cs.push([c,x]);el(g,'rect',{x:x-34,y:1720,width:68,height:8,rx:3,fill:col})});return cs};
 const a=hk(DARKG,'#c9962f','#7a5a2a'),b=hk(PAPG,'#a8741a','#6b4a1a');
 for(const [p,col] of [[DARKG,'rgba(201,150,47,.07)'],[PAPG,'rgba(168,116,26,.08)']]){const g=el(p,'g',{});for(let i=0;i<4;i++)el(g,'rect',{x:30+i*3,y:30+i*3,width:1020-i*6,height:1860-i*6,rx:10,fill:'none',stroke:col,'stroke-width':6})}
 window.THEME_UPD=t=>{[a,b].forEach(cs=>cs.forEach(([c,x],i)=>{const s=Math.sin(t*1.3+i*1.7)*(i==2?9:2.5);c.setAttribute('d',`M${x} 1650 L${x+s} 1720`)}));PTU(t)};
}
// ===== Người que cầm đèn dầu (linh vật thử nghiệm): vài lần xuất hiện, không che chữ
const MAS=(g)=>{const k=el(g,'g',{});const ln=(d,w,c)=>{el(k,'path',{d,stroke:'#fff','stroke-width':w+10,'stroke-linecap':'round','stroke-linejoin':'round',fill:'none'});el(k,'path',{d,stroke:c,'stroke-width':w,'stroke-linecap':'round','stroke-linejoin':'round',fill:'none'})};
 ln('M0 -90 L0 -10',12,'#17120c');ln('M0 -10 L-26 70 M0 -10 L26 70',12,'#17120c');ln('M0 -78 L-34 -30',12,'#17120c');ln('M0 -78 L56 -56',12,'#17120c');
 const lg=el(k,'g',{transform:'translate(60,-52)'});const gl=el(lg,'circle',{r:84,fill:'rgba(255,205,90,.30)'});const gl2=el(lg,'circle',{r:48,fill:'rgba(255,215,110,.40)'});
 el(lg,'path',{d:'M0 -6 L0 -26',stroke:'#17120c','stroke-width':5});el(lg,'path',{d:'M-18 8 Q0 24 18 8 Z',fill:'#b07a2a',stroke:'#17120c','stroke-width':5,'stroke-linejoin':'round'});const fl=el(lg,'path',{d:'M0 -4 Q-9 -14 0 -30 Q9 -14 0 -4Z',fill:'#ffd25a',stroke:'#e8892a','stroke-width':3});
 el(k,'circle',{cx:0,cy:-118,r:33,fill:'#fff'});el(k,'circle',{cx:0,cy:-118,r:26,fill:'#f5efe0',stroke:'#17120c','stroke-width':7});el(k,'circle',{cx:-9,cy:-122,r:3.5,fill:'#17120c'});el(k,'circle',{cx:9,cy:-122,r:3.5,fill:'#17120c'});el(k,'path',{d:'M-8 -108 Q0 -101 8 -108',stroke:'#17120c','stroke-width':3.5,fill:'none','stroke-linecap':'round'});
 return{k,at:(x,y,s=1,rot=0,op=1,t=0,fx=1)=>{k.setAttribute('transform',`translate(${x},${y}) rotate(${rot+Math.sin(t*2.4)*2}) scale(${s*fx},${s})`);k.setAttribute('opacity',op);const f=1+.12*Math.sin(t*11);gl.setAttribute('r',84*f);gl2.setAttribute('r',48*f);fl.setAttribute('transform',`scale(${1+.15*Math.sin(t*13)},${1+.2*Math.sin(t*9)})`)}}};
// ===== Lật trang sách mở đầu (khoảng 1 giây), phủ trên cùng, chữ gợi hook hiện ngay phía sau
const PTG=el(S,'g',{opacity:0}),PTB=el(PTG,'g',{});
el(PTB,'rect',{x:-100,y:-10,width:1280,height:1940,fill:'#efe6cf'});el(PTB,'rect',{x:50,y:60,width:980,height:1800,rx:14,fill:'none',stroke:'#a8741a','stroke-width':8});
for(let i=0;i<9;i++)el(PTB,'line',{x1:150,y1:1250+i*54,x2:930-((i*97)%210),y2:1250+i*54,stroke:'rgba(60,50,40,.28)','stroke-width':5,'stroke-linecap':'round'});
{const a=T(PTB,540,700,'BÍ MẬT BIỂU TƯỢNG',92,'#17120c',0,'middle','none');a.setAttribute('font-weight',900);a.setAttribute('stroke','none');const b=T(PTB,540,860,'MONA LISA',120,'#a8741a',0,'middle','none');b.setAttribute('font-weight',900);b.setAttribute('stroke','none');
 const m=el(PTB,'g',{transform:'translate(540,1090) scale(1.7)'});el(m,'path',{d:'M-18 8 Q0 24 18 8 Z',fill:'#b07a2a',stroke:'#17120c','stroke-width':5});el(m,'path',{d:'M0 -4 Q-9 -14 0 -30 Q9 -14 0 -4Z',fill:'#ffd25a',stroke:'#e8892a','stroke-width':3})}
const PTS=el(PTG,'rect',{x:1080,y:0,width:60,height:1920,fill:'rgba(0,0,0,.35)'});let PTA=false;
const PTU=t=>{if(!PTA){S.appendChild(PTG);PTA=true}const u=cl((t-.55)/.65);if(t>1.3||t<0){PTG.setAttribute('opacity',0);return}PTG.setAttribute('opacity',1);const sx_=1-ease(u);PTB.setAttribute('transform',`scale(${Math.max(.001,sx_).toFixed(3)},1)`);PTS.setAttribute('x',(1080*sx_).toFixed(1));PTS.setAttribute('opacity',u>0&&u<1?.6:0)};
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
  if(L)shw(L,t,540,mh>600?1000:338,-1,e);items.forEach((it,i)=>shw(S[i],t,540,1085+i*110,(i%2?1:-1),PV(t,n,it[3],it[4])))}}});


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
const FR=(g,w,h,hang)=>{const k=el(g,'g',{});if(hang){el(k,'path',{d:`M${-w*.28} ${-h/2-90} L0 ${-h/2-10} L${w*.28} ${-h/2-90}`,fill:'none',stroke:'#7a5a2a','stroke-width':6,'stroke-linejoin':'round'})}
 el(k,'rect',{x:-w/2,y:-h/2,width:w,height:h,rx:10,fill:'#c9962f',stroke:'#fff','stroke-width':8});el(k,'rect',{x:-w/2+30,y:-h/2+30,width:w-60,height:h-60,rx:4,fill:'#2a1a16',stroke:'#17120c','stroke-width':6});el(k,'rect',{x:-w/2+12,y:-h/2+12,width:w-24,height:h-24,rx:6,fill:'none',stroke:'#f2d27a','stroke-width':4});return k};
// 1: hook (Mona Lisa, zoom vào gương mặt, ✗ lên "chỗ trống")
PH(1,'d','ml1',640,700,'MONA LISA · LOUVRE',[['BỊ TRỘM NĂM 1911','bad',44,'bị',1.3],['NGƯỜI ĐẾN NGẮM CHỖ TRỐNG','base',32,'chỉ',4.8]],null,{fx:.45,fy:.28,z:1.9,w:['bị',1.3],r:170,mark:'x',m:['trống',6.6]});
// 2: trước vụ trộm (trần phòng Salon Carré, ảnh minh họa)
PH(2,'p','ml2',940,600,'PHÒNG SALON CARRÉ (ẢNH MINH HỌA)',[['TRƯỚC VỤ TRỘM','base',46,'Vì',.2],['CHƯA PHẢI BỨC ĐƯỢC TÌM XEM NHIỀU NHẤT','bad',24,'chưa',3.6]],null,{fx:.5,fy:.4,z:1.6,w:['bảo',4.8],r:200});
// 3: báo Ý vẽ cảnh lấy tranh
PH(3,'d','ml3',640,700,'BÁO Ý NĂM 1911: TRANH RỜI TƯỜNG',[['THỨ HAI 21/8/1911','base',40,'sáng',2.2],['LOUVRE ĐÓNG CỬA, CÓ NGƯỜI LẤY TRANH','bad',26,'khi',9.0]],'1911',{fx:.5,fy:.42,z:1.8,w:['lấy',11.0],r:190,mark:'x',m:['tường',13.0]});
// 4: khung trống, người que soi đèn tìm
S2(4,4,'d',null,g=>{const f=FR(g,480,600,true);const q=T(g,0,0,'?',300,'#e5483f',16,'middle',DK);const m=MAS(g);const A=strip2('MÃI ĐẾN TRƯA HÔM SAU','bad',38,41),B=strip2('KHUNG KÍNH BỊ BỎ Ở CẦU THANG','base',26,42);
 return{upd:t=>{const e=popv(t,R(4)+.1,.6);PUT(f,540,700+Math.sin(t*1.4)*5,e,1,-2+Math.sin(t*1.1));const qp=popv(t,AT(4,'không',9.0),.5);q.setAttribute('transform',`translate(540,700) rotate(-8) scale(${Math.max(.001,qp)})`);q.setAttribute('opacity',qp>0?1:0);const u=inn(t,AT(4,'một',3.2),1.6);m.at(120+u*180,1010,.8,0,popv(t,AT(4,'một',3.2),.5),t);shw(A,t,540,1130,-1,PV(t,4,'mãi',.1));shw(B,t,540,1240,1,PV(t,4,'Chiếc',9.6))}}});
// 5: báo Excelsior
PH(5,'p','ml5',640,700,'BÁO EXCELSIOR, PARIS',[['BÁO CHÍ ĐĂNG TIN LỚN','ok',38,'báo',4.6],['THÔNG BÁO TRUY TÌM KHẮP NƠI','base',30,'thông',7.0]],null,{fx:.5,fy:.08,z:1.9,w:['báo',4.6],r:210,mark:'ok',m:['lớn',6.8]});
// 6: tường trống, hàng nghìn người đến xem
S2(6,6,'d',null,g=>{const f=FR(g,300,400,true);const q=T(g,0,0,'?',200,'#e5483f',14,'middle',DK);const P=[0,1,2].map(i=>PEOPLE(g,i==1?9:8,['#3a5a7a','#7a3a3a','#4a6a4a'][i],60+i));const n=bigNum(g,'0',130,CGOLD);const A=strip2('LOUVRE MỞ LẠI','base',44,61),B=strip2('NGƯỜI XEM CHỖ TRỐNG','bad',36,62);
 return{upd:t=>{const e=popv(t,R(6)+.1,.6);PUT(f,540,590+Math.sin(t*1.3)*4,e,1,-1);const qp=popv(t,R(6)+.8,.5);q.setAttribute('transform',`translate(540,590) rotate(-8) scale(${Math.max(.001,qp)})`);q.setAttribute('opacity',qp>0?1:0);
  P.forEach((p,i)=>{const w=AT(6,['Hàng','đứng','trước'][i],[1.8,3.2,4.4][i]);const u=popv(t,w,.6);PUT(p,540,850+i*80+Math.sin(t*3+i)*3,u,1.0,0)});
  const w=AT(6,'Hàng',1.8),u=inn(t,w,2.6);n.textContent=String(Math.round(2000*u)).replace(/\B(?=(\d{3})+(?!\d))/g,'.')+'+';PUT(n,540,1075,popv(t,w,.5),.9,-2);shw(A,t,300,1230,-2,PV(t,6,'Louvre',.1));shw(B,t,700,1330,2,PV(t,6,'khoảng',5.6))}}});
// 7: Peruggia
PH(7,'d','ml7',900,700,'VINCENZO PERUGGIA · HỒ SƠ CẢNH SÁT PARIS',[['THỢ NGƯỜI Ý TỪNG LÀM Ở LOUVRE','base',26,'một',3.0],['GIẤU TRANH HƠN HAI NĂM','bad',38,'giấu',6.8]],null,{fx:.74,fy:.42,z:1.9,w:['Peruggia',2.0],r:150,mark:'x',m:['hai',7.4]});
// 8: hai năm giấu tranh (trục thời gian, người que soi đèn)
S2(8,8,'p',t=>'1911',g=>{const ln=el(g,'path',{d:'M180 640 L900 640',stroke:'#17120c','stroke-width':14,'stroke-linecap':'round',pathLength:1,'stroke-dasharray':1,'stroke-dashoffset':1});const d1=el(g,'circle',{r:34,fill:CSTEEL,stroke:'#fff','stroke-width':8}),d2=el(g,'circle',{r:34,fill:CRED,stroke:'#fff','stroke-width':8});const b1=bigNum(g,'1911',110,CSTEEL),b2=bigNum(g,'1913',110,CRED);const f=FR(g,120,150,false);const m=MAS(g);const A=strip2('CẢNH SÁT HỎI CUNG ÔNG','base',34,81),B=strip2('NHƯNG KHÔNG COI LÀ NGHI PHẠM','bad',28,82);
 return{upd:t=>{const w1=R(8)+.2,w2=AT(8,'cuối',6.4),v=inn(t,w1,w2-w1+.4);ln.setAttribute('stroke-dashoffset',1-v);PUT(d1,180,640,popv(t,w1,.5));PUT(d2,900,640,popv(t,w2,.5));PUT(b1,200,500,popv(t,w1,.5),1,-4);PUT(b2,880,500,popv(t,w2,.5),1,4);PUT(f,180+720*v,820+Math.sin(t*3)*6,popv(t,w1+.2,.5),1,0);m.at(260+Math.sin(t*.8)*20,1010,.7,0,popv(t,AT(8,'Cảnh',.4),.5),t);shw(A,t,540,1140,-1,PV(t,8,'Cảnh',.2));shw(B,t,540,1245,1,PV(t,8,'nhưng',2.8))}}});
// 9: thư ký tên giả Leonard (vẽ phẳng)
S2(9,9,'d',null,g=>{const k=el(g,'g',{});const sh=SHEET(k,560,520,9);const tt=T(k,0,-180,'THƯ GỬI FLORENCE',40,'#17120c',0,'middle','none');tt.setAttribute('stroke','none');const sg=SIG(k,'#1d3f78',9);const nm=T(k,0,150,'LEONARD',52,'#a8741a',0,'middle','none');nm.setAttribute('stroke','none');nm.setAttribute('font-style','italic');const x=XX(g,'#d8372d');const A=strip2('THƯ GỬI NGƯỜI BUÔN TRANH','base',34,91),B=strip2('KÝ TÊN GIẢ: LEONARD','bad',40,92);
 return{upd:t=>{const e=popv(t,R(9)+.1,.6);PUT(k,540,620+Math.sin(t*1.5)*6,e,1.05,-2+Math.sin(t*1.2)*.8);const a=inn(t,R(9)+.8,.8);sg.setAttribute('transform','translate(-40,40) scale(.6)');sg.setAttribute('opacity',a);const nn=popv(t,AT(9,'ký',5.4),.5);nm.setAttribute('opacity',nn>0?1:0);PUT(x,720,860,popv(t,AT(9,'giả',6.2),.5),.8,0);shw(A,t,540,1085,-1,PV(t,9,'viết',1.3));shw(B,t,540,1195,1,PV(t,9,'ký',5.4))}}});
// 10: bị bắt
PH(10,'p','ml10',700,700,'PERUGGIA SAU KHI BỊ BẮT',[['GẶP Ở KHÁCH SẠN','base',40,'gặp',.3],['NGƯỜI BUÔN TRANH BÁO CẢNH SÁT','ok',26,'rồi',5.2]],null,{fx:.5,fy:.42,z:1.7,w:['bị',8.0],r:190,mark:'ok',m:['bắt',8.6]});
// 11: tranh trở về Louvre
PH(11,'d','ml11',940,560,'TRANH TRỞ VỀ LOUVRE, THÁNG 1/1914',[['MONA LISA VỀ LẠI LOUVRE','ok',36,'Mona',1.4],['SAU KHI TRƯNG BÀY Ở VÀI THÀNH PHỐ Ý','base',24,'sau',5.0]],'1914',{fx:.45,fy:.45,z:1.8,w:['trở',2.4],r:170,mark:'ok',m:['Louvre',3.4]});
// 12: hơn 100.000 người trong hai ngày đầu
S2(12,12,'p',t=>'1914',g=>{const c=card('ml12',IMG+'ml12.jpg',940,670,121);const n=bigNum(g,'0',150,CGOLD);const L=strip2('HAI NGÀY ĐẦU','base',40,122),B=strip2('NGƯỜI ĐẾN XEM','ok',34,123);
 return{upd:t=>{const e=inn(t,R(12)-.2,.6);c.at(540,500,-2+Math.sin(t*1.1)*.5,1,e);c.zoom(1+.1*inn(t,R(12),E(12)-R(12)),.5,.5);const w=AT(12,'hơn',1.8),u=inn(t,w,1.4);n.textContent=String(Math.round(100000*u)).replace(/\B(?=(\d{3})+(?!\d))/g,'.')+'+';PUT(n,540,1040,popv(t,w,.5),1,-2);shw(L,t,540,895,-1,e);shw(B,t,540,1200,1,PV(t,12,'đã',3.2))}}});
// 13: bưu thiếp Mona Lisa sau 1911
PH(13,'d','ml13',620,700,'BƯU THIẾP MONA LISA SAU VỤ TRỘM 1911',[['SỬ GIA VẪN DÈ DẶT','bad',40,'các',.3],['CHỈ VỤ TRỘM ĐÃ LÀM NÊN DANH TIẾNG?','base',24,'chỉ',4.0]],null,{fx:.3,fy:.6,z:1.8,w:['dè',2.0],r:180,mark:'x',m:['chỉ',4.6]});
// 14: câu hỏi cuối: vẻ đẹp hay câu chuyện
S2(14,14,'p',null,g=>{const f1=FR(g,330,440,false),f2=FR(g,330,440,false);const q=T(g,0,0,'?',300,'#e5483f',16,'middle',DK);const m=MAS(g);const A=strip2('VẺ ĐẸP','ok',50,141),B=strip2('HAY CÂU CHUYỆN BIẾN MẤT?','bad',32,142);
 return{upd:t=>{PUT(f1,300,560+Math.sin(t*1.5)*6,popv(t,R(14)+.2,.6),1,-3);PUT(f2,780,560+Math.sin(t*1.5+2)*6,popv(t,AT(14,'hay',3.4),.6),1,3);const qp=popv(t,AT(14,'hay',3.4)+.5,.5);q.setAttribute('transform',`translate(540,640) rotate(${Math.sin(t*2)*6-6}) scale(${Math.max(.001,qp)})`);q.setAttribute('opacity',qp>0?1:0);m.at(540,1010,.8,0,popv(t,R(14)+.4,.5),t);shw(A,t,300,880,-2,PV(t,14,'vẻ',1.6));shw(B,t,700,1140,2,PV(t,14,'hay',3.4))}}},TOTAL);
sx(R(1)+.1,'whoosh',{d:.5,g:.5});
for(let i=1;i<=14;i++)bm(R(i)+.3,i%3!=1);
sx(R(14)+.3,'question',{g:.7});
