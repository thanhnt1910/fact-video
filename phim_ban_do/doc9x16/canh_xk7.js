// ===== Cầu Long Biên (xk7). Ảnh: lb1(1) lb2(2) lb3(3) lb5(5) lb6(6) lb8(8) lb9(9) lb12(12) lb15(15) lb16(16) lb18(18) lb19(19) lb20(20). Cảnh 4,7,10,11,13,14,17,21 vẽ phẳng.

// ===== Dấu ấn riêng của video này: nền THÉP – bản vẽ kỹ thuật (thay nền trống đồng mặc định), giàn thép trôi chậm dưới đáy
{DR1.setAttribute('opacity',0);DR2.setAttribute('opacity',0);
 DARKG.firstChild.setAttribute('fill','#0b1823');
 [...PAPG.children].forEach((c,i)=>{if(c.tagName=='g')c.setAttribute('opacity',0);if(c.tagName=='line')c.setAttribute('stroke',i%3?'rgba(70,100,120,.16)':'rgba(240,248,252,.30)')});
 PAPG.firstChild.setAttribute('fill','#c3ccc8');
 const grid=(p,col,op)=>{const g=el(p,'g',{opacity:op});for(let x=0;x<=1080;x+=60)el(g,'line',{x1:x,y1:0,x2:x,y2:1920,stroke:col,'stroke-width':x%300?1.2:2.4});for(let y=0;y<=1920;y+=60)el(g,'line',{x1:0,y1:y,x2:1080,y2:y,stroke:col,'stroke-width':y%300?1.2:2.4});return g};
 grid(DARKG,'#1a3a55',.55);grid(PAPG,'#6f8da0',.28);
 // vòng tròn đinh tán rải rác
 const rv=(p,col,seed)=>{const r=rng(seed);for(let i=0;i<46;i++){const x=60+Math.round(r()*17)*60,y=60+Math.round(r()*30)*60;el(p,'circle',{cx:x,cy:y,r:5,fill:col})}};rv(DARKG,'#24506f',3);rv(PAPG,'#7e98a6',4);
 // giàn thép Warren trôi chậm (chu kỳ 240 px nên lặp liền mạch)
 const mkTruss=(p,col,sw,op)=>{const g=el(p,'g',{opacity:op});const k=el(g,'g',{});for(let i=-1;i<12;i++){const x=i*240;el(k,'path',{d:`M${x} 1860 L${x+120} 1640 L${x+240} 1860`,fill:'none',stroke:col,'stroke-width':sw,'stroke-linejoin':'round'})}el(k,'path',{d:'M-240 1860 L2640 1860 M-240 1640 L2640 1640',stroke:col,'stroke-width':sw+4});for(let i=-1;i<12;i++)el(k,'circle',{cx:i*240+120,cy:1640,r:9,fill:col});return k};
 const TD=mkTruss(DARKG,'#1e4568',7,.9),TP=mkTruss(PAPG,'#8aa3b1',7,.8);
 window.THEME_UPD=t=>{const o=-((t*36)%240);TD.setAttribute('transform',`translate(${o.toFixed(1)},0)`);TP.setAttribute('transform',`translate(${o.toFixed(1)},0)`)};
}
const HB=[];const bm=(t,l)=>{sx(t,'boom',l?{light:true,g:.8}:{g:1});if(!l)HB.push(t)};
const PUT=(o,x,y,u,sc=1,rot=0)=>{o.setAttribute('transform',`translate(${x},${y}) rotate(${rot}) scale(${Math.max(.001,u)*sc})`);o.setAttribute('opacity',u>0?1:0)};
const SIG=(g,col,seed)=>{const k=el(g,'g',{});const r=rng(seed);let d='M-90 10';for(let i=0;i<7;i++)d+=` q${12+r()*10} ${-50-r()*40} ${22+r()*8} ${10+r()*20} t${22+r()*10} ${-6}`;el(k,'path',{d,fill:'none',stroke:col,'stroke-width':8,'stroke-linecap':'round','stroke-linejoin':'round'});return k};
const XX=(g,col='#e5483f')=>{const k=el(g,'g',{});el(k,'path',{d:'M-70 -70 L70 70 M70 -70 L-70 70',stroke:'#fff','stroke-width':34,'stroke-linecap':'round'});el(k,'path',{d:'M-70 -70 L70 70 M70 -70 L-70 70',stroke:col,'stroke-width':20,'stroke-linecap':'round'});return k};
const BEAM=(g,w)=>{const k=el(g,'g',{});el(k,'rect',{x:-w/2,y:-26,width:w,height:52,rx:8,fill:'#6d7378',stroke:'#fff','stroke-width':7});for(let i=0;i<w/52;i++)el(k,'path',{d:`M${-w/2+i*52} 24 L${-w/2+i*52+26} -24 L${-w/2+i*52+52} 24`,fill:'none',stroke:'#2d3236','stroke-width':5});return k};
// ảnh + dải chữ (mẫu chung)
const PH=(n,bg,key,mw,mh,lab,items,yr)=>S2(n,n,bg,yr?(t=>yr):null,g=>{const c=card(key,IMG+key+'.jpg',mw,mh,n*10+1);const L=lab?strip(lab,false,lab.length>34?22:26,n*10+2):null;const S=items.map((it,i)=>strip(it[0],it[1],it[2],n*10+3+i));
 return{upd:t=>{const e=inn(t,R(n)-.2,.6);c.at(540,630,(n%2?-2:2),1,e);c.zoom(1+.1*inn(t,R(n),E(n)-R(n)),.5,.5);if(L)sh(L,t,540,338,-1,e);items.forEach((it,i)=>sh(S[i],t,540,1085+i*110,(i%2?1:-1),PV(t,n,it[3],it[4])))}}});
