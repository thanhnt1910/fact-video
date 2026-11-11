import React from 'react';
import {Arrow, Bar, Big, C, Calc, Dash, Head, HatHero, Lab, Panel, Tag, clamp01, lerp, sp} from '../khoahoc/kit';

const YEL = '#f2c14e';
const GRY = '#8d8a84';
const STONE = '#6e6258';
const HOT = '#e0613b';
const GRN = '#6fd18f';

const Earth: React.FC<{x: number; y: number; r: number; o?: number}> = ({x, y, r, o = 1}) => (
  <g opacity={clamp01(o)}>
    <circle cx={x} cy={y} r={r} fill="#2f6fa8" stroke={C.cream} strokeWidth={6} />
    <path d={`M ${x - r * 0.5} ${y - r * 0.55} q ${r * 0.35} ${-r * 0.1} ${r * 0.5} ${r * 0.2} q ${-r * 0.1} ${r * 0.4} ${-r * 0.45} ${r * 0.35} z`} fill="#4f9a5a" />
    <path d={`M ${x + r * 0.1} ${y + r * 0.15} q ${r * 0.4} ${-r * 0.1} ${r * 0.5} ${r * 0.25} q ${-r * 0.2} ${r * 0.4} ${-r * 0.5} ${r * 0.2} z`} fill="#4f9a5a" />
  </g>
);
// Viên đá: tâm (x, y), tỉ lệ s.
const Rock: React.FC<{x: number; y: number; s?: number; o?: number; fill?: string}> = ({x, y, s = 1, o = 1, fill = STONE}) => (
  <g opacity={clamp01(o)} transform={`translate(${x} ${y}) scale(${s})`}>
    <path d="M -210 90 L -240 -10 L -170 -110 L -40 -150 L 110 -130 L 220 -40 L 240 70 L 150 110 Z" fill={fill} stroke={C.cream} strokeWidth={6 / s} strokeLinejoin="round" />
    <path d="M -120 -60 L -30 -20 L 40 -90 M 60 20 L 150 -10 M -150 40 L -80 70" fill="none" stroke="#4a3f36" strokeWidth={5 / s} strokeLinecap="round" />
  </g>
);
// Đồng hồ: tâm (x, y), bán kính r, spin = số vòng kim phút.
const Clock: React.FC<{x: number; y: number; r: number; spin?: number; o?: number}> = ({x, y, r, spin = 0, o = 1}) => {
  const am = spin * 2 * Math.PI - Math.PI / 2;
  const ah = (spin / 12) * 2 * Math.PI - Math.PI / 2;
  return (
    <g opacity={clamp01(o)}>
      <circle cx={x} cy={y} r={r} fill="#1a120d" stroke={C.amber} strokeWidth={r * 0.08} />
      {[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11].map((i) => {
        const a = (i / 12) * 2 * Math.PI;
        return <line key={i} x1={x + Math.cos(a) * r * 0.82} y1={y + Math.sin(a) * r * 0.82} x2={x + Math.cos(a) * r * 0.92} y2={y + Math.sin(a) * r * 0.92} stroke={C.cream} strokeWidth={r * 0.05} strokeLinecap="round" />;
      })}
      <line x1={x} y1={y} x2={x + Math.cos(am) * r * 0.72} y2={y + Math.sin(am) * r * 0.72} stroke={C.cream} strokeWidth={r * 0.06} strokeLinecap="round" />
      <line x1={x} y1={y} x2={x + Math.cos(ah) * r * 0.46} y2={y + Math.sin(ah) * r * 0.46} stroke={C.amber} strokeWidth={r * 0.09} strokeLinecap="round" />
      <circle cx={x} cy={y} r={r * 0.07} fill={C.amber} />
    </g>
  );
};
const Atom: React.FC<{x: number; y: number; r?: number; color?: string; label?: string; o?: number}> = ({x, y, r = 40, color = YEL, label, o = 1}) => (
  <g opacity={clamp01(o)}>
    <circle cx={x} cy={y} r={r} fill={color} stroke={C.cream} strokeWidth={5} />
    {label && (
      <text x={x} y={y + r * 0.36} textAnchor="middle" fontFamily="BeVN" fontWeight={800} fontSize={r * 0.95} fill={C.ink}>{label}</text>
    )}
  </g>
);
// Lưới 10 x 10 nguyên tử: n chấm đầu là xám (đã hóa chì), còn lại vàng.
const Grid: React.FC<{x: number; y: number; gray: number; cell?: number; o?: number}> = ({x, y, gray, cell = 52, o = 1}) => (
  <g opacity={clamp01(o)}>
    {Array.from({length: 100}).map((_, i) => {
      const cx = x + (i % 10) * cell;
      const cy = y + Math.floor(i / 10) * cell;
      const g = i < Math.round(gray);
      return <circle key={i} cx={cx} cy={cy} r={cell * 0.36} fill={g ? GRY : YEL} stroke={C.cream} strokeWidth={2.5} opacity={g ? 0.75 : 1} />;
    })}
  </g>
);
const Cookie: React.FC<{x: number; y: number; r?: number; o?: number}> = ({x, y, r = 46, o = 1}) => (
  <g opacity={clamp01(o)}>
    <circle cx={x} cy={y} r={r} fill="#c98a4b" stroke={C.cream} strokeWidth={5} />
    <circle cx={x - r * 0.3} cy={y - r * 0.2} r={r * 0.1} fill="#4a2f1b" />
    <circle cx={x + r * 0.25} cy={y - r * 0.3} r={r * 0.1} fill="#4a2f1b" />
    <circle cx={x + r * 0.05} cy={y + r * 0.3} r={r * 0.1} fill="#4a2f1b" />
  </g>
);
const Book: React.FC<{x: number; y: number; s?: number; o?: number}> = ({x, y, s = 1, o = 1}) => (
  <g opacity={clamp01(o)} transform={`translate(${x} ${y}) scale(${s})`} strokeLinejoin="round">
    <path d="M -230 -130 L 0 -100 L 0 130 L -230 100 Z" fill="#8a5f3a" stroke={C.cream} strokeWidth={6 / s} />
    <path d="M 230 -130 L 0 -100 L 0 130 L 230 100 Z" fill="#a07448" stroke={C.cream} strokeWidth={6 / s} />
    {[-60, -20, 20, 60].map((y0, i) => (
      <g key={i} stroke="#3a2818" strokeWidth={5 / s} opacity={0.6}>
        <line x1={-190} y1={y0 - 30 + i * 0.5} x2={-40} y2={y0 - 12} />
        <line x1={40} y1={y0 - 12} x2={190} y2={y0 - 30} />
      </g>
    ))}
  </g>
);
const Cup: React.FC<{x: number; y: number; f: number; temp: number}> = ({x, y, f, temp}) => (
  <g>
    <path d={`M ${x - 90} ${y - 110} L ${x + 90} ${y - 110} L ${x + 70} ${y + 90} L ${x - 70} ${y + 90} Z`} fill={`rgb(${Math.round(lerp(70, 224, temp))}, ${Math.round(lerp(120, 97, temp))}, ${Math.round(lerp(190, 59, temp))})`} stroke={C.cream} strokeWidth={6} />
    <path d={`M ${x + 90} ${y - 60} q 70 10 -10 100`} fill="none" stroke={C.cream} strokeWidth={6} />
    {[-40, 0, 40].map((dx, i) => (
      <path key={i} d={`M ${x + dx} ${y - 130} q 14 -30 0 -60 q -14 -30 0 -60`} fill="none" stroke={C.cream} strokeWidth={5} strokeLinecap="round" opacity={temp * (0.4 + 0.3 * Math.sin(f * 0.15 + i))} transform={`translate(0 ${-((f * 0.6 + i * 20) % 30)})`} />
    ))}
  </g>
);
const Meteor: React.FC<{x: number; y: number; s?: number; o?: number}> = ({x, y, s = 1, o = 1}) => (
  <g opacity={clamp01(o)} transform={`translate(${x} ${y}) scale(${s})`}>
    <path d="M -90 10 L -60 -70 L 20 -90 L 90 -40 L 80 40 L 10 80 Z" fill="#5b5560" stroke={C.cream} strokeWidth={6 / s} strokeLinejoin="round" />
    <circle cx={-20} cy={-10} r={14} fill="#3d3942" />
    <circle cx={35} cy={20} r={10} fill="#3d3942" />
  </g>
);

