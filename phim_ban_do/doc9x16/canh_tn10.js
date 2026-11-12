// ===== TÊN TỈNH THÀNH #10: Khánh Hòa (tn10). Bản đồ hành chính phẳng 34 tỉnh (geoBoundaries, phạm vi công cộng), không vẽ nước láng giềng.
// Phạm vi dinh Thái Khang không có ranh giới tin cậy: chỉ vẽ một dải dọc bờ biển từ sông Phan Rang tới giáp Phú Yên, không vẽ ranh giới cũ. Phú Khánh 1976–1989 = Phú Yên + Khánh Hòa (ranh giới tỉnh trước 2025, nét đứt).
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
// ===== Dấu ấn riêng (Khánh Hòa): nền tối xanh đại dương, giấy cát nhạt; tháp Chăm, hàng dừa và thuyền thúng mờ ở đáy, sóng biển chảy (y>1640)
{DR1.setAttribute('opacity',0);DR2.setAttribute('opacity',0);
 DARKG.firstChild.setAttribute('fill','#0c1b2e');
 [...PAPG.children].forEach(c=>{if(c.tagName=='g')c.setAttribute('opacity',0);if(c.tagName=='line')c.setAttribute('stroke','rgba(0,0,0,0)')});
 PAPG.firstChild.setAttribute('fill','#f0e6d0');
 const dots=(p,col)=>{const g=el(p,'g',{});const r=rng(1010);for(let i=0;i<80;i++)el(g,'circle',{cx:r()*1080,cy:200+r()*1300,r:1.5+r()*2.5,fill:col});return g};
 dots(DARKG,'rgba(150,190,240,.06)');dots(PAPG,'rgba(120,90,50,.10)');
 const sky=(p,col)=>{const g=el(p,'g',{});const L=(d,w=5)=>el(g,'path',{d,fill:'none',stroke:col,'stroke-width':w,'stroke-linejoin':'round','stroke-linecap':'round'});
  // tháp Chăm nhiều tầng
  L('M820 1640 L820 1500 L800 1500 L800 1460 L840 1440 L840 1400 L870 1370 L900 1400 L900 1440 L940 1460 L940 1500 L920 1500 L920 1640',5);L('M855 1640 L855 1580 Q870 1560 885 1580 L885 1640',4);
  // hàng dừa
  for(const[x,h]of[[120,190],[220,150],[1000,170]]){L(`M${x} 1640 Q${x+16} ${1640-h*.5} ${x+6} ${1640-h}`,5);for(const a of[-2.4,-1.9,-1.2,-.7,-.2])L(`M${x+6} ${1640-h} q${Math.cos(a)*70} ${Math.sin(a)*40+30} ${Math.cos(a)*100} ${Math.sin(a)*20+60}`,4)}
  // thuyền thúng
  for(const[x,s]of[[450,1],[580,.75]]){L(`M${x-50*s} 1618 Q${x} ${1660} ${x+50*s} 1618 Z`,5);L(`M${x-50*s} 1618 L${x+50*s} 1618`,3)}
  return g};
 const skA=sky(DARKG,'rgba(130,180,240,.15)'),skB=sky(PAPG,'rgba(110,80,40,.18)');
 const wv=(p,col)=>[0,1,2].map(i=>el(p,'path',{fill:'none',stroke:col,'stroke-width':4+i,opacity:.6-i*.12}));
 const wA=wv(DARKG,'rgba(110,170,230,.35)'),wB=wv(PAPG,'rgba(60,100,140,.30)');
 window.THEME_UPD=t=>{const dx=Math.sin(t*.1)*14;skA.setAttribute('transform',`translate(${dx.toFixed(1)},0)`);skB.setAttribute('transform',`translate(${dx.toFixed(1)},0)`);[wA,wB].forEach(L=>L.forEach((e,i)=>{const y0=1690+i*62;let d='';for(let x=-20;x<=1100;x+=28){const y=y0+Math.sin(x*.012+t*(1.0+i*.3)+i)*9;d+=(x<0?'M':'L')+x+' '+y.toFixed(1)}e.setAttribute('d',d)}))};
}

