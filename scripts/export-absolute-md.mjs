#!/usr/bin/env node
/**
 * Project a post for external paste (Substack, email, etc.).
 * Source of truth stays relative in content/posts/.
 *
 * Usage:
 *   node scripts/export-absolute-md.mjs <slug>
 *   node scripts/export-absolute-md.mjs <slug> --stdout
 *   node scripts/export-absolute-md.mjs <slug> -o path/to/out.md
 *   node scripts/export-absolute-md.mjs <slug> --html          # write export/<slug>.html
 *   node scripts/export-absolute-md.mjs <slug> --rich          # rendered RTF → macOS clipboard (Substack paste)
 *   node scripts/export-absolute-md.mjs <slug> --html --stdout # HTML fragment to stdout
 */
import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  SITE_BASE,
  toAbsoluteMarkdown,
  postMarkdownToHtmlFragment,
  wrapHtmlDocument,
} from './lib/post-markdown.mjs';

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const root = path.join(scriptDir, '..');
const postsDir = path.join(root, 'content', 'posts');
const defaultOutDir = path.join(root, 'export');

function usage() {
  console.error(`Usage: node scripts/export-absolute-md.mjs <slug> [options]

Options:
  --stdout          Write to stdout (markdown unless --html)
  -o <file>         Write to path
  --html            HTML fragment (absolute links); default file export/<slug>.html
  --rich            Render to RTF and copy to macOS clipboard for Substack paste
  --no-title        With --rich/--html: drop leading H1 (Substack title field already set)
  -h, --help        This help

Substack + X Article body: use --rich (formatted paste; plain markdown does not auto-render).
X Articles API (publish-x-article.mjs) is parked — see docs/export-for-x-article.md.
`);
  process.exit(1);
}

const args = process.argv.slice(2);
if (args.length === 0 || args.includes('-h') || args.includes('--help')) usage();

const slug = args[0].replace(/\.md$/, '');
const srcPath = path.join(postsDir, `${slug}.md`);
if (!fs.existsSync(srcPath)) {
  console.error(`Post not found: content/posts/${slug}.md`);
  process.exit(1);
}

const wantHtml = args.includes('--html');
const wantRich = args.includes('--rich');
const noTitle = args.includes('--no-title');
const stdout = args.includes('--stdout');
const oIdx = args.indexOf('-o');
const outArg = oIdx !== -1 ? args[oIdx + 1] : null;
if (oIdx !== -1 && !outArg) usage();

if (wantRich && wantHtml && stdout) {
  console.error('Use either --rich (clipboard) or --html --stdout, not both.');
  process.exit(1);
}

const source = fs.readFileSync(srcPath, 'utf8');
let projected = toAbsoluteMarkdown(source);

if (noTitle) {
  projected = projected.replace(/^#\s+[^\n]+\n+/, '');
}

const titleMatch = /^#\s+(.+)$/m.exec(source);
const title = titleMatch ? titleMatch[1].trim() : slug;

function printMeta() {
  console.error(`Source: content/posts/${slug}.md`);
  console.error(`Cover:  ${SITE_BASE}covers/${slug}.jpg`);
  console.error(`Live:   ${SITE_BASE}posts/${slug}/`);
}

if (wantRich) {
  if (process.platform !== 'darwin') {
    console.error('--rich requires macOS (textutil + pbcopy). On other OS use --html and paste via a browser/editor.');
    process.exit(1);
  }

  const fragment = postMarkdownToHtmlFragment(projected);
  const doc = wrapHtmlDocument(fragment, title);
  const tmpHtml = path.join(os.tmpdir(), `not-a-toe-export-${slug}.html`);
  fs.writeFileSync(tmpHtml, doc);

  // HTML → RTF on clipboard: Substack / Docs / Word paste as formatted content.
  const conv = spawnSync(
    'textutil',
    ['-convert', 'rtf', '-stdin', '-stdout'],
    { input: doc, encoding: 'utf8', maxBuffer: 20 * 1024 * 1024 },
  );
  if (conv.status !== 0) {
    console.error(conv.stderr || 'textutil failed');
    process.exit(1);
  }
  const clip = spawnSync('pbcopy', [], { input: conv.stdout, encoding: 'utf8' });
  if (clip.status !== 0) {
    console.error(clip.stderr || 'pbcopy failed');
    process.exit(1);
  }

  // Also keep a local HTML projection for re-export / debug (gitignored export/)
  fs.mkdirSync(defaultOutDir, { recursive: true });
  const htmlPath = path.join(defaultOutDir, `${slug}.html`);
  fs.writeFileSync(htmlPath, `${fragment}\n`);

  console.log(`Rich text (RTF) copied to clipboard — paste into Substack or X Article body.`);
  console.log(`Also wrote ${path.relative(root, htmlPath)} (HTML fragment).`);
  printMeta();
  if (noTitle) console.log('Leading H1 omitted (--no-title).');
  process.exit(0);
}

if (wantHtml) {
  const fragment = postMarkdownToHtmlFragment(projected);
  if (stdout) {
    process.stdout.write(fragment.endsWith('\n') ? fragment : `${fragment}\n`);
    process.exit(0);
  }
  const outPath = outArg || path.join(defaultOutDir, `${slug}.html`);
  fs.mkdirSync(path.dirname(outPath), { recursive: true });
  fs.writeFileSync(outPath, fragment.endsWith('\n') ? fragment : `${fragment}\n`);
  console.log(`Wrote ${path.relative(root, outPath)} (HTML fragment; absolute links; source unchanged).`);
  printMeta();
  process.exit(0);
}

// Default: absolute markdown
if (stdout) {
  process.stdout.write(projected);
  process.exit(0);
}

const outPath = outArg || path.join(defaultOutDir, `${slug}.md`);
fs.mkdirSync(path.dirname(outPath), { recursive: true });
fs.writeFileSync(outPath, projected.endsWith('\n') ? projected : `${projected}\n`);
console.log(`Wrote ${path.relative(root, outPath)} (absolute markdown; source unchanged).`);
printMeta();
console.log(`Tip: for Substack / X Article paste use  node scripts/export-absolute-md.mjs ${slug} --rich --no-title`);
