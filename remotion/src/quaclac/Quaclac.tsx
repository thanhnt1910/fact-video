import {makeVideo} from '../khoahoc/kit';
import {QlBackground} from './Bg';
import {timeline} from './content';
import {PANELS} from './scenes';
import CAPS from './caps.json';

export const Quaclac = makeVideo(QlBackground, '#3b2a1d', timeline(), PANELS, CAPS);
