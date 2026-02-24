#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';

const SITE = {
  title: 'Not a ToE',
  description: 'Not a ToE - rewritten from the ground up.',
  baseUrl: 'https://powerpig99.github.io/not-a-toe/',
  language: 'en-US',
  images: {
    og: 'images/card.jpg',
    twitter: 'images/card-twitter.jpg',
  },
};

const WORDS_PER_MINUTE = 265;
const EXCERPT_LIMIT = 300;

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const contentDir = path.join(scriptDir, 'content', 'posts');
const staticDir = path.join(scriptDir, 'static');
const outputDir = path.join(scriptDir, 'public');
const styleFile = path.join(scriptDir, 'style.css');

const baseUrl = new URL(SITE.baseUrl);
const basePath = baseUrl.pathname.replace(/\/$/, '');

function withBase(relativePath = '') {
  const clean = relativePath.replace(/^\/+/, '');
  if (!basePath) {
    return clean ? `/${clean}` : '/';
  }
  return clean ? `${basePath}/${clean}` : `${basePath}/`;
}

function absoluteUrl(relativePath = '') {
  return new URL(withBase(relativePath), SITE.baseUrl).toString();
}

function escapeHtml(text) {
  return text
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;');
}

function escapeAttribute(text) {
  return escapeHtml(text);
}

function decodeBasicEntities(text) {
  return text
    .replaceAll('&amp;', '&')
    .replaceAll('&lt;', '<')
    .replaceAll('&gt;', '>')
    .replaceAll('&quot;', '"')
    .replaceAll('&#39;', "'");
}

function applyEmphasis(text) {
  return text
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    .replace(/(?<!\*)\*([^*]+)\*(?!\*)/g, '<em>$1</em>');
}

function renderTextSegment(rawText) {
  let output = '';
  let cursor = 0;
  const linkRegex = /\[([^\]]+)\]\(([^)\s]+)\)/g;
  let match;

  while ((match = linkRegex.exec(rawText)) !== null) {
    const [full, label, href] = match;
    const start = match.index;

    if (start > cursor) {
      const before = rawText.slice(cursor, start);
      output += applyEmphasis(escapeHtml(before));
    }

    output += `<a href="${escapeAttribute(href)}">${applyEmphasis(escapeHtml(label))}</a>`;
    cursor = start + full.length;
  }

  if (cursor < rawText.length) {
    output += applyEmphasis(escapeHtml(rawText.slice(cursor)));
  }

  return output;
}

