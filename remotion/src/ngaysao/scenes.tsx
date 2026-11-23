import React from 'react';
import {Arrow, Big, C, Calc, Head, HatHero, Panel, Tag, clamp01, lerp, sp} from '../khoahoc/kit';

const AM = C.amber;
const RED = '#e0613b';
const BLUE = '#3a7be0';
const CX = 540;

const Hero2: React.FC<{f: number; cheer?: number}> = ({f, cheer = 0}) => <HatHero x={170} y={1250} s={2} walk={f * 0.13} cheer={cheer} hat="goggles" />;

const Earth: React.FC<{x: number; y: number; r: number; rot: number; flag?: boolean}> = ({x, y, r, rot, flag = true}) => {
  const a = ((rot - 90) * Math.PI) / 180;
  return (
    <g>
      <circle cx={x} cy={y} r={r} fill="#2f6f96" fillOpacity={0.55} stroke={C.cream} strokeWidth={5} />
      <path d={`M ${x - r * 0.4} ${y - r * 0.3} q ${r * 0.3} ${-r * 0.3} ${r * 0.5} 0 q ${r * 0.1} ${r * 0.5} ${-r * 0.3} ${r * 0.6} q ${-r * 0.3} ${-r * 0.2} ${-r * 0.2} ${-r * 0.6} Z`} fill="#4a9a5a" opacity={0.6} />
      {flag && (
        <g>
          <line x1={x} y1={y} x2={x + Math.cos(a) * r} y2={y + Math.sin(a) * r} stroke={AM} strokeWidth={5} />
          <circle cx={x + Math.cos(a) * r} cy={y + Math.sin(a) * r} r={13} fill={AM} stroke={C.cream} strokeWidth={4} />
        </g>
      )}
    </g>
  );
};
const Clock: React.FC<{x: number; y: number; r: number; hr: number; mn: number}> = ({x, y, r, hr, mn}) => {
  const hand = (deg: number, len: number, w: number, col: string) => {
    const a = ((deg - 90) * Math.PI) / 180;
    return <line x1={x} y1={y} x2={x + Math.cos(a) * len} y2={y + Math.sin(a) * len} stroke={col} strokeWidth={w} strokeLinecap="round" />;
  };
  return (
    <g>
      <circle cx={x} cy={y} r={r} fill="#1d2236" stroke={C.cream} strokeWidth={6} />
      {Array.from({length: 12}).map((_, i) => {
        const a = (i / 12) * Math.PI * 2;
        return <line key={i} x1={x + Math.sin(a) * r * 0.86} y1={y - Math.cos(a) * r * 0.86} x2={x + Math.sin(a) * r * 0.95} y2={y - Math.cos(a) * r * 0.95} stroke={C.cream} strokeWidth={4} />;
      })}
      {hand(hr, r * 0.5, 10, AM)}
      {hand(mn, r * 0.78, 6, C.cream)}
      <circle cx={x} cy={y} r={9} fill={C.cream} />
    </g>
  );
};
const Sun: React.FC<{x: number; y: number; r: number; f: number}> = ({x, y, r, f}) => (
  <g>
    {Array.from({length: 10}).map((_, i) => {
      const a = (i / 10) * Math.PI * 2 + f * 0.01;
      return <line key={i} x1={x + Math.cos(a) * (r + 10)} y1={y + Math.sin(a) * (r + 10)} x2={x + Math.cos(a) * (r + 28)} y2={y + Math.sin(a) * (r + 28)} stroke={AM} strokeWidth={6} strokeLinecap="round" />;
    })}
    <circle cx={x} cy={y} r={r} fill="#f0a040" stroke={C.cream} strokeWidth={5} />
  </g>
);
const StarI: React.FC<{x: number; y: number; r: number; f: number}> = ({x, y, r, f}) => (
  <g>
    <circle cx={x} cy={y} r={r * 1.8 + 3 * Math.sin(f * 0.1)} fill="#8fb8ff" opacity={0.15} />
    <circle cx={x} cy={y} r={r} fill="#cfe0ff" stroke={C.cream} strokeWidth={5} />
  </g>
);

