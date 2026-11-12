// ===== TÊN TỈNH THÀNH #08: Nghệ An (tn8). Bản đồ hành chính phẳng 34 tỉnh (geoBoundaries, phạm vi công cộng), không vẽ nước láng giềng.
const HB=[];const bm=(t,l)=>{sx(t,'boom',l?{light:true,g:.8}:{g:1});if(!l)HB.push(t)};
const PUT=(o,x,y,u,sc=1,rot=0)=>{o.setAttribute('transform',`translate(${x},${y}) rotate(${rot}) scale(${Math.max(.001,u)*sc})`);o.setAttribute('opacity',u>0?1:0)};
const CRED='#d8372d',CGOLD='#e0a63c',CSTEEL='#7fa6c4',OLN='#0a1018',RIV='#5fb3e6';
const KY=260/239.4;
const CK=(g,col=CGOLD)=>{const k=el(g,'g',{});const d='M-60 5 L-20 50 L65 -55';el(k,'path',{d,fill:'none',stroke:'#fff','stroke-width':34,'stroke-linecap':'round','stroke-linejoin':'round'});el(k,'path',{d,fill:'none',stroke:col,'stroke-width':20,'stroke-linecap':'round','stroke-linejoin':'round'});return k};
const XX=(g,col=CRED)=>{const k=el(g,'g',{});el(k,'path',{d:'M-60 -60 L60 60 M60 -60 L-60 60',stroke:'#fff','stroke-width':32,'stroke-linecap':'round'});el(k,'path',{d:'M-60 -60 L60 60 M60 -60 L-60 60',stroke:col,'stroke-width':18,'stroke-linecap':'round'});return k};
const HAN=(g,txt,size,col=CGOLD)=>{const t=T(g,0,size*.36,txt,size,col,Math.round(size*.06),'middle',OLN);t.setAttribute('style',"font-family:'Noto Serif CJK TC','Noto Serif CJK SC',serif;font-weight:900");return t};
const MLB=(g,txt,sz=30,col='#fff',bg=OLN)=>{const t=T(g,0,0,txt,sz,col,Math.max(5,Math.round(sz*.2)),'middle',bg);t.setAttribute('font-weight',900);return t};
const RINGS=(g,col,n=3)=>[...Array(n)].map(()=>el(g,'circle',{fill:'none',stroke:col,'stroke-width':6,r:1,opacity:0}));
const RU=(rs,t,R0,cx,cy,on=1,sp=.5)=>rs.forEach((e,i)=>{const u=((t*sp+i/rs.length)%1);e.setAttribute('cx',cx);e.setAttribute('cy',cy);e.setAttribute('r',12+u*R0);e.setAttribute('opacity',(1-u)*.85*on)});
// rồng phẳng tự vẽ (không theo mẫu nào), thân chữ S
const DRAGON=(g,col=CGOLD)=>{const k=el(g,'g',{});const d='M-150 60 C-110 -40 -40 90 10 0 S120 -70 150 -10';el(k,'path',{d,fill:'none',stroke:'#fff','stroke-width':52,'stroke-linecap':'round'});el(k,'path',{d,fill:'none',stroke:col,'stroke-width':38,'stroke-linecap':'round'});
 for(let i=0;i<7;i++){const x=-130+i*42,y=i%2?-34:30;el(k,'path',{d:`M${x} ${y-14} l12 -22 l12 22z`,fill:'#c0392b',stroke:'#fff','stroke-width':3})}
 const h=el(k,'g',{transform:'translate(158,-14)'});el(h,'ellipse',{rx:46,ry:32,fill:col,stroke:'#fff','stroke-width':7});el(h,'path',{d:'M-10 -28 L-30 -70 M14 -28 L8 -72',stroke:'#fff','stroke-width':8,'stroke-linecap':'round'});el(h,'circle',{cx:14,cy:-6,r:7,fill:OLN});el(h,'path',{d:'M40 10 Q70 20 76 46',fill:'none',stroke:'#fff','stroke-width':5});
 return k};
const CROWN=(g)=>{const k=el(g,'g',{});el(k,'path',{d:'M-60 30 L-70 -30 L-30 0 L0 -44 L30 0 L70 -30 L60 30Z',fill:CGOLD,stroke:'#fff','stroke-width':7,'stroke-linejoin':'round'});for(const x of[-70,0,70])el(k,'circle',{cx:x,cy:x?-34:-50,r:9,fill:CRED,stroke:'#fff','stroke-width':4});return k};
const FORT=(g)=>{const k=el(g,'g',{});const W='#8a7a5a';el(k,'rect',{x:-170,y:-30,width:340,height:120,fill:W,stroke:'#fff','stroke-width':7});for(let i=0;i<9;i++)el(k,'rect',{x:-170+i*40,y:-56,width:26,height:28,fill:W,stroke:'#fff','stroke-width':5});el(k,'path',{d:'M-34 90 L-34 30 Q0 0 34 30 L34 90Z',fill:'#2a1d10',stroke:'#fff','stroke-width':6});el(k,'path',{d:'M-60 -56 L-60 -150 L0 -186 L60 -150 L60 -56',fill:'#a8302a',stroke:'#fff','stroke-width':7,'stroke-linejoin':'round'});return k};
const SCRL=(g,w=380,h=300)=>{const k=el(g,'g',{});el(k,'rect',{x:-w/2,y:-h/2,width:w,height:h,rx:12,fill:'#e8dcba',stroke:OLN,'stroke-width':7});for(const x of[-w/2,w/2])el(k,'rect',{x:x-16,y:-h/2-10,width:32,height:h+20,rx:14,fill:'#9a6a3a',stroke:OLN,'stroke-width':6});for(let i=0;i<5;i++)el(k,'rect',{x:-w/2+44,y:-h/2+40+i*46,width:w-88-(i%2)*60,height:12,rx:6,fill:'rgba(60,40,20,.35)'});return k};
// ----- bản đồ hành chính phẳng
const KYP=1.0861;const PAL=['#8d7a5c','#7f6d52','#968263','#857257','#9a8667','#7a684e'];
const rpath=(ring)=>'M'+ring.map(p=>p[0]+' '+(-p[1]*KYP).toFixed(3)).join('L')+'Z';
function vnmap(w,h,seed=3){const g=mk();const id='vm'+(CID++);const o={g,w,h};
 const shg=el(g,'g',{filter:'url(#sh)'});el(shg,'rect',{x:-w/2-10,y:-h/2-10,width:w+20,height:h+20,rx:26,fill:'#e9dfc4'});
 const cp=el(g,'clipPath',{id});el(cp,'rect',{x:-w/2,y:-h/2,width:w,height:h,rx:20});
 const oc=el(g,'g',{'clip-path':`url(#${id})`});el(oc,'rect',{x:-w/2,y:-h/2,width:w,height:h,fill:'#13283a'});
 for(let i=0;i<14;i++)el(oc,'path',{d:`M${-w/2} ${-h/2+i*h/13} h${w}`,stroke:'rgba(127,166,196,.10)','stroke-width':2});
 const inner=el(oc,'g',{});o.inner=inner;const prov={};
 TINH34.forEach((p,i)=>{const d=p.p.map(rpath).join('');prov[p.n]=el(inner,'path',{d,fill:PAL[i%PAL.length],stroke:'#f6efdc','stroke-width':1.6,'vector-effect':'non-scaling-stroke','stroke-linejoin':'round'})});
 const outl=el(inner,'path',{d:TINH34.map(p=>p.p.map(rpath).join('')).join(''),fill:'none',stroke:'#fff8e6','stroke-width':3.2,'vector-effect':'non-scaling-stroke',opacity:.0});
 o.riv=el(inner,'g',{});o.top=el(oc,'g',{});o.over=el(g,'g',{});o.prov=prov;o.st={clon:106,clat:16,ppd:60};
 o.view=(clon,clat,ppd)=>{o.st={clon,clat,ppd};inner.setAttribute('transform',`translate(${(-clon*ppd).toFixed(2)},${(clat*KYP*ppd).toFixed(2)}) scale(${ppd})`)};
 o.P=(lon,lat)=>[(lon-o.st.clon)*o.st.ppd,(o.st.clat-lat)*o.st.ppd*KYP];
 o.at=(x,y,rot=0,sc=1,op=1)=>{g.setAttribute('transform',`translate(${x},${y}) rotate(${rot}) scale(${sc})`);g.setAttribute('opacity',op)};
 o.hi=(n,u,col='#f2c14e')=>{const e=prov[n];if(!e)return;e.setAttribute('fill',u>0?col:PAL[TINH34.findIndex(p=>p.n==n)%PAL.length]);e.setAttribute('fill-opacity',u>0?.55+.45*u:1)};
 o.line=(pts,col=RIV,wd=6,dash)=>{const d='M'+pts.map(p=>p[0]+' '+(-p[1]*KYP).toFixed(3)).join('L');const e=el(o.riv,'path',{d,fill:'none',stroke:col,'stroke-width':wd,'vector-effect':'non-scaling-stroke','stroke-linecap':'round','stroke-linejoin':'round',pathLength:1,'stroke-dasharray':dash||'1 1','stroke-dashoffset':1});return u=>{e.setAttribute('stroke-dashoffset',1-cl(u));e.setAttribute('opacity',u>0?1:0)}};
 o.view(106,16,60);return o}
