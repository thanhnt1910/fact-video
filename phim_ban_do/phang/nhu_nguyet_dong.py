"""Cảnh chuyển động chi tiết: quân Tống vượt sông Như Nguyệt trên bè, bị chặn bởi hàng rào tre, cọc và tên lửa (minh họa).
python phim_ban_do/phang/nhu_nguyet_dong.py <từ_khung> <đến_khung> <thư_mục> | still <giây>..."""
import sys, pathlib, random
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import chitiet
from chitiet import *   # noqa
import flat
flat.DETAIL = True
from flat import sh
from nguoi_nghieng import side_fig
from playwright.sync_api import sync_playwright
ROOT = pathlib.Path(__file__).resolve().parents[2]
FPS, DUR = 24, 11.0
PAL_Y = 600   # chân hàng rào bờ nam
RIV_Y = 640   # mép nước


def palisade_detail():
    o = ''; r = random.Random(3)
    for i in range(-5, 62):
        x = i * 34 + r.randint(-3, 3); h = 150 + r.randint(-14, 16)
        c = ('#6f4c2a', '#7a5532', '#654526')[i % 3]
        o += f'<path d="M{x},{PAL_Y} L{x},{PAL_Y-h} L{x+14},{PAL_Y-h-26} L{x+28},{PAL_Y-h} L{x+28},{PAL_Y}Z" fill="{c}"/><line x1="{x+14}" y1="{PAL_Y-h-20}" x2="{x+14}" y2="{PAL_Y}" stroke="#3a2a18" stroke-width="1.6" opacity=".5"/>'
    o += f'<rect y="{PAL_Y-92}" width="1920" height="9" fill="#4a3320"/><rect y="{PAL_Y-40}" width="1920" height="9" fill="#4a3320"/>'
    return o


def build():
    L = outdoor('grey', sun=(300, 250), cl=5, mt=420, birds_=(1500, 160))
    far = ''.join(hut(x, 560, .5) for x in range(120, 1900, 380)) + ''.join(tree(x + 150, 560, .65, 'grey') for x in range(120, 1900, 380))
    L.append(G('farland', f'<rect y="440" width="1920" height="170" fill="#5d6650"/>{far}'))
    L.append(G('bam', ''.join(bamboo(x, 600, 1.35, 'grey', 6) for x in (140, 760, 1380, 1800))))
    # quân Đại Việt sau hàng rào
    vs = ''
    for i in range(14):
        x = 70 + i * 135 + (i % 3) * 18; s = .68
        col = ('#3a4a6a', '#41506e', '#34445f')[i % 3]
        f = side_fig(f'v{i}', x, PAL_Y - 86 * s - 40, s, col, hat='cone' if i % 3 else 'helmet', seed=80 + i, pants=sh(col, .6), armor='#4a4e58' if i % 2 else None, sash='#a8452f', flip=-1, shadow=False)
        vs += f.replace(f'class="sf" id="v{i}"', f'class="sf vsold" id="v{i}" data-i="{i}" data-x="{x}"')
    L.append(G('vsoldiers', vs))
    L.append(G('banners', ''.join(pennant(x, 330, PAL_Y - 150, '#8a3a2a', 130) for x in (330, 980, 1620))))
    L.append(G('palisade', palisade_detail()))
    # bờ nam + nước
    L.append(f'<rect y="{PAL_Y}" width="1920" height="{RIV_Y-PAL_Y+14}" fill="#6a5a3e"/>')
    L.append('<defs><linearGradient id="rvg2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7d9aa6"/><stop offset="1" stop-color="#3c5766"/></linearGradient></defs>')
    L.append(f'<rect y="{RIV_Y}" width="1920" height="{1080-RIV_Y}" fill="url(#rvg2)"/>')
    L.append('<g id="rip"></g>')
    # cọc dưới sông: nhô lên khỏi mặt nước, nghiêng
    st = ''; r = random.Random(9)
    for i in range(30):
        x = 40 + i * 64 + r.randint(-14, 14); y = RIV_Y + 14 + (i % 3) * 22 + r.randint(0, 8); a = r.randint(-9, 9); h = 96 + r.randint(0, 40)
        st += f'<g transform="translate({x},{y}) rotate({a})"><path d="M-8,0 L-8,{-h} L0,{-h-24} L8,{-h} L8,0Z" fill="#5a3b1c"/><rect x="-8" y="{-h}" width="16" height="6" fill="#3a2410"/></g><ellipse class="swash" data-k="{i}" cx="{x}" cy="{y+3}" rx="18" ry="4" fill="#e8f4fa" opacity=".5"/>'
    L.append(G('stakes', st))
    # bè và quân Tống
    rafts = ''
    for k in range(3):
        planks = ''.join(f'<rect x="{-190+j*38}" y="-12" width="34" height="24" rx="4" fill="{("#8a6a40","#7a5a34")[j%2]}" stroke="#3a2812" stroke-width="2"/>' for j in range(10))
        logs = ''.join(f'<ellipse cx="{-196+j*0}" cy="{-2+j*9}" rx="9" ry="6" fill="#a98a5a" stroke="#3a2812" stroke-width="2"/>' for j in range(2))
        men = ''
        for m in range(3):
            col = ('#4a5a6e', '#566070', '#3c4a60')[(k + m) % 3]
            men += side_fig(f'r{k}{m}', -110 + m * 100, -86 * 1.0 - 4, 1.0, col, hat='song' if m == 1 else 'helmet', seed=100 + k * 3 + m, pants=sh(col, .6), armor='#3a3e48', sash='#2e4a80', flip=-1, shadow=False).replace(f'class="sf" id="r{k}{m}"', f'class="sf rman" id="r{k}{m}" data-k="{k}" data-m="{m}"')
        rafts += f'<g class="raft" id="raft{k}"><ellipse cx="0" cy="22" rx="210" ry="14" fill="#1c2c36" opacity=".35"/>{men}{planks}{logs}<path d="M-190,12 L190,12 L180,34 L-180,34Z" fill="#5a3b1c"/><g class="rfire" id="rfire{k}"></g></g>'
    L.append(G('rafts', rafts))
    L.append('<g id="arrows"></g><g id="smokeg"></g>')
    L.append('<rect width="1920" height="1080" fill="url(#vg)"/>')
    return svg(L, 'grey')


