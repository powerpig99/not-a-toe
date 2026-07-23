# Cover styles

Living inventory for essay covers in this folder. Filename = essay slug (`content/posts/<slug>.md` → `assets/covers/<slug>.jpg`). Install as landscape **20:9** JPEG (or jpeg/png/webp) at **1280×576** — the shared aspect for site, Substack featured image, and X Article cover.

| Related | Path |
|---------|------|
| Post authoring | [`content/posts/README.md`](../../content/posts/README.md) |
| Substack export | [`docs/export-for-substack.md`](../../docs/export-for-substack.md) |
| X Article export | [`docs/export-for-x-article.md`](../../docs/export-for-x-article.md) |
| Local memory / sleep audit | [`docs/local-memory.md`](../../docs/local-memory.md) |

## Principle

**Each new cover uses a visual style not already taken by an existing cover.**

Concept may echo the essay; medium and look must not. Before generating, read this file, pick a style absent from the inventory (or invent one not listed), generate, then add a row under Inventory and under Style families. Reusing a family dilutes the set into a house look that stops being chosen.

Differentiation is on **style** (medium, print/photo tradition, palette discipline, rendering method)—not on subject alone. Two dark chalk abstracts on black are the same style even if one has orbits and the other has a spiral.

## Spec

| Rule | Detail |
|------|--------|
| Aspect | **20:9** landscape only — X Article cover, Substack image, site og/title image share this file |
| Size | **1280×576** install (generate at 20:9; 1600×720 is fine if resized to 1280×576 before install) |
| Text | None (no title, no logo, no legible caption) |
| Fit | Concept reads the essay’s cut; style is independent of other covers |
| Not | Square, portrait, 16:9, 3:1 profile-banner, or other non-20:9 crops as the essay cover |
| After generate | Install as `<slug>.jpg`, update Inventory + Style families below |
| Legacy assets | Keep older covers as installed (many are 16:9). Do **not** bulk-regenerate or re-crop them for 20:9. Regenerate a legacy cover only when the operator explicitly asks for that slug. Site CSS uses `object-fit: cover` in a 20:9 box, so 16:9 files display with a mild center crop until replaced. |

## Style families (used)

Grouped by look. One representative name; multiple slugs may share a family (avoid adding more to crowded families).

