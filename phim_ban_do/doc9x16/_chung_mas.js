// ===== Người que cầm đèn dầu (linh vật thử nghiệm): vài lần xuất hiện, không che chữ
const MAS=(g)=>{const k=el(g,'g',{});const OL='#17120c',GD='#d9a84a';
 const lim=(w)=>{const a=el(k,'path',{d:'M0 0',stroke:'#fff','stroke-width':w+10,'stroke-linecap':'round','stroke-linejoin':'round',fill:'none'});const b=el(k,'path',{d:'M0 0',stroke:OL,'stroke-width':w,'stroke-linecap':'round','stroke-linejoin':'round',fill:'none'});return d=>{a.setAttribute('d',d);b.setAttribute('d',d)}};
 const body=lim(12),legs=lim(12),arm1=lim(12),arm2=lim(12);
 const lg=el(k,'g',{});const gl=el(lg,'circle',{cy:0,r:84,fill:'rgba(255,205,90,.28)'});const gl2=el(lg,'circle',{cy:0,r:48,fill:'rgba(255,215,110,.38)'});
 el(lg,'circle',{cx:0,cy:-56,r:9,fill:'none',stroke:'#fff','stroke-width':9});el(lg,'circle',{cx:0,cy:-56,r:9,fill:'none',stroke:GD,'stroke-width':4.5});
 el(lg,'path',{d:'M-20 -34 L-11 -48 L11 -48 L20 -34 Z',fill:GD,stroke:OL,'stroke-width':3.5,'stroke-linejoin':'round'});el(lg,'rect',{x:-22,y:-36,width:44,height:7,rx:2,fill:GD,stroke:OL,'stroke-width':3.5});
 el(lg,'rect',{x:-14,y:-29,width:28,height:56,fill:'#f2a23a',stroke:OL,'stroke-width':3.5});el(lg,'rect',{x:-9,y:-24,width:18,height:46,fill:'#ffcb6b'});el(lg,'path',{d:'M-14 -29 L-14 27 M14 -29 L14 27',stroke:GD,'stroke-width':5});
 const fl=el(lg,'path',{d:'M0 14 Q-9 2 0 -16 Q9 2 0 14Z',fill:'#fff2b8',stroke:'#e8892a','stroke-width':2.5});el(lg,'rect',{x:-1.5,y:12,width:3,height:10,fill:OL});
 el(lg,'rect',{x:-22,y:26,width:44,height:7,rx:2,fill:GD,stroke:OL,'stroke-width':3.5});
 const hd=el(k,'g',{});
 el(hd,'circle',{cx:0,cy:-118,r:36,fill:'#fff'});el(hd,'circle',{cx:0,cy:-118,r:30,fill:'#f5efe0',stroke:OL,'stroke-width':7});
 el(hd,'circle',{cx:-10,cy:-114,r:4.5,fill:OL});el(hd,'circle',{cx:10,cy:-114,r:4.5,fill:OL});el(hd,'path',{d:'M-9 -98 Q0 -90 9 -98',stroke:OL,'stroke-width':4.5,fill:'none','stroke-linecap':'round'});
 el(hd,'path',{d:'M-42 -140 L42 -140 L36 -162 Q0 -182 -36 -162Z',fill:'#6b4a2a',stroke:OL,'stroke-width':5,'stroke-linejoin':'round'});
 return{k,at:(x,y,s=1,rot=0,op=1,t=0,fx=1,walk=1)=>{k.setAttribute('transform',`translate(${x},${y}) rotate(${rot}) scale(${s*fx},${s})`);k.setAttribute('opacity',op);
  const w=Math.sin(t*6.5)*walk,bob=Math.abs(Math.cos(t*6.5))*4*walk,sw=Math.sin(t*6.5+Math.PI)*walk;
  body(`M0 ${-84-bob} L0 ${-10-bob}`);legs(`M0 ${-10-bob} L${-26*w-2} 70 M0 ${-10-bob} L${26*w+2} 70`);
  arm1(`M0 ${-70-bob} L${-30-14*sw} ${-20-bob}`);arm2(`M0 ${-70-bob} L58 ${-50-bob}`);
  hd.setAttribute('transform',`translate(0,${-bob})`);lg.setAttribute('transform',`translate(66,${-6-bob})`);
  const f=1+.12*Math.sin(t*11);gl.setAttribute('r',84*f);gl2.setAttribute('r',48*f);
  fl.setAttribute('transform',`translate(0,14) scale(${1+.12*Math.sin(t*13)},${1+.15*Math.sin(t*9)}) translate(0,-14)`)}}};
