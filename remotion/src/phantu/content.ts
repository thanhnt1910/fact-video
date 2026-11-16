import {buildTimeline} from '../khoahoc/tl';
import texts from './texts.json';
import ledaDur from './leda_dur.json';

// Video khoa học số 19 (dọc 1080x1920, tiếng Việt): Một phân tử dày bao nhiêu. Kịch bản: ke-hoach/khoa-hoc-video-19-phan-tu-day-kich-ban.md
// texts.json là PHỤ ĐỀ (chữ số); bản đọc nằm trong ke-hoach/giong-video-khoa-hoc-phantu.json.
export const SIZES = [4, 5, 2, 4, 5, 4, 3];
export const timeline = () => buildTimeline(texts as string[], SIZES, ledaDur as number[]);
