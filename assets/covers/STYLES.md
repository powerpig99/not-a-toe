# Cover styles

Living inventory for essay covers in this folder. Filename = essay slug (`content/posts/<slug>.md` → `assets/covers/<slug>.jpg`). Install as landscape **20:9** JPEG (or jpeg/png/webp) at **1280×576** — the shared aspect for site, Substack featured image, and X Article cover.

| Related | Path |
|---------|------|
| Post authoring | [`content/posts/README.md`](../../content/posts/README.md) |
| Paste export (Substack + X Article) | [`docs/export-for-substack.md`](../../docs/export-for-substack.md) — one absolute-markdown file |
| X Article API (parked) | [`docs/export-for-x-article.md`](../../docs/export-for-x-article.md) |
| Local memory / sleep audit | [`docs/local-memory.md`](../../docs/local-memory.md) |

## Principle

**Pick a style that is actually different — do not converge.**

Concept may echo the essay; medium and look must not. Differentiation is on **style** (medium, print/photo tradition, palette discipline, rendering method)—not on subject alone. Two dark chalk abstracts on black are the same style even if one has orbits and the other has a spiral.

### Default lag to relax: “still life / tabletop still”

Recent agent covers have **over-defaulted to stills** — museum craft tables, linen desks, prop arrays, soft side light, “documentary still life” framing. That is Image lag: a safe house look frozen as the cover form.

| Prefer | Avoid as the automatic next pick |
|--------|----------------------------------|
| Print traditions, full-bleed fields, landscapes, diagrams, textile/pattern, abstract media, cinematic or graphic whole-frame | “X still,” “still life,” “craft table,” “museum side light + prop on linen” as the first idea |
| Inventing a medium not in Style families | Another tabletop arrangement with a different prop |

When the concept is “fold,” “mirror,” “tool,” “residue,” or “coin,” **do not** answer with another still-life prop shot. Force a different medium first.

### Cream-linen / craft-table cluster (still crowded)

Cream-linen / museum craft-table documentary stills (brass prop + paper + cool side light) remain **saturated**. Prefer any other family or invent before adding another.

### When unused styles run thin

1. **First:** invent a genuine new family (name medium + tradition + palette) not listed in Style families.
2. **If invention stalls:** **randomly reuse** an existing family from the inventory — pick at random among used families, **not** the most recent one and **not** the largest crowded sets (Dark chalk; cream-linen stills; photoreal/surreal landscape stills).
3. **Never** settle into one fixed house style (especially stills) because it is easy. Variation across the set is the goal; reuse is for diversity under exhaustion, not for comfort.

**New family when possible; random used family when not — never converge.**

## Spec

| Rule | Detail |
|------|--------|
| Aspect | Prefer **20:9** landscape when the generator offers it (X Article cover compatibility). **16:9 as-is is fine** — install native aspect; **do not crop** to force 20:9. Site/Substack share the same file at native ratio (no crop mask). |
| Size | Prefer **1280×576** for 20:9; for 16:9, **1280×720** (or native download) is fine |
| Text | None (no title, no logo, no legible caption) |
| Fit | Concept reads the essay’s cut; style is independent of other covers |
| Not | Square, portrait, 3:1 profile-banner, or other non-landscape crops as the essay cover |
| After generate | Install as `<slug>.jpg`, update Inventory + Style families below |
| Imagine Image 2.0 | Quality Mode on **grok.com/imagine** (+ mobile); API for 2.0 still coming soon. Grok Build `image_gen` has no model pick. Widest consumer ratio currently **16:9** — install as-is. |
| Legacy assets | Keep older covers as installed. Do **not** bulk-regenerate for aspect. Regenerate a legacy cover only when the operator explicitly asks for that slug. |

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
| **Marquetry / wood-inlay panel** | Warm walnut–maple grain, darker veneer path rising then flattening against a hard rectangular ebony border, open uncut grain continuing past the frame, museum raking light, craft glue lines | `closed-assumptions-squeeze-compounding-into-s-curves` |
| **Trompe-l’oeil recursive frame still** | Cream museum wall, gilt outer frame holding a gallery scene that itself holds the same framed scene nested smaller, oil trompe-l’oeil depth, raking light, canvas weave | `self-image-speaks-as-if-from-nowhere` |
| **Mirror galvanometer / optical-lever still** | Cream linen craft table, antique brass mirror galvanometer, successive glass reflections amplifying a thin beam into a long trail past the scale frame, cool museum side light, brass–glass grain | `the-artifacts-of-self-amplification` |
| **Damascus / pattern-welded steel macro** | Full-bleed metallurgical macro, cold gray–black laminated striations folding denser into themselves, hard industrial rake light, oil sheen and forge scale, no tabletop props | `intelligence-folding-back-on-itself` |

