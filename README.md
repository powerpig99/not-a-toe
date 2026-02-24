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

This generates `public/` with:

- `index.html`
- `posts/<slug>/index.html` + `essay.md`
- `llms.txt` and `llms-full.txt`
- `sitemap.xml` and `robots.txt`
