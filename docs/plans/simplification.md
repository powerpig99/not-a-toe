# Plan: Replace Hugo + PaperMod with Zero-Dep Python Static Site Generator

## Context

Split authority is the root cause: content metadata and rendering behavior are spread across markdown files, CI mutation logic, and Hugo/PaperMod theme defaults. CI rewrites source files at deploy time (injecting frontmatter, deleting headings, falling back to filename-derived titles). Hugo + PaperMod is 122 theme files (~5,724 lines) for what is fundamentally markdown essays -> list + detail pages.

**Goal**: Single authoritative path — `content/posts/*.md` -> `python3 build.py` -> static HTML. No content mutation, no framework overhead, no split sources of truth.

## Decisions

- **Build tool**: Python, stdlib only (`tomllib` requires Python 3.11+)
- **Features**: Keep all current — dark/light auto, reading time, post nav, OG + Twitter `summary` cards
- **Content rule**: Every `.md` starts with `# Title`. Zero exceptions.
- **Pinned post**: `pinned_slug` field in `site.toml`
- **Markdown parser**: Hand-written, current text features now (headings, paragraphs, hr, lists, blockquotes, bold/italic, inline code, links), extensible for code fences/images/tables later
- **Config**: `site.toml` (parsed via stdlib `tomllib`)

## Files Overview

| Action | File | Purpose |
|--------|------|---------|
| Create | `build.py` | Entire static site generator (~300 lines) |
| Create | `style.css` | All CSS (PaperMod colors/layout extracted, ~250 lines) |
| Create | `site.toml` | Site config (replaces `hugo.yaml`) |
| Create | `.github/workflows/deploy.yml` | New CI (replaces Hugo workflow) |
| Modify | 4 posts | Normalize to `# Title` pattern |
| Modify | `.gitignore` | Remove Hugo-specific entries |
| Delete | `hugo.yaml`, `.gitmodules`, `themes/`, `layouts/`, `assets/` | Hugo/PaperMod removal |
| Delete | `.github/workflows/hugo.yml` | Old CI |
| Keep | `publish.py`, `post_tweet.py`, `static/images/*` | Still work as-is |

## Phase 1: Content Normalization

Normalize 4 files so every post starts with `# Title`:

1. **`not-a-theory-of-everything.md`** — Strip 4 frontmatter lines (`---`, `title:`, `weight:`, `---`), prepend `# Not a Theory of Everything\n`
2. **`help-is-half-the-problem.md`** — Replace line 1 `**help is half the problem**` with `# Help Is Half the Problem`
3. **`perception-perspective-refined.md`** — Replace line 1 `### Perception and Perspective...` with `# Perception and Perspective: The Collapse That Isn't There`
4. **`the-risk-you-delegate-is-the-risk-you-create.md`** — Replace line 1 `### The Risk You Delegate...` with `# The Risk You Delegate Is the Risk You Create`

**Commit separately** so current Hugo CI still works with normalized content.

**Verify**: `head -1 content/posts/*.md` — all 48 files start with `# `

## Phase 2: Site Config

Create `site.toml`:
```toml
title = "Not a ToE"
description = "Not a ToE - rewritten from the ground up."
base_url = "https://powerpig99.github.io/not-a-toe"
language = "en-US"
posts_per_page = 10
pinned_slug = "not-a-theory-of-everything"

[images]
og = "images/card.jpg"
twitter = "images/card-twitter.jpg"
```

## Phase 3: Markdown Parser (in `build.py`)

Line-by-line state machine. States: `IDLE`, `PARAGRAPH`, `UL`, `OL`, `BLOCKQUOTE`.

**Block-level** (first match wins per line):
- Blank line → flush current block
- Heading `^#{1,6} ` → emit `<hN>` with inline formatting
- Horizontal rule `^---$` / `^***$` / `^___$` → emit `<hr>`
- Blockquote `^> ` → accumulate in blockquote buffer, emit `<blockquote>` on flush
- Unordered list `^- ` → open/continue `<ul>`, emit `<li>`
- Ordered list `^[0-9]+\. ` → open/continue `<ol>`, emit `<li>`
- Anything else → accumulate in paragraph buffer

**Inline formatting** (sequential regex on text segments):
1. `html.escape()` first
2. Inline code `` `...` `` → `<code>...</code>` (protect from further formatting)
3. Bold `**...**` → `<strong>...</strong>`
4. Italic `*...*` → `<em>...</em>`
5. Links `[text](url)` → `<a href="url">text</a>`

