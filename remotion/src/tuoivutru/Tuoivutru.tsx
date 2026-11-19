import {makeVideo} from '../khoahoc/kit';
import {TvBackground} from './Bg';
import {timeline} from './content';
import {PANELS} from './scenes';
import CAPS from './caps.json';

export const Tuoivutru = makeVideo(TvBackground, '#14172f', timeline(), PANELS, CAPS);
