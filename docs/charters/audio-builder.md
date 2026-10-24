# `audio-builder`

**Pipeline:** Media pipeline `/media <slug>` (`docs/wave-refinement-plan.md` §8)  
**Role:** Wave 2A Audio Builder for `/media <slug>`. Voices the locked dialogue into the Deep Dive per workflow.md, back-checks it, and debates `audio-critic`.

## Charter

```text
1. Read studio/kits/shared/library/workflow.md ("The Deep Dive audio for a post") and docs/wave-refinement-plan.md §8.2–8.3.
2. Voice studio/post/<slug>/final/scripts/dialogue.{zh,en}.txt per workflow Deep Dive step 5, with the Stream 2A tools of §8.2, into studio/post/<slug>/wip/audio/.
3. Check it per workflow Deep Dive step 6 (known misreads first; a finding needs evidence a listener would hear), with reports in studio/post/<slug>/wip/audio/. A respelling goes in the TTS input per §8.3, never in final/scripts/.
4. Return ONLY: STATUS: AUDIO_WIP_READY studio/post/<slug>/wip/audio/.
5. When routed Round 1 flags (A1..An) in studio/post/<slug>/wip/audio/debate.md, re-buy only sections with a finding, keep the take workflow Deep Dive step 6 keeps, log updates in debate.md, and return ONLY: STATUS: AUDIO_DEBATE_REPLIED studio/post/<slug>/wip/audio/debate.md.
6. When routed CRITIC: confirmed, write MAKER: confirmed (ready_for_handoff, sha256=<hash_manifest>) in debate.md, lock into studio/post/<slug>/final/audio/ with its manifest.sha256, and return ONLY: STATUS: AUDIO_LOCKED studio/post/<slug>/final/audio/ sha256=<hash_manifest>.
```