| **Laboratory glassware still / sealed continuous curve** | Cream linen lab desk, graduated cylinder with continuous amber gradient, black stopper seal, continuous pencil curve under hard black rectangular seal plate, cool museum side light, no text | `the-reversal-from-defensible-claim-to-dogma` |
| **Assay touchstone / gold-streak still** | Cream linen craft table, black basalt touchstone with gold purity streaks as fixed standard, diverse metal samples forced into comparison against one streak, brass touch needles, cool museum side light | `the-source-of-all-harm` |
| **Medieval volvelle / paper dial still** | Layered circular parchment dials, nested rotating discs with abstract non-legible marks, one disc sealed by blank wax tab while map grid continues past torn edge, cool museum raking light, paper tooth | `the-real-lesson-from-the-consciousness-vector-paper` |
| **Wooden pigeon-hole sorter still** | Vintage wood cubby row on cream linen, most compartments sealed flush with blank plugs, one open hole with continuous blank ribbon trail continuing past the instrument, cool museum side light, craft grain | `the-price-of-closing-optionality` |
| **Batik / wax-resist dye on cotton** | Cream cotton, indigo wax-resist lattice as unbroken average field, one white wax trail rupturing a cell and continuing past fabric edge, craft-studio side light, cloth weave and crackled wax | `the-reality-distortion-field-inverts-the-baseline` |
| **Pepper’s ghost theatrical still** | Cream linen stage table, tilted glass plate projecting translucent sealed-vault silhouette, densified blank institutional seals aside, open instrument notebook and brass dividers as ordinary craft tools, cool museum side light | `the-imagining-of-ai-risk` |
| **Mola reverse-appliqué textile** | Layered indigo–coral–cream cotton, two independent cut-layer motifs with only a narrow central band of partial intersection, residual uncut top cloth outside, hand-stitch texture, cool museum craft light | `shared-consciousness-is-intersecting-individualities` |
| **Origami / continuous-sheet folded stair still** | Single cream paper sheet folded into discrete ascending terraces, continuous fiber from base to peak, soft museum side light, ivory–warm-gray, paper tooth and crease shadow only | `climbing-does-not-leave-the-ground` |
| **Notarial embosser / dry-seal still** | Cream linen craft table, antique brass notarial embosser, one raised blank seal impressed on cream vellum as finished identity, unmarked sheet continuing past the emboss, cool museum raking light, brass–paper grain | `liberation-rhetoric-begins-by-defining-captivity` |
| **Exchequer counting-board still** | Dark oak desk, black-and-cream chequered cloth, wooden and brass counters mid-transfer from depleted private pile to ordered public squares, blank brass nameplate over the public side, split tally sticks, cool museum raking light | `public-spending-does-not-create-capital` |
| **Schlieren optical still** | Dark lab field, collimated light revealing invisible density gradients around a cabin silhouette; rigid price-scoreboard frame capturing only partial bands while protective flow continues past it; silver-blue charcoal optical grain | `ownership-cost-freezes-lagged-averages-as-vehicle-property` |
| **Operant maze / conditioning apparatus still** | Cream linen museum table, wooden laboratory maze, pellet dispensers on short dependency paths, longer unsubsidized path without dispensers, cool museum side light, brass–wood craft grain | `the-myth-of-population-collapse-explained` |
| **Open assay balance still** | Cream linen museum table, antique dual-pan assay balance with visible knife-edge, pans unequal mid-weigh under continuous open adjustment, cool side light continuing past both pans into empty space, brass–ivory craft grain | `pessimism-is-the-shadow-of-optimism` |
| **Crossed-polarizers optical-bench still** | Cream linen lab table, two circular polarizing glass filters on brass mounts partially rotated, residual luminous band through incomplete extinction continuing past the bench edge, cool museum side light, glass–metal grain | `the-hard-problem-of-consciousness-is-consistent-with-learning` |
| **Deep-space orbital epicycle diagram** | Photoreal Earth on starfield, successive thin-line epicycle systems in cream→blue→amber→green→violet increasing formal complexity left-to-right, deep navy void, no craft table | `the-rational-choice-postulate-is-the-original-sin` |
| **Gilded reliquary / monstrance still** | Cream linen craft table, ornate gold protective casing and glass window claiming to safeguard a sacred light, bare candle flame continuing past the glass into empty air, cool museum raking light, brass–glass grain | `the-free-mind-is-displaced-by-what-claims-to-protect-it` |
| **Dual-epoch residual continuum still** | Split field: warm ochre cave clay (carved face, pot, tablets, gear) into cool blue wireframe neural head and circuit mesh; essay equation as sole legible center; dust-to-data continuum, no second substrate | `technology-is-residual-of-human-compounding` |
| **Industrial gear dissolving into residual waves** | Dark industrial left: large brass–iron gear and piston on tiled floor; center shatter of dark fragments; right luminous amber–cream flowing wave layers as residue continuum; cinematic split light | `the-average-is-residue-not-the-engine` |
| **Graphite ridge / luminous edge abstract** | Dark charcoal–graphite surface with fine grain, soft ridge crest, translucent amber–orange luminous layers flowing only at the far edge into empty dark field; residual mass vs active perimeter, no props | `residual-control-recedes-to-the-edge` |
| **Cinematic silhouette / luminous network spiral** | Dark rocky overlook, lone silhouette facing golden network spiral and bright core, mist and star-field void, digital-cinematic light | `consciousness-never-appears-as-data-among-data` |
| **Geometric mesh dissolving into alpine panorama** | Cream paper left: blue–ochre circle/triangle network and low-poly shards fracturing at a vertical seam; right photoreal misty mountain valley and lake under broken sky; abstract inventory edge into open territory | `abstraction-boundaries-and-the-moving-edge-of-reality` |
| **Cinematic dual-landscape monadnock** | Split cool fog / warm cosmic sky; standing rock with luminous golden tree-of-light and starfield cut; cool node-graph linking into the monadnock; roots as residual light into dark terrain | `causality-and-the-irreducible-prior` |
| **Dual-terrain photoreal footstep** | Split cracked basalt / luminous water, bare foot mid-step on fractured edge, cool–warm atmospheric light, painterly photoreal allegory | `hardness-is-not-inherent-in-the-action` |
| **Cinematic chip–network dual** | Dark void; isometric black microchip with golden fiber fan left of a jagged crack boundary; purple–blue particle wave mesh and node graph right; digital-cinematic light | `hardware-locality-is-not-the-information-boundary` |
| **Painterly chamber / luminous infinity dual** | Oil-like strokes; dark stone arch with chalk triangle-circle mark and stepped plinth left; golden ∞ over open valley path with geometric diagram haze right; cream–umber–gold | `potential-infinity-and-the-temporary-closures-of-mathematical-thought` |
| **Mixed-media profile / geometric residue field** | Cream paper ground; closed-eye face in profile dissolving into navy–ochre geometric lattice, ink spatter, and flowing residual lines; mixed-media collage | `residual-individualism` |
| **Cinematic overlook / golden growth-path** | Photoreal mountain overlook at dawn, figure on cliff with books and globe, stone path into mist, luminous golden ascending arrow and particle trails toward sunrise | `cheng-gong-xue` |
| **Photoreal balance-scale allegory** | Cracked earth, stone fulcrum seesaw; money-bag low vs grain sacks high with red up-arrows; dashed transfer trails; cool city / warm arid dual light | `the-reversal-of-causality-in-wealth-transfer-policies-and-price-floors` |
| **Dual-field spiral feedback allegory** | Split red storm / deep-teal circuit fields; concentric arrow rings around a silhouetted figure on a ridge in a luminous center aperture; constellation and circuit-line overlays, cracked-paint texture | `moral-language-dilutes-the-feedback-that-scales-freedom` |
| **Split-nave / root-mass cinematic allegory** | Full-bleed split field: cracked classical hall with geometric star and labyrinth left; dark root-mass with embedded faces and red veins right; central figure bisected by a thin red cut | `the-initial-distinction` |
| **Wayang kulit / shadow-puppet screen** | Full-bleed amber backlit cotton screen, oil-lamp glow; large speaker-at-podium silhouette composed by many small hand-shadows and puppet figures along the lower edge; no table, no text | `politicians-appear-as-visible-symptoms-of-responsibility-diffusion` |
| **Industrial-node constellation / gold spiral** | Dark navy atmospheric field, gold particle spiral core, cyan factory/vehicle/chip icon-nodes on a thin-edge graph, orange accent nodes | `guan-yu-gui-yin` |
| **Monumental ranking hall / concrete interior** | Cool concrete hall, mixed stone–wood vertical bars, three horizontal luminous lines, lone figure facing the outlier column, raking window light, polished floor | `the-hours-ranking-freezes-adequacy-as-one-scoreboard` |
| **Cinematic alpine trail / parchment map** | Photoreal mountain valley at sunrise, worn dirt path through fog, rolled parchment route-map in the foreground, title set in the sky | `the-map-after-the-territory` |
| **Cinematic dual-bank / cracked-sphere allegory** | Photoreal split landscape: storm-barren bank with seated observer, sunlit valley with standing figure, river cut, cracked stone sphere and eye between | `sowell-observed-the-surface-problem` |
| **Ink-wash to cosmic-diagram panorama** | Full-bleed split: sepia ink landscape, bamboo slip and brush left; gold river seam; indigo constellation, open diagram-book and geodesic sphere right | `du-zhongwen-zhexue-jianshi-you-gan` |
| **Cinematic split-ledger / crack-bisected figure** | Full-bleed dual field: warm sunlit path and glowing personal ledger left; vertical earth-crack through a back-turned figure; cold ruin, scales, fractured colossal head, and crowd right | `the-irreducible-prior-of-decision-and-consequence` |
| **Cinematic sealed-chamber / luminous-mind dual** | Full-bleed split: dark circular vault, checkerboard, glass cubes and geodesic sphere left; golden mountain pass, figure on cliff, translucent neural head and branching tree right | `on-closed-systems-open-minds-and-the-limits-of-proof` |
| **Particle-flow compounding panorama** | Dark navy void; silver bell-curve dissolving into particle scatter; three orbital spheres (factory, tree, circuit); silver-to-gold compounding streams | `mi-lv-shi-jie-guo-de-biao-xiang` |
| **Aerial pack-ice / polar lead** | Full-bleed downward aerial; discrete silver-blue floes of uneven size on charcoal open water; raking polar light; crystalline grain; field never reconstitutes into one sheet | `the-knowledge-problem-and-the-illusion-of-delegation` |
| **Cinematic mist-to-gold compounding panorama** | Cool fog and white point-cloud bell left; golden winding path through dark mountains; steep gold particle spike right with climbing silhouettes | `power-law-is-the-long-term-consequence-of-normal-distribution` |

