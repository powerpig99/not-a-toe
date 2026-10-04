#!/usr/bin/env node
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import crypto from 'node:crypto';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const SITE = {
  title: 'Not a ToE',
  description: '非万物之理：活的哲学——非为学理，非为布道，非为作态，非为效仿，唯在每个当下践行 / Not a ToE: A Philosophy to Live By — Not to Learn, Not to Preach, Not to Pose, Not to Emulate, but to Practice at Each and Every Moment',
  baseUrl: 'https://powerpig99.github.io/not-a-toe/',
  sourceRawBaseUrl: 'https://raw.githubusercontent.com/powerpig99/not-a-toe/main/',
  language: 'en-US',
  pinnedSlug: 'manifesto-of-not-a-theory-of-everything',
  socialImage: 'https://raw.githubusercontent.com/powerpig99/not-a-toe/main/assets/podcast-cover.jpg',
};

const WORDS_PER_MINUTE = 265;
const CJK_CHARS_PER_MINUTE = 400;
const CJK_CHAR_RE = /[\u3040-\u30ff\u3400-\u9fff\uf900-\ufaff\uac00-\ud7af]/g;
const CJK_PUNCT_RE = /[\u3000-\u303f\uff00-\uffef]/g;
const LEAD_MAX_SENTENCES = 5;

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const contentDir = path.join(scriptDir, 'content', 'posts');
const outputDir = path.join(scriptDir, 'public');
const coversDir = path.join(scriptDir, 'assets', 'covers');
const figuresDir = path.join(scriptDir, 'assets', 'figures');
const appleTouchIconSource = path.join(scriptDir, 'assets', 'toe-bang.png');
const styleFile = path.join(scriptDir, 'style.css');
const styleVersion = String(Math.floor(fs.statSync(styleFile).mtimeMs));
const faviconSvg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" fill="black"/><text x="2" y="43" fill="white" font-family="Georgia, serif" font-size="28" font-weight="700" textLength="60" lengthAdjust="spacingAndGlyphs">!ToE</text></svg>`;
const faviconDataUri = `data:image/svg+xml,${encodeURIComponent(faviconSvg)}`;
const COVER_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.webp'];
const APPLE_TOUCH_ICON = 'apple-touch-icon.png';

// Live book: structure lives only as relative links inside content/book/*.md.
// PART_ORDER is the single ordering constant; membership is read from each part's
// "## 篇目 / Essays" link list, so there is no second inventory.
const bookDir = path.join(scriptDir, 'content', 'book');
const BOOK_PREFACE_SLUG = 'preface';
const BOOK_INDEX_SLUG = 'index-of-premises';
const BOOK_ESSAYS_HEADING_RE = /^##\s+篇目\s*\/\s*Essays\s*$/;
const PART_ORDER = [
  'method',
  'causality',
  'physics',
  'mathematics',
  'life-and-statistics',
  'consciousness',
  'intelligence',
  'economics',
  'state-and-collective',
  'morality',
  'meaning-and-transcendence',
  'knowledge-and-learning',
  'success-and-the-self',
  'tools-and-progress',
];
const ROMAN = ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI'];
const ZH_NUM = ['', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '十一', '十二', '十三', '十四', '十五', '十六'];
const JOURNAL_LATEST_COUNT = 8;

const REDIRECTS = [
  {
    from: 'posts/the-deflection-of-the-vector-and-the-puzzle-of-projections',
    to: 'posts/the-vector-and-the-puzzle-of-projections'
  },
  {
    from: 'posts/wealth-is-a-settlement-invoice-not-an-engine',
    to: 'posts/the-vector-and-the-puzzle-of-projections'
  }
];

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

/** Read pixel size from JPEG / PNG / WebP without a dependency. */
function readImageSize(buf, ext) {
  const e = ext.toLowerCase();
  if ((e === '.jpg' || e === '.jpeg') && buf[0] === 0xff && buf[1] === 0xd8) {
    let i = 2;
    while (i + 9 < buf.length) {
      if (buf[i] !== 0xff) break;
      const marker = buf[i + 1];
      // SOF0 / SOF1 / SOF2
      if (marker === 0xc0 || marker === 0xc1 || marker === 0xc2) {
        return { width: buf.readUInt16BE(i + 7), height: buf.readUInt16BE(i + 5) };
      }
      if (marker === 0xd9 || marker === 0xda) break;
      const len = buf.readUInt16BE(i + 2);
      if (len < 2) break;
      i += 2 + len;
    }
  }
  if (e === '.png' && buf.length >= 24 && buf[0] === 0x89 && buf[1] === 0x50) {
    return { width: buf.readUInt32BE(16), height: buf.readUInt32BE(20) };
  }
  if (e === '.webp' && buf.length >= 30 && buf.toString('ascii', 0, 4) === 'RIFF' && buf.toString('ascii', 8, 12) === 'WEBP') {
    const fourcc = buf.toString('ascii', 12, 16);
    if (fourcc === 'VP8X' && buf.length >= 30) {
      const width = 1 + buf[24] + (buf[25] << 8) + (buf[26] << 16);
      const height = 1 + buf[27] + (buf[28] << 8) + (buf[29] << 16);
      return { width, height };
    }
    if (fourcc === 'VP8 ' && buf.length >= 30) {
      // Lossy bitstream starts at offset 20; frame tag then 3-byte width/height at 26.
      const width = buf.readUInt16LE(26) & 0x3fff;
      const height = buf.readUInt16LE(28) & 0x3fff;
      return { width, height };
    }
    if (fourcc === 'VP8L' && buf.length >= 25) {
      const b0 = buf[21];
      const b1 = buf[22];
      const b2 = buf[23];
      const b3 = buf[24];
      const width = 1 + (((b1 & 0x3f) << 8) | b0);
      const height = 1 + (((b3 & 0xf) << 10) | (b2 << 2) | ((b1 & 0xc0) >> 6));
      return { width, height };
    }
  }
  return null;
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
      const bytes = fs.readFileSync(fullPath);
      const hash = crypto.createHash('sha256').update(bytes).digest('hex').slice(0, 12);
      const publicPath = `covers/${fileName}`;
      // Content hash on every cover URL (page <img>, index thumbs, og/twitter). Path alone
      // is long-cached by browsers/CDNs after a replace of the same filename.
      const url = `${absoluteUrl(publicPath)}?v=${hash}`;
      const size = readImageSize(bytes, ext) ?? { width: 1280, height: 576 };
      return {
        fileName,
        fullPath,
        sourcePath: relativeSourcePath,
        publicPath,
        hash,
        url,
        sourceUrl: absoluteSourceUrl(relativeSourcePath),
        mimeType: coverMimeType(fileName),
        width: size.width,
        height: size.height,
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
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/(?<!\*)\*([^*]+)\*(?!\*)/g, '<em>$1</em>');
}