// ===== CẢNH
// thẻ chữ có viền (dùng cho trò ghép chữ)
const TILE=(g,txt,col=CGOLD,w=300,fg=OLN)=>{const k=el(g,'g',{});el(k,'rect',{x:-w/2,y:-62,width:w,height:124,rx:18,fill:col,stroke:'#fff','stroke-width':8});const t=T(k,0,30,txt,78,fg,0,'middle');t.setAttribute('font-weight',900);return k};
// chấm thị xã + nhãn trên bản đồ
const PIN=(m,txt,col=CRED,dy=-26,dx=0)=>{const k=el(m.top,'g',{});el(k,'circle',{r:13,fill:col,stroke:'#fff','stroke-width':5});const t=MLB(k,txt,30,'#fff');t.setAttribute('y',dy);t.setAttribute('x',dx);return k};
const PINAT=(m,k,p,u)=>{const[x,y]=m.P(...p);k.setAttribute('transform',`translate(${x},${y}) scale(${Math.max(.001,u)})`);k.setAttribute('opacity',u>0?1:0)};
const KH=[109.05,12.1],NT=[109.19,12.24],PR=[108.99,11.57],DC=[109.40,12.86],TSA=[114.3,10.4];
const COAST=[[108.99,11.57],[109.12,11.72],[109.2,11.88],[109.18,12.05],[109.21,12.24],[109.24,12.45],[109.3,12.62],[109.36,12.76],[109.40,12.86]];
const SEAH=()=>[strip('QĐ. HOÀNG SA (VIỆT NAM) ↗',false,22,901),strip('QĐ. TRƯỜNG SA (VIỆT NAM) →',false,22,902),strip('RANH GIỚI HIỆN NAY',false,20,903)];
const seaH=(L,t,e,lab=true)=>{sh(L[0],t,820,1180,0,e);sh(L[1],t,820,1235,0,e);sh(L[2],t,250,1235,0,e*(lab?1:0))};
const OLD=(m,names,fill='none')=>names.map(n=>{const p=TINH63.find(q=>q.n==n);return el(m.riv,'path',{d:p.p.map(rpath).join(''),fill,stroke:'#fff8e6','stroke-width':3,'stroke-dasharray':'10 8','vector-effect':'non-scaling-stroke',opacity:0})});
const MLINE=(m,pts,col=CGOLD,wd=10)=>{const d='M'+pts.map(p=>p[0]+' '+(-p[1]*KYP).toFixed(3)).join('L');const e=el(m.riv,'path',{d,fill:'none',stroke:col,'stroke-width':wd,'vector-effect':'non-scaling-stroke','stroke-linecap':'round','stroke-linejoin':'round',pathLength:1,'stroke-dasharray':'1 1','stroke-dashoffset':1});return u=>{e.setAttribute('stroke-dashoffset',1-cl(u));e.setAttribute('opacity',u>0?1:0)}};
const LBL=(m,txt,sz=30,col='#fff',bg=OLN)=>MLB(m.top,txt,sz,col,bg);
const LAT=(m,e,p,u,dy=0)=>{const[x,y]=m.P(...p);e.setAttribute('x',x);e.setAttribute('y',y+dy);e.setAttribute('opacity',u)};
const GIFT=(g)=>{const k=el(g,'g',{});el(k,'rect',{x:-140,y:-60,width:280,height:200,rx:12,fill:CRED,stroke:'#fff','stroke-width':8});el(k,'rect',{x:-160,y:-110,width:320,height:60,rx:10,fill:'#e5483f',stroke:'#fff','stroke-width':8});el(k,'rect',{x:-22,y:-110,width:44,height:250,fill:CGOLD,stroke:'#fff','stroke-width':5});el(k,'path',{d:'M0 -110 C-90 -200 -140 -120 0 -110 C140 -120 90 -200 0 -110',fill:CGOLD,stroke:'#fff','stroke-width':6});return k};
// chuỗi tên: 4 thẻ xếp dọc, thẻ cũ mờ dần (cảnh 5–7 dùng chung)
const NAMES=['THÁI KHANG','BÌNH KHANG','BÌNH HÒA','KHÁNH HÒA'];
const CHAIN=(g)=>NAMES.map((n,i)=>{const k=TILE(g,n,i==3?CGOLD:'#cdd6e0',560);k.setAttribute('opacity',0);return k});
const CNT=(g)=>{const k=el(g,'g',{});el(k,'circle',{r:62,fill:CRED,stroke:'#fff','stroke-width':7});const t=T(k,0,24,'1',70,'#fff',0,'middle');t.setAttribute('font-weight',900);return{k,t}};
// 1 hook: trước khi tên là Khánh Hòa, vùng đất mang ba tên khác
S2(1,1,'d',null,g=>{const m=vnmap(560,820,101);const hs=hsts(m);const rg=RINGS(m.top,CGOLD);const A=strip('KHÁNH HÒA',true,62,11);const q=[0,1,2].map(i=>TILE(g,'?','#cdd6e0',150));const B=strip('3 CÁI TÊN KHÁC',true,44,12);const tb=AT(1,'ba',5.2);bm(tb);
 return{upd:t=>{const e=inn(t,R(1)-.2,.5);m.at(300,720,-1,1,e);m.view(110.2,14.6,40+4*inn(t,R(1),E(1)-R(1)));hs(e);m.hi('Khánh Hòa',inn(t,AT(1,'Khánh',3.0),.5),CGOLD);const[x,y]=m.P(...KH);RU(rg,t,90,x,y,inn(t,AT(1,'Khánh',3.0),.4));
  sh(A,t,800,380,-3,PV(t,1,'Khánh',3.0));q.forEach((o,i)=>PUT(o,800,540+i*170,popv(t,tb-.1+i*.2,.45),.85,(i-1)*4+Math.sin(t*2+i)*2));sh(B,t,800,1080,2,popv(t,tb,.5))}}});