// Hoàng Sa, Trường Sa: nhãn theo tọa độ thật (đảo đã có trong dữ liệu Đà Nẵng, Khánh Hòa)
function hsts(m){const L=el(m.top,'g',{});const a=MLB(L,'QĐ. HOÀNG SA',20,'#fff'),a2=MLB(L,'(VIỆT NAM)',20,'#f2c14e');const b=MLB(L,'QĐ. TRƯỜNG SA',20,'#fff'),b2=MLB(L,'(VIỆT NAM)',20,'#f2c14e');[a,a2,b,b2].forEach(e=>e.setAttribute('text-anchor','end'));
 const dots=[[111.6,16.5],[112.3,16.6],[111.2,16.0],[112.0,16.1]].map(()=>el(L,'circle',{r:5,fill:'#fff6d0',stroke:OLN,'stroke-width':2}));const dt=[[114.3,10.4],[114.5,11.4],[113.9,9.9],[115.0,10.8]].map(()=>el(L,'circle',{r:5,fill:'#fff6d0',stroke:OLN,'stroke-width':2}));
 return op=>{const H=[[111.6,16.5],[112.3,16.6],[111.2,16.0],[112.0,16.1]],S=[[114.3,10.4],[114.5,11.4],[113.9,9.9],[115.0,10.8]];H.forEach((p,i)=>{const[x,y]=m.P(...p);dots[i].setAttribute('cx',x);dots[i].setAttribute('cy',y)});S.forEach((p,i)=>{const[x,y]=m.P(...p);dt[i].setAttribute('cx',x);dt[i].setAttribute('cy',y)});
  const[hx,hy]=m.P(111.1,16.3),[sx2,sy]=m.P(113.8,10.5);a.setAttribute('x',hx);a.setAttribute('y',hy-4);a2.setAttribute('x',hx);a2.setAttribute('y',hy+20);b.setAttribute('x',sx2);b.setAttribute('y',sy-4);b2.setAttribute('x',sx2);b2.setAttribute('y',sy+20);L.setAttribute('opacity',op)}}