// 1: hook
PH(1,'d','lb1',900,560,'CẦU LONG BIÊN NĂM 1915',[['CẦU DO EIFFEL THIẾT KẾ?',true,40,'nhiều',1.5],['BẢN VẼ GỐC KHÔNG CÓ CHỮ KÝ ÔNG',false,32,'nhưng',5.0]]);
// 2: bước ngoặt (chân dung)
S2(2,2,'p',null,g=>{const c=card('lb2',IMG+'lb2.jpg',470,640,21);const L=strip('GUSTAVE EIFFEL, 1888',false,24,22),A=strip('EIFFEL',true,56,23),B=strip('TÊN QUÁ NỔI TIẾNG',false,32,24),C=strip('NHƯNG HỒ SƠ KỂ KHÁC',true,34,25);const q=T(g,0,0,'?',260,'#e5483f',16,'middle',DK);
 return{upd:t=>{const e=inn(t,R(2)-.2,.6);c.at(300,650,-3,1,e);c.zoom(1+.1*inn(t,R(2),E(2)-R(2)),.5,.3);sh(L,t,300,338,-1,e);sh(A,t,790,520,3,PV(t,2,'cái',1.8));sh(B,t,790,640,-2,PV(t,2,'quá',2.6));const qp=popv(t,AT(2,'Nhưng',4.2),.5);q.setAttribute('transform',`translate(790,900) rotate(-8) scale(${Math.max(.001,qp)})`);q.setAttribute('opacity',qp>0?1:0);sh(C,t,790,1090,2,qp)}}});
// 3: mô tả cầu + số đếm
S2(3,3,'d',null,g=>{const c=card('lb3',IMG+'lb3.jpg',900,560,31);const L=strip('CẦU LONG BIÊN THỜI PHÁP THUỘC',false,24,32);const n=[bigNum(g,'0',120,'#f2c14e'),bigNum(g,'0',120,'#ff8a5c'),bigNum(g,'0',104,'#7fd0ff')];const lb=[strip('NHỊP THÉP',false,28,33),strip('TRỤ CẦU',false,28,34),strip('MÉT CẦU THÉP',false,28,35)];const X=[190,540,890];const W3=['mười','hai','nghìn'],F3=[2.4,3.6,6.2],V=[19,20,1680];
 return{upd:t=>{const e=inn(t,R(3)-.2,.6);c.at(540,590,-2,1,e);c.zoom(1+.1*inn(t,R(3),E(3)-R(3)),.5,.5);sh(L,t,540,318,-1,e);for(let i=0;i<3;i++){const w=Math.min(AT(3,W3[i],F3[i]),E(3)-2.4+i*.2),u=inn(t,w,.9);n[i].textContent=String(Math.round(V[i]*u)).replace(/\B(?=(\d{3})+(?!\d))/g,'.');n[i].setAttribute('transform',`translate(${X[i]},1130) rotate(${i-1}) scale(${t>w-.2?1:.001})`);sh(lb[i],t,X[i],1225,i-1,inn(t,w,.4))}}}});