// 2 cái tên cuối cùng không phải ngẫu nhiên, nó là một lời chúc
S2(2,2,'p',null,g=>{const w=TILE(g,'KHÁNH HÒA',CGOLD,560);const gf=GIFT(g);const A=strip('KHÔNG NGẪU NHIÊN',false,40,21),B=strip('MỘT LỜI CHÚC',true,56,22);const tc=AT(2,'chúc',5.0);bm(tc);
 return{upd:t=>{PUT(w,540,520,popv(t,R(2)+.05,.5),1,Math.sin(t*1.4)*2);sh(A,t,540,680,-2,PV(t,2,'ngẫu',3.0));PUT(gf,540,920,popv(t,tc-.4,.55),.9,Math.sin(t*2)*3);sh(B,t,540,1170,1,popv(t,tc,.5))}}});
// 3 năm 1653 (gần 400 năm trước), chúa Nguyễn Phúc Tần lập dinh Thái Khang
S2(3,3,'d',t=>t<AT(3,'chúa',2.6)-.4?null:'1653',g=>{const m=vnmap(960,880,103);const lab=LBL(m,'DINH THÁI KHANG',40,OLN,CGOLD);const cs=MLINE(m,COAST,CGOLD,12);const A=strip('GẦN 400 NĂM TRƯỚC',false,38,31),B=strip('CHÚA NGUYỄN PHÚC TẦN',true,42,32);const C=strip('VỊ TRÍ ƯỚC LƯỢNG',false,20,33);const SH=SEAH();const td=AT(3,'Thái',5.0);bm(td);
 return{upd:t=>{const e=inn(t,R(3)-.2,.5);m.at(540,760,0,1,e);m.view(109.1,12.2,lerp(260,290,inn(t,R(3),E(3)-R(3))));seaH(SH,t,e);cs(inn(t,td-.2,1.0));LAT(m,lab,[108.75,12.3],inn(t,td,.4));
  sh(A,t,540,400,-2,popv(t,R(3)+.05,.5));sh(B,t,540,480,1,PV(t,3,'chúa',2.6));sh(C,t,850,330,0,inn(t,td,.4))}}});