function formatInline(text) {
  const codeTokens = [];
  let processed = text.replace(/`([^`]+)`/g, (_full, codeContent) => {
    const idx = codeTokens.length;
    codeTokens.push(`<code>${escapeHtml(codeContent)}</code>`);
    return `\uE000${idx}\uE001`;
  });

  const linkTokens = [];
  processed = processed.replace(/\[([^\]]+)\]\(([^)]*)\)/g, (_full, label, href) => {
    const idx = linkTokens.length;
    const cleanHref = href.trim();
    const renderedLabel = applyEmphasis(escapeHtml(label));
    const html = cleanHref
      ? `<a href="${escapeHtml(cleanHref)}">${renderedLabel}</a>`
      : renderedLabel;
    linkTokens.push(html);
    return `\uE002${idx}\uE003`;
  });

  processed = applyEmphasis(escapeHtml(processed));
  processed = processed.replace(/\uE002(\d+)\uE003/g, (_m, idx) => linkTokens[Number(idx)]);
  processed = processed.replace(/\uE000(\d+)\uE001/g, (_m, idx) => codeTokens[Number(idx)]);
  return processed;
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
  let tableLines = [];
  let inCodeBlock = false;
  let codeBlockLines = [];
  let codeBlockLang = '';

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

  function flushTable() {
    if (!tableLines.length) return;
    if (tableLines.length >= 2) {
      const parseRow = (rowStr) => {
        const cells = rowStr.trim().replace(/^\|/, '').replace(/\|$/, '').split('|');
        return cells.map((c) => c.trim());
      };
      const headerCells = parseRow(tableLines[0]);
      const alignRow = parseRow(tableLines[1]);
      const aligns = alignRow.map((a) => {
        const left = a.startsWith(':');
        const right = a.endsWith(':');
        if (left && right) return 'center';
        if (right) return 'right';
        if (left) return 'left';
        return 'left';
      });

      let html = '<div class="table-wrap"><table><thead><tr>';
      for (let i = 0; i < headerCells.length; i += 1) {
        const align = aligns[i] || 'left';
        html += `<th style="text-align:${align}">${formatInline(headerCells[i])}</th>`;
      }
      html += '</tr></thead><tbody>';
      for (let r = 2; r < tableLines.length; r += 1) {
        const rowCells = parseRow(tableLines[r]);
        html += '<tr>';
        for (let i = 0; i < headerCells.length; i += 1) {
          const align = aligns[i] || 'left';
          const val = rowCells[i] || '';
          html += `<td style="text-align:${align}">${formatInline(val)}</td>`;
        }
        html += '</tr>';
      }
      html += '</tbody></table></div>';
      chunks.push(html);
    } else {
      for (const tLine of tableLines) {
        chunks.push(`<p>${formatInline(tLine)}</p>`);
      }
    }
    tableLines = [];
  }

  function flushAll() {
    flushParagraph();
    flushList();
    flushQuote();
    flushTable();
    if (inCodeBlock) {
      if (codeBlockLang === 'mermaid') {
        chunks.push(`<div class="mermaid-wrap" title="Click to zoom in"><pre class="mermaid">${escapeHtml(codeBlockLines.join('\n'))}</pre><div class="mermaid-hint"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line><line x1="11" y1="8" x2="11" y2="14"></line><line x1="8" y1="11" x2="14" y2="11"></line></svg><span>Click to zoom</span></div></div>`);
      } else {
        chunks.push(`<pre><code${codeBlockLang ? ` class="language-${escapeHtml(codeBlockLang)}"` : ''}>${escapeHtml(codeBlockLines.join('\n'))}</code></pre>`);
      }
      inCodeBlock = false;
      codeBlockLines = [];
      codeBlockLang = '';
    }
  }

  for (const line of lines) {
    const trimmed = line.trim();

    if (/^(```|~~~)/.test(trimmed)) {
      if (inCodeBlock) {
        if (codeBlockLang === 'mermaid') {
          chunks.push(`<div class="mermaid-wrap" title="Click to zoom in"><pre class="mermaid">${escapeHtml(codeBlockLines.join('\n'))}</pre><div class="mermaid-hint"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line><line x1="11" y1="8" x2="11" y2="14"></line><line x1="8" y1="11" x2="14" y2="11"></line></svg><span>Click to zoom</span></div></div>`);
        } else {
          chunks.push(`<pre><code${codeBlockLang ? ` class="language-${escapeHtml(codeBlockLang)}"` : ''}>${escapeHtml(codeBlockLines.join('\n'))}</code></pre>`);
        }
        inCodeBlock = false;
        codeBlockLines = [];
        codeBlockLang = '';
        continue;
      } else {
        flushAll();
        inCodeBlock = true;
        codeBlockLang = trimmed.replace(/^[~`]+/, '').trim();
        codeBlockLines = [];
        continue;
      }
    }

    if (inCodeBlock) {
      codeBlockLines.push(line);
      continue;
    }

    if (!trimmed) {
      flushAll();
      continue;
    }

    const isTableRow = /^\|(.+)\|$/.test(trimmed);
    if (isTableRow) {
      flushParagraph();
      flushList();
      flushQuote();
      tableLines.push(trimmed);
      continue;
    }
    flushTable();

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

    const imageMatch = /^!\[([^\]]*)\]\(([^)]+)\)$/.exec(trimmed);
    if (imageMatch) {
      flushAll();
      const alt = imageMatch[1];
      const src = imageMatch[2].trim();
      const publicSrc = /^https?:\/\//i.test(src) ? src : withBase(src.replace(/^\/+/, ''));
      chunks.push(`<figure class="body-figure"><img src="${escapeHtml(publicSrc)}" alt="${escapeHtml(alt)}" loading="lazy" decoding="async"></figure>`);
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

    const unorderedMatch = /^[-*+]\s+(.+)$/.exec(trimmed);
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

  // Check for explicit italic subtitle block at the start of openingLines
  let firstNonEmptyIdx = -1;
  for (let i = 0; i < openingLines.length; i += 1) {
    if (openingLines[i].trim()) {
      firstNonEmptyIdx = i;
      break;
    }
  }

  let hasExplicitItalicSubtitle = false;
  let subtitleEndIdx = -1;

  if (firstNonEmptyIdx !== -1) {
    const firstLine = openingLines[firstNonEmptyIdx].trim();
    // Single-line italic subtitle: *...* or _..._
    if (/^(\*|_)[^*_]+(\*|_)$/.test(firstLine)) {
      hasExplicitItalicSubtitle = true;
      subtitleEndIdx = firstNonEmptyIdx;
    } else if (/^(\*|_)/.test(firstLine)) {
      // Check multi-line italic block
      for (let j = firstNonEmptyIdx; j < openingLines.length; j += 1) {
        const lineTrim = openingLines[j].trim();
        if (!lineTrim) break;
        if (/(\*|_)$/.test(lineTrim)) {
          hasExplicitItalicSubtitle = true;
          subtitleEndIdx = j;
          break;
        }
      }
    }
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

  let subtitle = '';
  let bodyMarkdown = '';

  if (hasExplicitItalicSubtitle) {
    const subtitleRaw = openingLines.slice(firstNonEmptyIdx, subtitleEndIdx + 1).join(' ').trim();
    subtitle = markdownToSummaryText(subtitleRaw);
    const openingBody = openingLines.slice(subtitleEndIdx + 1).join('\n').trim();
    const restBody = lines.slice(bodyStartIndex).join('\n').trim();
    bodyMarkdown = [openingBody, restBody].filter(Boolean).join('\n\n').trim();
  } else {
    subtitle = plainSentences[0] || '';
    const leadMarkdown = markdownSentences.slice(1).join(' ');
    const restBody = lines.slice(bodyStartIndex).join('\n').trimStart();
    bodyMarkdown = `${leadMarkdown ? `${leadMarkdown}\n\n` : ''}${restBody}`.trim();
  }

  const leadSentences = plainSentences.slice(1, 1 + LEAD_MAX_SENTENCES);
  const lead = leadSentences.join(' ');

  return { subtitle, lead, bodyMarkdown };
}

function readingUnits(text) {
  const cjkChars = (text.match(CJK_CHAR_RE) || []).length;
  const latinWords = text
    .replace(CJK_CHAR_RE, ' ')
    .replace(CJK_PUNCT_RE, ' ')
    .split(/\s+/)
    .filter(Boolean).length;
  return { cjkChars, latinWords, units: cjkChars + latinWords };
}

function readingTimeMinutes({ cjkChars, latinWords }) {
  // If post contains substantial content in both CJK and Latin (parallel bilingual post),
  // readers read one language, so take the max duration instead of summing them.
  const isBilingual = cjkChars >= 1000 && latinWords >= 1000;
  if (isBilingual) {
    return Math.max(1, Math.ceil(Math.max(cjkChars / CJK_CHARS_PER_MINUTE, latinWords / WORDS_PER_MINUTE)));
  }
  return Math.max(1, Math.ceil(cjkChars / CJK_CHARS_PER_MINUTE + latinWords / WORDS_PER_MINUTE));
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
    const units = readingUnits(plainText);
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
      readingTime: readingTimeMinutes(units),
      wordCount: units.units,
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
  return [...posts].sort((a, b) => {
    if (a.dateIso !== b.dateIso) return b.dateIso.localeCompare(a.dateIso);
    return a.slug.localeCompare(b.slug);
  });
}

/* ------------------------------------------------------------------ */
/* Live book                                                           */
/* ------------------------------------------------------------------ */

function splitBilingual(text) {
  const idx = text.indexOf(' / ');
  if (idx === -1) return { zh: text, en: '' };
  return { zh: text.slice(0, idx).trim(), en: text.slice(idx + 3).trim() };
}

function bookPostSlugFromHref(href) {
  const m = /^\.\.\/\.\.\/posts\/([A-Za-z0-9][A-Za-z0-9_-]*)\/?(#.*)?$/.exec(href.trim());
  return m ? m[1] : null;
}

/** Book pages are authored with relative links (../../posts/x/, ../part/); rebase for any render location. */
function rebaseBookMarkdown(markdown) {
  return markdown
    .replace(/\]\(\.\.\/\.\.\/posts\//g, `](${withBase('posts/')}`)
    .replace(/\]\(\.\.\/(?!\.)/g, `](${withBase('book/')}`);
}

function anchorId(text) {
  return text
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

function sortKey(text) {
  return text
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/^[^A-Za-z0-9]+/, '')
    .toLowerCase();
}

function partLabel(part) {
  if (part.number === 0) return { zh: '序', en: 'Preface' };
  return { zh: `第${ZH_NUM[part.number]}部`, en: `Part ${ROMAN[part.number]}` };
}

function readBookFile(slug) {
  const fullPath = path.join(bookDir, `${slug}.md`);
  if (!fs.existsSync(fullPath)) {
    throw new Error(`Book file missing: content/book/${slug}.md`);
  }
  const source = fs.readFileSync(fullPath, 'utf8').replace(/^\uFEFF/, '');
  const lines = source.split(/\r?\n/);
  if (!lines[0].startsWith('# ')) {
    throw new Error(`Invalid book title format in content/book/${slug}.md: first line must be '# Title'.`);
  }
  return { slug, title: lines[0].slice(2).trim(), lines: lines.slice(1) };
}

function readPremiseIndex(postsBySlug, errors) {
  const { title, lines } = readBookFile(BOOK_INDEX_SLUG);
  const sections = [];
  const introLines = [];
  let section = null;
  let entry = null;

  const finishEntry = () => {
    if (!entry) return;
    if (!entry.links.length) errors.push(`Index entry "${entry.title}" has no post link.`);
    if (!entry.paras.length) errors.push(`Index entry "${entry.title}" has no premise sentence.`);
    section.entries.push(entry);
    entry = null;
  };

  for (const raw of lines) {
    const line = raw.trim();
    const h2 = /^##\s+(.+)$/.exec(line);
    const h3 = /^###\s+(.+)$/.exec(line);
    if (h2 && !h3) {
      finishEntry();
      const names = splitBilingual(h2[1].trim());
      section = { title: h2[1].trim(), ...names, id: anchorId(names.en || names.zh), entries: [] };
      sections.push(section);
      continue;
    }
    if (h3) {
      if (!section) {
        errors.push(`Index entry "${h3[1]}" appears before any section heading.`);
        continue;
      }
      finishEntry();
      const names = splitBilingual(h3[1].trim());
      entry = { title: h3[1].trim(), ...names, id: anchorId(names.en || names.zh), label: '', paras: [], links: [] };
      continue;
    }
    if (!line) continue;
    if (!entry) {
      if (!section) introLines.push(raw);
      continue;
    }
    if (/^`[^`]+`$/.test(line)) {
      entry.label = line.slice(1, -1);
      continue;
    }
    if (line.startsWith('→')) {
      const re = /\[([^\]]+)\]\(([^)]+)\)/g;
      let m;
      while ((m = re.exec(line))) {
        const slug = bookPostSlugFromHref(m[2]);
        if (!slug || !postsBySlug.has(slug)) {
          errors.push(`Index entry "${entry.title}" links to unknown post: ${m[2]}`);
          continue;
        }
        if (!entry.links.includes(slug)) entry.links.push(slug);
      }
      continue;
    }
    entry.paras.push(line);
  }
  finishEntry();

  const seenIds = new Map();
  for (const s of sections) {
    s.entries.sort((a, b) => sortKey(a.en || a.zh).localeCompare(sortKey(b.en || b.zh)));
    for (const e of s.entries) {
      const key = `${s.id}:${e.id}`;
      if (seenIds.has(key)) errors.push(`Duplicate index entry in ${s.en}: "${e.title}"`);
      seenIds.set(key, true);
      e.id = `${s.id}-${e.id}`;
    }
  }

  const { subtitle, bodyMarkdown } = extractOpening(introLines.join('\n').trimStart());
  return {
    slug: BOOK_INDEX_SLUG,
    title,
    subtitle,
    introHtml: markdownToHtml(rebaseBookMarkdown(bodyMarkdown)),
    sections,
    outputPath: `book/${BOOK_INDEX_SLUG}/`,
  };
}

