# Hypothesis backlog

One line per candidate: the change, the primary metric, and the rationale.
Top of the list goes first. Fed by experiment results; never edit an entry
retroactively to match a verdict.

1. **Build farm fields next to the civil centre** once near-CC food
   supplies deplete (or from the start — ground the trade-off) — primary
   metric: time to 100 population (G1 batch median, to beat: **11
   game-min**). Rationale: turn 008 evidence — effective food income is
   walk-distance-bound (≈ 0.17/s per assigned food gatherer during the
   sprint vs 0.4–0.8/s for wood next to the CC); farms give short, fixed
   walks. Ground field cost, gather rate and max gatherers in
   `docs/game_description/` before writing the turn.
2. **Build a storehouse near dense woodlines** — primary metric: wood income
   per game-minute. Rationale: travel time dominates late-game gathering as
   near-CC supplies deplete (`resources_and_gathering.md` — dropsite
   distance drives effective rates). Weakened by turn 007: wood is
   over-gathered relative to food under the current allocation.
3. **More builders per house foundation** (3–4 instead of 2) — primary
   metric: time to 100 population. Rationale: build time scales as
   30 / N^0.7 s; 4 builders ≈ 11.4 s vs 18.5 s with 2. Weakened by turn
   007: cap lift is rarely the binding gate, and extra builders come off
   food gathering.

Negative knowledge (tested, do not retry unchanged):

- **Parallel house construction (2 in flight, wood-gated)** — turn 007,
  neutral, reverted: the cap lift is not the binding constraint; training
  stalls on food < 50 far more minutes than at the cap.
- **Raise the food-gatherer share (75 % → 90 %, wood-floored)** — turn 008,
  neutral (direction negative), reverted: food income is
  walk-distance-bound, not share-bound; extra food gatherers mostly walk.
  Also: the food-order count misses gatherers returning to the dropsite,
  so a bare high quota locks the mix at ~100 % food and deadlocks house
  building (caught by the smoke test).
