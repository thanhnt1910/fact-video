const FR=(g,w,h,hang)=>{const k=el(g,'g',{});if(hang){el(k,'path',{d:`M${-w*.28} ${-h/2-90} L0 ${-h/2-10} L${w*.28} ${-h/2-90}`,fill:'none',stroke:'#7a5a2a','stroke-width':6,'stroke-linejoin':'round'})}
 el(k,'rect',{x:-w/2,y:-h/2,width:w,height:h,rx:10,fill:'#c9962f',stroke:'#fff','stroke-width':8});el(k,'rect',{x:-w/2+30,y:-h/2+30,width:w-60,height:h-60,rx:4,fill:'#2a1a16',stroke:'#17120c','stroke-width':6});el(k,'rect',{x:-w/2+12,y:-h/2+12,width:w-24,height:h-24,rx:6,fill:'none',stroke:'#f2d27a','stroke-width':4});return k};
// 1: hook (Mona Lisa, zoom vào gương mặt, ✗ lên "chỗ trống")
PH(1,'d','ml1',640,700,'MONA LISA · LOUVRE',[['BỊ TRỘM NĂM 1911','bad',44,'bị',1.3],['NGƯỜI ĐẾN NGẮM CHỖ TRỐNG','base',32,'chỉ',4.8]],null,{fx:.45,fy:.28,z:1.9,w:['bị',1.3],r:170,mark:'x',m:['trống',6.6]});
// 2: trước vụ trộm (trần phòng Salon Carré, ảnh minh họa)
PH(2,'p','ml2',940,600,'PHÒNG SALON CARRÉ (ẢNH MINH HỌA)',[['TRƯỚC VỤ TRỘM','base',46,'Vì',.2],['CHƯA PHẢI BỨC ĐƯỢC TÌM XEM NHIỀU NHẤT','bad',24,'chưa',3.6]],null,{fx:.5,fy:.4,z:1.6,w:['bảo',4.8],r:200});
// 3: báo Ý vẽ cảnh lấy tranh
PH(3,'d','ml3',640,700,'BÁO Ý NĂM 1911: TRANH RỜI TƯỜNG',[['THỨ HAI 21/8/1911','base',40,'sáng',2.2],['LOUVRE ĐÓNG CỬA, CÓ NGƯỜI LẤY TRANH','bad',26,'khi',9.0]],'1911',{fx:.5,fy:.42,z:1.8,w:['lấy',11.0],r:190,mark:'x',m:['tường',13.0]});
// 4: khung trống, người que soi đèn tìm
S2(4,4,'d',null,g=>{const f=FR(g,480,600,true);const q=T(g,0,0,'?',300,'#e5483f',16,'middle',DK);const m=MAS(g);const A=strip2('MÃI ĐẾN TRƯA HÔM SAU','bad',38,41),B=strip2('KHUNG KÍNH BỊ BỎ Ở CẦU THANG','base',26,42);
 return{upd:t=>{const e=popv(t,R(4)+.1,.6);PUT(f,540,700+Math.sin(t*1.4)*5,e,1,-2+Math.sin(t*1.1));const qp=popv(t,AT(4,'không',9.0),.5);q.setAttribute('transform',`translate(540,700) rotate(-8) scale(${Math.max(.001,qp)})`);q.setAttribute('opacity',qp>0?1:0);const u=inn(t,AT(4,'một',3.2),1.6);m.at(120+u*180,1010,.8,0,popv(t,AT(4,'một',3.2),.5),t,1,1);shw(A,t,540,1130,-1,PV(t,4,'mãi',.1));shw(B,t,540,1240,1,PV(t,4,'Chiếc',9.6))}}});
