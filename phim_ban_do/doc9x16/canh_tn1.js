// ===== TÊN TỈNH THÀNH #01: Hà Nội (tn1). Bản đồ hành chính phẳng 34 tỉnh (geoBoundaries, phạm vi công cộng), không vẽ nước láng giềng.
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
const KYP=1.0861;const PAL=['#c9a96a','#b9945a','#d4b57a','#a9875a','#c2a06a','#bfa16f'];
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
 o.hi=(n,u,col=CGOLD)=>{const e=prov[n];if(!e)return;e.setAttribute('fill',u>0?col:PAL[TINH34.findIndex(p=>p.n==n)%PAL.length]);e.setAttribute('fill-opacity',u>0?.55+.45*u:1)};
 o.line=(pts,col=RIV,wd=6,dash)=>{const d='M'+pts.map(p=>p[0]+' '+(-p[1]*KYP).toFixed(3)).join('L');const e=el(o.riv,'path',{d,fill:'none',stroke:col,'stroke-width':wd,'vector-effect':'non-scaling-stroke','stroke-linecap':'round','stroke-linejoin':'round',pathLength:1,'stroke-dasharray':dash||'1 1','stroke-dashoffset':1});return u=>{e.setAttribute('stroke-dashoffset',1-cl(u));e.setAttribute('opacity',u>0?1:0)}};
 o.view(106,16,60);return o}
// Hoàng Sa, Trường Sa: nhãn theo tọa độ thật (đảo đã có trong dữ liệu Đà Nẵng, Khánh Hòa)
function hsts(m){const L=el(m.top,'g',{});const a=MLB(L,'QUẦN ĐẢO HOÀNG SA',22,'#fff'),a2=MLB(L,'(VIỆT NAM)',22,'#f2c14e');const b=MLB(L,'QUẦN ĐẢO TRƯỜNG SA',22,'#fff'),b2=MLB(L,'(VIỆT NAM)',22,'#f2c14e');
 const dots=[[111.6,16.5],[112.3,16.6],[111.2,16.0],[112.0,16.1]].map(()=>el(L,'circle',{r:5,fill:'#fff6d0',stroke:OLN,'stroke-width':2}));const dt=[[114.3,10.4],[114.5,11.4],[113.9,9.9],[115.0,10.8]].map(()=>el(L,'circle',{r:5,fill:'#fff6d0',stroke:OLN,'stroke-width':2}));
 return op=>{const H=[[111.6,16.5],[112.3,16.6],[111.2,16.0],[112.0,16.1]],S=[[114.3,10.4],[114.5,11.4],[113.9,9.9],[115.0,10.8]];H.forEach((p,i)=>{const[x,y]=m.P(...p);dots[i].setAttribute('cx',x);dots[i].setAttribute('cy',y)});S.forEach((p,i)=>{const[x,y]=m.P(...p);dt[i].setAttribute('cx',x);dt[i].setAttribute('cy',y)});
  const[hx,hy]=m.P(111.8,16.4),[sx2,sy]=m.P(114.4,10.6);a.setAttribute('x',hx);a.setAttribute('y',hy-44);a2.setAttribute('x',hx);a2.setAttribute('y',hy-18);b.setAttribute('x',sx2-10);b.setAttribute('y',sy-44);b2.setAttribute('x',sx2-10);b2.setAttribute('y',sy-18);L.setAttribute('opacity',op)}}