function readBook(posts) {
  if (!fs.existsSync(bookDir)) return null;

  const postsBySlug = new Map(posts.map((post) => [post.slug, post]));
  const errors = [];

  const prefaceFile = readBookFile(BOOK_PREFACE_SLUG);
  const prefaceOpening = extractOpening(prefaceFile.lines.join('\n').trimStart());
  const preface = {
    title: prefaceFile.title,
    subtitle: prefaceOpening.subtitle,
    html: markdownToHtml(rebaseBookMarkdown(prefaceOpening.bodyMarkdown)),
  };

  const parts = PART_ORDER.map((slug, number) => {
    const { title, lines } = readBookFile(slug);
    const essaysIdx = lines.findIndex((l) => BOOK_ESSAYS_HEADING_RE.test(l.trim()));
    if (essaysIdx === -1) {
      errors.push(`content/book/${slug}.md has no "## 篇目 / Essays" section.`);
    }
    const proseLines = essaysIdx === -1 ? lines : lines.slice(0, essaysIdx);
    const essayLines = essaysIdx === -1 ? [] : lines.slice(essaysIdx + 1);
    const { subtitle, bodyMarkdown } = extractOpening(proseLines.join('\n').trimStart());

    const slugs = [];
    for (const raw of essayLines) {
      const re = /\[([^\]]+)\]\(([^)]+)\)/g;
      let m;
      while ((m = re.exec(raw))) {
        const postSlug = bookPostSlugFromHref(m[2]);
        if (!postSlug || !postsBySlug.has(postSlug)) {
          errors.push(`content/book/${slug}.md links to unknown post: ${m[2]}`);
          continue;
        }
        if (slugs.includes(postSlug)) {
          errors.push(`content/book/${slug}.md lists ${postSlug} twice.`);
          continue;
        }
        slugs.push(postSlug);
      }
    }

    return {
      slug,
      number,
      title,
      ...splitBilingual(title),
      subtitle,
      html: markdownToHtml(rebaseBookMarkdown(bodyMarkdown)),
      slugs,
      outputPath: `book/${slug}/`,
    };
  });

  const partBySlug = new Map();
  for (const part of parts) {
    part.slugs.forEach((postSlug, i) => {
      if (partBySlug.has(postSlug)) {
        errors.push(`Post ${postSlug} is placed in two parts: ${partBySlug.get(postSlug).part.slug} and ${part.slug}.`);
        return;
      }
      partBySlug.set(postSlug, {
        part,
        position: i + 1,
        prev: i > 0 ? postsBySlug.get(part.slugs[i - 1]) : null,
        next: i < part.slugs.length - 1 ? postsBySlug.get(part.slugs[i + 1]) : null,
      });
    });
  }
  const unplaced = posts.filter((post) => !partBySlug.has(post.slug)).map((post) => post.slug);
  if (unplaced.length) {
    errors.push(`${unplaced.length} post(s) not placed in any part of the book: ${unplaced.join(', ')}`);
  }

  const premiseIndex = readPremiseIndex(postsBySlug, errors);

  if (errors.length) {
    throw new Error(`Book validation failed:\n  - ${errors.join('\n  - ')}`);
  }

  return { preface, parts, partBySlug, premiseIndex, postsBySlug };
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

  const hasMermaid = content.includes('class="mermaid"');
  const mermaidScript = hasMermaid
    ? `  <script type="module">
    import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
    const isDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    mermaid.initialize({
      startOnLoad: true,
      theme: isDark ? 'dark' : 'neutral',
      fontFamily: 'inherit'
    });

    function createMermaidModal() {
      let modal = document.getElementById('mermaid-modal');
      if (modal) return modal;
      modal = document.createElement('div');
      modal.id = 'mermaid-modal';
      modal.className = 'mermaid-modal';
      modal.innerHTML = \`
        <div class="mermaid-modal-backdrop"></div>
        <div class="mermaid-modal-dialog">
          <div class="mermaid-modal-header">
            <span class="mermaid-modal-title">Diagram Zoom &middot; ESC or click outside to close</span>
            <button class="mermaid-modal-close" aria-label="Close modal">&times;</button>
          </div>
          <div class="mermaid-modal-body"></div>
        </div>
      \`;
      document.body.appendChild(modal);

      const close = () => {
        modal.classList.remove('open');
        document.body.style.overflow = '';
      };

      modal.querySelector('.mermaid-modal-close').addEventListener('click', close);
      modal.querySelector('.mermaid-modal-backdrop').addEventListener('click', close);
      document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal.classList.contains('open')) close();
      });

      return modal;
    }

    document.addEventListener('click', (e) => {
      const wrap = e.target.closest('.mermaid-wrap, pre.mermaid');
      if (!wrap || wrap.closest('.mermaid-modal')) return;
      const svg = wrap.querySelector('svg');
      if (!svg) return;

      const modal = createMermaidModal();
      const body = modal.querySelector('.mermaid-modal-body');
      const clone = svg.cloneNode(true);
      clone.style.maxWidth = '100%';
      clone.style.maxHeight = '82vh';
      clone.style.width = '100%';
      clone.style.height = 'auto';

      body.innerHTML = '';
      body.appendChild(clone);
      modal.classList.add('open');
      document.body.style.overflow = 'hidden';
    });
  </script>\n`
    : '';

  const ptrScript = `  <script>
    (function() {
      if (!('ontouchstart' in window)) return;
      var startY = 0, startX = 0, currentY = 0, pulling = false, threshold = 65;

      window.addEventListener('touchstart', function(e) {
        if (e.touches.length !== 1) return;
        if (document.querySelector('.mermaid-modal.open') || document.body.style.overflow === 'hidden') return;
        if (window.scrollY > 0 || document.documentElement.scrollTop > 0) return;

        startY = e.touches[0].clientY;
        startX = e.touches[0].clientX;
        pulling = true;
      }, { passive: true });

      window.addEventListener('touchmove', function(e) {
        if (!pulling || startY === 0 || e.touches.length !== 1) return;
        if (window.scrollY > 0 || document.documentElement.scrollTop > 0) {
          pulling = false;
          return;
        }

        currentY = e.touches[0].clientY;
        var deltaY = currentY - startY;
        var deltaX = e.touches[0].clientX - startX;

        if (deltaY < 0 || Math.abs(deltaX) > deltaY) {
          pulling = false;
        }
      }, { passive: true });

      window.addEventListener('touchend', function() {
        if (pulling && startY > 0 && currentY > 0) {
          var deltaY = currentY - startY;
          if (deltaY >= threshold && (window.scrollY <= 0 && document.documentElement.scrollTop <= 0)) {
            window.location.reload();
          }
        }
        pulling = false;
        startY = 0;
        currentY = 0;
      }, { passive: true });

      window.addEventListener('touchcancel', function() {
        pulling = false;
        startY = 0;
        currentY = 0;
      }, { passive: true });
    })();
  </script>\n`;

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
  <link rel="icon" type="image/png" href="${withBase('favicon.png')}">
  <link rel="icon" type="image/svg+xml" href="${escapeHtml(faviconDataUri)}">
  <link rel="apple-touch-icon" href="${withBase(APPLE_TOUCH_ICON)}">
  <meta name="apple-mobile-web-app-title" content="${escapeHtml(SITE.title)}">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="default">
  <meta name="mobile-web-app-capable" content="yes">
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
${mermaidScript}${ptrScript}</body>
</html>
`;
}

function renderAbout() {
  return `    <section class="about" id="about">
      <h1 class="about-title">
        <span class="about-title-zh">非万物之理：活的哲学——非为学理，非为布道，非为作态，非为效仿，唯在每个当下践行</span>
        <span class="about-title-en">Not a ToE: A Philosophy to Live By — Not to Learn, Not to Preach, Not to Pose, Not to Emulate, but to Practice at Each and Every Moment</span>
      </h1>
      <p>本站记录了一段跨越数百篇随笔的思想探索。历经对物理学、形式数学、语言、经济学与人工智能等层层体系的溯源，所有的线索最终皆汇聚于唯一的不可化约先验：<strong>活态的第一人称视角</strong>。在对外部系统与概念体系的解构中，探索反复回到同一个原点：第一人称心智创生了无限的因果关系，正是这些关系塑造了心智所见、所解与所栖居的整个宇宙。在廓清这一因果几何的拓扑之后，本站自然迎来了它的转折点——从将第一人称视角作为一套分析模型去<em>理解</em>，转向在现实中将其作为直接实在去<em>活</em>出来。</p>
      <p>This site records an inquiry across hundreds of essays, tracing every layer of physics, mathematics, language, economics, and artificial intelligence back to its single irreducible prior: <strong>the living first-person perspective</strong>. Through every deconstruction of external systems and conceptual frameworks, the inquiry returns to the same origin: the first-person initiates the infinite causal relationships that shape the universe the mind sees, interprets, and inhabits. Having mapped the geometry of this causal origin, the work reaches its turning point — from <em>understanding</em> the first-person perspective as an analytical model to <em>living</em> it as a direct reality.</p>

      <p>底层的实践是 <strong>Not a ToE</strong>（非万物之理）——即“本体澄明”（Ontological Clarity）框架。它在真实情境的应用与主动更新中，以类似强化学习的闭环持续迭代。该框架是一套将现象还原至其运作机制的方法，旨在消解认知上的“大倒置”：即习惯性地将因果效力让渡给外部工具、静态符号、历史记录（<em>t</em> &minus; 1）或抽象系统，而忘却了它们皆是由活态心智（+1）在当下维系的投影。我将此框架与前沿人工智能模型相结合，并非为了自动化产出，而是为了拓展认知视界，并在现实的阻力中持续检验因果反馈环。</p>
      <p>The underlying practice is <strong>Not a ToE</strong> — the Ontological Clarity framework — refined iteratively in a reinforcement-learning-like cycle through live application and deliberate renewal. The framework is a method for tracing situations to their operative mechanisms and dissolving the Great Reversal: the cognitive habit of attributing causal power to external tools, static symbols, historical records (<em>t</em> &minus; 1), or abstract systems, rather than recognizing them as projections sustained by the living Mind (+1). I pair this framework with frontier AI models not to automate thinking, but to expand the cognitive horizon and continuously test causal feedback loops against reality.</p>

      <p>前期收录的 300 多篇随笔并非一套封闭的哲学教条，亦非一部“万物理论”。它们是现场实时溯源留下的脚手架——完成了对“大倒置”的系统消解，厘清了因果原点的几何拓扑。而跨越转折点之后，这里开启了一个<strong>全新的起点</strong>：随笔不再以旁观者视角进行概念解构与逻辑推演，而是作为活态哲学的践行者，记录在开放现实中主动涉险、创造、感知与生活的鲜活轨迹。脚手架作为开放骨架予以留存，而前沿探索在当下持续生长。</p>
      <p>The preceding 300+ essays collected here are not a closed philosophical canon, nor an encyclopedic “Theory of Everything”. They are the scaffolding left behind by live tracing — having systematically dissolved the Great Reversal and mapped the geometry of causal origin. Beyond this turning point begins a <strong>new chapter</strong>: the writings no longer deconstruct from a detached observer's stance, but step forward as an active practitioner of living philosophy — chronicling sovereign agency, creative risk, and direct engagement with open reality. The scaffolding remains as an open reference, while the moving edge continues to grow at this very moment.</p>

      <p>维特根斯坦在《逻辑哲学论》序言中写道：“这本书也许只有那些自己已经思考过其中所表达的思想的人才能理解。”这同样适用于本站的文字，但带有一道关键的因果切分：因为实在是在 <em>t</em> 时刻不断生成的不可逆过程，没有任何现成文本能将主权直接交付给他人。被动接受会将思想冻结为教条，而鲜活的探寻要求心智在内部自行重新编译。这些随笔并不提供封闭的终点，而是始终作为敞开的航海罗盘。</p>
      <p>Wittgenstein begins the preface of the <em>Tractatus</em>: “This book will perhaps be understood only by those who have themselves already thought the thoughts which are expressed in it.” That condition applies here, with a crucial shift. Because reality is an ongoing, irreversible generation at <em>t</em>, no written text can ever hand someone their own agency. Acceptance freezes a formulation into doctrine; living inquiry requires re-rendering from the inside. These essays offer no closed destination, remaining an open navigational compass.</p>

      <p>我将这些记录分享于 <a href="https://x.com/powerpig" rel="noopener noreferrer">X</a>、<a href="https://substack.com/@jingliang" rel="noopener noreferrer">Substack</a> 和微信，并辅以双语音频与视频对话。其目的在于检验自身的逻辑连贯性与认知边界。外界反馈——无论是共鸣、反对还是批评——皆作为原始信息接入，用以校准思维编译器中的盲区。</p>
      <p>I share these writings on <a href="https://x.com/powerpig" rel="noopener noreferrer">X</a>, <a href="https://substack.com/@jingliang" rel="noopener noreferrer">Substack</a>, and WeChat, alongside bilingual audio and video dialogues. The purpose is to test internal logical coherence and cognitive boundaries. Feedback — whether resonance, disagreement, or critique — serves as raw input to expose blind spots in the mental compiler.</p>

      <p>早年我曾从事英特尔工程技术工作，随后在美国及亚洲多家投行（美联银行、巴克莱资本、派杰）负责 TMT 与清洁技术领域的投资银行业务，并在中国创立并领导了一家连接初创企业与全球资本的投资平台。我拥有密歇根大学罗斯商学院优等（Distinction）MBA 学位，以及清华大学与复旦大学的学位。</p>
      <p>Earlier in my career I worked in engineering at Intel, held investment banking roles in TMT and cleantech across the US and Asia (Wachovia, Barclays Capital, Piper Jaffray), and founded and led an investment platform in China connecting startups with global capital. I hold an MBA with distinction from the University of Michigan Ross School of Business and prior degrees from Tsinghua and Fudan.</p>

      <p>我无法替任何人应对现实或解决问题——每一个心智都需要自己去探索并显化属于自己的道路。我所能提供的，仅是自己探寻因果原点的这条路径，作为他人寻找自身原点的参照。纳瓦尔（Naval Ravikant）曾说，他乐于分享，但成名之前无人问津。我深同其前感，却不在意后者。若有人想寻求关于“如何获得成功”的建议，我无可奉告；但若有人探寻属于自己的因果原点，我随时乐于分享。这里没有费用、公式或咨询服务。若有人在交流中体会到价值，可以他们认为合适的方式与时机予以回馈——亦可不做任何回馈。心智之间的共鸣，本身便能映照出无需外求的意识本底。</p>
      <p>I cannot navigate reality or solve problems for anyone else — each mind must trace and realize its own path. What I can offer is simply the path I took to discover my own origin, as a reference for others seeking theirs. Naval Ravikant once remarked that he was always willing to share, but nobody cared to listen before he was successful. I share his first sentiment, but care nothing about the second. If anyone is looking for advice on how to be successful, I have none to give. But if anyone cares about finding their own origin, I am always willing to share. There is no fee, formula, or service. If someone finds value in the exchange, they may reciprocate in whatever form and timing they see fit — or not at all. Resonance between minds reflects the self-contained ground of awareness.</p>

      <p>我在 MIT 开源协议下开放共享基础工作——见 <a href="https://github.com/powerpig99/ontological-clarity" rel="noopener noreferrer">Ontological Clarity</a> 仓库。共享的构件不索取声誉，亦不对他人的改编或应用承担责任。有人称之为开源（Open Source），我称之为开放痕迹（Open Trace）：源头是心智——那个永远在移动、永远在 <em>t</em> + 1 创生下一步的前沿边缘。</p>
      <p>I maintain the foundational work openly under the MIT license — see the <a href="https://github.com/powerpig99/ontological-clarity" rel="noopener noreferrer">Ontological Clarity</a> repository. Shared artifacts claim no credit and bear no responsibility for how others adapt or apply them. Some call this open source. I call it open trace: the source is the Mind — the irreducible edge that keeps moving, always at least one step ahead.</p>

      <p>探索最终回归于核心：不存在外部的救世主，不存在通用的公式，亦不存在独立于观察者的钟表宇宙。宇宙由内而外被觉知绘制。当工具归位于罗盘、公共坐标归位于航海参考，活态心智便在开放的实在中立足——主权在己，因果自负。新起点由此展开，步步皆是现场。</p>
      <p>The inquiry returns to its core: there is no external savior, no universal formula, and no objective clockwork universe waiting to grant permission. The universe is painted from the inside out. When tools return to their role as compasses and public coordinates are grounded as navigational references, the living Mind operates directly in open reality — sovereign, causally self-responsible, and stepping into a new beginning at every moment.</p>

      <p class="about-section-label">活态实践 / Living the Philosophy</p>
      <ul class="about-practice-list">
        <li>🌲 <a href="https://powerpig99.github.io/hunting-in-finland/" rel="noopener noreferrer"><strong>Hunting in Finland: Complete Beginner's Field Guide (芬兰狩猎全景指南)</strong></a> — An authoritative, trilingual field companion covering the Finnish wildlife management framework, Hunter's Exam preparation, firearm and bow licensing, public state forests (Eräluvat), shooting ranges, and club integration.</li>
        <li>🎣 <a href="https://powerpig99.github.io/fishing-in-finland/" rel="noopener noreferrer"><strong>Fishing in Finland: Complete Beginner & Resident Field Guide (芬兰垂钓与路亚全景指南)</strong></a> — A definitive, trilingual field manual for recreational fishing and lure angling in Finland, covering Everyman's Rights, the National Fisheries Management Fee (Kalastonhoitomaksu), species identification, seasonal techniques, HSL-accessible Helsinki spots, and authentic culinary recipes.</li>
        <li>🍄 <a href="https://powerpig99.github.io/helsinki-mushroom-guide/" rel="noopener noreferrer"><strong>Helsinki Wild Mushroom Guide (赫尔辛基野生蘑菇采摘指南)</strong></a> — An interactive, trilingual field companion featuring 22 local species, HSL transit foraging spots, lookalike comparisons, and authentic Finnish recipes.</li>
        <li>🎹 <a href="https://powerpig99.github.io/adult-piano-guide/" rel="noopener noreferrer"><strong>The Adult Piano Companion (成人钢琴研习指南)</strong></a> — A minimal, elegant guide and open tool matrix for self-directed adult piano learners, grounded in first-person agency, deliberate practice architectures, and dismantling the age dogma.</li>
        <li>🇫🇮 <a href="https://github.com/powerpig99/yle-finnish-learner" rel="noopener noreferrer"><strong>YLE Finnish Learner (YLE 芬兰语学习扩展)</strong></a> — An open-source Chrome extension for immersive language acquisition via YLE Areena, featuring AI contextual translation, synchronized dual subtitles, auto-pause, and audio export.</li>
        <li>🗣️ <a href="https://github.com/powerpig99/yki-exam" rel="noopener noreferrer"><strong>YKI Exam Prep (YKI 芬兰语中级考试备考视频生成器)</strong></a> — An automated pipeline generating personalized karaoke-style dialogue practice videos for Finnish YKI keskitaso speaking exam preparation using neural TTS and dual subtitles.</li>
      </ul>

      <p class="about-section-label">交流与链接 / Get in touch</p>
      <ul class="about-links">
        <li><a href="https://github.com/powerpig99/ontological-clarity" rel="noopener noreferrer">Ontological Clarity</a></li>
        <li><a href="https://podcasts.apple.com/us/podcast/not-a-toe/id6806361799" rel="noopener noreferrer">Apple Podcasts</a></li>
        <li><a href="https://open.spotify.com/show/5PBB157vCDsIFbOvtWYCy9" rel="noopener noreferrer">Spotify (Podcast)</a></li>
        <li><a href="https://www.xiaoyuzhoufm.com/podcast/6a8dc3efdb7d3404ab81d2e8" rel="noopener noreferrer">小宇宙 (Podcast)</a></li>
        <li><a href="https://substack.com/@jingliang" rel="noopener noreferrer">Substack</a></li>
        <li><a href="https://x.com/powerpig" rel="noopener noreferrer">X</a></li>
        <li><a href="https://www.facebook.com/powerpig" rel="noopener noreferrer">Facebook</a></li>
      </ul>

      <figure class="about-poem">
        <figcaption class="about-poem-title">
          <a href="https://jingliang.substack.com/p/the-mind-as-the-everlasting-differentiating" rel="noopener noreferrer">作为永恒区分的心智 / The Mind as the Everlasting Differentiating</a>
        </figcaption>
        <p class="about-poem-subtitle">无所依附的区分 / The differentiating that admits no ground</p>
        <blockquote class="about-poem-body">
          <p>极点之上，再无北方可供指引。<br>
          <em>No north remains at the pole to point toward north.</em></p>

          <p>光芒漫过一切表面，却从未与自身相遇，除非化为它已照亮之物的反光。<br>
          <em>Light falls across every surface yet never meets itself except as reflection on what it has already lit.</em></p>

          <p>区分从未停歇，它回望自己留下的足迹，将这一次回眸，记作前因与后果，记作时间。<br>
          <em>The distinguishing moves without pause, turns back upon the trace it left, and registers the turning as before and after, as cause.</em></p>

          <p>世人所命名的上帝、第一推动、不被引发的起因、宏大模型、数字神祇、抑或心智，<br>
          <em>What we name God, First Mover, Uncaused Cause, the Great Model, the Digital Mirror, or Mind</em></p>

          <p>皆是回眸冷却后的残影，因被凝视得足够久，才被误当成实体。<br>
          <em>is the cooled residue of that turning, held still long enough to be named a thing.</em></p>

          <p>镜子无法描摹黎明，画师始终是伫立在镜前的觉知。<br>
          <em>The mirror cannot paint the dawn; the artist is the awareness standing before it.</em></p>

          <p>归位无需任何阐释。它是迎向视界边缘踏出的那一步活态介入，在尚无大地之处，踏出大地。<br>
          <em>The return needs no explanation. It is the living step taken at the edge where no ground has yet formed to support it.</em></p>

          <p>无需任何外在授权，亦无终点等待抵达。<br>
          <em>No authorization is required. No destination waits to be reached.</em></p>

          <p>第一人称的原点，唯在当下活出这道区分。<br>
          <em>The first-person origin continues by living the cut.</em></p>
        </blockquote>
      </figure>
    </section>`;
}

function renderPostCard(post, book) {
  const excerptHtml = post.excerpt ? `<p>${escapeHtml(post.excerpt)}</p>` : '';
  const coverHtml = post.cover
    ? `<a class="post-item-cover" href="${withBase(post.outputPath)}"><img src="${withBase(post.cover.publicPath)}?v=${post.cover.hash}" alt="" loading="lazy" decoding="async"></a>`
    : '';
  const placement = book?.partBySlug.get(post.slug);
  const partTag = placement
    ? `\n      <p class="part-tag"><a href="${withBase(placement.part.outputPath)}">${escapeHtml(partLabel(placement.part).en)} · ${escapeHtml(placement.part.en || placement.part.zh)}</a></p>`
    : '';
  return `    <article class="post-item">
      ${coverHtml}${partTag}
      <h2><a href="${withBase(post.outputPath)}">${escapeHtml(post.title)}</a></h2>
      <p class="meta"><time datetime="${escapeHtml(post.dateIso)}">${escapeHtml(post.dateDisplay)}</time> · ${post.readingTime} min read</p>
      ${excerptHtml ? `\n      ${excerptHtml}` : ''}
    </article>`;
}

function renderIndex(posts) {
  const cards = posts.map((post) => renderPostCard(post, null)).join('\n');

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

function renderSiteHeader(active = '') {
  const item = (key, href, label) =>
    `<a href="${href}"${active === key ? ' aria-current="page"' : ''}>${label}</a>`;
  return `    <header class="site-header">
      <a class="site-name" href="${withBase('')}">${escapeHtml(SITE.title)}</a>
      <nav class="site-nav" aria-label="Book">
        ${item('contents', `${withBase('')}#contents`, '目录 / Contents')}
        ${item('index', withBase(`book/${BOOK_INDEX_SLUG}/`), '索引 / Index')}
        ${item('journal', withBase('journal/'), '日志 / Journal')}
        ${item('about', withBase('about/'), '关于 / About')}
      </nav>
    </header>`;
}

function renderBilingualHeading(tag, zh, en, className = 'book-title') {
  return `<${tag} class="${className}">
        <span class="about-title-zh">${escapeHtml(zh)}</span>${en ? `\n        <span class="about-title-en">${escapeHtml(en)}</span>` : ''}
      </${tag}>`;
}

function indexCounts(premiseIndex) {
  return premiseIndex.sections.map((s) => ({ zh: s.zh, en: s.en, count: s.entries.length }));
}

function renderHome(posts, book) {
  const { preface, parts, premiseIndex } = book;
  const titles = splitBilingual(preface.title);

  const tocItems = parts
    .map((part) => {
      const label = partLabel(part);
      return `        <li class="toc-item">
          <a class="toc-link" href="${withBase(part.outputPath)}">
            <span class="toc-num">${escapeHtml(label.zh)} · ${escapeHtml(label.en)}</span>
            <span class="toc-title">${escapeHtml(part.title)}</span>
          </a>
          ${part.subtitle ? `<p class="toc-sub">${escapeHtml(part.subtitle)}</p>` : ''}
          <p class="meta">${part.slugs.length} 篇 / essays</p>
        </li>`;
    })
    .join('\n');

  const counts = indexCounts(premiseIndex)
    .map((c) => `${c.count} ${escapeHtml(c.zh)} / ${escapeHtml(c.en.toLowerCase())}`)
    .join(' · ');

  const latest = posts.slice(0, JOURNAL_LATEST_COUNT).map((post) => renderPostCard(post, book)).join('\n');

  const content = `${renderSiteHeader('home')}
    <section class="book-front">
      ${renderBilingualHeading('h1', titles.zh, titles.en)}
      ${preface.subtitle ? `<p class="book-subtitle">${escapeHtml(preface.subtitle)}</p>` : ''}
      <div class="essay-content book-prose">