| Family | Traits | Covers |
|--------|--------|--------|
| **Dark chalk / light trails** | Black or near-black field; chalk, charcoal, or particle light paths; orbits, sparks, arcs | `self-rl-for-humans`, `intelligence-belongs-only-to-the-mind`, `the-allocation-of-causal-power-in-validation`, `the-brain-does-not-backprop`, `ownership-and-self-worthiness`, `hassabis-frontier-agi-premise`, `mei-you-pu-du-zhi-you-zi-du` |
| **Painterly glass / gold path** | Oil-like strokes, translucent panel, gold or light ribbon through violet haze | `openness-is-consistency`, `a-new-deeper-look-at-antifragility` |
| **Soft pastel abstract** | Powdery dry-brush, muted navy/lavender, simple mass + light curve | `emotional-support-as-causal-interference` |
| **Oil split composition** | Painterly still-life contrast on dark ground (organic cavity vs grid) | `humans-tokens-and-the-scope-of-valuation` |
| **Minimal horizon band** | Near-Rothko: two fields, thin bright seam | `you-wu-zhi-bian` |
| **Ink wash / sumi-e** | Sparse brush, bamboo or scaffolding, large empty ground | `the-scaffolding-we-forget` |
| **Copperplate engraving** | Sepia paper, fine line hatch, technical/architectural plate | `complexity-obscures-emergence-as-the-act-of-mind` |
| **Linocut / woodcut monochrome** | Cream ground, dense black carved doors or relief | `sovereignty-belief-and-regulatory-structures` |
| **Risograph flat print** | Limited ink colors, cream stock, graphic illustration | `the-meaning-of-life-is-in-the-drafting`, `no-system-can-be-kept-closed` |
| **Constructivist poster** | Bold red/black/cream diagonals, hard geometry, thick outlines | `the-scaffolding-we-forget-local-models-as-default` |
| **Cyanotype** | Prussian blue print, paper stain, white plant silhouettes | `the-non-definitive-definition-of-intelligence` |
| **Ukiyo-e / nishiki-e** | Flat woodblock planes, mulberry paper, key-block line, traditional landscape | `what-always-listens-cannot-originate` |
| **Photoreal tableau** | Cinematic or documentary still, real materials, fog/dusk/night | `closed-reality-in-benchmark-maxing`, `production-consumption-and-the-minds-distinction` |
| **Paper craft / tabletop still** | Physical paper objects, soft studio light, beige seamless | `better-than-free-after-the-checklist-closes` |
| **Metaphysical plaza oil** | de Chirico–like arcade, empty frames, hard sun, teal sky | `agi-and-asi-are-temporary-goalposts` |
| **Surreal desert allegory** | Painted open landscape, symbolic props (rulers, frames, scoreboards) | `the-frame-that-conceals-improvement`, `the-question-that-installs-the-war` |
| **Cinematic dual-path** | Photoreal or near-photoreal landscape with luminous forked road | `the-path-drawn-one-step-at-a-time` |
| **Technical blueprint / diazo** | Deep blue print stock, white line work, systems plate, empty title block | `looping-and-graphing` |
| **Stained glass panel** | Leaded jewel-tone panes, cathedral glow, translucent color and grit | `token-efficiency-emulation-and-the-unclosable-gap` |
| **Art Deco poster / chrome and sunburst** | Cream/gold/black geometric sunburst, chrome-brass machine form, stepped chevrons, teal band | `the-flywheel-of-the-mind` |
| **Chinese gongbi fine-line color** | Meticulous outline, mineral-pigment washes on silk-cream ground, botanical-graph hybrid | `a-living-external-cortex` |
| **Wet-plate collodion / ambrotype** | Dark glass plate, silver-black chemical image, emulsion stain, fixed residue as sole readable term | `two-failures-of-trace` |
| **Mingei / katazome stencil** | Handmade washi texture, indigo–charcoal stencil, imperfect dye registration, folk-craft gate and current | `what-works-is-the-belief` |
| **Solarized surreal photograph** | Man Ray–adjacent Sabattier print: metallic silver, inverted midtones, rim glow, chemical grain | `performative-hindsight-that-pretends-to-be-foresight` |
| **Bauhaus primary-color geometry** | Flat primaries on cream stock, thick constructive outlines, hard geometry, silk-screen austerity | `causality-stays-at-the-edge-that-steers` |
| **Cut-paper shadowbox / Scherenschnitte** | Layered cardstock diorama, soft studio shadow, ivory ground, paper craft still | `a-creation-cannot-replace-its-source` |
| **Mezzotint / aquatint** | Velvet black copper-plate print, burnished silver-gray highlights, fine chemical grit, classical plate mark | `not-a-theory-of-everything` |
| **Sand animation / grain board** | Golden sand on dark board, raking light, continuous trail drawn through residual pits, documentary craft still | `causality-all-the-way` |
| **Byzantine glass mosaic** | Gold and ultramarine tesserae, mortar lines, antique glass shine, plaster border, museum-wall light | `evil-as-the-minds-own-creation` |
| **Embroidery / needlework on linen** | Hand-stitched plant and cut scaffold threads on cream linen weave, soft studio textile light, raised stitch shadow | `when-need-stops-being-the-measure` |
| **Sgraffito plaster / scraped fresco** | Layered wall plaster, raking light, deep scrape as luminous interior; shallow surface scratches as flat silhouettes | `the-npc-impression-is-structural` |
| **Suminagashi / floating-ink marbling** | Cream washi, black–indigo ink on water transferred as concentric ripples; wet-paper sheen; effect-lines forming a frame | `when-the-effect-authors-the-frame` |
| **Pinhole / camera obscura photograph** | Soft circular vignette, optical blur, dust motes in raking beam, cream–warm gray, chemical grain; empty-calendar ghost as residue | `closed-reality-in-the-pursuit-of-serendipity` |
| **Cloisonné / enamel medallion** | Antique gold wire cells, multi-scale jewel enamel facets, museum light on glaze and patina; lossy partition of a continuous field | `lossless-knowledge-of-an-open-field-is-incoherent` |
| **Gouache narrative still life** | Matte opaque gouache, cream–charcoal desk scene, clear objects, soft window light; real hand + residue medium + mirror lag | `the-model-never-becomes-a-second-edge` |
| **Dutch Golden Age vanitas still** | Warm umber parchment desk, brass instruments, candle raking light, folio whose diagrams continue past the paper edge into air | `why-mathematics-can-never-be-solved` |
| **Anaglyph red-cyan stereo graphic** | Cream print stock, dual red/cyan channel offset of one form, graphic ink tangle resolving into a single taut cut | `the-ramble-within-the-ramble` |
| **Persian miniature illumination** | Aged ivory parchment, lapis–vermillion–malachite jewel planes, burnished gold borders and path, flat pavilion lattice | `escaping-the-sandbox-stays-inside-the-hold` |
| **Drypoint cartographic plate** | Warm ivory rag paper, sepia iron-gall drypoint, incomplete map with grid continuing past torn edge, field-lines from stylus, plate tone | `the-reality-distortion-field-names-the-closed-map` |
| **Comic halftone / Ben-Day dots** | Cream newsprint, cyan–magenta–black process dots, slight misregistration, graphic speech-mass vs rain on cracked basin | `reality-is-the-minds-ongoing-realization` |
| **Sandblasted glass etching** | Frosted dark glass panel, teal–amber luminous path, grain, museum side light; opened circuit with third node | `therapy-opens-the-feedback-loop` |
| **Soft clay / stop-motion puppet still** | Warm polymer clay board, hand-pressed footprints and short path segments, soft studio light, fingerprint texture | `individual-choices-as-the-only-causal-levers` |

## Inventory (by slug)