// 4 vùng đất kéo dài từ sông Phan Rang ra đến giáp Phú Yên ngày nay
S2(4,4,'p',null,g=>{const m=vnmap(960,880,104);const cs=MLINE(m,COAST,CGOLD,14);const lp=LBL(m,'SÔNG PHAN RANG',30),ly=LBL(m,'GIÁP PHÚ YÊN',30);const rg1=RINGS(m.top,CRED),rg2=RINGS(m.top,CRED);const A=strip('KÉO DÀI',false,40,41),B=strip('PHAN RANG → PHÚ YÊN',true,44,42);const SH=SEAH();const tp=AT(4,'Phan',3.4),ty=AT(4,'Phú',4.6);bm(ty,true);
 return{upd:t=>{const e=inn(t,R(4)-.2,.5);m.at(540,760,0,1,e);m.view(109.15,12.2,lerp(300,330,inn(t,R(4),E(4)-R(4))));seaH(SH,t,e);cs(.001+inn(t,tp,ty-tp+.6)*.999);const[x1,y1]=m.P(...PR),[x2,y2]=m.P(...DC);RU(rg1,t,70,x1,y1,inn(t,tp,.4));RU(rg2,t,70,x2,y2,inn(t,ty,.4));
  LAT(m,lp,[108.6,11.5],inn(t,tp,.4));LAT(m,ly,[109.0,12.95],inn(t,ty,.4));sh(A,t,540,400,-2,popv(t,R(4)+.05,.5));sh(B,t,540,480,1,popv(t,ty,.5))}}});
// 5 năm 1690: Thái Khang đổi thành Bình Khang
S2(5,5,'d',t=>'1690',g=>{const C=CHAIN(g);const c=CNT(g);const ar=arrow(g,540,700,540,860);const A=strip('TÊN THỨ HAI',false,34,51);const tn=AT(5,'Bình',4.0);bm(tn);
 return{upd:t=>{PUT(C[0],540,600,popv(t,R(5)+.05,.5),.85,Math.sin(t*1.5)*2);ar.set(inn(t,tn-.5,.4));PUT(C[1],540,960,popv(t,tn,.5),1,Math.sin(t*1.5+1)*2);PUT(c.k,860,1110,popv(t,tn+.2,.4),.8,0);c.t.textContent='2';sh(A,t,540,1250,0,popv(t,tn+.2,.5))}}});
// 6 năm 1803, vua Gia Long: Bình Khang đổi thành Bình Hòa
S2(6,6,'p',t=>'1803',g=>{const C=CHAIN(g);const c=CNT(g);const ar=arrow(g,540,700,540,860);const A=strip('VUA GIA LONG',true,42,61),B=strip('TÊN THỨ BA',false,34,62);const tn=AT(6,'Hòa',7.0);bm(tn);
 return{upd:t=>{sh(A,t,540,400,-2,PV(t,6,'Gia',3.0));PUT(C[1],540,600,popv(t,R(6)+.05,.5),.85,Math.sin(t*1.5)*2);ar.set(inn(t,tn-.5,.4));PUT(C[2],540,960,popv(t,tn,.5),1,Math.sin(t*1.5+1)*2);PUT(c.k,860,1110,popv(t,tn+.2,.4),.8,0);c.t.textContent='3';sh(B,t,540,1250,0,popv(t,tn+.2,.5))}}});
// 7 năm 1832, vua Minh Mạng: đổi thành tỉnh Khánh Hòa
S2(7,7,'d',t=>'1832',g=>{const C=CHAIN(g);const ar=arrow(g,540,700,540,860);const A=strip('VUA MINH MẠNG',true,42,71),B=strip('TỈNH KHÁNH HÒA',true,50,72);const ck=CK(g);const tn=AT(7,'Khánh',6.6);bm(tn);
 return{upd:t=>{sh(A,t,540,400,-2,PV(t,7,'Minh',3.2));PUT(C[2],540,600,popv(t,R(7)+.05,.5),.85,Math.sin(t*1.5)*2);ar.set(inn(t,tn-.5,.4));PUT(C[3],540,960,popv(t,tn,.5),1.05,Math.sin(t*1.5+1)*2);PUT(ck,880,1080,popv(t,tn+.3,.4),.6,0);sh(B,t,540,1200,1,popv(t,tn+.2,.5))}}});
