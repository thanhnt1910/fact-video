import {buildTimeline} from '../khoahoc/tl';
import texts from './texts.json';
import ledaDur from './leda_dur.json';

// Video khoa học số 27 (dọc 1080x1920, tiếng Việt): Đường chân trời xa bao nhiêu. Kịch bản: ke-hoach/khoa-hoc-video-27-chan-troi-kich-ban.md
// texts.json là PHỤ ĐỀ (chữ số); bản đọc nằm trong ke-hoach/giong-video-khoa-hoc-chantroi.json.
export const SIZES = [4, 8, 6, 6, 9, 6];
export const timeline = () => buildTimeline(texts as string[], SIZES, ledaDur as number[]);
