import {buildTimeline} from '../khoahoc/tl';
import texts from './texts.json';
import ledaDur from './leda_dur.json';

// Video khoa học số 24 (dọc 1080x1920, tiếng Việt): Vũ trụ bao nhiêu tuổi (Hubble, chiếu phim ngược). Kịch bản: ke-hoach/khoa-hoc-video-24-tuoi-vu-tru-kich-ban.md
// texts.json là PHỤ ĐỀ (chữ số); bản đọc nằm trong ke-hoach/giong-video-khoa-hoc-tuoivutru.json.
export const SIZES = [3, 3, 7, 6, 3, 5];
export const timeline = () => buildTimeline(texts as string[], SIZES, ledaDur as number[]);
