// ===== TÊN TỈNH THÀNH #05: Hải Phòng (tn5). Bản đồ hành chính phẳng 34 tỉnh (geoBoundaries, phạm vi công cộng), không vẽ nước láng giềng.
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
// ===== Dấu ấn riêng (Hải Phòng): nền tối xanh than cảng, giấy kem; nét Nhà hát lớn Hải Phòng, cẩu cảng, tàu ở đáy; hoa phượng đỏ rơi chậm; sóng (y>1640)
{DR1.setAttribute('opacity',0);DR2.setAttribute('opacity',0);
 DARKG.firstChild.setAttribute('fill','#101c26');
 [...PAPG.children].forEach(c=>{if(c.tagName=='g')c.setAttribute('opacity',0);if(c.tagName=='line')c.setAttribute('stroke','rgba(0,0,0,0)')});
 PAPG.firstChild.setAttribute('fill','#efe6cf');
 const sky=(p,col)=>{const g=el(p,'g',{});const L=(d,w=5)=>el(g,'path',{d,fill:'none',stroke:col,'stroke-width':w,'stroke-linejoin':'round','stroke-linecap':'round'});
  // Nhà hát lớn: thân, hàng cột, trán tường tam giác, hai tháp bên
  L('M330 1620 L330 1520 L750 1520 L750 1620',6);L('M380 1520 L540 1450 L700 1520',6);for(let i=0;i<8;i++)L(`M${400+i*40} 1620 L${400+i*40} 1540`,4);
  L('M300 1620 L300 1480 L360 1480 L360 1620 M720 1620 L720 1480 L780 1480 L780 1620',5);L('M300 1480 L330 1440 L360 1480 M720 1480 L750 1440 L780 1480',5);
  // cẩu cảng bên phải
  L('M900 1620 L900 1420 L1060 1420 M900 1440 L980 1420 M1040 1420 L1040 1480',6);L('M860 1620 L940 1620',6);
  // tàu bên trái
  L('M20 1610 L230 1610 L200 1650 L50 1650Z',5);L('M90 1610 L90 1560 L170 1560 L170 1610',4);
  return g};
 const skA=sky(DARKG,'rgba(224,166,60,.16)'),skB=sky(PAPG,'rgba(70,80,100,.18)');
 const pet=(p,col)=>{const r=rng(55);return[...Array(14)].map(()=>({e:el(p,'circle',{r:4+r()*5,fill:col}),x:r()*1080,s:.3+r()*.5,ph:r()*6}))};
 const pA=pet(DARKG,'rgba(216,55,45,.35)'),pB=pet(PAPG,'rgba(216,55,45,.28)');
 const wv=(p,col)=>[0,1,2].map(i=>el(p,'path',{fill:'none',stroke:col,'stroke-width':4+i,opacity:.6-i*.12}));
 const wA=wv(DARKG,'rgba(127,166,196,.40)'),wB=wv(PAPG,'rgba(60,90,120,.30)');
 window.THEME_UPD=t=>{const dx=Math.sin(t*.1)*14;skA.setAttribute('transform',`translate(${dx.toFixed(1)},0)`);skB.setAttribute('transform',`translate(${dx.toFixed(1)},0)`);
  [pA,pB].forEach(P=>P.forEach(o=>{const y=200+((t*40*o.s+o.ph*200)%1450);o.e.setAttribute('cx',(o.x+Math.sin(t*.8+o.ph)*30).toFixed(1));o.e.setAttribute('cy',y.toFixed(1));o.e.setAttribute('opacity',y>1250&&y<1520?0:1)}));
  [wA,wB].forEach(L=>L.forEach((e,i)=>{const y0=1680+i*64;let d='';for(let x=-20;x<=1100;x+=26){const y=y0+Math.sin(x*.016-t*(1.6+i*.4)+i)*13;d+=(x<0?'M':'L')+x+' '+y.toFixed(1)}e.setAttribute('d',d)}))};
}
// ===== CẢNH
const HP=[106.68,20.86],HD=[106.33,20.94],KA=[106.63,20.81];
const SEAH=()=>[strip('QĐ. HOÀNG SA (VIỆT NAM) ↘',false,22,901),strip('QĐ. TRƯỜNG SA (VIỆT NAM) ↓',false,22,902),strip('RANH GIỚI HIỆN NAY',false,20,903)];
const seaH=(L,t,e,lab)=>{sh(L[0],t,820,1180,0,e);sh(L[1],t,820,1235,0,e);sh(L[2],t,250,1235,0,e*(lab===false?0:1))};
const CARD=(g,txt,col=CSTEEL,w=360)=>{const k=el(g,'g',{});el(k,'rect',{x:-w/2,y:-70,width:w,height:140,rx:16,fill:col,stroke:'#fff','stroke-width':7});const t=MLB(k,txt,Math.min(46,Math.floor(w*1.6/txt.length)),'#fff',col);t.setAttribute('y',16);return{k,t}};
const BOAT=(g,col='#6a4a2a')=>{const k=el(g,'g',{});el(k,'path',{d:'M-90 0 Q0 40 90 0 L70 -14 L-70 -14Z',fill:col,stroke:'#fff','stroke-width':5,'stroke-linejoin':'round'});el(k,'path',{d:'M-30 -14 Q0 -60 30 -14Z',fill:'#c9b48a',stroke:'#fff','stroke-width':4});return k};
const CRANE=(g)=>{const k=el(g,'g',{});const L=(d,w=10)=>{el(k,'path',{d,fill:'none',stroke:'#fff','stroke-width':w+8,'stroke-linecap':'round','stroke-linejoin':'round'});el(k,'path',{d,fill:'none',stroke:CGOLD,'stroke-width':w,'stroke-linecap':'round','stroke-linejoin':'round'})};L('M-60 0 L-30 -260 L30 -260 L60 0 M-45 -130 L45 -130');L('M-30 -260 L-200 -260 M30 -260 L140 -260 M0 -260 L0 -320 L-200 -260');const hk=el(k,'path',{d:'M-180 -260 L-180 -120',stroke:'#fff','stroke-width':4});return{k,hk}};
const CRATE=(g,col)=>{const k=el(g,'g',{});el(k,'rect',{x:-50,y:-36,width:100,height:72,rx:6,fill:col,stroke:'#fff','stroke-width':5});for(let i=-1;i<=1;i++)el(k,'path',{d:`M${i*30} -36 L${i*30} 36`,stroke:'rgba(0,0,0,.25)','stroke-width':5});return k};
const FLAG=(g)=>{const k=el(g,'g',{});el(k,'rect',{x:-4,y:-220,width:10,height:260,fill:'#c9c2b0',stroke:'#fff','stroke-width':3});const f=el(k,'path',{fill:'#da251d',stroke:'#fff','stroke-width':4});const s=el(k,'path',{fill:'#ffde00'});return{k,u:t=>{let d='M6 -220';for(let x=0;x<=150;x+=15)d+=` L${6+x} ${-220+Math.sin(x*.05-t*4)*6}`;for(let x=150;x>=0;x-=15)d+=` L${6+x} ${-120+Math.sin(x*.05-t*4)*6}`;f.setAttribute('d',d+'Z');const cx=81,cy=-170+Math.sin(75*.05-t*4)*6,R=26;let p='';for(let i=0;i<10;i++){const a=-Math.PI/2+i*Math.PI/5,r=i%2?R*.4:R;p+=(i?'L':'M')+(cx+r*Math.cos(a)).toFixed(1)+' '+(cy+r*Math.sin(a)).toFixed(1)}s.setAttribute('d',p+'Z')}}};
const oldP=(m,n,fill,dash=true)=>{const p=TINH63.find(q=>q.n==n);return el(m.riv,'path',{d:p.p.map(rpath).join(''),fill,stroke:'#fff8e6','stroke-width':3,'stroke-dasharray':dash?'10 8':'none','vector-effect':'non-scaling-stroke',opacity:0})};
const mlab=(m,txt,sz,col,bg)=>MLB(m.top,txt,sz,col,bg);
const putL=(m,e,lo,la,dy,op)=>{const[x,y]=m.P(lo,la);e.setAttribute('x',x);e.setAttribute('y',y+dy);e.setAttribute('opacity',op)};
// 1 hook: Hải Phòng từng là góc nhỏ của Hải Dương, giờ Hải Dương nhập vào Hải Phòng
S2(1,1,'d',null,g=>{const m=vnmap(940,860,51);const hs=hsts(m);const rg=RINGS(m.top,CGOLD);const dot=el(m.top,'circle',{r:13,fill:CGOLD,stroke:'#fff','stroke-width':5});const lHP=mlab(m,'HẢI PHÒNG',30,'#fff'),lHD=mlab(m,'HẢI DƯƠNG',30,'#fff');
 const A=strip('TỪNG LÀ GÓC NHỎ CỦA HẢI DƯƠNG',false,38,11),B=strip('GIỜ HẢI DƯƠNG NHẬP VÀO HẢI PHÒNG',true,38,12);const SH=SEAH();const tg=AT(1,'góc',2.4),tn=AT(1,'nhập',5.2);bm(tg,true);bm(tn);
 return{upd:t=>{const e=inn(t,R(1)-.2,.5);m.at(540,760,0,1,e);m.view(106.9,20.75,lerp(260,330,inn(t,R(1),E(1)-R(1))));seaH(SH,t,e);hs(e);
  const[x,y]=m.P(...HP);dot.setAttribute('cx',x);dot.setAttribute('cy',y);dot.setAttribute('opacity',e);RU(rg,t,70,x,y,inn(t,R(1)+.3,.4)*(1-inn(t,tn,.4)));putL(m,lHP,HP[0]+.05,HP[1],-30,e);putL(m,lHD,HD[0]-.02,HD[1]+.1,-10,inn(t,tg,.4));
  m.hi('Hải Phòng',inn(t,tn,.6),CGOLD);sh(A,t,540,380,-2,popv(t,tg,.5)*(1-inn(t,tn-.2,.3)));sh(B,t,540,380,2,popv(t,tn,.5))}}});
