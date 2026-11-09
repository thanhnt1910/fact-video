import React from 'react';
import {Composition} from 'remotion';
import {DemoBanDo, DEMO_DURATION} from './DemoBanDo';
import {Thales} from './thales/Thales';
import {timeline} from './thales/content';
import {Thales2} from './thales2/Thales2';
import {timeline2} from './thales2/content';
import {Thales3} from './thales3/Thales3';
import {timeline3} from './thales3/content';
import {FPS, H, W} from './lib/theme';

export const Root: React.FC = () => {
  return (
    <>
      <Composition id="DemoBanDo" component={DemoBanDo} durationInFrames={DEMO_DURATION} fps={30} width={1080} height={1920} />
      <Composition id="ThalesEN" component={Thales} durationInFrames={timeline('en').total} fps={FPS} width={W} height={H} defaultProps={{lang: 'en' as const}} />
      <Composition id="ThalesVI" component={Thales} durationInFrames={timeline('vi').total} fps={FPS} width={W} height={H} defaultProps={{lang: 'vi' as const}} />
      <Composition id="Thales2EN" component={Thales2} durationInFrames={timeline2('en').total} fps={FPS} width={W} height={H} defaultProps={{lang: 'en' as const}} />
      <Composition id="Thales2VI" component={Thales2} durationInFrames={timeline2('vi').total} fps={FPS} width={W} height={H} defaultProps={{lang: 'vi' as const}} />
      <Composition id="Thales3" component={Thales3} durationInFrames={timeline3().total} fps={FPS} width={W} height={H} />
    </>
  );
};
