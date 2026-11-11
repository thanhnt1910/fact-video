import React from 'react';
import {Arrow, Bar, Big, C, Calc, Dash, Head, HatHero, Lab, Panel, Tag, clamp01, lerp, seg, sp} from '../khoahoc/kit';

const FIRE = '#ffb347';
const LIGHT = '#fff2b0';
const SOUND = '#8fd1ff';

const Cloud: React.FC<{x: number; y: number; s?: number}> = ({x, y, s = 1}) => (
  <g transform={`translate(${x} ${y}) scale(${s})`} fill="#56637a" stroke={C.cream} strokeWidth={5 / s}>
    <circle cx={-60} cy={10} r={50} />
    <circle cx={0} cy={-20} r={68} />
    <circle cx={64} cy={8} r={52} />
    <rect x={-110} y={10} width={224} height={50} rx={25} stroke="none" />
  </g>
);
const Bolt: React.FC<{x: number; y: number; s?: number; o?: number}> = ({x, y, s = 1, o = 1}) => (
  <path transform={`translate(${x} ${y}) scale(${s})`} d="M 10 0 L -30 80 L -2 84 L -40 170 L 36 62 L 6 58 Z" fill={LIGHT} stroke={C.cream} strokeWidth={4 / s} strokeLinejoin="round" opacity={clamp01(o)} />
);
const Watch: React.FC<{x: number; y: number; r?: number; p: number; o?: number}> = ({x, y, r = 120, p, o = 1}) => (
  <g opacity={clamp01(o)}>
    <rect x={x - 14} y={y - r - 34} width={28} height={26} rx={6} fill="#b08a50" stroke={C.cream} strokeWidth={4} />
    <circle cx={x} cy={y} r={r} fill="#f4e9d0" stroke={C.cream} strokeWidth={8} />
    <circle cx={x} cy={y} r={r - 12} fill="none" stroke="#7a6a50" strokeWidth={3} />
    {Array.from({length: 12}, (_, i) => <line key={i} x1={x + (r - 14) * Math.sin((i * Math.PI) / 6)} y1={y - (r - 14) * Math.cos((i * Math.PI) / 6)} x2={x + (r - 26) * Math.sin((i * Math.PI) / 6)} y2={y - (r - 26) * Math.cos((i * Math.PI) / 6)} stroke="#4a3a28" strokeWidth={4} />)}
    <line x1={x} y1={y} x2={x + (r - 30) * Math.sin(p * Math.PI * 2)} y2={y - (r - 30) * Math.cos(p * Math.PI * 2)} stroke="#c0392b" strokeWidth={6} strokeLinecap="round" />
    <circle cx={x} cy={y} r={8} fill="#c0392b" />
  </g>
);
const Cannon: React.FC<{x: number; y: number; s?: number; fire?: number}> = ({x, y, s = 1, fire = 0}) => (
  <g transform={`translate(${x} ${y}) scale(${s})`} stroke={C.cream} strokeWidth={5 / s}>
    <rect x={-10} y={-70} width={150} height={44} rx={14} fill="#3b3f4a" transform="rotate(-10 0 -48)" />
    <circle cx={30} cy={-8} r={34} fill="#8a6a3a" />
    <circle cx={30} cy={-8} r={8} fill="#4a3a28" />
    {fire > 0 && <circle cx={150} cy={-84} r={22 + 40 * fire} fill={FIRE} opacity={1 - fire * 0.6} stroke="none" />}
  </g>
);
const Waves: React.FC<{x: number; y: number; p: number; maxR?: number; o?: number}> = ({x, y, p, maxR = 700, o = 1}) => (
  <g fill="none" stroke={SOUND} strokeWidth={5}>
    {[0, 0.12, 0.24].map((d, i) => {
      const q = clamp01((p - d) / (1 - d));
      return <circle key={i} cx={x} cy={y} r={20 + q * maxR} opacity={o * 0.8 * (1 - q) * (q > 0 ? 1 : 0)} />;
    })}
  </g>
);

