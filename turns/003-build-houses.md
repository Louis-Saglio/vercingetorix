# Turn 003 — build-houses

- **Goal served:** G1 — reach 100 population as fast as possible.
- **Phase:** closed — verdict **neutral**, change reverted. **Erratum
  (turn 005):** the Action section below claimed the reverted code was
  recoverable from this turn's commit — it was reverted before committing
  and is not in git history; turn 005 re-wrote it from the record above.

## Hypothesis

> If the bot builds houses (2 builders per foundation, one house in flight at
> a time) whenever population headroom (limit − used) drops below 3 and wood
> ≥ 75, until the population limit reaches 105, then **100 population is
> reached before the 20-game-minute limit in at least 6 of 10 matches**,
> because housing is the binding constraint: turn 002 showed the economy
> pinned at 20/20 from game-minute ~2 with food accumulating unused.

Grounding (from `docs/game_description/` and the pinned 0.28.0 data):

- House (gaul): 75 wood, 30 s build time, +5 population, own territory
  (`generic/buildings/house.md`). CC gives 20 → 16 houses needed for 100
  (`mechaniques/population_and_entity_limits.md`; foundations give nothing).
- Construction is two-step (`mechaniques/construction.md`):
  `ent.construct(...)` places a foundation (full cost paid immediately;
  placement failure destroys it *before* resources are taken — failed
  candidates are free), then `ent.repair(foundation)` builds it. Build time
  with N rate-1 builders: `30 / N^0.7` s → ~18.5 s with 2 builders.
- Civilians are builders (rate 1.0); with autocontinue they resume gathering
  nearby after finishing.
