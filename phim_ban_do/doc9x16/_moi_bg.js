// ----- nền: giấy báo sáng (có dòng kẻ) và nền báo tối, đổi theo cảnh
const DARKG=el(S,'g',{});el(DARKG,'rect',{width:1080,height:1920,fill:'#17110b'});
function drum(p,x,y,R0,col,op){const g=el(p,'g',{transform:`translate(${x},${y})`,opacity:op});[1,.82,.64,.46,.3].forEach((k,i)=>el(g,'circle',{r:R0*k,fill:'none',stroke:col,'stroke-width':i%2?3:6,'stroke-dasharray':i==2?'10 14':'none'}));for(let i=0;i<16;i++){const an=i*Math.PI/8;el(g,'path',{d:`M${Math.cos(an)*R0*.5} ${Math.sin(an)*R0*.5} L${Math.cos(an+.1)*R0*.8} ${Math.sin(an+.1)*R0*.8} L${Math.cos(an-.1)*R0*.8} ${Math.sin(an-.1)*R0*.8}Z`,fill:col,opacity:.6})}el(g,'circle',{r:R0*.12,fill:col});return g}
const DR1=drum(DARKG,90,330,360,'#2a1f13',1),DR2=drum(DARKG,1000,1330,420,'#261b10',1);
{const r=rng(11);for(let i=0;i<60;i++)el(DARKG,'rect',{x:r()*1080,y:r()*1920,width:2,height:14+r()*30,fill:'#2b2015',opacity:.7,transform:`rotate(${r()*180} 0 0)`})}
const PAPG=el(S,'g',{opacity:0});el(PAPG,'rect',{width:1080,height:1920,fill:'#cdb98c'});
{const r=rng(5);for(let i=0;i<420;i++){const x=r()*1080,y=r()*1920,l=20+r()*70,an=r()*Math.PI;el(PAPG,'line',{x1:x,y1:y,x2:x+Math.cos(an)*l,y2:y+Math.sin(an)*l*.4,stroke:i%3?'rgba(120,95,55,.20)':'rgba(255,245,215,.28)','stroke-width':1.6+r()*1.6,'stroke-linecap':'round'})}
 const dp=drum(PAPG,990,300,300,'#a8905f',.35);el(PAPG,'rect',{width:1080,height:1920,fill:'url(#vg)',opacity:.6})}
const STG=el(S,'g',{});
