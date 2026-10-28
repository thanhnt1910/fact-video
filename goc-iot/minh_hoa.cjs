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

  return { v11 };
};
