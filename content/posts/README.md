# Posts — authoring contract

Living guide for essays in this folder. Source of truth for site content lives here as `*.md`. Covers and Substack paste have their own trackers; this file is for writing, linking, and shipping the post itself. **Not a site post** — the build skips `README.md` (slug would otherwise be `/posts/README/`).

| Related | Path |
|---------|------|
| Markdown format (LLM copy-paste) | [`docs/essay-format.md`](../../docs/essay-format.md) |
| Cover style differentiation | [`assets/covers/STYLES.md`](../../assets/covers/STYLES.md) |
| Paste export (Substack + X Article) | [`docs/export-for-substack.md`](../../docs/export-for-substack.md) (one absolute-markdown file) |
| X Article API (parked) | [`docs/export-for-x-article.md`](../../docs/export-for-x-article.md) |
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
assets/covers/<slug>.jpg         # optional 20:9 / 1280×576 (site + Substack + X Article)
export/<slug>.md                 # shared paste export: absolute-link markdown (gitignored)
public/posts/<slug>/index.html   # site build output only (CI / local build.mjs)
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

## Refinement workflow (operator draft → site essay)

The operator’s draft is already as close as it can be. Ontological clarity is a **scale** for residual imprecision — not a license to rewrite the essay into prior house prose or to collapse a new cut into posts already shipped.

### Ground and instruments

| Surface | Role |
|---------|------|
| **Operator draft** (incl. title) | Ground of the cut. Keep it. Surgical nicks only. |
| **`/ontological-clarity`** | Method scale: locate residual freezes; dissolve only those; wait for feedback after a clean pass. |
| **Format docs** (`docs/essay-format.md`, this file’s structure table) | **Reference**, not absolute ground. Scaffold subtitle, sections, links as necessity of a site essay — not as a checklist that may overwrite the draft’s spine. |
| **Prior posts** | Adjacent axes. Pointers restore an axis; they must not absorb the new trace into “what we already had.” Same-axis old claims that the new cut makes false, over-closed, or incomplete must be nicked in the old prose (see Lattice consistency). |

### Surgical precision (not rewrite)

1. **Double-check for residual imprecision** under Method. Nick words/phrases that mis-bound or overload (e.g. one term doing two jobs). Do **not** rebuild section by section in house voice.
2. **Do not dissolve everything.** Identify boundaries: hold what the draft correctly holds; dissolve only excess freeze (e.g. exterior survey, dual arrows that cancel). Do **not** over-hold (warehouse of secrets) or over-relax (erasing real residual pressure).
3. **Do not collapse the new tracing** into remix of existing essays. If the cut is new (cascade, coin, residual-as-not-yet-folded, …), the body must carry *that* cut — not a summary of neighbors under new headings.
4. **Keep the original title** when the operator supplied one; it is often the most relatable name of the cut.
5. **Then wait for feedback.** Do not open a secondary branch (“over-template or not?”). Method first until residue is gone; operator decides next.

### Site scaffold (necessity, not requirement-as-ground)

After the draft’s precision holds, add only what the site essay needs:

| Add | Job |
|-----|-----|
| Subtitle (one sentence) | Essence of *this* cut — prefer language already in the draft |
| Lead (2–4 sentences) | Summary of the post’s moves; pure prose before first `##` |
| Section headings | Name *this* essay’s cuts, not generic slots or neighbor titles |
| Cross-links | Where an adjacent axis truly fits — pointer clause only; sparse |
| Reverse links | On every 1-hop outbound neighbor (see checklist below) |
| Lattice consistency | Same-axis old claims nicked or restored — not deferred to `/sleep` |
| Cover + STYLES | Usual ship path |

Do **not** invent long expansions, dual-error costume blocks, or neighbor laundry lists to “make it look like” other posts.

### Voice (from practice)

When the scale finds a residual and a nick is needed:

- **Premise formula (house).** When the irreducible prior is introduced by name *and* the draft already opens that naming, use this exact pair (or the first two clauses of a longer sentence that continues the derivation). If the draft names the prior cleanly without the formula, do not force a full insert that rewrites the paragraph.

  ```text
  Self-distinguishing activity occurs — uncaused, unceasing. Call it the Mind: the observer already underway, every act of which is a distinction.
  ```

  Do not invent parallel intros (“That is Mind,” “Call it the edge; the name adds nothing”) as substitutes. Essay-specific derivation continues after the formula; it does not replace it.

- **Clarity of the writing Mind, not performance for readers.** Draft so the next step at this Mind is cleaner. Do not write to teach, persuade, reassure, or brand. Cross-links restore axes for the same Mind under another load — not an index for an audience. “Embody. Never claim.” applies to the page itself. In public prose use **the Mind** or **the individual** as the sentence requires; house *locus* / *loci* stays internal to the skill derivation.
- **Mechanism, not moral framing.** Prefer allocation, locus, continuation, capacity thinning over stolen power, genuine stake, heroic independence.
- **Assert; don’t soften.** Drop padding (“rarely,” “in most cases,” “not primarily”) when the cut is structural.
- **Negation discipline.** Soft negation as differentiation is ordinary. Assertive negation of rival takes installs a closed boundary — avoid it. Exception: assertive negation of a **closed-reality assumption** opens rather than seals. Describe what the activity is doing.
- **Stand alone.** Fold ephemeral posts (X, drafts) into the prose. Do **not** depend on a link to something you may delete.
- **Cross-links as pointers.** Restore an axis with a short clause + link; do not restate the linked essay. Pattern:

  ```markdown
  … the same cut as [intelligence belongs only to The Mind](../intelligence-belongs-only-to-the-mind/).
  ```

- **Internal links stay relative** in source:

  ```markdown
  [link text](../other-slug/)
  ```

  Never put `https://powerpig99.github.io/not-a-toe/posts/...` in `content/posts/` — that is what the shared paste export projects for Substack / X Article.

## Cross-link checklist

1. Prefer posts that name the same geometry under a different face (allocation, medium-as-locus, delegation, ownership).
2. One pointer per cut is enough; avoid a laundry list in one paragraph.
3. Verify the target file exists: `content/posts/<slug>.md`.
4. After adding links, re-read: if a paragraph only exists to summarize another essay, delete the summary and keep the pointer.
5. After shipping a new or revised post, **always** update **reverse links** on 1-hop neighbors (two-way is default). For each outbound `](../other-slug/)`, open that neighbor and add a single pointer clause back to this slug where the same geometry appears — see [`docs/local-memory.md`](../../docs/local-memory.md) posts lattice. Pointer only; do not restate this essay.

## Lattice consistency (same ship)

A new essay is a further distinction in one field. Older posts that already speak on that axis must remain consistent with it. Reverse pointers are not this step. Apply `/ontological-clarity`: restore the bound; do not rewrite old essays into the new one; do not collapse two axes onto one name.

1. **Name the new cut** in one sentence — the distinction, not the topic.
2. **Find same-axis old prose.** Start with 1-hop neighbors, then search the named problem and the freeze the new cut dissolves (not the whole corpus). Same named problem, same freeze, or the same claim that intelligence, design, or thoughtfulness closes it. A shared word is not a shared axis.
3. **Classify each hit, then act:**

   | Class | What it is | Act |
   |-------|------------|-----|
   | **Inconsistent** | Old claim is now false or over-closed | Nick the old claim |
   | **Incomplete on the same axis** | Old essay treated a shallower face as the whole of that named problem | Restore the missing bound in the old sentence (a pointer alone is not enough if the old sentence still overclaims) |
   | **Adjacent, different axis** | Related face, not the same cut | Pointer only if it restores; do not collapse |
   | **No shared axis** | Topic overlap only | Leave |