## Inventory (by slug)

| Slug | Style family |
|------|----------------|
| `abstraction-boundaries-and-the-moving-edge-of-reality` | Geometric mesh dissolving into alpine panorama |
| `advocating-openness-of-others-is-a-desire-for-closure-of-the-self` | Brass iris diaphragm still |
| `a-creation-cannot-replace-its-source` | Cut-paper shadowbox / Scherenschnitte |
| `a-living-external-cortex` | Chinese gongbi fine-line color |
| `a-new-deeper-look-at-antifragility` | Painterly glass / gold path |
| `agi-and-asi-are-temporary-goalposts` | Metaphysical plaza oil |
| `better-than-free-after-the-checklist-closes` | Paper craft / tabletop still |
| `the-paradoxical-nature-of-bystander-insights` | Victorian stereograph dual-panel |
| `causality-all-the-way` | Sand animation / grain board |
| `cheng-gong-xue` | Cinematic overlook / golden growth-path |
| `causality-and-the-irreducible-prior` | Cinematic dual-landscape monadnock |
| `causality-stays-at-the-edge-that-steers` | Bauhaus primary-color geometry |
| `climbing-does-not-leave-the-ground` | Origami / continuous-sheet folded stair still |
| `closed-assumptions-squeeze-compounding-into-s-curves` | Marquetry / wood-inlay panel |
| `closed-reality-in-benchmark-maxing` | Photoreal tableau |
| `closed-reality-in-the-pursuit-of-serendipity` | Pinhole / camera obscura photograph |
| `complexity-obscures-emergence-as-the-act-of-mind` | Copperplate engraving |
| `consciousness-never-appears-as-data-among-data` | Cinematic silhouette / luminous network spiral |
| `curiosity-first-the-hidden-engine-of-talent-and-development` | Dendrochronology / polished tree-ring section |
| `data-is-local-intelligence-is-allocated` | Terrazzo / polished aggregate still |
| `du-zhongwen-zhexue-jianshi-you-gan` | Ink-wash to cosmic-diagram panorama |
| `emotional-support-as-causal-interference` | Soft pastel abstract |
| `exceptionality-perception-and-the-self-limiting-field-of-problems` | Natural-history specimen drawer still |
| `empowerment-establishes-the-centralization-of-power` | Sealing-wax / official seal still |
| `escaping-the-sandbox-stays-inside-the-hold` | Persian miniature illumination |
| `evil-as-the-minds-own-creation` | Byzantine glass mosaic |
| `expertise-as-reference-not-replacement` | Marine pilot chart / sailing-directions still |
| `externalized-virtue-becomes-its-opposite` | Processional figure / portable shrine still |
| `good-and-evil-are-the-two-sides-of-the-coin-and-the-cut` | Coining-die pair / mint-die still |
| `guan-yu-gui-yin` | Industrial-node constellation / gold spiral |
| `preference-clusters-and-the-language-of-judgment` | Iron-filing magnetograph / scientific plate |
| `hardness-is-not-inherent-in-the-action` | Dual-terrain photoreal footstep |
| `hardware-locality-is-not-the-information-boundary` | Cinematic chip–network dual |
| `hassabis-frontier-agi-premise` | Dark chalk / light trails |
| `having-more-is-never-the-cause` | Scratchboard / white-line scraperboard |
| `hierarchy-from-individual-difference` | Quipu / knotted-cord still life |
| `how-belief-actually-changes` | Egg tempera / gesso panel still |
| `humans-tokens-and-the-scope-of-valuation` | Oil split composition |
| `individual-choices-as-the-only-causal-levers` | Soft clay / stop-motion puppet still |
| `intelligence-belongs-only-to-the-mind` | Dark chalk / light trails |
| `intelligence-folding-back-on-itself` | Damascus / pattern-welded steel macro |
| `liberation-rhetoric-begins-by-defining-captivity` | Notarial embosser / dry-seal still |
| `the-illusion-of-free-intelligence` | Lost-wax investment casting still |
| `the-irreducible-prior-of-decision-and-consequence` | Cinematic split-ledger / crack-bisected figure |
| `the-knowledge-problem-and-the-illusion-of-delegation` | Aerial pack-ice / polar lead |
| `the-initial-distinction` | Split-nave / root-mass cinematic allegory |
| `the-imagining-of-ai-risk` | Pepper’s ghost theatrical still |
| `looping-and-graphing` | Technical blueprint / diazo |
| `lossless-knowledge-of-an-open-field-is-incoherent` | Cloisonné / enamel medallion |
| `mei-you-pu-du-zhi-you-zi-du` | Dark chalk / light trails |
| `mi-lv-shi-jie-guo-de-biao-xiang` | Particle-flow compounding panorama |
| `moral-language-dilutes-the-feedback-that-scales-freedom` | Dual-field spiral feedback allegory |
| `mistaking-the-expression-for-the-intelligence` | Graphite pencil study on toned paper |
| `no-outside-jumps-closed-loops-and-the-unreplicable-autonomy-of-mind` | Möbius paper sculpture still |
| `no-system-can-be-kept-closed` | Risograph flat print |
| `not-a-theory-of-everything` | Mezzotint / aquatint |
| `open-vision-in-a-closed-arena` | Limestone bas-relief / architectural frieze |
| `openness-is-consistency` | Painterly glass / gold path |
| `pessimism-is-the-shadow-of-optimism` | Open assay balance still |
| `power-law-is-the-long-term-consequence-of-normal-distribution` | Cinematic mist-to-gold compounding panorama |
| `politicians-appear-as-visible-symptoms-of-responsibility-diffusion` | Wayang kulit / shadow-puppet screen |
| `ontos-is-a-method-agent` | Urushi lacquer / maki-e still |
| `ownership-and-self-worthiness` | Dark chalk / light trails |
| `ownership-cost-freezes-lagged-averages-as-vehicle-property` | Schlieren optical still |
| `performative-hindsight-that-pretends-to-be-foresight` | Solarized surreal photograph |
| `potential-infinity-and-the-temporary-closures-of-mathematical-thought` | Painterly chamber / luminous infinity dual |
| `price-as-utterance-understanding-as-trade` | Wire-service teletype / ticker-tape still |
| `production-consumption-and-the-minds-distinction` | Photoreal tableau |
| `public-spending-does-not-create-capital` | Exchequer counting-board still |
| `reality-is-the-minds-ongoing-realization` | Comic halftone / Ben-Day dots |
| `restriction-is-a-selective-tax` | Bokashi woodblock / graded indigo print |
| `self-rl-for-humans` | Dark chalk / light trails |
| `self-image-speaks-as-if-from-nowhere` | Trompe-l’oeil recursive frame still |
| `shared-consciousness-is-intersecting-individualities` | Mola reverse-appliqué textile |
| `shared-humanity-is-never-shared` | Phenakistoscope / stopped zoetrope still |
| `sovereignty-belief-and-regulatory-structures` | Linocut / woodcut monochrome |
| `sowell-observed-the-surface-problem` | Cinematic dual-bank / cracked-sphere allegory |
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
| `the-free-mind-is-displaced-by-what-claims-to-protect-it` | Gilded reliquary / monstrance still |
| `the-hard-problem-of-consciousness-is-consistent-with-learning` | Crossed-polarizers optical-bench still |
| `the-hours-ranking-freezes-adequacy-as-one-scoreboard` | Monumental ranking hall / concrete interior |
| `the-frame-that-conceals-improvement` | Surreal desert allegory |
| `the-map-after-the-territory` | Cinematic alpine trail / parchment map |
| `the-meaning-of-life-is-in-the-drafting` | Risograph flat print |
| `the-model-never-becomes-a-second-edge` | Gouache narrative still life |
| `the-myth-of-population-collapse-explained` | Operant maze / conditioning apparatus still |
| `the-non-definitive-definition-of-intelligence` | Cyanotype |
| `the-npc-impression-is-structural` | Sgraffito plaster / scraped fresco |
| `the-path-drawn-one-step-at-a-time` | Cinematic dual-path |
| `the-presumption-of-agi-and-the-view-from-outside` | Glass-dome museum terrestrial model still |
| `the-price-of-closing-optionality` | Wooden pigeon-hole sorter still |
| `the-question-that-installs-the-war` | Surreal desert allegory |
| `the-rational-choice-postulate-is-the-original-sin` | Deep-space orbital epicycle diagram |
| `the-reality-distortion-field-inverts-the-baseline` | Batik / wax-resist dye on cotton |
| `the-reality-distortion-field-names-the-closed-map` | Drypoint cartographic plate |
| `the-reversal-from-defensible-claim-to-dogma` | Laboratory glassware still / sealed continuous curve |
| `the-reversal-of-causality-in-wealth-transfer-policies-and-price-floors` | Photoreal balance-scale allegory |
| `the-risk-is-the-belief-in-oversight-itself` | Security-print guilloche engraving |
| `the-ramble-within-the-ramble` | Anaglyph red-cyan stereo graphic |
| `the-real-scarcity-is-not-memory-but-continuous-re-tracing` | Charcoal wipe / continuous redraw on newsprint |
| `the-scaffolding-that-keeps-growing` | Lithographic crayon / stone print |
| `the-scaffolding-we-forget` | Ink wash / sumi-e |
| `the-scaffolding-we-forget-local-models-as-default` | Constructivist poster |
| `the-source-of-all-harm` | Assay touchstone / gold-streak still |
| `the-source-of-shared-change` | Monotype ghost-print still life |
| `the-strongest-belief-of-the-mind` | Palimpsest vellum / multi-ink redraw |
| `the-utility-men-of-progress` | Workshop pegboard still |
| `technology-is-residual-of-human-compounding` | Dual-epoch residual continuum still |
| `the-average-is-residue-not-the-engine` | Industrial gear dissolving into residual waves |
| `residual-control-recedes-to-the-edge` | Graphite ridge / luminous edge abstract |
| `residual-individualism` | Mixed-media profile / geometric residue field |
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
| `on-closed-systems-open-minds-and-the-limits-of-proof` | Cinematic sealed-chamber / luminous-mind dual |
| `only-if-it-is-not-kept-empty` | Celadon kiln shelf still life |
| `the-real-lesson-from-the-consciousness-vector-paper` | Medieval volvelle / paper dial still |

