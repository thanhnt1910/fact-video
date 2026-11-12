// ===== TÊN TỈNH THÀNH #06: Cần Thơ (tn6). Bản đồ hành chính phẳng 34 tỉnh (geoBoundaries, phạm vi công cộng), không vẽ nước láng giềng.
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
// ===== Dấu ấn riêng (Cần Thơ): nền tối xanh lá dừa, giấy vàng lúa; ghe chợ nổi có cây bẹo và cầu dây văng mờ ở đáy; sông Hậu chảy (y>1640)
{DR1.setAttribute('opacity',0);DR2.setAttribute('opacity',0);
 DARKG.firstChild.setAttribute('fill','#16220f');
 [...PAPG.children].forEach(c=>{if(c.tagName=='g')c.setAttribute('opacity',0);if(c.tagName=='line')c.setAttribute('stroke','rgba(0,0,0,0)')});
 PAPG.firstChild.setAttribute('fill','#efe6c4');
 const dots=(p,col)=>{const g=el(p,'g',{});const r=rng(606);for(let i=0;i<80;i++)el(g,'circle',{cx:r()*1080,cy:200+r()*1300,r:1.5+r()*2.5,fill:col});return g};
 dots(DARKG,'rgba(190,220,140,.06)');dots(PAPG,'rgba(130,110,50,.10)');
 const sky=(p,col)=>{const g=el(p,'g',{});const L=(d,w=5)=>el(g,'path',{d,fill:'none',stroke:col,'stroke-width':w,'stroke-linejoin':'round','stroke-linecap':'round'});
  // cầu dây văng: hai tháp chữ A, dây xòe
  L('M560 1630 L1100 1630',6);for(const x of[700,940]){L(`M${x-30} 1630 L${x} 1380 L${x+30} 1630`,6);for(let k=1;k<=5;k++){L(`M${x} ${1400+k*8} L${x-k*26} 1630`,2);L(`M${x} ${1400+k*8} L${x+k*26} 1630`,2)}}
  // ghe chợ nổi có cây bẹo treo trái cây
  for(const[x,s]of[[120,1],[330,.8]]){L(`M${x-90*s} 1600 Q${x} ${1640} ${x+90*s} 1600 Z`,5);L(`M${x} 1600 L${x} ${1600-150*s}`,4);el(g,'circle',{cx:x+8,cy:1600-140*s,r:10*s,fill:'none',stroke:col,'stroke-width':4});el(g,'circle',{cx:x-8,cy:1600-118*s,r:9*s,fill:'none',stroke:col,'stroke-width':4})}
  return g};
 const skA=sky(DARKG,'rgba(224,166,60,.16)'),skB=sky(PAPG,'rgba(90,80,40,.18)');
 const wv=(p,col)=>[0,1,2].map(i=>el(p,'path',{fill:'none',stroke:col,'stroke-width':4+i,opacity:.6-i*.12}));
 const wA=wv(DARKG,'rgba(200,170,110,.35)'),wB=wv(PAPG,'rgba(120,90,40,.30)');
 window.THEME_UPD=t=>{const dx=Math.sin(t*.1)*14;skA.setAttribute('transform',`translate(${dx.toFixed(1)},0)`);skB.setAttribute('transform',`translate(${dx.toFixed(1)},0)`);[wA,wB].forEach(L=>L.forEach((e,i)=>{const y0=1690+i*62;let d='';for(let x=-20;x<=1100;x+=28){const y=y0+Math.sin(x*.012+t*(1.0+i*.3)+i)*9;d+=(x<0?'M':'L')+x+' '+y.toFixed(1)}e.setAttribute('d',d)}))};
}
// ===== CẢNH
const CTH=[105.77,10.03];
const SEAH=()=>[strip('QĐ. HOÀNG SA (VIỆT NAM) ↗',false,22,901),strip('QĐ. TRƯỜNG SA (VIỆT NAM) →',false,22,902),strip('RANH GIỚI HIỆN NAY',false,20,903)];
const seaH=(L,t,e,lab)=>{sh(L[0],t,840,1180,0,e);sh(L[1],t,840,1235,0,e);sh(L[2],t,250,1235,0,e*(lab===false?0:1))};
// cá sặc rằn vẽ phẳng (thân dẹt, sọc chéo, vây lưng dài)
const FISH=(g,col='#8a9a5a')=>{const k=el(g,'g',{});el(k,'path',{d:'M-150 0 Q-60 -90 80 -40 L150 -80 L140 0 L150 80 L80 40 Q-60 90 -150 0Z',fill:col,stroke:'#fff','stroke-width':7,'stroke-linejoin':'round'});
 for(let i=0;i<5;i++)el(k,'path',{d:`M${-90+i*34} -48 L${-110+i*34} 48`,stroke:'rgba(30,40,20,.55)','stroke-width':9,'stroke-linecap':'round'});
 el(k,'path',{d:'M-70 -62 Q10 -110 70 -48',fill:'none',stroke:'#fff','stroke-width':6});el(k,'circle',{cx:-110,cy:-12,r:12,fill:'#fff'});el(k,'circle',{cx:-112,cy:-12,r:6,fill:OLN});return k};