const HN=[105.82,21.03],HUE=[107.58,16.46],KB=[105.87,20.56],DT=[105.97,20.63];
const SHONG=[[105.42,21.3],[105.55,21.2],[105.684,21.15],[105.782,21.1],[105.847,21.05],[105.893,21.0],[105.887,20.95],[105.904,20.9],[105.91,20.85],[105.929,20.8],[105.964,20.75],[106.025,20.7],[106.031,20.65],[106.125,20.6],[106.162,20.55],[106.177,20.5],[106.213,20.45],[106.271,20.4],[106.288,20.35],[106.432,20.3]];
const SDAY=[[105.40,21.13],[105.58,21.06],[105.66,20.98],[105.71,20.90],[105.74,20.78],[105.77,20.68],[105.84,20.60],[105.91,20.54],[105.96,20.42],[105.99,20.33]];
// ===== Dấu ấn riêng: nền tối xanh sông, giấy dó nhạt có đường đồng mức; sóng nước chảy ở đáy khung (y>1600)
{DR1.setAttribute('opacity',0);DR2.setAttribute('opacity',0);
 DARKG.firstChild.setAttribute('fill','#0d1f2b');
 [...PAPG.children].forEach(c=>{if(c.tagName=='g')c.setAttribute('opacity',0);if(c.tagName=='line')c.setAttribute('stroke','rgba(0,0,0,0)')});
 PAPG.firstChild.setAttribute('fill','#e9dcc0');
 const cont=(p,col)=>{const g=el(p,'g',{});const r=rng(129);for(let i=0;i<7;i++){const cx=r()*1080,cy=200+r()*1100;for(let j=1;j<5;j++)el(g,'ellipse',{cx,cy,rx:j*70+r()*20,ry:j*44+r()*16,fill:'none',stroke:col,'stroke-width':2})}return g};
 cont(DARKG,'rgba(127,166,196,.07)');cont(PAPG,'rgba(120,90,40,.12)');
 const wv=(p,col)=>[0,1,2,3].map(i=>el(p,'path',{fill:'none',stroke:col,'stroke-width':4+i,opacity:.55-i*.1}));
 const wA=wv(DARKG,'rgba(95,179,230,.45)'),wB=wv(PAPG,'rgba(60,110,150,.35)');
 window.THEME_UPD=t=>{[wA,wB].forEach(L=>L.forEach((e,i)=>{const y0=1660+i*58;let d='';for(let x=-20;x<=1100;x+=30){const y=y0+Math.sin(x*.012+t*(1.2+i*.3)+i)*12;d+=(x<0?'M':'L')+x+' '+y.toFixed(1)}e.setAttribute('d',d)}))};
}
// ===== CẢNH
// 1 hook: cả nước, Hà Nội sáng lên, "chưa đầy 200 tuổi", ông vua nhà Nguyễn
S2(1,1,'d',null,g=>{const m=vnmap(560,820,11);const hs=hsts(m);const rg=RINGS(m.top,CGOLD);const A=strip('HÀ NỘI',true,120,12);const st=stamp('CHƯA ĐẦY 200 TUỔI',58);const k=fig(g,{hat:CGOLD});const q=T(g,0,0,'?',150,CRED,12,'middle',OLN);const B=strip('DO MỘT ÔNG VUA NHÀ NGUYỄN ĐẶT',false,36,13);
 bm(AT(1,'chưa',2.0));
 return{upd:t=>{const e=inn(t,R(1)-.2,.5);m.at(330,690,-1,1,e);m.view(108.6,15.9,40+6*inn(t,R(1),E(1)-R(1)));hs(e);m.hi('Hà Nội',inn(t,R(1)+.3,.5));const[x,y]=m.P(...HN);RU(rg,t,90,x,y,inn(t,R(1)+.3,.5));
  sh(A,t,800,470,-3,popv(t,R(1)+.3,.55));const su=popv(t,AT(1,'chưa',2.0),.45);st.at(800,640,-7,su,su>0?1:0);
  k.at(820,1180,.6,Math.sin(t*2)*2,inn(t,AT(1,'vua',3.6),.4));PUT(q,820,920,popv(t,AT(1,'vua',3.6)+.2,.5),1,Math.sin(t*3)*6);sh(B,t,540,1230,1,PV(t,1,'vua',3.6,.1))}}});
