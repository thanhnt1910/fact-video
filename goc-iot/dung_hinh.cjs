const sharp = require('/opt/npm-tools/node_modules/sharp');
const fs = require('fs');
const path = require('path');

const W = 1080, H = 1920, FPS = 24;
const VID = parseInt(process.argv[2], 10);
const outDir = process.argv[3];
const mode = process.argv[4] || 'test';
const KB = JSON.parse(fs.readFileSync(path.join(__dirname, 'kich-ban.json'), 'utf-8'));
let TL = {};
try { TL = JSON.parse(fs.readFileSync((process.env.TLFILE || path.join(__dirname, 'giong', 'thoi-luong.json')), 'utf-8')); } catch (e) {}
const FONT = "Inter, 'DejaVu Sans', sans-serif";
const NAVY = '#12233F', YEL = '#FFD84D', TEAL = '#35C9B8';

const V1DEF = [
  { t0: 0, t1: 5.5, gfx: 's1', wave: false, mode: 'small', text: 'Bạn có từng bật đèn nhà mình từ xa bằng điện thoại chưa?',
    pts: [{ a: 1.5, b: 3.2, x: 850, y: 470 }, { a: 3.4, b: 4.9, x: 200, y: 430 }] },
  { t0: 5.5, t1: 12, gfx: 'hello', wave: true, mode: 'big', glow: true, text: 'Xin chào, mình là Bóng, chú bóng đèn thông minh của Góc IoT!', pts: [] },
  { t0: 12, t1: 23, gfx: 's3', wave: false, mode: 'small', text: 'IoT là viết tắt của Internet of Things: những vật dụng quen thuộc được gắn chip và kết nối mạng.',
    pts: [{ a: 3.0, b: 4.8, x: 540, y: 100 }, { a: 5.2, b: 6.9, x: 210, y: 250 }, { a: 7.9, b: 9.0, x: 540, y: 250 }, { a: 9.6, b: 10.9, x: 870, y: 250 }] },
  { t0: 23, t1: 31, gfx: 's4', wave: false, mode: 'small', text: 'Đèn, camera, đồng hồ... đều có thể là IoT. Mỗi ngày Bóng sẽ kể một điều nhỏ về chúng.',
    pts: [{ a: 0.3, b: 1.05, x: 210, y: 300 }, { a: 0.8, b: 1.4, x: 540, y: 300 }, { a: 1.5, b: 2.3, x: 870, y: 300 }, { a: 2.5, b: 3.6, x: 540, y: 700 }] },
  { t0: 31, t1: 38, gfx: 'curious', wave: false, mode: 'big', glow: true, text: 'Không cần giỏi kỹ thuật, chỉ cần tò mò là đủ!', pts: [] },
  { t0: 38, t1: 44, gfx: 'end', wave: true, mode: 'big', glow: true, text: 'Bạn đang dùng thiết bị thông minh nào? Bình luận cho Bóng biết nhé!', pts: [] },
];

let ALIGN = {};
try { if (process.env.ALIGN) ALIGN = JSON.parse(fs.readFileSync(process.env.ALIGN, 'utf-8')); } catch (e) {}
let scenes = [];
let TOTAL = 0;

const LAY = { big: { cy: 800, s: 1.25 }, small: { cy: 1040, s: 0.76 }, corner: { cy: 1275, s: 0.44 } };
// Nội dung chính đặt giữa khung hình; Bóng đứng ở góc dưới (xen kẽ trái, phải theo cảnh).
const CT = { cx: 540, cy: 790, sg: 1.08, ay: 500 };
const ctx = (x) => CT.cx + (x - 540) * CT.sg;
const cty = (y) => CT.cy + (y - CT.ay) * CT.sg;

const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const clamp01 = (x) => Math.max(0, Math.min(1, x));
const lerp = (a, b, k) => a + (b - a) * k;
const smooth = (x) => { x = clamp01(x); return x * x * (3 - 2 * x); };
const easeOutBack = (x) => { x = clamp01(x); const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); };
const f1 = (n) => n.toFixed(1);

function wrap(text, max) {
  const words = text.split(' ');
  const lines = [];
  let cur = '';
  for (const w of words) {
    if ((cur + ' ' + w).trim().length > max && cur) { lines.push(cur); cur = w; }
    else cur = (cur + ' ' + w).trim();
  }
  if (cur) lines.push(cur);
  return lines;
}

function at(cx, cy, k, local, delay, inner) {
  const o = clamp01((local - delay) / 0.3);
  if (o <= 0) return '';
  const s = k * easeOutBack((local - delay) / 0.5);
  const bob = local - delay > 0.6 ? 6 * Math.sin((local - delay) * 2.4 + cx * 0.013) : 0;
  return `<g opacity="${o.toFixed(2)}" transform="translate(${cx} ${(cy + bob).toFixed(1)}) scale(${s.toFixed(3)})">${inner}</g>`;
}

function wifi(cx, cy, col, op, w = 6) {
  return `<g opacity="${op}" stroke="${col}" stroke-width="${w}" stroke-linecap="round" fill="none">
<circle cx="${cx}" cy="${cy}" r="5" fill="${col}" stroke="none"/>
<path d="M${cx - 12} ${cy - 10} Q${cx} ${cy - 22} ${cx + 12} ${cy - 10}"/>
<path d="M${cx - 21} ${cy - 19} Q${cx} ${cy - 40} ${cx + 21} ${cy - 19}"/></g>`;
}

const iconBulb = () => `<circle cx="0" cy="-8" r="44" fill="${YEL}" stroke="#FFB300" stroke-width="6"/><rect x="-20" y="34" width="40" height="24" rx="8" fill="#8A97A8"/>`;
const iconCamera = () => `<rect x="-70" y="-40" width="140" height="90" rx="18" fill="#FFFFFF" stroke="${NAVY}" stroke-width="6"/><rect x="-38" y="-54" width="30" height="14" rx="5" fill="${NAVY}"/><circle cx="0" cy="5" r="26" fill="${NAVY}"/><circle cx="0" cy="5" r="10" fill="${TEAL}"/>`;
const iconWatch = () => `<rect x="-30" y="-78" width="60" height="44" rx="10" fill="${NAVY}"/><rect x="-30" y="34" width="60" height="44" rx="10" fill="${NAVY}"/><rect x="-38" y="-38" width="76" height="76" rx="22" fill="#FFFFFF" stroke="${NAVY}" stroke-width="6"/><path d="M0 -20 V0 H14" fill="none" stroke="${NAVY}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>`;
function iconChip() {
  const ps = [-27, -9, 9, 27];
  const pins = ps.map((p) => `<rect x="-62" y="${p - 4}" width="16" height="8" rx="3" fill="#8A97A8"/><rect x="46" y="${p - 4}" width="16" height="8" rx="3" fill="#8A97A8"/><rect x="${p - 4}" y="-62" width="8" height="16" rx="3" fill="#8A97A8"/><rect x="${p - 4}" y="46" width="8" height="16" rx="3" fill="#8A97A8"/>`).join('');
  return `${pins}<rect x="-46" y="-46" width="92" height="92" rx="12" fill="${NAVY}"/><rect x="-22" y="-22" width="44" height="44" rx="8" fill="${TEAL}"/>`;
}
const iconWifiBig = () => `<g stroke="${NAVY}" stroke-width="10" stroke-linecap="round" fill="none"><circle cx="0" cy="34" r="9" fill="${NAVY}" stroke="none"/><path d="M-26 12 Q0 -12 26 12"/><path d="M-46 -8 Q0 -48 46 -8"/><path d="M-66 -28 Q0 -86 66 -28"/></g>`;
const iconPlant = () => `<path d="M0 8 V-40" stroke="#3E9A5B" stroke-width="6" stroke-linecap="round"/><path d="M0 -10 Q-40 -10 -46 -44 Q-8 -46 0 -10 Z" fill="#6FCF8A" stroke="#3E9A5B" stroke-width="4" stroke-linejoin="round"/><path d="M0 -26 Q36 -26 42 -58 Q6 -60 0 -26 Z" fill="#6FCF8A" stroke="#3E9A5B" stroke-width="4" stroke-linejoin="round"/><path d="M-34 20 L34 20 L28 66 L-28 66 Z" fill="#E8896E" stroke="#C8604A" stroke-width="5" stroke-linejoin="round"/><rect x="-40" y="8" width="80" height="16" rx="6" fill="#D26F54" stroke="#C8604A" stroke-width="4"/>`;
const iconRouter = () => `<path d="M-60 10 L-70 -50 M60 10 L70 -50" stroke="${NAVY}" stroke-width="8" stroke-linecap="round"/><rect x="-90" y="10" width="180" height="64" rx="18" fill="${NAVY}"/><circle cx="-50" cy="42" r="6" fill="#3DDC84"/><circle cx="-20" cy="42" r="6" fill="${YEL}"/><circle cx="10" cy="42" r="6" fill="#FFFFFF"/>`;
const iconPhone = () => `<rect x="-62" y="-110" width="124" height="220" rx="26" fill="${NAVY}" stroke="#FFFFFF" stroke-width="6"/><rect x="-46" y="-80" width="92" height="150" rx="10" fill="#1B3358"/>`;

function house(on, onK) {
  const glow = on ? `<circle cx="0" cy="70" r="${(80 + 50 * onK).toFixed(0)}" fill="#FFF6C2" fill-opacity="0.5"/>` : '';
  const rays = on ? `<g stroke="#FFFFFF" stroke-width="8" stroke-linecap="round"><line x1="0" y1="-150" x2="0" y2="-185"/><line x1="-120" y1="-110" x2="-146" y2="-136"/><line x1="120" y1="-110" x2="146" y2="-136"/></g>` : '';
  return `${glow}${rays}<polygon points="-150,-10 0,-130 150,-10" fill="#FF8A5B" stroke="${NAVY}" stroke-width="6" stroke-linejoin="round"/>
<rect x="-120" y="-10" width="240" height="170" fill="#FFFFFF" stroke="${NAVY}" stroke-width="6"/>
<rect x="-80" y="30" width="100" height="80" rx="8" fill="${on ? YEL : '#1B3358'}" stroke="${NAVY}" stroke-width="5"/>
<line x1="-30" y1="30" x2="-30" y2="110" stroke="${NAVY}" stroke-width="4"/><line x1="-80" y1="70" x2="20" y2="70" stroke="${NAVY}" stroke-width="4"/>
<rect x="50" y="70" width="46" height="90" rx="6" fill="#C9D2DE" stroke="${NAVY}" stroke-width="5"/>`;
}

function gfxS1(local) {
  const toggleT = 4.0, onT = 4.9;
  const kn = smooth((local - toggleT) / 0.25);
  const trackCol = local >= toggleT ? '#3DDC84' : '#8A97A8';
  const knobX = -17 + 34 * kn;
  const ripple = local > toggleT - 0.2 && local < toggleT + 0.5 ? `<circle cx="${f1(knobX)}" cy="12" r="${f1(14 + 40 * (local - (toggleT - 0.2)) / 0.7)}" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-opacity="${(1 - (local - (toggleT - 0.2)) / 0.7).toFixed(2)}"/>` : '';
  const phone = at(200, 430, 1.5, local, 0.1, `${iconPhone()}<rect x="-34" y="-5" width="68" height="34" rx="17" fill="${trackCol}"/><circle cx="${f1(knobX)}" cy="12" r="13" fill="#FFFFFF"/>${ripple}`);
  const on = local >= onT;
  const onK = clamp01((local - onT) / 0.5);
  const home = at(850, 470, 1.4, local, 0.3, house(on, onK));
  const path = 'M300 370 Q450 190 630 360';
  let dots = '';
  if (local >= 4.2) {
    for (let i = 0; i < 5; i++) {
      const u = ((local - 4.2) * 0.9 + i / 5) % 1;
      const P0 = [300, 370], C = [450, 190], P2 = [630, 360];
      const x = (1 - u) * (1 - u) * P0[0] + 2 * (1 - u) * u * C[0] + u * u * P2[0];
      const y = (1 - u) * (1 - u) * P0[1] + 2 * (1 - u) * u * C[1] + u * u * P2[1];
      dots += `<circle cx="${f1(x)}" cy="${f1(y)}" r="12" fill="#FFFFFF"/>`;
    }
  }
  const wf = local > 0.4 ? wifi(200, 235, '#FFFFFF', (0.5 + 0.5 * Math.abs(Math.sin(local * 5))).toFixed(2)) : '';
  const sp = on ? [0, 1, 2, 3].map((i) => {
    const a = i * 1.57 + local * 2, r = 230 + 20 * Math.sin(local * 4 + i);
    return `<path d="M${f1(850 + Math.cos(a) * r)} ${f1(400 + Math.sin(a) * r * 0.7 - 6)} l4 10 l10 4 l-10 4 l-4 10 l-4 -10 l-10 -4 l10 -4 z" fill="#FFFFFF"/>`;
  }).join('') : '';
  return `<path d="${path}" fill="none" stroke="#FFFFFF" stroke-opacity="0.35" stroke-width="5" stroke-dasharray="14 16" stroke-linecap="round"/>${wf}${phone}${home}${dots}${sp}`;
}

function gfxHello(local) {
  const s = easeOutBack(local / 0.5);
  const a = clamp01(local / 0.3);
  const title = `<g opacity="${a}" transform="translate(540 270) scale(${s.toFixed(3)}) translate(-540 -270)"><text x="540" y="300" text-anchor="middle" font-family="${FONT}" font-weight="800" font-size="140" fill="${YEL}" stroke="${NAVY}" stroke-width="10" paint-order="stroke">Xin chào!</text></g>`;
  let conf = '';
  const cols = [YEL, '#FFFFFF', '#FF8A5B', NAVY];
  for (let i = 0; i < 22; i++) {
    const u = local * 0.9;
    if (u > 2.2) break;
    const ang = i * (Math.PI * 2 / 22) + i * 0.3;
    const sp = 380 + (i % 5) * 80;
    const x = 540 + Math.cos(ang) * sp * Math.min(u, 1.2);
    const y = 760 + Math.sin(ang) * sp * Math.min(u, 1.2) + 260 * u * u;
    const op = clamp01(1 - u / 2.2);
    conf += i % 2 === 0
      ? `<circle cx="${f1(x)}" cy="${f1(y)}" r="${8 + (i % 3) * 3}" fill="${cols[i % 4]}" opacity="${op.toFixed(2)}"/>`
      : `<rect x="${f1(x - 9)}" y="${f1(y - 9)}" width="18" height="18" rx="3" fill="${cols[i % 4]}" opacity="${op.toFixed(2)}" transform="rotate(${f1(u * 300 + i * 20)} ${f1(x)} ${f1(y)})"/>`;
  }
  return title + conf;
}

function gfxS3(local) {
  const card = (cx, label1, label2, icon, delay) => at(cx, 250, 1, local, delay,
    `<rect x="-115" y="-115" width="230" height="230" rx="36" fill="#FFFFFF" stroke="${NAVY}" stroke-width="6"/><g transform="scale(1.05)">${icon}</g>` +
    `<text x="0" y="170" text-anchor="middle" font-family="${FONT}" font-weight="700" font-size="38" fill="${NAVY}">${label1}</text><text x="0" y="214" text-anchor="middle" font-family="${FONT}" font-weight="700" font-size="38" fill="${NAVY}">${label2}</text>`);
  const plus = (cx, delay) => at(cx, 262, 1, local, delay, `<text x="0" y="36" text-anchor="middle" font-family="${FONT}" font-weight="800" font-size="120" fill="#FFFFFF" stroke="${NAVY}" stroke-width="8" paint-order="stroke">+</text>`);
  const res = at(540, 640, 1, local, 10.2, `<rect x="-400" y="-85" width="800" height="170" rx="48" fill="${NAVY}"/><text x="0" y="46" text-anchor="middle" font-family="${FONT}" font-weight="800" font-size="130" fill="${YEL}">= IoT</text>`);
  const sub = at(540, 100, 1, local, 2.8, `<text x="0" y="22" text-anchor="middle" font-family="${FONT}" font-weight="800" font-size="64" fill="#FFFFFF" stroke="${NAVY}" stroke-width="8" paint-order="stroke">IoT = Internet of Things</text>`);
  return card(210, 'Đồ vật', 'quen thuộc', iconBulb(), 5.0) + plus(375, 7.0) + card(540, 'Chip', 'nhỏ xíu', iconChip(), 7.7) + plus(705, 9.0) + card(870, 'Kết nối', 'mạng', iconWifiBig(), 9.4) + res + sub;
}

