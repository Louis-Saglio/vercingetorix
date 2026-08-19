# Turn 005 — Target the enemy civic centre

Goal served: G2 (defeat sandbox Rome).

## Hypothesis

> If I make the bot's sweep issue a direct `attack` on the enemy civic centre
> (instead of `attackMove` toward the nearest enemy entity), then the bot wins
> more seeds against sandbox Rome, because the army concentrates its
> capture/damage on the objective required by `conquest_civic_centers` instead
> of getting distracted by enemy units and structures.

Primary metric: protocol-default composite score (verdict good ≥ +4, bad ≤ −4,
neutral otherwise), with the error veto and the determinism canary. G2 win rate
is reported alongside it (win = enemy CC captured/destroyed before the limit).

## Implementation

Two edits in `bot/simulation/ai/vercingetorix/vercingetorix.js` (one change:
target the enemy CC):

- Added `enemyCivCentre(gameState)`: returns the first enemy-owned entity with
  class `CivCentre` (excludes gaia and self).
- The sweep now issues `soldier.attack(cc.id())` — a direct capture-allowed
  attack on the enemy CC — instead of `attackMove` at the nearest enemy
  entity. If no enemy CC exists (should only happen after victory), it falls
  back to the old nearest-enemy `attackMove`.

Why this should win: the spearman's melee hack (4.5) is reduced by the CC's
~30 hack armor to ~0.19 damage/hit, but its Capture attack (2.5/s, capture
allowed) accumulates against the CC's 2500 capture points minus 30/s regen —
the only realistic way spearmen take a CC. A direct `attack` orders that
capture; `attackMove` at whatever unit was nearest spread the army away from
the objective.

## Experiment

Settings: seeds 31–40 (fresh), sandbox Rome (`--difficulty2 0`, per G2),
`random/mainland` 128, `conquest_civic_centers`, treasures disabled, 20
game-minute limit, biome/placement pinned. Baseline = HEAD (turn-004 code);
treatment = the CC-targeting change; canary = seed 31 repeated with the
baseline code.

Results:

- Canary: **PASS**.
- Composite score: total **−4.21** (≤ −4), error veto false → **bad**.
- Win rate: baseline 0/10, treatment 0/10 (every match a time-limit draw; the
  enemy CC was never captured or destroyed).
- Why it lost the composite: the treatment army stopped killing enemy units
  (`enemyUnitsKilledValue` fell from ~1000–2500 to ~0–300) because a capture
  attack kills nothing, while still failing to take the CC. The direct attack
  also removed the per-soldier full-map scan (a performance win, but not
  enough to matter).

Diagnosis (game data): the CC has ~30 hack armor vs the spearman's 4.5 hack,
so melee is ~0.19 damage/hit; capture needs 2500 points against 30/s regen.
~20 spearmen give a net ~20 capture/s (≈125 s), but the CC's garrison arrows
kill them faster than they can hold the capture — the army collapses to ~10
or fewer before the CC falls.

## Verdict

**Bad.** Composite −4.21 ≤ −4, no wins, and the treatment discarded the
incidental enemy kills the baseline sweep produced. No error/determinism veto,
but the primary metric is clearly negative.

## Action

Revert the change (`git restore bot/simulation/ai/vercingetorix/vercingetorix.js`)
and commit the turn as `turn 005: target-enemy-civic-centre — bad`. No
`CHANGELOG.md` entry (reverted change leaves no trace in code, only the
journal).

## Next

G2 remains open. Negative knowledge: a lone spearman rush on the CC cannot
capture it before the garrison kills the army. Candidates for turn 006:
raise `SOLDIER_TARGET` (and the house cap it implies) for a much larger
capture force, or advance to Town Phase and build siege (rams) for crush
damage against the CC. The old nearest-enemy sweep stays as the baseline.