const P0: Panel = ({f}) => (
  <g>
    <Head a="Trái Đất quay đúng một vòng" b="có phải 24 giờ?" />
    <Earth x={CX + 100} y={850} r={150} rot={f * 3} />
    <Big x={CX + 100} y={1130} size={120} color={AM} o={sp(f, 8, 24)}>24 giờ?</Big>
    <Hero2 f={f} />
  </g>
);
const P1: Panel = ({f}) => (
  <g>
    <Head a="Nhưng thật ra" b="nó quay xong sớm hơn" />
    <Big x={CX + 100} y={880} size={190} color={AM} o={sp(f, 2, 18)}>− 4 phút</Big>
    <Hero2 f={f} />
  </g>
);
const P2: Panel = ({f}) => (
  <g>
    <Head a="Bốn phút ấy" b="từ đâu ra?" />
    <Clock x={CX - 10} y={860} r={150} hr={0} mn={f * 6} />
    <Big x={CX + 360} y={920} size={260} color={AM} o={sp(f, 8, 24)}>?</Big>
    <Hero2 f={f} />
  </g>
);
const P3: Panel = ({f}) => (
  <g>
    <Head a="Có hai cách đo" b="một ngày" />
    <Sun x={470} y={820} r={70} f={f} />
    <Tag x={470} y={980} color={C.cream} size={42} o={sp(f, 6, 20)}>nhìn Mặt Trời</Tag>
    <StarI x={830} y={820} r={34} f={f} />
    <Tag x={830} y={980} color={C.cream} size={42} o={sp(f, 16, 30)}>nhìn một ngôi sao</Tag>
    <Hero2 f={f} />
  </g>
);
const P4: Panel = ({f}) => (
  <g>
    <Head a="Từ lúc Mặt Trời giữa trời" b="tới giữa trời hôm sau" />
    <Sun x={470} y={800} r={55} f={f} />
    <line x1={470} y1={880} x2={470} y2={1020} stroke={C.cream} strokeWidth={5} strokeDasharray="10 8" />
    <Tag x={470} y={1070} color={C.cream} size={38}>hôm nay</Tag>
    <Arrow x1={560} y1={800} x2={740} y2={800} color={AM} p={sp(f, 10, 36)} />
    <g opacity={sp(f, 30, 44)}>
      <Sun x={830} y={800} r={55} f={f} />
      <line x1={830} y1={880} x2={830} y2={1020} stroke={C.cream} strokeWidth={5} strokeDasharray="10 8" />
      <Tag x={830} y={1070} color={C.cream} size={38}>hôm sau</Tag>
    </g>
    <Hero2 f={f} />
  </g>
);
const P5: Panel = ({f}) => (
  <g>
    <Head a="Trung bình" b="đồng hồ dùng con số này" />
    <Big x={CX + 100} y={820} size={190} color={AM} o={sp(f, 2, 18)}>24 giờ</Big>
    <Clock x={CX + 100} y={1060} r={110} hr={0} mn={0} />
    <Hero2 f={f} />
  </g>
);
const P6: Panel = ({f}) => (
  <g>
    <Head a="Cách hai" b="nhìn một ngôi sao rất xa" />
    <StarI x={CX + 100} y={820} r={50} f={f} />
    <Hero2 f={f} />
  </g>
);
const P7: Panel = ({f}) => (
  <g>
    <Head a="Đo tới lúc sao" b="trở lại đúng chỗ cũ" />
    <StarI x={900} y={700} r={30} f={f} />
    <line x1={560} y1={900} x2={900} y2={700} stroke={C.cream} strokeWidth={3} strokeDasharray="10 8" opacity={0.7} />
    <Earth x={560} y={900} r={110} rot={60 + 360 * sp(f, 8, 70)} />
    <Tag x={CX + 100} y={1100} color={AM} size={42} o={sp(f, 50, 66)}>về đúng chỗ cũ</Tag>
    <Hero2 f={f} />
  </g>
);
const P8: Panel = ({f}) => (
  <g>
    <Head a="Sao rất xa" b="hướng không đổi" />
    <StarI x={920} y={700} r={30} f={f} />
    <line x1={500} y1={900} x2={920} y2={700} stroke={C.cream} strokeWidth={3} strokeDasharray="10 8" opacity={0.7} />
    <line x1={500} y1={1040} x2={920} y2={720} stroke={C.cream} strokeWidth={3} strokeDasharray="10 8" opacity={0.7} />
    <Earth x={500} y={940} r={100} rot={f * 3} />
    <Tag x={CX + 100} y={1130} color={AM} size={42} o={sp(f, 14, 28)}>một vòng quay thật</Tag>
    <Hero2 f={f} />
  </g>
);
const P9: Panel = ({f}) => (
  <g>
    <Head a="Kết quả" />
    <Big x={CX + 100} y={860} size={120} color={AM} o={sp(f, 2, 18)}>23 giờ 56 phút</Big>
    <Hero2 f={f} />
  </g>
);
const P10: Panel = ({f}) => (
  <g>
    <Head a="Hai cách đo lệch nhau" />
    <Calc f={f} x={CX + 100} y={780} step={150} lines={[{t: '24 giờ − 23 giờ 56 phút', at: 2, size: 80}, {t: '= 4 phút', at: 22, size: 160, color: AM}]} />
    <Hero2 f={f} />
  </g>
);
const P11: Panel = ({f}) => {
  const a = f * 0.03 + 3.2;
  const ex = 640 + 260 * Math.cos(a);
  const ey = 860 + 150 * Math.sin(a);
  return (
    <g>
      <Head a="Trái Đất vừa quay quanh mình" b="vừa đi quanh Mặt Trời" />
      <ellipse cx={640} cy={860} rx={260} ry={150} fill="none" stroke={C.cream} strokeWidth={3} strokeDasharray="10 8" opacity={0.7} />
      <Sun x={640} y={860} r={44} f={f} />
      <Earth x={ex} y={ey} r={46} rot={f * 8} />
      <Tag x={640} y={1090} color={C.cream} size={38} o={sp(f, 10, 24)}>quay quanh mình và quanh Mặt Trời</Tag>
      <Hero2 f={f} />
    </g>
  );
};
const P12: Panel = ({f}) => (
  <g>
    <Head a="Kim giờ và kim phút" b="gặp nhau lúc 12 giờ" />
    <Clock x={CX + 100} y={880} r={190} hr={0} mn={0} />
    <Hero2 f={f} />
  </g>
);
const P13: Panel = ({f}) => {
  const k = sp(f, 4, 56);
  return (
    <g>
      <Head a="Kim phút đi hết 60 phút" b="kim giờ đã nhích đi" />
      <Clock x={CX + 100} y={880} r={190} hr={30 * k} mn={360 * k} />
      <Tag x={CX + 100} y={1130} color={AM} size={40} o={sp(f, 40, 56)}>kim giờ đã nhích</Tag>
      <Hero2 f={f} />
    </g>
  );
};
const P14: Panel = ({f}) => {
  const k = sp(f, 4, 50);
  return (
    <g>
      <Head a="Kim phút đi thêm" b="mới đuổi kịp kim giờ" />
      <Clock x={CX + 100} y={880} r={190} hr={30 + 2.7 * k} mn={360 + 32.7 * k} />
      <Hero2 f={f} />
    </g>
  );
};
const P15: Panel = ({f}) => (
  <g>
    <Head a="Hai kim gặp lại sau" b="không phải 60 phút" />
    <Big x={CX + 100} y={830} size={170} color={AM} o={sp(f, 2, 18)}>65,5 phút</Big>
    <Clock x={CX + 100} y={1080} r={110} hr={32.7} mn={32.7} />
    <Hero2 f={f} />
  </g>
);
const P16: Panel = ({f}) => (
  <g>
    <Head a="Trái Đất cũng vậy" />
    <Clock x={430} y={820} r={70} hr={0} mn={f * 6} />
    <Tag x={790} y={830} color={C.cream} size={40} o={sp(f, 4, 18)}>vòng quay như kim phút</Tag>
    <Sun x={430} y={1030} r={44} f={f} />
    <Tag x={790} y={1040} color={C.cream} size={40} o={sp(f, 18, 32)}>hướng Mặt Trời: kim giờ</Tag>
    <Hero2 f={f} />
  </g>
);
const P17: Panel = ({f}) => {
  const a0 = Math.PI;
  const a1 = Math.PI + 0.22;
  const cx = 700;
  const cy = 860;
  const R = 250;
  return (
    <g>
      <Head a="Mỗi ngày đi một đoạn" b="hướng Mặt Trời dịch khoảng 1 độ" />
      <circle cx={cx} cy={cy} r={R} fill="none" stroke={C.cream} strokeWidth={3} strokeDasharray="10 8" opacity={0.7} />
      <Sun x={cx} y={cy} r={44} f={f} />
      <Earth x={cx + R * Math.cos(a0)} y={cy + R * Math.sin(a0)} r={34} rot={0} flag={false} />
      <g opacity={sp(f, 10, 26)}>
        <Earth x={cx + R * Math.cos(a1)} y={cy + R * Math.sin(a1)} r={34} rot={0} flag={false} />
        <Tag x={470} y={620} color={AM} size={44}>≈ 1 độ</Tag>
      </g>
      <Hero2 f={f} />
    </g>
  );
};
const P18: Panel = ({f}) => (
  <g>
    <Head a="Một vòng quanh Mặt Trời" />
    <Big x={CX + 100} y={850} size={170} color={AM} o={sp(f, 2, 18)}>365 ngày</Big>
    <Hero2 f={f} />
  </g>
);
const P19: Panel = ({f}) => (
  <g>
    <Head a="Một vòng tròn" />
    <circle cx={CX + 100} cy={850} r={200} fill="none" stroke={C.cream} strokeWidth={8} />
    <Big x={CX + 100} y={890} size={110} color={AM} o={sp(f, 4, 20)}>360 độ</Big>
    <Hero2 f={f} />
  </g>
);
const P20: Panel = ({f}) => (
  <g>
    <Head a="Mỗi ngày" b="dịch gần 1 độ" />
    <Calc f={f} x={CX + 100} y={780} step={150} lines={[{t: '360 ÷ 365', at: 2, size: 130}, {t: '≈ 1 độ', at: 22, size: 160, color: AM}]} />
    <Hero2 f={f} />
  </g>
);
const P21: Panel = ({f}) => (
  <g>
    <Head a="Mặt Trời chưa về giữa trời" b="phải quay thêm gần 1 độ" />
    <Earth x={560} y={860} r={130} rot={80 + 14 * sp(f, 14, 50)} />
    <Arrow x1={720} y1={860} x2={930} y2={860} color={AM} p={sp(f, 2, 14)} />
    <Tag x={830} y={800} color={AM} size={38}>về Mặt Trời</Tag>
    <Tag x={CX + 100} y={1080} color={C.cream} size={42} o={sp(f, 30, 46)}>quay thêm gần 1 độ</Tag>
    <Hero2 f={f} />
  </g>
);
const P22: Panel = ({f}) => (
  <g>
    <Head a="Một ngày" />
    <Calc f={f} x={CX + 100} y={780} step={150} lines={[{t: '24 × 60', at: 2, size: 130}, {t: '= 1.440 phút', at: 22, size: 140, color: AM}]} />
    <Hero2 f={f} />
  </g>
);
const P23: Panel = ({f}) => (
  <g>
    <Head a="Chia cho 360 độ" />
    <Calc f={f} x={CX + 100} y={780} step={150} lines={[{t: '1.440 ÷ 360', at: 2, size: 130}, {t: '= 4 phút mỗi độ', at: 22, size: 96, color: AM}]} />
    <Hero2 f={f} />
  </g>
);
const P24: Panel = ({f}) => (
  <g>
    <Head a="Gần 1 độ" b="nhân 4 phút" />
    <Calc f={f} x={CX + 100} y={780} step={150} lines={[{t: '1 độ × 4 phút', at: 2, size: 120}, {t: '≈ 4 phút', at: 22, size: 170, color: AM}]} />
    <Hero2 f={f} />
  </g>
);
const P25: Panel = ({f}) => (
  <g>
    <Head a="Bốn phút quay thêm" b="ngày Mặt Trời dài hơn ngày sao" />
    <Big x={CX + 100} y={870} size={200} color={AM} o={sp(f, 2, 18)}>+ 4 phút</Big>
    <Hero2 f={f} />
  </g>
);
const P26: Panel = ({f}) => (
  <g>
    <Head a="Mỗi đêm sao mọc" b="sớm hơn khoảng 4 phút" />
    <Calc f={f} x={CX + 100} y={780} step={150} lines={[{t: 'tối nay: 21:00', at: 2, size: 100}, {t: 'mai: 20:56', at: 22, size: 120, color: AM}]} />
    <Tag x={CX + 100} y={1100} color={C.cream} size={36} o={sp(f, 30, 44)}>ví dụ một ngôi sao</Tag>
    <Hero2 f={f} />
  </g>
);
const P27: Panel = ({f}) => (
  <g>
    <Head a="Sau 30 đêm" />
    <Calc f={f} x={CX + 100} y={780} step={150} lines={[{t: '30 × 4', at: 2, size: 130}, {t: '= 120 phút', at: 22, size: 150, color: AM}]} />
    <Hero2 f={f} />
  </g>
);
const P28: Panel = ({f}) => (
  <g>
    <Head a="Sao mọc sớm hơn" />
    <Big x={CX + 100} y={870} size={200} color={AM} o={sp(f, 2, 18)}>2 tiếng</Big>
    <Hero2 f={f} />
  </g>
);
const P29: Panel = ({f}) => (
  <g>
    <Head a="Cả năm" b="quay quanh mình nhiều hơn số ngày" />
    <Big x={CX + 100} y={870} size={190} color={AM} o={sp(f, 2, 18)}>+ 1 vòng</Big>
    <Hero2 f={f} />
  </g>
);
const P30: Panel = ({f}) => (
  <g>
    <Head a="Một vòng quay thật" />
    <Big x={CX + 100} y={860} size={120} color={AM} o={sp(f, 2, 18)}>23 giờ 56 phút</Big>
    <Hero2 f={f} />
  </g>
);
const P31: Panel = ({f}) => {
  const a = f * 0.03 + 3.2;
  return (
    <g>
      <Head a="Ngày dài hơn 4 phút" b="vì còn đi quanh Mặt Trời" />
      <ellipse cx={640} cy={780} rx={240} ry={130} fill="none" stroke={C.cream} strokeWidth={3} strokeDasharray="10 8" opacity={0.7} />
      <Sun x={640} y={780} r={40} f={f} />
      <Earth x={640 + 240 * Math.cos(a)} y={780 + 130 * Math.sin(a)} r={42} rot={f * 8} />
      <Big x={CX + 100} y={1100} size={140} color={AM} o={sp(f, 6, 22)}>+ 4 phút</Big>
      <Hero2 f={f} cheer={sp(f, 10, 28)} />
    </g>
  );
};

export const PANELS: Panel[] = [P0, P1, P2, P3, P4, P5, P6, P7, P8, P9, P10, P11, P12, P13, P14, P15, P16, P17, P18, P19, P20, P21, P22, P23, P24, P25, P26, P27, P28, P29, P30, P31];
void lerp;
void clamp01;
