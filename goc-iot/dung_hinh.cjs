const sharp = require('/opt/npm-tools/node_modules/sharp');
const fs = require('fs');
const path = require('path');

const W = 1080, H = 1920, FPS = 24;
const VID = parseInt(process.argv[2], 10);
const outDir = process.argv[3];
const mode = process.argv[4] || 'test';
const KB = JSON.parse(fs.readFileSync('/home/claude/fact-video/goc-iot/kich-ban.json', 'utf-8'));
let TL = {};
try { TL = JSON.parse(fs.readFileSync((process.env.TLFILE || '/home/claude/fact-video/goc-iot/giong/thoi-luong.json'), 'utf-8')); } catch (e) {}
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

let scenes = [];
let TOTAL = 0;

const LAY = { big: { cy: 800, s: 1.25 }, small: { cy: 1040, s: 0.76 } };

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
  return `<g opacity="${o.toFixed(2)}" transform="translate(${cx} ${cy}) scale(${s.toFixed(3)})">${inner}</g>`;
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
function wordTimes(text, dur) {
  const ws = text.split(' ');
  const total = ws.reduce((a, w) => a + w.length + 1, 0);
  const start = 0.25, span = Math.max(0.5, dur - 0.7);
  let cum = 0;
  return ws.map((w) => { const t = start + span * cum / total; cum += w.length + 1; return t; });
}
function buildGeneric(def, text, dur) {
  const ws = text.split(' ').map(stripW);
  const wt = wordTimes(text, dur);
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
  return links + out + d.items.map((it) => itemSVG(it, local)).join('') + dots;
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
    if ((p.x < 480) !== (side < 0)) continue;
    const w = smooth((local - p.a) / 0.3) * (1 - smooth((local - p.b) / 0.3));
    if (w > bw) { bw = w; best = p; }
  }
  if (!best || bw < 0.001) return { w: 0 };
  const tx = (best.x - 540) / lay.s + 400, ty = (best.y - (lay.cy + bounce)) / lay.s + 400;
  const vx = tx - S[0], vy = ty - S[1];
  const dist = Math.hypot(vx, vy);
  let d = [vx / dist + side * 0.7, vy / dist];
  const dl = Math.hypot(d[0], d[1]); d = [d[0] / dl, d[1] / dl];
  const reach = Math.min(300, Math.max(180, dist - 90)) + 8 * Math.sin((local - best.a) * 9) * bw;
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
  const bounce = -22 * hop * (lay.s / 1.25);
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
  const tr = `translate(540 ${lay.cy.toFixed(1)}) scale(${sc.toFixed(3)}) translate(-400 -400)`;
  const shadow = `<g transform="${tr}"><ellipse cx="425" cy="700" rx="${(110 - 16 * hop).toFixed(1)}" ry="14" fill="${NAVY}" fill-opacity="0.2"/></g>`;
  const glowEl = glow ? `<g transform="${tr}"><circle cx="400" cy="330" r="${(215 + 22 * Math.sin(t * 3)).toFixed(1)}" fill="#FFF6C2" fill-opacity="0.32"/></g>` : '';
  const body = `
<g transform="translate(540 ${(lay.cy + bounce).toFixed(1)}) scale(${sc.toFixed(3)}) translate(-400 -400)" fill="none">
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
</g>`;
  return shadow + glowEl + body;
}

function subtitle(text, local, dur) {
  const lines = wrap(text, 27);
  const lh = 74, pad = 24;
  const boxH = lines.length * lh + pad * 2;
  const bottom = 1620;
  const top = bottom - boxH;
  const a = clamp01(local / 0.25);
  const allWords = text.split(' ');
  const total = allWords.reduce((s, w) => s + w.length + 1, 0);
  const start = 0.25, span = Math.max(0.5, dur - 0.7);
  let cum = 0;
  const times = allWords.map((w) => { const ts = start + span * cum / total; cum += w.length + 1; return ts; });
  let idx = 0;
  const tx = lines.map((l, i) => {
    const ws = l.split(' ');
    const spans = ws.map((w) => {
      const k = idx++;
      const cur = local >= times[k] && (k === allWords.length - 1 || local < times[k + 1]);
      const fut = local < times[k];
      const fill = cur ? YEL : '#FFFFFF';
      return `<tspan fill="${fill}" fill-opacity="${fut ? 0.4 : 1}">${esc(w)}</tspan>`;
    }).join(' ');
    return `<text x="540" y="${top + pad + i * lh + 54}" text-anchor="middle" font-family="${FONT}" font-weight="700" font-size="56">${spans}</text>`;
  }).join('\n');
  return `<g opacity="${a}"><rect x="50" y="${top}" width="980" height="${boxH}" rx="36" fill="${NAVY}" fill-opacity="0.92"/>${tx}</g>`;
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


const X3 = [210, 540, 870], X4 = [165, 420, 675, 930], X5 = [120, 330, 540, 750, 960];
const E = { mode: 'big', glow: true, wave: true, kind: 'end' };
const Q = (a, b) => ({ mode: 'big', glow: true, wave: false, kind: 'q', q: [a, b] });
const G = (gen) => ({ mode: 'small', wave: false, kind: 'gen', gen });
const DEFS = {
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
    if (VID === 1) {
      const o = V1DEF[i];
      sc = Object.assign({}, o, { old: o.t1 - o.t0 });
    } else {
      const d = DEFS[VID][i];
      sc = { mode: d.mode, glow: d.glow, wave: d.wave, gfx: d.kind === 'gen' ? 'gen' : d.kind, q: d.q, pts: [] };
      if (d.kind === 'gen') {
        const g = buildGeneric(d.gen, text, dur);
        sc.gen = Object.assign({}, d.gen, { items: g.items });
        sc.pts = g.pts;
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
  const lay2 = { cy: lay.cy, s: lay.s * entry };
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
<circle cx="540" cy="${lay.cy.toFixed(1)}" r="${ringR.toFixed(1)}" fill="#2DB8A8"/>
${gfx(sc.gfx, lw, t, sc)}
${bong(t, sc.wave, lay2, sc.glow, sc.pts || [], lw)}
${subtitle(sc.text, local, sc.t1 - sc.t0)}
</svg>`;
}

async function render(f, file) {
  await sharp(Buffer.from(frameSVG(f))).png({ compressionLevel: 1 }).toFile(file);
}

(async () => {
  fs.mkdirSync(outDir, { recursive: true });
  buildScenes();
  fs.writeFileSync(path.join(outDir, 'scenes.json'), JSON.stringify(scenes.map((c) => ({ t0: c.t0, t1: c.t1, text: c.text })), null, 1));
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
