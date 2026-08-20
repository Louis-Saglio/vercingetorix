# Turn 004 — food-first-allocation

- **Goal served:** G1 — reach 100 population as fast as possible.
- **Phase:** closed — verdict **good**, change validated.

## Hypothesis

> If idle gatherers are assigned by need — nearest **food** supply while
> food gatherers make up less than 75 % of all gatherers, nearest **wood**
> supply otherwise — instead of pure nearest-supply, then the batch mean of
> food gathered improves by **≥ 10 %** over the turn-002 baseline, because
> turn 003 proved food income is the binding constraint for G1 (training
> stalls with food pinned near 0 while wood/metal accumulate) and reaching
> 100 population needs food:wood ≈ 4:1 (~4550 food for workers, ~1200 wood
> for houses).

Grounding:

- Gather rates (`template_unit_support_civilian.xml`): civilians gather
  `food.fruit`/`food.meat` at 1/s vs `wood.tree` 0.7/s — food sources are
  not rate-penalized, they are simply outnumbered by trees under
  nearest-supply choice.
- Turn 002/003 evidence: need-blind batches ended with food 2000–2900 but
  wood up to 5945 and metal up to 2929 — the allocation, not the map,
  starves food.
- The 75/25 quota matches the G1 requirement ratio (4550 food / 1200 wood ≈
  79/21, rounded to a simple 3:1). Stone/metal buy nothing before Town phase
  and are ignored.
- This turn runs on the turn-002 code base (houses reverted in turn 003), so
  population stays capped at 20 — the extra food cannot show up as
  population yet. The metric is therefore the income shift itself; the G1
  payoff is measured next turn when houses are restored.

**Primary metric (M):** `resourcesGathered.food` at match end (end-of-game
statistics; `vegetarianFood` is a subset of `food` and excluded), batch mean
over the 10 seeds, treatment vs baseline.

**Verdict thresholds (single-metric, protocol defaults):**

- **good:** mean food gathered improves ≥ 10 %, no JS-error/determinism
  veto.
- **bad:** mean food gathered worsens ≥ 10 %, or any veto.
- **neutral:** otherwise.

## Experiment (specification, written before running)

- **Baseline:** turn-002 validated code (= current HEAD, commit `a0dcc8f`'s
  parent code state — HEAD itself); fresh baseline batch on this turn's
  seeds.
- **Treatment:** working tree with the allocation change below.
- **Seeds (fresh draw for this turn):** 31, 32, 33, 34, 35, 36, 37, 38, 39, 40.
- **Opponent:** Petra, civ `rome`, difficulty 0 (sandbox, per G1).
- **Map/victory/limit:** `random/mainland` 192, `conquest_civic_centers`,
  treasures disabled, 300 pop cap, biome `generic/temperate`, placement
  `circle`, 20-game-minute limit.
- **Canary:** one extra baseline-code match on seed 31; stats must be
  byte-identical to the baseline seed-31 run.

## Implementation

One change: need-based target selection in the turn-001 gathering loop
(`bot/simulation/ai/vercingetorix/vercingetorix.js`).

- `nearestSupply` gains a resource filter: it only considers supplies whose
  generic type is in an allowed set passed by the caller.
- In `play()`, before assigning idle gatherers, count how many own units are
  currently gathering food vs total gatherers: read each unit's
  `unitAIOrderData()[0].target`, resolve it with `gameState.getEntityById`
  and read `getResourceType()` (the same pattern `currentGatherRate` uses).
  Units ≤ 20 on this code base — cheap once per play tick.
- An idle gatherer is sent to the nearest **food** supply if food gatherers
  are below 75 % of all gatherers (and it can gather food), otherwise to the
  nearest **wood** supply; if no suitable supply of the wanted type is cached,
  fall back to the unrestricted nearest supply (never leave a unit idle for
  lack of a preferred type). Cavalry (meat-only) is unaffected — its rate
  filter already restricts it to animals.
- **Evidence of its own effect:** the per-minute samples' `food`/`wood`
  fields show the income shift directly; the `states` histogram confirms
  workers stay on `GATHER` (no idle fallout from the quota).
- **Performance:** one O(units) allocation scan + the existing
  O(units × supplies) nearest search per play tick; no new map scans.

## Verdict

**good.**

Primary metric: batch mean `resourcesGathered.food` = **4718** vs **2224**
baseline — **+112 %**, far above the ≥ 10 % bar, and consistent on every seed
(treatment 3824–5564, baseline 1100–3878). Wood holds at ~2200 every match
(the 25 % quota working as designed); stone/metal drop to 0 (deliberate —
nothing buys them before Town phase).

- **Vetoes:** JS errors 0 on all 20 matches; canary **PASS**; wall 15–19 s
  per 6000-turn match on both sides — no regression.
- **Composite report (for the record):** `total=-0.68`, "neutral" — the
  composite penalizes the deliberate stone/metal/wood sacrifice
  (resourcesGathered total 6911 vs 8250). The pre-registered single-metric
  thresholds govern this turn: the trade is the hypothesis, not a side
  effect. Noted as a known limitation of the need-blind composite when a
  hypothesis intentionally reallocates between composite inputs.
- **Behaviour observed:** food income ~3.4/s sustained even after the 20-cap
  stops training (stockpile 4900+ by minute 19 on the smoke seed) —
  consistent with the ~4550 food G1 needs once houses return.
- **Goal grading (G1):** all matches still G1 *Fail* (capped at 20 — houses
  are still out). Goal-progress: the food constraint measured in turn 003 is
  removed.

## Action

Validate: **keep the change.**

Observations carried forward:

- Food sources near the CC (berries + hunt) sustained ~15 food workers for
  20 minutes on all 10 seeds — no local exhaustion at this scale.
- With training capped at 20 and no houses, most of the food income is
  unused stockpile; the value materializes only with houses (next turn).

## Next

Backlog top: restore turn 003's house building (same experiment design and
≥ 6/10 threshold). With the food constraint fixed, 100 pop in 20 game-min
should be reachable.
