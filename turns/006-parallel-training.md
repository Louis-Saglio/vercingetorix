# Turn 006 — parallel-training

- **Goal served:** G1 — reach 100 population as fast as possible.
- **Phase:** closed — verdict **good**, change validated. New G1 best batch
  median: **11 game-minutes** (was 13).

## Hypothesis

> If the bot researches `unlock_civilians_house_generic` (Fertility
> Festival) at its first completed house and then trains
> `support_civilian_house` from every completed house under the same
> food/population gates as the civil centre, then the batch median
> time-to-100 drops from **13 to ≤ 11 game-minutes**, because the civil
> centre's single 8 s queue (≥ 10.7 min floor for 80+ workers, the turn-005
> rate limiter) is supplemented by every house's parallel 30 s queue.

Grounding (verified in the pinned 0.28.0 data):

- Houses research `unlock_civilians_house_generic` (250 food, 100 wood, 100
  metal, 60 s; `template_structure_civic_house.xml` Researcher list) and then
  train `units/{civ}/support_civilian_house` — same civilian, **30 s** build
  time (`units/gaul/support_civilian_house.xml`).
- Turn 005 evidence: at minute ~6 the bot has ~6 houses; research done by
  ~minute 8, then ~6 parallel queues ≈ 12 workers/min + the CC's 7.5/min ≈
  19.5/min vs 7.5/min serial. Workers still needed at that point ≈ 50 →
  ~3 min → 100 around minute 10–11.
- The tech needs **100 metal** — the allocation ignores metal today (turn
  004). Until the tech is researched, the wood quota slot sends workers to
  metal while the stockpile is < 100 (one worker on metal at 0.35/s banks
  100 in ~5 min; the wood quota is otherwise ~2200/match — ample slack).

**Primary metric (M):** time to 100 population (first per-minute `[HARNESS]`
sample with pop used ≥ 100), batch median over the 10 seeds.

**Verdict thresholds (single-metric; target pre-registered in the backlog):**

- **good:** median ≤ 11 min, still ≥ 6/10 matches reaching 100, no
  JS-error/determinism veto.
- **bad:** median ≥ 15 min, or fewer than 6/10 reaching 100, or any veto.
- **neutral:** otherwise (median 12–14).

## Experiment (specification, written before running)

- **Baseline:** turn-005 validated code (= current HEAD, commit `389cd84`);
  fresh baseline batch on this turn's seeds.
- **Treatment:** working tree with the parallel-training change below.
- **Seeds (fresh draw for this turn):** 51, 52, 53, 54, 55, 56, 57, 58, 59, 60.
- **Opponent:** Petra, civ `rome`, difficulty 0 (sandbox, per G1).
- **Map/victory/limit:** `random/mainland` 192, `conquest_civic_centers`,
  treasures disabled, 300 pop cap, biome `generic/temperate`, placement
  `circle`, 20-game-minute limit.
- **Canary:** one extra baseline-code match on seed 51; stats must be
  byte-identical to the baseline seed-51 run.

## Implementation

One change: parallel training in `play()`
(`bot/simulation/ai/vercingetorix/vercingetorix.js`).

- Research gate: once per play tick, if `!isResearched` and
  `!isResearching("unlock_civilians_house_generic")` and resources cover
  250 food / 100 wood / 100 metal, order the first completed own house
  (`hasClass("House") && !hasClass("Foundation")`) to `research(...)` it.
- House training: in the existing own-entities loop, every completed house
  goes through the same `trainWorker` gate as the civil centre (food ≥ 50,
  population room, queue empty), training
  `applyCiv("units/{civ}/support_civilian_house")` — only once the tech is
  researched (`trainWorker` gains the template and a researched check).
- Metal while saving: in the allocation step, if the tech is neither
  researched nor researching and `metal < 100`, the wood quota slot assigns
  the nearest **metal** supply instead of wood.
- **Evidence of its own effect:** the samples show `metal` rising to ~100
  then stopping (the one-off tech saving), `pop` climbing faster after the
  research minute, and the `states` histogram's gather mix. No new
  instrumentation needed.
- **Performance:** the house loop reuses the existing per-tick own-entities
  iteration; `isResearched`/`isResearching` are map lookups. No new scans.

## Verdict

**good.**

Primary metric: batch median time-to-100 = **11 game-minutes** (times
10–13 on 9 seeds, 16 on one) vs **13** on the paired baseline (13 on 8
seeds, 14 and 16 on two) — the ≤ 11 bar is met, 10/10 matches reach 100 on
both sides, and the composite's blind spot here (it has no time-to-100
input) is exactly why the turn declared single-metric thresholds.

- **Vetoes:** JS errors 0 on all 20 matches; canary **PASS**; wall 29–34 s
  per 6000-turn match on both sides — no regression versus the (already
  105-pop) baseline.
- **Composite report (for the record):** `total=-0.05`, "neutral" — all
  pairs draw–draw at the time limit with equal population peaks; the
  composite cannot see training speed.
- **Behaviour observed:** the tech is researched around game-minute 2 (its
  100 metal comes from the 300 starting stock — the metal-saving branch
  never fires in practice; harmless dead path, noted); house queues roughly
  double the training rate from minute ~3; food dips to ~30–90 during the
  minute 6–10 sprint but never deadlocks training.
- **Goal grading (G1):** 10/10 reach 100; new best batch median **11**
  (previous 13). Consecutive turns without beating the best: reset to 0.

## Action

Validate: **keep the change.**

Observations carried forward:

- Remaining variance is start-quality driven (the 16-minute outlier on seed
  53 exists on both sides — food-poor start); the mechanism is stable.
- Next levers by expected value: earlier/parallel house construction (the
  cap lift still gates the sprint), a storehouse near woodlines as supplies
  deplete, more builders per house.

## Next

Backlog top: parallel house construction. **Louis's instruction
(2026-08-20): stop after this turn — do not start turn 007
automatically.** Recorded in `CURRENT_TURN.md`.
