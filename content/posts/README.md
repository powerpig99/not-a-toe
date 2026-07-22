# Posts — authoring contract

Living guide for essays in this folder. Source of truth for site content lives here as `*.md`. Covers and Substack paste have their own trackers; this file is for writing, linking, and shipping the post itself. **Not a site post** — the build skips `README.md` (slug would otherwise be `/posts/README/`).

| Related | Path |
|---------|------|
| Markdown format (LLM copy-paste) | [`docs/essay-format.md`](../../docs/essay-format.md) |
| Cover style differentiation | [`assets/covers/STYLES.md`](../../assets/covers/STYLES.md) |
| Substack / external export | [`docs/export-for-substack.md`](../../docs/export-for-substack.md) |
| X Article publish | [`docs/export-for-x-article.md`](../../docs/export-for-x-article.md) |
| Local memory / sleep audit | [`docs/local-memory.md`](../../docs/local-memory.md) |
| Posts lattice (cross-link graph) | `node scripts/project-posts-graph.mjs` → [`docs/posts.graph.json`](../../docs/posts.graph.json) |
| Site authoring summary | [`README.md`](../../README.md) |

## Principle

Write for clarity of the Mind writing — not to inform other Minds. Every post lives by that: the dual as generative ground, open residue under load, never a finished product or ground truth. Do not announce the stance; do not perform it for an audience. Live it as background voice while drafting. Stating it installs an image to defend.

Posts are **living documents**: same-slug revise when a newer cut clarifies an older face; prefer pointer updates over URL churn. Relations live only as relative cross-links in prose — the posts graph is a disposable projection of those links, never a second inventory.

One file per essay. Filename = **slug** = permalink path `/posts/<slug>/`. Edit only under `content/posts/`; never hand-edit `public/` or treat `export/` as source.

## File layout

```text
content/posts/<slug>.md          # source (this folder)
assets/covers/<slug>.jpg         # optional 16:9 / 1280×720 (site + Substack + X Article)
export/<slug>.md                 # generated paste projection (gitignored)
public/posts/<slug>/index.html   # build output only
```

## Markdown structure

Exact build contract (also in `docs/essay-format.md`):

```text
# Title

*One-sentence subtitle — essence in plain prose.*

Lead: 2–4 complete sentences summarizing the argument.

## First body section
...
```

| Rule | Detail |
|------|--------|
| First line | `# Title` only |
| Subtitle | Exactly one sentence after the title, before any `##` (often italic with `*...*`) |
| Lead | Following sentences before first `##`; pure prose — no lists, quotes blocks, or HRs in the open |
| Body | Starts at first `##` / `###` |
| Section headings | Name the cut of that section — a specific claim or distinction. Not a generic slot |
| Allowed | Headings, paragraphs, `[text](url)`, `*`/`**`, `>`, lists, `---` in body only; hard line breaks (two trailing spaces) for verse in body |
| Forbidden | YAML frontmatter, HTML, non-prose blocks before first section heading |
| End | Trailing newline |

The build uses the first sentence before the first heading as subtitle (index excerpt, meta description) and keeps the rest of the open as the lead paragraph on the essay page.

### Section headings (body `##` / `###`)

Each heading is a miniature claim: what that block distinguishes. A reader skimming only headings should still feel the argument’s spine.

| Prefer | Avoid |
|--------|--------|
| Names the freeze, branch, or return in that section | Slot labels that could sit on any essay |
| Readable alone (stand-alone sense if quoted) | Meta wrappers for “the ending” or “the recap” |

**Do not use** generic closers or placeholders, including: *What Remains*, *What Remains True*, *In Closing*, *Conclusion*, *Summary*, *Key Takeaways*, *Final Thoughts*, *The Point*, *Bringing It Together*, *Recap*.

If the last section returns the reference or dissolves a freeze, **name that return** (e.g. the geometry, the edge, the disqualification) — not that something “remains.”

## Title, subtitle, lead

Three distinct jobs. Do not collapse them.

| Slot | Job | Test |
|------|-----|------|
| **Title** | Self-explanatory name of the cut | A reader who never opens the body still knows what claim the post makes |
| **Subtitle** | Essence only — one sentence | Names the core geometry or distinction; does **not** walk the argument |
| **Lead** | Summary of the post | Maps the main moves (usually 2–4 sentences); does **not** merely rephrase the subtitle |

**Title**
- Prefer a declarative phrase the index and link previews can stand on alone.
- Avoid opaque labels that only make sense after the body (“Two Failures of Trace,” “The Geometry”) unless the phrase is already a stable term in prior posts.
- Self-explanatory ≠ long. Compress the cut; do not outline the essay.

**Subtitle**
- One complete sentence (italic `*...*` is fine).
- Capture *what the post is saying at root* — the irreducible distinction — not a miniature of the sections.
- If it reads like a compressed lead (two failures, then capacity, then close), cut it back to essence.

**Lead**
- Summarize the blog post: what freezes, what dissolves, what remains.
- May name the sequence of cuts the body will open; the subtitle must not.
- Pure prose before first `##` — no lists, blockquotes, or horizontal rules in the open.

**Anti-repetition check**
1. Read title alone — does it state the claim?
2. Read subtitle alone — essence without section map?
3. Read lead alone — full summary without depending on the subtitle for the map?
4. If subtitle and lead share the same sentence structure or the same ordered list of points, rewrite until jobs separate.

