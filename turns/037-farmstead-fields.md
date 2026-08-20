# Turn 037 — Farmstead and fields

Goal served: G4a2 (robust renewable economy).

## Hypothesis

> If the bot builds a farmstead and four fields after Town and its food
> gatherers include the bot's own fields (fields are owned entities, and the
> gaia-only food filter excludes them), then ≥ 8/10 seeds have the farmstead
> and ≥ 3 fields built by minute 16 with 0 JS errors, because the field
> template is the renewable food engine (ResourceSupply food.grain, Max
> Infinity, 5 gatherers each) that removes the finite-early-food
> batch-dependence behind G4b's 5/10-vs-0/10 split (turn 036's
> reconsideration).

Primary metric: fraction of seeds with ≥ 1 farmstead AND ≥ 3 fields at the
minute-16 sample, 0 JS errors.

Verdict thresholds (pre-registered): good if ≥ 8/10 seeds reach the metric,
0 JS errors, canary PASS; bad if ≤ 2/10 or error/determinism veto; neutral
otherwise. Secondary (reported, not the verdict): late-game food rate,
composite. In-turn fix-and-rerun iterations allowed.

## Implementation

In `bot/simulation/ai/vercingetorix/vercingetorix.js`:

- `manageFarmstead`: after Town, build one farmstead (100 wood, 45 s) on
  the house ring walk with clearance.
- `manageFields`: while the farmstead exists and fields < 4, place fields
  (100 wood each) at 30 m offsets around the farmstead.
- The food resource list in `play()` now also includes the bot's own
  entities with `getResourceType() == "food"` (the fields) — the gaia-only
  owner filter is relaxed for food.
- The `[HARNESS]` sample reports `farmstead` and `fields`.

## Experiment

Settings: seeds 311–320 (fresh), sandbox Rome (`--difficulty2 0`),
`random/mainland` 128, `conquest_civic_centers`, treasures disabled, 30
game-minute limit, biome/placement pinned. Baseline = last validated code
(HEAD, turn-029 state) run once on these seeds; treatment = farmstead +
fields; canary = seed 311.

## Results

**Iteration 1 (farmstead + fields):** 0/10 — the farmstead barely builds
(1/10, one field): post-town soldier training eats the wood and the
100-wood farmstead never gets its turn (the turn-020 pattern again).

**Iteration 2 (in-turn fix):** training holds until the farmstead AND the
four fields are built — wood pools for the food engine first. Rerun below.

**Iteration 2 result:** deadlock — 0/10, melee stuck at 2 everywhere,
composite −13.05. The gate holds training forever because the farmstead and
fields never build: the manager order (houses → forges → arsenal →
farmstead) lets the 600-wood forges consume the pooled wood first on ~5
gatherers' income, so the farmstead's 100 wood never arrives, the fields
never start, and training never resumes. The renewable-food program needs
its own build order (farmstead + fields before the forges) or a gate on the
farmstead alone — next session's hypothesis.

## Verdict

**Bad** (pre-registered: 0/10 ≤ 2/10). Reverted.

## Action

Revert the change (`git restore bot/`) and commit as `turn 037:
farmstead-fields — bad`. No `CHANGELOG.md` entry. Louis asked to stop after
this turn — the deadlock fix is recorded for the next session.

## Next

Farmstead + fields with the corrected build order (farmstead and fields
before the forges in `play()`, and/or the training gate on the farmstead
alone), then grade the renewable food engine. See `turns/backlog.md`.