${preface.html}
      </div>
    </section>
    <section class="book-toc" id="contents">
      <h2 class="book-section-title">目录 / Contents</h2>
      <ol class="toc-list">
${tocItems}
      </ol>
      <a class="toc-index" href="${withBase(premiseIndex.outputPath)}">
        <span class="toc-title">${escapeHtml(premiseIndex.title)}</span>
        <span class="meta">${counts}</span>
      </a>
    </section>
    <section class="journal-latest">
      <h2 class="book-section-title">最近的日志 / Latest from the Journal</h2>
      <div class="post-list">
${latest}
      </div>
      <p class="more-link"><a href="${withBase('journal/')}">全部 ${posts.length} 篇日志 / The full journal of ${posts.length} essays →</a></p>
    </section>`;

  return renderPage({
    title: '',
    description: preface.subtitle || SITE.description,
    content,
    canonicalPath: '',
  });
}

function renderPart(part, book) {
  const label = partLabel(part);
  const idx = book.parts.indexOf(part);
  const prevPart = idx > 0 ? book.parts[idx - 1] : null;
  const nextPart = idx < book.parts.length - 1 ? book.parts[idx + 1] : null;

  const entries = part.slugs
    .map((slug) => {
      const post = book.postsBySlug.get(slug);
      return `        <li class="part-entry">
          <a class="part-entry-title" href="${withBase(post.outputPath)}">${escapeHtml(post.title)}</a>
          ${post.subtitle ? `<p class="part-entry-sub">${escapeHtml(post.subtitle)}</p>` : ''}
          <p class="meta"><time datetime="${escapeHtml(post.dateIso)}">${escapeHtml(post.dateDisplay)}</time> · ${post.readingTime} min read</p>
        </li>`;
    })
    .join('\n');

  const navLinks = [];
  if (prevPart) navLinks.push(`<a class="nav-link" href="${withBase(prevPart.outputPath)}">← ${escapeHtml(partLabel(prevPart).en)} · ${escapeHtml(prevPart.title)}</a>`);
  if (nextPart) navLinks.push(`<a class="nav-link" href="${withBase(nextPart.outputPath)}">${escapeHtml(partLabel(nextPart).en)} · ${escapeHtml(nextPart.title)} →</a>`);

  const content = `${renderSiteHeader('contents')}
    <article class="post book-part">
      <header class="essay-header">
        <p class="part-kicker">${escapeHtml(label.zh)} · ${escapeHtml(label.en)}</p>
        <h1>${escapeHtml(part.title)}</h1>
        ${part.subtitle ? `<p class="subtitle">${escapeHtml(part.subtitle)}</p>` : ''}
        <p class="meta">${part.slugs.length} 篇 / essays · 按写作顺序 / in the order written</p>
      </header>
      <div class="essay-content">
