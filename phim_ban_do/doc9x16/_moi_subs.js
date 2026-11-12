// ----- phụ đề cụm 2-3 chữ, từ khóa tô vàng
function chunks(txt,maxw=3){const parts=txt.match(/(?:[^,.;?]|(?<=\d)\.(?=\d))+[,.;?]?/g).map(s=>s.trim()).filter(Boolean);const out=[];parts.forEach(p=>{const w=p.split(/\s+/);const n=Math.ceil(w.length/maxw),k=Math.ceil(w.length/n);for(let i=0;i<w.length;i+=k)out.push(w.slice(i,i+k).join(' '))});const m=[];out.forEach(c=>{if(m.length&&c.split(/\s+/).length<2&&m[m.length-1].split(/\s+/).length<4)m[m.length-1]+=' '+c;else m.push(c)});return m}
const CH=[];const nw=x=>x.toLowerCase().replace(/[^\p{L}\p{N}]/gu,'');
SCRIPT.forEach(b=>{const cs=chunks(b.text);const ws=cs.map(c=>c.split(/\s+/).length),tot=ws.reduce((a,b)=>a+b,0);const span=DUR[b.n]-GAP;
 const A=(window.ASRW&&ASRW[b.n])||[],sp=((window.SPOK&&SPOK[b.n])||'').split(/\s+/).filter(Boolean),dp=b.text.split(/\s+/);let st=null;
 if(A.length>=2&&sp.length){const map=[];let k=0;dp.forEach((w,i)=>{map.push(k);if(/\d/.test(w)){let n=1;while(k+n<sp.length&&i+1<dp.length&&nw(sp[k+n])!==nw(dp[i+1])&&n<8)n++;k+=n}else k++});
  st=[];let di=0;cs.forEach((c,i)=>{const kk=map[Math.min(di,map.length-1)];st.push(A[Math.min(A.length-1,Math.round(kk/Math.max(1,sp.length)*A.length))]);di+=ws[i]})}
 let p=0;let t=TS[b.n]+.1;cs.forEach((c,i)=>{let a,e;if(st){a=TS[b.n]+Math.max(0,st[i]-.05);e=i+1<cs.length?TS[b.n]+Math.max(0,st[i+1]-.05):TS[b.n]+span-.02}else{const d=span*ws[i]/tot;a=t;e=t+d;t+=d}
  const hl=c.split(' ').map(w=>{const ix=b.text.indexOf(w,p);if(ix>=0)p=ix+w.length;const pre=ix>0?b.text.slice(Math.max(0,ix-2),ix):'';return /\d/.test(w)||(/^\p{Lu}/u.test(w)&&ix>0&&!/[.?!] $/.test(pre))});
  CH.push({a,b:e,txt:c,hl})})});CH.forEach((c,i)=>{if(i+1<CH.length&&CH[i+1].a>c.b)c.b=CH[i+1].a});
const cv=document.createElement('canvas').getContext('2d');cv.font='900 68px Inter';
function wrap(txt,mw){const w=txt.split(/\s+/),L=[];let cur='';w.forEach(x=>{const t=(cur+' '+x).trim();if(cv.measureText(t).width<=mw)cur=t;else{L.push(cur);cur=x}});L.push(cur);return L}
const SUBG=el(S,'g',{});
CH.forEach(c=>{const L=wrap(c.txt,900);const g=el(SUBG,'g',{opacity:0});let y=1400-(L.length-1)*44;let wi=0;L.forEach(l=>{const ws=l.split(' ');const tw=cv.measureText(l).width;let x=540-tw/2;
 ws.forEach((w,i)=>{const ww=cv.measureText(w).width,hl=c.hl[wi++];if(hl){el(g,'rect',{x:x-12,y:y-80,width:ww+24,height:104,rx:16,fill:'#e0b84a',stroke:'#17110b','stroke-width':5,transform:`rotate(-1.5 ${x+ww/2} ${y})`})}
  const t=el(g,'text',{x,y,'font-size':68,'text-anchor':'start',fill:hl?'#17110b':'#fff',stroke:hl?'none':'#0c0a08','stroke-width':16});t.textContent=w;x+=ww+cv.measureText(' ').width});y+=92});c.g=g;c.cy=1400});
