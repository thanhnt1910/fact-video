// ===== TÊN TỈNH THÀNH #04: Đà Nẵng (tn4). Bản đồ hành chính phẳng 34 tỉnh (geoBoundaries, phạm vi công cộng), không vẽ nước láng giềng.
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
// ===== Dấu ấn riêng (Đà Nẵng): nền tối xanh rêu biển, giấy cát nhạt; nét Ngũ Hành Sơn, bán đảo Sơn Trà, cầu quay sông Hàn mờ ở đáy; sóng biển lăn (y>1640)
{DR1.setAttribute('opacity',0);DR2.setAttribute('opacity',0);
 DARKG.firstChild.setAttribute('fill','#0f2626');
 [...PAPG.children].forEach(c=>{if(c.tagName=='g')c.setAttribute('opacity',0);if(c.tagName=='line')c.setAttribute('stroke','rgba(0,0,0,0)')});
 PAPG.firstChild.setAttribute('fill','#efe4c8');
 const sand=(p,col)=>{const g=el(p,'g',{});const r=rng(404);for(let i=0;i<90;i++)el(g,'circle',{cx:r()*1080,cy:200+r()*1300,r:1.5+r()*2.5,fill:col});return g};
 sand(DARKG,'rgba(150,220,210,.06)');sand(PAPG,'rgba(140,110,60,.10)');
 const sky=(p,col)=>{const g=el(p,'g',{});const L=(d,w=5)=>el(g,'path',{d,fill:'none',stroke:col,'stroke-width':w,'stroke-linejoin':'round','stroke-linecap':'round'});
  L('M-20 1610 Q120 1440 260 1520 Q330 1470 400 1610',6);                       // bán đảo Sơn Trà
  L('M640 1610 L690 1500 L730 1560 L780 1450 L830 1540 L860 1490 L910 1610',6);    // Ngũ Hành Sơn
  L('M300 1640 L620 1640',6);for(let i=0;i<8;i++)L(`M${310+i*40} 1640 L${310+i*40} 1600`,3);L('M420 1600 L500 1600 L460 1560Z',4); // cầu quay
  return g};
 const skA=sky(DARKG,'rgba(224,166,60,.16)'),skB=sky(PAPG,'rgba(60,90,90,.18)');
 const wv=(p,col)=>[0,1,2].map(i=>el(p,'path',{fill:'none',stroke:col,'stroke-width':4+i,opacity:.6-i*.12}));
 const wA=wv(DARKG,'rgba(120,210,200,.40)'),wB=wv(PAPG,'rgba(40,110,120,.30)');
 window.THEME_UPD=t=>{const dx=Math.sin(t*.1)*14;skA.setAttribute('transform',`translate(${dx.toFixed(1)},0)`);skB.setAttribute('transform',`translate(${dx.toFixed(1)},0)`);[wA,wB].forEach(L=>L.forEach((e,i)=>{const y0=1680+i*64;let d='';for(let x=-20;x<=1100;x+=26){const y=y0+Math.sin(x*.016-t*(1.6+i*.4)+i)*13;d+=(x<0?'M':'L')+x+' '+y.toFixed(1)}e.setAttribute('d',d)}))};
}
// ===== CẢNH
const DNG=[108.21,16.06];
const SEAH=()=>[strip('QĐ. HOÀNG SA (VIỆT NAM) ↗',false,22,901),strip('QĐ. TRƯỜNG SA (VIỆT NAM) ↘',false,22,902),strip('RANH GIỚI HIỆN NAY',false,20,903)];
const seaH=(L,t,e,lab)=>{sh(L[0],t,840,1180,0,e);sh(L[1],t,840,1235,0,e);sh(L[2],t,250,1235,0,e*(lab===false?0:1))};
const TOWER=(g,col='#b5703a')=>{const k=el(g,'g',{});el(k,'path',{d:'M-90 120 L-90 -40 L-60 -40 L-60 -120 L-30 -120 L-30 -190 L0 -230 L30 -190 L30 -120 L60 -120 L60 -40 L90 -40 L90 120Z',fill:col,stroke:'#fff','stroke-width':7,'stroke-linejoin':'round'});el(k,'path',{d:'M-26 120 L-26 40 Q0 10 26 40 L26 120Z',fill:'#3a2414',stroke:'#fff','stroke-width':5});return k};
const DOC=(g,txt)=>{const k=SCRL(g,380,300);const s=MLB(k,txt,40,CRED,'#e8dcba');s.setAttribute('y',-100);return k};
const flipSign=(s,tf,a,b,ca='#6a5a48',cb='#1d5a46')=>(t,x,y,sc,op)=>{const fl=inn(t,tf-.3,.4);s.k.setAttribute('transform',`translate(${x},${y}) scale(${sc*Math.max(.02,Math.abs(1-2*fl))},${sc})`);s.k.setAttribute('opacity',op);if(fl>.5){s.t.textContent=b;s.k.children[1].setAttribute('fill',cb)}else{s.t.textContent=a;s.k.children[1].setAttribute('fill',ca)}};
// 1 hook: Đà Nẵng từng mang một cái tên Tây hơn 60 năm
S2(1,1,'d',null,g=>{const m=vnmap(560,820,41);const hs=hsts(m);const rg=RINGS(m.top,CGOLD);const A=strip('ĐÀ NẴNG',true,64,11);const B=strip('TỪNG MANG TÊN TÂY?',false,42,12),C=strip('HƠN 60 NĂM',true,48,13);const q=T(g,0,0,'?',150,CGOLD,12,'middle',OLN);const tt=AT(1,'Tây',2.6);bm(tt);
 return{upd:t=>{const e=inn(t,R(1)-.2,.5);m.at(330,740,-1,1,e);m.view(108.7,15.9,44+6*inn(t,R(1),E(1)-R(1)));hs(e);m.hi('Đà Nẵng',inn(t,AT(1,'Đà',.8),.5),CRED);const[x,y]=m.P(...DNG);RU(rg,t,90,x,y,inn(t,AT(1,'Đà',.8),.4));
  sh(A,t,800,420,-3,PV(t,1,'Đà',.8));PUT(q,820,640,popv(t,tt-.2,.5),1,Math.sin(t*3)*6);sh(B,t,800,820,2,popv(t,tt,.5));sh(C,t,800,920,-2,PV(t,1,'sáu',3.4))}}});
