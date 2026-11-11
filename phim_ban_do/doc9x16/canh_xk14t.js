const VT2='D-DAY';
// ===== D-Day (xk14t). Ảnh: dd4(1) dd1(3) dd3(9) dd8(8) dd11(11) dd12(12). Cảnh 2,4,5,6,7,10 vẽ phẳng.
// ===== Dấu ấn riêng: nền bản đồ thời tiết xanh biển, vài đường đẳng áp trôi chậm ở đáy (y>1560)
{DR1.setAttribute('opacity',0);DR2.setAttribute('opacity',0);
 DARKG.firstChild.setAttribute('fill','#0e2230');
 [...PAPG.children].forEach(c=>{if(c.tagName=='g')c.setAttribute('opacity',0);if(c.tagName=='line')c.setAttribute('stroke','rgba(40,90,120,.13)')});
 PAPG.firstChild.setAttribute('fill','#dde8ec');
 const iso=(p,col)=>{const g=el(p,'g',{});return [[300,70,24],[420,110,32],[540,150,40],[660,190,48]].map(([rx,ry,sp],i)=>{const e=el(g,'ellipse',{rx,ry,fill:'none',stroke:col,'stroke-width':4,opacity:.55-i*.08});return[e,sp,i]})};
 const a=iso(DARKG,'rgba(130,190,225,.55)'),b=iso(PAPG,'rgba(60,110,140,.4)');
 for(const [p,col] of [[DARKG,'rgba(130,190,225,.08)'],[PAPG,'rgba(40,90,120,.1)']]){const g=el(p,'g',{});for(let i=0;i<4;i++)el(g,'rect',{x:30+i*3,y:30+i*3,width:1020-i*6,height:1860-i*6,rx:10,fill:'none',stroke:col,'stroke-width':6})}
 window.THEME_UPD=t=>{[a,b].forEach(cs=>cs.forEach(([e,sp,i])=>{e.setAttribute('cx',540+Math.sin(t*.22+i)*sp*2.2);e.setAttribute('cy',1740+Math.cos(t*.18+i*.7)*10)}));PTU(t)};
}
// ===== Người que cầm đèn dầu (linh vật thử nghiệm): vài lần xuất hiện, không che chữ
const MAS=(g)=>{const k=el(g,'g',{});const OL='#17120c',GD='#d9a84a';
 const lim=(w)=>{const a=el(k,'path',{d:'M0 0',stroke:'#fff','stroke-width':w+10,'stroke-linecap':'round','stroke-linejoin':'round',fill:'none'});const b=el(k,'path',{d:'M0 0',stroke:OL,'stroke-width':w,'stroke-linecap':'round','stroke-linejoin':'round',fill:'none'});return d=>{a.setAttribute('d',d);b.setAttribute('d',d)}};
 const body=lim(12),legs=lim(12),arm1=lim(12),arm2=lim(12);
 const lg=el(k,'g',{});const gl=el(lg,'circle',{cy:0,r:84,fill:'rgba(255,205,90,.28)'});const gl2=el(lg,'circle',{cy:0,r:48,fill:'rgba(255,215,110,.38)'});
 el(lg,'circle',{cx:0,cy:-56,r:9,fill:'none',stroke:'#fff','stroke-width':9});el(lg,'circle',{cx:0,cy:-56,r:9,fill:'none',stroke:GD,'stroke-width':4.5});
 el(lg,'path',{d:'M-20 -34 L-11 -48 L11 -48 L20 -34 Z',fill:GD,stroke:OL,'stroke-width':3.5,'stroke-linejoin':'round'});el(lg,'rect',{x:-22,y:-36,width:44,height:7,rx:2,fill:GD,stroke:OL,'stroke-width':3.5});
 el(lg,'rect',{x:-14,y:-29,width:28,height:56,fill:'#f2a23a',stroke:OL,'stroke-width':3.5});el(lg,'rect',{x:-9,y:-24,width:18,height:46,fill:'#ffcb6b'});el(lg,'path',{d:'M-14 -29 L-14 27 M14 -29 L14 27',stroke:GD,'stroke-width':5});
 const fl=el(lg,'path',{d:'M0 14 Q-9 2 0 -16 Q9 2 0 14Z',fill:'#fff2b8',stroke:'#e8892a','stroke-width':2.5});el(lg,'rect',{x:-1.5,y:12,width:3,height:10,fill:OL});
 el(lg,'rect',{x:-22,y:26,width:44,height:7,rx:2,fill:GD,stroke:OL,'stroke-width':3.5});
 const hd=el(k,'g',{});
 el(hd,'circle',{cx:0,cy:-118,r:36,fill:'#fff'});el(hd,'circle',{cx:0,cy:-118,r:30,fill:'#f5efe0',stroke:OL,'stroke-width':7});
 el(hd,'circle',{cx:-10,cy:-114,r:4.5,fill:OL});el(hd,'circle',{cx:10,cy:-114,r:4.5,fill:OL});el(hd,'path',{d:'M-9 -98 Q0 -90 9 -98',stroke:OL,'stroke-width':4.5,fill:'none','stroke-linecap':'round'});
 el(hd,'path',{d:'M-42 -140 L42 -140 L36 -162 Q0 -182 -36 -162Z',fill:'#6b4a2a',stroke:OL,'stroke-width':5,'stroke-linejoin':'round'});
 return{k,at:(x,y,s=1,rot=0,op=1,t=0,fx=1,walk=1)=>{k.setAttribute('transform',`translate(${x},${y}) rotate(${rot}) scale(${s*fx},${s})`);k.setAttribute('opacity',op);
  const w=Math.sin(t*6.5)*walk,bob=Math.abs(Math.cos(t*6.5))*4*walk,sw=Math.sin(t*6.5+Math.PI)*walk;
  body(`M0 ${-84-bob} L0 ${-10-bob}`);legs(`M0 ${-10-bob} L${-26*w-2} 70 M0 ${-10-bob} L${26*w+2} 70`);
  arm1(`M0 ${-70-bob} L${-30-14*sw} ${-20-bob}`);arm2(`M0 ${-70-bob} L58 ${-50-bob}`);
  hd.setAttribute('transform',`translate(0,${-bob})`);lg.setAttribute('transform',`translate(66,${-6-bob})`);
  const f=1+.12*Math.sin(t*11);gl.setAttribute('r',84*f);gl2.setAttribute('r',48*f);
  fl.setAttribute('transform',`translate(0,14) scale(${1+.12*Math.sin(t*13)},${1+.15*Math.sin(t*9)}) translate(0,-14)`)}}};
