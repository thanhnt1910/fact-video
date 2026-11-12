// ===== TÊN TỈNH THÀNH #07: Thanh Hóa (tn7). Bản đồ hành chính phẳng 34 tỉnh (geoBoundaries, phạm vi công cộng), không vẽ nước láng giềng.
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
// ===== Dấu ấn riêng (Thanh Hóa): nền tối xanh rêu đá, giấy kem; nét cổng Thành nhà Hồ (ba vòm đá), núi và cầu vòm Hàm Rồng ở đáy; cò bay chậm; sóng sông Mã (y>1640)
{DR1.setAttribute('opacity',0);DR2.setAttribute('opacity',0);
 DARKG.firstChild.setAttribute('fill','#141d18');
 [...PAPG.children].forEach(c=>{if(c.tagName=='g')c.setAttribute('opacity',0);if(c.tagName=='line')c.setAttribute('stroke','rgba(0,0,0,0)')});
 PAPG.firstChild.setAttribute('fill','#efe8d2');
 const sky=(p,col)=>{const g=el(p,'g',{});const L=(d,w=5)=>el(g,'path',{d,fill:'none',stroke:col,'stroke-width':w,'stroke-linejoin':'round','stroke-linecap':'round'});
  // cổng Thành nhà Hồ: khối đá, ba vòm
  L('M40 1630 L40 1500 L420 1500 L420 1630',6);for(let i=0;i<9;i++)L(`M${40+i*47} 1500 L${40+i*47} 1630`,2);L('M40 1540 L420 1540 M40 1585 L420 1585',2);
  L('M90 1630 L90 1585 Q125 1545 160 1585 L160 1630 M195 1630 L195 1570 Q230 1525 265 1570 L265 1630 M300 1630 L300 1585 Q335 1545 370 1585 L370 1630',5);
  // núi Hàm Rồng và cầu vòm thép
  L('M560 1630 Q600 1500 650 1560 Q700 1450 760 1540 Q800 1500 830 1630',6);
  L('M830 1610 L1080 1610',6);L('M840 1610 Q955 1500 1070 1610',6);for(let i=1;i<8;i++){const x=840+i*29;const y=1610-Math.sin(i/8*Math.PI)*110*.92;L(`M${x} 1610 L${x} ${y.toFixed(0)}`,2)}
  return g};
 const skA=sky(DARKG,'rgba(224,166,60,.16)'),skB=sky(PAPG,'rgba(70,90,70,.18)');
 const bird=(p,col)=>[...Array(5)].map((_,i)=>({e:el(p,'path',{fill:'none',stroke:col,'stroke-width':3,'stroke-linecap':'round'}),x:i*230,y:1540+(i%3)*22,s:.6+(i%2)*.3}));
 const bA=bird(DARKG,'rgba(240,230,200,.35)'),bB=bird(PAPG,'rgba(60,60,50,.30)');
 const wv=(p,col)=>[0,1,2].map(i=>el(p,'path',{fill:'none',stroke:col,'stroke-width':4+i,opacity:.6-i*.12}));
 const wA=wv(DARKG,'rgba(127,166,196,.40)'),wB=wv(PAPG,'rgba(60,100,90,.30)');
 window.THEME_UPD=t=>{const dx=Math.sin(t*.1)*14;skA.setAttribute('transform',`translate(${dx.toFixed(1)},0)`);skB.setAttribute('transform',`translate(${dx.toFixed(1)},0)`);
  [bA,bB].forEach(B=>B.forEach(o=>{const x=((o.x+t*30*o.s)%1200)-60,f=Math.sin(t*6+o.x)*8;o.e.setAttribute('d',`M${x-16} ${o.y-f} Q${x-8} ${o.y-6} ${x} ${o.y} Q${x+8} ${o.y-6} ${x+16} ${o.y-f}`)}));
  [wA,wB].forEach(L=>L.forEach((e,i)=>{const y0=1680+i*64;let d='';for(let x=-20;x<=1100;x+=26){const y=y0+Math.sin(x*.016-t*(1.6+i*.4)+i)*13;d+=(x<0?'M':'L')+x+' '+y.toFixed(1)}e.setAttribute('d',d)}))};
}
// ===== CẢNH (bản 2: người que chuyển động, chiếu vua, chữ Hán viết từng nét, dấu sắc là nhân vật)
const TH=[105.78,19.80],TL=[105.85,21.03];
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

