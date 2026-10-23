# Antigravity Implementation Plan for Event-Driven On-Demand Bot Dispatching (`/wake`, `/sleep`, `/deep-sleep`, and Orthogonal Planning Cycles)

> **Canonical Generic Specification:** [`docs/wave-refinement-plan.md`](../wave-refinement-plan.md)  
> **Companion Essay:** [`On-Demand Contexts Keep Coherence at One Step`](../../content/posts/on-demand-contexts-keep-coherence-at-one-step.md)  
> **Runtime:** Google Antigravity (`define_subagent`, `invoke_subagent`, `send_message`, `manage_subagents`, `search_web`, MCP tools, reactive wakeup, `ask_question`)  
> **Scope:** Applies to `not-a-toe` (Waking, Sleep Consolidation, and Planning) and across **any project in Extended Memory (`/Users/jingliang/Projects/*`)**.  
> **Skills:** On disk (checked 2026-10-23), `~/.gemini/config/plugins/ontological-clarity/skills/` holds links to all eleven project skills (`<name>` → `~/.grok/skills/<name>`) plus `ontological-clarity/SKILL.md` → `/Users/jingliang/Projects/ontological-clarity/SKILL.md`; `~/.gemini/skills/` holds links to nine of them (no `media`, no `recap`), with `ontological-clarity` → `~/.claude/skills/ontological-clarity`. Which of the two directories Antigravity reads skills from is not established here.

---

## 1. Mapping Generic Essay Stages to Antigravity Native Primitives

In Antigravity, each **Bot** (`base model + charter + skills`) is loaded on demand as an ephemeral subagent via `define_subagent` and `invoke_subagent`, and retired by dropping its context via `manage_subagents(Action="kill")`. The **Main Agent** (the active conversation session with the Operator) acts as the deterministic **`Dispatcher` & `Assembler`** (holding triggers, routing handoffs, and running deterministic checks—never acting as a standing project manager or making autonomous decisions).

> **Central Invariant:** **Only tasks are delegated to subagents; decisions always return to the Human Operator.** No deadline rule or watchdog stands in for human judgment on unresolved disagreements (`HOLD`), stalls, crashes, or `sha256` handoff mismatches.
>
> **Deterministic Task Tiers & Pre-Escalation Gate (Set Up Front in `SKILL`s, Audited by `/recap`):**
> - **Tier 1 (Deterministic Execution — Script / Single Executor Only):** Closed-endpoint commands (`interleave-post.py`, `audit-post.py`, `audit-book.py`, `build.mjs`, `project-posts-graph.mjs`, `watch-deploy.sh`, `sha256` checks, killing a confirmed-stuck read-only process) contract the decision space and never spawn `critic` or `scouter`.
> - **Tier 2 (Bounded Subtask — `Maker` ⇄ `Cold Critic` by Default):** Non-trivial subtasks (`drafter` ⇄ `critic`, `translator` ⇄ `stylist`, bounded code subtasks, or handling a non-trivial operational failure) always pair with a cold critic in both directions: (1) preventing mistakes and false-positive escalations, and (2) surfacing overlooked issues or a fresh angle.
> - **Tier 3 (Creative / Open-Ended Task — `Maker/Planner` + `Cold Scouter` + `Cold Critic/Evaluator` by Default):** Open-ended tasks (`/scout` / `/orthogonal-plan`, or `/wake` with external unknowns) run all three roles by default, with `scouter` inferring the best external sources (X, GitHub, official docs, papers) for the task at hand.
> - **Pre-Escalation Verification Gate:** Whenever a Tier 2 or Tier 3 task owner believes a choice requires Operator intervention, it first debates a fresh `critic` on equal footing (and if still unresolved where external prior art applies, runs a cold, retiring `scouter` → reconsiders with `critic`) before interrupting the Operator.
> - **Post-Task & On-Demand `/recap`:** Because no finite `SKILL` boundary catches every surprise, `recap` runs at task conclusion or on Operator call (`/recap`) to audit the trace against `/ontological-clarity` and propose surgical `SKILL`/charter updates, settled per `wave-refinement-plan.md` §4.5.

Because Antigravity controls turn order directly and delivers subagent replies via reactive wakeup (zero polling loops), subagents cannot edit files out of turn or close flags unilaterally:

| Generic Stage / Role | Antigravity Realization | Context & Lifecycle |
| :--- | :--- | :--- |
| **Stage 0 (`/wake` Probe & Settled Verdict)** | **Main Agent Session** (`ask_question` or direct chat) | Probes for the 4 waking materials (Spark, Source, AI/X Thread, Initial Draft). For unauthenticated X/Twitter status URLs (`x.com/.../status/<id>`), fetches directly via `curl -sL "https://cdn.syndication.twimg.com/tweet-result?id=<id>&token=a"` or `curl -sL "https://api.fxtwitter.com/<user>/status/<id>"`; for Grok share URLs (`grok.com/share/<id>` or `x.com/i/grok/share/<id>`), fetches the JSON transcript directly via `curl -sL "https://grok.com/rest/app-chat/share_links/<id>"`. Evaluates against `content/book/index-of-premises.md` & `content/posts/`, and settles `NEW POST (N)` / `REFINEMENT` / `DROP` with a fresh cold-critic subagent, the Operator hearing only a `HOLD` (or invokes the Section 4 Orthogonal Planning Cycle if external research is needed first). |
| **Stage 1 Maker (`Drafter`)** | `define_subagent(Name="drafter", EnableWriteTools=true)` → `invoke_subagent` per post (`drafter_id`) | Fresh conversation context per post. Reads target post (or Operator waking materials, keeping Operator draft/title as primary spine), `work/carry-over.md` (if present), upstream post, neighbors, `index-of-premises.md`, and `/ontological-clarity`. Writes `work/<slug>/en.md` (or `work/<slug>/zh.md` for the 3 Chinese-original posts; see §2) and `work/<slug>/notes.md`. |
| **Stage 1 Cold Critic (`Critic`)** | `define_subagent(Name="critic", EnableWriteTools=true)` → `invoke_subagent` per post (`critic_id`) | Guaranteed cold read: fresh conversation context per post without `drafter_id`'s chain of thought. Reads `work/<slug>/en.md`, `/ontological-clarity`, and `studio/kits/shared/review-method.md`. Writes `P1..Pn` (or `CRITIC: confirmed`) to `work/<slug>/debate-en.md`. |
| **Stage 1 Debate & `sha256` Handoff (`Drafter` ⇄ `Critic`)** | `send_message` routed by Main Agent between `drafter_id` and `critic_id` | Equal-footed debate under `/ontological-clarity` (zero compromise). `drafter_id` updates `work/<slug>/en.md` and logs `ACCEPT`/`COUNTER` in `debate-en.md`; `critic_id` verifies `en.md`, signs off on the **exact final file and its `sha256`** (`CRITIC: confirmed (file: work/<slug>/en.md, sha256: <hash>, date: <YYYY-MM-DD>)`), and `drafter_id` completes the handoff checklist. Any irreducible disagreement (`HOLD`) goes to the Operator with both positions stated briefly. Once `translator_id` recomputes and confirms the `sha256` of `en.md`, `drafter_id` and `critic_id` contexts are dropped (`manage_subagents(Action="kill")`). |
| **Stage 2 Maker (`Translator`)** | `define_subagent(Name="translator", EnableWriteTools=true)` → `invoke_subagent` per post (`translator_id`) | Fresh conversation context per post. **Finished Products Only:** Started **only after** `critic_id` signs off the finished `work/<slug>/en.md` with its `sha256`. First recomputes the `sha256` of `work/<slug>/en.md` and confirms receipt (allowing `drafter_id` and `critic_id` to drop). Translates locked `en.md` to `work/<slug>/zh.md` (if translating exposes a source ambiguity `T1..Tn` in `en.md`, Stage 1 is re-opened in a fresh maker/critic context and re-signed with a new `sha256`). |
| **Stage 2 Cold Critic (`Stylist`)** | `define_subagent(Name="stylist", EnableWriteTools=true)` → `invoke_subagent` per post (`stylist_id`) | Fresh conversation context per post. Cold-reads `work/<slug>/zh.md` first for native Chinese cadence & vocabulary hygiene, then checks 1:1 alignment against locked `work/<slug>/en.md`. Logs `S1..Sn` (or `STYLIST: confirmed`) in `work/<slug>/debate-zh.md`. |
| **Stage 2 Debate & `sha256` Handoff (`Translator` ⇄ `Stylist`)** | `send_message` routed by Main Agent between `translator_id` and `stylist_id` | Equal-footed debate routed via `send_message` until `stylist_id` verifies all fixes in `work/<slug>/zh.md` and signs off on the **exact final file and its `sha256`** (`STYLIST: confirmed (file: work/<slug>/zh.md, sha256: <hash>, date: <YYYY-MM-DD>)`), and `translator_id` completes the handoff checklist (or escalates `HOLD` to the Operator). Once Stage 3 confirms the `sha256` of `zh.md`, both contexts are immediately dropped (`manage_subagents(Action="kill")`). |
| **Cover Art (New Post `N`)** | Built-in `image-generator` subagent or `python3 scripts/generate-cover.py` | Generates ultra-wide 21:9 (`1344×576`) cover art at `assets/covers/<slug>.jpg` and registers in `assets/covers/STYLES.md`. |
| **Post-Run `Recap` (`recap`)** | `define_subagent(Name="recap", EnableWriteTools=true)` → `invoke_subagent` (`recap_id`) | Fresh conversation context loading `/ontological-clarity` and reading the run folder (`en.md`, `zh.md`, `debate-en.md`, `debate-zh.md`, any escalations). Identifies where the run fell short of logical coherence (conflicting charter goals, unstated skill premises, shared blind spots) and writes proposed charter/skill improvements to `work/<slug>/recap.md` (or `work/plan/<task-id>/recap.md`, or `studio/post/<slug>/recap.md`) (settled per `wave-refinement-plan.md` §4.5), then drops immediately. |
| **Stage 3 (`Dispatcher` / `Assembler`)** | **Main Agent Session** (Direct Batch Assembly — Zero Extra Subagent) | Recomputes and confirms `sha256` hashes for `work/<slug>/en.md` and `work/<slug>/zh.md`, kills all node subagents, interleaves `work/<slug>/en.md` + `work/<slug>/zh.md` into `content/posts/<slug>.md` via `python3 scripts/interleave-post.py <slug> [<slug2> ...]`, performs cross-streamline book/anchor sync (grepping both `content/posts/*.md` and active `work/*/{en,zh}.md`), runs `audit-post.py` (`--walkthrough <path>` for waking posts), `audit-book.py`, `build.mjs`, `project-posts-graph.mjs`, stages tracked paths only (`git add content/ data/ assets/`), commits/pushes, watches GitHub Actions deploy (`bash scripts/watch-deploy.sh`), verifies live HTTP 200, appends a new post `N` to `work/wave.md` as a pending `/sleep` origin, and deletes `work/<slug>/` once its `recap` is settled (`wave-refinement-plan.md` §4.5). |