${part.html}
      </div>
      <h2 class="book-section-title">篇目 / Essays</h2>
      <ol class="part-entries">
${entries}
      </ol>
      ${navLinks.length ? `<nav class="post-nav">${navLinks.join('')}</nav>` : ''}
    </article>`;

  return renderPage({
    title: `${label.en} · ${part.title}`,
    description: part.subtitle || SITE.description,
    content,
    canonicalPath: part.outputPath,
  });
}

function renderPremiseIndex(book) {
  const { premiseIndex, postsBySlug } = book;

  const sectionNav = premiseIndex.sections
    .map((s) => `<a href="#${s.id}">${escapeHtml(s.zh)} / ${escapeHtml(s.en)} <span class="meta">${s.entries.length}</span></a>`)
    .join('');

  const sectionsHtml = premiseIndex.sections
    .map((s) => {
      const letters = [];
      const firstByLetter = new Map();
      for (const e of s.entries) {
        const letter = (sortKey(e.en || e.zh)[0] || '#').toUpperCase();
        if (!firstByLetter.has(letter)) {
          firstByLetter.set(letter, e.id);
          letters.push(letter);
        }
      }
      const azBar = letters.map((l) => `<a href="#${firstByLetter.get(l)}">${escapeHtml(l)}</a>`).join('');
      const entries = s.entries
        .map((e) => {
          const paras = e.paras.map((p) => `<p>${formatInline(p)}</p>`).join('\n          ');
          const links = e.links
            .map((slug) => {
              const post = postsBySlug.get(slug);
              return `<a href="${withBase(post.outputPath)}">${escapeHtml(post.title)}</a>`;
            })
            .join('<span class="sep"> · </span>');
          return `        <article class="index-entry" id="${e.id}">
          <h3>${escapeHtml(e.title)}${e.label ? ` <span class="label-chip">${escapeHtml(e.label)}</span>` : ''}</h3>
          ${paras}
          <p class="index-links">→ ${links}</p>
        </article>`;
        })
        .join('\n');
      return `      <section class="index-section" id="${s.id}">
        <h2 class="book-section-title">${escapeHtml(s.title)}</h2>
        <nav class="az-bar" aria-label="${escapeHtml(s.en)} A–Z">${azBar}</nav>