const BOX=(g,txt)=>{const k=el(g,'g',{});el(k,'rect',{x:-130,y:-70,width:260,height:140,rx:10,fill:'#c89b5a',stroke:'#fff','stroke-width':7});el(k,'path',{d:'M-130 -20 L130 -20',stroke:'#7a5a2e','stroke-width':6});const t=MLB(k,txt,42,'#fff');t.setAttribute('y',36);return k};
const SIGN=(g,txt,col='#1d5a46')=>{const k=el(g,'g',{});el(k,'rect',{x:-8,y:0,width:16,height:240,fill:'#9aa3ab',stroke:'#fff','stroke-width':4});el(k,'rect',{x:-230,y:-80,width:460,height:96,rx:12,fill:col,stroke:'#fff','stroke-width':7});const t=MLB(k,txt,44,'#fff',col);t.setAttribute('y',-16);return{k,t}};
// ===== Dấu ấn riêng (Nghệ An): nền tối xanh lá sen sẫm, giấy kem; nét nhà tranh, ao sen, núi và sông Lam ở đáy; cánh sen trôi chậm; sóng sông Lam (y>1640)
{DR1.setAttribute('opacity',0);DR2.setAttribute('opacity',0);
 DARKG.firstChild.setAttribute('fill','#12201e');
 [...PAPG.children].forEach(c=>{if(c.tagName=='g')c.setAttribute('opacity',0);if(c.tagName=='line')c.setAttribute('stroke','rgba(0,0,0,0)')});
 PAPG.firstChild.setAttribute('fill','#f0e9d4');
 const sky=(p,col)=>{const g=el(p,'g',{});const L=(d,w=5)=>el(g,'path',{d,fill:'none',stroke:col,'stroke-width':w,'stroke-linejoin':'round','stroke-linecap':'round'});
  L('M60 1630 L60 1540 L260 1540 L260 1630',6);L('M30 1550 L160 1450 L290 1550',7);L('M130 1630 L130 1580 L190 1580 L190 1630',4);   // nhà tranh
  for(let i=0;i<4;i++){const x=360+i*70;L(`M${x} 1630 Q${x-22} 1590 ${x} 1570 Q${x+22} 1590 ${x} 1630`,4);L(`M${x-30} 1632 L${x+30} 1632`,3)}   // sen
  L('M640 1630 Q700 1470 780 1550 Q840 1440 920 1540 Q980 1500 1080 1630',6);   // núi
  return g};
 const skA=sky(DARKG,'rgba(224,166,60,.16)'),skB=sky(PAPG,'rgba(60,100,80,.18)');
 const pet=(p,col)=>{const r=rng(88);return[...Array(10)].map(()=>({e:el(p,'ellipse',{rx:9,ry:5,fill:col}),x:r()*1080,s:.25+r()*.4,ph:r()*6}))};
 const pA=pet(DARKG,'rgba(232,140,170,.32)'),pB=pet(PAPG,'rgba(214,110,140,.26)');
 const wv=(p,col)=>[0,1,2].map(i=>el(p,'path',{fill:'none',stroke:col,'stroke-width':4+i,opacity:.6-i*.12}));
 const wA=wv(DARKG,'rgba(127,166,196,.40)'),wB=wv(PAPG,'rgba(60,100,110,.30)');
 window.THEME_UPD=t=>{const dx=Math.sin(t*.1)*14;skA.setAttribute('transform',`translate(${dx.toFixed(1)},0)`);skB.setAttribute('transform',`translate(${dx.toFixed(1)},0)`);
  [pA,pB].forEach(P=>P.forEach(o=>{const y=200+((t*36*o.s+o.ph*200)%1450);o.e.setAttribute('cx',(o.x+Math.sin(t*.7+o.ph)*34).toFixed(1));o.e.setAttribute('cy',y.toFixed(1));o.e.setAttribute('transform',`rotate(${(t*30+o.ph*60)%360} ${o.x} ${y})`);o.e.setAttribute('opacity',y>1250&&y<1520?0:1)}));
  [wA,wB].forEach(L=>L.forEach((e,i)=>{const y0=1680+i*64;let d='';for(let x=-20;x<=1100;x+=26){const y=y0+Math.sin(x*.016-t*(1.6+i*.4)+i)*13;d+=(x<0?'M':'L')+x+' '+y.toFixed(1)}e.setAttribute('d',d)}))};
}
const SEAH=()=>[strip('QĐ. HOÀNG SA (VIỆT NAM) ↘',false,22,901),strip('QĐ. TRƯỜNG SA (VIỆT NAM) ↓',false,22,902),strip('RANH GIỚI HIỆN NAY',false,20,903)];
const seaH=(L,t,e,lab)=>{sh(L[0],t,820,1180,0,e);sh(L[1],t,820,1235,0,e);sh(L[2],t,250,1235,0,e*(lab===false?0:1))};
const CARD=(g,txt,col=CSTEEL,w=360)=>{const k=el(g,'g',{});el(k,'rect',{x:-w/2,y:-70,width:w,height:140,rx:16,fill:col,stroke:'#fff','stroke-width':7});const t=MLB(k,txt,Math.min(46,Math.floor(w*1.3/txt.length)),'#fff',col);t.setAttribute('y',16);return{k,t,r:k.children[0]}};
const putC=(c,x,y,s,rot=0)=>{c.k.setAttribute('transform',`translate(${x},${y}) rotate(${rot}) scale(${s})`);c.k.setAttribute('opacity',s>0?1:0)};
const BIG=(g,txt,sz=110,col='#fff')=>{const t=T(g,0,0,txt,sz,col,Math.round(sz*.09),'middle',OLN);t.setAttribute('font-weight',900);return t};
const ACC=(g)=>{const k=el(g,'g',{});el(k,'path',{d:'M-14 22 L18 -26',stroke:'#fff','stroke-width':24,'stroke-linecap':'round'});el(k,'path',{d:'M-14 22 L18 -26',stroke:CRED,'stroke-width':14,'stroke-linecap':'round'});
 const f=el(k,'g',{});el(f,'circle',{cx:-2,cy:-4,r:3.5,fill:'#fff'});el(f,'circle',{cx:8,cy:-10,r:3.5,fill:'#fff'});return k};
// ---- người que: chân đặt tại (x,y); góc tính từ phương thẳng đứng xuống, dương là về phía trước (phải)
const STK=(g,o={})=>{const k=el(g,'g',{});const col=o.col||OLN,oc=o.oc||'#fff',w=o.w||12;const ln=()=>{const a=el(k,'path',{fill:'none',stroke:oc,'stroke-width':w+10,'stroke-linecap':'round','stroke-linejoin':'round'});const b=el(k,'path',{fill:'none',stroke:col,'stroke-width':w,'stroke-linecap':'round','stroke-linejoin':'round'});return[a,b]};
 const back=el(k,'g',{});const lL=ln(),aL=ln(),bd=ln(),lR=ln(),aR=ln();const hd=el(k,'g',{});el(hd,'circle',{r:30,fill:oc});el(hd,'circle',{r:24,fill:o.face||col});
 if(o.crown){el(hd,'path',{d:'M-22 -18 L-26 -44 L-10 -30 L0 -50 L10 -30 L26 -44 L22 -18Z',fill:CGOLD,stroke:'#fff','stroke-width':5,'stroke-linejoin':'round'})}
 if(o.hat){el(hd,'path',{d:'M-40 -10 L0 -46 L40 -10Z',fill:o.hat,stroke:'#fff','stroke-width':5,'stroke-linejoin':'round'})}
 if(o.bun){el(hd,'circle',{cx:-20,cy:-16,r:14,fill:col,stroke:oc,'stroke-width':5})}
 if(o.robe){o.rb=el(back,'path',{fill:o.robe,stroke:'#fff','stroke-width':5,'stroke-linejoin':'round'})}
 const hand=el(k,'g',{});const R2=d=>d*Math.PI/180;
 const lim=(p,a1,a2,l1,l2)=>{const q=[p[0]+Math.sin(R2(a1))*l1,p[1]+Math.cos(R2(a1))*l1];const r=[q[0]+Math.sin(R2(a1+a2))*l2,q[1]+Math.cos(R2(a1+a2))*l2];return[q,r]};
 const D=(L,pts)=>{const d='M'+pts.map(p=>p[0].toFixed(1)+' '+p[1].toFixed(1)).join('L');L[0].setAttribute('d',d);L[1].setAttribute('d',d)};
 const set=(p={})=>{const H=[0,-100],lean=R2(p.lean||0);const S=[H[0]+Math.sin(lean)*90,H[1]-Math.cos(lean)*90];D(bd,[H,S]);
  const[q1,r1]=lim(H,p.lL1||-6,p.lL2||0,52,50),[q2,r2]=lim(H,p.lR1||6,p.lR2||0,52,50);D(lL,[H,q1,r1]);D(lR,[H,q2,r2]);
  const[q3,r3]=lim(S,p.aL1||-14,p.aL2||0,44,42),[q4,r4]=lim(S,p.aR1||14,p.aR2||0,44,42);D(aL,[S,q3,r3]);D(aR,[S,q4,r4]);
  hd.setAttribute('transform',`translate(${(S[0]+Math.sin(lean)*36).toFixed(1)},${(S[1]-Math.cos(lean)*36).toFixed(1)}) rotate(${(p.tilt||0)})`);
  hand.setAttribute('transform',`translate(${r4[0].toFixed(1)},${r4[1].toFixed(1)}) rotate(${(p.aR1||14)+(p.aR2||0)})`);
  if(o.rb)o.rb.setAttribute('d',`M${S[0]-16} ${S[1]+10} L${H[0]-38} ${H[1]+48} L${H[0]+38} ${H[1]+48} L${S[0]+16} ${S[1]+10}Z`)};
 set();return{k,hand,set,at:(x,y,s=1,op=1,fl=1)=>{k.setAttribute('transform',`translate(${x},${y}) scale(${fl*s},${s})`);k.setAttribute('opacity',op)}}};