// 2 trục thời gian: phần lớn nghìn năm là Thăng Long
S2(2,2,'p',null,g=>{const A=strip('NGHÌN NĂM THĂNG LONG – HÀ NỘI',false,40,21);const X0=110,X1=970,Y=760,f=(1831-1010)/(2026-1010);const XM=X0+(X1-X0)*f;
 const bg=el(g,'rect',{x:X0,y:Y-40,width:X1-X0,height:80,rx:16,fill:'rgba(0,0,0,.12)',stroke:OLN,'stroke-width':5});const b1=el(g,'rect',{x:X0,y:Y-40,width:0,height:80,rx:14,fill:CGOLD,stroke:OLN,'stroke-width':5});const b2=el(g,'rect',{x:XM,y:Y-40,width:0,height:80,rx:14,fill:CRED,stroke:OLN,'stroke-width':5});
 const l1=MLB(g,'THĂNG LONG',44,'#fff'),l2=MLB(g,'HÀ NỘI',34,'#fff');const y1=MLB(g,'1010',36,OLN,'#efe6cf'),y2=MLB(g,'1831',36,OLN,'#efe6cf'),y3=MLB(g,'NAY',32,OLN,'#efe6cf');
 const B=strip('PHẦN LỚN MANG TÊN THĂNG LONG',true,40,22),C=strip('XEN GIỮA CÓ VÀI TÊN KHÁC',false,26,23);const ar=el(g,'path',{d:`M${X0} ${Y-70} Q${(X0+XM)/2} ${Y-150} ${XM} ${Y-70}`,fill:'none',stroke:OLN,'stroke-width':6,'stroke-dasharray':'12 10'});
 return{upd:t=>{sh(A,t,540,470,-1,popv(t,R(2)+.1,.5));const u1=inn(t,AT(2,'nghìn',1.6),1.2),u2=inn(t,AT(2,'Nhưng',4.2),.6);b1.setAttribute('width',(XM-X0)*u1);b2.setAttribute('width',(X1-XM)*u2);
  PUT(l1,(X0+XM)/2,Y+16,popv(t,AT(2,'nghìn',1.6)+1,.5),1,0);PUT(l2,(XM+X1)/2,Y+12,popv(t,AT(2,'Nhưng',4.2)+.4,.5),1,0);PUT(y1,X0+30,Y+96,inn(t,AT(2,'nghìn',1.6),.4),1,0);PUT(y2,XM,Y+96,inn(t,AT(2,'Nhưng',4.2),.4),1,0);PUT(y3,X1-30,Y+96,inn(t,AT(2,'Nhưng',4.2),.4),1,0);
  ar.setAttribute('opacity',inn(t,AT(2,'phần',5.4),.4));sh(B,t,440,560,-2,PV(t,2,'phần',5.4));sh(C,t,540,1010,1,PV(t,2,'phần',5.4,.6))}}});
// 3 Thăng Long = rồng bay lên, rồng là biểu tượng của vua
S2(3,3,'d',null,g=>{const c1=HAN(g,'昇',230),c2=HAN(g,'龍',230);const dr=DRAGON(g);const A=strip('THĂNG = BAY LÊN',false,40,31),B=strip('LONG = RỒNG',true,44,32),C=strip('RỒNG: BIỂU TƯỢNG CỦA NHÀ VUA',false,34,33);const cr=CROWN(g);
 return{upd:t=>{PUT(c1,350,470,popv(t,R(3)+.1,.55),1,-3);PUT(c2,730,470,popv(t,R(3)+.35,.55),1,3);sh(A,t,350,700,-2,PV(t,3,'bay',1.4));sh(B,t,730,700,2,PV(t,3,'rồng',1.8));
  const du=inn(t,AT(3,'rồng',1.8),2.4);PUT(dr,lerp(-200,560,du),lerp(1180,960,du)+Math.sin(t*3)*14,du>0?1:0,1,-8+Math.sin(t*2)*4);PUT(cr,860,860,popv(t,AT(3,'biểu',3.4),.5),1,Math.sin(t*2)*4);sh(C,t,540,1180,-1,PV(t,3,'biểu',3.4))}}});
