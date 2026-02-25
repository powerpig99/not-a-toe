# Not a ToE

## Authoring contract

1. Add essays in `content/posts/*.md`.
2. The first line must be `# Title`.
3. Filename is the post slug and permalink (`/posts/<filename>/`).

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
- `sitemap.xml` and `robots.txt`

Social preview image is referenced from `assets/toe-bang.png` via metadata URL and is not copied into `public/`.
