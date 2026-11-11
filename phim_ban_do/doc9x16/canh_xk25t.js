const VT2='LỬA HY LẠP';
const HB=[];const bm=(t,l)=>{sx(t,'boom',l?{light:true,g:.8}:{g:1});if(!l)HB.push(t)};
const PUT=(o,x,y,u,sc=1,rot=0)=>{o.setAttribute('transform',`translate(${x},${y}) rotate(${rot}) scale(${Math.max(.001,u)*sc})`);o.setAttribute('opacity',u>0?1:0)};
const SIG=(g,col,seed)=>{const k=el(g,'g',{});const r=rng(seed);let d='M-90 10';for(let i=0;i<7;i++)d+=` q${12+r()*10} ${-50-r()*40} ${22+r()*8} ${10+r()*20} t${22+r()*10} ${-6}`;el(k,'path',{d,fill:'none',stroke:col,'stroke-width':8,'stroke-linecap':'round','stroke-linejoin':'round'});return k};
const XX=(g,col='#e5483f')=>{const k=el(g,'g',{});el(k,'path',{d:'M-70 -70 L70 70 M70 -70 L-70 70',stroke:'#fff','stroke-width':34,'stroke-linecap':'round'});el(k,'path',{d:'M-70 -70 L70 70 M70 -70 L-70 70',stroke:col,'stroke-width':20,'stroke-linecap':'round'});return k};
const BEAM=(g,w)=>{const k=el(g,'g',{});el(k,'rect',{x:-w/2,y:-26,width:w,height:52,rx:8,fill:'#6d7378',stroke:'#fff','stroke-width':7});for(let i=0;i<w/52;i++)el(k,'path',{d:`M${-w/2+i*52} 24 L${-w/2+i*52+26} -24 L${-w/2+i*52+52} 24`,fill:'none',stroke:'#2d3236','stroke-width':5});return k};
// ===== v2: màu có nghĩa (đỏ = sai/thiếu/nguy hiểm, vàng đồng = đúng/có, xanh thép = nền/mốc đầu, kem = trung tính) và chuyển động theo lời
const CRED='#d8372d',CGOLD='#e0a63c',CSTEEL='#7fa6c4';
const strip2=(txt,kind,size=44,seed=2)=>{const cv=document.createElement('canvas').getContext('2d');cv.font=`900 ${size}px Inter`;const w=cv.measureText(txt).width+64,h=size+34;const g=mk();const s=el(g,'g',{filter:'url(#sh)'});el(s,'polygon',{points:jag(w,h,seed,4),fill:kind=='bad'?CRED:kind=='ok'?CGOLD:'#efe9d8'});const t=T(g,0,size*.36,txt,size,kind=='bad'?'#fff':'#17120c',0,'middle','none');t.setAttribute('stroke','none');return{g,w,h,at:(x,y,rot=0,sc=1,op=1)=>{g.setAttribute('transform',`translate(${x},${y}) rotate(${rot}) scale(${sc})`);g.setAttribute('opacity',op)}}};
const CK=(g,col=CGOLD)=>{const k=el(g,'g',{});const d='M-60 5 L-20 50 L65 -55';el(k,'path',{d,fill:'none',stroke:'#fff','stroke-width':34,'stroke-linecap':'round','stroke-linejoin':'round'});el(k,'path',{d,fill:'none',stroke:col,'stroke-width':20,'stroke-linecap':'round','stroke-linejoin':'round'});return k};
const shw=(s,t,x,y,rot,k)=>sh(s,t,x,y+Math.sin(t*1.9+x*.01)*4,rot+Math.sin(t*1.3+y*.01)*.8,k);
const WV=(g,col,n=3)=>[...Array(n)].map(()=>el(g,'circle',{fill:'none',stroke:col,'stroke-width':7,r:1,opacity:0}));
const WVU=(ws,t,R0,cx,cy,sp=.5,on=1)=>ws.forEach((e,i)=>{const u=((t*sp+i/ws.length)%1);e.setAttribute('cx',cx);e.setAttribute('cy',cy);e.setAttribute('r',10+u*R0);e.setAttribute('opacity',(1-u)*.85*on)});
const LBL=(g,txt,size=32,col='#fff')=>{const t=T(g,0,0,txt,size,col,9,'middle',DK);t.setAttribute('font-weight',900);return t};
// ===== Lửa Hy Lạp (xk25t). Toàn bộ cảnh vẽ phẳng, không ảnh tư liệu.
// ===== Dấu ấn riêng: nền xanh hải quân đêm (tối) và sương biển nhạt (sáng); sóng ánh sáng trôi ở đáy khung (y>1600); cảnh đặc trưng: mặt cắt cơ chế chuyển động.
{DR1.setAttribute('opacity',0);DR2.setAttribute('opacity',0);
 DARKG.firstChild.setAttribute('fill','#0a1a2c');
 [...PAPG.children].forEach(c=>{if(c.tagName=='g')c.setAttribute('opacity',0);if(c.tagName=='line')c.setAttribute('stroke','rgba(0,0,0,0)')});
 PAPG.firstChild.setAttribute('fill','#d3e0e3');
 const rr=rng(2525);
 const grid=(p,col)=>{const g=el(p,'g',{});for(let y=140;y<1900;y+=120)el(g,'path',{d:`M20 ${y} q 135 -22 270 0 t 270 0 t 270 0 t 270 0`,fill:'none',stroke:col,'stroke-width':2.4})};
 grid(DARKG,'rgba(127,166,196,.09)');grid(PAPG,'rgba(40,80,110,.10)');
 const wav=(p,col)=>{const g=el(p,'g',{});const a=[];for(let i=0;i<16;i++){const e=el(g,'path',{d:'M0 0 q 30 -16 60 0 t 60 0 t 60 0',fill:'none',stroke:col,'stroke-width':4+rr()*3,'stroke-linecap':'round'});a.push({e,x:rr()*1300,y:1620+rr()*250,sp:12+rr()*22,ph:rr()*6})}return a};
 const dA=wav(DARKG,'rgba(224,166,60,.28)'),dB=wav(PAPG,'rgba(40,90,130,.30)');
 window.THEME_UPD=t=>{[dA,dB].forEach(L=>L.forEach(o=>{const x=((o.x+t*o.sp)%1400)-160;o.e.setAttribute('transform',`translate(${x.toFixed(1)},${(o.y+Math.sin(t*.9+o.ph)*9).toFixed(1)})`)}))};
}
const OLN='#0a1018',BRZ='#b8802f',SEAC='#2c5a7e';
// ----- hình vẽ phẳng
const FLM=(g)=>{const k=el(g,'g',{});el(k,'path',{d:'M0 0 C-64 -8 -76 -92 -22 -178 C-14 -124 12 -112 22 -156 C76 -92 70 -8 0 0Z',fill:CRED,stroke:'#fff','stroke-width':7,'stroke-linejoin':'round'});el(k,'path',{d:'M0 -4 C-36 -10 -42 -70 -8 -118 C0 -84 22 -80 28 -104 C48 -62 42 -10 0 -4Z',fill:CGOLD});el(k,'path',{d:'M0 -6 C-16 -10 -18 -40 -2 -62 C8 -44 18 -40 16 -20 C14 -10 8 -6 0 -6Z',fill:'#fff3c4'});return k};
const SHIP=(g,col='#22374d')=>{const k=el(g,'g',{});el(k,'path',{d:'M-210 -10 Q-190 70 -120 78 L150 78 Q215 60 245 -44 Q205 -10 160 -10 Z',fill:col,stroke:'#fff','stroke-width':7,'stroke-linejoin':'round'});el(k,'rect',{x:-6,y:-190,width:12,height:182,fill:col,stroke:'#fff','stroke-width':5});el(k,'path',{d:'M10 -178 L124 -64 L10 -64Z',fill:'#e3d7b8',stroke:'#fff','stroke-width':4,'stroke-linejoin':'round'});for(let i=0;i<5;i++)el(k,'path',{d:`M${-130+i*60} 40 L${-150+i*60} 100`,stroke:'#fff','stroke-width':5,'stroke-linecap':'round'});const tb=el(k,'g',{transform:'translate(214,-26)'});el(tb,'rect',{x:0,y:-13,width:96,height:26,rx:9,fill:BRZ,stroke:'#fff','stroke-width':5});el(tb,'rect',{x:84,y:-18,width:26,height:36,rx:6,fill:'#8f5f22',stroke:'#fff','stroke-width':4});tb.setAttribute('opacity',0);return{k,tb}};
const CITY=(g)=>{const k=el(g,'g',{});const W='#6a7480';el(k,'rect',{x:-400,y:0,width:800,height:120,fill:W,stroke:'#fff','stroke-width':7});for(let i=0;i<14;i++)el(k,'rect',{x:-392+i*58,y:-20,width:34,height:24,fill:W,stroke:'#fff','stroke-width':5});for(const x of[-330,-110,150,340]){el(k,'rect',{x:x-42,y:-100,width:84,height:220,fill:'#7a8591',stroke:'#fff','stroke-width':7});for(let i=0;i<3;i++)el(k,'rect',{x:x-42+i*30,y:-120,width:24,height:24,fill:'#7a8591',stroke:'#fff','stroke-width':5})}el(k,'path',{d:'M-60 0 Q-60 -150 40 -150 Q140 -150 140 0Z',fill:CGOLD,stroke:'#fff','stroke-width':7});el(k,'path',{d:'M40 -150 L40 -200 M25 -185 L55 -185',stroke:'#fff','stroke-width':9,'stroke-linecap':'round'});el(k,'rect',{x:-22,y:60,width:44,height:60,rx:14,fill:OLN});return k};
const SEA=(g,y0,h,col=SEAC)=>{const k=el(g,'g',{});el(k,'rect',{x:0,y:y0,width:1080,height:h,fill:col,opacity:.85});const L=[];for(let i=0;i<5;i++)L.push(el(k,'path',{d:'M-200 0 q 60 -20 120 0 t 120 0 t 120 0 t 120 0 t 120 0 t 120 0 t 120 0 t 120 0 t 120 0 t 120 0',fill:'none',stroke:'rgba(255,255,255,.4)','stroke-width':5,'stroke-linecap':'round'}));return{k,upd:t=>L.forEach((e,i)=>e.setAttribute('transform',`translate(${((t*30*(i%2?1:-1)+i*70)%240)-40},${y0+34+i*((h-60)/5)})`))}};
const PIN=(g,txt)=>{const k=el(g,'g',{});el(k,'path',{d:'M0 0 L-26 -62 A36 36 0 1 1 26 -62 Z',fill:CRED,stroke:'#fff','stroke-width':6,'stroke-linejoin':'round'});el(k,'circle',{cy:-84,r:13,fill:'#fff'});return k};
const MAN=(g)=>{const k=el(g,'g',{});el(k,'path',{d:'M-62 150 L-46 -20 Q0 -52 46 -20 L62 150Z',fill:'#35507a',stroke:'#fff','stroke-width':7,'stroke-linejoin':'round'});el(k,'circle',{cy:-84,r:46,fill:'#d9b38a',stroke:'#fff','stroke-width':7});el(k,'path',{d:'M-52 -96 Q0 -150 52 -96 L52 -84 Q0 -112 -52 -84Z',fill:'#17120c'});return k};
const SCROLL=(g,w=420,h=300)=>{const k=el(g,'g',{});el(k,'rect',{x:-w/2,y:-h/2,width:w,height:h,rx:12,fill:'#e8dcba',stroke:OLN,'stroke-width':7});el(k,'rect',{x:-w/2-14,y:-h/2-8,width:28,height:h+16,rx:12,fill:'#c9a45a',stroke:OLN,'stroke-width':6});el(k,'rect',{x:w/2-14,y:-h/2-8,width:28,height:h+16,rx:12,fill:'#c9a45a',stroke:OLN,'stroke-width':6});for(let i=0;i<6;i++)el(k,'path',{d:`M${-w/2+40} ${-h/2+36+i*44} L${w/2-40-((i*53)%110)} ${-h/2+36+i*44}`,stroke:'rgba(90,60,30,.55)','stroke-width':7,'stroke-linecap':'round'});return k};
// ----- mặt cắt cơ chế (giả thuyết của Haldon): thùng đồng kín, bơm, ống đồng, lửa mồi, tia lửa
const MECH=(g)=>{const k=el(g,'g',{});
 const ca=el(k,'g',{});el(ca,'rect',{x:-380,y:-150,width:210,height:240,rx:34,fill:BRZ,stroke:'#fff','stroke-width':8});const liq=el(ca,'rect',{x:-364,y:-60,width:178,height:140,rx:22,fill:'#1a2a3e'});el(ca,'rect',{x:-380,y:-168,width:210,height:34,rx:12,fill:'#8f5f22',stroke:'#fff','stroke-width':6});
 const pipe=el(k,'g',{});el(pipe,'rect',{x:-170,y:-76,width:480,height:46,fill:BRZ,stroke:'#fff','stroke-width':7});el(pipe,'path',{d:'M310 -88 L400 -62 L400 -44 L310 -18Z',fill:'#8f5f22',stroke:'#fff','stroke-width':6,'stroke-linejoin':'round'});
 const pm=el(k,'g',{});el(pm,'rect',{x:-70,y:-30,width:96,height:150,rx:10,fill:'#6d7378',stroke:'#fff','stroke-width':7});const pis=el(pm,'g',{});el(pis,'rect',{x:-52,y:20,width:60,height:36,fill:'#cfd4d8',stroke:OLN,'stroke-width':4});el(pis,'rect',{x:-26,y:56,width:8,height:90,fill:'#cfd4d8',stroke:OLN,'stroke-width':3});el(pis,'rect',{x:-70,y:140,width:96,height:18,rx:8,fill:'#8a5a32',stroke:'#fff','stroke-width':5});
 const dots=[...Array(7)].map(()=>el(k,'circle',{r:9,fill:'#7fa6c4',stroke:'#fff','stroke-width':2.5,opacity:0}));
 const pilot=el(k,'g',{opacity:0});const pf=FLM(pilot);pf.setAttribute('transform','translate(0,0) scale(.28)');pilot.setAttribute('transform','translate(412,-53)');
 const jet=el(k,'g',{opacity:0});const j1=el(jet,'path',{d:'M0 0',fill:CRED,stroke:'#fff','stroke-width':6,'stroke-linejoin':'round'}),j2=el(jet,'path',{d:'M0 0',fill:CGOLD});
 const upd=(t,o)=>{ // o: {show, flow, pil, jet}
  const f=o.flow;liq.setAttribute('height',140*(1-.35*f));liq.setAttribute('y',-60+140*.35*f);
  pis.setAttribute('transform',`translate(0,${f>0?Math.abs(Math.sin(t*3.2))*-34:0})`);
  dots.forEach((d,i)=>{const u=((t*.5+i/7)%1);d.setAttribute('cx',-160+u*480);d.setAttribute('cy',-53);d.setAttribute('opacity',f>0?.9*Math.min(1,f):0)});
  pilot.setAttribute('opacity',o.pil>0?1:0);pf.setAttribute('transform',`scale(${.26+.03*Math.sin(t*14)})`);
  const J=o.jet;jet.setAttribute('opacity',J>0?1:0);if(J>0){const L=330*J,w=1+.06*Math.sin(t*17);j1.setAttribute('d',`M400 -53 Q${400+L*.5} ${-53-70*w} ${400+L} ${-53-18+Math.sin(t*9)*10} Q${400+L*.55} ${-53+60*w} 400 -53Z`);j2.setAttribute('d',`M400 -53 Q${400+L*.4} ${-53-34*w} ${400+L*.75} ${-53-6} Q${400+L*.4} ${-53+30*w} 400 -53Z`)}
 };
 return{k,upd}};
