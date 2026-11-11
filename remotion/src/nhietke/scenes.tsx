import React from 'react';
import {Arrow, Bar, Big, C, Calc, Dash, Head, HatHero, Lab, Panel, Tag, clamp01, lerp, seg, sp} from '../khoahoc/kit';

const RED = '#e0613b';
const ICE = '#8fd1ff';

/** Nhiệt kế: bầu ở (x, y), ống cao h phía trên; level 0..1; ticks: số vạch; labels: chữ ở vài vạch */
const Th: React.FC<{x: number; y: number; h?: number; level: number; ticks?: number; labels?: {at: number; t: string; c?: string}[]; o?: number; color?: string; irregular?: boolean}> = ({x, y, h = 420, level, ticks = 0, labels = [], o = 1, color = RED, irregular = false}) => (
  <g opacity={clamp01(o)}>
    <rect x={x - 20} y={y - h} width={40} height={h} rx={20} fill="#0d1c20" stroke={C.cream} strokeWidth={6} />
    <circle cx={x} cy={y + 12} r={42} fill={color} stroke={C.cream} strokeWidth={6} />
    <rect x={x - 11} y={y - h * clamp01(level)} width={22} height={h * clamp01(level) + 10} rx={11} fill={color} />
    {Array.from({length: ticks}, (_, i) => {
      const u = irregular ? [0.05, 0.22, 0.3, 0.62, 0.7, 0.93][i % 6] : (i + 1) / (ticks + 1);
      return <line key={i} x1={x + 24} y1={y - (h - 16) * u - 8} x2={x + 46} y2={y - (h - 16) * u - 8} stroke={C.cream} strokeWidth={4} />;
    })}
    {labels.map((l, i) => (
      <Lab key={i} x={x + 62} y={y - (h - 16) * l.at - 8 + 14} anchor="start" size={38} color={l.c ?? C.cream}>
        {l.t}
      </Lab>
    ))}
  </g>
);

// --- Cảnh 1 ---
const P0: Panel = ({f}) => (
  <g>
    <Head a="Hôm nay nóng bao nhiêu độ?" b="ngày xưa 2 người đo ra 2 số khác nhau" />
    <HatHero x={250} y={1230} s={2} walk={f * 0.2} hat="goggles" />
    <HatHero x={830} y={1230} s={2} walk={f * 0.2 + 1} hat="goggles" />
    <Th x={380} y={1000} h={380} level={0.35 + 0.3 * sp(f, 8, 30)} o={sp(f, 4, 14)} />
    <Th x={700} y={1000} h={380} level={0.7 * sp(f, 8, 30) + 0.1} o={sp(f, 4, 14)} />
    <Big x={540} y={760} size={140} color={C.amber} o={0.9 * sp(f, 36, 52)}>≠</Big>
  </g>
);
const P1: Panel = ({f}) => (
  <g>
    <Head a="Vì sao một cái nhiệt kế" b="lại có thể nói sai?" />
    <Th x={540} y={1100} h={460} level={0.55} ticks={6} irregular />
    <Big x={820} y={760} size={170} color={C.amber} o={0.9 * sp(f, 14, 30)}>?</Big>
  </g>
);
const P2: Panel = ({f}) => (
  <g>
    <Head a="Nhiệt kế đã có từ lâu" b="nhưng vạch chia theo ý riêng" />
    <Th x={250} y={1080} h={420} level={0.5} ticks={4} o={sp(f, 6, 20)} />
    <Th x={540} y={1080} h={420} level={0.5} ticks={9} o={sp(f, 16, 30)} />
    <Th x={830} y={1080} h={420} level={0.5} ticks={6} irregular o={sp(f, 26, 40)} />
    <Tag x={540} y={1230} color={C.amber} size={42} o={sp(f, 40, 54)}>mỗi người một kiểu</Tag>
  </g>
);
const P3: Panel = ({f}) => (
  <g>
    <Head a="Có người chọn lúc bơ tan" b="người chọn than cháy, ngày lạnh nhất" />
    <g opacity={sp(f, 8, 22)}>
      <rect x={110} y={760} width={220} height={120} rx={14} fill="#f2d675" stroke={C.cream} strokeWidth={5} />
      <path d="M 110 880 Q 220 930 330 880" fill="#f2d675" />
      <Tag x={220} y={960} color={C.cream} size={36}>bơ tan</Tag>
    </g>
    <g opacity={sp(f, 26, 40)}>
      <circle cx={540} cy={830} r={70} fill="#3a2a22" stroke={C.cream} strokeWidth={5} />
      <circle cx={520} cy={810} r={26} fill="#e0613b" />
      <circle cx={566} cy={846} r={20} fill="#f2b35a" />
      <Tag x={540} y={960} color={C.cream} size={36}>than cháy</Tag>
    </g>
    <g opacity={sp(f, 44, 58)}>
      <path d="M 700 900 L 800 740 L 900 900 Z" fill="#dfe8f2" stroke={C.cream} strokeWidth={5} />
      <Tag x={800} y={960} color={C.cream} size={36}>ngày lạnh nhất</Tag>
    </g>
  </g>
);

