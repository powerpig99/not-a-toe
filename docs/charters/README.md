# Role Charters

> **Generic specification:** [`docs/wave-refinement-plan.md`](../wave-refinement-plan.md)  
> **Runtime registration:** [`docs/adapters/antigravity.md`](../adapters/antigravity.md), [`docs/adapters/claude-code.md`](../adapters/claude-code.md)

One file per role holds that role's charter, the text a runtime loads into a fresh context to start the bot (`Bot = base model + charter + skills`, plan §1). The charters are runtime-neutral: they name the house rule only as the ontological-clarity skill and name tools by what they do. Each adapter maps those names to its own primitives, tool names and paths, and registers each role with its runtime; no charter text lives in an adapter.

Tool words each adapter maps: **the ontological-clarity skill** (the house-rule file as its runtime reaches it), **web search** and **URL fetch** (open-internet tools), **reading the image files directly** (a multimodal file read of a rendered still or contact sheet), and **routed by the Dispatcher** (the runtime's way of sending a debate turn to a running role).

## Essay pipeline (plan §3, §4.3, §4.5)

- [`drafter`](drafter.md), [`critic`](critic.md), [`translator`](translator.md), [`stylist`](stylist.md), [`recap`](recap.md), [`batch-dispatcher`](batch-dispatcher.md)

## Orthogonal Planning Cycle (plan §6)

- [`planner`](planner.md), [`scouter`](scouter.md), [`evaluator`](evaluator.md)

## Media (plan §8)

No media charters: since 2026-10-30 media are made and published on Grok Bot, whose bots carry their own charters there, and the Mac-side embed step (`/media <slug>`, the `media` skill) is Tier 1 in the main session. The retired local media charters (`script-*`, `audio-*`, `infographic-*`, `film-*`, `publish*`) remain in git history.
