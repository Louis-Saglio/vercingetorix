# Turn 007 — Reachable bigger pre-attack army

Goal served: G2 (defeat sandbox Rome).

## Hypothesis

> If I raise the soldier target from 20 to 27 (the largest target the current
> 3-house cap can hold without needing a 4th house), then the composite score
> improves versus baseline, because a 27-spearman army trains, gathers, and
> kills more than a 20-spearman army and is the first valid test of the
> "bigger army" prerequisite for overrunning the enemy base.

Primary metric: protocol-default composite score (good ≥ +4, bad ≤ −4, neutral
otherwise), with the error veto and the determinism canary. G2 win rate is
reported alongside it (win = enemy CC captured/destroyed before the limit).

## Implementation

One constant in `bot/simulation/ai/vercingetorix/vercingetorix.js`:

- `const SOLDIER_TARGET = 20;` → `const SOLDIER_TARGET = 27;`

27 is the largest target reachable with the current 3-house cap (35 population):
27 melee + the bot's 8 non-melee units (4 laborers + 4 starting cavalry) = 35.
`ATTACK_THRESHOLD` is defined as `SOLDIER_TARGET`, so the attack also waits for
27 soldiers. The sweep is unchanged.

## Experiment

Settings: seeds 51–60 (first batch) then 61–70 (doubled-N repeat), sandbox
Rome (`--difficulty2 0`), `random/mainland` 128, `conquest_civic_centers`,
treasures disabled, 20 game-minute limit, biome/placement pinned. Baseline =
HEAD (turn-004 code); treatment = `SOLDIER_TARGET=27`; canary = seed 51.

Results (combined N = 20):

- Canary: **PASS**.
- Composite: first batch **+1.51**, combined 20 pairs **+3.79**, error veto
  false → **neutral** (still below +4).
- Win rate: 0/20 in both arms (all time-limit draws; the sweep still never
  captures the CC).
- The bigger army does slightly more military work (a few seeds train/kill
  more), but the effect is small and inconsistent across seeds, and it never
  reaches the objective.

## Verdict

**Neutral.** Combined composite +3.79 < +4 after the doubled-N repeat, 0 wins,
no error/determinism veto. Per protocol, still neutral after the repeat →
revert.

## Action

Revert the change (`git restore bot/simulation/ai/vercingetorix/vercingetorix.js`)
and commit as `turn 007: reachable-bigger-army — neutral`. No `CHANGELOG.md`
entry (reverted change leaves no trace in code, only the journal).

## Next

G2 remains open. Negative knowledge: a larger army (27 vs 20) with the old
nearest-enemy sweep does not convert into CC captures — the sweep never
focuses the objective. The next real lever is combining a big-enough army with
CC focus, or decomposing G2 into a "sustain a large army" prerequisite first.
See `turns/backlog.md`.
