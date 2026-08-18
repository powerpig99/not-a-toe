# Essay Formatting Guide

**Reference for site scaffold** — not absolute ground over the operator’s draft. The collection is an evolving living tracing, not a catalog of finished products. When refining an operator-supplied essay under `/ontological-clarity`, keep the draft’s cut and title; use this file to place subtitle, lead, sections, and links as necessity of a site essay. Full refinement contract (surgical precision, no rewrite, no collapse into prior posts) and **lattice consistency** (same-axis old residue re-traced in the same ship): [`content/posts/README.md`](../content/posts/README.md) § Refinement workflow and § Lattice consistency. Sleep leftover pass: [`docs/local-memory.md`](local-memory.md).

## Copy-Paste Prompt

Use when **drafting from scratch** or when the operator asks for a full draft in site form. For **refinement of an existing operator draft**, do not use this prompt as a rewrite mandate — apply the refinement workflow in the posts README, then add only the scaffold items below that the draft still lacks.

```markdown
You are writing one essay markdown file for the Not a ToE site.

Output rules (strict):
1. Output only markdown content, no explanations.
2. Write for clarity of the Mind writing — not to inform other Minds. No performance for audience; no meta announcing openness or method as posture. Live the dual as background; do not claim it.
3. First line must be exactly: `# <Title>` — self-explanatory; a reader who never opens the body still knows the claim. Prefer the operator’s title when one was given.
4. After the title, write exactly one complete sentence as the subtitle — essence only (core geometry), not a miniature of the argument or section map. Prefer language already in the draft when refining.
5. After the subtitle, write a lead of 2–4 complete sentences summarizing the post (the main moves). Do not merely rephrase the subtitle; if subtitle and lead share the same ordered points, separate the jobs.
6. Do not use `##` or `###` until after that subtitle + lead.
7. Avoid non-sentence blocks before first `##`/`###` (no lists, no blockquotes, no horizontal rules, no code fences).
8. Main body starts at first `##` heading.
9. Every `##` / `###` names the cut of that section (a specific claim or distinction). Do not use generic slots: What Remains, Conclusion, Summary, Key Takeaways, In Closing, Final Thoughts, The Point, Recap.
10. Use only simple markdown: headings, paragraphs, links `[text](url)`, emphasis `*`/`**`, quotes `>`, lists (`-` and `1.`), horizontal rule (`---`) only in body, and block images `![alt](figures/file.jpg)` after the first heading when a source figure is part of the cut. Hard line breaks (two trailing spaces) are allowed in the body for verse; keep the open pure prose. Source figures live in `assets/figures/` and are copied to `public/figures/`.
11. Keep quotes properly closed; punctuation inside quotes is allowed.
12. No frontmatter (`---` metadata), no HTML.
13. End with a newline.
14. Internal cross-links use relative form only: `[title](../other-slug/)`. Do not use absolute site URLs in the source file. Pointers restore axes; do not collapse the new cut into a remix of prior posts.
15. Fold any seed observation (tweet, note) into the prose so the essay stands alone; do not depend on a deletable external post link.
16. When introducing the irreducible prior by name, use the house premise formula exactly: `Self-distinguishing activity occurs — uncaused, unceasing. Call it the Mind: the observer already underway, every act of which is a distinction.` If refining a draft that already names the prior cleanly, do not force a full formula insert that rewrites the paragraph. Owner detail: [`content/posts/README.md`](../content/posts/README.md).
17. Negation: soft differentiation is fine; assertive negation of other takes is closed. Assertive negation is reserved for dissolving a closed-reality assumption. Prefer stating identity. Owner detail: [`content/posts/README.md`](../content/posts/README.md) refinement / voice section.
```

Full title / subtitle / lead jobs, refinement workflow, and anti-repetition check: [`content/posts/README.md`](../content/posts/README.md) (owner).

## Opening Structure

```text
# Title

<one-sentence subtitle — essence only>

<lead: summary of the post, not a rephrase of the subtitle>

## First body section
...
```

## Why This Works

- The build treats the first sentence before the first `##`/`###` as the **subtitle** (rendered under the title on the essay page; used for index excerpt and meta description).
- The following sentences before the first subsection are the **lead** (kept in the essay body as the opening paragraph).
- Title, subtitle, and lead have three distinct jobs (self-explanatory name / essence / summary). Collapsing them produces repetitive opens.
- Keeping the opening as pure prose makes previews deterministic on index and X cards.

## Cross-links

- In **source** (`content/posts/`): `[axis name](../slug/)`.
- Pointers only — restore an axis; do not restate the linked essay.
- Living updates (same-slug revise, sleep neighbor pass) still use relative pointers only — no absolute site URLs, no frontmatter `related:` list. The posts graph is a projection of these links: `node scripts/project-posts-graph.mjs`.
- For Substack / X Article paste, one absolute-link markdown export — see [`docs/export-for-substack.md`](export-for-substack.md).

## Optional Title Image

Place a **20:9** landscape cover at `assets/covers/<slug>.jpg` (or `.jpeg` / `.png` / `.webp`), matching the markdown filename without extension. Target **1280×576**. That aspect is the shared install for site title image, Substack featured image, and X Article `cover_media` — one file, three consumers. The build:

- copies it to `public/covers/`
- renders it above the essay title
- uses it for `og:image` / Twitter large-image card when present

Generate at `aspect_ratio` **20:9** (not square, portrait, or 16:9). Full style rule, inventory, and workflow: [`assets/covers/STYLES.md`](../assets/covers/STYLES.md). Authoring contract: [`content/posts/README.md`](../content/posts/README.md). Legacy covers (often 16:9) stay as installed until the operator asks to regenerate that slug.
