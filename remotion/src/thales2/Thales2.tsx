import React from 'react';
import {AbsoluteFill, Sequence} from 'remotion';
import {C} from '../lib/theme';
import {Fonts} from '../lib/Fonts';
import {Lang} from '../thales/content';
import {Background, Captions, Hud, SceneFade} from '../thales/Thales';
import {LABELS2, SceneId, timeline2} from './content';
import {Equal, Finale, Half, Hook, Numbers, Sc, StickTrick, SunShadow} from './scenes';

const SCENES: Record<SceneId, React.FC<Sc>> = {
  hook: Hook,
  sun: SunShadow,
  equal: Equal,
  half: Half,
  stick: StickTrick,
  numbers: Numbers,
  outro: Finale,
};

export const Thales2: React.FC<{lang: Lang}> = ({lang}) => {
  const tl = timeline2(lang);
  const t = LABELS2[lang];
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
