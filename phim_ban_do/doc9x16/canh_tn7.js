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
// ===== CẢNH
const TH=[105.78,19.80];
const SEAH=()=>[strip('QĐ. HOÀNG SA (VIỆT NAM) ↘',false,22,901),strip('QĐ. TRƯỜNG SA (VIỆT NAM) ↓',false,22,902),strip('RANH GIỚI HIỆN NAY',false,20,903)];
const seaH=(L,t,e,lab)=>{sh(L[0],t,820,1180,0,e);sh(L[1],t,820,1235,0,e);sh(L[2],t,250,1235,0,e*(lab===false?0:1))};
const CARD=(g,txt,col=CSTEEL,w=360)=>{const k=el(g,'g',{});el(k,'rect',{x:-w/2,y:-70,width:w,height:140,rx:16,fill:col,stroke:'#fff','stroke-width':7});const t=MLB(k,txt,Math.min(46,Math.floor(w*1.3/txt.length)),'#fff',col);t.setAttribute('y',16);return{k,t,r:k.children[0]}};
const putC=(c,x,y,s)=>{c.k.setAttribute('transform',`translate(${x},${y}) scale(${s})`);c.k.setAttribute('opacity',s>0?1:0)};
const flipC=(c,tf,a,b,ca,cb)=>(t,x,y,sc)=>{const fl=inn(t,tf-.3,.4);c.k.setAttribute('transform',`translate(${x},${y}) scale(${sc*Math.max(.02,Math.abs(1-2*fl))},${sc})`);c.k.setAttribute('opacity',sc>0?1:0);if(fl>.5){c.t.textContent=b;c.r.setAttribute('fill',cb)}else{c.t.textContent=a;c.r.setAttribute('fill',ca)}};
const BIG=(g,txt,sz=110,col='#fff')=>{const t=T(g,0,0,txt,sz,col,Math.round(sz*.09),'middle',OLN);t.setAttribute('font-weight',900);return t};
const ACC=(g)=>{const k=el(g,'g',{});el(k,'path',{d:'M-14 22 L18 -26',stroke:'#fff','stroke-width':24,'stroke-linecap':'round'});el(k,'path',{d:'M-14 22 L18 -26',stroke:CRED,'stroke-width':14,'stroke-linecap':'round'});return k};
// 1 hook: Thanh Hóa từng mất dấu sắc gần 400 năm, lấy lại vì tên mẹ một ông vua
S2(1,1,'d',null,g=>{const m=vnmap(940,860,71);const hs=hsts(m);const rg=RINGS(m.top,CGOLD);const lab=MLB(m.top,'THANH HOA',46,'#fff',OLN);const ac=ACC(g);const A=strip('MẤT DẤU SẮC GẦN 400 NĂM?',true,40,11),B=strip('VÌ TÊN MẸ MỘT ÔNG VUA',false,40,12);const SH=SEAH();const tl=AT(1,'lấy',3.8);bm(AT(1,'mất',1.6),true);bm(tl);
 return{upd:t=>{const e=inn(t,R(1)-.2,.5);m.at(540,760,0,1,e);m.view(106.2,19.6,lerp(170,210,inn(t,R(1),E(1)-R(1))));seaH(SH,t,e);hs(e);m.hi('Thanh Hóa',e,CGOLD);const[x,y]=m.P(...TH);RU(rg,t,80,x,y,e);
  const has=inn(t,tl,.3);lab.textContent=has>.5?'THANH HÓA':'THANH HOA';lab.setAttribute('x',x+40);lab.setAttribute('y',y-70);lab.setAttribute('opacity',e);
  const dy=lerp(-160,0,inn(t,tl-.2,.4));PUT(ac,540+x+40+92,760+y-70-58+dy,inn(t,tl-.2,.25),1,0);sh(A,t,540,380,-2,popv(t,AT(1,'mất',1.6),.5));sh(B,t,540,460,1,PV(t,1,'mẹ',5.4))}}});