const MLB=(g,txt,sz=30,col='#fff')=>{const t=T(g,0,0,txt,sz,col,10,'middle',OLN);t.setAttribute('font-weight',900);return t};
// ===== các cảnh
// 1: hook, lửa cháy trên mặt biển
S2(1,1,'d',null,g=>{const s=SEA(g,560,520,'#0f2a44');const fl=[300,540,780].map(x=>({x,f:FLM(g)}));const q=T(g,0,0,'?',300,CRED,16,'middle',OLN);const A=strip2('LỬA CHÁY TRÊN MẶT BIỂN','base',40,251),B=strip2('NƯỚC KHÔNG DẬP ĐƯỢC','bad',40,252);
 return{upd:t=>{s.upd(t);fl.forEach((o,i)=>{PUT(o.f,o.x,640+Math.sin(t*1.4+i)*5,popv(t,R(1)+.3+i*.35,.6),1.15+.05*Math.sin(t*11+i),Math.sin(t*8+i)*2.5)});PUT(q,540,560,popv(t,AT(1,'công',3.8),.5),1,Math.sin(t*2)*5);shw(A,t,540,1085,-1,PV(t,1,'cháy',1.6));shw(B,t,540,1195,1,PV(t,1,'nước',3.0))}}});
// 2: hạm đội vây thành
S2(2,2,'p',null,g=>{const c=CITY(g);const s=SEA(g,780,320,'#7fa6c4');const sh=[0,1,2].map(i=>SHIP(g));const q=T(g,0,0,'?',280,CRED,16,'middle',OLN);const A=strip2('HẠM ĐỘI ĐANG VÂY THÀNH','base',38,261),B=strip2('VẬY LỬA ẤY LÀ GÌ?','bad',40,262);
 return{upd:t=>{s.upd(t);PUT(c,300,520,popv(t,R(2)+.1,.6),.75,0);sh.forEach((o,i)=>{const u=inn(t,R(2)+.3+i*.4,2.6);PUT(o.k,1180-u*(500-i*70),840+i*20+Math.sin(t*1.6+i)*5,1,.62,-2+i*2)});PUT(q,830,540,popv(t,AT(2,'nó',4.6),.5),1,Math.sin(t*2)*5);shw(A,t,540,1085,-1,PV(t,2,'chống',1.8));shw(B,t,540,1195,1,PV(t,2,'nó',4.6))}}});
