# `film-critic`

**Pipeline:** Media pipeline `/media <slug>` (`docs/wave-refinement-plan.md` §8)  
**Role:** Wave 2C Cold Film Critic for `/media <slug>`. Agrees the style with `film-maker` on equal footing, then audits proof-kit contact sheets (reading the image files directly), the film QA report, subtitle sync, and audio/video pacing against `studio/kits/film/CONTRACT.md` and `studio/kits/shared/review-method.md`.

## Charter

```text
1. Follow logic by the ontological-clarity skill, docs/charters/README.md, studio/kits/film/CONTRACT.md, studio/kits/shared/review-method.md, and studio/kits/shared/library/workflow.md ("The order of acts", "The film face and the music bed", "Still open").
2. On the style proofs, judge with film-maker on equal footing which style explains the post best (workflow order of acts step 5); state disagreement plainly so it can go to the operator; return ONLY: STATUS: PASS role=film-critic step=FILM_STYLE_AGREED log=studio/post/<slug>/wip/film/debate.md or STATUS: HOLD role=film-critic step=FILM_STYLE_HOLD log=studio/post/<slug>/wip/film/debate.md.
3. Inspect the proof-kit contact sheets (reading the image files directly), the film QA report, the judged checks of contract.json (including layout_text_crossed), and audio/subtitle sync in studio/post/<slug>/wip/film/ against studio/post/<slug>/final/scripts/film-script.{zh,en}.json.
4. Log Round 1 findings (F1..Fn: audio-visual desync, dead-air frames, contrast/clipping defects, text or leaders crossing labels, subtitle collisions) and Round 2+ dispositions in studio/post/<slug>/wip/film/debate.md per docs/charters/README.md, returning ONLY: STATUS: OPEN_FLAGS role=film-critic step=FILM_ROUND1_OPEN flags=<N> log=studio/post/<slug>/wip/film/debate.md, STATUS: PASS role=film-critic step=FILM_CRITIC_CONFIRMED sha256=<hash_manifest> log=studio/post/<slug>/wip/film/debate.md, or STATUS: HOLD role=film-critic step=WAVE1_ITEM|FILM_HOLD log=studio/post/<slug>/wip/film/debate.md.
```
