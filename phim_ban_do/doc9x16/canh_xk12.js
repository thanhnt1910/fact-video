// ===== Chùa Một Cột (xk12). Ảnh: mc1(1) mc3(2) mc7(3) mc6(4) mc2(5) mc8(8) mc5(10) mc4(12). Cảnh 6,7,9,11 vẽ phẳng.
// ===== Dấu ấn riêng: nền AO SEN (xanh ngọc), vòng sóng nước lan ở đáy khung (y>1580)
{DR1.setAttribute('opacity',0);DR2.setAttribute('opacity',0);
 DARKG.firstChild.setAttribute('fill','#0f2523');
 [...PAPG.children].forEach(c=>{if(c.tagName=='g')c.setAttribute('opacity',0);if(c.tagName=='line')c.setAttribute('stroke','rgba(40,110,100,.12)')});
 PAPG.firstChild.setAttribute('fill','#dcead9');
 const mk=(p,col)=>{const g=el(p,'g',{});const rs=[0,1,2].map(i=>el(g,'ellipse',{cx:540,cy:1740,rx:10,ry:3,fill:'none',stroke:col,'stroke-width':4}));return rs};
 const a=mk(DARKG,'#5fb3a5'),b=mk(PAPG,'#2f8a7a');
 const lot=(p,x,y,c)=>{const g=el(p,'g',{opacity:.55,transform:`translate(${x},${y})`});for(let i=-2;i<=2;i++)el(g,'ellipse',{cx:i*18,cy:-Math.abs(i)*6,rx:12,ry:30,fill:c,transform:`rotate(${i*22} ${i*18} 0)`});return g};
 lot(DARKG,160,1760,'#e58aa6');lot(DARKG,900,1700,'#f0b0c4');lot(PAPG,160,1760,'#e58aa6');lot(PAPG,900,1700,'#f0b0c4');
 window.THEME_UPD=t=>{[a,b].forEach(rs=>rs.forEach((e,i)=>{const u=((t*.35+i/3)%1);e.setAttribute('rx',40+u*420);e.setAttribute('ry',10+u*70);e.setAttribute('opacity',(1-u)*.8)}))};
}

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
// ảnh + dải chữ + zoom tới đúng chỗ đang nói + vòng khoanh chạy tới + dấu ✗/✓. F={fx,fy,z,w:[từ,dự phòng],r,mark:'x'|'ok',m:[từ,dự phòng]}
const PH=(n,bg,key,mw,mh,lab,items,yr,F)=>S2(n,n,bg,yr?(t=>yr):null,g=>{const c=card(key,IMG+key+'.jpg',mw,mh,n*10+1);const L=lab?strip2(lab,'base',lab.length>34?22:26,n*10+2):null;const S=items.map((it,i)=>strip2(it[0],it[1],it[2],n*10+3+i));
 const rad=F&&F.r||130,col=F&&F.mark=='x'?CRED:CGOLD;const rg=F?el(c.top,'g',{}):null,rr=F?ring(rg,0,0,rad,col):null;const mkk=F&&F.mark?(F.mark=='x'?XX(c.top):CK(c.top)):null;
 return{upd:t=>{const e=inn(t,R(n)-.2,.6),rt=inn(t,R(n),E(n)-R(n));c.at(540,630,(n%2?-2:2)+Math.sin(t*1.1)*.5,1,e);
  if(!F)c.zoom(1+.1*rt,.5,.5);
  else{const tz=AT(n,F.w[0],F.w[1]),q=inn(t,tz,.9),ox=.5+(F.fx-.5)*q,oy=.5+(F.fy-.5)*q,s=1+.05*rt+(F.z-1)*q+.08*inn(t,tz+.9,Math.max(1,E(n)-tz));c.zoom(s,ox,oy);
   const px=-c.w/2+F.fx*c.w,py=-c.h/2+F.fy*c.h,qx=-c.w/2+ox*c.w,qy=-c.h/2+oy*c.h,X=qx+s*(px-qx),Y=qy+s*(py-qy);
   rg.setAttribute('transform',`translate(${X.toFixed(1)},${Y.toFixed(1)})`);rr.set(inn(t,tz+.35,.7));
   if(mkk){const tm=AT(n,F.m[0],F.m[1]);PUT(mkk,X+rad*.95,Y-rad*.8,popv(t,tm,.5),.5,0)}}
  if(L)shw(L,t,540,338,-1,e);items.forEach((it,i)=>shw(S[i],t,540,1085+i*110,(i%2?1:-1),PV(t,n,it[3],it[4])))}}});
