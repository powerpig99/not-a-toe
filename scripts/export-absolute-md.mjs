#!/usr/bin/env node
/**
 * Project a post's relative internal links to absolute site URLs for external paste
 * (Substack, email, etc.). Source of truth stays relative in content/posts/.
 *
 * Usage:
 *   node scripts/export-absolute-md.mjs <slug>
 *   node scripts/export-absolute-md.mjs <slug> --stdout
 *   node scripts/export-absolute-md.mjs <slug> -o path/to/out.md
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const SITE_BASE = 'https://powerpig99.github.io/not-a-toe/';
const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const root = path.join(scriptDir, '..');
const postsDir = path.join(root, 'content', 'posts');
const defaultOutDir = path.join(root, 'export');

function usage() {
  console.error(`Usage: node scripts/export-absolute-md.mjs <slug> [--stdout | -o <file>]`);
  process.exit(1);
}

function toAbsoluteMarkdown(md, baseUrl = SITE_BASE) {
  const base = baseUrl.endsWith('/') ? baseUrl : `${baseUrl}/`;
  return md.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (full, text, href) => {
    const target = href.trim();
    if (/^https?:\/\//i.test(target) || target.startsWith('mailto:') || target.startsWith('#')) {
      return full;
    }
    // Internal post links: ../slug/ or ./slug/
    const rel = target.replace(/^\.\//, '').replace(/^\.\.\//, '').replace(/\/$/, '');
    if (!rel || rel.includes('://') || rel.startsWith('/')) {
      // Site-root absolute path without host
      if (target.startsWith('/')) {
        const clean = target.replace(/^\/+/, '');
        return `[${text}](${new URL(clean, base).toString()})`;
      }
      return full;
    }
    // Treat bare or ../ relative as post slug
    const url = new URL(`posts/${rel}/`, base).toString();
    return `[${text}](${url})`;
  });
}

const args = process.argv.slice(2);
if (args.length === 0 || args.includes('-h') || args.includes('--help')) usage();

const slug = args[0].replace(/\.md$/, '');
const srcPath = path.join(postsDir, `${slug}.md`);
if (!fs.existsSync(srcPath)) {
  console.error(`Post not found: content/posts/${slug}.md`);
  process.exit(1);
}

const source = fs.readFileSync(srcPath, 'utf8');
const projected = toAbsoluteMarkdown(source);

const stdout = args.includes('--stdout');
const oIdx = args.indexOf('-o');
let outPath = null;
if (oIdx !== -1) {
  outPath = args[oIdx + 1];
  if (!outPath) usage();
} else if (!stdout) {
  fs.mkdirSync(defaultOutDir, { recursive: true });
  outPath = path.join(defaultOutDir, `${slug}.md`);
}

if (stdout) {
  process.stdout.write(projected);
} else {
  fs.writeFileSync(outPath, projected.endsWith('\n') ? projected : `${projected}\n`);
  console.log(`Wrote ${path.relative(root, outPath)} (absolute links; source unchanged).`);
  console.log(`Source: content/posts/${slug}.md`);
  console.log(`Cover:  ${SITE_BASE}covers/${slug}.jpg`);
  console.log(`Live:   ${SITE_BASE}posts/${slug}/`);
}