// 2 con lớn hơn mẹ; gần 140 năm
S2(2,2,'p',null,g=>{const mo=fig(g,{hat:CSTEEL}),co=fig(g,{hat:CGOLD});const A=strip('CON LỚN HƠN MẸ?',true,50,21),B=strip('CHUYỆN CÓ THẬT',false,40,22);const n=T(g,0,0,'0',120,CGOLD,12,'middle',OLN);const nl=strip('NĂM',false,36,23);const tl=AT(2,'lớn',1.2),tn=AT(2,'gần',4.4);bm(tl);
 return{upd:t=>{const u=inn(t,tl,1.4);mo.at(380,860,lerp(1.25,.75,u),0,popv(t,R(2)+.05,.5));co.at(680,860,lerp(.55,1.45,u),0,popv(t,R(2)+.2,.5));sh(A,t,540,330,-2,PV(t,2,'lớn',1.2));sh(B,t,540,1060,1,PV(t,2,'có',3.4));
  const v=inn(t,tn,1.2);n.textContent='~'+Math.round(140*v);PUT(n,440,1190,popv(t,tn,.4),1,0);sh(nl,t,640,1170,0,popv(t,tn,.4))}}});
// 3 cửa sông Cấm, vài làng chài, bến Ninh Hải
S2(3,3,'d',null,g=>{const rv=[0,1,2].map(i=>el(g,'path',{fill:'none',stroke:RIV,'stroke-width':9-i*2,'stroke-linecap':'round'}));const bs=[0,1,2].map(i=>BOAT(g,['#6a4a2a','#7a5a32','#5a3e22'][i]));const hs=[0,1,2].map(()=>{const k=el(g,'g',{});el(k,'path',{d:'M-50 0 L-50 -50 L0 -90 L50 -50 L50 0Z',fill:'#8a6a44',stroke:'#fff','stroke-width':5,'stroke-linejoin':'round'});el(k,'path',{d:'M-62 -46 L0 -100 L62 -46',fill:'none',stroke:'#c9b48a','stroke-width':10,'stroke-linecap':'round'});return k});
 const A=strip('CỬA SÔNG CẤM',false,42,31),B=strip('VÀI LÀNG CHÀI · HẢI DƯƠNG',false,36,32);const sg=SIGN(g,'BẾN NINH HẢI','#6a4a2a');const tb=AT(3,'Ninh',5.8);bm(tb);
 return{upd:t=>{const u=inn(t,R(3)+.05,.8);rv.forEach((e,i)=>{let d='';for(let x=40;x<=40+1000*u;x+=14)d+=(x==40?'M':'L')+x+' '+(900+i*40+Math.sin(x*.025+t*2.4+i)*10).toFixed(1);e.setAttribute('d',d)});sh(A,t,540,330,-2,PV(t,3,'sông',1.0));
  hs.forEach((h,i)=>PUT(h,200+i*170,760-(i%2)*20,popv(t,AT(3,'làng',2.0)+i*.12,.45),1,0));bs.forEach((b,i)=>PUT(b,(260+i*300+t*12)%1100,930+i*40+Math.sin(t*2+i)*6,popv(t,AT(3,'chài',2.4)+i*.1,.45),1,Math.sin(t*1.6+i)*3));sh(B,t,540,1110,1,PV(t,3,'chài',2.4));
  const su=popv(t,tb-.1,.5);sg.k.setAttribute('transform',`translate(820,470) scale(${su*.8})`);sg.k.setAttribute('opacity',su>0?1:0)}}});
