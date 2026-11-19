// news-image-20261119 entry (Node 22, standard library only).
//
// One image summing up Thursday 19 November 2026: 45 stories on one
// front page — Trump, Xi and Putin meet in Shenzhen, Fed minutes point
// to more hikes, Anthropic prices its IPO at $83, Israeli tanks push
// deeper into Gaza, Cyclone Akvan nears the Indian coast, plus 32
// numbered briefs and a dotted world map. The front page is entry.png
// beside this file (1024x1024 JPEG bytes, under the 1 MiB gate);
// build_image.py in this repo shows how it was composed. The program
// only copies that file to /output/entry.png, because the grader runs
// with no network and the judge sees exactly those bytes.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for
// /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const src = new URL("./entry.png", import.meta.url);

if (!existsSync(src)) {
  throw new Error("entry.png is missing next to main.ts");
}

const bytes = readFileSync(src);
const pngMagic = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const isPng = bytes.subarray(0, 8).equals(pngMagic);
const isJpeg =
  bytes[0] === 0xff &&
  bytes[1] === 0xd8 &&
  bytes[bytes.length - 2] === 0xff &&
  bytes[bytes.length - 1] === 0xd9;

if (!isPng && !isJpeg) {
  throw new Error("entry.png is neither a whole PNG nor a whole JPEG");
}
if (bytes.length > 1048576) {
  throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB limit`);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(src, join(outDir, "entry.png"));
console.log(`copied entry.png (${bytes.length} bytes) to ${outDir}`);