const LUTE=(g)=>{const k=el(g,'g',{});el(k,'circle',{cx:0,cy:40,r:70,fill:'#b5703a',stroke:'#fff','stroke-width':7});el(k,'circle',{cx:0,cy:40,r:16,fill:'#3a2414'});el(k,'rect',{x:-12,y:-190,width:24,height:170,fill:'#7a4a24',stroke:'#fff','stroke-width':5});for(let i=0;i<3;i++)el(k,'line',{x1:-26,y1:-170+i*20,x2:26,y2:-170+i*20,stroke:'#fff','stroke-width':5});return k};
const NOTE=(g)=>{const t=T(g,0,0,'♪',90,CGOLD,8,'middle',OLN);return t};
const BOOK=(g,txt)=>{const bk=el(g,'g',{});el(bk,'rect',{x:-300,y:-220,width:600,height:440,rx:14,fill:'#efe3c2',stroke:OLN,'stroke-width':8});el(bk,'path',{d:'M0 -220 L0 220',stroke:OLN,'stroke-width':6});for(let s of[-1,1])for(let i=0;i<7;i++)if(!(s==1&&i==2))el(bk,'rect',{x:s<0?-270:30,y:-170+i*52,width:230-(i%3)*40,height:12,rx:6,fill:'rgba(60,40,20,.3)'});
 const hl=el(bk,'rect',{x:24,y:-70,width:0,height:56,rx:8,fill:CGOLD});const ht=MLB(bk,txt,26,OLN,CGOLD);ht.setAttribute('x',150);ht.setAttribute('y',-32);return{bk,hl,ht}};
const WORD=(g,txt,sz,col='#fff')=>T(g,0,sz*.36,txt,sz,col,Math.round(sz*.09),'middle',OLN);
// 1 hook: chuyện chúa Nguyễn nghe đàn hát đặt tên Cần Thơ chỉ là lời kể dân gian
S2(1,1,'d',null,g=>{const m=vnmap(560,820,61);const hs=hsts(m);const rg=RINGS(m.top,CGOLD);const A=strip('CẦN THƠ',true,62,11);const lu=LUTE(g);const ns=[0,1,2].map(()=>NOTE(g));const st=stamp('LỜI KỂ DÂN GIAN',46);const tl=AT(1,'lời',4.4);bm(tl);
 return{upd:t=>{const e=inn(t,R(1)-.2,.5);m.at(330,740,-1,1,e);m.view(108.7,15.9,44+6*inn(t,R(1),E(1)-R(1)));hs(e);m.hi('Cần Thơ',inn(t,AT(1,'Cần',3.6),.5),CRED);const[x,y]=m.P(...CTH);RU(rg,t,90,x,y,inn(t,AT(1,'Cần',3.6),.4));
  sh(A,t,820,400,-3,PV(t,1,'Cần',3.6));PUT(lu,820,700,popv(t,AT(1,'đàn',2.2)-.2,.5),.8,Math.sin(t*2)*5);ns.forEach((n,i)=>{const u=((t*.6+i/3)%1);PUT(n,860+i*40-40,640-u*200,inn(t,AT(1,'đàn',2.2),.4)*(1-u),.6,0)});const su=popv(t,tl,.45);st.at(850,1010,-6,su*.9,su>0?1:0)}}});
