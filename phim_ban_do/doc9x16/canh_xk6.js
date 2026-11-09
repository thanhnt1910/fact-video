// ===== Phiến đá Rosetta (xk6). Ảnh: rs1 rs2 rs5(3) rs3(4) rs6(6) rs7(7) rs10(10) rs11(11) rs13(12) rs12(13). Cảnh 5, 8, 9, 14 vẽ phẳng.
const HB=[];const bm=(t,l)=>{sx(t,'boom',l?{light:true,g:.8}:{g:1});if(!l)HB.push(t)};
const PUT=(o,x,y,u,sc=1,rot=0)=>{o.setAttribute('transform',`translate(${x},${y}) rotate(${rot}) scale(${Math.max(.001,u)*sc})`);o.setAttribute('opacity',u>0?1:0)};
const stoneD=(g,col='#6e6a64')=>{const k=el(g,'g',{});el(k,'path',{d:'M-110 150 L-135 -40 L-70 -150 L40 -165 L125 -90 L110 150Z',fill:col,stroke:'#fff','stroke-width':8,'stroke-linejoin':'round'});[-95,-60,-25,10,45,80,115].forEach(y=>el(k,'path',{d:`M-90 ${y} L90 ${y}`,stroke:'#cfc9bd',opacity:.55,'stroke-width':5,'stroke-linecap':'round','stroke-dasharray':'14 8'}));return k};
const shipD=(g)=>{const k=el(g,'g',{});for(let i=0;i<3;i++)el(k,'path',{d:`M${-130+i*10} ${88+i*14} Q${-80+i*10} ${66+i*14} ${-30+i*10} ${88+i*14} T${70+i*10} ${88+i*14} T${130+i*10} ${88+i*14}`,fill:'none',stroke:'#6fb3e0','stroke-width':7,'stroke-linecap':'round'});
 el(k,'path',{d:'M-120 18 L120 18 L74 74 L-74 74Z',fill:'#7a5a3a',stroke:'#fff','stroke-width':7,'stroke-linejoin':'round'});el(k,'path',{d:'M0 -110 L0 18',stroke:'#fff','stroke-width':12});el(k,'path',{d:'M8 -100 L8 8 L84 8Z',fill:'#efe9d8',stroke:'#fff','stroke-width':5,'stroke-linejoin':'round'});el(k,'path',{d:'M-8 -88 L-8 8 L-66 8Z',fill:'#e0b84a',stroke:'#fff','stroke-width':5,'stroke-linejoin':'round'});return k};
// 1: mở đầu: pháo đài Julien 1799 (rs1)
S2(1,1,'d',t=>'1799',g=>{const c=card('rs1',IMG+'rs1.jpg',900,520,11);const A=strip('TẢNG ĐÁ LÍNH PHÁP ĐÀO ĐƯỢC',true,38,12),B=strip('CHÌA KHÓA ĐỌC CHỮ AI CẬP CỔ',false,36,13),L=strip('PHÁO ĐÀI JULIEN (TRANH)',false,26,14);
 return{upd:t=>{const e=inn(t,R(1)-.2,.6);c.at(540,630,-2,1,e);c.zoom(1+.1*inn(t,R(1),E(1)-R(1)),.5,.5);sh(L,t,540,338,-1,e);sh(A,t,540,1085,-1,PV(t,1,'tảng',.6));sh(B,t,540,1195,1,PV(t,1,'chìa',6.0))}}});
// 2: Bouchard, Rashid (rs2)
S2(2,2,'p',null,g=>{const c=card('rs2',IMG+'rs2.jpg',900,600,21);const A=strip('PIERRE-FRANÇOIS BOUCHARD',true,38,22),B=strip('RASHID · ROSETTA',false,46,23),C=strip('CHÂU THỔ SÔNG NILE',false,40,24),L=strip('PHÁO ĐÀI Ở RASHID NGÀY NAY',false,26,25);
 return{upd:t=>{const e=inn(t,R(2)-.2,.6);c.at(540,630,2,1,e);c.zoom(1+.12*inn(t,R(2),E(2)-R(2)),.5,.5);sh(L,t,540,338,1,e);sh(A,t,540,1060,-1,PV(t,2,'Pierre',2.2));sh(B,t,540,1160,1,PV(t,2,'Rashid',6.0));sh(C,t,540,1255,-1,PV(t,2,'châu',9.0))}}});
