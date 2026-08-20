# Turn 005 — build-houses-redux

- **Goal served:** G1 — reach 100 population as fast as possible.
- **Phase:** closed — verdict **good**, change validated. First goal-positive
  turn: G1's metric now exists (batch median time-to-100 = **13 game-min**).

## Hypothesis

> If house building (turn 003's mechanism: one house in flight, 2 builders,
> headroom < 3, wood ≥ 75, stop at limit 105) is restored on top of turn
> 004's food-first allocation, then **100 population is reached before the
> 20-game-minute limit in at least 6 of 10 matches**, because both binding
> constraints found so far are now removed: housing (proven mechanically in
> turn 003) and food income (+112 % in turn 004, ~3.4/s sustained vs the
> ~4550 food needed).

Feasibility arithmetic (from turns 002–004 evidence):

- 91 more civilians = 4550 food at ~3.4/s and rising (each new worker adds
  ~0.17/s food income) → food stops binding around minute 8–12.
- Training rate cap: the civil centre's single queue trains 1 worker per
  8 s → 80 more workers need ≥ 10.7 min of saturated queueing; reachable
  inside 20 min only if training never starves — exactly what turn 004
  provides.
- 16 houses ≈ 1200 wood; the 25 % wood quota produced ~2200 wood per match
  in turn 004 — ample.

**Primary metric (M):** time to 100 population (first per-minute `[HARNESS]`
sample with pop used ≥ 100), per match; batch summary = count reaching 100 +
median time. Baseline (turn-004 code) stays at 20.

**Verdict thresholds (same as turn 003, pre-registered in the backlog):**

- **good:** ≥ 6/10 matches reach 100 pop, no JS-error/determinism veto.
- **bad:** the population limit never rises above 20 in ≥ half the matches,
  or any veto.
- **neutral:** otherwise.

## Experiment (specification, written before running)

- **Baseline:** turn-004 validated code (= current HEAD, commit `1609979`);
  fresh baseline batch on this turn's seeds.
- **Treatment:** working tree with the house-building loop restored.
- **Seeds (fresh draw for this turn):** 41, 42, 43, 44, 45, 46, 47, 48, 49, 50.
- **Opponent:** Petra, civ `rome`, difficulty 0 (sandbox, per G1).
- **Map/victory/limit:** `random/mainland` 192, `conquest_civic_centers`,
  treasures disabled, 300 pop cap, biome `generic/temperate`, placement
  `circle`, 20-game-minute limit.
- **Canary:** one extra baseline-code match on seed 41; stats must be
  byte-identical to the baseline seed-41 run.

## Implementation

One change: re-apply turn 003's house-building code (including its in-turn
veto fix — the `supplyIds` null guard in `spotBlocked`) to the current bot.
The code is re-written from the turn-003 record: the turn-003 journal
wrongly claimed the reverted code was recoverable from its commit — it was
reverted before committing and is **not** in git history (correction
recorded here; the turn-003 journal gets an erratum line in this turn's
commit).

No interaction changes with turn 004's allocation: builders are drafted
from civilians by proximity and resume gathering via autocontinue; the
75/25 quota then re-balances on its own.

- **Evidence:** sample `pop` field shows the limit rising; `states`
  histogram shows `INDIVIDUAL.REPAIR.*`; food should no longer pin at 0
  while the queue starves.
- **Performance:** unchanged from turn 003 — bounded per-tick work, no new
  map scans.

## Verdict

**good.**

Primary metric: 100 population reached in **10/10 matches** (bar: ≥ 6), with
times 13–14 game-minutes on 9 seeds and 19 on one (median **13**, per-minute
sample resolution). The baseline never leaves 20. Composite report:
`total=+14.79`, verdict **good**. The turn-003/004 constraint chain
(housing, then food) is confirmed closed.

- **Vetoes:** JS errors 0 on all 20 matches; canary **PASS**.
- **Performance watch (not a veto, recorded per rule 9):** treatment wall
  26–33 s vs baseline 15–20 s for the same 6000 turns (~200 vs ~350 t/s).
  The drop tracks entity count (105 units + 17 buildings moving/gathering
  vs 20 idle units — simulation pathfinding/gathering cost), not AI
  decision cost: decisions stay on the 8-turn throttle with bounded loops,
  and turn 002 (same logic at 20 pop) ran at baseline speed. Turn rate stays
  ~10× real-time. Watch this as the bot grows; no protocol change yet.
- **Goal grading (G1):** **10/10 matches reach 100 pop — the goal's first
  non-Fail batch.** Best batch median so far: **13 game-minutes**. G1
  continues: the goal is achieved when 5 consecutive turns fail to beat 13.

## Action

Validate: **keep the change.** The bot now plays a complete economic loop:
gather by need → train continuously → house ahead of the cap → 100 pop at
minute ~13.

Observations carried forward:

- The civil centre's single training queue is now the rate limiter:
  ~10.7 min minimum for 80+ workers serial; everything else (housing, food)
  is ahead of it. Parallel training (houses + Fertility Festival tech) is
  the backlog's top candidate.
- One seed (42) reached 100 only at minute 19 — outliers worth a look if
  variance matters later (likely late food ramp on a food-poor start).

## Next

Backlog top: parallel training (research `unlock_civilians_house_generic`,
then train from houses) to cut the serial-queue floor below 10.7 min.