// --- Cảnh 1: câu hỏi và viên đá ---
const P0: Panel = ({f}) => (
  <g>
    <Head a="Làm sao biết Trái Đất" b="bao nhiêu tuổi?" />
    <Earth x={640} y={820} r={230} o={sp(f, 4, 20)} />
    <Big x={640} y={900} size={250} color={C.cream} o={0.9 * sp(f, 16, 32)}>?</Big>
    <Tag x={640} y={1170} color={C.cream} size={46} o={sp(f, 30, 46)}>chẳng ai có mặt để đếm</Tag>
    <HatHero x={170} y={1250} s={2} walk={f * 0.1} hat="helmet" />
  </g>
);
const P1: Panel = ({f}) => (
  <g>
    <Head a="Đáp án nằm ngay" b="trong những viên đá" />
    <Rock x={650} y={960} s={1.35} o={sp(f, 4, 20)} />
    <HatHero x={170} y={1250} s={2} walk={f * 0.2} cheer={sp(f, 14, 30)} hat="helmet" />
  </g>
);
const P2: Panel = ({f}) => (
  <g>
    <Head a="Mỗi viên đá giữ" b="một chiếc đồng hồ" />
    <Rock x={650} y={960} s={1.35} />
    <Clock x={650} y={950} r={120} spin={f * 0.03} o={sp(f, 6, 22)} />
    <Tag x={650} y={1170} color={C.amber} size={46} o={sp(f, 26, 42)}>chạy bằng nguyên tử</Tag>
    <HatHero x={170} y={1250} s={2} walk={f * 0.12} hat="helmet" />
  </g>
);
const P3: Panel = ({f}) => (
  <g>
    <Head a="Chiếc đồng hồ ấy" b="chạy thế nào?" />
    <Clock x={540} y={850} r={230} spin={f * 0.02} o={sp(f, 4, 20)} />
    <Big x={540} y={1170} size={150} color={C.amber} o={0.9 * sp(f, 20, 36)}>?</Big>
  </g>
);

