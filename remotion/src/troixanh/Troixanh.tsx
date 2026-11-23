import {makeVideo} from '../khoahoc/kit';
import {TxBackground} from './Bg';
import {timeline} from './content';
import {PANELS} from './scenes';
import CAPS from './caps.json';

export const Troixanh = makeVideo(TxBackground, '#142038', timeline(), PANELS, CAPS);
