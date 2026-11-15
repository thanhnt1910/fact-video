import {buildTimeline} from '../khoahoc/tl';
import texts from './texts.json';
import ledaDur from './leda_dur.json';

// Video khoa học số 17 (dọc 1080x1920, tiếng Việt): Một mét dài bao nhiêu. Kịch bản: ke-hoach/khoa-hoc-video-17-mot-met-kich-ban.md
// texts.json là PHỤ ĐỀ (chữ số); bản đọc nằm trong ke-hoach/giong-video-khoa-hoc-motmet.json.
export const SIZES = [4, 5, 3, 6, 5, 6, 3];
export const timeline = () => buildTimeline(texts as string[], SIZES, ledaDur as number[]);
