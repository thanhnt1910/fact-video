const VT2='TIỀN GIẤY';
// ===== Tiền giấy Hồ Quý Ly (xk13t). Ảnh: hq1(1) hq5(5) hq10(6). Cảnh 2,3,4,7,8,9,10,11 vẽ phẳng.
// ===== Dấu ấn riêng: nền giấy dó nâu vàng, vân gỗ khắc; một hàng con dấu đỏ triều đình lần lượt đóng xuống ở đáy (y>1600)
{DR1.setAttribute('opacity',0);DR2.setAttribute('opacity',0);
 DARKG.firstChild.setAttribute('fill','#241709');
 [...PAPG.children].forEach(c=>{if(c.tagName=='g')c.setAttribute('opacity',0);if(c.tagName=='line')c.setAttribute('stroke','rgba(120,80,30,.16)')});
 PAPG.firstChild.setAttribute('fill','#ead9ae');
 const sealRow=(p,col)=>{const g=el(p,'g',{});return [200,420,660,880].map((x,i)=>{const s=el(g,'g',{});el(s,'rect',{x:-34,y:-34,width:68,height:68,rx:6,fill:col,opacity:.92});el(s,'path',{d:'M-20 -8 L20 -8 M-20 8 L20 8 M0 -22 L0 22',stroke:'#fff',opacity:.8,'stroke-width':6,'stroke-linecap':'round'});return[s,x]})};
 const a=sealRow(DARKG,'#b3282a'),b=sealRow(PAPG,'#a32124');
 for(const [p,col] of [[DARKG,'rgba(214,160,60,.07)'],[PAPG,'rgba(120,80,30,.09)']]){const g=el(p,'g',{});for(let i=0;i<4;i++)el(g,'rect',{x:30+i*3,y:30+i*3,width:1020-i*6,height:1860-i*6,rx:10,fill:'none',stroke:col,'stroke-width':6})}
 window.THEME_UPD=t=>{[a,b].forEach(cs=>cs.forEach(([s,x],i)=>{const ph=((t*.45-i*.25)%1+1)%1;const k=ph<.18?1+(1-ph/.18)*.7:1;const op=ph<.05?ph/.05:1;s.setAttribute('transform',`translate(${x},1690) scale(${k}) rotate(${(i%2?3:-3)})`);s.setAttribute('opacity',op)}));PTU(t)};
}