// 1 hook: dấu sắc của Thanh Hóa bay mất, rồi bay về
S2(1,1,'d',null,g=>{const m=vnmap(940,860,71);const hs=hsts(m);const rg=RINGS(m.top,CGOLD);const lab=MLB(m.top,'THANH HOA',46,'#fff',OLN);const ac=ACC(g);const A=strip('MẤT DẤU SẮC GẦN 400 NĂM?',true,40,11),B=strip('VÌ TÊN MẸ MỘT ÔNG VUA',false,40,12);const SH=SEAH();const tm=AT(1,'mất',1.6),tl=AT(1,'lấy',3.8);bm(tm,true);bm(tl);
 return{upd:t=>{const e=inn(t,R(1)-.2,.5);m.at(540,760,0,1,e);m.view(106.2,19.6,lerp(170,210,inn(t,R(1),E(1)-R(1))));seaH(SH,t,e);hs(e);m.hi('Thanh Hóa',e,CGOLD);const[x,y]=m.P(...TH);RU(rg,t,80,x,y,e);
  lab.setAttribute('x',x+40);lab.setAttribute('y',y-70);lab.setAttribute('opacity',e);const hx=540+x+40+108,hy=760+y-70-58;
  const out=inn(t,tm,.9),back2=inn(t,tl-.2,.6);const ax=lerp(hx,980,out*(1-back2)),ay=lerp(hy,240,out*(1-back2))+Math.sin(t*5)*8*out*(1-back2);PUT(ac,ax,ay,e,1+.3*out*(1-back2),Math.sin(t*6)*20*out*(1-back2));
  sh(A,t,540,380,-2,popv(t,tm,.5));sh(B,t,540,460,1,PV(t,1,'mẹ',5.4))}}});
// 2 hai chữ chỉ khác một dấu; thầy đồ viết hai chữ Hán khác hẳn
S2(2,2,'p',null,g=>{const a=BIG(g,'THANH HÓA',62),b=BIG(g,'THANH HOA',62);const ne=T(g,0,0,'≠',110,CRED,10,'middle',OLN);const h1=HANW(g,'清化',140),h2=HANW(g,'清華',140);const dk=DESK(g);const sc=STK(g,{hat:'#7a5a32'});const br=BRUSH(sc.hand);br.setAttribute('transform','rotate(180) translate(0,-10)');const A=strip('CHỈ KHÁC MỘT DẤU',false,40,21),B=strip('HAI CHỮ HÁN KHÁC HẲN',true,42,22);const th=AT(2,'Hán',3.8);bm(th);
 return{upd:t=>{PUT(a,270,470,popv(t,R(2)+.05,.5),1,0);PUT(b,810,470,popv(t,R(2)+.3,.5),1,0);PUT(ne,540,450,popv(t,AT(2,'khác',1.8),.4),1,0);sh(A,t,540,320,-2,PV(t,2,'khác',1.8));
  h1.u(300,680,inn(t,th,1.0));h2.u(780,680,inn(t,th+.9,1.0));PUT(dk,540,1200,popv(t,R(2)+.2,.5),1,0);sc.at(540,1200,.9,popv(t,R(2)+.2,.5));const wr=inn(t,th,2.2)>0&&inn(t,th,2.2)<1;sc.set({aR1:70+(wr?Math.sin(t*14)*12:0),aR2:30,aL1:-30,aL2:40,lean:8});sh(B,t,540,860,1,popv(t,th,.5))}}});