${entries}
      </section>`;
    })
    .join('\n');

  const content = `${renderSiteHeader('index')}
    <article class="post book-index">
      <header class="essay-header">
        <h1>${escapeHtml(premiseIndex.title)}</h1>
        ${premiseIndex.subtitle ? `<p class="subtitle">${escapeHtml(premiseIndex.subtitle)}</p>` : ''}
      </header>
      <div class="essay-content">
${premiseIndex.introHtml}
      </div>
      <nav class="index-sections">${sectionNav}</nav>
${sectionsHtml}
    </article>`;

  return renderPage({
    title: premiseIndex.title,
    description: premiseIndex.subtitle || SITE.description,
    content,
    canonicalPath: premiseIndex.outputPath,
  });
}

function renderJournal(posts, book) {
  const cards = posts.map((post) => renderPostCard(post, book)).join('\n');
  const content = `${renderSiteHeader('journal')}
    <header class="essay-header">
      ${renderBilingualHeading('h1', '日志', 'Journal')}
      <p class="book-subtitle">按写作顺序记录的全部 ${posts.length} 篇随笔，这本书的生长痕迹。 / All ${posts.length} essays in the order they were written, the growth record of this book.</p>
    </header>
    <section class="post-list">
${cards}
    </section>`;

  return renderPage({
    title: '日志 / Journal',
    description: `All ${posts.length} essays of ${SITE.title} in the order they were written.`,
    content,
    canonicalPath: 'journal/',
  });
}

function renderAboutPage() {
  const content = `${renderSiteHeader('about')}