function gfxS4(local) {
  const R = [540, 700];
  const devs = [
    { x: 210, y: 300, icon: iconBulb(), label: 'Đèn', d: 0.2 },
    { x: 540, y: 300, icon: iconCamera(), label: 'Camera', d: 0.65 },
    { x: 870, y: 300, icon: iconWatch(), label: 'Đồng hồ', d: 1.35 },
  ];
  const RT = 2.4;
  let lines = '', dots = '', cards = '';
  devs.forEach((dv, k) => {
    if (local > RT) {
      lines += `<line x1="${R[0]}" y1="${R[1]}" x2="${dv.x}" y2="${dv.y}" stroke="#FFFFFF" stroke-opacity="0.45" stroke-width="5" stroke-dasharray="14 16" stroke-linecap="round"/>`;
      if (local > RT + 0.4) {
        for (let i = 0; i < 2; i++) {
          const u = (((local - RT) * 0.7 + i * 0.5 + k * 0.25) % 1);
          dots += `<circle cx="${f1(lerp(R[0], dv.x, u))}" cy="${f1(lerp(R[1], dv.y, u))}" r="11" fill="#FFFFFF"/>`;
        }
      }
    }
    cards += at(dv.x, dv.y, 1, local, dv.d,
      `<circle cx="0" cy="0" r="110" fill="#FFFFFF" stroke="${NAVY}" stroke-width="6"/><g transform="scale(1.1)">${dv.icon}</g><text x="0" y="162" text-anchor="middle" font-family="${FONT}" font-weight="700" font-size="38" fill="${NAVY}">${dv.label}</text>`);
  });
  const op = (0.5 + 0.5 * Math.abs(Math.sin(local * 3))).toFixed(2);
  const router = at(R[0], R[1], 1.5, local, RT, iconRouter()) + (local > RT + 0.3 ? `<g transform="translate(540 565) scale(1.6) translate(-540 -565)">${wifi(540, 565, '#FFFFFF', op)}</g>` : '');
  const badge = at(800, 740, 1, local, 3.4, `<rect x="-95" y="-48" width="190" height="96" rx="48" fill="${NAVY}"/><text x="0" y="22" text-anchor="middle" font-family="${FONT}" font-weight="800" font-size="64" fill="${YEL}">IoT</text>`);
  return lines + router + dots + cards + badge;
}

function gfxCurious(local, t) {
  const s = easeOutBack(local / 0.5);
  const a = clamp01(local / 0.3);
  const title = `<g opacity="${a}" transform="translate(540 240) scale(${s.toFixed(3)}) translate(-540 -240)"><text x="540" y="240" text-anchor="middle" font-family="${FONT}" font-weight="800" font-size="120" fill="${YEL}" stroke="${NAVY}" stroke-width="10" paint-order="stroke">Tò mò là đủ!</text><text x="540" y="330" text-anchor="middle" font-family="${FONT}" font-weight="700" font-size="48" fill="#FFFFFF" stroke="${NAVY}" stroke-width="8" paint-order="stroke">Không cần giỏi kỹ thuật</text></g>`;
  const xs = [140, 940, 200, 880, 120, 960];
  let bub = '';
  xs.forEach((x, i) => {
    const phase = (((local - i * 0.6) / 4) % 1 + 1) % 1;
    if (local < i * 0.6) return;
    const y = 900 - phase * 480;
    const op = Math.sqrt(Math.sin(Math.PI * phase));
    const r = 40 + (i % 3) * 8;
    bub += `<g opacity="${op.toFixed(2)}"><circle cx="${x + 12 * Math.sin(local * 2 + i)}" cy="${f1(y)}" r="${r}" fill="#FFFFFF" stroke="${NAVY}" stroke-width="6"/><text x="${x + 12 * Math.sin(local * 2 + i)}" y="${f1(y + r * 0.35)}" text-anchor="middle" font-family="${FONT}" font-weight="800" font-size="${r + 6}" fill="${NAVY}">?</text></g>`;
  });
  return title + bub;
}
function onlyBubbles(local) {
  const xs = [140, 940, 200, 880, 120, 960];
  let bub = '';
  xs.forEach((x, i) => {
    const phase = (((local - i * 0.6) / 4) % 1 + 1) % 1;
    if (local < i * 0.6) return;
    const y = 900 - phase * 480;
    const op = Math.sqrt(Math.sin(Math.PI * phase));
    const r = 40 + (i % 3) * 8;
    bub += `<g opacity="${op.toFixed(2)}"><circle cx="${x + 12 * Math.sin(local * 2 + i)}" cy="${f1(y)}" r="${r}" fill="#FFFFFF" stroke="${NAVY}" stroke-width="6"/><text x="${x + 12 * Math.sin(local * 2 + i)}" y="${f1(y + r * 0.35)}" text-anchor="middle" font-family="${FONT}" font-weight="800" font-size="${r + 6}" fill="${NAVY}">?</text></g>`;
  });
  return bub;
}

function gfxEnd(local) {
  const s = easeOutBack(local / 0.5);
  const a = clamp01(local / 0.3);
  const title = `<g opacity="${a}" transform="translate(540 270) scale(${s.toFixed(3)}) translate(-540 -270)"><text x="540" y="250" text-anchor="middle" font-family="${FONT}" font-weight="800" font-size="150" fill="#FFFFFF" stroke="${NAVY}" stroke-width="10" paint-order="stroke">Góc <tspan fill="${YEL}">IoT</tspan></text><text x="540" y="340" text-anchor="middle" font-family="${FONT}" font-weight="700" font-size="48" fill="${NAVY}">Theo dõi để không bỏ lỡ</text></g>`;
  const hx = [170, 930, 120, 970];
  let hearts = '';
  hx.forEach((x, i) => {
    const phase = (((local * 0.5 + i / 4) % 1) + 1) % 1;
    const y = 1120 - phase * 640;
    const op = Math.sin(Math.PI * phase);
    const sc = 0.5 + 0.25 * (i % 2);
    hearts += `<g opacity="${op.toFixed(2)}" transform="translate(${f1(x + 14 * Math.sin(local * 3 + i))} ${f1(y)}) scale(${sc})"><path d="M0 20 C-50 -30 -80 20 0 80 C80 20 50 -30 0 20 Z" fill="#FF5C7A" stroke="${NAVY}" stroke-width="7" stroke-linejoin="round" transform="translate(0 -50)"/></g>`;
  });
  const pulse = 1 + 0.05 * Math.sin(local * 6);
  const btn = local > 1.0 ? `<g opacity="${clamp01((local - 1.0) / 0.3).toFixed(2)}" transform="translate(540 1255) scale(${pulse.toFixed(3)})"><rect x="-210" y="-44" width="420" height="88" rx="44" fill="${YEL}" stroke="${NAVY}" stroke-width="6"/><text x="0" y="17" text-anchor="middle" font-family="${FONT}" font-weight="800" font-size="48" fill="${NAVY}">Theo dõi</text></g>` : '';
  return title + hearts + btn;
}


// ===== icon bổ sung =====
const iconTV = () => `<rect x="-64" y="-46" width="128" height="86" rx="12" fill="${NAVY}"/><rect x="-54" y="-36" width="108" height="66" rx="6" fill="#1B3358"/><path d="M-14 -20 L22 -3 L-14 14 Z" fill="${TEAL}"/><rect x="-26" y="44" width="52" height="10" rx="4" fill="#8A97A8"/>`;
const iconPurifier = () => `<rect x="-36" y="-62" width="72" height="124" rx="18" fill="#FFFFFF" stroke="${NAVY}" stroke-width="6"/><g stroke="#8A97A8" stroke-width="5" stroke-linecap="round"><line x1="-20" y1="-30" x2="20" y2="-30"/><line x1="-20" y1="-16" x2="20" y2="-16"/><line x1="-20" y1="-2" x2="20" y2="-2"/></g><circle cx="0" cy="30" r="9" fill="${TEAL}"/>`;
const iconRice = () => `<path d="M-52 -14 Q0 -80 52 -14 Z" fill="#FF8A5B" stroke="${NAVY}" stroke-width="6" stroke-linejoin="round"/><rect x="-52" y="-14" width="104" height="66" rx="20" fill="#FFFFFF" stroke="${NAVY}" stroke-width="6"/><circle cx="0" cy="-58" r="7" fill="${NAVY}"/><circle cx="0" cy="22" r="11" fill="${TEAL}"/>`;
const iconDoor = () => `<rect x="-42" y="-66" width="84" height="132" rx="8" fill="#FFB27A" stroke="${NAVY}" stroke-width="6"/><rect x="-30" y="-54" width="60" height="108" rx="4" fill="#FFD2AE"/><circle cx="20" cy="4" r="7" fill="${NAVY}"/>`;
const iconThermo = () => `<rect x="-14" y="-64" width="28" height="104" rx="14" fill="#FFFFFF" stroke="${NAVY}" stroke-width="6"/><circle cx="0" cy="44" r="24" fill="#FF5C5C" stroke="${NAVY}" stroke-width="6"/><rect x="-6" y="-24" width="12" height="70" rx="6" fill="#FF5C5C"/><g stroke="${NAVY}" stroke-width="4" stroke-linecap="round"><line x1="20" y1="-44" x2="34" y2="-44"/><line x1="20" y1="-24" x2="34" y2="-24"/><line x1="20" y1="-4" x2="34" y2="-4"/></g>`;
const iconDrop = () => `<path d="M0 -62 C40 -14 46 18 0 54 C-46 18 -40 -14 0 -62 Z" fill="#5CC8FF" stroke="${NAVY}" stroke-width="6" stroke-linejoin="round"/><path d="M-16 20 Q-12 34 2 38" stroke="#FFFFFF" stroke-width="6" fill="none" stroke-linecap="round"/>`;
const iconSun = () => { let r = ''; for (let i = 0; i < 8; i++) { const a = i * Math.PI / 4; r += `<line x1="${f1(Math.cos(a) * 42)}" y1="${f1(Math.sin(a) * 42)}" x2="${f1(Math.cos(a) * 62)}" y2="${f1(Math.sin(a) * 62)}"/>`; } return `<g stroke="#FFB300" stroke-width="8" stroke-linecap="round">${r}</g><circle cx="0" cy="0" r="30" fill="${YEL}" stroke="#FFB300" stroke-width="6"/>`; };
const iconMotion = () => `<g stroke="${NAVY}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round" fill="none"><path d="M-14 -16 L-14 22 M-14 -2 L10 8 M-14 22 L-30 54 M-14 22 L8 54"/></g><circle cx="-14" cy="-38" r="16" fill="#FFC9A8" stroke="${NAVY}" stroke-width="6"/><g stroke="${TEAL}" stroke-width="7" stroke-linecap="round" fill="none"><path d="M26 -30 Q38 -16 26 -2"/><path d="M40 -42 Q60 -16 40 10"/></g>`;
const iconRuler = () => `<rect x="-62" y="-20" width="124" height="40" rx="8" fill="${YEL}" stroke="${NAVY}" stroke-width="6"/><g stroke="${NAVY}" stroke-width="4" stroke-linecap="round"><line x1="-44" y1="-20" x2="-44" y2="0"/><line x1="-22" y1="-20" x2="-22" y2="-4"/><line x1="0" y1="-20" x2="0" y2="0"/><line x1="22" y1="-20" x2="22" y2="-4"/><line x1="44" y1="-20" x2="44" y2="0"/></g>`;
const iconEye = () => `<path d="M-62 0 Q0 -54 62 0 Q0 54 -62 0 Z" fill="#FFFFFF" stroke="${NAVY}" stroke-width="6" stroke-linejoin="round"/><circle cx="0" cy="0" r="24" fill="${TEAL}" stroke="${NAVY}" stroke-width="5"/><circle cx="0" cy="0" r="11" fill="${NAVY}"/><circle cx="6" cy="-7" r="5" fill="#FFFFFF"/>`;
const iconEyeX = () => `<g opacity="0.55">${iconEye()}</g><g stroke="#E5484D" stroke-width="12" stroke-linecap="round"><line x1="-48" y1="-48" x2="48" y2="48"/><line x1="48" y1="-48" x2="-48" y2="48"/></g>`;
const iconPerson = () => `<path d="M-38 56 Q-38 0 0 0 Q38 0 38 56 Z" fill="#FF8A5B" stroke="${NAVY}" stroke-width="6" stroke-linejoin="round"/><circle cx="0" cy="-30" r="24" fill="#FFC9A8" stroke="${NAVY}" stroke-width="6"/>`;
const iconQ = () => `<circle cx="0" cy="0" r="56" fill="${YEL}" stroke="${NAVY}" stroke-width="6"/><text x="0" y="30" text-anchor="middle" font-family="${FONT}" font-weight="800" font-size="86" fill="${NAVY}">?</text>`;
const iconFan = () => { let b = ''; for (let i = 0; i < 3; i++) b += `<ellipse cx="0" cy="-28" rx="16" ry="30" fill="#8FD3FF" stroke="${NAVY}" stroke-width="5" transform="rotate(${i * 120})"/>`; return `<circle r="62" fill="#FFFFFF" stroke="${NAVY}" stroke-width="6"/>${b}<circle r="10" fill="${NAVY}"/>`; };
const iconBell = () => `<path d="M-40 30 Q-40 -16 0 -34 Q40 -16 40 30 Z" fill="${YEL}" stroke="#FFB300" stroke-width="6" stroke-linejoin="round"/><rect x="-46" y="30" width="92" height="12" rx="6" fill="#FFB300"/><circle cx="0" cy="54" r="10" fill="#FFB300"/><circle cx="34" cy="-30" r="14" fill="#FF5C5C" stroke="#FFFFFF" stroke-width="4"/>`;
const iconBT = () => `<circle cx="0" cy="0" r="60" fill="#3B82F6" stroke="${NAVY}" stroke-width="6"/><path d="M-20 -30 L24 22 L2 44 L2 -44 L24 -22 L-20 30" fill="none" stroke="#FFFFFF" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>`;
const iconBat = (lv, col) => `<rect x="-56" y="-30" width="104" height="60" rx="10" fill="#FFFFFF" stroke="${NAVY}" stroke-width="6"/><rect x="48" y="-12" width="12" height="24" rx="4" fill="${NAVY}"/><rect x="-48" y="-22" width="${(88 * lv).toFixed(0)}" height="44" rx="5" fill="${col}"/>`;
const iconMesh = () => `<g stroke="${NAVY}" stroke-width="6" stroke-linecap="round"><line x1="0" y1="-40" x2="-46" y2="30"/><line x1="0" y1="-40" x2="46" y2="30"/><line x1="-46" y1="30" x2="46" y2="30"/></g><g fill="${TEAL}" stroke="${NAVY}" stroke-width="6"><circle cx="0" cy="-40" r="16"/><circle cx="-46" cy="30" r="16"/><circle cx="46" cy="30" r="16"/></g>`;
const iconCloud = () => `<path d="M-58 24 Q-72 -8 -38 -10 Q-32 -46 4 -42 Q34 -62 52 -26 Q82 -20 70 24 Z" fill="#FFFFFF" stroke="${NAVY}" stroke-width="6" stroke-linejoin="round"/>`;
const iconServer = () => [-48, -8, 32].map((y) => `<rect x="-58" y="${y}" width="116" height="34" rx="8" fill="${NAVY}"/><circle cx="-38" cy="${y + 17}" r="5" fill="#3DDC84"/><circle cx="-22" cy="${y + 17}" r="5" fill="${YEL}"/><line x1="8" y1="${y + 17}" x2="44" y2="${y + 17}" stroke="#8A97A8" stroke-width="5" stroke-linecap="round"/>`).join('');
const iconShield = () => `<path d="M0 -62 L52 -42 V8 Q52 46 0 66 Q-52 46 -52 8 V-42 Z" fill="${TEAL}" stroke="${NAVY}" stroke-width="6" stroke-linejoin="round"/><path d="M-22 4 L-6 22 L26 -14" fill="none" stroke="#FFFFFF" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>`;
const iconESP = () => `<rect x="-64" y="-36" width="128" height="72" rx="8" fill="${NAVY}"/><rect x="-24" y="-18" width="40" height="36" rx="4" fill="#C9D2DE"/><path d="M26 -22 H44 V-8 H32 V6 H50 V20" fill="none" stroke="${TEAL}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/><g fill="${YEL}">${[-48, -32, -16, 0, 16].map((x) => `<circle cx="${x}" cy="-28" r="3.5"/><circle cx="${x}" cy="28" r="3.5"/>`).join('')}</g>`;
const iconArduino = () => `<rect x="-66" y="-40" width="132" height="80" rx="12" fill="#1AA3A8" stroke="${NAVY}" stroke-width="6"/><rect x="-66" y="-22" width="30" height="34" rx="4" fill="#C9D2DE" stroke="${NAVY}" stroke-width="4"/><rect x="-12" y="-14" width="46" height="28" rx="4" fill="${NAVY}"/><g fill="${YEL}">${[-20, -4, 12, 28, 44].map((x) => `<rect x="${x}" y="-36" width="8" height="8" rx="2"/><rect x="${x}" y="28" width="8" height="8" rx="2"/>`).join('')}</g>`;
const ICONS = { bulb: iconBulb, camera: iconCamera, watch: iconWatch, chip: iconChip, wifi: iconWifiBig, plant: iconPlant, router: iconRouter, phone: () => `<g transform="scale(0.55)">${iconPhone()}</g>`, tv: iconTV, purifier: iconPurifier, rice: iconRice, door: iconDoor, thermo: iconThermo, drop: iconDrop, sun: iconSun, motion: iconMotion, ruler: iconRuler, eye: iconEye, eyex: iconEyeX, person: iconPerson, q: iconQ, fan: iconFan, bell: iconBell, bt: iconBT, batlow: () => iconBat(0.18, '#E5484D'), batfull: () => iconBat(1, '#3DDC84'), mesh: iconMesh, cloud: iconCloud, server: iconServer, shield: iconShield, esp: iconESP, arduino: iconArduino };

