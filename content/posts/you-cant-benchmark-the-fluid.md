# You Can't Benchmark the Fluid

François Chollet designed ARC to measure what he calls fluid intelligence—the ability to handle genuinely novel problems, not pattern-match against training data. It's a serious attempt at a serious problem. But it contains a contradiction at its foundation, and the contradiction isn't technical. It's structural.

A benchmark is a fixed formal structure: defined format, scoring criteria, success threshold. Fluid intelligence is precisely what operates where no fixed formal structure applies. The moment you formalize a test for it, you've created a frame—and what you're measuring is performance within that frame, not the capacity to operate without one.

This isn't the usual "teaching to the test" worry. It's not that models will overfit to ARC's specific puzzles, though they will. It's that *any* benchmark for fluid intelligence forces the dimension of "operates without prior frame" onto the axis of "performs within this specific frame." You're measuring the shadow and calling it the light source.

## The pattern

The pattern plays out predictably. Each version of ARC gets solved. Chollet releases ARC-AGI-2. The goalposts shift. This is presented as the benchmark working as intended—tracking the remaining gap. But what's actually happening is that the *formalization* keeps getting consumed, not that fluid intelligence keeps getting closer. Each test captures a static snapshot of what novelty looked like at the time the test was designed. Intelligence moves. The snapshot doesn't.

This connects to a deeper point about the "AGI gap." Chollet recently said we'll have AGI when it's no longer possible to point to something humans can do and AI can't—and expects that by 2030. But each capability gain redefines what counts as the gap. The remaining one percent after closing ninety-nine isn't one percent of the original problem. It's a freshly visible hundred percent that only became articulable from the new vantage point. The gap appears to shrink against a fixed reference, but the reference isn't fixed.

ARC is this dynamic made concrete. Each iteration doesn't converge on measuring fluid intelligence. It discovers that whatever the last iteration measured wasn't fluid intelligence after all—because the truly fluid part is, by definition, what the current formalization can't capture. The benchmark is always one step behind its own target, not because the engineering is bad, but because the target is defined by its escape from formalization.

None of this means benchmarks are useless. They measure something real—performance on specific problem classes, rate of capability gain, relative strengths across systems. What they can't do is what ARC claims to do: capture the thing that makes intelligence *fluid* rather than fixed. That capacity lives precisely in the gap between what any current formalization can specify and what the system actually does when the formalization runs out.

You can benchmark crystallized capability. You can't benchmark the fluid. The attempt to do so is a contradiction—not a hard problem awaiting a clever solution, but a category error built into the project itself.