JS = r"""
(cfg) => {
  const NS='http://www.w3.org/2000/svg', svg=document.documentElement;
  const Q=s=>[...document.querySelectorAll(s)], $=s=>document.querySelector(s);
  const el=(n,a,p)=>{const e=document.createElementNS(NS,n);for(const k in a)e.setAttribute(k,a[k]);(p||svg).appendChild(e);return e};
  const cam=document.createElementNS(NS,'g'); while(svg.childNodes.length>1) cam.appendChild(svg.childNodes[1]); svg.appendChild(cam);
  const hud=el('g',{});
  el('rect',{x:46,y:900,width:960,height:150,rx:14,fill:'#241a0e','fill-opacity':.88},hud);
  el('rect',{x:46,y:900,width:8,height:150,fill:'#c9742a'},hud);
  el('text',{x:80,y:962,'font-size':54,fill:'#f1e7cb','font-family':'Lora'},hud).textContent=cfg.cap;
  el('text',{x:80,y:1020,'font-size':34,fill:'#d6aa6e','font-family':'Lora'},hud).textContent='Cận cảnh · minh họa';
  el('image',{href:cfg.logo,x:1920-44-130,y:34,width:130,height:130,opacity:.8},hud);
  const lerp=(a,b,u)=>a+(b-a)*u, cl=(v,a=0,b=1)=>Math.max(a,Math.min(b,v)), D=Math.PI/180;
  const easeIO=u=>u<.5?4*u*u*u:1-Math.pow(-2*u+2,3)/2, ease=u=>u*u*(3-2*u);
  const A=[]; const add=(e,kf,dur,ph,ez)=>{const a=e.animate(kf,{duration:dur*1000,iterations:Infinity,easing:ez||'ease-in-out'});a.pause();A.push([a,ph*1000])};
  let seed=7; const rnd=()=>(seed=(seed*16807)%2147483647)/2147483647;
  const tb=(e,o)=>{e.style.transformBox='fill-box';e.style.transformOrigin=o};
  Q('#clouds').forEach(e=>add(e,[{transform:'translateX(0)'},{transform:'translateX(-90px)'}],40,0,'linear'));
  Q('#mountains').forEach(e=>add(e,[{transform:'translateX(0)'},{transform:'translateX(-30px)'}],30,0,'linear'));
  Q('#birds').forEach(e=>add(e,[{transform:'translate(0,0)'},{transform:'translate(260px,-30px)'}],14,0,'linear'));
  Q('.pen').forEach(e=>{tb(e,'left center');const d=1.1+rnd()*.5;add(e,[{rotate:'-3deg'},{rotate:'5deg'},{rotate:'-2deg'},{rotate:'4deg'},{rotate:'-3deg'}],d,rnd()*3);add(e,[{transform:'skewY(-4deg) scaleX(1)'},{transform:'skewY(4deg) scaleX(.9)'},{transform:'skewY(-4deg) scaleX(1)'}],d*1.3,rnd()*3)});
  Q('#bam').forEach(e=>{tb(e,'center bottom');add(e,[{transform:'skewX(-1.5deg)'},{transform:'skewX(1.5deg)'},{transform:'skewX(-1.5deg)'}],4.5,0)});
  const f$=(f,k)=>f.querySelector(k), setR=(e,d)=>{if(e)e.style.transform='rotate('+d+'deg)'};
  const rip=$('#rip'), arrows=$('#arrows'), smk=$('#smokeg');
  const fire=(g,t,k,sz)=>{g.innerHTML='';for(let i=0;i<9;i++){const ph=t*5+i*1.7+k*3;const x=(i-4)*34+Math.sin(ph)*6,h=(46+30*Math.abs(Math.sin(ph*.8+i)))*sz;
    el('path',{d:`M${x-14},0 Q${x-20},${-h*.5} ${x},${-h} Q${x+20},${-h*.5} ${x+14},0Z`,fill:i%2?'#ffb347':'#ff7a2c',opacity:.92},g);
    el('path',{d:`M${x-7},0 Q${x-9},${-h*.35} ${x},${-h*.62} Q${x+9},${-h*.35} ${x+7},0Z`,fill:'#ffe08a'},g)}
    el('ellipse',{cx:0,cy:-30,rx:190,ry:70,fill:'#ff9a3c',opacity:.2},g)};
  // đường đi của ba bè: tới gần rồi bị chặn, bè đầu bị cháy và lùi
  const rpos=(k,t)=>{const t0=k*.8; let u=cl((t-t0)/(5.2)); const a=easeIO(u);   // tiến
    let x=lerp(1560-k*40,600+k*520,a), y=lerp(1010-k*8,860-k*14,a), s=lerp(1.25,1.0,a);
    const back=cl((t-(7.0+k*.8))/3.6); if(back>0){const b=ease(back); x+=b*(k==0?340:150); y+=b*(k==0?120:50); s+=b*.15}
    return [x,y,s]};
  window.__seek=t=>{
    A.forEach(([a,p])=>{a.currentTime=t*1000+p});
    // sóng
    rip.innerHTML='';
    for(let i=0;i<34;i++){const y=660+((i*37)%380), sp=18+(i%5)*5, x=((i*211-t*sp*3)%2100+2100)%2100-100, w=50+(i*13)%90;
      el('path',{d:`M${x},${y} q${w/4},-5 ${w/2},0 t${w/2},0`,stroke:'#e8f4fa','stroke-width':2.2,fill:'none',opacity:.28+.22*Math.sin(t*2+i),'stroke-linecap':'round'},rip)}
    Q('.swash').forEach((e,i)=>{e.setAttribute('rx',16+5*Math.sin(t*3+i));e.setAttribute('opacity',.35+.2*Math.sin(t*2.4+i*1.3))});
    // bè + quân Tống
    Q('.raft').forEach((r,k)=>{const [x,y,s]=rpos(k,t); const bob=Math.sin(t*2.1+k)*5, roll=Math.sin(t*1.6+k*2)*1.6;
      r.style.transform=`translate(${x}px,${y+bob}px) rotate(${roll}deg) scale(${s})`;
      const burning=(k==0&&t>5.2)||(k==1&&t>8.2); const g=$('#rfire'+k); if(burning){const gr=cl((t-(k==0?5.2:8.2))/1.6);fire(g,t,k,gr*1.1);g.setAttribute('transform','translate(-10,-8)')}else g.innerHTML='';
    });
    Q('.rman').forEach(f=>{const k=+f.dataset.k,m=+f.dataset.m; const w=2*Math.PI*(t/1.3+m*.31+k*.2); const [x,y,s]=rpos(k,t);
      const moving=t<(5.8+k*.8)||t>(7+k*.8); const burning=(k==0&&t>5.2)||(k==1&&t>8.2);
      const a=Math.sin(w);
      if(burning){const pa=Math.sin(t*9+m);setR(f$(f,'.armF'),-150+20*pa);setR(f$(f,'.armFf'),-30);setR(f$(f,'.armB'),-130-20*pa);setR(f$(f,'.armBf'),-40);setR(f$(f,'.torso'),-6+5*pa)}
      else if(m==1){setR(f$(f,'.armF'),-40+6*a);setR(f$(f,'.armFf'),-70);setR(f$(f,'.armB'),-40-6*a);setR(f$(f,'.armBf'),-72);setR(f$(f,'.torso'),4+2*a)}
      else{const pole=.5-.5*Math.cos(w);setR(f$(f,'.armF'),-30-70*pole);setR(f$(f,'.armFf'),-20);setR(f$(f,'.armB'),-20-60*pole);setR(f$(f,'.armBf'),-20);setR(f$(f,'.torso'),-8+14*pole)}
      setR(f$(f,'.legF'),-5);setR(f$(f,'.legFs'),6);setR(f$(f,'.legB'),8);setR(f$(f,'.legBs'),5);
      const sp=f$(f,'.spear'); if(sp) sp.style.display='none';
    });
    // quân Đại Việt sau hàng rào: giương cung ném giáo theo nhịp
    Q('.vsold').forEach((f,i)=>{const w=2*Math.PI*(t/1.9+i*.17), x=+f.dataset.x;const pa=Math.max(0,Math.sin(w));
      f.style.transform=`translate(${x}px,${f.getAttribute('transform').match(/translate\([^,]+,([\d.]+)/)[1]}px) scale(-.68,.68)`;
      setR(f$(f,'.armF'),-110+50*pa);setR(f$(f,'.armFf'),-20);setR(f$(f,'.armB'),-60);setR(f$(f,'.armBf'),-25);setR(f$(f,'.torso'),-4+6*pa);
      const sp=f$(f,'.spear'); if(sp) sp.style.display='none'; f.style.translate='0px '+(-2*Math.abs(Math.sin(w/2)))+'px'});
    // tên: tên thường từ hàng rào xuống bè; tên lửa nhắm bè đầu
    arrows.innerHTML='';
    for(let j=0;j<10;j++){const per=1.25, ph=((t/per+j*.1)%1), idx=Math.floor(t/per+j*.1);
      const sx=140+((idx*97+j*173)%1600), a0=[sx,450];
      const k=(idx+j)%3,[bx,by]=rpos(k,t); const a1=[bx-60+((j*53)%120),by-60];
      const x=lerp(a0[0],a1[0],ph), y=lerp(a0[1],a1[1],ph)-Math.sin(ph*Math.PI)*120;
      const ph2=Math.max(0,ph-.06), x2=lerp(a0[0],a1[0],ph2), y2=lerp(a0[1],a1[1],ph2)-Math.sin(ph2*Math.PI)*120;
      const fl=(j%3==0)&&t>3.6&&t<6.0; if(ph<.96){el('path',{d:`M${x2},${y2} L${x},${y}`,stroke:fl?'#ffb347':'#f4e3b0','stroke-width':fl?5:3,'stroke-linecap':'round',opacity:.95},arrows); if(fl)el('circle',{cx:x,cy:y,r:7,fill:'#ff9a3c',opacity:.8},arrows)}}
    // khói từ bè cháy
    smk.innerHTML='';
    for(const k of [0,1]){const t0=k==0?5.2:8.2; if(t<t0) continue; const [x,y,s]=rpos(k,t);
      for(let i=0;i<7;i++){const ph=(((t-t0)*.45+i/7)%1);el('ellipse',{cx:x-20+Math.sin(i*2+t)*30+ph*60,cy:y-120-ph*260,rx:30+ph*50,ry:22+ph*34,fill:'#4a4440',opacity:.5*(1-ph)},smk)}}
    const u=easeIO(cl(t/cfg.dur)), z=lerp(1.0,1.38,u), cx=lerp(960,1080,u), cy=Math.min(lerp(540,760,u),1080-540/z);
    cam.style.transformOrigin='0 0'; cam.style.transform=`translate(${960-cx*z}px,${540-cy*z}px) scale(${z})`;
  };
}
"""