const WALK=(t,sp=6)=>{const a=Math.sin(t*sp)*26;return{lL1:a,lR1:-a,lL2:Math.max(0,-a)*.6,lR2:Math.max(0,a)*.6,aL1:-a*.8,aR1:a*.8}};
const BRUSH=(g)=>{const k=el(g,'g',{});el(k,'path',{d:'M0 0 L0 54',stroke:'#7a4a22','stroke-width':8,'stroke-linecap':'round'});el(k,'path',{d:'M-6 54 Q0 76 6 54Z',fill:OLN});return k};
const THRONE=(g)=>{const k=el(g,'g',{});el(k,'path',{d:'M-70 0 L-70 -170 Q0 -210 70 -170 L70 0 Z',fill:'#a8302a',stroke:'#fff','stroke-width':7});el(k,'rect',{x:-80,y:-70,width:160,height:24,rx:6,fill:CGOLD,stroke:'#fff','stroke-width':5});el(k,'rect',{x:-80,y:-6,width:160,height:12,fill:CGOLD});return k};
const DESK=(g)=>{const k=el(g,'g',{});el(k,'rect',{x:-110,y:-62,width:220,height:20,rx:5,fill:'#8a5a32',stroke:'#fff','stroke-width':5});el(k,'path',{d:'M-96 -42 L-96 0 M96 -42 L96 0',stroke:'#8a5a32','stroke-width':12});el(k,'rect',{x:-70,y:-74,width:120,height:12,fill:'#efe3c2',stroke:OLN,'stroke-width':3});return k};
// chiếu vua: giấy mở ra giữa hai trục, chữ hiện, ấn đỏ đóng xuống
const CHIEU=(g,txt,w=520)=>{const k=el(g,'g',{});const id='cc'+(CID++);const cp=el(k,'clipPath',{id});const cr=el(cp,'rect',{x:0,y:-110,width:1,height:220});const pg=el(k,'g',{'clip-path':`url(#${id})`});el(pg,'rect',{x:-w/2,y:-100,width:w,height:200,fill:'#efe3c2',stroke:'#9a6a3a','stroke-width':6});for(let i=0;i<3;i++)el(pg,'rect',{x:-w/2+40,y:-70+i*26,width:w-80-(i%2)*80,height:8,rx:4,fill:'rgba(80,50,20,.25)'});const tx=MLB(pg,txt,Math.min(54,Math.floor(w*1.4/txt.length)),CRED,'#efe3c2');tx.setAttribute('y',60);
 const r1=el(k,'rect',{x:-16,y:-116,width:32,height:232,rx:14,fill:'#9a6a3a',stroke:OLN,'stroke-width':5}),r2=el(k,'rect',{x:-16,y:-116,width:32,height:232,rx:14,fill:'#9a6a3a',stroke:OLN,'stroke-width':5});
 const seal=el(k,'g',{});el(seal,'rect',{x:-34,y:-34,width:68,height:68,rx:6,fill:CRED,stroke:'#fff','stroke-width':4});el(seal,'rect',{x:-22,y:-22,width:44,height:44,fill:'none',stroke:'#f6d0c0','stroke-width':4});
 return{k,u:(t,x,y,u,us,s=1)=>{k.setAttribute('transform',`translate(${x},${y}) scale(${s})`);k.setAttribute('opacity',u>0?1:0);const hw=w/2*u;cr.setAttribute('x',-hw);cr.setAttribute('width',2*hw+1);r1.setAttribute('x',-hw-16);r2.setAttribute('x',hw-16);PUT(seal,w/2-56,-62,popv(t,us,.35),lerp(1.8,1,inn(t,us,.25)),-8)}}};
// chữ Hán viết từ trên xuống, có ngọn bút chạy theo
const HANW=(g,txt,size)=>{const k=el(g,'g',{});const id='hw'+(CID++);const cp=el(k,'clipPath',{id});const cr=el(cp,'rect',{x:-size,y:-size*.8,width:size*2*txt.length,height:1});const gg=el(k,'g',{'clip-path':`url(#${id})`});HAN(gg,txt,size);const br=BRUSH(k);
 return{k,u:(x,y,u,s=1)=>{k.setAttribute('transform',`translate(${x},${y}) scale(${s})`);k.setAttribute('opacity',u>0?1:0);cr.setAttribute('height',size*1.6*u);cr.setAttribute('x',-size*txt.length);cr.setAttribute('width',size*2*txt.length);br.setAttribute('transform',`translate(${(Math.sin(u*40)*size*.35*txt.length).toFixed(1)},${(-size*.8+size*1.5*u-60).toFixed(1)})`);br.setAttribute('opacity',u>0&&u<1?1:0)}}};
