import {buildTimeline} from '../khoahoc/tl';
import texts from './texts.json';
import ledaDur from './leda_dur.json';

// Video khoa học số 25 (dọc 1080x1920, tiếng Việt): Sóng thần chạy nhanh bao nhiêu. Kịch bản: ke-hoach/khoa-hoc-video-25-song-than-kich-ban.md
// texts.json là PHỤ ĐỀ (chữ số); bản đọc nằm trong ke-hoach/giong-video-khoa-hoc-songthan.json.
export const SIZES = [4, 3, 4, 7, 4, 4];
export const timeline = () => buildTimeline(texts as string[], SIZES, ledaDur as number[]);
