// 1 hook: tháp, chỉ đứng 20 năm
PH(1,'d','ef1',940,940,'THÁP EIFFEL · PARIS',[['LÚC MỚI DỰNG CHỈ ĐƯỢC ĐỨNG 20 NĂM','bad',28,'hai',2.2],['RỒI PHẢI DỠ ĐI?','bad',40,'dỡ',5.0]],null,{fx:.5,fy:.12,z:1.9,w:['dỡ',5.0],r:200,mark:'x',m:['dỡ',5.4]});
sx(R(1)+.2,'wind',{d:2.6,g:.5});
// 2 lá thư ký tên
S2(2,2,'p',null,g=>{const sh0=SHEET(g,640,760,21);const sg=[];const rr=rng(5);for(let i=0;i<14;i++){const s=SIG(g,'#2a2a6a',20+i);sg.push(s)}const A=strip2('HƠN 40 NGHỆ SĨ KÝ TÊN','bad',40,22),B=strip2('ĐÒI CHẶN THÁP TRƯỚC KHI KHỞI CÔNG','base',28,23);const N=BIG(g,'40+',170,CRED,'#fff');
 return{upd:t=>{const e=popv(t,R(2)+.1,.6);PUT(sh0,540,640,e,1,Math.sin(t*1.4)*1.2);const w=AT(2,'hơn',1.0);sg.forEach((s,i)=>{const u=popv(t,w+i*.28,.4);PUT(s,400+(i%2)*270,430+Math.floor(i/2)*85,u,.55,-4+i%3*3)});PUT(N.k,540,1000,popv(t,AT(2,'bốn',2.4),.5),1,-3);shw(A,t,540,1130,-1,PV(t,2,'hơn',1.0));shw(B,t,540,1235,1,PV(t,2,'đòi',4.6))}}});
for(let i=0;i<5;i++)sx(AT(2,'hơn',1.0)+i*.5,'paper',{g:.5});
// 3 hai cái tên
S2(3,3,'d',null,g=>{const card=(txt,sub,x)=>{const k=el(g,'g',{});el(k,'rect',{x:-230,y:-140,width:460,height:280,rx:30,fill:'#efe6cf',stroke:'#17120c','stroke-width':8});el(k,'circle',{cx:0,cy:-60,r:46,fill:'#7a6652',stroke:'#17120c','stroke-width':6});const a=T(k,0,38,txt,44,'#17120c',0,'middle','none');const b=T(k,0,92,sub,28,'#6b5a48',0,'middle','none');return k};const c1=card('MAUPASSANT','nhà văn'),c2=card('CHARLES GARNIER','kiến trúc sư Nhà hát Opera');const A=strip2('NGƯỜI NỔI TIẾNG CŨNG KÝ','base',34,31);
 return{upd:t=>{PUT(c1,300,700,popv(t,AT(3,'Guy',1.2),.5),1,-5);PUT(c2,780,860,popv(t,AT(3,'Garnier',4.0),.5),1,4);shw(A,t,540,1130,-1,PV(t,3,'Trong',.2))}}});
