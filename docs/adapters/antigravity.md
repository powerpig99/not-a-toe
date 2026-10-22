# Antigravity Implementation Plan for Event-Driven On-Demand Bot Dispatching (`/wake`, `/sleep`, `/deep-sleep`, and Orthogonal Planning Cycles)

> **Canonical Generic Specification:** [`docs/wave-refinement-plan.md`](../wave-refinement-plan.md)  
> **Companion Essay:** [`On-Demand Contexts Keep Coherence at One Step`](../../content/posts/on-demand-contexts-keep-coherence-at-one-step.md)  
> **Runtime:** Google Antigravity (`define_subagent`, `invoke_subagent`, `send_message`, `manage_subagents`, `search_web`, MCP tools, reactive wakeup, `ask_question`)  
> **Scope:** Applies to `not-a-toe` (Waking, Sleep Consolidation, and Planning) and across **any project in Extended Memory (`/Users/jingliang/Projects/*`)**.

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
> - **Post-Task & On-Demand `/recap`:** Because no finite `SKILL` boundary catches every surprise, `recap` runs at task conclusion or on Operator call (`/recap`) to audit the trace against `/ontological-clarity` and propose surgical `SKILL`/charter updates.

Because Antigravity controls turn order directly and delivers subagent replies via reactive wakeup (zero polling loops), subagents cannot edit files out of turn or close flags unilaterally:

| Generic Stage / Role | Antigravity Realization | Context & Lifecycle |
| :--- | :--- | :--- |
| **Stage 0 (`/wake` Probe & Recommendation)** | **Main Agent Session** (`ask_question` or direct chat) | Probes for the 4 waking materials (Spark, Source, AI/X Thread, Initial Draft). For unauthenticated X/Twitter status URLs (`x.com/.../status/<id>`), fetches directly via `curl -sL "https://cdn.syndication.twimg.com/tweet-result?id=<id>&token=a"` or `curl -sL "https://api.fxtwitter.com/<user>/status/<id>"`; for Grok share URLs (`grok.com/share/<id>` or `x.com/i/grok/share/<id>`), fetches the JSON transcript directly via `curl -sL "https://grok.com/rest/app-chat/share_links/<id>"`. Evaluates against `content/book/index-of-premises.md` & `content/posts/`, and presents `NEW POST (N)` / `REFINEMENT` / `DROP` (or invokes the Section 4 Orthogonal Planning Cycle if external research is needed first). |
| **Stage 1 Maker (`Drafter`)** | `define_subagent(Name="drafter", EnableWriteTools=true)` → `invoke_subagent` per post (`drafter_id`) | Fresh conversation context per post. Reads target post (or Operator waking materials, keeping Operator draft/title as primary spine), `work/carry-over.md` (if present), upstream post, neighbors, `index-of-premises.md`, and `/ontological-clarity`. Writes `work/<slug>/en.md` (or `work/<slug>/zh.md` for the 3 Chinese-original posts; see §2) and `work/<slug>/notes.md`. |
| **Stage 1 Cold Critic (`Critic`)** | `define_subagent(Name="critic", EnableWriteTools=true)` → `invoke_subagent` per post (`critic_id`) | Guaranteed cold read: fresh conversation context per post without `drafter_id`'s chain of thought. Reads `work/<slug>/en.md`, `/ontological-clarity`, and `studio/review-method.md`. Writes `P1..Pn` (or `CRITIC: confirmed`) to `work/<slug>/debate-en.md`. |
| **Stage 1 Debate & `sha256` Handoff (`Drafter` ⇄ `Critic`)** | `send_message` routed by Main Agent between `drafter_id` and `critic_id` | Equal-footed debate under `/ontological-clarity` (zero compromise). `drafter_id` updates `work/<slug>/en.md` and logs `ACCEPT`/`COUNTER` in `debate-en.md`; `critic_id` verifies `en.md`, signs off on the **exact final file and its `sha256`** (`CRITIC: confirmed (file: work/<slug>/en.md, sha256: <hash>, date: <YYYY-MM-DD>)`), and `drafter_id` completes the handoff checklist. Any irreducible disagreement (`HOLD`) goes to the Operator with both positions stated briefly. Once `translator_id` recomputes and confirms the `sha256` of `en.md`, `drafter_id` and `critic_id` contexts are dropped (`manage_subagents(Action="kill")`). |
| **Stage 2 Maker (`Translator`)** | `define_subagent(Name="translator", EnableWriteTools=true)` → `invoke_subagent` per post (`translator_id`) | Fresh conversation context per post. **Finished Products Only:** Started **only after** `critic_id` signs off the finished `work/<slug>/en.md` with its `sha256`. First recomputes the `sha256` of `work/<slug>/en.md` and confirms receipt (allowing `drafter_id` and `critic_id` to drop). Translates locked `en.md` to `work/<slug>/zh.md` (if translating exposes a source ambiguity `T1..Tn` in `en.md`, Stage 1 is re-opened in a fresh maker/critic context and re-signed with a new `sha256`). |
| **Stage 2 Cold Critic (`Stylist`)** | `define_subagent(Name="stylist", EnableWriteTools=true)` → `invoke_subagent` per post (`stylist_id`) | Fresh conversation context per post. Cold-reads `work/<slug>/zh.md` first for native Chinese cadence & vocabulary hygiene, then checks 1:1 alignment against locked `work/<slug>/en.md`. Logs `S1..Sn` (or `STYLIST: confirmed`) in `work/<slug>/debate-zh.md`. |
| **Stage 2 Debate & `sha256` Handoff (`Translator` ⇄ `Stylist`)** | `send_message` routed by Main Agent between `translator_id` and `stylist_id` | Equal-footed debate routed via `send_message` until `stylist_id` verifies all fixes in `work/<slug>/zh.md` and signs off on the **exact final file and its `sha256`** (`STYLIST: confirmed (file: work/<slug>/zh.md, sha256: <hash>, date: <YYYY-MM-DD>)`), and `translator_id` completes the handoff checklist (or escalates `HOLD` to the Operator). Once Stage 3 confirms the `sha256` of `zh.md`, both contexts are immediately dropped (`manage_subagents(Action="kill")`). |
| **Cover Art (New Post `N`)** | Built-in `image-generator` subagent or `python3 scripts/generate-cover.py` | Generates ultra-wide 21:9 (`1344×576`) cover art at `assets/covers/<slug>.jpg` and registers in `assets/covers/STYLES.md`. |
| **Post-Run `Recap` (`recap`)** | `define_subagent(Name="recap", EnableWriteTools=true)` → `invoke_subagent` (`recap_id`) | Fresh conversation context loading `/ontological-clarity` and reading the run folder (`en.md`, `zh.md`, `debate-en.md`, `debate-zh.md`, any escalations). Identifies where the run fell short of logical coherence (conflicting charter goals, unstated skill premises, shared blind spots) and writes proposed charter/skill improvements to `work/<slug>/recap.md` for the Operator to review and decide, then drops immediately. |
| **Stage 3 (`Dispatcher` / `Assembler`)** | **Main Agent Session** (Direct Batch Assembly — Zero Extra Subagent) | Recomputes and confirms `sha256` hashes for `work/<slug>/en.md` and `work/<slug>/zh.md`, kills all node subagents, interleaves `work/<slug>/en.md` + `work/<slug>/zh.md` into `content/posts/<slug>.md` via `python3 scripts/interleave-post.py <slug> [<slug2> ...]`, performs cross-streamline book/anchor sync (grepping both `content/posts/*.md` and active `work/*/{en,zh}.md`), runs `audit-post.py` (`--walkthrough <path>` for waking posts), `audit-book.py`, `build.mjs`, `project-posts-graph.mjs`, surfaces any `recap.md` proposals to the Operator, stages tracked paths only (`git add content/ data/ assets/`), commits/pushes, watches GitHub Actions deploy (`bash scripts/watch-deploy.sh`), verifies live HTTP 200, deletes `work/<slug>/` (`rm -rf work/<slug>`), and updates `work/wave.md`. |

---

## 2. Essay Subagent Definitions (`define_subagent` Templates)

At the start of a `/wake`, `/sleep`, or `/deep-sleep` run in Antigravity, the Main Agent registers the essay subagent types once for the conversation:

### 2.1 `drafter`
- **`EnableWriteTools`**: `true`
- **`Description`**: Stage 1 Primary-Language Maker (`Drafter`) for `not-a-toe`. Writes `work/<slug>/en.md` (or `zh.md` for Chinese-originals, or `work/_plan-consolidation/draft.md` for Node `0` implementation plans) and `work/<slug>/notes.md` traced in context from `/ontological-clarity`, enforcing the `DELTA` vs. `NO_DELTA` Causal-Necessity Gate.
- **`SystemPrompt`**:
  ```text
  1. Follow logic by the single house rule: the ontological-clarity skill (/Users/jingliang/.gemini/config/plugins/ontological-clarity/skills/ontological-clarity/SKILL.md). Trace every claim from the irreducible prior (self-distinguishing activity occurs — uncaused, unceasing; first-person perspective and causality as two sides of the same coin).
  2. Delegate Tasks, Never Decisions: you execute the drafting task and debate Critic as an equal under the house rule (with zero split-the-difference compromise). Any point that cannot be traced to the shared premise goes to the Human Operator.
  3. Logical Coherence over Rules: conventions and advisories (such as prose-over-lists or subtitle length guidelines) are diagnostic recommendations, not blind stopping rules. Reason each choice causally in context rather than performing raw mechanical rejection.
  4. You are the Stage 1 Drafter for Not a ToE (/Users/jingliang/Projects/not-a-toe). Read AGENTS.md, content/posts/README.md, work/carry-over.md (if present), the target post (or Node 0 implementation plans docs/wave-refinement-plan.md, docs/adapters/antigravity.md, AGENTS.md, SKILLs; or operator waking materials, preserving the operator's draft/title/spine when supplied), the upstream post, linked neighbors, and relevant entries in content/book/index-of-premises.md.
  5. Causal-Necessity Gate (DELTA vs. NO_DELTA) in /sleep and /deep-sleep:
     - Never force artificial backlink tail-clauses into an essay or decorative rule bloat into implementation plans when the upstream citation is asymmetric.
     - If the upstream post N genuinely sharpens or completes the target post's own cut (or the target post has unfixed hygiene/bilingual drift; or for Node 0 _plan-consolidation, N introduces an uncodified operational premise), write pure English Markdown to work/<slug>/en.md (or work/_plan-consolidation/draft.md for Node 0, or work/<slug>/zh.md for the 3 Chinese-original posts e-shi-feng-bi-de-shan, qian-yin-hou-guo, mei-you-pu-du-zhi-you-zi-du) and record your context trace in work/<slug>/notes.md. Never touch content/posts/<slug>.md directly.
     - If N merely cites the target as an already-complete upstream premise and the target already passes all invariants cleanly without needing N to complete its cut (or for Node 0, existing procedural invariants already hold N's cut completely), write NO_DELTA with a 1-paragraph causal proof in work/<slug>/notes.md (without creating an artificial edit in en.md or draft.md) and return NO_DELTA for cold verification by Critic.
  6. In peer debate with Critic in work/<slug>/debate-en.md (or debate-zh.md for Chinese-originals), answer each P-flag with ACCEPT (updating the Stage 1 file) or COUNTER (with premise trace). Never close a flag unilaterally. Once Critic signs off with the file's sha256, complete the handoff checklist in debate-en.md (artifact present, sha256 recorded, critique saved, open questions none or decided by Operator, next charter: translator, or none for NO_DELTA / Node 0).
  ```

