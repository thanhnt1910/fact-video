// ===== tập 3 "Trưng Vương": cảnh vẽ thẳng lên bản đồ =====
const W=(n,w,o=0,def=2)=>{const sp=((window.SPOK&&SPOK[47000+n])||'').split(/\s+/).filter(Boolean),A=(window.ASRW&&ASRW[47000+n])||[];let c=-1;for(let i=0;i<sp.length;i++){if(nw(sp[i])===nw(w)){c++;if(c===o)return A.length>1?Math.max(0,A[Math.min(A.length-1,Math.round(i/sp.length*A.length))]-.1):def}}return def};
const fi=(t,n,d,w=.5)=>ease(cl((t-R(n)-d)/w));
const pop=(t,n,d,w=.4)=>Math.max(.001,back(cl((t-R(n)-d)/w)));
const CV={lon:105.4,lat:20.1,z:330},MID={lon:106.4,lat:21.15,z:142};
const UY=[107.5,24.4];
function bnr(txt,col=GOLD){const g=mk();const t=T(g,0,0,txt,30,col,6);const w=t.getComputedTextLength()+44;const r=el(g,'rect',{x:1040-w,y:198,width:w,height:62,rx:18,fill:'#0c0a08',opacity:.78,stroke:col,'stroke-width':3});g.insertBefore(r,t);t.setAttribute('x',1040-w/2);t.setAttribute('y',240);return g}
function shrine(){const g=mk();el(g,'ellipse',{cx:0,cy:4,rx:44,ry:8,fill:'#000',opacity:.3});el(g,'rect',{x:-28,y:-24,width:56,height:26,fill:'#d9c7a0',stroke:DK,'stroke-width':4});el(g,'rect',{x:-8,y:-20,width:16,height:22,fill:'#6b2a18'});el(g,'path',{d:'M-46 -22 Q0 -66 46 -22 L34 -24 Q0 -54 -34 -24Z',fill:GOLD,stroke:DK,'stroke-width':4,'stroke-linejoin':'round'});el(g,'path',{d:'M-30 -42 L0 -62 L30 -42Z',fill:'#b32a22',stroke:DK,'stroke-width':4,'stroke-linejoin':'round'});return g}
function fish(col='#8fd8ff'){const g=mk();el(g,'ellipse',{rx:22,ry:11,fill:col,stroke:DK,'stroke-width':3.5});el(g,'path',{d:'M20 0 L38 -11 L38 11Z',fill:col,stroke:DK,'stroke-width':3.5,'stroke-linejoin':'round'});el(g,'circle',{cx:-11,cy:-2,r:2.6,fill:DK});return g}
function coin(){const g=mk();el(g,'circle',{r:14,fill:GOLD,stroke:DK,'stroke-width':4});el(g,'rect',{x:-4.5,y:-4.5,width:9,height:9,fill:'none',stroke:DK,'stroke-width':2.5});return g}
function gift(){const g=mk();el(g,'rect',{x:-24,y:-18,width:48,height:34,rx:4,fill:RED,stroke:DK,'stroke-width':4});el(g,'rect',{x:-5,y:-18,width:10,height:34,fill:GOLD});el(g,'path',{d:'M0 -18 Q-20 -42 -10 -24 M0 -18 Q20 -42 10 -24',stroke:GOLD,'stroke-width':5,fill:'none','stroke-linecap':'round'});return g}
function cross(sz=26){const g=mk();el(g,'path',{d:`M${-sz} ${-sz} L${sz} ${sz} M${sz} ${-sz} L${-sz} ${sz}`,stroke:'#ff3b30','stroke-width':12,'stroke-linecap':'round'});el(g,'path',{d:`M${-sz} ${-sz} L${sz} ${sz} M${sz} ${-sz} L${-sz} ${sz}`,stroke:'#fff','stroke-width':4,'stroke-linecap':'round'});return g}
function heart(){const g=mk();el(g,'path',{d:'M0 14 C-30 -8 -16 -30 0 -14 C16 -30 30 -8 0 14Z',fill:'#ff5c7a',stroke:DK,'stroke-width':4,'stroke-linejoin':'round'});return g}
function field(col='#7fcf5a'){const g=mk();el(g,'path',{d:'M-46 18 L-30 -22 L46 -22 L30 18Z',fill:col,stroke:DK,'stroke-width':4,'stroke-linejoin':'round',opacity:.95});for(let i=-2;i<=2;i++)el(g,'path',{d:`M${i*16-8} 16 L${i*16+2} -20`,stroke:'#2f6b2a','stroke-width':3.5,'stroke-linecap':'round'});return g}
function scroll(){const g=mk();el(g,'rect',{x:-50,y:-34,width:100,height:68,rx:8,fill:'#efe3c0',stroke:DK,'stroke-width':4});el(g,'rect',{x:-58,y:-40,width:12,height:80,rx:6,fill:'#b8873a',stroke:DK,'stroke-width':3.5});el(g,'rect',{x:46,y:-40,width:12,height:80,rx:6,fill:'#b8873a',stroke:DK,'stroke-width':3.5});for(let i=0;i<4;i++)el(g,'path',{d:`M-34 ${-18+i*13} L34 ${-18+i*13}`,stroke:'#8a6a38','stroke-width':3.5,'stroke-linecap':'round'});return g}
const route=(a,b,u)=>[lerp(a[0],b[0],u),lerp(a[1],b[1],u)];