**Extension points for later**: Code fences (``` ``` ```), images (`![]()`), tables — each adds one block-level pattern and one flush handler.

**Title extraction**: First line must be `# Title`. Parser caller strips it; it becomes page title, not body content.

**Reading time**: `max(1, ceil(word_count / 265))` (PaperMod's rate).

**Description/excerpt**: First ~300 chars of plain text, trimmed to last sentence boundary (`.` + space/end).

## Phase 4: HTML Templates (in `build.py`)

Three template functions using f-strings. No separate template files.

**Base shell**: `<!DOCTYPE html>`, meta viewport, canonical URL, `<link>` to `style.css`, inline theme-detection JS in `<head>`, `<header>` with nav/logo, `<main>`, `<footer>`, scroll-to-top link.

**Post page**: `<article>` with title `<h1>`, date + reading time meta, HTML body, prev/next navigation.

**List page**: Loop of `<article class="post-entry">` with title, excerpt, reading time + date. Pagination nav at bottom.

**Meta tags**: OG (`og:title`, `og:description`, `og:image`, `og:url`, `og:type`, `og:site_name`, `og:locale`) + Twitter (`summary` card, `card-twitter.jpg` image).

**Inline JS** (minimal):
- Theme detection: read `prefers-color-scheme`, set `data-theme` on `<html>` before paint
- Scroll-to-top: show/hide link on scroll

## Phase 5: CSS (`style.css`)

Single file, copied to output root. Extracted from PaperMod with unused features removed.

**CSS variables** (from `themes/PaperMod/assets/css/core/theme-vars.css`):
```
Light: --theme: rgb(255,255,255), --primary: rgb(30,30,30), --secondary: rgb(108,108,108), --tertiary: rgb(214,214,214), --content: rgb(31,31,31), --entry: rgb(255,255,255), --code-bg: rgb(245,245,245), --border: rgb(238,238,238)
Dark:  --theme: rgb(29,30,32), --primary: rgb(218,218,219), --secondary: rgb(155,156,157), --tertiary: rgb(65,66,68), --content: rgb(196,196,197), --entry: rgb(46,46,51), --code-bg: rgb(55,56,62), --border: rgb(51,51,51)
Layout: --gap: 24px, --content-gap: 20px, --nav-width: 1024px, --main-width: 720px, --header-height: 60px, --footer-height: 60px, --radius: 8px
```

**Sections**: variables + dark mode toggle, reset, layout (main/nav/footer), post-single (header/meta/content/paginav), post-entry (list cards), pagination, heading size overrides (from current `custom.css`: post-title 24px, entry h2 20px, content h1 24px, h2 20px, h3 17px), nav width alignment, responsive breakpoints, scrollbar, scroll-to-top.

**Dropped**: code highlighting, search, profile mode, archive, tags, share buttons, TOC, cover images, breadcrumbs, i18n.

## Phase 6: LLM Outputs

`llms.txt` — index with links and one-line descriptions:
```
# Not a ToE
> Not a ToE - rewritten from the ground up.
## Essays
- [Title](/posts/slug/): First sentence description.
```

`llms-full.txt` — full content, all essays concatenated with `---` separators.

## Phase 7: CI Workflow

Create `.github/workflows/deploy.yml`:
- Trigger: push to `main`
- Checkout with `fetch-depth: 0` (for git dates)
- `setup-python@v5` with `python-version: '3.12'`
- `python3 build.py`
- Upload `./public` artifact
- Deploy to GitHub Pages

No Hugo setup, no submodule checkout, no content mutation step.

## Phase 8: Cleanup

1. Remove git submodule: `git submodule deinit -f themes/PaperMod && git rm -f themes/PaperMod`
2. Delete: `hugo.yaml`, `.gitmodules`, `themes/`, `layouts/`, `assets/`, `.github/workflows/hugo.yml`
3. Update `.gitignore`: remove `resources/`, `.hugo_build.lock`; add `__pycache__/`
4. Update `README.md` to reflect new build: `python3 build.py` or just push

## Build Orchestration (`build.py` main flow)

```
load site.toml
clean public/
copy static/images/ -> public/images/
copy style.css -> public/style.css
parse all content/posts/*.md (title from # heading, date from git log, body -> HTML)
sort posts (date desc, pinned first)
generate public/posts/<slug>/index.html for each post (with prev/next)
generate public/index.html + public/page/N/index.html (paginated list)
generate public/llms.txt, public/llms-full.txt
generate public/robots.txt
```

## Commit Strategy

1. **Commit A**: Normalize 4 posts (Phase 1). Push. Current Hugo CI validates.
2. **Commit B**: Add `build.py`, `style.css`, `site.toml`, new CI. Remove Hugo/PaperMod/layouts/assets/old CI. Atomic swap.

## Verification

After Phase 1:
- `head -1 content/posts/*.md` — all start with `# `
- Push; Hugo CI builds successfully

After Phase 2-8 (local):
- `python3 build.py` runs clean
- 48 `public/posts/<slug>/index.html` exist
- `public/index.html` + `public/page/2..5/index.html` exist (48 posts / 10 per page)
- `public/images/card.jpg`, `public/images/card-twitter.jpg` copied
- `public/style.css`, `public/llms.txt`, `public/llms-full.txt`, `public/robots.txt` exist
- Pinned post first on home page
- Prev/next links correct on post pages
- OG + Twitter meta tags present
- Dark/light mode works (`python3 -m http.server -d public 8000`)
- Spot-check 3 posts for reading time accuracy
- All URLs preserve `/posts/<slug>/` pattern

After push:
- GitHub Actions deploys successfully
- Live site renders correctly
- Spot-check 5 posts visually

## Recursive Recap (after each phase)

1. What is the single trigger now?
2. Is there exactly one source for title/date/slug?
3. Did we remove fallback branches?
4. What became dead and can now be deleted?
5. If we started fresh today, what is the next smallest simplifying step?
