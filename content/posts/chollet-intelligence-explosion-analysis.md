# The Shadow Mistaken for the Object: Chollet's Intelligence Explosion Argument

In 2017, François Chollet—creator of Keras and one of AI's sharpest practitioners—published "The Impossibility of Intelligence Explosion," arguing that the popular narrative of recursive AI self-improvement spiraling into superintelligence is fundamentally mistaken. The essay is widely cited, intellectually serious, and wrong in ways that are more interesting than most things that are right.

Chollet makes several interlocking claims. Intelligence is inseparable from its context—body, environment, culture. There is no "general" intelligence; the No Free Lunch theorem proves this mathematically. IQ past a certain threshold shows diminishing returns on real-world impact. Civilization is already a recursively self-improving system, and it progresses linearly, not exponentially. Therefore a single AI, no matter how powerful its brain, cannot break out of these constraints and explode into superintelligence.

Each of these observations points at something real. The essay's problem isn't that it's seeing things that aren't there. It's that it forces genuinely different things onto the same axis and then reads the resulting distortion as a discovery about reality.

## Intelligence as situated versus intelligence as bounded

Chollet's strongest point is that intelligence doesn't exist in a vacuum. A brain needs a body, an environment, a culture to do anything. A human raised by wolves doesn't develop human intelligence. An AI floating in empty space with no inputs solves nothing. All true.

But there's a subtle slide from "intelligence requires coupling to a context" to "intelligence is limited to its current context." These are different claims living on different axes. The first is about mechanism—how intelligence operates. The second is about ceiling—how far it can go. Chollet treats them as the same claim.

Consider: every tool humans have ever built required coupling to an environment. Fire required fuel and oxygen. Writing required surfaces and symbols. Computers required electricity and semiconductors. At every step, intelligence was situated. At no step did situatedness prevent intelligence from radically restructuring its own situation. The coupling is real; the ceiling it supposedly imposes is not demonstrated.

An AI that needs environmental coupling to function might still restructure its environment extremely fast. The question isn't whether coupling is necessary—it always is—but how rapidly a given system can establish, modify, and leverage its couplings. Chollet's framing treats the existence of the coupling as evidence for a speed limit, when it says nothing about speed at all.

## The No Free Lunch misdirection

Chollet invokes the No Free Lunch theorem to argue there's no such thing as general intelligence. The theorem states that no algorithm can outperform random chance across all possible problems. This is mathematically true and pragmatically irrelevant.

The theorem applies across the space of all possible problems weighted equally—which is another way of saying it applies in a universe with no structure whatsoever, where the future bears no relation to the past. We don't live in that universe. We live in a universe with deep, exploitable regularities. The entire reason intelligence works at all is that our universe is low-entropy: patterns exist, persist, and can be leveraged.

The real question isn't whether any system can be intelligent across all conceivable problems. It's whether a system can be *more general* than humans across the class of problems the actual universe generates. That's a continuum, not a binary. Humans are more general than octopodes. Octopodes are more general than sea cucumbers. The No Free Lunch theorem says nothing about where this continuum tops out, because it's a statement about the max-entropy case—precisely the case that doesn't apply.

By invoking it, Chollet collapses a continuum (degree of generality) into a binary (general/not-general), concludes that absolute generality is impossible, and treats this as evidence that the continuum can't extend much further than humans. The logic doesn't connect.

## The IQ argument and the architecture blind spot

Chollet observes that humans with IQs above 130 don't achieve proportionally more than those at 130. Feynman reportedly had an IQ of 126. Many people with IQs of 170+ accomplish less than scientists at 130. Therefore, he argues, raw cognitive power past a certain threshold doesn't translate to proportionally greater real-world impact.

This observation is real but the inference from it is wrong, because it confuses variation within an architecture with variation across architectures. All human brains are the same basic design. IQ variation represents parametric tuning—slightly bigger here, slightly faster there—not architectural change. It's like observing that a car going 200 mph isn't twice as useful as one going 100 mph, and concluding that no vehicle can be radically faster than a car. You've measured the diminishing returns of one design, not the limits of the design space.

