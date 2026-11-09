// ===== Chùa Cầu Hội An (xk5). Ảnh: ha1 ha2 ha4 ha5 ha6 ha7 ha8 ha9 ha10 ha11 ha13 (cảnh 1,2,4–11,13). Cảnh 3, 12, 14 vẽ phẳng.
const HB=[];const bm=(t,l)=>{sx(t,'boom',l?{light:true,g:.8}:{g:1});if(!l)HB.push(t)};
const PUT=(o,x,y,u,sc=1,rot=0)=>{o.setAttribute('transform',`translate(${x},${y}) rotate(${rot}) scale(${Math.max(.001,u)*sc})`);o.setAttribute('opacity',u>0?1:0)};
// 1: mở đầu: cầu trên tờ 20.000đ (ha1)
S2(1,1,'d',null,g=>{const c=card('ha1',IMG+'ha1.jpg',900,600,11);const A=strip('CẦU TRÊN TỜ 20.000Đ',true,52,12),B=strip('CÓ MÁI CHE · CÓ CHÙA TRÊN CẦU',false,32,13);
 return{upd:t=>{const e=inn(t,R(1)-.2,.6);c.at(540,640,-2,1,e);c.zoom(1+.1*inn(t,R(1),E(1)-R(1)),.5,.5);sh(A,t,540,1085,-1,PV(t,1,'cây',.6));sh(B,t,540,1195,1,PV(t,1,'mái',3.6))}}});
// 2: phố cổ Hội An (ha2)
S2(2,2,'p',null,g=>{const c=card('ha2',IMG+'ha2.jpg',900,640,21);const A=strip('PHỐ CỔ HỘI AN',true,56,22),B=strip('MIỀN TRUNG VIỆT NAM',false,44,23);
 return{upd:t=>{const e=inn(t,R(2)-.2,.6);c.at(540,650,2,1,e);c.zoom(1+.12*inn(t,R(2),E(2)-R(2)),.5,.5);sh(A,t,540,1085,-1,PV(t,2,'phố',1.4));sh(B,t,540,1195,1,PV(t,2,'miền',2.6))}}});
// 3: 1992 lý lịch di tích (vẽ phẳng)
S2(3,3,'d',t=>'1992',g=>{const pg=el(g,'g',{});el(pg,'rect',{x:-250,y:-300,width:500,height:600,rx:20,fill:'#efe3c5',stroke:'#17120c','stroke-width':10});const h=T(pg,0,-220,'LÝ LỊCH DI TÍCH',46,'#17120c',0,'middle','none');h.setAttribute('stroke','none');for(let i=0;i<6;i++)el(pg,'path',{d:`M-190 ${-130+i*65} L190 ${-130+i*65}`,stroke:'#8d7a52','stroke-width':6,'stroke-linecap':'round'});
 const S=stamp('1992',90);const A=strip('BAN QUẢN LÝ DI TÍCH HỘI AN',true,32,31),B=strip('LẬP LÝ LỊCH CỦA CẦU',false,44,32);
 return{upd:t=>{const e=popv(t,R(3)+.1,.6);PUT(pg,540,660,e,1,-2);const u=popv(t,AT(3,'năm',5.0),.5);S.at(640,860,-8,Math.max(.001,u),u>0?1:0);sh(A,t,540,1090,-1,PV(t,3,'Ban',.2));sh(B,t,540,1200,1,PV(t,3,'lập',2.6))}}});
// 4: cuối thế kỷ 16, đầu thế kỷ 17 (ha4)
S2(4,4,'p',null,g=>{const c=card('ha4',IMG+'ha4.jpg',900,600,41);const A=strip('CẦU ĐƯỢC LÀM',false,44,42),B=strip('CUỐI THẾ KỶ 16 · ĐẦU THẾ KỶ 17',true,36,43);
 return{upd:t=>{const e=inn(t,R(4)-.2,.6);c.at(540,640,-2,1,e);c.zoom(1+.12*inn(t,R(4),E(4)-R(4)),.5,.5);sh(A,t,540,1085,-1,PV(t,4,'cầu',2.0));sh(B,t,540,1195,1,PV(t,4,'cuối',3.6))}}});
// 5: thương nhân Nhật bỏ vốn, thợ mộc Hội An thi công (ha5: tư liệu thuyền chu ấn)
S2(5,5,'d',null,g=>{const c=card('ha5',IMG+'ha5.jpg',700,600,51);const L=strip('THUYỀN CHU ẤN · TƯ LIỆU NHẬT BẢN',false,24,52),A=strip('NHẬT BẢN: BỎ VỐN, THIẾT KẾ',true,34,53),B=strip('THỢ MỘC HỘI AN: THI CÔNG',false,34,54);
 return{upd:t=>{const e=inn(t,R(5)-.2,.6);c.at(540,650,-2,1,e);c.zoom(1+.12*inn(t,R(5),E(5)-R(5)),.5,.5);sh(L,t,540,338,1,e);sh(A,t,540,1085,-1,PV(t,5,'Nhật',.3));sh(B,t,540,1195,1,PV(t,5,'thợ',3.6))}}});