sx(AT(3,'Guy',1.2),'stamp',{g:.5});sx(AT(3,'Garnier',4.0),'stamp',{g:.5});
// 4 trang nhất báo, ống khói
PH(4,'p','ef2',560,760,'TRANG NHẤT BÁO LE TEMPS',[['“VÔ DỤNG VÀ QUÁI DỊ”','bad',40,'vô',3.4],['NHƯ ỐNG KHÓI NHÀ MÁY KHỔNG LỒ','base',28,'ống',6.0]],null,{fx:.5,fy:.25,z:1.8,w:['quái',4.4],r:170,mark:'x',m:['quái',4.8]});
// 5 Eiffel đáp lại
PH(5,'d','ef3',940,630,'GUSTAVE EIFFEL (1832–1923)',[['TRẢ LỜI ÔN HÒA','ok',40,'trả',2.4],['SO THÁP VỚI KIM TỰ THÁP AI CẬP','base',28,'kim',8.0]],null,{fx:.5,fy:.35,z:1.6,w:['yêu',5.4],r:170,mark:'ok',m:['yêu',5.8]});
// 6 giấy phép 20 năm
PH(6,'p','ef5',640,900,'HỢP ĐỒNG XÂY THÁP (LƯU TRỮ QUỐC GIA PHÁP)',[['GIẤY PHÉP CHỈ 20 NĂM','bad',40,'giấy',3.0],['TÍNH TỪ LÚC THÁP MỞ CỬA','base',30,'tính',5.2]],null,{fx:.5,fy:.2,z:1.9,w:['hai',3.4],r:150,mark:'x',m:['hai',3.8]});
sx(AT(6,'giấy',3.0),'stamp',{g:.8});
// 7 hết hạn → thuộc Paris, bị dỡ
S2(7,7,'d',null,g=>{const tw=TOWER(g);const cal=el(g,'g',{});el(cal,'rect',{x:-230,y:-210,width:460,height:420,rx:26,fill:'#efe6cf',stroke:'#17120c','stroke-width':8});el(cal,'rect',{x:-230,y:-210,width:460,height:100,rx:26,fill:CRED,stroke:'#17120c','stroke-width':8});T(cal,0,-135,'CÒN ... NĂM',34,'#fff',0,'middle','none');const num=BIG(cal,'20',200,'#17120c',null);const xx=XX(g);const A=strip2('HẾT HẠN: THUỘC VỀ PARIS','bad',34,71),B=strip2('VIỆC DỠ THÁP CÓ THỂ XẢY RA','bad',30,72);
 return{upd:t=>{const e=popv(t,R(7)+.1,.6);PUT(tw,290,720,e,.9,0);const w=AT(7,'Hết',.2),u=inn(t,w,3.5);num.set(String(Math.max(0,Math.round(20*(1-u)))));PUT(cal,770,640,e,1,3);PUT(xx,290,720,popv(t,AT(7,'dỡ',4.6),.5),1.6,0);shw(A,t,540,1130,-1,PV(t,7,'Hết',.2));shw(B,t,540,1235,1,PV(t,7,'dỡ',4.6))}}});
for(let i=0;i<7;i++)sx(R(7)+.4+i*.45,'tit',{f:1500,g:.4});
// 8 Eiffel tìm việc cho tháp
PH(8,'p','ef6',940,620,'BẢN DỰNG LẠI PHÒNG LÀM VIỆC CỦA EIFFEL TRÊN ĐỈNH THÁP',[['TÌM CHO THÁP MỘT CÔNG VIỆC','ok',34,'tìm',.6],['ĂNG-TEN VÔ TUYẾN, TỰ BỎ TIỀN LẮP','base',28,'ăng',4.0]],null,{fx:.5,fy:.45,z:1.6,w:['ăng',4.0],r:190,mark:'ok',m:['bỏ',7.0]});
sx(AT(8,'ăng',4.0),'hammer',{g:.5});
// 9 Morse từ tháp tới Panthéon
S2(9,9,'d',t=>'5/11/1898',g=>{const tw=TOWER(g);const dome=el(g,'g',{});el(dome,'path',{d:'M-110 0 A110 110 0 0 1 110 0 Z',fill:'#a89d88',stroke:'#17120c','stroke-width':7});el(dome,'rect',{x:-130,y:0,width:260,height:110,fill:'#8c826f',stroke:'#17120c','stroke-width':7});const ws=WV(g,CGOLD,3);const dots=[...Array(8)].map(()=>el(g,'circle',{r:14,fill:CGOLD,stroke:'#fff','stroke-width':5}));const A=strip2('MORSE: THÁP → ĐỀN PANTHÉON','ok',32,91),B=strip2('CÁCH NHAU KHOẢNG 4 KM','base',36,92);
 return{upd:t=>{const e=popv(t,R(9)+.1,.6);PUT(tw,200,740+Math.sin(t*3)*9,e,.7+Math.sin(t*4)*.025,Math.sin(t*2)*2);PUT(dome,880,880+Math.sin(t*2.2+1)*7,e,.9,Math.sin(t*1.7)*1.2);const w=AT(9,'tín',2.6);WVU(ws,t,420,230,540,.6,.35+.65*inn(t,w-.2,.2));dots.forEach((d,i)=>{const u=((t-w-i*.18)*.55);const uu=Math.max(0,Math.min(1,u));d.setAttribute('cx',230+uu*600);d.setAttribute('cy',560+Math.sin(uu*9)*20);d.setAttribute('opacity',(u>0&&u<1)?1:0)});shw(A,t,540,1130,-1,PV(t,9,'tín',2.6));shw(B,t,540,1235,1,PV(t,9,'cách',6.4))}}});
