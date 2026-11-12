// ===== TÊN TỈNH THÀNH #02: TP Hồ Chí Minh (tn2). Bản đồ hành chính phẳng 34 tỉnh (geoBoundaries, phạm vi công cộng), không vẽ nước láng giềng.
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
// ===== Dấu ấn riêng: nền tối xanh sông, giấy dó nhạt có đường đồng mức; sóng nước chảy ở đáy khung (y>1600)
{DR1.setAttribute('opacity',0);DR2.setAttribute('opacity',0);
 DARKG.firstChild.setAttribute('fill','#0d1f2b');
 [...PAPG.children].forEach(c=>{if(c.tagName=='g')c.setAttribute('opacity',0);if(c.tagName=='line')c.setAttribute('stroke','rgba(0,0,0,0)')});
 PAPG.firstChild.setAttribute('fill','#e9dcc0');
 const cont=(p,col)=>{const g=el(p,'g',{});const r=rng(129);for(let i=0;i<7;i++){const cx=r()*1080,cy=200+r()*1100;for(let j=1;j<5;j++)el(g,'ellipse',{cx,cy,rx:j*70+r()*20,ry:j*44+r()*16,fill:'none',stroke:col,'stroke-width':2})}return g};
 cont(DARKG,'rgba(127,166,196,.05)');cont(PAPG,'rgba(120,90,40,.07)');
 // nền biểu tượng Sài Gòn: cổng chợ Bến Thành có tháp đồng hồ, Nhà thờ Đức Bà, Bưu điện thành phố (vẽ nét phẳng, mờ)
 const sky=(p,col)=>{const g=el(p,'g',{});const L=(d,w=5)=>el(g,'path',{d,fill:'none',stroke:col,'stroke-width':w,'stroke-linejoin':'round','stroke-linecap':'round'});
  {const x=540,y=1560;L(`M${x-260} ${y} L${x-260} ${y-150} L${x+260} ${y-150} L${x+260} ${y}`,6);L(`M${x-70} ${y} L${x-70} ${y-90} Q${x} ${y-140} ${x+70} ${y-90} L${x+70} ${y}`,5);
   for(const dx of[-190,-120,120,190])L(`M${x+dx-24} ${y} L${x+dx-24} ${y-70} Q${x+dx} ${y-100} ${x+dx+24} ${y-70} L${x+dx+24} ${y}`,4);
   L(`M${x-290} ${y-150} L${x+290} ${y-150}`,7);L(`M${x-80} ${y-150} L${x-80} ${y-330} L${x+80} ${y-330} L${x+80} ${y-150}`,6);el(g,'circle',{cx:x,cy:y-250,r:48,fill:'none',stroke:col,'stroke-width':6});L(`M${x} ${y-250} L${x} ${y-285} M${x} ${y-250} L${x+24} ${y-238}`,5);
   L(`M${x-96} ${y-330} L${x} ${y-400} L${x+96} ${y-330}`,6);L(`M${x} ${y-400} L${x} ${y-430}`,5)}
  {const x=160,y=1600;for(const dx of[-60,60]){L(`M${x+dx-30} ${y} L${x+dx-30} ${y-300} L${x+dx} ${y-420} L${x+dx+30} ${y-300} L${x+dx+30} ${y}`,5);L(`M${x+dx} ${y-420} L${x+dx} ${y-460} M${x+dx-10} ${y-448} L${x+dx+10} ${y-448}`,4);for(const yy of[y-120,y-220])L(`M${x+dx-12} ${yy} L${x+dx-12} ${yy-40} Q${x+dx} ${yy-56} ${x+dx+12} ${yy-40} L${x+dx+12} ${yy}`,3)}
   L(`M${x-30} ${y} L${x-30} ${y-200} L${x+30} ${y-200} L${x+30} ${y}`,5);el(g,'circle',{cx:x,cy:y-150,r:20,fill:'none',stroke:col,'stroke-width':4});L(`M${x-30} ${y-200} L${x} ${y-240} L${x+30} ${y-200}`,5)}
  {const x0=760,y=1580;L(`M${x0} ${y} L${x0} ${y-160} L${x0+300} ${y-160} L${x0+300} ${y}`,6);L(`M${x0+60} ${y-160} Q${x0+150} ${y-260} ${x0+240} ${y-160}`,6);for(let i=0;i<5;i++){const xx=x0+30+i*60;L(`M${xx} ${y} L${xx} ${y-80} Q${xx+15} ${y-104} ${xx+30} ${y-80} L${xx+30} ${y}`,4)}el(g,'circle',{cx:x0+150,cy:y-200,r:22,fill:'none',stroke:col,'stroke-width':4})}
  return g};
 const skA=sky(DARKG,'rgba(224,166,60,.16)'),skB=sky(PAPG,'rgba(110,80,40,.16)');
 const wv=(p,col)=>[0,1,2,3].map(i=>el(p,'path',{fill:'none',stroke:col,'stroke-width':4+i,opacity:.55-i*.1}));
 const wA=wv(DARKG,'rgba(95,179,230,.45)'),wB=wv(PAPG,'rgba(60,110,150,.35)');
 window.THEME_UPD=t=>{const dx=Math.sin(t*.12)*18;skA.setAttribute('transform',`translate(${dx.toFixed(1)},0)`);skB.setAttribute('transform',`translate(${dx.toFixed(1)},0)`);[wA,wB].forEach(L=>L.forEach((e,i)=>{const y0=1660+i*58;let d='';for(let x=-20;x<=1100;x+=30){const y=y0+Math.sin(x*.012+t*(1.2+i*.3)+i)*12;d+=(x<0?'M':'L')+x+' '+y.toFixed(1)}e.setAttribute('d',d)}))};
}
// ===== CẢNH
const SG=[106.70,10.78];
// khối phố vẽ phẳng: 'cl' Chợ Lớn (mái cong phố người Hoa), 'bn' Bến Nghé (nhà ven sông, thuyền)
const BLOCK=(g,kind)=>{const k=el(g,'g',{});const W=kind=='cl'?'#b8834e':'#8aa0a8';el(k,'rect',{x:-190,y:-20,width:380,height:150,rx:10,fill:'rgba(0,0,0,.18)',stroke:'#fff','stroke-width':5});
 if(kind=='cl'){for(let i=0;i<4;i++){const x=-160+i*85;el(k,'rect',{x,y:-90,width:70,height:200,fill:W,stroke:'#fff','stroke-width':5});el(k,'path',{d:`M${x-10} -90 Q${x+35} -128 ${x+80} -90 L${x+70} -82 Q${x+35} -110 ${x} -82Z`,fill:'#a8302a',stroke:'#fff','stroke-width':4});el(k,'rect',{x:x+20,y:20,width:30,height:60,fill:'#3a2414',stroke:'#fff','stroke-width':3});el(k,'circle',{cx:x+35,cy:-40,r:11,fill:'#e0a63c',stroke:'#fff','stroke-width':3})}}
 else{for(let i=0;i<3;i++){const x=-150+i*110;el(k,'rect',{x,y:-60,width:80,height:110,fill:W,stroke:'#fff','stroke-width':5});el(k,'path',{d:`M${x-12} -60 L${x+40} -110 L${x+92} -60Z`,fill:'#6d5a45',stroke:'#fff','stroke-width':4})}
  for(let i=0;i<3;i++)el(k,'path',{d:`M-190 ${80+i*18} q30 -10 60 0 t60 0 t60 0 t60 0 t60 0 t60 0 t40 0`,fill:'none',stroke:RIV,'stroke-width':4});el(k,'path',{d:'M60 66 L150 66 L130 90 L80 90Z',fill:'#5a3a1e',stroke:'#fff','stroke-width':4})}
 return k};