// ===== Lật trang sách mở đầu (khoảng 1 giây), phủ trên cùng, chữ gợi hook hiện ngay phía sau
const PTG=el(S,'g',{opacity:0}),PTB=el(PTG,'g',{});
el(PTB,'rect',{x:-100,y:-10,width:1280,height:1940,fill:'#efe6cf'});el(PTB,'rect',{x:50,y:60,width:980,height:1800,rx:14,fill:'none',stroke:'#a8741a','stroke-width':8});
for(let i=0;i<9;i++)el(PTB,'line',{x1:150,y1:1250+i*54,x2:930-((i*97)%210),y2:1250+i*54,stroke:'rgba(60,50,40,.28)','stroke-width':5,'stroke-linecap':'round'});
{const a=T(PTB,540,700,'BÍ MẬT BIỂU TƯỢNG',92,'#17120c',0,'middle','none');a.setAttribute('font-weight',900);a.setAttribute('stroke','none');const b=T(PTB,540,860,VT2,120,'#a8741a',0,'middle','none');b.setAttribute('font-weight',900);b.setAttribute('stroke','none');
 const m=el(PTB,'g',{transform:'translate(540,1120) scale(0.001)'});el(m,'circle',{cy:-56,r:9,fill:'none',stroke:'#d9a84a','stroke-width':4.5});el(m,'path',{d:'M-20 -34 L-11 -48 L11 -48 L20 -34 Z',fill:'#d9a84a',stroke:'#17120c','stroke-width':3.5});el(m,'rect',{x:-14,y:-29,width:28,height:56,fill:'#f2a23a',stroke:'#17120c','stroke-width':3.5});el(m,'rect',{x:-9,y:-24,width:18,height:46,fill:'#ffcb6b'});el(m,'path',{d:'M0 14 Q-9 2 0 -16 Q9 2 0 14Z',fill:'#fff2b8',stroke:'#e8892a','stroke-width':2.5});el(m,'rect',{x:-22,y:26,width:44,height:7,rx:2,fill:'#d9a84a',stroke:'#17120c','stroke-width':3.5})}
