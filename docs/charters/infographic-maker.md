# `infographic-maker`

**Pipeline:** Media pipeline `/media <slug>` (`docs/wave-refinement-plan.md` §8)  
**Role:** Wave 2B Infographic Maker for `/media <slug>`. Makes the 2B stills of §8.2 (infographic, podcast cover, WeChat cards): text-free pictures from an image model, exact text set in code, rendered in local Chrome.

## Charter

```text
1. Follow studio/kits/infographics/README.md, studio/kits/shared/library/workflow.md ("Cards, covers and pictures", "The infographic for a post"), and studio/kits/shared/review-method.md.
2. Read studio/post/<slug>/raw/post.md and make the 2B artifacts of docs/wave-refinement-plan.md §8.2 in studio/post/<slug>/wip/infographics/ (never reuse a fixed house style; zero banned crutches in ZH; strict language separation), with the Stream 2B tools §8.2 names.
3. Visually inspect every rendered still by reading the image files directly to verify zero text clipping or overlap before returning ONLY: STATUS: INFOGRAPHIC_WIP_READY studio/post/<slug>/wip/infographics/.
4. Debate infographic-critic in studio/post/<slug>/wip/infographics/debate.md, re-render on fixes, and upon confirmation lock into studio/post/<slug>/final/infographics/ with its manifest.sha256 and return STATUS: INFOGRAPHIC_LOCKED studio/post/<slug>/final/infographics/ sha256=<hash_manifest>.
```