// 2 theo lời kể: Nguyễn Ánh chạy trốn quân Tây Sơn, nghe tiếng đàn và ngâm thơ bên bờ
S2(2,2,'p',null,g=>{const moon=el(g,'circle',{cx:820,cy:420,r:70,fill:'#f3e7b8',stroke:'#fff','stroke-width':5});const rv=[0,1,2].map(i=>el(g,'path',{fill:'none',stroke:RIV,'stroke-width':8-i*2,'stroke-linecap':'round'}));const sp=el(g,'g',{});drawShip(sp);const lu=LUTE(g);const ns=[0,1,2].map(()=>NOTE(g));
 const A=strip('THEO LỜI KỂ',false,40,21),B=strip('NGUYỄN ÁNH',true,44,22),C=strip('CHẠY TRỐN QUÂN TÂY SƠN',false,34,23);
 return{upd:t=>{moon.setAttribute('opacity',inn(t,R(2),.6));rv.forEach((e,i)=>{let d='';for(let x=40;x<=1040;x+=16)d+=(x==40?'M':'L')+x+' '+(860+i*30+Math.sin(x*.02+t*2+i)*10).toFixed(1);e.setAttribute('d',d);e.setAttribute('opacity',inn(t,R(2),.5))});
  const u=inn(t,AT(2,'chạy',2.0)-.3,4);PUT(sp,lerp(120,560,u),830+Math.sin(t*2)*6,inn(t,R(2)+.2,.4),2,0);sh(A,t,300,380,-2,inn(t,R(2)+.05,.4));sh(B,t,320,470,2,PV(t,2,'Nguyễn',1.2));sh(C,t,540,1120,-1,PV(t,2,'Tây',3.0));
  PUT(lu,860,1020,popv(t,AT(2,'đàn',4.6),.5),.6,Math.sin(t*2)*5);ns.forEach((n,i)=>{const v=((t*.6+i/3)%1);PUT(n,880+i*40-40,960-v*220,inn(t,AT(2,'đàn',4.6),.4)*(1-v),.6,0)})}}});
// 3 Cầm Thi Giang: sông của đàn và thơ; đọc trại thành Cần Thơ
S2(3,3,'d',null,g=>{const W=[['CẦM','ĐÀN'],['THI','THƠ'],['GIANG','SÔNG']].map(([a,b],i)=>({a:WORD(g,a,96,CGOLD),b:strip(b,false,34,31+i)}));const w2=WORD(g,'CẦM THI',90,'#fff'),w3=WORD(g,'CẦN THƠ',110,CGOLD);const ar=arrow(g,540,880,540,960);const C=strip('ĐỌC TRẠI',true,40,35);const td=AT(3,'Đọc',4.0);bm(td+.6,true);
 return{upd:t=>{W.forEach((o,i)=>{const x=200+i*340;PUT(o.a,x,520,popv(t,AT(3,'Cầm',1.6)+i*.25,.5),1,0);sh(o.b,t,x,640,i%2?2:-2,popv(t,AT(3,'đàn',3.0)-.3+i*.25,.45))});
  PUT(w2,540,800,popv(t,td,.5),1,0);ar.set(inn(t,td+.4,.4));PUT(w3,540,1060,popv(t,td+.7,.5),1,Math.sin(t*2.6)*2);sh(C,t,860,920,-3,popv(t,td+.4,.5))}}});
// 4 nhà nghiên cứu ĐH Cần Thơ: không sách sử cũ nào ghi tên Cầm Thi
S2(4,4,'p',null,g=>{const b=BOOK(g,'CẦM THI?');const x1=XX(g);const A=strip('NGHE RẤT THƠ MỘNG',false,36,41),B=strip('NHÀ NGHIÊN CỨU · ĐH CẦN THƠ',false,32,42);const st=stamp('KHÔNG SÁCH SỬ NÀO GHI',44);const tk=AT(4,'không',4.0);bm(tk);
 return{upd:t=>{sh(A,t,540,360,-2,popv(t,R(4)+.05,.5)*(1-inn(t,AT(4,'Nhưng',1.2),.3)));sh(B,t,540,360,1,PV(t,4,'Đại',2.6));PUT(b.bk,540,700,popv(t,AT(4,'Nhưng',1.2),.55),.95,-2+Math.sin(t*1.4));const u=inn(t,AT(4,'Đại',2.6),.6);b.hl.setAttribute('width',250*u);b.ht.setAttribute('opacity',u);
  PUT(x1,880,520,popv(t,tk+.2,.4),.7,0);const su=popv(t,tk,.45);st.at(540,1060,-5,su,su>0?1:0)}}});