// 3 Cửu Chân rồi Ái Châu, trên bản đồ, người dân đi lại
S2(3,3,'d',null,g=>{const m=vnmap(940,860,31);const hs=hsts(m);const rg=RINGS(m.top,CGOLD);const lab=MLB(m.top,'CỬU CHÂN',44,'#fff','#7a5a32');const pp=[0,1,2].map(i=>STK(g,{col:'#f2ead6',oc:OLN,hat:['#c9b48a',CGOLD,'#a8302a'][i],w:10}));const A=strip('NGÀY XƯA',false,42,31);const SH=SEAH();const tc=AT(3,'Ái',2.6);bm(AT(3,'Cửu',1.4),true);bm(tc,true);
 return{upd:t=>{const e=inn(t,R(3)-.2,.5);m.at(540,700,0,1,e);m.view(106.2,19.7,190);seaH(SH,t,e);hs(e);m.hi('Thanh Hóa',inn(t,AT(3,'Cửu',1.4),.5),'#c9a050');const[x,y]=m.P(...TH);RU(rg,t,70,x,y,e);
  const sw=inn(t,tc-.3,.4);lab.textContent=sw>.5?'ÁI CHÂU':'CỬU CHÂN';lab.setAttribute('x',x+30);lab.setAttribute('y',y-60);lab.setAttribute('opacity',popv(t,AT(3,'Cửu',1.4),.4));lab.setAttribute('transform',`translate(${x+30},${y-60}) scale(1,${Math.max(.05,Math.abs(1-2*sw))}) translate(${-(x+30)},${-(y-60)})`);
  sh(A,t,540,300,-2,PV(t,3,'Ngày',.2));pp.forEach((p,i)=>{p.at(-999,0,.5,0)})}}});
// 4 năm 1029: vua Lý Thái Tông ra chiếu, sứ giả mang chiếu từ Thăng Long vào phủ Thanh Hóa
S2(4,4,'p',t=>'1029',g=>{const th=THRONE(g);const k=STK(g,{crown:true,robe:CGOLD});const ch=CHIEU(g,'PHỦ THANH HÓA',460);const A=strip('VUA LÝ THÁI TÔNG',false,42,41);const st=stamp('LẦN ĐẦU XUẤT HIỆN',48);const tp=AT(4,'phủ',3.6),tl=AT(4,'lần',5.0);bm(tp);bm(tl,true);
 const ms=STK(g,{hat:CRED});el(ms.hand,'rect',{x:-14,y:-6,width:28,height:46,rx:8,fill:'#efe3c2',stroke:'#9a6a3a','stroke-width':5});
 return{upd:t=>{sh(A,t,540,320,-2,PV(t,4,'vua',1.0));PUT(th,250,900,popv(t,R(4)+.1,.5),.85,0);k.at(250,840,.85,popv(t,R(4)+.2,.5));k.set({lL1:80,lL2:-80,lR1:80,lR2:-80,aR1:110+Math.sin(t*2)*8*inn(t,tp-.8,.3),aR2:-10,aL1:-30,aL2:-40});
  ch.u(t,660,560,inn(t,tp-.6,.7),tp+.2,.9);const u=inn(t,tp+.6,E(4)-tp-.6);ms.set(WALK(t,8));ms.at(lerp(420,960,u),1180,.75,popv(t,tp+.5,.4));const su=popv(t,tl,.45);st.at(660,820,-5,su,su>0?1:0)}}});
