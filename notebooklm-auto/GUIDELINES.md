# NotebookLM Auto Prompt Engineering & Publishing Copy Guidelines

This document defines the canonical schemas, epistemological invariants, and generation standards for creating **NotebookLM Audio Overviews**, **Short-Form Video Scripts**, and **Multi-Platform Publishing Copy** (Spotify, WeChat Channels, and X) across the *Not a Theory of Everything (Not-A-TOE)* corpus.

---

## 1. Epistemological Invariants (Non-Negotiable)

1. **First-Person & Causality as Two Sides of the Same Coin**:
   - The first-person horizon (finite distinctions perceived now) and causality (open potential extending endlessly) are inseparable.
   - Explanations terminate at the first-person actor's live trade-offs, choices, and physical interventions (`+1`). Pushing past this into deterministic biological, cultural, or mechanical reductionism is cognitive evasion.
2. **Zero System Agency / Purge Reification**:
   - Systems, institutions, algorithms, and "objective laws" possess zero independent causal agency. They are emergent macro phenomena arising from conscious practitioners injecting free variables.
   - Never treat the "system" as an autonomous judge, punisher, or benevolent entity.
3. **No Essentialism or "View from Nowhere"**:
   - Never use metaphysical essentialist claims (e.g. avoid treating "essence" or "fundamentally" as disembodied objective entities).
   - Frame observations phenomenologically within first-person human experience and causal tracing.
4. **Artifacts as Residual Traces**:
   - All tools and artifacts (axes, rockets, LLMs) are historical traces left by the injection of human free choices. They lack the agency to autonomously inject free variables and possess zero independent intelligence.
   - Only conscious subjective minds possess true intelligence. AI is living intelligence mathematically simulating and extending its own faculties.
5. **Duality of Free Choice vs. Statistical Distributions**:
   - Micro sovereign choices are free at moment t; their population aggregation naturally forms normal distributions and compounds over time into power-law or exponential forms.
   - Believing that statistical distributions constitute an inescapable cage is itself a sovereign free choice. Third-person unpredictability is the outward signature of first-person subjective self-consistency.
6. **No Links Inside Prompt Instructions**:
   - Prompts serve as NotebookLM customization instructions given to the model alongside the imported source text. Since the blog post is already loaded as source material, links are unnecessary in prompt files (links belong in external social copy and Spotify descriptions only).
7. **Clean Typography**:
   - No raw LaTeX markup (use clean Chinese full-width brackets `（t）` and English text `moment t`).

---

## 2. Canonical File Structure & Naming Convention

For each post with slug `<SLUG>`, the following 4 files are maintained in `notebooklm-auto/prompts/`:

1. **Chinese Audio Overview**: `<SLUG>_zh.txt`
2. **English Audio Overview**: `<SLUG>.txt`
3. **Chinese Video Monologue**: `<SLUG>_video_zh.txt`
4. **English Video Monologue**: `<SLUG>_video_en.txt`

---

## 3. Template Schemas for Prompts

### Schema A: Chinese Audio Overview (`<SLUG>_zh.txt`)
```markdown
### [角色与对话规范]
* **形式与基调**：两路心智思辨视角（明理与雨涵）之间的自然深度对谈。聚焦...，杜绝学术说教、道德审判与机械清单。以真诚、敏锐、从容的对话，在观点的切磋与剖析中展开思考。肯定而不武断，不用否定来肯定，而是呈现理解与改善。
* **核心认识论禁令（至关重要）**：
  1. [核心禁令 1]
  2. [核心禁令 2]
  3. [核心禁令 3]
  4. [核心禁令 4]

* **视角分工**：
  - **明理（视角1）**：...
  - **雨涵（视角2）**：...

### [核心议题清单：“{{TITLE}}”]
- [议题 1]
- [议题 2]
...

### [开场台词 - 明理]
明理：[开场陈述]

雨涵：[呼应并引出核心张力]
(雨涵自然接话：...)
```

