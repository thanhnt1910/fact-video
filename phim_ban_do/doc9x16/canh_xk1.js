// ===== Cửu đỉnh ở Huế (xk1). Ảnh mỗi cái một lần: cd1(1) cd2(2) cd3(3) cd5(5) cd6(6) cd7(7) cd11+cd8(8) cd12+cd9(9) cd15(12). Cảnh 4,10,11,13,14,15 vẽ phẳng.
const HB=[];const bm=(t,l)=>{sx(t,'boom',l?{light:true,g:.8}:{g:1});if(!l)HB.push(t)};
// đỉnh đồng vẽ phẳng: miệng, thân, hai quai, ba chân
const urnD=(g,col='#6f9a86')=>{const k=el(g,'g',{});
 [[-60,40,-82,150],[60,40,82,150],[0,52,0,160]].forEach(([x1,y1,x2,y2])=>{el(k,'path',{d:`M${x1} ${y1} L${x2} ${y2}`,stroke:'#fff','stroke-width':30,'stroke-linecap':'round'});el(k,'path',{d:`M${x1} ${y1} L${x2} ${y2}`,stroke:'#33463d','stroke-width':20,'stroke-linecap':'round'})});
 [-72,72].forEach(x=>{el(k,'path',{d:`M${x} -64 L${x} -128 L${x+(x<0?30:-30)} -128`,fill:'none',stroke:'#fff','stroke-width':22,'stroke-linecap':'round','stroke-linejoin':'round'});el(k,'path',{d:`M${x} -64 L${x} -128 L${x+(x<0?30:-30)} -128`,fill:'none',stroke:'#33463d','stroke-width':12,'stroke-linecap':'round','stroke-linejoin':'round'})});
 el(k,'path',{d:'M-104 -58 Q-134 30 -66 74 L66 74 Q134 30 104 -58Z',fill:col,stroke:'#fff','stroke-width':8,'stroke-linejoin':'round'});
 el(k,'rect',{x:-112,y:-82,width:224,height:32,rx:14,fill:'#85b49f',stroke:'#fff','stroke-width':7});
 el(k,'path',{d:'M-62 -4 Q0 22 62 -4',fill:'none',stroke:'#33463d','stroke-width':7,'stroke-linecap':'round'});return k};