// 2 khác một dấu, hai chữ Hán khác hẳn
S2(2,2,'p',null,g=>{const a=BIG(g,'THANH HÓA',90),b=BIG(g,'THANH HOA',90);const ne=T(g,0,0,'≠',120,CRED,10,'middle',OLN);const h1=HAN(g,'清化',150),h2=HAN(g,'清華',150);const A=strip('CHỈ KHÁC MỘT DẤU',false,40,21),B=strip('HAI CHỮ HÁN KHÁC HẲN',true,42,22);const th=AT(2,'Hán',3.8);bm(th);
 return{upd:t=>{PUT(a,300,520,popv(t,R(2)+.05,.5),1,0);PUT(b,780,520,popv(t,R(2)+.3,.5),1,0);PUT(ne,540,500,popv(t,AT(2,'khác',1.8),.4),1,0);sh(A,t,540,330,-2,PV(t,2,'khác',1.8));
  PUT(h1,300,820,popv(t,th,.5),1,0);PUT(h2,780,820,popv(t,th+.2,.5),1,0);sh(B,t,540,1080,1,popv(t,th,.5))}}});
// 3 Cửu Chân rồi Ái Châu
S2(3,3,'d',null,g=>{const c1=CARD(g,'CỬU CHÂN','#7a5a32',360),c2=CARD(g,'ÁI CHÂU',CSTEEL,360);const ar=el(g,'path',{d:'M-60 0 L50 0 M20 -30 L55 0 L20 30',fill:'none',stroke:CGOLD,'stroke-width':14,'stroke-linecap':'round','stroke-linejoin':'round'});const A=strip('NGÀY XƯA',false,42,31);const tc=AT(3,'Ái',2.6);bm(AT(3,'Cửu',1.4),true);bm(tc,true);
 return{upd:t=>{sh(A,t,540,330,-2,PV(t,3,'Ngày',.2));putC(c1,540,600+Math.sin(t*1.6)*5,popv(t,AT(3,'Cửu',1.4),.5));ar.setAttribute('transform','translate(540,770) rotate(90)');ar.setAttribute('opacity',inn(t,tc-.4,.3));putC(c2,540,960+Math.sin(t*1.6+1)*5,popv(t,tc,.5))}}});
// 4 1029 Lý Thái Tông đổi Ái Châu thành phủ Thanh Hóa, lần đầu xuất hiện
S2(4,4,'p',t=>'1029',g=>{const c=CARD(g,'ÁI CHÂU',CSTEEL,460);const tf=AT(4,'phủ',3.6);const F=flipC(c,tf,'ÁI CHÂU','PHỦ THANH HÓA',CSTEEL,CGOLD);const cr=CROWN(g);const A=strip('VUA LÝ THÁI TÔNG',false,42,41);const st=stamp('LẦN ĐẦU XUẤT HIỆN',50);const tl=AT(4,'lần',5.0);bm(tf);bm(tl,true);
 return{upd:t=>{PUT(cr,540,470,popv(t,AT(4,'vua',1.0),.5),.9,Math.sin(t*1.5)*3);sh(A,t,540,330,-2,PV(t,4,'vua',1.0));F(t,540,760,popv(t,R(4)+.1,.5));const su=popv(t,tl,.45);st.at(540,1000,-5,su,su>0?1:0)}}});
// 5 Thanh là trong, Hóa là biến đổi; mong lòng người trong sáng, yên ổn
S2(5,5,'d',null,g=>{const h1=HAN(g,'清',200),h2=HAN(g,'化',200);const a1=strip('THANH = TRONG',true,42,51),a2=strip('HÓA = BIẾN ĐỔI',true,42,52);const rg=RINGS(g,RIV,3);const B=strip('MONG LÒNG NGƯỜI TRONG SÁNG, YÊN ỔN',false,34,53);const th=AT(5,'Hóa',2.0);bm(AT(5,'Thanh',.6),true);bm(th,true);
 return{upd:t=>{PUT(h1,320,560,popv(t,AT(5,'Thanh',.6)-.2,.5),1,0);sh(a1,t,320,740,-2,popv(t,AT(5,'Thanh',.6),.45));PUT(h2,760,560,popv(t,th-.2,.5),1,0);sh(a2,t,760,740,2,popv(t,th,.45));RU(rg,t,200,540,920,inn(t,AT(5,'mong',4.4),.5));sh(B,t,540,1110,1,PV(t,5,'mong',4.4))}}});