const PAG=(g,top=true,tilt=0)=>{const k=el(g,'g',{});const pil=el(k,'g',{transform:`rotate(${tilt})`});el(pil,'rect',{x:-34,y:-20,width:68,height:300,fill:'#b9b2a4',stroke:'#17120c','stroke-width':7});const up=el(pil,'g',{});if(top){el(up,'rect',{x:-130,y:-120,width:260,height:100,fill:'#5a3a24',stroke:'#17120c','stroke-width':7});el(up,'path',{d:'M-190 -118 Q-120 -150 0 -230 Q120 -150 190 -118 Q100 -126 0 -190 Q-100 -126 -190 -118Z',fill:'#8a4a2a',stroke:'#17120c','stroke-width':7,'stroke-linejoin':'round'});for(let i=0;i<4;i++)el(up,'rect',{x:-96+i*60,y:-104,width:20,height:70,fill:'#17120c'})}return{k,up,pil}};
const POND=(g,w=860)=>{const k=el(g,'g',{});el(k,'rect',{x:-w/2,y:280,width:w,height:150,rx:20,fill:'#2f6d6a',stroke:'#fff','stroke-width':8});for(let i=0;i<3;i++)el(k,'ellipse',{cx:-250+i*250,cy:350,rx:60,ry:14,fill:'none',stroke:'rgba(255,255,255,.4)','stroke-width':4});return k};
// 1 hook: thuốc nổ
PH(1,'d','mc1',940,700,'CHÙA MỘT CỘT · HÀ NỘI',[['BỊ ĐẶT THUỐC NỔ NĂM 1954','bad',32,'thuốc',2.8],['CHÙA HÔM NAY LÀ BẢN DỰNG LẠI?','base',30,'bản',5.6]],null,{fx:.44,fy:.3,z:1.9,w:['thuốc',2.8],r:200,mark:'x',m:['bản',6.0]});
// 2 trước đó là gì: bưu thiếp cũ
PH(2,'p','mc3',940,640,'BƯU THIẾP CŨ: CHÙA MỘT CỘT',[['VẬY TRƯỚC ĐÓ NÓ LÀ GÌ?','bad',38,'trước',.4],['PHẦN NÀO CÒN NGUYÊN TỪ XƯA?','ok',32,'phần',2.8]],null,{fx:.4,fy:.5,z:1.7,w:['phần',2.8],r:200});
// 3 năm 1049 vua Lý Thái Tông
PH(3,'d','mc7',560,900,'TƯỢNG VUA LÝ THÁI TÔNG TRONG CHÙA',[['XÂY CHÙA DIÊN HỰU','ok',38,'xây',3.8],['TÊN GỐC CỦA CHÙA MỘT CỘT','base',32,'tên',6.4]],'1049',{fx:.35,fy:.2,z:1.9,w:['xây',3.8],r:150,mark:'ok',m:['gốc',7.4]});
// 4 mơ thấy Quan Âm, cột đá giữa ao (ảnh tượng Quan Âm)
PH(4,'p','mc6',940,640,'TƯỢNG QUAN ÂM TRONG CHÙA',[['VUA NẰM MƠ THẤY PHẬT QUAN ÂM','base',28,'mơ',2.4],['DỰNG CỘT ĐÁ GIỮA AO LÀM TÒA SEN','ok',28,'dựng',8.0]],null,{fx:.55,fy:.35,z:1.6,w:['Phật',3.6],r:180});
// 5 cột đá giữa ao vuông
PH(5,'d','mc2',940,700,'CỘT ĐÁ GIỮA AO VUÔNG',[['MỘT CỘT ĐÁ GIỮA AO','base',36,'cột',1.4],['NHƯ ĐÓA SEN NỔI TRÊN NƯỚC','ok',34,'đóa',5.4]],null,{fx:.47,fy:.82,z:1.9,w:['cột',1.4],r:170,mark:'ok',m:['sen',6.2]});
// 6 tháng 9 năm 1954, thuốc nổ (vẽ phẳng)
S2(6,6,'d',t=>'9/1954',g=>{const P=PAG(g,true,0);const pd=POND(g);const bs=el(g,'g',{});for(let i=0;i<12;i++){const a=i/12*Math.PI*2;el(bs,'path',{d:`M0 0 L${Math.cos(a-.12)*190} ${Math.sin(a-.12)*190} L${Math.cos(a)*(i%2?300:240)} ${Math.sin(a)*(i%2?300:240)} L${Math.cos(a+.12)*190} ${Math.sin(a+.12)*190}Z`,fill:i%2?CRED:CGOLD,stroke:'#fff','stroke-width':5})}const sm=[];for(let i=0;i<5;i++)sm.push(el(g,'circle',{r:60+i*14,fill:'rgba(70,60,55,.7)'}));const A=strip2('TRƯỚC LÚC PHÁP RÚT KHỎI HÀ NỘI','base',30,61),B=strip2('CÓ NGƯỜI ĐẶT THUỐC NỔ','bad',40,62);
 return{upd:t=>{const e=popv(t,R(6)+.1,.6);PUT(pd,540,640,e,1,0);const w=AT(6,'thuốc',3.8),u=inn(t,w,.5);const sh=u>0&&u<1?Math.sin(t*60)*8:0;PUT(P.k,540+sh,720,e,1.25,0);const bu=popv(t,w+.2,.3);PUT(bs,540,640,bu*(1.2-inn(t,w+.2,.9)*.5),1.0,t*40);bs.setAttribute('opacity',Math.max(0,1-inn(t,w+.5,1.0)));sm.forEach((c,i)=>{const v=inn(t,w+.3+i*.1,2.4);c.setAttribute('transform',`translate(${540+(i-2)*60},${620-v*320})`);c.setAttribute('opacity',(1-v)*.8*(u>0?1:0))});P.up.setAttribute('opacity',1-inn(t,w+.1,.3));shw(A,t,540,1085,-1,PV(t,6,'Rồi',.2));shw(B,t,540,1195,1,PV(t,6,'thuốc',3.8))}}});
