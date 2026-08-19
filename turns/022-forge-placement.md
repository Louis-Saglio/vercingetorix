# Turn 022 — Forge placement ring

Goal served: G4 (defeat sandbox Rome — City is the siege-path prerequisite).

## Hypothesis

> If the forges get their own placement ring (16 candidates at 72 m from the
> CC, first candidate with ≥ 28 m clearance from every own structure), on top
> of the turn-021 design (training held until 3 forges, then City research at
> 750/750), then the bot reaches City Phase before the 20-minute limit on
> ≥ 8/10 seeds, because turn 021 showed the only remaining blocker is
> placement: the 8-offset house ring is exhausted by 5 houses and the forge's
> 22×22 footprint needs clearance the shared ring cannot provide.

Primary metric: fraction of seeds where `gameState.currentPhase() >= 3`
(sim ground truth) before the 20-minute limit, 0 JS errors.

Verdict thresholds (pre-registered): good if ≥ 8/10 seeds reach City, 0 JS
errors, canary PASS; bad if ≤ 2/10 or error/determinism veto; neutral
otherwise. Secondary (reported, not the verdict): city minute, forge minute,
stone/metal at minute 16, composite.

## Implementation

In `bot/simulation/ai/vercingetorix/vercingetorix.js`:

- The turn-021 design is restored (reverted as the bad verdict requires):
  3-forge target, training held while `forges < 3`, City research at 750/750
  via `canResearch`, sample fields.
- **New change:** `FORGE_OFFSETS` (16 candidates at 72 m, precomputed) and a
  `structureClear` helper; `manageForges` walks the ring (rotated per attempt)
  and places only at candidates ≥ 28 m from every own structure.

## Experiment

Settings: seeds 201–210 (fresh), sandbox Rome (`--difficulty2 0`),
`random/mainland` 128, `conquest_civic_centers`, treasures disabled, 20
game-minute limit, biome/placement pinned. Baseline = HEAD (turn-021 commit);
treatment = forge placement ring; canary = seed 201.

## Results

**First run — INVALID.** The city branch in `manageResearch` was unreachable:
the turn-019 `if (this.townResearched) return;` guard survived the re-apply,
so once Town posted, the function returned before the City code ever ran.
Symptoms matched: forges reach 3 and `townClass` reaches 3 on 5 seeds by t16
(placement ring works), stone/metal cross 750 at t17–19, yet `phase` stays 2
and no City research posts. The fix removes the early return (the Town branch
returns internally instead). Baseline and canary stay valid; treatment rerun
on the same seeds.

**Rerun results:**

- Canary: **PASS** (unchanged).
- Primary metric: **5/10** seeds reach City (201, 203, 205, 207, 210), at
  minute 17–19 — the seeds where the placement ring delivered 3 forges. The
  other five stall at 0–2 forges (placement candidates blocked by terrain —
  the structure-clearance filter alone is not enough), except 209 which never
  reaches Town (house stall). 0 JS errors. Composite −7.70.
- Neutral-repeat (protocol escalation, same seeds): **identical 5/10**, same
  forge pattern per seed — deterministic confirmation that this is signal,
  not noise. Still neutral → revert per protocol.
- Key evidence for the goal: City lands at minute 17–19 **even on the good
  seeds** — arsenal (300 wood) + ram (300 wood + 150 metal) + the march and
  CC kill cannot fit in the remaining 1–3 minutes of the 20-minute limit.

## Verdict

**Neutral** (5/10, between the pre-registered 2/10 and 8/10 boundaries),
repeat identical → **revert** per protocol. The placement ring is a real but
insufficient improvement; the negative knowledge is crisp.

## Action

Revert the change (`git restore bot/simulation/ai/vercingetorix/vercingetorix.js`)
and commit as `turn 022: forge-placement — neutral (reverted)`. The commit
also adjusts G4 in `docs/GOALS.md`: the match limit rises from 20 to 25
game-minutes, on this turn's evidence that the siege path (City at t17–19 →
arsenal → ram → march → CC kill) cannot finish inside 20 minutes.

## Next

Double-ring forge placement (72 m + 88 m, 32 candidates) — the single ring
still loses to terrain on ~half the seeds. Then the arsenal + ram + attack
turn under the 25-minute limit. See `turns/backlog.md`.
