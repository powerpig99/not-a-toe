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
| Legacy assets | Keep older covers as installed (many are 16:9). Do **not** bulk-regenerate or re-crop them for 20:9. Regenerate a legacy cover only when the operator explicitly asks for that slug. The site shows each cover at its native aspect ratio (no crop mask). |

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
| **Silverpoint / metalpoint on gesso** | Cream prepared ground, single-weight gray metal lines, paper tooth, museum raking light; stylus lag trail | `qian-yin-hou-guo` |
| **Kintsugi ceramic still life** | Documentary museum still life: ceramic vessel with gold repair seams on a continuous slate ledger grid that tries to absorb the discrete bowl | `the-coordinators-category-error` |
| **Pixel art / limited-palette retro** | Soft cream–indigo-teal limited palette, visible square pixels, gentle dithering; side-scroll tunnel with paved open door vs successive unfinished chambers | `whatever-is-one-prompt-away` |
| **Limestone bas-relief / architectural frieze** | Cream–warm gray stone low relief, museum side light, chisel grain; closed arena rings with open-horizon gap past the bound | `open-vision-in-a-closed-arena` |
| **Scratchboard / white-line scraperboard** | Black India-ink board, fine white blade scrapes, burr texture, museum raking light; density from successive discrete cuts | `having-more-is-never-the-cause` |
| **Graphite pencil study on toned paper** | Warm cream paper, academic cross-hatch, soft graphite gradation, museum raking light; precise instrument with path continuing past the dial | `mistaking-the-expression-for-the-intelligence` |
| **Urushi lacquer / maki-e still** | Deep black lacquer tray, gold maki-e line continuing past the vessel, nested specialty residue on one side only, museum craft light | `ontos-is-a-method-agent` |
| **Charcoal wipe / continuous redraw on newsprint** | Gray newsprint tooth, charcoal path re-drawn over wiped ghost trails, closed catalog of unjoined dots aside, raking side light | `the-real-scarcity-is-not-memory-but-continuous-re-tracing` |
| **Victorian stereograph dual-panel** | Cream antique card mount, twin albumen panels of one coin (obverse/reverse), monocular loupe between that can cover only one face, sepia museum light, chemical grain | `the-paradoxical-nature-of-bystander-insights` |
| **Encaustic wax on wood panel** | Warm beeswax layers, fused color, wood grain, museum raking light; open multi-climate strata under a cooler opaque scoreboard frame and blank gold steward seal | `the-climate-problem-registers-only-as-perception` |
| **Fresco strappo / detached mural fragment** | Warm plaster museum wall, mineral ochre–rose consoling wash over unfinished contour and hatch, open pinholes on raw far edge, raking side light, grit | `sympathy-is-a-placeholder-for-lack-of-clarity` |
| **Security-print guilloche engraving** | Cream rag banknote paper, rose-engine green–umber lattice, sealed supervisory windows with open stock continuing past the hold, plate tone, raking light | `the-risk-is-the-belief-in-oversight-itself` |
| **Palimpsest vellum / multi-ink redraw** | Aged cream vellum, successive translucent iron-gall map layers, ghost cartographies under newest path, bone stylus mid-redraw, raking museum light | `the-strongest-belief-of-the-mind` |
| **Celadon kiln shelf still life** | Pale jade celadon bowl with open residual interior, unworked clay coil beside it, dark kiln shelf, cool museum side light, crackle glaze | `only-if-it-is-not-kept-empty` |
| **Lithographic crayon / stone print** | Warm gray limestone ground, greasy black crayon, plate tone, museum raking light; multi-story scaffold densifying as it extends past the plate edge | `the-scaffolding-that-keeps-growing` |
| **Magic-lantern glass slide still** | Antique hand-painted glass slide on dark wood, fixed translucent figure-on-ladder image, living chalk trail continuing past the glass, amber projection cone + cool museum light | `the-fixed-image-of-transcendence` |
| **Chart-recorder / oscillograph strip** | Aged cream fanfold paper, pen-trace still life, thin early initiating spike then delayed denser oscillatory lag, mechanical grid, raking museum light | `symptom-and-cause-in-the-narratives-of-progress` |
| **Dendrochronology / polished tree-ring section** | Warm ivory linen, polished trunk cross-section, successive growth rings as discrete compounding layers, open cambium edge still living, cream–amber–olive, natural-history museum light | `curiosity-first-the-hidden-engine-of-talent-and-development` |
| **Quipu / knotted-cord still life** | Cream linen ground, horizontal bar with hanging cords of unequal knot sequences, stepped ordered fringe, warm earth fibers, museum raking light | `hierarchy-from-individual-difference` |
| **Miniature proscenium stage still life** | Scale-model wooden theater box, empty stage with hand-mirror, idle lectern and paper audience cutouts aside, cream table, soft museum side light | `when-observation-becomes-performance` |
| **Monotype ghost-print still life** | Cream rag paper, dark first pull beside pale ghost second pull of one plate, inked plate and brayer, overlapping residue as shared-looking field, cool museum side light, ink grain | `the-source-of-shared-change` |
| **Bokashi woodblock / graded indigo print** | Cream washi, indigo lattice gate partially open, warm amber path continuing past the bars into empty ground, imperfect registration, graded washes, raking craft light | `restriction-is-a-selective-tax` |
| **Wire-service teletype / ticker-tape still** | Cream linen table, vintage teletype platen, dual paper ribbons (one continuous clearing print, one fragmented re-readings), brass keys and ink spool, cool museum side light, no legible text | `price-as-utterance-understanding-as-trade` |
| **Camera lucida / brass prism drawing still** | Cream writing desk, brass camera lucida over open notebook, abstract ink trail without portrait or legible text, optical glass reflecting only paper, museum raking light, craft grain | `writing-without-the-image` |
| **Marine pilot chart / sailing-directions still** | Cream linen desk, open abstract current chart without legible text, amber wake-line continuing past torn edge into empty paper, brass dividers and pocket compass as instruments only, cool museum side light | `expertise-as-reference-not-replacement` |
| **Iron-filing magnetograph / scientific plate** | Warm cream rag paper, fine black iron filings in dense aligned field-line clusters, one off-axis misaligned cluster, archival grain, museum side light, no text | `preference-clusters-and-the-language-of-judgment` |
| **Glass-dome museum terrestrial model still** | Cream pedestal, sealed glass dome over hyper-detailed miniature Earth, worn walking path continuing past the case on polished floor, cool museum side light, documentary grain | `the-presumption-of-agi-and-the-view-from-outside` |
| **Brass iris diaphragm still** | Precision brass camera aperture on dark velvet, blades mostly closed with a thin light cone through a partial opening, cool studio craft light, documentary metal grain | `advocating-openness-of-others-is-a-desire-for-closure-of-the-self` |
| **Egg tempera / gesso panel still** | Cream gesso wood panel, matte mineral egg-tempera pigments, fine craquelure; nested open doorways through successive rooms, rearranged furniture in the near hold, clearer empty light beyond | `how-belief-actually-changes` |
| **Phenakistoscope / stopped zoetrope still** | Cream linen table, Victorian spinning disk stopped so discrete painted panels read as separate private frames, viewing slit-card aside, soft museum raking light, craft wood grain | `shared-humanity-is-never-shared` |
| **Coining-die pair / mint-die still** | Cream linen mint bench, matched antique coining dies face-to-face with empty gap between, no coin present, cool raking craft light, brass–steel grain | `good-and-evil-are-the-two-sides-of-the-coin-and-the-cut` |
| **Sealing-wax / official seal still** | Cream linen desk, antique sealing wax and blank-faced metal seal matrix, sealed document vs open unmarked sheet continuing past the frame, cool raking craft light, wax gloss and paper tooth | `empowerment-establishes-the-centralization-of-power` |
| **Processional figure / portable shrine still** | Cream linen craft table, folk-craft blank-faced wooden figure on carrying poles, supporting hands mid-elevation, empty pedestal with worn ring, cool raking museum light, ivory–umber–charcoal | `externalized-virtue-becomes-its-opposite` |
| **Photogram / cameraless object print** | Pure black photographic paper, cream border, white silhouettes of feather and airfoil, chemical silver grain, soft edge bloom, archival cameraless print | `the-flight-analogy-leaves-the-mind-untouched` |
| **Terrazzo / polished aggregate still** | Cream linen craft table, polished terrazzo sample slab, discrete multi-colored chips denser on one side with isolated chips alone, cool museum side light, mineral grain | `data-is-local-intelligence-is-allocated` |
| **Möbius paper sculpture still** | Seamless warm ivory tabletop, single continuous twisted cream cotton-paper band as closed loop, soft studio side light, paper tooth and fiber, quiet craft still | `no-outside-jumps-closed-loops-and-the-unreplicable-autonomy-of-mind` |
| **Natural-history specimen drawer still** | Cream wood museum drawer, felt-lined cells with unique eggs and small bird forms as discrete cases, closed brass type-loop medallion set aside, archival raking light | `exceptionality-perception-and-the-self-limiting-field-of-problems` |
| **Porcelain mold / residual clay still** | Cream linen craft table, blank white porcelain mold as uniform template, wet clay mid-press into the mold, free hand-thrown vessels of divergent silhouettes aside, cool museum side light, clay tooth and glaze sheen | `the-belief-in-utopia-is-the-path-to-dystopia` |
| **Workshop pegboard still** | Cream pegboard wall, empty hooks in sequence with mid-row tools temporarily hung, soft raking workshop light, documentary craft grain | `the-utility-men-of-progress` |
| **Lost-wax investment casting still** | Cream linen craft table, cracked ceramic shell shards as abundant residue, empty mold cavity, thin bronze pour trail already off-frame, cool museum side light | `the-illusion-of-free-intelligence` |
| **Trompe-l’oeil recursive frame still** | Cream museum wall, gilt outer frame holding a gallery scene that itself holds the same framed scene nested smaller, oil trompe-l’oeil depth, raking light, canvas weave | `self-image-speaks-as-if-from-nowhere` |
| **Mirror galvanometer / optical-lever still** | Cream linen craft table, antique brass mirror galvanometer, successive glass reflections amplifying a thin beam into a long trail past the scale frame, cool museum side light, brass–glass grain | `the-artifacts-of-self-amplification` |

