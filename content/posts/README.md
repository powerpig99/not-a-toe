# Posts — authoring contract

Living guide for essays in this folder. Source of truth for site content lives here as `*.md`. Covers and Substack paste have their own trackers; this file is for writing, linking, and shipping the post itself.

| Related | Path |
|---------|------|
| Markdown format (LLM copy-paste) | [`docs/essay-format.md`](../../docs/essay-format.md) |
| Cover style differentiation | [`assets/covers/STYLES.md`](../../assets/covers/STYLES.md) |
| Substack / external export | [`docs/export-for-substack.md`](../../docs/export-for-substack.md) |
| Local memory / sleep audit | [`docs/local-memory.md`](../../docs/local-memory.md) |
| Site authoring summary | [`README.md`](../../README.md) |

## Principle

One file per essay. Filename = **slug** = permalink path `/posts/<slug>/`. Edit only under `content/posts/`; never hand-edit `public/` or treat `export/` as source.

## File layout

```text
content/posts/<slug>.md          # source (this folder)
assets/covers/<slug>.jpg         # optional 1280×720 cover
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
| Allowed | Headings, paragraphs, `[text](url)`, `*`/`**`, `>`, lists, `---` in body only |
| Forbidden | YAML frontmatter, HTML, non-prose blocks before first section heading |
| End | Trailing newline |

The build uses the first sentence before the first heading as subtitle (index excerpt, meta description) and keeps the rest of the open as the lead paragraph on the essay page.

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

## Cover

Optional but usual for new essays.

1. Read [`assets/covers/STYLES.md`](../../assets/covers/STYLES.md) — pick a **style family not already used**.
2. Generate landscape art (16:9), no text; install as `assets/covers/<slug>.jpg` at **1280×720**.
3. Update STYLES.md inventory and family tables.
4. Build copies cover to `public/covers/` and uses it for `og:image` / X card when present.

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
2. [ ] Refine for mechanism language; fold any seed tweet into the lead so the essay stands alone.
3. [ ] Add relative cross-links as axis pointers; verify slugs exist.
4. [ ] Cover: new style per STYLES.md; install 1280×720; update STYLES.md.
5. [ ] Commit + push (or local `node build.mjs` first).
6. [ ] If posting to Substack: follow [`docs/export-for-substack.md`](../../docs/export-for-substack.md).

## After shipping

- Prefer not to rewrite published URLs/slugs; add a new post or revise in place under the same slug.
- If cross-links are added later, re-run Substack export only if you will update the Substack version by hand.
