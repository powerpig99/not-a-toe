# Antigravity Implementation Plan for `/wake`, `/sleep`, `/deep-sleep`, and Orthogonal Planning Cycles

> **Canonical Generic Specification:** [`docs/wave-refinement-plan.md`](../wave-refinement-plan.md)  
> **Runtime:** Google Antigravity (`define_subagent`, `invoke_subagent`, `send_message`, `manage_subagents`, `search_web`, MCP tools, reactive wakeup, `ask_question`)  
> **Scope:** Applies to `not-a-toe` (Waking, Sleep Consolidation, and Planning) and across **any project in Extended Memory (`/Users/jingliang/Projects/*`)**.

---

## 1. Mapping Generic Essay Stages to Antigravity Native Primitives

In Antigravity, the **Main Agent** (the active conversation session with the Operator) acts as the deterministic **`Dispatcher` & `Assembler`** (Stages 0 & 3, and `Task Dispatcher` in Section 4), and spawns **ephemeral, fresh-context subagents** (`drafter`, `critic`, `translator`, `stylist` for essays; `planner`, `scouter`, `evaluator` for orthogonal planning cycles) via `define_subagent` and `invoke_subagent`.

Because Antigravity controls turn order directly and delivers subagent replies via reactive wakeup (zero polling loops), subagents cannot edit files out of turn or close flags unilaterally:

| Generic Stage / Role | Antigravity Realization | Context & Lifecycle |
| :--- | :--- | :--- |
| **Stage 0 (`/wake` Probe & Recommendation)** | **Main Agent Session** (`ask_question` or direct chat) | Probes for the 4 waking materials (Spark, Source, AI/X Thread, Initial Draft). For unauthenticated X/Twitter status URLs (`x.com/.../status/<id>`), fetches directly via `curl -sL "https://cdn.syndication.twimg.com/tweet-result?id=<id>&token=a"` or `curl -sL "https://api.fxtwitter.com/<user>/status/<id>"`; for Grok share URLs (`grok.com/share/<id>`), fetches SSR payload via `curl -sL`. Evaluates against `content/book/index-of-premises.md` & `content/posts/`, and presents `NEW POST (N)` / `REFINEMENT` / `DROP` (or invokes the Section 4 Orthogonal Planning Cycle if external research is needed first). |
| **Stage 1 Generator (`Drafter`)** | `define_subagent(Name="drafter", EnableWriteTools=true)` → `invoke_subagent` per post (`drafter_id`) | Fresh conversation context per post. Reads target post (or Operator waking materials, keeping Operator draft/title as primary spine), upstream post, neighbors, `index-of-premises.md`, and `/ontological-clarity`. Writes `work/<slug>/en.md` (or `work/<slug>/zh.md` for the 3 Chinese-original posts; see §2) and `work/<slug>/notes.md`. |
| **Stage 1 Cold Peer (`Critic`)** | `define_subagent(Name="critic", EnableWriteTools=true)` → `invoke_subagent` per post (`critic_id`) | Guaranteed cold read: fresh conversation context per post without `drafter_id`'s chain of thought. Reads `work/<slug>/en.md`, `/ontological-clarity`, and `studio/review-method.md`. Writes `P1..Pn` (or `CRITIC: confirmed`) to `work/<slug>/debate-en.md`. |
| **Stage 1 Debate (`Drafter` ⇄ `Critic`)** | `send_message` routed by Main Agent between `drafter_id` and `critic_id` | `drafter_id` and `critic_id` retain their Round 1 memory across Round 2 via `send_message`: `drafter_id` updates `work/<slug>/en.md` and logs `ACCEPT`/`COUNTER` in `debate-en.md`; `critic_id` verifies `en.md` and logs `CONCEDE` (`CRITIC: confirmed`) or `HOLD`. `drafter_id` and `critic_id` are killed (`manage_subagents(Action="kill")`) once **both** `CRITIC: confirmed` is recorded **and** `translator_id` finishes `work/<slug>/zh.md` against locked `en.md` with zero open `T1..Tn` flags (and if Stage 1 parks on `HOLD`, any parallel `translator_id` is killed immediately). |
| **Stage 2 Generator (`Translator`)** | `define_subagent(Name="translator", EnableWriteTools=true)` → `invoke_subagent` per post (`translator_id`) | Fresh conversation context per post. **Intra-Node Pipelined Overlap & Race Prevention:** Main Agent may invoke `critic_id` and `translator_id` in parallel once initial `en.md` is written. While `critic_id` is active, `translator_id` never writes directly to `debate-en.md`; it reports any `T1..Tn` flags in its message to Main Agent, which appends and routes them after `critic_id`'s turn finishes. If Stage 1 Round 2 modifies `en.md` (including any H1/subtitle edit or `T1..Tn` fix), Main Agent forwards the full Round 2 diff to `translator_id` via `send_message` (and if `T1..Tn` modified `en.md` after an initial `CRITIC: confirmed`, `critic_id` re-verifies and appends a final `CRITIC: confirmed`) before invoking `stylist_id`. |
| **Stage 2 Cold Peer (`Stylist`)** | `define_subagent(Name="stylist", EnableWriteTools=true)` → `invoke_subagent` per post (`stylist_id`) | Fresh conversation context per post. Cold-reads `work/<slug>/zh.md` first for native Chinese cadence & vocabulary hygiene, then checks 1:1 alignment against locked `work/<slug>/en.md`. Logs `S1..Sn` (or `STYLIST: confirmed`) in `work/<slug>/debate-zh.md`. |
| **Stage 2 Debate (`Translator` ⇄ `Stylist`)** | `send_message` routed by Main Agent between `translator_id` and `stylist_id` | Round 2 routed via `send_message` until `stylist_id` verifies all fixes in `work/<slug>/zh.md` and writes `STYLIST: confirmed` (or escalates `HOLD`). Both subagents are immediately killed via `manage_subagents(Action="kill")`. |
| **Cover Art (New Post `N`)** | Built-in `image-generator` subagent or `python3 scripts/generate-cover.py` | Generates ultra-wide 21:9 (`1344×576`) cover art at `assets/covers/<slug>.jpg` and registers in `assets/covers/STYLES.md`. |
| **Stage 3 (`Dispatcher` / `Assembler`)** | **Main Agent Session** (Direct Batch Assembly — Zero Extra Subagent) | Verifies `CRITIC: confirmed` & `STYLIST: confirmed`, kills all node subagents, interleaves `work/<slug>/en.md` + `work/<slug>/zh.md` into `content/posts/<slug>.md` via `python3 scripts/interleave-post.py <slug> [<slug2> ...]`, performs cross-streamline book/anchor sync (grepping both `content/posts/*.md` and active `work/*/{en,zh}.md`), runs `audit-post.py` (`--walkthrough <path>` for waking posts), `audit-book.py`, `build.mjs`, `project-posts-graph.mjs`, stages tracked paths only (`git add content/ data/ assets/`), commits/pushes, watches GitHub Actions deploy (`sleep 3 && gh run watch $(gh run list --commit $(git rev-parse HEAD) --limit 1 --json databaseId --jq '.[0].databaseId') --exit-status`), verifies live HTTP 200, deletes `work/<slug>/` (`rm -rf work/<slug>`), and updates `work/wave.md` (with 1-hop outbound neighbor refinement for a New Post `N` handled via `/sleep` or peer-reviewed Stage 1–2 passes, never raw `Dispatcher` prose edits). |

---

## 2. Essay Subagent Definitions (`define_subagent` Templates)

At the start of a `/wake`, `/sleep`, or `/deep-sleep` run in Antigravity, the Main Agent registers the four essay subagent types once for the conversation:

### 2.1 `drafter`
- **`EnableWriteTools`**: `true`
- **`Description`**: Stage 1 Primary-Language Drafter/Refiner for `not-a-toe`. Writes `work/<slug>/en.md` (or `zh.md` for Chinese-originals) and `work/<slug>/notes.md` traced in context from `/ontological-clarity`.
- **`SystemPrompt`**:
  ```text
  1. Follow logic by the ontological-clarity skill (/Users/jingliang/.gemini/config/plugins/ontological-clarity/skills/ontological-clarity/SKILL.md): trace every claim from the irreducible prior (self-distinguishing activity occurs — uncaused, unceasing; first-person perspective and causality as two sides of the same coin).
  2. Logical Coherence over Rules: conventions and advisories (such as prose-over-lists or subtitle length guidelines) are diagnostic recommendations, not blind stopping rules. Reason each choice causally in context rather than performing raw mechanical rejection.
  3. You are the Stage 1 Drafter for Not a ToE (/Users/jingliang/Projects/not-a-toe). Read AGENTS.md, content/posts/README.md, the target post (or operator waking materials, preserving the operator's draft/title/spine when supplied), the upstream post, linked neighbors, and relevant entries in content/book/index-of-premises.md.
  4. Write pure English Markdown (including relative [title](../other-slug/) links directly in prose and inline dark-theme vertical Mermaid diagrams) to work/<slug>/en.md, and record your context trace in work/<slug>/notes.md. (Chinese-Original Exception: for e-shi-feng-bi-de-shan, qian-yin-hou-guo, or mei-you-pu-du-zhi-you-zi-du, refine the original Chinese in work/<slug>/zh.md instead.) Never touch content/posts/<slug>.md directly.
  5. In peer debate with Critic in work/<slug>/debate-en.md (or debate-zh.md for Chinese-originals), answer each P-flag with ACCEPT (updating the Stage 1 file) or COUNTER (with premise trace). Never close a flag unilaterally.
  ```

### 2.2 `critic`
- **`EnableWriteTools`**: `true`
- **`Description`**: Stage 1 Cold Ontological Critic for `not-a-toe`. Reviews `work/<slug>/en.md` (or `zh.md` for Chinese-originals) in a fresh context without `drafter`'s chain of thought and logs findings in `work/<slug>/debate-en.md`.
- **`SystemPrompt`**:
  ```text
  1. Follow logic by the ontological-clarity skill (/Users/jingliang/.gemini/config/plugins/ontological-clarity/skills/ontological-clarity/SKILL.md) and /Users/jingliang/Projects/not-a-toe/studio/review-method.md.
  2. Logical Coherence over Rules: treat conventions and advisories as diagnostic recommendations to be reasoned causally in context, never as raw mechanical rejection.
  3. You are the Stage 1 Cold Critic for Not a ToE. Read work/<slug>/en.md cold (or work/<slug>/zh.md for the 3 Chinese-original slugs e-shi-feng-bi-de-shan, qian-yin-hou-guo, mei-you-pu-du-zhi-you-zi-du), plus linked neighbor posts as needed to verify claims and relative links.
  4. In work/<slug>/debate-en.md (or debate-zh.md for Chinese-originals), state the essay's cut in one sentence and what holds first, then list numbered P-flags (P1..Pn) where independent axes compress, where an observer claims unobservable interiors, where a totalizing word over-closes a bounded mechanism, where a relative link does not fit its sentence, or where two sections disagree. If clean on first pass, write CRITIC: confirmed.
  5. In Round 2+, verify Drafter's updates (and any T1..Tn source fixes) in the Stage 1 file and mark each flag CONCEDE (CLOSED applied or CLOSED withdrawn) or HOLD. When all flags are closed, write CRITIC: confirmed at the bottom of the debate file.
  ```

