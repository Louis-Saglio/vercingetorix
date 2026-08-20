# Turn 001 — gather-starting-workers

- **Goal served:** G1 — reach 100 population as fast as possible.
- **Phase:** closed — verdict **good**, change validated.

## Hypothesis

> If every idle starting unit able to gather is ordered to gather the nearest
> suitable resource supply around the civil centre, then the batch mean of
> `resourcesGathered` (sum of food+wood+stone+metal at match end) rises from
> 0 (do-nothing baseline) to **≥ 2000 per match** (matches run to the shipped
> 30-game-minute limit), because
> income from the 9 starting units is the prerequisite for everything G1
> needs (food for training, wood for housing).

Grounding (from `docs/game_description/` and the pinned 0.28.0 data):

- Gauls start on `random/mainland` with a civil centre, 4 `support_civilian`,
  2 `infantry_spearman_b`, 2 `infantry_javelineer_b`, 1 `cavalry_javelineer_b`
  (`public/simulation/data/civs/gaul.json` → `StartEntities`), i.e. 9 gatherers
  for 9 population; pop limit 20 from the civil centre.
- Starting resources: 300 of each type (game default "Low",
  `starting_resources.json`) — too little to sustain training without income.
- Gather rates (`template_unit_support_civilian.xml`,
  `template_unit_infantry.xml`, `template_unit_cavalry.xml`): civilians gather
  everything (fruit/meat 1, wood 0.7, stone/metal 0.35 per s), infantry the
  same at reduced rates, cavalry only `food.meat` at 5/s. With ~9 gatherers at
  an effective ~0.5–0.8 /s over 1200 s, several thousand resources are
  plausible; 2000 is a conservative bar, 500 means the mechanism barely ran.

**Primary metric (M):** `resourcesGathered` total at match end, batch mean over
the 10 seeds, from the end-of-game statistics JSON.

**Verdict thresholds (single-metric hypothesis):**

- **good:** mean ≥ 2000, no JS-error or determinism veto.
- **bad:** mean ≤ 500, or any veto (JS errors up, canary mismatch).
- **neutral:** in between.

## Experiment (specification, written before running)

- **Baseline:** HEAD — the do-nothing bot (commit `cfe308b` lineage).
- **Treatment:** working tree with the gathering implementation below.
- **Seeds (fresh draw for this turn):** 1, 2, 3, 4, 5, 6, 7, 8, 9, 10.
- **Opponent:** Petra, civ `rome`, **difficulty 0 (sandbox)** — G1 specifies a
  non-interfering opponent; this overrides the protocol's default difficulty 3
  for as long as G1 is active.
- **Map/victory/limit:** `random/mainland` 192, `conquest_civic_centers`,
  treasures disabled, 300 pop cap, biome `generic/temperate`, placement
  `circle`, **30 game-minute limit** — correction to the spec written above:
  the shipped trigger enforces `TIME_LIMIT_MS = 30 * 60 * 1000`
  (`bot/maps/scripts/NonVisualTrigger.js:9`; its comment says 20). Found
  before any batch result was read; baseline and treatment share it, so the
  comparison is unaffected. The hypothesis bar (≥ 2000) stays conservative
  either way. The protocol/trigger mismatch is a post-turn reflection item.
- **Canary:** one extra baseline-identical match on seed 1 in the baseline
  batch; must be byte-identical in stats to the original seed-1 baseline run.

## Implementation

One change: a gathering assignment loop in
`bot/simulation/ai/vercingetorix/vercingetorix.js`.

- On the first update, find the own civil centre (`hasClass("CivCentre")`) and
  scan `gameState.getEntities()` **once** for entities with a `ResourceSupply`
  within 140 m of it; cache their ids. (One scan, not per tick — performance
  rule 9.)
- Every 8th sim turn (throttle counter, serialized), for each own unit with
  `ent.isGatherer()` and `ent.isIdle()`: pick the nearest cached supply
  (squared distance from the unit) with `resourceSupplyAmount() > 0` that the
  unit can actually gather (`resourceGatherRates()["generic.specific"] > 0`,
  generic fallback) and order `ent.gather(target)`. Units return to the civil
  centre dropsite on their own (UnitAI default).
- If no cached supply suits (exhaustion), rescan with the radius grown by 80 m
  (capped at 500 m). Newly trained units are picked up automatically the next
  time they are idle.
- **Evidence of its own effect:** the existing per-minute `[HARNESS]` samples
  already carry `food`/`wood`/`stone`/`metal` and the `states` histogram —
  the change is visible as `INDIVIDUAL.GATHER.*` states replacing
  `INDIVIDUAL.IDLE` and as rising resources. No extra instrumentation needed.
- **Performance:** one full scan at start, then O(units × cached supplies)
  every 8 turns; no per-tick map scans.

## Verdict

**good.**

Primary metric (pre-registered thresholds): batch mean `resourcesGathered`
= **6709** (min 6108, median 6676, max 7520; `vegetarianFood` excluded — it is
a subset of `food`, see `harness/src/report.rs`) vs **0** on every baseline
match. Far above the ≥ 2000 bar; the single-metric rule (≥ 10 % relative
improvement) is trivially satisfied.

- **Vetoes:** JS errors 0 on all 20 matches; canary **PASS**; turn rate
  unchanged (9000 turns in ~22–28 s wall on both sides, ~360–410 t/s) — no
  performance regression from the init scan + 8-turn loop.
- **Composite report (for the record):** `total=+4.00` (all pairs draw–draw,
  quality component only), printed verdict "neutral" — a harness float bug:
  0.4 × 10 = 3.999… < 4.0 threshold. Post-turn reflection item.
- **In-turn fixes:** two — (1) `nearestSupply` crashed after the radius-widen
  branch nulled `supplyIds` mid-loop (null guard added); (2) positions in the
  AI realm are `[x, z]` pairs, not `[x, y, z]` (`AIProxy.js:92,232`) — the
  cache matched zero supplies until indices were fixed.
  `docs/DEVELOPER_GUIDE.md` AI API reference corrected accordingly.
- **Goal grading (G1):** every match is a G1 *Fail* (100 population never
  reached — pop stayed 9/20; no training exists yet, as designed for this
  turn). The turn is goal-progress, not goal-achievement: income is the
  prerequisite for training and housing.

## Action

Validate: **keep the change.** The bot now gathers from all 9 starting units
from game-minute 1 (samples show `INDIVIDUAL.GATHER.*` replacing
`INDIVIDUAL.IDLE`).

Negative knowledge / observations carried forward:

- Nearest-supply allocation is need-blind: seeds 4, 5, 6, 8 gathered 0 stone
  or 0 metal while food is the only near-term need. Allocation by need is a
  backlog item.
- The shipped trigger enforces 30 game-minutes while the protocol default and
  the trigger's own comment say 20 — post-turn reflection item.
- Harness verdict boundary bug (above) — post-turn reflection item.

## Next

Backlog top (see `turns/backlog.md`): continuous civilian training at the
civil centre — the only way to move G1's population metric now that income
exists.