// --- Cảnh 1 ---
const P0: Panel = ({f}) => (
  <g>
    <Head a="Chớp và sấm cùng lúc" b="sao ta thấy chớp trước?" />
    <Cloud x={250} y={560} s={1.2} />
    <Bolt x={290} y={620} s={1.4} o={sp(f, 8, 12) * (1 - sp(f, 40, 70) * 0.6)} />
    <Waves x={290} y={760} p={seg(f, 14, 100)} maxR={820} />
    <HatHero x={800} y={1230} s={2} walk={f * 0.2} hat="pirate" />
    <Tag x={800} y={1010} color={C.amber} size={44} o={sp(f, 16, 28) * (1 - sp(f, 60, 70))}>thấy chớp!</Tag>
    <Tag x={800} y={1010} color={SOUND} size={44} o={sp(f, 84, 96)}>nghe sấm…</Tag>
  </g>
);
const P1: Panel = ({f}) => (
  <g>
    <Head a="Khoảng chờ ấy cho biết" b="giông cách mình bao xa" />
    <Watch x={540} y={850} r={170} p={seg(f, 8, 100)} />
    <Lab x={540} y={1160} size={120} color={C.amber} o={0.9 * sp(f, 30, 46)}>?</Lab>
  </g>
);
const P2: Panel = ({f}) => (
  <g>
    <Head a="Ánh sáng đến gần như tức thì" b="âm thanh đi chậm hơn nhiều" />
    <Lab x={110} y={700} size={40} anchor="start" color={C.cream}>ánh sáng</Lab>
    <Bar x={110} y={730} w={860} color={LIGHT} p={seg(f, 8, 16)} />
    <Lab x={110} y={910} size={40} anchor="start" color={C.cream}>âm thanh</Lab>
    <Bar x={110} y={940} w={860} color={SOUND} p={seg(f, 8, 110)} />
  </g>
);
const P3: Panel = ({f}) => (
  <g>
    <Head a="Muốn tính khoảng cách" b="phải biết âm thanh đi nhanh cỡ nào" />
    <Big x={540} y={820} size={190} color={C.amber} o={sp(f, 8, 24)}>?</Big>
    <Lab x={540} y={960} size={60} color={C.cream} o={sp(f, 20, 34)}>mét mỗi giây</Lab>
    <Waves x={540} y={1100} p={seg(f % 60, 0, 60)} maxR={260} />
  </g>
);

// --- Cảnh 2 ---
const P4: Panel = ({f}) => (
  <g>
    <Head a="Thế kỷ 17, Ga-xen-đi" b="thử với một khẩu đại bác" />
    <Cannon x={150} y={1150} s={1.5} />
    <HatHero x={880} y={1250} s={2} walk={f * 0.2} hat="scholar" />
    <Dash x1={190} y1={1260} x2={880} y2={1260} p={sp(f, 10, 50)} color={C.dim} />
    <Tag x={540} y={1210} color={C.cream} size={38} o={sp(f, 36, 50)}>đứng thật xa</Tag>
  </g>
);
const P5: Panel = ({f}) => {
  const fire = seg(f, 20, 40);
  return (
    <g>
      <Head a="Bấm giờ: từ lúc thấy lửa lóe" b="đến lúc nghe tiếng nổ" />
      <Cannon x={130} y={1130} s={1.4} fire={f > 20 ? fire : 0} />
      <Waves x={330} y={1010} p={seg(f, 24, 110)} maxR={760} />
      <HatHero x={900} y={1250} s={2} walk={f * 0.15} hat="scholar" />
      <Watch x={540} y={640} r={110} p={seg(f, 20, 100)} o={sp(f, 10, 22)} />
    </g>
  );
};
const P6: Panel = ({f}) => (
  <g>
    <Head a="Ánh sáng tới mắt ngay" b="chờ chính là âm thanh đang đi" />
    <rect x={110} y={760} width={30} height={70} rx={6} fill={LIGHT} stroke={C.cream} strokeWidth={4} opacity={sp(f, 6, 16)} />
    <rect x={140} y={760} width={lerp(0, 700, seg(f, 18, 70))} height={70} rx={6} fill={SOUND} stroke={C.cream} strokeWidth={4} />
    <Tag x={125} y={730} color={LIGHT} size={34} o={sp(f, 10, 22)}>ánh sáng</Tag>
    <Tag x={540} y={900} color={SOUND} size={44} o={sp(f, 50, 66)}>thời gian âm thanh đi</Tag>
  </g>
);
const P7: Panel = ({f}) => {
  const sw = Math.sin(f * 0.22);
  const hit = Math.max(0, Math.sin(f * 0.22 - 0.4));
  return (
    <g>
      <Head a="Như người bổ củi" b="bên kia sông" />
      <path d={`M 0 900 ${Array.from({length: 12}, (_, j) => `L ${j * 100} ${900 + Math.sin(j * 1.1 + f * 0.06) * 12}`).join(' ')} L 1080 1010 L 0 1010 Z`} fill="#2f6f8f" opacity={0.7} />
      <HatHero x={900} y={880} s={2} walk={f * 0.1} hat="gear" />
      <line x1={880} y1={820} x2={820 - 40 * sw} y2={760 + 40 * Math.abs(sw)} stroke={C.amber} strokeWidth={8} strokeLinecap="round" />
      <HatHero x={200} y={1230} s={2} walk={f * 0.12} hat="gear" />
      <Waves x={880} y={800} p={seg(f % 55, 0, 55)} maxR={520} o={hit > 0.8 ? 1 : 0.8} />
      <Tag x={640} y={1100} color={C.amber} size={38} o={sp(f, 24, 40)}>rìu bổ trước, tiếng “cốp” sau</Tag>
    </g>
  );
};