// 2 cái tên ấy là Tourane; giấy tờ chính thức thời Pháp thuộc
S2(2,2,'p',null,g=>{const s=SIGN(g,'ĐÀ NẴNG','#1d5a46');const tf=AT(2,'Tu',1.0);const F=flipSign(s,tf,'ĐÀ NẴNG','TOURANE','#1d5a46','#6a5a48');const dc=DOC(g,'TOURANE');const A=strip('THỜI PHÁP THUỘC',false,40,21);const st=stamp('TÊN CHÍNH THỨC',50);bm(tf);
 return{upd:t=>{F(t,540,520,1.2,inn(t,R(2)+.05,.3));sh(A,t,540,330,-2,PV(t,2,'Suốt',1.8));PUT(dc,540,900,popv(t,AT(2,'giấy',3.4),.5),.8,-3+Math.sin(t*1.4));const su=popv(t,AT(2,'giấy',3.4)+.5,.45);st.at(540,1170,-5,su*.9,su>0?1:0)}}});
// 3 cuộc xâm lược của Pháp bắt đầu bằng trận tấn công vào cửa biển Đà Nẵng
S2(3,3,'d',null,g=>{const m=vnmap(960,880,31);const rg=RINGS(m.top,CRED);const dot3=el(m.top,'circle',{r:14,fill:CRED,stroke:'#fff','stroke-width':5});const sp=el(m.top,'g',{});drawShip(sp);const sp2=el(m.top,'g',{});drawShip(sp2);const q=T(g,0,0,'?',160,CGOLD,12,'middle',OLN);const A=strip('VÌ SAO?',true,54,31),B=strip('XÂM LƯỢC BẮT ĐẦU TỪ ĐÂY',true,40,32),C=strip('CỬA BIỂN ĐÀ NẴNG',false,36,33);const SH=SEAH();const tb=AT(3,'tấn',4.4);bm(tb);
 return{upd:t=>{const out=inn(t,AT(3,'Cuộc',1.2),.3);PUT(q,540,640,popv(t,R(3)+.05,.5)*(1-out),1,Math.sin(t*3)*6);sh(A,t,540,420,-2,popv(t,R(3)+.05,.5)*(1-out));
  const e=inn(t,AT(3,'Cuộc',1.2)-.1,.5);m.at(540,760,0,e,e);m.view(108.5,16.0,lerp(210,250,inn(t,R(3),E(3)-R(3))));seaH(SH,t,e);const[x,y]=m.P(...DNG);dot3.setAttribute('cx',x);dot3.setAttribute('cy',y);dot3.setAttribute('opacity',e);const u=inn(t,AT(3,'Cuộc',1.2),tb-AT(3,'Cuộc',1.2)+.4);
  PUT(sp,lerp(x+460,x+70,u),y-20+Math.sin(t*2)*5,u>0?1:0,1.6,0);PUT(sp2,lerp(x+520,x+130,u),y+60+Math.sin(t*2+1)*5,u>0?1:0,1.3,0);RU(rg,t,90,x,y,inn(t,tb,.3));sh(B,t,540,400,-2,popv(t,AT(3,'bắt',3.4),.5));sh(C,t,540,1100,1,PV(t,3,'cửa',5.6))}}});