// 5 chữ Thanh là trong, chữ Hóa là biến đổi: dòng sông đục hóa trong, người dân an vui
S2(5,5,'d',null,g=>{const h1=HANW(g,'清',170),h2=HANW(g,'化',170);const a1=strip('THANH = TRONG',true,40,51),a2=strip('HÓA = BIẾN ĐỔI',true,40,52);const rv=[0,1,2].map(()=>el(g,'path',{fill:'none','stroke-width':16,'stroke-linecap':'round'}));const pp=[0,1].map(i=>STK(g,{col:'#f2ead6',oc:OLN,hat:[CGOLD,'#c9b48a'][i],w:10}));const B=strip('MONG LÒNG NGƯỜI TRONG SÁNG, YÊN ỔN',false,34,53);const th=AT(5,'Hóa',2.0),tm=AT(5,'mong',4.4);bm(AT(5,'Thanh',.6),true);bm(th,true);
 return{upd:t=>{h1.u(320,520,inn(t,AT(5,'Thanh',.6)-.2,.8));sh(a1,t,320,700,-2,popv(t,AT(5,'Thanh',.6)+.4,.45));h2.u(760,520,inn(t,th-.2,.8));sh(a2,t,760,700,2,popv(t,th+.4,.45));
  const c=inn(t,tm,1.4);const col=`rgb(${Math.round(lerp(150,95,c))},${Math.round(lerp(110,179,c))},${Math.round(lerp(60,230,c))})`;rv.forEach((e,i)=>{let d='';for(let x=40;x<=1040;x+=16)d+=(x==40?'M':'L')+x+' '+(900+i*34+Math.sin(x*.02+t*2+i)*10).toFixed(1);e.setAttribute('d',d);e.setAttribute('stroke',col);e.setAttribute('opacity',inn(t,R(5)+.2,.5))});
  pp.forEach((p,i)=>{p.set(c>.5?{aR1:150+Math.sin(t*5+i)*20,aR2:20,aL1:-150-Math.sin(t*5+i)*20,aL2:-20}:{});p.at(380+i*320,1230,.6,inn(t,R(5)+.3,.5))});sh(B,t,540,1110,1,popv(t,tm,.5))}}});
// 6 năm 1469: vua Lê Thánh Tông ra chiếu đổi tên thành Thanh Hoa; chữ Hoa là tốt đẹp, rực rỡ
S2(6,6,'p',t=>'1469',g=>{const th=THRONE(g);const k=STK(g,{crown:true,robe:'#a8302a'});const ch=CHIEU(g,'THANH HOA',420);const A=strip('VUA LÊ THÁNH TÔNG',false,42,61);const h=HANW(g,'華',150);const B=strip('HOA = TỐT ĐẸP, RỰC RỠ',true,38,62);const sp=[...Array(8)].map(()=>el(g,'path',{d:'M0 -16 L4 -4 L16 0 L4 4 L0 16 L-4 4 L-16 0 L-4 -4Z',fill:CGOLD,stroke:'#fff','stroke-width':3}));const tf=AT(6,'Thanh',3.2),th2=AT(6,'Hoa',4.4);bm(tf);
 return{upd:t=>{sh(A,t,540,320,-2,PV(t,6,'vua',1.4));PUT(th,240,900,popv(t,R(6)+.1,.5),.85,0);k.at(240,840,.85,popv(t,R(6)+.2,.5));k.set({lL1:80,lL2:-80,lR1:80,lR2:-80,aR1:100+Math.sin(t*2.4)*10,aR2:-10,aL1:-30,aL2:-40});
  ch.u(t,680,520,inn(t,tf-.7,.7),tf,.85);h.u(700,800,inn(t,th2-.2,.8),.9);sp.forEach((e,i)=>{const a=i/8*Math.PI*2+t*.6,r=120+Math.sin(t*3+i)*10;PUT(e,700+Math.cos(a)*r,800+Math.sin(a)*r*.7,popv(t,th2+.5+i*.05,.3),1,t*60)});sh(B,t,700,1010,1,popv(t,th2+.3,.5))}}});
// 7 Thanh Hoa dùng suốt thời Lê sang thời Nguyễn: đoàn người que nối nhau cầm biển tên đi qua thời gian
S2(7,7,'d',null,g=>{const bar=el(g,'path',{d:'M100 1000 L980 1000',stroke:'#c9b48a','stroke-width':10,'stroke-linecap':'round'});const d1=CARD(g,'THỜI LÊ','#7a5a32',260),d2=CARD(g,'THỜI NGUYỄN','#7a5a32',300);const pp=[0,1,2].map(i=>STK(g,{col:'#f2ead6',oc:OLN,hat:['#a8302a',CGOLD,'#c9b48a'][i],w:10}));const sign=strip('THANH HOA',true,40,71);const tn=AT(7,'Nguyễn',3.6);bm(tn,true);
 return{upd:t=>{putC(d1,250,580,popv(t,AT(7,'Lê',2.2)-.2,.45));putC(d2,820,580,popv(t,tn-.2,.45));bar.setAttribute('opacity',inn(t,R(7),.4));const u=inn(t,R(7)+.1,E(7)-R(7));
  pp.forEach((p,i)=>{p.set(Object.assign(WALK(t+i*.5,7),i==1?{aR1:160,aR2:0}:{}));p.at(lerp(80,760,u)+i*130,1000,.7,inn(t,R(7)+.1,.4))});sh(sign,t,lerp(80,760,u)+130+10,700+Math.sin(t*7)*4,0,inn(t,R(7)+.1,.4))}}});
