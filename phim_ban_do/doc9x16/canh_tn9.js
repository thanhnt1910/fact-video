// ===== TÊN TỈNH THÀNH #09: Quảng Ninh (tn9). Bản đồ hành chính phẳng 34 tỉnh (geoBoundaries, phạm vi công cộng), không vẽ nước láng giềng.
// Ranh giới cũ của Quảng Yên, Hồng Quảng, Hải Ninh không có dữ liệu tin cậy: chỉ đánh dấu bằng chấm và nhãn ở vị trí thị xã, không vẽ đường ranh giới cũ.
const HB=[];const bm=(t,l)=>{sx(t,'boom',l?{light:true,g:.8}:{g:1});if(!l)HB.push(t)};
const PUT=(o,x,y,u,sc=1,rot=0)=>{o.setAttribute('transform',`translate(${x},${y}) rotate(${rot}) scale(${Math.max(.001,u)*sc})`);o.setAttribute('opacity',u>0?1:0)};
const CRED='#d8372d',CGOLD='#e0a63c',CSTEEL='#7fa6c4',OLN='#0a1018',RIV='#5fb3e6',CSEA='#2f8f9d';
const CK=(g,col=CGOLD)=>{const k=el(g,'g',{});const d='M-60 5 L-20 50 L65 -55';el(k,'path',{d,fill:'none',stroke:'#fff','stroke-width':34,'stroke-linecap':'round','stroke-linejoin':'round'});el(k,'path',{d,fill:'none',stroke:col,'stroke-width':20,'stroke-linecap':'round','stroke-linejoin':'round'});return k};
const HAN=(g,txt,size,col=CGOLD)=>{const t=T(g,0,size*.36,txt,size,col,Math.round(size*.06),'middle',OLN);t.setAttribute('style',"font-family:'Noto Serif CJK TC','Noto Serif CJK SC',serif;font-weight:900");return t};
const MLB=(g,txt,sz=30,col='#fff',bg=OLN)=>{const t=T(g,0,0,txt,sz,col,Math.max(5,Math.round(sz*.2)),'middle',bg);t.setAttribute('font-weight',900);return t};
const RINGS=(g,col,n=3)=>[...Array(n)].map(()=>el(g,'circle',{fill:'none',stroke:col,'stroke-width':6,r:1,opacity:0}));
const RU=(rs,t,R0,cx,cy,on=1,sp=.5)=>rs.forEach((e,i)=>{const u=((t*sp+i/rs.length)%1);e.setAttribute('cx',cx);e.setAttribute('cy',cy);e.setAttribute('r',12+u*R0);e.setAttribute('opacity',(1-u)*.85*on)});
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
 o.riv=el(inner,'g',{});o.top=el(oc,'g',{});o.over=el(g,'g',{});o.prov=prov;o.st={clon:106,clat:16,ppd:60};
 o.view=(clon,clat,ppd)=>{o.st={clon,clat,ppd};inner.setAttribute('transform',`translate(${(-clon*ppd).toFixed(2)},${(clat*KYP*ppd).toFixed(2)}) scale(${ppd})`)};
 o.P=(lon,lat)=>[(lon-o.st.clon)*o.st.ppd,(o.st.clat-lat)*o.st.ppd*KYP];
 o.at=(x,y,rot=0,sc=1,op=1)=>{g.setAttribute('transform',`translate(${x},${y}) rotate(${rot}) scale(${sc})`);g.setAttribute('opacity',op)};
 o.hi=(n,u,col='#f2c14e')=>{const e=prov[n];if(!e)return;e.setAttribute('fill',u>0?col:PAL[TINH34.findIndex(p=>p.n==n)%PAL.length]);e.setAttribute('fill-opacity',u>0?.55+.45*u:1)};
 o.view(106,16,60);return o}