const ML=[105.45,21.3],CD=[105.7,20.35],HP=[109.2,21.7],ND=[107.2,24.7];
const WIDE2={lon:109.4,lat:23.4,z:112};
function flag(col='#d8392f'){const g=mk();el(g,'path',{d:'M0 0 L0 -90',stroke:DK,'stroke-width':8,'stroke-linecap':'round'});el(g,'path',{d:'M3 -88 L58 -74 L3 -52Z',fill:col,stroke:DK,'stroke-width':4,'stroke-linejoin':'round'});return g}
function crown(){const g=mk();el(g,'path',{d:'M-30 0 L-34 -34 L-16 -18 L0 -42 L16 -18 L34 -34 L30 0Z',fill:GOLD,stroke:DK,'stroke-width':5,'stroke-linejoin':'round'});return g}
function boat(){const g=mk();el(g,'path',{d:'M-34 -6 L34 -6 L22 12 L-22 12Z',fill:'#8a5a2b',stroke:DK,'stroke-width':4,'stroke-linejoin':'round'});el(g,'path',{d:'M0 -6 L0 -44 L24 -10Z',fill:'#efe3c0',stroke:DK,'stroke-width':3.5,'stroke-linejoin':'round'});return g}
function wheel(){const g=mk();el(g,'rect',{x:-30,y:-24,width:60,height:22,rx:4,fill:'#8a5a2b',stroke:DK,'stroke-width':4});[-18,18].forEach(x=>{el(g,'circle',{cx:x,cy:2,r:11,fill:'#c9a064',stroke:DK,'stroke-width':4})});return g}
const RN=(()=>{let a=7;return()=>{a=(a*1103515245+12345)&2147483647;return a/2147483647}})();
const DOTS=[[107.62,23.06],[104.46,20.62],[104.43,23.15],[109.69,23.92],[107.76,22.18],[104.83,19.18],[105.02,20.31],[104.08,21.42],[108.86,22.64],[105.76,20.25],[109.55,23.34],[103.9,20.15],[104.33,22.25],[109.59,22.89],[104.5,19.4],[105.03,22.76],[105.69,23.52],[104.49,24.05],[107.29,23.43],[104.98,19.87],[105.37,20.05],[105.06,23.85],[109.1,22.12],[104.13,23.91],[105.42,23.22],[104.31,20.24],[109.68,22.38],[105.78,24.1],[104.34,21.83],[108.25,22.62],[105.98,22.53],[108.24,22.0],[105.41,19.16],[104.01,19.78],[109.09,23.08],[107.15,22.94],[105.88,23.04],[109.5,19.53],[105.61,22.74],[105.03,22.19],[104.52,22.75],[107.67,21.75],[105.43,19.59],[109.19,23.5],[103.96,20.88],[109.61,21.94],[106.06,20.53],[106.99,23.79],[104.57,23.56],[108.67,22.22],[103.91,23.21],[104.83,23.26],[106.62,23.93],[107.3,22.59],[109.51,19.1],[105.53,22.3],[106.17,23.75],[107.83,23.88],[103.91,21.82],[104.52,19.81],[106.38,20.81],[104.11,22.59],[104.04,19.26],[104.33,21.05],[109.3,22.49]];
function dots(){return DOTS.map(()=>{const g=mk();el(g,'circle',{r:13,fill:'url(#halo)',opacity:.9});el(g,'circle',{r:7,fill:GOLD,stroke:DK,'stroke-width':3});return g})}
const showDots=(ds,k,t,n,d)=>ds.forEach((g,i)=>{const u=cl(((t-R(n)-d)*1)*1/2.4);const on=ease(u)*65>i;plc(g,DOTS[i][0],DOTS[i][1],on?1:.001)});
const tnt=(lo,la,rx,ry,c,o)=>setTint(lo,la,rx,ry,c,o);
function gcCity(col,r=18){const g=city(col,'',r);lab(g,'Giao Chỉ',54,30);return g}
const RED2='#e0524a',PINK='#f4a6b8',VIO='#c9a0f0',BLU='#9fd0ff',TG='#7fcf5a';