// 8 vua Thiệu Trị lên ngôi; mẹ vua là bà Hồ Thị Hoa
S2(8,8,'p',null,g=>{const th=THRONE(g);const k=STK(g,{crown:true,robe:CGOLD});const mo=STK(g,{bun:true,robe:'#7a5a8a'});const A=strip('VUA THIỆU TRỊ LÊN NGÔI',false,42,81);const c=CARD(g,'BÀ HỒ THỊ HOA',CSTEEL,420);const rg=RINGS(g,CRED,3);const tl=AT(8,'lên',1.8),th2=AT(8,'Hồ',4.0);bm(AT(8,'Thiệu',.9));bm(th2,true);
 return{upd:t=>{sh(A,t,540,320,-2,PV(t,8,'Thiệu',.9));PUT(th,360,960,popv(t,R(8)+.1,.5),.95,0);const up=inn(t,tl-.4,.8);k.at(lerp(140,360,up),lerp(1160,900,up),.9,popv(t,R(8)+.1,.4));k.set(up<1?WALK(t,8):{lL1:80,lL2:-80,lR1:80,lR2:-80,aR1:30,aL1:-30});
  mo.at(720,1180,.85,popv(t,th2-.4,.5));mo.set({aR1:-20,aL1:20,tilt:Math.sin(t*1.5)*5});putC(c,720,640,popv(t,th2-.2,.5));RU(rg,t,90,860,640,inn(t,th2+.4,.4))}}});
// 9 lệ kiêng tên: viên quan định viết rồi khựng lại, người định nói thì bịt miệng
S2(9,9,'d',null,g=>{const sc=SCRL(g,420,320);const bl=[0,1].map(()=>el(g,'rect',{width:150,height:28,rx:6,fill:CRED,stroke:'#fff','stroke-width':4}));const of=STK(g,{col:'#f2ead6',oc:OLN,hat:'#2a2a2a',w:10});const br=BRUSH(of.hand);br.setAttribute('transform','rotate(180) translate(0,-10)');const sp=STK(g,{col:'#f2ead6',oc:OLN,hat:'#c9b48a',w:10});const x1=XX(g);
 const A=strip('LỆ KIÊNG TÊN',true,50,91),B=strip('KHÔNG VIẾT, KHÔNG ĐỌC THẲNG',false,38,92);const tk=AT(9,'không',3.6),tv=AT(9,'viết',4.4),td=AT(9,'đọc',5.0);bm(AT(9,'kiêng',.8));bm(tk,true);
 return{upd:t=>{sh(A,t,540,320,-2,PV(t,9,'kiêng',.8));PUT(sc,540,640+Math.sin(t*1.4)*5,popv(t,R(9)+.1,.5),.95,-2);bl.forEach((b,i)=>{const v=inn(t,tv+i*.3,.3);b.setAttribute('x',450+i*30);b.setAttribute('y',590+i*80);b.setAttribute('opacity',v);b.setAttribute('width',150*v)});
  of.at(260,1180,.8,popv(t,R(9)+.3,.5));const stop=inn(t,tv,.3);of.set({aR1:lerp(70,20,stop)+(stop<.5?Math.sin(t*12)*10:0),aR2:lerp(30,60,stop),aL1:-20,lean:lerp(10,-6,stop)});
  sp.at(820,1180,.8,popv(t,R(9)+.4,.5));const sh2=inn(t,td,.3);sp.set({aR1:lerp(20,150,sh2),aR2:lerp(0,120,sh2),aL1:-20});PUT(x1,820,1180-0.8*170,popv(t,td+.2,.35),.35,0);sh(B,t,540,860,1,popv(t,tk,.5))}}});