el(PTB,'image',{href:'../../assets/logo/nguoi-gac-su.png',x:872,y:100,width:128,height:128,opacity:.9});
const PM=MAS(PTB);
const LC=el(PTB,'clipPath',{id:'plens'}),LCc=el(LC,'circle',{r:150,cx:300,cy:700});
const LG=el(PTB,'g',{'clip-path':'url(#plens)'}),LIN=el(LG,'g',{});
el(LIN,'rect',{x:-100,y:300,width:1280,height:900,fill:'#efe6cf'});
{const a=T(LIN,540,700,'BÍ MẬT BIỂU TƯỢNG',92,'#17120c',0,'middle','none');a.setAttribute('font-weight',900);a.setAttribute('stroke','none');const b=T(LIN,540,860,VT2,120,'#a8741a',0,'middle','none');b.setAttribute('font-weight',900);b.setAttribute('stroke','none')}
const LR=el(PTB,'g',{});el(LR,'circle',{r:150,fill:'rgba(255,255,255,.12)',stroke:'#17120c','stroke-width':16});el(LR,'circle',{r:150,fill:'none',stroke:'#d9a84a','stroke-width':8});el(LR,'path',{d:'M-100 -100 Q-60 -130 -10 -125',stroke:'rgba(255,255,255,.7)','stroke-width':10,fill:'none','stroke-linecap':'round'});
const LH=el(LR,'path',{d:'M106 106 L250 250',stroke:'#17120c','stroke-width':34,'stroke-linecap':'round'});el(LR,'path',{d:'M106 106 L250 250',stroke:'#6b4a2a','stroke-width':20,'stroke-linecap':'round'});
const PMU=t=>{const wx=Math.min(1,Math.max(0,t/.9)),x=-140+wx*400,walk=wx<1?1:0;PM.at(x,1190,1.7,0,1,t,1,walk);
 const p=(t-.45)/1.2,pp=Math.min(1,Math.max(0,p));let lx,ly,zz;if(p<0){lx=1300;ly=1000;zz=1}else{if(pp<.45){const q=pp/.45;lx=230+q*620;ly=700}else{const q=(pp-.45)/.55;lx=850-q*600;ly=860}zz=1.9}
 LCc.setAttribute('cx',lx);LCc.setAttribute('cy',ly);LIN.setAttribute('transform',`translate(${lx} ${ly}) scale(${zz}) translate(${-lx} ${-ly})`);LR.setAttribute('transform',`translate(${lx},${ly})`);
 const on=p>=-.2&&p<=1.05?1:0;LG.setAttribute('opacity',on);LR.setAttribute('opacity',on)};