const CZ={lon:106.0,lat:20.9,z:200},CZ2={lon:106.0,lat:21.6,z:175};
const lbl2=(txt,col=GOLD,sz=32)=>{const g=mk();lab(g,txt,0,sz,col);return g};
// T1: câu hỏi mở đầu
scene(R(1)-.2,E(1)+.2,WIDE,()=>{const big=mk();T(big,0,0,'?',280,WH,24);
 return {yr:'',upd:(u,t)=>{nine(t,R(1)+.3,GRN,false);setTint(109.5,21.8,4.2,2.6,GRN,.3);plc(big,109.0,24.1,1);big.setAttribute('opacity',ease(cl((t-R(1)-1.0)/.6)))}}});
// T2: 110 TCN chín quận
scene(R(2)-.2,E(2)+.2,WIDE,()=>{const st=mk();el(st,'rect',{x:-70,y:-70,width:140,height:140,rx:16,fill:RED,stroke:WH,'stroke-width':7});T(st,0,18,'HÁN',58,WH,0);const big=mk();T(big,0,0,'9',200,WH,22);T(big,0,58,'QUẬN',54,GOLD,14);
 return {yr:'110 TCN',upd:(u,t)=>{const d=W(2,'thôn',0,3.2),d2=W(2,'chín',0,6.4);const k=ease(cl((t-R(2)-d)/1.4));nine(t,R(2),hex(mixc(cG,cR,k)),false);setTint(109.5,21.8,4.2,2.6,hex(mixc(cG,cR,k)),.3+.12*k);const sk=ease(cl((t-R(2)-d)/.4));plc(st,112.9,24.2,sk>0?(1+.3*(1-sk))*.9:.001,-8);st.setAttribute('opacity',sk);plc(big,109.0,24.1,1);big.setAttribute('opacity',ease(cl((t-R(2)-d2)/.5)))}}});
// T3: 29 Nhâm Diên, Cửu Chân
scene(R(3)-.2,E(3)+.2,CZ,()=>{const cc=city(GRN,'Cửu Chân',17);const nd=pawn('#fff',1.3,'Nhâm Diên',-92);const f=field();const gf=gift();const he=heart();
 return {yr:'29 SCN',upd:(u,t)=>{hideNine();plc(cc,CC[0],CC[1]);plc(nd,CC[0]-.55,CC[1]+.05,pop(t,3,W(3,'Nhâm',0,.8)));plc(f,105.3,19.05,pop(t,3,W(3,'cày',0,4.8)));plc(gf,104.7,19.4,pop(t,3,W(3,'cưới',0,6.4)));plc(he,104.7,19.95,pop(t,3,W(3,'cưới',0,6.4)+.2,.4)*.9);setTint(105.6,19.8,2.2,1.8,GRN,.28)}}});
