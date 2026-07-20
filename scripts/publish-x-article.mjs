#!/usr/bin/env node
/**
 * Project a post to an X Article (draft by default; publish only with --publish).
 * Source of truth stays content/posts/<slug>.md — this is a disposable projection.
 *
 * Usage:
 *   node scripts/publish-x-article.mjs <slug>                 # dry-run payload
 *   node scripts/publish-x-article.mjs <slug> --draft         # create X draft
 *   node scripts/publish-x-article.mjs <slug> --publish       # draft + publish
 *   node scripts/publish-x-article.mjs --publish-id <id>      # publish existing draft
 *   node scripts/publish-x-article.mjs <slug> --dry-run -o export/<slug>.x-article.json
 *
 * Auth (OAuth 1.0a user context) from env:
 *   X_API_KEY, X_API_KEY_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET
 * Or JSON file via X_CREDENTIALS_PATH / ~/.config/x-api/credentials.json:
 *   { "api_key", "api_key_secret", "access_token", "access_token_secret" }
 *
 * Requires X Premium on the publishing account for Articles.
 */
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const SITE_BASE = 'https://powerpig99.github.io/not-a-toe/';
const API_BASE = 'https://api.x.com';
const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const root = path.join(scriptDir, '..');
const postsDir = path.join(root, 'content', 'posts');
const coversDir = path.join(root, 'assets', 'covers');
const defaultOutDir = path.join(root, 'export');

// ─── CLI ─────────────────────────────────────────────────────────────────────

function usage(code = 1) {
  console.error(`Usage:
  node scripts/publish-x-article.mjs <slug> [--dry-run] [-o file]
  node scripts/publish-x-article.mjs <slug> --draft [--no-cover] [--no-canonical]
  node scripts/publish-x-article.mjs <slug> --publish [--no-cover] [--no-canonical]
  node scripts/publish-x-article.mjs --publish-id <article_id>

Flags:
  --dry-run       Build payload only (default if neither --draft nor --publish)
  --draft         Create draft Article on X (does not publish)
  --publish       Create draft and publish immediately
  --publish-id    Publish an existing draft by Article id
  --no-cover      Skip cover image upload
  --no-canonical  Omit trailing "Originally published at …" block
  -o <file>       Write payload JSON (dry-run or after draft) to path
  -h, --help      This help
`);
  process.exit(code);
}

const args = process.argv.slice(2);
if (args.length === 0 || args.includes('-h') || args.includes('--help')) usage(0);

const wantDraft = args.includes('--draft');
const wantPublish = args.includes('--publish');
const noCover = args.includes('--no-cover');
const noCanonical = args.includes('--no-canonical');
const publishIdIdx = args.indexOf('--publish-id');
const publishId = publishIdIdx !== -1 ? args[publishIdIdx + 1] : null;
const oIdx = args.indexOf('-o');
const outPath = oIdx !== -1 ? args[oIdx + 1] : null;
const dryRun = !wantDraft && !wantPublish && !publishId;

const positional = args.filter(
  (a, i) =>
    !a.startsWith('-') &&
    args[i - 1] !== '-o' &&
    args[i - 1] !== '--publish-id',
);
const slugArg = positional[0]?.replace(/\.md$/, '') || null;

if (publishId && !/^\d+$/.test(publishId)) {
  console.error('--publish-id requires a numeric Article id');
  process.exit(1);
}
if (!publishId && !slugArg) usage();
if (wantDraft && wantPublish) {
  console.error('Use either --draft or --publish, not both (use --publish for draft+publish).');
  process.exit(1);
}

// ─── Markdown helpers (shared geometry with export-absolute-md) ───────────────

