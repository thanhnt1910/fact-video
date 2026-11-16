import React from 'react';
import {Arrow, Big, C, Calc, Head, HatHero, Panel, Tag, clamp01, lerp, sp} from '../khoahoc/kit';

const BLUE = '#6fb1e8';
const RED = '#e0613b';
const THREAD = '#e8c26a';
const CAN = '#5f86ab';

const ang = (i: number, n: number, off = 0) => ((-90 + ((i + off) * 360) / n) * Math.PI) / 180;
const ptsIn = (cx: number, cy: number, R: number, n: number) => Array.from({length: n}, (_, i) => [cx + R * Math.cos(ang(i, n)), cy + R * Math.sin(ang(i, n))]);
const ptsOut = (cx: number, cy: number, R: number, n: number) => {
  const r = R / Math.cos(Math.PI / n);
  return Array.from({length: n}, (_, i) => [cx + r * Math.cos(ang(i, n, 0.5)), cy + r * Math.sin(ang(i, n, 0.5))]);
};
const toStr = (p: number[][]) => p.map((q) => q.join(',')).join(' ');
const perim = (p: number[][]) => p.reduce((s, q, i) => s + Math.hypot(q[0] - p[(i + 1) % p.length][0], q[1] - p[(i + 1) % p.length][1]), 0);

const Poly: React.FC<{cx: number; cy: number; R: number; n: number; out?: boolean; color?: string; p?: number; w?: number; fill?: boolean}> = ({cx, cy, R, n, out = false, color = C.amber, p = 1, w = 7, fill = false}) => {
  const pts = out ? ptsOut(cx, cy, R, n) : ptsIn(cx, cy, R, n);
  const L = perim(pts);
  return <polygon points={toStr(pts)} fill={fill ? color : 'none'} fillOpacity={0.1} stroke={color} strokeWidth={w} strokeLinejoin="round" strokeDasharray={L} strokeDashoffset={L * (1 - clamp01(p))} />;
};
const Circle: React.FC<{cx: number; cy: number; R: number; o?: number; dash?: boolean}> = ({cx, cy, R, o = 1, dash = false}) => (
  <circle cx={cx} cy={cy} r={R} fill="none" stroke={C.cream} strokeWidth={6} strokeDasharray={dash ? '14 12' : undefined} opacity={clamp01(o)} />
);
const Dots: React.FC<{cx: number; cy: number; R: number; n: number; o?: number}> = ({cx, cy, R, n, o = 1}) => (
  <g opacity={clamp01(o)}>
    {ptsIn(cx, cy, R, n).map((q, i) => (
      <circle key={i} cx={q[0]} cy={q[1]} r={9} fill={C.cream} />
    ))}
  </g>
);
const fmt = (v: number, d: number) => v.toFixed(d).replace('.', ',');
// Thước số: đoạn [lo, hi] kẹp quanh pi trên thang [a, b].
const NL: React.FC<{y: number; a: number; b: number; lo: number; hi: number; p: number; d?: number; pi?: boolean; color?: string; label?: string; ticks?: number}> = ({y, a, b, lo, hi, p, d = 2, pi = true, color = C.amber, label, ticks = 6}) => {
  const X = (v: number) => 100 + (880 * (v - a)) / (b - a);
  const k = clamp01(p);
  const xl = X(lo);
  const xh = lerp(xl, X(hi), k);
  const PI = 3.14159265;
  return (
    <g>
      <line x1={100} y1={y} x2={980} y2={y} stroke={C.cream} strokeWidth={4} opacity={0.7} />
      {Array.from({length: ticks + 1}).map((_, i) => (
        <g key={i}>
          <line x1={100 + (880 * i) / ticks} y1={y - 14} x2={100 + (880 * i) / ticks} y2={y + 14} stroke={C.cream} strokeWidth={3} opacity={0.6} />
          <text x={100 + (880 * i) / ticks} y={y + 56} textAnchor="middle" fontFamily="BeVN" fontWeight={700} fontSize={32} fill={C.cream} opacity={0.75}>
            {fmt(a + ((b - a) * i) / ticks, d)}
          </text>
        </g>
      ))}
      <rect x={xl} y={y - 22} width={Math.max(2, xh - xl)} height={44} rx={8} fill={color} fillOpacity={0.55} stroke={color} strokeWidth={5} />
      {pi && (
        <g opacity={clamp01(k * 3)}>
          <line x1={X(PI)} y1={y - 70} x2={X(PI)} y2={y + 34} stroke={BLUE} strokeWidth={6} />
          <text x={X(PI)} y={y - 82} textAnchor="middle" fontFamily="BeVN" fontWeight={800} fontSize={56} fill={BLUE}>π</text>
        </g>
      )}
      {label && (
        <text x={540} y={y - 130} textAnchor="middle" fontFamily="BeVN" fontWeight={800} fontSize={46} fill={color} opacity={clamp01(k * 2)}>
          {label}
        </text>
      )}
    </g>
  );
};
const Digits: React.FC<{f: number; y: number; lines: string[]; size?: number; step?: number}> = ({f, y, lines, size = 70, step = 100}) => (
  <g>
    {lines.map((t, i) => (
      <Big key={i} x={540} y={y + i * step} size={size} color={i === 0 ? C.amber : C.cream} o={sp(f, 2 + i * 8, 14 + i * 8) * (i === 0 ? 1 : 0.85)}>
        {t}
      </Big>
    ))}
  </g>
);
const Hero2: React.FC<{f: number; x?: number; cheer?: number; s?: number}> = ({f, x = 170, cheer = 0, s = 2}) => <HatHero x={x} y={1250} s={s} walk={f * 0.13} cheer={cheer} hat="scholar" />;