// --- Cảnh 3 ---
const P8: Panel = ({f}) => (
  <g>
    <Head a="Công thức rất gọn" />
    <Big x={540} y={720} size={100} color={C.cream} o={sp(f, 6, 20)}>tốc độ =</Big>
    <Big x={540} y={860} size={100} color={C.amber} o={sp(f, 20, 34)}>quãng đường ÷ thời gian</Big>
    <HatHero x={200} y={1250} s={2} walk={f * 0.25} hat="scholar" cheer={sp(f, 40, 60)} />
  </g>
);
const P9: Panel = ({f}) => (
  <g>
    <Head a="Giả sử khẩu súng cách 3 km" b="ông đếm được 9 giây" />
    <Cannon x={130} y={1090} s={1.3} />
    <HatHero x={900} y={1210} s={2} walk={f * 0.15} hat="scholar" />
    <Arrow x1={170} y1={1270} x2={880} y2={1270} p={sp(f, 8, 40)} w={6} />
    <Big x={540} y={1200} size={90} color={C.amber} o={sp(f, 30, 44)}>3 km</Big>
    <Watch x={540} y={650} r={110} p={seg(f, 20, 100)} o={sp(f, 14, 26)} />
    <Big x={540} y={860} size={80} color={C.cream} o={sp(f, 50, 64)}>9 giây</Big>
  </g>
);
const P10: Panel = ({f}) => (
  <g>
    <Head a="Quãng đường chia thời gian" />
    <Calc f={f} y={720} lines={[{t: '3 000 ÷ 9', at: 6}, {t: '= khoảng 333', at: 26, color: C.amber}, {t: 'mét mỗi giây', at: 44, size: 60, color: C.cream}]} />
  </g>
);

