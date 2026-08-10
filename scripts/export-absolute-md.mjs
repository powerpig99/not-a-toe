#!/usr/bin/env node
/**
 * Project a post for external paste (Substack, X Article, etc.).
 * Source of truth stays relative in content/posts/.
 *
 * Usage:
 *   node scripts/export-absolute-md.mjs <slug>
 *   node scripts/export-absolute-md.mjs <slug> --stdout
 *   node scripts/export-absolute-md.mjs <slug> -o path/to/out.md
 *
 * Absolute markdown only → open in MacDown → copy rendered preview.
 * No HTML export. No RTF clipboard. Site HTML is public/ via build.mjs only.
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
  console.error(`Usage: node scripts/export-absolute-md.mjs <slug> [options]

Options:
  --stdout          Write absolute markdown to stdout
  -o <file>         Write absolute markdown to path
  -h, --help        This help

Default: write export/<slug>.md with absolute links. Open in MacDown and copy the
rendered preview for Substack / X Article paste (plain markdown does not auto-render).

Paste path only: absolute .md. No --html, no --rich. Site pages are public/ via build only.
X Articles API (publish-x-article.mjs) is parked — see docs/export-for-x-article.md.
`);
  process.exit(1);
}

const args = process.argv.slice(2);
if (args.length === 0 || args.includes('-h') || args.includes('--help')) usage();

if (args.includes('--html') || args.includes('--rich') || args.includes('--no-title')) {
  console.error('Removed flags: --html, --rich, --no-title.');
  console.error('Paste path: node scripts/export-absolute-md.mjs <slug> → open MacDown → copy preview.');
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

const source = fs.readFileSync(srcPath, 'utf8');
const projected = toAbsoluteMarkdown(source);

function printMeta() {
  console.error(`Source: content/posts/${slug}.md`);
  console.error(`Cover:  ${SITE_BASE}covers/${slug}.jpg`);
  console.error(`Live:   ${SITE_BASE}posts/${slug}/`);
}

if (stdout) {
  process.stdout.write(projected);
  process.exit(0);
}

const outPath = outArg || path.join(defaultOutDir, `${slug}.md`);
fs.mkdirSync(path.dirname(outPath), { recursive: true });
fs.writeFileSync(outPath, projected.endsWith('\n') ? projected : `${projected}\n`);
console.log(`Wrote ${path.relative(root, outPath)} (absolute markdown; source unchanged).`);
printMeta();
console.log(`Tip: open in MacDown and copy the rendered preview:  open -a MacDown ${path.relative(root, outPath)}`);