const BOX=(g,txt)=>{const k=el(g,'g',{});el(k,'rect',{x:-130,y:-70,width:260,height:140,rx:10,fill:'#c89b5a',stroke:'#fff','stroke-width':7});el(k,'path',{d:'M-130 -20 L130 -20',stroke:'#7a5a2e','stroke-width':6});const t=MLB(k,txt,42,'#fff');t.setAttribute('y',36);return k};
const SIGN=(g,txt,col='#1d5a46')=>{const k=el(g,'g',{});el(k,'rect',{x:-8,y:0,width:16,height:240,fill:'#9aa3ab',stroke:'#fff','stroke-width':4});el(k,'rect',{x:-230,y:-80,width:460,height:96,rx:12,fill:col,stroke:'#fff','stroke-width':7});const t=MLB(k,txt,44,'#fff',col);t.setAttribute('y',-16);return{k,t}};
// 1 hook: Sài Gòn xưa là Chợ Lớn, không phải trung tâm bây giờ
S2(1,1,'d',null,g=>{const m=vnmap(560,820,11);const hs=hsts(m);const rg=RINGS(m.top,CGOLD);const A=strip('SÀI GÒN XƯA',true,64,12);const B=strip('TRUNG TÂM BÂY GIỜ',false,38,13),C=strip('CHỢ LỚN',true,52,14);const x1=XX(g),k1=CK(g);const q=T(g,0,0,'?',150,CGOLD,12,'middle',OLN);
 bm(AT(1,'Chợ',5.6));
 return{upd:t=>{const e=inn(t,R(1)-.2,.5);m.at(330,740,-1,1,e);m.view(108.7,15.9,44+5*inn(t,R(1),E(1)-R(1)));hs(e);m.hi('TP Hồ Chí Minh',inn(t,R(1)+.3,.5));const[x,y]=m.P(...SG);RU(rg,t,90,x,y,inn(t,R(1)+.3,.5));
  sh(A,t,790,420,-3,popv(t,R(1)+.3,.55));PUT(q,820,560,popv(t,R(1)+.8,.5)*(1-inn(t,AT(1,'trung',2.8),.3)),1,Math.sin(t*3)*6);sh(B,t,800,620,2,PV(t,1,'trung',2.8));PUT(x1,800,620,popv(t,AT(1,'mà',5.0),.4),.7,0);sh(C,t,800,820,-2,PV(t,1,'Chợ',5.6));PUT(k1,960,780,popv(t,AT(1,'Chợ',5.6)+.3,.4),.7,0)}}});
