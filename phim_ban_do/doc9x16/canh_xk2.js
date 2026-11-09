// ===== Dấu $ (xk2). Ảnh: ds1(1) ds3(3) ds4(4) ds5(5) ds6(6) ds7(7) ds8(8) ds10(10). Cảnh 2, 9, 11 vẽ phẳng.
const HB=[];const bm=(t,l)=>{sx(t,'boom',l?{light:true,g:.8}:{g:1});if(!l)HB.push(t)};
const dol=(g,size=300,col='#f2c14e')=>{const t=T(g,0,0,'$',size,col,16,'middle',DK);return t};
// 1: mở đầu: ký hiệu tiền các nước (ds1) + dấu $ nảy lên + câu hỏi
S2(1,1,'d',null,g=>{const c=card('ds1',IMG+'ds1.jpg',900,600,11);const q=dol(g,260);const A=strip('DẤU $ AI VẼ RA?',true,56,12),B=strip('TRƯỚC CẢ KHI MỸ CÓ ĐÔ LA',false,34,13);
 return{upd:t=>{const e=inn(t,R(1)-.2,.6);c.at(540,640,-2,1,e);c.zoom(1+.1*inn(t,R(1),E(1)-R(1)),.5,.5);const u=popv(t,AT(1,'ký',1.2),.5);q.setAttribute('transform',`translate(800,520) rotate(-8) scale(${Math.max(.001,u)*(.95+.05*Math.sin(t*4))})`);q.setAttribute('opacity',u>0?1:0);
  sh(A,t,540,1085,-1,PV(t,1,'ký',1.2));sh(B,t,540,1195,1,PV(t,1,'trước',3.0))}}});
// 2: những năm 1770, chữ viết tay của thương nhân (trang sổ vẽ phẳng, dấu $ được viết ra)
S2(2,2,'p',t=>'1770',g=>{const pg=el(g,'g',{});el(pg,'rect',{x:-330,y:-330,width:660,height:660,rx:24,fill:'#efe3c5',stroke:'#17120c','stroke-width':10});for(let i=0;i<7;i++)el(pg,'path',{d:`M-280 ${-230+i*80} L280 ${-230+i*80}`,stroke:'#b9a57a','stroke-width':4});
 const pen=el(pg,'path',{d:'M60 -100 C-80 -150 -110 -40 0 -10 C110 20 90 130 -60 100 M0 -190 L0 190',fill:'none',stroke:'#2b2418','stroke-width':16,'stroke-linecap':'round',pathLength:1,'stroke-dasharray':'1 1','stroke-dashoffset':1});
 const A=strip('TỪ ĐIỂN OXFORD',true,50,21),B=strip('CHỮ VIẾT TAY CỦA THƯƠNG NHÂN',false,32,22);
 return{upd:t=>{const e=popv(t,R(2)+.1,.6);pg.setAttribute('transform',`translate(540,640) rotate(-3) scale(${Math.max(.001,e)*.95})`);pg.setAttribute('opacity',e>0?1:0);const w=AT(2,'chữ',4.5);pen.setAttribute('stroke-dashoffset',1-inn(t,w-.3,2.2));
  sh(A,t,540,1085,-1,PV(t,2,'Oxford',1.0));sh(B,t,540,1195,1,PV(t,2,'chữ',4.5))}}});
// 3: thương nhân Anh làm ăn với người gốc Tây Ban Nha (ds3: tiền giấy 1777, ảnh minh họa)
S2(3,3,'p',null,g=>{const c=card('ds3',IMG+'ds3.jpg',900,600,31);const L=strip('TIỀN GIẤY GEORGIA 1777 · ẢNH MINH HỌA',false,26,32),A=strip('THƯƠNG NHÂN ANH',true,48,33),B=strip('GỐC TÂY BAN NHA',false,48,34);
 return{upd:t=>{const e=inn(t,R(3)-.2,.6);c.at(540,660,2,1,e);c.zoom(1+.12*inn(t,R(3),E(3)-R(3)),.5,.5);sh(L,t,540,350,-1,e);sh(A,t,330,1085,-2,PV(t,3,'thương',.8));sh(B,t,740,1190,2,PV(t,3,'gốc',3.6))}}});
// 4: peso Tây Ban Nha, chữ P và S chồng lên nhau (ds4)
S2(4,4,'d',null,g=>{const c=card('ds4',IMG+'ds4.jpg',900,520,41);const P=T(g,0,0,'P',210,'#f5efe0',12,'middle',DK),Sx=T(g,0,0,'S',210,'#f2c14e',12,'middle',DK),Q=dol(g,230);
 const A=strip('PESO TÂY BAN NHA',true,48,42),B=strip('CHỮ P + CHỮ S',false,50,43);
 return{upd:t=>{const e=inn(t,R(4)-.2,.6);c.at(540,520,-1,1,e);c.zoom(1+.08*inn(t,R(4),E(4)-R(4)),.5,.5);const w=AT(4,'chữ',6.0),u=popv(t,w-.4,.5),m=inn(t,w+1.4,1.6);
  P.setAttribute('transform',`translate(${270+m*190},1000) rotate(-6) scale(${Math.max(.001,u)})`);Sx.setAttribute('transform',`translate(${810-m*190},1000) rotate(6) scale(${Math.max(.001,u)})`);P.setAttribute('opacity',m<.97?1:0);Sx.setAttribute('opacity',m<.97?1:0);
  const q=popv(t,w+3.0,.5);Q.setAttribute('transform',`translate(540,1000) scale(${Math.max(.001,q)})`);Q.setAttribute('opacity',q>0?1:0);
  sh(A,t,540,300,-1,PV(t,4,'peso',2.0));sh(B,t,540,1180,1,PV(t,4,'chữ',6.0))}}});