// ===== dựng cảnh theo lời đọc =====
const stripW = (w) => w.toLowerCase().replace(/[.,!?:;…]+/g, '');
function wordTimes(text, dur, key) {
  const ws = text.split(' ');
  if (key && ALIGN[key] && ALIGN[key].length === ws.length) return ALIGN[key];
  const total = ws.reduce((a, w) => a + w.length + 1, 0);
  const start = 0.25, span = Math.max(0.5, dur - 0.7);
  let cum = 0;
  return ws.map((w) => { const t = start + span * cum / total; cum += w.length + 1; return t; });
}
function buildGeneric(def, text, dur, key) {
  const ws = text.split(' ').map(stripW);
  const wt = wordTimes(text, dur, key);
  let from = 0;
  const items = (def.items || []).map((it) => {
    let k = 0;
    if (typeof it.w === 'string') {
      const a = stripW(it.w);
      let f = -1;
      for (let i = from; i < ws.length; i++) if (ws[i] === a || ws[i].startsWith(a)) { f = i; break; }
      if (f < 0) throw new Error('không thấy từ "' + it.w + '" trong: ' + text);
      k = f; from = f + (it.same ? 0 : 1);
    } else if (typeof it.w === 'number') k = it.w;
    const kk = it.k || 1;
    return Object.assign({}, it, { t: Math.max(0.1, wt[k] - 0.15), k: kk < 1.2 ? kk * 1.2 : kk, y: it.y < 500 && kk < 1.2 ? it.y + 40 : it.y });
  });
  const pts = [];
  items.forEach((it, i) => {
    if (it.p === false) return;
    const a = it.t + 0.25;
    let nxt = i + 1 < items.length ? items[i + 1].t : dur - 0.3;
    for (let j = i + 1; j < items.length; j++) if (items[j].p !== false) { nxt = items[j].t; break; }
    const b = Math.max(a + 0.9, Math.min(a + 2.0, nxt + 0.2));
    pts.push({ a, b, x: it.x, y: it.y - (it.pyoff || 0) });
  });
  return { items, pts };
}
function itemSVG(it, local) {
  if (it.hide) return '';
  const k = it.k || 1;
  if (it.pill) {
    const w = it.pill.length * 30 + 70;
    return at(it.x, it.y, k, local, it.t, `<rect x="${-w / 2}" y="-44" width="${w}" height="88" rx="44" fill="${NAVY}"/><text x="0" y="20" text-anchor="middle" font-family="${FONT}" font-weight="800" font-size="54" fill="${YEL}">${esc(it.pill)}</text>`);
  }
  const lab = (it.label || '').split('|').map((l, i) => `<text x="0" y="${166 + i * 46}" text-anchor="middle" font-family="${FONT}" font-weight="700" font-size="42" fill="${NAVY}">${esc(l)}</text>`).join('');
  return at(it.x, it.y, k, local, it.t, `<circle cx="0" cy="0" r="110" fill="#FFFFFF" stroke="${NAVY}" stroke-width="6"/><g transform="scale(${it.ik || 1.1})">${ICONS[it.ic]()}</g>${lab}`);
}
function gfxGen(local, sc) {
  if (process.env.DBG) console.error("gen", local.toFixed(2), JSON.stringify(sc.gen.items.map(i=>[i.ic,i.t.toFixed(2)])));
  const d = sc.gen;
  let out = '';
  if (d.title) {
    out += at(540, 100, 1, local, d.titleT || 0.3, `<text x="0" y="22" text-anchor="middle" font-family="${FONT}" font-weight="800" font-size="${d.titleSize || 64}" fill="#FFFFFF" stroke="${NAVY}" stroke-width="8" paint-order="stroke">${esc(d.title)}</text>`);
  }
  let links = '', dots = '';
  (d.links || []).forEach((l, n) => {
    const A = d.items[l[0]], B = d.items[l[1]];
    const t0 = Math.max(A.t, B.t) + 0.5;
    if (local < t0) return;
    links += `<line x1="${A.x}" y1="${A.y}" x2="${B.x}" y2="${B.y}" stroke="#FFFFFF" stroke-opacity="0.5" stroke-width="5" stroke-dasharray="14 16" stroke-linecap="round"/>`;
    for (let i = 0; i < 2; i++) {
      const u = (((local - t0) * 0.6 + i * 0.5 + n * 0.2) % 1);
      dots += `<circle cx="${f1(lerp(A.x, B.x, u))}" cy="${f1(lerp(A.y, B.y, u))}" r="10" fill="#FFFFFF"/>`;
    }
  });
  let hl = '';
  d.items.forEach((it) => {
    if (it.pill || it.hide || it.p === false) return;
    const u = (local - it.t - 0.25) / 1.4;
    if (u > 0 && u < 1) hl += `<circle cx="${it.x}" cy="${it.y}" r="${f1(125 * (it.k || 1) * (1.05 + 0.25 * u))}" fill="none" stroke="${YEL}" stroke-width="${f1(10 * (1 - u) + 2)}" stroke-opacity="${(0.9 * (1 - u)).toFixed(2)}"/>`;
  });
  const an = d.anim && ANIMS[d.anim] ? ANIMS[d.anim](local, d.items) : '';
  return `<g transform="translate(${CT.cx} ${CT.cy}) scale(${CT.sg}) translate(-540 -${CT.ay})">${links + out + an + d.items.map((it) => itemSVG(it, local)).join('') + hl + dots}</g>`;
}
function qBubbles(local, t1, t2) {
  const s = easeOutBack(local / 0.5), a = clamp01(local / 0.3);
  const title = `<g opacity="${a}" transform="translate(540 240) scale(${s.toFixed(3)}) translate(-540 -240)"><text x="540" y="240" text-anchor="middle" font-family="${FONT}" font-weight="800" font-size="${Math.min(110, Math.floor(950 / (t1.length * 0.56)))}" fill="${YEL}" stroke="${NAVY}" stroke-width="10" paint-order="stroke">${esc(t1)}</text><text x="540" y="330" text-anchor="middle" font-family="${FONT}" font-weight="700" font-size="${Math.min(52, Math.floor(980 / (t2.length * 0.55)))}" fill="#FFFFFF" stroke="${NAVY}" stroke-width="8" paint-order="stroke">${esc(t2)}</text></g>`;
  return title + onlyBubbles(local);
}

function gfx(kind, local, t, sc) {
  if (kind === 'gen') return gfxGen(local, sc);
  if (kind === 'q') return qBubbles(local, sc.q[0], sc.q[1]);
  if (kind === 's1') return gfxS1(local);
  if (kind === 'hello') return gfxHello(local);
  if (kind === 's3') return gfxS3(local);
  if (kind === 's4') return gfxS4(local);
  if (kind === 'curious') return gfxCurious(local, t);
  if (kind === 'end') return gfxEnd(local);
  return '';
}

function armPose(side, local, pts, lay, bounce) {
  const S = side < 0 ? [350, 495] : [450, 495];
  let best = null, bw = 0;
  for (const p of pts) {
    if ((p.x < (lay.corner ? 540 + (lay.ox || 0) : 480)) !== (side < 0)) continue;
    const w = smooth((local - p.a) / 0.3) * (1 - smooth((local - p.b) / 0.3));
    if (w > bw) { bw = w; best = p; }
  }
  if (!best || bw < 0.001) return { w: 0 };
  const tx = (best.x - (540 + (lay.ox || 0))) / lay.s + 400, ty = (best.y - (lay.cy + (lay.oy || 0) + bounce)) / lay.s + 400;
  const vx = tx - S[0], vy = ty - S[1];
  const dist = Math.hypot(vx, vy);
  let d = [vx / dist + side * 0.7 * Math.min(1, 260 / dist), vy / dist];
  const dl = Math.hypot(d[0], d[1]); d = [d[0] / dl, d[1] / dl];
  const reach = Math.min(lay.corner ? 340 : 300, Math.max(180, dist - 90)) + 8 * Math.sin((local - best.a) * 9) * bw;
  const H = [S[0] + d[0] * reach, S[1] + d[1] * reach];
  let pp = [d[1], -d[0]];
  if (pp[0] * side < 0) pp = [-pp[0], -pp[1]];
  const C = [(S[0] + H[0]) / 2 + pp[0] * 22, (S[1] + H[1]) / 2 + pp[1] * 22];
  return { w: bw, H, C, d };
}

