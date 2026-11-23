import {makeVideo} from '../khoahoc/kit';
import {NsBackground} from './Bg';
import {timeline} from './content';
import {PANELS} from './scenes';
import CAPS from './caps.json';

export const Ngaysao = makeVideo(NsBackground, '#10131f', timeline(), PANELS, CAPS);
