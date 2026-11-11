const VT2='D-DAY';
// ===== D-Day (xk14t). Ảnh: dd4(1) dd1(3) dd3(9) dd8(8) dd11(11) dd12(12). Cảnh 2,4,5,6,7,10 vẽ phẳng.
// ===== Dấu ấn riêng: nền bản đồ thời tiết xanh biển, vài đường đẳng áp trôi chậm ở đáy (y>1560)
{DR1.setAttribute('opacity',0);DR2.setAttribute('opacity',0);
 DARKG.firstChild.setAttribute('fill','#0e2230');
 [...PAPG.children].forEach(c=>{if(c.tagName=='g')c.setAttribute('opacity',0);if(c.tagName=='line')c.setAttribute('stroke','rgba(40,90,120,.13)')});
 PAPG.firstChild.setAttribute('fill','#dde8ec');
 const iso=(p,col)=>{const g=el(p,'g',{});return [[300,70,24],[420,110,32],[540,150,40],[660,190,48]].map(([rx,ry,sp],i)=>{const e=el(g,'ellipse',{rx,ry,fill:'none',stroke:col,'stroke-width':4,opacity:.55-i*.08});return[e,sp,i]})};
 const a=iso(DARKG,'rgba(130,190,225,.55)'),b=iso(PAPG,'rgba(60,110,140,.4)');
 for(const [p,col] of [[DARKG,'rgba(130,190,225,.08)'],[PAPG,'rgba(40,90,120,.1)']]){const g=el(p,'g',{});for(let i=0;i<4;i++)el(g,'rect',{x:30+i*3,y:30+i*3,width:1020-i*6,height:1860-i*6,rx:10,fill:'none',stroke:col,'stroke-width':6})}
 window.THEME_UPD=t=>{[a,b].forEach(cs=>cs.forEach(([e,sp,i])=>{e.setAttribute('cx',540+Math.sin(t*.22+i)*sp*2.2);e.setAttribute('cy',1740+Math.cos(t*.18+i*.7)*10)}));PTU(t)};
}