function bong(t, wave, lay, glow, pts, local) {
  const wp = t * Math.PI * 2 * 1.6;
  const amp = wave ? 1 : 0.35;
  const dx = 18 * Math.sin(wp) * amp;
  const dy = -8 * Math.abs(Math.sin(wp)) * amp;
  const arcOp = wave ? 0.45 + 0.55 * Math.abs(Math.sin(wp)) : 0;
  const kick = Math.sin(t * Math.PI * 2 * 1.2) * 10;
  const kx = 495 + kick, ky = 625 - Math.abs(kick) * 0.5;
  const bp = t % 3.2;
  let b = 1;
  if (bp < 0.16) b = Math.max(0.08, Math.abs(bp - 0.08) / 0.08);
  const m = 0.3 + 0.7 * Math.abs(Math.sin(t * 8.5) * Math.sin(t * 2.9 + 1));
  const px = 3 * Math.sin(t * 0.9);
  const rayOp = 0.55 + 0.45 * Math.sin(t * 3);
  const hop = Math.abs(Math.sin(t * Math.PI * 1.4));
  const ox = lay.ox || 0, vel = lay.vel || 0, sp = Math.min(1, Math.abs(vel) / 260);
  const jump = lay.jump || 0;
  const oy = lay.oy || 0, rot = lay.rot || 0;
  const cyy = lay.cy + oy;
  const bounce = (-22 * hop - 30 * sp * hop - 90 * jump) * (lay.s / 1.25);
  const sc = lay.s;
  const aL = armPose(-1, local, pts, lay, bounce), aR = armPose(1, local, pts, lay, bounce);
  const mix = (a, b, w) => [lerp(a[0], b[0], w), lerp(a[1], b[1], w)];
  const restLH = [340, 582], restLC = [270, 540];
  const rEnd = [572 + dx, 372 + dy], restRC = [570, 470], restRG = [576 + dx, 360 + dy];
  const lH = aL.w ? mix(restLH, aL.H, aL.w) : restLH, lC = aL.w ? mix(restLC, aL.C, aL.w) : restLC;
  const rH = aR.w ? mix(rEnd, aR.H, aR.w) : rEnd, rC = aR.w ? mix(restRC, aR.C, aR.w) : restRC;
  const rG = aR.w ? mix(restRG, aR.H, aR.w) : restRG;
  const finger = (a) => a.w > 0.05 ? `<line x1="${a.H[0].toFixed(1)}" y1="${a.H[1].toFixed(1)}" x2="${(a.H[0] + a.d[0] * 64 * a.w).toFixed(1)}" y2="${(a.H[1] + a.d[1] * 64 * a.w).toFixed(1)}" stroke="${NAVY}" stroke-width="26" stroke-linecap="round"/><line x1="${a.H[0].toFixed(1)}" y1="${a.H[1].toFixed(1)}" x2="${(a.H[0] + a.d[0] * 64 * a.w).toFixed(1)}" y2="${(a.H[1] + a.d[1] * 64 * a.w).toFixed(1)}" stroke="#FFFFFF" stroke-width="14" stroke-linecap="round"/>` : '';
  const wr = 1 - aR.w;
  const mouthBottom = 375 + 27.5 * m;
  const tongue = m > 0.55 ? `<ellipse cx="400" cy="${(mouthBottom - 9).toFixed(1)}" rx="14" ry="${(7 * m).toFixed(1)}" fill="#FF8A8A"/>` : '';
  const tr = `translate(${(540 + ox).toFixed(1)} ${cyy.toFixed(1)}) scale(${sc.toFixed(3)}) translate(-400 -400)`;
  const shadow = `<g transform="${tr}"><ellipse cx="425" cy="700" rx="${(110 - 16 * hop).toFixed(1)}" ry="14" fill="${NAVY}" fill-opacity="0.2"/></g>`;
  const glowEl = glow ? `<g transform="${tr}"><circle cx="400" cy="330" r="${(215 + 22 * Math.sin(t * 3)).toFixed(1)}" fill="#FFF6C2" fill-opacity="0.32"/></g>` : '';
  const tilt = Math.max(-14, Math.min(14, vel * 0.05)) + 3 * Math.sin(t * 5) * sp;
  const feetY = cyy + 300 * sc;
  const sq = Math.max(0, 1 - hop) ** 3, sy = 1 - 0.08 * sq + 0.05 * hop * (1 + sp), sx = 1 / sy;
  const fx = 540 + ox;
  const dust = [0, 1, 2].map((k) => { const ph = (t * 2.2 + k / 3) % 1; const dir = vel >= 0 ? -1 : 1; return sp > 0.15 ? `<circle cx="${(540 + ox + dir * (30 + ph * 90)).toFixed(1)}" cy="${(feetY - 10 - ph * 40).toFixed(1)}" r="${(10 + ph * 26) * sc}" fill="#FFFFFF" fill-opacity="${((1 - ph) * 0.4 * sp).toFixed(2)}"/>` : ''; }).join('');
  const lines = sp > 0.3 ? [0, 1, 2].map((k) => { const dir = vel >= 0 ? -1 : 1; const y = lay.cy - 120 + k * 90; return `<line x1="${(540 + ox + dir * 190 * sc).toFixed(1)}" y1="${y}" x2="${(540 + ox + dir * (190 + 90 * sp) * sc).toFixed(1)}" y2="${y}" stroke="#FFFFFF" stroke-opacity="0.55" stroke-width="8" stroke-linecap="round"/>`; }).join('') : '';
  const body = dust + lines + `<g transform="rotate(${rot.toFixed(1)} ${fx.toFixed(1)} ${(cyy + bounce).toFixed(1)})"><g transform="translate(${fx.toFixed(1)} ${feetY.toFixed(1)}) scale(${sx.toFixed(3)} ${sy.toFixed(3)}) translate(${(-fx).toFixed(1)} ${(-feetY).toFixed(1)})">
<g transform="rotate(${tilt.toFixed(2)} ${(540 + ox).toFixed(1)} ${feetY.toFixed(1)}) translate(${(540 + ox).toFixed(1)} ${(cyy + bounce).toFixed(1)}) scale(${sc.toFixed(3)}) translate(-400 -400)" fill="none">
<g stroke="#FFFFFF" stroke-width="10" stroke-linecap="round" stroke-opacity="${rayOp.toFixed(2)}">
<line x1="400" y1="150" x2="400" y2="116"/><line x1="269" y1="199" x2="246" y2="176"/>
<line x1="531" y1="199" x2="554" y2="176"/><line x1="215" y1="330" x2="183" y2="330"/></g>
<g stroke="${NAVY}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round">
<path d="M378 575 Q365 620 350 655"/>
<path d="M422 575 Q450 615 ${kx.toFixed(1)} ${ky.toFixed(1)}"/>
<path d="M350 495 Q${lC[0].toFixed(1)} ${lC[1].toFixed(1)} ${lH[0].toFixed(1)} ${lH[1].toFixed(1)}"/>
<path d="M450 495 Q${rC[0].toFixed(1)} ${rC[1].toFixed(1)} ${rH[0].toFixed(1)} ${rH[1].toFixed(1)}"/></g>
${finger(aL)}${finger(aR)}
<ellipse cx="340" cy="668" rx="36" ry="20" fill="#FF8A5B" stroke="${NAVY}" stroke-width="6"/>
<path d="M312 672 Q340 684 368 672" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round"/>
<g transform="rotate(-25 ${(kx + 15).toFixed(1)} ${(ky + 5).toFixed(1)})">
<ellipse cx="${(kx + 15).toFixed(1)}" cy="${(ky + 5).toFixed(1)}" rx="36" ry="20" fill="#FF8A5B" stroke="${NAVY}" stroke-width="6"/>
<path d="M${(kx - 13).toFixed(1)} ${(ky + 9).toFixed(1)} Q${(kx + 15).toFixed(1)} ${(ky + 21).toFixed(1)} ${(kx + 43).toFixed(1)} ${(ky + 9).toFixed(1)}" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round"/></g>
<rect x="350" y="465" width="100" height="60" rx="16" fill="#C9D2DE" stroke="#8A97A8" stroke-width="8"/>
<line x1="360" y1="487" x2="440" y2="487" stroke="#8A97A8" stroke-width="5" stroke-linecap="round"/>
<line x1="360" y1="507" x2="440" y2="507" stroke="#8A97A8" stroke-width="5" stroke-linecap="round"/>
<rect x="362" y="525" width="76" height="34" rx="14" fill="#8A97A8"/>
<rect x="378" y="559" width="44" height="18" rx="9" fill="#6B7788"/>
<circle cx="400" cy="330" r="150" fill="${YEL}" stroke="#FFB300" stroke-width="10"/>
<path d="M290 262 Q300 226 335 206" stroke="#FFF6C2" stroke-width="14" stroke-linecap="round" stroke-opacity="0.85"/>
<ellipse cx="360" cy="320" rx="30" ry="${(30 * b).toFixed(1)}" fill="#FFFFFF" stroke="#5A3E00" stroke-width="5"/>
<ellipse cx="440" cy="320" rx="30" ry="${(30 * b).toFixed(1)}" fill="#FFFFFF" stroke="#5A3E00" stroke-width="5"/>
<ellipse cx="${(367 + px).toFixed(1)}" cy="324" rx="14" ry="${(14 * b).toFixed(1)}" fill="#5A3E00"/>
<ellipse cx="${(447 + px).toFixed(1)}" cy="324" rx="14" ry="${(14 * b).toFixed(1)}" fill="#5A3E00"/>
${b > 0.5 ? `<circle cx="${(372 + px).toFixed(1)}" cy="317" r="5" fill="#FFFFFF"/><circle cx="${(452 + px).toFixed(1)}" cy="317" r="5" fill="#FFFFFF"/>` : ''}
<path d="M335 282 Q360 268 385 282" stroke="#5A3E00" stroke-width="7" stroke-linecap="round"/>
<path d="M415 282 Q440 268 465 280" stroke="#5A3E00" stroke-width="7" stroke-linecap="round"/>
<ellipse cx="322" cy="366" rx="18" ry="11" fill="#FF9E9E"/>
<ellipse cx="478" cy="366" rx="18" ry="11" fill="#FF9E9E"/>
<path d="M365 375 Q400 ${(375 + 55 * m).toFixed(1)} 435 375 Z" fill="#8B2E2E" stroke="#5A3E00" stroke-width="6" stroke-linejoin="round"/>
${tongue}
<circle cx="${lH[0].toFixed(1)}" cy="${lH[1].toFixed(1)}" r="24" fill="#FFFFFF" stroke="${NAVY}" stroke-width="6"/>
<circle cx="${rG[0].toFixed(1)}" cy="${rG[1].toFixed(1)}" r="26" fill="#FFFFFF" stroke="${NAVY}" stroke-width="6"/>
<circle cx="${(602 + dx).toFixed(1)}" cy="${(352 + dy).toFixed(1)}" r="10" fill="#FFFFFF" stroke="${NAVY}" stroke-width="5" opacity="${wr.toFixed(2)}"/>
<g opacity="${(arcOp * wr).toFixed(2)}" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round">
<path d="M614 332 Q632 346 628 374"/><path d="M632 314 Q662 342 652 382"/></g>
<path d="M250 410 L256 428 L274 434 L256 440 L250 458 L244 440 L226 434 L244 428 Z" fill="#FFFFFF" fill-opacity="${(0.5 + 0.5 * Math.sin(t * 4)).toFixed(2)}"/>
<path d="M590 485 L594 497 L606 501 L594 505 L590 517 L586 505 L574 501 L586 497 Z" fill="#FFFFFF" fill-opacity="${(0.5 + 0.5 * Math.sin(t * 4 + 2)).toFixed(2)}"/>
</g></g></g>`;
  let burst = '';
  for (const p of pts) {
    const q = local - p.a;
    if (q < 0 || q > 0.6) continue;
    const k = q / 0.6;
    for (let j = 0; j < 7; j++) {
      const ang = j / 7 * Math.PI * 2 + 0.4, r = 30 + 90 * k, sz = 14 * (1 - k);
      const cx = p.x + Math.cos(ang) * r, cy = p.y + Math.sin(ang) * r;
      burst += `<path d="M${cx} ${cy - sz} L${cx + sz * 0.3} ${cy - sz * 0.3} L${cx + sz} ${cy} L${cx + sz * 0.3} ${cy + sz * 0.3} L${cx} ${cy + sz} L${cx - sz * 0.3} ${cy + sz * 0.3} L${cx - sz} ${cy} L${cx - sz * 0.3} ${cy - sz * 0.3} Z" fill="${j % 2 ? '#FFFFFF' : YEL}" fill-opacity="${(1 - k).toFixed(2)}"/>`;
    }
  }
  return shadow + glowEl + body + burst;
}

function subtitle(fullText, local, dur, key) {
  // Cụm ngắn (tối đa 2 dòng); từng từ chỉ hiện khi được đọc tới. Vị trí chữ cố định nên không bị nhảy.
  const fw = fullText.split(' ');
  const ftotal = fw.reduce((s, w) => s + w.length + 1, 0);
  const fspan = Math.max(0.5, dur - 0.7);
  let fc = 0;
  let ft = fw.map((w) => { const t0 = 0.25 + fspan * fc / ftotal; fc += w.length + 1; return t0; });
  if (key && ALIGN[key] && ALIGN[key].length === fw.length) ft = ALIGN[key];
  const chunks = [];
  let cur = [];
  fw.forEach((w, k) => {
    const joined = cur.concat([w]).join(' ');
    if (cur.length && wrap(joined, 27).length > 2) { chunks.push(cur); cur = []; }
    cur.push(w);
    const len = cur.join(' ').length;
    if (/[,;:.!?…]$/.test(w) && (len >= 20 || /[.!?…]$/.test(w))) { chunks.push(cur); cur = []; }
  });
  if (cur.length) chunks.push(cur);
  let pos = 0;
  const info = chunks.map((c) => { const o = { words: c, from: pos }; pos += c.length; return o; });
  let curK = -1;
  for (let k = 0; k < fw.length; k++) if (local >= ft[k]) curK = k;
  if (curK < 0) return '';
  const ch = info.find((c) => curK >= c.from && curK < c.from + c.words.length);
  const lines = wrap(ch.words.join(' '), 27);
  const lh = 74, pad = 24;
  const boxH = lines.length * lh + pad * 2;
  const top = 1620 - boxH;
  const a = clamp01((local - ft[ch.from]) / 0.15 + 0.3);
  let idx = ch.from;
  const tx = lines.map((l, i) => {
    const spans = l.split(' ').map((w) => {
      const k = idx++;
      const shown = local >= ft[k];
      const isCur = k === curK;
      return `<tspan fill="${isCur ? YEL : '#FFFFFF'}" fill-opacity="${shown ? 1 : 0}">${esc(w)}</tspan>`;
    }).join(' ');
    return `<text x="540" y="${top + pad + i * lh + 54}" text-anchor="middle" font-family="${FONT}" font-weight="700" font-size="56">${spans}</text>`;
  }).join('\n');
  return `<g opacity="${a.toFixed(2)}"><rect x="50" y="${top}" width="980" height="${boxH}" rx="36" fill="${NAVY}" fill-opacity="0.92"/>${tx}</g>`;
}

const oxMemo = {};
function oxAt(idx, local) {
  const sc = scenes[idx];
  if (sc.mode === 'corner') {
    const start0 = idx > 0 ? oxEnd(idx - 1) : 0, tgt = (idx % 2 ? 1 : -1) * 355;
    return lerp(start0, tgt, smooth(local / 0.8)) + 10 * Math.sin(local * 1.7 + idx);
  }
  const pts = (sc.pts || []).slice().sort((a, b) => a.a - b.a);
  const start = idx > 0 ? oxEnd(idx - 1) : 0;
  const kf = [[0, start]];
  if (!pts.length) kf.push([0.9, (idx % 2 ? 1 : -1) * 190]);
  else {
    let lastT = 0;
    for (const p of pts) {
      const tt = Math.max(lastT + 0.25, p.a + 0.15);
      kf.push([tt, Math.max(-300, Math.min(300, (p.x - 540) * 0.6))]);
      lastT = tt;
    }
    kf.push([Math.max(lastT + 0.6, pts[pts.length - 1].b + 0.6), (idx % 2 ? 1 : -1) * 120]);
  }
  let v = kf[kf.length - 1][1];
  if (local <= 0) v = kf[0][1];
  else for (let i = 0; i < kf.length - 1; i++) if (local < kf[i + 1][0]) { v = lerp(kf[i][1], kf[i + 1][1], smooth((local - kf[i][0]) / (kf[i + 1][0] - kf[i][0]))); break; }
  return v + 22 * Math.sin(local * 1.7 + idx);
}
function oxEnd(idx) {
  if (oxMemo[idx] === undefined) oxMemo[idx] = oxAt(idx, scenes[idx].t1 - scenes[idx].t0);
  return oxMemo[idx];
}

function layoutAt(t, idx, local) {
  const c = LAY[scenes[idx].mode];
  if (idx > 0 && local < 0.6) {
    const p = LAY[scenes[idx - 1].mode];
    const k = smooth(local / 0.6);
    return { cy: lerp(p.cy, c.cy, k), s: lerp(p.s, c.s, k) };
  }
  return { cy: c.cy, s: c.s };
}