const CX = 540;
const CY = 800;
const R = 280;

// --- Cảnh 1: câu hỏi ---
const P0: Panel = ({f}) => (
  <g>
    <Head a="Số pi dài vô tận" b="tính bằng cách nào?" />
    <Digits f={f} y={640} lines={['3,14159265358979', '32384626433832', '79502884197169']} size={74} />
    <Big x={780} y={1130} size={150} color={C.amber} o={0.9 * sp(f, 22, 38)}>?</Big>
    <Hero2 f={f} />
  </g>
);
const P1: Panel = ({f}) => (
  <g>
    <Head a="Họ không cần" b="viết hết nó" />
    <Big x={540} y={760} size={96} color={C.cream} o={sp(f, 2, 14)}>3,14159265…</Big>
    <line x1={150} y1={730} x2={930} y2={730} stroke={RED} strokeWidth={10} strokeLinecap="round" strokeDasharray={800} strokeDashoffset={800 * (1 - sp(f, 12, 26))} />
    <Tag x={540} y={950} color={RED} size={60} o={sp(f, 16, 30)}>✕ không cần viết hết</Tag>
    <Hero2 f={f} />
  </g>
);
const P2: Panel = ({f}) => (
  <g>
    <Head a="Chỉ cần kẹp nó" b="giữa hai số gần nhau" />
    <NL y={820} a={3.1} b={3.18} lo={3.12} hi={3.16} p={sp(f, 6, 30)} d={2} ticks={4} />
    <Hero2 f={f} />
  </g>
);
const P3: Panel = ({f}) => (
  <g>
    <Head a="Archimedes kẹp pi" b="bằng hình nhiều cạnh" />
    <Circle cx={CX} cy={CY} R={R} />
    <Poly cx={CX} cy={CY} R={R} n={96} color={C.amber} p={sp(f, 4, 26)} w={6} />
    <Poly cx={CX} cy={CY} R={R} n={96} out color={BLUE} p={sp(f, 14, 36)} w={6} />
    <Hero2 f={f} cheer={sp(f, 24, 40)} />
  </g>
);