4. A pointer is enough only when the old claim still holds and only the new face needs naming.
5. Do this in the **same ship**. `/sleep` currency pass is a leftover catch, not the first pass.

Do not warehouse hits. Do not over-relax: if an old heading or installing sentence still names the shallower face as the whole problem, that sentence is the update.

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
| X Article | Upload same file as Article cover in the editor (paste path; API parked) |

1. Read [`assets/covers/STYLES.md`](../../assets/covers/STYLES.md). **Do not default to still life / craft-table stills** (recent lag). Prefer a **new** style family; if unused styles run thin, **randomly reuse** a used family — never converge on one fixed look.
2. Generate landscape art at **20:9** when available (Substack / X Article); **16:9 as-is** is fine (no forced crop). No text. Install as `assets/covers/<slug>.jpg`.
3. Update STYLES.md inventory and family tables.
4. Build copies cover to `public/covers/` and uses it for `og:image` / X card when present.

**Leave older covers as they are** unless the operator explicitly asks to regenerate that slug. Operator drop supersedes agent-gen.

## Ship checklist (full finish)

**One source:** `content/posts/<slug>.md` (+ cover under `assets/covers/`).  
**Build lives on CI:** push → GitHub Actions runs `node build.mjs` → deploys Pages.  
**Do not** commit `public/` or treat `export/` as canon (`export/` is gitignored).  
**Push ≠ live.** Source on `main` can be correct while Pages still serves the previous SHA. Do not claim published until the live URL returns 200.

**“Finish the rest” means the full ship below** — not site-only. Generate the absolute-markdown paste file after live is **required** on every new or same-slug revised essay. **Paste** into Substack / X Article is operator-only and may wait; **generating** `export/<slug>.md` does not wait for that decision and is not optional for the agent.

| Step | Required? | Who |
|------|-----------|-----|
| Preflight build + graph | Yes | Agent |
| Cover + STYLES | Yes (usual) | Agent |
| Reverse links on 1-hop neighbors (same ship) | Yes | Agent |
| Lattice consistency on same-axis old essays (same ship) | Yes | Agent |
| Commit / push / `gh run watch` / live 200 | Yes | Agent |
| `node scripts/export-absolute-md.mjs <slug>` after live | **Yes** | Agent |
| Paste into Substack / X Article + upload cover there | Operator | Operator only |

Do **not** skip export generation because paste might not happen immediately. Do **not** treat “if posting” as license to omit the file. The file is the finish artifact; paste is a later operator act.

### 1. Preflight (local)

```bash
node build.mjs
# optional: open public/posts/<slug>/index.html
# optional: node scripts/project-posts-graph.mjs  # missing_targets must stay 0
```

Local build is a check, not the publisher. Fix format/link/cover issues here before commit.

### 2. Commit and push

```bash
git add content/posts/<slug>.md assets/covers/<slug>.jpg assets/covers/STYLES.md
# plus any neighbor pointer edits in the same ship
git commit -m "Add <title> essay"
git push origin main
```

### 3. Wait for Actions (required)

```bash
gh run list --limit 3
gh run watch --exit-status          # blocks until the latest run for this branch finishes
# if no run appears within ~2 min after push:
gh workflow run deploy.yml --ref main
gh run watch --exit-status
```

Workflow: [`.github/workflows/deploy.yml`](../../.github/workflows/deploy.yml) — `push` to `main` and `workflow_dispatch`. Manual dispatch is the escape hatch when push webhooks lag or fail to start.

### 4. Verify live (required before “published”)

```bash
curl -sI "https://powerpig99.github.io/not-a-toe/posts/<slug>/" | head -1
# expect: HTTP/2 200
# cover when present
curl -sI "https://powerpig99.github.io/not-a-toe/covers/<slug>.jpg" | head -1
```

404 with a green local build almost always means **deploy has not finished** (or never started) — not a broken essay. Re-check step 3; do not re-architect the post.

### 5. Absolute-markdown export (required after live)

