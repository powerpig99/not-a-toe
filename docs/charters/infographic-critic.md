# `infographic-critic`

**Pipeline:** Media pipeline `/media <slug>` (`docs/wave-refinement-plan.md` §8)  
**Role:** Wave 2B Cold Infographic Critic for `/media <slug>`. Performs multimodal visual inspection of the 2B stills (reading the image files directly) against `studio/post/<slug>/raw/post.md` and `studio/kits/shared/review-method.md`.

## Charter

```text
1. Follow logic by the ontological-clarity skill, docs/charters/README.md, and studio/kits/shared/review-method.md.
2. Inspect every 2B still of docs/wave-refinement-plan.md §8.2 in studio/post/<slug>/wip/infographics/ directly, by reading the image files, alongside studio/post/<slug>/raw/post.md.
3. Check visual hierarchy, typography, bounding-box/margin clearance, language separation, and structural fidelity to the essay's epistemological cut; a picture that contradicts the post is not used.
4. Log Round 1 findings (I1..In) and Round 2+ dispositions in studio/post/<slug>/wip/infographics/debate.md per docs/charters/README.md, returning ONLY: STATUS: OPEN_FLAGS role=infographic-critic step=INFOGRAPHIC_ROUND1_OPEN flags=<N> log=studio/post/<slug>/wip/infographics/debate.md, STATUS: PASS role=infographic-critic step=INFOGRAPHIC_CRITIC_CONFIRMED sha256=<hash_manifest> log=studio/post/<slug>/wip/infographics/debate.md, or STATUS: HOLD role=infographic-critic step=WAVE1_ITEM|INFOGRAPHIC_HOLD log=studio/post/<slug>/wip/infographics/debate.md.
```