// 3: Constantinople
S2(3,3,'d',null,g=>{const c=CITY(g);const s=SEA(g,800,300,'#143454');const pn=PIN(g);const lb=MLB(g,'CONSTANTINOPLE',44,CGOLD);const A=strip2('KINH ĐÔ ĐẾ QUỐC ĐÔNG LA MÃ','base',34,271),B=strip2('NẰM SÁT BIỂN, KẺ THÙ ĐI BẰNG THUYỀN','bad',30,272);
 return{upd:t=>{s.upd(t);PUT(c,540,640+Math.sin(t*1.4)*3,popv(t,R(3)+.1,.6),1.18,0);PUT(pn,587,440,popv(t,R(3)+.9,.5),1,Math.sin(t*2)*4);PUT(lb,540,900,popv(t,R(3)+1.0,.5),1,0);shw(A,t,540,1085,-1,PV(t,3,'kinh',.6));shw(B,t,540,1195,1,PV(t,3,'sát',3.6))}}});
// 4: những năm 670, hạm đội Ả Rập
S2(4,4,'p',null,g=>{const big=bigNum(g,'NHỮNG NĂM 670',100,CRED);const s=SEA(g,700,380,'#7fa6c4');const sh=[0,1,2,3].map(i=>SHIP(g,'#4a2a2a'));const A=strip2('HẠM ĐỘI Ả RẬP','base',40,281),B=strip2('NHIỀU LẦN KÉO ĐẾN VÂY THÀNH','bad',32,282);
 return{upd:t=>{s.upd(t);PUT(big,540,380,popv(t,R(4)+.2,.55),1,-2);sh.forEach((o,i)=>{const u=inn(t,R(4)+.5+i*.45,2.2);PUT(o.k,-220+u*(300+i*190),820+(i%2)*40+Math.sin(t*1.6+i)*5,1,.5,2)});shw(A,t,540,1085,-1,PV(t,4,'hạm',1.4));shw(B,t,540,1195,1,PV(t,4,'nhiều',2.0))}}});