// 4 năm 1888 vua Đồng Khánh ra đạo dụ cắt Đà Nẵng làm đất nhượng cho Pháp
S2(4,4,'p',t=>'1888',g=>{const dc=SCRL(g,440,360);const A=strip('VUA ĐỒNG KHÁNH',false,42,41),B=strip('RA ĐẠO DỤ',false,38,42);const st=stamp('CẮT ĐẤT NHƯỢNG CHO PHÁP',44);const sc=el(g,'path',{d:'M-160 0 L160 0',stroke:CRED,'stroke-width':10,'stroke-dasharray':'22 14',fill:'none'});const tc=AT(4,'cắt',4.4);bm(tc);
 return{upd:t=>{sh(A,t,540,360,-2,PV(t,4,'vua',2.8));PUT(dc,540,700+Math.sin(t*1.8)*8,popv(t,R(4)+.1,.55),.92+.08*inn(t,AT(4,'đạo',3.8)-.2,.5),-2+Math.sin(t*1.4)*2);sh(B,t,540,450,1,PV(t,4,'đạo',3.8));sc.setAttribute('transform','translate(540,700)');sc.setAttribute('opacity',inn(t,tc,.3));const su=popv(t,tc+.2,.45);st.at(540,1000,-6,su,su>0?1:0)}}});