// --- Cảnh 2: Át-sơ ---
const P4: Panel = ({f}) => (
  <g>
    <Head a="Người xưa chỉ có thể" b="đoán tuổi Trái Đất" />
    <Book x={680} y={940} s={1.3} o={sp(f, 4, 20)} />
    <Big x={680} y={560} size={130} color={C.amber} o={0.9 * sp(f, 18, 34)}>?</Big>
    <HatHero x={170} y={1250} s={2} walk={f * 0.1} hat="scholar" />
  </g>
);
const P5: Panel = ({f}) => (
  <g>
    <Head a="Năm 1650, một giáo sĩ" b="cộng số đời người" />
    <Book x={680} y={960} s={1.2} />
    <Big x={680} y={600} size={170} color={C.amber} o={sp(f, 10, 28)}>1650</Big>
    <Tag x={680} y={1190} color={C.cream} size={44} o={sp(f, 26, 42)}>từ thuở khai thiên lập địa</Tag>
    <HatHero x={170} y={1250} s={2} walk={f * 0.12} hat="scholar" />
  </g>
);
const P6: Panel = ({f}) => (
  <g>
    <Head a="Át-sơ: năm 4004 TCN" b="Trái Đất hơn 6 000 năm" />
    <Big x={540} y={640} size={150} color={C.amber} o={sp(f, 6, 24)}>4004 TCN</Big>
    <Bar x={110} y={800} w={860} color={YEL} p={sp(f, 18, 44) * 0.012 + 0.01} />
    <Tag x={110} y={900} color={C.cream} size={42} anchor="start" o={sp(f, 36, 50)}>hơn 6 000 năm</Tag>
    <HatHero x={540} y={1250} s={2} walk={f * 0.15} hat="scholar" />
  </g>
);

