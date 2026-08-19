# Turn 006 — Grow a bigger pre-attack army

Goal served: G2 (defeat sandbox Rome).

## Hypothesis

> If I raise the soldier target from 20 to 32 (the largest army the current
> 4-house cap can hold), then the composite score improves versus baseline,
> because a 32-spearman army gathers, trains, and kills more than a 20-spearman
> army; this also moves G2 forward by giving the bot a larger force to overrun
> the enemy base.

Primary metric: protocol-default composite score (good ≥ +4, bad ≤ −4, neutral
otherwise), with the error veto and the determinism canary. G2 win rate is
reported alongside it (win = enemy CC captured/destroyed before the limit).

## Implementation

One constant in `bot/simulation/ai/vercingetorix/vercingetorix.js`:

- `const SOLDIER_TARGET = 20;` → `const SOLDIER_TARGET = 32;`

`ATTACK_THRESHOLD` is defined as `SOLDIER_TARGET`, so the attack threshold
rises with it — the bot keeps gathering and training until it has 32 citizen
soldiers before attacking. 32 is the largest army the current 4-house cap
(20 + 4×5 = 40 population) can hold: the bot's non-melee population is 8
(4 starting laborers + 4 starting cavalry), so 32 melee is the ceiling.
The sweep itself is unchanged.

## Experiment

Settings: seeds 41–50 (fresh), sandbox Rome (`--difficulty2 0`), `random/mainland`
128, `conquest_civic_centers`, treasures disabled, 20 game-minute limit,
biome/placement pinned. Baseline = HEAD (turn-004 code); treatment =
`SOLDIER_TARGET=32`; canary = seed 41 repeated with the baseline code.

Results:

- Canary: **PASS**.
- Composite: total **−3.31**, error veto false → **neutral** by the numeric
  thresholds.
- Win rate: 0/10 in both arms (all time-limit draws).
- **The treatment never attacked.** Per-minute samples show it stalls at
  **28 melee soldiers, population 35/35, 3 houses** — it cannot build the 4th
  house, so it never reaches 32, and because `ATTACK_THRESHOLD` follows
  `SOLDIER_TARGET`, `attackStarted` never flips true. `enemyUnitsKilledValue`
  drops to ~0 and `unitsTrained` drops to 21–26 (vs baseline 37–61), which is
  the whole composite loss.

## Verdict

**Invalid.** The implementation did not test the hypothesis: 32 soldiers was
chosen as "reachable with 4 houses", but the bot's house logic only ever gets
to 3 houses here (pop caps at 35), so the army stalls at 28 and never attacks.
The idea (a bigger army) was not exercised; the chosen target was wrong, not
refuted. Marking invalid rather than grinding a repeat of a deterministically
broken run.

## Action

Revert the change (`git restore bot/simulation/ai/vercingetorix/vercingetorix.js`)
and commit as `turn 006: bigger-army — invalid`. No `CHANGELOG.md` entry.

## Next

G2 remains open. The fix is to grow the army *and its housing together* in one
change: raise `SOLDIER_TARGET` and `HOUSE_TARGET` (e.g. 32 → 5 houses, or 40 →
6 houses) so the cap can actually hold the target, and then re-test whether a
larger army overruns the CC. That is the next candidate turn.
