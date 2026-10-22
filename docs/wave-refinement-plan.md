# Artificial Brain Waking, Sleep Consolidation & Orthogonal Planning Specification

> **Canonical Location:** [`docs/wave-refinement-plan.md`](../docs/wave-refinement-plan.md) (symlinked at `work/README.md`)  
> **Foundational Ground:** `/ontological-clarity` (`SKILL.md`) — the single house rule (*logical coherence*: derive everything from one premise)  
> **Companion Essay:** [`On-Demand Contexts Keep Coherence at One Step`](../content/posts/on-demand-contexts-keep-coherence-at-one-step.md)  
> **Scope:** Generic, Agentic-System-Agnostic Specification for **Event-Driven On-Demand Bot Dispatching** across **(A) The Living Book (`not-a-toe`) Waking & Sleep Consolidation Pipeline (`/wake` → `/sleep` → `/deep-sleep`)** and **(B) Controlled Open-Internet Injection for Orthogonal Planning Cycles (`Planner` → `Scouter` → `Evaluator` → `Task Dispatcher`)** across `not-a-toe` and any project in Extended Memory. Runtime-specific realizations live in [`docs/adapters/`](../docs/adapters/) (e.g., [`docs/adapters/antigravity.md`](../docs/adapters/antigravity.md)); Claude Code, Grok Bot, or any other agentic system customizes execution from its own standpoint using whatever tools it has available.

---

## 1. Ontological Foundations: Event-Driven On-Demand Bot Dispatching & the Artificial Brain

> **Core Idea:** What are called agents or bots are one base model wearing different masks (`Bot = base model + charter + skills`). Nothing is really created or retired; the model switches context according to the task at hand. "Creating" a bot means loading a charter and its skills into a fresh context; "retiring" it means dropping that context. Because each task loads only the context best suited to it—and discards that context once the finished artifact is handed over—there is no need for long contexts, and standing-agent defects (**long-context drift**, **stale memory**, and **role bleed**) are eliminated at the root.

Designing an agentic authoring, memory-consolidation, or engineering-planning pipeline by asking a standing agent session to draft, research, self-review, translate, and publish within one uninterrupted token trajectory pits the structural mechanics of autoregressive models against the structural mechanics of human cognition. Traced from the single premise of `/ontological-clarity` (*self-distinguishing activity occurs — uncaused, unceasing*), the system is wired around six runtime-agnostic invariants:

### 1.0 Central Principle: Delegate Tasks, Never Decisions (Zero Watchdogs or Deadline Rules)
- **Only tasks can be delegated, never decisions.** Decisions are always made by the living Mind; so-called automated decisions are pre-made decisions being executed. Bots carry out tasks (drafting an essay, critiquing it, translating it, scouting external constraints, recomputing a hash, handing over a finished file). Choosing between two positions the bots could not reconcile, or deciding what to do with a stalled step, a crash, or a hash mismatch, are decisions. Decisions stay with the Human Operator.
- **Disagreements, stalls, crashes, and hash mismatches go to the human (after deterministic pre-escalation verification).** When maker and cold critic cannot reach full agreement (after considering external prior art via a cold scouter where applicable), both positions are stated briefly and the run waits for the human to decide. When a step crashes or stalls, if the trace confirms a deterministic local fix (such as killing a confirmed-stuck read-only TUI process), the agent executes and reports it; if a genuine premise decision remains, it passes through the pre-escalation gate below before interrupting the human (always re-running any redone step in a **fresh context**, never by patching or restarting the old context).
- **No rule or watchdog stands in for judgment.** A deadline rule (*"if no answer by morning, publish anyway"*) or a watchdog (*"if a step is silent for an hour, restart it"*) looks like an automated decision, but is actually a decision made earlier without knowledge of the situation and executed blindly later. The scheme uses neither.
- **One Single House Rule (`Logical Coherence`):** The entire scheme rests on one requirement—**logical coherence**, packaged as `/ontological-clarity` and loaded by every bot. Makers and cold critics debate as equals; neither has the final say, and splitting the difference (compromise) is refused because it installs a second ground. Settling a point by tracing it back to the shared premise executes the pre-made house rule the human chose; any point that cannot be traced to the shared premise requires a new decision and goes to the human.

### 1.0.1 Deterministic Task Tiers, Pre-Escalation Verification Gate & `/recap`
"On-demand" means contexts are spun up only when a defined trigger fires—**not** that a task bot improvises its own process mid-flight. The governing `SKILL`s deterministically specify up front which contexts run for each class of task, how candidate escalations are verified before interrupting the Operator, and how `Recap` closes the loop on uncatchable surprises:

| Task Tier | Decision-Space Geometry (per [`The Density of Judgment`](../content/posts/the-density-of-judgment.md)) | Default On-Demand Contexts (Set Up Front in `SKILL`) | Structural Purpose |
| :--- | :--- | :--- | :--- |
| **Tier 1: Deterministic Execution** | Closed endpoint, fully stated parameters (`interleave-post.py`, `audit-post.py`, `audit-book.py`, `build.mjs`, `project-posts-graph.mjs`, `watch-deploy.sh`, `sha256` checks, killing a confirmed-hung read-only process) | **Script / Single Executor Only** (Zero `Critic`, Zero `Scouter`) | Outcome contracts the decision space to a terminating pass/fail; spinning up a critic or scouter adds cost without signal. |
| **Tier 2: Bounded Subtask** | Defined goal, non-trivial execution (`Drafter` in Stage 1, `Translator` in Stage 2, bounded code/config subtasks, or diagnosing a non-trivial operational failure) | **`Maker` ⇄ `Cold Critic` by Default** (`Cold Scouter` on candidate escalation) | Operates in **both directions**: (1) prevents errors, premise drift, and false-positive escalations, and (2) surfaces overlooked issues or a fresh angle that `Maker`'s trajectory missed. |
| **Tier 3: Creative / Open-Ended Task** | Open-ended design, research, or architecture that expands its own residual decision space (`/scout` / `/orthogonal-plan`, or `/wake` with external unknowns) | **`Maker/Planner` + `Cold Scouter` + `Cold Critic/Evaluator` by Default** | Injects external prior art from inferred high-signal spaces (X, GitHub, official docs, papers) alongside cold ontological evaluation from the start. |