// 4: đấu thầu sáu hãng (vẽ phẳng)
S2(4,4,'p',t=>'1897',g=>{const bx=[];for(let i=0;i<6;i++){const k=el(g,'g',{});el(k,'rect',{x:-130,y:-70,width:260,height:140,rx:22,fill:'#efe9d8',stroke:'#17120c','stroke-width':8});const tt=T(k,0,-6,'HÃNG',38,'#17120c',0,'middle','none');tt.setAttribute('stroke','none');const nn=T(k,0,46,String(i+1),56,'#d8372d',0,'middle','none');nn.setAttribute('stroke','none');bx.push(k)}
 const A=strip('ĐẤU THẦU XÂY CẦU',true,48,41),B=strip('SÁU HÃNG THAM GIA',false,44,42);
 return{upd:t=>{const w=R(4)+.5;for(let i=0;i<6;i++)PUT(bx[i],i%2?740:340,430+Math.floor(i/2)*230,popv(t,w+i*.45,.5)||0,1,(i%2?2:-2));sh(A,t,540,1085,-1,PV(t,4,'đấu',1.6));sh(B,t,540,1195,1,PV(t,4,'sáu',3.0))}}});
// 5: hãng thắng thầu (biển hãng ở Paris, minh họa)
PH(5,'d','lb5',900,560,'BIỂN HÃNG Ở PARIS (ẢNH MINH HỌA)',[['HÃNG THẮNG THẦU',true,44,'Hãng',.2],['DAYDÉ & PILLÉ · ĐỒ ÁN B',false,36,'đồ',4.0]]);
// 6: Levallois-Perret
PH(6,'p','lb6',900,560,'XƯỞNG LEVALLOIS-PERRET, 1887',[['HÃNG KẾ THỪA EIFFEL',true,40,'kế',1.8],['DỰ THẦU NHƯNG KHÔNG TRÚNG',false,34,'nhưng',4.4]]);
// 7: bản vẽ hai chữ ký (vẽ phẳng)
S2(7,7,'d',null,g=>{const k=el(g,'g',{});el(k,'rect',{x:-300,y:-270,width:600,height:540,rx:26,fill:'#f5efe0',stroke:'#17120c','stroke-width':10});for(let i=0;i<4;i++)el(k,'path',{d:`M-220 ${-170+i*50} L220 ${-170+i*50}`,stroke:'#b9ad8e','stroke-width':6,'stroke-linecap':'round'});const tt=T(k,0,-206,'BẢN VẼ ĐỒ ÁN B',44,'#17120c',0,'middle','none');tt.setAttribute('stroke','none');
 const s1=SIG(k,'#1d3f78',7),s2=SIG(k,'#9b2d20',8);const n1=T(k,0,0,'KỸ SƯ DAYDÉ',26,'#17120c',0,'middle','none'),n2=T(k,0,0,'KỸ SƯ PILLÉ',26,'#17120c',0,'middle','none');n1.setAttribute('stroke','none');n2.setAttribute('stroke','none');
 const A=strip('TRUNG TÂM LƯU TRỮ QUỐC GIA SỐ 1',false,28,71),B=strip('CÓ CHỮ KÝ HAI KỸ SƯ',true,42,72);
 return{upd:t=>{const e=popv(t,R(7)+.1,.6);PUT(k,540,640,e,1.05,-2);const a=inn(t,AT(7,'Theo',.2)+.6,.8),b=inn(t,AT(7,'các',3.0),.8);s1.setAttribute('transform',`translate(-165,50) scale(.5)`);s1.setAttribute('opacity',a);s2.setAttribute('transform',`translate(95,50) scale(.5)`);s2.setAttribute('opacity',b);n1.setAttribute('transform','translate(-95,150)');n1.setAttribute('opacity',a);n2.setAttribute('transform','translate(165,150)');n2.setAttribute('opacity',b);sh(A,t,540,1085,-1,PV(t,7,'Theo',.2));sh(B,t,540,1195,1,PV(t,7,'có',2.0))}}});