// --- Cảnh 3: Ken-vin ---
const P7: Panel = ({f}) => (
  <g>
    <Head a="Thế kỷ 19, Ken-vin nghĩ" b="Trái Đất từng nóng rực" />
    <circle cx={660} cy={880} r={240 + 6 * Math.sin(f * 0.2)} fill={HOT} opacity={0.25} />
    <circle cx={660} cy={880} r={210} fill={HOT} stroke={C.cream} strokeWidth={6} opacity={sp(f, 4, 20)} />
    <Tag x={660} y={1190} color={C.cream} size={44} o={sp(f, 24, 40)}>quả cầu nóng rực, rồi nguội dần</Tag>
    <HatHero x={150} y={1250} s={2} walk={f * 0.1} hat="scholar" />
  </g>
);
const P8: Panel = ({f}) => (
  <g>
    <Head a="Như một cốc nước nóng" b="nguội dần theo thời gian" />
    <Cup x={640} y={900} f={f} temp={1 - sp(f, 8, 70) * 0.9} />
    <Tag x={640} y={1150} color={C.amber} size={44} o={sp(f, 30, 46)}>nguội nhanh cỡ nào</Tag>
    <Tag x={640} y={1210} color={C.cream} size={44} o={sp(f, 40, 56)}>thì biết đã nguội bao lâu</Tag>
    <HatHero x={150} y={1250} s={2} walk={f * 0.1} hat="scholar" />
  </g>
);
const P9: Panel = ({f}) => (
  <g>
    <Head a="Năm 1897, Ken-vin tính" b="Trái Đất chỉ vài chục triệu năm" />
    <Big x={540} y={700} size={120} color={C.amber} o={sp(f, 6, 24)}>20 – 40 triệu năm</Big>
    <Bar x={110} y={830} w={860} color={HOT} p={sp(f, 18, 44) * 0.01 + 0.012} />
    <Tag x={540} y={980} color={C.cream} size={42} o={sp(f, 36, 52)}>ngắn hơn thực tế rất nhiều</Tag>
    <HatHero x={540} y={1250} s={2} walk={f * 0.12} hat="scholar" />
  </g>
);
const P10: Panel = ({f}) => (
  <g>
    <Head a="Nhưng ông bỏ sót" b="nhiệt sinh ra từ lòng đất" />
    <circle cx={640} cy={880} r={230} fill="#4a3626" stroke={C.cream} strokeWidth={6} />
    <circle cx={640} cy={880} r={110 + 8 * Math.sin(f * 0.25)} fill={HOT} opacity={sp(f, 8, 24)} />
    <Tag x={640} y={1190} color={C.amber} size={44} o={sp(f, 26, 42)}>lòng đất tự sinh thêm nhiệt</Tag>
    <HatHero x={150} y={1250} s={2} walk={f * 0.1} hat="scholar" />
  </g>
);
const P11: Panel = ({f}) => (
  <g>
    <Head a="Nguyên tố phóng xạ tự" b="phân rã và tỏa nhiệt" />
    <Atom x={400} y={820} r={70} label="U" color={f % 60 < 36 ? YEL : GRY} o={sp(f, 4, 18)} />
    <Arrow x1={490} y1={820} x2={650} y2={820} p={sp(f, 14, 34)} color={C.amber} />
    <Atom x={740} y={820} r={70} label="Pb" color={GRY} o={sp(f, 26, 40)} />
    {[0, 1, 2].map((i) => (
      <path key={i} d={`M ${360 + i * 40} 960 q 14 -30 0 -60`} fill="none" stroke={HOT} strokeWidth={6} strokeLinecap="round" opacity={0.5 + 0.4 * Math.sin(f * 0.2 + i)} />
    ))}
    <Tag x={540} y={1100} color={C.cream} size={44} o={sp(f, 30, 46)}>Trái Đất nguội chậm hơn</Tag>
    <HatHero x={150} y={1250} s={2} walk={f * 0.1} hat="scholar" />
  </g>
);

