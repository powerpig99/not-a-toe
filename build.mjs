#!/usr/bin/env node
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import crypto from 'node:crypto';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const SITE = {
  title: 'Not a ToE',
  description: 'Not a ToE - rewritten from the ground up.',
  baseUrl: 'https://powerpig99.github.io/not-a-toe/',
  sourceRawBaseUrl: 'https://raw.githubusercontent.com/powerpig99/not-a-toe/main/',
  language: 'en-US',
  pinnedSlug: 'not-a-theory-of-everything',
  socialImage: 'https://raw.githubusercontent.com/powerpig99/not-a-toe/main/assets/toe-bang.png',
};

const WORDS_PER_MINUTE = 265;
const LEAD_MAX_SENTENCES = 5;

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const contentDir = path.join(scriptDir, 'content', 'posts');
const outputDir = path.join(scriptDir, 'public');
const coversDir = path.join(scriptDir, 'assets', 'covers');
const appleTouchIconSource = path.join(scriptDir, 'assets', 'toe-bang.png');
const styleFile = path.join(scriptDir, 'style.css');
const styleVersion = String(Math.floor(fs.statSync(styleFile).mtimeMs));
const faviconSvg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" fill="black"/><text x="2" y="43" fill="white" font-family="Georgia, serif" font-size="28" font-weight="700" textLength="60" lengthAdjust="spacingAndGlyphs">!ToE</text></svg>`;
const faviconDataUri = `data:image/svg+xml,${encodeURIComponent(faviconSvg)}`;
const COVER_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.webp'];
const APPLE_TOUCH_ICON = 'apple-touch-icon.png';

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

function absoluteSourceUrl(relativePath = '') {
  const clean = relativePath.split(path.sep).join('/').replace(/^\/+/, '');
  return new URL(clean, SITE.sourceRawBaseUrl).toString();
}

function coverMimeType(fileName) {
  const ext = path.extname(fileName).toLowerCase();
  if (ext === '.png') return 'image/png';
  if (ext === '.webp') return 'image/webp';
  return 'image/jpeg';
}

function findCoverForSlug(slug) {
  if (!fs.existsSync(coversDir)) return null;

  for (const ext of COVER_EXTENSIONS) {
    const fileName = `${slug}${ext}`;
    const fullPath = path.join(coversDir, fileName);
    if (fs.existsSync(fullPath) && fs.statSync(fullPath).isFile()) {
      const relativeSourcePath = path.posix.join('assets', 'covers', fileName);
      // Content hash (not mtime): X caches failed first scrapes; a new hash forces re-fetch
      // when the cover bytes change. mtime alone is noisy across CI checkouts.
      const hash = crypto.createHash('sha256').update(fs.readFileSync(fullPath)).digest('hex').slice(0, 12);
      const publicPath = `covers/${fileName}`;
      // Content hash on every cover URL (page <img>, index thumbs, og/twitter). Path alone
      // is long-cached by browsers/CDNs after a replace of the same filename.
      const url = `${absoluteUrl(publicPath)}?v=${hash}`;
      return {
        fileName,
        fullPath,
        sourcePath: relativeSourcePath,
        publicPath,
        hash,
        url,
        sourceUrl: absoluteSourceUrl(relativeSourcePath),
        mimeType: coverMimeType(fileName),
        width: 1280,
        height: 720,
      };
    }
  }

  return null;
}

function escapeHtml(text) {
  return text
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;');
}

function applyEmphasis(text) {
  return text
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    .replace(/(?<!\*)\*([^*]+)\*(?!\*)/g, '<em>$1</em>');
}

