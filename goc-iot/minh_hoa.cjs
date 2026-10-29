// Cảnh minh họa có chuyển động thật cho video Góc IoT (thay cho hàng icon đứng yên).
// Mỗi cảnh: { w: [[tên, từ neo], ...] (theo thứ tự lời kể), point: [[tên, x, y]], draw(l, t) } với l = giây trong cảnh, t[tên] = giây từ neo xuất hiện.
module.exports = function (H) {
  const { NAVY, YEL, TEAL, RED, FONT, esc, f1, lerp, smooth, clamp01, easeOutBack, ICONS } = H;
  const GRN = '#3DDC84', SKY = '#8FD3FF', CRM = '#FFF3DC';
  const pr = (l, t0, d = 0.4) => clamp01((l - t0) / d);
  const pop = (l, t0, x, y, k, inner) => {
    if (l < t0) return '';
    const s = k * easeOutBack((l - t0) / 0.5);
    return `<g opacity="${clamp01((l - t0) / 0.25).toFixed(2)}" transform="translate(${f1(x)} ${f1(y)}) scale(${s.toFixed(3)})">${inner}</g>`;
  };
  const T = (x, y, s, size = 40, fill = NAVY, wt = 800, stroke = '') =>
    `<text x="${f1(x)}" y="${f1(y)}" text-anchor="middle" font-family="${FONT}" font-weight="${wt}" font-size="${size}" fill="${fill}"${stroke ? ` stroke="${stroke}" stroke-width="8" paint-order="stroke"` : ''}>${esc(s)}</text>`;
  const lines = (x, y, s, size, fill = NAVY) => s.split('|').map((ln, i) => T(x, y + i * (size + 6), ln, size, fill, 700)).join('');
  const photo = (w = 84, h = 64) => `<rect x="${-w / 2}" y="${-h / 2}" width="${w}" height="${h}" rx="8" fill="#FFFFFF" stroke="${NAVY}" stroke-width="5"/><circle cx="${-w / 5}" cy="${-h / 6}" r="${h / 9}" fill="${YEL}"/><path d="M${-w / 2 + 8} ${h / 2 - 8} L${-w / 8} ${-h / 12} L${w / 10} ${h / 5} L${w / 4} ${-h / 20} L${w / 2 - 8} ${h / 2 - 8} Z" fill="${TEAL}"/>`;
  const panel = (x, y, w, h, fill = '#FFFFFF', r = 28) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${r}" fill="${fill}" stroke="${NAVY}" stroke-width="6"/>`;
  // Bong bóng "câu trả lời sai" hiện trước, bị gạch chéo đỏ khi lời kể sửa lại.
  const myth = (l, tShow, tCross, text, x, y, w = 600) => {
    if (l < tShow) return '';
    let o = pop(l, tShow, x, y, 1, `<rect x="${-w / 2}" y="-44" width="${w}" height="88" rx="44" fill="#FFFFFF" stroke="${NAVY}" stroke-width="6"/>${T(0, 14, text, 38, NAVY, 800)}<circle cx="${-w / 2 - 6}" cy="46" r="12" fill="#FFFFFF" stroke="${NAVY}" stroke-width="5"/><circle cx="${-w / 2 - 28}" cy="70" r="7" fill="#FFFFFF" stroke="${NAVY}" stroke-width="4"/>`);
    if (tCross != null && l >= tCross) {
      const p = smooth((l - tCross) / 0.35);
      o += `<g transform="translate(${x} ${y})"><line x1="${-w / 2 + 20}" y1="0" x2="${f1(-w / 2 + 20 + (w - 40) * p)}" y2="0" stroke="${RED}" stroke-width="12" stroke-linecap="round"/></g>`;
      o += pop(l, tCross + 0.3, x + w / 2 - 20, y - 54, 1, `<rect x="-60" y="-26" width="120" height="52" rx="26" fill="${RED}"/>${T(0, 12, 'SAI', 34, '#FFFFFF')}`);
    }
    return o;
  };
  const ic = (name, k = 1) => `<g transform="scale(${k})">${ICONS[name]()}</g>`;

  // ----- Phòng khách nhìn từ trên xuống (hệ tọa độ 900 x 580) -----
  const ROOM = { w: 900, h: 580 };
  const PATH = [[130, 300], [300, 190], [520, 170], [720, 250], [770, 470], [540, 520], [380, 400], [130, 300]];
  const segLen = []; let totLen = 0;
  for (let i = 0; i < PATH.length - 1; i++) { const d = Math.hypot(PATH[i + 1][0] - PATH[i][0], PATH[i + 1][1] - PATH[i][1]); segLen.push(d); totLen += d; }
  const pathAt = (u) => {
    let d = ((u % 1) + 1) % 1 * totLen;
    for (let i = 0; i < segLen.length; i++) {
      if (d <= segLen[i]) { const k = d / segLen[i]; return [lerp(PATH[i][0], PATH[i + 1][0], k), lerp(PATH[i][1], PATH[i + 1][1], k), Math.atan2(PATH[i + 1][1] - PATH[i][1], PATH[i + 1][0] - PATH[i][0])]; }
      d -= segLen[i];
    }
    return [PATH[0][0], PATH[0][1], 0];
  };
  const furniture = () => `
    <rect x="0" y="0" width="900" height="580" rx="30" fill="${CRM}" stroke="${NAVY}" stroke-width="8"/>
    <ellipse cx="450" cy="300" rx="260" ry="150" fill="#FFFFFF" fill-opacity="0.55"/>
    <rect x="330" y="16" width="240" height="46" rx="10" fill="${NAVY}"/><rect x="346" y="24" width="208" height="28" rx="6" fill="#1B3358"/>
    <rect x="60" y="440" width="260" height="120" rx="26" fill="${SKY}" stroke="${NAVY}" stroke-width="6"/><rect x="76" y="452" width="228" height="40" rx="14" fill="#FFFFFF" fill-opacity="0.55"/>
    <rect x="530" y="330" width="230" height="110" rx="22" fill="#FFD9A8" stroke="${NAVY}" stroke-width="6"/>
    <circle cx="820" cy="92" r="52" fill="${GRN}" stroke="${NAVY}" stroke-width="6"/><circle cx="800" cy="74" r="22" fill="#2DBE6E"/><circle cx="842" cy="106" r="24" fill="#2DBE6E"/><rect x="800" y="126" width="40" height="30" rx="6" fill="#C77B4A" stroke="${NAVY}" stroke-width="5"/>`;
  const robotBody = (a, r = 46) => `<g transform="rotate(${(a * 180 / Math.PI).toFixed(1)})"><circle r="${r}" fill="${NAVY}" stroke="#FFFFFF" stroke-width="5"/><circle r="${r - 12}" fill="#1B3358"/><circle cx="${r - 22}" cy="0" r="11" fill="${TEAL}" stroke="#FFFFFF" stroke-width="3"/><circle cx="${r - 22}" cy="0" r="4" fill="#FFFFFF"/><rect x="${-r + 12}" y="-5" width="18" height="10" rx="5" fill="${YEL}"/></g>`;

  const v11 = [];
  // Cảnh 1 (index 0) là câu hỏi mở, không dùng ở đây.

  // Cảnh 2: robot chạy trong phòng, camera quét, ảnh bay vào bộ não
  v11.push({
    w: [['robot', 'robot'], ['camera', 'camera'], ['nghi', 'nghĩ'], ['hoc', 'máy']],
    point: [['robot', 540, 800], ['camera', 540, 800], ['nghi', 400, 380]],
    draw(l, t) {
      const ox = 90, oy = 480, speed = 0.075;
      let o = `<g transform="translate(${ox} ${oy})" opacity="${pr(l, 0.1, 0.4).toFixed(2)}">${furniture()}</g>`;
      const brain = pop(l, t.camera + 0.5, 880, 392, 1, `${panel(-100, -62, 200, 124, '#FFFFFF', 26)}<g transform="translate(-56 -8)">${ic('chip', 0.42)}</g>${T(30, -16, 'Đang học', 26)}<rect x="-30" y="12" width="110" height="18" rx="9" fill="${NAVY}" fill-opacity="0.2"/><rect x="-30" y="12" width="${f1(110 * clamp01((l - t.camera - 0.5) / 7))}" height="18" rx="9" fill="${GRN}"/>`);
      if (l >= t.robot) {
        const e = l - t.robot, [rx, ry, ra] = pathAt(e * speed), k = easeOutBack(e / 0.5);
        const cone = l >= t.camera ? `<path d="M0 0 L${f1(210 * Math.cos(-0.5))} ${f1(210 * Math.sin(-0.5))} L${f1(210 * Math.cos(0.5))} ${f1(210 * Math.sin(0.5))} Z" transform="rotate(${(ra * 180 / Math.PI).toFixed(1)})" fill="#FFFFFF" fill-opacity="${(0.22 + 0.12 * Math.sin(l * 6)).toFixed(2)}"/>` : '';
        o += `<g transform="translate(${f1(ox + rx)} ${f1(oy + ry)}) scale(${k.toFixed(3)})">${cone}${robotBody(ra)}</g>`;
      }
      o += brain;
      if (l >= t.camera) {
        for (let j = 0; j < 8; j++) {
          const te = t.camera + 0.35 + j * 1.15, u = (l - te) / 1.1;
          if (u < 0 || u > 1) continue;
          const [px, py] = pathAt((te - t.robot) * speed), fx = ox + px, fy = oy + py;
          const x = lerp(fx, 880, smooth(u)), y = lerp(fy, 392, smooth(u)) - 120 * Math.sin(Math.PI * u);
          o += `<circle cx="${f1(fx)}" cy="${f1(fy)}" r="${f1(30 + 60 * u)}" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-opacity="${(0.8 * (1 - u)).toFixed(2)}"/>`;
          o += `<g transform="translate(${f1(x)} ${f1(y)}) scale(${(1 - 0.5 * u).toFixed(2)})">${photo()}</g>`;
        }
      }
      o += myth(l, t.nghi, null, 'Ảnh chỉ nằm trong máy?', 330, 392, 560);
      return o;
    },
  });

  // Cảnh 3: ảnh được người thật gắn nhãn (khung bao vẽ lên tivi và cây cảnh)
  v11.push({
    w: [['khong', 'không'], ['nguoi', 'người'], ['tivi', 'tivi,'], ['cay', 'cây']],
    point: [['nguoi', 880, 640], ['tivi', 330, 640], ['cay', 330, 640]],
    draw(l, t) {
      const fx = 60, fy = 450, sc = 0.62;
      let o = myth(l, 0.1, t.khong, 'Ảnh chỉ nằm trong máy?', 330, 380, 560);
      o += `<g transform="translate(${fx} ${fy}) scale(${sc})" opacity="${pr(l, 0.1, 0.4).toFixed(2)}">${furniture()}</g>`;
      o += `<rect x="${fx - 8}" y="${fy - 8}" width="${f1(900 * sc + 16)}" height="${f1(580 * sc + 16)}" rx="22" fill="none" stroke="${NAVY}" stroke-width="8"/>`;
      const box = (t0, x, y, w, h, tag, tx, ty) => {
        if (l < t0) return '';
        const p = pr(l, t0, 0.7), per = 2 * (w + h);
        return `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="8" fill="none" stroke="${YEL}" stroke-width="7" stroke-dasharray="${f1(per)}" stroke-dashoffset="${f1(per * (1 - p))}"/>` +
          pop(l, t0 + 0.55, tx, ty, 1, `<rect x="-${tag.length * 13 + 22}" y="-30" width="${tag.length * 26 + 44}" height="58" rx="29" fill="${NAVY}"/>${T(0, 12, tag, 36, YEL)}`);
      };
      o += box(t.tivi, fx + 330 * sc - 8, fy + 14 * sc - 8, 240 * sc + 16, 52 * sc + 16, 'tivi', fx + 450 * sc, fy + 160 * sc);
      o += box(t.cay, fx + 768 * sc - 8, fy + 40 * sc - 8, 104 * sc + 16, 120 * sc + 16, 'cây cảnh', fx + 818 * sc - 40, fy + 250 * sc);
      // người làm thuê từ xa
      if (l >= t.nguoi) {
        const wx = 850, wy = 700;
        o += pop(l, t.nguoi, wx, wy, 1, `<circle cx="0" cy="-90" r="52" fill="#FFC9A8" stroke="${NAVY}" stroke-width="6"/><path d="M-70 40 Q-70 -30 0 -30 Q70 -30 70 40 Z" fill="${NAVY}"/><rect x="-100" y="40" width="200" height="14" rx="7" fill="${NAVY}"/><rect x="-86" y="-4" width="172" height="46" rx="8" fill="#FFFFFF" stroke="${NAVY}" stroke-width="5"/><circle cx="0" cy="19" r="8" fill="${TEAL}"/>${lines(0, 110, 'Người xem|và gắn nhãn', 34)}`);
        const tp = 0.4 * Math.sin(l * 10);
        o += `<g stroke="${NAVY}" stroke-width="6" stroke-linecap="round"><line x1="-40" y1="${f1(700 - 4 + tp * 10)}" x2="-40" y2="${f1(700 - 4 + tp * 10)}" transform="translate(${wx} 0)"/></g>`;
      }
      return o;
    },
  });

  // Cảnh 4: tháng 12/2022, tạp chí có 15 ảnh trong nhóm kín
  v11.push({
    w: [['lich', 'tháng'], ['tc', 'tạp'], ['anh', 'mười'], ['kin', 'nhóm']],
    point: [['lich', 250, 620], ['tc', 250, 900], ['anh', 700, 700]],
    draw(l, t) {
      let o = pop(l, t.lich, 250, 640, 1, `${panel(-150, -170, 300, 340, '#FFFFFF', 24)}<path d="M-150 -146 Q-150 -170 -126 -170 H126 Q150 -170 150 -146 V-90 H-150 Z" fill="${RED}" stroke="${NAVY}" stroke-width="6"/>${T(0, -112, 'THÁNG 12', 44, '#FFFFFF')}${T(0, 20, '2022', 96, NAVY)}<g fill="${NAVY}"><circle cx="-80" cy="-176" r="12"/><circle cx="80" cy="-176" r="12"/></g>${T(0, 110, 'Lịch', 1, '#FFFFFF')}`);
      o += pop(l, t.tc, 250, 960, 1, `${panel(-150, -62, 300, 124, '#FFFFFF', 22)}${T(0, -6, 'MIT', 52)}${T(0, 40, 'Technology Review', 28, NAVY, 700)}`);
      // lưới 15 ảnh
      const gx = 560, gy = 520, cw = 92, ch = 78;
      if (l >= t.anh - 0.1) {
        o += `<rect x="${gx - 24}" y="${gy - 24}" width="${5 * cw + 32}" height="${3 * ch + 44}" rx="22" fill="#FFFFFF" fill-opacity="0.35" stroke="${NAVY}" stroke-width="6"/>`;
        let n = 0;
        for (let j = 0; j < 15; j++) {
          const tj = t.anh + 0.1 + j * 0.14;
          if (l < tj) continue; n++;
          o += pop(l, tj, gx + (j % 5) * cw + cw / 2 - 4, gy + Math.floor(j / 5) * ch + ch / 2, 0.8, photo());
        }
        o += pop(l, t.anh, gx + 5 * cw / 2 - 8, gy + 3 * ch + 100, 1, `${T(0, 0, n + ' ảnh', 84, YEL, 800, NAVY)}`);
      }
      if (l >= t.kin) {
        const k = easeOutBack((l - t.kin) / 0.5);
        o += `<g transform="translate(${gx + 5 * cw - 4} ${gy - 22}) scale(${(1.1 * k).toFixed(3)})"><circle r="58" fill="#FFFFFF" stroke="${NAVY}" stroke-width="6"/><g transform="scale(0.75)">${ICONS.lock()}</g></g>`;
        o += pop(l, t.kin + 0.2, gx + 5 * cw / 2 - 8, gy - 56, 1, `<rect x="-120" y="-30" width="240" height="56" rx="28" fill="${NAVY}"/>${T(0, 10, 'nhóm kín', 34, YEL)}`);
      }
      return o;
    },
  });

  // Cảnh 5: máy thử nghiệm không bán ra, nhiều nước, tháng 6 đến 11/2020
  v11.push({
    w: [['robot', 'robot'], ['ban', 'bán'], ['nuoc', 'nhiều'], ['nam', 'tháng']],
    point: [['robot', 250, 620], ['nuoc', 700, 620], ['nam', 540, 960]],
    draw(l, t) {
      let o = pop(l, t.robot, 250, 640, 1.2, `<circle r="140" fill="#FFFFFF" stroke="${NAVY}" stroke-width="6"/><g transform="scale(1.5)">${ICONS.vac()}</g>`);
      if (l >= t.robot) o += pop(l, t.robot + 0.3, 250, 820, 1, `<rect x="-150" y="-30" width="300" height="58" rx="29" fill="${YEL}" stroke="${NAVY}" stroke-width="5"/>${T(0, 12, 'MÁY THỬ NGHIỆM', 30)}`);
      if (l >= t.ban) {
        const p = easeOutBack((l - t.ban) / 0.5);
        o += `<g transform="translate(250 640) scale(${p.toFixed(2)})"><circle r="156" fill="none" stroke="${RED}" stroke-width="14"/><line x1="-110" y1="110" x2="110" y2="-110" stroke="${RED}" stroke-width="14" stroke-linecap="round"/></g>`;
        o += pop(l, t.ban + 0.3, 250, 900, 1, T(0, 0, 'Không bán ra', 40, RED, 800));
      }
      // Bản đồ chấm và 5 nước
      const pins = [['Mỹ', 600, 590], ['Pháp', 760, 530], ['Tây Ban Nha', 720, 680], ['Đức', 860, 590], ['Nhật', 960, 670]];
      if (l >= t.nuoc) {
        o += `<rect x="520" y="470" width="520" height="330" rx="26" fill="#FFFFFF" fill-opacity="0.35" stroke="${NAVY}" stroke-width="6"/>`;
        for (let i = 0; i < 80; i++) { const x = 545 + (i % 16) * 31, y = 495 + Math.floor(i / 16) * 56 + ((i % 16) % 2) * 14; o += `<circle cx="${x}" cy="${y}" r="5" fill="${NAVY}" fill-opacity="0.18"/>`; }
        pins.forEach((p, i) => { o += pop(l, t.nuoc + i * 0.28, p[1], p[2], 1, `<circle r="20" fill="${RED}" stroke="#FFFFFF" stroke-width="5"/><circle r="${f1(30 + 14 * Math.sin(l * 4 + i))}" fill="none" stroke="${RED}" stroke-opacity="0.5" stroke-width="4"/>${T(0, 62, p[0], 28, NAVY, 800)}`); });
      }
      if (l >= t.nam) {
        const x0 = 120, x1 = 960, y = 1040, p = pr(l, t.nam, 3.2);
        o += `<rect x="${x0}" y="${y - 14}" width="${x1 - x0}" height="28" rx="14" fill="#FFFFFF" fill-opacity="0.5" stroke="${NAVY}" stroke-width="5"/><rect x="${x0}" y="${y - 14}" width="${f1((x1 - x0) * p)}" height="28" rx="14" fill="${YEL}" stroke="${NAVY}" stroke-width="5"/>`;
        o += T(x0 + 40, y + 70, 'Tháng 6', 40, NAVY) + T(x1 - 60, y + 70, 'Tháng 11/2020', 40, NAVY);
        o += `<circle cx="${f1(x0 + (x1 - x0) * p)}" cy="${y}" r="22" fill="${RED}" stroke="#FFFFFF" stroke-width="5"/>`;
      }
      return o;
    },
  });

  // Cảnh 6: ảnh đi từ nhà đến công ty, đến người làm thuê, rồi bị đăng lên nhóm kín
  v11.push({
    w: [['anh', 'ảnh'], ['cty', 'công'], ['nguoi', 'người'], ['nhom', 'nhóm'], ['trai', 'trái']],
    point: [['cty', 400, 700], ['nguoi', 700, 700], ['nhom', 900, 700]],
    draw(l, t) {
      const X = [130, 400, 670, 930], Y = 700;
      const node = (t0, i, inner, lab) => pop(l, t0, X[i], Y, 1, `<circle r="104" fill="#FFFFFF" stroke="${NAVY}" stroke-width="6"/>${inner}${lines(0, 168, lab, 34)}`);
      let o = node(t.anh, 0, `<g transform="scale(1.05)">${ICONS.vac()}</g>`, 'Robot|trong nhà');
      o += node(t.cty, 1, `<rect x="-52" y="-56" width="104" height="104" rx="8" fill="${SKY}" stroke="${NAVY}" stroke-width="6"/><g fill="#FFFFFF">${[-32, 0, 32].map((x) => [-34, -4, 26].map((y) => `<rect x="${x - 10}" y="${y}" width="20" height="20" rx="3"/>`).join('')).join('')}</g>`, 'Công ty|gắn nhãn');
      o += node(t.nguoi, 2, `<circle cx="0" cy="-30" r="30" fill="#FFC9A8" stroke="${NAVY}" stroke-width="5"/><path d="M-54 40 Q-54 0 0 0 Q54 0 54 40 Z" fill="${NAVY}"/><rect x="-60" y="34" width="120" height="12" rx="6" fill="${NAVY}"/>`, 'Người làm thuê|nước khác');
      o += node(t.nhom, 3, `<path d="M-60 -50 H60 Q72 -50 72 -38 V16 Q72 28 60 28 H10 L-30 60 V28 H-60 Q-72 28 -72 16 V-38 Q-72 -50 -60 -50 Z" fill="${YEL}" stroke="${NAVY}" stroke-width="6"/><g transform="translate(0 -8) scale(0.5)">${ICONS.lock()}</g>`, 'Nhóm kín');
      // ảnh chạy dọc đường đi
      const seg = (a, b, t0, per) => {
        if (l < t0) return '';
        let s = `<line x1="${X[a] + 112}" y1="${Y}" x2="${X[b] - 112}" y2="${Y}" stroke="#FFFFFF" stroke-opacity="0.6" stroke-width="6" stroke-dasharray="14 16" stroke-linecap="round"/>`;
        for (let i = 0; i < 2; i++) { const u = ((l - t0) * per + i * 0.5) % 1; s += `<g transform="translate(${f1(lerp(X[a] + 112, X[b] - 112, u))} ${Y - 46}) scale(0.62)">${photo()}</g>`; }
        return s;
      };
      o += seg(0, 1, t.cty + 0.3, 0.5) + seg(1, 2, t.nguoi + 0.3, 0.5) + seg(2, 3, t.nhom + 0.3, 0.5);
      if (l >= t.trai) {
        const p = pr(l, t.trai, 0.4), sh = 6 * Math.sin(l * 30) * (1 - p);
        o += pop(l, t.trai, 540 + sh, 1000, 1, `<rect x="-330" y="-48" width="660" height="96" rx="20" fill="#FFFFFF" stroke="${RED}" stroke-width="8"/>${T(0, 14, 'Trái thỏa thuận bảo mật', 48, RED)}`);
        o += `<g transform="translate(${X[3]} ${Y - 130}) scale(${easeOutBack((l - t.trai) / 0.5).toFixed(2)})"><circle r="30" fill="${RED}" stroke="#FFFFFF" stroke-width="5"/><text x="0" y="14" text-anchor="middle" font-family="${FONT}" font-weight="900" font-size="44" fill="#FFFFFF">!</text></g>`;
      }
      return o;
    },
  });

  // Cảnh 7: ký đồng ý, chấm dứt hợp tác, hơn 2 triệu ảnh
  v11.push({
    w: [['ky', 'ký'], ['chain', 'chấm'], ['hai', 'hai']],
    point: [['ky', 250, 620], ['chain', 780, 620], ['hai', 540, 960]],
    draw(l, t) {
      let o = pop(l, t.ky - 0.2, 270, 680, 1, `${panel(-150, -190, 300, 380, '#FFFFFF', 22)}${[-130, -100, -70, -40].map((y) => `<rect x="-110" y="${y}" width="${y === -40 ? 120 : 220}" height="12" rx="6" fill="${NAVY}" fill-opacity="0.25"/>`).join('')}${T(0, 120, 'Đã ký đồng ý', 34, NAVY, 800)}`);
      if (l >= t.ky + 0.4) {
        const p = pr(l, t.ky + 0.4, 1.0), pts = [[-100, 70], [-70, 20], [-40, 76], [-10, 24], [30, 72], [70, 30]];
        let d = '', total = pts.length - 1, upto = p * total;
        for (let i = 0; i <= Math.floor(upto) && i < pts.length; i++) {
          const a = pts[i]; if (i === 0) { d += `M${a[0]} ${a[1]}`; continue; }
          const b = pts[i - 1], f = Math.min(1, upto - (i - 1)); d += ` L${f1(lerp(b[0], a[0], f))} ${f1(lerp(b[1], a[1], f))}`;
        }
        o += `<g transform="translate(270 640)"><path d="${d}" fill="none" stroke="${NAVY}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></g>`;
        if (p >= 1) o += pop(l, t.ky + 1.5, 380, 520, 1, `<circle r="38" fill="${GRN}" stroke="${NAVY}" stroke-width="5"/><path d="M-18 2 L-5 16 L20 -14" fill="none" stroke="#FFFFFF" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>`);
      }
      if (l >= t.chain) {
        const p = pr(l, t.chain, 0.8), sp = 40 * smooth(p);
        const link = (x, r) => `<g transform="translate(${x} 640) rotate(${r})"><rect x="-70" y="-34" width="140" height="68" rx="34" fill="none" stroke="${NAVY}" stroke-width="14"/><rect x="-70" y="-34" width="140" height="68" rx="34" fill="none" stroke="#FFFFFF" stroke-width="5"/></g>`;
        o += link(740 - 54 - sp, -8 * p) + link(740 + 54 + sp, 8 * p);
        if (p > 0.4) o += `<g transform="translate(740 640) scale(${easeOutBack((p - 0.4) / 0.6).toFixed(2)})" stroke="${RED}" stroke-width="14" stroke-linecap="round"><line x1="-30" y1="-30" x2="30" y2="30"/><line x1="30" y1="-30" x2="-30" y2="30"/></g>`;
        o += pop(l, t.chain + 0.3, 740, 780, 1, lines(0, 0, 'Chấm dứt|hợp tác', 40));
      }
      if (l >= t.hai) {
        const p = pr(l, t.hai, 2.2), n = Math.round(2000000 * smooth(p)).toLocaleString('en-US').replace(/,/g, '.');
        o += pop(l, t.hai, 540, 960, 1, `${T(0, 0, 'Hơn ' + n + ' ảnh', 70, YEL, 800, NAVY)}`);
        for (let i = 0; i < 6; i++) { const u = ((l - t.hai) * 0.7 + i / 6) % 1; o += `<g transform="translate(${f1(lerp(250, 830, u))} ${f1(1050 - 40 * Math.sin(Math.PI * u))}) scale(0.5)" opacity="${(0.9 * Math.sin(Math.PI * u)).toFixed(2)}">${photo()}</g>`; }
      }
      return o;
    },
  });

  // Cảnh 8: ba việc làm được (chính sách, chỉ chia sẻ cần thiết, tắt camera)
  v11.push({
    w: [['doc', 'đọc'], ['chia', 'chia'], ['tat', 'tắt']],
    point: [['doc', 200, 640], ['chia', 540, 640], ['tat', 880, 640]],
    draw(l, t) {
      const X = [190, 540, 890], Y = 650;
      // 1. chính sách có công tắc
      let o = pop(l, t.doc, X[0], Y, 1, `${panel(-150, -200, 300, 400, '#FFFFFF', 22)}${T(0, -150, 'Chính sách', 36)}${[-80, 0, 80].map((y, i) => { const on = l < t.doc + 1.0 + i * 0.7; return `<rect x="-110" y="${y - 6}" width="130" height="14" rx="7" fill="${NAVY}" fill-opacity="0.25"/><rect x="40" y="${y - 22}" width="76" height="44" rx="22" fill="${on ? GRN : '#B8C4D2'}" stroke="${NAVY}" stroke-width="4"/><circle cx="${on ? 94 : 62}" cy="${y}" r="16" fill="#FFFFFF" stroke="${NAVY}" stroke-width="3"/>`; }).join('')}`);
      o += pop(l, t.doc + 0.2, X[0], Y + 250, 1, lines(0, 0, 'Đọc kỹ|quyền riêng tư', 34));
      // 2. chỉ chia sẻ dữ liệu cần thiết
      o += pop(l, t.chia, X[1], Y, 1, `<circle r="130" fill="#FFFFFF" stroke="${NAVY}" stroke-width="6"/><g transform="scale(1.5)">${ICONS.shield()}</g>`);
      if (l >= t.chia) for (let i = 0; i < 4; i++) { const u = ((l - t.chia) * 0.5 + i / 4) % 1, a = i * Math.PI / 2 + 0.7; o += `<g transform="translate(${f1(X[1] + Math.cos(a) * lerp(260, 140, u))} ${f1(Y + Math.sin(a) * lerp(260, 140, u))}) scale(0.4)" opacity="${(1 - u).toFixed(2)}">${photo()}</g>`; }
      o += pop(l, t.chia + 0.2, X[1], Y + 250, 1, lines(0, 0, 'Chỉ chia sẻ|dữ liệu cần thiết', 34));
      // 3. tắt camera
      o += pop(l, t.tat, X[2], Y, 1, `<circle r="130" fill="#FFFFFF" stroke="${NAVY}" stroke-width="6"/><g transform="scale(1.4)">${ICONS.camera()}</g>`);
      if (l >= t.tat + 0.4) { const p = easeOutBack((l - t.tat - 0.4) / 0.5); o += `<g transform="translate(${X[2]} ${Y}) scale(${p.toFixed(2)})"><line x1="-100" y1="100" x2="100" y2="-100" stroke="${RED}" stroke-width="16" stroke-linecap="round"/></g>`; }
      o += pop(l, t.tat + 0.2, X[2], Y + 250, 1, lines(0, 0, 'Tắt camera|nếu có tùy chọn', 34));
      return o;
    },
  });

  // ====== Helpers chung cho video 12-14 ======
  const tag = (x, y, text, w, fill = NAVY, col = YEL, size = 34) => `<rect x="${-w / 2}" y="-30" width="${w}" height="58" rx="29" fill="${fill}"/>${T(0, 12, text, size, col)}`;
  const toggle = (on, k = 1) => `<g transform="scale(${k})"><rect x="-60" y="-30" width="120" height="60" rx="30" fill="${on ? GRN : '#B8C4D2'}" stroke="${NAVY}" stroke-width="6"/><circle cx="${on ? 30 : -30}" cy="0" r="22" fill="#FFFFFF" stroke="${NAVY}" stroke-width="5"/></g>`;
  const cal = (month, year, k = 1) => `<g transform="scale(${k})">${panel(-130, -150, 260, 300, '#FFFFFF', 22)}<path d="M-130 -128 Q-130 -150 -108 -150 H108 Q130 -150 130 -128 V-80 H-130 Z" fill="${RED}" stroke="${NAVY}" stroke-width="6"/>${T(0, -96, month, 36, '#FFFFFF')}${T(0, 50, year, 84, NAVY)}</g>`;
  const person = (hair = NAVY, skin = '#FFC9A8') => `<circle cx="0" cy="-70" r="50" fill="${skin}" stroke="${NAVY}" stroke-width="6"/><path d="M-50 -78 Q-44 -126 0 -124 Q44 -126 50 -78 Q20 -100 -50 -78 Z" fill="${hair}"/><path d="M-80 60 Q-80 -10 0 -10 Q80 -10 80 60 Z" fill="${NAVY}"/><rect x="-100" y="50" width="200" height="14" rx="7" fill="${NAVY}"/><rect x="-86" y="2" width="172" height="52" rx="8" fill="#FFFFFF" stroke="${NAVY}" stroke-width="5"/><circle cx="0" cy="28" r="9" fill="${TEAL}"/>`;
  const check = (r = 38) => `<circle r="${r}" fill="${GRN}" stroke="${NAVY}" stroke-width="5"/><path d="M${-r * 0.47} ${r * 0.05} L${-r * 0.13} ${r * 0.4} L${r * 0.5} ${-r * 0.37}" fill="none" stroke="#FFFFFF" stroke-width="${r * 0.26}" stroke-linecap="round" stroke-linejoin="round"/>`;
  const cross = (r = 38) => `<circle r="${r}" fill="${RED}" stroke="${NAVY}" stroke-width="5"/><path d="M${-r * 0.4} ${-r * 0.4} L${r * 0.4} ${r * 0.4} M${r * 0.4} ${-r * 0.4} L${-r * 0.4} ${r * 0.4}" fill="none" stroke="#FFFFFF" stroke-width="${r * 0.26}" stroke-linecap="round"/>`;
  const counter = (l, t0, dur, to, fmt) => fmt(Math.round(to * smooth(pr(l, t0, dur))));
  const dots = (n) => n.toLocaleString('en-US').replace(/,/g, '.');
  const tvBox = (w, h, l, hue = 0) => {
    let sc = '';
    const cols = [RED, YEL, TEAL, '#8F7BFF', GRN];
    for (let i = 0; i < 5; i++) { const bw = w / 5 - 4, ph = (Math.sin(l * 3 + i * 1.3 + hue) + 1) / 2; sc += `<rect x="${f1(-w / 2 + 8 + i * (w - 16) / 5)}" y="${f1(h / 2 - 16 - (h - 56) * (0.3 + 0.7 * ph))}" width="${f1(bw - 4)}" height="${f1((h - 56) * (0.3 + 0.7 * ph))}" rx="6" fill="${cols[i]}"/>`; }
    return `<rect x="${-w / 2 - 14}" y="${-h / 2 - 14}" width="${w + 28}" height="${h + 28}" rx="22" fill="${NAVY}"/><rect x="${-w / 2}" y="${-h / 2}" width="${w}" height="${h}" rx="12" fill="#1B3358"/>${sc}<rect x="-70" y="${h / 2 + 14}" width="140" height="16" rx="8" fill="${NAVY}"/><rect x="-110" y="${h / 2 + 26}" width="220" height="12" rx="6" fill="${NAVY}"/>`;
  };
  const carSide = (k = 1, col = YEL) => `<g transform="scale(${k})"><path d="M-170 40 Q-170 -4 -130 -8 L-84 -66 Q-76 -80 -56 -80 H60 Q80 -80 94 -62 L138 -8 Q172 -4 172 40 Z" fill="${col}" stroke="${NAVY}" stroke-width="8" stroke-linejoin="round"/><path d="M-66 -12 L-40 -58 H54 L90 -12 Z" fill="${SKY}" stroke="${NAVY}" stroke-width="6" stroke-linejoin="round"/><circle cx="-100" cy="44" r="34" fill="${NAVY}"/><circle cx="-100" cy="44" r="14" fill="#B8C4D2"/><circle cx="104" cy="44" r="34" fill="${NAVY}"/><circle cx="104" cy="44" r="14" fill="#B8C4D2"/></g>`;
  const watchIc = (k = 1) => `<g transform="scale(${k})">${ICONS.watch()}</g>`;

  // ====== Video 12: TV thông minh ghi lại bạn xem gì ======
  const v12 = [];
  v12.push({ // 2: TV chỉ để xem?
    w: [['tv', 'TV'], ['xem', 'xem'], ['theo', 'theo']],
    point: [['tv', 540, 700], ['xem', 540, 600], ['theo', 540, 800]],
    draw(l, t) {
      let o = pop(l, 0.2, 540, 800, 1, tvBox(560, 330, l));
      o += myth(l, t.xem, null, 'TV chỉ để xem thôi?', 540, 470, 600);
      if (l >= t.theo) o += pop(l, t.theo, 860, 640, 1, `<circle r="64" fill="#FFFFFF" stroke="${NAVY}" stroke-width="6"/><g transform="scale(1.1)">${ICONS.eye()}</g>`);
      return o;
    },
  });
  v12.push({ // 3: tháng 2/2017 Vizio bị phạt 2,2 triệu đô
    w: [['khong', 'không'], ['thang', 'tháng'], ['phat', 'phạt']],
    point: [['thang', 220, 640], ['phat', 780, 760]],
    draw(l, t) {
      let o = myth(l, 0.1, t.khong, 'TV chỉ để xem thôi?', 540, 470, 600);
      o += pop(l, t.thang, 220, 760, 0.9, cal('THÁNG 2', '2017'));
      o += pop(l, t.thang + 0.3, 220, 960, 1, tag(0, 0, 'Hãng Vizio', 250));
      if (l >= t.phat) {
        o += pop(l, t.phat, 740, 740, 1, `<rect x="-280" y="-150" width="560" height="300" rx="34" fill="#FFFFFF" stroke="${RED}" stroke-width="10"/>${T(0, -70, 'BỊ PHẠT', 56, RED)}${T(0, 50, counter(l, t.phat, 1.6, 22, (n) => (n / 10).toFixed(1).replace('.', ',')) + ' triệu', 76, NAVY)}${T(0, 112, 'đô la', 44, NAVY, 700)}`);
        for (let i = 0; i < 5; i++) { const u = ((l - t.phat) * 0.8 + i / 5) % 1; o += `<g transform="translate(${f1(400 + i * 140)} ${f1(930 - 70 * u)})" opacity="${(1 - u).toFixed(2)}"><circle r="20" fill="${YEL}" stroke="${NAVY}" stroke-width="5"/>${T(0, 9, '$', 24, NAVY)}</g>`; }
      }
      return o;
    },
  });
  v12.push({ // 4: từ 2014, từng giây, 11 triệu TV
    w: [['nam', 'năm'], ['giay', 'giây'], ['trieu', 'triệu']],
    point: [['nam', 160, 620], ['giay', 260, 760], ['trieu', 540, 960]],
    draw(l, t) {
      let o = pop(l, t.nam, 160, 600, 0.55, cal('NĂM', '2014'));
      o += pop(l, 0.2, 280, 800, 1, tvBox(300, 190, l));
      o += pop(l, 0.3, 840, 800, 1, `<g transform="scale(1.6)">${ICONS.server()}</g>`);
      if (l >= t.giay) {
        for (let i = 0; i < 4; i++) { const u = ((l - t.giay) * 1.2 + i / 4) % 1; o += `<g transform="translate(${f1(lerp(430, 760, u))} ${f1(800 - 10 * Math.sin(Math.PI * u))})" opacity="${Math.sin(Math.PI * u).toFixed(2)}"><rect x="-26" y="-18" width="52" height="36" rx="6" fill="#FFFFFF" stroke="${NAVY}" stroke-width="4"/><rect x="-18" y="-10" width="36" height="20" rx="3" fill="${TEAL}"/></g>`; }
        o += pop(l, t.giay + 0.2, 560, 940, 1, tag(0, 0, 'Từng giây', 230));
        const sec = Math.floor((l - t.giay) % 10) + 1; o += pop(l, t.giay + 0.2, 280, 960, 1, T(0, 0, sec + ' giây', 40, NAVY));
      }
      if (l >= t.trieu) {
        for (let i = 0; i < 22; i++) { const x = 130 + (i % 11) * 82, y = 1060 + Math.floor(i / 11) * 62; o += pop(l, t.trieu + i * 0.05, x, y, 0.5, tvBox(70, 44, l, i)); }
        o += pop(l, t.trieu, 540, 1000, 1, T(0, 0, counter(l, t.trieu, 1.4, 11, (n) => n) + ' triệu TV', 64, YEL, 800, NAVY));
      }
      return o;
    },
  });
  v12.push({ // 5: phim cáp, DVD, mạng + tuổi, thu nhập
    w: [['cap', 'cáp'], ['dvd', 'DVD'], ['mang', 'mạng'], ['tuoi', 'tuổi'], ['thu', 'thu']],
    point: [['cap', 190, 600], ['dvd', 190, 740], ['mang', 190, 880], ['tuoi', 700, 900], ['thu', 700, 980]],
    draw(l, t) {
      const chip = (t0, y, lab, inner) => pop(l, t0, 190, y, 1, `<circle r="68" fill="#FFFFFF" stroke="${NAVY}" stroke-width="6"/>${inner}<text x="150" y="12" font-family="${FONT}" font-weight="800" font-size="34" fill="${NAVY}">${lab}</text>`);
      let o = chip(t.cap, 600, 'Phim cáp', `<rect x="-36" y="-24" width="72" height="48" rx="8" fill="${NAVY}"/><circle cx="-12" cy="0" r="8" fill="${TEAL}"/><rect x="6" y="-8" width="22" height="16" rx="4" fill="${YEL}"/>`);
      o += chip(t.dvd, 740, 'Đĩa DVD', `<circle r="38" fill="#CFE6F5" stroke="${NAVY}" stroke-width="6"/><circle r="12" fill="#FFFFFF" stroke="${NAVY}" stroke-width="5"/>`);
      o += chip(t.mang, 880, 'Phim trên mạng', `<g transform="scale(0.75)">${ICONS.cloud()}</g>`);
      const showBox = l >= t.cap + 0.6;
      if (showBox) {
        o += pop(l, t.cap + 0.6, 780, 740, 1, `${panel(-150, -150, 300, 300, '#FFFFFF', 26)}${T(0, -92, 'Dữ liệu xem', 34, NAVY)}${[-40, 10, 60].map((y, i) => `<rect x="-100" y="${y}" width="${f1(80 + 60 * ((Math.sin(l * 2 + i) + 1) / 2))}" height="16" rx="8" fill="${[RED, YEL, TEAL][i]}"/>`).join('')}`);
        for (let i = 0; i < 3; i++) { const tt = [t.cap, t.dvd, t.mang][i]; if (l >= tt) { const u = ((l - tt) * 0.9) % 1; o += `<g transform="translate(${f1(lerp(520, 640, u))} ${f1(lerp([600, 740, 880][i], 740, u))}) scale(0.5)" opacity="${(1 - u * 0.3).toFixed(2)}">${photo(60, 44)}</g>`; } }
      }
      if (l >= t.tuoi) o += pop(l, t.tuoi, 780, 950, 1, `<rect x="-170" y="-34" width="340" height="68" rx="34" fill="${YEL}" stroke="${NAVY}" stroke-width="6"/>${T(0, 14, '+ Tuổi', 42, NAVY)}`);
      if (l >= t.thu) o += pop(l, t.thu, 780, 1040, 1, `<rect x="-170" y="-34" width="340" height="68" rx="34" fill="${YEL}" stroke="${NAVY}" stroke-width="6"/>${T(0, 14, '+ Thu nhập', 42, NAVY)}`);
      return o;
    },
  });
  v12.push({ // 6: bán cho bên thứ ba, nhắm quảng cáo, không xin đồng ý
    w: [['ban', 'bán'], ['quang', 'quảng'], ['khong', 'không'], ['dongy', 'đồng']],
    point: [['ban', 540, 700], ['quang', 880, 760], ['khong', 540, 980], ['dongy', 300, 990]],
    draw(l, t) {
      let o = pop(l, 0.2, 190, 720, 1, `<circle r="90" fill="#FFFFFF" stroke="${NAVY}" stroke-width="6"/><g transform="scale(0.5) translate(0 -20)">${tvBox(150, 96, l)}</g>${lines(0, 140, 'Hãng TV', 32)}`);
      o += pop(l, t.ban, 880, 720, 1, `<circle r="90" fill="#FFFFFF" stroke="${NAVY}" stroke-width="6"/><rect x="-44" y="-46" width="88" height="92" rx="8" fill="${SKY}" stroke="${NAVY}" stroke-width="6"/><g fill="#FFFFFF">${[-24, 0, 24].map((x) => [-30, -4, 22].map((y) => `<rect x="${x - 8}" y="${y}" width="16" height="16" rx="3"/>`).join('')).join('')}</g>${lines(0, 140, 'Bên thứ ba', 32)}`);
      if (l >= t.ban) for (let i = 0; i < 3; i++) { const u = ((l - t.ban) * 0.8 + i / 3) % 1; o += `<g transform="translate(${f1(lerp(300, 770, u))} ${f1(720 - 30 * Math.sin(Math.PI * u))})"><circle r="18" fill="${YEL}" stroke="${NAVY}" stroke-width="5"/>${T(0, 8, '$', 22, NAVY)}</g>`; }
      if (l >= t.quang) o += pop(l, t.quang, 540, 560, 1, `<rect x="-290" y="-52" width="580" height="104" rx="26" fill="${NAVY}"/>${T(0, 16, 'Nhắm đúng quảng cáo', 50, YEL)}`);
      if (l >= t.khong) o += pop(l, t.khong, 540, 960, 1, `<rect x="-300" y="-44" width="600" height="88" rx="44" fill="#FFFFFF" stroke="${RED}" stroke-width="8"/>${T(0, 14, 'Không nói rõ cho người dùng', 36, RED)}`);
      if (l >= t.dongy) o += pop(l, t.dongy, 300, 1070, 1, `<rect x="-40" y="-40" width="80" height="80" rx="14" fill="#FFFFFF" stroke="${NAVY}" stroke-width="7"/>`) + pop(l, t.dongy + 0.4, 300, 1070, 1, cross(36)) + pop(l, t.dongy + 0.3, 640, 1070, 1, `${T(0, 0, 'Chưa xin đồng ý', 40, NAVY)}`);
      return o;
    },
  });
  v12.push({ // 7: nộp phạt, xóa dữ liệu, xin đồng ý trước
    w: [['phat', 'phạt'], ['xoa', 'xóa'], ['dongy', 'đồng']],
    point: [['phat', 190, 640], ['xoa', 540, 640], ['dongy', 890, 640]],
    draw(l, t) {
      const X = [190, 540, 890], Y = 650;
      let o = pop(l, t.phat, X[0], Y, 1, `<circle r="130" fill="#FFFFFF" stroke="${NAVY}" stroke-width="6"/><circle r="52" fill="${YEL}" stroke="${NAVY}" stroke-width="6"/>${T(0, 20, '$', 62, NAVY)}`);
      o += pop(l, t.phat + 0.2, X[0], Y + 230, 1, lines(0, 0, 'Nộp tiền phạt', 34));
      o += pop(l, t.xoa, X[1], Y, 1, `<circle r="130" fill="#FFFFFF" stroke="${NAVY}" stroke-width="6"/><rect x="-48" y="-30" width="96" height="100" rx="12" fill="#B8C4D2" stroke="${NAVY}" stroke-width="6"/><rect x="-62" y="-52" width="124" height="18" rx="9" fill="${NAVY}"/>`);
      if (l >= t.xoa) for (let i = 0; i < 3; i++) { const u = ((l - t.xoa) * 0.8 + i / 3) % 1; o += `<g transform="translate(${f1(X[1] + (i - 1) * 40)} ${f1(Y - 190 + 190 * u)}) scale(0.4)" opacity="${(1 - u).toFixed(2)}">${photo(60, 44)}</g>`; }
      o += pop(l, t.xoa + 0.2, X[1], Y + 230, 1, lines(0, 0, 'Xóa dữ liệu cũ', 34));
      o += pop(l, t.dongy, X[2], Y, 1, `<circle r="130" fill="#FFFFFF" stroke="${NAVY}" stroke-width="6"/><rect x="-44" y="-44" width="88" height="88" rx="14" fill="#FFFFFF" stroke="${NAVY}" stroke-width="7"/>`);
      if (l >= t.dongy + 0.4) o += `<g transform="translate(${X[2]} ${Y}) scale(${easeOutBack((l - t.dongy - 0.4) / 0.5).toFixed(2)})">${check(34)}</g>`;
      o += pop(l, t.dongy + 0.2, X[2], Y + 230, 1, lines(0, 0, 'Xin đồng ý|trước khi thu thập', 32));
      return o;
    },
  });
  v12.push({ // 8: cài đặt TV, tắt mục theo dõi
    w: [['cai', 'cài'], ['muc', 'mục'], ['tat', 'tắt']],
    point: [['cai', 540, 600], ['muc', 800, 800], ['tat', 800, 800]],
    draw(l, t) {
      const rows = ['Âm thanh', 'Hình ảnh', 'Theo dõi nội dung xem', 'Mạng'];
      let o = pop(l, t.cai - 0.2, 540, 790, 1, `${panel(-400, -230, 800, 470, '#FFFFFF', 30)}${T(0, -158, 'Cài đặt TV', 46, NAVY)}`);
      const on = l < t.tat + 0.2;
      rows.forEach((r, i) => {
        const y = 700 + i * 84, hi = i === 2, hl = hi && l >= t.muc;
        o += `<g opacity="${pr(l, t.cai + i * 0.2, 0.3).toFixed(2)}"><rect x="170" y="${y - 32}" width="740" height="64" rx="16" fill="${hl ? '#FFF3C4' : '#F1F5F9'}" stroke="${hl ? RED : 'none'}" stroke-width="6"/><text x="200" y="${y + 11}" font-family="${FONT}" font-weight="${hi ? 800 : 700}" font-size="32" fill="${NAVY}">${r}</text>${hi ? `<g transform="translate(840 ${y}) scale(0.55)">${toggle(on)}</g>` : ''}</g>`;
      });
      if (l >= t.tat + 0.3) o += pop(l, t.tat + 0.3, 540, 1060, 1, tag(0, 0, 'Tên mục khác nhau tùy hãng', 600, '#FFFFFF', NAVY, 32));
      return o;
    },
  });

  // ====== Video 13: bản đồ nhiệt Strava ======
  const v13 = [];
  const routeD = 'M-120 60 C-90 -20 -20 -40 20 10 S110 70 140 -10';
  v13.push({ // 2: ẩn danh thì không ai biết?
    w: [['nghi', 'nghĩ'], ['an', 'ẩn'], ['ai', 'ai']],
    point: [['nghi', 540, 600], ['an', 800, 760], ['ai', 800, 760]],
    draw(l, t) {
      let o = pop(l, 0.2, 260, 790, 1.7, watchIc(1));
      o += `<g transform="translate(260 760) scale(1.0)" opacity="${pr(l, 0.8, 0.4).toFixed(2)}"><path d="${routeD}" fill="none" stroke="${RED}" stroke-width="8" stroke-linecap="round" stroke-dasharray="500" stroke-dashoffset="${f1(500 * (1 - pr(l, 0.8, 2.5)))}" transform="translate(0 250)"/></g>`;
      o += myth(l, t.nghi, null, 'Ẩn danh thì không ai biết?', 540, 470, 640);
      if (l >= t.an) o += pop(l, t.an, 800, 780, 1, `<circle r="100" fill="#FFFFFF" stroke="${NAVY}" stroke-width="6"/><circle cx="0" cy="-24" r="34" fill="#B8C4D2"/><path d="M-54 56 Q-54 8 0 8 Q54 8 54 56 Z" fill="#B8C4D2"/>${T(0, 20, '?', 60, NAVY)}${T(0, 150, 'Ẩn danh', 36, NAVY)}`);
      return o;
    },
  });
  const mapBase = (x, y, w, h) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="26" fill="#0F2036" stroke="${NAVY}" stroke-width="6"/>`;
  const hotLines = (l, t0, x0, y0, w, h, n, seed = 0) => {
    let o = '';
    const CL = [[0.25, 0.35], [0.68, 0.6], [0.42, 0.8], [0.78, 0.25], [0.15, 0.75]];
    for (let i = 0; i < n; i++) {
      const tt = t0 + i * 0.1; if (l < tt) continue;
      const c = CL[(i + seed) % CL.length], j = ((i * 61 + seed * 17) % 100) / 100 - 0.5, k2 = ((i * 37 + seed * 11) % 100) / 100 - 0.5;
      const cx = x0 + w * c[0] + j * 120, cy = y0 + h * c[1] + k2 * 90, r = 40 + (i * 29) % 70, a = pr(l, tt, 0.5);
      const d = `M${f1(cx - r)} ${f1(cy + k2 * 40)} C${f1(cx - r / 2)} ${f1(cy - r)} ${f1(cx + r / 2)} ${f1(cy + r)} ${f1(cx + r)} ${f1(cy + j * 40)}`;
      o += `<path d="${d}" fill="none" stroke="#FF7A45" stroke-width="16" stroke-linecap="round" opacity="${(0.16 * a).toFixed(2)}"/><path d="${d}" fill="none" stroke="${i % 3 ? '#FFC53D' : '#FFE8A3'}" stroke-width="4" stroke-linecap="round" opacity="${(0.95 * a).toFixed(2)}"/>`;
    }
    return o;
  };
  v13.push({ // 3: tháng 11/2017 bản đồ nhiệt
    w: [['khong', 'không'], ['thang', 'tháng'], ['do', 'đồ'], ['sang', 'sáng']],
    point: [['thang', 210, 640], ['do', 700, 700], ['sang', 700, 700]],
    draw(l, t) {
      let o = myth(l, 0.1, t.khong, 'Ẩn danh thì không ai biết?', 540, 470, 640);
      o += pop(l, t.thang, 190, 780, 0.8, cal('THÁNG 11', '2017'));
      o += pop(l, t.thang + 0.3, 190, 960, 1, tag(0, 0, 'Strava', 200));
      if (l >= t.do) {
        o += pop(l, t.do, 690, 800, 1, mapBase(-300, -260, 600, 520));
        o += `<g transform="translate(690 800)">${hotLines(l, t.sang - 0.2, -300, -260, 600, 520, 40)}</g>`;
        o += pop(l, t.do + 0.3, 690, 1090, 1, tag(0, 0, 'Bản đồ nhiệt', 300));
      }
      return o;
    },
  });
  v13.push({ // 4: 13 nghìn tỷ điểm
    w: [['gom', 'gom'], ['nghin', 'nghìn'], ['diem', 'điểm']],
    point: [['gom', 540, 760], ['nghin', 540, 960], ['diem', 540, 960]],
    draw(l, t) {
      let o = pop(l, 0.2, 540, 760, 1, mapBase(-380, -230, 760, 460));
      o = `<g>${o}</g>`;
      o += `<g transform="translate(540 760)">${hotLines(l, t.gom - 0.2, -380, -230, 760, 460, 70, 3)}</g>`;
      if (l >= t.gom) for (let i = 0; i < 14; i++) { const u = ((l - t.gom) * 0.7 + i / 14) % 1, a = i * 2.4; o += `<circle cx="${f1(540 + Math.cos(a) * lerp(520, 40, u))}" cy="${f1(760 + Math.sin(a) * lerp(300, 30, u))}" r="6" fill="${YEL}" opacity="${(0.9 * (1 - u * 0.5)).toFixed(2)}"/>`; }
      if (l >= t.nghin) o += pop(l, t.nghin, 540, 1060, 1, `<rect x="-330" y="-52" width="660" height="104" rx="30" fill="${NAVY}"/>${T(0, 22, counter(l, t.nghin, 1.4, 13, (n) => n) + ' nghìn tỷ điểm', 58, YEL)}`);
      return o;
    },
  });
  const baseOutline = (x, y, k = 1) => `<g transform="translate(${x} ${y}) scale(${k})"><rect x="-190" y="-110" width="380" height="220" rx="24" fill="none" stroke="#FFB300" stroke-width="9" stroke-dasharray="26 12"/><rect x="-120" y="-60" width="240" height="120" rx="14" fill="none" stroke="#FF7A45" stroke-width="7"/><path d="M-190 0 H-260 M190 0 H260" stroke="#FFB300" stroke-width="7" stroke-linecap="round"/></g>`;
  v13.push({ // 5: cuối tháng 1/2018 sinh viên chỉ ra căn cứ quân sự
    w: [['cuoi', 'cuối'], ['sinh', 'sinh'], ['lo', 'lộ'], ['cu', 'căn']],
    point: [['cuoi', 200, 600], ['sinh', 190, 960], ['lo', 700, 760], ['cu', 700, 760]],
    draw(l, t) {
      let o = pop(l, t.cuoi, 190, 690, 0.8, cal('THÁNG 1', '2018'));
      o += pop(l, t.sinh, 190, 960, 0.9, `<g transform="scale(0.8) translate(0 -20)">${person('#5B3A1E')}</g>${lines(0, 90, 'Sinh viên|người Úc', 30)}`);
      o += pop(l, t.lo - 0.4, 700, 800, 1, mapBase(-300, -240, 600, 480));
      if (l >= t.lo - 0.4) {
        o += `<g transform="translate(700 800)">${hotLines(l, t.lo, -300, -240, 600, 480, 14, 7)}</g>`;
        const p = pr(l, t.lo + 0.2, 0.6);
        o += `<g opacity="${p.toFixed(2)}">${baseOutline(700, 800, 0.95)}</g>`;
        o += `<g transform="translate(700 800)"><circle r="${f1(180 + 14 * Math.sin(l * 5))}" fill="none" stroke="${RED}" stroke-width="7" opacity="${(0.9 * pr(l, t.cu, 0.4)).toFixed(2)}"/></g>`;
        if (l >= t.cu) o += pop(l, t.cu, 700, 1100, 1, tag(0, 0, 'Căn cứ quân sự', 380, RED, '#FFFFFF', 36));
      }
      return o;
    },
  });
  v13.push({ // 6: lính chạy vòng, thói quen lặp lại
    w: [['linh', 'lính'], ['tuan', 'tuần'], ['lap', 'lặp'], ['thoi', 'thói']],
    point: [['linh', 540, 760], ['lap', 540, 760], ['thoi', 540, 1040]],
    draw(l, t) {
      let o = mapBase(60, 480, 960, 560) + baseOutline(540, 760, 1.5);
      const loopP = (u) => { const a = u * Math.PI * 2; return [540 + 330 * Math.cos(a), 760 + 150 * Math.sin(a)]; };
      if (l >= t.linh) {
        for (let k = 0; k < 3; k++) {
          const e = (l - t.linh) * (0.35 + k * 0.05); const [x, y] = loopP((e + k / 3) % 1);
          o += pop(l, t.linh + k * 0.2, x, y, 0.8, `<circle r="26" fill="${GRN}" stroke="#FFFFFF" stroke-width="5"/><circle r="9" fill="#FFFFFF"/>`);
        }
      }
      if (l >= t.tuan) {
        const n = Math.min(60, Math.floor((l - t.tuan) * 14));
        let d = ''; for (let i = 0; i <= n; i++) { const [x, y] = loopP(i / 20); d += (i ? 'L' : 'M') + f1(x) + ' ' + f1(y); }
        o += `<path d="${d}" fill="none" stroke="#FFB300" stroke-width="${4 + Math.min(8, (l - t.tuan) * 1.5)}" stroke-linecap="round" opacity="0.9"/>`;
      }
      if (l >= t.lap) o += pop(l, t.lap, 540, 1090, 1, tag(0, 0, 'Đi lặp lại mỗi ngày', 480));
      if (l >= t.thoi) o += pop(l, t.thoi, 540, 560, 1, `<rect x="-300" y="-44" width="600" height="88" rx="44" fill="${RED}"/>${T(0, 14, 'Lộ thói quen sinh hoạt', 40, '#FFFFFF')}`);
      return o;
    },
  });
  v13.push({ // 7: riêng tư thì không lên bản đồ, có thể tắt chia sẻ
    w: [['rieng', 'riêng'], ['khong', 'không'], ['tat', 'tắt']],
    point: [['rieng', 250, 700], ['khong', 700, 800], ['tat', 860, 1000]],
    draw(l, t) {
      let o = pop(l, 0.2, 250, 760, 1, `${panel(-170, -170, 340, 340, '#FFFFFF', 26)}<path d="${routeD}" transform="translate(0 -10) scale(0.9)" fill="none" stroke="${RED}" stroke-width="9" stroke-linecap="round"/>${T(0, 130, 'Hoạt động', 32, NAVY)}`);
      if (l >= t.rieng) o += pop(l, t.rieng, 340, 600, 0.9, `<circle r="46" fill="#FFFFFF" stroke="${NAVY}" stroke-width="6"/><g transform="scale(0.55)">${ICONS.lock()}</g>`) + pop(l, t.rieng + 0.2, 250, 990, 1, tag(0, 0, 'Riêng tư', 220, NAVY, YEL));
      o += pop(l, 0.3, 760, 760, 1, mapBase(-210, -170, 420, 340));
      o += `<g transform="translate(760 760)">${hotLines(l, 0.5, -210, -170, 420, 340, 14, 5)}</g>`;
      if (l >= t.khong) { const a = pr(l, t.khong, 0.4); o += `<g transform="translate(540 760)" opacity="${a.toFixed(2)}"><path d="M-30 0 H80" stroke="${NAVY}" stroke-width="8" stroke-dasharray="12 12"/><g transform="translate(25 0)">${cross(30)}</g></g>`; }
      if (l >= t.tat) o += pop(l, t.tat, 760, 1030, 1, `<rect x="-250" y="-50" width="500" height="100" rx="30" fill="#FFFFFF" stroke="${NAVY}" stroke-width="6"/>${T(-60, 12, 'Chia sẻ', 36, NAVY)}<g transform="translate(130 0) scale(0.8)">${toggle(l < t.tat + 0.4)}</g>`);
      return o;
    },
  });
  v13.push({ // 8: ba việc làm được
    w: [['rieng', 'riêng'], ['vung', 'vùng'], ['tat', 'tắt']],
    point: [['rieng', 190, 640], ['vung', 540, 640], ['tat', 890, 640]],
    draw(l, t) {
      const X = [190, 540, 890], Y = 650;
      let o = pop(l, t.rieng, X[0], Y, 1, `<circle r="130" fill="#FFFFFF" stroke="${NAVY}" stroke-width="6"/><g transform="scale(1.6)">${ICONS.lock()}</g>`);
      o += pop(l, t.rieng + 0.2, X[0], Y + 230, 1, lines(0, 0, 'Hoạt động|riêng tư', 34));
      o += pop(l, t.vung, X[1], Y, 1, `<circle r="130" fill="#FFFFFF" stroke="${NAVY}" stroke-width="6"/><path d="M-60 20 L0 -40 L60 20 V70 H-60 Z" fill="${YEL}" stroke="${NAVY}" stroke-width="6" stroke-linejoin="round"/><rect x="-14" y="30" width="28" height="40" fill="${NAVY}"/>`);
      if (l >= t.vung) o += `<g transform="translate(${X[1]} ${Y})"><circle r="${f1(112 + 6 * Math.sin(l * 4))}" fill="none" stroke="${TEAL}" stroke-width="7" stroke-dasharray="16 10"/></g>`;
      o += pop(l, t.vung + 0.2, X[1], Y + 230, 1, lines(0, 0, 'Vùng ẩn|quanh nhà', 34));
      o += pop(l, t.tat, X[2], Y, 1, `<circle r="130" fill="#FFFFFF" stroke="${NAVY}" stroke-width="6"/><g transform="translate(0 -10) scale(1.2)">${toggle(l < t.tat + 0.5)}</g>${T(0, 80, 'Bản đồ nhiệt', 28, NAVY, 700)}`);
      o += pop(l, t.tat + 0.2, X[2], Y + 230, 1, lines(0, 0, 'Tắt đóng góp|dữ liệu', 34));
      return o;
    },
  });

  // ====== Video 14: xe bị điều khiển từ xa ======
  const v14 = [];
  v14.push({ // 2: xe hơi không phải thiết bị mạng?
    w: [['nghi', 'nghĩ'], ['ket', 'kết'], ['ai', 'ai']],
    point: [['nghi', 540, 600], ['ket', 540, 800], ['ai', 540, 800]],
    draw(l, t) {
      let o = pop(l, 0.2, 540, 800, 1.5, carSide(1));
      o += myth(l, t.nghi, null, 'Xe hơi đâu phải thiết bị mạng?', 540, 470, 700);
      if (l >= t.ket) o += pop(l, t.ket, 540, 640, 0.001 + 1, `<g opacity="0.9">${[0, 1, 2].map((i) => `<path d="M${-40 - i * 22} ${-10 - i * 10} Q0 ${-50 - i * 20} ${40 + i * 22} ${-10 - i * 10}" fill="none" stroke="${NAVY}" stroke-width="8" stroke-linecap="round" opacity="${(0.9 - i * 0.25).toFixed(2)}"/>`).join('')}<circle cy="14" r="9" fill="${NAVY}"/></g>`);
      return o;
    },
  });
  v14.push({ // 3: hệ thống giải trí nối mạng = cửa vào xe
    w: [['khong', 'không'], ['giai', 'giải'], ['cua', 'cửa']],
    point: [['giai', 540, 800], ['cua', 760, 800]],
    draw(l, t) {
      let o = myth(l, 0.1, t.khong, 'Xe hơi đâu phải thiết bị mạng?', 540, 470, 700);
      o += pop(l, 0.2, 400, 850, 1.4, carSide(1));
      if (l >= t.giai) {
        o += pop(l, t.giai, 400, 782, 1, `<rect x="-40" y="-24" width="80" height="46" rx="8" fill="#1B3358" stroke="${NAVY}" stroke-width="5"/><rect x="-32" y="-16" width="64" height="30" rx="5" fill="${TEAL}" opacity="${(0.6 + 0.3 * Math.sin(l * 5)).toFixed(2)}"/>`);
        o += pop(l, t.giai + 0.2, 400, 1030, 1, tag(0, 0, 'Hệ thống giải trí', 340));
        for (let i = 0; i < 3; i++) { const u = ((l - t.giai) * 0.8 + i / 3) % 1; o += `<path d="M${f1(450 + u * 160)} ${f1(782 - 40 * (0.4 + u))} Q${f1(470 + u * 170)} 782 ${f1(450 + u * 160)} ${f1(782 + 40 * (0.4 + u))}" fill="none" stroke="${NAVY}" stroke-width="8" stroke-linecap="round" opacity="${(1 - u).toFixed(2)}"/>`; }
        o += pop(l, t.giai + 0.5, 900, 700, 1, `<g transform="scale(1.1)">${ICONS.cloud()}</g>`);
      }
      if (l >= t.cua) {
        const op = easeOutBack((l - t.cua) / 0.5);
        o += `<g transform="translate(540 830) scale(${op.toFixed(2)})"><rect x="-34" y="-70" width="68" height="140" rx="10" fill="${RED}" fill-opacity="0.2" stroke="${RED}" stroke-width="8" stroke-dasharray="14 10"/><path d="M-6 -10 H18" stroke="${RED}" stroke-width="8" stroke-linecap="round"/></g>`;
        o += pop(l, t.cua + 0.2, 640, 590, 1, tag(0, 0, 'Một cánh cửa vào xe', 400, RED, '#FFFFFF', 34));
      }
      return o;
    },
  });
  v14.push({ // 4: tháng 7/2015, hai nhà nghiên cứu điều khiển Jeep
    w: [['thang', 'tháng'], ['nha', 'nhà'], ['jeep', 'Jeep']],
    point: [['thang', 190, 620], ['nha', 380, 680], ['jeep', 780, 800]],
    draw(l, t) {
      let o = pop(l, t.thang, 190, 740, 0.75, cal('THÁNG 7', '2015'));
      o += pop(l, t.nha, 330, 960, 0.85, `<g transform="translate(-60 0)">${person('#3B2314')}</g><g transform="translate(70 20) scale(0.9)">${person('#E7B04A', '#E8B994')}</g>`);
      o += pop(l, t.nha + 0.3, 330, 1110, 1, lines(0, 0, 'Hai nhà nghiên cứu', 32));
      if (l >= t.jeep) {
        o += pop(l, t.jeep, 790, 830, 1.1, carSide(1, '#7BC96F'));
        for (let i = 0; i < 4; i++) { const u = ((l - t.jeep) * 0.7 + i / 4) % 1; o += `<circle cx="${f1(lerp(450, 700, u))}" cy="${f1(800 - 60 * Math.sin(Math.PI * u))}" r="9" fill="${i % 2 ? YEL : TEAL}" stroke="${NAVY}" stroke-width="3"/>`; }
        o += pop(l, t.jeep + 0.3, 790, 1010, 1, tag(0, 0, 'Jeep Cherokee', 330));
      }
      return o;
    },
  });
  v14.push({ // 5: gạt nước, đồng hồ, giảm tốc xuống dừng
    w: [['gat', 'gạt'], ['dong', 'đồng'], ['giam', 'giảm']],
    point: [['gat', 300, 660], ['dong', 780, 660], ['giam', 540, 1000]],
    draw(l, t) {
      let o = '';
      // gạt nước
      o += pop(l, 0.2, 280, 700, 1, `<path d="M-130 80 Q-130 -90 0 -110 Q130 -90 130 80 Z" fill="${SKY}" stroke="${NAVY}" stroke-width="8"/>`);
      if (l >= t.gat) { const a = 70 * Math.sin((l - t.gat) * 6); o += `<g transform="translate(0 0)"><g transform="translate(280 770) rotate(${f1(a)})"><line x1="0" y1="0" x2="0" y2="-150" stroke="${NAVY}" stroke-width="10" stroke-linecap="round"/></g></g>`; o += pop(l, t.gat + 0.2, 280, 900, 1, tag(0, 0, 'Gạt nước tự chạy', 330)); }
      // đồng hồ tốc độ
      const sp = l < t.giam ? (l >= t.dong ? 40 + 110 * ((Math.sin((l - t.dong) * 7) + 1) / 2) : 120) : 120 * (1 - smooth(pr(l, t.giam, 3.5)));
      o += pop(l, t.dong - 0.1, 790, 700, 1, `<path d="M-130 70 A130 130 0 0 1 130 70 Z" fill="#FFFFFF" stroke="${NAVY}" stroke-width="8"/><g transform="translate(0 70) rotate(${f1(-90 + sp * 1.2)})"><line x1="0" y1="0" x2="0" y2="-100" stroke="${RED}" stroke-width="9" stroke-linecap="round"/></g><circle cx="0" cy="70" r="14" fill="${NAVY}"/>`);
      if (l >= t.dong) o += pop(l, t.dong + 0.2, 790, 900, 1, tag(0, 0, 'Đồng hồ nhảy loạn', 330));
      // xe giảm tốc
      if (l >= t.giam) {
        const x = 540 + 180 * smooth(pr(l, t.giam, 3.5)) - 90;
        o += `<g transform="translate(${f1(x)} 1050) scale(0.6)">${carSide(1)}</g>`;
        o += pop(l, t.giam, 540, 1160, 1, T(0, 0, Math.round(sp * 1.0) + ' km/giờ' + (sp < 2 ? ' · DỪNG' : ''), 44, YEL, 800, NAVY));
      }
      return o;
    },
  });
  v14.push({ // 6: thu hồi 1,4 triệu xe
    w: [['hang', 'hãng'], ['thu', 'thu'], ['trieu', 'triệu']],
    point: [['hang', 540, 640], ['thu', 540, 800], ['trieu', 540, 1000]],
    draw(l, t) {
      let o = pop(l, t.hang, 540, 600, 1, `<rect x="-250" y="-44" width="500" height="88" rx="44" fill="${NAVY}"/>${T(0, 14, 'Hãng Fiat Chrysler', 40, YEL)}`);
      if (l >= t.thu) {
        for (let i = 0; i < 18; i++) {
          const c = i % 6, r = Math.floor(i / 6), u = pr(l, t.thu + i * 0.07, 0.6);
          o += `<g transform="translate(${f1(130 + c * 164 + 600 * (1 - smooth(u)))} ${f1(740 + r * 105)}) scale(0.4)" opacity="${u.toFixed(2)}">${carSide(1, [YEL, '#7BC96F', '#FF9A6B'][i % 3])}</g>`;
        }
        o += pop(l, t.thu + 0.3, 880, 700, 1, `<rect x="-130" y="-34" width="260" height="68" rx="14" fill="${RED}" stroke="#FFFFFF" stroke-width="5" transform="rotate(-8)"/>${T(0, 14, 'THU HỒI', 44, '#FFFFFF').replace('<text', '<text transform="rotate(-8)"')}`);
      }
      if (l >= t.trieu) o += pop(l, t.trieu, 540, 1060, 1, `<rect x="-300" y="-52" width="600" height="104" rx="30" fill="#FFFFFF" stroke="${NAVY}" stroke-width="6"/>${T(0, 22, counter(l, t.trieu, 1.4, 14, (n) => (n / 10).toFixed(1).replace('.', ',')) + ' triệu xe', 58, NAVY)}`);
      return o;
    },
  });
  v14.push({ // 7: cơ quan an toàn xem xét; bài học cập nhật
    w: [['co', 'cơ'], ['xem', 'xem'], ['bai', 'bài'], ['cap', 'cập']],
    point: [['co', 300, 700], ['xem', 300, 700], ['bai', 700, 700], ['cap', 800, 950]],
    draw(l, t) {
      let o = pop(l, t.co, 280, 800, 1, `${panel(-170, -190, 340, 380, '#FFFFFF', 26)}${T(0, -130, 'Đợt thu hồi', 34, NAVY)}${[-60, 10, 80].map((y) => `<rect x="-110" y="${y - 8}" width="${y === 80 ? 120 : 210}" height="16" rx="8" fill="${NAVY}" fill-opacity="0.25"/>`).join('')}`);
      if (l >= t.xem) {
        const mx = 280 + 40 * Math.sin((l - t.xem) * 2), my = 800 + 20 * Math.cos((l - t.xem) * 2.4);
        o += `<g transform="translate(${f1(mx + 60)} ${f1(my - 10)})"><circle r="60" fill="#FFFFFF" fill-opacity="0.3" stroke="${NAVY}" stroke-width="9"/><line x1="42" y1="42" x2="96" y2="96" stroke="${NAVY}" stroke-width="14" stroke-linecap="round"/></g>`;
        o += pop(l, t.xem + 0.3, 280, 1060, 1, tag(0, 0, 'Có hiệu quả không?', 400));
      }
      if (l >= t.bai) o += pop(l, t.bai, 780, 780, 1, `${panel(-220, -150, 440, 300, '#FFF3C4', 26)}${T(0, -80, 'Bài học', 38, RED)}${lines(0, -20, 'Thiết bị nối mạng|nào cũng cần|được cập nhật', 36)}`);
      if (l >= t.cap) {
        const p = pr(l, t.cap, 2.2);
        o += pop(l, t.cap, 780, 1020, 1, `<rect x="-220" y="-14" width="440" height="28" rx="14" fill="${NAVY}" fill-opacity="0.2"/><rect x="-220" y="-14" width="${f1(440 * p)}" height="28" rx="14" fill="${p >= 1 ? GRN : YEL}"/>${T(0, 62, p >= 1 ? 'Đã cập nhật' : 'Đang cập nhật...', 34, NAVY)}`);
      }
      return o;
    },
  });
  v14.push({ // 8: ba việc làm được
    w: [['cap', 'cập'], ['kiem', 'kiểm'], ['dot', 'đợt']],
    point: [['cap', 300, 700], ['kiem', 800, 700], ['dot', 800, 700]],
    draw(l, t) {
      const Y = 680;
      let o = pop(l, 0.2, 280, Y, 1, `<circle r="140" fill="#FFFFFF" stroke="${NAVY}" stroke-width="6"/><g transform="translate(0 20) scale(0.5)">${carSide(1)}</g>`);
      if (l >= t.cap) { const p = pr(l, t.cap, 2.4); o += pop(l, t.cap, 280, Y + 190, 1, `<rect x="-150" y="-12" width="300" height="24" rx="12" fill="${NAVY}" fill-opacity="0.2"/><rect x="-150" y="-12" width="${f1(300 * p)}" height="24" rx="12" fill="${p >= 1 ? GRN : YEL}"/>`) + pop(l, t.cap + 0.2, 280, Y + 270, 1, lines(0, 0, 'Cập nhật phần mềm|khi hãng thông báo', 32)); }
      if (l >= t.kiem) {
        o += pop(l, t.kiem, 800, Y, 1, `<circle r="140" fill="#FFFFFF" stroke="${NAVY}" stroke-width="6"/>${[-50, 0, 50].map((y, i) => `<rect x="-90" y="${y - 12}" width="${i === 1 ? 110 : 150}" height="24" rx="12" fill="${NAVY}" fill-opacity="0.25"/>`).join('')}`);
        const sy = -50 + 50 * ((Math.sin((l - t.kiem) * 3) + 1) / 2) * 2; o += `<g transform="translate(830 ${f1(Y + sy - 40)})"><circle r="44" fill="#FFFFFF" fill-opacity="0.3" stroke="${NAVY}" stroke-width="9"/><line x1="32" y1="32" x2="70" y2="70" stroke="${NAVY}" stroke-width="12" stroke-linecap="round"/></g>`;
      }
      if (l >= t.dot) o += pop(l, t.dot, 800, Y + 230, 1, lines(0, 0, 'Kiểm tra xe có trong|đợt thu hồi nào không', 32));
      return o;
    },
  });
  return { v11, v12, v13, v14 };
};
