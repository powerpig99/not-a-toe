# Claude Code Implementation Plan for Event-Driven On-Demand Bot Dispatching (`/wake`, `/sleep`, `/deep-sleep`, `/scout`, and `/media`)

> **Canonical Generic Specification:** [`docs/wave-refinement-plan.md`](../wave-refinement-plan.md)  
> **Companion Essay:** [`On-Demand Contexts Keep Coherence at One Step`](../../content/posts/on-demand-contexts-keep-coherence-at-one-step.md)  
> **Runtime:** Claude Code (`Agent` tool with `subagent_type: "general-purpose"`, `run_in_background`, `SendMessage(to: "<agentId>")`, `Read` multimodal vision, `WebSearch`, `WebFetch`, `AskUserQuestion`)  
> **Scope:** Primary runtime for in-house local media production (`/media <slug>`), plus `/scout` and `/recap` across `/Users/jingliang/Projects/*`. Living Book authoring and memory consolidation (`/wake`, `/draft`, `/sleep`, `/deep-sleep`) run in Antigravity ([`docs/adapters/antigravity.md`](antigravity.md)) by default and are invoked in Claude Code only when explicitly requested by the Operator.  
> **Skills:** Claude Code reaches each project skill through the symlink `~/.claude/skills/<name>` → `~/.grok/skills/<name>`, and the house rule through `~/.claude/skills/ontological-clarity` → `~/.grok/skills/ontological-clarity` → `/Users/jingliang/Projects/ontological-clarity`.

---

## 1. Mapping Generic Workflow Roles to Claude Code Native Primitives

In Claude Code, each **Bot** (`base model + charter + skills`) is spawned on demand as an isolated subagent via the **`Agent` tool** (`subagent_type: "general-purpose"`, without model downgrading per `~/.claude/CLAUDE.md` *"No model switching mid-session"*). Multi-round peer debate (`Maker` ⇄ `Cold Critic` or `Planner` ⇄ `Evaluator`) routes turns back to the same subagent instance via `SendMessage(to: "<agentId>")` (carrying only a `STATUS:` line pointing to the file where the peer or Operator wrote; never messaging a subagent while it is still running), and a Bot is retired simply by dropping its `agentId` once its `sha256` handoff is confirmed. The **Main Agent** (the active Claude Code session with the Operator) acts as the deterministic **`Dispatcher` & `Assembler`**: one dispatcher level only (never spawning an intermediate node-runner or resume-runner subagent), keeping `running subagents <= W`, reporting any stalled subagent to the Operator rather than re-spawning a duplicate on the same files, and never treating harness interruption labels (`[Request interrupted by user]`) as Operator decisions unless the Operator states a decision in plain words.

> **Central Invariant:** **Only tasks are delegated to subagents; decisions always return to the Human Operator.** No deadline rule or watchdog stands in for human judgment on unresolved disagreements (`HOLD`), stalls, crashes, or `sha256` handoff mismatches.
>
> **Deterministic Task Tiers & Pre-Escalation Gate (Set Up Front in `SKILL`s, Audited by `/recap`):**
> - **Tier 1 (Deterministic Execution — Script / Single Executor Only):** Closed-endpoint commands (`interleave-post.py`, `check-signoffs.py`, `audit-post.py`, `audit-book.py`, `build.mjs`, `project-posts-graph.mjs`, `watch-deploy.sh`, the media tools in `wave-refinement-plan.md` §8.2, `sha256` checks, killing a confirmed-stuck read-only process) contract the decision space and never spawn `critic` or `scouter`.
> - **Tier 2 (Bounded Subtask — `Maker` ⇄ `Cold Critic` by Default):** Non-trivial subtasks (`script-drafter` ⇄ `script-critic`, `audio-builder` ⇄ `audio-critic`, `infographic-maker` ⇄ `infographic-critic`, `film-maker` ⇄ `film-critic`, `drafter` ⇄ `critic`, `translator` ⇄ `stylist`, bounded code subtasks) always pair with a cold critic in both directions.
> - **Tier 3 (Creative / Open-Ended Task — `Maker/Planner` + `Cold Scouter` + `Cold Critic/Evaluator` by Default):** Runs at the start of creative work (`/scout` / `/orthogonal-plan`, the film style pick in `studio/post/<slug>/wip/film/scout.md`, and `/wake` Stage 0 in `work/_wake/scout.md`).
> - **Pre-Escalation Verification Gate:** Whenever a Tier 2 or Tier 3 task owner believes a choice requires Operator intervention, it first debates a fresh `critic` on equal footing, and if maker and critic still cannot reach full agreement, runs a cold, retiring `scouter` on a neutral `QUESTION:` in `scout-<suffix>.md` beside the debate file (`"nothing relevant"` counts as a finding) and reconsiders with `critic` before interrupting the Operator.
> - **Post-Task & On-Demand `/recap`:** Runs at task conclusion or on Operator call (`/recap`) to audit the trace against `/ontological-clarity` and propose surgical `SKILL`/charter updates, settled per `wave-refinement-plan.md` §4.5.

