import React from 'react';
import {Arrow, Bar, Big, C, Calc, Dash, Head, HatHero, Lab, Panel, Tag, clamp01, lerp, seg, sp} from '../khoahoc/kit';

const SUN = '#f6c453';
const MOON = '#e9dcc0';
const EARTH = '#4f95d8';

const Sun: React.FC<{x: number; y: number; r?: number; o?: number}> = ({x, y, r = 80, o = 1}) => (
  <g opacity={clamp01(o)}>
    <circle cx={x} cy={y} r={r * 1.5} fill={SUN} opacity={0.2} />
    <circle cx={x} cy={y} r={r} fill={SUN} stroke={C.cream} strokeWidth={5} />
  </g>
);
const Moon: React.FC<{x: number; y: number; r?: number; half?: boolean; o?: number}> = ({x, y, r = 60, half = false, o = 1}) => (
  <g opacity={clamp01(o)}>
    <circle cx={x} cy={y} r={r} fill={half ? '#3a3a52' : MOON} stroke={C.cream} strokeWidth={5} />
    {half && <path d={`M ${x} ${y - r} A ${r} ${r} 0 0 0 ${x} ${y + r} Z`} fill={MOON} />}
  </g>
);
const Earth: React.FC<{x: number; y: number; r?: number; o?: number}> = ({x, y, r = 50, o = 1}) => (
  <g opacity={clamp01(o)}>
    <circle cx={x} cy={y} r={r} fill={EARTH} stroke={C.cream} strokeWidth={5} />
    <ellipse cx={x - r * 0.25} cy={y - r * 0.2} rx={r * 0.35} ry={r * 0.25} fill="#5fa86a" />
  </g>
);
const RightMark: React.FC<{x: number; y: number; s?: number; dx?: number; dy?: number; o?: number}> = ({x, y, s = 40, dx = 1, dy = 1, o = 1}) => (
  <path d={`M ${x + dx * s} ${y} L ${x + dx * s} ${y + dy * s} L ${x} ${y + dy * s}`} fill="none" stroke={C.amber} strokeWidth={6} opacity={clamp01(o)} />
);
// Tam giác: Trái Đất E, Mặt Trăng M (góc vuông), Mặt Trời S
const E = {x: 230, y: 1130};
const M = {x: 230, y: 700};
const S = {x: 930, y: 700};
const Tri: React.FC<{p?: number; right?: number; angle?: number; f?: number}> = ({p = 1, right = 0, angle = 0}) => (
  <g>
    <line x1={E.x} y1={E.y} x2={M.x} y2={lerp(E.y, M.y, clamp01(p))} stroke={C.cream} strokeWidth={5} />
    <line x1={M.x} y1={M.y} x2={lerp(M.x, S.x, clamp01(p))} y2={M.y} stroke={C.cream} strokeWidth={5} />
    <line x1={E.x} y1={E.y} x2={lerp(E.x, S.x, clamp01(p))} y2={lerp(E.y, S.y, clamp01(p))} stroke={C.amber} strokeWidth={5} strokeDasharray="12 10" opacity={clamp01(p)} />
    <Earth x={E.x} y={E.y} r={46} />
    <Moon x={M.x} y={M.y} r={36} half />
    <Sun x={S.x} y={S.y} r={46} />
    <RightMark x={M.x} y={M.y} dx={1} dy={1} s={36} o={right} />
    {angle > 0 && <path d={`M ${E.x} ${E.y - 120} A 120 120 0 0 1 ${E.x + 120 * Math.sin(Math.atan2(S.x - E.x, E.y - S.y))} ${E.y - 120 * Math.cos(Math.atan2(S.x - E.x, E.y - S.y))}`} fill="none" stroke={C.amber} strokeWidth={8} opacity={angle} />}
  </g>
);