// 2 ngày nay nhắc Sài Gòn là nghĩ tới chợ Bến Thành; ngày xưa khu ấy tên khác
S2(2,2,'p',null,g=>{const gt=el(g,'g',{});{const x=0,y=0;el(gt,'rect',{x:-260,y:-150,width:520,height:150,fill:'#d9c49a',stroke:OLN,'stroke-width':7});el(gt,'path',{d:'M-70 0 L-70 -90 Q0 -140 70 -90 L70 0Z',fill:'#5a4630',stroke:OLN,'stroke-width':6});el(gt,'rect',{x:-80,y:-330,width:160,height:180,fill:'#e6d4ad',stroke:OLN,'stroke-width':7});el(gt,'circle',{cx:0,cy:-250,r:48,fill:'#fff',stroke:OLN,'stroke-width':6});el(gt,'path',{d:'M0 -250 L0 -285 M0 -250 L24 -238',stroke:OLN,'stroke-width':6,'stroke-linecap':'round'});el(gt,'path',{d:'M-96 -330 L0 -400 L96 -330Z',fill:'#a8302a',stroke:OLN,'stroke-width':6})}
 const A=strip('NGÀY NAY: KHU CHỢ BẾN THÀNH',false,38,21),st=stamp('NGÀY XƯA: TÊN KHÁC',52);const hand=el(g,'path',{d:'M0 0 L-40 -20 L-40 20Z',fill:CRED});
 return{upd:t=>{PUT(gt,540,880,popv(t,R(2)+.1,.55),1,Math.sin(t*1.4)*1);sh(A,t,540,1000,-1,PV(t,2,'Bến',3.4));const su=popv(t,AT(2,'Nhưng',5.4),.45);st.at(540,380,-6,su,su>0?1:0)}}});