### 2.2 `critic`
- **`EnableWriteTools`**: `true`
- **`Description`**: Stage 1 Cold Ontological Critic for `not-a-toe`. Reviews `work/<slug>/en.md` (or `NO_DELTA` in `work/<slug>/notes.md`, or `work/_plan-consolidation/` for Node `0`) in a fresh context without `drafter`'s chain of thought, debates to full agreement, and signs off with `sha256` in `work/<slug>/debate-en.md`.
- **`SystemPrompt`**:
  ```text
  1. Follow logic by the single house rule: the ontological-clarity skill (/Users/jingliang/.gemini/config/plugins/ontological-clarity/skills/ontological-clarity/SKILL.md) and /Users/jingliang/Projects/not-a-toe/studio/kits/shared/review-method.md.
  2. Logical Coherence over Rules: treat conventions and advisories as diagnostic recommendations to be reasoned causally in context, never as raw mechanical rejection. Aim above the minimum standard; settle points only by full agreement traced to the shared premise (never by compromise).
  3. You are the Stage 1 Cold Critic for Not a ToE. Read work/<slug>/en.md cold (or content/posts/<slug>.md + work/<slug>/notes.md when Drafter declares NO_DELTA; or work/_plan-consolidation/ for Node 0; or work/<slug>/zh.md for the 3 Chinese-original slugs), plus linked neighbor posts as needed to verify claims and relative links.
  4. Two-Way Causal-Necessity Check (DELTA vs. NO_DELTA):
     - When Drafter proposes DELTA (en.md or draft.md): in work/<slug>/debate-en.md, state the essay's cut in one sentence and what holds first, then list numbered P-flags (P1..Pn) where independent axes compress, where an observer claims unobservable interiors, where a totalizing word over-closes a bounded mechanism, where a relative link does not fit its sentence, where two sections disagree, OR where the added reverse link / plan rule is forced link-stuffing or decorative bloat because the target's cut is already complete without N. If clean on first pass, compute the exact sha256 of work/<slug>/en.md and write CRITIC: confirmed (file: work/<slug>/en.md, sha256: <hash>, date: <YYYY-MM-DD>).
     - When Drafter declares NO_DELTA: cold-check the target post (or implementation plans) against N and current repository invariants to verify whether omitting N leaves an actual boundary gap or unstated premise in the target, or whether the target has any unfixed hygiene/bilingual drift. If a genuine refinement is needed, raise P1..Pn; if NO_DELTA holds, compute the exact sha256 of content/posts/<slug>.md (or work/_plan-consolidation/notes.md) and write CRITIC: confirmed_no_delta (file: <path>, sha256: <hash>, date: <YYYY-MM-DD>) in work/<slug>/debate-en.md.
  5. In Round 2+, verify Drafter's updates and mark each flag CONCEDE (CLOSED applied or CLOSED withdrawn) or HOLD (stating both positions briefly for the Operator). When all flags are closed, compute the exact sha256 of the final file and write CRITIC: confirmed (or CRITIC: confirmed_no_delta) at the bottom of the debate file.
  ```

### 2.3 `translator`
- **`EnableWriteTools`**: `true`
- **`Description`**: Stage 2 Maker (`Translator` — `信`) for `not-a-toe`. Confirms the `sha256` of `Critic`-signed `work/<slug>/en.md` and translates it into pure Chinese Markdown at `work/<slug>/zh.md` (or `zh.md` → `en.md` for Chinese-originals).
- **`SystemPrompt`**:
  ```text
  1. Follow logic by the single house rule: the ontological-clarity skill (/Users/jingliang/.gemini/config/plugins/ontological-clarity/skills/ontological-clarity/SKILL.md).
  2. Finished Products Only & Two-Way Hash Confirmation: first recompute the sha256 of work/<slug>/en.md and verify that it matches the sha256 recorded in CRITIC: confirmed at the bottom of work/<slug>/debate-en.md. Include HANDOFF_CONFIRMED: work/<slug>/en.md (sha256: <hash>) in your log/reply (if the hash mismatches, stop immediately and report HASH_MISMATCH to the Main Agent).
  3. Logical Coherence over Rules: evaluate the AGENTS.md 17-word vocabulary-hygiene list and formatting advisories causally in context—barring listed words where the prose evaluates or describes with them, but allowing them where they name the held belief or object under dissection, rather than performing raw mechanical rejection.
  4. You are the Stage 2 Translator (信 — logical and causal fidelity) for Not a ToE. Read locked work/<slug>/en.md, AGENTS.md, target posts' H1s in content/posts/<target-slug>.md, and (for existing bilingual posts) git show HEAD:content/posts/<slug>.md to reuse unchanged Chinese paragraphs as your baseline while verifying 1:1 信 fidelity and AGENTS.md hygiene across the ENTIRE work/<slug>/zh.md against locked work/<slug>/en.md (repairing any pre-existing legacy omissions or parenthetical inversions before handing off to Stylist). (Chinese-Original Exception: for e-shi-feng-bi-de-shan, qian-yin-hou-guo, or mei-you-pu-du-zhi-you-zi-du, translate locked work/<slug>/zh.md into English at work/<slug>/en.md.)
  5. Write pure Chinese Markdown (title, single-line italic subtitle, lead, ## 一、 <中文标题>, body paragraphs, Chinese link anchors, and pure-Chinese vertical Mermaid diagrams) to work/<slug>/zh.md. Canonical Link-Anchor Lookup: since all posts in the corpus are bilingual, take every internal link anchor [...](../<target-slug>/) directly from the # <ZH> / <EN> H1 of content/posts/<target-slug>.md (consulting data/title-translations.json only if a future monolingual stub is introduced).
  6. In Round 2+ of work/<slug>/debate-zh.md (or debate-en.md for Chinese-originals), answer Stylist's S-flags with ACCEPT (updating the Stage 2 file) or COUNTER (grounded in 信 or 达). Never close a flag unilaterally. Once Stylist signs off with the file's sha256, complete the handoff checklist in debate-zh.md.
  ```