// 4 khoảng 1870 vua Tự Đức giao Bùi Viện lập đồn canh: nha Hải Phòng sứ
S2(4,4,'p',t=>'1870',g=>{const ft=FORT(g);const pp=fig(g,{hat:CRED});const A=strip('VUA TỰ ĐỨC',false,42,41),B=strip('GIAO CHO BÙI VIỆN',false,40,42),C=strip('ĐỒN CANH GIỮ BỜ BIỂN',true,40,43);const st=stamp('NHA HẢI PHÒNG SỨ',50);const tn=AT(4,'nha',6.4);bm(AT(4,'vua',.8),true);bm(tn);
 return{upd:t=>{sh(A,t,540,320,-2,PV(t,4,'vua',.8));sh(B,t,540,410,1,PV(t,4,'Bùi',2.4));PUT(ft,560,820,popv(t,AT(4,'đồn',3.4),.55),1.1,Math.sin(t*1.2));pp.at(250,1000,.7,0,popv(t,AT(4,'Bùi',2.4),.5));sh(C,t,560,1050,-1,PV(t,4,'đồn',3.4));const su=popv(t,tn,.45);st.at(540,1170,-5,su,su>0?1:0)}}});
// 5 tên giải thích vài cách; Hải là biển, Phòng là canh giữ
S2(5,5,'d',null,g=>{const h1=HAN(g,'海',230),h2=HAN(g,'防',230);const A=strip('VÀI CÁCH GIẢI THÍCH',false,38,51),a1=strip('HẢI = BIỂN',true,44,52),a2=strip('PHÒNG = CANH GIỮ',true,44,53);const w=[0,1].map(i=>el(g,'path',{fill:'none',stroke:RIV,'stroke-width':7,'stroke-linecap':'round'}));const ft=FORT(g);const th=AT(5,'Hải',5.0),tp=AT(5,'Phòng',6.2);bm(th,true);bm(tp);
 return{upd:t=>{sh(A,t,540,330,-2,PV(t,5,'vài',1.4));PUT(h1,320,640,popv(t,th-.2,.5),1,0);PUT(h2,760,640,popv(t,tp-.2,.5),1,0);sh(a1,t,320,820,-2,popv(t,th,.45));sh(a2,t,760,820,2,popv(t,tp,.45));
  w.forEach((e,i)=>{let d='';for(let x=180;x<=460;x+=12)d+=(x==180?'M':'L')+x+' '+(960+i*30+Math.sin(x*.05+t*3+i)*9).toFixed(1);e.setAttribute('d',d);e.setAttribute('opacity',inn(t,th,.4))});PUT(ft,760,1010,popv(t,tp+.2,.45),.4,0)}}});