const sunD=(g,r=44)=>{const k=el(g,'g',{});for(let i=0;i<12;i++){const a=i*Math.PI/6;el(k,'path',{d:`M${Math.cos(a)*r*1.25} ${Math.sin(a)*r*1.25} L${Math.cos(a)*r*1.75} ${Math.sin(a)*r*1.75}`,stroke:'#f2c14e','stroke-width':9,'stroke-linecap':'round'})}el(k,'circle',{r,fill:'#f2c14e',stroke:'#fff','stroke-width':7});return k};
const ico=(g,kind)=>{const k=el(g,'g',{});const dk='#2f2a24',W2='#fff';
 if(kind=='cannon'){el(k,'g',{transform:'rotate(-14)'}).innerHTML='<rect x="-120" y="-34" width="200" height="56" rx="26" fill="#3a3732" stroke="#fff" stroke-width="7"/><rect x="60" y="-42" width="40" height="72" rx="10" fill="#4b463e" stroke="#fff" stroke-width="7"/>';
  el(k,'circle',{cx:-20,cy:54,r:58,fill:'#7a5a3a',stroke:'#fff','stroke-width':7});[0,1,2,3].forEach(i=>{const a=i*Math.PI/4;el(k,'path',{d:`M${-20+Math.cos(a)*58} ${54+Math.sin(a)*58} L${-20-Math.cos(a)*58} ${54-Math.sin(a)*58}`,stroke:'#fff','stroke-width':5})});el(k,'circle',{cx:-20,cy:54,r:12,fill:'#33281c',stroke:'#fff','stroke-width':4})}
 if(kind=='musket'){el(k,'g',{transform:'rotate(-14)'}).innerHTML='<rect x="-60" y="-14" width="210" height="20" rx="8" fill="#3a3732" stroke="#fff" stroke-width="6"/><path d="M-60 -18 L-130 20 L-132 46 L-60 12Z" fill="#7a5a3a" stroke="#fff" stroke-width="6" stroke-linejoin="round"/><circle cx="168" cy="-8" r="16" fill="#f2c14e" stroke="#fff" stroke-width="4"/>'}
 if(kind=='crossbow'){el(k,'path',{d:'M-110 -20 Q0 -130 110 -20',fill:'none',stroke:'#fff','stroke-width':22,'stroke-linecap':'round'});el(k,'path',{d:'M-110 -20 Q0 -130 110 -20',fill:'none',stroke:'#7a5a3a','stroke-width':12,'stroke-linecap':'round'});el(k,'path',{d:'M-110 -20 L0 40 L110 -20',fill:'none',stroke:'#fff','stroke-width':6});
  el(k,'rect',{x:-14,y:-76,width:28,height:170,rx:8,fill:'#7a5a3a',stroke:'#fff','stroke-width':6});el(k,'path',{d:'M0 -120 L0 20 M-14 -102 L0 -122 L14 -102',fill:'none',stroke:'#d8372d','stroke-width':7,'stroke-linecap':'round','stroke-linejoin':'round'})}
 if(kind=='ship'){for(let i=0;i<3;i++)el(k,'path',{d:`M${-130+i*10} ${88+i*14} Q${-80+i*10} ${66+i*14} ${-30+i*10} ${88+i*14} T${70+i*10} ${88+i*14} T${130+i*10} ${88+i*14}`,fill:'none',stroke:'#6fb3e0','stroke-width':7,'stroke-linecap':'round'});
  el(k,'path',{d:'M-120 18 L120 18 L74 74 L-74 74Z',fill:'#7a5a3a',stroke:'#fff','stroke-width':7,'stroke-linejoin':'round'});el(k,'path',{d:'M0 -110 L0 18',stroke:'#fff','stroke-width':12});el(k,'path',{d:'M8 -100 L8 8 L84 8Z',fill:'#efe9d8',stroke:'#fff','stroke-width':5,'stroke-linejoin':'round'});el(k,'path',{d:'M-8 -88 L-8 8 L-66 8Z',fill:'#e0b84a',stroke:'#fff','stroke-width':5,'stroke-linejoin':'round'})}
 return k};
const PUT=(o,x,y,u,sc=1,rot=0)=>{o.setAttribute('transform',`translate(${x},${y}) rotate(${rot}) scale(${Math.max(.001,u)*sc})`);o.setAttribute('opacity',u>0?1:0)};
// 1: mở đầu (cd1) + chín chiếc đỉnh hiện dần
S2(1,1,'d',null,g=>{const c=card('cd1',IMG+'cd1.jpg',400,600,11);const row=[...Array(9)].map(()=>{const k=el(g,'g',{});urnD(k);return k});
 const A=strip('CỬU ĐỈNH · HUẾ',true,56,12),B=strip('NÚI SÔNG · CÂY CỎ · MUÔNG THÚ',false,32,13),S=stamp('UNESCO',64);
 return{upd:t=>{const e=inn(t,R(1)-.2,.6);c.at(330,700,-2,1,e);c.zoom(1+.12*inn(t,R(1),E(1)-R(1)),.5,.3);const w=AT(1,'chín',.6);
  sh(A,t,760,520,3,PV(t,1,'chín',.6));row.forEach((k,i)=>PUT(k,130+i*100,1215,popv(t,w+.12*i,.4),.32));
  sh(B,t,540,1085,-1,PV(t,1,'khắc',2.2));const u=popv(t,AT(1,'UNESCO',5.4),.5);S.at(760,780,-6,Math.max(.001,u),u>0?1:0)}}});
// 2: Cửu đỉnh trước sân Thế Miếu (cd2)
S2(2,2,'p',null,g=>{const c=card('cd2',IMG+'cd2.jpg',900,600,21);const rg=ring(c.top,0,-.1*c.h,.17*c.h,'#d8372d');const A=strip('CỬU ĐỈNH',true,54,22),B=strip('SÂN THẾ MIẾU · HUẾ',false,38,23);
 return{upd:t=>{const e=inn(t,R(2)-.2,.6);c.at(540,660,2,1,e);c.zoom(1+.16*inn(t,R(2),E(2)-R(2)),.5,.4);rg.set(inn(t,AT(2,'Cửu',.5),1.0));sh(A,t,360,1070,-3,PV(t,2,'Cửu',.5));sh(B,t,690,1180,2,PV(t,2,'Thế',2.0))}}});
