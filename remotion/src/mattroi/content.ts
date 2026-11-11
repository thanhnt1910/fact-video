import {buildTimeline} from '../khoahoc/tl';
import texts from './texts.json';
import ledaDur from './leda_dur.json';

// Video khoa học số 10 (dọc 1080x1920, tiếng Việt): Mặt Trời xa hơn Mặt Trăng bao nhiêu lần. Kịch bản: ke-hoach/khoa-hoc-video-10-mat-troi-mat-trang-kich-ban.md
// texts.json là PHỤ ĐỀ (chữ số); bản đọc nằm trong ke-hoach/giong-video-khoa-hoc-mattroi.json.
export const SIZES = [4, 6, 6, 4, 3, 2];
export const timeline = () => buildTimeline(texts as string[], SIZES, ledaDur as number[]);
