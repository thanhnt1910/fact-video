// ===== TÊN TỈNH THÀNH #03: Huế (tn3). Bản đồ hành chính phẳng 34 tỉnh (geoBoundaries, phạm vi công cộng), không vẽ nước láng giềng.
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
const HN=[105.82,21.03],HUE=[107.58,16.46],KB=[105.87,20.56],DT=[105.97,20.63];
const SHONG=[[105.42,21.3],[105.55,21.2],[105.684,21.15],[105.782,21.1],[105.847,21.05],[105.893,21.0],[105.887,20.95],[105.904,20.9],[105.91,20.85],[105.929,20.8],[105.964,20.75],[106.025,20.7],[106.031,20.65],[106.125,20.6],[106.162,20.55],[106.177,20.5],[106.213,20.45],[106.271,20.4],[106.288,20.35],[106.432,20.3]];
const SDAY=[[105.40,21.13],[105.58,21.06],[105.66,20.98],[105.71,20.90],[105.74,20.78],[105.77,20.68],[105.84,20.60],[105.91,20.54],[105.96,20.42],[105.99,20.33]];
const BOX=(g,txt)=>{const k=el(g,'g',{});el(k,'rect',{x:-130,y:-70,width:260,height:140,rx:10,fill:'#c89b5a',stroke:'#fff','stroke-width':7});el(k,'path',{d:'M-130 -20 L130 -20',stroke:'#7a5a2e','stroke-width':6});const t=MLB(k,txt,42,'#fff');t.setAttribute('y',36);return k};
const SIGN=(g,txt,col='#1d5a46')=>{const k=el(g,'g',{});el(k,'rect',{x:-8,y:0,width:16,height:240,fill:'#9aa3ab',stroke:'#fff','stroke-width':4});el(k,'rect',{x:-230,y:-80,width:460,height:96,rx:12,fill:col,stroke:'#fff','stroke-width':7});const t=MLB(k,txt,44,'#fff',col);t.setAttribute('y',-16);return{k,t}};
// ===== Dấu ấn riêng (Huế): nền tối tím than, giấy hồng ngà; nét Ngọ Môn và cầu Trường Tiền mờ ở đáy; sông Hương trôi chậm (y>1640)
{DR1.setAttribute('opacity',0);DR2.setAttribute('opacity',0);
 DARKG.firstChild.setAttribute('fill','#1d1730');
 [...PAPG.children].forEach(c=>{if(c.tagName=='g')c.setAttribute('opacity',0);if(c.tagName=='line')c.setAttribute('stroke','rgba(0,0,0,0)')});
 PAPG.firstChild.setAttribute('fill','#ece0cf');
 const dots=(p,col)=>{const g=el(p,'g',{});const r=rng(303);for(let i=0;i<70;i++)el(g,'circle',{cx:r()*1080,cy:200+r()*1300,r:2+r()*3,fill:col});return g};
 dots(DARKG,'rgba(200,170,230,.07)');dots(PAPG,'rgba(120,80,110,.08)');
 const sky=(p,col)=>{const g=el(p,'g',{});const L=(d,w=5)=>el(g,'path',{d,fill:'none',stroke:col,'stroke-width':w,'stroke-linejoin':'round','stroke-linecap':'round'});
  // Ngọ Môn: thành dưới có ba cửa vòm, lầu hai tầng mái cong phía trên
  {const x=640,y=1600;L(`M${x-320} ${y} L${x-320} ${y-150} L${x+320} ${y-150} L${x+320} ${y}`,6);
   for(const dx of[-150,0,150])L(`M${x+dx-40} ${y} L${x+dx-40} ${y-80} Q${x+dx} ${y-120} ${x+dx+40} ${y-80} L${x+dx+40} ${y}`,5);
   L(`M${x-220} ${y-150} L${x-220} ${y-220} L${x+220} ${y-220} L${x+220} ${y-150}`,5);
   L(`M${x-260} ${y-220} Q${x-200} ${y-238} ${x-150} ${y-262} L${x+150} ${y-262} Q${x+200} ${y-238} ${x+260} ${y-220}`,6);
   L(`M${x-130} ${y-262} L${x-130} ${y-310} L${x+130} ${y-310} L${x+130} ${y-262}`,5);
   L(`M${x-170} ${y-310} Q${x-120} ${y-326} ${x-80} ${y-350} L${x+80} ${y-350} Q${x+120} ${y-326} ${x+170} ${y-310}`,6)}
  // cầu Trường Tiền: sáu nhịp vòm thép
  {const y=1640;for(let i=0;i<6;i++){const x0=-10+i*52;L(`M${x0} ${y} Q${x0+26} ${y-58} ${x0+52} ${y}`,4)}L(`M-10 ${y} L302 ${y}`,5)}
  return g};
 const skA=sky(DARKG,'rgba(224,166,60,.15)'),skB=sky(PAPG,'rgba(110,70,100,.16)');
 const wv=(p,col)=>[0,1,2].map(i=>el(p,'path',{fill:'none',stroke:col,'stroke-width':4+i,opacity:.55-i*.12}));
 const wA=wv(DARKG,'rgba(160,140,220,.40)'),wB=wv(PAPG,'rgba(110,80,140,.30)');
 window.THEME_UPD=t=>{const dx=Math.sin(t*.1)*16;skA.setAttribute('transform',`translate(${dx.toFixed(1)},0)`);skB.setAttribute('transform',`translate(${dx.toFixed(1)},0)`);[wA,wB].forEach(L=>L.forEach((e,i)=>{const y0=1690+i*62;let d='';for(let x=-20;x<=1100;x+=30){const y=y0+Math.sin(x*.010+t*(.8+i*.25)+i)*10;d+=(x<0?'M':'L')+x+' '+y.toFixed(1)}e.setAttribute('d',d)}))};
}
// ===== CẢNH
const THC=[107.17,16.78],HOC=[107.55,16.50];   // thành Thuận Châu (Triệu Phong, Quảng Trị), thành Hóa Châu (Hương Vinh, Huế): chấm địa danh có nguồn
const GIFT=(g,col=CRED)=>{const k=el(g,'g',{});const b=el(k,'g',{});el(b,'rect',{x:-120,y:-60,width:240,height:170,rx:10,fill:col,stroke:'#fff','stroke-width':7});el(b,'rect',{x:-20,y:-60,width:40,height:170,fill:CGOLD,stroke:'#fff','stroke-width':4});
 const lid=el(k,'g',{});el(lid,'rect',{x:-140,y:-110,width:280,height:56,rx:10,fill:col,stroke:'#fff','stroke-width':7});el(lid,'rect',{x:-22,y:-110,width:44,height:56,fill:CGOLD,stroke:'#fff','stroke-width':4});
 el(lid,'path',{d:'M0 -110 C-70 -190 -110 -120 0 -112 C110 -120 70 -190 0 -110Z',fill:CGOLD,stroke:'#fff','stroke-width':5});return{k,lid}};