// ===== Lật trang sách mở đầu (khoảng 1 giây), phủ trên cùng, chữ gợi hook hiện ngay phía sau
const PTG=el(S,'g',{opacity:0}),PTB=el(PTG,'g',{});
el(PTB,'rect',{x:-100,y:-10,width:1280,height:1940,fill:'#efe6cf'});el(PTB,'rect',{x:50,y:60,width:980,height:1800,rx:14,fill:'none',stroke:'#a8741a','stroke-width':8});
for(let i=0;i<9;i++)el(PTB,'line',{x1:150,y1:1250+i*54,x2:930-((i*97)%210),y2:1250+i*54,stroke:'rgba(60,50,40,.28)','stroke-width':5,'stroke-linecap':'round'});
{const a=T(PTB,540,700,'BÍ MẬT BIỂU TƯỢNG',92,'#17120c',0,'middle','none');a.setAttribute('font-weight',900);a.setAttribute('stroke','none');const b=T(PTB,540,860,VT2,120,'#a8741a',0,'middle','none');b.setAttribute('font-weight',900);b.setAttribute('stroke','none');
 const m=el(PTB,'g',{transform:'translate(540,1120) scale(0.001)'});el(m,'circle',{cy:-56,r:9,fill:'none',stroke:'#d9a84a','stroke-width':4.5});el(m,'path',{d:'M-20 -34 L-11 -48 L11 -48 L20 -34 Z',fill:'#d9a84a',stroke:'#17120c','stroke-width':3.5});el(m,'rect',{x:-14,y:-29,width:28,height:56,fill:'#f2a23a',stroke:'#17120c','stroke-width':3.5});el(m,'rect',{x:-9,y:-24,width:18,height:46,fill:'#ffcb6b'});el(m,'path',{d:'M0 14 Q-9 2 0 -16 Q9 2 0 14Z',fill:'#fff2b8',stroke:'#e8892a','stroke-width':2.5});el(m,'rect',{x:-22,y:26,width:44,height:7,rx:2,fill:'#d9a84a',stroke:'#17120c','stroke-width':3.5})}
el(PTB,'image',{href:'../../assets/logo/nguoi-gac-su.png',x:872,y:100,width:128,height:128,opacity:.9});
const PM=MAS(PTB);
const LC=el(PTB,'clipPath',{id:'plens'}),LCc=el(LC,'circle',{r:150,cx:300,cy:700});
const LG=el(PTB,'g',{'clip-path':'url(#plens)'}),LIN=el(LG,'g',{});
el(LIN,'rect',{x:-100,y:300,width:1280,height:900,fill:'#efe6cf'});
{const a=T(LIN,540,700,'BÍ MẬT BIỂU TƯỢNG',92,'#17120c',0,'middle','none');a.setAttribute('font-weight',900);a.setAttribute('stroke','none');const b=T(LIN,540,860,VT2,120,'#a8741a',0,'middle','none');b.setAttribute('font-weight',900);b.setAttribute('stroke','none')}
const LR=el(PTB,'g',{});el(LR,'circle',{r:150,fill:'rgba(255,255,255,.12)',stroke:'#17120c','stroke-width':16});el(LR,'circle',{r:150,fill:'none',stroke:'#d9a84a','stroke-width':8});el(LR,'path',{d:'M-100 -100 Q-60 -130 -10 -125',stroke:'rgba(255,255,255,.7)','stroke-width':10,fill:'none','stroke-linecap':'round'});
const LH=el(LR,'path',{d:'M106 106 L250 250',stroke:'#17120c','stroke-width':34,'stroke-linecap':'round'});el(LR,'path',{d:'M106 106 L250 250',stroke:'#6b4a2a','stroke-width':20,'stroke-linecap':'round'});
const PMU=t=>{const wx=Math.min(1,Math.max(0,t/.9)),x=-140+wx*400,walk=wx<1?1:0;PM.at(x,1190,1.7,0,1,t,1,walk);
 const p=(t-.45)/1.2,pp=Math.min(1,Math.max(0,p));let lx,ly,zz;if(p<0){lx=1300;ly=1000;zz=1}else{if(pp<.45){const q=pp/.45;lx=230+q*620;ly=700}else{const q=(pp-.45)/.55;lx=850-q*600;ly=860}zz=1.9}
 LCc.setAttribute('cx',lx);LCc.setAttribute('cy',ly);LIN.setAttribute('transform',`translate(${lx} ${ly}) scale(${zz}) translate(${-lx} ${-ly})`);LR.setAttribute('transform',`translate(${lx},${ly})`);
 const on=p>=-.2&&p<=1.05?1:0;LG.setAttribute('opacity',on);LR.setAttribute('opacity',on)};
const PTS=el(PTG,'rect',{x:1080,y:0,width:60,height:1920,fill:'rgba(0,0,0,.35)'});let PTA=false;
const PTU=t=>{if(!PTA){S.appendChild(PTG);PTA=true}PMU(t);const u=cl((t-1.7)/.55);if(t>2.4||t<0){PTG.setAttribute('opacity',0);return}PTG.setAttribute('opacity',1);const sx_=1-ease(u);PTB.setAttribute('transform',`scale(${Math.max(.001,sx_).toFixed(3)},1)`);PTS.setAttribute('x',(1080*sx_).toFixed(1));PTS.setAttribute('opacity',u>0&&u<1?.6:0)};
