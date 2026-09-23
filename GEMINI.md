# Not a ToE — Standard Operating Procedures & Invariants

## Core Working Philosophy
> **"非必要不变更，防止无意识漂移。"**
> Standard conventions remain consistent by default across sessions.
> They are non-dogmatic: intentional, context-driven variations are permitted when specifically requested,
> but accidental omission, convenience-driven shortcutting, and unconscious drift are caught before release.

---

## Strict Invariant: Canonical Live Site URL (Zero Hallucinated Domains)
> **The canonical live site URL for all posts is strictly:**
> `https://powerpig99.github.io/not-a-toe/posts/<slug>/`
> 
> - **CRITICAL PROHIBITION**: NEVER use `not-a-toe.org`, `not-a-toe.com`, or any other placeholder domain under ANY circumstances. The blog has no custom domain; it is deployed exclusively on GitHub Pages at `powerpig99.github.io/not-a-toe`.
> - **All multi-platform publishing copies** (Spotify ZH, Spotify EN, WeChat Video, X/Twitter) in walkthroughs and chat responses MUST use the exact URL: `https://powerpig99.github.io/not-a-toe/posts/<slug>/` (with trailing slash).
> - **Essay internal links** must NEVER use absolute URLs (always use relative `[title](../slug/)`).

---

## Standard Post Authoring & Publishing Deliverables

For every new or revised essay, the complete deliverable set consists of:

### 1. Markdown Essay (`content/posts/<slug>.md`)
- **First line (`# <Title>`)**: Concise, punchy bilingual title (`# <Chinese Title> / <English Title>`).
  - **Strictly zero compound subtitle delimiters**: Prohibit `：`, `:`, ` - `, ` — `, or `——` in the `# ` heading. Explanatory clauses, secondary framings, or subtitles must strictly belong to Line 3, not the title.
  - Keeps cards, index previews, and social cards clean and readable (strictly punchy 1-line titles, avoiding multi-line heading bloat).
- **Line 3 (`*<Subtitle>*`)**: Explicit single-line italic subtitle (`*<Chinese Subtitle> / <English Subtitle>*`).
  - **Strictly one concise sentence**: Essence and core distinction only; never a multi-sentence wall-of-text synopsis paragraph or chapter outline.
  - Sized compactly (typically under 140 characters total); exactly one line in the markdown source file.
- **Lead Prose (Line 5+)**: Opening narrative prose (2–4 complete sentences summarizing the argument before the first `##`).
  - Detailed synopsis, argument progression, and background context belong in the lead body paragraphs, never inside the italic `*...*` subtitle block.
- **Prose over lists**: **Strictly zero bulleted (`*`, `-`) or numbered (`1.`) lists in essay prose**. Complex causal arguments must unfold in flowing, continuous, rigorous narrative prose.
- **Mermaid styling**: All diagrams must adhere to the historical inline dark-theme palette:
  - Subgraphs: `style S_... fill:#161b22,stroke:#<hex>,stroke-width:1.5px,color:#<hex>`
  - Nodes: `style NodeID fill:#0d1117,stroke:#<hex>,stroke-width:1px,color:#f0f6fc`
  - Semantic colors: Green (`#3fb950` - Mind/sovereign judgment), Red (`#f85149` - Inversion/collapse/failure), Amber (`#d29922` - Scaffolding/tradeoffs), Blue (`#58a6ff` - Models/telemetry/signals), Purple (`#a371f7` - Self-referential loops/latent spaces).
- **Bilingual parallelism**: Every Chinese diagram must have an exact parallel English counterpart with identical node topology and semantic coloring.
- **Strict Language Separation ("中文的归中文，英文的归英文")**:
  - **Chinese belongs to Chinese**: In the Chinese version of an essay, all text, headings, and diagram node labels must be pure Chinese. Strictly zero English subtitle lines (e.g. `<br/>English text`) in Chinese diagrams, unless annotating recognized proper nouns (e.g. DNA, API, AI).
  - **English belongs to English**: In the English version, all text, headings, and diagram node labels must be pure English.
  - **Bilingual completeness**: Essays with bilingual titles must feature complete parallel Chinese and English sections (including title, subtitle, lead, section headings, narrative prose, and Mermaid diagrams).
- **Relative cross-links**: Weave internal links using relative form only: `[title](../slug/)`. All targets must resolve to existing post files.
- **Mathematical notation**: Unicode only (e.g. `S₀`, `∇L`, `h`). **Strictly zero raw `$` or `$$` symbols**.
- **Vocabulary hygiene**: Zero occurrences of prohibited crutches:
  `['纯粹', '绝对', '完全', '彻底', '绝不', '通常', '往往', '或许', '某种意义上', '降维重构', '本质', '根本', '自始至终', '缰绳', '物理现实', '平庸', '物理意志']`.
- **Epistemological discipline**:
  - Will and agency belong strictly to living Minds. Never subordinate will to physics; never use "物理意志".
  - Matter and physics are macroscopic phenomena arising from friction between cognitive models and reality.
  - Objective facts are macroscopic phenomena maintaining invariance across different subjective cognitions.
  - Purge moralizing and judgmental rhetoric; maintain a rigorous first-person analytical perspective.