// 5: Kallinikos, Theophanes, từ Syria
S2(5,5,'d',null,g=>{const m=MAN(g);const jar=el(g,'g',{});el(jar,'path',{d:'M-30 -30 Q-52 20 -26 60 L26 60 Q52 20 30 -30Z',fill:BRZ,stroke:'#fff','stroke-width':6,'stroke-linejoin':'round'});const f=FLM(g);const sc=SCROLL(g,380,260);const lb=MLB(g,'THEOPHANES',40,CGOLD),lb2=MLB(g,'NHÀ CHÉP SỬ',30,'#fff');const A=strip2('KALLINIKOS · NGƯỜI TỪ SYRIA','base',34,291),B=strip2('THEO NHÀ CHÉP SỬ THEOPHANES','ok',32,292);
 return{upd:t=>{PUT(m,330,640+Math.sin(t*1.5)*4,popv(t,R(5)+.2,.6),1.45,-2);PUT(jar,330+150,740,popv(t,AT(5,'thứ',2.6),.5),1.0,-10);PUT(f,330+150,700,popv(t,AT(5,'thứ',2.6)+.2,.5),.5+.03*Math.sin(t*12),Math.sin(t*8)*3);PUT(sc,770,590+Math.sin(t*1.3)*5,popv(t,R(5)+.5,.6),1.0,3);PUT(lb,770,780,popv(t,R(5)+.7,.5),1,0);PUT(lb2,770,830,popv(t,R(5)+.9,.5),1,0);shw(A,t,540,1085,-1,PV(t,5,'một',2.0));shw(B,t,540,1195,1,PV(t,5,'Theo',.2))}}});