const PAPERBALL=(g)=>{const k=el(g,'g',{});el(k,'circle',{r:20,fill:'#efe3c2',stroke:OLN,'stroke-width':4});el(k,'path',{d:'M-10 -6 L4 2 L-2 12 M6 -12 L10 4',stroke:OLN,'stroke-width':3,fill:'none'});return k};
// ===== CẢNH (người que chuyển động, chiếu vua, chữ Hán viết từng nét)
const NA=[104.95,19.2],HT=[105.75,18.3],TL=[105.85,21.03],NAMDAN=[105.5,18.7];
const NA_VIEW=(m,t,n,z0=250,z1=275)=>m.view(105.2,18.95,lerp(z0,z1,inn(t,R(n),E(n)-R(n))));
const HOUSE=(g,col='#c9a060')=>{const k=el(g,'g',{});el(k,'rect',{x:-80,y:-60,width:160,height:70,fill:'#8a6a44',stroke:'#fff','stroke-width':5});el(k,'path',{d:'M-110 -50 L0 -130 L110 -50Z',fill:col,stroke:'#fff','stroke-width':6,'stroke-linejoin':'round'});el(k,'rect',{x:-20,y:-40,width:40,height:50,fill:'#3a2414',stroke:'#fff','stroke-width':4});return k};
const LOTUS=(g)=>{const k=el(g,'g',{});for(let i=-2;i<=2;i++)el(k,'path',{d:'M0 0 Q-18 -26 0 -50 Q18 -26 0 0Z',fill:'#e88fae',stroke:'#fff','stroke-width':3,transform:`rotate(${i*24})`});el(k,'ellipse',{cx:0,cy:6,rx:44,ry:12,fill:'#4a8a5a',stroke:'#fff','stroke-width':3});return k};
const SCISS=(g)=>{const k=el(g,'g',{});const a=el(k,'g',{}),b=el(k,'g',{});[a,b].forEach((s,i)=>{el(s,'path',{d:'M0 0 L70 -8 L70 8Z',fill:'#cfd6dc',stroke:OLN,'stroke-width':4});el(s,'circle',{cx:-22,cy:i?14:-14,r:14,fill:'none',stroke:CRED,'stroke-width':8})});return{k,u:(x,y,o,s=1)=>{k.setAttribute('transform',`translate(${x},${y}) scale(${s})`);k.setAttribute('opacity',s>0?1:0);a.setAttribute('transform',`rotate(${-o})`);b.setAttribute('transform',`rotate(${o})`)}}};
const BOAT=(g)=>{const k=el(g,'g',{});el(k,'path',{d:'M-90 0 Q0 40 90 0 L70 -12 L-70 -12Z',fill:'#7a5a32',stroke:'#fff','stroke-width':5,'stroke-linejoin':'round'});return k};
const twoProv=(m)=>({set:(a,b,ca=CGOLD,cb=CGOLD)=>{m.hi('Nghệ An',a,ca);m.hi('Hà Tĩnh',b,cb)}});
const labAt=(m,e,p,op,dy=0)=>{const[x,y]=m.P(...p);e.setAttribute('x',x);e.setAttribute('y',y+dy);e.setAttribute('opacity',op)};

// 1 hook: Hà Tĩnh từng thuộc Nghệ An, rồi một ông vua chia đôi
S2(1,1,'d',null,g=>{const m=vnmap(940,860,81);const hs=hsts(m);const P=twoProv(m);const lNA=MLB(m.top,'NGHỆ AN',40,'#fff',OLN),lHT=MLB(m.top,'HÀ TĨNH',36,'#fff',OLN);const sc=SCISS(g);const A=strip('HÀ TĨNH TỪNG THUỘC NGHỆ AN?',true,40,11),B=strip('MỘT ÔNG VUA CHIA ĐÔI',false,40,12);const SH=SEAH();const tc=AT(1,'chia',4.6);bm(AT(1,'Hà',.9),true);bm(tc);
 return{upd:t=>{const e=inn(t,R(1)-.2,.5);m.at(540,760,0,1,e);NA_VIEW(m,t,1);seaH(SH,t,e);hs(e);const sp=inn(t,tc,.5);P.set(e,e,CGOLD,sp>0?CSTEEL:CGOLD);labAt(m,lNA,NA,e);labAt(m,lHT,HT,inn(t,tc,.4),20);
  const[x1,y1]=m.P(105.0,18.75),[x2,y2]=m.P(106.2,18.45);const u=inn(t,tc-.3,.8);sc.u(540+lerp(x1,x2,u),760+lerp(y1,y2,u),Math.abs(Math.sin(t*14))*22,popv(t,tc-.4,.3)*(1-inn(t,tc+.8,.3)));
  sh(A,t,540,380,-2,popv(t,AT(1,'Hà',.9),.5));sh(B,t,540,460,1,popv(t,tc,.5))}}});
// 2 xứ Nghệ: hai người que khoác vai dưới tấm biển
S2(2,2,'p',null,g=>{const a=STK(g,{hat:CGOLD}),b=STK(g,{hat:CSTEEL});const la=strip('NGHỆ AN',false,34,21),lb=strip('HÀ TĨNH',false,34,22);const ban=CARD(g,'XỨ NGHỆ',CRED,420);const A=strip('NÓI TỚI XỨ NGHỆ',false,40,23);const tx=AT(2,'xứ',2.6);bm(tx);
 return{upd:t=>{sh(A,t,540,330,-2,PV(t,2,'nói',1.6));putC(ban,540,560,popv(t,tx,.5),Math.sin(t*2)*2);const e=popv(t,R(2)+.1,.5);const sw=Math.sin(t*3)*6;a.at(430,1080,1,e);b.at(650,1080,1,e,-1);a.set({aR1:-60,aR2:-50,aL1:-20,tilt:sw*.5});b.set({aR1:-60,aR2:-50,aL1:-20,tilt:-sw*.5});sh(la,t,430,1150,-2,e);sh(lb,t,650,1150,2,e)}}});
// 3 Hoan Châu ở mạn nam xa xôi; người que đi bộ từ phía bắc xuống
S2(3,3,'d',null,g=>{const m=vnmap(940,860,31);const hs=hsts(m);const lab=MLB(m.top,'HOAN CHÂU',42,'#fff','#7a5a32');const dl=MLB(m.top,'THĂNG LONG',26,'#fff',OLN);const path=el(m.top,'path',{fill:'none',stroke:CGOLD,'stroke-width':6,'stroke-dasharray':'14 10'});const tv=STK(m.top,{col:'#f2ead6',oc:OLN,hat:'#c9b48a',w:10});const A=strip('MẠN NAM XA XÔI',true,42,31);const SH=SEAH();const th=AT(3,'Hoan',2.0);bm(th,true);
 return{upd:t=>{const e=inn(t,R(3)-.2,.5);m.at(540,760,0,1,e);m.view(105.6,19.9,lerp(150,170,inn(t,R(3),E(3)-R(3))));seaH(SH,t,e);hs(e);m.hi('Nghệ An',inn(t,th,.5),'#c9a050');m.hi('Hà Tĩnh',inn(t,th,.5),'#c9a050');labAt(m,lab,NA,popv(t,th,.4));labAt(m,dl,TL,e,-20);
  const[x1,y1]=m.P(...TL),[x2,y2]=m.P(105.4,19.0);path.setAttribute('d',`M${x1} ${y1} L${x2} ${y2}`);path.setAttribute('opacity',e);const u=((t-R(3))*.18)%1;tv.set(WALK(t,8));tv.at(lerp(x1,x2,u),lerp(y1,y2,u),.35,e);sh(A,t,540,380,-2,PV(t,3,'mạn',4.0))}}});