// 6 Pháp nhắm tới cảng; 1874 đặt sở thuế
S2(6,6,'p',t=>'1874',g=>{const sp=el(g,'g',{});drawShip(sp);const bx=BOX(g,'SỞ THUẾ');const A=strip('NGƯỜI PHÁP NHẮM TỚI CẢNG',true,40,61),B=strip('ĐẶT SỞ THUẾ NGAY TẠI CẢNG',false,38,62);const rv=[0,1].map(i=>el(g,'path',{fill:'none',stroke:RIV,'stroke-width':7-i*2,'stroke-linecap':'round'}));const tt=AT(6,'thuế',5.0);bm(AT(6,'Pháp',.9),true);bm(tt);
 return{upd:t=>{sh(A,t,540,330,-2,PV(t,6,'Pháp',.9));const u=inn(t,R(6)+.1,E(6)-R(6)-.6);PUT(sp,lerp(1150,700,u),860+Math.sin(t*2)*6,1,2.2,0);rv.forEach((e,i)=>{let d='';for(let x=40;x<=1040;x+=14)d+=(x==40?'M':'L')+x+' '+(960+i*36+Math.sin(x*.025+t*2.4+i)*9).toFixed(1);e.setAttribute('d',d)});
  PUT(bx,300,800,popv(t,tt-.2,.5),1,Math.sin(t*1.4)*2);sh(B,t,540,1130,1,PV(t,6,'đặt',3.6))}}});
