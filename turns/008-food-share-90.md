# Turn 008 — food-share-90

- **Goal served:** G1 — reach 100 population as fast as possible. Best batch
  median to beat: **11 game-minutes** (turn 006).

## Hypothesis

> If the allocation target for food gatherers rises from 75 % to 90 % of all
> gatherers (idle workers go to food while food gatherers are below 90 %),
> then the batch median time-to-100 drops by ≥ 10 % versus the paired
> baseline, because training stalls on food < 50 for 8–14 of 19 match
> minutes (turn-007 evidence) while wood banks 200–2500 unused — food
> income, not the population cap, paces growth, and wood needs during the
> sprint (~17 houses ≈ 130 wood/min) are far below what ~10 % of gatherers
> still deliver.

Grounding (turn-007 samples, e.g. seed 63 baseline): food pinned at 6–64
through minutes 5–16 with 45–75 gatherers; wood climbs to 1500+ after
minute 14. Consumption ratio over the sprint is ~3500 food vs ~1300 wood;
the 75 % target under-weights food because effective food rates suffer
from walk time and supply depletion while woodlines near the CC stay dense.

**Primary metric (M):** time to 100 population (first per-minute `[HARNESS]`
sample with pop used ≥ 100), batch median over the 10 seeds, compared
against the paired baseline on the same seeds.

**Verdict thresholds (single-metric, protocol rule):**

- **good:** treatment median improves ≥ 10 % versus the paired baseline
  median **and** is ≤ 11 game-min; still ≥ 6/10 matches reaching 100; no
  JS-error/determinism veto.
- **bad:** treatment median worsens ≥ 10 %, or fewer than 6/10 reaching
  100, or any veto.
- **neutral:** otherwise.

## Experiment (specification, written before running)

- **Baseline:** turn-006 validated code (= current HEAD, commit `b7afd82`);
  fresh baseline batch on this turn's seeds.
- **Treatment:** working tree with the allocation-target change below.
- **Seeds (fresh draw for this turn):** 71, 72, 73, 74, 75, 76, 77, 78, 79, 80.
- **Opponent:** Petra, civ `rome`, difficulty 0 (sandbox, per G1).
- **Map/victory/limit:** `random/mainland` 192, `conquest_civic_centers`,
  treasures disabled, 300 pop cap, biome `generic/temperate`, placement
  `circle`, 20-game-minute limit.
- **Canary:** one extra baseline-code match on seed 71; stats must be
  byte-identical to the baseline seed-71 run.

## Implementation

One change: the food/wood allocation target in `play()`
(`bot/simulation/ai/vercingetorix/vercingetorix.js`) — idle gatherers go to
food while `foodWorkers * 10 < gatherers * 9` (90 %, was
`foodWorkers * 4 < gatherers * 3` = 75 %).

**Smoke-test iteration (v1 deadlocked):** the bare 90 % quota deadlocked on
seed 71 — population stuck at 35/35 from minute 4, wood pinned at 32 for 15
minutes, food banking thousands. Cause: `foodWorkers` counts only workers
whose current order target is a food supply, so gatherers returning to the
dropsite are undercounted; the quota then sends every idle to food, wood
income collapses to zero as woodlines deplete, and the house gate
(wood < 75) blocks forever. Fix (same change, folded in before the
experiment): food is assigned only while `wood >= 150` — a wood floor that
keeps the house pipeline fed regardless of the undercount. Below the floor,
idles go to wood (or metal while saving for the tech, unchanged).

- **Evidence of its own effect:** the per-minute `[HARNESS]` samples show
  it directly — food should sit above the 50 training gate for more of the
  sprint, wood should hover near the 150 floor instead of banking
  thousands, and the GATHER state mix shifts toward food. No new
  instrumentation needed.
- **Performance:** same per-tick loops, one changed comparison plus one
  resource lookup.

## Verdict

**neutral** (direction consistently negative, below the 10 % bad bar).

Primary metric: batch median time-to-100 = **13.0 game-minutes** treatment
vs **12.0** paired baseline (worse by 8.3 % — under the 10 % "bad"
threshold, but the paired deltas are −1, +1, −1, −2, −1, −1, 0, 0, −2, 0:
seven seeds worse, one better, two tied — a real small cost, not noise).
10/10 matches reach 100 on both sides.

- **Vetoes:** JS errors 0 on all 21 matches; canary **PASS**; wall 29–39 s
  per match both sides — no performance regression.
- **Composite report (for the record):** `total=+0.16`, "neutral".
- **Why it fails — the hypothesis's mechanism is distance-bound, not
  share-bound:** even with the 90 % quota, food sits at 20–80 through the
  sprint (smoke seed 71) while wood banks 4000+. Effective food income
  during the sprint is ≈ 450 food/min over ~45 assigned food gatherers ≈
  **0.17/s each** — versus 0.4–0.8/s for wood next to the CC. Adding food
  gatherers barely raises food income because berries/hunts near the CC
  are depleted and the remaining supplies are far away; the extra food
  workers mostly walk. Meanwhile the shift off wood slightly delays the
  house pipeline on several seeds.
- **Goal grading (G1):** best batch median unbeaten (**11**, turn 006 —
  different seed set; medians compare only within a paired batch).
  Consecutive turns without beating the best: **2**.

## Action

Neutral, cause understood (the lever targets the wrong bottleneck — food
*share* instead of food *rate*). **Reverted** — the code leaves no trace;
negative knowledge recorded here and in the backlog.

## Next

Backlog reworked: food-share changes are exhausted (both directions
tested — 75 % in turns 004–007, 90 % here). New top hypothesis: bring the
food closer — build farm fields next to the civil centre once near-CC
food supplies deplete. **Louis's instruction (2026-08-20): stop after this
turn — do not start turn 009 automatically.** Recorded in
`CURRENT_TURN.md`.
