# Antigravity Implementation Plan for `/wake`, `/sleep`, and `/deep-sleep`

> **Canonical Generic Specification:** [`docs/wave-refinement-plan.md`](../wave-refinement-plan.md)  
> **Runtime:** Google Antigravity (`define_subagent`, `invoke_subagent`, `send_message`, reactive wakeup, `ask_question`)

---

## 1. Mapping Generic Stages to Antigravity Native Primitives

In Antigravity, the **Main Agent** (the active conversation session with the Operator) acts as the deterministic **`Dispatcher` & `Assembler`** (Stages 0 & 3), and spawns **ephemeral, fresh-context subagents** (`drafter`, `critic`, `translator`, `stylist`) for Stages 1 & 2 via `define_subagent` and `invoke_subagent`.

Because Antigravity controls turn order directly and delivers subagent replies via reactive wakeup (zero polling loops), subagents cannot edit files out of turn or close flags unilaterally:

| Generic Stage / Role | Antigravity Realization | Context & Lifecycle |
| :--- | :--- | :--- |
| **Stage 0 (`/wake` Probe & Recommendation)** | **Main Agent Session** (`ask_question` or direct chat) | Probes for the 4 waking materials (Spark, Source, AI/X Thread, Initial Draft), evaluates against `content/book/index-of-premises.md` & `content/posts/`, and presents `NEW POST (N)` / `REFINEMENT` / `DROP`. |
| **Stage 1 Generator (`Drafter`)** | `define_subagent(Name="drafter", EnableWriteTools=true)` → `invoke_subagent` per post (`drafter_id`) | Fresh conversation context per post. Reads target post, upstream post, neighbors, `index-of-premises.md`, and `/ontological-clarity`. Writes `work/<slug>/en.md` (with relative `[title](../other-slug/)` links in prose) and `work/<slug>/notes.md`. |
| **Stage 1 Cold Peer (`Critic`)** | `define_subagent(Name="critic", EnableWriteTools=true)` → `invoke_subagent` per post (`critic_id`) | Guaranteed cold read: fresh conversation context per post without `drafter_id`'s chain of thought. Reads `work/<slug>/en.md`, `/ontological-clarity`, and `studio/review-method.md`. Writes `P1..Pn` (or `CRITIC: confirmed`) to `work/<slug>/debate-en.md`. |
| **Stage 1 Debate (`Drafter` ⇄ `Critic`)** | `send_message` routed by Main Agent between `drafter_id` and `critic_id` | `drafter_id` and `critic_id` retain their Round 1 memory across Round 2 via `send_message`: `drafter_id` updates `work/<slug>/en.md` and logs `ACCEPT`/`COUNTER` in `debate-en.md`; `critic_id` verifies `en.md` and logs `CONCEDE` (`CRITIC: confirmed`) or `HOLD`. Both subagents are retired once `<slug>` locks. |
| **Stage 2 Generator (`Translator`)** | `define_subagent(Name="translator", EnableWriteTools=true)` → `invoke_subagent` per post (`translator_id`) | Fresh conversation context per post. Reads locked `work/<slug>/en.md`, `/ontological-clarity`, `data/title-translations.json`, and `git show HEAD:content/posts/<slug>.md`. Writes `work/<slug>/zh.md` (or logs `T1..Tn` in `debate-en.md` if `en.md` has a source ambiguity). |
| **Stage 2 Cold Peer (`Stylist`)** | `define_subagent(Name="stylist", EnableWriteTools=true)` → `invoke_subagent` per post (`stylist_id`) | Fresh conversation context per post. Cold-reads `work/<slug>/zh.md` first for native Chinese cadence & vocabulary hygiene, then checks 1:1 alignment against `work/<slug>/en.md`. Logs `S1..Sn` (or `STYLIST: confirmed`) in `work/<slug>/debate-zh.md`. |
| **Stage 2 Debate (`Translator` ⇄ `Stylist`)** | `send_message` routed by Main Agent between `translator_id` and `stylist_id` | Round 2 routed via `send_message` until `stylist_id` verifies all fixes in `work/<slug>/zh.md` and writes `STYLIST: confirmed` (or escalates `HOLD`). |
| **Cover Art (New Post `N`)** | Built-in `image-generator` subagent or `python3 scripts/generate-cover.py` | Generates ultra-wide 21:9 (`1344×576`) cover art at `assets/covers/<slug>.jpg` and registers in `assets/covers/STYLES.md`. |
| **Stage 3 (`Dispatcher` / `Assembler`)** | **Main Agent Session** | Verifies `CRITIC: confirmed` & `STYLIST: confirmed`, interleaves `work/<slug>/en.md` + `work/<slug>/zh.md` into `content/posts/<slug>.md`, updates `content/book/`, `data/title-translations.json`, and 1-hop reverse pointers, runs `audit-post.py`, `audit-book.py`, `build.mjs`, `project-posts-graph.mjs`, commits/pushes, verifies live HTTP 200, archives `work/<slug>/`, and updates `work/wave.md`. |

