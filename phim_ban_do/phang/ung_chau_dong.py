"""Cảnh chuyển động chi tiết: quân Đại Việt chồng bao đất lên mặt thành Ung Châu (bản demo cận cảnh, minh họa).
python phim_ban_do/phang/ung_chau_dong.py <từ_khung> <đến_khung> <thư_mục>   |   still <giây>...   (24 khung/giây)"""
import sys, pathlib, random, json
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
X0, X1, GY = 300, 1190, 905           # chân dốc, đỉnh dốc, mặt đất
WALLY = 640


def build():
    L = outdoor('dusk', sun=(1520, 330), cl=8, mt=600, birds_=(520, 210))
    far = ''.join(hut(x, 880, .55) for x in range(60, 1900, 330)) + ''.join(tree(x + 120, 880, .7, 'dusk') for x in range(60, 1900, 330))
    L.append(G('farland', f'<rect y="760" width="1920" height="130" fill="#3a3040"/>{far}'))
    L.append(wall(WALLY, 'dusk', tower_x=1560, side='song', h=250))
    # khói sau thành
    sm = ''.join(f'<g class="sm" data-k="{k}">{smoke(x, WALLY-60, 260, "#d9c7b8", .42, 18)}</g>' for k, x in enumerate((1180, 1330, 1800)))
    L.append(G('smoke', sm))
    # cờ trên tháp và tường
    L.append(G('flags', pennant(1620, 250, 470, '#b8352a', 170) + pennant(1210, 470, WALLY - 40, '#b8352a', 120) + pennant(1800, 480, WALLY - 40, '#b8352a', 120)))
    # quân giữ thành (nhỏ, đứng sau lỗ châu mai)
    df = ''
    for i, x in enumerate((1010, 1090, 1170, 1250, 1330, 1700, 1780, 1860)):
        s = .5; col = ('#5a4a62', '#4a5a72', '#62485a')[i % 3]
        f = side_fig(f'd{i}', x, WALLY - 50 - 86 * s + 40, s, col, hat='song', seed=20 + i, pants=sh(col, .6), armor='#3a3e48', sash='#8a2a24', spear='#b8352a', flip=-1, shadow=False)
        df += f.replace(f'class="sf" id="d{i}"', f'class="sf def" id="d{i}" data-i="{i}"')
    L.append(G('defenders', df))
    L.append(f'<rect y="{WALLY+250-8}" width="1920" height="12" fill="#2a2030"/>')
    L.append(ground('dusk', GY - 20, '#4a3a34'))
    L.append(f'<rect y="{GY-20}" width="1920" height="200" fill="#5a4838"/>')
    L.append(ground_marks_(GY - 10, GY + 60, 'gmA', 1)); L.append(ground_marks_(GY + 70, GY + 160, 'gmB', 2))
    # đống đất bên trái + bao đất
    L.append(G('pile', '<path d="M20,930 Q70,820 150,800 Q240,790 300,930Z" fill="#6a5238"/><path d="M60,930 Q110,850 170,840 Q240,845 280,930Z" fill="#7a6044"/>'
                       + sacks(120, 940, 1.0, 5)))
    # dốc bao đất lớn dần (JS vẽ lại polygon + hàng bao)
    L.append('<g id="ramp"><path id="rampbody" fill="#8c6f45"/><g id="ramprows"></g></g>')
    # người xếp bao tại đống đất
    fillers = ''
    for k, x in enumerate((200, 330)):
        f = side_fig(f'f{k}', x, GY + 24 - 86 * 1.1, 1.1, ('#3a4a6a', '#41506e')[k], hat='cone', seed=40 + k, pants='#3a3228', armor='#4a4e58', sash='#a8452f', shadow=True)
        fillers += f.replace(f'class="sf" id="f{k}"', f'class="sf fill" id="f{k}" data-i="{k}" data-x="{x}"')
    L.append(G('fillers', fillers))
    # người vác bao đất
    W_ = ''
    cols = ['#3a4a6a', '#34445f', '#41506e', '#2e3d58', '#3c4c70', '#3a4a6a', '#41506e']
    for i in range(7):
        f = side_fig(f'w{i}', 0, 0, 1.08, cols[i], hat='cone' if i % 3 else 'helmet', seed=60 + i, pants=sh(cols[i], .6), armor='#4a4e58' if i % 2 else None, sash='#a8452f',
                     beard=('white_goatee' if i == 3 else None), shadow=True)
        W_ += f.replace(f'class="sf" id="w{i}"', f'class="sf walker" id="w{i}" data-i="{i}"')
    L.append(G('walkers', W_))
    L.append('<g id="arrows"></g><g id="dust"></g>')
    L.append(f'<rect width="1920" height="1080" fill="url(#vg)"/>')
    return svg(L, 'dusk')


