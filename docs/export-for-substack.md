# Export for Substack and X Article

Living guide for projecting a site post into markdown with **absolute** links, then pasting **rendered** rich text from a markdown previewer (MacDown). Same path for **Substack** and **X Article** body paste.

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
| Substack / X Article body | Absolute links; **rendered** paste from MacDown (or equivalent) | `export/<slug>.md` via script |

Never edit `content/posts/` to “fix” external editors. Never treat `export/` as editable canon. The script is the disposable projection; the relative file is the source.

`export/` is **gitignored**. Local paste artifacts only.

Plain markdown on the clipboard does **not** auto-render in Substack or the X Article editor. The default path is: absolute `.md` → open in MacDown → copy from the **preview** (rendered HTML) → paste into the editor.

## Command

```bash
# Default: write export/<slug>.md (absolute links; gitignored)
node scripts/export-absolute-md.mjs <slug>

# Clipboard as raw markdown (macOS) — usually open the file in MacDown instead
node scripts/export-absolute-md.mjs <slug> --stdout | pbcopy

# Custom path
node scripts/export-absolute-md.mjs <slug> -o /tmp/<slug>.md

# Optional: RTF clipboard without MacDown (escape hatch)
node scripts/export-absolute-md.mjs <slug> --rich --no-title

# Optional: HTML fragment file / stdout
node scripts/export-absolute-md.mjs <slug> --html
node scripts/export-absolute-md.mjs <slug> --html --stdout
```

`<slug>` is the post filename without `.md` (e.g. `when-observation-becomes-performance`).

On success the default path prints:

- path of `export/<slug>.md`
- source, cover URL, live post URL

Re-run after any edit to the source if you will re-paste.

## Paste workflow (Substack and X Article)

1. **Ship the site first** so absolute links and cover URLs resolve on Pages.
2. **Export**

   ```bash
   node scripts/export-absolute-md.mjs <slug>
   open -a MacDown export/<slug>.md   # or open in your previewer
   ```

3. **MacDown**
   - Open the preview (rendered view).
   - Select all in the **preview** and copy (not the raw markdown pane).
   - The export keeps the leading `# Title` — leave it in the paste.
4. **Editor**
   - **Paste** (⌘V) into the body — not “Paste and Match Style.”
   - Keep the title heading from the export (do not strip the H1).
   - Platform title field: set if the editor requires it separately; still keep the in-body title.
   - **Cover:** upload `assets/covers/<slug>.jpg` (20:9) from disk; prefer local re-upload over hotlinking.
   - Subtitle: optional; italic open line is already in the export when present.
5. **Publish** when ready. Site, Substack, and X Article are parallel surfaces, not one CMS.

## Optional: `--rich` (RTF clipboard)

macOS only. Renders markdown → HTML → RTF via `textutil` and copies to the clipboard. Use when MacDown is unavailable; prefer MacDown when it is. Keeps the leading H1 by default.

```bash
node scripts/export-absolute-md.mjs <slug> --rich
# optional: --no-title only if you deliberately want the H1 dropped
```

Also writes `export/<slug>.html` as a debug helper. **Does not modify** the source file.

## Checklist

1. [ ] `content/posts/<slug>.md` final (relative links only).
2. [ ] Cover at `assets/covers/<slug>.jpg` if used; site live so cover URL resolves.
3. [ ] `node scripts/export-absolute-md.mjs <slug>`
4. [ ] Open `export/<slug>.md` in MacDown; copy from **preview**; paste into Substack and/or X Article; set title; upload cover; publish.
5. [ ] Do not commit `export/`. Do not copy absolute URLs back into `content/posts/`.

## Inventory note

Files under `export/` are local and gitignored. Do not maintain a committed list of exported slugs — re-export when the source changes and you need a fresh paste.

## Failure modes

| Symptom | Cause | Fix |
|---------|--------|-----|
| Raw markdown in editor | Copied from source pane, not preview | Copy from MacDown **preview** |
| Relative links | Pasted from `content/posts/` | Re-run script; use `export/<slug>.md` |
| Absolute links in site source | Hand-edited source for paste | Revert to `../slug/`; re-export |
| Flat paste (no formatting) | “Paste and Match Style” or plain-text clipboard | Paste ordinary; or re-copy from preview |
| Cover 404 | Not deployed or wrong slug | Push cover + post; match filename |
| “Two sources of truth” drift | Editing `export/` by hand | Delete export file; edit source; re-export |

## Site base URL

Hardcoded in `scripts/lib/post-markdown.mjs` as:

```text
https://powerpig99.github.io/not-a-toe/
```

If the site host ever moves, update `SITE_BASE` there and this paragraph.