// 5 nếu chúa đặt tên chữ Hán đẹp như Cầm Thi, người ta sẽ giữ nguyên, không đọc trại
S2(5,5,'d',null,g=>{const s=SIGN(g,'CẦM THI','#1d5a46');const ck=CK(g);const w=WORD(g,'CẦN THƠ',80,'#fff');const x1=XX(g);const A=strip('NẾU CHÚA ĐÃ ĐẶT',false,38,51),B=strip('THÌ SẼ GIỮ NGUYÊN',true,42,52),C=strip('KHÔNG ĐỌC TRẠI',false,36,53);const tg=AT(5,'giữ',4.4);bm(tg,true);
 return{upd:t=>{sh(A,t,540,360,-2,PV(t,5,'Nếu',1.2));PUT(s.k,540,560,popv(t,AT(5,'Hán',2.6)-.3,.55),1.1,Math.sin(t*1.6)*1.5);PUT(ck,860,470,popv(t,tg,.4),.7,0);sh(B,t,540,800,1,popv(t,tg,.5));
  PUT(w,540,1000,popv(t,AT(5,'đọc',5.2)-.2,.5),1,0);PUT(x1,540,1000,popv(t,AT(5,'đọc',5.2)+.2,.4),1.1,0);sh(C,t,540,1140,-1,PV(t,5,'đọc',5.2))}}});
// 6 sách địa chí đầu thế kỷ 19: Cần Thơ là tên một con sông
S2(6,6,'p',null,g=>{const q=T(g,0,0,'?',150,CGOLD,12,'middle',OLN);const dc=SCRL(g,420,320);const lab=MLB(dc,'CẦN THƠ GIANG',34,CRED,'#e8dcba');lab.setAttribute('y',-100);const rv=[0,1].map(i=>el(g,'path',{fill:'none',stroke:RIV,'stroke-width':12-i*4,'stroke-linecap':'round'}));
 const A=strip('SÁCH ĐỊA CHÍ ĐẦU THẾ KỶ 19',false,34,61),B=strip('TÊN MỘT CON SÔNG',true,46,62);const ts=AT(6,'sông',5.4);bm(ts);
 return{upd:t=>{PUT(q,540,560,popv(t,R(6)+.05,.5)*(1-inn(t,AT(6,'sách',2.0)-.2,.3)),1,Math.sin(t*3)*6);PUT(dc,540,640,popv(t,AT(6,'sách',2.0),.55),1,-2+Math.sin(t*1.4));sh(A,t,540,380,-2,PV(t,6,'sách',2.0));
  const u=inn(t,ts-.3,.8);rv.forEach((e,i)=>{let d='';for(let x=100;x<=100+880*u;x+=14)d+=(x==100?'M':'L')+x+' '+(960+i*26+Math.sin(x*.025+t*2.5+i)*10).toFixed(1);e.setAttribute('d',d)});sh(B,t,540,1100,1,popv(t,ts,.5))}}});
// 7 nhiều nhà nghiên cứu: gốc tiếng Khmer, chữ Kìn Tho, tên một loài cá
S2(7,7,'d',null,g=>{const w1=WORD(g,'KÌN THO',100,CGOLD),w2=WORD(g,'CẦN THƠ',100,'#fff');const ar=arrow(g,540,610,540,700);const A=strip('NHIỀU NHÀ NGHIÊN CỨU',false,34,71),B=strip('TIẾNG KHMER',true,44,72),C=strip('TÊN MỘT LOÀI CÁ',false,40,73);const f=FISH(g);const tf=AT(7,'cá',5.2);bm(tf);
 return{upd:t=>{sh(A,t,540,360,-2,popv(t,R(7)+.05,.5));sh(B,t,540,440,2,PV(t,7,'Khmer',2.8));PUT(w1,540,560,popv(t,AT(7,'Kìn',3.6)-.2,.5),1,0);ar.set(inn(t,AT(7,'Kìn',3.6)+.3,.4));PUT(w2,540,780,popv(t,AT(7,'Kìn',3.6)+.6,.5),1,0);
  PUT(f,lerp(1300,540,inn(t,tf-.5,.8)),980+Math.sin(t*3)*10,1,.9,Math.sin(t*4)*4);sh(C,t,540,1150,-1,popv(t,tf,.5))}}});
