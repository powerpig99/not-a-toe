# The Interface Stack: Why Agents Don't "Prefer" CLIs

Andrej Karpathy recently posted that "CLIs are super exciting precisely because they are a 'legacy' technology, which means AI agents can natively and easily use them, combine them, interact with them via the entire terminal toolkit." His advice: "It's 2026. Build. For. Agents."

He's not wrong. But the framing inverts the dependency it's trying to describe.

## The Word "Legacy"

Karpathy's argument runs: CLIs are old → old means agents can already use them → therefore build CLI-first for the agent era. The word doing the heavy lifting is "legacy" — positioned as accidental advantage. Something survived from the past, and it happens to be useful now.

But this treats the CLI's persistence as historical luck rather than structural necessity. The CLI didn't survive *despite* being old. It survived because it sits at a specific layer in the interface stack that nothing above it can replace, and nothing below it can symbolically access.

## The Stack

Three layers, each a projection from the one below:

**Physical manipulation** — switches, punch cards, wiring. Direct electrical-mechanical interaction with the machine. No symbolic mediation. The human acts on the hardware's own terms.

**Symbolic command (CLI)** — the first layer where interaction becomes text-mediated. The human issues commands in a formal language. The machine parses symbols. This is where the physical collapses into the linguistic. Everything after this point is text operating on text.

**Perceptual projection (GUI)** — visual layout, spatial metaphor, mouse targeting, pixel rendering. The symbolic command layer re-projected into human sensory space. Designed for pattern recognition, motor coordination, spatial intuition — the pre-symbolic capacities that humans bring but that have nothing to do with computation.

Each higher layer adds accommodation for human perceptual and cognitive constraints. Each adds indirection. Each is generated from the layer below it and cannot exist without it. The GUI is a projection of the CLI layer onto human visual-motor space. Remove the symbolic command layer, and there is nothing to render.

## What "Legacy" Obscures

Calling the CLI "legacy" collapses the structural into the historical. It frames the interface stack as a timeline — first we had CLIs, then we got GUIs, and now agents go "back" to CLIs. This is chronology masquerading as explanation.

The actual structure: CLI is the foundational symbolic interface. GUIs are projections from it, adding a perceptual accommodation layer. The GUI didn't *replace* the CLI any more than a map replaces the territory. It projected the territory onto a surface a human eye could parse.

When Karpathy says agents can "natively and easily" use CLIs, the word "natively" is doing more work than he intends. Agents operate in symbol space. The CLI *is* symbol space — it's the layer where human-machine interaction first becomes purely textual. Agents don't "prefer" CLIs. They simply don't need the projection layer that was never for them.

## The GUI as Sensory Accommodation

Consider what a GUI actually does: it takes symbolic operations (create file, move file, execute program) and re-encodes them as spatial metaphors (folders, drag-and-drop, double-click). This re-encoding exists because humans navigate space more fluently than they parse formal syntax. The desktop metaphor isn't computation — it's a sensory interface wrapping computation.

Karpathy's example makes this visible: "ask your Claude/Codex agent to install this new Polymarket CLI and ask for any arbitrary dashboards or interfaces or logic. The agents will build it for you." The agent operates at the symbolic layer, then *generates* the visual projection if a human needs one. The GUI becomes output, not interface.

This is the structural point his "legacy" framing misses: agents aren't reverting to an older technology. They're operating at the layer where symbolic command lives, and generating the perceptual projection layer on demand — when a human needs to see something. The projection is no longer the site of interaction. It's a rendering pass.

## What's Below

The physical layer — direct hardware manipulation — is where agents currently cannot go natively. Robotics is hard for precisely this reason: there is no symbolic abstraction to ride on. The physical layer is pre-linguistic. Every robotic action requires bridging from symbol space back into the physical without a stable intermediate representation.

This is not a "harder version of the same problem." It's a different layer entirely. The CLI-to-GUI gap is projection within symbol space (text to visual rendering of text-operations). The physical-to-CLI gap is the collapse from continuous physical reality into discrete symbolic command. That collapse is where the real interface problem lives, and it's why "just add more CLIs" doesn't extend downward.

## The Reach-Clarity Tradeoff

Karpathy's sensing is excellent — he sees the right thing. The CLI is where agents belong. The GUI era is ending for machine-to-machine interaction. Most people aren't even there yet; they're still asking how to make agents click buttons in browsers. He's already past that. His interpretation just hasn't caught up to his own intuition.

But there's a structural reason the gap persists, and it has nothing to do with capability. Reach requires compression into existing frames. "Legacy" is a word his audience already has coordinates for. "Foundational symbolic interface layer" has no landing pad. The act of communicating to many *is* the act of projecting onto shared dimensions, and shared dimensions are by definition lower-dimensional than what's being projected.

So the sensing-interpretation gap isn't just his — it's distributed. He senses clearly, compresses for reach, the compression becomes the dominant frame, and the audience's reception reshapes the field his own subsequent thinking operates in. The reach feeds back into the sensing.

This is the mechanism underneath every thought-leader pattern. The ones who see furthest are precisely the ones whose seeing gets most distorted by the requirement to transmit it. Not because they compromise — because transmission *is* dimensional reduction. The channel constrains the signal. The bigger the channel, the more the constraint. The very need for reach obscures the ability to see more clearly.

The only exit is to stop optimizing for reach — to treat writing as a thinking tool rather than a broadcast medium. Let the writing generate clarity for the writer. If it transmits, fine. But the optimization target is the seeing, not the landing.

## The Inversion

Karpathy's practical advice is sound: expose your product via CLI, write Skills, support MCP. Build interfaces agents can parse. All correct.

But the reasoning — "CLIs are legacy, and legacy happens to work for agents" — runs backward. CLIs aren't useful to agents because they're old. They're old because they're foundational. They're foundational because they're the first stable symbolic interface — the layer where human language and machine operation first share a surface. Everything above is accommodation. Agents strip the accommodation.

The question isn't whether to "build for agents." It's recognizing that the symbolic command layer was always the load-bearing structure, and the GUI era was an extended accommodation for human perceptual constraints. What's changing isn't the stack. It's which layers need to be rendered.