// Hoàng Sa, Trường Sa: nhãn theo tọa độ thật (đảo đã có trong dữ liệu Đà Nẵng, Khánh Hòa)
function hsts(m){const L=el(m.top,'g',{});const a=MLB(L,'QĐ. HOÀNG SA',20,'#fff'),a2=MLB(L,'(VIỆT NAM)',20,'#f2c14e');const b=MLB(L,'QĐ. TRƯỜNG SA',20,'#fff'),b2=MLB(L,'(VIỆT NAM)',20,'#f2c14e');[a,a2,b,b2].forEach(e=>e.setAttribute('text-anchor','end'));
 const H=[[111.6,16.5],[112.3,16.6],[111.2,16.0],[112.0,16.1]],S=[[114.3,10.4],[114.5,11.4],[113.9,9.9],[115.0,10.8]];
 const dots=H.map(()=>el(L,'circle',{r:5,fill:'#fff6d0',stroke:OLN,'stroke-width':2}));const dt=S.map(()=>el(L,'circle',{r:5,fill:'#fff6d0',stroke:OLN,'stroke-width':2}));
 return op=>{H.forEach((p,i)=>{const[x,y]=m.P(...p);dots[i].setAttribute('cx',x);dots[i].setAttribute('cy',y)});S.forEach((p,i)=>{const[x,y]=m.P(...p);dt[i].setAttribute('cx',x);dt[i].setAttribute('cy',y)});
  const[hx,hy]=m.P(111.1,16.3),[sx2,sy]=m.P(113.8,10.5);a.setAttribute('x',hx);a.setAttribute('y',hy-4);a2.setAttribute('x',hx);a2.setAttribute('y',hy+20);b.setAttribute('x',sx2);b.setAttribute('y',sy-4);b2.setAttribute('x',sx2);b2.setAttribute('y',sy+20);L.setAttribute('opacity',op)}}
