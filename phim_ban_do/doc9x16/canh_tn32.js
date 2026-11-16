// ===== TÊN TỈNH THÀNH #32: Tuyên Quang (tn32), chibi vẽ bằng code. Bản đồ hành chính phẳng 34 tỉnh (geoBoundaries, phạm vi công cộng), không vẽ nước láng giềng; ranh giới tỉnh trước 2025 vẽ nét đứt.
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
// ===== Dấu ấn riêng (Tuyên Quang): đổi màu nền, họa tiết mờ ở đáy, hạt trôi chậm, sóng nước ở đáy (y>1650)
{DR1.setAttribute('opacity',0);DR2.setAttribute('opacity',0);
 DARKG.firstChild.setAttribute('fill','#121619');
 [...PAPG.children].forEach(c=>{if(c.tagName=='g')c.setAttribute('opacity',0);if(c.tagName=='line')c.setAttribute('stroke','rgba(0,0,0,0)')});
 PAPG.firstChild.setAttribute('fill','#eef0ea');
 const sky=(p,col)=>{const g=el(p,'g',{});const L=(d,w=5)=>el(g,'path',{d,fill:'none',stroke:col,'stroke-width':w,'stroke-linejoin':'round','stroke-linecap':'round'});
  L('M0 1630 L80 1520 L140 1580 L230 1470 L330 1600 L420 1500 L520 1610 L640 1480 L760 1600 L860 1510 L960 1600 L1080 1540',5);
  return g};
 const skA=sky(DARKG,'rgba(220,200,160,.15)'),skB=sky(PAPG,'rgba(90,70,50,.16)');
 const fr=(p,col)=>{const r=rng(271);return[...Array(14)].map(()=>{const e=el(p,'g',{});el(e,'circle',{r:7,fill:col});return{e,x:30+r()*1020,y:230+r()*1000,ph:r()*6}})};
 const pA=fr(DARKG,'rgba(170,200,170,.25)'),pB=fr(PAPG,'rgba(60,100,70,.2)');
 const wv=(p,col)=>[0,1,2].map(i=>el(p,'path',{fill:'none',stroke:col,'stroke-width':4+i,opacity:.55-i*.12}));
 const wA=wv(DARKG,'rgba(110,170,210,.38)'),wB=wv(PAPG,'rgba(60,110,150,.22)');
 window.THEME_UPD=t=>{const dx=Math.sin(t*.09)*12;skA.setAttribute('transform',`translate(${dx.toFixed(1)},0)`);skB.setAttribute('transform',`translate(${dx.toFixed(1)},0)`);
  [pA,pB].forEach(P=>P.forEach(o=>o.e.setAttribute('transform',`translate(${(o.x+Math.sin(t*1.1+o.ph)*10).toFixed(1)},${(o.y+Math.sin(t*.8+o.ph)*14).toFixed(1)})`)));
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
// ===== Chibi vẽ bằng SVG (tự vẽ, không theo mẫu nào): đầu ~ nửa người, mắt to; nhún, chớp mắt, miệng theo lời, vẫy tay, nét mặt
const CNS='http://www.w3.org/2000/svg',COL='#3a2418';
const CE=(p,tag,a={})=>{const e=document.createElementNS(CNS,tag);for(const k in a)e.setAttribute(k,a[k]);p.appendChild(e);return e};
function chibi(parent,o){
 const g=CE(parent,'g',{}),body=CE(g,'g',{}),armL=CE(body,'g',{}),torso=CE(body,'g',{}),armR=CE(body,'g',{}),head=CE(g,'g',{});
 const sk=o.skin||'#f6d2b0';
 CE(torso,'ellipse',{cx:-34,cy:178,rx:30,ry:16,fill:o.shoe||'#3a2a22',stroke:COL,'stroke-width':6});CE(torso,'ellipse',{cx:34,cy:178,rx:30,ry:16,fill:o.shoe||'#3a2a22',stroke:COL,'stroke-width':6});
 if(o.pants){CE(torso,'path',{d:'M-62 110 L-66 170 L-6 170 L0 128 L6 170 L66 170 L62 110Z',fill:o.pants,stroke:COL,'stroke-width':7,'stroke-linejoin':'round'});
  CE(torso,'path',{d:'M-62 20 Q-72 70 -70 124 L70 124 Q72 70 62 20 Q0 4 -62 20Z',fill:o.robe,stroke:COL,'stroke-width':7,'stroke-linejoin':'round'})}
 else CE(torso,'path',{d:'M-62 20 Q-70 100 -96 170 L96 170 Q70 100 62 20 Q0 4 -62 20Z',fill:o.robe,stroke:COL,'stroke-width':7,'stroke-linejoin':'round'});
 if(o.stripes)o.stripes.forEach((c,i)=>CE(torso,'rect',{x:-68,y:52+i*22,width:136,height:10,fill:c,opacity:.9}));
 if(o.hem)CE(torso,'path',{d:'M-96 170 L96 170 L92 150 Q0 160 -92 150Z',fill:o.hem,stroke:COL,'stroke-width':5});
 if(o.collar=='v'){CE(torso,'path',{d:'M-34 16 L0 60 L34 16',fill:o.trim||'#fff',stroke:COL,'stroke-width':5,'stroke-linejoin':'round'})}
 else if(o.collar=='btn'){CE(torso,'path',{d:'M0 20 L0 120',stroke:COL,'stroke-width':4});[48,76,104].forEach(y=>CE(torso,'circle',{cx:0,cy:y,r:5,fill:'#e8dcc0',stroke:COL,'stroke-width':3}));CE(torso,'path',{d:'M-30 16 L0 34 L30 16',fill:'none',stroke:COL,'stroke-width':5})}
 if(o.sash)CE(torso,'rect',{x:-66,y:92,width:132,height:20,rx:8,fill:o.sash,stroke:COL,'stroke-width':5});
 const arm=(gg,s)=>{CE(gg,'path',{d:`M${s*50} 30 Q${s*96} 56 ${s*96} 120 L${s*66} 120 Q${s*62} 80 ${s*42} 62Z`,fill:o.sleeve||o.robe,stroke:COL,'stroke-width':7,'stroke-linejoin':'round'});CE(gg,'circle',{cx:s*81,cy:128,r:17,fill:sk,stroke:COL,'stroke-width':6})};
 arm(armL,-1);arm(armR,1);
 const hand=CE(armR,'g',{transform:'translate(81,128)'});
 if(o.hold=='pen'){CE(hand,'rect',{x:-6,y:-74,width:12,height:70,rx:5,fill:'#d8372d',stroke:COL,'stroke-width':4});CE(hand,'path',{d:'M-6 -74 L0 -92 L6 -74Z',fill:'#f2e2c2',stroke:COL,'stroke-width':3})}
 if(o.hold=='book'){CE(hand,'rect',{x:-40,y:-70,width:80,height:96,rx:6,fill:o.bookCol||'#2f5f8a',stroke:COL,'stroke-width':5});CE(hand,'rect',{x:-30,y:-56,width:60,height:14,fill:'#efe3c2'})}
 if(o.hold=='paper'){CE(hand,'rect',{x:-36,y:-84,width:72,height:90,rx:4,fill:'#f7f1e2',stroke:COL,'stroke-width':5});for(let i=0;i<4;i++)CE(hand,'rect',{x:-26,y:-70+i*18,width:52-(i%2)*14,height:6,fill:'rgba(60,40,20,.35)'})}
 if(o.hairBack)CE(head,'path',{d:o.hairBack,fill:o.hair||'#22181a',stroke:COL,'stroke-width':7,'stroke-linejoin':'round'});
 CE(head,'ellipse',{cx:0,cy:-110,rx:128,ry:120,fill:sk,stroke:COL,'stroke-width':7});
 CE(head,'ellipse',{cx:-118,cy:-96,rx:16,ry:24,fill:sk,stroke:COL,'stroke-width':6});CE(head,'ellipse',{cx:118,cy:-96,rx:16,ry:24,fill:sk,stroke:COL,'stroke-width':6});
 if(o.earring){CE(head,'circle',{cx:-120,cy:-60,r:13,fill:'#e8b23c',stroke:COL,'stroke-width':4});CE(head,'circle',{cx:120,cy:-60,r:13,fill:'#e8b23c',stroke:COL,'stroke-width':4})}
 const eyes=[-46,46].map(x=>{const e=CE(head,'g',{transform:`translate(${x},-92)`});const w=CE(e,'ellipse',{rx:26,ry:31,fill:'#fff',stroke:COL,'stroke-width':5});const ir=CE(e,'ellipse',{cx:2,cy:4,rx:19,ry:24,fill:o.eye||'#3a2414'});const h1=CE(e,'circle',{cx:-5,cy:-6,r:8,fill:'#fff'}),h2=CE(e,'circle',{cx:8,cy:12,r:4,fill:'#fff'});return{e,w,ir,h:[h1,h2]}});
 if(o.glasses){[-46,46].forEach(x=>CE(head,'circle',{cx:x,cy:-92,r:38,fill:'none',stroke:'#2a2a2a','stroke-width':6}));CE(head,'path',{d:'M-8 -96 L8 -96',stroke:'#2a2a2a','stroke-width':6})}
 const brows=[-46,46].map(x=>CE(head,'path',{d:`M${x-20} -140 Q${x} -150 ${x+20} -140`,fill:'none',stroke:o.hair||'#22181a','stroke-width':7,'stroke-linecap':'round'}));
 [-74,74].forEach(x=>CE(head,'ellipse',{cx:x,cy:-48,rx:20,ry:11,fill:'#f28e8e',opacity:.55}));
 if(o.mous)CE(head,'path',{d:'M-30 -34 Q-14 -44 0 -36 Q14 -44 30 -34',fill:'none',stroke:'#3a2a1a','stroke-width':7,'stroke-linecap':'round'});
 const mouth=CE(head,'path',{fill:'#9a3a32',stroke:COL,'stroke-width':5,'stroke-linejoin':'round'});
 if(o.hairFront)CE(head,'path',{d:o.hairFront,fill:o.hair||'#22181a',stroke:COL,'stroke-width':7,'stroke-linejoin':'round'});
 if(o.extra)o.extra(head);
 const st={look:0,emo:'smile',talk:0,wave:0,point:0,bob:1};
 const set=(t,p={})=>{Object.assign(st,p);const ph=o.ph||0;const b=Math.sin(t*3.2+ph)*5*st.bob;body.setAttribute('transform',`translate(0,${(b*.4).toFixed(1)})`);head.setAttribute('transform',`translate(0,${b.toFixed(1)}) rotate(${(Math.sin(t*1.7+ph)*3+st.look).toFixed(1)} 0 -20)`);
  const bl=((t+ph)%3.4)<.13;eyes.forEach(q=>{q.w.setAttribute('ry',bl?3:31);q.ir.setAttribute('opacity',bl?0:1);q.h.forEach(c=>c.setAttribute('opacity',bl?0:1))});
  const big=st.emo=='surprise';brows.forEach(br=>br.setAttribute('transform',`translate(0,${big?-12:0})`));
  const op=st.talk?Math.abs(Math.sin(t*16+ph))*14+4:0;
  mouth.setAttribute('d',big?'M-12 -26 Q0 -44 12 -26 Q0 -4 -12 -26Z':`M-20 -30 Q0 ${-14+op} 20 -30 Q0 -24 -20 -30Z`);
  armR.setAttribute('transform',st.wave?`rotate(${(-120+Math.sin(t*10)*22).toFixed(1)} 50 34)`:st.point?`rotate(${(-70+Math.sin(t*3)*6).toFixed(1)} 50 34)`:`rotate(${(Math.sin(t*2+1)*4).toFixed(1)} 50 34)`);
  armL.setAttribute('transform',`rotate(${(Math.sin(t*2)*-4).toFixed(1)} -50 34)`)};
 return{g,set,at:(x,y,s=1,fl=1,op=1)=>{g.setAttribute('transform',`translate(${x},${y}) scale(${s*fl},${s})`);g.setAttribute('opacity',s>0?op:0)}};
}
const HAIRF='M-128 -112 Q-120 -230 0 -232 Q120 -230 128 -112 Q96 -170 40 -150 Q10 -196 -30 -150 Q-90 -176 -128 -112Z';
const HAIRM='M-128 -112 Q-120 -224 0 -228 Q120 -224 128 -112 Q70 -168 0 -156 Q-70 -168 -128 -112Z';
// cô giáo (hiện đại): sơ mi trắng, quần xanh, tóc dài, bút đỏ
const CO_GIAO=p=>chibi(p,{robe:'#f4f1ea',pants:'#2f4f7a',collar:'btn',hair:'#1e1416',ph:.3,hold:'pen',hairBack:'M-130 -110 Q-150 40 -100 60 L100 60 Q150 40 130 -110 Z',hairFront:HAIRF});
// người M'nông bên hồ Lắk: áo dệt sọc đỏ đen (vẽ tối giản, không theo trang phục lễ hội cụ thể)
const NGUOI_MNONG=p=>chibi(p,{robe:'#2a2626',sleeve:'#2a2626',pants:'#2a2626',stripes:['#c8412f','#e0a63c','#c8412f'],skin:'#d9a57a',hair:'#1a1210',ph:1.4,hairFront:HAIRM});
// viên công sứ Pháp: áo trắng, mũ trắng vành rộng, ria
const CONG_SU=p=>chibi(p,{robe:'#efeee6',pants:'#efeee6',collar:'btn',hair:'#7a5a3a',ph:2.1,mous:true,hold:'paper',eye:'#3a5a7a',hairFront:HAIRM,
 extra:h=>{CE(h,'ellipse',{cx:0,cy:-196,rx:150,ry:30,fill:'#f2efe2',stroke:COL,'stroke-width':7});CE(h,'path',{d:'M-96 -196 Q-90 -290 0 -294 Q90 -290 96 -196Z',fill:'#f2efe2',stroke:COL,'stroke-width':7});CE(h,'path',{d:'M-92 -214 Q0 -230 92 -214',fill:'none',stroke:'#8a7a5a','stroke-width':10})}});
// cán bộ thống kê: áo xanh, kính, cầm sổ
const CAN_BO=p=>chibi(p,{robe:'#3b6f9c',pants:'#3a3a46',collar:'v',trim:'#f4f1ea',hair:'#1e1416',ph:.9,glasses:true,hold:'book',bookCol:'#c8412f',hairFront:HAIRM});
// ===== Thêm nhân vật chibi (minh họa chung, không phải chân dung người thật) và đồ vật dùng chung
const QUAN=p=>chibi(p,{robe:'#2f4f8a',sleeve:'#2f4f8a',hem:'#e0a63c',collar:'v',trim:'#e8dcc0',hair:'#1e1416',ph:.6,hold:'paper',hairFront:HAIRM,
 extra:h=>{CE(h,'path',{d:'M-104 -170 Q-100 -262 0 -266 Q100 -262 104 -170Z',fill:'#1d1d24',stroke:COL,'stroke-width':7});CE(h,'ellipse',{cx:-150,cy:-196,rx:52,ry:16,fill:'#1d1d24',stroke:COL,'stroke-width':6});CE(h,'ellipse',{cx:150,cy:-196,rx:52,ry:16,fill:'#1d1d24',stroke:COL,'stroke-width':6});CE(h,'rect',{x:-104,y:-186,width:208,height:16,fill:'#e0a63c'})}});
const NONG_DAN=p=>chibi(p,{robe:'#7a5636',sleeve:'#7a5636',pants:'#3a2a22',hair:'#1a1210',skin:'#e6b48c',ph:1.1,hairFront:HAIRM,
 extra:h=>{CE(h,'path',{d:'M-190 -170 L0 -320 L190 -170 Q0 -150 -190 -170Z',fill:'#e8d6a0',stroke:COL,'stroke-width':7,'stroke-linejoin':'round'});[-1,1].forEach(s=>CE(h,'path',{d:`M0 -316 L${s*120} -176`,stroke:'rgba(90,60,30,.4)','stroke-width':4}))}});
const VUA=p=>chibi(p,{robe:'#d9a024',sleeve:'#d9a024',hem:'#a8321f',collar:'v',trim:'#a8321f',hair:'#1e1416',ph:2.6,hairFront:HAIRM,
 extra:h=>{CE(h,'path',{d:'M-100 -176 L-110 -270 L-50 -226 L0 -292 L50 -226 L110 -270 L100 -176Z',fill:'#e8b23c',stroke:COL,'stroke-width':7,'stroke-linejoin':'round'});CE(h,'circle',{cx:0,cy:-218,r:14,fill:'#c8412f',stroke:COL,'stroke-width':4})}});
const pv63=(m,n,col)=>{const p=TINH63.find(q=>q.n==n);return el(m.riv,'path',{d:p.p.map(rpath).join(''),fill:col,stroke:'#fff8e6','stroke-width':3,'stroke-dasharray':'10 8','vector-effect':'non-scaling-stroke',opacity:0})};
const MAPY=(id)=>{const m=vnmap(940,860,id);return{m,hs:hsts(m),SH:SEAH()}};
const MON=(Q,t,n,z0,z1,c)=>{const e=inn(t,R(n)-.2,.5);Q.m.at(540,760,0,1,e);Q.m.view(c[0],c[1],lerp(z0,z1,inn(t,R(n),E(n)-R(n))));seaH(Q.SH,t,e);Q.hs(e);return e};
const CNT=(g,col=CGOLD,sz=96)=>{const n=T(g,0,0,'0',sz,col,10,'middle',OLN);n.setAttribute('font-weight',900);return n};
const BUB=(g,txt,col='#fff')=>{const k=el(g,'g',{});const w=txt.length*34+60;el(k,'path',{d:`M${-w/2} -60 h${w} v90 h${-w/2+40} l-30 34 l-4 -34 h${-w/2-6} z`,fill:col,stroke:OLN,'stroke-width':6,'stroke-linejoin':'round'});const t=T(k,0,4,txt,52,CRED,0,'middle','none');t.setAttribute('font-weight',900);t.setAttribute('stroke','none');return k};
const BOARD=(g,w=560,h=240)=>{const k=el(g,'g',{});el(k,'rect',{x:-w/2,y:-h/2,width:w,height:h,rx:12,fill:'#24382c',stroke:'#8a5a32','stroke-width':16});return k};
const CHALK=(g,txt,sz=90)=>{const id='ck'+(CID++);const cp=el(g,'clipPath',{id});const cr=el(cp,'rect',{x:-420,y:-sz,width:1,height:sz*1.75});const gg=el(g,'g',{'clip-path':`url(#${id})`});const t=T(gg,0,sz*.33,txt,sz,'#f4f1e6',0,'middle','none');t.setAttribute('font-weight',900);t.setAttribute('stroke','none');return u=>cr.setAttribute('width',840*cl(u))};
const SH=(k,x,y,u,rot=0)=>{k.setAttribute('transform',`translate(${x},${y}) rotate(${rot}) scale(${u})`);k.setAttribute('opacity',u>0?1:0)};
// tháp gạch cổ (vẽ chung, không theo một tháp cụ thể)
const TOWER=(g,lv=3,col='#b8653a')=>{const k=el(g,'g',{});for(let i=0;i<lv;i++){const w=200-i*44,y=-i*90;el(k,'rect',{x:-w/2,y:y-90,width:w,height:90,fill:col,stroke:OLN,'stroke-width':7});el(k,'rect',{x:-16,y:y-70,width:32,height:50,rx:14,fill:'#3a2418'})}el(k,'path',{d:`M-30 ${-lv*90} L0 ${-lv*90-70} L30 ${-lv*90}Z`,fill:col,stroke:OLN,'stroke-width':7});return k};
const HILL=(g,w,h,col)=>el(g,'path',{d:`M${-w/2} 0 Q${-w/4} ${-h} 0 ${-h} Q${w/4} ${-h} ${w/2} 0Z`,fill:col,stroke:OLN,'stroke-width':7});
const PEAKS=(g,col='#5f7d6a')=>{const k=el(g,'g',{});[[-220,280,300],[0,360,420],[220,300,320]].forEach(([x,w,h])=>el(k,'path',{d:`M${x-w/2} 0 L${x-w*.1} ${-h} L${x+w*.12} ${-h*.86} L${x+w/2} 0Z`,fill:col,stroke:OLN,'stroke-width':7,'stroke-linejoin':'round'}));return k};
const WAVES=(g,w=520,col='#9fd4f2')=>{const k=el(g,'g',{});el(k,'rect',{x:-w/2,y:-60,width:w,height:120,rx:60,fill:'#3f6f8f',stroke:'#fff','stroke-width':6});const ps=[0,1].map(i=>el(k,'path',{fill:'none',stroke:col,'stroke-width':6,'stroke-linecap':'round'}));return{k,u:t=>ps.forEach((p,i)=>{let d='';for(let x=-w*.4;x<=w*.4;x+=14)d+=(x<=-w*.4?'M':'L')+x+' '+(i*34-16+Math.sin(x*.05+t*3+i)*6).toFixed(1);p.setAttribute('d',d)})}};
const RONG9=(g,col='#3f9a6a')=>{const k=el(g,'g',{});const b=el(k,'path',{fill:'none',stroke:col,'stroke-width':34,'stroke-linecap':'round'});const hd=el(k,'g',{});el(hd,'circle',{r:34,fill:col,stroke:OLN,'stroke-width':6});el(hd,'circle',{cx:12,cy:-8,r:7,fill:'#fff'});el(hd,'path',{d:'M-10 -30 L-24 -64 M10 -30 L20 -66',stroke:CGOLD,'stroke-width':8,'stroke-linecap':'round'});return{k,u:t=>{let d='',hx=0,hy=0;for(let i=0;i<=24;i++){const x=-180+i*15,y=Math.sin(i*.5-t*4)*26;d+=(i?'L':'M')+x+' '+y.toFixed(1);hx=x;hy=y}b.setAttribute('d',d);hd.setAttribute('transform',`translate(${hx+20},${hy.toFixed(1)})`)}}};
// ===== Thêm đồ vật dùng cho #31–34
const STILT=(g,col='#8a5a32')=>{const k=el(g,'g',{});[-80,-20,40,100].forEach(x=>el(k,'rect',{x:x-8,y:-10,width:16,height:90,fill:'#6a4426',stroke:OLN,'stroke-width':4}));el(k,'rect',{x:-120,y:-90,width:250,height:84,fill:col,stroke:OLN,'stroke-width':6});el(k,'path',{d:'M-150 -86 L-40 -170 L80 -170 L160 -86Z',fill:'#5a4a3a',stroke:OLN,'stroke-width':6,'stroke-linejoin':'round'});return k};
const BOOKX=(g,txt,col='#c8412f')=>{const k=el(g,'g',{});el(k,'rect',{x:-150,y:-110,width:300,height:220,rx:10,fill:col,stroke:OLN,'stroke-width':7});el(k,'rect',{x:-115,y:-80,width:230,height:56,fill:'#efe3c2'});const t=T(k,0,-40,txt,34,OLN,0,'middle','none');t.setAttribute('font-weight',900);t.setAttribute('stroke','none');return k};
const POLE=(g)=>{const k=el(g,'g',{});el(k,'path',{d:'M-200 120 L-60 -60 L0 -40 L60 -70 L200 120Z',fill:'#5f7d6a',stroke:OLN,'stroke-width':6,'stroke-linejoin':'round'});el(k,'rect',{x:-8,y:-330,width:16,height:280,fill:'#d8d4ca',stroke:OLN,'stroke-width':4});const f=el(k,'path',{fill:'#c8412f',stroke:OLN,'stroke-width':4});return{k,u:t=>{const w=Math.sin(t*5)*10;f.setAttribute('d',`M8 -326 Q70 ${-336+w} 140 -316 Q70 ${-292+w} 8 -276Z`)}}};
const ROAD=(g)=>{const k=el(g,'g',{});el(k,'path',{d:'M-260 120 L-120 -140 L0 -90 L140 -180 L260 120Z',fill:'#6f8f6a',stroke:OLN,'stroke-width':6,'stroke-linejoin':'round'});el(k,'path',{d:'M-200 110 Q-60 60 -150 10 Q-250 -40 -40 -60 Q120 -80 30 -120',fill:'none',stroke:'#e8e0c8','stroke-width':12,'stroke-linecap':'round'});return k};
const BTREE=(g)=>{const k=el(g,'g',{});el(k,'path',{d:'M-24 120 L-14 -10 L14 -10 L24 120Z',fill:'#6a4426',stroke:OLN,'stroke-width':6});[[-90,-60,90],[60,-70,100],[0,-130,110],[-30,-40,80],[90,-20,70]].forEach(([x,y,r])=>el(k,'circle',{cx:x,cy:y,r,fill:'#4f8a4a',stroke:OLN,'stroke-width':6}));return k};
const TEA=(g)=>{const k=el(g,'g',{});for(let r=0;r<4;r++)el(k,'path',{d:`M-300 ${r*50} Q-150 ${r*50-40} 0 ${r*50} Q150 ${r*50+40} 300 ${r*50}`,fill:'none',stroke:['#5f9a4a','#4f8a3a','#6faa5a','#3f7a3a'][r],'stroke-width':30,'stroke-linecap':'round'});return k};
const FORK=(g)=>{const k=el(g,'g',{});const ps=['M-300 -160 Q-120 -40 0 40','M300 -160 Q120 -40 0 40','M0 40 Q20 130 -40 220'].map(d=>el(k,'path',{d,fill:'none',stroke:'#3f6f8f','stroke-width':46,'stroke-linecap':'round'}));const w=['M-300 -160 Q-120 -40 0 40','M300 -160 Q120 -40 0 40','M0 40 Q20 130 -40 220'].map(d=>el(k,'path',{d,fill:'none',stroke:'#9fd4f2','stroke-width':6,'stroke-dasharray':'20 26','stroke-linecap':'round'}));return{k,u:t=>w.forEach((p,i)=>p.setAttribute('stroke-dashoffset',(-t*60).toFixed(1)))}};
const STALL=(g,col='#c8412f')=>{const k=el(g,'g',{});el(k,'rect',{x:-90,y:-40,width:180,height:100,fill:'#b89a6a',stroke:OLN,'stroke-width':6});el(k,'path',{d:'M-110 -40 L-80 -100 L80 -100 L110 -40Z',fill:col,stroke:OLN,'stroke-width':6});return k};
const COIN=(g)=>{const k=el(g,'g',{});el(k,'ellipse',{rx:60,ry:24,fill:'#d8d8de',stroke:OLN,'stroke-width':6});el(k,'ellipse',{cy:-14,rx:60,ry:24,fill:'#eeeef2',stroke:OLN,'stroke-width':6});return k};
const MAP11=(Q,t,n,name,cen,z0,z1)=>{const e=MON(Q,t,n,z0,z1,cen);Q.m.hi(name,e*(.7+.25*Math.sin(t*3)),CGOLD);return e};
// ===== CẢNH tn32 Tuyên Quang (chibi vẽ bằng code + bản đồ hành chính phẳng; ranh giới trước 2025 nét đứt; không vẽ ranh giới năm 1891)
const TPTQ=[105.22,21.82],LUNGCU=[105.32,23.36],THL2=[105.85,21.03];
const LO=[[104.98,22.82],[105.05,22.4],[105.15,22.1],[105.22,21.82],[105.3,21.5]];
// 1 hook: cột cờ Lũng Cú ở vùng cực bắc giờ thuộc tỉnh Tuyên Quang
S2(1,1,'d',null,g=>{const pl=POLE(g);const a=TILE2(g,'LŨNG CÚ',CSTEEL,320),b=TILE2(g,'TUYÊN QUANG',CGOLD,440);const ar=el(g,'path',{d:'M0 -50 L0 40 M-26 14 L0 46 L26 14',fill:'none',stroke:'#fff','stroke-width':12,'stroke-linecap':'round','stroke-linejoin':'round'});const cg=CO_GIAO(g);const t0=AT(1,'Cột',.1),tt=AT(1,'Tuyên',3.4);bm(t0,true);bm(tt);
 return{upd:t=>{SH(pl.k,540,760,popv(t,t0,.45));pl.u(t);PUT(a,540,330,popv(t,t0+.3,.45),1,-2);PUT(ar,800,520,popv(t,tt-.3,.4),1,0);PUT(b,700,1030,popv(t,tt,.45),1,2);cg.set(t,{emo:'surprise',point:t>tt,look:6});cg.at(220,1690,.8*popv(t,R(1)+.3,.45))}}});
// 2 không phải lần đầu Hà Giang và Tuyên Quang về chung một nhà
S2(2,2,'p',null,g=>{const a=TILE2(g,'HÀ GIANG',CSTEEL,320),b=TILE2(g,'TUYÊN QUANG',CSTEEL,380);const roof=el(g,'path',{d:'M-400 0 L0 -170 L400 0',fill:'none',stroke:CGOLD,'stroke-width':14,'stroke-linejoin':'round','stroke-linecap':'round'});const q=T(g,0,0,'LẦN ĐẦU?',90,CRED,10,'middle',OLN);q.setAttribute('font-weight',900);const tl=AT(2,'lần',1.4),th=AT(2,'Hà',2.6),tc=AT(2,'chung',4.4);bm(tl);bm(th,true);bm(tc);
 return{upd:t=>{PUT(q,540,380,popv(t,R(2)+.2,.45),1,Math.sin(t*3)*4);PUT(a,320,800,popv(t,th,.4),1,-3);PUT(b,760,800,popv(t,th+.3,.4),1,3);PUT(roof,540,690,inn(t,tc-.3,.6),1,0)}}});
// 3 tên Tuyên Quang có từ rất sớm; thời vua Trần Hiến Tông đặt làm trấn Tuyên Quang
S2(3,3,'d',null,g=>{const st=TILE2(g,'TRẤN TUYÊN QUANG',CRED,520);const A=strip('THỜI TRẦN',false,44,31);const q=QUAN(g);const tt=AT(3,'Trần',2.2),ts=AT(3,'trấn',4.0);bm(R(3)+.2);bm(tt);bm(ts,true);
 return{upd:t=>{sh(A,t,540,330,-2,popv(t,tt,.45));PUT(st,540,560,popv(t,ts,.4),1+.04*Math.sin(t*4),-3);q.set(t,{point:t>ts,look:-4});q.at(540,1690,.85*popv(t,R(3)+.3,.45))}}});
// 4 vùng biên phía bắc kinh thành Thăng Long, các triều đại coi như hàng rào che chắn (bản đồ)
S2(4,4,'p',null,g=>{const Q=MAPY(41);const tq=pv63(Q.m,'Tuyên Quang',CGOLD);const pt=PIN(Q.m,'THĂNG LONG',CSTEEL,-30,28);const ar=MLINE(Q.m,[[105.85,21.1],[105.5,21.5],[105.25,21.8]],CRED,12);const A=strip('HÀNG RÀO CHE CHẮN',true,42,41);const tt=AT(4,'Thăng',2.0),th=AT(4,'hàng',4.6);bm(tt);bm(th,true);
 return{upd:t=>{const e=MON(Q,t,4,220,240,[105.5,21.9]);tq.setAttribute('opacity',e*(.7+.3*Math.sin(t*3)));PINAT(Q.m,pt,THL2,popv(t,tt,.45));ar(inn(t,tt+.3,1.2));sh(A,t,540,300,-2,popv(t,th,.45))}}});
// 5 thời Lê có lúc đổi tên Minh Quang, đến thời Nguyễn lại trở về Tuyên Quang
S2(5,5,'d',null,g=>{const N=['TUYÊN QUANG','MINH QUANG','TUYÊN QUANG'];const L=N.map((s,i)=>TILE2(g,s,i==2?CGOLD:CSTEEL,400));const X=[XX(g),XX(g)];const A=strip('THỜI LÊ',false,40,51),B=strip('THỜI NGUYỄN',false,40,52);const T0=[R(5)+.1,AT(5,'Minh',2.0),AT(5,'trở',3.8)];bm(T0[1],true);bm(T0[2]);
 return{upd:t=>{L.forEach((k,i)=>PUT(k,540+(i-1)*40,380+i*230,popv(t,T0[i],.4),1,(i-1)*3));X.forEach((x,i)=>PUT(x,540+(i-1)*40,380+i*230,popv(t,T0[i+1],.3)*.6,1,0));sh(A,t,800,500,3,popv(t,T0[1],.45));sh(B,t,280,760,-3,popv(t,T0[2],.45))}}});
// 6 năm 1831 Minh Mạng chia các vùng thành tỉnh; Tuyên Quang là một trong những tỉnh lập từ đợt ấy
S2(6,6,'p',t=>'1831',g=>{const q=QUAN(g);const st=TILE2(g,'TỈNH TUYÊN QUANG',CRED,500);const L=[...Array(6)].map(()=>{const k=el(g,'rect',{x:-70,y:-36,width:140,height:72,rx:10,fill:CSTEEL,stroke:'#fff','stroke-width':5});return k});const tc=AT(6,'chia',2.4),tt=AT(6,'Tuyên',3.8);bm(tc);bm(tt,true);
 return{upd:t=>{L.forEach((k,i)=>PUT(k,250+(i%3)*290,420+Math.floor(i/3)*120,popv(t,tc+i*.1,.35),1,0));PUT(st,540,760,popv(t,tt,.4),1+.04*Math.sin(t*4),-3);q.set(t,{point:t>tc,look:6});q.at(540,1690,.82*popv(t,R(6)+.3,.45))}}});
// 7 năm 1891 người Pháp lập tỉnh Hà Giang, lấy cả một phần đất phía bắc của Tuyên Quang (bản đồ ranh giới trước 2025)
S2(7,7,'d',t=>t<AT(7,'1891',1.8)-.3?'':'1891',g=>{const Q=MAPY(71);const tq=pv63(Q.m,'Tuyên Quang',CGOLD),hg=pv63(Q.m,'Hà Giang',CSTEEL);const l1=MLB(Q.m.top,'TUYÊN QUANG',30,'#fff',OLN),l2=MLB(Q.m.top,'HÀ GIANG',34,'#fff',CRED);const cs=CONG_SU(g);const th=AT(7,'Hà',2.8),tl=AT(7,'lấy',4.0);bm(th,true);bm(tl);
 return{upd:t=>{const e=MON(Q,t,7,200,210,[105.15,22.45]);tq.setAttribute('opacity',e);labAt(Q.m,l1,[105.25,21.95],e);hg.setAttribute('opacity',popv(t,th,.4)*(.75+.25*Math.sin(t*4)));labAt(Q.m,l2,[105.0,22.85],popv(t,th,.45));cs.set(t,{point:t>tl,look:6});cs.at(180,1690,.62*popv(t,R(7)+.4,.45))}}});
// 8 Hà Giang ở phía trên, Tuyên Quang ở phía dưới, cùng dọc sông Lô
S2(8,8,'p',null,g=>{const Q=MAPY(81);const tq=pv63(Q.m,'Tuyên Quang',CGOLD),hg=pv63(Q.m,'Hà Giang',CSTEEL);const lo=MLINE(Q.m,LO,'#5fb4e6',12);const ll=MLB(Q.m.top,'SÔNG LÔ',30,'#fff',CSTEEL);const A=strip('PHÍA TRÊN',false,38,81),B=strip('PHÍA DƯỚI',false,38,82);const ttr=AT(8,'trên',1.4),td=AT(8,'dưới',2.8),tl=AT(8,'Lô',4.2);bm(ttr);bm(td);bm(tl,true);
 return{upd:t=>{const e=MON(Q,t,8,210,200,[105.15,22.45]);hg.setAttribute('opacity',popv(t,ttr-.3,.4)*.8);tq.setAttribute('opacity',popv(t,td-.3,.4)*.8);sh(A,t,540,300,-2,popv(t,ttr,.45));sh(B,t,540,1150,2,popv(t,td,.45));lo(inn(t,tl-.5,1.2));labAt(Q.m,ll,[105.35,22.25],popv(t,tl,.45))}}});
// 9 năm 1976 hai tỉnh gộp lần đầu, tên ghép Hà Tuyên
S2(9,9,'d',t=>'1976',g=>{const a=TILE2(g,'HÀ GIANG',CSTEEL,320),b=TILE2(g,'TUYÊN QUANG',CSTEEL,380);const c=TILE2(g,'HÀ TUYÊN',CGOLD,380);const h1=TILE2(g,'HÀ',CRED,140),h2=TILE2(g,'TUYÊN',CRED,200);const rg=RINGS(g,CGOLD,3);const tg=AT(9,'gộp',1.4),tt=AT(9,'Hà',3.0),tc=AT(9,'chữ',4.4);bm(tg);bm(tt,true);bm(tc);
 return{upd:t=>{const mg=inn(t,tt-.4,.7);PUT(a,lerp(290,540,mg),lerp(460,640,mg),popv(t,R(9)+.1,.4)*(1-mg),1,-3);PUT(b,lerp(790,540,mg),lerp(460,640,mg),popv(t,R(9)+.3,.4)*(1-mg),1,3);PUT(c,540,640,mg,1+.04*Math.sin(t*4),0);RU(rg,t,240,540,640,mg);PUT(h1,380,900,popv(t,tc,.4),1,-4);PUT(h2,700,900,popv(t,tc+.4,.4),1,4)}}});
// 10 Hà Tuyên tồn tại 15 năm, năm 1991 lại chia thành Hà Giang và Tuyên Quang
S2(10,10,'p',t=>t<AT(10,'1991',2.4)-.3?'':'1991',g=>{const n=CNT(g,CGOLD,110);const c=TILE2(g,'HÀ TUYÊN',CGOLD,380);const a=TILE2(g,'HÀ GIANG',CSTEEL,320),b=TILE2(g,'TUYÊN QUANG',CSTEEL,380);const tm=AT(10,'mười',1.2),tc=AT(10,'chia',3.4);bm(tm,true);bm(tc);
 return{upd:t=>{n.textContent=Math.round(15*inn(t,tm,1.2))+' năm';PUT(n,540,380,popv(t,tm,.4),.9,0);const u=inn(t,tc,.8);PUT(c,540,640,popv(t,R(10)+.1,.4)*(1-u),1,0);PUT(a,lerp(540,290,u),640+u*120,u,1,-5);PUT(b,lerp(540,790,u),640+u*120,u,1,5)}}});
// 11 năm 2025 hợp nhất lần thứ hai, tên Tuyên Quang, trụ sở TP Tuyên Quang cũ
S2(11,11,'d',t=>'2025',g=>{const Q=MAPY(111);const P=['Hà Giang','Tuyên Quang'].map(n=>pv63(Q.m,n,CSTEEL));const l3=MLB(Q.m.top,'TUYÊN QUANG',46,'#fff',CRED);const pt=PIN(Q.m,'TRỤ SỞ',CRED,-30,28);const tl=AT(11,'lần',1.6),tm=AT(11,'mang',3.0),tt=AT(11,'trụ',4.6);bm(tl);bm(tm,true);bm(tt);
 return{upd:t=>{const e=MON(Q,t,11,200,215,[105.15,22.5]);const mg=inn(t,tm-.2,.6);P.forEach((p,i)=>p.setAttribute('opacity',popv(t,R(11)+.2+i*.3,.4)*(1-.5*mg)));Q.m.hi('Tuyên Quang',mg*(.75+.2*Math.sin(t*3)),CGOLD);labAt(Q.m,l3,[105.2,22.45],popv(t,tm,.45));PINAT(Q.m,pt,TPTQ,popv(t,tt,.45))}}});
// 12 cao nguyên đá Đồng Văn, đèo Mã Pì Lèng, cột cờ Lũng Cú nay đều trong tỉnh Tuyên Quang
S2(12,12,'p',null,g=>{const Q=MAPY(121);const pt=PIN(Q.m,'LŨNG CÚ',CRED,-30,28);const L=['CAO NGUYÊN ĐÁ ĐỒNG VĂN','ĐÈO MÃ PÌ LÈNG','CỘT CỜ LŨNG CÚ'].map((s,i)=>strip(s,i==2,32,121+i));const T0=[AT(12,'Đồng',1.4),AT(12,'Mã',2.8),AT(12,'Lũng',4.0)];bm(T0[0]);bm(T0[1]);bm(T0[2],true);
 return{upd:t=>{const e=MON(Q,t,12,215,240,[105.2,22.75]);Q.m.hi('Tuyên Quang',e*(.55+.15*Math.sin(t*3)),CGOLD);PINAT(Q.m,pt,LUNGCU,popv(t,T0[2],.45));sh(L[0],t,540,280,-2,popv(t,T0[0],.4));sh(L[1],t,540,1160,2,popv(t,T0[1],.4));sh(L[2],t,540,1230,-2,0)}}});
// 13 từ một trấn biên giới thời Trần, cái tên Tuyên Quang nay trải tới vùng cực bắc
S2(13,13,'d',null,g=>{const a=TILE2(g,'TRẤN TUYÊN QUANG',CSTEEL,480),b=TILE2(g,'TỈNH TUYÊN QUANG',CGOLD,480);const pl=POLE(g);const ar=el(g,'path',{d:'M0 60 L0 -40 M-26 -14 L0 -46 L26 -14',fill:'none',stroke:'#fff','stroke-width':12,'stroke-linecap':'round','stroke-linejoin':'round'});const A=strip('TỚI VÙNG CỰC BẮC',true,42,131);const tt=AT(13,'trấn',.6),tn=AT(13,'nay',3.4),tc=AT(13,'cực',5.0);bm(tt);bm(tn,true);bm(tc);
 return{upd:t=>{PUT(a,540,1060,popv(t,tt,.45),.9,-2);PUT(ar,540,920,popv(t,tn-.3,.4),1,0);PUT(b,540,800,popv(t,tn,.45),.9,2);SH(pl.k,540,560,.7*popv(t,tc-.4,.45));pl.u(t);sh(A,t,540,300,-2,popv(t,tc,.45))}}});
// 14 câu hỏi: đèo Mã Pì Lèng, cây đa Tân Trào (chibi vẫy tay)
S2(14,14,'d',null,g=>{const rd=ROAD(g);const tr=BTREE(g);const nd=NONG_DAN(g),cg=CO_GIAO(g);const A=strip('ĐÈO MÃ PÌ LÈNG',false,36,141),B=strip('CÂY ĐA TÂN TRÀO',false,36,142),C=strip('BẠN ĐÃ ĐẾN CHƯA?',true,42,143);const t1=AT(14,'đèo',1.0),t2=AT(14,'cây',2.6);bm(AT(14,'Bạn',.3));bm(t1);bm(t2,true);
 return{upd:t=>{sh(C,t,540,330,-2,PV(t,14,'Bạn',.3));SH(rd,300,720,.75*popv(t,t1-.2,.45));sh(A,t,300,860,-2,popv(t,t1,.45));SH(tr,780,700,.85*popv(t,t2-.2,.45),Math.sin(t*1.5)*2);sh(B,t,780,860,2,popv(t,t2,.45));nd.set(t,{wave:1,look:6});nd.at(330,1690,.66*popv(t,R(14)+.2,.45));cg.set(t,{wave:1,look:-6});cg.at(760,1690,.7*popv(t,R(14)+.4,.45),-1)}}},9999);
