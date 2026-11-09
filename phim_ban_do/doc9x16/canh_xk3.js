// ===== Nữ thần Tự do (xk3). Ảnh: ts1(1) ts2(2) ts4(4) ts5(5) ts7+ts8(8) ts9(9) ts10(10) ts11(11). Cảnh 3, 6, 7, 12 vẽ phẳng.
const HB=[];const bm=(t,l)=>{sx(t,'boom',l?{light:true,g:.8}:{g:1});if(!l)HB.push(t)};
const crown=(g,sc=1)=>{const k=el(g,'g',{});for(let i=0;i<7;i++){const a=-Math.PI/2+(i-3)*.42;const x=Math.cos(a)*70,y=Math.sin(a)*70;el(k,'path',{d:`M${x*.9} ${y*.9+40} L${x*2.5} ${y*2.5+40}`,stroke:'#fff','stroke-width':26,'stroke-linecap':'round'});el(k,'path',{d:`M${x*.9} ${y*.9+40} L${x*2.5} ${y*2.5+40}`,stroke:'#d9a441','stroke-width':14,'stroke-linecap':'round'})}
 el(k,'path',{d:'M-90 150 Q-100 20 0 10 Q100 20 90 150Z',fill:'#6f9a86',stroke:'#fff','stroke-width':8,'stroke-linejoin':'round'});el(k,'rect',{x:-96,y:30,width:192,height:26,rx:10,fill:'#85b49f',stroke:'#fff','stroke-width':6});return k};
const PUT=(o,x,y,u,sc=1,rot=0)=>{o.setAttribute('transform',`translate(${x},${y}) rotate(${rot}) scale(${Math.max(.001,u)*sc})`);o.setAttribute('opacity',u>0?1:0)};
// 1: mở đầu (ts1 đầu tượng ở Paris)
S2(1,1,'d',null,g=>{const c=card('ts1',IMG+'ts1.jpg',560,640,11);const A=strip('NỮ THẦN TỰ DO',true,54,12),B=strip('QUÀ KỶ NIỆM 100 NĂM ĐỘC LẬP',false,32,13),L=strip('ĐẦU TƯỢNG TRƯNG BÀY Ở PARIS',false,26,14);const cr=crown(g);
 return{upd:t=>{const e=inn(t,R(1)-.2,.6);c.at(340,650,-2,1,e);c.zoom(1+.1*inn(t,R(1),E(1)-R(1)),.5,.4);const u=popv(t,AT(1,'biểu',3.0),.5);PUT(cr,810,640,u,1.4,6);
  sh(A,t,540,1085,-1,PV(t,1,'tượng',.8));sh(B,t,540,1195,1,PV(t,1,'quà',6.0));sh(L,t,340,330,-1,e)}}});
// 2: Bartholdi (ts2) và Laboulaye
S2(2,2,'p',null,g=>{const c=card('ts2',IMG+'ts2.jpg',520,640,21);const A=strip('FRÉDÉRIC BARTHOLDI',true,40,22),B=strip('NHÀ ĐIÊU KHẮC',false,34,23),C=strip('ÉDOUARD DE LABOULAYE',true,32,24),D=strip('NHÀ SỬ HỌC',false,34,25),F=strip('CẢ HAI LÀ NGƯỜI PHÁP',false,38,26);
 return{upd:t=>{const e=inn(t,R(2)-.2,.6);c.at(310,660,-3,1,e);c.zoom(1+.12*inn(t,R(2),E(2)-R(2)),.5,.4);sh(A,t,780,520,3,PV(t,2,'Bartholdi',2.0));sh(B,t,780,640,-2,PV(t,2,'điêu',1.2));sh(C,t,770,820,-2,PV(t,2,'Laboulaye',4.4));sh(D,t,780,940,2,PV(t,2,'sử',3.6));sh(F,t,540,1180,-1,PV(t,2,'đều',6.2))}}});