- Feasibility estimate: 16 houses ≈ 5 min of serial building + 1200 wood;
  91 more civilians = 4550 food. Turn-002 incomes (20 workers) cover both
  well inside 20 minutes on wood-normal seeds; wood-poor seeds (turn 002
  showed 425 wood total on seed 15's baseline side) may not make it — hence
  the 6/10 bar, not 10/10.

**Primary metric (M):** time to 100 population (first per-minute `[HARNESS]`
sample with pop used ≥ 100), per match; batch summary = count of matches
reaching 100 + median time among those. Baseline (turn-002 code) never
exceeds 20.

**Verdict thresholds (single-metric hypothesis):**

- **good:** ≥ 6/10 matches reach 100 pop, no JS-error/determinism veto.
- **bad:** the population limit never rises above 20 in ≥ half the matches
  (placement mechanism broken), or any veto.
- **neutral:** otherwise (houses built but 100 reached in fewer than 6).

## Experiment (specification, written before running)

- **Baseline:** turn-002 validated code (commit `8e36672`); fresh baseline
  batch on this turn's seeds.
- **Treatment:** working tree with the house-building loop below.
- **Seeds (fresh draw for this turn):** 21, 22, 23, 24, 25, 26, 27, 28, 29, 30.
- **Opponent:** Petra, civ `rome`, difficulty 0 (sandbox, per G1).
- **Map/victory/limit:** `random/mainland` 192, `conquest_civic_centers`,
  treasures disabled, 300 pop cap, biome `generic/temperate`, placement
  `circle`, 20-game-minute limit.
- **Canary:** one extra baseline-code match on seed 21; stats must be
  byte-identical to the baseline seed-21 run.

## Implementation

One change: house construction in `play()` in
`bot/simulation/ai/vercingetorix/vercingetorix.js`.

- New serialized state: `houseSpotIndex` (deterministic candidate sequence),
  `housePending` (`{x, z}` of a just-placed construct order awaiting its
  foundation), `houseFoundationId` (foundation being built).
- Candidate spots are deterministic around the civil centre: ring
  `radius = 26 + 10 * floor(i / 10)`, `angle = (i % 10) * 36°`, fixed
  building angle. A candidate is skipped if within 12 m of any own structure
  or 9 m of a cached resource supply (house footprint 13×13; CC 32×32 —
  `template_structure_civic_house.xml`,
  `template_structure_civic_civil_centre.xml`).
- Each play tick:
  1. If `housePending`: look for an own `Foundation`-class entity near the
     pending spot. Found → order the 2 nearest civilians
     (`hasClass("Support")`) to `repair` it (autocontinue), record
     `houseFoundationId`, clear `housePending`. Not found → the placement
     failed (destroyed before charging); advance `houseSpotIndex`, clear
     `housePending` (retry next tick).
  2. If `houseFoundationId` no longer resolves to a `Foundation`-class
     entity → construction finished; clear it.
  3. If no pending/foundation in flight, `getPopulationLimit() < 105`,
     headroom `< 3`, and `wood ≥ 75`: order the civilian nearest the next
     valid candidate to `construct(applyCiv("structures/{civ}/house"), x, z,
     angle)`; set `housePending`, advance `houseSpotIndex`.
- **Evidence of its own effect:** the sample `pop` field shows the *limit*
  rising (20 → 25 → …) as houses complete; the `states` histogram shows
  `INDIVIDUAL.REPAIR.*` during construction. No new instrumentation needed.
- **Performance:** candidate validation walks own structures (≤ ~20) and
  cached supply ids (a few hundred) at most once per play tick; no new map
  scans.

## Verdict

**neutral** (after one in-turn fix-and-rerun).

First treatment batch: 2 JS errors on seed 23 (`spotBlocked` iterated
`this.supplyIds` after `nearestSupply`'s radius-widening had nulled it
mid-tick — same bug class as turn 001's) → error veto → **bad**. The bug was
small and understood: null guard added, treatment rerun on the same seeds
against the same baseline. Rerun: **0 JS errors on all matches, canary
PASS** → the veto clears.

Against the pre-registered thresholds on the clean rerun:

- 100 population reached in **0/10** matches (< 6 → not good).
- The population limit rose above 20 in **10/10** matches (final pops
  51–76 used / 55–80 limit) → not bad.
- → **neutral**.

The composite report reads `total=+14.90`, verdict good — the mechanism
unambiguously works (housing more than tripled final population vs the
20-cap baseline on every seed). The single-metric bar was not met because
the hypothesis's causal claim was half-wrong: housing **was** the constraint
at 20 pop, but once houses lift the cap, **food income becomes the binding
constraint** — samples show food pinned near 0 from minute ~5 (training
drains 50 food per worker) while wood and metal accumulate unused
(need-blind nearest-supply allocation sends most workers to trees/rocks).
~4550 food is needed for the remaining workers; need-blind food income
(~1.5–2/s effective) supplies roughly half of that in 20 minutes.

- **Goal grading (G1):** all matches still G1 *Fail* (100 never reached).

## Action

**Neutral → revert** (protocol rule 7: only validated improvements persist;
the fix that would make this turn converge — need-based gatherer allocation
— is a different change, backlog item, not an in-turn fix). The house code
leaves no trace in the working tree; it is preserved in this turn's commit
history (`git show <turn-003-commit>:bot/simulation/ai/vercingetorix/vercingetorix.js`)
and is ready to restore once food allocation lands.

Negative knowledge recorded:

- Housing mechanics are solved: deterministic ring placement with structure/
  supply avoidance, failure detection via missing foundation, 2 builders per
  foundation, one house in flight — 0 JS errors, houses complete, limit rises
  monotonically. Composite +14.90 quantifies the improvement that food
  starvation caps.
- **Food, not housing, is now the binding constraint for G1.** Allocation by
  need (backlog) is the prerequisite; houses should be restored right after.
- Bug pattern twice seen (001, 003): cached-collection fields nulled by a
  widening/rescan path must be guarded in every consumer. Both fixed at the
  call sites.

## Next

Backlog top becomes: allocate gatherers by need (food first) — the proven
binding constraint. Houses return immediately after as "restore turn 003's
validated-mechanism code" with the same experiment design; with food
unblocked, the ≥ 6/10 bar should be reachable.
