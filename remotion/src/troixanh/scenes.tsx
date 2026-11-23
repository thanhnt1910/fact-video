import React from 'react';
import {Arrow, Big, C, Calc, Head, HatHero, Panel, Tag, clamp01, lerp, sp} from '../khoahoc/kit';

const AM = C.amber;
const RED = '#e0402b';
const BLUE = '#3a7be0';
const VIO = '#9b4be0';
const SKY = '#2a5fa8';
const CX = 540;

const Hero2: React.FC<{f: number; cheer?: number}> = ({f, cheer = 0}) => <HatHero x={170} y={1250} s={2} walk={f * 0.13} cheer={cheer} hat="scholar" />;

const Fx: React.FC<{x: number; y: number; size: number; color?: string; o?: number; t: string}> = ({x, y, size, color = C.cream, o = 1, t}) => {
  const parts = t.split(/\^(.)/);
  const out: React.ReactNode[] = [];
  let raised = false;
  parts.forEach((p, i) => {
    if (i % 2 === 0) {
      if (p) out.push(<tspan key={i} dy={raised ? size * 0.38 : 0}>{p}</tspan>);
      if (p) raised = false;
    } else {
      out.push(<tspan key={i} dy={-size * 0.38} fontSize={size * 0.6}>{p}</tspan>);
      raised = true;
    }
  });
  return <Big x={x} y={y} size={size} color={color} o={o}>{out}</Big>;
};
const Sun: React.FC<{x: number; y: number; r: number; f: number; color?: string}> = ({x, y, r, f, color = '#fff1d0'}) => (
  <g>
    {Array.from({length: 10}).map((_, i) => {
      const a = (i / 10) * Math.PI * 2 + f * 0.01;
      return <line key={i} x1={x + Math.cos(a) * (r + 12)} y1={y + Math.sin(a) * (r + 12)} x2={x + Math.cos(a) * (r + 32)} y2={y + Math.sin(a) * (r + 32)} stroke={color} strokeWidth={6} strokeLinecap="round" opacity={0.8} />;
    })}
    <circle cx={x} cy={y} r={r} fill={color} stroke={C.cream} strokeWidth={5} />
  </g>
);
const wave = (x0: number, x1: number, y: number, amp: number, len: number, ph: number) => {
  let d = '';
  for (let x = x0; x <= x1; x += 4) d += `${x === x0 ? 'M' : 'L'} ${x} ${y + amp * Math.sin(((x - x0) / len) * Math.PI * 2 - ph)} `;
  return d;
};
const Eye: React.FC<{x: number; y: number}> = ({x, y}) => (
  <g>
    <circle cx={x} cy={y} r={24} fill={C.cream} stroke={AM} strokeWidth={5} />
    <circle cx={x} cy={y} r={9} fill={C.ink} />
  </g>
);
const Prism: React.FC<{f: number; p?: number}> = ({f, p = 1}) => (
  <g>
    <path d="M 700 720 L 820 920 L 580 920 Z" fill="#bfe3f0" fillOpacity={0.25} stroke={C.cream} strokeWidth={6} strokeLinejoin="round" />
    <line x1={340} y1={860} x2={640} y2={830} stroke="#fff1d0" strokeWidth={9} strokeLinecap="round" />
    {[VIO, BLUE, '#3fc46a', '#e8c52b', RED].map((c, i) => (
      <line key={i} x1={770} y1={830} x2={lerp(770, 960, clamp01(p * 1.3 - i * 0.05))} y2={lerp(830, 740 + i * 50, clamp01(p * 1.3 - i * 0.05))} stroke={c} strokeWidth={9} strokeLinecap="round" />
    ))}
    <rect x={0} y={0} width={0} height={0} />
    <circle cx={0} cy={0} r={0} fill="none" />
    <g opacity={0}>{f}</g>
  </g>
);
const Dots: React.FC<{x0: number; y0: number; w: number; h: number; f: number; n?: number; color?: string}> = ({x0, y0, w, h, f, n = 40, color = C.cream}) => (
  <g>
    {Array.from({length: n}).map((_, i) => {
      const a = (i * 7919) % 1000 / 1000;
      const b = (i * 6151) % 1000 / 1000;
      return <circle key={i} cx={x0 + a * w + 3 * Math.sin(f * 0.1 + i)} cy={y0 + b * h + 3 * Math.cos(f * 0.1 + i)} r={4} fill={color} opacity={0.85} />;
    })}
  </g>
);

