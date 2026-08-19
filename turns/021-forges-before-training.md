# Turn 021 — Forges before training

Goal served: G4 (defeat sandbox Rome — City is the siege-path prerequisite).

## Hypothesis

> If soldier training is held until the three forges are built (like the
> pre-Town gate holds training), then the bot reaches City Phase before the
> 20-minute limit on ≥ 8/10 seeds, because turn 020 showed the wood race is
> the blocker: continuous 50-wood training kept wood at 25–300 from minute 8,
> so the forges never got their 200 wood each. With training held, wood pools
> for the forges, then the army grows, then City research fires at 750/750.

Primary metric: fraction of seeds where `gameState.currentPhase() >= 3`
(sim ground truth) before the 20-minute limit, 0 JS errors.

Verdict thresholds (pre-registered): good if ≥ 8/10 seeds reach City, 0 JS
errors, canary PASS; bad if ≤ 2/10 or error/determinism veto; neutral
otherwise. Secondary (reported, not the verdict): city minute, forge minute,
stone/metal at minute 16, composite.

## Implementation

In `bot/simulation/ai/vercingetorix/vercingetorix.js`:

- The turn-020 change is restored (it was reverted as the bad verdict
  requires): `manageForges` (3 forges, foundation/repair with real builders),
  the City branch in `manageResearch` (750/750 + `canResearch`), serialized
  `forgeAttempts`/`cityAttempted`, `forges`/`townClass` in the sample.
- **New change:** `manageSoldiers` holds training while
  `forges < FORGE_TARGET` — wood pools for the forges before soldiers consume
  it.

## Experiment

Settings: seeds 191–200 (fresh), sandbox Rome (`--difficulty2 0`),
`random/mainland` 128, `conquest_civic_centers`, treasures disabled, 20
game-minute limit, biome/placement pinned. Baseline = HEAD (turn-020 commit);
treatment = forges-before-training; canary = seed 191.

## Results

- Canary: **PASS**.
- Primary metric: **0/10** reach City. Composite −9.61. 0 JS errors.
- The training gate works (wood pools to 655–925 by t16, no collapse), but a
  new blocker appears: **forge placement fails**. On seed 191 no forge is ever
  placed despite wood ≥ 200 from minute 9 (`forges=0, found=0` through minute
  18); seed 195 places exactly one. The 8 house offsets are exhausted by the 5
  houses, and the forge's 22×22 footprint needs more clearance than a house —
  the remaining candidate positions are blocked, so `construct` is silently
  rejected by the sim every tick. Training stays held forever (melee stuck at
  2), stone/metal stall at ~850/750.
- Seeds 193 and 199 re-hit the 5-house placement stall (phase stays 1) — the
  same offset-exhaustion problem for houses.

## Verdict

**Bad** (pre-registered: 0/10 ≤ 2/10). The training gate is not the blocker —
placement is: the shared 8-offset ring has no room left for three 22×22
forges. Reverted.

## Action

Revert the change (`git restore bot/simulation/ai/vercingetorix/vercingetorix.js`)
and commit as `turn 021: forges-before-training — bad`. No `CHANGELOG.md` entry.

## Next

Dedicated forge placement: a wider candidate ring (~16 positions at 72 m) with
clearance filtering (≥ ~26 m from every own structure), cycled per attempt.
The same machinery later serves the house-placement stall (2/10 seeds). See
`turns/backlog.md`.
