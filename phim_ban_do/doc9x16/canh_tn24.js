// ===== TÊN TỈNH THÀNH #24: Quảng Ngãi (tn24). Bản đồ hành chính phẳng 34 tỉnh (geoBoundaries, phạm vi công cộng), không vẽ nước láng giềng; ranh giới tỉnh trước 2025 vẽ nét đứt.
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
// ===== Dấu ấn riêng (Quảng Ngãi): nền xanh đêm, giấy kem; dáng núi Ấn đỉnh bằng và đảo Lý Sơn ở đáy, sóng sông Trà (y>1650), bụi sáng trôi
{DR1.setAttribute('opacity',0);DR2.setAttribute('opacity',0);
 DARKG.firstChild.setAttribute('fill','#111a22');
 [...PAPG.children].forEach(c=>{if(c.tagName=='g')c.setAttribute('opacity',0);if(c.tagName=='line')c.setAttribute('stroke','rgba(0,0,0,0)')});
 PAPG.firstChild.setAttribute('fill','#f1ecdc');
 const sky=(p,col)=>{const g=el(p,'g',{});const L=(d,w=5)=>el(g,'path',{d,fill:'none',stroke:col,'stroke-width':w,'stroke-linejoin':'round','stroke-linecap':'round'});
  L('M40 1630 L150 1560 L230 1530 L330 1530 L420 1575 L520 1630',5);   // núi Ấn đỉnh bằng
  L('M640 1630 Q700 1590 760 1600 Q800 1560 860 1575 Q930 1585 980 1630',4);   // đảo Lý Sơn
  L('M820 1578 L840 1548 L860 1578',3);
  return g};
 const skA=sky(DARKG,'rgba(150,190,220,.16)'),skB=sky(PAPG,'rgba(70,100,130,.16)');
 const fr=(p,col)=>{const r=rng(241);return[...Array(16)].map(()=>({e:el(p,'circle',{r:6,fill:col}),x:30+r()*1020,y:230+r()*1000,ph:r()*6}))};
 const pA=fr(DARKG,'rgba(150,200,230,.22)'),pB=fr(PAPG,'rgba(80,120,150,.20)');
 const wv=(p,col)=>[0,1,2].map(i=>el(p,'path',{fill:'none',stroke:col,'stroke-width':4+i,opacity:.55-i*.12}));
 const wA=wv(DARKG,'rgba(110,170,210,.40)'),wB=wv(PAPG,'rgba(60,110,150,.24)');
 window.THEME_UPD=t=>{const dx=Math.sin(t*.09)*12;skA.setAttribute('transform',`translate(${dx.toFixed(1)},0)`);skB.setAttribute('transform',`translate(${dx.toFixed(1)},0)`);
  [pA,pB].forEach(P=>P.forEach(o=>{o.e.setAttribute('cx',(o.x+Math.sin(t*1.1+o.ph)*10).toFixed(1));o.e.setAttribute('cy',(o.y-((t*14+o.ph*40)%60)).toFixed(1))}));
  [wA,wB].forEach(L=>L.forEach((e,i)=>{const y0=1690+i*62;let d='';for(let x=-20;x<=1100;x+=28){const y=y0+Math.sin(x*.011+t*(1.1+i*.35)+i)*9;d+=(x<0?'M':'L')+x+' '+y.toFixed(1)}e.setAttribute('d',d)}))};
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
const TILE2=(g,txt,col=CGOLD,w=300)=>{const k=el(g,'g',{});el(k,'rect',{x:-w/2,y:-62,width:w,height:124,rx:18,fill:col,stroke:'#fff','stroke-width':8});const t=T(k,0,28,txt,Math.min(78,Math.floor(w*1.5/txt.length)),'#fff',8,'middle',OLN);t.setAttribute('font-weight',900);return k};
const MLINE=(m,pts,col=CGOLD,wd=10)=>{const d='M'+pts.map(p=>p[0]+' '+(-p[1]*KYP).toFixed(3)).join('L');const e=el(m.riv,'path',{d,fill:'none',stroke:col,'stroke-width':wd,'vector-effect':'non-scaling-stroke','stroke-linecap':'round','stroke-linejoin':'round',pathLength:1,'stroke-dasharray':'1 1','stroke-dashoffset':1});return u=>{e.setAttribute('stroke-dashoffset',1-cl(u));e.setAttribute('opacity',u>0?1:0)}};
const OLD=(m,names,fill='none')=>names.map(n=>{const p=TINH63.find(q=>q.n==n);return el(m.riv,'path',{d:p.p.map(rpath).join(''),fill,stroke:'#fff8e6','stroke-width':3,'stroke-dasharray':'10 8','vector-effect':'non-scaling-stroke',opacity:0})});
const PIN=(m,txt,col=CRED,dy=-28,sz=30)=>{const k=el(m.top,'g',{});el(k,'circle',{r:13,fill:col,stroke:'#fff','stroke-width':5});const t=MLB(k,txt,sz,'#fff');t.setAttribute('y',dy);return k};
const PINAT=(m,k,p,u,dx=0,dy=0)=>{const[x,y]=m.P(...p);k.setAttribute('transform',`translate(${x+dx},${y+dy}) scale(${Math.max(.001,u)})`);k.setAttribute('opacity',u>0?1:0)};
const labAt=(m,e,p,op,dy=0)=>{const[x,y]=m.P(...p);e.setAttribute('x',x);e.setAttribute('y',y+dy);e.setAttribute('opacity',op)};
const HOUSE=(g,col='#3f7a5a')=>{const k=el(g,'g',{});el(k,'rect',{x:-90,y:-70,width:180,height:80,fill:'#8a6a44',stroke:'#fff','stroke-width':5});el(k,'path',{d:'M-120 -60 L0 -150 L120 -60Z',fill:col,stroke:'#fff','stroke-width':6,'stroke-linejoin':'round'});el(k,'rect',{x:-22,y:-46,width:44,height:56,fill:'#3a2414',stroke:'#fff','stroke-width':4});return k};
const PINE=(g,s=1,col='#3f7a5a')=>{const k=el(g,'g',{transform:`scale(${s})`});el(k,'rect',{x:-7,y:-20,width:14,height:30,fill:'#6a4a2a'});for(let i=0;i<3;i++)el(k,'path',{d:`M-${46-i*10} ${-16-i*34} L0 ${-70-i*34} L${46-i*10} ${-16-i*34}Z`,fill:col,stroke:'#fff','stroke-width':4,'stroke-linejoin':'round'});return k};
const MTN=(g,w=520,col='#5a7a6a')=>{const k=el(g,'g',{});el(k,'path',{d:`M${-w/2} 0 L${-w*.18} ${-w*.52} L${-w*.02} ${-w*.3} L${w*.16} ${-w*.62} L${w/2} 0Z`,fill:col,stroke:'#fff','stroke-width':7,'stroke-linejoin':'round'});el(k,'path',{d:`M${w*.08} ${-w*.48} L${w*.16} ${-w*.62} L${w*.25} ${-w*.47} L${w*.18} ${-w*.43} L${w*.14} ${-w*.5}Z`,fill:'#f2f2ea'});return k};
const SIGNP=(st,txt,col=CGOLD)=>{const k=el(st.hand,'g',{});el(k,'path',{d:'M0 0 L0 -90',stroke:'#7a4a22','stroke-width':7});el(k,'rect',{x:-80,y:-140,width:160,height:56,rx:8,fill:col,stroke:'#fff','stroke-width':5});const t=MLB(k,txt,30,'#fff',col);t.setAttribute('y',-102);k.fix=(r,fl=1)=>k.setAttribute('transform',`rotate(${-r}) scale(${fl},1)`);return k};
const SEAL=(g,col=CSTEEL)=>{const k=el(g,'g',{});el(k,'rect',{x:-14,y:-70,width:28,height:50,rx:6,fill:'#7a4a22'});el(k,'rect',{x:-36,y:-24,width:72,height:30,rx:6,fill:CRED,stroke:'#fff','stroke-width':4});return k};

const SCISS=(g)=>{const k=el(g,'g',{});const a=el(k,'g',{}),b=el(k,'g',{});[a,b].forEach((s,i)=>{el(s,'path',{d:'M0 0 L70 -8 L70 8Z',fill:'#cfd6dc',stroke:OLN,'stroke-width':4});el(s,'circle',{cx:-22,cy:i?14:-14,r:14,fill:'none',stroke:CRED,'stroke-width':8})});return{k,u:(x,y,o,s=1)=>{k.setAttribute('transform',`translate(${x},${y}) scale(${s})`);k.setAttribute('opacity',s>0?1:0);a.setAttribute('transform',`rotate(${-o})`);b.setAttribute('transform',`rotate(${o})`)}}};
// ===== CẢNH tn24 Quảng Ngãi (vẽ phẳng, người que, bản đồ hành chính phẳng 34 tỉnh; ranh giới trước 2025 nét đứt)
const QNc=[108.8,15.12],LS=[109.12,15.38],KTc=[108.0,14.35],BDc=[109.0,14.1];
const pv63=(m,n,col)=>{const p=TINH63.find(q=>q.n==n);return el(m.riv,'path',{d:p.p.map(rpath).join(''),fill:col,stroke:'#fff8e6','stroke-width':3,'stroke-dasharray':'10 8','vector-effect':'non-scaling-stroke',opacity:0})};
const MAPY=(id)=>{const m=vnmap(940,860,id);return{m,hs:hsts(m),SH:SEAH()}};
const MON=(Q,t,n,z0,z1,c)=>{const e=inn(t,R(n)-.2,.5);Q.m.at(540,760,0,1,e);Q.m.view(c[0],c[1],lerp(z0,z1,inn(t,R(n),E(n)-R(n))));seaH(Q.SH,t,e);Q.hs(e);return e};
const CNT=(g,col=CGOLD,sz=96)=>{const n=T(g,0,0,'0',sz,col,10,'middle',OLN);n.setAttribute('font-weight',900);return n};
const NGHIA=(g,sz=150)=>{const k=el(g,'g',{});el(k,'circle',{r:sz*.78,fill:'rgba(224,166,60,.16)',stroke:CGOLD,'stroke-width':8});HAN(k,'義',sz);return k};
const ARR=(g)=>el(g,'path',{d:'M-40 0 L30 0 M10 -22 L34 0 L10 22',fill:'none',stroke:'#fff','stroke-width':10,'stroke-linecap':'round','stroke-linejoin':'round'});

// 1 hook: tên chữ của Quảng Ngãi vốn là Quảng Nghĩa, có lúc tỉnh còn mang tên một con người
S2(1,1,'d',null,g=>{const a=TILE2(g,'QUẢNG NGÃI',CGOLD,440);const hw=el(g,'g',{});HAN(hw,'廣義',170);const b=TILE2(g,'QUẢNG NGHĨA',CSTEEL,460);const st=STK(g,{col:OLN});const q=T(g,0,0,'?',150,CRED,12,'middle',OLN);const A=strip('TÊN CHỮ LÀ GÌ?',true,44,11),B=strip('CÓ LÚC MANG TÊN MỘT NGƯỜI',false,34,12);const t0=AT(1,'Quảng',.1),tn=AT(1,'Nghĩa',1.8),tp=AT(1,'người',4.6);bm(t0,true);bm(tn);bm(tp,true);
 return{upd:t=>{PUT(a,540,360,popv(t,t0,.4),1,Math.sin(t*2)*1.5);sh(A,t,540,500,-2,popv(t,t0+.4,.4)*(1-inn(t,tn,.3)));PUT(hw,540,700,popv(t,tn-.3,.45),1,Math.sin(t*1.6)*2);PUT(b,540,900,popv(t,tn,.45),1,-Math.sin(t*2)*1.5);
  const u=popv(t,tp-.2,.4);st.set({...WALK(t,3),aR1:120+Math.sin(t*4)*10});st.at(400,1270,1.1*u,u>0?1:0);PUT(q,600,1080+Math.sin(t*3)*10,popv(t,tp,.4),1,Math.sin(t*4)*6);sh(B,t,540,1300,2,popv(t,tp+.2,.45))}}});
// 2 chữ Nghĩa đi theo vùng đất này từ thời Lê, khi đây là phủ Tư Nghĩa của thừa tuyên Quảng Nam
S2(2,2,'p',null,g=>{const hw=HANW(g,'義',190);const ring=el(g,'circle',{r:150,fill:'none',stroke:CGOLD,'stroke-width':8});const A=strip('THỜI LÊ',false,44,21);const c=CARD(g,'PHỦ TƯ NGHĨA',CGOLD,460);const d=CARD(g,'THỪA TUYÊN QUẢNG NAM',CSTEEL,560);const tc=AT(2,'Chữ',.1),tl=AT(2,'Lê',2.4),tp=AT(2,'phủ',3.6),tq=AT(2,'thừa',5.0);bm(tc,true);bm(tp);
 return{upd:t=>{hw.u(540,560,inn(t,tc,1.2),1);ring.setAttribute('cx',540);ring.setAttribute('cy',600);ring.setAttribute('opacity',inn(t,tc+1,.4)*(.6+.4*Math.sin(t*3)));sh(A,t,540,330,-2,popv(t,tl,.45));putC(c,540,930+Math.sin(t*2)*6,popv(t,tp,.45),-2);putC(d,540,1110-Math.sin(t*2)*6,popv(t,tq,.45),2)}}});
// 3 Tây Sơn đổi thành Hòa Nghĩa; đầu thời Nguyễn Gia Long đặt dinh Quảng Nghĩa, rồi trấn Quảng Nghĩa (thang tên, chữ Nghĩa luôn sáng)
S2(3,3,'d',null,g=>{const L=[['TƯ NGHĨA',CSTEEL],['HÒA NGHĨA',CSTEEL],['DINH QUẢNG NGHĨA',CGOLD],['TRẤN QUẢNG NGHĨA',CGOLD]].map(([s,c])=>CARD(g,s,c,s.length*22+90));const lb=[strip('THỜI LÊ',false,28,31),strip('TÂY SƠN',false,28,32),strip('GIA LONG',false,28,33),strip('SAU ĐÓ',false,28,34)];const ln=el(g,'path',{fill:'none',stroke:'#fff','stroke-width':6,'stroke-dasharray':'12 10'});const nh=NGHIA(g,90);
 const T0=[R(3)+.1,AT(3,'Hòa',1.6),AT(3,'dinh',4.6),AT(3,'trấn',6.6)];bm(T0[1]);bm(T0[2],true);bm(T0[3]);
 return{upd:t=>{let j=0;T0.forEach((tk,i)=>{if(t>tk)j=i});L.forEach((c,i)=>{putC(c,600,420+i*230,popv(t,T0[i],.4)*(i==j?1.05+.03*Math.sin(t*5):.85),i==j?Math.sin(t*3)*2:0);sh(lb[i],t,200,420+i*230,-4,popv(t,T0[i]+.1,.4))});ln.setAttribute('d',`M600 420 L600 ${420+lerp(0,690,inn(t,T0[1],T0[3]-T0[1]+.4))}`);ln.setAttribute('stroke-dashoffset',-t*30);PUT(nh,930,300,popv(t,R(3)+.3,.4),1,Math.sin(t*2)*4)}}});
// 4 năm 1832 vua Minh Mạng đổi trấn thành tỉnh; trên giấy tờ triều đình tên tỉnh vẫn là Quảng Nghĩa
S2(4,4,'p',t=>'1832',g=>{const ch=CHIEU(g,'TỈNH QUẢNG NGHĨA',600);const A=strip('ĐỔI TRẤN THÀNH TỈNH',false,40,41),B=strip('VẪN LÀ QUẢNG NGHĨA',true,42,42);const nh=NGHIA(g,80);const tv=AT(4,'vua',.8),td=AT(4,'đổi',2.2),tg=AT(4,'giấy',3.6),tq=AT(4,'Quảng',5.2);bm(td,true);bm(tq);
 return{upd:t=>{sh(A,t,540,340,-2,popv(t,tv,.45));ch.u(t,540,760,inn(t,td,.9),tq,1.1);sh(B,t,540,1080,2,popv(t,tq,.45));PUT(nh,880,560,popv(t,tq+.2,.4),1,Math.sin(t*3)*5)}}});
// 5 sang thời Pháp thuộc, tên tỉnh được gọi là Quảng Ngãi; vì sao Nghĩa thành Ngãi, tài liệu chính thức không chép rõ
S2(5,5,'d',null,g=>{const a=TILE2(g,'NGHĨA',CSTEEL,300),b=TILE2(g,'NGÃI',CGOLD,300);const ar=ARR(g);const q=T(g,0,0,'?',220,CRED,14,'middle',OLN);const A=strip('THỜI PHÁP THUỘC: QUẢNG NGÃI',false,36,51),B=strip('KHÔNG CHÉP RÕ LÝ DO',true,40,52);const tp=AT(5,'Pháp',1.2),tn=AT(5,'Ngãi',3.0),tv=AT(5,'Vì',4.0),tk=AT(5,'không',6.6);bm(tn,true);bm(tk);
 return{upd:t=>{sh(A,t,540,340,-2,popv(t,tp,.45));PUT(a,280,700,popv(t,tp+.3,.4),1,-3);PUT(ar,540,700,popv(t,tn-.2,.4),1.4+.1*Math.sin(t*6),0);PUT(b,800,700,popv(t,tn,.45),1+.04*Math.sin(t*4),3);PUT(q,540,1000+Math.sin(t*3)*12,popv(t,tv,.4),1,Math.sin(t*4)*8);sh(B,t,540,1230,2,popv(t,tk,.5))}}});
// 6 sau Cách mạng tháng Tám, tỉnh có thời gian ngắn mang tên Lê Trung Đình; đầu năm 1946 trở lại tên cũ (biển tên lật)
S2(6,6,'p',t=>t<AT(6,'đầu',5.2)?'1945':'1946',g=>{const s1=SIGN(g,'TỈNH LÊ TRUNG ĐÌNH',CRED),s2=SIGN(g,'TỈNH QUẢNG NGÃI','#1d5a46');const A=strip('MANG TÊN MỘT NGƯỜI',false,40,61);const st=stamp('THỜI GIAN NGẮN',52);const tl=AT(6,'Trung',2.6),tn=AT(6,'ngắn',1.4),td=AT(6,'đầu',5.2);bm(R(6)+.4,true);bm(td);
 return{upd:t=>{const fl=inn(t,td,.6);const sc=Math.cos(fl*Math.PI);const u=popv(t,R(6)+.3,.45);s1.k.setAttribute('transform',`translate(540,760) rotate(${Math.sin(t*2)*2}) scale(${(sc>0?sc:0)*u},${u})`);s1.k.setAttribute('opacity',sc>0&&u>0?1:0);s2.k.setAttribute('transform',`translate(540,760) rotate(${Math.sin(t*2)*2}) scale(${sc<0?-sc:0},1)`);s2.k.setAttribute('opacity',sc<0?1:0);
  sh(A,t,540,340,-2,popv(t,tl-.4,.45));const su=popv(t,tn,.45)*(1-fl);st.at(540,1200,-5,su,su>0?1:0)}}});
// 7 năm 1976 Quảng Ngãi gộp với Bình Định thành tỉnh Nghĩa Bình, chữ Nghĩa lại đứng đầu tên tỉnh
S2(7,7,'d',t=>'1976',g=>{const Q=MAPY(71);const qn=pv63(Q.m,'Quảng Ngãi',CGOLD),bd=pv63(Q.m,'Bình Định',CSTEEL);const la=MLB(Q.m.top,'QUẢNG NGÃI',30,'#fff',OLN),lb=MLB(Q.m.top,'BÌNH ĐỊNH',30,'#fff',OLN),ln=MLB(Q.m.top,'NGHĨA BÌNH',46,'#fff',CRED);const A=strip('CHỮ NGHĨA LẠI ĐỨNG ĐẦU',true,40,71);const tb=AT(7,'Bình',2.2),tn=AT(7,'Nghĩa',3.4),tc=AT(7,'chữ',4.8);bm(tb);bm(tn,true);
 return{upd:t=>{const e=MON(Q,t,7,200,230,[108.85,14.4]);const mg=inn(t,tn,.6);qn.setAttribute('opacity',e*(1-.4*mg));bd.setAttribute('opacity',popv(t,tb,.4)*(1-.4*mg));labAt(Q.m,la,[108.75,15.1],e*(1-mg));labAt(Q.m,lb,[108.95,14.1],popv(t,tb,.45)*(1-mg));labAt(Q.m,ln,[108.9,14.6],popv(t,tn,.45));Q.m.hi('Quảng Ngãi',mg*.6,CGOLD);sh(A,t,540,330,-2,popv(t,tc,.5))}}});
// 8 thị xã từng là tỉnh lỵ của Quảng Ngãi khi ấy vẫn mang tên chính thức thị xã Quảng Nghĩa
S2(8,8,'p',null,g=>{const hs=[0,1,2].map(i=>HOUSE(g,['#3f7a5a','#8a3a2a','#3f5a7a'][i]));const sg=SIGN(g,'THỊ XÃ QUẢNG NGHĨA','#1d5a46');const A=strip('TÊN CHÍNH THỨC',true,42,81);const nh=NGHIA(g,70);const tt=AT(8,'Thị',.1),tc=AT(8,'chính',3.8),tq=AT(8,'Quảng',5.2);bm(tt);bm(tq,true);
 return{upd:t=>{hs.forEach((h,i)=>PUT(h,[260,540,820][i],1180,popv(t,tt+i*.15,.4),.9,0));const u=popv(t,tq-.4,.45);sg.k.setAttribute('transform',`translate(540,${760+Math.sin(t*2)*6}) rotate(${Math.sin(t*1.8)*2}) scale(${u})`);sg.k.setAttribute('opacity',u>0?1:0);sh(A,t,540,360,-2,popv(t,tc,.45));PUT(nh,880,520,popv(t,tq+.3,.4),1,Math.sin(t*3)*5)}}});
// 9 năm 1981 Hội đồng Bộ trưởng chia thị xã thành thị xã Quảng Ngãi và huyện Tư Nghĩa (kéo cắt biển)
S2(9,9,'d',t=>'1981',g=>{const sg=SIGN(g,'THỊ XÃ QUẢNG NGHĨA','#1d5a46');const sc=SCISS(g);const a=CARD(g,'THỊ XÃ QUẢNG NGÃI',CGOLD,470),b=CARD(g,'HUYỆN TƯ NGHĨA',CSTEEL,420);const st=stamp('QUYẾT ĐỊNH 41/HĐBT',44);const th=AT(9,'Hội',1.6),tc=AT(9,'chia',4.0),tq=AT(9,'Quảng',5.0),tt=AT(9,'huyện',6.0)-.2;bm(th,true);bm(tc);bm(tt);
 return{upd:t=>{const cu=inn(t,tc+.2,.5);const u=popv(t,R(9)+.1,.4)*(1-cu);sg.k.setAttribute('transform',`translate(540,640) scale(${u})`);sg.k.setAttribute('opacity',u>0?1:0);sc.u(540,600,Math.abs(Math.sin(t*14))*22,popv(t,tc-.4,.3)*(1-inn(t,tc+.6,.3)));putC(a,lerp(540,300,cu),lerp(640,900,cu),popv(t,tq,.45),-3+Math.sin(t*3)*2);putC(b,lerp(540,790,cu),lerp(640,1060,cu),popv(t,tt,.45),3-Math.sin(t*3)*2);const su=popv(t,th,.45);st.at(540,350,-5,su,su>0?1:0)}}});
// 10 năm 1989 Nghĩa Bình chia lại; từ ngày 1/7 năm ấy tỉnh Quảng Ngãi được tái lập
S2(10,10,'p',t=>'1989',g=>{const nb=TILE2(g,'NGHĨA BÌNH',CRED,380);const a=TILE2(g,'QUẢNG NGÃI',CGOLD,380),b=TILE2(g,'BÌNH ĐỊNH',CSTEEL,360);const sc=SCISS(g);const n=CNT(g,CGOLD,84);const A=strip('NGÀY 1/7/1989: TÁI LẬP',true,40,101);const tc=AT(10,'chia',1.8),tn=AT(10,'ngày',3.0),tq=AT(10,'Quảng',5.0);bm(tc,true);bm(tq);
 return{upd:t=>{const sp=inn(t,tc,.6);PUT(nb,540,640,popv(t,R(10)+.1,.4)*(1-sp),1,Math.sin(t*3)*2);sc.u(540,700,Math.abs(Math.sin(t*14))*22,popv(t,tc-.4,.3)*(1-inn(t,tc+.4,.3)));PUT(a,lerp(540,290,sp),lerp(640,820,sp),sp,1+.04*Math.sin(t*4)*inn(t,tq,.4),-3);PUT(b,lerp(540,800,sp),lerp(640,820,sp),sp,.9,3);n.textContent=Math.round(13*sp)+' năm gộp';PUT(n,540,1040,popv(t,tc+.2,.4),.7,0);sh(A,t,540,360,-2,popv(t,tn,.5))}}});
// 11 năm 2025 Quảng Ngãi hợp nhất với Kon Tum ở phía tây, vẫn giữ tên Quảng Ngãi
S2(11,11,'d',t=>'2025',g=>{const Q=MAPY(111);const qn=pv63(Q.m,'Quảng Ngãi',CGOLD),kt=pv63(Q.m,'Kon Tum',CSTEEL);const la=MLB(Q.m.top,'QUẢNG NGÃI',30,'#fff',OLN),lb=MLB(Q.m.top,'KON TUM',30,'#fff',OLN),ln=MLB(Q.m.top,'QUẢNG NGÃI',48,'#fff',CRED);const A=strip('VẪN GIỮ TÊN QUẢNG NGÃI',true,40,1101);const tk=AT(11,'Kon',2.6),tg=AT(11,'giữ',4.6);bm(tk);bm(tg,true);
 return{upd:t=>{const e=MON(Q,t,11,230,205,[108.3,14.75]);const mg=inn(t,tg-.2,.6);qn.setAttribute('opacity',e*(1-mg*.5));kt.setAttribute('opacity',popv(t,tk,.4)*(1-mg*.5));labAt(Q.m,la,[108.75,15.05],e*(1-mg));labAt(Q.m,lb,[107.85,14.5],popv(t,tk,.45)*(1-mg));Q.m.hi('Quảng Ngãi',mg*(.8+.2*Math.sin(t*3)),CGOLD);labAt(Q.m,ln,[108.3,14.75],popv(t,tg,.45));sh(A,t,540,330,-2,popv(t,tg,.5))}}});
// 12 chữ Nghĩa vẫn còn trong tên nhiều xã quanh vùng, như xã Tư Nghĩa, xã Nghĩa Hành
S2(12,12,'p',null,g=>{const nh=NGHIA(g,130);const s1=SIGN(g,'XÃ TƯ NGHĨA','#1d5a46'),s2=SIGN(g,'XÃ NGHĨA HÀNH','#1d5a46');const A=strip('CHỮ NGHĨA VẪN CÒN',true,42,121);const tc=AT(12,'Chữ',.1),t1=AT(12,'Tư',3.8),t2=AT(12,'Hành',5.4);bm(tc,true);bm(t1);bm(t2);
 return{upd:t=>{PUT(nh,540,480,popv(t,tc,.45),1+.04*Math.sin(t*3),Math.sin(t*2)*4);sh(A,t,540,300,-2,popv(t,tc+.4,.45));[[s1,t1,300],[s2,t2,790]].forEach(([s,tk,x],i)=>{const u=popv(t,tk-.3,.45);s.k.setAttribute('transform',`translate(${x},${860+i*40}) rotate(${Math.sin(t*2+i)*3}) scale(${u*.9})`);s.k.setAttribute('opacity',u>0?1:0)})}}});
// 13 từ phủ Tư Nghĩa, qua Quảng Nghĩa, đến Quảng Ngãi: một chữ đổi cách gọi, cái tên vẫn theo vùng đất mấy trăm năm
S2(13,13,'d',null,g=>{const L=[['TƯ NGHĨA',CSTEEL],['QUẢNG NGHĨA',CSTEEL],['QUẢNG NGÃI',CGOLD]].map(([s,c])=>TILE2(g,s,c,s.length*26+80));const ar=[ARR(g),ARR(g)];const pin=el(g,'path',{d:'M0 0 C-50 -60 -50 -120 0 -120 C50 -120 50 -60 0 0Z',fill:CRED,stroke:'#fff','stroke-width':7});const A=strip('MỘT CHỮ ĐỔI CÁCH GỌI',true,42,131),B=strip('CÁI TÊN VẪN THEO VÙNG ĐẤT',false,36,132);const T0=[AT(13,'Tư',.6),AT(13,'qua',1.8),AT(13,'đến',3.2)],tc=AT(13,'chữ',4.4),tv=AT(13,'vẫn',6.0);bm(T0[2],true);bm(tc);
 return{upd:t=>{L.forEach((k,i)=>PUT(k,540,420+i*250,popv(t,T0[i],.4),i==2?1+.04*Math.sin(t*4):.85,(i-1)*2));ar.forEach((a,i)=>PUT(a,540,545+i*250,popv(t,T0[i+1]-.2,.3),1,90));sh(A,t,540,1160,-2,popv(t,tc,.5));PUT(pin,880,980,popv(t,tv,.4),.8,Math.sin(t*3)*4);sh(B,t,540,1270,2,popv(t,tv,.5))}}});
// 14 câu hỏi: đảo Lý Sơn, núi Ấn sông Trà
S2(14,14,'p',null,g=>{const sea=el(g,'rect',{x:-420,y:-40,width:840,height:200,rx:20,fill:'#3f6f8f',stroke:'#fff','stroke-width':6});const isl=el(g,'path',{d:'M-160 0 Q-110 -70 -40 -60 Q0 -120 70 -96 Q130 -80 170 0Z',fill:'#5a7a4a',stroke:'#fff','stroke-width':6,'stroke-linejoin':'round'});const mt=el(g,'path',{d:'M-220 0 L-120 -150 L60 -150 L180 0Z',fill:'#4f6f5a',stroke:'#fff','stroke-width':7,'stroke-linejoin':'round'});const rv=el(g,'path',{fill:'none',stroke:'#7fc4ea','stroke-width':14,'stroke-linecap':'round'});
 const A=strip('ĐẢO LÝ SƠN',false,40,141),B=strip('NÚI ẤN SÔNG TRÀ',false,40,142),Q=strip('BẠN ĐÃ ĐẾN CHƯA?',true,42,143);const t1=AT(14,'Lý',1.4),t2=AT(14,'núi',3.0);bm(AT(14,'Bạn',.3));bm(t1);bm(t2,true);
 return{upd:t=>{sh(Q,t,540,330,-2,PV(t,14,'Bạn',.3));PUT(sea,540,640,popv(t,t1-.3,.4),1,0);PUT(isl,540+Math.sin(t*1.5)*6,640,popv(t,t1-.2,.45),1,0);sh(A,t,540,820,2,popv(t,t1,.45));PUT(mt,540,1120,popv(t,t2-.2,.45),1,0);let d='';for(let x=-400;x<=400;x+=20){d+=(x<-399?'M':'L')+(540+x)+' '+(1150+Math.sin(x*.02+t*2)*14).toFixed(1)}rv.setAttribute('d',d);rv.setAttribute('opacity',popv(t,t2,.4));sh(B,t,540,1250,-2,popv(t,t2,.45))}}},9999);
