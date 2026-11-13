import {makeVideo} from '../khoahoc/kit';
import {MtBackground} from './Bg';
import {timeline} from './content';
import {PANELS} from './scenes';
import CAPS from './caps.json';

export const Matrang = makeVideo(MtBackground, '#0d1428', timeline(), PANELS, CAPS);