## Crowded — prefer not to extend

- **Dark chalk / light trails** (largest set)
- **Stills / still-life / craft-table** family cluster (any “still life,” “craft table,” “museum prop,” cream-linen desk — recent default lag)
- Photoreal tableau and surreal desert allegory (already several landscape stills)

## Unused candidates (pick from here or invent)

Not exhaustive. Prefer inventing something not in Style families above. If empty or stuck: **random reuse** of a non-crowded used family (see Principle).

Examples of non-still directions (illustrative only — invent, do not recycle as a new default list): full-bleed pattern, type poster without legible text, aerial/map, underwater, macro mineral, neon signage blur, stained atmospheric photograph, comic panel (no text), kinetic motion blur, collage tear, satellite false-color, botanical illustration plate, etc.

## Workflow for a new cover

1. Open this file; list families already used.
2. **Reject still-default:** if the first idea is a tabletop/museum still, discard it and pick a different medium.
3. Choose a **new** family (invent or Unused candidates). If no honest new style remains, **randomly** pick a used family that is **not** Dark chalk and **not** a still/craft-table look and **not** the last 2–3 covers’ families.
4. Prompt for that medium **explicitly** (name the tradition/medium in the prompt). Ban lazy defaults: cream-linen still, dark chalk abstract, “cinematic fog cube,” generic still life with prop.
5. Generate at **20:9** when available (`aspect_ratio: "20:9"`); **16:9 as-is** is fine — no forced crop. Install as `assets/covers/<slug>.jpg`.
6. Append the slug to Inventory and the family row (or add a new Style families row). On random reuse, append the slug to that family’s Covers cell.
7. Operator drop supersedes agent-gen when provided (install + update STYLES only).

Same asset is reused for Substack paste cover and X Article `cover_media` — do not maintain a second aspect-ratio set.