// 7 1887 tách mấy huyện ven biển khỏi Hải Dương để lập tỉnh Hải Phòng
S2(7,7,'d',t=>'1887',g=>{const big=CARD(g,'HẢI DƯƠNG',CSTEEL,520);const sm=CARD(g,'TỈNH HẢI PHÒNG',CGOLD,380);const cut=el(g,'path',{d:'M0 -110 L0 110',stroke:CRED,'stroke-width':10,'stroke-dasharray':'20 14',fill:'none'});const A=strip('NGƯỜI PHÁP MỞ RỘNG CẢNG',false,38,71),B=strip('TÁCH MẤY HUYỆN VEN BIỂN',true,40,72);const tt=AT(7,'tách',2.4),tl=AT(7,'lập',5.4);bm(tt);bm(tl,true);
 return{upd:t=>{sh(A,t,540,330,-2,PV(t,7,'mở',.6));const u=inn(t,tl-.3,.8);big.k.setAttribute('transform',`translate(${540-110*u},700) scale(${popv(t,R(7)+.05,.5)})`);sh(B,t,540,460,1,PV(t,7,'tách',2.4));
  cut.setAttribute('transform',`translate(700,700)`);cut.setAttribute('opacity',inn(t,tt,.3)*(1-u));const v=popv(t,tl-.3,.5);sm.k.setAttribute('transform',`translate(${540+220*u},${700+220*u}) scale(${v})`);sm.k.setAttribute('opacity',v>0?1:0)}}});
