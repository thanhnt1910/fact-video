import {buildTimeline} from '../khoahoc/tl';
import texts from './texts.json';
import ledaDur from './leda_dur.json';

// Video khoa học số 26 (dọc 1080x1920, tiếng Việt): Tàu chạy nhanh bao nhiêu (dây thắt nút). Kịch bản: ke-hoach/khoa-hoc-video-26-day-nut-kich-ban.md
// texts.json là PHỤ ĐỀ (chữ số); bản đọc nằm trong ke-hoach/giong-video-khoa-hoc-daynut.json.
export const SIZES = [3, 8, 6, 5, 3, 5];
export const timeline = () => buildTimeline(texts as string[], SIZES, ledaDur as number[]);