// --- Cảnh 2 ---
const P4: Panel = ({f}) => {
  const flame = Math.sin(f * 0.4) * 6;
  return (
    <g>
      <Head a="Nhiệt kế chạy nhờ" b="chất lỏng nở ra khi nóng" />
      <Th x={540} y={1000} h={440} level={0.2 + 0.6 * seg(f, 10, 80)} />
      <path d={`M 540 1130 Q ${515 + flame} 1090 540 1065 Q ${565 - flame} 1090 540 1130 Z`} fill="#f2b35a" stroke={C.cream} strokeWidth={4} />
      <Arrow x1={720} y1={760} x2={720} y2={600} p={sp(f, 40, 70)} />
      <Tag x={820} y={700} color={C.amber} size={38} o={sp(f, 50, 66)}>dâng cao</Tag>
    </g>
  );
};
const P5: Panel = ({f}) => (
  <g>
    <Head a="Giống cột nước trong ống nhỏ" b="ấm lên thì dâng, lạnh đi thì tụt" />
    <Th x={540} y={1050} h={460} level={0.45 + 0.35 * Math.sin(f * 0.07)} color="#3fa0d6" />
    <Tag x={800} y={780} color={C.amber} size={40} o={0.5 + 0.5 * Math.max(0, Math.sin(f * 0.07))}>ấm: dâng</Tag>
    <Tag x={800} y={1020} color={ICE} size={40} o={0.5 + 0.5 * Math.max(0, -Math.sin(f * 0.07))}>lạnh: tụt</Tag>
  </g>
);
const P6: Panel = ({f}) => (
  <g>
    <Head a="Dâng tới đâu thì gọi là" b="bao nhiêu độ?" />
    <Th x={400} y={1100} h={460} level={0.6} />
    <Arrow x1={620} y1={760} x2={470} y2={760} p={sp(f, 8, 30)} />
    <Big x={730} y={800} size={190} color={C.amber} o={0.9 * sp(f, 20, 38)}>?</Big>
    <Tag x={540} y={1260} color={C.cream} size={38} o={sp(f, 40, 56)}>không có mốc chung thì số vô nghĩa</Tag>
  </g>
);
const P7: Panel = ({f}) => (
  <g>
    <Head a="Vậy cần 2 mốc" b="mà ai cũng làm lại được" />
    <Th x={440} y={1100} h={460} level={0.55} />
    {[0.08, 0.92].map((u, i) => (
      <g key={i} opacity={sp(f, 10 + i * 20, 26 + i * 20)}>
        <line x1={380} y1={1100 - 444 * u - 8} x2={620} y2={1100 - 444 * u - 8} stroke={C.amber} strokeWidth={6} strokeDasharray="12 8" />
        <Lab x={640} y={1100 - 444 * u + 8} anchor="start" size={46} color={C.amber}>{i ? 'mốc 2' : 'mốc 1'}</Lab>
      </g>
    ))}
  </g>
);

