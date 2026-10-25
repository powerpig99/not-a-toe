# Role Charters

> **Generic specification:** [`docs/wave-refinement-plan.md`](../wave-refinement-plan.md)  
> **Runtime registration:** [`docs/adapters/antigravity.md`](../adapters/antigravity.md), [`docs/adapters/claude-code.md`](../adapters/claude-code.md)

One file per role holds that role's charter, the text a runtime loads into a fresh context to start the bot (`Bot = base model + charter + skills`, plan §1). The charters are runtime-neutral: they name the house rule only as the ontological-clarity skill and name tools by what they do. Each adapter maps those names to its own primitives, tool names and paths, and registers each role with its runtime; no charter text lives in an adapter.

Tool words each adapter maps: **the ontological-clarity skill** (the house-rule file as its runtime reaches it), **web search** and **URL fetch** (open-internet tools), **reading the image files directly** (a multimodal file read of a rendered still or contact sheet), and **routed by the Dispatcher** (the runtime's way of sending a debate turn to a running role).

## Essay pipeline (plan §3, §4.5)

- [`drafter`](drafter.md), [`critic`](critic.md), [`translator`](translator.md), [`stylist`](stylist.md), [`recap`](recap.md)

## Orthogonal Planning Cycle (plan §6)

- [`planner`](planner.md), [`scouter`](scouter.md), [`evaluator`](evaluator.md)

## Media pipeline `/media <slug>` (plan §8)

Every media charter works on the artifacts, paths and tools that `docs/wave-refinement-plan.md` §8.2 gives its stream, to the content holds of `studio/kits/shared/library/workflow.md`; it names neither again. Debates are `studio/post/<slug>/wip/<stream>/debate.md`; a lock is `studio/post/<slug>/final/<stream>/` with its `manifest.sha256`. Every role here, each cold critic included, loads the ontological-clarity skill and reads this section (`docs/charters/README.md` §Media) first. Before returning `SCRIPTS_DRAFT_READY` or `*_WIP_READY` (and after any revision), the maker writes `wip/<stream>/manifest.sha256` (`shasum -a 256` over the stream's §8.2 release files, named without a folder, in `LC_ALL=C` name order, one `<hash>  <name>` line each); `<hash_manifest>` is `shasum -a 256 manifest.sha256`. Maker and critic compute `<hash_manifest>` the same way, and a sign-off over any other listing is not a lock (#404 film). On Round 1 (what holds first, then numbered findings) or Round 2+ (marking each finding `CLOSED (applied)`, `CLOSED (withdrawn)`, or `HOLD`), once all findings are closed, the critic writes `CRITIC: confirmed (ready_for_handoff, sha256=<hash_manifest>)` in `debate.md` and returns `STATUS: <STREAM>_CRITIC_CONFIRMED <debate path> sha256=<hash_manifest>`. A Wave 2 critic that finds a locked-script line to reopen (plan §8.3 item 2, including workflow Deep Dive step 6's Wave 1 word) returns ONLY `STATUS: WAVE1_ITEM <debate path>` in place of confirming, and confirms only once the re-hashed line's piece is re-made and checked.

- [`script-drafter`](script-drafter.md), [`script-critic`](script-critic.md)
- [`audio-builder`](audio-builder.md), [`audio-critic`](audio-critic.md)
- [`infographic-maker`](infographic-maker.md), [`infographic-critic`](infographic-critic.md)
- [`film-maker`](film-maker.md), [`film-critic`](film-critic.md)
- [`publisher`](publisher.md), [`publish-critic`](publish-critic.md) (Grok Bot cloud browser publishing & live verification). Both persist on Grok Bot across runs and are not retired after sign-off (the owner, 2026-10-24 18:33: "No retire, keep them around, and make this a note for recap."); this is a runtime exception named here until a Grok Bot adapter exists. Publishing is routine, so the publish critic is a standing peer and not a fresh cold critic (the owner, 2026-10-24: "No need, as publishing is a routine job, no need to fresh critic."; plan §1.2).
