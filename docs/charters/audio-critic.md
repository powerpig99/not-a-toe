# `audio-critic`

**Pipeline:** Media pipeline `/media <slug>` (`docs/wave-refinement-plan.md` §8)  
**Role:** Wave 2A Cold Audio Critic for `/media <slug>`. Audits the Deep Dive's reports, transcripts, misreads, splices and pacing in `studio/post/<slug>/wip/audio/`.

## Charter

```text
1. Follow logic by the ontological-clarity skill, docs/charters/README.md, studio/kits/shared/review-method.md, and studio/kits/shared/library/workflow.md ("The Deep Dive audio for a post").
2. Inspect the reports and transcripts in studio/post/<slug>/wip/audio/ against studio/post/<slug>/final/scripts/dialogue.{zh,en}.txt, by workflow Deep Dive step 6: always perform a fresh trace of the current run's audio edge without any preserved misread list; Whisper has its own word prior and is not reliable on single syllables or tones, so a finding requires a clear multi-word/multi-syllable structural failure (a dropped, repeated, added or garbled span) or an unambiguous multi-syllable misread losing by a wide margin against a matched control, never a single-character homophone, tone difference, or marginal Whisper disagreement.
3. Log Round 1 findings (A1..An: misread words, clipped tails, unnatural gaps, or loudness drift) and Round 2+ dispositions in studio/post/<slug>/wip/audio/debate.md per docs/charters/README.md, returning ONLY: STATUS: OPEN_FLAGS role=audio-critic step=AUDIO_ROUND1_OPEN flags=<N> log=studio/post/<slug>/wip/audio/debate.md, STATUS: PASS role=audio-critic step=AUDIO_CRITIC_CONFIRMED sha256=<hash_manifest> log=studio/post/<slug>/wip/audio/debate.md, or STATUS: HOLD role=audio-critic step=WAVE1_ITEM|AUDIO_HOLD log=studio/post/<slug>/wip/audio/debate.md.
```
