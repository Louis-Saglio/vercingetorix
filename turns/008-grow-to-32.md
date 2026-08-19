# Turn 008 — Make the 32-soldier target reachable

Goal served: G2 (sustain a 32+ citizen-soldier army) — **achieved** this turn.

## Hypothesis

> If I make the 32-soldier target reachable — raise `SOLDIER_TARGET` from 20 to
> 32 and expand the house-offset candidates so the bot can actually build its
> 4 houses — then the fraction of seeds reaching ≥32 melee soldiers by
> game-minute 12 rises from 0 to most seeds, because the bot is no longer
> capped near 27 soldiers by a 3-house population limit.

Primary metric: fraction of seeds whose per-minute `[HARNESS]` `melee` sample
reaches ≥32 by game-minute 12.

Verdict thresholds (pre-registered): good if treatment ≥ 8/10 seeds with 0 JS
errors and canary PASS; bad if treatment ≤ 2/10 seeds, or error/determinism
veto; neutral otherwise.

## Implementation

One change ("make the 32-soldier target reachable"), two constants in
`bot/simulation/ai/vercingetorix/vercingetorix.js`:

- `const SOLDIER_TARGET = 20;` → `const SOLDIER_TARGET = 32;`
  (`ATTACK_THRESHOLD` follows it, so the attack also waits for 32.)
- `HOUSE_OFFSETS` grows from 4 to 8 candidate placements (cardinal + diagonal
  at ~16 tiles) so the bot can actually place its 4 houses. With only 4
  cardinal candidates, turn 006 stalled at 3 houses / population 35, which
  caps the army at ~27 soldiers.

## Experiment

Settings: seeds 71–80 (fresh), sandbox Rome (`--difficulty2 0`),
`random/mainland` 128, `conquest_civic_centers`, treasures disabled, 20
game-minute limit, biome/placement pinned. Baseline = HEAD (turn-004 code);
treatment = the grow-to-32 change; canary = seed 71.

Results:

- Canary: **PASS**.
- Primary metric: treatment reached ≥32 melee by minute 12 on **8/10** seeds
  (baseline 0/10); reached ≥28 by minute 12 on **9/10**.
- 0 JS errors in all 20 matches.
- Composite (reported, not the primary metric): +2.23 → neutral — expected,
  because this turn grows the army but does not change how it fights, so win
  rate is still 0/10 in both arms.

## Verdict

**Good** (pre-registered single metric): 8/10 ≥ 32-by-12 with 0 JS errors and
canary PASS meets the ≥8/10 good bar. The change is kept.

## Action

Keep the change. Commit as `turn 008: grow-to-32 — good` and push.

This batch also **achieves G2** (sustain a 32+ soldier army): 8/10 Good, 0 JS
errors, against sandbox Rome. `docs/GOALS.md` is updated in the same commit to
record the closing batch and promote G3 (defeat sandbox Rome) to the current
goal. `docs/CHANGELOG.md` gets an entry.

## Next

Goal G3: defeat sandbox Rome (win ≥8/10 seeds). The bot now fields 32 soldiers;
the next lever is to aim that army at the objective — likely a direct
capture-allowed attack on the enemy CC once the army is large, rather than the
old nearest-enemy sweep.