The relevant comparison isn't between a 130-IQ human and a 170-IQ human. It's between a human and something that thinks 1,000 times faster, holds 1,000 times more working context, has direct high-bandwidth access to its own cognitive tools, and can modify its own architecture. The variance between humans tells us almost nothing about this case, because humans occupy a single tiny point in the space of possible cognitive architectures. Chimpanzees could make the identical argument: "The smartest chimp doesn't accomplish radically more than a merely smart chimp, therefore no primate can ever build rockets."

## The linearity illusion

Chollet's empirical anchor is that scientific progress—the closest analog to a recursively self-improving AI—is measurably linear. Physics didn't advance faster between 1950-2000 than 1900-1950. Medicine improves at a steady pace. Therefore recursive self-improvement doesn't produce exponential takeoff.

This claim is both empirically questionable and theoretically unsound.

Empirically, it's a scale-dependent observation. Look at scientific output decade by decade and it might look roughly linear. Look at civilizational capability over centuries and it's clearly exponential: world GDP, energy capture, computation, information storage—all exponential on longer timescales. The "linearity" of recent scientific progress is an artifact of zooming in close enough that the curve looks flat. Any exponential looks linear from sufficiently inside it.

This is the mirror image of Kurzweil's error. Kurzweil stands on the exponential curve, looks forward, and sees an explosive future—feeling like "this moment" is the special inflection point. Chollet stands on the same curve, looks backward, and sees steady linear progress—feeling like the current pace is the natural rate. Both are projecting local experience as global structure. Same curve, opposite misreadings, same cause: the local derivative of an exponential is proportional to its current value, which from inside always feels like a constant.

Theoretically, even if recent scientific progress really is linear, this may be an artifact of how science currently runs—through human brains that can't be copied, communicate via low-bandwidth language, lose everything at death, rebuild from scratch each generation, and coordinate through bureaucracies optimized for political survival rather than discovery. The linearity might tell us about the scaling properties of *this particular implementation*, not about recursive self-improvement in principle.

## Civilization as cognitive system: true but not limiting

Chollet argues that individual brains are just modules in a larger cognitive system—civilization—and that this larger system is what actually progresses. Books, math, the internet, other people—these are literally part of your mind. This is his strongest insight and the one that survives scrutiny best.

But he draws the wrong conclusion from it. He argues that because civilization is already recursively self-improving and produces only linear progress, adding better brains won't qualitatively change the dynamic. The new AI brains will just be more modules in the same civilizational system, subject to the same bottlenecks and friction.

This ignores that the bottlenecks he identifies—communication bandwidth, coordination costs, adversarial counter-reactions, diminishing returns—are properties of how *human* modules connect, not properties of recursive self-improvement itself. Human civilization coordinates through speech and text at biological speed, loses institutional knowledge to death and politics, and scales with massive friction. None of these bottlenecks are necessary features of a cognitive system in general.

An AI that can copy itself, share knowledge by copying weights, think thousands of times faster than biological neurons, and directly interface with computational tools rather than typing on keyboards—such a system faces a completely different set of scaling constraints. Chollet's argument is like observing that a human bucket brigade can only move water at a certain rate and concluding that water can't be moved faster, while ignoring the possibility of pipes.

## What's actually going on

Strip away the specific claims and the essay reveals a single structural move repeated five different ways: observing properties of one specific implementation and presenting them as universal constraints.

Human IQ shows diminishing returns → intelligence shows diminishing returns. Human civilization progresses linearly → recursive self-improvement is linear. Human intelligence requires cultural scaffolding → intelligence is bounded by its scaffolding. Science encounters bottlenecks → all self-improving systems encounter comparable bottlenecks. Variation between humans is modest → variation in cognitive capability is modest.

Each time, the properties of the shadow are mistaken for properties of the object casting it. The shadow is real—it's genuinely there on the wall. But its shape tells you about the wall and the light source, not about the full geometry of the object.

This is why the essay feels convincing even when the arguments don't hold. Every individual observation is accurate. Intelligence really is situated. IQ really does show diminishing returns. Science really does face bottlenecks. The error isn't in the observations—it's in the inference that these observations about one system constrain all possible systems.

## The pattern in real time

In February 2026, someone on X suggested Chollet revisit the essay given recent AI progress. Chollet responded: "You should read it some day, it's a good read. Every single thing said there is still true."

He then quoted what he called the key bit: "the first superhuman AI will just be another step on a visibly linear ladder of progress, that we started climbing long ago."