## Inventory (by slug)

| Slug | Style family |
|------|----------------|
| `advocating-openness-of-others-is-a-desire-for-closure-of-the-self` | Brass iris diaphragm still |
| `a-creation-cannot-replace-its-source` | Cut-paper shadowbox / Scherenschnitte |
| `a-living-external-cortex` | Chinese gongbi fine-line color |
| `a-new-deeper-look-at-antifragility` | Painterly glass / gold path |
| `agi-and-asi-are-temporary-goalposts` | Metaphysical plaza oil |
| `better-than-free-after-the-checklist-closes` | Paper craft / tabletop still |
| `the-paradoxical-nature-of-bystander-insights` | Victorian stereograph dual-panel |
| `causality-all-the-way` | Sand animation / grain board |
| `causality-stays-at-the-edge-that-steers` | Bauhaus primary-color geometry |
| `closed-reality-in-benchmark-maxing` | Photoreal tableau |
| `closed-reality-in-the-pursuit-of-serendipity` | Pinhole / camera obscura photograph |
| `complexity-obscures-emergence-as-the-act-of-mind` | Copperplate engraving |
| `curiosity-first-the-hidden-engine-of-talent-and-development` | Dendrochronology / polished tree-ring section |
| `data-is-local-intelligence-is-allocated` | Terrazzo / polished aggregate still |
| `emotional-support-as-causal-interference` | Soft pastel abstract |
| `exceptionality-perception-and-the-self-limiting-field-of-problems` | Natural-history specimen drawer still |
| `empowerment-establishes-the-centralization-of-power` | Sealing-wax / official seal still |
| `escaping-the-sandbox-stays-inside-the-hold` | Persian miniature illumination |
| `evil-as-the-minds-own-creation` | Byzantine glass mosaic |
| `expertise-as-reference-not-replacement` | Marine pilot chart / sailing-directions still |
| `externalized-virtue-becomes-its-opposite` | Processional figure / portable shrine still |
| `good-and-evil-are-the-two-sides-of-the-coin-and-the-cut` | Coining-die pair / mint-die still |
| `preference-clusters-and-the-language-of-judgment` | Iron-filing magnetograph / scientific plate |
| `hassabis-frontier-agi-premise` | Dark chalk / light trails |
| `having-more-is-never-the-cause` | Scratchboard / white-line scraperboard |
| `hierarchy-from-individual-difference` | Quipu / knotted-cord still life |
| `how-belief-actually-changes` | Egg tempera / gesso panel still |
| `humans-tokens-and-the-scope-of-valuation` | Oil split composition |
| `individual-choices-as-the-only-causal-levers` | Soft clay / stop-motion puppet still |
| `intelligence-belongs-only-to-the-mind` | Dark chalk / light trails |
| `the-illusion-of-free-intelligence` | Lost-wax investment casting still |
| `looping-and-graphing` | Technical blueprint / diazo |
| `lossless-knowledge-of-an-open-field-is-incoherent` | Cloisonné / enamel medallion |
| `mei-you-pu-du-zhi-you-zi-du` | Dark chalk / light trails |
| `mistaking-the-expression-for-the-intelligence` | Graphite pencil study on toned paper |
| `no-outside-jumps-closed-loops-and-the-unreplicable-autonomy-of-mind` | Möbius paper sculpture still |
| `no-system-can-be-kept-closed` | Risograph flat print |
| `not-a-theory-of-everything` | Mezzotint / aquatint |
| `open-vision-in-a-closed-arena` | Limestone bas-relief / architectural frieze |
| `openness-is-consistency` | Painterly glass / gold path |
| `ontos-is-a-method-agent` | Urushi lacquer / maki-e still |
| `ownership-and-self-worthiness` | Dark chalk / light trails |
| `performative-hindsight-that-pretends-to-be-foresight` | Solarized surreal photograph |
| `price-as-utterance-understanding-as-trade` | Wire-service teletype / ticker-tape still |
| `production-consumption-and-the-minds-distinction` | Photoreal tableau |
| `reality-is-the-minds-ongoing-realization` | Comic halftone / Ben-Day dots |
| `restriction-is-a-selective-tax` | Bokashi woodblock / graded indigo print |
| `self-rl-for-humans` | Dark chalk / light trails |
| `self-image-speaks-as-if-from-nowhere` | Trompe-l’oeil recursive frame still |
| `shared-humanity-is-never-shared` | Phenakistoscope / stopped zoetrope still |
| `sovereignty-belief-and-regulatory-structures` | Linocut / woodcut monochrome |
| `symptom-and-cause-in-the-narratives-of-progress` | Chart-recorder / oscillograph strip |
| `sympathy-is-a-placeholder-for-lack-of-clarity` | Fresco strappo / detached mural fragment |
| `the-artifacts-of-self-amplification` | Mirror galvanometer / optical-lever still |
| `the-allocation-of-causal-power-in-validation` | Dark chalk / light trails |
| `the-brain-does-not-backprop` | Dark chalk / light trails |
| `the-climate-problem-registers-only-as-perception` | Encaustic wax on wood panel |
| `the-coordinators-category-error` | Kintsugi ceramic still life |
| `the-fixed-image-of-transcendence` | Magic-lantern glass slide still |
| `the-flight-analogy-leaves-the-mind-untouched` | Photogram / cameraless object print |
| `the-flywheel-of-the-mind` | Art Deco poster / chrome and sunburst |
| `the-frame-that-conceals-improvement` | Surreal desert allegory |
| `the-meaning-of-life-is-in-the-drafting` | Risograph flat print |
| `the-model-never-becomes-a-second-edge` | Gouache narrative still life |
| `the-non-definitive-definition-of-intelligence` | Cyanotype |
| `the-npc-impression-is-structural` | Sgraffito plaster / scraped fresco |
| `the-path-drawn-one-step-at-a-time` | Cinematic dual-path |
| `the-presumption-of-agi-and-the-view-from-outside` | Glass-dome museum terrestrial model still |
| `the-question-that-installs-the-war` | Surreal desert allegory |
| `the-reality-distortion-field-names-the-closed-map` | Drypoint cartographic plate |
| `the-risk-is-the-belief-in-oversight-itself` | Security-print guilloche engraving |
| `the-ramble-within-the-ramble` | Anaglyph red-cyan stereo graphic |
| `the-real-scarcity-is-not-memory-but-continuous-re-tracing` | Charcoal wipe / continuous redraw on newsprint |
| `the-scaffolding-that-keeps-growing` | Lithographic crayon / stone print |
| `the-scaffolding-we-forget` | Ink wash / sumi-e |
| `the-scaffolding-we-forget-local-models-as-default` | Constructivist poster |
| `the-source-of-shared-change` | Monotype ghost-print still life |
| `the-strongest-belief-of-the-mind` | Palimpsest vellum / multi-ink redraw |
| `the-utility-men-of-progress` | Workshop pegboard still |
| `therapy-opens-the-feedback-loop` | Sandblasted glass etching |
| `token-efficiency-emulation-and-the-unclosable-gap` | Stained glass panel |
| `two-failures-of-trace` | Wet-plate collodion / ambrotype |
| `what-always-listens-cannot-originate` | Ukiyo-e / nishiki-e |
| `what-works-is-the-belief` | Mingei / katazome stencil |
| `the-belief-in-utopia-is-the-path-to-dystopia` | Porcelain mold / residual clay still |
| `whatever-is-one-prompt-away` | Pixel art / limited-palette retro |
| `when-need-stops-being-the-measure` | Embroidery / needlework on linen |
| `when-observation-becomes-performance` | Miniature proscenium stage still life |
| `when-the-effect-authors-the-frame` | Suminagashi / floating-ink marbling |
| `why-mathematics-can-never-be-solved` | Dutch Golden Age vanitas still |
| `writing-without-the-image` | Camera lucida / brass prism drawing still |
| `qian-yin-hou-guo` | Silverpoint / metalpoint on gesso |
| `you-wu-zhi-bian` | Minimal horizon band |
| `only-if-it-is-not-kept-empty` | Celadon kiln shelf still life |

## Crowded — prefer not to extend

- **Dark chalk / light trails** (largest set)
- Photoreal tableau and surreal desert allegory (already several landscape stills)

## Unused candidates (pick from here or invent)

Not exhaustive. Prefer something not in Style families above.

## Workflow for a new cover

1. Open this file; list families already used.
2. Choose a **new** family (from Unused candidates or invent).
3. Prompt for that medium explicitly; ban crowded defaults (“dark abstract chalk,” “risograph red,” “cinematic fog cube”) unless the essay has no cover and you are replacing a style (then update the row).
4. Generate at **20:9** (`aspect_ratio: "20:9"` when using image tools); resize to 1280×576 if needed; save as `assets/covers/<slug>.jpg`.
5. Append the slug to Inventory and the family row (or add a new Style families row).
6. If a candidate from Unused was taken, move it into Style families and drop it from Unused.

Same asset is reused for Substack paste cover and X Article `cover_media` — do not maintain a second aspect-ratio set.
