# Export / publish for X Articles

Living guide for projecting a site post into a native **X Article** without changing the source of truth.

| Related | Path |
|---------|------|
| Source posts | [`content/posts/`](../content/posts/) · authoring [`content/posts/README.md`](../content/posts/README.md) |
| Script | [`scripts/publish-x-article.mjs`](../scripts/publish-x-article.mjs) |
| Substack export (paste) | [`docs/export-for-substack.md`](export-for-substack.md) |
| Cover styles | [`assets/covers/STYLES.md`](../assets/covers/STYLES.md) |
| Local memory / sleep audit | [`docs/local-memory.md`](local-memory.md) |

## Principle

**One source, three consumers.**

| Consumer | Form | Where |
|----------|------|--------|
| This site (build) | Relative `[text](../slug/)` | `content/posts/<slug>.md` only |
| Substack / paste | Absolute markdown projection | `export-absolute-md.mjs` → `export/` |
| X Article | Draft.js `content_state` + Articles API | `publish-x-article.mjs` |

Never edit `content/posts/` to “fix” X. Never treat `export/*.x-article.json` or receipts as canon. The relative markdown file is the source; the script is the disposable projection.

`export/` is **gitignored**. Local dry-run payloads and publish receipts only.

## Requirements

1. **X Premium** on the publishing account (any Premium tier since Jan 2026).
2. **X developer app** with user OAuth 1.0a write access (pay-per-use billing as applicable).
3. Credentials (any one source):

   **Env vars**

   ```bash
   export X_API_KEY=...
   export X_API_KEY_SECRET=...
   export X_ACCESS_TOKEN=...
   export X_ACCESS_TOKEN_SECRET=...
   ```

   **Or JSON file** at `~/.config/x-api/credentials.json` (or `X_CREDENTIALS_PATH`):

   ```json
   {
     "api_key": "...",
     "api_key_secret": "...",
     "access_token": "...",
     "access_token_secret": "..."
   }
   ```

Official endpoints: [Articles introduction](https://docs.x.com/x-api/articles/introduction) — draft `POST /2/articles/draft`, publish `POST /2/articles/{id}/publish`. Body format is Draft.js-style `content_state` (snake_case), not markdown.

## Commands

```bash
# Dry-run: convert only, write export/<slug>.x-article.json (default)
node scripts/publish-x-article.mjs <slug>

# Create draft on X (does not go live)
node scripts/publish-x-article.mjs <slug> --draft

# Draft + publish in one shot
node scripts/publish-x-article.mjs <slug> --publish

# Publish a draft already created
node scripts/publish-x-article.mjs --publish-id <article_id>

# Skip cover / skip canonical footer
node scripts/publish-x-article.mjs <slug> --draft --no-cover --no-canonical
```

`<slug>` is the post filename without `.md`.

## What the script does

1. Reads `content/posts/<slug>.md`.
2. Takes the H1 as Article **title**; body starts after it (subtitle italic, lead, sections).
3. Converts markdown → `content_state`:
   - `##` / `###` → header-two / header-three
   - paragraphs, lists, blockquotes
   - `**bold**`, `*italic*`, links (internal `../slug/` → absolute site URLs)
   - bare `x.com/.../status/ID` lines → embedded post entities
   - fenced code → plain text blocks (X has no code-block type)
4. Optionally uploads `assets/covers/<slug>.{jpg,jpeg,png,webp}` as `tweet_image` cover.
5. Appends a one-line canonical footer: “Originally published at Not a ToE” (disable with `--no-canonical`).
6. **Default:** dry-run JSON only. **`--draft`:** create draft. **`--publish`:** draft then publish.

Operator-gated publish is intentional — same discipline as Substack paste.

## Recommended workflow

1. Ship the site post (commit + push) so absolute links and cover URLs resolve.
2. Dry-run and skim payload:

   ```bash
   node scripts/publish-x-article.mjs <slug>
   # inspect export/<slug>.x-article.json
   ```

3. Create a **draft** and review in the X UI:

   ```bash
   node scripts/publish-x-article.mjs <slug> --draft
   ```

4. Publish when satisfied:

   ```bash
   node scripts/publish-x-article.mjs --publish-id <article_id>
   ```

Receipt (article_id, post_id) is written to `export/<slug>.x-article.receipt.json` (gitignored).

## Cover media

Use the same file as the site cover: `assets/covers/<slug>.jpg`.

| Rule | Detail |
|------|--------|
| Aspect | **20:9** landscape (matches site install) |
| Size | **1280×576** (or equivalent 20:9 resized to that) |
| Source | One cover for site / Substack / X — see [`assets/covers/STYLES.md`](../assets/covers/STYLES.md) |

Do not substitute a square, portrait, or profile-banner crop for Article cover. If the site cover is wrong aspect, fix the cover asset first; do not invent a second image only for X.

## Checklist

1. [ ] `content/posts/<slug>.md` final (relative links only).
2. [ ] Cover at `assets/covers/<slug>.jpg` (20:9) if you want cover media on the Article.
3. [ ] Credentials loaded (env or `~/.config/x-api/credentials.json`).
4. [ ] X Premium active on the account that owns the access token.
5. [ ] Dry-run → `--draft` → review → `--publish-id` (or `--publish` when confident).
6. [ ] Do not commit `export/` payloads or receipts. Do not copy absolute URLs back into `content/posts/`.

## Failure modes

| Symptom | Cause | Fix |
|---------|--------|-----|
| Auth / 401 | Missing or wrong OAuth tokens | Check env / credentials.json; app must have write |
| **403 `client-not-enrolled` / Client Forbidden** | App not attached to an X API **Project**, or product lacks write/Articles | [Developer portal](https://developer.x.com/en/portal/dashboard): create Project → attach App → pay-per-use (or write-capable access) → re-issue user tokens if needed |
| Premium / forbidden on publish | Account not Premium | Subscribe Premium on the publishing user |
| Cover upload 503 / fails | Media endpoint hiccup, scope, or format | Script continues without cover; retry; check image size |
| Links look wrong | Pasted from source relative MD | Always run this script (or Substack export), not raw source |
| Code blocks plain | X `content_state` has no code type | Expected; keep code short or link out |
| “Two sources of truth” | Editing export JSON by hand | Delete export artifact; edit source; re-run |

## Site base URL

Hardcoded in the script as:

```text
https://powerpig99.github.io/not-a-toe/
```

If the host moves, update `SITE_BASE` in `scripts/publish-x-article.mjs` and this paragraph (same constant as Substack export).
