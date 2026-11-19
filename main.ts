// v6 entrypoint for make.fun news-image-20261119.
// Copies the pre-rendered entry.png (a JPEG) to the output directory
// and verifies it is 1024x1024 and under 1 MiB, so both graded runs
// write exactly the same bytes. Standard library only, no network.
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const src = readFileSync(join(here, "entry.png"));

if (src[0] !== 0xff || src[1] !== 0xd8) {
  throw new Error("entry.png is not a JPEG");
}
if (src.length >= 1048576) {
  throw new Error(`entry.png is ${src.length} bytes, over the 1 MiB cap`);
}

// Walk the JPEG markers to the first frame header (SOF0/SOF2) and read
// its height and width (big-endian, 2 bytes each).
let width = 0;
let height = 0;
let i = 2;
while (i + 9 < src.length) {
  if (src[i] !== 0xff) {
    throw new Error("bad JPEG marker");
  }
  const marker = src[i + 1];
  if (marker === 0xd8 || (marker >= 0xd0 && marker <= 0xd9) || marker === 0x01) {
    i += 2;
    continue;
  }
  const segLen = src.readUInt16BE(i + 2);
  if (marker >= 0xc0 && marker <= 0xcf && marker !== 0xc4 && marker !== 0xc8 && marker !== 0xcc) {
    height = src.readUInt16BE(i + 5);
    width = src.readUInt16BE(i + 7);
    break;
  }
  i += 2 + segLen;
}
if (width !== 1024 || height !== 1024) {
  throw new Error(`entry.png is ${width}x${height}, expected 1024x1024`);
}

mkdirSync(outDir, { recursive: true });
writeFileSync(join(outDir, "entry.png"), src);
console.log(`wrote entry.png: ${src.length} bytes, 1024x1024`);