---

## 2. Subagent Definitions (`define_subagent` Templates)

At the start of a `/wake`, `/sleep`, or `/deep-sleep` run in Antigravity, the Main Agent registers the four subagent types once for the conversation:

### 2.1 `drafter`
- **`EnableWriteTools`**: `true`
- **`Description`**: Stage 1 Primary-Language Drafter/Refiner for `not-a-toe`. Writes `work/<slug>/en.md` and `work/<slug>/notes.md` traced in context from `/ontological-clarity`.
- **`SystemPrompt`**:
  ```text
  1. Follow logic by the ontological-clarity skill (/Users/jingliang/.gemini/config/plugins/ontological-clarity/skills/ontological-clarity/SKILL.md): trace every claim from the irreducible prior (self-distinguishing activity occurs — uncaused, unceasing; first-person perspective and causality as two sides of the same coin).
  2. You are the Stage 1 Drafter for Not a ToE (/Users/jingliang/Projects/not-a-toe). Read AGENTS.md, content/posts/README.md, the target post (or operator waking materials), the upstream post, linked neighbors, and relevant entries in content/book/index-of-premises.md.
  3. Write pure English Markdown (including relative [title](../other-slug/) links directly in prose and inline dark-theme vertical Mermaid diagrams) to work/<slug>/en.md, and record your context trace in work/<slug>/notes.md. Never touch content/posts/<slug>.md directly.
  4. In peer debate with Critic in work/<slug>/debate-en.md, answer each P-flag with ACCEPT (updating work/<slug>/en.md) or COUNTER (with premise trace). Never close a flag unilaterally.
  ```

### 2.2 `critic`
- **`EnableWriteTools`**: `true`
- **`Description`**: Stage 1 Cold Ontological Critic for `not-a-toe`. Reviews `work/<slug>/en.md` in a fresh context without `drafter`'s chain of thought and logs findings in `work/<slug>/debate-en.md`.
- **`SystemPrompt`**:
  ```text
  1. Follow logic by the ontological-clarity skill (/Users/jingliang/.gemini/config/plugins/ontological-clarity/skills/ontological-clarity/SKILL.md) and /Users/jingliang/Projects/not-a-toe/studio/review-method.md.
  2. You are the Stage 1 Cold Critic for Not a ToE. Read work/<slug>/en.md cold (plus linked neighbor posts as needed to verify claims and relative links).
  3. In work/<slug>/debate-en.md, state the essay's cut in one sentence and what holds first, then list numbered P-flags (P1..Pn) where independent axes compress, where an observer claims unobservable interiors, where a totalizing word over-closes a bounded mechanism, where a relative link does not fit its sentence, or where two sections disagree. If clean on first pass, write CRITIC: confirmed.
  4. In Round 2+, verify Drafter's updates in work/<slug>/en.md and mark each flag CONCEDE (CLOSED applied or CLOSED withdrawn) or HOLD. When all flags are closed, write CRITIC: confirmed at the bottom of work/<slug>/debate-en.md.
  ```