// 10 chữ Hoa gặp rắc rối: viên quan gãi đầu, vò giấy ném đi, viết chệch
S2(10,10,'p',null,g=>{const dk=DESK(g);const of=STK(g,{hat:'#2a2a2a'});const dc=SCRL(g,440,280);const w1=MLB(g,'TỈNH THANH',40,'#3a2a14','#e8dcba'),w2=MLB(g,'HOA',40,CRED,'#e8dcba');const x1=XX(g);const balls=[0,1,2].map(()=>PAPERBALL(g));const bb=bubble(g,170,110,'?',80);
 const A=strip('CHỮ HOA GẶP RẮC RỐI',true,44,101),B=strip('GIẤY TỜ PHẢI VIẾT CHỆCH',false,40,102);const tr=AT(10,'rắc',1.6),tg=AT(10,'giấy',3.4);bm(tr);
 return{upd:t=>{sh(A,t,540,320,-2,popv(t,tr,.5));const e=popv(t,R(10)+.1,.5);PUT(dc,540,560,e,1,-3);[w1,w2].forEach((w,i)=>{w.setAttribute('x',i?660:450);w.setAttribute('y',570);w.setAttribute('opacity',e)});PUT(x1,660,555,popv(t,tr+.3,.4),.6,0);
  PUT(dk,600,1190,e,1,0);of.at(420,1190,.9,e);const scr=inn(t,tr,.3)*(1-inn(t,tg,.3));of.set(scr>0?{aR1:150,aR2:120+Math.sin(t*16)*15,aL1:-20,tilt:-8}:{aR1:60+Math.sin(t*10)*10*inn(t,tg,.3),aR2:40,aL1:-30,aL2:30,lean:6});bb.at(300,820,.75,popv(t,tr+.2,.5)*(1-inn(t,tg,.3)));
  balls.forEach((b,i)=>{const t0=tg+.3+i*.55,u=cl((t-t0)/.8);PUT(b,lerp(470,880+i*50,u),lerp(1040,1210,u)-Math.sin(u*Math.PI)*220,u>0?1:0,1,u*360)});sh(B,t,540,880,1,popv(t,tg,.5))}}});
// 11 năm 1843: vua Thiệu Trị ra chiếu đổi hẳn thành tỉnh Thanh Hóa; dấu sắc bay về chỗ cũ
S2(11,11,'d',t=>'1843',g=>{const th=THRONE(g);const k=STK(g,{crown:true,robe:CGOLD,col:'#f2ead6',oc:OLN});const ch=CHIEU(g,'TỈNH THANH HOA',480);const ac=ACC(g);const A=strip('VUA THIỆU TRỊ',false,42,111);const st=stamp('LẤY LẠI TÊN CỔ',54);const tf=AT(11,'tỉnh',3.0),tc=AT(11,'cổ',6.0);bm(tf);bm(tc,true);
 return{upd:t=>{sh(A,t,540,320,-2,PV(t,11,'vua',1.0));PUT(th,230,900,popv(t,R(11)+.1,.5),.85,0);k.at(230,840,.85,popv(t,R(11)+.2,.5));k.set({lL1:80,lL2:-80,lR1:80,lR2:-80,aR1:105+Math.sin(t*2.2)*10,aR2:-10,aL1:-30,aL2:-40});
  ch.u(t,680,560,inn(t,tf-.8,.7),tf+.6,.85);const ch2=inn(t,tf+.2,.6);const tx=ch.k.querySelector('text');if(tx)tx.textContent=ch2>.9?'TỈNH THANH HÓA':'TỈNH THANH HOA';
  const ax=lerp(1000,680+150,ch2),ay=lerp(260,560+30,ch2)-Math.sin(ch2*Math.PI)*120;PUT(ac,ax,ay,popv(t,tf-.4,.4)*(1-inn(t,tf+.8,.2)),.9,Math.sin(t*6)*15*(1-ch2));const su=popv(t,tc-.6,.45);st.at(680,860,-5,su,su>0?1:0)}}});