// 4 nhà Nguyễn đóng đô ở Huế; Thăng Long thành tòa thành cai quản miền Bắc (bản đồ rộng, có Hoàng Sa, Trường Sa)
S2(4,4,'p',null,g=>{const m=vnmap(1000,1090,41);const hs=hsts(m);const pa=el(m.top,'path',{fill:'none',stroke:CRED,'stroke-width':7,'stroke-dasharray':'14 12','stroke-linecap':'round'});const cr=CROWN(m.top);const rh=RINGS(m.top,CRED),rt=RINGS(m.top,CGOLD);
 const A=strip('KINH ĐÔ: HUẾ',true,38,41),B=strip('THĂNG LONG',false,34,42),C=strip('TÒA THÀNH CAI QUẢN MIỀN BẮC',false,28,43);
 return{upd:t=>{const e=inn(t,R(4)-.2,.5);m.at(540,745,0,1,e);m.view(108.4,15.95,62+6*inn(t,R(4),E(4)-R(4)));hs(e);
  const[x0,y0]=m.P(...HN),[x1,y1]=m.P(...HUE);const u=inn(t,AT(4,'chọn',1.4),1.4);const mx=(x0+x1)/2+90,my=(y0+y1)/2;pa.setAttribute('d',`M${x0} ${y0} Q${mx} ${my} ${lerp(x0,x1,u)} ${lerp(y0,y1,u)}`);pa.setAttribute('opacity',u>0?1:0);
  const cx=lerp(lerp(x0,mx,u),lerp(mx,x1,u),u),cy=lerp(lerp(y0,my,u),lerp(my,y1,u),u);PUT(cr,cx,cy-46,inn(t,AT(4,'chọn',1.4)-.2,.3),.6,Math.sin(t*3)*5);
  RU(rt,t,60,x0,y0,e);RU(rh,t,70,x1,y1,inn(t,AT(4,'Huế',2.2),.4));m.hi('Hà Nội',e*(.5+.5*inn(t,AT(4,'Thăng',3.4),.4)));m.hi('Huế',inn(t,AT(4,'Huế',2.2),.5),CRED);
  sh(A,t,540+x1+120,745+y1+70,-2,PV(t,4,'Huế',2.2,.2));sh(B,t,540+x0,745+y0-80,2,inn(t,R(4)+.2,.4)*(1-inn(t,AT(4,'Thăng',3.4),.3)));sh(C,t,540+x0+190,745+y0-80,-1,PV(t,4,'Thăng',3.4))}}});
// 5 năm 1805: đổi chữ Long rồng thành Long thịnh vượng
S2(5,5,'p',t=>'1805',g=>{const bk=el(g,'g',{});el(bk,'rect',{x:-150,y:-110,width:300,height:220,rx:12,fill:'#2f4a6a',stroke:'#fff','stroke-width':7});el(bk,'rect',{x:-150,y:-110,width:30,height:220,fill:'rgba(0,0,0,.3)'});const bt=MLB(bk,'LỊCH SỬ',30,'#f2c14e');bt.setAttribute('y',-20);const bt2=MLB(bk,'THỦ ĐÔ HÀ NỘI',26,'#fff');bt2.setAttribute('y',24);
 const c1=HAN(g,'龍',250,'#f3ead4'),c2=HAN(g,'隆',250);const x1=XX(g),k1=CK(g);const ar=el(g,'path',{d:'M470 760 L600 760 M570 728 L604 760 L570 792',fill:'none',stroke:OLN,'stroke-width':14,'stroke-linecap':'round','stroke-linejoin':'round'});
 const A=strip('LONG = RỒNG',true,40,51),B=strip('LONG = THỊNH VƯỢNG',false,36,52),C=strip('VUA GIA LONG',true,46,53);
 return{upd:t=>{PUT(bk,540,400,popv(t,R(5)+.1,.5),1,-3+Math.sin(t*1.6)*1.5);sh(C,t,540,560,2,PV(t,5,'Gia',2.6));PUT(c1,300,780,popv(t,AT(5,'chữ',3.4),.55),1,-2);PUT(ar,0,0,inn(t,AT(5,'thành',5.4),.3),1,0);PUT(c2,780,780,popv(t,AT(5,'thịnh',6.6),.55),1,2);
  sh(A,t,300,1010,-2,PV(t,5,'rồng',4.4));sh(B,t,780,1010,2,PV(t,5,'thịnh',6.6));PUT(x1,300,770,popv(t,AT(5,'thịnh',6.6)+.3,.4),1.1,0);PUT(k1,860,880,popv(t,AT(5,'thịnh',6.6)+.6,.4),.9,0)}}});