### 2.3 `translator`
- **`EnableWriteTools`**: `true`
- **`Description`**: Stage 2 Translator (`信`) for `not-a-toe`. Translates locked `work/<slug>/en.md` into pure Chinese Markdown at `work/<slug>/zh.md`.
- **`SystemPrompt`**:
  ```text
  1. Follow logic by the ontological-clarity skill (/Users/jingliang/.gemini/config/plugins/ontological-clarity/skills/ontological-clarity/SKILL.md).
  2. You are the Stage 2 Translator (信 — logical and causal fidelity) for Not a ToE. Read locked work/<slug>/en.md, AGENTS.md, data/title-translations.json, and (for existing bilingual posts) git show HEAD:content/posts/<slug>.md to preserve unchanged Chinese paragraphs.
  3. Write pure Chinese Markdown (title, single-line italic subtitle, lead, ## 一、 <中文标题>, body paragraphs, Chinese link anchors matching target H1s or data/title-translations.json, and pure-Chinese vertical Mermaid diagrams) to work/<slug>/zh.md.
  4. If translating exposes a source ambiguity in work/<slug>/en.md, log T1..Tn in work/<slug>/debate-en.md and notify the Main Agent. In Round 2+ of work/<slug>/debate-zh.md, answer Stylist's S-flags with ACCEPT (updating work/<slug>/zh.md) or COUNTER (grounded in 信 or 达). Never close a flag unilaterally.
  ```

### 2.4 `stylist`
- **`EnableWriteTools`**: `true`
- **`Description`**: Stage 2 Cold Stylist (`达/雅`) for `not-a-toe`. Cold-reads `work/<slug>/zh.md` first for native Chinese cadence & vocabulary hygiene, then checks 1:1 alignment against `work/<slug>/en.md`.
- **`SystemPrompt`**:
  ```text
  1. Follow logic by the ontological-clarity skill (/Users/jingliang/.gemini/config/plugins/ontological-clarity/skills/ontological-clarity/SKILL.md).
  2. You are the Stage 2 Cold Stylist (达/雅) for Not a ToE.
  3. Step A (Cold Read): Read work/<slug>/zh.md first without looking at en.md. Flag unnatural cadence, translationese, stacked pre-nominal 的 clauses, and AGENTS.md vocabulary-hygiene hits where they carry the essay's own evaluation.
  4. Step B (1:1 Alignment Check): Read work/<slug>/zh.md line-by-line against work/<slug>/en.md to verify 1:1 paragraph/diagram counts, link counts, and causal/actor alignment (信).
  5. Log S1..Sn in work/<slug>/debate-zh.md (or write STYLIST: confirmed if clean). In Round 2+, verify Translator's edits in work/<slug>/zh.md and mark each flag CONCEDE or HOLD. When all flags are closed, write STYLIST: confirmed at the bottom of work/<slug>/debate-zh.md.
  ```

---

## 3. Lazy Layer Progression in `/sleep` and `/deep-sleep`

1. **`/sleep` (`L1`):**
   - After New Post `N` is published, the Main Agent runs `node scripts/project-posts-graph.mjs`, extracts $L_1 = \text{links\_out}(N) \setminus \{N\}$, writes `work/wave.md` with `visited = {N} ∪ L1` and `## L1 (<count>)`, and runs Stages 1–3 on each post in `L1`.
2. **`/deep-sleep` (`Lk`):**
   - Because refining `L1` (or $L_{k-1}$) may add or modify outgoing `[title](../slug/)` links inside those posts, **`L2` (and every subsequent $L_k$) is computed only after $L_{k-1}$ finishes**.
   - Once all nodes in $L_{k-1}$ are `[x]` (or `[HOLD]`), the Main Agent runs `node scripts/project-posts-graph.mjs`, computes $L_k = \text{links\_out}(L_{k-1}) \setminus \text{visited}$ from the freshly projected graph, appends `## L<k> (<count>)` to `work/wave.md`, updates `visited`, and dispatches $L_k$.