// --- Cảnh 1 ---
const P0: Panel = ({f}) => (
  <g>
    <Head a="Mặt Trời xa hơn Mặt Trăng" b="bao nhiêu lần?" />
    <Sun x={190} y={800} r={100} o={sp(f, 4, 16)} />
    <Moon x={880} y={800} r={46} o={sp(f, 10, 22)} />
    <Dash x1={320} y1={800} x2={820} y2={800} p={sp(f, 20, 50)} />
    <Big x={570} y={760} size={130} color={C.amber} o={0.9 * sp(f, 36, 52)}>?</Big>
    <Tag x={540} y={1000} color={C.cream} size={42} o={sp(f, 44, 58)}>chưa có cây thước nào dài tới thế</Tag>
    <HatHero x={200} y={1250} s={2} walk={f * 0.25} hat="scholar" />
  </g>
);
const P1: Panel = ({f}) => (
  <g>
    <Head a="Hơn 2 000 năm trước" b="A-ri-xta-khơ ngắm Mặt Trăng" />
    <Moon x={740} y={800} r={130} half o={sp(f, 6, 22)} />
    <HatHero x={260} y={1120} s={2} walk={f * 0.2} hat="scholar" />
    <Tag x={740} y={1010} color={C.amber} size={42} o={sp(f, 30, 44)}>lúc sáng đúng một nửa</Tag>
  </g>
);
const P2: Panel = ({f}) => (
  <g>
    <Head a="Khoảnh khắc ấy giấu" b="một hình tam giác" />
    <Tri p={seg(f, 8, 50)} />
    <Lab x={540} y={1260} size={48} color={C.amber} o={sp(f, 50, 64)}>(hình minh họa, không đúng tỉ lệ)</Lab>
  </g>
);
const P3: Panel = ({f}) => (
  <g>
    <Head a="Vì sao Mặt Trăng" b="sáng một nửa là manh mối?" />
    <Moon x={540} y={850} r={190} half o={sp(f, 4, 20)} />
    <Big x={540} y={1180} size={100} color={C.amber} o={0.9 * sp(f, 30, 46)}>?</Big>
  </g>
);

// --- Cảnh 2 ---
const P4: Panel = ({f}) => (
  <g>
    <Head a="Mặt Trăng tự nó không sáng" b="nửa hướng về Mặt Trời mới sáng" />
    <Sun x={150} y={860} r={90} />
    {[-70, 0, 70].map((d) => <Arrow key={d} x1={270} y1={860 + d} x2={lerp(270, 520, seg(f, 8, 36))} y2={860 + d * 0.5} p={sp(f, 8, 30)} color={SUN} w={5} />)}
    <Moon x={730} y={860} r={150} half o={sp(f, 4, 20)} />
  </g>
);
const P5: Panel = ({f}) => (
  <g>
    <Head a="Giống quả bóng trong phòng tối" b="đèn pin chỉ rọi sáng một nửa" />
    <rect x={110} y={820} width={160} height={70} rx={14} fill="#8a6a3a" stroke={C.cream} strokeWidth={5} />
    <path d={`M 270 835 L 520 740 L 520 970 L 270 875 Z`} fill="#fff2b0" opacity={0.3 * sp(f, 8, 24)} />
    <Moon x={650} y={855} r={140} half o={sp(f, 4, 20)} />
  </g>
);
const P6: Panel = ({f}) => (
  <g>
    <Head a="Thấy đúng nửa quả sáng" b="mắt nhìn vuông góc với tia đèn" />
    <Arrow x1={120} y1={800} x2={lerp(120, 480, seg(f, 6, 30))} y2={800} p={sp(f, 6, 22)} color={SUN} />
    <Moon x={650} y={800} r={140} half />
    <Arrow x1={650} y1={1200} x2={650} y2={lerp(1200, 980, seg(f, 24, 50))} p={sp(f, 24, 40)} color={C.cream} />
    <RightMark x={650} y={940} dx={-1} dy={1} s={34} o={sp(f, 46, 60)} />
    <HatHero x={760} y={1250} s={1.2} walk={0} hat="scholar" />
  </g>
);
const P7: Panel = ({f}) => (
  <g>
    <Head a="Mặt Trăng cũng vậy: Trái Đất," b="Mặt Trăng, Mặt Trời tạo tam giác" />
    <Tri p={seg(f, 6, 40)} />
    <Tag x={E.x + 120} y={E.y + 80} color={C.cream} size={34} o={sp(f, 30, 44)}>Trái Đất</Tag>
    <Tag x={M.x + 20} y={M.y - 60} color={C.cream} size={34} o={sp(f, 36, 50)}>Mặt Trăng</Tag>
    <Tag x={S.x - 20} y={S.y - 80} color={C.cream} size={34} o={sp(f, 42, 56)}>Mặt Trời</Tag>
  </g>
);
const P8: Panel = ({f}) => (
  <g>
    <Head a="Góc vuông của tam giác" b="nằm đúng ở Mặt Trăng" />
    <Tri right={sp(f, 10, 26)} />
    <Big x={420} y={860} size={90} color={C.amber} o={sp(f, 24, 40)}>90°</Big>
  </g>
);
const P9: Panel = ({f}) => (
  <g>
    <Head a="Chỉ còn phải biết" b="góc ở Trái Đất" />
    <Tri right={1} angle={sp(f, 10, 28)} />
    <Big x={420} y={1000} size={120} color={C.amber} o={0.9 * sp(f, 24, 40)}>?</Big>
  </g>
);

