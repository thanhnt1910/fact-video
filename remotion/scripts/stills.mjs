// Xuất nhiều khung hình của một video để soi bố cục.
// Dùng: node scripts/stills.mjs <IdVideo> <thư mục ra> <khung1> <khung2> ...
import path from 'node:path';
import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition} from '@remotion/renderer';

const [id, outDir, ...frames] = process.argv.slice(2);
const browserExecutable = process.env.CHROME || '/usr/bin/google-chrome';
const serveUrl = await bundle({entryPoint: path.resolve('src/index.ts')});
const comp = await selectComposition({serveUrl, id, browserExecutable});
for (const f of frames) {
  const out = path.join(outDir, `${id}_${String(f).padStart(5, '0')}.png`);
  await renderStill({composition: comp, serveUrl, output: out, frame: Number(f), browserExecutable});
  console.log('ok', out);
}