def main():
    cfg = dict(dur=DUR, cap='Sông Như Nguyệt, đầu năm 1077', logo=(ROOT / 'assets/logo/nguoi-gac-su.png').as_uri())
    p = pathlib.Path('/tmp/nn'); p.mkdir(exist_ok=True); f = p / 'nn.svg'; f.write_text(build(), encoding='utf-8')
    with sync_playwright() as pw:
        br = pw.chromium.launch(args=['--allow-file-access-from-files']); pg = br.new_page(viewport={'width': 1920, 'height': 1080})
        errs = []; pg.on('pageerror', lambda e: errs.append(str(e)[:200])); pg.goto(f.as_uri()); pg.evaluate(JS, cfg)
        if sys.argv[1] == 'still':
            for t in map(float, sys.argv[2:]):
                pg.evaluate('t=>window.__seek(t)', t); pg.screenshot(path=f'/tmp/nn/still_{t}.png')
        else:
            a, b, d = int(sys.argv[1]), int(sys.argv[2]), pathlib.Path(sys.argv[3]); d.mkdir(parents=True, exist_ok=True)
            for i in range(a, b):
                pg.evaluate('t=>window.__seek(t)', i / FPS); pg.screenshot(path=str(d / f'{i:04d}.png'))
        if errs: print('LỖI', errs[:3])
        br.close()


main()
