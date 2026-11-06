"""Ảnh bìa dọc 1080x1920 cho "Chuyện cai trị ngàn năm" tập 1: python assets/bia/HAN1/tao_bia.py [ra.png]
Nền: khung bản đồ của trang dựng (bỏ HUD, phụ đề); logo theo quy tắc kênh: vuông 130 px, độ đậm 0,8, góc trên phải, cách mép phải 44 px và mép trên 34 px."""
import sys, json
from pathlib import Path
from playwright.sync_api import sync_playwright
R = Path(__file__).resolve().parents[3]; D = R / 'phim_ban_do/doc9x16'
out = sys.argv[1] if len(sys.argv) > 1 else str(Path(__file__).with_name('bia_dung.png'))
kb = json.load(open(R / 'ke-hoach/thu-giong-hai/han1v3_full.json', encoding='utf-8'))
(D / 'data.js').write_text('const SCRIPT=' + json.dumps([{'n': b['n'], 'text': b.get('hien', b['text'])} for b in kb], ensure_ascii=False) + ';\n', encoding='utf-8')
with sync_playwright() as p:
    br = p.chromium.launch(args=['--allow-file-access-from-files']); pg = br.new_page(viewport={'width': 1080, 'height': 1920})
    pg.goto('file://' + str(D / 'trang.html')); pg.wait_for_timeout(800)
    pg.evaluate('''()=>{render(R(2)+4.6);
      [HUD,SUBP,SUBG,barsG,fr,topShade,cp].forEach(e=>e.setAttribute('display','none'));
      OV.querySelectorAll('text').forEach(t=>{if(/Lệnh|Đất do|Nam Việt/.test(t.textContent))t.setAttribute('display','none')});
      const g=el(S,'g',{});
      el(g,'rect',{x:0,y:0,width:1080,height:1920,fill:'#0d0b08',opacity:.28});
      el(g,'rect',{x:0,y:1020,width:1080,height:900,fill:'url(#bf)'});
      T(g,52,200,'110 TCN',130,'#fff',16,'start');
      T(g,540,1330,'CHÍN QUẬN',170,'#fff',26);
      T(g,540,1470,'RỒI SAO?',150,GOLD,24);
      T(g,540,1600,'CHUYỆN CAI TRỊ NGÀN NĂM · TẬP 1',44,'#f1e9d2',10);
      el(g,'image',{href:'../../assets/logo/nguoi-gac-su.png',x:1080-44-130,y:34,width:130,height:130,opacity:.8});
    }''')
    pg.wait_for_timeout(300); pg.screenshot(path=out); br.close()
print(out)
