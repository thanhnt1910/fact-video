const VT2='MONA LISA';
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