const SIGN=(g,txt,col='#1d4f5a')=>{const k=el(g,'g',{});el(k,'rect',{x:-8,y:0,width:16,height:240,fill:'#9aa3ab',stroke:'#fff','stroke-width':4});el(k,'rect',{x:-230,y:-80,width:460,height:96,rx:12,fill:col,stroke:'#fff','stroke-width':7});const t=MLB(k,txt,44,'#fff',col);t.setAttribute('y',-16);return{k,t}};
// ===== Dấu ấn riêng (Quảng Ninh): nền tối xanh biển đêm, giấy xanh xám nhạt; núi đá vôi giữa vịnh và thuyền buồm mờ ở đáy, sóng biển chảy (y>1640)
{DR1.setAttribute('opacity',0);DR2.setAttribute('opacity',0);
 DARKG.firstChild.setAttribute('fill','#0e1d24');
 [...PAPG.children].forEach(c=>{if(c.tagName=='g')c.setAttribute('opacity',0);if(c.tagName=='line')c.setAttribute('stroke','rgba(0,0,0,0)')});
 PAPG.firstChild.setAttribute('fill','#e4e8dc');
 const dots=(p,col)=>{const g=el(p,'g',{});const r=rng(909);for(let i=0;i<80;i++)el(g,'circle',{cx:r()*1080,cy:200+r()*1300,r:1.5+r()*2.5,fill:col});return g};
 dots(DARKG,'rgba(150,210,220,.06)');dots(PAPG,'rgba(60,90,100,.10)');
 const sky=(p,col)=>{const g=el(p,'g',{});const L=(d,w=5)=>el(g,'path',{d,fill:'none',stroke:col,'stroke-width':w,'stroke-linejoin':'round','stroke-linecap':'round'});
  // núi đá vôi dựng đứng giữa vịnh
  for(const[x,w,h]of[[90,90,190],[230,70,140],[620,110,230],[790,80,160],[960,100,210]])L(`M${x-w/2} 1640 Q${x-w/2-8} ${1640-h*.6} ${x-w/4} ${1640-h} Q${x} ${1640-h-22} ${x+w/4} ${1640-h+6} Q${x+w/2+10} ${1640-h*.5} ${x+w/2} 1640`,5);
  // thuyền buồm
  for(const[x,s]of[[420,1],[520,.7]]){L(`M${x-70*s} 1622 Q${x} ${1650} ${x+70*s} 1622 Z`,5);L(`M${x} 1622 L${x} ${1622-130*s}`,4);L(`M${x} ${1500+(1-s)*40} Q${x+70*s} ${1550} ${x+60*s} ${1612}`,4)}
  return g};
 const skA=sky(DARKG,'rgba(120,200,210,.15)'),skB=sky(PAPG,'rgba(40,80,90,.18)');
 const wv=(p,col)=>[0,1,2].map(i=>el(p,'path',{fill:'none',stroke:col,'stroke-width':4+i,opacity:.6-i*.12}));
 const wA=wv(DARKG,'rgba(110,190,200,.35)'),wB=wv(PAPG,'rgba(40,90,100,.30)');
 window.THEME_UPD=t=>{const dx=Math.sin(t*.1)*14;skA.setAttribute('transform',`translate(${dx.toFixed(1)},0)`);skB.setAttribute('transform',`translate(${dx.toFixed(1)},0)`);[wA,wB].forEach(L=>L.forEach((e,i)=>{const y0=1690+i*62;let d='';for(let x=-20;x<=1100;x+=28){const y=y0+Math.sin(x*.012+t*(1.0+i*.3)+i)*9;d+=(x<0?'M':'L')+x+' '+y.toFixed(1)}e.setAttribute('d',d)}))};
}
// ===== CẢNH
const QN=[107.25,21.2],QY=[106.81,20.94],HG=[107.08,20.95],MC=[107.97,21.53],HQ=[106.95,21.05],HN9=[107.6,21.42];
const SEAH=()=>[strip('QĐ. HOÀNG SA (VIỆT NAM) ↓',false,22,901),strip('RANH GIỚI HIỆN NAY',false,20,903)];
const seaH=(L,t,e)=>{sh(L[0],t,820,1235,0,e);sh(L[1],t,250,1235,0,e)};
// thẻ chữ có viền (dùng cho trò ghép chữ)
const TILE=(g,txt,col=CGOLD,w=300,fg=OLN)=>{const k=el(g,'g',{});el(k,'rect',{x:-w/2,y:-62,width:w,height:124,rx:18,fill:col,stroke:'#fff','stroke-width':8});const t=T(k,0,30,txt,78,fg,0,'middle');t.setAttribute('font-weight',900);return k};
// chấm thị xã + nhãn trên bản đồ
const PIN=(m,txt,col=CRED,dy=-26,dx=0)=>{const k=el(m.top,'g',{});el(k,'circle',{r:13,fill:col,stroke:'#fff','stroke-width':5});const t=MLB(k,txt,30,'#fff');t.setAttribute('y',dy);t.setAttribute('x',dx);return k};
const PINAT=(m,k,p,u)=>{const[x,y]=m.P(...p);k.setAttribute('transform',`translate(${x},${y}) scale(${Math.max(.001,u)})`);k.setAttribute('opacity',u>0?1:0)};
// núi đá vôi, xe goòng than
const KPATH=(x,w,h)=>`M${x-w*.75} 0 C${x-w*.55} -10 ${x-w*.6} ${-h*.45} ${x-w*.45} ${-h*.6} L${x-w*.3} ${-h*.62} C${x-w*.28} ${-h*.85} ${x-w*.12} ${-h} ${x+w*.02} ${-h} C${x+w*.18} ${-h*.98} ${x+w*.2} ${-h*.8} ${x+w*.3} ${-h*.75} C${x+w*.42} ${-h*.7} ${x+w*.5} ${-h*.4} ${x+w*.48} ${-h*.2} C${x+w*.55} -10 ${x+w*.7} 0 ${x+w*.85} 0Z`;
const KARST=(g,col='#3d6f6a')=>{const k=el(g,'g',{});for(const[x,w,h,c]of[[-220,160,250,'#2f5f5a'],[0,210,340,col],[230,150,220,'#2f5f5a']])el(k,'path',{d:KPATH(x,w,h),fill:c,stroke:'#fff','stroke-width':6,'stroke-linejoin':'round'});return k};
const CART=(g)=>{const k=el(g,'g',{});el(k,'path',{d:'M-120 -70 L120 -70 L95 30 L-95 30Z',fill:'#5a5f66',stroke:'#fff','stroke-width':7,'stroke-linejoin':'round'});for(let i=0;i<6;i++)el(k,'circle',{cx:-80+i*32,cy:-82-(i%2)*14,r:24,fill:'#15171a',stroke:'#3a3d42','stroke-width':3});for(const x of[-60,60])el(k,'circle',{cx:x,cy:44,r:22,fill:'#2a2d31',stroke:'#fff','stroke-width':6});el(k,'path',{d:'M-200 70 L200 70',stroke:'#9aa3ab','stroke-width':8});return k};
const BULB=(g)=>{const k=el(g,'g',{});el(k,'circle',{cx:0,cy:-30,r:70,fill:'#ffe08a',stroke:'#fff','stroke-width':7});el(k,'rect',{x:-32,y:34,width:64,height:46,rx:8,fill:'#9aa3ab',stroke:'#fff','stroke-width':6});for(let i=0;i<7;i++){const a=-Math.PI+i*Math.PI/6;el(k,'path',{d:`M${Math.cos(a)*92} ${-30+Math.sin(a)*92} L${Math.cos(a)*122} ${-30+Math.sin(a)*122}`,stroke:'#ffe08a','stroke-width':9,'stroke-linecap':'round'})}return k};
// bản đồ dùng chung cho các cảnh tỉnh (khung 960x880, tâm Quảng Ninh)
const QMAP=(seed)=>{const m=vnmap(960,880,seed);return m};
// 1 hook: tên Quảng Ninh là tên ghép, mỗi chữ từ một nơi, Bác Hồ gợi ý
S2(1,1,'d',null,g=>{const m=vnmap(560,820,91);const hs=hsts(m);const rg=RINGS(m.top,CGOLD);const A=strip('QUẢNG NINH',true,62,11);const q=TILE(g,'QUẢNG',CGOLD,300),n=TILE(g,'NINH','#7fd0d8',260);const pl=T(g,0,0,'+',90,'#fff',8,'middle',OLN);const B=strip('TÊN GHÉP',false,44,12);const C=strip('BÁC HỒ GỢI Ý',true,44,13);const tg=AT(1,'ghép',2.6);bm(tg);
 return{upd:t=>{const e=inn(t,R(1)-.2,.5);m.at(300,720,-1,1,e);m.view(107.0,16.2,42+4*inn(t,R(1),E(1)-R(1)));hs(e);m.hi('Quảng Ninh',inn(t,AT(1,'Quảng',1.2),.5),CGOLD);const[x,y]=m.P(...QN);RU(rg,t,90,x,y,inn(t,AT(1,'Quảng',1.2),.4));
  sh(A,t,800,380,-3,PV(t,1,'Quảng',1.2));const u=popv(t,tg-.1,.5),sp=1-inn(t,AT(1,'khác',4.4)-.3,.5)*.0;PUT(q,780,560,u,.8,-4+Math.sin(t*2)*2);PUT(pl,800,660,u,1,0);PUT(n,800,760,popv(t,tg+.2,.5),.8,4+Math.sin(t*2+1)*2);sh(B,t,800,880,2,popv(t,tg,.5));
  sh(C,t,540,1120,-1,PV(t,1,'Bác',6.4))}}});