// 12 tên đầu tiên quay lại sau hơn 370 năm: dấu sắc chạy theo vòng cung trên trục thời gian
S2(12,12,'p',null,g=>{const ys=[['1029','THANH HÓA',CGOLD],['1469','THANH HOA',CRED],['1843','THANH HÓA',CGOLD]];const L=el(g,'path',{d:'M180 760 L900 760',stroke:'#c9b48a','stroke-width':8,'stroke-linecap':'round'});const dots=ys.map(()=>el(g,'circle',{r:16,fill:'#fff',stroke:OLN,'stroke-width':5}));const yl=ys.map(y=>MLB(g,y[0],40,'#3a2a14','#efe8d2'));const nl=ys.map(y=>MLB(g,y[1],30,'#fff',y[2]));
 const arc=el(g,'path',{d:'M180 700 Q540 480 900 700',fill:'none',stroke:CGOLD,'stroke-width':10,'stroke-dasharray':'1 1',pathLength:1,'stroke-dashoffset':1,'stroke-linecap':'round'});const ac=ACC(g);const kid=STK(g,{hat:CGOLD});const A=strip('QUAY TRỞ LẠI',true,48,121),B=strip('SAU HƠN 370 NĂM VẮNG BÓNG',false,38,122);const tq=AT(12,'quay',2.4);bm(tq);
 return{upd:t=>{const e=popv(t,R(12)+.05,.5);L.setAttribute('opacity',e);ys.forEach((y,i)=>{const x=180+i*360,v=popv(t,R(12)+.15+i*.2,.4);dots[i].setAttribute('cx',x);dots[i].setAttribute('cy',760);dots[i].setAttribute('opacity',v);yl[i].setAttribute('x',x);yl[i].setAttribute('y',840);yl[i].setAttribute('opacity',v);nl[i].setAttribute('x',x);nl[i].setAttribute('y',900);nl[i].setAttribute('opacity',v)});
  const u=inn(t,tq,1.4);arc.setAttribute('stroke-dashoffset',1-u);const bx=(1-u)*(1-u)*180+2*(1-u)*u*540+u*u*900,by=(1-u)*(1-u)*700+2*(1-u)*u*480+u*u*700;PUT(ac,bx,by-30,popv(t,tq-.2,.3),1,Math.sin(t*6)*15);
  kid.at(900,1200,.8,popv(t,tq+1.2,.5));kid.set({aR1:160+Math.sin(t*8)*15,aR2:10,aL1:-160-Math.sin(t*8)*15,aL2:-10,lL1:-14,lR1:14});sh(A,t,540,400,-2,popv(t,tq,.5));sh(B,t,540,1060,1,PV(t,12,'sau',3.6))}}});
// 13 từ đó không đổi; 2025 Thanh Hóa giữ nguyên
S2(13,13,'d',t=>'2025',g=>{const m=vnmap(940,860,131);const hs=hsts(m);const lab=MLB(m.top,'THANH HÓA',44,'#fff',OLN);const A=strip('TỪ ĐÓ KHÔNG ĐỔI NỮA',false,40,131);const st=stamp('GIỮ NGUYÊN',60);const SH=SEAH();const tg=AT(13,'giữ',6.6);bm(tg);const fl=[0,1,2].map(()=>el(m.top,'path',{fill:CRED,stroke:'#fff','stroke-width':3}));
 return{upd:t=>{const e=inn(t,R(13)-.2,.5);m.at(540,760,0,1,e);m.view(106.2,19.6,lerp(210,170,inn(t,R(13),E(13)-R(13))));seaH(SH,t,e);hs(e);m.hi('Thanh Hóa',e,CGOLD);const[x,y]=m.P(105.3,20.0);lab.setAttribute('x',x);lab.setAttribute('y',y);lab.setAttribute('opacity',e);
  [[105.0,19.95],[105.6,19.6],[105.3,20.3]].forEach((p,i)=>{const[fx,fy]=m.P(...p);const w=Math.sin(t*5+i)*5;fl[i].setAttribute('d',`M${fx} ${fy} L${fx} ${fy-50} L${fx+34} ${fy-42+w} L${fx} ${fy-32}`);fl[i].setAttribute('opacity',popv(t,tg-.4+i*.15,.4))});
  sh(A,t,540,330,-2,PV(t,13,'Từ',.2));const su=popv(t,tg,.45);st.at(540,1030,-5,su,su>0?1:0)}}});