// ===== icon cho loạt an toàn và bảo mật =====
const RED = '#E5484D';
const slash = (r = 50) => `<line x1="${-r}" y1="${-r}" x2="${r}" y2="${r}" stroke="${RED}" stroke-width="12" stroke-linecap="round"/>`;
const iconLock = () => `<path d="M-26 -4 V-26 Q-26 -58 0 -58 Q26 -58 26 -26 V-4" fill="none" stroke="${NAVY}" stroke-width="11" stroke-linecap="round"/><rect x="-46" y="-6" width="92" height="68" rx="14" fill="${YEL}" stroke="${NAVY}" stroke-width="6"/><circle cx="0" cy="22" r="9" fill="${NAVY}"/><rect x="-4" y="28" width="8" height="20" rx="3" fill="${NAVY}"/>`;
const iconBug = () => `<g stroke="${NAVY}" stroke-width="6" stroke-linecap="round">${[-22, 0, 22].map((y) => `<line x1="-30" y1="${y}" x2="-56" y2="${y - 8}"/><line x1="30" y1="${y}" x2="56" y2="${y - 8}"/>`).join('')}</g><ellipse cx="0" cy="8" rx="34" ry="42" fill="${RED}" stroke="${NAVY}" stroke-width="6"/><circle cx="0" cy="-40" r="18" fill="${NAVY}"/><circle cx="-7" cy="-42" r="5" fill="#FFFFFF"/><circle cx="7" cy="-42" r="5" fill="#FFFFFF"/><line x1="0" y1="-30" x2="0" y2="52" stroke="${NAVY}" stroke-width="5"/>`;
const iconUpdate = () => `<g fill="none" stroke="${NAVY}" stroke-width="10" stroke-linecap="round"><path d="M-40 -8 A42 42 0 0 1 30 -30"/><path d="M40 8 A42 42 0 0 1 -30 30"/></g><path d="M16 -52 L44 -30 L10 -20 Z" fill="${NAVY}"/><path d="M-16 52 L-44 30 L-10 20 Z" fill="${NAVY}"/><circle cx="0" cy="0" r="12" fill="${TEAL}"/>`;
const iconUpdateX = () => `<g opacity="0.55">${iconUpdate()}</g>${slash(52)}`;
const iconReset = () => `<path d="M36 -26 A46 46 0 1 0 46 10" fill="none" stroke="${NAVY}" stroke-width="11" stroke-linecap="round"/><path d="M52 -52 L52 -12 L14 -28 Z" fill="${NAVY}"/><circle cx="0" cy="0" r="12" fill="${YEL}" stroke="${NAVY}" stroke-width="4"/>`;
const iconHouse = () => `<g transform="scale(0.4) translate(0 -10)">${house(false, 0)}</g>`;
const iconBedX = () => `<g opacity="0.8"><rect x="-56" y="-2" width="112" height="34" rx="8" fill="#8FD3FF" stroke="${NAVY}" stroke-width="6"/><rect x="-56" y="-34" width="14" height="66" rx="6" fill="${NAVY}"/><rect x="-36" y="-14" width="36" height="20" rx="9" fill="#FFFFFF" stroke="${NAVY}" stroke-width="4"/><rect x="-52" y="32" width="10" height="14" fill="${NAVY}"/><rect x="42" y="32" width="10" height="14" fill="${NAVY}"/></g><circle cx="0" cy="0" r="62" fill="none" stroke="${RED}" stroke-width="10"/>${slash(44)}`;
const iconList = () => `<rect x="-54" y="-62" width="108" height="124" rx="14" fill="#FFFFFF" stroke="${NAVY}" stroke-width="6"/>${[-36, -6].map((y) => `<circle cx="-30" cy="${y}" r="9" fill="${NAVY}"/><line x1="-12" y1="${y}" x2="38" y2="${y}" stroke="#8A97A8" stroke-width="7" stroke-linecap="round"/>`).join('')}<circle cx="-30" cy="26" r="9" fill="${NAVY}"/><g stroke="${RED}" stroke-width="9" stroke-linecap="round"><line x1="-6" y1="14" x2="18" y2="38"/><line x1="18" y1="14" x2="-6" y2="38"/></g>`;
const iconNoCopy = () => `<rect x="-48" y="-44" width="62" height="78" rx="10" fill="#FFFFFF" stroke="${NAVY}" stroke-width="6"/><rect x="-14" y="-22" width="62" height="78" rx="10" fill="#FFFFFF" stroke="${NAVY}" stroke-width="6"/><line x1="-4" y1="-4" x2="38" y2="-4" stroke="#8A97A8" stroke-width="6" stroke-linecap="round"/><line x1="-4" y1="14" x2="38" y2="14" stroke="#8A97A8" stroke-width="6" stroke-linecap="round"/>${slash(56)}`;
Object.assign(ICONS, { lock: iconLock, bug: iconBug, update: iconUpdate, updx: iconUpdateX, reset: iconReset, house: iconHouse, bedx: iconBedX, list: iconList, nocopy: iconNoCopy });

const iconKey = () => `<circle cx="-22" cy="-6" r="28" fill="${YEL}" stroke="${NAVY}" stroke-width="7"/><circle cx="-22" cy="-6" r="9" fill="${NAVY}"/><rect x="2" y="-14" width="62" height="16" rx="6" fill="${YEL}" stroke="${NAVY}" stroke-width="6"/><rect x="40" y="2" width="12" height="22" rx="3" fill="${NAVY}"/><rect x="56" y="2" width="10" height="16" rx="3" fill="${NAVY}"/>`;
const iconScramble = () => `<rect x="-62" y="-44" width="124" height="88" rx="14" fill="#FFFFFF" stroke="${NAVY}" stroke-width="6"/><text x="0" y="14" text-anchor="middle" font-family="${FONT}" font-weight="800" font-size="46" fill="${NAVY}">#@%&amp;</text>`;
Object.assign(ICONS, { key: iconKey, scramble: iconScramble });


// ===== hoạt họa minh họa cho từng ví dụ =====
const guessStr = (seed) => { const ch = 'abcdefghjkmnpqrstuvwxyz23456789'; let x = (seed * 9301 + 49297) % 233280, o = ''; for (let i = 0; i < 6; i++) { x = (x * 9301 + 49297) % 233280; o += ch[x % ch.length]; } return o; };
const ringsAt = (cx, cy, r0, r1, per, t, n, col, op) => { let o = ''; for (let k = 0; k < n; k++) { const ph = ((t / per) + k / n) % 1; const r = r0 + (r1 - r0) * ph; o += `<circle cx="${cx}" cy="${cy}" r="${r.toFixed(1)}" fill="none" stroke="${col}" stroke-width="8" stroke-opacity="${((1 - ph) * op).toFixed(2)}"/>`; } return o; };
const ANIMS = {
  cmdflow(local, it) {
    const t = local - it[0].t - 0.3; if (t < 0) return '';
    const pts = [[210, 190], [540, 190], [870, 190]]; let o = '';
    for (let k = 0; k < 2; k++) {
      const u = ((t * 0.25) + k / 2) % 1, seg = u < 0.5 ? 0 : 1, v = (u % 0.5) / 0.5;
      const x = lerp(pts[seg][0], pts[seg + 1][0], v);
      o += `<g transform="translate(${x.toFixed(1)} 190)"><rect x="-26" y="-18" width="52" height="36" rx="10" fill="${YEL}" stroke="${NAVY}" stroke-width="4"/><text x="0" y="8" text-anchor="middle" font-family="${FONT}" font-weight="800" font-size="22" fill="${NAVY}">BẬT</text></g>`;
    }
    return o;
  },
  blocked(local, it) {
    const t = local - it[1].t - 0.3; if (t < 0) return '';
    const u = (t * 0.45) % 1, x = u < 0.5 ? lerp(210, 470, u / 0.5) : lerp(470, 210, (u - 0.5) / 0.5);
    let o = `<g transform="translate(${x.toFixed(1)} 190)"><rect x="-26" y="-18" width="52" height="36" rx="10" fill="${YEL}" stroke="${NAVY}" stroke-width="4"/><text x="0" y="8" text-anchor="middle" font-family="${FONT}" font-weight="800" font-size="22" fill="${NAVY}">BẬT</text></g>`;
    if (u > 0.42 && u < 0.6) o += `<circle cx="540" cy="370" r="${(120 + 30 * (u - 0.42) / 0.18).toFixed(1)}" fill="none" stroke="${RED}" stroke-width="8" stroke-opacity="0.6"/>`;
    return o;
  },
  hot(local, it) {
    const t = local - it[0].t - 0.3; if (t < 0) return '';
    return ringsAt(540, 370, 120, 200, 1.6, t, 2, RED, 0.55);
  },
  swarm(local, it) {
    const t = local - it[1].t - 0.2; if (t < 0) return '';
    let o = '';
    for (let k = 0; k < 8; k++) {
      const u = ((t * 0.4) + k / 8) % 1, x = lerp(1010, 300, u), y = 150 + (k % 4) * 55 + 18 * Math.sin(u * 14 + k);
      o += `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="9" fill="${RED}" fill-opacity="${(0.9 - 0.4 * u).toFixed(2)}"/>`;
    }
    return o;
  },
  puff(local, it) {
    const t = local - it[1].t - 0.2; if (t < 0) return '';
    let o = '';
    for (let k = 0; k < 6; k++) {
      const u = ((t * 0.45) + k / 6) % 1, x = lerp(540, 870, u), y = 330 - 90 * u - 24 * Math.sin(u * 9 + k);
      o += `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="${(8 + 8 * u).toFixed(1)}" fill="#FFFFFF" fill-opacity="${(0.8 - 0.5 * u).toFixed(2)}"/>`;
    }
    return o;
  },
  shutter(local, it) {
    const t = local - it[1].t - 0.2; if (t < 0) return '';
    return ringsAt(540, 370, 100, 220, 1.2, t, 2, '#FFFFFF', 0.75);
  },
  rings1(local, it) {
    const t = local - it[0].t - 0.4; if (t < 0) return '';
    return `<clipPath id="c1"><rect x="0" y="150" width="1080" height="440"/></clipPath><g clip-path="url(#c1)">${ringsAt(210, 370, 130, 760, 2.4, t, 4, '#FFFFFF', 0.55)}</g>`;
  },
  packets(local, it) {
    const t = local - it[1].t - 0.3; if (t < 0) return '';
    let o = '';
    const x0 = 210, x1 = 870;
    for (let k = 0; k < 3; k++) {
      const u = ((t * 0.35) + k / 3) % 1, x = lerp(x0, x1, u);
      if (u < 0.22 || u > 0.78) o += `<g transform="translate(${x.toFixed(1)} 610)"><rect x="-34" y="-20" width="68" height="40" rx="12" fill="#FFFFFF" stroke="${NAVY}" stroke-width="4"/><text x="0" y="9" text-anchor="middle" font-family="${FONT}" font-weight="800" font-size="26" fill="${NAVY}">1 0 1</text></g>`;
      else { const y = 610 + 26 * Math.sin(u * 40); o += `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="11" fill="#FFFFFF"/><circle cx="${(x - 30).toFixed(1)}" cy="${(610 + 26 * Math.sin(u * 40 - 1.2)).toFixed(1)}" r="7" fill="#FFFFFF" fill-opacity="0.6"/>`; }
    }
    for (let k = 0; k < 2; k++) {
      const u = ((t * 0.35) + 0.15 + k / 2) % 1, x = lerp(x1, x0, u);
      if (u < 0.22 || u > 0.78) o += `<g transform="translate(${x.toFixed(1)} 690)"><rect x="-34" y="-20" width="68" height="40" rx="12" fill="${YEL}" stroke="${NAVY}" stroke-width="4"/><text x="0" y="9" text-anchor="middle" font-family="${FONT}" font-weight="800" font-size="26" fill="${NAVY}">0 1 1</text></g>`;
      else o += `<circle cx="${x.toFixed(1)}" cy="${(690 + 26 * Math.sin(u * 40)).toFixed(1)}" r="11" fill="${YEL}"/>`;
    }
    return o;
  },
  bands(local, it) {
    let o = '';
    const a = local - it[0].t - 0.3, b = local - it[1].t - 0.3, c = local - it[2].t - 0.3;
    if (a > 0) o += ringsAt(210, 370, 130, 270, 3.0, a, 2, '#FFFFFF', 0.6);
    if (b > 0) o += ringsAt(540, 370, 130, 190, 0.8, b, 2, YEL, 0.7);
    if (c > 0) {
      const ph = (c * 0.3) % 1, filled = 4 - Math.min(3, Math.floor(ph * 4));
      for (let i = 0; i < 4; i++) o += `<rect x="${812 + i * 34}" y="${215 - i * 16}" width="22" height="${16 + i * 16}" rx="5" fill="${i < filled ? '#FFFFFF' : NAVY}" fill-opacity="${i < filled ? 1 : 0.25}"/>`;
      o += `<circle cx="${(740 + 130 * ph).toFixed(1)}" cy="620" r="12" fill="${YEL}"/>`;
    }
    return o;
  },
  token(local, it) {
    const t = local - it[0].t - 0.3; if (t < 0) return '';
    const u = (t * 0.28) % 1, x = lerp(210, 870, u);
    const phase = u < 0.3 ? 0 : u < 0.78 ? 1 : 2;
    const txt = phase === 1 ? '#@%&' : 'Chào bạn';
    const fill = phase === 1 ? RED : phase === 2 ? '#3DDC84' : '#FFFFFF';
    const col = phase === 1 ? '#FFFFFF' : NAVY;
    return `<line x1="210" y1="170" x2="870" y2="170" stroke="#FFFFFF" stroke-opacity="0.35" stroke-width="5" stroke-dasharray="14 16"/><g transform="translate(${x.toFixed(1)} 170)"><rect x="-86" y="-30" width="172" height="60" rx="30" fill="${fill}" stroke="${NAVY}" stroke-width="5"/><text x="0" y="12" text-anchor="middle" font-family="${FONT}" font-weight="800" font-size="34" fill="${col}">${esc(txt)}</text></g>`;
  },
  guess(local, it) {
    let o = '';
    const a = local - it[0].t - 0.4, b = local - it[1].t - 0.4;
    if (a > 0) for (let i = 0; i < 3; i++) o += `<text x="250" y="${560 + i * 46}" text-anchor="middle" font-family="${FONT}" font-weight="700" font-size="34" fill="#FFFFFF" fill-opacity="${(0.85 - i * 0.2).toFixed(2)}">${guessStr(Math.floor(a * 14) + i * 7)}</text>`;
    if (b > 0) {
      o += `<text x="830" y="560" text-anchor="middle" font-family="${FONT}" font-weight="700" font-size="34" fill="#FFFFFF">${guessStr(Math.floor(b * 1.2))}</text>`;
      const blocked = (b % 2.4) > 1.0;
      o += `<text x="830" y="608" text-anchor="middle" font-family="${FONT}" font-weight="800" font-size="34" fill="${blocked ? RED : YEL}">${blocked ? 'Bị chặn' : 'chờ...'}</text>`;
    }
    return o;
  },
  sessions(local, it) {
    const t0 = it[1].t + 0.3; let o = '';
    const cols = ['#FF8A5B', '#7B61FF', '#3DDC84'];
    for (let i = 0; i < 3; i++) {
      const tt = local - (t0 + i * 0.7); if (tt < 0) continue;
      const s = easeOutBack(tt / 0.4), y = 300 + i * 90;
      o += `<g transform="translate(540 ${y}) scale(${s.toFixed(2)})"><text x="-108" y="10" font-family="${FONT}" font-weight="700" font-size="26" fill="#FFFFFF">Lần ${i + 1}</text><circle cx="-30" cy="0" r="22" fill="${cols[i]}" stroke="${NAVY}" stroke-width="5"/><rect x="-14" y="-6" width="52" height="12" rx="5" fill="${cols[i]}" stroke="${NAVY}" stroke-width="4"/><rect x="62" y="-20" width="44" height="40" rx="10" fill="${cols[i]}" stroke="${NAVY}" stroke-width="5"/><rect x="72" y="-34" width="24" height="22" rx="10" fill="none" stroke="${NAVY}" stroke-width="5"/></g>`;
    }
    return o;
  },
  pulses(local, it) {
    let o = '';
    const s = (i) => local - it[i].t - 0.4;
    if (s(0) > 0) o += `<circle cx="210" cy="370" r="${(130 + 8 * Math.sin(s(0) * 5)).toFixed(1)}" fill="none" stroke="${RED}" stroke-width="8" stroke-opacity="${(0.45 + 0.35 * Math.sin(s(0) * 5)).toFixed(2)}"/>`;
    if (s(1) > 0) o += `<circle cx="540" cy="370" r="${(130 + 8 * Math.sin(s(1) * 5)).toFixed(1)}" fill="none" stroke="#3DDC84" stroke-width="8" stroke-opacity="${(0.55 + 0.35 * Math.sin(s(1) * 5)).toFixed(2)}"/>`;
    if (s(2) > 0) o += `<g transform="translate(870 370) rotate(${(s(2) * 120).toFixed(1)})"><circle cx="0" cy="0" r="136" fill="none" stroke="#FFFFFF" stroke-width="8" stroke-dasharray="40 30" stroke-opacity="0.8"/></g>`;
    return o;
  },

  camflow(local, it) {
    const t = local - it[1].t - 0.2; if (t < 0) return '';
    let o = '';
    for (let k = 0; k < 3; k++) {
      const u = ((t * 0.3) + k / 3) % 1, x = lerp(210, 870, u);
      o += `<g transform="translate(${x.toFixed(1)} 190)"><rect x="-30" y="-22" width="60" height="44" rx="8" fill="#FFFFFF" stroke="${NAVY}" stroke-width="4"/><circle cx="-10" cy="-6" r="6" fill="${YEL}"/><path d="M-26 18 L-8 0 L4 12 L14 2 L26 18 Z" fill="#35C9B8"/></g>`;
    }
    const e = local - it[2].t - 0.3;
    if (e > 0) o += `<circle cx="870" cy="370" r="${(130 + 10 * Math.sin(e * 6)).toFixed(1)}" fill="none" stroke="${RED}" stroke-width="8" stroke-opacity="${(0.45 + 0.4 * Math.sin(e * 6)).toFixed(2)}"/>`;
    return o;
  },
  tries(local, it) {
    const t = local - it[0].t - 0.3; if (t < 0) return '';
    const words = ['1234', 'qwerty', 'admin', '0000', 'password', '123456', 'abc123', 'admin'];
    let o = '';
    for (const side of [0, 1]) {
      const idx = Math.floor(t * 6 + side * 3) % words.length, w = words[idx], hit = w === 'admin' || w === '123456';
      const x = side ? 880 : 200;
      o += `<g transform="translate(${x} 380)"><rect x="-110" y="-34" width="220" height="68" rx="34" fill="${hit ? RED : '#FFFFFF'}" stroke="${NAVY}" stroke-width="5"/><text x="0" y="12" text-anchor="middle" font-family="${FONT}" font-weight="800" font-size="36" fill="${hit ? '#FFFFFF' : NAVY}">${w}</text></g>`;
    }
    return o;
  },
  infect(local, it) {
    const t = local - it[0].t - 0.2; if (t < 0) return '';
    let o = `<text x="540" y="140" text-anchor="middle" font-family="${FONT}" font-weight="700" font-size="30" fill="#FFFFFF" fill-opacity="0.85">Bị chiếm quyền lần lượt</text>`;
    for (let i = 0; i < 11; i++) {
      const x = 130 + i * 82, bad = t * 3.2 > i + 1, sc = easeOutBack((t * 3 - i * 0.3) / 0.4);
      if (sc <= 0) continue;
      o += `<g transform="translate(${x} 205) scale(${sc.toFixed(2)})"><rect x="-27" y="-20" width="54" height="40" rx="9" fill="${bad ? RED : '#FFFFFF'}" stroke="${NAVY}" stroke-width="4"/><circle cx="0" cy="0" r="11" fill="${bad ? '#FFFFFF' : NAVY}"/></g>`;
    }
    return o;
  },
  strength(local, it) {
    const t = local - it[0].t - 0.2; if (t < 0) return '';
    const p = Math.min(1, t / 3.2), col = p < 0.34 ? RED : p < 0.7 ? YEL : '#3DDC84';
    const n = Math.round(p * 16);
    return `<text x="540" y="150" text-anchor="middle" font-family="${FONT}" font-weight="800" font-size="44" fill="#FFFFFF" stroke="${NAVY}" stroke-width="7" paint-order="stroke">${'•'.repeat(n)}</text><rect x="240" y="180" width="600" height="26" rx="13" fill="${NAVY}" fill-opacity="0.35"/><rect x="240" y="180" width="${(600 * p).toFixed(1)}" height="26" rx="13" fill="${col}"/>`;
  },
  progress(local, it) {
    const t = local - it[2].t - 0.2; if (t < 0) return '';
    const p = Math.min(1, (t * 0.35) % 1.3), done = p >= 1;
    return `<rect x="240" y="190" width="600" height="26" rx="13" fill="${NAVY}" fill-opacity="0.35"/><rect x="240" y="190" width="${(600 * Math.min(1, p)).toFixed(1)}" height="26" rx="13" fill="${done ? '#3DDC84' : YEL}"/><text x="540" y="172" text-anchor="middle" font-family="${FONT}" font-weight="800" font-size="30" fill="#FFFFFF" stroke="${NAVY}" stroke-width="6" paint-order="stroke">${done ? 'Đã cập nhật' : 'Đang cập nhật ' + Math.round(p * 100) + '%'}</text>`;
  },
  drain(local, it) {
    const t = local - it[0].t - 0.2; if (t < 0) return '';
    const p = Math.max(0, 1 - t / 3.4);
    return `<text x="540" y="140" text-anchor="middle" font-family="${FONT}" font-weight="800" font-size="34" fill="#FFFFFF" stroke="${NAVY}" stroke-width="6" paint-order="stroke">Hãng còn hỗ trợ</text><rect x="240" y="170" width="600" height="30" rx="15" fill="${NAVY}" fill-opacity="0.35"/><rect x="240" y="170" width="${(600 * p).toFixed(1)}" height="30" rx="15" fill="${p > 0.4 ? '#3DDC84' : RED}"/>`;
  },
  pulse2(local, it) {
    let o = '';
    const a = local - it[0].t - 0.4, b = local - it[1].t - 0.4;
    if (a > 0) o += ringsAt(300, 370, 125, 190, 1.4, a, 2, RED, 0.6);
    if (b > 0) o += ringsAt(780, 370, 125, 190, 1.4, b, 2, YEL, 0.6);
    return o;
  },
  wipe(local, it) {
    const t = local - it[0].t - 0.3; if (t < 0) return '';
    let o = '';
    for (let k = 0; k < 4; k++) {
      const u = ((t * 0.3) + k / 4) % 1, x = lerp(210, 540, u), op = 1 - smooth((u - 0.6) / 0.4);
      o += `<g opacity="${op.toFixed(2)}" transform="translate(${x.toFixed(1)} 690)"><rect x="-26" y="-18" width="52" height="36" rx="8" fill="#FFFFFF" stroke="${NAVY}" stroke-width="4"/></g>`;
    }
    const q = local - it[1].t - 0.3;
    if (q > 0) o += `<g transform="translate(540 370) rotate(${(q * 140).toFixed(1)})"><circle cx="0" cy="0" r="136" fill="none" stroke="#FFFFFF" stroke-width="8" stroke-dasharray="40 30" stroke-opacity="0.8"/></g>`;
    return o;
  },
  chips(local, it) {
    const t0 = it[0].t; if (local < t0) return '';
    const words = ['cam', 'mưa', 'sông', 'đèn', 'gió'];
    let o = `<text x="540" y="130" text-anchor="middle" font-family="${FONT}" font-weight="700" font-size="32" fill="#FFFFFF" fill-opacity="0.85">Ví dụ cụm từ</text>`;
    words.forEach((w, i) => {
      const tt = local - (t0 + 0.2 + i * 0.35); if (tt < 0) return;
      const sc = easeOutBack(tt / 0.4), x = 540 + (i - 2) * 138;
      o += `<g transform="translate(${x} 210) scale(${sc.toFixed(2)})"><rect x="-58" y="-34" width="116" height="68" rx="34" fill="#FFFFFF" stroke="${NAVY}" stroke-width="6"/><text x="0" y="12" text-anchor="middle" font-family="${FONT}" font-weight="800" font-size="36" fill="${NAVY}">${w}</text></g>`;
    });
    return o;
  },
};

