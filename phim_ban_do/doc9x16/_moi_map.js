function mapcard(mw,mh,seed){const g=mk();const id='cp'+(CID++);const o={g,w:mw,h:mh};
 const shg=el(g,'g',{filter:'url(#sh)'});el(shg,'polygon',{points:jag(mw+22,mh+22,seed+3,6),fill:'#eee7d3'});
 const cp=el(g,'clipPath',{id});el(cp,'polygon',{points:jag(mw,mh,seed,4)});
 const oc=el(g,'g',{'clip-path':`url(#${id})`});const im=el(oc,'image',{href:'map_relief.jpg',x:0,y:0,width:3542,height:4420});
 o.inner=el(oc,'g',{});o.top=el(g,'g',{});o.st={clon:108,clat:16,ppd:150};
 o.view=(clon,clat,ppd)=>{const s=ppd/239.4;o.st={clon,clat,ppd};im.setAttribute('transform',`translate(${-(clon-102)*239.4*s},${-(30.5-clat)*260*s}) scale(${s})`)};
 o.P=(lon,lat)=>[(lon-o.st.clon)*o.st.ppd,(o.st.clat-lat)*o.st.ppd*260/239.4];
 o.at=(x,y,rot=0,sc=1,op=1)=>{g.setAttribute('transform',`translate(${x},${y}) rotate(${rot}) scale(${sc})`);g.setAttribute('opacity',op)};
 return o}
const DN=[108.2,16.06];
function pin(p,x,y,u,col='#e5483f'){p.innerHTML='';if(u<=0)return;el(p,'circle',{cx:x,cy:y,r:16*u,fill:col,stroke:'#fff','stroke-width':5});for(let i=0;i<2;i++){const k=((performance.now?0:0)+i*.5);}}
function pulse(g,x,y,t,t0,col='#e5483f'){const u=cl((t-t0)/.4);g.innerHTML='';if(t<t0)return;el(g,'circle',{cx:x,cy:y,r:15*Math.min(1,u*1.4),fill:col,stroke:'#fff','stroke-width':5});[0,1].forEach(i=>{const w=(((t-t0)*.7)-i*.5);if(w<0)return;const m=w%1;el(g,'circle',{cx:x,cy:y,r:20+m*70,fill:'none',stroke:col,'stroke-width':5,opacity:(1-m)*.7})})}
// ----- bản đồ động: tàu, quân cờ, đường đi, chữ cái bay lên
function drawShip(g){el(g,'path',{d:'M-30 0 L30 0 L20 15 L-20 15Z',fill:'#5a3a1e',stroke:'#fff','stroke-width':3});el(g,'line',{x1:0,y1:0,x2:0,y2:-52,stroke:'#fff','stroke-width':4});el(g,'path',{d:'M3 -50 L3 -6 L32 -8Z',fill:'#f4ecd8',stroke:'#2a1a0c','stroke-width':2});el(g,'path',{d:'M-3 -44 L-3 -8 L-26 -10Z',fill:'#f4ecd8',stroke:'#2a1a0c','stroke-width':2})}
function drawPawn(g,col,lab,ly=-92){const k=el(g,'g',{transform:'scale(1.7)'});el(k,'circle',{cx:0,cy:-30,r:12,fill:col,stroke:'#fff','stroke-width':4});el(k,'path',{d:'M-15 0 Q-15 -19 0 -21 Q15 -19 15 0Z',fill:col,stroke:'#fff','stroke-width':4});if(lab)T(g,0,ly,lab,26,'#fff',8,'middle','#1b140c')}
function along(pts,u){const L=[0];for(let i=1;i<pts.length;i++)L.push(L[i-1]+Math.hypot(pts[i][0]-pts[i-1][0],pts[i][1]-pts[i-1][1]));const D=L[L.length-1]*cl(u);let i=1;while(i<pts.length-1&&L[i]<D)i++;const k=(D-L[i-1])/Math.max(1e-6,L[i]-L[i-1]);return[lerp(pts[i-1][0],pts[i][0],cl(k)),lerp(pts[i-1][1],pts[i][1],cl(k)),i,D]}
function trailPath(pts,u){const L=[0];for(let i=1;i<pts.length;i++)L.push(L[i-1]+Math.hypot(pts[i][0]-pts[i-1][0],pts[i][1]-pts[i-1][1]));const D=L[L.length-1]*cl(u);let d='M'+pts[0][0]+' '+pts[0][1];for(let i=1;i<pts.length;i++){if(L[i]<=D)d+=` L${pts[i][0]} ${pts[i][1]}`;else{const k=(D-L[i-1])/(L[i]-L[i-1]);d+=` L${lerp(pts[i-1][0],pts[i][0],k)} ${lerp(pts[i-1][1],pts[i][1],k)}`;break}}return d}
function hsMake(L){const hs=el(L,'g',{});const O=[[0,0],[16,-8],[30,6],[-14,10],[8,16],[-26,-4],[40,-12]];const hd=O.map(o=>el(hs,'circle',{cx:o[0],cy:o[1],r:5,fill:'#fff6d0',stroke:'#1b140c','stroke-width':2}));T(hs,-50,-56,'QUẦN ĐẢO HOÀNG SA',24,'#fff',7,'middle','#1b140c');T(hs,-50,-28,'(VIỆT NAM)',24,'#f2c14e',7,'middle','#1b140c');return(m,op)=>{const[x,y]=m.P(111.3,16.5);hs.setAttribute('transform',`translate(${x},${y})`);hs.setAttribute('opacity',op)}}
const PLACES=[['Huế',107.58,16.46,-1],['Đà Nẵng',108.2,16.05,-1],['Quảng Ngãi',108.8,15.12,-1],['Quy Nhơn',109.22,13.8,-1]];