// 8 chữ Khánh là vui mừng, chữ Hòa là hòa thuận: mong vùng đất luôn yên vui (慶和)
S2(8,8,'p',null,g=>{const sc=SCRL(g,600,360);const h1=HAN(g,'慶',150,CRED),h2=HAN(g,'和',150,'#2a6fb0');const A=strip('KHÁNH = VUI MỪNG',true,40,81),B=strip('HÒA = HÒA THUẬN',true,40,82),C=strip('MONG LUÔN YÊN VUI',false,40,83);const ty=AT(8,'yên',7.0);bm(ty);
 return{upd:t=>{const u=popv(t,R(8)+.05,.55);PUT(sc,540,640,u,1,-2+Math.sin(t*1.4));PUT(h1,410,640,u*(1+.08*inn(t,AT(8,'Khánh',.4),.3)*(1-inn(t,AT(8,'Hòa',2.2),.3))),1,0);PUT(h2,670,640,u*(1+.08*inn(t,AT(8,'Hòa',2.2),.3)),1,0);
  sh(A,t,540,920,-2,PV(t,8,'vui',1.2));sh(B,t,540,1010,2,PV(t,8,'thuận',3.0));sh(C,t,540,1140,-1,popv(t,ty,.5))}}});
// 9 cái tên giữ đến tận bây giờ, gần 200 năm
S2(9,9,'d',null,g=>{const cal=el(g,'g',{});el(cal,'rect',{x:-200,y:-200,width:400,height:400,rx:24,fill:'#fff',stroke:OLN,'stroke-width':8});el(cal,'rect',{x:-200,y:-200,width:400,height:100,rx:24,fill:CRED,stroke:OLN,'stroke-width':8});for(const x of[-110,110])el(cal,'rect',{x:x-12,y:-236,width:24,height:70,rx:10,fill:'#9aa3ab',stroke:OLN,'stroke-width':5});const num=T(cal,0,100,'~200',140,OLN,0,'middle');num.setAttribute('font-weight',900);const yr=MLB(cal,'NĂM',40,'#fff',CRED);yr.setAttribute('y',-136);
 const A=strip('GIỮ ĐẾN BÂY GIỜ',true,48,91),B=strip('1832 → NAY',false,38,92);const th=AT(9,'hai',4.4);bm(th);
 return{upd:t=>{sh(A,t,540,380,-2,popv(t,R(9)+.05,.5));PUT(cal,540,760,popv(t,R(9)+.3,.55),1,-3+Math.sin(t*1.5)*2);num.setAttribute('transform',`scale(${1+.12*popv(t,th,.5)*(1-inn(t,th+.5,.4))})`);sh(B,t,540,1110,1,popv(t,th,.5))}}});
// 10 Khánh Hòa có phần lãnh thổ rất xa ngoài biển: quần đảo Trường Sa
S2(10,10,'p',null,g=>{const m=vnmap(960,880,110);const hs=hsts(m);const rg=RINGS(m.top,CGOLD);const ar=el(m.top,'path',{fill:'none',stroke:'#fff','stroke-width':6,'stroke-dasharray':'14 10','stroke-linecap':'round'});const A=strip('RẤT XA NGOÀI BIỂN',false,38,101),B=strip('QUẦN ĐẢO TRƯỜNG SA',true,46,102);const H=strip('RANH GIỚI HIỆN NAY',false,20,103),HS=strip('QĐ. HOÀNG SA (VIỆT NAM) ↑',false,22,104);const tt=AT(10,'Trường',6.0);bm(tt);
 return{upd:t=>{const e=inn(t,R(10)-.2,.5);m.at(540,760,0,1,e);m.view(lerp(109.4,111.6,inn(t,AT(10,'xa',3.0)-.3,1.2)),lerp(12.2,11.4,inn(t,AT(10,'xa',3.0)-.3,1.2)),lerp(260,115,inn(t,AT(10,'xa',3.0)-.3,1.2)));hs(e);m.hi('Khánh Hòa',e,CGOLD);sh(H,t,250,1235,0,e);sh(HS,t,820,1235,0,e*inn(t,AT(10,'xa',3.0),.6));
  const[x1,y1]=m.P(109.3,12.1),[x2,y2]=m.P(...TSA);const u=inn(t,tt-.4,.8);ar.setAttribute('d',`M${x1} ${y1} L${lerp(x1,x2,u)} ${lerp(y1,y2,u)}`);ar.setAttribute('opacity',u>0?1:0);RU(rg,t,90,x2,y2,inn(t,tt,.4));
  sh(A,t,540,400,-2,PV(t,10,'xa',3.0));sh(B,t,540,1110,1,popv(t,tt,.5))}}});