const X3 = [210, 540, 870], X4 = [165, 420, 675, 930], X5 = [120, 330, 540, 750, 960];
const E = { mode: 'big', glow: true, wave: true, kind: 'end' };
const Q = (a, b) => ({ mode: 'big', glow: true, wave: false, kind: 'q', q: [a, b] });
const iconBed = () => `<rect x="-56" y="-2" width="112" height="34" rx="8" fill="#8FD3FF" stroke="${NAVY}" stroke-width="6"/><rect x="-56" y="-34" width="14" height="66" rx="6" fill="${NAVY}"/><rect x="-36" y="-14" width="36" height="20" rx="9" fill="#FFFFFF" stroke="${NAVY}" stroke-width="4"/><rect x="-52" y="32" width="10" height="14" fill="${NAVY}"/><rect x="42" y="32" width="10" height="14" fill="${NAVY}"/>`;
const iconCloudX = () => `${iconCloud()}<g stroke="${RED}" stroke-width="12" stroke-linecap="round"><line x1="-22" y1="-14" x2="22" y2="30"/><line x1="22" y1="-14" x2="-22" y2="30"/></g>`;
const iconBedHot = () => `${iconBed()}<g fill="none" stroke="${RED}" stroke-width="7" stroke-linecap="round"><path d="M-20 -44 Q-30 -58 -20 -70"/><path d="M4 -44 Q-6 -58 4 -70"/><path d="M28 -44 Q18 -58 28 -70"/></g>`;
Object.assign(ICONS, { bed: iconBed, cloudx: iconCloudX, bedhot: iconBedHot });
const iconBatSwell = () => `<rect x="-64" y="-34" width="120" height="68" rx="10" fill="#FFFFFF" stroke="${NAVY}" stroke-width="6"/><rect x="56" y="-14" width="14" height="28" rx="4" fill="${NAVY}"/><path d="M-50 -34 Q-6 -78 40 -34" fill="#FFFFFF" stroke="${RED}" stroke-width="7"/><rect x="-48" y="-18" width="86" height="36" rx="6" fill="#FFD84D"/>`;
Object.assign(ICONS, { batswell: iconBatSwell });
const iconVac = () => `<circle cx="0" cy="8" r="62" fill="${NAVY}" stroke="#FFFFFF" stroke-width="6"/><circle cx="0" cy="8" r="46" fill="#1B3358"/><circle cx="0" cy="-8" r="14" fill="${TEAL}" stroke="#FFFFFF" stroke-width="4"/><circle cx="0" cy="-8" r="5" fill="#FFFFFF"/><rect x="-22" y="26" width="44" height="8" rx="4" fill="${YEL}"/>`;
Object.assign(ICONS, { vac: iconVac });
const G = (gen) => ({ mode: 'corner', wave: false, kind: 'gen', gen });
const DEFS = {
  11: [
    Q('Điều gì xảy ra nếu', 'robot hút bụi chụp ảnh?'),
    G({ anim: 'shutter', items: [
      { ic: 'vac', x: X3[0], y: 330, k: 0.95, label: 'Robot|hút bụi', w: 'robot' },
      { ic: 'camera', x: X3[1], y: 330, k: 0.95, label: 'Camera', w: 'camera' },
      { ic: 'chip', x: X3[2], y: 330, k: 0.95, label: 'Dạy máy|nhận đồ vật', w: 'dạy' }], links: [[0, 1]] }),
    G({ items: [
      { ic: 'person', x: X3[0], y: 330, k: 0.95, label: 'Người thật|xem ảnh', w: 'người' },
      { ic: 'list', x: X3[1], y: 330, k: 0.95, label: 'Gắn nhãn:|tivi, cây cảnh', w: 'nhãn' },
      { ic: 'phone', x: X3[2], y: 330, k: 0.95, label: 'Làm thuê|từ xa', w: 'xa' }], links: [[0, 1], [1, 2]] }),
    G({ items: [
      { pill: '12/2022', x: 540, y: 670, k: 1, w: 'tháng' },
      { ic: 'eye', x: 540, y: 270, k: 0.9, label: 'Tạp chí|MIT Technology Review', w: 'mit' },
      { pill: '15 ảnh', x: 540, y: 750, k: 1, w: 'mười' }] }),
    G({ items: [
      { ic: 'vac', x: X3[0], y: 330, k: 0.95, label: 'Máy thử|không bán ra', w: 'robot' },
      { ic: 'mesh', x: X3[2], y: 330, k: 0.95, label: 'Nhiều nước', w: 'nhiều' },
      { pill: 'Tháng 6 đến 11/2020', x: 540, y: 720, k: 0.95, w: 'tháng' }] }),
    G({ anim: 'camflow', items: [
      { ic: 'list', x: X3[0], y: 330, k: 0.95, label: 'Công ty|gắn nhãn', w: 'công' },
      { ic: 'person', x: X3[1], y: 330, k: 0.95, label: 'Người làm thuê|nước khác', w: 'người' },
      { ic: 'lock', x: X3[2], y: 330, k: 0.95, label: 'Đăng lên|nhóm kín', w: 'nhóm' }], links: [[0, 1], [1, 2]] }),
    G({ items: [
      { ic: 'person', x: X3[0], y: 330, k: 0.95, label: 'Người dùng|đã ký đồng ý', w: 'người' },
      { ic: 'nocopy', x: X3[2], y: 330, k: 0.95, label: 'Chấm dứt|hợp tác', w: 'chấm' },
      { pill: 'Hơn 2 triệu ảnh đã chia sẻ', x: 540, y: 720, k: 0.95, w: 'hai' }] }),
    G({ items: [
      { ic: 'list', x: X3[0], y: 330, k: 0.95, label: 'Đọc chính sách|riêng tư', w: 'đọc' },
      { ic: 'shield', x: X3[1], y: 330, k: 0.95, label: 'Chỉ chia sẻ|dữ liệu cần', w: 'chia' },
      { ic: 'eyex', x: X3[2], y: 330, k: 0.95, label: 'Tắt camera|nếu có', w: 'tắt' }] }),
    E],
  10: [
    Q('Điều gì xảy ra nếu', 'pin bị sạc sai cách?'),
    G({ items: [
      { ic: 'camera', x: X3[0], y: 330, k: 0.95, label: 'Camera|không dây', w: 'camera' },
      { ic: 'watch', x: X3[1], y: 330, k: 0.95, label: 'Vòng tay', w: 'vòng' },
      { ic: 'batfull', x: X3[2], y: 330, k: 0.95, label: 'Sạc|dự phòng', w: 'sạc' }] }),
    G({ anim: 'puff', items: [
      { ic: 'thermo', x: X3[0], y: 330, k: 0.95, label: 'Nóng, sạc sai|hoặc hư', w: 'nóng' },
      { ic: 'cloud', x: X3[1], y: 330, k: 0.95, label: 'Sinh ra khí', w: 'khí' },
      { ic: 'batswell', x: X3[2], y: 330, k: 0.95, label: 'Pin phồng', w: 'phồng' }], links: [[0, 1]] }),
    G({ items: [
      { ic: 'person', x: X3[0], y: 330, k: 0.95, label: 'Nhà nghiên|cứu Maryland', w: 'nhà' },
      { ic: 'list', x: X3[1], y: 330, k: 0.95, label: 'Bài báo|tổng quan', w: 'bài' },
      { pill: '2025', x: 540, y: 700, k: 1, w: 'năm' }] }),
    G({ items: [
      { ic: 'batswell', x: X3[0], y: 330, k: 0.95, label: 'Pin phồng', w: 'pin' },
      { ic: 'batlow', x: X3[1], y: 330, k: 0.95, label: 'Giảm|dung lượng', w: 'dung' },
      { ic: 'bell', x: X3[2], y: 330, k: 0.95, label: 'Dấu hiệu|cảnh báo', w: 'cảnh' }] }),
    G({ items: [
      { ic: 'sun', x: X3[0], y: 330, k: 0.95, label: 'Để nóng,|xe dưới nắng', w: 'nóng' },
      { ic: 'nocopy', x: X3[1], y: 330, k: 0.95, label: 'Sạc không|đúng hãng', w: 'sạc' },
      { ic: 'batlow', x: X3[2], y: 330, k: 0.95, label: 'Rơi,|va đập', w: 'rơi' }] }),
    G({ items: [
      { ic: 'batswell', x: X3[0], y: 330, k: 0.95, label: 'Thấy pin phồng', w: 'phồng' },
      { ic: 'nocopy', x: X3[1], y: 330, k: 0.95, label: 'Ngừng dùng|ngừng sạc', w: 'ngừng' },
      { ic: 'updx', x: X3[2], y: 330, k: 0.95, label: 'Không bóp,|không chọc', w: 'không' }] }),
    G({ items: [
      { ic: 'shield', x: X3[0], y: 330, k: 0.95, label: 'Nơi thoáng,|hộp kim loại', w: 'nơi' },
      { ic: 'reset', x: X3[1], y: 330, k: 0.95, label: 'Điểm thu hồi|pin', w: 'điểm' },
      { ic: 'nocopy', x: X3[2], y: 330, k: 0.95, label: 'Không vứt|thùng rác', w: 'đừng' }] }),
    E],
  9: [
    Q('Điều gì xảy ra nếu', 'nhiều camera bị chiếm quyền?'),
    G({ items: [
      { ic: 'camera', x: X3[0], y: 330, k: 0.95, label: 'Một camera|bị chiếm', w: 'camera' },
      { ic: 'eye', x: X3[1], y: 330, k: 0.95, label: 'Người lạ|xem hình', w: 'người' },
      { ic: 'mesh', x: X3[2], y: 330, k: 0.95, label: 'Rất nhiều|camera', w: 'rất' }], links: [[0, 1]] }),
    G({ items: [
      { ic: 'mesh', x: X3[0], y: 330, k: 0.95, label: 'Nhóm thiết bị|bị chiếm', w: 'nhóm' },
      { pill: 'botnet', x: 540, y: 700, k: 1, w: 'botnet' },
      { ic: 'person', x: X3[2], y: 330, k: 0.95, label: 'Kẻ tấn công|ra lệnh', w: 'kẻ' }], links: [[2, 0]] }),
    G({ items: [
      { pill: '21/10/2016', x: 540, y: 720, k: 1, w: 'hai' },
      { ic: 'bug', x: X3[0], y: 330, k: 0.95, label: 'Phần mềm độc hại|Mirai', w: 'mirai' },
      { ic: 'camera', x: X3[2], y: 330, k: 0.95, label: 'Camera, đầu|ghi hình', w: 'camera' }], links: [[1, 2]] }),
    G({ items: [
      { ic: 'lock', x: X3[0], y: 330, k: 0.95, label: 'Mật khẩu|mặc định', w: 'mật' },
      { ic: 'key', x: X3[1], y: 330, k: 0.95, label: 'Cài sẵn|trong máy', w: 'cài' },
      { ic: 'nocopy', x: X3[2], y: 330, k: 0.95, label: 'Chủ không|đổi được', w: 'không' }] }),
    G({ anim: 'swarm', items: [
      { ic: 'server', x: X3[0], y: 330, k: 0.95, label: 'Dyn', w: 'dyn' },
      { ic: 'list', x: X3[1], y: 330, k: 0.95, label: 'Danh bạ|của internet', w: 'danh' }] }),
    G({ items: [
      { pill: 'Twitter', x: 300, y: 500, k: 0.95, w: 'twitter' },
      { pill: 'Netflix', x: 780, y: 500, k: 0.95, w: 'netflix' },
      { pill: 'Reddit', x: 300, y: 610, k: 0.95, w: 'reddit' },
      { pill: 'Spotify', x: 780, y: 610, k: 0.95, w: 'spotify' },
      { pill: 'Khoảng 100.000 thiết bị', x: 540, y: 730, k: 0.9, w: 'khoảng' }] }),
    G({ items: [
      { ic: 'lock', x: X3[0], y: 330, k: 0.95, label: 'Đổi mật khẩu|mặc định', w: 'mật' },
      { ic: 'update', x: X3[1], y: 330, k: 0.95, label: 'Cập nhật|phần mềm', w: 'cập' },
      { ic: 'updx', x: X3[2], y: 330, k: 0.95, label: 'Thay thiết bị|hết hỗ trợ', w: 'thay' }] }),
    E],
  8: [
    Q('Điều gì xảy ra nếu', 'đám mây nhà bạn sập?'),
    G({ anim: 'cmdflow', items: [
      { ic: 'phone', x: X3[0], y: 330, k: 0.95, label: 'Ứng dụng', w: 'ứng' },
      { ic: 'cloud', x: X3[1], y: 330, k: 0.95, label: 'Đám mây', w: 'đám' },
      { ic: 'bulb', x: X3[2], y: 330, k: 0.95, label: 'Thiết bị|trong nhà', w: 'thiết' }] }),
    G({ anim: 'blocked', items: [
      { ic: 'phone', x: X3[0], y: 330, k: 0.95, label: 'Lệnh|không đi được', w: 'nếu' },
      { ic: 'cloudx', x: X3[1], y: 330, k: 0.95, label: 'Đám mây|sập', w: 'sập' },
      { ic: 'bulb', x: X3[2], y: 330, k: 0.95, label: 'Đứng yên|cài đặt cuối', w: 'đứng' }] }),
    G({ items: [
      { pill: '20/10/2025 (giờ Mỹ)', x: 540, y: 720, k: 0.95, w: 'hai' },
      { ic: 'server', x: 540, y: 300, k: 0.95, label: 'Trung tâm dữ liệu|bang Virginia, Mỹ', w: 'trung' }] }),
    G({ anim: 'hot', items: [
      { ic: 'bedhot', x: 540, y: 300, k: 0.95, label: 'Giường thông minh|cần mạng liên tục', w: 'giường' },
      { pill: 'Khoảng 2.000 USD', x: 540, y: 740, k: 0.95, w: 'khoảng' }] }),
    G({ anim: 'blocked', items: [
      { ic: 'bedhot', x: X3[2], y: 330, k: 0.95, label: 'Nóng quá,|ngừng làm mát', w: 'giường' },
      { ic: 'phone', x: X3[0], y: 330, k: 0.95, label: 'Ứng dụng', w: 'ứng' },
      { ic: 'cloudx', x: X3[1], y: 330, k: 0.95, label: 'Mất kết nối', w: 'đám' }] }),
    G({ items: [
      { ic: 'person', x: X3[0], y: 330, k: 0.95, label: 'Người đứng|đầu hãng', w: 'người' },
      { ic: 'update', x: X3[1], y: 330, k: 0.95, label: 'Làm việc|ngày đêm', w: 'suốt' },
      { ic: 'shield', x: X3[2], y: 330, k: 0.95, label: 'Chế độ|mất mạng', w: 'chế' }], links: [[0, 1], [1, 2]] }),
    G({ items: [
      { ic: 'router', x: X3[1], y: 330, k: 0.95, label: 'Mất mạng', w: 'mất' },
      { ic: 'door', x: X3[0], y: 330, k: 0.95, label: 'Điều khiển|tại chỗ?', w: 'tại' },
      { ic: 'key', x: X3[2], y: 330, k: 0.95, label: 'Chìa cơ|dự phòng', w: 'chìa' }] }),
    E],
  7: [
    G({ anim: 'rings1', items: [
      { ic: 'router', x: X3[0], y: 330, k: 0.95, label: 'Router|phát sóng', w: 'wifi' },
      { ic: 'wifi', x: X3[1], y: 330, k: 0.95, label: 'Sóng lan|ra ngoài tường', w: 'sóng' },
      { ic: 'person', x: X3[2], y: 330, k: 0.95, label: 'Người đứng|gần nhà', w: 'người' }], links: [[0, 1], [1, 2]] }),
    G({ anim: 'packets', items: [
      { ic: 'router', x: X3[0], y: 330, k: 0.95, label: 'Router', w: 'router' },
      { ic: 'wifi', x: X3[1], y: 330, k: 0.95, label: 'Sóng|vô tuyến', w: 'sóng' },
      { ic: 'phone', x: X3[2], y: 330, k: 0.95, label: 'Điện thoại', w: 'điện' }] }),
    G({ anim: 'bands', items: [
      { ic: 'wifi', x: X3[0], y: 330, k: 0.95, label: 'Đi xa|hơn', w: 'xa' },
      { ic: 'wifi', x: X3[1], y: 330, k: 0.95, label: 'Nhanh|hơn', w: 'nhanh' },
      { ic: 'ruler', x: X3[2], y: 330, k: 0.95, label: 'Khoảng 30 đến|50 mét', w: 'ba' }] }),
    G({ anim: 'token', items: [
      { ic: 'scramble', x: X3[0], y: 330, k: 0.95, label: 'Dữ liệu|bị xáo trộn', w: 'xáo' },
      { ic: 'lock', x: X3[1], y: 330, k: 0.95, label: 'Mật khẩu|WiFi', w: 'mật' },
      { ic: 'key', x: X3[2], y: 330, k: 0.95, label: 'Chìa|giải mã', w: 'chìa' }] }),
    G({ anim: 'guess', items: [
      { pill: 'WPA2', x: 300, y: 700, k: 1, w: 'wpa2' },
      { pill: 'WPA3', x: 780, y: 700, k: 1, w: 'wpa3' },
      { ic: 'shield', x: 540, y: 300, k: 1.1, label: 'Chống đoán|mật khẩu', w: 'chống' }] }),
    G({ anim: 'sessions', items: [
      { pill: 'WPA3', x: 540, y: 700, k: 1, w: 'wpa3' },
      { ic: 'key', x: X3[0] + 80, y: 330, k: 0.95, label: 'Mỗi lần|một chìa riêng', w: 'chìa' },
      { ic: 'lock', x: X3[2] - 80, y: 330, k: 0.95, label: 'Dữ liệu cũ|vẫn kín', w: 'kín' }] }),
    G({ anim: 'pulses', items: [
      { ic: 'list', x: X3[0], y: 330, k: 0.95, label: 'Không mật khẩu|hoặc chuẩn cũ', w: 'không' },
      { ic: 'shield', x: X3[1], y: 330, k: 0.95, label: 'WPA3 hoặc|WPA2 AES', w: 'wpa3' },
      { ic: 'router', x: X3[2], y: 330, k: 0.95, label: 'Nâng cấp|hoặc thay', w: 'thay' }] }),
    G({ anim: 'chips', items: [
      { hide: true, p: false, x: 0, y: 0, w: 'cụm' },
      { pill: '16 ký tự', x: 330, y: 560, k: 0.9, w: 'mười' },
      { ic: 'router', x: 780, y: 520, k: 0.85, label: 'Kiểm tra|chuẩn bảo mật', w: 'router' }] }),
    E],
  1: [
    G({ anim: 'camflow', items: [
      { ic: 'camera', x: X3[0], y: 330, k: 0.95, label: 'Camera|trong nhà', w: 'camera' },
      { ic: 'house', x: X3[1], y: 330, k: 0.95, label: 'Hình ảnh|gia đình', w: 'gia' },
      { ic: 'eye', x: X3[2], y: 330, k: 0.95, label: 'Người lạ xem', w: 'người' },
      { pill: '3 việc cần làm', x: 540, y: 700, k: 1, w: 'ba' }], links: [[0, 1], [1, 2]] }),
    G({ anim: 'tries', title: 'Việc 1: Đổi mật khẩu mặc định', titleSize: 54, items: [
      { ic: 'lock', x: 540, y: 300, k: 1.25, label: 'Mật khẩu|mặc định', w: 'mật' },
      { pill: 'admin', x: 270, y: 700, k: 0.9, w: 'admin' },
      { pill: '123456', x: 810, y: 700, k: 0.9, w: '123456' }] }),
    G({ anim: 'infect', items: [
      { ic: 'bug', x: X3[0], y: 330, k: 0.95, label: 'Chương trình|tự động thử', w: 'chương' },
      { ic: 'camera', x: X3[1], y: 330, k: 0.95, label: 'Hàng loạt|thiết bị', w: 'hàng' },
      { pill: '2016', x: 300, y: 700, k: 0.9, w: 'năm' },
      { pill: 'Mirai', x: 780, y: 700, k: 0.9, w: 'mirai' },
      { ic: 'camera', x: X3[2], y: 330, k: 0.95, label: 'Hàng trăm nghìn|camera', w: 'hàng' }], links: [[0, 1]] }),
    G({ anim: 'strength', items: [
      { ic: 'lock', x: X3[0], y: 330, k: 0.95, label: 'Mật khẩu|dài', w: 'mật' },
      { ic: 'nocopy', x: X3[1], y: 330, k: 0.95, label: 'Không dùng lại|ở nơi khác', w: 'không' },
      { ic: 'shield', x: X3[2], y: 330, k: 0.95, label: 'Xác thực|hai bước', w: 'xác' }] }),
    G({ anim: 'progress', title: 'Việc 2: Cập nhật phần mềm', titleSize: 54, items: [
      { ic: 'bug', x: X3[0], y: 300, k: 0.85, label: 'Phần mềm|có lỗi', w: 'lỗi' },
      { ic: 'shield', x: X3[1], y: 300, k: 0.85, label: 'Hãng sửa lỗi', w: 'sửa' },
      { ic: 'update', x: X3[2], y: 300, k: 0.85, label: 'Bản cập nhật', w: 'bản' },
      { pill: 'Bật tự động', x: 540, y: 700, k: 1, w: 'tự' }], links: [[0, 1], [1, 2]] }),
    G({ anim: 'drain', items: [
      { ic: 'camera', x: X3[0], y: 330, k: 0.95, label: 'Thiết bị|quá cũ', w: 'thiết' },
      { ic: 'updx', x: X3[1], y: 330, k: 0.95, label: 'Hết cập nhật', w: 'cập' },
      { ic: 'camera', x: X3[2], y: 330, k: 0.95, label: 'Nên thay mới', w: 'thay' }], links: [[0, 1], [1, 2]] }),
    G({ anim: 'pulse2', title: 'Việc 3: Chỗ đặt và người xem', titleSize: 54, items: [
      { ic: 'bedx', x: 300, y: 330, k: 1.1, label: 'Phòng ngủ,|phòng tắm', w: 'phòng' },
      { ic: 'list', x: 780, y: 330, k: 1.1, label: 'Xóa người|không còn cần', w: 'xóa' }] }),
    G({ anim: 'wipe', items: [
      { ic: 'camera', x: X3[0], y: 330, k: 0.95, label: 'Bán hoặc|cho lại', w: 'camera' },
      { ic: 'reset', x: X3[1], y: 330, k: 0.95, label: 'Khôi phục|cài đặt gốc', w: 'khôi' },
      { ic: 'person', x: X3[2], y: 330, k: 0.95, label: 'Xóa khỏi|tài khoản', w: 'tài' }], links: [[0, 1], [1, 2]] }),
    E],
  2: [
    Q('Đếm thử nhé!', 'Nhà bạn có mấy thiết bị nối mạng?'),
    G({ items: [
      { ic: 'router', x: X4[0], y: 330, k: 0.85, label: 'Bộ phát|WiFi', w: 'wifi' },
      { ic: 'tv', x: X4[1], y: 330, k: 0.85, label: 'Tivi|thông minh', w: 'tivi' },
      { ic: 'watch', x: X4[2], y: 330, k: 0.85, label: 'Đồng hồ|thông minh', w: 'đồng' },
      { ic: 'camera', x: X4[3], y: 330, k: 0.85, label: 'Camera', w: 'camera' }] }),
    G({ items: [
      { ic: 'purifier', x: X3[0], y: 330, k: 0.95, label: 'Máy lọc|không khí', w: 'máy' },
      { ic: 'rice', x: X3[1], y: 330, k: 0.95, label: 'Nồi cơm', w: 'nồi' },
      { ic: 'phone', x: X3[2], y: 330, k: 0.95, label: 'Ứng dụng|trên điện thoại', w: 'ứng' }] }),
    Q('Có thể bạn chưa biết!', 'Nhiều thiết bị quanh ta là IoT'),
    G({ items: [
      { ic: 'wifi', x: X3[0], y: 330, k: 0.95, label: 'Kết nối|mạng', w: 'kết' },
      { ic: 'door', x: X3[1], y: 330, k: 0.95, label: 'Một cánh cửa', w: 'cánh' },
      { ic: 'q', x: X3[2], y: 330, k: 0.95, label: 'Nó làm gì?', w: 'làm' }], links: [[0, 1]] }),
    E],
  3: [
    G({ items: [
      { ic: 'bulb', x: X3[0], y: 330, k: 0.95, label: 'Đèn', w: 'đèn' },
      { ic: 'q', x: X3[1], y: 330, k: 0.8, label: 'Làm sao biết?', w: 'biết' },
      { ic: 'person', x: X3[2], y: 330, k: 0.95, label: 'Người đi vào', w: 'người' }] }),
    G({ items: [
      { ic: 'eye', x: 540, y: 300, k: 1.25, label: 'Cảm biến', w: 'cảm' },
      { pill: '= giác quan', x: 540, y: 600, k: 1, w: 'giác', pyoff: 0 }] }),
    G({ items: [
      { ic: 'thermo', x: X5[0], y: 330, k: 0.72, label: 'Nhiệt|độ', w: 'nhiệt' },
      { ic: 'drop', x: X5[1], y: 330, k: 0.72, label: 'Độ|ẩm', w: 'ẩm' },
      { ic: 'sun', x: X5[2], y: 330, k: 0.72, label: 'Ánh|sáng', w: 'ánh' },
      { ic: 'motion', x: X5[3], y: 330, k: 0.72, label: 'Chuyển|động', w: 'chuyển' },
      { ic: 'ruler', x: X5[4], y: 330, k: 0.72, label: 'Khoảng|cách', w: 'khoảng' }] }),
    G({ items: [
      { ic: 'thermo', x: X3[0], y: 330, k: 0.95, label: 'Hiện tượng|ngoài đời', w: 'hiện' },
      { pill: '28°C', x: X3[1], y: 330, k: 1, w: 'con' },
      { ic: 'chip', x: X3[2], y: 330, k: 0.95, label: 'Thiết bị|hiểu được', w: 'thiết' }], links: [[0, 1], [1, 2]] }),
    G({ items: [
      { ic: 'eyex', x: X3[0] + 40, y: 330, k: 1, label: 'Không có|cảm biến', w: 'không' },
      { ic: 'q', x: X3[2] - 40, y: 330, k: 1, label: 'Thế giới|xung quanh?', w: 'thế' }] }),
    E],
  4: [
    G({ items: [
      { ic: 'q', x: X3[1], y: 330, k: 0.85, label: 'Ai ra lệnh?', w: 'ai' },
      { ic: 'eye', x: X3[0], y: 330, k: 0.95, label: 'Cảm biến', w: 'cảm' },
      { ic: 'bulb', x: X3[2], y: 330, k: 0.95, label: 'Bóng đèn', w: 'bóng' }] }),
    G({ items: [
      { ic: 'chip', x: 540, y: 300, k: 1.3, label: 'Vi điều khiển', w: 'vi' },
      { pill: 'chạy chương trình', x: 540, y: 620, k: 0.9, w: 'chạy' }] }),
    G({ items: [
      { ic: 'esp', x: 330, y: 330, k: 1.05, label: 'ESP32', w: 'esp32' },
      { ic: 'arduino', x: 750, y: 330, k: 1.05, label: 'Arduino', w: 'arduino' }] }),
    G({ items: [
      { ic: 'eye', x: 150, y: 330, k: 0.7, label: 'Cảm biến', w: 'dữ' },
      { ic: 'chip', x: 400, y: 330, k: 0.8, label: 'Vi điều khiển', w: 'quyết' },
      { ic: 'bulb', x: 690, y: 180, k: 0.62, label: 'Bật đèn', w: 'đèn' },
      { ic: 'fan', x: 890, y: 340, k: 0.62, label: 'Mở quạt', w: 'quạt' },
      { ic: 'bell', x: 690, y: 520, k: 0.62, label: 'Gửi thông báo', w: 'thông' }], links: [[0, 1], [1, 2], [1, 3], [1, 4]] }),
    G({ items: [
      { ic: 'eye', x: X3[0], y: 330, k: 0.95, label: 'Cảm biến|mắt và tai', w: 'cảm' },
      { ic: 'chip', x: X3[2], y: 330, k: 0.95, label: 'Vi điều khiển|bộ não', w: 'vi' }], links: [[0, 1]] }),
    E],
  5: [
    G({ items: [
      { ic: 'bulb', x: X3[0], y: 330, k: 0.95, label: 'Đèn', w: 'đèn' },
      { ic: 'phone', x: X3[2], y: 330, k: 0.95, label: 'Điện thoại', w: 'điện' },
      { ic: 'q', x: X3[1], y: 330, k: 0.85, label: 'Bằng gì?', w: 'bằng' }] }),
    G({ items: [
      { ic: 'wifi', x: 250, y: 330, k: 1, label: 'WiFi', w: 'wifi' },
      { pill: 'nhiều dữ liệu', x: 250, y: 620, k: 0.8, w: 'nhiều' },
      { ic: 'batlow', x: 790, y: 330, k: 1, label: 'Tốn điện hơn', w: 'tốn' }] }),
    G({ items: [
      { ic: 'bt', x: X3[0], y: 330, k: 0.95, label: 'Bluetooth', w: 'bluetooth' },
      { pill: 'Gần', x: X3[1], y: 330, k: 0.95, w: 'gần' },
      { ic: 'batfull', x: X3[2], y: 330, k: 0.95, label: 'Tiết kiệm pin', w: 'tiết' }] }),
    G({ title: 'Zigbee', titleT: 0.4, items: [
      { ic: 'bulb', x: 190, y: 580, k: 0.62, label: 'Thiết bị nhỏ', w: 'thiết' },
      { ic: 'thermo', x: 540, y: 580, k: 0.62, label: 'Pin bền', w: 'pin' },
      { ic: 'fan', x: 890, y: 580, k: 0.62, label: 'Mạng lưới', w: 'và' },
      { ic: 'router', x: 540, y: 270, k: 0.9, label: 'Bộ trung tâm', w: 'trung' }], links: [[3, 0], [3, 1], [3, 2], [0, 1], [1, 2]] }),
    G({ items: [
      { ic: 'wifi', x: X3[0], y: 330, k: 0.95, label: 'WiFi', w: 'mỗi' },
      { ic: 'bt', x: X3[1], y: 330, k: 0.95, label: 'Bluetooth', w: 'phù' },
      { ic: 'mesh', x: X3[2], y: 330, k: 0.95, label: 'Zigbee', w: 'việc' }] }),
    E],
  6: [
    G({ items: [
      { ic: 'phone', x: X3[0], y: 330, k: 0.95, label: 'Đi du lịch xa', w: 'du' },
      { ic: 'thermo', x: X3[2], y: 330, k: 0.95, label: 'Nhiệt độ|trong nhà', w: 'nhiệt' },
      { ic: 'q', x: X3[1], y: 330, k: 0.8, label: 'Nhờ đâu?', w: 'nhờ' }] }),
    G({ items: [
      { ic: 'thermo', x: 210, y: 330, k: 1, label: 'Thiết bị', w: 'thiết' },
      { ic: 'cloud', x: 870, y: 330, k: 1, label: 'Máy chủ|(đám mây)', w: 'máy' }], links: [[0, 1]] }),
    G({ items: [
      { ic: 'cloud', x: 210, y: 330, k: 1, label: 'Máy chủ', w: 'máy' },
      { ic: 'phone', x: 870, y: 330, k: 1, label: 'Điện thoại|của bạn', w: 'điện' }], links: [[0, 1]] }),
    G({ items: [
      { ic: 'server', x: 540, y: 300, k: 1.3, label: 'Máy tính của một công ty', w: 'máy' },
      { pill: 'đặt ở nơi khác', x: 540, y: 640, k: 0.9, w: 'đặt' }] }),
    G({ items: [
      { ic: 'wifi', x: X3[0], y: 330, k: 0.95, label: 'Cần internet', w: 'internet' },
      { ic: 'shield', x: X3[2], y: 330, k: 0.95, label: 'Tin tưởng|nhà cung cấp', w: 'tin' }] }),
    E],
};
function buildScenes() {
  const kb = KB.videos.find((v) => v.id === VID);
  let t = 0;
  scenes = [];
  kb.scenes.forEach((text, i) => {
    const key = `v${VID}_s${i + 1}`;
    const dur = (TL[key] ? TL[key].giay : text.split(' ').length / 2.6) + 0.7;
    let sc;
    if (VID === 1 && !DEFS[1]) {
      const o = V1DEF[i];
      sc = Object.assign({}, o, { old: o.t1 - o.t0 });
    } else {
      const d = DEFS[VID][i];
      sc = { mode: d.mode, glow: d.glow, wave: d.wave, gfx: d.kind === 'gen' ? 'gen' : d.kind, q: d.q, pts: [] };
      if (d.kind === 'gen') {
        const g = buildGeneric(d.gen, text, dur, key);
        sc.gen = Object.assign({}, d.gen, { items: g.items });
        sc.pts = g.pts.map((q) => Object.assign({}, q, { x: ctx(q.x), y: cty(q.y) }));
      }
    }
    sc.text = text; sc.t0 = t; sc.t1 = t + dur; sc.key = key;
    t += dur;
    scenes.push(sc);
  });
  TOTAL = t;
}