// T4: 39 Tô Định
scene(R(4)-.2,E(4)+.2,CZ,()=>{const gc=city(GRN,'Giao Chỉ',17);const td=pawn('#7a1f1a',1.35,'Tô Định',-94);const cs=[0,1,2,3].map(()=>coin());
 return {yr:'39 SCN',upd:(u,t)=>{hideNine();const dd=W(4,'tham',0,2.8),dr=W(4,'tàn',0,4.0);const kr=ease(cl((t-R(4)-dr)/1.2));paint(gc,hex(mixc(cG,cR,kr)));plc(gc,GC[0],GC[1]);plc(td,GC[0]+.45,GC[1]+.05,pop(t,4,W(4,'Tô',0,.4)));cs.forEach((c,i)=>{const k=ease(cl((t-R(4)-dd-i*.3)/1.1));plc(c,lerp(GC[0]-1.0+i*.12,GC[0]+.45,k),lerp(GC[1]-.75-i*.12,GC[1]-.15,k),k>0?1:.001)});setTint(106.2,21.2,2.2,1.8,hex(mixc(cG,cR,kr)),.28)}}});
// T5: 40 Hai Bà, 65 thành
scene(R(5)-.2,E(5)+.2,MID,()=>{const ml=city(GRN,'Mê Linh',18);const ds=dots();const tt=pawn(PINK,1.4,'Trưng Trắc',-92);const tn=pawn(VIO,1.4,'Trưng Nhị',-92);const big=mk();T(big,0,0,'65',130,GOLD,16);T(big,0,50,'THÀNH',42,WH,10);
 return {yr:'40 SCN',upd:(u,t)=>{hideNine();plc(ml,ML[0],ML[1]);plc(tt,ML[0]-.9,ML[1]-.85,pop(t,5,W(5,'Trưng',0,.6)));plc(tn,ML[0]+.9,ML[1]-.85,pop(t,5,W(5,'Nhị',0,1.4)));showDots(ds,0,t,5,W(5,'lấy',0,3.4));const bk=ease(cl((t-R(5)-W(5,'sáu',0,5.0))/.5));plc(big,108.6,23.6,1);big.setAttribute('opacity',bk);setTint(106.8,21.4,3.4,2.6,GRN,.25)}}});
// T6: 42-43 Mã Viện
scene(R(6)-.2,E(6)+.2,CZ2,()=>{const ml=city(GRN,'Mê Linh',17);const mv=pawn('#3a3a48',1.4,'Mã Viện',-92);const tt=pawn(PINK,1.2);const tn=pawn(VIO,1.2);const x=cross(22);const col=mk();el(col,'rect',{x:-13,y:-84,width:26,height:84,fill:'#c98a3a',stroke:DK,'stroke-width':4});el(col,'rect',{x:-24,y:-96,width:48,height:16,rx:4,fill:GOLD,stroke:DK,'stroke-width':4});const bn=bnr('chia lại huyện');
 return {yr:'42–43 SCN',upd:(u,t)=>{hideNine();plc(ml,ML[0],ML[1]);const dm=W(6,'Mã',0,.6),dd=W(6,'đánh',0,2.4);const k=ease(cl((t-R(6)-dm)/(dd-dm+.8)));plc(mv,lerp(107.5,ML[0]+.7,k),lerp(23.7,ML[1]+.0,k),1.4);const out=1-ease(cl((t-R(6)-dd-1.0)/.5));plc(tt,ML[0]-.55,ML[1]-.9,.95);plc(tn,ML[0]+.35,ML[1]-.9,.95);tt.setAttribute('opacity',out);tn.setAttribute('opacity',out);plc(x,ML[0]-.1,ML[1]-.95,ease(cl((t-R(6)-dd-.6)/.3))*1.0||.001);const dc=W(6,'cột',0,5.2);plc(col,107.0,23.0,pop(t,6,dc,.5));const dh=W(6,'chia',0,7.8);bn.setAttribute('opacity',fi(t,6,dh,.4));setTint(106.2,21.4,2.8,2.2,'#3a3a48',.2)}}});
