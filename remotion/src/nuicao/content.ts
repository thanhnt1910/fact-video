import {buildTimeline} from '../khoahoc/tl';
import texts from './texts.json';
import ledaDur from './leda_dur.json';

// Video khoa học số 13 (dọc 1080x1920, tiếng Việt): Núi cao bao nhiêu (Ê-vơ-rét). Kịch bản: ke-hoach/khoa-hoc-video-13-nui-cao-kich-ban.md
// texts.json là PHỤ ĐỀ (chữ số); bản đọc nằm trong ke-hoach/giong-video-khoa-hoc-nuicao.json.
export const SIZES = [4, 6, 6, 6, 6, 5];
export const timeline = () => buildTimeline(texts as string[], SIZES, ledaDur as number[]);
