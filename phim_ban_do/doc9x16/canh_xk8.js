// ===== Hội An (xk8, nội dung mạch kể). Ảnh: ha7(1) ha2(2) ha4(3) ha5(5) ha6(6) ha8(9) ha1(11) ha13(15) ha11(17). Cảnh 4,7,8,10,12,13,14,16,18,19 vẽ phẳng.
// ===== Dấu ấn riêng: nền ĐÈN LỒNG (nâu rượu vang + họa tiết ô cửa lồng), hàng đèn lồng đung đưa ở mép dưới (y>1560)
{DR1.setAttribute('opacity',0);DR2.setAttribute('opacity',0);
 DARKG.firstChild.setAttribute('fill','#1c0e0a');
 [...PAPG.children].forEach((c,i)=>{if(c.tagName=='g')c.setAttribute('opacity',0);if(c.tagName=='line')c.setAttribute('stroke','rgba(120,60,20,.14)')});
 PAPG.firstChild.setAttribute('fill','#e9d5a6');
 const lat=(p,col,op)=>{const g=el(p,'g',{opacity:op});for(let x=-1080;x<=2160;x+=90)el(g,'line',{x1:x,y1:0,x2:x+1920,y2:1920,stroke:col,'stroke-width':x%270?1.4:2.6});for(let x=0;x<=3240;x+=90)el(g,'line',{x1:x,y1:0,x2:x-1920,y2:1920,stroke:col,'stroke-width':x%270?1.4:2.6});return g};
 lat(DARKG,'#5a2a14',.38);lat(PAPG,'#b07a3a',.22);
 const mkL=(p,col,glow)=>{const g=el(p,'g',{});const L=[];for(let i=0;i<7;i++){const x=70+i*156,k=el(g,'g',{});el(k,'line',{x1:0,y1:-170,x2:0,y2:-34,stroke:'#3a2418','stroke-width':3});el(k,'circle',{r:62,fill:glow,opacity:.16});el(k,'ellipse',{rx:30,ry:38,fill:col[i%col.length],stroke:'#2a140a','stroke-width':3});el(k,'path',{d:'M-30 0 Q0 -14 30 0 M-26 -16 Q0 -28 26 -16 M-26 16 Q0 4 26 16',fill:'none',stroke:'rgba(40,10,0,.45)','stroke-width':2.4});el(k,'rect',{x:-12,y:-44,width:24,height:8,rx:3,fill:'#3a2418'});el(k,'path',{d:'M-10 38 L-10 62 M0 40 L0 70 M10 38 L10 60',stroke:'#d6a43a','stroke-width':3,'stroke-linecap':'round'});L.push([k,x,i])}return L};
 const LD=mkL(DARKG,['#e0452a','#f0a63a','#e0452a','#f2c14e'],'#ffb347'),LP=mkL(PAPG,['#c4301c','#e08a1e','#c4301c','#e0a830'],'#ff9a2e');
 window.THEME_UPD=t=>{for(const L of [LD,LP])for(const [k,x,i] of L){const a=Math.sin(t*1.5+i*1.1)*5;k.setAttribute('transform',`translate(${x},${1740+Math.sin(t*1.1+i)*5}) rotate(${a.toFixed(2)} 0 -170)`)}};
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
// 1: hook
PH(1,'d','ha7',900,620,'CHÙA CẦU · HỘI AN',[['CẦU TRÊN TỜ 20.000 ĐỒNG','base',38,'cây',.8],['CÓ CẢ MỘT NGÔI CHÙA TRÊN CẦU?','ok',32,'chùa',4.6]],null,{fx:.5,fy:.3,z:1.8,w:['chùa',4.0],r:150});
// 2: phố cổ
PH(2,'p','ha2',900,640,'PHỐ CỔ HỘI AN',[['ĐÂY LÀ CHÙA CẦU','base',44,'chùa',1.2],['GỌI LÀ CHÙA, NHƯNG LÀ CÂY CẦU','bad',30,'nhưng',4.4]],null,{fx:.82,fy:.4,z:1.5,w:['phố',2.4],r:140});
// 3: mái ngói bắc qua lạch, vì sao tên chùa
PH(3,'d','ha4',900,600,'CHÙA CẦU HỘI AN',[['MÁI NGÓI BẮC QUA LẠCH NHỎ','base',34,'mái',.2],['VÌ SAO LẠI MANG TÊN CHÙA?','bad',34,'vì',4.0]],null,{fx:.5,fy:.4,z:1.9,w:['vì',4.0],r:150});
// 4: thương cảng, thế kỷ 15 (vẽ phẳng)
S2(4,4,'p',null,g=>{const sea=el(g,'g',{});for(let i=0;i<4;i++)el(sea,'path',{d:`M-100 ${700+i*70} q70 -34 140 0 t140 0 t140 0 t140 0 t140 0 t140 0 t140 0 t140 0`,fill:'none',stroke:i%2?CSTEEL:'#f5efe0','stroke-width':8,'stroke-linecap':'round',opacity:.85});
 const bt=[0,1].map(i=>{const b=el(g,'g',{});el(b,'path',{d:'M-90 0 L90 0 L60 44 L-60 44Z',fill:i?CGOLD:'#8a4a22',stroke:'#fff','stroke-width':7,'stroke-linejoin':'round'});el(b,'line',{x1:0,y1:0,x2:0,y2:-130,stroke:'#fff','stroke-width':8});el(b,'path',{d:'M6 -126 L74 -20 L6 -20Z',fill:'#f5efe0',stroke:'#17120c','stroke-width':6,'stroke-linejoin':'round'});return b});
 const n=bigNum(g,'0',200,CGOLD);const A=strip2('THƯƠNG CẢNG HỘI AN','ok',44,41),B=strip('THEO UNESCO',false,34,42),C=strip('THẾ KỶ',false,40,43);
 return{upd:t=>{const e=popv(t,R(4)+.1,.6);bt.forEach((b,i)=>{const x=-200+((t*60+i*560)%1500);PUT(b,x,720-i*40+Math.sin(t*2+i)*8,e,1,Math.sin(t*1.7+i)*3)});const w=AT(4,'thế',3.4),u=inn(t,w,1.1);n.textContent=String(Math.round(15*u));PUT(n,540,470,popv(t,w,.5),1,-3);shw(C,t,540,330,-1,popv(t,w,.4));shw(A,t,540,1085,-1,PV(t,4,'thương',.9));shw(B,t,540,1195,1,PV(t,4,'Theo',2.2))}}});
// 5: thuyền buôn Nhật (tranh xưa)
PH(5,'d','ha5',900,700,'THUYỀN BUÔN NHẬT BẢN, TRANH XƯA',[['NGƯỜI HOA VÀ NGƯỜI NHẬT','ok',38,'người',1.6],['ẢNH HƯỞNG LỚN NHẤT','base',40,'Ảnh',.2]],null,{fx:.58,fy:.5,z:1.6,w:['thuyền',4.6],r:230,mark:'ok',m:['suốt',6.5]});
// 6: tương truyền người Nhật dựng, năm xây chưa rõ
PH(6,'p','ha6',900,600,'CẦU NHẬT BẢN',[['TƯƠNG TRUYỀN: NGƯỜI NHẬT DỰNG','base',30,'Tương',2.0],['NĂM XÂY: CHƯA XÁC ĐỊNH','bad',34,'nhưng',5.0]],null,{fx:.45,fy:.6,z:1.8,w:['chính',3.4],r:170,mark:'x',m:['chưa',8.0]});
// 7: tên đầu tiên + thủy quái (vẽ phẳng)
S2(7,7,'d',null,g=>{const pl=el(g,'g',{});el(pl,'rect',{x:-300,y:-70,width:600,height:140,rx:26,fill:'#f5efe0',stroke:'#17120c','stroke-width':9});const t1=T(pl,0,22,'CẦU NHẬT BẢN',66,'#17120c',0,'middle','none');t1.setAttribute('stroke','none');const bd=el(g,'g',{});el(bd,'circle',{r:60,fill:CSTEEL,stroke:'#fff','stroke-width':9});const nn=T(bd,0,28,'1',84,'#0b1823',0,'middle','none');nn.setAttribute('stroke','none');
 const mo=el(g,'path',{d:'M180 760 C260 560 340 900 440 700 S620 560 700 760 S880 880 920 700',fill:'none',stroke:CRED,'stroke-width':34,'stroke-linecap':'round',pathLength:1,'stroke-dasharray':1,'stroke-dashoffset':1});const eye=el(g,'circle',{r:13,fill:'#fff',cx:920,cy:700});
 const A=strip2('TÊN THỨ NHẤT','base',44,71),B=strip2('CON THỦY QUÁI (TRUYỀN THUYẾT)','bad',30,72);
 return{upd:t=>{const e=popv(t,R(7)+.1,.6);PUT(pl,540,430+Math.sin(t*1.6)*6,e,1,-2);PUT(bd,190,300,popv(t,R(7)+.4,.5),1,-6);const w=AT(7,'truyền',4.4),u=inn(t,w,1.6);mo.setAttribute('stroke-dashoffset',1-u);mo.setAttribute('opacity',u>0?1:0);PUT(eye,920,700+Math.sin(t*3)*6,u>.95?1:0);shw(A,t,540,1085,-1,PV(t,7,'tên',.8));shw(B,t,540,1195,1,PV(t,7,'con',5.2))}}});
// 8: thủy quái trở mình, cầu đè chặn (vẽ phẳng)
S2(8,8,'p',null,g=>{const mo=el(g,'path',{d:'M160 800 C240 600 330 940 430 740 S620 600 700 800 S880 920 930 740',fill:'none',stroke:CRED,'stroke-width':36,'stroke-linecap':'round'});const bm1=BEAM(g,700);const x8=XX(g);
 const A=strip2('TRUYỀN THUYẾT','bad',48,81),B=strip('MỖI LẦN TRỞ MÌNH: ĐẤT RUNG, NƯỚC LỤT',false,28,82),C=strip2('CẦU DỰNG ĐỂ ĐÈ CHẶN','base',40,83);
 return{upd:t=>{const e=popv(t,R(8)+.1,.6);const w=AT(8,'trở',3.4),sk=inn(t,w,.4)*(1-inn(t,w+2.2,.4));mo.setAttribute('opacity',e>0?1:0);mo.setAttribute('transform',`translate(${Math.sin(t*38)*sk*9},${Math.sin(t*3)*10-sk*30})`);const wc=AT(8,'Cầu',6.4),d=inn(t,wc,.7);PUT(bm1,540,420+d*390,popv(t,wc,.4),1.0,0);PUT(x8,540,800,popv(t,wc+.9,.5),.7,0);shw(A,t,540,1000,-1,PV(t,8,'Người',.2));shw(B,t,540,1105,1,PV(t,8,'mỗi',2.4));shw(C,t,540,1215,-1,PV(t,8,'Cầu',6.4))}}});
// 9: việc được ghi lại
PH(9,'d','ha8',900,600,'CHÙA CẦU HỘI AN',[['TRUYỀN THUYẾT THÌ VẬY','bad',34,'truyền',.6],['NHƯNG CÓ VIỆC ĐƯỢC GHI LẠI','ok',34,'một',2.8]],null,{fx:.5,fy:.42,z:1.8,w:['ghi',3.4],r:160,mark:'ok',m:['hẳn',4.4]});
// 10: 1653 miếu nhỏ trên cầu (vẽ phẳng)
S2(10,10,'p',t=>'1653',g=>{const bd=BEAM(g,760);const sh1=el(g,'g',{});el(sh1,'rect',{x:-110,y:-70,width:220,height:100,fill:'#a8301f',stroke:'#17120c','stroke-width':8});el(sh1,'path',{d:'M-170 -70 L0 -170 L170 -70Z',fill:'#7a3a18',stroke:'#17120c','stroke-width':8,'stroke-linejoin':'round'});el(sh1,'rect',{x:-26,y:-34,width:52,height:64,fill:'#1b0f08'});
 const A=strip2('DÂN LÀNG DỰNG THÊM MIẾU NHỎ','ok',32,101),B=strip('THỜ BẮC ĐẾ TRẤN VŨ',false,40,102);
 return{upd:t=>{const e=popv(t,R(10)+.1,.6);PUT(bd,540,800,e,1,-1);const w=AT(10,'dựng',2.0),d=inn(t,w,.8);const sc=popv(t,w,.5);sh1.setAttribute('transform',`translate(540,${520+(1-d)*-160+Math.sin(t*1.5)*3}) scale(${Math.max(.001,sc)*1.5})`);sh1.setAttribute('opacity',sc>0?1:0);shw(A,t,540,1085,-1,PV(t,10,'dân',.9));shw(B,t,540,1195,1,PV(t,10,'thờ',4.0))}}});
// 11: dân gọi là chùa
PH(11,'p','ha1',900,560,'CHÙA CẦU VỀ ĐÊM',[['CÓ MIẾU TRÊN CẦU','base',44,'miếu',.6],['DÂN GỌI LÀ CHÙA: CHÙA CẦU','ok',34,'chùa',3.6]],null,{fx:.48,fy:.43,z:2.2,w:['dân',2.6],r:120,mark:'ok',m:['chùa',4.8]});
// 12: ba cái tên, tên thứ ba (vẽ phẳng)
S2(12,12,'d',null,g=>{const mkP=(txt,col,sz)=>{const k=el(g,'g',{});el(k,'rect',{x:-190,y:-60,width:380,height:120,rx:22,fill:col,stroke:'#fff','stroke-width':8});const tt=T(k,0,sz*.36,txt,sz,col==CRED?'#fff':'#17120c',0,'middle','none');tt.setAttribute('stroke','none');return k};
 const p1=mkP('CẦU NHẬT BẢN',CSTEEL,40),p2=mkP('CHÙA CẦU',CGOLD,52),p3=mkP('?',CRED,90);const A=strip2('CÂY CẦU CÓ TÊN THỨ BA','bad',40,121),B=strip('DO MỘT VỊ CHÚA ĐẶT',false,40,122);
 return{upd:t=>{const e=popv(t,R(12)+.1,.5);PUT(p1,540,430+Math.sin(t*1.7)*5,e,1,-2);PUT(p2,540,630+Math.sin(t*1.5)*5,popv(t,R(12)+.4,.5),1,2);const w=AT(12,'thứ',2.2);PUT(p3,540,830+Math.sin(t*2)*6,popv(t,w,.5),1,-1);shw(A,t,540,1085,-1,PV(t,12,'tên',1.6));shw(B,t,540,1195,1,PV(t,12,'chúa',5.0))}}});
// 13: 1719 Lai Viễn Kiều (vẽ phẳng)
S2(13,13,'p',t=>'1719',g=>{const bd=el(g,'g',{});el(bd,'rect',{x:-360,y:-110,width:720,height:220,rx:18,fill:'#22120a',stroke:CGOLD,'stroke-width':14});el(bd,'rect',{x:-335,y:-85,width:670,height:170,rx:10,fill:'none',stroke:'#7a5a2a','stroke-width':4});const t1=T(bd,0,22,'LAI VIỄN KIỀU',72,CGOLD,0,'middle','none');t1.setAttribute('stroke','none');
 el(bd,'line',{x1:-200,y1:-110,x2:-200,y2:-250,stroke:'#17120c','stroke-width':6});el(bd,'line',{x1:200,y1:-110,x2:200,y2:-250,stroke:'#17120c','stroke-width':6});
 const A=strip2('CHÚA NGUYỄN PHÚC CHU ĐẶT TÊN','base',30,131),B=strip2('CẦU ĐÓN KHÁCH PHƯƠNG XA','ok',40,132);
 return{upd:t=>{const e=popv(t,R(13)+.1,.6);const w=AT(13,'Lai',3.0);bd.setAttribute('transform',`translate(540,600) rotate(${Math.sin(t*1.4)*2.2} 0 -250) scale(${Math.max(.001,popv(t,w,.6))})`);bd.setAttribute('opacity',popv(t,w,.6)>0?1:0);shw(A,t,540,1085,-1,PV(t,13,'chúa',.9));shw(B,t,540,1195,1,PV(t,13,'cầu',6.4))}}});
// 14: ba cái tên (vẽ phẳng)
S2(14,14,'d',null,g=>{const mkP=(txt,col,sz)=>{const k=el(g,'g',{});el(k,'rect',{x:-190,y:-50,width:380,height:100,rx:20,fill:col,stroke:'#fff','stroke-width':8});const tt=T(k,0,sz*.36,txt,sz,'#17120c',0,'middle','none');tt.setAttribute('stroke','none');return k};
 const p1=mkP('CẦU NHẬT BẢN',CSTEEL,36),p2=mkP('CHÙA CẦU',CGOLD,46),p3=mkP('LAI VIỄN KIỀU',CGOLD,36);const ck=[0,1,2].map(()=>CK(g));const n=bigNum(g,'3',230,CGOLD);const A=strip2('MỘT CÂY CẦU, BA CÁI TÊN','ok',40,141),B=strip('MỖI TÊN KỂ MỘT LỚP LỊCH SỬ',false,34,142);
 return{upd:t=>{const e=popv(t,R(14)+.1,.5);const P=[p1,p2,p3];P.forEach((p,i)=>{PUT(p,380,360+i*150+Math.sin(t*1.6+i)*4,popv(t,R(14)+.2+i*.5,.5),1,(i-1)*2);PUT(ck[i],640,360+i*150,popv(t,R(14)+.6+i*.5,.5),.5,0)});PUT(n,850,500,popv(t,AT(14,'ba',4.6),.5),1,-6);shw(A,t,540,1085,-1,PV(t,14,'Thế',3.2));shw(B,t,540,1195,1,PV(t,14,'mỗi',6.0))}}});
// 15: vì sao phố cổ còn nguyên
PH(15,'p','ha13',900,520,'PHỐ CỔ HỘI AN VỀ ĐÊM',[['VÌ SAO PHỐ CỔ CÒN NGUYÊN?','bad',34,'vì',.6]],null,{fx:.45,fy:.5,z:1.6,w:['phố',1.4],r:220});
// 16: thương cảng suy giảm, phố cổ giữ nguyên (vẽ phẳng)
S2(16,16,'d',null,g=>{const ax=el(g,'path',{d:'M140 380 L140 820 L940 820',fill:'none',stroke:'#f5efe0','stroke-width':8,'stroke-linecap':'round'});const ln=el(g,'path',{d:'M170 420 L330 450 L480 520 L650 650 L800 760 L920 800',fill:'none',stroke:CRED,'stroke-width':16,'stroke-linecap':'round','stroke-linejoin':'round',pathLength:1,'stroke-dasharray':1,'stroke-dashoffset':1});const dt=el(g,'circle',{r:20,fill:CRED,stroke:'#fff','stroke-width':6});
 const hs=el(g,'g',{});el(hs,'rect',{x:-90,y:-50,width:180,height:100,fill:CGOLD,stroke:'#17120c','stroke-width':7});el(hs,'path',{d:'M-120 -50 L0 -130 L120 -50Z',fill:'#8a4a22',stroke:'#17120c','stroke-width':7,'stroke-linejoin':'round'});const ck=CK(g);const n=bigNum(g,'0',120,CRED);
 const A=strip('THEO UNESCO',false,36,161),B=strip2('THƯƠNG CẢNG SUY GIẢM','bad',40,162),C=strip2('PHỐ CỔ GIỮ NGUYÊN VẸN','ok',40,163);
 return{upd:t=>{const e=popv(t,R(16)+.1,.5);ax.setAttribute('opacity',e>0?1:0);const w=AT(16,'suy',2.4),u=inn(t,w,1.6);ln.setAttribute('stroke-dashoffset',1-u);const pts=[[170,420],[330,450],[480,520],[650,650],[800,760],[920,800]];const k=u*5,i=Math.min(4,Math.floor(k)),f=k-i;PUT(dt,pts[i][0]+(pts[i+1][0]-pts[i][0])*f,pts[i][1]+(pts[i+1][1]-pts[i][1])*f,u>0?1:0);const wn=AT(16,'thế',3.2);n.textContent=String(Math.round(19*inn(t,wn,.8)));PUT(n,540,300,popv(t,wn,.5),1,-2);const wh=AT(16,'Nhờ',6.2);PUT(hs,300,560,popv(t,wh,.5),1,-2);PUT(ck,420,470,popv(t,wh+.7,.5),.6,0);shw(A,t,300,1000,-1,PV(t,16,'Theo',.2));shw(B,t,540,1105,1,PV(t,16,'thương',1.4));shw(C,t,540,1215,-1,PV(t,16,'phố',7.0))}}});
// 17: 1999 Di sản thế giới
PH(17,'d','ha11',900,600,'PHỐ CỔ HỘI AN VỀ ĐÊM',[['DI SẢN THẾ GIỚI','ok',48,'Di',2.4],['PHỐ CỔ HỘI AN','base',44,'phố',.9]],'1999',{fx:.5,fy:.42,z:1.7,w:['công',1.6],r:200,mark:'ok',m:['Di',3.0]});
// 18: tờ tiền 20.000 đồng (vẽ phẳng, biểu tượng minh họa)
S2(18,18,'p',null,g=>{const nt=el(g,'g',{});el(nt,'rect',{x:-380,y:-190,width:760,height:380,rx:26,fill:'#2f78b8',stroke:'#fff','stroke-width':10});el(nt,'rect',{x:-350,y:-160,width:700,height:320,rx:16,fill:'none',stroke:'rgba(255,255,255,.55)','stroke-width':4});const nm=T(nt,-190,-70,'20.000',84,'#fff',0,'middle','none');nm.setAttribute('stroke','none');
 const br=el(nt,'g',{transform:'translate(120,40)'});el(br,'path',{d:'M-170 70 L170 70 L170 100 L-170 100Z',fill:'#17426c'});el(br,'path',{d:'M-120 70 L-120 20 L120 20 L120 70',fill:'#a8301f',stroke:'#17120c','stroke-width':5});el(br,'path',{d:'M-160 20 L0 -70 L160 20Z',fill:'#7a3a18',stroke:'#17120c','stroke-width':6,'stroke-linejoin':'round'});
 const A=strip2('CHÙA CẦU TRÊN TỜ 20.000 ĐỒNG','ok',34,181),B=strip('ÍT AI BIẾT CÂU CHUYỆN PHÍA SAU',false,32,182);
 return{upd:t=>{const e=popv(t,R(18)+.1,.6);nt.setAttribute('transform',`translate(540,${620+Math.sin(t*1.4)*8}) rotate(${-5+Math.sin(t*1.1)*2.5}) scale(${Math.max(.001,e)})`);nt.setAttribute('opacity',e>0?1:0);shw(A,t,540,1085,-1,PV(t,18,'hình',.8));shw(B,t,540,1195,1,PV(t,18,'ít',6.0))}}});
// 19: câu hỏi cuối (vẽ phẳng)
S2(19,19,'d',null,g=>{const q=T(g,0,0,'?',420,'#e5483f',18,'middle',DK);const mkP=(txt,col,sz)=>{const k=el(g,'g',{});el(k,'rect',{x:-190,y:-46,width:380,height:92,rx:20,fill:col,stroke:'#fff','stroke-width':8});const tt=T(k,0,sz*.36,txt,sz,'#17120c',0,'middle','none');tt.setAttribute('stroke','none');return k};
 const p=[mkP('CẦU NHẬT BẢN',CSTEEL,34),mkP('CHÙA CẦU',CGOLD,44),mkP('LAI VIỄN KIỀU',CGOLD,34)];const A=strip2('BẠN ĐANG ĐI TRÊN','base',40,191),B=strip2('CÂY CẦU CỦA AI?','bad',52,192);
 return{upd:t=>{const qp=popv(t,R(19)+.3,.7);q.setAttribute('transform',`translate(540,520) rotate(${Math.sin(t*2)*5-4}) scale(${Math.max(.001,qp)*1.05})`);q.setAttribute('opacity',qp>0?1:0);p.forEach((o,i)=>PUT(o,540,860+i*0+(i-1)*118+Math.sin(t*1.8+i)*5,popv(t,R(19)+.2+i*.35,.5),1,(i-1)*2));shw(A,t,540,1085,-1,PV(t,19,'khi',3.4));shw(B,t,540,1200,1,PV(t,19,'cây',5.0))}}},TOTAL);
sx(R(1)+.1,'whoosh',{d:.5,g:.5});
for(let i=1;i<=19;i++)bm(R(i)+.3,i%3!=1);
sx(R(19)+.3,'question',{g:.7});