// 8: Doumer ký phê duyệt, không có chữ ký Eiffel
S2(8,8,'p',null,g=>{const c=card('lb8',IMG+'lb8.jpg',470,640,81);const L=strip('PAUL DOUMER',false,26,82),A=strip('CHỮ KÝ PHÊ DUYỆT',true,34,83),B=strip('TOÀN QUYỀN ĐÔNG DƯƠNG',false,28,84),C=strip('KHÔNG CÓ CHỮ KÝ EIFFEL',true,30,85);const sg=SIG(g,'#1d3f78',9),x=XX(g);const bx=el(g,'g',{});el(bx,'rect',{x:-190,y:-60,width:380,height:120,rx:18,fill:'none',stroke:'#17120c','stroke-width':7,'stroke-dasharray':'18 12'});const ee=T(bx,0,14,'EIFFEL',54,'#17120c',0,'middle','none');ee.setAttribute('stroke','none');ee.setAttribute('opacity',.45);
 return{upd:t=>{const e=inn(t,R(8)-.2,.6);c.at(300,650,3,1,e);c.zoom(1+.1*inn(t,R(8),E(8)-R(8)),.5,.3);sh(L,t,300,338,-1,e);sh(A,t,790,470,3,PV(t,8,'chữ',.3));sh(B,t,790,590,-2,PV(t,8,'Toàn',1.6));const a=inn(t,AT(8,'và',4.4),.6);const a0=inn(t,AT(8,'Toàn',1.6)+.3,.7);sg.setAttribute('transform','translate(740,720) scale(.62)');sg.setAttribute('opacity',a0);const bp=popv(t,AT(8,'và',4.4),.5);PUT(bx,790,900,bp,1,-2);PUT(x,790,900,popv(t,AT(8,'không',4.8),.5),.8,0);sh(C,t,790,1030,2,PV(t,8,'không',4.8))}}});
// 9: tấm biển trên cầu
PH(9,'d','lb9',900,600,'TẤM BIỂN TRÊN CẦU NGÀY NAY',[['BIỂN KIM LOẠI',true,44,'tấm',1.4],['TÊN HÃNG DAYDÉ & PILLÉ',false,34,'tên',2.4]]);
// 10: 1898 – 1902 (vẽ phẳng)
S2(10,10,'p',t=>'1898',g=>{const ln=el(g,'path',{d:'M180 650 L900 650',stroke:'#f5efe0','stroke-width':14,'stroke-linecap':'round',pathLength:1,'stroke-dasharray':1,'stroke-dashoffset':1});const d1=el(g,'circle',{r:34,fill:'#d8372d',stroke:'#fff','stroke-width':8}),d2=el(g,'circle',{r:34,fill:'#2f9a5a',stroke:'#fff','stroke-width':8});const b1=bigNum(g,'1898',110,'#f2c14e'),b2=bigNum(g,'1902',110,'#7fd0ff');const bg2=BEAM(g,300);
 const A=strip('KHỞI CÔNG',true,44,101),B=strip('XÂY XONG',false,44,102);
 return{upd:t=>{const w1=AT(10,'khởi',.6),w2=AT(10,'hoàn',2.2),u=inn(t,w1,.5),v=inn(t,w1+.3,w2-w1+.6);ln.setAttribute('stroke-dashoffset',1-v);PUT(d1,180,650,popv(t,w1,.5));PUT(d2,900,650,popv(t,w2,.5));PUT(b1,200,520,popv(t,w1,.5),1,-4);PUT(b2,880,520,popv(t,w2,.5),1,4);PUT(bg2,180+720*v,820,popv(t,w1+.2,.5),1,0);sh(A,t,230,1085,-2,PV(t,10,'khởi',.6));sh(B,t,850,1195,2,PV(t,10,'hoàn',2.2))}}});
// 11: công nhân Việt Nam lắp nhịp thép (vẽ phẳng)
S2(11,11,'d',null,g=>{const bm1=BEAM(g,760),f=[0,1,2].map(i=>fig(g,{hat:['#d8c9a0','#c9b27c','#e0d2a8'][i],tool:i!=1}));const n=bigNum(g,'0',120,'#f2c14e');const A=strip('HÀNG NGHÌN CÔNG NHÂN VIỆT NAM',true,34,111),B=strip('LẮP RÁP NHỮNG NHỊP THÉP',false,38,112);
 return{upd:t=>{const e=popv(t,R(11)+.1,.6);PUT(bm1,540,900,e,1.1,-1);f.forEach((o,i)=>o.at(260+i*270,900-18,.55,Math.sin(t*5+i)*4,inn(t,R(11)+.3+i*.3,.4)));const w=AT(11,'Hàng',.2),u=inn(t,w,1.4);n.textContent=String(Math.round(1000*u)).replace(/\B(?=(\d{3})+(?!\d))/g,'.')+'+';PUT(n,540,500,popv(t,w,.5),1,-2);sh(A,t,540,1085,-1,PV(t,11,'Hàng',.2));sh(B,t,540,1195,1,PV(t,11,'lắp',1.4))}}});
