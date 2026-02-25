# Not a ToE

## Authoring contract

1. Add essays in `content/posts/*.md`.
2. The first line must be `# Title`.
3. Filename is the post slug and permalink (`/posts/<filename>/`).

## Build

Run:

```bash
scripts/restore-post-mtimes.sh
node build.mjs
```

For deterministic local checks (no stale `public/` reads), run the build and check in one command:

```bash
scripts/restore-post-mtimes.sh && node build.mjs && rg -n "style.css\\?v=" public/index.html
```

This generates `public/` with:

- `index.html`
- `posts/<slug>/index.html`
- `sitemap.xml` and `robots.txt`

Social preview image is referenced from `assets/toe-bang.png` via metadata URL and is not copied into `public/`.