// 5 thành phố Tourane do Pháp trực tiếp cai quản, không thuộc triều đình Huế
S2(5,5,'d',null,g=>{const m=vnmap(960,880,51);const rg=RINGS(m.top,CGOLD);const lab=MLB(m.top,'TOURANE',38,'#fff',CRED);const dot5=el(m.top,'circle',{r:14,fill:CGOLD,stroke:'#fff','stroke-width':5});const cr=CROWN(g);const x1=XX(g);const A=strip('NGƯỜI PHÁP TRỰC TIẾP CAI QUẢN',true,36,51),B=strip('KHÔNG THUỘC TRIỀU ĐÌNH HUẾ',false,34,52);const SH=SEAH();const tk=AT(5,'không',4.2);bm(AT(5,'Tu',1.6),true);
 return{upd:t=>{const e=inn(t,R(5)-.2,.5);m.at(540,760,0,1,e);m.view(107.9,16.3,200);seaH(SH,t,e);const[x,y]=m.P(...DNG);dot5.setAttribute('cx',x);dot5.setAttribute('cy',y);dot5.setAttribute('opacity',inn(t,AT(5,'Tu',1.6),.4));RU(rg,t,80,x,y,inn(t,AT(5,'Tu',1.6),.4));const[hx,hy]=m.P(107.58,16.46);
  lab.setAttribute('x',x+90);lab.setAttribute('y',y+70);lab.setAttribute('opacity',inn(t,AT(5,'Tu',1.6),.4));sh(A,t,540,400,-2,PV(t,5,'trực',3.0));PUT(cr,540+hx,760+hy-60,popv(t,tk,.5),.6,0);PUT(x1,540+hx,760+hy-60,popv(t,tk+.3,.4),.7,0);sh(B,t,540,480,1,popv(t,tk,.5))}}});
// 6 người dân vẫn gọi là Hàn: giấy tờ một đằng, người dân một nẻo
S2(6,6,'p',null,g=>{const dc=DOC(g,'TOURANE');const pp=[0,1].map(i=>fig(g,{hat:[CGOLD,CRED][i]}));const bb=bubble(g,260,120,'HÀN!',70);const rv=[0,1].map(i=>el(g,'path',{fill:'none',stroke:RIV,'stroke-width':8-i*2,'stroke-linecap':'round'}));const A=strip('CỬA HÀN · SÔNG HÀN',false,36,61),B=strip('GIẤY TỜ MỘT ĐẰNG',false,36,62),C=strip('NGƯỜI DÂN MỘT NẺO',true,38,63);bm(AT(6,'Hàn',1.8),true);
 return{upd:t=>{pp.forEach((p,i)=>p.at(680+i*150,880,.9,0,popv(t,R(6)+.1+i*.15,.5)));bb.at(820,420,1,popv(t,AT(6,'Hàn',1.8),.5));const u=inn(t,AT(6,'sông',3.0),.5);rv.forEach((e,i)=>{let d='';for(let x=560;x<=1040;x+=14)d+=(x==560?'M':'L')+x+' '+(980+i*26+Math.sin(x*.03+t*3+i)*10).toFixed(1);e.setAttribute('d',d);e.setAttribute('opacity',u)});sh(A,t,800,1080,-1,PV(t,6,'sông',3.0));
  PUT(dc,280,600,popv(t,AT(6,'Giấy',4.0),.5),.75,-4+Math.sin(t*1.4));sh(B,t,280,820,2,PV(t,6,'đằng',4.8));sh(C,t,760,1180,-2,PV(t,6,'nẻo',6.2))}}});
// 7 chữ Đà Nẵng từ đâu ra? gốc tiếng Chăm
S2(7,7,'d',null,g=>{const q=T(g,0,0,'ĐÀ NẴNG = ?',110,CGOLD,12,'middle',OLN);const tw=TOWER(g);const A=strip('CÁC NHÀ NGHIÊN CỨU',false,36,71),B=strip('GỐC TIẾNG CHĂM',true,52,72);const tg=AT(7,'gốc',4.0);bm(tg);
 return{upd:t=>{PUT(q,540,560,popv(t,R(7)+.1,.5),1,Math.sin(t*3)*3);sh(A,t,540,380,-1,PV(t,7,'Các',1.6));PUT(tw,540,900,popv(t,tg-.2,.55),1,Math.sin(t*1.4));sh(B,t,540,1120,2,popv(t,tg,.5))}}});
