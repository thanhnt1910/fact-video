import React from 'react';
import {Arrow, Big, C, Calc, Head, HatHero, Panel, Tag, clamp01, lerp, sp} from '../khoahoc/kit';

const STONE = '#9aa3a8';
const WATER = '#4f9fc4';
const WOOD = '#b98a52';
const RED = '#e0613b';
const AM = C.amber;
const CX = 540;

const Hero2: React.FC<{f: number; x?: number; cheer?: number}> = ({f, x = 170, cheer = 0}) => <HatHero x={x} y={1250} s={2} walk={f * 0.13} cheer={cheer} hat="scholar" />;

const Rock: React.FC<{x: number; y: number; r?: number}> = ({x, y, r = 26}) => (
  <g>
    <circle cx={x} cy={y} r={r} fill={STONE} stroke={C.cream} strokeWidth={5} />
    <circle cx={x - r * 0.3} cy={y - r * 0.3} r={r * 0.25} fill={C.cream} opacity={0.35} />
  </g>
);

// Giếng cắt ngang: miệng giếng y=520, đáy nước y=1180, hai thành x=CX±130.
const WT = 520, WB = 1180, WX = 240, WW = 130;
const Well: React.FC<{f: number; drop?: number; water?: boolean; ripple?: number}> = ({f, drop, water = true, ripple}) => (
  <g>
    <rect x={WX + 140} y={WT} width={WW * 2 - 280 + 280 - 140} height={0} fill="none" />
    <rect x={CX - WW} y={WT} width={WW * 2} height={WB - WT} fill="#0d1415" stroke={C.cream} strokeWidth={5} opacity={0.9} />
    {water && <rect x={CX - WW + 3} y={WB - 70} width={WW * 2 - 6} height={70} fill={WATER} opacity={0.75} />}
    <rect x={CX - WW - 36} y={WT - 26} width={36} height={26} fill={STONE} stroke={C.cream} strokeWidth={4} />
    <rect x={CX + WW} y={WT - 26} width={36} height={26} fill={STONE} stroke={C.cream} strokeWidth={4} />
    {ripple !== undefined && (
      <ellipse cx={CX} cy={WB - 70} rx={20 + 90 * clamp01(ripple)} ry={6 + 14 * clamp01(ripple)} fill="none" stroke={C.cream} strokeWidth={4} opacity={1 - clamp01(ripple)} />
    )}
    {drop !== undefined && <Rock x={CX} y={lerp(WT - 30, WB - 80, clamp01(drop))} />}
  </g>
);

const Ramp: React.FC<{ball?: number; marks?: number; label?: boolean}> = ({ball, marks = 0, label}) => {
  const x1 = 200, y1 = 640, x2 = 900, y2 = 1000;
  const P = (u: number) => ({x: lerp(x1, x2, u), y: lerp(y1, y2, u) - 32});
  const b = ball !== undefined ? P(clamp01(ball)) : null;
  return (
    <g>
      <line x1={x1} y1={y1} x2={x2} y2={y2} stroke={WOOD} strokeWidth={26} strokeLinecap="round" />
      <line x1={x1} y1={y1 - 13} x2={x2} y2={y2 - 13} stroke={C.cream} strokeWidth={4} opacity={0.6} />
      {[1, 4, 9].map((n, i) => {
        const u = n / 9;
        const p = P(u);
        return marks > i ? (
          <g key={n}>
            <line x1={p.x} y1={p.y + 22} x2={p.x} y2={p.y + 82} stroke={AM} strokeWidth={6} />
            <Big x={p.x} y={p.y + 150} size={62} color={AM}>{String(n)}</Big>
          </g>
        ) : null;
      })}
      {b && <circle cx={b.x} cy={b.y} r={28} fill={RED} stroke={C.cream} strokeWidth={5} />}
      {label && (
        <g>
          <line x1={x1} y1={y1 - 90} x2={x2} y2={y2 - 90} stroke={C.cream} strokeWidth={4} strokeDasharray="12 10" opacity={0.8} />
          <Big x={CX + 60} y={700} size={90} color={AM}>6 m</Big>
        </g>
      )}
    </g>
  );
};