### 2. Cover Art (`assets/covers/<slug>.jpg`)
- **Default Generator**: Local **Qwen-Image-2.1** pipeline executed via `python3 scripts/generate-cover.py <slug> --prompt "..."` (7B DiT + Qwen3-VL 8B, bfloat16 on Apple Silicon MPS).
- **Default Aspect & Resolution**: Ultra-wide **21:9** landscape (`1344×576`, exact 21:9 integer multiple of 32, ~0.77 MP, ~5 min inference on M4 Pro; or 20:9 `1280×576`).
- **Styles Are NEVER Fixed (Content-Driven & Novelty-Seeking)**: The generator and aspect ratio are standard, but the **visual style and artistic medium are strictly never fixed**. For every new essay, invent a fresh artistic medium, print tradition, material texture, and palette derived directly from the specific epistemological cut of that post. Never converge into a single "house style" (strictly zero repetitive cliches, zero readable text, zero logos, zero tabletop stills).
- Registered in `assets/covers/STYLES.md` under both `Style families (used)` and the `Inventory` table as a living record of corpus diversity.

### 3. Companion NotebookLM Prompts (Chinese Only, Link-Free)
Located in `notebooklm-auto/prompts/`:
- **Audio Dialogue** (`notebooklm-auto/prompts/<slug>_zh.txt`): Deep dialogue between 明理 (engineering/systems reality) and 雨涵 (philosophy/cybernetics). Must contain three standard sections:
  1. `### [角色与对话规范]` (Roles, core epistemological constraints, perspective division).
  2. `### [核心议题清单]` (Structured topic outline).
  3. `### [正文对谈开场示例]` (Strictly an **opening dialogue sample** of 2–4 concise turns, **NOT a full episode script or transcript dump**. Sized < 8.5 KB, typically 3–6 KB, 25–45 lines. Must begin with the canonical *Not a Theory of Everything* opening delivered by 明理: summarizing that any theory is scaffolding, first-person perspective and causality are two sides of the same coin, neither closing the universe nor reactive rebellion, and stepping into living friction; followed by 雨涵's natural transition into the essay's core tension and 1–2 grounding turns, leaving NotebookLM to generate the rest of the dynamic discussion naturally from the topic checklist).
  *Rule*: The canonical Not-a-ToE opening on causality and first-person perspective is refined based on the new analysis of each essay, but NEVER deleted or omitted. The opening sample must strictly stay within 2–4 dialogue turns to avoid prompt bloat.
- **Video Monologue** (`notebooklm-auto/prompts/<slug>_video_zh.txt`): Single-speaker philosophical deep monologue articulating the essay's core cuts in continuous, spoken prose. Must contain:
  1. `### [单人深度文稿规范]`
  2. `### [核心议题脉络]`
  3. `### [正文文稿]` (Full unbroken spoken monologue script).
- **Rules**: Zero links (no markdown or HTML URLs), zero banned words, zero raw `$` symbols, audio prompt strictly concise (< 8.5 KB, 2–4 opening turns).

### 4. Walkthrough Document (`walkthrough.md`)
Stored in the active conversation artifact directory, structured as:
1. Visual Artifact & Cover Art embedding (`![caption](/absolute/path/to/cover.jpg)`) with concept.
2. Mermaid diagram inventory with semantic color rationale.
3. Core epistemological cuts & argument architecture.
4. Verification & invariant diagnostic check results.
5. **Companion NotebookLM Prompts (Chinese Only, Link-Free)**: File links and full prompt texts for Audio Dialogue and Video Monologue.
6. **Multi-Platform Publishing Copies**:
   - All four platform copies must explicitly include the canonical live link to the original essay (`https://powerpig99.github.io/not-a-toe/posts/<slug>/`):
     - Spotify Podcast (ZH) (includes original post URL)
     - Spotify Podcast (EN) (includes original post URL)
     - WeChat Video Channels (微信视频号) (includes original post URL)
     - X (Twitter) (EN Only) (includes original post URL)

### 5. Bidirectional Reverse Linking & Content Refinement (双向反向链接与语境织网)
- **Dense Cognitive Lattice**: An essay is never an isolated leaf node. Identify key upstream and conceptually adjacent essays referenced by the new post.
- **Backlink Integration**: Establish explicit reverse links from those prior essays back to the new post using the standard relative link format: `[<Title>](../<slug>/)`.
- **Narrative Prose Refinement**: Do not merely append naked links; organically rewrite and deepen the surrounding narrative prose of the linked essays to weave in the new essay's conceptual advances, epistemological cuts, and distinctions.
- **Invariant Adherence**: Modified linked essays must preserve strict bilingual symmetry (parallel updates in both Chinese and English sections) and pass all repository invariants (zero banned words, zero bulleted/numbered lists in prose, proper relative links).

---

## Standard Automated Audit & Build Pipeline

Always execute the complete verification sequence before finalizing:
1. `python3 scripts/audit-post.py <slug>` — Verifies all 9 authoring invariants (title/subtitle separation, banned words, latex, links, lists, mermaid dark theme & vertical flow, walkthrough, and companion prompts). Must return **CLEAN PASS**.
2. **Reverse Linking & Prose Refinement** — Establish backlinks and refine surrounding narrative prose in key referenced essays; verify modified essays pass repository invariants.
3. `node build.mjs` — Compiles the static site into `public/`.
4. `node scripts/project-posts-graph.mjs` — Re-projects lattice graph; ensures `missing_targets: 0`.
5. `node scripts/project-local-graph.mjs` — Updates local workspace graph tracker.
6. `git add ... && git commit -m "Publish Post #XXX: <Title>" && git push origin main`.
7. `gh run watch --exit-status` — Verifies GitHub Actions deployment succeeds.
8. `curl -sI https://powerpig99.github.io/not-a-toe/posts/<slug>/` — Confirms live HTTP 200.
9. `node scripts/export-absolute-md.mjs <slug>` — Exports absolute markdown for Substack / X Article distribution.\n