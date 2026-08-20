# Hypothesis backlog

One line per candidate: the change, the primary metric, and the rationale.
Top of the list goes first. Fed by experiment results; never edit an entry
retroactively to match a verdict.

1. **Allocate gatherers by need (food first, then wood)** instead of pure
   nearest-supply — primary metric: food income per game-minute in the
   `[HARNESS]` samples (batch mean over minutes 5–19). Rationale: turn 003
   proved food is the binding constraint for G1 — training stalls with food
   pinned near 0 while wood/metal accumulate; reaching 100 pop needs ~4550
   food in 20 min (~4/s sustained), need-blind allocation supplies about
   half. E.g. target ratio: enough workers on food to keep training
   saturated, the rest on wood (houses need it), stone/metal ignored for now.
2. **Restore house building** (turn 003's reverted code, from its commit) —
   primary metric: time to 100 population; same experiment design and the
   same ≥ 6/10 threshold as turn 003. Rationale: the mechanism is proven
   (limit rose in 10/10, composite +14.90); it was reverted only because the
   food prerequisite was missing. With allocation fixed, 100 pop in 20 min
   should be reachable.