const TOWER=(g,col='#b5703a')=>{const k=el(g,'g',{});el(k,'path',{d:'M-90 120 L-90 -40 L-60 -40 L-60 -120 L-30 -120 L-30 -190 L0 -230 L30 -190 L30 -120 L60 -120 L60 -40 L90 -40 L90 120Z',fill:col,stroke:'#fff','stroke-width':7,'stroke-linejoin':'round'});el(k,'path',{d:'M-26 120 L-26 40 Q0 10 26 40 L26 120Z',fill:'#3a2414',stroke:'#fff','stroke-width':5});return k};
const BOOK=(g,txt)=>{const bk=el(g,'g',{});el(bk,'rect',{x:-300,y:-220,width:600,height:440,rx:14,fill:'#efe3c2',stroke:OLN,'stroke-width':8});el(bk,'path',{d:'M0 -220 L0 220',stroke:OLN,'stroke-width':6});for(let s of[-1,1])for(let i=0;i<7;i++)if(!(s==1&&i==2))el(bk,'rect',{x:s<0?-270:30,y:-170+i*52,width:230-(i%3)*40,height:12,rx:6,fill:'rgba(60,40,20,.3)'});
 const hl=el(bk,'rect',{x:24,y:-70,width:0,height:56,rx:8,fill:CGOLD});const ht=MLB(bk,txt,28,OLN,CGOLD);ht.setAttribute('x',150);ht.setAttribute('y',-32);return{bk,hl,ht}};