// 8 vùng đất xưa của người Chăm; từ Chăm thường được hiểu là sông lớn
S2(8,8,'p',null,g=>{const tw=TOWER(g);const rv=[0,1,2,3].map(i=>el(g,'path',{fill:'none',stroke:RIV,'stroke-width':6,'stroke-linecap':'round'}));const A=strip('ĐẤT XƯA CỦA NGƯỜI CHĂM',false,38,81),B=strip('SÔNG LỚN',true,64,82),N=strip('THƯỜNG ĐƯỢC HIỂU LÀ',false,30,83);const ts=AT(8,'sông',5.4);bm(ts);
 return{upd:t=>{PUT(tw,250,640,popv(t,R(8)+.1,.5),.8,0);sh(A,t,540,360,-2,PV(t,8,'Chăm',1.4));const u=inn(t,AT(8,'Từ',2.0),1.2),w=inn(t,ts,.8);rv.forEach((e,i)=>{let d='';for(let x=420;x<=1040;x+=14){const yy=760+(i-1.5)*(18+40*w)+Math.sin(x*.025+t*2.5+i)*8;d+=(x==420?'M':'L')+x+' '+yy.toFixed(1)}e.setAttribute('d',d);e.setAttribute('opacity',u);e.setAttribute('stroke-width',6+6*w)});
  sh(N,t,730,960,1,popv(t,ts-.6,.5));sh(B,t,730,1050,-2,popv(t,ts,.5))}}});
// 9 cái tên chỉ dòng sông đổ ra biển, hợp với thành phố cảng
S2(9,9,'d',null,g=>{const rv=[0,1,2].map(i=>el(g,'path',{fill:'none',stroke:RIV,'stroke-width':10-i*2,'stroke-linecap':'round'}));const sea=el(g,'rect',{x:680,y:560,width:440,height:480,rx:60,fill:'rgba(60,140,170,.28)'});const sp=el(g,'g',{});drawShip(sp);const an=el(g,'g',{});el(an,'path',{d:'M0 -70 L0 60 M-50 20 Q0 90 50 20 M-30 -40 L30 -40',fill:'none',stroke:'#fff','stroke-width':12,'stroke-linecap':'round'});el(an,'circle',{cy:-84,r:16,fill:'none',stroke:'#fff','stroke-width':10});
 const A=strip('SÔNG ĐỔ RA BIỂN',false,40,91),B=strip('THÀNH PHỐ CẢNG',true,50,92);const ck=CK(g);bm(AT(9,'cảng',4.0),true);
 return{upd:t=>{const u=inn(t,R(9)+.1,.8);rv.forEach((e,i)=>{let d='';for(let x=60;x<=660*u+40;x+=14)d+=(x==60?'M':'L')+x+' '+(780+i*28+Math.sin(x*.03+t*3+i)*12).toFixed(1);e.setAttribute('d',d)});sea.setAttribute('opacity',inn(t,AT(9,'biển',2.0),.5));sh(A,t,380,560,-2,PV(t,9,'dòng',1.0));
  PUT(sp,lerp(1100,860,inn(t,AT(9,'cảng',4.0)-.8,1.2)),800+Math.sin(t*2)*6,1,2,0);PUT(an,860,1000,popv(t,AT(9,'cảng',4.0),.5),.9,Math.sin(t*2)*4);sh(B,t,540,1180,1,PV(t,9,'cảng',4.0));PUT(ck,940,420,popv(t,AT(9,'cảng',4.0)+.3,.4),.6,0)}}});
// 10 giữa thế kỷ 20 tên Đà Nẵng được dùng lại, giữ đến nay
S2(10,10,'p',null,g=>{const s=SIGN(g,'TOURANE','#6a5a48');const tf=AT(10,'Đà',2.2);const F=flipSign(s,tf,'TOURANE','ĐÀ NẴNG');const A=strip('GIỮA THẾ KỶ 20',true,46,101),B=strip('DÙNG LẠI TRÊN GIẤY TỜ',false,38,102),C=strip('GIỮ ĐẾN NAY',false,40,103);const ck=CK(g);bm(tf);
 return{upd:t=>{F(t,540,640,1.2,inn(t,R(10)+.05,.3));sh(A,t,540,380,-2,PV(t,10,'giữa',.6));sh(B,t,540,1080,1,PV(t,10,'dùng',3.2));sh(C,t,540,1170,-1,PV(t,10,'giữ',4.6));PUT(ck,880,520,popv(t,tf+.4,.4),.7,0)}}});
