"""Mô phỏng bố cục khung hình (chưa có nhân vật, ảnh tư liệu để ô giữ chỗ) cho tập Tutankhamun, bản ngang và dọc."""
import asyncio
from playwright.async_api import async_playwright
INK="#241a16"; PAPER="#efe6d2"; SEAL="#b3261e"
CSS=f"""
*{{box-sizing:border-box;margin:0}} body{{font-family:'Inter','DejaVu Sans',sans-serif;overflow:hidden}}
.f{{position:relative;width:100%;height:100%}}
.dark{{background:radial-gradient(ellipse at 50% 40%,#3a2a22,#16100d)}} .paper{{background:{PAPER};color:{INK}}}
.tag{{position:absolute;font-weight:800;letter-spacing:.14em;font-size:var(--s2)}}
.cap{{position:absolute;left:50%;transform:translateX(-50%);background:#fff;color:{INK};font-weight:800;
 border-radius:var(--r);padding:var(--p1) var(--p2);font-size:var(--s1);text-align:center;box-shadow:0 6px 20px #0004;max-width:88%}}
.ph{{position:absolute;background:#c9bda3;border:4px solid {INK};display:flex;align-items:flex-end;justify-content:center;
 font-weight:700;font-size:var(--s3);color:{INK};padding:10px;text-align:center}}
.lab{{position:absolute;background:{INK};color:{PAPER};font-weight:800;font-size:var(--s3);padding:4px 12px;letter-spacing:.1em}}
.seal{{position:absolute;border:8px solid {SEAL};color:{SEAL};font-weight:900;text-align:center;border-radius:12px;transform:rotate(-6deg);line-height:1.1}}
.chip{{position:absolute;border:5px solid {INK};background:#fff;font-weight:800;border-radius:14px;text-align:center}}
svg{{position:absolute;inset:0;width:100%;height:100%}}
"""
def H(w,h):
    v=h>w
    s=dict(s1=34 if not v else 40,s2=18 if not v else 22,s3=17 if not v else 21,r=22,p1=12,p2=26)
    var=";".join(f"--{k}:{x}{'px'}" for k,x in s.items())
    return var
def frame_hook(w,h):
    v=h>w
    return f"""<div class="f dark" style="{H(w,h)}"><div class="tag" style="left:{5}%;top:{4}%;color:#e8c9a0">HỒ SƠ 01 · LỜI NGUYỀN TUTANKHAMUN</div>
<div style="position:absolute;left:8%;right:8%;top:{30 if not v else 28}%;color:#fff;font-weight:900;font-size:{64 if not v else 84}px;line-height:1.15;text-align:center">Mở mộ vua xong,<br>ông chết.</div>
<div style="position:absolute;left:8%;right:8%;top:{62 if not v else 52}%;color:#e8c9a0;font-weight:800;font-size:{36 if not v else 46}px;text-align:center">Lời nguyền có thật không?</div>
</div>"""
def frame_board(w,h):
    v=h>w
    if not v:
        ph=[(6,14,26,40,'Ảnh tư liệu: khu mộ'),(37,10,26,44,'Ảnh tư liệu: nhật ký Carter'),(68,14,26,40,'Ảnh tư liệu: bài báo 1923')]
        txt=[("LỜI ĐỒN",12,60),("BẰNG CHỨNG",72,60)]
    else:
        ph=[(12,10,80,17,'Ảnh tư liệu: khu mộ'),(12,33,80,17,'Ảnh tư liệu: nhật ký Carter'),(12,56,80,17,'Ảnh tư liệu: bài báo 1923')]
        txt=[('LỜI ĐỒN',12,1.5),('BẰNG CHỨNG',12,74.5)]
    out=f'<div class="f paper" style="{H(w,h)}">'
    for x,y,ww,hh,t in ph:
        out+=f'<div class="ph" style="left:{x}%;top:{y}%;width:{ww}%;height:{hh}%">{t}</div><div class="lab" style="left:{x}%;top:{y-(4 if not v else 3)}%">TƯ LIỆU</div>'
    out+=f'<svg viewBox="0 0 100 100" preserveAspectRatio="none"><path d="M{20 if not v else 6},{54 if not v else 14} Q{50 if not v else 2},{70 if not v else 44} {80 if not v else 6},{54 if not v else 74}" stroke="{SEAL}" stroke-width="0.6" fill="none"/></svg>'
    for t,x,y in txt:
        out+=f'<div class="tag" style="left:{x}%;top:{y}%;color:{SEAL}">{t}</div>'
    out+=f'<div class="cap" style="bottom:{8 if not v else 8}%">Hai mươi lăm người đã vào khu mộ kín.</div></div>'
    return out
def frame_seal(w,h):
    v=h>w
    return f"""<div class="f paper" style="{H(w,h)}"><div class="seal" style="left:{26 if not v else 14}%;top:{14 if not v else 12}%;width:{48 if not v else 72}%;padding:{22 if not v else 30}px 10px;font-size:{34 if not v else 40}px">MỨC ĐỘ CHẮC CHẮN<br><span style="font-size:{92 if not v else 110}px">CAO</span><br><span style="font-size:{22 if not v else 26}px;font-weight:700">không có bằng chứng cho lời nguyền</span></div>
<div style="position:absolute;left:8%;right:8%;top:{58 if not v else 48}%;font-weight:900;font-size:{36 if not v else 46}px;text-align:center">Còn thiếu một thứ nữa mới đủ để tin.</div>
<div class="chip" style="left:{8 if not v else 8}%;top:{74 if not v else 62}%;width:{40 if not v else 84}%;padding:14px;font-size:{26 if not v else 34}px">Dòng chữ khắc trong mộ</div>
<div class="chip" style="left:{52 if not v else 8}%;top:{74 if not v else 72}%;width:{40 if not v else 84}%;padding:14px;font-size:{26 if not v else 34}px">Nhóm người chết sớm bất thường</div></div>"""
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for name,(w,h) in {"ngang":(1280,720),"doc":(720,1280)}.items():
            for i,fn in enumerate([frame_hook,frame_board,frame_seal],1):
                pg=await b.new_page(viewport={"width":w,"height":h})
                await pg.set_content(f"<style>{CSS} html,body{{width:{w}px;height:{h}px}}</style>{fn(w,h)}")
                await pg.screenshot(path=f"{name}_{i}.png"); await pg.close()
        await b.close()
asyncio.run(main())
from PIL import Image
a=[Image.open(f"ngang_{i}.png") for i in (1,2,3)]
W=1280;H_=720;sheet=Image.new("RGB",(W,H_*3+40),"#000")
for i,im in enumerate(a): sheet.paste(im,(0,i*(H_+20)))
sheet.resize((960,int(sheet.height*0.75))).save("bo_cuc_ngang.jpg",quality=88)
d=[Image.open(f"doc_{i}.png") for i in (1,2,3)]
sh=Image.new("RGB",(720*3+40,1280),"#000")
for i,im in enumerate(d): sh.paste(im,(i*740,0))
sh.resize((int(sh.width*0.62),int(sh.height*0.62))).save("bo_cuc_doc.jpg",quality=88)
print("xong")
