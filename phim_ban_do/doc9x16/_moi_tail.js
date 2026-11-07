// ----- boom tự động: lấy lần hiện đầu tiên của thẻ ảnh, tem, thẻ đỏ; cú mạnh làm khung rung
const HB=[];
window.__AUTO=()=>{window.__REC=1;for(let t=0;t<TOTAL;t+=.1){window.__T=t;window.render(t)}window.__REC=0;
 const L=[...FIRST.values()].filter(e=>e.t>.5).sort((a,b)=>a.t-b.t);const heavy=[];
 L.filter(e=>e.kind!='strip').forEach(e=>{if(heavy.length<12&&heavy.every(h=>Math.abs(h-e.t)>2.2))heavy.push(e.t)});
 const light=[];L.forEach(e=>{if(heavy.includes(e.t))return;if(e.kind=='strip'&&!e.red)return;if([...heavy,...light].every(h=>Math.abs(h-e.t)>.9)&&light.length<14)light.push(e.t)});
 heavy.forEach(t=>{sx(t+.05,'boom',{g:1});HB.push(t+.05)});light.forEach(t=>sx(t+.05,'boom',{light:true,g:.8}))};