| Generic Stage / Role | Claude Code Realization | Context & Lifecycle |
| :--- | :--- | :--- |
| **Stage 0 (`/wake` Probe & Settled Verdict)** | **Main Agent Session** (`AskUserQuestion` or direct chat) | Probes for the 4 waking materials (Spark, Source, AI/X Thread, Initial Draft). Fetches `x.com/.../status/<id>` via `curl -sL "https://cdn.syndication.twimg.com/tweet-result?id=<id>&token=a"` or `api.fxtwitter.com`, and `grok.com/share/<id>` via `curl -sL "https://grok.com/rest/app-chat/share_links/<id>"`. Runs a cold, retiring `scouter` on `work/_wake/scout.md` (`work/_wake/research.md`), evaluates against `content/book/index-of-premises.md` & `content/posts/`, and settles `NEW POST (N)` / `REFINEMENT` / `DROP` with a fresh cold-critic `Agent`; the Operator hears only a `HOLD`. |
| **Stage 1 Maker (`Drafter`)** | `Agent(subagent_type="general-purpose")` per post (`drafter_agent_id`) | Fresh subagent context per post. For an existing post, first splits `content/posts/<slug>.md` via `python3 scripts/interleave-post.py --split <slug>`. Loads `~/.claude/skills/ontological-clarity/SKILL.md`. Writes `work/<slug>/en.md` and `work/<slug>/notes.md`. |
| **Stage 1 Cold Critic (`Critic`)** | `Agent(subagent_type="general-purpose")` per post (`critic_agent_id`) | Guaranteed cold read: fresh subagent context without `drafter_agent_id`'s chain of thought. Reads `work/<slug>/en.md`, `~/.claude/skills/ontological-clarity/SKILL.md`, and `studio/kits/shared/review-method.md`. Writes `P1..Pn` (or `CRITIC: confirmed`) to `work/<slug>/debate-en.md`. |
| **Stage 1 Debate & `sha256` Handoff (`Drafter` ⇄ `Critic`)** | `SendMessage(to=drafter_agent_id)` ⇄ `SendMessage(to=critic_agent_id)` routed by Main Agent | Equal-footed debate under `/ontological-clarity` until `critic_agent_id` signs off on `work/<slug>/en.md` and its `sha256`, and `drafter_agent_id` completes the handoff checklist. Once `translator_agent_id` confirms the `sha256` of `en.md`, `drafter_agent_id` and `critic_agent_id` are never messaged again (retired). |
| **Stage 2 Maker (`Translator`)** | `Agent(subagent_type="general-purpose")` per post (`translator_agent_id`) | Started **only after** `critic_agent_id` signs off `work/<slug>/en.md` with its `sha256`. First recomputes and confirms the `sha256` of `work/<slug>/en.md`, then translates locked `en.md` to `work/<slug>/zh.md`. |
| **Stage 2 Cold Critic (`Stylist`)** | `Agent(subagent_type="general-purpose")` per post (`stylist_agent_id`) | Cold-reads `work/<slug>/zh.md` first for native Chinese cadence & vocabulary hygiene, then checks 1:1 alignment against locked `work/<slug>/en.md`. Logs `S1..Sn` (or `STYLIST: confirmed` with `sha256` and `source_sha256`) in `work/<slug>/debate-zh.md`. |
| **Stage 2 Debate & `sha256` Handoff (`Translator` ⇄ `Stylist`)** | `SendMessage(to=translator_agent_id)` ⇄ `SendMessage(to=stylist_agent_id)` routed by Main Agent | Equal-footed debate until `stylist_agent_id` signs off on `work/<slug>/zh.md`, its `sha256`, and `source_sha256`, and `translator_agent_id` completes the handoff checklist. |
| **Cover Art (New Post `N`)** | Nano Banana through Antigravity: `studio/kits/shared/bin/agy.sh new-conversation --model=flash "<prompt naming the 1344×576 JPEG target path>"`; backup `python3 scripts/generate-cover.py <slug> --prompt "..."` | Generates ultra-wide 21:9 (`1344×576`) cover art at `assets/covers/<slug>.jpg` and registers in `assets/covers/STYLES.md`. |
| **Post-Run `Recap` (`recap`)** | `Agent(subagent_type="general-purpose")` (`recap_agent_id`) | Fresh subagent context reading the completed run folder (`work/<slug>/`, `work/plan/<task-id>/`, or `studio/post/<slug>/`) against `~/.claude/skills/ontological-clarity/SKILL.md` and writing `recap.md`. |
| **Stage 3 (`Dispatcher` / `Assembler`)** | **Main Agent Session** | Runs `python3 scripts/check-signoffs.py <slug>`, runs `python3 scripts/interleave-post.py <slug>`, performs cross-streamline book/anchor sync, runs `audit-post.py`, `audit-book.py`, `build.mjs`, `project-posts-graph.mjs`, stages tracked paths (`git add content/ data/ assets/`), commits/pushes, runs `bash scripts/watch-deploy.sh`, verifies live HTTP 200, appends a new post `N` to `work/wave.md` as a pending `/sleep` origin, and deletes `work/<slug>/` once its `recap` is settled (`wave-refinement-plan.md` §4.5). |

