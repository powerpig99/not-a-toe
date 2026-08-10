#!/usr/bin/env node
/**
 * Substack export: absolute-link markdown from content/posts/<slug>.md.
 *
 *   node scripts/export-absolute-md.mjs <slug>
 *   node scripts/export-absolute-md.mjs <slug> --stdout
 *   node scripts/export-absolute-md.mjs <slug> -o path/to/out.md
 *
 * Writes export/<slug>.md (gitignored). No HTML, RTF, or other modes.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { SITE_BASE, toAbsoluteMarkdown } from './lib/post-markdown.mjs';

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const root = path.join(scriptDir, '..');
const postsDir = path.join(root, 'content', 'posts');
const defaultOutDir = path.join(root, 'export');

function usage() {
  console.error(`Usage: node scripts/export-absolute-md.mjs <slug> [--stdout | -o <file>]

Substack export only: write absolute-link markdown (default: export/<slug>.md).
See docs/export-for-substack.md.
`);
  process.exit(1);
}

const args = process.argv.slice(2);
if (args.length === 0 || args.includes('-h') || args.includes('--help')) usage();

if (args.includes('--html') || args.includes('--rich') || args.includes('--no-title')) {
  console.error('Substack export is absolute markdown only. See docs/export-for-substack.md.');
  process.exit(1);
}

const slug = args[0].replace(/\.md$/, '');
const srcPath = path.join(postsDir, `${slug}.md`);
if (!fs.existsSync(srcPath)) {
  console.error(`Post not found: content/posts/${slug}.md`);
  process.exit(1);
}

const stdout = args.includes('--stdout');
const oIdx = args.indexOf('-o');
const outArg = oIdx !== -1 ? args[oIdx + 1] : null;
if (oIdx !== -1 && !outArg) usage();

const projected = toAbsoluteMarkdown(fs.readFileSync(srcPath, 'utf8'));

if (stdout) {
  process.stdout.write(projected);
  process.exit(0);
}

const outPath = outArg || path.join(defaultOutDir, `${slug}.md`);
fs.mkdirSync(path.dirname(outPath), { recursive: true });
fs.writeFileSync(outPath, projected.endsWith('\n') ? projected : `${projected}\n`);
console.log(`Wrote ${path.relative(root, outPath)} (absolute markdown for Substack).`);
console.error(`Source: content/posts/${slug}.md`);
console.error(`Live:   ${SITE_BASE}posts/${slug}/`);