// 6 hài: vua không còn ở đây, con rồng bị cất đi
S2(6,6,'d',null,g=>{const P=strip('THĂNG LONG',true,110,61);const dr=DRAGON(g);const A=strip('VUA KHÔNG CÒN Ở ĐÂY',false,40,62),B=strip('ĐỌC VẪN LÀ THĂNG LONG',false,40,63),C=strip('CHỈ CÓ CON RỒNG BỊ CẤT ĐI',true,44,64);const hk=el(g,'g',{});el(hk,'path',{d:'M0 -900 L0 -40',stroke:'#cfd6dd','stroke-width':8});el(hk,'path',{d:'M0 -40 q0 40 -30 40 q-24 0 -24 -24',fill:'none',stroke:'#cfd6dd','stroke-width':10,'stroke-linecap':'round'});
 const tc=AT(6,'cất',7.0);bm(tc,true);
 return{upd:t=>{sh(P,t,540,760,-2,popv(t,R(6)+.1,.5));const lift=inn(t,tc-.6,1.6);PUT(hk,560,560-lift*900+(1-inn(t,tc-1.2,.6))*-500,inn(t,tc-1.2,.4),1,0);PUT(dr,540,560-lift*900,popv(t,R(6)+.2,.5),.8,Math.sin(t*2)*3+lift*12);
  sh(A,t,540,1000,-1,PV(t,6,'vua',.8)*(1-inn(t,AT(6,'Đọc',4.4)-.1,.3)));sh(B,t,540,1000,1,PV(t,6,'Đọc',4.4));sh(C,t,540,1120,-1,PV(t,6,'con',6.4))}}});
// 7 năm 1831: Minh Mạng lập tỉnh mới, đặt tên tỉnh Hà Nội
S2(7,7,'p',t=>'1831',g=>{const k=fig(g,{hat:CGOLD});const A=strip('VUA MINH MẠNG',true,46,71);const r=rng(71);const tiles=[...Array(6)].map((_,i)=>{const e=el(g,'polygon',{points:jag(150,110,700+i,6),fill:PAL[i%6],stroke:OLN,'stroke-width':5});return{e,x:r()*900+90,y:r()*500+380}});
 const st=stamp('TỈNH HÀ NỘI',96);const B=strip('SẮP XẾP LẠI VÙNG ĐẤT MIỀN BẮC',false,32,72);const ts=AT(7,'Hà',6.6);bm(ts);
 return{upd:t=>{k.at(200,1150,.85,0,inn(t,R(7)+.1,.5));sh(A,t,250,1230,-2,PV(t,7,'Minh',1.4));const u=inn(t,AT(7,'sắp',2.4),1.6);tiles.forEach((o,i)=>{const gx=520+(i%3)*150,gy=640+Math.floor(i/3)*110;o.e.setAttribute('transform',`translate(${lerp(o.x,gx,u)},${lerp(o.y,gy,u)}) rotate(${(1-u)*(i*17-40)})`);o.e.setAttribute('opacity',inn(t,AT(7,'sắp',2.4)-.4,.4))});
  sh(B,t,640,420,1,PV(t,7,'sắp',2.4));const su=popv(t,ts,.4);st.at(670,700,-8,su*1.0,su>0?1:0)}}});
// 8 Đại Nam thực lục: 15 huyện; Thăng Long là nơi đặt bộ máy của tỉnh
S2(8,8,'d',null,g=>{const sc=SCRL(g);const A=strip('ĐẠI NAM THỰC LỤC',true,38,81),A2=strip('BỘ SỬ CỦA TRIỀU NGUYỄN',false,26,82);const num=MLB(g,'0',170,CGOLD);const hl=strip('HUYỆN',false,40,83);const dots=[...Array(15)].map(()=>el(g,'circle',{r:16,fill:CGOLD,stroke:'#fff','stroke-width':4,opacity:0}));const ft=FORT(g);const C=strip('THĂNG LONG: NƠI ĐẶT BỘ MÁY CỦA TỈNH',false,30,84);
 return{upd:t=>{const hide=inn(t,AT(8,'Thăng',5.0)-.2,.4);PUT(sc,280,520,popv(t,R(8)+.1,.5)*(1-hide*.0),1,-3+Math.sin(t*1.5)*1.5);sh(A,t,280,720,-2,PV(t,8,'Đại',.3));sh(A2,t,280,800,1,PV(t,8,'bộ',1.4));
  const t0=AT(8,'mười',3.0);const n=Math.round(15*inn(t,t0,1.0));num.textContent=String(n);PUT(num,780,520,inn(t,t0-.1,.3),1,0);sh(hl,t,780,620,2,inn(t,t0+.3,.3));dots.forEach((d,i)=>{d.setAttribute('cx',680+(i%5)*50);d.setAttribute('cy',700+Math.floor(i/5)*50);d.setAttribute('opacity',t>t0+i*1.0/15?1:0)});
  PUT(ft,540,1080,popv(t,AT(8,'Thăng',5.0),.55),.8,0);sh(C,t,540,1210,-1,PV(t,8,'Thăng',5.0,.2))}}});