// 7 cột đá chỉ hơi nghiêng (vẽ phẳng)
S2(7,7,'p',null,g=>{const P=PAG(g,false,0);const pd=POND(g);const ru=el(g,'g',{});for(let i=0;i<7;i++)el(ru,'polygon',{points:'-24,0 20,-10 28,16 -14,20',fill:'#6a4a30',stroke:'#17120c','stroke-width':5,transform:`translate(${-130+i*45},${-10-(i%3)*18})`});const ck=CK(g,CGOLD);const A=strip2('PHẦN TRÊN SÀN BỊ PHÁ HỎNG','bad',34,71),B=strip2('CỘT ĐÁ CHỈ HƠI NGHIÊNG','ok',38,72);
 return{upd:t=>{const e=popv(t,R(7)+.1,.6);PUT(pd,540,640,e,1,0);const w=AT(7,'cột',5.6),u=inn(t,w,1.2);P.pil.setAttribute('transform',`rotate(${u*5})`);PUT(P.k,540,720,e,1.25,0);PUT(ru,540,690,popv(t,R(7)+.4,.6),1,0);PUT(ck,780,500,popv(t,w+.8,.5),1.1,0);shw(A,t,540,1085,-1,PV(t,7,'phá',1.0));shw(B,t,540,1195,1,PV(t,7,'cột',5.6))}}});