// 3: sắc lệnh ở Memphis, năm 196 trước Công nguyên (rs5)
S2(3,3,'d',t=>'196 TCN',g=>{const c=card('rs5',IMG+'rs5.jpg',760,640,31);const A=strip('SẮC LỆNH CỦA HỘI NGHỊ THẦY TẾ',true,34,32),B=strip('THÀNH MEMPHIS',false,50,33);
 return{upd:t=>{const e=inn(t,R(3)-.2,.6);c.at(540,640,-2,1,e);c.zoom(1+.12*inn(t,R(3),E(3)-R(3)),.5,.5);sh(A,t,540,1085,-1,PV(t,3,'sắc',2.0));sh(B,t,540,1195,1,PV(t,3,'Memphis',5.2))}}});
// 4: một nội dung khắc ba lần bằng ba loại chữ (rs3)
S2(4,4,'p',null,g=>{const c=card('rs3',IMG+'rs3.jpg',500,640,41);const L=['TRÊN: CHỮ TƯỢNG HÌNH','GIỮA: CHỮ DEMOTIC','DƯỚI: CHỮ HY LẠP'],W=['tượng','Demotic','Hy'];const ls=L.map((s,i)=>strip(s,i==0,30,42+i));const A=strip('MỘT NỘI DUNG · KHẮC BA LẦN',true,38,45);
 return{upd:t=>{const e=inn(t,R(4)-.2,.6);c.at(300,650,-3,1,e);c.zoom(1+.12*inn(t,R(4),E(4)-R(4)),.5,.5);L.forEach((s,i)=>sh(ls[i],t,780,470+i*150,(i-1)*2,PV(t,4,W[i],3.0+i*1.8)));sh(A,t,540,1215,-1,PV(t,4,'Cùng',.3))}}});
// 5: chữ Demotic hằng ngày, chữ Hy Lạp của bộ máy cai trị (vẽ phẳng)
S2(5,5,'d',null,g=>{const bx=[0,1].map(i=>{const b=el(g,'g',{});el(b,'rect',{x:-210,y:-230,width:420,height:460,rx:30,fill:['#efe3c5','#dfe8f0'][i],stroke:'#17120c','stroke-width':9});const tt=T(b,0,-90,['DEMOTIC','HY LẠP'][i],54,'#17120c',0,'middle','none');tt.setAttribute('stroke','none');if(i){const sym=T(b,0,70,'Ω',150,'#17120c',0,'middle','none');sym.setAttribute('stroke','none')}else el(b,'path',{d:'M-120 40 C-90 -30 -60 110 -30 20 S30 -20 60 50 S100 0 120 30 M-120 110 C-80 70 -50 150 0 100 S80 80 120 120',fill:'none',stroke:'#17120c','stroke-width':12,'stroke-linecap':'round'});return b});
 const A=strip('CHỮ DÙNG HẰNG NGÀY',true,36,51),B=strip('NGÔN NGỮ BỘ MÁY CAI TRỊ',false,34,52),L=strip('THEO BẢO TÀNG ANH',false,28,53);
 return{upd:t=>{const a=popv(t,R(5)+.1,.6),b=popv(t,AT(5,'Còn',3.4),.6);PUT(bx[0],290,640,a,1,-3);PUT(bx[1],790,640,b,1,3);sh(L,t,540,340,-1,a);sh(A,t,290,1060,-2,PV(t,5,'chữ',1.4));sh(B,t,790,1180,2,PV(t,5,'ngôn',5.0))}}});
// 6: chữ tượng hình không còn dùng từ sau thế kỷ 4 (rs6: ảnh minh họa)
S2(6,6,'p',null,g=>{const c=card('rs6',IMG+'rs6.jpg',460,640,61);const L=strip('ẢNH MINH HỌA: CHỮ TƯỢNG HÌNH',false,24,62),A=strip('KHÔNG CÒN ĐƯỢC DÙNG',true,38,63),B=strip('TỪ SAU THẾ KỶ 4',false,44,64),C=strip('KHÔNG AI ĐỌC ĐƯỢC',true,40,65);
 return{upd:t=>{const e=inn(t,R(6)-.2,.6);c.at(300,650,-3,1,e);c.zoom(1+.12*inn(t,R(6),E(6)-R(6)),.5,.5);sh(L,t,300,338,-1,e);sh(A,t,790,520,3,PV(t,6,'đã',1.8));sh(B,t,790,670,-2,PV(t,6,'từ',3.2));sh(C,t,790,830,2,PV(t,6,'không',6.0))}}});
// 7: chữ Hy Lạp làm chìa khóa (rs7: bản dập)
S2(7,7,'d',null,g=>{const c=card('rs7',IMG+'rs7.jpg',460,640,71);const L=strip('BẢN DẬP PHIẾN ĐÁ',false,26,72),A=strip('ĐỌC ĐƯỢC CHỮ HY LẠP',true,36,73),B=strip('LÀM CHÌA KHÓA',false,46,74),C=strip('ĐỌC HAI LOẠI CÒN LẠI',true,36,75);
 return{upd:t=>{const e=inn(t,R(7)-.2,.6);c.at(300,650,3,1,e);c.zoom(1+.12*inn(t,R(7),E(7)-R(7)),.5,.5);sh(L,t,300,338,-1,e);sh(A,t,790,520,3,PV(t,7,'học',.2));sh(B,t,790,670,-2,PV(t,7,'chìa',4.2));sh(C,t,790,830,2,PV(t,7,'hai',5.4))}}});