// 5: báo Excelsior
PH(5,'p','ml5',640,700,'BÁO EXCELSIOR, PARIS',[['BÁO CHÍ ĐĂNG TIN LỚN','ok',38,'báo',4.6],['THÔNG BÁO TRUY TÌM KHẮP NƠI','base',30,'thông',7.0]],null,{fx:.5,fy:.08,z:1.9,w:['báo',4.6],r:210,mark:'ok',m:['lớn',6.8]});
// 6: tường trống, hàng nghìn người đến xem
S2(6,6,'d',null,g=>{const f=FR(g,300,400,true);const q=T(g,0,0,'?',200,'#e5483f',14,'middle',DK);const P=[0,1,2].map(i=>PEOPLE(g,i==1?9:8,['#3a5a7a','#7a3a3a','#4a6a4a'][i],60+i));const n=bigNum(g,'0',130,CGOLD);const A=strip2('LOUVRE MỞ LẠI','base',44,61),B=strip2('NGƯỜI XEM CHỖ TRỐNG','bad',36,62);
 return{upd:t=>{const e=popv(t,R(6)+.1,.6);PUT(f,540,590+Math.sin(t*1.3)*4,e,1,-1);const qp=popv(t,R(6)+.8,.5);q.setAttribute('transform',`translate(540,590) rotate(-8) scale(${Math.max(.001,qp)})`);q.setAttribute('opacity',qp>0?1:0);
  P.forEach((p,i)=>{const w=AT(6,['hàng','kéo','đứng'][i],[1.8,3.2,4.4][i]);const u=popv(t,w,.6);PUT(p,540,850+i*80+Math.sin(t*3+i)*3,u,1.0,0)});
  const w=AT(6,'hàng',1.8),u=inn(t,w,2.6);n.textContent=String(Math.round(2000*u)).replace(/\B(?=(\d{3})+(?!\d))/g,'.')+'+';PUT(n,540,1075,popv(t,w,.5),.9,-2);shw(A,t,300,1175,-2,PV(t,6,'Louvre',.1));shw(B,t,700,1262,2,PV(t,6,'khoảng',5.6))}}});
// 7: Peruggia
PH(7,'d','ml7',900,700,'VINCENZO PERUGGIA · HỒ SƠ CẢNH SÁT PARIS',[['THỢ NGƯỜI Ý TỪNG LÀM Ở LOUVRE','base',26,'một',3.0],['GIẤU TRANH HƠN HAI NĂM','bad',38,'giấu',6.8]],null,{fx:.74,fy:.42,z:1.9,w:['Peruggia',2.0],r:150,mark:'x',m:['hai',7.4]});
// 8: hai năm giấu tranh (trục thời gian, người que soi đèn)
S2(8,8,'p',t=>'1911',g=>{const ln=el(g,'path',{d:'M180 640 L900 640',stroke:'#17120c','stroke-width':14,'stroke-linecap':'round',pathLength:1,'stroke-dasharray':1,'stroke-dashoffset':1});const d1=el(g,'circle',{r:34,fill:CSTEEL,stroke:'#fff','stroke-width':8}),d2=el(g,'circle',{r:34,fill:CRED,stroke:'#fff','stroke-width':8});const b1=bigNum(g,'1911',110,CSTEEL),b2=bigNum(g,'1913',110,CRED);const f=FR(g,120,150,false);const m=MAS(g);const A=strip2('CẢNH SÁT HỎI CUNG ÔNG','base',34,81),B=strip2('NHƯNG KHÔNG COI LÀ NGHI PHẠM','bad',28,82);
 return{upd:t=>{const w1=R(8)+.2,w2=AT(8,'cuối',6.4),v=inn(t,w1,w2-w1+.4);ln.setAttribute('stroke-dashoffset',1-v);PUT(d1,180,640,popv(t,w1,.5));PUT(d2,900,640,popv(t,w2,.5));PUT(b1,200,500,popv(t,w1,.5),1,-4);PUT(b2,880,500,popv(t,w2,.5),1,4);PUT(f,180+720*v,820+Math.sin(t*3)*6,popv(t,w1+.2,.5),1,0);m.at(260+Math.sin(t*.8)*20,1010,.7,0,popv(t,AT(8,'Cảnh',.4),.5),t);shw(A,t,540,1140,-1,PV(t,8,'Cảnh',.2));shw(B,t,540,1245,1,PV(t,8,'nhưng',2.8))}}});
// 9: thư ký tên giả Leonard (vẽ phẳng)
S2(9,9,'d',null,g=>{const k=el(g,'g',{});const sh=SHEET(k,560,520,9);const tt=T(k,0,-180,'THƯ GỬI FLORENCE',40,'#17120c',0,'middle','none');tt.setAttribute('stroke','none');const sg=SIG(k,'#1d3f78',9);const nm=T(k,0,150,'LEONARD',52,'#a8741a',0,'middle','none');nm.setAttribute('stroke','none');nm.setAttribute('font-style','italic');const x=XX(g,'#d8372d');const A=strip2('THƯ GỬI NGƯỜI BUÔN TRANH','base',34,91),B=strip2('KÝ TÊN GIẢ: LEONARD','bad',40,92);
 return{upd:t=>{const e=popv(t,R(9)+.1,.6);PUT(k,540,620+Math.sin(t*1.5)*6,e,1.05,-2+Math.sin(t*1.2)*.8);const a=inn(t,R(9)+.8,.8);sg.setAttribute('transform','translate(-40,40) scale(.6)');sg.setAttribute('opacity',a);const nn=popv(t,AT(9,'ký',5.4),.5);nm.setAttribute('opacity',nn>0?1:0);PUT(x,720,860,popv(t,AT(9,'giả',6.2),.5),.8,0);shw(A,t,540,1085,-1,PV(t,9,'viết',1.3));shw(B,t,540,1195,1,PV(t,9,'ký',5.4))}}});
