// news-image-20261119 — entry program.
//
// The entry is the finished front page, entry.png, drawn by
// build_image.py and committed next to this file. This program
// copies it to the output directory and checks it before the
// grader sees it: the file must exist, stay under the 1 MiB cap,
// and measure exactly 1024 by 1024 pixels. A copy is byte for
// byte identical on every run, so the two grading runs agree.
//
// Run:  MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));
const SOURCE = join(HERE, "entry.png");
const OUT_DIR = process.env.MAKEFUN_OUTPUT_DIR || "out";
const OUT = join(OUT_DIR, "entry.png");
const MAX_BYTES = 1048576;
const WANT_W = 1024;
const WANT_H = 1024;

function fail(message) {
  console.error(`main.ts: ${message}`);
  process.exit(1);
}

// Read the width and height of a JPEG from its frame header.
// Walks the markers until a start-of-frame block gives the size.
function jpegSize(buf) {
  if (buf[0] !== 0xff || buf[1] !== 0xd8 || buf[2] !== 0xff) {
    return null;
  }
  let off = 2;
  while (off + 9 < buf.length) {
    if (buf[off] !== 0xff) return null;
    const marker = buf[off + 1];
    const len = buf.readUInt16BE(off + 2);
    if (marker >= 0xc0 && marker <= 0xcf && marker !== 0xc4
        && marker !== 0xc8 && marker !== 0xcc) {
      const height = buf.readUInt16BE(off + 5);
      const width = buf.readUInt16BE(off + 7);
      return { width, height };
    }
    off += 2 + len;
  }
  return null;
}

// Read the width and height of a PNG from its IHDR chunk.
function pngSize(buf) {
  const magic = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
  for (let i = 0; i < magic.length; i++) {
    if (buf[i] !== magic[i]) return null;
  }
  return {
    width: buf.readUInt32BE(16),
    height: buf.readUInt32BE(20),
  };
}

// The file is a JPEG in a .png name (or a real PNG): tell them apart
// by their first bytes, never by the extension.
function imageSize(buf) {
  return jpegSize(buf) ?? pngSize(buf);
}

function main() {
  let buf;
  try {
    buf = readFileSync(SOURCE);
  } catch {
    fail(`cannot read ${SOURCE}`);
  }
  const size = imageSize(buf);
  if (size === null) {
    fail("entry.png is neither a JPEG nor a PNG");
  }
  if (size.width !== WANT_W || size.height !== WANT_H) {
    fail(`entry.png is ${size.width}x${size.height}, want 1024x1024`);
  }
  if (buf.length >= MAX_BYTES) {
    fail(`entry.png is ${buf.length} bytes, over the 1 MiB cap`);
  }
  mkdirSync(OUT_DIR, { recursive: true });
  copyFileSync(SOURCE, OUT);
  const written = statSync(OUT).size;
  if (written !== buf.length) {
    fail(`copy is ${written} bytes, source is ${buf.length}`);
  }
  console.log(
    `main.ts: wrote ${OUT} (${size.width}x${size.height}, `
    + `${written} bytes)`,
  );
}

main();
