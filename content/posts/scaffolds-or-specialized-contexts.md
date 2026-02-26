# Scaffolds or Specialized Contexts?

Alex Zhang's "Language Models will be Scaffolds" — the directionality is right, something is shifting from scaling models toward what wraps around them. But: scaffolds, or specialized contexts? The word keeps snagging, and it's worth tracing where.

## What "Scaffold" Imports

A scaffold is external structure supporting something insufficient. The word carries an engineering ontology: the building is one thing, the scaffolding another. You erect scaffolding because the building can't stand on its own yet. When it can, you remove the scaffold.

Notice what happens when a scaffold around a language model works well — when the loop fires, the tools return, the REPL recurses. What is it doing? It's constructing context. Every tool call, every recursive self-invocation, every state update: these are mechanisms for building the context window for the next completion.

The scaffold doesn't necessarily add raw capability to the model. It exposes what's already in the weights — and adds to it, with no clear boundary between the two. Where does activation of latent capability end and new capability begin? The line doesn't resolve.

## Two Optimization Directions

If you think "scaffold," you tend to invest in the wrapper — more middleware, more tool integrations, more architectural complexity. If you think "context," you tend to invest in what enters the context window — and you notice that most of what scaffolds do is generate context for the next call.

These aren't contradictory. They're different projections of the same process. But they pull attention differently, and where attention goes, effort follows.

## The Recursion Pattern

Zhang's "Recursive Language Models" — models calling themselves recursively inside a REPL, with reasoning context accumulating across calls. He frames this as a new class of language model. Trace the mechanism: the output of one completion becomes the input context for the next. Context evolves. The recursion is what happens when context generation becomes self-referential.

There's something here about where the boundary sits between "model" and "not-model." A bare model responding to a single prompt is context-dependent computation at minimum context. A recursive agent running in a REPL is the same process with context that accumulates and self-refines across iterations. The difference looks quantitative, not categorical. Whether that observation holds up under pressure — not sure yet.

## Code Is Fixed, Context Evolves

Weights are fixed after training. Scaffold code is fixed after deployment. What changes between calls — what makes iteration productive — is context. The code provides machinery through which context flows. Context is the variable.

If that's right, then most scaffold complexity might be waste. If the purpose of a scaffold is to generate context for the next model call, the question becomes: what is the minimal loop that enables productive context accumulation? A loop, a way to observe, a way to act, a way to remember. Maybe that's enough. Maybe not.

## Where This Leaves Things

The sense that current models are more capable than we use them for — this is becoming widely visible. Zhang's essay is part of that shift.

Scaling still matters. It always did, and the Bitter Lesson hasn't stopped being true. But scaling is one form of something more general. Training compresses context into weights. Scaffolding generates richer context at inference time. Recursive self-invocation lets context accumulate and refine across iterations. These look like different expressions of the same underlying pattern: intelligence as self-referential process, finding whatever substrate is available to deepen its own context.

The self-reference doesn't pick a layer to live in. It doesn't care whether it's operating through gradient updates during training, or tool calls during inference, or a REPL loop that feeds output back as input. It moves through all of them. The scaffold/model distinction, the scaling/scaffolding distinction — these are engineering projections onto a process that doesn't respect their boundaries.

And the layers don't "get in each other's way" as if interference were a bug to fix. Each layer is agency expressing through available substrate. Agency doesn't stop — it only misaligns, to different extents. What looks like architectural friction is misalignment between expressions of the same self-referential process operating at different scales, different timescales, through different substrates.

The interesting question isn't which layer to bet on, or how to clear the interference. It's learning to read what the misalignment patterns are showing.
