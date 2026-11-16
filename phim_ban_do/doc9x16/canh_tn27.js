// ===== TÊN TỈNH THÀNH #27: Tây Ninh (tn27), chibi vẽ bằng code. Bản đồ hành chính phẳng 34 tỉnh (geoBoundaries, phạm vi công cộng), không vẽ nước láng giềng; ranh giới tỉnh trước 2025 vẽ nét đứt.
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
// ===== Dấu ấn riêng (Tây Ninh): đổi màu nền, họa tiết mờ ở đáy, hạt trôi chậm, sóng nước ở đáy (y>1650)
{DR1.setAttribute('opacity',0);DR2.setAttribute('opacity',0);
 DARKG.firstChild.setAttribute('fill','#15181a');
 [...PAPG.children].forEach(c=>{if(c.tagName=='g')c.setAttribute('opacity',0);if(c.tagName=='line')c.setAttribute('stroke','rgba(0,0,0,0)')});
 PAPG.firstChild.setAttribute('fill','#eef0e6');
 const sky=(p,col)=>{const g=el(p,'g',{});const L=(d,w=5)=>el(g,'path',{d,fill:'none',stroke:col,'stroke-width':w,'stroke-linejoin':'round','stroke-linecap':'round'});
  L('M0 1630 Q120 1590 220 1600 Q330 1450 420 1440 Q520 1450 600 1580 Q760 1600 1080 1620',5);
  return g};
 const skA=sky(DARKG,'rgba(220,200,160,.15)'),skB=sky(PAPG,'rgba(90,70,50,.16)');
 const fr=(p,col)=>{const r=rng(271);return[...Array(14)].map(()=>{const e=el(p,'g',{});el(e,'circle',{r:7,fill:col});return{e,x:30+r()*1020,y:230+r()*1000,ph:r()*6}})};
 const pA=fr(DARKG,'rgba(160,200,170,.25)'),pB=fr(PAPG,'rgba(60,100,70,.2)');
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
const CHALK=(g,txt,sz=90)=>{const id='ck'+(CID++);const cp=el(g,'clipPath',{id});const cr=el(cp,'rect',{x:-420,y:-sz,width:1,height:sz*1.4});const gg=el(g,'g',{'clip-path':`url(#${id})`});const t=T(gg,0,sz*.33,txt,sz,'#f4f1e6',0,'middle','none');t.setAttribute('font-weight',900);t.setAttribute('stroke','none');return u=>cr.setAttribute('width',840*cl(u))};
const SH=(k,x,y,u,rot=0)=>{k.setAttribute('transform',`translate(${x},${y}) rotate(${rot}) scale(${u})`);k.setAttribute('opacity',u>0?1:0)};
// tháp gạch cổ (vẽ chung, không theo một tháp cụ thể)
const TOWER=(g,lv=3,col='#b8653a')=>{const k=el(g,'g',{});for(let i=0;i<lv;i++){const w=200-i*44,y=-i*90;el(k,'rect',{x:-w/2,y:y-90,width:w,height:90,fill:col,stroke:OLN,'stroke-width':7});el(k,'rect',{x:-16,y:y-70,width:32,height:50,rx:14,fill:'#3a2418'})}el(k,'path',{d:`M-30 ${-lv*90} L0 ${-lv*90-70} L30 ${-lv*90}Z`,fill:col,stroke:OLN,'stroke-width':7});return k};
const HILL=(g,w,h,col)=>el(g,'path',{d:`M${-w/2} 0 Q${-w/4} ${-h} 0 ${-h} Q${w/4} ${-h} ${w/2} 0Z`,fill:col,stroke:OLN,'stroke-width':7});
const PEAKS=(g,col='#5f7d6a')=>{const k=el(g,'g',{});[[-220,280,300],[0,360,420],[220,300,320]].forEach(([x,w,h])=>el(k,'path',{d:`M${x-w/2} 0 L${x-w*.1} ${-h} L${x+w*.12} ${-h*.86} L${x+w/2} 0Z`,fill:col,stroke:OLN,'stroke-width':7,'stroke-linejoin':'round'}));return k};
const WAVES=(g,w=520,col='#9fd4f2')=>{const k=el(g,'g',{});el(k,'rect',{x:-w/2,y:-60,width:w,height:120,rx:60,fill:'#3f6f8f',stroke:'#fff','stroke-width':6});const ps=[0,1].map(i=>el(k,'path',{fill:'none',stroke:col,'stroke-width':6,'stroke-linecap':'round'}));return{k,u:t=>ps.forEach((p,i)=>{let d='';for(let x=-w*.4;x<=w*.4;x+=14)d+=(x<=-w*.4?'M':'L')+x+' '+(i*34-16+Math.sin(x*.05+t*3+i)*6).toFixed(1);p.setAttribute('d',d)})}};
const RONG9=(g,col='#3f9a6a')=>{const k=el(g,'g',{});const b=el(k,'path',{fill:'none',stroke:col,'stroke-width':34,'stroke-linecap':'round'});const hd=el(k,'g',{});el(hd,'circle',{r:34,fill:col,stroke:OLN,'stroke-width':6});el(hd,'circle',{cx:12,cy:-8,r:7,fill:'#fff'});el(hd,'path',{d:'M-10 -30 L-24 -64 M10 -30 L20 -66',stroke:CGOLD,'stroke-width':8,'stroke-linecap':'round'});return{k,u:t=>{let d='',hx=0,hy=0;for(let i=0;i<=24;i++){const x=-180+i*15,y=Math.sin(i*.5-t*4)*26;d+=(i?'L':'M')+x+' '+y.toFixed(1);hx=x;hy=y}b.setAttribute('d',d);hd.setAttribute('transform',`translate(${hx+20},${hy.toFixed(1)})`)}}};
// ===== CẢNH tn27 Tây Ninh (chibi vẽ bằng code + bản đồ hành chính phẳng 34 tỉnh; ranh giới trước 2025 nét đứt)
const BADEN=[106.17,11.38],TANAN=[106.41,10.54],GDINH=[106.70,10.78],TRB=[106.33,11.05];
const ELE=(g,col='#8a8f96')=>{const k=el(g,'g',{});el(k,'ellipse',{cx:0,cy:0,rx:120,ry:80,fill:col,stroke:OLN,'stroke-width':7});[-70,-20,30,80].forEach(x=>el(k,'rect',{x:x-16,y:50,width:32,height:70,rx:10,fill:col,stroke:OLN,'stroke-width':6}));el(k,'circle',{cx:120,cy:-40,r:62,fill:col,stroke:OLN,'stroke-width':7});el(k,'ellipse',{cx:96,cy:-40,rx:34,ry:48,fill:'#a8adb4',stroke:OLN,'stroke-width':5});const tr=el(k,'path',{fill:'none',stroke:col,'stroke-width':26,'stroke-linecap':'round'});el(k,'circle',{cx:140,cy:-56,r:7,fill:OLN});return{k,u:t=>tr.setAttribute('d',`M170 -20 Q200 30 ${190+Math.sin(t*3)*14} 80`)}};
// 1 hook: Tây Ninh nghĩa là phía tây yên ổn, nhưng ra đời giữa lúc vùng biên không yên
S2(1,1,'d',null,g=>{const a=TILE2(g,'TÂY',CGOLD,240),b=TILE2(g,'NINH',CGOLD,260);const A=strip('PHÍA TÂY',false,42,11),B=strip('YÊN ỔN',false,42,12),C=strip('VÙNG BIÊN KHÔNG YÊN',true,40,13);const q=QUAN(g);const t0=AT(1,'Tây',.1),tp=AT(1,'phía',1.2),ty=AT(1,'yên',1.9),tk=AT(1,'không',4.2);bm(t0,true);bm(tk);
 return{upd:t=>{const sk=t>tk?Math.sin(t*30)*6*(1-inn(t,tk+.6,.6)):0;PUT(a,370+sk,420,popv(t,t0,.4),1,-3);PUT(b,710-sk,420,popv(t,t0+.2,.4),1,3);sh(A,t,370,600,-3,popv(t,tp,.45));sh(B,t,710,600,3,popv(t,ty,.45));sh(C,t,540,800,2,popv(t,tk,.5));q.set(t,{emo:t>tk?'surprise':'smile',talk:0,look:-4});q.at(540,1680,.85*popv(t,R(1)+.3,.45))}}});
// 2 trước khi có tên: quanh núi Bà Đen đồi gò trùng điệp, rừng rậm, người ở thưa
S2(2,2,'p',null,g=>{const pk=PEAKS(g,'#4f6e5c');const tr=[0,1,2,3,4].map(()=>PINE(g,1.6,'#3f7a5a'));const A=strip('NÚI BÀ ĐEN',false,42,21),B=strip('RỪNG RẬM NỐI NHAU',true,40,22),C=strip('NGƯỜI Ở THƯA THỚT',false,38,23);const tb=AT(2,'Bà',1.6),tr2=AT(2,'rừng',3.6),tn=AT(2,'người',4.8);bm(tb,true);bm(tr2);bm(tn);
 return{upd:t=>{SH(pk,540,760,popv(t,R(2)+.1,.5));tr.forEach((k,i)=>{const u=popv(t,tr2-.3+i*.12,.4);k.setAttribute('transform',`translate(${180+i*180},${900+(i%2)*40}) scale(${1.6*u}) rotate(${Math.sin(t*2+i)*3})`);k.setAttribute('opacity',u>0?1:0)});sh(A,t,540,360,-2,popv(t,tb,.45));sh(B,t,540,1080,2,popv(t,tr2,.45));sh(C,t,540,1180,-2,popv(t,tn,.45))}}});
// 3 theo một số tài liệu, người Khmer xưa gọi bằng tên nghĩa là chuồng voi
S2(3,3,'d',null,g=>{const e1=ELE(g),e2=ELE(g,'#7c8188');const T1=TILE2(g,'CHUỒNG VOI',CGOLD,460);const A=strip('THEO MỘT SỐ TÀI LIỆU',false,36,31),B=strip('NHIỀU VOI VÀ THÚ DỮ',true,38,32);const tc=AT(3,'chuồng',3.4),tv=AT(3,'nhiều',5.2);bm(R(3)+.2);bm(tc,true);bm(tv);
 return{upd:t=>{sh(A,t,540,340,-2,popv(t,R(3)+.2,.45));PUT(T1,540,520,popv(t,tc,.45),1,Math.sin(t*2)*2);const w=Math.sin(t*2)*10;SH(e1.k,300+w,880,.9*popv(t,tc+.3,.45));e1.u(t);SH(e2.k,760-w,940,.75*popv(t,tc+.6,.45));e2.u(t+1);sh(B,t,540,1140,2,popv(t,tv,.45))}}});
// 4 từ thế kỷ 17 lưu dân từ miền Trung vào khai hoang, sống xen với cư dân bản địa ở Trảng Bàng, Gò Dầu (bản đồ)
S2(4,4,'p',null,g=>{const Q=MAPY(41);const ar=MLINE(Q.m,[[108.6,15.3],[108.9,13.6],[108.0,12.0],[106.9,11.3],[106.4,11.1]],CGOLD,12);const pt=PIN(Q.m,'TRẢNG BÀNG · GÒ DẦU',CRED,-30,28);const A=strip('THẾ KỶ 17',false,40,41),B=strip('VÀO KHAI HOANG',true,40,42);const nd=NONG_DAN(g);const tm=AT(4,'miền',2.0),tk=AT(4,'khai',3.2),tt=AT(4,'Trảng',5.6);bm(R(4)+.2);bm(tk,true);bm(tt);
 return{upd:t=>{const e=MON(Q,t,4,135,150,[107.4,13.0]);ar(inn(t,tm,1.6));PINAT(Q.m,pt,TRB,popv(t,tt,.45));sh(A,t,540,300,-2,popv(t,R(4)+.2,.45));sh(B,t,760,1150,2,popv(t,tk,.45));nd.set(t,{talk:0,wave:t>tt,look:4});nd.at(lerp(-120,210,inn(t,R(4)+.3,1.4)),1690,.62*popv(t,R(4)+.3,.4))}}});
// 5 năm 1834 hơn bảy trăm quân Xiêm vượt rạch Tây Ninh, định đánh xuống Gia Định, rồi buộc phải lui về đất Chân Lạp
S2(5,5,'d',t=>'1834',g=>{const Q=MAPY(51);const old=pv63(Q.m,'Tây Ninh',CGOLD);const ar=MLINE(Q.m,[[105.85,11.75],[106.12,11.3],[106.45,10.98]],CRED,14),bk=MLINE(Q.m,[[106.3,11.15],[106.0,11.45],[105.75,11.75]],CSTEEL,10);const pg=PIN(Q.m,'GIA ĐỊNH',CSTEEL,-30,28);const n=CNT(g,CRED,90);const A=strip('RẠCH TÂY NINH',false,38,51),B=strip('BUỘC PHẢI LUI',true,42,52);const tv=AT(5,'vượt',1.8),tg=AT(5,'Gia',3.0),tl=AT(5,'lui',5.0);bm(R(5)+.3,true);bm(tv);bm(tl);
 return{upd:t=>{const e=MON(Q,t,5,300,330,[106.2,11.15]);old.setAttribute('opacity',e*.6);ar(inn(t,tv-.2,1.4));PINAT(Q.m,pg,GDINH,popv(t,tg,.45));bk(inn(t,tl-.2,1.0));n.textContent=Math.round(700*inn(t,R(5)+.6,1))+'+ QUÂN';PUT(n,540,1160,popv(t,R(5)+.6,.4)*(1-inn(t,tl-.4,.4)),.8,0);sh(A,t,540,300,-2,popv(t,tv+.6,.45));sh(B,t,540,1150,2,popv(t,tl,.45))}}});
// 6 hai năm sau, năm 1836, vua Minh Mạng cho lập phủ Tây Ninh ở vùng biên, đặt dưới tỉnh Gia Định
S2(6,6,'p',t=>'1836',g=>{const q=QUAN(g);const st=TILE2(g,'PHỦ TÂY NINH',CRED,460);const A=strip('HAI NĂM SAU',false,40,61),B=strip('THUỘC TỈNH GIA ĐỊNH',false,38,62);const tl=AT(6,'lập',3.0),tg=AT(6,'Gia',5.4);bm(R(6)+.2);bm(tl,true);bm(tg);
 return{upd:t=>{sh(A,t,540,330,-2,popv(t,R(6)+.2,.45));PUT(st,540,560,popv(t,tl,.4),1+.04*Math.sin(t*4),-4);sh(B,t,540,780,2,popv(t,tg,.45));q.set(t,{point:t>tl-.4,talk:0,look:-6});q.at(540,1680,.85*popv(t,R(6)+.3,.45))}}});
// 7 sử không chép rõ vì sao chọn tên; đặt cạnh trận vừa qua, có thể hiểu như mong muốn giữ yên biên giới
S2(7,7,'d',null,g=>{const bd=BOARD(g,640,300);const w1=CHALK(bd,'TÂY = PHÍA TÂY',70),w2=CHALK(bd,'NINH = YÊN ỔN',70);const A=stamp('SỬ KHÔNG CHÉP RÕ',44);const B=strip('CÓ THỂ HIỂU',false,38,71),C=strip('MONG GIỮ YÊN BIÊN GIỚI',true,38,72);const cg=CO_GIAO(g);const ts=AT(7,'Sử',.1),tc=AT(7,'có',4.6),tg=AT(7,'giữ',6.6);bm(ts,true);bm(tc);bm(tg);
 return{upd:t=>{PUT(bd,540,560,popv(t,R(7)+.1,.45),1,0);w1(inn(t,R(7)+.3,1.0));w2(inn(t,R(7)+1.2,1.0));[...bd.querySelectorAll('g[clip-path]')].forEach((q,i)=>q.setAttribute('transform',`translate(0,${i?60:-50})`));const su=popv(t,ts+.4,.4);A.at(540,350,-6,su,su>0?1:0);sh(B,t,540,800,-2,popv(t,tc,.45));sh(C,t,540,900,2,popv(t,tg,.45));cg.set(t,{point:t>tc-.3,talk:0,look:6});cg.at(220,1690,.7*popv(t,R(7)+.3,.45))}}});
// 8 thời Pháp Tây Ninh thành một hạt riêng, từ năm 1900 gọi chính thức là tỉnh Tây Ninh
S2(8,8,'p',t=>t<AT(8,'1900',2.4)-.3?'':'1900',g=>{const sg=SIGN(g,'HẠT TÂY NINH',CSTEEL);const cs=CONG_SU(g);const A=strip('THỜI PHÁP',false,40,81);const th=AT(8,'hạt',1.4),tn=AT(8,'tỉnh',3.6);bm(th);bm(tn,true);
 return{upd:t=>{sh(A,t,540,330,-2,popv(t,R(8)+.1,.45));const fl=inn(t,tn-.2,.4);const u=popv(t,th-.2,.45);sg.k.setAttribute('transform',`translate(560,${640+Math.sin(t*2)*5}) scale(${u*Math.abs(Math.cos(fl*Math.PI))||.001},${u})`);sg.k.setAttribute('opacity',u>0?1:0);sg.t.textContent=fl>.5?'TỈNH TÂY NINH':'HẠT TÂY NINH';cs.set(t,{point:t>tn-.3,talk:0,look:6});cs.at(200,1690,.72*popv(t,R(8)+.3,.45))}}});
// 9 một phần đất bị cắt ra lập Phước Thành, Hậu Nghĩa, nhưng tên Tây Ninh vẫn giữ
S2(9,9,'d',null,g=>{const c=TILE2(g,'TÂY NINH',CGOLD,380);const a=TILE2(g,'PHƯỚC THÀNH',CSTEEL,330),b=TILE2(g,'HẬU NGHĨA',CSTEEL,300);const A=strip('TÊN VẪN GIỮ NGUYÊN',true,42,91);const rg=RINGS(g,CGOLD,3);const tc=AT(9,'cắt',2.0),tp=AT(9,'Phước',3.2),th=AT(9,'Hậu',4.0),tg=AT(9,'giữ',5.8);bm(tc,true);bm(tg);
 return{upd:t=>{PUT(c,540,620,popv(t,R(9)+.1,.45),1+.03*Math.sin(t*4),0);const u1=inn(t,tp,.8),u2=inn(t,th,.8);PUT(a,lerp(540,280,u1),lerp(620,880,u1),popv(t,tp,.3),.8,-8*u1);PUT(b,lerp(540,800,u2),lerp(620,880,u2),popv(t,th,.3),.8,8*u2);RU(rg,t,240,540,620,inn(t,tg,.5));sh(A,t,540,1120,2,popv(t,tg,.45))}}});
// 10 năm 2025 Tây Ninh hợp nhất Long An, giữ tên Tây Ninh, trụ sở ở phường Long An (Tân An cũ)
S2(10,10,'p',t=>'2025',g=>{const Q=MAPY(101);const tn=pv63(Q.m,'Tây Ninh',CGOLD),la=pv63(Q.m,'Long An',CSTEEL);const l1=MLB(Q.m.top,'TÂY NINH',30,'#fff',OLN),l2=MLB(Q.m.top,'LONG AN',30,'#fff',OLN),l3=MLB(Q.m.top,'TÂY NINH',48,'#fff',CRED);const pt=PIN(Q.m,'TRỤ SỞ: PHƯỜNG LONG AN',CRED,-30,28);const tl=AT(10,'Long',2.2),tg=AT(10,'giữ',3.6),tt=AT(10,'trụ',5.6);bm(tl);bm(tg,true);bm(tt);
 return{upd:t=>{const e=MON(Q,t,10,310,330,[106.25,11.05]);const mg=inn(t,tg-.2,.6);tn.setAttribute('opacity',e*(1-.5*mg));la.setAttribute('opacity',popv(t,tl,.4)*(1-.5*mg));labAt(Q.m,l1,[106.15,11.45],e*(1-mg));labAt(Q.m,l2,[106.2,10.75],popv(t,tl,.45)*(1-mg));Q.m.hi('Tây Ninh',mg*(.75+.2*Math.sin(t*3)),CGOLD);labAt(Q.m,l3,[106.15,11.2],popv(t,tg,.45));PINAT(Q.m,pt,TANAN,popv(t,tt,.45))}}});
// 11 cái tên phía tây nay trải từ biên giới xuống tận hạ lưu sông Vàm Cỏ
S2(11,11,'d',null,g=>{const Q=MAPY(111);const ln=MLINE(Q.m,[[106.0,11.85],[106.15,11.3],[106.3,10.9],[106.45,10.6],[106.65,10.45]],'#fff',12);const A=strip('TỪ BIÊN GIỚI',false,40,111),B=strip('XUỐNG TẬN SÔNG VÀM CỎ',true,40,112);const tb=AT(11,'biên',2.0),tv=AT(11,'Vàm',4.0);bm(tb);bm(tv,true);
 return{upd:t=>{const e=MON(Q,t,11,300,280,[106.25,11.1]);Q.m.hi('Tây Ninh',e*(.4+.15*Math.sin(t*3)),CGOLD);ln(inn(t,tb-.3,2.4));sh(A,t,540,300,-2,popv(t,tb,.45));sh(B,t,540,1150,2,popv(t,tv,.45))}}});
// 12 gần 200 năm trước chỉ là vùng biên rừng rậm; nay tên ấy phủ một tỉnh rộng hơn gấp đôi
S2(12,12,'p',null,g=>{const n=CNT(g,CGOLD,110);const s1=el(g,'rect',{x:-110,y:-110,width:220,height:220,rx:14,fill:CSTEEL,stroke:'#fff','stroke-width':8}),s2=el(g,'rect',{x:-160,y:-160,width:320,height:320,rx:18,fill:CGOLD,stroke:'#fff','stroke-width':8});const a=T(g,0,0,'TỈNH CŨ',40,'#fff',6,'middle',OLN),b=T(g,0,0,'TỈNH MỚI',44,'#fff',6,'middle',OLN);const A=strip('RỘNG HƠN GẤP ĐÔI',true,44,121);const th=AT(12,'hai',.3),tr=AT(12,'rộng',5.4),tn=AT(12,'nay',3.8);bm(th,true);bm(tr);
 return{upd:t=>{n.textContent=Math.round(189*inn(t,th,1.4))+' năm';PUT(n,540,380,popv(t,th,.4),.9,0);PUT(s1,300,760,popv(t,R(12)+.6,.45),1,-3);PUT(a,300,770,popv(t,R(12)+.6,.45),1,-3);PUT(s2,740,760,popv(t,tn,.45),1,3);PUT(b,740,770,popv(t,tn,.45),1,3);sh(A,t,540,1120,2,popv(t,tr,.45))}}});
// 13 câu hỏi: núi Bà Đen, Tân An bên sông Vàm Cỏ (chibi vẫy tay)
S2(13,13,'d',null,g=>{const pk=PEAKS(g,'#4f6e5c');const wv=WAVES(g,440);const nd=NONG_DAN(g),cg=CO_GIAO(g);const A=strip('NÚI BÀ ĐEN',false,38,131),B=strip('SÔNG VÀM CỎ',false,38,132),C=strip('BẠN ĐÃ ĐẾN CHƯA?',true,42,133);const t1=AT(13,'núi',1.0),t2=AT(13,'Tân',2.6);bm(AT(13,'Bạn',.3));bm(t1);bm(t2,true);
 return{upd:t=>{sh(C,t,540,330,-2,PV(t,13,'Bạn',.3));SH(pk,300,760,.6*popv(t,t1-.2,.45));sh(A,t,300,830,-2,popv(t,t1,.45));SH(wv.k,780,700,.8*popv(t,t2-.2,.45));wv.u(t);sh(B,t,780,830,2,popv(t,t2,.45));nd.set(t,{wave:1,look:6});nd.at(330,1690,.66*popv(t,R(13)+.2,.45));cg.set(t,{wave:1,look:-6});cg.at(760,1690,.7*popv(t,R(13)+.4,.45),-1)}}},9999);