// 11 năm 1982: huyện đảo Trường Sa nhập vào tỉnh Phú Khánh (Phú Yên + Khánh Hòa thời đó; ranh giới tỉnh trước 2025, nét đứt)
S2(11,11,'d',t=>'1982',g=>{const m=vnmap(960,880,111);const hs=hsts(m);const old=OLD(m,['Phú Yên','Khánh Hòa'],'rgba(242,193,78,.45)');const lab=LBL(m,'TỈNH PHÚ KHÁNH',34,OLN,CGOLD);const rg=RINGS(m.top,CGOLD);const ar=el(m.top,'path',{fill:'none',stroke:'#fff','stroke-width':6,'stroke-dasharray':'14 10','stroke-linecap':'round'});
 const A=strip('PHÚ YÊN + KHÁNH HÒA',false,36,111),B=strip('TRƯỜNG SA → PHÚ KHÁNH',true,40,112),H=strip('RANH GIỚI TỈNH TRƯỚC NĂM 2025',false,20,113),HS=strip('QĐ. HOÀNG SA (VIỆT NAM) ↑',false,22,114);const tp=AT(11,'Phú',5.4);bm(AT(11,'nhập',3.8));
 return{upd:t=>{const e=inn(t,R(11)-.2,.5);m.at(540,760,0,1,e);m.view(111.4,11.9,lerp(110,120,inn(t,R(11),E(11)-R(11))));hs(e);sh(H,t,250,1235,0,e);sh(HS,t,820,1235,0,e);old.forEach(o=>o.setAttribute('opacity',inn(t,tp-.3,.5)));LAT(m,lab,[110.2,13.3],inn(t,tp,.4));
  const[x1,y1]=m.P(...TSA),[x2,y2]=m.P(109.4,12.4);const u=inn(t,AT(11,'nhập',3.8)-.2,1.0);ar.setAttribute('d',`M${x1} ${y1} L${lerp(x1,x2,u)} ${lerp(y1,y2,u)}`);ar.setAttribute('opacity',u>0?1:0);RU(rg,t,80,x1,y1,inn(t,AT(11,'Trường',2.0),.4));
  sh(A,t,540,400,-2,PV(t,11,'chung',8.0,-.4));sh(B,t,540,1110,1,PV(t,11,'nhập',3.8))}}});
// 12 năm 1989: Phú Khánh tách đôi, Trường Sa thuộc tỉnh Khánh Hòa
S2(12,12,'p',t=>'1989',g=>{const m=vnmap(960,880,112);const hs=hsts(m);const old=OLD(m,['Phú Yên','Khánh Hòa']);const L=[['PHÚ YÊN',108.9,13.15],['KHÁNH HÒA',108.85,12.3]].map(([n,lo,la])=>({e:LBL(m,n,30),lo,la}));const rg=RINGS(m.top,CGOLD);const ar=el(m.top,'path',{fill:'none',stroke:CGOLD,'stroke-width':7,'stroke-linecap':'round'});
 const A=strip('TÁCH ĐÔI',true,48,121),B=strip('TRƯỜNG SA THUỘC KHÁNH HÒA',true,38,122),H=strip('RANH GIỚI TỈNH TRƯỚC NĂM 2025',false,20,123),HS=strip('QĐ. HOÀNG SA (VIỆT NAM) ↑',false,22,124);const tk=AT(12,'Khánh',6.0);bm(AT(12,'tách',3.6));
 return{upd:t=>{const e=inn(t,R(12)-.2,.5);m.at(540,760,0,1,e);m.view(111.4,11.9,lerp(118,132,inn(t,R(12),E(12)-R(12))));hs(e);sh(H,t,250,1235,0,e);const sp=inn(t,AT(12,'tách',3.6),.6);old.forEach((o,i)=>{o.setAttribute('opacity',e);o.setAttribute('fill',i==1&&inn(t,tk,.4)>0?'rgba(242,193,78,.6)':'rgba(255,255,255,.06)');o.setAttribute('transform',`translate(0,${(i?1:-1)*sp*.12})`)});
  L.forEach((o,i)=>LAT(m,o.e,[o.lo,o.la+(i?-1:1)*sp*.12],inn(t,AT(12,'tách',3.6)+i*.3,.4)));const[x1,y1]=m.P(...TSA),[x2,y2]=m.P(109.4,12.1);const u=inn(t,tk-.3,.8);ar.setAttribute('d',`M${x1} ${y1} L${lerp(x1,x2,u)} ${lerp(y1,y2,u)}`);ar.setAttribute('opacity',u>0?1:0);RU(rg,t,80,x1,y1,inn(t,tk,.4));
  sh(A,t,540,400,-2,PV(t,12,'tách',3.6));sh(B,t,540,1110,1,popv(t,tk,.5))}}});
