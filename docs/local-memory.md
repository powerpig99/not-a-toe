# Local memory — living trackers and sleep audit

Manifest of operational `.md` files for this project. Temporary ground at project scale: held only while it speeds contact; pruned at sleep. Disposable maps: `docs/local.graph.json` (trackers) and `docs/posts.graph.json` (essay lattice). Never hand-edit either; regenerate after sleep.

| Related | Path |
|---------|------|
| Skill sleep (framework store graph) | `~/.grok/skills/ontological-clarity/` (active) · mirror `~/.claude/skills/ontological-clarity/` · `node project-store-graph.mjs` |
| Project local graph (trackers) | `node scripts/project-local-graph.mjs` → `docs/local.graph.json` |
| Posts lattice (essay cross-links) | `node scripts/project-posts-graph.mjs` → `docs/posts.graph.json` |
| Knowledge graph (project leaf) | [`.grok/memory-graph/`](../.grok/memory-graph/README.md) · leaf of **Grok Build Memory** `~/.grok/memory-graph` · `sync` registers `project-not-a-toe` in parent · `up` / `evolve` · default method: ontological-clarity |
| Grok Build Memory (global root) | `~/.grok/memory-graph` · `projects.json` · `node ~/.grok/memory-graph/retrieval.mjs projects\|down project-not-a-toe` |
| Claude project memory | `~/.claude/projects/-Users-jingliang-Projects-not-a-toe/memory/MEMORY.md` |

## Principle

**One fact, one home.** Living trackers own their domain. `MEMORY.md` holds only what is not already in a tracker (resume cursor, rare project-specific prefs). Sleep walks this list, updates drift, prunes duplicates into the owner tracker, regenerates graphs.

**Essay relations:** cross-links in `content/posts/*.md` are the only durable relation store (`[text](../other-slug/)`). The posts graph is a disposable projection of those links — never a second inventory.

## Living trackers (audit set)

| ID | Path | Owns |
|----|------|------|
| `posts` | [`content/posts/README.md`](../content/posts/README.md) | Authoring contract, refinement workflow (surgical; draft as ground), voice, cross-links, reverse links, lattice consistency (same-axis old claims, same ship), ship checklist |
| `format` | [`docs/essay-format.md`](essay-format.md) | Site scaffold reference + LLM copy-paste prompt (not absolute ground over operator draft) |
| `export` | [`docs/export-for-substack.md`](export-for-substack.md) | Shared absolute-markdown: **generate required after live** on ship; paste is operator-only |
| `export-x` | [`docs/export-for-x-article.md`](export-for-x-article.md) | Points at shared export; Articles API parked |
| `export-stub` | [`export/README.md`](../export/README.md) | Pointer only — not a second export guide |
| `covers` | [`assets/covers/STYLES.md`](../assets/covers/STYLES.md) | Cover style families, inventory, differentiation rule |
| `root` | [`README.md`](../README.md) | Index of guides + minimal authoring summary |
| `local` | [`docs/local-memory.md`](local-memory.md) | This manifest + sleep audit steps |
| `knowledge-graph` | [`.grok/memory-graph/README.md`](../.grok/memory-graph/README.md) | Project leaf graph (parent: `~/.grok/memory-graph`); dual-write from `/sleep` when lasting; `sync` registers leaf |
| `memory` | Claude `memory/MEMORY.md` (outside repo) | Resume cursor, non-derivable prefs only |

Essay bodies under `content/posts/*.md` are **content**, not trackers — a living tracing, not a catalog of finished products. Sleep does not rewrite essays for inventory hygiene. It may run a leftover **related-post currency pass** (below) when new or changed posts appear, and may note cover/style inventory drift against `assets/covers/`. Drop-time re-tracing of same-axis old claims is owned by [`content/posts/README.md`](../content/posts/README.md) § Lattice consistency.

## Sleep audit procedure

**Pipeline:** session (perception) → **`/bridge`** working memory `memory/context.graph.json` → **`/sleep`** writes provisional packages under `memory/packages/` (living graph untouched; context left on disk; ignored by new sessions without `/resume-bridge`; next bridge replaces it) → **`/deep-sleep`** resonance-tests packages, regenerates the living graph, climbs bottom→top (+ store/trackers; dual-write to `.grok/memory-graph/`). Mid-day: bridge then `/clear` + later `/resume-bridge`. Operator call only.

1. **Load graphs** — `docs/local.graph.json` and `docs/posts.graph.json` if present (speed); else walk the tracker table and regenerate posts graph.
2. **Per tracker** — open file; for each claim that is a fact about the repo (paths, commands, counts, inventories):
   - Verify against filesystem / scripts.
   - Fix drift in the **owner** tracker only.
   - If the same fact appears in two trackers, keep the owner; replace the other with a one-line pointer.