function toAbsoluteHref(href, baseUrl = SITE_BASE) {
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

function findCover(slug) {
  for (const ext of ['.jpg', '.jpeg', '.png', '.webp']) {
    const p = path.join(coversDir, `${slug}${ext}`);
    if (fs.existsSync(p)) return p;
  }
  return null;
}

function parsePost(md) {
  const lines = md.replace(/\r\n/g, '\n').split('\n');
  let title = '';
  let i = 0;
  if (lines[0]?.startsWith('# ')) {
    title = lines[0].slice(2).trim();
    i = 1;
    while (i < lines.length && lines[i].trim() === '') i += 1;
  }
  const bodyLines = lines.slice(i);
  return { title, body: bodyLines.join('\n').trimEnd() + '\n' };
}

// ─── Inline markdown → text + style/entity ranges ────────────────────────────

/**
 * Parse a single line of inline markdown into plain text + DraftJS-style ranges.
 * Supports **bold**, *italic* / _italic_, ~~strike~~, [text](url).
 * Nested styles are best-effort (non-overlapping preferred).
 */
function parseInline(raw) {
  let s = raw;
  // Strip residual raw HTML
  s = s.replace(/<[^>]+>/g, '');

  const styles = [];
  const links = []; // { offset, length, url }
  let text = '';
  let i = 0;

  function push(str) {
    text += str;
  }

  while (i < s.length) {
    // link [label](url)
    if (s[i] === '[') {
      const close = s.indexOf('](', i);
      if (close !== -1) {
        const end = s.indexOf(')', close + 2);
        if (end !== -1) {
          const label = s.slice(i + 1, close);
          const url = s.slice(close + 2, end);
          const inner = parseInline(label);
          const start = text.length;
          // merge inner styles with offset
          for (const st of inner.styles) {
            styles.push({ offset: start + st.offset, length: st.length, style: st.style });
          }
          for (const lk of inner.links) {
            links.push({ offset: start + lk.offset, length: lk.length, url: lk.url });
          }
          // whole label is a link (outer wins for range length = full label text)
          const labelText = inner.text;
          push(labelText);
          links.push({
            offset: start,
            length: labelText.length,
            url: toAbsoluteHref(url),
          });
          i = end + 1;
          continue;
        }
      }
    }

    // bold **...**
    if (s.startsWith('**', i)) {
      const end = s.indexOf('**', i + 2);
      if (end !== -1) {
        const inner = parseInline(s.slice(i + 2, end));
        const start = text.length;
        for (const st of inner.styles) {
          styles.push({ offset: start + st.offset, length: st.length, style: st.style });
        }
        for (const lk of inner.links) {
          links.push({ offset: start + lk.offset, length: lk.length, url: lk.url });
        }
        styles.push({ offset: start, length: inner.text.length, style: 'bold' });
        push(inner.text);
        i = end + 2;
        continue;
      }
    }

    // strikethrough ~~...~~
    if (s.startsWith('~~', i)) {
      const end = s.indexOf('~~', i + 2);
      if (end !== -1) {
        const inner = parseInline(s.slice(i + 2, end));
        const start = text.length;
        for (const st of inner.styles) {
          styles.push({ offset: start + st.offset, length: st.length, style: st.style });
        }
        for (const lk of inner.links) {
          links.push({ offset: start + lk.offset, length: lk.length, url: lk.url });
        }
        styles.push({ offset: start, length: inner.text.length, style: 'strikethrough' });
        push(inner.text);
        i = end + 2;
        continue;
      }
    }

    // italic *...* (single asterisk, not bold)
    if (s[i] === '*' && s[i + 1] !== '*') {
      const end = s.indexOf('*', i + 1);
      if (end !== -1 && s[end + 1] !== '*') {
        const inner = parseInline(s.slice(i + 1, end));
        const start = text.length;
        for (const st of inner.styles) {
          styles.push({ offset: start + st.offset, length: st.length, style: st.style });
        }
        for (const lk of inner.links) {
          links.push({ offset: start + lk.offset, length: lk.length, url: lk.url });
        }
        styles.push({ offset: start, length: inner.text.length, style: 'italic' });
        push(inner.text);
        i = end + 1;
        continue;
      }
    }

    // italic _..._ (underscore, not inside words if possible)
    if (s[i] === '_' && s[i + 1] !== '_') {
      const end = s.indexOf('_', i + 1);
      if (end !== -1) {
        const inner = parseInline(s.slice(i + 1, end));
        const start = text.length;
        for (const st of inner.styles) {
          styles.push({ offset: start + st.offset, length: st.length, style: st.style });
        }
        for (const lk of inner.links) {
          links.push({ offset: start + lk.offset, length: lk.length, url: lk.url });
        }
        styles.push({ offset: start, length: inner.text.length, style: 'italic' });
        push(inner.text);
        i = end + 1;
        continue;
      }
    }

    // backticks: strip, keep text plain (no code block type on X)
    if (s[i] === '`') {
      const end = s.indexOf('`', i + 1);
      if (end !== -1) {
        push(s.slice(i + 1, end));
        i = end + 1;
        continue;
      }
    }

    push(s[i]);
    i += 1;
  }

  // Deduplicate link ranges that fully overlap (outer [label](url) + inner)
  const uniqLinks = [];
  for (const lk of links) {
    const dup = uniqLinks.find(
      (x) => x.offset === lk.offset && x.length === lk.length && x.url === lk.url,
    );
    if (!dup) uniqLinks.push(lk);
  }

  return { text, styles, links: uniqLinks };
}

function makeBlock(type, line, entities, entityKeyCounter) {
  const { text, styles, links } = parseInline(line);
  const block = {
    text,
    type,
    inline_style_ranges: styles.map((s) => ({
      offset: s.offset,
      length: s.length,
      style: s.style,
    })),
    entity_ranges: [],
  };

  const data = { urls: [], mentions: [], hashtags: [], cashtags: [] };

  for (const lk of links) {
    const key = entityKeyCounter.value;
    entityKeyCounter.value += 1;
    entities.push({
      key: String(key),
      value: {
        type: 'link',
        mutability: 'mutable',
        data: { url: lk.url },
      },
    });
    block.entity_ranges.push({
      key,
      offset: lk.offset,
      length: lk.length,
    });
    data.urls.push({
      from_index: lk.offset,
      to_index: lk.offset + lk.length,
      text: text.slice(lk.offset, lk.offset + lk.length),
    });
  }

  // Mentions / hashtags for live rendering
  const mentionRe = /@([A-Za-z0-9_]{1,15})\b/g;
  let m;
  while ((m = mentionRe.exec(text)) !== null) {
    data.mentions.push({
      from_index: m.index,
      to_index: m.index + m[0].length,
      text: m[0],
    });
  }
  const hashRe = /#([A-Za-z0-9_\u00C0-\u024F]+)/g;
  while ((m = hashRe.exec(text)) !== null) {
    data.hashtags.push({
      from_index: m.index,
      to_index: m.index + m[0].length,
      text: m[0],
    });
  }

  if (data.urls.length || data.mentions.length || data.hashtags.length || data.cashtags.length) {
    block.data = data;
  }

  return block;
}

/**
 * Convert essay body markdown to X content_state.
 * Skips leading H1 (title handled separately). Supports ##/###, lists, quotes, HR, paragraphs.
 */
function markdownToContentState(bodyMd, { canonicalUrl = null } = {}) {
  const lines = bodyMd.replace(/\r\n/g, '\n').split('\n');
  const blocks = [];
  const entities = [];
  const entityKeyCounter = { value: 0 };

  let para = [];
  let inFence = false;
  let fenceBuf = [];

  function flushPara() {
    if (!para.length) return;
    const joined = para.join(' ').replace(/\s+/g, ' ').trim();
    para = [];
    if (!joined) return;
    // Whole-paragraph italic wrapper (*...*) used for subtitles
    let line = joined;
    if (
      (line.startsWith('*') && line.endsWith('*') && !line.startsWith('**')) ||
      (line.startsWith('_') && line.endsWith('_') && !line.startsWith('__'))
    ) {
      // keep as italic via parseInline
    }
    blocks.push(makeBlock('unstyled', line, entities, entityKeyCounter));
  }

  function flushFence() {
    if (!fenceBuf.length) return;
    // X has no code block — emit as plain paragraphs
    for (const fl of fenceBuf) {
      blocks.push(makeBlock('unstyled', fl || ' ', entities, entityKeyCounter));
    }
    fenceBuf = [];
  }

  for (let li = 0; li < lines.length; li += 1) {
    const line = lines[li];

    if (line.trim().startsWith('```')) {
      if (inFence) {
        flushFence();
        inFence = false;
      } else {
        flushPara();
        inFence = true;
        fenceBuf = [];
      }
      continue;
    }
    if (inFence) {
      fenceBuf.push(line);
      continue;
    }

    // blank
    if (line.trim() === '') {
      flushPara();
      continue;
    }

    // HR
    if (/^(-{3,}|\*{3,}|_{3,})\s*$/.test(line.trim())) {
      flushPara();
      continue;
    }

    // ATX headings (body uses ## / ###; skip lone # if present)
    const hm = line.match(/^(#{1,3})\s+(.*)$/);
    if (hm) {
      flushPara();
      const level = hm[1].length;
      const type =
        level === 1 ? 'header-one' : level === 2 ? 'header-two' : 'header-three';
      blocks.push(makeBlock(type, hm[2].trim(), entities, entityKeyCounter));
      continue;
    }

    // blockquote
    if (line.trimStart().startsWith('>')) {
      flushPara();
      const q = line.replace(/^\s*>\s?/, '');
      // gather continued quote lines
      let qtext = q;
      while (li + 1 < lines.length && lines[li + 1].trimStart().startsWith('>')) {
        li += 1;
        qtext += ' ' + lines[li].replace(/^\s*>\s?/, '');
      }
      blocks.push(makeBlock('blockquote', qtext.trim(), entities, entityKeyCounter));
      continue;
    }

    // unordered list
    const ul = line.match(/^\s*[-*+]\s+(.*)$/);
    if (ul) {
      flushPara();
      blocks.push(makeBlock('unordered-list-item', ul[1], entities, entityKeyCounter));
      continue;
    }

    // ordered list
    const ol = line.match(/^\s*\d+\.\s+(.*)$/);
    if (ol) {
      flushPara();
      blocks.push(makeBlock('ordered-list-item', ol[1], entities, entityKeyCounter));
      continue;
    }

    // standalone x.com status URL → embed as post entity if pure URL line
    const statusM = line.trim().match(
      /^https?:\/\/(x\.com|twitter\.com)\/[^/]+\/status\/(\d+)(?:\?.*)?$/i,
    );
    if (statusM) {
      flushPara();
      const postId = statusM[2];
      const key = entityKeyCounter.value;
      entityKeyCounter.value += 1;
      entities.push({
        key: String(key),
        value: {
          type: 'post',
          mutability: 'immutable',
          data: { post_id: postId },
        },
      });
      blocks.push({
        text: ' ',
        type: 'atomic',
        entity_ranges: [{ key, offset: 0, length: 1 }],
        inline_style_ranges: [],
      });
      continue;
    }

    para.push(line.trim());
  }
  flushPara();
  if (inFence) flushFence();

  if (canonicalUrl) {
    blocks.push(
      makeBlock(
        'unstyled',
        `Originally published at [Not a ToE](${canonicalUrl}).`,
        entities,
        entityKeyCounter,
      ),
    );
  }

  // Ensure at least one block
  if (!blocks.length) {
    blocks.push({ text: ' ', type: 'unstyled', inline_style_ranges: [], entity_ranges: [] });
  }

  return { blocks, entities };
}

function buildArticlePayload(slug, sourceMd, { includeCanonical = true, coverMedia = null } = {}) {
  const { title, body } = parsePost(sourceMd);
  if (!title) {
    throw new Error(`Post has no H1 title: content/posts/${slug}.md`);
  }
  const canonicalUrl = includeCanonical
    ? new URL(`posts/${slug}/`, SITE_BASE).toString()
    : null;
  const content_state = markdownToContentState(body, { canonicalUrl });
  const payload = {
    title,
    content_state,
  };
  if (coverMedia) {
    payload.cover_media = coverMedia;
  }
  return payload;
}

// ─── OAuth 1.0a ──────────────────────────────────────────────────────────────

function loadCredentials() {
  const fromEnv = {
    api_key: process.env.X_API_KEY || process.env.TWITTER_API_KEY,
    api_key_secret: process.env.X_API_KEY_SECRET || process.env.TWITTER_API_KEY_SECRET,
    access_token: process.env.X_ACCESS_TOKEN || process.env.TWITTER_ACCESS_TOKEN,
    access_token_secret:
      process.env.X_ACCESS_TOKEN_SECRET || process.env.TWITTER_ACCESS_TOKEN_SECRET,
  };
  if (
    fromEnv.api_key &&
    fromEnv.api_key_secret &&
    fromEnv.access_token &&
    fromEnv.access_token_secret
  ) {
    return fromEnv;
  }

  const candidates = [
    process.env.X_CREDENTIALS_PATH,
    path.join(process.env.HOME || '', '.config/x-api/credentials.json'),
  ].filter(Boolean);

  for (const p of candidates) {
    if (!fs.existsSync(p)) continue;
    const j = JSON.parse(fs.readFileSync(p, 'utf8'));
    const creds = {
      api_key: j.api_key || j.consumer_key || j.X_API_KEY,
      api_key_secret: j.api_key_secret || j.consumer_secret || j.X_API_KEY_SECRET,
      access_token: j.access_token || j.X_ACCESS_TOKEN,
      access_token_secret: j.access_token_secret || j.X_ACCESS_TOKEN_SECRET,
    };
    if (
      creds.api_key &&
      creds.api_key_secret &&
      creds.access_token &&
      creds.access_token_secret
    ) {
      return creds;
    }
  }
  return null;
}

function percentEncode(s) {
  return encodeURIComponent(s).replace(/[!'()*]/g, (c) =>
    `%${c.charCodeAt(0).toString(16).toUpperCase()}`,
  );
}

function oauthHeader(method, url, creds, extraParams = {}) {
  const oauth = {
    oauth_consumer_key: creds.api_key,
    oauth_nonce: crypto.randomBytes(16).toString('hex'),
    oauth_signature_method: 'HMAC-SHA1',
    oauth_timestamp: Math.floor(Date.now() / 1000).toString(),
    oauth_token: creds.access_token,
    oauth_version: '1.0',
  };
  const all = { ...oauth, ...extraParams };
  const paramString = Object.keys(all)
    .sort()
    .map((k) => `${percentEncode(k)}=${percentEncode(String(all[k]))}`)
    .join('&');
  const base = [method.toUpperCase(), percentEncode(url), percentEncode(paramString)].join('&');
  const signingKey = `${percentEncode(creds.api_key_secret)}&${percentEncode(creds.access_token_secret)}`;
  const signature = crypto.createHmac('sha1', signingKey).update(base).digest('base64');
  oauth.oauth_signature = signature;
  const header =
    'OAuth ' +
    Object.keys(oauth)
      .sort()
      .map((k) => `${percentEncode(k)}="${percentEncode(oauth[k])}"`)
      .join(', ');
  return header;
}

async function xFetch(method, urlPath, creds, { json = null, form = null } = {}) {
  const url = urlPath.startsWith('http') ? urlPath : `${API_BASE}${urlPath}`;
  const headers = {
    Authorization: oauthHeader(method, url.split('?')[0], creds),
  };
  const init = { method, headers };
  if (json !== null) {
    headers['Content-Type'] = 'application/json';
    init.body = JSON.stringify(json);
  } else if (form !== null) {
    // multipart: do not set Content-Type (boundary auto)
    init.body = form;
  }
  const res = await fetch(url, init);
  const text = await res.text();
  let body;
  try {
    body = text ? JSON.parse(text) : null;
  } catch {
    body = { raw: text };
  }
  if (!res.ok) {
    const err = new Error(`X API ${method} ${urlPath} → ${res.status}`);
    err.status = res.status;
    err.body = body;
    err.hint = hintForXError(res.status, body);
    throw err;
  }
  return body;
}

function hintForXError(status, body) {
  const reason = body?.reason || body?.title || '';
  const detail = body?.detail || '';
  if (
    status === 403 ||
    /client-not-enrolled|Client Forbidden|attached to a Project/i.test(
      `${reason} ${detail} ${body?.type || ''}`,
    )
  ) {
    return (
      'Developer App is not enrolled in an X API Project (or lacks write/Articles access).\n' +
      '  → https://developer.x.com/en/portal/dashboard — create/open a Project, attach this App,\n' +
      '    enable pay-per-use (or a write-capable product), regenerate user access tokens if needed.\n' +
      '  → Publishing account also needs X Premium for Articles.'
    );
  }
  if (status === 401) {
    return 'Check X_API_KEY / X_API_KEY_SECRET / X_ACCESS_TOKEN / X_ACCESS_TOKEN_SECRET (OAuth 1.0a user context).';
  }
  if (status === 402 || /usage|cap|billing/i.test(detail)) {
    return 'Billing/usage issue on the X developer account — check pay-per-use balance in the portal.';
  }
  if (/premium|Premium|subscription/i.test(`${detail} ${reason}`)) {
    return 'Publishing account needs an active X Premium subscription for Articles.';
  }
  return null;
}

async function uploadCover(creds, coverPath) {
  const buf = fs.readFileSync(coverPath);
  const ext = path.extname(coverPath).toLowerCase();
  const mediaType =
    ext === '.png'
      ? 'image/png'
      : ext === '.webp'
        ? 'image/webp'
        : 'image/jpeg';

  // JSON one-shot upload with base64 media
  const body = await xFetch('POST', '/2/media/upload', creds, {
    json: {
      media: buf.toString('base64'),
      media_category: 'tweet_image',
      media_type: mediaType,
    },
  });
  const mediaId = body?.data?.id || body?.id || body?.media_id_string;
  if (!mediaId) {
    throw new Error(`Media upload returned no id: ${JSON.stringify(body)}`);
  }
  return {
    media_category: 'tweet_image',
    media_id: String(mediaId),
  };
}

// ─── Main ────────────────────────────────────────────────────────────────────

async function main() {
  if (publishId) {
    const creds = loadCredentials();
    if (!creds) {
      console.error(
        'Missing X OAuth credentials. Set X_API_KEY, X_API_KEY_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET\n' +
          'or place JSON at ~/.config/x-api/credentials.json',
      );
      process.exit(1);
    }
    console.log(`Publishing existing draft article_id=${publishId} …`);
    const pub = await xFetch('POST', `/2/articles/${publishId}/publish`, creds);
    const postId = pub?.data?.post_id;
    console.log('Published.');
    console.log(`article_id: ${publishId}`);
    if (postId) {
      console.log(`post_id:    ${postId}`);
      console.log(`post_url:   https://x.com/i/status/${postId}`);
    }
    return;
  }

  const slug = slugArg;
  const srcPath = path.join(postsDir, `${slug}.md`);
  if (!fs.existsSync(srcPath)) {
    console.error(`Post not found: content/posts/${slug}.md`);
    process.exit(1);
  }
  const source = fs.readFileSync(srcPath, 'utf8');
  const coverPath = noCover ? null : findCover(slug);

  let coverMedia = null;
  let payload;

  if (dryRun) {
    // Placeholder cover ref so operator sees field shape when cover exists
    if (coverPath) {
      coverMedia = {
        media_category: 'tweet_image',
        media_id: '<upload-on-draft>',
        _local_path: path.relative(root, coverPath),
      };
    }
    payload = buildArticlePayload(slug, source, {
      includeCanonical: !noCanonical,
      coverMedia: coverMedia
        ? { media_category: coverMedia.media_category, media_id: coverMedia.media_id }
        : null,
    });
    // Attach debug meta only in dry-run file, not in API body shape dump
    const dump = {
      _meta: {
        slug,
        source: `content/posts/${slug}.md`,
        cover: coverPath ? path.relative(root, coverPath) : null,
        live: `${SITE_BASE}posts/${slug}/`,
        blocks: payload.content_state.blocks.length,
        entities: payload.content_state.entities.length,
        mode: 'dry-run',
      },
      ...payload,
      ...(coverMedia?._local_path
        ? {
            cover_media: {
              media_category: 'tweet_image',
              media_id: '<upload-on-draft>',
              _local_path: coverMedia._local_path,
            },
          }
        : {}),
    };
    const json = JSON.stringify(dump, null, 2) + '\n';
    const dest =
      outPath ||
      (() => {
        fs.mkdirSync(defaultOutDir, { recursive: true });
        return path.join(defaultOutDir, `${slug}.x-article.json`);
      })();
    if (outPath === '-') {
      process.stdout.write(json);
    } else {
      fs.writeFileSync(dest, json);
      console.log(`Dry-run payload: ${path.relative(root, dest)}`);
      console.log(`Title:   ${payload.title}`);
      console.log(`Blocks:  ${payload.content_state.blocks.length}`);
      console.log(`Entities:${payload.content_state.entities.length}`);
      console.log(`Cover:   ${coverPath ? path.relative(root, coverPath) : '(none)'}`);
      console.log(`Source:  content/posts/${slug}.md`);
      console.log(`Live:    ${SITE_BASE}posts/${slug}/`);
      console.log('');
      console.log('Next: node scripts/publish-x-article.mjs ' + slug + ' --draft');
      console.log('Then: node scripts/publish-x-article.mjs ' + slug + ' --publish');
      console.log('  or: node scripts/publish-x-article.mjs --publish-id <article_id>');
    }
    return;
  }

  // Live draft / publish
  const creds = loadCredentials();
  if (!creds) {
    console.error(
      'Missing X OAuth credentials. Set X_API_KEY, X_API_KEY_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET\n' +
        'or place JSON at ~/.config/x-api/credentials.json',
    );
    process.exit(1);
  }

  if (coverPath) {
    console.log(`Uploading cover ${path.relative(root, coverPath)} …`);
    try {
      coverMedia = await uploadCover(creds, coverPath);
      console.log(`Cover media_id=${coverMedia.media_id}`);
    } catch (e) {
      console.error('Cover upload failed:', e.message);
      if (e.body) console.error(JSON.stringify(e.body, null, 2));
      console.error('Continuing without cover. Use --no-cover to silence this path.');
      coverMedia = null;
    }
  }

  payload = buildArticlePayload(slug, source, {
    includeCanonical: !noCanonical,
    coverMedia,
  });

  if (outPath) {
    fs.writeFileSync(
      outPath,
      JSON.stringify({ _meta: { slug, mode: wantPublish ? 'publish' : 'draft' }, ...payload }, null, 2) +
        '\n',
    );
  }

  console.log(`Creating draft Article: ${payload.title}`);
  let draft;
  try {
    draft = await xFetch('POST', '/2/articles/draft', creds, { json: payload });
  } catch (e) {
    console.error('Draft create failed:', e.message);
    if (e.body) console.error(JSON.stringify(e.body, null, 2));
    if (e.hint) console.error('\n' + e.hint);
    process.exit(1);
  }
  const articleId = draft?.data?.id;
  console.log(`Draft created. article_id=${articleId}`);
  console.log(`Title: ${draft?.data?.title || payload.title}`);

  // Save receipt (gitignored under export/)
  fs.mkdirSync(defaultOutDir, { recursive: true });
  const receiptPath = path.join(defaultOutDir, `${slug}.x-article.receipt.json`);
  const receipt = {
    slug,
    article_id: articleId,
    title: payload.title,
    cover_media: coverMedia,
    created_at: new Date().toISOString(),
    published: false,
    post_id: null,
  };
  fs.writeFileSync(receiptPath, JSON.stringify(receipt, null, 2) + '\n');
  console.log(`Receipt: ${path.relative(root, receiptPath)}`);

  if (!wantPublish) {
    console.log('');
    console.log('Draft only. Review on X, then:');
    console.log(`  node scripts/publish-x-article.mjs --publish-id ${articleId}`);
    console.log(`  # or re-run with --publish (creates a new draft)`);
    return;
  }

  console.log('Publishing …');
  try {
    const pub = await xFetch('POST', `/2/articles/${articleId}/publish`, creds);
    const postId = pub?.data?.post_id;
    receipt.published = true;
    receipt.post_id = postId || null;
    receipt.published_at = new Date().toISOString();
    fs.writeFileSync(receiptPath, JSON.stringify(receipt, null, 2) + '\n');
    console.log('Published.');
    if (postId) {
      console.log(`post_id:  ${postId}`);
      console.log(`post_url: https://x.com/i/status/${postId}`);
    }
  } catch (e) {
    console.error('Publish failed:', e.message);
    if (e.body) console.error(JSON.stringify(e.body, null, 2));
    console.error(`Draft remains article_id=${articleId}`);
    process.exit(1);
  }
}

main().catch((e) => {
  console.error(e.stack || e.message || e);
  process.exit(1);
});