## Voice and refinement (from practice)

When refining under ontological clarity (or any dissolution pass):

- **Clarity of the writing Mind, not performance for readers.** Draft so the next step at this locus is cleaner. Do not write to teach, persuade, reassure, or brand. Cross-links restore axes for the same Mind under another load — not an index for an audience. “Embody. Never claim.” applies to the page itself: no meta about openness, no posture of humility, no lecture about how the work should be read.
- **Mechanism, not moral framing.** Prefer allocation, locus, continuation, capacity thinning over stolen power, genuine stake, heroic independence.
- **Assert; don’t soften.** Drop padding (“rarely,” “in most cases,” “not primarily”) when the cut is structural.
- **Dissolve, don’t negate.** Describe what the activity is doing; avoid installing a corrective identity (“reject all external input”).
- **Stand alone.** Fold ephemeral posts (X, drafts) into the prose. Do **not** depend on a link to something you may delete. Link durable site posts and stable external sources when needed.
- **Cross-links as pointers.** Restore an axis with a short clause + link; do not restate the linked essay. Pattern:

  ```markdown
  … the same cut as [intelligence belongs only to The Mind](../intelligence-belongs-only-to-the-mind/).
  ```

- **Internal links stay relative** in source:

  ```markdown
  [link text](../other-slug/)
  ```

  Never put `https://powerpig99.github.io/not-a-toe/posts/...` in `content/posts/` — that is what the export script projects for Substack.

## Cross-link checklist

1. Prefer posts that name the same geometry under a different face (allocation, medium-as-locus, delegation, ownership).
2. One pointer per cut is enough; avoid a laundry list in one paragraph.
3. Verify the target file exists: `content/posts/<slug>.md`.
4. After adding links, re-read: if a paragraph only exists to summarize another essay, delete the summary and keep the pointer.
5. After shipping a new or revised post, sleep (or an explicit pass) reviews **1-hop neighbors** for pointer updates — see [`docs/local-memory.md`](../../docs/local-memory.md) posts lattice. Do not force reverse links; one-way is default.

### Posts graph (projection only)

```bash
node scripts/project-posts-graph.mjs                 # docs/posts.graph.json
node scripts/project-posts-graph.mjs --neighbors <slug>
node scripts/project-posts-graph.mjs --diff           # seeds vs prior graph + review sets
```

Edges = relative `](../slug/)` links already in these files. Never hand-edit the JSON; never maintain a separate `related:` list.

## Cover

Optional but usual for new essays. **One file serves three surfaces:** this site, Substack featured image, and X Article cover media.

| Surface | Role of the same file |
|---------|------------------------|
| Site | Title image + `og:image` / large Twitter card |
| Substack | Upload as post cover / social image (prefer local re-upload) |
| X Article | Uploaded as `cover_media` via [`docs/export-for-x-article.md`](../../docs/export-for-x-article.md) |

1. Read [`assets/covers/STYLES.md`](../../assets/covers/STYLES.md) — pick a **style family not already used**.
2. Generate landscape art at **16:9** (X Article / in-stream safe; also Substack-friendly), no text. Install as `assets/covers/<slug>.jpg` at **1280×720** (or 1600×900 resized down to 1280×720 for the site install).
3. Update STYLES.md inventory and family tables.
4. Build copies cover to `public/covers/` and uses it for `og:image` / X card when present.

Do not generate square, portrait, or ultra-wide banners as the essay cover — those crop badly when the same asset is reused as X Article cover and Substack image.

## Ship (site)

Default path: commit and push; GitHub Actions builds.

```bash
# typical new essay
git add content/posts/<slug>.md assets/covers/<slug>.jpg assets/covers/STYLES.md
git commit -m "Add <title> essay"
git push origin main
```

Local check (optional):

```bash
node build.mjs
# open public/posts/<slug>/index.html
```

Do not commit `public/` or `export/` as source of truth (`export/` is gitignored).

## New essay checklist

1. [ ] Draft `content/posts/<slug>.md` to format contract (title / subtitle / lead / `##` body).
2. [ ] Section headings name each cut — no generic slots (*What Remains*, *Conclusion*, *Summary*, …).
3. [ ] Refine for mechanism language; fold any seed tweet into the lead so the essay stands alone.
4. [ ] Add relative cross-links as axis pointers; verify slugs exist (`node scripts/project-posts-graph.mjs` → `missing_targets` must stay 0).
5. [ ] Cover: new style per STYLES.md; **16:9** landscape; install 1280×720; update STYLES.md.
6. [ ] Commit + push (or local `node build.mjs` first).
7. [ ] If posting to Substack: follow [`docs/export-for-substack.md`](../../docs/export-for-substack.md).
8. [ ] If posting as X Article: follow [`docs/export-for-x-article.md`](../../docs/export-for-x-article.md) (dry-run → `--draft` → review → publish).
9. [ ] Neighbor review: deferred to project `/sleep` unless this draft **depends** on correcting an older claim now — then edit that neighbor in the same session (pointer only).

## After shipping

- Prefer not to rewrite published URLs/slugs; add a new post or revise in place under the same slug.
- Living updates: same-slug edits when a newer cut clarifies an older face; regenerate posts graph after link changes.
- If cross-links are added later, re-run Substack export only if you will update the Substack version by hand.
- Sleep (operator call) runs the related-post currency pass on seeds from `--diff` — see [`docs/local-memory.md`](../../docs/local-memory.md).