// --- Cảnh 3 ---
const P10: Panel = ({f}) => (
  <g>
    <Head a="A-ri-xta-khơ cho rằng" b="góc ấy là 87°" />
    <Tri right={1} angle={1} />
    <Big x={440} y={1000} size={130} color={C.amber} o={sp(f, 12, 28)}>87°</Big>
    <Tag x={540} y={1230} color={C.cream} size={40} o={sp(f, 30, 44)}>chỉ kém góc vuông một chút</Tag>
  </g>
);
const P11: Panel = ({f}) => (
  <g>
    <Head a="Từ góc ấy" b="có công thức" />
    <Lab x={540} y={650} size={52} color={C.cream} o={sp(f, 6, 20)}>số lần xa</Lab>
    <Big x={540} y={820} size={120} color={C.amber} o={sp(f, 18, 34)}>= 1 ÷ cos(góc)</Big>
    <HatHero x={200} y={1250} s={2} walk={f * 0.25} hat="scholar" cheer={sp(f, 40, 60)} />
  </g>
);
const P12: Panel = ({f}) => (
  <g>
    <Head a="Cô-sin là con số máy tính bấm ra" b="góc gần 90° thì số càng nhỏ" />
    {[['cos 60°', '0,5'], ['cos 80°', '0,17'], ['cos 87°', '0,052']].map(([a, b], i) => (
      <g key={a} opacity={sp(f, 8 + i * 22, 22 + i * 22)}>
        <rect x={190} y={620 + i * 170} width={700} height={120} rx={24} fill="#2c2552" stroke={C.cream} strokeWidth={5} />
        <Big x={380} y={705 + i * 170} size={66} color={C.cream}>{a}</Big>
        <Big x={540} y={705 + i * 170} size={66} color={C.dim}>≈</Big>
        <Big x={730} y={705 + i * 170} size={72} color={C.amber}>{b}</Big>
      </g>
    ))}
  </g>
);
const P13: Panel = ({f}) => (
  <g>
    <Head a="Với 87°" b="máy tính cho cô-sin" />
    <Calc f={f} y={760} lines={[{t: 'cos 87°', at: 6}, {t: '≈ 0,052', at: 26, color: C.amber}]} />
  </g>
);
const P14: Panel = ({f}) => (
  <g>
    <Head a="Rồi một chia cho số ấy" />
    <Calc f={f} y={720} lines={[{t: '1 ÷ 0,052', at: 6}, {t: '≈ 19', at: 26, color: C.amber, size: 130}]} />
  </g>
);
const P15: Panel = ({f}) => (
  <g>
    <Head a="Theo A-ri-xta-khơ" b="Mặt Trời xa gấp khoảng 19 lần" />
    <Earth x={150} y={820} r={40} />
    <Moon x={150 + 880 / 19} y={820} r={22} half />
    <Sun x={940} y={820} r={46} o={sp(f, 20, 36)} />
    <Dash x1={190} y1={900} x2={940} y2={900} p={sp(f, 10, 50)} />
    <Big x={540} y={1010} size={100} color={C.amber} o={sp(f, 40, 56)}>≈ 19 lần</Big>
  </g>
);

