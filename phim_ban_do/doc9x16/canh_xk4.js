// ===== Hồ Nguyên Trừng (xk4). Ảnh: hd1(1) hd2(2) hd3(3) hd4(4) hd7(7) hd9(9). Cảnh 5, 6, 8, 10, 11 vẽ phẳng.
const HB=[];const bm=(t,l)=>{sx(t,'boom',l?{light:true,g:.8}:{g:1});if(!l)HB.push(t)};
const PUT=(o,x,y,u,sc=1,rot=0)=>{o.setAttribute('transform',`translate(${x},${y}) rotate(${rot}) scale(${Math.max(.001,u)*sc})`);o.setAttribute('opacity',u>0?1:0)};
const gun=(g,len=1,col='#3a3732')=>{const k=el(g,'g',{});el(k,'rect',{x:-120*len,y:-26,width:240*len,height:52,rx:24,fill:col,stroke:'#fff','stroke-width':7});el(k,'rect',{x:70*len,y:-34,width:34,height:68,rx:10,fill:'#4b463e',stroke:'#fff','stroke-width':6});el(k,'circle',{cx:-124*len,cy:0,r:12,fill:'#17120c'});return k};
const man=(g,col='#f5efe0')=>{const k=el(g,'g',{});el(k,'circle',{cx:0,cy:-52,r:22,fill:col,stroke:'#17120c','stroke-width':6});el(k,'path',{d:'M-26 40 L-20 -22 L20 -22 L26 40Z',fill:col,stroke:'#17120c','stroke-width':6,'stroke-linejoin':'round'});return k};
// 1: mở đầu (hd1 thành nhà Hồ)
S2(1,1,'d',null,g=>{const c=card('hd1',IMG+'hd1.jpg',900,600,11);const A=strip('SÚNG THẦN CƠ',true,56,12),B=strip('CON TRAI HỒ QUÝ LY',false,40,13),C=strip('THÀNH NHÀ HỒ · THANH HÓA',false,26,14);
 return{upd:t=>{const e=inn(t,R(1)-.2,.6);c.at(540,640,-2,1,e);c.zoom(1+.1*inn(t,R(1),E(1)-R(1)),.5,.5);sh(C,t,540,338,-1,e);sh(A,t,540,1085,-1,PV(t,1,'súng',3.4));sh(B,t,540,1195,1,PV(t,1,'con',1.2))}}});
// 2: Hồ Nguyên Trừng, cha là Hồ Quý Ly, người lập nhà Hồ (hd2 Cổng Nam)
S2(2,2,'p',null,g=>{const c=card('hd2',IMG+'hd2.jpg',900,600,21);const A=strip('HỒ NGUYÊN TRỪNG',true,50,22),B=strip('CHA: HỒ QUÝ LY',false,46,23),C=strip('NGƯỜI LẬP RA NHÀ HỒ',true,38,24),L=strip('CỔNG NAM THÀNH NHÀ HỒ',false,26,25);
 return{upd:t=>{const e=inn(t,R(2)-.2,.6);c.at(540,640,2,1,e);c.zoom(1+.12*inn(t,R(2),E(2)-R(2)),.5,.5);sh(L,t,540,338,-1,e);sh(A,t,540,1085,-1,PV(t,2,'Hồ',1.0));sh(B,t,540,1190,-2,PV(t,2,'Cha',2.6));sh(C,t,540,1290,2,PV(t,2,'người',5.0))}}});
// 3: Tả Tướng quốc (hd3 Cổng Bắc)
S2(3,3,'d',null,g=>{const c=card('hd3',IMG+'hd3.jpg',900,600,31);const A=strip('HỒ HÁN THƯƠNG LÀM VUA',false,38,32),B=strip('TẢ TƯỚNG QUỐC',true,56,33),C=strip('CHỨC RẤT CAO TRONG TRIỀU',false,34,34),L=strip('CỔNG BẮC THÀNH NHÀ HỒ',false,26,35);
 return{upd:t=>{const e=inn(t,R(3)-.2,.6);c.at(540,640,-2,1,e);c.zoom(1+.12*inn(t,R(3),E(3)-R(3)),.5,.5);sh(L,t,540,338,-1,e);sh(A,t,540,1065,-1,PV(t,3,'em',.4));sh(B,t,540,1165,1,PV(t,3,'Tả',4.5));sh(C,t,540,1260,-1,PV(t,3,'một',8.0,0))}}});
