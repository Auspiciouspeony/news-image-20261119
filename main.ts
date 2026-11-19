// news-image-20261119 — Thursday 19 November 2026 front page (Node 22).
//
// The entry is the image build_image.py draws and saves as entry.png
// beside this file. This program copies those exact bytes to the
// grader's output file, so both runs produce identical output, then
// verifies the copy before exiting: it must be a valid JPEG, exactly
// 1024x1024, under 1 MiB, and byte-identical to the source. A bad copy
// fails loudly instead of silently grading a broken image.
//
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync, statSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const EXPECTED_WIDTH = 1024;
const EXPECTED_HEIGHT = 1024;
const MAX_BYTES = 1024 * 1024;

function fail(message) {
  console.error(`main.ts: verification failed: ${message}`);
  process.exit(1);
}

// Read a JPEG's width and height from its SOF0/SOF1/SOF2 segment.
function jpegDimensions(buf) {
  if (buf.length < 4 || buf[0] !== 0xff || buf[1] !== 0xd8) {
    fail('not a JPEG (missing SOI marker)');
  }
  let offset = 2;
  while (offset + 3 < buf.length) {
    if (buf[offset] !== 0xff) fail(`bad JPEG marker at offset ${offset}`);
    const marker = buf[offset + 1];
    if (marker === 0xd9) break; // EOI: no SOF found
    if (marker === 0x01 || (marker >= 0xd0 && marker <= 0xd7)) {
      offset += 2; // standalone marker, no length field
      continue;
    }
    const length = buf.readUInt16BE(offset + 2);
    if (length < 2 || offset + 2 + length > buf.length) {
      fail(`truncated JPEG segment at offset ${offset}`);
    }
    if (marker === 0xc0 || marker === 0xc1 || marker === 0xc2) {
      const height = buf.readUInt16BE(offset + 5);
      const width = buf.readUInt16BE(offset + 7);
      return { width, height };
    }
    if (marker === 0xda) break; // SOS: scan data follows, SOF must precede it
    offset += 2 + length;
  }
  fail('no JPEG SOF segment found');
}

const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, 'entry.png');
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
const dest = join(outDir, 'entry.png');
copyFileSync(src, dest);

const srcBytes = readFileSync(src);
const outBytes = readFileSync(dest);
const outSize = statSync(dest).size;
if (outSize >= MAX_BYTES) {
  fail(`output is ${outSize} bytes, must be under 1 MiB`);
}
if (outBytes.length < 2 || outBytes[outBytes.length - 2] !== 0xff || outBytes[outBytes.length - 1] !== 0xd9) {
  fail('output is truncated (missing JPEG EOI marker)');
}
const { width, height } = jpegDimensions(outBytes);
if (width !== EXPECTED_WIDTH || height !== EXPECTED_HEIGHT) {
  fail(`output is ${width}x${height}, expected ${EXPECTED_WIDTH}x${EXPECTED_HEIGHT}`);
}
const srcHash = createHash('sha256').update(srcBytes).digest('hex');
const outHash = createHash('sha256').update(outBytes).digest('hex');
if (srcHash !== outHash) fail('output bytes differ from entry.png');
console.log(`main.ts: verified entry.png ${width}x${height}, ${outSize} bytes, sha256 ${outHash.slice(0, 12)}...`);