// 2 cái tên còn khá trẻ: mới có trên bản đồ hơn 60 năm
S2(2,2,'p',null,g=>{const cal=el(g,'g',{});el(cal,'rect',{x:-200,y:-200,width:400,height:400,rx:24,fill:'#fff',stroke:OLN,'stroke-width':8});el(cal,'rect',{x:-200,y:-200,width:400,height:100,rx:24,fill:CRED,stroke:OLN,'stroke-width':8});for(const x of[-110,110])el(cal,'rect',{x:x-12,y:-236,width:24,height:70,rx:10,fill:'#9aa3ab',stroke:OLN,'stroke-width':5});const num=T(cal,0,110,'60+',170,OLN,0,'middle');num.setAttribute('font-weight',900);const yr=MLB(cal,'NĂM',40,'#fff',CRED);yr.setAttribute('y',-136);
 const A=strip('CÒN KHÁ TRẺ',true,52,21),B=strip('MỚI CÓ TRÊN BẢN ĐỒ',false,38,22);const t6=AT(2,'sáu',5.0);bm(t6);
 return{upd:t=>{sh(A,t,540,380,-2,popv(t,AT(2,'trẻ',1.6)-.3,.5));PUT(cal,540,780,popv(t,AT(2,'Nó',2.6)-.2,.55),1,-3+Math.sin(t*1.5)*2);const k=Math.round(lerp(0,60,inn(t,t6-.6,1.0)));num.textContent=k>=60?'60+':String(k);sh(B,t,540,1140,1,PV(t,2,'bản',3.6))}}});