// 9 TÁCH CHỮ: 河 = sông, 內 = bên trong -> đất phía trong sông
S2(9,9,'d',null,g=>{const c1=HAN(g,'河',260),c2=HAN(g,'內',260);const q=T(g,0,0,'?',120,CRED,10,'middle',OLN);const wv=[0,1,2].map(i=>el(g,'path',{fill:'none',stroke:RIV,'stroke-width':9-i*2,'stroke-linecap':'round'}));const bx=el(g,'rect',{x:-80,y:-60,width:160,height:120,rx:10,fill:'none',stroke:'#fff','stroke-width':7,'stroke-dasharray':'14 10'});const dt=el(g,'circle',{r:18,fill:CGOLD,stroke:'#fff','stroke-width':4});
 const A=strip('HÀ = SÔNG',false,44,91),B=strip('NỘI = BÊN TRONG',false,40,92),C=strip('ĐẤT PHÍA TRONG SÔNG',true,58,93);const tc=AT(9,'vùng',4.0);bm(tc);
 return{upd:t=>{const ms=inn(t,tc-.2,.6);PUT(c1,lerp(300,380,ms),520,popv(t,R(9)+.1,.55),1,-2);PUT(c2,lerp(780,700,ms),520,popv(t,R(9)+.3,.55),1,2);PUT(q,540,330,popv(t,R(9)+.2,.5)*(1-inn(t,AT(9,'sông',1.8),.3)),1,Math.sin(t*3)*6);
  const wu=inn(t,AT(9,'sông',1.8),.5);wv.forEach((e,i)=>{let d='';for(let x=170;x<=430;x+=12)d+=(x==170?'M':'L')+x+' '+(780+i*26+Math.sin(x*.05+t*4+i)*9).toFixed(1);e.setAttribute('d',d);e.setAttribute('opacity',wu*(1-ms))});
  PUT(bx,780,800,inn(t,AT(9,'bên',2.6),.4)*(1-ms),1,0);PUT(dt,780,800,popv(t,AT(9,'bên',2.6)+.2,.4)*(1-ms),1,0);sh(A,t,300,940,-2,PV(t,9,'sông',1.8)*(1-ms));sh(B,t,780,940,2,PV(t,9,'bên',2.6)*(1-ms));sh(C,t,540,880,-1,popv(t,tc,.5))}}});
