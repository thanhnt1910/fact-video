// ===== tập 3 "Trưng Vương": cảnh vẽ thẳng lên bản đồ =====
const W=(n,w,o=0,def=2)=>{const sp=((window.SPOK&&SPOK[48000+n])||'').split(/\s+/).filter(Boolean),A=(window.ASRW&&ASRW[48000+n])||[];let c=-1;for(let i=0;i<sp.length;i++){if(nw(sp[i])===nw(w)){c++;if(c===o)return A.length>1?Math.max(0,A[Math.min(A.length-1,Math.round(i/sp.length*A.length))]-.1):def}}return def};
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

const SP=[107.0,23.7],CZC={lon:107.0,lat:23.84,z:400};
function pillar(){const g=mk();
 el(g,'ellipse',{cx:0,cy:8,rx:84,ry:16,fill:'#000',opacity:.38});
 el(g,'rect',{x:-58,y:-28,width:116,height:30,rx:4,fill:'#7a5a30',stroke:DK,'stroke-width':4});
 el(g,'rect',{x:-44,y:-56,width:88,height:30,rx:4,fill:'#8c6a38',stroke:DK,'stroke-width':4});
 el(g,'path',{d:'M-28 -56 L-21 -330 L21 -330 L28 -56Z',fill:'#b57d2c',stroke:DK,'stroke-width':5,'stroke-linejoin':'round'});
 el(g,'path',{d:'M-14 -60 L-10 -326 L2 -326 L-2 -60Z',fill:'#e0aa55',opacity:.75});
 [[-140,.5],[-210,.4],[-260,.35]].forEach(a=>el(g,'path',{d:`M-26 ${a[0]} L-23 ${a[0]-38} L-18 ${a[0]-6} L-22 ${a[0]+28}Z`,fill:'#4f9a78',opacity:a[1]}));
 [-120,-200].forEach(y=>el(g,'rect',{x:-26+(-y-120)*.012,y:y-9,width:52-(-y-120)*.024,height:18,rx:3,fill:'#7a5424',stroke:DK,'stroke-width':3.5}));
 el(g,'path',{d:'M-38 -330 L-46 -356 L46 -356 L38 -330Z',fill:'#c08a34',stroke:DK,'stroke-width':5,'stroke-linejoin':'round'});
 el(g,'ellipse',{cx:0,cy:-356,rx:46,ry:10,fill:'#e0aa55',stroke:DK,'stroke-width':4});
 lab(g,'Cột đồng',-392,46,GOLD);
 g.crack=el(g,'path',{d:'M4 -250 L-8 -210 L8 -176 L-6 -140',fill:'none',stroke:DK,'stroke-width':6,'stroke-linecap':'round','stroke-linejoin':'round',opacity:0});
 g.glow=el(g,'ellipse',{cx:0,cy:-190,rx:120,ry:210,fill:'url(#halo)',opacity:0});
 return g}
function rock(r=14){const g=mk();el(g,'ellipse',{rx:r*1.2,ry:r*.8,fill:'#9a9890',stroke:DK,'stroke-width':3.5});el(g,'ellipse',{cx:-r*.3,cy:-r*.25,rx:r*.5,ry:r*.28,fill:'#c8c6bc',opacity:.7});return g}
const RK=[[-70,14,15],[-44,22,13],[-18,18,16],[10,24,14],[38,16,15],[66,22,13],[-58,36,12],[-28,40,14],[0,38,13],[30,40,14],[56,36,12],[-40,-6,11],[-8,-4,12],[24,-4,11],[48,-8,10]];
// C1: biên giới nhà Hán trên bản đồ rộng
scene(R(1)-.2,R(1)+2.9,WIDE,()=>{const wall=pathLine(GOLD,12,'26 12');const tx=mk();lab(tx,'biên giới nhà Hán',0,40,GOLD);
 return {yr:'42 SCN',upd:(u,t)=>{hideNine();const k=ease(cl((t-R(1)-W(1,'cột',0,1.6))/1.2));const a=P(104.6,23.7),b=P(109.6,23.7);wall.setAttribute('d',`M${a[0]} ${a[1]} L${lerp(a[0],b[0],k)} ${a[1]}`);wall.setAttribute('opacity',k);plc(tx,107.0,24.35);tx.setAttribute('opacity',ease(cl((k-.5)/.4)));setTint(107.0,23.0,3.2,1.6,GOLD,.18)}}});
// C2: phóng vào chân cột, cột đồng, lời truyền, đá chất
scene(R(1)+2.9,E(3)+.3,CZC,()=>{const pl=pillar();const tag=mk();lab(tag,'hình minh họa · vị trí ước đoán',0,26,WH);const wall=pathLine(GOLD,8,'20 12');wall.setAttribute('opacity',.55);const rks=RK.map(r=>rock(r[2]));const pa=pawn('#d9c7a0',1.1);const pb=pawn('#efe4c8',1.1);
 return {yr:'42 SCN',upd:(u,t)=>{hideNine();const a=P(105.7,SP[1]),b=P(108.3,SP[1]);wall.setAttribute('d',`M${a[0]} ${a[1]} L${b[0]} ${a[1]}`);const k=pop(t,1,W(1,'dựng',0,2.8)+.4,.6);const p=plc(pl,SP[0],SP[1],k);pl.glow.setAttribute('opacity',ease(cl((t-R(2)-W(2,'Cột',0,2.8))/.6))*.8);const kc=ease(cl((t-R(2)-W(2,'gãy',0,3.8))/.4));pl.crack.setAttribute('opacity',kc);const pt=plc(tag,SP[0],SP[1]-.62,ease(cl((t-R(1)-4.2)/.5)));const tr=cl((t-R(3)-W(3,'đá',0,2.2))/3.0);const base=P(SP[0],SP[1]);rks.forEach((g,i)=>{const on=cl(tr*RK.length-i);const q=ease(on);plc(g,SP[0],SP[1],.001);g.setAttribute('transform',`translate(${base[0]+RK[i][0]*1.5},${base[1]+RK[i][1]*1.5-(1-q)*26}) scale(${q||.001})`)});const m=ease(cl((t-R(3)-.2)/2.2));plc(pa,SP[0]-1.1+m*.55,SP[1]-.25,m>0?1:.001);plc(pb,SP[0]+1.1-m*.55,SP[1]-.25,m>0?1:.001);setTint(107.0,23.5,1.6,1.4,'#c98a3a',.2)}}});
