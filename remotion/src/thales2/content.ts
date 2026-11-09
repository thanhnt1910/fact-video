import {FPS} from '../lib/theme';
import {Lang, beatSeconds} from '../thales/content';

// Video 1, bản 2 (sinh động hơn): "How Thales Measured a Pyramid"
// Có người đi, lạc đà, mặt trời lên cao, mây suy nghĩ, nhìn từ trên xuống, tam giác phóng to.
// Nguồn: xem remotion/scripts/thales.md

export type SceneId = 'hook' | 'sun' | 'equal' | 'half' | 'stick' | 'numbers' | 'outro';
export const END_SEC2 = 3.5;

export const TEXT2: Record<Lang, Record<SceneId, string[]>> = {
  en: {
    hook: [
      'Ancient writers tell a story about Thales, a Greek thinker who lived about 2,600 years ago.',
      'He stood before the Great Pyramid of Egypt and asked: how tall is it?',
      'No ladder was tall enough. No rope could reach the top. So how do you measure what you cannot climb?',
    ],
    sun: [
      'Thales had one tool: the Sun.',
      'You know this from your own shadow. When the Sun is low, your shadow is long.',
      'When the Sun climbs higher, your shadow gets shorter. The shadow changes because the angle of the sunlight changes.',
      'And at one moment of the day, your shadow is exactly as long as you are tall.',
    ],
    equal: [
      'The old story says Thales waited for exactly that moment.',
      "Why? The Sun lights him and the pyramid at the same angle. So the pyramid's shadow must also match the pyramid's height.",
      "So he only had to measure the pyramid's shadow on the ground. That length is the height.",
    ],
    half: [
      "There is one catch. The shadow starts at the pyramid's edge, but the height stands above its middle.",
      'Seen from above, the middle is half a base-width away from the edge.',
      'So the height is the shadow we measure, plus half of the base.',
    ],
    stick: [
      'But what if the Sun never gives you that perfect moment?',
      "Plutarch tells of another trick: stand a stick upright at the tip of the pyramid's shadow.",
      'Sunlight arrives in parallel rays, so it leans at the same angle on the stick and on the pyramid.',
      'That makes two triangles with the same shape, one small and one huge. Blow the small one up, and it fits exactly over the big one.',
      'So their sides keep the same proportion: the pyramid is as many times taller than the stick as its shadow is longer than the stick\'s shadow.',
    ],
    numbers: [
      'Try it with example numbers. A two-meter stick casts a three-meter shadow.',
      'So every two meters of height comes with three meters of shadow.',
      "The pyramid's shadow, from the center of its base, measures 220 meters. That is 220 times two, divided by three: about 147 meters.",
      'The Great Pyramid was built about 146.6 meters tall. Today, with its outer casing gone, it stands 138.5.',
    ],
    outro: [
      'No climbing. No rope. Just sunlight, a stick, and proportion.',
      'Did Thales really do it? We cannot be sure. But the method works for anyone, anywhere, today. That is how we know.',
    ],
  },
  vi: {
    hook: [
      'Các tác giả cổ đại kể về Thales, một nhà tư tưởng Hy Lạp sống cách đây khoảng 2.600 năm.',
      'Ông đứng trước Đại Kim Tự Tháp ở Ai Cập và tự hỏi: nó cao bao nhiêu?',
      'Không có thang nào đủ dài. Không có sợi dây nào với tới đỉnh. Vậy làm sao đo được thứ mình không leo lên được?',
    ],
    sun: [
      'Thales chỉ có một dụng cụ: Mặt Trời.',
      'Bạn biết điều này từ chính cái bóng của mình. Khi Mặt Trời còn thấp, bóng của bạn rất dài.',
      'Khi Mặt Trời lên cao hơn, bóng ngắn lại. Bóng thay đổi vì góc của ánh nắng thay đổi.',
      'Và có một lúc trong ngày, bóng của bạn dài đúng bằng chiều cao của bạn.',
    ],
    equal: [
      'Chuyện xưa kể rằng Thales chờ đúng lúc đó.',
      'Vì sao? Vì Mặt Trời chiếu vào ông và vào kim tự tháp theo cùng một góc. Nên bóng của kim tự tháp cũng dài bằng chiều cao của nó.',
      'Vậy ông chỉ cần đo bóng của kim tự tháp trên mặt đất. Độ dài đó chính là chiều cao.',
    ],
    half: [
      'Nhưng có một điểm vướng. Bóng bắt đầu từ mép kim tự tháp, còn chiều cao nằm phía trên tâm của nó.',
      'Nhìn từ trên xuống, tâm cách mép đúng nửa cạnh đáy.',
      'Vì vậy chiều cao bằng phần bóng ta đo được, cộng thêm nửa cạnh đáy.',
    ],
    stick: [
      'Nhưng nếu Mặt Trời không bao giờ cho ta khoảnh khắc hoàn hảo đó thì sao?',
      'Plutarch kể về một mẹo khác: cắm một cây gậy thẳng đứng ngay đầu bóng của kim tự tháp.',
      'Ánh nắng đến theo các tia song song, nên nó nghiêng cùng một góc trên cây gậy và trên kim tự tháp.',
      'Như vậy ta có hai tam giác cùng hình dạng, một nhỏ, một khổng lồ. Phóng to tam giác nhỏ lên, nó khớp đúng với tam giác lớn.',
      'Nên các cạnh có cùng tỉ lệ: kim tự tháp cao hơn cây gậy bao nhiêu lần thì bóng của nó dài hơn bóng cây gậy bấy nhiêu lần.',
    ],
    numbers: [
      'Thử với số liệu ví dụ. Một cây gậy dài hai mét đổ bóng dài ba mét.',
      'Vậy cứ hai mét chiều cao thì đi kèm ba mét bóng.',
      'Bóng của kim tự tháp, tính từ tâm đáy, đo được 220 mét. Lấy 220 nhân hai rồi chia ba: khoảng 147 mét.',
      'Đại Kim Tự Tháp khi xây xong cao khoảng 146,6 mét. Nay lớp đá ốp ngoài đã mất, chỉ còn 138,5 mét.',
    ],
    outro: [
      'Không leo trèo. Không dây thừng. Chỉ có ánh nắng, một cây gậy và phép tỉ lệ.',
      'Thales có thật sự làm vậy không? Chưa thể chắc. Nhưng cách đo này đúng với bất kỳ ai, ở bất kỳ đâu, ngay hôm nay. Đó là cách chúng ta biết.',
    ],
  },
};

