import React from 'react';
import {Arrow, Big, C, Calc, Head, HatHero, Panel, Tag, clamp01, lerp, sp} from '../khoahoc/kit';

const BOB = '#d9a23a';
const EARTH = '#3f7fc4';
const RED = '#e0613b';
const FLOOR = '#4b463a';
const AM = C.amber;

const Hero2: React.FC<{f: number; x?: number; cheer?: number}> = ({f, x = 170, cheer = 0}) => <HatHero x={x} y={1250} s={2} walk={f * 0.13} cheer={cheer} hat="scholar" />;

const Pend: React.FC<{f: number; x: number; y: number; len: number; amp?: number; r?: number; speed?: number; fixed?: number}> = ({f, x, y, len, amp = 0.35, r = 34, speed = 0.1, fixed}) => {
  const a = fixed !== undefined ? fixed : amp * Math.sin(f * speed);
  const bx = x + len * Math.sin(a);
  const by = y + len * Math.cos(a);
  return (
    <g>
      <line x1={x - 90} y1={y} x2={x + 90} y2={y} stroke={C.cream} strokeWidth={10} strokeLinecap="round" />
      <line x1={x} y1={y} x2={bx} y2={by} stroke={C.cream} strokeWidth={5} />
      <circle cx={bx} cy={by} r={r} fill={BOB} stroke={C.cream} strokeWidth={6} />
    </g>
  );
};
const Globe: React.FC<{cx: number; cy: number; r: number; o?: number}> = ({cx, cy, r, o = 1}) => (
  <g opacity={clamp01(o)}>
    <circle cx={cx} cy={cy} r={r} fill={EARTH} stroke={C.cream} strokeWidth={6} />
    <path d={`M ${cx - r * 0.5} ${cy - r * 0.45} q ${r * 0.3} ${-r * 0.15} ${r * 0.5} ${r * 0.15} q ${-r * 0.1} ${r * 0.4} ${-r * 0.45} ${r * 0.3} z`} fill="#4f9a5a" />
    <path d={`M ${cx + r * 0.1} ${cy + r * 0.2} q ${r * 0.4} ${-r * 0.1} ${r * 0.45} ${r * 0.25} q ${-r * 0.2} ${r * 0.4} ${-r * 0.5} ${r * 0.2} z`} fill="#4f9a5a" />
  </g>
);
// Nhìn từ trên xuống: sàn tròn + vạch mặt phẳng lắc.
const Top: React.FC<{cx: number; cy: number; r: number; floorRot: number; lineRot: number; showFloor?: boolean}> = ({cx, cy, r, floorRot, lineRot, showFloor = true}) => (
  <g>
    <g transform={`rotate(${floorRot} ${cx} ${cy})`}>
      <circle cx={cx} cy={cy} r={r} fill={FLOOR} stroke={C.cream} strokeWidth={6} />
      {showFloor &&
        [0, 45, 90, 135].map((d) => (
          <line key={d} x1={cx - r * Math.cos((d * Math.PI) / 180)} y1={cy - r * Math.sin((d * Math.PI) / 180)} x2={cx + r * Math.cos((d * Math.PI) / 180)} y2={cy + r * Math.sin((d * Math.PI) / 180)} stroke={C.cream} strokeWidth={2} opacity={0.25} />
        ))}
      <circle cx={cx + r * 0.7} cy={cy} r={12} fill={RED} />
    </g>
    <g transform={`rotate(${lineRot} ${cx} ${cy})`}>
      <line x1={cx - r * 0.95} y1={cy} x2={cx + r * 0.95} y2={cy} stroke={AM} strokeWidth={10} strokeLinecap="round" />
      <circle cx={cx} cy={cy} r={12} fill={BOB} stroke={C.cream} strokeWidth={4} />
    </g>
  </g>
);

const CX = 540;

