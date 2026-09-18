# Not a ToE — Standard Operating Procedures & Invariants

## Core Working Philosophy
> **"非必要不变更，防止无意识漂移。"**
> Standard conventions remain consistent by default across sessions.
> They are non-dogmatic: intentional, context-driven variations are permitted when specifically requested,
> but accidental omission, convenience-driven shortcutting, and unconscious drift are caught before release.

---

## Standard Post Authoring & Publishing Deliverables

For every new or revised essay, the complete deliverable set consists of:

### 1. Markdown Essay (`content/posts/<slug>.md`)
- **First line**: `# <Title>` (bilingual: Chinese / English).
- **Line 3**: `*<Subtitle>*` (one complete sentence; essence only, not section map).
- **Lead**: 2–4 complete sentences summarizing the argument before the first `##`.
- **Prose over lists**: **Strictly zero bulleted (`*`, `-`) or numbered (`1.`) lists in essay prose**. Complex causal arguments must unfold in flowing, continuous, rigorous narrative prose.
- **Mermaid styling**: All diagrams must adhere to the historical inline dark-theme palette:
  - Subgraphs: `style S_... fill:#161b22,stroke:#<hex>,stroke-width:1.5px,color:#<hex>`
  - Nodes: `style NodeID fill:#0d1117,stroke:#<hex>,stroke-width:1px,color:#f0f6fc`
  - Semantic colors: Green (`#3fb950` - Mind/sovereign judgment), Red (`#f85149` - Inversion/collapse/failure), Amber (`#d29922` - Scaffolding/tradeoffs), Blue (`#58a6ff` - Models/telemetry/signals), Purple (`#a371f7` - Self-referential loops/latent spaces).
- **Bilingual parallelism**: Every Chinese diagram must have an exact parallel English counterpart with identical node topology and semantic coloring.
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
- 16:9 or 20:9 landscape image (1280×720 or 1280×576).
- Invented, distinctive, non-crowded style family (zero text, zero legible symbols, zero dark chalk cliches).
- Registered in `assets/covers/STYLES.md` under both `Style families (used)` and the `Inventory` table.

### 3. Companion NotebookLM Prompts (Chinese Only, Link-Free)
Located in `notebooklm-auto/prompts/`:
- **Audio Dialogue** (`notebooklm-auto/prompts/<slug>_zh.txt`): Deep dialogue between 明理 (engineering/systems reality) and 雨涵 (philosophy/cybernetics), containing roles, core epistemological constraints, structured topic outline, and sample opening dialogue.
- **Video Monologue** (`notebooklm-auto/prompts/<slug>_video_zh.txt`): Single-speaker philosophical deep monologue articulating the essay's core cuts in continuous, spoken prose.
- **Rules**: Zero links (no markdown or HTML URLs), zero banned words, zero raw `$` symbols.

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

---

## Standard Automated Audit & Build Pipeline

Always execute the complete verification sequence before finalizing:
1. `python3 scripts/audit-post.py <slug>` — Verifies all 8 authoring invariants (post, prompts, and walkthrough). Must return **CLEAN PASS**.
2. `node build.mjs` — Compiles the static site into `public/`.
3. `node scripts/project-posts-graph.mjs` — Re-projects lattice graph; ensures `missing_targets: 0`.
4. `node scripts/project-local-graph.mjs` — Updates local workspace graph tracker.
5. `git add ... && git commit -m "Publish Post #XXX: <Title>" && git push origin main`.
6. `gh run watch --exit-status` — Verifies GitHub Actions deployment succeeds.
7. `curl -sI https://powerpig99.github.io/not-a-toe/posts/<slug>/` — Confirms live HTTP 200.
8. `node scripts/export-absolute-md.mjs <slug>` — Exports absolute markdown for Substack / X Article distribution.\n