// --- Cảnh 4 ---
const P16: Panel = ({f}) => (
  <g>
    <Head a="Nhưng con số thật" b="lớn hơn thế rất nhiều" />
    <Lab x={110} y={700} size={38} anchor="start" color={C.cream}>ông tính</Lab>
    <Bar x={110} y={730} w={860} color="#f2b35a" p={sp(f, 6, 30) * 0.05} />
    <Lab x={110} y={900} size={38} anchor="start" color={C.cream}>thật</Lab>
    <Bar x={110} y={930} w={860} color="#8fd1ff" p={sp(f, 24, 64)} />
    <Big x={540} y={1130} size={110} color={C.amber} o={0.9 * sp(f, 56, 72)}>?</Big>
  </g>
);
const P17: Panel = ({f}) => (
  <g>
    <Head a="Vì góc thật gần như vuông" b="chỉ hơn góc ông tính chừng 3°" />
    {[87, 90].map((a, i) => {
      const r = 520;
      const rad = ((90 - a) * Math.PI) / 180;
      return (
        <g key={a} opacity={sp(f, 6 + i * 18, 22 + i * 18)}>
          <line x1={200} y1={1150} x2={200 + r * Math.cos(rad)} y2={1150 - r * Math.sin(rad)} stroke={i ? C.amber : C.cream} strokeWidth={6} />
        </g>
      );
    })}
    <line x1={200} y1={1150} x2={200} y2={1150} />
    <Big x={780} y={760} size={90} color={C.cream} o={sp(f, 10, 24)}>87°</Big>
    <Big x={780} y={900} size={90} color={C.amber} o={sp(f, 26, 40)}>gần 90°</Big>
  </g>
);
const P18: Panel = ({f}) => (
  <g>
    <Head a="Ví dụ: ngắm cột đèn xa 100 m" b="lệch 3° là trượt hơn 5 m" />
    <HatHero x={150} y={1230} s={2} walk={0} hat="scholar" />
    <line x1={880} y1={1230} x2={880} y2={640} stroke="#b08a50" strokeWidth={14} strokeLinecap="round" />
    <circle cx={880} cy={630} r={28} fill="#fff2b0" stroke={C.cream} strokeWidth={5} />
    <line x1={200} y1={1100} x2={lerp(200, 880, seg(f, 8, 40))} y2={lerp(1100, 640, seg(f, 8, 40))} stroke={C.cream} strokeWidth={5} strokeDasharray="12 10" />
    <line x1={200} y1={1100} x2={lerp(200, 880, seg(f, 26, 58))} y2={lerp(1100, 750, seg(f, 26, 58))} stroke={C.amber} strokeWidth={5} opacity={sp(f, 26, 36)} />
    <Tag x={540} y={1210} color={C.cream} size={42} o={sp(f, 10, 24)}>100 m</Tag>
    <Tag x={760} y={880} color={C.amber} size={44} o={sp(f, 56, 70)}>trượt hơn 5 m</Tag>
  </g>
);
const P19: Panel = ({f}) => {
  const pts = Array.from({length: 31}, (_, i) => {
    const a = 60 + i;
    const v = Math.min(1 / Math.cos((Math.min(a, 89.4) * Math.PI) / 180), 42);
    return `${140 + (i / 30) * 800},${1150 - v * 11}`;
  });
  const k = seg(f, 8, 70);
  return (
    <g>
      <Head a="Gần góc vuông cô-sin rất nhỏ" b="nên kết quả vọt lên rất xa" />
      <line x1={140} y1={1150} x2={960} y2={1150} stroke={C.dim} strokeWidth={4} />
      <polyline points={pts.slice(0, Math.max(2, Math.round(2 + k * 29))).join(' ')} fill="none" stroke={C.amber} strokeWidth={8} strokeLinecap="round" strokeLinejoin="round" />
      <Tag x={200} y={1215} color={C.cream} size={32}>60°</Tag>
      <Tag x={900} y={1215} color={C.cream} size={32}>90°</Tag>
      <Arrow x1={930} y1={900} x2={930} y2={700} p={sp(f, 60, 80)} />
    </g>
  );
};