// 3 Bến Nghé và Chợ Lớn (sơ đồ minh họa)
S2(3,3,'d',null,g=>{const b1=BLOCK(g,'bn'),b2=BLOCK(g,'cl');const L1=strip('BẾN NGHÉ',false,44,31),L2=strip('SÀI GÒN',true,48,32),L3=strip('(CHỢ LỚN NGÀY NAY)',false,28,33),N=strip('SƠ ĐỒ MINH HỌA',false,20,34);const ar=el(g,'path',{fill:'none',stroke:CGOLD,'stroke-width':8,'stroke-dasharray':'14 10'});
 return{upd:t=>{PUT(b1,760,560,popv(t,R(3)+.1,.55),.9,Math.sin(t*1.5)*1);sh(L1,t,760,410,2,PV(t,3,'Bến',1.6));PUT(b2,320,900,popv(t,AT(3,'Sài',2.6),.55),.9,Math.sin(t*1.5+1)*1);sh(L2,t,320,740,-2,PV(t,3,'Sài',2.6));sh(L3,t,320,1090,1,PV(t,3,'Chợ',6.2));sh(N,t,880,1220,0,inn(t,R(3)+.5,.4))}}});
// 4 từ điển xưa ghi rõ
S2(4,4,'p',null,g=>{const bk=el(g,'g',{});el(bk,'rect',{x:-300,y:-220,width:600,height:440,rx:14,fill:'#efe3c2',stroke:OLN,'stroke-width':8});el(bk,'path',{d:'M0 -220 L0 220',stroke:OLN,'stroke-width':6});for(let s of[-1,1])for(let i=0;i<7;i++)if(!(s==1&&i==2))el(bk,'rect',{x:s<0?-270:30,y:-170+i*52,width:230-(i%3)*40,height:12,rx:6,fill:'rgba(60,40,20,.3)'});
 const hl=el(bk,'rect',{x:24,y:-70,width:0,height:56,rx:8,fill:CGOLD});const ht=MLB(bk,'SÀI GÒN = ĐẤT CHỢ LỚN',26,OLN,CGOLD);ht.setAttribute('x',150);ht.setAttribute('y',-32);
 const A=strip('TỪ ĐIỂN XƯA',true,46,41),B=strip('VỀ SAU MỚI HIỂU LÀ BẾN NGHÉ',false,32,42);const ck=CK(g);
 return{upd:t=>{PUT(bk,540,700,popv(t,R(4)+.1,.55),1,-2+Math.sin(t*1.4));sh(A,t,540,400,-2,PV(t,4,'Từ',.2));const u=inn(t,AT(4,'Sài',1.4),.6);hl.setAttribute('width',250*u);ht.setAttribute('opacity',u);PUT(ck,820,560,popv(t,AT(4,'Chợ',2.4),.4),.7,0);sh(B,t,540,1040,1,PV(t,4,'Chỉ',4.2))}}});