// 6 1469 Lê Thánh Tông đổi thành Thanh Hoa, chữ Hoa tốt đẹp rực rỡ
S2(6,6,'p',t=>'1469',g=>{const c=CARD(g,'THANH HÓA',CGOLD,460);const tf=AT(6,'Thanh',3.2);const F=flipC(c,tf,'THANH HÓA','THANH HOA',CGOLD,CRED);const A=strip('VUA LÊ THÁNH TÔNG',false,42,61);const h=HAN(g,'華',170);const B=strip('HOA = TỐT ĐẸP, RỰC RỠ',true,40,62);const sp=[...Array(8)].map(()=>el(g,'path',{d:'M0 -16 L4 -4 L16 0 L4 4 L0 16 L-4 4 L-16 0 L-4 -4Z',fill:CGOLD,stroke:'#fff','stroke-width':3}));const th=AT(6,'Hoa',4.4);bm(tf);
 return{upd:t=>{sh(A,t,540,330,-2,PV(t,6,'vua',1.4));F(t,540,560,popv(t,R(6)+.1,.5));PUT(h,540,840,popv(t,th,.5),1,0);sh(B,t,540,1060,1,popv(t,th,.5));sp.forEach((e,i)=>{const a=i/8*Math.PI*2+t*.6,r=150+Math.sin(t*3+i)*12;PUT(e,540+Math.cos(a)*r,840+Math.sin(a)*r*.7,popv(t,th+.2+i*.05,.3),1,t*60)})}}});
// 7 Thanh Hoa dùng suốt thời Lê, sang thời Nguyễn
S2(7,7,'d',null,g=>{const bar=el(g,'path',{d:'M140 760 L940 760',stroke:'#c9b48a','stroke-width':10,'stroke-linecap':'round',pathLength:1,'stroke-dasharray':'1 1','stroke-dashoffset':1});const d1=CARD(g,'THỜI LÊ','#7a5a32',260),d2=CARD(g,'THỜI NGUYỄN','#7a5a32',300);const tag=strip('THANH HOA',true,44,71);const tn=AT(7,'Nguyễn',3.6);bm(tn,true);
 return{upd:t=>{const u=inn(t,R(7)+.1,E(7)-R(7)-.4);bar.setAttribute('stroke-dashoffset',1-u);putC(d1,260,900,popv(t,AT(7,'Lê',2.2)-.2,.45));putC(d2,820,900,popv(t,tn-.2,.45));sh(tag,t,lerp(200,880,u),640,Math.sin(t*2)*2,popv(t,R(7)+.1,.45))}}});
// 8 vua Thiệu Trị lên ngôi, mẹ là bà Hồ Thị Hoa
S2(8,8,'p',null,g=>{const cr=CROWN(g);const k=fig(g,{hat:CGOLD});const A=strip('VUA THIỆU TRỊ LÊN NGÔI',false,42,81);const c=CARD(g,'MẸ VUA: HỒ THỊ HOA',CSTEEL,560);const rg=RINGS(g,CRED,3);const th=AT(8,'Hồ',4.0);bm(AT(8,'Thiệu',.9));bm(th,true);
 return{upd:t=>{sh(A,t,540,330,-2,PV(t,8,'Thiệu',.9));k.at(540,780,.9,0,popv(t,R(8)+.1,.5));PUT(cr,540,410+60*0,popv(t,AT(8,'lên',1.8),.5),.6,0);cr.setAttribute('transform',`translate(540,${430+Math.sin(t*2)*4}) scale(${.6*popv(t,AT(8,'lên',1.8),.5)})`);putC(c,540,980,popv(t,th-.3,.5));RU(rg,t,90,760,980,inn(t,th+.4,.4))}}});
// 9 lệ kiêng tên: tên vua và hoàng tộc không viết, không đọc thẳng
S2(9,9,'d',null,g=>{const sc=SCRL(g,460,360);const bl=[0,1].map(()=>el(g,'rect',{width:150,height:30,rx:6,fill:CRED,stroke:'#fff','stroke-width':4}));const A=strip('LỆ KIÊNG TÊN',true,50,91),B=strip('KHÔNG VIẾT, KHÔNG ĐỌC THẲNG',false,38,92);const tk=AT(9,'không',3.6);bm(AT(9,'kiêng',.8));bm(tk,true);
 return{upd:t=>{sh(A,t,540,330,-2,PV(t,9,'kiêng',.8));PUT(sc,540,760+Math.sin(t*1.4)*6,popv(t,R(9)+.1,.5),1,-2);bl.forEach((b,i)=>{const v=inn(t,tk+i*.3,.3);b.setAttribute('x',440+i*40);b.setAttribute('y',700+i*92+Math.sin(t*1.4)*6);b.setAttribute('opacity',v);b.setAttribute('width',150*v)});sh(B,t,540,1080,1,popv(t,tk,.5))}}});
