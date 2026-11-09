import {FPS} from '../lib/theme';

// Kịch bản video 1: "How Thales Measured a Pyramid" / "Thales đo kim tự tháp như thế nào"
// Nguồn đã kiểm: xem remotion/scripts/thales.md

export type Lang = 'en' | 'vi';
export type SceneId = 'intro' | 'rays' | 'equal' | 'similar' | 'numbers' | 'outro';

export const END_SEC = 3.5; // thẻ kết

export const TEXT: Record<Lang, Record<SceneId, string[]>> = {
  en: {
    intro: [
      'Ancient writers tell a story about Thales, a Greek thinker who lived about 2,600 years ago.',
      'He stood before the Great Pyramid of Giza, already some two thousand years old, and asked: how tall is it?',
      'He had no ladder and no rope. Only a stick, and the Sun.',
    ],
    rays: [
      'The Sun is so far away that its rays reach us almost perfectly parallel.',
      'So at one moment, every upright object casts a shadow at the same angle. The taller it is, the longer its shadow.',
    ],
    equal: [
      'The first account says Thales waited for the hour when his own shadow was exactly as long as he was tall.',
      "At that moment, the pyramid's height equals its shadow, measured from the center of its base.",
      'You can only measure from the edge, so you add half the base.',
    ],
    similar: [
      "A second account, by Plutarch, is more general. Thales set a stick upright at the tip of the pyramid's shadow.",
      "The Sun's rays form two triangles with the same shape: one small, one huge.",
      "So the pyramid's height is to the stick's height as the pyramid's shadow is to the stick's shadow.",
    ],
    numbers: [
      'Try it with example numbers. A two-meter stick casts a three-meter shadow.',
      "The pyramid's shadow, from the center of its base, measures 220 meters.",
      'The height is 220 times two, divided by three: about 147 meters.',
      'The Great Pyramid was built about 146.6 meters tall. Today, with its outer casing gone, it stands 138.5.',
    ],
    outro: [
      'No climbing. No rope. Just light, a stick, and proportion.',
      "Did Thales really do it? We can't be sure. But the proof works for anyone, anywhere, today. That is how we know.",
    ],
  },
  vi: {
    intro: [
      'Các tác giả cổ đại kể về Thales, một nhà tư tưởng Hy Lạp sống cách đây khoảng 2.600 năm.',
      'Ông đứng trước Đại Kim Tự Tháp Giza, lúc đó đã hai nghìn năm tuổi, và tự hỏi: nó cao bao nhiêu?',
      'Ông không có thang, không có dây. Chỉ có một cây gậy và Mặt Trời.',
    ],
    rays: [
      'Mặt Trời ở quá xa, nên tia sáng của nó đến chúng ta gần như song song.',
      'Vì vậy, cùng một lúc, mọi vật dựng đứng đều đổ bóng theo cùng một góc. Vật càng cao, bóng càng dài.',
    ],
    equal: [
      'Theo ghi chép thứ nhất, Thales chờ đến giờ bóng của chính ông dài đúng bằng chiều cao của ông.',
      'Lúc đó, chiều cao kim tự tháp bằng độ dài bóng của nó, tính từ tâm đáy.',
      'Ta chỉ đo được từ mép đáy, nên phải cộng thêm nửa cạnh đáy.',
    ],
    similar: [
      'Ghi chép thứ hai, của Plutarch, tổng quát hơn. Thales cắm một cây gậy thẳng đứng ngay đầu bóng của kim tự tháp.',
      'Tia nắng tạo ra hai tam giác cùng hình dạng: một nhỏ, một khổng lồ.',
      'Vì thế, chiều cao kim tự tháp so với chiều cao cây gậy bằng bóng kim tự tháp so với bóng cây gậy.',
    ],
    numbers: [
      'Thử với số liệu ví dụ. Một cây gậy dài hai mét đổ bóng dài ba mét.',
      'Bóng của kim tự tháp, tính từ tâm đáy, đo được 220 mét.',
      'Chiều cao bằng 220 nhân hai, chia ba: khoảng 147 mét.',
      'Đại Kim Tự Tháp khi xây xong cao khoảng 146,6 mét. Nay lớp đá ốp ngoài đã mất, chỉ còn 138,5 mét.',
    ],
    outro: [
      'Không leo trèo. Không dây thừng. Chỉ có ánh sáng, một cây gậy và phép tỉ lệ.',
      'Thales có thật sự làm vậy không? Chưa thể chắc. Nhưng phép chứng minh này đúng với bất kỳ ai, ở bất kỳ đâu, ngay hôm nay. Đó là cách chúng ta biết.',
    ],
  },
};

export const LABELS: Record<Lang, Record<string, string>> = {
  en: {
    title: 'How Thales Measured a Pyramid',
    longShadow: 'long shadow',
    shortShadow: 'short shadow',
    halfBase: '½ base',
    measured: 'measured',
    sameShape: 'same shape',
    built: 'built: 146.6 m',
    today: 'today: 138.5 m',
    tag: 'How we know what we know.',
  },
  vi: {
    title: 'Thales đo kim tự tháp như thế nào',
    longShadow: 'bóng dài',
    shortShadow: 'bóng ngắn',
    halfBase: '½ cạnh đáy',
    measured: 'đo được',
    sameShape: 'cùng hình dạng',
    built: 'xây xong: 146,6 m',
    today: 'hiện nay: 138,5 m',
    tag: 'Chúng ta biết điều đó bằng cách nào.',
  },
};

// Tốc độ đọc ước lượng (từ/giây) để đặt thời lượng khi chưa có giọng thật.
// Khi có file giọng, thay bằng thời lượng đo được.
const WPS: Record<Lang, number> = {en: 2.5, vi: 3.0};

export const beatSeconds = (lang: Lang, text: string) => {
  if (!text) return END_SEC;
  const words = text.trim().split(/\s+/).length;
  return Math.max(2.4, words / WPS[lang] + 0.7);
};

export type Beat = {text: string; start: number; dur: number};
export type SceneTl = {id: SceneId; start: number; dur: number; beats: Beat[]; bs: number[]};

const ORDER: SceneId[] = ['intro', 'rays', 'equal', 'similar', 'numbers', 'outro'];

export function timeline(lang: Lang): {scenes: SceneTl[]; total: number; beats: Beat[]} {
  let f = 0;
  const all: Beat[] = [];
  const scenes: SceneTl[] = ORDER.map((id) => {
    const texts = id === 'outro' ? [...TEXT[lang][id], ''] : TEXT[lang][id];
    const beats: Beat[] = texts.map((text) => {
      const dur = Math.round(beatSeconds(lang, text) * FPS);
      const b = {text, start: f, dur};
      f += dur;
      all.push(b);
      return b;
    });
    const start = beats[0].start;
    return {id, start, dur: f - start, beats, bs: beats.map((b) => b.start - start)};
  });
  return {scenes, total: f, beats: all};
}