const WORD=(g,txt,sz,col='#fff')=>{const t=T(g,0,sz*.36,txt,sz,col,Math.round(sz*.09),'middle',OLN);return t};
const SEAH=()=>[strip('QĐ. HOÀNG SA (VIỆT NAM) ↗',false,22,901),strip('QĐ. TRƯỜNG SA (VIỆT NAM) ↘',false,22,902),strip('RANH GIỚI HIỆN NAY',false,20,903)];
const seaH=(L,t,e)=>{sh(L[0],t,840,1180,0,e);sh(L[1],t,840,1235,0,e);sh(L[2],t,250,1235,0,e)};
// 1 hook: vùng đất Huế từng là sính lễ trong một đám cưới
S2(1,1,'d',null,g=>{const m=vnmap(560,820,31);const hs=hsts(m);const rg=RINGS(m.top,CGOLD);const A=strip('VÙNG ĐẤT HUẾ',true,60,11);const gf=GIFT(g);const B=strip('SÍNH LỄ CƯỚI?',false,46,12);const q=T(g,0,0,'?',150,CGOLD,12,'middle',OLN);
 const ts=AT(1,'sính',3.0);bm(ts);
 return{upd:t=>{const e=inn(t,R(1)-.2,.5);m.at(330,740,-1,1,e);m.view(108.7,15.9,44+6*inn(t,R(1),E(1)-R(1)));hs(e);m.hi('Huế',inn(t,AT(1,'Huế',1.4),.5),CRED);const[x,y]=m.P(...HUE);RU(rg,t,90,x,y,inn(t,AT(1,'Huế',1.4),.4));
  sh(A,t,800,400,-3,PV(t,1,'Huế',1.4));PUT(gf.k,810,700,popv(t,ts-.2,.55),1,Math.sin(t*3)*3);gf.lid.setAttribute('transform',`translate(0,${-30*inn(t,ts+.5,.4)}) rotate(${-14*inn(t,ts+.5,.4)})`);sh(B,t,810,900,2,popv(t,ts,.5));PUT(q,960,560,popv(t,AT(1,'đám',4.0),.5),.8,Math.sin(t*3)*6)}}});
// 2 ai cũng biết Huế là kinh đô; nhưng hơn 700 năm trước còn thuộc Chăm Pa
S2(2,2,'p',null,g=>{const ft=FORT(g);const cr=CROWN(g);const A=strip('KINH ĐÔ CẢ NƯỚC',false,44,21);const tw=TOWER(g);const B=strip('HƠN 700 NĂM TRƯỚC',true,46,22),C=strip('VƯƠNG QUỐC CHĂM PA',false,40,23);const tn=AT(2,'Nhưng',2.8);
 return{upd:t=>{const out=inn(t,tn,.4);PUT(ft,540,760,popv(t,R(2)+.1,.55)*(1-out),1,0);PUT(cr,540,500,popv(t,AT(2,'kinh',1.2),.5)*(1-out),.9,Math.sin(t*3)*4);sh(A,t,540,1000,-1,PV(t,2,'kinh',1.2)*(1-out));
  PUT(tw,540,760,popv(t,tn+.2,.55),1.2,Math.sin(t*1.4)*1);sh(B,t,540,420,-2,PV(t,2,'bảy',3.4));sh(C,t,540,1040,2,PV(t,2,'Chăm',5.8))}}});
// 3 năm 1306, vua Chăm Pa Chế Mân cưới công chúa Huyền Trân nhà Trần
S2(3,3,'d',t=>'1306',g=>{const a=fig(g,{hat:CGOLD}),b=fig(g,{hat:CRED});const A=strip('CHẾ MÂN',true,46,31),A2=strip('VUA CHĂM PA',false,30,32),B=strip('HUYỀN TRÂN',true,46,33),B2=strip('CÔNG CHÚA NHÀ TRẦN',false,30,34);const st=stamp('ĐÁM CƯỚI',58);const ts=AT(3,'cưới',4.8);bm(ts);
 return{upd:t=>{a.at(330,1000,1.25,0,popv(t,AT(3,'Chế',4.2)-.3,.5));sh(A,t,330,420,-2,PV(t,3,'Chế',4.2));sh(A2,t,330,490,1,PV(t,3,'vua',3.4));
  b.at(750,1000,1.25,0,popv(t,AT(3,'Huyền',5.6)-.3,.5));sh(B,t,750,420,2,PV(t,3,'Huyền',5.6));sh(B2,t,750,490,-1,PV(t,3,'Trần',6.6));const su=popv(t,ts,.45);st.at(540,1150,-5,su,su>0?1:0)}}});