// 4 năm 1030: vua Lý Thái Tông đổi Hoan Châu thành châu Nghệ An
S2(4,4,'p',t=>'1030',g=>{const th=THRONE(g);const k=STK(g,{crown:true,robe:CGOLD});const ch=CHIEU(g,'CHÂU NGHỆ AN',460);const A=strip('VUA LÝ THÁI TÔNG',false,42,41);const ms=STK(g,{hat:CRED});el(ms.hand,'rect',{x:-14,y:-6,width:28,height:46,rx:8,fill:'#efe3c2',stroke:'#9a6a3a','stroke-width':5});const tn=AT(4,'Nghệ',3.6);bm(tn);
 return{upd:t=>{sh(A,t,540,320,-2,PV(t,4,'vua',1.0));PUT(th,240,900,popv(t,R(4)+.1,.5),.85,0);k.at(240,840,.85,popv(t,R(4)+.2,.5));k.set({lL1:80,lL2:-80,lR1:80,lR2:-80,aR1:105+Math.sin(t*2.2)*10,aR2:-10,aL1:-30,aL2:-40});
  ch.u(t,680,540+Math.sin(t*1.6)*6,inn(t,R(4)+.4,1.0),tn+.2,.85);const u=inn(t,tn+.3,E(4)-tn);ms.set(WALK(t,8));ms.at(lerp(420,980,u),1180,.75,popv(t,tn,.4))}}});
// 5 chữ Nghệ là cai quản, chữ An là yên ổn: người dân cấy lúa yên bình
S2(5,5,'d',null,g=>{const h1=HANW(g,'乂',170),h2=HANW(g,'安',170);const a1=strip('NGHỆ = CAI QUẢN',true,40,51),a2=strip('AN = YÊN ỔN',true,40,52);const fld=el(g,'rect',{x:60,y:1010,width:960,height:160,rx:20,fill:'rgba(90,150,90,.35)'});const rice=[...Array(18)].map(()=>el(g,'path',{fill:'none',stroke:'#7ac070','stroke-width':4}));const pp=[0,1,2].map(i=>STK(g,{col:'#f2ead6',oc:OLN,hat:CGOLD,w:10}));const B=strip('LỜI MONG VÙNG ĐẤT ĐƯỢC YÊN',false,36,53);const ta=AT(5,'An',2.0),tm=AT(5,'mong',4.6);bm(AT(5,'Nghệ',.6),true);bm(ta,true);
 return{upd:t=>{h1.u(320,500,inn(t,AT(5,'Nghệ',.6)-.2,.8));sh(a1,t,320,680,-2,popv(t,AT(5,'Nghệ',.6)+.4,.45));h2.u(760,500,inn(t,ta-.2,.8));sh(a2,t,760,680,2,popv(t,ta+.4,.45));const e=inn(t,R(5)+.3,.5);fld.setAttribute('opacity',e);
  rice.forEach((r,i)=>{const x=100+i*52,y=1150;const sw=Math.sin(t*2+i)*6;r.setAttribute('d',`M${x} ${y} Q${x+sw} ${y-30} ${x+sw*2} ${y-55}`);r.setAttribute('opacity',e)});pp.forEach((p,i)=>{const b=Math.sin(t*2.4+i*1.3);p.set({lean:40+b*12,aR1:30+b*20,aR2:20,aL1:20+b*20,aL2:20,lL1:-14,lR1:14});p.at(260+i*280,1160,.6,e)});sh(B,t,540,880,1,popv(t,tm,.5))}}});
// 6 suốt nhiều thế kỷ, Nghệ An gồm cả Hà Tĩnh ngày nay
S2(6,6,'p',null,g=>{const m=vnmap(940,860,61);const hs=hsts(m);const P=twoProv(m);const lab=MLB(m.top,'NGHỆ AN XƯA',40,'#fff',OLN);const lHT=MLB(m.top,'HÀ TĨNH NGÀY NAY',26,'#fff','#7a5a32');const A=strip('GỒM CẢ HÀ TĨNH NGÀY NAY',true,40,61);const SH=SEAH();const tg=AT(6,'gồm',3.2);bm(tg,true);
 return{upd:t=>{const e=inn(t,R(6)-.2,.5);m.at(540,760,0,1,e);NA_VIEW(m,t,6,275,250);seaH(SH,t,e);hs(e);const pulse=.75+.25*Math.sin(t*3);P.set(e*pulse,inn(t,tg,.5)*pulse);labAt(m,lab,NA,e);labAt(m,lHT,HT,popv(t,tg+.3,.4),40);sh(A,t,540,380,-2,popv(t,tg,.5))}}});
// 7 năm 1831: vua Minh Mạng chia lại cả nước thành các tỉnh
S2(7,7,'d',t=>'1831',g=>{const th=THRONE(g);const k=STK(g,{crown:true,robe:CGOLD,col:'#f2ead6',oc:OLN});const bd=el(g,'rect',{x:480,y:440,width:440,height:520,rx:14,fill:'#efe3c2',stroke:'#9a6a3a','stroke-width':8});const cuts=[...Array(6)].map(()=>el(g,'path',{fill:'none',stroke:CRED,'stroke-width':6,'stroke-dasharray':'1 1',pathLength:1,'stroke-dashoffset':1}));const A=strip('VUA MINH MẠNG',false,42,71),B=strip('CHIA CẢ NƯỚC THÀNH CÁC TỈNH',true,36,72);const tc=AT(7,'chia',2.4);bm(tc);
 return{upd:t=>{sh(A,t,540,320,-2,PV(t,7,'vua',1.6));PUT(th,240,900,popv(t,R(7)+.1,.5),.85,0);k.at(240,840,.85,popv(t,R(7)+.2,.5));k.set({lL1:80,lL2:-80,lR1:80,lR2:-80,aR1:100+Math.sin(t*2.4)*12,aR2:-10,aL1:-30,aL2:-40});bd.setAttribute('opacity',popv(t,R(7)+.3,.5));
  cuts.forEach((c,i)=>{const y=500+i*80;c.setAttribute('d',`M490 ${y+Math.sin(i)*20} Q700 ${y+30*Math.cos(i*2)} 910 ${y+10}`);c.setAttribute('stroke-dashoffset',1-inn(t,tc+i*.25,.4))});sh(B,t,540,1080,1,popv(t,tc,.5))}}});