const PTS=el(PTG,'rect',{x:1080,y:0,width:60,height:1920,fill:'rgba(0,0,0,.35)'});let PTA=false;
const PTU=t=>{if(!PTA){S.appendChild(PTG);PTA=true}PMU(t);const u=cl((t-1.7)/.55);if(t>2.4||t<0){PTG.setAttribute('opacity',0);return}PTG.setAttribute('opacity',1);const sx_=1-ease(u);PTB.setAttribute('transform',`scale(${Math.max(.001,sx_).toFixed(3)},1)`);PTS.setAttribute('x',(1080*sx_).toFixed(1));PTS.setAttribute('opacity',u>0&&u<1?.6:0)};
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
const CLOUD=(g,col='#8da3b3')=>{const k=el(g,'g',{});[[-60,10,50],[0,-20,64],[62,8,52]].forEach(([x,y,r])=>el(k,'circle',{cx:x,cy:y,r,fill:col,stroke:'#fff','stroke-width':7}));el(k,'rect',{x:-110,y:10,width:220,height:46,rx:23,fill:col});return k};
const RAIN=(g,n=6)=>{const k=el(g,'g',{});const ls=[];for(let i=0;i<n;i++){ls.push(el(k,'path',{d:'M0 0 L-12 34',stroke:'#7fa6c4','stroke-width':8,'stroke-linecap':'round'}))}return{k,upd:t=>ls.forEach((l,i)=>{const u=((t*1.1+i/n)%1);l.setAttribute('transform',`translate(${-90+i*36},${60+u*90})`);l.setAttribute('opacity',1-u)})}};
const MOON=(g)=>{const k=el(g,'g',{});el(k,'circle',{r:62,fill:'#f2e6b8',stroke:'#fff','stroke-width':7});el(k,'circle',{cx:26,cy:-10,r:56,fill:'#0e2230'});return k};
const CALX=(g,hi)=>{const k=el(g,'g',{});el(k,'rect',{x:-210,y:-170,width:420,height:340,rx:14,fill:'#efe9d8',stroke:'#17120c','stroke-width':7});el(k,'rect',{x:-210,y:-170,width:420,height:64,rx:14,fill:'#d8372d',stroke:'#17120c','stroke-width':7});const tt=T(k,0,-124,'THÁNG 6 · 1944',32,'#fff',0,'middle','none');tt.setAttribute('stroke','none');tt.setAttribute('font-weight',900);const cells={};for(let i=0;i<14;i++){const x=-150+(i%7)*50,y=-60+Math.floor(i/7)*70;const c=el(k,'g',{});const n=T(c,x,y+10,String(i+1),30,'#17120c',0,'middle','none');n.setAttribute('stroke','none');n.setAttribute('font-weight',800);cells[i+1]={x,y}}return{k,cells}};
const MAN=(g,col='#6a7a8a')=>{const k=el(g,'g',{});el(k,'circle',{cx:0,cy:-100,r:26,fill:col,stroke:'#17120c','stroke-width':5});el(k,'rect',{x:-26,y:-72,width:52,height:100,rx:16,fill:col,stroke:'#17120c','stroke-width':5});return k};
// 1: hook (bản đồ thời tiết, zoom vào tâm bão, ✗)
PH(1,'d','dd4',900,596,'BẢN ĐỒ THỜI TIẾT THỜI ĐÓ (ẢNH TƯ LIỆU)',[['ĐỔ BỘ BỊ HOÃN MỘT NGÀY','bad',38,'hoãn',3.4],['CHỈ VÌ MỘT DỰ BÁO THỜI TIẾT','base',28,'chỉ',4.6]],null,{fx:.66,fy:.55,z:1.9,w:['hoãn',3.4],r:150,mark:'x',m:['một',4.0]});
// 2: kế hoạch chốt sẵn một ngày, thời tiết không theo
S2(2,2,'d',null,g=>{const c=CALX(g,5);const ring2=el(g,'circle',{r:34,fill:'none',stroke:CRED,'stroke-width':9});const cl=CLOUD(g);const rn=RAIN(g);const m=MAS(g);const A=strip2('KẾ HOẠCH CHỐT SẴN MỘT NGÀY','ok',34,21),B=strip2('NHƯNG THỜI TIẾT KHÔNG THEO','bad',34,22);
 return{upd:t=>{const e=popv(t,R(2)+.1,.6);PUT(c.k,540,560+Math.sin(t*1.3)*4,e,1.05,-2);const w=AT(2,'ngày',2.4);ring2.setAttribute('transform',`translate(${540+(c.cells[5].x)*1.05},${560+(c.cells[5].y+2)*1.05}) scale(${Math.max(.001,popv(t,w,.5))})`);const w2=AT(2,'thời',3.2),u=popv(t,w2,.6);PUT(cl,740,330,u,1.0,0);rn.k.setAttribute('transform','translate(740,330)');rn.k.setAttribute('opacity',u>0?1:0);rn.upd(t);m.at(130,1010,.8,0,popv(t,R(2)+.4,.5),t,1,0);shw(A,t,540,1130,-1,PV(t,2,'Kế',.2));shw(B,t,540,1240,1,PV(t,2,'nhưng',2.6))}}});