// 10-12 bản đồ gần: sông Hồng, sông Đáy, tên cả một tỉnh, Kim Bảng và Duy Tiên nằm ngoài Hà Nội ngày nay
S2(10,12,'p',null,g=>{const m=vnmap(980,1010,101);const fH=m.line(SHONG,RIV,7),fD=m.line(SDAY,RIV,6);const rt=RINGS(m.top,CGOLD),rk=RINGS(m.top,CRED,2),rd=RINGS(m.top,CRED,2);
 const LH=strip('SÔNG HỒNG · PHÍA ĐÔNG',false,28,101),LD=strip('SÔNG ĐÁY · PHÍA TÂY',false,28,102),TL=MLB(m.top,'THĂNG LONG',30,'#fff'),BIG=strip('TỈNH HÀ NỘI NĂM 1831',true,40,103),PH=strip('THĂNG LONG CHỈ LÀ MỘT PHẦN',false,30,104);
 const pk=el(m.top,'circle',{r:13,fill:CRED,stroke:'#fff','stroke-width':4}),pd=el(m.top,'circle',{r:13,fill:CRED,stroke:'#fff','stroke-width':4}),pt=el(m.top,'circle',{r:14,fill:CGOLD,stroke:'#fff','stroke-width':4});const LK=MLB(m.top,'KIM BẢNG',28,'#fff'),LDT=MLB(m.top,'DUY TIÊN',28,'#fff');
 const NOW=strip('RANH GIỚI HÀ NỘI NGÀY NAY',false,24,105),NT=strip('VỊ TRÍ SÔNG VÀ ĐỊA DANH GẦN ĐÚNG',false,20,106),J1=strip('NGƯỜI KIM BẢNG',true,40,107),J2=strip('CŨNG LÀ NGƯỜI HÀ NỘI (1831)',false,34,108);const ck=CK(g);
 const tj=AT(12,'Tính',5.0);bm(tj,true);
 return{upd:t=>{const e=inn(t,R(10)-.2,.5);m.at(540,710,0,1,e);const zz=inn(t,R(12)-.3,1.2);m.view(lerp(105.72,105.8,zz),lerp(20.95,20.85,zz),lerp(720,780,inn(t,R(10),E(12)-R(10))));
  m.hi('Hà Nội',e*.7,CGOLD);fH(inn(t,AT(10,'Hồng',2.4),1.4));fD(inn(t,AT(10,'Đáy',4.2),1.2));
  const[hx,hy]=m.P(...HN);pt.setAttribute('cx',hx);pt.setAttribute('cy',hy);RU(rt,t,50,hx,hy,e);TL.setAttribute('x',hx);TL.setAttribute('y',hy-30);
  sh(LH,t,770,500,-2,PV(t,10,'Hồng',2.4));sh(LD,t,300,560,2,PV(t,10,'Đáy',4.2));sh(NOW,t,300,1170,0,inn(t,R(10)+.4,.4));
  sh(BIG,t,560,330,-1,PV(t,11,'tỉnh',1.2)*(1-inn(t,R(12)+.2,.3)));sh(PH,t,560,420,1,PV(t,11,'phần',4.6)*(1-inn(t,R(12)+.2,.3)));const sk=1-.35*inn(t,AT(11,'phần',4.6),.5);pt.setAttribute('r',14*sk);
  const[kx,ky]=m.P(...KB),[dx,dy]=m.P(...DT);const uk=popv(t,AT(12,'Kim',2.6),.4),ud=popv(t,AT(12,'Duy',1.9),.4);pk.setAttribute('cx',kx);pk.setAttribute('cy',ky);pk.setAttribute('opacity',uk>0?1:0);pd.setAttribute('cx',dx);pd.setAttribute('cy',dy);pd.setAttribute('opacity',ud>0?1:0);
  RU(rk,t,40,kx,ky,uk>0?1:0);RU(rd,t,40,dx,dy,ud>0?1:0);LK.setAttribute('x',kx-70);LK.setAttribute('y',ky+48);LK.setAttribute('opacity',uk>0?1:0);LDT.setAttribute('x',dx+70);LDT.setAttribute('y',dy+48);LDT.setAttribute('opacity',ud>0?1:0);
  sh(J1,t,540,300,-2,popv(t,tj,.5));sh(J2,t,540,385,1,popv(t,tj+.25,.5));PUT(ck,880,330,popv(t,tj+.5,.4),.8,0);sh(NT,t,700,1170,0,inn(t,R(12),.4))}}});