// 3: 1875: Bartholdi thiết kế, Laboulaye gây quỹ (vẽ phẳng)
S2(3,3,'d',t=>'1875',g=>{const bp=el(g,'g',{});el(bp,'rect',{x:-210,y:-250,width:420,height:500,rx:24,fill:'#2f5d8c',stroke:'#fff','stroke-width':9});for(let i=0;i<6;i++)el(bp,'path',{d:`M-170 ${-190+i*70} L170 ${-190+i*70}`,stroke:'#8fb4dc','stroke-width':3,opacity:.6});const dr=el(bp,'path',{d:'M-90 190 L-90 -10 Q-90 -90 0 -100 Q90 -90 90 -10 L90 190 M-60 -100 L-110 -170 M0 -110 L0 -190 M60 -100 L110 -170',fill:'none',stroke:'#fff','stroke-width':10,'stroke-linecap':'round','stroke-linejoin':'round',pathLength:1,'stroke-dasharray':'1 1','stroke-dashoffset':1});
 const cn=el(g,'g',{});const coins=[...Array(10)].map((_,i)=>{const k=el(cn,'g',{});el(k,'ellipse',{cx:0,cy:0,rx:70,ry:24,fill:'#d9a441',stroke:'#fff','stroke-width':6});return k});const A=strip('BARTHOLDI: THIẾT KẾ',true,38,31),B=strip('LABOULAYE: GÂY QUỸ',false,38,32);
 return{upd:t=>{const e=popv(t,R(3)+.1,.6);PUT(bp,290,640,e,1,-3);dr.setAttribute('stroke-dashoffset',1-inn(t,AT(3,'Bartholdi',.8)+.6,2.4));
  const w=AT(3,'Laboulaye',3.6);coins.forEach((k,i)=>{const u=popv(t,w+.3+i*.2,.3);k.setAttribute('transform',`translate(790,${960-i*38-(1-u)*60}) scale(${Math.max(.001,u)})`);k.setAttribute('opacity',u>0?1:0)});
  sh(A,t,290,1085,-2,PV(t,3,'Bartholdi',.8));sh(B,t,790,1195,2,PV(t,3,'Laboulaye',3.6))}}});
// 4: khung sắt: Viollet-le-Duc, mất năm 1879 (ts4)
S2(4,4,'p',t=>'1879',g=>{const c=card('ts4',IMG+'ts4.jpg',520,640,41);const A=strip('KHUNG SẮT BÊN TRONG',true,34,42),B=strip('EUGÈNE VIOLLET-LE-DUC',false,34,43),C=strip('MẤT BẤT NGỜ',true,50,44);const rg=ring(c.top,-.2*c.w,-.05*c.h,.22*c.h,'#d8372d');
 return{upd:t=>{const e=inn(t,R(4)-.2,.6);c.at(310,660,-2,1,e);c.zoom(1+.12*inn(t,R(4),E(4)-R(4)),.5,.4);rg.set(inn(t,R(4)+.6,.9));sh(A,t,780,560,3,PV(t,4,'khung',2.0));sh(B,t,770,700,-2,PV(t,4,'Eugène',3.2));sh(C,t,780,880,2,PV(t,4,'mất',5.6))}}});
// 5: Gustave Eiffel (ts5)
S2(5,5,'d',null,g=>{const c=card('ts5',IMG+'ts5.jpg',900,600,51);const A=strip('GUSTAVE EIFFEL',true,52,52),B=strip('HOÀN THÀNH BỘ KHUNG',false,40,53),C=strip('SAU NÀY DỰNG THÁP EIFFEL',true,34,54);
 return{upd:t=>{const e=inn(t,R(5)-.2,.6);c.at(540,640,2,1,e);c.zoom(1+.14*inn(t,R(5),E(5)-R(5)),.5,.4);sh(A,t,540,1085,-1,PV(t,5,'Gustave',.4));sh(B,t,540,1195,1,PV(t,5,'hoàn',2.6));sh(C,t,540,330,-1,PV(t,5,'Ông',4.6))}}});