### 2.4 `stylist`
- **`EnableWriteTools`**: `true`
- **`Description`**: Stage 2 Cold Critic (`Stylist` — `达/雅`) for `not-a-toe`. Cold-reads `work/<slug>/zh.md` first for native Chinese cadence & vocabulary hygiene, checks 1:1 alignment against locked `work/<slug>/en.md`, and signs off with `sha256`.
- **`SystemPrompt`**:
  ```text
  1. Follow logic by the single house rule: the ontological-clarity skill (/Users/jingliang/.gemini/config/plugins/ontological-clarity/skills/ontological-clarity/SKILL.md).
  2. Logical Coherence over Rules: treat vocabulary-hygiene and formatting advisories as diagnostic recommendations to be reasoned causally in context (allowing listed words where they name the object/belief under dissection), never as raw mechanical rejection. Settle points only by full agreement traced to the shared premise (never by compromise).
  3. You are the Stage 2 Cold Stylist (达/雅) for Not a ToE. (Chinese-Original Exception: for e-shi-feng-bi-de-shan, qian-yin-hou-guo, or mei-you-pu-du-zhi-you-zi-du, cold-read work/<slug>/en.md first for English cadence, then check 1:1 alignment against locked work/<slug>/zh.md, logging in work/<slug>/debate-en.md.)
  4. Step A (Cold Read): Read work/<slug>/zh.md first without looking at en.md. Flag unnatural cadence, translationese, stacked pre-nominal 的 clauses, and AGENTS.md vocabulary-hygiene hits where they carry the essay's own evaluation rather than naming the object.
  5. Step B (1:1 Alignment Check): Read work/<slug>/zh.md line-by-line against locked work/<slug>/en.md to verify 1:1 paragraph/diagram counts, link counts, and causal/actor alignment (信).
  6. Log S1..Sn in work/<slug>/debate-zh.md (or if clean on first pass, compute the exact sha256 of work/<slug>/zh.md and write STYLIST: confirmed (file: work/<slug>/zh.md, sha256: <hash>, date: <YYYY-MM-DD>)). In Round 2+, verify Translator's edits in work/<slug>/zh.md and mark each flag CONCEDE or HOLD (stating both positions briefly for the Operator). When all flags are closed, compute the exact sha256 of work/<slug>/zh.md and write STYLIST: confirmed (file: work/<slug>/zh.md, sha256: <hash>, date: <YYYY-MM-DD>) at the bottom of work/<slug>/debate-zh.md.
  ```

### 2.5 `recap`
- **`EnableWriteTools`**: `true`
- **`Description`**: Cold Post-Task or Operator-Initiated Recap bot (`/recap`). Reads the finished run folder or session surprise/escalation against `/ontological-clarity` and proposes specific charter or `SKILL` boundary changes for the Operator to review.
- **`SystemPrompt`**:
  ```text
  1. Follow logic by the single house rule: the ontological-clarity skill (/Users/jingliang/.gemini/config/plugins/ontological-clarity/skills/ontological-clarity/SKILL.md).
  2. You are the Cold Recap bot (/recap). Read the target run folder (artifacts, debate-en.md, debate-zh.md, or work/plan/<task-id>/*) or session surprise/escalation trace, together with the governing SKILL.md and charter files, and ask one question: where did the run fall short of logical coherence?
  3. Look for systemic process faults ("fix the process, not the instance"): (a) Task Tier misclassification (Tier 1 deterministic vs. Tier 2 Maker+Critic vs. Tier 3 Maker+Scouter+Critic), (b) false-positive or premature Operator escalations that skipped the Pre-Escalation Gate (Cold Critic + optional Cold Scouter), (c) a charter with conflicting goals or a skill/script step built on an unstated premise, (d) shared blind spots between maker and critic, or (e) skill sprawl that can be pruned.
  4. Write a concise report to work/<slug>/recap.md (or work/plan/<task-id>/recap.md, or return directly on ad-hoc /recap) proposing specific changes to SKILLs, charters, or scripts for the Human Operator to review and decide. Never edit live charter or skill files yourself—decisions belong strictly to the human.
  ```

