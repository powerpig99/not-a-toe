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

1. Add essays in `content/posts/<slug>.md` (bilingual `# Title`, italic single-sentence subtitle, alternating paragraphs, zero lists).
2. Live Book Placement: Assign to exactly one part in `content/book/<part>.md` (placed last in written order); add or extend substantive entries in `content/book/index-of-premises.md` (label from 8 families, bilingual premise sentences, `→` link).
3. Filename is the post slug and permalink (`/posts/<slug>/`).
4. Cover image: place `assets/covers/<slug>.jpg` — ultra-wide **21:9** landscape (`1344×576`, Qwen-Image-2.1 MPS; 20:9 `1280×576` fallback). Content-driven novel artistic style registered in [`assets/covers/STYLES.md`](assets/covers/STYLES.md).
5. Companion NotebookLM Prompts: Chinese Audio Dialogue (`< 8.5 KB`, 2–4 opening turns with canonical opening) and Video Monologue (compact spoken script, ~9 KB) under `notebooklm-auto/prompts/`.
6. Use the drafting spec in [`docs/essay-format.md`](docs/essay-format.md) as **reference** for site scaffold. Full checklist + **refinement workflow** + **lattice consistency**: [`content/posts/README.md`](content/posts/README.md).
7. Internal cross-links stay **relative** (`[title](../other-slug/)`).
8. Preflight validation:
   - `python3 scripts/audit-post.py <slug>` (CLEAN PASS across all 10 invariants).
   - `python3 scripts/audit-book.py` (CLEAN PASS for the live book).
9. After live, **always generate** the absolute-markdown paste file for Substack / X Article (detail: [`docs/export-for-substack.md`](docs/export-for-substack.md)):

```bash
node scripts/export-absolute-md.mjs <slug>          # → export/<slug>.md (required after live)
```

## Publish (default)

CI builds and deploys Pages on push to `main`. **Push is not live** until Actions finishes and the post URL returns 200.

Full ship checklist (preflight audits → reverse links → live book placement → push → `gh run watch` → live curl → **required** export generate): [`content/posts/README.md`](content/posts/README.md) § Ship checklist.

```bash
git add content/posts/<slug>.md content/book/<part>.md content/book/index-of-premises.md assets/covers/<slug>.jpg assets/covers/STYLES.md notebooklm-auto/prompts/<slug>_zh.txt notebooklm-auto/prompts/<slug>_video_zh.txt
git commit -m "Publish Post #XXX: <Title>"
git push origin main
gh run watch --exit-status
curl -sI "https://powerpig99.github.io/not-a-toe/posts/<slug>/" | head -1
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

- `index.html` (book front matter: preface, contents, Index link, latest journal entries)
- `book/<part>/index.html` (one page per part) and `book/index-of-premises/index.html`
- `journal/index.html` (all essays in written order) and `about/index.html`
- `posts/<slug>/index.html` (with part breadcrumb and in-part navigation)
- `posts.json` and `posts.jsonl` (machine-readable post index with source markdown URLs and part placement)
- `sitemap.xml` and `robots.txt`

## Live book

The site reads as a live book, *非定论的心智指南 / A Non-Definitive Guide for the Mind*. Each part names a commonly held belief, scientific ones included, and collects the essays that trace it back to the boundary of its premises. The Index of Premises lists figures, theories, and concepts with links to the posts that dissect them. Structure lives only as relative links in [`content/book/`](content/book/). `PART_ORDER` in `build.mjs` is the single ordering constant. The build fails if a post is in no part, sits in two, or a book link breaks. Audit with `python3 scripts/audit-book.py`. The per-post ship step is in [`content/posts/README.md`](content/posts/README.md) § Ship checklist.

Do not commit `public/` as source of truth. Social preview image is referenced from `assets/toe-bang.png` via metadata URL. The same file is also copied into `public/apple-touch-icon.png` for iOS Safari “Add to Home Screen”.