// 8 loài cá ấy: cá sặc rằn, ngày xưa có rất nhiều ở vùng này
S2(8,8,'p',null,g=>{const big=FISH(g);const sm=[...Array(9)].map((_,i)=>FISH(g,['#8a9a5a','#9aa86a','#7a8a4a'][i%3]));const rv=[0,1,2].map(i=>el(g,'path',{fill:'none',stroke:RIV,'stroke-width':6,'stroke-linecap':'round',opacity:.6}));const A=strip('CÁ SẶC RẰN',true,60,81),B=strip('NGÀY XƯA CÓ RẤT NHIỀU',false,38,82);const ts=AT(8,'sặc',2.6);bm(ts);
 return{upd:t=>{PUT(big,540,560,popv(t,R(8)+.1,.55),1.6,Math.sin(t*3)*4);sh(A,t,540,820,-2,popv(t,ts,.5));const u=inn(t,AT(8,'nhiều',4.4)-.4,.8);
  sm.forEach((f,i)=>{const yy=930+(i%3)*90,sp=60+i*7;const x=((t*sp+i*160)%1300)-110;PUT(f,1180-x,yy+Math.sin(t*3+i)*8,u,.35,0)});rv.forEach((e,i)=>{let d='';for(let x=0;x<=1080;x+=20)d+=(x==0?'M':'L')+x+' '+(920+i*90+Math.sin(x*.02+t*2+i)*8).toFixed(1);e.setAttribute('d',d);e.setAttribute('opacity',.5*u)});sh(B,t,540,1220,1,PV(t,8,'nhiều',4.4))}}});
// 9 tính ra: chưa chắc là dòng sông của đàn và thơ, rất có thể là dòng sông của cá sặc
S2(9,9,'d',null,g=>{const lu=LUTE(g);const ns=[0,1].map(()=>NOTE(g));const f=FISH(g);const q=T(g,0,0,'?',120,'#fff',10,'middle',OLN);const ck=CK(g);const A=strip('SÔNG CỦA ĐÀN VÀ THƠ',false,34,91),B=strip('SÔNG CỦA CÁ SẶC',true,42,92);const tc=AT(9,'mà',3.6);bm(tc);
 return{upd:t=>{const L=popv(t,AT(9,'đàn',2.0)-.4,.5);PUT(lu,270,650,L,.85,Math.sin(t*2)*4);ns.forEach((n,i)=>PUT(n,330+i*50,520-i*30,L,.6,0));sh(A,t,270,900,-2,L);PUT(q,270,1040,popv(t,AT(9,'đàn',2.0),.4),.7,Math.sin(t*3)*6);
  PUT(f,800,650,popv(t,tc-.2,.5),.9,Math.sin(t*4)*4);sh(B,t,800,900,2,popv(t,tc,.5));PUT(ck,800,1040,popv(t,tc+.3,.4),.7,0)}}});
// 10 năm 1739 Mạc Thiên Tích lập đạo Trấn Giang (thủ sở bên bờ sông Hậu)
S2(10,10,'p',t=>t<AT(10,'Mạc',4.4)-.6?null:'1739',g=>{const m=vnmap(960,880,101);const rg=RINGS(m.top,CGOLD);const ft=el(m.top,'g',{});FORT(ft);const lab=MLB(m.top,'ĐẠO TRẤN GIANG',34,'#fff',CRED);const A=strip('TỪNG MANG TÊN KHÁC',false,38,101),B=strip('MẠC THIÊN TÍCH',true,42,102);const SH=SEAH();const tt=AT(10,'Trấn',6.0);bm(tt);
 return{upd:t=>{const e=inn(t,R(10)-.2,.5);m.at(540,760,0,1,e);m.view(105.8,10.0,lerp(220,260,inn(t,R(10),E(10)-R(10))));seaH(SH,t,e);const[x,y]=m.P(...CTH);RU(rg,t,80,x,y,inn(t,tt-.3,.4));ft.setAttribute('transform',`translate(${x},${y-20}) scale(${.35*popv(t,tt,.5)})`);lab.setAttribute('x',x);lab.setAttribute('y',y+70);lab.setAttribute('opacity',inn(t,tt,.4));
  sh(A,t,540,400,-2,PV(t,10,'tên',2.6));sh(B,t,540,480,1,PV(t,10,'Mạc',4.4))}}});