// --- Cảnh 4: chu kỳ bán rã ---
const P12: Panel = ({f}) => (
  <g>
    <Head a="Chính nguyên tố ấy" b="là chiếc đồng hồ trong đá" />
    <Rock x={650} y={960} s={1.35} />
    <Clock x={650} y={950} r={120} spin={f * 0.03} />
    {[[560, 1050], [650, 1070], [740, 1040]].map(([x, y], i) => (
      <Atom key={i} x={x} y={y} r={22} o={sp(f, 8 + i * 6, 20 + i * 6)} />
    ))}
    <HatHero x={170} y={1250} s={2} walk={f * 0.12} hat="gear" />
  </g>
);
const P13: Panel = ({f}) => (
  <g>
    <Head a="U-ra-ni-um tự biến" b="thành chì, rất đều đặn" />
    <Atom x={300} y={850} r={90} label="U" o={sp(f, 4, 18)} />
    <Arrow x1={410} y1={850} x2={660} y2={850} p={sp(f, 14, 40)} color={C.amber} />
    <Atom x={780} y={850} r={90} label="Pb" color={GRY} o={sp(f, 30, 44)} />
    <Tag x={300} y={1010} color={C.cream} size={42} o={sp(f, 8, 22)}>u-ra-ni-um</Tag>
    <Tag x={780} y={1010} color={C.cream} size={42} o={sp(f, 34, 48)}>chì</Tag>
    <HatHero x={540} y={1250} s={2} walk={f * 0.12} hat="gear" />
  </g>
);
const P14: Panel = ({f}) => {
  const n = f < 36 ? 8 : f < 70 ? 4 : 2;
  return (
    <g>
      <Head a="Ví dụ: túi bánh" b="mỗi buổi ăn một nửa" />
      {Array.from({length: n}).map((_, i) => (
        <Cookie key={i} x={300 + (i % 4) * 150} y={780 + Math.floor(i / 4) * 150} />
      ))}
      <Tag x={540} y={1130} color={C.amber} size={46} o={sp(f, 6, 20)}>{n === 8 ? '8 cái' : n === 4 ? 'còn 4 cái' : 'còn 2 cái'}</Tag>
      <HatHero x={150} y={1250} s={2} walk={f * 0.12} cheer={sp(f, 30, 50)} hat="gear" />
    </g>
  );
};
const P15: Panel = ({f}) => (
  <g>
    <Head a="Sau một khoảng cố định" b="còn lại đúng một nửa" />
    <Bar x={110} y={640} w={860} color={YEL} p={1} label="lúc đầu" />
    <Bar x={110} y={780} w={860} color={YEL} p={1 - sp(f, 14, 36) * 0.5} label="sau 1 chu kỳ" />
    <Tag x={540} y={1000} color={C.amber} size={54} o={sp(f, 36, 52)}>gọi là chu kỳ bán rã</Tag>
    <HatHero x={540} y={1250} s={2} walk={f * 0.12} hat="gear" />
  </g>
);
const P16: Panel = ({f}) => (
  <g>
    <Head a="U-ra-ni-um 238:" b="chu kỳ bán rã 4,5 tỉ năm" />
    <Big x={540} y={760} size={150} color={C.amber} o={sp(f, 6, 24)}>4,5 tỉ năm</Big>
    <Atom x={300} y={1000} r={60} label="U" o={sp(f, 14, 28)} />
    <Arrow x1={380} y1={1000} x2={700} y2={1000} p={sp(f, 20, 48)} color={C.cream} />
    <Atom x={780} y={1000} r={60} label="½" color="#c8b36a" o={sp(f, 40, 54)} />
    <HatHero x={150} y={1250} s={2} walk={f * 0.12} hat="gear" />
  </g>
);

