// Ảnh bìa Góc IoT: node tao_bia.cjs <khung.png> <ra.png> "<dòng 1>" "<dòng 2>"
// Khung lấy từ cảnh mở đầu (Bóng lớn): TLFILE=giong/thoi-luong.json AT=3.5 node dung_hinh.cjs <id> <thư mục> at
const sharp = require('sharp');
const [, , src, out, l1, l2] = process.argv;
const FONT = "Inter, 'DejaVu Sans', sans-serif", NAVY = '#12233F', YEL = '#FFD84D';
const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');
const fit = (s, w, max) => Math.min(max, Math.floor(w / (s.length * 0.56)));
const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920">
<rect x="40" y="1400" width="1000" height="250" rx="44" fill="${NAVY}" stroke="#FFFFFF" stroke-width="6"/>
<text x="540" y="1510" text-anchor="middle" font-family="${FONT}" font-weight="800" font-size="${fit(l1, 920, 84)}" fill="${YEL}">${esc(l1)}</text>
<text x="540" y="1596" text-anchor="middle" font-family="${FONT}" font-weight="700" font-size="${fit(l2, 920, 52)}" fill="#FFFFFF">${esc(l2)}</text>
<rect x="340" y="1700" width="400" height="96" rx="48" fill="${YEL}" stroke="${NAVY}" stroke-width="6"/>
<text x="540" y="1768" text-anchor="middle" font-family="${FONT}" font-weight="800" font-size="56" fill="${NAVY}">Góc IoT</text>
</svg>`;
sharp(src).composite([{ input: Buffer.from(svg) }]).jpeg({ quality: 92 }).toFile(out).then(() => console.log('ok', out));
