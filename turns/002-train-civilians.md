# Turn 002 — train-civilians

- **Goal served:** G1 — reach 100 population as fast as possible.
- **Phase:** closed — verdict **good**, change validated.

## Hypothesis

> If the civil centre continuously trains `support_civilian` workers (one
> queued at a time, only while food ≥ 50 and population room exists), then
> the population grows from the static 9 (turn-001 baseline) to the 20-pop
> housing cap in every match, with a batch **median time-to-20 ≤ 10 game
> minutes**, because training is the only way to raise population and the
> turn-001 income (food ≳ 1/s early) plus the 300 starting food covers the
> 550 food needed for 11 workers (50 food, 8 s each).

Grounding (from `docs/game_description/` and the pinned 0.28.0 data):

- `structures/gaul/civil_centre` trains `units/{civ}/support_civilian`
  (50 food, 8 s, 1 pop; `generic/units/support_civilian.md`).
- Population accounting (`mechaniques/population_and_entity_limits.md`):
  `popUsed` includes started training batches (reservation at batch start),
  so `getPopulation() < getPopulationLimit()` is the correct gate — queued
  reservations already count; training blocked at the cap fails silently,
  so the bot must not queue when full.
- Turn 001 evidence: food income with 9 mixed-allocation gatherers reaches
  food ≈ 560 by minute 1 and ≈ 1100 by minute 5 while spending nothing;
  training drains 375 food/min at full rate, so food will oscillate near 0 —
  expected, and the queue-when-food-≥-50 gate handles it.

**Primary metric (M):** time to reach population 20 (`pop` field of the
per-minute `[HARNESS]` samples, first sample at 20/20), batch median over the
10 seeds. The baseline never leaves 9.

**Verdict thresholds (single-metric hypothesis):**

- **good:** 20/20 reached in every match, median time-to-20 ≤ 10 min, no
  JS-error/determinism veto.
- **bad:** 20/20 reached in fewer than half the matches, or any veto.
- **neutral:** otherwise.

## Experiment (specification, written before running)

- **Baseline:** turn-001 validated code (commit `4bf3907`); fresh baseline
  batch on this turn's seeds (protocol rule 6 — turn 001's stored baseline
  covers different code+seeds).
- **Treatment:** working tree with the training loop below.
- **Seeds (fresh draw for this turn):** 11, 12, 13, 14, 15, 16, 17, 18, 19, 20.
- **Opponent:** Petra, civ `rome`, difficulty 0 (sandbox, per G1).
- **Map/victory/limit:** `random/mainland` 192, `conquest_civic_centers`,
  treasures disabled, 300 pop cap, biome `generic/temperate`, placement
  `circle`, 20-game-minute limit (trigger aligned in the post-001 tooling
  commit).
- **Canary:** one extra baseline-code match on seed 11; stats must be
  byte-identical to the baseline seed-11 run.

## Implementation

One change: a training gate in `play()` in
`bot/simulation/ai/vercingetorix/vercingetorix.js`, next to the gathering
loop.

- Each play tick (same 8-turn throttle), find the own civil centre
  (`hasClass("CivCentre")`, own entities only — a handful) and, if present:
  queue `cc.train(civ, "units/{civ}/support_civilian", 1)` when **all** hold:
  - `gameState.getResources().food >= 50` (the unit's cost),
  - `gameState.getPopulation() < gameState.getPopulationLimit()` (reservation
    room — started batches already count),
  - `cc.trainingQueue()` is empty or holds one item (keep at most one queued —
    piling reservations would lock population and food).
- Trained civilians become idle on spawn and are picked up by the turn-001
  gathering loop automatically — no extra wiring.
- **Evidence of its own effect:** the existing per-minute samples carry `pop`
  (rises toward 20/20), `food` (drains while training), and the `states`
  histogram (growing `GATHER` counts). No new instrumentation needed.
- **Performance:** no new scans — the CC lookup iterates own entities
  (≤ ~30 this match) once per play tick.

## Verdict

**good.**

Primary metric: 20/20 reached in **10/10 treatment matches**, batch median
time-to-20 = **2 game-minutes** (all seeds; per-minute sample resolution, so
the true time is between 1 and 2 minutes) vs **0/10** on the baseline
(population static at 9). The ≤ 10 min bar is met decisively. Composite
report agrees: `total=+15.12`, verdict **good** (every pair draw–draw;
resourcesGathered, unitsTrained, populationPeak all positive deltas).

- **Vetoes:** JS errors 0 on all 20 matches; canary **PASS**; wall time
  15–19 s per 6000-turn match on both sides (~330–400 t/s) — no regression.
- **In-turn fix:** `ent.train()` requires the resolved template name —
  `trainableEntities` replaces `{native}`/`{civ}` in the token list and does
  an exact `indexOf`, so the unresolved token logged an error per play tick
  (749 errors in the smoke run). Fixed with `gameState.applyCiv(...)`;
  `docs/DEVELOPER_GUIDE.md` AI API reference amended.
- **Behaviour observed:** exactly 11 civilians trained on every seed; food
  oscillates near 0 during the training window then accumulates once the
  housing cap stops training (food ~2100–2900 at minute 19) — the economy is
  now housing-blocked, as expected.
- **Goal grading (G1):** all matches still G1 *Fail* (100 never reached —
  capped at 20). Goal-progress: population grows to the housing cap in ~2
  minutes; housing is the binding constraint (backlog item 2).

## Action

Validate: **keep the change.**

Negative knowledge / observations carried forward:

- The economy idles at the 20-pop cap for ~17 of 20 game-minutes: population
  headroom, not food, is the constraint from minute ~2 on.
- Wood income varies wildly by seed (425–5945) with nearest-supply
  allocation; houses will need a reliable ~1200 wood for 16 houses —
  allocation by need (backlog item 3) may become a prerequisite if house
  building stalls on wood.

## Next

Backlog top: build houses when population headroom runs low — the binding
constraint for G1.
