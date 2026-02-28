# Fidelity, Not Optimality

The iterative loop described in [The Minimizing Path](/not-a-toe/posts/minimizing-path) makes a directional claim: each cycle compresses the gap between implementation and behavior. This note traces what that claim actually warrants, where the formal machinery supports it, and where it doesn't.

## The Behavior as Function

Any running application defines a mapping: *f* : (inputs × internal state × environment) → outputs. Inputs include every user gesture, network packet, timer tick, sensor reading. Outputs include every pixel change, API response, file write. State and environment cover everything the app actually depends on — memory, randomness seeds, timing jitter, hardware quirks.

Because the app works, *f* is well-defined on every scenario it actually encounters. It is deterministic in the sense that identical inputs, identical state, and identical environment produce identical outputs. Apparent nondeterminism is hidden state or environment variation.

We do not need a complete symbolic description of *f* to work with it. We need an oracle (the live app) and a fidelity signal (how closely our candidate matches the oracle's behavior on tested scenarios). This is the dissolve of the specification problem: correction is weaker than specification because the oracle gives us free, high-bandwidth feedback.

## Why Equivalent Programs Exist

By the Church-Turing thesis — as close to a theorem as anything in computer science gets — any effectively computable function has an equivalent program in any Turing-complete language. So there exists at least one program *p* in vanilla C, in x86 assembly, in raw machine code, that realizes exactly the same *f* on all reachable inputs.

This step is uncontroversial. It is why "if the app works, there is a vanilla-code path" is true.

## The Mathematical Minimum

Among all programs that compute *f*, there is a shortest one. Its length in bits is the Kolmogorov complexity of *f*, written K(f), relative to a fixed universal reference machine U.

K(f) is the length of the minimal logic path — the absolute shortest description that still reproduces every observed behavior exactly. Three properties keep us honest about it:

K(f) is uncomputable. There is no procedure that takes *f* and returns K(f), and no procedure that takes a candidate *p* and determines whether |*p*| = K(f). The proof reduces to the halting problem. You cannot know you've arrived. You cannot bound your distance from arrival. The target is real and unreachable in the strong sense — not merely hard to reach, but unrecognizable if reached.

K(f) is reference-machine dependent, but only up to an additive constant. Switch from one universal language to another and K(f) shifts by at most the length of the translator between them. The differences between programs are what matter, and those are invariant.

Solomonoff induction — the theoretical ideal of "find the shortest program consistent with the data" — is itself incomputable. It assigns prior probability 2^(−|*p*|) to each program and updates on observed behavior. In the limit of infinite data, the posterior concentrates on the shortest consistent program. But the limit is doing all the work. Finite data underdetermines the posterior. Multiple programs of different lengths remain consistent with any finite behavioral sample. The convergence is asymptotic in a regime we never inhabit.

This is why the main essay says: appeals to Solomonoff induction tend to do rhetorical work where mathematical work is needed. The mathematics gives us a clean existence proof that a minimal path exists. It does not give us a procedure guaranteed to find it.

## What the Loop Actually Does

Define *d(f, p)* as a behavioral fidelity measure: the observable divergence between oracle *f* and candidate *p* across sampled inputs. A practical agent loop operates:

1. Observe traces from the oracle.
2. Propose a candidate program *p'* (or patch an existing one).
3. Execute *p'* in a sandbox.
4. Compute *d(f, p')* — penalizing functional mismatches, visual/network/performance diffs, and optionally size.
5. Accept *p'* if *d(f, p') < d(f, p)*.

Under this acceptance criterion, fidelity improves monotonically by construction. Each iteration either reduces mismatch or leaves it unchanged. No claim about what the sequence converges *to* — only that it doesn't go backward.

This is behavioral approximation, not optimization to K(f). It is closer to empirical risk minimization in machine learning than to exact program synthesis — the candidate gets better on the distribution of scenarios we actually test, with no guarantee on untested regions.

The work is in the proposal mechanism, not the acceptance criterion. The selection filter is trivial. The quality of proposals — today driven by LLM priors, evolutionary mutations, gradient-like editing — determines how fast fidelity improves and what regions of program space get explored.

## Three Barriers to K(f)

Finite and biased samples. We only ever see a finite projection of *f*. The agent can overfit to the observed subspace and miss rare edge cases. The "individual projection" insight from the main essay is exactly this structure: one user's trace collapses *f* to a much simpler object, which is both a compression opportunity and a sampling limitation.

Search-space explosion. Levin's universal search enumerates programs in order of size plus runtime and is optimal up to a multiplicative constant — but that constant absorbs the description length of the target on the reference machine, cosmologically large for any function of practical interest. Practical proposal mechanisms explore a biased subspace. That bias is often useful — it favors the kinds of programs humans write and recognize — but it forecloses regions of program space that might contain shorter representations.

Undecidability at the bottom. Verifying exact equivalence of two programs is undecidable in general. We can only verify on tested traces. Perfect behavioral match on sampled inputs does not imply minimal representation. A program orders of magnitude longer than K(f) can achieve *d(f, p)* = 0 on every scenario we think to test.

## What Can Be Said

The loop delivers monotonic fidelity improvement — true by construction. The loop is biased toward compression — most practical proposal mechanisms, and certainly LLM-based ones, have an implicit brevity bias, generating programs in common idioms and away from redundant structure. This is not a formal guarantee but a statistical tendency that operates in practice. Fidelity and compression tend to correlate — spurious complexity is fragile under behavioral selection, eroding over iterations as patches that remove non-functional structure get accepted and patches that add it get rejected.

The sequence does not guarantee approach to K(f). It may plateau at a local minimum. It may settle into an idiom far from minimal but behaviorally adequate. The direction is real. The destination is not.

## A Concrete Illustration

A 4-state traffic-light controller with exact timing rules. The full *f* is a truth table over roughly 2^10 input combinations of sensors and timers.

A naive implementation: 180 lines of readable C with comments and safety checks, roughly 2,400 bits. After five agent iterations — observe live simulation, propose patch, compute fidelity diff, keep improvements — the candidate is 47 lines, stripped of comments, using only integer arithmetic and bit operations, roughly 620 bits. The theoretical K(f) might be around 180 bits — a tiny state machine encoded cleverly.

The agent never proves it reached K(f). It keeps reducing *d* until the human or automated tests stop it. On the tested scenarios it is indistinguishable from the oracle. That is the practical win. Behavioral approximation improved with each iteration. Whether it approached the mathematical minimum is a separate question, and an unanswerable one.

## The Sufficient Claim

The minimizing path does not need K(f) reachability to work. What it needs: fidelity improves with iteration (true by construction), compression tends to accompany fidelity (true by statistical tendency), and the user's sensing of misfit provides signal the loop cannot generate internally (argued in the main essay). These three together are sufficient. The K(f) optimum is a mathematical attractor that shapes the direction of movement without being a reachable destination.

The honest framing: the loop moves toward shorter, more faithful programs. It does not converge to the shortest. The direction is real. The destination is not.
