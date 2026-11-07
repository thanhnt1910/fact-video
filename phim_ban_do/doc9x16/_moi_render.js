let CLAST=null,CT0=0;
window.render=function(t){let cur=SCN[0],pv=null;SCN.forEach((s,i)=>{if(t>=s.a){cur=s;pv=i>0?SCN[i-1]:null}});
 const k=(pv&&pv.bg==cur.bg)?1:inn(t,cur.a,.3);PAPG.setAttribute('opacity',cur.bg=='p'?k:1-k);
 SCN.forEach((s,i)=>{const on=t>=s.a&&t<s.b+.01;s.g.setAttribute('display',on?'inline':'none');if(on){const out=i+1<SCN.length?cl((s.b-t)/.3):1;s.g.setAttribute('opacity',out);const e=inn(t,s.a,.35);s.g.setAttribute('transform',`translate(${(1-e)*90},0)`);s.upd(t)}});
 const lab=cur.cal?(typeof cur.cal=='function'?cur.cal(t):cur.cal):null;if(lab!==CLAST){CLAST=lab;CT0=t;if(lab)CAL.t.textContent=lab}
 if(lab){const f=popv(t,CT0,.45);CALG.setAttribute('transform',`translate(815,100) scale(1,${Math.max(.01,f)})`);CALG.setAttribute('opacity',1)}else CALG.setAttribute('opacity',0);
 CH.forEach(c=>{const on=t>=c.a&&t<c.b;c.g.setAttribute('opacity',on?1:0);if(on){const s=.88+.12*back(cl((t-c.a)/.16));c.g.setAttribute('transform',`translate(540,${c.cy}) scale(${s}) translate(-540,${-c.cy})`)}})}
</script>
