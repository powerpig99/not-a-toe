# Export for Substack (and other external paste)

Living guide for projecting a site post into markdown with **absolute** links, without changing the source of truth.

| Related | Path |
|---------|------|
| Source posts | [`content/posts/`](../content/posts/) · authoring [`content/posts/README.md`](../content/posts/README.md) |
| Export script | [`scripts/export-absolute-md.mjs`](../scripts/export-absolute-md.mjs) |
| Cover styles | [`assets/covers/STYLES.md`](../assets/covers/STYLES.md) |
| Local memory / sleep audit | [`docs/local-memory.md`](local-memory.md) |

## Principle

**One source, two consumers.**

| Consumer | Link form | Where |
|----------|-----------|--------|
| This site (build) | Relative `[text](../slug/)` | `content/posts/<slug>.md` only |
| Substack / email / paste | Absolute `https://powerpig99.github.io/not-a-toe/posts/<slug>/` | **Projection** via script → `export/<slug>.md` or clipboard |

Never edit `content/posts/` to “fix” Substack. Never treat `export/` as editable canon. Relative vs absolute on the same document is a Capacity error if held as two sources of truth — the script is the disposable projection; the relative file is the source.

`export/` is **gitignored**. Local paste artifacts only.

## Command

```bash
# Write export/<slug>.md (gitignored)
node scripts/export-absolute-md.mjs <slug>

# Clipboard (macOS)
node scripts/export-absolute-md.mjs <slug> --stdout | pbcopy

# Custom path
node scripts/export-absolute-md.mjs <slug> -o /tmp/<slug>.md
```

`<slug>` is the post filename without `.md` (e.g. `what-always-listens-cannot-originate`).

On success the script prints:

- path written (or streams to stdout)
- source: `content/posts/<slug>.md`
- cover URL: `https://powerpig99.github.io/not-a-toe/covers/<slug>.jpg`
- live post: `https://powerpig99.github.io/not-a-toe/posts/<slug>/`

## What the script does

1. Reads `content/posts/<slug>.md` (must exist).
2. Rewrites markdown links:
   - Leaves `http(s)://`, `mailto:`, and `#...` unchanged.
   - Maps `../slug/`, `./slug/`, and bare relative post targets to  
     `https://powerpig99.github.io/not-a-toe/posts/<slug>/`.
3. Writes the projection; **does not modify** the source file.

Re-run after any edit to the source if you will re-paste into Substack.

## Substack paste workflow

There is no official auto-publish API in this repo. Operator paste is intentional.

1. **Ship the site first** (or ensure the post and cover are already on `main` / live). Absolute links and the cover URL only help readers once the GitHub Pages deploy has the assets.
2. **Export**

   ```bash
   node scripts/export-absolute-md.mjs <slug> --stdout | pbcopy
   ```

3. **Substack editor**
   - New post (or update existing).
   - Paste markdown (or paste then fix formatting if the editor mangles headings).
   - **Cover / social image:** upload `assets/covers/<slug>.jpg` locally (20:9 landscape, same file as site + X Article cover), or use the cover URL the script printed if Substack accepts remote images. Prefer re-upload so Substack holds its own copy (X/GitHub hotlink quirks).
   - Title: usually the same as `# Title` in the file; Substack title field is separate from body — paste body **without** duplicating a second H1 if the editor already has the title, or paste full file and delete the duplicate H1 as needed.
   - Subtitle: optional; can reuse the italic one-sentence line from the open.
4. **Publish** on Substack when ready. Site and Substack are parallel surfaces, not a single CMS.

### Title / H1 double-up

If Substack already has a title field:

- Paste from the first body paragraph / sections only, **or**
- Paste full export and remove the leading `# Title` so it isn’t repeated.

Subtitle italic line can stay as the first paragraph under the title.

## Checklist (Substack)

1. [ ] `content/posts/<slug>.md` final (relative links only).
2. [ ] Cover at `assets/covers/<slug>.jpg` if used (20:9 shared with site + X Article); site pushed so cover URL resolves.
3. [ ] `node scripts/export-absolute-md.mjs <slug>` (or `--stdout | pbcopy`).
4. [ ] Paste into Substack; fix H1 / cover; publish.
5. [ ] Do not commit `export/` (gitignored). Do not copy absolute URLs back into `content/posts/`.

## Inventory note

Files under `export/` are local and gitignored. Do not maintain a committed list of “exported slugs” here — re-export whenever the source changes and you need a fresh paste. Historical local files (if any) are disposable caches.

## Failure modes

| Symptom | Cause | Fix |
|---------|--------|-----|
| Relative links on Substack | Pasted from `content/posts/` instead of export | Re-run script; paste from `export/` or clipboard |
| Absolute links in site source | Hand-edited source for Substack | Revert to `../slug/`; re-export for paste |
| Cover 404 | Not deployed or wrong slug | Push cover + post; match filename to slug |
| Empty or wrong export | Typo in slug | File must exist as `content/posts/<slug>.md` |
| “Two sources of truth” drift | Editing `export/` by hand | Delete export file; edit source; re-export |

## Site base URL

Hardcoded in the script as:

```text
https://powerpig99.github.io/not-a-toe/
```

If the site host ever moves, update `SITE_BASE` in `scripts/export-absolute-md.mjs` and this paragraph.