// --- Cảnh 1 ---
const P0: Panel = ({f}) => (
  <g>
    <Head a="Đứng trên Trái Đất" b="chẳng thấy nó quay" />
    <Globe cx={CX} cy={780} r={260} o={sp(f, 2, 14)} />
    <Big x={830} y={560} size={150} color={AM} o={0.9 * sp(f, 14, 30)}>?</Big>
    <Hero2 f={f} />
  </g>
);
const P1: Panel = ({f}) => (
  <g>
    <Head a="Năm 1851" b="một quả nặng treo dây" />
    <Pend f={f} x={CX} y={520} len={560} amp={0.3} r={44} speed={0.09} />
    <Hero2 f={f} />
  </g>
);
const P2: Panel = ({f}) => (
  <g>
    <Head a="Mặt phẳng đung đưa" b="của nó chầm chậm xoay" />
    <Top cx={CX} cy={800} r={290} floorRot={0} lineRot={lerp(0, 50, sp(f, 4, 60))} showFloor={false} />
    <Tag x={CX} y={1190} color={AM} size={46} o={sp(f, 14, 30)}>nhìn từ trên xuống</Tag>
  </g>
);
const P3: Panel = ({f}) => (
  <g>
    <Head a="Vì sao nó xoay" b="và nói gì về Trái Đất?" />
    <Pend f={f} x={380} y={560} len={400} amp={0.3} r={36} speed={0.09} />
    <Globe cx={760} cy={900} r={170} />
    <Big x={780} y={620} size={140} color={AM} o={0.9 * sp(f, 10, 26)}>?</Big>
    <Hero2 f={f} />
  </g>
);
// --- Cảnh 2: Panthéon ---
const P4: Panel = ({f}) => (
  <g>
    <Head a="Người làm thí nghiệm" b="là Foucault" />
    <HatHero x={540} y={1050} s={3.2} walk={f * 0.12} cheer={sp(f, 10, 26)} hat="scholar" />
    <Tag x={540} y={1180} color={C.cream} size={52} o={sp(f, 12, 26)}>Foucault</Tag>
  </g>
);
const P5: Panel = ({f}) => (
  <g>
    <Head a="Quả nặng 28 ki-lô-gam" b="dây dài 67 mét" />
    <path d="M 220 560 A 320 200 0 0 1 860 560 Z" fill="#6d6454" stroke={C.cream} strokeWidth={6} />
    <Pend f={f} x={CX} y={560} len={560} amp={0.22} r={42} speed={0.08} />
    <Tag x={760} y={880} color={C.cream} size={44} o={sp(f, 10, 24)}>dây 67 mét</Tag>
    <Tag x={CX} y={1240} color={AM} size={44} o={sp(f, 16, 30)}>nặng 28 ki-lô-gam</Tag>
  </g>
);
const P6: Panel = ({f}) => (
  <g>
    <Head a="67 mét" b="cao hơn 20 tầng nhà" />
    <rect x={560} y={520} width={300} height={700} fill="#5b5547" stroke={C.cream} strokeWidth={5} />
    {Array.from({length: 20}).map((_, i) => (
      <line key={i} x1={560} y1={520 + i * 35} x2={860} y2={520 + i * 35} stroke={C.cream} strokeWidth={2} opacity={0.5} />
    ))}
    <line x1={450} y1={520} x2={450} y2={520 + 700 * sp(f, 4, 30)} stroke={C.cream} strokeWidth={6} />
    <circle cx={450} cy={520 + 700 * sp(f, 4, 30)} r={34} fill={BOB} stroke={C.cream} strokeWidth={5} />
    <Tag x={310} y={880} color={AM} size={44} o={sp(f, 20, 34)}>67 m</Tag>
    <Tag x={710} y={1290} color={C.cream} size={42} o={sp(f, 22, 36)}>20 tầng</Tag>
  </g>
);
const P7: Panel = ({f}) => (
  <g>
    <Head a="Dây dài nên đung đưa" b="rất chậm, ai cũng nhìn kịp" />
    <Pend f={f} x={CX} y={520} len={600} amp={0.28} r={44} speed={0.06} />
    <Hero2 f={f} />
  </g>
);
// --- Cảnh 3: bàn xoay ---
const P8: Panel = ({f}) => {
  const th = (f * 1.2 * Math.PI) / 180;
  const R = 290;
  const px0 = -R * 0.9;
  const tt = clamp01(f / 70);
  const trace: string[] = [];
  const N = Math.floor(tt * 40);
  for (let i = 0; i <= N; i++) {
    const t = i / 40;
    const px = lerp(px0, -px0, t);
    const ang = -(t * 70 * 1.2 * Math.PI) / 180;
    trace.push(`${i ? 'L' : 'M'} ${CX + px * Math.cos(ang)} ${800 + px * Math.sin(ang)}`);
  }
  void th;
  return (
    <g>
      <Head a="Đặt tờ giấy lên bàn xoay" b="dùng thước vẽ đường thẳng" />
      <g transform={`rotate(${f * 1.2} ${CX} 800)`}>
        <circle cx={CX} cy={800} r={R} fill="#efe3c8" stroke={C.cream} strokeWidth={6} />
        <path d={trace.join(' ')} fill="none" stroke={RED} strokeWidth={7} strokeLinecap="round" />
      </g>
      <line x1={CX - R - 20} y1={800} x2={CX + R + 20} y2={800} stroke={C.cream} strokeWidth={4} strokeDasharray="10 10" opacity={0.6} />
      <circle cx={CX + lerp(px0, -px0, tt)} cy={800} r={14} fill={AM} />
      <Hero2 f={f} />
    </g>
  );
};
const P9: Panel = ({f}) => (
  <g>
    <Head a="Khi bàn dừng, đường bị cong" b="dù tay vẽ thẳng" />
    <circle cx={CX} cy={800} r={290} fill="#efe3c8" stroke={C.cream} strokeWidth={6} />
    <path d="M 290 880 Q 420 1000 560 760 T 790 620" fill="none" stroke={RED} strokeWidth={8} strokeLinecap="round" opacity={sp(f, 4, 18)} />
    <Tag x={CX} y={1190} color={AM} size={46} o={sp(f, 16, 30)}>đường vẽ bị cong</Tag>
  </g>
);
const P10: Panel = ({f}) => (
  <g>
    <Head a="Quả nặng như cây bút" b="theo một hướng cố định" />
    <Top cx={CX} cy={800} r={290} floorRot={0} lineRot={0} showFloor={false} />
    <Pend f={f} x={CX} y={1110} len={110} amp={0.45} r={22} speed={0.12} />
    <Tag x={CX} y={1270} color={AM} size={44} o={sp(f, 14, 28)}>hướng cố định trong không gian</Tag>
  </g>
);
const P11: Panel = ({f}) => (
  <g>
    <Head a="Mặt đất như tờ giấy" b="xoay cùng Trái Đất" />
    <Top cx={CX} cy={800} r={290} floorRot={f * 1.2} lineRot={0} />
    <Arrow x1={CX + 330} y1={600} x2={CX + 330} y2={760} color={C.cream} w={6} p={sp(f, 8, 24)} />
    <Tag x={CX} y={1190} color={C.cream} size={44} o={sp(f, 14, 28)}>sàn xoay, vạch vẫn đứng yên</Tag>
  </g>
);
const P12: Panel = ({f}) => (
  <g>
    <Head a="Nên người đứng dưới thấy" b="mặt phẳng lệch dần" />
    <Top cx={CX} cy={800} r={290} floorRot={f * 1.2} lineRot={0} />
    <Top cx={CX} cy={800} r={0.01} floorRot={0} lineRot={0} showFloor={false} />
    <Tag x={CX} y={1190} color={AM} size={44} o={sp(f, 10, 24)}>đứng trên sàn: thấy vạch xoay ngược</Tag>
  </g>
);
// --- Cảnh 4: tính ---
const P13: Panel = ({f}) => (
  <g>
    <Head a="Ở Bắc Cực" b="xoay trọn một vòng trong một ngày" />
    <Globe cx={CX} cy={820} r={250} />
    <circle cx={CX} cy={820} r={14} fill={C.cream} />
    <Tag x={CX} y={760} color={C.cream} size={40}>Bắc Cực</Tag>
    <line x1={CX - 200} y1={820} x2={CX + 200} y2={820} stroke={AM} strokeWidth={8} transform={`rotate(${lerp(0, 360, sp(f, 4, 60))} ${CX} 820)`} />
    <Tag x={CX} y={1160} color={AM} size={44} o={sp(f, 20, 34)}>1 vòng = 1 ngày</Tag>
  </g>
);
const P14: Panel = ({f}) => (
  <g>
    <Head a="Trái Đất quay" b="360 độ trong 24 giờ" />
    <Calc f={f} y={780} step={170} lines={[{t: '360 độ', at: 2, size: 130}, {t: '24 giờ', at: 12, size: 130, color: AM}]} />
    <Hero2 f={f} />
  </g>
);
const P15: Panel = ({f}) => (
  <g>
    <Head a="Mỗi giờ quay" />
    <Calc f={f} y={780} step={170} lines={[{t: '360 ÷ 24', at: 2, size: 120}, {t: '= 15 độ mỗi giờ', at: 12, size: 120, color: AM}]} />
    <Hero2 f={f} cheer={sp(f, 14, 30)} />
  </g>
);
// --- Cảnh 5: Paris ---
const P16: Panel = ({f}) => {
  const lat = (48.8 * Math.PI) / 180;
  return (
    <g>
      <Head a="Đền ấy ở Paris" b="không phải ở Bắc Cực" />
      <Globe cx={CX} cy={800} r={270} />
      <circle cx={CX} cy={800 - 270} r={14} fill={C.cream} />
      <Tag x={CX + 140} y={540} color={C.cream} size={38} anchor="start">Bắc Cực</Tag>
      <circle cx={CX + 270 * Math.cos(lat)} cy={800 - 270 * Math.sin(lat)} r={16} fill={RED} opacity={sp(f, 8, 22)} />
      <Tag x={CX + 390} y={640} color={RED} size={42} o={sp(f, 10, 24)}>Paris</Tag>
    </g>
  );
};
const P17: Panel = ({f}) => (
  <g>
    <Head a="Tốc độ xoay" b="15 độ × sin của vĩ độ" />
    <Calc f={f} y={780} step={170} lines={[{t: '15° × sin(vĩ độ)', at: 4, size: 100, color: AM}]} />
    <Tag x={CX} y={980} color={C.cream} size={44} o={sp(f, 16, 30)}>sin: con số từ 0 tới 1</Tag>
    <Hero2 f={f} />
  </g>
);
const P18: Panel = ({f}) => (
  <g>
    <Head a="Sin vĩ độ" b="0 ở xích đạo, 1 ở cực" />
    <line x1={140} y1={1000} x2={940} y2={1000} stroke={C.cream} strokeWidth={5} />
    <line x1={140} y1={1000} x2={140} y2={640} stroke={C.cream} strokeWidth={5} />
    <path d={Array.from({length: 31}, (_, i) => `${i ? 'L' : 'M'} ${140 + (800 * i) / 30} ${1000 - 340 * Math.sin((i / 30) * (Math.PI / 2)) * sp(f, 2, 34)}`).join(' ')} fill="none" stroke={AM} strokeWidth={8} />
    <Tag x={140} y={1070} color={C.cream} size={40}>xích đạo 0</Tag>
    <Tag x={900} y={1070} color={C.cream} size={40}>cực 1</Tag>
  </g>
);
const P19: Panel = ({f}) => (
  <g>
    <Head a="Paris ở khoảng 48,8 độ Bắc" b="sin khoảng 0,75" />
    <line x1={140} y1={1000} x2={940} y2={1000} stroke={C.cream} strokeWidth={5} />
    <path d={Array.from({length: 31}, (_, i) => `${i ? 'L' : 'M'} ${140 + (800 * i) / 30} ${1000 - 340 * Math.sin((i / 30) * (Math.PI / 2))}`).join(' ')} fill="none" stroke={AM} strokeWidth={8} opacity={0.6} />
    <line x1={140 + (800 * 48.8) / 90} y1={1000} x2={140 + (800 * 48.8) / 90} y2={1000 - 340 * 0.753} stroke={RED} strokeWidth={6} opacity={sp(f, 6, 20)} />
    <circle cx={140 + (800 * 48.8) / 90} cy={1000 - 340 * 0.753} r={14} fill={RED} opacity={sp(f, 10, 24)} />
    <Big x={CX} y={1170} size={96} color={AM} o={sp(f, 18, 34)}>sin ≈ 0,75</Big>
  </g>
);
const P20: Panel = ({f}) => (
  <g>
    <Head a="Tốc độ xoay ở Paris" />
    <Calc f={f} y={780} step={170} lines={[{t: '15 × 0,75', at: 2, size: 120}, {t: '≈ 11,3 độ mỗi giờ', at: 12, size: 110, color: AM}]} />
    <Hero2 f={f} />
  </g>
);
const P21: Panel = ({f}) => (
  <g>
    <Head a="Đúng như Foucault thấy" b="hơn 11 độ mỗi giờ" />
    <Big x={CX} y={820} size={170} color={AM} o={sp(f, 4, 18)}>11,3° / giờ</Big>
    <Hero2 f={f} cheer={sp(f, 10, 26)} />
  </g>
);
const P22: Panel = ({f}) => (
  <g>
    <Head a="Một vòng ở Paris" />
    <Calc f={f} y={780} step={170} lines={[{t: '360 ÷ 11,3', at: 2, size: 120}, {t: '≈ 32 giờ', at: 12, size: 130, color: AM}]} />
    <Hero2 f={f} />
  </g>
);
// --- Cảnh 6: kết ---
const P23: Panel = ({f}) => (
  <g>
    <Head a="Ở xích đạo sin bằng 0" b="quả lắc không xoay" />
    <Globe cx={CX} cy={800} r={270} />
    <line x1={CX - 270} y1={800} x2={CX + 270} y2={800} stroke={RED} strokeWidth={6} strokeDasharray="12 10" />
    <Tag x={CX} y={1170} color={RED} size={46} o={sp(f, 8, 22)}>xích đạo: không xoay</Tag>
  </g>
);
const P24: Panel = ({f}) => (
  <g>
    <Head a="Thí nghiệm đơn giản đầu tiên" b="cho thấy trực tiếp Trái Đất quay" />
    <Pend f={f} x={380} y={560} len={420} amp={0.3} r={36} speed={0.09} />
    <Globe cx={760} cy={900} r={170} />
    <Arrow x1={680} y1={680} x2={840} y2={680} color={C.cream} w={6} p={sp(f, 6, 22)} />
    <Hero2 f={f} />
  </g>
);
const P25: Panel = ({f}) => (
  <g>
    <Head a="Chỉ cần quả nặng và sợi dây" b="đứng yên trong phòng" />
    <Pend f={f} x={CX} y={540} len={520} amp={0.28} r={40} speed={0.09} />
    <Hero2 f={f} />
  </g>
);
const P26: Panel = ({f}) => (
  <g>
    <Head a="Quả lắc xoay vì chính ta" b="đang xoay cùng Trái Đất" />
    <Top cx={CX} cy={800} r={290} floorRot={f * 0.6} lineRot={0} />
    <Hero2 f={f} cheer={sp(f, 10, 28)} />
  </g>
);

export const PANELS: Panel[] = [P0, P1, P2, P3, P4, P5, P6, P7, P8, P9, P10, P11, P12, P13, P14, P15, P16, P17, P18, P19, P20, P21, P22, P23, P24, P25, P26];