// --- Cảnh 3 ---
const P8: Panel = ({f}) => (
  <g>
    <Head a="Năm 1714, Pha-ren-hai" b="28 tuổi, làm 2 nhiệt kế cùng số đo" />
    <Th x={300} y={1080} h={420} level={0.6 * sp(f, 8, 30)} ticks={9} o={sp(f, 4, 14)} />
    <Th x={560} y={1080} h={420} level={0.6 * sp(f, 8, 30)} ticks={9} o={sp(f, 4, 14)} />
    <Big x={880} y={800} size={110} color={C.amber} o={sp(f, 20, 36)}>1714</Big>
    <HatHero x={880} y={1230} s={2} walk={f * 0.2} hat="goggles" />
  </g>
);
const P9: Panel = ({f}) => (
  <g>
    <Head a="Bí quyết: dùng những" b="mốc cố định, không tùy ý" />
    <Th x={440} y={1100} h={460} level={0.55} ticks={9} />
    <g opacity={sp(f, 12, 28)}>
      <circle cx={760} cy={800} r={90} fill="#2c4a4a" stroke={C.cream} strokeWidth={6} />
      <path d="M 720 800 L 750 835 L 805 770" fill="none" stroke="#6fd18f" strokeWidth={14} strokeLinecap="round" strokeLinejoin="round" />
    </g>
    <Tag x={760} y={950} color={C.amber} size={42} o={sp(f, 30, 46)}>ai làm cũng ra</Tag>
  </g>
);
const P10: Panel = ({f}) => (
  <g>
    <Head a="Thang của ông: nước đóng băng 32°" b="nước sôi 212°" />
    <Th x={400} y={1150} h={620} level={sp(f, 8, 60)} ticks={0} labels={[{at: 0.12, t: '32° nước đóng băng', c: ICE}, {at: 0.92, t: '212° nước sôi', c: C.amber}]} />
  </g>
);
const P11: Panel = ({f}) => (
  <g>
    <Head a="Hai mốc ấy cách nhau" />
    <Calc f={f} y={720} lines={[{t: '212 − 32', at: 6}, {t: '= 180 độ', at: 26, color: C.amber, size: 120}]} />
  </g>
);

// --- Cảnh 4 ---
const P12: Panel = ({f}) => (
  <g>
    <Head a="Năm 1742, Xen-xi-út" b="cũng chọn nước đá và nước sôi" />
    <Th x={400} y={1120} h={560} level={sp(f, 8, 50)} labels={[{at: 0.12, t: 'nước đá', c: ICE}, {at: 0.92, t: 'nước sôi', c: C.amber}]} />
    <Big x={830} y={780} size={110} color={C.amber} o={sp(f, 20, 36)}>1742</Big>
  </g>
);
const P13: Panel = ({f}) => (
  <g>
    <Head a="Nhưng ông chia khoảng giữa" b="thành 100 phần, không phải 180" />
    {[100, 180].map((n, i) => (
      <g key={n} opacity={sp(f, 6 + i * 22, 20 + i * 22)}>
        <rect x={110} y={720 + i * 200} width={860} height={70} rx={12} fill="#1d3a3a" stroke={C.cream} strokeWidth={5} />
        {Array.from({length: n / 5 + 1}, (_, k) => <line key={k} x1={110 + (k * 860) / (n / 5)} y1={720 + i * 200} x2={110 + (k * 860) / (n / 5)} y2={760 + i * 200} stroke={C.cream} strokeWidth={2} />)}
        <Big x={540} y={700 + i * 200} size={70} color={i ? C.dim : C.amber}>{n + ' phần'}</Big>
      </g>
    ))}
  </g>
);
const P14: Panel = ({f}) => (
  <g>
    <Head a="Thang đầu tiên của ông bị ngược" b="sôi là 0°, đóng băng là 100°" />
    <Th x={400} y={1150} h={620} level={0.9} labels={[{at: 0.12, t: '100° nước đóng băng', c: ICE}, {at: 0.92, t: '0° nước sôi', c: C.amber}]} o={sp(f, 6, 20)} />
  </g>
);
const P15: Panel = ({f}) => {
  const k = seg(f, 20, 60);
  const up = k < 0.5;
  return (
    <g>
      <Head a="Về sau người ta lật lại" b="nay đóng băng 0°, sôi 100°" />
      <g transform={`translate(400 800) scale(${Math.cos(k * Math.PI)} 1) translate(-400 -800)`}>
        <Th x={400} y={1150} h={620} level={0.9} labels={up ? [{at: 0.12, t: '100°', c: ICE}, {at: 0.92, t: '0°', c: C.amber}] : []} />
      </g>
      {!up && <Th x={400} y={1150} h={620} level={0.9} labels={[{at: 0.12, t: '0° nước đóng băng', c: ICE}, {at: 0.92, t: '100° nước sôi', c: C.amber}]} o={sp(f, 60, 74)} />}
      <Arrow x1={700} y1={900} x2={700} y2={760} p={sp(f, 16, 40)} />
    </g>
  );
};
const P16: Panel = ({f}) => (
  <g>
    <Head a="Nước sôi còn khác nhau" b="tùy áp suất không khí" />
    <rect x={300} y={900} width={480} height={240} rx={30} fill="#6a7686" stroke={C.cream} strokeWidth={6} />
    <path d="M 300 900 L 780 900" stroke={C.cream} strokeWidth={8} />
    {Array.from({length: 7}, (_, i) => <circle key={i} cx={360 + i * 60} cy={1090 - ((f * (1 + i * 0.3) + i * 20) % 120)} r={10} fill={ICE} opacity={0.7} />)}
    {[400, 540, 680].map((x) => <Arrow key={x} x1={x} y1={640} x2={x} y2={lerp(640, 840, sp(f, 10, 40))} p={sp(f, 10, 30)} color={C.cream} w={6} />)}
    <Tag x={540} y={1240} color={C.amber} size={42} o={sp(f, 40, 56)}>đo ở áp suất nhất định</Tag>
  </g>
);

