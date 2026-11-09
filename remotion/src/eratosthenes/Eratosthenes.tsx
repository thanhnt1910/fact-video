import React from 'react';
import {AbsoluteFill, Sequence} from 'remotion';
import {C} from '../lib/theme';
import {Fonts} from '../lib/Fonts';
import {SceneFade} from '../thales/Thales';
import {LAB, SceneId, timeline} from './content';
import {Calc, Clue, Compare, Hook, Idea, Modern, Outro, Problem, Sc} from './scenes';
import {VBackground, VCaptions, VHud} from './v';

const SCENES: Record<SceneId, React.FC<Sc>> = {
  hook: Hook,
  problem: Problem,
  clue: Clue,
  idea: Idea,
  calc: Calc,
  compare: Compare,
  modern: Modern,
  outro: Outro,
};

export const Eratosthenes: React.FC = () => {
  const tl = timeline();
  return (
    <AbsoluteFill style={{background: C.bg2}}>
      <Fonts />
      <VBackground />
      {tl.scenes.map((s) => {
        const Scene = SCENES[s.id];
        return (
          <Sequence key={s.id} from={s.start} durationInFrames={s.dur}>
            <SceneFade dur={s.dur}>
              <Scene dur={s.dur} bs={s.bs} t={LAB} />
            </SceneFade>
          </Sequence>
        );
      })}
      <VHud />
      <VCaptions beats={tl.beats} />
    </AbsoluteFill>
  );
};
