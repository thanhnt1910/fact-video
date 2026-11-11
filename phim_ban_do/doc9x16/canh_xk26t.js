const VT2='ĐỊA CHẤN KẾ';
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
const WV=(g,col,n=3)=>[...Array(n)].map(()=>el(g,'circle',{fill:'none',stroke:col,'stroke-width':7,r:1,opacity:0}));
const WVU=(ws,t,R0,cx,cy,sp=.5,on=1)=>ws.forEach((e,i)=>{const u=((t*sp+i/ws.length)%1);e.setAttribute('cx',cx);e.setAttribute('cy',cy);e.setAttribute('r',10+u*R0);e.setAttribute('opacity',(1-u)*.85*on)});
const LBL=(g,txt,size=32,col='#fff')=>{const t=T(g,0,0,txt,size,col,9,'middle',DK);t.setAttribute('font-weight',900);return t};
// ===== Lửa Hy Lạp (xk25t). Toàn bộ cảnh vẽ phẳng, không ảnh tư liệu.
const OLN='#0a1018',BRZ='#b8802f',SEAC='#2c5a7e';
const MAN=(g)=>{const k=el(g,'g',{});el(k,'path',{d:'M-62 150 L-46 -20 Q0 -52 46 -20 L62 150Z',fill:'#35507a',stroke:'#fff','stroke-width':7,'stroke-linejoin':'round'});el(k,'circle',{cy:-84,r:46,fill:'#d9b38a',stroke:'#fff','stroke-width':7});el(k,'path',{d:'M-52 -96 Q0 -150 52 -96 L52 -84 Q0 -112 -52 -84Z',fill:'#17120c'});return k};
const SCROLL=(g,w=420,h=300)=>{const k=el(g,'g',{});el(k,'rect',{x:-w/2,y:-h/2,width:w,height:h,rx:12,fill:'#e8dcba',stroke:OLN,'stroke-width':7});el(k,'rect',{x:-w/2-14,y:-h/2-8,width:28,height:h+16,rx:12,fill:'#c9a45a',stroke:OLN,'stroke-width':6});el(k,'rect',{x:w/2-14,y:-h/2-8,width:28,height:h+16,rx:12,fill:'#c9a45a',stroke:OLN,'stroke-width':6});for(let i=0;i<6;i++)el(k,'path',{d:`M${-w/2+40} ${-h/2+36+i*44} L${w/2-40-((i*53)%110)} ${-h/2+36+i*44}`,stroke:'rgba(90,60,30,.55)','stroke-width':7,'stroke-linecap':'round'});return k};
const MLB=(g,txt,sz=30,col='#fff')=>{const t=T(g,0,0,txt,sz,col,10,'middle',OLN);t.setAttribute('font-weight',900);return t};
// ===== Địa chấn kế Trương Hành (xk26t). Cảnh vẽ phẳng, không ảnh tư liệu.
// ===== Dấu ấn riêng: nền xanh ngọc đồng (tối) và giấy xanh lá nhạt (sáng); sóng địa chấn (đường gãy rung) chạy ở đáy khung y>1600; cảnh đặc trưng: bình đồng, rồng và cóc, mặt cắt giả thuyết.
{DR1.setAttribute('opacity',0);DR2.setAttribute('opacity',0);
 DARKG.firstChild.setAttribute('fill','#0a2a28');
 [...PAPG.children].forEach(c=>{if(c.tagName=='g')c.setAttribute('opacity',0);if(c.tagName=='line')c.setAttribute('stroke','rgba(0,0,0,0)')});
 PAPG.firstChild.setAttribute('fill','#dce6d6');
 const rr=rng(2626);
 const ring=(p,col)=>{const g=el(p,'g',{});for(let i=0;i<5;i++)el(g,'circle',{cx:540,cy:760,r:150+i*170,fill:'none',stroke:col,'stroke-width':2.4})};
 ring(DARKG,'rgba(224,166,60,.07)');ring(PAPG,'rgba(30,90,70,.09)');
 const zz=(p,col)=>{const g=el(p,'g',{});const a=[];for(let i=0;i<4;i++){const e=el(g,'path',{d:'M0 0 l30 -26 l30 52 l30 -52 l30 52 l30 -26 l30 0 l30 0',fill:'none',stroke:col,'stroke-width':5,'stroke-linecap':'round','stroke-linejoin':'round'});a.push({e,x:rr()*1400,y:1640+i*58+rr()*20,sp:40+rr()*50,ph:rr()*6})}return a};
 const dA=zz(DARKG,'rgba(224,166,60,.32)'),dB=zz(PAPG,'rgba(20,100,80,.32)');
 window.THEME_UPD=t=>{[dA,dB].forEach(L=>L.forEach(o=>{const x=((o.x+t*o.sp)%1500)-240;o.e.setAttribute('transform',`translate(${x.toFixed(1)},${(o.y+Math.sin(t*14+o.ph)*5).toFixed(1)}) scale(${(1+.18*Math.sin(t*1.1+o.ph)).toFixed(3)},1)`)}))};
}
const CITY=(g)=>{const k=el(g,'g',{});const W='#6a7480';el(k,'rect',{x:-400,y:0,width:800,height:120,fill:W,stroke:'#fff','stroke-width':7});for(let i=0;i<14;i++)el(k,'rect',{x:-392+i*58,y:-20,width:34,height:24,fill:W,stroke:'#fff','stroke-width':5});for(const x of[-330,-110,150,340]){el(k,'rect',{x:x-42,y:-100,width:84,height:220,fill:'#7a8591',stroke:'#fff','stroke-width':7});for(let i=0;i<3;i++)el(k,'rect',{x:x-42+i*30,y:-120,width:24,height:24,fill:'#7a8591',stroke:'#fff','stroke-width':5})}el(k,'path',{d:'M-60 0 Q-60 -150 40 -150 Q140 -150 140 0Z',fill:CGOLD,stroke:'#fff','stroke-width':7});el(k,'path',{d:'M40 -150 L40 -200 M25 -185 L55 -185',stroke:'#fff','stroke-width':9,'stroke-linecap':'round'});el(k,'rect',{x:-22,y:60,width:44,height:60,rx:14,fill:OLN});return k};
const BR2='#8f5f22',GRNC='#2f7f6f';
// ----- hình vẽ phẳng: bình đồng (nhìn ngang), đầu rồng ngậm cầu, cóc há miệng
const DRG=(g,dir=1)=>{const k=el(g,'g',{});el(k,'path',{d:`M0 0 q ${28*dir} -34 ${64*dir} -22 q ${22*dir} 6 ${30*dir} 24 q ${-14*dir} 18 ${-42*dir} 16 q ${-30*dir} 6 ${-52*dir} -18Z`,fill:BRZ,stroke:'#fff','stroke-width':6,'stroke-linejoin':'round'});el(k,'circle',{cx:30*dir,cy:-12,r:5,fill:'#fff'});el(k,'path',{d:`M${6*dir} -26 l${-8*dir} -22 M${24*dir} -32 l${-4*dir} -24`,stroke:'#fff','stroke-width':6,'stroke-linecap':'round'});const ball=el(k,'circle',{cx:62*dir,cy:8,r:15,fill:CGOLD,stroke:OLN,'stroke-width':4});return{k,ball,dir}};
const TOAD=(g)=>{const k=el(g,'g',{});el(k,'ellipse',{rx:48,ry:30,fill:GRNC,stroke:'#fff','stroke-width':6});el(k,'circle',{cx:-22,cy:-26,r:11,fill:GRNC,stroke:'#fff','stroke-width':5});el(k,'circle',{cx:22,cy:-26,r:11,fill:GRNC,stroke:'#fff','stroke-width':5});el(k,'path',{d:'M-24 6 Q0 36 24 6Z',fill:'#07120f',stroke:'#fff','stroke-width':4,'stroke-linejoin':'round'});return k};
// bình: thân, nắp, 4 đầu rồng nhìn thấy (ngậm cầu), 4 cóc phía dưới; upd(t,{drop:idx|-1,shake})
const URN=(g)=>{const k=el(g,'g',{});const body=el(k,'g',{});
 el(body,'path',{d:'M-150 -120 Q-215 50 -150 168 Q-100 215 0 215 Q100 215 150 168 Q215 50 150 -120Z',fill:BRZ,stroke:'#fff','stroke-width':8,'stroke-linejoin':'round'});
 el(body,'path',{d:'M-150 -120 Q0 -245 150 -120Z',fill:BR2,stroke:'#fff','stroke-width':8,'stroke-linejoin':'round'});
 el(body,'path',{d:'M-170 -10 Q0 30 170 -10 M-182 70 Q0 112 182 70',fill:'none',stroke:'rgba(255,255,255,.55)','stroke-width':5});
 const X=[-190,-95,95,190],ds=[],tds=[];
 X.forEach((x,i)=>{const dir=x<0?-1:1;const d=DRG(k,dir);d.k.setAttribute('transform',`translate(${x*.8},${-40+Math.abs(x)*.05})`);ds.push(d);const td=TOAD(k);td.setAttribute('transform',`translate(${x*1.05},${268})`);tds.push(td)});
 const base=el(k,'rect',{x:-110,y:208,width:220,height:22,rx:8,fill:BR2,stroke:'#fff','stroke-width':6});k.insertBefore(base,body.nextSibling);
 const upd=(t,o)=>{const sh=o&&o.shake?Math.sin(t*38)*6*o.shake:0;k.firstChild;body.setAttribute('transform',`translate(${sh},0)`);ds.forEach((d,i)=>{d.k.setAttribute('transform',d.k.getAttribute('transform').replace(/translate\(([^,]+),/,(m,a)=>m));});if(o&&o.drop!=null){ds.forEach((d,i)=>{const hit=o.drop===i;const u=hit?Math.min(1,Math.max(0,o.du)):0;d.ball.setAttribute('cy',8+u*(268-40-8+20));d.ball.setAttribute('opacity',hit&&u>=1?1:1)})}};
 return{k,ds,tds,upd}};
// compass: vòng tròn tám vạch
const COMP=(g,r=150)=>{const k=el(g,'g',{});el(k,'circle',{r,fill:'rgba(10,30,28,.55)',stroke:'#fff','stroke-width':7});for(let i=0;i<8;i++){const a=i*Math.PI/4;el(k,'path',{d:`M${Math.sin(a)*(r-26)} ${-Math.cos(a)*(r-26)} L${Math.sin(a)*r} ${-Math.cos(a)*r}`,stroke:CGOLD,'stroke-width':9,'stroke-linecap':'round'});const dd=el(k,'circle',{cx:Math.sin(a)*(r-50),cy:-Math.cos(a)*(r-50),r:11,fill:BRZ,stroke:'#fff','stroke-width':4})}
 const ar=el(k,'g',{opacity:0});el(ar,'path',{d:`M0 0 L0 ${-(r-30)} M0 ${-(r-30)} l-18 34 M0 ${-(r-30)} l18 34`,stroke:CRED,'stroke-width':12,'stroke-linecap':'round','stroke-linejoin':'round',fill:'none'});return{k,ar}};
// mặt cắt giả thuyết: thân bình, thanh nặng treo, đòn bẩy, quả cầu
const MECHA=(g)=>{const k=el(g,'g',{});const body=el(k,'g',{});el(body,'path',{d:'M-250 -180 Q-330 40 -250 230 Q-180 300 0 300 Q180 300 250 230 Q330 40 250 -180Z',fill:'rgba(184,128,47,.28)',stroke:'#fff','stroke-width':9,'stroke-linejoin':'round'});el(body,'path',{d:'M-250 -180 Q0 -300 250 -180',fill:'none',stroke:'#fff','stroke-width':9});
 el(k,'path',{d:'M-90 -150 L90 -150',stroke:'#fff','stroke-width':8,'stroke-linecap':'round'});
 const pen=el(k,'g',{});el(pen,'path',{d:'M0 0 L0 250',stroke:'#fff','stroke-width':8,'stroke-linecap':'round'});el(pen,'circle',{cy:270,r:44,fill:'#6d7378',stroke:'#fff','stroke-width':7});
 const lv=el(k,'g',{});el(lv,'rect',{x:0,y:-8,width:220,height:16,rx:8,fill:CGOLD,stroke:OLN,'stroke-width':4});
 const dr=el(k,'g',{});el(dr,'path',{d:'M0 0 q 22 -32 54 -20 q 20 6 26 22 q -12 16 -38 14 q -26 4 -42 -16Z',fill:BRZ,stroke:'#fff','stroke-width':6});const ball=el(k,'circle',{r:16,fill:CGOLD,stroke:OLN,'stroke-width':4});
 const upd=(t,o)=>{const sh=o.shake?Math.sin(t*34)*7*o.shake:0;body.setAttribute('transform',`translate(${sh},0)`);pen.setAttribute('transform',`translate(${sh},-150) rotate(${o.tilt*22})`);lv.setAttribute('transform',`translate(${100+sh},40) rotate(${-o.lever*28})`);dr.setAttribute('transform',`translate(${326+sh},-30)`);ball.setAttribute('cx',356+sh);ball.setAttribute('cy',-14+o.ball*380)};
 return{k,upd}};
// ===== các cảnh
// 1: hook, bình đồng, dấu hỏi
S2(1,1,'d',null,g=>{const u=URN(g);const q=T(g,0,0,'?',300,CRED,16,'middle',OLN);const A=strip2('BÌNH ĐỒNG BÁO ĐỘNG ĐẤT','base',40,501),B=strip2('TỪ RẤT XA?','bad',40,502);
 return{upd:t=>{u.upd(t,{shake:inn(t,AT(1,'báo',3.0),1.6)*.6*(1-inn(t,AT(1,'báo',3.0)+2.4,.6))});PUT(u.k,540,720+Math.sin(t*1.4)*4,popv(t,R(1)+.2,.6),1.05,0);PUT(q,540,500,popv(t,AT(1,'từ',5.2),.5),.9,Math.sin(t*2)*5);shw(A,t,540,1085,-1,PV(t,1,'bình',2.0));shw(B,t,540,1195,1,PV(t,1,'từ',5.2))}}});
// 2: Trương Hành, năm 132
S2(2,2,'p',null,g=>{const m=MAN(g);const sc=SCROLL(g,380,260);const big=bigNum(g,'132',180,CGOLD);const lb=MLB(g,'TRƯƠNG HÀNH',42,CGOLD),lb2=MLB(g,'HỌC GIẢ THỜI HÁN',30,'#17120c');const A=strip2('TRƯƠNG HÀNH · THỜI HÁN','base',36,511),B=strip2('DÂNG TRIỀU ĐÌNH NĂM 132','ok',34,512);
 return{upd:t=>{PUT(m,320,700+Math.sin(t*1.5)*4,popv(t,R(2)+.2,.6),1.45,-2);PUT(lb,320,930,popv(t,R(2)+.6,.5),1,0);PUT(lb2,320,975,popv(t,R(2)+.8,.5),1,0);PUT(sc,770,620+Math.sin(t*1.3)*5,popv(t,AT(2,'dâng',3.6),.6),1.0,3);PUT(big,770,470,popv(t,AT(2,'năm',5.4),.55),.9,-2);shw(A,t,540,1085,-1,PV(t,2,'Đó',.6));shw(B,t,540,1195,1,PV(t,2,'dâng',3.6))}}});
// 3: bình lớn, tám rồng
S2(3,3,'d',null,g=>{const u=URN(g);const br=el(g,'path',{d:'M110 1010 L110 1040 L970 1040 L970 1010',fill:'none',stroke:CGOLD,'stroke-width':8,'stroke-linecap':'round','stroke-linejoin':'round'});const lb=MLB(g,'KHOẢNG 1,8 MÉT',36,CGOLD);const A=strip2('BÌNH ĐỒNG LỚN, TÁM ĐẦU RỒNG','base',34,521),B=strip2('MỖI ĐẦU NGẬM MỘT QUẢ CẦU','ok',32,522);
 return{upd:t=>{u.upd(t,{});PUT(u.k,540,640+Math.sin(t*1.4)*3,popv(t,R(3)+.1,.6),1.3,0);br.setAttribute('opacity',popv(t,AT(3,'rộng',1.2),.5)>0?1:0);PUT(lb,540,985,popv(t,AT(3,'rộng',1.2)+.2,.5),1,0);shw(A,t,540,1085,-1,PV(t,3,'lớn',.8));shw(B,t,540,1195,1,PV(t,3,'ngậm',5.2))}}});
// 4: cóc và la bàn
S2(4,4,'p',null,g=>{const d=DRG(g,1);const td=TOAD(g);const cp=COMP(g,150);const lb=MLB(g,'CÓC ĐỒNG HÁ MIỆNG',32,'#17120c'),lb2=MLB(g,'MỖI RỒNG MỘT PHƯƠNG',32,'#17120c');const A=strip2('DƯỚI MỖI RỒNG LÀ MỘT CON CÓC','base',32,531),B=strip2('MỖI RỒNG MỘT PHƯƠNG LA BÀN','ok',32,532);
 return{upd:t=>{PUT(d.k,320,560,popv(t,R(4)+.2,.55),2.4,0);PUT(td,320,960,popv(t,AT(4,'cóc',1.0),.55),2.0,0);PUT(lb,320,1030,popv(t,AT(4,'cóc',1.0)+.3,.5),1,0);cp.k.setAttribute('transform',`translate(790,700) scale(${Math.max(.001,popv(t,AT(4,'phương',4.4),.6))}) rotate(${t*8})`);PUT(lb2,790,900,popv(t,AT(4,'phương',4.4)+.3,.5),1,0);shw(A,t,540,1085,-1,PV(t,4,'Dưới',.2));shw(B,t,540,1195,1,PV(t,4,'Mỗi',4.2))}}});
// 5: đất rung, cầu rơi, tiếng kêu
S2(5,5,'d',null,g=>{const u=URN(g);const wv=WV(g,CRED,3);const A=strip2('ĐẤT RUNG, CẦU RƠI VÀO MIỆNG CÓC','base',32,541),B=strip2('TIẾNG KÊU BÁO NGƯỜI TRỰC','ok',34,542);const rg=WV(g,CGOLD,3);
 return{upd:t=>{const w=AT(5,'cầu',2.0),d0=AT(5,'xuống',3.2),sk=inn(t,R(5)+.2,.4)*(1-inn(t,d0,.3));u.upd(t,{shake:sk,drop:3,du:inn(t,d0,.8)});PUT(u.k,540,660,popv(t,R(5)+.1,.5),1.15,0);WVU(wv,t,260,540,1010,.8,sk>0.1?1:0);WVU(rg,t,160,810,860,.9,popv(t,d0+.8,.3)>0&&t<d0+3?1:0);shw(A,t,540,1085,-1,PV(t,5,'Nếu',.2));shw(B,t,540,1195,1,PV(t,5,'Tiếng',4.6))}}});
// 6: hướng rồng nhả cầu là hướng chấn
S2(6,6,'p',null,g=>{const cp=COMP(g,200);const src=el(g,'g',{});const WW=WV(g,CRED,3);const lb=MLB(g,'NGUỒN RUNG',32,CRED);const A=strip2('RỒNG NÀO NHẢ CẦU','base',38,551),B=strip2('HƯỚNG ẤY LÀ HƯỚNG RUNG CHẤN','ok',32,552);
 return{upd:t=>{const w=AT(6,'rồng',.8);cp.k.setAttribute('transform',`translate(540,680) scale(${Math.max(.001,popv(t,R(6)+.1,.6))})`);cp.ar.setAttribute('opacity',popv(t,AT(6,'nhả',1.8),.4)>0?1:0);cp.ar.setAttribute('transform',`rotate(45)`);WVU(WW,t,150,820,380,.6,popv(t,AT(6,'hướng',3.2),.4)>0?1:0);PUT(lb,820,300,popv(t,AT(6,'hướng',3.2)+.2,.5),1,0);shw(A,t,540,1085,-1,PV(t,6,'Con',.2));shw(B,t,540,1195,1,PV(t,6,'hướng',3.2))}}});
// 7: câu hỏi, làm sao nhạy
S2(7,7,'d',null,g=>{const u=URN(g);const q=T(g,0,0,'?',340,CRED,16,'middle',OLN);const A=strip2('LÀM SAO CẢM NHẬN ĐƯỢC?','bad',38,561),B=strip2('ĐẤT RUNG TỪ RẤT XA','base',34,562);
 return{upd:t=>{u.upd(t,{});PUT(u.k,540,740+Math.sin(t*1.4)*4,popv(t,R(7)+.1,.6),.95,0);PUT(q,540,500,popv(t,AT(7,'làm',.2),.5),.9,Math.sin(t*2)*5);shw(A,t,540,1085,-1,PV(t,7,'làm',.2));shw(B,t,540,1195,1,PV(t,7,'rất',4.4))}}});
// 8: giả thuyết bên trong
S2(8,8,'p',null,g=>{const m=MECHA(g);const gt=strip2('GIẢ THUYẾT','bad',44,571);const l1=MLB(g,'THANH NẶNG / CON LẮC',30,CRED),l2=MLB(g,'ĐÒN BẨY',30,'#17120c');const A=strip2('BÊN TRONG: THANH NẶNG HOẶC CON LẮC','base',30,572),B=strip2('KHÔNG CÒN BẢN VẼ, BẢN GỐC','bad',32,573);
 return{upd:t=>{m.upd(t,{shake:0,tilt:Math.sin(t*1.6)*.06,lever:0,ball:0});PUT(m.k,420,680,popv(t,R(8)+.1,.6),.8,0);shw(gt,t,540,330,-1,popv(t,R(8)+.1,.55));PUT(l1,420,1000,popv(t,AT(8,'thanh',1.2),.5),1,0);PUT(l2,780,780,popv(t,AT(8,'nghiêng',3.0),.5),1,0);shw(A,t,540,1085,-1,PV(t,8,'Các',.2));shw(B,t,540,1195,1,PV(t,8,'Chẳng',5.2))}}});
// 9: sóng tới, nghiêng, đòn bẩy, nhả cầu
S2(9,9,'d',null,g=>{const m=MECHA(g);const gt=strip2('GIẢ THUYẾT','bad',44,581);const WW=WV(g,CGOLD,3);const A=strip2('SÓNG TỚI, CON LẮC NGHIÊNG','base',34,582),B=strip2('ĐÒN BẨY NHẢ ĐÚNG QUẢ CẦU','ok',32,583);
 return{upd:t=>{const a0=AT(9,'sóng',.6),a1=AT(9,'nghiêng',1.8),a2=AT(9,'đòn',3.4),a3=AT(9,'nhả',4.8);const sk=inn(t,a0,.3)*(1-inn(t,a3+.8,.4));m.upd(t,{shake:sk*.8,tilt:inn(t,a1,.8)*(1-inn(t,a3+.8,.6)*.6),lever:inn(t,a2,.7)*(1-inn(t,a3+1.2,.6)),ball:inn(t,a3,.9)});PUT(m.k,420,680,popv(t,R(9)+.05,.5),.8,0);shw(gt,t,540,330,-1,1);WVU(WW,t,300,170,1000,.9,sk>.1?1:0);shw(A,t,540,1085,-1,PV(t,9,'Khi',.2));shw(B,t,540,1195,1,PV(t,9,'Nó',3.4))}}});
// 10: theo lời kể lại, không ai thấy rung
S2(10,10,'p',null,g=>{const u=URN(g);const p=[0,1,2].map(()=>MAN(g));const q=[0,1,2].map(()=>T(g,0,0,'?',120,CRED,10,'middle',OLN));const x=XX(g);const A=strip2('THEO LỜI KỂ LẠI','bad',42,591),B=strip2('CẦU RƠI, NHƯNG KHÔNG AI THẤY RUNG','base',30,592);
 return{upd:t=>{const d0=AT(10,'rơi',1.8);u.upd(t,{drop:1,du:inn(t,d0,.8)});PUT(u.k,330,620,popv(t,R(10)+.1,.6),.75,0);p.forEach((o,i)=>PUT(o,620+i*150,860,popv(t,AT(10,'cả',3.6)+i*.25,.5),.62,0));q.forEach((o,i)=>PUT(o,620+i*150,700+Math.sin(t*2+i)*5,popv(t,AT(10,'ai',4.6)+i*.2,.5),1,0));PUT(x,330,640,popv(t,AT(10,'hỏng',8.2),.5),.8,0);shw(A,t,540,1085,-1,PV(t,10,'Theo',.2));shw(B,t,540,1195,1,PV(t,10,'cầu',1.8))}}});
// 11: sứ giả, vài ngày sau, đúng hướng
S2(11,11,'d',null,g=>{const WW=WV(g,CRED,3);const path=el(g,'path',{d:'M880 400 Q640 560 260 860',fill:'none',stroke:CGOLD,'stroke-width':10,'stroke-dasharray':'22 18','stroke-linecap':'round',pathLength:1});const m=MAN(g);const c=CITY(g);const lb=MLB(g,'HÀNG TRĂM KM',36,CGOLD),lb2=MLB(g,'KINH ĐÔ',34,'#fff');const ck=CK(g);const A=strip2('VÀI NGÀY SAU, SỨ GIẢ BÁO TIN','base',32,601),B=strip2('ĐÚNG HƯỚNG BÌNH CHỈ (LỜI KỂ LẠI)','ok',28,602);
 return{upd:t=>{const w0=AT(11,'sứ',1.8),u=inn(t,w0,3.6);path.setAttribute('stroke-dasharray',`${22} ${18}`);path.setAttribute('opacity',popv(t,R(11)+.2,.5)>0?.9:0);WVU(WW,t,140,880,400,.6,popv(t,R(11)+.3,.5)>0?1:0);const px=880-620*u,py=400+460*Math.pow(u,1.0)-Math.sin(u*Math.PI)*60;PUT(m,px,py,popv(t,w0,.5),.5,0);PUT(c,300,860,popv(t,R(11)+.1,.6),.55,0);PUT(lb2,300,990,popv(t,R(11)+.4,.5),1,0);PUT(lb,590,520,popv(t,AT(11,'hàng',4.0),.5),1,-14);PUT(ck,860,700,popv(t,AT(11,'đúng',7.8),.5),1,0);shw(A,t,540,1085,-1,PV(t,11,'Vài',.2));shw(B,t,540,1195,1,PV(t,11,'đúng',7.8))}}});
// 12: chỉ là lời kể, nghi ngờ độ nhạy, ma sát
S2(12,12,'p',null,g=>{const u=URN(g);const f=[0,1,2].map(i=>el(g,'path',{d:'M0 0 l24 -30 l24 60 l24 -60 l24 30',fill:'none',stroke:CRED,'stroke-width':9,'stroke-linecap':'round','stroke-linejoin':'round'}));const lb=MLB(g,'MA SÁT BÊN TRONG',34,CRED);const A=strip2('CHỈ LÀ LỜI KỂ LẠI','bad',40,611),B=strip2('MA SÁT CÓ THỂ RẤT LỚN','bad',34,612);
 return{upd:t=>{u.upd(t,{});PUT(u.k,540,700+Math.sin(t*1.4)*3,popv(t,R(12)+.1,.6),.9,0);const w=AT(12,'ma',5.4);f.forEach((o,i)=>{const s=popv(t,w+i*.3,.4);const sh=Math.sin(t*22+i)*6;PUT(o,380+i*160+sh,900,s,1,0)});PUT(lb,540,1000,popv(t,w+.2,.5),1,0);shw(A,t,540,1085,-1,PV(t,12,'chuyện',.4));shw(B,t,540,1195,1,PV(t,12,'ma',5.4))}}});
// 13: không còn bản gốc
S2(13,13,'d',null,g=>{const sc=SCROLL(g,480,340);const gh=el(g,'g',{});const u=URN(g);gh.appendChild(u.k);const q=T(g,0,0,'?',320,CRED,16,'middle',OLN);const A=strip2('KHÔNG CÒN BẢN GỐC','bad',40,621),B=strip2('CHƯA AI KHẲNG ĐỊNH ĐỘ NHẠY','bad',32,622);
 return{upd:t=>{const f=inn(t,AT(13,'gốc',2.0),2.4);u.upd(t,{});PUT(u.k,540,620+Math.sin(t*1.4)*3,popv(t,R(13)+.1,.6)*(1-f*.85),.85,0);u.k.setAttribute('opacity',Math.max(.08,1-f*.9));PUT(sc,540,640,popv(t,AT(13,'gốc',2.0),.6)*f,1,-2);PUT(q,540,500,popv(t,AT(13,'chưa',4.2),.5),.8,Math.sin(t*2)*5);shw(A,t,540,1085,-1,PV(t,13,'Vì',.2));shw(B,t,540,1195,1,PV(t,13,'chưa',4.2))}}});
// 14: câu hỏi cuối
S2(14,14,'p',null,g=>{const u=URN(g);const q=T(g,0,0,'?',340,CRED,16,'middle',OLN);const l1=MLB(g,'VƯỢT THỜI ĐẠI',36,'#6b4a10'),l2=MLB(g,'MAY MẮN?',36,CRED);const A=strip2('PHÁT MINH VƯỢT THỜI ĐẠI','ok',38,631),B=strip2('HAY MỘT LẦN MAY MẮN?','bad',38,632);
 return{upd:t=>{u.upd(t,{});PUT(u.k,540,700+Math.sin(t*1.4)*3,popv(t,R(14)+.1,.6),.8,0);PUT(q,540,440,popv(t,AT(14,'Vậy',.2),.5),.8,Math.sin(t*2)*5);PUT(l1,300,1000,popv(t,AT(14,'phát',2.8),.5),1,-4);PUT(l2,780,1000,popv(t,AT(14,'may',6.0),.5),1,4);shw(A,t,540,1085,-1,PV(t,14,'phát',2.8));shw(B,t,540,1195,1,PV(t,14,'hay',5.0))}}});
sx(R(1)+.1,'whoosh',{d:.5,g:.5});
for(let i=1;i<=14;i++)bm(R(i)+.3,i%3!=1);
sx(AT(5,'xuống',3.2)+.4,'ping',{g:.9});sx(AT(9,'nhả',4.8)+.5,'ping',{g:.9});sx(AT(10,'rơi',1.8)+.4,'ping',{g:.8});sx(R(9)+.2,'creak',{g:.5});sx(R(14)+.3,'question',{g:.7});
