# Turn 031 — Assault-ready army, corrected metric

Goal served: G4a (assault-ready army), feeding G4b (the win).

## Hypothesis

> If the ram gate is 32 soldiers (turn 030's change, re-tested) under the
> corrected G4a metric — ≥ 32 melee at minute 22, ≥ 2 rams by minute 26,
> attack fired by minute 28 — then ≥ 8/10 seeds reach it, because turn 030
> showed the army side is already there (25–47 melee at t22) and the ram
> timeline needs the corrected window (City t20–29 → arsenal +180 s → two
> rams: 600 wood + 300 metal ≈ +3.5 min). The attack then fires with a
> 32–53-soldier army — the first real assault since turn 027's 18-unit force.

Primary metric: fraction of seeds with ≥ 32 melee at the minute-22 sample
AND ≥ 2 rams at the minute-26 sample AND attackStarted by minute 28, 0 JS
errors.

Verdict thresholds (pre-registered): good if ≥ 8/10 seeds reach the metric,
0 JS errors, canary PASS; bad if ≤ 2/10 or error/determinism veto; neutral
otherwise. Secondary (reported, not the verdict): wins before the 30-minute
limit, composite. In-turn fix-and-rerun iterations allowed.

## Implementation

In `bot/simulation/ai/vercingetorix/vercingetorix.js`: `RAM_ARMY_GATE = 32`
constant; `manageRams` gates on it (turn 030's change, reverted as its bad
verdict required).

## Experiment

Settings: seeds 281–290 (fresh), sandbox Rome (`--difficulty2 0`),
`random/mainland` 128, `conquest_civic_centers`, treasures disabled, 30
game-minute limit, biome/placement pinned. Baseline = last validated code
(HEAD, turn-029 state) run once on these seeds; treatment = ram gate at 32;
canary = seed 281.

## Results

**Iteration 1 (ram gate at 32):** 0/10 — the army is strong (27–51 melee at
t22) but no rams by t26, and the samples show why: the forges starve (wood
5–40 from minute 14 to 26, forges 0–2) — the turn-029 1:1 post-town split
halved the wood income, so the army's 50-wood training eats everything and
the 200-wood forges never pool; City research never posts (no 3 Town
structures), so the arsenal and rams never exist.

**Iteration 2 (in-turn fix):** soldiers return to 2:1 wood:food (wood for
the structures restored); the two post-town food workers stay (the food half
of the soldier cost). Rerun below.

**Iteration 2 result — the breakthrough:** composite **+4.98** (good band),
0 JS errors, canary PASS, and **the first wins of the project**: seeds 282
and 285 destroy the enemy CC (attack at minute 25/27, win before minute
26/30). The assault fires on 4/10 seeds by t28. But the pre-registered
metric itself fails 0/10: the 2-rams-by-t26 deadline is structurally
unreachable — City lands at t22–27, the arsenal builds 180 s after, and two
rams need ~3.5 more minutes (t26–29). The wins came from the fast seeds
where the whole chain lands early.

## Verdict

**Bad** (pre-registered: 0/10 ≤ 2/10). Reverted — the metric, not the code,
was wrong; the change produced the project's first wins. The negative
knowledge is the corrected timeline.

## Action

Revert the change (`git restore bot/`) and commit as `turn 031:
assault-ready-corrected — bad (first wins)`. No `CHANGELOG.md` entry for the
code; the journal records the breakthrough. GOALS.md keeps the corrected
G4a; G4b's win grading moves up as the next pre-registered metric.

## Next

Turn 032: re-apply the change (ram gate 32, 2:1 soldier split, food
workers), pre-register the **G4b win metric** (wins before the 30-minute
limit ≥ 8/10), and iterate on the ram timeline — the understood levers: one
post-town worker from food to metal (City earlier), or a third ram. See
`turns/backlog.md`.