// 5 người Pháp quy hoạch Bến Nghé thành thành phố
S2(5,5,'d',null,g=>{const b1=BLOCK(g,'bn');const sp=el(g,'g',{});drawShip(sp);const grid=el(g,'g',{});const gl=[];for(let i=0;i<6;i++){gl.push(el(grid,'path',{d:`M${-220+i*88} -180 L${-220+i*88} 180`,stroke:CSTEEL,'stroke-width':5,'stroke-dasharray':'1 1',pathLength:1,'stroke-dashoffset':1}));gl.push(el(grid,'path',{d:`M-220 ${-180+i*72} L220 ${-180+i*72}`,stroke:CSTEEL,'stroke-width':5,'stroke-dasharray':'1 1',pathLength:1,'stroke-dashoffset':1}))}
 const q=T(g,0,0,'?',160,CGOLD,12,'middle',OLN);const A=strip('ĐẦU NHỮNG NĂM 1860',true,40,51),B=strip('QUY HOẠCH THÀNH PHỐ',false,36,52);
 return{upd:t=>{PUT(q,540,420,popv(t,R(5)+.1,.5)*(1-inn(t,AT(5,'Đầu',2.0),.3)),1,Math.sin(t*3)*6);const su=inn(t,AT(5,'Pháp',3.6),1.6);PUT(sp,lerp(-100,300,su),700+Math.sin(t*2)*6,su>0?1:0,2.2,0);PUT(b1,700,800,popv(t,AT(5,'Bến',5.2),.5),.9,0);
  const gu=inn(t,AT(5,'thành',6.8),1.2);gl.forEach((e,i)=>{e.setAttribute('stroke-dashoffset',1-cl(gu*1.4-i*.04))});grid.setAttribute('transform','translate(700,760)');sh(A,t,540,420,-2,PV(t,5,'Đầu',2.0));sh(B,t,700,1080,1,PV(t,5,'thành',6.8))}}});
// 6-7 cái tên dọn nhà: SÀI GÒN chuyển sang Bến Nghé; chỗ cũ thành CHỢ LỚN; "Chợ Lớn mới là Sài Gòn gốc"
S2(6,7,'p',null,g=>{const b1=BLOCK(g,'bn'),b2=BLOCK(g,'cl');const bx=BOX(g,'SÀI GÒN');const L1=strip('BẾN NGHÉ',false,38,61),L2=strip('CHỢ LỚN',true,44,62),N1=strip('SÀI GÒN',true,48,63);const pa=el(g,'path',{fill:'none',stroke:CRED,'stroke-width':7,'stroke-dasharray':'14 12'});const crown=CROWN(g);const G=strip('SÀI GÒN GỐC',true,50,64);
 const tg=AT(7,'gốc',5.4);bm(tg,true);
 return{upd:t=>{const p1=[300,880],p0=[300,860],p2=[770,520];PUT(b2,300,900,inn(t,R(6)-.2,.4),.85,0);PUT(b1,770,560,inn(t,R(6)-.2,.4),.85,0);
  const mv=inn(t,AT(6,'đặt',.6),1.6);const cx=lerp(lerp(300,540,mv),lerp(540,770,mv),mv),cy=lerp(lerp(720,300,mv),lerp(300,380,mv),mv);PUT(bx,cx,cy+Math.sin(t*4)*4,inn(t,R(6)-.1,.3),.85,(1-mv)*-8+mv*6);pa.setAttribute('d',`M300 720 Q540 300 ${cx} ${cy}`);pa.setAttribute('opacity',mv>0&&mv<1?1:0);
  sh(L1,t,770,760,1,inn(t,R(6),.4)*(1-inn(t,AT(6,'Sài',2.0)+.2,.3)));sh(N1,t,770,760,-1,PV(t,6,'Sài',2.0,.3));sh(L2,t,300,1100,-2,PV(t,6,'Chợ',4.8));
  PUT(crown,300,720,popv(t,tg-.4,.5),.9,Math.sin(t*3)*4);sh(G,t,300,1200,2,popv(t,tg,.5))}}});