// 4 sính lễ: hai vùng đất, châu Ô và châu Lý (chấm địa danh theo thành cổ, ranh giới hiện nay)
S2(4,4,'p',null,g=>{const m=vnmap(960,880,41);const rg1=RINGS(m.top,CRED),rg2=RINGS(m.top,CRED);const L1=MLB(m.top,'CHÂU Ô',34,'#fff',CRED),L2=MLB(m.top,'CHÂU LÝ',34,'#fff',CRED);const d1=el(m.top,'circle',{r:12,fill:CRED,stroke:'#fff','stroke-width':4}),d2=el(m.top,'circle',{r:12,fill:CRED,stroke:'#fff','stroke-width':4});
 const gf=GIFT(g);const A=strip('HAI VÙNG ĐẤT',true,48,41);const SH=SEAH();bm(AT(4,'Ô',4.0),true);bm(AT(4,'Lý',4.8),true);
 return{upd:t=>{const e=inn(t,R(4)-.2,.5);m.at(540,760,0,1,e);m.view(107.25,16.7,lerp(200,260,inn(t,R(4),E(4)-R(4))));seaH(SH,t,e);
  const[x1,y1]=m.P(...THC),[x2,y2]=m.P(...HOC);const u1=popv(t,AT(4,'Ô',4.0),.45),u2=popv(t,AT(4,'Lý',4.8),.45);d1.setAttribute('cx',x1);d1.setAttribute('cy',y1);d1.setAttribute('opacity',u1>0?1:0);d2.setAttribute('cx',x2);d2.setAttribute('cy',y2);d2.setAttribute('opacity',u2>0?1:0);
  L1.setAttribute('x',x1-30);L1.setAttribute('y',y1-30);L1.setAttribute('opacity',u1>0?1:0);L2.setAttribute('x',x2+40);L2.setAttribute('y',y2+60);L2.setAttribute('opacity',u2>0?1:0);RU(rg1,t,70,x1,y1,u1>0?1:0);RU(rg2,t,70,x2,y2,u2>0?1:0);
  PUT(gf.k,880,420,popv(t,R(4)+.1,.5)*(1-inn(t,AT(4,'hai',2.2)+.6,.4)),.6,Math.sin(t*3)*3);sh(A,t,540,400,-2,PV(t,4,'hai',2.2))}}});
// 5 món quà cưới vẽ lại bản đồ; Đại Việt mở rộng về phía nam (mũi tên minh họa)
S2(5,5,'d',null,g=>{const m=vnmap(960,880,51);const pa=m.line([[106.2,18.6],[106.6,17.9],[107.0,17.2],[107.35,16.6]],CGOLD,9,null);const A=strip('VẼ LẠI CẢ BẢN ĐỒ',true,50,51),B=strip('ĐẠI VIỆT MỞ RỘNG VỀ PHÍA NAM',false,36,52),N=strip('MŨI TÊN MINH HỌA',false,20,53);const gf=GIFT(g);const pen=el(g,'g',{});el(pen,'path',{d:'M0 0 L18 -70 L40 -64 L22 6Z',fill:CGOLD,stroke:'#fff','stroke-width':5});el(pen,'path',{d:'M0 0 L22 6 L8 30Z',fill:'#fff'});
 const SH=SEAH();const d1=el(m.top,'circle',{r:11,fill:CRED,stroke:'#fff','stroke-width':4}),d2=el(m.top,'circle',{r:11,fill:CRED,stroke:'#fff','stroke-width':4});bm(AT(5,'vẽ',1.8));
 return{upd:t=>{const e=inn(t,R(5)-.2,.5);m.at(540,760,0,1,e);m.view(106.9,17.4,150);seaH(SH,t,e);const[x1,y1]=m.P(...THC),[x2,y2]=m.P(...HOC);[[d1,x1,y1],[d2,x2,y2]].forEach(([d,x,y])=>{d.setAttribute('cx',x);d.setAttribute('cy',y);d.setAttribute('opacity',e)});
  PUT(gf.k,220,420,popv(t,AT(5,'quà',1.0),.5)*(1-inn(t,AT(5,'vẽ',1.8)+.4,.3)),.7,Math.sin(t*3)*4);const pu=inn(t,AT(5,'vẽ',1.8),1.4);PUT(pen,lerp(380,760,pu),lerp(520,900,pu)+Math.sin(t*14)*6,pu>0&&pu<1?1:0,1.2,0);
  sh(A,t,540,400,-2,PV(t,5,'vẽ',1.8));pa(inn(t,AT(5,'Đại',4.0),1.6));sh(B,t,540,1100,1,PV(t,5,'Đại',4.0));sh(N,t,860,470,0,inn(t,AT(5,'Đại',4.0),.4))}}});