// --- Cảnh 5 ---
const P20: Panel = ({f}) => (
  <g>
    <Head a="Với góc thật" b="cùng phép chia ấy cho ra" />
    <Calc f={f} y={700} lines={[{t: '1 ÷ cos(89,85°)', at: 6, size: 84}, {t: '≈ 390 lần', at: 28, color: C.amber, size: 130}]} />
  </g>
);
const P21: Panel = ({f}) => (
  <g>
    <Head a="Góc thật chỉ kém 90°" b="chưa tới 1/6 độ" />
    <line x1={160} y1={1100} x2={900} y2={1100} stroke={C.cream} strokeWidth={5} />
    <line x1={160} y1={1100} x2={900} y2={1094} stroke={C.amber} strokeWidth={5} />
    <circle cx={700} cy={1097} r={150} fill="none" stroke={C.cream} strokeWidth={6} opacity={sp(f, 10, 26)} />
    <Tag x={700} y={880} color={C.amber} size={44} o={sp(f, 24, 40)}>khe hở nhỏ xíu</Tag>
    <Tag x={540} y={1290} color={C.cream} size={42} o={sp(f, 40, 56)}>thời ấy không ai đo nổi</Tag>
  </g>
);
const P22: Panel = ({f}) => (
  <g>
    <Head a="Cách làm hoàn toàn đúng" b="chỉ con số góc là lệch" />
    <g opacity={sp(f, 8, 24)}>
      <rect x={160} y={640} width={760} height={150} rx={26} fill="#2c2552" stroke={C.cream} strokeWidth={5} />
      <Lab x={400} y={735} size={56} color={C.cream}>cách làm</Lab>
      <path d="M 700 720 L 740 765 L 830 665" fill="none" stroke="#6fd18f" strokeWidth={14} strokeLinecap="round" strokeLinejoin="round" />
    </g>
    <g opacity={sp(f, 30, 46)}>
      <rect x={160} y={840} width={760} height={150} rx={26} fill="#2c2552" stroke={C.cream} strokeWidth={5} />
      <Lab x={400} y={935} size={56} color={C.cream}>con số góc</Lab>
      <path d="M 710 880 L 810 960 M 810 880 L 710 960" fill="none" stroke="#e0613b" strokeWidth={14} strokeLinecap="round" />
    </g>
  </g>
);

// --- Cảnh 6 ---
const P23: Panel = ({f}) => (
  <g>
    <Head a="Chỉ bằng đôi mắt và hình học" b="ông đã thấy Mặt Trời xa rất nhiều" />
    <HatHero x={220} y={1230} s={2} walk={f * 0.2} hat="scholar" />
    <Moon x={560} y={800} r={50} half />
    <Sun x={900} y={800} r={80} o={sp(f, 20, 36)} />
    <Arrow x1={320} y1={1050} x2={540} y2={860} p={sp(f, 8, 36)} color={C.cream} w={5} />
  </g>
);
const P24: Panel = ({f}) => (
  <g>
    <Head a="Nhìn Mặt Trăng lúc sáng một nửa" b="rồi đo góc: ra khoảng cách" />
    <Tri right={1} angle={1} />
    <HatHero x={540} y={1260} s={2} walk={f * 0.25} hat="scholar" cheer={sp(f, 20, 40)} />
  </g>
);

export const PANELS: Panel[] = [P0, P1, P2, P3, P4, P5, P6, P7, P8, P9, P10, P11, P12, P13, P14, P15, P16, P17, P18, P19, P20, P21, P22, P23, P24];