---

## 2. Essay Subagent Registration (`define_subagent`)

At the start of a `/wake`, `/sleep`, or `/deep-sleep` run in Antigravity, the Main Agent registers the essay subagent types once for the conversation. Each `SystemPrompt` is the `## Charter` block of the role's runtime-neutral charter file in [`docs/charters/`](../charters/), and each `Description` is that file's **Role** line; neither is restated here. When registering, map the charters' tool words as follows:
- **the ontological-clarity skill** → `/Users/jingliang/.gemini/config/plugins/ontological-clarity/skills/ontological-clarity/SKILL.md`
- **web search** / **URL fetch** → `search_web` / `read_url_content`
- **reading the image files directly** → `read_file`
- **routed by the Dispatcher** → `send_message`

| `Name` | Charter | `EnableWriteTools` |
| :--- | :--- | :--- |
| `drafter` | [`docs/charters/drafter.md`](../charters/drafter.md) | `true` |
| `critic` | [`docs/charters/critic.md`](../charters/critic.md) | `true` |
| `translator` | [`docs/charters/translator.md`](../charters/translator.md) | `true` |
| `stylist` | [`docs/charters/stylist.md`](../charters/stylist.md) | `true` |
| `recap` | [`docs/charters/recap.md`](../charters/recap.md) | `true` |

---

## 3. Lazy Layer Progression, Operational Safeguards & Adaptive Parallel Streamlines (`W`)