// 3 ngày xưa có tỉnh Quảng Yên (chỉ đánh dấu vị trí thị xã Quảng Yên, không vẽ ranh giới cũ)
S2(3,3,'d',null,g=>{const m=QMAP(31);const rg=RINGS(m.top,CRED);const pq=PIN(m,'QUẢNG YÊN');const A=strip('NGÀY XƯA',false,40,31),B=strip('TỈNH QUẢNG YÊN',true,48,32);const C=strip('CHẤM: VỊ TRÍ THỊ XÃ',false,20,33);const SH=SEAH();const tq=AT(3,'Quảng',3.4);bm(tq);
 return{upd:t=>{const e=inn(t,R(3)-.2,.5);m.at(540,760,0,1,e);m.view(107.3,21.05,lerp(360,420,inn(t,R(3),E(3)-R(3))));seaH(SH,t,e);m.hi('Quảng Ninh',e*.35,'#cdb98a');const[x,y]=m.P(...QY);RU(rg,t,90,x,y,inn(t,tq,.4));PINAT(m,pq,QY,popv(t,tq-.1,.5));
  sh(A,t,540,400,-2,popv(t,R(3)+.05,.5));sh(B,t,540,480,1,popv(t,tq,.5));sh(C,t,850,330,0,inn(t,tq,.4))}}});
// 4 năm 1955: Quảng Yên nhập với đặc khu Hồng Gai thành khu Hồng Quảng
S2(4,4,'p',t=>'1955',g=>{const m=QMAP(41);const pq=PIN(m,'QUẢNG YÊN',CRED,-30,-60),ph=PIN(m,'HỒNG GAI','#2a7fa0',58,60);const blob=el(m.top,'circle',{fill:'rgba(242,193,78,.30)',stroke:CGOLD,'stroke-width':6,'stroke-dasharray':'14 10'});const lab=MLB(m.top,'KHU HỒNG QUẢNG',40,OLN,CGOLD);
 const A=strip('NHẬP LÀM MỘT',false,38,41),B=strip('KHU HỒNG QUẢNG',true,48,42);const SH=SEAH();const th=AT(4,'Hồng',5.2);bm(th);
 return{upd:t=>{const e=inn(t,R(4)-.2,.5);m.at(540,760,0,1,e);m.view(107.0,21.0,lerp(520,560,inn(t,R(4),E(4)-R(4))));seaH(SH,t,e);
  const mv=inn(t,AT(4,'nhập',3.0),1.0);const mid=[(QY[0]+HG[0])/2,(QY[1]+HG[1])/2];PINAT(m,pq,[lerp(QY[0],mid[0]-.05,mv),lerp(QY[1],mid[1],mv)],popv(t,R(4)+.2,.5)*(1-inn(t,th+.6,.4)));PINAT(m,ph,[lerp(HG[0],mid[0]+.05,mv),lerp(HG[1],mid[1],mv)],popv(t,AT(4,'đặc',3.8)-.3,.5)*(1-inn(t,th+.6,.4)));
  const[x,y]=m.P(...mid);const u=popv(t,th,.6);blob.setAttribute('cx',x);blob.setAttribute('cy',y);blob.setAttribute('r',150*u);blob.setAttribute('opacity',u>0?1:0);lab.setAttribute('x',x);lab.setAttribute('y',y+12);lab.setAttribute('opacity',inn(t,th+.3,.4));
  sh(A,t,540,400,-2,PV(t,4,'nhập',3.0));sh(B,t,540,1110,1,popv(t,th,.5))}}});
