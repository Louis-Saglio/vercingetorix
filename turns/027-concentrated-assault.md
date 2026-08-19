# Turn 027 — Concentrated assault

Goal served: G4 (defeat sandbox Rome).

## Hypothesis

> If the attack waits for **two rams** (a third joins as it finishes) and the
> whole army attack-moves at the enemy civic centre itself instead of the
> nearest enemy unit, then the bot wins on ≥ 8/10 seeds before the 30-minute
> limit, because turn 026's final iteration showed the economy chain works
> (City 8/10, arsenal, rams, full mobilization) and the assault alone fails:
> one ram at a time dies to the concentrated garrison fire (8 pierce arrows
> per garrisoned soldier, 20 garrison slots) before landing its 150-crush
> hits, and the soldiers die fighting Rome's units away from the objective.
> Two rams split the arrows and land ~200 crush dps on the 3000-hp,
> crush-armor-0 CC — a ~15-second kill once in contact — while the army
> concentrates on the CC with them.

Primary metric: fraction of seeds won (enemy CC destroyed before the limit),
0 JS errors.

Verdict thresholds (pre-registered): good if ≥ 8/10 wins, 0 JS errors, canary
PASS; bad if ≤ 2/10 or error/determinism veto; neutral otherwise. Secondary
(reported, not the verdict): win minute, ram minute, composite. In-turn
fix-and-rerun iterations allowed.

## Implementation

In `bot/maps/scripts/NonVisualTrigger.js` (30-minute limit) and
`bot/simulation/ai/vercingetorix/vercingetorix.js`:

- Restores the turn-026 siege economy (documented by its five iterations):
  all-wood post-town gather split, free training after the 3 forges with a
  pause after the arsenal until two rams exist, arsenal on the double ring,
  foundation-safe ram training.
- `RAM_TARGET` = 3; the attack triggers at `rams ≥ 2`.
- The soldier sweep now attack-moves at the **enemy civic centre** (the
  objective), not the nearest enemy unit; the rams attack the CC directly.
- Sample fields unchanged (arsenal/rams).

## Experiment

Settings: seeds 251–260 (fresh), sandbox Rome (`--difficulty2 0`),
`random/mainland` 128, `conquest_civic_centers`, treasures disabled, 30
game-minute limit, biome/placement pinned. Baseline = last validated code
(HEAD, 20-minute trigger) run once on these seeds; treatment = concentrated
assault; canary = seed 251.

## Results

- Canary: **PASS**. 0 JS errors. Composite +9.67.
- Primary metric: **0/10 wins**. Two rams assemble at minute 24–28 (attack at
  24–28), the whole army mobilizes and marches at the CC — and dies within a
  minute of contact (melee 0 by minute 25 on the fastest seeds). End stats
  make the root cause explicit: **we trained 18 units (15 infantry + 3 rams);
  sandbox Rome trained 116 (90 infantry + 26 civilians)**. The assault never
  stood a chance — the bot's economy is ~1/6 of Rome's, and the force is
  hard-countered (all-hack spearmen vs Rome's ranged units + 20 garrison
  arrows; exchange 1:3, the CC takes zero damage).
- Gaul cannot train extra workers (the house trainer references
  `units/{civ}/support_civilian_house`, which does not exist for gaul — the
  civ scales through citizen soldiers only), so the missing engine is plain
  **army scaling**: more houses, more soldiers.

## Verdict

**Bad** (pre-registered: 0/10 wins ≤ 2/10). Reverted.

## Action

Revert the change (`git restore bot/`) and commit as `turn 027:
concentrated-assault — bad`. No `CHANGELOG.md` entry. G4 is reconsidered in
the next commit: it has resisted eight turns (018–027) with one consistent
root cause — the economy gap (18 vs 116 units trained).

## Next

Reconsider G4: split it into G4a — **army scaling** (≥ 50 melee soldiers by
minute ~22: 8 houses for pop, SOLDIER_TARGET 50, house placement on the
clearance ring) — and G4b — the win vs sandbox with the scaled army + rams.
See `turns/backlog.md`.