// 3: Minh Mạng khởi đúc 1835 (cd3, bản vẽ tư liệu)
S2(3,3,'d',t=>'1835',g=>{const c=card('cd3',IMG+'cd3.jpg',880,610,31);const L=strip('BẢN VẼ TƯ LIỆU',false,28,32),A=strip('VUA MINH MẠNG',true,52,33),B=strip('BẮT ĐẦU ĐÚC',false,52,34);
 return{upd:t=>{const e=inn(t,R(3)-.2,.6);c.at(540,690,-2,1,e);c.zoom(1+.14*inn(t,R(3),E(3)-R(3)),.5,.5);sh(L,t,340,340,-2,e);sh(A,t,540,1070,-2,PV(t,3,'Minh',2.3));sh(B,t,540,1190,2,PV(t,3,'bắt',4.4))}}});
// 4: kéo dài đến 1837 (trục thời gian, đỉnh đi qua)
S2(4,4,'p',t=>'1837',g=>{const ln=el(g,'path',{d:'M180 800 L900 800',stroke:'#17120c','stroke-width':10,'stroke-linecap':'round',pathLength:1,'stroke-dasharray':'1 1','stroke-dashoffset':1});const d1=el(g,'circle',{cx:180,cy:800,r:26,fill:'#d8372d',stroke:'#fff','stroke-width':8}),d2=el(g,'circle',{cx:900,cy:800,r:26,fill:'#d9a441',stroke:'#fff','stroke-width':8});
 const k=el(g,'g',{});urnD(k);const A=strip('THEO NHIỀU NGUỒN',true,48,41),y1=strip('1835',true,54,42),y2=strip('1837',true,54,43),B=strip('VIỆC LÀM KÉO DÀI',false,42,44);const tk=tickMark(g,900,950,70,'#2e9e5f');
 return{upd:t=>{sh(A,t,540,470,-2,PV(t,4,'nhiều',.3));const t0=AT(4,'kéo',2.0),u=inn(t,t0,E(4)-t0-.5);ln.setAttribute('stroke-dashoffset',1-inn(t,R(4)+.2,.6));d1.setAttribute('r',26*popv(t,R(4)+.2,.4));d2.setAttribute('r',26*popv(t,t0+.6,.4));
  PUT(k,180+u*720,680,inn(t,t0-.1,.3),.5);sh(y1,t,180,910,-3,inn(t,R(4)+.3,.4));sh(y2,t,900,910,3,popv(t,AT(4,'bảy',3.2)-.5,.4));sh(B,t,540,1120,1,PV(t,4,'kéo',2.0));tk.set(inn(t,AT(4,'bảy',3.2),.4))}}});
// 5: chín tên riêng (cd5)
S2(5,5,'d',null,g=>{const c=card('cd5',IMG+'cd5.jpg',880,660,51);const nm=['Cao','Nhân','Chương','Anh','Nghị','Thuần','Tuyên','Dụ','Huyền'];const tg=nm.map((s,i)=>strip(s.toUpperCase(),i%2==0,46,52+i));
 return{upd:t=>{const e=inn(t,R(5)-.2,.6);c.at(540,640,-2,1,e);c.zoom(1+.12*inn(t,R(5),E(5)-R(5)),.5,.5);nm.forEach((s,i)=>sh(tg[i],t,230+(i%3)*310,1060+Math.floor(i/3)*88,(i%3-1)*2,PV(t,5,s,1.6+i*.5)))}}});
