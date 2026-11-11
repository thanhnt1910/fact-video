import {makeVideo} from '../khoahoc/kit';
import {TdBackground} from './Bg';
import {timeline} from './content';
import {PANELS} from './scenes';
import CAPS from './caps.json';

export const Tuoitd = makeVideo(TdBackground, '#2a2018', timeline(), PANELS, CAPS);
