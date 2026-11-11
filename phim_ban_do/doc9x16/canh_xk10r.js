// ===== Đội quân đất nung (xk10). Ảnh: tc2(1) tc7(5) tc5(6) tc8(7) tc3(8) tc1(11) tc6(12). Cảnh 2,3,4,9,10,13 vẽ phẳng.
// ===== Dấu ấn riêng: nền ĐẤT NUNG nâu đỏ có vân đất nứt, bụi đất mịn trôi chậm ở mép dưới (y>1540)
{DR1.setAttribute('opacity',0);DR2.setAttribute('opacity',0);
 DARKG.firstChild.setAttribute('fill','#2a140c');
 [...PAPG.children].forEach((c,i)=>{if(c.tagName=='g')c.setAttribute('opacity',0);if(c.tagName=='line')c.setAttribute('stroke','rgba(120,60,30,.14)')});
 PAPG.firstChild.setAttribute('fill','#e6c9a6');
 const cracks=(p,col,op,seed)=>{const g=el(p,'g',{opacity:op});const r=rng(seed);for(let i=0;i<26;i++){let x=r()*1080,y=r()*1920,d=`M${x.toFixed(0)} ${y.toFixed(0)}`;for(let j=0;j<5;j++){x+=(r()-.5)*160;y+=(r()-.3)*140;d+=` L${x.toFixed(0)} ${y.toFixed(0)}`}el(g,'path',{d,fill:'none',stroke:col,'stroke-width':2.4+r()*2,'stroke-linecap':'round','stroke-linejoin':'round'})}return g};
 cracks(DARKG,'#6a3418',.5,7);cracks(PAPG,'#a8683c',.3,8);
 const mkD=(p,col)=>{const g=el(p,'g',{});const r=rng(5);const D=[];for(let i=0;i<46;i++){const c=el(g,'circle',{r:2+r()*3.5,fill:col,opacity:.5});D.push([c,r()*1080,1560+r()*320,.2+r()*.6,r()*6])}return D};
 const DD=mkD(DARKG,'#d9a070'),DP=mkD(PAPG,'#9a6034');
 window.THEME_UPD=t=>{for(const D of [DD,DP])for(const [c,x,y,sp,ph] of D){c.setAttribute('cx',((x+t*28*sp)%1100).toFixed(1));c.setAttribute('cy',(y+Math.sin(t*.8+ph)*14).toFixed(1))}};
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

// ===== Bộ vẽ phẳng dùng chung cho bản viết lại #16–#19
const SHEET=(g,w,h,seed)=>{const k=el(g,'g',{});el(k,'rect',{x:-w/2,y:-h/2,width:w,height:h,rx:10,fill:'#efe6cf',stroke:'#17120c','stroke-width':7});const r=rng(seed);for(let i=0;i<Math.floor(h/46)-1;i++)el(k,'line',{x1:-w/2+40,y1:-h/2+50+i*46,x2:w/2-40-r()*130,y2:-h/2+50+i*46,stroke:'rgba(60,50,40,.35)','stroke-width':5,'stroke-linecap':'round'});return k};
const TOWER=(g,col='#7a6652',sw=7)=>{const k=el(g,'g',{});el(k,'path',{d:'M-90 260 L-14 -250 L14 -250 L90 260 Z',fill:col,stroke:'#17120c','stroke-width':sw,'stroke-linejoin':'round'});for(let i=0;i<5;i++){const y=-160+i*85,w=14+i*17;el(k,'path',{d:`M${-w} ${y} L${w} ${y+45} M${w} ${y} L${-w} ${y+45}`,stroke:'#17120c','stroke-width':4})}el(k,'rect',{x:-6,y:-310,width:12,height:60,fill:'#17120c'});return k};
const WV=(g,col,n=3)=>[...Array(n)].map(()=>el(g,'circle',{fill:'none',stroke:col,'stroke-width':7,r:1,opacity:0}));
const WVU=(ws,t,R0,cx,cy,sp=.5,on=1)=>ws.forEach((e,i)=>{const u=((t*sp+i/ws.length)%1);e.setAttribute('cx',cx);e.setAttribute('cy',cy);e.setAttribute('r',10+u*R0);e.setAttribute('opacity',(1-u)*.85*on)});
const BIG=(g,txt,size,fill='#fff',stroke='#17120c')=>{const k=el(g,'g',{});const a=T(k,0,size*.36,txt,size,fill,stroke?14:0,'middle',stroke||'none');a.setAttribute('font-weight',900);return {k,set:s=>{a.textContent=s}}};
const POLEFLAG=(g,col='#da251d')=>{const k=el(g,'g',{});el(k,'rect',{x:-8,y:-300,width:16,height:600,fill:'#b9b2a4',stroke:'#17120c','stroke-width':6});const f=el(k,'path',{d:'M8 -296 L240 -296 L240 -150 L8 -150Z',fill:col,stroke:'#17120c','stroke-width':6});return{k,f}};
const PEOPLE=(g,n,col,seed)=>{const k=el(g,'g',{});const r=rng(seed);for(let i=0;i<n;i++){const x=(i-(n-1)/2)*70,h=70+r()*18;el(k,'circle',{cx:x,cy:-h-18,r:17,fill:col,stroke:'#17120c','stroke-width':4});el(k,'rect',{x:x-17,y:-h,width:34,height:h,rx:12,fill:col,stroke:'#17120c','stroke-width':4})}return k};
const FIG=(g,cols)=>{const k=el(g,'g',{});el(k,'rect',{x:-70,y:-20,width:140,height:260,rx:30,fill:cols[1],stroke:'#17120c','stroke-width':7});el(k,'circle',{cx:0,cy:-95,r:62,fill:cols[0],stroke:'#17120c','stroke-width':7});el(k,'rect',{x:-90,y:60,width:180,height:50,rx:12,fill:cols[2],stroke:'#17120c','stroke-width':6});return k};
const PUZ=(g,seed,n)=>{const k=el(g,'g',{});const r=rng(seed);for(let i=0;i<n;i++){const x=(r()-.5)*640,y=(r()-.3)*200,a=r()*360;el(k,'polygon',{points:'-34,-8 20,-24 38,12 -10,26',fill:i%2?'#a8643f':'#8a4a2a',stroke:'#17120c','stroke-width':5,transform:`translate(${x},${y}) rotate(${a})`})}return k};
const PHONE=(g)=>{const k=el(g,'g',{});el(k,'rect',{x:-90,y:-170,width:180,height:340,rx:34,fill:'#2b2f36',stroke:'#fff','stroke-width':8});el(k,'rect',{x:-72,y:-140,width:144,height:250,rx:10,fill:'#9fd0e8'});el(k,'circle',{cx:0,cy:140,r:16,fill:'#fff'});return k};
PH(1,'d','tc2',700,940,'ĐẦU TƯỢNG LÍNH ĐẤT NUNG',[['ĐẦU TƯỢNG ĐẦU TIÊN','base',34,'đầu',.6],['BỊ VỨT NGOÀI ĐỒNG CHO TRẺ CHƠI?','bad',28,'vứt',3.0]],null,{fx:.5,fy:.3,z:1.8,w:['vứt',3.0],r:190,mark:'x',m:['vứt',3.6]});
PH(2,'p','tc7',940,330,'KHU LĂNG TẦN THỦY HOÀNG (TÂY AN)',[['MẤY ANH EM NÔNG DÂN ĐI ĐÀO GIẾNG','base',28,'mấy',1.0],['CÁCH LĂNG KHOẢNG 1,5 KM','ok',34,'cách',5.2]],null,{fx:.5,fy:.5,z:1.5,w:['cách',5.2],r:130});
sx(R(2)+1.2,'dig',{g:.8});sx(R(2)+1.9,'dig',{g:.7});
PH(3,'d','tc4',940,640,'NÔNG DÂN YANG XINMAN, MỘT NGƯỜI TRONG NHÓM PHÁT HIỆN',[['THẤY MỘT CÁI ĐẦU TƯỢNG','base',34,'đầu',3.4],['YANG ZHIFA TƯỞNG LÀ CÁI BÌNH','bad',28,'bình',8.0]],null,{fx:.5,fy:.4,z:1.5,w:['bình',8.0],r:170,mark:'x',m:['bình',8.4]});
sx(R(3)+.5,'clink',{g:.8});
S2(4,4,'p',null,g=>{const pz=PUZ(g,4,10);const kids=PEOPLE(g,3,'#c4553f',41);const A=strip2('MẢNH VỠ BỊ VỨT NGOÀI ĐỒNG','bad',36,41),B=strip2('TRẺ CON NHẶT LÀM ĐỒ CHƠI','base',34,42);
 return{upd:t=>{const e=popv(t,R(4)+.1,.6);PUT(pz,540,700,e,1.25,0);const w=AT(4,'trẻ',3.8);PUT(kids,540,900,popv(t,w,.6),1.1,0);kids.setAttribute('transform',`translate(${540+Math.sin(t*1.5)*40},${900+Math.sin(t*3)*8}) scale(1.1)`);shw(A,t,540,1130,-1,PV(t,4,'vứt',2.0));shw(B,t,540,1235,1,PV(t,4,'trẻ',3.8))}}});
sx(R(4)+2.0,'thud',{g:.5});sx(R(4)+2.5,'thud',{g:.4});
S2(5,5,'d',t=>'4/1974',g=>{const ph=PHONE(g);const ws=WV(g,CGOLD,3);const nm=el(g,'g',{});el(nm,'rect',{x:-280,y:-60,width:560,height:120,rx:26,fill:CGOLD,stroke:'#fff','stroke-width':8});const nt=T(nm,0,18,'ZHAO KANGMIN',48,'#17120c',0,'middle','none');const A=strip2('MỘT CÚ ĐIỆN THOẠI BÁO TIN','base',34,51),B=strip2('NGƯỜI DUY NHẤT LO DI VẬT HUYỆN LÂM ĐỒNG','ok',24,52);
 return{upd:t=>{const e=popv(t,R(5)+.1,.6);PUT(ph,540,560,e,1,Math.sin(t*28)*3*(e>.9?1:0));WVU(ws,t,300,540,560,.9,e);PUT(nm,540,900,popv(t,AT(5,'Zhao',3.0),.5),1,-2);shw(A,t,540,1130,-1,PV(t,5,'một',.4));shw(B,t,540,1235,1,PV(t,5,'người',5.0))}}});
for(let i=0;i<4;i++)sx(R(5)+.3+i*.55,'tit',{f:1700,g:.6});
PH(6,'p','tc6',940,640,'KHAI QUẬT TẠI HỐ TƯỢNG',[['TỰ HỌC KHẢO CỔ QUA TẠP CHÍ','base',30,'tự',.4],['NHẶT TỪNG MẢNH, KỂ CẢ MẢNH BẰNG MÓNG TAY','ok',24,'nhặt',3.8]],null,{fx:.5,fy:.55,z:1.7,w:['nhặt',3.8],r:200,mark:'ok',m:['móng',6.4]});
sx(AT(6,'nhặt',3.8),'clink',{g:.6});sx(AT(6,'nhặt',3.8)+.8,'clink',{g:.5});
PH(7,'d','tc5',940,640,'KHU PHỤC CHẾ TƯỢNG SAU KHAI QUẬT',[['MANG VỀ BẢO TÀNG VÀ GHÉP LẠI','ok',30,'mang',.6],['CHIẾN BINH CAO BẰNG NGƯỜI THẬT','base',28,'chiến',4.6]],null,{fx:.45,fy:.5,z:1.6,w:['chiến',4.6],r:200});
sx(R(7)+1.0,'clink',{g:.6});sx(R(7)+4.7,'chime',{g:.4});
S2(8,8,'p',null,g=>{const hd=el(g,'g',{});el(hd,'circle',{cx:0,cy:0,r:120,fill:'#a8643f',stroke:'#17120c','stroke-width':8});el(hd,'rect',{x:-60,y:100,width:120,height:150,fill:'#8a4a2a',stroke:'#17120c','stroke-width':8});const hm=el(g,'g',{});el(hm,'rect',{x:-30,y:-260,width:60,height:260,fill:'#6a4a30',stroke:'#17120c','stroke-width':6});el(hm,'rect',{x:-120,y:-320,width:240,height:90,rx:14,fill:'#6d7378',stroke:'#17120c','stroke-width':6});const xx=XX(g);const A=strip2('CÁCH MẠNG VĂN HÓA: ĐỒ CŨ CÓ THỂ BỊ ĐẬP','bad',24,81),B=strip2('ÔNG KHÔNG VỘI BÁO LÊN CẤP CAO','base',30,82);
 return{upd:t=>{const e=popv(t,R(8)+.1,.6);PUT(hd,540,700,e,1,0);const w=AT(8,'đập',4.0),u=inn(t,w-.6,.5);PUT(hm,680-u*40,600+u*140,popv(t,w-.7,.4)*(1-inn(t,w+.7,.4)),1,-30+u*30);PUT(xx,540,700,popv(t,AT(8,'lo',5.6),.5),1.2,0);shw(A,t,540,1130,-1,PV(t,8,'Cách',1.8));shw(B,t,540,1235,1,PV(t,8,'không',6.2))}}});
sx(AT(8,'đập',4.0),'thud',{f:55,g:.9});
S2(9,9,'d',null,g=>{const sh0=SHEET(g,520,640,91);const hl=el(g,'g',{});const r1=el(hl,'rect',{x:-210,y:-250,width:420,height:90,rx:8,fill:CRED});const t1=T(hl,0,-190,'TIN',58,'#fff',0,'middle','none');const mouth=BIG(g,'!',220,CGOLD,'#fff');const A=strip2('XIN NHÀ BÁO: ĐỪNG VIẾT','bad',34,92),B=strip2('TÂN HOA XÃ VẪN ĐƯA TIN','ok',34,93);
 return{upd:t=>{const e=popv(t,R(9)+.1,.6);PUT(sh0,540,640,e,1,-2+Math.sin(t*1.3));PUT(hl,540,640,popv(t,AT(9,'Nhà',3.6),.5),1,-2);PUT(mouth.k,860,480,popv(t,AT(9,'xin',2.4),.5),1,10);shw(A,t,540,1130,-1,PV(t,9,'xin',2.4));shw(B,t,540,1235,1,PV(t,9,'vẫn',5.0))}}});
sx(AT(9,'Nhà',3.6),'paper',{g:.7});sx(AT(9,'vẫn',5.0),'stamp',{g:.6});
PH(10,'p','tc1',940,630,'TƯỢNG NGỰA VÀ LÍNH ĐẤT NUNG SAU KHAI QUẬT',[['KHÔNG AI RA LỆNH PHÁ','ok',36,'không',.4],['KHAI QUẬT CHÍNH THỨC: HƠN 500 TƯỢNG','ok',28,'năm',6.0]],null,{fx:.5,fy:.5,z:1.5,w:['năm',6.0],r:200,mark:'ok',m:['năm',6.4]});
sx(AT(10,'năm',6.0),'chime',{g:.5});
S2(11,11,'d',null,g=>{const f=FIG(g,['#e6b89a','#8a4a2a','#3a6a4a']);const flk=[...Array(10)].map((_,i)=>el(g,'polygon',{points:'0,0 28,-8 36,18 4,26',fill:['#c0392b','#3a6a4a','#6a3a8a'][i%3],stroke:'#17120c','stroke-width':4}));const num=BIG(g,'0',190,CRED,'#fff');const A=strip2('TƯỢNG TỪNG ĐƯỢC SƠN NHIỀU MÀU','base',30,111),B=strip2('GẶP KHÔNG KHÍ KHÔ: SƠN CUỘN LẠI','bad',26,112);
 return{upd:t=>{const e=popv(t,R(11)+.1,.6);PUT(f,380,700,e,1.2,0);const w=AT(11,'mười',6.0),u=inn(t,w,4.0);num.set(Math.round(u*15)+' s');PUT(num.k,800,640,popv(t,w-.3,.5),.8,0);flk.forEach((p,i)=>{const v=inn(t,w+.3+i*.2,1.8);p.setAttribute('transform',`translate(${380+((i*53)%160)-80},${620+v*260}) rotate(${v*180})`);p.setAttribute('opacity',v>0&&v<1?1:0)});shw(A,t,540,1130,-1,PV(t,11,'sơn',1.4));shw(B,t,540,1235,1,PV(t,11,'cuộn',6.8))}}});
S2(12,12,'p',null,g=>{const f=FIG(g,['#e6b89a','#c0392b','#3a6a4a']);const fg=FIG(g,['#a8643f','#a8643f','#8a4a2a']);const flk=[...Array(12)].map((_,i)=>el(g,'polygon',{points:'0,0 28,-8 36,18 4,26',fill:['#c0392b','#3a6a4a','#6a3a8a'][i%3],stroke:'#17120c','stroke-width':4}));const num=BIG(g,'0:00',170,CRED,'#fff');const A=strip2('CHỪNG 4 PHÚT: MÀU BONG GẦN HẾT','bad',28,121),B=strip2('NGÀY NAY TƯỢNG MÀU ĐẤT','base',32,122);
 return{upd:t=>{const e=popv(t,R(12)+.1,.6);const w=AT(12,'bốn',1.0),u=inn(t,w,3.5);PUT(f,380,700,e*(1-u),1.2,0);PUT(fg,380,700,e*u,1.2,0);const m=Math.round(u*4);num.set(m+':00');PUT(num.k,800,640,popv(t,w-.3,.5),.8,0);flk.forEach((p,i)=>{const v=inn(t,w+.2+i*.25,1.8);p.setAttribute('transform',`translate(${380+((i*47)%170)-85},${600+v*300}) rotate(${v*220})`);p.setAttribute('opacity',v>0&&v<1?1:0)});shw(A,t,540,1130,-1,PV(t,12,'bốn',1.0));shw(B,t,540,1235,1,PV(t,12,'ngày',5.0))}}});
sx(AT(12,'bốn',1.0),'rip',{g:.5});
PH(13,'d','tc9',700,940,'TƯỢNG LÍNH ĐẤT NUNG',[['CHÍNH PHỦ CÔNG NHẬN ÔNG ZHAO','ok',28,'chính',2.2],['LÀ NGƯỜI PHÁT HIỆN RA ĐỘI QUÂN','base',28,'là',6.0]],'1990',{fx:.5,fy:.25,z:1.7,w:['chính',2.2],r:190,mark:'ok',m:['công',3.6]});
sx(AT(13,'công',3.6),'stamp',{g:.8});
S2(14,14,'p',null,g=>{const A0=el(g,'g',{});el(A0,'ellipse',{cx:0,cy:60,rx:110,ry:40,fill:'#2b2f36',stroke:'#fff','stroke-width':8});el(A0,'rect',{x:-8,y:-200,width:16,height:240,fill:'#6a4a30',stroke:'#17120c','stroke-width':5});el(A0,'rect',{x:-50,y:-250,width:100,height:70,rx:10,fill:'#6d7378',stroke:'#17120c','stroke-width':5});const B0=PUZ(g,14,6);const q=BIG(g,'?',330,CRED,'#fff');const A=strip2('NGƯỜI ĐÀO GIẾNG','base',40,141),B=strip2('HAY NGƯỜI NHẶT TỪNG MẢNH VỠ?','bad',32,142);
 return{upd:t=>{const e=popv(t,R(14)+.1,.6);PUT(A0,300,700,e,1.2,0);PUT(B0,780,820,e,.85,0);PUT(q.k,540,430,popv(t,AT(14,'ai',.8),.5),1,Math.sin(t*2)*5);shw(A,t,540,1130,-1,PV(t,14,'người',3.2));shw(B,t,540,1235,1,PV(t,14,'hay',5.0))}}},TOTAL);
sx(R(14)+.3,'wind',{d:2.2,g:.4});

sx(R(1)+.1,'whoosh',{d:.5,g:.5});
for(let i=1;i<=14;i++)bm(R(i)+.3,i%3!=1);
sx(R(14)+.3,'question',{g:.7});