// 6 năm 1307 Trần Anh Tông đổi tên: Ô thành Thuận, Lý thành Hóa
S2(6,6,'p',t=>'1307',g=>{const s1=SIGN(g,'CHÂU Ô','#6a5a48'),s2=SIGN(g,'CHÂU LÝ','#6a5a48');const A=strip('VUA TRẦN ANH TÔNG ĐỔI TÊN',false,38,61);const t1=AT(6,'Thuận',6.0),t2=AT(6,'Hóa',8.0);bm(t1,true);bm(t2,true);
 const flip=(s,tf,a,b,x,y)=>(t)=>{const fl=inn(t,tf-.3,.4);s.k.setAttribute('transform',`translate(${x},${y}) scale(${.92*Math.max(.02,Math.abs(1-2*fl))},.92)`);s.k.setAttribute('opacity',inn(t,R(6)+.1,.4));if(fl>.5){s.t.textContent=b;s.k.children[1].setAttribute('fill','#1d5a46')}else{s.t.textContent=a;s.k.children[1].setAttribute('fill','#6a5a48')}};
 const f1=flip(s1,t1,'CHÂU Ô','CHÂU THUẬN',290,760),f2=flip(s2,t2,'CHÂU LÝ','CHÂU HÓA',790,760);
 return{upd:t=>{f1(t);f2(t);sh(A,t,540,460,-2,PV(t,6,'vua',2.6))}}});
// 7 ghép lại: Thuận Hóa, gọi cả một vùng suốt mấy trăm năm
S2(7,7,'d',null,g=>{const A=strip('THUẬN',false,90,71),B=strip('HÓA',false,90,72),C=strip('THUẬN HÓA',true,90,73);const pl=T(g,0,0,'+',140,CGOLD,10,'middle',OLN);const D=strip('GỌI CẢ MỘT VÙNG ĐẤT',false,38,74),Ex=strip('SUỐT MẤY TRĂM NĂM',false,38,75);const mg=AT(7,'Thuận',1.6);bm(mg+.3);
 return{upd:t=>{const u=inn(t,mg,.6);sh(A,t,lerp(300,540,u),lerp(560,700,u),-3,popv(t,R(7)+.05,.5)*(1-u));sh(B,t,lerp(800,540,u),lerp(820,700,u),3,popv(t,R(7)+.3,.5)*(1-u));PUT(pl,540,700,popv(t,R(7)+.4,.4)*(1-u),1,0);sh(C,t,540,700,-1,popv(t,mg+.3,.55));
  sh(D,t,540,940,1,PV(t,7,'vùng',3.8));sh(Ex,t,540,1040,-1,PV(t,7,'trăm',5.2))}}});