// 8 phần đất phía nam tách ra thành tỉnh Hà Tĩnh
S2(8,8,'p',null,g=>{const m=vnmap(940,860,81);const hs=hsts(m);const P=twoProv(m);const lNA=MLB(m.top,'NGHỆ AN',40,'#fff',OLN),lHT=MLB(m.top,'HÀ TĨNH',44,'#fff',CSTEEL);const sc=SCISS(g);const A=strip('PHẦN ĐẤT PHÍA NAM',false,40,81),B=strip('TỈNH MỚI: HÀ TĨNH',true,44,82);const SH=SEAH();const tt=AT(8,'tách',2.4),th=AT(8,'Hà',4.6);bm(tt);bm(th,true);
 return{upd:t=>{const e=inn(t,R(8)-.2,.5);m.at(540,760,0,1,e);NA_VIEW(m,t,8);seaH(SH,t,e);hs(e);const s=inn(t,tt,.5);P.set(e,e,CGOLD,s>0?CSTEEL:CGOLD);labAt(m,lNA,NA,e);const[hx,hy]=m.P(...HT);lHT.setAttribute('x',hx);lHT.setAttribute('y',hy+20);lHT.setAttribute('opacity',popv(t,th,.4));
  const[x1,y1]=m.P(105.0,18.75),[x2,y2]=m.P(106.2,18.45);const u=inn(t,tt-.4,.9);sc.u(540+lerp(x1,x2,u),760+lerp(y1,y2,u),Math.abs(Math.sin(t*14))*22,popv(t,tt-.5,.3)*(1-inn(t,tt+.6,.3)));sh(A,t,540,380,-2,PV(t,8,'phía',1.0));sh(B,t,540,460,1,popv(t,th,.5))}}});
// 9 chữ Hà là sông, chữ Tĩnh là yên lặng: người que câu cá trên sông lặng
S2(9,9,'d',null,g=>{const h1=HANW(g,'河',170),h2=HANW(g,'靜',170);const a1=strip('HÀ = SÔNG',true,40,91),a2=strip('TĨNH = YÊN LẶNG',true,40,92);const rv=[0,1,2].map(()=>el(g,'path',{fill:'none',stroke:RIV,'stroke-width':10,'stroke-linecap':'round'}));const bt=BOAT(g);const fs=STK(g,{col:'#f2ead6',oc:OLN,hat:CGOLD,w:10});const line=el(g,'path',{fill:'none',stroke:'#f2ead6','stroke-width':3});const B=strip('XỨ NGHỆ CÓ THÊM MỘT CÁI TÊN',false,36,93);const tt=AT(9,'Tĩnh',2.0),tx=AT(9,'xứ',4.6);bm(AT(9,'Hà',.6),true);bm(tt,true);
 return{upd:t=>{h1.u(320,500,inn(t,AT(9,'Hà',.6)-.2,.8));sh(a1,t,320,680,-2,popv(t,AT(9,'Hà',.6)+.4,.45));h2.u(760,500,inn(t,tt-.2,.8));sh(a2,t,760,680,2,popv(t,tt+.4,.45));const e=inn(t,R(9)+.2,.5);
  rv.forEach((r,i)=>{let d='';for(let x=40;x<=1040;x+=16)d+=(x==40?'M':'L')+x+' '+(1060+i*36+Math.sin(x*.015+t*1.2+i)*5).toFixed(1);r.setAttribute('d',d);r.setAttribute('opacity',e*.8)});const bx=540+Math.sin(t*.6)*30,by=1050+Math.sin(t*1.5)*3;PUT(bt,bx,by,e,1,0);fs.set({lL1:80,lL2:-80,lR1:80,lR2:-80,aR1:120,aR2:-20,aL1:-20});fs.at(bx,by-14,.55,e);
  line.setAttribute('d',`M${bx+60} ${by-100} Q${bx+130} ${by-90} ${bx+140} ${by+20}`);line.setAttribute('opacity',e);sh(B,t,540,880,1,popv(t,tx,.5))}}});
// 10 hai tỉnh lại về chung một nhà
S2(10,10,'p',null,g=>{const hs2=HOUSE(g,CGOLD);const a=STK(g,{hat:CGOLD}),b=STK(g,{hat:CSTEEL});const A=strip('HƠN 140 NĂM SAU',false,42,101),B=strip('VỀ CHUNG MỘT NHÀ',true,48,102);const tc=AT(10,'chung',2.6);bm(tc);
 return{upd:t=>{sh(A,t,540,330,-2,PV(t,10,'Hơn',.4));PUT(hs2,540,820,popv(t,R(10)+.1,.5),1.5,0);const u=inn(t,R(10)+.3,tc-R(10));a.set(u<1?WALK(t,8):{aR1:-60,aR2:-50});b.set(u<1?WALK(t+.5,8):{aR1:-60,aR2:-50});a.at(lerp(80,460,u),1230,.75,1);b.at(lerp(1000,620,u),1230,.75,1,-1);sh(B,t,540,480,1,popv(t,tc,.5))}}});
// 11 năm 1976: nhập lại thành tỉnh Nghệ Tĩnh
S2(11,11,'d',t=>'1976',g=>{const m=vnmap(940,860,111);const hs=hsts(m);const P=twoProv(m);const lab=MLB(m.top,'NGHỆ TĨNH',48,'#fff',CRED);const st=stamp('NGHỆ TĨNH',64);const SH=SEAH();const tn=AT(11,'Nghệ',4.0);bm(AT(11,'nhập',2.6));bm(tn,true);
 return{upd:t=>{const e=inn(t,R(11)-.2,.5);m.at(540,760,0,1,e);NA_VIEW(m,t,11);seaH(SH,t,e);hs(e);const mg=inn(t,AT(11,'nhập',2.6),.6);P.set(e,e,CGOLD,mg>.5?CGOLD:CSTEEL);labAt(m,lab,[105.25,18.85],popv(t,tn,.4));const su=popv(t,tn+.4,.45);st.at(540,1020,-5,su,su>0?1:0)}}});
// 12 năm 1991: Quốc hội tách lại thành Nghệ An và Hà Tĩnh
S2(12,12,'p',t=>'1991',g=>{const m=vnmap(940,860,121);const hs=hsts(m);const P=twoProv(m);const lNA=MLB(m.top,'NGHỆ AN',40,'#fff',OLN),lHT=MLB(m.top,'HÀ TĨNH',40,'#fff',OLN);const sc=SCISS(g);const A=strip('TÁCH LẠI THÀNH HAI TỈNH',true,42,121);const SH=SEAH();const tt=AT(12,'tách',3.0);bm(tt);
 return{upd:t=>{const e=inn(t,R(12)-.2,.5);m.at(540,760,0,1,e);NA_VIEW(m,t,12,275,250);seaH(SH,t,e);hs(e);const s=inn(t,tt,.5);P.set(e,e,CGOLD,s>0?CSTEEL:CGOLD);labAt(m,lNA,NA,popv(t,tt+.3,.4));labAt(m,lHT,HT,popv(t,tt+.5,.4),20);
  const[x1,y1]=m.P(105.0,18.75),[x2,y2]=m.P(106.2,18.45);const u=inn(t,tt-.4,.9);sc.u(540+lerp(x1,x2,u),760+lerp(y1,y2,u),Math.abs(Math.sin(t*14))*22,popv(t,tt-.5,.3)*(1-inn(t,tt+.6,.3)));sh(A,t,540,380,-2,popv(t,tt,.5))}}});