// 4: Binh chế khí, ba loại súng thần cơ (hd4: ảnh minh họa, sách thần khí phổ)
S2(4,4,'p',null,g=>{const c=card('hd4',IMG+'hd4.jpg',900,600,41);const L=strip('ẢNH MINH HỌA: SÁCH THẦN KHÍ PHỔ',false,26,42),A=strip('BINH CHẾ KHÍ · MINH SỬ',true,40,43),B=strip('BA LOẠI SÚNG THẦN CƠ',false,46,44);
 return{upd:t=>{const e=inn(t,R(4)-.2,.6);c.at(540,600,2,1,e);c.zoom(1+.12*inn(t,R(4),E(4)-R(4)),.5,.5);sh(L,t,540,338,-1,e);sh(A,t,380,1085,-1,PV(t,4,'Binh',3.8));sh(B,t,540,1215,1,PV(t,4,'ba',6.0))}}});
// 5: ba loại súng: lưng voi, hai người khiêng, một người vác (vẽ phẳng, ba hàng)
S2(5,5,'d',null,g=>{const G=[0,1,2].map(i=>gun(g,[1.0,.9,.7][i]));const M=[man(el(g,'g',{})),man(el(g,'g',{})),man(el(g,'g',{}))];
 const lab=[['LỚN: TRÊN LƯNG VOI','Loại',true],['VỪA: HAI NGƯỜI KHIÊNG','vừa',false],['NHỎ: MỘT NGƯỜI VÁC','nhỏ',true]];const sg=lab.map((a,i)=>strip(a[0],a[2],30,51+i));
 const ele=el(g,'g',{});el(ele,'ellipse',{cx:0,cy:30,rx:190,ry:90,fill:'#8c8c92',stroke:'#fff','stroke-width':8});[-110,-45,45,110].forEach(x=>el(ele,'rect',{x:x-24,y:70,width:48,height:90,rx:18,fill:'#7a7a80',stroke:'#fff','stroke-width':6}));el(ele,'path',{d:'M175 -10 Q250 -20 250 70 Q250 140 215 150',fill:'none',stroke:'#fff','stroke-width':34,'stroke-linecap':'round'});el(ele,'path',{d:'M175 -10 Q250 -20 250 70 Q250 140 215 150',fill:'none',stroke:'#8c8c92','stroke-width':22,'stroke-linecap':'round'});
 return{upd:t=>{const w0=AT(5,'Loại',.3),w1=AT(5,'vừa',3.0),w2=AT(5,'nhỏ',6.2);const u0=popv(t,w0,.5),u1=popv(t,w1,.5),u2=popv(t,w2,.5);
  PUT(ele,290,520,u0,.7);PUT(G[0],290,462,u0,.55,-8);PUT(G[1],290,820,u1,.6);PUT(M[0],120,830,u1,.8);PUT(M[1],470,830,u1,.8);PUT(G[2],270,1120,u2,.55);PUT(M[2],480,1110,u2,.9);
  sh(sg[0],t,790,470,-1,PV(t,5,'Loại',.3));sh(sg[1],t,790,830,1,PV(t,5,'vừa',3.0));sh(sg[2],t,790,1120,-1,PV(t,5,'nhỏ',6.2))}}});