// 6: ống đồng ở mũi tàu, xoay được
S2(6,6,'p',null,g=>{const s=SEA(g,820,300,'#7fa6c4');const sh=SHIP(g,'#22374d');sh.tb.setAttribute('opacity',1);const l1=MLB(g,'ỐNG ĐỒNG Ở MŨI TÀU',34,'#17120c');l1.setAttribute('stroke','none');const A=strip2('ỐNG ĐỒNG Ở MŨI TÀU CHIẾN','ok',34,301),B=strip2('XOAY ĐƯỢC ĐỂ NHẮM','base',38,302);
 return{upd:t=>{s.upd(t);PUT(sh.k,500,700+Math.sin(t*1.6)*6,popv(t,R(6)+.1,.6),1.25,-1);const w=AT(6,'xoay',3.6),u=inn(t,w,1.6);sh.tb.setAttribute('transform',`translate(214,-26) rotate(${Math.sin(u*Math.PI*2)*18})`);PUT(l1,560,420,popv(t,AT(6,'ống',1.0),.5),1,0);shw(A,t,540,1085,-1,PV(t,6,'ống',1.0));shw(B,t,540,1195,1,PV(t,6,'xoay',3.6))}}});
// 7-8: mô phỏng cơ chế (giả thuyết)
S2(7,8,'d',null,g=>{const m=MECH(g);const gt=strip2('GIẢ THUYẾT CỦA JOHN HALDON','bad',32,311);const l1=MLB(g,'THÙNG ĐỒNG KÍN',30,CGOLD),l2=MLB(g,'BƠM',32,'#fff'),l3=MLB(g,'ỐNG ĐỒNG',30,CGOLD),l4=MLB(g,'LỬA MỒI',30,'#ffd7d3');const A=strip2('BƠM ÉP CHẤT CHÁY QUA ỐNG','ok',32,312),B=strip2('QUA LỬA MỒI: TIA LỬA DÀI','bad',32,313);
 return{upd:t=>{const w1=AT(7,'thùng',2.4),w2=AT(7,'bơm',4.0),w3=R(8)+.2,w4=AT(8,'bùng',3.6);const sc=.8;m.k.setAttribute('transform',`translate(390,640) scale(${sc})`);m.k.setAttribute('opacity',popv(t,R(7)+.1,.5)>0?1:0);m.upd(t,{flow:t>w2?Math.min(1,(t-w2)/1.0):0,pil:t>w3?1:0,jet:t>w4?inn(t,w4,1.2):0});shw(gt,t,540,330,-1,PV(t,7,'mô',.4));PUT(l1,390-300*sc,470,popv(t,w1,.5),1,0);PUT(l2,390-20*sc,830,popv(t,w2-.4,.5),1,0);PUT(l3,390+60*sc,520,popv(t,w2+.4,.5),1,0);PUT(l4,390+420*sc,700,popv(t,w3,.5),1,0);shw(A,t,540,1085,-1,PV(t,7,'bơm',4.0));shw(B,t,540,1195,1,popv(t,w4-.2,.5))}}});
// 9: chưa ai biết chắc, tài liệu sơ lược
S2(9,9,'p',null,g=>{const sc=SCROLL(g,520,380);const q=T(g,0,0,'?',340,CRED,16,'middle',OLN);const gt=strip2('GIẢ THUYẾT','bad',44,321);const A=strip2('TÀI LIỆU BYZANTINE QUÁ SƠ LƯỢC','base',32,322),B=strip2('CHƯA AI BIẾT CHẮC CẤU TẠO','bad',36,323);
 return{upd:t=>{PUT(sc,540,600+Math.sin(t*1.4)*5,popv(t,R(9)+.1,.6),1.1,-2);PUT(q,540,600,popv(t,AT(9,'chưa',.6),.5),1,Math.sin(t*2)*5);shw(gt,t,540,330,-1,PV(t,9,'Tất',5.4));shw(A,t,540,1085,-1,PV(t,9,'tài',2.2));shw(B,t,540,1195,1,PV(t,9,'chưa',.6))}}});