// --- Cảnh 5 ---
const P17: Panel = ({f}) => (
  <g>
    <Head a="Giờ có 2 thang" b="làm sao đổi qua lại?" />
    <Th x={300} y={1150} h={560} level={0.5} labels={[{at: 0.12, t: '0° C'}, {at: 0.92, t: '100° C'}]} />
    <Th x={700} y={1150} h={560} level={0.5} labels={[{at: 0.12, t: '32° F'}, {at: 0.92, t: '212° F'}]} />
    <Arrow x1={440} y1={800} x2={610} y2={800} p={sp(f, 20, 44)} />
    <Arrow x1={610} y1={880} x2={440} y2={880} p={sp(f, 30, 54)} />
  </g>
);
const P18: Panel = ({f}) => (
  <g>
    <Head a="So hai khoảng giữa hai mốc" />
    <Calc f={f} y={720} lines={[{t: '180 ÷ 100', at: 6}, {t: '= 1,8', at: 26, color: C.amber, size: 130}]} />
  </g>
);
const P19: Panel = ({f}) => (
  <g>
    <Head a="Vậy 1 độ C dài bằng" b="1,8 độ F" />
    <Bar x={110} y={720} w={400} color={ICE} p={sp(f, 6, 24)} label="1 độ C" />
    <Bar x={110} y={850} w={400} color={RED} p={sp(f, 18, 36)} h={56} />
    <rect x={110} y={850} width={400 * 1.8} height={56} rx={10} fill="none" stroke={C.cream} strokeWidth={4} opacity={0} />
    <Bar x={110} y={850} w={720} color={RED} p={sp(f, 18, 40)} label="1,8 độ F" />
  </g>
);
const P20: Panel = ({f}) => (
  <g>
    <Head a="Số 1,8 ấy" b="chính là 9/5" />
    <Big x={540} y={780} size={150} color={C.cream} o={sp(f, 6, 20)}>1,8</Big>
    <Big x={540} y={930} size={130} color={C.amber} o={sp(f, 24, 40)}>= 9/5</Big>
  </g>
);
const P21: Panel = ({f}) => (
  <g>
    <Head a="Vậy công thức đổi là" />
    <Lab x={540} y={640} size={52} color={C.cream} o={sp(f, 6, 18)}>độ F</Lab>
    <Big x={540} y={780} size={96} color={C.amber} o={sp(f, 16, 30)}>= độ C × 9 ÷ 5 + 32</Big>
    <HatHero x={200} y={1250} s={2} walk={f * 0.25} hat="goggles" cheer={sp(f, 40, 60)} />
  </g>
);
const P22: Panel = ({f}) => (
  <g>
    <Head a="Cộng 32 vì thang Pha-ren-hai" b="bắt đầu thấp hơn: nước đá là 32°" />
    <Th x={300} y={1150} h={540} level={0.1} labels={[{at: 0.1, t: '0° C', c: ICE}]} />
    <Th x={700} y={1150} h={540} level={0.1} labels={[{at: 0.1, t: '32° F', c: ICE}]} />
    <Dash x1={450} y1={1150 - 54 - 8} x2={640} y2={1150 - 54 - 8} p={sp(f, 20, 50)} color={C.amber} />
  </g>
);

