# Local memory — living trackers and sleep audit

Manifest of operational `.md` files for this project. Temporary ground at project scale: held only while it speeds contact; pruned at sleep. Disposable maps: `docs/local.graph.json` (trackers) and `docs/posts.graph.json` (essay lattice). Never hand-edit either; regenerate after sleep.

| Related | Path |
|---------|------|
| Skill sleep (framework store graph) | `~/.grok/skills/ontological-clarity/` (active) · mirror `~/.claude/skills/ontological-clarity/` · `node project-store-graph.mjs` |
| Project local graph (trackers) | `node scripts/project-local-graph.mjs` → `docs/local.graph.json` |
| Posts lattice (essay cross-links) | `node scripts/project-posts-graph.mjs` → `docs/posts.graph.json` |
| Claude project memory | `~/.claude/projects/-Users-jingliang-Projects-not-a-toe/memory/MEMORY.md` |

## Principle

**One fact, one home.** Living trackers own their domain. `MEMORY.md` holds only what is not already in a tracker (resume cursor, rare project-specific prefs). Sleep walks this list, updates drift, prunes duplicates into the owner tracker, regenerates graphs.

**Essay relations:** cross-links in `content/posts/*.md` are the only durable relation store (`[text](../other-slug/)`). The posts graph is a disposable projection of those links — never a second inventory.

## Living trackers (audit set)

| ID | Path | Owns |
|----|------|------|
| `posts` | [`content/posts/README.md`](../content/posts/README.md) | Authoring contract, voice, cross-links, living-update, ship checklist |
| `format` | [`docs/essay-format.md`](essay-format.md) | LLM copy-paste format prompt only |
| `export` | [`docs/export-for-substack.md`](export-for-substack.md) | Absolute-link projection, Substack paste |
| `export-x` | [`docs/export-for-x-article.md`](export-for-x-article.md) | X Article content_state projection + draft/publish |
| `export-stub` | [`export/README.md`](../export/README.md) | Pointer only — not a second export guide |
| `covers` | [`assets/covers/STYLES.md`](../assets/covers/STYLES.md) | Cover style families, inventory, differentiation rule |
| `root` | [`README.md`](../README.md) | Index of guides + minimal authoring summary |
| `local` | [`docs/local-memory.md`](local-memory.md) | This manifest + sleep audit steps |
| `memory` | Claude `memory/MEMORY.md` (outside repo) | Resume cursor, non-derivable prefs only |

Essay bodies under `content/posts/*.md` are **content**, not trackers. Sleep does not rewrite essays for inventory hygiene. It may run a **related-post currency pass** (below) when new or changed posts appear, and may note cover/style inventory drift against `assets/covers/`.

## Sleep audit procedure

Entered with project `/sleep` (or when sleep residue is operational). Operator call only.

1. **Load graphs** — `docs/local.graph.json` and `docs/posts.graph.json` if present (speed); else walk the tracker table and regenerate posts graph.
2. **Per tracker** — open file; for each claim that is a fact about the repo (paths, commands, counts, inventories):
   - Verify against filesystem / scripts.
   - Fix drift in the **owner** tracker only.
   - If the same fact appears in two trackers, keep the owner; replace the other with a one-line pointer.
3. **MEMORY.md** — drop anything now owned by a tracker; keep resume + prefs that cannot be re-derived.
4. **Covers inventory** — if `assets/covers/*.jpg` and STYLES inventory disagree, update STYLES (owner).
5. **Posts lattice (living essays)** — currency pass, not inventory rewrite:
   1. Capture prior posts graph (already on disk), then regenerate:

      ```bash
      node scripts/project-posts-graph.mjs --diff   # seeds + 1-hop review sets (uses prior JSON)
      node scripts/project-posts-graph.mjs           # write fresh docs/posts.graph.json
      ```

      Or inspect one seed: `node scripts/project-posts-graph.mjs --neighbors <slug>`.
   2. **Seeds** — new or hash-changed slugs under `content/posts/` (from `--diff`, or git since last sleep). Cap attention; do not re-walk the whole corpus.
   3. **Neighbor set** — for each seed, 1-hop: `links_out` + inbound citers. Cap total neighbors reviewed per sleep (e.g. ≤15), prioritizing shared geometry over hub bulk.
   4. **Review each neighbor** (read; no silent mass rewrite):
      - Does the seed’s cut make an existing claim stale or incomplete on the **same** axis?
      - Is a **single pointer clause** enough? If yes, add `[text](../seed-slug/)`. If the paragraph would summarize the seed, stop.
      - Broken `../slug/` → fix immediately (lint).
      - Do **not** add reverse links by default; only when the older post’s own cut is clarified by naming the newer face.
      - One-way edges are normal. Isolation can be correct.
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
- if same geometry and no pointer, add one clause + relative link
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
