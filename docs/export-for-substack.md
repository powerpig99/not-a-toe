# Export for Substack and X Article (rich paste)

Living guide for projecting a site post into **formatted paste** (headings, emphasis, links) without changing the source of truth. Same path for **Substack** and **X Article** body paste.

| Related | Path |
|---------|------|
| Source posts | [`content/posts/`](../content/posts/) · authoring [`content/posts/README.md`](../content/posts/README.md) |
| Export script | [`scripts/export-absolute-md.mjs`](../scripts/export-absolute-md.mjs) · helpers [`scripts/lib/post-markdown.mjs`](../scripts/lib/post-markdown.mjs) |
| X Article (API parked) | [`docs/export-for-x-article.md`](export-for-x-article.md) |
| Cover styles | [`assets/covers/STYLES.md`](../assets/covers/STYLES.md) |
| Local memory / sleep audit | [`docs/local-memory.md`](local-memory.md) |

## Principle

**One source, one paste projection.**

| Consumer | Link / form | Where |
|----------|-------------|--------|
| This site (build) | Relative `[text](../slug/)` | `content/posts/<slug>.md` only |
| Substack / X Article body | Absolute links, **rendered rich text** on clipboard | `export-absolute-md.mjs --rich` |

Never edit `content/posts/` to “fix” external editors. Never treat `export/` as editable canon. The script is the disposable projection; the relative file is the source.

`export/` is **gitignored**. Local paste artifacts only.

Plain markdown on the clipboard does **not** auto-render in Substack or the X Article editor — both want paste that already carries formatting. Use `--rich` (HTML → RTF → macOS clipboard).

## Command

```bash
# Default for Substack + X Article paste (macOS)
node scripts/export-absolute-md.mjs <slug> --rich --no-title

# Keep leading H1 in the paste (if the editor has no separate title field)
node scripts/export-absolute-md.mjs <slug> --rich

# Absolute markdown file only (gitignored; editors will show raw markdown)
node scripts/export-absolute-md.mjs <slug>

# HTML fragment file / stdout
node scripts/export-absolute-md.mjs <slug> --html
node scripts/export-absolute-md.mjs <slug> --html --stdout

# Custom path (markdown)
node scripts/export-absolute-md.mjs <slug> -o /tmp/<slug>.md
```

`<slug>` is the post filename without `.md` (e.g. `hierarchy-from-individual-difference`).

On success `--rich` prints:

- confirmation that RTF is on the clipboard
- `export/<slug>.html` written (debug / re-paste helper)
- source, cover URL, live post URL

## What `--rich` does

1. Reads `content/posts/<slug>.md` (must exist).
2. Rewrites relative post links to absolute site URLs.
3. Renders markdown → HTML (headings, paragraphs, emphasis, links, lists, blockquotes).
4. Converts HTML → RTF via macOS `textutil` and copies to the clipboard via `pbcopy`.
5. Also writes `export/<slug>.html` (gitignored). **Does not modify** the source file.

Re-run after any edit to the source if you will re-paste.

## Paste workflow (Substack and X Article)

1. **Ship the site first** so absolute links and cover URLs resolve on Pages.
2. **Export**

   ```bash
   node scripts/export-absolute-md.mjs <slug> --rich --no-title
   ```

3. **Editor**
   - Set **title** in the platform title field.
   - **Paste** (⌘V) into the body — not “Paste and Match Style.”
   - **Cover:** upload `assets/covers/<slug>.jpg` (20:9) from disk; prefer local re-upload over hotlinking.
   - Subtitle: optional; italic open line is already in the paste when present.
4. **Publish** when ready. Site, Substack, and X Article are parallel surfaces, not one CMS.

### Title / H1 double-up

If the editor has a title field (both Substack and X Article do):

- Prefer `--no-title` so the leading `# Title` is omitted from the paste.
- Or paste full export and delete a duplicate H1 in the body.

## Checklist

1. [ ] `content/posts/<slug>.md` final (relative links only).
2. [ ] Cover at `assets/covers/<slug>.jpg` if used; site live so cover URL resolves.
3. [ ] `node scripts/export-absolute-md.mjs <slug> --rich --no-title`
4. [ ] Paste into Substack and/or X Article body; set title; upload cover; publish.
5. [ ] Do not commit `export/`. Do not copy absolute URLs back into `content/posts/`.

## Inventory note

Files under `export/` are local and gitignored. Do not maintain a committed list of exported slugs — re-export when the source changes and you need a fresh paste.

## Failure modes

| Symptom | Cause | Fix |
|---------|--------|-----|
| Raw markdown in editor | Pasted absolute `.md` or plain text | Use `--rich`; avoid “Match Style” |
| Relative links | Pasted from `content/posts/` | Re-run script |
| Absolute links in site source | Hand-edited source for paste | Revert to `../slug/`; re-export |
| Flat paste (no formatting) | Clipboard only plain text | Re-run `--rich` on macOS; paste into empty block |
| Cover 404 | Not deployed or wrong slug | Push cover + post; match filename |
| “Two sources of truth” drift | Editing `export/` by hand | Delete export file; edit source; re-export |

## Site base URL

Hardcoded in `scripts/lib/post-markdown.mjs` as:

```text
https://powerpig99.github.io/not-a-toe/
```

If the site host ever moves, update `SITE_BASE` there and this paragraph.
