# Export for Substack

Project a site post to markdown with **absolute** links for Substack. That is the only paste export.

| Related | Path |
|---------|------|
| Source posts | [`content/posts/`](../content/posts/) · authoring [`content/posts/README.md`](../content/posts/README.md) |
| Script | [`scripts/export-absolute-md.mjs`](../scripts/export-absolute-md.mjs) · helpers [`scripts/lib/post-markdown.mjs`](../scripts/lib/post-markdown.mjs) |
| Cover styles | [`assets/covers/STYLES.md`](../assets/covers/STYLES.md) |
| Local memory | [`docs/local-memory.md`](local-memory.md) |

## Principle

| Consumer | Form | Where |
|----------|------|--------|
| Site | Relative `[text](../slug/)` | `content/posts/<slug>.md` |
| Substack | Absolute links | `export/<slug>.md` via script |

Never edit source to “fix” Substack. Never treat `export/` as canon. Site HTML is `public/` via build only — not this export.

`export/` is gitignored. Artifact: **one absolute-markdown file per slug**.

## Command

```bash
node scripts/export-absolute-md.mjs <slug>
# → export/<slug>.md
```

Optional: `--stdout`, or `-o <path>`. No other modes.

`<slug>` = filename without `.md`. Re-run after source edits when you will re-paste.

## Substack paste (operator)

1. Ship the site so absolute links resolve.
2. `node scripts/export-absolute-md.mjs <slug>`
3. Open `export/<slug>.md` in a markdown previewer (e.g. MacDown); copy from the **rendered** preview into Substack (plain markdown does not auto-render).
4. Upload cover from `assets/covers/<slug>.jpg` if used; publish.

## Site base URL

In `scripts/lib/post-markdown.mjs`:

```text
https://powerpig99.github.io/not-a-toe/
```

Update `SITE_BASE` there if the host moves.