// --- Cảnh 4 ---
const P11: Panel = ({f}) => (
  <g>
    <Head a="Số đo của Ga-xen-đi" b="còn cao hơn thực tế" />
    <Lab x={110} y={700} size={38} anchor="start" color={C.cream}>số của Ga-xen-đi</Lab>
    <Bar x={110} y={730} w={860} color="#f2b35a" p={sp(f, 6, 30)} />
    <Lab x={110} y={900} size={38} anchor="start" color={C.cream}>số thật</Lab>
    <Bar x={110} y={930} w={860} color={SOUND} p={sp(f, 20, 44) * 0.74} />
    <Tag x={540} y={1120} color={C.amber} size={42} o={sp(f, 40, 56)}>cách bấm giờ thời ấy còn thô</Tag>
  </g>
);
const P12: Panel = ({f}) => (
  <g>
    <Head a="Viện Hàn lâm Khoa học Pháp" b="đo lại thật cẩn thận" />
    <path d="M 240 820 L 540 640 L 840 820 Z" fill="#c9b98c" stroke={C.cream} strokeWidth={6} opacity={sp(f, 6, 20)} />
    {[300, 420, 540, 660, 780].map((x) => <rect key={x} x={x - 22} y={830} width={44} height={230} fill="#e4d7ae" stroke={C.cream} strokeWidth={4} opacity={sp(f, 10, 28)} />)}
    <rect x={220} y={1060} width={640} height={36} rx={6} fill="#c9b98c" stroke={C.cream} strokeWidth={5} opacity={sp(f, 10, 28)} />
    <Big x={540} y={1210} size={120} color={C.amber} o={sp(f, 30, 46)}>1738</Big>
  </g>
);
const P13: Panel = ({f}) => (
  <g>
    <Head a="Kết quả: 332 mét mỗi giây" b="rất gần số đo ngày nay" />
    <Big x={540} y={860} size={220} color={C.amber} o={sp(f, 8, 26)}>332</Big>
    <Lab x={540} y={980} size={56} color={C.cream} o={sp(f, 22, 38)}>mét mỗi giây</Lab>
    <Waves x={540} y={1150} p={seg(f % 70, 0, 70)} maxR={300} />
  </g>
);
const Thermo: React.FC<{x: number; y: number; level: number; color: string}> = ({x, y, level, color}) => (
  <g stroke={C.cream} strokeWidth={6}>
    <rect x={x - 30} y={y - 260} width={60} height={260} rx={30} fill="#1d2634" />
    <circle cx={x} cy={y + 10} r={56} fill={color} />
    <rect x={x - 16} y={y - 250 + 250 * (1 - level)} width={32} height={250 * level} rx={16} fill={color} stroke="none" />
  </g>
);
const P14: Panel = ({f}) => (
  <g>
    <Head a="Ngày nay, ở 20 °C" b="âm thanh đi khoảng 343 mét mỗi giây" />
    <Thermo x={300} y={1100} level={0.62 * sp(f, 6, 30)} color="#e0613b" />
    <Big x={700} y={850} size={120} color={C.amber} o={sp(f, 16, 32)}>20 °C</Big>
    <Big x={700} y={1020} size={150} color={SOUND} o={sp(f, 26, 42)}>343</Big>
    <Lab x={700} y={1100} size={44} color={C.cream} o={sp(f, 30, 44)}>mét mỗi giây</Lab>
  </g>
);
const P15: Panel = ({f}) => (
  <g>
    <Head a="Ở 0 °C, âm thanh chậm lại" b="chỉ còn 331 mét mỗi giây" />
    <Thermo x={300} y={1100} level={0.2 + 0.4 * (1 - sp(f, 6, 30))} color="#5fb0e0" />
    <Big x={700} y={850} size={120} color="#9fd8ff" o={sp(f, 16, 32)}>0 °C</Big>
    <Big x={700} y={1020} size={150} color={SOUND} o={sp(f, 26, 42)}>331</Big>
    <Lab x={700} y={1100} size={44} color={C.cream} o={sp(f, 30, 44)}>mét mỗi giây</Lab>
  </g>
);

