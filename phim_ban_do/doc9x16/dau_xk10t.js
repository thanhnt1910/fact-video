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
 ln('M0 -90 L0 -10',12,'#17120c');ln('M0 -10 L-26 70 M0 -10 L26 70',12,'#17120c');ln('M0 -78 L-34 -30',12,'#17120c');ln('M0 -78 L58 -66',12,'#17120c');
 const lg=el(k,'g',{transform:'translate(60,-6)'});const gl=el(lg,'circle',{cy:-4,r:84,fill:'rgba(255,205,90,.28)'});const gl2=el(lg,'circle',{cy:-4,r:48,fill:'rgba(255,215,110,.38)'});
 const GD='#d9a84a',GS='#8a5e1a';el(lg,'path',{d:'M-3 -50 L-3 -62',stroke:'#fff','stroke-width':0});el(lg,'circle',{cx:0,cy:-56,r:9,fill:'none',stroke:'#fff','stroke-width':9});el(lg,'circle',{cx:0,cy:-56,r:9,fill:'none',stroke:GD,'stroke-width':4.5});
 el(lg,'path',{d:'M-20 -34 L-11 -48 L11 -48 L20 -34 Z',fill:GD,stroke:'#17120c','stroke-width':3.5,'stroke-linejoin':'round'});el(lg,'rect',{x:-22,y:-36,width:44,height:7,rx:2,fill:GD,stroke:'#17120c','stroke-width':3.5});
 el(lg,'rect',{x:-14,y:-29,width:28,height:56,fill:'#f2a23a',stroke:'#17120c','stroke-width':3.5});el(lg,'rect',{x:-9,y:-24,width:18,height:46,fill:'#ffcb6b'});el(lg,'path',{d:'M-14 -29 L-14 27 M14 -29 L14 27',stroke:GD,'stroke-width':5});
 const fl=el(lg,'path',{d:'M0 14 Q-9 2 0 -16 Q9 2 0 14Z',fill:'#fff2b8',stroke:'#e8892a','stroke-width':2.5});el(lg,'rect',{x:-1.5,y:12,width:3,height:10,fill:'#17120c'});
 el(lg,'rect',{x:-22,y:26,width:44,height:7,rx:2,fill:GD,stroke:'#17120c','stroke-width':3.5});el(lg,'path',{d:'M-16 33 L-12 40 L12 40 L16 33 Z',fill:GD,stroke:'#17120c','stroke-width':3.5,'stroke-linejoin':'round'});
 el(k,'circle',{cx:0,cy:-118,r:33,fill:'#fff'});el(k,'circle',{cx:0,cy:-118,r:26,fill:'#f5efe0',stroke:'#17120c','stroke-width':7});el(k,'circle',{cx:-9,cy:-122,r:3.5,fill:'#17120c'});el(k,'circle',{cx:9,cy:-122,r:3.5,fill:'#17120c'});el(k,'path',{d:'M-5 -106 Q0 -102 5 -106',stroke:'#17120c','stroke-width':3.5,fill:'none','stroke-linecap':'round'});
 el(k,'path',{d:'M-24 -112 Q-22 -86 0 -84 Q22 -86 24 -112 Q14 -98 0 -98 Q-14 -98 -24 -112Z',fill:'#d8d2c4',stroke:'#17120c','stroke-width':3.5,'stroke-linejoin':'round'});
 el(k,'circle',{cx:-10,cy:-122,r:9.5,fill:'rgba(255,255,255,.25)',stroke:'#17120c','stroke-width':3.5});el(k,'circle',{cx:10,cy:-122,r:9.5,fill:'rgba(255,255,255,.25)',stroke:'#17120c','stroke-width':3.5});el(k,'path',{d:'M-0.5 -122 L0.5 -122 M-19.5 -122 L-27 -126 M19.5 -122 L27 -126',stroke:'#17120c','stroke-width':3.5});
 el(k,'path',{d:'M-27 -134 Q0 -160 27 -134 Z',fill:'#6b4a2a',stroke:'#17120c','stroke-width':3.5,'stroke-linejoin':'round'});el(k,'rect',{x:-28,y:-136,width:56,height:7,rx:3,fill:'#4a321c',stroke:'#17120c','stroke-width':3});
 const sc=el(k,'g',{transform:'translate(-34,-30) rotate(-20)'});el(sc,'rect',{x:-8,y:-20,width:16,height:40,rx:7,fill:'#f2e6c4',stroke:'#17120c','stroke-width':4});el(sc,'path',{d:'M-4 -10 L4 -10 M-4 0 L4 0 M-4 10 L4 10',stroke:'#8a5e1a','stroke-width':2.5});
 return{k,at:(x,y,s=1,rot=0,op=1,t=0,fx=1)=>{k.setAttribute('transform',`translate(${x},${y}) rotate(${rot+Math.sin(t*2.4)*2}) scale(${s*fx},${s})`);k.setAttribute('opacity',op);const f=1+.12*Math.sin(t*11);gl.setAttribute('r',84*f);gl2.setAttribute('r',48*f);fl.setAttribute('transform',`translate(0,14) scale(${1+.12*Math.sin(t*13)},${1+.15*Math.sin(t*9)}) translate(0,-14)`)}}};