def ground_marks_(y0, y1, cls, seed, n=40, col='#3e2f26'):
    r = random.Random(seed); o = ''
    for _ in range(n):
        x = r.randint(-100, 2000); y = r.randint(y0, y1); w = r.randint(30, 90)
        o += f'<ellipse cx="{x}" cy="{y}" rx="{w}" ry="{3+(y-y0)*.03}" fill="{col}" opacity=".5"/>'
    return f'<g class="{cls}">{o}</g>'


JS = r"""
(cfg) => {
  const NS='http://www.w3.org/2000/svg', svg=document.documentElement, D=Math.PI/180;
  const Q=s=>[...document.querySelectorAll(s)], $=s=>document.querySelector(s);
  const el=(n,a,p)=>{const e=document.createElementNS(NS,n);for(const k in a)e.setAttribute(k,a[k]);(p||svg).appendChild(e);return e};
  const cam=document.createElementNS(NS,'g'); cam.id='cam'; while(svg.childNodes.length>1) cam.appendChild(svg.childNodes[1]); svg.appendChild(cam);
  // HUD (ngoài camera)
  const hud=el('g',{id:'hud'});
  const chip=el('g',{},hud);
  el('rect',{x:46,y:900,width:880,height:150,rx:14,fill:'#241a0e','fill-opacity':.88},chip);
  el('rect',{x:46,y:900,width:8,height:150,fill:'#c9742a'},chip);
  const t1=el('text',{x:80,y:962,'font-size':54,fill:'#f1e7cb','font-family':'Lora'},chip); t1.textContent=cfg.cap;
  const t2=el('text',{x:80,y:1020,'font-size':34,fill:'#d6aa6e','font-family':'Lora'},chip); t2.textContent='Cận cảnh · minh họa';
  el('image',{href:cfg.logo,x:1920-44-130,y:34,width:130,height:130,opacity:.8},hud);
  const X0=cfg.X0, X1=cfg.X1, GY=cfg.GY, WY=cfg.WALLY, N=14;
  const lerp=(a,b,u)=>a+(b-a)*u, cl=(v,a=0,b=1)=>Math.max(a,Math.min(b,v));
  const ease=u=>u*u*(3-2*u), easeIO=u=>u<.5?4*u*u*u:1-Math.pow(-2*u+2,3)/2;
  const prog=t=>cl(.12+.88*(t/cfg.dur),0,1);         // độ cao dốc 12% -> 100%
  const topY=t=>GY-prog(t)*(GY-WY+4);
  const surf=(x,t)=>lerp(GY, topY(t), cl((x-X0+80)/(X1-X0+80)));  // mặt dốc
  // --- vòng quay cảnh quan (kéo theo thời gian, xác định theo t) ---
  const A=[]; const add=(e,kf,dur,ph,ease2)=>{const a=e.animate(kf,{duration:dur*1000,iterations:Infinity,easing:ease2||'ease-in-out'});a.pause();A.push([a,ph*1000])};
  let seed=7; const rnd=()=>(seed=(seed*16807)%2147483647)/2147483647;
  const tb=(e,o)=>{e.style.transformBox='fill-box';e.style.transformOrigin=o};
  Q('#clouds').forEach(e=>add(e,[{transform:'translateX(0)'},{transform:'translateX(-90px)'}],40,0,'linear'));
  Q('#mountains').forEach(e=>add(e,[{transform:'translateX(0)'},{transform:'translateX(-30px)'}],30,0,'linear'));
  Q('#birds').forEach(e=>add(e,[{transform:'translate(0,0)'},{transform:'translate(-260px,-30px)'}],14,0,'linear'));
  Q('.pen').forEach(e=>{tb(e,'left center');const d=1.1+rnd()*.5;add(e,[{rotate:'-3deg'},{rotate:'5deg'},{rotate:'-2deg'},{rotate:'4deg'},{rotate:'-3deg'}],d,rnd()*3);add(e,[{transform:'skewY(-4deg) scaleX(1)'},{transform:'skewY(4deg) scaleX(.9)'},{transform:'skewY(-4deg) scaleX(1)'}],d*1.3,rnd()*3)});
  Q('.sm').forEach((e,i)=>{tb(e,'center bottom');add(e,[{transform:'translateY(0) scale(1,1)',opacity:.0},{transform:'translateY(-40px) scale(1.1,1.1)',opacity:1,offset:.25},{transform:'translateY(-150px) scale(1.5,1.3)',opacity:0}],6.5,i*2.1,'ease-out')});
  const fig=(f,key)=>f.querySelector(key), setR=(e,d)=>{if(e)e.style.transform='rotate('+d+'deg)'};
  const pose=(f,w,carry,moving)=>{
    const sn=Math.sin(w), cs=Math.cos(w);
    const thigh=a=>-26*Math.sin(a), knee=a=>4+48*Math.pow(Math.max(0,Math.cos(a)),1.4);
    if(moving){setR(fig(f,'.legF'),thigh(w));setR(fig(f,'.legFs'),knee(w));setR(fig(f,'.legB'),thigh(w+Math.PI));setR(fig(f,'.legBs'),knee(w+Math.PI));}
    else{setR(fig(f,'.legF'),-3);setR(fig(f,'.legFs'),6);setR(fig(f,'.legB'),5);setR(fig(f,'.legBs'),4)}
    if(carry){setR(fig(f,'.armF'),-148);setR(fig(f,'.armFf'),-38);setR(fig(f,'.armB'),-132+4*sn);setR(fig(f,'.armBf'),-44);setR(fig(f,'.torso'),9+1.6*cs)}
    else{setR(fig(f,'.armB'),30*sn);setR(fig(f,'.armBf'),-22-12*Math.max(0,sn));setR(fig(f,'.armF'),-30*sn);setR(fig(f,'.armFf'),-26-10*Math.max(0,-sn));setR(fig(f,'.torso'),3+1.5*cs)}
    const sp=fig(f,'.spear'); if(sp) sp.style.display='none';
    fig(f,'.body').style.transform='translateY('+(moving?-3.4*Math.abs(Math.cos(w)):0)+'px)';
  };
  // bao đất trên vai: thêm một lần
  Q('.walker').forEach(f=>{const g=el('g',{class:'sack',transform:'translate(-14,-92) rotate(-18)'},fig(f,'.torso'));
    el('ellipse',{cx:0,cy:0,rx:30,ry:19,fill:'#b09a68',stroke:'#7a6a44','stroke-width':2},g);el('path',{d:'M-24,-2 Q0,-9 24,-2',stroke:'#7a6a44','stroke-width':2,fill:'none'},g);el('path',{d:'M-10,-14 q10,-9 20,0',stroke:'#7a6a44','stroke-width':2.4,fill:'none'},g)});
  const sacksG=$('#ramprows'), body=$('#rampbody');
  const CYC=cfg.cyc, STR=170;                         // chu kỳ một lượt (giây), bước chân (px / vòng)
  const dust=$('#dust'), arrows=$('#arrows');
  window.__seek=t=>{
    A.forEach(([a,p])=>{a.currentTime=t*1000+p});
    // dốc
    const ty=topY(t); body.setAttribute('d',`M${X0-120},${GY+10} L${X1+90},${GY+10} L${X1+90},${ty+14} Q${X1+60},${ty-6} ${X1-20},${ty-8} L${X0-120},${GY-4} Z`);
    sacksG.innerHTML='';
    const NB=26, courses=1+Math.ceil(prog(t)*2);
    for(let c=0;c<courses;c++)for(let r=0;r<NB;r++){const f=(r+(c%2)*.5)/NB, x=lerp(X0-100,X1+50,f), y=lerp(GY+2,ty+4,f)+10+c*20;
      if(y>GY+10) continue;
      el('ellipse',{cx:x,cy:y,rx:27,ry:15,fill:(r+c)%2?'#b8a370':'#a68f5c',stroke:'#6b5230','stroke-width':1.6},sacksG);
      if((r+c)%3==0)el('path',{d:`M${x-14},${y-3} q14,-8 28,0`,stroke:'#7a6a44','stroke-width':1.5,fill:'none'},sacksG)}
    // vẽ lớp bao theo bậc: các bao nhô lên mặt dốc
    // người vác
    Q('.walker').forEach(f=>{const i=+f.dataset.i; const u=((t/CYC+i/7)%1+1)%1;
      let x,carry,moving=true,dir=1,dist;
      if(u<.50){const k=u/.50; x=lerp(X0+10,X1-30,easeIO(k)*.0+k); carry=true; dist=x-X0}
      else if(u<.57){x=X1-30;carry=false;moving=false;dist=X1-X0}
      else if(u<.95){const k=(u-.57)/.38;x=lerp(X1-30,X0+10,k);carry=false;dir=-1;dist=(X1-X0)+(X1-30-x)}
      else{x=X0+10;carry=false;moving=false;dist=2*(X1-X0)}
      // lúc đặt bao (0.50-0.57) giơ tay đẩy bao lên; lúc nhặt (0.95-1) cúi xuống
      const w=2*Math.PI*dist/STR+i;
      pose(f,w,carry,moving);
      const s=1.08, yy=surf(x,t)-86*s+6-(carry?0:0);
      const slope=Math.atan2(topY(t)-GY,X1-X0)/D*.55;
      f.style.transform=`translate(${x}px,${yy}px) rotate(${dir>0?slope:-slope}deg) scale(${dir*s},${s})`;
      const sk=f.querySelector('.sack'); sk.style.display=carry?'block':'none';
      if(u>=.50&&u<.57){const k=(u-.50)/.07; setR(fig(f,'.armF'),-148+80*k);setR(fig(f,'.armB'),-132+70*k);setR(fig(f,'.torso'),9+8*Math.sin(k*Math.PI));}
      if(u>=.95||u<.02){const k=u>=.95?(u-.95)/.05:1+u/.02; setR(fig(f,'.torso'),12+22*Math.sin(Math.min(1,k)*Math.PI));setR(fig(f,'.armF'),-30+10*k);setR(fig(f,'.armB'),-20)}
      f.style.opacity=1;
    });
    // người xếp bao: cúi lên xuống
    Q('.fill').forEach((f,i)=>{const w=2*Math.PI*(t/1.7+i*.37), s=1.1; const b=.5-.5*Math.cos(w);
      setR(fig(f,'.torso'),8+30*b);setR(fig(f,'.armF'),20+60*b);setR(fig(f,'.armFf'),-20-30*b);setR(fig(f,'.armB'),10+50*b);setR(fig(f,'.armBf'),-30);
      setR(fig(f,'.legF'),-6);setR(fig(f,'.legFs'),8);setR(fig(f,'.legB'),8);setR(fig(f,'.legBs'),6);
      const sp=fig(f,'.spear'); if(sp) sp.style.display='none';
      f.style.transform=`translate(${f.dataset.x}px,${GY+24-86*1.1+5}px) scale(${i?-1.1:1.1},1.1)`});
    // quân giữ thành đung đưa nhẹ
    Q('.def').forEach((f,i)=>{const w=2*Math.PI*(t/2.2+i*.31);f.style.translate='0px '+(-2*Math.sin(w))+'px';
      setR(fig(f,'.armF'),-90-14*Math.sin(w));setR(fig(f,'.armFf'),-20);setR(fig(f,'.armB'),10);setR(fig(f,'.torso'),2*Math.sin(w))});
    // tên bắn từ thành xuống
    arrows.innerHTML='';
    for(let k=0;k<5;k++){const ph=((t/1.35+k*.21)%1), seedx=(Math.floor(t/1.35+k*.21)*37+k*11)%100/100;
      const a0=[1050+seedx*600,WY-40], a1=[420+seedx*760,GY+10+k*14];
      const f=ph, x=lerp(a0[0],a1[0],f), y=lerp(a0[1],a1[1],f)-Math.sin(f*Math.PI)*210;
      const f2=Math.max(0,f-.05), x2=lerp(a0[0],a1[0],f2), y2=lerp(a0[1],a1[1],f2)-Math.sin(f2*Math.PI)*210;
      if(f<.97)el('path',{d:`M${x2},${y2} L${x},${y}`,stroke:'#f4e3b0','stroke-width':3.2,'stroke-linecap':'round',opacity:.9},arrows)}
    // bụi dưới chân người vác
    dust.innerHTML='';
    Q('.walker').forEach((f,i)=>{const m=f.style.transform.match(/translate\(([-\d.]+)px,\s*([-\d.]+)px/); if(!m) return; const x=+m[1], y=+m[2]+86*1.08-6;
      for(let k=0;k<3;k++){const ph=((t*1.6+i*.3+k*.33)%1);el('ellipse',{cx:x-30*(f.style.transform.indexOf('scale(-')<0?1:-1)*ph-10,cy:y-4-ph*14,rx:6+ph*14,ry:3+ph*6,fill:'#c9a77a',opacity:.28*(1-ph)},dust)}});
    // camera: dolly + zoom mượt (ease-in-out liên tục)
    const u=easeIO(cl(t/cfg.dur)), z=lerp(1.0,1.55,u), cx=lerp(960,1010,u), cy=lerp(560,700,u);
    cam.style.transformOrigin='0 0'; cam.style.transform=`translate(${960-cx*z}px,${540-cy*z}px) scale(${z})`;
  };
}
"""


def main():
    cfg = dict(X0=X0, X1=X1, GY=GY, WALLY=WALLY, dur=DUR, cyc=8.0, cap='Ung Châu, đầu năm 1076', logo=(ROOT / 'assets/logo/nguoi-gac-su.png').as_uri())
    p = pathlib.Path('/tmp/uc'); p.mkdir(exist_ok=True); f = p / 'uc.svg'; f.write_text(build(), encoding='utf-8')
    with sync_playwright() as pw:
        br = pw.chromium.launch(args=['--allow-file-access-from-files']); pg = br.new_page(viewport={'width': 1920, 'height': 1080}); pg.goto(f.as_uri()); pg.evaluate(JS, cfg)
        if sys.argv[1] == 'still':
            for t in map(float, sys.argv[2:]):
                pg.evaluate('t=>window.__seek(t)', t); pg.screenshot(path=f'/tmp/uc/still_{t}.png')
        else:
            a, b, d = int(sys.argv[1]), int(sys.argv[2]), pathlib.Path(sys.argv[3]); d.mkdir(parents=True, exist_ok=True)
            for i in range(a, b):
                pg.evaluate('t=>window.__seek(t)', i / FPS); pg.screenshot(path=str(d / f'{i:04d}.png'))
        br.close()


main()