sx(AT(9,'tín',2.6),'morse',{pat:'.-.. .-',g:.9});
// 10 phòng thí nghiệm của Ferrié
PH(10,'d','ef7',940,580,'SÁCH CỦA EIFFEL VỀ THÍ NGHIỆM DƯỚI CHÂN THÁP',[['ĐẠI ÚY FERRIÉ, 31 TUỔI','ok',34,'Đại',1.4],['LÀM THÍ NGHIỆM TRONG CHÒI NHỎ','base',28,'chòi',7.4]],null,{fx:.5,fy:.5,z:1.6,w:['chòi',7.4],r:180});
// 11 tới Tunisia
S2(11,11,'p',t=>'1908',g=>{const sea=el(g,'rect',{x:-420,y:-60,width:840,height:300,rx:30,fill:'#2f6d9a',stroke:'#fff','stroke-width':8});const land1=el(g,'ellipse',{cx:-250,cy:-130,rx:200,ry:80,fill:'#8c7b5a',stroke:'#17120c','stroke-width':6}),land2=el(g,'ellipse',{cx:260,cy:260,rx:200,ry:70,fill:'#a69067',stroke:'#17120c','stroke-width':6});const ws=WV(g,CGOLD,4);const pa=el(g,'circle',{r:22,fill:CRED,stroke:'#fff','stroke-width':6}),tn=el(g,'circle',{r:22,fill:CGOLD,stroke:'#fff','stroke-width':6});const t1=T(g,0,0,'PARIS',34,'#fff',8,'middle','#17120c'),t2=T(g,0,0,'BIZERTE (TUNISIA)',30,'#fff',8,'middle','#17120c');const A=strip2('TÍN HIỆU VƯỢT ĐỊA TRUNG HẢI','ok',32,111),B=strip2('TỚI CĂN CỨ HẢI QUÂN BIZERTE','base',30,112);
 return{upd:t=>{const e=popv(t,R(11)+.1,.6);[sea,land1,land2].forEach(o=>o.setAttribute('opacity',e));const gx=540,gy=720;pa.setAttribute('cx',gx-200);pa.setAttribute('cy',gy-170);tn.setAttribute('cx',gx+250);tn.setAttribute('cy',gy+190);t1.setAttribute('x',gx-200);t1.setAttribute('y',gy-210);t2.setAttribute('x',gx+240);t2.setAttribute('y',gy+250);[sea,land1,land2].forEach(o=>o.setAttribute('transform',`translate(${gx},${gy})`));const w=AT(11,'tín',2.0);WVU(ws,t,640,gx-200,gy-170,.55,inn(t,w-.2,.2));pa.setAttribute('opacity',e);tn.setAttribute('opacity',popv(t,AT(11,'Bizerte',6.4),.5));t1.setAttribute('opacity',e);t2.setAttribute('opacity',popv(t,AT(11,'Bizerte',6.4),.5));shw(A,t,540,1130,-1,PV(t,11,'tín',2.0));shw(B,t,540,1235,1,PV(t,11,'căn',5.4))}}});
sx(AT(11,'tín',2.0),'morse',{pat:'-.-. --',g:.8});sx(AT(11,'Bizerte',6.4),'ping',{g:.6});
// 12 gia hạn 70 năm
PH(12,'d','ef8',940,760,'CHÂN THÁP EIFFEL',[['GIA HẠN THÊM 70 NĂM','ok',40,'bảy',5.0],['THÁP KHÔNG CÒN BỊ DỠ','base',32,'thành',2.0]],'1910',{fx:.5,fy:.55,z:1.5,w:['bảy',5.0],r:200,mark:'ok',m:['bảy',5.6]});
sx(AT(12,'bảy',5.0),'stamp',{g:.7});sx(AT(12,'bảy',5.0)+.1,'chime',{g:.5});
// 13 câu hỏi cuối
S2(13,13,'p',null,g=>{const tw=TOWER(g,'#8a7a64');const ws=WV(g,CGOLD,4);const q=BIG(g,'?',320,CRED,'#fff');const A=strip2('KHÔNG CÓ LÀN SÓNG VÔ TUYẾN','bad',30,131),B=strip2('PARIS CÒN THÁP EIFFEL KHÔNG?','bad',34,132);
 return{upd:t=>{const e=popv(t,R(13)+.1,.6);PUT(tw,540,700,e,1.1,0);WVU(ws,t,420,540,400,.5,e);PUT(q.k,830,520,popv(t,AT(13,'còn',4.4),.6),1,8);shw(A,t,540,1130,-1,PV(t,13,'Vậy',.2));shw(B,t,540,1235,1,PV(t,13,'còn',4.4))}}},TOTAL);
sx(R(13)+.3,'wind',{d:2.4,g:.4});