3. **MEMORY.md** — drop anything now owned by a tracker; keep resume + prefs that cannot be re-derived.
4. **Covers inventory** — if `assets/covers/*.jpg` and STYLES inventory disagree, update STYLES (owner).
5. **Posts lattice (living tracing)** — leftover currency pass, not inventory rewrite and not the drop-time re-trace:
   1. Capture prior posts graph (already on disk), then regenerate:

      ```bash
      node scripts/project-posts-graph.mjs --diff   # seeds + 1-hop review sets (uses prior JSON)
      node scripts/project-posts-graph.mjs           # write fresh docs/posts.graph.json
      ```

      Or inspect one seed: `node scripts/project-posts-graph.mjs --neighbors <slug>`.
   2. **Seeds** — new or hash-changed slugs under `content/posts/` (from `--diff`, or git since last sleep). Cap attention; do not re-walk the whole corpus.
   3. **Neighbor set** — for each seed, 1-hop: `links_out` + inbound citers. Cap total neighbors reviewed per sleep (e.g. ≤15), prioritizing shared geometry over hub bulk.
   4. **Review each neighbor** (read; no silent mass rewrite). Drop-time lattice consistency is owned by [`content/posts/README.md`](../content/posts/README.md) § Lattice consistency — this sleep pass is a leftover catch, not the first pass:
      - Does the seed’s cut make an existing claim stale, over-closed, or incomplete on the **same** axis? If the old sentence still overclaims, **nick the old claim** — a pointer is not enough.
      - **Two-way is default:** for each outbound link from the seed, ensure the neighbor has a reverse pointer to the seed (single clause; same geometry). Add if missing.
      - Is a **single pointer clause** enough? Only when the old claim still holds and only the new face needs naming. If the paragraph would summarize the seed, stop.
      - Broken `../slug/` → fix immediately (lint).
      - Skip reverse only when the neighbor genuinely has no shared axis (rare); note the skip. Isolation is exception, not default.
   5. If prose changed and Substack/X will be updated by hand, re-export those surfaces (export trackers).
   6. If any links changed, regenerate posts graph again.
6. **Regenerate tracker / skill graphs**

   ```bash
   node scripts/project-local-graph.mjs
   # framework store, from skill dir (prefer active grok copy):
   node ~/.grok/skills/ontological-clarity/project-store-graph.mjs
   ```

7. **Vital sign** — report net length change on trackers (excluding inventory rows that merely list new world residue), whether MEMORY shrank, posts-graph `missing_targets` (must be 0), and seed/neighbor review outcome (NO_CHANGE vs pointer edits).

### Sleep prompt sketch (posts pass)

```text
Seeds: <from --diff or new slugs>
For each neighbor in 1-hop review_set:
- open content/posts/<neighbor>.md
- same-axis leftover: if the old claim is now false, over-closed, or incomplete, nick it (posts README § Lattice consistency)
- two-way default: ensure reverse pointer from neighbor → seed when shared geometry
- pointer only when the old claim still holds
- do not restate the seed essay
- regenerate: node scripts/project-posts-graph.mjs
```

## Prune rules

| Keep | Prune / move |
|------|----------------|
| Domain-specific workflow in its tracker | Duplicate workflow prose in MEMORY or root README |
| Inventory tables that list real covers/posts | Invented second inventories |
| Relative-link rule in posts + format | Absolute site URLs copied into `content/posts/` |
| Cross-links in essay prose as relation store | Hand-maintained `related:` tables or second graph ground |
| Export script usage in export doc | Hand-maintained list of exported slugs in git |
| Resume: goal / status / pending | Session narrative or essay summaries in MEMORY |

## Graphs

Two disposable projections — not ground. After sleep, regenerate; discard freely if stale.

**Trackers** — `scripts/project-local-graph.mjs`: trackers, MEMORY anchors, key scripts.

```bash
node scripts/project-local-graph.mjs           # docs/local.graph.json
node scripts/project-local-graph.mjs --stdout
node scripts/project-local-graph.mjs --mermaid # docs/local.graph.mmd
```

**Posts lattice** — `scripts/project-posts-graph.mjs`: essay nodes and `points_to` edges from relative cross-links. Does not replace prose.

```bash
node scripts/project-posts-graph.mjs              # docs/posts.graph.json
node scripts/project-posts-graph.mjs --stdout
node scripts/project-posts-graph.mjs --mermaid    # docs/posts.graph.mmd (hubs view)
node scripts/project-posts-graph.mjs --neighbors <slug>
node scripts/project-posts-graph.mjs --diff       # seeds vs prior JSON + review sets
```
