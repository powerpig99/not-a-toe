# Local memory — living trackers and sleep audit

Manifest of operational `.md` files for this project. Temporary ground at project scale: held only while it speeds contact; pruned at sleep. The disposable map is `docs/local.graph.json` (never hand-edit; regenerate after sleep).

| Related | Path |
|---------|------|
| Skill sleep (framework store graph) | `~/.claude/skills/ontological-clarity/` · `node project-store-graph.mjs` |
| Project local graph | `node scripts/project-local-graph.mjs` → `docs/local.graph.json` |
| Claude project memory | `~/.claude/projects/-Users-jingliang-Projects-not-a-toe/memory/MEMORY.md` |

## Principle

**One fact, one home.** Living trackers own their domain. `MEMORY.md` holds only what is not already in a tracker (resume cursor, rare project-specific prefs). Sleep walks this list, updates drift, prunes duplicates into the owner tracker, regenerates the local graph.

## Living trackers (audit set)

| ID | Path | Owns |
|----|------|------|
| `posts` | [`content/posts/README.md`](../content/posts/README.md) | Authoring contract, voice, cross-links, ship checklist |
| `format` | [`docs/essay-format.md`](essay-format.md) | LLM copy-paste format prompt only |
| `export` | [`docs/export-for-substack.md`](export-for-substack.md) | Absolute-link projection, Substack paste |
| `export-x` | [`docs/export-for-x-article.md`](export-for-x-article.md) | X Article content_state projection + draft/publish |
| `export-stub` | [`export/README.md`](../export/README.md) | Pointer only — not a second export guide |
| `covers` | [`assets/covers/STYLES.md`](../assets/covers/STYLES.md) | Cover style families, inventory, differentiation rule |
| `root` | [`README.md`](../README.md) | Index of guides + minimal authoring summary |
| `local` | [`docs/local-memory.md`](local-memory.md) | This manifest + sleep audit steps |
| `memory` | Claude `memory/MEMORY.md` (outside repo) | Resume cursor, non-derivable prefs only |

Essay bodies under `content/posts/*.md` are **content**, not trackers. Sleep does not rewrite essays for inventory hygiene; it may note cover/style inventory drift against `assets/covers/`.

## Sleep audit procedure

Entered with project `/sleep` (or when sleep residue is operational). Operator call only.

1. **Load graph** — `docs/local.graph.json` if present (speed); else walk the table above.
2. **Per tracker** — open file; for each claim that is a fact about the repo (paths, commands, counts, inventories):
   - Verify against filesystem / scripts.
   - Fix drift in the **owner** tracker only.
   - If the same fact appears in two trackers, keep the owner; replace the other with a one-line pointer.
3. **MEMORY.md** — drop anything now owned by a tracker; keep resume + prefs that cannot be re-derived.
4. **Covers inventory** — if `assets/covers/*.jpg` and STYLES inventory disagree, update STYLES (owner).
5. **Regenerate graphs**

   ```bash
   node scripts/project-local-graph.mjs
   # framework store, from skill dir:
   node ~/.claude/skills/ontological-clarity/project-store-graph.mjs
   ```

6. **Vital sign** — report net length change on trackers (excluding inventory rows that merely list new world residue) and whether MEMORY shrank.

## Prune rules

| Keep | Prune / move |
|------|----------------|
| Domain-specific workflow in its tracker | Duplicate workflow prose in MEMORY or root README |
| Inventory tables that list real covers/posts | Invented second inventories |
| Relative-link rule in posts + format | Absolute site URLs copied into `content/posts/` |
| Export script usage in export doc | Hand-maintained list of exported slugs in git |
| Resume: goal / status / pending | Session narrative or essay summaries in MEMORY |

## Graph

`scripts/project-local-graph.mjs` builds nodes (trackers, MEMORY anchors, key scripts) and edges (`owns`, `points_to`, `implements`). Projection only — not ground. After sleep, regenerate; discard freely if stale.

```bash
node scripts/project-local-graph.mjs           # docs/local.graph.json
node scripts/project-local-graph.mjs --stdout
node scripts/project-local-graph.mjs --mermaid # docs/local.graph.mmd
```