| Slug | Style family |
|------|----------------|
| `a-creation-cannot-replace-its-source` | Cut-paper shadowbox / Scherenschnitte |
| `a-living-external-cortex` | Chinese gongbi fine-line color |
| `a-new-deeper-look-at-antifragility` | Painterly glass / gold path |
| `agi-and-asi-are-temporary-goalposts` | Metaphysical plaza oil |
| `better-than-free-after-the-checklist-closes` | Paper craft / tabletop still |
| `causality-all-the-way` | Sand animation / grain board |
| `causality-stays-at-the-edge-that-steers` | Bauhaus primary-color geometry |
| `closed-reality-in-benchmark-maxing` | Photoreal tableau |
| `closed-reality-in-the-pursuit-of-serendipity` | Pinhole / camera obscura photograph |
| `complexity-obscures-emergence-as-the-act-of-mind` | Copperplate engraving |
| `emotional-support-as-causal-interference` | Soft pastel abstract |
| `escaping-the-sandbox-stays-inside-the-hold` | Persian miniature illumination |
| `evil-as-the-minds-own-creation` | Byzantine glass mosaic |
| `hassabis-frontier-agi-premise` | Dark chalk / light trails |
| `humans-tokens-and-the-scope-of-valuation` | Oil split composition |
| `individual-choices-as-the-only-causal-levers` | Soft clay / stop-motion puppet still |
| `intelligence-belongs-only-to-the-mind` | Dark chalk / light trails |
| `looping-and-graphing` | Technical blueprint / diazo |
| `lossless-knowledge-of-an-open-field-is-incoherent` | Cloisonné / enamel medallion |
| `mei-you-pu-du-zhi-you-zi-du` | Dark chalk / light trails |
| `no-system-can-be-kept-closed` | Risograph flat print |
| `not-a-theory-of-everything` | Mezzotint / aquatint |
| `openness-is-consistency` | Painterly glass / gold path |
| `ownership-and-self-worthiness` | Dark chalk / light trails |
| `performative-hindsight-that-pretends-to-be-foresight` | Solarized surreal photograph |
| `production-consumption-and-the-minds-distinction` | Photoreal tableau |
| `reality-is-the-minds-ongoing-realization` | Comic halftone / Ben-Day dots |
| `self-rl-for-humans` | Dark chalk / light trails |
| `sovereignty-belief-and-regulatory-structures` | Linocut / woodcut monochrome |
| `the-allocation-of-causal-power-in-validation` | Dark chalk / light trails |
| `the-brain-does-not-backprop` | Dark chalk / light trails |
| `the-flywheel-of-the-mind` | Art Deco poster / chrome and sunburst |
| `the-frame-that-conceals-improvement` | Surreal desert allegory |
| `the-meaning-of-life-is-in-the-drafting` | Risograph flat print |
| `the-model-never-becomes-a-second-edge` | Gouache narrative still life |
| `the-non-definitive-definition-of-intelligence` | Cyanotype |
| `the-npc-impression-is-structural` | Sgraffito plaster / scraped fresco |
| `the-path-drawn-one-step-at-a-time` | Cinematic dual-path |
| `the-question-that-installs-the-war` | Surreal desert allegory |
| `the-reality-distortion-field-names-the-closed-map` | Drypoint cartographic plate |
| `the-ramble-within-the-ramble` | Anaglyph red-cyan stereo graphic |
| `the-scaffolding-we-forget` | Ink wash / sumi-e |
| `the-scaffolding-we-forget-local-models-as-default` | Constructivist poster |
| `therapy-opens-the-feedback-loop` | Sandblasted glass etching |
| `token-efficiency-emulation-and-the-unclosable-gap` | Stained glass panel |
| `two-failures-of-trace` | Wet-plate collodion / ambrotype |
| `what-always-listens-cannot-originate` | Ukiyo-e / nishiki-e |
| `what-works-is-the-belief` | Mingei / katazome stencil |
| `when-need-stops-being-the-measure` | Embroidery / needlework on linen |
| `when-the-effect-authors-the-frame` | Suminagashi / floating-ink marbling |
| `why-mathematics-can-never-be-solved` | Dutch Golden Age vanitas still |
| `you-wu-zhi-bian` | Minimal horizon band |

## Crowded — prefer not to extend

- **Dark chalk / light trails** (largest set)
- Photoreal tableau and surreal desert allegory (already several landscape stills)

## Unused candidates (pick from here or invent)

Not exhaustive. Prefer something not in Style families above.

- Ceramic glaze still life on porcelain
- Pixel art / limited-palette retro game screen (no UI text)
## Workflow for a new cover

1. Open this file; list families already used.
2. Choose a **new** family (from Unused candidates or invent).
3. Prompt for that medium explicitly; ban crowded defaults (“dark abstract chalk,” “risograph red,” “cinematic fog cube”) unless the essay has no cover and you are replacing a style (then update the row).
4. Generate at **20:9** (`aspect_ratio: "20:9"` when using image tools); resize to 1280×576 if needed; save as `assets/covers/<slug>.jpg`.
5. Append the slug to Inventory and the family row (or add a new Style families row).
6. If a candidate from Unused was taken, move it into Style families and drop it from Unused.

Same asset is reused for Substack paste cover and X Article `cover_media` — do not maintain a second aspect-ratio set.