// --- Cảnh 6 ---
const P23: Panel = ({f}) => (
  <g>
    <Head a="Ví dụ, một ngày 25 độ C" b="đổi sang độ F thì là bao nhiêu?" />
    <Th x={540} y={1150} h={560} level={0.25 + 0.0 * f} labels={[{at: 0.25, t: '25° C', c: C.amber}]} />
    <Big x={830} y={800} size={120} color={C.amber} o={0.9 * sp(f, 16, 32)}>?</Big>
  </g>
);
const P24: Panel = ({f}) => (
  <g>
    <Head a="Nhân với 9" />
    <Calc f={f} y={720} lines={[{t: '25 × 9', at: 6}, {t: '= 225', at: 24, color: C.amber, size: 130}]} />
  </g>
);
const P25: Panel = ({f}) => (
  <g>
    <Head a="Rồi chia cho 5" />
    <Calc f={f} y={720} lines={[{t: '225 ÷ 5', at: 6}, {t: '= 45', at: 24, color: C.amber, size: 130}]} />
  </g>
);
const P26: Panel = ({f}) => (
  <g>
    <Head a="Cộng 32" b="được 77 độ F" />
    <Calc f={f} y={720} lines={[{t: '45 + 32', at: 6}, {t: '= 77 °F', at: 24, color: C.amber, size: 130}]} />
    <Th x={880} y={1150} h={400} level={0.45} o={0.0} />
  </g>
);

// --- Cảnh 7 ---
const P27: Panel = ({f}) => (
  <g>
    <Head a="Hai người đo ra 2 số khác nhau" b="vì thiếu mốc chung" />
    <HatHero x={250} y={1230} s={2} walk={f * 0.2} hat="goggles" />
    <HatHero x={830} y={1230} s={2} walk={f * 0.2 + 1} hat="goggles" />
    <Th x={380} y={1000} h={380} level={0.4} ticks={6} irregular />
    <Th x={700} y={1000} h={380} level={0.7} ticks={3} irregular />
    <Big x={540} y={760} size={140} color={C.amber} o={0.9 * sp(f, 20, 36)}>≠</Big>
  </g>
);
const P28: Panel = ({f}) => (
  <g>
    <Head a="Có 2 mốc chung" b="mọi nhiệt kế nói cùng một điều" />
    {[220, 540, 860].map((x, i) => (
      <Th key={x} x={x} y={1100} h={440} level={0.55} ticks={9} o={sp(f, 6 + i * 12, 20 + i * 12)} labels={[]} />
    ))}
    <Dash x1={150} y1={1100 - 0.55 * 440 - 8} x2={930} y2={1100 - 0.55 * 440 - 8} p={sp(f, 40, 70)} color={C.amber} />
    <HatHero x={540} y={1260} s={1.0} walk={f * 0.2} hat="goggles" cheer={sp(f, 50, 70)} />
  </g>
);

export const PANELS: Panel[] = [P0, P1, P2, P3, P4, P5, P6, P7, P8, P9, P10, P11, P12, P13, P14, P15, P16, P17, P18, P19, P20, P21, P22, P23, P24, P25, P26, P27, P28];