function formatInline(text) {
  const parts = text.split(/(`[^`]+`)/g);
  return parts
    .map((part) => {
      if (part.startsWith('`') && part.endsWith('`') && part.length >= 2) {
        return `<code>${escapeHtml(part.slice(1, -1))}</code>`;
      }
      return renderTextSegment(part);
    })
    .join('');
}

function markdownToHtml(markdownBody) {
  const lines = markdownBody.split(/\r?\n/);
  const chunks = [];

  let paragraph = [];
  let listType = null;
  let listItems = [];
  let quoteLines = [];

  function flushParagraph() {
    if (!paragraph.length) return;
    chunks.push(`<p>${formatInline(paragraph.join(' '))}</p>`);
    paragraph = [];
  }

  function flushList() {
    if (!listType || !listItems.length) return;
    const items = listItems.map((item) => `<li>${formatInline(item)}</li>`).join('');
    chunks.push(`<${listType}>${items}</${listType}>`);
    listType = null;
    listItems = [];
  }

  function flushQuote() {
    if (!quoteLines.length) return;
    chunks.push(`<blockquote><p>${formatInline(quoteLines.join(' '))}</p></blockquote>`);
    quoteLines = [];
  }

  function flushAll() {
    flushParagraph();
    flushList();
    flushQuote();
  }

  for (const line of lines) {
    const trimmed = line.trim();

    if (!trimmed) {
      flushAll();
      continue;
    }

    const hrMatch = /^(-{3,}|\*{3,}|_{3,})$/.test(trimmed);
    if (hrMatch) {
      flushAll();
      chunks.push('<hr>');
      continue;
    }

    const headingMatch = /^(#{1,6})\s+(.+)$/.exec(trimmed);
    if (headingMatch) {
      flushAll();
      const level = headingMatch[1].length;
      chunks.push(`<h${level}>${formatInline(headingMatch[2].trim())}</h${level}>`);
      continue;
    }

    const quoteMatch = /^>\s?(.*)$/.exec(trimmed);
    if (quoteMatch) {
      flushParagraph();
      flushList();
      quoteLines.push(quoteMatch[1]);
      continue;
    }

    const unorderedMatch = /^-\s+(.+)$/.exec(trimmed);
    if (unorderedMatch) {
      flushParagraph();
      flushQuote();
      if (listType && listType !== 'ul') {
        flushList();
      }
      listType = 'ul';
      listItems.push(unorderedMatch[1]);
      continue;
    }

    const orderedMatch = /^\d+\.\s+(.+)$/.exec(trimmed);
    if (orderedMatch) {
      flushParagraph();
      flushQuote();
      if (listType && listType !== 'ol') {
        flushList();
      }
      listType = 'ol';
      listItems.push(orderedMatch[1]);
      continue;
    }

    flushList();
    flushQuote();
    paragraph.push(trimmed);
  }

  flushAll();
  return chunks.join('\n');
}

function getGitDate(filePath) {
  const result = spawnSync('git', ['log', '-1', '--format=%cI', '--', filePath], {
    cwd: scriptDir,
    encoding: 'utf8',
  });

  const date = result.stdout.trim();
  if (result.status === 0 && date) {
    return date;
  }

  return fs.statSync(filePath).mtime.toISOString();
}

function formatDate(dateIso) {
  const date = new Date(dateIso);
  return new Intl.DateTimeFormat('en-US', {
    month: 'long',
    day: 'numeric',
    year: 'numeric',
  }).format(date);
}

function toPlainText(html) {
  const withoutTags = html.replace(/<[^>]+>/g, ' ');
  return decodeBasicEntities(withoutTags).replace(/\s+/g, ' ').trim();
}

function buildExcerpt(text, limit = EXCERPT_LIMIT) {
  if (text.length <= limit) {
    return text;
  }

  const partial = text.slice(0, limit);
  const boundary = Math.max(partial.lastIndexOf('. '), partial.lastIndexOf('! '), partial.lastIndexOf('? '));
  if (boundary > 120) {
    return partial.slice(0, boundary + 1).trim();
  }

  const space = partial.lastIndexOf(' ');
  return `${partial.slice(0, space > 0 ? space : limit).trim()}...`;
}

function wordCount(text) {
  return text.split(/\s+/).filter(Boolean).length;
}

function readPosts() {
  const files = fs
    .readdirSync(contentDir)
    .filter((file) => file.endsWith('.md'))
    .sort((a, b) => a.localeCompare(b));

  return files.map((fileName) => {
    const fullPath = path.join(contentDir, fileName);
    const slug = path.basename(fileName, '.md');
    const source = fs.readFileSync(fullPath, 'utf8').replace(/^\uFEFF/, '');
    const lines = source.split(/\r?\n/);

    if (!lines.length || !lines[0].startsWith('# ')) {
      throw new Error(`Invalid post title format in ${fileName}: first line must be '# Title'.`);
    }

    const title = lines[0].slice(2).trim();
    if (!title) {
      throw new Error(`Invalid post title in ${fileName}: title cannot be empty.`);
    }

    const markdownBody = lines.slice(1).join('\n').trimStart();
    const htmlBody = markdownToHtml(markdownBody);
    const plainText = toPlainText(htmlBody);
    const dateIso = getGitDate(fullPath);
    const words = wordCount(plainText);

    return {
      slug,
      title,
      dateIso,
      dateDisplay: formatDate(dateIso),
      readingTime: Math.max(1, Math.ceil(words / WORDS_PER_MINUTE)),
      htmlBody,
      plainText,
      excerpt: buildExcerpt(plainText),
      description: buildExcerpt(plainText, 220),
      markdownSource: source.endsWith('\n') ? source : `${source}\n`,
      outputPath: `posts/${slug}/`,
      sourcePath: path.join('content', 'posts', fileName),
    };
  });
}

function sortPosts(posts) {
  return posts
    .sort((a, b) => {
      if (a.dateIso !== b.dateIso) return b.dateIso.localeCompare(a.dateIso);
      return a.slug.localeCompare(b.slug);
    });
}

function renderPage({ title, description, content, canonicalPath, ogType = 'website', ogImagePath = SITE.images.og }) {
  const fullTitle = title ? `${title} | ${SITE.title}` : SITE.title;
  const canonicalUrl = absoluteUrl(canonicalPath);
  const ogImage = absoluteUrl(ogImagePath);

  return `<!doctype html>
<html lang="${SITE.language}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="index,follow">
  <title>${escapeHtml(fullTitle)}</title>
  <meta name="description" content="${escapeAttribute(description)}">
  <link rel="canonical" href="${escapeAttribute(canonicalUrl)}">
  <link rel="stylesheet" href="${withBase('style.css')}">
  <meta property="og:title" content="${escapeAttribute(fullTitle)}">
  <meta property="og:description" content="${escapeAttribute(description)}">
  <meta property="og:type" content="${escapeAttribute(ogType)}">
  <meta property="og:url" content="${escapeAttribute(canonicalUrl)}">
  <meta property="og:site_name" content="${escapeAttribute(SITE.title)}">
  <meta property="og:locale" content="${escapeAttribute(SITE.language)}">
  <meta property="og:image" content="${escapeAttribute(ogImage)}">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="${escapeAttribute(fullTitle)}">
  <meta name="twitter:description" content="${escapeAttribute(description)}">
  <meta name="twitter:image" content="${escapeAttribute(absoluteUrl(SITE.images.twitter))}">
</head>
<body>
  <header class="site-header">
    <div class="wrap">
      <a class="site-title" href="${withBase('')}">${escapeHtml(SITE.title)}</a>
      <a class="site-link" href="${withBase('llms.txt')}">LLMS</a>
    </div>
  </header>
  <main class="wrap">
${content}
  </main>
  <footer class="site-footer">
    <div class="wrap">
      <p>${escapeHtml(SITE.title)} · Markdown essays for humans and LLMs.</p>
    </div>
  </footer>
</body>
</html>
`;
}

function renderIndex(posts) {
  const cards = posts
    .map((post) => {
      return `    <article class="post-card">
      <h2><a href="${withBase(post.outputPath)}">${escapeHtml(post.title)}</a></h2>
      <p class="meta"><time datetime="${escapeAttribute(post.dateIso)}">${escapeHtml(post.dateDisplay)}</time> · ${post.readingTime} min read</p>
      <p>${escapeHtml(post.excerpt)}</p>
    </article>`;
    })
    .join('\n');

  const content = `    <section class="hero">
      <h1>${escapeHtml(SITE.title)}</h1>
      <p>${escapeHtml(SITE.description)}</p>
      <p class="hero-links"><a href="${withBase('llms.txt')}">llms.txt</a> · <a href="${withBase('llms-full.txt')}">llms-full.txt</a></p>
    </section>
    <section class="post-list">
${cards}
    </section>`;

  return renderPage({
    title: '',
    description: SITE.description,
    content,
    canonicalPath: '',
  });
}

function renderPost(post, newerPost, olderPost) {
  const navLinks = [];
  if (newerPost) {
    navLinks.push(`<a class="nav-link" href="${withBase(newerPost.outputPath)}">← ${escapeHtml(newerPost.title)}</a>`);
  }
  if (olderPost) {
    navLinks.push(`<a class="nav-link" href="${withBase(olderPost.outputPath)}">${escapeHtml(olderPost.title)} →</a>`);
  }

  const navHtml = navLinks.length ? `<nav class="post-nav">${navLinks.join('')}</nav>` : '';

  const content = `    <article class="essay">
      <header class="essay-header">
        <h1>${escapeHtml(post.title)}</h1>
        <p class="meta"><time datetime="${escapeAttribute(post.dateIso)}">${escapeHtml(post.dateDisplay)}</time> · ${post.readingTime} min read</p>
        <p class="essay-tools"><a href="./essay.md">Raw Markdown</a></p>
      </header>
      <div class="essay-content">
${post.htmlBody}
      </div>
      ${navHtml}
    </article>`;

  return renderPage({
    title: post.title,
    description: post.description || SITE.description,
    content,
    canonicalPath: post.outputPath,
    ogType: 'article',
  });
}

function xmlEscape(text) {
  return text
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&apos;');
}

function generateSitemap(posts) {
  const urls = [
    absoluteUrl(''),
    absoluteUrl('llms.txt'),
    absoluteUrl('llms-full.txt'),
    ...posts.map((post) => absoluteUrl(post.outputPath)),
  ];

  const rows = urls.map((url) => `  <url><loc>${xmlEscape(url)}</loc></url>`).join('\n');
  return `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${rows}
</urlset>
`;
}

function generateLlmsTxt(posts) {
  const lines = [
    `# ${SITE.title}`,
    `> ${SITE.description}`,
    '',
    '## Essays',
  ];

  for (const post of posts) {
    lines.push(`- [${post.title}](${absoluteUrl(post.outputPath)}): ${post.description}`);
  }

  lines.push('');
  lines.push(`Full corpus: ${absoluteUrl('llms-full.txt')}`);
  return `${lines.join('\n')}\n`;
}