// --- Cảnh 2: pi là gì ---
const P4: Panel = ({f}) => {
  const L = 2 * Math.PI * 220;
  return (
    <g>
      <Head a="Pi = chu vi" b="chia đường kính" />
      <circle cx={CX} cy={760} r={220} fill="none" stroke={C.amber} strokeWidth={10} strokeDasharray={L} strokeDashoffset={L * (1 - sp(f, 4, 30))} />
      <line x1={CX - 220} y1={760} x2={CX + 220} y2={760} stroke={C.cream} strokeWidth={8} opacity={sp(f, 24, 36)} />
      <Tag x={CX} y={730} color={C.cream} size={36} o={sp(f, 28, 40)}>đường kính</Tag>
      <Tag x={CX} y={1090} color={C.amber} size={46} o={sp(f, 14, 28)}>chu vi = đường bao</Tag>
      <Big x={CX} y={1190} size={74} color={C.cream} o={sp(f, 30, 44)}>chu vi ÷ đường kính</Big>
    </g>
  );
};
const P5: Panel = ({f}) => (
  <g>
    <Head a="Tròn lớn hay nhỏ" b="kết quả vẫn như nhau" />
    <circle cx={290} cy={800} r={120} fill="none" stroke={C.amber} strokeWidth={8} opacity={sp(f, 2, 14)} />
    <circle cx={730} cy={800} r={210} fill="none" stroke={C.amber} strokeWidth={8} opacity={sp(f, 8, 20)} />
    <Big x={290} y={1100} size={90} color={C.cream} o={sp(f, 18, 32)}>hơn 3</Big>
    <Big x={730} y={1100} size={90} color={C.cream} o={sp(f, 22, 36)}>hơn 3</Big>
    <Tag x={CX} y={1200} color={C.amber} size={46} o={sp(f, 28, 42)}>chu vi ÷ đường kính</Tag>
  </g>
);
const P6: Panel = ({f}) => {
  const n = Math.floor(sp(f, 4, 50) * 9);
  return (
    <g>
      <Head a="Quấn sợi chỉ quanh lon" b="rồi chia cho bề ngang" />
      <rect x={400} y={540} width={280} height={520} rx={26} fill={CAN} stroke={C.cream} strokeWidth={6} />
      {Array.from({length: n}).map((_, i) => (
        <ellipse key={i} cx={540} cy={600 + i * 48} rx={140} ry={20} fill="none" stroke={THREAD} strokeWidth={6} />
      ))}
      <Arrow x1={400} y1={1130} x2={680} y2={1130} color={C.cream} w={6} p={sp(f, 30, 44)} />
      <Tag x={540} y={1200} color={C.cream} size={40} o={sp(f, 34, 48)}>bề ngang của lon</Tag>
      <Hero2 f={f} x={190} />
    </g>
  );
};
const P7: Panel = ({f}) => (
  <g>
    <Head a="Được khoảng 3,1" b="nhưng chỉ giãn, lệch" />
    <path d={`M 100 780 Q 250 ${740 + 18 * Math.sin(f * 0.15)} 400 790 T 700 780 T 980 790`} fill="none" stroke={THREAD} strokeWidth={8} strokeLinecap="round" opacity={sp(f, 2, 14)} />
    {Array.from({length: 11}).map((_, i) => (
      <line key={i} x1={100 + i * 88} y1={900} x2={100 + i * 88} y2={i % 5 === 0 ? 950 : 930} stroke={C.cream} strokeWidth={4} opacity={0.8} />
    ))}
    <line x1={100} y1={900} x2={980} y2={900} stroke={C.cream} strokeWidth={4} opacity={0.8} />
    <Big x={CX} y={1090} size={110} color={C.amber} o={sp(f, 14, 28)}>≈ 3,1</Big>
    <Tag x={CX} y={1180} color={RED} size={46} o={sp(f, 24, 38)}>chữ số sau: không đáng tin</Tag>
    <Hero2 f={f} />
  </g>
);
const P8: Panel = ({f}) => (
  <g>
    <Head a="Đường cong khó đo" b="đường thẳng đo chính xác" />
    <path d="M 120 700 Q 260 540 420 700 T 720 700 T 960 640" fill="none" stroke={RED} strokeWidth={9} strokeLinecap="round" opacity={sp(f, 2, 16)} />
    <Tag x={CX} y={870} color={RED} size={46} o={sp(f, 10, 24)}>khó đo</Tag>
    <line x1={120} y1={1030} x2={960} y2={1030} stroke={C.amber} strokeWidth={10} strokeLinecap="round" opacity={sp(f, 16, 30)} />
    {Array.from({length: 22}).map((_, i) => (
      <line key={i} x1={120 + i * 40} y1={1030} x2={120 + i * 40} y2={1030 + (i % 5 === 0 ? 46 : 26)} stroke={C.cream} strokeWidth={4} opacity={sp(f, 18, 32)} />
    ))}
    <Tag x={CX} y={1160} color={C.amber} size={46} o={sp(f, 24, 38)}>đo rất chính xác</Tag>
  </g>
);
// --- Cảnh 3: kẹp vòng tròn ---
const P9: Panel = ({f}) => (
  <g>
    <Head a="Thay vòng tròn" b="bằng hình có cạnh thẳng" />
    <Circle cx={CX} cy={CY} R={R} o={1 - 0.55 * sp(f, 8, 24)} dash />
    <Poly cx={CX} cy={CY} R={R} n={6} color={C.amber} p={sp(f, 10, 34)} />
    <Hero2 f={f} />
  </g>
);
const P10: Panel = ({f}) => (
  <g>
    <Head a="Hình 6 cạnh" b="nằm trong vòng tròn" />
    <Circle cx={CX} cy={CY} R={R} />
    <Poly cx={CX} cy={CY} R={R} n={6} color={C.amber} p={sp(f, 2, 24)} />
    <Dots cx={CX} cy={CY} R={R} n={6} o={sp(f, 18, 30)} />
    <Tag x={CX} y={1190} color={C.amber} size={46} o={sp(f, 20, 34)}>đỉnh chạm vòng tròn</Tag>
  </g>
);
const P11: Panel = ({f}) => (
  <g>
    <Head a="Chu vi hình trong" b="ngắn hơn vòng tròn" />
    <Circle cx={CX} cy={CY - 60} R={230} o={0.8} />
    <Poly cx={CX} cy={CY - 60} R={230} n={6} color={C.amber} w={11} />
    <path d="M 240 1100 L 840 1100" stroke={C.amber} strokeWidth={9} strokeLinecap="round" opacity={sp(f, 8, 20)} />
    <path d="M 240 1100 Q 540 1000 840 1100" fill="none" stroke={C.cream} strokeWidth={7} opacity={sp(f, 14, 26)} />
    <Tag x={CX} y={1210} color={C.amber} size={44} o={sp(f, 22, 36)}>đường thẳng luôn ngắn hơn</Tag>
  </g>
);
const P12: Panel = ({f}) => (
  <g>
    <Head a="Hình 6 cạnh khác" b="nằm ngoài vòng tròn" />
    <Circle cx={CX} cy={CY} R={R - 20} />
    <Poly cx={CX} cy={CY} R={R - 20} n={6} out color={BLUE} p={sp(f, 2, 26)} />
    <Tag x={CX} y={1190} color={BLUE} size={46} o={sp(f, 20, 34)}>cạnh chạm vòng tròn</Tag>
  </g>
);
const P13: Panel = ({f}) => (
  <g>
    <Head a="Chu vi hình ngoài" b="dài hơn vòng tròn" />
    <Circle cx={CX} cy={CY - 40} R={R - 30} o={0.8} />
    <Poly cx={CX} cy={CY - 40} R={R - 30} n={6} out color={BLUE} w={11} />
    <Tag x={CX} y={1190} color={BLUE} size={46} o={sp(f, 10, 24)}>ôm bên ngoài nên dài hơn</Tag>
  </g>
);
const P14: Panel = ({f}) => (
  <g>
    <Head a="Vòng tròn bị kẹp" b="giữa hai chu vi" />
    <Circle cx={CX} cy={CY} R={R - 30} />
    <Poly cx={CX} cy={CY} R={R - 30} n={6} color={C.amber} w={8} />
    <Poly cx={CX} cy={CY} R={R - 30} n={6} out color={BLUE} w={8} />
    <Tag x={CX} y={1190} color={C.cream} size={46} o={sp(f, 10, 24)}>cả hai đo được bằng thước</Tag>
  </g>
);
// --- Cảnh 4: tính ---
const P15: Panel = ({f}) => (
  <g>
    <Head a="Đường kính = 1" b="mỗi cạnh = nửa đường kính" />
    <Circle cx={CX} cy={640} R={170} o={0.7} />
    <Poly cx={CX} cy={640} R={170} n={6} color={C.amber} w={9} />
    <Calc f={f} y={1010} step={140} lines={[{t: '6 × 0,5 = 3', at: 10, size: 120, color: C.amber}]} />
    <Tag x={CX} y={1190} color={C.cream} size={42} o={sp(f, 20, 34)}>chu vi hình trong = 3</Tag>
  </g>
);
const P16: Panel = ({f}) => (
  <g>
    <Head a="Chu vi hình ngoài" b="khoảng 3,46" />
    <Circle cx={CX} cy={660} R={180} o={0.7} />
    <Poly cx={CX} cy={660} R={180} n={6} out color={BLUE} w={9} />
    <Big x={CX} y={1090} size={130} color={BLUE} o={sp(f, 8, 24)}>≈ 3,46</Big>
  </g>
);
const P17: Panel = ({f}) => (
  <g>
    <Head a="Pi nằm giữa 3 và 3,46" b="khoảng kẹp còn rất rộng" />
    <NL y={880} a={3} b={3.5} lo={3} hi={3.4641} p={sp(f, 6, 34)} d={2} ticks={5} />
    <Hero2 f={f} />
  </g>
);
// --- Cảnh 5: gấp đôi số cạnh ---
const P18: Panel = ({f}) => (
  <g>
    <Head a="Gấp đôi số cạnh" b="hình càng ôm sát vòng tròn" />
    {[6, 12, 24, 48].map((n, i) => (
      <g key={n} opacity={sp(f, 2 + i * 9, 14 + i * 9)}>
        <circle cx={170 + i * 247} cy={820} r={88} fill="none" stroke={C.cream} strokeWidth={4} opacity={0.6} />
        <Poly cx={170 + i * 247} cy={820} R={88} n={n} color={C.amber} w={5} />
        <Poly cx={170 + i * 247} cy={820} R={88} n={n} out color={BLUE} w={5} />
        <Tag x={170 + i * 247} y={990} color={C.cream} size={42}>{n} cạnh</Tag>
      </g>
    ))}
    {[0, 1, 2].map((i) => (
      <Arrow key={i} x1={248 + i * 247} y1={820} x2={262 + i * 247} y2={820} p={sp(f, 12 + i * 9, 20 + i * 9)} w={5} />
    ))}
    <Hero2 f={f} />
  </g>
);
const NLP = (n: number, lo: number, hi: number, label: string): Panel =>
  ({f}) => (
    <g>
      <Head a={`${n} cạnh`} b={label} />
      <Circle cx={CX} cy={640} R={170} o={0.7} />
      <Poly cx={CX} cy={640} R={170} n={n} color={C.amber} w={6} />
      <Poly cx={CX} cy={640} R={170} n={n} out color={BLUE} w={6} />
      <NL y={1060} a={3} b={3.5} lo={lo} hi={hi} p={sp(f, 6, 30)} d={2} ticks={5} />
    </g>
  );
