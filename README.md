# Not a ToE

## Authoring contract

Guides (read these instead of re-deriving the workflow each time):

| Topic | Doc |
|-------|-----|
| Posts: structure, voice, cross-links, ship checklist | [`content/posts/README.md`](content/posts/README.md) |
| LLM markdown format (copy-paste prompt) | [`docs/essay-format.md`](docs/essay-format.md) |
| Cover style differentiation | [`assets/covers/STYLES.md`](assets/covers/STYLES.md) |
| Paste export (Substack + X Article) | [`docs/export-for-substack.md`](docs/export-for-substack.md) (one absolute-markdown file) |
| X Article API (parked) | [`docs/export-for-x-article.md`](docs/export-for-x-article.md) |
| Local memory / sleep audit / graphs | [`docs/local-memory.md`](docs/local-memory.md) — trackers: `node scripts/project-local-graph.mjs`; posts lattice: `node scripts/project-posts-graph.mjs` |

1. Add essays in `content/posts/*.md`.
2. The first line must be `# Title`.
3. Filename is the post slug and permalink (`/posts/<filename>/`).
4. Optional title/cover image: place `assets/covers/<slug>.jpg` (also `.jpeg`, `.png`, `.webp`) — landscape; prefer **20:9** (1280×576) when available, **16:9 as-is** OK (no forced crop). Same file for site, Substack, and X Article. Build copies it to `public/covers/`. Spec + style differentiation: [`assets/covers/STYLES.md`](assets/covers/STYLES.md).
5. Use the drafting spec in [`docs/essay-format.md`](docs/essay-format.md) as **reference** for site scaffold (subtitle, lead, sections). Full checklist + **refinement workflow** (operator draft is ground; surgical precision under `/ontological-clarity`; no rewrite/collapse into prior posts): [`content/posts/README.md`](content/posts/README.md).
6. Internal cross-links stay **relative** (`[title](../other-slug/)`) in source. After live, **always generate** the absolute-markdown paste file for Substack / X Article (detail: [`docs/export-for-substack.md`](docs/export-for-substack.md)). Generate is required on ship; **paste** is operator-only and may wait:

```bash
node scripts/export-absolute-md.mjs <slug>          # → export/<slug>.md (required after live)
```

## Publish (default)

CI builds and deploys Pages on push to `main`. **Push is not live** until Actions finishes and the post URL returns 200.

Full ship checklist (preflight → reverse links → push → `gh run watch` → live curl → **required** export generate): [`content/posts/README.md`](content/posts/README.md) § Ship checklist. “Finish the rest” means that full sequence — not site-only.

```bash
git add content/posts/<slug>.md
git commit -m "Add <title> essay"
git push origin main
gh run watch --exit-status
curl -sI "https://powerpig99.github.io/not-a-toe/posts/<slug>/" | head -1
# if no run starts: gh workflow run deploy.yml --ref main
node scripts/export-absolute-md.mjs <slug>   # required after live; paste is operator
```

## Local build (optional preflight)

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

Do not commit `public/` as source of truth. Social preview image is referenced from `assets/toe-bang.png` via metadata URL. The same file is also copied into `public/apple-touch-icon.png` for iOS Safari “Add to Home Screen”.