// 12: tên cũ Paul Doumer
PH(12,'p','lb12',900,600,'CẦU PAUL DOUMER (LONG BIÊN)',[['TÊN CŨ: PAUL DOUMER',true,40,'Lúc',.2],['SAU ĐỔI THÀNH LONG BIÊN',false,36,'Sau',4.0]]);
// 13: nhầm lẫn: tháp Eiffel nằm ngang (vẽ phẳng)
S2(13,13,'d',null,g=>{const tw=el(g,'g',{});el(tw,'path',{d:'M0 -230 L-120 230 L120 230Z',fill:'none',stroke:'#fff','stroke-width':20,'stroke-linejoin':'round'});el(tw,'path',{d:'M0 -230 L-120 230 L120 230Z',fill:'none',stroke:'#7a5a3a','stroke-width':10,'stroke-linejoin':'round'});for(let i=0;i<6;i++){const y=-150+i*70,w=(y+230)/460*120;el(tw,'path',{d:`M${-w} ${y} L${w} ${y} M${-w} ${y} L${w*.6} ${y+70}`,stroke:'#7a5a3a','stroke-width':6})}
 const bd=BEAM(g,820);const q=T(g,0,0,'?',230,'#e5483f',16,'middle',DK);const A=strip('CẦU BẰNG THÉP',false,40,131),B=strip('THÁP EIFFEL NẰM NGANG?',true,40,132);
 return{upd:t=>{const e=popv(t,R(13)+.1,.6);const w=AT(13,'tháp',5.0),u=inn(t,w-.3,1.2);PUT(tw,540-u*0,540,e,.9,-90*u);tw.setAttribute('transform',`translate(540,560) rotate(${-90*u+90*u*0}) scale(${.9*Math.max(.001,e)})`);PUT(bd,540,860,popv(t,R(13)+.3,.6)*u,1.0,0);const qp=popv(t,R(13)+.2,.5);q.setAttribute('transform',`translate(910,500) rotate(10) scale(${Math.max(.001,qp)})`);q.setAttribute('opacity',qp>0?1:0);sh(A,t,540,1085,-1,PV(t,13,'Cầu',1.2));sh(B,t,540,1195,1,PV(t,13,'tháp',5.0))}}});
// 14: ý kiến Lê Huy Tuấn (vẽ phẳng)
S2(14,14,'p',null,g=>{const bm1=BEAM(g,420);const ne=T(g,0,0,'≠',300,'#e5483f',16,'middle',DK);const ei=T(g,0,0,'EIFFEL',92,'#17120c',0,'middle','none');ei.setAttribute('stroke','none');const st=T(g,0,0,'THÉP',92,'#17120c',0,'middle','none');st.setAttribute('stroke','none');
 const A=strip('LÊ HUY TUẤN',true,52,141),B=strip('TRUNG TÂM LƯU TRỮ QUỐC GIA SỐ 1',false,26,142),C=strip('LÀM BẰNG THÉP CHƯA ĐỦ',false,36,143);
 return{upd:t=>{const e=popv(t,R(14)+.1,.6);PUT(st,300,560,e,1,-4);PUT(ei,780,560,popv(t,R(14)+.5,.6),1,4);PUT(ne,540,570,popv(t,AT(14,'làm',3.6),.5),1,-6);PUT(bm1,540,820,popv(t,R(14)+.3,.5),.8,0);sh(A,t,540,1060,-1,PV(t,14,'Lê',1.0));sh(B,t,540,1160,1,PV(t,14,'Trung',1.8));sh(C,t,540,1250,-1,PV(t,14,'làm',3.6))}}});