const P19 = NLP(12, 3.11, 3.22, 'pi giữa 3,11 và 3,22');
const P20 = NLP(24, 3.13, 3.16, 'pi giữa 3,13 và 3,16');
const P21 = NLP(48, 3.14, 3.15, 'pi giữa 3,14 và 3,15');
const P22: Panel = ({f}) => (
  <g>
    <Head a="96 cạnh" b="ông dừng ở đó" />
    <Circle cx={CX} cy={CY} R={R} />
    <Poly cx={CX} cy={CY} R={R} n={96} color={C.amber} w={6} />
    <Poly cx={CX} cy={CY} R={R} n={96} out color={BLUE} w={6} />
    <Big x={CX} y={1190} size={110} color={C.amber} o={sp(f, 10, 26)}>96 cạnh</Big>
    <Hero2 f={f} cheer={sp(f, 20, 36)} />
  </g>
);
// --- Cảnh 6: kết quả ---
const P23: Panel = ({f}) => (
  <g>
    <Head a="Archimedes ghi lại" />
    <Big x={CX} y={680} size={112} color={C.cream} o={sp(f, 4, 18)}>π &gt; 223/71</Big>
    <Big x={CX} y={860} size={112} color={C.amber} o={sp(f, 16, 30)}>π &lt; 22/7</Big>
    <Hero2 f={f} />
  </g>
);
const P24: Panel = ({f}) => (
  <g>
    <Head a="Đổi ra số thập phân" />
    <NL y={780} a={3.14} b={3.144} lo={3.1408} hi={3.1429} p={sp(f, 6, 34)} d={3} ticks={4} />
    <Big x={CX} y={1010} size={80} color={C.cream} o={sp(f, 20, 34)}>3,1408 &lt; π &lt; 3,1429</Big>
  </g>
);
const P25: Panel = ({f}) => (
  <g>
    <Head a="Làm tròn theo hướng an toàn" b="nên khoảng kẹp rộng hơn chút" />
    <Tag x={CX} y={650} color={C.amber} size={40}>Archimedes</Tag>
    <NL y={760} a={3.14} b={3.144} lo={3.1408} hi={3.1429} p={sp(f, 4, 26)} d={3} ticks={4} color={C.amber} pi={false} />
    <Tag x={CX} y={950} color={BLUE} size={40}>hình 96 cạnh chính xác</Tag>
    <NL y={1060} a={3.14} b={3.144} lo={3.141} hi={3.1427} p={sp(f, 14, 36)} d={3} ticks={4} color={BLUE} pi={false} />
  </g>
);
const P26: Panel = ({f}) => (
  <g>
    <Head a="Pi thật là 3,1416" b="nằm gọn giữa hai số ấy" />
    <NL y={820} a={3.14} b={3.144} lo={3.1408} hi={3.1429} p={1} d={3} ticks={4} />
    <Big x={CX} y={1060} size={130} color={BLUE} o={sp(f, 6, 22)}>π ≈ 3,1416</Big>
    <Hero2 f={f} cheer={sp(f, 16, 32)} />
  </g>
);
const P27: Panel = ({f}) => (
  <g>
    <Head a="22/7 chỉ lệch pi" b="chưa đến 1 phần nghìn" />
    <Calc f={f} y={700} step={150} lines={[{t: '22 ÷ 7 = 3,14286', at: 4, size: 84}, {t: 'π = 3,14159', at: 14, size: 84, color: BLUE}, {t: 'lệch < 1 phần nghìn', at: 26, size: 78, color: C.amber}]} />
    <Hero2 f={f} />
  </g>
);
const P28: Panel = ({f}) => {
  const k = sp(f, 4, 44);
  return (
    <g>
      <Head a="Cứ gấp đôi số cạnh" b="kẹp chính xác đến đâu cũng được" />
      <NL y={820} a={3} b={3.5} lo={lerp(3, 3.1408, k)} hi={lerp(3.4641, 3.1429, k)} p={1} d={2} ticks={5} />
      <Tag x={CX} y={1050} color={C.cream} size={44} o={sp(f, 20, 34)}>thêm cạnh → kẹp hẹp dần</Tag>
      <Hero2 f={f} />
    </g>
  );
};
const P29: Panel = ({f}) => (
  <g>
    <Head a="Ngày nay máy tính tính được" b="hơn 100 nghìn tỉ chữ số" />
    <Digits f={f} y={620} lines={['3,14159265358979', '32384626433832', '79502884197169']} size={70} step={96} />
    <Big x={CX} y={1000} size={104} color={C.amber} o={sp(f, 18, 34)}>hơn 100 nghìn tỉ</Big>
    <Hero2 f={f} x={540} />
  </g>
);
const P30: Panel = ({f}) => (
  <g>
    <Head a="Pi dài vô tận" b="nhưng ta kẹp được nó" />
    <Circle cx={CX} cy={760} R={230} />
    <Poly cx={CX} cy={760} R={230} n={96} color={C.amber} w={6} />
    <Poly cx={CX} cy={760} R={230} n={96} out color={BLUE} w={6} />
    <Big x={CX} y={790} size={120} color={C.cream} o={sp(f, 4, 18)}>π</Big>
    <Hero2 f={f} cheer={sp(f, 10, 28)} />
  </g>
);

export const PANELS: Panel[] = [P0, P1, P2, P3, P4, P5, P6, P7, P8, P9, P10, P11, P12, P13, P14, P15, P16, P17, P18, P19, P20, P21, P22, P23, P24, P25, P26, P27, P28, P29, P30];
