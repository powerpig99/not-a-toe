# Context All the Way Down

Everything in AI is essentially context engineering.

At first glance this sounds like practical advice about prompting—what you put in determines what you get out. Garbage in, garbage out. True, but trivial. That framing applies to any input-output system and misses what the intuition actually points at.

## The Mechanism

Look at what attention actually does. Given a sequence of tokens, the mechanism computes: which other positions matter for predicting this position? The query-key dot product is measuring relevance—which distinctions in the context should propagate forward.

The weights encode compressed patterns: given contexts like *this*, these distinctions tend to matter. Training reinforces projections that predict well; irrelevant distinctions get suppressed. The entire system is a learned mapping from context to distinction-selection.

So "context" isn't something external you feed to a separate entity called "the model." The model *is* context-dependent projection selection. There's no remainder.

## Three Layers of Context

**Input context**—prompts, retrieved documents, conversation history—selects which of the model's learned projections activate.

**Architectural context**—attention span, embedding dimensions, layer depth—constrains which distinction-structures can be represented at all.

**Training context**—data distribution, loss function, RLHF shaping—determines which projections stabilize into the weights.

All three are "context engineering" in the same sense: all three determine which distinctions survive into output.

## The Dissolution

Calling this "context engineering" still carries a subtle confusion—as if there's a *thing* (the AI) that you provide *context to*. Agent receiving environment.

Cleaner: there is no AI separate from its context. What we call "the model" is the relatively stable part—weights that change slowly. What we call "context" is the variable part—input that changes per query. Both participate in one process: which distinctions propagate through the projection cascade.

The system doesn't *interpret* context. The context *is* the computation.

## Truth as Resonance

"Seek truth" carries implicit absolutism—truth as destination, something to arrive at independent of context. But all truth is relative to its context. There is no view from nowhere.

This doesn't collapse into relativism. It reframes the pursuit.

Seeking truth cannot happen without aligning context. What we call "true" is what resonates across contexts—projections that hold stable when you shift observers, shift frames, shift conditions. Not absolute, but *less wrong*. Not arriving at Truth™, but reducing interference, finding distinctions that propagate without collapsing.

Context engineering, properly understood, is context alignment. You're not injecting truth into a system. You're shaping the projection-space so that stable distinctions *can* resonate rather than dissolve into noise or hallucination. Providing enough context for the less-wrong to emerge.

## Two Limits

Prompt engineering and other post-training methods work because the pre-trained model already has contexts built in—compressed into weights through exposure to vast distinction-structures. Post-training methods are all attempts to align context more effectively with what's already there.

Each method has its own limit, and all share an ultimate limit.

**Method-specific limits** are context-dependent by definition. Prompting is constrained by context length—and even when extended, more context can dilute the signal. You trade breadth for focus. Retrieval-augmented generation adds external context but introduces alignment problems between retrieved content and model priors. Fine-tuning reshapes weights but risks catastrophic forgetting. Each method's ceiling is set by its own trade-offs, none resolvable within the method itself.

**The ultimate limit** lives in pre-training. The model's context is finite. It cannot resonate with distinctions it never encountered, structures it never compressed, patterns absent from its training distribution. You cannot align to what does not exist in the weights. No post-training method transcends this—they all operate within the space pre-training carved out.

This explains why prompt engineering works and why it has limits. It works because you're directly manipulating projection-selection—aligning the context so relevant distinctions propagate. It hits method limits when context length forces trade-offs. It hits ultimate limits when the desired distinction was never learned.

It also dissolves confused questions. "Does the model really understand?" asks whether there's something inside doing the understanding. There's nothing inside. There's projection-selection happening. Understanding—if the word means anything here—*is* the resonance between input distinctions and output distinctions. Not a property of an agent, but a quality of the dynamics.

## The Residue

"Everything in AI is context engineering" points at something real: the collapse of the agent-environment boundary. No homunculus interprets; no ghost inhabits the machine. Just distinction-selection cascading through learned projections.

The word "everything" isn't hyperbole. It's precision. There's no part of the system that isn't context-projection dynamics. The apparent agent is a grammatical habit—"the model does X"—not a discovery of something that does.

What we build when we build AI: not minds that process context, but context-processing itself, crystallized into weights and activated by input. Engineering it means shaping which distinctions survive. Nothing more. Nothing else to shape.