// 5 ngay cạnh khu Hồng Quảng là tỉnh Hải Ninh (đánh dấu Móng Cái, nơi đặt tỉnh lỵ)
S2(5,5,'d',null,g=>{const m=QMAP(51);const ph=PIN(m,'HỒNG QUẢNG',CGOLD),pn=PIN(m,'HẢI NINH','#7fd0d8');const ar=el(m.top,'path',{fill:'none',stroke:'#fff','stroke-width':8,'stroke-linecap':'round','stroke-dasharray':'16 12'});const A=strip('NGAY CẠNH',false,40,51),B=strip('TỈNH HẢI NINH',true,48,52);const SH=SEAH();const tn=AT(5,'Hải',1.6);bm(tn);
 return{upd:t=>{const e=inn(t,R(5)-.2,.5);m.at(540,760,0,1,e);m.view(107.4,21.2,lerp(300,330,inn(t,R(5),E(5)-R(5))));seaH(SH,t,e);PINAT(m,ph,HQ,e);PINAT(m,pn,HN9,popv(t,tn-.1,.5));
  const[x1,y1]=m.P(...HQ),[x2,y2]=m.P(...HN9);const u=inn(t,R(5)+.2,.7);ar.setAttribute('d',`M${x1+30} ${y1} L${lerp(x1+30,x2-30,u)} ${lerp(y1,y2,u)}`);
  sh(A,t,540,400,-2,popv(t,R(5)+.05,.5));sh(B,t,540,1110,1,popv(t,tn,.5))}}});
// 6 năm 1963: Quốc hội quyết định nhập khu Hồng Quảng và tỉnh Hải Ninh làm một
S2(6,6,'p',t=>'1963',g=>{const m=QMAP(61);const ph=PIN(m,'HỒNG QUẢNG',CGOLD),pn=PIN(m,'HẢI NINH','#7fd0d8');const rg=RINGS(m.top,CGOLD);const A=strip('QUỐC HỘI QUYẾT ĐỊNH',false,38,61),B=strip('NHẬP LÀM MỘT',true,50,62);const SH=SEAH();const tm=AT(6,'một',7.0);bm(AT(6,'nhập',3.4));
 return{upd:t=>{const e=inn(t,R(6)-.2,.5);m.at(540,760,0,1,e);m.view(107.35,21.15,lerp(330,300,inn(t,R(6),E(6)-R(6))));seaH(SH,t,e);const mv=inn(t,AT(6,'nhập',3.4),1.2);
  PINAT(m,ph,[lerp(HQ[0],QN[0]-.12,mv),lerp(HQ[1],QN[1],mv)],e*(1-inn(t,tm,.4)));PINAT(m,pn,[lerp(HN9[0],QN[0]+.12,mv),lerp(HN9[1],QN[1],mv)],e*(1-inn(t,tm,.4)));
  m.hi('Quảng Ninh',inn(t,tm-.2,.6),CGOLD);const[x,y]=m.P(...QN);RU(rg,t,110,x,y,inn(t,tm,.4));sh(A,t,540,400,-2,PV(t,6,'Quốc',2.0));sh(B,t,540,1110,1,popv(t,tm-.3,.5))}}});
// 7 tỉnh mới cần một cái tên; Bác Hồ gợi ý cách đặt (không vẽ chân dung)
S2(7,7,'d',null,g=>{const s=SIGN(g,'TỈNH ???');const b=BULB(g);const A=strip('TỈNH MỚI CẦN MỘT CÁI TÊN',false,36,71),B=strip('BÁC HỒ GỢI Ý CÁCH ĐẶT',true,44,72);const tb=AT(7,'Bác',4.0);bm(tb);
 return{upd:t=>{sh(A,t,540,380,-2,popv(t,R(7)+.05,.5));PUT(s.k,540,640,popv(t,AT(7,'tên',2.0)-.4,.55),1.1,Math.sin(t*1.6)*1.5);s.t.textContent=Math.floor(t*3)%2?'TỈNH ???':'TỈNH ??';
  PUT(b,540,1040,popv(t,tb,.5),.8,Math.sin(t*2)*4);sh(B,t,540,1240,1,popv(t,tb+.1,.5))}}});