// 15: thép ở Pháp thế kỷ 19 (ảnh minh họa)
PH(15,'d','lb15',900,600,'CẦU THÉP Ở PHÁP THẾ KỶ 19 (ẢNH MINH HỌA)',[['THÉP PHÁT TRIỂN TỪ GIỮA THẾ KỶ 19',true,28,'công',1.4],['EIFFEL KHÔNG PHẢI KỸ SƯ DUY NHẤT',false,28,'Eiffel',5.0]]);
// 16: 1938 gia cố dầm
PH(16,'p','lb16',900,600,'CẦU DO EIFFEL XÂY Ở PHÁP (ẢNH MINH HỌA)',[['HÃNG EIFFEL GIA CỐ DẦM',true,38,'hãng',1.4],['ĐỂ CẦU CHỊU TẢI NẶNG HƠN',false,34,'để',3.6]],'1938');
// 17: chiến tranh, bom đánh hư nhiều nhịp (vẽ phẳng)
S2(17,17,'d',null,g=>{const sp=[];for(let i=0;i<8;i++){const b=el(g,'g',{});el(b,'rect',{x:-48,y:-26,width:96,height:52,rx:6,fill:'#6d7378',stroke:'#fff','stroke-width':6});el(b,'path',{d:'M-48 24 L-24 -24 L0 24 L24 -24 L48 24',fill:'none',stroke:'#2d3236','stroke-width':5});sp.push(b)}
 const half=el(g,'rect',{x:0,y:0,width:10,height:40,rx:8,fill:'#f2c14e',stroke:'#fff','stroke-width':6});const A=strip('BOM ĐÁNH HƯ NHIỀU NHỊP',true,38,171),B=strip('NAY CÒN KHOẢNG MỘT NỬA',false,38,172);const gone=[1,3,4,6];
 return{upd:t=>{const e=popv(t,R(17)+.1,.6);const w=AT(17,'bom',2.2),w2=AT(17,'Nay',7.0);sp.forEach((b,i)=>{const gi=gone.indexOf(i);const u=gi>=0?inn(t,w+gi*.5,.5):0;PUT(b,170+i*100,560,e*(1-u),1.0,u*(gi%2?18:-18));b.setAttribute('transform',`translate(${170+i*100},${560+u*160}) rotate(${u*(gi%2?25:-25)}) scale(${Math.max(.001,e)})`);b.setAttribute('opacity',e>0?(1-u):0)});const hv=inn(t,w2-.2,.8);half.setAttribute('width',Math.max(1,400*hv));half.setAttribute('transform','translate(340,780)');half.setAttribute('opacity',hv>0?1:0);sh(A,t,540,1085,-1,PV(t,17,'bom',2.2));sh(B,t,540,1195,1,PV(t,17,'Nay',7.0))}}});
// 18: ngày nay: tàu hỏa, xe máy
PH(18,'d','lb18',900,600,'TÀU HỎA TRÊN CẦU LONG BIÊN',[['NGÀY NAY',true,50,'Hiện',.2],['TÀU · XE MÁY · XE ĐẠP · NGƯỜI ĐI BỘ',false,26,'xe',2.0]]);
// 19: 2014 đề nghị xếp hạng
PH(19,'p','lb19',900,600,'CẦU LONG BIÊN NGÀY NAY',[['ĐỀ NGHỊ XẾP HẠNG',true,44,'đề',1.6],['DI TÍCH QUỐC GIA',false,44,'di',3.4]],'2014');
// 20: cầu thép đầu tiên bắc qua sông Hồng
PH(20,'d','lb20',900,560,'HOÀNG HÔN TRÊN SÔNG HỒNG',[['CÂY CẦU THÉP ĐẦU TIÊN',true,42,'cây',2.4],['BẮC QUA SÔNG HỒNG Ở HÀ NỘI',false,32,'bắc',3.6]]);
// 21: câu hỏi cuối (vẽ phẳng)
S2(21,21,'p',null,g=>{const q=T(g,0,0,'?',420,'#e5483f',18,'middle',DK);const A=strip('CÔNG TRÌNH NÀO BẠN TỪNG NGHE',true,30,211),B=strip('LÀ CỦA NGƯỜI NỔI TIẾNG?',true,34,212),C=strip('NHƯNG HÓA RA KHÔNG PHẢI',false,32,213);const f=[0,1,2].map(i=>fig(g,{hat:['#d8c9a0','#c9b27c','#e0d2a8'][i]}));
 return{upd:t=>{const qp=popv(t,R(21)+.2,.7);q.setAttribute('transform',`translate(540,690) rotate(${Math.sin(t*2)*6-4}) scale(${Math.max(.001,qp)*1.05})`);q.setAttribute('opacity',qp>0?1:0);f.forEach((o,i)=>o.at(240+i*300,560,.46,0,inn(t,R(21)+.5+i*.2,.4)*.0));sh(A,t,540,1000,-1,PV(t,21,'Còn',.2));sh(B,t,540,1105,1,PV(t,21,'là',3.0));sh(C,t,540,1215,-1,PV(t,21,'nhưng',5.0))}}},TOTAL);
sx(R(1)+.1,'whoosh',{d:.5,g:.5});
for(let i=1;i<=21;i++)bm(R(i)+.3,i%3!=1);
sx(R(21)+.3,'question',{g:.7});