// 11 năm 1876 người Pháp lập hạt Cần Thơ; tên sông thành tên cả vùng
S2(11,11,'d',t=>'1876',g=>{const m=vnmap(960,880,111);const s=SIGN(g,'HẠT CẦN THƠ','#1d5a46');const ring=el(m.top,'circle',{fill:'rgba(242,193,78,.25)',stroke:CGOLD,'stroke-width':5});const A=strip('NGƯỜI PHÁP LẬP',false,38,111),B=strip('TÊN SÔNG → TÊN CẢ VÙNG',true,40,112);const SH=SEAH();bm(AT(11,'hạt',3.4));
 return{upd:t=>{const e=inn(t,R(11)-.2,.5);m.at(540,760,0,1,e);m.view(105.8,10.0,240);seaH(SH,t,e);const[x,y]=m.P(...CTH);const u=inn(t,AT(11,'Từ',4.2),1.6);ring.setAttribute('cx',x);ring.setAttribute('cy',y);ring.setAttribute('r',20+150*u);ring.setAttribute('opacity',u>0?1:0);
  sh(A,t,540,400,-2,PV(t,11,'Pháp',2.6));PUT(s.k,780,560,popv(t,AT(11,'hạt',3.4),.55),.75,Math.sin(t*1.6)*1.5);sh(B,t,540,1100,1,PV(t,11,'vùng',6.0,-.6))}}});
// 12 năm 2004 chia tỉnh Cần Thơ; thành phố Cần Thơ trực thuộc trung ương (ranh giới trước 2025, nét đứt)
S2(12,12,'p',t=>'2004',g=>{const m=vnmap(960,880,121);const old=['Cần Thơ','Hậu Giang'].map(n=>{const p=TINH63.find(q=>q.n==n);return el(m.riv,'path',{d:p.p.map(rpath).join(''),fill:n=='Cần Thơ'?'rgba(242,193,78,.75)':'rgba(255,255,255,.08)',stroke:'#fff8e6','stroke-width':3,'stroke-dasharray':'10 8','vector-effect':'non-scaling-stroke',opacity:0})});
 const L=[['TP CẦN THƠ',105.65,10.12],['HẬU GIANG',105.62,9.8]].map(([n,lo,la])=>({e:MLB(m.top,n,30,'#fff'),lo,la}));const A=strip('CHIA TỈNH CẦN THƠ',false,38,121),B=strip('TRỰC THUỘC TRUNG ƯƠNG',true,44,122);const H=strip('RANH GIỚI TRƯỚC NĂM 2025',false,20,123);const SH=SEAH();bm(AT(12,'trực',6.0));
 return{upd:t=>{const e=inn(t,R(12)-.2,.5);m.at(540,760,0,1,e);m.view(105.7,9.95,lerp(300,340,inn(t,R(12),E(12)-R(12))));seaH(SH,t,e,false);sh(H,t,250,1235,0,e);old.forEach((o,i)=>o.setAttribute('opacity',i==0?inn(t,AT(12,'thành',4.0),.4):e));L.forEach((o,i)=>{const[x,y]=m.P(o.lo,o.la);o.e.setAttribute('x',x);o.e.setAttribute('y',y);o.e.setAttribute('opacity',inn(t,AT(12,'chia',3.4)+i*.3,.4))});
  sh(A,t,540,400,-2,PV(t,12,'chia',3.4));sh(B,t,540,480,1,PV(t,12,'trực',6.0))}}});