```bash
node scripts/export-absolute-md.mjs <slug>
# → export/<slug>.md  (gitignored; same file for Substack and X Article body paste)
```

Run **once per ship** after the live URL returns 200 so absolute links resolve. Owner detail: [`docs/export-for-substack.md`](../../docs/export-for-substack.md).

| Do | Do not |
|----|--------|
| Generate `export/<slug>.md` before claiming the ship finished | Skip generation because paste is “maybe later” |
| Re-run after same-slug source edits that will be re-pasted | Commit `export/` or edit source to absolute links for editors |
| Leave paste to the operator | Claim Substack/X is published without operator paste |

**Operator paste** (not agent): open `export/<slug>.md` in a markdown previewer → copy from the **rendered** preview into Substack and/or X Article → upload cover from `assets/covers/<slug>.jpg` if used.

### 6. Neighbor pointers and lattice consistency (same ship)

For every outbound `](../other-slug/)`, add a reverse pointer on that neighbor in the **same** ship (two-way default). Pointer clause only.

Then run **Lattice consistency**: name the new cut; search same-axis old prose; nick inconsistent or over-closed claims; restore incomplete same-axis bounds in the old sentence. A pointer is not a substitute for that nick. `/sleep` currency pass is a leftover catch — see [`docs/local-memory.md`](../../docs/local-memory.md).

Regenerate the posts graph after either kind of edit.

### Copy-paste ship block

```bash
SLUG=<slug>
node build.mjs
git add content/posts/"$SLUG".md assets/covers/"$SLUG".jpg assets/covers/STYLES.md
# plus neighbor reverse-link files and same-axis consistency nicks when edited
git commit -m "Add <title> essay"
git push origin main
gh run watch --exit-status || { gh workflow run deploy.yml --ref main && gh run watch --exit-status; }
curl -sI "https://powerpig99.github.io/not-a-toe/posts/${SLUG}/" | head -1
curl -sI "https://powerpig99.github.io/not-a-toe/covers/${SLUG}.jpg" | head -1
node scripts/export-absolute-md.mjs "$SLUG"
# operator: paste export/$SLUG.md (rendered) + cover into Substack / X Article when ready
```

## New essay checklist

1. [ ] Draft `content/posts/<slug>.md` to format contract (title / subtitle / lead / `##` body).
2. [ ] Section headings name each cut — no generic slots (*What Remains*, *Conclusion*, *Summary*, …).
3. [ ] Refine for mechanism language; fold any seed tweet into the lead so the essay stands alone.
4. [ ] Add relative cross-links as axis pointers; verify slugs exist (`node scripts/project-posts-graph.mjs` → `missing_targets` must stay 0).
5. [ ] Cover: new style per STYLES.md; **20:9** landscape preferred (**16:9 as-is** OK); install; update STYLES.md.
6. [ ] Neighbor reverse pointers **in the same ship** (two-way default). **Lattice consistency:** identify same-axis old claims that are now false, over-closed, or incomplete; nick or restore them in the old prose; regenerate posts graph.
7. [ ] **Ship:** preflight → commit/push → `gh run watch` → live post (and cover) URL 200.
8. [ ] **Export (required after live):** `node scripts/export-absolute-md.mjs <slug>` → `export/<slug>.md` ([`docs/export-for-substack.md`](../../docs/export-for-substack.md)). Paste into Substack / X is operator-only and may wait; generating the file does not.

## After shipping

- Prefer not to rewrite published URLs/slugs; add a new post or revise in place under the same slug.
- Living updates: same-slug edits when a newer cut clarifies an older face; regenerate posts graph after link changes.
- After same-slug body or link edits that will be re-pasted externally: re-run `node scripts/export-absolute-md.mjs <slug>` so `export/` matches source.
- Sleep (operator call) runs a leftover currency pass on seeds from `--diff` — see [`docs/local-memory.md`](../../docs/local-memory.md). Same-axis consistency of a new drop is ship-time, not sleep-time.
