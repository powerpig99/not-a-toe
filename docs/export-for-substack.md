# Export for Substack and X Article

One projection: site post → markdown with **absolute** links. Same file for **Substack** and **X Article** body paste. No separate X export.

| Related | Path |
|---------|------|
| Source posts | [`content/posts/`](../content/posts/) · authoring / full ship [`content/posts/README.md`](../content/posts/README.md) |
| Script | [`scripts/export-absolute-md.mjs`](../scripts/export-absolute-md.mjs) · helpers [`scripts/lib/post-markdown.mjs`](../scripts/lib/post-markdown.mjs) |
| X Article API (parked; not this export) | [`docs/export-for-x-article.md`](export-for-x-article.md) |
| Cover styles | [`assets/covers/STYLES.md`](../assets/covers/STYLES.md) |
| Local memory | [`docs/local-memory.md`](local-memory.md) |

## Principle

| Consumer | Form | Where |
|----------|------|--------|
| Site | Relative `[text](../slug/)` | `content/posts/<slug>.md` |
| Substack / X Article paste | Absolute links | `export/<slug>.md` via script |

Never edit source to “fix” external editors. Never treat `export/` as canon. Site HTML is `public/` via build only — not this export.

`export/` is gitignored. Artifact: **one absolute-markdown file per slug**, shared by both surfaces.

### Generate vs paste (do not conflate)

| Act | Required on ship? | Who |
|-----|-------------------|-----|
| **Generate** `export/<slug>.md` after live | **Yes** — part of full finish / “finish the rest” | Agent |
| **Paste** into Substack / X Article (+ cover upload there) | Operator timing | Operator only |

“If I might not post to Substack yet” is **not** a reason to skip generation. The export file is the finish artifact; paste can wait. Full ship order: [`content/posts/README.md`](../content/posts/README.md) § Ship checklist.

## Command

```bash
node scripts/export-absolute-md.mjs <slug>
# → export/<slug>.md
```

Optional: `--stdout`, or `-o <path>`. No other modes.

`<slug>` = filename without `.md`. Re-run after same-slug source edits when the external paste will be updated.

## Ship sequence (agent)

1. Site live: post URL (and cover if any) return 200 — ship checklist steps 1–4.
2. **Required:** `node scripts/export-absolute-md.mjs <slug>` → `export/<slug>.md`.
3. Ship is finished for the agent. Do not leave generation as a “maybe later” offer.

## Paste (operator only)

1. Confirm site is live so absolute links resolve.
2. Confirm `export/<slug>.md` exists (agent should have generated it on ship).
3. Open `export/<slug>.md` in a markdown previewer (e.g. MacDown); copy from the **rendered** preview into Substack and/or X Article (plain markdown does not auto-render).
4. Upload cover from `assets/covers/<slug>.jpg` if used; publish.

## Site base URL

In `scripts/lib/post-markdown.mjs`:

```text
https://powerpig99.github.io/not-a-toe/
```

Update `SITE_BASE` there if the host moves.