1. **`/sleep` (`N`-Driven Causal Ripple: `Node 0` + `Pre-Wave Sweep` + `Trace DELTA Until NO_DELTA` + `Post-Wave Sweep`):**
   - **Node `0` (`_plan-consolidation` — Stage 1 Only: `Drafter` ⇄ `Cold Critic`, Zero Translation):** Evaluates `N` against `docs/wave-refinement-plan.md`, `docs/adapters/*.md`, `AGENTS.md`, and `/Users/jingliang/.grok/skills/*/SKILL.md` under the two-way **`DELTA` vs. `NO_DELTA` Causal-Necessity Gate**.
   - **Pre-Wave Reverse-Link Sweep (`_reverse-link-sweep` — Stage 1 `Drafter` ⇄ `Cold Critic`):** Scans `content/book/index-of-premises.md`, `content/book/*.md`, and the compact `slug + # Title + *Subtitle*` catalog of all posts outside `links_out(N) ∪ {N}` to propose and cold-verify any unlinked posts `S_pre` that should reverse-link to `N` (or be linked from `N`), merging confirmed candidates into $L_1 = (\text{links\_out}(N) \cup S_{\text{pre}}) \setminus \{N\}$.
   - **Recursive `DELTA`-Only Wave (`L1 → L2 → ...` Stopping at `NO_DELTA`):** Runs across $L_k$ under the two-way **`DELTA` vs. `NO_DELTA` Causal-Necessity Gate**: where `N` (or a parent `DELTA` node) sharpens or completes a target post's own cut (`DELTA` → `CRITIC: confirmed`), it runs Stages 1–3; where the target is already complete on its own axis (`NO_DELTA` → `CRITIC: confirmed_no_delta`), it skips Stages 2–3 and **stops that branch immediately**. Only `DELTA` nodes expand to the next layer along reverse and forward links ($L_k = (\text{links\_in}(\text{DELTA}_{k-1}) \cup \text{links\_out}(\text{DELTA}_{k-1})) \setminus \text{visited}$, excluding mega-hubs with `in_degree > 30` from `links_in` expansion) until a layer produces zero `DELTA`.
   - **Post-Wave Cross-Link Sweep (`_post-wave-sweep` — Stage 1 `Drafter` ⇄ `Cold Critic`):** Verifies across `N` and all `DELTA` posts from the wave against the unvisited corpus catalog that no cross-link updates were missed before `/sleep` finishes.
2. **`/deep-sleep` (Full-Corpus & Site-Wide Consolidation Across All Remaining Posts and Book/Site Contents):**
   - Once `/sleep` finishes `N`'s `DELTA` ripple, `/deep-sleep` consolidates **all remaining unvisited posts (`content/posts/*.md \ visited`, ordered by oldest last-commit timestamp first or by Book Part)** and **all remaining book/site contents (`content/book/README.md`, `content/book/<part>.md`, `content/book/index-of-premises.md`)** in batches of size $B$ (default $B = 12$) across $W$ parallel streamlines under the same two-way `DELTA` vs. `NO_DELTA` Causal-Necessity Gate (checking both missing cross-links to newer posts and `/ontological-clarity` / `AGENTS.md` hygiene).
3. **Customizable & Auto-Derived Concurrency ($W$ Parallel Streamlines):**
   - **Explicit Override:** If the Operator specifies a concurrency target (e.g., `/sleep concurrency=8` or `/deep-sleep 10`), the Main Agent maintains $W$ concurrent node streamlines in `work/<slug-j>/`.
   - **Automatic Derivation from Layer Size:** When no override is passed, the Main Agent derives $W$ automatically from the remaining unchecked node count $R = |L_k|_{\text{rem}}$:
     - $R \le 4 \implies W = R$
     - $5 \le R \le 20 \implies W = 6$
     - $21 \le R \le 60 \implies W = 8$
     - $R > 60 \implies W = 12$
4. **Operational Safeguards:**
   - **Finished Products Only & Two-Way `sha256` Handoff:** `translator_id` is started only after `critic_id` signs off on `work/<slug>/en.md` with its `sha256`. Upon receiver `sha256` confirmation, `drafter_id` and `critic_id` are immediately retired via `manage_subagents(Action="kill", ConversationIds=[...])`. Likewise, `translator_id` and `stylist_id` are immediately retired once Stage 3 confirms the `sha256` of `work/<slug>/zh.md`. Any redo starts from a **fresh context**, never by patching an old context.
   - **Deterministic Interleaving via `scripts/interleave-post.py`:** Always run `python3 scripts/interleave-post.py <slug> [<slug2> ...]` in Stage 3 rather than writing ad-hoc inline split scripts, so blank lines inside ```` ```mermaid ... ``` ```` blocks are stripped and `CN Paragraph -> CN Diagram -> EN Paragraph -> EN Diagram` pairing is enforced before `audit-post.py`.
   - **Whole-File 1:1 `信` Check When Reusing `HEAD` Chinese Paragraphs:** When refining an existing bilingual post, `translator_id` reuses unchanged Chinese paragraphs from `HEAD` as a baseline but audits the full `work/<slug>/zh.md` line-by-line against `work/<slug>/en.md` so pre-existing legacy omissions in adjacent paragraphs are caught in Pass 1 before `stylist_id` runs.
   - **Cross-Streamline H1 & Anchor Sync:** When an H1 changes in Stage 3, update (1) its entry in `content/book/<part>.md`, (2) all `→` links to it in `content/book/index-of-premises.md`, and (3) any incoming link anchors in both `content/posts/*.md` and active in-flight `work/*/{en,zh}.md` (updating `work/<in-flight-slug>/{en,zh}.md` rather than `content/posts/<in-flight-slug>.md` whenever `<in-flight-slug>` has an active streamline).
   - **Commit-Filtered CI Deploy Verification & Tracked-Only `git add`:** Stage only `content/posts/`, `content/book/`, `data/`, and `assets/`—never `work/` or `public/`. After `git push origin main`, run `bash scripts/watch-deploy.sh` (which disables interactive prompts, polls until the workflow run for `HEAD` is registered, and watches that run ID with `--exit-status` and `</dev/null`).

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
| **`Task Dispatcher`** | **Main Agent Session** | Locked `work/plan/<task-id>/final-plan.md` (plus minimal `STATUS:` tokens during routing) | Intermediate subagent token trajectories, `research-v*.md`, and `debate-v*.md` (unless escalated on `HOLD` / `max_cycles`) | Enforces `max_cycles` (default `3`) and `max_depth` (default `2`), surfaces any verified `HOLD`/residual package to the Operator, deterministically dispatches the peer-verified subtask DAG in `final-plan.md` by tier (`tier: deterministic` directly; `tier: subtask` with `Maker` ⇄ `Cold Critic` + Pre-Escalation Gate; `tier: creative` via child `Planner` → `Scouter` → `Evaluator` recursion), and runs `recap` at task conclusion or on Operator `/recap` call |

