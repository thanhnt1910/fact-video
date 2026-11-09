import React from 'react';
import {AbsoluteFill, Sequence} from 'remotion';
import {C} from '../lib/theme';
import {Fonts} from '../lib/Fonts';
import {Background, Captions, Hud, SceneFade} from '../thales/Thales';
import {Equal, Finale, Half, Numbers, Sc, StickTrick, SunShadow} from '../thales2/scenes';
import {LABELS3, SceneId, timeline3} from './content';
import {Everest, Everyday, Hook3, Idea, LadderFail, Modern, SlopeFail, Tools} from './scenes';

const SCENES: Record<SceneId, React.FC<Sc>> = {
  hook: Hook3,
  tools: Tools,
  ladder: LadderFail,
  slope: SlopeFail,
  idea: Idea,
  sun: SunShadow,
  equal: Equal,
  half: Half,
  stick: StickTrick,
  numbers: Numbers,
  modern: Modern,
  everest: Everest,
  everyday: Everyday,
  outro: Finale,
};

export const Thales3: React.FC = () => {
  const tl = timeline3();
  return (
    <AbsoluteFill style={{background: C.bg2}}>
      <Fonts />
      <Background />
      {tl.scenes.map((s) => {
        const Scene = SCENES[s.id];
        return (
          <Sequence key={s.id} from={s.start} durationInFrames={s.dur}>
            <SceneFade dur={s.dur}>
              <Scene dur={s.dur} bs={s.bs} t={LABELS3} />
            </SceneFade>
          </Sequence>
        );
      })}
      <Hud />
      <Captions beats={tl.beats} />
    </AbsoluteFill>
  );
};