// 8 lấy chữ Quảng của Hồng Quảng, ghép chữ Ninh của Hải Ninh, thành Quảng Ninh
S2(8,8,'p',null,g=>{const h1=TILE(g,'HỒNG','#cdb98a',250),q=TILE(g,'QUẢNG',CGOLD,300),h2=TILE(g,'HẢI','#cdb98a',220),n=TILE(g,'NINH','#7fd0d8',260);const res=strip('QUẢNG NINH',true,72,81);const ck=CK(g);
 const tq=AT(8,'Quảng',1.0),tn=AT(8,'Ninh',4.0),tt=AT(8,'thành',5.6);bm(tt);
 return{upd:t=>{const a=popv(t,R(8)+.05,.5),b=popv(t,AT(8,'ghép',3.0)-.1,.5);const fq=inn(t,tq+.6,.8),fn=inn(t,tn+.4,.8),go=inn(t,tt,.4);
  PUT(h1,lerp(260,260,fq),480,a*(1-.6*fq)*(1-go),.85,0);PUT(q,lerp(560,380,go),lerp(480,880,fq),a,.85+.15*fq,Math.sin(t*2)*2*(1-go));
  PUT(h2,260,660,b*(1-.6*fn)*(1-go),.85,0);PUT(n,lerp(530,700,go),lerp(660,880,fn),b,.85+.15*fn,Math.sin(t*2+1)*2*(1-go));
  sh(res,t,540,1110,-1,popv(t,tt+.2,.5));PUT(ck,880,1100,popv(t,tt+.5,.4),.6,0)}}});
// 9 theo lời Bác, Quảng Ninh còn có nghĩa: một vùng đất lớn an bình (chữ Hán 廣寧)
S2(9,9,'d',null,g=>{const sc=SCRL(g,560,380);const h1=HAN(g,'廣',150,CGOLD),h2=HAN(g,'寧',150,'#7fd0d8');const A=strip('THEO LỜI BÁC',false,40,91),B=strip('MỘT VÙNG ĐẤT LỚN',true,46,92),C=strip('AN BÌNH',true,56,93);const tl=AT(9,'lớn',5.0),ta=AT(9,'an',5.6);bm(ta);
 return{upd:t=>{sh(A,t,540,380,-2,popv(t,R(9)+.05,.5));const u=popv(t,AT(9,'Quảng',1.4)-.2,.55);PUT(sc,540,700,u,1,-2+Math.sin(t*1.4));PUT(h1,420,700,u,1,0);PUT(h2,660,700,u,1,0);
  sh(B,t,540,1000,-1,popv(t,AT(9,'vùng',4.0),.5));sh(C,t,540,1110,2,popv(t,ta,.5))}}});
// 10 từ đó tên Quảng Ninh gắn với vịnh Hạ Long, những mỏ than lớn của miền Bắc
S2(10,10,'p',null,g=>{const k=KARST(g);const sea=[0,1,2].map(i=>el(g,'path',{fill:'none',stroke:CSEA,'stroke-width':8-i*2,'stroke-linecap':'round'}));const c=CART(g);const nm=TILE(g,'QUẢNG NINH',CGOLD,640);const A=strip('VỊNH HẠ LONG',true,50,101),B=strip('MỎ THAN LỚN',true,50,102),C=strip('TỪ ĐÓ',false,40,103);const th=AT(10,'Hạ',4.2),tm=AT(10,'mỏ',6.4);bm(th);bm(tm,true);
 return{upd:t=>{sh(C,t,540,360,-2,popv(t,R(10)+.05,.5));PUT(nm,540,700+Math.sin(t*1.5)*8,popv(t,R(10)+.1,.5)*(1-inn(t,th-.5,.3)),1,Math.sin(t*1.2)*2);const u=popv(t,th-.2,.55);PUT(k,540+Math.sin(t*.8)*14,700,u,1+.05*inn(t,th,E(10)-th),0);sea.forEach((e,i)=>{let d='';for(let x=120;x<=960;x+=16)d+=(x==120?'M':'L')+x+' '+(712+i*26+Math.sin(x*.025+t*2.5+i)*8).toFixed(1);e.setAttribute('d',d);e.setAttribute('opacity',u>0?1:0)});sh(A,t,540,820,-1,popv(t,th,.5));
  PUT(c,lerp(1300,540,inn(t,tm-.5,.8))+Math.sin(t*1.5)*10,1030+Math.abs(Math.sin(t*5))*-6,1,.9,0);sh(B,t,540,1200,1,popv(t,tm,.5))}}});
