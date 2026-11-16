import {buildTimeline} from '../khoahoc/tl';
import texts from './texts.json';
import ledaDur from './leda_dur.json';

// Video khoa học số 20 (dọc 1080x1920, tiếng Việt): Một năm dài bao nhiêu ngày. Kịch bản: ke-hoach/khoa-hoc-video-20-do-dai-nam-kich-ban.md
// texts.json là PHỤ ĐỀ (chữ số); bản đọc nằm trong ke-hoach/giong-video-khoa-hoc-namdai.json.
export const SIZES = [4, 4, 2, 7, 5, 7, 2];
export const timeline = () => buildTimeline(texts as string[], SIZES, ledaDur as number[]);