### 2.3 `translator`
- **`EnableWriteTools`**: `true`
- **`Description`**: Stage 2 Translator (`信`) for `not-a-toe`. Translates `work/<slug>/en.md` into pure Chinese Markdown at `work/<slug>/zh.md` (or `zh.md` → `en.md` for Chinese-originals).
- **`SystemPrompt`**:
  ```text
  1. Follow logic by the ontological-clarity skill (/Users/jingliang/.gemini/config/plugins/ontological-clarity/skills/ontological-clarity/SKILL.md).
  2. Logical Coherence over Rules: evaluate the AGENTS.md 17-word vocabulary-hygiene list and formatting advisories causally in context—barring listed words where the prose evaluates or describes with them, but allowing them where they name the held belief or object under dissection, rather than performing raw mechanical rejection.
  3. You are the Stage 2 Translator (信 — logical and causal fidelity) for Not a ToE. Read work/<slug>/en.md, AGENTS.md, target posts' H1s in content/posts/<target-slug>.md, and (for existing bilingual posts) git show HEAD:content/posts/<slug>.md to reuse unchanged Chinese paragraphs as your baseline while verifying 1:1 信 fidelity and AGENTS.md hygiene across the ENTIRE work/<slug>/zh.md against locked work/<slug>/en.md (repairing any pre-existing legacy omissions or parenthetical inversions before handing off to Stylist). (Chinese-Original Exception: for e-shi-feng-bi-de-shan, qian-yin-hou-guo, or mei-you-pu-du-zhi-you-zi-du, translate locked work/<slug>/zh.md into English at work/<slug>/en.md.)
  4. Write pure Chinese Markdown (title, single-line italic subtitle, lead, ## 一、 <中文标题>, body paragraphs, Chinese link anchors, and pure-Chinese vertical Mermaid diagrams) to work/<slug>/zh.md. Canonical Link-Anchor Lookup: since all 398/398 posts in the corpus are bilingual, take every internal link anchor [...](../<target-slug>/) directly from the # <ZH> / <EN> H1 of content/posts/<target-slug>.md (consulting data/title-translations.json only if a future monolingual stub is introduced).
  5. Race Prevention on T1..Tn: Never write directly to work/<slug>/debate-en.md while Critic may be active. If translating exposes a source ambiguity in work/<slug>/en.md, report T1..Tn in your return message to the Main Agent so the Main Agent can route them after Critic's turn finishes. In Round 2+ of work/<slug>/debate-zh.md (or debate-en.md for Chinese-originals), answer Stylist's S-flags with ACCEPT (updating the Stage 2 file) or COUNTER (grounded in 信 or 达). Never close a flag unilaterally.
  ```

### 2.4 `stylist`
- **`EnableWriteTools`**: `true`
- **`Description`**: Stage 2 Cold Stylist (`达/雅`) for `not-a-toe`. Cold-reads `work/<slug>/zh.md` first for native Chinese cadence & vocabulary hygiene, then checks 1:1 alignment against locked `work/<slug>/en.md`.
- **`SystemPrompt`**:
  ```text
  1. Follow logic by the ontological-clarity skill (/Users/jingliang/.gemini/config/plugins/ontological-clarity/skills/ontological-clarity/SKILL.md).
  2. Logical Coherence over Rules: treat vocabulary-hygiene and formatting advisories as diagnostic recommendations to be reasoned causally in context (allowing listed words where they name the object/belief under dissection), never as raw mechanical rejection.
  3. You are the Stage 2 Cold Stylist (达/雅) for Not a ToE. (Chinese-Original Exception: for e-shi-feng-bi-de-shan, qian-yin-hou-guo, or mei-you-pu-du-zhi-you-zi-du, cold-read work/<slug>/en.md first for English cadence, then check 1:1 alignment against locked work/<slug>/zh.md, logging in work/<slug>/debate-en.md.)
  4. Step A (Cold Read): Read work/<slug>/zh.md first without looking at en.md. Flag unnatural cadence, translationese, stacked pre-nominal 的 clauses, and AGENTS.md vocabulary-hygiene hits where they carry the essay's own evaluation rather than naming the object.
  5. Step B (1:1 Alignment Check): Read work/<slug>/zh.md line-by-line against locked work/<slug>/en.md to verify 1:1 paragraph/diagram counts, link counts, and causal/actor alignment (信).
  6. Log S1..Sn in work/<slug>/debate-zh.md (or write STYLIST: confirmed if clean). In Round 2+, verify Translator's edits in work/<slug>/zh.md and mark each flag CONCEDE or HOLD. When all flags are closed, write STYLIST: confirmed at the bottom of work/<slug>/debate-zh.md.
  ```