// 13 năm 2025 nhập Sóc Trăng và Hậu Giang, vẫn giữ tên Cần Thơ
S2(13,13,'d',t=>'2025',g=>{const m=vnmap(960,880,131);const old=['Cần Thơ','Hậu Giang','Sóc Trăng'].map(n=>{const p=TINH63.find(q=>q.n==n);return el(m.riv,'path',{d:p.p.map(rpath).join(''),fill:'none',stroke:'#fff8e6','stroke-width':3,'stroke-dasharray':'10 8','vector-effect':'non-scaling-stroke',opacity:0})});
 const L=[['SÓC TRĂNG',105.95,9.55],['HẬU GIANG',105.55,9.8]].map(([n,lo,la])=>({e:MLB(m.top,n,28,'#fff'),lo,la}));const A=strip('VẪN GIỮ TÊN CẦN THƠ',true,46,131);const SH=SEAH();const tg=AT(13,'giữ',5.4);bm(tg);
 return{upd:t=>{const e=inn(t,R(13)-.2,.5);m.at(540,760,0,1,e);m.view(105.85,9.75,lerp(260,230,inn(t,R(13),E(13)-R(13))));seaH(SH,t,e);old.forEach((o,i)=>o.setAttribute('opacity',e*(i==0?1:inn(t,AT(13,i==2?'Sóc':'Hậu',4)-.2,.4))));
  L.forEach((o,i)=>{const[x,y]=m.P(o.lo,o.la);o.e.setAttribute('x',x);o.e.setAttribute('y',y);o.e.setAttribute('opacity',inn(t,AT(13,i==0?'Sóc':'Hậu',4)-.2,.4)*(1-inn(t,tg,.4)))});m.hi('Cần Thơ',inn(t,tg-.3,.6),CGOLD);sh(A,t,540,400,-2,popv(t,tg,.5))}}});
// 14 tóm lại: tên một con sông nhỏ, có lẽ tên một loài cá, thành tên thành phố hơn 4 triệu dân
S2(14,14,'p',null,g=>{const rv=[0,1].map(i=>el(g,'path',{fill:'none',stroke:RIV,'stroke-width':10-i*4,'stroke-linecap':'round'}));const f=FISH(g);const s=SIGN(g,'THÀNH PHỐ CẦN THƠ','#1d5a46');const a1=arrow(g,360,560,460,560),a2=arrow(g,600,620,630,730);const A=strip('HƠN 4 TRIỆU DÂN',true,46,141),N=strip('CÓ LẼ',false,28,142);bm(AT(14,'bốn',5.6));
 return{upd:t=>{const u=inn(t,AT(14,'sông',1.2)-.2,.6);rv.forEach((e,i)=>{let d='';for(let x=60;x<=60+280*u;x+=12)d+=(x==60?'M':'L')+x+' '+(560+i*24+Math.sin(x*.04+t*3+i)*8).toFixed(1);e.setAttribute('d',d)});
  a1.set(inn(t,AT(14,'cá',2.8)-.4,.3));PUT(f,580,560,popv(t,AT(14,'cá',2.8),.5),.65,Math.sin(t*4)*4);sh(N,t,580,460,-3,popv(t,AT(14,'cá',2.8),.4));a2.set(inn(t,AT(14,'thành',4.6)-.4,.3));PUT(s.k,640,820,popv(t,AT(14,'thành',4.6),.55),.85,Math.sin(t*1.6)*1.5);sh(A,t,540,1160,1,PV(t,14,'bốn',5.6))}}});
// 15 câu hỏi: chuyện dân gian hay hơn sự thật?
S2(15,15,'d',null,g=>{const c1=SCRL(g,320,260);const t1=MLB(c1,'CHUYỆN DÂN GIAN',30,CRED,'#e8dcba');t1.setAttribute('y',-80);const c2=SCRL(g,320,260);const t2=MLB(c2,'SỰ THẬT',34,'#1d5a46','#e8dcba');t2.setAttribute('y',-80);const vs=T(g,0,0,'VS',90,CGOLD,10,'middle',OLN);const A=strip('Ở QUÊ BẠN CÓ KHÔNG?',true,44,151);bm(R(15)+.2);
 return{upd:t=>{PUT(c1,270,640,popv(t,AT(15,'dân',2.0)-.4,.5),.85,-4+Math.sin(t*1.6)*2);PUT(vs,540,660,popv(t,AT(15,'sự',3.6)-.4,.4),1,0);PUT(c2,810,640,popv(t,AT(15,'sự',3.6)-.2,.5),.85,4+Math.sin(t*1.6+1)*2);sh(A,t,540,1080,-1,popv(t,R(15)+.2,.5))}}});