// 13 năm 2025: Ninh Thuận nhập vào Khánh Hòa, tên chung vẫn là Khánh Hòa
S2(13,13,'d',t=>'2025',g=>{const m=vnmap(960,880,113);const old=OLD(m,['Khánh Hòa','Ninh Thuận']);const L=[['NINH THUẬN',108.75,11.65]].map(([n,lo,la])=>({e:LBL(m,n,30),lo,la}));const A=strip('VẪN LÀ KHÁNH HÒA',true,48,131);const SH=SEAH();const tv=AT(13,'vẫn',7.0);bm(tv);
 return{upd:t=>{const e=inn(t,R(13)-.2,.5);m.at(540,760,0,1,e);m.view(108.95,12.0,lerp(260,240,inn(t,R(13),E(13)-R(13))));seaH(SH,t,e);old.forEach((o,i)=>o.setAttribute('opacity',e*(i==0?1:inn(t,AT(13,'Ninh',4.0)-.2,.4))));
  L.forEach(o=>LAT(m,o.e,[o.lo,o.la],inn(t,AT(13,'Ninh',4.0)-.2,.4)*(1-inn(t,tv,.4))));m.hi('Khánh Hòa',inn(t,tv-.3,.6),CGOLD);sh(A,t,540,400,-2,popv(t,tv,.5))}}});
// 14 tỉnh lại trải tới sông Phan Rang, nơi dinh Thái Khang bắt đầu gần 400 năm trước
S2(14,14,'p',null,g=>{const m=vnmap(960,880,114);const cs=MLINE(m,COAST,CGOLD,12);const rg=RINGS(m.top,CRED);const lp=LBL(m,'SÔNG PHAN RANG',30);const tile=TILE(g,'THÁI KHANG','#cdd6e0',480);const A=strip('LẠI TRẢI TỚI',false,40,141),B=strip('NƠI MỌI THỨ BẮT ĐẦU',true,42,142);const SH=SEAH();const tp=AT(14,'Phan',3.0);bm(tp);
 return{upd:t=>{const e=inn(t,R(14)-.2,.5);m.at(540,760,0,1,e);m.view(lerp(109.0,108.95,inn(t,R(14),E(14)-R(14))),12.0,lerp(240,300,inn(t,R(14),E(14)-R(14))));seaH(SH,t,e);m.hi('Khánh Hòa',e,'#e9c46a');const[x,y]=m.P(...PR);RU(rg,t,90,x,y,inn(t,tp,.4));LAT(m,lp,[108.6,11.45],inn(t,tp,.4));
  cs(.001+.999*inn(t,AT(14,'Thái',5.0),1.0));PUT(tile,540,1000,popv(t,AT(14,'Thái',5.0),.5),.8,Math.sin(t*1.5)*2);sh(A,t,540,400,-2,popv(t,R(14)+.05,.5));sh(B,t,540,1130,1,popv(t,AT(14,'Thái',5.0)+.3,.5))}}});
// 15 câu hỏi: bạn đã từng đến Nha Trang, hay mơ một lần ra Trường Sa?
S2(15,15,'d',null,g=>{const a=TILE(g,'NHA TRANG',CGOLD,560),b=TILE(g,'TRƯỜNG SA','#7fb8e8',560);const A=strip('BẠN ĐÃ ĐẾN CHƯA?',true,52,151);const q=T(g,0,0,'?',160,CGOLD,12,'middle',OLN);bm(R(15)+.2);
 return{upd:t=>{PUT(a,540,560,popv(t,AT(15,'Nha',1.6)-.2,.5),1,-3+Math.sin(t*2)*2);PUT(b,540,800,popv(t,AT(15,'Trường',3.6)-.2,.5),1,3+Math.sin(t*2+1)*2);PUT(q,860,680,popv(t,R(15)+.3,.4),1,Math.sin(t*3)*6);sh(A,t,540,1080,-1,popv(t,R(15)+.2,.5))}}});
