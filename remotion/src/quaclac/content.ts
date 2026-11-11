import {buildTimeline} from '../khoahoc/tl';
import texts from './texts.json';
import ledaDur from './leda_dur.json';

// Video khoa học số 12 (dọc 1080x1920, tiếng Việt): Đồng hồ quả lắc. Kịch bản: ke-hoach/khoa-hoc-video-12-dong-ho-qua-lac-kich-ban.md
// texts.json là PHỤ ĐỀ (chữ số); bản đọc nằm trong ke-hoach/giong-video-khoa-hoc-quaclac.json.
export const SIZES = [4, 4, 3, 3, 7, 2];
export const timeline = () => buildTimeline(texts as string[], SIZES, ledaDur as number[]);