// 8 chữ Huế từ đâu? Thuận Hóa → Hóa → Huế
S2(8,8,'p',null,g=>{const q=T(g,0,0,'HUẾ = ?',120,CGOLD,12,'middle',OLN);const w1=WORD(g,'THUẬN HÓA',96),w2=WORD(g,'HÓA',120,CGOLD),w3=WORD(g,'HUẾ',140,CGOLD);const ln=el(g,'path',{d:'M-232 0 L-12 0',stroke:CRED,'stroke-width':16,'stroke-linecap':'round'});const ar=arrow(g,540,800,540,900);const A=strip('NHIỀU NHÀ NGHIÊN CỨU CHO RẰNG',false,30,81),B=strip('GỌI TẮT',false,38,82),C=strip('ĐỌC TRẠI',true,42,83);
 const tt=AT(8,'tắt',4.0),td=AT(8,'trại',6.1);bm(td+.2);
 return{upd:t=>{const out=inn(t,AT(8,'Nhiều',1.8),.3);PUT(q,540,640,popv(t,R(8)+.1,.5)*(1-out),1,Math.sin(t*3)*3);sh(A,t,540,380,-1,PV(t,8,'Nhiều',1.8));
  PUT(w1,540,560,popv(t,tt-.2,.5),1,0);ln.setAttribute('transform','translate(540,556)');ln.setAttribute('opacity',inn(t,tt+.4,.3));sh(B,t,880,440,3,popv(t,tt,.5));
  PUT(w2,540,700,popv(t,tt+.6,.5),1,0);ar.set(inn(t,td-.2,.4));PUT(w3,540,1000,popv(t,td,.5),1.1,Math.sin(t*2.6)*2);sh(C,t,860,920,-3,popv(t,td,.5))}}});
// 9 như hòa nhau thành huề nhau: hai tiếng, một nghĩa (bảng tỉ số)
S2(9,9,'d',null,g=>{const bd=el(g,'g',{});el(bd,'rect',{x:-300,y:-170,width:600,height:340,rx:24,fill:'#1a2a1f',stroke:'#fff','stroke-width':8});const sc=T(bd,0,40,'1 – 1',150,'#f6efdc',0,'middle','none');sc.setAttribute('stroke','none');
 const s1=SIGN(g,'HÒA NHAU','#6a5a48');const A=strip('HAI TIẾNG NGHE KHÁC',false,38,91),B=strip('VẪN MỘT NGHĨA',true,44,92);const ck=CK(g);const th=AT(9,'huề',2.4);bm(th,true);
 return{upd:t=>{PUT(bd,540,560,popv(t,R(9)+.1,.5),1,Math.sin(t*1.4)*1);const fl=inn(t,th-.3,.4);s1.k.setAttribute('transform',`translate(540,880) scale(${Math.max(.02,Math.abs(1-2*fl))},1)`);s1.k.setAttribute('opacity',inn(t,AT(9,'hòa',1.4)-.2,.3));if(fl>.5){s1.t.textContent='HUỀ NHAU';s1.k.children[1].setAttribute('fill','#1d5a46')}else{s1.t.textContent='HÒA NHAU';s1.k.children[1].setAttribute('fill','#6a5a48')}
  sh(A,t,540,1160,1,PV(t,9,'Hai',3.2));sh(B,t,540,1240,-1,PV(t,9,'nghĩa',5.0));PUT(ck,860,400,popv(t,AT(9,'nghĩa',5.0)+.2,.4),.7,0)}}});
// 10 từ điển in năm 1651 ghi Hóa và Huế cùng một nghĩa
S2(10,10,'p',t=>'1651',g=>{const b=BOOK(g,'HÓA = HUẾ');const A=strip('TỪ ĐIỂN IN NĂM 1651',true,44,101),B=strip('CÙNG MỘT NGHĨA',false,40,102),N=strip('HÌNH MINH HỌA',false,20,103);const ck=CK(g);const th=AT(10,'Hóa',5.2);bm(th);
 return{upd:t=>{PUT(b.bk,540,720,popv(t,R(10)+.1,.55),1,-2+Math.sin(t*1.4));sh(A,t,540,400,-2,PV(t,10,'từ',1.2));const u=inn(t,th,.6);b.hl.setAttribute('width',250*u);b.ht.setAttribute('opacity',u);PUT(ck,820,560,popv(t,AT(10,'cùng',6.0),.4),.7,0);sh(B,t,540,1060,1,PV(t,10,'cùng',6.0));sh(N,t,860,1150,0,inn(t,R(10)+.4,.4))}}});