// 8: 1801 quân Anh lấy tảng đá theo điều khoản đầu hàng (vẽ phẳng)
S2(8,8,'d',t=>'1801',g=>{const b1=el(g,'g',{}),b2=el(g,'g',{});[b1,b2].forEach((b,i)=>{el(b,'rect',{x:-150,y:-70,width:300,height:140,rx:24,fill:i?'#2f5d8c':'#c8372d',stroke:'#fff','stroke-width':8});const tt=T(b,0,18,i?'QUÂN ANH':'QUÂN PHÁP',40,'#fff',0,'middle','none');tt.setAttribute('stroke','none')});const st=stoneD(g);const ar=el(g,'path',{d:'M290 700 L790 700',stroke:'#f2c14e','stroke-width':10,'stroke-dasharray':'22 16','stroke-linecap':'round',pathLength:1,'stroke-dashoffset':0});
 const A=strip('ĐIỀU KHOẢN ĐẦU HÀNG',true,42,81),B=strip('QUÂN ANH LẤY TẢNG ĐÁ',false,40,82);
 return{upd:t=>{const e=popv(t,R(8)+.1,.6);PUT(b1,290,520,e,1);PUT(b2,790,520,popv(t,R(8)+.4,.6),1);const w=AT(8,'theo',2.6),u=inn(t,w-.5,1.6);PUT(st,290+u*500,790,popv(t,R(8)+.5,.5),.8,-4+8*u);ar.setAttribute('opacity',inn(t,R(8)+.6,.5)*.7);sh(A,t,540,1085,-1,PV(t,8,'theo',2.6));sh(B,t,540,1195,1,PV(t,8,'lấy',.9))}}});
// 9: tới cảng Portsmouth tháng 2 năm 1802 (vẽ phẳng)
S2(9,9,'p',t=>'1802',g=>{const sp=shipD(el(g,'g',{}));const k=el(g,'g',{});el(k,'rect',{x:-260,y:-250,width:520,height:500,rx:28,fill:'#f5efe0',stroke:'#17120c','stroke-width':10});el(k,'path',{d:'M-260 -190 L-260 -222 Q-260 -250 -232 -250 L232 -250 Q260 -250 260 -222 L260 -190Z',fill:'#d8372d'});const h=T(k,0,-204,'THÁNG 2 · 1802',42,'#fff',0,'middle','none');h.setAttribute('stroke','none');const d=T(k,0,70,'2',300,'#17120c',0,'middle','none');d.setAttribute('stroke','none');
 const A=strip('CẢNG PORTSMOUTH',true,50,91),B=strip('TẢNG ĐÁ ĐẾN ANH',false,46,92);
 return{upd:t=>{const e=popv(t,R(9)+.1,.6);PUT(k,540,600,e,.95,-2);const w=AT(9,'tới',.5),u=inn(t,w,2.0);const sk=el;PUT(sp,160+u*0,1010,popv(t,R(9)+.3,.5),1.0,-2);sp.setAttribute('transform',`translate(${160+u*660},1030) rotate(${-2+4*Math.sin(t*3)}) scale(.95)`);sp.setAttribute('opacity',e>0?1:0);sh(A,t,540,1165,-1,PV(t,9,'cảng',1.4));sh(B,t,540,1265,1,PV(t,9,'tới',.5))}}});
// 10: vào Bảo tàng Anh (rs10)
S2(10,10,'p',null,g=>{const c=card('rs10',IMG+'rs10.jpg',440,640,101);const L=strip('BẢO TÀNG ANH',false,28,102),A=strip('CHUYỂN VÀO BẢO TÀNG ANH',true,32,103),B=strip('VẪN NẰM Ở ĐÓ ĐẾN NAY',false,34,104);
 return{upd:t=>{const e=inn(t,R(10)-.2,.6);c.at(300,650,-3,1,e);c.zoom(1+.12*inn(t,R(10),E(10)-R(10)),.5,.5);sh(L,t,300,338,-1,e);sh(A,t,790,560,3,PV(t,10,'chuyển',1.4));sh(B,t,790,720,-2,PV(t,10,'vẫn',4.6))}}});