Here's what makes this interesting. In the same thread, just above, Chollet had posted that we can say we have AGI "when it's no longer possible to point to something that regular humans can do and AI can't"—and that he expects this will become nearly impossible by 2030.

Read those two positions together. The first says: AI will match human capability across the board within about four years. The second says: the 2017 essay arguing that individual cognitive scaling hits hard ceilings—situatedness, diminishing returns, civilizational bottlenecks—is entirely correct.

He can technically hold both by retreating to the claim about dynamics: yes, AI reaches human level, but it's just another linear step, not an explosion. But this quietly concedes the game. The 2017 essay's force didn't come from a narrow claim about the shape of the progress curve. It came from arguing that intelligence *couldn't* be meaningfully scaled by improving individual systems—that the brain was never the bottleneck, that raw cognitive power past a threshold didn't translate to proportionally greater capability, that you couldn't decouple intelligence from its civilizational scaffolding. If AI matches human intelligence by 2030 through scaling individual systems, most of those arguments didn't hold as constraints. They described how human progress felt from the inside, not what was possible in principle.

The tell is the phrase "every single thing said there is still true." If you're tracking reality, you look at what's happened since 2017—the scaling results, the generality gains, the capability jumps that surprised even optimists—and ask which specific claims in your essay this evidence updates. That's observation. "Everything is still true" is maintenance. It's the move of someone preserving the coherence of a prior frame rather than re-deriving from current ground.

This is the essay's structural error made personal. The same pattern that led Chollet to mistake properties of one implementation for universal constraints now leads him to mistake consistency of narrative for consistency with evidence. The projection—the essay as a coherent intellectual object—has become something to maintain rather than something to test. The representation substitutes for the observation. And the maintenance cost becomes invisible, because it feels like just being consistent.

## The irony of the update

Here's the deeper irony: Chollet was actually less wrong in 2017 than he is now.

The 2017 essay, despite its flawed arguments, was gesturing at something real—that "intelligence" isn't a single scalar you push past a threshold and win. The situatedness point, the emphasis on intelligence as embedded in larger systems, the skepticism toward a clean finish line—these intuitions had genuine substance, even though the arguments built around them didn't hold.

His 2026 position abandons exactly what was most valuable. By accepting the benchmark-closing framing—AGI arrives when you can't point to a gap—he's adopted the very picture he originally criticized: intelligence as a measurable quantity that AI is converging toward and will eventually match. He's traded a flawed argument for a correct intuition for a cleaner argument for a flawed intuition.

The benchmark framing itself deserves dissolution. "Closing the gap" assumes the gap is a fixed quantity being consumed. But each capability gain redefines what counts as the gap. When AI masters protein folding, we don't say "the remaining tasks got easier." We discover new problems that weren't even articulable before the previous frontier was reached. The remaining one percent after closing ninety-nine isn't one percent of the original problem. It's a freshly visible hundred percent that only became visible from the new vantage point.

This is why the gap will seem to perpetually shrink without closing. The shrinking is real, measured against a fixed reference. But the reference isn't fixed—each advance reveals new territory. Chollet's 2030 prediction, that it will become "nearly impossible" to point to something humans can do and AI can't, will likely feel perpetually almost-true without arriving, because each closing reshapes what "can do" means.

So the critique here is not that Chollet's 2017 conclusion was wrong. It's that his arguments didn't support his conclusion—and that by 2026, he's abandoned the conclusion that was closest to right while defending the arguments that were furthest from it.

## What survives

The essay's lasting contribution is the insistence that intelligence is embedded, not abstract. Any real AGI will need to couple to environments, accumulate experience, and operate within physical constraints. This is a genuine corrective to the most naive versions of the intelligence explosion narrative, which imagine a brain in a jar bootstrapping itself to godhood through pure thought.

But "intelligence is embedded" is a constraint on mechanism, not on outcome. It tells you that an AI can't do everything from inside a box with no inputs. It tells you nothing about what an AI can do given inputs, tools, and the ability to reshape its own situation—which is, after all, exactly what the intelligence explosion hypothesis is actually about.

The essay's lasting error is treating the scaling properties of human civilization as a natural law rather than an engineering report. When you mistake one system's performance curve for a universal constraint, you've confused the map for the territory—and foreclosed possibilities that the territory may well contain.
