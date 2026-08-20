# Hypothesis backlog

One line per candidate: the change, the primary metric, and the rationale.
Top of the list goes first. Fed by experiment results; never edit an entry
retroactively to match a verdict.

1. **Raise the food-gatherer share** (food while food gatherers are below
   ~90 % of all gatherers, up from 75 %) — primary metric: time to 100
   population (G1 batch median, to beat: **11 game-min**). Rationale: turn
   007 evidence — training stalls with food < 50 for 8–14 of 19 match
   minutes while wood banks 200–2500 unused; food income, not the
   population cap, paces growth.
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
