import {makeVideo} from '../khoahoc/kit';
import {SaoBackground} from './Bg';
import {timeline} from './content';
import {PANELS} from './scenes';
import CAPS from './caps.json';

export const Sao = makeVideo(SaoBackground, '#141a45', timeline(), PANELS, CAPS);