// --- Cảnh 5: phép tính ---
const P17: Panel = ({f}) => (
  <g>
    <Head a="Giả sử đá có" b="100 nguyên tử u-ra-ni-um" />
    <Grid x={290} y={540} gray={0} o={sp(f, 4, 20)} />
    <Big x={540} y={1180} size={110} color={C.amber} o={sp(f, 24, 40)}>100 nguyên tử</Big>
  </g>
);
const P18: Panel = ({f}) => (
  <g>
    <Head a="Sau 1 chu kỳ" b="còn lại một nửa" />
    <Grid x={290} y={500} gray={sp(f, 6, 40) * 50} cell={46} />
    <Calc f={f} y={1080} step={110} lines={[{t: '100 ÷ 2 = 50', at: 20, size: 100, color: C.amber}]} />
  </g>
);
const P19: Panel = ({f}) => (
  <g>
    <Head a="Sau 2 chu kỳ" b="lại còn một nửa" />
    <Grid x={290} y={500} gray={50 + sp(f, 6, 40) * 25} cell={46} />
    <Calc f={f} y={1080} step={110} lines={[{t: '50 ÷ 2 = 25', at: 20, size: 100, color: C.amber}]} />
  </g>
);
const P20: Panel = ({f}) => (
  <g>
    <Head a="Vậy tuổi của đá" b="tính thế nào?" />
    <Calc f={f} y={700} step={150} lines={[{t: 'tuổi của đá', at: 4, size: 84, color: C.cream}, {t: '= số chu kỳ', at: 18, size: 84, color: C.amber}, {t: '× một chu kỳ', at: 32, size: 84, color: C.amber}]} />
    <HatHero x={540} y={1250} s={2} walk={f * 0.12} hat="gear" />
  </g>
);
const P21: Panel = ({f}) => (
  <g>
    <Head a="U-ra-ni-um và chì" b="nhiều bằng nhau" />
    <Bar x={110} y={650} w={430} color={YEL} p={sp(f, 6, 24)} />
    <Bar x={540} y={650} w={430} color={GRY} p={sp(f, 14, 32)} />
    <Tag x={325} y={790} color={C.cream} size={40} o={sp(f, 14, 28)}>u-ra-ni-um</Tag>
    <Tag x={755} y={790} color={C.cream} size={40} o={sp(f, 22, 36)}>chì</Tag>
    <Tag x={540} y={930} color={C.cream} size={54} o={sp(f, 26, 42)}>50 – 50</Tag>
    <Big x={540} y={1100} size={100} color={C.amber} o={sp(f, 36, 52)}>đúng 1 chu kỳ</Big>
  </g>
);
const P22: Panel = ({f}) => (
  <g>
    <Head a="Tuổi của đá" />
    <Calc f={f} y={720} step={170} lines={[{t: '1 × 4,5', at: 6, size: 120}, {t: '= 4,5 tỉ năm', at: 28, size: 130, color: C.amber}]} />
    <HatHero x={540} y={1250} s={2} walk={f * 0.2} cheer={sp(f, 36, 54)} hat="gear" />
  </g>
);

