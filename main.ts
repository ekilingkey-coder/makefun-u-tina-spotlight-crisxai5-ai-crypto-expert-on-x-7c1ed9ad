import { copyFileSync, mkdirSync, existsSync } from 'node:fs';
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

console.log(`main: copied ${src}`);
console.log(`main: wrote destination ${dst}`);
console.log(`main: done`);