// 6: 1653 người Hoa tiếp quản, nối thêm gian nhô ra (ha6)
S2(6,6,'p',t=>'1653',g=>{const c=card('ha6',IMG+'ha6.jpg',900,600,61);const rg=ring(c.top,.02*c.w,-.02*c.h,.2*c.h,'#d8372d');const A=strip('NGƯỜI NHẬT RỜI HỘI AN',false,36,62),B=strip('NGƯỜI HOA TIẾP QUẢN CẦU',true,38,63),C=strip('NỐI THÊM MỘT GIAN',false,44,64);
 return{upd:t=>{const e=inn(t,R(6)-.2,.6);c.at(540,640,2,1,e);c.zoom(1+.12*inn(t,R(6),E(6)-R(6)),.5,.5);rg.set(inn(t,AT(6,'nối',6.4),.9));sh(A,t,540,1060,-1,PV(t,6,'sau',1.8));sh(B,t,540,1160,1,PV(t,6,'người',3.0,0));sh(C,t,540,1260,-1,PV(t,6,'nối',6.4))}}});
// 7: chùa Cầu (ha7)
S2(7,7,'d',null,g=>{const c=card('ha7',IMG+'ha7.jpg',900,620,71);const A=strip('CHÙA CẦU',true,70,72),B=strip('TÊN DÂN GỌI',false,44,73);
 return{upd:t=>{const e=inn(t,R(7)-.2,.6);c.at(540,640,-2,1,e);c.zoom(1+.14*inn(t,R(7),E(7)-R(7)),.5,.5);sh(A,t,540,1085,-1,PV(t,7,'chùa',2.2));sh(B,t,540,1195,1,PV(t,7,'dân',.8))}}});
// 8: 1719 Lai Viễn Kiều (ha8)
S2(8,8,'p',t=>'1719',g=>{const c=card('ha8',IMG+'ha8.jpg',900,600,81);const A=strip('CHÚA NGUYỄN PHÚC CHU',false,36,82),B=strip('LAI VIỄN KIỀU',true,62,83),C=strip('CẦU ĐÓN KHÁCH PHƯƠNG XA',false,38,84);
 return{upd:t=>{const e=inn(t,R(8)-.2,.6);c.at(540,630,2,1,e);c.zoom(1+.12*inn(t,R(8),E(8)-R(8)),.5,.5);sh(A,t,540,1040,-1,PV(t,8,'chúa',.8));sh(B,t,540,1150,1,PV(t,8,'Lai',3.0));sh(C,t,540,1255,-1,PV(t,8,'nghĩa',5.4))}}});
// 9: thương cảng nhỏ, thế kỷ 15 đến 19 (ha9: ảnh minh họa sông Thu Bồn)
S2(9,9,'d',null,g=>{const c=card('ha9',IMG+'ha9.jpg',460,640,91);const L=strip('ẢNH MINH HỌA: SÔNG THU BỒN NGÀY NAY',false,24,92),A=strip('THEO UNESCO',false,40,93),B=strip('THƯƠNG CẢNG NHỎ',true,40,94),C=strip('THẾ KỶ 15 → 19',true,44,95);
 return{upd:t=>{const e=inn(t,R(9)-.2,.6);c.at(300,650,-3,1,e);c.zoom(1+.12*inn(t,R(9),E(9)-R(9)),.5,.5);sh(L,t,540,338,-1,e);sh(A,t,780,520,3,PV(t,9,'UNESCO',.5));sh(B,t,780,670,-2,PV(t,9,'thương',1.2));sh(C,t,780,820,2,PV(t,9,'thế',3.2))}}});
// 10: ảnh hưởng người Hoa, người Nhật, châu Âu (ha10: Hội quán Phúc Kiến)
S2(10,10,'p',null,g=>{const c=card('ha10',IMG+'ha10.jpg',460,640,101);const L=strip('HỘI QUÁN PHÚC KIẾN',false,26,102),A=strip('NGƯỜI HOA',true,46,103),B=strip('NGƯỜI NHẬT',false,46,104),C=strip('CHÂU ÂU (VỀ SAU)',true,38,105);
 return{upd:t=>{const e=inn(t,R(10)-.2,.6);c.at(310,650,3,1,e);c.zoom(1+.12*inn(t,R(10),E(10)-R(10)),.5,.5);sh(L,t,310,338,-1,e);sh(A,t,790,560,3,PV(t,10,'Hoa',2.8));sh(B,t,790,700,-2,PV(t,10,'Nhật',3.8));sh(C,t,790,840,2,PV(t,10,'châu',6.0))}}});