export const LABELS2: Record<Lang, Record<string, string>> = {
  en: {
    title: 'How Thales Measured a Pyramid',
    halfBase: '½ base',
    measured: 'measured',
    angle: 'angle',
    sameAngle: 'same angle',
    sameShape: 'same shape',
    ratio: 'shadow : height = 3 : 2',
    built: 'built: 146.6 m',
    today: 'today: 138.5 m',
    scale: '(not to scale)',
    tag: 'How we know what we know.',
  },
  vi: {
    title: 'Thales đo kim tự tháp như thế nào',
    halfBase: '½ cạnh đáy',
    measured: 'đo được',
    angle: 'góc',
    sameAngle: 'cùng một góc',
    sameShape: 'cùng hình dạng',
    ratio: 'bóng : cao = 3 : 2',
    built: 'xây xong: 146,6 m',
    today: 'hiện nay: 138,5 m',
    scale: '(không đúng tỉ lệ)',
    tag: 'Chúng ta biết điều đó bằng cách nào.',
  },
};

export type Beat2 = {text: string; start: number; dur: number};
export type SceneTl2 = {id: SceneId; start: number; dur: number; beats: Beat2[]; bs: number[]};
const ORDER: SceneId[] = ['hook', 'sun', 'equal', 'half', 'stick', 'numbers', 'outro'];

export function timeline2(lang: Lang): {scenes: SceneTl2[]; total: number; beats: Beat2[]} {
  let f = 0;
  const all: Beat2[] = [];
  const scenes: SceneTl2[] = ORDER.map((id) => {
    const texts = id === 'outro' ? [...TEXT2[lang][id], ''] : TEXT2[lang][id];
    const beats: Beat2[] = texts.map((text) => {
      const dur = Math.round((text ? beatSeconds(lang, text) : END_SEC2) * FPS);
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
