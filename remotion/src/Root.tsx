import React from 'react';
import {Composition} from 'remotion';
import {DemoBanDo, DEMO_DURATION} from './DemoBanDo';
import {Thales} from './thales/Thales';
import {timeline} from './thales/content';
import {Thales2} from './thales2/Thales2';
import {timeline2} from './thales2/content';
import {Thales3} from './thales3/Thales3';
import {timeline3} from './thales3/content';
import {Eratosthenes} from './eratosthenes/Eratosthenes';
import {Cavendish} from './cavendish/Cavendish';
import {Anhsang} from './anhsang/Anhsang';
import {timeline as timelineAs} from './anhsang/content';
import {Kinhdo} from './kinhdo/Kinhdo';
import {Daybien} from './daybien/Daybien';
import {Vuongmien} from './vuongmien/Vuongmien';
import {timeline as timelineVm} from './vuongmien/content';
import {Kinhhienvi} from './kinhhienvi/Kinhhienvi';
import {Sao} from './sao/Sao';
import {Quaclac} from './quaclac/Quaclac';
import {Nuicao} from './nuicao/Nuicao';
import {Tuoitd} from './tuoitd/Tuoitd';
import {Matrang} from './matrang/Matrang';
import {timeline as timelineMtr} from './matrang/content';
import {timeline as timelineTd} from './tuoitd/content';
import {timeline as timelineNc} from './nuicao/content';
import {timeline as timelineQl} from './quaclac/content';
import {Nhietke} from './nhietke/Nhietke';
import {timeline as timelineNk} from './nhietke/content';
import {Mattroi} from './mattroi/Mattroi';
import {timeline as timelineMt} from './mattroi/content';
import {Amthanh} from './amthanh/Amthanh';
import {timeline as timelineAm} from './amthanh/content';
import {timeline as timelineSao} from './sao/content';
import {timeline as timelineKh} from './kinhhienvi/content';
import {timeline as timelineDb} from './daybien/content';
import {timeline as timelineKd} from './kinhdo/content';
import {timeline as timelineCav} from './cavendish/content';
import {timeline as timelineEra} from './eratosthenes/content';
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
      <Composition id="Anhsang" component={Anhsang} durationInFrames={timelineAs().total} fps={FPS} width={1080} height={1920} />
      <Composition id="Vuongmien" component={Vuongmien} durationInFrames={timelineVm().total} fps={FPS} width={1080} height={1920} />
      <Composition id="Kinhhienvi" component={Kinhhienvi} durationInFrames={timelineKh().total} fps={FPS} width={1080} height={1920} />
      <Composition id="Sao" component={Sao} durationInFrames={timelineSao().total} fps={FPS} width={1080} height={1920} />
      <Composition id="Quaclac" component={Quaclac} durationInFrames={timelineQl().total} fps={FPS} width={1080} height={1920} />
      <Composition id="Nuicao" component={Nuicao} durationInFrames={timelineNc().total} fps={FPS} width={1080} height={1920} />
      <Composition id="Tuoitd" component={Tuoitd} durationInFrames={timelineTd().total} fps={FPS} width={1080} height={1920} />
      <Composition id="Matrang" component={Matrang} durationInFrames={timelineMtr().total} fps={FPS} width={1080} height={1920} />
      <Composition id="Nhietke" component={Nhietke} durationInFrames={timelineNk().total} fps={FPS} width={1080} height={1920} />
      <Composition id="Mattroi" component={Mattroi} durationInFrames={timelineMt().total} fps={FPS} width={1080} height={1920} />
      <Composition id="Amthanh" component={Amthanh} durationInFrames={timelineAm().total} fps={FPS} width={1080} height={1920} />
      <Composition id="Daybien" component={Daybien} durationInFrames={timelineDb().total} fps={FPS} width={1080} height={1920} />
      <Composition id="Kinhdo" component={Kinhdo} durationInFrames={timelineKd().total} fps={FPS} width={1080} height={1920} />
      <Composition id="Cavendish" component={Cavendish} durationInFrames={timelineCav().total} fps={FPS} width={1080} height={1920} />
      <Composition id="Eratosthenes" component={Eratosthenes} durationInFrames={timelineEra().total} fps={FPS} width={1080} height={1920} />
    </>
  );
};