// 6: 1407 nhà Hồ thua, bị đưa về Nam Kinh (vẽ phẳng, trục di chuyển)
S2(6,6,'d',t=>'1407',g=>{const ln=el(g,'path',{d:'M180 760 L900 760',stroke:'#17120c','stroke-width':10,'stroke-linecap':'round','stroke-dasharray':'28 22'});const d1=el(g,'circle',{cx:180,cy:760,r:28,fill:'#d8372d',stroke:'#fff','stroke-width':8}),d2=el(g,'circle',{cx:900,cy:760,r:28,fill:'#d9a441',stroke:'#fff','stroke-width':8});const k=man(el(g,'g',{}),'#d8372d');
 const A=strip('NHÀ HỒ THUA QUÂN MINH',true,40,61),B=strip('ĐẠI NGU',false,38,62),C=strip('NAM KINH',false,38,63),D=strip('BỊ BẮT, ĐƯA VỀ NAM KINH',true,38,64);
 return{upd:t=>{sh(A,t,540,420,-2,PV(t,6,'nhà',.2));sh(B,t,230,860,-2,inn(t,R(6)+.3,.4));sh(C,t,850,860,2,popv(t,AT(6,'Nam',5.0)-.3,.4));const w=AT(6,'bị',3.0),u=inn(t,w,E(6)-w-.6);d1.setAttribute('r',28*popv(t,R(6)+.2,.4));d2.setAttribute('r',28*popv(t,w,.4));PUT(k,180+u*720,700,popv(t,R(6)+.3,.4),1.5,0);sh(D,t,540,1090,1,PV(t,6,'bị',3.0))}}});
// 7: nhà Minh tha tội, dùng tài chế súng (hd7: ảnh minh họa)
S2(7,7,'p',null,g=>{const c=card('hd7',IMG+'hd7.jpg',420,660,71);const L=strip('ẢNH MINH HỌA: SÚNG THỜI MINH',false,24,72),A=strip('NHÀ MINH THA TỘI',true,48,73),B=strip('DÙNG TÀI CHẾ SÚNG',false,44,74);const tk=tickMark(g,820,900,80,'#2e9e5f');
 return{upd:t=>{const e=inn(t,R(7)-.2,.6);c.at(310,650,-3,1,e);c.zoom(1+.1*inn(t,R(7),E(7)-R(7)),.5,.4);sh(L,t,310,338,-1,e);sh(A,t,780,540,2,PV(t,7,'tha',1.0));sh(B,t,780,690,-2,PV(t,7,'dùng',2.4));tk.set(inn(t,AT(7,'tha',1.0)+.8,.4))}}});
// 8: 1445 thượng thư bộ Công (vẽ phẳng, ấn)
S2(8,8,'d',t=>'1445',g=>{const sl=el(g,'g',{});el(sl,'rect',{x:-150,y:-150,width:300,height:300,rx:26,fill:'#c8372d',stroke:'#fff','stroke-width':10});const tx=T(sl,0,-20,'CÔNG',80,'#fbe9c9',0,'middle','none');tx.setAttribute('stroke','none');const tb=T(sl,0,95,'BỘ',70,'#fbe9c9',0,'middle','none');tb.setAttribute('stroke','none');
 const st=el(g,'g',{});const rk=[['THƯỢNG THƯ','#d8372d'],['THỊ LANG','#d9a441'],['LANG TRUNG','#6f9a86']].map((a,i)=>{const b=el(g,'g',{});el(b,'rect',{x:-190,y:-30,width:380,height:60,rx:30,fill:a[1],stroke:'#fff','stroke-width':6});const tt=T(b,0,12,a[0],32,'#fff',0,'middle','none');tt.setAttribute('stroke','none');return b});
 const A=strip('XÂY DỰNG VÀ CHẾ TẠO',false,40,81),B=strip('THƯỢNG THƯ BỘ CÔNG',true,44,82);
 return{upd:t=>{const e=popv(t,R(8)+.1,.6);PUT(sl,320,640,e,1.1,-4);const w=AT(8,'Thượng',4.0);rk.forEach((b,i)=>PUT(b,790,820-i*130,popv(t,w-1.0+i*.5,.4),1,i%2?1:-1));
  sh(A,t,540,1085,-1,PV(t,8,'quan',9.0));sh(B,t,540,1195,1,PV(t,8,'Thượng',4.0))}}});