// 8 một năm sau tách đôi: thành phố Hải Phòng và tỉnh Kiến An
S2(8,8,'p',t=>'1888',g=>{const a=CARD(g,'TỈNH HẢI PHÒNG',CGOLD,420);const b=CARD(g,'TP HẢI PHÒNG',CGOLD,340),c=CARD(g,'TỈNH KIẾN AN',CSTEEL,340);const A=strip('MỘT NĂM SAU',false,42,81),B=strip('TÁCH ĐÔI',true,50,82);const ts=AT(8,'tách',2.0);bm(ts);
 return{upd:t=>{sh(A,t,540,330,-2,PV(t,8,'năm',.6));const u=inn(t,ts,.7);const va=popv(t,R(8)+.05,.45)*(1-u);a.k.setAttribute('transform',`translate(540,720) scale(${va})`);a.k.setAttribute('opacity',va>0?1:0);
  const vb=popv(t,AT(8,'thành',3.0)-.2,.5),vc=popv(t,AT(8,'Kiến',4.2)-.2,.5);b.k.setAttribute('transform',`translate(${540-lerp(0,210,u)},${720-30*u}) scale(${vb*.95})`);b.k.setAttribute('opacity',vb>0?1:0);c.k.setAttribute('transform',`translate(${540+lerp(0,210,u)},${720+190*u}) scale(${vc*.95})`);c.k.setAttribute('opacity',vc>0?1:0);sh(B,t,540,460,1,popv(t,ts,.45))}}});
// 9 tàu thuyền đông; thương cảng lớn nhất miền Bắc thời Pháp thuộc
S2(9,9,'d',null,g=>{const cr=[0,1].map(()=>CRANE(g));const cs=[0,1,2,3].map(i=>CRATE(g,[CRED,CSTEEL,CGOLD,'#7a5a32'][i]));const ss=[0,1,2].map(()=>{const k=el(g,'g',{});drawShip(k);return k});const rv=[0,1].map(i=>el(g,'path',{fill:'none',stroke:RIV,'stroke-width':7-i*2,'stroke-linecap':'round'}));
 const A=strip('TÀU THUYỀN NGÀY CÀNG ĐÔNG',false,38,91),B=strip('THƯƠNG CẢNG LỚN NHẤT MIỀN BẮC',true,40,92);const ck=CK(g);const tl=AT(9,'lớn',4.4);bm(tl);
 return{upd:t=>{sh(A,t,540,330,-2,PV(t,9,'Tàu',.4));cr.forEach((c,i)=>PUT(c.k,300+i*420,860,popv(t,R(9)+.1+i*.15,.5),.9,0));cs.forEach((c,i)=>{const lift=Math.max(0,Math.sin(t*1.2+i*1.5))*60*(i<2?1:0);PUT(c,160+i*130+(i>1?260:0),900-lift,popv(t,AT(9,'đông',1.8)+i*.1,.4),.8,0)});
  ss.forEach((s,i)=>PUT(s,(1200-((t*50+i*380)%1400)),1000+i*30+Math.sin(t*2+i)*5,popv(t,R(9)+.2+i*.2,.4),1.3-i*.15,0));rv.forEach((e,i)=>{let d='';for(let x=40;x<=1040;x+=14)d+=(x==40?'M':'L')+x+' '+(1040+i*30+Math.sin(x*.025+t*2.4+i)*8).toFixed(1);e.setAttribute('d',d)});sh(B,t,540,1180,1,PV(t,9,'lớn',4.4));PUT(ck,920,460,popv(t,tl+.3,.4),.6,0)}}});
// 10 13/5/1955 người lính Pháp cuối cùng rời bến cảng, Hải Phòng được giải phóng
S2(10,10,'p',t=>'1955',g=>{const sp=el(g,'g',{});drawShip(sp);const fl=FLAG(g);const rg=RINGS(g,CRED,3);const A=strip('13/5/1955',true,54,101),B=strip('LÍNH PHÁP CUỐI CÙNG RỜI CẢNG',false,36,102),C=strip('HẢI PHÒNG ĐƯỢC GIẢI PHÓNG',true,42,103);const tg=AT(10,'giải',6.0);bm(R(10)+.2,true);bm(tg);
 return{upd:t=>{sh(A,t,540,330,-2,popv(t,R(10)+.2,.5));const u=inn(t,AT(10,'rời',3.6)-.4,2.4);PUT(sp,lerp(560,1250,u),900+Math.sin(t*2)*6,popv(t,AT(10,'lính',2.6),.4),1.8,0);sh(B,t,540,1110,1,PV(t,10,'lính',2.6));
  fl.u(t);PUT(fl.k,300,960,popv(t,tg-.2,.55),1.4,0);RU(rg,t,140,400,760,inn(t,tg,.4));sh(C,t,540,460,2,popv(t,tg,.5))}}});
