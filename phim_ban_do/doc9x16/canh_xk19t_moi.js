// ===== Giấy (xk19t). Toàn bộ cảnh vẽ phẳng, không dùng ảnh tư liệu.
// ===== Dấu ấn riêng: nền giấy dó kem lộ sợi + lưới khung xeo mờ; nền tối màu mực; sợi giấy trôi chậm ở đáy khung (y>1600)
{DR1.setAttribute('opacity',0);DR2.setAttribute('opacity',0);
 DARKG.firstChild.setAttribute('fill','#1c1914');
 [...PAPG.children].forEach(c=>{if(c.tagName=='g')c.setAttribute('opacity',0);if(c.tagName=='line')c.setAttribute('stroke','rgba(0,0,0,0)')});
 PAPG.firstChild.setAttribute('fill','#efe4c6');
 const rr=rng(1919);
 const mesh=(p,col)=>{const g=el(p,'g',{});for(let x=60;x<1040;x+=13)el(g,'line',{x1:x,y1:20,x2:x,y2:1900,stroke:col,'stroke-width':1.6});for(let y=140;y<1900;y+=190)el(g,'line',{x1:20,y1:y,x2:1060,y2:y,stroke:col,'stroke-width':4})};
 mesh(DARKG,'rgba(214,180,110,.07)');mesh(PAPG,'rgba(120,85,40,.09)');
 {const g=el(PAPG,'g',{});for(let i=0;i<150;i++){const x=rr()*1040+20,y=rr()*1860+20,l=30+rr()*60;el(g,'path',{d:`M${x} ${y} q ${l*.4} ${-10+rr()*20} ${l} ${(rr()-.5)*18}`,fill:'none',stroke:'rgba(150,105,55,.2)','stroke-width':1.5+rr()*1.4,'stroke-linecap':'round'})}}
 const drift=(p,col)=>{const g=el(p,'g',{});const a=[];for(let i=0;i<18;i++){const e=el(g,'path',{d:'M0 0 q 22 -12 44 0 t 44 0',fill:'none',stroke:col,'stroke-width':4+rr()*3,'stroke-linecap':'round'});a.push({e,x:rr()*1300,y:1620+rr()*250,sp:14+rr()*26,ph:rr()*6})}return a};
 const dA=drift(DARKG,'rgba(214,190,130,.28)'),dB=drift(PAPG,'rgba(140,100,50,.32)');
 window.THEME_UPD=t=>{[dA,dB].forEach(L=>L.forEach(o=>{const x=((o.x+t*o.sp)%1300)-110;o.e.setAttribute('transform',`translate(${x.toFixed(1)},${(o.y+Math.sin(t*.9+o.ph)*9).toFixed(1)}) rotate(${(Math.sin(t*.7+o.ph)*8).toFixed(1)})`)}));PTU(t)};
}
