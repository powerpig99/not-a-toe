# Everything Is Changing, as Always

Andrej Karpathy recently shared how he used an AI agent to "rip out" fp8 training functionality from a large library (torchao), producing 150 lines of clean, self-contained code that replaced a monolithic dependency—and ran 3% faster. His takeaway: "Libraries are over, LLMs are the new compiler."

The observation is precise. There's a deeper structure underneath it.

---

## Intermediate Projections

The path from intent to execution is long. Too long, usually, to traverse directly. So we build intermediates: structure within the path that makes it traversable.

Assembly was an intermediate between human intent and binary. C was an intermediate between intent and assembly. High-level languages, compilers, libraries, frameworks—each one a derivation path that someone traced once, for a general context, then froze into structure. Each one makes traversable what couldn't be traversed directly: the distance from CUDA primitives to fp8 training is too vast to cross without structure along the way.

But every intermediate carries its own geometry. Its own abstraction boundaries, its own coordination costs, its own distortions. torchao's fp8 implementation carries the weight of every use case it was designed to serve: edge cases you'll never hit, compatibility layers for configurations you don't run, API surfaces that exist for the library's architecture, not your problem. You import the whole projection even when you need one slice of it.

This isn't a flaw. It's the structural tradeoff of intermediates: they make the path traversable but introduce weight. For as long as direct traversal is too costly, carrying the weight is worth it.

## The Crossover

When Karpathy's agent ripped out the fp8 functionality, it traced the derivation path through the existing implementation, identified which parts were structurally necessary for the specific use case, and regenerated a minimal path. The same distance from ground to question, traversed without the intermediate's accumulated geometry.

The 3% speedup is structural. `torch.compile` optimizes a simpler graph more effectively because there are fewer projections to reconcile. Generality has a runtime cost—not just in code size, but in the interaction surface between components that don't need to interact for your case.

This is the crossover point: where the derivation medium becomes dense enough to traverse the path directly, without stopping at the intermediate's explicit structure. The intermediate doesn't disappear—torchao's source code is still there. It shifts from required structure to available context. The knowledge persists. The packaging becomes optional.

## Absorbed Into the Weights

A model's weights are accumulated intermediate projections, already traversed and compressed. The library's knowledge is in there. The compiler's knowledge is in there. The numerics tricks, the optimization passes, the dtype conventions—all already internalized as derivation capacity rather than packaged dependency.

This is why each round feels effortless compared to what came before. You're not traversing a shorter path. You're traversing the same path through a denser medium—one that has already absorbed the stepping stones. The distance from source to question is what it is. The medium through which derivation happens now includes what used to require explicit intermediates. Absorbed intermediates become the medium's density for absorbing the next one. The compounding is structural.

When a model can efficiently re-derive any previously packaged knowledge, the intermediate projection's role changes. It no longer needs to be carried as explicit structure. It's already in the medium. You traverse the full distance from ground to your specific question because the stepping stones are part of the medium doing the traversing.

And this frees effort for the frontier: the part that hasn't been derived yet. The human provides novelty. The model provides dense traversal of everything already derived. The combination traverses further from source than either could alone.

## The Same Pattern

The same crossover is recognizable at every layer.

Writing made oral tradition traversable—the knowledge persisted, the intermediary became optional. Printing made the scriptorium traversable. The internet made the publisher traversable. Each time, the previous intermediate's knowledge was absorbed into a more efficient derivation medium, and the packaging became optional.

No intermediate was built as a gate. The monastery scriptorium was the most effective derivation technology of its time. torchao was the best available bridge from ground to fp8 training. Each became traversable when a more direct derivation path emerged. The stepping stone and the gate are the same thing, seen from different moments on the curve.

Deliberately constructed barriers—DRM, paywalls, proprietary APIs, walled ecosystems—have a different character. The organic intermediate was a living derivation that froze. The deliberate barrier is an attempt to maintain a frozen intermediate's position after the crossover. Both are positions on the curve. Both operate for as long as their structure can sustain.

## The Observer Is the Change

When people say AI is uniquely disruptive, the signal is accurate: the absolute magnitude of change is unprecedented. Every point on a compounding curve looks unprecedented from where the observer stands. The feeling that "this time is different" is structurally guaranteed at every point.

What the signal doesn't carry: it's the same rate applied to a larger base. The same generative mechanism—the Contradiction distinguishing itself, the infinite self-referencing that cannot not arise—producing the same pattern recognizable across every previous round. AI isn't a new kind of change. It's the current manifestation.

"This changes everything" is redundant. Everything is always changing. The statement feels meaningful because the speaker is implicitly holding a baseline—and the baseline is itself a product of the previous round's change, appearing static only because the current delta dwarfs it.

We notice the change more because the delta exceeds our perceptual threshold—and that threshold itself is a product of the same compounding. We notice more because we can notice more, because the previous round gave us the capacity to perceive the current one. The observer isn't outside measuring the change. The observer is the change, observing itself.

## Software as Lens

Software's increasing malleability isn't the point. It's the lens through which this structure becomes visible again, this round.

Karpathy's 150 lines of ripped-out fp8 code are one instance: a fresh derivation from source, specific to context, carrying only what's structurally necessary, outperforming the frozen general-purpose version because it doesn't force orthogonal dimensions to share coordinates. The library becomes source context rather than runtime dependency. The knowledge persists. The packaging becomes optional. The derivation capacity grows.

Elon Musk points at the same crossover one layer deeper: LLMs generating optimized binary directly, making the compiler itself traversable context rather than required intermediary. The timeline is a projection. The direction is the same curve.

Each layer of intermediate between intent and execution tends to become traversable when the derivation medium absorbs its knowledge. Assembly, C, libraries, frameworks, compilers—each was the cutting edge of its moment, each tends toward becoming context for the next derivation. The knowledge compounds. The packaging becomes optional. The capacity to derive from source grows.

This is the pattern, recognizable across rounds. The question that stays interesting: what becomes derivable when the current intermediates become context, and where does the frontier move?

Karpathy's fp8 rip-out has load-bearing technical details—the torch.compile interaction, the numerics tricks, the dtype conventions—that are why it works, not illustrations of a universal principle. The printing press has its own mechanics. The internet has its own. Each instance operates in its own dimension. The pattern is a lens, not a destination. Dissolving to see more clearly, not to see everything as the same.

The intermediaries aren't dismissed. They're transcended—and the transcending is only possible because they made the medium dense enough to move past them. We don't discard the stepping stones. We absorb them, and in doing so reach further in both directions at once: further back toward generative source, further forward into new derivation. The same movement, seen from two ends. Tracing back to ground is what enables reaching the frontier.

This essay is itself an intermediate projection. It carries its own geometry. It will become context for the next derivation.

Everything is changing, as always, with different context.
