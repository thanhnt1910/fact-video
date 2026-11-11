const VT2='TIỀN GIẤY';
// ===== Tiền giấy Hồ Quý Ly (xk13t). Ảnh: hq1(1) hq5(5) hq10(6). Cảnh 2,3,4,7,8,9,10,11 vẽ phẳng.
// ===== Dấu ấn riêng: nền giấy dó nâu vàng, vân gỗ khắc; một hàng con dấu đỏ triều đình lần lượt đóng xuống ở đáy (y>1600)
{DR1.setAttribute('opacity',0);DR2.setAttribute('opacity',0);
 DARKG.firstChild.setAttribute('fill','#241709');
 [...PAPG.children].forEach(c=>{if(c.tagName=='g')c.setAttribute('opacity',0);if(c.tagName=='line')c.setAttribute('stroke','rgba(120,80,30,.16)')});
 PAPG.firstChild.setAttribute('fill','#ead9ae');
 const sealRow=(p,col)=>{const g=el(p,'g',{});return [200,420,660,880].map((x,i)=>{const s=el(g,'g',{});el(s,'rect',{x:-34,y:-34,width:68,height:68,rx:6,fill:col,opacity:.92});el(s,'path',{d:'M-20 -8 L20 -8 M-20 8 L20 8 M0 -22 L0 22',stroke:'#fff',opacity:.8,'stroke-width':6,'stroke-linecap':'round'});return[s,x]})};
 const a=sealRow(DARKG,'#b3282a'),b=sealRow(PAPG,'#a32124');
 for(const [p,col] of [[DARKG,'rgba(214,160,60,.07)'],[PAPG,'rgba(120,80,30,.09)']]){const g=el(p,'g',{});for(let i=0;i<4;i++)el(g,'rect',{x:30+i*3,y:30+i*3,width:1020-i*6,height:1860-i*6,rx:10,fill:'none',stroke:col,'stroke-width':6})}
 window.THEME_UPD=t=>{[a,b].forEach(cs=>cs.forEach(([s,x],i)=>{const ph=((t*.45-i*.25)%1+1)%1;const k=ph<.18?1+(1-ph/.18)*.7:1;const op=ph<.05?ph/.05:1;s.setAttribute('transform',`translate(${x},1690) scale(${k}) rotate(${(i%2?3:-3)})`);s.setAttribute('opacity',op)}));PTU(t)};
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
const COIN=(g,r=70,col='#b08a3e')=>{const k=el(g,'g',{});el(k,'circle',{r,fill:col,stroke:'#fff','stroke-width':7});el(k,'circle',{r:r*.86,fill:'none',stroke:'#17120c','stroke-width':4});el(k,'rect',{x:-r*.2,y:-r*.2,width:r*.4,height:r*.4,fill:'#241709',stroke:'#17120c','stroke-width':4});return k};
const NOTE=(g,w,h,seed,title)=>{const k=el(g,'g',{});el(k,'rect',{x:-w/2,y:-h/2,width:w,height:h,rx:10,fill:'#efe3c2',stroke:'#17120c','stroke-width':7});el(k,'rect',{x:-w/2+16,y:-h/2+16,width:w-32,height:h-32,rx:6,fill:'none',stroke:'#a8741a','stroke-width':4});if(title){const t=T(k,0,-h/2+54,title,Math.min(40,w/11),'#17120c',0,'middle','none');t.setAttribute('stroke','none');t.setAttribute('font-weight',900)}const sl=el(k,'g',{});el(sl,'rect',{x:-30,y:-30,width:60,height:60,rx:5,fill:'#b3282a'});el(sl,'path',{d:'M-17 -6 L17 -6 M-17 8 L17 8 M0 -20 L0 20',stroke:'#fff','stroke-width':5,'stroke-linecap':'round'});sl.setAttribute('transform',`translate(${w/2-70},${h/2-60})`);return{k,seal:sl,w,h}};
const DRG=(g)=>{const k=el(g,'g',{});el(k,'path',{d:'M-50 20 Q-30 -40 0 0 T50 -10 L62 -24',fill:'none',stroke:'#7a4a1a','stroke-width':10,'stroke-linecap':'round'});el(k,'circle',{cx:62,cy:-24,r:7,fill:'#7a4a1a'});return k};
const TUR=(g)=>{const k=el(g,'g',{});el(k,'ellipse',{rx:48,ry:32,fill:'#4f6a3a',stroke:'#17120c','stroke-width':6});el(k,'circle',{cx:56,cy:-4,r:13,fill:'#4f6a3a',stroke:'#17120c','stroke-width':5});[[-26,24],[26,24],[-26,-24],[26,-24]].forEach(([x,y])=>el(k,'ellipse',{cx:x,cy:y,rx:11,ry:7,fill:'#4f6a3a',stroke:'#17120c','stroke-width':4}));return k};
const PHX=(g)=>{const k=el(g,'g',{});el(k,'path',{d:'M-40 30 Q-10 -50 30 -20 Q10 -10 40 10 Q0 30 -40 30Z',fill:'#b3482a',stroke:'#17120c','stroke-width':6,'stroke-linejoin':'round'});el(k,'path',{d:'M-60 40 Q-30 20 -40 30',fill:'none',stroke:'#e0a63c','stroke-width':8,'stroke-linecap':'round'});return k};
// 1: hook (đồng tiền cổ, ✗ lên "cấm dùng")
PH(1,'d','hq1',920,474,'ĐỒNG TIỀN CỔ (ẢNH MINH HỌA)',[['TIỀN GIẤY TỪ THỜI NHÀ TRẦN','ok',30,'giấy',1.6],['DÂN BỊ CẤM DÙNG TIỀN ĐỒNG','bad',30,'cấm',3.4]],null,{fx:.2,fy:.5,z:1.9,w:['đồng',4.2],r:150,mark:'x',m:['đồng',4.6]});
// 2: tiền tiện hơn nhưng dân không chịu dùng
S2(2,2,'d',null,g=>{const n=NOTE(g,380,240,2,null);const q=T(g,0,0,'?',260,'#e5483f',16,'middle',DK);const P=PEOPLE(g,5,'#6a5a46',22);const x=XX(g,'#d8372d');const m=MAS(g);const A=strip2('TIỀN GIẤY TIỆN HƠN','ok',40,21),B=strip2('DÂN KHÔNG CHỊU DÙNG','bad',40,22);
 return{upd:t=>{const e=popv(t,R(2)+.1,.6);PUT(n.k,540,520+Math.sin(t*1.4)*5,e,1,-3);PUT(P,540,930,popv(t,AT(2,'dân',1.6),.6),1.1,0);PUT(x,540,520,popv(t,AT(2,'không',2.0),.5),.9,0);const qp=popv(t,AT(2,'sao',3.2),.5);q.setAttribute('transform',`translate(540,640) rotate(-8) scale(${Math.max(.001,qp)*.55})`);q.setAttribute('opacity',qp>0?1:0);m.at(130,1010,.8,0,popv(t,R(2)+.4,.5),t,1,0);shw(A,t,540,1130,-1,PV(t,2,'tiện',.4));shw(B,t,540,1240,1,PV(t,2,'dân',1.6))}}});
// 3: triều đình nhà Trần in tờ tiền giấy đầu tiên
S2(3,3,'p',null,g=>{const n=NOTE(g,560,340,3,null);const A=strip2('CUỐI THỜI NHÀ TRẦN','base',42,31),B=strip2('TỜ TIỀN GIẤY ĐẦU TIÊN CỦA NƯỚC TA','ok',28,32);
 return{upd:t=>{const e=popv(t,R(3)+.1,.6);PUT(n.k,540,640+Math.sin(t*1.3)*5,e,1,-2);const w=AT(3,'in',5.0),u=inn(t,w,.5);n.seal.setAttribute('transform',`translate(${n.w/2-70},${n.h/2-60}) scale(${t<w?.001:(2.4-1.4*u)})`);n.seal.setAttribute('opacity',t<w?0:1);shw(A,t,540,1085,-1,PV(t,3,'cuối',1.8));shw(B,t,540,1195,1,PV(t,3,'tờ',6.0))}}});
// 4: Thông bảo hội sao, mỗi mệnh giá một hình
S2(4,4,'d',null,g=>{const n=NOTE(g,640,420,4,'THÔNG BẢO HỘI SAO');const d=DRG(g),tu=TUR(g),ph=PHX(g);const A=strip2('THÔNG BẢO HỘI SAO','ok',44,41),B=strip2('MỖI MỆNH GIÁ MỘT HÌNH KHÁC NHAU','base',26,42);
 return{upd:t=>{const e=popv(t,R(4)+.1,.6);PUT(n.k,540,600+Math.sin(t*1.3)*5,e,1,2);PUT(d,380,640,popv(t,AT(4,'rồng',5.0),.5),1.15,0);PUT(tu,540,690,popv(t,AT(4,'rùa',5.8),.5),1.0,0);PUT(ph,700,650,popv(t,AT(4,'phượng',6.4),.5),1.15,0);shw(A,t,540,1085,-1,PV(t,4,'Tờ',.2));shw(B,t,540,1195,1,PV(t,4,'mỗi',3.0))}}});
// 5: thu tiền đồng về đổi tiền giấy
PH(5,'p','hq5',920,478,'ĐỒNG TIỀN CỔ (ẢNH MINH HỌA)',[['THU TIỀN ĐỒNG VỀ, ĐỔI LẤY TIỀN GIẤY','base',26,'thu',1.4],['DÂN KHÔNG ĐƯỢC DÙNG TIỀN ĐỒNG','bad',28,'không',6.2]],null,{fx:.5,fy:.5,z:1.8,w:['đồng',4.0],r:190,mark:'x',m:['không',6.4]});
// 6: sách chép lại hình phạt
PH(6,'d','hq10',720,604,'TRANG SỬ CŨ (ẢNH MINH HỌA)',[['NGƯỜI TA CHÉP LẠI','base',40,'Người',.2],['XỬ TỬ · TỊCH THU TÀI SẢN','bad',32,'xử',3.0]],null,{fx:.55,fy:.4,z:1.8,w:['xử',3.0],r:170});
// 7: dân quay về đổi hàng lấy hàng
S2(7,7,'p',null,g=>{const a1=PEOPLE(g,1,'#6a5a46',71),a2=PEOPLE(g,1,'#5a6a7a',72);const bag=el(g,'g',{});el(bag,'rect',{x:-40,y:-50,width:80,height:90,rx:26,fill:'#c8a15a',stroke:'#17120c','stroke-width':6});const cl=el(g,'g',{});el(cl,'rect',{x:-50,y:-30,width:100,height:60,rx:8,fill:'#3f7fa8',stroke:'#17120c','stroke-width':6});const c=COIN(g,50);const x=XX(g,'#d8372d');const m=MAS(g);const A=strip2('DÂN QUEN TIỀN ĐỒNG','base',38,71),B=strip2('QUAY VỀ ĐỔI HÀNG LẤY HÀNG','bad',32,72);
 return{upd:t=>{const e=popv(t,R(7)+.1,.6);PUT(a1,220,800,e,1.9,0);PUT(a2,860,800,e,1.9,0);const w=AT(7,'đổi',6.0),u=inn(t,w,1.4);PUT(bag,220+u*320,560-Math.sin(u*Math.PI)*60,popv(t,w-.4,.5),1.3,0);PUT(cl,860-u*320,560-Math.sin(u*Math.PI)*60,popv(t,w-.4,.5),1.2,0);PUT(c,540,500,popv(t,AT(7,'tiền',1.2),.5),1.2,0);PUT(x,540,500,popv(t,AT(7,'ép',3.6),.5),.9,0);m.at(540,1010,.8,0,popv(t,R(7)+.6,.5),t,1,0);shw(A,t,540,1130,-1,PV(t,7,'dân',.2));shw(B,t,540,1240,1,PV(t,7,'quay',5.2))}}});
// 8: tiền giấy mất giá
S2(8,8,'d',null,g=>{const n=NOTE(g,420,260,8,null);const big=bigNum(g,'100%',150,CRED);const ar=el(g,'path',{d:'M0 -120 L0 120 M-60 60 L0 130 L60 60',fill:'none',stroke:CRED,'stroke-width':28,'stroke-linecap':'round','stroke-linejoin':'round'});const A=strip2('TIỀN GIẤY MẤT GIÁ','bad',44,81),B=strip2('RỒI KHÔNG CÒN ĐƯỢC DÙNG','base',34,82);
 return{upd:t=>{const e=popv(t,R(8)+.1,.6);const u=inn(t,AT(8,'dần',1.6),2.0);PUT(n.k,540,560-0,e,1.0*(1-.45*u),-2+u*8);n.k.setAttribute('opacity',e>0?(1-.7*u):0);big.textContent=String(Math.round(100*(1-u)))+'%';PUT(big,540,860,popv(t,R(8)+.3,.5),1,0);PUT(ar,820,560+u*60,popv(t,R(8)+.5,.5),1.0,0);shw(A,t,540,1130,-1,PV(t,8,'Vì',.2));shw(B,t,540,1240,1,PV(t,8,'rồi',2.4))}}});
// 9: khi dân không còn tin, tờ tiền chỉ còn là tờ giấy
S2(9,9,'p',null,g=>{const n=NOTE(g,520,320,9,null);const x=XX(g,'#d8372d');const A=strip2('DÂN KHÔNG CÒN TIN','bad',42,91),B=strip2('CHỈ CÒN LÀ MỘT TỜ GIẤY','base',34,92);
 return{upd:t=>{const e=popv(t,R(9)+.1,.6);const u=inn(t,AT(9,'chỉ',3.2),1.2);PUT(n.k,540,620+u*80,e,1.0-.35*u,-3+u*22);n.k.setAttribute('opacity',e>0?(1-.5*u):0);PUT(x,540,620,popv(t,AT(9,'không',1.6),.5),1.0,0);shw(A,t,540,1085,-1,PV(t,9,'Khi',.2));shw(B,t,540,1195,1,PV(t,9,'chỉ',3.2))}}});
// 10: khoảng mười năm sau, nhà Hồ sụp đổ
S2(10,10,'d',null,g=>{const ln=el(g,'path',{d:'M180 640 L900 640',stroke:'#17120c','stroke-width':14,'stroke-linecap':'round',pathLength:1,'stroke-dasharray':1,'stroke-dashoffset':1});const d1=el(g,'circle',{r:34,fill:CSTEEL,stroke:'#fff','stroke-width':8}),d2=el(g,'circle',{r:34,fill:CRED,stroke:'#fff','stroke-width':8});const l1=strip2('TIỀN GIẤY RA ĐỜI','base',26,101),l2=strip2('NHÀ HỒ SỤP ĐỔ','bad',26,102);const big=bigNum(g,'~10 NĂM',130,CGOLD);const A=strip2('QUÂN NHÀ MINH TRÀN SANG','bad',38,103);
 return{upd:t=>{const w1=R(10)+.2,w2=AT(10,'sụp',3.6),v=inn(t,w1,w2-w1+.4);ln.setAttribute('stroke-dashoffset',1-v);PUT(d1,180,640,popv(t,w1,.5));PUT(d2,900,640,popv(t,w2,.5));shw(l1,t,250,520,-3,PV(t,10,'Khoảng',.2));shw(l2,t,830,520,3,PV(t,10,'sụp',3.6));PUT(big,540,860,popv(t,AT(10,'mười',1.0),.5),1,-2);shw(A,t,540,1130,-1,PV(t,10,'quân',5.2))}}});
// 11: câu hỏi cuối: nỗi sợ hay lòng tin
S2(11,11,'p',null,g=>{const n=NOTE(g,330,210,11,null);const hv=el(g,'g',{});el(hv,'path',{d:'M0 60 C-150 -40 -90 -140 0 -70 C90 -140 150 -40 0 60Z',fill:CRED,stroke:'#fff','stroke-width':9});const q=T(g,0,0,'?',280,'#e5483f',16,'middle',DK);const m=MAS(g);const A=strip2('NỖI SỢ','bad',50,111),B=strip2('HAY LÒNG TIN CỦA DÂN?','ok',34,112);
 return{upd:t=>{PUT(n.k,300,600+Math.sin(t*1.5)*6,popv(t,R(11)+.2,.6),1.1,-3);PUT(hv,780,600+Math.sin(t*1.5+2)*6,popv(t,AT(11,'lòng',4.6),.6),1.0,3);const qp=popv(t,AT(11,'thắng',3.2)+.3,.5);q.setAttribute('transform',`translate(540,640) rotate(${Math.sin(t*2)*6-6}) scale(${Math.max(.001,qp)})`);q.setAttribute('opacity',qp>0?1:0);m.at(540,1010,.8,0,popv(t,R(11)+.4,.5),t,1,0);shw(A,t,300,880,-2,PV(t,11,'nỗi',2.2));shw(B,t,700,1140,2,PV(t,11,'lòng',4.6))}}},TOTAL);
sx(R(1)+.1,'whoosh',{d:.5,g:.5});
for(let i=1;i<=11;i++)bm(R(i)+.3,i%3!=1);
sx(R(11)+.3,'question',{g:.7});