// 8 tên Gia Định từ năm 1698 (bản đồ cả nước, có Hoàng Sa, Trường Sa)
S2(8,8,'d',t=>'1698',g=>{const m=vnmap(560,820,81);const hs=hsts(m);const rg=RINGS(m.top,CGOLD);const A=strip('PHỦ GIA ĐỊNH',true,56,81),B=strip('NGUYỄN HỮU CẢNH',false,40,82),C=strip('LẬP CHO CHÚA NGUYỄN',false,32,83);const sc=SCRL(g,300,240);
 return{upd:t=>{const e=inn(t,R(8)-.2,.5);m.at(330,740,-1,1,e);m.view(108.7,15.9,46);hs(e);m.hi('TP Hồ Chí Minh',inn(t,AT(8,'Gia',.8),.5));const[x,y]=m.P(...SG);RU(rg,t,80,x,y,e);
  PUT(sc,820,520,popv(t,AT(8,'Năm',2.8),.5),.9,Math.sin(t*1.5)*2);sh(A,t,820,720,-2,PV(t,8,'phủ',5.6));sh(B,t,820,820,2,PV(t,8,'Nguyễn',4.6));sh(C,t,820,900,-1,PV(t,8,'chúa',6.6))}}});
// 9 Sài Gòn – Gia Định
S2(9,9,'p',t=>'1975',g=>{const A=strip('SÀI GÒN',false,90,91),B=strip('GIA ĐỊNH',false,90,92),C=strip('SÀI GÒN – GIA ĐỊNH',true,72,93);const pl=T(g,0,0,'+',140,CGOLD,10,'middle',OLN);
 return{upd:t=>{const mg=inn(t,AT(9,'ghép',3.8),.6);sh(A,t,lerp(300,540,mg),lerp(560,700,mg),-3,popv(t,R(9)+.1,.5)*(1-mg));sh(B,t,lerp(780,540,mg),lerp(820,700,mg),3,popv(t,R(9)+.4,.5)*(1-mg));PUT(pl,540,700,popv(t,R(9)+.6,.4)*(1-mg),1,0);sh(C,t,540,700,-1,popv(t,AT(9,'ghép',3.8)+.3,.55))}}});
// 10 năm 1976 đổi tên Thành phố Hồ Chí Minh
S2(10,10,'d',t=>'1976',g=>{const dc=el(g,'g',{});el(dc,'rect',{x:-280,y:-340,width:560,height:680,rx:10,fill:'#fbf6e8',stroke:OLN,'stroke-width':7});const h1=MLB(dc,'QUỐC HỘI',44,CRED,'#fbf6e8');h1.setAttribute('y',-250);const h2=MLB(dc,'KỲ HỌP ĐẦU TIÊN',30,OLN,'#fbf6e8');h2.setAttribute('y',-200);for(let i=0;i<7;i++)el(dc,'rect',{x:-220,y:-140+i*48,width:440-(i%3)*60,height:13,rx:6,fill:'rgba(40,30,20,.25)'});
 const st=stamp('THÀNH PHỐ HỒ CHÍ MINH',50);const mh=strip('HÌNH MINH HỌA',false,20,101);const ts=AT(10,'Thành',6.4);bm(ts);
 return{upd:t=>{PUT(dc,540,660,popv(t,R(10)+.1,.55),1,-2+Math.sin(t*1.4));sh(mh,t,800,1060,0,inn(t,R(10)+.4,.4));const su=popv(t,ts,.45);st.at(540,760,-6,su,su>0?1:0)}}});