// 5: peso tám réal (ds5), hợp pháp đến 1857
S2(5,5,'d',t=>'1857',g=>{const c=card('ds5',IMG+'ds5.jpg',620,560,51);const n=bigNum(g,'0',230,'#f2c14e');const A=strip('PESO 8 RÉAL',true,46,52),B=strip('TIỀN HỢP PHÁP Ở MỸ ĐẾN',false,34,53),C=strip('1857',true,70,54);
 return{upd:t=>{const e=inn(t,R(5)-.2,.6);c.at(310,680,-3,1,e);c.zoom(1+.12*inn(t,R(5),E(5)-R(5)),.5,.5);const w=AT(5,'tám',1.5),u=inn(t,w,1.2);n.textContent=String(Math.round(u*8));n.setAttribute('transform',`translate(800,600) rotate(4) scale(${t>w-.3?1:.001})`);
  sh(A,t,800,780,2,PV(t,5,'peso',.3));sh(B,t,540,1090,-1,PV(t,5,'tiền',2.6));sh(C,t,540,1200,1,PV(t,5,'năm',6.2))}}});
// 6: hai cột Hercules (ds6), dải băng chữ S
S2(6,6,'p',null,g=>{const c=card('ds6',IMG+'ds6.jpg',720,700,61);const A=strip('HAI CỘT HERCULES',true,48,62),B=strip('HUY HIỆU TÂY BAN NHA',false,34,63),C=strip('DẢI BĂNG CHỮ S',true,46,64);
 return{upd:t=>{const e=inn(t,R(6)-.2,.6);c.at(540,680,2,1,e);c.zoom(1+.14*inn(t,R(6),E(6)-R(6)),.5,.5);sh(A,t,540,360,-2,PV(t,6,'cột',1.8));sh(B,t,540,1090,1,PV(t,6,'huy',3.3));sh(C,t,540,1200,-1,PV(t,6,'dải',5.2))}}});
// 7: chữ U và S ghép lại, bị đóng dấu "không đúng" (ds7: ảnh minh họa)
S2(7,7,'d',null,g=>{const c=card('ds7',IMG+'ds7.jpg',620,500,71);const U=T(g,0,0,'U',200,'#f5efe0',12,'middle',DK),Sx=T(g,0,0,'S',200,'#f2c14e',12,'middle',DK);const S=stamp('KHÔNG ĐÚNG',60);const A=strip('U + S = ?',true,60,72),L=strip('ẢNH MINH HỌA',false,26,73);
 return{upd:t=>{const e=inn(t,R(7)-.2,.6);c.at(540,560,-2,1,e);c.zoom(1+.1*inn(t,R(7),E(7)-R(7)),.5,.5);const w=AT(7,'hai',2.2),u=popv(t,w,.5),m=inn(t,w+.8,1.2);
  U.setAttribute('transform',`translate(${300+m*180},1010) rotate(-6) scale(${Math.max(.001,u)})`);Sx.setAttribute('transform',`translate(${780-m*180},1010) rotate(6) scale(${Math.max(.001,u)})`);
  const v=popv(t,AT(7,'Cách',4.6),.5);S.at(540,1010,-8,Math.max(.001,v),v>0?1:0);sh(A,t,540,860,-1,PV(t,7,'U',1.9));sh(L,t,540,300,1,e)}}});
// 8: đồng thaler Bohemia (ds8)
S2(8,8,'p',null,g=>{const c=card('ds8',IMG+'ds8.jpg',800,600,81);const A=strip('CHỮ ĐÔ LA',true,52,82),B=strip('TỪ ĐỒNG THALER',false,48,83),C=strip('BOHEMIA · ĐẦU THẾ KỶ 16',false,34,84);
 return{upd:t=>{const e=inn(t,R(8)-.2,.6);c.at(540,650,-2,1,e);c.zoom(1+.14*inn(t,R(8),E(8)-R(8)),.5,.5);sh(A,t,540,1085,-1,PV(t,8,'chữ',.4));sh(B,t,540,1190,1,PV(t,8,'đồng',1.5));sh(C,t,540,330,-1,PV(t,8,'Bohemia',4.5))}}});