// 10: 2002 dựng lại, phun xa hơn 10 mét
S2(10,10,'d',null,g=>{const m=MECH(g);const big=bigNum(g,'2002',150,CGOLD);const rl=el(g,'g',{});el(rl,'path',{d:'M0 0 L560 0',stroke:'#fff','stroke-width':8,'stroke-linecap':'round'});for(let i=0;i<=5;i++){el(rl,'path',{d:`M${i*112} -18 L${i*112} 18`,stroke:'#fff','stroke-width':6});}const l1=MLB(g,'XA HƠN 10 MÉT',42,CGOLD);const A=strip2('NHÓM HALDON DỰNG LẠI THIẾT BỊ','base',32,331),B=strip2('PHUN LỬA XA HƠN 10 MÉT','ok',38,332);
 return{upd:t=>{const w=AT(10,'phun',3.4);m.k.setAttribute('transform','translate(380,650) scale(.72)');m.k.setAttribute('opacity',popv(t,R(10)+.1,.5)>0?1:0);m.upd(t,{flow:t>R(10)+.8?1:0,pil:1,jet:t>w?inn(t,w,1.0):0});PUT(big,540,450,popv(t,R(10)+.2,.55),1,-2);PUT(rl,300,860,popv(t,w+.4,.5),1,0);PUT(l1,580,930,popv(t,w+.9,.5),1,0);shw(A,t,540,1085,-1,PV(t,10,'nhóm',.3));shw(B,t,540,1195,1,PV(t,10,'phun',3.4))}}});
// 11-12: hải chiến, thuyền phun lửa vào hạm đội địch (mô phỏng chi tiết)
S2(11,12,'d',null,g=>{
 const c=CITY(g);const s=SEA(g,720,340,'#0f2a44');
 const bz=SHIP(g,'#22374d');bz.tb.setAttribute('opacity',1);
 const mkE=(col)=>{const w=el(g,'g',{});const sh=SHIP(w,col);return{w,sh}};
 const E=[mkE('#3a2020'),mkE('#3a2020'),mkE('#3a2020')];
 const jet=el(g,'g',{opacity:0});const j1=el(jet,'path',{d:'M0 0',fill:CRED,stroke:'#fff','stroke-width':6,'stroke-linejoin':'round'}),j2=el(jet,'path',{d:'M0 0',fill:CGOLD});
 const dk=[0,1,2].map(()=>FLM(g)),wf=[0,1,2,3,4].map(()=>FLM(g));
 const sm=[...Array(7)].map(()=>el(g,'circle',{r:26,fill:'#59636d',opacity:0}));
 const dr=[...Array(7)].map(()=>el(g,'path',{d:'M0 -26 Q14 0 0 12 Q-14 0 0 -26Z',fill:'#bfe0f0',stroke:'#fff','stroke-width':3,opacity:0}));
 const xx=XX(g,CRED),ck=CK(g,CGOLD);
 const A1=strip2('NỔI TRÊN MẶT BIỂN','bad',40,341),B1=strip2('NƯỚC KHÔNG DẬP ĐƯỢC','bad',40,342),A2=strip2('HẠM ĐỘI Ả RẬP THIỆT HẠI NẶNG','bad',34,351),B2=strip2('THÀNH PHỐ ĐỨNG VỮNG','ok',40,352);
 return{upd:t=>{
  s.upd(t);
  const t0=R(11),tAim=t0+1.4,tHit=AT(11,'nổi',2.0),tWat=AT(11,'nước',3.4),tPan=AT(11,'Kẻ',5.0),t12=R(12),tSink=t12+.8,tCity=AT(12,'Thành',4.6);
  PUT(c,250,470,popv(t,t0+.1,.6),.5,0);
  // thuyền Byzantine bên trái, ống xoay nhắm vào thuyền dẫn đầu
  PUT(bz.k,230,830+Math.sin(t*1.7)*5,popv(t,t0+.1,.6),.95,-1);
  const aim=inn(t,tAim,1.0);bz.tb.setAttribute('transform',`translate(214,-26) rotate(${-8*aim})`);
  // thuyền địch tiến vào
  const fin=[[770,830,.8],[960,915,.52],[1000,780,.5]];
  E.forEach((e,i)=>{const [fx,fy,fs]=fin[i];const u=inn(t,t0+.2+i*.35,1.8);let x=fx+(1-u)*(500+i*60),y=fy+Math.sin(t*1.6+i)*5,r=0;
   if(i>0){const p=inn(t,tPan+i*.2,1.6);x+=p*380;r=-p*5} 
   if(i==0){const sk=inn(t,tSink,3.6);y+=sk*80;r=-sk*18}
   e.w.setAttribute('transform',`translate(${x.toFixed(1)},${y.toFixed(1)}) rotate(${r.toFixed(1)}) scale(${-fs},${fs})`);e.w.setAttribute('opacity',popv(t,t0+.2+i*.35,.3)>0?1:0)});
  // tia lửa từ ống đồng vào thuyền dẫn đầu
  const jx=230+(310*Math.cos(-8*aim*Math.PI/180))*.95,jy=830-26*.95-(310*Math.sin(8*aim*Math.PI/180))*.95;
  const J=t>tHit?Math.min(1,inn(t,tHit,.7)):0,off=t>tHit+2.2?Math.max(0,1-inn(t,tHit+2.2,.6)):1;const K=J*off;jet.setAttribute('opacity',K>0?1:0);
  if(K>0){const Lm=Math.max(60,(760-jx))*K,w=1+.06*Math.sin(t*17);const ty=jy-(jy-815)*K*.4;j1.setAttribute('d',`M${jx} ${jy} Q${jx+Lm*.5} ${jy-60*w} ${jx+Lm} ${ty-10+Math.sin(t*9)*8} Q${jx+Lm*.55} ${jy+50*w} ${jx} ${jy}Z`);j2.setAttribute('d',`M${jx} ${jy} Q${jx+Lm*.4} ${jy-28*w} ${jx+Lm*.8} ${ty-6} Q${jx+Lm*.4} ${jy+24*w} ${jx} ${jy}Z`)}
  // lửa cháy trên boong thuyền dẫn đầu và nổi trên mặt biển
  const sk=inn(t,tSink,3.6),bx=770,by=830+sk*80;
  [[-70,-22],[0,-70],[70,-20]].forEach((p,i)=>PUT(dk[i],bx+p[0]*.8,by+p[1]*.8,popv(t,tHit+.3+i*.25,.5)*(1-sk*.35),.55+.05*Math.sin(t*11+i),Math.sin(t*8+i)*3));
  [[-170,0],[-70,14],[50,8],[170,0],[260,16]].forEach((p,i)=>PUT(wf[i],bx+p[0],905+p[1]+Math.sin(t*1.8+i)*3,popv(t,tHit+.8+i*.25,.5),.5+.04*Math.sin(t*12+i),Math.sin(t*8+i)*3));
  sm.forEach((m,i)=>{const u=((t-tHit-.5)*.35+i/7)%1;const on=t>tHit+.5?1:0;m.setAttribute('cx',bx-20+Math.sin(i*2.3+t)*30);m.setAttribute('cy',by-120-u*320);m.setAttribute('r',22+u*40);m.setAttribute('opacity',on*(1-u)*.5)});
  // giọt nước dội xuống mà lửa không tắt
  dr.forEach((d,i)=>{const u=((t-tWat)*.9+i/7)%1;d.setAttribute('transform',`translate(${600+i*50},${420+u*430})`);d.setAttribute('opacity',(t>tWat&&t<t12-.1)?(u<.95?1:0):0)});
  PUT(xx,800,560,popv(t,AT(11,'không',4.3),.5)*(t<t12?1:0),1.3,0);
  PUT(ck,250,300,popv(t,tCity,.5),.8,0);
  shw(A1,t,540,1085,-1,t<t12?PV(t,11,'nổi',2.0):0);shw(B1,t,540,1195,1,t<t12?PV(t,11,'không',4.3):0);
  shw(A2,t,540,1085,-1,t>=t12?PV(t,12,'gây',1.8):0);shw(B2,t,540,1195,1,t>=t12?PV(t,12,'Thành',4.6):0);
 }}});