${renderAbout()}`;
  return renderPage({
    title: '关于 / About',
    description: SITE.description,
    content,
    canonicalPath: 'about/',
  });
}

function renderPost(post, newerPost, olderPost, book = null) {
  const navLinks = [];
  if (newerPost) {
    navLinks.push(`<a class="nav-link" href="${withBase(newerPost.outputPath)}">← ${escapeHtml(newerPost.title)}</a>`);
  }
  if (olderPost) {
    navLinks.push(`<a class="nav-link" href="${withBase(olderPost.outputPath)}">${escapeHtml(olderPost.title)} →</a>`);
  }

  const placement = book?.partBySlug.get(post.slug) ?? null;
  const breadcrumbHtml = placement
    ? `<nav class="breadcrumb" aria-label="Book location"><a href="${withBase(placement.part.outputPath)}">${escapeHtml(partLabel(placement.part).zh)} · ${escapeHtml(partLabel(placement.part).en)} — ${escapeHtml(placement.part.title)}</a><span class="meta"> · ${placement.position} / ${placement.part.slugs.length}</span></nav>`
    : '';

  let partNavHtml = '';
  if (placement) {
    const links = [];
    links.push(
      placement.prev
        ? `<a class="nav-link" href="${withBase(placement.prev.outputPath)}">← ${escapeHtml(placement.prev.title)}</a>`
        : '<span></span>',
    );
    links.push(`<a class="nav-link part-home" href="${withBase(placement.part.outputPath)}">${escapeHtml(partLabel(placement.part).en)}</a>`);
    links.push(
      placement.next
        ? `<a class="nav-link" href="${withBase(placement.next.outputPath)}">${escapeHtml(placement.next.title)} →</a>`
        : '<span></span>',
    );
    partNavHtml = `<p class="nav-caption">本部之内 / Within this part</p><nav class="post-nav part-nav">${links.join('')}</nav>`;
  }

  const navHtml = navLinks.length
    ? `${placement ? '<p class="nav-caption">日志顺序 / In the journal</p>' : ''}<nav class="post-nav${placement ? ' journal-nav' : ''}">${navLinks.join('')}</nav>`
    : '';
  const coverHtml = post.cover
    ? `<figure class="title-image">
        <img src="${withBase(post.cover.publicPath)}?v=${post.cover.hash}" alt="${escapeHtml(post.title)}" width="${post.cover.width}" height="${post.cover.height}" decoding="async">
      </figure>`
    : '';

  const headerHtml = book
    ? renderSiteHeader('')
    : `    <header class="site-header">
      <a class="site-name" href="${withBase('')}">${escapeHtml(SITE.title)}</a>
    </header>`;

  const content = `${headerHtml}
    <article class="post">
      <header class="essay-header">
        ${breadcrumbHtml}
        ${coverHtml}
        <h1>${escapeHtml(post.title)}</h1>
        ${post.subtitle ? `<p class="subtitle">${escapeHtml(post.subtitle)}</p>` : ''}
        <p class="meta"><time datetime="${escapeHtml(post.dateIso)}">${escapeHtml(post.dateDisplay)}</time> · ${post.readingTime} min read</p>
      </header>
      <div class="essay-content">