// 11 năm 2025 sắp xếp lại, Quảng Ninh là một trong những tỉnh giữ nguyên
S2(11,11,'d',t=>'2025',g=>{const m=vnmap(640,900,111);const hs=hsts(m);const ck=CK(g);const A=strip('CẢ NƯỚC SẮP XẾP LẠI',false,36,111),B=strip('GIỮ NGUYÊN',true,56,112),H=strip('34 TỈNH, THÀNH · RANH GIỚI HIỆN NAY',false,20,113);const tg=AT(11,'giữ',8.0);bm(tg);
 return{upd:t=>{const e=inn(t,R(11)-.2,.5);m.at(540,780,0,1,e);const z=inn(t,tg-1,1.2);m.view(lerp(106.6,107.0,z),lerp(16.2,19.6,z),lerp(40,95,z)+4*inn(t,R(11),tg-1-R(11)));hs(e*(1-inn(t,tg-1,.6)));
  m.hi('Quảng Ninh',inn(t,AT(11,'Quảng',4.0),.5),CGOLD);sh(A,t,540,330,-2,PV(t,11,'sắp',2.8));sh(H,t,540,1250,0,e);PUT(ck,800,600,popv(t,tg,.4),.8,0);sh(B,t,540,1180,1,popv(t,tg,.5))}}});
// 12 hai tên cũ Hồng Quảng và Hải Ninh, mỗi tên còn để lại một chữ
S2(12,12,'p',null,g=>{const h1=TILE(g,'HỒNG','#cdb98a',250),q=TILE(g,'QUẢNG',CGOLD,300),h2=TILE(g,'HẢI','#cdb98a',220),n=TILE(g,'NINH','#7fd0d8',260);const A=strip('HAI TÊN CŨ',false,40,121),B=strip('MỖI TÊN CÒN MỘT CHỮ',true,44,122);const tc=AT(12,'chữ',6.4);bm(tc);
 return{upd:t=>{sh(A,t,540,360,-2,popv(t,R(12)+.05,.5));const a=popv(t,AT(12,'Hồng',2.4)-.2,.5),b=popv(t,AT(12,'Hải',3.4)-.2,.5),f=inn(t,tc-.4,.8);
  PUT(h1,lerp(270,270,f),560,a*(1-f),.85,0);PUT(q,lerp(560,380,f),lerp(560,880,f),a,.85+.15*f,0);PUT(h2,260,720,b*(1-f),.85,0);PUT(n,lerp(530,700,f),lerp(720,880,f),b,.85+.15*f,0);sh(B,t,540,1110,1,popv(t,tc,.5))}}});
// 13 câu hỏi: tỉnh nào khác cũng từng có tên ghép như vậy?
S2(13,13,'d',null,g=>{const a=TILE(g,'?',CGOLD,160),b=TILE(g,'?','#7fd0d8',160);const pl=T(g,0,0,'+',90,'#fff',8,'middle',OLN);const q=T(g,0,0,'?',220,CGOLD,14,'middle',OLN);const A=strip('TỈNH NÀO KHÁC?',true,52,131),B=strip('CŨNG CÓ TÊN GHÉP',false,40,132);bm(R(13)+.2);
 return{upd:t=>{PUT(q,540,560,popv(t,R(13)+.1,.5),1,Math.sin(t*3)*6);const u=popv(t,AT(13,'ghép',4.2)-.3,.5);PUT(a,360,880,u,1,-4+Math.sin(t*2)*3);PUT(pl,540,880,u,1,0);PUT(b,720,880,u,1,4+Math.sin(t*2+1)*3);sh(A,t,540,1080,-1,popv(t,R(13)+.2,.5));sh(B,t,540,1180,1,PV(t,13,'ghép',4.2))}}});