function generateLlmsFull(posts) {
  const sections = [`# ${SITE.title}`, `> ${SITE.description}`, ''];

  for (const post of posts) {
    sections.push(`## ${post.title}`);
    sections.push(`URL: ${absoluteUrl(post.outputPath)}`);
    sections.push(`Date: ${post.dateDisplay}`);
    sections.push(`Reading time: ${post.readingTime} min`);
    sections.push('');
    sections.push(post.markdownSource.trimEnd());
    sections.push('');
    sections.push('---');
    sections.push('');
  }

  return `${sections.join('\n')}\n`;
}

function cleanPublicDir() {
  fs.rmSync(outputDir, { recursive: true, force: true });
  fs.mkdirSync(outputDir, { recursive: true });
}

function writeFile(relativePath, contents) {
  const fullPath = path.join(outputDir, relativePath);
  fs.mkdirSync(path.dirname(fullPath), { recursive: true });
  fs.writeFileSync(fullPath, contents, 'utf8');
}

function copyStaticAssets() {
  if (fs.existsSync(staticDir)) {
    fs.cpSync(staticDir, outputDir, { recursive: true });
  }

  if (!fs.existsSync(styleFile)) {
    throw new Error('style.css not found.');
  }

  fs.copyFileSync(styleFile, path.join(outputDir, 'style.css'));
}

function build() {
  cleanPublicDir();
  copyStaticAssets();

  const posts = sortPosts(readPosts());

  writeFile('index.html', renderIndex(posts));

  posts.forEach((post, index) => {
    const newer = index > 0 ? posts[index - 1] : null;
    const older = index < posts.length - 1 ? posts[index + 1] : null;

    writeFile(path.join(post.outputPath, 'index.html'), renderPost(post, newer, older));
    writeFile(path.join(post.outputPath, 'essay.md'), post.markdownSource);
  });

  writeFile('llms.txt', generateLlmsTxt(posts));
  writeFile('llms-full.txt', generateLlmsFull(posts));
  writeFile('sitemap.xml', generateSitemap(posts));
  writeFile('robots.txt', `User-agent: *\nAllow: /\nSitemap: ${absoluteUrl('sitemap.xml')}\n`);
}

try {
  build();
  console.log(`Built ${withBase('')} from ${path.relative(scriptDir, contentDir)}.`);
} catch (error) {
  console.error(error.message);
  process.exit(1);
}