function frameSVG(f) {
  const t = f / FPS;
  let idx = scenes.findIndex((s) => t >= s.t0 && t < s.t1);
  if (idx < 0) idx = scenes.length - 1;
  const sc = scenes[idx];
  const local = t - sc.t0;
  const lw = sc.old ? local * sc.old / (sc.t1 - sc.t0) : local;
  const lay = layoutAt(t, idx, local);
  const entry = t < 0.7 ? Math.max(0.01, easeOutBack(t / 0.7)) : 1;
  const ox = oxAt(idx, lw), vel = (oxAt(idx, lw + 0.04) - oxAt(idx, Math.max(0, lw - 0.04))) / 0.08;
  const jump = idx > 0 && local < 0.5 ? Math.sin(Math.PI * local / 0.5) : 0;
  const st = idx % 4;
  let oy = 0, rot = 0;
  if (st === 1) oy = -35 + 38 * Math.sin(local * 1.7);
  else if (st === 2) { oy = 10 * Math.sin(local * 2.2); rot = 10 * Math.sin(local * 3.6); }
  else if (st === 3) { oy = 38 * Math.cos(local * 1.2) - 12; rot = 5 * Math.sin(local * 2.4); }
  if (idx % 3 === 1 && local < 0.9) rot += 360 * smooth(local / 0.9);
  oy = Math.max(-70, Math.min(70, oy));
  const lay2 = { cy: lay.cy, s: lay.s * entry, ox, vel, jump: jump * (idx % 3 === 1 ? 1.6 : 1), oy, rot, corner: sc.mode === 'corner' };
  let bok = '';
  for (let i = 0; i < 14; i++) {
    const x = (i * 163 + 60) % 1080;
    const y = 2000 - ((t * 35 + i * 151) % 2100);
    bok += `<circle cx="${x}" cy="${f1(y)}" r="${10 + (i % 4) * 6}" fill="#FFFFFF" fill-opacity="${(0.1 + 0.05 * (i % 3)).toFixed(2)}"/>`;
  }
  const ringR = 440 * (lay.s / 1.25);
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
<rect width="${W}" height="${H}" fill="${TEAL}"/>
<g fill="none" stroke="#2AA898" stroke-width="6" stroke-linecap="round" stroke-linejoin="round">
<path d="M0 560 H150 L210 500 H340"/><path d="M1080 600 H930 L870 540 H750"/>
<path d="M0 1380 H130 L190 1440 H330"/><path d="M1080 1330 H950 L890 1390 H760"/>
<path d="M0 1800 H260 L320 1860 H520"/><path d="M1080 1780 H820 L760 1840"/></g>
${bok}
<circle cx="${(540 + lay2.ox * (lay2.corner ? 1 : 0.5)).toFixed(1)}" cy="${(lay.cy + lay2.oy * 0.6).toFixed(1)}" r="${ringR.toFixed(1)}" fill="#2DB8A8"/>
${gfx(sc.gfx, lw, t, sc)}
${bong(t, sc.wave, lay2, sc.glow, sc.pts || [], lw)}
${subtitle(sc.text, local, sc.t1 - sc.t0, sc.key)}
</svg>`;
}

async function render(f, file) {
  await sharp(Buffer.from(frameSVG(f))).png({ compressionLevel: 1 }).toFile(file);
}

(async () => {
  fs.mkdirSync(outDir, { recursive: true });
  buildScenes();
  // mốc tiếng động theo hình (dùng cho sfx_video.py)
  const NEG = ['updx', 'bedx', 'nocopy'], GOOD = ['shield', 'lock', 'update', 'reset'];
  const ev = [];
  scenes.forEach((c, i) => {
    if (i === 0) ev.push({ t: 0.05, name: 'impact', gain: 0.45 });
    else ev.push({ t: c.t0, name: 'transition', gain: 0.5 });
    if (c.gfx === 'end') { ev.push({ t: c.t0 + 0.1, name: 'outro', gain: 0.8 }); ev.push({ t: c.t0 + 1.0, name: 'pop', gain: 0.8 }); }
    if (c.gen) {
      if (c.gen.title) ev.push({ t: c.t0 + (c.gen.titleT || 0.3), name: 'reveal', gain: 0.55 });
      c.gen.items.forEach((it) => {
        const name = it.pill ? 'tick' : NEG.includes(it.ic) ? 'impact' : it.ic === 'bug' ? 'impact' : GOOD.includes(it.ic) ? 'chime' : 'pop';
        const gain = name === 'impact' ? 0.35 : name === 'chime' ? 0.5 : name === 'tick' ? 0.8 : 1;
        ev.push({ t: c.t0 + it.t, name, gain });
      });
      (c.gen.links || []).forEach((l) => ev.push({ t: c.t0 + Math.max(c.gen.items[l[0]].t, c.gen.items[l[1]].t) + 0.5, name: 'tick', gain: 0.5 }));
    }
  });
  ev.sort((x, y) => x.t - y.t);
  fs.writeFileSync(path.join(outDir, 'events.json'), JSON.stringify({ total: TOTAL, events: ev }, null, 1));
  fs.writeFileSync(path.join(outDir, 'scenes.json'), JSON.stringify(scenes.map((c) => ({ t0: c.t0, t1: c.t1, text: c.text })), null, 1));
  if (mode === 'at') {
    for (const tt of (process.env.AT || '').split(',').filter(Boolean)) await render(Math.round(parseFloat(tt) * FPS), path.join(outDir, `at_${tt}.png`));
    return;
  }
  if (mode === 'test') {
    const times = [];
    scenes.forEach((c) => { times.push(c.t0 + (c.t1 - c.t0) * 0.35); times.push(c.t0 + (c.t1 - c.t0) * 0.8); });
    const files = [];
    for (let i = 0; i < times.length; i++) {
      const file = path.join(outDir, `test_${i}.png`);
      await render(Math.round(times[i] * FPS), file);
      files.push(file);
    }
    const tiles = await Promise.all(files.map((f) => sharp(f).resize(360, 640).png().toBuffer()));
    const comps = tiles.map((buf, i) => ({ input: buf, left: (i % 4) * 360, top: Math.floor(i / 4) * 640 }));
    await sharp({ create: { width: 1440, height: 1920, channels: 3, background: '#ffffff' } }).composite(comps).png().toFile(path.join(outDir, 'montage.png'));
    console.log('test done', TOTAL.toFixed(1));
  } else {
    const n = Math.floor(TOTAL * FPS);
    const conc = 6;
    for (let i = 0; i < n; i += conc) {
      const batch = [];
      for (let j = i; j < Math.min(i + conc, n); j++) batch.push(render(j, path.join(outDir, `f${String(j).padStart(5, '0')}.png`)));
      await Promise.all(batch);
    }
    console.log('frames done', n, TOTAL.toFixed(2));
  }
})();