- **Deterministic Pre-Escalation Verification Gate (`Task Owner` ⇄ `Cold Critic` [→ `Cold Scouter` → Reconsider] → `Operator`):**
  Whenever an agent handling a Tier 2 or Tier 3 task believes something requires Operator intervention, it must not interrupt the Operator from inside its single trajectory:
  1. **Step A — Equal-Footed `Cold Critic` Check:** Spin up a fresh `Cold Critic` (with `/ontological-clarity` and the candidate question/blocker, without the task owner's session history) to debate on equal footing: *Is this genuinely an underivable human Decision between unranked goals/premises, or is it a Task already derivable from the house rule and existing repository premises (`Logical Coherence over Rules`)? Does a new angle dissolve the blocker?* If resolved, execute and report—zero interruption.
  2. **Step B — Cold `Scouter` Injection (When Still Unresolved & External Prior Art Applies):** If `Task Owner` and `Cold Critic` still conclude Operator intervention is needed (or remain deadlocked) and the issue touches external tools, architectures, or domain patterns, spin up a cold, retiring `Scouter` that infers the best external inspiration sources for the task at hand (e.g., X threads, GitHub repositories/issues, official docs) and returns a concise findings brief. `Task Owner` and `Cold Critic` reconsider with that brief in hand.
  3. **Step C — Verified Operator Escalation:** Only if `Task Owner` and `Cold Critic` still conclude after reconsideration that a genuine human decision is required do they surface the concise options and premise trace to the Operator.
- **`Recap` (`/recap`) as the Bridge Over Incompleteness & the Mechanism of Front-Loaded Automation:**
  Every mid-run human intervention is the injection of a premise that was not specified at the beginning. Because no finite `SKILL` boundary can anticipate every surprise, bots never bend their process rules mid-run; instead, a cold **`Recap`** pass—run at the conclusion of a task or invoked on demand by the Operator via **`/recap`**—traces the completed run backward under `/ontological-clarity`, isolates the premises that had to be injected along the way to reach the desired outcome, and proposes codifying them at the very beginning of the governing `SKILL`, charter, or script. Once those discovered premises sit at the front as starting conditions, everything in between becomes deterministically derivable (`Tier 3 → Tier 2 → Tier 1`), and the middle segment runs end-to-end without interruption until it reaches the next uncodified edge. That uninterrupted middle is the earlier interventions in compiled form, not their absence, and codifying them is itself a decision made at the current edge (`Recap` proposes, the Operator decides); so `Recap` stays a standing pass rather than a phase that ends: each adopted codification turns the previous outer loop into the present inner loop, and the edge moves outward.

### 1.1 Topology of the Artificial Brain
The operator's repositories and session instruments form a single coherent cognitive architecture:
1. **Artificial Mind (`ontological-clarity`):** [`/Users/jingliang/Projects/ontological-clarity/SKILL.md`](../../ontological-clarity/SKILL.md) (installed at runtime as `/Users/jingliang/.gemini/config/plugins/ontological-clarity/skills/ontological-clarity/SKILL.md`) — the direct public image of the living Mind (the single premise, what follows, method, communication discipline, self-check, and renewal). It holds zero memory warehouse.
2. **Artificial Memory (`not-a-toe` — The Living Book):** [`content/posts/*.md`](../content/posts/) + [`content/book/*.md`](../content/book/) + [`docs/posts.graph.json`](../docs/posts.graph.json) — **the digitized memory of a Mind tracing and experiencing reality as is** (not a static blog log and not a prescriptive "philosophy to live by"). Every essay is a discrete operative cut made in concrete friction; internal cross-links (`[title](../slug/)`) are the synaptic connections of long-term memory.
3. **Experimental Artificial Baby Brain (`ontos`):** [`/Users/jingliang/Projects/ontos`](../../ontos/) — an experimental attempt to run from the Artificial Mind + model loop with minimal or no pre-populated Artificial Memory.
4. **Working Memory (`/bridge`, `/resume-bridge`, `/retire`):** Model- and agent-agnostic plain Markdown files at `<project>/memory/bridges/<id>.md` (with `<project>/memory/bridges/.last_session` tracking session continuity). Working memory carries only the moving `Next` edge and the preceding traces it still depends on across context clears; once a task finishes or consolidates into long-term memory, `/retire` deletes the bridge—because a brain does not keep a permanent log of its own sleep.
5. **Extended Memory (`/Users/jingliang/Projects/*`):** Every project repository on disk (`not-a-toe`, `ontos`, `brief`, `orbit`, etc.) is an externalized artifact of Extended Memory. Both the peer-debate pattern and the orthogonal research-planning cycle (Section 6) apply across any project in Extended Memory.

### 1.2 Trajectory vs. Identity (Generator ⇄ Cold Peer)
- **The Agent's Bind (Trajectory Gravity Well):** An LLM agent is a finite projection engine. Every token it generates becomes the conditioning history (`Trace`) for every token that follows. Left inside its own drafting or research session, its first draft becomes its retained `Image`: it cannot step outside the token trajectory it just predicted, so self-review merely rationalizes and wraps its own blind spots.
- **The Agent's Strength (Zero Ego):** Unlike a human whose reasoning history fuses with identity, an agent has zero personal attachment to having been "right" one turn ago. When a valid counterpoint or external constraint enters its context from *outside* its self-reinforcing loop, it performs a clean Bayesian update.
- **The Architectural Consequence:** Every generative stage (`Drafter` in Stage 1, `Translator` in Stage 2, `Planner` in Section 6) is paired with an equal-footed **Cold Peer** (`Critic` in Stage 1, `Stylist` in Stage 2, `Evaluator` armed with a fresh `Scouter` report in Section 6) running in a **fresh, isolated context** that receives the **task context** (the artifact, linked posts or external report, and skill) without the **session context** (the generator's internal chain of thought). No third "Judge Agent" is inserted between them: every flag is either resolved by **mutual agreement (`ACCEPT` / `CONCEDE`)** under logical coherence, sent for another bounded external scouting pass (`SCOUT` in Section 6), or escalated on irreducible deadlock (`HOLD`) to the **Human Operator**.

### 1.3 Mitosis of Projection Along Orthogonal Axes (`Capacity`)
Cramming $2^N$ independent requirements—context probing, open-internet scouting, ontological derivation, primary-language prose, causal translation (`信`), native target-language cadence (`达/雅`), and book/index assembly—into one prompt or simultaneous edit exceeds a center's finite `Capacity`. Independent axes compress onto one register, causing cadence edits to invert causal steps, translation choices to soften the cut, or raw search results to pollute the planning trajectory.
- **The Architectural Consequence:** The architecture splits projections along clean, orthogonal boundaries:
  - **Orthogonal Planning Cycle (Section 6 — Any Project / Pre-Implementation Research):** `Planner` $\rightarrow$ `Scouter` (fresh, retires) $\rightarrow$ `Evaluator` (fresh, debates `Planner`, writes `residuals-vN.md` or promotes `final-plan.md`, retires) $\rightarrow$ `Task Dispatcher`.
  - **Stage 0 (Waking Probe & Lattice Recommendation — `/wake` / `/draft` only):** Gather spark, source, AI/X thread & initial draft $\rightarrow$ evaluate against the Living Book $\rightarrow$ recommend `New Post` / `Refinement` / `Drop` (optionally invoking the Section 6 Planning Cycle when external reference architectures are needed before drafting).
  - **Stage 1 (Primary-Language Cut & Cold Ontological Review):** `Drafter` $\leftrightarrow$ `Critic` (including relative `[title](../slug/)` links directly in the prose).
  - **Stage 2 (Logical Translation [`信`] & Cold Cadence Review [`达/雅`]):** `Translator` $\leftrightarrow$ `Stylist`.
  - **Stage 3 (Deterministic Assembly, Audits, Publish & Wave Dispatch):** `Dispatcher` / `Assembler`.

### 1.4 Dispatcher vs. Orchestrator (`Observer` + `Power`)
- **Agentic System as Dispatcher (Finite Projection):** Routing tasks across stages, interleaving paired paragraphs, running deterministic audits, dispatching the peer-verified parallel/serial subtask DAG locked inside `final-plan.md`, and advancing the wave cursor are well-defined structural operations executed by the runtime's `Dispatcher` / `Assembler`. All generative architectural decisions—including how a plan decomposes into orthogonal parallel/serial subtasks and which subtasks require child research cycles—are authored by `Planner` inside `plan-vN.md` and cold-verified by `Scouter` and `Evaluator` before `final-plan.md` locks, never invented unreviewed by `Task Dispatcher`.
- **The Human as Ultimate Orchestrator (Unprojected Intent):** Agents remain finite projection engines. The wiring localizes non-convergence; it does not classify "premise-level residual" versus "implementation-detail residual," nor does it dissolve contradictions in living intent. Only the human holds dynamic, limit-resolution sensing and can step backward out of a broken frame when two premises collide. Whenever a peer debate reaches an irreducible `HOLD` (or a planning loop hits `max_cycles` or `max_depth`), the local streamline pauses and surfaces the exact coordinate of friction to the Operator. Making that call forces a higher-order synthesis that dissolves the contradiction, revises the premises, or accepts the bound rather than overriding one peer by fiat.

### 1.5 Wake vs. Sleep: Lazy Layer-by-Layer Consolidation of Artificial Memory
- **Waking Edge (`/wake`, alias `/draft` — New Blog Post `N` or Refinement):** A new essay `N` is the most recent digital edge left behind by the living Mind. Invoking `/wake [seed]` (or `/draft [seed]`) cleanly pauses any active sleep consolidation after its current in-flight node, probes for the four waking materials (**1. new intuition/spark**, **2. inspiring source**, **3. thinking process [AI discussion or X comment thread]**, and **4. initial draft**—whether all four or a simple initial idea), evaluates them against the Living Book, and recommends **New Post (`N`)**, **Refinement of existing post(s)**, or **Drop (repetitive)**. On the Operator's go-ahead, it runs Stages 1–3 to publish and (for a new post `N`) initializes a fresh consolidation cycle (`visited = {N}`).
- **Sleep Consolidation (`/sleep` and `/deep-sleep`):** Once `N` is published, external input is turned off and the Artificial Brain enters sleep consolidation under a two-way **`DELTA` vs. `NO_DELTA` Causal-Necessity Gate** (preventing forced backlink stuffing in essays and decorative rule bloat in plans), split cleanly along two orthogonal causal roles:
  - **`/sleep` (Shallow Sleep — `N`-Driven Causal Ripple: `Node 0` + `Pre-Wave Reverse-Link Sweep` + `Recursive DELTA Wave Until NO_DELTA` + `Post-Wave Sweep`):**
    1. **Node `0` (`_plan-consolidation` — Stage 1 Only: `Drafter` ⇄ `Cold Critic`, Zero Translation):** Evaluates whether `N` introduces or sharpens an operational/procedural premise for `docs/wave-refinement-plan.md`, `docs/adapters/antigravity.md`, `AGENTS.md`, or `SKILL`s (`DELTA` in `work/_plan-consolidation/draft.md`, or `NO_DELTA` with a 1-paragraph causal proof in `work/_plan-consolidation/notes.md`), cold-verified by `Critic` in `work/_plan-consolidation/debate-en.md`.
    2. **Pre-Wave Reverse-Link Sweep (`_reverse-link-sweep` — Stage 1 `Drafter` ⇄ `Cold Critic`):** Scans `content/book/index-of-premises.md`, `content/book/*.md`, and the compact `slug + # Title + *Subtitle*` catalog of all posts outside `links_out(N) ∪ {N}` to catch any unlinked existing posts whose cut is sharpened or completed by `N` (needing `P -> N` or `N -> P`). Confirmed sweep candidates merge with `links_out(N) \setminus \{N\}` to form `L1`.
    3. **Recursive `DELTA`-Only Wave (`L1 → L2 → ...` Stopping at `NO_DELTA`):** Consolidates `L1` under `Drafter` ⇄ `Cold Critic`. Any node confirmed `NO_DELTA` (`CRITIC: confirmed_no_delta`) did not move and **terminates its branch immediately** (skipping Stages 2–3 and expanding no further). Only nodes that actually change (`DELTA` → Stages 1–3) propagate to the next layer along reverse and forward links ($L_k = (\text{links\_in}(\text{DELTA}_{k-1}) \cup \text{links\_out}(\text{DELTA}_{k-1})) \setminus \text{visited}$, excluding foundational mega-hubs with `in_degree > 30` from `links_in` expansion), repeating until a layer produces zero `DELTA` ($\text{DELTA}_k = \emptyset$).
    4. **Post-Wave Cross-Link Sweep (`_post-wave-sweep` — Stage 1 `Drafter` ⇄ `Cold Critic`):** Verifies across `N` and all `DELTA` posts from the wave against the unvisited corpus catalog that no cross-link updates were missed before `/sleep` closes.
  - **`/deep-sleep` (Deep Sleep — Full-Corpus & Site-Wide Consolidation Across All Remaining Posts and Book/Site Contents):** Because `/sleep` stops at `NO_DELTA` to bound `N`'s ripple, older posts outside `N`'s immediate `DELTA` chain and non-post site contents are consolidated by `/deep-sleep`:
    1. **All Remaining Unvisited Posts (`content/posts/*.md \setminus visited`):** Ordered deterministically by staleness (oldest git commit timestamp first, or by Book Part) and processed in batches of $B$ across $W$ parallel streamlines under the same two-way `DELTA` vs. `NO_DELTA` Causal-Necessity Gate (`Drafter` ⇄ `Cold Critic` → `Translator` ⇄ `Stylist` → `Dispatcher/Assembler`), weaving missing cross-links to newer posts and repairing any prose/hygiene drift.
    2. **All Remaining Site & Book Contents (`content/book/*.md`):** Consolidates the Book Preface (`content/book/README.md`), the 14 Part Prefaces (`content/book/<part>.md`), and `content/book/index-of-premises.md` entry formulations under `Drafter` ⇄ `Cold Critic` (`→ Translator ⇄ Stylist` when prose changes) until the entire Living Book is consolidated or a new `/wake` initiates the next cycle.
- **Hubs Recur by Design:** High-degree hubs (`individual-choices-as-the-only-causal-levers`, `openness-is-consistency`, `intelligence-belongs-only-to-the-mind`) appear in most cycles because hubs are where stabilized traces broadcast furthest across the lattice. Within a single cycle (`visited`), each post is visited at most once; across cycles, as past lag is paid off, each pass becomes naturally lighter.

---

## 2. Workspace Separation: Working Directories (`work/`) vs. Canonical Source

Placing in-flight single-language drafts or intermediate research/planning artifacts inside canonical source directories collapses two orthogonal axes—*in-flight working state* and *the repository's canonical build surface*. The generic architecture separates **in-flight plain-Markdown workspaces (`work/`, excluded via `.git/info/exclude` or `.gitignore`)** from **canonical published source** using a simple, role-agnostic layout with explicit single-artifact ownership:

| Path | Writer / Owner | Purpose |
| :--- | :--- | :--- |
| `work/<slug>/en.md` | `Drafter` (signed off by `Critic`) | Pure primary-language (EN, or `zh.md` for Chinese-originals) Markdown draft/refinement, including Mermaid diagrams and relative `[title](../other-slug/)` links. Passed to Stage 2 **only** as a finished product signed off with its `sha256`. |
| `work/<slug>/notes.md` | `Drafter` | Context trace: waking materials (spark, source, AI/X thread, initial draft), linked posts read, Index of Premises entries checked, and refinement rationale. |
| `work/<slug>/debate-en.md` | `Critic` $\leftrightarrow$ `Drafter` | Primary-language debate log (`P1..Pn` and any post-lock `T1..Tn` flags routed by `Dispatcher`). Ends with `CRITIC: confirmed (sha256: <hash>, date: <YYYY-MM-DD>)` + completed handoff checklist when all flags are closed. |
| `work/<slug>/zh.md` | `Translator` (signed off by `Stylist`) | Pure secondary-language (ZH, or `en.md` for Chinese-originals) Markdown translation of the `Critic`-signed primary text. |
| `work/<slug>/debate-zh.md` | `Stylist` $\leftrightarrow$ `Translator` | Secondary-language debate log (`S1..Sn` cadence and 1:1 alignment flags). Ends with `STYLIST: confirmed (sha256: <hash>, date: <YYYY-MM-DD>)` + completed handoff checklist when all flags are closed. |
| `work/<slug>/recap.md` | `Recap` (Cold Post-Run Reviewer) | Post-run review against `/ontological-clarity`: identifies where the run fell short of logical coherence (conflicting charter goals, unstated skill premises, shared blind spots) and **proposes** charter/skill edits for the Operator to decide. |
| `work/carry-over.md` | Final pair of a run | Late information learned too late to act on in the current run; read by the next run's first bot and cleared once acted on (see `work/todo.md` for cross-node wave notes). |
| `work/wave.md` | `Dispatcher` | Active N-layer sleep consolidation checklist (`N`, `L1`, `L2`, ..., `Lk`, `visited`, parked `HOLD`s, and commit SHAs). |
| `work/plan/<task-id>/plan-vN.md` | `Planner` | Self-contained versioned technical specification and orthogonal subtask DAG (see Section 6). |
| `work/plan/<task-id>/research-vN.md` | `Scouter` | Structured external research report for cycle $N$; `Scouter` retires immediately after writing. |
| `work/plan/<task-id>/debate-vN.md` | `Evaluator` $\leftrightarrow$ `Planner` | Equal-footed planning debate log (`E1..En`); ends with `EVALUATOR: confirmed (sha256: <hash>, date: <YYYY-MM-DD>)`, `SCOUT`, or `HOLD`. |
| `work/plan/<task-id>/residuals-vN.md` | `Evaluator` | Neutral, falsifiable external research questions written by `Evaluator` at the end of Round 2 when `SCOUT` items remain for Cycle $N+1$. |
| `work/plan/<task-id>/final-plan.md` | `Evaluator` (or Operator on `HOLD`) | Promoted from `plan-vN.md` by `Evaluator` upon `EVALUATOR: confirmed` (signed off by `sha256`); the **only** artifact read by `Task Dispatcher`. |
| `work/todo.md` | Any role | Out-of-scope cross-node or cross-subtask observations saved for future nodes so active contexts stay clean. |
| `memory/bridges/<id>.md` | `/bridge`, `/resume-bridge`, `/retire` | Ephemeral Working Memory across session clears (`Next` + `Traces` with priors named; deleted upon `/retire`). |
| `content/posts/<slug>.md` | `Dispatcher` / `Assembler` | Canonical alternating bilingual post on the live site. Untouched during Stages 1–2 so `git status` stays clean until Stage 3 assembly. |

> **Why Transient Workspaces Are Deleted, Not Archived (Checkpoints vs. Weight-Update History):**
> Just as neural network training saves current checkpoints rather than hoarding every historical gradient step, persistence in `/ontological-clarity` is re-tracing in the present configuration—nothing is stored outside the current rendering. Once a post refinement (`work/<slug>/`) or planning task (`work/plan/<task-id>/`) is absorbed into canonical source (`content/posts/*.md`, `content/book/*.md`, or project code, replicated to GitHub `origin/main`), its intermediate drafts, debates, and superseded `wave.md` files are **deleted (`rm -rf`)**, never archived into `work/archive/` or `.bak` folders out of mere possibility. Keeping dead intermediate history creates epistemic rabbit holes for future searches instead of sharpening the living present.

---

## 3. The 4-Stage Essay Pipeline & Role Specifications

```mermaid
flowchart TD
    subgraph S_Wake["Stage 0 (/wake or /draft Only): Probe Waking Materials & Recommend"]
        W0["Operator invokes /wake or /draft<br/>Probe for: 1. Spark/Intuition, 2. Source, 3. AI/X Thread, 4. Initial Draft"] --> W1{"Evaluate against Index of Premises & existing posts<br/>Recommend: NEW POST (N) vs. REFINEMENT vs. DROP"}
        W1 -->|"DROP (repetitive)"| W_Drop["Cite existing post(s) & stop cleanly"]
        W1 -->|"Needs external research"| W_Plan["Optional: Run Orthogonal Planning Cycle (Section 6)<br/>Planner → Scouter → Evaluator"]
        W_Plan --> W2
        W1 -->|"Operator Go-Ahead: NEW POST (N) or REFINEMENT"| W2["Lock <slug>, Book Part & initial spine (keep Operator draft/title)"]
    end

    subgraph S_EN["Stage 1: Primary-Language Cut & Cold Ontological Review (work/slug/en.md & debate-en.md)"]
        W2 --> B1
        B1["Drafter (Maker Context)<br/>Writes/refines EN in work/slug/en.md (with relative cross-links)<br/>Traces in context from /ontological-clarity + Index + neighbors"] --> B2["Critic (Fresh Cold Context)<br/>No Drafter chain-of-thought<br/>Traces en.md from irreducible prior & review-method.md"]
        B2 -->|"Raises P1..Pn"| DebateEN["Drafter ⇄ Critic Equal-Footed Debate<br/>ACCEPT / COUNTER / CONCEDE / HOLD (Zero Compromise)"]
        DebateEN -->|"All P-flags CLOSED"| LockEN["Critic signs off exact en.md + sha256<br/>Drafter completes Handoff Checklist"]
        DebateEN -->|"Irreducible HOLD"| Op_EN["Park Node in work/wave.md<br/>Escalate both positions briefly to Operator"]
        Op_EN -->|"Operator Decides"| LockEN
        B2 -->|"Clean on first pass"| LockEN
    end

    subgraph S_ZH["Stage 2: Logical Translation (信) & Cold Cadence Review (达/雅) (work/slug/zh.md & debate-zh.md)"]
        LockEN -->|"Finished Product Only (sha256 confirmed by Translator)"| B3["Translator (Maker Context — 信)<br/>Recomputes & confirms en.md sha256 (Stage 1 contexts drop)<br/>Translates locked en.md → work/slug/zh.md"]
        B3 -.->|"Reports T1..Tn if EN has source ambiguity"| DebateEN
        B3 --> B4["Stylist (Fresh Cold Context — 达/雅)<br/>Cold-reads zh.md first, then checks 1:1 against en.md<br/>Raises S1..Sn for cadence, translationese & 信 alignment"]
        B4 --> DebateZH["Translator ⇄ Stylist Equal-Footed Debate<br/>ACCEPT / COUNTER / CONCEDE / HOLD (Zero Compromise)"]
        DebateZH -->|"All S-flags CLOSED"| LockZH["Stylist signs off exact zh.md + sha256<br/>Translator completes Handoff Checklist"]
        DebateZH -->|"Irreducible HOLD"| Op_ZH["Park Node & Escalate both positions to Operator"]
        Op_ZH --> LockZH
        B4 -->|"Clean on first pass"| LockZH
    end

    subgraph S_Final["Stage 3: Deterministic Assembly, Audits, Publish, Recap & Sleep Dispatch"]
        LockZH --> B5["Dispatcher / Assembler & Post-Run Recap<br/>1. Recompute & confirm en.md + zh.md sha256 (Stage 2 contexts drop)<br/>2. Interleave locked en.md + zh.md into content/posts/slug.md<br/>3. Sync Book Part, Index of Premises, title-translations.json & incoming anchors<br/>4. Run audit-post.py, audit-book.py, build.mjs, project-posts-graph.mjs<br/>5. Run cold Recap (proposes charter/skill improvements to Operator)<br/>6. Commit (tracked paths only), push, verify live HTTP 200, delete work/slug/"]
        B5 -->|"After New Post N"| Sleep1["/sleep: Shallow Sleep<br/>Consolidate L1 = links_out(N) - {N}"]
        Sleep1 -->|"After L1 completes"| SleepK["/deep-sleep: Deep Sleep<br/>Re-project graph & compute Lk = links_out(L_{k-1}) - visited<br/>Repeats L2 → L3 → ... → Lk until next /wake"]
        Sleep1 -.->|"Each node in L1"| B1
        SleepK -.->|"Each node in Lk"| B1
    end

    style S_Wake fill:#161b22,stroke:#3fb950,stroke-width:1.5px,color:#3fb950
    style S_EN fill:#161b22,stroke:#58a6ff,stroke-width:1.5px,color:#58a6ff
    style S_ZH fill:#161b22,stroke:#a371f7,stroke-width:1.5px,color:#a371f7
    style S_Final fill:#161b22,stroke:#3fb950,stroke-width:1.5px,color:#3fb950
    style W0 fill:#0d1117,stroke:#3fb950,stroke-width:1px,color:#f0f6fc
    style W1 fill:#0d1117,stroke:#d29922,stroke-width:1px,color:#f0f6fc
    style W_Drop fill:#0d1117,stroke:#f85149,stroke-width:1px,color:#f0f6fc
    style W_Plan fill:#0d1117,stroke:#58a6ff,stroke-width:1px,color:#f0f6fc
    style W2 fill:#0d1117,stroke:#3fb950,stroke-width:1px,color:#f0f6fc
    style B1 fill:#0d1117,stroke:#58a6ff,stroke-width:1px,color:#f0f6fc
    style B2 fill:#0d1117,stroke:#a371f7,stroke-width:1px,color:#f0f6fc
    style DebateEN fill:#0d1117,stroke:#d29922,stroke-width:1px,color:#f0f6fc
    style LockEN fill:#0d1117,stroke:#3fb950,stroke-width:1px,color:#f0f6fc
    style Op_EN fill:#0d1117,stroke:#f85149,stroke-width:1px,color:#f0f6fc
    style B3 fill:#0d1117,stroke:#58a6ff,stroke-width:1px,color:#f0f6fc
    style B4 fill:#0d1117,stroke:#a371f7,stroke-width:1px,color:#f0f6fc
    style DebateZH fill:#0d1117,stroke:#d29922,stroke-width:1px,color:#f0f6fc
    style LockZH fill:#0d1117,stroke:#3fb950,stroke-width:1px,color:#f0f6fc
    style Op_ZH fill:#0d1117,stroke:#f85149,stroke-width:1px,color:#f0f6fc
    style B5 fill:#0d1117,stroke:#3fb950,stroke-width:1px,color:#f0f6fc
    style Sleep1 fill:#0d1117,stroke:#58a6ff,stroke-width:1px,color:#f0f6fc
    style SleepK fill:#0d1117,stroke:#a371f7,stroke-width:1px,color:#f0f6fc
```

### Role Specifications & Operational Learnings

> **Foundational Rule — Causal Reasoning over Raw Mechanical Rejection (`Logical Coherence over Rules`):**
> Logical coherence (each case traced back to the irreducible prior) comes before any rule, since logic is scale-invariant and rules are context-dependent. Across all stages (`Drafter`, `Critic`, `Translator`, `Stylist`, and `Dispatcher`), authoring conventions and audit advisories—such as the 17-word vocabulary-hygiene list in `AGENTS.md`, prose-over-lists, subtitle length guidelines, and book ordering—are **recommendations and diagnostic signals, not mechanical stopping rules**. Never perform raw mechanical rejection of a word or structure without reasoning causally about its actual context: when a listed word names the held belief or object under dissection, or when a list's structure carries meaning prose would blur, keeping it is the logically coherent choice.

#### Stage 1 Generator — `Drafter` (Primary-Language Drafter / Refiner)
- **Context Loaded:** `/ontological-clarity`, [`AGENTS.md`](../AGENTS.md) (*Write in context, traced to premises*), the target post `content/posts/<slug>.md` (or the implementation plans `docs/wave-refinement-plan.md`, `docs/adapters/antigravity.md`, `AGENTS.md`, and `SKILL`s for Node `0` `_plan-consolidation`, or the Operator's waking materials—spark, source, AI/X discussion thread, and initial draft—for `/wake`), the upstream post that triggered this wave step, the target post's linked neighbors, its [`content/book/index-of-premises.md`](../content/book/index-of-premises.md) entries, and its book chapter.
- **Execution:** Writes or refines the pure English essay in `work/<slug>/en.md` (or pure Chinese in `work/<slug>/zh.md` for the 3 Chinese-original posts; see §5.3), including relative `[title](../other-slug/)` links directly in the prose, and records its context trace (plus candidate 1-hop reverse-pointer notes for a new post `N`) in `work/<slug>/notes.md`.
  - **Operator Draft Preservation (`/wake`):** When the Operator supplies an initial draft, `Drafter` preserves the Operator's title, structural spine, and argument order as the ground of the cut—applying surgical precision (weaving relative links, adding vertical dark-theme Mermaid diagrams, tightening ungrounded phrasing) rather than rewriting into generic house prose.
  - **Causal-Necessity Gate (`DELTA` vs. `NO_DELTA`) for Both Posts (`L1`/`Lk`) and Implementation Plans (`Node 0` in `/sleep`):**
    - Unconditional backlink injection in essays or unconditional rule additions in implementation plans force artificial tail-clauses and decorative rule bloat when an upstream citation is asymmetric (i.e., when `N` draws its premise from an already-complete hub without altering that hub's own cut, or when `N` dissects a domain premise that does not change procedural invariants).
    - **`DELTA` (Refinement Needed):** If the upstream post `N` exposes an unstated premise, compressed axis, boundary exception, or downstream distinction that **genuinely sharpens or completes the target's own cut** (or if the target post has an existing hygiene/bilingual/structural drift under current invariants), `Drafter` writes the surgical refinement in `work/<slug>/en.md` (or `work/_plan-consolidation/draft.md` for Node `0`) and records its causal trace in `work/<slug>/notes.md`.
    - **`NO_DELTA` (Target Already Complete & Self-Contained):** If `N` merely cites the target post as an already-complete upstream premise (or, for Node `0` `_plan-consolidation`, if `N`'s cut is already fully satisfied by existing procedural invariants) and the target passes all current repository invariants without needing `N` to complete its own cut, `Drafter` records `NO_DELTA` with a 1-paragraph causal justification in `work/<slug>/notes.md` (without creating an artificial edit in `en.md` or `draft.md`) and hands straight to `Critic` for cold two-way verification.
- **Debate Rule:** Replies `ACCEPT` (with exact replacement text updated in `work/<slug>/en.md` and premise trace) or `COUNTER` (with premise trace showing why the current phrasing or `NO_DELTA` verdict is causally coherent in context) to each `P`-flag from `Critic` in `work/<slug>/debate-en.md`. Never closes a flag unilaterally.

#### Stage 1 Cold Peer — `Critic` (Cold Ontological Reviewer)
- **Context Loaded:** Fresh, isolated context with `/ontological-clarity`, [`studio/review-method.md`](../studio/review-method.md), and `work/<slug>/en.md` (or the existing `content/posts/<slug>.md` + `work/<slug>/notes.md` when `Drafter` declares `NO_DELTA`, or `work/_plan-consolidation/` + target plan/skill files for Node `0`), plus linked posts as needed to verify claims and relative links. Never reads `Drafter`'s session history.
- **Execution (Two-Way `DELTA` / `NO_DELTA` Verification):**
  - **When `Drafter` proposes `DELTA` (`en.md` or `draft.md`):** States what the draft's cut is and what holds first in `work/<slug>/debate-en.md`, then lists numbered points (`P1..Pn`) where independent axes compress, where an observer judges unobservable interiors, where a totalizing word ("only", "never", "all") over-closes a bounded mechanism, where a relative link does not fit its sentence, where two sections disagree, **or where a proposed reverse link / plan rule is forced link-stuffing or decorative bloat because the target's cut is already complete without `N`**.
  - **When `Drafter` declares `NO_DELTA`:** Cold-checks the target post (or implementation plans) against `N` and current repository invariants to verify the opposite direction—whether omitting `N` leaves an actual boundary gap or unstated premise in the target, or whether the target has any unfixed hygiene/bilingual drift. If a genuine refinement is needed, raises `P1..Pn` requiring `Drafter` to produce `en.md` / `draft.md`.
- **Gate & Cryptographic `sha256` Sign-Off:** In Round 2+, marks each point `CONCEDE` (`CLOSED applied` or `CLOSED withdrawn`) or `HOLD` (full agreement only; zero split-the-difference compromise). Any point remaining on `HOLD` after Round 2 is escalated to the Operator with both positions stated briefly.
  - **If `DELTA` is confirmed:** Once all points are closed and verified verbatim in `work/<slug>/en.md` (or `work/_plan-consolidation/draft.md`), `Critic` signs off on the **exact final file and its `sha256` hash** (`CRITIC: confirmed (file: work/<slug>/en.md, sha256: <hash>, date: <YYYY-MM-DD>)`) in `work/<slug>/debate-en.md`, and `Drafter` completes the handoff checklist.
  - **If `NO_DELTA` is confirmed:** `Critic` signs off on the unchanged canonical file (or `notes.md` for Node `0`) with `CRITIC: confirmed_no_delta (file: content/posts/<slug>.md, sha256: <hash>, date: <YYYY-MM-DD>)` in `work/<slug>/debate-en.md`. Confirmed `NO_DELTA` nodes skip Stage 2 (`Translator` ⇄ `Stylist`) and Stage 3 (`interleave-post.py`) completely, prune `work/<slug>/`, and check off `- [x] <slug> (NO_DELTA)` in `work/wave.md`.

#### Stage 2 Generator — `Translator` (`信` — Logical & Causal Fidelity)
- **Context Loaded:** Critic-signed `work/<slug>/en.md`, `/ontological-clarity`, target posts' H1 headings in `content/posts/<target-slug>.md`, [`data/title-translations.json`](../data/title-translations.json), and `git show HEAD:content/posts/<slug>.md` (to reuse or refine unchanged Chinese paragraphs from already-bilingual posts).
- **Finished Products Only & Two-Way `sha256` Handoff Confirmation:**
  - **Finished Products Only:** What passes from Stage 1 to Stage 2 is strictly the final `work/<slug>/en.md` that `Critic` has signed off with its `sha256`—never an unapproved draft plus a list of pending fixes.
  - **Receiver Confirmation Before Stage 1 Contexts Drop:** Upon starting in a fresh context, `Translator` recomputes the `sha256` of `work/<slug>/en.md` and confirms receipt directly with **both** `Drafter` and `Critic` (via the routing harness). If the hash mismatches or confirmation is missing, the handoff is void and escalates to the Operator. Once confirmed, `Drafter` and `Critic` contexts are dropped (`kill`)—unless `Translator` surfaces a source ambiguity (`T1..Tn`) that requires re-opening Stage 1 in a fresh maker/critic pass and re-signing `en.md` with a new `sha256`.
- **Execution & Whole-File 1:1 Fidelity Check:** Writes pure Chinese Markdown (title, single-line italic subtitle, lead, `## 一、 <中文标题>`, body paragraphs, Chinese link anchors, and pure-Chinese Mermaid diagrams) to `work/<slug>/zh.md`. Since all posts in the corpus are bilingual, every internal link `[...](../<target-slug>/)` takes its canonical Chinese anchor directly from the `# <ZH> / <EN>` H1 of `content/posts/<target-slug>.md` (with `data/title-translations.json` kept only as a fallback if a new monolingual stub is ever introduced). When refining an existing bilingual post, `Translator` reuses unchanged Chinese paragraphs from `HEAD` as its baseline **but verifies 1:1 `信` fidelity and `AGENTS.md` vocabulary hygiene across the entire `work/<slug>/zh.md` against locked `work/<slug>/en.md`** before handing off to `Stylist`, so pre-existing legacy omissions (e.g., dropped nouns or parenthetical inversions in adjacent sections) are repaired in the first pass rather than triggering an avoidable Round 2. Evaluates vocabulary-hygiene hits causally in context (barring them where the prose evaluates or describes with them, allowing them where they name the object/belief under dissection).
- **Debate Rule:** Answers `Stylist` flags `S1..Sn` in `work/<slug>/debate-zh.md` with `ACCEPT` or `COUNTER` (with a causal reason grounded in `信` or `达`). **Never closes a flag unilaterally; there is no unilateral "`信` wins" override.**

#### Stage 2 Cold Peer — `Stylist` (`达/雅` — Native Cadence & 1:1 Alignment Reviewer)
- **Context Loaded:** Fresh, isolated context. Performs a **cold read of `work/<slug>/zh.md` first** (to catch unnatural cadence, stacked pre-nominal `的` clauses, ungrammatical focus frames, garden-path phrases, and vocabulary-hygiene hits where they carry the essay's own evaluation rather than naming the object), and **then** reads it line-by-line against locked `work/<slug>/en.md` to verify 1:1 causal, actor, and emphasis alignment.
- **Gate & Cryptographic `sha256` Sign-Off:** Raises `S1..Sn` in `work/<slug>/debate-zh.md`. In Round 2+, marks each point `CONCEDE` or `HOLD` (including holding when a `Translator` counter-proposal alters `信`, e.g., turning a constitutive relation into a causal `因为`). Once all `S`-flags are settled and verified verbatim in `work/<slug>/zh.md` with matching block counts and link counts, `Stylist` signs off on the **exact final file and its `sha256` hash** (`STYLIST: confirmed (file: work/<slug>/zh.md, sha256: <hash>, date: <YYYY-MM-DD>)`) in `work/<slug>/debate-zh.md`, and `Translator` completes the handoff checklist. Any irreducible `HOLD` goes to the Operator with both positions stated briefly.

#### Stage 3 — `Dispatcher` / `Assembler` & Post-Run `Recap` (Deterministic Gate, Assembly, Publish, Recap & Wave Dispatch)
- **Strict Dispatcher Boundary:** Deterministic verifier, assembler, and wave dispatcher—**never** an autonomous Orchestrator or prose rewriter. Never spawns a separate subagent just to interleave paragraphs, and never hand-rewrites neighbor prose in `content/posts/` without Stage 1/2 peer review; for a New Post `N`, 1-hop reverse-link and narrative refinement across outbound neighbors is executed by `/sleep` (`L1 = links_out(N) \setminus \{N\}`), or if woven into 1–2 neighbors during `/wake`, passes through `Drafter` $\leftrightarrow$ `Critic` and `Translator` $\leftrightarrow$ `Stylist`.
- **Execution Checklist per Node (or Completed Streamline Batch):**
  1. **Verify Stage Gates, Recompute `sha256` Hashes & Drop Contexts:** Check that `work/<slug>/debate-en.md` ends with `CRITIC: confirmed (sha256: ...)` and `work/<slug>/debate-zh.md` ends with `STYLIST: confirmed (sha256: ...)`, with zero open flags or unresolved Operator points. Recompute the `sha256` of `work/<slug>/en.md` and `work/<slug>/zh.md` to confirm receipt with Stage 2 (`Translator` and `Stylist`), then immediately drop (`kill`) all remaining task bot contexts for `<slug>`.
  2. **Interleave (`python3 scripts/interleave-post.py <slug>`):** Combine locked `work/<slug>/en.md` and `work/<slug>/zh.md` into `content/posts/<slug>.md` via `python3 scripts/interleave-post.py <slug> [<slug2> ...]`, which strips blank lines inside ```` ```mermaid ... ``` ```` blocks, verifies 1:1 block-kind parity (`h1`, `subtitle`, `h2`, `prose`, `mermaid`), and attaches diagrams to their preceding prose in each language (`CN Paragraph -> CN Diagram -> EN Paragraph -> EN Diagram`).
  3. **Sync Book & Lattice Metadata:**
     - Update [`content/book/<part>.md`](../content/book/) and [`content/book/index-of-premises.md`](../content/book/index-of-premises.md) (when adding a new post `N`, or updating `→ [<Title>](../../posts/<slug>/)` links if an H1 title changed).
     - **Cross-Streamline Incoming Anchor Sync:** If `<slug>`'s H1 title changed, grep **both** `content/posts/*.md` **and** active in-flight `work/*/en.md` and `work/*/zh.md` for `](../<slug>/)`. If an incoming link sits inside an active `work/<in-flight-slug>/`, update `work/<in-flight-slug>/{en,zh}.md` (never `content/posts/<in-flight-slug>.md` directly while in-flight) so its subsequent Stage 3 assembly preserves the synced anchor.
  4. **Run Audits & Projections (Evaluating Advisories Causally in Context):**
     - `python3 scripts/audit-post.py <slug>` (pass `--walkthrough <path>` explicitly when auditing a waking post whose `walkthrough.md` sits in a session artifact directory; passes on `CLEAN PASS`, or on `PASSED WITH ADVISORIES` when each advisory is causally verified in context—never treat an advisory as a blind stopping rule).
     - `python3 scripts/audit-book.py` (uses `git log --reverse -M` so historical slug renames preserve their original creation date; passes on `CLEAN PASS`, or on `PASSED WITH ADVISORIES` when each advisory is causally verified in context).
     - `node build.mjs`
     - `node scripts/project-posts-graph.mjs` (`missing_targets: 0`)
  5. **Post-Run `Recap` & Carry-Over Note (`Fix the Process, Not the Instance`):**
     - Write any late-discovered information too late to act on in the current run to `work/carry-over.md` (or `work/todo.md` for cross-node wave items) so the next run's first bot reads it and clears it once acted on.
     - Run a fresh **`Recap`** pass (loading `/ontological-clarity` and reading the run folder: artifacts, `debate-en.md`, `debate-zh.md`, and any escalations) to ask one question: *where did the run fall short of logical coherence?* (e.g., a charter with conflicting goals, a skill step built on an unstated premise, or shared blind spots between maker and critic). If `Recap` identifies a process fault, it **proposes** specific charter/skill changes to the Human Operator for decision—never self-editing charters or skills silently.
  6. **Publish & Prune Transient Workspace (Tracked Paths Only in `git add`):**
     - Never pass gitignored paths (`work/` or `public/`) to `git add` (which exits with code `1`); stage only tracked canonical paths (`content/posts/`, `content/book/`, `data/`, `assets/`).
     - For a **Waking New Post (`N`) or Waking Refinement**: Present `walkthrough.md` (for `N`) and any `Recap` proposals, pause for Operator check (unless the Operator already authorized push), then `git commit` & `git push origin main`, run `bash scripts/watch-deploy.sh`, verify live HTTP 200, delete `work/<slug>/` (`rm -rf work/<slug>`), and (for a New Post `N`) overwrite `work/wave.md` with the fresh wave state (`visited = {N}`), ready for `/sleep` to weave `N` into `L1`.
     - For a **Sleep Wave Node Batch (`L1` / `L2` / ... / `Lk`)**: Commit all nodes completed in the batch, `git push origin main`, wait for GitHub Pages deploy (`bash scripts/watch-deploy.sh`), verify live HTTP 200 on `https://powerpig99.github.io/not-a-toe/posts/<slug>/`, delete `work/<slug>/` (`rm -rf work/<slug>`), mark the nodes `[x]` in `work/wave.md`, and dispatch the next window.

---

## 4. Operator Command Lifecycle: `/wake` (`/draft`), `/sleep`, `/deep-sleep`, and `/bridge`

### 4.1 `/wake [seed]` (Alias: `/draft [seed]`) — Waking Evaluation & Inscription into Artificial Memory
1. **Interrupt Sleep Cleanly:** If a `/sleep` or `/deep-sleep` consolidation wave is active in `work/wave.md`, let any currently in-flight node finish and do not dispatch further sleep nodes.
2. **Stage 0A — Probe for Waking Materials (If Not Already Supplied):**
   - Ask the Operator for whichever of the four waking inputs they have (it can be all four, or just a simple initial idea):
     1. **New Intuition / Spark:** What is the new intuition or core idea?
     2. **Inspiring Source:** What source inspired the spark (an X post/link, article, paper, or observation)?
     3. **Thinking Process:** Is there a discussion with AI (e.g., Grok/Gemini/Claude chat or share link) or an X comment thread?
     4. **Initial Draft:** Is there an initial draft of the essay already, or are we starting from a simple initial idea?
3. **Stage 0B — Corpus Evaluation & Recommendation (`New Post` vs. `Refinement` vs. `Drop`):**
   - Load `/ontological-clarity` and [`AGENTS.md`](../AGENTS.md), and search [`content/book/index-of-premises.md`](../content/book/index-of-premises.md), [`docs/posts.graph.json`](../docs/posts.graph.json), and the closest existing posts in `content/posts/`.
   - Give an explicit recommendation and **wait for the Operator's go-ahead**:
     - **`NEW POST` (`N`):** The spark introduces a genuinely new operative cut or dissects a held belief/premise not yet covered by an existing post. Propose the bilingual title (preserving the Operator's title if supplied), single-sentence italic subtitle, `<slug>`, spine, Book Part (`content/book/<part>.md`), Index of Premises entries, and adjacent cross-links.
     - **`REFINEMENT` (of existing post(s)):** The spark sharpens, extends, or corrects a face on the same axis as 1–2 existing posts without needing a separate URL. Name the exact target post(s) and the surgical refinement to weave in.
     - **`DROP` (Repetitive):** The cut is already held in existing post(s) with no new distinction. Cite the exact existing post(s) and recommend dropping so the Living Book never accumulates duplicate nodes.
4. **Stages 1–3 — Authoring & Ship (On Operator Go-Ahead for `NEW POST` or `REFINEMENT`):**
   - Run Stage 1 (`Drafter` $\leftrightarrow$ `Critic` on `work/<slug>/en.md`).
   - Run Stage 2 (`Translator` $\leftrightarrow$ `Stylist` on `work/<slug>/zh.md`).
   - Generate novel 21:9 cover art (`assets/covers/<slug>.jpg`, for `NEW POST` `N`) and register in [`assets/covers/STYLES.md`](../assets/covers/STYLES.md).
   - Run Stage 3 (interleave, Book Part & Index of Premises update, `audit-post.py --walkthrough <path>`, `audit-book.py`, `build.mjs`, `project-posts-graph.mjs`, `walkthrough.md`, and publish; any immediate backlink woven into 1–2 prior essays during `/wake` passes through Stages 1–2 peer review, while full 1-hop consolidation across all outbound neighbors runs in `/sleep`).
   - For a `NEW POST` `N`, overwrite `work/wave.md` (`visited = {N}`), ready for `/sleep`.

### 4.2 `/sleep` — `N`-Driven Causal Ripple (`Node 0` + `Pre-Wave Sweep` + `Trace DELTA Until NO_DELTA` + `Post-Wave Sweep`)
- By `Trace` asymmetry in `/ontological-clarity`, a new post `N` can require reverse links (`P → N`) both in posts `N` explicitly linked to (`links_out(N)`) and in conceptually adjacent posts across the Living Book that `N` did not link to directly. Conversely, when a visited post `u` is confirmed `NO_DELTA` (`sha256` unchanged), it transmits zero further perturbation along its edges.
- **Execution:**
  1. Identify the most recently published waking post `N` (or active wave in `work/wave.md`).
  2. **Run Node `0` (`_plan-consolidation` — Stage 1 Only: `Drafter` ⇄ `Cold Critic`, Zero Translation):**
     - `Drafter` evaluates `N` against `docs/wave-refinement-plan.md`, `docs/adapters/antigravity.md`, `AGENTS.md`, and `/Users/jingliang/.grok/skills/*/SKILL.md` under the `DELTA` vs. `NO_DELTA` Causal-Necessity Gate (`draft.md` + `notes.md` on `DELTA`, or `NO_DELTA` with a 1-paragraph causal proof in `notes.md`).
     - `Cold Critic` verifies `work/_plan-consolidation/` cold (`CRITIC: confirmed` or `CRITIC: confirmed_no_delta` with `sha256` in `work/_plan-consolidation/debate-en.md`), confirmed plan edits are applied, `work/_plan-consolidation/` is pruned (`rm -rf`), and Node `0` is marked `- [x]` in `work/wave.md`.
  3. **Run Pre-Wave Reverse-Link Sweep (`_reverse-link-sweep` — Stage 1 `Drafter` ⇄ `Cold Critic`):**
     - Regenerate [`docs/posts.graph.json`](../docs/posts.graph.json) (`node scripts/project-posts-graph.mjs`).
     - `Drafter` reads `content/posts/<N>.md`, `content/book/index-of-premises.md`, `content/book/*.md`, and the compact `slug + # Title + *Subtitle*` catalog of all posts outside `links_out(N) ∪ {N}`, proposing candidate posts $S_{\text{pre}}$ in `work/_reverse-link-sweep/notes.md` whose own cut is sharpened or completed by `N` (requiring `P → N` or `N → P`), or `NO_DELTA` if `links_out(N)` already holds every directly relevant post.
     - `Cold Critic` cold-reads `N`, `work/_reverse-link-sweep/notes.md`, and the full text of each candidate `content/posts/<slug>.md` (plus adjacent entries in `index-of-premises.md` and `content/book/<part>.md`), rejecting thematic/keyword link-stuffing and signing off on the confirmed candidate set $S_{\text{pre}}$ (`CRITIC: confirmed` or `CRITIC: confirmed_no_delta` with `sha256` in `work/_reverse-link-sweep/debate-en.md`).
     - Merge confirmed $S_{\text{pre}}$ with $\text{links\_out}(N) \setminus \{N\}$ to form $L_1 = (\text{links\_out}(N) \cup S_{\text{pre}}) \setminus \{N\}$ (sorted by descending `links_out`), and write `## L1 (<count>)` to `work/wave.md` with $\text{visited} = \{N\} \cup L_1$.
  4. **Run Recursive `DELTA`-Only Wave Across $W$ Parallel Streamlines (`L1 → L2 → ...` Stopping at `NO_DELTA`):**
     - For every unchecked `[ ]` post in $L_k$ ($k = 1, 2, \dots$), Stage 1 (`Drafter` ⇄ `Cold Critic`) evaluates causal necessity first:
       - **`DELTA` (`CRITIC: confirmed`):** Where `N` (for $L_1$) or a parent `DELTA` node in $L_{k-1}$ (for $k \ge 2$) sharpens or completes the target post's own cut (or the target post has hygiene/bilingual drift), `Drafter` weaves the surgical refinement and cross-link into `work/<slug>/en.md`, `Critic` signs off with `sha256`, Stage 2 (`Translator` ⇄ `Stylist`) translates and signs off `work/<slug>/zh.md`, and Stage 3 (`Dispatcher`) interleaves, audits, builds, commits, pushes, verifies live HTTP 200, deletes `work/<slug>/`, and marks `- [x] <slug> (DELTA)`.
       - **`NO_DELTA` (`CRITIC: confirmed_no_delta` — Branch Stops Here):** Where the target post is already complete on its own axis and passes all invariants cleanly, `Critic` confirms `NO_DELTA` in `work/<slug>/debate-en.md`, Stages 2 and 3 are skipped, `work/<slug>/` is deleted, `Dispatcher` marks `- [x] <slug> (NO_DELTA)`, and **that branch terminates without expanding into $L_{k+1}$**.
     - Once all nodes in $L_{k-1}$ are `[x]` (or parked on `[HOLD]`), collect $\text{DELTA}_{k-1}$ (the subset of nodes in $L_{k-1}$ that finished as `DELTA`). If $\text{DELTA}_{k-1} = \emptyset$, the `DELTA` ripple has converged; otherwise re-project `docs/posts.graph.json` and compute:
       $$L_k = \left(\text{links\_in}(\text{DELTA}_{k-1}) \cup \text{links\_out}(\text{DELTA}_{k-1})\right) \setminus \text{visited}$$
       (including `links_in(u)` for every $u \in \text{DELTA}_{k-1}$ with `in_degree <= 30` so reverse-link dependents are traced without mega-hub explosion), append `## L<k> (<count>)` to `work/wave.md`, add $L_k$ to `visited`, and repeat until $\text{DELTA}_k = \emptyset$ or $L_k = \emptyset$.
  5. **Run Post-Wave Cross-Link Sweep (`_post-wave-sweep` — Stage 1 `Drafter` ⇄ `Cold Critic`):**
     - `Drafter` and `Cold Critic` inspect `N` and all `DELTA` posts modified during the wave against `content/book/index-of-premises.md`, `content/book/*.md`, and the unvisited corpus `Title + Subtitle` catalog to verify that no newly refined `DELTA` cut missed a cross-link (running Stages 1–3 on any confirmed candidate until `CRITIC: confirmed_no_delta`).
  6. Run cold `Recap` (`/recap`) and report `/sleep` completion, ready for `/deep-sleep` (or `/wake`).

### 4.3 `/deep-sleep` — Full-Corpus & Site-Wide Consolidation (`All Remaining Posts + Book/Site Contents`)
- **Orthogonal Division of Labor:** Because `/sleep` stops at `NO_DELTA` to bound `N`'s causal ripple, `/deep-sleep` consolidates **all remaining unvisited posts (`content/posts/*.md \setminus visited`) and the rest of the site contents (`content/book/*.md` prefaces and `content/book/index-of-premises.md`)** so older posts and book surfaces are systematically refreshed and cross-linked rather than starved.
- **Execution:**
  1. Read `work/wave.md`. If `/sleep` still has unchecked `[ ]` items in its `N`-ripple, finish those first.
  2. **If the current `## Deep Sleep Batch <m>` still has unchecked `[ ]` nodes:** Resume across $W$ parallel streamlines until the batch is `[x]` complete.
  3. **Once the current batch is `[x]` complete (or starting the first Deep Sleep batch after `/sleep`):**
     - Run `node scripts/project-posts-graph.mjs`.
     - Queue all remaining unvisited posts (`content/posts/*.md \setminus visited`) ordered deterministically by **oldest last-commit timestamp first** (`git log -1 --format="%ct"`, or by Book Part if specified), followed by the remaining book/site content nodes (`_book:README`, the 14 `_book:<part>` prefaces, and `_book:index-of-premises`).
     - Select the next batch of size $B$ (default $B = 12$), append `## Deep Sleep Batch <m> (<count>)` to `work/wave.md`, add them to `visited`, and run the Two-Way `DELTA` vs. `NO_DELTA` pipeline (`Drafter` ⇄ `Cold Critic` [checking both missing cross-links to newer posts and `/ontological-clarity` / `AGENTS.md` prose hygiene] → `Translator` ⇄ `Stylist` → `Dispatcher/Assembler`) across $W$ parallel streamlines.
     - Repeat batch by batch until the entire corpus and book are 100% consolidated or a new waking post `N'` (`/wake`) initiates a new cycle.

### 4.4 `/bridge`, `/resume-bridge`, and `/retire` — Ephemeral Working Memory (RAM)
- **Model- and Agent-Agnostic Plain Markdown:** Stored at `<project>/memory/bridges/<id>.md` (excluded from git) with zero external Python scripts.
- **Same-Session vs. New-Session Resume:**
  - `/bridge` writes `<project>/memory/bridges/<id>.md` (`Next` + `Traces` with priors named; pointers to `work/wave.md` or `work/plan/<task-id>/` over paraphrases) and stamps `<project>/memory/bridges/.last_session` with `<id>`. Checkpoint with `/bridge` at layer boundaries or before switching between wave execution and architectural planning.
  - `/resume-bridge` **in the same session after `/clear`** (when `SESSION_KEY != none` and matches `Session: <SESSION_KEY>` in `memory/bridges/<id>.md`) auto-loads that bridge and continues immediately without prompting.
  - `/resume-bridge` **in a new session or after `/retire`** lists all available bridges in `<project>/memory/bridges/*.md` sorted by `Updated` and asks the Operator which thread to pick.
  - `/retire` deletes the finished bridge `<project>/memory/bridges/<id>.md` and removes `.last_session` so no stale working-memory log lingers once changes are consolidated into long-term memory.

### 4.5 `/recap` — Cold Post-Task & Operator-Initiated Process Optimization Audit
- **Bridging `SKILL` Incompleteness Without Mid-Run Drift:** Because deterministic `SKILL` boundaries cannot foresee every surprise, **`/recap`** can run automatically at the conclusion of a task (`work/<slug>/recap.md` or `work/plan/<task-id>/recap.md`) **or** be invoked on demand at any time by the Operator (`/recap [target]`).
- **Execution:** Spawns a fresh, cold `Recap` context under `/ontological-clarity` to inspect the completed run folder or session surprise/escalation against the governing `SKILL`s and charters. It checks for (1) Task Tier misclassification (Tier 1 vs. Tier 2 vs. Tier 3), (2) Pre-Escalation Gate accuracy (whether a `Cold Critic` and, where applicable, a `Cold Scouter` were used before interrupting the Operator), (3) unstated premises or conflicting charter goals, (4) shared blind spots between maker and critic, and (5) skill sprawl that can be pruned, presenting surgical `SKILL`/charter diff proposals for the Operator to decide.

---

## 5. Non-Blocking Fault Isolation, Adaptive Parallel Streamlines & Session Hygiene

### 5.1 Non-Blocking Fault Isolation, Hub-First Ordering & Adaptive Parallel Streamlines (`W`)
Because `work/<slug>/` isolates in-flight drafts from `content/posts/`, Stages 1 & 2 across distinct nodes in a layer $L_k$ share zero mutable state:
- **Hub-First Out-Degree Ordering:** Within each layer $L_k$, nodes are sorted by descending outgoing link count (`links_out` in `docs/posts.graph.json`), so the highest-leverage hubs consolidate first.
- **Customizable & Auto-Derived Parallel Concurrency ($W$ Streamlines):**
  - **Operator Override (Customizable):** The Operator may pass an explicit concurrency target (e.g., `/sleep concurrency=8`, `/deep-sleep 10`, or in natural language) to set the number of concurrent node streamlines $W$ directly.
  - **Automatic Derivation from Layer Size (Default):** When not explicitly specified, `Dispatcher` derives the active streamline window $W$ from the number of remaining unchecked `[ ]` nodes $R = |L_k|_{\text{rem}}$ in the current layer:
    $$W(R) = \begin{cases} R & \text{if } R \le 4 \\ 6 & \text{if } 5 \le R \le 20 \\ 8 & \text{if } 21 \le R \le 60 \\ 12 & \text{if } R > 60 \end{cases}$$
    Up to $W$ independent `work/<slug-j>/` directories run Stages 1 & 2 concurrently across nodes (while within each node, Stage 2 starts only after Stage 1 signs off the finished `en.md` and its `sha256` per §3).
  - **Serialized / Batched Stage 3 Assembly:** Only Stage 3 (`content/posts/<slug>.md` interleaving, `content/book/` & `data/title-translations.json` sync, `build.mjs`, `project-posts-graph.mjs`, and `git commit && git push`) touches shared repository state. `Dispatcher` batches all nodes that finish Stage 2 in the same turn into a single atomic build, graph projection, commit, and push.
- **Localized Fault Isolation on `HOLD`:** If Node $j$ hits an irreducible deadlock between `Drafter` and `Critic` (or `Translator` and `Stylist`) after Round 2, `Dispatcher` marks Node $j$ as `[HOLD — awaiting Operator]` in `work/wave.md` and **immediately refills its streamline slot with the next `[ ]` node**. A premise contradiction in one node never halts the wave; only that node's local streamline waits for the Operator's synthesis.

### 5.2 Session Trajectory Hygiene Across Wave Nodes
To prevent a long sleep wave from turning agent sessions into a cross-node epistemic gravity well:
1. **1 Node per Fresh Subagent Context (While Scaling $W$ Across Nodes):** Parallelism scales *across* isolated node contexts ($W$ concurrent streamlines), never by stuffing many unrelated essays into a single subagent's conversation history. Each generative and review role (`Drafter`, `Critic`, `Translator`, `Stylist`) runs in a fresh context per node and is retired (`kill`) immediately once that stage's handoff is confirmed, so prior debates never act as conditioning history for the next essay.
2. **Externalize Durable Findings Only to `work/todo.md` & `work/carry-over.md`:** Any cross-post observation discovered while working on Node $j$ (e.g., a broken title case or residual moral phrasing noticed in a neighbor) is appended as a one-line fact to `work/todo.md` (and any late run-level information to `work/carry-over.md`) and dropped from active session memory until that neighbor's own wave node or next run arrives.
3. **True Cold-Read Separation:** `Critic` (on `en.md`), `Stylist` (cold read on `zh.md`), and `Recap` (post-run review against `/ontological-clarity`) must run in a fresh context unconditioned by the generator's session tokens.

### 5.3 Chinese-Original Exception
All `400/400` posts in the corpus are now full alternating bilingual essays (`0` monolingual stubs remain in `data/title-translations.json`). For the 3 historically Chinese-first posts (`e-shi-feng-bi-de-shan`, `qian-yin-hou-guo`, `mei-you-pu-du-zhi-you-zi-du`) or when a future waking post is drafted Chinese-first, the language order in Stages 1 and 2 flips so the author's original Chinese is refined first rather than overwritten by a back-translation:
- **Stage 1 (`Drafter` $\leftrightarrow$ `Critic`):** Refines the Chinese text in `work/<slug>/zh.md` (logged and signed off by `sha256` in `work/<slug>/debate-zh.md`).
- **Stage 2 (`Translator` $\leftrightarrow$ `Stylist`):** Translates/syncs the locked Chinese into English in `work/<slug>/en.md` (logged and signed off by `sha256` in `work/<slug>/debate-en.md`).
- **Stage 3 (`Dispatcher` / `Assembler`):** Interleaves `zh.md` and `en.md` into `content/posts/<slug>.md` via `python3 scripts/interleave-post.py <slug>`.

---

## 6. Supplementary Architecture: Controlled Open-Internet Injection for Orthogonal Planning Cycles (Cross-Project)

> **Scope & Relation to Essay Pipeline:** Applies across `not-a-toe` and **any project in Extended Memory (`/Users/jingliang/Projects/*`)** for tasks that require structured external research before a stable implementation plan can be handed to a Dispatcher (coding, system design, research synthesis, media/tooling pipelines, or `/wake` Stage 0 reference-architecture scouting). It does not replace the waking/sleep essay pipeline; it provides an orthogonal planning loop wherever best-known external references must be injected under strict context boundaries.  
> **Practical Bound:** Agents remain finite projection engines. This wiring localizes non-convergence; it does not classify "premise-level residual" versus "implementation-detail residual," nor does it dissolve contradictions in living intent. The human orchestrator retains responsibility for claiming residuals and spotting inconsistencies. The resulting system is a larger, better-structured deterministic machine whose usefulness still depends on the operator's capacity to leverage it.

### 6.1 Purpose and Mechanism
For any task whose implementation plan benefits from current external knowledge (best-known practices, reference architectures, constraints, failure modes), this cycle inserts a retiring **Scouter** layer between generative planning (**Planner**) and equal-footed evaluation (**Evaluator**). Each Scouter receives only a defined technical plan artifact (plus any neutral, falsifiable research questions from the previous cycle's `residuals-v{N-1}.md`), performs deep external research, delivers a structured report, and retires immediately. No Scouter session history conditions later agents. The cycle repeats until the plan stabilizes under the available external signal (`EVALUATOR: confirmed`), advances to the next scouting cycle on open empirical/technical questions (`SCOUT`), or escalates irreducible deadlocks (`HOLD`) to the Operator. Once finalized, `Evaluator` promotes `plan-vN.md` to `final-plan.md` and hands it to a **Task Dispatcher** that deterministically dispatches the peer-verified subtask DAG (recursing the same pattern on subtasks marked `needs_research: true`).

### 6.2 Roles and Context Boundaries

| Role | Context Received | Context Explicitly Excluded | Lifetime | Output |
| :--- | :--- | :--- | :--- | :--- |
| **Planner** | Original goal + given information; in cycle $N > 1$, `debate-v{N-1}.md` & `residuals-v{N-1}.md` | `Scouter`'s raw search session, other `Planner` histories, direct web/external search tools | Persists across one planning cycle ($v1 \dots vN$) until `final-plan.md` locks | Self-contained `plan-vN.md` (including orthogonal subtask DAG); debate replies in `debate-vN.md` |
| **Scouter** | `plan-vN.md` only (or `plan-vN.md` + `residuals-v{N-1}.md` only) | Original user goal/prompt, session motivation, `Planner` or `Evaluator` session tokens, `debate-v*.md` transcripts, prior `research-v*.md` | Single pass per cycle $N$; **retires immediately** after writing report | Structured research report `research-vN.md` (implementations, constraints, failure modes, sources) |
| **Evaluator** | Original goal + given information + `plan-vN.md` + `research-vN.md` | `Planner`'s chain-of-thought, `Scouter`'s raw search trajectory, prior `Evaluator` sessions, direct web/external search tools | Single debate pass per cycle $N$; **retires immediately** after writing Round 2 disposition | Evaluation points `E1..En` & Round 2 dispositions (`CONCEDE` / `SCOUT` / `HOLD`) in `debate-vN.md`; writes `residuals-vN.md` (on `SCOUT`) or promotes `final-plan.md` (on `EVALUATOR: confirmed`) |
| **Task Dispatcher** | Finalized `final-plan.md` only (plus minimal `STATUS:` routing tokens during cycles) | All intermediate session histories, raw `research-v*.md` and `debate-v*.md` contents (unless escalated on `HOLD` / `max_cycles`) | Persists for the task; may recurse up to `max_depth` | Dispatches the locked parallel/serial subtask DAG from `final-plan.md`; spawns child planning cycles for subtasks with `needs_research: true` |

**Context-Boundary & Artifact Invariants:**
1. **Mandatory Retirement of Scouter & Evaluator:** Every `Scouter` and `Evaluator` starts in a fresh context and is terminated (`kill`) immediately after its single-cycle duty. No role accumulates a long-lived research or evaluation trajectory across cycles.
2. **Planner Trajectory Put to Work for Continuity Only (Zero Direct Search):** `Planner` is the only role that retains session continuity across cycles $v1 \dots vN$ of a single plan. Neither `Planner` nor `Evaluator` may invoke web search or external URL tools; all external scouting belongs exclusively to `Scouter`.
3. **Self-Contained Specification in `plan-vN.md` & Neutral Questions in `residuals-vN.md`:** `plan-vN.md` must contain only the self-contained technical specification (components, premises, constraints, interfaces, verification steps, and the orthogonal parallel/serial subtask DAG with file/state isolation boundaries and `needs_research: true|false` flags). `residuals-vN.md` (written by `Evaluator`) must contain only neutral, falsifiable research questions—never the raw user prompt, session narrative, or debate transcript rationalizations.
4. **Uncontaminated `Task Dispatcher` Routing:** During Cycles $1 \dots N$, `Planner`, `Scouter`, and `Evaluator` return only minimal status tokens and file pointers (`STATUS: PLAN_READY`, `STATUS: RESEARCH_READY`, `STATUS: DEBATE_ROUND1_OPEN`, `STATUS: RESIDUALS_PACKAGED`, `STATUS: EVALUATOR_CONFIRMED`, `STATUS: HOLD`) to the routing harness. `Task Dispatcher` routes file paths without reading `research-v*.md` or `debate-v*.md` into its own context prior to reading `final-plan.md` (unless `STATUS: HOLD` or `max_cycles` triggers Operator escalation).

### 6.3 Planning Cycle Topology & Steps

```mermaid
flowchart TD
    subgraph S_Cycle["Orthogonal Planning Cycle (Repeats Until Stable or Max Cycles)"]
        P["Planner (Persistent per Task)<br/>Drafts / revises self-contained plan-vN.md (+ subtask DAG)<br/>from original context + residuals-v(N-1)"]
        S["Scouter (Fresh Cold Context)<br/>Receives plan-vN.md (+ residuals-v(N-1)) only<br/>Deep external research → research-vN.md<br/>Retires immediately"]
        E["Evaluator (Fresh Cold Context)<br/>Receives original context + plan-vN.md + research-vN.md<br/>Debates Planner in debate-vN.md (CONCEDE / SCOUT / HOLD)<br/>Writes residuals-vN.md or final-plan.md & retires"]
        P --> S
        S --> E
        E -->|"SCOUT (N < max_cycles): writes residuals-vN.md"| P
    end

    S_Cycle -->|"EVALUATOR: confirmed → writes final-plan.md"| TD["Task Dispatcher<br/>Reads final-plan.md only<br/>Dispatches locked parallel / serial subtask DAG<br/>Recurses cycle (depth ≤ max_depth) or executes"]
    E -->|"HOLD after Round 2 or SCOUT at N == max_cycles"| Op["Human Operator<br/>Claims residual package<br/>Synthesizes premise, revises rule, or accepts bound"]
    Op --> TD

    style S_Cycle fill:#161b22,stroke:#58a6ff,stroke-width:1.5px,color:#58a6ff
    style P fill:#0d1117,stroke:#58a6ff,stroke-width:1px,color:#f0f6fc
    style S fill:#0d1117,stroke:#d29922,stroke-width:1px,color:#f0f6fc
    style E fill:#0d1117,stroke:#a371f7,stroke-width:1px,color:#f0f6fc
    style TD fill:#0d1117,stroke:#3fb950,stroke-width:1px,color:#f0f6fc
    style Op fill:#0d1117,stroke:#f85149,stroke-width:1px,color:#f0f6fc
```

1. **Draft / Revise (`Planner`):** `Planner` drafts (or revises) a self-contained implementation plan and orthogonal subtask DAG in `work/plan/<task-id>/plan-vN.md` from the original goal and given information (or in cycle $N > 1$, from `residuals-v{N-1}.md` and `debate-v{N-1}.md`), and returns `STATUS: PLAN_READY`.
2. **Scout (`Scouter` — Fresh Context, Retires):** `Scouter` is spawned in a fresh context receiving **only** the path to `plan-vN.md` (plus `residuals-v{N-1}.md` if $N > 1$). It conducts deep external/open-internet research on best-known implementations, hard constraints, APIs, failure modes, and subtask isolation assumptions, writes `work/plan/<task-id>/research-vN.md`, returns `STATUS: RESEARCH_READY`, and retires immediately.
3. **Evaluate & Debate (`Evaluator` ⇄ `Planner` — Fresh Evaluator Context, Retires):**
   - **Round 1:** `Evaluator` is spawned in a fresh context receiving the original goal + given information + `plan-vN.md` + `research-vN.md`. It evaluates `plan-vN.md` (including its subtask decomposition and `needs_research` flags) against the goal and `research-vN.md`, logs numbered evaluation points (`E1..En`) in `work/plan/<task-id>/debate-vN.md`, and returns `STATUS: DEBATE_ROUND1_OPEN` (or `EVALUATOR: confirmed` if clean on first pass).
   - **Planner Reply:** `Planner` replies to each `E1..En` in `debate-vN.md` on equal footing with `ACCEPT` (updating `plan-vN.md`), `COUNTER` (tracing why the plan's premise holds against `research-vN.md`), `SCOUT` (proposing a specific falsifiable external research question for Cycle $N+1$), or `HOLD`. Neither peer closes a flag unilaterally.
   - **Round 2 Dispositions (`CONCEDE` vs. `SCOUT` vs. `HOLD`):** In Round 2, `Evaluator` verifies `Planner`'s updates and marks each flag with one of three distinct dispositions:
     1. **`CONCEDE` (`CLOSED applied` or `CLOSED withdrawn`):** Resolved in the current cycle.
     2. **`SCOUT` (External-Signal Residual):** `Planner` and `Evaluator` agree that a concrete, falsifiable external/technical question or newly revised mechanism is not yet settled by `research-vN.md`.
     3. **`HOLD` (Irreducible Deadlock):** `Planner` and `Evaluator` remain deadlocked on a premise, goal interpretation, or already-scouted constraint after Round 2 where further external search will not resolve the disagreement.
4. **Cycle Transition & Artifact Packaging (`Evaluator` Ownership):**
   - **Local Convergence (`EVALUATOR: confirmed`):** When all `E1..En` are `CONCEDE` with zero `SCOUT` or `HOLD` items, `Evaluator` writes `EVALUATOR: confirmed` at the bottom of `debate-vN.md`, copies `plan-vN.md` to `work/plan/<task-id>/final-plan.md`, returns `STATUS: EVALUATOR_CONFIRMED`, and retires.
   - **Next Scouting Cycle (`SCOUT` with Zero `HOLD` and $N < \text{max\_cycles}$):** When one or more `SCOUT` items remain (and zero `HOLD` items) and $N < \text{max\_cycles}$, `Evaluator` writes the neutral, falsifiable research questions to `work/plan/<task-id>/residuals-vN.md`, returns `STATUS: RESIDUALS_PACKAGED`, and retires. `Planner` then writes `plan-v{N+1}.md` and Cycle $N+1$ begins with a fresh `Scouter`.
5. **Hard Stabilization Bound & Escalation:**
   - Every planning run enforces a hard maximum cycle bound (`max_cycles`, default `3`, or an explicit Operator stop condition).
   - **Irreducible `HOLD` or Bound Reached (`N == max_cycles`):** If any flag is marked `HOLD` after Round 2 (at any cycle $N$), or if `SCOUT` residuals remain when $N == \text{max\_cycles}$, `Evaluator` packages the unresolved tensions into `work/plan/<task-id>/residuals-vN.md`, returns `STATUS: HOLD`, and retires. The local planning streamline pauses and surfaces the residual package (`residuals-vN.md`, current `plan-vN.md`, and relevant excerpts from `research-vN.md`) to the **Operator**. Other parallel streamlines continue unimpeded.
   - **Operator Claim:** The Operator claims the residual package and performs the higher-order synthesis—revising premises, accepting the residual as outside the current projection, or injecting a refined rule—and authorizes or writes `final-plan.md` for `Task Dispatcher`.

### 6.4 Task Dispatcher Recursion & Integration with Canonical Pipeline

- **Deterministic Dispatch of Peer-Verified Subtask DAG by Task Tier (`max_depth` Bounded):**
  - `Task Dispatcher` reads **only** `work/plan/<task-id>/final-plan.md` and executes the parallel/serial subtask DAG already verified by `Scouter` and `Evaluator`, where each subtask carries an explicit deterministic tier (`tier: deterministic | subtask | creative`):
  - **Tier 1 Subtasks (`tier: deterministic`):** Closed-endpoint scripts, builds, or checks with fully stated parameters. `Task Dispatcher` executes them directly with **zero `Critic` and zero `Scouter`**.
  - **Tier 2 Subtasks (`tier: subtask`, default for bounded non-trivial subtasks):** Dispatched to an isolated `Maker` paired by default with a fresh **`Cold Critic`** (operating in both directions: preventing errors/false-positive escalations and surfacing overlooked angles). If `Maker` believes an issue requires Operator intervention, it must pass the deterministic **Pre-Escalation Gate** (`Maker` ⇄ `Cold Critic`, plus a cold retiring `Scouter` inferring external sources like X/GitHub/docs if external prior art applies) before interrupting the Operator. (When the subtask is Living Book prose, this maps to Stages 1–3 of the canonical essay pipeline.)
  - **Tier 3 Subtasks (`tier: creative` / `needs_research: true`):** Open-ended or architectural subtasks that expand their residual decision space. If current recursion depth $d < \text{max\_depth}$ (default `max_depth = 2`, overridable by the Operator), `Task Dispatcher` recurses the full Planning Cycle (`Planner` → cold `Scouter` → cold `Evaluator`) in an isolated child directory `work/plan/<task-id>/<subtask-id>/` with zero parent session history leaking downward. If $d == \text{max\_depth}$ and a child plan still requests further subtask research recursion, `Task Dispatcher` pauses that branch and escalates to the Operator.
  - Cross-subtask observations are appended as one-line facts to `work/todo.md` and dropped from active session contexts.
  - **Post-Task `Recap` & Cleanup:** At the conclusion of `final-plan.md` (or whenever the Operator invokes `/recap`), a cold `Recap` pass audits the run (`work/plan/<task-id>/recap.md`) against `/ontological-clarity` and surfaces any proposed `SKILL`/charter boundary improvements to the Operator before `Task Dispatcher` deletes `work/plan/<task-id>/` (`rm -rf work/plan/<task-id>`).

| Canonical Element | Integration with Orthogonal Planning Cycle (Section 6) |
| :--- | :--- |
| **Stage 0 `/wake` probe** | May invoke the Section 6 Planning Cycle (Tier 3) when a waking spark requires external reference architectures or empirical/technical verification before a cut is drafted. |
| **Stage 1 (`Drafter` ⇄ `Critic`)** | Tier 2 bounded subtask; the Section 6 Planning Cycle complements (never substitutes for) ontological review. |
| **Stage 2 (`Translator` ⇄ `Stylist`)** | Tier 2 bounded subtask; unchanged. |
| **Stage 3 (`Dispatcher` / `Assembler`)** | Executes Tier 1 deterministic scripts/audits/deploys for essays; acts as `Task Dispatcher` across Tier 1/2/3 subtasks in `final-plan.md` for Extended Memory projects. |
| **`/sleep` & `/deep-sleep`** | Unaffected; essay lattice consolidation continues under Sections 4–5. |
| **`/bridge` & `/resume-bridge`** | A planning cycle may checkpoint its state in `<project>/memory/bridges/<id>.md` holding only the pointer to `plan-vN.md` and `residuals-vN.md` across session clears. |
| **`/recap`** | Runs at task conclusion or on Operator demand to audit tier classification, pre-escalation gate accuracy, and `SKILL` boundaries. |
| **Minimal Artifacts (`work/plan/<task-id>/`)** | `plan-vN.md` (Planner), `research-vN.md` (Scouter), `debate-vN.md` (Evaluator ⇄ Planner), `residuals-vN.md` (Evaluator on `SCOUT`/`HOLD`), `final-plan.md` (Evaluator on `EVALUATOR: confirmed`, handed to Task Dispatcher), `recap.md` (Recap). |

---

## 7. Event-Driven On-Demand Bot Dispatching: Reference Protocol, Failure Handling, Open Questions & Glossary

> **Companion Essay:** [`On-Demand Contexts Keep Coherence at One Step`](../content/posts/on-demand-contexts-keep-coherence-at-one-step.md) & [`The Density of Judgment`](../content/posts/the-density-of-judgment.md)  
> **Scope:** General multi-step agent pipeline scheme (`Bot = base model + charter + skills`) applicable across essay authoring, sleep consolidation, media production (`studio/deliverables/skills-grokbot/`), and any project in Extended Memory.

### 7.1 End-to-End Run Lifecycle & Sequence Diagram

1. **Trigger & Deterministic Tier Selection:** A schedule, incoming email, user message, webhook, or event fires. The **Dispatcher** (the only persistent bot holding triggers; there is no standing project manager) reads the step's deterministic tier from its `SKILL`/runbook:
   - **Tier 1 (Deterministic Execution):** Closed-endpoint script or command; runs directly without spawning a critic or scouter.
   - **Tier 2 (Bounded Subtask):** Starts the task's **Maker** and clones a **Cold Critic** in a fresh context by default.
   - **Tier 3 (Creative / Open-Ended Task):** Starts **Maker/Planner**, a retiring **Cold Scouter** (which infers the highest-signal external sources—X, GitHub, official docs, papers—for the task at hand), and a **Cold Critic/Evaluator** by default.
2. **Load Context:** Each task bot reads the runbook, the single house rule (`/ontological-clarity`), its charter, its deterministic `SKILL`s, and any carry-over note (`carry-over.md`) from the previous run.
3. **Make:** For Tier 2/3 steps, the maker produces its artifact in the run folder (incorporating `Scouter`'s external report in Tier 3).
4. **Critique in Both Directions:** The cold critic reviews the artifact without the maker's working history—both catching mistakes/drift **and** surfacing overlooked issues or fresh angles that the maker's trajectory missed. The existing standard is the minimum; the critic aims to improve on it.
5. **Debate to Full Agreement:** Both argue as equals from the same logic (`/ontological-clarity`). A point is settled only when both fully agree, never by splitting the difference.
6. **Pre-Escalation Gate Before Interrupting the Human:** Whenever a task owner believes a choice or surprise needs human intervention, or when maker and critic appear deadlocked:
   - First, `Maker` and `Cold Critic` debate on equal footing whether the point is genuinely an underivable human Decision or a Task already derivable from the house rule and existing premises.
   - Second, if they still conclude human intervention is needed (or remain deadlocked) and external prior art applies, they spin up a cold, retiring **`Scouter`** to study solutions from relevant external spaces (X, GitHub, official docs/papers inferred from the task) and reconsider with that findings brief in hand.
   - Only what remains unresolved after reconsideration goes to the human, with both positions stated briefly.
7. **Apply and Sign Off:** The maker applies the agreed fixes. The cold critic signs off on the **exact final file and its `sha256` hash**.
8. **Start the Next Bot and Hand Over:** Maker and critic together start the next step's bot from its charter and hand over the finished artifact.
9. **Confirm:** The handoff is official only when the receiver recomputes the `sha256` hash and confirms receipt directly with **both** maker and critic (if a step hands over to several receivers, **every** receiver must confirm). Then maker and critic contexts are dropped.
10. **Repeat & Recap (`/recap`):** Repeat until the last step finishes. The final pair writes `carry-over.md`, then a fresh **Recap** bot (or an on-demand `/recap` triggered by the human at any point) loads the house rule, reads the whole run folder (artifacts, critique records, escalations) and governing `SKILL`s, asks *where did the deterministic `SKILL` boundaries fall short of logical coherence?*, and **proposes** surgical changes to `SKILL`s or charters for the human to review and decide.

```mermaid
sequenceDiagram
    autonumber
    participant T as Trigger
    participant D as Dispatcher
    participant M1 as Maker (Tier 2/3)
    participant C1 as Cold Critic
    participant S1 as Cold Scouter (Tier 3 or Pre-Escalation)
    participant M2 as Next Bot
    participant H as Human

    T->>D: schedule / event / user command
    D->>M1: start from charter & deterministic SKILL tier (fresh context)
    M1->>M1: load runbook, house rule, SKILLs, carry-over note
    M1->>C1: clone Cold Critic (fresh context, no working history)
    opt Tier 3 Creative Task (by default)
        M1->>S1: spawn Cold Scouter (infers X / GitHub / docs sources)
        S1->>M1: structured external report (S1 retires)
    end
    M1->>M1: produce artifact
    loop Debate as equals under /ontological-clarity (errors + new angles)
        C1->>M1: critique (aim above standard)
        M1->>C1: response / revision
    end
    opt Candidate escalation or deadlock remains
        M1->>S1: spawn Cold Scouter if external prior art applies
        S1->>C1: external solutions brief (S1 retires)
        C1->>M1: reconsider with external signal
        opt Still requires a genuine human Decision
            M1->>H: both positions + scouted context stated briefly
            H->>M1: decision (plus optional SKILL optimization)
        end
    end
    M1->>M1: apply agreed fixes
    C1->>M1: sign off on final file + sha256
    Note over M1,C1: together start next bot from its charter
    M1->>M2: hand over finished artifact
    M2->>M1: confirm receipt (file + hash)
    M2->>C1: confirm receipt (file + hash)
    Note over M1,C1: contexts dropped
    Note over M2,H: ...last step finishes, cold Recap (/recap) runs, human decides SKILL updates
```

### 7.2 Six-Step Handoff Protocol

1. **Final artifact only.** The file is the critic-approved version, with no pending fixes.
2. **Sign-off record.** The critic records file name, `sha256`, date, what was checked, and the points agreed.
3. **Handoff checklist.** The maker completes the shared checklist: artifact present, hash recorded, critique record saved, open questions none or decided by the human, next charter(s) named.
4. **Start the receiver(s).** Maker and critic start each next bot from its charter and point it at the run folder.
5. **Confirmation by every receiver.** Each receiver recomputes the hash and confirms directly with both maker and critic. If any confirmation is missing or any hash does not match, the handoff is not official.
6. **Drop the contexts.** Nothing from maker's or critic's chat survives except what is in the run folder.

### 7.3 Canonical File & Skill Layout for General Pipelines

```text
pipeline/
├── runbook.md              # step order, which charter runs each step
├── house-rule.md           # the single house rule: logical coherence (/ontological-clarity)
├── handoff-checklist.md
├── charters/
│   ├── gatherer.md         # name + role description
│   ├── writer.md
│   └── video-producer.md
├── skills/
│   ├── ontological-clarity.md  # how to apply the house rule
│   ├── gather-sources.md
│   ├── write-brief.md
│   ├── produce-short-video.md
│   ├── critic.md           # loaded by every cold critic
│   └── recap.md            # post-run review
├── carry-over.md           # late information for the next run (cleared once acted on)
└── runs/
    └── <run-date>/
        ├── 01-gather/      # digest.md, critique-record.md (with sha256 sign-off)
        ├── 02-brief/       # brief.md, critique-record.md (with sha256 sign-off)
        ├── 03-video/       # video.mp4, critique-record.md (with sha256 sign-off)
        ├── escalations.md  # questions to the human and decisions
        └── recap.md        # findings and proposed charter/skill changes for human review
```

### 7.4 Failure Handling (`Fix the Process, Not the Instance`)

When a step fails or produces weak work, ask which `SKILL` or charter allowed it. A change to that file is proposed (via post-task or operator-initiated `/recap`), the human decides on it, and the step is then rerun from a **fresh context**. Never patch a running bot with ad-hoc instructions: the fix disappears with the context.
- **A bot crashes or stalls:** If the trace confirms a deterministic local cleanup (e.g., killing a confirmed-stuck read-only TUI process or fixing an unexamined script timing assumption), execute and report it; if a non-trivial choice remains, verify via the Pre-Escalation Gate (`Maker` ⇄ `Cold Critic` [+ optional `Cold Scouter`]) before asking the human whether to redo the step from the last confirmed handoff (in a fresh context) or hold the run. Partial work is discarded.
- **Hash mismatch at handoff:** The handoff is void. The human is told and decides: the previous pair re-signs, or a fresh pair redoes the step.
- **Maker and critic cannot agree (after Pre-Escalation `Scouter` check where applicable):** When `Maker` and `Cold Critic` remain deadlocked—even after spinning up a cold `Scouter` to check relevant external prior art (X, GitHub, docs) where applicable—unresolved points go to the human with both positions stated briefly. The run waits. No rule or watchdog decides in the human's place.
- **Repeated failures or surprises at one step:** Indicates a design fault in that step's deterministic `SKILL` boundary or charter, usually an incoherence or tier misclassification. The `Recap` (`/recap`, run at task conclusion or on Operator call) records it and proposes a surgical `SKILL`/charter change; the human decides.

### 7.5 Incremental Adoption Path (Migrating from a Standing Project Manager)

1. **Write down what the PM knows:** Turn implicit instructions into a `runbook.md`, one charter per role, and a set of deterministic `SKILL`s classifying each step into Tier 1 (deterministic), Tier 2 (`Maker` ⇄ `Cold Critic`), or Tier 3 (`Maker` + `Cold Scouter` + `Cold Critic`). Check them against the house rule (`/ontological-clarity`).
2. **Move triggers to a Dispatcher:** At first the Dispatcher simply wakes the PM.
3. **Convert one step:** Pick the step with the most drift and run it according to its tier (`Maker` + `Cold Critic`), handing back to the PM.
4. **Add sign-off `sha256` hashes, critique records, the Pre-Escalation Gate, and `/recap`.**
5. **Convert the remaining steps** one at a time, letting each pair start the next bot.
6. **Drop the PM context** once the Dispatcher starts the first bot directly.

### 7.6 Trade-Offs and Open Questions (Active Brainstorming Surface)

- **Start-up latency:** Tier 2 and Tier 3 steps pay to load fresh contexts (`Maker` + `Cold Critic` [+ `Cold Scouter`]). *Open question:* Can shared context be cached (e.g., prompt-prefix caching of immutable skill/charter files) without reintroducing stale session memory?
- **Deterministic Tiering vs. Universal Critics (Resolved via Tier 1 / Tier 2 / Tier 3):** Closed-endpoint deterministic steps (Tier 1) run without a critic or scouter, bounded subtasks (Tier 2) run `Maker` ⇄ `Cold Critic` by default (preventing mistakes and surfacing new angles), and creative/open-ended tasks (Tier 3) run `Maker` + `Cold Scouter` + `Cold Critic` from the start.
- **Waiting for agreement & Pre-Escalation Accuracy:** Requiring `Maker` to pass candidate escalations through `Cold Critic` (and `Cold Scouter` where external prior art applies) filters out false-positive interruptions before they reach the human. A rising rate of escalations the gate should have dissolved, or of the same surprise or decision recurring at one step, signals incoherent charters or `SKILL` boundaries; fix them via `/recap` rather than loosening the rule or adding timeouts.
- **Audit trail & run-folder retention:** Run folders, critique records, `sha256` hashes, and recaps make every output traceable. Once absorbed into canonical git checkpoints in `not-a-toe` (or Extended Memory repos), transient `work/<slug>/` and `work/plan/<task-id>/` folders are pruned so stale trajectories do not linger.
- **Breaking Shared Blind Spots:** Because `Maker` and `Cold Critic` share a base model, they can share a blind spot. In Tier 3 tasks (by default) and in Tier 2 pre-escalation checks (when deadlocked on an external/technical question), a cold retiring **`Scouter`** injects external signal from inferred spaces (X, GitHub, docs, papers) to break the shared blind spot before escalating to the human; post-run **`Recap` (`/recap`)** audits what remains.
- **Skill sprawl:** "Fix the process" adds instructions over time, so skills need regular pruning during `/recap`. Pruning is the one routine fix that does not replace a decision.

### 7.7 Glossary

- **Decision:** A choice made by the human. Bots are delegated tasks, never decisions.
- **House rule:** Logical coherence (`/ontological-clarity`), the one rule every bot follows: everything derives from one premise.
- **Task Tiers (Tier 1 / Tier 2 / Tier 3):** Deterministic classification set up front in `SKILL`s: Tier 1 (closed-endpoint script/executor only), Tier 2 (bounded subtask: `Maker` ⇄ `Cold Critic` by default), Tier 3 (creative/open-ended task: `Maker` + `Cold Scouter` + `Cold Critic` by default).
- **Pre-Escalation Gate:** Deterministic verification before interrupting the human: `Maker` debates a fresh `Cold Critic` on equal footing (and if still unresolved where external prior art applies, spins up a cold `Scouter` → reconsiders) before surfacing a decision to the human.
- **Bot:** The base model with a particular charter and skills loaded (`Bot = base model + charter + skills`); a temporary context, not a separate entity.
- **Dispatcher:** The only persistent bot; holds all triggers and starts the first bot of each chain.
- **Maker:** The clone that produces a step's artifact (the task owner).
- **Cold critic:** The clone that reviews it in both directions (catching mistakes/drift and surfacing overlooked angles), with the critic skill and no working history.
- **Cold scouter:** A single-pass context that infers the highest-signal external spaces for the task (X, GitHub, official docs, papers), writes a structured findings report, and retires immediately.
- **Full agreement:** Both sides accept a point outright under the house rule, with no compromise.
- **Sign-off:** The critic's approval of the exact final file, recorded with its `sha256`.
- **Handoff:** Transfer of a finished artifact, official once every receiver has recomputed the `sha256` and confirmed with both maker and critic.
- **Recap (`/recap`):** A cold post-task or operator-initiated review of the run folder or session surprise against the house rule, proposing surgical `SKILL`/charter improvements for human review.
- **Carry-over note:** Late information passed from one run to the next, cleared once acted on.
