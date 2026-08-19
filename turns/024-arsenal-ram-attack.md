# Turn 024 — Arsenal, ram, and the attack

Goal served: G4 (defeat sandbox Rome — this is the first turn that can
actually win).

## Hypothesis

> If the bot builds an arsenal in City Phase, trains siege rams there, and
> attacks — soldiers at 32 as before, rams sent straight at the enemy civic
> centre — under a 25-game-minute limit, then the bot wins (destroys the enemy
> CC) on ≥ 8/10 seeds, because every prerequisite now works (Town 9/10, City
> 9/10, 750/750 banked) and the ram's 150 crush damage per hit is the
> siege-appropriate tool turns 005/009 proved the spearmen are not. The
> 25-minute limit (from 20) is part of the change: turn 022's evidence showed
> the siege timeline cannot finish inside 20 minutes.

Primary metric: fraction of seeds won (enemy CC destroyed before the limit),
0 JS errors.

Verdict thresholds (pre-registered): good if ≥ 8/10 wins, 0 JS errors, canary
PASS; bad if ≤ 2/10 or error/determinism veto; neutral otherwise. Secondary
(reported, not the verdict): win minute, city minute, composite.

## Implementation

- `bot/maps/scripts/NonVisualTrigger.js`: `TIME_LIMIT_MS` 20 → 25 minutes.
- `bot/simulation/ai/vercingetorix/vercingetorix.js`:
  - `manageArsenal`: after `currentPhase() >= 3`, place one arsenal (300
    wood) on the forge double ring with the same clearance walk; foundation
    repaired by an arsenal-capable builder.
  - `manageRams`: while an arsenal exists and rams < 2, train
    `units/{civ}/siege_ram` there when wood ≥ 300 and metal ≥ 150.
  - The attack trigger drops the stone/metal gate (city + arsenal + rams
    spend those): attack at 32 soldiers, as before. The sweep commands idle
    rams to `attack()` the nearest enemy `CivCentre`; soldiers keep their
    attack-move sweep.
  - The `[HARNESS]` sample reports `arsenal` and `rams`.

## Experiment

Settings: seeds 221–230 (fresh), sandbox Rome (`--difficulty2 0`),
`random/mainland` 128, `conquest_civic_centers`, treasures disabled, 25
game-minute limit (the change), biome/placement pinned. Baseline = HEAD
(turn-023 commit, 20-minute trigger); treatment = siege endgame; canary =
seed 221.

## Results

- Canary: **PASS**.
- Primary metric: **0/10 wins**; the rams never train (0 everywhere), so
  nothing ever attacks the enemy CC. Arsenal completes on 6/10 (City reached
  on 8/10 at minute 18–20). Two failure modes:
  1. **JS errors, seeds 228/230 (41/37 — error veto):** `manageRams` calls
     `train` on the arsenal *foundation* — foundations carry the Arsenal
     class, so the `byClass("Arsenal")` filter matches them, but a foundation
     has no Trainer component.
  2. **Metal starvation:** the ram costs 150 metal, but City research spends
     the 750 metal bank; afterwards only the 2 metal workers gather (~0.4/s),
     so 150 metal arrives around minute 25 — after the limit. The bot must
     over-bank before researching City (gate City at metal ≥ 900, i.e. the
     750 cost + the 150 ram cost).
- Composite +9.69 would have been good, but the error veto forces bad —
  correctly so.

## Verdict

**Bad** (pre-registered: 0/10 wins ≤ 2/10, and the error veto). Reverted.

## Action

Revert the change (`git restore bot/`) and commit as `turn 024:
arsenal-ram-attack — bad`. No `CHANGELOG.md` entry. Louis asked to stop after
this turn — no turn 025 until his protocol feedback is incorporated.

## Next

Fix both failure modes, then retry: filter foundations out of the arsenal
lookup in `manageRams`, and gate City research on metal ≥ 900 (750 cost +
150 for the first ram) — possibly also stone ≥ 900 if the arsenal needs it.
See `turns/backlog.md`.