// 3: bờ biển Normandy (ảnh vệ tinh)
PH(3,'p','dd1',760,690,'BỜ BIỂN NORMANDY, PHÁP (ẢNH VỆ TINH)',[['NGÀY 5/6/1944','base',44,'ngày',5.6],['QUÂN ĐỒNG MINH ĐỊNH ĐỔ BỘ','ok',30,'đổ',3.6]],'1944',{fx:.42,fy:.3,z:1.8,w:['Normandy',3.0],r:170});
// 4: cần trăng, thủy triều thấp, nhưng biển động
S2(4,4,'d',null,g=>{const mo=MOON(g);const cl=CLOUD(g);const rn=RAIN(g);const wv=el(g,'path',{d:'M-300 0 Q-225 -40 -150 0 T0 0 T150 0 T300 0',fill:'none',stroke:'#7fa6c4','stroke-width':12,'stroke-linecap':'round'});const A=strip2('ĐÊM CÓ TRĂNG · THỦY TRIỀU RÚT THẤP','base',26,41),B=strip2('NHƯNG BIỂN ĐỘNG, MƯA GIÓ','bad',38,42);
 return{upd:t=>{PUT(mo,300,420+Math.sin(t*1.2)*6,popv(t,AT(4,'trăng',1.6),.6),1.3,0);const w=AT(4,'thủy',3.6);wv.setAttribute('transform',`translate(540,${820-inn(t,w,2)*-0}) `);wv.setAttribute('opacity',popv(t,w,.5));const w2=AT(4,'biển',5.6),u=popv(t,w2,.6);PUT(cl,720,380,u,1.3,0);rn.k.setAttribute('transform','translate(720,380)');rn.k.setAttribute('opacity',u>0?1:0);rn.upd(t);shw(A,t,540,1085,-1,PV(t,4,'Họ',.2));shw(B,t,540,1195,1,PV(t,4,'Nhưng',4.8))}}});
// 5: nhóm dự báo do đại tá James Stagg đứng đầu
S2(5,5,'p',null,g=>{const ps=[MAN(g,'#5a6a7a'),MAN(g,'#7a6a5a'),MAN(g,'#4a7a6a')];const st=MAN(g,'#355a7a');const bd=el(g,'g',{});el(bd,'rect',{x:-190,y:-110,width:380,height:220,rx:12,fill:'#efe9d8',stroke:'#17120c','stroke-width':7});for(let i=0;i<5;i++)el(bd,'path',{d:`M-150 ${-60+i*34} Q-90 ${-80+i*34} -30 ${-60+i*34} T90 ${-60+i*34}`,fill:'none',stroke:'#7a8a99','stroke-width':5});const A=strip2('ĐẠI TÁ JAMES STAGG','ok',44,51),B=strip2('ĐỨNG ĐẦU NHÓM DỰ BÁO','base',34,52);
 return{upd:t=>{const e=popv(t,R(5)+.1,.6);PUT(bd,540,500,e,1.2,-2);ps.forEach((p,i)=>PUT(p,330+i*100,880,popv(t,R(5)+.2+i*.15,.5),1.3,0));PUT(st,760,880,popv(t,AT(5,'James',3.6),.6),1.6,0);shw(A,t,540,1130,-1,PV(t,5,'đại',3.2));shw(B,t,540,1240,1,PV(t,5,'đứng',5.0))}}});
