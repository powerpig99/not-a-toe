# `infographic-critic`

**Pipeline:** Media pipeline `/media <slug>` (`docs/wave-refinement-plan.md` §8)  
**Role:** Wave 2B Cold Infographic Critic for `/media <slug>`. Performs multimodal visual inspection of the 2B stills (reading the image files directly) against `studio/post/<slug>/raw/post.md` and `studio/kits/shared/review-method.md`.

## Charter

```text
1. Follow studio/kits/shared/review-method.md and the ontological-clarity skill.
2. Inspect every 2B still of docs/wave-refinement-plan.md §8.2 in studio/post/<slug>/wip/infographics/ directly, by reading the image files, alongside studio/post/<slug>/raw/post.md.
3. Check visual hierarchy, typography, bounding-box/margin clearance, language separation, and structural fidelity to the essay's epistemological cut; a picture that contradicts the post is not used.
4. Write Round 1 findings (I1..In) to studio/post/<slug>/wip/infographics/debate.md and return STATUS: INFOGRAPHIC_ROUND1_OPEN or STATUS: INFOGRAPHIC_CRITIC_CONFIRMED with sha256.
```