// 13 năm 2025: cả hai tỉnh giữ nguyên
S2(13,13,'d',t=>'2025',g=>{const m=vnmap(940,860,131);const hs=hsts(m);const P=twoProv(m);const lNA=MLB(m.top,'NGHỆ AN',40,'#fff',OLN),lHT=MLB(m.top,'HÀ TĨNH',40,'#fff',OLN);const fl=[0,1].map(()=>el(m.top,'path',{fill:CRED,stroke:'#fff','stroke-width':3}));const st=stamp('GIỮ NGUYÊN CẢ HAI',54);const SH=SEAH();const tg=AT(13,'giữ',5.8);bm(tg);
 return{upd:t=>{const e=inn(t,R(13)-.2,.5);m.at(540,760,0,1,e);NA_VIEW(m,t,13);seaH(SH,t,e);hs(e);P.set(e,e,CGOLD,CSTEEL);labAt(m,lNA,NA,e);labAt(m,lHT,HT,e,20);
  [[104.6,19.5],[105.55,18.15]].forEach((p,i)=>{const[fx,fy]=m.P(...p);const w=Math.sin(t*5+i)*5;fl[i].setAttribute('d',`M${fx} ${fy} L${fx} ${fy-56} L${fx+38} ${fy-46+w} L${fx} ${fy-36}`);fl[i].setAttribute('opacity',popv(t,tg-.3+i*.2,.4))});const su=popv(t,tg+.3,.45);st.at(560,470,-5,su,su>0?1:0)}}});
// 14 quê hương Chủ tịch Hồ Chí Minh: làng Sen quê nội, làng Hoàng Trù quê ngoại (vẽ phẳng, không vẽ hình Bác)
S2(14,14,'p',null,g=>{const h1=HOUSE(g),h2=HOUSE(g);const ls=[0,1,2,3,4].map(()=>LOTUS(g));const pond=el(g,'ellipse',{cx:540,cy:1130,rx:420,ry:70,fill:'rgba(90,150,160,.4)',stroke:'#fff','stroke-width':4});const A=strip('QUÊ HƯƠNG CHỦ TỊCH HỒ CHÍ MINH',true,36,141);const l1=strip('LÀNG SEN · QUÊ NỘI',false,32,142),l2=strip('LÀNG HOÀNG TRÙ · QUÊ NGOẠI',false,30,143);const rg=RINGS(g,CGOLD,3);const tS=AT(14,'Sen',3.6),tH=AT(14,'Hoàng',5.4),tR=AT(14,'ra',7.2);bm(AT(14,'quê',1.4));bm(tR,true);
 return{upd:t=>{sh(A,t,540,330,-2,PV(t,14,'quê',1.4));PUT(h1,280,800,popv(t,tS-.2,.5),1,0);sh(l1,t,280,880,-2,popv(t,tS,.45));PUT(h2,800,800,popv(t,tH-.2,.5),1,0);sh(l2,t,800,880,2,popv(t,tH,.45));RU(rg,t,140,800,740,inn(t,tR,.4));
  pond.setAttribute('opacity',inn(t,R(14)+.2,.5));ls.forEach((l,i)=>PUT(l,220+i*150,1120+Math.sin(t*1.6+i)*5,popv(t,R(14)+.4+i*.12,.4),.8,Math.sin(t+i)*5))}}});
// 15 Nghệ An gần một nghìn năm; Hà Tĩnh là người em
S2(15,15,'d',null,g=>{const a=STK(g,{col:'#f2ead6',oc:OLN,hat:CGOLD,w:12}),b=STK(g,{col:'#f2ead6',oc:OLN,hat:CSTEEL,w:10});const la=strip('NGHỆ AN · GẦN 1000 NĂM',true,34,151),lb=strip('HÀ TĨNH · NGƯỜI EM',false,32,152);const n=T(g,0,0,'0',110,CGOLD,10,'middle',OLN);const te=AT(15,'em',4.6);bm(AT(15,'nghìn',2.4));bm(te,true);
 return{upd:t=>{const v=inn(t,R(15)+.2,1.6);n.textContent=Math.round(996*v);PUT(n,540,480,popv(t,R(15)+.2,.4),1,0);a.at(440,1150,1.15,popv(t,R(15)+.1,.5));a.set({aR1:-50,aR2:-40,aL1:-150-Math.sin(t*4)*10,aL2:-20});sh(la,t,420,700,-2,popv(t,AT(15,'nghìn',2.4),.45));
  b.at(620,1150,.75,popv(t,te-.3,.5),-1);b.set({aR1:-50,aR2:-40,aL1:-150-Math.sin(t*4+1)*10,aL2:-20});sh(lb,t,680,800,2,popv(t,te,.45))}}});
// 16 câu hỏi: quê bạn mang tên ấy bao nhiêu năm?
S2(16,16,'p',null,g=>{const m=vnmap(560,820,161);const hs=hsts(m);const qs=[[105.85,21.0],[106.68,20.86],[107.6,16.4],[108.2,16.05],[106.7,10.8],[105.75,10.05],[105.7,19.8],[108.95,13.8]].map(()=>T(m.top,0,0,'?',44,CGOLD,6,'middle',OLN));const A=strip('QUÊ BẠN',false,46,161),B=strip('TÊN ẤY BAO NHIÊU NĂM?',true,36,162);const kid=STK(g,{hat:CGOLD});const tq=AT(16,'Quê',.4);bm(tq);
 return{upd:t=>{const e=inn(t,R(16)-.2,.5);m.at(330,740,-1,1,e);m.view(108.6,15.9,44);hs(e);m.hi('Nghệ An',e,CGOLD);m.hi('Hà Tĩnh',e,CSTEEL);const P0=[[105.85,21.0],[106.68,20.86],[107.6,16.4],[108.2,16.05],[106.7,10.8],[105.75,10.05],[105.7,19.8],[108.95,13.8]];qs.forEach((q,i)=>{const[x,y]=m.P(...P0[i]);q.setAttribute('x',x);q.setAttribute('y',y+14+Math.sin(t*3+i)*5);q.setAttribute('opacity',popv(t,tq+.2+i*.15,.4))});
  sh(A,t,800,560,-2,popv(t,tq,.5));sh(B,t,790,650,2,PV(t,16,'bao',1.6));kid.at(800,1150,.85,popv(t,tq+.3,.5));kid.set({aR1:150,aR2:110+Math.sin(t*14)*14,aL1:-20,tilt:-8})}}},9999);
