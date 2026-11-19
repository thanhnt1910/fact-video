import {makeVideo} from '../khoahoc/kit';
import {GiBackground} from './Bg';
import {timeline} from './content';
import {PANELS} from './scenes';
import CAPS from './caps.json';

export const Gieng = makeVideo(GiBackground, '#1c2627', timeline(), PANELS, CAPS);