### 4.2 Planning Subagent Registration (`define_subagent`)

Register each planning role from its charter in [`docs/charters/`](../charters/) with the tool-word mapping of §2:

| `Name` | Charter | `EnableWriteTools` | `EnableMCPTools` |
| :--- | :--- | :--- | :--- |
| `planner` | [`docs/charters/planner.md`](../charters/planner.md) | `true` | `false` |
| `scouter` | [`docs/charters/scouter.md`](../charters/scouter.md) | `true` | `true` |
| `evaluator` | [`docs/charters/evaluator.md`](../charters/evaluator.md) | `true` | `false` |

---

## 5. Antigravity Realization of the Local Media Production Pipeline (`/media <slug>`)

Generic agentic-system-agnostic specification: [`docs/wave-refinement-plan.md` §8](../wave-refinement-plan.md).

### 5.1 Role-to-Primitive Mapping (`studio/post/<slug>/`)

| Generic Role (`wave-refinement-plan.md` §8) | Antigravity Primitive | Workspace Mode | `EnableWriteTools` | `EnableMCPTools` |
| --- | --- | --- | --- | --- |
| **Media Dispatcher** | Main Agent | Root `/Users/jingliang/Projects/not-a-toe` | `true` | `true` |
| **`script-drafter`** | `define_subagent` + `invoke_subagent` | `inherit` (restricted to `studio/post/<slug>/`) | `true` | `false` |
| **`script-critic`** | `define_subagent` + `invoke_subagent` | `inherit` (restricted to `studio/post/<slug>/`) | `true` | `false` |
| **`audio-builder`** | `define_subagent` + `invoke_subagent` | `inherit` (restricted to `studio/post/<slug>/` + `studio/kits/audio/`) | `true` | `false` |
| **`audio-critic`** | `define_subagent` + `invoke_subagent` | `inherit` (restricted to `studio/post/<slug>/`) | `true` | `false` |
| **`infographic-maker`** | `define_subagent` + `invoke_subagent` | `inherit` (restricted to `studio/post/<slug>/` + `studio/kits/infographics/`) | `true` | `false` |
| **`infographic-critic`** | `define_subagent` + `invoke_subagent` | `inherit` (restricted to `studio/post/<slug>/`) | `true` | `false` |
| **`film-maker`** | `define_subagent` + `invoke_subagent` | `inherit` (restricted to `studio/post/<slug>/` + `studio/kits/film/`) | `true` | `false` |
| **`film-critic`** | `define_subagent` + `invoke_subagent` | `inherit` (restricted to `studio/post/<slug>/`) | `true` | `false` |

### 5.2 Media Subagent Registration (`define_subagent` for `/media <slug>`)

Register each of the 8 media roles of §5.1 from its charter in [`docs/charters/`](../charters/) (`script-drafter.md`, `script-critic.md`, `audio-builder.md`, `audio-critic.md`, `infographic-maker.md`, `infographic-critic.md`, `film-maker.md`, `film-critic.md`), with the workspace mode and tool flags of §5.1 and the tool-word mapping of §2. The conventions every media charter shares are stated once in [`docs/charters/README.md`](../charters/README.md).