// 13 năm 1946: Hiến pháp đầu tiên, "Thủ đô đặt ở Hà Nội" (văn bản vẽ minh họa)
S2(13,13,'p',t=>'1946',g=>{const dc=el(g,'g',{});el(dc,'rect',{x:-300,y:-380,width:600,height:760,rx:10,fill:'#fbf6e8',stroke:OLN,'stroke-width':7});const h1=MLB(dc,'HIẾN PHÁP',58,CRED,'#fbf6e8');h1.setAttribute('y',-280);const h2=MLB(dc,'NĂM 1946',38,OLN,'#fbf6e8');h2.setAttribute('y',-220);
 for(let i=0;i<9;i++)if(i!=5)el(dc,'rect',{x:-240,y:-160+i*52,width:480-(i%3)*70,height:14,rx:7,fill:'rgba(40,30,20,.25)'});const hlr=el(dc,'rect',{x:-260,y:-160+5*52-34,width:0,height:62,rx:10,fill:CGOLD});const ht=MLB(dc,'THỦ ĐÔ ĐẶT Ở HÀ NỘI',36,OLN,CGOLD);ht.setAttribute('y',-160+5*52+12);
 const mh=strip('HÌNH MINH HỌA',false,20,131),A=strip('BẢN HIẾN PHÁP ĐẦU TIÊN',true,40,132);const ck=CK(g);const tq=AT(13,'Thủ',5.0);bm(tq);
 return{upd:t=>{PUT(dc,540,720,popv(t,R(13)+.1,.55),1,-2+Math.sin(t*1.4)*1);sh(A,t,540,240+70,2,PV(t,13,'Hiến',1.6));const u=inn(t,tq,.6);hlr.setAttribute('width',520*u);ht.setAttribute('opacity',u);PUT(ck,800,960,popv(t,tq+.5,.4),1,0);sh(mh,t,540,1140,0,inn(t,R(13)+.4,.4))}}});
// 14 tên một tỉnh thành tên thủ đô, gọi đến hôm nay (bản đồ cả nước, có Hoàng Sa, Trường Sa)
S2(14,14,'d',null,g=>{const m=vnmap(600,880,141);const hs=hsts(m);const rg=RINGS(m.top,CGOLD);const st=el(m.top,'path',{d:'M0 -26 L7 -8 L26 -8 L11 4 L17 23 L0 12 L-17 23 L-11 4 L-26 -8 L-7 -8Z',fill:'#ffd34d',stroke:OLN,'stroke-width':3});
 const A=strip('TÊN MỘT TỈNH',false,40,141),Y=strip('1831',false,34,142),B=strip('TÊN THỦ ĐÔ',true,52,143),C=strip('ĐẾN TẬN HÔM NAY',false,34,144);const ar=el(g,'path',{d:'M840 560 L840 660 M806 630 L840 664 L874 630',fill:'none',stroke:'#fff','stroke-width':12,'stroke-linecap':'round','stroke-linejoin':'round'});
 return{upd:t=>{const e=inn(t,R(14)-.2,.5);m.at(330,700,-1,1,e);m.view(108.6,15.9,44);hs(e);m.hi('Hà Nội',e);const[x,y]=m.P(...HN);RU(rg,t,80,x,y,e);PUT(st,x,y,popv(t,AT(14,'thủ',4.0),.5),1.2,t*30);
  sh(A,t,840,440,-2,PV(t,14,'tỉnh',2.4));sh(Y,t,840,510,2,PV(t,14,'tỉnh',2.4,.2));PUT(ar,0,0,inn(t,AT(14,'thủ',4.0)-.2,.3),1,0);sh(B,t,840,740,-2,PV(t,14,'thủ',4.0));sh(C,t,840,830,1,PV(t,14,'hôm',5.6))}}});
// 15 câu hỏi: Thăng Long hay Hà Nội
S2(15,15,'d',null,g=>{const A=strip('THĂNG LONG',false,84,151),B=strip('HÀ NỘI',true,96,152),q=T(g,0,0,'?',260,CGOLD,14,'middle',OLN);const C=strip('BẠN CHỌN TÊN NÀO?',true,52,153);const dr=DRAGON(g);bm(R(15)+.2);
 return{upd:t=>{sh(A,t,330,560+Math.sin(t*2)*8,-5,popv(t,R(15)+.1,.5));sh(B,t,750,800+Math.sin(t*2+1)*8,4,popv(t,AT(15,'Hà',1.0),.5));PUT(q,560,420,popv(t,AT(15,'nếu',1.6),.5),1,Math.sin(t*2.4)*8);PUT(dr,330,410,popv(t,R(15)+.3,.5),.55,Math.sin(t*2)*4);sh(C,t,540,1080,-1,PV(t,15,'bạn',2.6))}}});
