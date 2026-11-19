import {buildTimeline} from '../khoahoc/tl';
import texts from './texts.json';
import ledaDur from './leda_dur.json';

// Video khoa học số 23 (dọc 1080x1920, tiếng Việt): Giếng sâu bao nhiêu (Galileo, máng dốc). Kịch bản: ke-hoach/khoa-hoc-video-23-gieng-sau-kich-ban.md
// texts.json là PHỤ ĐỀ (chữ số); bản đọc nằm trong ke-hoach/giong-video-khoa-hoc-gieng.json.
export const SIZES = [3, 6, 6, 6, 7];
export const timeline = () => buildTimeline(texts as string[], SIZES, ledaDur as number[]);