// 11 năm 1997 Đà Nẵng tách khỏi Quảng Nam – Đà Nẵng, trực thuộc trung ương (ranh giới tỉnh trước 2025, nét đứt)
S2(11,11,'d',t=>'1997',g=>{const m=vnmap(960,880,111);const old=['Đà Nẵng','Quảng Nam'].map(n=>{const p=TINH63.find(q=>q.n==n);return el(m.riv,'path',{d:p.p.map(rpath).join(''),fill:n=='Đà Nẵng'?'rgba(242,193,78,.75)':'rgba(255,255,255,.08)',stroke:'#fff8e6','stroke-width':3,'stroke-dasharray':'10 8','vector-effect':'non-scaling-stroke',opacity:0})});
 const L=[['ĐÀ NẴNG',108.15,16.05],['QUẢNG NAM',107.9,15.55]].map(([n,lo,la])=>({e:MLB(m.top,n,30,'#fff'),lo,la}));const A=strip('TÁCH KHỎI QUẢNG NAM – ĐÀ NẴNG',false,34,111),B=strip('TRỰC THUỘC TRUNG ƯƠNG',true,44,112);const H=strip('RANH GIỚI TRƯỚC NĂM 2025',false,20,113);const SH=SEAH();bm(AT(11,'trực',5.6));
 return{upd:t=>{const e=inn(t,R(11)-.2,.5);m.at(540,760,0,1,e);m.view(108.0,15.75,lerp(245,290,inn(t,R(11),E(11)-R(11))));seaH(SH,t,e,false);sh(H,t,250,1235,0,e);old.forEach((o,i)=>o.setAttribute('opacity',i==0?inn(t,AT(11,'tách',2.6),.4):e));L.forEach((o,i)=>{const[x,y]=m.P(o.lo,o.la);o.e.setAttribute('x',x);o.e.setAttribute('y',y);o.e.setAttribute('opacity',i==0?inn(t,AT(11,'tách',2.6),.4):inn(t,AT(11,'Quảng',3.4),.4))});
  sh(A,t,540,400,-2,PV(t,11,'tách',2.6));sh(B,t,540,480,1,PV(t,11,'trực',5.6))}}});
// 12 năm 2025 Đà Nẵng và Quảng Nam nhập làm một; điều thú vị ở cái tên
S2(12,12,'p',t=>'2025',g=>{const m=vnmap(960,880,121);const old=['Đà Nẵng','Quảng Nam'].map(n=>{const p=TINH63.find(q=>q.n==n);return el(m.riv,'path',{d:p.p.map(rpath).join(''),fill:'none',stroke:'#fff8e6','stroke-width':3,'stroke-dasharray':'10 8','vector-effect':'non-scaling-stroke',opacity:0})});const A=strip('NHẬP LÀM MỘT',true,50,121);const q=T(g,0,0,'TÊN?',110,CGOLD,12,'middle',OLN);const SH=SEAH();const tn=AT(12,'nhập',3.8);bm(tn);
 return{upd:t=>{const e=inn(t,R(12)-.2,.5);m.at(540,760,0,1,e);m.view(108.0,15.75,lerp(290,250,inn(t,R(12),E(12)-R(12))));seaH(SH,t,e);old.forEach(o=>o.setAttribute('opacity',e*(1-inn(t,tn+.4,.6))));m.hi('Đà Nẵng',inn(t,tn,.6),CGOLD);sh(A,t,540,400,-2,popv(t,tn,.5));PUT(q,820,560,popv(t,AT(12,'tên',6.0)-.3,.5),1,Math.sin(t*3)*5)}}});