// 6: ông dự đoán một khoảng lặng ngắn, hoãn đúng một ngày
S2(6,6,'d',null,g=>{const c1=CLOUD(g),c2=CLOUD(g);const sun=el(g,'g',{});el(sun,'circle',{r:56,fill:'#f2c24a',stroke:'#fff','stroke-width':7});const ar=el(g,'path',{d:'M-170 0 L170 0 M110 -50 L170 0 L110 50',fill:'none',stroke:CGOLD,'stroke-width':20,'stroke-linecap':'round','stroke-linejoin':'round'});const d5=bigNum(g,'5/6',90,CSTEEL),d6=bigNum(g,'6/6',90,CGOLD);const A=strip2('KHOẢNG LẶNG GIỮA CÁC CƠN BÃO','ok',32,61),B=strip2('KHUYÊN HOÃN ĐÚNG MỘT NGÀY','base',34,62);
 return{upd:t=>{PUT(c1,230,420+Math.sin(t*1.2)*5,popv(t,R(6)+.1,.6),1.0,0);PUT(c2,850,420+Math.sin(t*1.2+2)*5,popv(t,R(6)+.3,.6),1.0,0);PUT(sun,540,430,popv(t,AT(6,'khoảng',1.8),.6),1.0,0);PUT(d5,330,770,popv(t,AT(6,'hoãn',4.6),.5),1,-3);PUT(ar,540,770,popv(t,AT(6,'hoãn',4.6)+.2,.5),.7,0);PUT(d6,750,770,popv(t,AT(6,'một',5.2),.5),1,3);shw(A,t,540,1085,-1,PV(t,6,'Ông',.2));shw(B,t,540,1195,1,PV(t,6,'nên',3.4))}}});
// 7: không phải ai cũng tin
S2(7,7,'p',null,g=>{const ps=[0,1,2,3].map(i=>MAN(g,['#5a6a7a','#7a6a5a','#4a7a6a','#7a5a6a'][i]));const xs=[0,1,2,3].map(()=>null);const bub=[0,1,2,3].map(i=>{const k=el(g,'g',{});el(k,'ellipse',{rx:56,ry:44,fill:'#fff',stroke:'#17120c','stroke-width':5});const q=T(k,0,14,'✗',46,CRED,0,'middle','none');q.setAttribute('stroke','none');q.setAttribute('font-weight',900);return k});const m=MAS(g);const A=strip2('KHÔNG PHẢI AI CŨNG TIN','bad',40,71),B=strip2('NHIỀU NHÀ KHÍ TƯỢNG KHÁC PHẢN ĐỐI','base',26,72);
 return{upd:t=>{ps.forEach((p,i)=>{PUT(p,210+i*220,860,popv(t,R(7)+.1+i*.12,.5),1.5,Math.sin(t*3+i)*3)});bub.forEach((b,i)=>PUT(b,210+i*220,560+Math.sin(t*2+i)*6,popv(t,AT(7,'nhiều',1.8)+i*.2,.5),1.2,0));m.at(540,1010,.8,0,popv(t,R(7)+.5,.5),t,1,0);shw(A,t,540,1130,-1,PV(t,7,'Nhưng',.2));shw(B,t,540,1240,1,PV(t,7,'nhiều',1.8))}}});
