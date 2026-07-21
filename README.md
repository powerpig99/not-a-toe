# Not a ToE

## Authoring contract

Guides (read these instead of re-deriving the workflow each time):

| Topic | Doc |
|-------|-----|
| Posts: structure, voice, cross-links, ship checklist | [`content/posts/README.md`](content/posts/README.md) |
| LLM markdown format (copy-paste prompt) | [`docs/essay-format.md`](docs/essay-format.md) |
| Cover style differentiation | [`assets/covers/STYLES.md`](assets/covers/STYLES.md) |
| Substack / external export | [`docs/export-for-substack.md`](docs/export-for-substack.md) |
| X Article publish | [`docs/export-for-x-article.md`](docs/export-for-x-article.md) |
| Local memory / sleep audit / graphs | [`docs/local-memory.md`](docs/local-memory.md) — trackers: `node scripts/project-local-graph.mjs`; posts lattice: `node scripts/project-posts-graph.mjs` |

1. Add essays in `content/posts/*.md`.
2. The first line must be `# Title`.
3. Filename is the post slug and permalink (`/posts/<filename>/`).
4. Optional title/cover image: place `assets/covers/<slug>.jpg` (also `.jpeg`, `.png`, `.webp`) as **16:9** landscape (1280×720) — same file for site, Substack, and X Article cover. Build copies it to `public/covers/` and renders it above the title. **New covers need a style not already in** [`assets/covers/STYLES.md`](assets/covers/STYLES.md).
5. Use the drafting spec in [`docs/essay-format.md`](docs/essay-format.md) for standardized LLM output; full checklist in [`content/posts/README.md`](content/posts/README.md).
6. Internal cross-links stay **relative** (`[title](../other-slug/)`) in source. For Substack or other external paste, project absolute URLs without editing the source (detail: [`docs/export-for-substack.md`](docs/export-for-substack.md)):

```bash
node scripts/export-absolute-md.mjs <slug>          # writes export/<slug>.md (gitignored)
node scripts/export-absolute-md.mjs <slug> --stdout # pipe to clipboard: | pbcopy

# X Article (dry-run default; --draft then --publish-id when ready)
node scripts/publish-x-article.mjs <slug>
node scripts/publish-x-article.mjs <slug> --draft
```

## Publish (default)

For normal publishing, just commit and push. GitHub Actions handles mtime restore and build:

```bash
git add content/posts/<slug>.md
git commit -m "Add <title> essay"
git push origin main
```

## Local build (optional)

Run:

```bash
node build.mjs
```

For deterministic local checks (no stale `public/` reads), run the build and check in one command:

```bash
node build.mjs && rg -n "style.css\\?v=" public/index.html
```

This generates `public/` with:

- `index.html`
- `posts/<slug>/index.html`
- `posts.json` and `posts.jsonl` (machine-readable post index with source markdown URLs)
- `sitemap.xml` and `robots.txt`

Social preview image is referenced from `assets/toe-bang.png` via metadata URL. The same file is also copied into `public/apple-touch-icon.png` for iOS Safari “Add to Home Screen”.
