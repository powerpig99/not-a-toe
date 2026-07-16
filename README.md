# Not a ToE

## Authoring contract

1. Add essays in `content/posts/*.md`.
2. The first line must be `# Title`.
3. Filename is the post slug and permalink (`/posts/<filename>/`).
4. Optional title/cover image: place `assets/covers/<slug>.jpg` (also `.jpeg`, `.png`, `.webp`). Build copies it to `public/covers/` and renders it above the title.
5. Use the drafting spec in [`docs/essay-format.md`](docs/essay-format.md) for standardized LLM output.
6. Internal cross-links stay **relative** (`[title](../other-slug/)`) in source. For Substack or other external paste, project absolute URLs without editing the source:

```bash
node scripts/export-absolute-md.mjs <slug>          # writes export/<slug>.md (gitignored)
node scripts/export-absolute-md.mjs <slug> --stdout # pipe to clipboard: | pbcopy
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

Social preview image is referenced from `assets/toe-bang.png` via metadata URL and is not copied into `public/`.