// 11 không do vua đặt, mà người dân tự gọi; tên dân gian
S2(11,11,'d',null,g=>{const cr=CROWN(g);const x1=XX(g);const pp=[0,1,2].map(i=>fig(g,{hat:[CGOLD,'#c9b48a',CRED][i]}));const bb=bubble(g,300,130,'HUẾ!',70);const A=strip('KHÔNG DO VUA ĐẶT',false,40,111),B=strip('NGƯỜI DÂN TỰ GỌI',true,46,112),C=strip('TÊN DÂN GIAN',false,40,113);const ck=CK(g);
 const tv=AT(11,'vua',1.8),tp=AT(11,'người',3.0);bm(tp);
 return{upd:t=>{PUT(cr,260,560,popv(t,R(11)+.1,.5),1,Math.sin(t*3)*4);PUT(x1,260,560,popv(t,tv+.2,.4),1,0);sh(A,t,260,740,-2,popv(t,tv,.5));
  pp.forEach((p,i)=>p.at(640+i*130,960,.95,0,popv(t,tp+i*.12,.5)));bb.at(800,520,1,popv(t,AT(11,'tự',3.6),.5));sh(B,t,770,1070,2,popv(t,tp+.3,.5));PUT(ck,960,400,popv(t,AT(11,'tự',3.6)+.3,.4),.6,0);sh(C,t,540,1200,-1,PV(t,11,'gian',6.6))}}});
// 12 năm 1802 Gia Long đóng đô ở Phú Xuân, trên đất Thuận Hóa cũ
S2(12,12,'p',t=>'1802',g=>{const m=vnmap(560,820,121);const hs=hsts(m);const rg=RINGS(m.top,CGOLD);const ft=FORT(g);const A=strip('VUA GIA LONG',false,40,121),B=strip('ĐÓNG ĐÔ Ở PHÚ XUÂN',true,44,122),C=strip('KINH ĐÔ CẢ NƯỚC',false,38,123),D=strip('TRÊN ĐẤT THUẬN HÓA CŨ',false,32,124);const td=AT(12,'đóng',3.4);bm(td);
 return{upd:t=>{const e=inn(t,R(12)-.2,.5);m.at(330,740,-1,1,e);m.view(108.7,15.9,46);hs(e);m.hi('Huế',inn(t,AT(12,'Phú',4.0),.5),CGOLD);const[x,y]=m.P(...HUE);RU(rg,t,80,x,y,inn(t,AT(12,'Phú',4.0),.4));
  sh(A,t,820,420,2,PV(t,12,'Gia',2.8));PUT(ft,820,700,popv(t,td,.55),.75,0);sh(B,t,820,900,-2,popv(t,td,.5));sh(C,t,820,990,1,PV(t,12,'Kinh',4.8));sh(D,t,820,1070,-1,PV(t,12,'Thuận',6.8))}}});
// 13 người dân vẫn gọi Huế; năm 1899 lập thị xã Huế, tên thành chính thức
S2(13,13,'d',t=>t<AT(13,'Đến',2.4)?null:'1899',g=>{const pp=[0,1].map(i=>fig(g,{hat:[CGOLD,CRED][i]}));const bb=bubble(g,300,130,'HUẾ',70);const s=SIGN(g,'THỊ XÃ HUẾ','#1d5a46');const st=stamp('TÊN CHÍNH THỨC',52);const A=strip('NGƯỜI DÂN VẪN GỌI',false,38,131);const tl=AT(13,'lập',5.2),tc=AT(13,'chính',7.4);bm(tc);
 return{upd:t=>{const out=inn(t,tl-.3,.4);pp.forEach((p,i)=>p.at(300+i*150,980,.9,0,popv(t,R(13)+.1+i*.15,.5)*(1-out)));bb.at(440,560,1,popv(t,AT(13,'gọi',1.0),.5)*(1-out));sh(A,t,380,1120,-1,PV(t,13,'gọi',1.0)*(1-out));
  PUT(s.k,540,620,popv(t,tl,.55),1.2,Math.sin(t*1.6)*1.5);const su=popv(t,tc,.45);st.at(540,1050,-6,su,su>0?1:0)}}});