// 9: hai chuyện khác nhau (vẽ phẳng): tên có nguồn gốc rõ, hình dấu còn là giả thuyết
S2(9,9,'d',null,g=>{const L=el(g,'g',{}),Rr=el(g,'g',{});el(L,'rect',{x:-210,y:-250,width:420,height:500,rx:34,fill:'#efe3c5',stroke:'#17120c','stroke-width':9});el(Rr,'rect',{x:-210,y:-250,width:420,height:500,rx:34,fill:'#efe3c5',stroke:'#17120c','stroke-width':9});
 T(L,0,-120,'ĐÔ LA',72,'#17120c',0,'middle','none').setAttribute('stroke','none');T(Rr,0,-100,'$',200,'#17120c',0,'middle','none').setAttribute('stroke','none');
 const tk=tickMark(g,320,880,100,'#2e9e5f');const qm=T(g,0,0,'?',190,'#e5483f',14,'middle',DK);const A=strip('TÊN: NGUỒN GỐC RÕ',true,38,91),B=strip('HÌNH DẤU: GIẢ THUYẾT',false,38,92);
 return{upd:t=>{const a=popv(t,R(9)+.1,.6),b=popv(t,AT(9,'Cái',2.4),.6);L.setAttribute('transform',`translate(290,600) rotate(-3) scale(${Math.max(.001,a)})`);Rr.setAttribute('transform',`translate(790,600) rotate(3) scale(${Math.max(.001,b)})`);L.setAttribute('opacity',a>0?1:0);Rr.setAttribute('opacity',b>0?1:0);
  tk.set(inn(t,AT(9,'nguồn',3.4),.4));const q=popv(t,AT(9,'giả',5.6),.5);qm.setAttribute('transform',`translate(790,880) rotate(-8) scale(${Math.max(.001,q)*(.95+.05*Math.sin(t*4))})`);qm.setAttribute('opacity',q>0?1:0);
  sh(A,t,290,1090,-1,PV(t,9,'Cái',2.4));sh(B,t,790,1190,1,PV(t,9,'hình',4.8))}}});
// 10: sau 1800 xuất hiện trên sách báo in (ds10: bảng ký hiệu tiền tệ năm 1861)
S2(10,10,'p',t=>'1800',g=>{const c=card('ds10',IMG+'ds10.jpg',760,760,101);const rg=ring(c.top,.14*c.w,.215*c.h,.07*c.h,'#d8372d');const A=strip('SÁCH BÁO IN',true,52,102),B=strip('NGÀY CÀNG NHIỀU',false,46,103),L=strip('BẢNG KÝ HIỆU TIỀN TỆ, 1861',false,26,104);
 return{upd:t=>{const e=inn(t,R(10)-.2,.6);c.at(540,650,2,1,e);c.zoom(1+.14*inn(t,R(10),E(10)-R(10)),.5,.5);rg.set(inn(t,AT(10,'xuất',2.2),.8));sh(L,t,540,300,-1,e);sh(A,t,540,1090,-1,PV(t,10,'sách',3.4));sh(B,t,540,1200,1,PV(t,10,'ngày',2.8))}}});
// 11: câu hỏi cuối
S2(11,11,'d',null,g=>{const rg=[0,1,2].map(()=>el(g,'circle',{fill:'none',stroke:'#f2c14e','stroke-width':5}));const q=dol(g,330);const m=T(g,0,0,'?',200,'#e5483f',14,'middle',DK);const A=strip('AI VẼ RA DẤU $?',true,50,111),B=strip('GIẢ THUYẾT NÀO HỢP LÝ NHẤT?',false,38,112);
 return{upd:t=>{const e=inn(t,R(11)-.2,.7);rg.forEach((r2,i)=>{const u=((t-R(11)-i*.9)*.4)%1;r2.setAttribute('cx',540);r2.setAttribute('cy',650);r2.setAttribute('r',240+Math.max(0,u)*240);r2.setAttribute('opacity',(1-Math.max(0,u))*.5*e)});const qp=popv(t,R(11)+.2);q.setAttribute('transform',`translate(520,720) rotate(-8) scale(${qp*(.95+.05*Math.sin(t*4))})`);q.setAttribute('opacity',qp>0?1:0);const mp=popv(t,AT(11,'giả',3.4)||R(11)+3,.5);m.setAttribute('transform',`translate(800,520) rotate(10) scale(${Math.max(.001,mp)})`);m.setAttribute('opacity',mp>0?1:0);
  sh(A,t,540,1030,-1,PV(t,11,'một',.3));sh(B,t,540,1160,1,PV(t,11,'Bạn',3.6))}}},TOTAL);
sx(R(1)+.1,'whoosh',{d:.5,g:.5});
bm(R(1)+.3);bm(R(2)+.3,1);bm(R(3)+.3,1);bm(AT(4,'chữ',6.0));bm(R(5)+.3,1);bm(R(6)+.3,1);bm(AT(7,'Cách',4.6));bm(R(8)+.3,1);bm(AT(9,'giả',5.6),1);bm(R(10)+.3,1);bm(R(11)+.3);
sx(R(11)+.3,'question',{g:.7});
