import {makeVideo} from '../khoahoc/kit';
import {NcBackground} from './Bg';
import {timeline} from './content';
import {PANELS} from './scenes';
import CAPS from './caps.json';

export const Nuicao = makeVideo(NcBackground, '#1b2d4a', timeline(), PANELS, CAPS);