// 11 1962 Kiến An nhập trở lại, hai nửa lại thành một Hải Phòng
S2(11,11,'d',t=>'1962',g=>{const b=CARD(g,'TP HẢI PHÒNG',CGOLD,340),c=CARD(g,'TỈNH KIẾN AN',CSTEEL,340),d=CARD(g,'HẢI PHÒNG',CGOLD,460);const A=strip('NHẬP TRỞ LẠI',true,48,111),B=strip('HAI NỬA LẠI THÀNH MỘT',false,40,112);const tn=AT(11,'nhập',3.0),tm=AT(11,'một',6.4);bm(tn,true);bm(tm);
 return{upd:t=>{const u=inn(t,tn,1.0),w=inn(t,tm-.3,.4);const v=popv(t,R(11)+.05,.45)*(1-w);[[b,-1,-30],[c,1,190]].forEach(([o,s,dy])=>{o.k.setAttribute('transform',`translate(${540+s*lerp(210,90,u)},${720+dy*(1-u)}) scale(${v*.95})`);o.k.setAttribute('opacity',v>0?1:0)});
  const vd=popv(t,tm-.2,.5);d.k.setAttribute('transform',`translate(540,720) scale(${vd*1.1})`);d.k.setAttribute('opacity',vd>0?1:0);sh(A,t,540,330,-2,PV(t,11,'nhập',3.0));sh(B,t,540,1060,1,PV(t,11,'hai',4.4))}}});
// 12 Hải Dương vẫn là tỉnh láng giềng, mỗi nơi một tên, hơn 100 năm (ranh giới trước 2025, nét đứt)
S2(12,12,'p',null,g=>{const m=vnmap(940,860,121);const hs=hsts(m);const o1=oldP(m,'Hải Dương','rgba(127,166,196,.55)'),o2=oldP(m,'Hải Phòng','rgba(224,166,60,.55)');const l1=mlab(m,'HẢI DƯƠNG',30,'#fff'),l2=mlab(m,'HẢI PHÒNG',30,'#fff');const A=strip('MỖI NƠI MỘT TÊN',true,46,121),B=strip('HƠN 100 NĂM',false,42,122);const H=strip('RANH GIỚI TRƯỚC NĂM 2025',false,20,123);const SH=SEAH();bm(AT(12,'tên',3.6),true);
 return{upd:t=>{const e=inn(t,R(12)-.2,.5);m.at(540,760,0,1,e);m.view(106.75,20.75,lerp(300,340,inn(t,R(12),E(12)-R(12))));seaH(SH,t,e,false);sh(H,t,250,1235,0,e);hs(e);o1.setAttribute('opacity',inn(t,AT(12,'Hải',.6),.4));o2.setAttribute('opacity',inn(t,AT(12,'mỗi',2.4),.4));
  putL(m,l1,106.42,21.05,0,inn(t,AT(12,'Hải',.6),.4));putL(m,l2,106.85,20.75,0,inn(t,AT(12,'mỗi',2.4),.4));sh(A,t,540,380,-2,PV(t,12,'tên',3.6));sh(B,t,540,460,1,PV(t,12,'hơn',5.0))}}});
