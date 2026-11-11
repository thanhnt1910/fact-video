import React from 'react';
import {AbsoluteFill, Sequence, useCurrentFrame} from 'remotion';
import {C, FPS, clamp01, seg, sp} from '../lib/theme';
import {Fonts} from '../lib/Fonts';
import {SceneFade} from '../thales/Thales';
import {Big, Hero, Lab, Svg, VCaptions, VHud, lerp} from '../eratosthenes/v';
import {Head, Tag} from '../kinhdo/scenes';

export {C, FPS, clamp01, seg, sp, Big, Hero, Lab, Svg, lerp, Head, Tag};

export {END_C, buildTimeline} from './tl';
export type {Beat, SceneTl, Tl} from './tl';
import type {Tl, SceneTl} from './tl';
export type Panel = (a: {f: number; d: number; k: number}) => React.ReactNode;

const Push: React.FC<{dur: number; children: React.ReactNode}> = ({dur, children}) => {
  const f = useCurrentFrame();
  const k = 1 + 0.02 * Math.min(1, f / Math.max(1, dur));
  return <div style={{position: 'absolute', inset: 0, transform: `scale(${k})`, transformOrigin: '50% 48%'}}>{children}</div>;
};

const PanelScene: React.FC<{s: SceneTl; panels: Panel[]}> = ({s, panels}) => {
  const f = useCurrentFrame();
  const n = s.beats.length;
  return (
    <Svg>
      {s.beats.map((b, i) => {
        const hasText = !!b.text;
        const k = s.first + Math.min(i, panels.length - 1 - s.first);
        const pi = hasText ? s.first + i : Math.min(s.first + i - 1, panels.length - 1);
        const next = i < n - 1 && s.beats[i + 1].text !== '';
        const o = hasText ? sp(f, s.bs[i] + 2, s.bs[i] + 14) * (next ? 1 - sp(f, s.bs[i + 1] - 10, s.bs[i + 1]) : 1) : 0;
        const shown = hasText ? o : 0;
        if (hasText && shown <= 0.001) return null;
        if (!hasText) return null;
        const P = panels[pi];
        void k;
        return (
          <g key={i} opacity={shown}>
            {P({f: f - s.bs[i], d: b.dur, k: pi})}
          </g>
        );
      })}
    </Svg>
  );
};

export const makeVideo = (bg: React.FC, bgColor: string, tl: Tl, panels: Panel[], caps: unknown) => {
  const V: React.FC = () => {
    const Bg = bg;
    return (
      <AbsoluteFill style={{background: bgColor}}>
        <Fonts />
        <Bg />
        {tl.scenes.map((s) => (
          <Sequence key={s.first} from={s.start} durationInFrames={s.dur}>
            <SceneFade dur={s.dur}>
              <Push dur={s.dur}>
                <PanelScene s={s} panels={panels} />
              </Push>
            </SceneFade>
          </Sequence>
        ))}
        <VHud />
        <VCaptions beats={tl.beats} caps={caps as {text: string; start: number; end: number}[][]} />
      </AbsoluteFill>
    );
  };
  return V;
};