// --- Cảnh 5 ---
const P16: Panel = ({f}) => (
  <g>
    <Head a="Quay lại cơn giông" b="trong 3 giây âm thanh đi bao xa?" />
    <Watch x={540} y={820} r={170} p={seg(f, 8, 90) * 0.25} />
    <Big x={540} y={1130} size={110} color={C.amber} o={sp(f, 20, 36)}>3 giây</Big>
  </g>
);
const P17: Panel = ({f}) => (
  <g>
    <Head a="Âm thanh đi trong 3 giây" />
    <Calc f={f} y={720} lines={[{t: '343 × 3', at: 6}, {t: '= gần 1 000 mét', at: 26, color: C.amber}]} />
  </g>
);
const P18: Panel = ({f}) => (
  <g>
    <Head a="Gần bằng 1 ki-lô-mét" b="cứ 3 giây chờ ≈ 1 km" />
    {[['3 giây', '1 km'], ['6 giây', '2 km'], ['9 giây', '3 km']].map(([a, b], i) => (
      <g key={a} opacity={sp(f, 8 + i * 22, 22 + i * 22)}>
        <rect x={190} y={620 + i * 170} width={700} height={120} rx={24} fill="#1f2a3d" stroke={C.cream} strokeWidth={5} />
        <Lab x={330} y={698 + i * 170} size={56} color={C.cream}>{a}</Lab>
        <Lab x={540} y={698 + i * 170} size={56} color={C.dim}>→</Lab>
        <Lab x={730} y={698 + i * 170} size={56} color={C.amber}>{b}</Lab>
      </g>
    ))}
  </g>
);
const P19: Panel = ({f}) => (
  <g>
    <Head a="Ví dụ: thấy chớp rồi đếm" b="đến 9 mới nghe sấm" />
    <Cloud x={230} y={640} s={1} />
    <Bolt x={260} y={690} s={1.1} o={sp(f, 6, 10) * (1 - sp(f, 14, 40))} />
    {Array.from({length: 9}, (_, i) => <Big key={i} x={120 + i * 100} y={1000} size={86} color={i === 8 ? C.amber : C.cream} o={sp(f, 20 + i * 8, 28 + i * 8)}>{String(i + 1)}</Big>)}
    <HatHero x={900} y={1230} s={2} walk={f * 0.2} hat="pirate" cheer={sp(f, 100, 120)} />
  </g>
);
const P20: Panel = ({f}) => (
  <g>
    <Head a="Chia 9 giây cho 3" />
    <Calc f={f} y={720} lines={[{t: '9 ÷ 3', at: 6}, {t: '= 3 km', at: 24, color: C.amber}]} />
    <Tag x={540} y={1060} color={C.cream} size={44} o={sp(f, 40, 56)}>cơn giông cách bạn chừng đó</Tag>
  </g>
);

// --- Cảnh 6 ---
const P21: Panel = ({f}) => (
  <g>
    <Head a="Chớp và sấm cùng xảy ra" b="nhưng âm thanh đi chậm hơn" />
    <Cloud x={250} y={600} s={1.1} />
    <Bolt x={290} y={650} s={1.2} o={sp(f, 6, 10)} />
    <Arrow x1={290} y1={900} x2={900} y2={900} p={seg(f, 8, 18)} color={LIGHT} />
    <Arrow x1={290} y1={1010} x2={900} y2={1010} p={seg(f, 8, 100)} color={SOUND} />
    <Tag x={600} y={860} color={LIGHT} size={34} o={sp(f, 10, 20)}>ánh sáng</Tag>
    <Tag x={600} y={1070} color={SOUND} size={34} o={sp(f, 20, 30)}>âm thanh</Tag>
  </g>
);
const P22: Panel = ({f}) => {
  const k = seg(f, 6, 100);
  return (
    <g>
      <Head a="Khoảng chờ ấy cho biết" b="giông còn xa hay đã gần" />
      <line x1={80} y1={1100} x2={1000} y2={1100} stroke={C.dim} strokeWidth={4} opacity={0.5} />
      <Cloud x={lerp(900, 330, k)} y={760} s={lerp(0.6, 1.4, k)} />
      <HatHero x={150} y={1230} s={2} walk={f * 0.15} hat="pirate" cheer={sp(f, 50, 70)} />
      <Tag x={900} y={1190} color={C.cream} size={36} o={1 - k}>xa</Tag>
      <Tag x={420} y={1190} color={C.amber} size={36} o={k}>gần</Tag>
    </g>
  );
};

export const PANELS: Panel[] = [P0, P1, P2, P3, P4, P5, P6, P7, P8, P9, P10, P11, P12, P13, P14, P15, P16, P17, P18, P19, P20, P21, P22];