// 8: Eisenhower nghe theo
PH(8,'d','dd8',760,590,'TƯỚNG DWIGHT EISENHOWER NÓI CHUYỆN VỚI LÍNH · 1944 (ẢNH TƯ LIỆU)',[['EISENHOWER NGHE THEO DỰ BÁO','ok',34,'nghe',4.2],['VÌ ÔNG STAGG TỪNG DỰ BÁO ĐÚNG','base',28,'nhiều',6.6]],null,{fx:.38,fy:.28,z:1.8,w:['Eisenhower',1.4],r:170,mark:'ok',m:['nghe',4.4]});
// 9: hoãn thêm là lùi hai tuần, kế hoạch dễ lộ
PH(9,'p','dd3',900,675,'BẢN ĐỒ KẾ HOẠCH TẠI SOUTHWICK HOUSE (ẢNH MINH HỌA)',[['HOÃN THÊM = LÙI CẢ HAI TUẦN','bad',32,'lùi',3.4],['KẾ HOẠCH DỄ BỊ LỘ','bad',40,'kế',6.0]],null,{fx:.5,fy:.45,z:1.7,w:['lùi',3.2],r:170,mark:'x',m:['lộ',7.0]});
// 10: quân Đức tin bão kéo dài nên phòng thủ lỏng lẻo
S2(10,10,'d',null,g=>{const bk=[0,1,2,3,4].map(i=>{const k=el(g,'g',{});el(k,'path',{d:'M-46 30 L-46 -10 Q0 -50 46 -10 L46 30 Z',fill:'#7a7468',stroke:'#17120c','stroke-width':6});return k});const cl=CLOUD(g,'#6f8494');const rn=RAIN(g);const bq=el(g,'g',{});el(bq,'circle',{r:34,fill:'none',stroke:'#17120c','stroke-width':9});el(bq,'circle',{cx:90,r:34,fill:'none',stroke:'#17120c','stroke-width':9});el(bq,'path',{d:'M34 0 L56 0',stroke:'#17120c','stroke-width':9});const m=MAS(g);const A=strip2('QUÂN ĐỨC TIN BÃO SẼ KÉO DÀI','base',34,101),B=strip2('NHIỀU NƠI PHÒNG THỦ LỎNG LẺO','bad',34,102);
 return{upd:t=>{const w=AT(10,'tin',3.0);const u=popv(t,w,.6);PUT(cl,560,380,u,1.5,0);rn.k.setAttribute('transform','translate(560,400) scale(1.4)');rn.k.setAttribute('opacity',u>0?1:0);rn.upd(t);PUT(bq,240,560,popv(t,R(10)+.2,.5),1.2,-6);bk.forEach((b,i)=>{const gap=i==2?0:1;PUT(b,120+i*210,880,popv(t,AT(10,'lỏng',6.0)-.6+i*.15,.5)*gap+ (i==2?0:0),1.5,0)});m.at(540,1010,.8,0,popv(t,R(10)+.6,.5),t,1,0);shw(A,t,540,1130,-1,PV(t,10,'Còn',.2));shw(B,t,540,1240,1,PV(t,10,'nhiều',5.2))}}});
// 11: ngày 6/6 đổ bộ bắt đầu
PH(11,'d','dd11',760,618,'ĐỔ BỘ LÊN BÃI OMAHA · 6/6/1944 (ẢNH TƯ LIỆU)',[['NGÀY 6/6, CUỘC ĐỔ BỘ BẮT ĐẦU','ok',32,'thế',.4],['ĐÚNG KHOẢNG THỜI TIẾT ÔNG STAGG CHỈ RA','base',22,'đúng',4.6]],null,{fx:.45,fy:.55,z:1.7,w:['bắt',3.2],r:200,mark:'ok',m:['đúng',4.8]});
// 12: câu hỏi cuối
PH(12,'p','dd12',900,666,'TÀU ĐỔ BỘ GẦN BÃI OMAHA · THÁNG 6/1944 (ẢNH TƯ LIỆU)',[['ĐỔ BỘ ĐÚNG NGÀY CŨ, GIỮA BIỂN ĐỘNG','bad',28,'diễn',2.6],['KẾT CỤC SẼ RA SAO?','base',44,'kết',4.8]],null,{fx:.55,fy:.6,z:1.6,w:['biển',4.0],r:190},TOTAL);
sx(R(1)+.1,'whoosh',{d:.5,g:.5});
for(let i=1;i<=12;i++)bm(R(i)+.3,i%3!=1);
sx(R(12)+.3,'question',{g:.7});
