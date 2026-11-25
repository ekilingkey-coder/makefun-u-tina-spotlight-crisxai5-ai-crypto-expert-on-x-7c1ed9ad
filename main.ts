import { copyFileSync, mkdirSync, existsSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const root = process.cwd();
const src = join(root, 'POST.json');
const outDir = '/output';
const dst = join(outDir, 'POST.json');

console.log(`main: source = ${src}`);
if (!existsSync(src)) {
  console.error(`main: ERROR: source file not found: ${src}`);
  process.exit(1);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(src, dst);

const srcBytes = readFileSync(src).length;
const dstBytes = readFileSync(dst).length;
const match = srcBytes === dstBytes;

console.log(`main: copied ${src}`);
console.log(`main: wrote destination ${dst}`);
console.log(`main: source bytes=${srcBytes} destination bytes=${dstBytes} match=${match}`);
console.log(`main: done`);