// ===== Lật trang sách mở đầu (khoảng 1 giây), phủ trên cùng, chữ gợi hook hiện ngay phía sau
const PTG=el(S,'g',{opacity:0}),PTB=el(PTG,'g',{});
el(PTB,'rect',{x:-100,y:-10,width:1280,height:1940,fill:'#efe6cf'});el(PTB,'rect',{x:50,y:60,width:980,height:1800,rx:14,fill:'none',stroke:'#a8741a','stroke-width':8});
for(let i=0;i<9;i++)el(PTB,'line',{x1:150,y1:1250+i*54,x2:930-((i*97)%210),y2:1250+i*54,stroke:'rgba(60,50,40,.28)','stroke-width':5,'stroke-linecap':'round'});
{const a=T(PTB,540,700,'BÍ MẬT BIỂU TƯỢNG',92,'#17120c',0,'middle','none');a.setAttribute('font-weight',900);a.setAttribute('stroke','none');const b=T(PTB,540,860,'MONA LISA',120,'#a8741a',0,'middle','none');b.setAttribute('font-weight',900);b.setAttribute('stroke','none');
 const m=el(PTB,'g',{transform:'translate(540,1120) scale(2.2)'});el(m,'circle',{cy:-56,r:9,fill:'none',stroke:'#d9a84a','stroke-width':4.5});el(m,'path',{d:'M-20 -34 L-11 -48 L11 -48 L20 -34 Z',fill:'#d9a84a',stroke:'#17120c','stroke-width':3.5});el(m,'rect',{x:-14,y:-29,width:28,height:56,fill:'#f2a23a',stroke:'#17120c','stroke-width':3.5});el(m,'rect',{x:-9,y:-24,width:18,height:46,fill:'#ffcb6b'});el(m,'path',{d:'M0 14 Q-9 2 0 -16 Q9 2 0 14Z',fill:'#fff2b8',stroke:'#e8892a','stroke-width':2.5});el(m,'rect',{x:-22,y:26,width:44,height:7,rx:2,fill:'#d9a84a',stroke:'#17120c','stroke-width':3.5})}
const PTS=el(PTG,'rect',{x:1080,y:0,width:60,height:1920,fill:'rgba(0,0,0,.35)'});let PTA=false;
const PTU=t=>{if(!PTA){S.appendChild(PTG);PTA=true}const u=cl((t-.55)/.65);if(t>1.3||t<0){PTG.setAttribute('opacity',0);return}PTG.setAttribute('opacity',1);const sx_=1-ease(u);PTB.setAttribute('transform',`scale(${Math.max(.001,sx_).toFixed(3)},1)`);PTS.setAttribute('x',(1080*sx_).toFixed(1));PTS.setAttribute('opacity',u>0&&u<1?.6:0)};