---

## 2. Subagent Charter Templates (`Agent` Prompts for `/media`, `/scout`, `/recap`, and Post Roles)

When spawning any role via Claude Code's `Agent` tool:
- Pass the `## Charter` block of the role's runtime-neutral charter file in [`docs/charters/`](../charters/), the house-rule path (`~/.claude/skills/ontological-clarity/SKILL.md`), and the node facts (slug, layer, upstream parent slugs with commits, work folder)—nothing more. Map tool words: **the ontological-clarity skill** → `~/.claude/skills/ontological-clarity/SKILL.md`; **web search** / **URL fetch** → `WebSearch` / `WebFetch`; **reading the image files directly** → `Read`; **routed by the Dispatcher** → `SendMessage(to: "<agentId>")`.
- Keep `running subagents <= W`, each isolated to its own working directory.
- For **`Planner` / `Evaluator` / `Drafter` / `Critic` / `Translator` / `Stylist`**, instruct the subagent **not** to call `WebSearch` or `WebFetch`; only **`Scouter`** may use `WebSearch`, `WebFetch`, and external `curl` lookups.
- Enforce **single-line `STATUS:` pointer returns** (`STATUS: ... <path> [sha256=<hash>]`) so the Main Agent's context window never accumulates intermediate subagent reasoning or raw search results.

---

## 3. Claude Code Realization of the Local Media Production Pipeline (`/media <slug>`)

Generic agentic-system-agnostic specification: [`docs/wave-refinement-plan.md` §8](../wave-refinement-plan.md).

### 3.1 Role-to-Primitive Mapping (`studio/post/<slug>/`)

| Generic Role (`wave-refinement-plan.md` §8) | Claude Code Primitive | Parallelism & Multimodal Tools |
| --- | --- | --- |
| **Media Dispatcher** | **Main Agent Session** | Initializes `studio/post/<slug>/{raw,wip,final}/`, routes `STATUS:` tokens, runs Wave 3 (export, publish by default, build) per §8.2. |
| **`script-drafter` ⇄ `script-critic`** | Two isolated `Task(subagent_type="general-purpose")` instances (`script_drafter_id`, `script_critic_id`), debated via `resume` | Wave 1 per §8.2: drafts and cold-audits in `wip/scripts/`, locks `final/scripts/` with `sha256`. |
| **`audio-builder` ⇄ `audio-critic`** | Spawned in parallel in Wave 2 (`run_in_background: true` or parallel `Task` tool calls in one turn) | Stream 2A per §8.2, via `Bash`; locks `final/audio/`. |
| **`infographic-maker` ⇄ `infographic-critic`** | Spawned in parallel in Wave 2 (`run_in_background: true` or parallel `Task` tool calls in one turn) | Stream 2B per §8.2; both Maker and Cold Critic inspect the rendered stills directly with Claude Code's multimodal **`Read`** tool; locks `final/infographics/`. |
| **`film-maker` ⇄ `film-critic`** | Spawned in parallel in Wave 2 (`run_in_background: true` or parallel `Task` tool calls in one turn) | Stream 2C per §8.2; contact sheets inspected with Claude Code's multimodal **`Read`** tool; locks `final/film/`. |

### 3.2 Subagent Charter Prompts for `/media <slug>`

Use the 8 media charters (`script-drafter`, `script-critic`, `audio-builder`, `audio-critic`, `infographic-maker`, `infographic-critic`, `film-maker`, `film-critic`) in [`docs/charters/`](../charters/), with the shared media conventions of [`docs/charters/README.md`](../charters/README.md) and the tool-word mapping of §2.