// 6: miếu hiệu (cd6, án thờ vua Gia Long)
S2(6,6,'p',null,g=>{const c=card('cd6',IMG+'cd6.jpg',400,533,61);const A=strip('MIẾU HIỆU',true,56,62),B=strip('TÊN GỌI KHI THỜ VUA',false,34,63),C=strip('MỖI TÊN · MỘT VỊ VUA',true,36,64),D=strip('ÁN THỜ VUA GIA LONG, HUẾ',false,26,65);
 return{upd:t=>{const e=inn(t,R(6)-.2,.6);c.at(310,700,-2,1,e);c.zoom(1+.14*inn(t,R(6),E(6)-R(6)),.5,.4);sh(A,t,780,540,3,PV(t,6,'miếu',2.4));sh(B,t,780,670,-2,PV(t,6,'thờ',4.6));sh(C,t,780,800,2,PV(t,6,'vị',3.4));sh(D,t,310,1040,-1,inn(t,R(6)+.5,.4))}}});
// 7: 18 hình mỗi đỉnh, ba tầng, 162 hình (cd7)
S2(7,7,'d',null,g=>{const c=card('cd7',IMG+'cd7.jpg',420,560,71);const n=bigNum(g,'0',210,'#f2c14e');const A=strip('HÌNH CHẠM NỔI',true,46,72),B=strip('TỔNG CỘNG',false,40,73);const bars=[0,1,2].map(i=>{const b=el(g,'g',{});el(b,'rect',{x:-150,y:-24,width:300,height:48,rx:24,fill:['#d8372d','#d9a441','#6f9a86'][i],stroke:'#fff','stroke-width':6});const tt=T(b,0,12,'TẦNG '+(i+1),30,'#fff',0,'middle','none');tt.setAttribute('stroke','none');return b});
 return{upd:t=>{const e=inn(t,R(7)-.2,.6);c.at(310,700,-2,1,e);c.zoom(1+.12*inn(t,R(7),E(7)-R(7)),.5,.4);const w1=AT(7,'mười',1.8),w3=AT(7,'tầng',4.0),w4=AT(7,'Tổng',5.2);const u1=inn(t,w1,1.0),u4=inn(t,w4,1.4);const v=t<w4?Math.round(u1*18):Math.round(18+u4*144);
  n.textContent=String(v);n.setAttribute('fill',t<w4?'#f2c14e':'#ff8a5c');n.setAttribute('transform',`translate(800,600) rotate(-4) scale(${t>w1-.2?1:.001})`);sh(A,t,800,730,2,inn(t,w1+.3,.4));bars.forEach((b,i)=>PUT(b,800,850+i*66,popv(t,w3+i*.3,.4),1,i%2?1:-1));sh(B,t,800,1090,-2,PV(t,7,'Tổng',5.2))}}});
// 8: mặt trời mặt trăng, núi, sông (cd11 + cd8)
S2(8,8,'p',null,g=>{const c1=card('cd11',IMG+'cd11.jpg',380,475,81),c2=card('cd8',IMG+'cd8.jpg',440,330,82);const sun=sunD(g,34);const A=strip('MẶT TRỜI · MẶT TRĂNG · SAO',true,38,83),B=strip('NÚI · SÔNG HƯƠNG · SÔNG HỒNG · BẠCH ĐẰNG',false,28,84),L=strip('HẢI VÂN QUAN',false,28,85);
 return{upd:t=>{const e=inn(t,R(8)-.2,.6);c1.at(290,650,-3,1,e);c1.zoom(1+.14*inn(t,R(8),E(8)-R(8)),.5,.4);const w=AT(8,'núi',3.6),u=inn(t,w-.3,.6);c2.at(790,800,3,.9+.1*u,u);c2.zoom(1+.14*inn(t,w,E(8)-w),.5,.5);
  const su=popv(t,AT(8,'mặt',.7),.5);PUT(sun,880,440,su,1,t*40);sh(A,t,540,1085,-1,PV(t,8,'mặt',.7,.1));sh(L,t,790,590,2,u);sh(B,t,540,1190,1,PV(t,8,'núi',3.6))}}});