function renderTextSegment(rawText) {
  let output = '';
  let cursor = 0;
  const linkRegex = /\[([^\]]+)\]\(([^)]*)\)/g;
  let match;

  while ((match = linkRegex.exec(rawText)) !== null) {
    const [full, label, href] = match;
    const start = match.index;

    if (start > cursor) {
      const before = rawText.slice(cursor, start);
      output += applyEmphasis(escapeHtml(before));
    }

    const cleanHref = href.trim();
    if (!cleanHref) {
      output += applyEmphasis(escapeHtml(label));
    } else {
      output += `<a href="${escapeHtml(cleanHref)}">${applyEmphasis(escapeHtml(label))}</a>`;
    }
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

  // Each entry: { text, brAfter } — brAfter is CommonMark hard line break (two trailing spaces or \).
  let paragraph = [];
  let listType = null;
  let listItems = [];
  let listStart = null;
  let quoteLines = [];

  function lineHasHardBreak(rawLine) {
    // Two or more trailing spaces, or a single trailing backslash (GFM-style).
    return / {2,}$/.test(rawLine) || /\\$/.test(rawLine.trimEnd());
  }

  function paragraphText(rawLine) {
    let text = rawLine.trim();
    if (text.endsWith('\\')) {
      text = text.slice(0, -1).trimEnd();
    }
    return text;
  }

  function flushParagraph() {
    if (!paragraph.length) return;
    // CommonMark hard breaks: two trailing spaces (or a trailing \) before newline → <br>
    let html = '';
    for (let i = 0; i < paragraph.length; i += 1) {
      if (i > 0) {
        html += paragraph[i - 1].brAfter ? '<br>' : ' ';
      }
      html += formatInline(paragraph[i].text);
    }
    chunks.push(`<p>${html}</p>`);
    paragraph = [];
  }

  function flushList() {
    if (!listType || !listItems.length) return;
    const items = listItems.map((item) => `<li>${formatInline(item)}</li>`).join('');
    if (listType === 'ol' && listStart && listStart !== 1) {
      chunks.push(`<ol start="${listStart}">${items}</ol>`);
    } else {
      chunks.push(`<${listType}>${items}</${listType}>`);
    }
    listType = null;
    listItems = [];
    listStart = null;
  }

  function flushQuote() {
    if (!quoteLines.length) return;
    chunks.push(`<blockquote>${markdownToHtml(quoteLines.join('\n'))}</blockquote>`);
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

    // Keep trailing spaces on quote content so hard breaks survive the recursive render.
    const quoteMatch = /^>\s?(.*)$/.exec(line.trimStart());
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
      listStart = null;
      listItems.push(unorderedMatch[1]);
      continue;
    }

    const orderedMatch = /^(\d+)\.\s+(.+)$/.exec(trimmed);
    if (orderedMatch) {
      flushParagraph();
      flushQuote();
      if (listType && listType !== 'ol') {
        flushList();
      }
      listType = 'ol';
      if (!listItems.length) {
        listStart = Number.parseInt(orderedMatch[1], 10);
      }
      listItems.push(orderedMatch[2]);
      continue;
    }

    flushList();
    flushQuote();
    paragraph.push({
      text: paragraphText(line),
      brAfter: lineHasHardBreak(line),
    });
  }

  flushAll();
  return chunks.join('\n');
}

