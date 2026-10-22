# Opus 5.5 Cinematic Technical Video Recipe

**How to build Flint-style cinematic motion-graphics short films using Claude Opus 5.5 + code-to-video rendering (late 2026)**

This recipe produces dark framed UI panels, glowing technical diagrams, precise code windows, schematic illustrations, and clean kinetic typography — the exact aesthetic of the Recursive “FLINT” short film.

---

## Core Pipeline

1. **Claude Opus 5.5** (via Claude Code) writes the animation as deterministic code.
2. **HyperFrames** (HeyGen’s open-source HTML-native renderer) or a pure Playwright + ffmpeg setup captures every frame.
3. You add voiceover, music, and final polish.

**Why this works so well for Flint-style videos**: Everything is a pure function of time. Technical accuracy, perfect text rendering, and precise diagram animations are far more reliable than generative video models.

---

## Prerequisites

- Claude Code access with Opus 5.5 (`claude-opus-5-5`)
- Node.js 22+
- FFmpeg
- (Recommended) HyperFrames skills

```bash
# Install HyperFrames skills for Claude Code
npx skills add heygen-com/hyperframes
```

---

## Step-by-Step Recipe

### Phase 1: Project Setup & Brief (30–60 min)

1. Create a project folder.
2. Drop in any reference frames, brand assets, or screenshots of the desired style (dark UI panels, cyan/gold accents, technical diagrams).
3. Write a tight brief covering:
   - Total duration (start with 60–90 seconds for a full film)
   - Chapter structure (e.g., Eureka Machine → Architecture Search → Quantization → Megakernel → Local Performance → Future)
   - Exact technical facts you want shown
   - Visual style rules (palette, banned effects, framing style)
   - Target resolution (1920×1080)

### Phase 2: Blueprint with Opus 5.5

Start in Claude Code and ask for a **beat sheet + keyframes first** before full code. This is critical.

**Strong opening prompt pattern**:

```
Using HyperFrames, create a cinematic technical short film about [topic].

Duration: 75 seconds, 1920x1080, 30fps.

Style: Dark cinematic UI panels with thin gold/cyan frames, glowing diagrams, schematic laptop/chip illustrations, precise code windows. High contrast, minimal particles, no generic gradients or floating orbs.

Chapters:
1. 0-12s: Title + "How it was built" framing
2. 12-28s: Eureka Machine searching architectures
3. 28-45s: Quantization discovery (4-bit lm_head)
4. 45-60s: Megakernel + local speed
5. 60-75s: Closing goal statement

Rules:
- Every frame is a pure function of time t
- No requestAnimationFrame, timers, or unseeded random
- Expose seek(t) and DURATION
- Start by outputting only a beat sheet and 6 keyframe descriptions
- Then wait for my approval before writing full code
```

Iterate on the blueprint until the narrative and visual rhythm feel right.

### Phase 3: Generate the Scene Code

Once the blueprint is locked, have Opus write the full HyperFrames composition (or a single seekable HTML file).

Key constraints to include:
- Deterministic (no `Date.now()`, no CSS transitions that fight the seek function)
- Clear chapter transitions
- Technical diagrams that actually match the real concepts (MoE routing, expert counts, 4-bit, etc.)
- On-screen text that is large and readable

### Phase 4: Preview & Critique Loop

This is where most of the quality comes from.

1. Preview:
   ```bash
   npx hyperframes preview
   ```
2. Generate contact sheets (stills at regular intervals).
3. Ask Opus to critique harshly:
   ```
   Act as a senior motion designer. Score this on hook, readability, technical accuracy, pacing, and visual cohesion (1-10).
   List the 3 worst problems with timestamps.
   Then fix only those issues.
   ```
4. Repeat 2–4 times. Good films usually need 3–6 critique rounds.

### Phase 5: Render

```bash
npx hyperframes render --quality delivery --output flint-style.mp4
```

Or with the pure Playwright method if you prefer full control.

### Phase 6: Audio & Final Polish

