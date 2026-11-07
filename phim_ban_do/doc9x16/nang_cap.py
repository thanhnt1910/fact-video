"""Nâng cấp trang cũ lên phong cách mới: python nang_cap.py <số> -> trang_vn<số>m.html
Giữ nguyên cảnh và hàm trợ giúp của trang cũ; thay nền, HUD, phụ đề, kết xuất; thêm bia đá, boom tự động, rung khung."""
import re, sys
n = sys.argv[1]
L = open(f'trang_vn{n}.html', encoding='utf-8').read().split('\n')
bg = open('_moi_bg.js', encoding='utf-8').read(); util = open('_moi_util.js', encoding='utf-8').read(); subs = open('_moi_subs.js', encoding='utf-8').read(); tail = open('_moi_tail.js', encoding='utf-8').read()
hud = L[26].replace("const HUD=el(S,'g',{});", "const HUD=el(S,'g',{});", 1)   # tiêu đề + dòng ghi công của trang cũ
hud_all = '// ----- khung chung\n' + hud + '\n' + L[27] + '\n'
wr = '''const FIRST=new Map();function wrapAt(o,kind,red){if(!o||!o.at)return o;const f=o.at;o.at=function(x,y,rot,sc,op){if(window.__REC&&(op===undefined||op>.5)&&(sc===undefined||sc>.4)&&!FIRST.has(o))FIRST.set(o,{kind,red,t:window.__T});return f.apply(this,arguments)};return o}
const _cardO=card,_stripO=strip,_stampO=stamp;card=function(){return wrapAt(_cardO.apply(this,arguments),'card')};strip=function(txt,red){return wrapAt(_stripO.apply(this,arguments),'strip',red)};stamp=function(){return wrapAt(_stampO.apply(this,arguments),'stamp')};
const _sceneOld=scene;let SCI=0;scene=function(a,b,build){_sceneOld(a,b,build);SCN[SCN.length-1].bg=(SCI++%2)?'p':'d'};
function S2(n0,n1,bg,cal,build,endT){scene(R(n0)-.2,endT||E(n1),build);const s=SCN[SCN.length-1];s.bg=bg;s.cal=cal}
'''
render = '''let CLAST=null,CT0=0;
window.render=function(t){let shx=0,shy=0;HB.forEach(b=>{const u=(t-b)/.4;if(u>=0&&u<1){const k=Math.pow(1-u,2)*11;shx+=Math.sin(u*70)*k;shy+=Math.cos(u*53)*k*.7}});STG.setAttribute('transform',`translate(${shx.toFixed(1)},${shy.toFixed(1)})`);
 if(typeof BGP!=='undefined')BGP.forEach(o=>{if(t>=o.a&&t<=o.b+.05){const u=cl((t-o.a)/Math.max(.1,o.b-o.a));const z=1.1+.2*u;o.gi.setAttribute('transform',`translate(${o.cx},${o.cy}) scale(${z}) translate(${-o.cx-(u-.5)*60},${-o.cy})`)}});
 let cur=SCN[0],pv=null;SCN.forEach((s,i)=>{if(t>=s.a){cur=s;pv=i>0?SCN[i-1]:null}});
 const k=(pv&&pv.bg==cur.bg)?1:inn(t,cur.a,.3);PAPG.setAttribute('opacity',cur.bg=='p'?k:1-k);
 SCN.forEach((s,i)=>{const on=t>=s.a&&t<s.b+.01;s.g.setAttribute('display',on?'inline':'none');if(on){const out=i+1<SCN.length?cl((s.b-t)/.3):1;s.g.setAttribute('opacity',out);const e=inn(t,s.a,.35);s.g.setAttribute('transform',`translate(${(1-e)*90},0)`);s.upd(t)}});
 const lab=cur.cal?(typeof cur.cal=='function'?cur.cal(t):cur.cal):null;if(lab!==CLAST){CLAST=lab;CT0=t;if(lab){CAL.t.textContent=lab;CAL.t.setAttribute('font-size',lab.length>5?19:28)}}
 if(lab){const f=popv(t,CT0,.45);CALG.setAttribute('transform',`translate(815,100) scale(1,${Math.max(.01,f)})`);CALG.setAttribute('opacity',1)}else CALG.setAttribute('opacity',0);
 CH.forEach(c=>{const on=t>=c.a&&t<c.b;c.g.setAttribute('opacity',on?1:0);if(on){const s=.88+.12*back(cl((t-c.a)/.16));c.g.setAttribute('transform',`translate(540,${c.cy}) scale(${s}) translate(-540,${-c.cy})`)}})}
</script>'''
out = L[:19] + [bg + hud_all + util] + L[28:54] + [subs + wr] + L[65:]
s = '\n'.join(out)
# SUBP không còn
s = s.replace('S.appendChild(SUBP);S.appendChild(SUBG);', 'S.appendChild(SUBG);')
# bỏ tiếng tem cũ (thay bằng boom tự động)
def clean(m):
    stmts = m.group(0).split(';'); return ';'.join(x for x in stmts if "'stamp'" not in x)
s = re.sub(r"^sx\(.*$", clean, s, flags=re.M)
# chèn khối boom tự động trước window.SFX và gọi sau khi dựng
s = s.replace('window.SFX=SFXQ;', tail + 'window.SFX=SFXQ;', 1)
i = s.index('window.render=function'); s = s[:i] + render + '\n<script>window.__AUTO();</script>\n'
s = s.replace('let CLAST=null,CT0=0;', 'let CLAST=null,CT0=0;', 1)
s += ''
open(f'trang_vn{n}m.html', 'w', encoding='utf-8').write(s)
print('ok', len(s))
