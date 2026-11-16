import {makeVideo} from '../khoahoc/kit';
import {ClBackground} from './Bg';
import {timeline} from './content';
import {PANELS} from './scenes';
import CAPS from './caps.json';

export const Conlac = makeVideo(ClBackground, '#26231c', timeline(), PANELS, CAPS);