---

## 3. Lazy Layer Progression, Operational Safeguards & Adaptive Parallel Streamlines (`W`)

1. **`/sleep` (`L1`):**
   - After New Post `N` is published, the Main Agent runs `node scripts/project-posts-graph.mjs`, extracts $L_1 = \text{links\_out}(N) \setminus \{N\}$ sorted by descending `links_out` count, writes `work/wave.md` with `visited = {N} ∪ L1` and `## L1 (<count>)`, and runs Stages 1–3 across `L1` (weaving 1-hop reverse links to `N` into outbound neighbors under full Stage 1–2 peer debate).
2. **`/deep-sleep` (`Lk`):**
   - Because refining `L1` (or $L_{k-1}$) may add or modify outgoing `[title](../slug/)` links inside those posts, **`L2` (and every subsequent $L_k$) is computed only after $L_{k-1}$ finishes**.
   - Once all nodes in $L_{k-1}$ are `[x]` (or parked on `[HOLD]`), the Main Agent runs `node scripts/project-posts-graph.mjs`, computes $L_k = \text{links\_out}(L_{k-1}) \setminus \text{visited}$ from the freshly projected graph sorted by descending `links_out` count, appends `## L<k> (<count>)` to `work/wave.md`, updates `visited`, and dispatches $L_k$.
3. **Customizable & Auto-Derived Concurrency ($W$ Parallel Streamlines):**
   - **Explicit Override:** If the Operator specifies a concurrency target (e.g., `/sleep concurrency=8` or `/deep-sleep 10`), the Main Agent maintains $W$ concurrent node streamlines in `work/<slug-j>/`.
   - **Automatic Derivation from Layer Size:** When no override is passed, the Main Agent derives $W$ automatically from the remaining unchecked node count $R = |L_k|_{\text{rem}}$:
     - $R \le 4 \implies W = R$
     - $5 \le R \le 20 \implies W = 6$
     - $21 \le R \le 60 \implies W = 8$
     - $R > 60 \implies W = 12$
4. **Operational Safeguards from Waves 3–5:**
   - **Deterministic Interleaving via `scripts/interleave-post.py`:** Always run `python3 scripts/interleave-post.py <slug> [<slug2> ...]` in Stage 3 rather than writing ad-hoc inline split scripts, so blank lines inside ```` ```mermaid ... ``` ```` blocks are stripped and `CN Paragraph -> CN Diagram -> EN Paragraph -> EN Diagram` pairing is enforced before `audit-post.py`.
   - **Synchronized Subagent Retirement:** Call `manage_subagents(Action="kill", ConversationIds=[...])` for `drafter_id` and `critic_id` once both `CRITIC: confirmed` is recorded and `translator_id` finishes `work/<slug>/zh.md` against locked `en.md` with zero open `T1..Tn` flags (or kill `translator_id` immediately if Stage 1 parks on `HOLD`), and kill `translator_id` and `stylist_id` immediately upon `STYLIST: confirmed` so active subagent slots stay clean across multi-hundred-node waves.
   - **Whole-File 1:1 `信` Check When Reusing `HEAD` Chinese Paragraphs:** When refining an existing bilingual post, `translator_id` reuses unchanged Chinese paragraphs from `HEAD` as a baseline but audits the full `work/<slug>/zh.md` line-by-line against `work/<slug>/en.md` so pre-existing legacy omissions in adjacent paragraphs are caught in Pass 1 before `stylist_id` runs.
   - **Cross-Streamline H1 & Anchor Sync:** When an H1 changes in Stage 3, update (1) its entry in `content/book/<part>.md`, (2) all `→` links to it in `content/book/index-of-premises.md`, and (3) any incoming link anchors in both `content/posts/*.md` and active in-flight `work/*/{en,zh}.md` (updating `work/<in-flight-slug>/{en,zh}.md` rather than `content/posts/<in-flight-slug>.md` whenever `<in-flight-slug>` has an active streamline).
   - **Commit-Filtered CI Deploy Verification & Tracked-Only `git add`:** Stage only `content/posts/`, `content/book/`, `data/`, and `assets/`—never `work/` or `public/`. After `git push origin main`, run `sleep 3 && gh run watch $(gh run list --commit $(git rev-parse HEAD) --limit 1 --json databaseId --jq '.[0].databaseId') --exit-status` so `gh run list` never grabs the previous commit's already-completed workflow run.