// 6: 4/7/1884 trao tượng (vẽ phẳng, tờ lịch)
S2(6,6,'p',t=>'1884',g=>{const pg=el(g,'g',{});el(pg,'rect',{x:-260,y:-290,width:520,height:580,rx:30,fill:'#f5efe0',stroke:'#17120c','stroke-width':10});el(pg,'path',{d:'M-260 -230 L-260 -260 Q-260 -290 -230 -290 L230 -290 Q260 -290 260 -260 L260 -230Z',fill:'#d8372d'});const h=T(pg,0,-244,'THÁNG 7 · 1884',44,'#fff',0,'middle','none');h.setAttribute('stroke','none');const d=T(pg,0,100,'4',340,'#17120c',0,'middle','none');d.setAttribute('stroke','none');
 const S=stamp('PHÁP TRAO TƯỢNG',54),B=strip('CHO NƯỚC MỸ',false,46,61);
 return{upd:t=>{const e=popv(t,R(6)+.1,.6);PUT(pg,540,650,e,1,-2);const u=popv(t,AT(6,'chính',3.4),.5);S.at(560,880,-8,Math.max(.001,u),u>0?1:0);sh(B,t,540,1130,1,PV(t,6,'cho',5.0))}}});
// 7: 214 thùng gỗ đến New York (vẽ phẳng)
S2(7,7,'d',t=>'1885',g=>{const n=bigNum(g,'0',220,'#f2c14e');const bx=[...Array(214)].map((_,i)=>{const k=el(g,'g',{});el(k,'rect',{x:-17,y:-17,width:34,height:34,rx:4,fill:'#a8763e',stroke:'#fff','stroke-width':3});el(k,'path',{d:'M-17 -17 L17 17 M17 -17 L-17 17',stroke:'#6b4520','stroke-width':3});return k});
 const A=strip('NEW YORK · 17 THÁNG 6',true,36,71),B=strip('THÙNG GỖ',false,52,72);
 return{upd:t=>{const w=AT(7,'hai',4.4),u=inn(t,w,2.4),cnt=Math.round(u*214);bx.forEach((k,i)=>{const col=i%17,row=Math.floor(i/17);k.setAttribute('transform',`translate(${540-8*44+col*44+0},${470+row*40})`);k.setAttribute('opacity',i<cnt?1:.0)});
  n.textContent=String(cnt);n.setAttribute('transform',`translate(540,1080) rotate(-3) scale(${t>w-.3?1:.001})`);sh(A,t,540,360,-1,PV(t,7,'New',.5));sh(B,t,540,1200,2,PV(t,7,'thùng',6.4))}}});
// 8: bệ tượng, hết tiền (ts7 + ts8)
S2(8,8,'p',t=>'1884',g=>{const c1=card('ts7',IMG+'ts7.jpg',700,480,81),c2=card('ts8',IMG+'ts8.jpg',380,540,82);const A=strip('BỆ TƯỢNG: NƯỚC MỸ LO',true,38,83),B=strip('HẾT TIỀN',true,64,84),L=strip('BỆ TƯỢNG ĐANG XÂY, 1885',false,24,85);const tk=el(g,'g',{});
 return{upd:t=>{const e=inn(t,R(8)-.2,.6);c1.at(400,620,-2,1,e);c1.zoom(1+.12*inn(t,R(8),E(8)-R(8)),.5,.4);const w=AT(8,'bệ',1.2),u=inn(t,w-.1,.6);c2.at(830,830,3,.9+.1*u,u);sh(L,t,400,330,-1,e);sh(A,t,540,1085,-1,PV(t,8,'phải',.5));sh(B,t,540,1200,2,PV(t,8,'thì',5.0))}}});
// 9: Joseph Pulitzer kêu gọi quyên góp (ts9)
S2(9,9,'d',null,g=>{const c=card('ts9',IMG+'ts9.jpg',520,640,91);const rg=ring(c.top,-.25*c.w,.33*c.h,.11*c.h,'#d8372d');const A=strip('JOSEPH PULITZER',true,40,92),B=strip('HỨA ĐĂNG TÊN',false,44,93),C=strip('TỪNG NGƯỜI ỦNG HỘ',false,38,94),L=strip('TRANG HARPER\'S WEEKLY',false,24,95);
 return{upd:t=>{const e=inn(t,R(9)-.2,.6);c.at(310,660,-2,1,e);c.zoom(1+.12*inn(t,R(9),E(9)-R(9)),.5,.5);rg.set(inn(t,AT(9,'Joseph',.3)+.2,.9));sh(A,t,780,540,3,PV(t,9,'Joseph',.3));sh(B,t,780,690,-2,PV(t,9,'hứa',3.0));sh(C,t,780,820,2,PV(t,9,'từng',3.8));sh(L,t,310,340,-1,e)}}});