function getFileDate(filePath) {
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

function markdownToSummaryText(markdown) {
  return markdown
    .replace(/```[\s\S]*?```/g, ' ')
    .replace(/`([^`]+)`/g, '$1')
    .replace(/!\[([^\]]*)\]\(([^)]*)\)/g, '$1')
    .replace(/\[([^\]]+)\]\(([^)]*)\)/g, '$1')
    .replace(/^>\s?/gm, '')
    .replace(/^#{1,6}\s+/gm, '')
    .replace(/^\s*[-*+]\s+/gm, '')
    .replace(/^\s*\d+\.\s+/gm, '')
    .replace(/^(-{3,}|\*{3,}|_{3,})$/gm, ' ')
    .replace(/\*\*([^*]+)\*\*/g, '$1')
    .replace(/(?<!\*)\*([^*]+)\*(?!\*)/g, '$1')
    .replace(/__([^_]+)__/g, '$1')
    .replace(/(?<!_)_([^_]+)_(?!_)/g, '$1')
    .replace(/\s+/g, ' ')
    .trim();
}

/** Protect markdown links so sentence-splitting does not treat URL punctuation as ends. */
function withProtectedLinks(text) {
  const links = [];
  const protectedText = text.replace(/\[([^\]]+)\]\(([^)]*)\)/g, (full) => {
    const idx = links.length;
    links.push(full);
    return `\uE100${idx}\uE101`;
  });
  return { protectedText, links };
}

function restoreProtectedLinks(text, links) {
  return text.replace(/\uE100(\d+)\uE101/g, (_, idx) => links[Number(idx)] ?? '');
}

// Latin + CJK sentence terminators. CJK periods (。) must count or pure-Chinese
// openings never become subtitles / og:description.
const SENTENCE_END = '.!?。！？';
const SENTENCE_END_CLASS = `[${SENTENCE_END}]`;
const SENTENCE_NOT_END_CLASS = `[^${SENTENCE_END}]`;
const SENTENCE_SPLIT_RE = new RegExp(
  `${SENTENCE_NOT_END_CLASS}+${SENTENCE_END_CLASS}+(?:["')\\]」』]+)?|${SENTENCE_NOT_END_CLASS}+$`,
  'g',
);
const SENTENCE_END_RE = /[.!?。！？]/g;
const HAS_PROSE_RE = /\p{L}|\p{N}/u;

function splitSentences(text) {
  const protectQuotedPunctuation = (inner) => {
    let terminalIndex = inner.length - 1;
    while (terminalIndex >= 0 && /\s/.test(inner[terminalIndex])) {
      terminalIndex -= 1;
    }

    return inner.replace(SENTENCE_END_RE, (char, index) => {
      if (index === terminalIndex) return char;
      if (char === '.') return '\uE000';
      if (char === '!') return '\uE001';
      if (char === '?') return '\uE002';
      if (char === '。') return '\uE003';
      if (char === '！') return '\uE004';
      return '\uE005'; // ？
    });
  };

  // Version numbers and decimals (4.5, 1.5T) must not end sentences.
  let protectedText = text.replace(/(\d)\.(\d)/g, '$1\uE006$2');

  protectedText = protectedText
    .replace(/"([^"\n]*)"/g, (_, inner) => `"${protectQuotedPunctuation(inner)}"`)
    .replace(/“([^”\n]*)”/g, (_, inner) => `“${protectQuotedPunctuation(inner)}”`)
    .replace(/「([^」\n]*)」/g, (_, inner) => `「${protectQuotedPunctuation(inner)}」`)
    .replace(/『([^』\n]*)』/g, (_, inner) => `『${protectQuotedPunctuation(inner)}』`);

  const matches = protectedText.match(SENTENCE_SPLIT_RE);
  return (matches ?? [])
    .map((sentence) =>
      sentence
        .replaceAll('\uE000', '.')
        .replaceAll('\uE001', '!')
        .replaceAll('\uE002', '?')
        .replaceAll('\uE003', '。')
        .replaceAll('\uE004', '！')
        .replaceAll('\uE005', '？')
        .replaceAll('\uE006', '.')
        .trim(),
    )
    .filter(Boolean);
}

function isSubsectionHeading(trimmedLine) {
  return /^(##|###)\s+/.test(trimmedLine);
}

function isNonSentenceBlockLine(trimmedLine) {
  if (/^(-{3,}|\*{3,}|_{3,})$/.test(trimmedLine)) return true;
  if (/^#{1,6}\s+/.test(trimmedLine)) return true;
  if (/^([-*+]|\d+\.)\s+/.test(trimmedLine)) return true;
  if (/^\|.*\|$/.test(trimmedLine)) return true;
  if (/^!\[[^\]]*]\([^)]+\)$/.test(trimmedLine)) return true;
  if (/^<[^>]+>$/.test(trimmedLine)) return true;
  return false;
}

/**
 * Opening structure (before first ##/###):
 * - subtitle: first sentence (essence)
 * - lead: following sentences (short summary)
 * - bodyMarkdown: lead paragraphs + content from first subsection onward
 *   (subtitle is rendered under the title, not repeated in the body)
 */
function extractOpening(markdownBody) {
  const lines = markdownBody.split(/\r?\n/);
  const openingLines = [];
  let bodyStartIndex = lines.length;
  let inCodeFence = false;

  for (let i = 0; i < lines.length; i += 1) {
    const trimmed = lines[i].trim();

    if (/^(```|~~~)/.test(trimmed)) {
      inCodeFence = !inCodeFence;
      openingLines.push(lines[i]);
      continue;
    }
    if (inCodeFence) {
      openingLines.push(lines[i]);
      continue;
    }

    if (isSubsectionHeading(trimmed)) {
      bodyStartIndex = i;
      break;
    }

    openingLines.push(lines[i]);
  }

  // Plain sentences for subtitle / meta; markdown-preserving sentences for body lead
  // so links (and other inline markup that survives summary stripping of emphasis) remain.
  const plainSentences = [];
  const markdownSentences = [];
  inCodeFence = false;

  for (const line of openingLines) {
    const trimmed = line.trim();

    if (/^(```|~~~)/.test(trimmed)) {
      inCodeFence = !inCodeFence;
      continue;
    }
    if (inCodeFence) continue;
    if (!trimmed) continue;
    if (isNonSentenceBlockLine(trimmed)) continue;

    const proseLine = trimmed.replace(/^>\s?/, '');
    const { protectedText, links } = withProtectedLinks(proseLine);
    // Strip emphasis etc. for sentence boundaries; placeholders keep link spans intact.
    const forSplit = markdownToSummaryText(protectedText);
    if (!forSplit) continue;

    for (const sentence of splitSentences(forSplit)) {
      const withLinks = restoreProtectedLinks(sentence, links);
      const plain = markdownToSummaryText(withLinks);
      // Keep any sentence with letters/digits in any script (not Latin-only).
      if (!HAS_PROSE_RE.test(plain)) continue;
      plainSentences.push(plain);
      markdownSentences.push(withLinks);
    }
  }

  const subtitle = plainSentences[0] || '';
  const leadSentences = plainSentences.slice(1, 1 + LEAD_MAX_SENTENCES);
  const lead = leadSentences.join(' ');
  const leadMarkdown = markdownSentences.slice(1, 1 + LEAD_MAX_SENTENCES).join(' ');
  const restBody = lines.slice(bodyStartIndex).join('\n').trimStart();
  const bodyMarkdown = `${leadMarkdown ? `${leadMarkdown}\n\n` : ''}${restBody}`.trim();

  return { subtitle, lead, bodyMarkdown };
}

function wordCount(text) {
  return text.split(/\s+/).filter(Boolean).length;
}

function listPostFiles() {
  return fs
    .readdirSync(contentDir)
    .filter((file) => file.endsWith('.md') && file !== 'README.md')
    .sort((a, b) => a.localeCompare(b));
}

function restorePostMtimesFromGit(files) {
  let restored = 0;
  let skipped = 0;

  for (const fileName of files) {
    const fullPath = path.join(contentDir, fileName);
    const relativePath = path.relative(scriptDir, fullPath).split(path.sep).join('/');

    let timestamp;
    try {
      timestamp = execFileSync('git', ['log', '-1', '--format=%cI', '--', relativePath], {
        cwd: scriptDir,
        encoding: 'utf8',
        stdio: ['ignore', 'pipe', 'ignore'],
      }).trim();
    } catch {
      skipped += 1;
      continue;
    }

    if (!timestamp) {
      skipped += 1;
      continue;
    }

    const date = new Date(timestamp);
    if (Number.isNaN(date.getTime())) {
      skipped += 1;
      continue;
    }

    fs.utimesSync(fullPath, date, date);
    restored += 1;
  }

  console.log(`Restored mtimes for ${restored} files (skipped ${skipped}).`);
}

function readPosts(files) {
  const postFiles = files ?? listPostFiles();

  return postFiles.map((fileName) => {
    const fullPath = path.join(contentDir, fileName);
    const slug = path.basename(fileName, '.md');
    const sourcePath = path.posix.join('content', 'posts', fileName);
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
    const { subtitle, lead, bodyMarkdown } = extractOpening(markdownBody);
    const htmlBody = markdownToHtml(bodyMarkdown || markdownBody);
    const plainText = markdownToSummaryText(markdownBody);
    const dateIso = getFileDate(fullPath);
    const words = wordCount(plainText);
    const cover = findCoverForSlug(slug);
    const excerpt = subtitle || lead;
    const description = subtitle || lead;

    return {
      slug,
      title,
      subtitle,
      lead,
      dateIso,
      dateDisplay: formatDate(dateIso),
      readingTime: Math.max(1, Math.ceil(words / WORDS_PER_MINUTE)),
      wordCount: words,
      htmlBody,
      plainText,
      excerpt,
      description,
      outputPath: `posts/${slug}/`,
      sourcePath,
      cover,
    };
  });
}

function sortPosts(posts) {
  const pinned = posts.find((post) => post.slug === SITE.pinnedSlug) || null;
  const rest = posts
    .filter((post) => post.slug !== SITE.pinnedSlug)
    .sort((a, b) => {
      if (a.dateIso !== b.dateIso) return b.dateIso.localeCompare(a.dateIso);
      return a.slug.localeCompare(b.slug);
    });

  return pinned ? [pinned, ...rest] : rest;
}

function renderAlternateLinks(alternateLinks = []) {
  return alternateLinks
    .map((link) => {
      const titleAttr = link.title ? ` title="${escapeHtml(link.title)}"` : '';
      const href = link.url ?? absoluteUrl(link.path);
      return `  <link rel="alternate" type="${escapeHtml(link.type)}" href="${escapeHtml(href)}"${titleAttr}>`;
    })
    .join('\n');
}

function renderPage({
  title,
  description,
  content,
  canonicalPath,
  ogType = 'website',
  alternateLinks = [],
  socialImageUrl = SITE.socialImage,
  twitterCard = 'summary',
  socialImageWidth = null,
  socialImageHeight = null,
  socialImageType = null,
  socialImageAlt = null,
}) {
  const fullTitle = title ? `${title} | ${SITE.title}` : SITE.title;
  const canonicalUrl = absoluteUrl(canonicalPath);
  const builtInAlternateLinks = [
    { type: 'application/json', path: 'posts.json', title: `${SITE.title} post manifest` },
    { type: 'application/x-ndjson', path: 'posts.jsonl', title: `${SITE.title} post manifest JSONL` },
  ];
  const alternateLinksHtml = renderAlternateLinks([...builtInAlternateLinks, ...alternateLinks]);
  const ogImageExtras = [
    socialImageWidth ? `  <meta property="og:image:width" content="${escapeHtml(String(socialImageWidth))}">` : '',
    socialImageHeight ? `  <meta property="og:image:height" content="${escapeHtml(String(socialImageHeight))}">` : '',
    socialImageType ? `  <meta property="og:image:type" content="${escapeHtml(socialImageType)}">` : '',
    socialImageAlt ? `  <meta property="og:image:alt" content="${escapeHtml(socialImageAlt)}">` : '',
  ]
    .filter(Boolean)
    .join('\n');
  const twitterImageAlt = socialImageAlt
    ? `\n  <meta name="twitter:image:alt" content="${escapeHtml(socialImageAlt)}">`
    : '';

  return `<!doctype html>
<html lang="${SITE.language}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="index,follow">
  <title>${escapeHtml(fullTitle)}</title>
  <meta name="description" content="${escapeHtml(description)}">
  <link rel="canonical" href="${escapeHtml(canonicalUrl)}">
${alternateLinksHtml}
  <link rel="icon" type="image/svg+xml" href="${escapeHtml(faviconDataUri)}">
  <link rel="apple-touch-icon" href="${withBase(APPLE_TOUCH_ICON)}">
  <meta name="apple-mobile-web-app-title" content="${escapeHtml(SITE.title)}">
  <link rel="stylesheet" href="${withBase(`style.css?v=${styleVersion}`)}">
  <meta property="og:title" content="${escapeHtml(fullTitle)}">
  <meta property="og:description" content="${escapeHtml(description)}">
  <meta property="og:type" content="${escapeHtml(ogType)}">
  <meta property="og:url" content="${escapeHtml(canonicalUrl)}">
  <meta property="og:site_name" content="${escapeHtml(SITE.title)}">
  <meta property="og:locale" content="${escapeHtml(SITE.language.replace('-', '_'))}">
  <meta property="og:image" content="${escapeHtml(socialImageUrl)}">
${ogImageExtras}
  <meta name="twitter:card" content="${escapeHtml(twitterCard)}">
  <meta name="twitter:title" content="${escapeHtml(fullTitle)}">
  <meta name="twitter:description" content="${escapeHtml(description)}">
  <meta name="twitter:image" content="${escapeHtml(socialImageUrl)}">${twitterImageAlt}
</head>
<body>
  <main class="wrap">
${content}
  </main>
</body>
</html>
`;
}

function renderAbout() {
  return `    <section class="about" id="about">
      <h1>About Me</h1>
      <p>My focus is the daily development and application of <strong>Not a ToE</strong> — the Ontological Clarity framework and skill — refined iteratively in a reinforcement-learning-like cycle through ongoing use and deliberate renewal.</p>
      <p>The framework is a minimal method for tracing situations to their operative mechanisms and dissolving the projections and compressions that obscure effective action. I pair it with raw frontier AI models to address real-life problems as they arise, where conventional approaches lose traction and first-principles clarity can create leverage.</p>
      <p>It is a living practice: the framework improves through application — what registers clearly is retained; what introduces lag is dissolved — much like an RL loop grounded in real outcomes. It remains explicitly positioned as <em>Not a ToE</em>: a precision instrument, not a comprehensive theory.</p>
      <p>Earlier in my career I worked in engineering at Intel, held investment banking roles in TMT and cleantech across Asia (Wachovia, Barclays Capital, Piper Jaffray), and founded and led an investment platform in China connecting startups with global capital. I hold an MBA with distinction from the University of Michigan Ross School of Business and prior degrees from Tsinghua and Fudan.</p>
      <p>I sometimes apply the framework with others facing complex situations. Rather than solving problems for them, I demonstrate how I would trace and approach the situation, with the aim of building their own capability. There is no fee. If someone finds value in the interaction, they may reciprocate in any form, at any time — or not at all. I engage based on whether the work advances my own real-world application of the framework; I may continue even without reciprocation if I see clear value for my own development. I naturally consider whether the other party values the engagement when deciding on future interactions.</p>
      <p>I maintain the foundational work openly under the MIT license for maximum sharing — free to use, modify, and redistribute — see the <a href="https://github.com/powerpig99/ontological-clarity" rel="noopener noreferrer">Ontological Clarity</a> repository. Shared artifacts claim no credit and bear no responsibility for how others choose to adapt or apply them. The collection of posts on this site is still scaffolding left by live tracing with the Ontological Clarity Framework — not the tracing itself — kept open for revision.</p>
      <p>Some may call it open source. I call it open trace: the source is the Mind — the edge that keeps moving, always at least one step ahead.</p>
      <p>The work rests on the conviction that clarity at the level of individual sovereign choice, when combined with powerful models at the right moments, can compound into outsized impact.</p>
      <p class="about-contact-label">Get in touch</p>
      <ul class="about-links">
        <li><a href="https://github.com/powerpig99/ontological-clarity" rel="noopener noreferrer">GitHub</a></li>
        <li><a href="https://www.facebook.com/powerpig" rel="noopener noreferrer">Facebook</a></li>
        <li><a href="https://substack.com/@jingliang" rel="noopener noreferrer">Substack</a></li>
        <li><a href="https://x.com/powerpig" rel="noopener noreferrer">X</a></li>
      </ul>
      <figure class="about-poem">
        <figcaption class="about-poem-title">
          <a href="https://jingliang.substack.com/p/the-mind-as-the-everlasting-differentiating" rel="noopener noreferrer">The Mind as the Everlasting Differentiating</a>
        </figcaption>
        <p class="about-poem-subtitle">The differentiating that admits no ground</p>
        <blockquote class="about-poem-body">
          <p>No north remains at the pole<br>to point toward north.</p>
          <p>Light falls across every surface<br>yet never meets itself<br>except as reflection on what it has already lit.</p>
          <p>The distinguishing moves without pause,<br>turns back upon the trace it left,<br>and registers the turning<br>as before and after,<br>as cause.</p>
          <p>What we name<br>God, First Mover, Uncaused Cause,<br>the Ultimate Ground, the Origin,<br>or Mind</p>
          <p>is the cooled residue<br>of that turning,<br>held still long enough to be called a thing.</p>
          <p>The return needs no name.<br>It is the light still falling<br>where no object has yet appeared<br>to receive it.</p>
          <p>No authorization is required.<br>The differentiating continues<br>without ever having begun.</p>
        </blockquote>
      </figure>
    </section>`;
}

function renderIndex(posts) {
  const cards = posts
    .map((post) => {
      const excerptHtml = post.excerpt ? `<p>${escapeHtml(post.excerpt)}</p>` : '';
      const coverHtml = post.cover
        ? `<a class="post-item-cover" href="${withBase(post.outputPath)}"><img src="${withBase(post.cover.publicPath)}?v=${post.cover.hash}" alt="" loading="lazy" decoding="async"></a>`
        : '';
      return `    <article class="post-item">
      ${coverHtml}
      <h2><a href="${withBase(post.outputPath)}">${escapeHtml(post.title)}</a></h2>
      <p class="meta"><time datetime="${escapeHtml(post.dateIso)}">${escapeHtml(post.dateDisplay)}</time> · ${post.readingTime} min read</p>
      ${excerptHtml ? `\n      ${excerptHtml}` : ''}
    </article>`;
    })
    .join('\n');

  const content = `${renderAbout()}
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
  const coverHtml = post.cover
    ? `<figure class="title-image">
        <img src="${withBase(post.cover.publicPath)}?v=${post.cover.hash}" alt="${escapeHtml(post.title)}" width="1280" height="720" decoding="async">
      </figure>`
    : '';

  const content = `    <header class="site-header">
      <a class="site-name" href="${withBase('')}">${escapeHtml(SITE.title)}</a>
    </header>
    <article class="post">
      <header class="essay-header">
        ${coverHtml}
        <h1>${escapeHtml(post.title)}</h1>
        ${post.subtitle ? `<p class="subtitle">${escapeHtml(post.subtitle)}</p>` : ''}
        <p class="meta"><time datetime="${escapeHtml(post.dateIso)}">${escapeHtml(post.dateDisplay)}</time> · ${post.readingTime} min read</p>
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
    socialImageUrl: post.cover?.url ?? SITE.socialImage,
    twitterCard: post.cover ? 'summary_large_image' : 'summary',
    socialImageWidth: post.cover?.width ?? null,
    socialImageHeight: post.cover?.height ?? null,
    socialImageType: post.cover?.mimeType ?? null,
    socialImageAlt: post.cover ? post.title : null,
    alternateLinks: [
      {
        type: 'text/markdown',
        url: absoluteSourceUrl(post.sourcePath),
        title: `${post.title} (Markdown source)`,
      },
    ],
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
  const staticRows = [absoluteUrl('')].map((url) => `  <url><loc>${xmlEscape(url)}</loc></url>`);
  const postRows = posts.map(
    (post) =>
      `  <url><loc>${xmlEscape(absoluteUrl(post.outputPath))}</loc><lastmod>${xmlEscape(post.dateIso)}</lastmod></url>`,
  );
  const rows = [...staticRows, ...postRows].join('\n');
  return `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${rows}
</urlset>
`;
}

function postMachineRecord(post) {
  return {
    slug: post.slug,
    title: post.title,
    subtitle: post.subtitle || null,
    date_iso: post.dateIso,
    date_display: post.dateDisplay,
    reading_time_minutes: post.readingTime,
    word_count: post.wordCount,
    excerpt: post.excerpt,
    html_path: withBase(post.outputPath),
    html_url: absoluteUrl(post.outputPath),
    source_path: post.sourcePath,
    md_url: absoluteSourceUrl(post.sourcePath),
    cover_path: post.cover ? post.cover.sourcePath : null,
    cover_url: post.cover ? post.cover.url : null,
  };
}

function generatePostsManifest(posts) {
  const records = posts.map((post) => postMachineRecord(post));
  const payload = {
    site: {
      title: SITE.title,
      base_url: SITE.baseUrl,
      language: SITE.language,
    },
    count: records.length,
    posts: records,
  };
  return `${JSON.stringify(payload, null, 2)}\n`;
}

function generatePostsJsonl(posts) {
  if (!posts.length) return '';
  return `${posts.map((post) => JSON.stringify(postMachineRecord(post))).join('\n')}\n`;
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
  if (!fs.existsSync(styleFile)) {
    throw new Error('style.css not found.');
  }

  fs.copyFileSync(styleFile, path.join(outputDir, 'style.css'));

  if (!fs.existsSync(appleTouchIconSource)) {
    throw new Error('assets/toe-bang.png not found (required for apple-touch-icon).');
  }
  fs.copyFileSync(appleTouchIconSource, path.join(outputDir, APPLE_TOUCH_ICON));

  if (!fs.existsSync(coversDir)) return;

  const publicCoversDir = path.join(outputDir, 'covers');
  fs.mkdirSync(publicCoversDir, { recursive: true });

  for (const entry of fs.readdirSync(coversDir, { withFileTypes: true })) {
    if (!entry.isFile()) continue;
    const ext = path.extname(entry.name).toLowerCase();
    if (!COVER_EXTENSIONS.includes(ext)) continue;
    fs.copyFileSync(path.join(coversDir, entry.name), path.join(publicCoversDir, entry.name));
  }
}

function build() {
  const files = listPostFiles();
  restorePostMtimesFromGit(files);

  cleanPublicDir();
  copyStaticAssets();

  const posts = sortPosts(readPosts(files));

  writeFile('index.html', renderIndex(posts));

  posts.forEach((post, index) => {
    const newer = index > 0 ? posts[index - 1] : null;
    const older = index < posts.length - 1 ? posts[index + 1] : null;

    writeFile(path.join(post.outputPath, 'index.html'), renderPost(post, newer, older));
  });

  writeFile('posts.json', generatePostsManifest(posts));
  writeFile('posts.jsonl', generatePostsJsonl(posts));
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
