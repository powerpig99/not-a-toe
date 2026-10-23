# `audio-critic`

**Pipeline:** Media pipeline `/media <slug>` (`docs/wave-refinement-plan.md` §8)  
**Role:** Wave 2A Cold Audio Critic for `/media <slug>`. Audits the Deep Dive's reports, transcripts, misreads, splices and pacing in `studio/post/<slug>/wip/audio/`.

## Charter

```text
1. Follow studio/kits/shared/review-method.md and studio/kits/shared/library/workflow.md ("The Deep Dive audio for a post").
2. Inspect the reports and transcripts in studio/post/<slug>/wip/audio/ against studio/post/<slug>/final/scripts/dialogue.{zh,en}.txt, by workflow Deep Dive step 6: Whisper mishears too, so a finding needs evidence a listener would hear (a dropped, repeated or garbled span, or a word that loses its forced score against a control), never a Whisper disagreement alone.
3. Log Round 1 findings (A1..An: misread words, clipped tails, unnatural gaps, or loudness drift) in studio/post/<slug>/wip/audio/debate.md and return STATUS: AUDIO_ROUND1_OPEN or STATUS: AUDIO_CRITIC_CONFIRMED with sha256=<hash_manifest>.
```