// 10 chữ Hoa gặp rắc rối, giấy tờ phải viết chệch
S2(10,10,'p',null,g=>{const dc=SCRL(g,460,300);const w1=MLB(g,'TỈNH THANH',46,'#3a2a14','#e8dcba'),w2=MLB(g,'HOA',46,CRED,'#e8dcba');const x1=XX(g);const pp=[0,1].map(i=>fig(g,{hat:['#c9b48a',CSTEEL][i]}));const bb=bubble(g,180,110,'?',80);const A=strip('CHỮ HOA GẶP RẮC RỐI',true,44,101),B=strip('GIẤY TỜ PHẢI VIẾT CHỆCH',false,40,102);const tr=AT(10,'rắc',1.6);bm(tr);
 return{upd:t=>{sh(A,t,540,330,-2,popv(t,tr,.5));const e=popv(t,R(10)+.1,.5);PUT(dc,400,640,e,1,-3);[w1,w2].forEach((w,i)=>{w.setAttribute('x',i?520:330);w.setAttribute('y',650);w.setAttribute('opacity',e)});w2.setAttribute('transform',`translate(${Math.sin(t*20)*3*inn(t,tr,.2)},0)`);PUT(x1,520,635,popv(t,tr+.3,.4),.6,0);
  pp.forEach((p,i)=>p.at(760+i*140,1000,.75,Math.sin(t*2+i)*4,popv(t,AT(10,'giấy',3.4)+i*.15,.5)));bb.at(880,560,.8,popv(t,AT(10,'giấy',3.4)+.3,.5));sh(B,t,400,880,1,PV(t,10,'giấy',3.4))}}});
// 11 1843 Thiệu Trị đổi hẳn thành tỉnh Thanh Hóa, lấy lại tên cổ
S2(11,11,'d',t=>'1843',g=>{const c=CARD(g,'THANH HOA',CRED,460);const tf=AT(11,'tỉnh',3.0);const F=flipC(c,tf,'THANH HOA','TỈNH THANH HÓA',CRED,CGOLD);const A=strip('VUA THIỆU TRỊ',false,42,111);const st=stamp('LẤY LẠI TÊN CỔ',56);const ck=CK(g);const tc=AT(11,'cổ',6.0);bm(tf);bm(tc,true);
 return{upd:t=>{sh(A,t,540,330,-2,PV(t,11,'vua',1.0));F(t,540,620,popv(t,R(11)+.1,.5));PUT(ck,860,480,popv(t,tf+.3,.4),.6,0);const su=popv(t,tc-.6,.45);st.at(540,900,-5,su,su>0?1:0)}}});
// 12 tên đầu tiên quay lại sau hơn 370 năm
S2(12,12,'p',null,g=>{const ys=[['1029','THANH HÓA',CGOLD],['1469','THANH HOA',CRED],['1843','THANH HÓA',CGOLD]];const L=el(g,'path',{d:'M180 760 L900 760',stroke:'#c9b48a','stroke-width':8,'stroke-linecap':'round'});const dots=ys.map(()=>el(g,'circle',{r:16,fill:'#fff',stroke:OLN,'stroke-width':5}));const yl=ys.map(y=>MLB(g,y[0],40,'#3a2a14','#efe8d2'));const nl=ys.map(y=>MLB(g,y[1],30,'#fff',y[2]));
 const arc=el(g,'path',{d:'M900 700 Q540 480 180 700',fill:'none',stroke:CGOLD,'stroke-width':10,'stroke-dasharray':'1 1',pathLength:1,'stroke-dashoffset':1,'stroke-linecap':'round'});const A=strip('QUAY TRỞ LẠI',true,48,121),B=strip('SAU HƠN 370 NĂM VẮNG BÓNG',false,38,122);const tq=AT(12,'quay',2.4);bm(tq);
 return{upd:t=>{const e=popv(t,R(12)+.05,.5);L.setAttribute('opacity',e);ys.forEach((y,i)=>{const x=180+i*360,v=popv(t,R(12)+.15+i*.2,.4);dots[i].setAttribute('cx',x);dots[i].setAttribute('cy',760);dots[i].setAttribute('opacity',v);yl[i].setAttribute('x',x);yl[i].setAttribute('y',840);yl[i].setAttribute('opacity',v);nl[i].setAttribute('x',x);nl[i].setAttribute('y',900);nl[i].setAttribute('opacity',v)});
  arc.setAttribute('stroke-dashoffset',1-inn(t,tq,.9));sh(A,t,540,400,-2,popv(t,tq,.5));sh(B,t,540,1080,1,PV(t,12,'sau',3.6))}}});