// 14 năm 2025 thành phố trực thuộc trung ương, giữ nguyên tên khi sắp xếp tỉnh
S2(14,14,'p',t=>'2025',g=>{const m=vnmap(960,880,141);const rg=RINGS(m.top,CGOLD);const lab=MLB(m.top,'THÀNH PHỐ HUẾ',34,'#fff',OLN);const A=strip('TRỰC THUỘC TRUNG ƯƠNG',true,44,141),B=strip('GIỮ NGUYÊN TÊN',false,44,142);const SH=SEAH();const ck=CK(g);const tg=AT(14,'giữ',5.6);bm(AT(14,'trực',4.2));
 return{upd:t=>{const e=inn(t,R(14)-.2,.5);m.at(540,760,0,1,e);m.view(107.45,16.35,lerp(240,300,inn(t,R(14),E(14)-R(14))));seaH(SH,t,e);m.hi('Huế',inn(t,AT(14,'Huế',2.8),.5),CGOLD);const[x,y]=m.P(...HUE);RU(rg,t,80,x,y,inn(t,AT(14,'Huế',2.8),.4));lab.setAttribute('x',x);lab.setAttribute('y',y-60);lab.setAttribute('opacity',inn(t,AT(14,'Huế',2.8),.4));
  sh(A,t,540,400,-2,PV(t,14,'trực',4.2));sh(B,t,540,480,1,popv(t,tg,.5));PUT(ck,880,560,popv(t,tg+.3,.4),.6,0)}}});
// 15 tóm lại: sính lễ → chữ đọc trại → tên thành phố
S2(15,15,'d',null,g=>{const gf=GIFT(g);const w=WORD(g,'HÓA → HUẾ',70,CGOLD);const s=SIGN(g,'THÀNH PHỐ HUẾ','#1d5a46');const a1=arrow(g,330,590,330,710),a2=arrow(g,330,870,330,960);const A=strip('MỘT MÓN SÍNH LỄ',false,34,151),B=strip('MỘT CHỮ ĐỌC TRẠI',false,34,152),C=strip('TÊN CẢ MỘT THÀNH PHỐ',true,40,153);bm(AT(15,'phố',6.2));
 return{upd:t=>{PUT(gf.k,330,470,popv(t,AT(15,'sính',1.0)-.2,.5),.7,Math.sin(t*3)*3);sh(A,t,770,470,2,PV(t,15,'sính',1.0));a1.set(inn(t,AT(15,'chữ',2.2)-.3,.3));PUT(w,330,790,popv(t,AT(15,'chữ',2.2),.5),1,0);sh(B,t,800,790,-2,PV(t,15,'chữ',2.2));
  a2.set(inn(t,AT(15,'người',3.6),.3));PUT(s.k,330,1060,popv(t,AT(15,'người',3.6),.55),.8,Math.sin(t*1.6)*1.5);sh(C,t,780,1040,1,PV(t,15,'phố',6.2))}}});
// 16 câu hỏi cho người xem
S2(16,16,'p',null,g=>{const bx=BOX(g,'TÊN QUÊ BẠN?');const hs=[0,1,2].map(i=>{const k=el(g,'g',{});el(k,'rect',{x:-60,y:-40,width:120,height:90,fill:PAL[i*2],stroke:'#fff','stroke-width':5});el(k,'path',{d:'M-75 -40 L0 -100 L75 -40Z',fill:CRED,stroke:'#fff','stroke-width':5});return k});const bb=bubble(g,320,120,'GỌI MÃI…',54);const A=strip('THÀNH TÊN CHÍNH THỨC?',true,44,161);bm(R(16)+.2);
 return{upd:t=>{hs.forEach((k,i)=>PUT(k,250+i*290,900,popv(t,R(16)+.1+i*.15,.5),1,0));PUT(bx,540,600+Math.abs(Math.sin(t*3))*-30,popv(t,R(16)+.3,.5),1.4,Math.sin(t*3)*5);bb.at(780,760,.9,popv(t,AT(16,'gọi',2.4),.5));sh(A,t,540,1120,-1,PV(t,16,'chính',3.8))}}});