// 13 Quảng Nam rộng gấp khoảng tám lần Đà Nẵng cũ, vẫn mang tên Đà Nẵng
S2(13,13,'d',null,g=>{const X0=120,W=840,Y1=560,Y2=760;const b1=el(g,'rect',{x:X0,y:Y1-45,width:0,height:90,rx:12,fill:CSTEEL,stroke:'#fff','stroke-width':5}),b2=el(g,'rect',{x:X0,y:Y2-45,width:0,height:90,rx:12,fill:CGOLD,stroke:'#fff','stroke-width':5});const l1=strip('QUẢNG NAM',false,34,131),l2=strip('ĐÀ NẴNG CŨ',false,34,132);const A=strip('GẤP KHOẢNG 8 LẦN',true,46,133);const st=stamp('TÊN: ĐÀ NẴNG',56);const tm=AT(13,'mang',4.6);bm(tm);
 return{upd:t=>{const u1=inn(t,R(13)+.1,1.2),u2=inn(t,AT(13,'cũ',3.0)-.6,.6);b1.setAttribute('width',W*u1);b2.setAttribute('width',W/8.2*u2);sh(l1,t,X0+140,Y1-90,-2,inn(t,R(13)+.1,.4));sh(l2,t,X0+140,Y2-90,2,inn(t,AT(13,'cũ',3.0)-.6,.4));sh(A,t,560,960,-1,PV(t,13,'gấp',1.4));const su=popv(t,tm,.45);st.at(540,1140,-6,su,su>0?1:0)}}});
// 14 từng nhường chỗ cho tên Tây, giờ tên Đà Nẵng phủ cả đất Quảng Nam
S2(14,14,'p',null,g=>{const m=vnmap(960,880,141);const lab=MLB(m.top,'ĐÀ NẴNG',52,'#fff',OLN);const tg=strip('TOURANE',false,34,141);const x1=XX(g);const A=strip('PHỦ CẢ ĐẤT QUẢNG NAM',true,44,142);const SH=SEAH();bm(AT(14,'phủ',4.0),true);
 return{upd:t=>{const e=inn(t,R(14)-.2,.5);m.at(540,760,0,1,e);m.view(108.0,15.75,lerp(240,280,inn(t,R(14),E(14)-R(14))));seaH(SH,t,e);m.hi('Đà Nẵng',inn(t,AT(14,'giờ',2.4),.6),CGOLD);const[x,y]=m.P(108.0,15.7);lab.setAttribute('x',x);lab.setAttribute('y',y);lab.setAttribute('opacity',inn(t,AT(14,'giờ',2.4),.5));
  sh(tg,t,220,620,-3,popv(t,R(14)+.1,.5));PUT(x1,220,620,popv(t,AT(14,'Tây',2.0),.4),.5,0);sh(A,t,600,400,2,PV(t,14,'phủ',4.0))}}});
// 15 câu hỏi: tên giấy tờ khác tên người dân gọi
S2(15,15,'d',null,g=>{const dc=DOC(g,'TÊN GIẤY TỜ');const pp=[0,1,2].map(i=>fig(g,{hat:[CGOLD,'#c9b48a',CRED][i]}));const bb=bubble(g,300,120,'TÊN KHÁC!',56);const ne=T(g,0,0,'≠',150,CGOLD,12,'middle',OLN);const A=strip('Ở QUÊ BẠN CÓ KHÔNG?',true,44,151);bm(R(15)+.2);
 return{upd:t=>{PUT(dc,280,640,popv(t,AT(15,'giấy',1.8)-.3,.5),.7,-3+Math.sin(t*1.4));PUT(ne,540,660,popv(t,AT(15,'khác',2.4),.45),1,0);pp.forEach((p,i)=>p.at(700+i*120,900,.8,0,popv(t,AT(15,'người',3.0)+i*.12,.5)));bb.at(820,500,.9,popv(t,AT(15,'gọi',4.0),.5));sh(A,t,540,1140,-1,popv(t,R(15)+.2,.5))}}});