// 11 ý tưởng từ 1946, đến khi thống nhất mới chính thức
S2(11,11,'p',null,g=>{const X0=150,X1=930,Y=720;const bar=el(g,'rect',{x:X0,y:Y-30,width:0,height:60,rx:14,fill:CSTEEL,stroke:OLN,'stroke-width':5});const y1=MLB(g,'1946',54,OLN,'#efe6cf'),y2=MLB(g,'1976',54,OLN,'#efe6cf');const A=strip('Ý TƯỞNG',false,40,111),B=strip('CHÍNH THỨC',true,44,112);const d1=el(g,'circle',{r:24,fill:CSTEEL,stroke:'#fff','stroke-width':5}),d2=el(g,'circle',{r:28,fill:CGOLD,stroke:'#fff','stroke-width':5});const ck=CK(g);
 return{upd:t=>{const u=inn(t,AT(11,'Nhưng',3.2),1.6);bar.setAttribute('width',(X1-X0)*u);PUT(d1,X0,Y,popv(t,R(11)+.2,.4),1,0);PUT(y1,X0+20,Y+90,popv(t,R(11)+.3,.4),1,0);sh(A,t,X0+90,Y-110,-2,PV(t,11,'ý',.6));PUT(d2,X1,Y,popv(t,AT(11,'chính',5.6),.4),1,0);PUT(y2,X1-20,Y+90,popv(t,AT(11,'chính',5.6),.4),1,0);sh(B,t,X1-110,Y-110,2,PV(t,11,'chính',5.6));PUT(ck,X1-20,Y-240,popv(t,AT(11,'chính',5.6)+.3,.4),.7,0)}}});
// 12 năm 2025 nhập Bình Dương, Bà Rịa – Vũng Tàu, vẫn giữ tên (ranh giới cũ nét đứt)
S2(12,12,'d',t=>'2025',g=>{const m=vnmap(960,900,121);const old=['Ho Chi Minh','Bình Dương','Bà Rịa–Vũng Tàu'].map(n=>{const p=TINH63.find(q=>q.n==n);return el(m.riv,'path',{d:p.p.map(rpath).join(''),fill:'none',stroke:'#fff8e6','stroke-width':3,'stroke-dasharray':'10 8','vector-effect':'non-scaling-stroke',opacity:0})});
 const L=[['BÌNH DƯƠNG',106.63,11.2],['TP HỒ CHÍ MINH CŨ',106.68,10.78],['BÀ RỊA – VŨNG TÀU',107.25,10.55]].map(([n,lo,la])=>({e:MLB(m.top,n,28,'#fff'),lo,la}));const A=strip('VẪN GIỮ TÊN',true,48,121),B=strip('THÀNH PHỐ HỒ CHÍ MINH',false,40,122);
 const H=strip('QĐ. HOÀNG SA (VIỆT NAM) ↗',false,22,123),S=strip('QĐ. TRƯỜNG SA (VIỆT NAM) ↘',false,22,124),NOW=strip('RANH GIỚI HIỆN NAY, NÉT ĐỨT LÀ TỈNH CŨ',false,20,125);
 return{upd:t=>{const e=inn(t,R(12)-.2,.5);m.at(540,770,0,1,e);m.view(106.85,10.85,lerp(230,270,inn(t,R(12),E(12)-R(12))));m.hi('TP Hồ Chí Minh',e*inn(t,AT(12,'nhập',1.4),.6));old.forEach((o,i)=>o.setAttribute('opacity',inn(t,AT(12,'Bình',2.4)+i*.3,.4)));
  L.forEach((o,i)=>{const[x,y]=m.P(o.lo,o.la);o.e.setAttribute('x',x);o.e.setAttribute('y',y);o.e.setAttribute('opacity',inn(t,AT(12,'Bình',2.4)+i*.3,.4))});sh(A,t,540,380,-2,PV(t,12,'giữ',5.4));sh(B,t,540,460,1,PV(t,12,'giữ',5.4,.2));
  sh(H,t,850,1180,0,e);sh(S,t,850,1235,0,e);sh(NOW,t,300,1235,0,e)}}});