- Voiceover: ElevenLabs, Fish Audio, or local TTS (Kokoro works well with HyperFrames).
- Music: Ambient electronic (Suno or royalty-free).
- Sound design: Subtle UI clicks, data whooshes, low drones.
- Final pass in DaVinci Resolve or Premiere only if needed (usually not required).

---

## Pro Tips for Flint-Level Quality

- **Reference frames beat adjectives**. Screenshot moments from the original Flint film or similar tech videos and say “match this framing and glow treatment.”
- **Ban the defaults**. Explicitly ban centered titles on gradients, random particles, excessive glows, and linear motion.
- **Beat grid**. Sync major changes to a 90–120 BPM grid so the film has rhythm.
- **One idea per scene**. Technical videos fall apart when they try to show too much at once.
- **Start short**. Perfect a 20–30 second chapter first, then expand.
- **Cost reality**: A 60–90s high-quality piece often takes $5–40 in Opus 5.5 tokens depending on how many critique loops you run.

---

## Alternative Paths

| Approach | Best For | Difficulty |
|---------|----------|------------|
| **Claude Code + HyperFrames** | Fastest polished results | Low |
| **Single HTML + Playwright** | Maximum control | Medium |
| **Remotion** | If you already work in React | Medium |
| **Manim** | Pure mathematical/diagram-heavy | Medium-High |

This pipeline is currently one of the strongest ways to produce accurate, cinematic technical explainers. The Flint film’s visual language maps extremely well onto it.

---

## Key References (late 2026)

### Core Guides
- [How to Make Videos with Claude Opus 5.5: A Deterministic Render Pipeline](https://huggingface.co/blog/karmen-beatapi/how-to-make-videos-with-claude-opus-5-5) — Best single-source technical walkthrough (Playwright + ffmpeg, prompt template, `seek(t)` contract).
- [Make a video with Claude Code: HyperFrames and Remotion step by step](https://claudevideo.org/guides/hyperframes-remotion-claude-code) — Official-style HyperFrames quickstart.
- [Opus 5.5 Video Examples & How to Make Them](https://claudeimagine.com/opus-5-5-video) — 30 remakes + skill installation.
- [GitHub: bilaldemirerr/opus-video-recipes](https://github.com/bilaldemirerr/opus-video-recipes) — Real MP4s, exact prompts, measured token costs (HyperFrames + Remotion).

### Prompting & Workflow
- [GitHub: Li-Evan/awesome-opus-5.5-video-prompts](https://github.com/Li-Evan/awesome-opus-5.5-video-prompts) — 334 verified prompts + director’s toolkit.
- [Opus 5.5 Video Guide: How the One-Prompt Motion Graphics Are Made](https://ciyo.ai/blog/opus-5-5-video-motion-graphics-guide) — Contact-sheet critique loop and house rules.
- [Claude Opus 5.5 + Remotion Video Workflow](https://bettertoken.ai/en/blog/claude-opus-5-5-remotion-video-workflow/)
- [HyperFrames vs Remotion vs Manim](https://bilallabs.vercel.app/ai/opus-video/hyperframes-vs-remotion-vs-manim)

### Field Notes
- [Where Is Opus 5.5 Strong in Making Video? Notes from a Small Studio](https://huggingface.co/blog/BreadStudio/opus-5-5-video-field-notes) — Blueprint vs. coding division of labor.

---

## Minimal Deterministic Render Contract (from BeatAPI guide)

The HTML scene must:
- Set `window.DURATION`
- Expose `async window.seek(t)`
- Be a pure function of `t` (no `Date.now`, `requestAnimationFrame`, timers, CSS transitions, or unseeded `Math.random`)

Example render script structure (Node + Playwright):

```javascript
// Simplified from the official guide
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
await page.goto(pathToFileURL(scene).href);
await page.waitForFunction(() => typeof window.seek === "function");
// Loop: page.evaluate(t => window.seek(t), i / fps) + screenshot → ffmpeg
```

---

*Last updated: October 22, 2026*
