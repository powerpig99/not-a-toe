/**
 * Shared post markdown helpers for external projections (Substack, etc.).
 * Source of truth remains content/posts/*.md with relative links.
 */

export const SITE_BASE = 'https://powerpig99.github.io/not-a-toe/';

export function toAbsoluteHref(href, baseUrl = SITE_BASE) {
  const base = baseUrl.endsWith('/') ? baseUrl : `${baseUrl}/`;
  const target = href.trim();
  if (/^https?:\/\//i.test(target) || target.startsWith('mailto:') || target.startsWith('#')) {
    return target;
  }
  if (target.startsWith('/')) {
    return new URL(target.replace(/^\/+/, ''), base).toString();
  }
  const rel = target.replace(/^\.\//, '').replace(/^\.\.\//, '').replace(/\/$/, '');
  if (!rel || rel.includes('://')) return target;
  return new URL(`posts/${rel}/`, base).toString();
}

/** Rewrite relative post links and body figures to absolute site URLs. */
export function toAbsoluteMarkdown(md, baseUrl = SITE_BASE) {
  const base = baseUrl.endsWith('/') ? baseUrl : `${baseUrl}/`;
  const withImages = md.replace(/!\[([^\]]*)\]\(([^)]+)\)/g, (full, alt, src) => {
    const target = src.trim();
    if (/^https?:\/\//i.test(target) || target.startsWith('mailto:') || target.startsWith('#')) {
      return full;
    }
    const clean = target.replace(/^\/+/, '');
    return `![${alt}](${new URL(clean, base).toString()})`;
  });
  return withImages.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (full, text, href) => {
    const target = href.trim();
    if (/^https?:\/\//i.test(target) || target.startsWith('mailto:') || target.startsWith('#')) {
      return full;
    }
    const abs = toAbsoluteHref(target, baseUrl);
    return `[${text}](${abs})`;
  });
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
      output += applyEmphasis(escapeHtml(rawText.slice(cursor, start)));
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

/**
 * Site-parity markdown → HTML (headings, p, lists, blockquote, hr, hard breaks).
 * Matches the geometry of build.mjs markdownToHtml for paste surfaces.
 */
export function markdownToHtml(markdownBody) {
  const lines = markdownBody.split(/\r?\n/);
  const chunks = [];

  let paragraph = [];
  let listType = null;
  let listItems = [];
  let listStart = null;
  let quoteLines = [];

  function lineHasHardBreak(rawLine) {
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

    if (/^(-{3,}|\*{3,}|_{3,})$/.test(trimmed)) {
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
      chunks.push(`<figure class="body-figure"><img src="${escapeHtml(src)}" alt="${escapeHtml(alt)}" loading="lazy" decoding="async"></figure>`);
      continue;
    }

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
      if (listType && listType !== 'ul') flushList();
      listType = 'ul';
      listStart = null;
      listItems.push(unorderedMatch[1]);
      continue;
    }

    const orderedMatch = /^(\d+)\.\s+(.+)$/.exec(trimmed);
    if (orderedMatch) {
      flushParagraph();
      flushQuote();
      if (listType && listType !== 'ol') flushList();
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

/**
 * Full post HTML fragment for paste (document shell optional).
 * Absolute links already applied to `md` via toAbsoluteMarkdown.
 */
export function postMarkdownToHtmlFragment(md) {
  return markdownToHtml(md.trim());
}

export function wrapHtmlDocument(fragment, title = '') {
  const t = title ? escapeHtml(title) : '';
  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>${t}</title>
</head>
<body>
${fragment}
</body>
</html>
`;
}