// 10: lớp đồng mỏng, gió làm tượng lắc (ts10)
S2(10,10,'p',null,g=>{const c=card('ts10',IMG+'ts10.jpg',760,600,101);const S=[['ĐỒNG DÀY 2,4 MM','dày',290,1070,true],['GIÓ 80 KM/GIỜ','Gió',790,1070,false],['TƯỢNG LẮC 7 CM','tượng',290,1180,false],['ĐUỐC LẮC 13 CM','đuốc',790,1180,true]];const sg=S.map((a,i)=>strip(a[0],a[4],32,111+i));const L=strip('KHUNG BÊN TRONG TƯỢNG',false,24,115);
 return{upd:t=>{const e=inn(t,R(10)-.2,.6);c.at(540,630,2,1,e);c.zoom(1+.12*inn(t,R(10),E(10)-R(10)),.5,.5);sh(L,t,540,320,-1,e);S.forEach((a,i)=>sh(sg[i],t,a[2],a[3],(i%2?2:-2),PV(t,10,a[1],1.5+i*2.2)))}}});
// 11: khánh thành 28/10/1886 (ts11)
S2(11,11,'d',t=>'1886',g=>{const c=card('ts11',IMG+'ts11.jpg',520,640,121);const A=strip('KHÁNH THÀNH',true,54,122),B=strip('28 THÁNG 10',false,56,123),L=strip('NEW YORK EVENING POST',false,24,124);
 return{upd:t=>{const e=inn(t,R(11)-.2,.6);c.at(310,660,-3,1,e);c.zoom(1+.14*inn(t,R(11),E(11)-R(11)),.5,.2);sh(L,t,310,340,-1,e);sh(A,t,780,640,3,PV(t,11,'khánh',.8));sh(B,t,780,790,-2,PV(t,11,'hai',2.0))}}});
// 12: câu hỏi cuối
S2(12,12,'d',null,g=>{const rg=[0,1,2].map(()=>el(g,'circle',{fill:'none',stroke:'#f2c14e','stroke-width':5}));const q=T(g,0,0,'?',340,'#e5483f',18,'middle',DK);const cr=crown(g);const A=strip('VÌ SAO QUÀ KỶ NIỆM THÀNH BIỂU TƯỢNG?',true,32,131),B=strip('BẠN NGHĨ SAO?',false,52,132);
 return{upd:t=>{const e=inn(t,R(12)-.2,.7);rg.forEach((r2,i)=>{const u=((t-R(12)-i*.9)*.4)%1;r2.setAttribute('cx',540);r2.setAttribute('cy',640);r2.setAttribute('r',240+Math.max(0,u)*240);r2.setAttribute('opacity',(1-Math.max(0,u))*.5*e)});const qp=popv(t,R(12)+.3);q.setAttribute('transform',`translate(540,690) rotate(-8) scale(${qp*(.92+.08*Math.sin(t*4))})`);q.setAttribute('opacity',qp>0?1:0);PUT(cr,860,1160,popv(t,R(12)+.8,.5),.7,6);sh(A,t,540,1030,-1,PV(t,12,'Bạn',.2));sh(B,t,540,1160,1,PV(t,12,'Bạn',3.6))}}},TOTAL);
sx(R(1)+.1,'whoosh',{d:.5,g:.5});
bm(R(1)+.3);bm(R(2)+.3,1);bm(AT(3,'Laboulaye',3.6),1);bm(R(4)+.3,1);bm(R(5)+.3,1);bm(AT(6,'chính',3.4));bm(AT(7,'hai',4.4),1);bm(R(8)+.3,1);bm(R(9)+.3,1);bm(R(10)+.3,1);bm(R(11)+.3);bm(R(12)+.3);
sx(R(12)+.3,'question',{g:.7});