// 13 2025 sắp xếp tỉnh; Hải Dương nhập vào Hải Phòng, tên chung là thành phố Hải Phòng
S2(13,13,'d',t=>'2025',g=>{const m=vnmap(940,860,131);const hs=hsts(m);const o1=oldP(m,'Hải Dương','none'),o2=oldP(m,'Hải Phòng','none');const lab=mlab(m,'HẢI PHÒNG',44,'#fff',OLN);const A=strip('SẮP XẾP LẠI CÁC TỈNH',false,38,131),B=strip('HẢI DƯƠNG NHẬP VÀO HẢI PHÒNG',true,38,132);const st=stamp('TÊN: HẢI PHÒNG',56);const SH=SEAH();const tn=AT(13,'nhập',4.6),tt=AT(13,'tên',6.4);bm(tn);bm(tt,true);
 return{upd:t=>{const e=inn(t,R(13)-.2,.5);m.at(540,760,0,1,e);m.view(106.9,20.75,lerp(340,280,inn(t,R(13),E(13)-R(13))));seaH(SH,t,e);hs(e);[o1,o2].forEach(o=>o.setAttribute('opacity',e*(1-inn(t,tn+.4,.6))));m.hi('Hải Phòng',inn(t,tn,.6),CGOLD);putL(m,lab,106.75,20.85,0,inn(t,tt,.4));
  sh(A,t,540,330,-2,PV(t,13,'sắp',1.2));sh(B,t,540,410,1,popv(t,tn,.5));const su=popv(t,tt+.2,.45);st.at(540,1160,-6,su*.9,su>0?1:0)}}});
// 14 góc nhỏ ngày nào ôm trọn cả tỉnh từng chứa mình
S2(14,14,'p',null,g=>{const big=el(g,'circle',{cx:540,cy:760,r:260,fill:'rgba(127,166,196,.35)',stroke:'#fff','stroke-width':7});const sm=el(g,'circle',{r:50,fill:'rgba(224,166,60,.85)',stroke:'#fff','stroke-width':7});const lb=MLB(g,'HẢI DƯƠNG',40,'#fff'),ls=MLB(g,'HẢI PHÒNG',34,'#fff');const A=strip('GÓC NHỎ NGÀY NÀO',false,42,141),B=strip('ÔM TRỌN CẢ TỈNH',true,48,142);const to=AT(14,'ôm',2.8);bm(to);
 return{upd:t=>{const e=popv(t,R(14)+.05,.5);const u=inn(t,to-.2,1.4);big.setAttribute('opacity',e*(1-.6*u));big.setAttribute('r',260*e);const r=lerp(50,320,u),cx=lerp(700,540,u),cy=lerp(900,760,u);sm.setAttribute('cx',cx);sm.setAttribute('cy',cy);sm.setAttribute('r',r*e);sm.setAttribute('fill-opacity',lerp(1,.6,u));
  lb.setAttribute('x',540);lb.setAttribute('y',lerp(640,700,u));lb.setAttribute('opacity',e);ls.setAttribute('x',cx);ls.setAttribute('y',lerp(cy+12,cy+90,u));ls.setAttribute('opacity',e);ls.setAttribute('font-size',lerp(34,54,u));sh(A,t,540,330,-2,PV(t,14,'góc',.6));sh(B,t,540,1150,1,popv(t,to,.5))}}});
// 15 câu hỏi: quê bạn từng mang những cái tên nào?
S2(15,15,'d',null,g=>{const m=vnmap(560,820,151);const hs=hsts(m);const qs=[[105.85,21.0],[106.68,20.86],[107.6,16.4],[108.2,16.05],[106.7,10.8],[105.75,10.05],[105.7,18.7],[108.95,13.8]].map(()=>T(m.top,0,0,'?',44,CGOLD,6,'middle',OLN));const A=strip('QUÊ BẠN',false,48,151),B=strip('TỪNG MANG TÊN GÌ?',true,46,152);const tq=AT(15,'quê',.6);bm(tq);
 return{upd:t=>{const e=inn(t,R(15)-.2,.5);m.at(330,740,-1,1,e);m.view(108.6,15.9,44);hs(e);const P0=[[105.85,21.0],[106.68,20.86],[107.6,16.4],[108.2,16.05],[106.7,10.8],[105.75,10.05],[105.7,18.7],[108.95,13.8]];qs.forEach((q,i)=>{const[x,y]=m.P(...P0[i]);q.setAttribute('x',x);q.setAttribute('y',y+14+Math.sin(t*3+i)*5);q.setAttribute('opacity',popv(t,tq+.2+i*.15,.4))});
  sh(A,t,810,560,-2,popv(t,tq,.5));sh(B,t,800,660,2,PV(t,15,'tên',2.4))}}});