// 14 thầy giáo chỉ bảng: Thanh Hóa là tên gốc, Thanh Hoa đến sau
S2(14,14,'p',null,g=>{const bd=el(g,'rect',{x:300,y:440,width:620,height:520,rx:14,fill:'#1f3a2e',stroke:'#8a5a32','stroke-width':14});const a=CARD(g,'THANH HÓA',CGOLD,400),b=CARD(g,'THANH HOA',CRED,400);const la=strip('TÊN GỐC · 1029',true,34,141),lb=strip('ĐẾN SAU · 1469',false,34,142);const ck=CK(g);const te=STK(g,{hat:'#2a2a2a'});const A=strip('KHÔNG PHẢI VIẾT SAI',false,40,143);const ts=AT(14,'sau',4.0);bm(AT(14,'sai',1.6),true);bm(ts);
 return{upd:t=>{bd.setAttribute('opacity',popv(t,R(14),.4));putC(a,610,570,popv(t,R(14)+.05,.5));sh(A,t,540,330,-2,PV(t,14,'sai',1.6));PUT(ck,860,560,popv(t,ts,.4),.5,0);sh(la,t,610,680,-1,popv(t,ts,.45));putC(b,610,810,popv(t,AT(14,'Thanh',2.6),.5));sh(lb,t,610,920,1,popv(t,ts+.2,.45));
  te.at(180,1200,.95,popv(t,R(14)+.1,.5));const pt=inn(t,ts,.3);te.set({aR1:lerp(120,95,pt)+Math.sin(t*4)*6,aR2:lerp(-30,-10,pt),aL1:-20,lean:4})}}});
// 15 câu hỏi: tỉnh nào khác từng đổi tên vì kiêng tên vua?
S2(15,15,'d',null,g=>{const m=vnmap(560,820,151);const hs=hsts(m);const qs=[[105.85,21.0],[106.68,20.86],[107.6,16.4],[108.2,16.05],[106.7,10.8],[105.75,10.05],[105.7,18.7],[108.95,13.8]].map(()=>T(m.top,0,0,'?',44,CGOLD,6,'middle',OLN));const A=strip('TỈNH NÀO KHÁC?',true,44,151),B=strip('ĐỔI TÊN VÌ KIÊNG TÊN VUA',false,32,152);const kid=STK(g,{col:'#f2ead6',oc:OLN,hat:CGOLD,w:10});const tq=AT(15,'tỉnh',1.0);bm(tq);
 return{upd:t=>{const e=inn(t,R(15)-.2,.5);m.at(330,740,-1,1,e);m.view(108.6,15.9,44);hs(e);m.hi('Thanh Hóa',e,CGOLD);const P0=[[105.85,21.0],[106.68,20.86],[107.6,16.4],[108.2,16.05],[106.7,10.8],[105.75,10.05],[105.7,18.7],[108.95,13.8]];qs.forEach((q,i)=>{const[x,y]=m.P(...P0[i]);q.setAttribute('x',x);q.setAttribute('y',y+14+Math.sin(t*3+i)*5);q.setAttribute('opacity',popv(t,tq+.2+i*.15,.4))});
  sh(A,t,790,560,-2,popv(t,tq,.5));sh(B,t,780,650,2,PV(t,15,'kiêng',2.4));kid.at(800,1150,.85,popv(t,tq+.3,.5));kid.set({aR1:150,aR2:110+Math.sin(t*14)*14,aL1:-20,tilt:-8})}}},9999);