// 9: cây cỏ và muông thú (cd12 + cd9)
S2(9,9,'d',null,g=>{const c1=card('cd12',IMG+'cd12.jpg',500,375,91),c2=card('cd9',IMG+'cd9.jpg',380,476,92);const A=strip('LÚA · SEN · QUẾ · VẢI THIỀU',true,36,93);const an=[['VOI','voi',120],['HỔ','hổ',280],['RÙA','rùa',430],['CHIM CÔNG','chim',650],['CÁ SẤU','cá',915]];const tg=an.map((a,i)=>strip(a[0],i%2==0,38,94+i));
 return{upd:t=>{const e=inn(t,R(9)-.2,.6);c1.at(300,600,-3,1,e);c1.zoom(1+.14*inn(t,R(9),E(9)-R(9)),.5,.4);const w=AT(9,'voi',4.4),u=inn(t,w-.4,.6);c2.at(790,830,3,.9+.1*u,u);c2.zoom(1+.14*inn(t,w,E(9)-w),.5,.5);
  sh(A,t,540,335,-1,PV(t,9,'cây',.3));an.forEach((a,i)=>sh(tg[i],t,a[2],1180,(i-2)*1.4,PV(t,9,a[1],w-R(9)+i*.5)))}}});
// 10: vũ khí và thuyền (vẽ phẳng)
S2(10,10,'p',null,g=>{const it=[['cannon','ĐẠI PHÁO','đại',300,570],['musket','SÚNG ĐIỂU THƯƠNG','súng',780,570],['crossbow','NỎ','nỏ',300,940],['ship','THUYỀN CHIẾN · THUYỀN BIỂN','thuyền',780,940]];const ic=it.map(a=>{const k=el(g,'g',{});ico(k,a[0]);return k});const lb=it.map((a,i)=>strip(a[1],i%2==0,a[1].length>20?26:34,101+i));
 return{upd:t=>{it.forEach((a,i)=>{const w=AT(10,a[2],1.0+i*1.4),u=popv(t,w,.5);PUT(ic[i],a[3],a[4],u,1.25,(i%2?3:-3));sh(lb[i],t,a[3],a[4]+190,(i%2?2:-2),popv(t,w+.15,.4))})}}});
// 11: tượng trưng (đỉnh vẽ to, bốn chữ)
S2(11,11,'d',null,g=>{const k=el(g,'g',{});urnD(k);const ST=[['THÀNH CÔNG','thành',310,470,true],['TRƯỜNG TỒN','trường',770,470,false],['GIÀU CÓ','giàu',310,1120,false],['THỐNG NHẤT','thống',770,1120,true]];const sg=ST.map((a,i)=>strip(a[0],a[4],44,111+i));const A=strip('PHAN THANH HẢI · BÁO VĂN HÓA',false,28,115);const ring2=[0,1].map(()=>el(g,'circle',{fill:'none',stroke:'#f2c14e','stroke-width':5}));
 return{upd:t=>{const e=popv(t,R(11)+.1,.6);PUT(k,540,800,e,2.3);sh(A,t,540,335,-1,PV(t,11,'Phan',.4));ST.forEach((a,i)=>sh(sg[i],t,a[2],a[3],(i%2?2:-2),PV(t,11,a[1],1.5+i*.9)));
  ring2.forEach((r,i)=>{const u=((t-R(11)-i*1.1)*.35)%1;r.setAttribute('cx',540);r.setAttribute('cy',800);r.setAttribute('r',230+Math.max(0,u)*220);r.setAttribute('opacity',(1-Math.max(0,u))*.45*e)})}}});
// 12: bách khoa thư bằng đồng (cd15)
S2(12,12,'p',null,g=>{const c=card('cd15',IMG+'cd15.jpg',920,611,121);const A=strip('BÁCH KHOA THƯ BẰNG ĐỒNG',true,46,122),B=strip('ĐẦU THẾ KỶ 19',false,44,123);
 return{upd:t=>{const e=inn(t,R(12)-.2,.6);c.at(540,680,2,1,e);c.zoom(1+.3*inn(t,R(12),E(12)-R(12)),.3,.5);sh(A,t,540,1085,-1,PV(t,12,'bách',2.3));sh(B,t,540,1195,2,PV(t,12,'đầu',4.2))}}});