// 13 tên Sài Gòn còn ở sông, cảng, phường
S2(13,13,'p',null,g=>{const rv=[0,1,2].map(i=>el(g,'path',{fill:'none',stroke:RIV,'stroke-width':10-i*2,'stroke-linecap':'round'}));const an=el(g,'g',{});el(an,'path',{d:'M0 -70 L0 60 M-50 20 Q0 90 50 20 M-30 -40 L30 -40',fill:'none',stroke:OLN,'stroke-width':12,'stroke-linecap':'round'});el(an,'circle',{cy:-84,r:16,fill:'none',stroke:OLN,'stroke-width':10});
 const A=strip('SÔNG SÀI GÒN',false,40,131),B=strip('CẢNG SÀI GÒN',false,40,132);const sg=SIGN(g,'PHƯỜNG SÀI GÒN');
 return{upd:t=>{const u=inn(t,AT(13,'sông',3.4),.6);rv.forEach((e,i)=>{let d='';for(let x=80;x<=500;x+=14)d+=(x==80?'M':'L')+x+' '+(520+i*26+Math.sin(x*.03+t*3+i)*12).toFixed(1);e.setAttribute('d',d);e.setAttribute('opacity',u)});sh(A,t,290,440,-2,PV(t,13,'sông',3.4));
  PUT(an,800,520,popv(t,AT(13,'cảng',4.6),.5),1,Math.sin(t*2)*4);sh(B,t,800,660,2,PV(t,13,'cảng',4.6));PUT(sg.k,540,880,popv(t,AT(13,'phường',7.4),.55),1,Math.sin(t*1.6)*1.5)}}});
// 14 phường Sài Gòn lập từ toàn bộ phường Bến Nghé: cái tên dọn về nhà mới
S2(14,14,'d',null,g=>{const sg=SIGN(g,'PHƯỜNG BẾN NGHÉ','#6a5a48');const bx=BOX(g,'SÀI GÒN');const A=strip('TOÀN BỘ PHƯỜNG BẾN NGHÉ',false,34,141),B=strip('ĐÃ DỌN VỀ NHÀ MỚI',true,46,142);const ck=CK(g);const tf=AT(14,'Bến',3.2);bm(tf+.6);
 return{upd:t=>{PUT(sg.k,540,700,popv(t,R(14)+.1,.5),1,0);const fl=inn(t,tf+.4,.4);sg.k.setAttribute('transform',`translate(540,700) scale(${Math.max(.02,Math.abs(1-2*fl))},1)`);if(fl>.5){sg.t.textContent='PHƯỜNG SÀI GÒN';sg.k.children[1].setAttribute('fill','#1d5a46')}else{sg.t.textContent='PHƯỜNG BẾN NGHÉ';sg.k.children[1].setAttribute('fill','#6a5a48')}
  sh(A,t,540,420,-2,PV(t,14,'toàn',2.2));const mv=inn(t,AT(14,'dọn',6.8)-.8,1.0);PUT(bx,lerp(-200,540,mv),lerp(1000,560,mv),mv>0?1:0,.8,(1-mv)*20);sh(B,t,540,1080,1,PV(t,14,'dọn',6.8));PUT(ck,800,560,popv(t,AT(14,'dọn',6.8)+.3,.4),.7,0)}}});
// 15 câu hỏi
S2(15,15,'d',null,g=>{const bx=BOX(g,'TÊN QUÊ BẠN?');const hs=[0,1,2].map(i=>{const k=el(g,'g',{});el(k,'rect',{x:-60,y:-40,width:120,height:90,fill:PAL[i*2],stroke:'#fff','stroke-width':5});el(k,'path',{d:'M-75 -40 L0 -100 L75 -40Z',fill:CRED,stroke:'#fff','stroke-width':5});return k});const A=strip('Ở QUÊ BẠN, CÓ TÊN NÀO DỌN NHÀ?',true,40,151);bm(R(15)+.2);
 return{upd:t=>{hs.forEach((k,i)=>PUT(k,250+i*290,860,popv(t,R(15)+.1+i*.15,.5),1,0));const ph=((t-R(15))*.5)%1;const xi=250+Math.floor(((t-R(15))*.5)%3)*290;PUT(bx,lerp(250,830,inn(t,R(15)+.4,3.0)),620+Math.abs(Math.sin(t*3))*-40,popv(t,R(15)+.3,.5),.7,Math.sin(t*3)*6);sh(A,t,540,1120,-1,PV(t,15,'quê',.6))}}});