// 11: suy giảm cuối thế kỷ 19, phố cổ nguyên vẹn (ha11)
S2(11,11,'d',null,g=>{const c=card('ha11',IMG+'ha11.jpg',900,620,111);const A=strip('SUY GIẢM CUỐI THẾ KỶ 19',false,38,112),B=strip('PHỐ CỔ GIỮ NGUYÊN VẸN',true,44,113);
 return{upd:t=>{const e=inn(t,R(11)-.2,.6);c.at(540,640,-2,1,e);c.zoom(1+.12*inn(t,R(11),E(11)-R(11)),.5,.5);sh(A,t,540,1085,-1,PV(t,11,'suy',2.4));sh(B,t,540,1195,1,PV(t,11,'giữ',6.0))}}});
// 12: 1999 di sản thế giới (vẽ phẳng)
S2(12,12,'p',t=>'1999',g=>{const S=stamp('UNESCO',96);const L=['DI SẢN THẾ GIỚI','KHU ĐÔ THỊ CỔ','HỘI AN'],W=['Di','khu','Hội'];const ls=L.map((s,i)=>strip(s,i==0,46,121+i));const tk=L.map((s,i)=>tickMark(g,150,780+i*130,64));
 return{upd:t=>{const u=popv(t,AT(12,'UNESCO',1.4),.5);S.at(540,520,-4,Math.max(.001,u),u>0?1:0);L.forEach((s,i)=>{const w=AT(12,W[i],2.6+i*.9);sh(ls[i],t,570,780+i*130,(i-1)*1.5,popv(t,w,.45));tk[i].set(inn(t,w+.4,.4))})}}});
// 13: ví dụ bảo tồn đặc biệt tốt (ha13)
S2(13,13,'p',null,g=>{const c=card('ha13',IMG+'ha13.jpg',900,560,131);const A=strip('BẢO TỒN ĐẶC BIỆT TỐT',true,44,132),B=strip('THƯƠNG CẢNG TRUYỀN THỐNG',false,36,133),C=strip('Ở CHÂU Á',false,44,134);
 return{upd:t=>{const e=inn(t,R(13)-.2,.6);c.at(540,620,2,1,e);c.zoom(1+.12*inn(t,R(13),E(13)-R(13)),.5,.5);sh(A,t,540,1040,-1,PV(t,13,'bảo',4.0));sh(B,t,540,1145,1,PV(t,13,'thương',5.8));sh(C,t,540,1245,-1,PV(t,13,'châu',7.0))}}});
// 14: câu hỏi cuối
S2(14,14,'d',null,g=>{const rg=[0,1,2].map(()=>el(g,'circle',{fill:'none',stroke:'#f2c14e','stroke-width':5}));const q=T(g,0,0,'?',340,'#e5483f',18,'middle',DK);const A=strip('VÌ SAO MỘT CẢNG NHỎ ĐỂ LẠI DẤU ẤN NHIỀU NƯỚC?',true,28,141),B=strip('BẠN THỬ ĐOÁN XEM',false,52,142);
 return{upd:t=>{const e=inn(t,R(14)-.2,.7);rg.forEach((r2,i)=>{const u=((t-R(14)-i*.9)*.4)%1;r2.setAttribute('cx',540);r2.setAttribute('cy',640);r2.setAttribute('r',240+Math.max(0,u)*240);r2.setAttribute('opacity',(1-Math.max(0,u))*.5*e)});const qp=popv(t,R(14)+.3);q.setAttribute('transform',`translate(540,690) rotate(-8) scale(${qp*(.92+.08*Math.sin(t*4))})`);q.setAttribute('opacity',qp>0?1:0);sh(A,t,540,1030,-1,PV(t,14,'Vì',.2));sh(B,t,540,1160,1,PV(t,14,'Bạn',4.2))}}},TOTAL);
sx(R(1)+.1,'whoosh',{d:.5,g:.5});
bm(R(1)+.3);bm(R(2)+.3,1);bm(AT(3,'năm',5.0),1);bm(R(4)+.3,1);bm(R(5)+.3,1);bm(R(6)+.3,1);bm(R(7)+.3);bm(R(8)+.3,1);bm(R(9)+.3,1);bm(R(10)+.3,1);bm(R(11)+.3,1);bm(AT(12,'UNESCO',1.4));bm(R(13)+.3,1);bm(R(14)+.3);
sx(R(14)+.3,'question',{g:.7});
