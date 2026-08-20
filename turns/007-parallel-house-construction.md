# Turn 007 — parallel-house-construction

- **Goal served:** G1 — reach 100 population as fast as possible. Best batch
  median to beat: **11 game-minutes** (turn 006).

## Hypothesis

> If the bot keeps up to **two** houses in flight — placing the next house
> while one is still under construction, gated on wood ≥ 75 × (in-flight +
> 1) — then the batch median time-to-100 drops from **11 to ≤ 10
> game-minutes**, because the population cap lift is currently serialized at
> one house at a time (placement walk + ~18.5 s build with 2 builders ≈
> 20–30 s per house) and the cap trailed usage through the minute 6–10
> sprint in turns 005–006; two parallel builds double the cap-lift
> throughput exactly when training stalls at the cap.

Grounding:

- Turn 005/006 evidence: the cap trailed usage through the sprint — the
  `pop` samples show training waiting on house completions.
- G1 needs 17 houses (CC 20 + 17 × 5 = 105); serialized at ~25 s each that
  is ~7 game-minutes of cap lift, all of it on the critical path while the
  trainers can produce workers faster than the cap rises.
- Build time scales as 30 / N^0.7 s (backlog note, from
  `docs/game_description/`); with 2 foundations in flight each gets 1
  placer + 2 repairers ≈ 3 builders ≈ 13.5 s, so the pair completes in
  roughly the time one house took before.

**Primary metric (M):** time to 100 population (first per-minute `[HARNESS]`
sample with pop used ≥ 100), batch median over the 10 seeds.

**Verdict thresholds (single-metric; backlog top entry, pre-registered):**

- **good:** median ≤ 10 min, still ≥ 6/10 matches reaching 100, no
  JS-error/determinism veto.
- **bad:** median ≥ 13 min, or fewer than 6/10 reaching 100, or any veto.
- **neutral:** otherwise (median 11–12).

## Experiment (specification, written before running)

- **Baseline:** turn-006 validated code (= current HEAD, commit `3f5ba4d`);
  fresh baseline batch on this turn's seeds.
- **Treatment:** working tree with the parallel-construction change below.
- **Seeds (fresh draw for this turn):** 61, 62, 63, 64, 65, 66, 67, 68, 69, 70.
- **Opponent:** Petra, civ `rome`, difficulty 0 (sandbox, per G1).
- **Map/victory/limit:** `random/mainland` 192, `conquest_civic_centers`,
  treasures disabled, 300 pop cap, biome `generic/temperate`, placement
  `circle`, 20-game-minute limit.
- **Canary:** one extra baseline-code match on seed 61; stats must be
  byte-identical to the baseline seed-61 run.

## Implementation

One change: up to two houses in flight in `buildHouses`
(`bot/simulation/ai/vercingetorix/vercingetorix.js`).

- `houseFoundationId` (single id) becomes `houseFoundationIds` (array);
  each play tick drops ids whose entity is no longer a Foundation (the
  existing completion detection, now a filter). Serialize/Deserialize
  updated to match (no save-format compatibility kept, per policy).
- Placement gate: at most 2 foundations in flight, and wood must cover the
  in-flight houses plus the new one (`wood < 75 * (inFlight + 1)` — the
  second house needs 150 wood banked). Headroom (< 3) and limit (< 105)
  gates unchanged; still one placement per play tick, so `housePending`
  stays a single spot.
- Builder assignment unchanged: 1 civilian places, the 2 nearest repair
  the foundation on the next tick. With 2 in flight that is up to ~6
  civilians on construction during the sprint.
- **Evidence of its own effect:** the per-minute `[HARNESS]` samples carry
  `pop` as `used/limit` — parallel construction shows as limit steps of
  +10 within one minute instead of serialized +5 steps, and the `states`
  histogram shows more builders in BUILD/REPAIR states during the sprint.
  No new instrumentation needed.
- **Performance:** the foundation check filters a ≤ 2-element array; the
  rest reuses the existing per-tick own-entities loops. No new scans.

## Verdict

**neutral.**

Primary metric: batch median time-to-100 = **12.5 game-minutes** on both
sides (baseline times 9–16, treatment 9–19 on the same seeds; paired deltas
0, 0, −3, +1, 0, +1, 0, +1, −1, −1). 10/10 matches reach 100 on both sides.

- **Vetoes:** JS errors 0 on all 21 matches; canary **PASS**; wall 30–38 s
  per match both sides — no performance regression.
- **Composite report (for the record):** `total=+0.24`, "neutral" — all
  pairs draw–draw at the time limit.
- **Why neutral — the hypothesis's premise is falsified as the binding
  gate:** the change works mechanically (treatment minutes spent at the
  population cap drop, e.g. seed 61: 7 → 3; seed 63: 6 → 2), but training
  stalls on **food**, not on the cap: minutes below cap with food < 50
  dominate and even rise (seed 61: 8 → 12; seed 63: 11 → 14; the extra
  builders come off gathering). Wood banks 200–2500 unused while food sits
  at 16–45 through the sprint — the food:wood allocation, not house
  throughput, paces growth.
- Seed 63's −3 is not the mechanism: Rome killed 7 workers in the
  treatment run (baseline: 1) — behavior divergence reshuffles Roman
  harassment; deterministic luck per seed, not a systematic cost.
- **Goal grading (G1):** best batch median unbeaten (**11**, turn 006 —
  different seed set; medians compare only within a paired batch).
  Consecutive turns without beating the best: **1**.

## Action

Neutral → diagnosed (food income, not cap lift, is the binding constraint;
no small in-turn fix to house parallelism changes that, and re-running the
same treatment is bit-identical by determinism). **Reverted** — the code
leaves no trace; negative knowledge recorded here and in the backlog.

## Next

Backlog reworked: drop parallel house construction (falsified premise);
new top hypothesis targets the food side — raise the food-gatherer share
(75 % → 90 %) so training stops stalling on food < 50.
