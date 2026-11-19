// news-image-20261119 — entrypoint (Node 22, standard library only).
//
// The front page is pre-rendered by build_image.py into the entry.png
// beside this file. This program copies that image to the grader's
// output directory (MAKEFUN_OUTPUT_DIR, default /output).

import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(new URL("./entry.png", import.meta.url), join(outDir, "entry.png"));