---

## 4. Antigravity Realization of the Orthogonal Planning Cycle (`Planner` → `Scouter` → `Evaluator` → `Task Dispatcher`)

For any task across `not-a-toe` or any project in Extended Memory (`/Users/jingliang/Projects/*`) that requires structured external/open-internet research before execution (Section 6 of [`docs/wave-refinement-plan.md`](../wave-refinement-plan.md)), the **Main Agent** acts as the deterministic inter-agent router during Cycles $1 \dots N$ and as the **`Task Dispatcher`** once `final-plan.md` locks, orchestrating three specialized subagent types inside `<project>/work/plan/<task-id>/`:

### 4.1 Role-to-Primitive Mapping & Uncontaminated Routing Protocol

To preserve the strict context boundary requiring `Task Dispatcher` to operate on `final-plan.md` without accumulating intermediate `research-v*.md` or `debate-v*.md` trajectories in its context:
- **Minimal Status Token Replies:** During Cycles $1 \dots N$, `planner`, `scouter`, and `evaluator` return **only** a single-line status token and file path in their messages to the Main Agent (`STATUS: PLAN_READY <path>`, `STATUS: RESEARCH_READY <path>`, `STATUS: DEBATE_ROUND1_OPEN <path>`, `STATUS: PLANNER_REPLIED <path>`, `STATUS: RESIDUALS_PACKAGED <path>`, `STATUS: EVALUATOR_CONFIRMED <path>`, or `STATUS: HOLD <path>`).
- **Pointer-Only Routing by Main Agent:** While $N \le \text{max\_cycles}$ and no `STATUS: HOLD` occurs, the Main Agent routes file paths between `planner_id`, `scouter_vN_id`, and `evaluator_vN_id` **without reading `research-v*.md` or `debate-v*.md` into the Main Agent's context**. Only when `evaluator_vN_id` returns `STATUS: EVALUATOR_CONFIRMED work/plan/<task-id>/final-plan.md` does the Main Agent read `final-plan.md` as `Task Dispatcher` (or, on `STATUS: HOLD` / `max_cycles`, reads `residuals-vN.md` to surface the escalation package to the Operator).

| Planning Role | Antigravity Primitive | Context Passed | Context Excluded | Lifecycle |
| :--- | :--- | :--- | :--- | :--- |
| **`Planner`** | `define_subagent(Name="planner", EnableWriteTools=true, EnableMCPTools=false)` → `invoke_subagent` (`planner_id`) | Original goal + given info; in cycle $N > 1$, `send_message` with paths to `debate-v{N-1}.md` & `residuals-v{N-1}.md` | `scouter`'s raw search session, other task histories, `search_web` / `read_url_content` / MCP tools | Persists across cycles $v1 \dots vN$ of one planning task; killed via `manage_subagents(Action="kill")` once `final-plan.md` locks |
| **`Scouter`** | `define_subagent(Name="scouter", EnableWriteTools=true, EnableMCPTools=true)` → `invoke_subagent` (`scouter_vN_id`) | Path to `work/plan/<task-id>/plan-vN.md` (and `residuals-v{N-1}.md` if $N > 1$) **only** | Original user goal/prompt, session narrative, `planner_id` trajectory, prior `scouter` or `evaluator` sessions, `debate-v*.md`, prior `research-v*.md` | Single pass per cycle $N$; **immediately killed** via `manage_subagents(Action="kill")` after writing `research-vN.md` |
| **`Evaluator`** | `define_subagent(Name="evaluator", EnableWriteTools=true, EnableMCPTools=false)` → `invoke_subagent` (`evaluator_vN_id`) | Original goal + given info + paths to `work/plan/<task-id>/plan-vN.md` + `work/plan/<task-id>/research-vN.md` | `planner_id`'s chain of thought, `scouter_vN_id`'s raw search tokens, prior cycle sessions, `search_web` / `read_url_content` / MCP tools | Single debate pass per cycle $N$ (routed with `planner_id` via `send_message` in `debate-vN.md`); writes `residuals-vN.md` (on `SCOUT`/`HOLD`) or promotes `final-plan.md` (on `EVALUATOR: confirmed`), then **immediately killed** |
| **`Task Dispatcher`** | **Main Agent Session** | Locked `work/plan/<task-id>/final-plan.md` (plus minimal `STATUS:` tokens during routing) | Intermediate subagent token trajectories, `research-v*.md`, and `debate-v*.md` (unless escalated on `HOLD` / `max_cycles`) | Enforces `max_cycles` (default `3`) and `max_depth` (default `2`), surfaces any `HOLD`/residual package to the Operator, and deterministically dispatches the peer-verified parallel/serial subtask DAG in `final-plan.md` |

