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
18. Prose over lists (CRITICAL): Unless strictly necessary, do NOT write essays in list or checklist form (`*` or `1.`). Express complex causal mechanics and arguments in continuous, flowing, rigorous narrative prose. If a list is genuinely unavoidable, always insert an empty blank line BEFORE and AFTER the list block.
19. Cross-links as standard workflow: Mandatory relative cross-linking (`[title](../slug/)`) of directly related corpus essays is an integral part of the standard authoring process. Pointers restore axes; they do not summarize or remix prior posts.
20. Mermaid diagram styling and bilingual parallelism:
    - Inline dark-theme styling is mandatory for all Mermaid diagrams to match historical posts:
      - Subgraph: `style S_... fill:#161b22,stroke:#<hex>,stroke-width:1.5px,color:#<hex>`
      - Node: `style NodeID fill:#0d1117,stroke:#<hex>,stroke-width:1px,color:#f0f6fc`
      - Semantic color palette: Green (`#3fb950` - Sovereign judgment, living calibration, authentic causality), Red (`#f85149` - Inversion, outsourcing, alienation, prescriptive protocol, failure/backlash), Amber/Gold (`#d29922` - Mechanical execution, scaffolding, tradeoffs), Blue (`#58a6ff` - Computational models, telemetry, signals, references), Purple (`#a371f7` - Self-referential loop, paradoxical circuit, meta-choice).
    - For bilingual posts (Chinese + English sections), diagrams must maintain exact topological and conceptual parallelism: every Chinese diagram must have its English parallel diagram with identical node hierarchy and semantic coloring.
    - Strict Language Separation ("中文的归中文，英文的归英文"):
      - Chinese belongs to Chinese: In the Chinese version of an essay, all text, headings, and diagram node labels must be pure Chinese. Strictly zero English subtitle lines (e.g. `<br/>English text`) in Chinese diagrams, unless annotating recognized proper nouns (e.g. DNA, API, AI).
      - English belongs to English: In the English version, all text, headings, and diagram node labels must be pure English.
      - Bilingual completeness: Essays with bilingual titles must feature complete parallel Chinese and English sections (including title, subtitle, lead, section headings, narrative prose, and Mermaid diagrams).
21. Epistemological discipline & vocabulary hygiene:
    - Will and agency belong strictly to the living Mind (主权心智). Never subordinate will to physics; never use "物理意志" or attribute will/agency to inanimate tools, capital, markets, or physical substrate. Capital is an inert informational accounting metric.
    - Matter and physics are the macroscopic phenomena arising from the friction between our cognitive modeling and reality, experienced directly as physical friction.
    - Objective facts: there are no mind-independent objective facts; "objective facts" are macroscopic phenomena that maintain invariance across different subjective cognitions.
    - Clean moralizing rhetoric: purge judgmental, patronizing, or moralizing language that presumes a God's-eye view. Maintain a rigorous first-person analytical perspective.
    - Banned words zero-tolerance: zero occurrences of prohibited buzzwords and clichés (`['纯粹', '绝对', '完全', '彻底', '绝不', '通常', '往往', '或许', '某种意义上', '降维重构', '本质', '根本', '自始至终', '缰绳', '物理现实', '平庸', '物理意志']`).
22. Mathematical and symbolic notation: Do NOT use LaTeX syntax (`$` or `$$`). `build.mjs`, Substack, and X do not parse LaTeX, leaving raw dollar signs and backslashes in the output. Always use clean Unicode mathematical symbols (e.g. `—∞ → +∞`, `ΔV + ΔE = 0`, `R_perceive = R_collapse`, `V₁ ⇌ V₂ ⇌ V₃ ⇌ V₁`, `(0 or 1)`), emphasis (`*V*`), or backticked code.
23. Companion NotebookLM Prompts (Standard Deliverable):
    - For every post, generate companion Chinese NotebookLM prompt files under `notebooklm-auto/prompts/`:
      - Audio Dialogue (`notebooklm-auto/prompts/<slug>_zh.txt`): Deep dialogue between 明理 (engineering/systems reality) and 雨涵 (philosophy/cybernetics), containing three mandatory sections:
        1. `### [角色与对话规范]` (roles, strict epistemological constraints, perspective division)
        2. `### [核心议题清单]` (structured topic outline)
        3. `### [正文对谈开场示例]` (Strictly an opening dialogue sample of 2–4 concise turns, NOT a full episode transcript dump. Sized < 8.5 KB, typically 3–6 KB, 25–45 lines. Must begin with the canonical *Not a Theory of Everything* standard opening delivered by 明理: summarizing that any theory/model is scaffolding, first-person perspective and causality are two sides of the same coin, neither closing the universe nor reactive rebellion, and stepping into living friction; followed by 雨涵's natural transition into the essay's core tension and 1–2 grounding turns, leaving NotebookLM to generate the rest of the dynamic discussion naturally from the topic checklist. Rule: refine the opening based on the new analysis, but NEVER delete or omit it; keep strictly to 2–4 dialogue turns).
      - Video Monologue (`notebooklm-auto/prompts/<slug>_video_zh.txt`): Single-speaker philosophical deep monologue dissecting the post's core cuts, containing `### [单人深度文稿规范]`, `### [核心议题脉络]`, and `### [正文文稿]` (full unbroken spoken monologue text).
    - Both prompt files must be strictly link-free (no markdown or HTML links), contain 0 banned words, and contain 0 raw `$` symbols. Audio prompts must strictly adhere to concise limits (< 8.5 KB, 2–4 opening turns).
24. Standard Walkthrough Contract:
    - Every post walkthrough must embed the visual artifact, describe the cover art style and concept, catalogue all dark-theme Mermaid diagrams with semantic coloring, articulate core epistemological cuts, report invariant diagnostic check results, include full text and links for Companion NotebookLM Prompts, and provide multi-platform publishing copies (Spotify Podcast ZH, Spotify Podcast EN, WeChat Video Channels, and X/Twitter EN Only; all four platform copies must explicitly include the original essay live URL: `https://powerpig99.github.io/not-a-toe/posts/<slug>/`).
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

Place a landscape cover at `assets/covers/<slug>.jpg` (or `.jpeg` / `.png` / `.webp`), matching the markdown filename without extension. 
Default generator is local **Qwen-Image-2.1** (`python3 scripts/generate-cover.py <slug> --prompt "..."`), targeting ultra-wide **21:9** at **1344×576** (or 20:9 at **1280×576**). That aspect is the shared install for site title image, Substack featured image, and X Article `cover_media` — one file, three consumers. The build:

- copies it to `public/covers/`
- renders it above the essay title
- uses it for `og:image` / Twitter large-image card when present

Generate at ultra-wide `aspect_ratio` **21:9** (`1344×576`) or **20:9** (`1280×576`) (not square, portrait, or 16:9). Full style rule, inventory, and workflow: [`assets/covers/STYLES.md`](../assets/covers/STYLES.md). Authoring contract: [`content/posts/README.md`](../content/posts/README.md). Legacy covers (often 16:9) stay as installed until the operator asks to regenerate that slug.
