import {buildTimeline} from '../khoahoc/tl';
import texts from './texts.json';
import ledaDur from './leda_dur.json';

// Video khoa học số 15 (dọc 1080x1920, tiếng Việt): Mặt Trăng xa bao nhiêu. Kịch bản: ke-hoach/khoa-hoc-video-15-mat-trang-xa-kich-ban.md
// texts.json là PHỤ ĐỀ (chữ số); bản đọc nằm trong ke-hoach/giong-video-khoa-hoc-matrang.json.
export const SIZES = [4, 7, 5, 5, 6, 4];
export const timeline = () => buildTimeline(texts as string[], SIZES, ledaDur as number[]);