### Schema B: English Audio Overview (`<SLUG>.txt`)
```markdown
### [Role and Conversation Guidelines]
* **Format and Tone**: A natural, deeply reflective philosophical dialogue between two sharp analytical minds (Julian and Clara). Focus on ..., without preachiness, moralizing lectures, or forced slogans. Affirmative without being absolutist, improving rather than merely negating.
* **Core Epistemological Invariants (CRITICAL)**:
  1. [Invariant 1]
  2. [Invariant 2]
  3. [Invariant 3]
  4. [Invariant 4]

* **Perspective Division**:
  - **Julian (Speaker 1)**: ...
  - **Clara (Speaker 2)**: ...

### [Core Agenda: "{{TITLE}}"]
- [Agenda item 1]
- [Agenda item 2]
...

### [Opening Line - Julian]
Julian: [Opening thesis]

Clara: [Response and pivot]
(Clara continues naturally: ...)
```

### Schema C: Chinese Video Monologue (`<SLUG>_video_zh.txt`)
```markdown
### [短视频口述文案规范]
* **定位与基调**：第一人称思辨独白，沉静、透彻、富有前沿视野与因果力量。从“...”切入，剖析...。肯定而不武断，不用否定来肯定，注重理解与改善。
* **语言风格**：短句交错，层层递进，杜绝学术空话与说教腔调，直击人心。
* **核心内容脉络**：
  1. **现象切入**：...
  2. **认识论根基**：...
  ...

### [口述参考台词]
[口述逐字稿]
```

### Schema D: English Video Monologue (`<SLUG>_video_en.txt`)
```markdown
### [Short-Form Video Monologue Guidelines]
* **Positioning and Tone**: A first-person philosophical monologue, calm, piercing, rich in frontier vision and causal weight. Hooking from "...", dissecting ... Affirmative without being absolutist, improving rather than merely negating.
* **Style**: Alternating concise rhythmic lines, progressive conceptual depth, zero academic jargon or preachiness.
* **Core Narrative Arc**:
  1. **The Hook**: ...
  2. **Epistemological Root**: ...
  ...

### [Spoken Script]
[Spoken script lines]
```

---

## 4. Standardized Multi-Platform Publishing Copy Schemas

To prevent tone drift and stylistic inconsistency across releases, all distribution copy must strictly adhere to the following schemas:

### A. Spotify Podcast Channel (ZH & EN)
* **Title Format (ZH)**: `EP<Number>｜<Core Chinese Title>`
* **Description Format (ZH)**:
  - 2 essayistic paragraphs:
    - *Paragraph 1*: Problem hook & category error deconstruction + key physical/engineering metaphor.
    - *Paragraph 2*: Epistemological core mechanism + first-person causal sovereignty takeaway.
  - *Footer*: `🔗 完整深度长文：https://powerpig99.github.io/not-a-toe/posts/<slug>/`
* **Title Format (EN)**: `EP<Number> | <Core English Title>`
* **Description Format (EN)**:
  - 2 continuous essayistic paragraphs matching the Chinese thematic depth.
  - *Footer*: `🔗 Read the full essay: https://powerpig99.github.io/not-a-toe/posts/<slug>/`

### B. WeChat Channels / Video Platforms (微信视频号 / 抖音 / B站)
* **Title Format**: `【<Core Chinese Title>】`
* **Caption / Post Copy**:
  - *Paragraph 1*: High-tension question or phenomenon hook.
  - *Paragraph 2*: Deep epistemological insight (artifacts as traces, no disembodied system, the true locus of agency).
  - *Paragraph 3*: Decisive punchline (Realign or become the error term).
  - *Hashtags*: `#非万物之理 #认识论 #哲学思考 #人工智能 #第一人称主权`
  - *Footer*: `🔗 完整长文请参阅：https://powerpig99.github.io/not-a-toe/posts/<slug>/`

### C. X (Twitter) Article & Thread Copy (EN & ZH)
* **EN Format**:
  - *Hook Line*: High-impact sentence challenging conventional tech/philosophical consensus.
  - *Thread Beats (3-4 concise blocks)*:
    1. The False Dichotomy / Delusion
    2. The Engineering Metaphor
    3. The Epistemological Demarcation (Tool vs. Mind)
    4. The Evolutionary Takeaway
  - *CTA / Link*: Direct link to the live article.
* **ZH Format**:
  - *Hook Line*: 穿透性主张
  - *Thread Beats*: 核心剖析、隐喻对照、主权回归
  - *CTA / Link*: 直达博文链接。