const P0: Panel = ({f}) => (
  <g>
    <Head a="Mặt Trời màu trắng" b="sao bầu trời lại xanh?" />
    <Sun x={440} y={820} r={90} f={f} />
    <rect x={620} y={640} width={340} height={380} rx={20} fill={SKY} stroke={C.cream} strokeWidth={5} opacity={sp(f, 4, 18)} />
    <Big x={790} y={880} size={160} color={AM} o={sp(f, 14, 28)}>?</Big>
    <Hero2 f={f} />
  </g>
);
const P1: Panel = ({f}) => {
  const k = sp(f, 4, 40);
  return (
    <g>
      <Head a="Nhưng chiều tối" b="bầu trời ấy lại đỏ rực" />
      <defs>
        <linearGradient id="txSun" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor={k > 0.5 ? '#c4584a' : SKY} />
          <stop offset="1" stopColor={k > 0.5 ? '#f0a040' : '#4a86c8'} />
        </linearGradient>
      </defs>
      <rect x={400} y={640} width={560} height={420} rx={20} fill="url(#txSun)" stroke={C.cream} strokeWidth={5} />
      <circle cx={680} cy={lerp(760, 980, k)} r={64} fill="#fff1d0" stroke={C.cream} strokeWidth={5} />
      <Hero2 f={f} />
    </g>
  );
};
const P2: Panel = ({f}) => (
  <g>
    <Head a="Cả hai chuyện" b="do một quy luật có số 4" />
    <Big x={CX + 100} y={920} size={380} color={AM} o={sp(f, 2, 20)}>4</Big>
    <Hero2 f={f} />
  </g>
);
const P3: Panel = ({f}) => (
  <g>
    <Head a="Ánh sáng trắng" b="là hỗn hợp nhiều màu" />
    <Prism f={f} p={sp(f, 6, 40)} />
    <Hero2 f={f} />
  </g>
);
const P4: Panel = ({f}) => (
  <g>
    <Head a="Mỗi màu có một bước sóng" b="độ dài một sóng ánh sáng" />
    <path d={wave(340, 940, 840, 50, 240, f * 0.12)} fill="none" stroke={RED} strokeWidth={9} />
    <g opacity={sp(f, 10, 26)}>
      <line x1={340 + 60} y1={960} x2={340 + 300} y2={960} stroke={AM} strokeWidth={6} />
      <line x1={400} y1={940} x2={400} y2={980} stroke={AM} strokeWidth={6} />
      <line x1={640} y1={940} x2={640} y2={980} stroke={AM} strokeWidth={6} />
      <Tag x={520} y={1040} color={AM} size={44}>một bước sóng</Tag>
    </g>
    <Hero2 f={f} />
  </g>
);
const P5: Panel = ({f}) => (
  <g>
    <Head a="Đỏ sóng dài" b="tím sóng ngắn" />
    <path d={wave(340, 940, 780, 45, 240, f * 0.12)} fill="none" stroke={RED} strokeWidth={9} />
    <Tag x={CX + 100} y={700} color={RED} size={44} o={sp(f, 6, 20)}>đỏ ≈ 700 nm</Tag>
    <path d={wave(340, 940, 1000, 45, 106, f * 0.2)} fill="none" stroke={VIO} strokeWidth={9} opacity={sp(f, 18, 30)} />
    <Tag x={CX + 100} y={920} color="#c08aff" size={44} o={sp(f, 22, 34)}>tím ≈ 400 nm</Tag>
    <Hero2 f={f} />
  </g>
);
const P6: Panel = ({f}) => (
  <g>
    <Head a="Không khí gồm" b="phân tử nhỏ hơn bước sóng" />
    <Dots x0={360} y0={700} w={560} h={240} f={f} n={60} />
    <path d={wave(340, 940, 1080, 40, 240, f * 0.12)} fill="none" stroke={RED} strokeWidth={8} opacity={sp(f, 14, 28)} />
    <Tag x={CX + 100} y={1000} color={C.cream} size={38} o={sp(f, 20, 34)}>chấm nhỏ xíu so với sóng</Tag>
    <Hero2 f={f} />
  </g>
);
const P7: Panel = ({f}) => {
  const p = sp(f, 4, 26);
  const q = sp(f, 24, 46);
  return (
    <g>
      <Head a="Ánh sáng bị bắn ra" b="mọi hướng: tán xạ" />
      <line x1={340} y1={860} x2={lerp(340, 640, p)} y2={860} stroke="#fff1d0" strokeWidth={9} strokeLinecap="round" />
      <circle cx={650} cy={860} r={16} fill={C.cream} stroke={AM} strokeWidth={4} />
      {Array.from({length: 8}).map((_, i) => {
        const a = (i / 8) * Math.PI * 2 + 0.3;
        return <line key={i} x1={650} y1={860} x2={650 + Math.cos(a) * 230 * q} y2={860 + Math.sin(a) * 230 * q} stroke={BLUE} strokeWidth={6} strokeLinecap="round" opacity={0.8} />;
      })}
      <Hero2 f={f} />
    </g>
  );
};
const P8: Panel = ({f}) => (
  <g>
    <Head a="Phần bắn vào mắt ta" b="thấy ở khắp bầu trời" />
    <Eye x={640} y={1060} />
    {Array.from({length: 7}).map((_, i) => {
      const a = Math.PI + 0.35 + (i / 6) * (Math.PI - 0.7);
      const sx = 640 + Math.cos(a) * 380;
      const sy = 1060 + Math.sin(a) * 380;
      const k = clamp01((f - 4 - i * 4) / 18);
      return <line key={i} x1={sx} y1={sy} x2={lerp(sx, 640, k * 0.82)} y2={lerp(sy, 1060, k * 0.82)} stroke={BLUE} strokeWidth={6} strokeLinecap="round" strokeDasharray="14 10" opacity={0.9} />;
    })}
    <Hero2 f={f} />
  </g>
);
const P9: Panel = ({f}) => (
  <g>
    <Head a="Màu sóng ngắn" b="bị bắn mạnh hơn rất nhiều" />
    <g opacity={sp(f, 2, 14)}>
      <rect x={340} y={760} width={600 * 0.15 + 600 * 0.85 * sp(f, 10, 36)} height={70} rx={14} fill={BLUE} />
      <Tag x={640} y={725} color={C.cream} size={38}>xanh, tím: sóng ngắn</Tag>
    </g>
    <g opacity={sp(f, 6, 18)}>
      <rect x={340} y={960} width={140} height={70} rx={14} fill={RED} />
      <Tag x={640} y={925} color={C.cream} size={38}>đỏ: sóng dài</Tag>
    </g>
    <Hero2 f={f} />
  </g>
);
const P10: Panel = ({f}) => (
  <g>
    <Head a="Năm" b="nhà vật lý" />
    <Big x={CX + 100} y={850} size={200} color={AM} o={sp(f, 2, 18)}>1859</Big>
    <Tag x={CX + 100} y={980} color={C.cream} size={60} o={sp(f, 14, 28)}>John Tyndall</Tag>
    <Hero2 f={f} />
  </g>
);
const P11: Panel = ({f}) => (
  <g>
    <Head a="Vài năm sau" b="huân tước" />
    <Tag x={CX + 100} y={850} color={AM} size={90} o={sp(f, 2, 18)}>Lord Rayleigh</Tag>
    <Tag x={CX + 100} y={970} color={C.cream} size={44} o={sp(f, 16, 30)}>tìm ra quy luật</Tag>
    <Hero2 f={f} />
  </g>
);
const P12: Panel = ({f}) => (
  <g>
    <Head a="Ánh sáng bị bắn" b="tỉ lệ nghịch với bước sóng" />
    <Fx x={CX + 100} y={820} size={110} color={AM} o={sp(f, 2, 18)} t="1 ÷ (bước sóng)^4" />
    <Tag x={CX + 100} y={930} color={C.cream} size={42} o={sp(f, 18, 32)}>bước sóng nhân với chính nó 4 lần</Tag>
    <Hero2 f={f} />
  </g>
);
const P13: Panel = ({f}) => (
  <g>
    <Head a="Bước sóng ngắn đi một nửa" b="bị bắn mạnh gấp 16 lần" />
    <Calc f={f} x={CX + 100} y={780} step={150} lines={[{t: '2 × 2 × 2 × 2', at: 2, size: 120}, {t: '= 16 lần', at: 22, size: 150, color: AM}]} />
    <Hero2 f={f} />
  </g>
);
const P14: Panel = ({f}) => (
  <g>
    <Head a="So tím với đỏ" />
    <Big x={CX + 100} y={850} size={150} color={C.cream} o={sp(f, 2, 18)}>700 ÷ 400</Big>
    <Hero2 f={f} />
  </g>
);
const P15: Panel = ({f}) => (
  <g>
    <Head a="Ra" />
    <Big x={CX + 100} y={850} size={190} color={AM} o={sp(f, 2, 18)}>1,75</Big>
    <Hero2 f={f} />
  </g>
);
const P16: Panel = ({f}) => (
  <g>
    <Head a="Nhân với chính nó" />
    <Calc f={f} x={CX + 100} y={780} step={150} lines={[{t: '1,75 × 1,75', at: 2, size: 120}, {t: '≈ 3,06', at: 22, size: 160, color: AM}]} />
    <Hero2 f={f} />
  </g>
);
const P17: Panel = ({f}) => (
  <g>
    <Head a="Nhân với chính nó" b="lần nữa" />
    <Calc f={f} x={CX + 100} y={780} step={150} lines={[{t: '3,06 × 3,06', at: 2, size: 120}, {t: '≈ 9,4', at: 22, size: 170, color: AM}]} />
    <Hero2 f={f} />
  </g>
);
const P18: Panel = ({f}) => (
  <g>
    <Head a="Tím bị bắn mạnh" b="gần gấp 10 lần đỏ" />
    <rect x={340} y={780} width={60} height={70} rx={10} fill={RED} />
    <rect x={340} y={900} width={60 + 540 * sp(f, 6, 40)} height={70} rx={10} fill={VIO} />
    <Tag x={CX + 100} y={750} color={RED} size={36}>đỏ</Tag>
    <Tag x={CX + 100} y={1020} color="#c08aff" size={36}>tím ≈ 9,4 lần</Tag>
    <Hero2 f={f} />
  </g>
);
const P19: Panel = ({f}) => (
  <g>
    <Head a="Vậy sao bầu trời" b="không màu tím?" />
    <circle cx={CX + 100} cy={850} r={150} fill={VIO} opacity={0.7} stroke={C.cream} strokeWidth={6} />
    <Big x={CX + 100} y={910} size={200} color={C.cream} o={sp(f, 6, 22)}>?</Big>
    <Hero2 f={f} />
  </g>
);
const P20: Panel = ({f}) => (
  <g>
    <Head a="Mặt Trời ít tím hơn xanh" b="mắt kém nhạy với tím" />
    <Sun x={470} y={820} r={60} f={f} />
    <Tag x={470} y={960} color={C.cream} size={40} o={sp(f, 4, 18)}>ít tím hơn xanh</Tag>
    <Eye x={820} y={820} />
    <Tag x={820} y={960} color={C.cream} size={40} o={sp(f, 18, 32)}>kém nhạy với tím</Tag>
    <Hero2 f={f} />
  </g>
);
const P21: Panel = ({f}) => (
  <g>
    <Head a="Cộng lại" b="màu xanh thắng" />
    <rect x={400} y={680} width={540} height={340} rx={24} fill={SKY} stroke={C.cream} strokeWidth={6} />
    <Big x={CX + 130} y={890} size={150} color={C.cream} o={sp(f, 4, 20)}>XANH</Big>
    <Hero2 f={f} />
  </g>
);
const P22: Panel = ({f}) => {
  const k = sp(f, 4, 40);
  return (
    <g>
      <Head a="Lúc hoàng hôn" b="Mặt Trời thấp sát chân trời" />
      <rect x={340} y={680} width={600} height={400} rx={20} fill="#c4584a" opacity={0.55} stroke={C.cream} strokeWidth={5} />
      <line x1={340} y1={980} x2={940} y2={980} stroke={C.cream} strokeWidth={6} />
      <circle cx={700} cy={lerp(800, 960, k)} r={70} fill="#f0a040" stroke={C.cream} strokeWidth={5} />
      <rect x={340} y={980} width={600} height={100} fill="#14181f" opacity={0.85} />
      <Hero2 f={f} />
    </g>
  );
};
const P23: Panel = ({f}) => (
  <g>
    <Head a="Ánh sáng đi qua" b="lớp không khí dày hơn" />
    <path d="M 340 1060 Q 640 900 940 1060" fill="none" stroke={C.cream} strokeWidth={5} />
    <path d="M 340 1000 Q 640 840 940 1000" fill="none" stroke={BLUE} strokeWidth={5} strokeDasharray="12 10" opacity={0.8} />
    <line x1={640} y1={700} x2={640} y2={lerp(700, 905, sp(f, 4, 20))} stroke="#fff1d0" strokeWidth={8} strokeLinecap="round" />
    <line x1={420} y1={lerp(700, 1012, 0)} x2={lerp(420, 640, 0)} y2={1012} stroke="none" />
    <line x1={460} y1={lerp(980, 960, sp(f, 20, 50))} x2={lerp(460, 900, sp(f, 20, 50))} y2={lerp(980, 1020, sp(f, 20, 50))} stroke="#f0a040" strokeWidth={8} strokeLinecap="round" />
    <Tag x={760} y={760} color={C.cream} size={36} o={sp(f, 10, 24)}>đường ngắn</Tag>
    <Tag x={700} y={1130} color={AM} size={38} o={sp(f, 36, 50)}>đường dài hơn nhiều</Tag>
    <Hero2 f={f} />
  </g>
);
const P24: Panel = ({f}) => {
  const k = sp(f, 4, 50);
  return (
    <g>
      <Head a="Màu xanh bị bắn ra" b="gần hết" />
      <defs>
        <linearGradient id="txRay" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0" stopColor="#fff1d0" />
          <stop offset="1" stopColor="#e0602b" />
        </linearGradient>
      </defs>
      <line x1={340} y1={860} x2={lerp(340, 940, k)} y2={860} stroke="url(#txRay)" strokeWidth={14} strokeLinecap="round" />
      {Array.from({length: 8}).map((_, i) => {
        const x = 400 + i * 70;
        const o = clamp01((k * 600 + 340 - x) / 40) * (1 - clamp01((f - 20 - i * 3) / 20));
        return <line key={i} x1={x} y1={860} x2={x + 10 + 30 * (i % 3)} y2={860 - 110 - 15 * (i % 2)} stroke={BLUE} strokeWidth={7} strokeLinecap="round" opacity={o} />;
      })}
      <Hero2 f={f} />
    </g>
  );
};
const P25: Panel = ({f}) => (
  <g>
    <Head a="Chỉ còn đỏ, cam, vàng" b="tới mắt ta" />
    <line x1={340} y1={860} x2={800} y2={860} stroke="#e0602b" strokeWidth={14} strokeLinecap="round" />
    <Eye x={860} y={860} />
    {[RED, '#f08a3a', '#e8c52b'].map((c, i) => <circle key={i} cx={500 + i * 90} cy={960} r={30} fill={c} stroke={C.cream} strokeWidth={4} opacity={sp(f, 4 + i * 6, 16 + i * 6)} />)}
    <Hero2 f={f} />
  </g>
);
const P26: Panel = ({f}) => (
  <g>
    <Head a="Mây trắng vì" b="giọt nước rất lớn" />
    <g opacity={sp(f, 2, 16)}>
      <circle cx={560} cy={820} r={80} fill={C.cream} />
      <circle cx={660} cy={780} r={100} fill={C.cream} />
      <circle cx={780} cy={830} r={80} fill={C.cream} />
      <rect x={560} y={820} width={300} height={90} rx={40} fill={C.cream} />
    </g>
    <Tag x={CX + 150} y={1010} color={AM} size={42} o={sp(f, 16, 30)}>bắn mọi màu đều nhau</Tag>
    <Hero2 f={f} />
  </g>
);
const P27: Panel = ({f}) => (
  <g>
    <Head a="Bầu trời xanh" b="hoàng hôn đỏ" />
    <rect x={340} y={680} width={300} height={360} rx={20} fill={SKY} stroke={C.cream} strokeWidth={5} />
    <rect x={640} y={680} width={300} height={360} rx={20} fill="#c4584a" stroke={C.cream} strokeWidth={5} />
    <Tag x={CX + 100} y={1110} color={AM} size={50} o={sp(f, 10, 26)}>cùng một quy luật</Tag>
    <Hero2 f={f} cheer={sp(f, 10, 28)} />
  </g>
);

export const PANELS: Panel[] = [P0, P1, P2, P3, P4, P5, P6, P7, P8, P9, P10, P11, P12, P13, P14, P15, P16, P17, P18, P19, P20, P21, P22, P23, P24, P25, P26, P27];
