import React from 'react';
import {AbsoluteFill, Sequence, useCurrentFrame} from 'remotion';
import {C, W, H, seg} from '../lib/theme';
import {Fonts} from '../lib/Fonts';
import {LABELS, Lang, SceneTl, timeline} from './content';
import {Equal, Intro, Numbers, Outro, Rays, Sc, Similar} from './scenes';
import {FlameMark} from './parts';

export const Background: React.FC = () => (
  <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} style={{position: 'absolute', left: 0, top: 0}}>
    <defs>
      <radialGradient id="bgT" cx="50%" cy="45%" r="75%">
        <stop offset="0%" stopColor={C.bg1} />
        <stop offset="100%" stopColor={C.bg2} />
      </radialGradient>
      <pattern id="gridT" width="80" height="80" patternUnits="userSpaceOnUse">
        <path d="M80 0 L0 0 L0 80" fill="none" stroke={C.cream} strokeWidth="1.5" opacity="0.07" />
      </pattern>
    </defs>
    <rect width={W} height={H} fill="url(#bgT)" />
    <rect width={W} height={H} fill="url(#gridT)" />
    <rect x={30} y={30} width={W - 60} height={H - 60} rx={8} fill="none" stroke={C.cream} strokeWidth={2} opacity={0.14} />
  </svg>
);

export const Hud: React.FC = () => (
  <div style={{position: 'absolute', right: 80, top: 54, display: 'flex', alignItems: 'center', gap: 14, opacity: 0.9}}>
    <FlameMark width={34} />
    <div style={{fontFamily: 'Cormorant', fontWeight: 600, fontSize: 50, lineHeight: 1, color: C.cream}}>
      Proof<span style={{color: C.amber}}>wick</span>
    </div>
  </div>
);

export const Captions: React.FC<{beats: {text: string; start: number; dur: number}[]}> = ({beats}) => {
  const f = useCurrentFrame();
  const b = beats.find((x) => f >= x.start && f < x.start + x.dur);
  if (!b || !b.text) return null;
  const local = f - b.start;
  const o = Math.min(seg(local, 0, 8), 1 - seg(local, b.dur - 8, b.dur));
  return (
    <div style={{position: 'absolute', left: 190, width: 1540, top: 905, height: 130, display: 'flex', alignItems: 'center', justifyContent: 'center', opacity: o}}>
      <div
        style={{
          fontFamily: 'BeVN',
          fontWeight: 800,
          fontSize: 42,
          lineHeight: 1.28,
          textAlign: 'center',
          color: '#fff',
          WebkitTextStroke: '8px #130c08',
          paintOrder: 'stroke fill',
        }}
      >
        {b.text}
      </div>
    </div>
  );
};

export const SceneFade: React.FC<{dur: number; children: React.ReactNode}> = ({dur, children}) => {
  const f = useCurrentFrame();
  const o = Math.min(seg(f, 0, 8), 1 - seg(f, dur - 8, dur));
  return <AbsoluteFill style={{opacity: o}}>{children}</AbsoluteFill>;
};

const SCENES: Record<SceneTl['id'], React.FC<Sc>> = {
  intro: Intro,
  rays: Rays,
  equal: Equal,
  similar: Similar,
  numbers: Numbers,
  outro: Outro,
};

export const Thales: React.FC<{lang: Lang}> = ({lang}) => {
  const tl = timeline(lang);
  const t = LABELS[lang];
  return (
    <AbsoluteFill style={{background: C.bg2}}>
      <Fonts />
      <Background />
      {tl.scenes.map((s) => {
        const Scene = SCENES[s.id];
        return (
          <Sequence key={s.id} from={s.start} durationInFrames={s.dur}>
            <SceneFade dur={s.dur}>
              <Scene dur={s.dur} bs={s.bs} t={t} />
            </SceneFade>
          </Sequence>
        );
      })}
      <Hud />
      <Captions beats={tl.beats} />
    </AbsoluteFill>
  );
};
