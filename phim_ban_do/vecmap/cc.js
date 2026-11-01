// cc.js — minh họa cận cảnh vẽ THẲNG trên bản đồ (không cắt sang cảnh khác).
// Item: {k:'cc', lon, lat, t0, t1, fi, fo}. Mọi hình neo theo tọa độ bản đồ nên phóng to cùng bản đồ;
// huy hiệu chân dung và chữ vẽ ở lớp HUD, neo theo vị trí nhân vật.
(function(){
const A=0.2,cA=Math.cos(A),sA=Math.sin(A);
let K1=1,FX=0,FY=0,SCf=1;
function setup(it){MIR=it.mir?-1:1;SCf=1920/((it.wf||0.15)*G.k*G.scale);K1=1/SCf;const f=P(it.lon,it.lat);FX=f[0];FY=f[1]}
let MIR=1;const Lc=(u,v)=>{u*=MIR;return [FX+(u*cA-v*sA)*K1,FY+(u*sA+v*cA)*K1]};
const toS=(x,y)=>[(x-CAMX)*SC,(y-CAMY)*SC];
const W=px=>px*K1;
const VI={tun:'#8a5a2b',trou:'#5b4026',cloth:'#7a3b1c',arm:'#7a6038'};
const SO={tun:'#3a64a8',trou:'#27487f',iron:'#8a929c',arm:'#5b6470',plume:'#2e4a80'};

// ---------- nhân vật (cao 70 px ở độ phóng đại cuối, quay mặt sang phải) ----------
function fig(P0,x,y,o){
 const al=o.al==null?1:o.al;if(al<=0.01)return;const k=K1*(o.sz||70)/70;
 const g=el('g',{transform:`translate(${x},${y}) rotate(${o.rot||0}) scale(${k*(o.flip?-1:1)},${k})`,opacity:al},P0);
 const col=o.col,tr=o.trou||shadeC(col,.65),sw=1.3,sk=SKIN;
 el('ellipse',{cx:0,cy:0,rx:15,ry:4,fill:'#000',opacity:.16},g);
 if(o.cape)el('path',{d:'M-9,-52 Q-26,-30 -18,-4 L-3,-11 L8,-50z',fill:'#8c2a1e',stroke:INK,'stroke-width':sw},g);
 const sway=o.walk?Math.sin(o.walk)*5:0;
 for(const s of [-1,1]){const d=`M${s*3},-30 L${s*6+(s>0?sway:-sway)},-3`;el('path',{d,stroke:INK,'stroke-width':8.4,'stroke-linecap':'round'},g);el('path',{d,stroke:tr,'stroke-width':6,'stroke-linecap':'round'},g)}
 for(const s of [-1,1])el('ellipse',{cx:s*7+(s>0?sway:-sway),cy:-1.5,rx:5.2,ry:2.6,fill:'#2b2218',stroke:INK,'stroke-width':.8},g);
 // thân
 el('path',{d:'M-11,-52 Q-12.5,-40 -10.5,-27 L10.5,-27 Q12.5,-40 11,-52 Q0,-56 -11,-52z',fill:col,stroke:INK,'stroke-width':sw,'stroke-linejoin':'round'},g);
 if(o.armor){const ac=o.acol;
  el('path',{d:'M-10.6,-50 Q0,-54 10.6,-50 L10.8,-33 L-10.8,-33z',fill:ac,stroke:INK,'stroke-width':1},g);
  for(let i=0;i<4;i++)el('path',{d:`M-10.5,${-46+i*4.4} L10.5,${-46+i*4.4}`,stroke:INK,'stroke-width':.7,opacity:.7},g);
  for(let i=-2;i<=2;i++)el('path',{d:`M${i*4},-50 L${i*4},-33`,stroke:INK,'stroke-width':.5,opacity:.45},g);
  el('path',{d:'M-11,-28 L11,-28 L14,-17 L-14,-17z',fill:ac,stroke:INK,'stroke-width':1,'stroke-linejoin':'round'},g);
  for(let i=-2;i<=2;i++)el('path',{d:`M${i*5},-28 L${i*5.6},-17`,stroke:INK,'stroke-width':.5,opacity:.5},g);
  if(o.pauld){for(const s of [-1,1]){el('ellipse',{cx:s*11.5,cy:-50,rx:6.4,ry:4.6,fill:ac,stroke:INK,'stroke-width':1},g);el('path',{d:`M${s*11.5-5},-50 L${s*11.5+5},-50`,stroke:'#e6c86a','stroke-width':1.1},g)}}}
 el('path',{d:'M-10.5,-29.5 L10.5,-29.5',stroke:'#3b2a1c','stroke-width':3},g);
 if(o.sack)el('ellipse',{cx:-9,cy:-46,rx:10,ry:7.5,fill:'#cdbd8e',stroke:INK,'stroke-width':1.1},g);
 // tay + vũ khí
 const arm=(x0,y0,x1,y1,w)=>{const d=`M${x0},${y0} L${x1},${y1}`;el('path',{d,stroke:INK,'stroke-width':(w||5.6)+1.8,'stroke-linecap':'round'},g);el('path',{d,stroke:col,'stroke-width':w||5.6,'stroke-linecap':'round'},g);el('circle',{cx:x1,cy:y1,r:2.8,fill:sk,stroke:INK,'stroke-width':.7},g)};
 const w=o.arm;
 if(w=='spear'){const sx=15;el('path',{d:`M${sx},-94 L${sx},5`,stroke:'#6e5032','stroke-width':2.8,'stroke-linecap':'round'},g);
  el('path',{d:`M${sx},-104 L${sx-3},-93 L${sx+3},-93z`,fill:'#d6dade',stroke:INK,'stroke-width':1,'stroke-linejoin':'round'},g);
  if(o.tassel)el('path',{d:`M${sx},-92 q4,5 1,10 q-3,-4 -1,-10z`,fill:o.tassel},g);
  arm(8,-49,sx,-40)}
 else if(w=='bow'){const d=o.d||0,bx=25,Nx=bx-17*d;
  el('path',{d:`M-6,-50 L${Nx},-47`,stroke:INK,'stroke-width':7,'stroke-linecap':'round'},g);el('path',{d:`M-6,-50 L${Nx},-47`,stroke:col,'stroke-width':5.2,'stroke-linecap':'round'},g);
  el('path',{d:`M${bx},-76 Q${bx+13},-47 ${bx},-18`,fill:'none',stroke:'#5a3b1c','stroke-width':3.2,'stroke-linecap':'round'},g);
  el('path',{d:`M${bx},-76 L${Nx},-47 L${bx},-18`,fill:'none',stroke:'#ece3c8','stroke-width':.9},g);
  if(o.nock){el('path',{d:`M${Nx},-47 L${bx+22},-47`,stroke:'#3b2a1c','stroke-width':1.7},g);el('path',{d:`M${bx+22},-47 l-5,-2.6 l0,5.2z`,fill:'#cfd4da',stroke:INK,'stroke-width':.6},g);
   if(o.fire)el('circle',{cx:bx+23,cy:-47,r:3.6,fill:'#ff9c1a',stroke:'#d63a1c','stroke-width':1},g)}
  el('circle',{cx:Nx,cy:-47,r:2.6,fill:sk,stroke:INK,'stroke-width':.7},g);
  arm(8,-50,bx,-47)}
 else if(w=='point'){arm(8,-50,33,-68);
  el('path',{d:'M-8,-33 L-20,-14',stroke:'#2b2218','stroke-width':3.2,'stroke-linecap':'round'},g);el('path',{d:'M-8,-33 l-3,-2 l4,-3',stroke:'#e6c86a','stroke-width':1.6,fill:'none'},g);
  arm(-8,-48,-9,-34,5)}
 else if(w=='flail'){const f1=Math.sin((o.tt||0)*14+(o.ph||0))*9,f2=Math.cos((o.tt||0)*13+(o.ph||0))*9;arm(8,-50,17,-84+f1);arm(-8,-50,-17,-82+f2)}
 else {arm(8,-50,11,-36);arm(-8,-50,-11,-36)}
 // đầu
 el('circle',{cx:0,cy:-62,r:8.2,fill:sk,stroke:INK,'stroke-width':sw},g);
 el('circle',{cx:3.4,cy:-62.6,r:.95,fill:INK},g);
 const h=o.hat;
 if(h=='khan'||h=='ltk'){
  el('path',{d:'M-8.4,-63 A8.4,8.4 0 0 1 8.4,-63 Q0,-67 -8.4,-63z',fill:'#2b2218'},g);
  el('circle',{cx:-1,cy:-73,r:3.8,fill:'#2b2218',stroke:INK,'stroke-width':.8},g);
  el('path',{d:'M-8.5,-65.5 Q0,-71 8.5,-65.5 L8.5,-62.6 Q0,-67.8 -8.5,-62.6z',fill:o.hatcol||'#7a3b1c',stroke:INK,'stroke-width':.9},g);
  el('path',{d:'M-8,-65 l-7,2.5 l1.5,-6 z',fill:o.hatcol||'#7a3b1c',stroke:INK,'stroke-width':.8},g)}
 else if(h=='non'){el('path',{d:'M-15,-62 L0,-82 L15,-62 Q0,-57 -15,-62z',fill:'#d8c58a',stroke:INK,'stroke-width':1.1,'stroke-linejoin':'round'},g);el('path',{d:'M-7,-62 Q0,-57 7,-62',stroke:'#7a3b1c','stroke-width':1.2,fill:'none'},g)}
 else if(h=='quan'){el('path',{d:'M-9,-63 Q-10,-75 0,-75 Q10,-75 9,-63z',fill:'#2b2218',stroke:INK,'stroke-width':1},g);el('path',{d:'M-10,-64 L10,-64',stroke:INK,'stroke-width':1.6},g)}
 else if(h=='cap'){el('path',{d:'M-8.6,-64 Q-9,-72 0,-72 Q9,-72 8.6,-64z',fill:'#cdbd8e',stroke:INK,'stroke-width':1},g)}
 else if(h=='songhelm'){
  el('path',{d:'M-9.8,-62 Q-10,-74 0,-76 Q10,-74 9.8,-62z',fill:SO.iron,stroke:INK,'stroke-width':1.1,'stroke-linejoin':'round'},g);
  el('path',{d:'M-10.4,-62 L10.4,-62',stroke:INK,'stroke-width':1.6},g);
  el('path',{d:'M-9.8,-62 L-10.6,-55 L-6.2,-57.5z',fill:SO.iron,stroke:INK,'stroke-width':.9},g);
  el('path',{d:'M-5,-72 Q-3,-75 1,-75',stroke:'#c9d0d8','stroke-width':1.1,fill:'none'},g);
  el('path',{d:'M0,-76 L0,-82',stroke:INK,'stroke-width':2.1},g);
  if(o.plume)el('path',{d:'M0,-82 q-6,-1 -5,6 q3,-3 5,-6 q6,3 5,10 q-4,-6 -5,-10z',fill:SO.plume,stroke:INK,'stroke-width':.7},g)}
 if(o.beard){el('path',{d:'M-5.4,-58 Q0,-47 5.4,-58 Q0,-54.5 -5.4,-58z',fill:'#2f2f35',stroke:INK,'stroke-width':.7},g);el('path',{d:'M-1.6,-56.6 Q0,-51 1.8,-56.6',stroke:'#aeb3bb','stroke-width':1.2,fill:'none'},g)}
 if(o.must)el('path',{d:'M-4.5,-58.4 Q0,-56 4.5,-58.4',stroke:'#2f2f35','stroke-width':1.5,fill:'none'},g);
}
function swimmer(P0,x,y,tm,al,song,i){
 if(al<=.01)return;const k=K1,g=el('g',{transform:`translate(${x},${y}) scale(${k})`,opacity:al},P0);
 const b=Math.sin(tm*5+i)*1.4;
 el('ellipse',{cx:0,cy:5,rx:16,ry:5,fill:'none',stroke:'#e8f4fa','stroke-width':1.4,opacity:.7},g);
 el('ellipse',{cx:0,cy:5,rx:26,ry:8,fill:'none',stroke:'#e8f4fa','stroke-width':1,opacity:.4},g);
 for(const s of [-1,1]){const d=`M${s*6},${3+b} L${s*15},${-14+b+Math.sin(tm*9+i+s)*4}`;el('path',{d,stroke:INK,'stroke-width':4.6,'stroke-linecap':'round'},g);el('path',{d,stroke:'#3a64a8','stroke-width':3,'stroke-linecap':'round'},g)}
 el('circle',{cx:0,cy:-5+b,r:7.4,fill:SKIN,stroke:INK,'stroke-width':1.1},g);
 el('path',{d:`M-8.4,${-6+b} Q-8.6,${-16+b} 0,${-18+b} Q8.6,${-16+b} 8.4,${-6+b}z`,fill:SO.iron,stroke:INK,'stroke-width':1},g);
 el('path',{d:`M-12,${3+b} q6,4 12,0 q6,4 12,0`,fill:'none',stroke:'#7fa7c4','stroke-width':3.2,'stroke-linecap':'round'},g)}
// ---------- thuyền (nhìn nghiêng, rộng ~200 px) ----------
function boat(P0,x,y,o){
 const bn=o.burn||0,g=el('g',{transform:`translate(${x},${y}) rotate(${o.rot||0}) scale(${K1})`,opacity:o.al==null?1:o.al},P0);
 const hull='M-100,-16 Q-96,16 -58,19 L62,19 Q94,15 102,-22 L90,-10 L-88,-10z';
 el('path',{d:'M-112,17 q14,7 28,0 q14,7 28,0 q14,7 28,0 q14,7 28,0 q14,7 28,0 q14,7 28,0 q14,7 28,0 q14,7 28,0',fill:'none',stroke:'#e8f4fa','stroke-width':1.8,opacity:.65},g);
 el('path',{d:hull,fill:'#7a5634',stroke:INK,'stroke-width':2.2,'stroke-linejoin':'round'},g);
 el('path',{d:'M-93,0 L97,0 M-88,9 L84,9',stroke:'#4a3018','stroke-width':1.4,opacity:.7},g);
 for(let i=-4;i<=4;i++)el('path',{d:`M${i*20},-10 L${i*20},19`,stroke:'#4a3018','stroke-width':.8,opacity:.45},g);
 el('path',{d:'M-88,-10 L90,-10',stroke:'#a07848','stroke-width':3},g);
 for(let i=-4;i<=4;i++)el('path',{d:`M${i*20},-10 L${i*20},-21`,stroke:'#5a3b1c','stroke-width':2.4,'stroke-linecap':'round'},g);
 el('path',{d:'M-90,-21 L92,-21',stroke:'#5a3b1c','stroke-width':1.8},g);
 // buồm: cháy thì co lại
 const sl=1-.86*bn;
 el('path',{d:'M0,-10 L0,-96',stroke:'#4a3018','stroke-width':4,'stroke-linecap':'round'},g);
 el('g',{transform:`translate(0,-22) scale(1,${sl})`},g).innerHTML=`<path d="M2,-70 L58,0 L2,0z" fill="${bn>0.05?'#7d6a4a':'#d8c594'}" stroke="${INK}" stroke-width="1.6" stroke-linejoin="round"/><path d="M2,-46 L40,0 M2,-22 L22,0" stroke="${INK}" stroke-width=".8" opacity=".55"/>`;
 if(bn>0)el('path',{d:hull,fill:'#1e1610',opacity:.55*bn},g);
}
function flameC(g,x,y,s,t,a){
 for(let k=0;k<9;k++){const dx=(k-4)*s*.28,hh=s*(1.2+.8*Math.sin(t*9+k*1.7));el('path',{d:`M${x+dx-s*.2},${y} q${s*.1},${-hh*.6} ${s*.2},${-hh} q${s*.1},${hh*.4} ${s*.2},${hh}z`,fill:k%2?'#ee9a1c':'#d63a1c',opacity:.92*a},g)}
 for(let k=0;k<5;k++){const dx=(k-2)*s*.34,hh=s*(.7+.4*Math.sin(t*11+k*2.3));el('path',{d:`M${x+dx-s*.12},${y} q${s*.06},${-hh*.6} ${s*.12},${-hh} q${s*.06},${hh*.4} ${s*.12},${hh}z`,fill:'#ffe27a',opacity:.9*a},g)}
 el('ellipse',{cx:x,cy:y-s*.5,rx:s*1.9,ry:s*1.3,fill:'url(#flg)',opacity:.55*a},g);
 for(let k=0;k<6;k++){const ph=((t*.45+k/6)%1);el('ellipse',{cx:x+Math.sin(t*1.3+k*2)*s*.5+ph*s*.9,cy:y-s*1.4-ph*s*5.5,rx:s*(.5+ph*1.2),ry:s*(.4+ph*.9),fill:'#4a4440',opacity:.5*a*(1-ph)},g)}
}
// ---------- tên bay ----------
function arrow(g,S,T,p,arc,fire,t){
 const pos=q=>[lerp(S[0],T[0],q),lerp(S[1],T[1],q)-Math.sin(q*Math.PI)*arc*K1];
 const [x,y]=pos(p),[x0,y0]=pos(Math.max(0,p-.04)),an=Math.atan2(y-y0,x-x0)*180/Math.PI;
 const e=el('g',{transform:`translate(${x},${y}) rotate(${an}) scale(${K1})`},g);
 el('path',{d:'M-26,0 L0,0',stroke:'#3b2a1c','stroke-width':1.8,'stroke-linecap':'round'},e);
 el('path',{d:'M0,0 l-6,-3 l0,6z',fill:'#cfd4da',stroke:INK,'stroke-width':.6},e);
 el('path',{d:'M-26,0 l-5,-3 M-26,0 l-5,3 M-22,0 l-5,-3 M-22,0 l-5,3',stroke:'#e6e0cc','stroke-width':1.1},e);
 if(fire){el('ellipse',{cx:-4,cy:0,rx:16,ry:5,fill:'#ff9c1a',opacity:.45},e);el('circle',{cx:2,cy:0,r:5,fill:'#ffd84a',stroke:'#d63a1c','stroke-width':1.4},e);for(let i=1;i<=3;i++)el('circle',{cx:-i*11,cy:Math.sin(t*20+i)*2,r:3.4-i*.6,fill:'#e8821c',opacity:.6},e)}
}
function shot(j,tau,ts0,gap,dt){const ph=tau-ts0-j*dt;if(ph<-.9)return{d:0,nock:false};const n=Math.floor((ph+.9)/gap),loc=ph-n*gap;if(loc<0)return{d:ease((loc+.9)/.9),nock:true};return{d:0,nock:false}}
// ---------- bố cục cảnh ----------
const BURN=[6.0,7.7,9.3,10.8],RU=[-340,-115,115,340],RVE=[-30,-18,-27,-20];
const VA=[-270,-165,-60,45,150,255];       // cung thủ Đại Việt
const VS=[-215,-110,-5,100,205];           // lính cầm giáo
const SS=[-300,-185,-70,60,180];           // lính Tống cầm giáo (bờ bắc)
const SAU=[-240,-30,140];                  // cung thủ Tống
const LTK={u:-355,v:205},QQ={u:270,v:-215};
function rafPos(r,tau){const p=ease(cl((tau-.2-r*.25)/3.6));const b=cl((tau-BURN[r])/3);
 return [RU[r]+Math.sin(tau*.9+r)*3+b*14*(r%2?-1:1), lerp(-125,RVE[r],p)+Math.sin(tau*1.6+r*2)*2+b*6]}
const rn=(()=>{const f=rnd(77);const a=[];for(let i=0;i<60;i++)a.push(f());return a})();
function ground(D,tau){
 const poly=(pts,fill,ex)=>el('polygon',Object.assign({points:pts.map(p=>Lc(p[0],p[1]).join(',')).join(' '),fill},ex||{}),D);
 const X=14000;
 poly([[-X,-1200],[X,-1200],[X,-150],[-X,-150]],'#dfe6bd',{opacity:.6});
 poly([[-X,70],[X,70],[X,1200],[-X,1200]],'#dfe6bd',{opacity:.6});
 poly([[-X,-150],[X,-150],[X,-134],[-X,-134]],'#efe2b8',{opacity:.9});
 poly([[-X,54],[X,54],[X,70],[-X,70]],'#efe2b8',{opacity:.9});
 poly([[-X,-142],[X,-142],[X,62],[-X,62]],'#7fa7c4');
 poly([[-X,-142],[X,-142],[X,-90],[-X,-90]],'#8db3cb',{opacity:.55});
 for(const v of [-143,63]){let d='';for(let u=-1300;u<=1300;u+=40){const q=Lc(u,v+Math.sin(u/55+v)*2.2);d+=(u==-1300?'M':'L')+q.join(',')}el('path',{d,fill:'none',stroke:'#a8956a','stroke-width':W(2.6),'stroke-linejoin':'round'},D)}
 for(let i=0;i<46;i++){const u=((i*97+tau*16)%2400)-1200,v=-130+((i*53)%180),a=Lc(u,v),b=Lc(u+26+rn[i%60]*14,v);el('path',{d:`M${a[0]},${a[1]} L${b[0]},${b[1]}`,stroke:'#e8f4fa','stroke-width':W(1.8),'stroke-linecap':'round',opacity:.5},D)}
 // lau sậy hai bờ
 for(let i=0;i<34;i++){const u=-1150+i*70+rn[i%60]*30,v=(i%2?-149:67),a=Lc(u,v);for(let q=-1;q<=1;q++)el('path',{d:`M${a[0]+q*W(3)},${a[1]} q${W(q*3)},${-W(10)} ${W(q*5)},${-W(18)}`,stroke:'#6f8a4a','stroke-width':W(1.8),fill:'none','stroke-linecap':'round'},D)}
 // lối đất bờ nam
 el('path',{d:`M${Lc(-1300,150).join(',')} L${Lc(1300,166).join(',')}`,stroke:'#cdb985','stroke-width':W(26),fill:'none',opacity:.45,'stroke-linecap':'round'},D);
}
function tree(g,x,y,s){const e=el('g',{transform:`translate(${x},${y}) scale(${K1*s})`},g);
 el('ellipse',{cx:0,cy:2,rx:18,ry:5,fill:'#000',opacity:.12},e);el('path',{d:'M0,0 L0,-22',stroke:'#5a3b1c','stroke-width':4,'stroke-linecap':'round'},e);
 el('circle',{cx:0,cy:-34,r:20,fill:'#7b9a58',stroke:'#4d6a37','stroke-width':1.5},e);el('circle',{cx:-8,cy:-40,r:11,fill:'#8cac66'},e);el('circle',{cx:9,cy:-28,r:9,fill:'#6d8c4b'},e)}
function stake(g,x,y,h,wd,col){const e=el('g',{transform:`translate(${x},${y}) scale(${K1})`},g);
 el('path',{d:`M${-wd},0 L${-wd},${-h} L0,${-h-wd*1.5} L${wd},${-h} L${wd},0z`,fill:col,stroke:INK,'stroke-width':1.2,'stroke-linejoin':'round'},e)}

const CCnn=function(t,it,a){
 setup(it);const tau=(t-(it.ts==null?it.t0:it.ts))*(it.sp||1)+(it.tau0||0);
 const zf=ease(cl((SC/SCf-.3)/.6)),al=a*zf;if(al<=.01)return;
 const GD=el('g',{opacity:a},dyn);ground(GD,tau);
 const D=el('g',{opacity:al},dyn);
 const L=[];const push=(y,f)=>L.push({y,f});
 // cây xa
 for(let i=0;i<22;i++){const u=-1100+i*105+rn[i]*40,v=(i%2?1:-1)*(330+rn[i+20]*110),p=Lc(u,v);push(p[1],()=>tree(D,p[0],p[1],.9+rn[i+10]*.5))}
 // cọc chặn sông + hàng rào đất bờ nam
 for(let u=-520;u<=520;u+=34){const p=Lc(u+((u/34)%2)*6,22+Math.sin(u)*3);push(p[1],()=>stake(D,p[0],p[1],27+((u/34)&3)*3,3.4,'#5a3b1c'))}
 for(let u=-560;u<=560;u+=15){const p=Lc(u,102+Math.sin(u/9)*1.5);push(p[1],()=>stake(D,p[0],p[1],36+((u/15)&3)*2,4.2,'#8a5a2b'))}
 {const a1=Lc(-570,84),a2=Lc(570,84);push(a1[1]+W(1),()=>{el('path',{d:`M${a1[0]},${a1[1]} L${a2[0]},${a2[1]}`,stroke:'#6b4a28','stroke-width':W(2.4),opacity:.8},D)})}
 // thuyền + lính trên thuyền
 for(let r=0;r<4;r++){const [bu,bv]=rafPos(r,tau),bp=Lc(bu,bv),burnT=BURN[r],bn=ease(cl((tau-burnT)/1.2)),sink=ease(cl((tau-burnT-3)/3.2)),rot=sink*7*(r%2?-1:1);
  push(bp[1],()=>{boat(D,bp[0],bp[1]+W(sink*26),{burn:bn,rot,al:1-.45*sink});
   if(bn>0.02){for(const [fx,fs,fy] of [[-52,13,-12],[8,17,-12],[58,12,-12]])flameC(D,bp[0]+W(fx),bp[1]+W(fy+sink*26),W(fs)*bn,t*(1+fx*.01),1)}});
  for(let i=0;i<3;i++){const off=[-48,4,52][i],tJ=burnT+.9+.4*i,pj=(tau-tJ)/.55;
   const dx=(i%2?1:-1)*(12+60*cl(pj)),base=Lc(bu+off,bv-8+sink*26);
   if(pj<0){push(bp[1]+W(2+i),()=>fig(D,base[0],base[1],{sz:62,col:SO.tun,trou:SO.trou,hat:'songhelm',plume:i==1,armor:true,acol:SO.arm,arm:tau>burnT+.25?'flail':'spear',tt:tau,ph:i+r,flip:true}))}
   else if(pj<1){const jx=base[0]+W(dx*Math.min(1,pj*1.2)*(i%2?1:-1)*(i%2?1:-1)),jy=base[1]+W(40*pj)-W(54*Math.sin(pj*Math.PI));
    push(bp[1]+W(3),()=>fig(D,jx,jy,{sz:62,col:SO.tun,trou:SO.trou,hat:'songhelm',armor:true,acol:SO.arm,arm:'flail',tt:tau,ph:i+r,rot:pj*80*(i%2?1:-1)}))}
   else{const wp=Lc(bu+off+(i%2?1:-1)*(46+i*8),bv+30+i*5);const fa=1-cl((tau-tJ-.55-1.3)/1.5);
    push(wp[1],()=>{const rr=cl((tau-tJ-.55)/.9);if(rr<1)el('ellipse',{cx:wp[0],cy:wp[1],rx:W(10+34*rr),ry:W(4+11*rr),fill:'none',stroke:'#fff',opacity:(1-rr)*.85,'stroke-width':W(2.4)},D);swimmer(D,wp[0],wp[1],tau,fa,true,i+r)})}}}
 // Việt: hàng cung thủ và lính cầm giáo
 VA.forEach((u,j)=>{const p=Lc(u,140+(j%2)*6),sh=shot(j,tau,4.2,1.35,.33);
  push(p[1],()=>fig(D,p[0],p[1]+Math.sin(tau*2+j)*W(.6),{sz:72,col:VI.tun,trou:VI.trou,hat:'khan',hatcol:j%3==1?'#8a3a24':'#6b4a2a',arm:'bow',d:sh.d,nock:sh.nock,fire:tau>5.0&&j%2==0,armor:j%3==0,acol:VI.arm}))});
 VS.forEach((u,j)=>{const p=Lc(u,176+(j%2)*8);push(p[1],()=>fig(D,p[0],p[1]+Math.sin(tau*1.7+j*2)*W(.5),{sz:72,col:j%2?VI.tun:'#7a4f26',trou:VI.trou,hat:'khan',hatcol:j%2?'#6b4a2a':'#8a3a24',arm:'spear',armor:j%2==0,acol:VI.arm}))});
 // Lý Thường Kiệt trên gò đất
 {const p=Lc(LTK.u,LTK.v);push(p[1],()=>{el('ellipse',{cx:p[0],cy:p[1],rx:W(76),ry:W(20),fill:'#a98d5a',stroke:INK,'stroke-width':W(1.6)},D);
   el('ellipse',{cx:p[0],cy:p[1]-W(5),rx:W(62),ry:W(14),fill:'#bfa36a'},D);
   fig(D,p[0],p[1]-W(8),{sz:86,col:'#7a3b1c',trou:'#4a2a1a',hat:'ltk',hatcol:'#b3261e',arm:'point',armor:true,pauld:true,acol:'#b08a3a',cape:true,beard:true})})}
 // Tống: bờ bắc
 SS.forEach((u,j)=>{const p=Lc(u,-218-(j%2)*10);push(p[1],()=>fig(D,p[0],p[1]+Math.sin(tau*1.9+j)*W(.5),{sz:72,col:SO.tun,trou:SO.trou,hat:'songhelm',armor:true,acol:SO.arm,arm:'spear',tassel:'#8c2a1e',flip:true}))});
 SAU.forEach((u,j)=>{const p=Lc(u,-172),sh=shot(j,tau,5.2,2.4,.6);push(p[1],()=>fig(D,p[0],p[1],{sz:72,col:SO.tun,trou:SO.trou,hat:'songhelm',armor:true,acol:SO.arm,arm:'bow',d:sh.d,nock:sh.nock,flip:false}))});
 {const p=Lc(QQ.u,QQ.v);push(p[1],()=>fig(D,p[0],p[1],{sz:84,col:'#2f568f',trou:SO.trou,hat:'songhelm',plume:true,armor:true,pauld:true,acol:'#6c7682',arm:'point',must:true,flip:true}))}
 L.sort((a,b)=>a.y-b.y);for(const e of L)e.f();
 // tên bay (vẽ sau cùng để nằm trên đầu người)
 const AR=el('g',{},D);
 VA.forEach((u,j)=>{const S0=Lc(u+18,140-52);for(let n=Math.max(0,Math.floor((tau-4.2-j*.33-.85)/1.35));n<=Math.floor((tau-4.2-j*.33)/1.35)+1;n++){const ts=4.2+j*.33+n*1.35,p=(tau-ts)/.85;if(p<=0||p>=1)continue;
   const r=(j+n)%4,tp=rafPos(r,ts+.85),T=Lc(tp[0]+(((j*7+n*3)%5)-2)*14,tp[1]-26);arrow(AR,S0,T,p,130,false,t)}});
 for(let r=0;r<4;r++){const p=(tau-(BURN[r]-.8))/.8;if(p>0&&p<1){const j=(r*2+1)%6,S0=Lc(VA[j]+18,140-52),tp=rafPos(r,BURN[r]),T=Lc(tp[0],tp[1]-30);arrow(AR,S0,T,p,150,true,t)}}
 SAU.forEach((u,j)=>{const S0=Lc(u+18,-172-52);for(let n=Math.max(0,Math.floor((tau-5.2-j*.6-.85)/2.4));n<=Math.floor((tau-5.2-j*.6)/2.4)+1;n++){const ts=5.2+j*.6+n*2.4,p=(tau-ts)/.85;if(p<=0||p>=1)continue;
   const T=Lc(-300+((j*5+n*2)%6)*120,100);arrow(AR,S0,T,p,110,false,t)}});
};
// ---------- lớp HUD: huy hiệu chân dung, tên, "!!!" ----------
function portrait(g,cx,cy,r,kind,id){
 const cp=el('clipPath',{id},g);el('circle',{cx,cy,r},cp);
 const e=el('g',{'clip-path':`url(#${id})`},g);
 el('rect',{x:cx-r,y:cy-r,width:2*r,height:2*r,fill:kind=='v'?'#e9d9ae':'#d4dde8'},e);
 const s=r/50,t=`translate(${cx},${cy+6*s}) scale(${s})`;const q=el('g',{transform:t},e);
 if(kind=='v'){
  el('path',{d:'M-32,-6 Q-44,24 -40,44 L-14,44 L-8,-4z',fill:'#8c2a1e',stroke:INK,'stroke-width':1.6},q);
  el('path',{d:'M-34,46 Q-36,16 -20,10 L20,10 Q36,16 34,46z',fill:'#b08a3a',stroke:INK,'stroke-width':2},q);
  for(let i=0;i<4;i++)el('path',{d:`M-30,${18+i*7} L30,${18+i*7}`,stroke:INK,'stroke-width':1,opacity:.5},q);
  for(const sx of [-1,1]){el('ellipse',{cx:sx*30,cy:14,rx:12,ry:8,fill:'#c8a24a',stroke:INK,'stroke-width':1.8},q)}
  el('rect',{x:-6,y:-2,width:12,height:14,fill:SKIN,stroke:INK,'stroke-width':1.6},q);
  el('ellipse',{cx:0,cy:-16,rx:17,ry:19,fill:SKIN,stroke:INK,'stroke-width':2},q);
  el('path',{d:'M-17,-18 A17,17 0 0 1 17,-18 Q0,-26 -17,-18z',fill:'#2b2218'},q);
  el('circle',{cx:0,cy:-40,r:7,fill:'#2b2218',stroke:INK,'stroke-width':1.4},q);
  el('path',{d:'M-18,-24 Q0,-34 18,-24 L18,-19 Q0,-28 -18,-19z',fill:'#b3261e',stroke:INK,'stroke-width':1.6},q);
  el('path',{d:'M-9,-14 q3,-2 6,0 M3,-14 q3,-2 6,0',stroke:INK,'stroke-width':1.8,fill:'none','stroke-linecap':'round'},q);
  el('path',{d:'M-14,-6 Q0,26 14,-6 Q8,6 0,6 Q-8,6 -14,-6z',fill:'#2f2f35',stroke:INK,'stroke-width':1.2},q);
  el('path',{d:'M-3,2 Q0,18 3,2',stroke:'#aeb3bb','stroke-width':2.2,fill:'none'},q);
 } else {
  el('path',{d:'M-36,46 Q-38,16 -20,10 L20,10 Q38,16 36,46z',fill:'#56606c',stroke:INK,'stroke-width':2},q);
  for(let i=0;i<4;i++)el('path',{d:`M-32,${17+i*7} L32,${17+i*7}`,stroke:INK,'stroke-width':1,opacity:.5},q);
  for(const sx of [-1,1])el('ellipse',{cx:sx*32,cy:14,rx:12,ry:8,fill:'#6c7682',stroke:INK,'stroke-width':1.8},q);
  el('path',{d:'M-14,22 L14,22 L10,46 L-10,46z',fill:'#2f568f',stroke:INK,'stroke-width':1.2},q);
  el('rect',{x:-6,y:-2,width:12,height:14,fill:SKIN,stroke:INK,'stroke-width':1.6},q);
  el('ellipse',{cx:0,cy:-16,rx:17,ry:19,fill:SKIN,stroke:INK,'stroke-width':2},q);
  el('path',{d:'M-20,-18 Q-22,-42 0,-46 Q22,-42 20,-18 L16,-12 L-16,-12z',fill:'#8a929c',stroke:INK,'stroke-width':2,'stroke-linejoin':'round'},q);
  el('path',{d:'M-21,-19 L21,-19',stroke:INK,'stroke-width':2.4},q);
  el('path',{d:'M-19,-18 L-23,-4 L-15,-8z M19,-18 L23,-4 L15,-8z',fill:'#8a929c',stroke:INK,'stroke-width':1.4},q);
  el('path',{d:'M0,-46 L0,-56',stroke:INK,'stroke-width':3.2},q);
  el('path',{d:'M0,-56 q-12,-2 -10,12 q6,-6 10,-12 q12,6 10,20 q-8,-10 -10,-20z',fill:'#2e4a80',stroke:INK,'stroke-width':1.2},q);
  el('path',{d:'M-9,-13 q3,-2 6,0 M3,-13 q3,-2 6,0',stroke:INK,'stroke-width':1.8,fill:'none','stroke-linecap':'round'},q);
  el('path',{d:'M-9,-3 Q0,2 9,-3 Q0,0 -9,-3z',fill:'#3a3a40',stroke:INK,'stroke-width':1},q);
  el('path',{d:'M-7,2 Q0,10 7,2 Q0,6 -7,2z',fill:'#7a7e86',stroke:INK,'stroke-width':.8},q)}
 el('circle',{cx,cy,r,fill:'none',stroke:kind=='v'?'#c9742a':'#3a64a8','stroke-width':6},g);
 el('circle',{cx,cy,r:r+3,fill:'none',stroke:'#241a0e','stroke-width':2.4},g);
}
function badge(t,tau,it,u,v,fh,kind,name,sub,t0,id,below){
 const e=ease(cl((tau-t0)/.6));if(e<=0)return;const p=Lc(u,v),[sx,sy]=toS(p[0],p[1]);
 const H=fh*SC/SCf,r=50,dir=sx>420?-1:1;
 const cx=below?sx+dir*190:sx,cy=below?sy-H*.75:sy-H-r-46;
 const g=el('g',{opacity:e,transform:`translate(${cx},${cy}) scale(${.6+.4*e}) translate(${-cx},${-cy})`},hud);
 const col=kind=='v'?'#c9742a':'#3a64a8';
 if(below){el('path',{d:`M${cx-dir*(r+3)},${cy} L${sx},${sy-H*.5}`,stroke:'#241a0e','stroke-width':3,opacity:.85},g);el('circle',{cx:sx,cy:sy-H*.5,r:5,fill:col,stroke:'#241a0e','stroke-width':2},g)}
 else{el('path',{d:`M${sx},${cy+r+3} L${sx},${sy-H-4}`,stroke:'#241a0e','stroke-width':3,opacity:.85},g);el('circle',{cx:sx,cy:sy-H-4,r:5,fill:col,stroke:'#241a0e','stroke-width':2},g)}
 portrait(g,cx,cy,r,kind,id);
 const w=Math.max(220,name.length*17+40),py=below?cy+r+8:cy-r-62;
 el('rect',{x:cx-w/2,y:py,width:w,height:56,rx:10,fill:'#241a0e',opacity:.9},g);
 el('rect',{x:cx-w/2,y:py,width:7,height:56,fill:col},g);
 el('text',{x:cx+3,y:py+27,'text-anchor':'middle','font-size':28,'font-weight':700,fill:'#f4ecc8'},g).textContent=name;
 el('text',{x:cx+3,y:py+49,'text-anchor':'middle','font-size':19,fill:'#d9ccaa'},g).textContent=sub;
}
function burst(cx,cy,u,txt){
 const s=ease(cl(u/.25))*(1-.15*cl((u-.8)/.2)),o=1-cl((u-.75)/.25),pts=[];const n=16;
 for(let i=0;i<n*2;i++){const an=i/(n*2)*6.2832+Math.sin(u*9)*.05,r=(i%2?46:84)*s*(1+.06*Math.sin(u*30+i));pts.push((cx+Math.cos(an)*r)+','+(cy+Math.sin(an)*r))}
 const g=el('g',{opacity:o},hud);
 el('polygon',{points:pts.join(' '),fill:'#ffd84a',stroke:'#b3261e','stroke-width':6,'stroke-linejoin':'round'},g);
 el('text',{x:cx,y:cy+20*s,'text-anchor':'middle','font-size':58*s,'font-weight':700,fill:'#7a1f1f','paint-order':'stroke',stroke:'#fff3c4','stroke-width':4},g).textContent='!!!';
}
const CCHnn=function(t,it,a){
 setup(it);const tau=(t-(it.ts==null?it.t0:it.ts))*(it.sp||1)+(it.tau0||0);if(tau<0)return;const zf=ease(cl((SC/SCf-.8)/.2));if(zf<=0.01||a<=0.01)return;
 const g=el('g',{opacity:a*zf},hud);
 const save=hud;
 badge(t,tau,it,LTK.u,LTK.v-8,86,'v','Lý Thường Kiệt','Đại Việt',2.4,'cpL',true);
 badge(t,tau,it,QQ.u,QQ.v,84,'s','Quách Quỳ','nhà Tống',3.4,'cpQ');
 for(const r of [0,2]){const u=(tau-BURN[r]-.05)/1.5;if(u>0&&u<1){const rp=rafPos(r,tau),p=Lc(rp[0],rp[1]),[sx,sy]=toS(p[0],p[1]);burst(sx,sy-190*SC/SCf,u)}}
};

// =================== CẢNH ỨNG CHÂU: đắp đường đất bằng bao đất, đánh thành ===================
const UW=-80,WH=118,UR=[-420,420];
function ucBreach(){return 14.2}
function wallTop(u){return Lc(u,UW)}
function drawWall(D,tau,L){
 const b1=Lc(UR[0],UW),b2=Lc(UR[1],UW),t=W(WH);
 L.push({y:b1[1]-W(2),f:()=>{
  el('polygon',{points:`${b1[0]},${b1[1]} ${b2[0]},${b2[1]} ${b2[0]},${b2[1]-t} ${b1[0]},${b1[1]-t}`,fill:'#bfb59d',stroke:INK,'stroke-width':W(2.2),'stroke-linejoin':'round'},D);
  for(let r=1;r<6;r++){const y0=b1[1]+(b2[1]-b1[1])*0,p0=Lc(UR[0],UW),p1=Lc(UR[1],UW);el('path',{d:`M${p0[0]},${p0[1]-t*r/6} L${p1[0]},${p1[1]-t*r/6}`,stroke:'#8d8470','stroke-width':W(1),opacity:.8},D)}
  for(let u=UR[0]+30,i=0;u<UR[1];u+=46,i++){for(let r=0;r<6;r++){const p=Lc(u+(r%2)*23,UW);el('path',{d:`M${p[0]},${p[1]-t*r/6} L${p[0]},${p[1]-t*(r+1)/6}`,stroke:'#8d8470','stroke-width':W(.9),opacity:.7},D)}}
  const g=Lc(0,UW);el('path',{d:`M${g[0]-W(38)},${g[1]} L${g[0]-W(38)},${g[1]-W(58)} A${W(38)},${W(34)} 0 0 1 ${g[0]+W(38)},${g[1]-W(58)} L${g[0]+W(38)},${g[1]}z`,fill:'#3a2a1c',stroke:INK,'stroke-width':W(2)},D);
  const open=cl((tau-ucBreach())/.8);
  for(let i=-3;i<=3;i++)el('path',{d:`M${g[0]+W(i*10)},${g[1]} L${g[0]+W(i*10)},${g[1]-W(60)+W(Math.abs(i)*2)}`,stroke:'#6b4a28','stroke-width':W(5.2),opacity:1-open*.85},D);
  for(const e of UR){const p=Lc(e,UW),w=W(34);el('rect',{x:p[0]-w,y:p[1]-W(158),width:2*w,height:W(158),fill:'#b3a98f',stroke:INK,'stroke-width':W(2.2)},D);
   el('path',{d:`M${p[0]-w-W(12)},${p[1]-W(158)} L${p[0]},${p[1]-W(190)} L${p[0]+w+W(12)},${p[1]-W(158)}z`,fill:'#6e6a64',stroke:INK,'stroke-width':W(2.2),'stroke-linejoin':'round'},D)}
 }});
 // lỗ châu mai vẽ sau lính để che chân
 for(let u=UR[0]+60;u<UR[1]-40;u+=46){const p=Lc(u,UW);L.push({y:p[1]-W(2)+W(.5),f:()=>el('rect',{x:p[0]-W(12),y:p[1]-t-W(14),width:W(24),height:W(14),fill:'#bfb59d',stroke:INK,'stroke-width':W(1.6)},D)})}
}
function house(D,x,y,s,burn,t){const e=el('g',{transform:`translate(${x},${y}) scale(${K1*s})`},D);
 el('rect',{x:-30,y:-34,width:60,height:34,fill:'#d9ccaa',stroke:INK,'stroke-width':1.8},e);
 el('path',{d:'M-38,-34 L0,-62 L38,-34z',fill:'#6e6a64',stroke:INK,'stroke-width':1.8,'stroke-linejoin':'round'},e);
 el('rect',{x:-7,y:-20,width:14,height:20,fill:'#5a3b1c'},e);
 if(burn>0)e.setAttribute('data-b','1')}
function ground2(D,tau){
 const poly=(pts,fill,ex)=>el('polygon',Object.assign({points:pts.map(p=>Lc(p[0],p[1]).join(',')).join(' '),fill},ex||{}),D);
 const X=14000;poly([[-X,-1300],[X,-1300],[X,1300],[-X,1300]],'#dfe6bd',{opacity:.55});
 poly([[-X,-40],[X,-40],[X,10],[-X,10]],'#8fb3c8',{opacity:.75});   // hào quanh thành
 el('path',{d:`M${Lc(-900,215).join(',')} Q${Lc(-100,170).join(',')} ${Lc(60,60).join(',')}`,stroke:'#cdb985','stroke-width':W(30),fill:'none',opacity:.5,'stroke-linecap':'round'},D);
}
const CCuc=function(t,it,a){
 setup(it);const tau=(t-(it.ts==null?it.t0:it.ts))*(it.sp||1)+(it.tau0||0);
 const zf=ease(cl((SC/SCf-.3)/.6)),al=a*zf;
 const GD=el('g',{opacity:a},dyn);ground2(GD,tau);
 if(al<=.01)return;const D=el('g',{opacity:al},dyn);
 const L=[];const push=(y,f)=>L.push({y,f});const BR=ucBreach();
 const hRamp=WH*ease(cl((tau-1)/10.5));
 // nhà trong thành
 [[-330,-200],[-190,-250],[-60,-190],[90,-240],[220,-200],[340,-260],[-260,-320],[40,-330],[280,-340]].forEach(([u,v],i)=>{const p=Lc(u,v),b=ease(cl((tau-BR-.6-i*.35)/1.2));push(p[1],()=>{house(D,p[0],p[1],1.0+(i%3)*.12,b,t);if(b>0.02)flameC(D,p[0],p[1]-W(40),W(14)*b,t+i,1)})});
 drawWall(D,tau,L);
 // đường đất bao đất
 {const bl=Lc(-45,155),br=Lc(175,155),h=W(hRamp),tr=Lc(100,UW+6),tl=Lc(20,UW+6);
  push(bl[1],()=>{el('polygon',{points:`${bl[0]},${bl[1]} ${br[0]},${br[1]} ${tr[0]},${tr[1]-h} ${tl[0]},${tl[1]-h}`,fill:'#a98d5a',stroke:INK,'stroke-width':W(2.2),'stroke-linejoin':'round'},D);
   for(let r=0;r<9;r++){const f=r/9;for(let c=0;c<6;c++){const x=lerp(lerp(bl[0],tl[0],f),lerp(br[0],tr[0],f),(c+.5+(r%2)*.5)/6.5),y=lerp(bl[1],tl[1]-h,f)+W(0);if(f*1.0<=1)el('ellipse',{cx:x,cy:y,rx:W(11)*(1-f*.4),ry:W(6)*(1-f*.4),fill:'#cdbd8e',stroke:INK,'stroke-width':W(.8)},D)}}})}
 // kho bao đất
 {const p=Lc(-300,205);push(p[1],()=>{for(let i=0;i<9;i++)el('ellipse',{cx:p[0]+W((i%3)*26-26),cy:p[1]-W(Math.floor(i/3)*11),rx:W(13),ry:W(7),fill:'#cdbd8e',stroke:INK,'stroke-width':W(1)},D)})}
 // người khiêng đất
 for(let k=0;k<8;k++){const pr=((tau*.075+k/8)%1);let u,v,hh=0,sack=true,fl=false;
  if(pr<.25){const f=pr/.25;u=lerp(-290,60+(k%3-1)*22,f);v=lerp(205,150,f)}
  else if(pr<.5){const f=(pr-.25)/.25;u=lerp(60+(k%3-1)*22,60+(k%3-1)*14,f);v=lerp(150,UW+30,f);hh=hRamp*f*.96}
  else if(pr<.56){u=60+(k%3-1)*14;v=UW+30;hh=hRamp*.96;sack=false}
  else {const f=(pr-.56)/.44;u=lerp(60+(k%3-1)*14,-290,f);v=lerp(UW+30,205,f);hh=hRamp*(1-ease(cl(f*3)));sack=false;fl=true}
  const p=Lc(u,v);const dist=Math.hypot(p[0],p[1]);
  push(p[1]+W(3),()=>fig(D,p[0],p[1]-W(hh),{sz:66,col:k%2?VI.tun:'#7a4f26',trou:VI.trou,hat:'khan',hatcol:k%2?'#6b4a2a':'#8a3a24',arm:'none',sack,flip:fl,walk:tau*7+k*1.3}))}
 // cung thủ Đại Việt
 [-260,-170,-80,260,340].forEach((u,j)=>{const p=Lc(u,128+(j%2)*10),sh=shot(j,tau,3.5,1.3,.27);push(p[1],()=>fig(D,p[0],p[1],{sz:70,col:VI.tun,trou:VI.trou,hat:'khan',hatcol:j%2?'#8a3a24':'#6b4a2a',arm:'bow',d:sh.d,nock:sh.nock,fire:tau>8&&j%2==0,armor:j==1,acol:VI.arm,flip:false}))});
 [-200,-30,200,300].forEach((u,j)=>{const p=Lc(u,176),r=BR+1+j*.35;const adv=ease(cl((tau-r)/2.2));const q=Lc(lerp(u,u*.2,adv),lerp(176,UW-10,adv*(tau>BR?1:0)));const pp=tau>BR+.5?q:p;push(pp[1],()=>fig(D,pp[0],pp[1],{sz:70,col:j%2?VI.tun:'#7a4f26',trou:VI.trou,hat:'khan',hatcol:'#6b4a2a',arm:'spear',armor:j%2==0,acol:VI.arm,walk:tau>BR+.5&&adv<1?tau*8:0}))});
 // lính Tống trên thành
 for(let i=0;i<10;i++){const u=-360+i*76,p=wallTop(u),bow=i%3==1,sh=shot(i,tau,3.0,1.6,.3);
  const gone=cl((tau-BR-.3-((i*37)%10)*.18)/1.4);if(gone>=1)continue;
  push(p[1]-W(3),()=>fig(D,p[0],p[1]-W(WH)-W(3)+W(gone*18),{sz:64,col:SO.tun,trou:SO.trou,hat:'songhelm',plume:i==4,armor:true,acol:SO.arm,arm:gone>0?'flail':(bow?'bow':'spear'),tt:tau,ph:i,d:sh.d,nock:sh.nock&&bow,flip:!bow,al:1-gone}))}
 // quân Việt lên thành sau khi thủng
 for(let i=0;i<7;i++){const u=-120+i*42,p=wallTop(u),ap=ease(cl((tau-BR-1.2-i*.25)/.8));if(ap<=0)continue;push(p[1]-W(2),()=>fig(D,p[0],p[1]-W(WH)-W(3),{sz:66,col:i%2?VI.tun:'#7a4f26',trou:VI.trou,hat:'khan',hatcol:'#6b4a2a',arm:'spear',al:ap}))}
 // Lý Thường Kiệt chỉ huy trên gò đất phía sau
 {const p=Lc(-380,215);push(p[1],()=>{el('ellipse',{cx:p[0],cy:p[1],rx:W(76),ry:W(20),fill:'#a98d5a',stroke:INK,'stroke-width':W(1.6)},D);el('ellipse',{cx:p[0],cy:p[1]-W(5),rx:W(62),ry:W(14),fill:'#bfa36a'},D);
   fig(D,p[0],p[1]-W(8),{sz:86,col:'#7a3b1c',trou:'#4a2a1a',hat:'ltk',hatcol:'#b3261e',arm:'point',armor:true,pauld:true,acol:'#b08a3a',cape:true,beard:true})})}
 L.sort((x,y)=>x.y-y.y);for(const e of L)e.f();
 const AR=el('g',{},D);
 [-260,-170,-80,260,340].forEach((u,j)=>{const S0=Lc(u+18,128-52+(j%2)*10);for(let n=Math.max(0,Math.floor((tau-3.5-j*.27-.85)/1.3));n<=Math.floor((tau-3.5-j*.27)/1.3)+1;n++){const ts=3.5+j*.27+n*1.3,p=(tau-ts)/.85;if(p<=0||p>=1||ts>BR+.2)continue;
  const T=Lc(-340+((j*3+n*5)%9)*76,UW-WH-30);arrow(AR,S0,T,p,120,tau>8&&j%2==0,t)}});
 for(let i=1;i<10;i+=3){const p0=wallTop(-360+i*76),S0=[p0[0]+W(18),p0[1]-W(WH)-W(52)];for(let n=Math.max(0,Math.floor((tau-3.0-i*.3-.85)/1.6));n<=Math.floor((tau-3.0-i*.3)/1.6)+1;n++){const ts=3.0+i*.3+n*1.6,p=(tau-ts)/.85;if(p<=0||p>=1||ts>BR-.3)continue;
  const T=Lc(-300+((i*7+n*3)%7)*80,135);arrow(AR,S0,T,p,90,false,t)}}
};
const CCHuc=function(t,it,a){
 setup(it);const tau=(t-(it.ts==null?it.t0:it.ts))*(it.sp||1)+(it.tau0||0);if(tau<0)return;const zf=ease(cl((SC/SCf-.8)/.2));if(zf<=0.01||a<=0.01)return;
 badge(t,tau,it,-380,207,86,'v','Lý Thường Kiệt','Đại Việt',2.0,'cpL',true);
 const u=(tau-BR0()-.1)/1.6;if(u>0&&u<1){const p=Lc(40,UW),[sx,sy]=toS(p[0],p[1]);burst(sx,sy-120*SC/SCf,u)}
};
function BR0(){return ucBreach()}

// ============ BỘ DỰNG CẢNH CHUNG (mỗi cảnh = hàm bố cục) ============
const POS={};
function hill(D,x,y,s,col){const e=el('g',{transform:`translate(${x},${y}) scale(${K1*s})`},D);
 el('path',{d:'M-170,0 L-80,-120 L-30,-70 L40,-170 L170,0z',fill:col||'#9aa57a',stroke:'#5f6b46','stroke-width':2,'stroke-linejoin':'round'},e);
 el('path',{d:'M40,-170 L80,-95 L20,-80 z',fill:'#7e8a62',opacity:.8},e);el('path',{d:'M-80,-120 L-50,-80 L-100,-70 z',fill:'#7e8a62',opacity:.7},e)}
function tent(D,x,y,s,col){const e=el('g',{transform:`translate(${x},${y}) scale(${K1*s})`},D);
 el('ellipse',{cx:0,cy:2,rx:48,ry:7,fill:'#000',opacity:.14},e);
 el('path',{d:'M-46,0 L0,-62 L46,0z',fill:col||'#8d9bb5',stroke:INK,'stroke-width':2,'stroke-linejoin':'round'},e);
 el('path',{d:'M0,-62 L0,0 M-20,-26 L0,0 M20,-26 L0,0',stroke:INK,'stroke-width':1,opacity:.5},e);
 el('path',{d:'M-12,0 L0,-30 L12,0z',fill:'#2b2218'},e)}
function ele(D,x,y,k,ph,flip){const e=el('g',{transform:`translate(${x},${y}) scale(${k*(flip?-1:1)},${k})`},D),gc='#8c8780';
 el('ellipse',{cx:0,cy:0,rx:66,ry:9,fill:'#000',opacity:.15},e);
 for(const [lx,p] of [[-38,0],[-16,2.4],[22,1.2],[44,3.6]]){const sw=Math.sin(ph+p)*7;el('path',{d:`M${lx},-34 L${lx+sw},-2`,stroke:INK,'stroke-width':20,'stroke-linecap':'round'},e);el('path',{d:`M${lx},-34 L${lx+sw},-2`,stroke:gc,'stroke-width':17,'stroke-linecap':'round'},e)}
 el('ellipse',{cx:0,cy:-62,rx:68,ry:40,fill:gc,stroke:INK,'stroke-width':2.2},e);
 el('path',{d:'M46,-84 Q92,-92 98,-52 Q100,-30 86,-12 Q80,-6 76,-14 Q84,-40 74,-52 Q62,-60 46,-48z',fill:gc,stroke:INK,'stroke-width':2.2,'stroke-linejoin':'round'},e);
 el('ellipse',{cx:60,cy:-70,rx:15,ry:23,fill:'#a29d96',stroke:INK,'stroke-width':1.8},e);
 el('path',{d:'M84,-40 Q112,-34 118,-52',stroke:'#f2ead2','stroke-width':6,fill:'none','stroke-linecap':'round'},e);
 el('circle',{cx:88,cy:-70,r:2.2,fill:INK},e);
 el('path',{d:'M-68,-70 Q-84,-60 -76,-38',stroke:gc,'stroke-width':6,fill:'none','stroke-linecap':'round'},e);
 el('path',{d:'M-34,-96 L34,-96 L28,-84 L-28,-84z',fill:'#7a3b1c',stroke:INK,'stroke-width':1.6},e);
 el('path',{d:'M-34,-96 Q0,-130 34,-96',fill:'#b3261e',stroke:INK,'stroke-width':1.6},e)}
function gateT(D,x,y,s){const e=el('g',{transform:`translate(${x},${y}) scale(${K1*s})`},D);
 el('rect',{x:-110,y:-70,width:220,height:70,fill:'#c8b88a',stroke:INK,'stroke-width':2},e);
 el('path',{d:'M-130,-70 L-90,-108 L90,-108 L130,-70z',fill:'#6e6a64',stroke:INK,'stroke-width':2,'stroke-linejoin':'round'},e);
 el('path',{d:'M-100,-70 L-70,-96 M100,-70 L70,-96',stroke:INK,'stroke-width':1.2,opacity:.5},e);
 for(const px of [-100,-50,50,100])el('rect',{x:px-6,y:-70,width:12,height:70,fill:'#8a3a24',stroke:INK,'stroke-width':1.4},e);
 el('path',{d:'M-34,0 L-34,-42 A34,26 0 0 1 34,-42 L34,0z',fill:'#3a2a1c',stroke:INK,'stroke-width':1.6},e)}
function temple(D,x,y,s){const e=el('g',{transform:`translate(${x},${y}) scale(${K1*s})`},D);
 el('ellipse',{cx:0,cy:3,rx:100,ry:12,fill:'#000',opacity:.15},e);
 el('rect',{x:-70,y:-60,width:140,height:60,fill:'#b8946a',stroke:INK,'stroke-width':2},e);
 el('path',{d:'M-96,-60 Q-80,-72 0,-86 Q80,-72 96,-60z',fill:'#6e6a64',stroke:INK,'stroke-width':2,'stroke-linejoin':'round'},e);
 el('path',{d:'M-78,-86 Q-56,-98 0,-112 Q56,-98 78,-86 Q40,-92 0,-96 Q-40,-92 -78,-86z',fill:'#5f5b55',stroke:INK,'stroke-width':2,'stroke-linejoin':'round'},e);
 for(const px of [-56,-20,20,56])el('rect',{x:px-5,y:-60,width:10,height:60,fill:'#8a3a24',stroke:INK,'stroke-width':1.2},e);
 el('rect',{x:-16,y:-44,width:32,height:44,fill:'#2b2218'},e);
 el('ellipse',{cx:-70,cy:-8,rx:7,ry:9,fill:'#ffb347',opacity:.9},e);el('ellipse',{cx:70,cy:-8,rx:7,ry:9,fill:'#ffb347',opacity:.9},e)}
const VF=(k,x)=>Object.assign({sz:70,col:k%2?VI.tun:'#7a4f26',trou:VI.trou,hat:'khan',hatcol:k%2?'#6b4a2a':'#8a3a24',arm:'spear',armor:k%3==0,acol:VI.arm},x||{});
const SF=(k,x)=>Object.assign({sz:70,col:SO.tun,trou:SO.trou,hat:'songhelm',plume:k%7==3,armor:true,acol:SO.arm,arm:'spear',tassel:'#8c2a1e',flip:true},x||{});
function mkGround(D,tau,o){o=o||{};const poly=(pts,fill,ex)=>el('polygon',Object.assign({points:pts.map(p=>Lc(p[0],p[1]).join(',')).join(' '),fill},ex||{}),D);const X=14000;
 poly([[-X,-1300],[X,-1300],[X,1300],[-X,1300]],o.tint||'#dfe6bd',{opacity:o.top||.55});
 if(o.sea){const v0=o.sea;poly([[-X,-1300],[X,-1300],[X,v0],[-X,v0]],'#7fa7c4');poly([[-X,v0],[X,v0],[X,v0+16],[-X,v0+16]],'#efe2b8');
  for(let i=0;i<40;i++){const u=((i*91+tau*14)%2400)-1200,v=-420+((i*53)%(v0+440)),a=Lc(u,v),b=Lc(u+30,v);el('path',{d:`M${a[0]},${a[1]} L${b[0]},${b[1]}`,stroke:'#e8f4fa','stroke-width':W(1.8),opacity:.5,'stroke-linecap':'round'},D)}}
 if(o.river){const [v0,v1]=o.river;poly([[-X,v0],[X,v0],[X,v1],[-X,v1]],'#7fa7c4');poly([[-X,v0-14],[X,v0-14],[X,v0],[-X,v0]],'#efe2b8');poly([[-X,v1],[X,v1],[X,v1+14],[-X,v1+14]],'#efe2b8')}
 if(o.road){const [a,b]=o.road;el('path',{d:`M${Lc(-1500,a).join(',')} L${Lc(1500,b).join(',')}`,stroke:'#cdb985','stroke-width':W(o.rw||44),fill:'none',opacity:.6,'stroke-linecap':'round'},D)}
}
function scenery(c,seed,o){o=o||{};const f=rnd(seed);const n=o.n||16;for(let i=0;i<n;i++){const u=-1100+i*(2200/n)+f()*60,v=(i%2?1:-1)*((o.vmin||330)+f()*110);if(o.skip&&o.skip(u,v))continue;const p=Lc(u,v);c.push(p[1],()=>tree(c.D,p[0],p[1],.9+f()*.4))}}
function FG(c,u,v,o,key){const p=Lc(u,v);if(key)POS[key]=[u,v];c.push(p[1],()=>fig(c.D,p[0],p[1],o))}
// đoàn người đi dọc: n người, bắt đầu từ trái, tốc độ spd (px/giây của cảnh)
function column(c,n,spd,v,mk,o){o=o||{};const sp=o.gap||92;for(let k=0;k<n;k++){const span=2500,u0=((k*sp+c.tau*spd)%span)-1250;const rev=spd<0;const uu=rev?-u0:u0;
  const x=Object.assign({},mk(k),{walk:c.tau*spd*.09+k*1.1,flip:rev});
  FG(c,uu,v+(k%2)*14,x,o.keys&&o.keys[k])}}
function dust(c,uf,v,tau){}
function shootRow(c,list,v,mk,tgtFn,ts0,gap,dt,fire){list.forEach((u,j)=>{const sh=shot(j,c.tau,ts0,gap,dt);FG(c,u,v+(j%2)*8,Object.assign(mk(j),{arm:'bow',d:sh.d,nock:sh.nock,fire:fire&&c.tau>fire&&j%2==0}));
  const S0=Lc(u+18*(mk(j).flip?-1:1),v+(j%2)*8-52);for(let n=Math.max(0,Math.floor((c.tau-ts0-j*dt-.85)/gap));n<=Math.floor((c.tau-ts0-j*dt)/gap)+1;n++){const ts=ts0+j*dt+n*gap,p=(c.tau-ts)/.85;if(p<=0||p>=1)continue;const tg=tgtFn(j,n,ts+.85);c.arrows.push([S0,Lc(tg[0],tg[1]),p,fire&&c.tau>fire&&j%2==0])}})}
const SCN={};
SCN.march={gnd:{road:[110,130],rw:50},build(c){const it=c.it,sv=it.side||'v',n=it.n||12,spd=it.spd||95*(it.dir||1);
  scenery(c,5,{n:18,vmin:300});[-700,300].forEach((u,i)=>{const p=Lc(u,-420);c.push(p[1],()=>hill(c.D,p[0],p[1],1.4-i*.2))});
  column(c,n,spd,120,k=>sv=='v'?VF(k):SF(k),{keys:{0:'lead'}});
  if(it.carry)for(let k=0;k<4;k++){const u=((k*150+c.tau*spd*.8+400)%2500)-1250;FG(c,(spd<0?-u:u),205,Object.assign(VF(k),{arm:'none',sack:true,walk:c.tau*8+k,flip:spd<0}))}},
 badges:it=>it.badge?[Object.assign({key:'lead',fh:70},it.badge)]:[]};
SCN.tl={gnd:{road:[140,140],rw:70,tint:'#e6dcb4'},build(c){
  const hs=[[-640,-120],[-420,-190],[-200,-130],[260,-170],[480,-120],[680,-200],[-760,-250],[560,-300]];hs.forEach(([u,v],i)=>{const p=Lc(u,v);c.push(p[1],()=>house(c.D,p[0],p[1],1.2+(i%3)*.15,0,0))});
  {const p=Lc(0,-170);c.push(p[1],()=>gateT(c.D,p[0],p[1],1.5))}
  scenery(c,9,{n:10,vmin:380});
  [-90,90].forEach((u,i)=>FG(c,u,-150+i*4,SF(i,{col:VI.tun,trou:VI.trou,hat:'khan',hatcol:'#6b4a2a',armor:true,acol:VI.arm,flip:false,tassel:null}),null));
  column(c,5,-34,150,k=>({sz:68,col:'#8c7a58',trou:VI.trou,hat:'non',arm:'none',sack:k%2==0}),{gap:210});
  column(c,3,30,185,k=>({sz:70,col:k%2?'#3d3a52':'#5a3b4a',trou:'#2b2218',hat:'quan',arm:'none'}),{gap:320});
  FG(c,-300,220,{sz:86,col:'#7a3b1c',trou:'#4a2a1a',hat:'ltk',hatcol:'#b3261e',arm:'point',armor:true,pauld:true,acol:'#b08a3a',cape:true,beard:true},'ltk')},
 badges:it=>it.badge?[{key:'ltk',fh:86,kind:'v',name:'Lý Thường Kiệt',sub:'Đại Việt',below:true}]:[]};
SCN.xuong={gnd:{river:[-150,60],road:[140,150],tint:'#e3dcb8'},build(c){
  scenery(c,3,{n:14,vmin:330});
  [[-420,0],[-80,-14],[300,-6]].forEach(([u,v],i)=>{const p=Lc(u,v),prog=cl((c.tau-.5-i*1.5)/7);c.push(p[1],()=>{boat(c.D,p[0],p[1],{burn:0,al:.35+.65*prog});for(let q=0;q<5;q++)el('path',{d:`M${p[0]+W(-80+q*40)},${p[1]+W(4)} l0,${-W(36*(1-prog)+8)}`,stroke:'#8a5a2b','stroke-width':W(3)},c.D)})});
  [-460,-380,-130,-40,260,340].forEach((u,i)=>FG(c,u,i%2?70:84,{sz:66,col:'#8c7a58',trou:VI.trou,hat:'cap',arm:'flail',tt:c.tau*.55,ph:i,flip:i%2==0},null));
  [-300,150,420,-560].forEach((u,i)=>FG(c,u,112,SF(i,{key:null}),i==1?'a':i==3?'b':null));
  for(let k=0;k<3;k++)FG(c,-100+k*60,170,{sz:66,col:'#8c7a58',trou:VI.trou,hat:'cap',arm:'none',sack:true,walk:c.tau*7+k,flip:k==1},null)},
 badges:it=>[{key:'a',fh:70,kind:'s',name:'Thẩm Khởi',sub:'quan nhà Tống',t0:2,below:true},{key:'b',fh:70,kind:'s',name:'Lưu Di',sub:'quan nhà Tống',t0:3,below:true}]};
SCN.bien={gnd:{sea:-120,tint:'#e3dcb8'},build(c){
  const bd=ease(cl((c.tau-.3)/6));
  [-500,-120,260,560].forEach((u,i)=>{const p=Lc(u+(1-bd)*(i%2?-90:90),-260+bd*130+Math.sin(c.tau*1.3+i)*3);c.push(p[1],()=>{boat(c.D,p[0],p[1],{al:1});for(let q=0;q<3;q++)fig(c.D,p[0]+W(-40+q*40),p[1]-W(8),VF(i+q,{sz:62,flip:false}))})});
  [-600,-300,-20,300,560].forEach((u,i)=>{const p=Lc(u,40+(i%2)*40),b=ease(cl((c.tau-6-i*.8)/1.4));c.push(p[1],()=>{house(c.D,p[0],p[1],1.3,b,0);if(b>.02)flameC(c.D,p[0],p[1]-W(44),W(15)*b,c.tau+i,1)})});
  for(let i=0;i<9;i++){const u=-560+i*140;const lt=c.tau>3.5+i*.3?1:0;FG(c,lt?u+(i%3-1)*40:u-60,130+(i%2)*10+lt*0,VF(i,{walk:lt&&c.tau<8+i*.3?c.tau*8:0}),null)}
  for(let i=0;i<5;i++)FG(c,-500+i*230,80,SF(i,{al:1-cl((c.tau-8-i*.5)/1.5),arm:c.tau>8+i*.5?'flail':'spear',tt:c.tau,ph:i}),null);
  c.vi=true},badges:()=>[]};
SCN.ai={gnd:{road:[40,40],rw:130,tint:'#d9e0b4'},build(c){
  [-900,-480,-60,380,800].forEach((u,i)=>{const p=Lc(u,-250-(i%2)*30);c.push(p[1],()=>hill(c.D,p[0],p[1],2.3,i%2?'#8fa070':'#9aa57a'))});
  [-780,-300,200,640].forEach((u,i)=>{const p=Lc(u,320+(i%2)*30);c.push(p[1],()=>hill(c.D,p[0],p[1],2.1,i%2?'#8fa070':'#9aa57a'))});
  const cols=[];for(let k=0;k<12;k++){const u=((k*88+c.tau*52)%2600)-1300;const hit=cl((c.tau-5-((k*37)%9)*.4)/1.2);if(u<-950||u>950)continue;cols.push(k);
   FG(c,u,40+(k%2)*16,SF(k,Object.assign({flip:false,walk:c.tau*5+k,al:1-hit*.0},hit>0?{arm:'flail',tt:c.tau,ph:k,rot:hit*70*(k%2?1:-1)}:{})),null)}
  const top=[-640,-440,-240,-40,160,360,560],bot=[-560,-340,-120,100,320,540];
  top.forEach((u,j)=>{const sh=shot(j,c.tau,2.5,1.5,.3);FG(c,u,-190+(j%2)*10,Object.assign(VF(j,{flip:false,sz:66}),{arm:'bow',d:sh.d,nock:sh.nock}),null);
   const S0=Lc(u+18,-190+(j%2)*10-52);for(let n=Math.max(0,Math.floor((c.tau-2.5-j*.3-.85)/1.5));n<=Math.floor((c.tau-2.5-j*.3)/1.5)+1;n++){const ts=2.5+j*.3+n*1.5,p=(c.tau-ts)/.85;if(p<=0||p>=1)continue;c.arrows.push([S0,Lc(u-200+((n*3+j)%5)*70,45),p,false])}});
  bot.forEach((u,j)=>{const sh=shot(j,c.tau,2.9,1.5,.3);FG(c,u,215+(j%2)*10,Object.assign(VF(j+1,{flip:false,sz:66}),{arm:'bow',d:sh.d,nock:sh.nock}),null);
   const S0=Lc(u+18,215+(j%2)*10-52);for(let n=Math.max(0,Math.floor((c.tau-2.9-j*.3-.85)/1.5));n<=Math.floor((c.tau-2.9-j*.3)/1.5)+1;n++){const ts=2.9+j*.3+n*1.5,p=(c.tau-ts)/.85;if(p<=0||p>=1)continue;c.arrows.push([S0,Lc(u-150+((n*3+j)%5)*70,50),p,false])}})},
 badges:()=>[],burst:[{t:6.2,u:-100,v:20},{t:8.4,u:240,v:30}]};
SCN.camp={gnd:{tint:'#d9dcb4',road:[160,150]},build(c){
  scenery(c,12,{n:14,vmin:380});
  [[-620,-100],[-340,-150],[-60,-110],[240,-150],[520,-100],[-480,60],[330,70]].forEach(([u,v],i)=>{const p=Lc(u,v);c.push(p[1],()=>tent(c.D,p[0],p[1],1.5,i%2?'#8d9bb5':'#a3aec4'))});
  {const p=Lc(-120,120);c.push(p[1],()=>flameC(c.D,p[0],p[1],W(12),c.tau,1))}
  [-250,-60,180,420,-520].forEach((u,i)=>FG(c,u,170+(i%2)*20,SF(i,{arm:'none',rot:80*(i%2?1:-1),flip:i%2==0,hat:'songhelm',sz:66}),null));
  [-180,40,300,-380,520].forEach((u,i)=>FG(c,u+Math.sin(c.tau*.9+i)*3,95+(i%3)*14,SF(i,{arm:'spear',rot:Math.sin(c.tau*.7+i)*5,flip:i%2==0}),null))},
 badges:()=>[]};
SCN.dam={gnd:{tint:'#e3dcb8',road:[120,120]},build(c){
  scenery(c,21,{n:12,vmin:360});
  const out=ease(cl((c.tau-12)/8));
  [-640,500].forEach((u,i)=>{const p=Lc(u,-110);c.push(p[1],()=>tent(c.D,p[0],p[1],1.5,i?'#8d9bb5':'#9a6e3a'))});
  [-300,-420,-520].forEach((u,i)=>FG(c,u,100+i*22,VF(i,{flip:false,arm:i==0?'point':'spear'}),i==0?'ltk2':null));
  FG(c,-210,125,{sz:86,col:'#7a3b1c',trou:'#4a2a1a',hat:'ltk',hatcol:'#b3261e',arm:'point',armor:true,pauld:true,acol:'#b08a3a',cape:true,beard:true},'ltk');
  [200,320,440].forEach((u,i)=>FG(c,u+out*900,100+i*22,SF(i,{walk:out>0&&out<1?c.tau*8:0}),null));
  FG(c,120+out*900,125,SF(3,{plume:true,hat:'songhelm'}),null)},
 badges:()=>[{key:'ltk',fh:86,kind:'v',name:'Lý Thường Kiệt',sub:'Đại Việt',below:true}]};
SCN.voi={gnd:{road:[120,130],rw:70,tint:'#e6dcb4'},build(c){
  scenery(c,31,{n:12,vmin:360});
  {const p=Lc(780,-90);c.push(p[1],()=>gateT(c.D,p[0],p[1],2.0))}
  for(let k=0;k<5;k++){const u=((k*300+c.tau*60)%2600)-1500;const p=Lc(u,130+(k%2)*18);c.push(p[1],()=>{ele(c.D,p[0],p[1],K1*1.1,c.tau*5+k,false)})}
  for(let k=0;k<5;k++){const u=((k*300+c.tau*60)%2600)-1500;FG(c,u-110,170+(k%2)*8,VF(k,{walk:c.tau*5.4+k,flip:false,arm:'spear'}),k==0?'ex':null)}
  FG(c,((0*300+c.tau*60)%2600)-1500-230,150,{sz:74,col:'#8a5a2b',trou:VI.trou,hat:'khan',hatcol:'#8a3a24',arm:'none',walk:c.tau*5.4},'envoy');
  [660,880].forEach((u,i)=>FG(c,u,50,SF(i,{flip:true}),null));
  FG(c,740,60,{sz:76,col:'#5a3b4a',trou:'#2b2218',hat:'quan',arm:'none',flip:true},null)},
 badges:()=>[{key:'envoy',fh:74,kind:'v',name:'Đào Tống Nguyên',sub:'sứ thần Đại Việt',t0:1.5}]};
SCN.giao={gnd:{tint:'#e3dcb8',road:[130,130]},build(c){
  scenery(c,41,{n:12,vmin:360});
  {const p=Lc(0,100);c.push(p[1],()=>{el('path',{d:`M${p[0]-W(14)},${p[1]} L${p[0]-W(14)},${p[1]-W(60)} L${p[0]},${p[1]-W(72)} L${p[0]+W(14)},${p[1]-W(60)} L${p[0]+W(14)},${p[1]}z`,fill:'#a39a86',stroke:INK,'stroke-width':W(2)},c.D)})}
  const g=ease(cl((c.tau-2)/10));
  for(let i=0;i<5;i++){FG(c,260+i*70-g*900,95+(i%2)*20,SF(i,{walk:g>0&&g<1?c.tau*7:0,flip:true}),null);FG(c,-320-i*70+g*0,110+(i%2)*14,VF(i,{flip:false}),null)}
  for(let i=0;i<4;i++){const u=-480+((c.tau*34+i*140)%900);FG(c,u,170+(i%2)*16,{sz:66,col:'#8c7a58',trou:VI.trou,hat:'cap',arm:'none',walk:c.tau*7+i,flip:false},null)}
  for(let i=0;i<4;i++)FG(c,-600-i*60+g*500,60,{sz:70,col:'#3d3a52',trou:'#2b2218',hat:'quan',arm:'none',flip:false,al:i<2?1:1},null)},
 badges:()=>[]};
SCN.nha={gnd:{tint:'#ecd9b4',top:.7},build(c){
  scenery(c,51,{n:10,vmin:360});
  [[-420,-100],[420,-130]].forEach(([u,v],i)=>{const p=Lc(u,v);c.push(p[1],()=>house(c.D,p[0],p[1],1.7,0,0))});
  {const p=Lc(0,-120);c.push(p[1],()=>gateT(c.D,p[0],p[1],1.2))}
  FG(c,-60,110,{sz:86,col:'#7a3b1c',trou:'#4a2a1a',hat:'ltk',hatcol:'#b3261e',arm:'none',armor:true,pauld:true,acol:'#b08a3a',cape:true,beard:true},'ltk');
  [100,-200,230].forEach((u,i)=>FG(c,u,125+i*10,VF(i,{flip:i!=1,arm:'none',sz:68}),null))},
 badges:()=>[{key:'ltk',fh:84,kind:'v',name:'Lý Thường Kiệt',sub:'qua đời năm 1105',t0:2,below:true}]};
SCN.den={gnd:{river:[-100,70],tint:'#cfd6b4'},build(c){
  const p=Lc(0,150);c.push(p[1],()=>temple(c.D,p[0],p[1],1.5));
  scenery(c,61,{n:12,vmin:380});
  for(let i=0;i<10;i++)FG(c,-420+i*95,(i%2)*20+250,VF(i,{flip:i>4?true:false,arm:i%3==0?'bow':'spear',d:0,sz:68}),null);
  for(let i=0;i<4;i++){const q=Lc(-300+i*200,200);c.push(q[1]-1,()=>{el('rect',{x:q[0]-W(2),y:q[1]-W(40),width:W(4),height:W(40),fill:'#5a3b1c'},c.D);flameC(c.D,q[0],q[1]-W(42),W(8),c.tau+i,1)})}},
 badges:()=>[]};
//@@CC2-BEGIN
// ===== Cảnh riêng từng đoạn (mỗi cảnh chỉ dùng MỘT lần) — mini-DSL =====
const FT={
 v:(n,o)=>VF(n,Object.assign({flip:false},o)),
 s:(n,o)=>SF(n,o),
 d:(n,o)=>Object.assign({sz:66,col:n%2?'#8c7a58':'#9a7c52',trou:VI.trou,hat:'non',arm:'none'},o),
 w:(n,o)=>Object.assign({sz:66,col:'#8c7a58',trou:VI.trou,hat:'cap',arm:'none'},o),
 q:(n,o)=>Object.assign({sz:70,col:n%2?'#3d3a52':'#5a3b4a',trou:'#2b2218',hat:'quan',arm:'none'},o),
 qs:(n,o)=>Object.assign({sz:70,col:n%2?'#3d5a7a':'#2f4a6a',trou:'#1f2a3a',hat:'quan',arm:'none',flip:true},o),
 k:(n,o)=>Object.assign({sz:76,col:'#b3861e',trou:'#4a2a1a',hat:'quan',arm:'none'},o),
 L:(n,o)=>Object.assign({sz:86,col:'#7a3b1c',trou:'#4a2a1a',hat:'ltk',hatcol:'#b3261e',arm:'none',armor:true,pauld:true,acol:'#b08a3a',cape:true,beard:true},o)};
function runS(c,items){let n=0;const tau=c.tau;
 for(const q of items){n++;const k=q[0],u=q[1],v=q[2],a=q[3],b=q[4];const p=Lc(u,v);
  switch(k){
   case'h':c.push(p[1],()=>house(c.D,p[0],p[1],a||1.3,b?ease(cl((tau-b)/1.4)):0,0));break;
   case'g':c.push(p[1],()=>gateT(c.D,p[0],p[1],a||1.5));break;
   case't':c.push(p[1],()=>tent(c.D,p[0],p[1],a||1.5,b||'#a3aec4'));break;
   case'hl':c.push(p[1],()=>hill(c.D,p[0],p[1],a||2,b||'#8fa070'));break;
   case'tp':c.push(p[1],()=>temple(c.D,p[0],p[1],a||1.5));break;
   case'b':c.push(p[1],()=>boat(c.D,p[0],p[1],Object.assign({al:1},a)));break;
   case'e':c.push(p[1],()=>ele(c.D,p[0],p[1],K1*(a||1.1),tau*5+n,!!b));break;
   case'f':c.push(p[1],()=>flameC(c.D,p[0],p[1],W(a||12),tau+n,1));break;
   case'k':c.push(p[1],()=>stake(c.D,p[0],p[1],a||40,b||4,'#5a3b1c'));break;
   case'tr':c.push(p[1],()=>tree(c.D,p[0],p[1],a||1.1));break;
   case'fig':{const o=Object.assign({},FT[a](n,b&&b.o?{}:{}),b||{});if(o.w){o.walk=tau*7+n;delete o.w}if(o.sw){o.rot=Math.sin(tau*.8+n)*4;delete o.sw}
     const key=o.key;delete o.key;FG(c,u,v,o,key);break}
   case'col':{const [t,cnt,spd,gap,o]=[a,b,q[4],q[5],q[6]||{}];/*['col',u0,v,type,n,spd,gap,opts]*/break}
   case'vol':{const u2=a,v2=b,cnt=q[5]||6;for(let j=0;j<cnt;j++){const ts=j*.45,p0=((tau-ts)%2.6)/1.0;if(p0<=0||p0>=1)continue;c.arrows.push([Lc(u,v),Lc(u2+((j*7)%5)*50,v2+((j*3)%4)*14),p0,false])}break}
  }}}
// đoàn đi: ['mv', type, n, spd, v, gap, opts]
function mvS(c,type,cnt,spd,v,gap,o){column(c,cnt,spd,v,k=>FT[type](k,o||{}),{gap:gap||100})}
const R2=(name,gnd,items,badges,extra)=>{SCN[name]={gnd,build(c){scenery(c,extra&&extra.seed||name.length*7,{n:extra&&extra.trees!=null?extra.trees:10,vmin:extra&&extra.vmin||380});runS(c,items);if(extra&&extra.mv)for(const m of extra.mv)mvS(c,...m);if(extra&&extra.dyn)extra.dyn(c)},badges:()=>badges||[]}};
const LB=(sub,below)=>({key:'ltk',fh:86,kind:'v',name:'Lý Thường Kiệt',sub:sub||'Đại Việt',below:below!==false,t0:1.5});
const Lf=(u,v,o)=>['fig',u,v,'L',Object.assign({key:'ltk'},o||{})];
const F=(t,u,v,o)=>['fig',u,v,t,o||{}];
// 1 vượt biên đêm
R2('hoBien',{river:[-40,40],road:[130,130],rw:56,tint:'#cfd3b0'},[['hl',-760,-260,2.3],['hl',420,-300,2.5],['h',620,-190,1.4],['f',380,-120,14],['f',-520,-100,12],['k',150,30,70,5],F('v',-40,170,{w:1}),F('v',-170,190,{w:1}),F('v',-300,160,{w:1}),F('v',-440,185,{w:1}),F('v',90,175,{w:1}),F('s',470,-60,{arm:'spear'}),F('s',560,-40,{arm:'spear'})],[],{mv:[['v',7,-60,95,200,{arm:'spear'}]]});
// 2 lính canh Việt nhìn quân Tống từ xa
R2('canhGac',{river:[-120,-40],tint:'#dde0b8'},[['hl',-800,-300,2.4],['hl',-100,-340,2.1],['hl',620,-290,2.2],['t',-420,90,1.4,'#a8854e'],['f',-300,120,11],F('v',-120,130,{arm:'spear'}),F('v',60,160,{arm:'spear'}),F('v',-260,175,{arm:'bow'}),F('s',-300,-200,{walk:0}),F('s',-180,-210),F('s',40,-190),F('s',220,-215),F('s',400,-195),F('s',560,-220)],[],{mv:[['s',6,50,90,-170,{arm:'spear'}]]});
// 3-4 hai hướng: quân Việt tiến một bên sông, quân Tống đứng canh bên kia
R2('haiHuong',{river:[-20,70],tint:'#e3dcb8'},[['h',-640,-170,1.3],['h',660,-180,1.3],['b',200,10,{al:1}],['tp',-300,-220,1.2],F('L',-470,150,{arm:'point',key:'ltk'}),F('v',-600,180),F('v',-700,160),F('v',-340,200),F('s',470,-40),F('s',560,-10),F('s',650,-30),F('s',720,20)],[LB('chỉ huy',false)],{mv:[['v',4,70,90,230,{arm:'spear'}]]});
// 5-6 nhìn về phía bắc từ đồi
R2('nhinBac',{tint:'#e8dfb8',top:.7},[['hl',-700,-250,2.6,'#8da16e'],['hl',100,-330,3,'#97a97a'],['hl',700,-250,2.5],['g',480,-190,1.6],F('L',-120,150,{arm:'point',key:'ltk',flip:false}),F('v',-290,170),F('v',-360,200),F('v',140,190,{flip:true})],[LB('nhìn về phía bắc')]);
// 7 phường Thái Hòa: nhà, chợ
R2('phuong',{road:[150,150],rw:90,tint:'#e6dcb4'},[['h',-700,-170,1.4],['h',-380,-200,1.2],['h',200,-190,1.3],['h',560,-160,1.5],['t',-120,-80,1.0,'#b89862'],['t',360,-60,1.0,'#a8854e'],F('d',-60,-20,{sw:1}),F('d',-180,-10,{sw:1}),F('d',320,10,{sw:1}),F('w',420,20,{sw:1}),F('d',-560,60),F('d',-460,80,{flip:true})],[],{mv:[['d',5,40,110,200,{sack:true}],['q',2,-30,160,300]]});
// 8-9 gia đình quan: sân nhà, cha và con
R2('giaDinh',{tint:'#ead9b4',top:.7},[['h',-420,-180,1.9],['h',460,-200,1.7],['tp',0,-250,1.0],['tr',-760,-60,1.3],['tr',780,-30,1.2],F('q',-90,100,{sw:1}),F('d',30,120,{sz:52,flip:true}),F('d',-250,150,{flip:true}),F('w',320,140,{flip:true})],[]);
// 10-12 triều đường
R2('trieuDuong',{tint:'#e0cfa4',top:.8},[['g',0,-260,2.2],['h',-760,-160,1.6],['h',760,-160,1.6],F('k',0,-120,{arm:'none',sw:1}),F('q',-380,-10),F('q',-250,0),F('q',-120,10),F('q',120,10,{flip:true}),F('q',250,0,{flip:true}),F('q',380,-10,{flip:true}),Lf(-40,150),F('v',-500,160,{arm:'spear'}),F('v',500,160,{arm:'spear',flip:true})],[LB('trong triều')]);
// 13 hạm đội vua Lý ra khơi
R2('hamDoi',{sea:-90,tint:'#e3dcb8'},[['b',-500,-250,{}],['b',-120,-300,{}],['b',300,-230,{}],['b',640,-290,{}],['b',-260,-150,{}],F('L',-60,150,{arm:'point',key:'ltk'}),F('v',-180,170),F('v',70,180,{flip:true})],[LB('theo vua nam chinh')],{trees:3});
// 14 Chiêm Thành: thành đất bị chiếm, voi chiến
R2('chiemThanh',{tint:'#e9d8a8'},[['g',-360,-210,1.9],['h',-640,-130,1.1,2],['h',580,-190,1.2,3],['e',260,60,1.2,1],['e',480,100,1.2,0],F('v',-60,110,{arm:'spear'}),F('v',-180,130,{arm:'spear'}),F('v',60,160,{arm:'spear',flip:true}),F('d',360,-10,{flip:true,sz:60,hat:'cap'})],[]);
// 15-16 nhận chức Thái úy
R2('thaiUy',{tint:'#e6d3a8',top:.8},[['g',0,-240,1.8],['h',-740,-150,1.3],['h',740,-150,1.3],F('k',150,-60,{flip:true}),Lf(-60,60,{arm:'none'}),F('q',-300,100),F('q',-420,120),F('q',330,120,{flip:true}),F('v',-560,170,{arm:'spear'}),F('v',560,170,{arm:'spear',flip:true})],[LB('Thái úy, năm 1075')]);
// 17-18 quân Tống làm đường, dựng trại ở biên
R2('tongBien',{road:[60,60],rw:120,tint:'#d9dcb4'},[['t',-560,-130,1.3,'#8d9bb5'],['t',-300,-170,1.3,'#a3aec4'],['t',560,-150,1.3,'#8d9bb5'],['k',300,70,60,6],['k',360,60,60,6],F('s',-80,10,{arm:'flail',sw:1}),F('s',20,40,{arm:'flail'}),F('s',120,0,{arm:'spear'}),F('w',-200,160,{arm:'flail',sw:1}),F('w',420,160,{arm:'flail'})],[],{mv:[['w',4,60,100,180,{sack:true,sz:62}]]});
// 19-20 triều Tống
R2('trieuTong',{tint:'#d8dce6',top:.8},[['g',0,-250,2.2],['h',-720,-170,1.5],['h',720,-170,1.5],F('qs',-340,-20),F('qs',-210,0),F('qs',-90,10),F('qs',100,10,{flip:true}),F('qs',230,0,{flip:true}),F('qs',360,-20,{flip:true}),F('k',0,-100,{col:'#3d5a8a'}),F('s',-520,150,{arm:'spear'}),F('s',520,150,{arm:'spear',flip:false})],[]);
// 21 Vương An Thạch: bàn viết, người xếp hàng
R2('vuongAnThach',{tint:'#dde0e8',top:.8},[['h',-620,-170,1.6],['h',620,-190,1.6],['t',0,-70,1.5,'#6a6a7a'],F('qs',0,30,{key:'van',sw:1}),F('d',-200,150,{walk:0}),F('d',-300,170),F('d',-410,160),F('w',280,150,{flip:true}),F('qs',-120,70,{flip:true,sz:60})],[{key:'van',fh:70,kind:'s',name:'Vương An Thạch',sub:'người cải cách nhà Tống',t0:1.5,below:true}]);
// 22-23 lính Tống tập luyện
R2('taoLuyen',{tint:'#d9dcb4',road:[150,150]},[['t',-640,-150,1.4,'#8d9bb5'],['t',600,-170,1.4,'#a3aec4'],['hl',0,-340,2.6,'#8fa070']].concat([-380,-220,-60,100,260,420].map((u,i)=>F('s',u,40+(i%2)*14,{arm:'spear',rot:Math.sin(0+i)*4,sw:1}))).concat([F('qs',-60,-80,{sz:76,hat:'quan'}),F('s',-300,180,{arm:'bow'}),F('s',-120,200,{arm:'bow'})]),[]);
// 24 xưởng đóng thuyền
R2('xuongThuyen',{river:[-170,40],road:[140,150],tint:'#e3dcb8'},[['b',-420,-60,{al:.5}],['b',-40,-70,{al:.8}],['b',340,-60,{al:.35}],['h',-720,-230,1.3],['h',700,-240,1.3],F('qs',-250,120,{key:'tk',sw:1}),F('qs',250,130,{key:'ld',flip:true}),F('w',-100,60,{arm:'flail',sw:1}),F('w',60,80,{arm:'flail'}),F('w',-360,70,{arm:'flail'}),F('d',480,100,{sack:true,w:1})],[{key:'tk',fh:70,kind:'s',name:'Thẩm Khởi',sub:'quan nhà Tống',t0:1.5,below:true},{key:'ld',fh:70,kind:'s',name:'Lưu Di',sub:'quan nhà Tống',t0:2.5,below:true}]);
// 25-26 họp bàn trong triều Lý
R2('hopBan',{tint:'#e0cfa4',top:.8},[['h',-700,-170,1.5],['h',720,-170,1.5],['g',0,-250,1.7],['t',0,-30,1.8,'#9a6e3a'],F('k',0,-100,{sw:1}),Lf(-210,80,{arm:'point'}),F('q',-380,130),F('q',280,100,{flip:true}),F('q',420,130,{flip:true}),F('v',-520,170,{arm:'spear'})],[LB('bàn việc nước',false)]);
// 27 tháp canh đêm
R2('thapCanh',{tint:'#cfd3b0'},[['g',60,-200,2.0],['hl',-760,-250,2.4],['hl',700,-300,2.6],['f',-120,-60,12],['f',280,-40,12],Lf(-30,110,{arm:'point'}),F('v',-210,160,{flip:false}),F('v',150,170,{flip:true})],[LB('trước khi quyết định')]);
// 28-29 xuất quân
R2('xuatQuan',{road:[110,110],rw:80,tint:'#d9dcb4'},[['t',-700,-140,1.4,'#a3541e'],['t',-420,-190,1.4,'#8a5a2b'],['t',640,-180,1.4,'#a3541e'],Lf(-160,60,{arm:'point'}),F('v',-300,130,{arm:'spear'}),F('v',-40,130,{arm:'spear'}),F('v',80,110,{arm:'spear'}),F('q',300,60,{flip:true,sz:66})],[LB('chỉ huy chiến dịch',false)],{mv:[['v',9,80,88,190,{arm:'spear'}]]});
// 30 thanh miêu
R2('thanhMieu',{road:[160,160],tint:'#e3dcb8'},[['h',-560,-150,1.4],['h',-100,-190,1.3],['h',520,-150,1.5],['t',120,-30,1.5,'#6a6a7a'],F('qs',120,60,{key:'ts',flip:true,sw:1}),F('qs',250,90,{flip:true,sz:62}),F('d',-60,150,{w:0}),F('d',-170,170,{sz:60}),F('d',-290,150),F('w',20,170,{sack:true}),F('s',380,110,{arm:'spear',flip:true})],[]);
// 31-32 lều quân: bàn chiến lược
R2('leuQuan',{tint:'#d9dcb4'},[['t',-300,-170,2.4,'#a3541e'],['t',420,-150,1.6,'#8a5a2b'],['t',-740,-130,1.3,'#a3541e'],['f',100,90,12],Lf(-90,100,{arm:'point'}),F('v',-250,140,{sw:1}),F('v',60,150,{flip:true}),F('q',230,170,{flip:true}),F('v',-440,185,{arm:'spear'})],[LB('lập kế hoạch tiến công')]);
// 34 thuyền chiến Việt đánh vào bờ biển Tống
R2('duongBien',{sea:-100,tint:'#e3dcb8'},[['b',-560,-300,{}],['b',-120,-260,{}],['b',320,-320,{}],['b',620,-250,{}],['h',-560,60,1.2,2],['h',-80,40,1.3,4],['h',380,70,1.2,3],['h',700,50,1.1],F('v',-300,130,{arm:'spear',w:1}),F('v',-120,150,{arm:'spear',w:1}),F('v',140,150,{arm:'spear',w:1}),F('s',520,150,{arm:'flail'}),F('s',-400,175,{arm:'spear'})],[],{trees:2});
// 35 Khâm Châu, Liêm Châu: đổ bộ, thành nhỏ cháy
R2('khamChau',{sea:-60,tint:'#e9d8a8'},[['g',100,-190,1.7],['h',-640,-80,1.3,2.5],['h',-300,-100,1.2,3.5],['h',560,-100,1.4,4.5],['b',-480,-220,{}],['b',420,-240,{}],F('v',-120,100,{arm:'spear',w:1}),F('v',20,130,{arm:'spear',w:1}),F('v',200,110,{arm:'spear'}),F('s',-260,60,{arm:'spear',flip:true})],[],{trees:3});
// 36-37 hành quân qua núi
R2('duongNui',{road:[70,150],rw:60,tint:'#d4dfb0'},[['hl',-760,-260,3,'#8da16e'],['hl',-200,-330,3.2,'#7f9462'],['hl',420,-260,2.8,'#97a97a'],['hl',800,-330,2.6]],[],{trees:16,vmin:260,mv:[['v',13,-70,86,170,{arm:'spear'}],['d',3,-60,160,260,{sack:true}]]});
// 38-39 Côn Lôn: chặn viện binh (cảnh ải cũ)
// 40 đến sát Ung Châu (nhìn từ xa)
R2('ucXa',{river:[-220,-140],tint:'#e3dcb8'},[['g',0,-300,2.0],['h',-300,-300,1.2],['h',320,-310,1.2],['h',-600,-250,1.0],['h',620,-260,1.0],F('v',-280,60,{arm:'spear'}),F('v',-120,90,{arm:'spear'}),F('v',60,60,{arm:'spear'}),F('v',220,100,{arm:'spear'}),F('v',360,70,{arm:'spear'}),F('s',-120,-250,{arm:'bow'}),F('s',40,-260,{arm:'bow'}),F('s',200,-250,{arm:'bow'})],[],{mv:[['v',5,-30,90,170,{arm:'spear'}]]});
// 41 trên mặt thành: lính Tống phòng thủ
R2('mattThanh',{tint:'#d4d8e0',top:.8},[['g',0,-250,2.4],['k',-500,-200,50,5],['k',500,-200,50,5]].concat([-560,-420,-280,-140,140,280,420,560].map((u,i)=>F('s',u,-80+(i%2)*10,{arm:i%2?'bow':'spear',flip:false}))).concat([F('qs',0,40,{sz:78,flip:false}),F('s',-300,160,{arm:'spear'}),F('s',300,170,{arm:'spear'})]),[]);
// 42-43 đắp đồi đất, thang, đào
R2('daoDat',{tint:'#e3dcb8',road:[200,200]},[['hl',-100,-60,1.6,'#b4986a'],['hl',140,-40,1.3,'#b4986a'],['g',-480,-250,1.5],F('v',-20,60,{arm:'flail',sw:1}),F('v',120,70,{arm:'flail'}),F('v',-160,90,{arm:'flail'}),F('d',280,130,{sack:true,w:1}),F('d',420,150,{sack:true,w:1}),F('d',560,130,{sack:true,w:1})],[],{mv:[['d',6,70,100,210,{sack:true}]]});
// 44-46 đối đầu quanh chân thành: tên bay (cảnh uc gốc) -> dùng 'uc'
// 47 tờ lịch bốn mươi ngày: cắm cọc đếm (cảnh đồng không có người)
R2('doDem',{tint:'#e9dfbf'},[['g',480,-260,1.7],['k',-420,80,60,6],['k',-340,90,60,6],['k',-260,80,60,6],['k',-180,90,60,6],['k',-100,80,60,6],['k',-20,90,60,6],['k',60,80,60,6],['f',-520,140,11],['f',200,120,11],F('v',-420,160,{sw:1}),F('v',330,140,{flip:true,arm:'spear'})],[]);
// 48-49 thành sau trận: khói, dân tản
R2('thanhHoang',{tint:'#d9cfb0'},[['h',-560,-130,1.4,0.2],['h',-220,-170,1.3,0.2],['h',320,-150,1.5,0.2],['h',700,-180,1.2,0.2],['f',-560,-160,15],['f',320,-180,15],['g',60,-290,1.7],F('d',-100,80,{walk:0,sw:1}),F('d',20,110,{sz:58}),F('d',-250,130,{flip:true,sack:true,w:1}),F('w',150,140,{flip:true,sack:true,w:1}),F('v',420,130,{arm:'spear'})],[]);
// 50-51 rút quân với xe và lương
R2('rutQuan',{river:[-200,-110],road:[140,160],rw:70,tint:'#e3dcb8'},[['hl',-700,-330,2.2],['b',-100,-155,{al:.9}]],[],{mv:[['v',9,-90,88,170,{arm:'spear',sack:true}],['d',3,-70,110,260,{sack:true}]]});
// 52-53 trạm gác biên giới lúc hoàng hôn
R2('tramGac',{tint:'#e8d6a8',top:.7},[['g',420,-180,1.6],['k',-300,-50,90,6],['f',-200,70,14],F('L',-80,130,{arm:'none',key:'ltk'}),F('v',-300,110,{arm:'spear'}),F('v',60,185,{flip:true,arm:'spear'}),F('s',640,-80,{arm:'spear'})],[LB('nhìn lại phía sau',false)]);
// 54 trại Tống tập kết
R2('tongKetTap',{tint:'#d4d8e0'},[['t',-640,-180,1.6,'#8d9bb5'],['t',-340,-220,1.6,'#a3aec4'],['t',0,-240,1.8,'#8d9bb5'],['t',380,-210,1.6,'#a3aec4'],['t',680,-170,1.6,'#8d9bb5'],['f',-100,60,12],F('s',-380,70,{arm:'spear',sw:1}),F('s',-200,100,{arm:'spear'}),F('s',100,90,{arm:'spear'}),F('s',260,130,{arm:'spear'}),F('qs',-20,150,{sz:76})],[]);
// 55 Quách Quỳ cưỡi đi đầu bộ binh
R2('quachQuy',{road:[110,130],rw:56,tint:'#d9dcb4'},[['hl',-600,-330,2.4],['hl',500,-330,2.4],F('qs',-80,120,{key:'qq',sz:84,flip:false,w:1,plume:true})],[{key:'qq',fh:84,kind:'s',name:'Quách Quỳ',sub:'chỉ huy bộ binh nhà Tống',t0:1.5,below:true}],{mv:[['s',11,86,84,200,{flip:false}]]});
// 56 nhìn sông Như Nguyệt từ gò cao
R2('nhinSong',{river:[-210,-120],tint:'#e3dcb8'},[['hl',-600,-380,2.3],['hl',420,-380,2.3],Lf(-200,150,{arm:'point'}),F('v',-340,180),F('v',-70,190,{flip:true}),F('s',-140,-300,{arm:'spear'}),F('s',100,-290,{arm:'spear'}),F('s',380,-300,{arm:'spear'})],[LB('chọn nơi đón địch')],{trees:8});
// 58-60 phòng tuyến trên bản đồ (không cận cảnh) -- map only
// 61 đóng cọc, hàng rào bờ sông
R2('phongTuyen',{river:[-260,-150],tint:'#e3dcb8',road:[130,130]},[['b',-200,-205,{al:.4}]].concat([-760,-640,-520,-400,-280,-160,-40,80,200,320,440,560,680].map((u,i)=>['k',u,-130+(i%2)*6,48,5])).concat([F('v',-300,60,{arm:'flail',sw:1}),F('v',-120,80,{arm:'flail'}),F('v',100,60,{arm:'flail'}),F('d',320,120,{sack:true,w:1}),F('d',460,140,{sack:true,w:1}),F('v',-460,100,{arm:'spear'})]),[]);
// 62 gác đêm trên phòng tuyến
R2('gacDem',{river:[-230,-120],tint:'#cfd3b0'},[['f',-440,40,12],['f',200,50,12],['f',620,20,11]].concat([-760,-560,-360,-160,40,240,440,640].map((u,i)=>['k',u,-100,46,5])).concat([F('v',-300,80,{arm:'spear'}),F('v',-220,110,{arm:'spear',flip:true}),F('v',280,100,{arm:'bow'}),F('v',380,120,{arm:'bow'}),F('s',-120,-330,{arm:'spear'})]),[]);
// 65-66 quân dự bị chạy dọc bờ
R2('quanDuBi',{river:[-240,-130],road:[110,110],rw:60,tint:'#dde0b8'},[['h',560,-190,1.2]],[LB('điều quân dọc bờ sông',true)],{mv:[['v',8,130,80,100,{arm:'spear'}]],dyn:c=>FG(c,-300,170,{sz:86,col:'#7a3b1c',trou:'#4a2a1a',hat:'ltk',hatcol:'#b3261e',arm:'point',armor:true,pauld:true,acol:'#b08a3a',cape:true,beard:true},'ltk')});
// 69-70 đường đêm tới đền
R2('denDem',{road:[130,130],rw:40,tint:'#c9cfae'},[['tp',380,-180,1.6],['f',150,40,10],['f',-300,60,10],['hl',-700,-280,2.2],F('v',-120,130,{w:1,arm:'spear'}),F('v',-250,150,{w:1,arm:'spear'}),F('d',60,160,{flip:true,w:1})],[],{mv:[['v',6,50,100,200,{arm:'spear'}]]});
// 72-73 trong đền: hai vị thần, quân sĩ quỳ
R2('trongDen',{tint:'#c9cfae',top:.9},[['tp',0,-190,2.2],['f',-300,40,10],['f',300,40,10]].concat([-360,-200,-40,120,280,440].map((u,i)=>F('v',u,100+(i%2)*22,{arm:'none',rot:60*(i%3==0?0:1)*0,sw:1}))).concat([F('d',-100,190,{sw:1})]),[]);
// 74-77 rạng sáng bờ sông, quân đứng nghe
R2('binhMinh',{river:[-210,-100],tint:'#ecdcb4',top:.7},[['hl',-700,-380,2.6,'#9aa57a'],['hl',480,-390,2.8,'#97a97a'],['tp',-480,-260,1.1]].concat([-520,-380,-240,-100,40,180,320,460,600].map((u,i)=>F('v',u,70+(i%3)*30,{arm:i%2?'spear':'bow',d:0,sw:1}))).concat([Lf(-60,200,{arm:'none'})]),[LB('đọc bài thơ bên sông')]);
// 78 Việt nghỉ bên đống lửa
R2('nghiNgoi',{tint:'#d9dcb4'},[['f',-100,80,13],['f',360,100,12],['t',-520,-110,1.4,'#a3541e'],['t',600,-100,1.4,'#8a5a2b']].concat([-260,-180,-20,60,220,300,480].map((u,i)=>F('v',u,100+(i%3)*24,{arm:'none',rot:i%2?80:-80,flip:i%2==0,sw:0}))),[]);
// 79-80 lương Tống cạn: bao rỗng, ngựa mệt
R2('luongTong',{tint:'#d4d8e0'},[['t',-560,-140,1.4,'#8d9bb5'],['t',480,-150,1.4,'#a3aec4']].concat([-220,-100,40,160,300].map((u,i)=>F('s',u,50+(i%2)*30,{arm:'none',rot:i%2?70:-70,flip:i%2==0}))).concat([F('d',-340,160,{sack:true,w:0}),F('d',-440,180,{sack:true,sz:60}),F('qs',360,120,{sz:72})]),[]);
// 81-83 lều đêm: Lý Thường Kiệt suy nghĩ
R2('leuDem',{tint:'#cfd3b0',top:.9},[['t',-200,-170,2.6,'#a3541e'],['t',500,-120,1.4,'#8a5a2b'],['f',-60,70,14],Lf(-260,100,{arm:'none'}),F('v',80,110,{flip:true,sw:1}),F('q',240,150,{flip:true})],[LB('cân nhắc: đánh tiếp hay thương lượng')]);
// 84-85 đàm phán
R2('thuongLuong',{tint:'#e0d8b8'},[['t',0,-60,1.4,'#6a6a7a'],['h',-720,-180,1.3],['h',720,-190,1.3],Lf(-260,70,{arm:'none'}),F('v',-400,110,{arm:'spear'}),F('v',-520,150,{arm:'spear'}),F('qs',250,70,{flip:true}),F('s',380,110,{arm:'spear',flip:true}),F('s',500,150,{arm:'spear',flip:true})],[LB('đề nghị thương lượng',false)]);
// 86 quân Tống rút
R2('tongRut',{road:[110,130],rw:70,tint:'#dde0b8'},[['hl',-500,-330,2.4],['hl',600,-340,2.4],['t',-760,-160,1.1,'#8d9bb5']],[],{mv:[['s',10,-80,90,150,{arm:'spear',sack:true}]]});
// 87-88 sứ đoàn Việt: viết thư, bản đồ
R2('ngoaiGiao',{tint:'#e6d3a8',top:.8},[['g',0,-260,1.8],['h',-740,-150,1.3],['h',740,-150,1.3],['t',-100,10,1.3,'#9a6e3a'],F('q',-250,70,{sw:1}),F('q',60,70,{flip:true,sw:1}),F('q',-360,130),F('v',-560,170,{arm:'spear'}),F('v',560,170,{arm:'spear',flip:true})],[]);
// 90 trao đất: cột mốc, hai đoàn trao nhận
R2('traDat',{tint:'#e3dcb8',road:[120,120]},[['k',0,60,90,10],['hl',-760,-300,2.2],['hl',700,-300,2.2],F('q',-200,70,{key:'qa'}),F('qs',200,70,{flip:true}),F('v',-340,110,{arm:'spear'}),F('v',-420,140,{arm:'spear'}),F('s',340,110,{arm:'spear',flip:true}),F('s',420,140,{arm:'spear',flip:true})],[]);
// 91-92 trao đổi tù binh
R2('traTu',{road:[120,120],rw:60,tint:'#e3dcb8'},[['hl',-760,-300,2.2],['hl',700,-300,2.2],['k',0,40,90,8],F('v',-440,100,{arm:'spear'}),F('s',440,100,{arm:'spear',flip:true})],[],{mv:[['d',5,45,90,160,{sack:false,hat:'cap'}],['s',4,-40,90,240,{arm:'none',hat:'cap'}]]});
// 93-94 hội đàm Vĩnh Bình (nhà rạp)
R2('vinhBinh',{tint:'#e3dcb8'},[['tp',0,-190,1.5],['t',-520,-110,1.4,'#a3541e'],['t',520,-110,1.4,'#8d9bb5'],F('q',-220,50,{sw:1}),F('q',-340,90),F('qs',220,50,{flip:true,sw:1}),F('qs',340,90,{flip:true}),F('v',-560,150,{arm:'spear'}),F('s',560,150,{arm:'spear',flip:true})],[]);
// 98-99 Thái úy, người có thế lực trong chính sự (tl gốc dùng ở đây)
// 100 Lý Giác nổi dậy ở Diễn Châu
R2('dienChau',{tint:'#d9dcb4',road:[160,150]},[['h',-640,-100,1.3,3],['h',-260,-140,1.2,5],['h',480,-130,1.3],['f',-640,-120,14],F('d',-120,70,{arm:'spear',sz:66,hat:'cap'}),F('d',-20,100,{arm:'spear',hat:'cap'}),F('d',100,80,{arm:'flail',hat:'cap'}),F('v',380,120,{arm:'spear',flip:true}),F('v',480,150,{arm:'spear',flip:true})],[],{mv:[['v',6,-60,86,200,{arm:'spear'}]]});
// 103 tuổi già: triều đường buổi chiều
R2('tuoiGia',{tint:'#ecd9b4',top:.7},[['h',-480,-160,1.6],['g',380,-200,1.4],['tr',-760,0,1.4],Lf(-80,110,{arm:'none',sw:1}),F('q',140,140,{flip:true,sz:60}),F('v',-250,170,{arm:'spear'})],[LB('những năm cuối đời')]);
// 110-111 ngã ba: hai con đường
R2('nga3',{tint:'#e3dcb8'},[['hl',-640,-300,2.3],['hl',640,-300,2.3],['tr',0,-250,1.8],Lf(0,120,{arm:'none',sw:1}),F('v',-200,160,{arm:'spear'}),F('v',220,160,{arm:'spear',flip:true})],[LB('hai nước cờ')]);
// 112-113 hậu cần, địa hình, thời điểm: kho lương, sông, đồi
R2('hauCan',{river:[-230,-140],road:[130,130],rw:60,tint:'#e3dcb8'},[['h',-600,-80,1.4],['h',-360,-100,1.3],['h',520,-90,1.4],['hl',100,-380,2.6],['b',-60,-185,{al:.9}],F('d',-480,120,{sack:true,w:1}),F('d',-300,150,{sack:true,w:1}),F('v',360,120,{arm:'spear'})],[],{mv:[['d',4,60,100,190,{sack:true}]]});
// 114-115 kết: bờ sông lúc bình minh, đoàn quân đứng sau
R2('songSang',{river:[-210,-100],tint:'#f0e0b8',top:.6},[['hl',-640,-380,2.8,'#9aa57a'],['hl',560,-390,2.6,'#97a97a'],['tp',-440,-250,1.2]].concat([-420,-300,-180,-60,320,440,560].map((u,i)=>F('v',u,70+(i%2)*26,{arm:'spear',sw:1}))).concat([Lf(110,170,{arm:'none',sw:1})]),[LB('một người, hai nước cờ')]);

//@@CC2-END
function genScene(t,it,a){
 setup(it);const def=SCN[it.scene];const tau=(t-(it.ts==null?it.t0:it.ts))*(it.sp||1)+(it.tau0||0);
 const zf=ease(cl((SC/SCf-.3)/.6)),al=a*zf;
 const GD=el('g',{opacity:a},dyn);mkGround(GD,tau,def.gnd);
 if(al<=.01)return;const D=el('g',{opacity:al},dyn);
 const L=[];const c={D,L,tau,t,it,arrows:[],push:(y,f)=>L.push({y,f})};
 for(const k in POS)delete POS[k];def.build(c);
 L.sort((x,y)=>x.y-y.y);for(const e of L)e.f();
 const AR=el('g',{},D);for(const [S0,T,p,fire] of c.arrows)arrow(AR,S0,T,p,110,fire,t);
 window.__lastTau=tau}
function genHUD(t,it,a){
 setup(it);const def=SCN[it.scene];const tau=(t-(it.ts==null?it.t0:it.ts))*(it.sp||1)+(it.tau0||0);const zf=ease(cl((SC/SCf-.8)/.2));if(zf<=.01||a<=.01)return;
 const g=el('g',{opacity:a*zf},hud);
 let i=0;for(const b of def.badges(it)||[]){const q=POS[b.key];if(!q)continue;
  const sv=hud;badge(t,tau,it,q[0],q[1],b.fh,b.kind||'v',b.name,b.sub,b.t0==null?1.5:b.t0,'cp'+(i++),b.below)}
 for(const b of def.burst||[]){const u=(tau-b.t)/1.5;if(u>0&&u<1){const p=Lc(b.u,b.v),[sx,sy]=toS(p[0],p[1]);burst(sx,sy-130*SC/SCf,u)}}}
window.CC=(t,it,a)=>(it.scene=='uc'?CCuc(t,it,a):it.scene=='nn'?CCnn(t,it,a):genScene(t,it,a));
window.CCH=(t,it,a)=>(it.scene=='uc'?CCHuc(t,it,a):it.scene=='nn'?CCHnn(t,it,a):genHUD(t,it,a));
})();
