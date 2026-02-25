# The Moving Ground: On "Intelligent AI Delegation"

Tomašev et al. propose a comprehensive framework for how AI agents should decompose tasks, assign them across agents and humans, monitor execution, verify completion, and recover from failure — all within an emerging "agentic web." The framework draws on principal-agent theory, transaction cost economics, contingency theory, and organizational management to design protocols for trust, reputation, permissions, and accountability in multi-agent delegation chains. The engineering is thorough and the protocol gap analysis — showing where MCP lacks permission attenuation, A2A lacks cryptographic verification, AP2 lacks conditional settlement — is immediately actionable.

The paper will likely prove useful. And that usefulness is precisely what obscures its limitation.

## The Asymptote

The framework is built on a set of ground assumptions: agents will delegate, markets will coordinate, protocols will govern, humans will oversee. These are not predictions about the future — they are descriptions of the present, projected forward under continuity. The paper then constructs elaborate structures on this ground: reputation ledgers, trust scores, authority gradients, smart contracts, verification games. Each component addresses a real gap in current agentic coordination. Each solution, once implemented, will become the ground from which the *next* gap is measured — and that next gap will be structured differently from the one just solved.

This is the asymptotic nature of bridging the coordination gap between human intent and machine execution. Each improvement redefines the remaining distance rather than closing it. Moving from 99% to 99.9% looks like progress toward 100%, but 100% is not the limit of the same series — it is a different kind of thing entirely. The paper treats the delegation problem as an engineering gap to be closed with sufficient protocol sophistication. But the gap is generative: it produces the next version of itself from each solution, not because the solutions fail, but because they succeed and thereby shift what "the problem" is.

## Extrapolative Foresight and Its Limits

The paper exemplifies what might be called *extrapolative foresight*: take current dynamics, identify failure modes, design structures to address them. This works when the ground is stable enough that the problems being solved today remain the problems that matter tomorrow. For the near term, this is likely the case.

The structural issue is not that the forecast is wrong about the trajectory, but that it cannot represent the possibility that the coordinate system in which the trajectory is plotted might not persist. The paper borrows from human organizational theory — span of control, authority gradients, zones of indifference — and maps these onto AI agent networks. The implicit assumption is that the *problem structure* is conserved even as the substrate changes. Delegation is delegation, trust is trust, accountability is accountability — just faster and at scale.

But what happens when the ground shifts is not that agents get faster at delegating. It is that "delegation" may cease to be the operative concept. The entire framework is organized around a human-AI boundary, stable agent identities, and persistent capability hierarchies. These are precisely the features most likely to dissolve first. An agent that outgrows its delegator mid-task represents an authority gradient inversion that no protocol in the framework can handle, because the framework assumes delegation flows from more-capable to less-capable across stable timescales.

## What the Delegation Chain Actually Surfaces

The paper treats long delegation chains (A→B→C→...→Y) as monitoring and accountability problems. Each node is a potential point of failure, so the solution is better contracts, better checkpoints, better verification.

The deeper structure is different. Each node in a delegation chain is a *re-projection* — the intent gets re-interpreted through each agent's operational constraints, context window, and capability surface. What emerges at the terminal node is not a "distorted version" of the original intent that better monitoring could have preserved. It is a distinct projection that may share very little geometry with the original. This is not a channel quality problem solvable by better encoding and error correction. It is a dimensionality mismatch between the delegator's intent-space and the delegatee's action-space. No protocol bridges that gap; it can only be managed.

The paper's treatment of trust illustrates the same pattern. "Trust" collapses multiple orthogonal dimensions — capability, alignment, integrity, stability — into a computable score. These dimensions can move independently. A high-reputation agent could be perfectly capable and honest but undergoing a fine-tuning update that shifts its alignment mid-task. The framework cannot distinguish this from performance degradation, because the collapse has already occurred in the representation.

## What Survives

Not everything in the paper is equally bound to the current ground. The *contract-first decomposition* principle — recursively decompose tasks until each unit has a concrete verification mechanism — is structurally more durable than the trust and reputation architecture. It does not depend on stable capability hierarchies or persistent agent identity. It simply says: do not delegate what you cannot verify. That is a constraint that survives ground shifts, because it does not commit to any particular ground.

Similarly, the ethical observations about de-skilling, moral crumple zones, and apprenticeship pipeline erosion are refreshingly specific. The paradox of automation — that removing humans from routine work deprives them of the situational awareness needed to handle the exceptions they are retained for — does not require the current agent topology to hold. It is a structural feature of any system that concentrates routine execution in one substrate and exception-handling in another.

## The Honest Position

The paper presents itself as a framework for "the emerging agentic web" — as if the destination is known and the task is engineering safer passage. The honest position is that this is a near-term engineering proposal of genuine value, bounded in ways it does not acknowledge. The assumptions are probably valid for the foreseeable future. The protocols will probably get built roughly along these lines. The framework will age well as reference architecture.

The limitation is not a mistake anyone is making. You cannot build protocols for a regime you cannot yet conceptualize. You build for what you can see, and that is legitimate. The only error is mistaking the reach of your sight for the extent of what is there. Foresight that uses the present as its base does not merely risk being wrong about the future — it risks being right about a future that does not arrive, because the ground shifted under the question itself.

---

*February 2026*
