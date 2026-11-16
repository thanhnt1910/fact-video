import {makeVideo} from '../khoahoc/kit';
import {NdBackground} from './Bg';
import {timeline} from './content';
import {PANELS} from './scenes';
import CAPS from './caps.json';

export const Namdai = makeVideo(NdBackground, '#1c1832', timeline(), PANELS, CAPS);
