#!/usr/bin/env node
/**
 * Project a post for external paste (Substack, email, etc.).
 * Source of truth stays relative in content/posts/.
 *
 * Usage:
 *   node scripts/export-absolute-md.mjs <slug>
 *   node scripts/export-absolute-md.mjs <slug> --stdout
 *   node scripts/export-absolute-md.mjs <slug> -o path/to/out.md
 *   node scripts/export-absolute-md.mjs <slug> --rich   # optional RTF → macOS clipboard (no MacDown)
 *
 * No HTML export file. Site HTML is only public/ via build.mjs.
 */
import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
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
  --stdout          Write absolute markdown to stdout
  -o <file>         Write absolute markdown to path
  --rich            Optional: RTF → macOS clipboard (escape hatch without MacDown)
  --no-title        With --rich: drop leading H1 (Substack title field already set)
  -h, --help        This help

Default: write export/<slug>.md with absolute links. Open in MacDown and copy the
rendered preview for Substack / X Article paste (plain markdown does not auto-render).

No HTML export. Do not pass --html (removed). Site pages are public/ via build only.
--rich is optional (clipboard only; does not write export/<slug>.html).
X Articles API (publish-x-article.mjs) is parked — see docs/export-for-x-article.md.
`);
  process.exit(1);
}

const args = process.argv.slice(2);
if (args.length === 0 || args.includes('-h') || args.includes('--help')) usage();

if (args.includes('--html')) {
  console.error('HTML export is not used. Default path: absolute .md → MacDown preview paste.');
  console.error('Optional escape hatch without MacDown: --rich (RTF clipboard only).');
  process.exit(1);
}

const slug = args[0].replace(/\.md$/, '');
const srcPath = path.join(postsDir, `${slug}.md`);
if (!fs.existsSync(srcPath)) {
  console.error(`Post not found: content/posts/${slug}.md`);
  process.exit(1);
}

const wantRich = args.includes('--rich');
const noTitle = args.includes('--no-title');
const stdout = args.includes('--stdout');
const oIdx = args.indexOf('-o');
const outArg = oIdx !== -1 ? args[oIdx + 1] : null;
if (oIdx !== -1 && !outArg) usage();

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
    console.error('--rich requires macOS (textutil + pbcopy). On other OS use absolute .md + a markdown previewer.');
    process.exit(1);
  }

  const fragment = postMarkdownToHtmlFragment(projected);
  const doc = wrapHtmlDocument(fragment, title);

  // HTML → RTF on clipboard only (tmpdir unused; textutil stdin). No export/*.html.
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

  console.log(`Rich text (RTF) copied to clipboard — paste into Substack or X Article body.`);
  printMeta();
  if (noTitle) console.log('Leading H1 omitted (--no-title).');
  process.exit(0);
}

// Default: absolute markdown only
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