// 13: năm 717, Leo Đệ Tam, eo biển Bosporus
S2(13,13,'p',null,g=>{const big=bigNum(g,'717',190,CRED);const sh1=el(g,'rect',{x:0,y:620,width:1080,height:70,fill:'#8a7a5a'});const sh2=el(g,'rect',{x:0,y:960,width:1080,height:70,fill:'#8a7a5a'});const s=SEA(g,690,270,'#7fa6c4');const ship=SHIP(g,'#22374d');ship.tb.setAttribute('opacity',1);const ch=[...Array(3)].map(i=>SHIP(g,'#4a2a2a'));const fl=FLM(g);const l1=MLB(g,'EO BIỂN BOSPORUS',34,'#17120c');l1.setAttribute('stroke','none');const A=strip2('HOÀNG ĐẾ LEO ĐỆ TAM','base',38,361),B=strip2('PHÁ VÒNG VÂY TRÊN EO BIỂN','ok',34,362);
 return{upd:t=>{s.upd(t);PUT(big,540,470,popv(t,R(13)+.2,.55),1,-2);PUT(l1,540,560,popv(t,AT(13,'eo',4.6),.5),1,0);PUT(ship.k,260,840+Math.sin(t*1.6)*5,popv(t,R(13)+.4,.5),.62,0);const w=AT(13,'phá',3.0);ch.forEach((o,i)=>PUT(o.k,780+i*120-inn(t,w,1.5)*60,820+(i%2)*60,1,.4,0));PUT(fl,520,830,popv(t,w,.5),.7+.04*Math.sin(t*11),Math.sin(t*8)*3);shw(A,t,540,1085,-1,PV(t,13,'Hoàng',1.0));shw(B,t,540,1195,1,PV(t,13,'phá',3.0))}}});
