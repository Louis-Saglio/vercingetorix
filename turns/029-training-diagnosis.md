# Turn 029 — Diagnose the training-rate collapse

Goal served: G4a (army scaling) — evidence-collection turn.

## Hypothesis

> If I restore the turn-028 iteration-5 code (free post-town training, 8
> houses, rams gated on the full army) with a per-minute log of the CC's
> training-queue length, and run it on a known-good seed (211) and a
> known-bad seed (264), then the queue log will separate the two competing
> explanations for the ~1.5 soldiers/min ceiling: (a) the seed batch
> 261–270 is wood-poor (the validated turn-023 code also peaks at 16 there),
> or (b) the train posts stop working after ~minute 14 for a code reason.
> The evidence tells turn 030 exactly what to fix.

Primary metric: the diagnosis (qualitative — this is an evidence-collection
turn; the deliverable is the understanding, written below).

## Implementation

In `bot/simulation/ai/vercingetorix/vercingetorix.js` (and the 30-minute
trigger):

- Restores the turn-028 iteration-5 design (reverted as its bad verdict
  requires).
- The `[HARNESS]` sample adds `q` — the CC training queue length — and
  `trainable` — whether `cc.trainableEntities(civ)` still lists the spearman.

## Experiment

Settings: seeds 211 and 264, sandbox Rome (`--difficulty2 0`),
`random/mainland` 128, `conquest_civic_centers`, treasures disabled, 30
game-minute limit, biome/placement pinned. No baseline/treatment pairing —
this is a diagnostic, not a verdict experiment (recorded here for
transparency; the turn's deliverable is the understanding).

## Results

## Verdict

## Action

## Next