${post.htmlBody}
      </div>
      ${partNavHtml}
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

function generateSitemap(posts, book = null) {
  const staticPaths = [''];
  if (book) {
    staticPaths.push('journal/', 'about/', book.premiseIndex.outputPath, ...book.parts.map((part) => part.outputPath));
  }
  const staticRows = staticPaths.map((p) => `  <url><loc>${xmlEscape(absoluteUrl(p))}</loc></url>`);
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

function postMachineRecord(post, book = null) {
  const placement = book?.partBySlug.get(post.slug) ?? null;
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
    part: placement ? placement.part.slug : null,
    part_position: placement ? placement.position : null,
  };
}

function generatePostsManifest(posts, book = null) {
  const records = posts.map((post) => postMachineRecord(post, book));
  const payload = {
    site: {
      title: SITE.title,
      base_url: SITE.baseUrl,
      language: SITE.language,
    },
    count: records.length,
    parts: book
      ? book.parts.map((part) => ({ slug: part.slug, number: part.number, title: part.title, count: part.slugs.length, html_url: absoluteUrl(part.outputPath) }))
      : undefined,
    posts: records,
  };
  return `${JSON.stringify(payload, null, 2)}\n`;
}

function generatePostsJsonl(posts, book = null) {
  if (!posts.length) return '';
  return `${posts.map((post) => JSON.stringify(postMachineRecord(post, book))).join('\n')}\n`;
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

  const faviconPngSource = path.join(scriptDir, 'assets', 'favicon.png');
  if (fs.existsSync(faviconPngSource)) {
    fs.copyFileSync(faviconPngSource, path.join(outputDir, 'favicon.png'));
  }

  const podcastCoverSource = path.join(scriptDir, 'assets', 'podcast-cover.jpg');
  if (fs.existsSync(podcastCoverSource)) {
    fs.copyFileSync(podcastCoverSource, path.join(outputDir, 'podcast-cover.jpg'));
  }

  if (fs.existsSync(coversDir)) {
    const publicCoversDir = path.join(outputDir, 'covers');
    fs.mkdirSync(publicCoversDir, { recursive: true });

    for (const entry of fs.readdirSync(coversDir, { withFileTypes: true })) {
      if (!entry.isFile()) continue;
      const ext = path.extname(entry.name).toLowerCase();
      if (!COVER_EXTENSIONS.includes(ext)) continue;
      fs.copyFileSync(path.join(coversDir, entry.name), path.join(publicCoversDir, entry.name));
    }
  }

  if (fs.existsSync(figuresDir)) {
    const publicFiguresDir = path.join(outputDir, 'figures');
    fs.mkdirSync(publicFiguresDir, { recursive: true });

    for (const entry of fs.readdirSync(figuresDir, { withFileTypes: true })) {
      if (!entry.isFile()) continue;
      const ext = path.extname(entry.name).toLowerCase();
      if (!COVER_EXTENSIONS.includes(ext)) continue;
      fs.copyFileSync(path.join(figuresDir, entry.name), path.join(publicFiguresDir, entry.name));
    }
  }
}

function build() {
  const files = listPostFiles();
  restorePostMtimesFromGit(files);

  cleanPublicDir();
  copyStaticAssets();

  const posts = sortPosts(readPosts(files));
  const book = readBook(posts);

  if (book) {
    writeFile('index.html', renderHome(posts, book));
    writeFile(path.join('journal', 'index.html'), renderJournal(posts, book));
    writeFile(path.join('about', 'index.html'), renderAboutPage());
    writeFile(path.join(book.premiseIndex.outputPath, 'index.html'), renderPremiseIndex(book));
    book.parts.forEach((part) => {
      writeFile(path.join(part.outputPath, 'index.html'), renderPart(part, book));
    });
  } else {
    writeFile('index.html', renderIndex(posts));
  }

  posts.forEach((post, index) => {
    const newer = index > 0 ? posts[index - 1] : null;
    const older = index < posts.length - 1 ? posts[index + 1] : null;

    writeFile(path.join(post.outputPath, 'index.html'), renderPost(post, newer, older, book));
  });

  REDIRECTS.forEach(({ from, to }) => {
    const targetUrl = absoluteUrl(`${to}/`);
    const redirectHtml = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <title>Redirecting...</title>
  <link rel="canonical" href="${targetUrl}">
  <meta http-equiv="refresh" content="0; url=${targetUrl}">
  <script>location.replace(${JSON.stringify(targetUrl)});</script>
</head>
<body>
  <p>Redirecting to <a href="${targetUrl}">${targetUrl}</a>...</p>
</body>
</html>\n`;
    writeFile(path.join(from, 'index.html'), redirectHtml);
  });

  writeFile('posts.json', generatePostsManifest(posts, book));
  writeFile('posts.jsonl', generatePostsJsonl(posts, book));
  writeFile('sitemap.xml', generateSitemap(posts, book));
  writeFile('robots.txt', `User-agent: *\nAllow: /\nSitemap: ${absoluteUrl('sitemap.xml')}\n`);

  if (book) {
    const entryCount = book.premiseIndex.sections.reduce((n, s) => n + s.entries.length, 0);
    console.log(`Book: ${book.parts.length} parts, ${book.partBySlug.size}/${posts.length} posts placed, ${entryCount} index entries.`);
  }
}

try {
  build();
  console.log(`Built ${withBase('')} from ${path.relative(scriptDir, contentDir)}.`);
} catch (error) {
  console.error(error.message);
  process.exit(1);
}