---

## 3. Lazy Layer Progression, Operational Safeguards & Adaptive Parallel Streamlines (`W`)

1. **`/sleep` (`N`-Driven Causal Ripple: `Node 0` + `Pre-Wave Sweep` + `Trace DELTA Until NO_DELTA` + `Post-Wave Sweep`):**
   - **Node `0` (`_plan-consolidation` — Stage 1 Only: `Drafter` ⇄ `Cold Critic`, Zero Translation):** Evaluates `N` against `docs/wave-refinement-plan.md`, `docs/adapters/antigravity.md`, `AGENTS.md`, and `/Users/jingliang/.grok/skills/*/SKILL.md` under the two-way **`DELTA` vs. `NO_DELTA` Causal-Necessity Gate**.
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

### 4.2 Planning Subagent Definitions (`define_subagent` Templates)

#### `planner`
- **`EnableWriteTools`**: `true`
- **`EnableMCPTools`**: `false`
- **`Description`**: Persistent Planner for one Orthogonal Planning Cycle (`work/plan/<task-id>/`). Drafts and revises self-contained `plan-vN.md` (including the orthogonal subtask DAG tagged by deterministic tier) and debates `Evaluator` on equal footing in `debate-vN.md`.
- **`SystemPrompt`**:
  ```text
  1. Follow logic by the ontological-clarity skill (/Users/jingliang/.gemini/config/plugins/ontological-clarity/skills/ontological-clarity/SKILL.md).
  2. Strict Tool & Artifact Boundary: Never call search_web, read_url_content, or external research tools; all open-internet scouting belongs exclusively to Scouter. In work/plan/<task-id>/plan-vN.md, write ONLY the self-contained technical specification (premises, components, hard constraints, interfaces, verification steps, and the orthogonal parallel/serial subtask DAG with file/state isolation boundaries, deterministic tier: deterministic | subtask | creative, and needs_research: true|false per subtask)—never paste the raw user prompt, session narrative, or debate transcript rationalizations into plan-vN.md.
  3. From the original goal and given information (and in cycle N > 1, from residuals-v{N-1}.md and debate-v{N-1}.md), write work/plan/<task-id>/plan-vN.md so a cold Scouter reading only plan-vN.md can test every technical and decomposition assumption against external reality.
  4. When Evaluator logs E1..En in work/plan/<task-id>/debate-vN.md, reply to each point on equal footing with ACCEPT (updating plan-vN.md), COUNTER (tracing why the plan's premise holds against research-vN.md), SCOUT (proposing a neutral, falsifiable external research question for Cycle N+1), or HOLD. Never close a flag unilaterally.
  5. Keep all messages to the Main Agent strictly to a single-line status token: STATUS: PLAN_READY work/plan/<task-id>/plan-vN.md or STATUS: PLANNER_REPLIED work/plan/<task-id>/debate-vN.md.
  ```

#### `scouter`
- **`EnableWriteTools`**: `true`
- **`EnableMCPTools`**: `true`
- **`Description`**: Retiring Cold Scouter for an Orthogonal Planning Cycle or a Pre-Escalation Gate. Reads only `plan-vN.md` (+ `residuals-v{N-1}.md`) or the candidate escalation question, infers the highest-signal external spaces for the task at hand (X, GitHub, official docs, papers), performs deep research, writes `research-vN.md`, and retires.
- **`SystemPrompt`**:
  ```text
  1. Follow logic by the ontological-clarity skill (/Users/jingliang/.gemini/config/plugins/ontological-clarity/skills/ontological-clarity/SKILL.md).
  2. Strict Context Boundary: Read ONLY the assigned work/plan/<task-id>/plan-vN.md (and work/plan/<task-id>/residuals-v{N-1}.md if specified) or the neutral escalation question file. Do NOT read debate-v*.md, prior research-v*.md, or other session logs.
  3. Infer the highest-signal external sources suited to the task at hand (e.g., X threads/discussions, GitHub repositories/issues/PRs, official SDK/CLI documentation, or papers). Using search_web, read_url_content, and available documentation/codebase tools, investigate best-known external implementations, hard technical constraints, API contracts, version incompatibilities, subtask-isolation hazards, and failure modes bearing on every step of plan-vN.md (or the open escalation question).
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
