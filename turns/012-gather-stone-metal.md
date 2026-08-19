# Turn 012 — Gather stone and metal

Goal served: G3 (defeat sandbox Rome, via the siege path).

## Hypothesis

> If I make the bot gather stone and metal in addition to wood and food, then
> the bot accumulates the 750 stone + 750 metal that City Phase requires,
> because the resource scan and gather split are extended to the two resources
> the baseline never touches.

Primary metric: fraction of seeds that reach ≥ 750 stone AND ≥ 750 metal by
game-minute 16 (0 JS errors).

Verdict thresholds (pre-registered): good if ≥ 8/10 seeds, 0 JS errors, canary
PASS; bad if ≤ 2/10 or error/determinism veto; neutral otherwise.

## Implementation

In `bot/simulation/ai/vercingetorix/vercingetorix.js`:

- The per-tick resource scan now also collects `stoneResources` and
  `metalResources` (gaia entities with `getResourceType()` "stone"/"metal").
- `manageSoldiers` takes the four resource arrays and splits idle gatherers
  wood/food/stone/metal by `entity id % 4` instead of wood/food by `% 3`.
- The per-minute `[HARNESS]` sample now reports `stone` and `metal`.

## Experiment

Settings: seeds 111–120 (fresh), sandbox Rome (`--difficulty2 0`),
`random/mainland` 128, `conquest_civic_centers`, treasures disabled, 20
game-minute limit, biome/placement pinned. Baseline = HEAD (turn-011 code);
treatment = stone/metal gathering; canary = seed 111.

Results:

- Canary: **PASS**.
- Primary metric: **0/10** in both arms reach 750 stone + 750 metal by minute
  16. Stone never rises above the starting 300 (no stone was gathered); metal
  reaches ~670–700 but not 750.
- Composite: **−18.33** → bad; the 4-way split starves wood/food, collapsing the
  bot's economy and kills.

## Verdict

**Bad.** 0/10 on the primary metric, and the change cripples the economy
(composite −18.33). Reverted.

## Action

Revert the change (`git restore bot/simulation/ai/vercingetorix/vercingetorix.js`)
and commit as `turn 012: gather-stone-metal — bad`. No `CHANGELOG.md` entry.

## Next

Stone/metal gathering as a naive 4-way split fails: stone is not found within
the 160 m scan (or is too rare), and splitting gatherers starves wood/food.
The siege path needs a targeted gatherer assignment, not a blanket split. See
`turns/backlog.md`.
