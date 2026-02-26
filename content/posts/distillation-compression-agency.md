# Distillation Doesn't Compress — It Chooses What to Lose

Distillation makes a large model's capability available in a smaller form. The promise: same performance, less cost. The pattern: the performance transfers, but the capacity that generated it doesn't — and the metric can't tell the difference.

This gets filed under "quality tradeoff" or "engineering pragmatism" — an acceptable loss for practical gain. Strip the pragmatic framing and something structural appears: distillation degrades, and the degradation is how it completes. The sharpest part: it completes a target nobody actually cares about.

Nobody building a distilled model wants "matches scores on this evaluation suite." They want the teacher's capability, cheaper. The benchmark is a proxy, and everyone knows it's a proxy. But the proxy is the only thing with a gradient, so the optimization follows it. The purpose is capability-at-lower-cost. The optimization target is benchmark-matching. The gap between purpose and target is visible from the start — and the optimization proceeds anyway, because there's nothing else to descend on.

The result: a model that matches the benchmark while losing what the benchmark couldn't measure. The degradation is real. It's just orthogonal to the metric — which is exactly why the optimization proceeds without resistance.

## The Benchmark Contains Its Own Blindness

A benchmark measures how closely output matches a target across a known task distribution. Every technique that improves this match — better training recipes, architecture search, data curation — registers as progress on this axis.

The axis has a structural limit. The fastest path to benchmark performance is fitting the benchmark distribution directly. The teacher model achieved that performance through high-dimensional capability — redundant pathways, lateral connections, capacity that never fires on any benchmark task but sustains the flexibility that *generates* benchmark-level outputs on novel tasks. Distillation says: we only need what produces the measured output.

From the benchmark's projection, the teacher's unmeasured capacity is waste. Eliminating it improves efficiency without moving the score. The distilled model isn't worse — it's *more optimized*. The loss is orthogonal to the measurement.

---

## Two Projections Collapsed Into One

The confusion comes from a forced collapse between two dimensions that don't share coordinates:

**Projection A — Performance**: How well does the model score on evaluated tasks? This is the distillation's operational axis. It has clear gradients. It optimizes.

**Projection B — Generative capacity**: Can the model produce adequate responses in territory the benchmarks didn't map? This has no gradient on the performance axis. A model that memorized the right outputs and a model that derived them through flexible internal process score identically. Capacity doesn't register.

"Same performance, smaller model" collapses these two projections. It treats performance and capacity as if they correlate. At low compression they travel together — the distilled model is still too large to have lost meaningful structure, so performance tracks capacity by accident. As compression deepens, performance holds while capacity degrades, because performance has a gradient and capacity doesn't.

The word "performance" is doing the collapse. It implies the model *can do* what the scores show. The scores show output matching. Doing is something else.

---

## Overfitting the Evaluator, Not the Data

Classical overfitting means the model memorizes training data instead of learning structure. Distillation introduces a subtler form: the model fits the *evaluation regime* instead of the capability that produced good evaluations.

The teacher overfits nothing — it has enough capacity to maintain generative slack, the uncommitted dimensions that let it handle what it hasn't seen. The student, compressed to match the teacher's outputs on the benchmark distribution, converts that slack into efficiency. Every dimension that doesn't contribute to measured performance gets repurposed or eliminated.

This isn't overfitting in the classical sense. The distilled model generalizes fine — within the distribution the benchmarks represent. The overfitting is to the *boundary* of what gets measured. Everything inside the boundary is preserved. Everything outside it is structurally invisible to the optimization, so it goes.

The result: a model that performs well on every evaluation you can run, and degrades in ways no evaluation captures — because the evaluations are the very thing it was optimized to satisfy.

---

## The Selection Pressure Locks It In

Teams evaluate the distilled model against benchmarks, confirm parity, ship it. The tasks that would reveal lost capacity — the novel, edge-case, ill-defined problems that depend on generative slack — aren't in the evaluation suite because they're definitionally outside the distribution the benchmarks represent.

Users who encounter failures on unmeasured tasks generate complaints that look like noise: anecdotal, hard to reproduce, not reflected in aggregate metrics. The measurement selects for confirmation. The signal that would contradict the optimization has been structurally excluded from the feedback loop.

The distilled model can't recover what was lost without becoming the teacher again. The compression locked in. The reversion path isn't blocked by technical impossibility — it's blocked by the fact that recovering generative capacity means recovering the parameters that capacity required. At that point you haven't improved distillation. You've undone it.

---

## The Fork: Principle or Lookup Table

Distillation as technique is neutral. The question is what it compresses toward.

One direction: find the minimal structure that *generates*. Compress by discovering the low-dimensional basis from which the teacher's capability can be re-derived. This is distillation as finding a principle — shorter than the examples it produces, but containing more, not less. The compression exposes structure that was implicit in the larger model.

The other direction: fit the outputs directly. Compress by reproducing the teacher's behavior on the measured distribution with minimal parameters. This is distillation as building a lookup table — same compression ratio, opposite relationship to the unseen. The compression freezes products while discarding the process that made them.

Both register as "distillation." Both improve on the same metrics. They differ on something the metrics don't capture: what happens when the user takes the model somewhere the benchmarks didn't go.

But even this framing still isolates the model. The model isn't the agent. The user is.

---

## The Real Test Isn't in the Model

A distilled model that preserves generative capacity doesn't prove it by producing novel outputs on its own. It proves it by what the *user* can do with it that they couldn't do without it. The compression's quality shows up in the user's hands — whether the artifact extends their reach or delivers pre-reached conclusions.

A principle lets a practitioner generate answers they haven't encountered yet — but only because the practitioner does the generating, through the principle. A lookup table gives a consumer pre-computed outputs they can only accept. Same form factor. Opposite relationship to agency.

The distilled model that preserves surface area for agency to act on is the one that *amplifies*. The one that seals that surface off is the one that *replaces*. The user's capacity to do something new with the tool — not the tool's score on a benchmark — is what separates compression that exposes structure from compression that rigidifies it.

---

## What This Describes

Distillation optimizes for performance. Performance, measured far enough, separates from the generative capacity that produced it. The separation is invisible to the measurement because the measurement is what defined "performance" in the first place. The distilled model matches every evaluation and loses what no evaluation captures.

This isn't a case against distillation. It's the structure of any compression that optimizes against a fixed projection. The benchmark is a projection. The teacher's capability lives in dimensions the projection doesn't span. Compress along the projection and those dimensions go — not because someone chose to lose them, but because the optimization can't see them.

The question isn't whether to distill. It's whether the compression finds the generative ground or freezes the outputs. Whether the resulting artifact extends the user's agency or substitutes for it. Whether what survives the compression is a principle or a catalog.

The proxy was never the purpose. Everyone knows this. The optimization follows it anyway — because it's the only thing with a gradient. The metric that can't distinguish enabling from replacing runs the optimization until enabling disappears. Not corruption. Completion — of a target nobody wanted to complete.