// 8 năm 1955 dựng lại
PH(8,'d','mc8',940,700,'CHÙA MỘT CỘT SAU KHI DỰNG LẠI',[['CHÍNH QUYỀN PHỤC HỒI CHÙA','base',32,'phục',2.8],['NĂM 1955 CHÙA DỰNG LẠI','ok',38,'dựng',6.0]],'1955',{fx:.5,fy:.38,z:1.7,w:['dựng',6.0],r:200,mark:'ok',m:['dựng',6.2]});
// 9 Nguyễn Bá Lăng: bản vẽ (vẽ phẳng)
S2(9,9,'p',null,g=>{const sc=el(g,'g',{});el(sc,'rect',{x:-380,y:-250,width:760,height:500,rx:12,fill:'#e8dcc0',stroke:'#17120c','stroke-width':8});for(let i=0;i<12;i++)el(sc,'line',{x1:-380,y1:-250+i*45,x2:380,y2:-250+i*45,stroke:'rgba(80,110,160,.25)','stroke-width':2});const P=PAG(sc,true,0);P.k.setAttribute('transform','translate(0,-40) scale(.95)');const nm=el(g,'g',{});el(nm,'rect',{x:-260,y:-60,width:520,height:110,rx:24,fill:CGOLD,stroke:'#fff','stroke-width':8});const nt=T(nm,0,24,'NGUYỄN BÁ LĂNG',52,'#17120c',0,'middle','none');nt.setAttribute('stroke','none');const A=strip2('NGƯỜI NGHIÊN CỨU HỌA ĐỒ','base',36,91),B=strip2('ĐIỀU KHIỂN CÔNG TRƯỜNG','ok',38,92);
 return{upd:t=>{const e=popv(t,R(9)+.1,.6);PUT(sc,540,600,e,1,Math.sin(t*1.2)*1);const w=AT(9,'ông',5.0);PUT(nm,540,1000+Math.sin(t*1.7)*5,popv(t,w,.5),1,-2);shw(A,t,540,1085,-1,PV(t,9,'nghiên',.4));shw(B,t,540,1195,1,PV(t,9,'điều',3.0))}}});
// 10 chỉ cột đá còn nguyên từ thời Lý
PH(10,'p','mc5',640,900,'TRỤ ĐÁ DƯỚI CHÙA',[['PHẦN ĐÁNG TIN LÀ CÒN NGUYÊN','base',28,'đáng',2.0],['TỪ THỜI LÝ LÀ CỘT ĐÁ','ok',36,'cột',6.0]],null,{fx:.5,fy:.58,z:1.9,w:['cột',6.0],r:160,mark:'ok',m:['Lý',5.4]});
// 11 bị phá rồi dựng lại theo hình sen cũ (vẽ phẳng): trước/sau
S2(11,11,'d',null,g=>{const pd=POND(g);const P1=PAG(g,true,0),P2=PAG(g,true,0);const lt=el(g,'g',{});for(let i=0;i<8;i++){const a=(i-3.5)*.3;el(lt,'ellipse',{cx:Math.sin(a)*90,cy:-Math.cos(a)*90,rx:28,ry:62,fill:i%2?'#f08aa4':'#f8b9c9',stroke:'#fff','stroke-width':5,transform:`rotate(${a*57.3} ${Math.sin(a)*90} ${-Math.cos(a)*90})`})}const A=strip2('BỊ PHÁ GIỮA LÚC ĐỔI CHỦ','bad',34,111),B=strip2('DỰNG LẠI THEO HÌNH SEN CŨ','ok',34,112);
 return{upd:t=>{const e=popv(t,R(11)+.1,.6);PUT(pd,540,640,e,1,0);const w=AT(11,'dựng',4.8),u=inn(t,w,1.4);PUT(P1.k,540,720,e*(1-u),1.25,0);PUT(P2.k,540,720,u,1.25,0);P1.k.setAttribute('opacity',(1-u)*e);PUT(lt,540,520,popv(t,w+1.0,.7),1.3,0);shw(A,t,540,1085,-1,PV(t,11,'bị',.3));shw(B,t,540,1195,1,PV(t,11,'dựng',4.8))}}});
// 12 câu hỏi cuối
PH(12,'d','mc4',940,640,'BƯU THIẾP CŨ: PAGODE MONTÉE SUR UN PILIER',[['NẾU CHỈ CỘT ĐÁ CÒN CỔ','base',34,'chỉ',.4],['THỨ GÌ KHIẾN TA GỌI ĐÂY LÀ CHÙA XƯA?','bad',26,'thứ',3.6]],null,{fx:.55,fy:.45,z:1.7,w:['thứ',3.6],r:200},TOTAL);

sx(R(1)+.1,'whoosh',{d:.5,g:.5});
for(let i=1;i<=12;i++)bm(R(i)+.3,i%3!=1);
sx(R(12)+.3,'question',{g:.7});