// 13: ngày 8 tháng 5 năm 2024 (tờ lịch vẽ)
S2(13,13,'d',t=>'2024',g=>{const pg=el(g,'g',{});el(pg,'rect',{x:-260,y:-290,width:520,height:580,rx:30,fill:'#f5efe0',stroke:'#17120c','stroke-width':10});el(pg,'path',{d:'M-260 -230 L-260 -260 Q-260 -290 -230 -290 L230 -290 Q260 -290 260 -260 L260 -230Z',fill:'#d8372d'});const h=T(pg,0,-244,'THÁNG 5 · 2024',44,'#fff',0,'middle','none');h.setAttribute('stroke','none');const d=T(pg,0,100,'8',340,'#17120c',0,'middle','none');d.setAttribute('stroke','none');
 const S=stamp('ĐƯỢC GHI DANH',58),B=strip('CÁC BẢN ĐÚC NỔI TRÊN CỬU ĐỈNH',false,30,131);
 return{upd:t=>{const e=popv(t,R(13)+.1,.6);PUT(pg,540,650,e,1,-2);const u=popv(t,AT(13,'ghi',4.0),.5);S.at(640,860,-8,Math.max(.001,u),u>0?1:0);sh(B,t,540,1130,1,PV(t,13,'bản',2.8))}}});
// 14: Di sản tư liệu khu vực châu Á và Thái Bình Dương
S2(14,14,'p',null,g=>{const S=stamp('UNESCO',92);const L=['DI SẢN TƯ LIỆU','KHU VỰC CHÂU Á','VÀ THÁI BÌNH DƯƠNG'],W=['Di','khu','Thái'];const ls=L.map((s,i)=>strip(s,i==0,46,141+i));const tk=L.map((s,i)=>tickMark(g,150,780+i*130,64));
 return{upd:t=>{const u=popv(t,AT(14,'UNESCO',3.1),.5);S.at(540,520,-4,Math.max(.001,u),u>0?1:0);L.forEach((s,i)=>{const w=AT(14,W[i],.2+i*1.0);sh(ls[i],t,570,780+i*130,(i-1)*1.5,popv(t,w,.45));tk[i].set(inn(t,w+.4,.4))})}}});
// 15: câu hỏi cuối
S2(15,15,'d',null,g=>{const rg=[0,1,2].map(()=>el(g,'circle',{fill:'none',stroke:'#f2c14e','stroke-width':5}));const q=T(g,0,0,'?',340,'#e5483f',18,'middle',DK);const k=el(g,'g',{});urnD(k);const A=strip('VÌ SAO KHẮC CẢ ĐẤT NƯỚC LÊN ĐỒNG?',true,38,151),B=strip('BẠN NGHĨ SAO?',false,52,152);
 return{upd:t=>{const e=inn(t,R(15)-.2,.7);rg.forEach((r2,i)=>{const u=((t-R(15)-i*.9)*.4)%1;r2.setAttribute('cx',540);r2.setAttribute('cy',640);r2.setAttribute('r',240+Math.max(0,u)*240);r2.setAttribute('opacity',(1-Math.max(0,u))*.5*e)});const qp=popv(t,R(15)+.3);q.setAttribute('transform',`translate(540,690) rotate(-8) scale(${qp*(.92+.08*Math.sin(t*4))})`);q.setAttribute('opacity',qp>0?1:0);PUT(k,880,1180,popv(t,R(15)+.8,.5),.6,6);sh(A,t,540,1030,-1,PV(t,15,'Vì',.2));sh(B,t,540,1160,1,PV(t,15,'Bạn',3.6))}}},TOTAL);
sx(R(1)+.1,'whoosh',{d:.5,g:.5});
bm(R(1)+.3);bm(AT(1,'UNESCO',5.4));bm(R(2)+.3,1);bm(AT(3,'bắt',4.4));bm(R(4)+.3,1);bm(AT(5,'Cao',1.6));bm(R(6)+.3,1);bm(AT(7,'Tổng',5.2));bm(R(8)+.3,1);bm(R(9)+.3,1);
bm(AT(10,'đại',1.0),1);bm(AT(11,'thống',4.8));bm(R(12)+.3,1);bm(AT(13,'ghi',4.0));bm(AT(14,'UNESCO',3.1));bm(R(15)+.3);
sx(R(15)+.3,'question',{g:.7});