// 11: 1814 Thomas Young (rs11: thư 1818)
S2(11,11,'d',t=>'1814',g=>{const c=card('rs11',IMG+'rs11.jpg',460,640,111);const L=strip('THƯ CỦA YOUNG, 1818',false,24,112),A=strip('THOMAS YOUNG',true,46,113),B=strip('MỘT SỐ KÝ TỰ GHI ÂM THANH',false,28,114);
 return{upd:t=>{const e=inn(t,R(11)-.2,.6);c.at(300,650,-3,1,e);c.zoom(1+.12*inn(t,R(11),E(11)-R(11)),.5,.5);sh(L,t,300,338,-1,e);sh(A,t,790,540,3,PV(t,11,'Thomas',1.6));sh(B,t,780,700,-2,PV(t,11,'nhận',3.2))}}});
// 12: 1822 Champollion công bố bảng chữ cái ghi âm (rs13: thư gửi Dacier)
S2(12,12,'p',t=>'1822',g=>{const c=card('rs13',IMG+'rs13.jpg',460,640,121);const L=strip('THƯ GỬI DACIER, 1822',false,24,122),A=strip('JEAN-FRANÇOIS CHAMPOLLION',true,26,123),B=strip('BẢNG CHỮ CÁI GHI ÂM',false,40,124);
 return{upd:t=>{const e=inn(t,R(12)-.2,.6);c.at(300,650,3,1,e);c.zoom(1+.12*inn(t,R(12),E(12)-R(12)),.5,.5);sh(L,t,300,338,-1,e);sh(A,t,780,540,3,PV(t,12,'Jean',1.6));sh(B,t,780,700,-2,PV(t,12,'công',4.0))}}});
// 13: từ đó đọc được chữ Ai Cập cổ (rs12: bàn của Champollion)
S2(13,13,'d',null,g=>{const c=card('rs12',IMG+'rs12.jpg',900,560,131);const L=strip('BÀN LÀM VIỆC CỦA CHAMPOLLION',false,26,132),A=strip('TỪ ĐÓ',false,44,133),B=strip('ĐỌC ĐƯỢC CHỮ AI CẬP CỔ',true,44,134);
 return{upd:t=>{const e=inn(t,R(13)-.2,.6);c.at(540,640,-2,1,e);c.zoom(1+.12*inn(t,R(13),E(13)-R(13)),.5,.5);sh(L,t,540,338,-1,e);sh(A,t,540,1085,-1,PV(t,13,'Từ',.2));sh(B,t,540,1195,1,PV(t,13,'người',1.4))}}});
// 14: kích thước phiến đá + câu hỏi cuối (vẽ phẳng)
S2(14,14,'d',null,g=>{const st=stoneD(g);const n1=bigNum(g,'0',120,'#f2c14e'),n2=bigNum(g,'0',120,'#ff8a5c');const l1=strip('CAO (MÉT)',false,30,141),l2=strip('NẶNG (KG)',false,30,142);const q=T(g,0,0,'?',260,'#e5483f',16,'middle',DK);const A=strip('CÒN BAO NHIÊU CHỮ CỔ CHƯA AI ĐỌC ĐƯỢC?',true,30,143);
 return{upd:t=>{const e=popv(t,R(14)+.1,.6);PUT(st,300,640,e,1.5,-3);const w1=AT(14,'cao',.4),w2=AT(14,'nặng',3.4);const u1=inn(t,w1,1.4),u2=inn(t,w2,1.6);n1.textContent=(1.12*u1).toFixed(2).replace('.',',');n2.textContent=String(Math.round(760*u2));
  n1.setAttribute('transform',`translate(780,520) rotate(-3) scale(${t>w1-.2?1:.001})`);n2.setAttribute('transform',`translate(780,820) rotate(3) scale(${t>w2-.2?1:.001})`);sh(l1,t,780,590,-1,inn(t,w1,.4));sh(l2,t,780,890,1,inn(t,w2,.4));
  const qp=popv(t,AT(14,'Bạn',7.0),.5);q.setAttribute('transform',`translate(540,1130) rotate(-8) scale(${Math.max(.001,qp)})`);q.setAttribute('opacity',qp>0?1:0);sh(A,t,540,1255,-1,PV(t,14,'Bạn',7.0))}}},TOTAL);
sx(R(1)+.1,'whoosh',{d:.5,g:.5});
bm(R(1)+.3);bm(R(2)+.3,1);bm(R(3)+.3,1);bm(R(4)+.3,1);bm(R(5)+.3,1);bm(R(6)+.3,1);bm(R(7)+.3);bm(R(8)+.3,1);bm(R(9)+.3,1);bm(R(10)+.3,1);bm(R(11)+.3,1);bm(R(12)+.3);bm(R(13)+.3,1);bm(R(14)+.3);
sx(R(14)+.3,'question',{g:.7});