// T7: 160 Hạ Phương
scene(R(7)-.2,E(7)+.2,{lon:106.0,lat:19.7,z:190},()=>{const nn=city(RED,'Nhật Nam',17);const hp=pawn('#fff',1.35,'Hạ Phương',-92);const cr=[0,1,2,3,4,5,6,7].map((i)=>pawn(i%2?'#d9c7a0':'#efe4c8',.8));const big=mk();T(big,0,0,'10.000+',92,GOLD,14);
 return {yr:'160 SCN',upd:(u,t)=>{hideNine();plc(nn,NN[0],NN[1]);plc(hp,105.0,18.9,pop(t,7,W(7,'Hạ',0,.5)));const d=W(7,'hàng',0,5.4)-1.8;cr.forEach((g,i)=>{const k=ease(cl((t-R(7)-d-i*.18)/1.6));plc(g,lerp(104.2+(i%3)*.1,105.25+(i%4)*.06,k),lerp(19.7-(i%2)*.25,19.0-(i%3)*.08,k),k>0?.8:.001)});const bk=ease(cl((t-R(7)-W(7,'hơn',0,3.6))/.5));plc(big,105.3,20.5,1);big.setAttribute('opacity',bk);paint(nn,hex(mixc(cR,cG,ease(cl((t-R(7)-d-1.6)/1.0)))));setTint(105.4,19.0,2.0,1.6,RED,.22)}}});
// T8: sáu mốc
const CP=[[105.3,23.2],[106.7,24.2],[108.1,24.7],[109.5,24.6],[110.9,24.2],[112.1,23.6]],CY=['110','29','39','40','42','160'];
scene(R(8)-.2,E(8)+.2,WIDE,()=>{const ch=CP.map((p,i)=>{const g=mk();el(g,'circle',{r:34,fill:i<2?'#2f7d4a':i==2?'#8a2b24':i==3?'#c04a78':'#3a3a48',stroke:WH,'stroke-width':6});T(g,0,12,CY[i],i==5?30:34,WH,6);return g});const ls=CP.slice(1).map(()=>pathLine(GOLD,5,'10 10'));
 const tx=[['quan tốt',1,'tốt',-.55],['quan tham',2,'tham',.6],['nổi dậy',3,'dậy',-.55],['siết chặt',4,'siết',.6]].map(a=>({g:lbl2(a[0]),i:a[1],w:a[2],dy:a[3]}));
 return {yr:'',upd:(u,t)=>{hideNine();CP.forEach((p,i)=>{const k=pop(t,8,.2+i*.55,.4);plc(ch[i],p[0],p[1],k)});ls.forEach((l,i)=>{const k=ease(cl((t-R(8)-.2-(i+1)*.55+.25)/.4));const a=P(CP[i][0],CP[i][1]),b=P(CP[i+1][0],CP[i+1][1]);l.setAttribute('d',`M${a[0]} ${a[1]} L${a[0]+(b[0]-a[0])*k} ${a[1]+(b[1]-a[1])*k}`);l.setAttribute('opacity',.8*(k>0?1:0))});tx.forEach(o=>{const d=W(8,o.w,0,2.0+o.i);plc(o.g,CP[o.i][0],CP[o.i][1]+o.dy,1);o.g.setAttribute('opacity',fi(t,8,d,.4))});setTint(106.5,21.8,3.4,2.2,GOLD,.15)}}});
// T9: mời xem
scene(R(9)-.2,E(9)+.4,WIDE,()=>{const big=mk();T(big,0,0,'XEM TỪNG TẬP',84,GOLD,14);
 return {yr:'',upd:(u,t)=>{nine(t,R(9)+.2,GRN,false);setTint(109.5,21.8,4.2,2.6,GRN,.3);plc(big,108.8,24.2,1);big.setAttribute('opacity',fi(t,9,.3,.5))}}});
