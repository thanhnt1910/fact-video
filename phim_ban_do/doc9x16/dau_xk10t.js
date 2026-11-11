// ===== Mona Lisa (xk10t). Ảnh: ml1(1) ml2(2) ml3(3) ml5(5) ml7(7) ml10(10) ml11(11) ml12(12) ml13(13). Cảnh 4,6,8,9,14 vẽ phẳng.
// ===== Dấu ấn riêng: nền nhung đỏ thẫm bảo tàng + khung vàng; bốn móc treo tranh trống ở đáy (y>1640), một sợi dây đung đưa
{DR1.setAttribute('opacity',0);DR2.setAttribute('opacity',0);
 DARKG.firstChild.setAttribute('fill','#1c0e12');
 [...PAPG.children].forEach(c=>{if(c.tagName=='g')c.setAttribute('opacity',0);if(c.tagName=='line')c.setAttribute('stroke','rgba(120,70,40,.14)')});
 PAPG.firstChild.setAttribute('fill','#e8dcc2');
 const hk=(p,col,cord)=>{const g=el(p,'g',{});const cs=[];[150,390,690,930].forEach((x,i)=>{el(g,'circle',{cx:x,cy:1650,r:9,fill:col});const c=el(g,'path',{d:`M${x} 1650 L${x} 1720`,stroke:cord,'stroke-width':4,'stroke-linecap':'round'});cs.push([c,x]);el(g,'rect',{x:x-34,y:1720,width:68,height:8,rx:3,fill:col})});return cs};
 const a=hk(DARKG,'#c9962f','#7a5a2a'),b=hk(PAPG,'#a8741a','#6b4a1a');
 for(const [p,col] of [[DARKG,'rgba(201,150,47,.07)'],[PAPG,'rgba(168,116,26,.08)']]){const g=el(p,'g',{});for(let i=0;i<4;i++)el(g,'rect',{x:30+i*3,y:30+i*3,width:1020-i*6,height:1860-i*6,rx:10,fill:'none',stroke:col,'stroke-width':6})}
 window.THEME_UPD=t=>{[a,b].forEach(cs=>cs.forEach(([c,x],i)=>{const s=Math.sin(t*1.3+i*1.7)*(i==2?9:2.5);c.setAttribute('d',`M${x} 1650 L${x+s} 1720`)}));PTU(t)};
}
// ===== Người que cầm đèn dầu (linh vật thử nghiệm): vài lần xuất hiện, không che chữ
const MAS=(g)=>{const k=el(g,'g',{});const ln=(d,w,c)=>{el(k,'path',{d,stroke:'#fff','stroke-width':w+10,'stroke-linecap':'round','stroke-linejoin':'round',fill:'none'});el(k,'path',{d,stroke:c,'stroke-width':w,'stroke-linecap':'round','stroke-linejoin':'round',fill:'none'})};
 ln('M0 -90 L0 -10',12,'#17120c');ln('M0 -10 L-26 70 M0 -10 L26 70',12,'#17120c');ln('M0 -78 L-34 -30',12,'#17120c');ln('M0 -78 L56 -56',12,'#17120c');
 const lg=el(k,'g',{transform:'translate(60,-52)'});const gl=el(lg,'circle',{r:84,fill:'rgba(255,205,90,.30)'});const gl2=el(lg,'circle',{r:48,fill:'rgba(255,215,110,.40)'});
 el(lg,'path',{d:'M0 -6 L0 -26',stroke:'#17120c','stroke-width':5});el(lg,'path',{d:'M-18 8 Q0 24 18 8 Z',fill:'#b07a2a',stroke:'#17120c','stroke-width':5,'stroke-linejoin':'round'});const fl=el(lg,'path',{d:'M0 -4 Q-9 -14 0 -30 Q9 -14 0 -4Z',fill:'#ffd25a',stroke:'#e8892a','stroke-width':3});
 el(k,'circle',{cx:0,cy:-118,r:33,fill:'#fff'});el(k,'circle',{cx:0,cy:-118,r:26,fill:'#f5efe0',stroke:'#17120c','stroke-width':7});el(k,'circle',{cx:-9,cy:-122,r:3.5,fill:'#17120c'});el(k,'circle',{cx:9,cy:-122,r:3.5,fill:'#17120c'});el(k,'path',{d:'M-8 -108 Q0 -101 8 -108',stroke:'#17120c','stroke-width':3.5,fill:'none','stroke-linecap':'round'});
 return{k,at:(x,y,s=1,rot=0,op=1,t=0,fx=1)=>{k.setAttribute('transform',`translate(${x},${y}) rotate(${rot+Math.sin(t*2.4)*2}) scale(${s*fx},${s})`);k.setAttribute('opacity',op);const f=1+.12*Math.sin(t*11);gl.setAttribute('r',84*f);gl2.setAttribute('r',48*f);fl.setAttribute('transform',`scale(${1+.15*Math.sin(t*13)},${1+.2*Math.sin(t*9)})`)}}};
// ===== Lật trang sách mở đầu (khoảng 1 giây), phủ trên cùng, chữ gợi hook hiện ngay phía sau
const PTG=el(S,'g',{opacity:0}),PTB=el(PTG,'g',{});
el(PTB,'rect',{x:-100,y:-10,width:1280,height:1940,fill:'#efe6cf'});el(PTB,'rect',{x:50,y:60,width:980,height:1800,rx:14,fill:'none',stroke:'#a8741a','stroke-width':8});
for(let i=0;i<9;i++)el(PTB,'line',{x1:150,y1:1250+i*54,x2:930-((i*97)%210),y2:1250+i*54,stroke:'rgba(60,50,40,.28)','stroke-width':5,'stroke-linecap':'round'});
{const a=T(PTB,540,700,'BÍ MẬT BIỂU TƯỢNG',92,'#17120c',0,'middle','none');a.setAttribute('font-weight',900);a.setAttribute('stroke','none');const b=T(PTB,540,860,'MONA LISA',120,'#a8741a',0,'middle','none');b.setAttribute('font-weight',900);b.setAttribute('stroke','none');
 const m=el(PTB,'g',{transform:'translate(540,1090) scale(1.7)'});el(m,'path',{d:'M-18 8 Q0 24 18 8 Z',fill:'#b07a2a',stroke:'#17120c','stroke-width':5});el(m,'path',{d:'M0 -4 Q-9 -14 0 -30 Q9 -14 0 -4Z',fill:'#ffd25a',stroke:'#e8892a','stroke-width':3})}
const PTS=el(PTG,'rect',{x:1080,y:0,width:60,height:1920,fill:'rgba(0,0,0,.35)'});let PTA=false;
const PTU=t=>{if(!PTA){S.appendChild(PTG);PTA=true}const u=cl((t-.55)/.65);if(t>1.3||t<0){PTG.setAttribute('opacity',0);return}PTG.setAttribute('opacity',1);const sx_=1-ease(u);PTB.setAttribute('transform',`scale(${Math.max(.001,sx_).toFixed(3)},1)`);PTS.setAttribute('x',(1080*sx_).toFixed(1));PTS.setAttribute('opacity',u>0&&u<1?.6:0)};