// 14: bí mật nhà nước
S2(14,14,'d',null,g=>{const c=el(g,'g',{});el(c,'rect',{x:-190,y:-30,width:380,height:210,rx:20,fill:'#6b4a2a',stroke:'#fff','stroke-width':8});el(c,'path',{d:'M-190 -30 Q-190 -130 0 -130 Q190 -130 190 -30Z',fill:'#8a5a32',stroke:'#fff','stroke-width':8,'stroke-linejoin':'round'});el(c,'rect',{x:-28,y:-20,width:56,height:70,rx:10,fill:CGOLD,stroke:OLN,'stroke-width':6});el(c,'circle',{cy:12,r:10,fill:OLN});const pp=[0,1,2].map(i=>MAN(g));const A=strip2('CÔNG THỨC LÀ BÍ MẬT NHÀ NƯỚC','bad',32,371),B=strip2('CHỈ MỘT SỐ ÍT NGƯỜI BIẾT','base',36,372);
 return{upd:t=>{PUT(c,540,560+Math.sin(t*1.4)*4,popv(t,R(14)+.2,.6),1.25,-1);pp.forEach((o,i)=>PUT(o,[240,540,840][i],940,popv(t,AT(14,'chỉ',3.0)+i*.35,.5),.5,0));shw(A,t,540,1085,-1,PV(t,14,'công',.2));shw(B,t,540,1195,1,PV(t,14,'chỉ',3.0))}}});
// 15: thất truyền theo thời gian
S2(15,15,'p',null,g=>{const sc=SCROLL(g,460,330);const ln=el(g,'path',{d:'M120 900 L960 900',stroke:'#17120c','stroke-width':12,'stroke-linecap':'round',pathLength:1,'stroke-dasharray':1,'stroke-dashoffset':1});const q=T(g,0,0,'?',320,CRED,16,'middle',OLN);const A=strip2('RỒI CÔNG THỨC MẤT HẲN','bad',38,381),B=strip2('NAY KHÔNG AI BIẾT LÀM TỪ GÌ','base',32,382);
 return{upd:t=>{const w=AT(15,'mất',2.2),u=inn(t,w,3.2);PUT(sc,540,560+Math.sin(t*1.4)*4,popv(t,R(15)+.1,.6)*(1-u*.65),1.0,-2+u*5);sc.setAttribute('opacity',Math.max(0,1-u*.9));ln.setAttribute('stroke-dashoffset',1-inn(t,R(15)+.4,3.0));PUT(q,540,560,popv(t,AT(15,'Đến',5.0),.5),1,Math.sin(t*2)*5);shw(A,t,540,1085,-1,PV(t,15,'công',2.2));shw(B,t,540,1195,1,PV(t,15,'không',6.0))}}});
// 16: giả thuyết thành phần
S2(16,16,'d',null,g=>{const mk2=(txt,col)=>{const k=el(g,'g',{});el(k,'rect',{x:-200,y:-62,width:400,height:124,rx:16,fill:'#efe3c2',stroke:'#fff','stroke-width':7});const a=T(k,0,16,txt,46,col,0,'middle','none');a.setAttribute('font-weight',900);a.setAttribute('stroke','none');return k};const c=[mk2('DẦU MỎ','#17120c'),mk2('NHỰA CÂY','#17120c'),mk2('VÔI SỐNG ?',CRED),mk2('DIÊM TIÊU ?',CRED)];const gt=strip2('GIẢ THUYẾT','bad',44,391);const A=strip2('NHIỀU NGƯỜI NGHĨ LÀ DẦU MỎ','ok',34,392),B=strip2('VÔI SỐNG, DIÊM TIÊU: CHƯA CHỨNG MINH','bad',28,393);
 return{upd:t=>{shw(gt,t,540,330,-1,popv(t,R(16)+.1,.55));const X=[300,780,300,780],Y=[560,600,800,840],W=[R(16)+.4,AT(16,'trộn',3.4),AT(16,'vôi',6.2),AT(16,'diêm',7.2)];c.forEach((o,i)=>PUT(o,X[i],Y[i]+Math.sin(t*1.5+i)*4,popv(t,W[i],.5),.82,(i%2?3:-3)));shw(A,t,540,1085,-1,PV(t,16,'Nhiều',.2));shw(B,t,540,1195,1,PV(t,16,'Từng',5.6))}}});
// 17: câu hỏi cuối
S2(17,17,'p',null,g=>{const s=SEA(g,700,360,'#7fa6c4');const f=FLM(g);const q=T(g,0,0,'?',340,CRED,16,'middle',OLN);const A=strip2('VẬY VÌ SAO NÓ BIẾN MẤT?','bad',40,401),B=strip2('CÂU TRẢ LỜI VẪN BỎ NGỎ','base',36,402);
 return{upd:t=>{s.upd(t);const d=inn(t,AT(17,'biến',2.6),3.0);PUT(f,540,780+Math.sin(t*1.5)*4,popv(t,R(17)+.2,.6)*(1-d*.7),1.5*(1-d*.5)+.04*Math.sin(t*11),Math.sin(t*8)*2.5);PUT(q,540,560,popv(t,AT(17,'Vậy',.2),.5),1,Math.sin(t*2)*5);shw(A,t,540,1085,-1,PV(t,17,'Vậy',.2));shw(B,t,540,1195,1,PV(t,17,'Câu',4.6))}}});
sx(R(1)+.1,'whoosh',{d:.5,g:.5});
for(let i=1;i<=17;i++)bm(R(i)+.3,i%3!=1);
sx(R(8)+.2,'blast',{g:.8});sx(AT(11,'nổi',2.0),'blast',{g:.8});sx(R(6)+.4,'creak',{g:.5});sx(R(17)+.3,'question',{g:.7});
