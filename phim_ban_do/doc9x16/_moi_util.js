function calIcon(p,label,fs=26){const g=el(p,'g',{});const sh0=el(g,'g',{filter:'url(#sh)'});el(sh0,'path',{d:'M-48 54 L-48 -22 Q-48 -62 0 -62 Q48 -62 48 -22 L48 54Z',fill:'#6f6a60'});el(g,'path',{d:'M-48 54 L-48 -22 Q-48 -62 0 -62 Q48 -62 48 -22 L48 54Z',fill:'none',stroke:'#e0b84a','stroke-width':5});el(g,'path',{d:'M-36 46 L-36 -20 Q-36 -50 0 -50 Q36 -50 36 -20 L36 46Z',fill:'#8a857a'});const t=T(g,0,18,label,fs,'#f4e3a8',0,'middle','none');t.setAttribute('stroke','none');return{g,t}}
const CAL=calIcon(HUD,'',28);const CALG=CAL.g;
// ----- hình người phẳng, viền trắng
function fig(g,o={}){const k=el(g,'g',{});const f=o.fill||'#141312',sk=o.stroke||'#fff';
 const lim=(d,w=44)=>{el(k,'path',{d,stroke:sk,'stroke-width':w+12,'stroke-linecap':'round',fill:'none'});el(k,'path',{d,stroke:f,'stroke-width':w,'stroke-linecap':'round',fill:'none'})};
 if(o.arm)lim('M36 -214 L92 -306',30);
 if(o.tool){el(k,'path',{d:'M56 -150 L128 20',stroke:'#8a5a2a','stroke-width':12,'stroke-linecap':'round'});el(k,'path',{d:'M112 -2 L150 14 L132 46 L100 28Z',fill:'#9aa0a6',stroke:'#fff','stroke-width':4})}
 el(k,'path',{d:'M-46 -236 Q-46 -252 -30 -252 L30 -252 Q46 -252 46 -236 L46 -120 L34 -120 L34 0 L4 0 L4 -108 L-4 -108 L-4 0 L-34 0 L-34 -120 L-46 -120Z',fill:f,stroke:sk,'stroke-width':8,'stroke-linejoin':'round'});
 el(k,'circle',{cx:0,cy:-286,r:34,fill:f,stroke:sk,'stroke-width':8});
 if(o.hat)el(k,'path',{d:'M-38 -296 Q-36 -340 0 -342 Q36 -340 38 -296Z',fill:o.hat,stroke:sk,'stroke-width':6,'stroke-linejoin':'round'});
 return{k,at:(x,y,s=1,rot=0,op=1)=>{k.setAttribute('transform',`translate(${x},${y}) rotate(${rot}) scale(${s})`);k.setAttribute('opacity',op)}}}
function bubble(g,w,h,txt,size){const k=el(g,'g',{});const sh0=el(k,'g',{filter:'url(#sh)'});el(sh0,'rect',{x:-w/2,y:-h/2,width:w,height:h,rx:44,fill:'#fff'});el(sh0,'path',{d:`M-90 ${h/2-4} L-130 ${h/2+66} L-30 ${h/2-4}Z`,fill:'#fff'});
 const L=txt.split('|');L.forEach((l,i)=>{const t=T(k,0,-(L.length-1)*size*.55+i*size*1.1+size*.35,l,size,'#17120c',0,'middle','none');t.setAttribute('stroke','none')});
 return{k,at:(x,y,s=1,op=1)=>{k.setAttribute('transform',`translate(${x},${y}) scale(${s})`);k.setAttribute('opacity',op)}}}
function putAt(o,x,y,rot=0,sc=1,op=1){o.g.setAttribute('transform',`translate(${x},${y}) rotate(${rot}) scale(${sc})`);o.g.setAttribute('opacity',op)}