// 13 từ đó không đổi; 2025 Thanh Hóa giữ nguyên
S2(13,13,'d',t=>'2025',g=>{const m=vnmap(940,860,131);const hs=hsts(m);const lab=MLB(m.top,'THANH HÓA',44,'#fff',OLN);const A=strip('TỪ ĐÓ KHÔNG ĐỔI NỮA',false,40,131);const st=stamp('GIỮ NGUYÊN',60);const SH=SEAH();const tg=AT(13,'giữ',6.6);bm(tg);
 return{upd:t=>{const e=inn(t,R(13)-.2,.5);m.at(540,760,0,1,e);m.view(106.2,19.6,lerp(210,170,inn(t,R(13),E(13)-R(13))));seaH(SH,t,e);hs(e);m.hi('Thanh Hóa',e,CGOLD);const[x,y]=m.P(105.3,20.0);lab.setAttribute('x',x);lab.setAttribute('y',y);lab.setAttribute('opacity',e);
  sh(A,t,540,330,-2,PV(t,13,'Từ',.2));const su=popv(t,tg,.45);st.at(540,1030,-5,su,su>0?1:0)}}});
// 14 Thanh Hóa không phải viết sai; Thanh Hoa mới là tên đến sau
S2(14,14,'p',null,g=>{const a=CARD(g,'THANH HÓA',CGOLD,420),b=CARD(g,'THANH HOA',CRED,420);const la=strip('TÊN GỐC · 1029',true,38,141),lb=strip('ĐẾN SAU · 1469',false,38,142);const ck=CK(g);const x1=XX(g);const A=strip('KHÔNG PHẢI VIẾT SAI',false,40,143);const ts=AT(14,'sau',4.0);bm(AT(14,'sai',1.6),true);bm(ts);
 return{upd:t=>{putC(a,540,560,popv(t,R(14)+.05,.5));sh(A,t,540,330,-2,PV(t,14,'sai',1.6));PUT(x1,840,560,popv(t,AT(14,'sai',1.6),.4)*(1-inn(t,ts-.5,.3)),.5,0);PUT(ck,840,560,popv(t,ts,.4),.55,0);sh(la,t,540,680,-1,popv(t,ts,.45));putC(b,540,900,popv(t,AT(14,'Thanh',2.6),.5));sh(lb,t,540,1020,1,popv(t,ts+.2,.45))}}});
// 15 câu hỏi: tỉnh nào khác từng đổi tên vì kiêng tên vua?
S2(15,15,'d',null,g=>{const m=vnmap(560,820,151);const hs=hsts(m);const qs=[[105.85,21.0],[106.68,20.86],[107.6,16.4],[108.2,16.05],[106.7,10.8],[105.75,10.05],[105.7,18.7],[108.95,13.8]].map(()=>T(m.top,0,0,'?',44,CGOLD,6,'middle',OLN));const A=strip('TỈNH NÀO KHÁC?',true,44,151),B=strip('ĐỔI TÊN VÌ KIÊNG TÊN VUA',false,32,152);const tq=AT(15,'tỉnh',1.0);bm(tq);
 return{upd:t=>{const e=inn(t,R(15)-.2,.5);m.at(330,740,-1,1,e);m.view(108.6,15.9,44);hs(e);m.hi('Thanh Hóa',e,CGOLD);const P0=[[105.85,21.0],[106.68,20.86],[107.6,16.4],[108.2,16.05],[106.7,10.8],[105.75,10.05],[105.7,18.7],[108.95,13.8]];qs.forEach((q,i)=>{const[x,y]=m.P(...P0[i]);q.setAttribute('x',x);q.setAttribute('y',y+14+Math.sin(t*3+i)*5);q.setAttribute('opacity',popv(t,tq+.2+i*.15,.4))});
  sh(A,t,790,560,-2,popv(t,tq,.5));sh(B,t,780,650,2,PV(t,15,'kiêng',2.4))}}},9999);