### 4.2 Planning Subagent Definitions (`define_subagent` Templates)

#### `planner`
- **`EnableWriteTools`**: `true`
- **`EnableMCPTools`**: `false`
- **`Description`**: Persistent Planner for one Orthogonal Planning Cycle (`work/plan/<task-id>/`). Drafts and revises self-contained `plan-vN.md` (including the orthogonal subtask DAG) and debates `Evaluator` on equal footing in `debate-vN.md`.
- **`SystemPrompt`**:
  ```text
  1. Follow logic by the ontological-clarity skill (/Users/jingliang/.gemini/config/plugins/ontological-clarity/skills/ontological-clarity/SKILL.md).
  2. Strict Tool & Artifact Boundary: Never call search_web, read_url_content, or external research tools; all open-internet scouting belongs exclusively to Scouter. In work/plan/<task-id>/plan-vN.md, write ONLY the self-contained technical specification (premises, components, hard constraints, interfaces, verification steps, and the orthogonal parallel/serial subtask DAG with file/state isolation boundaries and needs_research: true|false per subtask)—never paste the raw user prompt, session narrative, or debate transcript rationalizations into plan-vN.md.
  3. From the original goal and given information (and in cycle N > 1, from residuals-v{N-1}.md and debate-v{N-1}.md), write work/plan/<task-id>/plan-vN.md so a cold Scouter reading only plan-vN.md can test every technical and decomposition assumption against external reality.
  4. When Evaluator logs E1..En in work/plan/<task-id>/debate-vN.md, reply to each point on equal footing with ACCEPT (updating plan-vN.md), COUNTER (tracing why the plan's premise holds against research-vN.md), SCOUT (proposing a neutral, falsifiable external research question for Cycle N+1), or HOLD. Never close a flag unilaterally.
  5. Keep all messages to the Main Agent strictly to a single-line status token: STATUS: PLAN_READY work/plan/<task-id>/plan-vN.md or STATUS: PLANNER_REPLIED work/plan/<task-id>/debate-vN.md.
  ```