// 9: cha đẻ súng thần công (hd9: ảnh minh họa)
S2(9,9,'d',null,g=>{const c=card('hd9',IMG+'hd9.jpg',900,560,91);const L=strip('ẢNH MINH HỌA: SÚNG BA NÒNG THỜI MINH',false,26,92),A=strip('CHA ĐẺ SÚNG THẦN CÔNG',true,46,93),B=strip('TRUNG QUỐC',false,52,94),C=strip('THEO BÁO ĐẠI BIỂU NHÂN DÂN',false,28,95);
 return{upd:t=>{const e=inn(t,R(9)-.2,.6);c.at(540,630,2,1,e);c.zoom(1+.14*inn(t,R(9),E(9)-R(9)),.5,.5);sh(L,t,540,338,-1,e);sh(C,t,540,1010,1,PV(t,9,'Theo',.2));sh(A,t,540,1110,-1,PV(t,9,'cha',2.6));sh(B,t,540,1215,1,PV(t,9,'Trung',3.8))}}});
// 10: mất 1446, Nam Ông mộng lục (vẽ phẳng, cuộn sách)
S2(10,10,'p',t=>'1446',g=>{const bk=el(g,'g',{});el(bk,'rect',{x:-190,y:-250,width:380,height:500,rx:16,fill:'#efe3c5',stroke:'#17120c','stroke-width':10});el(bk,'rect',{x:-190,y:-250,width:60,height:500,rx:12,fill:'#8a5a2e',stroke:'#17120c','stroke-width':8});for(let i=0;i<7;i++)el(bk,'path',{d:`M-90 ${-170+i*55} L150 ${-170+i*55}`,stroke:'#8d7a52','stroke-width':6,'stroke-linecap':'round'});
 const cs=el(g,'g',{});el(cs,'path',{d:'M-50 -70 Q-90 -20 -50 40 M50 -70 Q90 -20 50 40',fill:'none',stroke:'#fff','stroke-width':10,'stroke-linecap':'round'});
 const A=strip('NAM ÔNG MỘNG LỤC',true,44,101),B=strip('TẬP VĂN XUÔI ÔNG ĐỂ LẠI',false,36,102),C=strip('MẤT NĂM 1446',false,44,103);
 return{upd:t=>{const e=popv(t,R(10)+.1,.6);PUT(bk,320,660,e,1,-3);cs.setAttribute('opacity',0);sh(C,t,780,520,3,PV(t,10,'mất',.2));const w=AT(10,'Nam',5.4);sh(A,t,540,1085,-1,PV(t,10,'Nam',5.4));sh(B,t,540,1195,1,PV(t,10,'tập',4.6));
  const q=popv(t,AT(10,'Ngoài',3.2),.5);const gn=PUT;}}});
// 11: câu hỏi cuối
S2(11,11,'d',null,g=>{const rg=[0,1,2].map(()=>el(g,'circle',{fill:'none',stroke:'#f2c14e','stroke-width':5}));const q=T(g,0,0,'?',340,'#e5483f',18,'middle',DK);const k=gun(g,.8);const A=strip('NÊN NHỚ ÔNG THẾ NÀO?',true,50,111),B=strip('GIÚP NƯỚC MÌNH RỒI GIÚP NƯỚC ĐÁNH BẠI MÌNH',false,26,112);
 return{upd:t=>{const e=inn(t,R(11)-.2,.7);rg.forEach((r2,i)=>{const u=((t-R(11)-i*.9)*.4)%1;r2.setAttribute('cx',540);r2.setAttribute('cy',640);r2.setAttribute('r',240+Math.max(0,u)*240);r2.setAttribute('opacity',(1-Math.max(0,u))*.5*e)});const qp=popv(t,R(11)+.3);q.setAttribute('transform',`translate(540,690) rotate(-8) scale(${qp*(.92+.08*Math.sin(t*4))})`);q.setAttribute('opacity',qp>0?1:0);PUT(k,540,1090,popv(t,R(11)+.8,.5),.6,-8);sh(A,t,540,1000,-1,PV(t,11,'Bạn',3.6));sh(B,t,540,1215,1,PV(t,11,'Một',.2))}}},TOTAL);
sx(R(1)+.1,'whoosh',{d:.5,g:.5});
bm(R(1)+.3);bm(R(2)+.3,1);bm(R(3)+.3,1);bm(R(4)+.3,1);bm(AT(5,'Loại',.3),1);bm(R(6)+.3);bm(R(7)+.3,1);bm(AT(8,'Thượng',4.0));bm(R(9)+.3,1);bm(R(10)+.3,1);bm(R(11)+.3);
sx(R(11)+.3,'question',{g:.7});