// --- Cảnh 6: Patterson ---
const P23: Panel = ({f}) => (
  <g>
    <Head a="Đá mặt đất tan chảy" b="rồi trộn lại" />
    <Rock x={650} y={940} s={1.3} fill={`rgb(${Math.round(lerp(110, 224, sp(f, 8, 50)))}, ${Math.round(lerp(98, 97, sp(f, 8, 50)))}, ${Math.round(lerp(88, 59, sp(f, 8, 50)))})`} />
    <Clock x={650} y={930} r={90} spin={-f * 0.05} o={sp(f, 6, 20)} />
    <Tag x={650} y={1190} color={C.amber} size={44} o={sp(f, 30, 46)}>đồng hồ hay bị làm lại</Tag>
    <HatHero x={150} y={1250} s={2} walk={f * 0.1} hat="gear" />
  </g>
);
const P24: Panel = ({f}) => (
  <g>
    <Head a="Thiên thạch hình thành" b="cùng thời với Trái Đất" />
    <Earth x={330} y={900} r={150} o={sp(f, 4, 18)} />
    <Meteor x={780} y={900} s={1.5} o={sp(f, 10, 24)} />
    <Dash x1={330} y1={1130} x2={780} y2={1130} p={sp(f, 24, 48)} color={C.cream} />
    <Tag x={555} y={1190} color={C.amber} size={42} o={sp(f, 38, 54)}>cùng tuổi</Tag>
  </g>
);
const P25: Panel = ({f}) => (
  <g>
    <Head a="Năm 1956, Pát-tơ-sơn" b="đo chì trong thiên thạch" />
    <Meteor x={700} y={900} s={2} />
    <Tag x={700} y={1130} color={C.cream} size={42} o={sp(f, 8, 24)}>Canyon Diablo</Tag>
    <Atom x={620} y={860} r={34} label="Pb" color={GRY} o={sp(f, 18, 30)} />
    <Atom x={760} y={940} r={34} label="Pb" color={GRY} o={sp(f, 26, 38)} />
    <HatHero x={170} y={1250} s={2} walk={f * 0.12} hat="gear" />
  </g>
);
const P26: Panel = ({f}) => (
  <g>
    <Head a="Kết quả: 4,55 tỉ năm" b="sai số chưa tới 100 triệu" />
    <Big x={540} y={760} size={160} color={C.amber} o={sp(f, 6, 24)}>4,55 tỉ năm</Big>
    <Tag x={540} y={920} color={C.cream} size={54} o={sp(f, 24, 40)}>± 70 triệu năm</Tag>
    <HatHero x={540} y={1250} s={2} walk={f * 0.2} cheer={sp(f, 30, 50)} hat="gear" />
  </g>
);
const P27: Panel = ({f}) => (
  <g>
    <Head a="Bùn đáy biển cũng nằm" b="đúng trên đường ấy" />
    <line x1={170} y1={1150} x2={910} y2={620} stroke={C.cream} strokeWidth={5} strokeDasharray="12 10" opacity={sp(f, 30, 50)} />
    {[[260, 1090], [380, 1000], [500, 920], [640, 820], [780, 720]].map(([x, y], i) => (
      <circle key={i} cx={x} cy={y} r={20} fill={GRY} stroke={C.cream} strokeWidth={4} opacity={sp(f, 4 + i * 5, 14 + i * 5)} />
    ))}
    <Earth x={560} y={910} r={36} o={sp(f, 34, 48)} />
    <Tag x={560} y={1020} color={C.amber} size={40} o={sp(f, 40, 54)}>bùn đáy biển</Tag>
    <Tag x={300} y={1210} color={C.cream} size={40} o={sp(f, 20, 34)}>các thiên thạch</Tag>
  </g>
);

// --- Cảnh 7: kết ---
const P28: Panel = ({f}) => (
  <g>
    <Head a="Phép đo mới nhất" b="cho kết quả gần như vậy" />
    <Big x={540} y={780} size={170} color={C.amber} o={sp(f, 6, 24)}>4,54 tỉ năm</Big>
    <Earth x={540} y={1050} r={110} o={sp(f, 18, 34)} />
  </g>
);
const P29: Panel = ({f}) => (
  <g>
    <Head a="So với tính của Át-sơ" b="lớn hơn bao nhiêu lần?" />
    <Calc f={f} y={720} step={170} lines={[{t: '4,54 tỉ ÷ 6 000', at: 6, size: 100}, {t: '≈ 757 000 lần', at: 30, size: 120, color: C.amber}]} />
    <HatHero x={540} y={1250} s={2} walk={f * 0.15} hat="scholar" />
  </g>
);
const P30: Panel = ({f}) => (
  <g>
    <Head a="Tuổi Trái Đất đọc từ" b="đồng hồ nguyên tử trong đá" />
    <Rock x={380} y={950} s={0.85} />
    <Clock x={380} y={940} r={80} spin={f * 0.03} />
    <Meteor x={800} y={940} s={1.3} o={sp(f, 8, 22)} />
    <HatHero x={560} y={1250} s={2} walk={f * 0.25} cheer={sp(f, 20, 44)} hat="helmet" />
  </g>
);

export const PANELS: Panel[] = [P0, P1, P2, P3, P4, P5, P6, P7, P8, P9, P10, P11, P12, P13, P14, P15, P16, P17, P18, P19, P20, P21, P22, P23, P24, P25, P26, P27, P28, P29, P30];