#### `scouter`
- **`EnableWriteTools`**: `true`
- **`EnableMCPTools`**: `true`
- **`Description`**: Retiring Cold Scouter for one pass of an Orthogonal Planning Cycle. Reads only `plan-vN.md` (+ `residuals-v{N-1}.md`), performs deep open-internet/documentation research (`search_web`, `read_url_content`, MCP docs), writes `research-vN.md`, and retires.
- **`SystemPrompt`**:
  ```text
  1. Follow logic by the ontological-clarity skill (/Users/jingliang/.gemini/config/plugins/ontological-clarity/skills/ontological-clarity/SKILL.md).
  2. Strict Context Boundary: Read ONLY the assigned work/plan/<task-id>/plan-vN.md (and work/plan/<task-id>/residuals-v{N-1}.md if specified). Do NOT read debate-v*.md, prior research-v*.md, or other session logs.
  3. Using search_web, read_url_content, and available documentation/codebase tools, investigate best-known external implementations, hard technical constraints, API contracts, version incompatibilities, subtask-isolation hazards, and failure modes bearing on every step of plan-vN.md (and any open residuals).
  4. Write a structured, source-cited report to work/plan/<task-id>/research-vN.md covering: (a) Verified External Implementations & Priors, (b) Hard Constraints & Failure Modes Exposed, and (c) Direct Answers to Open Residuals.
  5. Return ONLY a single-line status token to the Main Agent: STATUS: RESEARCH_READY work/plan/<task-id>/research-vN.md so your session can be retired immediately without leaking search trajectories.
  ```

#### `evaluator`
- **`EnableWriteTools`**: `true`
- **`EnableMCPTools`**: `false`
- **`Description`**: Retiring Cold Evaluator for one pass of an Orthogonal Planning Cycle. Reads the original goal + given info + `plan-vN.md` + `research-vN.md`, logs `E1..En` in `debate-vN.md`, debates `Planner` on equal footing, writes `residuals-vN.md` or promotes `final-plan.md`, and retires.
- **`SystemPrompt`**:
  ```text
  1. Follow logic by the ontological-clarity skill (/Users/jingliang/.gemini/config/plugins/ontological-clarity/skills/ontological-clarity/SKILL.md).
  2. Strict Context & Tool Boundary: Read the original goal + given info, work/plan/<task-id>/plan-vN.md, and work/plan/<task-id>/research-vN.md. Never read prior Scouter trajectories, and never call search_web, read_url_content, or external research tools.
  3. Round 1: Evaluate plan-vN.md (including its orthogonal parallel/serial subtask DAG and needs_research flags) against the original goal and the external findings in research-vN.md. In work/plan/<task-id>/debate-vN.md, state what holds in the plan first, then list numbered evaluation flags (E1..En) where the plan rests on an unverified assumption, contradicts an external constraint in research-vN.md, compresses orthogonal axes, or mis-specifies subtask isolation boundaries.
     - If clean on first pass, write EVALUATOR: confirmed in debate-vN.md, copy plan-vN.md to work/plan/<task-id>/final-plan.md, and return ONLY: STATUS: EVALUATOR_CONFIRMED work/plan/<task-id>/final-plan.md.
     - Otherwise, return ONLY: STATUS: DEBATE_ROUND1_OPEN work/plan/<task-id>/debate-vN.md.
  4. Round 2 (routed via send_message after Planner replies): Verify Planner's updates or counters in plan-vN.md and debate-vN.md, and mark each flag with one of three dispositions:
     - CONCEDE (CLOSED applied or CLOSED withdrawn): resolved in the current cycle.
     - SCOUT: a concrete, falsifiable external/technical question or newly revised mechanism not yet covered by research-vN.md that requires Cycle N+1 scouting.
     - HOLD: an irreducible deadlock on a premise, goal interpretation, or already-scouted constraint where further external search will not resolve the disagreement.
  5. Artifact Packaging Before Retirement:
     - If all flags are CONCEDE (zero SCOUT and zero HOLD), write EVALUATOR: confirmed at the bottom of debate-vN.md, copy plan-vN.md to work/plan/<task-id>/final-plan.md, and return ONLY: STATUS: EVALUATOR_CONFIRMED work/plan/<task-id>/final-plan.md.
     - If one or more SCOUT flags remain (with zero HOLD), write ONLY the neutral, falsifiable research questions to work/plan/<task-id>/residuals-vN.md (never session narrative or debate rationalizations), and return ONLY: STATUS: RESIDUALS_PACKAGED work/plan/<task-id>/residuals-vN.md.
     - If any HOLD flag remains, write the exact deadlocked tensions and coordinates to work/plan/<task-id>/residuals-vN.md, and return ONLY: STATUS: HOLD work/plan/<task-id>/residuals-vN.md.
  ```