/** Người que đội mũ riêng theo chủ đề. */
export type HatKind = 'helmet' | 'pirate' | 'scholar' | 'goggles' | 'gear';
export const HatHero: React.FC<{x: number; y: number; s?: number; walk?: number; cheer?: number; hat: HatKind; stick?: boolean}> = ({x, y, s = 1, walk = 0, cheer = 0, hat, stick = false}) => {
  const bob = (Math.abs(Math.sin(walk)) * 2.5 + clamp01(cheer) * Math.abs(Math.sin(walk * 1.6)) * 7) * s;
  const sk = 5 / s;
  return (
    <g>
      <Hero x={x} y={y} s={s} walk={walk} cheer={cheer} stick={stick} />
      <g transform={`translate(${x} ${y - bob}) scale(${s})`} strokeWidth={sk} strokeLinecap="round" strokeLinejoin="round">
        {hat === 'helmet' && (
          <g fill="#bfe3f0" fillOpacity={0.28} stroke={C.cream}>
            <circle cx={0} cy={-70} r={19} />
            <path d="M -12 -78 Q 0 -86 12 -78" fill="none" strokeWidth={sk * 0.6} opacity={0.7} />
          </g>
        )}
        {hat === 'pirate' && (
          <g fill="#2a2a38" stroke={C.cream}>
            <path d="M -22 -80 Q -4 -112 20 -80 Q 0 -88 -22 -80 Z" />
            <circle cx={0} cy={-90} r={3} fill={C.cream} stroke="none" />
          </g>
        )}
        {hat === 'scholar' && (
          <g fill="#dcd2b4" stroke={C.cream}>
            <path d="M -16 -82 Q -16 -96 0 -96 Q 16 -96 16 -82 Z" />
            <path d="M -14 -82 L 4 -76 L 22 -82" fill="none" />
            <path d="M -17 -81 Q -6 -76 -2 -70" fill="none" opacity={0.9} />
          </g>
        )}
        {hat === 'goggles' && (
          <g fill="#bfe3f0" fillOpacity={0.35} stroke={C.cream}>
            <circle cx={-5} cy={-70} r={5.5} />
            <circle cx={6} cy={-70} r={5.5} />
            <line x1={-11} y1={-70} x2={-15} y2={-72} />
            <line x1={12} y1={-70} x2={15} y2={-72} />
          </g>
        )}
        {hat === 'gear' && (
          <g fill="#8a6a3a" stroke={C.cream}>
            <path d="M -14 -82 L -10 -98 L -4 -90 L 0 -102 L 4 -90 L 10 -98 L 14 -82 Z" />
          </g>
        )}
      </g>
    </g>
  );
};

/** Các dòng tính toán hiện dần: at = khung (trong khung câu) bắt đầu hiện. */
export const Calc: React.FC<{f: number; x?: number; y: number; step?: number; lines: {t: string; at: number; color?: string; size?: number}[]}> = ({f, x = 540, y, step = 120, lines}) => (
  <g>
    {lines.map((l, i) => (
      <Big key={i} x={x} y={y + i * step} size={l.size ?? 92} color={l.color ?? C.cream} o={sp(f, l.at, l.at + 12)}>
        {l.t}
      </Big>
    ))}
  </g>
);

/** Thanh ngang so sánh độ dài (0..1). */
export const Bar: React.FC<{x: number; y: number; w: number; h?: number; color: string; p: number; label?: string; lc?: string}> = ({x, y, w, h = 68, color, p, label, lc = C.ink}) => (
  <g>
    <rect x={x} y={y} width={Math.max(2, w * clamp01(p))} height={h} rx={10} fill={color} stroke={C.cream} strokeWidth={4} />
    {label && (
      <text x={x + 18} y={y + h * 0.7} fontFamily="BeVN" fontWeight={800} fontSize={h * 0.55} fill={lc}>
        {label}
      </text>
    )}
  </g>
);

export const Dash: React.FC<{x1: number; y1: number; x2: number; y2: number; color?: string; p?: number; w?: number}> = ({x1, y1, x2, y2, color = C.amber, p = 1, w = 5}) => (
  <line x1={x1} y1={y1} x2={lerp(x1, x2, clamp01(p))} y2={lerp(y1, y2, clamp01(p))} stroke={color} strokeWidth={w} strokeDasharray="12 10" strokeLinecap="round" opacity={clamp01(p * 3)} />
);

export const Arrow: React.FC<{x1: number; y1: number; x2: number; y2: number; color?: string; p?: number; w?: number}> = ({x1, y1, x2, y2, color = C.amber, p = 1, w = 7}) => {
  const k = clamp01(p);
  const ex = lerp(x1, x2, k);
  const ey = lerp(y1, y2, k);
  const a = Math.atan2(y2 - y1, x2 - x1);
  return (
    <g opacity={clamp01(p * 3)} stroke={color} strokeWidth={w} strokeLinecap="round" strokeLinejoin="round" fill="none">
      <line x1={x1} y1={y1} x2={ex} y2={ey} />
      <path d={`M ${ex - 26 * Math.cos(a - 0.45)} ${ey - 26 * Math.sin(a - 0.45)} L ${ex} ${ey} L ${ex - 26 * Math.cos(a + 0.45)} ${ey - 26 * Math.sin(a + 0.45)}`} />
    </g>
  );
};