// 10: bị bắt
PH(10,'p','ml10',700,700,'PERUGGIA SAU KHI BỊ BẮT',[['GẶP Ở KHÁCH SẠN','base',40,'gặp',.3],['NGƯỜI BUÔN TRANH BÁO CẢNH SÁT','ok',26,'rồi',5.2]],null,{fx:.5,fy:.42,z:1.7,w:['bị',8.0],r:190,mark:'ok',m:['bắt',8.6]});
// 11: tranh trở về Louvre
PH(11,'d','ml11',940,560,'TRANH TRỞ VỀ LOUVRE, THÁNG 1/1914',[['MONA LISA VỀ LẠI LOUVRE','ok',36,'Mona',1.4],['SAU KHI TRƯNG BÀY Ở VÀI THÀNH PHỐ Ý','base',24,'sau',5.0]],'1914',{fx:.45,fy:.45,z:1.8,w:['trở',2.4],r:170,mark:'ok',m:['Louvre',3.4]});
// 12: hơn 100.000 người trong hai ngày đầu
S2(12,12,'p',t=>'1914',g=>{const c=card('ml12',IMG+'ml12.jpg',940,670,121);const n=bigNum(g,'0',150,CGOLD);const L=strip2('HAI NGÀY ĐẦU','base',40,122),B=strip2('NGƯỜI ĐẾN XEM','ok',34,123);
 return{upd:t=>{const e=inn(t,R(12)-.2,.6);c.at(540,500,-2+Math.sin(t*1.1)*.5,1,e);c.zoom(1+.1*inn(t,R(12),E(12)-R(12)),.5,.5);const w=AT(12,'hơn',1.8),u=inn(t,w,1.4);n.textContent=String(Math.round(100000*u)).replace(/\B(?=(\d{3})+(?!\d))/g,'.')+'+';PUT(n,540,1085,popv(t,w,.5),1,-2);shw(L,t,540,895,-1,e);shw(B,t,540,1200,1,PV(t,12,'đã',3.2))}}});
// 13: bưu thiếp Mona Lisa sau 1911
PH(13,'d','ml13',620,700,'BƯU THIẾP MONA LISA SAU VỤ TRỘM 1911',[['SỬ GIA VẪN DÈ DẶT','bad',40,'các',.3],['CHỈ VỤ TRỘM ĐÃ LÀM NÊN DANH TIẾNG?','base',24,'chỉ',4.0]],null,{fx:.3,fy:.6,z:1.8,w:['dè',2.0],r:180,mark:'x',m:['chỉ',4.6]});
// 14: câu hỏi cuối: vẻ đẹp hay câu chuyện
S2(14,14,'p',null,g=>{const f1=FR(g,330,440,false),f2=FR(g,330,440,false);const q=T(g,0,0,'?',300,'#e5483f',16,'middle',DK);const m=MAS(g);const A=strip2('VẺ ĐẸP','ok',50,141),B=strip2('HAY CÂU CHUYỆN BIẾN MẤT?','bad',32,142);
 return{upd:t=>{PUT(f1,300,560+Math.sin(t*1.5)*6,popv(t,R(14)+.2,.6),1,-3);PUT(f2,780,560+Math.sin(t*1.5+2)*6,popv(t,AT(14,'hay',3.4),.6),1,3);const qp=popv(t,AT(14,'hay',3.4)+.5,.5);q.setAttribute('transform',`translate(540,640) rotate(${Math.sin(t*2)*6-6}) scale(${Math.max(.001,qp)})`);q.setAttribute('opacity',qp>0?1:0);m.at(540,1010,.8,0,popv(t,R(14)+.4,.5),t);shw(A,t,300,880,-2,PV(t,14,'vẻ',1.6));shw(B,t,700,1140,2,PV(t,14,'hay',3.4))}}},TOTAL);
sx(R(1)+.1,'whoosh',{d:.5,g:.5});
for(let i=1;i<=14;i++)bm(R(i)+.3,i%3!=1);
sx(R(14)+.3,'question',{g:.7});