// --- Cảnh 1: câu hỏi ---
const P0: Panel = ({f}) => (
  <g>
    <Head a="Thả đá, đếm giây" b="giếng sâu bao nhiêu?" />
    <Well f={f} drop={sp(f, 10, 50)} ripple={f > 50 ? (f - 50) / 30 : undefined} />
    <Big x={CX + 300} y={760} size={150} color={AM} o={0.9 * sp(f, 40, 56)}>?</Big>
    <Hero2 f={f} />
  </g>
);
const P1: Panel = ({f}) => {
  const ys = [0, 1, 2, 3].map((n) => 560 + 22 * n * n * 1.7);
  return (
    <g>
      <Head a="Đá rơi càng lúc" b="càng nhanh" />
      {ys.map((y, i) => (
        <g key={i} opacity={sp(f, 4 + i * 8, 16 + i * 8)}>
          <Rock x={CX} y={y} r={22} />
        </g>
      ))}
      <Arrow x1={CX + 110} y1={560} x2={CX + 110} y2={1000} color={RED} p={sp(f, 10, 40)} />
      <Tag x={CX + 250} y={1060} color={AM} size={40} o={sp(f, 24, 40)}>mỗi giây xa hơn</Tag>
    </g>
  );
};
const P2: Panel = ({f}) => (
  <g>
    <Head a="Một quy luật gọn" b="tìm ra nhờ máng gỗ" />
    <g opacity={sp(f, 2, 16)}><Ramp ball={sp(f, 10, 70)} /></g>
    <Hero2 f={f} />
  </g>
);
// --- Cảnh 2: Galileo và máng dốc ---
const P3: Panel = ({f}) => (
  <g>
    <Head a="Hơn 400 năm trước" b="Galileo đo chuyện vật rơi" />
    <Big x={CX} y={820} size={200} color={AM} o={sp(f, 2, 18)}>400+</Big>
    <Tag x={CX} y={980} color={C.cream} size={46} o={sp(f, 12, 26)}>năm trước</Tag>
    <Hero2 f={f} />
  </g>
);
const P4: Panel = ({f}) => (
  <g>
    <Head a="Đá rơi quá nhanh" b="chưa có đồng hồ bấm giây" />
    <Rock x={CX} y={lerp(560, 1080, clamp01(f / 18))} />
    <circle cx={CX + 160} cy={820} r={90} fill="none" stroke={C.cream} strokeWidth={8} opacity={sp(f, 8, 22)} />
    <line x1={CX + 100} y1={880} x2={CX + 220} y2={760} stroke={RED} strokeWidth={12} strokeLinecap="round" opacity={sp(f, 16, 30)} />
    <Hero2 f={f} />
  </g>
);
const P5: Panel = ({f}) => (
  <g>
    <Head a="Cho nó rơi chậm lại" b="lăn bóng xuống máng dốc" />
    <Ramp ball={sp(f, 10, 90)} />
    <Hero2 f={f} />
  </g>
);
const P6: Panel = ({f}) => (
  <g>
    <Head a="Máng gỗ dài khoảng 6 mét" b="rãnh thẳng và nhẵn" />
    <Ramp label ball={0.04} />
    <Hero2 f={f} />
  </g>
);
const P7: Panel = ({f}) => (
  <g>
    <Head a="Bóng cũng nhanh dần" b="chỉ là chậm hơn" />
    <Ramp ball={Math.pow(clamp01(f / 100), 2)} />
    <Hero2 f={f} />
  </g>
);
const P8: Panel = ({f}) => {
  const drop = (f % 24) / 24;
  return (
    <g>
      <Head a="Đo thời gian" b="bằng đồng hồ nước" />
      <path d="M 400 520 L 680 520 L 600 700 L 480 700 Z" fill={WATER} fillOpacity={0.5} stroke={C.cream} strokeWidth={6} strokeLinejoin="round" />
      <rect x={500} y={1000} width={80} height={170} rx={10} fill="none" stroke={C.cream} strokeWidth={6} />
      <rect x={504} y={1170 - 160 * sp(f, 0, 90)} width={72} height={160 * sp(f, 0, 90)} fill={WATER} opacity={0.8} />
      <line x1={540} y1={700} x2={540} y2={1000} stroke={WATER} strokeWidth={5} strokeDasharray="14 16" strokeDashoffset={-f * 4} />
      <circle cx={540} cy={720 + 240 * drop * drop} r={9} fill={C.cream} opacity={0.9} />
      <Hero2 f={f} />
    </g>
  );
};
// --- Cảnh 3: bình phương ---
const P9: Panel = ({f}) => (
  <g>
    <Head a="Đánh dấu chỗ bóng tới" b="sau những khoảng thời gian bằng nhau" />
    <Ramp marks={f > 70 ? 3 : f > 44 ? 2 : f > 16 ? 1 : 0} ball={0.0 + sp(f, 4, 100)} />
    <Hero2 f={f} />
  </g>
);
const P10: Panel = ({f}) => (
  <g>
    <Head a="Gấp 4 lần, gấp 9 lần" b="chứ không gấp 2, gấp 3" />
    <Calc f={f} x={620} y={760} step={170} lines={[{t: '2 khoảng → 4 lần', at: 4, size: 96, color: AM}, {t: '3 khoảng → 9 lần', at: 40, size: 96, color: AM}]} />
    <Hero2 f={f} />
  </g>
);
const P11: Panel = ({f}) => (
  <g>
    <Head a="Đó là các số" b="bình phương" />
    <Calc f={f} x={620} y={760} step={170} lines={[{t: '4 = 2 × 2', at: 4, size: 110}, {t: '9 = 3 × 3', at: 34, size: 110}]} />
    <Hero2 f={f} />
  </g>
);
const P12: Panel = ({f}) => (
  <g>
    <Head a="Quãng đường đi được" b="lớn theo bình phương thời gian" />
    <Big x={CX + 60} y={800} size={130} color={AM} o={sp(f, 4, 20)}>thời gian²</Big>
    <Arrow x1={CX + 60} y1={850} x2={CX + 60} y2={1010} color={RED} p={sp(f, 14, 34)} />
    <Big x={CX + 60} y={1130} size={110} color={C.cream} o={sp(f, 24, 40)}>quãng đường</Big>
    <Hero2 f={f} />
  </g>
);
// --- Cảnh 4: công thức ---
const P13: Panel = ({f}) => (
  <g>
    <Head a="Với vật rơi" b="công thức là" />
    <Big x={CX + 60} y={700} size={96} color={C.cream} o={sp(f, 2, 14)}>quãng đường =</Big>
    <Big x={CX + 60} y={850} size={120} color={AM} o={sp(f, 14, 28)}>½ × g × t²</Big>
    <Tag x={CX + 60} y={960} color={C.cream} size={42} o={sp(f, 26, 40)}>t là thời gian rơi, tính bằng giây</Tag>
    <Hero2 f={f} />
  </g>
);
const P14: Panel = ({f}) => (
  <g>
    <Head a="g ≈ 9,8" b="mỗi giây nhanh thêm 9,8 m/s" />
    <Big x={CX + 60} y={800} size={190} color={AM} o={sp(f, 2, 18)}>g ≈ 9,8</Big>
    <Rock x={CX + 60} y={lerp(900, 1200, clamp01((f % 60) / 60) ** 2)} />
    <Hero2 f={f} />
  </g>
);
const P15: Panel = ({f}) => (
  <g>
    <Head a="Rơi 1 giây" />
    <Calc f={f} x={620} y={740} step={150} lines={[{t: '½ × 9,8 × 1 × 1', at: 2, size: 96}, {t: '= 4,9 m', at: 28, size: 140, color: AM}]} />
    <Hero2 f={f} />
  </g>
);
const P16: Panel = ({f}) => (
  <g>
    <Head a="Rơi 2 giây" />
    <Calc f={f} x={620} y={740} step={150} lines={[{t: '½ × 9,8 × 4', at: 2, size: 110}, {t: '= 19,6 m', at: 28, size: 140, color: AM}]} />
    <Hero2 f={f} />
  </g>
);
const P17: Panel = ({f}) => (
  <g>
    <Head a="Rơi 3 giây" />
    <Calc f={f} x={620} y={740} step={150} lines={[{t: '½ × 9,8 × 9', at: 2, size: 110}, {t: '= 44,1 m', at: 28, size: 140, color: AM}]} />
    <Hero2 f={f} />
  </g>
);
const P18: Panel = ({f}) => (
  <g>
    <Head a="Đếm được 3 giây" b="giếng sâu khoảng 44 mét" />
    <Well f={f} drop={1} ripple={(f % 50) / 50} />
    <Arrow x1={CX + 190} y1={WT} x2={CX + 190} y2={WB - 70} color={RED} p={sp(f, 4, 30)} />
    <Big x={CX + 350} y={860} size={100} color={AM} o={sp(f, 20, 36)}>44 m</Big>
    <Hero2 f={f} />
  </g>
);
const P19: Panel = ({f}) => (
  <g>
    <Head a="Cao ngang tòa nhà" b="khoảng 15 tầng" />
    {Array.from({length: 15}).map((_, i) => (
      <rect key={i} x={CX - 130} y={1180 - (i + 1) * 46 * sp(f, 2 + i * 2, 14 + i * 2)} width={260} height={44} fill={i % 2 ? '#5d6e72' : '#6f8286'} stroke={C.cream} strokeWidth={3} />
    ))}
    <Big x={CX + 340} y={760} size={130} color={AM} o={sp(f, 30, 44)}>15</Big>
    <Hero2 f={f} />
  </g>
);
// --- Cảnh 5: nặng hay nhẹ, tiếng tõm ---
const P20: Panel = ({f}) => (
  <g>
    <Head a="Đá nặng và đá nhẹ" b="rơi có khác nhau không?" />
    <Rock x={CX - 150} y={820} r={60} />
    <Rock x={CX + 150} y={840} r={24} />
    <Big x={CX} y={1020} size={150} color={AM} o={sp(f, 8, 24)}>?</Big>
    <Hero2 f={f} />
  </g>
);
const P21: Panel = ({f}) => {
  const t = clamp01(f / 70);
  return (
    <g>
      <Head a="Lông chim rơi chậm" b="vì không khí cản nó" />
      <Rock x={CX - 150} y={lerp(560, 1150, t * t)} r={26} />
      <path d={`M ${CX + 150} ${lerp(560, 1150, t * 0.35 + 0.02 * Math.sin(f * 0.3))} q 22 -28 6 -62 q -30 30 -6 62 z`} fill={C.cream} stroke={C.cream} strokeWidth={3} transform={`rotate(${20 * Math.sin(f * 0.2)} ${CX + 150} ${lerp(560, 1150, t * 0.35)})`} />
      <Hero2 f={f} />
    </g>
  );
};
const P22: Panel = ({f}) => {
  const t = clamp01((f - 8) / 70);
  return (
    <g>
      <Head a="Không có không khí" b="mọi vật rơi cùng lúc" />
      <Rock x={CX - 150} y={lerp(560, 1150, t * t)} r={50} />
      <Rock x={CX + 150} y={lerp(560, 1150, t * t)} r={20} />
      <line x1={CX - 330} y1={1150} x2={CX + 330} y2={1150} stroke={C.cream} strokeWidth={4} opacity={0.5} />
      <Hero2 f={f} />
    </g>
  );
};
const P23: Panel = ({f}) => (
  <g>
    <Head a="Công thức không cần biết" b="đá nặng bao nhiêu" />
    <Big x={CX + 60} y={800} size={120} color={AM} o={sp(f, 2, 16)}>½ × g × t²</Big>
    <Big x={CX + 60} y={980} size={90} color={C.cream} o={sp(f, 16, 30)}>khối lượng</Big>
    <line x1={CX - 230} y1={955} x2={CX + 350} y2={955} stroke={RED} strokeWidth={10} strokeLinecap="round" opacity={sp(f, 26, 40)} />
    <Hero2 f={f} />
  </g>
);
const P24: Panel = ({f}) => (
  <g>
    <Head a="Tiếng tõm bay lên" b="mất khoảng 1/8 giây" />
    <Well f={f} drop={1} ripple={0.5} />
    {[0, 1, 2].map((i) => {
      const t = ((f * 0.03 + i * 0.33) % 1);
      return <path key={i} d={`M ${CX - 60} ${lerp(1100, 640, t)} q 60 -40 120 0`} fill="none" stroke={AM} strokeWidth={6} strokeLinecap="round" opacity={1 - t} />;
    })}
    <Big x={CX + 360} y={860} size={90} color={AM} o={sp(f, 10, 26)}>⅛ giây</Big>
    <Hero2 f={f} />
  </g>
);
const P25: Panel = ({f}) => (
  <g>
    <Head a="Giếng sâu thì trừ bớt" b="thời gian ấy khỏi số giây đếm" />
    <Calc f={f} x={620} y={740} step={150} lines={[{t: 'số giây đếm', at: 2, size: 90}, {t: '− thời gian âm thanh', at: 22, size: 80, color: AM}]} />
    <Hero2 f={f} />
  </g>
);
const P26: Panel = ({f}) => (
  <g>
    <Head a="Một hòn đá, vài giây đếm" b="là biết giếng sâu bao nhiêu" />
    <Well f={f} drop={sp(f, 6, 40)} ripple={f > 40 ? (f - 40) / 30 : undefined} />
    <Hero2 f={f} cheer={sp(f, 40, 56)} />
  </g>
);
const P27: Panel = ({f}) => (
  <g>
    <Head a="Quy luật Galileo tìm ra" b="từ một cái máng gỗ" />
    <Ramp ball={Math.pow(clamp01(f / 110), 2)} />
    <Hero2 f={f} cheer={sp(f, 10, 28)} />
  </g>
);

export const PANELS: Panel[] = [P0, P1, P2, P3, P4, P5, P6, P7, P8, P9, P10, P11, P12, P13, P14, P15, P16, P17, P18, P19, P20, P21, P22, P23, P24, P25, P26, P27];
